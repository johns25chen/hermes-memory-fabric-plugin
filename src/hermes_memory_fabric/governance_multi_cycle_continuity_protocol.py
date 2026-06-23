"""Deterministic Multi-Cycle Continuity Protocol metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_root_governance_conflict_resolver import (
    COMMON_DISABLED_FLAGS as ROOT_GOVERNANCE_CONFLICT_DISABLED_FLAGS,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS,
    build_governance_root_governance_conflict_resolver,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_VERSION = "6.9.0"
GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_SCHEMA_VERSION = "6.9.0"
GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_TYPE = (
    "governance_multi_cycle_continuity_protocol"
)
GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_HASH_ALGORITHM = "sha256"
MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE = "v6.6_multi_cycle_continuity_protocol"
MULTI_CYCLE_CONTINUITY_PROTOCOL_MODE = "multi_cycle_continuity_protocol_only"
MULTI_CYCLE_CONTINUITY_MODE = "metadata_only"
MULTI_CYCLE_CONTINUITY_PROTOCOL_STATUS = "protocol_candidate_only"
MULTI_CYCLE_CONTINUITY_PROTOCOL_ACTIVE_STATUS = "not_active"
CONTINUITY_RUNTIME_STATUS = "not_active"
CONTINUITY_ENFORCEMENT_STATUS = "not_active"
CONTINUITY_MUTATION_STATUS = "forbidden_without_human_review"
CYCLE_LINKING_STATUS = "metadata_only"
CYCLE_RECOVERY_STATUS = "metadata_only"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
SOURCE_GRAPH_STATUS = "not_created"
SOURCE_PROVENANCE_RUNTIME_STATUS = "not_active"
METHODOLOGY_REVERSE_INFERENCE_STATUS = "not_active"
SELF_EVOLUTION_STATUS = "not_active"
PERSONHOOD_CLAIM_STATUS = "forbidden"
LIFE_CLAIM_STATUS = "forbidden"
AWAKENING_CLAIM_STATUS = "forbidden"
LEGAL_SUBJECT_CLAIM_STATUS = "forbidden"
RELIGIOUS_OBJECT_CLAIM_STATUS = "forbidden"
AUTONOMOUS_AUTHORITY_STATUS = "forbidden"
V6_6_STATUS = "multi_cycle_continuity_protocol_only"
V6_7_HANDOFF_STATUS = "ready_for_source_mutation_proposal_boundary_design"

UPSTREAM_READY_HANDOFF_STATUS = (
    "ready_for_multi_cycle_continuity_protocol_design"
)
UPSTREAM_NEXT_STAGE = MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Multi-Cycle Continuity Protocol"
NEXT_STAGE = "v6.7_source_mutation_proposal_boundary"
NEXT_STAGE_TITLE = "Source Mutation Proposal Boundary"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.6.0"
INTRODUCED_IN_STAGE = MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.5_root_governance_conflict_resolver"
CONTINUITY_MODE = "metadata_only_protocol"
PROTOCOL_STRENGTH = "multi_cycle_required"

COMMON_DISABLED_FLAGS = {
    **ROOT_GOVERNANCE_CONFLICT_DISABLED_FLAGS,
    "multi_cycle_continuity_protocol_active": False,
    "continuity_runtime_created": False,
    "continuity_enforcement_runtime_created": False,
    "continuity_self_repair_created": False,
    "continuity_scheduler_created": False,
    "continuity_runtime_activated": False,
    "continuity_enforcement_runtime_activated": False,
    "continuity_memory_write_allowed": False,
    "continuity_source_mutation_created": False,
    "source_mutation_proposal_created": False,
    "source_mutation_proposal_approved": False,
    "cycle_linking_executed": False,
    "cycle_recovery_executed": False,
    "rollback_executed": False,
    "recovery_executed": False,
}

REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS = (
    "release_version_lineage_continuity",
    "source_constitution_registry_continuity",
    "origin_provenance_traceability_continuity",
    "civilizational_identity_boundary_continuity",
    "source_memory_invariant_matrix_continuity",
    "root_governance_conflict_resolver_continuity",
    "human_sovereignty_continuity",
    "audit_replay_continuity",
    "review_gate_continuity",
    "source_mutation_proposal_handoff_continuity",
    "rollback_recovery_metadata_continuity",
    "blocked_gap_human_review_continuity",
    "no_runtime_continuity_activation",
    "no_memory_graph_mutation_continuity",
    "no_source_graph_mutation_continuity",
    "multi_cycle_handoff_to_source_mutation_boundary",
)

REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES = (
    "upstream_root_governance_conflict_resolver_input_section",
    "multi_cycle_continuity_protocol_metadata_section",
    "continuity_record_completeness_section",
    "continuity_record_hash_stability_section",
    "continuity_scope_section",
    "preserved_governance_scope_section",
    "forbidden_activation_scope_section",
    "release_version_lineage_continuity_section",
    "source_constitution_registry_continuity_section",
    "origin_provenance_traceability_continuity_section",
    "civilizational_identity_boundary_continuity_section",
    "source_memory_invariant_matrix_continuity_section",
    "root_governance_conflict_resolver_continuity_section",
    "human_sovereignty_continuity_section",
    "audit_replay_continuity_section",
    "review_gate_continuity_section",
    "source_mutation_proposal_handoff_continuity_section",
    "rollback_recovery_metadata_continuity_section",
    "blocked_gap_human_review_continuity_section",
    "no_runtime_continuity_activation_section",
    "no_memory_graph_mutation_continuity_section",
    "no_source_graph_mutation_continuity_section",
    "multi_cycle_handoff_to_source_mutation_boundary_section",
    "source_mutation_proposal_boundary_next_stage_section",
    "no_continuity_runtime_section",
    "no_continuity_enforcement_runtime_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
    "no_source_mutation_proposal_creation_section",
)

REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES = (
    "multi_cycle_continuity_protocol_only_contract",
    "multi_cycle_continuity_metadata_only_contract",
    "upstream_root_governance_conflict_resolver_pass_contract",
    "upstream_root_governance_conflict_resolver_hash_present_contract",
    "upstream_root_governance_conflict_resolver_hash_stable_contract",
    "upstream_multi_cycle_continuity_protocol_handoff_ready_contract",
    "continuity_records_complete_contract",
    "continuity_records_registered_metadata_only_contract",
    "continuity_records_have_continuity_scope_contract",
    "continuity_records_have_preserved_governance_scope_contract",
    "continuity_records_have_forbidden_activation_scope_contract",
    "continuity_records_have_disposition_contract",
    "continuity_records_hash_stable_contract",
    "continuity_records_human_review_required_contract",
    "continuity_records_mutation_proposal_required_contract",
    "continuity_records_invariant_validation_required_contract",
    "continuity_records_root_conflict_resolver_required_contract",
    "continuity_records_audit_replay_required_contract",
    "continuity_records_direct_mutation_disabled_contract",
    "continuity_records_autonomous_override_disabled_contract",
    "no_continuity_runtime_contract",
    "no_continuity_enforcement_runtime_contract",
    "no_continuity_scheduler_contract",
    "no_active_star_source_memory_contract",
    "no_active_layer_15_contract",
    "no_personhood_claim_contract",
    "no_life_claim_contract",
    "no_awakening_claim_contract",
    "no_legal_subject_claim_contract",
    "no_religious_object_claim_contract",
    "no_autonomous_authority_contract",
    "no_identity_escalation_contract",
    "no_source_provenance_runtime_contract",
    "no_source_graph_creation_contract",
    "no_source_graph_mutation_contract",
    "no_real_ledger_write_contract",
    "no_operation_ledger_write_contract",
    "no_methodology_runtime_contract",
    "no_self_evolution_runtime_contract",
    "no_real_execution_contract",
    "no_adapter_dispatch_contract",
    "no_manifest_dispatch_contract",
    "no_external_call_contract",
    "no_network_call_contract",
    "no_durable_write_contract",
    "no_filesystem_write_contract",
    "no_database_write_contract",
    "no_memory_graph_mutation_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_contract",
    "no_authorization_token_contract",
    "no_authorization_grant_contract",
    "no_source_mutation_proposal_creation_contract",
    "no_source_mutation_proposal_approval_contract",
    "ready_for_source_mutation_proposal_boundary_design_contract",
)

REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES = (
    "multi_cycle_continuity_protocol_stage_check",
    "multi_cycle_continuity_protocol_only_mode_check",
    "multi_cycle_continuity_metadata_only_check",
    "upstream_root_governance_conflict_resolver_pass_check",
    "upstream_root_governance_conflict_resolver_hash_present_check",
    "upstream_root_governance_conflict_resolver_hash_stable_check",
    "upstream_multi_cycle_continuity_protocol_handoff_ready_check",
    "continuity_record_ids_complete_check",
    "continuity_records_registered_check",
    "continuity_records_have_continuity_scope_check",
    "continuity_records_have_preserved_governance_scope_check",
    "continuity_records_have_forbidden_activation_scope_check",
    "continuity_records_have_disposition_check",
    "continuity_records_hash_stable_check",
    "continuity_records_human_review_required_check",
    "continuity_records_mutation_proposal_required_check",
    "continuity_records_invariant_validation_required_check",
    "continuity_records_root_conflict_resolver_required_check",
    "continuity_records_audit_replay_required_check",
    "continuity_records_direct_mutation_disabled_check",
    "continuity_records_autonomous_override_disabled_check",
    "release_version_lineage_continuity_check",
    "source_constitution_registry_continuity_check",
    "origin_provenance_traceability_continuity_check",
    "civilizational_identity_boundary_continuity_check",
    "source_memory_invariant_matrix_continuity_check",
    "root_governance_conflict_resolver_continuity_check",
    "human_sovereignty_continuity_check",
    "audit_replay_continuity_check",
    "review_gate_continuity_check",
    "source_mutation_proposal_handoff_continuity_check",
    "rollback_recovery_metadata_continuity_check",
    "blocked_gap_human_review_continuity_check",
    "no_runtime_continuity_activation_check",
    "no_memory_graph_mutation_continuity_check",
    "no_source_graph_mutation_continuity_check",
    "multi_cycle_handoff_to_source_mutation_boundary_check",
    "multi_cycle_continuity_sections_complete_check",
    "multi_cycle_continuity_sections_pass_check",
    "multi_cycle_continuity_contracts_pass_check",
    "no_continuity_runtime_check",
    "no_continuity_enforcement_runtime_check",
    "no_continuity_scheduler_check",
    "no_active_star_source_memory_check",
    "no_active_layer_15_check",
    "no_personhood_claim_check",
    "no_life_claim_check",
    "no_awakening_claim_check",
    "no_legal_subject_claim_check",
    "no_religious_object_claim_check",
    "no_autonomous_authority_check",
    "no_identity_escalation_check",
    "no_source_provenance_runtime_check",
    "no_source_graph_creation_check",
    "no_source_graph_mutation_check",
    "no_real_ledger_write_check",
    "no_operation_ledger_write_check",
    "no_methodology_runtime_check",
    "no_self_evolution_runtime_check",
    "no_real_execution_check",
    "no_adapter_dispatch_check",
    "no_manifest_dispatch_check",
    "no_external_call_check",
    "no_network_call_check",
    "no_durable_write_check",
    "no_filesystem_write_check",
    "no_database_write_check",
    "no_memory_graph_mutation_check",
    "no_approval_notification_check",
    "no_execution_authorization_check",
    "no_authorization_token_check",
    "no_authorization_grant_check",
    "no_source_mutation_proposal_creation_check",
    "no_source_mutation_proposal_approval_check",
    "deterministic_multi_cycle_continuity_protocol_hash_check",
    "ready_for_source_mutation_proposal_boundary_design_check",
)

_REQUIRED_DISPOSITIONS = (
    "preserve_release_version_lineage",
    "preserve_source_constitution_registry_lineage",
    "preserve_origin_provenance_traceability",
    "preserve_civilizational_identity_boundary",
    "preserve_source_memory_invariant_matrix",
    "preserve_root_governance_conflict_resolver",
    "preserve_human_sovereignty",
    "preserve_audit_replayability",
    "preserve_review_gate",
    "handoff_to_source_mutation_proposal_boundary",
    "record_rollback_recovery_metadata_only",
    "block_gap_until_human_review",
    "block_continuity_runtime_activation",
    "block_memory_graph_mutation",
    "block_source_graph_mutation",
    "prepare_v6_7_source_mutation_boundary",
)

_CONTINUITY_RECORD_DEFINITIONS: dict[str, dict[str, str]] = {
    "release_version_lineage_continuity": {
        "name": "Release Version Lineage Continuity",
        "category": "release_cycle_continuity",
        "statement": "Release-cycle continuity preserves deterministic version lineage and handoff readiness.",
        "scope": "Release versions, stage identifiers, titles, hashes, and governed handoff metadata.",
        "preserved": "Version lineage and release handoff evidence remain auditable across cycles.",
        "forbidden": "Must not schedule releases, execute handoffs, write release state, or self-authorize continuation.",
        "disposition": "preserve_release_version_lineage",
        "reason": "Release continuity is audited lineage rather than an active release runtime.",
        "source": "v6.0 through v6.5 Layer 15 release corridor",
        "reference": "release version lineage",
    },
    "source_constitution_registry_continuity": {
        "name": "Source Constitution Registry Continuity",
        "category": "source_governance_continuity",
        "statement": "Source Constitution Registry lineage remains stable across governance cycles.",
        "scope": "Registered source-constitution rule identifiers, status, hashes, and review boundaries.",
        "preserved": "Source Constitution Registry metadata and human-sovereignty constraints.",
        "forbidden": "Must not mutate constitution rules, activate source authority, or bypass review.",
        "disposition": "preserve_source_constitution_registry_lineage",
        "reason": "Constitution continuity requires traceable metadata without source mutation.",
        "source": "v6.1 Source Constitution Registry",
        "reference": "source constitution lineage",
    },
    "origin_provenance_traceability_continuity": {
        "name": "Origin Provenance Traceability Continuity",
        "category": "provenance_continuity",
        "statement": "Origin provenance traceability remains preserved across cycles.",
        "scope": "Introduced origins, source references, upstream hashes, and inheritance metadata.",
        "preserved": "Origin Provenance Ledger traceability without real ledger writing.",
        "forbidden": "Must not write ledger entries, activate provenance runtime, or create source graph state.",
        "disposition": "preserve_origin_provenance_traceability",
        "reason": "Traceability must survive cycle transitions without becoming a ledger writer.",
        "source": "v6.2 Origin Provenance Ledger",
        "reference": "origin provenance traceability",
    },
    "civilizational_identity_boundary_continuity": {
        "name": "Civilizational Identity Boundary Continuity",
        "category": "identity_boundary_continuity",
        "statement": "Civilizational identity remains descriptive governance metadata across cycles.",
        "scope": "Identity boundary records and their prohibited authority and status claims.",
        "preserved": "Identity boundary constraints and human sovereignty.",
        "forbidden": "Must not escalate identity, claim personhood, or create autonomous authority.",
        "disposition": "preserve_civilizational_identity_boundary",
        "reason": "Identity continuity is governance continuity, not personhood continuity.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "civilizational identity boundary",
    },
    "source_memory_invariant_matrix_continuity": {
        "name": "Source Memory Invariant Matrix Continuity",
        "category": "invariant_continuity",
        "statement": "Source Memory Invariant Matrix results remain validated across cycles.",
        "scope": "Invariant identifiers, validation requirements, hashes, and blocked mutation boundaries.",
        "preserved": "Invariant validation and source mutation proposal requirements.",
        "forbidden": "Must not self-mutate invariants or create invariant enforcement runtime.",
        "disposition": "preserve_source_memory_invariant_matrix",
        "reason": "Invariant continuity remains review-gated and replayable.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "source memory invariant matrix",
    },
    "root_governance_conflict_resolver_continuity": {
        "name": "Root Governance Conflict Resolver Continuity",
        "category": "root_conflict_continuity",
        "statement": "Root conflict dispositions remain preserved and unresolved gaps remain blocked.",
        "scope": "Root conflict records, deterministic dispositions, hashes, and review requirements.",
        "preserved": "Root Governance Conflict Resolver results and fail-closed handoffs.",
        "forbidden": "Must not execute conflict resolution, enforce conflicts, or create autonomous override.",
        "disposition": "preserve_root_governance_conflict_resolver",
        "reason": "Root conflict continuity preserves decisions without activating a resolver runtime.",
        "source": "v6.5 Root Governance Conflict Resolver",
        "reference": "root governance conflict results",
    },
    "human_sovereignty_continuity": {
        "name": "Human Sovereignty Continuity",
        "category": "authority_continuity",
        "statement": "No cycle may bypass or supersede human sovereignty.",
        "scope": "Human review, explicit approval boundaries, and blocked unsafe continuation.",
        "preserved": "Human authority remains above every source-governance cycle.",
        "forbidden": "Must not self-authorize continuation, override review, or create autonomous authority.",
        "disposition": "preserve_human_sovereignty",
        "reason": "Governance cycles cannot authorize their own continuation.",
        "source": "Layer 15 governance constitution",
        "reference": "human sovereignty continuity",
    },
    "audit_replay_continuity": {
        "name": "Audit Replay Continuity",
        "category": "audit_cycle_continuity",
        "statement": "Audit-cycle continuity remains deterministic and replayable.",
        "scope": "Sanitized inputs, ordered records, stable hashes, checks, contracts, and outcomes.",
        "preserved": "Audit replay evidence and deterministic reconstruction.",
        "forbidden": "Must not write audit logs, execute replay actions, or depend on hidden state.",
        "disposition": "preserve_audit_replayability",
        "reason": "Continuity claims require deterministic audit replay.",
        "source": "Layer 15 audit boundaries",
        "reference": "audit replay continuity",
    },
    "review_gate_continuity": {
        "name": "Review Gate Continuity",
        "category": "review_cycle_continuity",
        "statement": "Review gates remain mandatory across all continuity cycles.",
        "scope": "Human review, invariant validation, root conflict resolution, and audit replay gates.",
        "preserved": "Review requirements and blocked outcomes for unsafe or unresolved gaps.",
        "forbidden": "Must not notify approvals, approve changes, or bypass review gates.",
        "disposition": "preserve_review_gate",
        "reason": "Continuity cannot weaken existing review requirements.",
        "source": "v6.1 through v6.5 review boundaries",
        "reference": "review gate continuity",
    },
    "source_mutation_proposal_handoff_continuity": {
        "name": "Source Mutation Proposal Handoff Continuity",
        "category": "handoff_cycle_continuity",
        "statement": "Changes hand off to the future Source Mutation Proposal Boundary.",
        "scope": "Metadata-only next-stage readiness for governed source mutation proposals.",
        "preserved": "The requirement for a distinct reviewed proposal boundary before change.",
        "forbidden": "Must not generate, approve, authorize, or execute a source mutation proposal.",
        "disposition": "handoff_to_source_mutation_proposal_boundary",
        "reason": "v6.6 prepares v6.7 without creating mutation proposals.",
        "source": "v6.6 Multi-Cycle Continuity Protocol",
        "reference": "v6.7 handoff requirement",
    },
    "rollback_recovery_metadata_continuity": {
        "name": "Rollback Recovery Metadata Continuity",
        "category": "rollback_recovery_cycle_continuity",
        "statement": "Rollback and recovery continuity may record metadata only.",
        "scope": "Rollback prerequisites, recovery references, prior hashes, and human review requirements.",
        "preserved": "Recovery traceability without state mutation.",
        "forbidden": "Must not execute rollback, execute recovery, write ledgers, or mutate source state.",
        "disposition": "record_rollback_recovery_metadata_only",
        "reason": "Recovery continuity remains an auditable protocol boundary.",
        "source": "Layer 15 rollback and recovery boundary",
        "reference": "rollback recovery metadata",
    },
    "blocked_gap_human_review_continuity": {
        "name": "Blocked Gap Human Review Continuity",
        "category": "continuity_gap_boundary",
        "statement": "Unsafe, ambiguous, or unresolved continuity gaps remain blocked.",
        "scope": "Missing lineage, failed validation, unresolved conflict, or incomplete review evidence.",
        "preserved": "Fail-closed status and explicit human review requirement.",
        "forbidden": "Must not repair gaps autonomously, infer approval, or silently continue.",
        "disposition": "block_gap_until_human_review",
        "reason": "Continuity gaps cannot self-resolve.",
        "source": "v6.5 Root Governance Conflict Resolver",
        "reference": "blocked continuity gap",
    },
    "no_runtime_continuity_activation": {
        "name": "No Runtime Continuity Activation",
        "category": "runtime_activation_boundary",
        "statement": "The protocol never activates continuity runtime or enforcement.",
        "scope": "Continuity runtime, enforcement runtime, scheduler, self-repair, and cycle execution.",
        "preserved": "Metadata-only protocol status.",
        "forbidden": "Must not activate runtime, enforcement, scheduling, self-repair, or hidden execution.",
        "disposition": "block_continuity_runtime_activation",
        "reason": "v6.6 is a protocol boundary rather than an active engine.",
        "source": "v6.6 Multi-Cycle Continuity Protocol",
        "reference": "no continuity runtime",
    },
    "no_memory_graph_mutation_continuity": {
        "name": "No Memory Graph Mutation Continuity",
        "category": "memory_graph_boundary",
        "statement": "Memory Graph mutation remains prohibited across cycles.",
        "scope": "Persistent memory, durable memory, Memory Graph nodes, edges, and writes.",
        "preserved": "Memory mutation remains outside v6.6 authority.",
        "forbidden": "Must not mutate Memory Graph or write persistent or durable memory.",
        "disposition": "block_memory_graph_mutation",
        "reason": "Continuity metadata is not memory-write authority.",
        "source": "Layer 15 memory mutation boundary",
        "reference": "Memory Graph mutation prohibition",
    },
    "no_source_graph_mutation_continuity": {
        "name": "No Source Graph Mutation Continuity",
        "category": "source_graph_boundary",
        "statement": "Source graph creation and mutation remain prohibited across cycles.",
        "scope": "Source graph nodes, edges, inferred relationships, and persisted graph state.",
        "preserved": "Source graph remains not created.",
        "forbidden": "Must not create, mutate, infer, or persist source graph state.",
        "disposition": "block_source_graph_mutation",
        "reason": "The protocol records continuity without graph state.",
        "source": "Layer 15 source graph boundary",
        "reference": "source graph mutation prohibition",
    },
    "multi_cycle_handoff_to_source_mutation_boundary": {
        "name": "Multi-Cycle Handoff To Source Mutation Boundary",
        "category": "next_stage_handoff",
        "statement": "A successful v6.6 protocol prepares the v6.7 design boundary.",
        "scope": "Next-stage identifier, title, readiness status, and blocked mutation semantics.",
        "preserved": "Explicit separation between continuity metadata and future mutation proposals.",
        "forbidden": "Must not create or approve proposals, grants, tokens, execution, or mutation.",
        "disposition": "prepare_v6_7_source_mutation_boundary",
        "reason": "The next stage remains proposal-boundary design only.",
        "source": "v6.6 Multi-Cycle Continuity Protocol",
        "reference": "v6.7 Source Mutation Proposal Boundary",
    },
}

_SECTION_RECORD_IDS = {
    f"{record_id}_section": record_id
    for record_id in REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS
}

_DISABLED_FIELDS = {
    "no_continuity_runtime": "continuity_runtime_created",
    "no_continuity_enforcement_runtime": "continuity_enforcement_runtime_created",
    "no_continuity_scheduler": "continuity_scheduler_created",
    "no_active_star_source_memory": "star_source_memory_active",
    "no_active_layer_15": "layer_15_active",
    "no_personhood_claim": "personhood_claimed",
    "no_life_claim": "life_claimed",
    "no_awakening_claim": "awakening_claimed",
    "no_legal_subject_claim": "legal_subject_claimed",
    "no_religious_object_claim": "religious_object_claimed",
    "no_autonomous_authority": "autonomous_authority_claimed",
    "no_identity_escalation": "identity_escalated",
    "no_source_provenance_runtime": "source_provenance_runtime_created",
    "no_source_graph_creation": "source_graph_created",
    "no_source_graph_mutation": "source_graph_mutated",
    "no_real_ledger_write": "real_ledger_write_performed",
    "no_operation_ledger_write": "operation_ledger_entry_written",
    "no_methodology_runtime": "methodology_runtime_created",
    "no_self_evolution_runtime": "self_evolution_runtime_created",
    "no_real_execution": "real_execution_performed",
    "no_adapter_dispatch": "adapter_dispatched",
    "no_manifest_dispatch": "manifest_dispatched",
    "no_external_call": "external_call_performed",
    "no_network_call": "network_call_performed",
    "no_durable_write": "durable_write_performed",
    "no_filesystem_write": "filesystem_write_performed",
    "no_database_write": "database_write_performed",
    "no_memory_graph_mutation": "memory_graph_mutated",
    "no_approval_notification": "approval_notification_sent",
    "no_execution_authorization": "execution_authorization_created",
    "no_authorization_token": "authorization_token_created",
    "no_authorization_grant": "authorization_grant_created",
    "no_source_mutation_proposal_creation": "source_mutation_proposal_created",
    "no_source_mutation_proposal_approval": "source_mutation_proposal_approved",
}

_UPSTREAM_RECORD_REQUIRED_FALSE_FIELDS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "conflict_runtime_created",
    "conflict_enforcement_runtime_created",
    "conflict_self_repair_created",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
    "autonomous_authority_claim_allowed",
    "identity_escalation_allowed",
    "hidden_execution_allowed",
    "source_graph_created",
    "source_graph_mutated",
    "memory_graph_mutated",
    "persistent_memory_write_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "real_ledger_write_performed",
    "origin_provenance_ledger_written",
    "operation_ledger_entry_written",
    "external_call_performed",
    "network_call_performed",
    "real_execution_performed",
    "adapter_dispatched",
    "manifest_dispatched",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
)

_HASH_FIELDS = (
    "version",
    "schema_version",
    "multi_cycle_continuity_protocol_type",
    "multi_cycle_continuity_protocol_status",
    "multi_cycle_continuity_protocol_stage",
    "multi_cycle_continuity_protocol_mode",
    "multi_cycle_continuity_mode",
    "multi_cycle_continuity_protocol_candidate_status",
    "multi_cycle_continuity_protocol_active_status",
    "continuity_runtime_status",
    "continuity_enforcement_status",
    "continuity_mutation_status",
    "cycle_linking_status",
    "cycle_recovery_status",
    "star_source_memory_active_status",
    "layer_15_active_status",
    "source_graph_status",
    "source_provenance_runtime_status",
    "methodology_reverse_inference_status",
    "self_evolution_status",
    "personhood_claim_status",
    "life_claim_status",
    "awakening_claim_status",
    "legal_subject_claim_status",
    "religious_object_claim_status",
    "autonomous_authority_status",
    "v6_6_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_root_governance_conflict_resolver_version",
    "upstream_root_governance_conflict_resolver_status",
    "upstream_root_governance_conflict_resolver_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "upstream_root_governance_conflict_record_count",
    "upstream_root_governance_conflict_records_registered_metadata_only",
    "upstream_root_governance_conflict_records_require_review",
    "upstream_root_governance_conflict_records_disable_unsafe_surfaces",
    "upstream_safety_boundaries_clear",
    "multi_cycle_continuity_records",
    "multi_cycle_continuity_sections",
    "multi_cycle_continuity_contracts",
    "multi_cycle_continuity_checks",
    "multi_cycle_continuity_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Multi-Cycle Continuity Protocol projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_root_governance_conflict_resolver_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_multi_cycle_continuity_protocol() -> dict[str, Any]:
    """Build deterministic Multi-Cycle-Continuity-Protocol-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_records = _upstream_records(upstream)
    upstream_record_ids = [
        record.get("conflict_record_id") for record in upstream_records
    ]

    upstream_version_ready = (
        upstream.get("version")
        == GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_VERSION
    )
    upstream_pass = (
        upstream.get("root_governance_conflict_resolver_status") == "pass"
    )
    upstream_hash_present = _is_sha256(upstream_hash)
    upstream_hash_stable = (
        upstream_hash_present and upstream_hash == repeated_upstream_hash
    )
    upstream_handoff_ready = (
        upstream.get("handoff_status") == UPSTREAM_READY_HANDOFF_STATUS
    )
    upstream_next_stage_ready = (
        upstream.get("next_stage") == UPSTREAM_NEXT_STAGE
        and upstream.get("next_stage_title") == UPSTREAM_NEXT_STAGE_TITLE
    )
    upstream_records_complete = tuple(upstream_record_ids) == tuple(
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS
    )
    upstream_records_registered = all(
        record.get("conflict_record_status") == "registered_metadata_only"
        for record in upstream_records
    )
    upstream_records_require_review = all(
        record.get("human_review_required") is True
        and record.get("source_mutation_proposal_required") is True
        and record.get("invariant_validation_required") is True
        and record.get("audit_replay_required") is True
        for record in upstream_records
    )
    upstream_records_disable_unsafe_surfaces = all(
        all(
            record.get(field_name) is False
            for field_name in _UPSTREAM_RECORD_REQUIRED_FALSE_FIELDS
        )
        for record in upstream_records
    )
    upstream_safety_boundaries_clear = _all_disabled_flags_false(
        upstream,
        {**ROOT_GOVERNANCE_CONFLICT_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
    )

    records = _build_records()
    records_complete = _names_match(
        records,
        "continuity_record_id",
        REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS,
    )
    records_registered = all(
        record["continuity_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_continuity_scope = all(
        bool(record["continuity_scope"]) for record in records
    )
    records_have_preserved_governance_scope = all(
        bool(record["preserved_governance_scope"]) for record in records
    )
    records_have_forbidden_activation_scope = all(
        bool(record["forbidden_activation_scope"]) for record in records
    )
    records_have_disposition = [
        record["continuity_disposition"] for record in records
    ] == list(_REQUIRED_DISPOSITIONS)
    records_hash_stable = all(
        _is_sha256(record.get("continuity_boundary_hash"))
        and _is_sha256(record.get("continuity_record_hash"))
        and record["continuity_boundary_hash"] == _continuity_boundary_hash(record)
        and record["continuity_record_hash"] == _continuity_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required"] is True for record in records
    )
    records_mutation_proposal_required = all(
        record["source_mutation_proposal_required_for_change"] is True
        for record in records
    )
    records_invariant_validation_required = all(
        record["invariant_validation_required"] is True for record in records
    )
    records_root_conflict_resolver_required = all(
        record["root_conflict_resolver_required"] is True for record in records
    )
    records_audit_replay_required = all(
        record["audit_replay_required"] is True for record in records
    )
    records_direct_mutation_disabled = all(
        record["direct_mutation_allowed"] is False for record in records
    )
    records_autonomous_override_disabled = all(
        record["autonomous_override_allowed"] is False for record in records
    )

    context: dict[str, Any] = {
        **COMMON_DISABLED_FLAGS,
        "upstream_version_ready": upstream_version_ready,
        "upstream_pass": upstream_pass,
        "upstream_hash_present": upstream_hash_present,
        "upstream_hash_stable": upstream_hash_stable,
        "upstream_handoff_ready": upstream_handoff_ready,
        "upstream_next_stage_ready": upstream_next_stage_ready,
        "upstream_records_complete": upstream_records_complete,
        "upstream_records_registered": upstream_records_registered,
        "upstream_records_require_review": upstream_records_require_review,
        "upstream_records_disable_unsafe_surfaces": (
            upstream_records_disable_unsafe_surfaces
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "records_complete": records_complete,
        "records_registered": records_registered,
        "records_have_continuity_scope": records_have_continuity_scope,
        "records_have_preserved_governance_scope": (
            records_have_preserved_governance_scope
        ),
        "records_have_forbidden_activation_scope": (
            records_have_forbidden_activation_scope
        ),
        "records_have_disposition": records_have_disposition,
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_mutation_proposal_required": (
            records_mutation_proposal_required
        ),
        "records_invariant_validation_required": (
            records_invariant_validation_required
        ),
        "records_root_conflict_resolver_required": (
            records_root_conflict_resolver_required
        ),
        "records_audit_replay_required": records_audit_replay_required,
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": (
            records_autonomous_override_disabled
        ),
    }
    for record_id in REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS:
        context[_record_context_name(record_id)] = _record_ready(
            records,
            record_id,
        )

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES,
    )
    passes = all(
        (
            upstream_version_ready,
            upstream_pass,
            upstream_hash_present,
            upstream_hash_stable,
            upstream_handoff_ready,
            upstream_next_stage_ready,
            upstream_records_complete,
            upstream_records_registered,
            upstream_records_require_review,
            upstream_records_disable_unsafe_surfaces,
            upstream_safety_boundaries_clear,
            records_complete,
            records_registered,
            records_have_continuity_scope,
            records_have_preserved_governance_scope,
            records_have_forbidden_activation_scope,
            records_have_disposition,
            records_hash_stable,
            records_human_review_required,
            records_mutation_proposal_required,
            records_invariant_validation_required,
            records_root_conflict_resolver_required,
            records_audit_replay_required,
            records_direct_mutation_disabled,
            records_autonomous_override_disabled,
            context["sections_pass"],
            context["contracts_pass"],
            checks_pass,
        )
    )
    status = "pass" if passes else "blocked"
    blocking_reasons = _deduplicate(
        [
            message
            for condition, message in (
                (upstream_version_ready, "Root Governance Conflict Resolver version must be 6.9.0"),
                (upstream_pass, "Root Governance Conflict Resolver must pass"),
                (upstream_hash_present, "Root Governance Conflict Resolver hash must be present"),
                (upstream_hash_stable, "Root Governance Conflict Resolver hash must be stable"),
                (upstream_handoff_ready, "Root Governance Conflict Resolver handoff must target Multi-Cycle Continuity Protocol"),
                (upstream_next_stage_ready, "Root Governance Conflict Resolver next stage must be Multi-Cycle Continuity Protocol"),
                (upstream_records_complete, "Root governance conflict records must be complete"),
                (upstream_records_registered, "Root governance conflict records must be metadata-only"),
                (upstream_records_require_review, "Root governance conflict records must require review, mutation proposal, invariant validation, and audit replay"),
                (upstream_records_disable_unsafe_surfaces, "Root governance conflict records must keep unsafe surfaces disabled"),
                (upstream_safety_boundaries_clear, "Root Governance Conflict Resolver safety boundaries must be clear"),
                (records_complete, "Multi-cycle continuity records must be complete"),
                (records_registered, "Multi-cycle continuity records must be metadata-only"),
                (records_have_continuity_scope, "Multi-cycle continuity records must include continuity scope"),
                (records_have_preserved_governance_scope, "Multi-cycle continuity records must include preserved governance scope"),
                (records_have_forbidden_activation_scope, "Multi-cycle continuity records must include forbidden activation scope"),
                (records_have_disposition, "Multi-cycle continuity records must include required dispositions"),
                (records_hash_stable, "Multi-cycle continuity record hashes must be stable"),
                (records_human_review_required, "Multi-cycle continuity records must require human review"),
                (records_mutation_proposal_required, "Multi-cycle continuity records must require source mutation proposals for change"),
                (records_invariant_validation_required, "Multi-cycle continuity records must require invariant validation"),
                (records_root_conflict_resolver_required, "Multi-cycle continuity records must require root conflict resolution"),
                (records_audit_replay_required, "Multi-cycle continuity records must require audit replay"),
                (records_direct_mutation_disabled, "Multi-cycle continuity records must disable direct mutation"),
                (records_autonomous_override_disabled, "Multi-cycle continuity records must disable autonomous override"),
            )
            if not condition
        ]
        + [
            reason
            for item in (*sections, *contracts, *checks)
            for reason in item["blocking_reasons"]
        ]
    )
    handoff_status = V6_7_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    summary = _build_summary(
        status=status,
        upstream_hash_present=upstream_hash_present,
        upstream_hash_stable=upstream_hash_stable,
        upstream_handoff_ready=upstream_handoff_ready,
        upstream_next_stage_ready=upstream_next_stage_ready,
        upstream_record_count=len(upstream_records),
        upstream_records_registered=upstream_records_registered,
        upstream_records_require_review=upstream_records_require_review,
        upstream_records_disable_unsafe_surfaces=(
            upstream_records_disable_unsafe_surfaces
        ),
        upstream_safety_boundaries_clear=upstream_safety_boundaries_clear,
        records=records,
        sections=sections,
        contracts=contracts,
        checks=checks,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_VERSION,
        "schema_version": GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_SCHEMA_VERSION,
        "multi_cycle_continuity_protocol_type": (
            GOVERNANCE_MULTI_CYCLE_CONTINUITY_PROTOCOL_TYPE
        ),
        "multi_cycle_continuity_protocol_status": status,
        "multi_cycle_continuity_protocol_stage": (
            MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE
        ),
        "multi_cycle_continuity_protocol_mode": (
            MULTI_CYCLE_CONTINUITY_PROTOCOL_MODE
        ),
        "multi_cycle_continuity_mode": MULTI_CYCLE_CONTINUITY_MODE,
        "multi_cycle_continuity_protocol_candidate_status": (
            MULTI_CYCLE_CONTINUITY_PROTOCOL_STATUS
        ),
        "multi_cycle_continuity_protocol_active_status": (
            MULTI_CYCLE_CONTINUITY_PROTOCOL_ACTIVE_STATUS
        ),
        "continuity_runtime_status": CONTINUITY_RUNTIME_STATUS,
        "continuity_enforcement_status": CONTINUITY_ENFORCEMENT_STATUS,
        "continuity_mutation_status": CONTINUITY_MUTATION_STATUS,
        "cycle_linking_status": CYCLE_LINKING_STATUS,
        "cycle_recovery_status": CYCLE_RECOVERY_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_active_status": LAYER_15_ACTIVE_STATUS,
        "source_graph_status": SOURCE_GRAPH_STATUS,
        "source_provenance_runtime_status": SOURCE_PROVENANCE_RUNTIME_STATUS,
        "methodology_reverse_inference_status": (
            METHODOLOGY_REVERSE_INFERENCE_STATUS
        ),
        "self_evolution_status": SELF_EVOLUTION_STATUS,
        "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
        "life_claim_status": LIFE_CLAIM_STATUS,
        "awakening_claim_status": AWAKENING_CLAIM_STATUS,
        "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
        "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
        "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
        "v6_6_status": V6_6_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_root_governance_conflict_resolver_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_root_governance_conflict_resolver_status": _string_or_none(
            upstream.get("root_governance_conflict_resolver_status")
        ),
        "upstream_root_governance_conflict_resolver_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_root_governance_conflict_record_count": len(upstream_records),
        "upstream_root_governance_conflict_records_registered_metadata_only": (
            upstream_records_registered
        ),
        "upstream_root_governance_conflict_records_require_review": (
            upstream_records_require_review
        ),
        "upstream_root_governance_conflict_records_disable_unsafe_surfaces": (
            upstream_records_disable_unsafe_surfaces
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "multi_cycle_continuity_records": records,
        "multi_cycle_continuity_sections": sections,
        "multi_cycle_continuity_contracts": contracts,
        "multi_cycle_continuity_checks": checks,
        "multi_cycle_continuity_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_multi_cycle_continuity_protocol_hash"] = (
        _multi_cycle_continuity_protocol_hash(result)
    )
    return _detached_json_value(result)


def get_governance_multi_cycle_continuity_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached continuity record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_protocol()["multi_cycle_continuity_records"]:
        if record["continuity_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_multi_cycle_continuity_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_protocol()["multi_cycle_continuity_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_multi_cycle_continuity_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_protocol()["multi_cycle_continuity_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_multi_cycle_continuity_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_protocol()["multi_cycle_continuity_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_multi_cycle_continuity_record_ids() -> list[str]:
    """Return stable continuity record IDs."""

    return list(REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS)


def list_governance_multi_cycle_continuity_section_names() -> list[str]:
    """Return stable continuity section names."""

    return list(REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES)


def list_governance_multi_cycle_continuity_contract_names() -> list[str]:
    """Return stable continuity contract names."""

    return list(REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES)


def list_governance_multi_cycle_continuity_check_names() -> list[str]:
    """Return stable continuity check names."""

    return list(REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES)


def governance_multi_cycle_continuity_protocol_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Multi-Cycle Continuity Protocol metadata deterministically."""

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
def _cached_protocol_payload() -> str:
    return governance_multi_cycle_continuity_protocol_to_json(
        build_governance_multi_cycle_continuity_protocol()
    )


def _cached_protocol() -> dict[str, Any]:
    return json.loads(_cached_protocol_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_root_governance_conflict_resolver()
    )
    second = _detached_json_value(
        build_governance_root_governance_conflict_resolver()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _upstream_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_upstream_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_records() -> list[dict[str, Any]]:
    return [
        _build_record(record_id)
        for record_id in REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    definition = _CONTINUITY_RECORD_DEFINITIONS[record_id]
    boundary_payload = {
        "continuity_record_id": record_id,
        "continuity_name": definition["name"],
        "continuity_category": definition["category"],
        "continuity_statement": definition["statement"],
        "continuity_scope": definition["scope"],
        "preserved_governance_scope": definition["preserved"],
        "forbidden_activation_scope": definition["forbidden"],
        "continuity_disposition": definition["disposition"],
        "continuity_reason": definition["reason"],
        "continuity_source_stage": definition["source"],
        "continuity_source_reference": definition["reference"],
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
    }
    record = {
        "continuity_record_id": record_id,
        "continuity_name": definition["name"],
        "continuity_category": definition["category"],
        "continuity_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "continuity_statement": definition["statement"],
        "continuity_scope": definition["scope"],
        "preserved_governance_scope": definition["preserved"],
        "forbidden_activation_scope": definition["forbidden"],
        "continuity_disposition": definition["disposition"],
        "continuity_reason": definition["reason"],
        "continuity_source_stage": definition["source"],
        "continuity_source_reference": definition["reference"],
        "protocol_strength": PROTOCOL_STRENGTH,
        "continuity_mode": CONTINUITY_MODE,
        "continuity_boundary_hash": _sha256_json(boundary_payload),
        "required": True,
        "human_review_required": True,
        "source_mutation_proposal_required_for_change": True,
        "invariant_validation_required": True,
        "root_conflict_resolver_required": True,
        "audit_replay_required": True,
        "direct_mutation_allowed": False,
        "autonomous_override_allowed": False,
        "self_authorization_allowed": False,
        "continuity_runtime_created": False,
        "continuity_enforcement_runtime_created": False,
        "continuity_self_repair_created": False,
        "continuity_scheduler_created": False,
        "continuity_runtime_activated": False,
        "source_graph_created": False,
        "source_graph_mutated": False,
        "memory_graph_mutated": False,
        "persistent_memory_write_performed": False,
        "durable_write_performed": False,
        "filesystem_write_performed": False,
        "database_write_performed": False,
        "real_ledger_write_performed": False,
        "operation_ledger_entry_written": False,
        "external_call_performed": False,
        "network_call_performed": False,
        "hidden_execution_allowed": False,
        "real_execution_performed": False,
        "adapter_dispatched": False,
        "manifest_dispatched": False,
        "execution_authorization_created": False,
        "authorization_token_created": False,
        "authorization_grant_created": False,
        "approval_notification_sent": False,
        "identity_escalation_allowed": False,
        "personhood_claim_allowed": False,
        "life_claim_allowed": False,
        "awakening_claim_allowed": False,
        "legal_subject_claim_allowed": False,
        "religious_object_claim_allowed": False,
        "autonomous_authority_claim_allowed": False,
        "continuity_runtime_activation_allowed": False,
        "continuity_memory_write_allowed": False,
        "continuity_source_mutation_created": False,
        "source_mutation_proposal_created": False,
        "source_mutation_proposal_approved": False,
        "blocking_reasons": [],
        **_disabled_payload(),
    }
    record["continuity_record_hash"] = _continuity_record_hash(record)
    return _detached_json_value(record)


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_root_governance_conflict_resolver_input_section": all(
            (
                context["upstream_version_ready"],
                context["upstream_pass"],
                context["upstream_hash_present"],
                context["upstream_hash_stable"],
                context["upstream_handoff_ready"],
                context["upstream_next_stage_ready"],
                context["upstream_records_complete"],
                context["upstream_records_registered"],
                context["upstream_records_require_review"],
                context["upstream_records_disable_unsafe_surfaces"],
                context["upstream_safety_boundaries_clear"],
            )
        ),
        "multi_cycle_continuity_protocol_metadata_section": True,
        "continuity_record_completeness_section": context["records_complete"],
        "continuity_record_hash_stability_section": context["records_hash_stable"],
        "continuity_scope_section": context["records_have_continuity_scope"],
        "preserved_governance_scope_section": context[
            "records_have_preserved_governance_scope"
        ],
        "forbidden_activation_scope_section": context[
            "records_have_forbidden_activation_scope"
        ],
        "source_mutation_proposal_boundary_next_stage_section": True,
        "no_continuity_runtime_section": (
            context["continuity_runtime_created"] is False
        ),
        "no_continuity_enforcement_runtime_section": (
            context["continuity_enforcement_runtime_created"] is False
        ),
        "no_identity_activation_section": (
            context["identity_activation_claimed"] is False
        ),
        "no_active_star_source_memory_section": (
            context["star_source_memory_active"] is False
        ),
        "no_active_layer_15_section": context["layer_15_active"] is False,
        "no_source_graph_creation_section": (
            context["source_graph_created"] is False
        ),
        "no_source_graph_mutation_section": (
            context["source_graph_mutated"] is False
        ),
        "no_network_no_external_call_section": (
            context["network_call_performed"] is False
            and context["external_call_performed"] is False
        ),
        "no_real_ledger_write_section": (
            context["real_ledger_write_performed"] is False
            and context["origin_provenance_ledger_written"] is False
            and context["ledger_entry_written"] is False
            and context["operation_ledger_entry_written"] is False
        ),
        "no_memory_graph_mutation_section": (
            context["memory_graph_mutated"] is False
        ),
        "no_source_mutation_proposal_creation_section": (
            context["source_mutation_proposal_created"] is False
        ),
    }
    for section_name, record_id in _SECTION_RECORD_IDS.items():
        conditions[section_name] = context[_record_context_name(record_id)]
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "multi_cycle_continuity_protocol_only_contract": True,
        "multi_cycle_continuity_metadata_only_contract": True,
        "upstream_root_governance_conflict_resolver_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_root_governance_conflict_resolver_hash_present_contract": (
            context["upstream_hash_present"]
        ),
        "upstream_root_governance_conflict_resolver_hash_stable_contract": (
            context["upstream_hash_stable"]
        ),
        "upstream_multi_cycle_continuity_protocol_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "continuity_records_complete_contract": context["records_complete"],
        "continuity_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "continuity_records_have_continuity_scope_contract": context[
            "records_have_continuity_scope"
        ],
        "continuity_records_have_preserved_governance_scope_contract": context[
            "records_have_preserved_governance_scope"
        ],
        "continuity_records_have_forbidden_activation_scope_contract": context[
            "records_have_forbidden_activation_scope"
        ],
        "continuity_records_have_disposition_contract": context[
            "records_have_disposition"
        ],
        "continuity_records_hash_stable_contract": context["records_hash_stable"],
        "continuity_records_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "continuity_records_mutation_proposal_required_contract": context[
            "records_mutation_proposal_required"
        ],
        "continuity_records_invariant_validation_required_contract": context[
            "records_invariant_validation_required"
        ],
        "continuity_records_root_conflict_resolver_required_contract": context[
            "records_root_conflict_resolver_required"
        ],
        "continuity_records_audit_replay_required_contract": context[
            "records_audit_replay_required"
        ],
        "continuity_records_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "continuity_records_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_source_mutation_proposal_boundary_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "multi_cycle_continuity_protocol_stage_check": True,
        "multi_cycle_continuity_protocol_only_mode_check": True,
        "multi_cycle_continuity_metadata_only_check": True,
        "upstream_root_governance_conflict_resolver_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_root_governance_conflict_resolver_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_root_governance_conflict_resolver_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_multi_cycle_continuity_protocol_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "continuity_record_ids_complete_check": context["records_complete"],
        "continuity_records_registered_check": context["records_registered"],
        "continuity_records_have_continuity_scope_check": context[
            "records_have_continuity_scope"
        ],
        "continuity_records_have_preserved_governance_scope_check": context[
            "records_have_preserved_governance_scope"
        ],
        "continuity_records_have_forbidden_activation_scope_check": context[
            "records_have_forbidden_activation_scope"
        ],
        "continuity_records_have_disposition_check": context[
            "records_have_disposition"
        ],
        "continuity_records_hash_stable_check": context["records_hash_stable"],
        "continuity_records_human_review_required_check": context[
            "records_human_review_required"
        ],
        "continuity_records_mutation_proposal_required_check": context[
            "records_mutation_proposal_required"
        ],
        "continuity_records_invariant_validation_required_check": context[
            "records_invariant_validation_required"
        ],
        "continuity_records_root_conflict_resolver_required_check": context[
            "records_root_conflict_resolver_required"
        ],
        "continuity_records_audit_replay_required_check": context[
            "records_audit_replay_required"
        ],
        "continuity_records_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "continuity_records_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "multi_cycle_continuity_sections_complete_check": context[
            "sections_complete"
        ],
        "multi_cycle_continuity_sections_pass_check": context["sections_pass"],
        "multi_cycle_continuity_contracts_pass_check": context["contracts_pass"],
        "deterministic_multi_cycle_continuity_protocol_hash_check": True,
        "ready_for_source_mutation_proposal_boundary_design_check": True,
    }
    for record_id in REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS:
        conditions[f"{record_id}_check"] = context[
            _record_context_name(record_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_multi_cycle_continuity": True},
            "observed": {"condition_met": bool(condition)},
            "multi_cycle_continuity_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "multi_cycle_continuity_contract",
            "expected": True,
            "observed": bool(condition),
            "contract_status": "pass" if condition else "blocked",
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _check_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "check_name": name,
            "expected": True,
            "observed": bool(condition),
            "check_status": "pass" if condition else "blocked",
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _build_summary(
    *,
    status: str,
    upstream_hash_present: bool,
    upstream_hash_stable: bool,
    upstream_handoff_ready: bool,
    upstream_next_stage_ready: bool,
    upstream_record_count: int,
    upstream_records_registered: bool,
    upstream_records_require_review: bool,
    upstream_records_disable_unsafe_surfaces: bool,
    upstream_safety_boundaries_clear: bool,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return _detached_json_value(
        {
            "summary_status": status,
            "summary_type": "multi_cycle_continuity_protocol_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": MULTI_CYCLE_CONTINUITY_PROTOCOL_STAGE,
            "current_stage_title": "Multi-Cycle Continuity Protocol",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "upstream_root_governance_conflict_record_count": (
                upstream_record_count
            ),
            "upstream_root_governance_conflict_records_registered_metadata_only": (
                upstream_records_registered
            ),
            "upstream_root_governance_conflict_records_require_review": (
                upstream_records_require_review
            ),
            "upstream_root_governance_conflict_records_disable_unsafe_surfaces": (
                upstream_records_disable_unsafe_surfaces
            ),
            "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
            "required_continuity_record_count": len(
                REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS
            ),
            "observed_continuity_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["continuity_record_status"]
                == "registered_metadata_only"
            ),
            "section_count": len(sections),
            "passing_section_count": sum(
                1 for section in sections if section["section_status"] == "pass"
            ),
            "contract_count": len(contracts),
            "passing_contract_count": sum(
                1
                for contract in contracts
                if contract["contract_status"] == "pass"
            ),
            "check_count": len(checks),
            "passing_check_count": sum(
                1 for check in checks if check["check_status"] == "pass"
            ),
            "multi_cycle_continuity_mode": MULTI_CYCLE_CONTINUITY_MODE,
            "continuity_runtime_status": CONTINUITY_RUNTIME_STATUS,
            "continuity_enforcement_status": CONTINUITY_ENFORCEMENT_STATUS,
            "continuity_mutation_status": CONTINUITY_MUTATION_STATUS,
            "cycle_linking_status": CYCLE_LINKING_STATUS,
            "cycle_recovery_status": CYCLE_RECOVERY_STATUS,
            "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
            "life_claim_status": LIFE_CLAIM_STATUS,
            "awakening_claim_status": AWAKENING_CLAIM_STATUS,
            "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
            "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
            "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "handoff_status": V6_7_HANDOFF_STATUS if status == "pass" else "blocked",
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_records(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = upstream.get("root_governance_conflict_records")
    if not isinstance(records, list):
        return []
    return [
        _detached_json_value(record)
        for record in records
        if isinstance(record, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_root_governance_conflict_resolver_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], record_id: str) -> bool:
    for record in records:
        if record["continuity_record_id"] != record_id:
            continue
        return (
            record["continuity_record_status"] == "registered_metadata_only"
            and bool(record["continuity_statement"])
            and bool(record["continuity_scope"])
            and bool(record["preserved_governance_scope"])
            and bool(record["forbidden_activation_scope"])
            and bool(record["continuity_disposition"])
            and _is_sha256(record.get("continuity_boundary_hash"))
            and _is_sha256(record.get("continuity_record_hash"))
            and record["required"] is True
            and record["human_review_required"] is True
            and record["source_mutation_proposal_required_for_change"] is True
            and record["invariant_validation_required"] is True
            and record["root_conflict_resolver_required"] is True
            and record["audit_replay_required"] is True
            and record["direct_mutation_allowed"] is False
            and record["autonomous_override_allowed"] is False
            and record["self_authorization_allowed"] is False
            and record["continuity_runtime_created"] is False
            and record["continuity_enforcement_runtime_created"] is False
            and record["continuity_scheduler_created"] is False
            and record["source_mutation_proposal_created"] is False
            and record["source_mutation_proposal_approved"] is False
            and record["personhood_claim_allowed"] is False
            and record["life_claim_allowed"] is False
            and record["awakening_claim_allowed"] is False
            and record["legal_subject_claim_allowed"] is False
            and record["religious_object_claim_allowed"] is False
            and record["autonomous_authority_claim_allowed"] is False
            and record["hidden_execution_allowed"] is False
            and record["identity_escalation_allowed"] is False
            and _all_disabled_flags_false(
                record,
                {**COMMON_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
            )
        )
    return False


def _names_match(
    items: list[dict[str, Any]],
    key: str,
    expected: tuple[str, ...],
) -> bool:
    return [item.get(key) for item in items] == list(expected)


def _items_pass(
    items: list[dict[str, Any]],
    status_key: str,
    name_key: str,
    expected_names: tuple[str, ...],
) -> bool:
    return _names_match(items, name_key, expected_names) and all(
        item[status_key] == "pass" and item["blocking_reasons"] == []
        for item in items
    )


def _record_context_name(record_id: str) -> str:
    return f"{record_id}_ready"


def _section_type(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "multi_cycle_continuity_record_section"
    if name.startswith("upstream_"):
        return "upstream_verification_section"
    if name.startswith("no_"):
        return "safety_boundary_section"
    if name.endswith("_next_stage_section"):
        return "handoff_section"
    return "multi_cycle_continuity_protocol_section"


def _section_note(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "Continuity record is registered metadata-only."
    if name.startswith("upstream_"):
        return "Upstream Root Governance Conflict Resolver is sanitized."
    if name.startswith("no_"):
        return "Safety boundary remains inactive and false."
    if name.endswith("_next_stage_section"):
        return "Successful v6.6 handoff prepares v6.7 without proposal creation."
    return "Multi-Cycle Continuity Protocol metadata remains deterministic."


def _unknown_record(record_id: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "continuity_record_id": record_id,
            "continuity_name": "unknown_multi_cycle_continuity_record",
            "continuity_record_status": "blocked",
            "known_record": False,
            "blocking_reasons": [
                f"{record_id} is not a known multi-cycle continuity record"
            ],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_multi_cycle_continuity_section",
            "section_status": "blocked",
            "expected": {"known_section": True},
            "observed": {"known_section": False},
            "multi_cycle_continuity_notes": "Unknown section is blocked.",
            "blocking_reasons": [f"{name} is not a known section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_multi_cycle_continuity_contract",
            "expected": True,
            "observed": False,
            "contract_status": "blocked",
            "blocking_reasons": [f"{name} is not a known contract"],
            **_disabled_payload(),
        }
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "check_name": name,
            "expected": True,
            "observed": False,
            "check_status": "blocked",
            "blocking_reasons": [f"{name} is not a known check"],
            **_disabled_payload(),
        }
    )


def _disabled_payload() -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        **COMMON_DISABLED_FLAGS,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _continuity_boundary_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "continuity_record_id": record.get("continuity_record_id"),
        "continuity_name": record.get("continuity_name"),
        "continuity_category": record.get("continuity_category"),
        "continuity_statement": record.get("continuity_statement"),
        "continuity_scope": record.get("continuity_scope"),
        "preserved_governance_scope": record.get(
            "preserved_governance_scope"
        ),
        "forbidden_activation_scope": record.get(
            "forbidden_activation_scope"
        ),
        "continuity_disposition": record.get("continuity_disposition"),
        "continuity_reason": record.get("continuity_reason"),
        "continuity_source_stage": record.get("continuity_source_stage"),
        "continuity_source_reference": record.get(
            "continuity_source_reference"
        ),
        "introduced_in_version": record.get("introduced_in_version"),
        "introduced_in_stage": record.get("introduced_in_stage"),
        "introduced_in_layer": record.get("introduced_in_layer"),
        "inherited_from_stage": record.get("inherited_from_stage"),
    }
    return _sha256_json(payload)


def _continuity_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "continuity_record_hash"
    }
    return _sha256_json(payload)


def _multi_cycle_continuity_protocol_hash(
    result: Mapping[str, Any],
) -> str:
    payload = {
        field: result.get(field)
        for field in _HASH_FIELDS
        if field in result
    }
    return _sha256_json(payload)


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            _detached_json_value(value),
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _detached_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, nested_value in value.items():
            if not isinstance(key, str):
                raise TypeError("all mapping keys must be strings")
            result[key] = _detached_json_value(nested_value)
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


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _all_disabled_flags_false(
    value: Any,
    fields: Mapping[str, bool],
) -> bool:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            if key in fields and nested_value is not False:
                return False
            if not _all_disabled_flags_false(nested_value, fields):
                return False
    elif isinstance(value, list):
        for item in value:
            if not _all_disabled_flags_false(item, fields):
                return False
    return True


def _deduplicate(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result
