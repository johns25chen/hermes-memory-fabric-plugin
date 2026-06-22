from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

from hermes_memory_fabric.governance_cli_report_envelope import (
    GOVERNANCE_CLI_REPORT_ENVELOPE_HASH_ALGORITHM,
    GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION,
    GOVERNANCE_CLI_REPORT_ENVELOPE_TYPE,
    GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION,
    SAFETY_BOUNDARIES,
    build_governance_cli_report_envelope,
    build_governance_cli_report_envelope_from_payload,
    governance_cli_report_envelope_to_json,
)
from hermes_memory_fabric.governance_kernel_cli_dry_run import (
    build_governance_kernel_cli_dry_run_result,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_cli_report_envelope.py"
)

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "6.4.0",
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
        "schema_version": "6.4.0",
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


def _cli_result(mode: str = "audit_report") -> dict[str, object]:
    return build_governance_kernel_cli_dry_run_result(
        {"mode": mode, "events": _full_events()}
    )


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
    assert GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION == "6.4.0"
    assert GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION == "6.4.0"
    assert GOVERNANCE_CLI_REPORT_ENVELOPE_TYPE == "governance_cli_report_envelope"
    assert GOVERNANCE_CLI_REPORT_ENVELOPE_HASH_ALGORITHM == "sha256"


def test_valid_cli_result_wraps_successfully():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["version"] == "6.4.0"
    assert envelope["schema_version"] == "6.4.0"
    assert envelope["envelope_type"] == "governance_cli_report_envelope"
    assert envelope["source_report_type"] == "governance_kernel_cli_dry_run"
    assert envelope["source_report_version"] == "6.4.0"
    assert envelope["report"]["dry_run_status"] == "pass"


def test_build_from_payload_wraps_successfully():
    payload = {"mode": "audit_report", "events": _full_events()}

    envelope = build_governance_cli_report_envelope_from_payload(payload)

    assert envelope["envelope_status"] == "pass"
    assert envelope["report"]["requested_mode"] == "audit_report"


def test_envelope_status_pass_for_pass_cli_report():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["dry_run_status"] == "pass"
    assert envelope["envelope_status"] == "pass"


def test_envelope_status_blocked_for_blocked_cli_report():
    cli_result = build_governance_kernel_cli_dry_run_result(
        {"mode": "unknown"}
    )

    envelope = build_governance_cli_report_envelope(cli_result)

    assert envelope["dry_run_status"] == "blocked"
    assert envelope["envelope_status"] == "blocked"


def test_malformed_cli_result_is_blocked():
    envelope = build_governance_cli_report_envelope({"dry_run_status": "pass"})

    assert envelope["envelope_status"] == "blocked"
    assert envelope["dry_run_status"] == "pass"
    assert envelope["report_summary"]["blocking_reason_count"] > 0


def test_non_mapping_cli_result_is_blocked():
    envelope = build_governance_cli_report_envelope(["not", "mapping"])  # type: ignore[arg-type]

    assert envelope["envelope_status"] == "blocked"
    assert envelope["dry_run_status"] == "blocked"
    assert envelope["report"] is None


def test_non_string_mapping_key_is_blocked():
    envelope = build_governance_cli_report_envelope({1: "bad"})  # type: ignore[dict-item]

    assert envelope["envelope_status"] == "blocked"
    assert envelope["report"] is None
    assert envelope["report_summary"]["blocking_reason_count"] == 1


def test_non_finite_float_is_blocked():
    cli_result = _cli_result()
    cli_result["bad"] = float("inf")

    envelope = build_governance_cli_report_envelope(cli_result)

    assert envelope["envelope_status"] == "blocked"
    assert envelope["report"] is None


def test_report_summary_contains_requested_mode_and_dry_run_status():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["report_summary"]["requested_mode"] == "audit_report"
    assert envelope["report_summary"]["dry_run_status"] == "pass"


def test_report_summary_includes_final_state_where_available():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["report_summary"]["final_state"] == "finalized"


def test_report_metadata_local_only_and_no_execution():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["report_metadata"]["local_only"] is True
    assert envelope["report_metadata"]["no_execution"] is True
    assert envelope["report_metadata"]["no_writes"] is True
    assert envelope["report_metadata"]["no_external_calls"] is True


def test_star_cosmos_entry_claimed_is_false():
    envelope = build_governance_cli_report_envelope(_cli_result())

    assert envelope["report_metadata"]["star_cosmos_entry_claimed"] is False


def test_deterministic_report_hash_stable_across_repeated_runs():
    cli_result = _cli_result()

    first = build_governance_cli_report_envelope(cli_result)
    second = build_governance_cli_report_envelope(cli_result)

    assert first["deterministic_report_hash"] == second["deterministic_report_hash"]


def test_deterministic_envelope_hash_stable_across_repeated_runs():
    cli_result = _cli_result()

    first = build_governance_cli_report_envelope(cli_result)
    second = build_governance_cli_report_envelope(cli_result)

    assert first["deterministic_envelope_hash"] == second["deterministic_envelope_hash"]


def test_deterministic_report_hash_changes_when_cli_result_changes():
    first_cli = _cli_result()
    second_cli = _cli_result()
    second_cli["result"]["accepted_event_count"] = 99  # type: ignore[index]

    first = build_governance_cli_report_envelope(first_cli)
    second = build_governance_cli_report_envelope(second_cli)

    assert first["deterministic_report_hash"] != second["deterministic_report_hash"]


def test_deterministic_envelope_hash_changes_when_cli_result_changes():
    first_cli = _cli_result()
    second_cli = _cli_result()
    second_cli["result"]["accepted_event_count"] = 99  # type: ignore[index]

    first = build_governance_cli_report_envelope(first_cli)
    second = build_governance_cli_report_envelope(second_cli)

    assert (
        first["deterministic_envelope_hash"]
        != second["deterministic_envelope_hash"]
    )


def test_sensitive_keys_and_values_do_not_leak():
    cli_result = _cli_result()
    cli_result["api_key"] = "top-level-sensitive"
    cli_result["result"]["secret"] = "hidden-value"  # type: ignore[index]
    cli_result["result"]["duplicate"] = "hidden-value"  # type: ignore[index]

    envelope = build_governance_cli_report_envelope(cli_result)
    serialized = governance_cli_report_envelope_to_json(envelope)

    for blocked in (
        '"api_key"',
        '"secret"',
        "top-level-sensitive",
        "hidden-value",
    ):
        assert blocked not in serialized
    assert envelope["report_summary"]["sensitive_fields_omitted"] is True


def test_input_cli_result_is_not_mutated():
    cli_result = _cli_result()
    original = deepcopy(cli_result)

    build_governance_cli_report_envelope(cli_result)

    assert cli_result == original


def test_input_payload_is_not_mutated():
    payload = {"mode": "audit_report", "events": _full_events()}
    original = deepcopy(payload)

    build_governance_cli_report_envelope_from_payload(payload)

    assert payload == original


def test_json_serialization_is_deterministic():
    envelope = build_governance_cli_report_envelope(_cli_result())

    first = governance_cli_report_envelope_to_json(envelope)
    second = governance_cli_report_envelope_to_json(envelope)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["envelope_status"] == "pass"


def test_all_safety_fields_remain_false():
    envelope = build_governance_cli_report_envelope(_cli_result())

    _assert_safety(envelope)


def test_envelope_module_has_only_local_standard_library_surfaces():
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
        "governance_kernel_cli_dry_run",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
        "math",
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
        "filesystem",
        "database",
        "url" + "open",
        "urllib" + "." + "request",
        "requests" + ".",
        "github",
        "openclaw",
        "composio",
        "memory_graph",
        "memory graph",
        "operation_ledger",
    ):
        assert forbidden not in source.casefold()
