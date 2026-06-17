#!/usr/bin/env python3
"""Smoke test for the execution adapter declaration schema registry."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_execution_adapter_declaration_schema_registry import (  # noqa: E402
    build_governance_execution_adapter_declaration_schema_registry,
    governance_execution_adapter_declaration_schema_registry_to_json,
    list_governance_execution_adapter_declaration_schema_check_names,
    list_governance_execution_adapter_declaration_schema_contract_names,
    list_governance_execution_adapter_declaration_schema_field_names,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


EXPECTED_FIELD_NAMES = [
    "adapter_id",
    "adapter_name",
    "adapter_kind",
    "adapter_version",
    "adapter_owner",
    "adapter_description",
    "declared_capabilities",
    "declared_inputs",
    "declared_outputs",
    "declared_permissions",
    "declared_side_effects",
    "declared_external_dependencies",
    "declared_durable_writes",
    "declared_memory_graph_mutations",
    "declared_operation_ledger_writes",
    "declared_approval_requirements",
    "declared_dry_run_inspection",
    "declared_redaction_policy",
    "declared_safety_boundaries",
    "declared_star_cosmos_entry_status",
]

EXPECTED_CONTRACT_NAMES = [
    "schema_registry_declaration_only_contract",
    "adapter_identity_schema_contract",
    "adapter_capability_schema_contract",
    "adapter_input_schema_contract",
    "adapter_output_schema_contract",
    "adapter_permission_schema_contract",
    "adapter_side_effect_schema_contract",
    "adapter_external_dependency_schema_contract",
    "adapter_durable_write_schema_contract",
    "adapter_memory_graph_mutation_schema_contract",
    "adapter_operation_ledger_write_schema_contract",
    "adapter_human_approval_schema_contract",
    "adapter_dry_run_inspection_schema_contract",
    "adapter_redaction_schema_contract",
    "star_cosmos_candidate_only_schema_contract",
]

EXPECTED_CHECK_NAMES = [
    "execution_adapter_boundary_pass_check",
    "declaration_schema_registry_stage_check",
    "schema_only_mode_check",
    "declaration_fields_complete_check",
    "declaration_contracts_complete_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
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
    "fixture-approval-phrase-5-0",
    "fixture-stdout-tail-5-0",
    "fixture-stdout-5-0",
    "fixture-raw-logs-5-0",
    "fixture-token-5-0",
    "fixture-api-key-5-0",
    "fixture-secret-5-0",
    "fixture-password-5-0",
    "fixture-credential-5-0",
    "fixture-approval-phrase-5-1",
    "fixture-stdout-tail-5-1",
    "fixture-stdout-5-1",
    "fixture-raw-logs-5-1",
    "fixture-token-5-1",
    "fixture-api-key-5-1",
    "fixture-secret-5-1",
    "fixture-password-5-1",
    "fixture-credential-5-1",
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


def _assert_no_sensitive_leak(registry: dict[str, object]) -> None:
    protected = {
        "fields": registry["declaration_schema_fields"],
        "contracts": registry["declaration_schema_contracts"],
        "checks": registry["declaration_schema_checks"],
        "summary": registry["registry_summary"],
        "hashes": {
            "registry": registry["deterministic_declaration_schema_registry_hash"],
            "boundary": registry["boundary_hash"],
        },
        "json": governance_execution_adapter_declaration_schema_registry_to_json(
            registry
        ),
    }
    serialized = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in serialized:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_execution_adapter_declaration_schema_registry()
        second = build_governance_execution_adapter_declaration_schema_registry()

        if first["declaration_schema_registry_status"] != "pass":
            raise AssertionError("declaration_schema_registry_status")
        if (
            first["declaration_schema_registry_stage"]
            != "v5.1_execution_adapter_declaration_schema_registry_candidate"
        ):
            raise AssertionError("declaration_schema_registry_stage")
        if first["declaration_registry_mode"] != "schema_only":
            raise AssertionError("declaration_registry_mode")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        for key in (
            "star_cosmos_memory_active",
            "execution_adapter_implemented",
            "execution_adapter_invoked",
            "real_execution_enabled",
            "external_calls_enabled",
            "durable_writes_enabled",
            "memory_graph_mutation_enabled",
            "operation_ledger_writes_enabled",
            "autonomous_execution_enabled",
        ):
            if first[key] is not False:
                raise AssertionError(key)
        if (
            list_governance_execution_adapter_declaration_schema_field_names()
            != EXPECTED_FIELD_NAMES
        ):
            raise AssertionError("field_names")
        if (
            list_governance_execution_adapter_declaration_schema_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract_names")
        if (
            list_governance_execution_adapter_declaration_schema_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check_names")
        if [
            field["field_name"] for field in first["declaration_schema_fields"]
        ] != EXPECTED_FIELD_NAMES:
            raise AssertionError("fields")
        if [
            contract["contract_name"]
            for contract in first["declaration_schema_contracts"]
        ] != EXPECTED_CONTRACT_NAMES:
            raise AssertionError("contracts")
        if [
            check["check_name"] for check in first["declaration_schema_checks"]
        ] != EXPECTED_CHECK_NAMES:
            raise AssertionError("checks")
        if (
            first["deterministic_declaration_schema_registry_hash"]
            != second["deterministic_declaration_schema_registry_hash"]
        ):
            raise AssertionError("registry_hash_stability")
        for field in first["declaration_schema_fields"]:
            if field["field_status"] != "pass":
                raise AssertionError(field["field_name"])
        for contract in first["declaration_schema_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["declaration_schema_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])

        _assert_safety(first)
        _assert_no_sensitive_leak(first)
    except Exception as exc:
        print(
            "governance_execution_adapter_declaration_schema_registry="
            f"failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_declaration_schema_registry=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
