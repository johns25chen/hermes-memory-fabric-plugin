"""Deterministic, local-only audit reports for governance event replay."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any

from .event_driven_governance_kernel import replay_governance_events
from .governance_event_canonicalizer import (
    canonicalize_governance_event_sequence,
)
from .governance_transition_policy_registry import (
    GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
    SAFETY_BOUNDARIES,
    TRANSITION_POLICY_REGISTRY_VERSION,
)


REPLAY_AUDIT_REPORT_VERSION = "5.11.0"
REPLAY_AUDIT_SCHEMA_VERSION = "5.11.0"
REPLAY_AUDIT_HASH_ALGORITHM = "sha256"

ERROR_CATEGORY_TAXONOMY = (
    "schema_validation_error",
    "canonicalization_error",
    "duplicate_event_id",
    "invalid_previous_event_chain",
    "invalid_state_transition",
    "blocked_event",
    "malformed_event",
    "unknown_event_type",
    "invalid_payload_schema",
)

_AUDIT_REPORT_HASH_FIELDS = (
    "version",
    "schema_version",
    "audit_report_status",
    "replay_status",
    "canonicalization_status",
    "final_state",
    "accepted_event_count",
    "rejected_event_count",
    "blocking_reasons",
    "error_categories",
    "accepted_event_summaries",
    "rejected_event_summaries",
    "replay_outcome",
    "deterministic_replay_hash",
    "deterministic_sequence_hash",
    "next_allowed_events",
    "transition_policy_version",
    "transition_policy_registry_version",
    "policy_evaluation_summaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": REPLAY_AUDIT_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_AUDIT_REPORT_HASH_FIELDS),
    "input_shape": "sanitized replay audit report projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_events_included": False,
    "sensitive_fields_included": False,
}


def build_governance_replay_audit_report(
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build a deterministic, sanitized audit report for local replay."""

    try:
        event_sequence = list(events)
    except TypeError:
        event_sequence = []
        canonical_sequence = canonicalize_governance_event_sequence(events)
        replay_result = replay_governance_events(event_sequence)
        extra_blocking_reasons = ["events must be a sequence"]
    else:
        canonical_sequence = canonicalize_governance_event_sequence(
            event_sequence
        )
        replay_result = replay_governance_events(event_sequence)
        extra_blocking_reasons = []

    canonicalization_status = canonical_sequence[
        "canonicalization_status"
    ]
    replay_status = replay_result["audit_status"]
    blocking_reasons = _deduplicate(
        [
            *extra_blocking_reasons,
            *canonical_sequence["blocking_reasons"],
            *replay_result["blocking_reasons"],
        ]
    )
    error_categories = _classify_error_categories(
        blocking_reasons,
        canonicalization_blocked=canonicalization_status == "blocked",
        replay_blocked=replay_status == "blocked",
    )
    accepted_event_summaries = _accepted_event_summaries(replay_result)
    rejected_event_summaries = _rejected_event_summaries(replay_result)
    policy_evaluation_summaries = _policy_evaluation_summaries(
        replay_result
    )
    final_state = replay_result["current_state"]
    accepted_event_count = len(replay_result["accepted_events"])
    rejected_event_count = len(replay_result["rejected_events"])
    audit_report_status = (
        "pass"
        if canonicalization_status == "pass" and replay_status == "pass"
        else "blocked"
    )

    report: dict[str, Any] = {
        "version": REPLAY_AUDIT_REPORT_VERSION,
        "schema_version": REPLAY_AUDIT_SCHEMA_VERSION,
        "audit_report_status": audit_report_status,
        "replay_status": replay_status,
        "canonicalization_status": canonicalization_status,
        "final_state": final_state,
        "accepted_event_count": accepted_event_count,
        "rejected_event_count": rejected_event_count,
        "blocking_reasons": blocking_reasons,
        "error_categories": error_categories,
        "error_category_taxonomy": list(ERROR_CATEGORY_TAXONOMY),
        "accepted_event_summaries": accepted_event_summaries,
        "rejected_event_summaries": rejected_event_summaries,
        "transition_policy_version": GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
        "transition_policy_registry_version": (
            TRANSITION_POLICY_REGISTRY_VERSION
        ),
        "policy_evaluation_summaries": policy_evaluation_summaries,
        "canonical_events": canonical_sequence["canonical_events"],
        "canonical_sequence": canonical_sequence,
        "replay_outcome": {
            "accepted_event_count": accepted_event_count,
            "blocking_reasons": list(replay_result["blocking_reasons"]),
            "event_count": replay_result["event_count"],
            "final_state": final_state,
            "previous_state": replay_result["previous_state"],
            "rejected_event_count": rejected_event_count,
            "status": replay_status,
        },
        "deterministic_replay_hash": replay_result[
            "deterministic_replay_hash"
        ],
        "deterministic_sequence_hash": canonical_sequence[
            "deterministic_sequence_hash"
        ],
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "next_allowed_events": list(replay_result["next_allowed_events"]),
    }
    report["audit_report_hash"] = _audit_report_hash(report)

    safety_boundaries = dict(SAFETY_BOUNDARIES)
    report["safety_boundaries"] = safety_boundaries
    report.update(safety_boundaries)
    return report


def governance_replay_audit_report_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize a replay audit report deterministically."""

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


def _accepted_event_summaries(
    replay_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    canonical_events = iter(replay_result["accepted_events"])
    summaries: list[dict[str, Any]] = []
    for event_index, transition in enumerate(
        replay_result["transition_history"]
    ):
        if transition["accepted"] is not True:
            continue
        canonical_event = next(canonical_events)
        summary = {
            "event_index": event_index,
            **dict(canonical_event),
            "canonical_event_hash": _hash_json_value(canonical_event),
        }
        summaries.append(summary)
    return summaries


def _rejected_event_summaries(
    replay_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for rejection in replay_result["rejected_events"]:
        event = rejection.get("event")
        summary: dict[str, Any] = {
            "event_index": rejection["event_index"],
            "blocking_reasons": list(rejection["blocking_reasons"]),
            "error_categories": _classify_error_categories(
                rejection["blocking_reasons"],
                canonicalization_blocked=False,
                replay_blocked=True,
            ),
        }
        if isinstance(event, Mapping):
            for field in (
                "actor",
                "created_at",
                "event_id",
                "event_type",
                "payload",
                "previous_event_id",
                "schema_version",
                "sensitive_fields_omitted",
            ):
                if field in event:
                    summary[field] = _detached_json_value(event[field])
        summaries.append(summary)
    return summaries


def _policy_evaluation_summaries(
    replay_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for event_index, transition in enumerate(
        replay_result["transition_history"]
    ):
        evaluation = transition["policy_evaluation"]
        summaries.append(
            {
                "event_index": event_index,
                "valid_transition": evaluation["valid_transition"],
                "current_state": evaluation["current_state"],
                "event_type": evaluation["event_type"],
                "next_state": evaluation["next_state"],
                "blocking_reasons": list(
                    evaluation["blocking_reasons"]
                ),
                "policy_version": evaluation["policy_version"],
                "transition_policy": _detached_json_value(
                    evaluation["transition_policy"]
                ),
            }
        )
    return summaries


def _classify_error_categories(
    blocking_reasons: Sequence[str],
    *,
    canonicalization_blocked: bool,
    replay_blocked: bool,
) -> list[str]:
    categories: set[str] = set()
    for reason in blocking_reasons:
        if "event_id must be unique" in reason:
            categories.add("duplicate_event_id")
        if "previous_event_id does not match" in reason:
            categories.add("invalid_previous_event_chain")
        if "not allowed from the current governance state" in reason:
            categories.add("invalid_state_transition")
        if reason == "blocked event received":
            categories.add("blocked_event")
        if reason == "event_type is not allowed":
            categories.add("unknown_event_type")
        if (
            "payload must be a mapping" in reason
            or "required payload field" in reason
            or "payload field " in reason
        ):
            categories.add("invalid_payload_schema")
        if (
            reason == "event must be a mapping"
            or reason == "events must be a sequence"
            or reason.startswith("missing required field:")
            or (
                "must be a non-empty string" in reason
                and not reason.startswith("payload field ")
            )
        ):
            categories.add("malformed_event")
        if reason.startswith("schema_version must equal"):
            categories.add("schema_validation_error")
        if (
            "deterministic JSON-compatible" in reason
            or "string mapping keys" in reason
            or "finite floats" in reason
        ):
            categories.add("canonicalization_error")

    if canonicalization_blocked and not categories:
        categories.add("canonicalization_error")
    if replay_blocked and blocking_reasons and not categories:
        categories.add("schema_validation_error")
    return [
        category
        for category in ERROR_CATEGORY_TAXONOMY
        if category in categories
    ]


def _audit_report_hash(report: Mapping[str, Any]) -> str:
    hash_input = {
        field: report[field]
        for field in _AUDIT_REPORT_HASH_FIELDS
    }
    return _hash_json_value(hash_input)


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


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
    "ERROR_CATEGORY_TAXONOMY",
    "HASH_INPUT_CONTRACT",
    "REPLAY_AUDIT_HASH_ALGORITHM",
    "REPLAY_AUDIT_REPORT_VERSION",
    "REPLAY_AUDIT_SCHEMA_VERSION",
    "build_governance_replay_audit_report",
    "governance_replay_audit_report_to_json",
]
