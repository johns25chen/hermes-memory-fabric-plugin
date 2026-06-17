from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

from hermes_memory_fabric.governance_kernel_cli_dry_run import (
    GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION,
    GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM,
    GOVERNANCE_KERNEL_CLI_MODE,
    GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION,
    SAFETY_BOUNDARIES,
    build_governance_kernel_cli_dry_run_result,
    governance_kernel_cli_dry_run_to_json,
    main,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_kernel_cli_dry_run.py"
)
SCRIPT = PROJECT_ROOT / "scripts" / "governance_kernel_cli_dry_run.py"

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "5.1.0",
        "initialization_scope": "test",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "test",
    },
    "review_completed": {
        "review_id": "review-1",
        "review_status": "complete",
    },
    "dry_run_approved": {
        "approval_id": "approval-1",
        "approved_for": "plan-preparation-only",
    },
    "dry_run_prepared": {
        "dry_run_id": "dry-run-1",
        "plan_id": "plan-1",
    },
    "dry_run_completed": {
        "dry_run_id": "dry-run-1",
        "completion_status": "recorded-only",
    },
    "attestation_submitted": {
        "attestation_id": "attestation-1",
        "attestation_status": "recorded-only",
    },
    "finalization_requested": {
        "finalization_id": "finalization-1",
        "requested_scope": "test",
    },
}


def _event(
    event_id: str,
    event_type: str,
    previous_event_id: str | None,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "actor": "test-actor",
        "created_at": f"2026-06-16T00:00:{event_id[-1:]}Z",
        "payload": (
            payload
            if payload is not None
            else dict(_PAYLOADS[event_type])
        ),
        "previous_event_id": previous_event_id,
        "schema_version": "5.1.0",
    }


def _full_events() -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(_PAYLOADS, start=1):
        event_id = f"event-{index}"
        events.append(
            _event(
                event_id,
                event_type,
                previous_event_id,
                {**_PAYLOADS[event_type], "sequence": index},
            )
        )
        previous_event_id = event_id
    return events


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert value[key] is False
                assert boundaries[key] is False
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def test_public_constants():
    assert GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION == "5.1.0"
    assert GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION == "5.1.0"
    assert GOVERNANCE_KERNEL_CLI_MODE == "local_cli_dry_run_only"
    assert GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM == "sha256"


def test_validate_event_mode_passes_valid_event():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "validate_event", "event": _full_events()[0]}
    )

    assert result["dry_run_status"] == "pass"
    assert result["requested_mode"] == "validate_event"
    assert result["result"]["valid"] is True


def test_canonicalize_event_mode_returns_v460_canonicalization_version():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "canonicalize_event", "event": _full_events()[0]}
    )

    assert result["dry_run_status"] == "pass"
    assert result["result"]["canonicalization_version"] == "5.1.0"


def test_canonicalize_sequence_mode_is_deterministic():
    payload = {"mode": "canonicalize_sequence", "events": _full_events()}

    first = build_governance_kernel_cli_dry_run_result(payload)
    second = build_governance_kernel_cli_dry_run_result(payload)

    assert first == second
    assert first["dry_run_status"] == "pass"
    assert first["result"]["canonicalization_status"] == "pass"


def test_replay_sequence_mode_reaches_finalized_for_full_sequence():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "replay_sequence", "events": _full_events()}
    )

    assert result["dry_run_status"] == "pass"
    assert result["result"]["current_state"] == "finalized"


def test_audit_report_mode_reaches_finalized_for_full_sequence():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "audit_report", "events": _full_events()}
    )

    assert result["dry_run_status"] == "pass"
    assert result["result"]["final_state"] == "finalized"


def test_local_store_replay_mode_reaches_finalized_for_full_sequence():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "local_store_replay", "events": _full_events()}
    )

    assert result["dry_run_status"] == "pass"
    assert result["result"]["final_state"] == "finalized"
    assert (
        result["result"]["append_sequence"]["append_sequence_status"]
        == "pass"
    )


def test_unknown_mode_is_blocked():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "unknown", "event": _full_events()[0]}
    )

    assert result["dry_run_status"] == "blocked"
    assert "mode is not supported" in result["blocking_reasons"]


def test_missing_event_is_blocked_for_event_mode():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "validate_event"}
    )

    assert result["dry_run_status"] == "blocked"
    assert result["blocking_reasons"] == ["event must be a mapping"]


def test_missing_events_is_blocked_for_sequence_mode():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "canonicalize_sequence"}
    )

    assert result["dry_run_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "events must be a sequence of mappings"
    ]


def test_invalid_schema_version_is_blocked():
    event = _full_events()[0]
    event["schema_version"] = "4.5.0"

    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "validate_event", "event": event}
    )

    assert result["dry_run_status"] == "blocked"
    assert "schema_version must equal 5.1.0" in result["blocking_reasons"]


def test_invalid_payload_schema_is_blocked():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {"kernel_version": "5.1.0"},
    )

    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "validate_event", "event": event}
    )

    assert result["dry_run_status"] == "blocked"
    assert (
        "missing required payload field: initialization_scope"
        in result["blocking_reasons"]
    )


def test_invalid_json_like_payload_is_blocked():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "validate_event", "event": {"bad": {"not", "json"}}}
    )

    assert result["dry_run_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "payload must contain deterministic JSON-compatible values"
    ]


def test_sensitive_keys_and_values_do_not_leak():
    event = _full_events()[0]
    event["payload"]["nested"] = {
        "secret": "hidden-value",
        "token": "token-value",
        "visible": "safe",
    }
    event["payload"]["duplicate"] = "hidden-value"
    payload = {
        "mode": "validate_event",
        "event": event,
        "api_key": "top-level-sensitive",
    }

    result = build_governance_kernel_cli_dry_run_result(payload)
    serialized = governance_kernel_cli_dry_run_to_json(result)

    assert result["dry_run_status"] == "pass"
    for blocked in (
        '"secret"',
        '"token"',
        '"api_key"',
        "hidden-value",
        "token-value",
        "top-level-sensitive",
    ):
        assert blocked not in serialized


def test_input_payload_is_not_mutated():
    payload = {"mode": "replay_sequence", "events": _full_events()}
    original = deepcopy(payload)

    build_governance_kernel_cli_dry_run_result(payload)

    assert payload == original


def test_deterministic_cli_hash_stable_across_repeated_runs():
    payload = {"mode": "audit_report", "events": _full_events()}

    first = build_governance_kernel_cli_dry_run_result(payload)
    second = build_governance_kernel_cli_dry_run_result(payload)

    assert first["deterministic_cli_hash"] == second["deterministic_cli_hash"]


def test_deterministic_cli_hash_changes_when_payload_changes():
    payload = {"mode": "audit_report", "events": _full_events()}
    changed = deepcopy(payload)
    changed["events"][2]["payload"]["sequence"] = 99  # type: ignore[index]

    first = build_governance_kernel_cli_dry_run_result(payload)
    second = build_governance_kernel_cli_dry_run_result(changed)

    assert first["deterministic_cli_hash"] != second["deterministic_cli_hash"]


def test_json_serialization_is_deterministic():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "audit_report", "events": _full_events()}
    )

    first = governance_kernel_cli_dry_run_to_json(result)
    second = governance_kernel_cli_dry_run_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["dry_run_status"] == "pass"


def test_main_reads_stdin_json(capsys):
    code = main(
        [],
        stdin_text=json.dumps(
            {"mode": "validate_event", "event": _full_events()[0]}
        ),
    )
    captured = capsys.readouterr()

    assert code == 0
    assert json.loads(captured.out)["dry_run_status"] == "pass"
    assert captured.err == ""


def test_main_supports_input_json(capsys):
    payload = json.dumps(
        {"mode": "validate_event", "event": _full_events()[0]}
    )

    code = main(["--input-json", payload])
    captured = capsys.readouterr()

    assert code == 0
    assert json.loads(captured.out)["dry_run_status"] == "pass"
    assert captured.err == ""


def test_main_supports_mode_override(capsys):
    payload = json.dumps({"event": _full_events()[0]})

    code = main(["--mode", "validate_event"], stdin_text=payload)
    captured = capsys.readouterr()

    decoded = json.loads(captured.out)
    assert code == 0
    assert decoded["requested_mode"] == "validate_event"
    assert decoded["dry_run_status"] == "pass"
    assert captured.err == ""


def test_cli_script_returns_zero_for_pass_and_one_for_blocked():
    pass_payload = json.dumps(
        {"mode": "validate_event", "event": _full_events()[0]}
    )
    pass_completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=PROJECT_ROOT,
        input=pass_payload,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    blocked_completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--input-json", '{"mode":"unknown"}'],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert pass_completed.returncode == 0
    assert json.loads(pass_completed.stdout)["dry_run_status"] == "pass"
    assert pass_completed.stderr == ""
    assert blocked_completed.returncode == 1
    assert json.loads(blocked_completed.stdout)["dry_run_status"] == "blocked"
    assert blocked_completed.stderr == ""


def test_all_safety_fields_remain_false():
    result = build_governance_kernel_cli_dry_run_result(
        {"mode": "local_store_replay", "events": _full_events()}
    )

    _assert_safety(result)


def test_cli_module_has_only_local_standard_library_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert imported_roots <= {
        "__future__",
        "collections",
        "event_driven_governance_kernel",
        "governance_event_canonicalizer",
        "governance_event_schema_registry",
        "governance_local_event_store_dry_run",
        "governance_replay_audit_report",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
        "math",
        "sys",
        "typing",
    }
    assert called_names.isdisjoint(
        {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
        }
    )
    for forbidden in (
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "pathlib",
        "github",
        "openclaw",
        "composio",
        "memory_graph",
        "operation_ledger",
        "filesystem",
        "database",
        "network",
        "write",
        "execution",
    ):
        assert forbidden not in source.casefold()
