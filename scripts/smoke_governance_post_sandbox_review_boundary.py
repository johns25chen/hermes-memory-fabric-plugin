#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_post_sandbox_review_boundary import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_post_sandbox_review_boundary,
    governance_post_sandbox_review_boundary_to_json,
    list_governance_post_sandbox_review_boundary_check_names,
    list_governance_post_sandbox_review_boundary_contract_names,
    list_governance_post_sandbox_review_boundary_section_names,
)


SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    '"sandbox_runtime_payload"',
    '"sandbox_result_payload"',
    '"rollback_payload"',
    '"quarantine_payload"',
    '"incident_payload"',
    '"audit_log_payload"',
    '"operation_ledger_entry_payload"',
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call_instruction",
    "shell_" + "command",
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
    "git " + "push",
    "g" + "h api",
)


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_DISABLED_FLAGS:
            if key in value and value[key] is not False:
                raise AssertionError(key)
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                if value.get(key) is not False:
                    raise AssertionError(key)
                if boundaries.get(key) is not False:
                    raise AssertionError(key)
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_no_sensitive_leak(value: object) -> None:
    lowered = json.dumps(value, sort_keys=True).lower()
    for blocked in SENSITIVE_BLOCKED_TERMS:
        candidate = blocked if blocked.startswith("/") else blocked.lower()
        if candidate in lowered:
            raise AssertionError(blocked)


def main() -> int:
    try:
        first = build_governance_post_sandbox_review_boundary()
        second = build_governance_post_sandbox_review_boundary()
        if first != second:
            raise AssertionError("boundary changed between builds")

        expected_top_level = {
            "version": "6.9.0",
            "schema_version": "6.9.0",
            "post_sandbox_review_boundary_status": "pass",
            "post_sandbox_review_boundary_stage": (
                "v5.12_post_sandbox_review_boundary"
            ),
            "post_sandbox_review_boundary_mode": (
                "post_sandbox_review_boundary_only"
            ),
            "post_sandbox_review_mode": "metadata_only",
            "post_sandbox_review_status": "not_started",
            "sandbox_result_status": "not_available",
            "sandbox_review_status": "not_performed",
            "rollback_status": "not_triggered",
            "quarantine_status": "not_triggered",
            "incident_status": "not_triggered",
            "audit_evidence_status": "metadata_only",
            "failure_handling_status": "metadata_only",
            "layer_14_closure_readiness_status": "candidate_only",
            "star_cosmos_entry_status": "candidate_only",
            "controlled_adapter_sandbox_candidate_version": "6.9.0",
            "controlled_adapter_sandbox_candidate_status": "pass",
            "handoff_status": (
                "ready_for_star_cosmos_closure_handoff_audit_design"
            ),
        }
        for key, expected in expected_top_level.items():
            if first[key] != expected:
                raise AssertionError(key)

        metadata = first["post_sandbox_review_metadata"]
        if (
            metadata["post_sandbox_review_metadata_type"]
            != "future_post_sandbox_review_boundary_metadata"
        ):
            raise AssertionError("post_sandbox_review_metadata_type")
        if metadata["post_sandbox_review_metadata_mode"] != "metadata_only":
            raise AssertionError("post_sandbox_review_metadata_mode")
        if metadata["post_sandbox_review_metadata_available"] is not True:
            raise AssertionError("post_sandbox_review_metadata_available")
        if metadata["post_sandbox_review_declared"] is not True:
            raise AssertionError("post_sandbox_review_declared")

        if list_governance_post_sandbox_review_boundary_section_names() != list(
            REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_post_sandbox_review_boundary_contract_names() != list(
            REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_post_sandbox_review_boundary_check_names() != list(
            REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if any(
            section["section_status"] != "pass"
            for section in first["post_sandbox_review_sections"]
        ):
            raise AssertionError("section status")
        if any(
            contract["contract_status"] != "pass"
            for contract in first["post_sandbox_review_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            check["check_status"] != "pass"
            for check in first["post_sandbox_review_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first["deterministic_post_sandbox_review_boundary_hash"]
        second_hash = second["deterministic_post_sandbox_review_boundary_hash"]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if len(first["controlled_adapter_sandbox_candidate_hash"]) != 64:
            raise AssertionError("controlled adapter sandbox candidate hash")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "sections": first["post_sandbox_review_sections"],
                "contracts": first["post_sandbox_review_contracts"],
                "checks": first["post_sandbox_review_checks"],
                "summary": first["post_sandbox_review_summary"],
                "hash": first_hash,
                "json": governance_post_sandbox_review_boundary_to_json(first),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_post_sandbox_review_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
