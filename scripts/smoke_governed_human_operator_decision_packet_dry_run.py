#!/usr/bin/env python3
"""Smoke test for governed Human Operator decision packet dry-run."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_human_operator_decision_packet_dry_run import (  # noqa: E402
    build_governed_human_operator_decision_packet_dry_run,
)


def _valid_validation_report() -> dict[str, object]:
    return {
        "version": "2.14.0",
        "status": "validation_ready",
        "read_only": True,
        "read_only_memory": True,
        "validation_only": True,
        "dry_run_only": True,
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
        "authorization_granted": False,
        "validation_authorized": False,
        "envelope_authorized": False,
        "approval_request_created": False,
        "approval_request_submitted": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
            "direction": "星穹 dry-run envelope -> 星穹 dry-run envelope validation gate",
        },
        "candidate_ids_validated": ["star-dome-decision-packet-smoke-candidate"],
        "blocked_candidate_ids": [],
        "validated_dry_run_envelope_summary": {
            "validation_status": "dry_run_envelope_validated_for_human_review_only",
            "is_real_approval_request": False,
            "is_submittable": False,
            "is_executable": False,
            "candidate_ids": ["star-dome-decision-packet-smoke-candidate"],
            "source_envelope_version": "2.13.0",
            "source_preparation_version": "2.12.0",
            "envelope_type": "approval_request_dry_run",
        },
    }


EXPECTED_RESULT = {
    "status": "decision_packet_ready",
    "read_only": True,
    "read_only_memory": True,
    "dry_run_only": True,
    "decision_packet_only": True,
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
    "decision_packet_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}


def main() -> int:
    try:
        result = build_governed_human_operator_decision_packet_dry_run(
            _valid_validation_report()
        )
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(
                    f"governed_human_operator_decision_packet_dry_run=failed {key}",
                    file=sys.stderr,
                )
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星穹记忆":
            print(
                "governed_human_operator_decision_packet_dry_run=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        packet = result.get("human_operator_decision_packet", {})
        for key in ("is_real_human_decision", "is_approval", "is_submittable", "is_executable"):
            if packet.get(key) is not False:
                print(
                    f"governed_human_operator_decision_packet_dry_run=failed {key}",
                    file=sys.stderr,
                )
                return 1
        if not result.get("candidate_ids_for_decision_review"):
            print(
                "governed_human_operator_decision_packet_dry_run=failed candidate_ids",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_human_operator_decision_packet_dry_run=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_human_operator_decision_packet_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
