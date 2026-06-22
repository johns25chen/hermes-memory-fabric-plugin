"""Deterministic Layer 15 Star-Source Memory entry-candidate metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_star_cosmos_closure_handoff_audit import (
    build_governance_star_cosmos_closure_handoff_audit,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_VERSION = "6.5.0"
GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SCHEMA_VERSION = "6.5.0"
GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_TYPE = (
    "governance_star_source_memory_entry_candidate"
)
GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_HASH_ALGORITHM = "sha256"
STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_STAGE = (
    "v6.0_star_source_memory_entry_candidate"
)
STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_MODE = "star_source_entry_candidate_only"
STAR_SOURCE_MEMORY_MODE = "metadata_only"
STAR_SOURCE_ENTRY_STATUS = "entry_candidate_only"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ENTRY_STATUS = "entry_candidate_only"
SOURCE_PROVENANCE_STATUS = "not_active"
METHODOLOGY_REVERSE_INFERENCE_STATUS = "not_active"
SELF_EVOLUTION_STATUS = "not_active"
V6_ENTRY_STATUS = "entry_candidate_only"
V6_HANDOFF_ACCEPTANCE_STATUS = "accepted_as_metadata_only"

READY_HANDOFF_STATUS = (
    "ready_for_source_constitution_registry_design"
)
STAR_SOURCE_ENTRY_NEXT_STAGE = "v6.1_source_constitution_registry"
STAR_SOURCE_ENTRY_NEXT_STAGE_TITLE = "Source Constitution Registry"
UPSTREAM_READY_HANDOFF_STATUS = (
    "ready_for_v6_star_source_entry_candidate_design"
)
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_source_memory_active": False,
    "star_source_active_entry_claimed": False,
    "star_source_entry_candidate_activated": False,
    "layer_15_active": False,
    "source_provenance_active": False,
    "methodology_reverse_inference_active": False,
    "self_evolution_active": False,
    "source_graph_created": False,
    "source_graph_mutation_enabled": False,
    "source_provenance_engine_created": False,
    "methodology_reverse_inference_engine_created": False,
    "self_evolution_engine_created": False,
    "autonomous_rule_mutation_enabled": False,
    "governance_policy_mutation_enabled": False,
    "memory_graph_mutation_enabled": False,
    "real_execution_enabled": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "adapter_dispatched": False,
    "manifest_dispatched": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "controlled_adapter_sandbox_started": False,
    "adapter_sandbox_entered": False,
    "sandbox_runtime_created": False,
    "sandbox_execution_enabled": False,
    "sandbox_network_enabled": False,
    "sandbox_writes_enabled": False,
    "sandbox_result_available": False,
    "actual_post_sandbox_review_performed": False,
    "rollback_triggered": False,
    "quarantine_triggered": False,
    "incident_triggered": False,
    "audit_log_written": False,
    "closure_record_written": False,
    "external_calls_enabled": False,
    "network_calls_enabled": False,
    "durable_writes_enabled": False,
    "filesystem_writes_enabled": False,
    "database_writes_enabled": False,
    "hermes_connected": False,
    "codex_connected": False,
    "openclaw_connected": False,
    "github_connected": False,
    "composio_connected": False,
    "tool_routing_enabled": False,
    "command_routing_enabled": False,
    "cross_system_coordination_enabled": False,
    "system_handoff_completed": False,
    "operation_ledger_writes_enabled": False,
    "operation_ledger_entry_created": False,
    "operation_ledger_entry_written": False,
    "operation_ledger_proposal_persisted": False,
    "operation_ledger_proposal_submitted": False,
    "operation_ledger_proposal_dispatched": False,
    "autonomous_execution_enabled": False,
    "approval_request_created": False,
    "real_approval_record_written": False,
    "approval_notification_sent": False,
    "execution_authorization_issued": False,
    "authorization_token_created": False,
    "authorization_grant_created": False,
}

REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES = (
    "star_cosmos_closure_handoff_audit_pass",
    "star_cosmos_closure_handoff_audit_hash_present",
    "star_cosmos_closure_handoff_audit_hash_stable",
    "star_cosmos_handoff_ready",
    "star_source_entry_candidate_declared",
    "star_source_entry_candidate_not_activated",
    "layer_15_not_active",
    "star_source_memory_not_active",
    "source_provenance_not_active",
    "methodology_reverse_inference_not_active",
    "self_evolution_not_active",
    "source_graph_not_created",
    "source_graph_mutation_not_enabled",
    "source_provenance_engine_not_created",
    "methodology_reverse_inference_engine_not_created",
    "self_evolution_engine_not_created",
    "autonomous_rule_mutation_not_enabled",
    "governance_policy_mutation_not_enabled",
    "memory_graph_mutation_not_enabled",
    "metadata_only_boundary_declared",
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
    "no_operation_ledger_writes",
    "no_real_approval_record",
    "no_approval_notification",
    "no_execution_authorization_issued",
    "no_authorization_token_created",
    "no_authorization_grant_created",
    "no_star_source_active_entry",
)

REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES = (
    "star_cosmos_closure_handoff_audit_pass_evidence",
    "deterministic_star_cosmos_closure_handoff_audit_hash_evidence",
    "star_cosmos_handoff_ready_evidence",
    "star_source_entry_metadata_evidence",
    "source_provenance_entry_metadata_evidence",
    "methodology_reverse_inference_entry_metadata_evidence",
    "self_evolution_entry_metadata_evidence",
    "star_source_entry_candidate_not_activated_evidence",
    "layer_15_not_active_evidence",
    "star_source_memory_not_active_evidence",
    "source_provenance_not_active_evidence",
    "methodology_reverse_inference_not_active_evidence",
    "self_evolution_not_active_evidence",
    "source_graph_not_created_evidence",
    "source_graph_mutation_not_enabled_evidence",
    "source_provenance_engine_not_created_evidence",
    "methodology_reverse_inference_engine_not_created_evidence",
    "self_evolution_engine_not_created_evidence",
    "autonomous_rule_mutation_not_enabled_evidence",
    "governance_policy_mutation_not_enabled_evidence",
    "memory_graph_mutation_not_enabled_evidence",
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
    "no_operation_ledger_write_evidence",
    "no_real_approval_record_evidence",
    "no_approval_notification_evidence",
    "no_execution_authorization_issued_evidence",
    "no_authorization_token_created_evidence",
    "no_authorization_grant_created_evidence",
    "no_star_source_active_entry_evidence",
)

REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES = (
    "star_cosmos_closure_handoff_audit_blocked",
    "missing_star_cosmos_closure_handoff_audit_hash",
    "unstable_star_cosmos_closure_handoff_audit_hash",
    "star_cosmos_handoff_not_ready",
    "star_source_entry_metadata_invalid",
    "source_provenance_entry_metadata_invalid",
    "methodology_reverse_inference_entry_metadata_invalid",
    "self_evolution_entry_metadata_invalid",
    "star_source_entry_candidate_activated",
    "layer_15_active",
    "star_source_memory_active",
    "source_provenance_active",
    "methodology_reverse_inference_active",
    "self_evolution_active",
    "source_graph_created",
    "source_graph_mutation_enabled",
    "source_provenance_engine_created",
    "methodology_reverse_inference_engine_created",
    "self_evolution_engine_created",
    "autonomous_rule_mutation_enabled",
    "governance_policy_mutation_enabled",
    "memory_graph_mutation_enabled",
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
    "operation_ledger_writes_enabled",
    "real_approval_record_written",
    "approval_notification_sent",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
    "star_source_active_entry_claimed",
)

REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES = (
    "star_cosmos_closure_handoff_input_section",
    "star_source_entry_metadata_section",
    "source_provenance_entry_metadata_section",
    "methodology_reverse_inference_entry_metadata_section",
    "self_evolution_entry_metadata_section",
    "layer_15_entry_candidate_only_section",
    "star_source_inactive_section",
    "source_graph_disabled_section",
    "source_provenance_engine_disabled_section",
    "methodology_reverse_inference_engine_disabled_section",
    "self_evolution_engine_disabled_section",
    "autonomous_rule_mutation_disabled_section",
    "governance_policy_mutation_disabled_section",
    "memory_graph_mutation_disabled_section",
    "external_network_write_disabled_section",
    "adapter_manifest_execution_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_source_active_entry_disabled_section",
    "next_stage_source_constitution_registry_section",
)

REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES = (
    "star_source_entry_candidate_only_contract",
    "star_source_entry_metadata_only_contract",
    "star_cosmos_closure_handoff_audit_pass_contract",
    "star_cosmos_closure_handoff_audit_hash_present_contract",
    "star_cosmos_closure_handoff_audit_hash_stable_contract",
    "star_cosmos_handoff_ready_contract",
    "source_provenance_not_active_contract",
    "methodology_reverse_inference_not_active_contract",
    "self_evolution_not_active_contract",
    "star_source_entry_candidate_not_activated_contract",
    "layer_15_not_active_contract",
    "star_source_memory_not_active_contract",
    "source_graph_not_created_contract",
    "source_graph_mutation_not_enabled_contract",
    "source_provenance_engine_not_created_contract",
    "methodology_reverse_inference_engine_not_created_contract",
    "self_evolution_engine_not_created_contract",
    "autonomous_rule_mutation_not_enabled_contract",
    "governance_policy_mutation_not_enabled_contract",
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
    "no_star_source_active_entry_contract",
)

REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES = (
    "star_source_entry_candidate_stage_check",
    "star_source_entry_candidate_only_mode_check",
    "star_source_metadata_only_check",
    "star_cosmos_closure_handoff_audit_pass_check",
    "star_cosmos_closure_handoff_audit_hash_present_check",
    "star_cosmos_closure_handoff_audit_hash_stable_check",
    "star_cosmos_handoff_ready_check",
    "star_source_entry_readiness_conditions_declared_check",
    "star_source_entry_evidence_requirements_declared_check",
    "star_source_entry_blocking_conditions_declared_check",
    "star_source_entry_sections_complete_check",
    "star_source_entry_sections_pass_check",
    "star_source_entry_contracts_pass_check",
    "source_provenance_not_active_check",
    "methodology_reverse_inference_not_active_check",
    "self_evolution_not_active_check",
    "star_source_entry_candidate_not_activated_check",
    "layer_15_not_active_check",
    "star_source_memory_not_active_check",
    "source_graph_not_created_check",
    "source_graph_mutation_not_enabled_check",
    "source_provenance_engine_not_created_check",
    "methodology_reverse_inference_engine_not_created_check",
    "self_evolution_engine_not_created_check",
    "autonomous_rule_mutation_not_enabled_check",
    "governance_policy_mutation_not_enabled_check",
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
    "no_star_source_active_entry_check",
    "deterministic_star_source_memory_entry_candidate_hash_check",
    "ready_for_source_constitution_registry_design_check",
)

_UPSTREAM_REFS = (
    "star_cosmos_closure_handoff_audit_status",
    "deterministic_star_cosmos_closure_handoff_audit_hash",
    "handoff_status",
)

_DISABLED_CONTRACT_FIELDS = {
    "source_provenance_not_active_contract": "source_provenance_active",
    "methodology_reverse_inference_not_active_contract": (
        "methodology_reverse_inference_active"
    ),
    "self_evolution_not_active_contract": "self_evolution_active",
    "star_source_entry_candidate_not_activated_contract": (
        "star_source_memory_active"
    ),
    "layer_15_not_active_contract": "layer_15_active",
    "star_source_memory_not_active_contract": "star_source_memory_active",
    "source_graph_not_created_contract": "source_graph_created",
    "source_graph_mutation_not_enabled_contract": (
        "source_graph_mutation_enabled"
    ),
    "source_provenance_engine_not_created_contract": (
        "source_provenance_engine_created"
    ),
    "methodology_reverse_inference_engine_not_created_contract": (
        "methodology_reverse_inference_engine_created"
    ),
    "self_evolution_engine_not_created_contract": "self_evolution_engine_created",
    "autonomous_rule_mutation_not_enabled_contract": (
        "autonomous_rule_mutation_enabled"
    ),
    "governance_policy_mutation_not_enabled_contract": (
        "governance_policy_mutation_enabled"
    ),
    "no_real_execution_contract": "real_execution_enabled",
    "no_adapter_invocation_contract": "execution_adapter_invoked",
    "no_adapter_dispatch_contract": "adapter_dispatched",
    "no_manifest_dispatch_contract": "manifest_dispatched",
    "no_manifest_execution_contract": "manifest_executed",
    "no_dry_run_plan_execution_contract": "dry_run_plan_executed",
    "no_external_call_contract": "external_calls_enabled",
    "no_network_call_contract": "network_calls_enabled",
    "no_durable_write_contract": "durable_writes_enabled",
    "no_filesystem_write_contract": "filesystem_writes_enabled",
    "no_database_write_contract": "database_writes_enabled",
    "no_memory_graph_mutation_contract": "memory_graph_mutation_enabled",
    "no_operation_ledger_write_contract": "operation_ledger_writes_enabled",
    "no_real_approval_record_contract": "real_approval_record_written",
    "no_approval_notification_contract": "approval_notification_sent",
    "no_execution_authorization_issued_contract": (
        "execution_authorization_issued"
    ),
    "no_authorization_token_created_contract": "authorization_token_created",
    "no_authorization_grant_created_contract": "authorization_grant_created",
    "no_star_source_active_entry_contract": "star_source_active_entry_claimed",
}

_HASH_FIELDS = (
    "version",
    "schema_version",
    "star_source_memory_entry_candidate_type",
    "star_source_memory_entry_candidate_status",
    "star_source_memory_entry_candidate_stage",
    "star_source_memory_entry_candidate_mode",
    "star_source_memory_mode",
    "star_source_entry_status",
    "star_source_memory_active_status",
    "layer_15_entry_status",
    "source_provenance_status",
    "methodology_reverse_inference_status",
    "self_evolution_status",
    "v6_entry_status",
    "v6_handoff_acceptance_status",
    *COMMON_DISABLED_FLAGS,
    "star_cosmos_closure_handoff_audit_version",
    "star_cosmos_closure_handoff_audit_status",
    "star_cosmos_closure_handoff_audit_hash",
    "star_source_entry_metadata",
    "source_provenance_entry_metadata",
    "methodology_reverse_inference_entry_metadata",
    "self_evolution_entry_metadata",
    "star_source_entry_sections",
    "star_source_entry_contracts",
    "star_source_entry_checks",
    "star_source_entry_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Layer 15 entry-candidate projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_star_cosmos_closure_handoff_audit_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_star_source_memory_entry_candidate() -> dict[str, Any]:
    """Build deterministic Layer-15-entry-candidate-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_hash = _upstream_hash(repeated_upstream)
    upstream_pass = _upstream_passes(upstream)
    hash_present = _is_sha256(upstream_hash)
    hash_stable = hash_present and upstream_hash == repeated_hash
    handoff_ready = (
        upstream.get("handoff_status") == UPSTREAM_READY_HANDOFF_STATUS
    )

    metadata = _build_star_source_entry_metadata(
        upstream_pass=upstream_pass,
        hash_present=hash_present,
        hash_stable=hash_stable,
        handoff_ready=handoff_ready,
    )
    provenance_metadata = _build_inactive_entry_metadata(
        metadata_type="source_provenance_entry_candidate_metadata",
        status_field="source_provenance_status",
        declared_field="source_provenance_entry_declared",
    )
    methodology_metadata = _build_inactive_entry_metadata(
        metadata_type="methodology_reverse_inference_entry_candidate_metadata",
        status_field="methodology_reverse_inference_status",
        declared_field="methodology_reverse_inference_entry_declared",
    )
    evolution_metadata = _build_inactive_entry_metadata(
        metadata_type="self_evolution_entry_candidate_metadata",
        status_field="self_evolution_status",
        declared_field="self_evolution_entry_declared",
    )
    metadata_valid = _star_source_entry_metadata_valid(metadata)
    provenance_valid = _inactive_entry_metadata_valid(
        provenance_metadata,
        metadata_type="source_provenance_entry_candidate_metadata",
        status_field="source_provenance_status",
        declared_field="source_provenance_entry_declared",
        active_field="source_provenance_active",
    )
    methodology_valid = _inactive_entry_metadata_valid(
        methodology_metadata,
        metadata_type="methodology_reverse_inference_entry_candidate_metadata",
        status_field="methodology_reverse_inference_status",
        declared_field="methodology_reverse_inference_entry_declared",
        active_field="methodology_reverse_inference_active",
    )
    evolution_valid = _inactive_entry_metadata_valid(
        evolution_metadata,
        metadata_type="self_evolution_entry_candidate_metadata",
        status_field="self_evolution_status",
        declared_field="self_evolution_entry_declared",
        active_field="self_evolution_active",
    )
    context: dict[str, Any] = {
        **COMMON_DISABLED_FLAGS,
        "upstream_pass": upstream_pass,
        "hash_present": hash_present,
        "hash_stable": hash_stable,
        "handoff_ready": handoff_ready,
        "metadata_valid": metadata_valid,
        "provenance_valid": provenance_valid,
        "methodology_valid": methodology_valid,
        "evolution_valid": evolution_valid,
        "readiness_names_declared": (
            metadata.get("star_source_entry_readiness_conditions")
            == list(REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES)
        ),
        "evidence_names_declared": (
            metadata.get("required_star_source_entry_evidence")
            == list(REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES)
        ),
        "blocking_names_declared": (
            metadata.get("star_source_entry_blocking_conditions")
            == list(REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES)
        ),
    }
    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES,
    )
    passes = (
        upstream_pass
        and hash_stable
        and handoff_ready
        and metadata_valid
        and provenance_valid
        and methodology_valid
        and evolution_valid
        and context["sections_pass"]
        and context["contracts_pass"]
        and checks_pass
    )
    status = "pass" if passes else "blocked"
    blocking_reasons = _deduplicate(
        [
            *(["Star-Cosmos closure handoff audit must pass"] if not upstream_pass else []),
            *(["Star-Cosmos closure handoff audit hash must be stable"] if not hash_stable else []),
            *(["Star-Cosmos handoff must be ready"] if not handoff_ready else []),
            *(["Star-Source entry metadata must be valid"] if not metadata_valid else []),
            *(["source provenance entry metadata must be valid"] if not provenance_valid else []),
            *(["methodology entry metadata must be valid"] if not methodology_valid else []),
            *(["self-evolution entry metadata must be valid"] if not evolution_valid else []),
            *(
                reason
                for item in (*sections, *contracts, *checks)
                for reason in item["blocking_reasons"]
            ),
        ]
    )
    handoff_status = READY_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_VERSION,
        "schema_version": (
            GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SCHEMA_VERSION
        ),
        "star_source_memory_entry_candidate_type": (
            GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_TYPE
        ),
        "star_source_memory_entry_candidate_status": status,
        "star_source_memory_entry_candidate_stage": (
            STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_STAGE
        ),
        "star_source_memory_entry_candidate_mode": (
            STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_MODE
        ),
        "star_source_memory_mode": STAR_SOURCE_MEMORY_MODE,
        "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_entry_status": LAYER_15_ENTRY_STATUS,
        "source_provenance_status": SOURCE_PROVENANCE_STATUS,
        "methodology_reverse_inference_status": (
            METHODOLOGY_REVERSE_INFERENCE_STATUS
        ),
        "self_evolution_status": SELF_EVOLUTION_STATUS,
        "v6_entry_status": V6_ENTRY_STATUS,
        "v6_handoff_acceptance_status": V6_HANDOFF_ACCEPTANCE_STATUS,
        **COMMON_DISABLED_FLAGS,
        "star_cosmos_closure_handoff_audit_version": _string_or_none(
            upstream.get("version")
        ),
        "star_cosmos_closure_handoff_audit_status": _string_or_none(
            upstream.get("star_cosmos_closure_handoff_audit_status")
        ),
        "star_cosmos_closure_handoff_audit_hash": upstream_hash,
        "star_source_entry_metadata": metadata,
        "source_provenance_entry_metadata": provenance_metadata,
        "methodology_reverse_inference_entry_metadata": methodology_metadata,
        "self_evolution_entry_metadata": evolution_metadata,
        "star_source_entry_sections": sections,
        "star_source_entry_contracts": contracts,
        "star_source_entry_checks": checks,
        "star_source_entry_summary": _build_summary(
            status=status,
            hash_present=hash_present,
            hash_stable=hash_stable,
            handoff_ready=handoff_ready,
            metadata_valid=metadata_valid,
            provenance_valid=provenance_valid,
            methodology_valid=methodology_valid,
            evolution_valid=evolution_valid,
            sections=sections,
            contracts=contracts,
            checks=checks,
        ),
        "handoff_status": handoff_status,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_star_source_memory_entry_candidate_hash"] = (
        _star_source_memory_entry_candidate_hash(result)
    )
    return _detached_json_value(result)


def get_governance_star_source_memory_entry_candidate_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached entry section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_candidate()["star_source_entry_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_star_source_memory_entry_candidate_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached entry contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_candidate()["star_source_entry_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_star_source_memory_entry_candidate_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached entry check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_candidate()["star_source_entry_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_star_source_memory_entry_candidate_section_names() -> list[str]:
    """Return stable entry section names."""

    return list(REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES)


def list_governance_star_source_memory_entry_candidate_contract_names() -> list[str]:
    """Return stable entry contract names."""

    return list(REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES)


def list_governance_star_source_memory_entry_candidate_check_names() -> list[str]:
    """Return stable entry check names."""

    return list(REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES)


def governance_star_source_memory_entry_candidate_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize entry-candidate metadata deterministically."""

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
    return governance_star_source_memory_entry_candidate_to_json(
        build_governance_star_source_memory_entry_candidate()
    )


def _cached_candidate() -> dict[str, Any]:
    return json.loads(_cached_candidate_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_star_cosmos_closure_handoff_audit()
    )
    second = _detached_json_value(
        build_governance_star_cosmos_closure_handoff_audit()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _upstream_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_upstream_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_star_source_entry_metadata(
    *,
    upstream_pass: bool,
    hash_present: bool,
    hash_stable: bool,
    handoff_ready: bool,
) -> dict[str, Any]:
    ready = upstream_pass and hash_present and hash_stable and handoff_ready
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "star_source_entry_metadata_type": (
                "layer_15_star_source_memory_entry_candidate_metadata"
            ),
            "star_source_entry_metadata_mode": STAR_SOURCE_MEMORY_MODE,
            "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
            "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
            "layer_15_entry_status": LAYER_15_ENTRY_STATUS,
            "source_provenance_status": SOURCE_PROVENANCE_STATUS,
            "methodology_reverse_inference_status": (
                METHODOLOGY_REVERSE_INFERENCE_STATUS
            ),
            "self_evolution_status": SELF_EVOLUTION_STATUS,
            "v6_entry_status": V6_ENTRY_STATUS,
            "v6_handoff_acceptance_status": V6_HANDOFF_ACCEPTANCE_STATUS,
            "star_cosmos_closure_handoff_audit_pass_required": True,
            "star_cosmos_closure_handoff_audit_hash_required": True,
            "star_cosmos_closure_handoff_audit_hash_present": hash_present,
            "star_cosmos_closure_handoff_audit_hash_stable": hash_stable,
            "star_cosmos_handoff_ready": handoff_ready,
            "star_source_entry_candidate_declared": True,
            "star_source_entry_candidate_activated": False,
            "source_provenance_entry_declared": True,
            "methodology_reverse_inference_entry_declared": True,
            "self_evolution_entry_declared": True,
            "required_star_source_entry_evidence": list(
                REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES
            ),
            "star_source_entry_blocking_conditions": list(
                REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES
            ),
            "star_source_entry_readiness_conditions": list(
                REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES
            ),
            "star_source_entry_next_stage": STAR_SOURCE_ENTRY_NEXT_STAGE,
            "star_source_entry_next_stage_title": (
                STAR_SOURCE_ENTRY_NEXT_STAGE_TITLE
            ),
            "star_source_entry_handoff_status": (
                READY_HANDOFF_STATUS if ready else BLOCKED_HANDOFF_STATUS
            ),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_inactive_entry_metadata(
    *,
    metadata_type: str,
    status_field: str,
    declared_field: str,
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "entry_metadata_type": metadata_type,
            "entry_metadata_mode": "metadata_only",
            "entry_status": "entry_candidate_only",
            status_field: "not_active",
            declared_field: True,
            "runtime_created": False,
            "live_output_included": False,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions = {
        "star_cosmos_closure_handoff_input_section": (
            context["upstream_pass"]
            and context["hash_present"]
            and context["hash_stable"]
            and context["handoff_ready"]
        ),
        "star_source_entry_metadata_section": context["metadata_valid"],
        "source_provenance_entry_metadata_section": context["provenance_valid"],
        "methodology_reverse_inference_entry_metadata_section": context[
            "methodology_valid"
        ],
        "self_evolution_entry_metadata_section": context["evolution_valid"],
        "layer_15_entry_candidate_only_section": not context["layer_15_active"],
        "star_source_inactive_section": not context["star_source_memory_active"],
        "source_graph_disabled_section": (
            not context["source_graph_created"]
            and not context["source_graph_mutation_enabled"]
        ),
        "source_provenance_engine_disabled_section": (
            not context["source_provenance_engine_created"]
            and not context["source_provenance_active"]
        ),
        "methodology_reverse_inference_engine_disabled_section": (
            not context["methodology_reverse_inference_engine_created"]
            and not context["methodology_reverse_inference_active"]
        ),
        "self_evolution_engine_disabled_section": (
            not context["self_evolution_engine_created"]
            and not context["self_evolution_active"]
        ),
        "autonomous_rule_mutation_disabled_section": (
            not context["autonomous_rule_mutation_enabled"]
        ),
        "governance_policy_mutation_disabled_section": (
            not context["governance_policy_mutation_enabled"]
        ),
        "memory_graph_mutation_disabled_section": (
            not context["memory_graph_mutation_enabled"]
        ),
        "external_network_write_disabled_section": (
            not context["external_calls_enabled"]
            and not context["network_calls_enabled"]
            and not context["durable_writes_enabled"]
            and not context["filesystem_writes_enabled"]
            and not context["database_writes_enabled"]
        ),
        "adapter_manifest_execution_disabled_section": (
            not context["execution_adapter_invoked"]
            and not context["adapter_dispatched"]
            and not context["manifest_dispatched"]
            and not context["manifest_executed"]
            and not context["dry_run_plan_executed"]
        ),
        "operation_ledger_write_disabled_section": (
            not context["operation_ledger_writes_enabled"]
            and not context["operation_ledger_entry_created"]
            and not context["operation_ledger_entry_written"]
            and not context["operation_ledger_proposal_persisted"]
            and not context["operation_ledger_proposal_submitted"]
            and not context["operation_ledger_proposal_dispatched"]
        ),
        "approval_authorization_disabled_section": (
            not context["real_approval_record_written"]
            and not context["approval_notification_sent"]
            and not context["execution_authorization_issued"]
            and not context["authorization_token_created"]
            and not context["authorization_grant_created"]
        ),
        "star_source_active_entry_disabled_section": (
            not context["star_source_active_entry_claimed"]
        ),
        "next_stage_source_constitution_registry_section": (
            context["metadata_valid"]
        ),
    }
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "star_source_entry_candidate_only_contract": True,
        "star_source_entry_metadata_only_contract": context["metadata_valid"],
        "star_cosmos_closure_handoff_audit_pass_contract": context[
            "upstream_pass"
        ],
        "star_cosmos_closure_handoff_audit_hash_present_contract": context[
            "hash_present"
        ],
        "star_cosmos_closure_handoff_audit_hash_stable_contract": context[
            "hash_stable"
        ],
        "star_cosmos_handoff_ready_contract": context["handoff_ready"],
    }
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        conditions[contract_name] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "star_source_entry_candidate_stage_check": True,
        "star_source_entry_candidate_only_mode_check": True,
        "star_source_metadata_only_check": context["metadata_valid"],
        "star_cosmos_closure_handoff_audit_pass_check": context["upstream_pass"],
        "star_cosmos_closure_handoff_audit_hash_present_check": context[
            "hash_present"
        ],
        "star_cosmos_closure_handoff_audit_hash_stable_check": context[
            "hash_stable"
        ],
        "star_cosmos_handoff_ready_check": context["handoff_ready"],
        "star_source_entry_readiness_conditions_declared_check": context[
            "readiness_names_declared"
        ],
        "star_source_entry_evidence_requirements_declared_check": context[
            "evidence_names_declared"
        ],
        "star_source_entry_blocking_conditions_declared_check": context[
            "blocking_names_declared"
        ],
        "star_source_entry_sections_complete_check": context[
            "sections_complete"
        ],
        "star_source_entry_sections_pass_check": context["sections_pass"],
        "star_source_entry_contracts_pass_check": context["contracts_pass"],
        "deterministic_star_source_memory_entry_candidate_hash_check": True,
        "ready_for_source_constitution_registry_design_check": (
            context["metadata_valid"]
            and context["provenance_valid"]
            and context["methodology_valid"]
            and context["evolution_valid"]
            and context["sections_pass"]
            and context["contracts_pass"]
        ),
    }
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        check_name = contract_name.removesuffix("_contract") + "_check"
        conditions[check_name] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES
    ]


def _build_summary(
    *,
    status: str,
    hash_present: bool,
    hash_stable: bool,
    handoff_ready: bool,
    metadata_valid: bool,
    provenance_valid: bool,
    methodology_valid: bool,
    evolution_valid: bool,
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "star_source_memory_entry_candidate_summary",
            "star_source_memory_entry_candidate_status": status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "star_cosmos_closure_handoff_audit_hash_present": hash_present,
            "star_cosmos_closure_handoff_audit_hash_stable": hash_stable,
            "star_cosmos_handoff_ready": handoff_ready,
            "star_source_entry_metadata_valid": metadata_valid,
            "source_provenance_entry_metadata_valid": provenance_valid,
            "methodology_reverse_inference_entry_metadata_valid": (
                methodology_valid
            ),
            "self_evolution_entry_metadata_valid": evolution_valid,
            "star_source_entry_section_count": len(sections),
            "star_source_entry_sections_pass": _items_pass(
                sections,
                "section_status",
                "section_name",
                REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
            ),
            "star_source_entry_contract_count": len(contracts),
            "star_source_entry_contracts_pass": _items_pass(
                contracts,
                "contract_status",
                "contract_name",
                REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES,
            ),
            "star_source_entry_check_count": len(checks),
            "star_source_entry_checks_pass": _items_pass(
                checks,
                "check_status",
                "check_name",
                REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES,
            ),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": name.removesuffix("_section") + "_boundary",
            "section_status": "pass" if condition else "blocked",
            "source_star_cosmos_closure_handoff_audit_refs": list(_UPSTREAM_REFS),
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "star_source_entry_notes": [
                "Deterministic local entry-candidate metadata only."
            ],
            "blocking_reasons": (
                [] if condition else ["Star-Source entry section must pass"]
            ),
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": name.removesuffix("_contract") + "_boundary_contract",
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "contract_status": "pass" if condition else "blocked",
            "blocking_reasons": (
                [] if condition else ["Star-Source entry contract must pass"]
            ),
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _check_from_condition(name: str, condition: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "check_name": name,
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "check_status": "pass" if condition else "blocked",
            "blocking_reasons": (
                [] if condition else ["Star-Source entry check must pass"]
            ),
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    result = _section_from_condition(name, False)
    result["section_type"] = "unknown_star_source_entry_section"
    result["source_star_cosmos_closure_handoff_audit_refs"] = []
    result["observed"]["requested_section_name"] = name
    result["blocking_reasons"] = [
        "Star-Source entry section name is not recognized"
    ]
    return _detached_json_value(result)


def _unknown_contract(name: str) -> dict[str, Any]:
    result = _contract_from_condition(name, False)
    result["contract_type"] = "unknown_star_source_entry_contract"
    result["observed"]["requested_contract_name"] = name
    result["blocking_reasons"] = [
        "Star-Source entry contract name is not recognized"
    ]
    return _detached_json_value(result)


def _unknown_check(name: str) -> dict[str, Any]:
    result = _check_from_condition(name, False)
    result["observed"]["requested_check_name"] = name
    result["blocking_reasons"] = [
        "Star-Source entry check name is not recognized"
    ]
    return _detached_json_value(result)


def _star_source_memory_entry_candidate_hash(
    result: Mapping[str, Any],
) -> str:
    projection = {
        field: result[field]
        for field in _HASH_FIELDS
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


def _upstream_hash(value: Mapping[str, Any]) -> str | None:
    return _string_or_none(
        value.get("deterministic_star_cosmos_closure_handoff_audit_hash")
    )


def _upstream_passes(value: Mapping[str, Any]) -> bool:
    return (
        value.get("version")
        == GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_VERSION
        and value.get("star_cosmos_closure_handoff_audit_status") == "pass"
        and value.get("handoff_status") == UPSTREAM_READY_HANDOFF_STATUS
        and _is_sha256(_upstream_hash(value))
        and _all_safety_boundaries_false(value)
    )


def _star_source_entry_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("star_source_entry_metadata_type")
        == "layer_15_star_source_memory_entry_candidate_metadata"
        and metadata.get("star_source_entry_metadata_mode") == "metadata_only"
        and metadata.get("star_source_entry_status") == "entry_candidate_only"
        and metadata.get("star_source_memory_active_status") == "not_active"
        and metadata.get("layer_15_entry_status") == "entry_candidate_only"
        and metadata.get("source_provenance_status") == "not_active"
        and metadata.get("methodology_reverse_inference_status") == "not_active"
        and metadata.get("self_evolution_status") == "not_active"
        and metadata.get("v6_entry_status") == "entry_candidate_only"
        and metadata.get("v6_handoff_acceptance_status")
        == "accepted_as_metadata_only"
        and metadata.get("star_cosmos_closure_handoff_audit_pass_required")
        is True
        and metadata.get("star_cosmos_closure_handoff_audit_hash_required")
        is True
        and metadata.get("star_cosmos_closure_handoff_audit_hash_present")
        is True
        and metadata.get("star_cosmos_closure_handoff_audit_hash_stable")
        is True
        and metadata.get("star_cosmos_handoff_ready") is True
        and metadata.get("star_source_entry_candidate_declared") is True
        and metadata.get("star_source_entry_candidate_activated") is False
        and metadata.get("source_provenance_entry_declared") is True
        and metadata.get("methodology_reverse_inference_entry_declared") is True
        and metadata.get("self_evolution_entry_declared") is True
        and metadata.get("required_star_source_entry_evidence")
        == list(REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("star_source_entry_blocking_conditions")
        == list(REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES)
        and metadata.get("star_source_entry_readiness_conditions")
        == list(REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES)
        and metadata.get("star_source_entry_next_stage")
        == STAR_SOURCE_ENTRY_NEXT_STAGE
        and metadata.get("star_source_entry_next_stage_title")
        == STAR_SOURCE_ENTRY_NEXT_STAGE_TITLE
        and metadata.get("star_source_entry_handoff_status")
        == READY_HANDOFF_STATUS
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _inactive_entry_metadata_valid(
    metadata: Mapping[str, Any],
    *,
    metadata_type: str,
    status_field: str,
    declared_field: str,
    active_field: str,
) -> bool:
    return (
        metadata.get("entry_metadata_type") == metadata_type
        and metadata.get("entry_metadata_mode") == "metadata_only"
        and metadata.get("entry_status") == "entry_candidate_only"
        and metadata.get(status_field) == "not_active"
        and metadata.get(declared_field) is True
        and metadata.get(active_field) is False
        and metadata.get("runtime_created") is False
        and metadata.get("live_output_included") is False
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _items_pass(
    items: Sequence[Mapping[str, Any]],
    status_field: str,
    name_field: str,
    expected_names: Sequence[str],
) -> bool:
    return _names_match(items, name_field, expected_names) and all(
        item.get(status_field) == "pass" for item in items
    )


def _names_match(
    items: Sequence[Mapping[str, Any]],
    name_field: str,
    expected_names: Sequence[str],
) -> bool:
    return [item.get(name_field) for item in items] == list(expected_names)


def _all_common_disabled_flags_false(value: Mapping[str, Any]) -> bool:
    return all(value.get(field_name) is False for field_name in COMMON_DISABLED_FLAGS)


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
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


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
