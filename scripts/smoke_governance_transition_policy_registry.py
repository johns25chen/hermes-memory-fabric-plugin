#!/usr/bin/env python3
"""Smoke test for the local governance transition policy registry."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    ALLOWED_GOVERNANCE_STATES,
    GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
    GOVERNANCE_TRANSITION_POLICY_REGISTRY,
    SAFETY_BOUNDARIES,
    evaluate_governance_transition,
    governance_transition_policy_registry_to_json,
)


def main() -> int:
    try:
        evaluations: dict[str, object] = {}
        for state in ALLOWED_GOVERNANCE_STATES:
            event_type, expected_state = next(
                iter(GOVERNANCE_TRANSITION_POLICY_REGISTRY[state].items())
            )
            result = evaluate_governance_transition(state, event_type)
            if result["valid_transition"] is not True:
                raise AssertionError(state)
            if result["next_state"] != expected_state:
                raise AssertionError(f"{state}.next_state")
            if (
                result["policy_version"]
                != GOVERNANCE_STATE_MACHINE_POLICY_VERSION
            ):
                raise AssertionError(f"{state}.policy_version")
            for key in SAFETY_BOUNDARIES:
                if result.get(key) is not False:
                    raise AssertionError(f"{state}.{key}")
                if result["safety_boundaries"].get(key) is not False:
                    raise AssertionError(
                        f"{state}.safety_boundaries.{key}"
                    )
            evaluations[state] = result

        invalid = evaluate_governance_transition(
            "review_ready",
            "review_completed",
        )
        if invalid["valid_transition"] is not False:
            raise AssertionError("invalid_transition")
        unknown = evaluate_governance_transition(
            "unknown_state",
            "blocked",
        )
        if unknown["valid_transition"] is not False:
            raise AssertionError("unknown_state")
        evaluations["invalid_transition"] = invalid
        evaluations["unknown_state"] = unknown

        for evaluation_name, evaluation in evaluations.items():
            if not isinstance(evaluation, dict):
                raise AssertionError(f"{evaluation_name}.evaluation")
            for key in SAFETY_BOUNDARIES:
                if evaluation.get(key) is not False:
                    raise AssertionError(f"{evaluation_name}.{key}")
                if evaluation["safety_boundaries"].get(key) is not False:
                    raise AssertionError(
                        f"{evaluation_name}.safety_boundaries.{key}"
                    )

        first = governance_transition_policy_registry_to_json(evaluations)
        second = governance_transition_policy_registry_to_json(evaluations)
        if first != second:
            raise AssertionError("deterministic_json")
    except Exception as exc:
        print(
            f"governance_transition_policy_registry=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_transition_policy_registry=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
