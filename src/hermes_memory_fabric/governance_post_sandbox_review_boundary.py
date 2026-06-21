"""Deterministic future post-sandbox review boundary metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_controlled_adapter_sandbox_candidate import (
    build_governance_controlled_adapter_sandbox_candidate,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION = "6.4.0"
GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_SCHEMA_VERSION = "6.4.0"
GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_TYPE = (
    "governance_post_sandbox_review_boundary"
)
GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_HASH_ALGORITHM = "sha256"
POST_SANDBOX_REVIEW_BOUNDARY_STAGE = "v5.12_post_sandbox_review_boundary"
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
POST_SANDBOX_REVIEW_BOUNDARY_MODE = "post_sandbox_review_boundary_only"
POST_SANDBOX_REVIEW_MODE = "metadata_only"
POST_SANDBOX_REVIEW_STATUS = "not_started"
SANDBOX_RESULT_STATUS = "not_available"
SANDBOX_REVIEW_STATUS = "not_performed"
ROLLBACK_STATUS = "not_triggered"
QUARANTINE_STATUS = "not_triggered"
INCIDENT_STATUS = "not_triggered"
AUDIT_EVIDENCE_STATUS = "metadata_only"
FAILURE_HANDLING_STATUS = "metadata_only"
LAYER_14_CLOSURE_READINESS_STATUS = "candidate_only"

READY_HANDOFF_STATUS = "ready_for_star_cosmos_closure_handoff_audit_design"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "actual_post_sandbox_review_performed": False,
    "controlled_adapter_sandbox_started": False,
    "adapter_sandbox_entered": False,
    "sandbox_runtime_created": False,
    "sandbox_execution_enabled": False,
    "sandbox_result_available": False,
    "sandbox_failure_observed": False,
    "sandbox_success_observed": False,
    "rollback_triggered": False,
    "quarantine_triggered": False,
    "incident_triggered": False,
    "audit_log_written": False,
    "audit_evidence_persisted": False,
    "failure_handling_executed": False,
    "remediation_executed": False,
    "closure_audit_started": False,
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

REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES = (
    "controlled_adapter_sandbox_candidate_pass",
    "controlled_adapter_sandbox_candidate_hash_present",
    "controlled_adapter_sandbox_candidate_hash_stable",
    "controlled_adapter_sandbox_not_started",
    "adapter_sandbox_not_entered",
    "sandbox_runtime_not_created",
    "sandbox_execution_not_enabled",
    "sandbox_result_not_available",
    "actual_post_sandbox_review_not_performed",
    "rollback_not_triggered",
    "quarantine_not_triggered",
    "incident_not_triggered",
    "audit_log_not_written",
    "audit_evidence_not_persisted",
    "failure_handling_not_executed",
    "remediation_not_executed",
    "closure_audit_not_started",
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
    "post_sandbox_review_metadata_only",
    "layer_14_closure_candidate_only_declared",
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

REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES = (
    "controlled_adapter_sandbox_candidate_pass_evidence",
    "deterministic_controlled_adapter_sandbox_candidate_hash_evidence",
    "sandbox_candidate_metadata_evidence",
    "post_sandbox_review_metadata_evidence",
    "post_sandbox_review_scope_evidence",
    "controlled_adapter_sandbox_not_started_evidence",
    "adapter_sandbox_not_entered_evidence",
    "sandbox_runtime_not_created_evidence",
    "sandbox_execution_not_enabled_evidence",
    "sandbox_result_not_available_evidence",
    "actual_post_sandbox_review_not_performed_evidence",
    "rollback_not_triggered_evidence",
    "quarantine_not_triggered_evidence",
    "incident_not_triggered_evidence",
    "audit_log_not_written_evidence",
    "audit_evidence_not_persisted_evidence",
    "failure_handling_not_executed_evidence",
    "remediation_not_executed_evidence",
    "closure_audit_not_started_evidence",
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

REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES = (
    "controlled_adapter_sandbox_candidate_blocked",
    "missing_controlled_adapter_sandbox_candidate_hash",
    "unstable_controlled_adapter_sandbox_candidate_hash",
    "post_sandbox_review_metadata_invalid",
    "candidate_only_boundary_missing",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_result_available",
    "actual_post_sandbox_review_performed",
    "sandbox_failure_observed",
    "sandbox_success_observed",
    "rollback_triggered",
    "quarantine_triggered",
    "incident_triggered",
    "audit_log_written",
    "audit_evidence_persisted",
    "failure_handling_executed",
    "remediation_executed",
    "closure_audit_started",
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
    "star_cosmos_active_entry_claimed",
)

REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES = (
    "controlled_adapter_sandbox_candidate_input_section",
    "post_sandbox_review_metadata_section",
    "review_scope_section",
    "sandbox_result_unavailable_section",
    "actual_review_disabled_section",
    "rollback_disabled_section",
    "quarantine_disabled_section",
    "incident_disabled_section",
    "audit_log_write_disabled_section",
    "failure_handling_disabled_section",
    "sandbox_entry_disabled_section",
    "sandbox_runtime_disabled_section",
    "sandbox_execution_disabled_section",
    "external_network_write_disabled_section",
    "tool_command_routing_disabled_section",
    "adapter_manifest_execution_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_cosmos_candidate_only_section",
    "layer_14_closure_readiness_section",
)
REQUIRED_POST_SANDBOX_REVIEW_SECTION_NAMES = (
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES
)

REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES = (
    "post_sandbox_review_boundary_only_contract",
    "post_sandbox_review_metadata_only_contract",
    "controlled_adapter_sandbox_candidate_pass_contract",
    "controlled_adapter_sandbox_candidate_hash_present_contract",
    "controlled_adapter_sandbox_candidate_hash_stable_contract",
    "post_sandbox_review_readiness_conditions_declared_contract",
    "post_sandbox_review_evidence_requirements_declared_contract",
    "post_sandbox_review_blocking_conditions_declared_contract",
    "post_sandbox_review_sections_complete_contract",
    "post_sandbox_review_sections_pass_contract",
    "candidate_only_boundary_contract",
    "controlled_adapter_sandbox_not_started_contract",
    "adapter_sandbox_not_entered_contract",
    "sandbox_runtime_not_created_contract",
    "sandbox_execution_not_enabled_contract",
    "sandbox_result_not_available_contract",
    "actual_post_sandbox_review_not_performed_contract",
    "rollback_not_triggered_contract",
    "quarantine_not_triggered_contract",
    "incident_not_triggered_contract",
    "audit_log_not_written_contract",
    "audit_evidence_not_persisted_contract",
    "failure_handling_not_executed_contract",
    "remediation_not_executed_contract",
    "closure_audit_not_started_contract",
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
REQUIRED_POST_SANDBOX_REVIEW_CONTRACT_NAMES = (
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES
)

REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES = (
    "post_sandbox_review_boundary_stage_check",
    "post_sandbox_review_boundary_only_mode_check",
    "post_sandbox_review_metadata_only_check",
    "controlled_adapter_sandbox_candidate_pass_check",
    "controlled_adapter_sandbox_candidate_hash_present_check",
    "controlled_adapter_sandbox_candidate_hash_stable_check",
    "post_sandbox_review_readiness_conditions_declared_check",
    "post_sandbox_review_evidence_requirements_declared_check",
    "post_sandbox_review_blocking_conditions_declared_check",
    "post_sandbox_review_sections_complete_check",
    "post_sandbox_review_sections_pass_check",
    "post_sandbox_review_contracts_pass_check",
    "candidate_only_boundary_check",
    "controlled_adapter_sandbox_not_started_check",
    "adapter_sandbox_not_entered_check",
    "sandbox_runtime_not_created_check",
    "sandbox_execution_not_enabled_check",
    "sandbox_result_not_available_check",
    "actual_post_sandbox_review_not_performed_check",
    "rollback_not_triggered_check",
    "quarantine_not_triggered_check",
    "incident_not_triggered_check",
    "audit_log_not_written_check",
    "audit_evidence_not_persisted_check",
    "failure_handling_not_executed_check",
    "remediation_not_executed_check",
    "closure_audit_not_started_check",
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
    "deterministic_post_sandbox_review_boundary_hash_check",
    "layer_14_closure_readiness_check",
)
REQUIRED_POST_SANDBOX_REVIEW_CHECK_NAMES = (
    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES
)

_CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_REFS = (
    "controlled_adapter_sandbox_candidate_status",
    "deterministic_controlled_adapter_sandbox_candidate_hash",
    "controlled_adapter_sandbox_candidate_metadata",
)

_POST_SANDBOX_REVIEW_BOUNDARY_HASH_FIELDS = (
    "version",
    "schema_version",
    "post_sandbox_review_boundary_type",
    "post_sandbox_review_boundary_status",
    "post_sandbox_review_boundary_stage",
    "post_sandbox_review_boundary_mode",
    "post_sandbox_review_mode",
    "post_sandbox_review_status",
    "sandbox_result_status",
    "sandbox_review_status",
    "rollback_status",
    "quarantine_status",
    "incident_status",
    "audit_evidence_status",
    "failure_handling_status",
    "layer_14_closure_readiness_status",
    "star_cosmos_entry_status",
    "post_sandbox_review_declared",
    *COMMON_DISABLED_FLAGS,
    "controlled_adapter_sandbox_candidate_version",
    "controlled_adapter_sandbox_candidate_status",
    "controlled_adapter_sandbox_candidate_hash",
    "post_sandbox_review_metadata",
    "post_sandbox_review_sections",
    "post_sandbox_review_contracts",
    "post_sandbox_review_checks",
    "post_sandbox_review_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_POST_SANDBOX_REVIEW_BOUNDARY_HASH_FIELDS),
    "input_shape": "sanitized post-sandbox review boundary projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_controlled_adapter_sandbox_candidate_included": False,
    "sandbox_result_payload_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_DISABLED_CONTRACT_SPECS = (
    ("controlled_adapter_sandbox_not_started_contract", "controlled_adapter_sandbox_started"),
    ("adapter_sandbox_not_entered_contract", "adapter_sandbox_entered"),
    ("sandbox_runtime_not_created_contract", "sandbox_runtime_created"),
    ("sandbox_execution_not_enabled_contract", "sandbox_execution_enabled"),
    ("sandbox_result_not_available_contract", "sandbox_result_available"),
    (
        "actual_post_sandbox_review_not_performed_contract",
        "actual_post_sandbox_review_performed",
    ),
    ("rollback_not_triggered_contract", "rollback_triggered"),
    ("quarantine_not_triggered_contract", "quarantine_triggered"),
    ("incident_not_triggered_contract", "incident_triggered"),
    ("audit_log_not_written_contract", "audit_log_written"),
    ("audit_evidence_not_persisted_contract", "audit_evidence_persisted"),
    ("failure_handling_not_executed_contract", "failure_handling_executed"),
    ("remediation_not_executed_contract", "remediation_executed"),
    ("closure_audit_not_started_contract", "closure_audit_started"),
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


def build_governance_post_sandbox_review_boundary() -> dict[str, Any]:
    """Build deterministic future-post-sandbox-review-boundary-only metadata."""

    candidate, repeated_candidate = _controlled_adapter_sandbox_candidate_pair()
    metadata = _build_post_sandbox_review_metadata(candidate, repeated_candidate)
    sections = _build_post_sandbox_review_sections(
        candidate,
        repeated_candidate,
        metadata,
    )
    contracts = _build_post_sandbox_review_contracts(
        candidate,
        repeated_candidate,
        metadata,
        sections,
    )
    checks = _build_post_sandbox_review_checks(
        candidate,
        repeated_candidate,
        metadata,
        sections,
        contracts,
    )

    candidate_passes = _controlled_adapter_sandbox_candidate_passes(candidate)
    metadata_valid = _post_sandbox_review_metadata_valid(metadata)
    sections_pass = _sections_pass(sections)
    contracts_pass = _contracts_pass(contracts)
    checks_pass = _checks_pass(checks)
    boundary_status = (
        "pass"
        if candidate_passes
        and metadata_valid
        and sections_pass
        and contracts_pass
        and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["controlled adapter sandbox candidate must pass at version 6.4.0"]
                if not candidate_passes
                else []
            ),
            *(
                ["post-sandbox review boundary metadata must remain metadata-only"]
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
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION,
        "schema_version": GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_SCHEMA_VERSION,
        "post_sandbox_review_boundary_type": (
            GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_TYPE
        ),
        "post_sandbox_review_boundary_status": boundary_status,
        "post_sandbox_review_boundary_stage": POST_SANDBOX_REVIEW_BOUNDARY_STAGE,
        "post_sandbox_review_boundary_mode": POST_SANDBOX_REVIEW_BOUNDARY_MODE,
        "post_sandbox_review_mode": POST_SANDBOX_REVIEW_MODE,
        "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
        "sandbox_result_status": SANDBOX_RESULT_STATUS,
        "sandbox_review_status": SANDBOX_REVIEW_STATUS,
        "rollback_status": ROLLBACK_STATUS,
        "quarantine_status": QUARANTINE_STATUS,
        "incident_status": INCIDENT_STATUS,
        "audit_evidence_status": AUDIT_EVIDENCE_STATUS,
        "failure_handling_status": FAILURE_HANDLING_STATUS,
        "layer_14_closure_readiness_status": (
            LAYER_14_CLOSURE_READINESS_STATUS
        ),
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "post_sandbox_review_declared": True,
        **COMMON_DISABLED_FLAGS,
        "controlled_adapter_sandbox_candidate_version": _string_or_none(
            candidate.get("version")
        ),
        "controlled_adapter_sandbox_candidate_status": _string_or_none(
            candidate.get("controlled_adapter_sandbox_candidate_status")
        ),
        "controlled_adapter_sandbox_candidate_hash": candidate_hash,
        "post_sandbox_review_metadata": metadata,
        "post_sandbox_review_sections": sections,
        "post_sandbox_review_contracts": contracts,
        "post_sandbox_review_checks": checks,
        "post_sandbox_review_summary": _post_sandbox_review_summary(
            boundary_status,
            candidate,
            repeated_candidate,
            metadata,
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
    result["deterministic_post_sandbox_review_boundary_hash"] = (
        _post_sandbox_review_boundary_hash(result)
    )
    return _detached_json_value(result)


def get_governance_post_sandbox_review_boundary_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached review-boundary section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_boundary()["post_sandbox_review_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_post_sandbox_review_boundary_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached review-boundary contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_boundary()["post_sandbox_review_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_post_sandbox_review_boundary_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached review-boundary check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_boundary()["post_sandbox_review_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_post_sandbox_review_boundary_section_names() -> list[str]:
    """Return stable post-sandbox review section names."""

    return list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES)


def list_governance_post_sandbox_review_boundary_contract_names() -> list[str]:
    """Return stable post-sandbox review contract names."""

    return list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES)


def list_governance_post_sandbox_review_boundary_check_names() -> list[str]:
    """Return stable post-sandbox review check names."""

    return list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES)


def governance_post_sandbox_review_boundary_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize post-sandbox review boundary metadata deterministically."""

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
    return governance_post_sandbox_review_boundary_to_json(
        build_governance_post_sandbox_review_boundary()
    )


def _cached_boundary() -> dict[str, Any]:
    return json.loads(_cached_boundary_payload())


@lru_cache(maxsize=1)
def _cached_candidate_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_controlled_adapter_sandbox_candidate()
    )
    second = _detached_json_value(
        build_governance_controlled_adapter_sandbox_candidate()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _controlled_adapter_sandbox_candidate_pair() -> tuple[
    dict[str, Any],
    dict[str, Any],
]:
    first_payload, second_payload = _cached_candidate_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_post_sandbox_review_metadata(
    candidate: Mapping[str, Any],
    repeated_candidate: Mapping[str, Any],
) -> dict[str, Any]:
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    repeated_hash = _controlled_adapter_sandbox_candidate_hash(repeated_candidate)
    hash_present = _is_sha256(candidate_hash)
    hash_stable = hash_present and candidate_hash == repeated_hash
    review_ready = (
        _controlled_adapter_sandbox_candidate_passes(candidate)
        and hash_stable
        and _controlled_adapter_sandbox_candidate_metadata_valid(candidate)
        and _upstream_candidate_boundaries_disabled(candidate)
        and _all_safety_boundaries_false(candidate)
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "post_sandbox_review_metadata_type": (
                "future_post_sandbox_review_boundary_metadata"
            ),
            "post_sandbox_review_metadata_mode": POST_SANDBOX_REVIEW_MODE,
            "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
            "sandbox_result_status": SANDBOX_RESULT_STATUS,
            "sandbox_review_status": SANDBOX_REVIEW_STATUS,
            "rollback_status": ROLLBACK_STATUS,
            "quarantine_status": QUARANTINE_STATUS,
            "incident_status": INCIDENT_STATUS,
            "audit_evidence_status": AUDIT_EVIDENCE_STATUS,
            "failure_handling_status": FAILURE_HANDLING_STATUS,
            "layer_14_closure_readiness_status": (
                LAYER_14_CLOSURE_READINESS_STATUS
            ),
            "post_sandbox_review_required": True,
            "post_sandbox_review_metadata_available": True,
            "post_sandbox_review_declared": True,
            "candidate_only": True,
            "controlled_adapter_sandbox_candidate_pass_required": True,
            "controlled_adapter_sandbox_candidate_hash_required": True,
            "controlled_adapter_sandbox_candidate_status": _string_or_none(
                candidate.get("controlled_adapter_sandbox_candidate_status")
            ),
            "controlled_adapter_sandbox_candidate_hash_present": hash_present,
            "controlled_adapter_sandbox_candidate_hash_stable": hash_stable,
            "sandbox_candidate_metadata_available": (
                _controlled_adapter_sandbox_candidate_metadata_valid(candidate)
            ),
            "post_sandbox_review_readiness_conditions": list(
                REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES
            ),
            "required_post_sandbox_review_evidence": list(
                REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES
            ),
            "post_sandbox_review_blocking_conditions": list(
                REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES
            ),
            "post_sandbox_review_next_stage": (
                "star_cosmos_closure_handoff_audit"
            ),
            "post_sandbox_review_handoff_status": (
                READY_HANDOFF_STATUS if review_ready else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_post_sandbox_review_sections(
    candidate: Mapping[str, Any],
    repeated_candidate: Mapping[str, Any],
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    repeated_hash = _controlled_adapter_sandbox_candidate_hash(repeated_candidate)
    section_specs = (
        (
            "controlled_adapter_sandbox_candidate_input_section",
            "controlled_adapter_sandbox_candidate_input",
            {
                "controlled_adapter_sandbox_candidate_version": (
                    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION
                ),
                "controlled_adapter_sandbox_candidate_status": "pass",
                "controlled_adapter_sandbox_candidate_hash_present": True,
                "controlled_adapter_sandbox_candidate_hash_stable": True,
                "sandbox_candidate_metadata_available": True,
            },
            {
                "controlled_adapter_sandbox_candidate_version": _string_or_none(
                    candidate.get("version")
                ),
                "controlled_adapter_sandbox_candidate_status": _string_or_none(
                    candidate.get("controlled_adapter_sandbox_candidate_status")
                ),
                "controlled_adapter_sandbox_candidate_hash_present": _is_sha256(
                    candidate_hash
                ),
                "controlled_adapter_sandbox_candidate_hash_stable": (
                    _is_sha256(candidate_hash) and candidate_hash == repeated_hash
                ),
                "sandbox_candidate_metadata_available": (
                    _controlled_adapter_sandbox_candidate_metadata_valid(candidate)
                ),
            },
            ("Consumes detached deterministic sandbox-candidate metadata.",),
        ),
        (
            "post_sandbox_review_metadata_section",
            "post_sandbox_review_metadata_boundary",
            {
                "post_sandbox_review_metadata_mode": POST_SANDBOX_REVIEW_MODE,
                "post_sandbox_review_metadata_available": True,
                "post_sandbox_review_declared": True,
            },
            _select(
                metadata,
                (
                    "post_sandbox_review_metadata_mode",
                    "post_sandbox_review_metadata_available",
                    "post_sandbox_review_declared",
                ),
            ),
            ("Defines future review-boundary metadata only.",),
        ),
        (
            "review_scope_section",
            "post_sandbox_review_scope_boundary",
            {
                "candidate_only": True,
                "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
                "layer_14_closure_readiness_status": (
                    LAYER_14_CLOSURE_READINESS_STATUS
                ),
            },
            _select(
                metadata,
                (
                    "candidate_only",
                    "post_sandbox_review_status",
                    "layer_14_closure_readiness_status",
                ),
            ),
            ("Limits the result to future candidate review scope.",),
        ),
        (
            "sandbox_result_unavailable_section",
            "sandbox_result_unavailable_boundary",
            {
                "sandbox_result_status": SANDBOX_RESULT_STATUS,
                "sandbox_result_available": False,
                "sandbox_failure_observed": False,
                "sandbox_success_observed": False,
            },
            _select(
                metadata,
                (
                    "sandbox_result_status",
                    "sandbox_result_available",
                    "sandbox_failure_observed",
                    "sandbox_success_observed",
                ),
            ),
            ("Keeps sandbox result observations absent.",),
        ),
        (
            "actual_review_disabled_section",
            "actual_post_sandbox_review_disabled_boundary",
            {
                "sandbox_review_status": SANDBOX_REVIEW_STATUS,
                "actual_post_sandbox_review_performed": False,
            },
            _select(
                metadata,
                (
                    "sandbox_review_status",
                    "actual_post_sandbox_review_performed",
                ),
            ),
            ("Keeps actual post-sandbox review absent.",),
        ),
        (
            "rollback_disabled_section",
            "rollback_disabled_boundary",
            {"rollback_status": ROLLBACK_STATUS, "rollback_triggered": False},
            _select(metadata, ("rollback_status", "rollback_triggered")),
            ("Keeps rollback effects absent.",),
        ),
        (
            "quarantine_disabled_section",
            "quarantine_disabled_boundary",
            {
                "quarantine_status": QUARANTINE_STATUS,
                "quarantine_triggered": False,
            },
            _select(metadata, ("quarantine_status", "quarantine_triggered")),
            ("Keeps quarantine effects absent.",),
        ),
        (
            "incident_disabled_section",
            "incident_disabled_boundary",
            {"incident_status": INCIDENT_STATUS, "incident_triggered": False},
            _select(metadata, ("incident_status", "incident_triggered")),
            ("Keeps incident effects absent.",),
        ),
        (
            "audit_log_write_disabled_section",
            "audit_log_write_disabled_boundary",
            {
                "audit_evidence_status": AUDIT_EVIDENCE_STATUS,
                "audit_log_written": False,
                "audit_evidence_persisted": False,
                "closure_audit_started": False,
            },
            _select(
                metadata,
                (
                    "audit_evidence_status",
                    "audit_log_written",
                    "audit_evidence_persisted",
                    "closure_audit_started",
                ),
            ),
            ("Keeps audit-log and closure-audit effects absent.",),
        ),
        (
            "failure_handling_disabled_section",
            "failure_handling_disabled_boundary",
            {
                "failure_handling_status": FAILURE_HANDLING_STATUS,
                "failure_handling_executed": False,
                "remediation_executed": False,
            },
            _select(
                metadata,
                (
                    "failure_handling_status",
                    "failure_handling_executed",
                    "remediation_executed",
                ),
            ),
            ("Keeps failure handling and remediation absent.",),
        ),
        (
            "sandbox_entry_disabled_section",
            "sandbox_entry_disabled_boundary",
            {
                "controlled_adapter_sandbox_started": False,
                "adapter_sandbox_entered": False,
            },
            _select(
                metadata,
                (
                    "controlled_adapter_sandbox_started",
                    "adapter_sandbox_entered",
                ),
            ),
            ("Keeps sandbox start and entry absent.",),
        ),
        (
            "sandbox_runtime_disabled_section",
            "sandbox_runtime_disabled_boundary",
            {"sandbox_runtime_created": False},
            _select(metadata, ("sandbox_runtime_created",)),
            ("Keeps sandbox runtime creation absent.",),
        ),
        (
            "sandbox_execution_disabled_section",
            "sandbox_execution_disabled_boundary",
            {
                "sandbox_execution_enabled": False,
                "real_execution_enabled": False,
                "dry_run_plan_executed": False,
            },
            _select(
                metadata,
                (
                    "sandbox_execution_enabled",
                    "real_execution_enabled",
                    "dry_run_plan_executed",
                ),
            ),
            ("Keeps sandbox and plan execution absent.",),
        ),
        (
            "external_network_write_disabled_section",
            "external_network_write_disabled_boundary",
            {
                "external_calls_enabled": False,
                "network_calls_enabled": False,
                "durable_writes_enabled": False,
                "filesystem_writes_enabled": False,
                "database_writes_enabled": False,
                "memory_graph_mutation_enabled": False,
            },
            _select(
                metadata,
                (
                    "external_calls_enabled",
                    "network_calls_enabled",
                    "durable_writes_enabled",
                    "filesystem_writes_enabled",
                    "database_writes_enabled",
                    "memory_graph_mutation_enabled",
                ),
            ),
            ("Keeps external, network, and write surfaces disabled.",),
        ),
        (
            "tool_command_routing_disabled_section",
            "tool_command_routing_disabled_boundary",
            {
                "hermes_connected": False,
                "codex_connected": False,
                "openclaw_connected": False,
                "github_connected": False,
                "tool_routing_enabled": False,
                "command_routing_enabled": False,
                "cross_system_coordination_enabled": False,
                "system_handoff_completed": False,
            },
            _select(
                metadata,
                (
                    "hermes_connected",
                    "codex_connected",
                    "openclaw_connected",
                    "github_connected",
                    "tool_routing_enabled",
                    "command_routing_enabled",
                    "cross_system_coordination_enabled",
                    "system_handoff_completed",
                ),
            ),
            ("Keeps connections, routing, coordination, and handoff absent.",),
        ),
        (
            "adapter_manifest_execution_disabled_section",
            "adapter_manifest_execution_disabled_boundary",
            {
                "execution_adapter_implemented": False,
                "execution_adapter_invoked": False,
                "adapter_dispatched": False,
                "manifest_dispatched": False,
                "manifest_executed": False,
            },
            _select(
                metadata,
                (
                    "execution_adapter_implemented",
                    "execution_adapter_invoked",
                    "adapter_dispatched",
                    "manifest_dispatched",
                    "manifest_executed",
                ),
            ),
            ("Keeps adapter and manifest capability absent.",),
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
            _select(
                metadata,
                (
                    "operation_ledger_writes_enabled",
                    "operation_ledger_entry_created",
                    "operation_ledger_entry_written",
                    "operation_ledger_proposal_persisted",
                    "operation_ledger_proposal_submitted",
                    "operation_ledger_proposal_dispatched",
                ),
            ),
            ("Keeps operation-ledger write effects absent.",),
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
            "layer_14_closure_readiness_section",
            "layer_14_closure_readiness_boundary",
            {
                "layer_14_closure_readiness_status": (
                    LAYER_14_CLOSURE_READINESS_STATUS
                ),
                "post_sandbox_review_next_stage": (
                    "star_cosmos_closure_handoff_audit"
                ),
                "post_sandbox_review_handoff_status": READY_HANDOFF_STATUS,
                "post_sandbox_review_readiness_conditions": list(
                    REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES
                ),
            },
            _select(
                metadata,
                (
                    "layer_14_closure_readiness_status",
                    "post_sandbox_review_next_stage",
                    "post_sandbox_review_handoff_status",
                    "post_sandbox_review_readiness_conditions",
                ),
            ),
            ("Marks readiness for future closure-handoff audit design only.",),
        ),
    )
    return [
        _section_from_expected(
            name,
            section_type=section_type,
            expected=expected,
            observed=observed,
            post_sandbox_review_notes=notes,
        )
        for name, section_type, expected, observed, notes in section_specs
    ]


def _build_post_sandbox_review_contracts(
    candidate: Mapping[str, Any],
    repeated_candidate: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    repeated_hash = _controlled_adapter_sandbox_candidate_hash(repeated_candidate)
    contracts = [
        _contract_from_expected(
            "post_sandbox_review_boundary_only_contract",
            contract_type="post_sandbox_review_boundary_mode_contract",
            expected={
                "post_sandbox_review_boundary_mode": (
                    POST_SANDBOX_REVIEW_BOUNDARY_MODE
                )
            },
            observed={
                "post_sandbox_review_boundary_mode": (
                    POST_SANDBOX_REVIEW_BOUNDARY_MODE
                )
            },
        ),
        _contract_from_expected(
            "post_sandbox_review_metadata_only_contract",
            contract_type="post_sandbox_review_metadata_contract",
            expected={
                "post_sandbox_review_metadata_mode": POST_SANDBOX_REVIEW_MODE,
                "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "post_sandbox_review_metadata_mode",
                    "post_sandbox_review_status",
                ),
            ),
        ),
        _contract_from_expected(
            "controlled_adapter_sandbox_candidate_pass_contract",
            contract_type="sandbox_candidate_status_contract",
            expected={
                "controlled_adapter_sandbox_candidate_version": (
                    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION
                ),
                "controlled_adapter_sandbox_candidate_status": "pass",
            },
            observed={
                "controlled_adapter_sandbox_candidate_version": _string_or_none(
                    candidate.get("version")
                ),
                "controlled_adapter_sandbox_candidate_status": _string_or_none(
                    candidate.get("controlled_adapter_sandbox_candidate_status")
                ),
            },
        ),
        _contract_from_expected(
            "controlled_adapter_sandbox_candidate_hash_present_contract",
            contract_type="sandbox_candidate_hash_contract",
            expected={"controlled_adapter_sandbox_candidate_hash_present": True},
            observed={
                "controlled_adapter_sandbox_candidate_hash_present": _is_sha256(
                    candidate_hash
                )
            },
        ),
        _contract_from_expected(
            "controlled_adapter_sandbox_candidate_hash_stable_contract",
            contract_type="sandbox_candidate_hash_contract",
            expected={"controlled_adapter_sandbox_candidate_hash_stable": True},
            observed={
                "controlled_adapter_sandbox_candidate_hash_stable": (
                    _is_sha256(candidate_hash) and candidate_hash == repeated_hash
                )
            },
        ),
        *_requirements_contracts(metadata),
        _contract_from_expected(
            "post_sandbox_review_sections_complete_contract",
            contract_type="post_sandbox_review_sections_contract",
            expected={
                "post_sandbox_review_section_names": list(
                    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES
                )
            },
            observed={"post_sandbox_review_section_names": _section_names(sections)},
        ),
        _contract_from_expected(
            "post_sandbox_review_sections_pass_contract",
            contract_type="post_sandbox_review_sections_contract",
            expected={"post_sandbox_review_sections_pass": True},
            observed={"post_sandbox_review_sections_pass": _sections_pass(sections)},
        ),
        _contract_from_expected(
            "candidate_only_boundary_contract",
            contract_type="candidate_only_boundary_contract",
            expected={
                "candidate_only": True,
                "layer_14_closure_readiness_status": (
                    LAYER_14_CLOSURE_READINESS_STATUS
                ),
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "candidate_only",
                    "layer_14_closure_readiness_status",
                    "star_cosmos_entry_status",
                ),
            ),
        ),
        *[
            _contract_from_expected(
                contract_name,
                contract_type="disabled_post_sandbox_review_boundary_contract",
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
            "post_sandbox_review_readiness_conditions_declared_contract",
            "post_sandbox_review_readiness_conditions",
            list(REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES),
        ),
        (
            "post_sandbox_review_evidence_requirements_declared_contract",
            "required_post_sandbox_review_evidence",
            list(REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "post_sandbox_review_blocking_conditions_declared_contract",
            "post_sandbox_review_blocking_conditions",
            list(REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES),
        ),
    )
    return [
        _contract_from_expected(
            contract_name,
            contract_type="post_sandbox_review_requirements_contract",
            expected={field_name: expected_value},
            observed={field_name: metadata.get(field_name)},
        )
        for contract_name, field_name, expected_value in specs
    ]


def _build_post_sandbox_review_checks(
    candidate: Mapping[str, Any],
    repeated_candidate: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    repeated_hash = _controlled_adapter_sandbox_candidate_hash(repeated_candidate)
    checks = [
        _check_from_expected(
            "post_sandbox_review_boundary_stage_check",
            expected={
                "post_sandbox_review_boundary_stage": (
                    POST_SANDBOX_REVIEW_BOUNDARY_STAGE
                )
            },
            observed={
                "post_sandbox_review_boundary_stage": (
                    POST_SANDBOX_REVIEW_BOUNDARY_STAGE
                )
            },
        ),
        _check_from_expected(
            "post_sandbox_review_boundary_only_mode_check",
            expected={
                "post_sandbox_review_boundary_mode": (
                    POST_SANDBOX_REVIEW_BOUNDARY_MODE
                )
            },
            observed={
                "post_sandbox_review_boundary_mode": (
                    POST_SANDBOX_REVIEW_BOUNDARY_MODE
                )
            },
        ),
        _check_from_expected(
            "post_sandbox_review_metadata_only_check",
            expected={
                "post_sandbox_review_metadata_mode": POST_SANDBOX_REVIEW_MODE,
                "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "post_sandbox_review_metadata_mode",
                    "post_sandbox_review_status",
                ),
            ),
        ),
        _check_from_expected(
            "controlled_adapter_sandbox_candidate_pass_check",
            expected={"controlled_adapter_sandbox_candidate_status": "pass"},
            observed={
                "controlled_adapter_sandbox_candidate_status": _string_or_none(
                    candidate.get("controlled_adapter_sandbox_candidate_status")
                )
            },
        ),
        _check_from_expected(
            "controlled_adapter_sandbox_candidate_hash_present_check",
            expected={"controlled_adapter_sandbox_candidate_hash_present": True},
            observed={
                "controlled_adapter_sandbox_candidate_hash_present": _is_sha256(
                    candidate_hash
                )
            },
        ),
        _check_from_expected(
            "controlled_adapter_sandbox_candidate_hash_stable_check",
            expected={"controlled_adapter_sandbox_candidate_hash_stable": True},
            observed={
                "controlled_adapter_sandbox_candidate_hash_stable": (
                    _is_sha256(candidate_hash) and candidate_hash == repeated_hash
                )
            },
        ),
        *_requirements_checks(metadata),
        _check_from_expected(
            "post_sandbox_review_sections_complete_check",
            expected={
                "post_sandbox_review_section_names": list(
                    REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES
                )
            },
            observed={"post_sandbox_review_section_names": _section_names(sections)},
        ),
        _check_from_expected(
            "post_sandbox_review_sections_pass_check",
            expected={"post_sandbox_review_sections_pass": True},
            observed={"post_sandbox_review_sections_pass": _sections_pass(sections)},
        ),
        _check_from_expected(
            "post_sandbox_review_contracts_pass_check",
            expected={"post_sandbox_review_contracts_pass": True},
            observed={
                "post_sandbox_review_contracts_pass": _contracts_pass(contracts)
            },
        ),
        _check_from_expected(
            "candidate_only_boundary_check",
            expected={
                "candidate_only": True,
                "layer_14_closure_readiness_status": (
                    LAYER_14_CLOSURE_READINESS_STATUS
                ),
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            },
            observed=_select(
                metadata,
                (
                    "candidate_only",
                    "layer_14_closure_readiness_status",
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
            for check_name, field_name in _DISABLED_CHECK_SPECS
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
            "deterministic_post_sandbox_review_boundary_hash_check",
            expected={
                "hash_algorithm": (
                    GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_HASH_ALGORITHM
                ),
                "hash_projection_declared": True,
            },
            observed={
                "hash_algorithm": HASH_INPUT_CONTRACT["algorithm"],
                "hash_projection_declared": (
                    HASH_INPUT_CONTRACT["hash_fields"]
                    == list(_POST_SANDBOX_REVIEW_BOUNDARY_HASH_FIELDS)
                ),
            },
        ),
        _check_from_expected(
            "layer_14_closure_readiness_check",
            expected={
                "post_sandbox_review_handoff_status": READY_HANDOFF_STATUS,
                "post_sandbox_review_sections_pass": True,
                "post_sandbox_review_contracts_pass": True,
            },
            observed={
                "post_sandbox_review_handoff_status": metadata.get(
                    "post_sandbox_review_handoff_status"
                ),
                "post_sandbox_review_sections_pass": _sections_pass(sections),
                "post_sandbox_review_contracts_pass": _contracts_pass(contracts),
            },
        ),
    ]
    return _detached_json_value(checks)


def _requirements_checks(
    metadata: Mapping[str, Any],
) -> list[dict[str, Any]]:
    specs = (
        (
            "post_sandbox_review_readiness_conditions_declared_check",
            "post_sandbox_review_readiness_conditions",
            list(REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES),
        ),
        (
            "post_sandbox_review_evidence_requirements_declared_check",
            "required_post_sandbox_review_evidence",
            list(REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES),
        ),
        (
            "post_sandbox_review_blocking_conditions_declared_check",
            "post_sandbox_review_blocking_conditions",
            list(REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES),
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


def _post_sandbox_review_summary(
    boundary_status: str,
    candidate: Mapping[str, Any],
    repeated_candidate: Mapping[str, Any],
    metadata: Mapping[str, Any],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    candidate_hash = _controlled_adapter_sandbox_candidate_hash(candidate)
    repeated_hash = _controlled_adapter_sandbox_candidate_hash(repeated_candidate)
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "post_sandbox_review_boundary_summary",
            "post_sandbox_review_boundary_status": boundary_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if boundary_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "post_sandbox_review_mode": POST_SANDBOX_REVIEW_MODE,
            "post_sandbox_review_status": POST_SANDBOX_REVIEW_STATUS,
            "sandbox_result_status": SANDBOX_RESULT_STATUS,
            "sandbox_review_status": SANDBOX_REVIEW_STATUS,
            "rollback_status": ROLLBACK_STATUS,
            "quarantine_status": QUARANTINE_STATUS,
            "incident_status": INCIDENT_STATUS,
            "audit_evidence_status": AUDIT_EVIDENCE_STATUS,
            "failure_handling_status": FAILURE_HANDLING_STATUS,
            "layer_14_closure_readiness_status": (
                LAYER_14_CLOSURE_READINESS_STATUS
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "controlled_adapter_sandbox_candidate_version": _string_or_none(
                candidate.get("version")
            ),
            "controlled_adapter_sandbox_candidate_status": _string_or_none(
                candidate.get("controlled_adapter_sandbox_candidate_status")
            ),
            "controlled_adapter_sandbox_candidate_hash_present": _is_sha256(
                candidate_hash
            ),
            "controlled_adapter_sandbox_candidate_hash_stable": (
                _is_sha256(candidate_hash) and candidate_hash == repeated_hash
            ),
            "post_sandbox_review_metadata_valid": (
                _post_sandbox_review_metadata_valid(metadata)
            ),
            "post_sandbox_review_section_count": len(sections),
            "post_sandbox_review_sections_pass": _sections_pass(sections),
            "post_sandbox_review_contract_count": len(contracts),
            "post_sandbox_review_contracts_pass": _contracts_pass(contracts),
            "post_sandbox_review_check_count": len(checks),
            "post_sandbox_review_checks_pass": _checks_pass(checks),
            "post_sandbox_review_declared": True,
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
    post_sandbox_review_notes: Sequence[str],
) -> dict[str, Any]:
    blocking_reasons = _expected_blocking_reasons(
        expected,
        observed,
        "post-sandbox review boundary section values must match",
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": section_name,
            "section_type": section_type,
            "section_status": "pass" if not blocking_reasons else "blocked",
            "source_controlled_adapter_sandbox_candidate_refs": list(
                _CONTROLLED_ADAPTER_SANDBOX_CANDIDATE_REFS
            ),
            "expected": dict(expected),
            "observed": dict(observed),
            "post_sandbox_review_notes": list(post_sandbox_review_notes),
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
        "post-sandbox review boundary contract values must match",
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
        "post-sandbox review boundary check values must match",
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
            "section_type": "unknown_post_sandbox_review_boundary_section",
            "section_status": "blocked",
            "source_controlled_adapter_sandbox_candidate_refs": [],
            "expected": {"known_section_name": True},
            "observed": {
                "known_section_name": False,
                "requested_section_name": name,
            },
            "post_sandbox_review_notes": [],
            "blocking_reasons": [
                "post-sandbox review boundary section name is not recognized"
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
            "contract_type": "unknown_post_sandbox_review_boundary_contract",
            "expected": {"known_contract_name": True},
            "observed": {
                "known_contract_name": False,
                "requested_contract_name": name,
            },
            "contract_status": "blocked",
            "blocking_reasons": [
                "post-sandbox review boundary contract name is not recognized"
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
                "post-sandbox review boundary check name is not recognized"
            ],
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _post_sandbox_review_boundary_hash(result: Mapping[str, Any]) -> str:
    projection = {
        field: result[field]
        for field in _POST_SANDBOX_REVIEW_BOUNDARY_HASH_FIELDS
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


def _controlled_adapter_sandbox_candidate_hash(
    candidate: Mapping[str, Any],
) -> str | None:
    return _string_or_none(
        candidate.get("deterministic_controlled_adapter_sandbox_candidate_hash")
    )


def _controlled_adapter_sandbox_candidate_passes(
    candidate: Mapping[str, Any],
) -> bool:
    return (
        candidate.get("controlled_adapter_sandbox_candidate_status") == "pass"
        and candidate.get("version")
        == GOVERNANCE_POST_SANDBOX_REVIEW_BOUNDARY_VERSION
        and _is_sha256(_controlled_adapter_sandbox_candidate_hash(candidate))
        and candidate.get("controlled_adapter_sandbox_started") is False
        and candidate.get("adapter_sandbox_entered") is False
        and candidate.get("sandbox_runtime_created") is False
        and candidate.get("sandbox_execution_enabled") is False
        and candidate.get("star_cosmos_memory_active") is False
    )


def _controlled_adapter_sandbox_candidate_metadata_valid(
    candidate: Mapping[str, Any],
) -> bool:
    metadata = candidate.get("controlled_adapter_sandbox_candidate_metadata")
    return (
        isinstance(metadata, Mapping)
        and metadata.get("sandbox_candidate_metadata_mode") == "metadata_only"
        and metadata.get("sandbox_candidate_metadata_available") is True
        and metadata.get("sandbox_candidate_declared") is True
        and metadata.get("candidate_only") is True
        and metadata.get("controlled_adapter_sandbox_started") is False
        and metadata.get("adapter_sandbox_entered") is False
        and metadata.get("sandbox_runtime_created") is False
        and metadata.get("sandbox_execution_enabled") is False
    )


def _post_sandbox_review_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("post_sandbox_review_metadata_type")
        == "future_post_sandbox_review_boundary_metadata"
        and metadata.get("post_sandbox_review_metadata_mode")
        == POST_SANDBOX_REVIEW_MODE
        and metadata.get("post_sandbox_review_status")
        == POST_SANDBOX_REVIEW_STATUS
        and metadata.get("sandbox_result_status") == SANDBOX_RESULT_STATUS
        and metadata.get("sandbox_review_status") == SANDBOX_REVIEW_STATUS
        and metadata.get("rollback_status") == ROLLBACK_STATUS
        and metadata.get("quarantine_status") == QUARANTINE_STATUS
        and metadata.get("incident_status") == INCIDENT_STATUS
        and metadata.get("audit_evidence_status") == AUDIT_EVIDENCE_STATUS
        and metadata.get("failure_handling_status") == FAILURE_HANDLING_STATUS
        and metadata.get("layer_14_closure_readiness_status")
        == LAYER_14_CLOSURE_READINESS_STATUS
        and metadata.get("post_sandbox_review_required") is True
        and metadata.get("post_sandbox_review_metadata_available") is True
        and metadata.get("post_sandbox_review_declared") is True
        and metadata.get("candidate_only") is True
        and metadata.get("controlled_adapter_sandbox_candidate_pass_required")
        is True
        and metadata.get("controlled_adapter_sandbox_candidate_hash_required")
        is True
        and metadata.get("controlled_adapter_sandbox_candidate_status") == "pass"
        and metadata.get("controlled_adapter_sandbox_candidate_hash_present")
        is True
        and metadata.get("controlled_adapter_sandbox_candidate_hash_stable")
        is True
        and metadata.get("sandbox_candidate_metadata_available") is True
        and metadata.get("post_sandbox_review_readiness_conditions")
        == list(REQUIRED_POST_SANDBOX_REVIEW_READINESS_CONDITION_NAMES)
        and metadata.get("required_post_sandbox_review_evidence")
        == list(REQUIRED_POST_SANDBOX_REVIEW_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("post_sandbox_review_blocking_conditions")
        == list(REQUIRED_POST_SANDBOX_REVIEW_BLOCKING_CONDITION_NAMES)
        and metadata.get("post_sandbox_review_next_stage")
        == "star_cosmos_closure_handoff_audit"
        and metadata.get("post_sandbox_review_handoff_status")
        == READY_HANDOFF_STATUS
        and metadata.get("star_cosmos_entry_status")
        == STAR_COSMOS_ENTRY_STATUS
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _sections_pass(sections: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [section.get("section_name") for section in sections]
        == list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_SECTION_NAMES)
        and all(section.get("section_status") == "pass" for section in sections)
    )


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [contract.get("contract_name") for contract in contracts]
        == list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CONTRACT_NAMES)
        and all(
            contract.get("contract_status") == "pass" for contract in contracts
        )
    )


def _checks_pass(checks: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [check.get("check_name") for check in checks]
        == list(REQUIRED_POST_SANDBOX_REVIEW_BOUNDARY_CHECK_NAMES)
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


def _upstream_candidate_boundaries_disabled(value: Mapping[str, Any]) -> bool:
    required_false_fields = (
        "star_cosmos_memory_active",
        "controlled_adapter_sandbox_started",
        "adapter_sandbox_entered",
        "sandbox_runtime_created",
        "sandbox_execution_enabled",
        "hermes_connected",
        "codex_connected",
        "openclaw_connected",
        "github_connected",
        "tool_routing_enabled",
        "command_routing_enabled",
        "cross_system_coordination_enabled",
        "system_handoff_completed",
        "execution_adapter_implemented",
        "execution_adapter_invoked",
        "adapter_dispatched",
        "manifest_dispatched",
        "manifest_executed",
        "dry_run_plan_executed",
        "real_execution_enabled",
        "external_calls_enabled",
        "network_calls_enabled",
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
    )
    return all(value.get(key) is False for key in required_false_fields)


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
