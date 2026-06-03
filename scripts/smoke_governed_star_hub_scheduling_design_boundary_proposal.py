#!/usr/bin/env python3
"""Smoke test for governed Star-Hub scheduling design boundary proposal."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_hub_scheduling_design_boundary_proposal import (  # noqa: E402
    build_governed_star_hub_scheduling_design_boundary_proposal,
)


EXPECTED_CHAIN = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
    "v2.17.0",
    "v2.18.0",
    "v2.19.0",
]

SOURCE_CHAIN = EXPECTED_CHAIN[:-1]

EXPECTED_FLAGS = {
    "status": "star_hub_scheduling_design_boundary_proposal_ready",
    "read_only": True,
    "read_only_memory": True,
    "proposal_only": True,
    "design_boundary_proposal_only": True,
    "scheduling_design_boundary_proposal_only": True,
    "star_hub_design_boundary_only": True,
    "scheduling_performed": False,
    "would_schedule_anything": False,
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
    "design_boundary_authorized": False,
    "scheduling_design_authorized": False,
    "star_hub_scheduling_authorized": False,
    "star_hub_scheduling_executed": False,
    "star_hub_handoff_authorized": False,
    "handoff_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
    "civilization_core_complete_claimed": False,
    "star_dome_final_closure_claimed": False,
}


def _valid_preflight_report() -> dict[str, object]:
    return {
        "version": "2.19.0",
        "status": "star_hub_preflight_boundary_analysis_ready",
        "read_only": True,
        "read_only_memory": True,
        "analysis_only": True,
        "preflight_only": True,
        "boundary_analysis_only": True,
        "star_hub_preflight_only": True,
        "would_mutate_memory": False,
        "writes_files": False,
        "invokes_openclaw": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "would_write_durable_memory": False,
        "would_mutate_memory_graph": False,
        "would_create_operation_ledger_entry": False,
        "would_create_approval_request": False,
        "would_submit_approval_request": False,
        "would_execute_approval_request": False,
        "would_record_human_decision": False,
        "would_grant_approval": False,
        "authorization_granted": False,
        "preflight_analysis_authorized": False,
        "star_hub_design_authorized": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "scheduling_performed": False,
        "handoff_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "star_dome_final_closure_claimed": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星枢记忆",
            "primary_layer_status": "preflight boundary analysis only, not scheduling",
            "supporting_layers": ["星穹记忆", "星域记忆", "星界记忆", "星辰记忆"],
        },
        "analyzed_chain_versions": SOURCE_CHAIN,
        "next_allowed_step": "v2.20.0 Star-Hub scheduling design boundary proposal",
        "blocking_reasons": [],
        "non_authorization_boundary": {
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_scheduling": False,
            "star_hub_preflight_boundary_analysis_ready_is_star_hub_handoff": False,
            "star_hub_preflight_boundary_analysis_ready_is_authorization": False,
            "star_hub_preflight_boundary_analysis_ready_is_civilization_core_completion": False,
        },
    }


def main() -> int:
    try:
        result = build_governed_star_hub_scheduling_design_boundary_proposal(
            _valid_preflight_report()
        )
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_hub_scheduling_design_boundary_proposal=failed {key}",
                    file=sys.stderr,
                )
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星枢记忆":
            print(
                "governed_star_hub_scheduling_design_boundary_proposal=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if (
            layer_mapping.get("primary_layer_status")
            != "scheduling design boundary proposal only, not scheduling"
        ):
            print(
                "governed_star_hub_scheduling_design_boundary_proposal=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("proposed_chain_versions") != EXPECTED_CHAIN:
            print(
                "governed_star_hub_scheduling_design_boundary_proposal=failed proposed_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != (
            "v2.21.0 Star-Hub scheduling design boundary review gate"
        ):
            print(
                "governed_star_hub_scheduling_design_boundary_proposal=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_hub_scheduling_design_boundary_proposal=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_hub_scheduling_design_boundary_proposal=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
