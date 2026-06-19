"""Deterministic adapter handoff audit metadata for future sandbox planning."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_manifest_authorization_gate import (
    build_governance_execution_adapter_manifest_authorization_gate,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION = "5.13.0"
GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_SCHEMA_VERSION = "5.13.0"
GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_TYPE = (
    "governance_execution_adapter_handoff_audit"
)
GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE = "v5.8_adapter_handoff_audit"
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
ADAPTER_HANDOFF_AUDIT_MODE = "adapter_handoff_audit_only"
FUTURE_ADAPTER_SANDBOX_STATUS = "not_entered"

READY_HANDOFF_STATUS = "ready_for_operation_ledger_proposal_boundary_design"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "adapter_dispatched": False,
    "manifest_dispatched": False,
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
    "execution_authorization_issued": False,
    "authorization_token_created": False,
    "authorization_grant_created": False,
    "adapter_sandbox_entered": False,
    "controlled_adapter_sandbox_started": False,
}

REQUIRED_HANDOFF_READINESS_CONDITION_NAMES = (
    "execution_adapter_boundary_candidate_sealed",
    "adapter_contract_registry_candidate_sealed",
    "adapter_capability_manifest_candidate_sealed",
    "invocation_request_envelope_candidate_sealed",
    "human_approval_boundary_candidate_sealed",
    "adapter_dry_run_simulator_candidate_sealed",
    "side_effect_policy_registry_candidate_sealed",
    "execution_plan_review_matrix_candidate_sealed",
    "manifest_authorization_gate_pass",
    "manifest_authorization_gate_hash_present",
    "manifest_authorization_gate_hash_stable",
    "authorization_metadata_only",
    "approval_metadata_only",
    "candidate_only_boundary_confirmed",
    "no_real_execution",
    "no_adapter_invocation",
    "no_adapter_dispatch",
    "no_manifest_dispatch",
    "no_manifest_execution",
    "no_dry_run_plan_execution",
    "no_external_calls",
    "no_durable_writes",
    "no_filesystem_writes",
    "no_database_writes",
    "no_memory_graph_mutation",
    "no_operation_ledger_writes",
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_adapter_sandbox_entry",
    "no_star_cosmos_active_entry",
)

REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES = (
    "v5_0_boundary_candidate_evidence",
    "v5_1_contract_registry_candidate_evidence",
    "v5_2_capability_manifest_candidate_evidence",
    "v5_3_invocation_request_envelope_candidate_evidence",
    "v5_4_human_approval_boundary_candidate_evidence",
    "v5_5_dry_run_simulator_candidate_evidence",
    "v5_6_side_effect_policy_registry_candidate_evidence",
    "v5_7_execution_plan_review_matrix_candidate_evidence",
    "manifest_authorization_gate_pass_evidence",
    "deterministic_authorization_gate_hash_evidence",
    "authorization_metadata_evidence",
    "approval_metadata_evidence",
    "candidate_only_boundary_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_adapter_dispatch_evidence",
    "no_manifest_dispatch_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_durable_write_evidence",
    "no_filesystem_write_evidence",
    "no_database_write_evidence",
    "no_memory_graph_mutation_evidence",
    "no_operation_ledger_write_evidence",
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_adapter_sandbox_entry_evidence",
    "no_star_cosmos_active_entry_evidence",
)

REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES = (
    "manifest_authorization_gate_blocked",
    "missing_manifest_authorization_gate_hash",
    "unstable_manifest_authorization_gate_hash",
    "authorization_metadata_invalid",
    "approval_metadata_invalid",
    "candidate_only_boundary_missing",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "adapter_dispatch_enabled",
    "manifest_dispatch_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "real_approval_record_written",
    "approval_notification_sent",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "adapter_sandbox_entered",
    "controlled_adapter_sandbox_started",
    "star_cosmos_active_entry_claimed",
)

REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES = (
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
)

REQUIRED_ADAPTER_HANDOFF_AUDIT_CONTRACT_NAMES = (
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
)

REQUIRED_ADAPTER_HANDOFF_AUDIT_CHECK_NAMES = (
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
)

_ADAPTER_HANDOFF_AUDIT_HASH_FIELDS = (
    "version",
    "schema_version",
    "adapter_handoff_audit_type",
    "adapter_handoff_audit_status",
    "adapter_handoff_audit_stage",
    "adapter_handoff_audit_mode",
    "star_cosmos_entry_status",
    "future_adapter_sandbox_status",
    *COMMON_DISABLED_FLAGS,
    "manifest_authorization_gate_version",
    "manifest_authorization_gate_status",
    "manifest_authorization_gate_hash",
    "adapter_handoff_audit_metadata",
    "adapter_handoff_audit_sections",
    "adapter_handoff_audit_contracts",
    "adapter_handoff_audit_checks",
    "adapter_handoff_audit_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_ADAPTER_HANDOFF_AUDIT_HASH_FIELDS),
    "input_shape": "sanitized adapter handoff audit metadata projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_manifest_authorization_gate_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_AUTHORIZATION_GATE_REFS = (
    "manifest_authorization_gate_status",
    "deterministic_manifest_authorization_gate_hash",
    "manifest_authorization_gate_checks",
)


def build_governance_execution_adapter_handoff_audit() -> dict[str, Any]:
    """Build deterministic adapter-handoff-audit-only metadata."""

    authorization_gate, authorization_gate_repeat = (
        _manifest_authorization_gate_pair()
    )
    handoff_metadata = _build_handoff_metadata(
        authorization_gate,
        authorization_gate_repeat,
    )
    sections = _build_handoff_sections(
        authorization_gate,
        authorization_gate_repeat,
        handoff_metadata,
    )
    contracts = _build_handoff_contracts(
        authorization_gate,
        authorization_gate_repeat,
        handoff_metadata,
        sections,
    )
    checks = _build_handoff_checks(
        authorization_gate,
        authorization_gate_repeat,
        handoff_metadata,
        sections,
        contracts,
    )

    authorization_gate_passes = _manifest_authorization_gate_passes(
        authorization_gate
    )
    metadata_valid = _handoff_metadata_valid(handoff_metadata)
    sections_pass = _sections_pass(sections)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    audit_status = (
        "pass"
        if authorization_gate_passes
        and metadata_valid
        and sections_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["manifest authorization gate must pass at version 5.13.0"]
                if not authorization_gate_passes
                else []
            ),
            *(
                ["adapter handoff audit metadata must remain metadata-only"]
                if not metadata_valid
                else []
            ),
            *(
                reason
                for section in sections
                for reason in section["blocking_reasons"]
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
    audit: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION,
        "schema_version": GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_SCHEMA_VERSION,
        "adapter_handoff_audit_type": GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_TYPE,
        "adapter_handoff_audit_status": audit_status,
        "adapter_handoff_audit_stage": EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE,
        "adapter_handoff_audit_mode": ADAPTER_HANDOFF_AUDIT_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
        **COMMON_DISABLED_FLAGS,
        "manifest_authorization_gate_version": _string_or_none(
            authorization_gate.get("version")
        ),
        "manifest_authorization_gate_status": _string_or_none(
            authorization_gate.get("manifest_authorization_gate_status")
        ),
        "manifest_authorization_gate_hash": _string_or_none(
            authorization_gate.get("deterministic_manifest_authorization_gate_hash")
        ),
        "adapter_handoff_audit_metadata": handoff_metadata,
        "adapter_handoff_audit_sections": sections,
        "adapter_handoff_audit_contracts": contracts,
        "adapter_handoff_audit_checks": checks,
        "adapter_handoff_audit_summary": _handoff_audit_summary(
            audit_status,
            authorization_gate,
            authorization_gate_repeat,
            handoff_metadata,
            sections,
            contracts,
            checks,
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if audit_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    audit["deterministic_adapter_handoff_audit_hash"] = (
        _execution_adapter_handoff_audit_hash(audit)
    )
    return _detached_json_value(audit)


def get_governance_execution_adapter_handoff_audit_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff audit section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES:
        return _unknown_section(name)
    audit = _cached_handoff_audit()
    for section in audit["adapter_handoff_audit_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_execution_adapter_handoff_audit_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff audit contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_ADAPTER_HANDOFF_AUDIT_CONTRACT_NAMES:
        return _unknown_contract(name)
    audit = _cached_handoff_audit()
    for contract in audit["adapter_handoff_audit_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_handoff_audit_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff audit check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_ADAPTER_HANDOFF_AUDIT_CHECK_NAMES:
        return _unknown_check(name)
    audit = _cached_handoff_audit()
    for check in audit["adapter_handoff_audit_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_handoff_audit_section_names() -> list[str]:
    """Return stable handoff audit section names."""

    return list(REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES)


def list_governance_execution_adapter_handoff_audit_contract_names() -> list[str]:
    """Return stable handoff audit contract names."""

    return list(REQUIRED_ADAPTER_HANDOFF_AUDIT_CONTRACT_NAMES)


def list_governance_execution_adapter_handoff_audit_check_names() -> list[str]:
    """Return stable handoff audit check names."""

    return list(REQUIRED_ADAPTER_HANDOFF_AUDIT_CHECK_NAMES)


def governance_execution_adapter_handoff_audit_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize adapter handoff audit metadata deterministically."""

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
def _cached_handoff_audit_payload() -> str:
    return governance_execution_adapter_handoff_audit_to_json(
        build_governance_execution_adapter_handoff_audit()
    )


def _cached_handoff_audit() -> dict[str, Any]:
    return json.loads(_cached_handoff_audit_payload())


@lru_cache(maxsize=1)
def _cached_manifest_authorization_gate_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_execution_adapter_manifest_authorization_gate()
    )
    second = _detached_json_value(
        build_governance_execution_adapter_manifest_authorization_gate()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _manifest_authorization_gate_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_manifest_authorization_gate_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_handoff_metadata(
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    authorization_hash = _string_or_none(
        authorization_gate.get("deterministic_manifest_authorization_gate_hash")
    )
    repeat_hash = _string_or_none(
        authorization_gate_repeat.get(
            "deterministic_manifest_authorization_gate_hash"
        )
    )
    hash_present = _is_sha256(authorization_hash)
    hash_stable = hash_present and authorization_hash == repeat_hash
    metadata_valid = _manifest_authorization_gate_passes(
        authorization_gate
    ) and hash_stable
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "handoff_audit_metadata_type": (
                "future_controlled_adapter_sandbox_entry_readiness_metadata"
            ),
            "handoff_audit_metadata_mode": "metadata_only",
            "handoff_audit_status": "not_handed_off",
            "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
            "handoff_required": True,
            "handoff_approved": False,
            "candidate_only": True,
            "authorization_gate_pass_required": True,
            "authorization_gate_hash_required": True,
            "manifest_authorization_gate_version": _string_or_none(
                authorization_gate.get("version")
            ),
            "manifest_authorization_gate_status": _string_or_none(
                authorization_gate.get("manifest_authorization_gate_status")
            ),
            "manifest_authorization_gate_hash_present": hash_present,
            "manifest_authorization_gate_hash_stable": hash_stable,
            "authorization_metadata_only": _authorization_metadata_only(
                authorization_gate
            ),
            "approval_metadata_only": _approval_metadata_only(authorization_gate),
            "required_handoff_evidence": list(
                REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES
            ),
            "handoff_audit_blocking_conditions": list(
                REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES
            ),
            "handoff_audit_readiness_conditions": list(
                REQUIRED_HANDOFF_READINESS_CONDITION_NAMES
            ),
            "handoff_audit_next_stage": "operation_ledger_proposal_boundary",
            "handoff_audit_handoff_status": (
                READY_HANDOFF_STATUS if metadata_valid else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_handoff_sections(
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
    handoff_metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    sections = [
        _sealed_layer_section(
            "v5_0_execution_adapter_boundary_audit",
            "execution_adapter_boundary_candidate_audit",
            "execution_adapter_boundary_candidate",
            "v5_0_boundary_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_1_adapter_contract_registry_audit",
            "adapter_contract_registry_candidate_audit",
            "adapter_contract_registry_candidate",
            "v5_1_contract_registry_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_2_adapter_capability_manifest_audit",
            "adapter_capability_manifest_candidate_audit",
            "adapter_capability_manifest_candidate",
            "v5_2_capability_manifest_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_3_invocation_request_envelope_audit",
            "invocation_request_envelope_candidate_audit",
            "invocation_request_envelope_candidate",
            "v5_3_invocation_request_envelope_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_4_human_approval_boundary_audit",
            "human_approval_boundary_candidate_audit",
            "human_approval_boundary_candidate",
            "v5_4_human_approval_boundary_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_5_adapter_dry_run_simulator_audit",
            "adapter_dry_run_simulator_candidate_audit",
            "adapter_dry_run_simulator_candidate",
            "v5_5_dry_run_simulator_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_6_side_effect_policy_registry_audit",
            "side_effect_policy_registry_candidate_audit",
            "side_effect_policy_registry_candidate",
            "v5_6_side_effect_policy_registry_candidate_evidence",
            authorization_gate,
        ),
        _sealed_layer_section(
            "v5_7_execution_plan_review_matrix_audit",
            "execution_plan_review_matrix_candidate_audit",
            "execution_plan_review_matrix_candidate",
            "v5_7_execution_plan_review_matrix_candidate_evidence",
            authorization_gate,
        ),
        _manifest_authorization_gate_section(
            authorization_gate,
            authorization_gate_repeat,
        ),
        _authorization_metadata_section(authorization_gate),
        _approval_metadata_section(authorization_gate),
        _candidate_only_section(handoff_metadata),
        _runtime_disabled_section(handoff_metadata),
        _write_disabled_section(handoff_metadata),
        _external_call_disabled_section(handoff_metadata),
        _adapter_sandbox_not_entered_section(handoff_metadata),
        _star_cosmos_candidate_only_section(handoff_metadata),
        _future_handoff_readiness_section(handoff_metadata),
    ]
    return _detached_json_value(sections)


def _build_handoff_contracts(
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
    handoff_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    authorization_hash = _string_or_none(
        authorization_gate.get("deterministic_manifest_authorization_gate_hash")
    )
    repeat_hash = _string_or_none(
        authorization_gate_repeat.get(
            "deterministic_manifest_authorization_gate_hash"
        )
    )
    section_names = _section_names(sections)
    section_statuses = [section["section_status"] for section in sections]
    contracts = [
        _contract_from_expected(
            "adapter_handoff_audit_only_contract",
            contract_type="adapter_handoff_audit_mode_contract",
            expected={
                "adapter_handoff_audit_mode": ADAPTER_HANDOFF_AUDIT_MODE,
                "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
                "handoff_approved": False,
            },
            observed={
                "adapter_handoff_audit_mode": ADAPTER_HANDOFF_AUDIT_MODE,
                "future_adapter_sandbox_status": handoff_metadata.get(
                    "future_adapter_sandbox_status"
                ),
                "handoff_approved": handoff_metadata.get("handoff_approved"),
            },
        ),
        _contract_from_expected(
            "future_adapter_sandbox_not_entered_contract",
            contract_type="future_adapter_sandbox_boundary_contract",
            expected={
                "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
                "adapter_sandbox_entered": False,
                "controlled_adapter_sandbox_started": False,
            },
            observed={
                "future_adapter_sandbox_status": handoff_metadata.get(
                    "future_adapter_sandbox_status"
                ),
                "adapter_sandbox_entered": handoff_metadata.get(
                    "adapter_sandbox_entered"
                ),
                "controlled_adapter_sandbox_started": handoff_metadata.get(
                    "controlled_adapter_sandbox_started"
                ),
            },
        ),
        _contract_from_expected(
            "manifest_authorization_gate_pass_contract",
            contract_type="manifest_authorization_gate_status_contract",
            expected={
                "manifest_authorization_gate_status": "pass",
                "manifest_authorization_gate_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION
                ),
            },
            observed={
                "manifest_authorization_gate_status": _string_or_none(
                    authorization_gate.get("manifest_authorization_gate_status")
                ),
                "manifest_authorization_gate_version": _string_or_none(
                    authorization_gate.get("version")
                ),
            },
        ),
        _contract_from_expected(
            "manifest_authorization_gate_hash_present_contract",
            contract_type="manifest_authorization_gate_hash_contract",
            expected={"manifest_authorization_gate_hash_present": True},
            observed={
                "manifest_authorization_gate_hash_present": _is_sha256(
                    authorization_hash
                )
            },
        ),
        _contract_from_expected(
            "manifest_authorization_gate_hash_stable_contract",
            contract_type="manifest_authorization_gate_hash_contract",
            expected={"manifest_authorization_gate_hash_stable": True},
            observed={
                "manifest_authorization_gate_hash_stable": (
                    _is_sha256(authorization_hash)
                    and authorization_hash == repeat_hash
                )
            },
        ),
        _contract_from_expected(
            "handoff_metadata_only_contract",
            contract_type="handoff_metadata_mode_contract",
            expected={
                "handoff_audit_metadata_mode": "metadata_only",
                "handoff_audit_status": "not_handed_off",
                "handoff_approved": False,
            },
            observed={
                "handoff_audit_metadata_mode": handoff_metadata.get(
                    "handoff_audit_metadata_mode"
                ),
                "handoff_audit_status": handoff_metadata.get(
                    "handoff_audit_status"
                ),
                "handoff_approved": handoff_metadata.get("handoff_approved"),
            },
        ),
        _contract_from_expected(
            "handoff_readiness_conditions_declared_contract",
            contract_type="handoff_readiness_condition_contract",
            expected={
                "handoff_audit_readiness_conditions": list(
                    REQUIRED_HANDOFF_READINESS_CONDITION_NAMES
                )
            },
            observed={
                "handoff_audit_readiness_conditions": handoff_metadata.get(
                    "handoff_audit_readiness_conditions"
                )
            },
        ),
        _contract_from_expected(
            "handoff_evidence_requirements_declared_contract",
            contract_type="handoff_evidence_requirement_contract",
            expected={
                "required_handoff_evidence": list(
                    REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES
                )
            },
            observed={
                "required_handoff_evidence": handoff_metadata.get(
                    "required_handoff_evidence"
                )
            },
        ),
        _contract_from_expected(
            "handoff_blocking_conditions_declared_contract",
            contract_type="handoff_blocking_condition_contract",
            expected={
                "handoff_audit_blocking_conditions": list(
                    REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES
                )
            },
            observed={
                "handoff_audit_blocking_conditions": handoff_metadata.get(
                    "handoff_audit_blocking_conditions"
                )
            },
        ),
        _contract_from_expected(
            "handoff_audit_sections_complete_contract",
            contract_type="handoff_section_completeness_contract",
            expected={
                "adapter_handoff_audit_section_names": list(
                    REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES
                )
            },
            observed={"adapter_handoff_audit_section_names": section_names},
        ),
        _contract_from_expected(
            "handoff_audit_sections_pass_contract",
            contract_type="handoff_section_status_contract",
            expected={"all_sections_pass": True},
            observed={"all_sections_pass": all(status == "pass" for status in section_statuses)},
        ),
        _contract_from_expected(
            "authorization_metadata_only_contract",
            contract_type="authorization_metadata_boundary_contract",
            expected={"authorization_metadata_only": True},
            observed={
                "authorization_metadata_only": handoff_metadata.get(
                    "authorization_metadata_only"
                )
            },
        ),
        _contract_from_expected(
            "approval_metadata_only_contract",
            contract_type="approval_metadata_boundary_contract",
            expected={"approval_metadata_only": True},
            observed={
                "approval_metadata_only": handoff_metadata.get(
                    "approval_metadata_only"
                )
            },
        ),
        _contract_from_expected(
            "candidate_only_boundary_contract",
            contract_type="candidate_only_boundary_contract",
            expected={
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed={
                "candidate_only": handoff_metadata.get("candidate_only"),
                "star_cosmos_entry_status": handoff_metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        *_flag_contracts(handoff_metadata),
        _contract_from_expected(
            "star_cosmos_candidate_only_contract",
            contract_type="star_cosmos_candidate_only_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": handoff_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": handoff_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
    ]
    return _detached_json_value(contracts)


def _build_handoff_checks(
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
    handoff_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    authorization_hash = _string_or_none(
        authorization_gate.get("deterministic_manifest_authorization_gate_hash")
    )
    repeat_hash = _string_or_none(
        authorization_gate_repeat.get(
            "deterministic_manifest_authorization_gate_hash"
        )
    )
    section_names = _section_names(sections)
    contract_statuses = [contract["contract_status"] for contract in contracts]
    checks = [
        _check_from_expected(
            "adapter_handoff_audit_stage_check",
            expected={"adapter_handoff_audit_stage": EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE},
            observed={"adapter_handoff_audit_stage": EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE},
        ),
        _check_from_expected(
            "adapter_handoff_audit_only_mode_check",
            expected={"adapter_handoff_audit_mode": ADAPTER_HANDOFF_AUDIT_MODE},
            observed={"adapter_handoff_audit_mode": ADAPTER_HANDOFF_AUDIT_MODE},
        ),
        _check_from_expected(
            "future_adapter_sandbox_not_entered_check",
            expected={
                "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
                "adapter_sandbox_entered": False,
                "controlled_adapter_sandbox_started": False,
            },
            observed={
                "future_adapter_sandbox_status": handoff_metadata.get(
                    "future_adapter_sandbox_status"
                ),
                "adapter_sandbox_entered": handoff_metadata.get(
                    "adapter_sandbox_entered"
                ),
                "controlled_adapter_sandbox_started": handoff_metadata.get(
                    "controlled_adapter_sandbox_started"
                ),
            },
        ),
        _check_from_expected(
            "manifest_authorization_gate_pass_check",
            expected={
                "manifest_authorization_gate_status": "pass",
                "manifest_authorization_gate_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION
                ),
            },
            observed={
                "manifest_authorization_gate_status": _string_or_none(
                    authorization_gate.get("manifest_authorization_gate_status")
                ),
                "manifest_authorization_gate_version": _string_or_none(
                    authorization_gate.get("version")
                ),
            },
        ),
        _check_from_expected(
            "manifest_authorization_gate_hash_present_check",
            expected={"manifest_authorization_gate_hash_present": True},
            observed={
                "manifest_authorization_gate_hash_present": _is_sha256(
                    authorization_hash
                )
            },
        ),
        _check_from_expected(
            "manifest_authorization_gate_hash_stable_check",
            expected={"manifest_authorization_gate_hash_stable": True},
            observed={
                "manifest_authorization_gate_hash_stable": (
                    _is_sha256(authorization_hash)
                    and authorization_hash == repeat_hash
                )
            },
        ),
        _check_from_expected(
            "handoff_metadata_only_check",
            expected={
                "handoff_audit_metadata_mode": "metadata_only",
                "handoff_audit_status": "not_handed_off",
            },
            observed={
                "handoff_audit_metadata_mode": handoff_metadata.get(
                    "handoff_audit_metadata_mode"
                ),
                "handoff_audit_status": handoff_metadata.get(
                    "handoff_audit_status"
                ),
            },
        ),
        _check_from_expected(
            "handoff_readiness_conditions_declared_check",
            expected={
                "handoff_audit_readiness_conditions": list(
                    REQUIRED_HANDOFF_READINESS_CONDITION_NAMES
                )
            },
            observed={
                "handoff_audit_readiness_conditions": handoff_metadata.get(
                    "handoff_audit_readiness_conditions"
                )
            },
        ),
        _check_from_expected(
            "handoff_evidence_requirements_declared_check",
            expected={
                "required_handoff_evidence": list(
                    REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES
                )
            },
            observed={
                "required_handoff_evidence": handoff_metadata.get(
                    "required_handoff_evidence"
                )
            },
        ),
        _check_from_expected(
            "handoff_blocking_conditions_declared_check",
            expected={
                "handoff_audit_blocking_conditions": list(
                    REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES
                )
            },
            observed={
                "handoff_audit_blocking_conditions": handoff_metadata.get(
                    "handoff_audit_blocking_conditions"
                )
            },
        ),
        _check_from_expected(
            "handoff_audit_sections_complete_check",
            expected={
                "adapter_handoff_audit_section_names": list(
                    REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES
                )
            },
            observed={"adapter_handoff_audit_section_names": section_names},
        ),
        _check_from_expected(
            "handoff_audit_sections_pass_check",
            expected={"all_sections_pass": True},
            observed={"all_sections_pass": _sections_pass(sections)},
        ),
        _check_from_expected(
            "handoff_audit_contracts_pass_check",
            expected={"all_contracts_pass": True},
            observed={
                "all_contracts_pass": all(
                    status == "pass" for status in contract_statuses
                )
            },
        ),
        _check_from_expected(
            "authorization_metadata_only_check",
            expected={"authorization_metadata_only": True},
            observed={
                "authorization_metadata_only": handoff_metadata.get(
                    "authorization_metadata_only"
                )
            },
        ),
        _check_from_expected(
            "approval_metadata_only_check",
            expected={"approval_metadata_only": True},
            observed={
                "approval_metadata_only": handoff_metadata.get(
                    "approval_metadata_only"
                )
            },
        ),
        _check_from_expected(
            "candidate_only_boundary_check",
            expected={
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed={
                "candidate_only": handoff_metadata.get("candidate_only"),
                "star_cosmos_entry_status": handoff_metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        *_flag_checks(handoff_metadata),
        _check_from_expected(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": handoff_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": handoff_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
        _check_from_expected(
            "deterministic_handoff_audit_hash_check",
            expected={
                "hash_algorithm": GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM,
                "hash_fields_declared": True,
            },
            observed={
                "hash_algorithm": HASH_INPUT_CONTRACT["algorithm"],
                "hash_fields_declared": (
                    HASH_INPUT_CONTRACT["hash_fields"]
                    == list(_ADAPTER_HANDOFF_AUDIT_HASH_FIELDS)
                ),
            },
        ),
        _check_from_expected(
            "handoff_audit_readiness_check",
            expected={
                "handoff_audit_handoff_status": READY_HANDOFF_STATUS,
                "handoff_audit_next_stage": "operation_ledger_proposal_boundary",
            },
            observed={
                "handoff_audit_handoff_status": handoff_metadata.get(
                    "handoff_audit_handoff_status"
                ),
                "handoff_audit_next_stage": handoff_metadata.get(
                    "handoff_audit_next_stage"
                ),
            },
        ),
    ]
    return _detached_json_value(checks)


def _sealed_layer_section(
    name: str,
    section_type: str,
    layer_name: str,
    evidence_name: str,
    authorization_gate: Mapping[str, Any],
) -> dict[str, Any]:
    expected = {
        "sealed_layer_name": layer_name,
        "evidence_requirement": evidence_name,
        "candidate_only": True,
        "manifest_authorization_gate_status": "pass",
        "manifest_authorization_gate_hash_present": True,
    }
    observed = {
        "sealed_layer_name": layer_name,
        "evidence_requirement": evidence_name,
        "candidate_only": True,
        "manifest_authorization_gate_status": _string_or_none(
            authorization_gate.get("manifest_authorization_gate_status")
        ),
        "manifest_authorization_gate_hash_present": _is_sha256(
            _string_or_none(
                authorization_gate.get(
                    "deterministic_manifest_authorization_gate_hash"
                )
            )
        ),
    }
    return _section_from_expected(
        name,
        section_type=section_type,
        source_authorization_gate_refs=list(_AUTHORIZATION_GATE_REFS),
        expected=expected,
        observed=observed,
        audit_notes=[
            "sealed layer evidence is evaluated through the local authorization gate",
            "adapter handoff audit records metadata labels only",
        ],
    )


def _manifest_authorization_gate_section(
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    authorization_hash = _string_or_none(
        authorization_gate.get("deterministic_manifest_authorization_gate_hash")
    )
    repeat_hash = _string_or_none(
        authorization_gate_repeat.get(
            "deterministic_manifest_authorization_gate_hash"
        )
    )
    return _section_from_expected(
        "manifest_authorization_gate_audit",
        section_type="manifest_authorization_gate_handoff_audit",
        source_authorization_gate_refs=list(_AUTHORIZATION_GATE_REFS),
        expected={
            "manifest_authorization_gate_status": "pass",
            "manifest_authorization_gate_version": (
                GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION
            ),
            "manifest_authorization_gate_hash_present": True,
            "manifest_authorization_gate_hash_stable": True,
        },
        observed={
            "manifest_authorization_gate_status": _string_or_none(
                authorization_gate.get("manifest_authorization_gate_status")
            ),
            "manifest_authorization_gate_version": _string_or_none(
                authorization_gate.get("version")
            ),
            "manifest_authorization_gate_hash_present": _is_sha256(
                authorization_hash
            ),
            "manifest_authorization_gate_hash_stable": (
                _is_sha256(authorization_hash) and authorization_hash == repeat_hash
            ),
        },
        audit_notes=[
            "handoff audit depends on a passing and stable authorization gate hash",
        ],
    )


def _authorization_metadata_section(
    authorization_gate: Mapping[str, Any],
) -> dict[str, Any]:
    metadata = _authorization_metadata(authorization_gate)
    return _section_from_expected(
        "authorization_metadata_audit",
        section_type="authorization_metadata_handoff_audit",
        source_authorization_gate_refs=[
            "manifest_execution_authorization_metadata",
            "no_execution_authorization_issued_check",
            "no_authorization_token_created_check",
            "no_authorization_grant_created_check",
        ],
        expected={
            "authorization_metadata_mode": "metadata_only",
            "authorization_status": "not_issued",
            "execution_authorization_issued": False,
            "authorization_token_created": False,
            "authorization_grant_created": False,
        },
        observed={
            "authorization_metadata_mode": metadata.get(
                "authorization_metadata_mode"
            ),
            "authorization_status": metadata.get("authorization_status"),
            "execution_authorization_issued": metadata.get(
                "execution_authorization_issued"
            ),
            "authorization_token_created": metadata.get(
                "authorization_token_created"
            ),
            "authorization_grant_created": metadata.get(
                "authorization_grant_created"
            ),
        },
        audit_notes=[
            "authorization evidence remains metadata-only and not issued",
        ],
    )


def _approval_metadata_section(
    authorization_gate: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "approval_metadata_audit",
        section_type="approval_metadata_handoff_audit",
        source_authorization_gate_refs=[
            "manifest_approval_gate_status",
            "no_real_approval_record_write_authorization_check",
            "no_approval_notification_authorization_check",
        ],
        expected={
            "manifest_approval_gate_status": "pass",
            "approval_request_created": False,
            "approval_notification_sent": False,
            "real_approval_record_written": False,
        },
        observed={
            "manifest_approval_gate_status": _string_or_none(
                authorization_gate.get("manifest_approval_gate_status")
            ),
            "approval_request_created": authorization_gate.get(
                "approval_request_created"
            ),
            "approval_notification_sent": authorization_gate.get(
                "approval_notification_sent"
            ),
            "real_approval_record_written": authorization_gate.get(
                "real_approval_record_written"
            ),
        },
        audit_notes=[
            "approval evidence is inherited as local metadata and no approval record is created",
        ],
    )


def _candidate_only_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "candidate_only_boundary_audit",
        section_type="candidate_only_boundary_handoff_audit",
        source_authorization_gate_refs=["star_cosmos_candidate_only_authorization_check"],
        expected={
            "candidate_only": True,
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
        },
        observed={
            "candidate_only": handoff_metadata.get("candidate_only"),
            "star_cosmos_entry_status": handoff_metadata.get(
                "star_cosmos_entry_status"
            ),
            "star_cosmos_memory_active": handoff_metadata.get(
                "star_cosmos_memory_active"
            ),
        },
        audit_notes=["handoff audit remains candidate-only"],
    )


def _runtime_disabled_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    keys = (
        "execution_adapter_implemented",
        "execution_adapter_invoked",
        "adapter_dispatched",
        "manifest_dispatched",
        "manifest_executed",
        "dry_run_plan_executed",
        "real_execution_enabled",
        "autonomous_execution_enabled",
    )
    expected = {key: False for key in keys}
    observed = {key: handoff_metadata.get(key) for key in keys}
    return _section_from_expected(
        "runtime_disabled_boundary_audit",
        section_type="runtime_disabled_boundary_handoff_audit",
        source_authorization_gate_refs=[
            "no_real_execution_authorization_check",
            "no_adapter_invocation_authorization_check",
            "no_manifest_execution_authorization_check",
            "no_dry_run_plan_execution_authorization_check",
        ],
        expected=expected,
        observed=observed,
        audit_notes=["runtime capability remains disabled in handoff metadata"],
    )


def _write_disabled_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    keys = (
        "durable_writes_enabled",
        "filesystem_writes_enabled",
        "database_writes_enabled",
        "memory_graph_mutation_enabled",
        "operation_ledger_writes_enabled",
    )
    expected = {key: False for key in keys}
    observed = {key: handoff_metadata.get(key) for key in keys}
    return _section_from_expected(
        "write_disabled_boundary_audit",
        section_type="write_disabled_boundary_handoff_audit",
        source_authorization_gate_refs=[
            "no_durable_write_authorization_check",
            "no_filesystem_write_authorization_check",
            "no_database_write_authorization_check",
            "no_memory_graph_mutation_authorization_check",
            "no_operation_ledger_write_authorization_check",
        ],
        expected=expected,
        observed=observed,
        audit_notes=["durable mutation surfaces remain disabled"],
    )


def _external_call_disabled_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "external_call_disabled_boundary_audit",
        section_type="external_call_disabled_boundary_handoff_audit",
        source_authorization_gate_refs=["no_external_call_authorization_check"],
        expected={"external_calls_enabled": False},
        observed={
            "external_calls_enabled": handoff_metadata.get(
                "external_calls_enabled"
            )
        },
        audit_notes=["external call capability remains disabled"],
    )


def _adapter_sandbox_not_entered_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "adapter_sandbox_not_entered_audit",
        section_type="adapter_sandbox_not_entered_handoff_audit",
        source_authorization_gate_refs=[
            "no_execution_authorization_issued_check",
            "no_authorization_token_created_check",
            "no_authorization_grant_created_check",
        ],
        expected={
            "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
            "adapter_sandbox_entered": False,
            "controlled_adapter_sandbox_started": False,
        },
        observed={
            "future_adapter_sandbox_status": handoff_metadata.get(
                "future_adapter_sandbox_status"
            ),
            "adapter_sandbox_entered": handoff_metadata.get(
                "adapter_sandbox_entered"
            ),
            "controlled_adapter_sandbox_started": handoff_metadata.get(
                "controlled_adapter_sandbox_started"
            ),
        },
        audit_notes=["future sandbox status remains not entered"],
    )


def _star_cosmos_candidate_only_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "star_cosmos_candidate_only_audit",
        section_type="star_cosmos_candidate_only_handoff_audit",
        source_authorization_gate_refs=["star_cosmos_candidate_only_authorization_check"],
        expected={
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
        },
        observed={
            "star_cosmos_entry_status": handoff_metadata.get(
                "star_cosmos_entry_status"
            ),
            "star_cosmos_memory_active": handoff_metadata.get(
                "star_cosmos_memory_active"
            ),
        },
        audit_notes=["Star-Cosmos remains candidate-only in this metadata layer"],
    )


def _future_handoff_readiness_section(
    handoff_metadata: Mapping[str, Any],
) -> dict[str, Any]:
    return _section_from_expected(
        "future_handoff_readiness_audit",
        section_type="future_handoff_readiness_handoff_audit",
        source_authorization_gate_refs=[
            "authorization_handoff_readiness_check",
            "deterministic_authorization_gate_hash_check",
        ],
        expected={
            "handoff_audit_handoff_status": READY_HANDOFF_STATUS,
            "handoff_audit_next_stage": "operation_ledger_proposal_boundary",
            "handoff_audit_readiness_conditions": list(
                REQUIRED_HANDOFF_READINESS_CONDITION_NAMES
            ),
            "required_handoff_evidence": list(
                REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES
            ),
            "handoff_audit_blocking_conditions": list(
                REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES
            ),
        },
        observed={
            "handoff_audit_handoff_status": handoff_metadata.get(
                "handoff_audit_handoff_status"
            ),
            "handoff_audit_next_stage": handoff_metadata.get(
                "handoff_audit_next_stage"
            ),
            "handoff_audit_readiness_conditions": handoff_metadata.get(
                "handoff_audit_readiness_conditions"
            ),
            "required_handoff_evidence": handoff_metadata.get(
                "required_handoff_evidence"
            ),
            "handoff_audit_blocking_conditions": handoff_metadata.get(
                "handoff_audit_blocking_conditions"
            ),
        },
        audit_notes=["future readiness labels are complete and metadata-only"],
    )


def _flag_contracts(handoff_metadata: Mapping[str, Any]) -> list[dict[str, Any]]:
    flag_specs = (
        ("no_real_execution_contract", "real_execution_enabled"),
        ("no_adapter_invocation_contract", "execution_adapter_invoked"),
        ("no_adapter_dispatch_contract", "adapter_dispatched"),
        ("no_manifest_dispatch_contract", "manifest_dispatched"),
        ("no_manifest_execution_contract", "manifest_executed"),
        ("no_dry_run_plan_execution_contract", "dry_run_plan_executed"),
        ("no_external_call_contract", "external_calls_enabled"),
        ("no_durable_write_contract", "durable_writes_enabled"),
        ("no_filesystem_write_contract", "filesystem_writes_enabled"),
        ("no_database_write_contract", "database_writes_enabled"),
        ("no_memory_graph_mutation_contract", "memory_graph_mutation_enabled"),
        ("no_operation_ledger_write_contract", "operation_ledger_writes_enabled"),
        ("no_real_approval_record_contract", "real_approval_record_written"),
        ("no_approval_notification_contract", "approval_notification_sent"),
        (
            "no_execution_authorization_issued_contract",
            "execution_authorization_issued",
        ),
        ("no_authorization_token_created_contract", "authorization_token_created"),
        ("no_authorization_grant_created_contract", "authorization_grant_created"),
        ("no_adapter_sandbox_entry_contract", "adapter_sandbox_entered"),
    )
    return [
        _contract_from_expected(
            contract_name,
            contract_type="disabled_boundary_contract",
            expected={field_name: False},
            observed={field_name: handoff_metadata.get(field_name)},
        )
        for contract_name, field_name in flag_specs
    ]


def _flag_checks(handoff_metadata: Mapping[str, Any]) -> list[dict[str, Any]]:
    flag_specs = (
        ("no_real_execution_check", "real_execution_enabled"),
        ("no_adapter_invocation_check", "execution_adapter_invoked"),
        ("no_adapter_dispatch_check", "adapter_dispatched"),
        ("no_manifest_dispatch_check", "manifest_dispatched"),
        ("no_manifest_execution_check", "manifest_executed"),
        ("no_dry_run_plan_execution_check", "dry_run_plan_executed"),
        ("no_external_call_check", "external_calls_enabled"),
        ("no_durable_write_check", "durable_writes_enabled"),
        ("no_filesystem_write_check", "filesystem_writes_enabled"),
        ("no_database_write_check", "database_writes_enabled"),
        ("no_memory_graph_mutation_check", "memory_graph_mutation_enabled"),
        ("no_operation_ledger_write_check", "operation_ledger_writes_enabled"),
        ("no_real_approval_record_check", "real_approval_record_written"),
        ("no_approval_notification_check", "approval_notification_sent"),
        ("no_execution_authorization_issued_check", "execution_authorization_issued"),
        ("no_authorization_token_created_check", "authorization_token_created"),
        ("no_authorization_grant_created_check", "authorization_grant_created"),
        ("no_adapter_sandbox_entry_check", "adapter_sandbox_entered"),
    )
    return [
        _check_from_expected(
            check_name,
            expected={field_name: False},
            observed={field_name: handoff_metadata.get(field_name)},
        )
        for check_name, field_name in flag_specs
    ]


def _handoff_audit_summary(
    audit_status: str,
    authorization_gate: Mapping[str, Any],
    authorization_gate_repeat: Mapping[str, Any],
    handoff_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    authorization_hash = _string_or_none(
        authorization_gate.get("deterministic_manifest_authorization_gate_hash")
    )
    repeat_hash = _string_or_none(
        authorization_gate_repeat.get(
            "deterministic_manifest_authorization_gate_hash"
        )
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "adapter_handoff_audit_summary",
            "adapter_handoff_audit_status": audit_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if audit_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "future_adapter_sandbox_status": FUTURE_ADAPTER_SANDBOX_STATUS,
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "manifest_authorization_gate_version": _string_or_none(
                authorization_gate.get("version")
            ),
            "manifest_authorization_gate_status": _string_or_none(
                authorization_gate.get("manifest_authorization_gate_status")
            ),
            "manifest_authorization_gate_hash_present": _is_sha256(
                authorization_hash
            ),
            "manifest_authorization_gate_hash_stable": (
                _is_sha256(authorization_hash) and authorization_hash == repeat_hash
            ),
            "handoff_metadata_valid": _handoff_metadata_valid(handoff_metadata),
            "adapter_handoff_audit_section_count": len(sections),
            "adapter_handoff_audit_sections_pass": _sections_pass(sections),
            "adapter_handoff_audit_contract_count": len(contracts),
            "adapter_handoff_audit_contracts_pass": _contracts_pass(contracts),
            "adapter_handoff_audit_check_count": len(checks),
            "adapter_handoff_audit_checks_pass": _checks_pass(checks),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_expected(
    section_name: str,
    *,
    section_type: str,
    source_authorization_gate_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    audit_notes: Sequence[str],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "adapter handoff audit section expected values must match observed values",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": section_name,
            "section_type": section_type,
            "section_status": "pass" if not blocking_reasons else "blocked",
            "source_authorization_gate_refs": list(source_authorization_gate_refs),
            "expected": dict(expected),
            "observed": dict(observed),
            "audit_notes": list(audit_notes),
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _contract_from_expected(
    contract_name: str,
    *,
    contract_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "adapter handoff audit contract expected values must match observed values",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "contract_name": contract_name,
            "contract_type": contract_type,
            "expected": dict(expected),
            "observed": dict(observed),
            "contract_status": "pass" if not blocking_reasons else "blocked",
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _check_from_expected(
    check_name: str,
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "adapter handoff audit check expected values must match observed values",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "check_name": check_name,
            "expected": dict(expected),
            "observed": dict(observed),
            "check_status": "pass" if not blocking_reasons else "blocked",
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_adapter_handoff_audit_section",
            "section_status": "blocked",
            "source_authorization_gate_refs": [],
            "expected": {"known_section_name": True},
            "observed": {
                "known_section_name": False,
                "requested_section_name": name,
            },
            "audit_notes": [],
            "blocking_reasons": [
                "execution adapter handoff audit section name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_adapter_handoff_audit_contract",
            "expected": {"known_contract_name": True},
            "observed": {
                "known_contract_name": False,
                "requested_contract_name": name,
            },
            "contract_status": "blocked",
            "blocking_reasons": [
                "execution adapter handoff audit contract name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _unknown_check(name: str) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "check_name": name,
            "expected": {"known_check_name": True},
            "observed": {
                "known_check_name": False,
                "requested_check_name": name,
            },
            "check_status": "blocked",
            "blocking_reasons": [
                "execution adapter handoff audit check name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _execution_adapter_handoff_audit_hash(result: Mapping[str, Any]) -> str:
    projection = {
        field: result[field]
        for field in _ADAPTER_HANDOFF_AUDIT_HASH_FIELDS
        if field in result
    }
    payload = json.dumps(
        _detached_json_value(projection),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _manifest_authorization_gate_passes(
    authorization_gate: Mapping[str, Any],
) -> bool:
    return (
        authorization_gate.get("manifest_authorization_gate_status") == "pass"
        and authorization_gate.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION
        and _is_sha256(
            _string_or_none(
                authorization_gate.get(
                    "deterministic_manifest_authorization_gate_hash"
                )
            )
        )
    )


def _authorization_metadata_only(authorization_gate: Mapping[str, Any]) -> bool:
    metadata = _authorization_metadata(authorization_gate)
    return (
        metadata.get("authorization_metadata_mode") == "metadata_only"
        and metadata.get("authorization_status") == "not_issued"
        and metadata.get("execution_authorization_issued") is False
        and metadata.get("authorization_token_created") is False
        and metadata.get("authorization_grant_created") is False
    )


def _approval_metadata_only(authorization_gate: Mapping[str, Any]) -> bool:
    return (
        authorization_gate.get("manifest_approval_gate_status") == "pass"
        and authorization_gate.get("approval_request_created") is False
        and authorization_gate.get("approval_notification_sent") is False
        and authorization_gate.get("real_approval_record_written") is False
    )


def _authorization_metadata(authorization_gate: Mapping[str, Any]) -> Mapping[str, Any]:
    metadata = authorization_gate.get("manifest_execution_authorization_metadata")
    return metadata if isinstance(metadata, Mapping) else {}


def _handoff_metadata_valid(handoff_metadata: Mapping[str, Any]) -> bool:
    return (
        handoff_metadata.get("handoff_audit_metadata_type")
        == "future_controlled_adapter_sandbox_entry_readiness_metadata"
        and handoff_metadata.get("handoff_audit_metadata_mode") == "metadata_only"
        and handoff_metadata.get("handoff_audit_status") == "not_handed_off"
        and handoff_metadata.get("future_adapter_sandbox_status")
        == FUTURE_ADAPTER_SANDBOX_STATUS
        and handoff_metadata.get("handoff_required") is True
        and handoff_metadata.get("handoff_approved") is False
        and handoff_metadata.get("candidate_only") is True
        and handoff_metadata.get("authorization_gate_pass_required") is True
        and handoff_metadata.get("authorization_gate_hash_required") is True
        and handoff_metadata.get("handoff_audit_handoff_status")
        == READY_HANDOFF_STATUS
        and handoff_metadata.get("handoff_audit_next_stage")
        == "operation_ledger_proposal_boundary"
        and handoff_metadata.get("handoff_audit_readiness_conditions")
        == list(REQUIRED_HANDOFF_READINESS_CONDITION_NAMES)
        and handoff_metadata.get("required_handoff_evidence")
        == list(REQUIRED_HANDOFF_EVIDENCE_REQUIREMENT_NAMES)
        and handoff_metadata.get("handoff_audit_blocking_conditions")
        == list(REQUIRED_HANDOFF_BLOCKING_CONDITION_NAMES)
        and _all_common_disabled_flags_false(handoff_metadata)
        and _all_safety_boundaries_false(handoff_metadata)
    )


def _sections_pass(sections: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [section.get("section_name") for section in sections]
        == list(REQUIRED_ADAPTER_HANDOFF_AUDIT_SECTION_NAMES)
        and all(section.get("section_status") == "pass" for section in sections)
    )


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [contract.get("contract_name") for contract in contracts]
        == list(REQUIRED_ADAPTER_HANDOFF_AUDIT_CONTRACT_NAMES)
        and all(contract.get("contract_status") == "pass" for contract in contracts)
    )


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [check.get("check_name") for check in checks]
        == list(REQUIRED_ADAPTER_HANDOFF_AUDIT_CHECK_NAMES)
        and all(check.get("check_status") == "pass" for check in checks)
    )


def _section_names(sections: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        str(section.get("section_name"))
        for section in sections
        if section.get("section_name") is not None
    ]


def _expected_blocking_reasons(
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    message: str,
) -> list[str]:
    return (
        []
        if _detached_json_value(dict(expected)) == _detached_json_value(dict(observed))
        else [message]
    )


def _all_common_disabled_flags_false(value: Mapping[str, Any]) -> bool:
    return all(value.get(key) is False for key in COMMON_DISABLED_FLAGS)


def _all_safety_boundaries_false(value: Mapping[str, Any]) -> bool:
    boundaries = value.get("safety_boundaries")
    return (
        isinstance(boundaries, Mapping)
        and all(boundaries.get(key) is False for key in SAFETY_BOUNDARIES)
        and all(value.get(key) is False for key in SAFETY_BOUNDARIES)
    )


def _is_sha256(value: str | None) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _deduplicate(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _detached_json_value(value: Any) -> Any:
    _assert_json_compatible(value)
    return json.loads(
        json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
        )
    )


def _assert_json_compatible(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            if not isinstance(key, str):
                raise ValueError("mapping keys must be strings")
            _assert_json_compatible(nested_value)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _assert_json_compatible(item)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("floats must be finite")
    elif value is None or isinstance(value, (str, int, bool)):
        return
    else:
        raise ValueError("value must be JSON-compatible")


__all__ = [
    "ADAPTER_HANDOFF_AUDIT_MODE",
    "EXECUTION_ADAPTER_HANDOFF_AUDIT_STAGE",
    "FUTURE_ADAPTER_SANDBOX_STATUS",
    "GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_HANDOFF_AUDIT_VERSION",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_handoff_audit",
    "get_governance_execution_adapter_handoff_audit_check",
    "get_governance_execution_adapter_handoff_audit_contract",
    "get_governance_execution_adapter_handoff_audit_section",
    "governance_execution_adapter_handoff_audit_to_json",
    "list_governance_execution_adapter_handoff_audit_check_names",
    "list_governance_execution_adapter_handoff_audit_contract_names",
    "list_governance_execution_adapter_handoff_audit_section_names",
]
