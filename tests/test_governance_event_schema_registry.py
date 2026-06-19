from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_event_schema_registry import (
    ALLOWED_EVENT_TYPES,
    CANONICAL_EVENT_SCHEMA_VERSION,
    GOVERNANCE_EVENT_SCHEMA_REGISTRY,
    REQUIRED_TOP_LEVEL_EVENT_FIELDS,
    SAFETY_BOUNDARIES,
    SCHEMA_REGISTRY_VERSION,
    get_governance_event_schema,
    governance_event_schema_registry_to_json,
    sanitize_governance_event,
    validate_event_against_schema_registry,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "governance_event_schema_registry.py"
)

PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "5.13.0",
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


def _event(event_type: str = "governance_kernel_initialized") -> dict[str, object]:
    return {
        "event_id": "event-1",
        "event_type": event_type,
        "actor": "test-actor",
        "created_at": "2026-06-15T00:00:00Z",
        "payload": dict(PAYLOADS.get(event_type, {})),
        "previous_event_id": None,
        "schema_version": CANONICAL_EVENT_SCHEMA_VERSION,
    }


def test_every_allowed_event_type_has_a_schema():
    assert SCHEMA_REGISTRY_VERSION == "5.13.0"
    assert tuple(GOVERNANCE_EVENT_SCHEMA_REGISTRY) == ALLOWED_EVENT_TYPES
    for event_type in ALLOWED_EVENT_TYPES:
        assert get_governance_event_schema(event_type)


def test_unknown_event_type_schema_is_empty():
    assert get_governance_event_schema("unknown") == {}


def test_every_schema_has_required_payload_fields():
    for event_type in ALLOWED_EVENT_TYPES:
        schema = get_governance_event_schema(event_type)
        required = schema["required_payload_fields"]
        assert required
        assert all(field_type == "str" for field_type in required.values())


@pytest.mark.parametrize("event_type", ALLOWED_EVENT_TYPES)
def test_valid_event_for_each_event_type_passes(event_type: str):
    result = validate_event_against_schema_registry(_event(event_type))

    assert result["valid"] is True
    assert result["blocking_reasons"] == []
    assert isinstance(result["sanitized_event"], dict)
    assert result["schema_version"] == "5.13.0"
    assert result["event_type"] == event_type


@pytest.mark.parametrize("field", REQUIRED_TOP_LEVEL_EVENT_FIELDS)
def test_missing_top_level_field_fails(field: str):
    event = _event()
    del event[field]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert f"missing required field: {field}" in result["blocking_reasons"]


@pytest.mark.parametrize("field", ("event_id", "event_type", "actor", "created_at"))
def test_empty_string_top_level_field_fails(field: str):
    event = _event()
    event[field] = " "

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert f"{field} must be a non-empty string" in result["blocking_reasons"]


def test_unknown_event_type_fails():
    result = validate_event_against_schema_registry(_event("unknown"))

    assert result["valid"] is False
    assert "event_type is not allowed" in result["blocking_reasons"]


def test_wrong_schema_version_fails():
    event = _event()
    event["schema_version"] = "4.0.0"

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert "schema_version must equal 5.13.0" in result["blocking_reasons"]


def test_payload_not_mapping_fails():
    event = _event()
    event["payload"] = []

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert "payload must be a mapping" in result["blocking_reasons"]


def test_missing_required_payload_field_fails():
    event = _event("proposal_submitted")
    del event["payload"]["proposal_id"]  # type: ignore[index]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert (
        "missing required payload field: proposal_id"
        in result["blocking_reasons"]
    )


def test_empty_required_payload_string_fails():
    event = _event("review_completed")
    event["payload"]["review_status"] = " "  # type: ignore[index]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert (
        "payload field review_status must be a non-empty string"
        in result["blocking_reasons"]
    )


def test_non_string_required_payload_field_fails():
    event = _event("dry_run_prepared")
    event["payload"]["plan_id"] = 1  # type: ignore[index]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert (
        "payload field plan_id must be a non-empty string"
        in result["blocking_reasons"]
    )


def test_non_string_mapping_key_fails():
    event = _event()
    event["payload"][1] = "invalid-key"  # type: ignore[index]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert any(
        "string mapping keys" in reason
        for reason in result["blocking_reasons"]
    )


@pytest.mark.parametrize("value", (math.inf, -math.inf, math.nan))
def test_non_finite_float_fails(value: float):
    event = _event()
    event["payload"]["measurement"] = value  # type: ignore[index]

    result = validate_event_against_schema_registry(event)

    assert result["valid"] is False
    assert any(
        "finite floats" in reason for reason in result["blocking_reasons"]
    )


def test_sensitive_keys_and_values_are_omitted():
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
    event = _event()
    event["payload"]["nested"] = sensitive  # type: ignore[index]
    event["payload"]["duplicate"] = "token-value"  # type: ignore[index]

    result = validate_event_against_schema_registry(event)
    serialized = json.dumps(result, sort_keys=True)

    assert result["valid"] is True
    assert result["sensitive_fields_omitted"] is True
    assert result["sanitized_event"]["sensitive_fields_omitted"] is True
    for key, value in sensitive.items():
        assert f'"{key}"' not in serialized
        assert value not in serialized


def test_sanitization_is_deterministic_and_does_not_mutate_input():
    event = _event()
    event["payload"]["unordered"] = {"z": 1, "a": 2}  # type: ignore[index]
    original = deepcopy(event)

    first = sanitize_governance_event(event)
    second = sanitize_governance_event(event)

    assert first == second
    assert event == original
    assert list(first) == sorted(first)
    assert list(first["payload"]["unordered"]) == ["a", "z"]


def test_registry_json_serialization_is_deterministic():
    result = validate_event_against_schema_registry(_event())

    first = governance_event_schema_registry_to_json(result)
    second = governance_event_schema_registry_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["valid"] is True


def test_all_safety_flags_remain_false():
    result = validate_event_against_schema_registry(_event())

    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False


def test_registry_module_has_no_external_side_effect_surfaces():
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
        "governance_transition_policy_registry",
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
            "url" + "open",
        }
    )
