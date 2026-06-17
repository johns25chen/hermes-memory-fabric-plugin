#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_execution_adapter_manifest_validation_matrix import (  # noqa: E402
    SAFETY_BOUNDARIES,
    build_governance_execution_adapter_manifest_validation_matrix,
    governance_execution_adapter_manifest_validation_matrix_to_json,
    list_governance_execution_adapter_manifest_validation_check_names,
    list_governance_execution_adapter_manifest_validation_contract_names,
    list_governance_execution_adapter_manifest_validation_row_names,
)


EXPECTED_ROW_NAMES = [
    "minimal_read_only_fixture_validation_row",
    "permission_declared_fixture_validation_row",
    "external_dependency_declared_fixture_validation_row",
    "durable_write_disabled_fixture_validation_row",
    "memory_graph_mutation_disabled_fixture_validation_row",
    "operation_ledger_write_disabled_fixture_validation_row",
    "approval_required_fixture_validation_row",
    "redaction_required_fixture_validation_row",
    "star_cosmos_candidate_only_fixture_validation_row",
    "fixture_pack_integrity_validation_row",
    "fixture_contract_integrity_validation_row",
    "fixture_check_integrity_validation_row",
    "deterministic_hash_validation_row",
    "sanitized_payload_validation_row",
    "safety_boundary_validation_row",
    "candidate_only_boundary_validation_row",
]

EXPECTED_CONTRACT_NAMES = [
    "validation_matrix_only_contract",
    "manifest_fixture_pack_pass_contract",
    "validation_row_names_complete_contract",
    "validation_rows_pass_contract",
    "fixture_pack_hash_present_contract",
    "fixture_pack_hash_stable_contract",
    "fixture_payload_sanitized_contract",
    "fixture_contracts_pass_contract",
    "fixture_checks_pass_contract",
    "no_executable_command_validation_contract",
    "no_live_endpoint_validation_contract",
    "no_secret_validation_contract",
    "no_raw_log_validation_contract",
    "adapter_not_implemented_validation_contract",
    "adapter_not_invoked_validation_contract",
    "manifest_not_executed_validation_contract",
    "dry_run_plan_not_executed_validation_contract",
    "real_execution_disabled_validation_contract",
    "external_calls_disabled_validation_contract",
    "durable_writes_disabled_validation_contract",
    "filesystem_writes_disabled_validation_contract",
    "database_writes_disabled_validation_contract",
    "memory_graph_mutation_disabled_validation_contract",
    "operation_ledger_writes_disabled_validation_contract",
    "autonomous_execution_disabled_validation_contract",
    "star_cosmos_candidate_only_validation_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_fixture_pack_pass_check",
    "manifest_validation_matrix_stage_check",
    "validation_only_mode_check",
    "validation_row_names_complete_check",
    "validation_rows_pass_check",
    "validation_contracts_pass_check",
    "fixture_pack_hash_present_check",
    "fixture_pack_hash_stable_check",
    "fixture_payloads_sanitized_check",
    "fixture_contracts_pass_check",
    "fixture_checks_pass_check",
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
        first = build_governance_execution_adapter_manifest_validation_matrix()
        second = build_governance_execution_adapter_manifest_validation_matrix()

        if first != second:
            raise AssertionError("manifest validation matrix changed between builds")
        if first["manifest_validation_matrix_status"] != "pass":
            raise AssertionError("manifest_validation_matrix_status")
        if (
            first["manifest_validation_matrix_stage"]
            != "v5.4_execution_adapter_manifest_validation_matrix_candidate"
        ):
            raise AssertionError("manifest_validation_matrix_stage")
        if first["manifest_validation_matrix_mode"] != "validation_only":
            raise AssertionError("manifest_validation_matrix_mode")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        for key in COMMON_FALSE_FIELDS:
            if first[key] is not False:
                raise AssertionError(key)
        if (
            list_governance_execution_adapter_manifest_validation_row_names()
            != EXPECTED_ROW_NAMES
        ):
            raise AssertionError("row names")
        if (
            list_governance_execution_adapter_manifest_validation_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if (
            list_governance_execution_adapter_manifest_validation_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check names")
        if (
            first["deterministic_manifest_validation_matrix_hash"]
            != second["deterministic_manifest_validation_matrix_hash"]
        ):
            raise AssertionError("deterministic_manifest_validation_matrix_hash")
        for row in first["manifest_validation_rows"]:
            if row["row_status"] != "pass":
                raise AssertionError(row["row_name"])
        for contract in first["manifest_validation_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["manifest_validation_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])
        _assert_safety(first)
        json_output = governance_execution_adapter_manifest_validation_matrix_to_json(
            first
        )
        _assert_no_sensitive_leak(
            {
                "rows": first["manifest_validation_rows"],
                "contracts": first["manifest_validation_contracts"],
                "checks": first["manifest_validation_checks"],
                "summary": first["manifest_validation_matrix_summary"],
                "hash": first["deterministic_manifest_validation_matrix_hash"],
                "fixture_pack_hash": first["manifest_fixture_pack_hash"],
                "json": json_output,
            }
        )
    except Exception as exc:  # pragma: no cover
        print(
            f"governance_execution_adapter_manifest_validation_matrix=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_manifest_validation_matrix=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
