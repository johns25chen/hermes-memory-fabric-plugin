from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

from hermes_memory_fabric.event_driven_governance_kernel import (
    KERNEL_VERSION,
    SAFETY_BOUNDARIES,
    apply_governance_event,
    replay_governance_events,
    validate_governance_event,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "event_driven_governance_kernel.py"
)

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "5.12.0",
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
    "blocked": {
        "reason": "test-block",
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
        "created_at": f"2026-06-14T00:00:{event_id[-1:]}Z",
        "payload": (
            payload
            if payload is not None
            else dict(_PAYLOADS.get(event_type, {}))
        ),
        "previous_event_id": previous_event_id,
        "schema_version": "5.12.0",
    }


def _full_events() -> list[dict[str, object]]:
    event_types = [
        "governance_kernel_initialized",
        "proposal_submitted",
        "review_completed",
        "dry_run_approved",
        "dry_run_prepared",
        "dry_run_completed",
        "attestation_submitted",
        "finalization_requested",
    ]
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(event_types, start=1):
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


def test_valid_full_event_sequence_reaches_finalized():
    result = replay_governance_events(_full_events())

    assert KERNEL_VERSION == "5.12.0"
    assert result["version"] == "5.12.0"
    assert result["kernel_name"] == "event_driven_governance_kernel"
    assert result["current_state"] == "finalized"
    assert result["previous_state"] == "attestation_ready"
    assert result["event_count"] == 8
    assert len(result["accepted_events"]) == 8
    assert result["rejected_events"] == []
    assert result["audit_status"] == "pass"
    assert result["replay_safe"] is True
    assert result["next_allowed_events"] == ["blocked"]
    assert result["transition_policy_version"] == "5.12.0"
    assert result["transition_policy_registry_version"] == "5.12.0"
    assert all(
        transition["policy_evaluation"]["valid_transition"] is True
        for transition in result["transition_history"]
    )


def test_valid_partial_sequence_reaches_review_ready():
    result = replay_governance_events(_full_events()[:3])

    assert result["current_state"] == "review_ready"
    assert result["previous_state"] == "proposal_open"
    assert result["audit_status"] == "pass"


def test_duplicate_event_id_is_rejected():
    events = _full_events()[:2]
    events.append(_event("event-2", "review_completed", "event-2"))

    result = replay_governance_events(events)

    assert result["current_state"] == "blocked"
    assert result["audit_status"] == "blocked"
    assert len(result["rejected_events"]) == 1
    assert "event_id must be unique within a replay" in result["blocking_reasons"]


def test_unknown_event_type_is_rejected():
    event = _event("event-1", "unknown_event", None)

    result = replay_governance_events([event])

    assert result["current_state"] == "blocked"
    assert result["rejected_events"][0]["event"]["event_type"] == "unknown_event"
    assert "event_type is not allowed" in result["blocking_reasons"]


def test_malformed_event_is_rejected():
    event = _event("event-1", "governance_kernel_initialized", None)
    del event["actor"]

    result = replay_governance_events([event])

    assert result["current_state"] == "blocked"
    assert "missing required field: actor" in result["blocking_reasons"]


def test_invalid_previous_event_id_chain_is_rejected():
    events = _full_events()[:2]
    events[1]["previous_event_id"] = "wrong-event"

    result = replay_governance_events(events)

    assert result["current_state"] == "blocked"
    assert (
        "previous_event_id does not match the prior accepted event"
        in result["blocking_reasons"]
    )


def test_invalid_transition_is_rejected():
    event = _event("event-1", "review_completed", None)

    result = replay_governance_events([event])

    assert result["current_state"] == "blocked"
    assert result["transition_history"][0]["accepted"] is False
    assert (
        "event_type is not allowed from the current governance state"
        in result["blocking_reasons"]
    )


def test_invalid_payload_schema_is_rejected():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {"kernel_version": "5.12.0"},
    )

    result = replay_governance_events([event])

    assert result["current_state"] == "blocked"
    assert (
        "missing required payload field: initialization_scope"
        in result["blocking_reasons"]
    )


def test_blocked_event_moves_to_blocked_state():
    event = _event("event-1", "blocked", None)

    result = replay_governance_events([event])

    assert result["current_state"] == "blocked"
    assert len(result["accepted_events"]) == 1
    assert result["accepted_events"][0]["event_id"] == event["event_id"]
    assert result["accepted_events"][0]["canonicalization_version"] == "5.12.0"
    assert result["rejected_events"] == []
    assert result["audit_status"] == "blocked"
    assert result["blocking_reasons"] == ["blocked event received"]


def test_replay_is_deterministic_across_repeated_runs():
    events = _full_events()

    first = replay_governance_events(events)
    second = replay_governance_events(events)

    assert first == second
    assert first["deterministic_replay_hash"] == second["deterministic_replay_hash"]


def test_replay_hash_changes_when_event_order_changes():
    events = _full_events()
    reordered = deepcopy(events)
    reordered[3], reordered[4] = reordered[4], reordered[3]

    original = replay_governance_events(events)
    changed = replay_governance_events(reordered)

    assert (
        original["deterministic_replay_hash"]
        != changed["deterministic_replay_hash"]
    )


def test_replay_hash_changes_when_payload_changes():
    events = _full_events()
    changed_events = deepcopy(events)
    changed_events[2]["payload"] = {"sequence": 3, "changed": True}

    original = replay_governance_events(events)
    changed = replay_governance_events(changed_events)

    assert (
        original["deterministic_replay_hash"]
        != changed["deterministic_replay_hash"]
    )


def test_sensitive_keys_and_values_are_not_leaked():
    sensitive = {
        "approval_phrase": "approval-value",
        "stdout_tail": "tail-value",
        "stdout": "stdout-value",
        "raw_logs": "logs-value",
        "token": "token-value",
        "api_key": "api-value",
        "secret": "secret-value",
        "password": "password-value",
        "credential": "credential-value",
    }
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {
            **_PAYLOADS["governance_kernel_initialized"],
            "safe": "visible",
            "nested": sensitive,
        },
    )

    validation = validate_governance_event(event)
    result = replay_governance_events([event])
    serialized = json.dumps(
        {"validation": validation, "result": result},
        sort_keys=True,
    )

    assert validation["valid"] is True
    assert validation["sanitized_event"]["sensitive_fields_omitted"] is True
    assert validation["sanitized_event"]["payload"]["safe"] == "visible"
    for key, value in sensitive.items():
        assert f'"{key}"' not in serialized
        assert value not in serialized


def test_input_events_are_not_mutated():
    events = _full_events()
    original = deepcopy(events)

    replay_governance_events(events)

    assert events == original


def test_safety_fields_remain_false_on_report_and_transitions():
    result = replay_governance_events(_full_events())

    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False
        for transition in result["transition_history"]:
            assert transition[key] is False
            assert transition["safety_boundaries"][key] is False


def test_single_event_transition_is_deterministic_and_side_effect_free():
    event = _event("event-1", "governance_kernel_initialized", None)

    transition = apply_governance_event("initialized", event)

    assert transition["accepted"] is True
    assert transition["previous_state"] == "initialized"
    assert transition["next_state"] == "proposal_open"
    for key in SAFETY_BOUNDARIES:
        assert transition[key] is False


def test_core_module_has_no_external_side_effect_imports_or_calls():
    tree = ast.parse(CORE_MODULE.read_text(encoding="utf-8"))
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
        "enum",
        "governance_event_canonicalizer",
        "governance_event_schema_registry",
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
