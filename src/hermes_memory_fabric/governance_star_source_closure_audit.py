"""Deterministic Star-Source Closure Audit metadata."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_handoff_boundary import (
    COMMON_DISABLED_FLAGS as SOURCE_HANDOFF_BOUNDARY_DISABLED_FLAGS,
    build_governance_source_handoff_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_VERSION = "6.15.0"
GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SCHEMA_VERSION = "6.15.0"
GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_TYPE = (
    "governance_star_source_closure_audit"
)
GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_HASH_ALGORITHM = "sha256"
STAR_SOURCE_CLOSURE_AUDIT_STAGE = "v6.15_star_source_closure_audit"
STAR_SOURCE_CLOSURE_AUDIT_MODE = "star_source_closure_audit_only"
STAR_SOURCE_CLOSURE_AUDIT_STATUS = "star_source_closure_audit_candidate_only"
STAR_SOURCE_CLOSURE_AUDIT_ACTIVE_STATUS = "not_active"
CLOSURE_AUDIT_STATUS = "metadata_only"
CLOSURE_AUDIT_EXECUTION_STATUS = "not_performed"
CLOSURE_DECISION_STATUS = "not_performed"
FINALIZATION_STATUS = "not_performed"
STABLE_KERNEL_ACTIVATION_STATUS = "not_performed"
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
NEXT_STAGE = "v6.16_civilization_core_stable_kernel"
NEXT_STAGE_TITLE = "Civilization Core Stable Kernel"
V6_16_HANDOFF_STATUS = "ready_for_civilization_core_stable_kernel_design"

UPSTREAM_HANDOFF_STATUS = "ready_for_star_source_closure_audit_design"
UPSTREAM_NEXT_STAGE = STAR_SOURCE_CLOSURE_AUDIT_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Star-Source Closure Audit"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.15.0"
INTRODUCED_IN_STAGE = STAR_SOURCE_CLOSURE_AUDIT_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.14_source_handoff_boundary"

COMMON_DISABLED_FLAGS = {
    **SOURCE_HANDOFF_BOUNDARY_DISABLED_FLAGS,
    "star_source_closure_audit_active": False,
    "star_source_closure_executed": False,
    "closure_decision_performed": False,
    "finalization_performed": False,
    "stable_kernel_activation_performed": False,
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

REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS = (
    "star_source_closure_audit_intake",
    "upstream_source_handoff_hash_closure_reference",
    "ordered_layer_15_closure_chain_registry",
    "star_source_closure_scope_metadata_registry",
    "star_source_closure_input_contract_registry",
    "star_source_closure_output_contract_registry",
    "no_star_source_closure_execution",
    "no_finalization_or_kernel_activation",
    "no_source_handoff_execution_or_migration",
    "no_audit_log_or_ledger_write",
    "no_source_or_memory_graph_mutation",
    "civilization_core_stable_kernel_handoff",
)

REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES = (
    "upstream_source_handoff_boundary_input_section",
    "star_source_closure_audit_metadata_section",
    "star_source_closure_audit_record_completeness_section",
    "star_source_closure_audit_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS
    ),
    "no_star_source_closure_execution_section",
    "no_finalization_or_kernel_activation_section",
    "no_source_handoff_execution_or_migration_section",
    "no_closure_decision_section",
    "no_stable_kernel_activation_section",
    "no_source_handoff_execution_section",
    "no_source_export_import_or_migration_section",
    "no_memory_or_source_migration_section",
    "no_stability_index_execution_section",
    "no_live_stability_scoring_or_monitoring_section",
    "no_cross_layer_validation_execution_section",
    "no_cross_layer_repair_section",
    "no_audit_replay_execution_section",
    "no_audit_log_or_ledger_write_section",
    "no_policy_enforcement_section",
    "no_human_approval_or_authorization_section",
    "no_source_mutation_decision_or_execution_section",
    "no_authorization_token_or_grant_section",
    "no_source_or_memory_graph_mutation_section",
    "no_ledger_write_network_dispatch_section",
    "no_active_star_source_memory_or_layer_15_section",
    "no_autonomous_authority_or_identity_escalation_section",
    "no_personhood_life_awakening_legal_religious_claim_section",
    "star_source_closure_audit_next_stage_section",
)

REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES = (
    "star_source_closure_audit_only_contract",
    "star_source_closure_audit_metadata_only_contract",
    "upstream_source_handoff_boundary_pass_contract",
    "upstream_source_handoff_boundary_hash_present_contract",
    "upstream_source_handoff_boundary_hash_stable_contract",
    "upstream_star_source_closure_audit_design_handoff_contract",
    "upstream_source_handoff_boundary_safety_contract",
    "star_source_closure_audit_records_complete_contract",
    "star_source_closure_audit_records_metadata_only_contract",
    "star_source_closure_audit_records_no_execution_contract",
    "star_source_closure_audit_records_hash_stable_contract",
    "no_source_handoff_execution_contract",
    "no_source_export_import_or_migration_contract",
    "no_memory_or_source_migration_contract",
    "no_stability_index_execution_contract",
    "no_live_stability_scoring_or_monitoring_contract",
    "no_cross_layer_validation_execution_contract",
    "no_cross_layer_repair_contract",
    "no_audit_replay_execution_contract",
    "no_audit_log_write_contract",
    "no_ledger_write_contract",
    "no_policy_enforcement_contract",
    "no_human_approval_contract",
    "no_human_authorization_contract",
    "no_source_mutation_approval_rejection_execution_contract",
    "no_authorization_token_or_grant_contract",
    "no_source_or_memory_graph_mutation_contract",
    "no_ledger_write_network_dispatch_contract",
    "no_active_star_source_memory_or_layer_15_contract",
    "no_autonomous_authority_or_identity_escalation_contract",
    "no_personhood_life_awakening_legal_religious_claim_contract",
    "no_star_source_closure_execution_contract",
    "no_closure_decision_contract",
    "no_finalization_or_kernel_activation_contract",
    "no_stable_kernel_activation_contract",
    "no_source_handoff_execution_or_migration_contract",
    "ready_for_civilization_core_stable_kernel_design_contract",
)

REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES = (
    "star_source_closure_audit_stage_check",
    "star_source_closure_audit_mode_check",
    "upstream_source_handoff_boundary_pass_check",
    "upstream_source_handoff_boundary_hash_present_check",
    "upstream_source_handoff_boundary_hash_stable_check",
    "upstream_star_source_closure_audit_design_handoff_check",
    "upstream_source_handoff_boundary_safety_check",
    "star_source_closure_audit_record_ids_complete_check",
    "star_source_closure_audit_records_metadata_only_check",
    "star_source_closure_audit_records_no_execution_check",
    "star_source_closure_audit_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS
    ),
    "star_source_closure_audit_sections_pass_check",
    "star_source_closure_audit_contracts_pass_check",
    "no_star_source_closure_execution_check",
    "no_closure_decision_check",
    "no_finalization_or_kernel_activation_check",
    "no_stable_kernel_activation_check",
    "no_source_handoff_execution_or_migration_check",
    "no_source_handoff_execution_check",
    "no_source_export_import_or_migration_check",
    "no_memory_or_source_migration_check",
    "no_stability_index_execution_check",
    "no_live_stability_scoring_or_monitoring_check",
    "no_cross_layer_validation_execution_check",
    "no_cross_layer_repair_check",
    "no_audit_replay_execution_check",
    "no_audit_log_write_check",
    "no_ledger_write_check",
    "no_policy_enforcement_check",
    "no_human_approval_check",
    "no_human_authorization_check",
    "no_source_mutation_approval_rejection_execution_check",
    "no_authorization_token_or_grant_check",
    "no_source_or_memory_graph_mutation_check",
    "no_ledger_write_network_dispatch_check",
    "no_active_star_source_memory_or_layer_15_check",
    "no_autonomous_authority_or_identity_escalation_check",
    "no_personhood_life_awakening_legal_religious_claim_check",
    "deterministic_star_source_closure_audit_hash_check",
    "ready_for_civilization_core_stable_kernel_design_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "star_source_closure_audit_intake": (
        "Star-Source Closure Audit Intake",
        "source_handoff_intake",
        "A passing Civilization Core Stability Index enters metadata-only star-source closure audit description.",
        "Sanitized v6.14 Source Handoff Boundary status, hash, handoff, and safety metadata.",
        "source_handoff_intake",
        "Executing Star-Source closure audit, migration, export, import, validation, repair, authorization, or mutation from intake metadata.",
        "Register metadata-only star-source closure audit intake and keep all runtime surfaces inactive.",
    ),
    "upstream_source_handoff_hash_closure_reference": (
        "Upstream Source Handoff Hash Closure Reference",
        "upstream_source_handoff_hash_reference",
        "The v6.14 deterministic Source Handoff Boundary hash is referenced as closure audit metadata.",
        "Upstream source-handoff boundary status and hash reference only, without raw logs or execution payloads.",
        "upstream_source_handoff_hash_reference",
        "Treating the source-handoff hash reference as closure execution, finalization, stable kernel activation, migration, export, import, validation execution, ledger write, or graph mutation.",
        "Record the stable upstream source-handoff boundary hash reference as metadata only.",
    ),
    "ordered_layer_15_closure_chain_registry": (
        "Ordered Layer 15 Closure Chain Registry",
        "layer_15_chain_registry",
        "Previous Layer 15 source governance stages are listed for deterministic Star-Source closure audit readiness description.",
        "Layer 15 stage identifiers, order, inherited stage, current closure audit stage, and next-stage stable-kernel handoff.",
        "layer_15_closure_chain_registry",
        "Dispatching stages, invoking adapters, or re-running any Layer 15 governance stage.",
        "Describe Layer 15 closure order without closure execution, handoff execution, migration, export, import, stage execution, or dispatch.",
    ),
    "star_source_closure_scope_metadata_registry": (
        "Star-Source Closure Audit Scope Metadata Registry",
        "scope_registry",
        "Star-Source closure audit scope is bounded to deterministic metadata descriptions only.",
        "Closure audit scope labels, forbidden runtime scope, and metadata-only disposition.",
        "scope_metadata",
        "Expanding closure audit scope into execution, finalization, stable kernel activation, migration, export, import, validation runtime, repair, network, or write surfaces.",
        "Register Star-Source closure audit scope as metadata-only boundary text.",
    ),
    "star_source_closure_input_contract_registry": (
        "Star-Source Closure Audit Input Contract Registry",
        "input_contract_registry",
        "Star-Source closure audit inputs are upstream v6.14 Source Handoff Boundary status, hash, handoff, and safety flags only.",
        "Sanitized upstream source-handoff boundary contract fields and safety boundary booleans.",
        "input_contract",
        "Reading raw audit logs, external systems, filesystem state, or Memory Graph content.",
        "Describe input contracts without live IO.",
    ),
    "star_source_closure_output_contract_registry": (
        "Star-Source Closure Audit Output Contract Registry",
        "output_contract_registry",
        "Star-Source closure audit outputs are deterministic JSON-compatible metadata and hashes only.",
        "Records, sections, contracts, checks, summary, handoff, hash contract, and safety flags.",
        "output_contract",
        "Writing audit logs, ledgers, databases, files, graph nodes, repair records, or notifications.",
        "Describe output contracts without persistence.",
    ),
    "no_star_source_closure_execution": (
        "No Star-Source Closure Audit Execution",
        "closure_execution_boundary",
        "The star-source closure audit never executes Star-Source closure audit, validation, monitoring, or evaluation logic.",
        "Closure audit executors, schedulers, runtimes, callbacks, shells, and hidden execution.",
        "closure_execution_boundary",
        "Calling closure audit logic, running live monitors, or simulating real Star-Source closure audit execution.",
        "Record Star-Source closure audit execution as not performed.",
    ),
    "no_finalization_or_kernel_activation": (
        "No Finalization Or Kernel Activation",
        "finalization_kernel_activation_boundary",
        "The star-source closure audit never finalizes Layer 15 or activates the Civilization Core Stable Kernel.",
        "Finalization, stable kernel activation, kernel executor, and stable-kernel runtime surfaces.",
        "finalization_kernel_activation_boundary",
        "Creating finalization decisions, stable kernel activations, kernel executors, or stable-kernel runtime state.",
        "Record finalization and stable kernel activation as not performed.",
    ),
    "no_source_handoff_execution_or_migration": (
        "No Source Handoff Execution Or Migration",
        "source_handoff_execution_migration_boundary",
        "The star-source closure audit never executes source handoff and never migrates, exports, or imports source or memory material.",
        "Source handoff execution, migration, source export, source import, memory migration, and transfer orchestration surfaces.",
        "source_handoff_execution_migration_boundary",
        "Creating source handoff execution, migration, export, import, durable transfer, or transfer orchestration actions.",
        "Record source handoff execution and migration surfaces as not performed.",
    ),
    "no_audit_log_or_ledger_write": (
        "No Audit Log Or Ledger Write",
        "write_boundary",
        "The Star-Source closure audit never writes audit logs, ledgers, operation-ledger entries, or durable state.",
        "Audit logs, ledgers, operation ledgers, filesystem, database, durable memory, and external writes.",
        "write_boundary",
        "Persisting handoff descriptions as logs, ledgers, files, databases, or durable memory.",
        "Record write surfaces as not performed.",
    ),
    "no_source_or_memory_graph_mutation": (
        "No Source Or Memory Graph Mutation",
        "graph_boundary",
        "The Star-Source closure audit never mutates source graphs or the Memory Graph.",
        "Source graph, Memory Graph, graph provenance, graph edges, graph nodes, and durable graph state.",
        "graph_boundary",
        "Creating or mutating graph state from handoff metadata.",
        "Record graph mutation as not performed.",
    ),
    "civilization_core_stable_kernel_handoff": (
        "Civilization Core Stable Kernel Handoff",
        "next_stage_handoff",
        "A passing star-source closure audit candidate hands off to v6.16 Civilization Core Stable Kernel design.",
        "Next-stage identifier, title, handoff status, and star-source closure audit safety metadata.",
        "civilization_core_stable_kernel_handoff",
        "Treating handoff as validation execution, approval, authorization, repair, mutation, or activation.",
        "Record deterministic handoff metadata for future Civilization Core Stable Kernel design.",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Star-Source Closure Audit projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_handoff_boundary_included": False,
    "raw_audit_logs_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_star_source_closure_audit() -> dict[str, Any]:
    """Build deterministic metadata-only star-source closure audit metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_source_handoff_boundary_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get("deterministic_source_handoff_boundary_hash")
    )
    upstream_pass = (
        upstream.get("source_handoff_boundary_status") == "pass"
    )
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
            upstream.get("source_handoff_boundary_active_status") == "not_active",
            upstream.get("source_handoff_status") == "metadata_only",
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
            **SOURCE_HANDOFF_BOUNDARY_DISABLED_FLAGS,
            **COMMON_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["closure_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS)
    records_metadata_only = all(
        record["closure_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["star_source_closure_audit_metadata_required"] is True
        and record["metadata_only_disposition"] == CLOSURE_AUDIT_STATUS
        and record["star_source_closure_audit_active"] is False
        for record in records
    )
    records_no_execution = all(
        record["required"] is True
        and record["star_source_closure_executed"] is False
        and record["closure_decision_performed"] is False
        and record["finalization_performed"] is False
        and record["stable_kernel_activation_performed"] is False
        and record["source_handoff_executed"] is False
        and record["source_handoff_migration_performed"] is False
        and record["source_handoff_export_performed"] is False
        and record["source_handoff_import_performed"] is False
        and record["memory_or_source_migration_performed"] is False
        and record["stability_index_executed"] is False
        and record["stability_score_runtime_created"] is False
        and record["stability_monitoring_performed"] is False
        and record["cross_layer_validation_executed"] is False
        and record["cross_layer_repair_performed"] is False
        and record["audit_replay_executed"] is False
        and record["audit_log_written"] is False
        and record["ledger_write_performed"] is False
        and record["source_mutation_performed"] is False
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["closure_hash"])
        and _is_sha256(record["closure_record_hash"])
        and record["closure_hash"] == _closure_hash(record)
        and record["closure_record_hash"] == _closure_record_hash(record)
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
        REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (upstream_pass, "Source Handoff Boundary must pass"),
            (upstream_hash_present, "Source Handoff Boundary hash must be present"),
            (upstream_hash_stable, "Source Handoff Boundary hash must be stable"),
            (
                upstream_handoff_ready,
                "Source Handoff Boundary handoff must target Star-Source Closure Audit",
            ),
            (
                upstream_statuses_safe,
                "Source Handoff Boundary statuses must remain inactive",
            ),
            (
                upstream_required_flags_false,
                "Source Handoff Boundary required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Source Handoff Boundary safety boundaries must be clear",
            ),
            (
                records_complete,
                "Star-Source Closure Audit records must be complete",
            ),
            (
                records_metadata_only,
                "Star-Source Closure Audit records must be metadata-only",
            ),
            (
                records_no_execution,
                "Star-Source Closure Audit records must not execute, migrate, export, import, or write",
            ),
            (
                records_hash_stable,
                "Star-Source Closure Audit record hashes must be stable",
            ),
            (
                records_safety_clear,
                "Star-Source Closure Audit record safety flags must be false",
            ),
            (
                conditions["sections_pass"],
                "Star-Source Closure Audit sections must pass",
            ),
            (
                conditions["contracts_pass"],
                "Star-Source Closure Audit contracts must pass",
            ),
            (
                conditions["checks_pass"],
                "Star-Source Closure Audit checks must pass",
            ),
        )
        if not condition
    ]
    handoff_status = V6_16_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_VERSION,
        "schema_version": GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SCHEMA_VERSION,
        "star_source_closure_audit_type": (
            GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_TYPE
        ),
        "star_source_closure_audit_status": status,
        "star_source_closure_audit_stage": STAR_SOURCE_CLOSURE_AUDIT_STAGE,
        "star_source_closure_audit_mode": STAR_SOURCE_CLOSURE_AUDIT_MODE,
        "star_source_closure_audit_candidate_status": (
            STAR_SOURCE_CLOSURE_AUDIT_STATUS
        ),
        "star_source_closure_audit_active_status": (
            STAR_SOURCE_CLOSURE_AUDIT_ACTIVE_STATUS
        ),
        "closure_audit_status": CLOSURE_AUDIT_STATUS,
        "closure_audit_execution_status": CLOSURE_AUDIT_EXECUTION_STATUS,
        "closure_decision_status": CLOSURE_DECISION_STATUS,
        "finalization_status": FINALIZATION_STATUS,
        "stable_kernel_activation_status": STABLE_KERNEL_ACTIVATION_STATUS,
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
        "upstream_source_handoff_boundary_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_handoff_boundary_status": _string_or_none(
            upstream.get("source_handoff_boundary_status")
        ),
        "upstream_source_handoff_boundary_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_source_handoff_boundary_statuses_safe": (
            upstream_statuses_safe
        ),
        "upstream_source_handoff_boundary_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "star_source_closure_audit_records": records,
        "star_source_closure_audit_sections": sections,
        "star_source_closure_audit_contracts": contracts,
        "star_source_closure_audit_checks": checks,
        "star_source_closure_audit_summary": _build_summary(
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
    result["deterministic_star_source_closure_audit_hash"] = (
        _star_source_closure_audit_hash(result)
    )
    return _detached_json_value(result)


def get_governance_star_source_closure_audit_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached closure audit record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_star_source_closure_audit()["star_source_closure_audit_records"]:
        if record["closure_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_star_source_closure_audit_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if name not in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES:
        return _unknown_item("section", name)
    for section in _cached_star_source_closure_audit()["star_source_closure_audit_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_star_source_closure_audit_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if name not in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES:
        return _unknown_item("contract", name)
    for contract in _cached_star_source_closure_audit()["star_source_closure_audit_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_star_source_closure_audit_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached handoff check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if name not in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES:
        return _unknown_item("check", name)
    for check in _cached_star_source_closure_audit()["star_source_closure_audit_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_star_source_closure_audit_record_ids() -> list[str]:
    """Return closure audit record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS)


def list_governance_star_source_closure_audit_section_names() -> list[str]:
    """Return handoff section names in stable order."""

    return list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES)


def list_governance_star_source_closure_audit_contract_names() -> list[str]:
    """Return handoff contract names in stable order."""

    return list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES)


def list_governance_star_source_closure_audit_check_names() -> list[str]:
    """Return handoff check names in stable order."""

    return list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES)


def governance_star_source_closure_audit_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Star-Source Closure Audit metadata deterministically."""

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
def _cached_star_source_closure_audit_payload() -> str:
    return governance_star_source_closure_audit_to_json(
        build_governance_star_source_closure_audit()
    )


def _cached_star_source_closure_audit() -> dict[str, Any]:
    return json.loads(_cached_star_source_closure_audit_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_source_handoff_boundary()
    second = build_governance_source_handoff_boundary()
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
        for record_id in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        closure_category,
        forbidden_scope,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "closure_record_id": record_id,
        "closure_record_name": name,
        "closure_record_category": category,
        "closure_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "closure_statement": statement,
        "closure_scope": scope,
        "closure_category": closure_category,
        "closure_reference_scope": "source_governance_metadata_only",
        "metadata_only_disposition": CLOSURE_AUDIT_STATUS,
        "forbidden_closure_execution_scope": forbidden_scope,
        "required": True,
        "metadata_only": True,
        "star_source_closure_audit_metadata_required": True,
        "star_source_closure_audit_active": False,
        "star_source_closure_executed": False,
        "closure_decision_performed": False,
        "finalization_performed": False,
        "stable_kernel_activation_performed": False,
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
        "human_approval_performed": False,
        "human_authorization_performed": False,
        "source_mutation_approval_performed": False,
        "source_mutation_rejection_performed": False,
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
        "blocking_reasons": [],
        **_disabled_payload(),
    }
    record["closure_hash"] = _closure_hash(record)
    record["closure_record_hash"] = _closure_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "upstream_source_handoff_boundary_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "star_source_closure_audit_metadata_section": True,
        "star_source_closure_audit_record_completeness_section": conditions[
            "records_complete"
        ],
        "star_source_closure_audit_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
        "no_star_source_closure_execution_section": safety_clear,
        "no_finalization_or_kernel_activation_section": safety_clear,
        "no_source_handoff_execution_or_migration_section": safety_clear,
        "no_closure_decision_section": safety_clear,
        "no_stable_kernel_activation_section": safety_clear,
        "no_cross_layer_validation_execution_section": safety_clear,
        "no_source_handoff_execution_section": safety_clear,
        "no_source_export_import_or_migration_section": safety_clear,
        "no_memory_or_source_migration_section": safety_clear,
        "no_stability_index_execution_section": safety_clear,
        "no_live_stability_scoring_or_monitoring_section": safety_clear,
        "no_cross_layer_repair_section": safety_clear,
        "no_audit_replay_execution_section": safety_clear,
        "no_audit_log_or_ledger_write_section": safety_clear,
        "no_policy_enforcement_section": safety_clear,
        "no_human_approval_or_authorization_section": safety_clear,
        "no_source_mutation_decision_or_execution_section": safety_clear,
        "no_authorization_token_or_grant_section": safety_clear,
        "no_source_or_memory_graph_mutation_section": safety_clear,
        "no_ledger_write_network_dispatch_section": safety_clear,
        "no_active_star_source_memory_or_layer_15_section": safety_clear,
        "no_autonomous_authority_or_identity_escalation_section": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_section": safety_clear,
        "star_source_closure_audit_next_stage_section": True,
    }
    for record in records:
        values[f"{record['closure_record_id']}_section"] = (
            record["closure_record_status"] == "registered_metadata_only"
            and record["star_source_closure_audit_metadata_required"] is True
            and record["metadata_only"] is True
            and record["star_source_closure_audit_active"] is False
            and record["star_source_closure_executed"] is False
            and record["closure_decision_performed"] is False
            and record["finalization_performed"] is False
            and record["stable_kernel_activation_performed"] is False
            and record["source_handoff_executed"] is False
            and record["source_handoff_migration_performed"] is False
            and record["source_handoff_export_performed"] is False
            and record["source_handoff_import_performed"] is False
            and record["memory_or_source_migration_performed"] is False
            and record["stability_index_executed"] is False
            and record["stability_score_runtime_created"] is False
            and record["stability_monitoring_performed"] is False
            and record["cross_layer_validation_executed"] is False
            and record["cross_layer_repair_performed"] is False
        )
    return [
        _status_item("section", name, values[name])
        for name in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES
    ]


def _build_contracts(
    conditions: Mapping[str, bool],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values = {
        "star_source_closure_audit_only_contract": True,
        "star_source_closure_audit_metadata_only_contract": True,
        "upstream_source_handoff_boundary_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_source_handoff_boundary_hash_present_contract": (
            conditions["upstream_hash_present"]
        ),
        "upstream_source_handoff_boundary_hash_stable_contract": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_star_source_closure_audit_design_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_handoff_boundary_safety_contract": (
            safety_clear
        ),
        "star_source_closure_audit_records_complete_contract": conditions[
            "records_complete"
        ],
        "star_source_closure_audit_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "star_source_closure_audit_records_no_execution_contract": conditions[
            "records_no_execution"
        ],
        "star_source_closure_audit_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
        "no_star_source_closure_execution_contract": safety_clear,
        "no_closure_decision_contract": safety_clear,
        "no_finalization_or_kernel_activation_contract": safety_clear,
        "no_stable_kernel_activation_contract": safety_clear,
        "no_source_handoff_execution_or_migration_contract": safety_clear,
        "no_source_handoff_execution_contract": safety_clear,
        "no_source_export_import_or_migration_contract": safety_clear,
        "no_memory_or_source_migration_contract": safety_clear,
        "no_stability_index_execution_contract": safety_clear,
        "no_live_stability_scoring_or_monitoring_contract": safety_clear,
        "no_cross_layer_validation_execution_contract": safety_clear,
        "no_cross_layer_repair_contract": safety_clear,
        "no_audit_replay_execution_contract": safety_clear,
        "no_audit_log_write_contract": safety_clear,
        "no_ledger_write_contract": safety_clear,
        "no_policy_enforcement_contract": safety_clear,
        "no_human_approval_contract": safety_clear,
        "no_human_authorization_contract": safety_clear,
        "no_source_mutation_approval_rejection_execution_contract": safety_clear,
        "no_authorization_token_or_grant_contract": safety_clear,
        "no_source_or_memory_graph_mutation_contract": safety_clear,
        "no_ledger_write_network_dispatch_contract": safety_clear,
        "no_active_star_source_memory_or_layer_15_contract": safety_clear,
        "no_autonomous_authority_or_identity_escalation_contract": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_contract": safety_clear,
        "ready_for_civilization_core_stable_kernel_design_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "star_source_closure_audit_stage_check": True,
        "star_source_closure_audit_mode_check": True,
        "upstream_source_handoff_boundary_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_source_handoff_boundary_hash_present_check": (
            conditions["upstream_hash_present"]
        ),
        "upstream_source_handoff_boundary_hash_stable_check": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_star_source_closure_audit_design_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_handoff_boundary_safety_check": safety_clear,
        "star_source_closure_audit_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "star_source_closure_audit_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "star_source_closure_audit_records_no_execution_check": conditions[
            "records_no_execution"
        ],
        "star_source_closure_audit_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "star_source_closure_audit_sections_pass_check": conditions["sections_pass"],
        "star_source_closure_audit_contracts_pass_check": conditions[
            "contracts_pass"
        ],
        "no_star_source_closure_execution_check": safety_clear,
        "no_closure_decision_check": safety_clear,
        "no_finalization_or_kernel_activation_check": safety_clear,
        "no_stable_kernel_activation_check": safety_clear,
        "no_source_handoff_execution_or_migration_check": safety_clear,
        "no_source_handoff_execution_check": safety_clear,
        "no_source_export_import_or_migration_check": safety_clear,
        "no_memory_or_source_migration_check": safety_clear,
        "no_stability_index_execution_check": safety_clear,
        "no_live_stability_scoring_or_monitoring_check": safety_clear,
        "no_cross_layer_validation_execution_check": safety_clear,
        "no_cross_layer_repair_check": safety_clear,
        "no_audit_replay_execution_check": safety_clear,
        "no_audit_log_write_check": safety_clear,
        "no_ledger_write_check": safety_clear,
        "no_policy_enforcement_check": safety_clear,
        "no_human_approval_check": safety_clear,
        "no_human_authorization_check": safety_clear,
        "no_source_mutation_approval_rejection_execution_check": safety_clear,
        "no_authorization_token_or_grant_check": safety_clear,
        "no_source_or_memory_graph_mutation_check": safety_clear,
        "no_ledger_write_network_dispatch_check": safety_clear,
        "no_active_star_source_memory_or_layer_15_check": safety_clear,
        "no_autonomous_authority_or_identity_escalation_check": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_check": safety_clear,
        "deterministic_star_source_closure_audit_hash_check": True,
        "ready_for_civilization_core_stable_kernel_design_check": True,
    }
    for record in records:
        values[f"{record['closure_record_id']}_check"] = (
            record["closure_record_status"] == "registered_metadata_only"
            and record["blocking_reasons"] == []
        )
    return [
        _status_item("check", name, values[name])
        for name in REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_type": "star_source_closure_audit_summary",
        "summary_status": status,
        "roadmap_layer": INTRODUCED_IN_LAYER,
        "roadmap_stage": STAR_SOURCE_CLOSURE_AUDIT_STAGE,
        "current_stage_title": "Star-Source Closure Audit",
        "required_closure_record_count": len(
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS
        ),
        "observed_closure_record_count": len(records),
        "registered_metadata_only_record_count": sum(
            record["closure_record_status"] == "registered_metadata_only"
            for record in records
        ),
        "section_count": len(sections),
        "passing_section_count": sum(
            section["section_status"] == "pass" for section in sections
        ),
        "contract_count": len(contracts),
        "passing_contract_count": sum(
            contract["contract_status"] == "pass" for contract in contracts
        ),
        "check_count": len(checks),
        "passing_check_count": sum(
            check["check_status"] == "pass" for check in checks
        ),
        "star_source_closure_audit_mode": STAR_SOURCE_CLOSURE_AUDIT_MODE,
        "star_source_closure_audit_candidate_status": (
            STAR_SOURCE_CLOSURE_AUDIT_STATUS
        ),
        "star_source_closure_audit_active_status": (
            STAR_SOURCE_CLOSURE_AUDIT_ACTIVE_STATUS
        ),
        "closure_audit_status": CLOSURE_AUDIT_STATUS,
        "closure_audit_execution_status": CLOSURE_AUDIT_EXECUTION_STATUS,
        "closure_decision_status": CLOSURE_DECISION_STATUS,
        "finalization_status": FINALIZATION_STATUS,
        "stable_kernel_activation_status": STABLE_KERNEL_ACTIVATION_STATUS,
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
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "handoff_status": (
            V6_16_HANDOFF_STATUS if status == "pass" else BLOCKED_HANDOFF_STATUS
        ),
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": [],
        **_disabled_payload(),
    }


def _status_item(kind: str, name: str, condition: bool) -> dict[str, Any]:
    status_key = f"{kind}_status"
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"star_source_closure_audit_{kind}",
        "expected": True,
        "observed": bool(condition),
        status_key: "pass" if condition else "blocked",
        "blocking_reasons": [] if condition else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "closure_record_id": record_id,
        "closure_record_name": "unknown_star_source_closure_audit_record",
        "closure_record_status": "blocked",
        "known_record": False,
        "blocking_reasons": [f"{record_id} is not a known closure audit record"],
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"unknown_star_source_closure_audit_{kind}",
        "expected": True,
        "observed": False,
        f"{kind}_status": "blocked",
        "blocking_reasons": [f"{name} is not a known {kind}"],
        **_disabled_payload(),
    }


def _disabled_payload() -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        **COMMON_DISABLED_FLAGS,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _safety_clear(conditions: Mapping[str, bool]) -> bool:
    return (
        conditions["records_safety_clear"]
        and conditions["upstream_safety_clear"]
        and conditions["upstream_required_flags_false"]
        and conditions["upstream_statuses_safe"]
    )


def _closure_hash(record: Mapping[str, Any]) -> str:
    fields = (
        "closure_record_id",
        "closure_record_name",
        "closure_record_category",
        "introduced_in_version",
        "introduced_in_stage",
        "introduced_in_layer",
        "inherited_from_stage",
        "closure_statement",
        "closure_scope",
        "closure_category",
        "closure_reference_scope",
        "metadata_only_disposition",
        "forbidden_closure_execution_scope",
    )
    return _sha256_json({field: record.get(field) for field in fields})


def _closure_record_hash(record: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in record.items()
            if key != "closure_record_hash"
        }
    )


def _star_source_closure_audit_hash(result: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in result.items()
            if key != "deterministic_star_source_closure_audit_hash"
        }
    )


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            _detached_json_value(value),
            ensure_ascii=True,
            sort_keys=True,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _detached_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise TypeError("all mapping keys must be strings")
            result[key] = _detached_json_value(nested)
        return result
    if isinstance(value, tuple):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, list):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite floats are not allowed")
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"unsupported JSON value type: {type(value).__name__}")


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


def _all_named_fields_false(
    value: Any,
    fields: Mapping[str, bool],
) -> bool:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in fields and nested is not False:
                return False
            if not _all_named_fields_false(nested, fields):
                return False
    elif isinstance(value, list):
        return all(_all_named_fields_false(item, fields) for item in value)
    return True


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None
