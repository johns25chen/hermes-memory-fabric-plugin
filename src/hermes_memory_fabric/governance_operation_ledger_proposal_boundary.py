"""Deterministic operation-ledger proposal boundary metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_handoff_audit import (
    build_governance_execution_adapter_handoff_audit,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION = "6.6.0"
GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SCHEMA_VERSION = "6.6.0"
GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_TYPE = (
    "governance_operation_ledger_proposal_boundary"
)
GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM = "sha256"
OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE = (
    "v5.9_operation_ledger_proposal_boundary"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE = (
    "operation_ledger_proposal_boundary_only"
)
OPERATION_LEDGER_PROPOSAL_MODE = "metadata_only"
OPERATION_LEDGER_ENTRY_STATUS = "not_created"
OPERATION_LEDGER_WRITE_STATUS = "not_written"
FUTURE_CROSS_SYSTEM_COORDINATION_STATUS = "not_entered"

READY_HANDOFF_STATUS = "ready_for_cross_system_coordination_boundary_design"
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
    "operation_ledger_mutation_enabled": False,
    "operation_ledger_entry_created": False,
    "operation_ledger_entry_written": False,
    "operation_ledger_proposal_persisted": False,
    "operation_ledger_proposal_submitted": False,
    "operation_ledger_proposal_dispatched": False,
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

REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES = (
    "adapter_handoff_audit_pass",
    "adapter_handoff_audit_hash_present",
    "adapter_handoff_audit_hash_stable",
    "future_adapter_sandbox_not_entered",
    "handoff_metadata_only",
    "candidate_only_boundary_confirmed",
    "approval_metadata_only",
    "authorization_metadata_only",
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
    "no_operation_ledger_entry_created",
    "no_operation_ledger_entry_written",
    "no_operation_ledger_proposal_persisted",
    "no_operation_ledger_proposal_submitted",
    "no_operation_ledger_proposal_dispatched",
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_adapter_sandbox_entry",
    "no_star_cosmos_active_entry",
)

REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES = (
    "adapter_handoff_audit_pass_evidence",
    "deterministic_handoff_audit_hash_evidence",
    "handoff_metadata_evidence",
    "approval_metadata_evidence",
    "authorization_metadata_evidence",
    "candidate_only_boundary_evidence",
    "future_adapter_sandbox_not_entered_evidence",
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
    "no_operation_ledger_entry_created_evidence",
    "no_operation_ledger_entry_written_evidence",
    "no_operation_ledger_proposal_persisted_evidence",
    "no_operation_ledger_proposal_submitted_evidence",
    "no_operation_ledger_proposal_dispatched_evidence",
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_adapter_sandbox_entry_evidence",
    "no_star_cosmos_active_entry_evidence",
)

REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES = (
    "adapter_handoff_audit_blocked",
    "missing_adapter_handoff_audit_hash",
    "unstable_adapter_handoff_audit_hash",
    "handoff_metadata_invalid",
    "candidate_only_boundary_missing",
    "future_adapter_sandbox_entered",
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
    "operation_ledger_entry_created",
    "operation_ledger_entry_written",
    "operation_ledger_proposal_persisted",
    "operation_ledger_proposal_submitted",
    "operation_ledger_proposal_dispatched",
    "real_approval_record_written",
    "approval_notification_sent",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "adapter_sandbox_entered",
    "controlled_adapter_sandbox_started",
    "star_cosmos_active_entry_claimed",
)

REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES = (
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
)

REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES = (
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
)

REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES = (
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
)

_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_FIELDS = (
    "version",
    "schema_version",
    "operation_ledger_proposal_boundary_type",
    "operation_ledger_proposal_boundary_status",
    "operation_ledger_proposal_boundary_stage",
    "operation_ledger_proposal_boundary_mode",
    "operation_ledger_proposal_mode",
    "operation_ledger_entry_status",
    "operation_ledger_write_status",
    "future_cross_system_coordination_status",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "adapter_handoff_audit_version",
    "adapter_handoff_audit_status",
    "adapter_handoff_audit_hash",
    "operation_ledger_proposal_metadata",
    "operation_ledger_proposal_boundary_sections",
    "operation_ledger_proposal_boundary_contracts",
    "operation_ledger_proposal_boundary_checks",
    "operation_ledger_proposal_boundary_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_FIELDS),
    "input_shape": (
        "sanitized operation ledger proposal boundary metadata projection"
    ),
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_adapter_handoff_audit_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_HANDOFF_REFS = (
    "adapter_handoff_audit_status",
    "deterministic_adapter_handoff_audit_hash",
    "adapter_handoff_audit_metadata",
)


def build_governance_operation_ledger_proposal_boundary() -> dict[str, Any]:
    """Build deterministic operation-ledger-proposal-boundary-only metadata."""

    handoff_audit, repeated_handoff_audit = _adapter_handoff_audit_pair()
    proposal_metadata = _build_proposal_metadata(
        handoff_audit,
        repeated_handoff_audit,
    )
    sections = _build_boundary_sections(
        handoff_audit,
        repeated_handoff_audit,
        proposal_metadata,
    )
    contracts = _build_boundary_contracts(
        handoff_audit,
        repeated_handoff_audit,
        proposal_metadata,
        sections,
    )
    checks = _build_boundary_checks(
        handoff_audit,
        repeated_handoff_audit,
        proposal_metadata,
        sections,
        contracts,
    )

    handoff_passes = _adapter_handoff_audit_passes(handoff_audit)
    metadata_valid = _proposal_metadata_valid(proposal_metadata)
    sections_pass = _sections_pass(sections)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    boundary_status = (
        "pass"
        if handoff_passes
        and metadata_valid
        and sections_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["adapter handoff audit must pass at version 6.6.0"]
                if not handoff_passes
                else []
            ),
            *(
                ["operation ledger proposal metadata must remain metadata-only"]
                if not metadata_valid
                else []
            ),
            *(
                reason
                for item in (*sections, *contracts, *checks)
                for reason in item["blocking_reasons"]
            ),
        ]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION,
        "schema_version": (
            GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SCHEMA_VERSION
        ),
        "operation_ledger_proposal_boundary_type": (
            GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_TYPE
        ),
        "operation_ledger_proposal_boundary_status": boundary_status,
        "operation_ledger_proposal_boundary_stage": (
            OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE
        ),
        "operation_ledger_proposal_boundary_mode": (
            OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE
        ),
        "operation_ledger_proposal_mode": OPERATION_LEDGER_PROPOSAL_MODE,
        "operation_ledger_entry_status": OPERATION_LEDGER_ENTRY_STATUS,
        "operation_ledger_write_status": OPERATION_LEDGER_WRITE_STATUS,
        "future_cross_system_coordination_status": (
            FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
        ),
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "adapter_handoff_audit_version": _string_or_none(
            handoff_audit.get("version")
        ),
        "adapter_handoff_audit_status": _string_or_none(
            handoff_audit.get("adapter_handoff_audit_status")
        ),
        "adapter_handoff_audit_hash": _string_or_none(
            handoff_audit.get("deterministic_adapter_handoff_audit_hash")
        ),
        "operation_ledger_proposal_metadata": proposal_metadata,
        "operation_ledger_proposal_boundary_sections": sections,
        "operation_ledger_proposal_boundary_contracts": contracts,
        "operation_ledger_proposal_boundary_checks": checks,
        "operation_ledger_proposal_boundary_summary": _boundary_summary(
            boundary_status,
            handoff_audit,
            repeated_handoff_audit,
            proposal_metadata,
            sections,
            contracts,
            checks,
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if boundary_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_operation_ledger_proposal_boundary_hash"] = (
        _operation_ledger_proposal_boundary_hash(result)
    )
    return _detached_json_value(result)


def get_governance_operation_ledger_proposal_boundary_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached proposal boundary section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_boundary()[
        "operation_ledger_proposal_boundary_sections"
    ]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_operation_ledger_proposal_boundary_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached proposal boundary contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_boundary()[
        "operation_ledger_proposal_boundary_contracts"
    ]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_operation_ledger_proposal_boundary_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached proposal boundary check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_boundary()["operation_ledger_proposal_boundary_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_operation_ledger_proposal_boundary_section_names() -> list[str]:
    """Return stable proposal boundary section names."""

    return list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES)


def list_governance_operation_ledger_proposal_boundary_contract_names() -> list[str]:
    """Return stable proposal boundary contract names."""

    return list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES)


def list_governance_operation_ledger_proposal_boundary_check_names() -> list[str]:
    """Return stable proposal boundary check names."""

    return list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES)


def governance_operation_ledger_proposal_boundary_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize operation ledger proposal boundary metadata deterministically."""

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
def _cached_boundary_payload() -> str:
    return governance_operation_ledger_proposal_boundary_to_json(
        build_governance_operation_ledger_proposal_boundary()
    )


def _cached_boundary() -> dict[str, Any]:
    return json.loads(_cached_boundary_payload())


@lru_cache(maxsize=1)
def _cached_adapter_handoff_audit_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(build_governance_execution_adapter_handoff_audit())
    second = _detached_json_value(build_governance_execution_adapter_handoff_audit())
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _adapter_handoff_audit_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_adapter_handoff_audit_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_proposal_metadata(
    handoff_audit: Mapping[str, Any],
    repeated_handoff_audit: Mapping[str, Any],
) -> dict[str, Any]:
    handoff_hash = _string_or_none(
        handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    repeated_hash = _string_or_none(
        repeated_handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    handoff_metadata = _handoff_metadata(handoff_audit)
    hash_present = _is_sha256(handoff_hash)
    hash_stable = hash_present and handoff_hash == repeated_hash
    proposal_ready = (
        _adapter_handoff_audit_passes(handoff_audit)
        and hash_stable
        and _handoff_metadata_is_valid(handoff_audit)
        and _upstream_disabled_boundaries_hold(handoff_audit)
        and _all_safety_boundaries_false(handoff_audit)
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "proposal_metadata_type": (
                "future_operation_ledger_proposal_boundary_metadata"
            ),
            "proposal_metadata_mode": OPERATION_LEDGER_PROPOSAL_MODE,
            "proposal_status": "metadata_only_proposal",
            "operation_ledger_entry_status": OPERATION_LEDGER_ENTRY_STATUS,
            "operation_ledger_write_status": OPERATION_LEDGER_WRITE_STATUS,
            "future_cross_system_coordination_status": (
                FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
            ),
            "proposal_required": True,
            "proposal_metadata_available": True,
            "proposal_persisted": False,
            "proposal_submitted": False,
            "proposal_dispatched": False,
            "candidate_only": True,
            "adapter_handoff_audit_pass_required": True,
            "adapter_handoff_audit_hash_required": True,
            "adapter_handoff_audit_status": _string_or_none(
                handoff_audit.get("adapter_handoff_audit_status")
            ),
            "adapter_handoff_audit_hash_present": hash_present,
            "adapter_handoff_audit_hash_stable": hash_stable,
            "handoff_metadata_only": (
                handoff_metadata.get("handoff_audit_metadata_mode")
                == "metadata_only"
            ),
            "approval_metadata_only": (
                handoff_metadata.get("approval_metadata_only") is True
            ),
            "authorization_metadata_only": (
                handoff_metadata.get("authorization_metadata_only") is True
            ),
            "future_adapter_sandbox_not_entered": (
                handoff_metadata.get("future_adapter_sandbox_status")
                == "not_entered"
                and handoff_audit.get("adapter_sandbox_entered") is False
                and handoff_audit.get("controlled_adapter_sandbox_started")
                is False
            ),
            "proposal_boundary_readiness_conditions": list(
                REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES
            ),
            "required_proposal_evidence": list(
                REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES
            ),
            "proposal_boundary_blocking_conditions": list(
                REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES
            ),
            "proposal_boundary_next_stage": (
                "cross_system_coordination_boundary"
            ),
            "proposal_boundary_handoff_status": (
                READY_HANDOFF_STATUS if proposal_ready else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_boundary_sections(
    handoff_audit: Mapping[str, Any],
    repeated_handoff_audit: Mapping[str, Any],
    proposal_metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    handoff_hash = _string_or_none(
        handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    repeated_hash = _string_or_none(
        repeated_handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    handoff_metadata = _handoff_metadata(handoff_audit)
    sections = [
        _section_from_expected(
            "adapter_handoff_audit_input_section",
            section_type="adapter_handoff_audit_input_boundary",
            source_handoff_audit_refs=_HANDOFF_REFS,
            expected={
                "adapter_handoff_audit_version": (
                    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION
                ),
                "adapter_handoff_audit_status": "pass",
                "adapter_handoff_audit_hash_present": True,
                "adapter_handoff_audit_hash_stable": True,
            },
            observed={
                "adapter_handoff_audit_version": _string_or_none(
                    handoff_audit.get("version")
                ),
                "adapter_handoff_audit_status": _string_or_none(
                    handoff_audit.get("adapter_handoff_audit_status")
                ),
                "adapter_handoff_audit_hash_present": _is_sha256(handoff_hash),
                "adapter_handoff_audit_hash_stable": (
                    _is_sha256(handoff_hash) and handoff_hash == repeated_hash
                ),
            },
            proposal_notes=["Consumes detached deterministic handoff audit metadata."],
        ),
        _section_from_expected(
            "handoff_metadata_section",
            section_type="handoff_metadata_boundary",
            source_handoff_audit_refs=("adapter_handoff_audit_metadata",),
            expected={
                "handoff_metadata_only": True,
                "handoff_not_completed": True,
                "approval_metadata_only": True,
                "authorization_metadata_only": True,
            },
            observed={
                "handoff_metadata_only": (
                    handoff_metadata.get("handoff_audit_metadata_mode")
                    == "metadata_only"
                ),
                "handoff_not_completed": (
                    handoff_metadata.get("handoff_audit_status")
                    == "not_handed_off"
                ),
                "approval_metadata_only": (
                    handoff_metadata.get("approval_metadata_only") is True
                ),
                "authorization_metadata_only": (
                    handoff_metadata.get("authorization_metadata_only") is True
                ),
            },
            proposal_notes=["Preserves the sealed handoff as metadata only."],
        ),
        _section_from_expected(
            "proposal_metadata_section",
            section_type="operation_ledger_proposal_metadata_boundary",
            source_handoff_audit_refs=_HANDOFF_REFS,
            expected={
                "proposal_metadata_mode": OPERATION_LEDGER_PROPOSAL_MODE,
                "proposal_status": "metadata_only_proposal",
                "proposal_metadata_available": True,
                "proposal_persisted": False,
                "proposal_submitted": False,
                "proposal_dispatched": False,
            },
            observed={
                key: proposal_metadata.get(key)
                for key in (
                    "proposal_metadata_mode",
                    "proposal_status",
                    "proposal_metadata_available",
                    "proposal_persisted",
                    "proposal_submitted",
                    "proposal_dispatched",
                )
            },
            proposal_notes=["Defines future proposal metadata without persistence."],
        ),
        _section_from_expected(
            "candidate_only_boundary_section",
            section_type="candidate_only_boundary",
            source_handoff_audit_refs=("star_cosmos_entry_status",),
            expected={
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "candidate_only": proposal_metadata.get("candidate_only"),
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": proposal_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
            proposal_notes=["Keeps the boundary candidate-only."],
        ),
        _section_from_expected(
            "runtime_disabled_boundary_section",
            section_type="runtime_disabled_boundary",
            source_handoff_audit_refs=("adapter_handoff_audit_metadata",),
            expected={
                "real_execution_enabled": False,
                "execution_adapter_invoked": False,
                "adapter_dispatched": False,
                "manifest_dispatched": False,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
                "autonomous_execution_enabled": False,
            },
            observed={
                key: proposal_metadata.get(key)
                for key in (
                    "real_execution_enabled",
                    "execution_adapter_invoked",
                    "adapter_dispatched",
                    "manifest_dispatched",
                    "manifest_executed",
                    "dry_run_plan_executed",
                    "autonomous_execution_enabled",
                )
            },
            proposal_notes=["Declares runtime surfaces disabled."],
        ),
        _section_from_expected(
            "write_disabled_boundary_section",
            section_type="write_disabled_boundary",
            source_handoff_audit_refs=("adapter_handoff_audit_metadata",),
            expected={
                "durable_writes_enabled": False,
                "filesystem_writes_enabled": False,
                "database_writes_enabled": False,
                "memory_graph_mutation_enabled": False,
                "operation_ledger_writes_enabled": False,
                "operation_ledger_mutation_enabled": False,
            },
            observed={
                key: proposal_metadata.get(key)
                for key in (
                    "durable_writes_enabled",
                    "filesystem_writes_enabled",
                    "database_writes_enabled",
                    "memory_graph_mutation_enabled",
                    "operation_ledger_writes_enabled",
                    "operation_ledger_mutation_enabled",
                )
            },
            proposal_notes=["Declares all write surfaces disabled."],
        ),
        _section_from_expected(
            "operation_ledger_entry_not_created_section",
            section_type="operation_ledger_entry_boundary",
            source_handoff_audit_refs=("deterministic_adapter_handoff_audit_hash",),
            expected={
                "operation_ledger_entry_status": OPERATION_LEDGER_ENTRY_STATUS,
                "operation_ledger_write_status": OPERATION_LEDGER_WRITE_STATUS,
                "operation_ledger_entry_created": False,
                "operation_ledger_entry_written": False,
            },
            observed={
                key: proposal_metadata.get(key)
                for key in (
                    "operation_ledger_entry_status",
                    "operation_ledger_write_status",
                    "operation_ledger_entry_created",
                    "operation_ledger_entry_written",
                )
            },
            proposal_notes=["No operation ledger entry is created or written."],
        ),
        _section_from_expected(
            "operation_ledger_proposal_not_persisted_section",
            section_type="operation_ledger_proposal_persistence_boundary",
            source_handoff_audit_refs=("deterministic_adapter_handoff_audit_hash",),
            expected={
                "operation_ledger_proposal_persisted": False,
                "operation_ledger_proposal_submitted": False,
                "operation_ledger_proposal_dispatched": False,
            },
            observed={
                key: proposal_metadata.get(key)
                for key in (
                    "operation_ledger_proposal_persisted",
                    "operation_ledger_proposal_submitted",
                    "operation_ledger_proposal_dispatched",
                )
            },
            proposal_notes=["Proposal metadata remains in-memory and local."],
        ),
        _section_from_expected(
            "external_call_disabled_boundary_section",
            section_type="external_call_disabled_boundary",
            source_handoff_audit_refs=("adapter_handoff_audit_metadata",),
            expected={"external_calls_enabled": False},
            observed={
                "external_calls_enabled": proposal_metadata.get(
                    "external_calls_enabled"
                )
            },
            proposal_notes=["Declares external calls disabled."],
        ),
        _section_from_expected(
            "adapter_sandbox_not_entered_section",
            section_type="adapter_sandbox_boundary",
            source_handoff_audit_refs=("adapter_handoff_audit_metadata",),
            expected={
                "future_adapter_sandbox_not_entered": True,
                "adapter_sandbox_entered": False,
                "controlled_adapter_sandbox_started": False,
            },
            observed={
                "future_adapter_sandbox_not_entered": proposal_metadata.get(
                    "future_adapter_sandbox_not_entered"
                ),
                "adapter_sandbox_entered": proposal_metadata.get(
                    "adapter_sandbox_entered"
                ),
                "controlled_adapter_sandbox_started": proposal_metadata.get(
                    "controlled_adapter_sandbox_started"
                ),
            },
            proposal_notes=["The adapter sandbox boundary is not entered."],
        ),
        _section_from_expected(
            "star_cosmos_candidate_only_section",
            section_type="star_cosmos_candidate_only_boundary",
            source_handoff_audit_refs=("star_cosmos_entry_status",),
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": proposal_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
            proposal_notes=["Does not claim active Star-Cosmos entry."],
        ),
        _section_from_expected(
            "future_cross_system_coordination_readiness_section",
            section_type="future_cross_system_coordination_readiness_boundary",
            source_handoff_audit_refs=_HANDOFF_REFS,
            expected={
                "future_cross_system_coordination_status": (
                    FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
                ),
                "proposal_boundary_handoff_status": READY_HANDOFF_STATUS,
                "proposal_boundary_next_stage": (
                    "cross_system_coordination_boundary"
                ),
                "proposal_boundary_readiness_conditions": list(
                    REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES
                ),
            },
            observed={
                "future_cross_system_coordination_status": proposal_metadata.get(
                    "future_cross_system_coordination_status"
                ),
                "proposal_boundary_handoff_status": proposal_metadata.get(
                    "proposal_boundary_handoff_status"
                ),
                "proposal_boundary_next_stage": proposal_metadata.get(
                    "proposal_boundary_next_stage"
                ),
                "proposal_boundary_readiness_conditions": proposal_metadata.get(
                    "proposal_boundary_readiness_conditions"
                ),
            },
            proposal_notes=["Marks readiness for future boundary design only."],
        ),
    ]
    return _detached_json_value(sections)


def _build_boundary_contracts(
    handoff_audit: Mapping[str, Any],
    repeated_handoff_audit: Mapping[str, Any],
    proposal_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    handoff_hash = _string_or_none(
        handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    repeated_hash = _string_or_none(
        repeated_handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    contracts = [
        _contract_from_expected(
            "operation_ledger_proposal_boundary_only_contract",
            contract_type="proposal_boundary_mode_contract",
            expected={
                "operation_ledger_proposal_boundary_mode": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE
                )
            },
            observed={
                "operation_ledger_proposal_boundary_mode": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE
                )
            },
        ),
        _contract_from_expected(
            "operation_ledger_proposal_metadata_only_contract",
            contract_type="proposal_metadata_mode_contract",
            expected={
                "proposal_metadata_mode": OPERATION_LEDGER_PROPOSAL_MODE,
                "proposal_status": "metadata_only_proposal",
            },
            observed={
                "proposal_metadata_mode": proposal_metadata.get(
                    "proposal_metadata_mode"
                ),
                "proposal_status": proposal_metadata.get("proposal_status"),
            },
        ),
        _contract_from_expected(
            "adapter_handoff_audit_pass_contract",
            contract_type="adapter_handoff_audit_status_contract",
            expected={
                "adapter_handoff_audit_version": (
                    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION
                ),
                "adapter_handoff_audit_status": "pass",
            },
            observed={
                "adapter_handoff_audit_version": _string_or_none(
                    handoff_audit.get("version")
                ),
                "adapter_handoff_audit_status": _string_or_none(
                    handoff_audit.get("adapter_handoff_audit_status")
                ),
            },
        ),
        _contract_from_expected(
            "adapter_handoff_audit_hash_present_contract",
            contract_type="adapter_handoff_audit_hash_contract",
            expected={"adapter_handoff_audit_hash_present": True},
            observed={
                "adapter_handoff_audit_hash_present": _is_sha256(handoff_hash)
            },
        ),
        _contract_from_expected(
            "adapter_handoff_audit_hash_stable_contract",
            contract_type="adapter_handoff_audit_hash_contract",
            expected={"adapter_handoff_audit_hash_stable": True},
            observed={
                "adapter_handoff_audit_hash_stable": (
                    _is_sha256(handoff_hash) and handoff_hash == repeated_hash
                )
            },
        ),
        _contract_from_expected(
            "proposal_readiness_conditions_declared_contract",
            contract_type="proposal_requirements_contract",
            expected={
                "proposal_boundary_readiness_conditions": list(
                    REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES
                )
            },
            observed={
                "proposal_boundary_readiness_conditions": proposal_metadata.get(
                    "proposal_boundary_readiness_conditions"
                )
            },
        ),
        _contract_from_expected(
            "proposal_evidence_requirements_declared_contract",
            contract_type="proposal_requirements_contract",
            expected={
                "required_proposal_evidence": list(
                    REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES
                )
            },
            observed={
                "required_proposal_evidence": proposal_metadata.get(
                    "required_proposal_evidence"
                )
            },
        ),
        _contract_from_expected(
            "proposal_blocking_conditions_declared_contract",
            contract_type="proposal_requirements_contract",
            expected={
                "proposal_boundary_blocking_conditions": list(
                    REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES
                )
            },
            observed={
                "proposal_boundary_blocking_conditions": proposal_metadata.get(
                    "proposal_boundary_blocking_conditions"
                )
            },
        ),
        _contract_from_expected(
            "proposal_boundary_sections_complete_contract",
            contract_type="proposal_boundary_sections_contract",
            expected={
                "proposal_boundary_section_names": list(
                    REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES
                )
            },
            observed={
                "proposal_boundary_section_names": _section_names(sections)
            },
        ),
        _contract_from_expected(
            "proposal_boundary_sections_pass_contract",
            contract_type="proposal_boundary_sections_contract",
            expected={"proposal_boundary_sections_pass": True},
            observed={
                "proposal_boundary_sections_pass": _sections_pass(sections)
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
                "candidate_only": proposal_metadata.get("candidate_only"),
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        _contract_from_expected(
            "future_cross_system_coordination_not_entered_contract",
            contract_type="future_coordination_boundary_contract",
            expected={
                "future_cross_system_coordination_status": (
                    FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
                )
            },
            observed={
                "future_cross_system_coordination_status": proposal_metadata.get(
                    "future_cross_system_coordination_status"
                )
            },
        ),
        *_flag_contracts(proposal_metadata),
        _contract_from_expected(
            "star_cosmos_candidate_only_contract",
            contract_type="star_cosmos_candidate_only_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": proposal_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
    ]
    return _detached_json_value(contracts)


def _build_boundary_checks(
    handoff_audit: Mapping[str, Any],
    repeated_handoff_audit: Mapping[str, Any],
    proposal_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    handoff_hash = _string_or_none(
        handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    repeated_hash = _string_or_none(
        repeated_handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    checks = [
        _check_from_expected(
            "operation_ledger_proposal_boundary_stage_check",
            expected={
                "operation_ledger_proposal_boundary_stage": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE
                )
            },
            observed={
                "operation_ledger_proposal_boundary_stage": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE
                )
            },
        ),
        _check_from_expected(
            "operation_ledger_proposal_boundary_only_mode_check",
            expected={
                "operation_ledger_proposal_boundary_mode": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE
                )
            },
            observed={
                "operation_ledger_proposal_boundary_mode": (
                    OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE
                )
            },
        ),
        _check_from_expected(
            "operation_ledger_proposal_metadata_only_check",
            expected={
                "operation_ledger_proposal_mode": OPERATION_LEDGER_PROPOSAL_MODE
            },
            observed={
                "operation_ledger_proposal_mode": proposal_metadata.get(
                    "proposal_metadata_mode"
                )
            },
        ),
        _check_from_expected(
            "operation_ledger_entry_not_created_check",
            expected={
                "operation_ledger_entry_status": OPERATION_LEDGER_ENTRY_STATUS,
                "operation_ledger_entry_created": False,
            },
            observed={
                "operation_ledger_entry_status": proposal_metadata.get(
                    "operation_ledger_entry_status"
                ),
                "operation_ledger_entry_created": proposal_metadata.get(
                    "operation_ledger_entry_created"
                ),
            },
        ),
        _check_from_expected(
            "operation_ledger_write_not_written_check",
            expected={
                "operation_ledger_write_status": OPERATION_LEDGER_WRITE_STATUS,
                "operation_ledger_entry_written": False,
            },
            observed={
                "operation_ledger_write_status": proposal_metadata.get(
                    "operation_ledger_write_status"
                ),
                "operation_ledger_entry_written": proposal_metadata.get(
                    "operation_ledger_entry_written"
                ),
            },
        ),
        _check_from_expected(
            "adapter_handoff_audit_pass_check",
            expected={"adapter_handoff_audit_status": "pass"},
            observed={
                "adapter_handoff_audit_status": _string_or_none(
                    handoff_audit.get("adapter_handoff_audit_status")
                )
            },
        ),
        _check_from_expected(
            "adapter_handoff_audit_hash_present_check",
            expected={"adapter_handoff_audit_hash_present": True},
            observed={
                "adapter_handoff_audit_hash_present": _is_sha256(handoff_hash)
            },
        ),
        _check_from_expected(
            "adapter_handoff_audit_hash_stable_check",
            expected={"adapter_handoff_audit_hash_stable": True},
            observed={
                "adapter_handoff_audit_hash_stable": (
                    _is_sha256(handoff_hash) and handoff_hash == repeated_hash
                )
            },
        ),
        _check_from_expected(
            "proposal_readiness_conditions_declared_check",
            expected={
                "proposal_boundary_readiness_conditions": list(
                    REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES
                )
            },
            observed={
                "proposal_boundary_readiness_conditions": proposal_metadata.get(
                    "proposal_boundary_readiness_conditions"
                )
            },
        ),
        _check_from_expected(
            "proposal_evidence_requirements_declared_check",
            expected={
                "required_proposal_evidence": list(
                    REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES
                )
            },
            observed={
                "required_proposal_evidence": proposal_metadata.get(
                    "required_proposal_evidence"
                )
            },
        ),
        _check_from_expected(
            "proposal_blocking_conditions_declared_check",
            expected={
                "proposal_boundary_blocking_conditions": list(
                    REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES
                )
            },
            observed={
                "proposal_boundary_blocking_conditions": proposal_metadata.get(
                    "proposal_boundary_blocking_conditions"
                )
            },
        ),
        _check_from_expected(
            "proposal_boundary_sections_complete_check",
            expected={
                "proposal_boundary_section_names": list(
                    REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES
                )
            },
            observed={
                "proposal_boundary_section_names": _section_names(sections)
            },
        ),
        _check_from_expected(
            "proposal_boundary_sections_pass_check",
            expected={"proposal_boundary_sections_pass": True},
            observed={
                "proposal_boundary_sections_pass": _sections_pass(sections)
            },
        ),
        _check_from_expected(
            "proposal_boundary_contracts_pass_check",
            expected={"proposal_boundary_contracts_pass": True},
            observed={
                "proposal_boundary_contracts_pass": _contracts_pass(contracts)
            },
        ),
        _check_from_expected(
            "candidate_only_boundary_check",
            expected={
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed={
                "candidate_only": proposal_metadata.get("candidate_only"),
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        _check_from_expected(
            "future_cross_system_coordination_not_entered_check",
            expected={
                "future_cross_system_coordination_status": (
                    FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
                )
            },
            observed={
                "future_cross_system_coordination_status": proposal_metadata.get(
                    "future_cross_system_coordination_status"
                )
            },
        ),
        *_flag_checks(proposal_metadata),
        _check_from_expected(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": proposal_metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": proposal_metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
        _check_from_expected(
            "deterministic_operation_ledger_proposal_boundary_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM
                ),
                "hash_projection_declared": True,
            },
            observed={
                "hash_algorithm": HASH_INPUT_CONTRACT["algorithm"],
                "hash_projection_declared": (
                    HASH_INPUT_CONTRACT["hash_fields"]
                    == list(_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_FIELDS)
                ),
            },
        ),
        _check_from_expected(
            "proposal_boundary_readiness_check",
            expected={
                "proposal_boundary_handoff_status": READY_HANDOFF_STATUS,
                "proposal_boundary_sections_pass": True,
                "proposal_boundary_contracts_pass": True,
            },
            observed={
                "proposal_boundary_handoff_status": proposal_metadata.get(
                    "proposal_boundary_handoff_status"
                ),
                "proposal_boundary_sections_pass": _sections_pass(sections),
                "proposal_boundary_contracts_pass": _contracts_pass(contracts),
            },
        ),
    ]
    return _detached_json_value(checks)


def _flag_contracts(
    proposal_metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
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
        (
            "no_operation_ledger_entry_created_contract",
            "operation_ledger_entry_created",
        ),
        (
            "no_operation_ledger_entry_written_contract",
            "operation_ledger_entry_written",
        ),
        (
            "no_operation_ledger_proposal_persisted_contract",
            "operation_ledger_proposal_persisted",
        ),
        (
            "no_operation_ledger_proposal_submitted_contract",
            "operation_ledger_proposal_submitted",
        ),
        (
            "no_operation_ledger_proposal_dispatched_contract",
            "operation_ledger_proposal_dispatched",
        ),
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
            observed={field_name: proposal_metadata.get(field_name)},
        )
        for contract_name, field_name in flag_specs
    ]


def _flag_checks(
    proposal_metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
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
        (
            "no_operation_ledger_entry_created_check",
            "operation_ledger_entry_created",
        ),
        (
            "no_operation_ledger_entry_written_check",
            "operation_ledger_entry_written",
        ),
        (
            "no_operation_ledger_proposal_persisted_check",
            "operation_ledger_proposal_persisted",
        ),
        (
            "no_operation_ledger_proposal_submitted_check",
            "operation_ledger_proposal_submitted",
        ),
        (
            "no_operation_ledger_proposal_dispatched_check",
            "operation_ledger_proposal_dispatched",
        ),
        ("no_real_approval_record_check", "real_approval_record_written"),
        ("no_approval_notification_check", "approval_notification_sent"),
        (
            "no_execution_authorization_issued_check",
            "execution_authorization_issued",
        ),
        ("no_authorization_token_created_check", "authorization_token_created"),
        ("no_authorization_grant_created_check", "authorization_grant_created"),
        ("no_adapter_sandbox_entry_check", "adapter_sandbox_entered"),
    )
    return [
        _check_from_expected(
            check_name,
            expected={field_name: False},
            observed={field_name: proposal_metadata.get(field_name)},
        )
        for check_name, field_name in flag_specs
    ]


def _boundary_summary(
    boundary_status: str,
    handoff_audit: Mapping[str, Any],
    repeated_handoff_audit: Mapping[str, Any],
    proposal_metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    handoff_hash = _string_or_none(
        handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    repeated_hash = _string_or_none(
        repeated_handoff_audit.get("deterministic_adapter_handoff_audit_hash")
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "operation_ledger_proposal_boundary_summary",
            "operation_ledger_proposal_boundary_status": boundary_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if boundary_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "operation_ledger_proposal_mode": OPERATION_LEDGER_PROPOSAL_MODE,
            "operation_ledger_entry_status": OPERATION_LEDGER_ENTRY_STATUS,
            "operation_ledger_write_status": OPERATION_LEDGER_WRITE_STATUS,
            "future_cross_system_coordination_status": (
                FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "adapter_handoff_audit_version": _string_or_none(
                handoff_audit.get("version")
            ),
            "adapter_handoff_audit_status": _string_or_none(
                handoff_audit.get("adapter_handoff_audit_status")
            ),
            "adapter_handoff_audit_hash_present": _is_sha256(handoff_hash),
            "adapter_handoff_audit_hash_stable": (
                _is_sha256(handoff_hash) and handoff_hash == repeated_hash
            ),
            "proposal_metadata_valid": _proposal_metadata_valid(
                proposal_metadata
            ),
            "proposal_boundary_section_count": len(sections),
            "proposal_boundary_sections_pass": _sections_pass(sections),
            "proposal_boundary_contract_count": len(contracts),
            "proposal_boundary_contracts_pass": _contracts_pass(contracts),
            "proposal_boundary_check_count": len(checks),
            "proposal_boundary_checks_pass": _checks_pass(checks),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_expected(
    section_name: str,
    *,
    section_type: str,
    source_handoff_audit_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    proposal_notes: Sequence[str],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "operation ledger proposal boundary section values must match",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": section_name,
            "section_type": section_type,
            "section_status": "pass" if not blocking_reasons else "blocked",
            "source_handoff_audit_refs": list(source_handoff_audit_refs),
            "expected": dict(expected),
            "observed": dict(observed),
            "proposal_notes": list(proposal_notes),
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
        "operation ledger proposal boundary contract values must match",
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
        "operation ledger proposal boundary check values must match",
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
            "section_type": "unknown_operation_ledger_proposal_boundary_section",
            "section_status": "blocked",
            "source_handoff_audit_refs": [],
            "expected": {"known_section_name": True},
            "observed": {
                "known_section_name": False,
                "requested_section_name": name,
            },
            "proposal_notes": [],
            "blocking_reasons": [
                "operation ledger proposal boundary section name is not recognized"
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
            "contract_type": "unknown_operation_ledger_proposal_boundary_contract",
            "expected": {"known_contract_name": True},
            "observed": {
                "known_contract_name": False,
                "requested_contract_name": name,
            },
            "contract_status": "blocked",
            "blocking_reasons": [
                "operation ledger proposal boundary contract name is not recognized"
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
                "operation ledger proposal boundary check name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _operation_ledger_proposal_boundary_hash(
    result: Mapping[str, Any],
) -> str:
    projection = {
        field: result[field]
        for field in _OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_FIELDS
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


def _adapter_handoff_audit_passes(
    handoff_audit: Mapping[str, Any],
) -> bool:
    return (
        handoff_audit.get("adapter_handoff_audit_status") == "pass"
        and handoff_audit.get("version")
        == GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION
        and _is_sha256(
            _string_or_none(
                handoff_audit.get("deterministic_adapter_handoff_audit_hash")
            )
        )
    )


def _handoff_metadata(
    handoff_audit: Mapping[str, Any],
) -> Mapping[str, Any]:
    metadata = handoff_audit.get("adapter_handoff_audit_metadata")
    return metadata if isinstance(metadata, Mapping) else {}


def _handoff_metadata_is_valid(
    handoff_audit: Mapping[str, Any],
) -> bool:
    metadata = _handoff_metadata(handoff_audit)
    return (
        metadata.get("handoff_audit_metadata_mode") == "metadata_only"
        and metadata.get("handoff_audit_status") == "not_handed_off"
        and metadata.get("candidate_only") is True
        and metadata.get("approval_metadata_only") is True
        and metadata.get("authorization_metadata_only") is True
        and metadata.get("future_adapter_sandbox_status") == "not_entered"
    )


def _proposal_metadata_valid(
    proposal_metadata: Mapping[str, Any],
) -> bool:
    return (
        proposal_metadata.get("proposal_metadata_type")
        == "future_operation_ledger_proposal_boundary_metadata"
        and proposal_metadata.get("proposal_metadata_mode")
        == OPERATION_LEDGER_PROPOSAL_MODE
        and proposal_metadata.get("proposal_status") == "metadata_only_proposal"
        and proposal_metadata.get("operation_ledger_entry_status")
        == OPERATION_LEDGER_ENTRY_STATUS
        and proposal_metadata.get("operation_ledger_write_status")
        == OPERATION_LEDGER_WRITE_STATUS
        and proposal_metadata.get("future_cross_system_coordination_status")
        == FUTURE_CROSS_SYSTEM_COORDINATION_STATUS
        and proposal_metadata.get("proposal_required") is True
        and proposal_metadata.get("proposal_metadata_available") is True
        and proposal_metadata.get("proposal_persisted") is False
        and proposal_metadata.get("proposal_submitted") is False
        and proposal_metadata.get("proposal_dispatched") is False
        and proposal_metadata.get("candidate_only") is True
        and proposal_metadata.get("adapter_handoff_audit_pass_required") is True
        and proposal_metadata.get("adapter_handoff_audit_hash_required") is True
        and proposal_metadata.get("adapter_handoff_audit_status") == "pass"
        and proposal_metadata.get("adapter_handoff_audit_hash_present") is True
        and proposal_metadata.get("adapter_handoff_audit_hash_stable") is True
        and proposal_metadata.get("handoff_metadata_only") is True
        and proposal_metadata.get("approval_metadata_only") is True
        and proposal_metadata.get("authorization_metadata_only") is True
        and proposal_metadata.get("future_adapter_sandbox_not_entered") is True
        and proposal_metadata.get("proposal_boundary_readiness_conditions")
        == list(REQUIRED_PROPOSAL_READINESS_CONDITION_NAMES)
        and proposal_metadata.get("required_proposal_evidence")
        == list(REQUIRED_PROPOSAL_EVIDENCE_REQUIREMENT_NAMES)
        and proposal_metadata.get("proposal_boundary_blocking_conditions")
        == list(REQUIRED_PROPOSAL_BLOCKING_CONDITION_NAMES)
        and proposal_metadata.get("proposal_boundary_next_stage")
        == "cross_system_coordination_boundary"
        and proposal_metadata.get("proposal_boundary_handoff_status")
        == READY_HANDOFF_STATUS
        and _all_common_disabled_flags_false(proposal_metadata)
        and _all_safety_boundaries_false(proposal_metadata)
    )


def _sections_pass(sections: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [section.get("section_name") for section in sections]
        == list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SECTION_NAMES)
        and all(section.get("section_status") == "pass" for section in sections)
    )


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [contract.get("contract_name") for contract in contracts]
        == list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CONTRACT_NAMES)
        and all(
            contract.get("contract_status") == "pass" for contract in contracts
        )
    )


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [check.get("check_name") for check in checks]
        == list(REQUIRED_OPERATION_LEDGER_PROPOSAL_BOUNDARY_CHECK_NAMES)
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
        if _detached_json_value(dict(expected))
        == _detached_json_value(dict(observed))
        else [message]
    )


def _all_common_disabled_flags_false(value: Mapping[str, Any]) -> bool:
    return all(value.get(key) is False for key in COMMON_DISABLED_FLAGS)


def _upstream_disabled_boundaries_hold(value: Mapping[str, Any]) -> bool:
    upstream_fields = (
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
    return all(value.get(key) is False for key in upstream_fields)


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
    "FUTURE_CROSS_SYSTEM_COORDINATION_STATUS",
    "GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_HASH_ALGORITHM",
    "GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_SCHEMA_VERSION",
    "GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_TYPE",
    "GOVERNANCE_OPERATION_LEDGER_PROPOSAL_BOUNDARY_VERSION",
    "OPERATION_LEDGER_ENTRY_STATUS",
    "OPERATION_LEDGER_PROPOSAL_BOUNDARY_MODE",
    "OPERATION_LEDGER_PROPOSAL_BOUNDARY_STAGE",
    "OPERATION_LEDGER_PROPOSAL_MODE",
    "OPERATION_LEDGER_WRITE_STATUS",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_operation_ledger_proposal_boundary",
    "get_governance_operation_ledger_proposal_boundary_check",
    "get_governance_operation_ledger_proposal_boundary_contract",
    "get_governance_operation_ledger_proposal_boundary_section",
    "governance_operation_ledger_proposal_boundary_to_json",
    "list_governance_operation_ledger_proposal_boundary_check_names",
    "list_governance_operation_ledger_proposal_boundary_contract_names",
    "list_governance_operation_ledger_proposal_boundary_section_names",
]
