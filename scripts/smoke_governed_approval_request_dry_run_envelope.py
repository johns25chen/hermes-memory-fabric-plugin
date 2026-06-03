#!/usr/bin/env python3
"""Smoke test for governed approval request dry-run envelope."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_approval_request_dry_run_envelope import (  # noqa: E402
    build_governed_approval_request_dry_run_envelope,
)


def _valid_preparation_report() -> dict[str, object]:
    return {
        "version": "2.12.0",
        "status": "preparation_ready",
        "read_only": True,
        "read_only_memory": True,
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
        "authorization_granted": False,
        "preparation_authorized": False,
        "approval_request_created": False,
        "approval_request_authorized": False,
        "approval_granted": False,
        "memory_write_authorized": False,
        "openclaw_execution_authorized": False,
        "civilization_core_layer_mapping": {
            "primary_layer": "星穹记忆",
            "supporting_layers": ["星辰记忆", "星域记忆", "星界记忆"],
            "direction": "星穹治理评审闸门 -> 受治理 approval request 准备",
        },
        "candidate_ids_for_human_review": ["star-dome-envelope-smoke-candidate"],
        "blocked_candidate_ids": [],
        "approval_request_draft_material": {
            "draft_status": "prepared_for_human_operator_only",
            "is_real_approval_request": False,
            "candidate_ids": ["star-dome-envelope-smoke-candidate"],
        },
    }


EXPECTED_RESULT = {
    "status": "envelope_ready",
    "read_only": True,
    "read_only_memory": True,
    "dry_run_only": True,
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
    "authorization_granted": False,
    "envelope_authorized": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}


def main() -> int:
    try:
        result = build_governed_approval_request_dry_run_envelope(_valid_preparation_report())
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(f"governed_approval_request_dry_run_envelope=failed {key}", file=sys.stderr)
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星穹记忆":
            print("governed_approval_request_dry_run_envelope=failed primary_layer", file=sys.stderr)
            return 1
        envelope = result.get("dry_run_envelope", {})
        if envelope.get("is_real_approval_request") is not False:
            print("governed_approval_request_dry_run_envelope=failed real_request", file=sys.stderr)
            return 1
        if envelope.get("is_submittable") is not False:
            print("governed_approval_request_dry_run_envelope=failed submittable", file=sys.stderr)
            return 1
        if not result.get("candidate_ids_in_envelope"):
            print("governed_approval_request_dry_run_envelope=failed candidate_ids", file=sys.stderr)
            return 1
    except Exception as exc:
        print(
            f"governed_approval_request_dry_run_envelope=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_approval_request_dry_run_envelope=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
