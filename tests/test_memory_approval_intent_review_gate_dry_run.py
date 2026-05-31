from __future__ import annotations

import io
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from hermes_memory_fabric.codex_task_summary_ingestion import (
    candidates_to_jsonl,
    generate_codex_task_summary_candidates,
)
from hermes_memory_fabric.memory_approval_intent_dry_run import run_memory_approval_intent_dry_run
from hermes_memory_fabric.memory_approval_intent_review_gate_dry_run import (
    run_memory_approval_intent_review_gate_dry_run,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "scripts" / "review_approval_intent_dry_run.py"


def _summary() -> str:
    return """# v1.8.0 Approval Intent Review Gate Dry Run

Goal / Purpose
Convert v1.7 approval intent dry-run objects plus explicit reviewer decisions into review outcome candidates.

Included / Changed files
- src/hermes_memory_fabric/memory_approval_intent_review_gate_dry_run.py
- scripts/review_approval_intent_dry_run.py

Validation
- focused pytest
- smoke_approval_intent_review_gate_dry_run.py

Boundary
- Dry-run review outcome only.
- No token issuance.
- No proposal creation.
- No operation ledger append.
- No executor invocation.
- No memory write.

Version
1.8.0

Result
Generated local approval intent review outcome candidates.
"""


def _intent() -> dict[str, object]:
    candidates = generate_codex_task_summary_candidates(_summary())
    low_risk = [candidate for candidate in candidates if candidate["risk_level"] == "low"]
    preview = run_memory_candidate_proposal_dry_run(low_risk)
    return run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)


def _assert_no_write_review(result: dict[str, object]) -> None:
    assert result["dry_run"] is True
    assert result["approval_token_issued"] is False
    assert result["approval_token_id"] is None
    assert result["creates_real_proposal"] is False
    assert result["writes_proposal_files"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["writes_token_files"] is False
    assert result["writes_approval_audit"] is False
    assert result["invokes_real_executor"] is False
    assert result["applies_proposals"] is False
    assert result["provider_tools"] == []


def _hermes_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


def test_approved_outcome_from_valid_v17_intent_and_decision_approve():
    intent = _intent()

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve", "looks safe")

    assert result["version"] == "1.8.0"
    assert result["review_gate_status"] == "approved"
    assert result["review_outcome_status"] == "approved"
    assert result["review_outcome_kind"] == "approval_intent_review_outcome_candidate"
    assert result["review_outcome_id"].startswith("approval-intent-review-outcome-dry-run-")
    assert result["reviewer_decision"] == "approve"
    assert result["reviewer_reason"] == "looks safe"
    assert result["source_approval_intent_version"] == "1.7.0"
    assert result["source_approval_intent_status"] == "ready"
    assert result["source_approval_intent_id"] == intent["approval_intent_id"]
    assert result["source_human_review_required"] is True
    assert result["required_next_step"] == "manual_review_outcome_recorded_no_token_issued"
    _assert_no_write_review(result)


def test_changes_requested_outcome_from_valid_v17_intent_and_decision_request_changes():
    result = run_memory_approval_intent_review_gate_dry_run(_intent(), "request_changes")

    assert result["review_gate_status"] == "changes_requested"
    assert result["review_outcome_status"] == "changes_requested"
    assert result["required_next_step"] == "return_to_approval_intent_source_for_revision"
    _assert_no_write_review(result)


def test_rejected_outcome_from_valid_v17_intent_and_decision_reject():
    result = run_memory_approval_intent_review_gate_dry_run(_intent(), "reject")

    assert result["review_gate_status"] == "rejected"
    assert result["review_outcome_status"] == "rejected"
    assert result["required_next_step"] == "stop_no_token_no_write"
    _assert_no_write_review(result)


def test_locked_when_source_approval_intent_status_is_locked():
    intent = _intent()
    intent["approval_intent_status"] = "locked"

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

    assert result["review_gate_status"] == "locked"
    assert "source_approval_intent_status_must_be_ready" in result["safety_summary"][
        "source_approval_intent_errors"
    ]
    assert result["required_next_step"] == "repair_source_approval_intent_or_review_decision"
    _assert_no_write_review(result)


def test_locked_when_source_approval_intent_status_is_rejected():
    intent = _intent()
    intent["approval_intent_status"] = "rejected"

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

    assert result["review_gate_status"] == "locked"
    assert "source_approval_intent_status_must_be_ready" in result["safety_summary"][
        "source_approval_intent_errors"
    ]
    _assert_no_write_review(result)


def test_locked_when_source_version_is_not_170():
    intent = _intent()
    intent["version"] = "1.6.0"

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

    assert result["review_gate_status"] == "locked"
    assert "source_approval_intent_version_must_be_1.7.0" in result["safety_summary"][
        "source_approval_intent_errors"
    ]
    _assert_no_write_review(result)


def test_locked_when_source_is_missing_required_keys():
    intent = _intent()
    del intent["approval_intent_id"]

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

    assert result["review_gate_status"] == "locked"
    assert "missing_approval_intent_id" in result["safety_summary"]["source_approval_intent_errors"]
    _assert_no_write_review(result)


def test_locked_when_any_source_no_write_flag_is_unsafe():
    for flag in (
        "approval_token_issued",
        "creates_real_proposal",
        "writes_proposal_files",
        "writes_operation_ledger",
        "writes_memory",
        "writes_graph",
        "writes_config",
        "writes_sqlite",
        "writes_token_files",
        "writes_approval_audit",
        "invokes_real_executor",
        "applies_proposals",
    ):
        intent = _intent()
        intent[flag] = True

        result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

        assert result["review_gate_status"] == "locked"
        assert f"source_{flag}_must_be_false" in result["safety_summary"][
            "source_approval_intent_errors"
        ]
        _assert_no_write_review(result)


def test_locked_when_source_provider_tools_is_not_empty():
    intent = _intent()
    intent["provider_tools"] = ["unsafe_tool"]

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")

    assert result["review_gate_status"] == "locked"
    assert "source_provider_tools_must_be_empty" in result["safety_summary"][
        "source_approval_intent_errors"
    ]
    _assert_no_write_review(result)


def test_locked_when_reviewer_decision_is_unsupported():
    result = run_memory_approval_intent_review_gate_dry_run(_intent(), "defer")

    assert result["review_gate_status"] == "locked"
    assert "reviewer_decision_must_be_supported" in result["safety_summary"][
        "source_approval_intent_errors"
    ]
    _assert_no_write_review(result)


def test_deterministic_review_outcome_id():
    intent = _intent()

    first = run_memory_approval_intent_review_gate_dry_run(intent, "approve", "same reason")
    second = run_memory_approval_intent_review_gate_dry_run(intent, "approve", "same reason")

    assert first["review_outcome_id"] == second["review_outcome_id"]
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_input_approval_intent_dict_is_not_mutated():
    intent = _intent()
    before = deepcopy(intent)

    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")
    result["source_approval_intent_snapshot"]["safety_summary"].clear()

    assert intent == before


def test_cli_stdout_writes_no_files(tmp_path):
    intent_path = tmp_path / "intent.json"
    intent_path.write_text(json.dumps(_intent(), sort_keys=True), encoding="utf-8")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())

    completed = _run_cli(["--input", str(intent_path), "--decision", "approve"], tmp_path)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert after == before == [Path("intent.json")]
    assert result["review_gate_status"] == "approved"
    _assert_no_write_review(result)


def test_cli_explicit_output_writes_only_requested_file(tmp_path):
    intent_path = tmp_path / "intent.json"
    output_path = tmp_path / "review.json"
    intent_path.write_text(json.dumps(_intent(), sort_keys=True), encoding="utf-8")

    completed = _run_cli(
        [
            "--input",
            str(intent_path),
            "--decision",
            "approve",
            "--reason",
            "reviewed",
            "--output",
            str(output_path),
            "--print-summary",
        ],
        tmp_path,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert "approval_intent_review_gate_dry_run_summary=" in completed.stderr
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file()) == [
        Path("intent.json"),
        Path("review.json"),
    ]
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["review_gate_status"] == "approved"
    assert result["reviewer_reason"] == "reviewed"
    _assert_no_write_review(result)


def test_cli_refuses_output_under_hermes_home(tmp_path):
    hermes_home = tmp_path / "hermes-home"
    intent_path = tmp_path / "intent.json"
    output_path = hermes_home / "review.json"
    intent_path.write_text(json.dumps(_intent(), sort_keys=True), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    env["HERMES_HOME"] = str(hermes_home)

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--input",
            str(intent_path),
            "--decision",
            "approve",
            "--output",
            str(output_path),
        ],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert "refusing_output_under_hermes_home" in completed.stderr
    assert _hermes_files(hermes_home) == []


def test_smoke_chain_remains_no_write(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    candidates = generate_codex_task_summary_candidates(_summary())
    candidate_jsonl = candidates_to_jsonl(candidates)
    loaded_candidates = [json.loads(line) for line in io.StringIO(candidate_jsonl) if line.strip()]

    before = _hermes_files(hermes_home)
    preview = run_memory_candidate_proposal_dry_run(loaded_candidates)
    intent = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    result = run_memory_approval_intent_review_gate_dry_run(intent, "approve")
    after = _hermes_files(hermes_home)

    assert intent["approval_intent_status"] == "ready"
    assert result["review_gate_status"] == "approved"
    _assert_no_write_review(result)
    assert before == []
    assert after == []


def _run_cli(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    return subprocess.run(
        [sys.executable, str(CLI_SCRIPT), *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
