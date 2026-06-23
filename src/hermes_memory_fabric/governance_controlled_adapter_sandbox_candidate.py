"""Deterministic controlled adapter sandbox candidate metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_cross_system_coordination_boundary import (
    build_governance_cross_system_coordination_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION = "6.9.0"
GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SCHEMA_VERSION = "6.9.0"
GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_TYPE = (
    "governance_controlled_adapter_sandbox_candidate"
)
GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_ALGORITHM = "sha256"
CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE = (
    "v5.11_controlled_adapter_sandbox_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE = (
    "controlled_adapter_sandbox_candidate_only"
)
CONTROLLED_ADAPTER_SANDBOX_MODE = "metadata_only"
CONTROLLED_ADAPTER_SANDBOX_STATUS = "not_started"
ADAPTER_SANDBOX_ENTRY_STATUS = "not_entered"
SANDBOX_EXECUTION_STATUS = "not_enabled"
SANDBOX_RUNTIME_STATUS = "not_started"
SANDBOX_SCOPE_STATUS = "candidate_scope_only"
SANDBOX_POLICY_STATUS = "metadata_only"
FUTURE_POST_SANDBOX_REVIEW_STATUS = "not_entered"

READY_HANDOFF_STATUS = "ready_for_post_sandbox_review_boundary_design"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "controlled_adapter_sandbox_started": False,
    "adapter_sandbox_entered": False,
    "sandbox_runtime_created": False,
    "sandbox_execution_enabled": False,
    "sandbox_network_enabled": False,
    "sandbox_external_calls_enabled": False,
    "sandbox_filesystem_writes_enabled": False,
    "sandbox_database_writes_enabled": False,
    "sandbox_memory_graph_mutation_enabled": False,
    "sandbox_operation_ledger_writes_enabled": False,
    "sandbox_tool_routing_enabled": False,
    "sandbox_command_routing_enabled": False,
    "sandbox_adapter_invocation_enabled": False,
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
}

REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES = (
    "cross_system_coordination_boundary_pass",
    "cross_system_coordination_boundary_hash_present",
    "cross_system_coordination_boundary_hash_stable",
    "cross_system_coordination_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "controlled_adapter_sandbox_not_started",
    "adapter_sandbox_not_entered",
    "sandbox_runtime_not_created",
    "sandbox_execution_not_enabled",
    "sandbox_network_not_enabled",
    "sandbox_external_calls_not_enabled",
    "sandbox_filesystem_writes_not_enabled",
    "sandbox_database_writes_not_enabled",
    "sandbox_memory_graph_mutation_not_enabled",
    "sandbox_operation_ledger_writes_not_enabled",
    "sandbox_tool_routing_not_enabled",
    "sandbox_command_routing_not_enabled",
    "sandbox_adapter_invocation_not_enabled",
    "sandbox_candidate_metadata_only",
    "candidate_scope_only_declared",
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
    "no_star_cosmos_active_entry",
)

REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES = (
    "cross_system_coordination_boundary_pass_evidence",
    "deterministic_cross_system_coordination_boundary_hash_evidence",
    "cross_system_coordination_metadata_evidence",
    "sandbox_candidate_metadata_evidence",
    "sandbox_candidate_scope_evidence",
    "controlled_adapter_sandbox_not_started_evidence",
    "adapter_sandbox_not_entered_evidence",
    "sandbox_runtime_not_created_evidence",
    "sandbox_execution_not_enabled_evidence",
    "sandbox_network_not_enabled_evidence",
    "sandbox_external_calls_not_enabled_evidence",
    "sandbox_filesystem_writes_not_enabled_evidence",
    "sandbox_database_writes_not_enabled_evidence",
    "sandbox_memory_graph_mutation_not_enabled_evidence",
    "sandbox_operation_ledger_writes_not_enabled_evidence",
    "sandbox_tool_routing_not_enabled_evidence",
    "sandbox_command_routing_not_enabled_evidence",
    "sandbox_adapter_invocation_not_enabled_evidence",
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
    "no_star_cosmos_active_entry_evidence",
)

REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES = (
    "cross_system_coordination_boundary_blocked",
    "missing_cross_system_coordination_boundary_hash",
    "unstable_cross_system_coordination_boundary_hash",
    "sandbox_candidate_metadata_invalid",
    "candidate_only_boundary_missing",
    "cross_system_coordination_started",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "tool_routing_configured",
    "command_routing_configured",
    "system_handoff_completed",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_network_enabled",
    "sandbox_external_calls_enabled",
    "sandbox_filesystem_writes_enabled",
    "sandbox_database_writes_enabled",
    "sandbox_memory_graph_mutation_enabled",
    "sandbox_operation_ledger_writes_enabled",
    "sandbox_tool_routing_enabled",
    "sandbox_command_routing_enabled",
    "sandbox_adapter_invocation_enabled",
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
    "star_cosmos_active_entry_claimed",
)

REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES = (
    "cross_system_coordination_boundary_input_section",
    "sandbox_candidate_metadata_section",
    "candidate_scope_section",
    "sandbox_policy_metadata_section",
    "sandbox_entry_disabled_section",
    "sandbox_runtime_disabled_section",
    "sandbox_execution_disabled_section",
    "sandbox_network_disabled_section",
    "sandbox_external_call_disabled_section",
    "sandbox_write_disabled_section",
    "sandbox_tool_command_routing_disabled_section",
    "sandbox_adapter_invocation_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_cosmos_candidate_only_section",
    "future_post_sandbox_review_readiness_section",
)

REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES = (
    "controlled_adapter_sandbox_candidate_only_contract",
    "sandbox_candidate_metadata_only_contract",
    "cross_system_coordination_boundary_pass_contract",
    "cross_system_coordination_boundary_hash_present_contract",
    "cross_system_coordination_boundary_hash_stable_contract",
    "sandbox_candidate_readiness_conditions_declared_contract",
    "sandbox_candidate_evidence_requirements_declared_contract",
    "sandbox_candidate_blocking_conditions_declared_contract",
    "sandbox_candidate_sections_complete_contract",
    "sandbox_candidate_sections_pass_contract",
    "candidate_only_boundary_contract",
    "controlled_adapter_sandbox_not_started_contract",
    "adapter_sandbox_not_entered_contract",
    "sandbox_runtime_not_created_contract",
    "sandbox_execution_not_enabled_contract",
    "sandbox_network_not_enabled_contract",
    "sandbox_external_calls_not_enabled_contract",
    "sandbox_filesystem_writes_not_enabled_contract",
    "sandbox_database_writes_not_enabled_contract",
    "sandbox_memory_graph_mutation_not_enabled_contract",
    "sandbox_operation_ledger_writes_not_enabled_contract",
    "sandbox_tool_routing_not_enabled_contract",
    "sandbox_command_routing_not_enabled_contract",
    "sandbox_adapter_invocation_not_enabled_contract",
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
    "star_cosmos_candidate_only_contract",
)

REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES = (
    "controlled_adapter_sandbox_candidate_stage_check",
    "controlled_adapter_sandbox_candidate_only_mode_check",
    "sandbox_candidate_metadata_only_check",
    "controlled_adapter_sandbox_not_started_check",
    "adapter_sandbox_not_entered_check",
    "sandbox_runtime_not_created_check",
    "sandbox_execution_not_enabled_check",
    "sandbox_network_not_enabled_check",
    "sandbox_external_calls_not_enabled_check",
    "sandbox_filesystem_writes_not_enabled_check",
    "sandbox_database_writes_not_enabled_check",
    "sandbox_memory_graph_mutation_not_enabled_check",
    "sandbox_operation_ledger_writes_not_enabled_check",
    "sandbox_tool_routing_not_enabled_check",
    "sandbox_command_routing_not_enabled_check",
    "sandbox_adapter_invocation_not_enabled_check",
    "cross_system_coordination_boundary_pass_check",
    "cross_system_coordination_boundary_hash_present_check",
    "cross_system_coordination_boundary_hash_stable_check",
    "sandbox_candidate_readiness_conditions_declared_check",
    "sandbox_candidate_evidence_requirements_declared_check",
    "sandbox_candidate_blocking_conditions_declared_check",
    "sandbox_candidate_sections_complete_check",
    "sandbox_candidate_sections_pass_check",
    "sandbox_candidate_contracts_pass_check",
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
    "star_cosmos_candidate_only_check",
    "deterministic_controlled_adapter_sandbox_candidate_hash_check",
    "sandbox_candidate_readiness_check",
)

_CROSS_SYSTEM_COORDINATION_REFS = (
    "cross_system_coordination_boundary_status",
    "deterministic_cross_system_coordination_boundary_hash",
    "cross_system_coordination_metadata",
)

_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_FIELDS = (
    "version",
    "schema_version",
    "controlled_adapter_sandbox_candidate_type",
    "controlled_adapter_sandbox_candidate_status",
    "controlled_adapter_sandbox_candidate_stage",
    "controlled_adapter_sandbox_candidate_mode",
    "controlled_adapter_sandbox_mode",
    "controlled_adapter_sandbox_status",
    "adapter_sandbox_entry_status",
    "sandbox_execution_status",
    "sandbox_runtime_status",
    "sandbox_scope_status",
    "sandbox_policy_status",
    "future_post_sandbox_review_status",
    "star_cosmos_entry_status",
    "sandbox_candidate_declared",
    *COMMON_DISABLED_FLAGS,
    "cross_system_coordination_boundary_version",
    "cross_system_coordination_boundary_status",
    "cross_system_coordination_boundary_hash",
    "controlled_adapter_sandbox_candidate_metadata",
    "controlled_adapter_sandbox_candidate_sections",
    "controlled_adapter_sandbox_candidate_contracts",
    "controlled_adapter_sandbox_candidate_checks",
    "controlled_adapter_sandbox_candidate_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_FIELDS),
    "input_shape": "sanitized controlled adapter sandbox candidate projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_cross_system_coordination_boundary_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_DISABLED_CONTRACT_SPECS = (
    ("controlled_adapter_sandbox_not_started_contract", "controlled_adapter_sandbox_started"),
    ("adapter_sandbox_not_entered_contract", "adapter_sandbox_entered"),
    ("sandbox_runtime_not_created_contract", "sandbox_runtime_created"),
    ("sandbox_execution_not_enabled_contract", "sandbox_execution_enabled"),
    ("sandbox_network_not_enabled_contract", "sandbox_network_enabled"),
    ("sandbox_external_calls_not_enabled_contract", "sandbox_external_calls_enabled"),
    (
        "sandbox_filesystem_writes_not_enabled_contract",
        "sandbox_filesystem_writes_enabled",
    ),
    ("sandbox_database_writes_not_enabled_contract", "sandbox_database_writes_enabled"),
    (
        "sandbox_memory_graph_mutation_not_enabled_contract",
        "sandbox_memory_graph_mutation_enabled",
    ),
    (
        "sandbox_operation_ledger_writes_not_enabled_contract",
        "sandbox_operation_ledger_writes_enabled",
    ),
    ("sandbox_tool_routing_not_enabled_contract", "sandbox_tool_routing_enabled"),
    (
        "sandbox_command_routing_not_enabled_contract",
        "sandbox_command_routing_enabled",
    ),
    (
        "sandbox_adapter_invocation_not_enabled_contract",
        "sandbox_adapter_invocation_enabled",
    ),
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
)

_DISABLED_CHECK_SPECS = tuple(
    (contract_name.removesuffix("_contract") + "_check", field_name)
    for contract_name, field_name in _DISABLED_CONTRACT_SPECS
)


def build_governance_controlled_adapter_sandbox_candidate() -> dict[str, Any]:
    """Build deterministic controlled-adapter-sandbox-candidate-only metadata."""

    boundary, repeated_boundary = _cross_system_coordination_boundary_pair()
    metadata = _build_candidate_metadata(boundary, repeated_boundary)
    sections = _build_candidate_sections(boundary, repeated_boundary, metadata)
    contracts = _build_candidate_contracts(
        boundary,
        repeated_boundary,
        metadata,
        sections,
    )
    checks = _build_candidate_checks(
        boundary,
        repeated_boundary,
        metadata,
        sections,
        contracts,
    )

    boundary_passes = _cross_system_boundary_passes(boundary)
    metadata_valid = _candidate_metadata_valid(metadata)
    sections_pass = _sections_pass(sections)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    candidate_status = (
        "pass"
        if boundary_passes
        and metadata_valid
        and sections_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["cross-system coordination boundary must pass at version 6.9.0"]
                if not boundary_passes
                else []
            ),
            *(
                ["controlled adapter sandbox candidate metadata must remain metadata-only"]
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
    boundary_hash = _cross_system_boundary_hash(boundary)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION,
        "schema_version": (
            GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SCHEMA_VERSION
        ),
        "controlled_adapter_sandbox_candidate_type": (
            GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_TYPE
        ),
        "controlled_adapter_sandbox_candidate_status": candidate_status,
        "controlled_adapter_sandbox_candidate_stage": (
            CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE
        ),
        "controlled_adapter_sandbox_candidate_mode": (
            CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
        ),
        "controlled_adapter_sandbox_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
        "controlled_adapter_sandbox_status": CONTROLLED_ADAPTER_SANDBOX_STATUS,
        "adapter_sandbox_entry_status": ADAPTER_SANDBOX_ENTRY_STATUS,
        "sandbox_execution_status": SANDBOX_EXECUTION_STATUS,
        "sandbox_runtime_status": SANDBOX_RUNTIME_STATUS,
        "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
        "sandbox_policy_status": SANDBOX_POLICY_STATUS,
        "future_post_sandbox_review_status": FUTURE_POST_SANDBOX_REVIEW_STATUS,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "sandbox_candidate_declared": True,
        **COMMON_DISABLED_FLAGS,
        "cross_system_coordination_boundary_version": _string_or_none(
            boundary.get("version")
        ),
        "cross_system_coordination_boundary_status": _string_or_none(
            boundary.get("cross_system_coordination_boundary_status")
        ),
        "cross_system_coordination_boundary_hash": boundary_hash,
        "controlled_adapter_sandbox_candidate_metadata": metadata,
        "controlled_adapter_sandbox_candidate_sections": sections,
        "controlled_adapter_sandbox_candidate_contracts": contracts,
        "controlled_adapter_sandbox_candidate_checks": checks,
        "controlled_adapter_sandbox_candidate_summary": _candidate_summary(
            candidate_status,
            boundary,
            repeated_boundary,
            metadata,
            sections,
            contracts,
            checks,
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if candidate_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_controlled_adapter_sandbox_candidate_hash"] = (
        _controlled_adapter_sandbox_candidate_hash(result)
    )
    return _detached_json_value(result)


def get_governance_controlled_adapter_sandbox_candidate_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached candidate section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_candidate()[
        "controlled_adapter_sandbox_candidate_sections"
    ]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_controlled_adapter_sandbox_candidate_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached candidate contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_candidate()[
        "controlled_adapter_sandbox_candidate_contracts"
    ]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_controlled_adapter_sandbox_candidate_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached candidate check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_candidate()["controlled_adapter_sandbox_candidate_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_controlled_adapter_sandbox_candidate_section_names() -> list[str]:
    """Return stable candidate section names."""

    return list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES)


def list_governance_controlled_adapter_sandbox_candidate_contract_names() -> list[str]:
    """Return stable candidate contract names."""

    return list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES)


def list_governance_controlled_adapter_sandbox_candidate_check_names() -> list[str]:
    """Return stable candidate check names."""

    return list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES)


def governance_controlled_adapter_sandbox_candidate_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize candidate metadata deterministically."""

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
def _cached_candidate_payload() -> str:
    return governance_controlled_adapter_sandbox_candidate_to_json(
        build_governance_controlled_adapter_sandbox_candidate()
    )


def _cached_candidate() -> dict[str, Any]:
    return json.loads(_cached_candidate_payload())


@lru_cache(maxsize=1)
def _cached_boundary_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_cross_system_coordination_boundary()
    )
    second = _detached_json_value(
        build_governance_cross_system_coordination_boundary()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _cross_system_coordination_boundary_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_boundary_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_candidate_metadata(
    boundary: Mapping[str, Any],
    repeated_boundary: Mapping[str, Any],
) -> dict[str, Any]:
    boundary_hash = _cross_system_boundary_hash(boundary)
    repeated_hash = _cross_system_boundary_hash(repeated_boundary)
    hash_present = _is_sha256(boundary_hash)
    hash_stable = hash_present and boundary_hash == repeated_hash
    candidate_ready = (
        _cross_system_boundary_passes(boundary)
        and hash_stable
        and _cross_system_metadata_evidence_valid(boundary)
        and _all_upstream_boundaries_disabled(boundary)
        and _all_safety_boundaries_false(boundary)
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "sandbox_candidate_metadata_type": (
                "future_controlled_adapter_sandbox_candidate_metadata"
            ),
            "sandbox_candidate_metadata_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
            "sandbox_candidate_status": "metadata_only_candidate",
            "controlled_adapter_sandbox_status": CONTROLLED_ADAPTER_SANDBOX_STATUS,
            "adapter_sandbox_entry_status": ADAPTER_SANDBOX_ENTRY_STATUS,
            "sandbox_execution_status": SANDBOX_EXECUTION_STATUS,
            "sandbox_runtime_status": SANDBOX_RUNTIME_STATUS,
            "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
            "sandbox_policy_status": SANDBOX_POLICY_STATUS,
            "future_post_sandbox_review_status": FUTURE_POST_SANDBOX_REVIEW_STATUS,
            "sandbox_candidate_required": True,
            "sandbox_candidate_metadata_available": True,
            "sandbox_candidate_declared": True,
            "candidate_only": True,
            "cross_system_coordination_boundary_pass_required": True,
            "cross_system_coordination_boundary_hash_required": True,
            "cross_system_coordination_boundary_status": _string_or_none(
                boundary.get("cross_system_coordination_boundary_status")
            ),
            "cross_system_coordination_boundary_hash_present": hash_present,
            "cross_system_coordination_boundary_hash_stable": hash_stable,
            "cross_system_coordination_metadata_available": (
                _cross_system_metadata_evidence_valid(boundary)
            ),
            "sandbox_candidate_readiness_conditions": list(
                REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES
            ),
            "required_sandbox_candidate_evidence": list(
                REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES
            ),
            "sandbox_candidate_blocking_conditions": list(
                REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES
            ),
            "sandbox_candidate_next_stage": "post_sandbox_review_boundary",
            "sandbox_candidate_handoff_status": (
                READY_HANDOFF_STATUS if candidate_ready else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_candidate_sections(
    boundary: Mapping[str, Any],
    repeated_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    boundary_hash = _cross_system_boundary_hash(boundary)
    repeated_hash = _cross_system_boundary_hash(repeated_boundary)
    section_specs = (
        (
            "cross_system_coordination_boundary_input_section",
            "cross_system_coordination_boundary_input",
            {
                "cross_system_coordination_boundary_version": (
                    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION
                ),
                "cross_system_coordination_boundary_status": "pass",
                "cross_system_coordination_boundary_hash_present": True,
                "cross_system_coordination_boundary_hash_stable": True,
                "cross_system_coordination_metadata_available": True,
            },
            {
                "cross_system_coordination_boundary_version": _string_or_none(
                    boundary.get("version")
                ),
                "cross_system_coordination_boundary_status": _string_or_none(
                    boundary.get("cross_system_coordination_boundary_status")
                ),
                "cross_system_coordination_boundary_hash_present": _is_sha256(
                    boundary_hash
                ),
                "cross_system_coordination_boundary_hash_stable": (
                    _is_sha256(boundary_hash) and boundary_hash == repeated_hash
                ),
                "cross_system_coordination_metadata_available": (
                    _cross_system_metadata_evidence_valid(boundary)
                ),
            },
            ("Consumes detached deterministic coordination-boundary metadata.",),
        ),
        (
            "sandbox_candidate_metadata_section",
            "sandbox_candidate_metadata_boundary",
            {
                "sandbox_candidate_metadata_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
                "sandbox_candidate_status": "metadata_only_candidate",
                "sandbox_candidate_metadata_available": True,
                "sandbox_candidate_declared": True,
            },
            _select(
                metadata,
                (
                    "sandbox_candidate_metadata_mode",
                    "sandbox_candidate_status",
                    "sandbox_candidate_metadata_available",
                    "sandbox_candidate_declared",
                ),
            ),
            ("Defines candidate metadata without enabling a sandbox.",),
        ),
        (
            "candidate_scope_section",
            "sandbox_candidate_scope_boundary",
            {
                "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
                "candidate_only": True,
            },
            _select(metadata, ("sandbox_scope_status", "candidate_only")),
            ("Limits the result to candidate scope.",),
        ),
        (
            "sandbox_policy_metadata_section",
            "sandbox_policy_metadata_boundary",
            {
                "sandbox_policy_status": SANDBOX_POLICY_STATUS,
                "sandbox_candidate_metadata_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
            },
            _select(
                metadata,
                ("sandbox_policy_status", "sandbox_candidate_metadata_mode"),
            ),
            ("Declares policy metadata only.",),
        ),
        (
            "sandbox_entry_disabled_section",
            "sandbox_entry_disabled_boundary",
            {
                "controlled_adapter_sandbox_status": CONTROLLED_ADAPTER_SANDBOX_STATUS,
                "adapter_sandbox_entry_status": ADAPTER_SANDBOX_ENTRY_STATUS,
                "controlled_adapter_sandbox_started": False,
                "adapter_sandbox_entered": False,
            },
            _select(
                metadata,
                (
                    "controlled_adapter_sandbox_status",
                    "adapter_sandbox_entry_status",
                    "controlled_adapter_sandbox_started",
                    "adapter_sandbox_entered",
                ),
            ),
            ("Keeps sandbox start and entry absent.",),
        ),
        (
            "sandbox_runtime_disabled_section",
            "sandbox_runtime_disabled_boundary",
            {
                "sandbox_runtime_status": SANDBOX_RUNTIME_STATUS,
                "sandbox_runtime_created": False,
            },
            _select(metadata, ("sandbox_runtime_status", "sandbox_runtime_created")),
            ("Keeps sandbox runtime creation absent.",),
        ),
        (
            "sandbox_execution_disabled_section",
            "sandbox_execution_disabled_boundary",
            {
                "sandbox_execution_status": SANDBOX_EXECUTION_STATUS,
                "sandbox_execution_enabled": False,
                "real_execution_enabled": False,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
            _select(
                metadata,
                (
                    "sandbox_execution_status",
                    "sandbox_execution_enabled",
                    "real_execution_enabled",
                    "manifest_executed",
                    "dry_run_plan_executed",
                ),
            ),
            ("Keeps execution surfaces disabled.",),
        ),
        (
            "sandbox_network_disabled_section",
            "sandbox_network_disabled_boundary",
            {"sandbox_network_enabled": False, "network_calls_enabled": False},
            _select(
                metadata,
                ("sandbox_network_enabled", "network_calls_enabled"),
            ),
            ("Keeps network capability disabled.",),
        ),
        (
            "sandbox_external_call_disabled_section",
            "sandbox_external_call_disabled_boundary",
            {
                "sandbox_external_calls_enabled": False,
                "external_calls_enabled": False,
            },
            _select(
                metadata,
                ("sandbox_external_calls_enabled", "external_calls_enabled"),
            ),
            ("Keeps external calls disabled.",),
        ),
        (
            "sandbox_write_disabled_section",
            "sandbox_write_disabled_boundary",
            {
                "sandbox_filesystem_writes_enabled": False,
                "sandbox_database_writes_enabled": False,
                "sandbox_memory_graph_mutation_enabled": False,
                "durable_writes_enabled": False,
                "filesystem_writes_enabled": False,
                "database_writes_enabled": False,
                "memory_graph_mutation_enabled": False,
            },
            _select(
                metadata,
                (
                    "sandbox_filesystem_writes_enabled",
                    "sandbox_database_writes_enabled",
                    "sandbox_memory_graph_mutation_enabled",
                    "durable_writes_enabled",
                    "filesystem_writes_enabled",
                    "database_writes_enabled",
                    "memory_graph_mutation_enabled",
                ),
            ),
            ("Keeps durable, filesystem, database, and graph writes disabled.",),
        ),
        (
            "sandbox_tool_command_routing_disabled_section",
            "sandbox_tool_command_routing_disabled_boundary",
            {
                "sandbox_tool_routing_enabled": False,
                "sandbox_command_routing_enabled": False,
                "tool_routing_enabled": False,
                "command_routing_enabled": False,
                "cross_system_coordination_enabled": False,
                "system_handoff_completed": False,
            },
            _select(
                metadata,
                (
                    "sandbox_tool_routing_enabled",
                    "sandbox_command_routing_enabled",
                    "tool_routing_enabled",
                    "command_routing_enabled",
                    "cross_system_coordination_enabled",
                    "system_handoff_completed",
                ),
            ),
            ("Keeps coordination and routing disabled.",),
        ),
        (
            "sandbox_adapter_invocation_disabled_section",
            "sandbox_adapter_invocation_disabled_boundary",
            {
                "sandbox_adapter_invocation_enabled": False,
                "execution_adapter_implemented": False,
                "execution_adapter_invoked": False,
                "adapter_dispatched": False,
                "manifest_dispatched": False,
            },
            _select(
                metadata,
                (
                    "sandbox_adapter_invocation_enabled",
                    "execution_adapter_implemented",
                    "execution_adapter_invoked",
                    "adapter_dispatched",
                    "manifest_dispatched",
                ),
            ),
            ("Keeps adapter and manifest invocation surfaces disabled.",),
        ),
        (
            "operation_ledger_write_disabled_section",
            "operation_ledger_write_disabled_boundary",
            {
                "sandbox_operation_ledger_writes_enabled": False,
                "operation_ledger_writes_enabled": False,
                "operation_ledger_entry_created": False,
                "operation_ledger_entry_written": False,
                "operation_ledger_proposal_persisted": False,
                "operation_ledger_proposal_submitted": False,
                "operation_ledger_proposal_dispatched": False,
            },
            _select(
                metadata,
                (
                    "sandbox_operation_ledger_writes_enabled",
                    "operation_ledger_writes_enabled",
                    "operation_ledger_entry_created",
                    "operation_ledger_entry_written",
                    "operation_ledger_proposal_persisted",
                    "operation_ledger_proposal_submitted",
                    "operation_ledger_proposal_dispatched",
                ),
            ),
            ("Keeps operation-ledger writes and proposal transitions absent.",),
        ),
        (
            "approval_authorization_disabled_section",
            "approval_authorization_disabled_boundary",
            {
                "approval_request_created": False,
                "approval_notification_sent": False,
                "real_approval_record_written": False,
                "execution_authorization_issued": False,
                "authorization_token_created": False,
                "authorization_grant_created": False,
            },
            _select(
                metadata,
                (
                    "approval_request_created",
                    "approval_notification_sent",
                    "real_approval_record_written",
                    "execution_authorization_issued",
                    "authorization_token_created",
                    "authorization_grant_created",
                ),
            ),
            ("Keeps approval and authorization effects absent.",),
        ),
        (
            "star_cosmos_candidate_only_section",
            "star_cosmos_candidate_only_boundary",
            {
                "candidate_only": True,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            _select(
                metadata,
                (
                    "candidate_only",
                    "star_cosmos_entry_status",
                    "star_cosmos_memory_active",
                ),
            ),
            ("Does not claim active Star-Cosmos entry.",),
        ),
        (
            "future_post_sandbox_review_readiness_section",
            "future_post_sandbox_review_readiness_boundary",
            {
                "future_post_sandbox_review_status": (
                    FUTURE_POST_SANDBOX_REVIEW_STATUS
                ),
                "sandbox_candidate_next_stage": "post_sandbox_review_boundary",
                "sandbox_candidate_handoff_status": READY_HANDOFF_STATUS,
                "sandbox_candidate_readiness_conditions": list(
                    REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES
                ),
            },
            _select(
                metadata,
                (
                    "future_post_sandbox_review_status",
                    "sandbox_candidate_next_stage",
                    "sandbox_candidate_handoff_status",
                    "sandbox_candidate_readiness_conditions",
                ),
            ),
            ("Marks readiness for future review-boundary design only.",),
        ),
    )
    return [
        _section_from_expected(
            name,
            section_type=section_type,
            expected=expected,
            observed=observed,
            sandbox_candidate_notes=notes,
        )
        for name, section_type, expected, observed, notes in section_specs
    ]


def _build_candidate_contracts(
    boundary: Mapping[str, Any],
    repeated_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    boundary_hash = _cross_system_boundary_hash(boundary)
    repeated_hash = _cross_system_boundary_hash(repeated_boundary)
    contracts = [
        _contract_from_expected(
            "controlled_adapter_sandbox_candidate_only_contract",
            contract_type="sandbox_candidate_mode_contract",
            expected={
                "controlled_adapter_sandbox_candidate_mode": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
                )
            },
            observed={
                "controlled_adapter_sandbox_candidate_mode": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
                )
            },
        ),
        _contract_from_expected(
            "sandbox_candidate_metadata_only_contract",
            contract_type="sandbox_candidate_metadata_contract",
            expected={
                "sandbox_candidate_metadata_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
                "sandbox_candidate_status": "metadata_only_candidate",
            },
            observed=_select(
                metadata,
                ("sandbox_candidate_metadata_mode", "sandbox_candidate_status"),
            ),
        ),
        _contract_from_expected(
            "cross_system_coordination_boundary_pass_contract",
            contract_type="coordination_boundary_status_contract",
            expected={
                "cross_system_coordination_boundary_version": (
                    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION
                ),
                "cross_system_coordination_boundary_status": "pass",
            },
            observed={
                "cross_system_coordination_boundary_version": _string_or_none(
                    boundary.get("version")
                ),
                "cross_system_coordination_boundary_status": _string_or_none(
                    boundary.get("cross_system_coordination_boundary_status")
                ),
            },
        ),
        _contract_from_expected(
            "cross_system_coordination_boundary_hash_present_contract",
            contract_type="coordination_boundary_hash_contract",
            expected={"cross_system_coordination_boundary_hash_present": True},
            observed={
                "cross_system_coordination_boundary_hash_present": _is_sha256(
                    boundary_hash
                )
            },
        ),
        _contract_from_expected(
            "cross_system_coordination_boundary_hash_stable_contract",
            contract_type="coordination_boundary_hash_contract",
            expected={"cross_system_coordination_boundary_hash_stable": True},
            observed={
                "cross_system_coordination_boundary_hash_stable": (
                    _is_sha256(boundary_hash) and boundary_hash == repeated_hash
                )
            },
        ),
        *_requirements_contracts(metadata),
        _contract_from_expected(
            "sandbox_candidate_sections_complete_contract",
            contract_type="sandbox_candidate_sections_contract",
            expected={
                "sandbox_candidate_section_names": list(
                    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES
                )
            },
            observed={"sandbox_candidate_section_names": _section_names(sections)},
        ),
        _contract_from_expected(
            "sandbox_candidate_sections_pass_contract",
            contract_type="sandbox_candidate_sections_contract",
            expected={"sandbox_candidate_sections_pass": True},
            observed={"sandbox_candidate_sections_pass": _sections_pass(sections)},
        ),
        _contract_from_expected(
            "candidate_only_boundary_contract",
            contract_type="candidate_only_boundary_contract",
            expected={
                "candidate_only": True,
                "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "candidate_only",
                    "sandbox_scope_status",
                    "star_cosmos_entry_status",
                ),
            ),
        ),
        *[
            _contract_from_expected(
                contract_name,
                contract_type="disabled_sandbox_candidate_boundary_contract",
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for contract_name, field_name in _DISABLED_CONTRACT_SPECS
        ],
        _contract_from_expected(
            "star_cosmos_candidate_only_contract",
            contract_type="star_cosmos_candidate_only_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed=_select(
                metadata,
                ("star_cosmos_entry_status", "star_cosmos_memory_active"),
            ),
        ),
    ]
    return _detached_json_value(contracts)


def _requirements_contracts(
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs = (
        (
            "sandbox_candidate_readiness_conditions_declared_contract",
            "sandbox_candidate_readiness_conditions",
            list(REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES),
        ),
        (
            "sandbox_candidate_evidence_requirements_declared_contract",
            "required_sandbox_candidate_evidence",
            list(REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "sandbox_candidate_blocking_conditions_declared_contract",
            "sandbox_candidate_blocking_conditions",
            list(REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES),
        ),
    )
    return [
        _contract_from_expected(
            contract_name,
            contract_type="sandbox_candidate_requirements_contract",
            expected={field_name: expected_value},
            observed={field_name: metadata.get(field_name)},
        )
        for contract_name, field_name, expected_value in specs
    ]


def _build_candidate_checks(
    boundary: Mapping[str, Any],
    repeated_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    boundary_hash = _cross_system_boundary_hash(boundary)
    repeated_hash = _cross_system_boundary_hash(repeated_boundary)
    checks = [
        _check_from_expected(
            "controlled_adapter_sandbox_candidate_stage_check",
            expected={
                "controlled_adapter_sandbox_candidate_stage": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE
                )
            },
            observed={
                "controlled_adapter_sandbox_candidate_stage": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_STAGE
                )
            },
        ),
        _check_from_expected(
            "controlled_adapter_sandbox_candidate_only_mode_check",
            expected={
                "controlled_adapter_sandbox_candidate_mode": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
                )
            },
            observed={
                "controlled_adapter_sandbox_candidate_mode": (
                    CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_MODE
                )
            },
        ),
        _check_from_expected(
            "sandbox_candidate_metadata_only_check",
            expected={
                "sandbox_candidate_metadata_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
                "sandbox_policy_status": SANDBOX_POLICY_STATUS,
            },
            observed=_select(
                metadata,
                ("sandbox_candidate_metadata_mode", "sandbox_policy_status"),
            ),
        ),
        *[
            _check_from_expected(
                check_name,
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for check_name, field_name in _DISABLED_CHECK_SPECS[:13]
        ],
        _check_from_expected(
            "cross_system_coordination_boundary_pass_check",
            expected={"cross_system_coordination_boundary_status": "pass"},
            observed={
                "cross_system_coordination_boundary_status": _string_or_none(
                    boundary.get("cross_system_coordination_boundary_status")
                )
            },
        ),
        _check_from_expected(
            "cross_system_coordination_boundary_hash_present_check",
            expected={"cross_system_coordination_boundary_hash_present": True},
            observed={
                "cross_system_coordination_boundary_hash_present": _is_sha256(
                    boundary_hash
                )
            },
        ),
        _check_from_expected(
            "cross_system_coordination_boundary_hash_stable_check",
            expected={"cross_system_coordination_boundary_hash_stable": True},
            observed={
                "cross_system_coordination_boundary_hash_stable": (
                    _is_sha256(boundary_hash) and boundary_hash == repeated_hash
                )
            },
        ),
        *_requirements_checks(metadata),
        _check_from_expected(
            "sandbox_candidate_sections_complete_check",
            expected={
                "sandbox_candidate_section_names": list(
                    REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES
                )
            },
            observed={"sandbox_candidate_section_names": _section_names(sections)},
        ),
        _check_from_expected(
            "sandbox_candidate_sections_pass_check",
            expected={"sandbox_candidate_sections_pass": True},
            observed={"sandbox_candidate_sections_pass": _sections_pass(sections)},
        ),
        _check_from_expected(
            "sandbox_candidate_contracts_pass_check",
            expected={"sandbox_candidate_contracts_pass": True},
            observed={
                "sandbox_candidate_contracts_pass": _contracts_pass(contracts)
            },
        ),
        _check_from_expected(
            "candidate_only_boundary_check",
            expected={
                "candidate_only": True,
                "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "candidate_only",
                    "sandbox_scope_status",
                    "star_cosmos_entry_status",
                ),
            ),
        ),
        *[
            _check_from_expected(
                check_name,
                expected={field_name: False},
                observed={field_name: metadata.get(field_name)},
            )
            for check_name, field_name in _DISABLED_CHECK_SPECS[13:]
        ],
        _check_from_expected(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed=_select(
                metadata,
                ("star_cosmos_entry_status", "star_cosmos_memory_active"),
            ),
        ),
        _check_from_expected(
            "deterministic_controlled_adapter_sandbox_candidate_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_ALGORITHM
                ),
                "hash_projection_declared": True,
            },
            observed={
                "hash_algorithm": HASH_INPUT_CONTRACT["algorithm"],
                "hash_projection_declared": (
                    HASH_INPUT_CONTRACT["hash_fields"]
                    == list(_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_FIELDS)
                ),
            },
        ),
        _check_from_expected(
            "sandbox_candidate_readiness_check",
            expected={
                "sandbox_candidate_handoff_status": READY_HANDOFF_STATUS,
                "sandbox_candidate_sections_pass": True,
                "sandbox_candidate_contracts_pass": True,
            },
            observed={
                "sandbox_candidate_handoff_status": metadata.get(
                    "sandbox_candidate_handoff_status"
                ),
                "sandbox_candidate_sections_pass": _sections_pass(sections),
                "sandbox_candidate_contracts_pass": _contracts_pass(contracts),
            },
        ),
    ]
    return _detached_json_value(checks)


def _requirements_checks(
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs = (
        (
            "sandbox_candidate_readiness_conditions_declared_check",
            "sandbox_candidate_readiness_conditions",
            list(REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES),
        ),
        (
            "sandbox_candidate_evidence_requirements_declared_check",
            "required_sandbox_candidate_evidence",
            list(REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "sandbox_candidate_blocking_conditions_declared_check",
            "sandbox_candidate_blocking_conditions",
            list(REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES),
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


def _candidate_summary(
    candidate_status: str,
    boundary: Mapping[str, Any],
    repeated_boundary: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    boundary_hash = _cross_system_boundary_hash(boundary)
    repeated_hash = _cross_system_boundary_hash(repeated_boundary)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "controlled_adapter_sandbox_candidate_summary",
            "controlled_adapter_sandbox_candidate_status": candidate_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if candidate_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "controlled_adapter_sandbox_mode": CONTROLLED_ADAPTER_SANDBOX_MODE,
            "controlled_adapter_sandbox_status": CONTROLLED_ADAPTER_SANDBOX_STATUS,
            "adapter_sandbox_entry_status": ADAPTER_SANDBOX_ENTRY_STATUS,
            "sandbox_execution_status": SANDBOX_EXECUTION_STATUS,
            "sandbox_runtime_status": SANDBOX_RUNTIME_STATUS,
            "sandbox_scope_status": SANDBOX_SCOPE_STATUS,
            "sandbox_policy_status": SANDBOX_POLICY_STATUS,
            "future_post_sandbox_review_status": FUTURE_POST_SANDBOX_REVIEW_STATUS,
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "cross_system_coordination_boundary_version": _string_or_none(
                boundary.get("version")
            ),
            "cross_system_coordination_boundary_status": _string_or_none(
                boundary.get("cross_system_coordination_boundary_status")
            ),
            "cross_system_coordination_boundary_hash_present": _is_sha256(
                boundary_hash
            ),
            "cross_system_coordination_boundary_hash_stable": (
                _is_sha256(boundary_hash) and boundary_hash == repeated_hash
            ),
            "sandbox_candidate_metadata_valid": _candidate_metadata_valid(metadata),
            "sandbox_candidate_section_count": len(sections),
            "sandbox_candidate_sections_pass": _sections_pass(sections),
            "sandbox_candidate_contract_count": len(contracts),
            "sandbox_candidate_contracts_pass": _contracts_pass(contracts),
            "sandbox_candidate_check_count": len(checks),
            "sandbox_candidate_checks_pass": _checks_pass(checks),
            "sandbox_candidate_declared": True,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_expected(
    section_name: str,
    *,
    section_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    sandbox_candidate_notes: Sequence[str],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "controlled adapter sandbox candidate section values must match",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": section_name,
            "section_type": section_type,
            "section_status": "pass" if not blocking_reasons else "blocked",
            "source_cross_system_coordination_refs": list(
                _CROSS_SYSTEM_COORDINATION_REFS
            ),
            "expected": dict(expected),
            "observed": dict(observed),
            "sandbox_candidate_notes": list(sandbox_candidate_notes),
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
        "controlled adapter sandbox candidate contract values must match",
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
        "controlled adapter sandbox candidate check values must match",
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
            "section_type": "unknown_controlled_adapter_sandbox_candidate_section",
            "section_status": "blocked",
            "source_cross_system_coordination_refs": [],
            "expected": {"known_section_name": True},
            "observed": {
                "known_section_name": False,
                "requested_section_name": name,
            },
            "sandbox_candidate_notes": [],
            "blocking_reasons": [
                "controlled adapter sandbox candidate section name is not recognized"
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
                "unknown_controlled_adapter_sandbox_candidate_contract"
            ),
            "expected": {"known_contract_name": True},
            "observed": {
                "known_contract_name": False,
                "requested_contract_name": name,
            },
            "contract_status": "blocked",
            "blocking_reasons": [
                "controlled adapter sandbox candidate contract name is not recognized"
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
                "controlled adapter sandbox candidate check name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _controlled_adapter_sandbox_candidate_hash(
    result: Mapping[str, Any],
) -> str:
    projection = {
        field: result[field]
        for field in _CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_HASH_FIELDS
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


def _cross_system_boundary_hash(boundary: Mapping[str, Any]) -> str | None:
    return _string_or_none(
        boundary.get("deterministic_cross_system_coordination_boundary_hash")
    )


def _cross_system_boundary_passes(boundary: Mapping[str, Any]) -> bool:
    return (
        boundary.get("cross_system_coordination_boundary_status") == "pass"
        and boundary.get("version")
        == GOVERNANCE_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_VERSION
        and _is_sha256(_cross_system_boundary_hash(boundary))
    )


def _cross_system_metadata_evidence_valid(
    boundary: Mapping[str, Any],
) -> bool:
    metadata = boundary.get("cross_system_coordination_metadata")
    return (
        isinstance(metadata, Mapping)
        and metadata.get("coordination_metadata_mode") == "metadata_only"
        and metadata.get("coordination_metadata_available") is True
        and metadata.get("coordination_established") is False
        and metadata.get("coordination_persisted") is False
        and metadata.get("coordination_submitted") is False
        and metadata.get("coordination_dispatched") is False
    )


def _candidate_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("sandbox_candidate_metadata_type")
        == "future_controlled_adapter_sandbox_candidate_metadata"
        and metadata.get("sandbox_candidate_metadata_mode")
        == CONTROLLED_ADAPTER_SANDBOX_MODE
        and metadata.get("sandbox_candidate_status") == "metadata_only_candidate"
        and metadata.get("controlled_adapter_sandbox_status")
        == CONTROLLED_ADAPTER_SANDBOX_STATUS
        and metadata.get("adapter_sandbox_entry_status")
        == ADAPTER_SANDBOX_ENTRY_STATUS
        and metadata.get("sandbox_execution_status") == SANDBOX_EXECUTION_STATUS
        and metadata.get("sandbox_runtime_status") == SANDBOX_RUNTIME_STATUS
        and metadata.get("sandbox_scope_status") == SANDBOX_SCOPE_STATUS
        and metadata.get("sandbox_policy_status") == SANDBOX_POLICY_STATUS
        and metadata.get("future_post_sandbox_review_status")
        == FUTURE_POST_SANDBOX_REVIEW_STATUS
        and metadata.get("sandbox_candidate_required") is True
        and metadata.get("sandbox_candidate_metadata_available") is True
        and metadata.get("sandbox_candidate_declared") is True
        and metadata.get("candidate_only") is True
        and metadata.get("cross_system_coordination_boundary_pass_required")
        is True
        and metadata.get("cross_system_coordination_boundary_hash_required")
        is True
        and metadata.get("cross_system_coordination_boundary_status") == "pass"
        and metadata.get("cross_system_coordination_boundary_hash_present") is True
        and metadata.get("cross_system_coordination_boundary_hash_stable") is True
        and metadata.get("cross_system_coordination_metadata_available") is True
        and metadata.get("sandbox_candidate_readiness_conditions")
        == list(REQUIRED_SANDBOX_CANDIDATE_READINESS_CONDITION_NAMES)
        and metadata.get("required_sandbox_candidate_evidence")
        == list(REQUIRED_SANDBOX_CANDIDATE_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("sandbox_candidate_blocking_conditions")
        == list(REQUIRED_SANDBOX_CANDIDATE_BLOCKING_CONDITION_NAMES)
        and metadata.get("sandbox_candidate_next_stage")
        == "post_sandbox_review_boundary"
        and metadata.get("sandbox_candidate_handoff_status")
        == READY_HANDOFF_STATUS
        and metadata.get("star_cosmos_entry_status")
        == STAR_COSMOS_ENTRY_STATUS
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _sections_pass(sections: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [section.get("section_name") for section in sections]
        == list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_SECTION_NAMES)
        and all(section.get("section_status") == "pass" for section in sections)
    )


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [contract.get("contract_name") for contract in contracts]
        == list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CONTRACT_NAMES)
        and all(
            contract.get("contract_status") == "pass" for contract in contracts
        )
    )


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [check.get("check_name") for check in checks]
        == list(REQUIRED_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_CHECK_NAMES)
        and all(check.get("check_status") == "pass" for check in checks)
    )


def _section_names(sections: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        str(section.get("section_name"))
        for section in sections
        if section.get("section_name") is not None
    ]


def _select(value: Mapping[str, Any], names: Sequence[str]) -> dict[str, Any]:
    return {name: value.get(name) for name in names}


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


def _all_upstream_boundaries_disabled(value: Mapping[str, Any]) -> bool:
    return all(value.get(key) is False for key in COMMON_DISABLED_FLAGS if key in value)


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
    deduplicated: list[str] = []
    for value in values:
        if value not in deduplicated:
            deduplicated.append(value)
    return deduplicated


def _detached_json_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, str, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite floats are not allowed")
        return value
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, nested_value in value.items():
            if not isinstance(key, str):
                raise TypeError("all mapping keys must be strings")
            result[key] = _detached_json_value(nested_value)
        return result
    if isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        return [_detached_json_value(item) for item in value]
    raise TypeError(f"value is not JSON-compatible: {type(value).__name__}")
