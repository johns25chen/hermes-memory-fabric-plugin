#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_cross_system_coordination_boundary import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_cross_system_coordination_boundary,
    governance_cross_system_coordination_boundary_to_json,
    list_governance_cross_system_coordination_boundary_check_names,
    list_governance_cross_system_coordination_boundary_contract_names,
    list_governance_cross_system_coordination_boundary_section_names,
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
        first = build_governance_cross_system_coordination_boundary()
        second = build_governance_cross_system_coordination_boundary()
        if first != second:
            raise AssertionError("coordination boundary changed between builds")

        expected_top_level = {
            "cross_system_coordination_boundary_status": "pass",
            "cross_system_coordination_boundary_stage": (
                "v5.10_cross_system_coordination_boundary"
            ),
            "cross_system_coordination_boundary_mode": (
                "cross_system_coordination_boundary_only"
            ),
            "cross_system_coordination_mode": "metadata_only",
            "cross_system_coordination_status": "not_started",
            "hermes_coordination_status": "not_connected",
            "codex_coordination_status": "not_connected",
            "openclaw_coordination_status": "not_connected",
            "github_coordination_status": "not_connected",
            "tool_routing_status": "not_configured",
            "command_routing_status": "not_configured",
            "system_handoff_status": "not_handed_off",
            "future_controlled_adapter_sandbox_status": "not_entered",
            "star_cosmos_entry_status": "candidate_only",
            "operation_ledger_proposal_boundary_status": "pass",
        }
        for key, expected in expected_top_level.items():
            if first[key] != expected:
                raise AssertionError(key)

        metadata = first["cross_system_coordination_metadata"]
        if metadata["coordination_metadata_mode"] != "metadata_only":
            raise AssertionError("coordination_metadata_mode")
        if metadata["coordination_metadata_available"] is not True:
            raise AssertionError("coordination_metadata_available")

        if list_governance_cross_system_coordination_boundary_section_names() != list(
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_cross_system_coordination_boundary_contract_names() != list(
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_cross_system_coordination_boundary_check_names() != list(
            REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if any(
            section["section_status"] != "pass"
            for section in first["cross_system_coordination_boundary_sections"]
        ):
            raise AssertionError("section status")
        if any(
            contract["contract_status"] != "pass"
            for contract in first["cross_system_coordination_boundary_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            check["check_status"] != "pass"
            for check in first["cross_system_coordination_boundary_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first["deterministic_cross_system_coordination_boundary_hash"]
        second_hash = second[
            "deterministic_cross_system_coordination_boundary_hash"
        ]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "sections": first["cross_system_coordination_boundary_sections"],
                "contracts": first[
                    "cross_system_coordination_boundary_contracts"
                ],
                "checks": first["cross_system_coordination_boundary_checks"],
                "summary": first["cross_system_coordination_boundary_summary"],
                "hash": first_hash,
                "json": governance_cross_system_coordination_boundary_to_json(
                    first
                ),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_cross_system_coordination_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
