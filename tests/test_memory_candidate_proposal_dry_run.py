from __future__ import annotations

import io
import json
from copy import deepcopy
from pathlib import Path

from hermes_memory_fabric.codex_task_summary_ingestion import (
    candidates_to_jsonl,
    generate_codex_task_summary_candidates,
)
from hermes_memory_fabric.memory_block_review_queue import validate_review_queue_item
from hermes_memory_fabric.memory_blocks import validate_memory_block_candidate
from hermes_memory_fabric.memory_candidate_proposal_dry_run import (
    cli_main,
    run_memory_candidate_proposal_dry_run,
)
from hermes_memory_fabric.memory_governance_submission_packet import (
    validate_governance_submission_packet,
)
from hermes_memory_fabric.memory_human_review_outcome_gate import (
    validate_human_review_outcome_candidate,
)
from hermes_memory_fabric.memory_proposal_draft_builder import validate_memory_proposal_draft
from hermes_memory_fabric.memory_proposal_governance_gate import (
    validate_governance_submission_candidate,
)
from hermes_memory_fabric.memory_real_proposal_creation_plan import (
    validate_real_proposal_creation_plan,
)
from hermes_memory_fabric.memory_real_proposal_dry_run import validate_real_proposal_dry_run
from hermes_memory_fabric.memory_review_decision_gate import validate_review_decision_candidate


def _summary() -> str:
    return """# v1.5.0 Memory Candidate Proposal Dry Run

Goal / Purpose
Convert v1.3.1 Memory Fabric candidates into isolated Memory Block proposal previews.

Included / Changed files
- src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py
- scripts/propose_memory_candidates_dry_run.py

Validation
- focused pytest
- smoke_memory_candidate_proposal_dry_run.py

Boundary
- Dry-run adapter only.
- No proposal file writes.
- No operation ledger writes.
- No memory writes.
- No graph writes.
- No token files.
- No approval audit writes.
- No provider tools.

Version
1.5.0

Result
Generated local proposal preview objects from low-risk candidate JSONL.
"""


def _candidates():
    return generate_codex_task_summary_candidates(_summary())


def _candidate():
    return next(candidate for candidate in _candidates() if candidate["risk_level"] == "low")


def _hermes_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def _assert_real_write_flags_false(result):
    assert result["created_real_proposal"] is False
    assert result["writes_proposal_files"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["writes_token_files"] is False
    assert result["writes_approval_audit"] is False
    assert result["applies_proposals"] is False
    assert result["provider_tools"] == []


def _assert_preview_valid(preview):
    assert validate_memory_block_candidate(preview["memory_block_candidate"]) == {"valid": True, "errors": []}
    assert validate_review_queue_item(preview["review_queue_item"]) == {"valid": True, "errors": []}
    assert validate_review_decision_candidate(preview["review_decision_candidate"]) == {
        "valid": True,
        "errors": [],
    }
    assert validate_memory_proposal_draft(preview["proposal_draft"]) == {"valid": True, "errors": []}
    assert validate_governance_submission_candidate(preview["governance_submission_candidate"]) == {
        "valid": True,
        "errors": [],
    }
    assert validate_governance_submission_packet(preview["governance_submission_packet"]) == {
        "valid": True,
        "errors": [],
    }
    assert validate_human_review_outcome_candidate(preview["human_review_outcome_candidate"]) == {
        "valid": True,
        "errors": [],
    }
    assert validate_real_proposal_creation_plan(preview["real_proposal_creation_plan"]) == {
        "valid": True,
        "errors": [],
    }
    assert validate_real_proposal_dry_run(preview["real_proposal_dry_run"]) == {"valid": True, "errors": []}


def test_low_risk_v13_candidates_produce_valid_dry_run_proposal_previews():
    candidates = _candidates()

    result = run_memory_candidate_proposal_dry_run(candidates)

    assert result["version"] == "1.5.0"
    assert result["dry_run"] is True
    assert result["accepted_count"] == len(candidates)
    assert result["rejected_count"] == 0
    assert result["locked_count"] == 0
    _assert_real_write_flags_false(result)
    for candidate, preview in zip(candidates, result["proposal_previews"]):
        block = preview["memory_block_candidate"]
        metadata = block["metadata"]
        assert block["block_type"] == "project_context"
        assert block["status"] == "review_required"
        assert block["version"] == "0.1"
        assert block["project_scope"] == candidate["project_id"]
        assert block["content"] == candidate["content"]
        assert block["source_fact_ids"] == [candidate["id"]]
        assert metadata["tags"] == candidate["tags"]
        assert metadata["provenance"] == candidate["provenance"]
        assert metadata["source"] == candidate["source"]
        assert metadata["source_id"] == candidate["source_id"]
        assert metadata["risk_level"] == candidate["risk_level"]
        assert preview["real_proposal_dry_run"]["proposal_record_preview"]["written"] is False
        assert preview["real_proposal_dry_run"]["operation_ledger_preview"]["written"] is False
        _assert_real_write_flags_false(preview)
        _assert_preview_valid(preview)


def test_high_risk_candidates_are_locked_by_default():
    candidate = deepcopy(_candidate())
    candidate["risk_level"] = "high"

    result = run_memory_candidate_proposal_dry_run([candidate])

    assert result["accepted_count"] == 0
    assert result["rejected_count"] == 0
    assert result["locked_count"] == 1
    assert result["proposal_previews"] == []
    assert result["rejected_candidates"][0]["disposition"] == "locked"
    assert result["rejected_candidates"][0]["reasons"] == ["risk_level_not_allowed:high"]
    _assert_real_write_flags_false(result)


def test_unsafe_governance_candidates_are_rejected():
    candidate = deepcopy(_candidate())
    candidate["governance"]["dry_run"] = False
    candidate["governance"]["would_write_memory"] = True

    result = run_memory_candidate_proposal_dry_run([candidate])

    assert result["accepted_count"] == 0
    assert result["rejected_count"] == 1
    assert result["locked_count"] == 0
    rejected = result["rejected_candidates"][0]
    assert rejected["disposition"] == "rejected"
    assert "governance_dry_run_must_be_true" in rejected["reasons"]
    assert "governance_would_write_memory_must_be_false" in rejected["reasons"]
    _assert_real_write_flags_false(result)


def test_input_candidates_are_not_mutated():
    candidates = _candidates()
    before = deepcopy(candidates)

    result = run_memory_candidate_proposal_dry_run(candidates)
    result["proposal_previews"][0]["memory_block_candidate"]["metadata"]["tags"].append("changed")

    assert candidates == before


def test_output_is_deterministic():
    candidates = _candidates()

    first = run_memory_candidate_proposal_dry_run(candidates)
    second = run_memory_candidate_proposal_dry_run(candidates)

    assert first == second
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_no_writes_to_hermes_home_or_proposal_ledger_token_audit_files(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    before = _hermes_files(hermes_home)

    result = run_memory_candidate_proposal_dry_run(_candidates())

    after = _hermes_files(hermes_home)
    assert before == []
    assert after == []
    assert not (hermes_home / "memory" / "proposals" / "memory_write_proposals.jsonl").exists()
    assert not (hermes_home / "memory" / "audit" / "memory_operation_ledger.jsonl").exists()
    assert not (hermes_home / "memory" / "tokens").exists()
    assert not (hermes_home / "memory" / "approval_audit").exists()
    _assert_real_write_flags_false(result)


def test_generated_preview_passes_existing_relevant_validators():
    result = run_memory_candidate_proposal_dry_run([_candidate()])

    _assert_preview_valid(result["proposal_previews"][0])


def test_cli_stdout_mode_does_not_write_files(tmp_path):
    input_path = tmp_path / "candidates.jsonl"
    input_path.write_text(candidates_to_jsonl(_candidates()), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    exit_code = cli_main(["--input", str(input_path)], stdout=stdout, stderr=stderr)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    result = json.loads(stdout.getvalue())
    assert exit_code == 0
    assert after == before == [Path("candidates.jsonl")]
    assert stderr.getvalue() == ""
    assert result["accepted_count"] >= 1
    _assert_real_write_flags_false(result)


def test_cli_explicit_output_writes_only_to_requested_path(tmp_path):
    input_path = tmp_path / "candidates.jsonl"
    output_path = tmp_path / "proposal-dry-run.json"
    input_path.write_text(candidates_to_jsonl(_candidates()), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = cli_main(
        ["--input", str(input_path), "--output", str(output_path), "--print-summary"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == 0
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*")) == [
        Path("candidates.jsonl"),
        Path("proposal-dry-run.json"),
    ]
    assert stdout.getvalue() == ""
    assert "memory_candidate_proposal_dry_run_summary=" in stderr.getvalue()
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["accepted_count"] >= 1
    _assert_real_write_flags_false(result)
