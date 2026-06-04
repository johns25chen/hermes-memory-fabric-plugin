#!/usr/bin/env python3
"""Smoke test for governed Star-Law design boundary review gate."""

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
from hermes_memory_fabric.governed_star_law_design_boundary_proposal import (  # noqa: E402
    build_governed_star_law_design_boundary_proposal,
)
from hermes_memory_fabric.governed_star_law_design_boundary_review_gate import (  # noqa: E402
    REVIEWED_CHAIN_VERSIONS,
    REVIEWED_STAR_HUB_CHAIN_VERSIONS,
    build_governed_star_law_design_boundary_review_gate,
)
from hermes_memory_fabric.governed_star_law_preflight_boundary_analysis import (  # noqa: E402
    build_governed_star_law_preflight_boundary_analysis,
)
from smoke_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (  # noqa: E402
    _valid_proposal_report,
)


EXPECTED_FLAGS = {
    "status": "star_law_design_boundary_review_gate_ready",
    "read_only": True,
    "read_only_memory": True,
    "review_gate_only": True,
    "design_boundary_review_gate_only": True,
    "star_law_design_boundary_review_gate_only": True,
    "star_law_design_boundary_review_ready": True,
    "star_law_candidate_rule_set_boundary_proposal_ready_for_human_review_only": True,
    "star_law_self_enforcing_law_created": False,
    "star_law_self_enforcing_law_active": False,
    "star_law_rules_created": False,
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


def _valid_design_proposal_report() -> dict[str, object]:
    review_gate_report = (
        build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
            _valid_proposal_report()
        )
    )
    audit_report = build_governed_star_hub_chain_closure_audit(review_gate_report)
    manifest_report = build_governed_star_hub_closure_boundary_manifest(audit_report)
    preflight_report = build_governed_star_law_preflight_boundary_analysis(
        manifest_report
    )
    return build_governed_star_law_design_boundary_proposal(preflight_report)


def main() -> int:
    try:
        result = build_governed_star_law_design_boundary_review_gate(
            _valid_design_proposal_report()
        )
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_law_design_boundary_review_gate=failed {key}",
                    file=sys.stderr,
                )
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if not isinstance(mapping, dict):
            print(
                "governed_star_law_design_boundary_review_gate=failed layer_mapping",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer") != "星律记忆":
            print(
                "governed_star_law_design_boundary_review_gate=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("source_layer") != "星律记忆":
            print(
                "governed_star_law_design_boundary_review_gate=failed source_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer_status") != (
            "Star-Law design boundary review gate only, not rule activation and not rule enforcement"
        ):
            print(
                "governed_star_law_design_boundary_review_gate=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("reviewed_chain_versions") != REVIEWED_CHAIN_VERSIONS:
            print(
                "governed_star_law_design_boundary_review_gate=failed reviewed_chain_versions",
                file=sys.stderr,
            )
            return 1
        if (
            result.get("reviewed_star_hub_chain_versions")
            != REVIEWED_STAR_HUB_CHAIN_VERSIONS
        ):
            print(
                "governed_star_law_design_boundary_review_gate=failed reviewed_star_hub_chain_versions",
                file=sys.stderr,
            )
            return 1
        if (
            result.get("next_allowed_step")
            != "v2.31.0 Star-Law candidate rule-set boundary proposal"
        ):
            print(
                "governed_star_law_design_boundary_review_gate=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_law_design_boundary_review_gate=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_law_design_boundary_review_gate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
