#!/usr/bin/env python3
"""Smoke test for the governance execution adapter boundary."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_execution_adapter_boundary import (  # noqa: E402
    build_governance_execution_adapter_boundary,
    governance_execution_adapter_boundary_to_json,
    list_governance_execution_adapter_boundary_check_names,
    list_governance_execution_adapter_boundary_contract_names,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


EXPECTED_CONTRACT_NAMES = [
    "adapter_declaration_contract",
    "adapter_identity_contract",
    "adapter_capability_contract",
    "adapter_input_contract",
    "adapter_output_contract",
    "adapter_invocation_prohibition_contract",
    "adapter_side_effect_prohibition_contract",
    "dry_run_inspection_contract",
    "external_call_prohibition_contract",
    "durable_write_prohibition_contract",
    "memory_graph_mutation_prohibition_contract",
    "operation_ledger_write_prohibition_contract",
    "human_approval_non_execution_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "readiness_audit_pass_check",
    "boundary_stage_check",
    "declaration_only_mode_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "contract_completeness_check",
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


def _assert_no_sensitive_leak(boundary: dict[str, object]) -> None:
    protected = {
        "contracts": boundary["adapter_boundary_contracts"],
        "checks": boundary["boundary_checks"],
        "summary": boundary["boundary_summary"],
        "hashes": {
            "boundary": boundary["deterministic_execution_adapter_boundary_hash"],
            "readiness": boundary["readiness_audit_hash"],
        },
        "json": governance_execution_adapter_boundary_to_json(boundary),
    }
    serialized = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in serialized:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_execution_adapter_boundary()
        second = build_governance_execution_adapter_boundary()

        if first["execution_adapter_boundary_status"] != "pass":
            raise AssertionError("execution_adapter_boundary_status")
        if (
            first["boundary_stage"]
            != "v5.0_execution_adapter_boundary_candidate"
        ):
            raise AssertionError("boundary_stage")
        if first["boundary_mode"] != "declaration_only":
            raise AssertionError("boundary_mode")
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
            list_governance_execution_adapter_boundary_contract_names()
            != EXPECTED_CONTRACT_NAMES
        ):
            raise AssertionError("contract_names")
        if list_governance_execution_adapter_boundary_check_names() != EXPECTED_CHECK_NAMES:
            raise AssertionError("check_names")
        if [
            contract["contract_name"]
            for contract in first["adapter_boundary_contracts"]
        ] != EXPECTED_CONTRACT_NAMES:
            raise AssertionError("contracts")
        if [
            check["check_name"]
            for check in first["boundary_checks"]
        ] != EXPECTED_CHECK_NAMES:
            raise AssertionError("checks")
        if (
            first["deterministic_execution_adapter_boundary_hash"]
            != second["deterministic_execution_adapter_boundary_hash"]
        ):
            raise AssertionError("boundary_hash_stability")
        for contract in first["adapter_boundary_contracts"]:
            if contract["contract_status"] != "pass":
                raise AssertionError(contract["contract_name"])
        for check in first["boundary_checks"]:
            if check["check_status"] != "pass":
                raise AssertionError(check["check_name"])

        _assert_safety(first)
        _assert_no_sensitive_leak(first)
    except Exception as exc:
        print(
            f"governance_execution_adapter_boundary=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_execution_adapter_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
