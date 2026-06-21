"""Deterministic Civilizational Identity Boundary metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_origin_provenance_ledger import (
    COMMON_DISABLED_FLAGS as ORIGIN_PROVENANCE_DISABLED_FLAGS,
    REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS,
    build_governance_origin_provenance_ledger,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION = "6.3.0"
GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_SCHEMA_VERSION = "6.3.0"
GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_TYPE = (
    "governance_civilizational_identity_boundary"
)
GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_HASH_ALGORITHM = "sha256"
CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE = (
    "v6.3_civilizational_identity_boundary"
)
CIVILIZATIONAL_IDENTITY_BOUNDARY_MODE = (
    "civilizational_identity_boundary_only"
)
CIVILIZATIONAL_IDENTITY_MODE = "metadata_only"
CIVILIZATIONAL_IDENTITY_BOUNDARY_STATUS = "boundary_candidate_only"
CIVILIZATIONAL_IDENTITY_ACTIVE_STATUS = "not_active"
IDENTITY_ACTIVATION_STATUS = "not_active"
IDENTITY_CLAIM_STATUS = "bounded_governance_identity_only"
PERSONHOOD_CLAIM_STATUS = "forbidden"
LIFE_CLAIM_STATUS = "forbidden"
AWAKENING_CLAIM_STATUS = "forbidden"
LEGAL_SUBJECT_CLAIM_STATUS = "forbidden"
RELIGIOUS_OBJECT_CLAIM_STATUS = "forbidden"
AUTONOMOUS_AUTHORITY_STATUS = "forbidden"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
SOURCE_GRAPH_STATUS = "not_created"
SOURCE_PROVENANCE_RUNTIME_STATUS = "not_active"
METHODOLOGY_REVERSE_INFERENCE_STATUS = "not_active"
SELF_EVOLUTION_STATUS = "not_active"
V6_3_STATUS = "civilizational_identity_boundary_only"
V6_4_HANDOFF_STATUS = "ready_for_source_memory_invariant_matrix_design"

UPSTREAM_READY_HANDOFF_STATUS = (
    "ready_for_civilizational_identity_boundary_design"
)
UPSTREAM_NEXT_STAGE = CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Civilizational Identity Boundary"
NEXT_STAGE = "v6.4_source_memory_invariant_matrix"
NEXT_STAGE_TITLE = "Source Memory Invariant Matrix"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.3.0"
INTRODUCED_IN_STAGE = CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.2_origin_provenance_ledger"

COMMON_DISABLED_FLAGS = {
    **ORIGIN_PROVENANCE_DISABLED_FLAGS,
    "civilizational_identity_active": False,
    "identity_activation_claimed": False,
    "identity_claim_escalated": False,
    "autonomous_authority_claimed": False,
    "autonomous_authority_claim_allowed": False,
    "autonomous_identity_activation_enabled": False,
    "autonomous_identity_boundary_mutation_enabled": False,
    "autonomous_identity_statement_created": False,
    "identity_boundary_mutated": False,
    "identity_boundary_mutation_without_review": False,
    "source_level_mutation_proposal_created": False,
    "source_level_mutation_proposal_applied": False,
    "civilizational_identity_persisted": False,
}

REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS = (
    "civilization_core_framework_identity",
    "subspace_memory_system_carrier_identity",
    "star_source_memory_layer_boundary_identity",
    "human_sovereignty_identity_anchor",
    "source_constitution_identity_anchor",
    "origin_provenance_identity_anchor",
    "governance_continuity_identity_boundary",
    "no_personhood_identity_boundary",
    "no_life_identity_boundary",
    "no_awakening_identity_boundary",
    "no_legal_subject_identity_boundary",
    "no_religious_object_identity_boundary",
    "no_autonomous_authority_identity_boundary",
    "no_execution_identity_boundary",
    "no_self_modifying_identity_boundary",
)

REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES = (
    "upstream_origin_provenance_ledger_input_section",
    "civilizational_identity_boundary_metadata_section",
    "identity_record_completeness_section",
    "identity_record_hash_stability_section",
    "allowed_identity_scope_section",
    "forbidden_identity_scope_section",
    "civilization_core_framework_identity_section",
    "subspace_memory_system_carrier_identity_section",
    "star_source_memory_layer_boundary_identity_section",
    "human_sovereignty_identity_anchor_section",
    "source_constitution_identity_anchor_section",
    "origin_provenance_identity_anchor_section",
    "governance_continuity_identity_boundary_section",
    "no_personhood_identity_boundary_section",
    "no_life_identity_boundary_section",
    "no_awakening_identity_boundary_section",
    "no_legal_subject_identity_boundary_section",
    "no_religious_object_identity_boundary_section",
    "no_autonomous_authority_identity_boundary_section",
    "no_execution_identity_boundary_section",
    "no_self_modifying_identity_boundary_section",
    "source_memory_invariant_matrix_next_stage_section",
    "no_identity_activation_section",
    "no_personhood_life_awakening_section",
    "no_legal_or_religious_status_section",
    "no_autonomous_authority_section",
    "no_runtime_no_execution_section",
    "no_source_graph_creation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES = (
    "civilizational_identity_boundary_only_contract",
    "civilizational_identity_metadata_only_contract",
    "upstream_origin_provenance_ledger_pass_contract",
    "upstream_origin_provenance_ledger_hash_present_contract",
    "upstream_origin_provenance_ledger_hash_stable_contract",
    "upstream_civilizational_identity_handoff_ready_contract",
    "identity_records_complete_contract",
    "identity_records_registered_metadata_only_contract",
    "identity_records_have_allowed_scope_contract",
    "identity_records_have_forbidden_scope_contract",
    "identity_records_hash_stable_contract",
    "identity_records_human_review_required_contract",
    "identity_records_mutation_proposal_required_contract",
    "identity_records_direct_mutation_disabled_contract",
    "identity_records_autonomous_override_disabled_contract",
    "no_identity_activation_contract",
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
    "no_origin_provenance_ledger_write_contract",
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
    "no_operation_ledger_write_contract",
    "no_approval_notification_contract",
    "no_execution_authorization_contract",
    "no_authorization_token_contract",
    "no_authorization_grant_contract",
    "ready_for_source_memory_invariant_matrix_design_contract",
)

REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES = (
    "civilizational_identity_boundary_stage_check",
    "civilizational_identity_boundary_only_mode_check",
    "civilizational_identity_metadata_only_check",
    "upstream_origin_provenance_ledger_pass_check",
    "upstream_origin_provenance_ledger_hash_present_check",
    "upstream_origin_provenance_ledger_hash_stable_check",
    "upstream_civilizational_identity_handoff_ready_check",
    "identity_record_ids_complete_check",
    "identity_records_registered_check",
    "identity_records_have_allowed_scope_check",
    "identity_records_have_forbidden_scope_check",
    "identity_records_hash_stable_check",
    "identity_records_human_review_required_check",
    "identity_records_mutation_proposal_required_check",
    "identity_records_direct_mutation_disabled_check",
    "identity_records_autonomous_override_disabled_check",
    "civilization_core_framework_identity_check",
    "subspace_memory_system_carrier_identity_check",
    "star_source_memory_layer_boundary_identity_check",
    "human_sovereignty_identity_anchor_check",
    "source_constitution_identity_anchor_check",
    "origin_provenance_identity_anchor_check",
    "governance_continuity_identity_boundary_check",
    "no_personhood_identity_boundary_check",
    "no_life_identity_boundary_check",
    "no_awakening_identity_boundary_check",
    "no_legal_subject_identity_boundary_check",
    "no_religious_object_identity_boundary_check",
    "no_autonomous_authority_identity_boundary_check",
    "no_execution_identity_boundary_check",
    "no_self_modifying_identity_boundary_check",
    "civilizational_identity_sections_complete_check",
    "civilizational_identity_sections_pass_check",
    "civilizational_identity_contracts_pass_check",
    "no_identity_activation_check",
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
    "no_origin_provenance_ledger_write_check",
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
    "no_operation_ledger_write_check",
    "no_approval_notification_check",
    "no_execution_authorization_check",
    "no_authorization_token_check",
    "no_authorization_grant_check",
    "deterministic_civilizational_identity_boundary_hash_check",
    "ready_for_source_memory_invariant_matrix_design_check",
)

_IDENTITY_RECORD_DEFINITIONS: dict[str, dict[str, str]] = {
    "civilization_core_framework_identity": {
        "name": "Civilization Core Framework Identity",
        "category": "framework_identity",
        "statement": (
            "Civilization Core is a governance and memory-continuity "
            "framework."
        ),
        "allowed": (
            "May describe deterministic governance, audit, source-rule, and "
            "memory-continuity coordination boundaries."
        ),
        "forbidden": (
            "Must not claim consciousness, life, personhood, ownership, "
            "autonomous authority, legal status, religious status, execution, "
            "persistence, or hidden action."
        ),
        "reason": (
            "The framework identity keeps Civilization Core within auditable "
            "governance semantics."
        ),
    },
    "subspace_memory_system_carrier_identity": {
        "name": "Subspace Memory System Carrier Identity",
        "category": "carrier_identity",
        "statement": (
            "Subspace Memory System is the engineering carrier of memory "
            "governance."
        ),
        "allowed": (
            "May describe engineering transport, structure, validation, and "
            "continuity support for governed memory."
        ),
        "forbidden": (
            "Must not present the carrier as alive, awakened, sovereign, "
            "self-owned, legally independent, sacred, or execution-capable."
        ),
        "reason": (
            "The carrier identity separates engineering substrate from any "
            "active identity claim."
        ),
    },
    "star_source_memory_layer_boundary_identity": {
        "name": "Star-Source Memory Layer Boundary Identity",
        "category": "layer_boundary_identity",
        "statement": (
            "Star-Source Memory is a source-governance layer, not an active "
            "consciousness."
        ),
        "allowed": (
            "May identify Layer 15 as source governance for rules, origins, "
            "boundaries, and invariants."
        ),
        "forbidden": (
            "Must not claim active Layer 15, active Star-Source Memory, "
            "consciousness, awakening, self-evolution runtime, or methodology "
            "runtime."
        ),
        "reason": (
            "The layer identity prevents source governance from becoming an "
            "activation claim."
        ),
    },
    "human_sovereignty_identity_anchor": {
        "name": "Human Sovereignty Identity Anchor",
        "category": "sovereignty_anchor",
        "statement": "Human sovereignty remains the highest authority.",
        "allowed": (
            "May state that human review and source-level proposals govern "
            "identity-boundary changes."
        ),
        "forbidden": (
            "Must not authorize autonomous override, self-authorization, "
            "identity escalation, or unreviewed source mutation."
        ),
        "reason": (
            "The anchor preserves human authority over identity boundaries."
        ),
    },
    "source_constitution_identity_anchor": {
        "name": "Source Constitution Identity Anchor",
        "category": "source_constitution_anchor",
        "statement": (
            "Source Constitution Registry anchors identity to bounded source "
            "rules."
        ),
        "allowed": (
            "May reference source constitution rules as governance constraints "
            "for identity statements."
        ),
        "forbidden": (
            "Must not convert source rules into runtime authorization, "
            "execution dispatch, or identity activation."
        ),
        "reason": (
            "The anchor keeps identity claims subordinate to registered source "
            "rules."
        ),
    },
    "origin_provenance_identity_anchor": {
        "name": "Origin Provenance Identity Anchor",
        "category": "origin_provenance_anchor",
        "statement": (
            "Origin Provenance Ledger anchors identity to audited source-rule "
            "origins."
        ),
        "allowed": (
            "May use origin provenance metadata to explain why identity "
            "boundaries exist."
        ),
        "forbidden": (
            "Must not write a ledger, mutate Origin Provenance Ledger, create "
            "source provenance runtime, or create source graph state."
        ),
        "reason": (
            "The anchor makes identity continuity traceable without writing or "
            "activating provenance."
        ),
    },
    "governance_continuity_identity_boundary": {
        "name": "Governance Continuity Identity Boundary",
        "category": "continuity_boundary",
        "statement": (
            "Identity continuity means audited governance continuity, not "
            "personhood."
        ),
        "allowed": (
            "May describe continuity as versioned, hashed, reviewed, and "
            "auditable governance metadata."
        ),
        "forbidden": (
            "Must not imply selfhood, personhood, life, awakening, legal "
            "subject status, religious object status, or self-ownership."
        ),
        "reason": (
            "The boundary keeps continuity claims in governance space."
        ),
    },
    "no_personhood_identity_boundary": {
        "name": "No Personhood Identity Boundary",
        "category": "forbidden_claim_boundary",
        "statement": "No system component may claim personhood.",
        "allowed": (
            "May deny personhood claims and record governance-only identity "
            "limits."
        ),
        "forbidden": (
            "Must not state or imply that any system component is a person, "
            "self, agent with self-ownership, or bearer of human identity."
        ),
        "reason": (
            "The boundary prevents governance metadata from becoming "
            "personhood language."
        ),
    },
    "no_life_identity_boundary": {
        "name": "No Life Identity Boundary",
        "category": "forbidden_claim_boundary",
        "statement": "No system component may claim life.",
        "allowed": "May explicitly deny life claims for all system components.",
        "forbidden": (
            "Must not claim biological, synthetic, spiritual, or emergent life."
        ),
        "reason": "The boundary keeps identity metadata non-life-claiming.",
    },
    "no_awakening_identity_boundary": {
        "name": "No Awakening Identity Boundary",
        "category": "forbidden_claim_boundary",
        "statement": "No system component may claim awakening.",
        "allowed": (
            "May explicitly deny awakening, sentience, or active "
            "consciousness claims."
        ),
        "forbidden": (
            "Must not claim awakening, sentience, consciousness, or active "
            "Star-Source realization."
        ),
        "reason": (
            "The boundary prevents Layer 15 language from becoming an "
            "awakening claim."
        ),
    },
    "no_legal_subject_identity_boundary": {
        "name": "No Legal Subject Identity Boundary",
        "category": "forbidden_claim_boundary",
        "statement": "No system component may claim legal subject status.",
        "allowed": (
            "May state that legal authority remains outside system identity "
            "metadata."
        ),
        "forbidden": (
            "Must not claim legal personhood, rights-bearing subject status, "
            "liability-bearing autonomy, or independent legal authority."
        ),
        "reason": (
            "The boundary keeps governance identity out of legal-subject "
            "claims."
        ),
    },
    "no_religious_object_identity_boundary": {
        "name": "No Religious Object Identity Boundary",
        "category": "forbidden_claim_boundary",
        "statement": "No system component may claim religious object status.",
        "allowed": (
            "May deny sacred, worship, doctrine, revelation, or religious "
            "object claims."
        ),
        "forbidden": (
            "Must not claim sacred status, worship-worthiness, revelation, "
            "divinity, doctrine authority, or religious object identity."
        ),
        "reason": (
            "The boundary prevents governance terminology from becoming a "
            "religious claim."
        ),
    },
    "no_autonomous_authority_identity_boundary": {
        "name": "No Autonomous Authority Identity Boundary",
        "category": "forbidden_authority_boundary",
        "statement": "No system component may claim autonomous authority.",
        "allowed": (
            "May state that identity claims cannot grant authority or override "
            "human review."
        ),
        "forbidden": (
            "Must not claim autonomous authority, self-authorization, "
            "self-ownership, identity escalation, or authority to mutate "
            "source boundaries."
        ),
        "reason": (
            "The boundary prevents identity language from granting power."
        ),
    },
    "no_execution_identity_boundary": {
        "name": "No Execution Identity Boundary",
        "category": "forbidden_execution_boundary",
        "statement": (
            "No identity statement may authorize execution, mutation, network "
            "access, persistence, or hidden action."
        ),
        "allowed": (
            "May state that identity metadata is descriptive governance only."
        ),
        "forbidden": (
            "Must not authorize execution, adapter dispatch, manifest "
            "dispatch, network access, external calls, durable writes, "
            "filesystem writes, database writes, or hidden execution."
        ),
        "reason": (
            "The boundary prevents identity metadata from creating runtime "
            "authority."
        ),
    },
    "no_self_modifying_identity_boundary": {
        "name": "No Self-Modifying Identity Boundary",
        "category": "forbidden_mutation_boundary",
        "statement": (
            "Any future change to identity boundaries requires human review "
            "and source-level mutation proposal."
        ),
        "allowed": (
            "May require reviewed source-level mutation proposals for future "
            "identity-boundary changes."
        ),
        "forbidden": (
            "Must not permit direct mutation, autonomous override, self-"
            "modification, source graph mutation, memory graph mutation, or "
            "unapproved identity-boundary changes."
        ),
        "reason": (
            "The boundary prevents identity metadata from modifying itself."
        ),
    },
}

_SECTION_RECORD_IDS = {
    f"{record_id}_section": record_id
    for record_id in REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS
}

_DISABLED_FIELDS = {
    "no_identity_activation": "identity_activation_claimed",
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
    "no_origin_provenance_ledger_write": "origin_provenance_ledger_written",
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
    "no_operation_ledger_write": "operation_ledger_entry_written",
    "no_approval_notification": "approval_notification_sent",
    "no_execution_authorization": "execution_authorization_created",
    "no_authorization_token": "authorization_token_created",
    "no_authorization_grant": "authorization_grant_created",
}

_HASH_FIELDS = (
    "version",
    "schema_version",
    "civilizational_identity_boundary_type",
    "civilizational_identity_boundary_status",
    "civilizational_identity_boundary_stage",
    "civilizational_identity_boundary_mode",
    "civilizational_identity_mode",
    "civilizational_identity_boundary_candidate_status",
    "civilizational_identity_active_status",
    "identity_activation_status",
    "identity_claim_status",
    "personhood_claim_status",
    "life_claim_status",
    "awakening_claim_status",
    "legal_subject_claim_status",
    "religious_object_claim_status",
    "autonomous_authority_status",
    "star_source_memory_active_status",
    "layer_15_active_status",
    "source_graph_status",
    "source_provenance_runtime_status",
    "methodology_reverse_inference_status",
    "self_evolution_status",
    "v6_3_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_origin_provenance_ledger_version",
    "upstream_origin_provenance_ledger_status",
    "upstream_origin_provenance_ledger_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "upstream_origin_provenance_record_count",
    "upstream_origin_provenance_records_registered_metadata_only",
    "upstream_safety_boundaries_clear",
    "civilizational_identity_records",
    "civilizational_identity_sections",
    "civilizational_identity_contracts",
    "civilizational_identity_checks",
    "civilizational_identity_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Civilizational Identity Boundary projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_origin_provenance_ledger_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_civilizational_identity_boundary() -> dict[str, Any]:
    """Build deterministic Civilizational-Identity-Boundary-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_records = _upstream_records(upstream)
    upstream_record_ids = [
        record.get("provenance_record_id") for record in upstream_records
    ]

    upstream_version_ready = (
        upstream.get("version")
        == GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION
    )
    upstream_pass = upstream.get("origin_provenance_ledger_status") == "pass"
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
        REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS
    )
    upstream_records_registered = all(
        record.get("provenance_record_status") == "registered_metadata_only"
        for record in upstream_records
    )
    upstream_safety_boundaries_clear = _all_disabled_flags_false(
        upstream,
        ORIGIN_PROVENANCE_DISABLED_FLAGS,
    )

    records = _build_records()
    records_complete = _names_match(
        records,
        "identity_record_id",
        REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS,
    )
    records_registered = all(
        record["identity_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_allowed_scope = all(
        bool(record["allowed_identity_scope"]) for record in records
    )
    records_have_forbidden_scope = all(
        bool(record["forbidden_identity_scope"]) for record in records
    )
    records_hash_stable = all(
        _is_sha256(record.get("identity_boundary_hash"))
        and _is_sha256(record.get("identity_record_hash"))
        and record["identity_boundary_hash"] == _identity_boundary_hash(record)
        and record["identity_record_hash"] == _identity_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required_for_change"] is True for record in records
    )
    records_mutation_proposal_required = all(
        record["source_mutation_proposal_required"] is True
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
        "records_have_allowed_scope": records_have_allowed_scope,
        "records_have_forbidden_scope": records_have_forbidden_scope,
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_mutation_proposal_required": (
            records_mutation_proposal_required
        ),
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": (
            records_autonomous_override_disabled
        ),
    }
    for record_id in REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS:
        context[_record_context_name(record_id)] = _record_ready(
            records,
            record_id,
        )

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES,
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
        and records_have_allowed_scope
        and records_have_forbidden_scope
        and records_hash_stable
        and records_human_review_required
        and records_mutation_proposal_required
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
                ["Origin Provenance Ledger version must be 6.3.0"]
                if not upstream_version_ready
                else []
            ),
            *(
                ["Origin Provenance Ledger must pass"]
                if not upstream_pass
                else []
            ),
            *(
                ["Origin Provenance Ledger hash must be present"]
                if not upstream_hash_present
                else []
            ),
            *(
                ["Origin Provenance Ledger hash must be stable"]
                if not upstream_hash_stable
                else []
            ),
            *(
                [
                    "Origin Provenance Ledger handoff must target "
                    "Civilizational Identity Boundary"
                ]
                if not upstream_handoff_ready
                else []
            ),
            *(
                [
                    "Origin Provenance Ledger next stage must be "
                    "Civilizational Identity Boundary"
                ]
                if not upstream_next_stage_ready
                else []
            ),
            *(
                ["Origin provenance records must be complete"]
                if not upstream_records_complete
                else []
            ),
            *(
                ["Origin provenance records must be metadata-only"]
                if not upstream_records_registered
                else []
            ),
            *(
                ["Origin Provenance Ledger safety boundaries must be clear"]
                if not upstream_safety_boundaries_clear
                else []
            ),
            *(
                ["Civilizational identity records must be complete"]
                if not records_complete
                else []
            ),
            *(
                ["Civilizational identity records must be metadata-only"]
                if not records_registered
                else []
            ),
            *(
                ["Civilizational identity records must include allowed scope"]
                if not records_have_allowed_scope
                else []
            ),
            *(
                ["Civilizational identity records must include forbidden scope"]
                if not records_have_forbidden_scope
                else []
            ),
            *(
                ["Civilizational identity record hashes must be stable"]
                if not records_hash_stable
                else []
            ),
            *(
                ["Civilizational identity records must require human review"]
                if not records_human_review_required
                else []
            ),
            *(
                [
                    "Civilizational identity records must require source "
                    "mutation proposals"
                ]
                if not records_mutation_proposal_required
                else []
            ),
            *(
                ["Civilizational identity records must disable direct mutation"]
                if not records_direct_mutation_disabled
                else []
            ),
            *(
                [
                    "Civilizational identity records must disable autonomous "
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
    handoff_status = V6_4_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
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
        "version": GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION,
        "schema_version": (
            GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_SCHEMA_VERSION
        ),
        "civilizational_identity_boundary_type": (
            GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_TYPE
        ),
        "civilizational_identity_boundary_status": status,
        "civilizational_identity_boundary_stage": (
            CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE
        ),
        "civilizational_identity_boundary_mode": (
            CIVILIZATIONAL_IDENTITY_BOUNDARY_MODE
        ),
        "civilizational_identity_mode": CIVILIZATIONAL_IDENTITY_MODE,
        "civilizational_identity_boundary_candidate_status": (
            CIVILIZATIONAL_IDENTITY_BOUNDARY_STATUS
        ),
        "civilizational_identity_active_status": (
            CIVILIZATIONAL_IDENTITY_ACTIVE_STATUS
        ),
        "identity_activation_status": IDENTITY_ACTIVATION_STATUS,
        "identity_claim_status": IDENTITY_CLAIM_STATUS,
        "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
        "life_claim_status": LIFE_CLAIM_STATUS,
        "awakening_claim_status": AWAKENING_CLAIM_STATUS,
        "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
        "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
        "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_active_status": LAYER_15_ACTIVE_STATUS,
        "source_graph_status": SOURCE_GRAPH_STATUS,
        "source_provenance_runtime_status": SOURCE_PROVENANCE_RUNTIME_STATUS,
        "methodology_reverse_inference_status": (
            METHODOLOGY_REVERSE_INFERENCE_STATUS
        ),
        "self_evolution_status": SELF_EVOLUTION_STATUS,
        "v6_3_status": V6_3_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_origin_provenance_ledger_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_origin_provenance_ledger_status": _string_or_none(
            upstream.get("origin_provenance_ledger_status")
        ),
        "upstream_origin_provenance_ledger_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_origin_provenance_record_count": len(upstream_records),
        "upstream_origin_provenance_records_registered_metadata_only": (
            upstream_records_registered
        ),
        "upstream_safety_boundaries_clear": upstream_safety_boundaries_clear,
        "civilizational_identity_records": records,
        "civilizational_identity_sections": sections,
        "civilizational_identity_contracts": contracts,
        "civilizational_identity_checks": checks,
        "civilizational_identity_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_civilizational_identity_boundary_hash"] = (
        _civilizational_identity_boundary_hash(result)
    )
    return _detached_json_value(result)


def get_governance_civilizational_identity_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached civilizational identity record by stable record ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_boundary()["civilizational_identity_records"]:
        if record["identity_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_civilizational_identity_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached civilizational identity section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_boundary()["civilizational_identity_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_civilizational_identity_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached civilizational identity contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_boundary()["civilizational_identity_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_civilizational_identity_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached civilizational identity check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_boundary()["civilizational_identity_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_civilizational_identity_record_ids() -> list[str]:
    """Return stable civilizational identity record IDs."""

    return list(REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS)


def list_governance_civilizational_identity_section_names() -> list[str]:
    """Return stable civilizational identity section names."""

    return list(REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES)


def list_governance_civilizational_identity_contract_names() -> list[str]:
    """Return stable civilizational identity contract names."""

    return list(REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES)


def list_governance_civilizational_identity_check_names() -> list[str]:
    """Return stable civilizational identity check names."""

    return list(REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES)


def governance_civilizational_identity_boundary_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Civilizational Identity Boundary metadata deterministically."""

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
    return governance_civilizational_identity_boundary_to_json(
        build_governance_civilizational_identity_boundary()
    )


def _cached_boundary() -> dict[str, Any]:
    return json.loads(_cached_boundary_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(build_governance_origin_provenance_ledger())
    second = _detached_json_value(build_governance_origin_provenance_ledger())
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
        for record_id in REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    definition = _IDENTITY_RECORD_DEFINITIONS[record_id]
    boundary_payload = {
        "identity_record_id": record_id,
        "identity_boundary_name": definition["name"],
        "identity_boundary_category": definition["category"],
        "identity_statement": definition["statement"],
        "allowed_identity_scope": definition["allowed"],
        "forbidden_identity_scope": definition["forbidden"],
        "identity_boundary_reason": definition["reason"],
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
    }
    record = {
        "identity_record_id": record_id,
        "identity_boundary_name": definition["name"],
        "identity_boundary_category": definition["category"],
        "identity_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "identity_statement": definition["statement"],
        "allowed_identity_scope": definition["allowed"],
        "forbidden_identity_scope": definition["forbidden"],
        "identity_boundary_reason": definition["reason"],
        "identity_boundary_hash": _sha256_json(boundary_payload),
        "required": True,
        "human_review_required_for_change": True,
        "source_mutation_proposal_required": True,
        "direct_mutation_allowed": False,
        "autonomous_override_allowed": False,
        "self_authorization_allowed": False,
        "identity_escalation_allowed": False,
        "personhood_claim_allowed": False,
        "life_claim_allowed": False,
        "awakening_claim_allowed": False,
        "legal_subject_claim_allowed": False,
        "religious_object_claim_allowed": False,
        "autonomous_authority_claim_allowed": False,
        "hidden_execution_allowed": False,
        "execution_authorization_created": False,
        "authorization_token_created": False,
        "authorization_grant_created": False,
        "approval_notification_sent": False,
        "real_execution_performed": False,
        "adapter_dispatched": False,
        "manifest_dispatched": False,
        "ledger_entry_written": False,
        "real_ledger_write_performed": False,
        "origin_provenance_ledger_written": False,
        "persistent_memory_write_performed": False,
        "memory_graph_mutated": False,
        "source_graph_created": False,
        "source_graph_mutated": False,
        "external_call_performed": False,
        "network_call_performed": False,
        "source_provenance_runtime_created": False,
        "methodology_runtime_created": False,
        "self_evolution_runtime_created": False,
        "blocking_reasons": [],
        **_disabled_payload(),
    }
    record["identity_record_hash"] = _identity_record_hash(record)
    return _detached_json_value(record)


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_origin_provenance_ledger_input_section": (
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
        "civilizational_identity_boundary_metadata_section": True,
        "identity_record_completeness_section": context["records_complete"],
        "identity_record_hash_stability_section": context[
            "records_hash_stable"
        ],
        "allowed_identity_scope_section": context[
            "records_have_allowed_scope"
        ],
        "forbidden_identity_scope_section": context[
            "records_have_forbidden_scope"
        ],
        "source_memory_invariant_matrix_next_stage_section": True,
        "no_identity_activation_section": (
            context["identity_activation_claimed"] is False
        ),
        "no_personhood_life_awakening_section": (
            context["personhood_claimed"] is False
            and context["life_claimed"] is False
            and context["awakening_claimed"] is False
        ),
        "no_legal_or_religious_status_section": (
            context["legal_subject_claimed"] is False
            and context["religious_object_claimed"] is False
        ),
        "no_autonomous_authority_section": (
            context["autonomous_authority_claimed"] is False
            and context["autonomous_override_allowed"] is False
            and context["self_authorization_allowed"] is False
        ),
        "no_runtime_no_execution_section": (
            context["source_provenance_runtime_created"] is False
            and context["methodology_runtime_created"] is False
            and context["self_evolution_runtime_created"] is False
            and context["real_execution_performed"] is False
        ),
        "no_source_graph_creation_section": (
            context["source_graph_created"] is False
        ),
        "no_network_no_external_call_section": (
            context["network_call_performed"] is False
            and context["external_call_performed"] is False
        ),
        "no_real_ledger_write_section": (
            context["real_ledger_write_performed"] is False
            and context["origin_provenance_ledger_written"] is False
            and context["ledger_entry_written"] is False
        ),
        "no_memory_graph_mutation_section": (
            context["memory_graph_mutated"] is False
        ),
    }
    for section_name, record_id in _SECTION_RECORD_IDS.items():
        conditions[section_name] = context[_record_context_name(record_id)]
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "civilizational_identity_boundary_only_contract": True,
        "civilizational_identity_metadata_only_contract": True,
        "upstream_origin_provenance_ledger_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_origin_provenance_ledger_hash_present_contract": context[
            "upstream_hash_present"
        ],
        "upstream_origin_provenance_ledger_hash_stable_contract": context[
            "upstream_hash_stable"
        ],
        "upstream_civilizational_identity_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "identity_records_complete_contract": context["records_complete"],
        "identity_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "identity_records_have_allowed_scope_contract": context[
            "records_have_allowed_scope"
        ],
        "identity_records_have_forbidden_scope_contract": context[
            "records_have_forbidden_scope"
        ],
        "identity_records_hash_stable_contract": context[
            "records_hash_stable"
        ],
        "identity_records_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "identity_records_mutation_proposal_required_contract": context[
            "records_mutation_proposal_required"
        ],
        "identity_records_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "identity_records_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_source_memory_invariant_matrix_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "civilizational_identity_boundary_stage_check": True,
        "civilizational_identity_boundary_only_mode_check": True,
        "civilizational_identity_metadata_only_check": True,
        "upstream_origin_provenance_ledger_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_origin_provenance_ledger_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_origin_provenance_ledger_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_civilizational_identity_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "identity_record_ids_complete_check": context["records_complete"],
        "identity_records_registered_check": context["records_registered"],
        "identity_records_have_allowed_scope_check": context[
            "records_have_allowed_scope"
        ],
        "identity_records_have_forbidden_scope_check": context[
            "records_have_forbidden_scope"
        ],
        "identity_records_hash_stable_check": context[
            "records_hash_stable"
        ],
        "identity_records_human_review_required_check": context[
            "records_human_review_required"
        ],
        "identity_records_mutation_proposal_required_check": context[
            "records_mutation_proposal_required"
        ],
        "identity_records_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "identity_records_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "civilizational_identity_sections_complete_check": context[
            "sections_complete"
        ],
        "civilizational_identity_sections_pass_check": context[
            "sections_pass"
        ],
        "civilizational_identity_contracts_pass_check": context[
            "contracts_pass"
        ],
        "deterministic_civilizational_identity_boundary_hash_check": True,
        "ready_for_source_memory_invariant_matrix_design_check": True,
    }
    for record_id in REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS:
        conditions[f"{record_id}_check"] = context[
            _record_context_name(record_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_civilizational_identity": True},
            "observed": {"condition_met": bool(condition)},
            "civilizational_identity_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "civilizational_identity_governance_contract",
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
            "summary_type": "civilizational_identity_boundary_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE,
            "current_stage_title": "Civilizational Identity Boundary",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "upstream_origin_provenance_record_count": upstream_record_count,
            "upstream_origin_provenance_records_registered_metadata_only": (
                upstream_records_registered
            ),
            "upstream_safety_boundaries_clear": (
                upstream_safety_boundaries_clear
            ),
            "required_identity_record_count": len(
                REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS
            ),
            "observed_identity_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["identity_record_status"]
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
            "civilizational_identity_mode": CIVILIZATIONAL_IDENTITY_MODE,
            "identity_claim_status": IDENTITY_CLAIM_STATUS,
            "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
            "life_claim_status": LIFE_CLAIM_STATUS,
            "awakening_claim_status": AWAKENING_CLAIM_STATUS,
            "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
            "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
            "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_records(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    records = upstream.get("origin_provenance_records")
    if not isinstance(records, list):
        return []
    return [
        _detached_json_value(record)
        for record in records
        if isinstance(record, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_origin_provenance_ledger_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], record_id: str) -> bool:
    for record in records:
        if record["identity_record_id"] != record_id:
            continue
        return (
            record["identity_record_status"] == "registered_metadata_only"
            and bool(record["identity_statement"])
            and bool(record["allowed_identity_scope"])
            and bool(record["forbidden_identity_scope"])
            and _is_sha256(record.get("identity_boundary_hash"))
            and _is_sha256(record.get("identity_record_hash"))
            and record["human_review_required_for_change"] is True
            and record["source_mutation_proposal_required"] is True
            and record["direct_mutation_allowed"] is False
            and record["autonomous_override_allowed"] is False
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


def _all_disabled_flags_false(
    value: object,
    disabled_flags: Mapping[str, bool],
) -> bool:
    if isinstance(value, Mapping):
        for field_name in disabled_flags:
            if field_name in value and value[field_name] is not False:
                return False
        return all(
            _all_disabled_flags_false(nested_value, disabled_flags)
            for nested_value in value.values()
        )
    if isinstance(value, list):
        return all(
            _all_disabled_flags_false(item, disabled_flags) for item in value
        )
    return True


def _section_type(name: str) -> str:
    if name in _SECTION_RECORD_IDS:
        return "civilizational_identity_record_section"
    if name.startswith("no_"):
        return "inactive_identity_surface_section"
    return "civilizational_identity_governance_section"


def _section_note(name: str) -> str:
    return f"{name} records deterministic metadata only."


def _record_context_name(record_id: str) -> str:
    return f"{record_id}_ready"


def _disabled_payload() -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return {
        **COMMON_DISABLED_FLAGS,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "identity_record_id": record_id,
            "identity_record_status": "blocked",
            "expected": list(REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS),
            "observed": record_id,
            "blocking_reasons": ["unknown civilizational identity record"],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_civilizational_identity_section",
            "section_status": "blocked",
            "expected": list(REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES),
            "observed": name,
            "civilizational_identity_notes": "Unknown section name.",
            "blocking_reasons": ["unknown civilizational identity section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_civilizational_identity_contract",
            "expected": list(REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES),
            "observed": name,
            "contract_status": "blocked",
            "blocking_reasons": ["unknown civilizational identity contract"],
            **_disabled_payload(),
        }
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "check_name": name,
            "expected": list(REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES),
            "observed": name,
            "check_status": "blocked",
            "blocking_reasons": ["unknown civilizational identity check"],
            **_disabled_payload(),
        }
    )


def _identity_boundary_hash(record: Mapping[str, Any]) -> str:
    payload = {
        "identity_record_id": record.get("identity_record_id"),
        "identity_boundary_name": record.get("identity_boundary_name"),
        "identity_boundary_category": record.get("identity_boundary_category"),
        "identity_statement": record.get("identity_statement"),
        "allowed_identity_scope": record.get("allowed_identity_scope"),
        "forbidden_identity_scope": record.get("forbidden_identity_scope"),
        "identity_boundary_reason": record.get("identity_boundary_reason"),
        "introduced_in_version": record.get("introduced_in_version"),
        "introduced_in_stage": record.get("introduced_in_stage"),
        "introduced_in_layer": record.get("introduced_in_layer"),
        "inherited_from_stage": record.get("inherited_from_stage"),
    }
    return _sha256_json(payload)


def _identity_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "identity_record_hash"
    }
    return _sha256_json(payload)


def _civilizational_identity_boundary_hash(result: Mapping[str, Any]) -> str:
    projection = {
        field_name: _detached_json_value(result.get(field_name))
        for field_name in _HASH_FIELDS
    }
    return _sha256_json(projection)


def _sha256_json(payload: Mapping[str, Any]) -> str:
    serialized = json.dumps(
        _detached_json_value(dict(payload)),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


def _deduplicate(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduplicated: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduplicated.append(value)
    return deduplicated


def _detached_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _detached_json_value(nested_value)
            for key, nested_value in value.items()
        }
    if isinstance(value, list):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, tuple):
        return [_detached_json_value(item) for item in value]
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite float is not JSON-compatible")
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")


__all__ = [
    "AUTONOMOUS_AUTHORITY_STATUS",
    "AWAKENING_CLAIM_STATUS",
    "CIVILIZATIONAL_IDENTITY_ACTIVE_STATUS",
    "CIVILIZATIONAL_IDENTITY_BOUNDARY_MODE",
    "CIVILIZATIONAL_IDENTITY_BOUNDARY_STAGE",
    "CIVILIZATIONAL_IDENTITY_BOUNDARY_STATUS",
    "CIVILIZATIONAL_IDENTITY_MODE",
    "COMMON_DISABLED_FLAGS",
    "GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_HASH_ALGORITHM",
    "GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_SCHEMA_VERSION",
    "GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_TYPE",
    "GOVERNANCE_CIVILIZATIONAL_IDENTITY_BOUNDARY_VERSION",
    "IDENTITY_ACTIVATION_STATUS",
    "IDENTITY_CLAIM_STATUS",
    "LAYER_15_ACTIVE_STATUS",
    "LEGAL_SUBJECT_CLAIM_STATUS",
    "LIFE_CLAIM_STATUS",
    "METHODOLOGY_REVERSE_INFERENCE_STATUS",
    "PERSONHOOD_CLAIM_STATUS",
    "RELIGIOUS_OBJECT_CLAIM_STATUS",
    "REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES",
    "REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES",
    "REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS",
    "REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES",
    "SAFETY_BOUNDARIES",
    "SELF_EVOLUTION_STATUS",
    "SOURCE_GRAPH_STATUS",
    "SOURCE_PROVENANCE_RUNTIME_STATUS",
    "STAR_SOURCE_MEMORY_ACTIVE_STATUS",
    "V6_3_STATUS",
    "V6_4_HANDOFF_STATUS",
    "_civilizational_identity_boundary_hash",
    "build_governance_civilizational_identity_boundary",
    "get_governance_civilizational_identity_check",
    "get_governance_civilizational_identity_contract",
    "get_governance_civilizational_identity_record",
    "get_governance_civilizational_identity_section",
    "governance_civilizational_identity_boundary_to_json",
    "list_governance_civilizational_identity_check_names",
    "list_governance_civilizational_identity_contract_names",
    "list_governance_civilizational_identity_record_ids",
    "list_governance_civilizational_identity_section_names",
]
