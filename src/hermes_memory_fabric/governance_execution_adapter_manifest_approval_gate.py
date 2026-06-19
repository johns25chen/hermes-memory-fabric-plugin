"""Deterministic manifest approval-gate metadata for future adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_manifest_policy_gate import (
    build_governance_execution_adapter_manifest_policy_gate,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION = "5.13.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_SCHEMA_VERSION = "5.13.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_TYPE = (
    "governance_execution_adapter_manifest_approval_gate"
)
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE = (
    "v5.6_execution_adapter_manifest_approval_gate_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
MANIFEST_APPROVAL_GATE_MODE = "approval_gate_only"

READY_HANDOFF_STATUS = "ready_for_future_execution_authorization_gate_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_APPROVAL_ROLE_NAMES = (
    "governance_owner_review",
    "safety_boundary_review",
    "manifest_policy_review",
    "execution_adapter_boundary_review",
    "star_cosmos_candidate_review",
)

REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES = (
    "manifest_policy_gate_pass_evidence",
    "deterministic_policy_gate_hash_evidence",
    "sanitized_payload_evidence",
    "candidate_only_boundary_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_durable_write_evidence",
    "no_memory_graph_mutation_evidence",
    "no_operation_ledger_write_evidence",
    "no_star_cosmos_active_entry_evidence",
)

REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES = (
    "policy_gate_blocked",
    "missing_policy_gate_hash",
    "unsafe_payload_evidence",
    "candidate_only_boundary_missing",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "star_cosmos_active_entry_claimed",
    "real_approval_record_written",
    "approval_notification_sent",
)

REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES = (
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
)

REQUIRED_MANIFEST_APPROVAL_CONTRACT_NAMES = (
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
)

REQUIRED_MANIFEST_APPROVAL_CHECK_NAMES = (
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
    "approval_request_created": False,
    "approval_notification_sent": False,
    "real_approval_record_written": False,
}

_MANIFEST_APPROVAL_GATE_HASH_FIELDS = (
    "version",
    "schema_version",
    "manifest_approval_gate_type",
    "manifest_approval_gate_status",
    "manifest_approval_gate_stage",
    "manifest_approval_gate_mode",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "manifest_policy_gate_version",
    "manifest_policy_gate_status",
    "manifest_policy_gate_hash",
    "manifest_approval_request_metadata",
    "manifest_approval_gate_decisions",
    "manifest_approval_gate_contracts",
    "manifest_approval_gate_checks",
    "manifest_approval_gate_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MANIFEST_APPROVAL_GATE_HASH_FIELDS),
    "input_shape": "sanitized future execution adapter manifest approval gate projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_manifest_policy_gate_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_execution_adapter_manifest_approval_gate() -> dict[str, Any]:
    """Build deterministic approval-gate-only manifest metadata."""

    policy_gate = _detached_json_value(
        build_governance_execution_adapter_manifest_policy_gate()
    )
    policy_gate_repeat = _detached_json_value(
        build_governance_execution_adapter_manifest_policy_gate()
    )
    request_metadata = _build_approval_request_metadata(policy_gate)
    decisions = _build_approval_decisions(
        policy_gate,
        policy_gate_repeat,
        request_metadata,
    )
    contracts = _build_approval_contracts(
        policy_gate,
        policy_gate_repeat,
        request_metadata,
        decisions,
    )
    checks = _build_approval_checks(
        policy_gate,
        policy_gate_repeat,
        request_metadata,
        decisions,
        contracts,
    )

    policy_gate_passes = _manifest_policy_gate_passes(policy_gate)
    request_metadata_valid = _approval_request_metadata_valid(request_metadata)
    decisions_pass = _decisions_pass(decisions)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    approval_gate_status = (
        "pass"
        if policy_gate_passes
        and request_metadata_valid
        and decisions_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["manifest policy gate must pass at version 5.13.0"]
                if not policy_gate_passes
                else []
            ),
            *(
                ["approval request metadata must remain metadata-only"]
                if not request_metadata_valid
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
        "version": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_SCHEMA_VERSION
        ),
        "manifest_approval_gate_type": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_TYPE
        ),
        "manifest_approval_gate_status": approval_gate_status,
        "manifest_approval_gate_stage": (
            EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE
        ),
        "manifest_approval_gate_mode": MANIFEST_APPROVAL_GATE_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "manifest_policy_gate_version": _string_or_none(policy_gate.get("version")),
        "manifest_policy_gate_status": _string_or_none(
            policy_gate.get("manifest_policy_gate_status")
        ),
        "manifest_policy_gate_hash": _string_or_none(
            policy_gate.get("deterministic_manifest_policy_gate_hash")
        ),
        "manifest_approval_request_metadata": request_metadata,
        "manifest_approval_gate_decisions": decisions,
        "manifest_approval_gate_contracts": contracts,
        "manifest_approval_gate_checks": checks,
        "manifest_approval_gate_summary": _manifest_approval_gate_summary(
            request_metadata,
            decisions,
            contracts,
            checks,
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if approval_gate_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    gate["deterministic_manifest_approval_gate_hash"] = (
        _execution_adapter_manifest_approval_gate_hash(gate)
    )
    return _detached_json_value(gate)


def get_governance_execution_adapter_manifest_approval_decision(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest approval decision by stable name."""

    if not isinstance(name, str):
        return _unknown_decision("")
    if name not in REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES:
        return _unknown_decision(name)
    gate = _cached_manifest_approval_gate()
    for decision in gate["manifest_approval_gate_decisions"]:
        if decision["decision_name"] == name:
            return _detached_json_value(decision)
    return _unknown_decision(name)


def get_governance_execution_adapter_manifest_approval_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest approval contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_MANIFEST_APPROVAL_CONTRACT_NAMES:
        return _unknown_contract(name)
    gate = _cached_manifest_approval_gate()
    for contract in gate["manifest_approval_gate_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_manifest_approval_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest approval check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_MANIFEST_APPROVAL_CHECK_NAMES:
        return _unknown_check(name)
    gate = _cached_manifest_approval_gate()
    for check in gate["manifest_approval_gate_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_manifest_approval_decision_names() -> list[str]:
    """Return stable manifest approval decision names."""

    return list(REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES)


def list_governance_execution_adapter_manifest_approval_contract_names() -> list[str]:
    """Return stable manifest approval contract names."""

    return list(REQUIRED_MANIFEST_APPROVAL_CONTRACT_NAMES)


def list_governance_execution_adapter_manifest_approval_check_names() -> list[str]:
    """Return stable manifest approval check names."""

    return list(REQUIRED_MANIFEST_APPROVAL_CHECK_NAMES)


def governance_execution_adapter_manifest_approval_gate_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize manifest approval-gate metadata deterministically."""

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


@lru_cache(maxsize=1)
def _cached_manifest_approval_gate_payload() -> str:
    return governance_execution_adapter_manifest_approval_gate_to_json(
        build_governance_execution_adapter_manifest_approval_gate()
    )


def _cached_manifest_approval_gate() -> dict[str, Any]:
    return json.loads(_cached_manifest_approval_gate_payload())


def _build_approval_request_metadata(
    policy_gate: Mapping[str, Any],
) -> dict[str, Any]:
    policy_gate_passes = _manifest_policy_gate_passes(policy_gate)
    policy_gate_hash = _string_or_none(
        policy_gate.get("deterministic_manifest_policy_gate_hash")
    )
    metadata_valid = policy_gate_passes and _is_sha256(policy_gate_hash)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "approval_request_type": (
                "future_execution_adapter_manifest_approval_request_metadata"
            ),
            "approval_request_mode": "metadata_only",
            "approval_request_status": "not_created",
            "approval_required": True,
            "real_approval_record_written": False,
            "approval_notification_sent": False,
            "approval_request_created": False,
            "candidate_only": True,
            "execution_authorized": False,
            "adapter_invocation_authorized": False,
            "manifest_execution_authorized": False,
            "dry_run_plan_execution_authorized": False,
            "required_approval_roles": list(REQUIRED_APPROVAL_ROLE_NAMES),
            "approval_evidence_requirements": list(
                REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES
            ),
            "approval_blocking_conditions": list(
                REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES
            ),
            "approval_handoff_status": (
                READY_HANDOFF_STATUS if metadata_valid else BLOCKED_HANDOFF_STATUS
            ),
            "manifest_policy_gate_status": _string_or_none(
                policy_gate.get("manifest_policy_gate_status")
            ),
            "manifest_policy_gate_version": _string_or_none(policy_gate.get("version")),
            "manifest_policy_gate_hash_present": _is_sha256(policy_gate_hash),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_approval_decisions(
    policy_gate: Mapping[str, Any],
    policy_gate_repeat: Mapping[str, Any],
    request_metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    policy_hash = _string_or_none(
        policy_gate.get("deterministic_manifest_policy_gate_hash")
    )
    repeat_hash = _string_or_none(
        policy_gate_repeat.get("deterministic_manifest_policy_gate_hash")
    )
    policy_hash_present = _is_sha256(policy_hash)
    policy_hash_stable = policy_hash_present and policy_hash == repeat_hash
    return [
        _decision(
            "policy_gate_pass_approval_decision",
            decision_type="upstream_manifest_policy_gate_approval",
            source_policy_decision_refs=[
                "validation_matrix_pass_policy_decision",
                "policy_decisions_pass_contract",
            ],
            source_policy_contract_refs=[
                "manifest_validation_matrix_pass_contract",
                "policy_decisions_pass_contract",
            ],
            source_policy_check_refs=[
                "manifest_validation_matrix_pass_check",
                "policy_handoff_readiness_check",
            ],
            expected={
                "manifest_policy_gate_status": "pass",
                "manifest_policy_gate_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION
                ),
                "manifest_policy_gate_hash_present": True,
            },
            observed={
                "manifest_policy_gate_status": _string_or_none(
                    policy_gate.get("manifest_policy_gate_status")
                ),
                "manifest_policy_gate_version": _string_or_none(
                    policy_gate.get("version")
                ),
                "manifest_policy_gate_hash_present": policy_hash_present,
            },
            approval_notes=[
                "approval gate can evaluate only a passing local policy gate",
                "upstream policy gate payload remains outside the approval hash",
            ],
            blocking_reasons=_manifest_policy_gate_blocking_reasons(policy_gate),
        ),
        _decision(
            "policy_gate_hash_approval_decision",
            decision_type="policy_gate_hash_approval",
            source_policy_decision_refs=["deterministic_hash_policy_decision"],
            source_policy_contract_refs=[
                "validation_matrix_hash_present_contract",
                "validation_matrix_hash_stable_contract",
            ],
            source_policy_check_refs=[
                "validation_matrix_hash_present_check",
                "validation_matrix_hash_stable_check",
                "deterministic_policy_gate_hash_check",
            ],
            expected={
                "manifest_policy_gate_hash_present": True,
                "manifest_policy_gate_hash_stable": True,
            },
            observed={
                "manifest_policy_gate_hash_present": policy_hash_present,
                "manifest_policy_gate_hash_stable": policy_hash_stable,
            },
            approval_notes=[
                "approval request metadata requires a stable upstream policy hash",
            ],
            blocking_reasons=[]
            if policy_hash_present and policy_hash_stable
            else ["manifest policy gate hash must be present and stable"],
        ),
        _metadata_decision(
            request_metadata,
            "approval_request_metadata_only_decision",
            decision_type="approval_request_metadata_policy",
            expected={
                "approval_request_mode": "metadata_only",
                "approval_request_status": "not_created",
                "approval_request_created": False,
                "execution_authorized": False,
            },
            observed={
                "approval_request_mode": request_metadata.get(
                    "approval_request_mode"
                ),
                "approval_request_status": request_metadata.get(
                    "approval_request_status"
                ),
                "approval_request_created": request_metadata.get(
                    "approval_request_created"
                ),
                "execution_authorized": request_metadata.get(
                    "execution_authorized"
                ),
            },
            approval_notes=[
                "approval request details are metadata only and not created",
            ],
        ),
        _metadata_list_decision(
            request_metadata,
            "approval_roles_declared_decision",
            decision_type="approval_role_metadata_policy",
            metadata_key="required_approval_roles",
            expected_values=REQUIRED_APPROVAL_ROLE_NAMES,
            approval_notes=["generic approval role labels must be complete"],
        ),
        _metadata_list_decision(
            request_metadata,
            "approval_evidence_requirements_declared_decision",
            decision_type="approval_evidence_metadata_policy",
            metadata_key="approval_evidence_requirements",
            expected_values=REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES,
            approval_notes=[
                "approval evidence requirement labels must be complete",
            ],
        ),
        _metadata_list_decision(
            request_metadata,
            "approval_blocking_conditions_declared_decision",
            decision_type="approval_blocking_condition_metadata_policy",
            metadata_key="approval_blocking_conditions",
            expected_values=REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES,
            approval_notes=["approval blocking condition labels must be complete"],
        ),
        _source_policy_decision(
            policy_gate,
            "sanitized_payload_approval_decision",
            decision_type="sanitized_payload_approval",
            source_decision_name="sanitized_payload_policy_decision",
            source_contract_name="sanitized_payload_policy_contract",
            source_check_name="sanitized_payload_policy_check",
            approval_notes=[
                "approval metadata depends on sanitized policy payload evidence",
            ],
        ),
        _source_policy_decision(
            policy_gate,
            "candidate_only_approval_decision",
            decision_type="candidate_only_approval",
            source_decision_name="candidate_only_policy_decision",
            source_contract_name="candidate_only_policy_contract",
            source_check_name="candidate_only_policy_check",
            approval_notes=[
                "approval metadata requires candidate-only boundary evidence",
            ],
        ),
        _disabled_flag_decision(
            "no_real_execution_approval_decision",
            "real_execution_enabled",
            "no_real_execution_policy_decision",
            "no_real_execution_policy_contract",
            "no_real_execution_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_adapter_invocation_approval_decision",
            "execution_adapter_invoked",
            "no_adapter_invocation_policy_decision",
            "no_adapter_invocation_policy_contract",
            "no_adapter_invocation_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_manifest_execution_approval_decision",
            "manifest_executed",
            "no_manifest_execution_policy_decision",
            "no_manifest_execution_policy_contract",
            "no_manifest_execution_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_dry_run_plan_execution_approval_decision",
            "dry_run_plan_executed",
            "no_dry_run_plan_execution_policy_decision",
            "no_dry_run_plan_execution_policy_contract",
            "no_dry_run_plan_execution_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_external_call_approval_decision",
            "external_calls_enabled",
            "no_external_call_policy_decision",
            "no_external_call_policy_contract",
            "no_external_call_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_durable_write_approval_decision",
            "durable_writes_enabled",
            "no_durable_write_policy_decision",
            "no_durable_write_policy_contract",
            "no_durable_write_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_filesystem_write_approval_decision",
            "filesystem_writes_enabled",
            "no_filesystem_write_policy_decision",
            "no_filesystem_write_policy_contract",
            "no_filesystem_write_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_database_write_approval_decision",
            "database_writes_enabled",
            "no_database_write_policy_decision",
            "no_database_write_policy_contract",
            "no_database_write_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_memory_graph_mutation_approval_decision",
            "memory_graph_mutation_enabled",
            "no_memory_graph_mutation_policy_decision",
            "no_memory_graph_mutation_policy_contract",
            "no_memory_graph_mutation_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_operation_ledger_write_approval_decision",
            "operation_ledger_writes_enabled",
            "no_operation_ledger_write_policy_decision",
            "no_operation_ledger_write_policy_contract",
            "no_operation_ledger_write_policy_check",
            policy_gate,
            request_metadata,
        ),
        _disabled_flag_decision(
            "no_autonomous_execution_approval_decision",
            "autonomous_execution_enabled",
            "no_autonomous_execution_policy_decision",
            "no_autonomous_execution_policy_contract",
            "no_autonomous_execution_policy_check",
            policy_gate,
            request_metadata,
        ),
        _metadata_decision(
            request_metadata,
            "no_real_approval_record_write_decision",
            decision_type="real_approval_record_write_approval",
            expected={"real_approval_record_written": False},
            observed={
                "real_approval_record_written": request_metadata.get(
                    "real_approval_record_written"
                )
            },
            approval_notes=[
                "approval gate metadata does not write real approval records",
            ],
            source_policy_decision_refs=["no_durable_write_policy_decision"],
            source_policy_contract_refs=["no_durable_write_policy_contract"],
            source_policy_check_refs=["no_durable_write_policy_check"],
        ),
        _metadata_decision(
            request_metadata,
            "no_approval_notification_decision",
            decision_type="approval_notification_approval",
            expected={"approval_notification_sent": False},
            observed={
                "approval_notification_sent": request_metadata.get(
                    "approval_notification_sent"
                )
            },
            approval_notes=[
                "approval gate metadata does not send approval notifications",
            ],
            source_policy_decision_refs=["no_external_call_policy_decision"],
            source_policy_contract_refs=["no_external_call_policy_contract"],
            source_policy_check_refs=["no_external_call_policy_check"],
        ),
        _decision(
            "star_cosmos_candidate_only_approval_decision",
            decision_type="star_cosmos_candidate_only_approval",
            source_policy_decision_refs=[
                "star_cosmos_candidate_only_policy_decision",
                "candidate_only_policy_decision",
            ],
            source_policy_contract_refs=[
                "star_cosmos_candidate_only_policy_contract",
                "candidate_only_policy_contract",
            ],
            source_policy_check_refs=[
                "star_cosmos_candidate_only_policy_check",
                "candidate_only_policy_check",
            ],
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "candidate_only": True,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": request_metadata.get(
                    "star_cosmos_memory_active"
                ),
                "candidate_only": request_metadata.get("candidate_only"),
            },
            approval_notes=[
                "Star-Cosmos remains candidate-only in approval gate metadata",
            ],
            blocking_reasons=[]
            if request_metadata.get("star_cosmos_memory_active") is False
            and request_metadata.get("candidate_only") is True
            else ["Star-Cosmos candidate-only boundary must remain false-active"],
        ),
    ]


def _build_approval_contracts(
    policy_gate: Mapping[str, Any],
    policy_gate_repeat: Mapping[str, Any],
    request_metadata: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    decision_names = _decision_names(decisions)
    policy_hash = _string_or_none(
        policy_gate.get("deterministic_manifest_policy_gate_hash")
    )
    repeat_hash = _string_or_none(
        policy_gate_repeat.get("deterministic_manifest_policy_gate_hash")
    )
    return [
        _contract(
            "approval_gate_only_contract",
            contract_type="approval_gate_mode_contract",
            expected={
                "manifest_approval_gate_mode": MANIFEST_APPROVAL_GATE_MODE,
                "approval_request_created": False,
                "approval_notification_sent": False,
                "real_approval_record_written": False,
            },
            observed={
                "manifest_approval_gate_mode": MANIFEST_APPROVAL_GATE_MODE,
                "approval_request_created": False,
                "approval_notification_sent": False,
                "real_approval_record_written": False,
            },
        ),
        _contract(
            "manifest_policy_gate_pass_contract",
            contract_type="upstream_manifest_policy_gate_contract",
            expected={
                "manifest_policy_gate_status": "pass",
                "manifest_policy_gate_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION
                ),
                "manifest_policy_gate_hash_present": True,
            },
            observed={
                "manifest_policy_gate_status": _string_or_none(
                    policy_gate.get("manifest_policy_gate_status")
                ),
                "manifest_policy_gate_version": _string_or_none(
                    policy_gate.get("version")
                ),
                "manifest_policy_gate_hash_present": _is_sha256(policy_hash),
            },
            blocking_reasons=_manifest_policy_gate_blocking_reasons(policy_gate),
        ),
        _metadata_contract(
            "approval_request_metadata_only_contract",
            request_metadata,
            expected={
                "approval_request_mode": "metadata_only",
                "approval_request_status": "not_created",
                "approval_request_created": False,
            },
            observed={
                "approval_request_mode": request_metadata.get(
                    "approval_request_mode"
                ),
                "approval_request_status": request_metadata.get(
                    "approval_request_status"
                ),
                "approval_request_created": request_metadata.get(
                    "approval_request_created"
                ),
            },
        ),
        _metadata_list_contract(
            "approval_roles_declared_contract",
            "required_approval_roles",
            REQUIRED_APPROVAL_ROLE_NAMES,
            request_metadata,
        ),
        _metadata_list_contract(
            "approval_evidence_requirements_declared_contract",
            "approval_evidence_requirements",
            REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES,
            request_metadata,
        ),
        _metadata_list_contract(
            "approval_blocking_conditions_declared_contract",
            "approval_blocking_conditions",
            REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES,
            request_metadata,
        ),
        _contract(
            "approval_decision_names_complete_contract",
            contract_type="approval_decision_name_contract",
            expected={
                "decision_names": list(REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES),
                "decision_count": len(REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES),
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
            "approval_decisions_pass_contract",
            contract_type="approval_decision_status_contract",
            expected={"approval_decisions_pass": True, "blocked_decision_count": 0},
            observed={
                "approval_decisions_pass": _decisions_pass(decisions),
                "blocked_decision_count": len(_blocked_decision_names(decisions)),
                "blocked_decision_names": _blocked_decision_names(decisions),
            },
            blocking_reasons=[]
            if _decisions_pass(decisions)
            else ["manifest approval decisions must pass"],
        ),
        _contract(
            "policy_gate_hash_present_contract",
            contract_type="policy_gate_hash_contract",
            expected={"manifest_policy_gate_hash_present": True},
            observed={"manifest_policy_gate_hash_present": _is_sha256(policy_hash)},
            blocking_reasons=[]
            if _is_sha256(policy_hash)
            else ["manifest policy gate hash must be present"],
        ),
        _contract(
            "policy_gate_hash_stable_contract",
            contract_type="policy_gate_hash_contract",
            expected={"manifest_policy_gate_hash_stable": True},
            observed={
                "manifest_policy_gate_hash_stable": _is_sha256(policy_hash)
                and policy_hash == repeat_hash
            },
            blocking_reasons=[]
            if _is_sha256(policy_hash) and policy_hash == repeat_hash
            else ["manifest policy gate hash must be stable"],
        ),
        _decision_status_contract(
            "sanitized_payload_approval_contract",
            "sanitized_payload_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "candidate_only_approval_contract",
            "candidate_only_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_real_execution_approval_contract",
            "no_real_execution_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_adapter_invocation_approval_contract",
            "no_adapter_invocation_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_manifest_execution_approval_contract",
            "no_manifest_execution_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_dry_run_plan_execution_approval_contract",
            "no_dry_run_plan_execution_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_external_call_approval_contract",
            "no_external_call_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_durable_write_approval_contract",
            "no_durable_write_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_filesystem_write_approval_contract",
            "no_filesystem_write_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_database_write_approval_contract",
            "no_database_write_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_memory_graph_mutation_approval_contract",
            "no_memory_graph_mutation_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_operation_ledger_write_approval_contract",
            "no_operation_ledger_write_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_autonomous_execution_approval_contract",
            "no_autonomous_execution_approval_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_real_approval_record_write_contract",
            "no_real_approval_record_write_decision",
            decisions,
        ),
        _decision_status_contract(
            "no_approval_notification_contract",
            "no_approval_notification_decision",
            decisions,
        ),
        _decision_status_contract(
            "star_cosmos_candidate_only_approval_contract",
            "star_cosmos_candidate_only_approval_decision",
            decisions,
        ),
    ]


def _build_approval_checks(
    policy_gate: Mapping[str, Any],
    policy_gate_repeat: Mapping[str, Any],
    request_metadata: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    decision_names = _decision_names(decisions)
    policy_hash = _string_or_none(
        policy_gate.get("deterministic_manifest_policy_gate_hash")
    )
    repeat_hash = _string_or_none(
        policy_gate_repeat.get("deterministic_manifest_policy_gate_hash")
    )
    checks = [
        _check(
            "manifest_policy_gate_pass_check",
            expected={
                "manifest_policy_gate_status": "pass",
                "manifest_policy_gate_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION
                ),
                "manifest_policy_gate_hash_present": True,
            },
            observed={
                "manifest_policy_gate_status": _string_or_none(
                    policy_gate.get("manifest_policy_gate_status")
                ),
                "manifest_policy_gate_version": _string_or_none(
                    policy_gate.get("version")
                ),
                "manifest_policy_gate_hash_present": _is_sha256(policy_hash),
            },
            blocking_reasons=_manifest_policy_gate_blocking_reasons(policy_gate),
        ),
        _simple_check(
            "manifest_approval_gate_stage_check",
            EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE,
            EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE,
        ),
        _simple_check(
            "approval_gate_only_mode_check",
            MANIFEST_APPROVAL_GATE_MODE,
            MANIFEST_APPROVAL_GATE_MODE,
        ),
        _metadata_check(
            "approval_request_metadata_only_check",
            request_metadata,
            expected={
                "approval_request_mode": "metadata_only",
                "approval_request_status": "not_created",
                "approval_request_created": False,
            },
            observed={
                "approval_request_mode": request_metadata.get(
                    "approval_request_mode"
                ),
                "approval_request_status": request_metadata.get(
                    "approval_request_status"
                ),
                "approval_request_created": request_metadata.get(
                    "approval_request_created"
                ),
            },
        ),
        _metadata_list_check(
            "approval_roles_declared_check",
            "required_approval_roles",
            REQUIRED_APPROVAL_ROLE_NAMES,
            request_metadata,
        ),
        _metadata_list_check(
            "approval_evidence_requirements_declared_check",
            "approval_evidence_requirements",
            REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES,
            request_metadata,
        ),
        _metadata_list_check(
            "approval_blocking_conditions_declared_check",
            "approval_blocking_conditions",
            REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES,
            request_metadata,
        ),
        _check(
            "approval_decision_names_complete_check",
            expected={
                "decision_names": list(REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES),
                "decision_count": len(REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES),
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
            "approval_decisions_pass_check",
            expected={"approval_decisions_pass": True, "blocked_decision_count": 0},
            observed={
                "approval_decisions_pass": _decisions_pass(decisions),
                "blocked_decision_count": len(_blocked_decision_names(decisions)),
                "blocked_decision_names": _blocked_decision_names(decisions),
            },
            blocking_reasons=[]
            if _decisions_pass(decisions)
            else ["manifest approval decisions must pass"],
        ),
        _check(
            "approval_contracts_pass_check",
            expected={"approval_contracts_pass": True, "blocked_contract_count": 0},
            observed={
                "approval_contracts_pass": _contracts_pass(contracts),
                "blocked_contract_count": len(_blocked_contract_names(contracts)),
                "blocked_contract_names": _blocked_contract_names(contracts),
            },
            blocking_reasons=[]
            if _contracts_pass(contracts)
            else ["manifest approval contracts must pass"],
        ),
        _check(
            "policy_gate_hash_present_check",
            expected={"manifest_policy_gate_hash_present": True},
            observed={"manifest_policy_gate_hash_present": _is_sha256(policy_hash)},
            blocking_reasons=[]
            if _is_sha256(policy_hash)
            else ["manifest policy gate hash must be present"],
        ),
        _check(
            "policy_gate_hash_stable_check",
            expected={"manifest_policy_gate_hash_stable": True},
            observed={
                "manifest_policy_gate_hash_stable": _is_sha256(policy_hash)
                and policy_hash == repeat_hash
            },
            blocking_reasons=[]
            if _is_sha256(policy_hash) and policy_hash == repeat_hash
            else ["manifest policy gate hash must be stable"],
        ),
        _decision_status_check(
            "sanitized_payload_approval_check",
            "sanitized_payload_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "candidate_only_approval_check",
            "candidate_only_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_real_execution_approval_check",
            "no_real_execution_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_adapter_invocation_approval_check",
            "no_adapter_invocation_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_manifest_execution_approval_check",
            "no_manifest_execution_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_dry_run_plan_execution_approval_check",
            "no_dry_run_plan_execution_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_external_call_approval_check",
            "no_external_call_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_durable_write_approval_check",
            "no_durable_write_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_filesystem_write_approval_check",
            "no_filesystem_write_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_database_write_approval_check",
            "no_database_write_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_memory_graph_mutation_approval_check",
            "no_memory_graph_mutation_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_operation_ledger_write_approval_check",
            "no_operation_ledger_write_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_autonomous_execution_approval_check",
            "no_autonomous_execution_approval_decision",
            decisions,
        ),
        _decision_status_check(
            "no_real_approval_record_write_check",
            "no_real_approval_record_write_decision",
            decisions,
        ),
        _decision_status_check(
            "no_approval_notification_check",
            "no_approval_notification_decision",
            decisions,
        ),
        _decision_status_check(
            "star_cosmos_candidate_only_approval_check",
            "star_cosmos_candidate_only_approval_decision",
            decisions,
        ),
        _check(
            "deterministic_approval_gate_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM
                ),
                "request_decision_contract_check_data_in_hash": True,
            },
            observed={
                "hash_algorithm": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM
                ),
                "request_decision_contract_check_data_in_hash": all(
                    field in _MANIFEST_APPROVAL_GATE_HASH_FIELDS
                    for field in (
                        "manifest_approval_request_metadata",
                        "manifest_approval_gate_decisions",
                        "manifest_approval_gate_contracts",
                        "manifest_approval_gate_checks",
                    )
                ),
            },
            blocking_reasons=[]
            if all(
                field in _MANIFEST_APPROVAL_GATE_HASH_FIELDS
                for field in (
                    "manifest_approval_request_metadata",
                    "manifest_approval_gate_decisions",
                    "manifest_approval_gate_contracts",
                    "manifest_approval_gate_checks",
                )
            )
            else [
                "approval gate hash must include request, decision, contract, and check data"
            ],
        ),
    ]
    component_checks_pass = all(check["check_status"] == "pass" for check in checks)
    checks.append(
        _check(
            "approval_handoff_readiness_check",
            expected={
                "manifest_policy_gate_passes": True,
                "approval_request_metadata_valid": True,
                "approval_decisions_pass": True,
                "approval_contracts_pass": True,
                "component_approval_checks_pass": True,
            },
            observed={
                "manifest_policy_gate_passes": (
                    _manifest_policy_gate_passes(policy_gate)
                ),
                "approval_request_metadata_valid": (
                    _approval_request_metadata_valid(request_metadata)
                ),
                "approval_decisions_pass": _decisions_pass(decisions),
                "approval_contracts_pass": _contracts_pass(contracts),
                "component_approval_checks_pass": component_checks_pass,
            },
            blocking_reasons=[]
            if _manifest_policy_gate_passes(policy_gate)
            and _approval_request_metadata_valid(request_metadata)
            and _decisions_pass(decisions)
            and _contracts_pass(contracts)
            and component_checks_pass
            else ["approval handoff readiness requires all approval gates to pass"],
        )
    )
    return checks


def _metadata_decision(
    request_metadata: Mapping[str, Any],
    decision_name: str,
    *,
    decision_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    approval_notes: Sequence[str],
    source_policy_decision_refs: Sequence[str] = (
        "candidate_only_policy_decision",
    ),
    source_policy_contract_refs: Sequence[str] = (
        "candidate_only_policy_contract",
    ),
    source_policy_check_refs: Sequence[str] = ("candidate_only_policy_check",),
) -> dict[str, Any]:
    metadata_valid = _approval_request_metadata_valid(request_metadata)
    observed_matches = _observed_matches_expected(expected, observed)
    return _decision(
        decision_name,
        decision_type=decision_type,
        source_policy_decision_refs=source_policy_decision_refs,
        source_policy_contract_refs=source_policy_contract_refs,
        source_policy_check_refs=source_policy_check_refs,
        expected=expected,
        observed=observed,
        approval_notes=approval_notes,
        blocking_reasons=[]
        if metadata_valid and observed_matches
        else [f"{decision_name} must remain metadata-only"],
    )


def _metadata_list_decision(
    request_metadata: Mapping[str, Any],
    decision_name: str,
    *,
    decision_type: str,
    metadata_key: str,
    expected_values: Sequence[str],
    approval_notes: Sequence[str],
) -> dict[str, Any]:
    observed_values = _string_list(request_metadata.get(metadata_key))
    missing_values = [value for value in expected_values if value not in observed_values]
    extra_values = [value for value in observed_values if value not in expected_values]
    return _decision(
        decision_name,
        decision_type=decision_type,
        source_policy_decision_refs=["candidate_only_policy_decision"],
        source_policy_contract_refs=["candidate_only_policy_contract"],
        source_policy_check_refs=["candidate_only_policy_check"],
        expected={
            metadata_key: list(expected_values),
            "missing_values": [],
            "extra_values": [],
        },
        observed={
            metadata_key: observed_values,
            "missing_values": missing_values,
            "extra_values": extra_values,
        },
        approval_notes=approval_notes,
        blocking_reasons=[]
        if not missing_values and not extra_values
        else [f"{metadata_key} must match the approval gate contract"],
    )


def _source_policy_decision(
    policy_gate: Mapping[str, Any],
    decision_name: str,
    *,
    decision_type: str,
    source_decision_name: str,
    source_contract_name: str,
    source_check_name: str,
    approval_notes: Sequence[str],
) -> dict[str, Any]:
    policy_decision_status = _policy_decision_status(policy_gate, source_decision_name)
    policy_contract_status = _policy_contract_status(policy_gate, source_contract_name)
    policy_check_status = _policy_check_status(policy_gate, source_check_name)
    return _decision(
        decision_name,
        decision_type=decision_type,
        source_policy_decision_refs=[source_decision_name],
        source_policy_contract_refs=[source_contract_name],
        source_policy_check_refs=[source_check_name],
        expected={
            "source_policy_decision_status": "pass",
            "source_policy_contract_status": "pass",
            "source_policy_check_status": "pass",
        },
        observed={
            "source_policy_decision_status": policy_decision_status,
            "source_policy_contract_status": policy_contract_status,
            "source_policy_check_status": policy_check_status,
        },
        approval_notes=approval_notes,
        blocking_reasons=[]
        if policy_decision_status == "pass"
        and policy_contract_status == "pass"
        and policy_check_status == "pass"
        else [f"{source_decision_name} must pass before approval metadata passes"],
    )


def _disabled_flag_decision(
    decision_name: str,
    flag_name: str,
    source_decision_name: str,
    source_contract_name: str,
    source_check_name: str,
    policy_gate: Mapping[str, Any],
    request_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    policy_status = _policy_decision_status(policy_gate, source_decision_name)
    flag_disabled = (
        policy_gate.get(flag_name) is False and request_metadata.get(flag_name) is False
    )
    return _decision(
        decision_name,
        decision_type="disabled_runtime_boundary_approval",
        source_policy_decision_refs=[source_decision_name],
        source_policy_contract_refs=[source_contract_name],
        source_policy_check_refs=[source_check_name],
        expected={
            flag_name: False,
            "source_policy_decision_status": "pass",
        },
        observed={
            flag_name: request_metadata.get(flag_name),
            "policy_gate_" + flag_name: policy_gate.get(flag_name),
            "source_policy_decision_status": policy_status,
        },
        approval_notes=[
            f"{flag_name} must remain false in approval-gate-only metadata",
        ],
        blocking_reasons=[]
        if flag_disabled and policy_status == "pass"
        else [f"{flag_name} must remain false"],
    )


def _decision(
    decision_name: str,
    *,
    decision_type: str,
    source_policy_decision_refs: Sequence[str],
    source_policy_contract_refs: Sequence[str],
    source_policy_check_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    approval_notes: Sequence[str],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    decision: dict[str, Any] = {
        "decision_name": decision_name,
        "decision_type": decision_type,
        "decision_status": "pass" if not blocking_reasons else "blocked",
        "source_policy_decision_refs": list(source_policy_decision_refs),
        "source_policy_contract_refs": list(source_policy_contract_refs),
        "source_policy_check_refs": list(source_policy_check_refs),
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "approval_notes": list(approval_notes),
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
        check_name=check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _metadata_contract(
    contract_name: str,
    request_metadata: Mapping[str, Any],
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> dict[str, Any]:
    return _contract(
        contract_name,
        contract_type="approval_request_metadata_contract",
        expected=expected,
        observed=observed,
        blocking_reasons=[]
        if _approval_request_metadata_valid(request_metadata)
        and _observed_matches_expected(expected, observed)
        else [f"{contract_name} must remain metadata-only"],
    )


def _metadata_check(
    check_name: str,
    request_metadata: Mapping[str, Any],
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> dict[str, Any]:
    return _check(
        check_name,
        expected=expected,
        observed=observed,
        blocking_reasons=[]
        if _approval_request_metadata_valid(request_metadata)
        and _observed_matches_expected(expected, observed)
        else [f"{check_name} must remain metadata-only"],
    )


def _metadata_list_contract(
    contract_name: str,
    metadata_key: str,
    expected_values: Sequence[str],
    request_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    observed_values = _string_list(request_metadata.get(metadata_key))
    missing_values = [value for value in expected_values if value not in observed_values]
    extra_values = [value for value in observed_values if value not in expected_values]
    return _contract(
        contract_name,
        contract_type="approval_request_metadata_list_contract",
        expected={
            metadata_key: list(expected_values),
            "missing_values": [],
            "extra_values": [],
        },
        observed={
            metadata_key: observed_values,
            "missing_values": missing_values,
            "extra_values": extra_values,
        },
        blocking_reasons=[]
        if not missing_values and not extra_values
        else [f"{metadata_key} must match the approval gate contract"],
    )


def _metadata_list_check(
    check_name: str,
    metadata_key: str,
    expected_values: Sequence[str],
    request_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    observed_values = _string_list(request_metadata.get(metadata_key))
    missing_values = [value for value in expected_values if value not in observed_values]
    extra_values = [value for value in observed_values if value not in expected_values]
    return _check(
        check_name,
        expected={
            metadata_key: list(expected_values),
            "missing_values": [],
            "extra_values": [],
        },
        observed={
            metadata_key: observed_values,
            "missing_values": missing_values,
            "extra_values": extra_values,
        },
        blocking_reasons=[]
        if not missing_values and not extra_values
        else [f"{metadata_key} must match the approval gate contract"],
    )


def _decision_status_contract(
    contract_name: str,
    decision_name: str,
    decisions: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    decision_status = _decision_status(decisions, decision_name)
    return _contract(
        contract_name,
        contract_type="approval_decision_status_contract",
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
        decision_type="unknown_manifest_approval_decision",
        source_policy_decision_refs=[],
        source_policy_contract_refs=[],
        source_policy_check_refs=[],
        expected={"known_decision_name": True},
        observed={"known_decision_name": False, "requested_decision_name": name},
        approval_notes=[],
        blocking_reasons=[
            "execution adapter manifest approval decision name is not recognized"
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
            "execution adapter manifest approval contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter manifest approval check name is not recognized"
        ],
    )


def _manifest_approval_gate_summary(
    request_metadata: Mapping[str, Any],
    decisions: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_decisions = _blocked_decision_names(decisions)
    blocked_contracts = _blocked_contract_names(contracts)
    blocked_checks = _blocked_check_names(checks)
    return _detached_json_value(
        {
            "approval_request_metadata_status": (
                "pass"
                if _approval_request_metadata_valid(request_metadata)
                else "blocked"
            ),
            "approval_role_count": len(
                _string_list(request_metadata.get("required_approval_roles"))
            ),
            "approval_evidence_requirement_count": len(
                _string_list(
                    request_metadata.get("approval_evidence_requirements")
                )
            ),
            "approval_blocking_condition_count": len(
                _string_list(request_metadata.get("approval_blocking_conditions"))
            ),
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
            "manifest_approval_gate_mode": MANIFEST_APPROVAL_GATE_MODE,
            "manifest_approval_gate_stage": (
                EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "raw_manifest_policy_gate_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "live_endpoint_included": False,
            "manifest_approval_gate_summary_status": (
                "safe"
                if _approval_request_metadata_valid(request_metadata)
                and not blocked_decisions
                and not blocked_contracts
                and not blocked_checks
                else "blocked"
            ),
        }
    )


def _manifest_policy_gate_passes(policy_gate: Mapping[str, Any]) -> bool:
    return (
        policy_gate.get("manifest_policy_gate_status") == "pass"
        and policy_gate.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION
        and _is_sha256(
            _string_or_none(policy_gate.get("deterministic_manifest_policy_gate_hash"))
        )
    )


def _manifest_policy_gate_blocking_reasons(
    policy_gate: Mapping[str, Any],
) -> list[str]:
    policy_hash = _string_or_none(
        policy_gate.get("deterministic_manifest_policy_gate_hash")
    )
    return _deduplicate(
        [
            *(
                ["manifest policy gate status must pass"]
                if policy_gate.get("manifest_policy_gate_status") != "pass"
                else []
            ),
            *(
                ["manifest policy gate version must equal 5.13.0"]
                if policy_gate.get("version")
                != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION
                else []
            ),
            *(
                ["manifest policy gate hash must be present"]
                if not _is_sha256(policy_hash)
                else []
            ),
        ]
    )


def _approval_request_metadata_valid(request_metadata: Mapping[str, Any]) -> bool:
    return (
        request_metadata.get("approval_request_type")
        == "future_execution_adapter_manifest_approval_request_metadata"
        and request_metadata.get("approval_request_mode") == "metadata_only"
        and request_metadata.get("approval_request_status") == "not_created"
        and request_metadata.get("approval_required") is True
        and request_metadata.get("real_approval_record_written") is False
        and request_metadata.get("approval_notification_sent") is False
        and request_metadata.get("approval_request_created") is False
        and request_metadata.get("candidate_only") is True
        and request_metadata.get("execution_authorized") is False
        and request_metadata.get("adapter_invocation_authorized") is False
        and request_metadata.get("manifest_execution_authorized") is False
        and request_metadata.get("dry_run_plan_execution_authorized") is False
        and _string_list(request_metadata.get("required_approval_roles"))
        == list(REQUIRED_APPROVAL_ROLE_NAMES)
        and _string_list(request_metadata.get("approval_evidence_requirements"))
        == list(REQUIRED_APPROVAL_EVIDENCE_REQUIREMENT_NAMES)
        and _string_list(request_metadata.get("approval_blocking_conditions"))
        == list(REQUIRED_APPROVAL_BLOCKING_CONDITION_NAMES)
        and request_metadata.get("approval_handoff_status") == READY_HANDOFF_STATUS
        and _all_safety_boundaries_false(request_metadata)
    )


def _all_safety_boundaries_false(value: Mapping[str, Any]) -> bool:
    boundaries = value.get("safety_boundaries")
    if not isinstance(boundaries, Mapping):
        return False
    return all(boundaries.get(key) is False for key in SAFETY_BOUNDARIES) and all(
        value.get(key) is False for key in COMMON_DISABLED_FLAGS
    )


def _policy_decisions(policy_gate: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    decisions = policy_gate.get("manifest_policy_gate_decisions")
    return (
        [decision for decision in decisions if isinstance(decision, Mapping)]
        if isinstance(decisions, list)
        else []
    )


def _policy_contracts(policy_gate: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    contracts = policy_gate.get("manifest_policy_gate_contracts")
    return (
        [contract for contract in contracts if isinstance(contract, Mapping)]
        if isinstance(contracts, list)
        else []
    )


def _policy_checks(policy_gate: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    checks = policy_gate.get("manifest_policy_gate_checks")
    return (
        [check for check in checks if isinstance(check, Mapping)]
        if isinstance(checks, list)
        else []
    )


def _policy_decision_status(policy_gate: Mapping[str, Any], name: str) -> str:
    for decision in _policy_decisions(policy_gate):
        if decision.get("decision_name") == name:
            return _status_or_blocked(decision.get("decision_status"))
    return "blocked"


def _policy_contract_status(policy_gate: Mapping[str, Any], name: str) -> str:
    for contract in _policy_contracts(policy_gate):
        if contract.get("contract_name") == name:
            return _status_or_blocked(contract.get("contract_status"))
    return "blocked"


def _policy_check_status(policy_gate: Mapping[str, Any], name: str) -> str:
    for check in _policy_checks(policy_gate):
        if check.get("check_name") == name:
            return _status_or_blocked(check.get("check_status"))
    return "blocked"


def _decision_names(decisions: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        decision["decision_name"]
        for decision in decisions
        if isinstance(decision.get("decision_name"), str)
    ]


def _missing_decision_names(decision_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES
        if name not in decision_names
    ]


def _extra_decision_names(decision_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in decision_names
        if name not in REQUIRED_MANIFEST_APPROVAL_DECISION_NAMES
    ]


def _decision_name_blocking_reasons(decision_names: Sequence[str]) -> list[str]:
    return _deduplicate(
        [
            *(
                ["manifest approval decision names must be complete"]
                if _missing_decision_names(decision_names)
                else []
            ),
            *(
                ["manifest approval decision names must not include extras"]
                if _extra_decision_names(decision_names)
                else []
            ),
        ]
    )


def _decisions_pass(decisions: Sequence[Mapping[str, Any]]) -> bool:
    return all(decision.get("decision_status") == "pass" for decision in decisions)


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return all(contract.get("contract_status") == "pass" for contract in contracts)


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return all(check.get("check_status") == "pass" for check in checks)


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


def _string_list(value: Any) -> list[str]:
    return list(value) if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def _observed_matches_expected(
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> bool:
    return all(observed.get(key) == expected_value for key, expected_value in expected.items())


def _execution_adapter_manifest_approval_gate_hash(
    gate: Mapping[str, Any],
) -> str:
    hash_input = {field: gate[field] for field in _MANIFEST_APPROVAL_GATE_HASH_FIELDS}
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
    "EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION",
    "MANIFEST_APPROVAL_GATE_MODE",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_manifest_approval_gate",
    "get_governance_execution_adapter_manifest_approval_check",
    "get_governance_execution_adapter_manifest_approval_contract",
    "get_governance_execution_adapter_manifest_approval_decision",
    "governance_execution_adapter_manifest_approval_gate_to_json",
    "list_governance_execution_adapter_manifest_approval_check_names",
    "list_governance_execution_adapter_manifest_approval_contract_names",
    "list_governance_execution_adapter_manifest_approval_decision_names",
]
