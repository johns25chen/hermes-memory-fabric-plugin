#!/usr/bin/env python3
"""Smoke test for governed Star-Hub preflight boundary analysis."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_hub_preflight_boundary_analysis import (  # noqa: E402
    build_governed_star_hub_preflight_boundary_analysis,
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
]

EXPECTED_FLAGS = {
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
    "closure_authorized": False,
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


def _valid_manifest_report() -> dict[str, object]:
    return {
        "version": "2.18.0",
        "status": "boundary_manifest_ready",
        "read_only": True,
        "read_only_memory": True,
        "manifest_only": True,
        "boundary_manifest_only": True,
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
        "boundary_manifest_authorized": False,
        "star_dome_stage_boundary_manifested": True,
        "star_dome_final_closure_claimed": False,
        "star_hub_handoff_authorized": False,
        "star_hub_scheduling_authorized": False,
        "handoff_authorized": False,
        "closure_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_complete_claimed": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
        },
        "manifested_chain_versions": EXPECTED_CHAIN[:-1],
        "next_allowed_step": "v2.19.0 Star-Hub preflight boundary analysis",
        "blocking_reasons": [],
        "star_dome_stage_closure_statement": {
            "statement_status": "star_dome_stage_boundary_manifested_for_human_review_only",
            "star_dome_governance_chain_stage_ready_for_closure": True,
            "star_dome_final_closure_claimed": False,
            "civilization_core_complete_claimed": False,
            "star_hub_handoff_authorized": False,
            "star_hub_scheduling_authorized": False,
            "durable_memory_write_authorized": False,
            "memory_graph_mutation_authorized": False,
            "operation_ledger_creation_authorized": False,
            "openclaw_execution_authorized": False,
            "approval_authorized": False,
            "real_human_decision_recorded": False,
        },
        "non_authorization_boundary": {
            "boundary_manifest_ready_is_star_hub_scheduling_permission": False,
            "boundary_manifest_ready_is_star_hub_handoff_permission": False,
            "boundary_manifest_ready_is_civilization_core_completion": False,
        },
    }


def main() -> int:
    try:
        result = build_governed_star_hub_preflight_boundary_analysis(
            _valid_manifest_report()
        )
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_hub_preflight_boundary_analysis=failed {key}",
                    file=sys.stderr,
                )
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星枢记忆":
            print(
                "governed_star_hub_preflight_boundary_analysis=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if (
            layer_mapping.get("primary_layer_status")
            != "preflight boundary analysis only, not scheduling"
        ):
            print(
                "governed_star_hub_preflight_boundary_analysis=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("analyzed_chain_versions") != EXPECTED_CHAIN:
            print(
                "governed_star_hub_preflight_boundary_analysis=failed analyzed_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != (
            "v2.20.0 Star-Hub scheduling design boundary proposal"
        ):
            print(
                "governed_star_hub_preflight_boundary_analysis=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_hub_preflight_boundary_analysis=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_hub_preflight_boundary_analysis=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
