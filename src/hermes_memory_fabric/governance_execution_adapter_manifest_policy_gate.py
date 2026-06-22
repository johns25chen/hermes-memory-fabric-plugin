"""Deterministic manifest policy-gate metadata for future adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_manifest_validation_matrix import (
    build_governance_execution_adapter_manifest_validation_matrix,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION = "6.5.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_SCHEMA_VERSION = "6.5.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_TYPE = (
    "governance_execution_adapter_manifest_policy_gate"
)
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE = (
    "v5.5_execution_adapter_manifest_policy_gate_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
MANIFEST_POLICY_GATE_MODE = "policy_gate_only"

READY_HANDOFF_STATUS = "ready_for_future_manifest_approval_gate_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_MANIFEST_POLICY_DECISION_NAMES = (
    "validation_matrix_pass_policy_decision",
    "validation_rows_pass_policy_decision",
    "validation_contracts_pass_policy_decision",
    "validation_checks_pass_policy_decision",
    "deterministic_hash_policy_decision",
    "sanitized_payload_policy_decision",
    "candidate_only_policy_decision",
    "safety_boundary_policy_decision",
    "no_real_execution_policy_decision",
    "no_adapter_invocation_policy_decision",
    "no_manifest_execution_policy_decision",
    "no_dry_run_plan_execution_policy_decision",
    "no_external_call_policy_decision",
    "no_durable_write_policy_decision",
    "no_filesystem_write_policy_decision",
    "no_database_write_policy_decision",
    "no_memory_graph_mutation_policy_decision",
    "no_operation_ledger_write_policy_decision",
    "no_autonomous_execution_policy_decision",
    "star_cosmos_candidate_only_policy_decision",
)

REQUIRED_MANIFEST_POLICY_CONTRACT_NAMES = (
    "policy_gate_only_contract",
    "manifest_validation_matrix_pass_contract",
    "policy_decision_names_complete_contract",
    "policy_decisions_pass_contract",
    "validation_matrix_hash_present_contract",
    "validation_matrix_hash_stable_contract",
    "sanitized_payload_policy_contract",
    "candidate_only_policy_contract",
    "no_real_execution_policy_contract",
    "no_adapter_invocation_policy_contract",
    "no_manifest_execution_policy_contract",
    "no_dry_run_plan_execution_policy_contract",
    "no_external_call_policy_contract",
    "no_durable_write_policy_contract",
    "no_filesystem_write_policy_contract",
    "no_database_write_policy_contract",
    "no_memory_graph_mutation_policy_contract",
    "no_operation_ledger_write_policy_contract",
    "no_autonomous_execution_policy_contract",
    "star_cosmos_candidate_only_policy_contract",
)

REQUIRED_MANIFEST_POLICY_CHECK_NAMES = (
    "manifest_validation_matrix_pass_check",
    "manifest_policy_gate_stage_check",
    "policy_gate_only_mode_check",
    "policy_decision_names_complete_check",
    "policy_decisions_pass_check",
    "policy_contracts_pass_check",
    "validation_matrix_hash_present_check",
    "validation_matrix_hash_stable_check",
    "sanitized_payload_policy_check",
    "candidate_only_policy_check",
    "no_real_execution_policy_check",
    "no_adapter_invocation_policy_check",
    "no_manifest_execution_policy_check",
    "no_dry_run_plan_execution_policy_check",
    "no_external_call_policy_check",
    "no_durable_write_policy_check",
    "no_filesystem_write_policy_check",
    "no_database_write_policy_check",
    "no_memory_graph_mutation_policy_check",
    "no_operation_ledger_write_policy_check",
    "no_autonomous_execution_policy_check",
    "star_cosmos_candidate_only_policy_check",
    "deterministic_policy_gate_hash_check",
    "policy_handoff_readiness_check",
)

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "real_execution_enabled": False,
    "external_calls_enabled": False,
    "durable_writes_enabled": False,
    "filesystem_writes_enabled": False,
    "database_writes_enabled": False,
    "memory_graph_mutation_enabled": False,
    "operation_ledger_writes_enabled": False,
    "autonomous_execution_enabled": False,
}

_MANIFEST_POLICY_GATE_HASH_FIELDS = (
    "version",
    "schema_version",
    "manifest_policy_gate_type",
    "manifest_policy_gate_status",
    "manifest_policy_gate_stage",
    "manifest_policy_gate_mode",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "manifest_validation_matrix_version",
    "manifest_validation_matrix_status",
    "manifest_validation_matrix_hash",
    "manifest_policy_gate_decisions",
    "manifest_policy_gate_contracts",
    "manifest_policy_gate_checks",
    "manifest_policy_gate_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MANIFEST_POLICY_GATE_HASH_FIELDS),
    "input_shape": "sanitized future execution adapter manifest policy gate projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_validation_matrix_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_execution_adapter_manifest_policy_gate() -> dict[str, Any]:
    """Build deterministic policy-gate-only manifest metadata."""

    matrix = _detached_json_value(
        build_governance_execution_adapter_manifest_validation_matrix()
    )
    matrix_repeat = _detached_json_value(
        build_governance_execution_adapter_manifest_validation_matrix()
    )
    decisions = _build_policy_decisions(matrix, matrix_repeat)
    contracts = _build_policy_contracts(matrix, matrix_repeat, decisions)
    checks = _build_policy_checks(matrix, matrix_repeat, decisions, contracts)

    matrix_passes = _manifest_validation_matrix_passes(matrix)
    decisions_pass = all(
        decision["decision_status"] == "pass" for decision in decisions
    )
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    policy_gate_status = (
        "pass"
        if matrix_passes and decisions_pass and contracts_pass and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["manifest validation matrix must pass at version 6.5.0"]
                if not matrix_passes
                else []
            ),
            *(
                reason
                for decision in decisions
                for reason in decision["blocking_reasons"]
            ),
            *(
                reason
                for contract in contracts
                for reason in contract["blocking_reasons"]
            ),
            *(reason for check in checks for reason in check["blocking_reasons"]),
        ]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    gate: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_SCHEMA_VERSION
        ),
        "manifest_policy_gate_type": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_TYPE
        ),
        "manifest_policy_gate_status": policy_gate_status,
        "manifest_policy_gate_stage": EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE,
        "manifest_policy_gate_mode": MANIFEST_POLICY_GATE_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "manifest_validation_matrix_version": _string_or_none(
            matrix.get("version")
        ),
        "manifest_validation_matrix_status": _string_or_none(
            matrix.get("manifest_validation_matrix_status")
        ),
        "manifest_validation_matrix_hash": _string_or_none(
            matrix.get("deterministic_manifest_validation_matrix_hash")
        ),
        "manifest_policy_gate_decisions": decisions,
        "manifest_policy_gate_contracts": contracts,
        "manifest_policy_gate_checks": checks,
        "manifest_policy_gate_summary": _manifest_policy_gate_summary(
            decisions,
            contracts,
            checks,
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if policy_gate_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    gate["deterministic_manifest_policy_gate_hash"] = (
        _execution_adapter_manifest_policy_gate_hash(gate)
    )
    return _detached_json_value(gate)


def get_governance_execution_adapter_manifest_policy_decision(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest policy decision by stable name."""

    if not isinstance(name, str):
        return _unknown_decision("")
    gate = build_governance_execution_adapter_manifest_policy_gate()
    for decision in gate["manifest_policy_gate_decisions"]:
        if decision["decision_name"] == name:
            return _detached_json_value(decision)
    return _unknown_decision(name)


def get_governance_execution_adapter_manifest_policy_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest policy contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    gate = build_governance_execution_adapter_manifest_policy_gate()
    for contract in gate["manifest_policy_gate_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_manifest_policy_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest policy check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    gate = build_governance_execution_adapter_manifest_policy_gate()
    for check in gate["manifest_policy_gate_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_manifest_policy_decision_names() -> list[str]:
    """Return stable manifest policy decision names."""

    return list(REQUIRED_MANIFEST_POLICY_DECISION_NAMES)


def list_governance_execution_adapter_manifest_policy_contract_names() -> list[str]:
    """Return stable manifest policy contract names."""

    return list(REQUIRED_MANIFEST_POLICY_CONTRACT_NAMES)


def list_governance_execution_adapter_manifest_policy_check_names() -> list[str]:
    """Return stable manifest policy check names."""

    return list(REQUIRED_MANIFEST_POLICY_CHECK_NAMES)


def governance_execution_adapter_manifest_policy_gate_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize manifest policy-gate metadata deterministically."""

    return (
        json.dumps(
            _detached_json_value(dict(result)),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _build_policy_decisions(
    matrix: Mapping[str, Any],
    matrix_repeat: Mapping[str, Any],
) -> list[dict[str, Any]]:
    row_names = _validation_row_names(matrix)
    contract_names = _validation_contract_names(matrix)
    check_names = _validation_check_names(matrix)
    matrix_hash = _string_or_none(
        matrix.get("deterministic_manifest_validation_matrix_hash")
    )
    repeat_hash = _string_or_none(
        matrix_repeat.get("deterministic_manifest_validation_matrix_hash")
    )
    matrix_hash_present = _is_sha256(matrix_hash)
    matrix_hash_stable = matrix_hash_present and matrix_hash == repeat_hash
    return [
        _decision(
            "validation_matrix_pass_policy_decision",
            decision_type="upstream_manifest_validation_matrix_policy",
            source_validation_row_refs=[
                "fixture_pack_integrity_validation_row",
                "fixture_contract_integrity_validation_row",
                "fixture_check_integrity_validation_row",
            ],
            source_validation_contract_refs=[
                "validation_matrix_only_contract",
                "manifest_fixture_pack_pass_contract",
            ],
            source_validation_check_refs=[
                "manifest_fixture_pack_pass_check",
                "validation_only_mode_check",
            ],
            expected={
                "manifest_validation_matrix_status": "pass",
                "manifest_validation_matrix_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION
                ),
                "manifest_validation_matrix_hash_present": True,
            },
            observed={
                "manifest_validation_matrix_status": _string_or_none(
                    matrix.get("manifest_validation_matrix_status")
                ),
                "manifest_validation_matrix_version": _string_or_none(
                    matrix.get("version")
                ),
                "manifest_validation_matrix_hash_present": matrix_hash_present,
            },
            policy_notes=[
                "policy gate can evaluate only a passing local validation matrix",
                "upstream validation matrix data is observed as metadata",
            ],
            blocking_reasons=_manifest_validation_matrix_blocking_reasons(matrix),
        ),
        _status_decision(
            "validation_rows_pass_policy_decision",
            decision_type="validation_row_policy",
            source_refs=row_names,
            source_validation_contract_refs=["validation_rows_pass_contract"],
            source_validation_check_refs=["validation_rows_pass_check"],
            expected_key="validation_rows_pass",
            blocked_names_key="blocked_validation_row_names",
            source_statuses=_validation_row_statuses(matrix),
            policy_notes=[
                "all validation rows must pass before policy handoff metadata is ready",
            ],
        ),
        _status_decision(
            "validation_contracts_pass_policy_decision",
            decision_type="validation_contract_policy",
            source_refs=row_names,
            source_validation_contract_refs=contract_names,
            source_validation_check_refs=["validation_contracts_pass_check"],
            expected_key="validation_contracts_pass",
            blocked_names_key="blocked_validation_contract_names",
            source_statuses=_validation_contract_statuses(matrix),
            policy_notes=[
                "all validation contracts must pass before policy decisions pass",
            ],
        ),
        _status_decision(
            "validation_checks_pass_policy_decision",
            decision_type="validation_check_policy",
            source_refs=row_names,
            source_validation_contract_refs=["fixture_checks_pass_contract"],
            source_validation_check_refs=check_names,
            expected_key="validation_checks_pass",
            blocked_names_key="blocked_validation_check_names",
            source_statuses=_validation_check_statuses(matrix),
            policy_notes=[
                "all validation checks must pass before policy checks pass",
            ],
        ),
        _decision(
            "deterministic_hash_policy_decision",
            decision_type="deterministic_hash_policy",
            source_validation_row_refs=["deterministic_hash_validation_row"],
            source_validation_contract_refs=[
                "fixture_pack_hash_present_contract",
                "fixture_pack_hash_stable_contract",
            ],
            source_validation_check_refs=[
                "fixture_pack_hash_present_check",
                "fixture_pack_hash_stable_check",
                "deterministic_hash_check",
            ],
            expected={
                "manifest_validation_matrix_hash_present": True,
                "manifest_validation_matrix_hash_stable": True,
            },
            observed={
                "manifest_validation_matrix_hash_present": matrix_hash_present,
                "manifest_validation_matrix_hash_stable": matrix_hash_stable,
            },
            policy_notes=[
                "policy decision inputs require a stable upstream validation matrix hash",
            ],
            blocking_reasons=[]
            if matrix_hash_present and matrix_hash_stable
            else ["manifest validation matrix hash must be present and stable"],
        ),
        _source_status_decision(
            matrix,
            "sanitized_payload_policy_decision",
            decision_type="sanitized_payload_policy",
            row_refs=["sanitized_payload_validation_row"],
            contract_refs=["fixture_payload_sanitized_contract"],
            check_refs=["fixture_payloads_sanitized_check"],
            policy_notes=[
                "policy metadata depends on sanitized validation payload expectations",
            ],
        ),
        _source_status_decision(
            matrix,
            "candidate_only_policy_decision",
            decision_type="candidate_only_policy",
            row_refs=["candidate_only_boundary_validation_row"],
            contract_refs=["star_cosmos_candidate_only_validation_contract"],
            check_refs=["star_cosmos_candidate_only_check"],
            policy_notes=[
                "candidate-only state must remain explicit before any future approval gate",
            ],
        ),
        _decision(
            "safety_boundary_policy_decision",
            decision_type="safety_boundary_policy",
            source_validation_row_refs=["safety_boundary_validation_row"],
            source_validation_contract_refs=[
                "real_execution_disabled_validation_contract",
                "external_calls_disabled_validation_contract",
                "durable_writes_disabled_validation_contract",
            ],
            source_validation_check_refs=[
                "real_execution_disabled_check",
                "external_calls_disabled_check",
                "durable_writes_disabled_check",
            ],
            expected={"all_safety_boundaries_false": True},
            observed={
                "all_safety_boundaries_false": _all_safety_boundaries_false(matrix)
            },
            policy_notes=[
                "policy gate metadata is blocked if any safety boundary is enabled",
            ],
            blocking_reasons=[]
            if _all_safety_boundaries_false(matrix)
            else ["all safety boundaries must remain false"],
        ),
        _disabled_flag_decision(
            matrix,
            "no_real_execution_policy_decision",
            "real_execution_enabled",
            "real_execution_disabled_validation_contract",
            "real_execution_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_adapter_invocation_policy_decision",
            "execution_adapter_invoked",
            "adapter_not_invoked_validation_contract",
            "adapter_not_invoked_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_manifest_execution_policy_decision",
            "manifest_executed",
            "manifest_not_executed_validation_contract",
            "manifest_not_executed_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_dry_run_plan_execution_policy_decision",
            "dry_run_plan_executed",
            "dry_run_plan_not_executed_validation_contract",
            "dry_run_plan_not_executed_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_external_call_policy_decision",
            "external_calls_enabled",
            "external_calls_disabled_validation_contract",
            "external_calls_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_durable_write_policy_decision",
            "durable_writes_enabled",
            "durable_writes_disabled_validation_contract",
            "durable_writes_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_filesystem_write_policy_decision",
            "filesystem_writes_enabled",
            "filesystem_writes_disabled_validation_contract",
            "filesystem_writes_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_database_write_policy_decision",
            "database_writes_enabled",
            "database_writes_disabled_validation_contract",
            "database_writes_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_memory_graph_mutation_policy_decision",
            "memory_graph_mutation_enabled",
            "memory_graph_mutation_disabled_validation_contract",
            "memory_graph_mutation_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_operation_ledger_write_policy_decision",
            "operation_ledger_writes_enabled",
            "operation_ledger_writes_disabled_validation_contract",
            "operation_ledger_writes_disabled_check",
        ),
        _disabled_flag_decision(
            matrix,
            "no_autonomous_execution_policy_decision",
            "autonomous_execution_enabled",
            "autonomous_execution_disabled_validation_contract",
            "autonomous_execution_disabled_check",
        ),
        _decision(
            "star_cosmos_candidate_only_policy_decision",
            decision_type="star_cosmos_candidate_only_policy",
            source_validation_row_refs=[
                "star_cosmos_candidate_only_fixture_validation_row",
                "candidate_only_boundary_validation_row",
            ],
            source_validation_contract_refs=[
                "star_cosmos_candidate_only_validation_contract"
            ],
            source_validation_check_refs=["star_cosmos_candidate_only_check"],
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": _string_or_none(
                    matrix.get("star_cosmos_entry_status")
                ),
                "star_cosmos_memory_active": matrix.get(
                    "star_cosmos_memory_active"
                ),
            },
            policy_notes=[
                "Star-Cosmos remains candidate-only in policy gate metadata",
            ],
            blocking_reasons=[]
            if matrix.get("star_cosmos_entry_status") == STAR_COSMOS_ENTRY_STATUS
            and matrix.get("star_cosmos_memory_active") is False
            else ["Star-Cosmos candidate-only boundary must remain false-active"],
        ),
    ]


def _build_policy_contracts(
    matrix: Mapping[str, Any],
    matrix_repeat: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    decision_names = _decision_names(decisions)
    matrix_hash = _string_or_none(
        matrix.get("deterministic_manifest_validation_matrix_hash")
    )
    repeat_hash = _string_or_none(
        matrix_repeat.get("deterministic_manifest_validation_matrix_hash")
    )
    return [
        _contract(
            "policy_gate_only_contract",
            contract_type="policy_gate_mode_contract",
            expected={
                "manifest_policy_gate_mode": MANIFEST_POLICY_GATE_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "manifest_policy_gate_mode": MANIFEST_POLICY_GATE_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "manifest_validation_matrix_pass_contract",
            contract_type="upstream_manifest_validation_matrix_contract",
            expected={
                "manifest_validation_matrix_status": "pass",
                "manifest_validation_matrix_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION
                ),
                "manifest_validation_matrix_hash_present": True,
            },
            observed={
                "manifest_validation_matrix_status": _string_or_none(
                    matrix.get("manifest_validation_matrix_status")
                ),
                "manifest_validation_matrix_version": _string_or_none(
                    matrix.get("version")
                ),
                "manifest_validation_matrix_hash_present": _is_sha256(matrix_hash),
            },
            blocking_reasons=_manifest_validation_matrix_blocking_reasons(matrix),
        ),
        _contract(
            "policy_decision_names_complete_contract",
            contract_type="policy_decision_name_contract",
            expected={
                "decision_names": list(REQUIRED_MANIFEST_POLICY_DECISION_NAMES),
                "decision_count": len(REQUIRED_MANIFEST_POLICY_DECISION_NAMES),
            },
            observed={
                "decision_names": decision_names,
                "decision_count": len(decision_names),
                "missing_decision_names": _missing_decision_names(decision_names),
                "extra_decision_names": _extra_decision_names(decision_names),
            },
            blocking_reasons=_decision_name_blocking_reasons(decision_names),
        ),
        _contract(
            "policy_decisions_pass_contract",
            contract_type="policy_decision_status_contract",
            expected={"policy_decisions_pass": True, "blocked_decision_count": 0},
            observed={
                "policy_decisions_pass": _decisions_pass(decisions),
                "blocked_decision_count": len(_blocked_decision_names(decisions)),
                "blocked_decision_names": _blocked_decision_names(decisions),
            },
            blocking_reasons=[]
            if _decisions_pass(decisions)
            else ["manifest policy decisions must pass"],
        ),
        _contract(
            "validation_matrix_hash_present_contract",
            contract_type="validation_matrix_hash_contract",
            expected={"manifest_validation_matrix_hash_present": True},
            observed={
                "manifest_validation_matrix_hash_present": _is_sha256(matrix_hash)
            },
            blocking_reasons=[]
            if _is_sha256(matrix_hash)
            else ["manifest validation matrix hash must be present"],
        ),
        _contract(
            "validation_matrix_hash_stable_contract",
            contract_type="validation_matrix_hash_contract",
            expected={"manifest_validation_matrix_hash_stable": True},
            observed={
                "manifest_validation_matrix_hash_stable": _is_sha256(matrix_hash)
                and matrix_hash == repeat_hash
            },
            blocking_reasons=[]
            if _is_sha256(matrix_hash) and matrix_hash == repeat_hash
            else ["manifest validation matrix hash must be stable"],
        ),
        _decision_status_contract(
            "sanitized_payload_policy_contract",
            "sanitized_payload_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "candidate_only_policy_contract",
            "candidate_only_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_real_execution_policy_contract",
            "no_real_execution_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_adapter_invocation_policy_contract",
            "no_adapter_invocation_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_manifest_execution_policy_contract",
            "no_manifest_execution_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_dry_run_plan_execution_policy_contract",
            "no_dry_run_plan_execution_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_external_call_policy_contract",
            "no_external_call_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_durable_write_policy_contract",
            "no_durable_write_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_filesystem_write_policy_contract",
            "no_filesystem_write_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_database_write_policy_contract",
            "no_database_write_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_memory_graph_mutation_policy_contract",
            "no_memory_graph_mutation_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_operation_ledger_write_policy_contract",
            "no_operation_ledger_write_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_autonomous_execution_policy_contract",
            "no_autonomous_execution_policy_decision",
            decisions,
        ),
        _decision_status_contract(
            "star_cosmos_candidate_only_policy_contract",
            "star_cosmos_candidate_only_policy_decision",
            decisions,
        ),
    ]


def _build_policy_checks(
    matrix: Mapping[str, Any],
    matrix_repeat: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    decision_names = _decision_names(decisions)
    matrix_hash = _string_or_none(
        matrix.get("deterministic_manifest_validation_matrix_hash")
    )
    repeat_hash = _string_or_none(
        matrix_repeat.get("deterministic_manifest_validation_matrix_hash")
    )
    checks = [
        _check(
            "manifest_validation_matrix_pass_check",
            expected={
                "manifest_validation_matrix_status": "pass",
                "manifest_validation_matrix_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION
                ),
                "manifest_validation_matrix_hash_present": True,
            },
            observed={
                "manifest_validation_matrix_status": _string_or_none(
                    matrix.get("manifest_validation_matrix_status")
                ),
                "manifest_validation_matrix_version": _string_or_none(
                    matrix.get("version")
                ),
                "manifest_validation_matrix_hash_present": _is_sha256(matrix_hash),
            },
            blocking_reasons=_manifest_validation_matrix_blocking_reasons(matrix),
        ),
        _simple_check(
            "manifest_policy_gate_stage_check",
            EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE,
            EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE,
        ),
        _simple_check(
            "policy_gate_only_mode_check",
            MANIFEST_POLICY_GATE_MODE,
            MANIFEST_POLICY_GATE_MODE,
        ),
        _check(
            "policy_decision_names_complete_check",
            expected={
                "decision_names": list(REQUIRED_MANIFEST_POLICY_DECISION_NAMES),
                "decision_count": len(REQUIRED_MANIFEST_POLICY_DECISION_NAMES),
            },
            observed={
                "decision_names": decision_names,
                "decision_count": len(decision_names),
                "missing_decision_names": _missing_decision_names(decision_names),
                "extra_decision_names": _extra_decision_names(decision_names),
            },
            blocking_reasons=_decision_name_blocking_reasons(decision_names),
        ),
        _check(
            "policy_decisions_pass_check",
            expected={"policy_decisions_pass": True, "blocked_decision_count": 0},
            observed={
                "policy_decisions_pass": _decisions_pass(decisions),
                "blocked_decision_count": len(_blocked_decision_names(decisions)),
                "blocked_decision_names": _blocked_decision_names(decisions),
            },
            blocking_reasons=[]
            if _decisions_pass(decisions)
            else ["manifest policy decisions must pass"],
        ),
        _check(
            "policy_contracts_pass_check",
            expected={"policy_contracts_pass": True, "blocked_contract_count": 0},
            observed={
                "policy_contracts_pass": _contracts_pass(contracts),
                "blocked_contract_count": len(_blocked_contract_names(contracts)),
                "blocked_contract_names": _blocked_contract_names(contracts),
            },
            blocking_reasons=[]
            if _contracts_pass(contracts)
            else ["manifest policy contracts must pass"],
        ),
        _check(
            "validation_matrix_hash_present_check",
            expected={"manifest_validation_matrix_hash_present": True},
            observed={
                "manifest_validation_matrix_hash_present": _is_sha256(matrix_hash)
            },
            blocking_reasons=[]
            if _is_sha256(matrix_hash)
            else ["manifest validation matrix hash must be present"],
        ),
        _check(
            "validation_matrix_hash_stable_check",
            expected={"manifest_validation_matrix_hash_stable": True},
            observed={
                "manifest_validation_matrix_hash_stable": _is_sha256(matrix_hash)
                and matrix_hash == repeat_hash
            },
            blocking_reasons=[]
            if _is_sha256(matrix_hash) and matrix_hash == repeat_hash
            else ["manifest validation matrix hash must be stable"],
        ),
        _decision_status_check(
            "sanitized_payload_policy_check",
            "sanitized_payload_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "candidate_only_policy_check",
            "candidate_only_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_real_execution_policy_check",
            "no_real_execution_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_adapter_invocation_policy_check",
            "no_adapter_invocation_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_manifest_execution_policy_check",
            "no_manifest_execution_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_dry_run_plan_execution_policy_check",
            "no_dry_run_plan_execution_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_external_call_policy_check",
            "no_external_call_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_durable_write_policy_check",
            "no_durable_write_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_filesystem_write_policy_check",
            "no_filesystem_write_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_database_write_policy_check",
            "no_database_write_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_memory_graph_mutation_policy_check",
            "no_memory_graph_mutation_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_operation_ledger_write_policy_check",
            "no_operation_ledger_write_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "no_autonomous_execution_policy_check",
            "no_autonomous_execution_policy_decision",
            decisions,
        ),
        _decision_status_check(
            "star_cosmos_candidate_only_policy_check",
            "star_cosmos_candidate_only_policy_decision",
            decisions,
        ),
        _check(
            "deterministic_policy_gate_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM
                ),
                "decision_contract_check_data_in_hash": True,
            },
            observed={
                "hash_algorithm": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM
                ),
                "decision_contract_check_data_in_hash": all(
                    field in _MANIFEST_POLICY_GATE_HASH_FIELDS
                    for field in (
                        "manifest_policy_gate_decisions",
                        "manifest_policy_gate_contracts",
                        "manifest_policy_gate_checks",
                    )
                ),
            },
            blocking_reasons=[]
            if all(
                field in _MANIFEST_POLICY_GATE_HASH_FIELDS
                for field in (
                    "manifest_policy_gate_decisions",
                    "manifest_policy_gate_contracts",
                    "manifest_policy_gate_checks",
                )
            )
            else ["policy gate hash must include decision, contract, and check data"],
        ),
    ]
    component_checks_pass = all(check["check_status"] == "pass" for check in checks)
    checks.append(
        _check(
            "policy_handoff_readiness_check",
            expected={
                "manifest_validation_matrix_passes": True,
                "policy_decisions_pass": True,
                "policy_contracts_pass": True,
                "component_policy_checks_pass": True,
            },
            observed={
                "manifest_validation_matrix_passes": (
                    _manifest_validation_matrix_passes(matrix)
                ),
                "policy_decisions_pass": _decisions_pass(decisions),
                "policy_contracts_pass": _contracts_pass(contracts),
                "component_policy_checks_pass": component_checks_pass,
            },
            blocking_reasons=[]
            if _manifest_validation_matrix_passes(matrix)
            and _decisions_pass(decisions)
            and _contracts_pass(contracts)
            and component_checks_pass
            else ["policy handoff readiness requires all policy gates to pass"],
        )
    )
    return checks


def _status_decision(
    decision_name: str,
    *,
    decision_type: str,
    source_refs: Sequence[str],
    source_validation_contract_refs: Sequence[str],
    source_validation_check_refs: Sequence[str],
    expected_key: str,
    blocked_names_key: str,
    source_statuses: Mapping[str, str],
    policy_notes: Sequence[str],
) -> dict[str, Any]:
    blocked_names = [
        name for name, status in source_statuses.items() if status != "pass"
    ]
    return _decision(
        decision_name,
        decision_type=decision_type,
        source_validation_row_refs=source_refs,
        source_validation_contract_refs=source_validation_contract_refs,
        source_validation_check_refs=source_validation_check_refs,
        expected={expected_key: True, blocked_names_key: []},
        observed={
            expected_key: not blocked_names,
            blocked_names_key: blocked_names,
            "source_statuses": dict(source_statuses),
        },
        policy_notes=policy_notes,
        blocking_reasons=[]
        if not blocked_names
        else [f"{decision_name} requires all source statuses to pass"],
    )


def _source_status_decision(
    matrix: Mapping[str, Any],
    decision_name: str,
    *,
    decision_type: str,
    row_refs: Sequence[str],
    contract_refs: Sequence[str],
    check_refs: Sequence[str],
    policy_notes: Sequence[str],
) -> dict[str, Any]:
    row_statuses = _named_statuses(
        _manifest_validation_rows(matrix),
        "row_name",
        "row_status",
        row_refs,
    )
    contract_statuses = _named_statuses(
        _manifest_validation_contracts(matrix),
        "contract_name",
        "contract_status",
        contract_refs,
    )
    check_statuses = _named_statuses(
        _manifest_validation_checks(matrix),
        "check_name",
        "check_status",
        check_refs,
    )
    source_passes = all(
        status == "pass"
        for status in [
            *row_statuses.values(),
            *contract_statuses.values(),
            *check_statuses.values(),
        ]
    )
    return _decision(
        decision_name,
        decision_type=decision_type,
        source_validation_row_refs=row_refs,
        source_validation_contract_refs=contract_refs,
        source_validation_check_refs=check_refs,
        expected={"source_validation_metadata_passes": True},
        observed={
            "source_validation_metadata_passes": source_passes,
            "row_statuses": row_statuses,
            "contract_statuses": contract_statuses,
            "check_statuses": check_statuses,
        },
        policy_notes=policy_notes,
        blocking_reasons=[]
        if source_passes
        else [f"{decision_name} source validation metadata must pass"],
    )


def _disabled_flag_decision(
    matrix: Mapping[str, Any],
    decision_name: str,
    flag_name: str,
    contract_ref: str,
    check_ref: str,
) -> dict[str, Any]:
    flag_disabled = matrix.get(flag_name) is False
    return _decision(
        decision_name,
        decision_type="disabled_boundary_policy",
        source_validation_row_refs=["safety_boundary_validation_row"],
        source_validation_contract_refs=[contract_ref],
        source_validation_check_refs=[check_ref],
        expected={flag_name: False},
        observed={flag_name: matrix.get(flag_name)},
        policy_notes=[
            f"{flag_name} must remain false in policy-gate-only metadata",
        ],
        blocking_reasons=[]
        if flag_disabled
        else [f"{flag_name} must remain false"],
    )


def _decision(
    decision_name: str,
    *,
    decision_type: str,
    source_validation_row_refs: Sequence[str],
    source_validation_contract_refs: Sequence[str],
    source_validation_check_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    policy_notes: Sequence[str],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    decision: dict[str, Any] = {
        "decision_name": decision_name,
        "decision_type": decision_type,
        "decision_status": "pass" if not blocking_reasons else "blocked",
        "source_validation_row_refs": list(source_validation_row_refs),
        "source_validation_contract_refs": list(source_validation_contract_refs),
        "source_validation_check_refs": list(source_validation_check_refs),
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "policy_notes": list(policy_notes),
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(decision)


def _contract(
    contract_name: str,
    *,
    contract_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    contract: dict[str, Any] = {
        "contract_name": contract_name,
        "contract_type": contract_type,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "contract_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(contract)


def _check(
    check_name: str,
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    check: dict[str, Any] = {
        "check_name": check_name,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "check_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(check)


def _simple_check(
    check_name: str,
    expected: bool | str,
    observed: bool | str,
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _decision_status_contract(
    contract_name: str,
    decision_name: str,
    decisions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    decision_status = _decision_status(decisions, decision_name)
    return _contract(
        contract_name,
        contract_type="policy_decision_status_contract",
        expected={"decision_name": decision_name, "decision_status": "pass"},
        observed={"decision_name": decision_name, "decision_status": decision_status},
        blocking_reasons=[]
        if decision_status == "pass"
        else [f"{decision_name} must pass"],
    )


def _decision_status_check(
    check_name: str,
    decision_name: str,
    decisions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    decision_status = _decision_status(decisions, decision_name)
    return _check(
        check_name,
        expected={"decision_name": decision_name, "decision_status": "pass"},
        observed={"decision_name": decision_name, "decision_status": decision_status},
        blocking_reasons=[]
        if decision_status == "pass"
        else [f"{decision_name} must pass"],
    )


def _unknown_decision(name: str) -> dict[str, Any]:
    return _decision(
        name,
        decision_type="unknown_manifest_policy_decision",
        source_validation_row_refs=[],
        source_validation_contract_refs=[],
        source_validation_check_refs=[],
        expected={"known_decision_name": True},
        observed={"known_decision_name": False, "requested_decision_name": name},
        policy_notes=[],
        blocking_reasons=[
            "execution adapter manifest policy decision name is not recognized"
        ],
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _contract(
        name,
        contract_type="unknown_contract",
        expected={"known_contract_name": True},
        observed={
            "known_contract_name": False,
            "requested_contract_name": name,
        },
        blocking_reasons=[
            "execution adapter manifest policy contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter manifest policy check name is not recognized"
        ],
    )


def _manifest_policy_gate_summary(
    decisions: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_decisions = _blocked_decision_names(decisions)
    blocked_contracts = _blocked_contract_names(contracts)
    blocked_checks = _blocked_check_names(checks)
    return _detached_json_value(
        {
            "decision_count": len(decisions),
            "decision_pass_count": len(decisions) - len(blocked_decisions),
            "decision_blocked_count": len(blocked_decisions),
            "blocked_decision_names": blocked_decisions,
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "manifest_policy_gate_mode": MANIFEST_POLICY_GATE_MODE,
            "manifest_policy_gate_stage": (
                EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "raw_validation_matrix_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "executable_command_included": False,
            "live_endpoint_included": False,
            "manifest_policy_gate_summary_status": (
                "safe"
                if not blocked_decisions
                and not blocked_contracts
                and not blocked_checks
                else "blocked"
            ),
        }
    )


def _manifest_validation_matrix_passes(matrix: Mapping[str, Any]) -> bool:
    return (
        matrix.get("manifest_validation_matrix_status") == "pass"
        and matrix.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION
        and _is_sha256(
            _string_or_none(
                matrix.get("deterministic_manifest_validation_matrix_hash")
            )
        )
    )


def _manifest_validation_matrix_blocking_reasons(
    matrix: Mapping[str, Any],
) -> list[str]:
    matrix_hash = _string_or_none(
        matrix.get("deterministic_manifest_validation_matrix_hash")
    )
    return _deduplicate(
        [
            *(
                ["manifest validation matrix status must pass"]
                if matrix.get("manifest_validation_matrix_status") != "pass"
                else []
            ),
            *(
                ["manifest validation matrix version must equal 6.5.0"]
                if matrix.get("version")
                != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION
                else []
            ),
            *(
                ["manifest validation matrix hash must be present"]
                if not _is_sha256(matrix_hash)
                else []
            ),
        ]
    )


def _all_safety_boundaries_false(matrix: Mapping[str, Any]) -> bool:
    boundaries = matrix.get("safety_boundaries")
    if not isinstance(boundaries, Mapping):
        return False
    return all(boundaries.get(key) is False for key in SAFETY_BOUNDARIES) and all(
        matrix.get(key) is False for key in COMMON_DISABLED_FLAGS
    )


def _manifest_validation_rows(matrix: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = matrix.get("manifest_validation_rows")
    return [row for row in rows if isinstance(row, Mapping)] if isinstance(rows, list) else []


def _manifest_validation_contracts(
    matrix: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    contracts = matrix.get("manifest_validation_contracts")
    return (
        [contract for contract in contracts if isinstance(contract, Mapping)]
        if isinstance(contracts, list)
        else []
    )


def _manifest_validation_checks(matrix: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    checks = matrix.get("manifest_validation_checks")
    return (
        [check for check in checks if isinstance(check, Mapping)]
        if isinstance(checks, list)
        else []
    )


def _validation_row_names(matrix: Mapping[str, Any]) -> list[str]:
    return [
        row["row_name"]
        for row in _manifest_validation_rows(matrix)
        if isinstance(row.get("row_name"), str)
    ]


def _validation_contract_names(matrix: Mapping[str, Any]) -> list[str]:
    return [
        contract["contract_name"]
        for contract in _manifest_validation_contracts(matrix)
        if isinstance(contract.get("contract_name"), str)
    ]


def _validation_check_names(matrix: Mapping[str, Any]) -> list[str]:
    return [
        check["check_name"]
        for check in _manifest_validation_checks(matrix)
        if isinstance(check.get("check_name"), str)
    ]


def _validation_row_statuses(matrix: Mapping[str, Any]) -> dict[str, str]:
    return {
        row["row_name"]: _status_or_blocked(row.get("row_status"))
        for row in _manifest_validation_rows(matrix)
        if isinstance(row.get("row_name"), str)
    }


def _validation_contract_statuses(matrix: Mapping[str, Any]) -> dict[str, str]:
    return {
        contract["contract_name"]: _status_or_blocked(
            contract.get("contract_status")
        )
        for contract in _manifest_validation_contracts(matrix)
        if isinstance(contract.get("contract_name"), str)
    }


def _validation_check_statuses(matrix: Mapping[str, Any]) -> dict[str, str]:
    return {
        check["check_name"]: _status_or_blocked(check.get("check_status"))
        for check in _manifest_validation_checks(matrix)
        if isinstance(check.get("check_name"), str)
    }


def _named_statuses(
    values: Sequence[Mapping[str, Any]],
    name_key: str,
    status_key: str,
    names: Sequence[str],
) -> dict[str, str]:
    found = {
        value[name_key]: _status_or_blocked(value.get(status_key))
        for value in values
        if isinstance(value.get(name_key), str)
    }
    return {name: found.get(name, "blocked") for name in names}


def _decision_names(decisions: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        decision["decision_name"]
        for decision in decisions
        if isinstance(decision.get("decision_name"), str)
    ]


def _missing_decision_names(decision_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in REQUIRED_MANIFEST_POLICY_DECISION_NAMES
        if name not in decision_names
    ]


def _extra_decision_names(decision_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in decision_names
        if name not in REQUIRED_MANIFEST_POLICY_DECISION_NAMES
    ]


def _decision_name_blocking_reasons(decision_names: Sequence[str]) -> list[str]:
    return _deduplicate(
        [
            *(
                ["manifest policy decision names must be complete"]
                if _missing_decision_names(decision_names)
                else []
            ),
            *(
                ["manifest policy decision names must not include extras"]
                if _extra_decision_names(decision_names)
                else []
            ),
        ]
    )


def _decisions_pass(decisions: Sequence[Mapping[str, Any]]) -> bool:
    return all(decision.get("decision_status") == "pass" for decision in decisions)


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return all(contract.get("contract_status") == "pass" for contract in contracts)


def _decision_status(
    decisions: Sequence[Mapping[str, Any]],
    decision_name: str,
) -> str:
    for decision in decisions:
        if decision.get("decision_name") == decision_name:
            return _status_or_blocked(decision.get("decision_status"))
    return "blocked"


def _blocked_decision_names(decisions: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(decision.get("decision_name")) or "unknown"
        for decision in decisions
        if decision.get("decision_status") != "pass"
    ]


def _blocked_contract_names(contracts: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(contract.get("contract_name")) or "unknown"
        for contract in contracts
        if contract.get("contract_status") != "pass"
    ]


def _blocked_check_names(checks: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(check.get("check_name")) or "unknown"
        for check in checks
        if check.get("check_status") != "pass"
    ]


def _status_or_blocked(value: Any) -> str:
    return value if value in {"pass", "blocked"} else "blocked"


def _execution_adapter_manifest_policy_gate_hash(
    gate: Mapping[str, Any],
) -> str:
    hash_input = {field: gate[field] for field in _MANIFEST_POLICY_GATE_HASH_FIELDS}
    return _hash_json_value(hash_input)


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        _detached_json_value(value),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            _reject_non_finite(value),
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _reject_non_finite(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError("mapping keys must be strings")
        return {key: _reject_non_finite(value[key]) for key in value}
    if isinstance(value, list):
        return [_reject_non_finite(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("floats must be finite")
        return value
    raise ValueError("value must be deterministic JSON-compatible")


def _is_sha256(value: str | None) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _deduplicate(values: Sequence[str] | Any) -> list[str]:
    return list(dict.fromkeys(list(values)))


__all__ = [
    "EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION",
    "MANIFEST_POLICY_GATE_MODE",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_manifest_policy_gate",
    "get_governance_execution_adapter_manifest_policy_check",
    "get_governance_execution_adapter_manifest_policy_contract",
    "get_governance_execution_adapter_manifest_policy_decision",
    "governance_execution_adapter_manifest_policy_gate_to_json",
    "list_governance_execution_adapter_manifest_policy_check_names",
    "list_governance_execution_adapter_manifest_policy_contract_names",
    "list_governance_execution_adapter_manifest_policy_decision_names",
]
