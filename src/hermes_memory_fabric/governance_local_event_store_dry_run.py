"""Deterministic in-process governance event store simulation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any

from .governance_event_canonicalizer import (
    canonicalize_governance_event,
    canonicalize_governance_event_sequence,
)
from .governance_replay_audit_report import (
    build_governance_replay_audit_report,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


LOCAL_EVENT_STORE_DRY_RUN_VERSION = "5.11.0"
LOCAL_EVENT_STORE_SCHEMA_VERSION = "5.11.0"
LOCAL_EVENT_STORE_MODE = "in_memory_dry_run_only"
LOCAL_EVENT_STORE_HASH_ALGORITHM = "sha256"


def create_governance_local_event_store_dry_run() -> dict[str, Any]:
    """Create a deterministic empty local event store simulation."""

    return _build_store([])


def append_governance_event_to_local_store_dry_run(
    store: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    """Return a new store simulation containing one canonical event."""

    normalized_store, store_reasons = _inspect_store(store)
    if store_reasons:
        return _append_result(
            append_status="blocked",
            store=normalized_store,
            appended_event=None,
            blocking_reasons=store_reasons,
        )

    try:
        canonical_event = canonicalize_governance_event(event)
    except ValueError as exc:
        return _append_result(
            append_status="blocked",
            store=normalized_store,
            appended_event=None,
            blocking_reasons=_canonicalization_reasons(exc),
        )
    except TypeError:
        return _append_result(
            append_status="blocked",
            store=normalized_store,
            appended_event=None,
            blocking_reasons=[
                "event must be deterministic JSON-compatible"
            ],
        )

    blocking_reasons: list[str] = []
    event_id = canonical_event["event_id"]
    if event_id in normalized_store["event_ids"]:
        blocking_reasons.append(
            "event_id must be unique within the local event store"
        )

    expected_previous_event_id = (
        normalized_store["event_ids"][-1]
        if normalized_store["event_ids"]
        else None
    )
    if canonical_event["previous_event_id"] != expected_previous_event_id:
        blocking_reasons.append(
            "previous_event_id does not match the prior local store event"
        )

    if blocking_reasons:
        return _append_result(
            append_status="blocked",
            store=normalized_store,
            appended_event=None,
            blocking_reasons=blocking_reasons,
        )

    appended_event = _detached_json_value(canonical_event)
    next_store = _build_store(
        [
            *normalized_store["canonical_events"],
            appended_event,
        ]
    )
    return _append_result(
        append_status="pass",
        store=next_store,
        appended_event=appended_event,
        blocking_reasons=[],
    )


def append_governance_events_to_local_store_dry_run(
    store: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Append events in order and stop at the first blocked event."""

    normalized_store, store_reasons = _inspect_store(store)
    if store_reasons:
        return _append_sequence_result(
            append_sequence_status="blocked",
            store=normalized_store,
            appended_event_count=0,
            rejected_event_count=1,
            blocking_reasons=store_reasons,
        )

    if isinstance(events, (str, bytes, bytearray, Mapping)):
        return _append_sequence_result(
            append_sequence_status="blocked",
            store=normalized_store,
            appended_event_count=0,
            rejected_event_count=1,
            blocking_reasons=["events must be a sequence of mappings"],
        )
    try:
        event_sequence = list(events)
    except TypeError:
        return _append_sequence_result(
            append_sequence_status="blocked",
            store=normalized_store,
            appended_event_count=0,
            rejected_event_count=1,
            blocking_reasons=["events must be a sequence of mappings"],
        )

    current_store = normalized_store
    appended_event_count = 0
    for event_index, event in enumerate(event_sequence):
        append_result = append_governance_event_to_local_store_dry_run(
            current_store,
            event,
        )
        current_store = append_result["store"]
        if append_result["append_status"] != "pass":
            return _append_sequence_result(
                append_sequence_status="blocked",
                store=current_store,
                appended_event_count=appended_event_count,
                rejected_event_count=1,
                blocking_reasons=[
                    f"event[{event_index}]: {reason}"
                    for reason in append_result["blocking_reasons"]
                ],
            )
        appended_event_count += 1

    return _append_sequence_result(
        append_sequence_status="pass",
        store=current_store,
        appended_event_count=appended_event_count,
        rejected_event_count=0,
        blocking_reasons=[],
    )


def read_governance_local_event_store_dry_run(
    store: Mapping[str, Any],
) -> dict[str, Any]:
    """Read a detached deterministic view of the store simulation."""

    normalized_store, blocking_reasons = _inspect_store(store)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "schema_version": LOCAL_EVENT_STORE_SCHEMA_VERSION,
        "store_mode": LOCAL_EVENT_STORE_MODE,
        "read_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": blocking_reasons,
        "event_count": normalized_store["event_count"],
        "canonical_events": _detached_json_value(
            normalized_store["canonical_events"]
        ),
        "event_ids": list(normalized_store["event_ids"]),
        "deterministic_store_hash": normalized_store[
            "deterministic_store_hash"
        ],
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def build_governance_local_event_store_replay_report_dry_run(
    store: Mapping[str, Any],
) -> dict[str, Any]:
    """Replay the detached canonical events held by the store simulation."""

    normalized_store, blocking_reasons = _inspect_store(store)
    replay_audit_report = build_governance_replay_audit_report(
        normalized_store["canonical_events"]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "schema_version": LOCAL_EVENT_STORE_SCHEMA_VERSION,
        "store_mode": LOCAL_EVENT_STORE_MODE,
        "replay_report_status": (
            replay_audit_report["audit_report_status"]
            if not blocking_reasons
            else "blocked"
        ),
        "blocking_reasons": blocking_reasons,
        "event_count": normalized_store["event_count"],
        "replay_audit_report": replay_audit_report,
        "deterministic_store_hash": normalized_store[
            "deterministic_store_hash"
        ],
        "deterministic_replay_hash": replay_audit_report[
            "deterministic_replay_hash"
        ],
        "deterministic_sequence_hash": replay_audit_report[
            "deterministic_sequence_hash"
        ],
        "audit_report_hash": replay_audit_report["audit_report_hash"],
        "final_state": replay_audit_report["final_state"],
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def governance_local_event_store_dry_run_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize a local event store result deterministically."""

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


def _build_store(
    canonical_events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    detached_events = _detached_json_value(list(canonical_events))
    event_ids = [event["event_id"] for event in detached_events]
    deterministic_store_hash = _deterministic_store_hash(
        detached_events,
        event_ids,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "schema_version": LOCAL_EVENT_STORE_SCHEMA_VERSION,
        "store_mode": LOCAL_EVENT_STORE_MODE,
        "hash_algorithm": LOCAL_EVENT_STORE_HASH_ALGORITHM,
        "event_count": len(detached_events),
        "canonical_events": detached_events,
        "event_ids": event_ids,
        "deterministic_store_hash": deterministic_store_hash,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _inspect_store(
    store: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    empty_store = _build_store([])
    if not isinstance(store, Mapping):
        return empty_store, ["store must be a mapping"]

    raw_events = store.get("canonical_events")
    if isinstance(raw_events, (str, bytes, bytearray, Mapping)):
        return empty_store, ["store canonical_events must be a sequence"]
    try:
        event_sequence = list(raw_events)
    except TypeError:
        return empty_store, ["store canonical_events must be a sequence"]

    try:
        canonical_sequence = canonicalize_governance_event_sequence(
            event_sequence
        )
    except (TypeError, ValueError):
        return empty_store, [
            "store canonical_events must be deterministic and canonical"
        ]

    if canonical_sequence["canonicalization_status"] != "pass":
        return empty_store, [
            f"store canonical_events: {reason}"
            for reason in canonical_sequence["blocking_reasons"]
        ]

    normalized_store = _build_store(
        canonical_sequence["canonical_events"]
    )
    blocking_reasons: list[str] = []
    if list(event_sequence) != normalized_store["canonical_events"]:
        blocking_reasons.append(
            "store canonical_events must already be canonical and sanitized"
        )
    if store.get("version") != LOCAL_EVENT_STORE_DRY_RUN_VERSION:
        blocking_reasons.append(
            f"store version must equal {LOCAL_EVENT_STORE_DRY_RUN_VERSION}"
        )
    if store.get("schema_version") != LOCAL_EVENT_STORE_SCHEMA_VERSION:
        blocking_reasons.append(
            "store schema_version must equal "
            f"{LOCAL_EVENT_STORE_SCHEMA_VERSION}"
        )
    if store.get("store_mode") != LOCAL_EVENT_STORE_MODE:
        blocking_reasons.append(
            f"store_mode must equal {LOCAL_EVENT_STORE_MODE}"
        )
    if store.get("hash_algorithm") != LOCAL_EVENT_STORE_HASH_ALGORITHM:
        blocking_reasons.append(
            "hash_algorithm must equal "
            f"{LOCAL_EVENT_STORE_HASH_ALGORITHM}"
        )
    if store.get("event_count") != normalized_store["event_count"]:
        blocking_reasons.append(
            "event_count must match canonical_events"
        )
    if store.get("event_ids") != normalized_store["event_ids"]:
        blocking_reasons.append("event_ids must match canonical_events")
    if (
        store.get("deterministic_store_hash")
        != normalized_store["deterministic_store_hash"]
    ):
        blocking_reasons.append(
            "deterministic_store_hash must match canonical_events"
        )

    store_safety = store.get("safety_boundaries")
    safety_is_false = isinstance(store_safety, Mapping) and all(
        store.get(key) is False and store_safety.get(key) is False
        for key in SAFETY_BOUNDARIES
    )
    if not safety_is_false:
        blocking_reasons.append(
            "store safety boundaries must remain false"
        )
    return normalized_store, _deduplicate(blocking_reasons)


def _append_result(
    *,
    append_status: str,
    store: Mapping[str, Any],
    appended_event: Mapping[str, Any] | None,
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    detached_store = _detached_json_value(store)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "append_status": append_status,
        "store": detached_store,
        "appended_event": (
            _detached_json_value(appended_event)
            if appended_event is not None
            else None
        ),
        "blocking_reasons": list(blocking_reasons),
        "deterministic_store_hash": detached_store[
            "deterministic_store_hash"
        ],
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _append_sequence_result(
    *,
    append_sequence_status: str,
    store: Mapping[str, Any],
    appended_event_count: int,
    rejected_event_count: int,
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    detached_store = _detached_json_value(store)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "append_sequence_status": append_sequence_status,
        "store": detached_store,
        "appended_event_count": appended_event_count,
        "rejected_event_count": rejected_event_count,
        "blocking_reasons": list(blocking_reasons),
        "deterministic_store_hash": detached_store[
            "deterministic_store_hash"
        ],
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _deterministic_store_hash(
    canonical_events: Sequence[Mapping[str, Any]],
    event_ids: Sequence[str],
) -> str:
    hash_input = {
        "version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "store_mode": LOCAL_EVENT_STORE_MODE,
        "canonical_events": list(canonical_events),
        "event_ids": list(event_ids),
    }
    serialized = json.dumps(
        hash_input,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _canonicalization_reasons(exc: ValueError) -> list[str]:
    message = str(exc)
    prefix = "governance event canonicalization blocked: "
    details = message[len(prefix) :] if message.startswith(prefix) else message
    return _deduplicate(
        [reason.strip() for reason in details.split(";") if reason.strip()]
    )


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "LOCAL_EVENT_STORE_DRY_RUN_VERSION",
    "LOCAL_EVENT_STORE_HASH_ALGORITHM",
    "LOCAL_EVENT_STORE_MODE",
    "LOCAL_EVENT_STORE_SCHEMA_VERSION",
    "SAFETY_BOUNDARIES",
    "append_governance_event_to_local_store_dry_run",
    "append_governance_events_to_local_store_dry_run",
    "build_governance_local_event_store_replay_report_dry_run",
    "create_governance_local_event_store_dry_run",
    "governance_local_event_store_dry_run_to_json",
    "read_governance_local_event_store_dry_run",
]
