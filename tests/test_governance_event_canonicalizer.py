from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_event_canonicalizer import (
    CANONICALIZER_VERSION,
    CANONICAL_EVENT_HASH_ALGORITHM,
    CANONICAL_EVENT_SCHEMA_VERSION,
    canonicalize_governance_event,
    canonicalize_governance_event_sequence,
    governance_event_canonicalizer_to_json,
)
from hermes_memory_fabric.governance_event_schema_registry import (
    SAFETY_BOUNDARIES,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "governance_event_canonicalizer.py"
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
        "created_at": f"2026-06-15T00:00:{event_id[-1:]}Z",
        "payload": (
            payload
            if payload is not None
            else dict(_PAYLOADS.get(event_type, {}))
        ),
        "previous_event_id": previous_event_id,
        "schema_version": "5.12.0",
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
                {
                    **_PAYLOADS[event_type],
                    "nested": {"z": 1, "a": 2},
                    "sequence": [index, index + 1],
                },
            )
        )
        previous_event_id = event_id
    return events


def _rechain(events: list[dict[str, object]]) -> None:
    previous_event_id: str | None = None
    for event in events:
        event["previous_event_id"] = previous_event_id
        previous_event_id = str(event["event_id"])


def test_public_versions_and_hash_algorithm():
    assert CANONICALIZER_VERSION == "5.12.0"
    assert CANONICAL_EVENT_SCHEMA_VERSION == "5.12.0"
    assert CANONICAL_EVENT_HASH_ALGORITHM == "sha256"


def test_valid_full_sequence_canonicalizes_successfully():
    result = canonicalize_governance_event_sequence(_full_events())

    assert result["version"] == "5.12.0"
    assert result["canonicalization_status"] == "pass"
    assert result["event_count"] == 8
    assert result["canonical_event_count"] == 8
    assert result["rejected_event_count"] == 0
    assert result["rejected_events"] == []
    assert result["blocking_reasons"] == []
    assert len(result["deterministic_sequence_hash"]) == 64


def test_every_canonical_event_has_v450_canonicalization_version():
    result = canonicalize_governance_event_sequence(_full_events())

    assert all(
        event["canonicalization_version"] == "5.12.0"
        for event in result["canonical_events"]
    )


def test_canonical_mappings_are_recursively_sorted():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {
            "z": {"d": 4, "b": 2},
            "kernel_version": "5.12.0",
            "initialization_scope": "test",
            "a": {"y": 2, "x": 1},
        },
    )

    canonical = canonicalize_governance_event(event)

    assert list(canonical) == sorted(canonical)
    assert list(canonical["payload"]) == sorted(canonical["payload"])
    assert list(canonical["payload"]["a"]) == ["x", "y"]
    assert list(canonical["payload"]["z"]) == ["b", "d"]


def test_list_order_is_preserved():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {
            **_PAYLOADS["governance_kernel_initialized"],
            "ordered": [{"z": 1, "a": 2}, "second", "third"],
        },
    )

    canonical = canonicalize_governance_event(event)

    assert canonical["payload"]["ordered"] == [
        {"a": 2, "z": 1},
        "second",
        "third",
    ]


def test_only_canonical_fields_are_preserved():
    event = _full_events()[0]
    event["extra"] = "omitted"

    canonical = canonicalize_governance_event(event)

    assert set(canonical) == {
        "actor",
        "canonicalization_version",
        "created_at",
        "event_id",
        "event_type",
        "payload",
        "previous_event_id",
        "schema_version",
    }


def test_duplicate_event_id_is_rejected():
    events = _full_events()[:2]
    events[1]["event_id"] = events[0]["event_id"]
    events[1]["previous_event_id"] = events[0]["event_id"]

    result = canonicalize_governance_event_sequence(events)

    assert result["canonicalization_status"] == "blocked"
    assert result["rejected_event_count"] == 1
    assert (
        "event_id must be unique within a canonical sequence"
        in result["blocking_reasons"]
    )


def test_invalid_previous_event_id_chain_is_rejected():
    events = _full_events()[:2]
    events[1]["previous_event_id"] = "wrong-event"

    result = canonicalize_governance_event_sequence(events)

    assert result["canonicalization_status"] == "blocked"
    assert (
        "previous_event_id does not match the prior sequence event"
        in result["blocking_reasons"]
    )


def test_unknown_event_type_is_rejected():
    result = canonicalize_governance_event_sequence(
        [_event("event-1", "unknown", None)]
    )

    assert result["canonicalization_status"] == "blocked"
    assert "event_type is not allowed" in result["blocking_reasons"]


def test_invalid_payload_schema_is_rejected():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {"kernel_version": "5.12.0"},
    )

    result = canonicalize_governance_event_sequence([event])

    assert result["canonicalization_status"] == "blocked"
    assert (
        "missing required payload field: initialization_scope"
        in result["blocking_reasons"]
    )


def test_non_string_mapping_key_is_rejected():
    event = _full_events()[0]
    event["payload"][1] = "invalid"  # type: ignore[index]

    with pytest.raises(ValueError, match="string mapping keys"):
        canonicalize_governance_event(event)


@pytest.mark.parametrize("value", (math.inf, -math.inf, math.nan))
def test_non_finite_float_is_rejected(value: float):
    event = _full_events()[0]
    event["payload"]["measurement"] = value  # type: ignore[index]

    with pytest.raises(ValueError, match="finite floats"):
        canonicalize_governance_event(event)


def test_input_events_are_not_mutated():
    events = _full_events()
    original = deepcopy(events)

    canonicalize_governance_event_sequence(events)

    assert events == original


def test_canonical_hash_is_stable_across_repeated_runs():
    events = _full_events()

    first = canonicalize_governance_event_sequence(events)
    second = canonicalize_governance_event_sequence(events)

    assert first == second
    assert (
        first["deterministic_sequence_hash"]
        == second["deterministic_sequence_hash"]
    )


def test_canonical_hash_changes_when_event_order_changes():
    events = _full_events()
    reordered = deepcopy(events)
    reordered[2], reordered[3] = reordered[3], reordered[2]
    _rechain(reordered)

    original = canonicalize_governance_event_sequence(events)
    changed = canonicalize_governance_event_sequence(reordered)

    assert original["canonicalization_status"] == "pass"
    assert changed["canonicalization_status"] == "pass"
    assert (
        original["deterministic_sequence_hash"]
        != changed["deterministic_sequence_hash"]
    )


def test_canonical_hash_changes_when_payload_changes():
    events = _full_events()
    changed_events = deepcopy(events)
    changed_events[2]["payload"]["sequence"] = [99, 100]  # type: ignore[index]

    original = canonicalize_governance_event_sequence(events)
    changed = canonicalize_governance_event_sequence(changed_events)

    assert (
        original["deterministic_sequence_hash"]
        != changed["deterministic_sequence_hash"]
    )


def test_sensitive_keys_and_values_do_not_leak():
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
    event = _full_events()[0]
    event["payload"]["nested_sensitive"] = sensitive  # type: ignore[index]
    event["payload"]["duplicate"] = "token-value"  # type: ignore[index]

    result = canonicalize_governance_event_sequence([event])
    serialized = json.dumps(result, sort_keys=True)

    assert result["canonicalization_status"] == "pass"
    for key, value in sensitive.items():
        assert f'"{key}"' not in serialized
        assert value not in serialized


def test_json_serialization_is_deterministic():
    result = canonicalize_governance_event_sequence(_full_events())

    first = governance_event_canonicalizer_to_json(result)
    second = governance_event_canonicalizer_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["canonicalization_status"] == "pass"


def test_safety_fields_remain_false():
    result = canonicalize_governance_event_sequence(_full_events())

    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False


def test_canonicalizer_has_no_external_side_effect_surfaces():
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
        "governance_event_schema_registry",
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
