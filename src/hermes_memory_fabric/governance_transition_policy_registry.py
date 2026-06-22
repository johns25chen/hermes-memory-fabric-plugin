"""Deterministic, local-only governance transition policy registry."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
from typing import Any


TRANSITION_POLICY_REGISTRY_VERSION = "6.5.0"
TRANSITION_POLICY_SCHEMA_VERSION = "6.5.0"
GOVERNANCE_STATE_MACHINE_POLICY_VERSION = "6.5.0"

ALLOWED_GOVERNANCE_STATES = (
    "initialized",
    "proposal_open",
    "review_ready",
    "approved_for_dry_run",
    "dry_run_ready",
    "dry_run_completed",
    "attestation_ready",
    "finalized",
    "blocked",
)

GOVERNANCE_TRANSITION_POLICY_REGISTRY: dict[str, dict[str, str]] = {
    "initialized": {
        "governance_kernel_initialized": "proposal_open",
        "proposal_submitted": "proposal_open",
        "blocked": "blocked",
    },
    "proposal_open": {
        "proposal_submitted": "proposal_open",
        "review_completed": "review_ready",
        "blocked": "blocked",
    },
    "review_ready": {
        "dry_run_approved": "approved_for_dry_run",
        "blocked": "blocked",
    },
    "approved_for_dry_run": {
        "dry_run_prepared": "dry_run_ready",
        "blocked": "blocked",
    },
    "dry_run_ready": {
        "dry_run_completed": "dry_run_completed",
        "blocked": "blocked",
    },
    "dry_run_completed": {
        "attestation_submitted": "attestation_ready",
        "blocked": "blocked",
    },
    "attestation_ready": {
        "finalization_requested": "finalized",
        "blocked": "blocked",
    },
    "finalized": {"blocked": "blocked"},
    "blocked": {"blocked": "blocked"},
}

SAFETY_BOUNDARIES = {
    "unsafe_side_effects_performed": False,
    "real_execution_performed": False,
    "execution_adapter_invoked": False,
    "external_calls_performed": False,
    "filesystem_written": False,
    "database_written": False,
    "memory_written": False,
    "durable_memory_written": False,
    "memory_graph_mutated": False,
    "operation_ledger_entry_created": False,
    "network_called": False,
    "github_api_called": False,
    "openclaw_called": False,
    "composio_called": False,
    "request_created": False,
    "request_submitted": False,
    "request_executed": False,
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
    "scheduling_performed": False,
    "handoff_performed": False,
    "consciousness_claimed": False,
    "self_awareness_claimed": False,
    "personhood_claimed": False,
    "sentience_claimed": False,
}

_KNOWN_EVENT_TYPES = frozenset(
    event_type
    for state in ALLOWED_GOVERNANCE_STATES
    for event_type in GOVERNANCE_TRANSITION_POLICY_REGISTRY[state]
)


def get_governance_transition_policy(state: str) -> dict[str, Any]:
    """Return a detached transition policy for a governance state."""

    normalized_state = state if isinstance(state, str) else ""
    policy = GOVERNANCE_TRANSITION_POLICY_REGISTRY.get(normalized_state)
    if policy is None:
        return {
            "state": normalized_state,
            "policy_status": "blocked",
            "known_state": False,
            "allowed_events": [],
            "next_states": {},
            "policy_version": GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
        }
    return {
        "state": normalized_state,
        "policy_status": "active",
        "known_state": True,
        "allowed_events": list(policy),
        "next_states": dict(policy),
        "policy_version": GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
    }


def evaluate_governance_transition(
    state: str,
    event_type: str,
) -> dict[str, Any]:
    """Evaluate one transition without performing side effects."""

    normalized_state = state if isinstance(state, str) else ""
    normalized_event_type = event_type if isinstance(event_type, str) else ""
    transition_policy = get_governance_transition_policy(normalized_state)
    blocking_reasons: list[str] = []
    next_state = "blocked"

    if transition_policy["known_state"] is not True:
        blocking_reasons.append(
            "current_state is not a recognized governance state"
        )
    elif normalized_event_type not in _KNOWN_EVENT_TYPES:
        blocking_reasons.append(
            "event_type is not a recognized governance event type"
        )
    elif normalized_event_type not in transition_policy["next_states"]:
        blocking_reasons.append(
            "event_type is not allowed from the current governance state"
        )
    else:
        next_state = transition_policy["next_states"][normalized_event_type]

    valid_transition = not blocking_reasons
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        "valid_transition": valid_transition,
        "current_state": normalized_state,
        "event_type": normalized_event_type,
        "next_state": next_state,
        "blocking_reasons": _deduplicate(blocking_reasons),
        "policy_version": GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
        "transition_policy": transition_policy,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def governance_transition_policy_registry_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize a transition policy result deterministically."""

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


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "ALLOWED_GOVERNANCE_STATES",
    "GOVERNANCE_STATE_MACHINE_POLICY_VERSION",
    "GOVERNANCE_TRANSITION_POLICY_REGISTRY",
    "SAFETY_BOUNDARIES",
    "TRANSITION_POLICY_REGISTRY_VERSION",
    "TRANSITION_POLICY_SCHEMA_VERSION",
    "evaluate_governance_transition",
    "get_governance_transition_policy",
    "governance_transition_policy_registry_to_json",
]
