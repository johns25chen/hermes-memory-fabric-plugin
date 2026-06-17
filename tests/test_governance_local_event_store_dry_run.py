from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_local_event_store_dry_run import (
    LOCAL_EVENT_STORE_DRY_RUN_VERSION,
    LOCAL_EVENT_STORE_HASH_ALGORITHM,
    LOCAL_EVENT_STORE_MODE,
    LOCAL_EVENT_STORE_SCHEMA_VERSION,
    SAFETY_BOUNDARIES,
    append_governance_event_to_local_store_dry_run,
    append_governance_events_to_local_store_dry_run,
    build_governance_local_event_store_replay_report_dry_run,
    create_governance_local_event_store_dry_run,
    governance_local_event_store_dry_run_to_json,
    read_governance_local_event_store_dry_run,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "governance_local_event_store_dry_run.py"
)

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


def _append(
    events: list[dict[str, object]],
) -> dict[str, object]:
    return append_governance_events_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        events,
    )


def _assert_safety(result: dict[str, object]) -> None:
    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False


def test_empty_store_shape_is_deterministic():
    first = create_governance_local_event_store_dry_run()
    second = create_governance_local_event_store_dry_run()

    assert first == second
    assert LOCAL_EVENT_STORE_DRY_RUN_VERSION == "5.1.0"
    assert LOCAL_EVENT_STORE_SCHEMA_VERSION == "5.1.0"
    assert LOCAL_EVENT_STORE_MODE == "in_memory_dry_run_only"
    assert LOCAL_EVENT_STORE_HASH_ALGORITHM == "sha256"
    assert first["version"] == "5.1.0"
    assert first["store_mode"] == "in_memory_dry_run_only"
    assert first["event_count"] == 0
    assert first["canonical_events"] == []
    assert first["event_ids"] == []
    assert len(first["deterministic_store_hash"]) == 64


def test_empty_store_safety_flags_remain_false():
    _assert_safety(create_governance_local_event_store_dry_run())


def test_append_valid_event_succeeds():
    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        _full_events()[0],
    )

    assert result["append_status"] == "pass"
    assert result["blocking_reasons"] == []
    assert result["store"]["event_count"] == 1
    assert result["store"]["event_ids"] == ["event-1"]
    assert result["appended_event"]["canonicalization_version"] == "5.1.0"


def test_append_full_valid_sequence_succeeds():
    result = _append(_full_events())

    assert result["append_sequence_status"] == "pass"
    assert result["appended_event_count"] == 8
    assert result["rejected_event_count"] == 0
    assert result["store"]["event_count"] == 8


def test_read_returns_detached_canonical_event_copies():
    store = _append(_full_events())["store"]
    first = read_governance_local_event_store_dry_run(store)
    first["canonical_events"][0]["payload"]["sequence"] = 99
    first["event_ids"].append("mutated")

    second = read_governance_local_event_store_dry_run(store)

    assert second["canonical_events"][0]["payload"]["sequence"] == 1
    assert second["event_ids"] == [f"event-{index}" for index in range(1, 9)]


def test_replay_report_from_store_reaches_finalized():
    store = _append(_full_events())["store"]

    result = build_governance_local_event_store_replay_report_dry_run(
        store
    )

    assert result["replay_report_status"] == "pass"
    assert result["final_state"] == "finalized"
    assert result["replay_audit_report"]["accepted_event_count"] == 8
    assert len(result["deterministic_replay_hash"]) == 64
    assert len(result["deterministic_sequence_hash"]) == 64
    assert len(result["audit_report_hash"]) == 64


def test_duplicate_event_id_is_rejected():
    first = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        _full_events()[0],
    )
    duplicate = _event(
        "event-1",
        "proposal_submitted",
        "event-1",
    )

    result = append_governance_event_to_local_store_dry_run(
        first["store"],
        duplicate,
    )

    assert result["append_status"] == "blocked"
    assert result["store"]["event_count"] == 1
    assert any(
        "event_id must be unique" in reason
        for reason in result["blocking_reasons"]
    )


def test_invalid_previous_event_id_chain_is_rejected():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        "wrong-event",
    )

    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )

    assert result["append_status"] == "blocked"
    assert any(
        "previous_event_id does not match" in reason
        for reason in result["blocking_reasons"]
    )


def test_invalid_schema_version_is_rejected():
    event = _full_events()[0]
    event["schema_version"] = "4.4.0"

    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )

    assert result["append_status"] == "blocked"
    assert "schema_version must equal 5.1.0" in result["blocking_reasons"]


def test_invalid_payload_schema_is_rejected():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {"kernel_version": "5.1.0"},
    )

    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )

    assert result["append_status"] == "blocked"
    assert (
        "missing required payload field: initialization_scope"
        in result["blocking_reasons"]
    )


@pytest.mark.parametrize("value", (math.inf, -math.inf, math.nan))
def test_non_deterministic_json_values_are_rejected(value: float):
    event = _full_events()[0]
    event["payload"]["measurement"] = value

    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )

    assert result["append_status"] == "blocked"
    assert any(
        "finite floats" in reason for reason in result["blocking_reasons"]
    )


def test_sequence_stops_at_first_blocked_event_and_keeps_prior_appends():
    events = _full_events()[:3]
    events[1]["schema_version"] = "4.4.0"

    result = _append(events)

    assert result["append_sequence_status"] == "blocked"
    assert result["appended_event_count"] == 1
    assert result["rejected_event_count"] == 1
    assert result["store"]["event_ids"] == ["event-1"]


def test_sensitive_keys_and_values_do_not_leak():
    event = _full_events()[0]
    event["payload"]["nested"] = {
        "secret": "hidden-value",
        "token": "token-value",
    }
    event["payload"]["duplicate"] = "hidden-value"

    result = append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )
    replay = build_governance_local_event_store_replay_report_dry_run(
        result["store"]
    )
    serialized = json.dumps(
        {"append": result, "replay": replay},
        sort_keys=True,
    )

    assert result["append_status"] == "pass"
    assert '"secret"' not in serialized
    assert '"token"' not in serialized
    assert "hidden-value" not in serialized
    assert "token-value" not in serialized


def test_input_store_is_not_mutated():
    store = create_governance_local_event_store_dry_run()
    original = deepcopy(store)

    append_governance_event_to_local_store_dry_run(
        store,
        _full_events()[0],
    )

    assert store == original


def test_input_event_is_not_mutated():
    event = _full_events()[0]
    original = deepcopy(event)

    append_governance_event_to_local_store_dry_run(
        create_governance_local_event_store_dry_run(),
        event,
    )

    assert event == original


def test_store_hash_is_stable_across_repeated_runs():
    first = _append(_full_events())
    second = _append(_full_events())

    assert (
        first["deterministic_store_hash"]
        == second["deterministic_store_hash"]
    )


def test_store_hash_changes_when_event_order_changes():
    events = _full_events()[:2]
    reordered = [deepcopy(events[1]), deepcopy(events[0])]
    reordered[0]["previous_event_id"] = None
    reordered[1]["previous_event_id"] = reordered[0]["event_id"]

    first = _append(events)
    second = _append(reordered)

    assert first["append_sequence_status"] == "pass"
    assert second["append_sequence_status"] == "pass"
    assert (
        first["deterministic_store_hash"]
        != second["deterministic_store_hash"]
    )


def test_store_hash_changes_when_payload_changes():
    events = _full_events()
    changed = deepcopy(events)
    changed[2]["payload"]["sequence"] = 99

    first = _append(events)
    second = _append(changed)

    assert (
        first["deterministic_store_hash"]
        != second["deterministic_store_hash"]
    )


def test_json_serialization_is_deterministic():
    result = _append(_full_events())

    first = governance_local_event_store_dry_run_to_json(result)
    second = governance_local_event_store_dry_run_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["append_sequence_status"] == "pass"


def test_all_result_safety_fields_remain_false():
    append_result = _append(_full_events())
    read_result = read_governance_local_event_store_dry_run(
        append_result["store"]
    )
    replay_result = (
        build_governance_local_event_store_replay_report_dry_run(
            append_result["store"]
        )
    )

    _assert_safety(append_result)
    _assert_safety(append_result["store"])
    _assert_safety(read_result)
    _assert_safety(replay_result)
    _assert_safety(replay_result["replay_audit_report"])


def test_module_has_only_local_standard_library_surfaces():
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
        "governance_event_canonicalizer",
        "governance_replay_audit_report",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
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
        "pathlib",
        "subprocess",
        "socket",
        "url" + "lib",
        "requ" + "ests",
        "git" + "hub",
        "open" + "claw",
        "com" + "posio",
        "memory_" + "graph",
        "operation_" + "ledger",
        "sql" + "ite",
        "file" + "system",
        "data" + "base",
        "net" + "work",
        "write",
    ):
        assert forbidden not in source.casefold()
