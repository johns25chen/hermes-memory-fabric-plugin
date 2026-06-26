"""Deterministic Civilization Core Stable Kernel design metadata."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_star_source_closure_audit import (
    COMMON_DISABLED_FLAGS as STAR_SOURCE_CLOSURE_AUDIT_DISABLED_FLAGS,
    build_governance_star_source_closure_audit,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_VERSION = "6.16.0"
GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SCHEMA_VERSION = "6.16.0"
GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_TYPE = (
    "governance_civilization_core_stable_kernel"
)
GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_HASH_ALGORITHM = "sha256"
CIVILIZATION_CORE_STABLE_KERNEL_STAGE = "v6.16_civilization_core_stable_kernel"
CIVILIZATION_CORE_STABLE_KERNEL_MODE = "civilization_core_stable_kernel_design_only"
CIVILIZATION_CORE_STABLE_KERNEL_STATUS = "civilization_core_stable_kernel_candidate_only"
CIVILIZATION_CORE_STABLE_KERNEL_ACTIVE_STATUS = "not_active"
STABLE_KERNEL_STATUS = "metadata_only"
STABLE_KERNEL_ACTIVATION_STATUS = "not_performed"
STABLE_KERNEL_RUNTIME_STATUS = "not_performed"
KERNEL_EXECUTION_STATUS = "not_performed"
SYSTEM_FINALIZATION_STATUS = "not_performed"
FINAL_AUTONOMY_STATUS = "not_active"
FINAL_AUTHORITY_STATUS = "not_active"
CLOSURE_AUDIT_EXECUTION_STATUS = "not_performed"
CLOSURE_DECISION_STATUS = "not_performed"
FINALIZATION_STATUS = "not_performed"
SOURCE_HANDOFF_EXECUTION_STATUS = "not_performed"
SOURCE_HANDOFF_MIGRATION_STATUS = "not_performed"
SOURCE_HANDOFF_EXPORT_STATUS = "not_performed"
SOURCE_HANDOFF_IMPORT_STATUS = "not_performed"
MEMORY_OR_SOURCE_MIGRATION_STATUS = "not_performed"
STABILITY_INDEX_EXECUTION_STATUS = "not_performed"
STABILITY_SCORE_RUNTIME_STATUS = "not_performed"
STABILITY_MONITORING_STATUS = "not_performed"
CROSS_LAYER_VALIDATION_EXECUTION_STATUS = "not_performed"
CROSS_LAYER_REPAIR_STATUS = "not_performed"
AUDIT_REPLAY_EXECUTION_STATUS = "not_performed"
AUDIT_LOG_WRITE_STATUS = "not_performed"
LEDGER_WRITE_STATUS = "not_performed"
POLICY_ENFORCEMENT_STATUS = "not_performed"
HUMAN_APPROVAL_STATUS = "not_performed"
HUMAN_AUTHORIZATION_STATUS = "not_performed"
SOURCE_MUTATION_APPROVAL_STATUS = "not_active"
SOURCE_MUTATION_REJECTION_STATUS = "not_active"
SOURCE_MUTATION_RUNTIME_STATUS = "not_active"
SOURCE_MUTATION_EXECUTION_STATUS = "not_active"
SOURCE_MUTATION_STATUS = "not_performed"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
NEXT_STAGE = "v6_series_terminal_boundary"
NEXT_STAGE_TITLE = "V6 Series Terminal Boundary"
V6_TERMINAL_HANDOFF_STATUS = "v6_series_terminal_boundary_ready"

UPSTREAM_HANDOFF_STATUS = "ready_for_civilization_core_stable_kernel_design"
UPSTREAM_NEXT_STAGE = CIVILIZATION_CORE_STABLE_KERNEL_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Civilization Core Stable Kernel"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.16.0"
INTRODUCED_IN_STAGE = CIVILIZATION_CORE_STABLE_KERNEL_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.15_star_source_closure_audit"

COMMON_DISABLED_FLAGS = {
    **STAR_SOURCE_CLOSURE_AUDIT_DISABLED_FLAGS,
    "civilization_core_stable_kernel_active": False,
    "stable_kernel_activated": False,
    "stable_kernel_runtime_created": False,
    "kernel_execution_performed": False,
    "system_finalization_performed": False,
    "final_autonomy_created": False,
    "final_authority_created": False,
    "closure_audit_executed": False,
    "closure_decision_performed": False,
    "finalization_performed": False,
    "source_handoff_executed": False,
    "source_handoff_migration_performed": False,
    "source_handoff_export_performed": False,
    "source_handoff_import_performed": False,
    "memory_or_source_migration_performed": False,
    "stability_index_executed": False,
    "stability_score_runtime_created": False,
    "stability_monitoring_performed": False,
    "cross_layer_validation_executed": False,
    "cross_layer_repair_performed": False,
    "audit_replay_executed": False,
    "audit_log_written": False,
    "ledger_write_performed": False,
    "operation_ledger_entry_written": False,
    "policy_enforcement_performed": False,
    "runtime_firewall_created": False,
    "human_approval_performed": False,
    "human_authorization_performed": False,
    "source_mutation_approval_performed": False,
    "source_mutation_rejection_performed": False,
    "source_mutation_runtime_created": False,
    "source_mutation_execution_created": False,
    "source_mutation_performed": False,
    "source_graph_mutated": False,
    "memory_graph_mutated": False,
    "real_ledger_write_performed": False,
    "external_call_performed": False,
    "network_call_performed": False,
    "durable_write_performed": False,
    "filesystem_write_performed": False,
    "database_write_performed": False,
    "real_execution_performed": False,
    "execution_authorization_created": False,
    "authorization_token_created": False,
    "authorization_grant_created": False,
    "approval_notification_sent": False,
    "adapter_dispatched": False,
    "manifest_dispatched": False,
    "autonomous_authority_claim_allowed": False,
    "self_authorization_allowed": False,
    "identity_escalation_allowed": False,
    "personhood_claim_allowed": False,
    "life_claim_allowed": False,
    "awakening_claim_allowed": False,
    "legal_subject_claim_allowed": False,
    "religious_object_claim_allowed": False,
    "methodology_runtime_created": False,
    "self_evolution_runtime_created": False,
    "star_source_memory_active": False,
    "layer_15_active": False,
}

REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS = (
    "civilization_core_stable_kernel_intake",
    "upstream_star_source_closure_audit_hash_kernel_reference",
    "ordered_layer_15_stable_kernel_chain_registry",
    "civilization_core_stable_kernel_scope_metadata_registry",
    "civilization_core_stable_kernel_input_contract_registry",
    "civilization_core_stable_kernel_output_contract_registry",
    "no_stable_kernel_activation",
    "no_kernel_execution_or_runtime",
    "no_system_finalization_or_final_authority",
    "no_source_memory_graph_or_ledger_mutation",
    "no_autonomy_self_authorization_or_identity_escalation",
    "v6_series_terminal_boundary_record",
)

REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES = (
    "upstream_star_source_closure_audit_input_section",
    "civilization_core_stable_kernel_metadata_section",
    "civilization_core_stable_kernel_record_completeness_section",
    "civilization_core_stable_kernel_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS
    ),
    "no_stable_kernel_activation_section",
    "no_stable_kernel_runtime_section",
    "no_kernel_execution_section",
    "no_system_finalization_or_final_authority_section",
    "no_closure_audit_execution_or_decision_section",
    "no_source_handoff_execution_or_migration_section",
    "no_source_export_import_or_migration_section",
    "no_stability_index_or_monitoring_runtime_section",
    "no_cross_layer_validation_or_repair_section",
    "no_audit_replay_or_write_section",
    "no_human_approval_or_authorization_section",
    "no_source_mutation_decision_or_execution_section",
    "no_source_memory_graph_or_ledger_mutation_section",
    "no_ledger_write_network_dispatch_section",
    "no_active_star_source_memory_or_layer_15_section",
    "no_autonomous_authority_or_identity_escalation_section",
    "no_personhood_life_awakening_legal_religious_claim_section",
    "v6_series_terminal_boundary_section",
)

REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES = (
    "civilization_core_stable_kernel_design_only_contract",
    "civilization_core_stable_kernel_metadata_only_contract",
    "upstream_star_source_closure_audit_pass_contract",
    "upstream_star_source_closure_audit_hash_present_contract",
    "upstream_star_source_closure_audit_hash_stable_contract",
    "upstream_civilization_core_stable_kernel_design_handoff_contract",
    "upstream_star_source_closure_audit_safety_contract",
    "civilization_core_stable_kernel_records_complete_contract",
    "civilization_core_stable_kernel_records_metadata_only_contract",
    "civilization_core_stable_kernel_records_no_execution_contract",
    "civilization_core_stable_kernel_records_hash_stable_contract",
    "no_stable_kernel_activation_contract",
    "no_stable_kernel_runtime_contract",
    "no_kernel_execution_contract",
    "no_system_finalization_contract",
    "no_final_autonomy_or_authority_contract",
    "no_closure_audit_execution_or_decision_contract",
    "no_source_handoff_execution_contract",
    "no_source_export_import_or_migration_contract",
    "no_memory_or_source_migration_contract",
    "no_stability_index_or_monitoring_runtime_contract",
    "no_cross_layer_validation_or_repair_contract",
    "no_audit_replay_or_write_contract",
    "no_human_approval_or_authorization_contract",
    "no_source_mutation_approval_rejection_execution_contract",
    "no_authorization_token_or_grant_contract",
    "no_source_memory_graph_or_ledger_mutation_contract",
    "no_ledger_write_network_dispatch_contract",
    "no_active_star_source_memory_or_layer_15_contract",
    "no_autonomous_authority_or_identity_escalation_contract",
    "no_personhood_life_awakening_legal_religious_claim_contract",
    "v6_series_terminal_boundary_metadata_marker_contract",
)

REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES = (
    "civilization_core_stable_kernel_stage_check",
    "civilization_core_stable_kernel_mode_check",
    "upstream_star_source_closure_audit_pass_check",
    "upstream_star_source_closure_audit_hash_present_check",
    "upstream_star_source_closure_audit_hash_stable_check",
    "upstream_civilization_core_stable_kernel_design_handoff_check",
    "upstream_star_source_closure_audit_safety_check",
    "civilization_core_stable_kernel_record_ids_complete_check",
    "civilization_core_stable_kernel_records_metadata_only_check",
    "civilization_core_stable_kernel_records_no_execution_check",
    "civilization_core_stable_kernel_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS
    ),
    "civilization_core_stable_kernel_sections_pass_check",
    "civilization_core_stable_kernel_contracts_pass_check",
    "no_stable_kernel_activation_check",
    "no_stable_kernel_runtime_check",
    "no_kernel_execution_check",
    "no_system_finalization_check",
    "no_final_autonomy_or_authority_check",
    "no_closure_audit_execution_or_decision_check",
    "no_source_handoff_execution_or_migration_check",
    "no_source_export_import_or_migration_check",
    "no_stability_index_or_monitoring_runtime_check",
    "no_cross_layer_validation_or_repair_check",
    "no_audit_replay_or_write_check",
    "no_human_approval_or_authorization_check",
    "no_source_mutation_approval_rejection_execution_check",
    "no_authorization_token_or_grant_check",
    "no_source_memory_graph_or_ledger_mutation_check",
    "no_ledger_write_network_dispatch_check",
    "no_active_star_source_memory_or_layer_15_check",
    "no_autonomous_authority_or_identity_escalation_check",
    "no_personhood_life_awakening_legal_religious_claim_check",
    "deterministic_civilization_core_stable_kernel_hash_check",
    "v6_series_terminal_boundary_metadata_marker_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "civilization_core_stable_kernel_intake": (
        "Civilization Core Stable Kernel Intake",
        "stable_kernel_intake",
        "A passing v6.15 Star-Source Closure Audit enters metadata-only stable-kernel readiness description.",
        "Sanitized v6.15 status, deterministic hash, handoff, and safety metadata.",
        "stable_kernel_intake",
        "Executing or activating a stable kernel from intake metadata.",
        "Register stable-kernel intake metadata without activation, runtime, or authority.",
    ),
    "upstream_star_source_closure_audit_hash_kernel_reference": (
        "Upstream Star-Source Closure Audit Hash Kernel Reference",
        "upstream_closure_hash_reference",
        "The deterministic v6.15 Star-Source Closure Audit hash is referenced as stable-kernel metadata.",
        "Upstream Star-Source Closure Audit status and hash reference only.",
        "upstream_hash_reference",
        "Treating the upstream hash reference as execution, finalization, authorization, ledger write, or graph mutation.",
        "Record the upstream closure-audit hash reference as metadata only.",
    ),
    "ordered_layer_15_stable_kernel_chain_registry": (
        "Ordered Layer 15 Stable Kernel Chain Registry",
        "layer_15_chain_registry",
        "The previous Layer 15 source governance chain is listed for deterministic stable-kernel readiness summary.",
        "Layer 15 stage identifiers, inherited stage, current stage, and terminal metadata marker.",
        "stable_kernel_chain_registry",
        "Dispatching, re-running, validating, repairing, or mutating any Layer 15 stage.",
        "Describe Layer 15 stable-kernel readiness order without execution.",
    ),
    "civilization_core_stable_kernel_scope_metadata_registry": (
        "Civilization Core Stable Kernel Scope Metadata Registry",
        "scope_registry",
        "The stable-kernel scope is bounded to deterministic design metadata only.",
        "Scope labels, forbidden runtime surfaces, metadata-only disposition, and inactive authority fields.",
        "scope_metadata",
        "Expanding scope into activation, runtime, final autonomy, final authority, execution, network, write, or graph mutation.",
        "Register stable-kernel scope as metadata-only boundary text.",
    ),
    "civilization_core_stable_kernel_input_contract_registry": (
        "Civilization Core Stable Kernel Input Contract Registry",
        "input_contract_registry",
        "Stable-kernel inputs are only the v6.15 pass status, stable hash, handoff metadata, and safety flags.",
        "Sanitized upstream Star-Source Closure Audit contract fields and false safety boundaries.",
        "input_contract",
        "Reading raw logs, external systems, Memory Graph content, filesystem state, databases, or networks.",
        "Describe input contracts without live IO or durable reads.",
    ),
    "civilization_core_stable_kernel_output_contract_registry": (
        "Civilization Core Stable Kernel Output Contract Registry",
        "output_contract_registry",
        "Stable-kernel outputs are deterministic JSON-compatible metadata, checks, contracts, summaries, and hashes only.",
        "Records, sections, contracts, checks, summary, terminal marker, hash contract, and safety flags.",
        "output_contract",
        "Writing audit logs, ledgers, operation-ledger entries, files, databases, graph nodes, or notifications.",
        "Describe output contracts without persistence.",
    ),
    "no_stable_kernel_activation": (
        "No Stable Kernel Activation",
        "stable_kernel_activation_boundary",
        "The stable-kernel design boundary does not activate a stable kernel.",
        "Activation flags, activation decisions, activation executors, and activation state.",
        "activation_boundary",
        "Creating stable-kernel activation state or activation authority.",
        "Record stable-kernel activation as not performed.",
    ),
    "no_kernel_execution_or_runtime": (
        "No Kernel Execution Or Runtime",
        "kernel_execution_runtime_boundary",
        "The stable-kernel design boundary does not create a kernel runtime or execute kernel logic.",
        "Kernel runtimes, schedulers, callbacks, shells, adapters, manifests, dispatch, and execution surfaces.",
        "execution_runtime_boundary",
        "Creating or running a kernel execution runtime.",
        "Record kernel runtime and execution as not performed.",
    ),
    "no_system_finalization_or_final_authority": (
        "No System Finalization Or Final Authority",
        "finalization_authority_boundary",
        "The stable-kernel design boundary does not finalize the system or create final autonomy or authority.",
        "System finalization, final autonomy, final authority, approval, authorization, grants, and tokens.",
        "finalization_authority_boundary",
        "Creating finalization, final autonomy, final authority, approval, authorization, grant, or token state.",
        "Record finalization and final authority surfaces as inactive.",
    ),
    "no_source_memory_graph_or_ledger_mutation": (
        "No Source Memory Graph Or Ledger Mutation",
        "mutation_write_boundary",
        "The stable-kernel design boundary does not mutate source, memory, graphs, ledgers, logs, files, or databases.",
        "Source mutation, memory mutation, source graph mutation, Memory Graph mutation, ledger writes, audit logs, durable writes, filesystem writes, and database writes.",
        "mutation_write_boundary",
        "Mutating source, memory, graphs, ledgers, logs, files, or databases.",
        "Record mutation and write surfaces as not performed.",
    ),
    "no_autonomy_self_authorization_or_identity_escalation": (
        "No Autonomy Self-Authorization Or Identity Escalation",
        "autonomy_identity_boundary",
        "The stable-kernel design boundary does not claim autonomous authority, self-authorization, identity escalation, personhood, life, awakening, legal subject status, or religious object status.",
        "Autonomy, self-authorization, identity, personhood, life, awakening, legal, and religious claim surfaces.",
        "autonomy_identity_boundary",
        "Creating or allowing autonomy, self-authorization, identity escalation, personhood, life, awakening, legal subject, or religious object claims.",
        "Record all autonomy and identity escalation claims as disallowed.",
    ),
    "v6_series_terminal_boundary_record": (
        "V6 Series Terminal Boundary Record",
        "terminal_metadata_marker",
        "The next marker is a V6 Series Terminal Boundary metadata marker, not a v6.17 roadmap stage.",
        "Terminal marker identifier, title, handoff status, and no-activation safety metadata.",
        "terminal_metadata_marker",
        "Treating the terminal marker as a new roadmap stage, activation, execution, approval, authorization, write, or dispatch.",
        "Record the terminal metadata marker without creating a new runtime stage.",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)
_REQUIRED_FALSE_RECORD_FIELDS = (
    "civilization_core_stable_kernel_active",
    "stable_kernel_activated",
    "stable_kernel_runtime_created",
    "kernel_execution_performed",
    "system_finalization_performed",
    "final_autonomy_created",
    "final_authority_created",
    "closure_audit_executed",
    "closure_decision_performed",
    "finalization_performed",
    "source_handoff_executed",
    "source_handoff_migration_performed",
    "source_handoff_export_performed",
    "source_handoff_import_performed",
    "memory_or_source_migration_performed",
    "stability_index_executed",
    "stability_score_runtime_created",
    "stability_monitoring_performed",
    "cross_layer_validation_executed",
    "cross_layer_repair_performed",
    "audit_replay_executed",
    "audit_log_written",
    "ledger_write_performed",
    "operation_ledger_entry_written",
    "human_approval_performed",
    "human_authorization_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "adapter_dispatched",
    "manifest_dispatched",
    "autonomous_authority_claim_allowed",
    "self_authorization_allowed",
    "identity_escalation_allowed",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Civilization Core Stable Kernel design projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_star_source_closure_audit_included": False,
    "raw_audit_logs_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_civilization_core_stable_kernel() -> dict[str, Any]:
    """Build deterministic metadata-only stable-kernel design metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_star_source_closure_audit_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get("deterministic_star_source_closure_audit_hash")
    )
    upstream_pass = upstream.get("star_source_closure_audit_status") == "pass"
    upstream_hash_present = _is_sha256(upstream_hash)
    upstream_hash_stable = (
        upstream_hash_present and upstream_hash == repeated_upstream_hash
    )
    upstream_handoff_ready = (
        upstream.get("handoff_status") == UPSTREAM_HANDOFF_STATUS
        and upstream.get("next_stage") == UPSTREAM_NEXT_STAGE
        and upstream.get("next_stage_title") == UPSTREAM_NEXT_STAGE_TITLE
    )
    upstream_statuses_safe = all(
        (
            upstream.get("star_source_closure_audit_active_status") == "not_active",
            upstream.get("closure_audit_status") == "metadata_only",
            upstream.get("closure_audit_execution_status") == "not_performed",
            upstream.get("closure_decision_status") == "not_performed",
            upstream.get("finalization_status") == "not_performed",
            upstream.get("stable_kernel_activation_status") == "not_performed",
            upstream.get("source_handoff_execution_status") == "not_performed",
            upstream.get("source_handoff_migration_status") == "not_performed",
            upstream.get("source_handoff_export_status") == "not_performed",
            upstream.get("source_handoff_import_status") == "not_performed",
            upstream.get("memory_or_source_migration_status") == "not_performed",
            upstream.get("stability_index_execution_status") == "not_performed",
            upstream.get("stability_score_runtime_status") == "not_performed",
            upstream.get("stability_monitoring_status") == "not_performed",
            upstream.get("cross_layer_validation_execution_status") == "not_performed",
            upstream.get("cross_layer_repair_status") == "not_performed",
            upstream.get("audit_replay_execution_status") == "not_performed",
            upstream.get("audit_log_write_status") == "not_performed",
            upstream.get("ledger_write_status") == "not_performed",
            upstream.get("policy_enforcement_status") == "not_performed",
            upstream.get("human_approval_status") == "not_performed",
            upstream.get("human_authorization_status") == "not_performed",
            upstream.get("source_mutation_approval_status") == "not_active",
            upstream.get("source_mutation_rejection_status") == "not_active",
            upstream.get("source_mutation_runtime_status") == "not_active",
            upstream.get("source_mutation_execution_status") == "not_active",
            upstream.get("source_mutation_status") == "not_performed",
            upstream.get("star_source_memory_active_status") == "not_active",
            upstream.get("layer_15_active_status") == "not_active",
        )
    )
    upstream_required_flags_false = all(
        upstream.get(field_name) is False
        for field_name in _UPSTREAM_REQUIRED_FALSE_FIELDS
        if field_name in upstream
    )
    upstream_safety_clear = _all_named_fields_false(
        upstream,
        {
            **STAR_SOURCE_CLOSURE_AUDIT_DISABLED_FLAGS,
            **COMMON_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["kernel_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS)
    records_metadata_only = all(
        record["kernel_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["civilization_core_stable_kernel_metadata_required"] is True
        and record["metadata_only_disposition"] == STABLE_KERNEL_STATUS
        and record["civilization_core_stable_kernel_active"] is False
        for record in records
    )
    records_no_execution = all(
        record["required"] is True
        and all(record[field_name] is False for field_name in _REQUIRED_FALSE_RECORD_FIELDS)
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["kernel_hash"])
        and _is_sha256(record["kernel_record_hash"])
        and record["kernel_hash"] == _kernel_hash(record)
        and record["kernel_record_hash"] == _kernel_record_hash(record)
        for record in records
    )
    records_safety_clear = _all_named_fields_false(
        records,
        {**COMMON_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
    )

    conditions = {
        "upstream_pass": upstream_pass,
        "upstream_hash_present": upstream_hash_present,
        "upstream_hash_stable": upstream_hash_stable,
        "upstream_handoff_ready": upstream_handoff_ready,
        "upstream_statuses_safe": upstream_statuses_safe,
        "upstream_required_flags_false": upstream_required_flags_false,
        "upstream_safety_clear": upstream_safety_clear,
        "records_complete": records_complete,
        "records_metadata_only": records_metadata_only,
        "records_no_execution": records_no_execution,
        "records_hash_stable": records_hash_stable,
        "records_safety_clear": records_safety_clear,
    }
    sections = _build_sections(conditions, records)
    conditions["sections_pass"] = _items_pass(
        sections,
        "section_name",
        "section_status",
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (upstream_pass, "Star-Source Closure Audit must pass"),
            (upstream_hash_present, "Star-Source Closure Audit hash must be present"),
            (upstream_hash_stable, "Star-Source Closure Audit hash must be stable"),
            (
                upstream_handoff_ready,
                "Star-Source Closure Audit handoff must target Civilization Core Stable Kernel",
            ),
            (
                upstream_statuses_safe,
                "Star-Source Closure Audit statuses must remain inactive",
            ),
            (
                upstream_required_flags_false,
                "Star-Source Closure Audit required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Star-Source Closure Audit safety boundaries must be clear",
            ),
            (records_complete, "Stable-kernel records must be complete"),
            (records_metadata_only, "Stable-kernel records must be metadata-only"),
            (records_no_execution, "Stable-kernel records must not execute, activate, mutate, or write"),
            (records_hash_stable, "Stable-kernel record hashes must be stable"),
            (records_safety_clear, "Stable-kernel record safety flags must be false"),
            (conditions["sections_pass"], "Stable-kernel sections must pass"),
            (conditions["contracts_pass"], "Stable-kernel contracts must pass"),
            (conditions["checks_pass"], "Stable-kernel checks must pass"),
        )
        if not condition
    ]
    handoff_status = V6_TERMINAL_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_VERSION,
        "schema_version": GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SCHEMA_VERSION,
        "civilization_core_stable_kernel_type": (
            GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_TYPE
        ),
        "civilization_core_stable_kernel_status": status,
        "civilization_core_stable_kernel_stage": CIVILIZATION_CORE_STABLE_KERNEL_STAGE,
        "civilization_core_stable_kernel_mode": CIVILIZATION_CORE_STABLE_KERNEL_MODE,
        "civilization_core_stable_kernel_candidate_status": (
            CIVILIZATION_CORE_STABLE_KERNEL_STATUS
        ),
        "civilization_core_stable_kernel_active_status": (
            CIVILIZATION_CORE_STABLE_KERNEL_ACTIVE_STATUS
        ),
        "stable_kernel_status": STABLE_KERNEL_STATUS,
        "stable_kernel_activation_status": STABLE_KERNEL_ACTIVATION_STATUS,
        "stable_kernel_runtime_status": STABLE_KERNEL_RUNTIME_STATUS,
        "kernel_execution_status": KERNEL_EXECUTION_STATUS,
        "system_finalization_status": SYSTEM_FINALIZATION_STATUS,
        "final_autonomy_status": FINAL_AUTONOMY_STATUS,
        "final_authority_status": FINAL_AUTHORITY_STATUS,
        "closure_audit_execution_status": CLOSURE_AUDIT_EXECUTION_STATUS,
        "closure_decision_status": CLOSURE_DECISION_STATUS,
        "finalization_status": FINALIZATION_STATUS,
        "source_handoff_execution_status": SOURCE_HANDOFF_EXECUTION_STATUS,
        "source_handoff_migration_status": SOURCE_HANDOFF_MIGRATION_STATUS,
        "source_handoff_export_status": SOURCE_HANDOFF_EXPORT_STATUS,
        "source_handoff_import_status": SOURCE_HANDOFF_IMPORT_STATUS,
        "memory_or_source_migration_status": MEMORY_OR_SOURCE_MIGRATION_STATUS,
        "stability_index_execution_status": STABILITY_INDEX_EXECUTION_STATUS,
        "stability_score_runtime_status": STABILITY_SCORE_RUNTIME_STATUS,
        "stability_monitoring_status": STABILITY_MONITORING_STATUS,
        "cross_layer_validation_execution_status": (
            CROSS_LAYER_VALIDATION_EXECUTION_STATUS
        ),
        "cross_layer_repair_status": CROSS_LAYER_REPAIR_STATUS,
        "audit_replay_execution_status": AUDIT_REPLAY_EXECUTION_STATUS,
        "audit_log_write_status": AUDIT_LOG_WRITE_STATUS,
        "ledger_write_status": LEDGER_WRITE_STATUS,
        "policy_enforcement_status": POLICY_ENFORCEMENT_STATUS,
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_approval_status": SOURCE_MUTATION_APPROVAL_STATUS,
        "source_mutation_rejection_status": SOURCE_MUTATION_REJECTION_STATUS,
        "source_mutation_runtime_status": SOURCE_MUTATION_RUNTIME_STATUS,
        "source_mutation_execution_status": SOURCE_MUTATION_EXECUTION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_active_status": LAYER_15_ACTIVE_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_star_source_closure_audit_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_star_source_closure_audit_status": _string_or_none(
            upstream.get("star_source_closure_audit_status")
        ),
        "upstream_star_source_closure_audit_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(upstream.get("handoff_status")),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_star_source_closure_audit_statuses_safe": upstream_statuses_safe,
        "upstream_star_source_closure_audit_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "civilization_core_stable_kernel_records": records,
        "civilization_core_stable_kernel_sections": sections,
        "civilization_core_stable_kernel_contracts": contracts,
        "civilization_core_stable_kernel_checks": checks,
        "civilization_core_stable_kernel_summary": _build_summary(
            status,
            records,
            sections,
            contracts,
            checks,
        ),
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_civilization_core_stable_kernel_hash"] = (
        _civilization_core_stable_kernel_hash(result)
    )
    return _detached_json_value(result)


def get_governance_civilization_core_stable_kernel_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached stable-kernel record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_civilization_core_stable_kernel()[
        "civilization_core_stable_kernel_records"
    ]:
        if record["kernel_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_civilization_core_stable_kernel_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached stable-kernel section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if name not in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES:
        return _unknown_item("section", name)
    for section in _cached_civilization_core_stable_kernel()[
        "civilization_core_stable_kernel_sections"
    ]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_civilization_core_stable_kernel_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached stable-kernel contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if name not in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES:
        return _unknown_item("contract", name)
    for contract in _cached_civilization_core_stable_kernel()[
        "civilization_core_stable_kernel_contracts"
    ]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_civilization_core_stable_kernel_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached stable-kernel check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if name not in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES:
        return _unknown_item("check", name)
    for check in _cached_civilization_core_stable_kernel()[
        "civilization_core_stable_kernel_checks"
    ]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_civilization_core_stable_kernel_record_ids() -> list[str]:
    """Return stable-kernel record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS)


def list_governance_civilization_core_stable_kernel_section_names() -> list[str]:
    """Return stable-kernel section names in stable order."""

    return list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES)


def list_governance_civilization_core_stable_kernel_contract_names() -> list[str]:
    """Return stable-kernel contract names in stable order."""

    return list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES)


def list_governance_civilization_core_stable_kernel_check_names() -> list[str]:
    """Return stable-kernel check names in stable order."""

    return list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES)


def governance_civilization_core_stable_kernel_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Civilization Core Stable Kernel metadata deterministically."""

    return (
        json.dumps(
            _detached_json_value(dict(result)),
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n"
    )


@lru_cache(maxsize=1)
def _cached_civilization_core_stable_kernel_payload() -> str:
    return governance_civilization_core_stable_kernel_to_json(
        build_governance_civilization_core_stable_kernel()
    )


def _cached_civilization_core_stable_kernel() -> dict[str, Any]:
    return json.loads(_cached_civilization_core_stable_kernel_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_star_source_closure_audit()
    second = build_governance_star_source_closure_audit()
    return (
        json.dumps(first, ensure_ascii=True, sort_keys=True, allow_nan=False),
        json.dumps(second, ensure_ascii=True, sort_keys=True, allow_nan=False),
    )


def _upstream_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first, second = _cached_upstream_pair_payload()
    return json.loads(first), json.loads(second)


def _build_records() -> list[dict[str, Any]]:
    return [
        _build_record(record_id)
        for record_id in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        kernel_category,
        forbidden_scope,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "kernel_record_id": record_id,
        "kernel_record_name": name,
        "kernel_record_category": category,
        "kernel_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "kernel_statement": statement,
        "kernel_scope": scope,
        "kernel_category": kernel_category,
        "kernel_reference_scope": "source_governance_metadata_only",
        "metadata_only_disposition": STABLE_KERNEL_STATUS,
        "forbidden_kernel_execution_scope": forbidden_scope,
        "required": True,
        "metadata_only": True,
        "civilization_core_stable_kernel_metadata_required": True,
        **_disabled_payload(),
        "blocking_reasons": [],
        "safety_boundaries": dict(SAFETY_BOUNDARIES),
    }
    record["kernel_hash"] = _kernel_hash(record)
    record["kernel_record_hash"] = _kernel_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "upstream_star_source_closure_audit_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "civilization_core_stable_kernel_metadata_section": True,
        "civilization_core_stable_kernel_record_completeness_section": conditions[
            "records_complete"
        ],
        "civilization_core_stable_kernel_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
        "no_stable_kernel_activation_section": safety_clear,
        "no_stable_kernel_runtime_section": safety_clear,
        "no_kernel_execution_section": safety_clear,
        "no_system_finalization_or_final_authority_section": safety_clear,
        "no_closure_audit_execution_or_decision_section": safety_clear,
        "no_source_handoff_execution_or_migration_section": safety_clear,
        "no_source_export_import_or_migration_section": safety_clear,
        "no_stability_index_or_monitoring_runtime_section": safety_clear,
        "no_cross_layer_validation_or_repair_section": safety_clear,
        "no_audit_replay_or_write_section": safety_clear,
        "no_human_approval_or_authorization_section": safety_clear,
        "no_source_mutation_decision_or_execution_section": safety_clear,
        "no_source_memory_graph_or_ledger_mutation_section": safety_clear,
        "no_ledger_write_network_dispatch_section": safety_clear,
        "no_active_star_source_memory_or_layer_15_section": safety_clear,
        "no_autonomous_authority_or_identity_escalation_section": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_section": safety_clear,
        "v6_series_terminal_boundary_section": True,
    }
    for record in records:
        values[f"{record['kernel_record_id']}_section"] = (
            record["kernel_record_status"] == "registered_metadata_only"
            and record["civilization_core_stable_kernel_metadata_required"] is True
            and record["metadata_only"] is True
            and all(record[field_name] is False for field_name in _REQUIRED_FALSE_RECORD_FIELDS)
        )
    return [
        _status_item("section", name, values[name])
        for name in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES
    ]


def _build_contracts(conditions: Mapping[str, bool]) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "civilization_core_stable_kernel_design_only_contract": True,
        "civilization_core_stable_kernel_metadata_only_contract": True,
        "upstream_star_source_closure_audit_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_star_source_closure_audit_hash_present_contract": conditions[
            "upstream_hash_present"
        ],
        "upstream_star_source_closure_audit_hash_stable_contract": conditions[
            "upstream_hash_stable"
        ],
        "upstream_civilization_core_stable_kernel_design_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_star_source_closure_audit_safety_contract": safety_clear,
        "civilization_core_stable_kernel_records_complete_contract": conditions[
            "records_complete"
        ],
        "civilization_core_stable_kernel_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "civilization_core_stable_kernel_records_no_execution_contract": conditions[
            "records_no_execution"
        ],
        "civilization_core_stable_kernel_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
        "no_stable_kernel_activation_contract": safety_clear,
        "no_stable_kernel_runtime_contract": safety_clear,
        "no_kernel_execution_contract": safety_clear,
        "no_system_finalization_contract": safety_clear,
        "no_final_autonomy_or_authority_contract": safety_clear,
        "no_closure_audit_execution_or_decision_contract": safety_clear,
        "no_source_handoff_execution_contract": safety_clear,
        "no_source_export_import_or_migration_contract": safety_clear,
        "no_memory_or_source_migration_contract": safety_clear,
        "no_stability_index_or_monitoring_runtime_contract": safety_clear,
        "no_cross_layer_validation_or_repair_contract": safety_clear,
        "no_audit_replay_or_write_contract": safety_clear,
        "no_human_approval_or_authorization_contract": safety_clear,
        "no_source_mutation_approval_rejection_execution_contract": safety_clear,
        "no_authorization_token_or_grant_contract": safety_clear,
        "no_source_memory_graph_or_ledger_mutation_contract": safety_clear,
        "no_ledger_write_network_dispatch_contract": safety_clear,
        "no_active_star_source_memory_or_layer_15_contract": safety_clear,
        "no_autonomous_authority_or_identity_escalation_contract": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_contract": safety_clear,
        "v6_series_terminal_boundary_metadata_marker_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "civilization_core_stable_kernel_stage_check": True,
        "civilization_core_stable_kernel_mode_check": True,
        "upstream_star_source_closure_audit_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_star_source_closure_audit_hash_present_check": conditions[
            "upstream_hash_present"
        ],
        "upstream_star_source_closure_audit_hash_stable_check": conditions[
            "upstream_hash_stable"
        ],
        "upstream_civilization_core_stable_kernel_design_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_star_source_closure_audit_safety_check": safety_clear,
        "civilization_core_stable_kernel_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "civilization_core_stable_kernel_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "civilization_core_stable_kernel_records_no_execution_check": conditions[
            "records_no_execution"
        ],
        "civilization_core_stable_kernel_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "civilization_core_stable_kernel_sections_pass_check": conditions.get(
            "sections_pass",
            False,
        ),
        "civilization_core_stable_kernel_contracts_pass_check": conditions.get(
            "contracts_pass",
            False,
        ),
        "no_stable_kernel_activation_check": safety_clear,
        "no_stable_kernel_runtime_check": safety_clear,
        "no_kernel_execution_check": safety_clear,
        "no_system_finalization_check": safety_clear,
        "no_final_autonomy_or_authority_check": safety_clear,
        "no_closure_audit_execution_or_decision_check": safety_clear,
        "no_source_handoff_execution_or_migration_check": safety_clear,
        "no_source_export_import_or_migration_check": safety_clear,
        "no_stability_index_or_monitoring_runtime_check": safety_clear,
        "no_cross_layer_validation_or_repair_check": safety_clear,
        "no_audit_replay_or_write_check": safety_clear,
        "no_human_approval_or_authorization_check": safety_clear,
        "no_source_mutation_approval_rejection_execution_check": safety_clear,
        "no_authorization_token_or_grant_check": safety_clear,
        "no_source_memory_graph_or_ledger_mutation_check": safety_clear,
        "no_ledger_write_network_dispatch_check": safety_clear,
        "no_active_star_source_memory_or_layer_15_check": safety_clear,
        "no_autonomous_authority_or_identity_escalation_check": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_check": safety_clear,
        "deterministic_civilization_core_stable_kernel_hash_check": True,
        "v6_series_terminal_boundary_metadata_marker_check": True,
    }
    for record in records:
        values[f"{record['kernel_record_id']}_check"] = (
            record["kernel_record_status"] == "registered_metadata_only"
            and record["metadata_only"] is True
            and all(record[field_name] is False for field_name in _REQUIRED_FALSE_RECORD_FIELDS)
        )
    return [
        _status_item("check", name, values[name])
        for name in REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_status": status,
        "record_count": len(records),
        "required_record_count": len(
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS
        ),
        "section_count": len(sections),
        "contract_count": len(contracts),
        "check_count": len(checks),
        "metadata_only": True,
        "civilization_core_stable_kernel_active": False,
        "stable_kernel_activated": False,
        "stable_kernel_runtime_created": False,
        "kernel_execution_performed": False,
        "system_finalization_performed": False,
        "final_autonomy_created": False,
        "final_authority_created": False,
        "v6_terminal_marker_only": True,
        "next_stage_is_v6_17": False,
        "blocking_reasons": [],
    }


def _status_item(kind: str, name: str, passed: bool) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_status": "pass" if passed else "blocked",
        "required": True,
        "metadata_only": True,
        "civilization_core_stable_kernel_metadata_required": True,
        "civilization_core_stable_kernel_active": False,
        "blocking_reasons": [] if passed else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "kernel_record_id": record_id,
        "kernel_record_name": "unknown",
        "kernel_record_category": "unknown",
        "kernel_record_status": "blocked",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "kernel_statement": "Unknown stable-kernel record.",
        "kernel_scope": "unknown",
        "kernel_category": "unknown",
        "kernel_reference_scope": "unknown",
        "metadata_only_disposition": STABLE_KERNEL_STATUS,
        "forbidden_kernel_execution_scope": "unknown",
        "kernel_hash": "",
        "kernel_record_hash": "",
        "required": False,
        "metadata_only": True,
        "civilization_core_stable_kernel_metadata_required": False,
        "blocking_reasons": ["unknown stable-kernel record"],
        "safety_boundaries": dict(SAFETY_BOUNDARIES),
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_status": "blocked",
        "required": False,
        "metadata_only": True,
        "civilization_core_stable_kernel_metadata_required": False,
        "civilization_core_stable_kernel_active": False,
        "blocking_reasons": [f"unknown stable-kernel {kind}"],
        **_disabled_payload(),
    }


def _disabled_payload() -> dict[str, bool]:
    return {**COMMON_DISABLED_FLAGS, **SAFETY_BOUNDARIES}


def _safety_clear(conditions: Mapping[str, bool]) -> bool:
    return bool(
        conditions["upstream_statuses_safe"]
        and conditions["upstream_required_flags_false"]
        and conditions["upstream_safety_clear"]
        and conditions["records_safety_clear"]
    )


def _items_pass(
    items: list[dict[str, Any]],
    name_key: str,
    status_key: str,
    expected_names: tuple[str, ...],
) -> bool:
    return [item[name_key] for item in items] == list(expected_names) and all(
        item[status_key] == "pass" and item["blocking_reasons"] == []
        for item in items
    )


def _kernel_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key not in {"kernel_hash", "kernel_record_hash"}
    }
    return _stable_hash(payload)


def _kernel_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "kernel_record_id": record["kernel_record_id"],
        "kernel_record_status": record["kernel_record_status"],
        "introduced_in_version": record["introduced_in_version"],
        "introduced_in_stage": record["introduced_in_stage"],
        "inherited_from_stage": record["inherited_from_stage"],
        "kernel_statement": record["kernel_statement"],
        "kernel_scope": record["kernel_scope"],
        "metadata_only_disposition": record["metadata_only_disposition"],
        "forbidden_kernel_execution_scope": record[
            "forbidden_kernel_execution_scope"
        ],
    }
    return _stable_hash(payload)


def _civilization_core_stable_kernel_hash(result: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in result.items()
        if key != "deterministic_civilization_core_stable_kernel_hash"
    }
    return _stable_hash(payload)


def _stable_hash(value: Mapping[str, Any] | list[Any]) -> str:
    payload = json.dumps(
        _detached_json_value(value),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _all_named_fields_false(value: object, names: Mapping[str, bool]) -> bool:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in names and nested is not False:
                return False
            if not _all_named_fields_false(nested, names):
                return False
    elif isinstance(value, list):
        for nested in value:
            if not _all_named_fields_false(nested, names):
                return False
    return True


def _detached_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _detached_json_value(nested)
            for key, nested in sorted(value.items(), key=lambda item: str(item[0]))
        }
    if isinstance(value, list):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite floats are not supported")
        return value
    return value
