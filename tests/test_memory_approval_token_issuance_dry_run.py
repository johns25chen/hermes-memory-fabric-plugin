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
from hermes_memory_fabric.memory_approval_token_issuance_dry_run import (
    approval_token_issuance_dry_run_to_json,
    run_memory_approval_token_issuance_dry_run,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "scripts" / "issue_approval_token_dry_run.py"


def _summary() -> str:
    return """# v1.9.0 Approval Token Issuance Dry Run

Goal / Purpose
Convert an approved v1.8 approval-intent review outcome into a token issuance dry-run candidate.

Included / Changed files
- src/hermes_memory_fabric/memory_approval_token_issuance_dry_run.py
- scripts/issue_approval_token_dry_run.py

Validation
- focused pytest
- smoke_approval_token_issuance_dry_run.py

Boundary
- Dry-run candidate only.
- No usable token.
- No token file.
- No proposal creation.
- No operation ledger append.
- No executor invocation.
- No memory write.

Version
1.9.0

Result
Generated local approval token issuance dry-run candidates.
"""


def _review_outcome() -> dict[str, object]:
    candidates = generate_codex_task_summary_candidates(_summary())
    low_risk = [candidate for candidate in candidates if candidate["risk_level"] == "low"]
    preview = run_memory_candidate_proposal_dry_run(low_risk)
    intent = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    return run_memory_approval_intent_review_gate_dry_run(intent, "approve", "looks safe")


def _assert_no_write_token(result: dict[str, object]) -> None:
    assert result["dry_run"] is True
    assert result["approval_token_issued"] is False
    assert result["approval_token_id"] is None
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False
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


def test_ready_token_issuance_dry_run_from_valid_approved_v18_review_outcome():
    review = _review_outcome()

    result = run_memory_approval_token_issuance_dry_run(
        review,
        issuer="manual-human-review",
        issuance_reason="ready to draft",
    )

    assert result["version"] == "1.9.0"
    assert result["token_issuance_status"] == "ready"
    assert result["token_draft_id"].startswith("approval-token-issuance-draft-dry-run-")
    assert result["token_intent_id"].startswith("approval-token-intent-dry-run-")
    assert result["token_kind"] == "approval_token_issuance_draft_candidate"
    assert result["token_status"] == "draft_ready"
    assert result["issuer"] == "manual-human-review"
    assert result["issuance_reason"] == "ready to draft"
    assert result["source_review_gate_version"] == "1.8.0"
    assert result["source_review_gate_status"] == "approved"
    assert result["source_review_outcome_id"] == review["review_outcome_id"]
    assert result["source_reviewer_decision"] == "approve"
    assert result["source_required_next_step"] == "manual_review_outcome_recorded_no_token_issued"
    assert result["required_next_step"] == "manual_token_issuance_review_required_no_token_created"
    _assert_no_write_token(result)


def test_locked_when_review_gate_status_is_changes_requested():
    review = _review_outcome()
    review["review_gate_status"] = "changes_requested"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_review_gate_status_must_be_approved" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    assert result["required_next_step"] == "repair_source_review_outcome_before_token_issuance_dry_run"
    _assert_no_write_token(result)


def test_locked_when_review_gate_status_is_rejected():
    review = _review_outcome()
    review["review_gate_status"] = "rejected"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_review_gate_status_must_be_approved" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    _assert_no_write_token(result)


def test_locked_when_review_gate_status_is_locked():
    review = _review_outcome()
    review["review_gate_status"] = "locked"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_review_gate_status_must_be_approved" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    _assert_no_write_token(result)


def test_locked_when_reviewer_decision_is_not_approve():
    review = _review_outcome()
    review["reviewer_decision"] = "request_changes"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_reviewer_decision_must_be_approve" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    _assert_no_write_token(result)


def test_locked_when_source_version_is_not_180():
    review = _review_outcome()
    review["version"] = "1.7.0"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_review_gate_version_must_be_1.8.0" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    _assert_no_write_token(result)


def test_locked_when_source_required_next_step_is_wrong():
    review = _review_outcome()
    review["required_next_step"] = "issue_real_token"

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert (
        "source_required_next_step_must_be_manual_review_outcome_recorded_no_token_issued"
        in result["safety_summary"]["source_review_outcome_errors"]
    )
    _assert_no_write_token(result)


def test_locked_when_source_is_missing_required_keys():
    review = _review_outcome()
    del review["review_outcome_id"]

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "missing_review_outcome_id" in result["safety_summary"]["source_review_outcome_errors"]
    _assert_no_write_token(result)


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
        review = _review_outcome()
        review[flag] = True

        result = run_memory_approval_token_issuance_dry_run(review)

        assert result["token_issuance_status"] == "locked"
        assert f"source_{flag}_must_be_false" in result["safety_summary"][
            "source_review_outcome_errors"
        ]
        _assert_no_write_token(result)


def test_locked_when_source_provider_tools_is_not_empty():
    review = _review_outcome()
    review["provider_tools"] = ["unsafe_tool"]

    result = run_memory_approval_token_issuance_dry_run(review)

    assert result["token_issuance_status"] == "locked"
    assert "source_provider_tools_must_be_empty" in result["safety_summary"][
        "source_review_outcome_errors"
    ]
    _assert_no_write_token(result)


def test_deterministic_token_draft_id():
    review = _review_outcome()

    first = run_memory_approval_token_issuance_dry_run(review, issuance_reason="same reason")
    second = run_memory_approval_token_issuance_dry_run(review, issuance_reason="same reason")

    assert first["token_draft_id"] == second["token_draft_id"]
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_deterministic_token_intent_id():
    review = _review_outcome()

    first = run_memory_approval_token_issuance_dry_run(review, issuer="issuer-a")
    second = run_memory_approval_token_issuance_dry_run(review, issuer="issuer-a")

    assert first["token_intent_id"] == second["token_intent_id"]
    assert first["token_intent_id"] != run_memory_approval_token_issuance_dry_run(
        review,
        issuer="issuer-b",
    )["token_intent_id"]


def test_input_review_outcome_dict_is_not_mutated():
    review = _review_outcome()
    before = deepcopy(review)

    result = run_memory_approval_token_issuance_dry_run(review)
    result["source_review_outcome_snapshot"]["safety_summary"].clear()

    assert review == before


def test_json_serializer_is_deterministic():
    result = run_memory_approval_token_issuance_dry_run(_review_outcome())

    rendered = approval_token_issuance_dry_run_to_json(result)

    assert rendered == json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def test_cli_stdout_writes_no_files(tmp_path):
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(_review_outcome(), sort_keys=True), encoding="utf-8")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())

    completed = _run_cli(["--input", str(review_path)], tmp_path)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert after == before == [Path("review.json")]
    assert result["token_issuance_status"] == "ready"
    _assert_no_write_token(result)


def test_cli_explicit_output_writes_only_requested_file(tmp_path):
    review_path = tmp_path / "review.json"
    output_path = tmp_path / "token-draft.json"
    review_path.write_text(json.dumps(_review_outcome(), sort_keys=True), encoding="utf-8")

    completed = _run_cli(
        [
            "--input",
            str(review_path),
            "--issuer",
            "issuer-a",
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
    assert "approval_token_issuance_dry_run_summary=" in completed.stderr
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file()) == [
        Path("review.json"),
        Path("token-draft.json"),
    ]
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["token_issuance_status"] == "ready"
    assert result["issuer"] == "issuer-a"
    assert result["issuance_reason"] == "reviewed"
    _assert_no_write_token(result)


def test_cli_refuses_output_under_hermes_home(tmp_path):
    hermes_home = tmp_path / "hermes-home"
    review_path = tmp_path / "review.json"
    output_path = hermes_home / "token-draft.json"
    review_path.write_text(json.dumps(_review_outcome(), sort_keys=True), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    env["HERMES_HOME"] = str(hermes_home)

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--input",
            str(review_path),
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
    review = run_memory_approval_intent_review_gate_dry_run(intent, "approve")
    result = run_memory_approval_token_issuance_dry_run(review)
    after = _hermes_files(hermes_home)

    assert preview["version"] == "1.5.0"
    assert intent["approval_intent_status"] == "ready"
    assert review["review_gate_status"] == "approved"
    assert result["token_issuance_status"] == "ready"
    _assert_no_write_token(result)
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
