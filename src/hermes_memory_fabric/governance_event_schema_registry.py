"""Deterministic, local-only schema registry for governance events."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
import math
from typing import Any

from .governance_transition_policy_registry import SAFETY_BOUNDARIES


SCHEMA_REGISTRY_VERSION = "5.1.0"
CANONICAL_EVENT_SCHEMA_VERSION = "5.1.0"

ALLOWED_EVENT_TYPES = (
    "governance_kernel_initialized",
    "proposal_submitted",
    "review_completed",
    "dry_run_approved",
    "dry_run_prepared",
    "dry_run_completed",
    "attestation_submitted",
    "finalization_requested",
    "blocked",
)

REQUIRED_TOP_LEVEL_EVENT_FIELDS = (
    "event_id",
    "event_type",
    "actor",
    "created_at",
    "payload",
    "previous_event_id",
    "schema_version",
)

GOVERNANCE_EVENT_SCHEMA_REGISTRY: dict[str, dict[str, Any]] = {
    "governance_kernel_initialized": {
        "required_payload_fields": {
            "kernel_version": "str",
            "initialization_scope": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "proposal_submitted": {
        "required_payload_fields": {
            "proposal_id": "str",
            "proposal_type": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "review_completed": {
        "required_payload_fields": {
            "review_id": "str",
            "review_status": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "dry_run_approved": {
        "required_payload_fields": {
            "approval_id": "str",
            "approved_for": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "dry_run_prepared": {
        "required_payload_fields": {
            "dry_run_id": "str",
            "plan_id": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "dry_run_completed": {
        "required_payload_fields": {
            "dry_run_id": "str",
            "completion_status": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "attestation_submitted": {
        "required_payload_fields": {
            "attestation_id": "str",
            "attestation_status": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "finalization_requested": {
        "required_payload_fields": {
            "finalization_id": "str",
            "requested_scope": "str",
        },
        "allow_unknown_payload_fields": True,
    },
    "blocked": {
        "required_payload_fields": {
            "reason": "str",
        },
        "allow_unknown_payload_fields": True,
    },
}

_SENSITIVE_KEYS = frozenset(
    {
        "approval_phrase",
        "stdout_tail",
        "stdout",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
    }
)


def get_governance_event_schema(event_type: str) -> dict[str, Any]:
    """Return a detached schema for a known event type."""

    schema = GOVERNANCE_EVENT_SCHEMA_REGISTRY.get(event_type)
    if schema is None:
        return {}
    required_fields = schema["required_payload_fields"]
    return {
        "allow_unknown_payload_fields": bool(
            schema["allow_unknown_payload_fields"]
        ),
        "required_payload_fields": dict(required_fields),
        "schema_version": CANONICAL_EVENT_SCHEMA_VERSION,
    }


def validate_event_against_schema_registry(
    event: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and sanitize one governance event without side effects."""

    if not isinstance(event, Mapping):
        return _validation_result(
            valid=False,
            blocking_reasons=["event must be a mapping"],
            sanitized_event=None,
            event_type=None,
            sensitive_fields_omitted=False,
        )

    sanitized_candidate = sanitize_governance_event(event)
    public_event_type = _safe_non_empty_string(
        sanitized_candidate.get("event_type")
    )
    blocking_reasons: list[str] = []
    for field in REQUIRED_TOP_LEVEL_EVENT_FIELDS:
        if field not in event:
            blocking_reasons.append(f"missing required field: {field}")

    for field in ("event_id", "event_type", "actor", "created_at"):
        value = event.get(field)
        if not isinstance(value, str) or not value.strip():
            blocking_reasons.append(f"{field} must be a non-empty string")

    event_type = _safe_non_empty_string(event.get("event_type"))
    if event_type is not None and event_type not in ALLOWED_EVENT_TYPES:
        blocking_reasons.append("event_type is not allowed")

    if event.get("schema_version") != CANONICAL_EVENT_SCHEMA_VERSION:
        blocking_reasons.append(
            f"schema_version must equal {CANONICAL_EVENT_SCHEMA_VERSION}"
        )

    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        blocking_reasons.append("payload must be a mapping")

    previous_event_id = event.get("previous_event_id")
    if previous_event_id is not None and (
        not isinstance(previous_event_id, str) or not previous_event_id.strip()
    ):
        blocking_reasons.append(
            "previous_event_id must be a non-empty string or None"
        )

    compatible, sensitive_fields_omitted = _json_compatible(event)
    sensitive_fields_omitted = (
        sensitive_fields_omitted
        or bool(sanitized_candidate.get("sensitive_fields_omitted"))
    )
    if not compatible:
        blocking_reasons.append(
            "event values must be deterministic JSON-compatible values "
            "with string mapping keys and finite floats"
        )

    if event_type in GOVERNANCE_EVENT_SCHEMA_REGISTRY and isinstance(
        payload, Mapping
    ):
        required_payload_fields = GOVERNANCE_EVENT_SCHEMA_REGISTRY[
            event_type
        ]["required_payload_fields"]
        for field, field_type in required_payload_fields.items():
            if field not in payload:
                blocking_reasons.append(
                    f"missing required payload field: {field}"
                )
                continue
            value = payload[field]
            if field_type == "str" and (
                not isinstance(value, str) or not value.strip()
            ):
                blocking_reasons.append(
                    f"payload field {field} must be a non-empty string"
                )

    if blocking_reasons:
        return _validation_result(
            valid=False,
            blocking_reasons=_deduplicate(blocking_reasons),
            sanitized_event=None,
            event_type=public_event_type,
            sensitive_fields_omitted=sensitive_fields_omitted,
        )

    sanitized_event = sanitized_candidate
    sensitive_fields_omitted = bool(
        sanitized_event.get("sensitive_fields_omitted")
    )
    return _validation_result(
        valid=True,
        blocking_reasons=[],
        sanitized_event=sanitized_event,
        event_type=public_event_type,
        sensitive_fields_omitted=sensitive_fields_omitted,
    )


def sanitize_governance_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Return a deterministic copy with sensitive fields and values omitted."""

    if not isinstance(event, Mapping):
        return {}
    sensitive_values = _collect_sensitive_scalar_values(event)
    sanitized, sensitive_fields_omitted = _sanitize_value(
        event,
        sensitive_values,
    )
    if not isinstance(sanitized, dict):
        return {}
    if sensitive_fields_omitted:
        sanitized["sensitive_fields_omitted"] = True
    return sanitized


def governance_event_schema_registry_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize a schema-registry result deterministically."""

    return (
        json.dumps(
            dict(result),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _validation_result(
    *,
    valid: bool,
    blocking_reasons: Sequence[str],
    sanitized_event: dict[str, Any] | None,
    event_type: str | None,
    sensitive_fields_omitted: bool,
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "valid": valid,
        "blocking_reasons": list(blocking_reasons),
        "sanitized_event": sanitized_event,
        "schema_version": CANONICAL_EVENT_SCHEMA_VERSION,
        "event_type": event_type,
        "sensitive_fields_omitted": sensitive_fields_omitted,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _safe_non_empty_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _json_compatible(value: Any) -> tuple[bool, bool]:
    if isinstance(value, Mapping):
        sensitive_fields_omitted = False
        for key, nested_value in value.items():
            if not isinstance(key, str):
                return False, sensitive_fields_omitted
            if key.casefold() in _SENSITIVE_KEYS:
                sensitive_fields_omitted = True
                compatible, nested_omitted = _json_compatible(nested_value)
                if not compatible:
                    return False, True
                sensitive_fields_omitted = (
                    sensitive_fields_omitted or nested_omitted
                )
                continue
            compatible, nested_omitted = _json_compatible(nested_value)
            if not compatible:
                return False, sensitive_fields_omitted or nested_omitted
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return True, sensitive_fields_omitted
    if isinstance(value, list):
        sensitive_fields_omitted = False
        for item in value:
            compatible, nested_omitted = _json_compatible(item)
            if not compatible:
                return False, sensitive_fields_omitted or nested_omitted
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return True, sensitive_fields_omitted
    if value is None or isinstance(value, (str, bool, int)):
        return True, False
    if isinstance(value, float):
        return math.isfinite(value), False
    return False, False


def _collect_sensitive_scalar_values(
    value: Any,
    *,
    sensitive_context: bool = False,
) -> set[tuple[type[Any], Any]]:
    collected: set[tuple[type[Any], Any]] = set()
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            nested_sensitive = (
                sensitive_context
                or isinstance(key, str)
                and key.casefold() in _SENSITIVE_KEYS
            )
            collected.update(
                _collect_sensitive_scalar_values(
                    nested_value,
                    sensitive_context=nested_sensitive,
                )
            )
        return collected
    if isinstance(value, list):
        for item in value:
            collected.update(
                _collect_sensitive_scalar_values(
                    item,
                    sensitive_context=sensitive_context,
                )
            )
        return collected
    if sensitive_context and (
        isinstance(value, str)
        or isinstance(value, int)
        and not isinstance(value, bool)
        or isinstance(value, float)
        and math.isfinite(value)
    ):
        collected.add((type(value), value))
    return collected


def _sanitize_value(
    value: Any,
    sensitive_values: set[tuple[type[Any], Any]],
) -> tuple[Any, bool]:
    if isinstance(value, Mapping):
        sanitized: dict[str, Any] = {}
        sensitive_fields_omitted = False
        string_keys = [key for key in value if isinstance(key, str)]
        for key in sorted(string_keys):
            if key.casefold() in _SENSITIVE_KEYS:
                sensitive_fields_omitted = True
                continue
            nested_value, nested_omitted = _sanitize_value(
                value[key],
                sensitive_values,
            )
            sanitized[key] = nested_value
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized, sensitive_fields_omitted
    if isinstance(value, list):
        sanitized_items: list[Any] = []
        sensitive_fields_omitted = False
        for item in value:
            nested_value, nested_omitted = _sanitize_value(
                item,
                sensitive_values,
            )
            sanitized_items.append(nested_value)
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized_items, sensitive_fields_omitted
    if (
        isinstance(value, str)
        or isinstance(value, int)
        and not isinstance(value, bool)
        or isinstance(value, float)
        and math.isfinite(value)
    ) and (type(value), value) in sensitive_values:
        return "<sensitive value omitted>", True
    if value is None or isinstance(value, (str, bool, int)):
        return value, False
    if isinstance(value, float) and math.isfinite(value):
        return value, False
    return "<unsupported>", False


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "ALLOWED_EVENT_TYPES",
    "CANONICAL_EVENT_SCHEMA_VERSION",
    "GOVERNANCE_EVENT_SCHEMA_REGISTRY",
    "REQUIRED_TOP_LEVEL_EVENT_FIELDS",
    "SAFETY_BOUNDARIES",
    "SCHEMA_REGISTRY_VERSION",
    "get_governance_event_schema",
    "governance_event_schema_registry_to_json",
    "sanitize_governance_event",
    "validate_event_against_schema_registry",
]
