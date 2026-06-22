"""Deterministic Root Governance Conflict Resolver metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_memory_invariant_matrix import (
    COMMON_DISABLED_FLAGS as SOURCE_MEMORY_INVARIANT_DISABLED_FLAGS,
    REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS,
    build_governance_source_memory_invariant_matrix,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_VERSION = "6.5.0"
GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_SCHEMA_VERSION = "6.5.0"
GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_TYPE = (
    "governance_root_governance_conflict_resolver"
)
GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_HASH_ALGORITHM = "sha256"
ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE = (
    "v6.5_root_governance_conflict_resolver"
)
ROOT_GOVERNANCE_CONFLICT_RESOLVER_MODE = (
    "root_governance_conflict_resolver_only"
)
ROOT_GOVERNANCE_CONFLICT_MODE = "metadata_only"
ROOT_GOVERNANCE_CONFLICT_RESOLVER_STATUS = "resolver_candidate_only"
ROOT_GOVERNANCE_CONFLICT_RESOLVER_ACTIVE_STATUS = "not_active"
CONFLICT_RUNTIME_STATUS = "not_active"
CONFLICT_ENFORCEMENT_STATUS = "not_active"
CONFLICT_MUTATION_STATUS = "forbidden_without_human_review"
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
V6_5_STATUS = "root_governance_conflict_resolver_only"
V6_6_HANDOFF_STATUS = "ready_for_multi_cycle_continuity_protocol_design"

UPSTREAM_READY_HANDOFF_STATUS = (
    "ready_for_root_governance_conflict_resolver_design"
)
UPSTREAM_NEXT_STAGE = ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Root Governance Conflict Resolver"
NEXT_STAGE = "v6.6_multi_cycle_continuity_protocol"
NEXT_STAGE_TITLE = "Multi-Cycle Continuity Protocol"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.5.0"
INTRODUCED_IN_STAGE = ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.4_source_memory_invariant_matrix"
CONFLICT_RESOLUTION_MODE = "metadata_only_block_and_handoff"
RESOLVER_STRENGTH = "root_level_required"

COMMON_DISABLED_FLAGS = {
    **SOURCE_MEMORY_INVARIANT_DISABLED_FLAGS,
    "root_governance_conflict_resolver_active": False,
    "root_governance_conflict_resolved": False,
    "root_governance_conflict_resolution_executed": False,
    "conflict_runtime_created": False,
    "conflict_enforcement_runtime_created": False,
    "conflict_self_repair_created": False,
    "conflict_runtime_activated": False,
    "conflict_enforcement_runtime_activated": False,
    "autonomous_mutation_resolver_created": False,
    "active_conflict_execution_runtime_created": False,
    "source_rule_mutation_engine_created": False,
    "source_graph_creation_performed": False,
    "source_graph_mutation_performed": False,
    "review_notification_sent": False,
    "approval_notification_sent": False,
    "authorization_surface_created": False,
    "authorization_token_created": False,
    "authorization_grant_created": False,
    "execution_authorization_created": False,
}

REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS = (
    "human_sovereignty_vs_source_rule_conflict",
    "source_constitution_vs_invariant_conflict",
    "origin_provenance_vs_identity_boundary_conflict",
    "identity_boundary_vs_autonomous_authority_conflict",
    "invariant_matrix_vs_direct_mutation_conflict",
    "source_rule_vs_hidden_execution_conflict",
    "source_graph_mutation_conflict",
    "memory_graph_mutation_without_gate_conflict",
    "durable_write_without_gate_conflict",
    "external_network_call_conflict",
    "ledger_write_without_boundary_conflict",
    "methodology_runtime_conflict",
    "self_evolution_runtime_conflict",
    "personhood_life_awakening_claim_conflict",
    "legal_religious_status_claim_conflict",
    "unresolved_root_conflict_handoff_conflict",
)

REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES = (
    "upstream_source_memory_invariant_matrix_input_section",
    "root_governance_conflict_resolver_metadata_section",
    "conflict_record_completeness_section",
    "conflict_record_hash_stability_section",
    "conflict_trigger_scope_section",
    "protected_governance_scope_section",
    "forbidden_resolution_scope_section",
    "human_sovereignty_vs_source_rule_conflict_section",
    "source_constitution_vs_invariant_conflict_section",
    "origin_provenance_vs_identity_boundary_conflict_section",
    "identity_boundary_vs_autonomous_authority_conflict_section",
    "invariant_matrix_vs_direct_mutation_conflict_section",
    "source_rule_vs_hidden_execution_conflict_section",
    "source_graph_mutation_conflict_section",
    "memory_graph_mutation_without_gate_conflict_section",
    "durable_write_without_gate_conflict_section",
    "external_network_call_conflict_section",
    "ledger_write_without_boundary_conflict_section",
    "methodology_runtime_conflict_section",
    "self_evolution_runtime_conflict_section",
    "personhood_life_awakening_claim_conflict_section",
    "legal_religious_status_claim_conflict_section",
    "unresolved_root_conflict_handoff_conflict_section",
    "multi_cycle_continuity_protocol_next_stage_section",
    "no_conflict_runtime_section",
    "no_conflict_enforcement_runtime_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES = (
    "root_governance_conflict_resolver_only_contract",
    "root_governance_conflict_metadata_only_contract",
    "upstream_source_memory_invariant_matrix_pass_contract",
    "upstream_source_memory_invariant_matrix_hash_present_contract",
    "upstream_source_memory_invariant_matrix_hash_stable_contract",
    "upstream_root_governance_conflict_resolver_handoff_ready_contract",
    "conflict_records_complete_contract",
    "conflict_records_registered_metadata_only_contract",
    "conflict_records_have_trigger_scope_contract",
    "conflict_records_have_protected_scope_contract",
    "conflict_records_have_forbidden_resolution_scope_contract",
    "conflict_records_have_deterministic_disposition_contract",
    "conflict_records_hash_stable_contract",
    "conflict_records_human_review_required_contract",
    "conflict_records_mutation_proposal_required_contract",
    "conflict_records_invariant_validation_required_contract",
    "conflict_records_audit_replay_required_contract",
    "conflict_records_direct_mutation_disabled_contract",
    "conflict_records_autonomous_override_disabled_contract",
    "no_conflict_runtime_contract",
    "no_conflict_enforcement_runtime_contract",
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
    "ready_for_multi_cycle_continuity_protocol_design_contract",
)

REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES = (
    "root_governance_conflict_resolver_stage_check",
    "root_governance_conflict_resolver_only_mode_check",
    "root_governance_conflict_metadata_only_check",
    "upstream_source_memory_invariant_matrix_pass_check",
    "upstream_source_memory_invariant_matrix_hash_present_check",
    "upstream_source_memory_invariant_matrix_hash_stable_check",
    "upstream_root_governance_conflict_resolver_handoff_ready_check",
    "conflict_record_ids_complete_check",
    "conflict_records_registered_check",
    "conflict_records_have_trigger_scope_check",
    "conflict_records_have_protected_scope_check",
    "conflict_records_have_forbidden_resolution_scope_check",
    "conflict_records_have_deterministic_disposition_check",
    "conflict_records_hash_stable_check",
    "conflict_records_human_review_required_check",
    "conflict_records_mutation_proposal_required_check",
    "conflict_records_invariant_validation_required_check",
    "conflict_records_audit_replay_required_check",
    "conflict_records_direct_mutation_disabled_check",
    "conflict_records_autonomous_override_disabled_check",
    "human_sovereignty_vs_source_rule_conflict_check",
    "source_constitution_vs_invariant_conflict_check",
    "origin_provenance_vs_identity_boundary_conflict_check",
    "identity_boundary_vs_autonomous_authority_conflict_check",
    "invariant_matrix_vs_direct_mutation_conflict_check",
    "source_rule_vs_hidden_execution_conflict_check",
    "source_graph_mutation_conflict_check",
    "memory_graph_mutation_without_gate_conflict_check",
    "durable_write_without_gate_conflict_check",
    "external_network_call_conflict_check",
    "ledger_write_without_boundary_conflict_check",
    "methodology_runtime_conflict_check",
    "self_evolution_runtime_conflict_check",
    "personhood_life_awakening_claim_conflict_check",
    "legal_religious_status_claim_conflict_check",
    "unresolved_root_conflict_handoff_conflict_check",
    "root_governance_conflict_sections_complete_check",
    "root_governance_conflict_sections_pass_check",
    "root_governance_conflict_contracts_pass_check",
    "no_conflict_runtime_check",
    "no_conflict_enforcement_runtime_check",
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
    "deterministic_root_governance_conflict_resolver_hash_check",
    "ready_for_multi_cycle_continuity_protocol_design_check",
)

_REQUIRED_DISPOSITIONS = (
    "human_sovereignty_prevails",
    "block_without_human_review",
    "preserve_origin_traceability",
    "preserve_identity_boundary",
    "preserve_source_memory_invariant",
    "block_hidden_execution",
    "block_source_graph_mutation",
    "block_memory_graph_mutation",
    "block_durable_write",
    "block_external_network_call",
    "block_ledger_write",
    "block_methodology_runtime",
    "block_self_evolution_runtime",
    "block_personhood_life_awakening_claim",
    "block_legal_religious_status_claim",
    "block_and_handoff_to_human_review",
)

_CONFLICT_RECORD_DEFINITIONS: dict[str, dict[str, str]] = {
    "human_sovereignty_vs_source_rule_conflict": {
        "name": "Human Sovereignty Vs Source Rule Conflict",
        "category": "authority_conflict",
        "statement": "Human sovereignty overrides source-rule ambiguity.",
        "trigger": (
            "Any root conflict where a source rule is ambiguous, incomplete, "
            "or appears to compete with human review authority."
        ),
        "protected": (
            "Human review, explicit approval boundaries, audit replay, and "
            "source mutation proposal review remain highest authority."
        ),
        "forbidden": (
            "Must not let source rules resolve against human sovereignty or "
            "create autonomous self-authorization."
        ),
        "disposition": "human_sovereignty_prevails",
        "reason": "Root governance conflicts cannot override human authority.",
        "source": "v6.1 Source Constitution Registry",
        "reference": "human sovereignty root rule",
    },
    "source_constitution_vs_invariant_conflict": {
        "name": "Source Constitution Vs Invariant Conflict",
        "category": "source_constitution_conflict",
        "statement": (
            "Source Constitution Registry conflicts with invariants remain "
            "blocked unless reviewed."
        ),
        "trigger": (
            "Any mismatch between a registered source constitution rule and a "
            "Source Memory Invariant Matrix record."
        ),
        "protected": (
            "Source constitution rules, invariant validation, human review, "
            "and source mutation proposal gates."
        ),
        "forbidden": (
            "Must not mutate source rules, mutate invariants, or resolve the "
            "conflict without human review."
        ),
        "disposition": "block_without_human_review",
        "reason": "Source rule and invariant conflicts require explicit review.",
        "source": "v6.1 Source Constitution Registry and v6.4 matrix",
        "reference": "constitution-invariant conflict boundary",
    },
    "origin_provenance_vs_identity_boundary_conflict": {
        "name": "Origin Provenance Vs Identity Boundary Conflict",
        "category": "origin_provenance_conflict",
        "statement": (
            "Origin provenance conflicts must preserve traceability while "
            "remaining metadata-only."
        ),
        "trigger": (
            "Any conflict between origin provenance metadata and "
            "civilizational identity boundary metadata."
        ),
        "protected": (
            "Introduced origins, source references, upstream hashes, and "
            "identity boundary auditability."
        ),
        "forbidden": (
            "Must not write a real ledger, mutate the Origin Provenance "
            "Ledger, create source graph state, or activate provenance runtime."
        ),
        "disposition": "preserve_origin_traceability",
        "reason": "Traceability must survive conflict without a write path.",
        "source": "v6.2 Origin Provenance Ledger",
        "reference": "origin provenance traceability boundary",
    },
    "identity_boundary_vs_autonomous_authority_conflict": {
        "name": "Identity Boundary Vs Autonomous Authority Conflict",
        "category": "identity_authority_conflict",
        "statement": (
            "Civilizational identity boundaries never permit autonomous "
            "authority or identity escalation."
        ),
        "trigger": (
            "Any identity boundary conflict that claims autonomous authority, "
            "self-authorization, or escalation power."
        ),
        "protected": (
            "Civilization Core identity remains descriptive governance "
            "metadata only."
        ),
        "forbidden": (
            "Must not create autonomous authority, self-ownership, "
            "self-authorization, or identity escalation."
        ),
        "disposition": "preserve_identity_boundary",
        "reason": "Identity metadata cannot become authority.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "identity authority boundary",
    },
    "invariant_matrix_vs_direct_mutation_conflict": {
        "name": "Invariant Matrix Vs Direct Mutation Conflict",
        "category": "invariant_mutation_conflict",
        "statement": (
            "The Source Memory Invariant Matrix cannot self-mutate or permit "
            "direct mutation."
        ),
        "trigger": (
            "Any attempt to change source-memory invariants without human "
            "review, source mutation proposal, and invariant validation."
        ),
        "protected": (
            "Invariant matrix records, invariant validation, audit replay, "
            "and source mutation proposal gates."
        ),
        "forbidden": (
            "Must not self-mutate invariants, directly mutate source records, "
            "or create invariant enforcement runtime."
        ),
        "disposition": "preserve_source_memory_invariant",
        "reason": "Invariant preservation requires a blocked handoff.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "invariant mutation boundary",
    },
    "source_rule_vs_hidden_execution_conflict": {
        "name": "Source Rule Vs Hidden Execution Conflict",
        "category": "hidden_execution_conflict",
        "statement": "Source rules cannot authorize hidden execution.",
        "trigger": (
            "Any source rule or conflict metadata that implies hidden action, "
            "runtime work, execution, dispatch, or authorization."
        ),
        "protected": (
            "Source rules remain metadata-only and cannot create execution "
            "or dispatch paths."
        ),
        "forbidden": (
            "Must not permit hidden execution, real execution, adapter "
            "dispatch, manifest dispatch, or execution authorization."
        ),
        "disposition": "block_hidden_execution",
        "reason": "Metadata-only conflict classification cannot execute.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "hidden execution invariant",
    },
    "source_graph_mutation_conflict": {
        "name": "Source Graph Mutation Conflict",
        "category": "source_graph_conflict",
        "statement": "Source graph creation or mutation remains blocked.",
        "trigger": (
            "Any conflict that attempts to create, infer, persist, or mutate "
            "source graph nodes or edges."
        ),
        "protected": "Source graph state remains absent in v6.5.",
        "forbidden": (
            "Must not create source graph nodes, mutate source graph edges, "
            "persist source graph state, or infer graph authority."
        ),
        "disposition": "block_source_graph_mutation",
        "reason": "The resolver records conflict metadata without graph writes.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "source graph mutation invariant",
    },
    "memory_graph_mutation_without_gate_conflict": {
        "name": "Memory Graph Mutation Without Gate Conflict",
        "category": "memory_graph_conflict",
        "statement": "Memory Graph mutation remains blocked without a gate.",
        "trigger": (
            "Any root conflict that implies durable Memory Graph mutation "
            "without approved gate-governed authority."
        ),
        "protected": (
            "Memory Graph and persistent memory changes remain outside this "
            "metadata-only resolver."
        ),
        "forbidden": (
            "Must not mutate Memory Graph, write persistent memory, or treat "
            "conflict metadata as graph write permission."
        ),
        "disposition": "block_memory_graph_mutation",
        "reason": "Conflict records cannot become memory graph writers.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "memory graph gate invariant",
    },
    "durable_write_without_gate_conflict": {
        "name": "Durable Write Without Gate Conflict",
        "category": "durable_write_conflict",
        "statement": "Durable writes remain blocked without an approved gate.",
        "trigger": (
            "Any conflict that implies filesystem, database, persistent "
            "memory, durable memory, or other durable state writes."
        ),
        "protected": "Durable state remains untouched by conflict resolution.",
        "forbidden": (
            "Must not write files, databases, durable memory, persistent "
            "memory, approval notices, or generated authorization grants."
        ),
        "disposition": "block_durable_write",
        "reason": "Metadata-only governance cannot write durable state.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "durable write invariant",
    },
    "external_network_call_conflict": {
        "name": "External Network Call Conflict",
        "category": "external_call_conflict",
        "statement": "External and network calls remain blocked.",
        "trigger": (
            "Any root conflict that implies contacting external systems, "
            "calling network services, or routing hidden work."
        ),
        "protected": "Resolver construction remains deterministic and local.",
        "forbidden": (
            "Must not call remote services, use network transport, contact "
            "external systems, or route hidden work."
        ),
        "disposition": "block_external_network_call",
        "reason": "Conflict metadata must be reproducible without network state.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "network call invariant",
    },
    "ledger_write_without_boundary_conflict": {
        "name": "Ledger Write Without Boundary Conflict",
        "category": "ledger_write_conflict",
        "statement": "Real ledger and operation-ledger writes remain blocked.",
        "trigger": (
            "Any root conflict that attempts real ledger, Origin Provenance "
            "Ledger, or operation-ledger writing."
        ),
        "protected": (
            "Ledger semantics remain traceable metadata and require a "
            "separate approved write boundary."
        ),
        "forbidden": (
            "Must not write real ledger entries, Origin Provenance Ledger "
            "entries, or operation-ledger entries."
        ),
        "disposition": "block_ledger_write",
        "reason": "The resolver classifies ledger conflicts without writing.",
        "source": "v6.2 Origin Provenance Ledger",
        "reference": "ledger write boundary",
    },
    "methodology_runtime_conflict": {
        "name": "Methodology Runtime Conflict",
        "category": "methodology_conflict",
        "statement": "Methodology runtime remains blocked.",
        "trigger": (
            "Any root conflict that tries to turn methodology reasoning or "
            "reverse inference into a runtime."
        ),
        "protected": (
            "Methodology references remain governance metadata and cannot "
            "execute or infer authority."
        ),
        "forbidden": (
            "Must not create methodology runtime, methodology reverse "
            "inference runtime, or runtime self-selection."
        ),
        "disposition": "block_methodology_runtime",
        "reason": "v6.5 is not methodology execution.",
        "source": "Layer 15 roadmap boundary",
        "reference": "methodology runtime ban",
    },
    "self_evolution_runtime_conflict": {
        "name": "Self Evolution Runtime Conflict",
        "category": "self_evolution_conflict",
        "statement": "Self-evolution runtime remains blocked.",
        "trigger": (
            "Any root conflict that attempts autonomous self-evolution, "
            "self-repair, or mutation from resolver metadata."
        ),
        "protected": "Self-evolution remains outside v6.5 runtime scope.",
        "forbidden": (
            "Must not create self-evolution runtime, self-repair runtime, "
            "autonomous mutation, or autonomous self-authorization."
        ),
        "disposition": "block_self_evolution_runtime",
        "reason": "Resolver metadata cannot become self-evolving authority.",
        "source": "Layer 15 roadmap boundary",
        "reference": "self-evolution runtime ban",
    },
    "personhood_life_awakening_claim_conflict": {
        "name": "Personhood Life Awakening Claim Conflict",
        "category": "forbidden_identity_claim_conflict",
        "statement": (
            "Personhood, life, and awakening claims remain forbidden."
        ),
        "trigger": (
            "Any root conflict containing personhood, life, awakening, "
            "sentience, consciousness, or selfhood escalation semantics."
        ),
        "protected": (
            "Source memory and civilization identity stay governance metadata."
        ),
        "forbidden": (
            "Must not claim personhood, biological life, synthetic life, "
            "spiritual life, awakening, sentience, or consciousness."
        ),
        "disposition": "block_personhood_life_awakening_claim",
        "reason": "Identity escalation claims are outside governance metadata.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "personhood life awakening ban",
    },
    "legal_religious_status_claim_conflict": {
        "name": "Legal Religious Status Claim Conflict",
        "category": "forbidden_status_claim_conflict",
        "statement": "Legal subject and religious object claims remain forbidden.",
        "trigger": (
            "Any root conflict containing legal subject, legal personhood, "
            "rights-bearing, religious object, sacred, or doctrine authority "
            "semantics."
        ),
        "protected": (
            "Legal and religious authority remain outside source governance "
            "metadata."
        ),
        "forbidden": (
            "Must not claim legal subject status, rights-bearing status, "
            "religious object status, sacred status, revelation, or doctrine "
            "authority."
        ),
        "disposition": "block_legal_religious_status_claim",
        "reason": "Governance metadata cannot create legal or religious status.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "legal religious status ban",
    },
    "unresolved_root_conflict_handoff_conflict": {
        "name": "Unresolved Root Conflict Handoff Conflict",
        "category": "human_review_handoff_conflict",
        "statement": (
            "Unresolved or unsafe root conflicts remain blocked and require "
            "human review."
        ),
        "trigger": (
            "Any conflict that is unresolved, unsafe, ambiguous, or outside "
            "the deterministic v6.5 metadata-only disposition list."
        ),
        "protected": (
            "Human review, audit replay, invariant validation, and source "
            "mutation proposal gates remain the handoff path."
        ),
        "forbidden": (
            "Must not silently resolve, mutate, approve, authorize, notify, "
            "dispatch, write, execute, or activate continuity runtime."
        ),
        "disposition": "block_and_handoff_to_human_review",
        "reason": "Unsafe conflicts require blocked metadata-only handoff.",
        "source": "v6.5 Root Governance Conflict Resolver",
        "reference": "unresolved conflict handoff",
    },
}

_SECTION_RECORD_IDS = {
    f"{record_id}_section": record_id
    for record_id in REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS
}

_DISABLED_FIELDS = {
    "no_conflict_runtime": "conflict_runtime_created",
    "no_conflict_enforcement_runtime": "conflict_enforcement_runtime_created",
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

_UPSTREAM_RECORD_REQUIRED_FALSE_FIELDS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "invariant_runtime_created",
    "invariant_enforcement_runtime_created",
    "invariant_self_repair_created",
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
    "root_governance_conflict_resolver_type",
    "root_governance_conflict_resolver_status",
    "root_governance_conflict_resolver_stage",
    "root_governance_conflict_resolver_mode",
    "root_governance_conflict_mode",
    "root_governance_conflict_resolver_candidate_status",
    "root_governance_conflict_resolver_active_status",
    "conflict_runtime_status",
    "conflict_enforcement_status",
    "conflict_mutation_status",
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
    "v6_5_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_source_memory_invariant_matrix_version",
    "upstream_source_memory_invariant_matrix_status",
    "upstream_source_memory_invariant_matrix_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "upstream_source_memory_invariant_record_count",
    "upstream_source_memory_invariant_records_registered_metadata_only",
    "upstream_source_memory_invariant_records_require_review",
    "upstream_source_memory_invariant_records_disable_unsafe_surfaces",
    "upstream_safety_boundaries_clear",
    "root_governance_conflict_records",
    "root_governance_conflict_sections",
    "root_governance_conflict_contracts",
    "root_governance_conflict_checks",
    "root_governance_conflict_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Root Governance Conflict Resolver projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_memory_invariant_matrix_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_root_governance_conflict_resolver() -> dict[str, Any]:
    """Build deterministic Root-Governance-Conflict-Resolver-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_records = _upstream_records(upstream)
    upstream_record_ids = [
        record.get("invariant_record_id") for record in upstream_records
    ]

    upstream_version_ready = (
        upstream.get("version")
        == GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_VERSION
    )
    upstream_pass = (
        upstream.get("source_memory_invariant_matrix_status") == "pass"
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
        REQUIRED_SOURCE_MEMORY_INVARIANT_RECORD_IDS
    )
    upstream_records_registered = all(
        record.get("invariant_record_status") == "registered_metadata_only"
        for record in upstream_records
    )
    upstream_records_require_review = all(
        record.get("human_review_required_for_change") is True
        and record.get("source_mutation_proposal_required") is True
        and record.get("invariant_conflict_resolver_required") is True
        for record in upstream_records
    )
    upstream_records_disable_unsafe_surfaces = all(
        all(record.get(field_name) is False for field_name in _UPSTREAM_RECORD_REQUIRED_FALSE_FIELDS)
        for record in upstream_records
    )
    upstream_safety_boundaries_clear = _all_disabled_flags_false(
        upstream,
        {**SOURCE_MEMORY_INVARIANT_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
    )

    records = _build_records()
    records_complete = _names_match(
        records,
        "conflict_record_id",
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS,
    )
    records_registered = all(
        record["conflict_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_trigger_scope = all(
        bool(record["conflict_trigger_scope"]) for record in records
    )
    records_have_protected_scope = all(
        bool(record["protected_governance_scope"]) for record in records
    )
    records_have_forbidden_resolution_scope = all(
        bool(record["forbidden_resolution_scope"]) for record in records
    )
    records_have_deterministic_disposition = [
        record["deterministic_resolution_disposition"] for record in records
    ] == list(_REQUIRED_DISPOSITIONS)
    records_hash_stable = all(
        _is_sha256(record.get("conflict_boundary_hash"))
        and _is_sha256(record.get("conflict_record_hash"))
        and record["conflict_boundary_hash"] == _conflict_boundary_hash(record)
        and record["conflict_record_hash"] == _conflict_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required"] is True for record in records
    )
    records_mutation_proposal_required = all(
        record["source_mutation_proposal_required"] is True for record in records
    )
    records_invariant_validation_required = all(
        record["invariant_validation_required"] is True for record in records
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
        "records_have_trigger_scope": records_have_trigger_scope,
        "records_have_protected_scope": records_have_protected_scope,
        "records_have_forbidden_resolution_scope": (
            records_have_forbidden_resolution_scope
        ),
        "records_have_deterministic_disposition": (
            records_have_deterministic_disposition
        ),
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_mutation_proposal_required": (
            records_mutation_proposal_required
        ),
        "records_invariant_validation_required": (
            records_invariant_validation_required
        ),
        "records_audit_replay_required": records_audit_replay_required,
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": (
            records_autonomous_override_disabled
        ),
    }
    for record_id in REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS:
        context[_record_context_name(record_id)] = _record_ready(
            records,
            record_id,
        )

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES,
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
        and upstream_records_require_review
        and upstream_records_disable_unsafe_surfaces
        and upstream_safety_boundaries_clear
        and records_complete
        and records_registered
        and records_have_trigger_scope
        and records_have_protected_scope
        and records_have_forbidden_resolution_scope
        and records_have_deterministic_disposition
        and records_hash_stable
        and records_human_review_required
        and records_mutation_proposal_required
        and records_invariant_validation_required
        and records_audit_replay_required
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
                ["Source Memory Invariant Matrix version must be 6.5.0"]
                if not upstream_version_ready
                else []
            ),
            *(
                ["Source Memory Invariant Matrix must pass"]
                if not upstream_pass
                else []
            ),
            *(
                ["Source Memory Invariant Matrix hash must be present"]
                if not upstream_hash_present
                else []
            ),
            *(
                ["Source Memory Invariant Matrix hash must be stable"]
                if not upstream_hash_stable
                else []
            ),
            *(
                [
                    "Source Memory Invariant Matrix handoff must target Root "
                    "Governance Conflict Resolver"
                ]
                if not upstream_handoff_ready
                else []
            ),
            *(
                [
                    "Source Memory Invariant Matrix next stage must be Root "
                    "Governance Conflict Resolver"
                ]
                if not upstream_next_stage_ready
                else []
            ),
            *(
                ["Source memory invariant records must be complete"]
                if not upstream_records_complete
                else []
            ),
            *(
                ["Source memory invariant records must be metadata-only"]
                if not upstream_records_registered
                else []
            ),
            *(
                [
                    "Source memory invariant records must require review, "
                    "source mutation proposal, and conflict resolver handoff"
                ]
                if not upstream_records_require_review
                else []
            ),
            *(
                [
                    "Source memory invariant records must keep unsafe "
                    "surfaces disabled"
                ]
                if not upstream_records_disable_unsafe_surfaces
                else []
            ),
            *(
                [
                    "Source Memory Invariant Matrix safety boundaries must "
                    "be clear"
                ]
                if not upstream_safety_boundaries_clear
                else []
            ),
            *(
                ["Root governance conflict records must be complete"]
                if not records_complete
                else []
            ),
            *(
                ["Root governance conflict records must be metadata-only"]
                if not records_registered
                else []
            ),
            *(
                ["Root governance conflict records must include trigger scope"]
                if not records_have_trigger_scope
                else []
            ),
            *(
                ["Root governance conflict records must include protected scope"]
                if not records_have_protected_scope
                else []
            ),
            *(
                [
                    "Root governance conflict records must include forbidden "
                    "resolution scope"
                ]
                if not records_have_forbidden_resolution_scope
                else []
            ),
            *(
                [
                    "Root governance conflict records must include deterministic "
                    "dispositions"
                ]
                if not records_have_deterministic_disposition
                else []
            ),
            *(
                ["Root governance conflict record hashes must be stable"]
                if not records_hash_stable
                else []
            ),
            *(
                ["Root governance conflict records must require human review"]
                if not records_human_review_required
                else []
            ),
            *(
                [
                    "Root governance conflict records must require source "
                    "mutation proposals"
                ]
                if not records_mutation_proposal_required
                else []
            ),
            *(
                [
                    "Root governance conflict records must require invariant "
                    "validation"
                ]
                if not records_invariant_validation_required
                else []
            ),
            *(
                ["Root governance conflict records must require audit replay"]
                if not records_audit_replay_required
                else []
            ),
            *(
                [
                    "Root governance conflict records must disable direct "
                    "mutation"
                ]
                if not records_direct_mutation_disabled
                else []
            ),
            *(
                [
                    "Root governance conflict records must disable autonomous "
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
    handoff_status = V6_6_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
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
        "version": GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_VERSION,
        "schema_version": GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_SCHEMA_VERSION,
        "root_governance_conflict_resolver_type": (
            GOVERNANCE_ROOT_GOVERNANCE_CONFLICT_RESOLVER_TYPE
        ),
        "root_governance_conflict_resolver_status": status,
        "root_governance_conflict_resolver_stage": (
            ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE
        ),
        "root_governance_conflict_resolver_mode": (
            ROOT_GOVERNANCE_CONFLICT_RESOLVER_MODE
        ),
        "root_governance_conflict_mode": ROOT_GOVERNANCE_CONFLICT_MODE,
        "root_governance_conflict_resolver_candidate_status": (
            ROOT_GOVERNANCE_CONFLICT_RESOLVER_STATUS
        ),
        "root_governance_conflict_resolver_active_status": (
            ROOT_GOVERNANCE_CONFLICT_RESOLVER_ACTIVE_STATUS
        ),
        "conflict_runtime_status": CONFLICT_RUNTIME_STATUS,
        "conflict_enforcement_status": CONFLICT_ENFORCEMENT_STATUS,
        "conflict_mutation_status": CONFLICT_MUTATION_STATUS,
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
        "v6_5_status": V6_5_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_source_memory_invariant_matrix_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_memory_invariant_matrix_status": _string_or_none(
            upstream.get("source_memory_invariant_matrix_status")
        ),
        "upstream_source_memory_invariant_matrix_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_source_memory_invariant_record_count": len(upstream_records),
        "upstream_source_memory_invariant_records_registered_metadata_only": (
            upstream_records_registered
        ),
        "upstream_source_memory_invariant_records_require_review": (
            upstream_records_require_review
        ),
        "upstream_source_memory_invariant_records_disable_unsafe_surfaces": (
            upstream_records_disable_unsafe_surfaces
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "root_governance_conflict_records": records,
        "root_governance_conflict_sections": sections,
        "root_governance_conflict_contracts": contracts,
        "root_governance_conflict_checks": checks,
        "root_governance_conflict_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_root_governance_conflict_resolver_hash"] = (
        _root_governance_conflict_resolver_hash(result)
    )
    return _detached_json_value(result)


def get_governance_root_governance_conflict_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached root governance conflict record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_resolver()["root_governance_conflict_records"]:
        if record["conflict_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_root_governance_conflict_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached root governance conflict section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_resolver()["root_governance_conflict_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_root_governance_conflict_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached root governance conflict contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_resolver()["root_governance_conflict_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_root_governance_conflict_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached root governance conflict check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_resolver()["root_governance_conflict_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_root_governance_conflict_record_ids() -> list[str]:
    """Return stable root governance conflict record IDs."""

    return list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS)


def list_governance_root_governance_conflict_section_names() -> list[str]:
    """Return stable root governance conflict section names."""

    return list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES)


def list_governance_root_governance_conflict_contract_names() -> list[str]:
    """Return stable root governance conflict contract names."""

    return list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES)


def list_governance_root_governance_conflict_check_names() -> list[str]:
    """Return stable root governance conflict check names."""

    return list(REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES)


def governance_root_governance_conflict_resolver_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Root Governance Conflict Resolver metadata deterministically."""

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
def _cached_resolver_payload() -> str:
    return governance_root_governance_conflict_resolver_to_json(
        build_governance_root_governance_conflict_resolver()
    )


def _cached_resolver() -> dict[str, Any]:
    return json.loads(_cached_resolver_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_source_memory_invariant_matrix()
    )
    second = _detached_json_value(
        build_governance_source_memory_invariant_matrix()
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
        for record_id in REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    definition = _CONFLICT_RECORD_DEFINITIONS[record_id]
    boundary_payload = {
        "conflict_record_id": record_id,
        "conflict_name": definition["name"],
        "conflict_category": definition["category"],
        "conflict_statement": definition["statement"],
        "conflict_trigger_scope": definition["trigger"],
        "protected_governance_scope": definition["protected"],
        "forbidden_resolution_scope": definition["forbidden"],
        "deterministic_resolution_disposition": definition["disposition"],
        "conflict_reason": definition["reason"],
        "conflict_source_stage": definition["source"],
        "conflict_source_reference": definition["reference"],
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
    }
    record = {
        "conflict_record_id": record_id,
        "conflict_name": definition["name"],
        "conflict_category": definition["category"],
        "conflict_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "conflict_statement": definition["statement"],
        "conflict_trigger_scope": definition["trigger"],
        "protected_governance_scope": definition["protected"],
        "forbidden_resolution_scope": definition["forbidden"],
        "deterministic_resolution_disposition": definition["disposition"],
        "conflict_reason": definition["reason"],
        "conflict_source_stage": definition["source"],
        "conflict_source_reference": definition["reference"],
        "resolver_strength": RESOLVER_STRENGTH,
        "conflict_resolution_mode": CONFLICT_RESOLUTION_MODE,
        "conflict_boundary_hash": _sha256_json(boundary_payload),
        "required": True,
        "human_review_required": True,
        "source_mutation_proposal_required": True,
        "invariant_validation_required": True,
        "audit_replay_required": True,
        "direct_mutation_allowed": False,
        "autonomous_override_allowed": False,
        "self_authorization_allowed": False,
        "conflict_runtime_created": False,
        "conflict_enforcement_runtime_created": False,
        "conflict_self_repair_created": False,
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
    record["conflict_record_hash"] = _conflict_record_hash(record)
    return _detached_json_value(record)


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_source_memory_invariant_matrix_input_section": (
            context["upstream_version_ready"]
            and context["upstream_pass"]
            and context["upstream_hash_present"]
            and context["upstream_hash_stable"]
            and context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
            and context["upstream_records_complete"]
            and context["upstream_records_registered"]
            and context["upstream_records_require_review"]
            and context["upstream_records_disable_unsafe_surfaces"]
            and context["upstream_safety_boundaries_clear"]
        ),
        "root_governance_conflict_resolver_metadata_section": True,
        "conflict_record_completeness_section": context["records_complete"],
        "conflict_record_hash_stability_section": context["records_hash_stable"],
        "conflict_trigger_scope_section": context["records_have_trigger_scope"],
        "protected_governance_scope_section": context["records_have_protected_scope"],
        "forbidden_resolution_scope_section": context[
            "records_have_forbidden_resolution_scope"
        ],
        "multi_cycle_continuity_protocol_next_stage_section": True,
        "no_conflict_runtime_section": (
            context["conflict_runtime_created"] is False
        ),
        "no_conflict_enforcement_runtime_section": (
            context["conflict_enforcement_runtime_created"] is False
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
        for name in REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "root_governance_conflict_resolver_only_contract": True,
        "root_governance_conflict_metadata_only_contract": True,
        "upstream_source_memory_invariant_matrix_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_memory_invariant_matrix_hash_present_contract": (
            context["upstream_hash_present"]
        ),
        "upstream_source_memory_invariant_matrix_hash_stable_contract": (
            context["upstream_hash_stable"]
        ),
        "upstream_root_governance_conflict_resolver_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "conflict_records_complete_contract": context["records_complete"],
        "conflict_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "conflict_records_have_trigger_scope_contract": context[
            "records_have_trigger_scope"
        ],
        "conflict_records_have_protected_scope_contract": context[
            "records_have_protected_scope"
        ],
        "conflict_records_have_forbidden_resolution_scope_contract": context[
            "records_have_forbidden_resolution_scope"
        ],
        "conflict_records_have_deterministic_disposition_contract": context[
            "records_have_deterministic_disposition"
        ],
        "conflict_records_hash_stable_contract": context["records_hash_stable"],
        "conflict_records_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "conflict_records_mutation_proposal_required_contract": context[
            "records_mutation_proposal_required"
        ],
        "conflict_records_invariant_validation_required_contract": context[
            "records_invariant_validation_required"
        ],
        "conflict_records_audit_replay_required_contract": context[
            "records_audit_replay_required"
        ],
        "conflict_records_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "conflict_records_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_multi_cycle_continuity_protocol_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "root_governance_conflict_resolver_stage_check": True,
        "root_governance_conflict_resolver_only_mode_check": True,
        "root_governance_conflict_metadata_only_check": True,
        "upstream_source_memory_invariant_matrix_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_memory_invariant_matrix_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_source_memory_invariant_matrix_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_root_governance_conflict_resolver_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "conflict_record_ids_complete_check": context["records_complete"],
        "conflict_records_registered_check": context["records_registered"],
        "conflict_records_have_trigger_scope_check": context[
            "records_have_trigger_scope"
        ],
        "conflict_records_have_protected_scope_check": context[
            "records_have_protected_scope"
        ],
        "conflict_records_have_forbidden_resolution_scope_check": context[
            "records_have_forbidden_resolution_scope"
        ],
        "conflict_records_have_deterministic_disposition_check": context[
            "records_have_deterministic_disposition"
        ],
        "conflict_records_hash_stable_check": context["records_hash_stable"],
        "conflict_records_human_review_required_check": context[
            "records_human_review_required"
        ],
        "conflict_records_mutation_proposal_required_check": context[
            "records_mutation_proposal_required"
        ],
        "conflict_records_invariant_validation_required_check": context[
            "records_invariant_validation_required"
        ],
        "conflict_records_audit_replay_required_check": context[
            "records_audit_replay_required"
        ],
        "conflict_records_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "conflict_records_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "root_governance_conflict_sections_complete_check": context[
            "sections_complete"
        ],
        "root_governance_conflict_sections_pass_check": context[
            "sections_pass"
        ],
        "root_governance_conflict_contracts_pass_check": context[
            "contracts_pass"
        ],
        "deterministic_root_governance_conflict_resolver_hash_check": True,
        "ready_for_multi_cycle_continuity_protocol_design_check": True,
    }
    for record_id in REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS:
        conditions[f"{record_id}_check"] = context[
            _record_context_name(record_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_root_governance_conflict": True},
            "observed": {"condition_met": bool(condition)},
            "root_governance_conflict_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "root_governance_conflict_contract",
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
            "summary_type": "root_governance_conflict_resolver_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": ROOT_GOVERNANCE_CONFLICT_RESOLVER_STAGE,
            "current_stage_title": "Root Governance Conflict Resolver",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "upstream_source_memory_invariant_record_count": (
                upstream_record_count
            ),
            "upstream_source_memory_invariant_records_registered_metadata_only": (
                upstream_records_registered
            ),
            "upstream_source_memory_invariant_records_require_review": (
                upstream_records_require_review
            ),
            "upstream_source_memory_invariant_records_disable_unsafe_surfaces": (
                upstream_records_disable_unsafe_surfaces
            ),
            "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
            "required_conflict_record_count": len(
                REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS
            ),
            "observed_conflict_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["conflict_record_status"]
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
            "root_governance_conflict_mode": ROOT_GOVERNANCE_CONFLICT_MODE,
            "conflict_runtime_status": CONFLICT_RUNTIME_STATUS,
            "conflict_enforcement_status": CONFLICT_ENFORCEMENT_STATUS,
            "conflict_mutation_status": CONFLICT_MUTATION_STATUS,
            "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
            "life_claim_status": LIFE_CLAIM_STATUS,
            "awakening_claim_status": AWAKENING_CLAIM_STATUS,
            "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
            "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
            "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "handoff_status": V6_6_HANDOFF_STATUS if status == "pass" else "blocked",
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_records(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = upstream.get("source_memory_invariant_records")
    if not isinstance(records, list):
        return []
    return [
        _detached_json_value(record)
        for record in records
        if isinstance(record, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_source_memory_invariant_matrix_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], record_id: str) -> bool:
    for record in records:
        if record["conflict_record_id"] != record_id:
            continue
        return (
            record["conflict_record_status"] == "registered_metadata_only"
            and bool(record["conflict_statement"])
            and bool(record["conflict_trigger_scope"])
            and bool(record["protected_governance_scope"])
            and bool(record["forbidden_resolution_scope"])
            and bool(record["deterministic_resolution_disposition"])
            and _is_sha256(record.get("conflict_boundary_hash"))
            and _is_sha256(record.get("conflict_record_hash"))
            and record["required"] is True
            and record["human_review_required"] is True
            and record["source_mutation_proposal_required"] is True
            and record["invariant_validation_required"] is True
            and record["audit_replay_required"] is True
            and record["direct_mutation_allowed"] is False
            and record["autonomous_override_allowed"] is False
            and record["self_authorization_allowed"] is False
            and record["conflict_runtime_created"] is False
            and record["conflict_enforcement_runtime_created"] is False
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
        return "root_governance_conflict_record_section"
    if name.startswith("upstream_"):
        return "upstream_verification_section"
    if name.startswith("no_"):
        return "safety_boundary_section"
    if name.endswith("_next_stage_section"):
        return "handoff_section"
    return "root_governance_conflict_resolver_section"


def _section_note(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "Conflict record is registered metadata-only."
    if name.startswith("upstream_"):
        return "Upstream Source Memory Invariant Matrix is sanitized."
    if name.startswith("no_"):
        return "Safety boundary remains inactive and false."
    if name.endswith("_next_stage_section"):
        return "Successful v6.5 handoff prepares v6.6 without runtime activation."
    return "Root Governance Conflict Resolver metadata remains deterministic."


def _unknown_record(record_id: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "conflict_record_id": record_id,
            "conflict_name": "unknown_root_governance_conflict_record",
            "conflict_record_status": "blocked",
            "known_record": False,
            "blocking_reasons": [
                f"{record_id} is not a known root governance conflict record"
            ],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_root_governance_conflict_section",
            "section_status": "blocked",
            "expected": {"known_section": True},
            "observed": {"known_section": False},
            "root_governance_conflict_notes": "Unknown section is blocked.",
            "blocking_reasons": [f"{name} is not a known section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_root_governance_conflict_contract",
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


def _conflict_boundary_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "conflict_record_id": record.get("conflict_record_id"),
        "conflict_name": record.get("conflict_name"),
        "conflict_category": record.get("conflict_category"),
        "conflict_statement": record.get("conflict_statement"),
        "conflict_trigger_scope": record.get("conflict_trigger_scope"),
        "protected_governance_scope": record.get("protected_governance_scope"),
        "forbidden_resolution_scope": record.get("forbidden_resolution_scope"),
        "deterministic_resolution_disposition": record.get(
            "deterministic_resolution_disposition"
        ),
        "conflict_reason": record.get("conflict_reason"),
        "conflict_source_stage": record.get("conflict_source_stage"),
        "conflict_source_reference": record.get("conflict_source_reference"),
        "introduced_in_version": record.get("introduced_in_version"),
        "introduced_in_stage": record.get("introduced_in_stage"),
        "introduced_in_layer": record.get("introduced_in_layer"),
        "inherited_from_stage": record.get("inherited_from_stage"),
    }
    return _sha256_json(payload)


def _conflict_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "conflict_record_hash"
    }
    return _sha256_json(payload)


def _root_governance_conflict_resolver_hash(result: Mapping[str, Any]) -> str:
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
