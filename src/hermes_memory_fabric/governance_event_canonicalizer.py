"""Deterministic, local-only canonicalization for governance events."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_event_schema_registry import (
    SAFETY_BOUNDARIES,
    sanitize_governance_event,
    validate_event_against_schema_registry,
)


CANONICALIZER_VERSION = "4.9.0"
CANONICAL_EVENT_SCHEMA_VERSION = "4.9.0"
CANONICAL_EVENT_HASH_ALGORITHM = "sha256"

CANONICAL_EVENT_FIELDS = (
    "actor",
    "canonicalization_version",
    "created_at",
    "event_id",
    "event_type",
    "payload",
    "previous_event_id",
    "schema_version",
)

HASH_INPUT_CONTRACT = {
    "algorithm": CANONICAL_EVENT_HASH_ALGORITHM,
    "canonical_event_fields": list(CANONICAL_EVENT_FIELDS),
    "canonicalization_version": CANONICALIZER_VERSION,
    "encoding": "utf-8",
    "input_shape": {
        "canonical_events": "ordered canonical event list",
        "canonicalization_version": CANONICALIZER_VERSION,
    },
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "list_order_preserved": True,
}


def canonicalize_governance_event(
    event: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and return the canonical representation of one event."""

    validation = validate_event_against_schema_registry(event)
    if validation["valid"] is not True:
        reasons = "; ".join(validation["blocking_reasons"])
        raise ValueError(
            f"governance event canonicalization blocked: {reasons}"
        )

    sanitized_event = validation["sanitized_event"]
    if not isinstance(sanitized_event, Mapping):
        raise ValueError(
            "governance event canonicalization blocked: "
            "validated event is not a mapping"
        )

    projected = {
        "actor": sanitized_event["actor"],
        "canonicalization_version": CANONICALIZER_VERSION,
        "created_at": sanitized_event["created_at"],
        "event_id": sanitized_event["event_id"],
        "event_type": sanitized_event["event_type"],
        "payload": sanitized_event["payload"],
        "previous_event_id": sanitized_event["previous_event_id"],
        "schema_version": sanitized_event["schema_version"],
    }
    canonical = _canonicalize_value(projected)
    if not isinstance(canonical, dict):
        raise AssertionError("canonical governance event must be a mapping")
    return canonical


def canonicalize_governance_event_sequence(
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Canonicalize an ordered event sequence and fail closed on rejection."""

    try:
        event_sequence = list(events)
    except TypeError:
        return _sequence_result(
            event_count=0,
            canonical_events=[],
            rejected_events=[],
            blocking_reasons=["events must be a sequence"],
        )

    canonical_events: list[dict[str, Any]] = []
    rejected_events: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []
    seen_event_ids: set[str] = set()
    previous_event_id: str | None = None

    for index, event in enumerate(event_sequence):
        validation = validate_event_against_schema_registry(event)
        event_reasons = list(validation["blocking_reasons"])
        event_id = _non_empty_string(event, "event_id")

        if event_id is not None and event_id in seen_event_ids:
            event_reasons.append(
                "event_id must be unique within a canonical sequence"
            )

        event_previous_id = (
            event.get("previous_event_id")
            if isinstance(event, Mapping)
            else None
        )
        if event_previous_id != previous_event_id:
            event_reasons.append(
                "previous_event_id does not match the prior sequence event"
            )

        if event_reasons:
            deduplicated_reasons = _deduplicate(event_reasons)
            rejected_events.append(
                {
                    "blocking_reasons": deduplicated_reasons,
                    "event": _rejection_snapshot(event),
                    "event_index": index,
                }
            )
            blocking_reasons.extend(deduplicated_reasons)
        else:
            canonical_events.append(canonicalize_governance_event(event))

        if event_id is not None:
            seen_event_ids.add(event_id)
        previous_event_id = event_id

    return _sequence_result(
        event_count=len(event_sequence),
        canonical_events=canonical_events,
        rejected_events=rejected_events,
        blocking_reasons=_deduplicate(blocking_reasons),
    )


def governance_event_canonicalizer_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize a canonicalization result deterministically."""

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


def _sequence_result(
    *,
    event_count: int,
    canonical_events: Sequence[Mapping[str, Any]],
    rejected_events: Sequence[Mapping[str, Any]],
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    canonical_event_list = [dict(event) for event in canonical_events]
    rejected_event_list = [dict(event) for event in rejected_events]
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": CANONICALIZER_VERSION,
        "canonicalization_status": (
            "pass" if not rejected_event_list and not blocking_reasons else "blocked"
        ),
        "canonical_events": canonical_event_list,
        "rejected_events": rejected_event_list,
        "blocking_reasons": list(blocking_reasons),
        "event_count": event_count,
        "canonical_event_count": len(canonical_event_list),
        "rejected_event_count": len(rejected_event_list),
        "deterministic_sequence_hash": _deterministic_sequence_hash(
            canonical_event_list
        ),
        "hash_input_contract": _canonicalize_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _deterministic_sequence_hash(
    canonical_events: Sequence[Mapping[str, Any]],
) -> str:
    hash_input = {
        "canonical_events": list(canonical_events),
        "canonicalization_version": CANONICALIZER_VERSION,
    }
    serialized = json.dumps(
        hash_input,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _canonicalize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError(
                "governance event canonicalization blocked: "
                "mapping keys must be strings"
            )
        return {
            key: _canonicalize_value(value[key])
            for key in sorted(value)
        }
    if isinstance(value, list):
        return [_canonicalize_value(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(
                "governance event canonicalization blocked: "
                "floats must be finite"
            )
        return value
    raise ValueError(
        "governance event canonicalization blocked: "
        "value is not deterministic JSON-compatible"
    )


def _rejection_snapshot(event: Any) -> dict[str, Any] | None:
    if not isinstance(event, Mapping):
        return None
    sanitized_event = sanitize_governance_event(event)
    snapshot = {
        key: sanitized_event[key]
        for key in CANONICAL_EVENT_FIELDS
        if key != "canonicalization_version" and key in sanitized_event
    }
    snapshot["canonicalization_version"] = CANONICALIZER_VERSION
    canonical = _canonicalize_value(snapshot)
    if not isinstance(canonical, dict):
        return None
    return canonical


def _non_empty_string(event: Any, field: str) -> str | None:
    if not isinstance(event, Mapping):
        return None
    value = event.get(field)
    if isinstance(value, str) and value.strip():
        return value
    return None


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "CANONICALIZER_VERSION",
    "CANONICAL_EVENT_FIELDS",
    "CANONICAL_EVENT_HASH_ALGORITHM",
    "CANONICAL_EVENT_SCHEMA_VERSION",
    "HASH_INPUT_CONTRACT",
    "canonicalize_governance_event",
    "canonicalize_governance_event_sequence",
    "governance_event_canonicalizer_to_json",
]
