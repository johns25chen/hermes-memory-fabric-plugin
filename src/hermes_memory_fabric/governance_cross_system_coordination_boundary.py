"""Deterministic cross-system coordination boundary metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_operation_ledger_proposal_boundary import (
    build_governance_operation_ledger_proposal_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION = "6.3.0"
GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_SCHEMA_VERSION = "6.3.0"
GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_TYPE = (
    "governance_cross_system_coordination_boundary"
)
GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM = "sha256"
CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE = (
    "v5.10_cross_system_coordination_boundary"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE = (
    "cross_system_coordination_boundary_only"
)
CROSS_SYSTEM_COORDINATION_MODE = "metadata_only"
CROSS_SYSTEM_COORDINATION_STATUS = "not_started"
HERMES_COORDINATION_STATUS = "not_connected"
CODEX_COORDINATION_STATUS = "not_connected"
OPENCLAW_COORDINATION_STATUS = "not_connected"
GITHUB_COORDINATION_STATUS = "not_connected"
TOOL_ROUTING_STATUS = "not_configured"
COMMAND_ROUTING_STATUS = "not_configured"
SYSTEM_HANDOFF_STATUS = "not_handed_off"
FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS = "not_entered"

READY_HANDOFF_STATUS = "ready_for_controlled_adapter_sandbox_candidate_design"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "hermes_connected": False,
    "codex_connected": False,
    "openclaw_connected": False,
    "github_connected": False,
    "tool_routing_enabled": False,
    "command_routing_enabled": False,
    "cross_system_coordination_enabled": False,
    "system_handoff_completed": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "adapter_dispatched": False,
    "manifest_dispatched": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "real_execution_enabled": False,
    "external_calls_enabled": False,
    "network_calls_enabled": False,
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

REQUIRED_COORDINATION_READINESS_CONDITION_NAMES = (
    "operation_ledger_proposal_boundary_pass",
    "operation_ledger_proposal_boundary_hash_present",
    "operation_ledger_proposal_boundary_hash_stable",
    "operation_ledger_entry_not_created",
    "operation_ledger_write_not_written",
    "operation_ledger_proposal_not_persisted",
    "operation_ledger_proposal_not_submitted",
    "operation_ledger_proposal_not_dispatched",
    "cross_system_coordination_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "metadata_only_boundary_confirmed",
    "candidate_only_boundary_confirmed",
    "no_real_execution",
    "no_adapter_invocation",
    "no_adapter_dispatch",
    "no_manifest_dispatch",
    "no_manifest_execution",
    "no_dry_run_plan_execution",
    "no_external_calls",
    "no_network_calls",
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

REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES = (
    "operation_ledger_proposal_boundary_pass_evidence",
    "deterministic_operation_ledger_proposal_boundary_hash_evidence",
    "operation_ledger_proposal_metadata_evidence",
    "coordination_metadata_evidence",
    "hermes_not_connected_evidence",
    "codex_not_connected_evidence",
    "openclaw_not_connected_evidence",
    "github_not_connected_evidence",
    "tool_routing_not_configured_evidence",
    "command_routing_not_configured_evidence",
    "system_handoff_not_completed_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_adapter_dispatch_evidence",
    "no_manifest_dispatch_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_network_call_evidence",
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

REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES = (
    "operation_ledger_proposal_boundary_blocked",
    "missing_operation_ledger_proposal_boundary_hash",
    "unstable_operation_ledger_proposal_boundary_hash",
    "coordination_metadata_invalid",
    "candidate_only_boundary_missing",
    "cross_system_coordination_started",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "tool_routing_configured",
    "command_routing_configured",
    "system_handoff_completed",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "adapter_dispatch_enabled",
    "manifest_dispatch_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "network_calls_enabled",
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

REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES = (
    "operation_ledger_proposal_boundary_input_section",
    "coordination_metadata_section",
    "hermes_boundary_section",
    "codex_boundary_section",
    "openclaw_boundary_section",
    "github_boundary_section",
    "tool_routing_disabled_section",
    "command_routing_disabled_section",
    "runtime_disabled_boundary_section",
    "write_disabled_boundary_section",
    "external_call_disabled_boundary_section",
    "network_call_disabled_boundary_section",
    "operation_ledger_write_disabled_section",
    "adapter_sandbox_not_entered_section",
    "star_cosmos_candidate_only_section",
    "future_controlled_adapter_sandbox_readiness_section",
)

REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES = (
    "cross_system_coordination_boundary_only_contract",
    "cross_system_coordination_metadata_only_contract",
    "operation_ledger_proposal_boundary_pass_contract",
    "operation_ledger_proposal_boundary_hash_present_contract",
    "operation_ledger_proposal_boundary_hash_stable_contract",
    "coordination_readiness_conditions_declared_contract",
    "coordination_evidence_requirements_declared_contract",
    "coordination_blocking_conditions_declared_contract",
    "coordination_boundary_sections_complete_contract",
    "coordination_boundary_sections_pass_contract",
    "candidate_only_boundary_contract",
    "hermes_not_connected_contract",
    "codex_not_connected_contract",
    "openclaw_not_connected_contract",
    "github_not_connected_contract",
    "tool_routing_not_configured_contract",
    "command_routing_not_configured_contract",
    "system_handoff_not_completed_contract",
    "no_real_execution_contract",
    "no_adapter_invocation_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_manifest_execution_contract",
    "no_dry_run_plan_execution_contract",
    "no_external_call_contract",
    "no_network_call_contract",
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

REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES = (
    "cross_system_coordination_boundary_stage_check",
    "cross_system_coordination_boundary_only_mode_check",
    "cross_system_coordination_metadata_only_check",
    "cross_system_coordination_not_started_check",
    "hermes_not_connected_check",
    "codex_not_connected_check",
    "openclaw_not_connected_check",
    "github_not_connected_check",
    "tool_routing_not_configured_check",
    "command_routing_not_configured_check",
    "system_handoff_not_completed_check",
    "operation_ledger_proposal_boundary_pass_check",
    "operation_ledger_proposal_boundary_hash_present_check",
    "operation_ledger_proposal_boundary_hash_stable_check",
    "coordination_readiness_conditions_declared_check",
    "coordination_evidence_requirements_declared_check",
    "coordination_blocking_conditions_declared_check",
    "coordination_boundary_sections_complete_check",
    "coordination_boundary_sections_pass_check",
    "coordination_boundary_contracts_pass_check",
    "candidate_only_boundary_check",
    "no_real_execution_check",
    "no_adapter_invocation_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_manifest_execution_check",
    "no_dry_run_plan_execution_check",
    "no_external_call_check",
    "no_network_call_check",
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
    "deterministic_cross_system_coordination_boundary_hash_check",
    "coordination_boundary_readiness_check",
)

_OPERATION_LEDGER_PROPOSAL_REFS = (
    "operation_ledger_proposal_boundary_status",
    "deterministic_operation_ledger_proposal_boundary_hash",
    "operation_ledger_proposal_metadata",
)

_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_FIELDS = (
    "version",
    "schema_version",
    "cross_system_coordination_boundary_type",
    "cross_system_coordination_boundary_status",
    "cross_system_coordination_boundary_stage",
    "cross_system_coordination_boundary_mode",
    "cross_system_coordination_mode",
    "cross_system_coordination_status",
    "hermes_coordination_status",
    "codex_coordination_status",
    "openclaw_coordination_status",
    "github_coordination_status",
    "tool_routing_status",
    "command_routing_status",
    "system_handoff_status",
    "future_controlled_adapter_sandbox_status",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "operation_ledger_proposal_boundary_version",
    "operation_ledger_proposal_boundary_status",
    "operation_ledger_proposal_boundary_hash",
    "cross_system_coordination_metadata",
    "cross_system_coordination_boundary_sections",
    "cross_system_coordination_boundary_contracts",
    "cross_system_coordination_boundary_checks",
    "cross_system_coordination_boundary_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_FIELDS),
    "input_shape": "sanitized cross-system coordination boundary projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_operation_ledger_proposal_boundary_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_FLAG_CONTRACT_SPECS = (
    ("hermes_not_connected_contract", "hermes_connected"),
    ("codex_not_connected_contract", "codex_connected"),
    ("openclaw_not_connected_contract", "openclaw_connected"),
    ("github_not_connected_contract", "github_connected"),
    ("tool_routing_not_configured_contract", "tool_routing_enabled"),
    ("command_routing_not_configured_contract", "command_routing_enabled"),
    ("system_handoff_not_completed_contract", "system_handoff_completed"),
    ("no_real_execution_contract", "real_execution_enabled"),
    ("no_adapter_invocation_contract", "execution_adapter_invoked"),
    ("no_adapter_dispatch_contract", "adapter_dispatched"),
    ("no_manifest_dispatch_contract", "manifest_dispatched"),
    ("no_manifest_execution_contract", "manifest_executed"),
    ("no_dry_run_plan_execution_contract", "dry_run_plan_executed"),
    ("no_external_call_contract", "external_calls_enabled"),
    ("no_network_call_contract", "network_calls_enabled"),
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

_FLAG_CHECK_SPECS = (
    ("hermes_not_connected_check", "hermes_connected"),
    ("codex_not_connected_check", "codex_connected"),
    ("openclaw_not_connected_check", "openclaw_connected"),
    ("github_not_connected_check", "github_connected"),
    ("tool_routing_not_configured_check", "tool_routing_enabled"),
    ("command_routing_not_configured_check", "command_routing_enabled"),
    ("system_handoff_not_completed_check", "system_handoff_completed"),
    ("no_real_execution_check", "real_execution_enabled"),
    ("no_adapter_invocation_check", "execution_adapter_invoked"),
    ("no_adapter_dispatch_check", "adapter_dispatched"),
    ("no_manifest_dispatch_check", "manifest_dispatched"),
    ("no_manifest_execution_check", "manifest_executed"),
    ("no_dry_run_plan_execution_check", "dry_run_plan_executed"),
    ("no_external_call_check", "external_calls_enabled"),
    ("no_network_call_check", "network_calls_enabled"),
    ("no_durable_write_check", "durable_writes_enabled"),
    ("no_filesystem_write_check", "filesystem_writes_enabled"),
    ("no_database_write_check", "database_writes_enabled"),
    ("no_memory_graph_mutation_check", "memory_graph_mutation_enabled"),
    ("no_operation_ledger_write_check", "operation_ledger_writes_enabled"),
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


def build_governance_cross_system_coordination_boundary() -> dict[str, Any]:
    """Build deterministic coordination-boundary-only metadata."""

    proposal_boundary, repeated_proposal_boundary = _proposal_boundary_pair()
    coordination_metadata = _build_coordination_metadata(
        proposal_boundary,
        repeated_proposal_boundary,
    )
    sections = _build_boundary_sections(
        proposal_boundary,
        repeated_proposal_boundary,
        coordination_metadata,
    )
    contracts = _build_boundary_contracts(
        proposal_boundary,
        repeated_proposal_boundary,
        coordination_metadata,
        sections,
    )
    checks = _build_boundary_checks(
        proposal_boundary,
        repeated_proposal_boundary,
        coordination_metadata,
        sections,
        contracts,
    )

    proposal_boundary_passes = _proposal_boundary_passes(proposal_boundary)
    metadata_valid = _coordination_metadata_valid(coordination_metadata)
    sections_pass = _sections_pass(sections)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    boundary_status = (
        "pass"
        if proposal_boundary_passes
        and metadata_valid
        and sections_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["operation ledger proposal boundary must pass at version 6.3.0"]
                if not proposal_boundary_passes
                else []
            ),
            *(
                ["cross-system coordination metadata must remain metadata-only"]
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
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION,
        "schema_version": (
            GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_SCHEMA_VERSION
        ),
        "cross_system_coordination_boundary_type": (
            GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_TYPE
        ),
        "cross_system_coordination_boundary_status": boundary_status,
        "cross_system_coordination_boundary_stage": (
            CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE
        ),
        "cross_system_coordination_boundary_mode": (
            CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
        ),
        "cross_system_coordination_mode": CROSS_SYSTEM_COORDINATION_MODE,
        "cross_system_coordination_status": CROSS_SYSTEM_COORDINATION_STATUS,
        "hermes_coordination_status": HERMES_COORDINATION_STATUS,
        "codex_coordination_status": CODEX_COORDINATION_STATUS,
        "openclaw_coordination_status": OPENCLAW_COORDINATION_STATUS,
        "github_coordination_status": GITHUB_COORDINATION_STATUS,
        "tool_routing_status": TOOL_ROUTING_STATUS,
        "command_routing_status": COMMAND_ROUTING_STATUS,
        "system_handoff_status": SYSTEM_HANDOFF_STATUS,
        "future_controlled_adapter_sandbox_status": (
            FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
        ),
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "operation_ledger_proposal_boundary_version": _string_or_none(
            proposal_boundary.get("version")
        ),
        "operation_ledger_proposal_boundary_status": _string_or_none(
            proposal_boundary.get("operation_ledger_proposal_boundary_status")
        ),
        "operation_ledger_proposal_boundary_hash": proposal_hash,
        "cross_system_coordination_metadata": coordination_metadata,
        "cross_system_coordination_boundary_sections": sections,
        "cross_system_coordination_boundary_contracts": contracts,
        "cross_system_coordination_boundary_checks": checks,
        "cross_system_coordination_boundary_summary": _boundary_summary(
            boundary_status,
            proposal_boundary,
            repeated_proposal_boundary,
            coordination_metadata,
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
    result["deterministic_cross_system_coordination_boundary_hash"] = (
        _cross_system_coordination_boundary_hash(result)
    )
    return _detached_json_value(result)


def get_governance_cross_system_coordination_boundary_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached coordination boundary section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_boundary()[
        "cross_system_coordination_boundary_sections"
    ]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_cross_system_coordination_boundary_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached coordination boundary contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_boundary()[
        "cross_system_coordination_boundary_contracts"
    ]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_cross_system_coordination_boundary_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached coordination boundary check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_boundary()["cross_system_coordination_boundary_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_cross_system_coordination_boundary_section_names() -> list[str]:
    """Return stable coordination boundary section names."""

    return list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES)


def list_governance_cross_system_coordination_boundary_contract_names() -> list[str]:
    """Return stable coordination boundary contract names."""

    return list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES)


def list_governance_cross_system_coordination_boundary_check_names() -> list[str]:
    """Return stable coordination boundary check names."""

    return list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES)


def governance_cross_system_coordination_boundary_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize cross-system coordination boundary metadata deterministically."""

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
    return governance_cross_system_coordination_boundary_to_json(
        build_governance_cross_system_coordination_boundary()
    )


def _cached_boundary() -> dict[str, Any]:
    return json.loads(_cached_boundary_payload())


@lru_cache(maxsize=1)
def _cached_proposal_boundary_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_operation_ledger_proposal_boundary()
    )
    second = _detached_json_value(
        build_governance_operation_ledger_proposal_boundary()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _proposal_boundary_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_proposal_boundary_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_coordination_metadata(
    proposal_boundary: Mapping[str, Any],
    repeated_proposal_boundary: Mapping[str, Any],
) -> dict[str, Any]:
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    repeated_hash = _proposal_boundary_hash(repeated_proposal_boundary)
    hash_present = _is_sha256(proposal_hash)
    hash_stable = hash_present and proposal_hash == repeated_hash
    coordination_ready = (
        _proposal_boundary_passes(proposal_boundary)
        and hash_stable
        and _proposal_metadata_evidence_valid(proposal_boundary)
        and _upstream_disabled_boundaries_hold(proposal_boundary)
        and _all_safety_boundaries_false(proposal_boundary)
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "coordination_metadata_type": (
                "future_cross_system_coordination_boundary_metadata"
            ),
            "coordination_metadata_mode": CROSS_SYSTEM_COORDINATION_MODE,
            "coordination_status": "metadata_only_boundary",
            "cross_system_coordination_status": CROSS_SYSTEM_COORDINATION_STATUS,
            "hermes_coordination_status": HERMES_COORDINATION_STATUS,
            "codex_coordination_status": CODEX_COORDINATION_STATUS,
            "openclaw_coordination_status": OPENCLAW_COORDINATION_STATUS,
            "github_coordination_status": GITHUB_COORDINATION_STATUS,
            "tool_routing_status": TOOL_ROUTING_STATUS,
            "command_routing_status": COMMAND_ROUTING_STATUS,
            "system_handoff_status": SYSTEM_HANDOFF_STATUS,
            "future_controlled_adapter_sandbox_status": (
                FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
            ),
            "coordination_required": True,
            "coordination_metadata_available": True,
            "coordination_established": False,
            "coordination_persisted": False,
            "coordination_submitted": False,
            "coordination_dispatched": False,
            "candidate_only": True,
            "operation_ledger_proposal_boundary_pass_required": True,
            "operation_ledger_proposal_boundary_hash_required": True,
            "operation_ledger_proposal_boundary_status": _string_or_none(
                proposal_boundary.get(
                    "operation_ledger_proposal_boundary_status"
                )
            ),
            "operation_ledger_proposal_boundary_hash_present": hash_present,
            "operation_ledger_proposal_boundary_hash_stable": hash_stable,
            "operation_ledger_proposal_metadata_available": (
                _proposal_metadata_evidence_valid(proposal_boundary)
            ),
            "coordination_boundary_readiness_conditions": list(
                REQUIRED_COORDINATION_READINESS_CONDITION_NAMES
            ),
            "required_coordination_evidence": list(
                REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES
            ),
            "coordination_boundary_blocking_conditions": list(
                REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES
            ),
            "coordination_boundary_next_stage": (
                "controlled_adapter_sandbox_candidate"
            ),
            "coordination_boundary_handoff_status": (
                READY_HANDOFF_STATUS
                if coordination_ready
                else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_boundary_sections(
    proposal_boundary: Mapping[str, Any],
    repeated_proposal_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    repeated_hash = _proposal_boundary_hash(repeated_proposal_boundary)
    section_specs = (
        (
            "operation_ledger_proposal_boundary_input_section",
            "operation_ledger_proposal_boundary_input",
            {
                "operation_ledger_proposal_boundary_version": (
                    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION
                ),
                "operation_ledger_proposal_boundary_status": "pass",
                "operation_ledger_proposal_boundary_hash_present": True,
                "operation_ledger_proposal_boundary_hash_stable": True,
                "operation_ledger_proposal_metadata_available": True,
            },
            {
                "operation_ledger_proposal_boundary_version": _string_or_none(
                    proposal_boundary.get("version")
                ),
                "operation_ledger_proposal_boundary_status": _string_or_none(
                    proposal_boundary.get(
                        "operation_ledger_proposal_boundary_status"
                    )
                ),
                "operation_ledger_proposal_boundary_hash_present": _is_sha256(
                    proposal_hash
                ),
                "operation_ledger_proposal_boundary_hash_stable": (
                    _is_sha256(proposal_hash)
                    and proposal_hash == repeated_hash
                ),
                "operation_ledger_proposal_metadata_available": (
                    _proposal_metadata_evidence_valid(proposal_boundary)
                ),
            },
            ("Consumes detached deterministic proposal-boundary metadata.",),
        ),
        (
            "coordination_metadata_section",
            "cross_system_coordination_metadata_boundary",
            {
                "coordination_metadata_mode": CROSS_SYSTEM_COORDINATION_MODE,
                "coordination_status": "metadata_only_boundary",
                "coordination_metadata_available": True,
                "coordination_established": False,
                "coordination_persisted": False,
                "coordination_submitted": False,
                "coordination_dispatched": False,
            },
            {
                key: metadata.get(key)
                for key in (
                    "coordination_metadata_mode",
                    "coordination_status",
                    "coordination_metadata_available",
                    "coordination_established",
                    "coordination_persisted",
                    "coordination_submitted",
                    "coordination_dispatched",
                )
            },
            ("Defines coordination boundary metadata without coordination.",),
        ),
        *_system_section_specs(metadata),
        (
            "tool_routing_disabled_section",
            "tool_routing_disabled_boundary",
            {
                "tool_routing_status": TOOL_ROUTING_STATUS,
                "tool_routing_enabled": False,
            },
            {
                "tool_routing_status": metadata.get("tool_routing_status"),
                "tool_routing_enabled": metadata.get("tool_routing_enabled"),
            },
            ("Keeps tool routing unconfigured and disabled.",),
        ),
        (
            "command_routing_disabled_section",
            "command_routing_disabled_boundary",
            {
                "command_routing_status": COMMAND_ROUTING_STATUS,
                "command_routing_enabled": False,
            },
            {
                "command_routing_status": metadata.get(
                    "command_routing_status"
                ),
                "command_routing_enabled": metadata.get(
                    "command_routing_enabled"
                ),
            },
            ("Keeps command routing unconfigured and disabled.",),
        ),
        (
            "runtime_disabled_boundary_section",
            "runtime_disabled_boundary",
            {
                "cross_system_coordination_status": (
                    CROSS_SYSTEM_COORDINATION_STATUS
                ),
                "cross_system_coordination_enabled": False,
                "system_handoff_status": SYSTEM_HANDOFF_STATUS,
                "system_handoff_completed": False,
                "real_execution_enabled": False,
                "execution_adapter_invoked": False,
                "adapter_dispatched": False,
                "manifest_dispatched": False,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
                "autonomous_execution_enabled": False,
            },
            {
                key: metadata.get(key)
                for key in (
                    "cross_system_coordination_status",
                    "cross_system_coordination_enabled",
                    "system_handoff_status",
                    "system_handoff_completed",
                    "real_execution_enabled",
                    "execution_adapter_invoked",
                    "adapter_dispatched",
                    "manifest_dispatched",
                    "manifest_executed",
                    "dry_run_plan_executed",
                    "autonomous_execution_enabled",
                )
            },
            ("Declares coordination and runtime surfaces disabled.",),
        ),
        (
            "write_disabled_boundary_section",
            "write_disabled_boundary",
            {
                "durable_writes_enabled": False,
                "filesystem_writes_enabled": False,
                "database_writes_enabled": False,
                "memory_graph_mutation_enabled": False,
            },
            {
                key: metadata.get(key)
                for key in (
                    "durable_writes_enabled",
                    "filesystem_writes_enabled",
                    "database_writes_enabled",
                    "memory_graph_mutation_enabled",
                )
            },
            ("Declares durable, filesystem, database, and graph writes disabled.",),
        ),
        (
            "external_call_disabled_boundary_section",
            "external_call_disabled_boundary",
            {"external_calls_enabled": False},
            {"external_calls_enabled": metadata.get("external_calls_enabled")},
            ("Declares external calls disabled.",),
        ),
        (
            "network_call_disabled_boundary_section",
            "network_call_disabled_boundary",
            {"network_calls_enabled": False},
            {"network_calls_enabled": metadata.get("network_calls_enabled")},
            ("Declares network calls disabled.",),
        ),
        (
            "operation_ledger_write_disabled_section",
            "operation_ledger_write_disabled_boundary",
            {
                "operation_ledger_writes_enabled": False,
                "operation_ledger_entry_created": False,
                "operation_ledger_entry_written": False,
                "operation_ledger_proposal_persisted": False,
                "operation_ledger_proposal_submitted": False,
                "operation_ledger_proposal_dispatched": False,
            },
            {
                key: metadata.get(key)
                for key in (
                    "operation_ledger_writes_enabled",
                    "operation_ledger_entry_created",
                    "operation_ledger_entry_written",
                    "operation_ledger_proposal_persisted",
                    "operation_ledger_proposal_submitted",
                    "operation_ledger_proposal_dispatched",
                )
            },
            ("Keeps operation-ledger entry and proposal writes absent.",),
        ),
        (
            "adapter_sandbox_not_entered_section",
            "adapter_sandbox_not_entered_boundary",
            {
                "future_controlled_adapter_sandbox_status": (
                    FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
                ),
                "adapter_sandbox_entered": False,
                "controlled_adapter_sandbox_started": False,
            },
            {
                "future_controlled_adapter_sandbox_status": metadata.get(
                    "future_controlled_adapter_sandbox_status"
                ),
                "adapter_sandbox_entered": metadata.get(
                    "adapter_sandbox_entered"
                ),
                "controlled_adapter_sandbox_started": metadata.get(
                    "controlled_adapter_sandbox_started"
                ),
            },
            ("The future controlled adapter sandbox is not entered.",),
        ),
        (
            "star_cosmos_candidate_only_section",
            "star_cosmos_candidate_only_boundary",
            {
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            {
                "candidate_only": metadata.get("candidate_only"),
                "star_cosmos_entry_status": metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
            ("Does not claim active Star-Cosmos entry.",),
        ),
        (
            "future_controlled_adapter_sandbox_readiness_section",
            "future_controlled_adapter_sandbox_readiness_boundary",
            {
                "coordination_boundary_next_stage": (
                    "controlled_adapter_sandbox_candidate"
                ),
                "coordination_boundary_handoff_status": READY_HANDOFF_STATUS,
                "future_controlled_adapter_sandbox_status": (
                    FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
                ),
                "coordination_boundary_readiness_conditions": list(
                    REQUIRED_COORDINATION_READINESS_CONDITION_NAMES
                ),
            },
            {
                "coordination_boundary_next_stage": metadata.get(
                    "coordination_boundary_next_stage"
                ),
                "coordination_boundary_handoff_status": metadata.get(
                    "coordination_boundary_handoff_status"
                ),
                "future_controlled_adapter_sandbox_status": metadata.get(
                    "future_controlled_adapter_sandbox_status"
                ),
                "coordination_boundary_readiness_conditions": metadata.get(
                    "coordination_boundary_readiness_conditions"
                ),
            },
            ("Marks readiness for future candidate design only.",),
        ),
    )
    return [
        _section_from_expected(
            name,
            section_type=section_type,
            source_operation_ledger_proposal_refs=(
                _OPERATION_LEDGER_PROPOSAL_REFS
            ),
            expected=expected,
            observed=observed,
            coordination_notes=notes,
        )
        for name, section_type, expected, observed, notes in section_specs
    ]


def _system_section_specs(
    metadata: Mapping[str, Any],
) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        (
            f"{system_name}_boundary_section",
            f"{system_name}_coordination_boundary",
            {
                f"{system_name}_coordination_status": status,
                f"{system_name}_connected": False,
            },
            {
                f"{system_name}_coordination_status": metadata.get(
                    f"{system_name}_coordination_status"
                ),
                f"{system_name}_connected": metadata.get(
                    f"{system_name}_connected"
                ),
            },
            (f"Keeps {display_name} disconnected.",),
        )
        for system_name, display_name, status in (
            ("hermes", "Hermes", HERMES_COORDINATION_STATUS),
            ("codex", "Codex", CODEX_COORDINATION_STATUS),
            ("openclaw", "OpenClaw", OPENCLAW_COORDINATION_STATUS),
            ("github", "GitHub", GITHUB_COORDINATION_STATUS),
        )
    )


def _build_boundary_contracts(
    proposal_boundary: Mapping[str, Any],
    repeated_proposal_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    repeated_hash = _proposal_boundary_hash(repeated_proposal_boundary)
    contracts = [
        _contract_from_expected(
            "cross_system_coordination_boundary_only_contract",
            contract_type="coordination_boundary_mode_contract",
            expected={
                "cross_system_coordination_boundary_mode": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
                )
            },
            observed={
                "cross_system_coordination_boundary_mode": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
                )
            },
        ),
        _contract_from_expected(
            "cross_system_coordination_metadata_only_contract",
            contract_type="coordination_metadata_mode_contract",
            expected={
                "coordination_metadata_mode": CROSS_SYSTEM_COORDINATION_MODE,
                "coordination_status": "metadata_only_boundary",
            },
            observed={
                "coordination_metadata_mode": metadata.get(
                    "coordination_metadata_mode"
                ),
                "coordination_status": metadata.get("coordination_status"),
            },
        ),
        _contract_from_expected(
            "operation_ledger_proposal_boundary_pass_contract",
            contract_type="proposal_boundary_status_contract",
            expected={
                "operation_ledger_proposal_boundary_version": (
                    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION
                ),
                "operation_ledger_proposal_boundary_status": "pass",
            },
            observed={
                "operation_ledger_proposal_boundary_version": _string_or_none(
                    proposal_boundary.get("version")
                ),
                "operation_ledger_proposal_boundary_status": _string_or_none(
                    proposal_boundary.get(
                        "operation_ledger_proposal_boundary_status"
                    )
                ),
            },
        ),
        _contract_from_expected(
            "operation_ledger_proposal_boundary_hash_present_contract",
            contract_type="proposal_boundary_hash_contract",
            expected={
                "operation_ledger_proposal_boundary_hash_present": True
            },
            observed={
                "operation_ledger_proposal_boundary_hash_present": _is_sha256(
                    proposal_hash
                )
            },
        ),
        _contract_from_expected(
            "operation_ledger_proposal_boundary_hash_stable_contract",
            contract_type="proposal_boundary_hash_contract",
            expected={
                "operation_ledger_proposal_boundary_hash_stable": True
            },
            observed={
                "operation_ledger_proposal_boundary_hash_stable": (
                    _is_sha256(proposal_hash)
                    and proposal_hash == repeated_hash
                )
            },
        ),
        *_requirements_contracts(metadata),
        _contract_from_expected(
            "coordination_boundary_sections_complete_contract",
            contract_type="coordination_boundary_sections_contract",
            expected={
                "coordination_boundary_section_names": list(
                    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES
                )
            },
            observed={
                "coordination_boundary_section_names": _section_names(sections)
            },
        ),
        _contract_from_expected(
            "coordination_boundary_sections_pass_contract",
            contract_type="coordination_boundary_sections_contract",
            expected={"coordination_boundary_sections_pass": True},
            observed={
                "coordination_boundary_sections_pass": _sections_pass(sections)
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
                "candidate_only": metadata.get("candidate_only"),
                "star_cosmos_entry_status": metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        *[
            _contract_from_expected(
                contract_name,
                contract_type="disabled_coordination_boundary_contract",
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for contract_name, field_name in _FLAG_CONTRACT_SPECS
        ],
        _contract_from_expected(
            "star_cosmos_candidate_only_contract",
            contract_type="star_cosmos_candidate_only_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
    ]
    return _detached_json_value(contracts)


def _requirements_contracts(
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs = (
        (
            "coordination_readiness_conditions_declared_contract",
            "coordination_boundary_readiness_conditions",
            list(REQUIRED_COORDINATION_READINESS_CONDITION_NAMES),
        ),
        (
            "coordination_evidence_requirements_declared_contract",
            "required_coordination_evidence",
            list(REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "coordination_blocking_conditions_declared_contract",
            "coordination_boundary_blocking_conditions",
            list(REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES),
        ),
    )
    return [
        _contract_from_expected(
            contract_name,
            contract_type="coordination_requirements_contract",
            expected={field_name: expected_value},
            observed={field_name: metadata.get(field_name)},
        )
        for contract_name, field_name, expected_value in specs
    ]


def _build_boundary_checks(
    proposal_boundary: Mapping[str, Any],
    repeated_proposal_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    repeated_hash = _proposal_boundary_hash(repeated_proposal_boundary)
    checks = [
        _check_from_expected(
            "cross_system_coordination_boundary_stage_check",
            expected={
                "cross_system_coordination_boundary_stage": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE
                )
            },
            observed={
                "cross_system_coordination_boundary_stage": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE
                )
            },
        ),
        _check_from_expected(
            "cross_system_coordination_boundary_only_mode_check",
            expected={
                "cross_system_coordination_boundary_mode": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
                )
            },
            observed={
                "cross_system_coordination_boundary_mode": (
                    CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE
                )
            },
        ),
        _check_from_expected(
            "cross_system_coordination_metadata_only_check",
            expected={
                "cross_system_coordination_mode": CROSS_SYSTEM_COORDINATION_MODE
            },
            observed={
                "cross_system_coordination_mode": metadata.get(
                    "coordination_metadata_mode"
                )
            },
        ),
        _check_from_expected(
            "cross_system_coordination_not_started_check",
            expected={
                "cross_system_coordination_status": (
                    CROSS_SYSTEM_COORDINATION_STATUS
                )
            },
            observed={
                "cross_system_coordination_status": metadata.get(
                    "cross_system_coordination_status"
                )
            },
        ),
        *[
            _check_from_expected(
                check_name,
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for check_name, field_name in _FLAG_CHECK_SPECS[:7]
        ],
        _check_from_expected(
            "operation_ledger_proposal_boundary_pass_check",
            expected={"operation_ledger_proposal_boundary_status": "pass"},
            observed={
                "operation_ledger_proposal_boundary_status": _string_or_none(
                    proposal_boundary.get(
                        "operation_ledger_proposal_boundary_status"
                    )
                )
            },
        ),
        _check_from_expected(
            "operation_ledger_proposal_boundary_hash_present_check",
            expected={
                "operation_ledger_proposal_boundary_hash_present": True
            },
            observed={
                "operation_ledger_proposal_boundary_hash_present": _is_sha256(
                    proposal_hash
                )
            },
        ),
        _check_from_expected(
            "operation_ledger_proposal_boundary_hash_stable_check",
            expected={
                "operation_ledger_proposal_boundary_hash_stable": True
            },
            observed={
                "operation_ledger_proposal_boundary_hash_stable": (
                    _is_sha256(proposal_hash)
                    and proposal_hash == repeated_hash
                )
            },
        ),
        *_requirements_checks(metadata),
        _check_from_expected(
            "coordination_boundary_sections_complete_check",
            expected={
                "coordination_boundary_section_names": list(
                    REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES
                )
            },
            observed={
                "coordination_boundary_section_names": _section_names(sections)
            },
        ),
        _check_from_expected(
            "coordination_boundary_sections_pass_check",
            expected={"coordination_boundary_sections_pass": True},
            observed={
                "coordination_boundary_sections_pass": _sections_pass(sections)
            },
        ),
        _check_from_expected(
            "coordination_boundary_contracts_pass_check",
            expected={"coordination_boundary_contracts_pass": True},
            observed={
                "coordination_boundary_contracts_pass": _contracts_pass(
                    contracts
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
                "candidate_only": metadata.get("candidate_only"),
                "star_cosmos_entry_status": metadata.get(
                    "star_cosmos_entry_status"
                ),
            },
        ),
        *[
            _check_from_expected(
                check_name,
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for check_name, field_name in _FLAG_CHECK_SPECS[7:]
        ],
        _check_from_expected(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": metadata.get(
                    "star_cosmos_entry_status"
                ),
                "star_cosmos_memory_active": metadata.get(
                    "star_cosmos_memory_active"
                ),
            },
        ),
        _check_from_expected(
            "deterministic_cross_system_coordination_boundary_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM
                ),
                "hash_projection_declared": True,
            },
            observed={
                "hash_algorithm": HASH_INPUT_CONTRACT["algorithm"],
                "hash_projection_declared": (
                    HASH_INPUT_CONTRACT["hash_fields"]
                    == list(_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_FIELDS)
                ),
            },
        ),
        _check_from_expected(
            "coordination_boundary_readiness_check",
            expected={
                "coordination_boundary_handoff_status": READY_HANDOFF_STATUS,
                "coordination_boundary_sections_pass": True,
                "coordination_boundary_contracts_pass": True,
            },
            observed={
                "coordination_boundary_handoff_status": metadata.get(
                    "coordination_boundary_handoff_status"
                ),
                "coordination_boundary_sections_pass": _sections_pass(sections),
                "coordination_boundary_contracts_pass": _contracts_pass(
                    contracts
                ),
            },
        ),
    ]
    return _detached_json_value(checks)


def _requirements_checks(
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs = (
        (
            "coordination_readiness_conditions_declared_check",
            "coordination_boundary_readiness_conditions",
            list(REQUIRED_COORDINATION_READINESS_CONDITION_NAMES),
        ),
        (
            "coordination_evidence_requirements_declared_check",
            "required_coordination_evidence",
            list(REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "coordination_blocking_conditions_declared_check",
            "coordination_boundary_blocking_conditions",
            list(REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES),
        ),
    )
    return [
        _check_from_expected(
            check_name,
            expected={field_name: expected_value},
            observed={field_name: metadata.get(field_name)},
        )
        for check_name, field_name, expected_value in specs
    ]


def _boundary_summary(
    boundary_status: str,
    proposal_boundary: Mapping[str, Any],
    repeated_proposal_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    proposal_hash = _proposal_boundary_hash(proposal_boundary)
    repeated_hash = _proposal_boundary_hash(repeated_proposal_boundary)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "cross_system_coordination_boundary_summary",
            "cross_system_coordination_boundary_status": boundary_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if boundary_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "cross_system_coordination_mode": CROSS_SYSTEM_COORDINATION_MODE,
            "cross_system_coordination_status": CROSS_SYSTEM_COORDINATION_STATUS,
            "system_handoff_status": SYSTEM_HANDOFF_STATUS,
            "future_controlled_adapter_sandbox_status": (
                FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "operation_ledger_proposal_boundary_version": _string_or_none(
                proposal_boundary.get("version")
            ),
            "operation_ledger_proposal_boundary_status": _string_or_none(
                proposal_boundary.get(
                    "operation_ledger_proposal_boundary_status"
                )
            ),
            "operation_ledger_proposal_boundary_hash_present": _is_sha256(
                proposal_hash
            ),
            "operation_ledger_proposal_boundary_hash_stable": (
                _is_sha256(proposal_hash) and proposal_hash == repeated_hash
            ),
            "coordination_metadata_valid": _coordination_metadata_valid(
                metadata
            ),
            "coordination_boundary_section_count": len(sections),
            "coordination_boundary_sections_pass": _sections_pass(sections),
            "coordination_boundary_contract_count": len(contracts),
            "coordination_boundary_contracts_pass": _contracts_pass(contracts),
            "coordination_boundary_check_count": len(checks),
            "coordination_boundary_checks_pass": _checks_pass(checks),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_expected(
    section_name: str,
    *,
    section_type: str,
    source_operation_ledger_proposal_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    coordination_notes: Sequence[str],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "cross-system coordination boundary section values must match",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": section_name,
            "section_type": section_type,
            "section_status": "pass" if not blocking_reasons else "blocked",
            "source_operation_ledger_proposal_refs": list(
                source_operation_ledger_proposal_refs
            ),
            "expected": dict(expected),
            "observed": dict(observed),
            "coordination_notes": list(coordination_notes),
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
        "cross-system coordination boundary contract values must match",
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
        "cross-system coordination boundary check values must match",
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
            "section_type": "unknown_cross_system_coordination_boundary_section",
            "section_status": "blocked",
            "source_operation_ledger_proposal_refs": [],
            "expected": {"known_section_name": True},
            "observed": {
                "known_section_name": False,
                "requested_section_name": name,
            },
            "coordination_notes": [],
            "blocking_reasons": [
                "cross-system coordination boundary section name is not recognized"
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
            "contract_type": (
                "unknown_cross_system_coordination_boundary_contract"
            ),
            "expected": {"known_contract_name": True},
            "observed": {
                "known_contract_name": False,
                "requested_contract_name": name,
            },
            "contract_status": "blocked",
            "blocking_reasons": [
                "cross-system coordination boundary contract name is not recognized"
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
                "cross-system coordination boundary check name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _cross_system_coordination_boundary_hash(
    result: Mapping[str, Any],
) -> str:
    projection = {
        field: result[field]
        for field in _CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_FIELDS
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


def _proposal_boundary_hash(
    proposal_boundary: Mapping[str, Any],
) -> str | None:
    return _string_or_none(
        proposal_boundary.get(
            "deterministic_operation_ledger_proposal_boundary_hash"
        )
    )


def _proposal_boundary_passes(
    proposal_boundary: Mapping[str, Any],
) -> bool:
    return (
        proposal_boundary.get("operation_ledger_proposal_boundary_status")
        == "pass"
        and proposal_boundary.get("version")
        == GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION
        and _is_sha256(_proposal_boundary_hash(proposal_boundary))
    )


def _proposal_metadata_evidence_valid(
    proposal_boundary: Mapping[str, Any],
) -> bool:
    proposal_metadata = proposal_boundary.get(
        "operation_ledger_proposal_metadata"
    )
    return (
        isinstance(proposal_metadata, Mapping)
        and proposal_metadata.get("proposal_metadata_mode") == "metadata_only"
        and proposal_metadata.get("proposal_metadata_available") is True
        and proposal_metadata.get("proposal_persisted") is False
        and proposal_metadata.get("proposal_submitted") is False
        and proposal_metadata.get("proposal_dispatched") is False
    )


def _coordination_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("coordination_metadata_type")
        == "future_cross_system_coordination_boundary_metadata"
        and metadata.get("coordination_metadata_mode")
        == CROSS_SYSTEM_COORDINATION_MODE
        and metadata.get("coordination_status") == "metadata_only_boundary"
        and metadata.get("cross_system_coordination_status")
        == CROSS_SYSTEM_COORDINATION_STATUS
        and metadata.get("hermes_coordination_status")
        == HERMES_COORDINATION_STATUS
        and metadata.get("codex_coordination_status")
        == CODEX_COORDINATION_STATUS
        and metadata.get("openclaw_coordination_status")
        == OPENCLAW_COORDINATION_STATUS
        and metadata.get("github_coordination_status")
        == GITHUB_COORDINATION_STATUS
        and metadata.get("tool_routing_status") == TOOL_ROUTING_STATUS
        and metadata.get("command_routing_status") == COMMAND_ROUTING_STATUS
        and metadata.get("system_handoff_status") == SYSTEM_HANDOFF_STATUS
        and metadata.get("future_controlled_adapter_sandbox_status")
        == FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS
        and metadata.get("coordination_required") is True
        and metadata.get("coordination_metadata_available") is True
        and metadata.get("coordination_established") is False
        and metadata.get("coordination_persisted") is False
        and metadata.get("coordination_submitted") is False
        and metadata.get("coordination_dispatched") is False
        and metadata.get("candidate_only") is True
        and metadata.get("operation_ledger_proposal_boundary_pass_required")
        is True
        and metadata.get("operation_ledger_proposal_boundary_hash_required")
        is True
        and metadata.get("operation_ledger_proposal_boundary_status") == "pass"
        and metadata.get(
            "operation_ledger_proposal_boundary_hash_present"
        )
        is True
        and metadata.get(
            "operation_ledger_proposal_boundary_hash_stable"
        )
        is True
        and metadata.get("operation_ledger_proposal_metadata_available") is True
        and metadata.get("coordination_boundary_readiness_conditions")
        == list(REQUIRED_COORDINATION_READINESS_CONDITION_NAMES)
        and metadata.get("required_coordination_evidence")
        == list(REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("coordination_boundary_blocking_conditions")
        == list(REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES)
        and metadata.get("coordination_boundary_next_stage")
        == "controlled_adapter_sandbox_candidate"
        and metadata.get("coordination_boundary_handoff_status")
        == READY_HANDOFF_STATUS
        and metadata.get("star_cosmos_entry_status")
        == STAR_COSMOS_ENTRY_STATUS
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _sections_pass(sections: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [section.get("section_name") for section in sections]
        == list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES)
        and all(section.get("section_status") == "pass" for section in sections)
    )


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [contract.get("contract_name") for contract in contracts]
        == list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES)
        and all(
            contract.get("contract_status") == "pass" for contract in contracts
        )
    )


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [check.get("check_name") for check in checks]
        == list(REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES)
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


def _upstream_disabled_boundaries_hold(
    value: Mapping[str, Any],
) -> bool:
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
    "CODEX_COORDINATION_STATUS",
    "COMMAND_ROUTING_STATUS",
    "COMMON_DISABLED_FLAGS",
    "CROSS_SYSTEM_COORDINATION_BOUNDARY_MODE",
    "CROSS_SYSTEM_COORDINATION_BOUNDARY_STAGE",
    "CROSS_SYSTEM_COORDINATION_MODE",
    "CROSS_SYSTEM_COORDINATION_STATUS",
    "FUTURE_CONTROLLED_ADAPTER_SANDBOX_STATUS",
    "GITHUB_COORDINATION_STATUS",
    "GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_HASH_ALGORITHM",
    "GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_SCHEMA_VERSION",
    "GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_TYPE",
    "GOVERNANCE_CROSS_SYSTEM_COORDINATION_BOUNDARY_VERSION",
    "HERMES_COORDINATION_STATUS",
    "OPENCLAW_COORDINATION_STATUS",
    "REQUIRED_COORDINATION_BLOCKING_CONDITION_NAMES",
    "REQUIRED_COORDINATION_EVIDENCE_REQUIREMENT_NAMES",
    "REQUIRED_COORDINATION_READINESS_CONDITION_NAMES",
    "REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CHECK_NAMES",
    "REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_CONTRACT_NAMES",
    "REQUIRED_CROSS_SYSTEM_COORDINATION_BOUNDARY_SECTION_NAMES",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "SYSTEM_HANDOFF_STATUS",
    "TOOL_ROUTING_STATUS",
    "build_governance_cross_system_coordination_boundary",
    "get_governance_cross_system_coordination_boundary_check",
    "get_governance_cross_system_coordination_boundary_contract",
    "get_governance_cross_system_coordination_boundary_section",
    "governance_cross_system_coordination_boundary_to_json",
    "list_governance_cross_system_coordination_boundary_check_names",
    "list_governance_cross_system_coordination_boundary_contract_names",
    "list_governance_cross_system_coordination_boundary_section_names",
]
