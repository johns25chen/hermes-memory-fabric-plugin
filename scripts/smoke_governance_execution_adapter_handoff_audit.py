#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_execution_adapter_handoff_audit import (  # noqa: E402
    SAFETY_BOUNDARIES,
    build_governance_execution_adapter_handoff_audit,
    governance_execution_adapter_handoff_audit_to_json,
    list_governance_execution_adapter_handoff_audit_check_names,
    list_governance_execution_adapter_handoff_audit_contract_names,
    list_governance_execution_adapter_handoff_audit_section_names,
)


EXPECTED_SECTION_NAMES = [
    "v5_0_execution_adapter_boundary_audit",
    "v5_1_adapter_contract_registry_audit",
    "v5_2_adapter_capability_manifest_audit",
    "v5_3_invocation_request_envelope_audit",
    "v5_4_human_approval_boundary_audit",
    "v5_5_adapter_dry_run_simulator_audit",
    "v5_6_side_effect_policy_registry_audit",
    "v5_7_execution_plan_review_matrix_audit",
    "manifest_authorization_gate_audit",
    "authorization_metadata_audit",
    "approval_metadata_audit",
    "candidate_only_boundary_audit",
    "runtime_disabled_boundary_audit",
    "write_disabled_boundary_audit",
    "external_call_disabled_boundary_audit",
    "adapter_sandbox_not_entered_audit",
    "star_cosmos_candidate_only_audit",
    "future_handoff_readiness_audit",
]

EXPECTED_CONTRACT_NAMES = [
    "adapter_handoff_audit_only_contract",
    "future_adapter_sandbox_not_entered_contract",
    "manifest_authorization_gate_pass_contract",
    "manifest_authorization_gate_hash_present_contract",
    "manifest_authorization_gate_hash_stable_contract",
    "handoff_metadata_only_contract",
    "handoff_readiness_conditions_declared_contract",
    "handoff_evidence_requirements_declared_contract",
    "handoff_blocking_conditions_declared_contract",
    "handoff_audit_sections_complete_contract",
    "handoff_audit_sections_pass_contract",
    "authorization_metadata_only_contract",
    "approval_metadata_only_contract",
    "candidate_only_boundary_contract",
    "no_real_execution_contract",
    "no_adapter_invocation_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_manifest_execution_contract",
    "no_dry_run_plan_execution_contract",
    "no_external_call_contract",
    "no_durable_write_contract",
    "no_filesystem_write_contract",
    "no_database_write_contract",
    "no_memory_graph_mutation_contract",
    "no_operation_ledger_write_contract",
    "no_real_approval_record_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_issued_contract",
    "no_authorization_token_created_contract",
    "no_authorization_grant_created_contract",
    "no_adapter_sandbox_entry_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "adapter_handoff_audit_stage_check",
    "adapter_handoff_audit_only_mode_check",
    "future_adapter_sandbox_not_entered_check",
    "manifest_authorization_gate_pass_check",
    "manifest_authorization_gate_hash_present_check",
    "manifest_authorization_gate_hash_stable_check",
    "handoff_metadata_only_check",
    "handoff_readiness_conditions_declared_check",
    "handoff_evidence_requirements_declared_check",
    "handoff_blocking_conditions_declared_check",
    "handoff_audit_sections_complete_check",
    "handoff_audit_sections_pass_check",
    "handoff_audit_contracts_pass_check",
    "authorization_metadata_only_check",
    "approval_metadata_only_check",
    "candidate_only_boundary_check",
    "no_real_execution_check",
    "no_adapter_invocation_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_manifest_execution_check",
    "no_dry_run_plan_execution_check",
    "no_external_call_check",
    "no_durable_write_check",
    "no_filesystem_write_check",
    "no_database_write_check",
    "no_memory_graph_mutation_check",
    "no_operation_ledger_write_check",
    "no_real_approval_record_check",
    "no_approval_notification_check",
    "no_execution_authorization_issued_check",
    "no_authorization_token_created_check",
    "no_authorization_grant_created_check",
    "no_adapter_sandbox_entry_check",
    "star_cosmos_candidate_only_check",
    "deterministic_handoff_audit_hash_check",
    "handoff_audit_readiness_check",
]

COMMON_FALSE_FIELDS = (
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "adapter_dispatched",
    "manifest_dispatched",
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
    "approval_request_created",
    "approval_notification_sent",
    "real_approval_record_written",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "adapter_sandbox_entered",
    "controlled_adapter_sandbox_started",
)

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_artifact"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call",
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
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
        first = build_governance_execution_adapter_handoff_audit()
        second = build_governance_execution_adapter_handoff_audit()

        if first != second:
            raise AssertionError("adapter handoff audit changed between builds")
        if first["adapter_handoff_audit_status"] != "pass":
            raise AssertionError("adapter_handoff_audit_status")
        if first["adapter_handoff_audit_stage"] != "v5.8_adapter_handoff_audit":
            raise AssertionError("adapter_handoff_audit_stage")
        if first["adapter_handoff_audit_mode"] != "adapter_handoff_audit_only":
            raise AssertionError("adapter_handoff_audit_mode")
        if first["future_adapter_sandbox_status"] != "not_entered":
            raise AssertionError("future_adapter_sandbox_status")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        if first["manifest_authorization_gate_status"] != "pass":
            raise AssertionError("manifest_authorization_gate_status")
        metadata = first["adapter_handoff_audit_metadata"]
        if metadata["handoff_audit_metadata_mode"] != "metadata_only":
            raise AssertionError("handoff_audit_metadata_mode")
        if metadata["handoff_audit_status"] != "not_handed_off":
            raise AssertionError("handoff_audit_status")
        for key in COMMON_FALSE_FIELDS:
            if first[key] is not False:
                raise AssertionError(key)
            if key in metadata and metadata[key] is not False:
                raise AssertionError(key)
        if (
            list_governance_execution_adapter_handoff_audit_section_names()
            != EXPECTED_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if (
            list_governance_execution_adapter_handoff_audit_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if (
            list_governance_execution_adapter_handoff_audit_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check names")
        if (
            first["deterministic_adapter_handoff_audit_hash"]
            != second["deterministic_adapter_handoff_audit_hash"]
        ):
            raise AssertionError("deterministic_adapter_handoff_audit_hash")
        for section in first["adapter_handoff_audit_sections"]:
            if section["section_status"] != "pass":
                raise AssertionError(section["section_name"])
        for contract in first["adapter_handoff_audit_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["adapter_handoff_audit_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])
        _assert_safety(first)
        json_output = governance_execution_adapter_handoff_audit_to_json(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "sections": first["adapter_handoff_audit_sections"],
                "contracts": first["adapter_handoff_audit_contracts"],
                "checks": first["adapter_handoff_audit_checks"],
                "summary": first["adapter_handoff_audit_summary"],
                "hashes": {
                    "handoff_audit": first[
                        "deterministic_adapter_handoff_audit_hash"
                    ],
                    "manifest_authorization_gate": first[
                        "manifest_authorization_gate_hash"
                    ],
                },
                "json": json_output,
            }
        )
    except Exception as exc:  # pragma: no cover - smoke failure path
        print(
            f"governance_execution_adapter_handoff_audit=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_handoff_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
