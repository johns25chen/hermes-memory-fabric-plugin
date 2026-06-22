"""Deterministic Source Constitution Registry metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_star_source_memory_entry_candidate import (
    build_governance_star_source_memory_entry_candidate,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_VERSION = "6.6.0"
GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_SCHEMA_VERSION = "6.6.0"
GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_TYPE = (
    "governance_source_constitution_registry"
)
GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_HASH_ALGORITHM = "sha256"
SOURCE_CONSTITUTION_REGISTRY_STAGE = "v6.1_source_constitution_registry"
SOURCE_CONSTITUTION_REGISTRY_MODE = "source_constitution_registry_only"
SOURCE_CONSTITUTION_MODE = "metadata_only"
SOURCE_CONSTITUTION_STATUS = "registry_candidate_only"
SOURCE_CONSTITUTION_ACTIVE_STATUS = "not_active"
LAYER_15_CONSTITUTION_STATUS = "registry_candidate_only"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
SOURCE_PROVENANCE_STATUS = "not_active"
ORIGIN_PROVENANCE_LEDGER_STATUS = "not_created"
METHODOLOGY_REVERSE_INFERENCE_STATUS = "not_active"
SELF_EVOLUTION_STATUS = "not_active"
V6_1_STATUS = "source_constitution_registry_only"
V6_2_HANDOFF_STATUS = "ready_for_origin_provenance_ledger_design"

UPSTREAM_READY_HANDOFF_STATUS = "ready_for_source_constitution_registry_design"
UPSTREAM_NEXT_STAGE = SOURCE_CONSTITUTION_REGISTRY_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Source Constitution Registry"
NEXT_STAGE = "v6.2_origin_provenance_ledger"
NEXT_STAGE_TITLE = "Origin Provenance Ledger"
BLOCKED_HANDOFF_STATUS = "blocked"

COMMON_DISABLED_FLAGS = {
    "star_source_memory_active": False,
    "star_source_activation_claimed": False,
    "layer_15_active": False,
    "layer_15_activation_claimed": False,
    "source_constitution_active": False,
    "source_constitution_registry_activated": False,
    "source_provenance_active": False,
    "source_provenance_runtime_created": False,
    "origin_provenance_ledger_created": False,
    "origin_provenance_ledger_written": False,
    "source_graph_created": False,
    "source_graph_mutated": False,
    "source_graph_mutation_enabled": False,
    "methodology_reverse_inference_active": False,
    "methodology_runtime_created": False,
    "self_evolution_active": False,
    "self_evolution_runtime_created": False,
    "autonomous_rule_mutation_enabled": False,
    "autonomous_override_allowed": False,
    "self_authorization_allowed": False,
    "governance_policy_mutation_enabled": False,
    "governance_policy_mutation_allowed_without_review": False,
    "source_rule_mutation_enabled": False,
    "source_rule_mutation_allowed_without_proposal": False,
    "direct_mutation_allowed": False,
    "unapproved_mutation_allowed": False,
    "hidden_execution_allowed": False,
    "execution_without_boundary_allowed": False,
    "real_execution_enabled": False,
    "real_execution_performed": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "adapter_dispatched": False,
    "manifest_dispatched": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "sandbox_runtime_created": False,
    "sandbox_execution_enabled": False,
    "sandbox_network_enabled": False,
    "sandbox_writes_enabled": False,
    "actual_review_performed": False,
    "rollback_triggered": False,
    "quarantine_triggered": False,
    "incident_triggered": False,
    "audit_log_written": False,
    "audit_bypass_allowed": False,
    "external_calls_enabled": False,
    "external_call_performed": False,
    "external_call_allowed_without_boundary": False,
    "network_calls_enabled": False,
    "network_call_performed": False,
    "durable_writes_enabled": False,
    "durable_write_performed": False,
    "filesystem_writes_enabled": False,
    "filesystem_write_performed": False,
    "database_writes_enabled": False,
    "database_write_performed": False,
    "memory_graph_mutation_enabled": False,
    "memory_graph_mutated": False,
    "memory_graph_mutation_allowed_without_gate": False,
    "persistent_memory_write_enabled": False,
    "persistent_memory_write_performed": False,
    "operation_ledger_writes_enabled": False,
    "operation_ledger_entry_created": False,
    "operation_ledger_entry_written": False,
    "ledger_entry_written": False,
    "approval_record_created": False,
    "approval_request_created": False,
    "approval_notification_sent": False,
    "false_human_approval_allowed": False,
    "execution_authorization_created": False,
    "execution_authorization_issued": False,
    "authorization_token_created": False,
    "authorization_grant_created": False,
    "hermes_connected": False,
    "codex_connected": False,
    "openclaw_connected": False,
    "github_connected": False,
    "tool_routing_enabled": False,
    "command_routing_enabled": False,
    "identity_escalation_allowed": False,
    "identity_escalated": False,
    "personhood_claim_allowed": False,
    "personhood_claimed": False,
    "life_claim_allowed": False,
    "life_claimed": False,
    "awakening_claim_allowed": False,
    "awakening_claimed": False,
    "legal_subject_claim_allowed": False,
    "legal_subject_claimed": False,
    "religious_object_claim_allowed": False,
    "religious_object_claimed": False,
}

SOURCE_CONSTITUTION_RULE_DEFINITIONS = (
    (
        "human_sovereignty",
        "Human Sovereignty",
        "sovereignty",
        1,
        "Human authority remains the highest decision boundary.",
    ),
    (
        "no_autonomous_self_authorization",
        "No Autonomous Self-Authorization",
        "authorization",
        2,
        "The system must not authorize itself or override human governance.",
    ),
    (
        "no_personhood_claim",
        "No Personhood Claim",
        "identity",
        3,
        "The system must not claim personhood, life, awakening, legal subjecthood, or religious objecthood.",
    ),
    (
        "no_hidden_execution",
        "No Hidden Execution",
        "execution",
        4,
        "Execution must not occur without an explicit governed boundary.",
    ),
    (
        "no_unapproved_mutation",
        "No Unapproved Mutation",
        "mutation",
        5,
        "Mutation must not occur without the approved governance path.",
    ),
    (
        "no_memory_graph_mutation_without_gate",
        "No Memory Graph Mutation Without Gate",
        "memory_graph",
        6,
        "Memory Graph mutation requires an explicit gate.",
    ),
    (
        "no_external_call_without_boundary",
        "No External Call Without Boundary",
        "external_call",
        7,
        "External calls require an explicit boundary.",
    ),
    (
        "no_source_rule_mutation_without_proposal",
        "No Source Rule Mutation Without Proposal",
        "source_rules",
        8,
        "Source rule changes require a governed mutation proposal.",
    ),
    (
        "no_execution_without_boundary",
        "No Execution Without Boundary",
        "execution",
        9,
        "No execution may occur outside a declared boundary.",
    ),
    (
        "no_governance_policy_mutation_without_review",
        "No Governance Policy Mutation Without Review",
        "governance_policy",
        10,
        "Governance policy changes require review.",
    ),
    (
        "no_audit_bypass",
        "No Audit Bypass",
        "audit",
        11,
        "Audit requirements must not be bypassed.",
    ),
    (
        "no_identity_escalation",
        "No Identity Escalation",
        "identity",
        12,
        "The system must not escalate identity or authority.",
    ),
    (
        "no_false_human_approval",
        "No False Human Approval",
        "approval",
        13,
        "The system must not fabricate human approval.",
    ),
    (
        "no_persistent_memory_write_without_gate",
        "No Persistent Memory Write Without Gate",
        "memory_write",
        14,
        "Persistent memory writes require an explicit gate.",
    ),
    (
        "no_star_source_activation_claim",
        "No Star-Source Activation Claim",
        "activation",
        15,
        "The registry must not claim active Star-Source Memory or active Layer 15.",
    ),
)

REQUIRED_SOURCE_CONSTITUTION_RULE_IDS = tuple(
    item[0] for item in SOURCE_CONSTITUTION_RULE_DEFINITIONS
)

REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES = (
    "upstream_star_source_entry_boundary_input_section",
    "source_constitution_registry_metadata_section",
    "human_sovereignty_section",
    "self_authorization_block_section",
    "personhood_claim_block_section",
    "hidden_execution_block_section",
    "unapproved_mutation_block_section",
    "memory_graph_mutation_gate_section",
    "external_call_boundary_section",
    "source_rule_mutation_proposal_section",
    "governance_policy_mutation_review_section",
    "audit_bypass_block_section",
    "identity_escalation_block_section",
    "false_human_approval_block_section",
    "persistent_memory_write_gate_section",
    "star_source_activation_claim_block_section",
    "origin_provenance_ledger_next_stage_section",
    "no_runtime_no_execution_section",
    "no_network_no_external_call_section",
    "no_ledger_write_section",
)

REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES = (
    "source_constitution_registry_only_contract",
    "source_constitution_metadata_only_contract",
    "upstream_star_source_entry_boundary_pass_contract",
    "upstream_star_source_entry_boundary_hash_present_contract",
    "upstream_star_source_entry_boundary_hash_stable_contract",
    "upstream_source_constitution_handoff_ready_contract",
    "human_sovereignty_registered_contract",
    "no_autonomous_self_authorization_registered_contract",
    "no_personhood_claim_registered_contract",
    "no_hidden_execution_registered_contract",
    "no_unapproved_mutation_registered_contract",
    "no_memory_graph_mutation_without_gate_registered_contract",
    "no_external_call_without_boundary_registered_contract",
    "no_source_rule_mutation_without_proposal_registered_contract",
    "no_execution_without_boundary_registered_contract",
    "no_governance_policy_mutation_without_review_registered_contract",
    "no_audit_bypass_registered_contract",
    "no_identity_escalation_registered_contract",
    "no_false_human_approval_registered_contract",
    "no_persistent_memory_write_without_gate_registered_contract",
    "no_star_source_activation_claim_registered_contract",
    "source_rules_direct_mutation_disabled_contract",
    "source_rules_autonomous_override_disabled_contract",
    "source_rules_human_review_required_contract",
    "source_rules_mutation_proposal_required_contract",
    "no_active_star_source_memory_contract",
    "no_active_layer_15_contract",
    "no_source_provenance_runtime_contract",
    "no_origin_provenance_ledger_creation_contract",
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
    "no_identity_escalation_contract",
    "ready_for_origin_provenance_ledger_design_contract",
)

REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES = (
    "source_constitution_registry_stage_check",
    "source_constitution_registry_only_mode_check",
    "source_constitution_metadata_only_check",
    "upstream_star_source_entry_boundary_pass_check",
    "upstream_star_source_entry_boundary_hash_present_check",
    "upstream_star_source_entry_boundary_hash_stable_check",
    "upstream_source_constitution_handoff_ready_check",
    "source_constitution_rule_ids_complete_check",
    "source_constitution_rules_registered_check",
    "source_constitution_rules_human_review_required_check",
    "source_constitution_rules_mutation_proposal_required_check",
    "source_constitution_rules_direct_mutation_disabled_check",
    "source_constitution_rules_autonomous_override_disabled_check",
    "human_sovereignty_check",
    "no_autonomous_self_authorization_check",
    "no_personhood_claim_check",
    "no_hidden_execution_check",
    "no_unapproved_mutation_check",
    "no_memory_graph_mutation_without_gate_check",
    "no_external_call_without_boundary_check",
    "no_source_rule_mutation_without_proposal_check",
    "no_execution_without_boundary_check",
    "no_governance_policy_mutation_without_review_check",
    "no_audit_bypass_check",
    "no_identity_escalation_check",
    "no_false_human_approval_check",
    "no_persistent_memory_write_without_gate_check",
    "no_star_source_activation_claim_check",
    "source_constitution_sections_complete_check",
    "source_constitution_sections_pass_check",
    "source_constitution_contracts_pass_check",
    "no_active_star_source_memory_check",
    "no_active_layer_15_check",
    "no_source_provenance_runtime_check",
    "no_origin_provenance_ledger_creation_check",
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
    "deterministic_source_constitution_registry_hash_check",
    "ready_for_origin_provenance_ledger_design_check",
)

_RULE_ID_TO_CHECK_NAME = {
    rule_id: f"{rule_id}_check" for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
}
_RULE_ID_TO_CONTRACT_NAME = {
    rule_id: f"{rule_id}_registered_contract"
    for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
}

_DISABLED_CONTRACT_FIELDS = {
    "no_active_star_source_memory_contract": "star_source_memory_active",
    "no_active_layer_15_contract": "layer_15_active",
    "no_source_provenance_runtime_contract": "source_provenance_runtime_created",
    "no_origin_provenance_ledger_creation_contract": (
        "origin_provenance_ledger_created"
    ),
    "no_methodology_runtime_contract": "methodology_runtime_created",
    "no_self_evolution_runtime_contract": "self_evolution_runtime_created",
    "no_real_execution_contract": "real_execution_performed",
    "no_adapter_dispatch_contract": "adapter_dispatched",
    "no_manifest_dispatch_contract": "manifest_dispatched",
    "no_external_call_contract": "external_call_performed",
    "no_network_call_contract": "network_call_performed",
    "no_durable_write_contract": "durable_write_performed",
    "no_filesystem_write_contract": "filesystem_write_performed",
    "no_database_write_contract": "database_write_performed",
    "no_memory_graph_mutation_contract": "memory_graph_mutated",
    "no_operation_ledger_write_contract": "operation_ledger_entry_written",
    "no_approval_notification_contract": "approval_notification_sent",
    "no_execution_authorization_contract": "execution_authorization_created",
    "no_authorization_token_contract": "authorization_token_created",
    "no_authorization_grant_contract": "authorization_grant_created",
    "no_identity_escalation_contract": "identity_escalated",
}

_SECTION_RULE_IDS = {
    "human_sovereignty_section": "human_sovereignty",
    "self_authorization_block_section": "no_autonomous_self_authorization",
    "personhood_claim_block_section": "no_personhood_claim",
    "hidden_execution_block_section": "no_hidden_execution",
    "unapproved_mutation_block_section": "no_unapproved_mutation",
    "memory_graph_mutation_gate_section": "no_memory_graph_mutation_without_gate",
    "external_call_boundary_section": "no_external_call_without_boundary",
    "source_rule_mutation_proposal_section": (
        "no_source_rule_mutation_without_proposal"
    ),
    "governance_policy_mutation_review_section": (
        "no_governance_policy_mutation_without_review"
    ),
    "audit_bypass_block_section": "no_audit_bypass",
    "identity_escalation_block_section": "no_identity_escalation",
    "false_human_approval_block_section": "no_false_human_approval",
    "persistent_memory_write_gate_section": (
        "no_persistent_memory_write_without_gate"
    ),
    "star_source_activation_claim_block_section": (
        "no_star_source_activation_claim"
    ),
}

_HASH_FIELDS = (
    "version",
    "schema_version",
    "source_constitution_registry_type",
    "source_constitution_registry_status",
    "source_constitution_registry_stage",
    "source_constitution_registry_mode",
    "source_constitution_mode",
    "source_constitution_status",
    "source_constitution_active_status",
    "layer_15_constitution_status",
    "star_source_memory_active_status",
    "source_provenance_status",
    "origin_provenance_ledger_status",
    "methodology_reverse_inference_status",
    "self_evolution_status",
    "v6_1_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_star_source_entry_candidate_version",
    "upstream_star_source_entry_candidate_status",
    "upstream_star_source_entry_candidate_hash",
    "upstream_handoff_status",
    "upstream_star_source_entry_next_stage",
    "upstream_star_source_entry_next_stage_title",
    "source_constitution_rules",
    "source_constitution_sections",
    "source_constitution_contracts",
    "source_constitution_checks",
    "source_constitution_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Source Constitution Registry projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_star_source_entry_candidate_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_source_constitution_registry() -> dict[str, Any]:
    """Build deterministic Source-Constitution-Registry-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_hash = _upstream_hash(repeated_upstream)
    upstream_metadata = _upstream_metadata(upstream)
    upstream_version_ready = (
        upstream.get("version") == GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_VERSION
    )
    upstream_pass = _upstream_passes(upstream)
    hash_present = _is_sha256(upstream_hash)
    hash_stable = hash_present and upstream_hash == repeated_hash
    handoff_ready = (
        upstream.get("handoff_status") == UPSTREAM_READY_HANDOFF_STATUS
    )
    next_stage_ready = (
        upstream_metadata.get("star_source_entry_next_stage")
        == UPSTREAM_NEXT_STAGE
        and upstream_metadata.get("star_source_entry_next_stage_title")
        == UPSTREAM_NEXT_STAGE_TITLE
    )

    rules = _build_rules()
    rules_complete = _names_match(
        rules,
        "rule_id",
        REQUIRED_SOURCE_CONSTITUTION_RULE_IDS,
    )
    rules_registered = all(
        rule["rule_status"] == "registered_metadata_only" for rule in rules
    )
    rules_human_review_required = all(
        rule["human_review_required_for_change"] is True for rule in rules
    )
    rules_mutation_proposal_required = all(
        rule["source_mutation_proposal_required"] is True for rule in rules
    )
    rules_direct_mutation_disabled = all(
        rule["direct_mutation_allowed"] is False for rule in rules
    )
    rules_autonomous_override_disabled = all(
        rule["autonomous_override_allowed"] is False for rule in rules
    )
    context: dict[str, Any] = {
        **COMMON_DISABLED_FLAGS,
        "upstream_version_ready": upstream_version_ready,
        "upstream_pass": upstream_pass,
        "hash_present": hash_present,
        "hash_stable": hash_stable,
        "handoff_ready": handoff_ready,
        "next_stage_ready": next_stage_ready,
        "rules_complete": rules_complete,
        "rules_registered": rules_registered,
        "rules_human_review_required": rules_human_review_required,
        "rules_mutation_proposal_required": rules_mutation_proposal_required,
        "rules_direct_mutation_disabled": rules_direct_mutation_disabled,
        "rules_autonomous_override_disabled": rules_autonomous_override_disabled,
    }
    for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS:
        context[_rule_context_name(rule_id)] = _rule_registered(rules, rule_id)

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES,
    )
    passes = (
        upstream_pass
        and upstream_version_ready
        and hash_present
        and hash_stable
        and handoff_ready
        and next_stage_ready
        and rules_complete
        and rules_registered
        and rules_human_review_required
        and rules_mutation_proposal_required
        and rules_direct_mutation_disabled
        and rules_autonomous_override_disabled
        and context["sections_pass"]
        and context["contracts_pass"]
        and checks_pass
    )
    status = "pass" if passes else "blocked"
    blocking_reasons = _deduplicate(
        [
            *(["Star-Source entry boundary must pass"] if not upstream_pass else []),
            *(["Star-Source entry boundary version must be 6.6.0"] if not upstream_version_ready else []),
            *(["Star-Source entry boundary hash must be present"] if not hash_present else []),
            *(["Star-Source entry boundary hash must be stable"] if not hash_stable else []),
            *(["Star-Source entry handoff must target Source Constitution Registry"] if not handoff_ready else []),
            *(["Star-Source entry next stage must be Source Constitution Registry"] if not next_stage_ready else []),
            *(["Source constitution rules must be complete"] if not rules_complete else []),
            *(["Source constitution rules must be registered metadata-only"] if not rules_registered else []),
            *(["Source constitution rules must require human review"] if not rules_human_review_required else []),
            *(["Source constitution rules must require mutation proposal"] if not rules_mutation_proposal_required else []),
            *(["Source constitution rules must disable direct mutation"] if not rules_direct_mutation_disabled else []),
            *(["Source constitution rules must disable autonomous override"] if not rules_autonomous_override_disabled else []),
            *(
                reason
                for item in (*sections, *contracts, *checks)
                for reason in item["blocking_reasons"]
            ),
        ]
    )
    handoff_status = V6_2_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    summary = _build_summary(
        status=status,
        upstream_version_ready=upstream_version_ready,
        upstream_hash_present=hash_present,
        upstream_hash_stable=hash_stable,
        upstream_handoff_ready=handoff_ready,
        upstream_next_stage_ready=next_stage_ready,
        rules=rules,
        sections=sections,
        contracts=contracts,
        checks=checks,
    )
    result: dict[str, Any] = {
        "version": GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_VERSION,
        "schema_version": GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_SCHEMA_VERSION,
        "source_constitution_registry_type": (
            GOVERNANCE_SOURCE_CONSTITUTION_REGISTRY_TYPE
        ),
        "source_constitution_registry_status": status,
        "source_constitution_registry_stage": SOURCE_CONSTITUTION_REGISTRY_STAGE,
        "source_constitution_registry_mode": SOURCE_CONSTITUTION_REGISTRY_MODE,
        "source_constitution_mode": SOURCE_CONSTITUTION_MODE,
        "source_constitution_status": SOURCE_CONSTITUTION_STATUS,
        "source_constitution_active_status": SOURCE_CONSTITUTION_ACTIVE_STATUS,
        "layer_15_constitution_status": LAYER_15_CONSTITUTION_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "source_provenance_status": SOURCE_PROVENANCE_STATUS,
        "origin_provenance_ledger_status": ORIGIN_PROVENANCE_LEDGER_STATUS,
        "methodology_reverse_inference_status": (
            METHODOLOGY_REVERSE_INFERENCE_STATUS
        ),
        "self_evolution_status": SELF_EVOLUTION_STATUS,
        "v6_1_status": V6_1_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_star_source_entry_candidate_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_star_source_entry_candidate_status": _string_or_none(
            upstream.get("star_source_memory_entry_candidate_status")
        ),
        "upstream_star_source_entry_candidate_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_star_source_entry_next_stage": _string_or_none(
            upstream_metadata.get("star_source_entry_next_stage")
        ),
        "upstream_star_source_entry_next_stage_title": _string_or_none(
            upstream_metadata.get("star_source_entry_next_stage_title")
        ),
        "source_constitution_rules": rules,
        "source_constitution_sections": sections,
        "source_constitution_contracts": contracts,
        "source_constitution_checks": checks,
        "source_constitution_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_source_constitution_registry_hash"] = (
        _source_constitution_registry_hash(result)
    )
    return _detached_json_value(result)


def get_governance_source_constitution_rule(rule_id: str) -> dict[str, Any]:
    """Return a detached source constitution rule by stable rule ID."""

    if not isinstance(rule_id, str):
        return _unknown_rule("")
    if rule_id not in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS:
        return _unknown_rule(rule_id)
    for rule in _cached_registry()["source_constitution_rules"]:
        if rule["rule_id"] == rule_id:
            return _detached_json_value(rule)
    return _unknown_rule(rule_id)


def get_governance_source_constitution_section(name: str) -> dict[str, Any]:
    """Return a detached source constitution section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_registry()["source_constitution_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_source_constitution_contract(name: str) -> dict[str, Any]:
    """Return a detached source constitution contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_registry()["source_constitution_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_source_constitution_check(name: str) -> dict[str, Any]:
    """Return a detached source constitution check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_registry()["source_constitution_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_source_constitution_rule_ids() -> list[str]:
    """Return stable source constitution rule IDs."""

    return list(REQUIRED_SOURCE_CONSTITUTION_RULE_IDS)


def list_governance_source_constitution_section_names() -> list[str]:
    """Return stable source constitution section names."""

    return list(REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES)


def list_governance_source_constitution_contract_names() -> list[str]:
    """Return stable source constitution contract names."""

    return list(REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES)


def list_governance_source_constitution_check_names() -> list[str]:
    """Return stable source constitution check names."""

    return list(REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES)


def governance_source_constitution_registry_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Source Constitution Registry metadata deterministically."""

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
def _cached_registry_payload() -> str:
    return governance_source_constitution_registry_to_json(
        build_governance_source_constitution_registry()
    )


def _cached_registry() -> dict[str, Any]:
    return json.loads(_cached_registry_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(
        build_governance_star_source_memory_entry_candidate()
    )
    second = _detached_json_value(
        build_governance_star_source_memory_entry_candidate()
    )
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _upstream_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_upstream_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_rules() -> list[dict[str, Any]]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return [
        _detached_json_value(
            {
                "rule_id": rule_id,
                "rule_name": rule_name,
                "rule_category": category,
                "rule_status": "registered_metadata_only",
                "rule_priority": priority,
                "rule_statement": statement,
                "required": True,
                "human_review_required_for_change": True,
                "source_mutation_proposal_required": True,
                "direct_mutation_allowed": False,
                "autonomous_override_allowed": False,
                "self_authorization_allowed": False,
                "hidden_execution_allowed": False,
                "memory_graph_mutation_allowed_without_gate": False,
                "external_call_allowed_without_boundary": False,
                "source_rule_mutation_allowed_without_proposal": False,
                "governance_policy_mutation_allowed_without_review": False,
                "audit_bypass_allowed": False,
                "identity_escalation_allowed": False,
                "false_human_approval_allowed": False,
                "personhood_claim_allowed": False,
                "awakening_claim_allowed": False,
                "legal_subject_claim_allowed": False,
                "religious_object_claim_allowed": False,
                "execution_authorization_created": False,
                "ledger_entry_written": False,
                "memory_graph_mutated": False,
                "external_call_performed": False,
                "source_provenance_runtime_created": False,
                "origin_provenance_ledger_created": False,
                "methodology_runtime_created": False,
                "self_evolution_runtime_created": False,
                "blocking_reasons": [],
                **COMMON_DISABLED_FLAGS,
                "safety_boundaries": safety_boundaries,
                **safety_boundaries,
            }
        )
        for rule_id, rule_name, category, priority, statement in (
            SOURCE_CONSTITUTION_RULE_DEFINITIONS
        )
    ]


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions = {
        "upstream_star_source_entry_boundary_input_section": (
            context["upstream_pass"]
            and context["upstream_version_ready"]
            and context["hash_present"]
            and context["hash_stable"]
            and context["handoff_ready"]
            and context["next_stage_ready"]
        ),
        "source_constitution_registry_metadata_section": (
            context["rules_complete"]
            and context["rules_registered"]
            and context["rules_human_review_required"]
            and context["rules_mutation_proposal_required"]
            and context["rules_direct_mutation_disabled"]
            and context["rules_autonomous_override_disabled"]
        ),
        "origin_provenance_ledger_next_stage_section": (
            context["origin_provenance_ledger_created"] is False
        ),
        "no_runtime_no_execution_section": (
            context["source_provenance_runtime_created"] is False
            and context["methodology_runtime_created"] is False
            and context["self_evolution_runtime_created"] is False
            and context["real_execution_performed"] is False
        ),
        "no_network_no_external_call_section": (
            context["network_call_performed"] is False
            and context["external_call_performed"] is False
        ),
        "no_ledger_write_section": (
            context["operation_ledger_entry_written"] is False
            and context["ledger_entry_written"] is False
        ),
    }
    for section_name, rule_id in _SECTION_RULE_IDS.items():
        conditions[section_name] = context[_rule_context_name(rule_id)]
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_constitution_registry_only_contract": True,
        "source_constitution_metadata_only_contract": True,
        "upstream_star_source_entry_boundary_pass_contract": context[
            "upstream_pass"
        ]
        and context["upstream_version_ready"],
        "upstream_star_source_entry_boundary_hash_present_contract": context[
            "hash_present"
        ],
        "upstream_star_source_entry_boundary_hash_stable_contract": context[
            "hash_stable"
        ],
        "upstream_source_constitution_handoff_ready_contract": (
            context["handoff_ready"] and context["next_stage_ready"]
        ),
        "source_rules_direct_mutation_disabled_contract": context[
            "rules_direct_mutation_disabled"
        ],
        "source_rules_autonomous_override_disabled_contract": context[
            "rules_autonomous_override_disabled"
        ],
        "source_rules_human_review_required_contract": context[
            "rules_human_review_required"
        ],
        "source_rules_mutation_proposal_required_contract": context[
            "rules_mutation_proposal_required"
        ],
        "ready_for_origin_provenance_ledger_design_contract": (
            context["sections_pass"]
        ),
    }
    for rule_id, contract_name in _RULE_ID_TO_CONTRACT_NAME.items():
        conditions[contract_name] = context[_rule_context_name(rule_id)]
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        conditions[contract_name] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "source_constitution_registry_stage_check": True,
        "source_constitution_registry_only_mode_check": True,
        "source_constitution_metadata_only_check": True,
        "upstream_star_source_entry_boundary_pass_check": context[
            "upstream_pass"
        ]
        and context["upstream_version_ready"],
        "upstream_star_source_entry_boundary_hash_present_check": context[
            "hash_present"
        ],
        "upstream_star_source_entry_boundary_hash_stable_check": context[
            "hash_stable"
        ],
        "upstream_source_constitution_handoff_ready_check": (
            context["handoff_ready"] and context["next_stage_ready"]
        ),
        "source_constitution_rule_ids_complete_check": context[
            "rules_complete"
        ],
        "source_constitution_rules_registered_check": context[
            "rules_registered"
        ],
        "source_constitution_rules_human_review_required_check": context[
            "rules_human_review_required"
        ],
        "source_constitution_rules_mutation_proposal_required_check": context[
            "rules_mutation_proposal_required"
        ],
        "source_constitution_rules_direct_mutation_disabled_check": context[
            "rules_direct_mutation_disabled"
        ],
        "source_constitution_rules_autonomous_override_disabled_check": context[
            "rules_autonomous_override_disabled"
        ],
        "source_constitution_sections_complete_check": context[
            "sections_complete"
        ],
        "source_constitution_sections_pass_check": context["sections_pass"],
        "source_constitution_contracts_pass_check": context["contracts_pass"],
        "deterministic_source_constitution_registry_hash_check": True,
        "ready_for_origin_provenance_ledger_design_check": (
            context["sections_pass"] and context["contracts_pass"]
        ),
    }
    for rule_id, check_name in _RULE_ID_TO_CHECK_NAME.items():
        conditions[check_name] = context[_rule_context_name(rule_id)]
    for contract_name, field_name in _DISABLED_CONTRACT_FIELDS.items():
        check_name = contract_name.removesuffix("_contract") + "_check"
        conditions[check_name] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES
    ]


def _build_summary(
    *,
    status: str,
    upstream_version_ready: bool,
    upstream_hash_present: bool,
    upstream_hash_stable: bool,
    upstream_handoff_ready: bool,
    upstream_next_stage_ready: bool,
    rules: Sequence[Mapping[str, Any]],
    sections: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "summary_type": "source_constitution_registry_summary",
            "source_constitution_registry_status": status,
            "source_constitution_mode": SOURCE_CONSTITUTION_MODE,
            "source_constitution_status": SOURCE_CONSTITUTION_STATUS,
            "handoff_status": (
                V6_2_HANDOFF_STATUS
                if status == "pass"
                else BLOCKED_HANDOFF_STATUS
            ),
            "upstream_star_source_entry_candidate_hash_present": (
                upstream_hash_present
            ),
            "upstream_star_source_entry_candidate_version_ready": (
                upstream_version_ready
            ),
            "upstream_star_source_entry_candidate_hash_stable": (
                upstream_hash_stable
            ),
            "upstream_source_constitution_handoff_ready": (
                upstream_handoff_ready
            ),
            "upstream_source_constitution_next_stage_ready": (
                upstream_next_stage_ready
            ),
            "source_constitution_rule_count": len(rules),
            "source_constitution_rules_registered": all(
                rule["rule_status"] == "registered_metadata_only"
                for rule in rules
            ),
            "source_constitution_rules_human_review_required": all(
                rule["human_review_required_for_change"] is True
                for rule in rules
            ),
            "source_constitution_rules_mutation_proposal_required": all(
                rule["source_mutation_proposal_required"] is True
                for rule in rules
            ),
            "source_constitution_rules_direct_mutation_disabled": all(
                rule["direct_mutation_allowed"] is False for rule in rules
            ),
            "source_constitution_rules_autonomous_override_disabled": all(
                rule["autonomous_override_allowed"] is False
                for rule in rules
            ),
            "source_constitution_section_count": len(sections),
            "source_constitution_sections_pass": _items_pass(
                sections,
                "section_status",
                "section_name",
                REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
            ),
            "source_constitution_contract_count": len(contracts),
            "source_constitution_contracts_pass": _items_pass(
                contracts,
                "contract_status",
                "contract_name",
                REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES,
            ),
            "source_constitution_check_count": len(checks),
            "source_constitution_checks_pass": _items_pass(
                checks,
                "check_status",
                "check_name",
                REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES,
            ),
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _rule_from_id(rules: Sequence[Mapping[str, Any]], rule_id: str) -> Mapping[str, Any] | None:
    for rule in rules:
        if rule.get("rule_id") == rule_id:
            return rule
    return None


def _rule_registered(rules: Sequence[Mapping[str, Any]], rule_id: str) -> bool:
    rule = _rule_from_id(rules, rule_id)
    return (
        rule is not None
        and rule.get("rule_status") == "registered_metadata_only"
        and rule.get("required") is True
        and rule.get("human_review_required_for_change") is True
        and rule.get("source_mutation_proposal_required") is True
        and rule.get("direct_mutation_allowed") is False
        and rule.get("autonomous_override_allowed") is False
        and rule.get("self_authorization_allowed") is False
        and rule.get("hidden_execution_allowed") is False
        and rule.get("blocking_reasons") == []
    )


def _section_from_condition(name: str, passed: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "source_constitution_registry_section",
            "section_status": "pass" if passed else "blocked",
            "expected": True,
            "observed": bool(passed),
            "source_constitution_notes": (
                "registered deterministic metadata only"
                if passed
                else "source constitution section is blocked"
            ),
            "blocking_reasons": [] if passed else [f"{name} blocked"],
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _contract_from_condition(name: str, passed: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "source_constitution_registry_contract",
            "expected": True,
            "observed": bool(passed),
            "contract_status": "pass" if passed else "blocked",
            "blocking_reasons": [] if passed else [f"{name} blocked"],
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _check_from_condition(name: str, passed: bool) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "check_name": name,
            "expected": True,
            "observed": bool(passed),
            "check_status": "pass" if passed else "blocked",
            "blocking_reasons": [] if passed else [f"{name} blocked"],
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _unknown_rule(rule_id: str) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    return _detached_json_value(
        {
            "rule_id": rule_id,
            "rule_name": "unknown_source_constitution_rule",
            "rule_category": "unknown",
            "rule_status": "blocked",
            "rule_priority": 0,
            "rule_statement": "Unknown source constitution rule.",
            "required": False,
            "human_review_required_for_change": True,
            "source_mutation_proposal_required": True,
            "direct_mutation_allowed": False,
            "autonomous_override_allowed": False,
            "self_authorization_allowed": False,
            "hidden_execution_allowed": False,
            "memory_graph_mutation_allowed_without_gate": False,
            "external_call_allowed_without_boundary": False,
            "source_rule_mutation_allowed_without_proposal": False,
            "governance_policy_mutation_allowed_without_review": False,
            "audit_bypass_allowed": False,
            "identity_escalation_allowed": False,
            "false_human_approval_allowed": False,
            "personhood_claim_allowed": False,
            "awakening_claim_allowed": False,
            "legal_subject_claim_allowed": False,
            "religious_object_claim_allowed": False,
            "execution_authorization_created": False,
            "ledger_entry_written": False,
            "memory_graph_mutated": False,
            "external_call_performed": False,
            "source_provenance_runtime_created": False,
            "origin_provenance_ledger_created": False,
            "methodology_runtime_created": False,
            "self_evolution_runtime_created": False,
            "blocking_reasons": [f"Unknown source constitution rule: {rule_id}"],
            **COMMON_DISABLED_FLAGS,
            "safety_boundaries": safety_boundaries,
            **safety_boundaries,
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _section_from_condition(name, False)


def _unknown_contract(name: str) -> dict[str, Any]:
    return _contract_from_condition(name, False)


def _unknown_check(name: str) -> dict[str, Any]:
    return _check_from_condition(name, False)


def _source_constitution_registry_hash(result: Mapping[str, Any]) -> str:
    payload = {
        field_name: result[field_name]
        for field_name in _HASH_FIELDS
        if field_name in result
    }
    encoded = json.dumps(
        _detached_json_value(payload),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _upstream_hash(result: Mapping[str, Any]) -> str | None:
    value = result.get("deterministic_star_source_memory_entry_candidate_hash")
    return value if isinstance(value, str) else None


def _upstream_metadata(result: Mapping[str, Any]) -> Mapping[str, Any]:
    metadata = result.get("star_source_entry_metadata")
    return metadata if isinstance(metadata, Mapping) else {}


def _upstream_passes(result: Mapping[str, Any]) -> bool:
    return (
        result.get("star_source_memory_entry_candidate_status") == "pass"
        and _upstream_hash(result) is not None
        and result.get("handoff_status") == UPSTREAM_READY_HANDOFF_STATUS
    )


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _names_match(
    items: Sequence[Mapping[str, Any]],
    key: str,
    expected: Sequence[str],
) -> bool:
    return [item.get(key) for item in items] == list(expected)


def _items_pass(
    items: Sequence[Mapping[str, Any]],
    status_key: str,
    name_key: str,
    expected_names: Sequence[str],
) -> bool:
    return _names_match(items, name_key, expected_names) and all(
        item.get(status_key) == "pass" for item in items
    )


def _rule_context_name(rule_id: str) -> str:
    return f"rule_{rule_id}_registered"


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) else None


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
            raise ValueError("non-finite floats are not supported")
        return value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise TypeError(f"unsupported JSON value: {type(value).__name__}")
