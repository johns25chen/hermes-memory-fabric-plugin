#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_operation_ledger_proposal_boundary import (  # noqa: E402
    SAFETY_BOUNDARIES,
    build_governance_operation_ledger_proposal_boundary,
    governance_operation_ledger_proposal_boundary_to_json,
    list_governance_operation_ledger_proposal_boundary_check_names,
    list_governance_operation_ledger_proposal_boundary_contract_names,
    list_governance_operation_ledger_proposal_boundary_section_names,
)


EXPECTED_SECTION_NAMES = [
    "adapter_handoff_audit_input_section",
    "handoff_metadata_section",
    "proposal_metadata_section",
    "candidate_only_boundary_section",
    "runtime_disabled_boundary_section",
    "write_disabled_boundary_section",
    "operation_ledger_entry_not_created_section",
    "operation_ledger_proposal_not_persisted_section",
    "external_call_disabled_boundary_section",
    "adapter_sandbox_not_entered_section",
    "star_cosmos_candidate_only_section",
    "future_cross_system_coordination_readiness_section",
]

EXPECTED_CONTRACT_NAMES = [
    "operation_ledger_proposal_boundary_only_contract",
    "operation_ledger_proposal_metadata_only_contract",
    "adapter_handoff_audit_pass_contract",
    "adapter_handoff_audit_hash_present_contract",
    "adapter_handoff_audit_hash_stable_contract",
    "proposal_readiness_conditions_declared_contract",
    "proposal_evidence_requirements_declared_contract",
    "proposal_blocking_conditions_declared_contract",
    "proposal_boundary_sections_complete_contract",
    "proposal_boundary_sections_pass_contract",
    "candidate_only_boundary_contract",
    "future_cross_system_coordination_not_entered_contract",
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
    "no_operation_ledger_entry_created_contract",
    "no_operation_ledger_entry_written_contract",
    "no_operation_ledger_proposal_persisted_contract",
    "no_operation_ledger_proposal_submitted_contract",
    "no_operation_ledger_proposal_dispatched_contract",
    "no_real_approval_record_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_issued_contract",
    "no_authorization_token_created_contract",
    "no_authorization_grant_created_contract",
    "no_adapter_sandbox_entry_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "operation_ledger_proposal_boundary_stage_check",
    "operation_ledger_proposal_boundary_only_mode_check",
    "operation_ledger_proposal_metadata_only_check",
    "operation_ledger_entry_not_created_check",
    "operation_ledger_write_not_written_check",
    "adapter_handoff_audit_pass_check",
    "adapter_handoff_audit_hash_present_check",
    "adapter_handoff_audit_hash_stable_check",
    "proposal_readiness_conditions_declared_check",
    "proposal_evidence_requirements_declared_check",
    "proposal_blocking_conditions_declared_check",
    "proposal_boundary_sections_complete_check",
    "proposal_boundary_sections_pass_check",
    "proposal_boundary_contracts_pass_check",
    "candidate_only_boundary_check",
    "future_cross_system_coordination_not_entered_check",
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
    "no_operation_ledger_entry_created_check",
    "no_operation_ledger_entry_written_check",
    "no_operation_ledger_proposal_persisted_check",
    "no_operation_ledger_proposal_submitted_check",
    "no_operation_ledger_proposal_dispatched_check",
    "no_real_approval_record_check",
    "no_approval_notification_check",
    "no_execution_authorization_issued_check",
    "no_authorization_token_created_check",
    "no_authorization_grant_created_check",
    "no_adapter_sandbox_entry_check",
    "star_cosmos_candidate_only_check",
    "deterministic_operation_ledger_proposal_boundary_hash_check",
    "proposal_boundary_readiness_check",
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
    "operation_ledger_mutation_enabled",
    "operation_ledger_entry_created",
    "operation_ledger_entry_written",
    "operation_ledger_proposal_persisted",
    "operation_ledger_proposal_submitted",
    "operation_ledger_proposal_dispatched",
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
    lowered = json.dumps(value, sort_keys=True).lower()
    for blocked in SENSITIVE_BLOCKED_TERMS:
        candidate = blocked if blocked.startswith("/") else blocked.lower()
        if candidate in lowered:
            raise AssertionError(blocked)


def main() -> int:
    try:
        first = build_governance_operation_ledger_proposal_boundary()
        second = build_governance_operation_ledger_proposal_boundary()

        if first != second:
            raise AssertionError("proposal boundary changed between builds")
        expected_top_level = {
            "operation_ledger_proposal_boundary_status": "pass",
            "operation_ledger_proposal_boundary_stage": (
                "v5.9_operation_ledger_proposal_boundary"
            ),
            "operation_ledger_proposal_boundary_mode": (
                "operation_ledger_proposal_boundary_only"
            ),
            "operation_ledger_proposal_mode": "metadata_only",
            "operation_ledger_entry_status": "not_created",
            "operation_ledger_write_status": "not_written",
            "future_cross_system_coordination_status": "not_entered",
            "star_cosmos_entry_status": "candidate_only",
            "adapter_handoff_audit_status": "pass",
        }
        for key, expected in expected_top_level.items():
            if first[key] != expected:
                raise AssertionError(key)

        metadata = first["operation_ledger_proposal_metadata"]
        if metadata["proposal_metadata_mode"] != "metadata_only":
            raise AssertionError("proposal_metadata_mode")
        if metadata["proposal_metadata_available"] is not True:
            raise AssertionError("proposal_metadata_available")
        for key in COMMON_FALSE_FIELDS:
            if first[key] is not False:
                raise AssertionError(key)
            if metadata[key] is not False:
                raise AssertionError(key)

        if (
            list_governance_operation_ledger_proposal_boundary_section_names()
            != EXPECTED_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if (
            list_governance_operation_ledger_proposal_boundary_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if (
            list_governance_operation_ledger_proposal_boundary_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if (
            first["deterministic_operation_ledger_proposal_boundary_hash"]
            != second["deterministic_operation_ledger_proposal_boundary_hash"]
        ):
            raise AssertionError(
                "deterministic_operation_ledger_proposal_boundary_hash"
            )
        for section in first["operation_ledger_proposal_boundary_sections"]:
            if section["section_status"] != "pass":
                raise AssertionError(section["section_name"])
        for contract in first["operation_ledger_proposal_boundary_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["operation_ledger_proposal_boundary_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])

        _assert_safety(first)
        json_output = governance_operation_ledger_proposal_boundary_to_json(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "sections": first[
                    "operation_ledger_proposal_boundary_sections"
                ],
                "contracts": first[
                    "operation_ledger_proposal_boundary_contracts"
                ],
                "checks": first["operation_ledger_proposal_boundary_checks"],
                "summary": first[
                    "operation_ledger_proposal_boundary_summary"
                ],
                "hashes": {
                    "proposal_boundary": first[
                        "deterministic_operation_ledger_proposal_boundary_hash"
                    ],
                    "adapter_handoff_audit": first[
                        "adapter_handoff_audit_hash"
                    ],
                },
                "json": json_output,
            }
        )
    except Exception as exc:  # pragma: no cover - smoke failure path
        print(
            f"governance_operation_ledger_proposal_boundary=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_operation_ledger_proposal_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
