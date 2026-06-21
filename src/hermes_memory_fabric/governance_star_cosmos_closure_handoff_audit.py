"""Deterministic Layer 14 Star-Cosmos closure handoff audit metadata."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_post_sandbox_review_boundary import (
    COMMON_DISABLED_FLAGS as POST_SANDBOX_REVIEW_DISABLED_FLAGS,
    build_governance_post_sandbox_review_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_VERSION = "6.3.0"
GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SCHEMA_VERSION = "6.3.0"
GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_TYPE = (
    "governance_star_cosmos_closure_handoff_audit"
)
GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_HASH_ALGORITHM = "sha256"
STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_STAGE = (
    "v5.13_star_cosmos_closure_handoff_audit"
)
STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_MODE = (
    "star_cosmos_closure_handoff_audit_only"
)
STAR_COSMOS_CLOSURE_MODE = "metadata_only"
STAR_COSMOS_CLOSURE_STATUS = "closure_candidate_only"
LAYER_14_CLOSURE_STATUS = "closure_candidate_only"
V6_HANDOFF_STATUS = "ready_for_star_source_entry_candidate_design"
STAR_SOURCE_ENTRY_STATUS = "not_entered"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
STAR_COSMOS_ENTRY_STATUS = "candidate_only"

READY_HANDOFF_STATUS = "ready_for_v6_star_source_entry_candidate_design"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "star_source_memory_active": False,
    "v6_started": False,
    "layer_15_started": False,
    "star_source_entry_candidate_activated": False,
    "actual_layer_14_closure_performed": False,
    "closure_handoff_audit_executed": False,
    "closure_record_written": False,
    "closure_audit_log_written": False,
    "closure_evidence_persisted": False,
    "source_provenance_engine_created": False,
    "source_evolution_engine_created": False,
    "source_graph_mutation_enabled": False,
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
    "audit_evidence_persisted": False,
    "failure_handling_executed": False,
    "remediation_executed": False,
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

REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES = (
    "post_sandbox_review_boundary_pass",
    "post_sandbox_review_boundary_hash_present",
    "post_sandbox_review_boundary_hash_stable",
    "v5_layer_stack_inventory_complete",
    "v5_layer_stack_metadata_only",
    "layer_14_closure_candidate_only_declared",
    "v6_handoff_metadata_only",
    "v6_entry_candidate_design_allowed",
    "v6_entry_candidate_not_started",
    "layer_15_not_started",
    "star_source_memory_not_active",
    "star_cosmos_memory_not_active",
    "actual_layer_14_closure_not_performed",
    "closure_handoff_audit_not_executed",
    "closure_record_not_written",
    "closure_audit_log_not_written",
    "closure_evidence_not_persisted",
    "source_provenance_engine_not_created",
    "source_evolution_engine_not_created",
    "source_graph_mutation_not_enabled",
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
    "hermes_not_connected",
    "codex_not_connected",
    "openclaw_not_connected",
    "github_not_connected",
    "tool_routing_not_configured",
    "command_routing_not_configured",
    "system_handoff_not_completed",
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
    "no_star_source_active_entry",
)

REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES = (
    "post_sandbox_review_boundary_pass_evidence",
    "deterministic_post_sandbox_review_boundary_hash_evidence",
    "v5_layer_stack_inventory_evidence",
    "star_cosmos_closure_metadata_evidence",
    "v6_handoff_metadata_evidence",
    "layer_14_closure_candidate_only_evidence",
    "v6_entry_candidate_not_started_evidence",
    "layer_15_not_started_evidence",
    "star_source_memory_not_active_evidence",
    "star_cosmos_memory_not_active_evidence",
    "actual_layer_14_closure_not_performed_evidence",
    "closure_handoff_audit_not_executed_evidence",
    "closure_record_not_written_evidence",
    "closure_audit_log_not_written_evidence",
    "closure_evidence_not_persisted_evidence",
    "source_provenance_engine_not_created_evidence",
    "source_evolution_engine_not_created_evidence",
    "source_graph_mutation_not_enabled_evidence",
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
    "no_star_source_active_entry_evidence",
)

REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES = (
    "post_sandbox_review_boundary_blocked",
    "missing_post_sandbox_review_boundary_hash",
    "unstable_post_sandbox_review_boundary_hash",
    "v5_layer_stack_inventory_incomplete",
    "star_cosmos_closure_metadata_invalid",
    "layer_14_closure_candidate_only_missing",
    "v6_handoff_metadata_invalid",
    "v6_entry_candidate_started",
    "layer_15_started",
    "star_source_memory_active",
    "star_cosmos_memory_active",
    "actual_layer_14_closure_performed",
    "closure_handoff_audit_executed",
    "closure_record_written",
    "closure_audit_log_written",
    "closure_evidence_persisted",
    "source_provenance_engine_created",
    "source_evolution_engine_created",
    "source_graph_mutation_enabled",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_result_available",
    "actual_post_sandbox_review_performed",
    "rollback_triggered",
    "quarantine_triggered",
    "incident_triggered",
    "audit_log_written",
    "audit_evidence_persisted",
    "failure_handling_executed",
    "remediation_executed",
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
    "star_source_active_entry_claimed",
)

REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES = (
    "post_sandbox_review_boundary_input_section",
    "v5_layer_stack_inventory_section",
    "star_cosmos_closure_metadata_section",
    "v6_handoff_readiness_section",
    "layer_14_closure_candidate_only_section",
    "v6_entry_disabled_section",
    "layer_15_disabled_section",
    "star_source_inactive_section",
    "actual_closure_disabled_section",
    "closure_record_write_disabled_section",
    "closure_audit_log_write_disabled_section",
    "source_provenance_engine_disabled_section",
    "source_evolution_engine_disabled_section",
    "source_graph_mutation_disabled_section",
    "sandbox_entry_disabled_section",
    "sandbox_runtime_disabled_section",
    "sandbox_execution_disabled_section",
    "post_sandbox_review_disabled_section",
    "rollback_quarantine_incident_disabled_section",
    "external_network_write_disabled_section",
    "tool_command_routing_disabled_section",
    "adapter_manifest_execution_disabled_section",
    "operation_ledger_write_disabled_section",
    "approval_authorization_disabled_section",
    "star_cosmos_candidate_only_section",
    "star_source_entry_candidate_section",
)
REQUIRED_STAR_COSMOS_CLOSURE_SECTION_NAMES = (
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES
)

REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES = (
    "star_cosmos_closure_handoff_audit_only_contract",
    "star_cosmos_closure_metadata_only_contract",
    "post_sandbox_review_boundary_pass_contract",
    "post_sandbox_review_boundary_hash_present_contract",
    "post_sandbox_review_boundary_hash_stable_contract",
    "v5_layer_stack_inventory_complete_contract",
    "star_cosmos_closure_readiness_conditions_declared_contract",
    "star_cosmos_closure_evidence_requirements_declared_contract",
    "star_cosmos_closure_blocking_conditions_declared_contract",
    "star_cosmos_closure_sections_complete_contract",
    "star_cosmos_closure_sections_pass_contract",
    "closure_candidate_only_boundary_contract",
    "v6_handoff_metadata_only_contract",
    "v6_entry_candidate_not_started_contract",
    "layer_15_not_started_contract",
    "star_source_memory_not_active_contract",
    "star_cosmos_memory_not_active_contract",
    "actual_layer_14_closure_not_performed_contract",
    "closure_handoff_audit_not_executed_contract",
    "closure_record_not_written_contract",
    "closure_audit_log_not_written_contract",
    "closure_evidence_not_persisted_contract",
    "source_provenance_engine_not_created_contract",
    "source_evolution_engine_not_created_contract",
    "source_graph_mutation_not_enabled_contract",
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
    "no_star_cosmos_active_entry_contract",
    "no_star_source_active_entry_contract",
)
REQUIRED_STAR_COSMOS_CLOSURE_CONTRACT_NAMES = (
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES
)

REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES = (
    "star_cosmos_closure_handoff_audit_stage_check",
    "star_cosmos_closure_handoff_audit_only_mode_check",
    "star_cosmos_closure_metadata_only_check",
    "post_sandbox_review_boundary_pass_check",
    "post_sandbox_review_boundary_hash_present_check",
    "post_sandbox_review_boundary_hash_stable_check",
    "v5_layer_stack_inventory_complete_check",
    "star_cosmos_closure_readiness_conditions_declared_check",
    "star_cosmos_closure_evidence_requirements_declared_check",
    "star_cosmos_closure_blocking_conditions_declared_check",
    "star_cosmos_closure_sections_complete_check",
    "star_cosmos_closure_sections_pass_check",
    "star_cosmos_closure_contracts_pass_check",
    "closure_candidate_only_boundary_check",
    "v6_handoff_metadata_only_check",
    "v6_entry_candidate_not_started_check",
    "layer_15_not_started_check",
    "star_source_memory_not_active_check",
    "star_cosmos_memory_not_active_check",
    "actual_layer_14_closure_not_performed_check",
    "closure_handoff_audit_not_executed_check",
    "closure_record_not_written_check",
    "closure_audit_log_not_written_check",
    "closure_evidence_not_persisted_check",
    "source_provenance_engine_not_created_check",
    "source_evolution_engine_not_created_check",
    "source_graph_mutation_not_enabled_check",
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
    "no_star_cosmos_active_entry_check",
    "no_star_source_active_entry_check",
    "deterministic_star_cosmos_closure_handoff_audit_hash_check",
    "ready_for_v6_entry_candidate_design_check",
)
REQUIRED_STAR_COSMOS_CLOSURE_CHECK_NAMES = (
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES
)

_V5_LAYER_STACK_SPECS = (
    (
        "v5.0.0_execution_adapter_boundary_candidate",
        "v5.0.0",
        "Execution adapter boundary candidate metadata.",
    ),
    (
        "v5.1.0_execution_adapter_declaration_schema_registry_candidate",
        "v5.1.0",
        "Execution adapter declaration schema registry candidate metadata.",
    ),
    (
        "v5.2.0_execution_adapter_manifest_dry_run_design_candidate",
        "v5.2.0",
        "Execution adapter manifest dry-run design candidate metadata.",
    ),
    (
        "v5.3.0_execution_adapter_manifest_fixture_pack_candidate",
        "v5.3.0",
        "Execution adapter manifest fixture pack candidate metadata.",
    ),
    (
        "v5.4.0_execution_adapter_manifest_validation_matrix_candidate",
        "v5.4.0",
        "Execution adapter manifest validation matrix candidate metadata.",
    ),
    (
        "v5.5.0_execution_adapter_manifest_policy_gate_candidate",
        "v5.5.0",
        "Execution adapter manifest policy gate candidate metadata.",
    ),
    (
        "v5.6.0_execution_adapter_manifest_approval_gate_candidate",
        "v5.6.0",
        "Execution adapter manifest approval gate candidate metadata.",
    ),
    (
        "v5.7.0_execution_adapter_manifest_authorization_gate_candidate",
        "v5.7.0",
        "Execution adapter manifest authorization gate candidate metadata.",
    ),
    (
        "v5.8.0_adapter_handoff_audit",
        "v5.8.0",
        "Execution adapter handoff audit metadata.",
    ),
    (
        "v5.9.0_operation_ledger_proposal_boundary",
        "v5.9.0",
        "Operation ledger proposal boundary metadata.",
    ),
    (
        "v5.10.0_cross_system_coordination_boundary",
        "v5.10.0",
        "Cross-system coordination boundary metadata.",
    ),
    (
        "v5.11.0_controlled_adapter_sandbox_candidate",
        "v5.11.0",
        "Controlled adapter sandbox candidate metadata.",
    ),
    (
        "v5.12.0_post_sandbox_review_boundary",
        "v5.12.0",
        "Post-sandbox review boundary metadata.",
    ),
)

_POST_SANDBOX_REVIEW_BOUNDARY_REFS = (
    "post_sandbox_review_boundary_status",
    "deterministic_post_sandbox_review_boundary_hash",
    "post_sandbox_review_metadata",
)

_STAR_COSMOS_CLOSURE_HASH_FIELDS = (
    "version",
    "schema_version",
    "star_cosmos_closure_handoff_audit_type",
    "star_cosmos_closure_handoff_audit_status",
    "star_cosmos_closure_handoff_audit_stage",
    "star_cosmos_closure_handoff_audit_mode",
    "star_cosmos_closure_mode",
    "star_cosmos_closure_status",
    "layer_14_closure_status",
    "v6_handoff_status",
    "star_source_entry_status",
    "star_source_memory_active_status",
    "star_cosmos_entry_status",
    "star_source_entry_candidate_declared",
    "closure_handoff_audit_declared",
    "closure_handoff_audit_metadata_only",
    *COMMON_DISABLED_FLAGS,
    "post_sandbox_review_boundary_version",
    "post_sandbox_review_boundary_status",
    "post_sandbox_review_boundary_hash",
    "v5_layer_stack_closure_inventory",
    "star_cosmos_closure_metadata",
    "v6_handoff_readiness_metadata",
    "star_cosmos_closure_sections",
    "star_cosmos_closure_contracts",
    "star_cosmos_closure_checks",
    "star_cosmos_closure_summary",
    "star_cosmos_closure_handoff_status",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_STAR_COSMOS_CLOSURE_HASH_FIELDS),
    "input_shape": "sanitized Layer 14 closure handoff audit projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_post_sandbox_review_boundary_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_DISABLED_CONTRACT_FIELDS = {
    "v6_entry_candidate_not_started_contract": "v6_started",
    "layer_15_not_started_contract": "layer_15_started",
    "star_source_memory_not_active_contract": "star_source_memory_active",
    "star_cosmos_memory_not_active_contract": "star_cosmos_memory_active",
    "actual_layer_14_closure_not_performed_contract": (
        "actual_layer_14_closure_performed"
    ),
    "closure_handoff_audit_not_executed_contract": (
        "closure_handoff_audit_executed"
    ),
    "closure_record_not_written_contract": "closure_record_written",
    "closure_audit_log_not_written_contract": "closure_audit_log_written",
    "closure_evidence_not_persisted_contract": "closure_evidence_persisted",
    "source_provenance_engine_not_created_contract": (
        "source_provenance_engine_created"
    ),
    "source_evolution_engine_not_created_contract": (
        "source_evolution_engine_created"
    ),
    "source_graph_mutation_not_enabled_contract": (
        "source_graph_mutation_enabled"
    ),
    "controlled_adapter_sandbox_not_started_contract": (
        "controlled_adapter_sandbox_started"
    ),
    "adapter_sandbox_not_entered_contract": "adapter_sandbox_entered",
    "sandbox_runtime_not_created_contract": "sandbox_runtime_created",
    "sandbox_execution_not_enabled_contract": "sandbox_execution_enabled",
    "sandbox_result_not_available_contract": "sandbox_result_available",
    "actual_post_sandbox_review_not_performed_contract": (
        "actual_post_sandbox_review_performed"
    ),
    "rollback_not_triggered_contract": "rollback_triggered",
    "quarantine_not_triggered_contract": "quarantine_triggered",
    "incident_not_triggered_contract": "incident_triggered",
    "audit_log_not_written_contract": "audit_log_written",
    "audit_evidence_not_persisted_contract": "audit_evidence_persisted",
    "failure_handling_not_executed_contract": "failure_handling_executed",
    "remediation_not_executed_contract": "remediation_executed",
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
    "no_star_cosmos_active_entry_contract": "star_cosmos_memory_active",
    "no_star_source_active_entry_contract": "star_source_memory_active",
}


def build_governance_star_cosmos_closure_handoff_audit() -> dict[str, Any]:
    """Build deterministic Layer-14-closure-handoff-audit-only metadata."""

    upstream, repeated_upstream = _post_sandbox_review_boundary_pair()
    upstream_hash = _post_sandbox_review_boundary_hash(upstream)
    repeated_hash = _post_sandbox_review_boundary_hash(repeated_upstream)
    upstream_pass = _post_sandbox_review_boundary_passes(upstream)
    hash_present = _is_sha256(upstream_hash)
    hash_stable = hash_present and upstream_hash == repeated_hash
    inventory = _build_v5_layer_stack_closure_inventory()
    inventory_complete = _inventory_valid(inventory)
    metadata = _build_star_cosmos_closure_metadata(
        upstream_pass=upstream_pass,
        hash_present=hash_present,
        hash_stable=hash_stable,
        inventory_complete=inventory_complete,
    )
    metadata_valid = _star_cosmos_closure_metadata_valid(metadata)
    readiness = _build_v6_handoff_readiness_metadata(
        metadata,
        inventory_complete=inventory_complete,
    )
    context: dict[str, Any] = {
        **COMMON_DISABLED_FLAGS,
        "upstream_pass": upstream_pass,
        "hash_present": hash_present,
        "hash_stable": hash_stable,
        "inventory_complete": inventory_complete,
        "metadata_valid": metadata_valid,
        "readiness_valid": _v6_handoff_readiness_metadata_valid(readiness),
        "readiness_names_declared": (
            metadata.get("star_cosmos_closure_readiness_conditions")
            == list(REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES)
        ),
        "evidence_names_declared": (
            metadata.get("required_star_cosmos_closure_evidence")
            == list(REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES)
        ),
        "blocking_names_declared": (
            metadata.get("star_cosmos_closure_blocking_conditions")
            == list(REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES)
        ),
    }
    sections = _build_star_cosmos_closure_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
    )
    contracts = _build_star_cosmos_closure_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES,
    )
    checks = _build_star_cosmos_closure_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES,
    )
    audit_passes = (
        upstream_pass
        and hash_stable
        and inventory_complete
        and metadata_valid
        and context["readiness_valid"]
        and context["sections_pass"]
        and context["contracts_pass"]
        and checks_pass
    )
    audit_status = "pass" if audit_passes else "blocked"
    blocking_reasons = _deduplicate(
        [
            *(["post-sandbox review boundary must pass"] if not upstream_pass else []),
            *(["post-sandbox review boundary hash must be stable"] if not hash_stable else []),
            *(["v5 layer stack inventory must be complete"] if not inventory_complete else []),
            *(["Star-Cosmos closure metadata must be valid"] if not metadata_valid else []),
            *(
                ["v6 handoff readiness metadata must be valid"]
                if not context["readiness_valid"]
                else []
            ),
            *(
                reason
                for item in (*sections, *contracts, *checks)
                for reason in item["blocking_reasons"]
            ),
        ]
    )
    handoff_status = READY_HANDOFF_STATUS if audit_passes else BLOCKED_HANDOFF_STATUS
    closure_handoff_status = (
        READY_HANDOFF_STATUS if metadata_valid else BLOCKED_HANDOFF_STATUS
    )
    v6_handoff_status = V6_HANDOFF_STATUS if metadata_valid else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_VERSION,
        "schema_version": (
            GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SCHEMA_VERSION
        ),
        "star_cosmos_closure_handoff_audit_type": (
            GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_TYPE
        ),
        "star_cosmos_closure_handoff_audit_status": audit_status,
        "star_cosmos_closure_handoff_audit_stage": (
            STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_STAGE
        ),
        "star_cosmos_closure_handoff_audit_mode": (
            STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_MODE
        ),
        "star_cosmos_closure_mode": STAR_COSMOS_CLOSURE_MODE,
        "star_cosmos_closure_status": STAR_COSMOS_CLOSURE_STATUS,
        "layer_14_closure_status": LAYER_14_CLOSURE_STATUS,
        "v6_handoff_status": v6_handoff_status,
        "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "star_source_entry_candidate_declared": True,
        "closure_handoff_audit_declared": True,
        "closure_handoff_audit_metadata_only": True,
        **COMMON_DISABLED_FLAGS,
        "post_sandbox_review_boundary_version": _string_or_none(
            upstream.get("version")
        ),
        "post_sandbox_review_boundary_status": _string_or_none(
            upstream.get("post_sandbox_review_boundary_status")
        ),
        "post_sandbox_review_boundary_hash": upstream_hash,
        "v5_layer_stack_closure_inventory": inventory,
        "star_cosmos_closure_metadata": metadata,
        "v6_handoff_readiness_metadata": readiness,
        "star_cosmos_closure_sections": sections,
        "star_cosmos_closure_contracts": contracts,
        "star_cosmos_closure_checks": checks,
        "star_cosmos_closure_summary": _build_star_cosmos_closure_summary(
            audit_status,
            upstream_hash=upstream_hash,
            hash_stable=hash_stable,
            inventory=inventory,
            metadata_valid=metadata_valid,
            readiness_valid=context["readiness_valid"],
            sections=sections,
            contracts=contracts,
            checks=checks,
        ),
        "star_cosmos_closure_handoff_status": closure_handoff_status,
        "handoff_status": handoff_status,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_star_cosmos_closure_handoff_audit_hash"] = (
        _star_cosmos_closure_handoff_audit_hash(result)
    )
    return _detached_json_value(result)


def get_governance_star_cosmos_closure_handoff_audit_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached closure section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_audit()["star_cosmos_closure_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_star_cosmos_closure_handoff_audit_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached closure contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_audit()["star_cosmos_closure_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_star_cosmos_closure_handoff_audit_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached closure check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_audit()["star_cosmos_closure_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_star_cosmos_closure_handoff_audit_section_names() -> list[str]:
    """Return stable closure section names."""

    return list(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES)


def list_governance_star_cosmos_closure_handoff_audit_contract_names() -> list[str]:
    """Return stable closure contract names."""

    return list(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES)


def list_governance_star_cosmos_closure_handoff_audit_check_names() -> list[str]:
    """Return stable closure check names."""

    return list(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES)


def governance_star_cosmos_closure_handoff_audit_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize closure handoff audit metadata deterministically."""

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
def _cached_audit_payload() -> str:
    return governance_star_cosmos_closure_handoff_audit_to_json(
        build_governance_star_cosmos_closure_handoff_audit()
    )


def _cached_audit() -> dict[str, Any]:
    return json.loads(_cached_audit_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(build_governance_post_sandbox_review_boundary())
    second = _detached_json_value(build_governance_post_sandbox_review_boundary())
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _post_sandbox_review_boundary_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_upstream_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_v5_layer_stack_closure_inventory() -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    for name, version_label, notes in _V5_LAYER_STACK_SPECS:
        safety_boundaries = dict(SAFETY_BOUNDARIES)
        inventory.append(
            {
                "layer_stage_name": name,
                "layer_stage_version_label": version_label,
                "layer_stage_status": "sealed_metadata_boundary",
                "layer_stage_execution_status": "no_execution",
                "layer_stage_closure_status": (
                    "included_in_layer_14_closure_candidate"
                ),
                "layer_stage_notes": notes,
                "safety_boundaries": safety_boundaries,
                **COMMON_DISABLED_FLAGS,
                **safety_boundaries,
            }
        )
    return _detached_json_value(inventory)


def _build_star_cosmos_closure_metadata(
    *,
    upstream_pass: bool,
    hash_present: bool,
    hash_stable: bool,
    inventory_complete: bool,
) -> dict[str, Any]:
    ready = upstream_pass and hash_stable and inventory_complete
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "star_cosmos_closure_metadata_type": (
                "layer_14_star_cosmos_closure_handoff_audit_metadata"
            ),
            "star_cosmos_closure_metadata_mode": STAR_COSMOS_CLOSURE_MODE,
            "star_cosmos_closure_status": STAR_COSMOS_CLOSURE_STATUS,
            "layer_14_closure_status": LAYER_14_CLOSURE_STATUS,
            "v6_handoff_status": (
                V6_HANDOFF_STATUS if ready else BLOCKED_HANDOFF_STATUS
            ),
            "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
            "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
            "closure_handoff_audit_required": True,
            "closure_handoff_audit_declared": True,
            "closure_handoff_audit_metadata_only": True,
            "post_sandbox_review_boundary_pass_required": True,
            "post_sandbox_review_boundary_hash_required": True,
            "post_sandbox_review_boundary_hash_present": hash_present,
            "post_sandbox_review_boundary_hash_stable": hash_stable,
            "v5_layer_stack_complete": inventory_complete,
            "v5_layer_stack_closure_candidate_only": True,
            "v6_entry_candidate_design_allowed": ready,
            "v6_entry_candidate_started": False,
            "star_cosmos_closure_readiness_conditions": list(
                REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES
            ),
            "required_star_cosmos_closure_evidence": list(
                REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES
            ),
            "star_cosmos_closure_blocking_conditions": list(
                REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES
            ),
            "star_cosmos_closure_next_stage": "v6_star_source_entry_candidate",
            "star_cosmos_closure_handoff_status": (
                READY_HANDOFF_STATUS if ready else BLOCKED_HANDOFF_STATUS
            ),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_v6_handoff_readiness_metadata(
    metadata: Mapping[str, Any],
    *,
    inventory_complete: bool,
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "v6_handoff_readiness_metadata_type": (
                "future_star_source_entry_candidate_design_readiness_metadata"
            ),
            "v6_handoff_readiness_metadata_mode": "metadata_only",
            "v6_handoff_status": metadata.get("v6_handoff_status"),
            "handoff_status": metadata.get("star_cosmos_closure_handoff_status"),
            "v5_layer_stack_inventory_complete": inventory_complete,
            "v6_entry_candidate_design_allowed": metadata.get(
                "v6_entry_candidate_design_allowed"
            ),
            "v6_entry_candidate_started": False,
            "layer_15_started": False,
            "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
            "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
            "readiness_conditions": list(
                REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES
            ),
            "evidence_requirements": list(
                REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES
            ),
            "blocking_conditions": list(
                REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES
            ),
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _build_star_cosmos_closure_sections(
    context: Mapping[str, Any],
) -> list[dict[str, Any]]:
    section_conditions = {
        "post_sandbox_review_boundary_input_section": (
            context["upstream_pass"]
            and context["hash_present"]
            and context["hash_stable"]
        ),
        "v5_layer_stack_inventory_section": context["inventory_complete"],
        "star_cosmos_closure_metadata_section": context["metadata_valid"],
        "v6_handoff_readiness_section": context["readiness_valid"],
        "layer_14_closure_candidate_only_section": True,
        "v6_entry_disabled_section": not context["v6_started"],
        "layer_15_disabled_section": not context["layer_15_started"],
        "star_source_inactive_section": not context["star_source_memory_active"],
        "actual_closure_disabled_section": (
            not context["actual_layer_14_closure_performed"]
            and not context["closure_handoff_audit_executed"]
        ),
        "closure_record_write_disabled_section": (
            not context["closure_record_written"]
            and not context["closure_evidence_persisted"]
        ),
        "closure_audit_log_write_disabled_section": (
            not context["closure_audit_log_written"]
            and not context["audit_log_written"]
            and not context["audit_evidence_persisted"]
        ),
        "source_provenance_engine_disabled_section": (
            not context["source_provenance_engine_created"]
        ),
        "source_evolution_engine_disabled_section": (
            not context["source_evolution_engine_created"]
        ),
        "source_graph_mutation_disabled_section": (
            not context["source_graph_mutation_enabled"]
            and not context["memory_graph_mutation_enabled"]
        ),
        "sandbox_entry_disabled_section": (
            not context["controlled_adapter_sandbox_started"]
            and not context["adapter_sandbox_entered"]
        ),
        "sandbox_runtime_disabled_section": not context["sandbox_runtime_created"],
        "sandbox_execution_disabled_section": (
            not context["sandbox_execution_enabled"]
            and not context["sandbox_result_available"]
        ),
        "post_sandbox_review_disabled_section": (
            not context["actual_post_sandbox_review_performed"]
        ),
        "rollback_quarantine_incident_disabled_section": (
            not context["rollback_triggered"]
            and not context["quarantine_triggered"]
            and not context["incident_triggered"]
        ),
        "external_network_write_disabled_section": (
            not context["external_calls_enabled"]
            and not context["network_calls_enabled"]
            and not context["durable_writes_enabled"]
            and not context["filesystem_writes_enabled"]
            and not context["database_writes_enabled"]
        ),
        "tool_command_routing_disabled_section": (
            not context["tool_routing_enabled"]
            and not context["command_routing_enabled"]
            and not context["cross_system_coordination_enabled"]
            and not context["system_handoff_completed"]
        ),
        "adapter_manifest_execution_disabled_section": (
            not context["execution_adapter_implemented"]
            and not context["execution_adapter_invoked"]
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
            not context["approval_request_created"]
            and not context["approval_notification_sent"]
            and not context["real_approval_record_written"]
            and not context["execution_authorization_issued"]
            and not context["authorization_token_created"]
            and not context["authorization_grant_created"]
        ),
        "star_cosmos_candidate_only_section": (
            not context["star_cosmos_memory_active"]
        ),
        "star_source_entry_candidate_section": (
            not context["star_source_memory_active"]
            and not context["star_source_entry_candidate_activated"]
        ),
    }
    return [
        _section_from_condition(name, section_conditions[name])
        for name in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES
    ]


def _build_star_cosmos_closure_contracts(
    context: Mapping[str, Any],
) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "star_cosmos_closure_handoff_audit_only_contract": True,
        "star_cosmos_closure_metadata_only_contract": context["metadata_valid"],
        "post_sandbox_review_boundary_pass_contract": context["upstream_pass"],
        "post_sandbox_review_boundary_hash_present_contract": context[
            "hash_present"
        ],
        "post_sandbox_review_boundary_hash_stable_contract": context[
            "hash_stable"
        ],
        "v5_layer_stack_inventory_complete_contract": context[
            "inventory_complete"
        ],
        "star_cosmos_closure_readiness_conditions_declared_contract": context[
            "readiness_names_declared"
        ],
        "star_cosmos_closure_evidence_requirements_declared_contract": context[
            "evidence_names_declared"
        ],
        "star_cosmos_closure_blocking_conditions_declared_contract": context[
            "blocking_names_declared"
        ],
        "star_cosmos_closure_sections_complete_contract": context[
            "sections_complete"
        ],
        "star_cosmos_closure_sections_pass_contract": context["sections_pass"],
        "closure_candidate_only_boundary_contract": True,
        "v6_handoff_metadata_only_contract": context["readiness_valid"],
    }
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        conditions[contract_name] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES
    ]


def _build_star_cosmos_closure_checks(
    context: Mapping[str, Any],
) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "star_cosmos_closure_handoff_audit_stage_check": True,
        "star_cosmos_closure_handoff_audit_only_mode_check": True,
        "star_cosmos_closure_metadata_only_check": context["metadata_valid"],
        "post_sandbox_review_boundary_pass_check": context["upstream_pass"],
        "post_sandbox_review_boundary_hash_present_check": context["hash_present"],
        "post_sandbox_review_boundary_hash_stable_check": context["hash_stable"],
        "v5_layer_stack_inventory_complete_check": context["inventory_complete"],
        "star_cosmos_closure_readiness_conditions_declared_check": context[
            "readiness_names_declared"
        ],
        "star_cosmos_closure_evidence_requirements_declared_check": context[
            "evidence_names_declared"
        ],
        "star_cosmos_closure_blocking_conditions_declared_check": context[
            "blocking_names_declared"
        ],
        "star_cosmos_closure_sections_complete_check": context[
            "sections_complete"
        ],
        "star_cosmos_closure_sections_pass_check": context["sections_pass"],
        "star_cosmos_closure_contracts_pass_check": context["contracts_pass"],
        "closure_candidate_only_boundary_check": True,
        "v6_handoff_metadata_only_check": context["readiness_valid"],
        "deterministic_star_cosmos_closure_handoff_audit_hash_check": True,
        "ready_for_v6_entry_candidate_design_check": (
            context["metadata_valid"]
            and context["readiness_valid"]
            and context["sections_pass"]
            and context["contracts_pass"]
        ),
    }
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        check_name = contract_name.removesuffix("_contract") + "_check"
        conditions[check_name] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES
    ]


def _build_star_cosmos_closure_summary(
    audit_status: str,
    *,
    upstream_hash: str | None,
    hash_stable: bool,
    inventory: Sequence[Mapping[str, Any]],
    metadata_valid: bool,
    readiness_valid: bool,
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "star_cosmos_closure_handoff_audit_summary",
            "star_cosmos_closure_handoff_audit_status": audit_status,
            "handoff_status": (
                READY_HANDOFF_STATUS
                if audit_status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "post_sandbox_review_boundary_hash_present": _is_sha256(upstream_hash),
            "post_sandbox_review_boundary_hash_stable": hash_stable,
            "v5_layer_stack_inventory_count": len(inventory),
            "v5_layer_stack_inventory_complete": _inventory_valid(inventory),
            "star_cosmos_closure_metadata_valid": metadata_valid,
            "v6_handoff_readiness_metadata_valid": readiness_valid,
            "star_cosmos_closure_section_count": len(sections),
            "star_cosmos_closure_sections_pass": _items_pass(
                sections,
                "section_status",
                "section_name",
                REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
            ),
            "star_cosmos_closure_contract_count": len(contracts),
            "star_cosmos_closure_contracts_pass": _items_pass(
                contracts,
                "contract_status",
                "contract_name",
                REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES,
            ),
            "star_cosmos_closure_check_count": len(checks),
            "star_cosmos_closure_checks_pass": _items_pass(
                checks,
                "check_status",
                "check_name",
                REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES,
            ),
            "star_cosmos_closure_status": STAR_COSMOS_CLOSURE_STATUS,
            "layer_14_closure_status": LAYER_14_CLOSURE_STATUS,
            "v6_handoff_status": V6_HANDOFF_STATUS,
            "star_source_entry_status": STAR_SOURCE_ENTRY_STATUS,
            "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    blocking_reasons = (
        [] if condition else ["Star-Cosmos closure section condition must pass"]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": name.removesuffix("_section") + "_boundary",
            "section_status": "pass" if condition else "blocked",
            "source_post_sandbox_review_boundary_refs": list(
                _POST_SANDBOX_REVIEW_BOUNDARY_REFS
            ),
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "star_cosmos_closure_notes": [
                "Deterministic local closure-candidate metadata only."
            ],
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    blocking_reasons = (
        [] if condition else ["Star-Cosmos closure contract condition must pass"]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": name.removesuffix("_contract") + "_boundary_contract",
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "contract_status": "pass" if condition else "blocked",
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _check_from_condition(name: str, condition: bool) -> dict[str, Any]:
    blocking_reasons = (
        [] if condition else ["Star-Cosmos closure check condition must pass"]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "check_name": name,
            "expected": {"condition_satisfied": True},
            "observed": {"condition_satisfied": condition},
            "check_status": "pass" if condition else "blocked",
            "blocking_reasons": blocking_reasons,
            "safety_boundaries": safety_boundaries,
            **COMMON_DISABLED_FLAGS,
            **safety_boundaries,
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    result = _section_from_condition(name, False)
    result["section_type"] = "unknown_star_cosmos_closure_section"
    result["source_post_sandbox_review_boundary_refs"] = []
    result["observed"]["requested_section_name"] = name
    result["blocking_reasons"] = [
        "Star-Cosmos closure section name is not recognized"
    ]
    return _detached_json_value(result)


def _unknown_contract(name: str) -> dict[str, Any]:
    result = _contract_from_condition(name, False)
    result["contract_type"] = "unknown_star_cosmos_closure_contract"
    result["observed"]["requested_contract_name"] = name
    result["blocking_reasons"] = [
        "Star-Cosmos closure contract name is not recognized"
    ]
    return _detached_json_value(result)


def _unknown_check(name: str) -> dict[str, Any]:
    result = _check_from_condition(name, False)
    result["observed"]["requested_check_name"] = name
    result["blocking_reasons"] = [
        "Star-Cosmos closure check name is not recognized"
    ]
    return _detached_json_value(result)


def _star_cosmos_closure_handoff_audit_hash(
    result: Mapping[str, Any],
) -> str:
    projection = {
        field: result[field]
        for field in _STAR_COSMOS_CLOSURE_HASH_FIELDS
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


def _post_sandbox_review_boundary_hash(
    value: Mapping[str, Any],
) -> str | None:
    return _string_or_none(
        value.get("deterministic_post_sandbox_review_boundary_hash")
    )


def _post_sandbox_review_boundary_passes(value: Mapping[str, Any]) -> bool:
    return (
        value.get("version")
        == GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_VERSION
        and value.get("post_sandbox_review_boundary_status") == "pass"
        and _is_sha256(_post_sandbox_review_boundary_hash(value))
        and all(
            value.get(field_name) is False
            for field_name in POST_SANDBOX_REVIEW_DISABLED_FLAGS
        )
        and _all_safety_boundaries_false(value)
    )


def _inventory_valid(inventory: Sequence[Mapping[str, Any]]) -> bool:
    return (
        [item.get("layer_stage_name") for item in inventory]
        == [item[0] for item in _V5_LAYER_STACK_SPECS]
        and len(inventory) == 13
        and all(
            item.get("layer_stage_version_label") == version_label
            and item.get("layer_stage_status") == "sealed_metadata_boundary"
            and item.get("layer_stage_execution_status") == "no_execution"
            and item.get("layer_stage_closure_status")
            == "included_in_layer_14_closure_candidate"
            and _all_common_disabled_flags_false(item)
            and _all_safety_boundaries_false(item)
            for item, (_, version_label, _) in zip(
                inventory,
                _V5_LAYER_STACK_SPECS,
                strict=True,
            )
        )
    )


def _star_cosmos_closure_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("star_cosmos_closure_metadata_type")
        == "layer_14_star_cosmos_closure_handoff_audit_metadata"
        and metadata.get("star_cosmos_closure_metadata_mode")
        == STAR_COSMOS_CLOSURE_MODE
        and metadata.get("star_cosmos_closure_status")
        == STAR_COSMOS_CLOSURE_STATUS
        and metadata.get("layer_14_closure_status") == LAYER_14_CLOSURE_STATUS
        and metadata.get("v6_handoff_status") == V6_HANDOFF_STATUS
        and metadata.get("star_source_entry_status") == STAR_SOURCE_ENTRY_STATUS
        and metadata.get("star_source_memory_active_status")
        == STAR_SOURCE_MEMORY_ACTIVE_STATUS
        and metadata.get("closure_handoff_audit_required") is True
        and metadata.get("closure_handoff_audit_declared") is True
        and metadata.get("closure_handoff_audit_metadata_only") is True
        and metadata.get("post_sandbox_review_boundary_pass_required") is True
        and metadata.get("post_sandbox_review_boundary_hash_required") is True
        and metadata.get("post_sandbox_review_boundary_hash_present") is True
        and metadata.get("post_sandbox_review_boundary_hash_stable") is True
        and metadata.get("v5_layer_stack_complete") is True
        and metadata.get("v5_layer_stack_closure_candidate_only") is True
        and metadata.get("v6_entry_candidate_design_allowed") is True
        and metadata.get("v6_entry_candidate_started") is False
        and metadata.get("star_cosmos_closure_readiness_conditions")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES)
        and metadata.get("required_star_cosmos_closure_evidence")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("star_cosmos_closure_blocking_conditions")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES)
        and metadata.get("star_cosmos_closure_next_stage")
        == "v6_star_source_entry_candidate"
        and metadata.get("star_cosmos_closure_handoff_status")
        == READY_HANDOFF_STATUS
        and _all_common_disabled_flags_false(metadata)
        and _all_safety_boundaries_false(metadata)
    )


def _v6_handoff_readiness_metadata_valid(metadata: Mapping[str, Any]) -> bool:
    return (
        metadata.get("v6_handoff_readiness_metadata_type")
        == "future_star_source_entry_candidate_design_readiness_metadata"
        and metadata.get("v6_handoff_readiness_metadata_mode") == "metadata_only"
        and metadata.get("v6_handoff_status") == V6_HANDOFF_STATUS
        and metadata.get("handoff_status") == READY_HANDOFF_STATUS
        and metadata.get("v5_layer_stack_inventory_complete") is True
        and metadata.get("v6_entry_candidate_design_allowed") is True
        and metadata.get("v6_entry_candidate_started") is False
        and metadata.get("layer_15_started") is False
        and metadata.get("star_source_entry_status") == STAR_SOURCE_ENTRY_STATUS
        and metadata.get("star_source_memory_active_status")
        == STAR_SOURCE_MEMORY_ACTIVE_STATUS
        and metadata.get("readiness_conditions")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES)
        and metadata.get("evidence_requirements")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES)
        and metadata.get("blocking_conditions")
        == list(REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES)
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
