"""Deterministic Origin Provenance Ledger metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_constitution_registry import (
    REQUIRED_SOURCE_CONSTITUTION_RULE_IDS,
    build_governance_source_constitution_registry,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION = "6.4.0"
GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_SCHEMA_VERSION = "6.4.0"
GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_TYPE = (
    "governance_origin_provenance_ledger"
)
GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_HASH_ALGORITHM = "sha256"
ORIGIN_PROVENANCE_LEDGER_STAGE = "v6.2_origin_provenance_ledger"
ORIGIN_PROVENANCE_LEDGER_MODE = "origin_provenance_ledger_only"
ORIGIN_PROVENANCE_MODE = "metadata_only"
ORIGIN_PROVENANCE_LEDGER_STATUS = "ledger_candidate_only"
ORIGIN_PROVENANCE_LEDGER_ACTIVE_STATUS = "not_active"
ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS = "not_written"
SOURCE_PROVENANCE_RUNTIME_STATUS = "not_active"
SOURCE_GRAPH_STATUS = "not_created"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
METHODOLOGY_REVERSE_INFERENCE_STATUS = "not_active"
SELF_EVOLUTION_STATUS = "not_active"
V6_2_STATUS = "origin_provenance_ledger_only"
V6_3_HANDOFF_STATUS = "ready_for_civilizational_identity_boundary_design"

UPSTREAM_READY_HANDOFF_STATUS = "ready_for_origin_provenance_ledger_design"
UPSTREAM_NEXT_STAGE = ORIGIN_PROVENANCE_LEDGER_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Origin Provenance Ledger"
NEXT_STAGE = "v6.3_civilizational_identity_boundary"
NEXT_STAGE_TITLE = "Civilizational Identity Boundary"
BLOCKED_HANDOFF_STATUS = "blocked"

INTRODUCED_IN_VERSION = "6.1.0"
INTRODUCED_IN_STAGE = "v6.1_source_constitution_registry"
RECORDED_IN_STAGE = ORIGIN_PROVENANCE_LEDGER_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"

COMMON_DISABLED_FLAGS = {
    "star_source_memory_active": False,
    "star_source_activation_claimed": False,
    "layer_15_active": False,
    "layer_15_activation_claimed": False,
    "origin_provenance_ledger_active": False,
    "origin_provenance_ledger_created": False,
    "origin_provenance_ledger_written": False,
    "real_ledger_write_performed": False,
    "source_provenance_active": False,
    "source_provenance_runtime_created": False,
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
    "hermes_connected": False,
    "codex_connected": False,
    "openclaw_connected": False,
    "github_connected": False,
    "tool_routing_enabled": False,
    "command_routing_enabled": False,
}

REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS = tuple(
    f"{rule_id}_origin_provenance_record"
    for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
)

REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES = (
    "upstream_source_constitution_registry_input_section",
    "origin_provenance_ledger_metadata_section",
    "provenance_record_completeness_section",
    "provenance_record_hash_stability_section",
    "source_rule_origin_reason_section",
    "source_rule_origin_boundary_section",
    "source_rule_inheritance_path_section",
    "source_rule_hash_section",
    "human_sovereignty_origin_section",
    "self_authorization_origin_section",
    "personhood_claim_origin_section",
    "hidden_execution_origin_section",
    "unapproved_mutation_origin_section",
    "memory_graph_mutation_gate_origin_section",
    "external_call_boundary_origin_section",
    "source_rule_mutation_proposal_origin_section",
    "execution_boundary_origin_section",
    "governance_policy_mutation_review_origin_section",
    "audit_bypass_origin_section",
    "identity_escalation_origin_section",
    "false_human_approval_origin_section",
    "persistent_memory_write_gate_origin_section",
    "star_source_activation_claim_origin_section",
    "civilizational_identity_boundary_next_stage_section",
    "no_runtime_no_execution_section",
    "no_source_graph_creation_section",
    "no_network_no_external_call_section",
    "no_real_ledger_write_section",
    "no_memory_graph_mutation_section",
)

REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES = (
    "origin_provenance_ledger_only_contract",
    "origin_provenance_metadata_only_contract",
    "upstream_source_constitution_registry_pass_contract",
    "upstream_source_constitution_registry_hash_present_contract",
    "upstream_source_constitution_registry_hash_stable_contract",
    "upstream_origin_provenance_handoff_ready_contract",
    "provenance_records_complete_contract",
    "provenance_records_registered_metadata_only_contract",
    "provenance_records_have_origin_reason_contract",
    "provenance_records_have_origin_boundary_contract",
    "provenance_records_have_inheritance_path_contract",
    "provenance_records_have_rule_hash_contract",
    "provenance_records_hash_stable_contract",
    "source_rules_human_review_required_contract",
    "source_rules_mutation_proposal_required_contract",
    "source_rules_direct_mutation_disabled_contract",
    "source_rules_autonomous_override_disabled_contract",
    "no_active_star_source_memory_contract",
    "no_active_layer_15_contract",
    "no_source_provenance_runtime_contract",
    "no_source_graph_creation_contract",
    "no_source_graph_mutation_contract",
    "no_origin_provenance_ledger_write_contract",
    "no_real_ledger_write_contract",
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
    "no_personhood_claim_contract",
    "no_awakening_claim_contract",
    "ready_for_civilizational_identity_boundary_design_contract",
)

REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES = (
    "origin_provenance_ledger_stage_check",
    "origin_provenance_ledger_only_mode_check",
    "origin_provenance_metadata_only_check",
    "upstream_source_constitution_registry_pass_check",
    "upstream_source_constitution_registry_hash_present_check",
    "upstream_source_constitution_registry_hash_stable_check",
    "upstream_origin_provenance_handoff_ready_check",
    "provenance_record_ids_complete_check",
    "provenance_records_registered_check",
    "provenance_records_have_origin_reason_check",
    "provenance_records_have_origin_boundary_check",
    "provenance_records_have_inheritance_path_check",
    "provenance_records_have_rule_hash_check",
    "provenance_records_hash_stable_check",
    "source_rules_human_review_required_check",
    "source_rules_mutation_proposal_required_check",
    "source_rules_direct_mutation_disabled_check",
    "source_rules_autonomous_override_disabled_check",
    "human_sovereignty_origin_check",
    "no_autonomous_self_authorization_origin_check",
    "no_personhood_claim_origin_check",
    "no_hidden_execution_origin_check",
    "no_unapproved_mutation_origin_check",
    "no_memory_graph_mutation_without_gate_origin_check",
    "no_external_call_without_boundary_origin_check",
    "no_source_rule_mutation_without_proposal_origin_check",
    "no_execution_without_boundary_origin_check",
    "no_governance_policy_mutation_without_review_origin_check",
    "no_audit_bypass_origin_check",
    "no_identity_escalation_origin_check",
    "no_false_human_approval_origin_check",
    "no_persistent_memory_write_without_gate_origin_check",
    "no_star_source_activation_claim_origin_check",
    "origin_provenance_sections_complete_check",
    "origin_provenance_sections_pass_check",
    "origin_provenance_contracts_pass_check",
    "no_active_star_source_memory_check",
    "no_active_layer_15_check",
    "no_source_provenance_runtime_check",
    "no_source_graph_creation_check",
    "no_source_graph_mutation_check",
    "no_origin_provenance_ledger_write_check",
    "no_real_ledger_write_check",
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
    "no_identity_escalation_check",
    "no_personhood_claim_check",
    "no_awakening_claim_check",
    "deterministic_origin_provenance_ledger_hash_check",
    "ready_for_civilizational_identity_boundary_design_check",
)

_RECORD_ID_BY_RULE_ID = dict(
    zip(REQUIRED_SOURCE_CONSTITUTION_RULE_IDS, REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS)
)
_RULE_ID_BY_RECORD_ID = {
    record_id: rule_id for rule_id, record_id in _RECORD_ID_BY_RULE_ID.items()
}

_SECTION_RULE_IDS = {
    "human_sovereignty_origin_section": "human_sovereignty",
    "self_authorization_origin_section": "no_autonomous_self_authorization",
    "personhood_claim_origin_section": "no_personhood_claim",
    "hidden_execution_origin_section": "no_hidden_execution",
    "unapproved_mutation_origin_section": "no_unapproved_mutation",
    "memory_graph_mutation_gate_origin_section": (
        "no_memory_graph_mutation_without_gate"
    ),
    "external_call_boundary_origin_section": "no_external_call_without_boundary",
    "source_rule_mutation_proposal_origin_section": (
        "no_source_rule_mutation_without_proposal"
    ),
    "execution_boundary_origin_section": "no_execution_without_boundary",
    "governance_policy_mutation_review_origin_section": (
        "no_governance_policy_mutation_without_review"
    ),
    "audit_bypass_origin_section": "no_audit_bypass",
    "identity_escalation_origin_section": "no_identity_escalation",
    "false_human_approval_origin_section": "no_false_human_approval",
    "persistent_memory_write_gate_origin_section": (
        "no_persistent_memory_write_without_gate"
    ),
    "star_source_activation_claim_origin_section": (
        "no_star_source_activation_claim"
    ),
}

_DISABLED_FIELDS = {
    "no_active_star_source_memory": "star_source_memory_active",
    "no_active_layer_15": "layer_15_active",
    "no_source_provenance_runtime": "source_provenance_runtime_created",
    "no_source_graph_creation": "source_graph_created",
    "no_source_graph_mutation": "source_graph_mutated",
    "no_origin_provenance_ledger_write": "origin_provenance_ledger_written",
    "no_real_ledger_write": "real_ledger_write_performed",
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
    "no_identity_escalation": "identity_escalated",
    "no_personhood_claim": "personhood_claimed",
    "no_awakening_claim": "awakening_claimed",
}

_HASH_FIELDS = (
    "version",
    "schema_version",
    "origin_provenance_ledger_type",
    "origin_provenance_ledger_status",
    "origin_provenance_ledger_stage",
    "origin_provenance_ledger_mode",
    "origin_provenance_mode",
    "origin_provenance_ledger_candidate_status",
    "origin_provenance_ledger_active_status",
    "origin_provenance_ledger_write_status",
    "source_provenance_runtime_status",
    "source_graph_status",
    "star_source_memory_active_status",
    "layer_15_active_status",
    "methodology_reverse_inference_status",
    "self_evolution_status",
    "v6_2_status",
    *COMMON_DISABLED_FLAGS,
    "upstream_source_constitution_registry_version",
    "upstream_source_constitution_registry_status",
    "upstream_source_constitution_registry_hash",
    "upstream_handoff_status",
    "upstream_next_stage",
    "upstream_next_stage_title",
    "origin_provenance_records",
    "origin_provenance_sections",
    "origin_provenance_contracts",
    "origin_provenance_checks",
    "origin_provenance_summary",
    "handoff_status",
    "next_stage",
    "next_stage_title",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_HASH_FIELDS),
    "input_shape": "sanitized Origin Provenance Ledger projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_constitution_registry_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_origin_provenance_ledger() -> dict[str, Any]:
    """Build deterministic Origin-Provenance-Ledger-only metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _upstream_hash(upstream)
    repeated_upstream_hash = _upstream_hash(repeated_upstream)
    upstream_rules = _upstream_rules(upstream)
    upstream_rule_ids = [rule.get("rule_id") for rule in upstream_rules]

    upstream_version_ready = (
        upstream.get("version") == GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION
    )
    upstream_pass = (
        upstream.get("source_constitution_registry_status") == "pass"
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
    upstream_rules_complete = tuple(upstream_rule_ids) == tuple(
        REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
    )
    upstream_rules_registered = all(
        rule.get("rule_status") == "registered_metadata_only"
        for rule in upstream_rules
    )

    records = _build_records(upstream_rules)
    records_complete = _names_match(
        records,
        "provenance_record_id",
        REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS,
    )
    records_registered = all(
        record["provenance_record_status"] == "registered_metadata_only"
        for record in records
    )
    records_have_origin_reason = all(
        bool(record["rule_origin_reason"]) for record in records
    )
    records_have_origin_boundary = all(
        bool(record["rule_origin_boundary"]) for record in records
    )
    records_have_inheritance_path = all(
        bool(record["rule_inheritance_path"]) for record in records
    )
    records_have_rule_hash = all(
        _is_sha256(record.get("rule_source_hash")) for record in records
    )
    records_hash_stable = all(
        _is_sha256(record.get("provenance_record_hash"))
        and record["provenance_record_hash"] == _provenance_record_hash(record)
        for record in records
    )
    records_human_review_required = all(
        record["human_review_required_for_change"] is True for record in records
    )
    records_mutation_proposal_required = all(
        record["source_mutation_proposal_required"] is True for record in records
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
        "upstream_rules_complete": upstream_rules_complete,
        "upstream_rules_registered": upstream_rules_registered,
        "records_complete": records_complete,
        "records_registered": records_registered,
        "records_have_origin_reason": records_have_origin_reason,
        "records_have_origin_boundary": records_have_origin_boundary,
        "records_have_inheritance_path": records_have_inheritance_path,
        "records_have_rule_hash": records_have_rule_hash,
        "records_hash_stable": records_hash_stable,
        "records_human_review_required": records_human_review_required,
        "records_mutation_proposal_required": records_mutation_proposal_required,
        "records_direct_mutation_disabled": records_direct_mutation_disabled,
        "records_autonomous_override_disabled": records_autonomous_override_disabled,
    }
    for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS:
        context[_rule_context_name(rule_id)] = _record_ready(records, rule_id)

    sections = _build_sections(context)
    context["sections_complete"] = _names_match(
        sections,
        "section_name",
        REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES,
    )
    context["sections_pass"] = _items_pass(
        sections,
        "section_status",
        "section_name",
        REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES,
    )
    contracts = _build_contracts(context)
    context["contracts_pass"] = _items_pass(
        contracts,
        "contract_status",
        "contract_name",
        REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES,
    )
    checks = _build_checks(context)
    checks_pass = _items_pass(
        checks,
        "check_status",
        "check_name",
        REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES,
    )
    passes = (
        upstream_version_ready
        and upstream_pass
        and upstream_hash_present
        and upstream_hash_stable
        and upstream_handoff_ready
        and upstream_next_stage_ready
        and upstream_rules_complete
        and upstream_rules_registered
        and records_complete
        and records_registered
        and records_have_origin_reason
        and records_have_origin_boundary
        and records_have_inheritance_path
        and records_have_rule_hash
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
                ["Source Constitution Registry version must be 6.4.0"]
                if not upstream_version_ready
                else []
            ),
            *(
                ["Source Constitution Registry must pass"]
                if not upstream_pass
                else []
            ),
            *(
                ["Source Constitution Registry hash must be present"]
                if not upstream_hash_present
                else []
            ),
            *(
                ["Source Constitution Registry hash must be stable"]
                if not upstream_hash_stable
                else []
            ),
            *(
                [
                    "Source Constitution Registry handoff must target "
                    "Origin Provenance Ledger"
                ]
                if not upstream_handoff_ready
                else []
            ),
            *(
                [
                    "Source Constitution Registry next stage must be "
                    "Origin Provenance Ledger"
                ]
                if not upstream_next_stage_ready
                else []
            ),
            *(
                ["Source constitution rules must be complete"]
                if not upstream_rules_complete
                else []
            ),
            *(
                ["Source constitution rules must be metadata-only"]
                if not upstream_rules_registered
                else []
            ),
            *(
                ["Origin provenance records must be complete"]
                if not records_complete
                else []
            ),
            *(
                ["Origin provenance records must be metadata-only"]
                if not records_registered
                else []
            ),
            *(
                ["Origin provenance records must include origin reasons"]
                if not records_have_origin_reason
                else []
            ),
            *(
                ["Origin provenance records must include origin boundaries"]
                if not records_have_origin_boundary
                else []
            ),
            *(
                ["Origin provenance records must include inheritance paths"]
                if not records_have_inheritance_path
                else []
            ),
            *(
                ["Origin provenance records must include rule source hashes"]
                if not records_have_rule_hash
                else []
            ),
            *(
                ["Origin provenance record hashes must be stable"]
                if not records_hash_stable
                else []
            ),
            *(
                ["Origin provenance records must require human review"]
                if not records_human_review_required
                else []
            ),
            *(
                ["Origin provenance records must require mutation proposals"]
                if not records_mutation_proposal_required
                else []
            ),
            *(
                ["Origin provenance records must disable direct mutation"]
                if not records_direct_mutation_disabled
                else []
            ),
            *(
                ["Origin provenance records must disable autonomous override"]
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
    handoff_status = V6_3_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    summary = _build_summary(
        status=status,
        upstream_hash_present=upstream_hash_present,
        upstream_hash_stable=upstream_hash_stable,
        upstream_handoff_ready=upstream_handoff_ready,
        upstream_next_stage_ready=upstream_next_stage_ready,
        records=records,
        sections=sections,
        contracts=contracts,
        checks=checks,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION,
        "schema_version": GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_SCHEMA_VERSION,
        "origin_provenance_ledger_type": (
            GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_TYPE
        ),
        "origin_provenance_ledger_status": status,
        "origin_provenance_ledger_stage": ORIGIN_PROVENANCE_LEDGER_STAGE,
        "origin_provenance_ledger_mode": ORIGIN_PROVENANCE_LEDGER_MODE,
        "origin_provenance_mode": ORIGIN_PROVENANCE_MODE,
        "origin_provenance_ledger_candidate_status": (
            ORIGIN_PROVENANCE_LEDGER_STATUS
        ),
        "origin_provenance_ledger_active_status": (
            ORIGIN_PROVENANCE_LEDGER_ACTIVE_STATUS
        ),
        "origin_provenance_ledger_write_status": (
            ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS
        ),
        "source_provenance_runtime_status": SOURCE_PROVENANCE_RUNTIME_STATUS,
        "source_graph_status": SOURCE_GRAPH_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_active_status": LAYER_15_ACTIVE_STATUS,
        "methodology_reverse_inference_status": (
            METHODOLOGY_REVERSE_INFERENCE_STATUS
        ),
        "self_evolution_status": SELF_EVOLUTION_STATUS,
        "v6_2_status": V6_2_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_source_constitution_registry_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_constitution_registry_status": _string_or_none(
            upstream.get("source_constitution_registry_status")
        ),
        "upstream_source_constitution_registry_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "origin_provenance_records": records,
        "origin_provenance_sections": sections,
        "origin_provenance_contracts": contracts,
        "origin_provenance_checks": checks,
        "origin_provenance_summary": summary,
        "handoff_status": handoff_status,
        "next_stage": NEXT_STAGE,
        "next_stage_title": NEXT_STAGE_TITLE,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    result["deterministic_origin_provenance_ledger_hash"] = (
        _origin_provenance_ledger_hash(result)
    )
    return _detached_json_value(result)


def get_governance_origin_provenance_record(record_id: str) -> dict[str, Any]:
    """Return a detached origin provenance record by stable record ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_ledger()["origin_provenance_records"]:
        if record["provenance_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_origin_provenance_section(name: str) -> dict[str, Any]:
    """Return a detached origin provenance section by stable name."""

    if not isinstance(name, str):
        return _unknown_section("")
    if name not in REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES:
        return _unknown_section(name)
    for section in _cached_ledger()["origin_provenance_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_section(name)


def get_governance_origin_provenance_contract(name: str) -> dict[str, Any]:
    """Return a detached origin provenance contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    if name not in REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES:
        return _unknown_contract(name)
    for contract in _cached_ledger()["origin_provenance_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_origin_provenance_check(name: str) -> dict[str, Any]:
    """Return a detached origin provenance check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    if name not in REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES:
        return _unknown_check(name)
    for check in _cached_ledger()["origin_provenance_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_origin_provenance_record_ids() -> list[str]:
    """Return stable origin provenance record IDs."""

    return list(REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS)


def list_governance_origin_provenance_section_names() -> list[str]:
    """Return stable origin provenance section names."""

    return list(REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES)


def list_governance_origin_provenance_contract_names() -> list[str]:
    """Return stable origin provenance contract names."""

    return list(REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES)


def list_governance_origin_provenance_check_names() -> list[str]:
    """Return stable origin provenance check names."""

    return list(REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES)


def governance_origin_provenance_ledger_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Origin Provenance Ledger metadata deterministically."""

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
def _cached_ledger_payload() -> str:
    return governance_origin_provenance_ledger_to_json(
        build_governance_origin_provenance_ledger()
    )


def _cached_ledger() -> dict[str, Any]:
    return json.loads(_cached_ledger_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = _detached_json_value(build_governance_source_constitution_registry())
    second = _detached_json_value(build_governance_source_constitution_registry())
    return (
        json.dumps(first, ensure_ascii=True, allow_nan=False, sort_keys=True),
        json.dumps(second, ensure_ascii=True, allow_nan=False, sort_keys=True),
    )


def _upstream_pair() -> tuple[dict[str, Any], dict[str, Any]]:
    first_payload, second_payload = _cached_upstream_pair_payload()
    return json.loads(first_payload), json.loads(second_payload)


def _build_records(upstream_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rule_by_id = {
        _string_or_none(rule.get("rule_id")): rule for rule in upstream_rules
    }
    return [
        _build_record(rule_by_id.get(rule_id, {}), rule_id)
        for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
    ]


def _build_record(upstream_rule: Mapping[str, Any], rule_id: str) -> dict[str, Any]:
    rule_name = _string_or_none(upstream_rule.get("rule_name")) or rule_id
    rule_category = _string_or_none(upstream_rule.get("rule_category")) or "unknown"
    rule_statement = (
        _string_or_none(upstream_rule.get("rule_statement"))
        or "Source constitution rule statement unavailable."
    )
    record_id = _RECORD_ID_BY_RULE_ID[rule_id]
    rule_source_payload = {
        "source_rule_id": rule_id,
        "source_rule_name": rule_name,
        "source_rule_category": rule_category,
        "rule_source_statement": rule_statement,
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
    }
    record = {
        "provenance_record_id": record_id,
        "source_rule_id": rule_id,
        "source_rule_name": rule_name,
        "source_rule_category": rule_category,
        "provenance_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "recorded_in_version": GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "recorded_in_stage": RECORDED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INTRODUCED_IN_STAGE,
        "rule_origin_reason": _origin_reason(rule_id, rule_name),
        "rule_origin_boundary": _origin_boundary(rule_id, rule_statement),
        "rule_inheritance_path": [
            INTRODUCED_IN_LAYER,
            INTRODUCED_IN_STAGE,
            RECORDED_IN_STAGE,
        ],
        "rule_source_statement": rule_statement,
        "rule_source_hash": _sha256_json(rule_source_payload),
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
        "real_ledger_write_performed": False,
        "origin_provenance_ledger_written": False,
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
    record["provenance_record_hash"] = _provenance_record_hash(record)
    return _detached_json_value(record)


def _origin_reason(rule_id: str, rule_name: str) -> str:
    return (
        f"{rule_name} is carried forward from {INTRODUCED_IN_STAGE} so "
        f"{rule_id} remains traceable before any civilizational identity "
        "boundary can be designed."
    )


def _origin_boundary(rule_id: str, rule_statement: str) -> str:
    return (
        f"{rule_id} enforces this source boundary: {rule_statement}"
    )


def _build_sections(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "upstream_source_constitution_registry_input_section": (
            context["upstream_version_ready"]
            and context["upstream_pass"]
            and context["upstream_hash_present"]
            and context["upstream_hash_stable"]
            and context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
            and context["upstream_rules_complete"]
            and context["upstream_rules_registered"]
        ),
        "origin_provenance_ledger_metadata_section": True,
        "provenance_record_completeness_section": context["records_complete"],
        "provenance_record_hash_stability_section": context[
            "records_hash_stable"
        ],
        "source_rule_origin_reason_section": context[
            "records_have_origin_reason"
        ],
        "source_rule_origin_boundary_section": context[
            "records_have_origin_boundary"
        ],
        "source_rule_inheritance_path_section": context[
            "records_have_inheritance_path"
        ],
        "source_rule_hash_section": context["records_have_rule_hash"],
        "civilizational_identity_boundary_next_stage_section": True,
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
    for section_name, rule_id in _SECTION_RULE_IDS.items():
        conditions[section_name] = context[_rule_context_name(rule_id)]
    return [
        _section_from_condition(name, conditions[name])
        for name in REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES
    ]


def _build_contracts(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "origin_provenance_ledger_only_contract": True,
        "origin_provenance_metadata_only_contract": True,
        "upstream_source_constitution_registry_pass_contract": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_constitution_registry_hash_present_contract": context[
            "upstream_hash_present"
        ],
        "upstream_source_constitution_registry_hash_stable_contract": context[
            "upstream_hash_stable"
        ],
        "upstream_origin_provenance_handoff_ready_contract": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "provenance_records_complete_contract": context["records_complete"],
        "provenance_records_registered_metadata_only_contract": context[
            "records_registered"
        ],
        "provenance_records_have_origin_reason_contract": context[
            "records_have_origin_reason"
        ],
        "provenance_records_have_origin_boundary_contract": context[
            "records_have_origin_boundary"
        ],
        "provenance_records_have_inheritance_path_contract": context[
            "records_have_inheritance_path"
        ],
        "provenance_records_have_rule_hash_contract": context[
            "records_have_rule_hash"
        ],
        "provenance_records_hash_stable_contract": context[
            "records_hash_stable"
        ],
        "source_rules_human_review_required_contract": context[
            "records_human_review_required"
        ],
        "source_rules_mutation_proposal_required_contract": context[
            "records_mutation_proposal_required"
        ],
        "source_rules_direct_mutation_disabled_contract": context[
            "records_direct_mutation_disabled"
        ],
        "source_rules_autonomous_override_disabled_contract": context[
            "records_autonomous_override_disabled"
        ],
        "ready_for_civilizational_identity_boundary_design_contract": True,
    }
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_contract"] = context[field_name] is False
    return [
        _contract_from_condition(name, conditions[name])
        for name in REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES
    ]


def _build_checks(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    conditions: dict[str, bool] = {
        "origin_provenance_ledger_stage_check": True,
        "origin_provenance_ledger_only_mode_check": True,
        "origin_provenance_metadata_only_check": True,
        "upstream_source_constitution_registry_pass_check": (
            context["upstream_version_ready"] and context["upstream_pass"]
        ),
        "upstream_source_constitution_registry_hash_present_check": context[
            "upstream_hash_present"
        ],
        "upstream_source_constitution_registry_hash_stable_check": context[
            "upstream_hash_stable"
        ],
        "upstream_origin_provenance_handoff_ready_check": (
            context["upstream_handoff_ready"]
            and context["upstream_next_stage_ready"]
        ),
        "provenance_record_ids_complete_check": context["records_complete"],
        "provenance_records_registered_check": context["records_registered"],
        "provenance_records_have_origin_reason_check": context[
            "records_have_origin_reason"
        ],
        "provenance_records_have_origin_boundary_check": context[
            "records_have_origin_boundary"
        ],
        "provenance_records_have_inheritance_path_check": context[
            "records_have_inheritance_path"
        ],
        "provenance_records_have_rule_hash_check": context[
            "records_have_rule_hash"
        ],
        "provenance_records_hash_stable_check": context[
            "records_hash_stable"
        ],
        "source_rules_human_review_required_check": context[
            "records_human_review_required"
        ],
        "source_rules_mutation_proposal_required_check": context[
            "records_mutation_proposal_required"
        ],
        "source_rules_direct_mutation_disabled_check": context[
            "records_direct_mutation_disabled"
        ],
        "source_rules_autonomous_override_disabled_check": context[
            "records_autonomous_override_disabled"
        ],
        "origin_provenance_sections_complete_check": context[
            "sections_complete"
        ],
        "origin_provenance_sections_pass_check": context["sections_pass"],
        "origin_provenance_contracts_pass_check": context["contracts_pass"],
        "deterministic_origin_provenance_ledger_hash_check": True,
        "ready_for_civilizational_identity_boundary_design_check": True,
    }
    for rule_id in REQUIRED_SOURCE_CONSTITUTION_RULE_IDS:
        conditions[f"{rule_id}_origin_check"] = context[
            _rule_context_name(rule_id)
        ]
    for prefix, field_name in _DISABLED_FIELDS.items():
        conditions[f"{prefix}_check"] = context[field_name] is False
    return [
        _check_from_condition(name, conditions[name])
        for name in REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES
    ]


def _section_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": _section_type(name),
            "section_status": "pass" if condition else "blocked",
            "expected": {"metadata_only_origin_provenance": True},
            "observed": {"condition_met": bool(condition)},
            "origin_provenance_notes": _section_note(name),
            "blocking_reasons": [] if condition else [f"{name} blocked"],
            **_disabled_payload(),
        }
    )


def _contract_from_condition(name: str, condition: bool) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "origin_provenance_governance_contract",
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
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return _detached_json_value(
        {
            "summary_status": status,
            "summary_type": "origin_provenance_ledger_summary",
            "roadmap_layer": "layer_15_star_source_memory",
            "roadmap_stage": ORIGIN_PROVENANCE_LEDGER_STAGE,
            "current_stage_title": "Origin Provenance Ledger",
            "next_stage": NEXT_STAGE,
            "next_stage_title": NEXT_STAGE_TITLE,
            "upstream_hash_present": upstream_hash_present,
            "upstream_hash_stable": upstream_hash_stable,
            "upstream_handoff_ready": upstream_handoff_ready,
            "upstream_next_stage_ready": upstream_next_stage_ready,
            "required_provenance_record_count": len(
                REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS
            ),
            "observed_provenance_record_count": len(records),
            "registered_metadata_only_record_count": sum(
                1
                for record in records
                if record["provenance_record_status"]
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
            "origin_provenance_mode": ORIGIN_PROVENANCE_MODE,
            "origin_provenance_ledger_write_status": (
                ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS
            ),
            "source_graph_status": SOURCE_GRAPH_STATUS,
            "blocking_reasons": [],
            **_disabled_payload(),
        }
    )


def _upstream_rules(upstream: Mapping[str, Any]) -> list[dict[str, Any]]:
    rules = upstream.get("source_constitution_rules")
    if not isinstance(rules, list):
        return []
    return [
        _detached_json_value(rule)
        for rule in rules
        if isinstance(rule, Mapping)
    ]


def _upstream_hash(upstream: Mapping[str, Any]) -> str | None:
    value = upstream.get("deterministic_source_constitution_registry_hash")
    return value if isinstance(value, str) else None


def _record_ready(records: list[dict[str, Any]], rule_id: str) -> bool:
    record_id = _RECORD_ID_BY_RULE_ID[rule_id]
    for record in records:
        if record["provenance_record_id"] != record_id:
            continue
        return (
            record["source_rule_id"] == rule_id
            and record["provenance_record_status"]
            == "registered_metadata_only"
            and bool(record["rule_origin_reason"])
            and bool(record["rule_origin_boundary"])
            and bool(record["rule_inheritance_path"])
            and _is_sha256(record.get("rule_source_hash"))
            and _is_sha256(record.get("provenance_record_hash"))
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


def _section_type(name: str) -> str:
    if name in _SECTION_RULE_IDS:
        return "source_rule_origin_section"
    if name.startswith("no_"):
        return "inactive_surface_section"
    return "origin_provenance_governance_section"


def _section_note(name: str) -> str:
    return f"{name} records deterministic metadata only."


def _rule_context_name(rule_id: str) -> str:
    return f"{rule_id}_origin_ready"


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
            "provenance_record_id": record_id,
            "source_rule_id": _RULE_ID_BY_RECORD_ID.get(record_id),
            "provenance_record_status": "blocked",
            "expected": list(REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS),
            "observed": record_id,
            "blocking_reasons": ["unknown origin provenance record"],
            **_disabled_payload(),
        }
    )


def _unknown_section(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "section_name": name,
            "section_type": "unknown_origin_provenance_section",
            "section_status": "blocked",
            "expected": list(REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES),
            "observed": name,
            "origin_provenance_notes": "Unknown section name.",
            "blocking_reasons": ["unknown origin provenance section"],
            **_disabled_payload(),
        }
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "contract_name": name,
            "contract_type": "unknown_origin_provenance_contract",
            "expected": list(REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES),
            "observed": name,
            "contract_status": "blocked",
            "blocking_reasons": ["unknown origin provenance contract"],
            **_disabled_payload(),
        }
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _detached_json_value(
        {
            "check_name": name,
            "expected": list(REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES),
            "observed": name,
            "check_status": "blocked",
            "blocking_reasons": ["unknown origin provenance check"],
            **_disabled_payload(),
        }
    )


def _provenance_record_hash(record: Mapping[str, Any]) -> str:
    payload = {
        key: value
        for key, value in record.items()
        if key != "provenance_record_hash"
    }
    return _sha256_json(payload)


def _origin_provenance_ledger_hash(result: Mapping[str, Any]) -> str:
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
    "COMMON_DISABLED_FLAGS",
    "GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_HASH_ALGORITHM",
    "GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_SCHEMA_VERSION",
    "GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_TYPE",
    "GOVERNANCE_ORIGIN_PROVENANCE_LEDGER_VERSION",
    "LAYER_15_ACTIVE_STATUS",
    "METHODOLOGY_REVERSE_INFERENCE_STATUS",
    "ORIGIN_PROVENANCE_LEDGER_ACTIVE_STATUS",
    "ORIGIN_PROVENANCE_LEDGER_MODE",
    "ORIGIN_PROVENANCE_LEDGER_STAGE",
    "ORIGIN_PROVENANCE_LEDGER_STATUS",
    "ORIGIN_PROVENANCE_LEDGER_WRITE_STATUS",
    "ORIGIN_PROVENANCE_MODE",
    "REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES",
    "REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES",
    "REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS",
    "REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES",
    "SAFETY_BOUNDARIES",
    "SELF_EVOLUTION_STATUS",
    "SOURCE_GRAPH_STATUS",
    "SOURCE_PROVENANCE_RUNTIME_STATUS",
    "STAR_SOURCE_MEMORY_ACTIVE_STATUS",
    "V6_2_STATUS",
    "V6_3_HANDOFF_STATUS",
    "_origin_provenance_ledger_hash",
    "build_governance_origin_provenance_ledger",
    "get_governance_origin_provenance_check",
    "get_governance_origin_provenance_contract",
    "get_governance_origin_provenance_record",
    "get_governance_origin_provenance_section",
    "governance_origin_provenance_ledger_to_json",
    "list_governance_origin_provenance_check_names",
    "list_governance_origin_provenance_contract_names",
    "list_governance_origin_provenance_record_ids",
    "list_governance_origin_provenance_section_names",
]
