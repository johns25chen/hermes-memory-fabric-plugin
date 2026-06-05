#!/usr/bin/env python3
"""Smoke test for governed Star-Law candidate rule violation observation boundary proposal."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_law_candidate_rule_enforcement_boundary_review_gate import (  # noqa: E402
    build_governed_star_law_candidate_rule_enforcement_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_law_candidate_rule_violation_observation_boundary_proposal import (  # noqa: E402
    PROPOSED_CHAIN_VERSIONS,
    PROPOSED_STAR_HUB_CHAIN_VERSIONS,
    READY_NEXT_ALLOWED_STEP,
    build_governed_star_law_candidate_rule_violation_observation_boundary_proposal,
)
from smoke_governed_star_law_candidate_rule_enforcement_boundary_review_gate import (  # noqa: E402
    _valid_candidate_rule_enforcement_boundary_proposal_report,
)


EXPECTED_FLAGS = {
    "status": "star_law_candidate_rule_violation_observation_boundary_proposal_ready",
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "candidate_rule_violation_observation_boundary_proposal_only": True,
    "star_law_candidate_rule_violation_observation_boundary_proposal_only": True,
    "candidate_rule_violation_observation_boundary_proposed_for_human_review_only": True,
    "candidate_rule_violation_observation_boundary_review_gate_ready_for_human_review_only": True,
    "candidate_rule_violation_observation_performed": False,
    "candidate_rule_violation_observation_authorized": False,
    "candidate_rule_violation_detected": False,
    "candidate_rule_violation_recorded": False,
    "candidate_rule_violation_enforced": False,
    "candidate_rule_violation_ledger_entry_created": False,
    "candidate_rule_enforcement_performed": False,
    "candidate_rule_enforcement_authorized": False,
    "candidate_rule_activation_performed": False,
    "candidate_rule_activation_authorized": False,
    "star_law_candidate_rules_created": False,
    "star_law_candidate_rules_activated": False,
    "star_law_candidate_rules_enforced": False,
    "star_law_rules_created": False,
    "star_law_rules_activated": False,
    "star_law_rules_enforced": False,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
    "autonomous_governance_created": False,
    "autonomous_execution_authorized": False,
    "self_executing_policy_created": False,
    "self_executing_policy_active": False,
    "enters_star_law_layer": False,
    "mature_star_law_claimed": False,
    "enters_star_soul_layer": False,
    "enters_star_cosmos_layer": False,
    "enters_star_source_layer": False,
    "civilization_core_complete_claimed": False,
    "handoff_authorized": False,
    "star_hub_handoff_authorized": False,
    "handoff_performed": False,
    "dry_run_performed": False,
    "dry_run_executed": False,
    "scheduling_performed": False,
    "would_schedule_anything": False,
    "would_execute_dry_run": False,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "would_create_approval_request": False,
    "would_submit_approval_request": False,
    "would_execute_approval_request": False,
    "would_record_human_decision": False,
    "would_grant_approval": False,
    "authorization_granted": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "human_decision_recorded": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "star_dome_final_closure_claimed": False,
}


def _valid_candidate_rule_enforcement_boundary_review_gate_report() -> dict[str, object]:
    return build_governed_star_law_candidate_rule_enforcement_boundary_review_gate(
        _valid_candidate_rule_enforcement_boundary_proposal_report()
    )


def main() -> int:
    try:
        result = (
            build_governed_star_law_candidate_rule_violation_observation_boundary_proposal(
                _valid_candidate_rule_enforcement_boundary_review_gate_report()
            )
        )
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed {key}",
                    file=sys.stderr,
                )
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if not isinstance(mapping, dict):
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed layer_mapping",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer") != "星律记忆":
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("source_layer") != "星律记忆":
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed source_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer_status") != (
            "Star-Law candidate rule violation observation boundary proposal only, not violation observation execution, not violation enforcement, and not autonomous execution"
        ):
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("proposed_chain_versions") != PROPOSED_CHAIN_VERSIONS:
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed proposed_chain_versions",
                file=sys.stderr,
            )
            return 1
        if (
            result.get("proposed_star_hub_chain_versions")
            != PROPOSED_STAR_HUB_CHAIN_VERSIONS
        ):
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed proposed_star_hub_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != READY_NEXT_ALLOWED_STEP:
            print(
                "governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_law_candidate_rule_violation_observation_boundary_proposal=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_law_candidate_rule_violation_observation_boundary_proposal=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
