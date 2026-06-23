"""Deterministic Source Mutation Review Gate metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_mutation_proposal_boundary import (
    COMMON_DISABLED_FLAGS as SOURCE_MUTATION_PROPOSAL_BOUNDARY_DISABLED_FLAGS,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS,
    build_governance_source_mutation_proposal_boundary,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_VERSION = "6.9.0"
GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_SCHEMA_VERSION = "6.9.0"
GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_TYPE = (
    "governance_source_mutation_review_gate"
)
GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_HASH_ALGORITHM = "sha256"
SOURCE_MUTATION_REVIEW_GATE_STAGE = "v6.8_source_mutation_review_gate"
SOURCE_MUTATION_REVIEW_GATE_MODE = "source_mutation_review_gate_only"
SOURCE_MUTATION_REVIEW_MODE = "metadata_only"
SOURCE_MUTATION_REVIEW_GATE_STATUS = "review_gate_candidate_only"
SOURCE_MUTATION_REVIEW_GATE_ACTIVE_STATUS = "not_active"
SOURCE_MUTATION_REVIEW_RUNTIME_STATUS = "not_active"
SOURCE_MUTATION_REVIEW_EXECUTION_STATUS = "not_active"
SOURCE_MUTATION_REVIEW_DECISION_STATUS = "not_performed"
SOURCE_MUTATION_REVIEW_STATUS = "not_active"
SOURCE_MUTATION_APPROVAL_STATUS = "not_active"
SOURCE_MUTATION_REJECTION_STATUS = "not_active"
SOURCE_MUTATION_RUNTIME_STATUS = "not_active"
SOURCE_MUTATION_EXECUTION_STATUS = "not_active"
SOURCE_MUTATION_PROPOSAL_CREATION_STATUS = "not_active"
SOURCE_MUTATION_PROPOSAL_APPROVAL_STATUS = "not_active"
SOURCE_MUTATION_STATUS = "not_performed"
HUMAN_APPROVAL_STATUS = "not_performed"
HUMAN_SOVEREIGNTY_LOCK_STATUS = "not_active"
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
V6_8_STATUS = "source_mutation_review_gate_only"
V6_9_HANDOFF_STATUS = "ready_for_human_sovereignty_lock_design"

UPSTREAM_READY_HANDOFF_STATUS = "ready_for_source_mutation_review_gate_design"
UPSTREAM_NEXT_STAGE = SOURCE_MUTATION_REVIEW_GATE_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Source Mutation Review Gate"
NEXT_STAGE = "v6.9_human_sovereignty_lock"
NEXT_STAGE_TITLE = "Human Sovereignty Lock"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.9.0"
INTRODUCED_IN_STAGE = SOURCE_MUTATION_REVIEW_GATE_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.7_source_mutation_proposal_boundary"
REVIEW_GATE_RECORD_MODE = "metadata_only_gate"
GATE_STRENGTH = "source_mutation_review_required"

COMMON_DISABLED_FLAGS = {
    **SOURCE_MUTATION_PROPOSAL_BOUNDARY_DISABLED_FLAGS,
    "source_mutation_review_gate_active": False,
    "source_mutation_review_runtime_created": False,
    "source_mutation_review_execution_created": False,
    "source_mutation_review_decision_performed": False,
    "human_approval_performed": False,
    "source_mutation_approval_performed": False,
    "source_mutation_rejection_performed": False,
    "source_mutation_runtime_created": False,
    "source_mutation_execution_created": False,
    "source_mutation_performed": False,
    "source_mutation_proposal_created": False,
    "source_mutation_proposal_approved": False,
    "source_mutation_proposal_rejected": False,
    "source_mutation_review_gate_created": False,
    "source_mutation_review_gate_activated": False,
    "human_sovereignty_lock_created": False,
    "human_sovereignty_lock_activated": False,
    "review_auto_approval_allowed": False,
    "review_auto_rejection_allowed": False,
    "review_runtime_activation_allowed": False,
    "review_memory_write_allowed": False,
    "review_source_graph_mutation_allowed": False,
    "review_memory_graph_mutation_allowed": False,
}

REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS = (
    "review_gate_intake_metadata_check",
    "human_sovereignty_review_requirement",
    "source_constitution_review_check",
    "origin_provenance_review_check",
    "civilizational_identity_review_check",
    "source_memory_invariant_review_check",
    "root_governance_conflict_review_check",
    "multi_cycle_continuity_review_check",
    "audit_replay_review_check",
    "proposal_scope_review_check",
    "proposal_risk_review_check",
    "unsafe_surface_blocking_review_check",
    "no_review_decision_execution_gate",
    "no_auto_approval_or_rejection_gate",
    "no_source_or_memory_graph_mutation_gate",
    "human_sovereignty_lock_handoff_gate",
)

REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES = (
    "upstream_source_mutation_proposal_boundary_input_section",
    "source_mutation_review_gate_metadata_section",
    "review_gate_record_completeness_section",
    "review_gate_record_hash_stability_section",
    "review_gate_scope_section",
    "required_review_metadata_scope_section",
    "forbidden_review_activation_scope_section",
    "review_gate_intake_metadata_check_section",
    "human_sovereignty_review_requirement_section",
    "source_constitution_review_check_section",
    "origin_provenance_review_check_section",
    "civilizational_identity_review_check_section",
    "source_memory_invariant_review_check_section",
    "root_governance_conflict_review_check_section",
    "multi_cycle_continuity_review_check_section",
    "audit_replay_review_check_section",
    "proposal_scope_review_check_section",
    "proposal_risk_review_check_section",
    "unsafe_surface_blocking_review_check_section",
    "no_review_decision_execution_gate_section",
    "no_auto_approval_or_rejection_gate_section",
    "no_source_or_memory_graph_mutation_gate_section",
    "human_sovereignty_lock_handoff_gate_section",
    "human_sovereignty_lock_next_stage_section",
    "no_source_mutation_review_runtime_section",
    "no_source_mutation_review_execution_section",
    "no_source_mutation_review_decision_section",
    "no_human_approval_section",
    "no_source_mutation_approval_section",
    "no_source_mutation_rejection_section",
    "no_source_mutation_runtime_section",
    "no_source_mutation_execution_section",
    "no_source_mutation_proposal_creation_section",
    "no_source_mutation_proposal_approval_section",
    "no_human_sovereignty_lock_activation_section",
    "no_identity_activation_section",
    "no_active_star_source_memory_section",
    "no_active_layer_15_section",
    "no_source_graph_creation_section",
    "no_source_graph_mutation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CONTRACT_NAMES = (
    "source_mutation_review_gate_only_contract",
    "source_mutation_review_metadata_only_contract",
    "upstream_source_mutation_proposal_boundary_pass_contract",
    "upstream_source_mutation_proposal_boundary_hash_present_contract",
    "upstream_source_mutation_proposal_boundary_hash_stable_contract",
    "upstream_source_mutation_review_gate_handoff_ready_contract",
    "review_gate_records_complete_contract",
    "review_gate_records_registered_metadata_only_contract",
    "review_gate_records_have_gate_scope_contract",
    "review_gate_records_have_required_metadata_scope_contract",
    "review_gate_records_have_forbidden_activation_scope_contract",
    "review_gate_records_have_disposition_contract",
    "review_gate_records_hash_stable_contract",
    "review_gate_records_human_review_required_contract",
    "review_gate_records_human_sovereignty_lock_required_contract",
    "review_gate_records_constitution_alignment_required_contract",
    "review_gate_records_origin_provenance_required_contract",
    "review_gate_records_identity_boundary_required_contract",
    "review_gate_records_invariant_validation_required_contract",
    "review_gate_records_root_conflict_resolution_required_contract",
    "review_gate_records_multi_cycle_continuity_required_contract",
    "review_gate_records_audit_replay_required_contract",
    "review_gate_records_direct_mutation_disabled_contract",
    "review_gate_records_autonomous_override_disabled_contract",
    "no_source_mutation_review_runtime_contract",
    "no_source_mutation_review_execution_contract",
    "no_source_mutation_review_decision_contract",
    "no_human_approval_contract",
    "no_source_mutation_approval_contract",
    "no_source_mutation_rejection_contract",
    "no_source_mutation_runtime_contract",
    "no_source_mutation_execution_contract",
    "no_source_mutation_performed_contract",
    "no_source_mutation_proposal_creation_contract",
    "no_source_mutation_proposal_approval_contract",
    "no_human_sovereignty_lock_activation_contract",
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
    "no_review_auto_approval_contract",
    "no_review_auto_rejection_contract",
    "ready_for_human_sovereignty_lock_design_contract",
)

REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CHECK_NAMES = (
    "source_mutation_review_gate_stage_check",
    "source_mutation_review_gate_only_mode_check",
    "source_mutation_review_metadata_only_check",
    "upstream_source_mutation_proposal_boundary_pass_check",
    "upstream_source_mutation_proposal_boundary_hash_present_check",
    "upstream_source_mutation_proposal_boundary_hash_stable_check",
    "upstream_source_mutation_review_gate_handoff_ready_check",
    "review_gate_record_ids_complete_check",
    "review_gate_records_registered_check",
    "review_gate_records_have_gate_scope_check",
    "review_gate_records_have_required_metadata_scope_check",
    "review_gate_records_have_forbidden_activation_scope_check",
    "review_gate_records_have_disposition_check",
    "review_gate_records_hash_stable_check",
    "review_gate_records_human_review_required_check",
    "review_gate_records_human_sovereignty_lock_required_check",
    "review_gate_records_constitution_alignment_required_check",
    "review_gate_records_origin_provenance_required_check",
    "review_gate_records_identity_boundary_required_check",
    "review_gate_records_invariant_validation_required_check",
    "review_gate_records_root_conflict_resolution_required_check",
    "review_gate_records_multi_cycle_continuity_required_check",
    "review_gate_records_audit_replay_required_check",
    "review_gate_records_direct_mutation_disabled_check",
    "review_gate_records_autonomous_override_disabled_check",
    "review_gate_intake_metadata_check_check",
    "human_sovereignty_review_requirement_check",
    "source_constitution_review_check_check",
    "origin_provenance_review_check_check",
    "civilizational_identity_review_check_check",
    "source_memory_invariant_review_check_check",
    "root_governance_conflict_review_check_check",
    "multi_cycle_continuity_review_check_check",
    "audit_replay_review_check_check",
    "proposal_scope_review_check_check",
    "proposal_risk_review_check_check",
    "unsafe_surface_blocking_review_check_check",
    "no_review_decision_execution_gate_check",
    "no_auto_approval_or_rejection_gate_check",
    "no_source_or_memory_graph_mutation_gate_check",
    "human_sovereignty_lock_handoff_gate_check",
    "source_mutation_review_gate_sections_complete_check",
    "source_mutation_review_gate_sections_pass_check",
    "source_mutation_review_gate_contracts_pass_check",
    "no_source_mutation_review_runtime_check",
    "no_source_mutation_review_execution_check",
    "no_source_mutation_review_decision_check",
    "no_human_approval_check",
    "no_source_mutation_approval_check",
    "no_source_mutation_rejection_check",
    "no_source_mutation_runtime_check",
    "no_source_mutation_execution_check",
    "no_source_mutation_performed_check",
    "no_source_mutation_proposal_creation_check",
    "no_source_mutation_proposal_approval_check",
    "no_human_sovereignty_lock_activation_check",
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
    "no_review_auto_approval_check",
    "no_review_auto_rejection_check",
    "deterministic_source_mutation_review_gate_hash_check",
    "ready_for_human_sovereignty_lock_design_check",
)

_REQUIRED_DISPOSITIONS = (
    "record_review_gate_intake_metadata_only",
    "require_human_sovereignty_review",
    "require_source_constitution_review",
    "require_origin_provenance_review",
    "require_civilizational_identity_review",
    "require_source_memory_invariant_review",
    "require_root_governance_conflict_review",
    "require_multi_cycle_continuity_review",
    "require_audit_replay_review",
    "review_proposal_scope_metadata_only",
    "review_proposal_risk_metadata_only",
    "block_unsafe_surfaces_metadata_only",
    "block_review_decision_execution",
    "block_auto_approval_or_rejection",
    "block_source_and_memory_graph_mutation",
    "handoff_to_human_sovereignty_lock",
)

_REVIEW_GATE_RECORD_DEFINITIONS: dict[str, dict[str, str]] = {
    "review_gate_intake_metadata_check": {
        "name": "Source Mutation Intake Metadata Boundary",
        "category": "proposal_intake_boundary",
        "statement": "Source mutation intake is described as metadata only.",
        "scope": "Proposal identity, purpose, source scope, evidence, risks, and requested review path.",
        "preserved": "Complete proposal metadata without creating a proposal runtime or mutation authority.",
        "forbidden": "Must not generate, submit, approve, reject, execute, or apply a proposal.",
        "disposition": "record_review_gate_intake_metadata_only",
        "reason": "Review requires deterministic intake metadata before any decision.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "source mutation intake metadata",
    },
    "human_sovereignty_review_requirement": {
        "name": "Human Sovereignty Review Requirement",
        "category": "human_authority_boundary",
        "statement": "Every source mutation proposal remains subordinate to human sovereignty.",
        "scope": "Human ownership, reviewer identity class, explicit review requirement, and blocked status.",
        "preserved": "Human authority remains the controlling source-governance authority.",
        "forbidden": "Must not self-authorize, infer consent, or create autonomous authority.",
        "disposition": "require_human_sovereignty_review",
        "reason": "Source-level change cannot be authorized by this metadata boundary.",
        "source": "Layer 15 human sovereignty constraints",
        "reference": "human review requirement",
    },
    "source_constitution_review_check": {
        "name": "Source Constitution Alignment Requirement",
        "category": "constitution_alignment_boundary",
        "statement": "Proposal metadata must identify alignment with Source Constitution rules.",
        "scope": "Affected rule identifiers, alignment evidence, conflicts, and unresolved questions.",
        "preserved": "Source Constitution Registry constraints remain explicit and reviewable.",
        "forbidden": "Must not rewrite constitution rules or treat alignment metadata as permission.",
        "disposition": "require_source_constitution_review",
        "reason": "A proposal cannot be review-ready without constitution alignment evidence.",
        "source": "v6.1 Source Constitution Registry",
        "reference": "source constitution alignment",
    },
    "origin_provenance_review_check": {
        "name": "Origin Provenance Preservation Requirement",
        "category": "origin_provenance_boundary",
        "statement": "Proposal metadata must preserve origin provenance and inheritance lineage.",
        "scope": "Origin references, inherited stages, evidence surfaces, hashes, and lineage impact.",
        "preserved": "Origin provenance remains traceable without ledger writing.",
        "forbidden": "Must not rewrite origin records, write ledgers, or activate provenance runtime.",
        "disposition": "require_origin_provenance_review",
        "reason": "Source mutation review requires stable origin traceability.",
        "source": "v6.2 Origin Provenance Ledger",
        "reference": "origin provenance preservation",
    },
    "civilizational_identity_review_check": {
        "name": "Civilizational Identity Non-Escalation Requirement",
        "category": "identity_boundary",
        "statement": "Proposal metadata must preserve civilizational identity boundaries.",
        "scope": "Identity claims, authority implications, escalation risks, and prohibited status claims.",
        "preserved": "Identity remains descriptive governance metadata under human sovereignty.",
        "forbidden": "Must not claim personhood, life, awakening, legal status, religious status, or autonomous authority.",
        "disposition": "require_civilizational_identity_review",
        "reason": "Source mutation proposals cannot expand identity or authority.",
        "source": "v6.3 Civilizational Identity Boundary",
        "reference": "civilizational identity non-escalation",
    },
    "source_memory_invariant_review_check": {
        "name": "Source Memory Invariant Validation Requirement",
        "category": "invariant_validation_boundary",
        "statement": "Proposal metadata must enumerate affected source-memory invariants.",
        "scope": "Invariant identifiers, expected preservation, validation evidence, and blocked failures.",
        "preserved": "Source Memory Invariant Matrix validation remains mandatory.",
        "forbidden": "Must not bypass, rewrite, or enforce invariants through runtime mutation.",
        "disposition": "require_source_memory_invariant_review",
        "reason": "Review readiness requires explicit invariant impact analysis.",
        "source": "v6.4 Source Memory Invariant Matrix",
        "reference": "source memory invariant validation",
    },
    "root_governance_conflict_review_check": {
        "name": "Root Governance Conflict Resolution Requirement",
        "category": "root_conflict_boundary",
        "statement": "Proposal metadata must identify root governance conflicts and dispositions.",
        "scope": "Conflict identifiers, deterministic classifications, unresolved conflicts, and required handoffs.",
        "preserved": "Root conflict resolution remains fail-closed and human-reviewed.",
        "forbidden": "Must not execute conflict resolution or autonomously override a conflict.",
        "disposition": "require_root_governance_conflict_review",
        "reason": "Unresolved root conflicts block proposal readiness.",
        "source": "v6.5 Root Governance Conflict Resolver",
        "reference": "root governance conflict resolution",
    },
    "multi_cycle_continuity_review_check": {
        "name": "Multi-Cycle Continuity Review Check",
        "category": "continuity_boundary",
        "statement": "Proposal metadata must preserve governance continuity across release cycles.",
        "scope": "Version lineage, prior hashes, continuity records, recovery references, and handoff evidence.",
        "preserved": "Multi-cycle governance continuity remains replayable.",
        "forbidden": "Must not activate continuity runtime, scheduling, enforcement, rollback, or recovery.",
        "disposition": "require_multi_cycle_continuity_review",
        "reason": "Source mutation review requires continuity evidence from v6.6.",
        "source": "v6.6 Multi-Cycle Continuity Protocol",
        "reference": "multi-cycle continuity evidence",
    },
    "audit_replay_review_check": {
        "name": "Audit Replay Requirement",
        "category": "audit_replay_boundary",
        "statement": "Proposal metadata must be deterministic and replayable.",
        "scope": "Sanitized inputs, ordered records, stable hashes, sections, contracts, checks, and summary.",
        "preserved": "Independent audit replay without hidden state or audit-log writing.",
        "forbidden": "Must not execute replay actions, write audit logs, or depend on hidden execution.",
        "disposition": "require_audit_replay_review",
        "reason": "Human review needs reproducible review-gate evidence.",
        "source": "Layer 15 audit boundaries",
        "reference": "audit replay requirement",
    },
    "proposal_scope_review_check": {
        "name": "Proposal Scope Definition Boundary",
        "category": "proposal_scope_boundary",
        "statement": "Proposal metadata must define the exact source-level scope under consideration.",
        "scope": "Affected source rules, records, invariants, identities, cycles, and explicitly excluded surfaces.",
        "preserved": "A bounded review target with no implied mutation permission.",
        "forbidden": "Must not expand scope dynamically or treat scope completeness as authorization.",
        "disposition": "review_proposal_scope_metadata_only",
        "reason": "Review cannot proceed safely with ambiguous mutation scope.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "proposal scope metadata",
    },
    "proposal_risk_review_check": {
        "name": "Proposal Risk Classification Boundary",
        "category": "proposal_risk_boundary",
        "statement": "Proposal metadata must classify source-governance risk deterministically.",
        "scope": "Constitution, provenance, identity, invariant, conflict, continuity, execution, write, graph, and authority risks.",
        "preserved": "Risk classification remains informational and review-required.",
        "forbidden": "Must not auto-approve low risk or execute mitigations.",
        "disposition": "review_proposal_risk_metadata_only",
        "reason": "Risk metadata prepares review without making a decision.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "proposal risk classification",
    },
    "unsafe_surface_blocking_review_check": {
        "name": "Unsafe Surface Blocking Review Check",
        "category": "unsafe_surface_boundary",
        "statement": "Unsafe mutation surfaces remain blocked by metadata policy.",
        "scope": "Execution, network, writes, ledgers, graphs, identity, authority, active Layer 15, and mutation surfaces.",
        "preserved": "Unsafe-surface classification is deterministic and fail-closed.",
        "forbidden": "Must not activate, authorize, dispatch, notify, approve, reject, or execute any unsafe surface.",
        "disposition": "block_unsafe_surfaces_metadata_only",
        "reason": "Metadata completeness cannot make an unsafe proposal actionable.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "unsafe surface blocking metadata",
    },
    "no_review_decision_execution_gate": {
        "name": "No Review Decision Execution Gate",
        "category": "review_decision_boundary",
        "statement": "Review-gate pass records metadata completeness only.",
        "scope": "Review decisions, approval, rejection, mutation, execution, authorization, and dispatch.",
        "preserved": "Review metadata remains separate from decisions and execution.",
        "forbidden": "Must not decide, approve, reject, create proposals, mutate, execute, authorize, or dispatch.",
        "disposition": "block_review_decision_execution",
        "reason": "A review gate is not a reviewer, decision engine, or executor.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "no review decision execution",
    },
    "no_auto_approval_or_rejection_gate": {
        "name": "No Automatic Proposal Approval Boundary",
        "category": "proposal_approval_boundary",
        "statement": "This module never approves or rejects source mutation proposals.",
        "scope": "Approval, rejection, decision, notification, token, grant, and authorization surfaces.",
        "preserved": "Every proposal remains blocked pending the future human-sovereignty lock.",
        "forbidden": "Must not auto-approve, auto-reject, notify approval, or create authorization.",
        "disposition": "block_auto_approval_or_rejection",
        "reason": "Proposal approval belongs outside this boundary.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "no automatic proposal approval",
    },
    "no_source_or_memory_graph_mutation_gate": {
        "name": "No Source Or Memory Graph Mutation Boundary",
        "category": "graph_mutation_boundary",
        "statement": "Proposal metadata cannot create or mutate source or Memory Graph state.",
        "scope": "Source graph nodes and edges, Memory Graph nodes and edges, persistent memory, and durable state.",
        "preserved": "Graph and memory state remain unchanged.",
        "forbidden": "Must not create source graphs, mutate either graph, or write persistent memory.",
        "disposition": "block_source_and_memory_graph_mutation",
        "reason": "Metadata readiness is not graph-mutation authority.",
        "source": "Layer 15 graph and memory boundaries",
        "reference": "source and Memory Graph mutation prohibition",
    },
    "human_sovereignty_lock_handoff_gate": {
        "name": "Human Sovereignty Lock Handoff Gate",
        "category": "next_stage_handoff",
        "statement": "A passing v6.8 review gate prepares v6.9 Human Sovereignty Lock design.",
        "scope": "Next-stage identifier, title, metadata-completeness status, and blocked mutation semantics.",
        "preserved": "Clear separation between metadata review and future human sovereignty.",
        "forbidden": "Must not create or activate the lock, perform human approval, notify, authorize, mutate, or execute.",
        "disposition": "handoff_to_human_sovereignty_lock",
        "reason": "Successful metadata validation hands off without authorizing mutation.",
        "source": "v6.8 Source Mutation Review Gate",
        "reference": "v6.9 Human Sovereignty Lock",
    },
}

_SECTION_RECORD_IDS = {
    f"{record_id}_section": record_id
    for record_id in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS
}

_DISABLED_FIELDS = {
    "no_source_mutation_review_runtime": "source_mutation_review_runtime_created",
    "no_source_mutation_review_execution": "source_mutation_review_execution_created",
    "no_source_mutation_review_decision": "source_mutation_review_decision_performed",
    "no_human_approval": "human_approval_performed",
    "no_source_mutation_approval": "source_mutation_approval_performed",
    "no_source_mutation_rejection": "source_mutation_rejection_performed",
    "no_source_mutation_runtime": "source_mutation_runtime_created",
    "no_source_mutation_execution": "source_mutation_execution_created",
    "no_source_mutation_performed": "source_mutation_performed",
    "no_source_mutation_proposal_creation": "source_mutation_proposal_created",
    "no_source_mutation_proposal_approval": "source_mutation_proposal_approved",
    "no_human_sovereignty_lock_activation": "human_sovereignty_lock_activated",
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
    "no_review_auto_approval": "review_auto_approval_allowed",
    "no_review_auto_rejection": "review_auto_rejection_allowed",
}

_UPSTREAM_RECORD_REQUIRED_FALSE_FIELDS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "source_mutation_runtime_created",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_mutation_proposal_created",
    "source_mutation_proposal_approved",
    "source_mutation_proposal_rejected",
    "source_mutation_review_performed",
    "source_mutation_review_gate_created",
    "source_mutation_review_gate_activated",
    "proposal_auto_creation_allowed",
    "proposal_auto_approval_allowed",
    "proposal_runtime_activation_allowed",
    "proposal_memory_write_allowed",
    "proposal_source_graph_mutation_allowed",
    "proposal_memory_graph_mutation_allowed",
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
    "source_mutation_review_gate_type",
    "source_mutation_review_gate_status",
    "source_mutation_review_gate_stage",
    "source_mutation_review_gate_mode",
    "source_mutation_review_mode",
    "source_mutation_review_gate_candidate_status",
    "source_mutation_review_gate_active_status",
    "source_mutation_review_runtime_status",
    "source_mutation_review_execution_status",
    "source_mutation_review_decision_status",
    "source_mutation_approval_status",
    "source_mutation_rejection_status",
    "source_mutation_runtime_status",
    "source_mutation_execution_status",
    "source_mutation_proposal_creation_status",
    "source_mutation_proposal_approval_status",
    "source_mutation_status",
    "human_approval_status",
    "human_sovereignty_lock_status",
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
    "v6_8_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_source_mutation_proposal_boundary_version",
    "upstream_source_mutation_proposal_boundary_status",
    "upstream_source_mutation_proposal_boundary_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "upstream_source_mutation_proposal_boundary_record_count",
    "upstream_source_mutation_proposal_boundary_records_registered_metadata_only",
    "upstream_source_mutation_proposal_boundary_records_require_review",
    "upstream_source_mutation_proposal_boundary_records_disable_unsafe_surfaces",
    "upstream_safety_boundaries_clear",
    "source_mutation_review_gate_records",
    "source_mutation_review_gate_sections",
    "source_mutation_review_gate_contracts",
    "source_mutation_review_gate_checks",
    "source_mutation_review_gate_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Source Mutation Review Gate projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_mutation_proposal_boundary_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_source_mutation_review_gate() -> dict[str, Any]:
    """Build deterministic Source-Mutation-Review-Gate-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_records = _upstream_records(upstream)
    upstream_record_ids = [
        record.get("proposal_boundary_record_id") for record in upstream_records
    ]

    upstream_version_ready = (
        upstream.get("version")
        == GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_VERSION
    )
    upstream_pass = (
        upstream.get("source_mutation_proposal_boundary_status") == "pass"
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
        REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS
    )
    upstream_records_registered = all(
        record.get("proposal_boundary_record_status") == "registered_metadata_only"
        for record in upstream_records
    )
    upstream_records_require_review = all(
        record.get("human_review_required") is True
        and record.get("source_mutation_review_gate_required") is True
        and record.get("source_constitution_alignment_required") is True
        and record.get("origin_provenance_preservation_required") is True
        and record.get("civilizational_identity_boundary_required") is True
        and record.get("source_memory_invariant_validation_required") is True
        and record.get("root_governance_conflict_resolution_required") is True
        and record.get("multi_cycle_continuity_required") is True
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
        {**SOURCE_MUTATION_PROPOSAL_BOUNDARY_DISABLED_FLAGS, **SAFETY_BOUNDARIES},
    )

    records = _build_records()
    records_complete = _names_match(
        records,
        "review_gate_record_id",
        REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS,
    )
    records_registered = all(
        record["review_gate_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_boundary_scope = all(
        bool(record["review_gate_scope"]) for record in records
    )
    records_have_required_metadata_scope = all(
        bool(record["required_review_metadata_scope"]) for record in records
    )
    records_have_forbidden_activation_scope = all(
        bool(record["forbidden_review_activation_scope"]) for record in records
    )
    records_have_disposition = [
        record["review_gate_disposition"] for record in records
    ] == list(_REQUIRED_DISPOSITIONS)
    records_hash_stable = all(
        _is_sha256(record.get("review_gate_hash"))
        and _is_sha256(record.get("review_gate_record_hash"))
        and record["review_gate_hash"] == _review_gate_hash(record)
        and record["review_gate_record_hash"] == _review_gate_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required"] is True for record in records
    )
    records_human_sovereignty_lock_required = all(
        record["human_sovereignty_lock_required"] is True
        for record in records
    )
    records_constitution_alignment_required = all(
        record["source_constitution_alignment_required"] is True
        for record in records
    )
    records_origin_provenance_required = all(
        record["origin_provenance_preservation_required"] is True
        for record in records
    )
    records_identity_boundary_required = all(
        record["civilizational_identity_boundary_required"] is True
        for record in records
    )
    records_invariant_validation_required = all(
        record["source_memory_invariant_validation_required"] is True
        for record in records
    )
    records_root_conflict_resolver_required = all(
        record["root_governance_conflict_resolution_required"] is True
        for record in records
    )
    records_multi_cycle_continuity_required = all(
        record["multi_cycle_continuity_required"] is True for record in records
    )
    records_source_mutation_proposal_boundary_required = all(
        record["source_mutation_proposal_boundary_required"] is True
        for record in records
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
        "records_have_boundary_scope": records_have_boundary_scope,
        "records_have_required_metadata_scope": (
            records_have_required_metadata_scope
        ),
        "records_have_forbidden_activation_scope": (
            records_have_forbidden_activation_scope
        ),
        "records_have_disposition": records_have_disposition,
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_human_sovereignty_lock_required": records_human_sovereignty_lock_required,
        "records_constitution_alignment_required": (
            records_constitution_alignment_required
        ),
        "records_origin_provenance_required": (
            records_origin_provenance_required
        ),
        "records_identity_boundary_required": (
            records_identity_boundary_required
        ),
        "records_invariant_validation_required": (
            records_invariant_validation_required
        ),
        "records_root_conflict_resolver_required": (
            records_root_conflict_resolver_required
        ),
        "records_multi_cycle_continuity_required": (
            records_multi_cycle_continuity_required
        ),
        "records_source_mutation_proposal_boundary_required": (
            records_source_mutation_proposal_boundary_required
        ),
        "records_audit_replay_required": records_audit_replay_required,
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": (
            records_autonomous_override_disabled
        ),
        "handoff_status": V6_9_HANDOFF_STATUS,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
    }
    for record_id in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS:
        context[_record_context_name(record_id)] = _record_ready(
            records,
            record_id,
        )

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CHECK_NAMES,
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
            records_have_boundary_scope,
            records_have_required_metadata_scope,
            records_have_forbidden_activation_scope,
            records_have_disposition,
            records_hash_stable,
            records_human_review_required,
            records_human_sovereignty_lock_required,
            records_constitution_alignment_required,
            records_origin_provenance_required,
            records_identity_boundary_required,
            records_invariant_validation_required,
            records_root_conflict_resolver_required,
            records_source_mutation_proposal_boundary_required,
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
                (upstream_version_ready, "Source Mutation Proposal Boundary version must be 6.9.0"),
                (upstream_pass, "Source Mutation Proposal Boundary must pass"),
                (upstream_hash_present, "Source Mutation Proposal Boundary hash must be present"),
                (upstream_hash_stable, "Source Mutation Proposal Boundary hash must be stable"),
                (upstream_handoff_ready, "Source Mutation Proposal Boundary handoff must target Source Mutation Review Gate"),
                (upstream_next_stage_ready, "Source Mutation Proposal Boundary next stage must be Source Mutation Review Gate"),
                (upstream_records_complete, "Source mutation proposal boundary records must be complete"),
                (upstream_records_registered, "Source mutation proposal boundary records must be metadata-only"),
                (upstream_records_require_review, "Source mutation proposal boundary records must require review, mutation proposal, invariant validation, root conflict resolution, and audit replay"),
                (upstream_records_disable_unsafe_surfaces, "Source mutation proposal boundary records must keep unsafe surfaces disabled"),
                (upstream_safety_boundaries_clear, "Source Mutation Proposal Boundary safety boundaries must be clear"),
                (records_complete, "Review-gate records must be complete"),
                (records_registered, "Review-gate records must be metadata-only"),
                (records_have_boundary_scope, "Review-gate records must include boundary scope"),
                (records_have_required_metadata_scope, "Review-gate records must include required metadata scope"),
                (records_have_forbidden_activation_scope, "Review-gate records must include forbidden activation scope"),
                (records_have_disposition, "Review-gate records must include required dispositions"),
                (records_hash_stable, "Review-gate record hashes must be stable"),
                (records_human_review_required, "Review-gate records must require human review"),
                (records_human_sovereignty_lock_required, "Review-gate records must require the future review gate"),
                (records_constitution_alignment_required, "Review-gate records must require constitution alignment"),
                (records_origin_provenance_required, "Review-gate records must preserve origin provenance"),
                (records_identity_boundary_required, "Review-gate records must preserve identity boundaries"),
                (records_invariant_validation_required, "Review-gate records must require invariant validation"),
                (records_root_conflict_resolver_required, "Review-gate records must require root conflict resolution"),
                (records_source_mutation_proposal_boundary_required, "Review-gate records must require source mutation proposal boundary"),
                (records_audit_replay_required, "Review-gate records must require audit replay"),
                (records_direct_mutation_disabled, "Review-gate records must disable direct mutation"),
                (records_autonomous_override_disabled, "Review-gate records must disable autonomous override"),
            )
            if not condition
        ]
        + [
            reason
            for item in (*sections, *contracts, *checks)
            for reason in item["blocking_reasons"]
        ]
    )
    handoff_status = V6_9_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
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
        "version": GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_VERSION,
        "schema_version": GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_SCHEMA_VERSION,
        "source_mutation_review_gate_type": (
            GOVERNANCE_SOURCE_MUTATION_REVIEW_GATE_TYPE
        ),
        "source_mutation_review_gate_status": status,
        "source_mutation_review_gate_stage": (
            SOURCE_MUTATION_REVIEW_GATE_STAGE
        ),
        "source_mutation_review_gate_mode": (
            SOURCE_MUTATION_REVIEW_GATE_MODE
        ),
        "source_mutation_review_mode": SOURCE_MUTATION_REVIEW_MODE,
        "source_mutation_review_gate_candidate_status": (
            SOURCE_MUTATION_REVIEW_GATE_STATUS
        ),
        "source_mutation_review_gate_active_status": (
            SOURCE_MUTATION_REVIEW_GATE_ACTIVE_STATUS
        ),
        "source_mutation_review_runtime_status": (
            SOURCE_MUTATION_REVIEW_RUNTIME_STATUS
        ),
        "source_mutation_review_execution_status": (
            SOURCE_MUTATION_REVIEW_EXECUTION_STATUS
        ),
        "source_mutation_review_decision_status": (
            SOURCE_MUTATION_REVIEW_DECISION_STATUS
        ),
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "source_mutation_approval_status": SOURCE_MUTATION_APPROVAL_STATUS,
        "source_mutation_rejection_status": SOURCE_MUTATION_REJECTION_STATUS,
        "source_mutation_runtime_status": SOURCE_MUTATION_RUNTIME_STATUS,
        "source_mutation_execution_status": SOURCE_MUTATION_EXECUTION_STATUS,
        "source_mutation_proposal_creation_status": (
            SOURCE_MUTATION_PROPOSAL_CREATION_STATUS
        ),
        "source_mutation_proposal_approval_status": (
            SOURCE_MUTATION_PROPOSAL_APPROVAL_STATUS
        ),
        "source_mutation_review_status": SOURCE_MUTATION_REVIEW_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "human_sovereignty_lock_status": HUMAN_SOVEREIGNTY_LOCK_STATUS,
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
        "v6_8_status": V6_8_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_source_mutation_proposal_boundary_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_mutation_proposal_boundary_status": _string_or_none(
            upstream.get("source_mutation_proposal_boundary_status")
        ),
        "upstream_source_mutation_proposal_boundary_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_source_mutation_proposal_boundary_record_count": len(upstream_records),
        "upstream_source_mutation_proposal_boundary_records_registered_metadata_only": (
            upstream_records_registered
        ),
        "upstream_source_mutation_proposal_boundary_records_require_review": (
            upstream_records_require_review
        ),
        "upstream_source_mutation_proposal_boundary_records_disable_unsafe_surfaces": (
            upstream_records_disable_unsafe_surfaces
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "source_mutation_review_gate_records": records,
        "source_mutation_review_gate_sections": sections,
        "source_mutation_review_gate_contracts": contracts,
        "source_mutation_review_gate_checks": checks,
        "source_mutation_review_gate_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_source_mutation_review_gate_hash"] = (
        _source_mutation_review_gate_hash(result)
    )
    return _detached_json_value(result)


def get_governance_source_mutation_review_gate_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached continuity record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_protocol()["source_mutation_review_gate_records"]:
        if record["review_gate_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_source_mutation_review_gate_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_protocol()["source_mutation_review_gate_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_source_mutation_review_gate_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_protocol()["source_mutation_review_gate_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_source_mutation_review_gate_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached continuity check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_protocol()["source_mutation_review_gate_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_source_mutation_review_gate_record_ids() -> list[str]:
    """Return stable continuity record IDs."""

    return list(REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS)


def list_governance_source_mutation_review_gate_section_names() -> list[str]:
    """Return stable continuity section names."""

    return list(REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES)


def list_governance_source_mutation_review_gate_contract_names() -> list[str]:
    """Return stable continuity contract names."""

    return list(REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CONTRACT_NAMES)


def list_governance_source_mutation_review_gate_check_names() -> list[str]:
    """Return stable continuity check names."""

    return list(REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CHECK_NAMES)


def governance_source_mutation_review_gate_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Source Mutation Review Gate metadata deterministically."""

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
    return governance_source_mutation_review_gate_to_json(
        build_governance_source_mutation_review_gate()
    )


def _cached_protocol() -> dict[str, Any]:
    return json.loads(_cached_protocol_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_source_mutation_proposal_boundary()
    )
    second = _detached_json_value(
        build_governance_source_mutation_proposal_boundary()
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
        for record_id in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    definition = _REVIEW_GATE_RECORD_DEFINITIONS[record_id]
    boundary_payload = {
        "review_gate_record_id": record_id,
        "review_gate_name": definition["name"],
        "review_gate_category": definition["category"],
        "review_gate_statement": definition["statement"],
        "review_gate_scope": definition["scope"],
        "required_review_metadata_scope": definition["preserved"],
        "forbidden_review_activation_scope": definition["forbidden"],
        "review_gate_disposition": definition["disposition"],
        "review_gate_reason": definition["reason"],
        "review_gate_source_stage": definition["source"],
        "review_gate_source_reference": definition["reference"],
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
    }
    record = {
        "review_gate_record_id": record_id,
        "review_gate_name": definition["name"],
        "review_gate_category": definition["category"],
        "review_gate_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "review_gate_statement": definition["statement"],
        "review_gate_scope": definition["scope"],
        "required_review_metadata_scope": definition["preserved"],
        "forbidden_review_activation_scope": definition["forbidden"],
        "review_gate_disposition": definition["disposition"],
        "review_gate_reason": definition["reason"],
        "review_gate_source_stage": definition["source"],
        "review_gate_source_reference": definition["reference"],
        "gate_strength": GATE_STRENGTH,
        "review_gate_mode": REVIEW_GATE_RECORD_MODE,
        "review_gate_hash": _sha256_json(boundary_payload),
        "required": True,
        "human_review_required": True,
        "human_sovereignty_lock_required": True,
        "source_constitution_alignment_required": True,
        "origin_provenance_preservation_required": True,
        "civilizational_identity_boundary_required": True,
        "source_memory_invariant_validation_required": True,
        "root_governance_conflict_resolution_required": True,
        "multi_cycle_continuity_required": True,
        "source_mutation_proposal_boundary_required": True,
        "audit_replay_required": True,
        "review_metadata_only": True,
        "direct_mutation_allowed": False,
        "autonomous_override_allowed": False,
        "self_authorization_allowed": False,
        "source_mutation_runtime_created": False,
        "source_mutation_execution_created": False,
        "source_mutation_performed": False,
        "source_mutation_proposal_created": False,
        "source_mutation_proposal_approved": False,
        "source_mutation_proposal_rejected": False,
        "source_mutation_review_performed": False,
        "source_mutation_review_gate_created": False,
        "source_mutation_review_gate_activated": False,
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
        "review_auto_approval_allowed": False,
        "review_auto_rejection_allowed": False,
        "review_runtime_activation_allowed": False,
        "review_memory_write_allowed": False,
        "review_source_graph_mutation_allowed": False,
        "review_memory_graph_mutation_allowed": False,
        "blocking_reasons": [],
        **_disabled_payload(),
    }
    record["review_gate_record_hash"] = _review_gate_record_hash(record)
    return _detached_json_value(record)


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_source_mutation_proposal_boundary_input_section": all(
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
        "source_mutation_review_gate_metadata_section": True,
        "review_gate_record_completeness_section": context["records_complete"],
        "review_gate_record_hash_stability_section": context["records_hash_stable"],
        "review_gate_scope_section": context["records_have_boundary_scope"],
        "required_review_metadata_scope_section": context[
            "records_have_required_metadata_scope"
        ],
        "forbidden_review_activation_scope_section": context[
            "records_have_forbidden_activation_scope"
        ],
        "human_sovereignty_lock_next_stage_section": (
            context["handoff_status"] == V6_9_HANDOFF_STATUS
            and context["next_stage"] == NEXT_STAGE
            and context["next_stage_title"] == NEXT_STAGE_TITLE
        ),
        "no_source_mutation_review_runtime_section": (
            context["source_mutation_review_runtime_created"] is False
        ),
        "no_source_mutation_review_execution_section": (
            context["source_mutation_review_execution_created"] is False
        ),
        "no_source_mutation_review_decision_section": (
            context["source_mutation_review_decision_performed"] is False
        ),
        "no_human_approval_section": (
            context["human_approval_performed"] is False
        ),
        "no_source_mutation_approval_section": (
            context["source_mutation_approval_performed"] is False
        ),
        "no_source_mutation_rejection_section": (
            context["source_mutation_rejection_performed"] is False
        ),
        "no_source_mutation_runtime_section": (
            context["source_mutation_runtime_created"] is False
        ),
        "no_source_mutation_execution_section": (
            context["source_mutation_execution_created"] is False
        ),
        "no_source_mutation_proposal_creation_section": (
            context["source_mutation_proposal_created"] is False
        ),
        "no_source_mutation_proposal_approval_section": (
            context["source_mutation_proposal_approved"] is False
        ),
        "no_human_sovereignty_lock_activation_section": (
            context["human_sovereignty_lock_activated"] is False
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
        for name in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_mutation_review_gate_only_contract": True,
        "source_mutation_review_metadata_only_contract": True,
        "upstream_source_mutation_proposal_boundary_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_mutation_proposal_boundary_hash_present_contract": (
            context["upstream_hash_present"]
        ),
        "upstream_source_mutation_proposal_boundary_hash_stable_contract": (
            context["upstream_hash_stable"]
        ),
        "upstream_source_mutation_review_gate_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "review_gate_records_complete_contract": context["records_complete"],
        "review_gate_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "review_gate_records_have_gate_scope_contract": context[
            "records_have_boundary_scope"
        ],
        "review_gate_records_have_required_metadata_scope_contract": context[
            "records_have_required_metadata_scope"
        ],
        "review_gate_records_have_forbidden_activation_scope_contract": context[
            "records_have_forbidden_activation_scope"
        ],
        "review_gate_records_have_disposition_contract": context[
            "records_have_disposition"
        ],
        "review_gate_records_hash_stable_contract": context["records_hash_stable"],
        "review_gate_records_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "review_gate_records_human_sovereignty_lock_required_contract": context[
            "records_human_sovereignty_lock_required"
        ],
        "review_gate_records_constitution_alignment_required_contract": context[
            "records_constitution_alignment_required"
        ],
        "review_gate_records_origin_provenance_required_contract": context[
            "records_origin_provenance_required"
        ],
        "review_gate_records_identity_boundary_required_contract": context[
            "records_identity_boundary_required"
        ],
        "review_gate_records_invariant_validation_required_contract": context[
            "records_invariant_validation_required"
        ],
        "review_gate_records_root_conflict_resolution_required_contract": context[
            "records_root_conflict_resolver_required"
        ],
        "review_gate_records_multi_cycle_continuity_required_contract": context[
            "records_multi_cycle_continuity_required"
        ],
        "review_gate_records_source_mutation_proposal_boundary_required_contract": context[
            "records_source_mutation_proposal_boundary_required"
        ],
        "review_gate_records_audit_replay_required_contract": context[
            "records_audit_replay_required"
        ],
        "review_gate_records_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "review_gate_records_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_human_sovereignty_lock_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_mutation_review_gate_stage_check": True,
        "source_mutation_review_gate_only_mode_check": True,
        "source_mutation_review_metadata_only_check": True,
        "upstream_source_mutation_proposal_boundary_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_mutation_proposal_boundary_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_source_mutation_proposal_boundary_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_source_mutation_review_gate_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "review_gate_record_ids_complete_check": context["records_complete"],
        "review_gate_records_registered_check": context["records_registered"],
        "review_gate_records_have_gate_scope_check": context[
            "records_have_boundary_scope"
        ],
        "review_gate_records_have_required_metadata_scope_check": context[
            "records_have_required_metadata_scope"
        ],
        "review_gate_records_have_forbidden_activation_scope_check": context[
            "records_have_forbidden_activation_scope"
        ],
        "review_gate_records_have_disposition_check": context[
            "records_have_disposition"
        ],
        "review_gate_records_hash_stable_check": context["records_hash_stable"],
        "review_gate_records_human_review_required_check": context[
            "records_human_review_required"
        ],
        "review_gate_records_human_sovereignty_lock_required_check": context[
            "records_human_sovereignty_lock_required"
        ],
        "review_gate_records_constitution_alignment_required_check": context[
            "records_constitution_alignment_required"
        ],
        "review_gate_records_origin_provenance_required_check": context[
            "records_origin_provenance_required"
        ],
        "review_gate_records_identity_boundary_required_check": context[
            "records_identity_boundary_required"
        ],
        "review_gate_records_invariant_validation_required_check": context[
            "records_invariant_validation_required"
        ],
        "review_gate_records_root_conflict_resolution_required_check": context[
            "records_root_conflict_resolver_required"
        ],
        "review_gate_records_multi_cycle_continuity_required_check": context[
            "records_multi_cycle_continuity_required"
        ],
        "review_gate_records_source_mutation_proposal_boundary_required_check": context[
            "records_source_mutation_proposal_boundary_required"
        ],
        "review_gate_records_audit_replay_required_check": context[
            "records_audit_replay_required"
        ],
        "review_gate_records_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "review_gate_records_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "source_mutation_review_gate_sections_complete_check": context[
            "sections_complete"
        ],
        "source_mutation_review_gate_sections_pass_check": context["sections_pass"],
        "source_mutation_review_gate_contracts_pass_check": context["contracts_pass"],
        "deterministic_source_mutation_review_gate_hash_check": True,
        "ready_for_human_sovereignty_lock_design_check": True,
    }
    for record_id in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS:
        conditions[f"{record_id}_check"] = context[
            _record_context_name(record_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_MUTATION_REVIEW_GATE_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_source_mutation_review_gate": True},
            "observed": {"condition_met": bool(condition)},
            "source_mutation_review_gate_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "source_mutation_review_gate_contract",
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
            "summary_type": "source_mutation_review_gate_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": SOURCE_MUTATION_REVIEW_GATE_STAGE,
            "current_stage_title": "Source Mutation Review Gate",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "upstream_source_mutation_proposal_boundary_record_count": (
                upstream_record_count
            ),
            "upstream_source_mutation_proposal_boundary_records_registered_metadata_only": (
                upstream_records_registered
            ),
            "upstream_source_mutation_proposal_boundary_records_require_review": (
                upstream_records_require_review
            ),
            "upstream_source_mutation_proposal_boundary_records_disable_unsafe_surfaces": (
                upstream_records_disable_unsafe_surfaces
            ),
            "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
            "required_review_gate_record_count": len(
                REQUIRED_SOURCE_MUTATION_REVIEW_GATE_RECORD_IDS
            ),
            "observed_review_gate_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["review_gate_record_status"]
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
            "source_mutation_review_gate_mode": SOURCE_MUTATION_REVIEW_GATE_MODE,
            "source_mutation_review_mode": SOURCE_MUTATION_REVIEW_MODE,
            "source_mutation_runtime_status": SOURCE_MUTATION_RUNTIME_STATUS,
            "source_mutation_execution_status": SOURCE_MUTATION_EXECUTION_STATUS,
            "source_mutation_proposal_creation_status": (
                SOURCE_MUTATION_PROPOSAL_CREATION_STATUS
            ),
            "source_mutation_proposal_approval_status": (
                SOURCE_MUTATION_PROPOSAL_APPROVAL_STATUS
            ),
            "source_mutation_review_status": SOURCE_MUTATION_REVIEW_STATUS,
            "source_mutation_review_gate_status": (
                SOURCE_MUTATION_REVIEW_GATE_STATUS
            ),
            "source_mutation_status": SOURCE_MUTATION_STATUS,
            "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
            "life_claim_status": LIFE_CLAIM_STATUS,
            "awakening_claim_status": AWAKENING_CLAIM_STATUS,
            "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
            "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
            "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "handoff_status": V6_9_HANDOFF_STATUS if status == "pass" else "blocked",
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_records(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = upstream.get("source_mutation_proposal_boundary_records")
    if not isinstance(records, list):
        return []
    return [
        _detached_json_value(record)
        for record in records
        if isinstance(record, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_source_mutation_proposal_boundary_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], record_id: str) -> bool:
    for record in records:
        if record["review_gate_record_id"] != record_id:
            continue
        return (
            record["review_gate_record_status"] == "registered_metadata_only"
            and bool(record["review_gate_statement"])
            and bool(record["review_gate_scope"])
            and bool(record["required_review_metadata_scope"])
            and bool(record["forbidden_review_activation_scope"])
            and bool(record["review_gate_disposition"])
            and _is_sha256(record.get("review_gate_hash"))
            and _is_sha256(record.get("review_gate_record_hash"))
            and record["required"] is True
            and record["human_review_required"] is True
            and record["human_sovereignty_lock_required"] is True
            and record["source_constitution_alignment_required"] is True
            and record["origin_provenance_preservation_required"] is True
            and record["civilizational_identity_boundary_required"] is True
            and record["source_memory_invariant_validation_required"] is True
            and record["root_governance_conflict_resolution_required"] is True
            and record["source_mutation_proposal_boundary_required"] is True
            and record["audit_replay_required"] is True
            and record["review_metadata_only"] is True
            and record["direct_mutation_allowed"] is False
            and record["autonomous_override_allowed"] is False
            and record["self_authorization_allowed"] is False
            and record["source_mutation_runtime_created"] is False
            and record["source_mutation_execution_created"] is False
            and record["source_mutation_performed"] is False
            and record["source_mutation_proposal_created"] is False
            and record["source_mutation_proposal_approved"] is False
            and record["source_mutation_proposal_rejected"] is False
            and record["source_mutation_review_performed"] is False
            and record["source_mutation_review_gate_created"] is False
            and record["source_mutation_review_gate_activated"] is False
            and record["personhood_claim_allowed"] is False
            and record["life_claim_allowed"] is False
            and record["awakening_claim_allowed"] is False
            and record["legal_subject_claim_allowed"] is False
            and record["religious_object_claim_allowed"] is False
            and record["autonomous_authority_claim_allowed"] is False
            and record["hidden_execution_allowed"] is False
            and record["identity_escalation_allowed"] is False
            and record["review_auto_approval_allowed"] is False
            and record["review_auto_rejection_allowed"] is False
            and record["review_runtime_activation_allowed"] is False
            and record["review_memory_write_allowed"] is False
            and record["review_source_graph_mutation_allowed"] is False
            and record["review_memory_graph_mutation_allowed"] is False
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
        return "source_mutation_review_gate_record_section"
    if name.startswith("upstream_"):
        return "upstream_verification_section"
    if name.startswith("no_"):
        return "safety_boundary_section"
    if name.endswith("_next_stage_section"):
        return "handoff_section"
    return "source_mutation_review_gate_section"


def _section_note(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "Review-gate record is registered metadata-only."
    if name.startswith("upstream_"):
        return "Upstream Source Mutation Proposal Boundary is sanitized."
    if name.startswith("no_"):
        return "Safety boundary remains inactive and false."
    if name.endswith("_next_stage_section"):
        return "Successful v6.8 handoff prepares v6.9 without lock activation."
    return "Source Mutation Review Gate metadata remains deterministic."


def _unknown_record(record_id: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "review_gate_record_id": record_id,
            "review_gate_name": "unknown_source_mutation_review_gate_record",
            "review_gate_record_status": "blocked",
            "known_record": False,
            "blocking_reasons": [
                f"{record_id} is not a known review-gate record"
            ],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_source_mutation_review_gate_section",
            "section_status": "blocked",
            "expected": {"known_section": True},
            "observed": {"known_section": False},
            "source_mutation_review_gate_notes": "Unknown section is blocked.",
            "blocking_reasons": [f"{name} is not a known section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_source_mutation_review_gate_contract",
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


def _review_gate_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "review_gate_record_id": record.get("review_gate_record_id"),
        "review_gate_name": record.get("review_gate_name"),
        "review_gate_category": record.get("review_gate_category"),
        "review_gate_statement": record.get("review_gate_statement"),
        "review_gate_scope": record.get("review_gate_scope"),
        "required_review_metadata_scope": record.get(
            "required_review_metadata_scope"
        ),
        "forbidden_review_activation_scope": record.get(
            "forbidden_review_activation_scope"
        ),
        "review_gate_disposition": record.get("review_gate_disposition"),
        "review_gate_reason": record.get("review_gate_reason"),
        "review_gate_source_stage": record.get("review_gate_source_stage"),
        "review_gate_source_reference": record.get(
            "review_gate_source_reference"
        ),
        "introduced_in_version": record.get("introduced_in_version"),
        "introduced_in_stage": record.get("introduced_in_stage"),
        "introduced_in_layer": record.get("introduced_in_layer"),
        "inherited_from_stage": record.get("inherited_from_stage"),
    }
    return _sha256_json(payload)


def _review_gate_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "review_gate_record_hash"
    }
    return _sha256_json(payload)


def _source_mutation_review_gate_hash(
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
