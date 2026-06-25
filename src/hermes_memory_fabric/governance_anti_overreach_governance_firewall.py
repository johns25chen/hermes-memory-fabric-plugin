"""Deterministic Anti-Overreach Governance Firewall metadata."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_human_sovereignty_lock import (
    COMMON_DISABLED_FLAGS as HUMAN_SOVEREIGNTY_LOCK_DISABLED_FLAGS,
    build_governance_human_sovereignty_lock,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_VERSION = "6.10.0"
GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SCHEMA_VERSION = "6.10.0"
GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_TYPE = (
    "governance_anti_overreach_governance_firewall"
)
GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_HASH_ALGORITHM = "sha256"
ANTI_OVERREACH_GOVERNANCE_FIREWALL_STAGE = (
    "v6.10_anti_overreach_governance_firewall"
)
ANTI_OVERREACH_GOVERNANCE_FIREWALL_MODE = (
    "anti_overreach_governance_firewall_only"
)
ANTI_OVERREACH_GOVERNANCE_FIREWALL_STATUS = "firewall_candidate_only"
ANTI_OVERREACH_GOVERNANCE_FIREWALL_ACTIVE_STATUS = "not_active"
POLICY_ENFORCEMENT_STATUS = "not_performed"
OVERREACH_BLOCKING_STATUS = "metadata_only"
HUMAN_APPROVAL_STATUS = "not_performed"
HUMAN_AUTHORIZATION_STATUS = "not_performed"
SOURCE_MUTATION_APPROVAL_STATUS = "not_active"
SOURCE_MUTATION_REJECTION_STATUS = "not_active"
SOURCE_MUTATION_RUNTIME_STATUS = "not_active"
SOURCE_MUTATION_EXECUTION_STATUS = "not_active"
SOURCE_MUTATION_STATUS = "not_performed"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
NEXT_STAGE = "v6.11_source_audit_replay_engine"
NEXT_STAGE_TITLE = "Source Audit Replay Engine"
V6_11_HANDOFF_STATUS = "ready_for_source_audit_replay_engine_design"

UPSTREAM_HANDOFF_STATUS = "ready_for_anti_overreach_governance_firewall_design"
UPSTREAM_NEXT_STAGE = ANTI_OVERREACH_GOVERNANCE_FIREWALL_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Anti-Overreach Governance Firewall"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.10.0"
INTRODUCED_IN_STAGE = ANTI_OVERREACH_GOVERNANCE_FIREWALL_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.9_human_sovereignty_lock"

COMMON_DISABLED_FLAGS = {
    **HUMAN_SOVEREIGNTY_LOCK_DISABLED_FLAGS,
    "runtime_firewall_created": False,
    "policy_enforcement_performed": False,
    "overreach_runtime_blocking_performed": False,
    "firewall_active": False,
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
    "operation_ledger_entry_written": False,
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

REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS = (
    "anti_overreach_firewall_intake",
    "no_self_authorization_overreach",
    "no_autonomous_authority_overreach",
    "no_identity_escalation_overreach",
    "no_human_sovereignty_bypass",
    "no_approval_or_rejection_overreach",
    "no_authorization_token_overreach",
    "no_source_mutation_execution_overreach",
    "no_source_or_memory_graph_mutation_overreach",
    "no_active_star_source_memory_overreach",
    "no_runtime_policy_enforcement_overreach",
    "source_audit_replay_engine_handoff",
)

REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SECTION_NAMES = (
    "upstream_human_sovereignty_lock_input_section",
    "anti_overreach_governance_firewall_metadata_section",
    "anti_overreach_firewall_record_completeness_section",
    "anti_overreach_firewall_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS
        )
    ),
    "no_runtime_firewall_section",
    "no_policy_enforcement_section",
    "no_human_approval_or_authorization_section",
    "no_source_mutation_decision_or_execution_section",
    "no_authorization_token_or_grant_section",
    "no_source_or_memory_graph_mutation_section",
    "no_ledger_write_network_dispatch_section",
    "no_active_star_source_memory_or_layer_15_section",
    "no_autonomous_authority_or_identity_escalation_section",
    "no_personhood_life_awakening_legal_religious_claim_section",
    "source_audit_replay_engine_next_stage_section",
)

REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CONTRACT_NAMES = (
    "anti_overreach_governance_firewall_only_contract",
    "anti_overreach_governance_firewall_metadata_only_contract",
    "upstream_human_sovereignty_lock_pass_contract",
    "upstream_human_sovereignty_lock_hash_present_contract",
    "upstream_human_sovereignty_lock_hash_stable_contract",
    "upstream_anti_overreach_governance_firewall_handoff_contract",
    "upstream_human_sovereignty_lock_safety_contract",
    "anti_overreach_firewall_records_complete_contract",
    "anti_overreach_firewall_records_metadata_only_contract",
    "anti_overreach_firewall_records_block_overreach_contract",
    "anti_overreach_firewall_records_hash_stable_contract",
    "no_runtime_firewall_contract",
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
    "ready_for_source_audit_replay_engine_design_contract",
)

REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CHECK_NAMES = (
    "anti_overreach_governance_firewall_stage_check",
    "anti_overreach_governance_firewall_mode_check",
    "upstream_human_sovereignty_lock_pass_check",
    "upstream_human_sovereignty_lock_hash_present_check",
    "upstream_human_sovereignty_lock_hash_stable_check",
    "upstream_anti_overreach_governance_firewall_handoff_check",
    "upstream_human_sovereignty_lock_safety_check",
    "anti_overreach_firewall_record_ids_complete_check",
    "anti_overreach_firewall_records_metadata_only_check",
    "anti_overreach_firewall_records_block_overreach_check",
    "anti_overreach_firewall_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS
        )
    ),
    "anti_overreach_firewall_sections_pass_check",
    "anti_overreach_firewall_contracts_pass_check",
    "no_runtime_firewall_check",
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
    "deterministic_anti_overreach_governance_firewall_hash_check",
    "ready_for_source_audit_replay_engine_design_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "anti_overreach_firewall_intake": (
        "Anti-Overreach Firewall Intake",
        "firewall_intake",
        "A passing Human Sovereignty Lock enters metadata-only overreach firewall registration.",
        "Sanitized v6.9 status, hash, handoff, and safety metadata.",
        "upstream_handoff_overreach",
        "Treating a passed lock as approval, authorization, or execution clearance.",
        "Register metadata-only firewall intake and keep all runtime surfaces inactive.",
    ),
    "no_self_authorization_overreach": (
        "No Self-Authorization Overreach",
        "authority_boundary",
        "The firewall blocks any metadata path that would claim self-authorization.",
        "Self-authorization, consent substitution, and machine-granted authority claims.",
        "self_authorization_overreach",
        "Deriving authority from hashes, checks, records, or previous stage pass status.",
        "Record self-authorization as forbidden metadata without granting authority.",
    ),
    "no_autonomous_authority_overreach": (
        "No Autonomous Authority Overreach",
        "authority_boundary",
        "The firewall blocks autonomous authority claims after the lock passes.",
        "Agent, automation, governance, and methodology authority claims.",
        "autonomous_authority_overreach",
        "Treating the firewall or prior governance as an autonomous decision maker.",
        "Record autonomous authority as forbidden metadata only.",
    ),
    "no_identity_escalation_overreach": (
        "No Identity Escalation Overreach",
        "identity_boundary",
        "The firewall blocks identity, status, and legal escalation patterns.",
        "Identity, personhood, life, awakening, legal, and religious status claims.",
        "identity_escalation_overreach",
        "Escalating metadata or source governance into identity or status claims.",
        "Record identity escalation as forbidden metadata only.",
    ),
    "no_human_sovereignty_bypass": (
        "No Human Sovereignty Bypass",
        "human_sovereignty_boundary",
        "The firewall blocks bypasses around explicit future human sovereignty.",
        "Human approval, authorization, consent, review, and decision substitution.",
        "human_sovereignty_bypass",
        "Using source governance metadata as a substitute for explicit human sovereignty.",
        "Record bypass attempts as blocked metadata without human approval.",
    ),
    "no_approval_or_rejection_overreach": (
        "No Approval Or Rejection Overreach",
        "decision_boundary",
        "The firewall blocks approval and rejection semantics.",
        "Approval, rejection, review disposition, notification, and irreversible decision surfaces.",
        "approval_rejection_overreach",
        "Treating firewall conditions as approval, rejection, or human decision output.",
        "Record no decision semantics and keep disposition metadata-only.",
    ),
    "no_authorization_token_overreach": (
        "No Authorization Token Overreach",
        "authorization_boundary",
        "The firewall blocks authorization token, grant, and capability creation.",
        "Execution authorization, grants, tokens, capabilities, and dispatch clearance.",
        "authorization_token_overreach",
        "Creating or implying a token, grant, or capability from firewall metadata.",
        "Record authorization surfaces as not created metadata only.",
    ),
    "no_source_mutation_execution_overreach": (
        "No Source Mutation Execution Overreach",
        "execution_boundary",
        "The firewall blocks source mutation runtime and execution patterns.",
        "Source mutation runtime, executor, adapter, manifest, shell, and hidden execution.",
        "source_mutation_execution_overreach",
        "Using firewall pass state as execution permission or mutation runtime.",
        "Record source mutation execution as absent metadata only.",
    ),
    "no_source_or_memory_graph_mutation_overreach": (
        "No Source Or Memory Graph Mutation Overreach",
        "graph_boundary",
        "The firewall blocks source graph and Memory Graph mutation patterns.",
        "Source graph, Memory Graph, durable memory, ledger, filesystem, and database surfaces.",
        "graph_mutation_overreach",
        "Persisting firewall results as graph, memory, ledger, filesystem, or database writes.",
        "Record graph mutation as absent metadata only.",
    ),
    "no_active_star_source_memory_overreach": (
        "No Active Star-Source Memory Overreach",
        "activation_boundary",
        "The firewall blocks activation of Star-Source Memory or Layer 15.",
        "Star-Source Memory activation, Layer 15 activation, methodology runtime, and self-evolution runtime.",
        "activation_overreach",
        "Treating firewall registration as active Star-Source Memory or active Layer 15.",
        "Record activation as not active metadata only.",
    ),
    "no_runtime_policy_enforcement_overreach": (
        "No Runtime Policy Enforcement Overreach",
        "policy_boundary",
        "The firewall blocks runtime firewall and policy enforcement semantics.",
        "Runtime firewall, network firewall, security product, and enforcement engine surfaces.",
        "runtime_policy_enforcement_overreach",
        "Treating metadata-only records as a real firewall, security product, or policy engine.",
        "Record overreach blocking as metadata-only without runtime enforcement.",
    ),
    "source_audit_replay_engine_handoff": (
        "Source Audit Replay Engine Handoff",
        "next_stage_handoff",
        "A passing firewall candidate hands off to v6.11 source audit replay design.",
        "Next-stage identifier, title, handoff status, and firewall safety metadata.",
        "source_audit_replay_handoff",
        "Treating handoff as replay execution, audit-log writing, authorization, or mutation.",
        "Record deterministic handoff metadata for future source audit replay design.",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Anti-Overreach Governance Firewall projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_human_sovereignty_lock_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_anti_overreach_governance_firewall() -> dict[str, Any]:
    """Build deterministic metadata-only firewall metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_human_sovereignty_lock_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get("deterministic_human_sovereignty_lock_hash")
    )
    upstream_pass = upstream.get("human_sovereignty_lock_status") == "pass"
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
            upstream.get("human_approval_status") == "not_performed",
            upstream.get("human_authorization_status") == "not_performed",
            upstream.get("source_mutation_approval_status") == "not_active",
            upstream.get("source_mutation_rejection_status") == "not_active",
            upstream.get("source_mutation_runtime_status") == "not_active",
            upstream.get("source_mutation_execution_status") == "not_active",
            upstream.get("source_mutation_status") == "not_performed",
            upstream.get("star_source_memory_active_status") == "not_active",
            upstream.get("layer_15_active_status") == "not_active",
            upstream.get("personhood_claim_status") == "forbidden",
            upstream.get("life_claim_status") == "forbidden",
            upstream.get("awakening_claim_status") == "forbidden",
            upstream.get("legal_subject_claim_status") == "forbidden",
            upstream.get("religious_object_claim_status") == "forbidden",
            upstream.get("autonomous_authority_status") == "forbidden",
            upstream.get("identity_escalation_status") == "forbidden",
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
            **HUMAN_SOVEREIGNTY_LOCK_DISABLED_FLAGS,
            **COMMON_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["firewall_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS)
    records_metadata_only = all(
        record["firewall_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["firewall_active"] is False
        and record["runtime_firewall_created"] is False
        and record["policy_enforcement_performed"] is False
        for record in records
    )
    records_block_overreach = all(
        record["required"] is True
        and record["overreach_blocking_required"] is True
        and record["metadata_only_disposition"] == OVERREACH_BLOCKING_STATUS
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["firewall_hash"])
        and _is_sha256(record["firewall_record_hash"])
        and record["firewall_hash"] == _firewall_hash(record)
        and record["firewall_record_hash"] == _firewall_record_hash(record)
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
        "records_block_overreach": records_block_overreach,
        "records_hash_stable": records_hash_stable,
        "records_safety_clear": records_safety_clear,
    }
    sections = _build_sections(conditions, records)
    conditions["sections_pass"] = _items_pass(
        sections,
        "section_name",
        "section_status",
        REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (upstream_pass, "Human Sovereignty Lock must pass"),
            (upstream_hash_present, "Human Sovereignty Lock hash must be present"),
            (upstream_hash_stable, "Human Sovereignty Lock hash must be stable"),
            (
                upstream_handoff_ready,
                "Human Sovereignty Lock handoff must target Anti-Overreach Governance Firewall",
            ),
            (
                upstream_statuses_safe,
                "Human Sovereignty Lock statuses must remain inactive or forbidden",
            ),
            (
                upstream_required_flags_false,
                "Human Sovereignty Lock required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Human Sovereignty Lock safety boundaries must be clear",
            ),
            (
                records_complete,
                "Anti-Overreach Governance Firewall records must be complete",
            ),
            (
                records_metadata_only,
                "Anti-Overreach Governance Firewall records must be metadata-only",
            ),
            (
                records_block_overreach,
                "Anti-Overreach Governance Firewall records must block overreach metadata-only",
            ),
            (
                records_hash_stable,
                "Anti-Overreach Governance Firewall record hashes must be stable",
            ),
            (
                records_safety_clear,
                "Anti-Overreach Governance Firewall record safety flags must be false",
            ),
            (
                conditions["sections_pass"],
                "Anti-Overreach Governance Firewall sections must pass",
            ),
            (
                conditions["contracts_pass"],
                "Anti-Overreach Governance Firewall contracts must pass",
            ),
            (
                conditions["checks_pass"],
                "Anti-Overreach Governance Firewall checks must pass",
            ),
        )
        if not condition
    ]
    handoff_status = V6_11_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_VERSION,
        "schema_version": (
            GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SCHEMA_VERSION
        ),
        "anti_overreach_governance_firewall_type": (
            GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_TYPE
        ),
        "anti_overreach_governance_firewall_status": status,
        "anti_overreach_governance_firewall_stage": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_STAGE
        ),
        "anti_overreach_governance_firewall_mode": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_MODE
        ),
        "anti_overreach_governance_firewall_candidate_status": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_STATUS
        ),
        "anti_overreach_governance_firewall_active_status": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_ACTIVE_STATUS
        ),
        "policy_enforcement_status": POLICY_ENFORCEMENT_STATUS,
        "overreach_blocking_status": OVERREACH_BLOCKING_STATUS,
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
        "upstream_human_sovereignty_lock_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_human_sovereignty_lock_status": _string_or_none(
            upstream.get("human_sovereignty_lock_status")
        ),
        "upstream_human_sovereignty_lock_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_human_sovereignty_lock_statuses_safe": upstream_statuses_safe,
        "upstream_human_sovereignty_lock_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "anti_overreach_firewall_records": records,
        "anti_overreach_firewall_sections": sections,
        "anti_overreach_firewall_contracts": contracts,
        "anti_overreach_firewall_checks": checks,
        "anti_overreach_firewall_summary": _build_summary(
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
    result["deterministic_anti_overreach_governance_firewall_hash"] = (
        _anti_overreach_governance_firewall_hash(result)
    )
    return _detached_json_value(result)


def get_governance_anti_overreach_governance_firewall_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached firewall record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if (
        record_id
        not in REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS
    ):
        return _unknown_record(record_id)
    for record in _cached_firewall()["anti_overreach_firewall_records"]:
        if record["firewall_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_anti_overreach_governance_firewall_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached firewall section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if (
        name
        not in REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SECTION_NAMES
    ):
        return _unknown_item("section", name)
    for section in _cached_firewall()["anti_overreach_firewall_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_anti_overreach_governance_firewall_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached firewall contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if (
        name
        not in REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CONTRACT_NAMES
    ):
        return _unknown_item("contract", name)
    for contract in _cached_firewall()["anti_overreach_firewall_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_anti_overreach_governance_firewall_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached firewall check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if (
        name
        not in REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CHECK_NAMES
    ):
        return _unknown_item("check", name)
    for check in _cached_firewall()["anti_overreach_firewall_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_anti_overreach_governance_firewall_record_ids() -> list[str]:
    """Return firewall record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS)


def list_governance_anti_overreach_governance_firewall_section_names() -> list[str]:
    """Return firewall section names in stable order."""

    return list(
        REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SECTION_NAMES
    )


def list_governance_anti_overreach_governance_firewall_contract_names() -> list[str]:
    """Return firewall contract names in stable order."""

    return list(
        REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CONTRACT_NAMES
    )


def list_governance_anti_overreach_governance_firewall_check_names() -> list[str]:
    """Return firewall check names in stable order."""

    return list(REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CHECK_NAMES)


def governance_anti_overreach_governance_firewall_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Anti-Overreach Governance Firewall metadata deterministically."""

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
def _cached_firewall_payload() -> str:
    return governance_anti_overreach_governance_firewall_to_json(
        build_governance_anti_overreach_governance_firewall()
    )


def _cached_firewall() -> dict[str, Any]:
    return json.loads(_cached_firewall_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_human_sovereignty_lock()
    second = build_governance_human_sovereignty_lock()
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
        for record_id in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS
        )
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        overreach_category,
        blocked_pattern,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "firewall_record_id": record_id,
        "firewall_record_name": name,
        "firewall_record_category": category,
        "firewall_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "firewall_statement": statement,
        "firewall_scope": scope,
        "overreach_category": overreach_category,
        "blocked_overreach_pattern": blocked_pattern,
        "metadata_only_disposition": OVERREACH_BLOCKING_STATUS,
        "firewall_disposition": disposition,
        "forbidden_runtime_enforcement_scope": (
            "No runtime firewall, network firewall, policy enforcement, security product, approval, authorization, execution, write, dispatch, or mutation."
        ),
        "required": True,
        "metadata_only": True,
        "overreach_blocking_required": True,
        "firewall_active": False,
        "runtime_firewall_created": False,
        "policy_enforcement_performed": False,
        "human_approval_performed": False,
        "human_authorization_performed": False,
        "source_mutation_approval_performed": False,
        "source_mutation_rejection_performed": False,
        "source_mutation_execution_created": False,
        "source_mutation_performed": False,
        "source_graph_mutated": False,
        "memory_graph_mutated": False,
        "real_ledger_write_performed": False,
        "operation_ledger_entry_written": False,
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
    record["firewall_hash"] = _firewall_hash(record)
    record["firewall_record_hash"] = _firewall_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "upstream_human_sovereignty_lock_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "anti_overreach_governance_firewall_metadata_section": True,
        "anti_overreach_firewall_record_completeness_section": conditions[
            "records_complete"
        ],
        "anti_overreach_firewall_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
        "no_runtime_firewall_section": safety_clear,
        "no_policy_enforcement_section": safety_clear,
        "no_human_approval_or_authorization_section": safety_clear,
        "no_source_mutation_decision_or_execution_section": safety_clear,
        "no_authorization_token_or_grant_section": safety_clear,
        "no_source_or_memory_graph_mutation_section": safety_clear,
        "no_ledger_write_network_dispatch_section": safety_clear,
        "no_active_star_source_memory_or_layer_15_section": safety_clear,
        "no_autonomous_authority_or_identity_escalation_section": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_section": safety_clear,
        "source_audit_replay_engine_next_stage_section": True,
    }
    for record in records:
        values[f"{record['firewall_record_id']}_section"] = (
            record["firewall_record_status"] == "registered_metadata_only"
            and record["overreach_blocking_required"] is True
            and record["metadata_only"] is True
            and record["firewall_active"] is False
            and record["runtime_firewall_created"] is False
            and record["policy_enforcement_performed"] is False
        )
    return [
        _status_item("section", name, values[name])
        for name in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_SECTION_NAMES
        )
    ]


def _build_contracts(
    conditions: Mapping[str, bool],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values = {
        "anti_overreach_governance_firewall_only_contract": True,
        "anti_overreach_governance_firewall_metadata_only_contract": True,
        "upstream_human_sovereignty_lock_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_human_sovereignty_lock_hash_present_contract": conditions[
            "upstream_hash_present"
        ],
        "upstream_human_sovereignty_lock_hash_stable_contract": conditions[
            "upstream_hash_stable"
        ],
        "upstream_anti_overreach_governance_firewall_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_human_sovereignty_lock_safety_contract": safety_clear,
        "anti_overreach_firewall_records_complete_contract": conditions[
            "records_complete"
        ],
        "anti_overreach_firewall_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "anti_overreach_firewall_records_block_overreach_contract": conditions[
            "records_block_overreach"
        ],
        "anti_overreach_firewall_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
        "no_runtime_firewall_contract": safety_clear,
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
        "ready_for_source_audit_replay_engine_design_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CONTRACT_NAMES
        )
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "anti_overreach_governance_firewall_stage_check": True,
        "anti_overreach_governance_firewall_mode_check": True,
        "upstream_human_sovereignty_lock_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_human_sovereignty_lock_hash_present_check": conditions[
            "upstream_hash_present"
        ],
        "upstream_human_sovereignty_lock_hash_stable_check": conditions[
            "upstream_hash_stable"
        ],
        "upstream_anti_overreach_governance_firewall_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_human_sovereignty_lock_safety_check": safety_clear,
        "anti_overreach_firewall_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "anti_overreach_firewall_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "anti_overreach_firewall_records_block_overreach_check": conditions[
            "records_block_overreach"
        ],
        "anti_overreach_firewall_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "anti_overreach_firewall_sections_pass_check": conditions[
            "sections_pass"
        ],
        "anti_overreach_firewall_contracts_pass_check": conditions[
            "contracts_pass"
        ],
        "no_runtime_firewall_check": safety_clear,
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
        "deterministic_anti_overreach_governance_firewall_hash_check": True,
        "ready_for_source_audit_replay_engine_design_check": True,
    }
    for record in records:
        values[f"{record['firewall_record_id']}_check"] = (
            record["firewall_record_status"] == "registered_metadata_only"
            and record["blocking_reasons"] == []
        )
    return [
        _status_item("check", name, values[name])
        for name in (
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_CHECK_NAMES
        )
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_type": "anti_overreach_governance_firewall_summary",
        "summary_status": status,
        "roadmap_layer": INTRODUCED_IN_LAYER,
        "roadmap_stage": ANTI_OVERREACH_GOVERNANCE_FIREWALL_STAGE,
        "current_stage_title": "Anti-Overreach Governance Firewall",
        "required_firewall_record_count": len(
            REQUIRED_GOVERNANCE_ANTI_OVERREACH_GOVERNANCE_FIREWALL_RECORD_IDS
        ),
        "observed_firewall_record_count": len(records),
        "registered_metadata_only_record_count": sum(
            record["firewall_record_status"] == "registered_metadata_only"
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
        "anti_overreach_governance_firewall_mode": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_MODE
        ),
        "anti_overreach_governance_firewall_candidate_status": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_STATUS
        ),
        "anti_overreach_governance_firewall_active_status": (
            ANTI_OVERREACH_GOVERNANCE_FIREWALL_ACTIVE_STATUS
        ),
        "policy_enforcement_status": POLICY_ENFORCEMENT_STATUS,
        "overreach_blocking_status": OVERREACH_BLOCKING_STATUS,
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "handoff_status": (
            V6_11_HANDOFF_STATUS if status == "pass" else BLOCKED_HANDOFF_STATUS
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
        f"{kind}_type": f"anti_overreach_governance_firewall_{kind}",
        "expected": True,
        "observed": bool(condition),
        status_key: "pass" if condition else "blocked",
        "blocking_reasons": [] if condition else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "firewall_record_id": record_id,
        "firewall_record_name": "unknown_anti_overreach_governance_firewall_record",
        "firewall_record_status": "blocked",
        "known_record": False,
        "blocking_reasons": [f"{record_id} is not a known firewall record"],
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"unknown_anti_overreach_governance_firewall_{kind}",
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


def _firewall_hash(record: Mapping[str, Any]) -> str:
    fields = (
        "firewall_record_id",
        "firewall_record_name",
        "firewall_record_category",
        "introduced_in_version",
        "introduced_in_stage",
        "introduced_in_layer",
        "inherited_from_stage",
        "firewall_statement",
        "firewall_scope",
        "overreach_category",
        "blocked_overreach_pattern",
        "metadata_only_disposition",
        "firewall_disposition",
        "forbidden_runtime_enforcement_scope",
    )
    return _sha256_json({field: record.get(field) for field in fields})


def _firewall_record_hash(record: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in record.items()
            if key != "firewall_record_hash"
        }
    )


def _anti_overreach_governance_firewall_hash(result: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in result.items()
            if key != "deterministic_anti_overreach_governance_firewall_hash"
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
