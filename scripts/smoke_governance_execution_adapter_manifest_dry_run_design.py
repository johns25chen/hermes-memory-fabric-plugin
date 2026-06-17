#!/usr/bin/env python3
"""Smoke test for the execution adapter manifest dry-run design."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_execution_adapter_manifest_dry_run_design import (  # noqa: E402
    build_governance_execution_adapter_manifest_dry_run_design,
    governance_execution_adapter_manifest_dry_run_design_to_json,
    list_governance_execution_adapter_manifest_design_check_names,
    list_governance_execution_adapter_manifest_design_contract_names,
    list_governance_execution_adapter_manifest_section_names,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


EXPECTED_SECTION_NAMES = [
    "manifest_identity_section",
    "manifest_adapter_reference_section",
    "manifest_capabilities_section",
    "manifest_inputs_section",
    "manifest_outputs_section",
    "manifest_permissions_section",
    "manifest_side_effects_section",
    "manifest_external_dependencies_section",
    "manifest_durable_writes_section",
    "manifest_memory_graph_mutations_section",
    "manifest_operation_ledger_writes_section",
    "manifest_approval_requirements_section",
    "manifest_dry_run_inspection_section",
    "manifest_redaction_policy_section",
    "manifest_safety_boundaries_section",
    "manifest_star_cosmos_candidate_status_section",
]

EXPECTED_CONTRACT_NAMES = [
    "manifest_design_only_contract",
    "declaration_schema_registry_pass_contract",
    "manifest_identity_design_contract",
    "manifest_adapter_reference_design_contract",
    "manifest_capability_design_contract",
    "manifest_input_design_contract",
    "manifest_output_design_contract",
    "manifest_permission_design_contract",
    "manifest_side_effect_design_contract",
    "manifest_external_dependency_design_contract",
    "manifest_durable_write_design_contract",
    "manifest_memory_graph_mutation_design_contract",
    "manifest_operation_ledger_write_design_contract",
    "manifest_approval_requirement_design_contract",
    "manifest_dry_run_inspection_design_contract",
    "manifest_redaction_design_contract",
    "star_cosmos_candidate_only_manifest_contract",
]

EXPECTED_CHECK_NAMES = [
    "declaration_schema_registry_pass_check",
    "manifest_dry_run_design_stage_check",
    "design_only_mode_check",
    "manifest_sections_complete_check",
    "manifest_contracts_complete_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "manifest_not_executed_check",
    "dry_run_plan_not_executed_check",
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
    "fixture-approval-phrase-5-2",
    "fixture-stdout-tail-5-2",
    "fixture-stdout-5-2",
    "fixture-raw-logs-5-2",
    "fixture-token-5-2",
    "fixture-api-key-5-2",
    "fixture-secret-5-2",
    "fixture-password-5-2",
    "fixture-credential-5-2",
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


def _assert_no_sensitive_leak(design: dict[str, object]) -> None:
    protected = {
        "sections": design["manifest_sections"],
        "contracts": design["manifest_design_contracts"],
        "checks": design["manifest_design_checks"],
        "summary": design["manifest_design_summary"],
        "hashes": {
            "manifest": design["deterministic_manifest_dry_run_design_hash"],
            "registry": design["declaration_schema_registry_hash"],
        },
        "json": governance_execution_adapter_manifest_dry_run_design_to_json(
            design
        ),
    }
    serialized = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in serialized:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_execution_adapter_manifest_dry_run_design()
        second = build_governance_execution_adapter_manifest_dry_run_design()

        if first["manifest_dry_run_design_status"] != "pass":
            raise AssertionError("manifest_dry_run_design_status")
        if (
            first["manifest_dry_run_design_stage"]
            != "v5.2_execution_adapter_manifest_dry_run_design_candidate"
        ):
            raise AssertionError("manifest_dry_run_design_stage")
        if first["manifest_dry_run_design_mode"] != "design_only":
            raise AssertionError("manifest_dry_run_design_mode")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        for key in (
            "star_cosmos_memory_active",
            "execution_adapter_implemented",
            "execution_adapter_invoked",
            "manifest_executed",
            "dry_run_plan_executed",
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
            list_governance_execution_adapter_manifest_section_names()
            != EXPECTED_SECTION_NAMES
        ):
            raise AssertionError("section_names")
        if (
            list_governance_execution_adapter_manifest_design_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract_names")
        if (
            list_governance_execution_adapter_manifest_design_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check_names")
        if [
            section["section_name"] for section in first["manifest_sections"]
        ] != EXPECTED_SECTION_NAMES:
            raise AssertionError("sections")
        if [
            contract["contract_name"]
            for contract in first["manifest_design_contracts"]
        ] != EXPECTED_CONTRACT_NAMES:
            raise AssertionError("contracts")
        if [
            check["check_name"] for check in first["manifest_design_checks"]
        ] != EXPECTED_CHECK_NAMES:
            raise AssertionError("checks")
        if (
            first["deterministic_manifest_dry_run_design_hash"]
            != second["deterministic_manifest_dry_run_design_hash"]
        ):
            raise AssertionError("manifest_hash_stability")
        for section in first["manifest_sections"]:
            if section["design_status"] != "pass":
                raise AssertionError(section["section_name"])
        for contract in first["manifest_design_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["manifest_design_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])

        _assert_safety(first)
        _assert_no_sensitive_leak(first)
    except Exception as exc:
        print(
            f"governance_execution_adapter_manifest_dry_run_design=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_manifest_dry_run_design=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
