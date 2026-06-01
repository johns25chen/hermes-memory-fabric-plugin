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
    run_memory_approval_token_issuance_dry_run,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run
from hermes_memory_fabric.memory_token_authority_boundary_contract_dry_run import (
    token_authority_boundary_contract_dry_run_to_json,
    run_memory_token_authority_boundary_contract_dry_run,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = PROJECT_ROOT / "scripts" / "build_token_authority_boundary_contract_dry_run.py"


def _summary() -> str:
    return """# v2.0.0 Token Authority Boundary Contract Dry Run

Goal / Purpose
Convert a v1.9 approval token issuance dry-run candidate into a declarative
token authority boundary contract candidate.

Included / Changed files
- src/hermes_memory_fabric/memory_token_authority_boundary_contract_dry_run.py
- scripts/build_token_authority_boundary_contract_dry_run.py

Validation
- focused pytest
- smoke_token_authority_boundary_contract_dry_run.py

Boundary
- Dry-run authority contract candidate only.
- No usable token.
- No token file.
- No proposal creation.
- No operation ledger append.
- No executor invocation.
- No memory write.

Version
2.0.0

Result
Generated local token authority boundary contract dry-run candidates.
"""


def _token_issuance() -> dict[str, object]:
    candidates = generate_codex_task_summary_candidates(_summary())
    low_risk = [candidate for candidate in candidates if candidate["risk_level"] == "low"]
    preview = run_memory_candidate_proposal_dry_run(low_risk)
    intent = run_memory_approval_intent_dry_run(preview, repo_root=PROJECT_ROOT)
    review = run_memory_approval_intent_review_gate_dry_run(intent, "approve", "looks safe")
    return run_memory_approval_token_issuance_dry_run(review, issuance_reason="ready")


def _assert_no_token_no_write(result: dict[str, object]) -> None:
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


def test_ready_authority_contract_from_valid_v19_token_issuance_dry_run():
    token_issuance = _token_issuance()

    result = run_memory_token_authority_boundary_contract_dry_run(token_issuance)

    assert result["version"] == "2.0.0"
    assert result["authority_contract_status"] == "ready"
    assert result["authority_contract_id"].startswith(
        "token-authority-boundary-contract-dry-run-"
    )
    assert result["authority_contract_kind"] == "token_authority_boundary_contract_candidate"
    assert result["source_token_issuance_version"] == "1.9.0"
    assert result["source_token_issuance_status"] == "ready"
    assert result["source_token_draft_id"] == token_issuance["token_draft_id"]
    assert result["source_token_intent_id"] == token_issuance["token_intent_id"]
    assert result["source_required_next_step"] == (
        "manual_token_issuance_review_required_no_token_created"
    )
    assert result["authority_scope"] == ["memory_proposal_apply_preview_only"]
    assert result["expiry_seconds"] == 900
    assert result["revocation_required"] is True
    assert result["audit_required"] is True
    assert result["ledger_required"] is True
    assert result["executor_boundary_required"] is True
    assert result["required_next_step"] == "manual_authority_contract_review_required_no_token_created"
    assert result["allowed_future_authority_actions"] == [
        "define_token_scope",
        "define_token_expiry",
        "define_token_revocation",
        "define_token_audit_requirements",
        "define_executor_boundary",
        "define_ledger_boundary",
    ]
    assert result["forbidden_future_authority_actions"] == [
        "issue_real_approval_token",
        "create_token_value",
        "write_token_file",
        "append_operation_ledger",
        "invoke_real_executor",
        "apply_memory_proposal",
        "write_memory",
        "write_graph",
        "write_config",
        "write_sqlite",
        "write_approval_audit",
        "expose_provider_tools",
    ]
    _assert_no_token_no_write(result)


def test_locked_when_source_token_issuance_status_is_locked():
    source = _token_issuance()
    source["token_issuance_status"] = "locked"

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_token_issuance_status_must_be_ready" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    assert result["required_next_step"] == (
        "repair_source_token_issuance_or_authority_boundary_before_real_token"
    )
    _assert_no_token_no_write(result)


def test_locked_when_source_version_is_not_190():
    source = _token_issuance()
    source["version"] = "1.8.0"

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_token_issuance_version_must_be_1.9.0" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_source_required_next_step_is_wrong():
    source = _token_issuance()
    source["required_next_step"] = "issue_real_token"

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert (
        "source_required_next_step_must_be_manual_token_issuance_review_required_no_token_created"
        in result["safety_summary"]["source_token_issuance_errors"]
    )
    _assert_no_token_no_write(result)


def test_locked_when_source_is_missing_required_keys():
    source = _token_issuance()
    del source["token_draft_id"]

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "missing_token_draft_id" in result["safety_summary"]["source_token_issuance_errors"]
    _assert_no_token_no_write(result)


def test_locked_when_approval_token_issued_is_true():
    source = _token_issuance()
    source["approval_token_issued"] = True

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_approval_token_issued_must_be_false" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_approval_token_id_is_not_none():
    source = _token_issuance()
    source["approval_token_id"] = "token-id"

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_approval_token_id_must_be_null" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_approval_token_value_is_not_none():
    source = _token_issuance()
    source["approval_token_value"] = "token-value"

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_approval_token_value_must_be_null" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_creates_usable_token_is_true():
    source = _token_issuance()
    source["creates_usable_token"] = True

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_creates_usable_token_must_be_false" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_any_source_no_write_flag_is_unsafe():
    for flag in (
        "approval_token_issued",
        "creates_usable_token",
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
        source = _token_issuance()
        source[flag] = True

        result = run_memory_token_authority_boundary_contract_dry_run(source)

        assert result["authority_contract_status"] == "locked"
        assert f"source_{flag}_must_be_false" in result["safety_summary"][
            "source_token_issuance_errors"
        ]
        _assert_no_token_no_write(result)


def test_locked_when_source_provider_tools_is_not_empty():
    source = _token_issuance()
    source["provider_tools"] = ["unsafe_tool"]

    result = run_memory_token_authority_boundary_contract_dry_run(source)

    assert result["authority_contract_status"] == "locked"
    assert "source_provider_tools_must_be_empty" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_authority_scope_is_empty():
    result = run_memory_token_authority_boundary_contract_dry_run(
        _token_issuance(),
        authority_scope=[],
    )

    assert result["authority_contract_status"] == "locked"
    assert "authority_scope_must_be_non_empty_list" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_authority_scope_contains_non_string_or_empty_values():
    result = run_memory_token_authority_boundary_contract_dry_run(
        _token_issuance(),
        authority_scope=["ok", "", 7],  # type: ignore[list-item]
    )

    assert result["authority_contract_status"] == "locked"
    assert "authority_scope_values_must_be_non_empty_strings" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_expiry_seconds_is_zero_or_negative():
    for expiry_seconds in (0, -1):
        result = run_memory_token_authority_boundary_contract_dry_run(
            _token_issuance(),
            expiry_seconds=expiry_seconds,
        )

        assert result["authority_contract_status"] == "locked"
        assert "expiry_seconds_must_be_positive_int" in result["safety_summary"][
            "source_token_issuance_errors"
        ]
        _assert_no_token_no_write(result)


def test_locked_when_revocation_required_is_false():
    result = run_memory_token_authority_boundary_contract_dry_run(
        _token_issuance(),
        revocation_required=False,
    )

    assert result["authority_contract_status"] == "locked"
    assert "revocation_required_must_be_true" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_locked_when_audit_required_is_false():
    result = run_memory_token_authority_boundary_contract_dry_run(
        _token_issuance(),
        audit_required=False,
    )

    assert result["authority_contract_status"] == "locked"
    assert "audit_required_must_be_true" in result["safety_summary"][
        "source_token_issuance_errors"
    ]
    _assert_no_token_no_write(result)


def test_deterministic_authority_contract_id():
    source = _token_issuance()

    first = run_memory_token_authority_boundary_contract_dry_run(source)
    second = run_memory_token_authority_boundary_contract_dry_run(source)

    assert first["authority_contract_id"] == second["authority_contract_id"]
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_input_token_issuance_dict_is_not_mutated():
    source = _token_issuance()
    before = deepcopy(source)

    result = run_memory_token_authority_boundary_contract_dry_run(source)
    result["source_token_issuance_snapshot"]["safety_summary"].clear()

    assert source == before


def test_json_serializer_is_deterministic():
    result = run_memory_token_authority_boundary_contract_dry_run(_token_issuance())

    rendered = token_authority_boundary_contract_dry_run_to_json(result)

    assert rendered == json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def test_cli_stdout_writes_no_files(tmp_path):
    input_path = tmp_path / "token-issuance.json"
    input_path.write_text(json.dumps(_token_issuance(), sort_keys=True), encoding="utf-8")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())

    completed = _run_cli(["--input", str(input_path)], tmp_path)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file())
    result = json.loads(completed.stdout)
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert after == before == [Path("token-issuance.json")]
    assert result["authority_contract_status"] == "ready"
    _assert_no_token_no_write(result)


def test_cli_explicit_output_writes_only_requested_file(tmp_path):
    input_path = tmp_path / "token-issuance.json"
    output_path = tmp_path / "authority-contract.json"
    input_path.write_text(json.dumps(_token_issuance(), sort_keys=True), encoding="utf-8")

    completed = _run_cli(
        [
            "--input",
            str(input_path),
            "--scope",
            "memory_proposal_apply_preview_only",
            "--expiry-seconds",
            "1200",
            "--output",
            str(output_path),
            "--print-summary",
        ],
        tmp_path,
    )

    assert completed.returncode == 0
    assert completed.stdout == ""
    assert "token_authority_boundary_contract_dry_run_summary=" in completed.stderr
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*") if path.is_file()) == [
        Path("authority-contract.json"),
        Path("token-issuance.json"),
    ]
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["authority_contract_status"] == "ready"
    assert result["expiry_seconds"] == 1200
    _assert_no_token_no_write(result)


def test_cli_refuses_output_under_hermes_home(tmp_path):
    hermes_home = tmp_path / "hermes-home"
    input_path = tmp_path / "token-issuance.json"
    output_path = hermes_home / "authority-contract.json"
    input_path.write_text(json.dumps(_token_issuance(), sort_keys=True), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = f"{PROJECT_ROOT / 'src'}:{PROJECT_ROOT}"
    env["HERMES_HOME"] = str(hermes_home)

    completed = subprocess.run(
        [
            sys.executable,
            str(CLI_SCRIPT),
            "--input",
            str(input_path),
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
    token_issuance = run_memory_approval_token_issuance_dry_run(review)
    result = run_memory_token_authority_boundary_contract_dry_run(token_issuance)
    after = _hermes_files(hermes_home)

    assert preview["version"] == "1.5.0"
    assert intent["approval_intent_status"] == "ready"
    assert review["review_gate_status"] == "approved"
    assert token_issuance["token_issuance_status"] == "ready"
    assert result["authority_contract_status"] == "ready"
    _assert_no_token_no_write(result)
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
