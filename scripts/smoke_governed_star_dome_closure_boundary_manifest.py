#!/usr/bin/env python3
"""Smoke test for governed Star-Dome closure boundary manifest."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_star_dome_closure_boundary_manifest import (  # noqa: E402
    build_governed_star_dome_closure_boundary_manifest,
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
]

EXPECTED_FLAGS = {
    "status": "boundary_manifest_ready",
    "read_only": True,
    "read_only_memory": True,
    "manifest_only": True,
    "boundary_manifest_only": True,
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
}


def _valid_audit_report() -> dict[str, object]:
    return {
        "version": "2.17.0",
        "status": "chain_closure_audit_passed",
        "read_only": True,
        "read_only_memory": True,
        "audit_only": True,
        "closure_audit_only": True,
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
        "closure_authorized": False,
        "star_dome_closed": False,
        "handoff_authorized": False,
        "human_decision_recorded": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
        },
        "audited_chain_versions": EXPECTED_CHAIN[:-1],
        "next_allowed_step": "v2.18.0 Star-Dome closure boundary manifest",
        "blocking_reasons": [],
        "chain_closure_summary": {"star_dome_final_closure_claimed": False},
        "non_authorization_boundary": {
            "chain_closure_audit_passed_is_star_dome_final_closure": False,
        },
    }


def main() -> int:
    try:
        result = build_governed_star_dome_closure_boundary_manifest(_valid_audit_report())
        for key, expected in EXPECTED_FLAGS.items():
            if result.get(key) != expected:
                print(
                    f"governed_star_dome_closure_boundary_manifest=failed {key}",
                    file=sys.stderr,
                )
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星穹记忆":
            print(
                "governed_star_dome_closure_boundary_manifest=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        if result.get("manifested_chain_versions") != EXPECTED_CHAIN:
            print(
                "governed_star_dome_closure_boundary_manifest=failed manifested_chain_versions",
                file=sys.stderr,
            )
            return 1
        if result.get("next_allowed_step") != "v2.19.0 Star-Hub preflight boundary analysis":
            print(
                "governed_star_dome_closure_boundary_manifest=failed next_allowed_step",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_star_dome_closure_boundary_manifest=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_star_dome_closure_boundary_manifest=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
