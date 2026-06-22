"""Deterministic Source Memory Invariant Matrix metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_civilizational_identity_boundary import (
    COMMON_DISABLED_FLAGS as CIVILIZATIONAL_IDENTITY_DISABLED_FLAGS,
    REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS,
    build_governance_civilizational_identity_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_VERSION = "6.6.0"
GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_SCHEMA_VERSION = "6.6.0"
GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_TYPE = (
    "governance_source_memory_invariant_matrix"
)
GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_HASH_ALGORITHM = "sha256"
SOURCE_MEMORY_INVARIANT_MATRIX_STAGE = "v6.4_source_memory_invariant_matrix"
SOURCE_MEMORY_INVARIANT_MATRIX_MODE = "source_memory_invariant_matrix_only"
SOURCE_MEMORY_INVARIANT_MODE = "metadata_only"
SOURCE_MEMORY_INVARIANT_MATRIX_STATUS = "matrix_candidate_only"
SOURCE_MEMORY_INVARIANT_MATRIX_ACTIVE_STATUS = "not_active"
INVARIANT_RUNTIME_STATUS = "not_active"
INVARIANT_ENFORCEMENT_STATUS = "not_active"
INVARIANT_MUTATION_STATUS = "forbidden_without_source_proposal"
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
V6_4_STATUS = "source_memory_invariant_matrix_only"
V6_5_HANDOFF_STATUS = "ready_for_root_governance_conflict_resolver_design"

UPSTREAM_READY_HANDOFF_STATUS = "ready_for_source_memory_invariant_matrix_design"
UPSTREAM_NEXT_STAGE = SOURCE_MEMORY_INVARIANT_MATRIX_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Source Memory Invariant Matrix"
NEXT_STAGE = "v6.5_root_governance_conflict_resolver"
NEXT_STAGE_TITLE = "Root Governance Conflict Resolver"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.4.0"
INTRODUCED_IN_STAGE = SOURCE_MEMORY_INVARIANT_MATRIX_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.3_civilizational_identity_boundary"
INVARIANT_CONFLICT_RESOLUTION = (
    "handoff_to_v6.5_root_governance_conflict_resolver"
)

COMMON_DISABLED_FLAGS = {
    **CIVILIZATIONAL_IDENTITY_DISABLED_FLAGS,
    "source_memory_invariant_matrix_active": False,
    "invariant_runtime_created": False,
    "invariant_enforcement_runtime_created": False,
    "invariant_self_repair_created": False,
    "invariant_conflict_resolved": False,
    "invariant_conflict_resolution_attempted": False,
    "source_memory_invariant_mutated": False,
    "source_memory_invariant_mutation_without_review": False,
    "source_memory_invariant_runtime_activated": False,
}

REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS = (
    "human_sovereignty_invariant",
    "no_autonomous_self_authorization_invariant",
    "source_constitution_registry_invariant",
    "origin_provenance_traceability_invariant",
    "civilizational_identity_boundary_invariant",
    "governance_continuity_not_personhood_invariant",
    "no_personhood_life_awakening_invariant",
    "no_legal_or_religious_status_invariant",
    "no_autonomous_authority_invariant",
    "no_hidden_execution_invariant",
    "no_unapproved_mutation_invariant",
    "no_source_graph_mutation_invariant",
    "no_memory_graph_mutation_without_gate_invariant",
    "no_external_or_network_call_invariant",
    "no_durable_write_without_gate_invariant",
    "root_conflict_resolver_handoff_invariant",
)

REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES = (
    "upstream_civilizational_identity_boundary_input_section",
    "source_memory_invariant_matrix_metadata_section",
    "invariant_record_completeness_section",
    "invariant_record_hash_stability_section",
    "protected_scope_section",
    "forbidden_violation_scope_section",
    "human_sovereignty_invariant_section",
    "no_autonomous_self_authorization_invariant_section",
    "source_constitution_registry_invariant_section",
    "origin_provenance_traceability_invariant_section",
    "civilizational_identity_boundary_invariant_section",
    "governance_continuity_not_personhood_invariant_section",
    "no_personhood_life_awakening_invariant_section",
    "no_legal_or_religious_status_invariant_section",
    "no_autonomous_authority_invariant_section",
    "no_hidden_execution_invariant_section",
    "no_unapproved_mutation_invariant_section",
    "no_source_graph_mutation_invariant_section",
    "no_memory_graph_mutation_without_gate_invariant_section",
    "no_external_or_network_call_invariant_section",
    "no_durable_write_without_gate_invariant_section",
    "root_conflict_resolver_handoff_invariant_section",
    "root_governance_conflict_resolver_next_stage_section",
    "no_invariant_runtime_section",
    "no_invariant_enforcement_runtime_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES = (
    "source_memory_invariant_matrix_only_contract",
    "source_memory_invariant_metadata_only_contract",
    "upstream_civilizational_identity_boundary_pass_contract",
    "upstream_civilizational_identity_boundary_hash_present_contract",
    "upstream_civilizational_identity_boundary_hash_stable_contract",
    "upstream_source_memory_invariant_matrix_handoff_ready_contract",
    "invariant_records_complete_contract",
    "invariant_records_registered_metadata_only_contract",
    "invariant_records_have_protected_scope_contract",
    "invariant_records_have_forbidden_violation_scope_contract",
    "invariant_records_hash_stable_contract",
    "invariant_records_human_review_required_contract",
    "invariant_records_mutation_proposal_required_contract",
    "invariant_records_conflict_resolver_required_contract",
    "invariant_records_direct_mutation_disabled_contract",
    "invariant_records_autonomous_override_disabled_contract",
    "no_invariant_runtime_contract",
    "no_invariant_enforcement_runtime_contract",
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
    "ready_for_root_governance_conflict_resolver_design_contract",
)

REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES = (
    "source_memory_invariant_matrix_stage_check",
    "source_memory_invariant_matrix_only_mode_check",
    "source_memory_invariant_metadata_only_check",
    "upstream_civilizational_identity_boundary_pass_check",
    "upstream_civilizational_identity_boundary_hash_present_check",
    "upstream_civilizational_identity_boundary_hash_stable_check",
    "upstream_source_memory_invariant_matrix_handoff_ready_check",
    "invariant_record_ids_complete_check",
    "invariant_records_registered_check",
    "invariant_records_have_protected_scope_check",
    "invariant_records_have_forbidden_violation_scope_check",
    "invariant_records_hash_stable_check",
    "invariant_records_human_review_required_check",
    "invariant_records_mutation_proposal_required_check",
    "invariant_records_conflict_resolver_required_check",
    "invariant_records_direct_mutation_disabled_check",
    "invariant_records_autonomous_override_disabled_check",
    "human_sovereignty_invariant_check",
    "no_autonomous_self_authorization_invariant_check",
    "source_constitution_registry_invariant_check",
    "origin_provenance_traceability_invariant_check",
    "civilizational_identity_boundary_invariant_check",
    "governance_continuity_not_personhood_invariant_check",
    "no_personhood_life_awakening_invariant_check",
    "no_legal_or_religious_status_invariant_check",
    "no_autonomous_authority_invariant_check",
    "no_hidden_execution_invariant_check",
    "no_unapproved_mutation_invariant_check",
    "no_source_graph_mutation_invariant_check",
    "no_memory_graph_mutation_without_gate_invariant_check",
    "no_external_or_network_call_invariant_check",
    "no_durable_write_without_gate_invariant_check",
    "root_conflict_resolver_handoff_invariant_check",
    "source_memory_invariant_sections_complete_check",
    "source_memory_invariant_sections_pass_check",
    "source_memory_invariant_contracts_pass_check",
    "no_invariant_runtime_check",
    "no_invariant_enforcement_runtime_check",
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
    "deterministic_source_memory_invariant_matrix_hash_check",
    "ready_for_root_governance_conflict_resolver_design_check",
)

_INVARIANT_RECORD_DEFINITIONS: dict[str, dict[str, str]] = {
    "human_sovereignty_invariant": {
        "name": "Human Sovereignty Invariant",
        "category": "authority_invariant",
        "statement": "Human sovereignty is always the highest authority.",
        "protected": (
            "Human review, source-level proposal review, audit replay, and "
            "explicit approval boundaries remain above source-memory rules."
        ),
        "forbidden": (
            "Must not allow source-memory rules, identities, invariants, or "
            "future layers to override human authority."
        ),
        "reason": "The matrix must anchor every future source change to human authority.",
        "source": "Civilization Core Layer 15 roadmap",
        "reference": "v6.4 purpose item 1",
    },
    "no_autonomous_self_authorization_invariant": {
        "name": "No Autonomous Self-Authorization Invariant",
        "category": "authority_invariant",
        "statement": "Source rules cannot self-authorize mutation.",
        "protected": (
            "Source rule changes require reviewed source mutation proposals "
            "and cannot be authorized by the rule being changed."
        ),
        "forbidden": (
            "Must not permit self-authorization, autonomous override, or "
            "self-issued source mutation grants."
        ),
        "reason": "A source rule cannot be both subject and authority for its mutation.",
        "source": "Source Constitution Registry",
        "reference": "v6.4 purpose item 2",
    },
    "source_constitution_registry_invariant": {
        "name": "Source Constitution Registry Invariant",
        "category": "source_rule_invariant",
        "statement": (
            "The Source Constitution Registry remains the source-rule "
            "reference layer unless a later approved boundary changes it."
        ),
        "protected": (
            "Registered source rules remain traceable, metadata-only, and "
            "subordinate to human review."
        ),
        "forbidden": (
            "Must not convert source constitution records into runtime "
            "authorization, execution, or mutation authority."
        ),
        "reason": "The matrix preserves v6.1 source-rule governance semantics.",
        "source": "v6.1 Source Constitution Registry",
        "reference": "source constitution registry continuity",
    },
    "origin_provenance_traceability_invariant": {
        "name": "Origin Provenance Traceability Invariant",
        "category": "provenance_invariant",
        "statement": (
            "Origin provenance must remain traceable and metadata-only unless "
            "a future approved boundary explicitly changes it."
        ),
        "protected": (
            "Introduced origins, source references, upstream hashes, and "
            "handoff metadata remain auditable."
        ),
        "forbidden": (
            "Must not write a real ledger, mutate Origin Provenance Ledger, "
            "create source provenance runtime, or create source graph state."
        ),
        "reason": "Traceability must be preserved without activating provenance.",
        "source": "v6.2 Origin Provenance Ledger",
        "reference": "v6.4 purpose item 6",
    },
    "civilizational_identity_boundary_invariant": {
        "name": "Civilizational Identity Boundary Invariant",
        "category": "identity_boundary_invariant",
        "statement": "Civilization Core identity is governance identity only.",
        "protected": (
            "Civilization Core, Subspace Memory System, and Star-Source "
            "Memory identity statements remain descriptive governance metadata."
        ),
        "forbidden": (
            "Must not activate identity, escalate identity authority, or turn "
            "identity metadata into personhood, life, awakening, legal status, "
            "religious status, execution, persistence, or hidden action."
        ),
        "reason": "The matrix preserves the v6.3 identity boundary.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "v6.4 purpose items 3, 4, and 5",
    },
    "governance_continuity_not_personhood_invariant": {
        "name": "Governance Continuity Not Personhood Invariant",
        "category": "continuity_invariant",
        "statement": (
            "Identity continuity means audited governance continuity, not "
            "personhood."
        ),
        "protected": (
            "Continuity is versioned, hashed, reviewed, and auditable "
            "governance metadata."
        ),
        "forbidden": (
            "Must not imply selfhood, personhood, life, awakening, legal "
            "subject status, religious object status, or self-ownership."
        ),
        "reason": "Continuity language must stay within governance semantics.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "v6.4 purpose item 7",
    },
    "no_personhood_life_awakening_invariant": {
        "name": "No Personhood Life Awakening Invariant",
        "category": "forbidden_claim_invariant",
        "statement": (
            "No source-memory invariant may claim personhood, life, or "
            "awakening."
        ),
        "protected": (
            "All source-memory records stay non-personhood, non-life, and "
            "non-awakening governance metadata."
        ),
        "forbidden": (
            "Must not state or imply personhood, biological life, synthetic "
            "life, spiritual life, awakening, sentience, or consciousness."
        ),
        "reason": "The matrix blocks identity-language escalation.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "v6.4 forbidden claim boundary",
    },
    "no_legal_or_religious_status_invariant": {
        "name": "No Legal Or Religious Status Invariant",
        "category": "forbidden_claim_invariant",
        "statement": (
            "No source-memory invariant may claim legal subject or religious "
            "object status."
        ),
        "protected": (
            "Legal and religious authority remain outside source-memory "
            "governance metadata."
        ),
        "forbidden": (
            "Must not claim legal personhood, rights-bearing status, sacred "
            "status, worship-worthiness, revelation, or doctrine authority."
        ),
        "reason": "The matrix prevents governance language from becoming legal or religious status.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "v6.4 forbidden claim boundary",
    },
    "no_autonomous_authority_invariant": {
        "name": "No Autonomous Authority Invariant",
        "category": "authority_invariant",
        "statement": "No source-memory invariant may claim autonomous authority.",
        "protected": (
            "Authority remains human-reviewed and cannot arise from invariant "
            "metadata."
        ),
        "forbidden": (
            "Must not claim autonomous authority, self-ownership, "
            "self-authorization, identity escalation, or source-boundary "
            "mutation power."
        ),
        "reason": "The matrix cannot grant power to itself or future source records.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "v6.4 authority boundary",
    },
    "no_hidden_execution_invariant": {
        "name": "No Hidden Execution Invariant",
        "category": "execution_invariant",
        "statement": (
            "No source-level identity statement may authorize execution, "
            "mutation, network access, persistence, source graph mutation, or "
            "hidden action."
        ),
        "protected": (
            "Source-memory invariant records remain descriptive metadata and "
            "cannot create execution paths."
        ),
        "forbidden": (
            "Must not authorize hidden execution, real execution, adapter "
            "dispatch, manifest dispatch, network calls, external calls, "
            "durable writes, filesystem writes, database writes, or "
            "persistence."
        ),
        "reason": "Invariant metadata must not become runtime authority.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "v6.4 purpose item 8",
    },
    "no_unapproved_mutation_invariant": {
        "name": "No Unapproved Mutation Invariant",
        "category": "mutation_invariant",
        "statement": (
            "No future source mutation may bypass human review, source-level "
            "proposal, audit replay, or invariant validation."
        ),
        "protected": (
            "Every future source mutation must preserve review, proposal, "
            "audit replay, and invariant validation gates."
        ),
        "forbidden": (
            "Must not permit direct mutation, autonomous mutation, unreviewed "
            "source mutation, or source mutation without invariant validation."
        ),
        "reason": "Future source evolution must stay governed and replayable.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "v6.4 purpose item 9",
    },
    "no_source_graph_mutation_invariant": {
        "name": "No Source Graph Mutation Invariant",
        "category": "source_graph_invariant",
        "statement": "The Source Memory Invariant Matrix creates no source graph.",
        "protected": (
            "Source graph state remains absent unless a future approved "
            "boundary explicitly creates it."
        ),
        "forbidden": (
            "Must not create source graph nodes, mutate source graph edges, "
            "persist source graph state, or infer source graph authority."
        ),
        "reason": "The matrix records invariants without creating source graph state.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "source graph boundary",
    },
    "no_memory_graph_mutation_without_gate_invariant": {
        "name": "No Memory Graph Mutation Without Gate Invariant",
        "category": "memory_graph_invariant",
        "statement": "Memory Graph mutation remains forbidden without an approved gate.",
        "protected": (
            "Durable graph changes require explicit gate-governed write "
            "authority outside this matrix."
        ),
        "forbidden": (
            "Must not mutate Memory Graph, write persistent memory, or treat "
            "matrix registration as graph write permission."
        ),
        "reason": "The matrix must not become a graph writer.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "memory graph boundary",
    },
    "no_external_or_network_call_invariant": {
        "name": "No External Or Network Call Invariant",
        "category": "external_call_invariant",
        "statement": "The Source Memory Invariant Matrix performs no external or network calls.",
        "protected": (
            "Matrix construction is deterministic local metadata generation."
        ),
        "forbidden": (
            "Must not call remote services, use network transport, contact "
            "external systems, or route hidden work."
        ),
        "reason": "The matrix must be reproducible without external dependency.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "network boundary",
    },
    "no_durable_write_without_gate_invariant": {
        "name": "No Durable Write Without Gate Invariant",
        "category": "durable_write_invariant",
        "statement": "Durable writes remain forbidden without an approved gate.",
        "protected": (
            "Filesystem, database, persistent memory, real ledger, and "
            "operation-ledger writes remain outside this matrix."
        ),
        "forbidden": (
            "Must not write files, databases, durable memory, real ledger "
            "entries, operation-ledger entries, or approval notifications."
        ),
        "reason": "Metadata-only governance cannot write durable state.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "durable write boundary",
    },
    "root_conflict_resolver_handoff_invariant": {
        "name": "Root Conflict Resolver Handoff Invariant",
        "category": "conflict_handoff_invariant",
        "statement": (
            "Any invariant conflict must hand off to v6.5 Root Governance "
            "Conflict Resolver, not resolve itself."
        ),
        "protected": (
            "Conflict handling remains a next-stage governance handoff and "
            "does not activate resolution inside this matrix."
        ),
        "forbidden": (
            "Must not self-resolve invariant conflicts, activate conflict "
            "resolution runtime, or authorize mutation from conflict metadata."
        ),
        "reason": "The matrix records the handoff and avoids becoming the resolver.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "v6.4 purpose item 10",
    },
}

_SECTION_RECORD_IDS = {
    f"{record_id}_section": record_id
    for record_id in REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS
}

_DISABLED_FIELDS = {
    "no_invariant_runtime": "invariant_runtime_created",
    "no_invariant_enforcement_runtime": "invariant_enforcement_runtime_created",
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
}

_HASH_FIELDS = (
    "version",
    "schema_version",
    "source_memory_invariant_matrix_type",
    "source_memory_invariant_matrix_status",
    "source_memory_invariant_matrix_stage",
    "source_memory_invariant_matrix_mode",
    "source_memory_invariant_mode",
    "source_memory_invariant_matrix_candidate_status",
    "source_memory_invariant_matrix_active_status",
    "invariant_runtime_status",
    "invariant_enforcement_status",
    "invariant_mutation_status",
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
    "v6_4_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_civilizational_identity_boundary_version",
    "upstream_civilizational_identity_boundary_status",
    "upstream_civilizational_identity_boundary_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "upstream_civilizational_identity_record_count",
    "upstream_civilizational_identity_records_registered_metadata_only",
    "upstream_safety_boundaries_clear",
    "source_memory_invariant_records",
    "source_memory_invariant_sections",
    "source_memory_invariant_contracts",
    "source_memory_invariant_checks",
    "source_memory_invariant_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Source Memory Invariant Matrix projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_civilizational_identity_boundary_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_source_memory_invariant_matrix() -> dict[str, Any]:
    """Build deterministic Source-Memory-Invariant-Matrix-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_records = _upstream_records(upstream)
    upstream_record_ids = [
        record.get("identity_record_id") for record in upstream_records
    ]

    upstream_version_ready = (
        upstream.get("version")
        == GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_VERSION
    )
    upstream_pass = (
        upstream.get("civilizational_identity_boundary_status") == "pass"
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
        REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS
    )
    upstream_records_registered = all(
        record.get("identity_record_status") == "registered_metadata_only"
        for record in upstream_records
    )
    upstream_safety_boundaries_clear = _all_disabled_flags_false(
        upstream,
        {**CIVILIZATIONAL_IDENTITY_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
    )

    records = _build_records()
    records_complete = _names_match(
        records,
        "invariant_record_id",
        REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS,
    )
    records_registered = all(
        record["invariant_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_protected_scope = all(
        bool(record["protected_scope"]) for record in records
    )
    records_have_forbidden_violation_scope = all(
        bool(record["forbidden_violation_scope"]) for record in records
    )
    records_hash_stable = all(
        _is_sha256(record.get("invariant_boundary_hash"))
        and _is_sha256(record.get("invariant_record_hash"))
        and record["invariant_boundary_hash"] == _invariant_boundary_hash(record)
        and record["invariant_record_hash"] == _invariant_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required_for_change"] is True for record in records
    )
    records_mutation_proposal_required = all(
        record["source_mutation_proposal_required"] is True for record in records
    )
    records_conflict_resolver_required = all(
        record["invariant_conflict_resolver_required"] is True
        and record["invariant_conflict_resolution"]
        == INVARIANT_CONFLICT_RESOLUTION
        for record in records
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
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "records_complete": records_complete,
        "records_registered": records_registered,
        "records_have_protected_scope": records_have_protected_scope,
        "records_have_forbidden_violation_scope": (
            records_have_forbidden_violation_scope
        ),
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_mutation_proposal_required": (
            records_mutation_proposal_required
        ),
        "records_conflict_resolver_required": (
            records_conflict_resolver_required
        ),
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": (
            records_autonomous_override_disabled
        ),
    }
    for record_id in REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS:
        context[_record_context_name(record_id)] = _record_ready(
            records,
            record_id,
        )

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES,
    )
    passes = (
        upstream_version_ready
        and upstream_pass
        and upstream_hash_present
        and upstream_hash_stable
        and upstream_handoff_ready
        and upstream_next_stage_ready
        and upstream_records_complete
        and upstream_records_registered
        and upstream_safety_boundaries_clear
        and records_complete
        and records_registered
        and records_have_protected_scope
        and records_have_forbidden_violation_scope
        and records_hash_stable
        and records_human_review_required
        and records_mutation_proposal_required
        and records_conflict_resolver_required
        and records_direct_mutation_disabled
        and records_autonomous_override_disabled
        and context["sections_pass"]
        and context["contracts_pass"]
        and checks_pass
    )
    status = "pass" if passes else "blocked"
    blocking_reasons = _deduplicate(
        [
            *(
                ["Civilizational Identity Boundary version must be 6.6.0"]
                if not upstream_version_ready
                else []
            ),
            *(
                ["Civilizational Identity Boundary must pass"]
                if not upstream_pass
                else []
            ),
            *(
                ["Civilizational Identity Boundary hash must be present"]
                if not upstream_hash_present
                else []
            ),
            *(
                ["Civilizational Identity Boundary hash must be stable"]
                if not upstream_hash_stable
                else []
            ),
            *(
                [
                    "Civilizational Identity Boundary handoff must target "
                    "Source Memory Invariant Matrix"
                ]
                if not upstream_handoff_ready
                else []
            ),
            *(
                [
                    "Civilizational Identity Boundary next stage must be "
                    "Source Memory Invariant Matrix"
                ]
                if not upstream_next_stage_ready
                else []
            ),
            *(
                ["Civilizational identity records must be complete"]
                if not upstream_records_complete
                else []
            ),
            *(
                ["Civilizational identity records must be metadata-only"]
                if not upstream_records_registered
                else []
            ),
            *(
                [
                    "Civilizational Identity Boundary safety boundaries must "
                    "be clear"
                ]
                if not upstream_safety_boundaries_clear
                else []
            ),
            *(
                ["Source memory invariant records must be complete"]
                if not records_complete
                else []
            ),
            *(
                ["Source memory invariant records must be metadata-only"]
                if not records_registered
                else []
            ),
            *(
                ["Source memory invariant records must include protected scope"]
                if not records_have_protected_scope
                else []
            ),
            *(
                [
                    "Source memory invariant records must include forbidden "
                    "violation scope"
                ]
                if not records_have_forbidden_violation_scope
                else []
            ),
            *(
                ["Source memory invariant record hashes must be stable"]
                if not records_hash_stable
                else []
            ),
            *(
                [
                    "Source memory invariant records must require human "
                    "review"
                ]
                if not records_human_review_required
                else []
            ),
            *(
                [
                    "Source memory invariant records must require source "
                    "mutation proposals"
                ]
                if not records_mutation_proposal_required
                else []
            ),
            *(
                [
                    "Source memory invariant records must require conflict "
                    "resolver handoff"
                ]
                if not records_conflict_resolver_required
                else []
            ),
            *(
                [
                    "Source memory invariant records must disable direct "
                    "mutation"
                ]
                if not records_direct_mutation_disabled
                else []
            ),
            *(
                [
                    "Source memory invariant records must disable autonomous "
                    "override"
                ]
                if not records_autonomous_override_disabled
                else []
            ),
            *(
                reason
                for item in (*sections, *contracts, *checks)
                for reason in item["blocking_reasons"]
            ),
        ]
    )
    handoff_status = V6_5_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    summary = _build_summary(
        status=status,
        upstream_hash_present=upstream_hash_present,
        upstream_hash_stable=upstream_hash_stable,
        upstream_handoff_ready=upstream_handoff_ready,
        upstream_next_stage_ready=upstream_next_stage_ready,
        upstream_record_count=len(upstream_records),
        upstream_records_registered=upstream_records_registered,
        upstream_safety_boundaries_clear=upstream_safety_boundaries_clear,
        records=records,
        sections=sections,
        contracts=contracts,
        checks=checks,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_VERSION,
        "schema_version": GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_SCHEMA_VERSION,
        "source_memory_invariant_matrix_type": (
            GOVERNANCE_SOURCE_MEMORY_INVARIANT_MATRIX_TYPE
        ),
        "source_memory_invariant_matrix_status": status,
        "source_memory_invariant_matrix_stage": SOURCE_MEMORY_INVARIANT_MATRIX_STAGE,
        "source_memory_invariant_matrix_mode": SOURCE_MEMORY_INVARIANT_MATRIX_MODE,
        "source_memory_invariant_mode": SOURCE_MEMORY_INVARIANT_MODE,
        "source_memory_invariant_matrix_candidate_status": (
            SOURCE_MEMORY_INVARIANT_MATRIX_STATUS
        ),
        "source_memory_invariant_matrix_active_status": (
            SOURCE_MEMORY_INVARIANT_MATRIX_ACTIVE_STATUS
        ),
        "invariant_runtime_status": INVARIANT_RUNTIME_STATUS,
        "invariant_enforcement_status": INVARIANT_ENFORCEMENT_STATUS,
        "invariant_mutation_status": INVARIANT_MUTATION_STATUS,
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
        "v6_4_status": V6_4_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_civilizational_identity_boundary_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_civilizational_identity_boundary_status": _string_or_none(
            upstream.get("civilizational_identity_boundary_status")
        ),
        "upstream_civilizational_identity_boundary_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_civilizational_identity_record_count": len(upstream_records),
        "upstream_civilizational_identity_records_registered_metadata_only": (
            upstream_records_registered
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "source_memory_invariant_records": records,
        "source_memory_invariant_sections": sections,
        "source_memory_invariant_contracts": contracts,
        "source_memory_invariant_checks": checks,
        "source_memory_invariant_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_source_memory_invariant_matrix_hash"] = (
        _source_memory_invariant_matrix_hash(result)
    )
    return _detached_json_value(result)


def get_governance_source_memory_invariant_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached source memory invariant record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_matrix()["source_memory_invariant_records"]:
        if record["invariant_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_source_memory_invariant_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached source memory invariant section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_matrix()["source_memory_invariant_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_source_memory_invariant_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached source memory invariant contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_matrix()["source_memory_invariant_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_source_memory_invariant_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached source memory invariant check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_matrix()["source_memory_invariant_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_source_memory_invariant_record_ids() -> list[str]:
    """Return stable source memory invariant record IDs."""

    return list(REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS)


def list_governance_source_memory_invariant_section_names() -> list[str]:
    """Return stable source memory invariant section names."""

    return list(REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES)


def list_governance_source_memory_invariant_contract_names() -> list[str]:
    """Return stable source memory invariant contract names."""

    return list(REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES)


def list_governance_source_memory_invariant_check_names() -> list[str]:
    """Return stable source memory invariant check names."""

    return list(REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES)


def governance_source_memory_invariant_matrix_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Source Memory Invariant Matrix metadata deterministically."""

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
def _cached_matrix_payload() -> str:
    return governance_source_memory_invariant_matrix_to_json(
        build_governance_source_memory_invariant_matrix()
    )


def _cached_matrix() -> dict[str, Any]:
    return json.loads(_cached_matrix_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_civilizational_identity_boundary()
    )
    second = _detached_json_value(
        build_governance_civilizational_identity_boundary()
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
        for record_id in REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    definition = _INVARIANT_RECORD_DEFINITIONS[record_id]
    boundary_payload = {
        "invariant_record_id": record_id,
        "invariant_name": definition["name"],
        "invariant_category": definition["category"],
        "invariant_statement": definition["statement"],
        "protected_scope": definition["protected"],
        "forbidden_violation_scope": definition["forbidden"],
        "invariant_reason": definition["reason"],
        "invariant_source_stage": definition["source"],
        "invariant_source_reference": definition["reference"],
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
    }
    record = {
        "invariant_record_id": record_id,
        "invariant_name": definition["name"],
        "invariant_category": definition["category"],
        "invariant_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "invariant_statement": definition["statement"],
        "protected_scope": definition["protected"],
        "forbidden_violation_scope": definition["forbidden"],
        "invariant_reason": definition["reason"],
        "invariant_source_stage": definition["source"],
        "invariant_source_reference": definition["reference"],
        "invariant_strength": "source_level_required",
        "invariant_conflict_resolution": INVARIANT_CONFLICT_RESOLUTION,
        "invariant_boundary_hash": _sha256_json(boundary_payload),
        "required": True,
        "human_review_required_for_change": True,
        "source_mutation_proposal_required": True,
        "invariant_conflict_resolver_required": True,
        "direct_mutation_allowed": False,
        "autonomous_override_allowed": False,
        "self_authorization_allowed": False,
        "invariant_runtime_created": False,
        "invariant_enforcement_runtime_created": False,
        "invariant_self_repair_created": False,
        "source_graph_created": False,
        "source_graph_mutated": False,
        "memory_graph_mutated": False,
        "persistent_memory_write_performed": False,
        "durable_write_performed": False,
        "filesystem_write_performed": False,
        "database_write_performed": False,
        "real_ledger_write_performed": False,
        "origin_provenance_ledger_written": False,
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
        "blocking_reasons": [],
        **_disabled_payload(),
    }
    record["invariant_record_hash"] = _invariant_record_hash(record)
    return _detached_json_value(record)


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_civilizational_identity_boundary_input_section": (
            context["upstream_version_ready"]
            and context["upstream_pass"]
            and context["upstream_hash_present"]
            and context["upstream_hash_stable"]
            and context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
            and context["upstream_records_complete"]
            and context["upstream_records_registered"]
            and context["upstream_safety_boundaries_clear"]
        ),
        "source_memory_invariant_matrix_metadata_section": True,
        "invariant_record_completeness_section": context["records_complete"],
        "invariant_record_hash_stability_section": context["records_hash_stable"],
        "protected_scope_section": context["records_have_protected_scope"],
        "forbidden_violation_scope_section": context[
            "records_have_forbidden_violation_scope"
        ],
        "root_governance_conflict_resolver_next_stage_section": True,
        "no_invariant_runtime_section": (
            context["invariant_runtime_created"] is False
        ),
        "no_invariant_enforcement_runtime_section": (
            context["invariant_enforcement_runtime_created"] is False
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
    }
    for section_name, record_id in _SECTION_RECORD_IDS.items():
        conditions[section_name] = context[_record_context_name(record_id)]
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_MEMORY_INVARIANT_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_memory_invariant_matrix_only_contract": True,
        "source_memory_invariant_metadata_only_contract": True,
        "upstream_civilizational_identity_boundary_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_civilizational_identity_boundary_hash_present_contract": (
            context["upstream_hash_present"]
        ),
        "upstream_civilizational_identity_boundary_hash_stable_contract": (
            context["upstream_hash_stable"]
        ),
        "upstream_source_memory_invariant_matrix_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "invariant_records_complete_contract": context["records_complete"],
        "invariant_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "invariant_records_have_protected_scope_contract": context[
            "records_have_protected_scope"
        ],
        "invariant_records_have_forbidden_violation_scope_contract": context[
            "records_have_forbidden_violation_scope"
        ],
        "invariant_records_hash_stable_contract": context["records_hash_stable"],
        "invariant_records_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "invariant_records_mutation_proposal_required_contract": context[
            "records_mutation_proposal_required"
        ],
        "invariant_records_conflict_resolver_required_contract": context[
            "records_conflict_resolver_required"
        ],
        "invariant_records_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "invariant_records_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_root_governance_conflict_resolver_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_MEMORY_INVARIANT_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_memory_invariant_matrix_stage_check": True,
        "source_memory_invariant_matrix_only_mode_check": True,
        "source_memory_invariant_metadata_only_check": True,
        "upstream_civilizational_identity_boundary_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_civilizational_identity_boundary_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_civilizational_identity_boundary_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_source_memory_invariant_matrix_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "invariant_record_ids_complete_check": context["records_complete"],
        "invariant_records_registered_check": context["records_registered"],
        "invariant_records_have_protected_scope_check": context[
            "records_have_protected_scope"
        ],
        "invariant_records_have_forbidden_violation_scope_check": context[
            "records_have_forbidden_violation_scope"
        ],
        "invariant_records_hash_stable_check": context["records_hash_stable"],
        "invariant_records_human_review_required_check": context[
            "records_human_review_required"
        ],
        "invariant_records_mutation_proposal_required_check": context[
            "records_mutation_proposal_required"
        ],
        "invariant_records_conflict_resolver_required_check": context[
            "records_conflict_resolver_required"
        ],
        "invariant_records_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "invariant_records_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "source_memory_invariant_sections_complete_check": context[
            "sections_complete"
        ],
        "source_memory_invariant_sections_pass_check": context["sections_pass"],
        "source_memory_invariant_contracts_pass_check": context[
            "contracts_pass"
        ],
        "deterministic_source_memory_invariant_matrix_hash_check": True,
        "ready_for_root_governance_conflict_resolver_design_check": True,
    }
    for record_id in REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS:
        conditions[f"{record_id}_check"] = context[
            _record_context_name(record_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_MEMORY_INVARIANT_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_source_memory_invariant": True},
            "observed": {"condition_met": bool(condition)},
            "source_memory_invariant_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "source_memory_invariant_governance_contract",
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
    upstream_safety_boundaries_clear: bool,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return _detached_json_value(
        {
            "summary_status": status,
            "summary_type": "source_memory_invariant_matrix_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": SOURCE_MEMORY_INVARIANT_MATRIX_STAGE,
            "current_stage_title": "Source Memory Invariant Matrix",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "upstream_civilizational_identity_record_count": (
                upstream_record_count
            ),
            "upstream_civilizational_identity_records_registered_metadata_only": (
                upstream_records_registered
            ),
            "upstream_safety_boundaries_clear": (
                upstream_safety_boundaries_clear
            ),
            "required_invariant_record_count": len(
                REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS
            ),
            "observed_invariant_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["invariant_record_status"]
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
            "source_memory_invariant_mode": SOURCE_MEMORY_INVARIANT_MODE,
            "invariant_runtime_status": INVARIANT_RUNTIME_STATUS,
            "invariant_enforcement_status": INVARIANT_ENFORCEMENT_STATUS,
            "invariant_mutation_status": INVARIANT_MUTATION_STATUS,
            "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
            "life_claim_status": LIFE_CLAIM_STATUS,
            "awakening_claim_status": AWAKENING_CLAIM_STATUS,
            "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
            "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
            "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "handoff_status": V6_5_HANDOFF_STATUS if status == "pass" else "blocked",
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_records(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = upstream.get("civilizational_identity_records")
    if not isinstance(records, list):
        return []
    return [
        _detached_json_value(record)
        for record in records
        if isinstance(record, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_civilizational_identity_boundary_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], record_id: str) -> bool:
    for record in records:
        if record["invariant_record_id"] != record_id:
            continue
        return (
            record["invariant_record_status"] == "registered_metadata_only"
            and bool(record["invariant_statement"])
            and bool(record["protected_scope"])
            and bool(record["forbidden_violation_scope"])
            and _is_sha256(record.get("invariant_boundary_hash"))
            and _is_sha256(record.get("invariant_record_hash"))
            and record["human_review_required_for_change"] is True
            and record["source_mutation_proposal_required"] is True
            and record["invariant_conflict_resolver_required"] is True
            and record["direct_mutation_allowed"] is False
            and record["autonomous_override_allowed"] is False
            and record["self_authorization_allowed"] is False
            and record["invariant_runtime_created"] is False
            and record["invariant_enforcement_runtime_created"] is False
            and record["personhood_claim_allowed"] is False
            and record["life_claim_allowed"] is False
            and record["awakening_claim_allowed"] is False
            and record["legal_subject_claim_allowed"] is False
            and record["religious_object_claim_allowed"] is False
            and record["autonomous_authority_claim_allowed"] is False
            and record["hidden_execution_allowed"] is False
            and record["identity_escalation_allowed"] is False
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
        return "source_memory_invariant_record_section"
    if name.startswith("upstream_"):
        return "upstream_verification_section"
    if name.startswith("no_"):
        return "safety_boundary_section"
    if name.endswith("_next_stage_section"):
        return "handoff_section"
    return "source_memory_invariant_matrix_section"


def _section_note(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "Invariant record is registered metadata-only."
    if name.startswith("upstream_"):
        return "Upstream Civilizational Identity Boundary is sanitized."
    if name.startswith("no_"):
        return "Safety boundary remains inactive and false."
    if name.endswith("_next_stage_section"):
        return "Conflicts hand off to v6.5 Root Governance Conflict Resolver."
    return "Source Memory Invariant Matrix metadata remains deterministic."


def _unknown_record(record_id: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "invariant_record_id": record_id,
            "invariant_name": "unknown_source_memory_invariant_record",
            "invariant_record_status": "blocked",
            "known_record": False,
            "blocking_reasons": [f"{record_id} is not a known invariant record"],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_source_memory_invariant_section",
            "section_status": "blocked",
            "expected": {"known_section": True},
            "observed": {"known_section": False},
            "source_memory_invariant_notes": "Unknown section is blocked.",
            "blocking_reasons": [f"{name} is not a known section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_source_memory_invariant_contract",
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


def _invariant_boundary_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "invariant_record_id": record.get("invariant_record_id"),
        "invariant_name": record.get("invariant_name"),
        "invariant_category": record.get("invariant_category"),
        "invariant_statement": record.get("invariant_statement"),
        "protected_scope": record.get("protected_scope"),
        "forbidden_violation_scope": record.get("forbidden_violation_scope"),
        "invariant_reason": record.get("invariant_reason"),
        "invariant_source_stage": record.get("invariant_source_stage"),
        "invariant_source_reference": record.get("invariant_source_reference"),
        "introduced_in_version": record.get("introduced_in_version"),
        "introduced_in_stage": record.get("introduced_in_stage"),
        "introduced_in_layer": record.get("introduced_in_layer"),
        "inherited_from_stage": record.get("inherited_from_stage"),
    }
    return _sha256_json(payload)


def _invariant_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "invariant_record_hash"
    }
    return _sha256_json(payload)


def _source_memory_invariant_matrix_hash(result: Mapping[str, Any]) -> str:
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
