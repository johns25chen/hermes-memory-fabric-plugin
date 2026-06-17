#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_execution_adapter_manifest_approval_gate import (  # noqa: E402
    SAFETY_BOUNDARIES,
    build_governance_execution_adapter_manifest_approval_gate,
    governance_execution_adapter_manifest_approval_gate_to_json,
    list_governance_execution_adapter_manifest_approval_check_names,
    list_governance_execution_adapter_manifest_approval_contract_names,
    list_governance_execution_adapter_manifest_approval_decision_names,
)


EXPECTED_DECISION_NAMES = [
    "policy_gate_pass_approval_decision",
    "policy_gate_hash_approval_decision",
    "approval_request_metadata_only_decision",
    "approval_roles_declared_decision",
    "approval_evidence_requirements_declared_decision",
    "approval_blocking_conditions_declared_decision",
    "sanitized_payload_approval_decision",
    "candidate_only_approval_decision",
    "no_real_execution_approval_decision",
    "no_adapter_invocation_approval_decision",
    "no_manifest_execution_approval_decision",
    "no_dry_run_plan_execution_approval_decision",
    "no_external_call_approval_decision",
    "no_durable_write_approval_decision",
    "no_filesystem_write_approval_decision",
    "no_database_write_approval_decision",
    "no_memory_graph_mutation_approval_decision",
    "no_operation_ledger_write_approval_decision",
    "no_autonomous_execution_approval_decision",
    "no_real_approval_record_write_decision",
    "no_approval_notification_decision",
    "star_cosmos_candidate_only_approval_decision",
]

EXPECTED_CONTRACT_NAMES = [
    "approval_gate_only_contract",
    "manifest_policy_gate_pass_contract",
    "approval_request_metadata_only_contract",
    "approval_roles_declared_contract",
    "approval_evidence_requirements_declared_contract",
    "approval_blocking_conditions_declared_contract",
    "approval_decision_names_complete_contract",
    "approval_decisions_pass_contract",
    "policy_gate_hash_present_contract",
    "policy_gate_hash_stable_contract",
    "sanitized_payload_approval_contract",
    "candidate_only_approval_contract",
    "no_real_execution_approval_contract",
    "no_adapter_invocation_approval_contract",
    "no_manifest_execution_approval_contract",
    "no_dry_run_plan_execution_approval_contract",
    "no_external_call_approval_contract",
    "no_durable_write_approval_contract",
    "no_filesystem_write_approval_contract",
    "no_database_write_approval_contract",
    "no_memory_graph_mutation_approval_contract",
    "no_operation_ledger_write_approval_contract",
    "no_autonomous_execution_approval_contract",
    "no_real_approval_record_write_contract",
    "no_approval_notification_contract",
    "star_cosmos_candidate_only_approval_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_policy_gate_pass_check",
    "manifest_approval_gate_stage_check",
    "approval_gate_only_mode_check",
    "approval_request_metadata_only_check",
    "approval_roles_declared_check",
    "approval_evidence_requirements_declared_check",
    "approval_blocking_conditions_declared_check",
    "approval_decision_names_complete_check",
    "approval_decisions_pass_check",
    "approval_contracts_pass_check",
    "policy_gate_hash_present_check",
    "policy_gate_hash_stable_check",
    "sanitized_payload_approval_check",
    "candidate_only_approval_check",
    "no_real_execution_approval_check",
    "no_adapter_invocation_approval_check",
    "no_manifest_execution_approval_check",
    "no_dry_run_plan_execution_approval_check",
    "no_external_call_approval_check",
    "no_durable_write_approval_check",
    "no_filesystem_write_approval_check",
    "no_database_write_approval_check",
    "no_memory_graph_mutation_approval_check",
    "no_operation_ledger_write_approval_check",
    "no_autonomous_execution_approval_check",
    "no_real_approval_record_write_check",
    "no_approval_notification_check",
    "star_cosmos_candidate_only_approval_check",
    "deterministic_approval_gate_hash_check",
    "approval_handoff_readiness_check",
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
    "approval_request_created",
    "approval_notification_sent",
    "real_approval_record_written",
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
        first = build_governance_execution_adapter_manifest_approval_gate()
        second = build_governance_execution_adapter_manifest_approval_gate()

        if first != second:
            raise AssertionError("manifest approval gate changed between builds")
        if first["manifest_approval_gate_status"] != "pass":
            raise AssertionError("manifest_approval_gate_status")
        if (
            first["manifest_approval_gate_stage"]
            != "v5.6_execution_adapter_manifest_approval_gate_candidate"
        ):
            raise AssertionError("manifest_approval_gate_stage")
        if first["manifest_approval_gate_mode"] != "approval_gate_only":
            raise AssertionError("manifest_approval_gate_mode")
        if first["star_cosmos_entry_status"] != "candidate_only":
            raise AssertionError("star_cosmos_entry_status")
        if first["manifest_policy_gate_status"] != "pass":
            raise AssertionError("manifest_policy_gate_status")
        metadata = first["manifest_approval_request_metadata"]
        if metadata["approval_request_mode"] != "metadata_only":
            raise AssertionError("approval_request_mode")
        if metadata["approval_request_status"] != "not_created":
            raise AssertionError("approval_request_status")
        for key in COMMON_FALSE_FIELDS:
            if first[key] is not False:
                raise AssertionError(key)
            if key in metadata and metadata[key] is not False:
                raise AssertionError(key)
        if (
            list_governance_execution_adapter_manifest_approval_decision_names()
            != EXPECTED_DECISION_NAMES
        ):
            raise AssertionError("decision names")
        if (
            list_governance_execution_adapter_manifest_approval_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if (
            list_governance_execution_adapter_manifest_approval_check_names()
            != EXPECTED_CHECK_NAMES
        ):
            raise AssertionError("check names")
        if (
            first["deterministic_manifest_approval_gate_hash"]
            != second["deterministic_manifest_approval_gate_hash"]
        ):
            raise AssertionError("deterministic_manifest_approval_gate_hash")
        for decision in first["manifest_approval_gate_decisions"]:
            if decision["decision_status"] != "pass":
                raise AssertionError(decision["decision_name"])
        for contract in first["manifest_approval_gate_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["manifest_approval_gate_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])
        _assert_safety(first)
        json_output = governance_execution_adapter_manifest_approval_gate_to_json(
            first
        )
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "decisions": first["manifest_approval_gate_decisions"],
                "contracts": first["manifest_approval_gate_contracts"],
                "checks": first["manifest_approval_gate_checks"],
                "summary": first["manifest_approval_gate_summary"],
                "hashes": {
                    "manifest_approval_gate": first[
                        "deterministic_manifest_approval_gate_hash"
                    ],
                    "manifest_policy_gate": first["manifest_policy_gate_hash"],
                },
                "json": json_output,
            }
        )
    except Exception as exc:  # pragma: no cover - smoke failure path
        print(
            f"governance_execution_adapter_manifest_approval_gate=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_manifest_approval_gate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
