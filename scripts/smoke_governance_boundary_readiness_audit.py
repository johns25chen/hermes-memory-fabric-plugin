#!/usr/bin/env python3
"""Smoke test for the governance boundary readiness audit."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_boundary_readiness_audit import (  # noqa: E402
    build_governance_boundary_readiness_audit,
    governance_boundary_readiness_audit_to_json,
    list_governance_boundary_readiness_check_names,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


EXPECTED_CHECK_NAMES = [
    "version_alignment_check",
    "validation_matrix_status_check",
    "fixture_pack_presence_check",
    "fixture_coverage_check",
    "expected_vs_observed_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
    "local_only_boundary_check",
    "no_execution_boundary_check",
    "no_durable_write_boundary_check",
    "no_external_call_boundary_check",
    "no_star_cosmos_claim_check",
    "handoff_candidate_check",
]

SENSITIVE_BLOCKED_TERMS = [
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase-4-10",
    "fixture-stdout-tail-4-10",
    "fixture-stdout-4-10",
    "fixture-raw-logs-4-10",
    "fixture-token-4-10",
    "fixture-api-key-4-10",
    "fixture-secret-4-10",
    "fixture-password-4-10",
    "fixture-credential-4-10",
]


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                if value.get(key) is not False:
                    raise AssertionError(key)
                if boundaries.get(key) is not False:
                    raise AssertionError(f"safety_boundaries.{key}")
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_no_sensitive_leak(audit: dict[str, object]) -> None:
    protected = {
        "checks": audit["readiness_checks"],
        "summary": audit["readiness_summary"],
        "hashes": {
            "audit": audit["deterministic_readiness_audit_hash"],
            "matrix": audit["validation_matrix_hash"],
        },
        "json": governance_boundary_readiness_audit_to_json(audit),
    }
    serialized = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in serialized:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_boundary_readiness_audit()
        second = build_governance_boundary_readiness_audit()

        if first["readiness_audit_status"] != "pass":
            raise AssertionError("readiness_audit_status")
        if first["readiness_stage"] != "13.5_boundary_closure":
            raise AssertionError("readiness_stage")
        if (
            first["next_stage_candidate"]
            != "v5.0_execution_adapter_boundary_candidate"
        ):
            raise AssertionError("next_stage_candidate")
        if (
            first["handoff_recommendation"]
            != "ready_for_v5_0_boundary_candidate"
        ):
            raise AssertionError("handoff_recommendation")
        if first["star_cosmos_entry_claimed"] is not False:
            raise AssertionError("star_cosmos_entry_claimed")
        if first["execution_adapter_implemented"] is not False:
            raise AssertionError("execution_adapter_implemented")
        if first["real_execution_enabled"] is not False:
            raise AssertionError("real_execution_enabled")
        if list_governance_boundary_readiness_check_names() != EXPECTED_CHECK_NAMES:
            raise AssertionError("check_names")
        if [
            check["check_name"] for check in first["readiness_checks"]
        ] != EXPECTED_CHECK_NAMES:
            raise AssertionError("readiness_checks")
        if (
            first["deterministic_readiness_audit_hash"]
            != second["deterministic_readiness_audit_hash"]
        ):
            raise AssertionError("readiness_audit_hash_stability")
        for check in first["readiness_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])

        _assert_safety(first)
        _assert_no_sensitive_leak(first)
    except Exception as exc:
        print(
            f"governance_boundary_readiness_audit=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_boundary_readiness_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
