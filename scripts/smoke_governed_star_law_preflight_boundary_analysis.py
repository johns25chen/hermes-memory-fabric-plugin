#!/usr/bin/env python3
"""Smoke test for governed Star-Law preflight boundary analysis."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_hub_chain_closure_audit import (  # noqa: E402
    build_governed_star_hub_chain_closure_audit,
)
from hermes_memory_fabric.governed_star_hub_closure_boundary_manifest import (  # noqa: E402
    build_governed_star_hub_closure_boundary_manifest,
)
from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (  # noqa: E402
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_law_preflight_boundary_analysis import (  # noqa: E402
    build_governed_star_law_preflight_boundary_analysis,
)
from smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (  # noqa: E402
    _valid_proposal_report,
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
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
    "v2.27.0",
]

EXPECTED_STAR_HUB_CHAIN = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
    "v2.26.0",
    "v2.27.0",
]

EXPECTED_FLAGS = {
    "status": "star_law_preflight_boundary_analysis_ready",
    "read_only": True,
    "read_only_memory": True,
    "preflight_analysis_only": True,
    "star_law_preflight_boundary_analysis_only": True,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
    "star_law_rules_activated": False,
    "star_law_rules_enforced": False,
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


def main() -> int:
    try:
        review_gate_report = (
            build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
                _valid_proposal_report()
            )
        )
        audit_report = build_governed_star_hub_chain_closure_audit(review_gate_report)
        manifest_report = build_governed_star_hub_closure_boundary_manifest(audit_report)
        result = build_governed_star_law_preflight_boundary_analysis(
            manifest_report
        )
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_law_preflight_boundary_analysis=failed {key}",
                    file=sys.stderr,
                )
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if mapping.get("primary_layer") != "星律记忆":
            print(
                "governed_star_law_preflight_boundary_analysis=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("source_layer") != "星枢记忆":
            print(
                "governed_star_law_preflight_boundary_analysis=failed source_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer_status") != (
            "Star-Law preflight boundary analysis only, not self-enforcing law and not autonomous execution"
        ):
            print(
                "governed_star_law_preflight_boundary_analysis=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("analyzed_chain_versions") != EXPECTED_CHAIN:
            print(
                "governed_star_law_preflight_boundary_analysis=failed analyzed_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("analyzed_star_hub_chain_versions") != EXPECTED_STAR_HUB_CHAIN:
            print(
                "governed_star_law_preflight_boundary_analysis=failed analyzed_star_hub_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != "v2.29.0 Star-Law design boundary proposal":
            print(
                "governed_star_law_preflight_boundary_analysis=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_law_preflight_boundary_analysis=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_law_preflight_boundary_analysis=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
