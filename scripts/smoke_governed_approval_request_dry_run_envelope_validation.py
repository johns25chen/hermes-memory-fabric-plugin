#!/usr/bin/env python3
"""Smoke test for governed approval request dry-run envelope validation."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_approval_request_dry_run_envelope_validation import (  # noqa: E402
    build_governed_approval_request_dry_run_envelope_validation,
)


def _valid_envelope_report() -> dict[str, object]:
    return {
        "version": "2.13.0",
        "status": "envelope_ready",
        "read_only": True,
        "read_only_memory": True,
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
            "direction": "星穹 approval request 准备材料 -> 星穹 dry-run envelope",
        },
        "candidate_ids_in_envelope": ["star-dome-validation-smoke-candidate"],
        "blocked_candidate_ids": [],
        "dry_run_envelope": {
            "envelope_status": "dry_run_prepared_for_human_operator_only",
            "is_real_approval_request": False,
            "is_submittable": False,
            "candidate_ids": ["star-dome-validation-smoke-candidate"],
            "source_preparation_version": "2.12.0",
            "envelope_type": "approval_request_dry_run",
        },
    }


EXPECTED_RESULT = {
    "status": "validation_ready",
    "read_only": True,
    "read_only_memory": True,
    "validation_only": True,
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
    "validation_authorized": False,
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
        result = build_governed_approval_request_dry_run_envelope_validation(
            _valid_envelope_report()
        )
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(
                    f"governed_approval_request_dry_run_envelope_validation=failed {key}",
                    file=sys.stderr,
                )
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星穹记忆":
            print(
                "governed_approval_request_dry_run_envelope_validation=failed primary_layer",
                file=sys.stderr,
            )
            return 1
        summary = result.get("validated_dry_run_envelope_summary", {})
        if summary.get("is_real_approval_request") is not False:
            print(
                "governed_approval_request_dry_run_envelope_validation=failed real_request",
                file=sys.stderr,
            )
            return 1
        if summary.get("is_submittable") is not False:
            print(
                "governed_approval_request_dry_run_envelope_validation=failed submittable",
                file=sys.stderr,
            )
            return 1
        if summary.get("is_executable") is not False:
            print(
                "governed_approval_request_dry_run_envelope_validation=failed executable",
                file=sys.stderr,
            )
            return 1
        if not result.get("candidate_ids_validated"):
            print(
                "governed_approval_request_dry_run_envelope_validation=failed candidate_ids",
                file=sys.stderr,
            )
            return 1
    except Exception as exc:
        print(
            f"governed_approval_request_dry_run_envelope_validation=failed {type(exc).__name__}",
            file=sys.stderr,
        )
        return 1

    print("governed_approval_request_dry_run_envelope_validation=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
