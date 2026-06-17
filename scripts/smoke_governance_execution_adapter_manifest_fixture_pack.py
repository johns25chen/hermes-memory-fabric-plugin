#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_execution_adapter_manifest_fixture_pack import (  # noqa: E402
    SAFETY_BOUNDARIES,
    build_governance_execution_adapter_manifest_fixture_pack,
    governance_execution_adapter_manifest_fixture_pack_to_json,
    list_governance_execution_adapter_manifest_fixture_check_names,
    list_governance_execution_adapter_manifest_fixture_contract_names,
    list_governance_execution_adapter_manifest_fixture_names,
)


EXPECTED_FIXTURE_NAMES = [
    "minimal_read_only_manifest_fixture",
    "permission_declared_manifest_fixture",
    "external_dependency_declared_manifest_fixture",
    "durable_write_declared_but_disabled_manifest_fixture",
    "memory_graph_mutation_declared_but_disabled_manifest_fixture",
    "operation_ledger_write_declared_but_disabled_manifest_fixture",
    "approval_required_manifest_fixture",
    "redaction_required_manifest_fixture",
    "star_cosmos_candidate_only_manifest_fixture",
]

EXPECTED_CONTRACT_NAMES = [
    "fixture_pack_only_contract",
    "manifest_dry_run_design_pass_contract",
    "sanitized_fixture_payload_contract",
    "fixture_names_complete_contract",
    "fixture_payload_json_contract",
    "no_executable_command_fixture_contract",
    "no_live_endpoint_fixture_contract",
    "no_secret_fixture_contract",
    "no_raw_log_fixture_contract",
    "adapter_not_implemented_fixture_contract",
    "adapter_not_invoked_fixture_contract",
    "manifest_not_executed_fixture_contract",
    "dry_run_plan_not_executed_fixture_contract",
    "external_calls_disabled_fixture_contract",
    "durable_writes_disabled_fixture_contract",
    "filesystem_writes_disabled_fixture_contract",
    "database_writes_disabled_fixture_contract",
    "memory_graph_mutation_disabled_fixture_contract",
    "operation_ledger_writes_disabled_fixture_contract",
    "autonomous_execution_disabled_fixture_contract",
    "star_cosmos_candidate_only_fixture_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_dry_run_design_pass_check",
    "manifest_fixture_pack_stage_check",
    "fixture_only_mode_check",
    "fixture_names_complete_check",
    "fixture_payloads_sanitized_check",
    "fixture_payloads_json_compatible_check",
    "fixture_payloads_deterministic_check",
    "no_executable_command_check",
    "no_live_endpoint_check",
    "no_secret_or_token_check",
    "no_raw_log_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "manifest_not_executed_check",
    "dry_run_plan_not_executed_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "filesystem_writes_disabled_check",
    "database_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
]

COMMON_FALSE_FIELDS = (
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "manifest_executed",
    "dry_run_plan_executed",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
)

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase",
    "fixture-stdout-tail",
    "fixture-stdout",
    "fixture-stderr",
    "fixture-raw-logs",
    "fixture-token",
    "fixture-api-key",
    "fixture-secret",
    "fixture-password",
    "fixture-credential",
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "git " + "push",
    "g" + "h api",
)


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_FALSE_FIELDS:
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
    serialized = json.dumps(value, sort_keys=True)
    lowered = serialized.lower()
    for blocked in SENSITIVE_BLOCKED_TERMS:
        candidate = blocked if blocked.startswith("/") else blocked.lower()
        if candidate in lowered:
            raise AssertionError(blocked)


def main() -> int:
    try:
        first = build_governance_execution_adapter_manifest_fixture_pack()
        second = build_governance_execution_adapter_manifest_fixture_pack()

        if first != second:
            raise AssertionError("manifest fixture pack changed between builds")
        if first["manifest_fixture_pack_status"] != "pass":
            raise AssertionError("manifest_fixture_pack_status")
        if (
            first["manifest_fixture_pack_stage"]
            != "v5.3_execution_adapter_manifest_fixture_pack_candidate"
        ):
            raise AssertionError("manifest_fixture_pack_stage")
        if first["manifest_fixture_pack_mode"] != "fixture_only":
            raise AssertionError("manifest_fixture_pack_mode")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        for key in COMMON_FALSE_FIELDS:
            if first[key] is not False:
                raise AssertionError(key)
        if (
            list_governance_execution_adapter_manifest_fixture_names()
            != EXPECTED_FIXTURE_NAMES
        ):
            raise AssertionError("fixture names")
        if (
            list_governance_execution_adapter_manifest_fixture_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if (
            list_governance_execution_adapter_manifest_fixture_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check names")
        if (
            first["deterministic_manifest_fixture_pack_hash"]
            != second["deterministic_manifest_fixture_pack_hash"]
        ):
            raise AssertionError("deterministic_manifest_fixture_pack_hash")
        for fixture in first["manifest_fixtures"]:
            if fixture["fixture_status"] != "pass":
                raise AssertionError(fixture["fixture_name"])
        for contract in first["manifest_fixture_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["manifest_fixture_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])
        _assert_safety(first)
        json_output = governance_execution_adapter_manifest_fixture_pack_to_json(
            first
        )
        _assert_no_sensitive_leak(
            {
                "fixtures": first["manifest_fixtures"],
                "contracts": first["manifest_fixture_contracts"],
                "checks": first["manifest_fixture_checks"],
                "summary": first["manifest_fixture_pack_summary"],
                "hash": first["deterministic_manifest_fixture_pack_hash"],
                "design_hash": first["manifest_dry_run_design_hash"],
                "json": json_output,
            }
        )
    except Exception as exc:  # pragma: no cover
        print(
            f"governance_execution_adapter_manifest_fixture_pack=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_manifest_fixture_pack=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
