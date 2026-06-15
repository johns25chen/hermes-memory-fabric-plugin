"""Deterministic, local-only event-driven governance state machine."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
import hashlib
import json
from typing import Any, TypeAlias

from .governance_event_canonicalizer import (
    canonicalize_governance_event_sequence,
)
from .governance_event_schema_registry import (
    ALLOWED_EVENT_TYPES,
    CANONICAL_EVENT_SCHEMA_VERSION,
    SAFETY_BOUNDARIES,
    sanitize_governance_event,
    validate_event_against_schema_registry,
)


KERNEL_VERSION = CANONICAL_EVENT_SCHEMA_VERSION
KERNEL_NAME = "event_driven_governance_kernel"


class GovernanceState(StrEnum):
    """States in the local governance kernel."""

    INITIALIZED = "initialized"
    PROPOSAL_OPEN = "proposal_open"
    REVIEW_READY = "review_ready"
    APPROVED_FOR_DRY_RUN = "approved_for_dry_run"
    DRY_RUN_READY = "dry_run_ready"
    DRY_RUN_COMPLETED = "dry_run_completed"
    ATTESTATION_READY = "attestation_ready"
    FINALIZED = "finalized"
    BLOCKED = "blocked"


GovernanceEvent: TypeAlias = Mapping[str, Any]
GovernanceRecord: TypeAlias = dict[str, Any]

_STATE_ORDER = tuple(state.value for state in GovernanceState)

STATE_MACHINE: dict[str, dict[str, str]] = {
    GovernanceState.INITIALIZED.value: {
        "governance_kernel_initialized": GovernanceState.PROPOSAL_OPEN.value,
        "proposal_submitted": GovernanceState.PROPOSAL_OPEN.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.PROPOSAL_OPEN.value: {
        "proposal_submitted": GovernanceState.PROPOSAL_OPEN.value,
        "review_completed": GovernanceState.REVIEW_READY.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.REVIEW_READY.value: {
        "dry_run_approved": GovernanceState.APPROVED_FOR_DRY_RUN.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.APPROVED_FOR_DRY_RUN.value: {
        "dry_run_prepared": GovernanceState.DRY_RUN_READY.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.DRY_RUN_READY.value: {
        "dry_run_completed": GovernanceState.DRY_RUN_COMPLETED.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.DRY_RUN_COMPLETED.value: {
        "attestation_submitted": GovernanceState.ATTESTATION_READY.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.ATTESTATION_READY.value: {
        "finalization_requested": GovernanceState.FINALIZED.value,
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.FINALIZED.value: {
        "blocked": GovernanceState.BLOCKED.value,
    },
    GovernanceState.BLOCKED.value: {
        "blocked": GovernanceState.BLOCKED.value,
    },
}

def validate_governance_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Delegate event validation to the canonical schema registry."""

    return validate_event_against_schema_registry(event)


def apply_governance_event(
    current_state: str,
    event: Mapping[str, Any],
    previous_event_id: str | None = None,
) -> dict[str, Any]:
    """Apply one event to a state and return a side-effect-free transition."""

    state = _state_value(current_state)
    validation = validate_governance_event(event)
    raw_event_type = _safe_non_empty_string(event, "event_type")
    sanitized_event = sanitize_governance_event(event)
    event_id = _safe_non_empty_string(sanitized_event, "event_id")
    event_type = _safe_non_empty_string(sanitized_event, "event_type")

    blocking_reasons = list(validation["blocking_reasons"])
    if state not in STATE_MACHINE:
        blocking_reasons.append("current_state is not a recognized governance state")

    if validation["valid"] and event.get("previous_event_id") != previous_event_id:
        blocking_reasons.append(
            "previous_event_id does not match the prior accepted event"
        )

    if not blocking_reasons:
        next_state = STATE_MACHINE[state].get(str(raw_event_type))
        if next_state is None:
            blocking_reasons.append(
                "event_type is not allowed from the current governance state"
            )

    if blocking_reasons:
        return _transition(
            accepted=False,
            previous_state=state,
            next_state=GovernanceState.BLOCKED.value,
            event_id=event_id,
            event_type=event_type,
            blocking_reasons=blocking_reasons,
        )

    next_state = STATE_MACHINE[state][str(raw_event_type)]
    transition_reasons = (
        ["blocked event received"]
        if raw_event_type == "blocked"
        else []
    )
    return _transition(
        accepted=True,
        previous_state=state,
        next_state=next_state,
        event_id=event_id,
        event_type=event_type,
        blocking_reasons=transition_reasons,
    )


def replay_governance_events(
    events: Sequence[Mapping[str, Any]],
) -> GovernanceRecord:
    """Replay governance events into a deterministic, sanitized audit report."""

    event_sequence = list(events)
    current_state = GovernanceState.INITIALIZED.value
    previous_state = current_state
    previous_event_id: str | None = None
    seen_event_ids: set[str] = set()
    accepted_events: list[dict[str, Any]] = []
    accepted_source_events: list[Mapping[str, Any]] = []
    rejected_events: list[dict[str, Any]] = []
    transition_history: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    for index, event in enumerate(event_sequence):
        validation = validate_governance_event(event)
        raw_event_id = _safe_non_empty_string(event, "event_id")
        sanitized_event = sanitize_governance_event(event)
        event_id = _safe_non_empty_string(sanitized_event, "event_id")
        event_type = _safe_non_empty_string(sanitized_event, "event_type")
        rejection_reasons = list(validation["blocking_reasons"])

        if raw_event_id is not None and raw_event_id in seen_event_ids:
            rejection_reasons.append("event_id must be unique within a replay")

        if rejection_reasons:
            transition = _transition(
                accepted=False,
                previous_state=current_state,
                next_state=GovernanceState.BLOCKED.value,
                event_id=event_id,
                event_type=event_type,
                blocking_reasons=rejection_reasons,
            )
        else:
            transition = apply_governance_event(
                current_state,
                event,
                previous_event_id=previous_event_id,
            )

        previous_state = current_state
        current_state = transition["next_state"]
        transition_history.append(transition)

        if transition["accepted"]:
            accepted_source_events.append(event)
            if raw_event_id is not None:
                seen_event_ids.add(raw_event_id)
                previous_event_id = raw_event_id
            blocking_reasons.extend(transition["blocking_reasons"])
        else:
            rejection_snapshot = _sanitized_rejection_snapshot(event)
            rejected_events.append(
                {
                    "event_index": index,
                    "event": rejection_snapshot,
                    "blocking_reasons": list(transition["blocking_reasons"]),
                }
            )
            blocking_reasons.extend(transition["blocking_reasons"])

    canonical_sequence = canonicalize_governance_event_sequence(
        accepted_source_events
    )
    if canonical_sequence["canonicalization_status"] != "pass":
        raise AssertionError("accepted events must form a canonical sequence")
    accepted_events = canonical_sequence["canonical_events"]

    audit_status = (
        "pass"
        if not rejected_events and current_state != GovernanceState.BLOCKED.value
        else "blocked"
    )
    replay_hash = _deterministic_replay_hash(
        canonical_sequence["deterministic_sequence_hash"],
        current_state,
    )
    next_allowed_events = list(STATE_MACHINE[current_state])
    safety_boundaries = dict(SAFETY_BOUNDARIES)

    return {
        "version": KERNEL_VERSION,
        "kernel_name": KERNEL_NAME,
        "current_state": current_state,
        "previous_state": previous_state,
        "event_count": len(event_sequence),
        "accepted_events": accepted_events,
        "rejected_events": rejected_events,
        "transition_history": transition_history,
        "blocking_reasons": _deduplicate(blocking_reasons),
        "audit_status": audit_status,
        "replay_safe": True,
        "deterministic_replay_hash": replay_hash,
        "state_machine": _state_machine_report(),
        "allowed_transitions": _allowed_transition_report(),
        "final_report": {
            "current_state": current_state,
            "accepted_event_count": len(accepted_events),
            "rejected_event_count": len(rejected_events),
            "audit_status": audit_status,
            "kernel_states_claim_real_world_execution": False,
        },
        "safety_boundaries": safety_boundaries,
        "next_allowed_events": next_allowed_events,
        **safety_boundaries,
    }


def _transition(
    *,
    accepted: bool,
    previous_state: str,
    next_state: str,
    event_id: str | None,
    event_type: str | None,
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "accepted": accepted,
        "previous_state": previous_state,
        "next_state": next_state,
        "event_id": event_id,
        "event_type": event_type,
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _state_value(state: str) -> str:
    if isinstance(state, GovernanceState):
        return state.value
    return state if isinstance(state, str) else ""


def _safe_non_empty_string(
    event: Mapping[str, Any] | Any,
    field: str,
) -> str | None:
    if not isinstance(event, Mapping):
        return None
    value = event.get(field)
    if isinstance(value, str) and value.strip():
        return value
    return None


def _sanitized_rejection_snapshot(event: Any) -> dict[str, Any] | None:
    if not isinstance(event, Mapping):
        return None
    return sanitize_governance_event(event)


def _deterministic_replay_hash(
    canonical_sequence_hash: str,
    final_state: str,
) -> str:
    payload = {
        "canonical_sequence_hash": canonical_sequence_hash,
        "final_state": final_state,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _state_machine_report() -> dict[str, dict[str, str]]:
    return {
        state: dict(STATE_MACHINE[state])
        for state in _STATE_ORDER
    }


def _allowed_transition_report() -> list[dict[str, str]]:
    return [
        {
            "previous_state": state,
            "event_type": event_type,
            "next_state": next_state,
        }
        for state in _STATE_ORDER
        for event_type, next_state in STATE_MACHINE[state].items()
    ]


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "ALLOWED_EVENT_TYPES",
    "GovernanceEvent",
    "GovernanceRecord",
    "GovernanceState",
    "KERNEL_NAME",
    "KERNEL_VERSION",
    "SAFETY_BOUNDARIES",
    "STATE_MACHINE",
    "apply_governance_event",
    "replay_governance_events",
    "validate_governance_event",
]
