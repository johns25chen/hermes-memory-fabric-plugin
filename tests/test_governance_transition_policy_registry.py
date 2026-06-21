from __future__ import annotations

import ast
from copy import deepcopy
import json
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_transition_policy_registry import (
    ALLOWED_GOVERNANCE_STATES,
    GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
    GOVERNANCE_TRANSITION_POLICY_REGISTRY,
    SAFETY_BOUNDARIES,
    TRANSITION_POLICY_REGISTRY_VERSION,
    TRANSITION_POLICY_SCHEMA_VERSION,
    evaluate_governance_transition,
    get_governance_transition_policy,
    governance_transition_policy_registry_to_json,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "governance_transition_policy_registry.py"
)

EXPECTED_TRANSITIONS = {
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


def test_public_versions_and_expected_states():
    assert TRANSITION_POLICY_REGISTRY_VERSION == "6.1.0"
    assert TRANSITION_POLICY_SCHEMA_VERSION == "6.1.0"
    assert GOVERNANCE_STATE_MACHINE_POLICY_VERSION == "6.1.0"
    assert tuple(EXPECTED_TRANSITIONS) == ALLOWED_GOVERNANCE_STATES
    assert GOVERNANCE_TRANSITION_POLICY_REGISTRY == EXPECTED_TRANSITIONS


@pytest.mark.parametrize("state", ALLOWED_GOVERNANCE_STATES)
def test_every_policy_mapping_is_deterministic(state: str):
    first = get_governance_transition_policy(state)
    second = get_governance_transition_policy(state)

    assert first == second
    assert first["allowed_events"] == list(EXPECTED_TRANSITIONS[state])
    assert first["next_states"] == EXPECTED_TRANSITIONS[state]


@pytest.mark.parametrize(
    ("state", "event_type", "expected_state"),
    [
        (state, event_type, next_state)
        for state, transitions in EXPECTED_TRANSITIONS.items()
        for event_type, next_state in transitions.items()
    ],
)
def test_valid_transitions_return_expected_next_state(
    state: str,
    event_type: str,
    expected_state: str,
):
    result = evaluate_governance_transition(state, event_type)

    assert result["valid_transition"] is True
    assert result["current_state"] == state
    assert result["event_type"] == event_type
    assert result["next_state"] == expected_state
    assert result["blocking_reasons"] == []
    assert result["policy_version"] == "6.1.0"


def test_unknown_state_is_rejected_with_empty_blocked_policy():
    result = evaluate_governance_transition("unknown", "blocked")

    assert result["valid_transition"] is False
    assert result["next_state"] == "blocked"
    assert result["transition_policy"]["policy_status"] == "blocked"
    assert result["transition_policy"]["allowed_events"] == []
    assert result["transition_policy"]["next_states"] == {}


def test_unknown_event_type_is_rejected():
    result = evaluate_governance_transition("initialized", "unknown")

    assert result["valid_transition"] is False
    assert result["next_state"] == "blocked"
    assert (
        "event_type is not a recognized governance event type"
        in result["blocking_reasons"]
    )


def test_invalid_transition_is_rejected():
    result = evaluate_governance_transition(
        "review_ready",
        "review_completed",
    )

    assert result["valid_transition"] is False
    assert result["next_state"] == "blocked"
    assert (
        "event_type is not allowed from the current governance state"
        in result["blocking_reasons"]
    )


@pytest.mark.parametrize("state", ALLOWED_GOVERNANCE_STATES)
def test_blocked_event_maps_to_blocked_for_every_state(state: str):
    result = evaluate_governance_transition(state, "blocked")

    assert result["valid_transition"] is True
    assert result["next_state"] == "blocked"


def test_get_policy_returns_detached_copies():
    registry_before = deepcopy(GOVERNANCE_TRANSITION_POLICY_REGISTRY)
    first = get_governance_transition_policy("initialized")
    first["allowed_events"].append("mutated")
    first["next_states"]["mutated"] = "blocked"

    second = get_governance_transition_policy("initialized")

    assert second["allowed_events"] == list(EXPECTED_TRANSITIONS["initialized"])
    assert second["next_states"] == EXPECTED_TRANSITIONS["initialized"]
    assert GOVERNANCE_TRANSITION_POLICY_REGISTRY == registry_before


def test_json_serialization_is_deterministic():
    result = evaluate_governance_transition(
        "initialized",
        "governance_kernel_initialized",
    )

    first = governance_transition_policy_registry_to_json(result)
    second = governance_transition_policy_registry_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["valid_transition"] is True


def test_all_safety_fields_remain_false():
    result = evaluate_governance_transition(
        "initialized",
        "governance_kernel_initialized",
    )

    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False


def test_registry_module_has_no_external_or_write_surfaces():
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
