"""Deterministic, local-only event-driven governance state machine."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from enum import StrEnum
import hashlib
import json
import math
from typing import Any, TypeAlias


KERNEL_VERSION = "4.0.0"
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

_STATE_ORDER = tuple(state.value for state in GovernanceState)
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
_REQUIRED_EVENT_FIELDS = (
    "event_id",
    "event_type",
    "actor",
    "created_at",
    "payload",
    "previous_event_id",
    "schema_version",
)

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

SAFETY_BOUNDARIES = {
    "unsafe_side_effects_performed": False,
    "memory_written": False,
    "durable_memory_written": False,
    "memory_graph_mutated": False,
    "operation_ledger_entry_created": False,
    "network_called": False,
    "github_api_called": False,
    "openclaw_called": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_executed": False,
    "approval_granted": False,
    "real_approval_granted": False,
    "real_human_decision_recorded": False,
    "dry_run_executed": False,
    "dry_run_plan_executed": False,
    "completion_executed": False,
    "attestation_executed": False,
    "finalization_executed": False,
    "autonomous_execution_authorized": False,
    "autonomous_governance_created": False,
    "consciousness_claimed": False,
    "self_awareness_claimed": False,
    "personhood_claimed": False,
    "sentience_claimed": False,
}


def validate_governance_event(event: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and sanitize one governance event without mutating it."""

    if not isinstance(event, Mapping):
        return {
            "valid": False,
            "blocking_reasons": ["event must be a mapping"],
            "sanitized_event": None,
        }

    blocking_reasons: list[str] = []
    for field in _REQUIRED_EVENT_FIELDS:
        if field not in event:
            blocking_reasons.append(f"missing required field: {field}")

    for field in ("event_id", "event_type", "actor", "created_at"):
        value = event.get(field)
        if not isinstance(value, str) or not value.strip():
            blocking_reasons.append(f"{field} must be a non-empty string")

    event_type = event.get("event_type")
    if isinstance(event_type, str) and event_type not in ALLOWED_EVENT_TYPES:
        blocking_reasons.append("event_type is not allowed")

    if event.get("schema_version") != KERNEL_VERSION:
        blocking_reasons.append(f"schema_version must equal {KERNEL_VERSION}")

    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        blocking_reasons.append("payload must be a mapping")

    previous_event_id = event.get("previous_event_id")
    if previous_event_id is not None and (
        not isinstance(previous_event_id, str) or not previous_event_id.strip()
    ):
        blocking_reasons.append("previous_event_id must be a non-empty string or None")

    compatible, sensitive_fields_omitted = _json_compatible(event)
    if not compatible:
        blocking_reasons.append(
            "event values must be deterministic JSON-compatible values with string mapping keys"
        )

    if blocking_reasons:
        return {
            "valid": False,
            "blocking_reasons": _deduplicate(blocking_reasons),
            "sanitized_event": None,
        }

    sanitized_event, sanitized_omitted = _sanitize_value(event)
    if not isinstance(sanitized_event, dict):
        return {
            "valid": False,
            "blocking_reasons": ["event could not be sanitized deterministically"],
            "sanitized_event": None,
        }
    if sensitive_fields_omitted or sanitized_omitted:
        sanitized_event["sensitive_fields_omitted"] = True

    return {
        "valid": True,
        "blocking_reasons": [],
        "sanitized_event": sanitized_event,
    }


def apply_governance_event(
    current_state: str,
    event: Mapping[str, Any],
    previous_event_id: str | None = None,
) -> dict[str, Any]:
    """Apply one event to a state and return a side-effect-free transition."""

    state = _state_value(current_state)
    validation = validate_governance_event(event)
    event_id = _safe_non_empty_string(event, "event_id")
    event_type = _safe_non_empty_string(event, "event_type")

    blocking_reasons = list(validation["blocking_reasons"])
    if state not in STATE_MACHINE:
        blocking_reasons.append("current_state is not a recognized governance state")

    if validation["valid"] and event.get("previous_event_id") != previous_event_id:
        blocking_reasons.append(
            "previous_event_id does not match the prior accepted event"
        )

    if not blocking_reasons:
        next_state = STATE_MACHINE[state].get(str(event_type))
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

    next_state = STATE_MACHINE[state][str(event_type)]
    transition_reasons = (
        ["blocked event received"]
        if event_type == "blocked"
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
    rejected_events: list[dict[str, Any]] = []
    transition_history: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    for index, event in enumerate(event_sequence):
        validation = validate_governance_event(event)
        event_id = _safe_non_empty_string(event, "event_id")
        event_type = _safe_non_empty_string(event, "event_type")
        rejection_reasons = list(validation["blocking_reasons"])

        if event_id is not None and event_id in seen_event_ids:
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
            sanitized_event = validation["sanitized_event"]
            if not isinstance(sanitized_event, dict):
                raise AssertionError("validated event must have a sanitized mapping")
            accepted_events.append(sanitized_event)
            if event_id is not None:
                seen_event_ids.add(event_id)
                previous_event_id = event_id
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

    audit_status = (
        "pass"
        if not rejected_events and current_state != GovernanceState.BLOCKED.value
        else "blocked"
    )
    replay_hash = _deterministic_replay_hash(accepted_events, current_state)
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


def _json_compatible(value: Any) -> tuple[bool, bool]:
    if isinstance(value, Mapping):
        sensitive_fields_omitted = False
        for key, nested_value in value.items():
            if not isinstance(key, str):
                return False, sensitive_fields_omitted
            if key.casefold() in _SENSITIVE_KEYS:
                sensitive_fields_omitted = True
                continue
            compatible, nested_omitted = _json_compatible(nested_value)
            if not compatible:
                return False, sensitive_fields_omitted or nested_omitted
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return True, sensitive_fields_omitted
    if isinstance(value, (list, tuple)):
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


def _sanitize_value(value: Any) -> tuple[Any, bool]:
    if isinstance(value, Mapping):
        sanitized: dict[str, Any] = {}
        sensitive_fields_omitted = False
        string_keys = [key for key in value if isinstance(key, str)]
        for key in sorted(string_keys):
            if key.casefold() in _SENSITIVE_KEYS:
                sensitive_fields_omitted = True
                continue
            nested_value, nested_omitted = _sanitize_value(value[key])
            sanitized[key] = nested_value
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized, sensitive_fields_omitted
    if isinstance(value, (list, tuple)):
        sanitized_items: list[Any] = []
        sensitive_fields_omitted = False
        for item in value:
            nested_value, nested_omitted = _sanitize_value(item)
            sanitized_items.append(nested_value)
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized_items, sensitive_fields_omitted
    if value is None or isinstance(value, (str, bool, int)):
        return value, False
    if isinstance(value, float) and math.isfinite(value):
        return value, False
    return "<unsupported>", False


def _sanitized_rejection_snapshot(event: Any) -> dict[str, Any] | None:
    if not isinstance(event, Mapping):
        return None
    sanitized, sensitive_fields_omitted = _sanitize_value(event)
    if not isinstance(sanitized, dict):
        return None
    if sensitive_fields_omitted:
        sanitized["sensitive_fields_omitted"] = True
    return sanitized


def _deterministic_replay_hash(
    accepted_events: Sequence[Mapping[str, Any]],
    final_state: str,
) -> str:
    payload = {
        "accepted_events": list(accepted_events),
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
