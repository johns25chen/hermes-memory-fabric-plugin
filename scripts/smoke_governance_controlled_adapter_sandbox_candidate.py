#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_controlled_adapter_sandbox_candidate import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES,
    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_controlled_adapter_sandbox_candidate,
    governance_controlled_adapter_sandbox_candidate_to_json,
    list_governance_controlled_adapter_sandbox_candidate_check_names,
    list_governance_controlled_adapter_sandbox_candidate_contract_names,
    list_governance_controlled_adapter_sandbox_candidate_section_names,
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
    '"operation_ledger_entry_payload"',
    '"sandbox_runtime_payload"',
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
        first = build_governance_controlled_adapter_sandbox_candidate()
        second = build_governance_controlled_adapter_sandbox_candidate()
        if first != second:
            raise AssertionError("candidate changed between builds")

        expected_top_level = {
            "controlled_adapter_sandbox_candidate_status": "pass",
            "controlled_adapter_sandbox_candidate_stage": (
                "v5.11_controlled_adapter_sandbox_candidate"
            ),
            "controlled_adapter_sandbox_candidate_mode": (
                "controlled_adapter_sandbox_candidate_only"
            ),
            "controlled_adapter_sandbox_mode": "metadata_only",
            "controlled_adapter_sandbox_status": "not_started",
            "adapter_sandbox_entry_status": "not_entered",
            "sandbox_execution_status": "not_enabled",
            "sandbox_runtime_status": "not_started",
            "sandbox_scope_status": "candidate_scope_only",
            "sandbox_policy_status": "metadata_only",
            "future_post_sandbox_review_status": "not_entered",
            "star_cosmos_entry_status": "candidate_only",
            "cross_system_coordination_boundary_status": "pass",
        }
        for key, expected in expected_top_level.items():
            if first[key] != expected:
                raise AssertionError(key)

        metadata = first["controlled_adapter_sandbox_candidate_metadata"]
        if metadata["sandbox_candidate_metadata_mode"] != "metadata_only":
            raise AssertionError("sandbox_candidate_metadata_mode")
        if metadata["sandbox_candidate_metadata_available"] is not True:
            raise AssertionError("sandbox_candidate_metadata_available")
        if metadata["sandbox_candidate_declared"] is not True:
            raise AssertionError("sandbox_candidate_declared")

        if list_governance_controlled_adapter_sandbox_candidate_section_names() != list(
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_controlled_adapter_sandbox_candidate_contract_names() != list(
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_controlled_adapter_sandbox_candidate_check_names() != list(
            REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if any(
            section["section_status"] != "pass"
            for section in first["controlled_adapter_sandbox_candidate_sections"]
        ):
            raise AssertionError("section status")
        if any(
            contract["contract_status"] != "pass"
            for contract in first["controlled_adapter_sandbox_candidate_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            check["check_status"] != "pass"
            for check in first["controlled_adapter_sandbox_candidate_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first[
            "deterministic_controlled_adapter_sandbox_candidate_hash"
        ]
        second_hash = second[
            "deterministic_controlled_adapter_sandbox_candidate_hash"
        ]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "sections": first[
                    "controlled_adapter_sandbox_candidate_sections"
                ],
                "contracts": first[
                    "controlled_adapter_sandbox_candidate_contracts"
                ],
                "checks": first[
                    "controlled_adapter_sandbox_candidate_checks"
                ],
                "summary": first[
                    "controlled_adapter_sandbox_candidate_summary"
                ],
                "hash": first_hash,
                "json": governance_controlled_adapter_sandbox_candidate_to_json(
                    first
                ),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_controlled_adapter_sandbox_candidate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
