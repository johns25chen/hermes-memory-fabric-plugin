#!/usr/bin/env python3
"""Smoke test for governed Star-Hub chain closure audit."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_hub_chain_closure_audit import (  # noqa: E402
    build_governed_star_hub_chain_closure_audit,
)
from hermes_memory_fabric.governed_star_hub_scheduling_dry_run_execution_boundary_review_gate import (  # noqa: E402
    build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate,
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
]

EXPECTED_STAR_HUB_CHAIN = [
    "v2.19.0",
    "v2.20.0",
    "v2.21.0",
    "v2.22.0",
    "v2.23.0",
    "v2.24.0",
    "v2.25.0",
]

EXPECTED_FLAGS = {
    "status": "star_hub_chain_closure_audit_ready",
    "read_only": True,
    "read_only_memory": True,
    "audit_only": True,
    "chain_closure_audit_only": True,
    "star_hub_chain_closure_audit_only": True,
    "closure_manifest_created": False,
    "star_hub_final_closure_claimed": False,
    "star_hub_closure_claimed": False,
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
    "dry_run_execution_boundary_review_authorized": False,
    "dry_run_execution_boundary_authorized": False,
    "dry_run_execution_authorized": False,
    "scheduling_dry_run_authorized": False,
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


def main() -> int:
    try:
        review_gate_report = (
            build_governed_star_hub_scheduling_dry_run_execution_boundary_review_gate(
                _valid_proposal_report()
            )
        )
        result = build_governed_star_hub_chain_closure_audit(review_gate_report)
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_hub_chain_closure_audit=failed {key}",
                    file=sys.stderr,
                )
                return 1
        mapping = result.get("civilization_core_layer_mapping", {})
        if mapping.get("primary_layer") != "星枢记忆":
            print(
                "governed_star_hub_chain_closure_audit=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if mapping.get("primary_layer_status") != (
            "Star-Hub chain closure audit only, not final closure and not handoff"
        ):
            print(
                "governed_star_hub_chain_closure_audit=failed primary_layer_status",
                file=sys.stderr,
            )
            return 1
        if result.get("audited_chain_versions") != EXPECTED_CHAIN:
            print(
                "governed_star_hub_chain_closure_audit=failed audited_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("audited_star_hub_chain_versions") != EXPECTED_STAR_HUB_CHAIN:
            print(
                "governed_star_hub_chain_closure_audit=failed audited_star_hub_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != "v2.27.0 Star-Hub closure boundary manifest":
            print(
                "governed_star_hub_chain_closure_audit=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_hub_chain_closure_audit=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_hub_chain_closure_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
