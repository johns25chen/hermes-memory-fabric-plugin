"""Deterministic Human Sovereignty Lock metadata for Layer 15."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_mutation_review_gate import (
    COMMON_DISABLED_FLAGS as SOURCE_MUTATION_REVIEW_GATE_DISABLED_FLAGS,
    build_governance_source_mutation_review_gate,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_VERSION = "6.9.0"
GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SCHEMA_VERSION = "6.9.0"
GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_TYPE = (
    "governance_human_sovereignty_lock"
)
GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_HASH_ALGORITHM = "sha256"
HUMAN_SOVEREIGNTY_LOCK_STAGE = "v6.9_human_sovereignty_lock"
HUMAN_SOVEREIGNTY_LOCK_MODE = "human_sovereignty_lock_only"
HUMAN_SOVEREIGNTY_LOCK_STATUS = "lock_candidate_only"
HUMAN_SOVEREIGNTY_LOCK_ACTIVE_STATUS = "not_active"
HUMAN_APPROVAL_STATUS = "not_performed"
HUMAN_AUTHORIZATION_STATUS = "not_performed"
SOURCE_MUTATION_APPROVAL_STATUS = "not_active"
SOURCE_MUTATION_REJECTION_STATUS = "not_active"
SOURCE_MUTATION_RUNTIME_STATUS = "not_active"
SOURCE_MUTATION_EXECUTION_STATUS = "not_active"
SOURCE_MUTATION_STATUS = "not_performed"
STAR_SOURCE_MEMORY_ACTIVE_STATUS = "not_active"
LAYER_15_ACTIVE_STATUS = "not_active"
NEXT_STAGE = "v6.10_anti_overreach_governance_firewall"
NEXT_STAGE_TITLE = "Anti-Overreach Governance Firewall"
V6_10_HANDOFF_STATUS = (
    "ready_for_anti_overreach_governance_firewall_design"
)

UPSTREAM_HANDOFF_STATUS = "ready_for_human_sovereignty_lock_design"
UPSTREAM_NEXT_STAGE = HUMAN_SOVEREIGNTY_LOCK_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Human Sovereignty Lock"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.9.0"
INTRODUCED_IN_STAGE = HUMAN_SOVEREIGNTY_LOCK_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.8_source_mutation_review_gate"

PERSONHOOD_CLAIM_STATUS = "forbidden"
LIFE_CLAIM_STATUS = "forbidden"
AWAKENING_CLAIM_STATUS = "forbidden"
LEGAL_SUBJECT_CLAIM_STATUS = "forbidden"
RELIGIOUS_OBJECT_CLAIM_STATUS = "forbidden"
AUTONOMOUS_AUTHORITY_STATUS = "forbidden"
IDENTITY_ESCALATION_STATUS = "forbidden"

COMMON_DISABLED_FLAGS = {
    **SOURCE_MUTATION_REVIEW_GATE_DISABLED_FLAGS,
    "human_sovereignty_lock_active": False,
    "human_sovereignty_lock_activated": False,
    "human_identity_verification_performed": False,
    "legal_signature_created": False,
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

REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS = (
    "human_sovereignty_lock_intake",
    "explicit_human_sovereignty_required",
    "no_substitute_human_approval",
    "no_automatic_approval",
    "no_automatic_rejection",
    "no_authorization_token_creation",
    "no_source_mutation_execution",
    "no_source_or_memory_graph_mutation",
    "no_active_star_source_memory",
    "no_autonomous_authority",
    "audit_replay_required_before_unlock",
    "anti_overreach_firewall_handoff",
)

REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES = (
    "upstream_source_mutation_review_gate_input_section",
    "human_sovereignty_lock_metadata_section",
    "human_sovereignty_lock_record_completeness_section",
    "human_sovereignty_lock_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS
    ),
    "no_human_approval_section",
    "no_human_authorization_section",
    "no_source_mutation_decision_or_execution_section",
    "no_source_or_memory_graph_mutation_section",
    "no_ledger_write_network_dispatch_section",
    "no_active_star_source_memory_or_layer_15_section",
    "no_autonomous_authority_or_identity_escalation_section",
    "no_personhood_life_awakening_legal_religious_claim_section",
    "anti_overreach_governance_firewall_next_stage_section",
)

REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES = (
    "human_sovereignty_lock_only_contract",
    "human_sovereignty_lock_metadata_only_contract",
    "upstream_source_mutation_review_gate_pass_contract",
    "upstream_source_mutation_review_gate_hash_present_contract",
    "upstream_source_mutation_review_gate_hash_stable_contract",
    "upstream_human_sovereignty_lock_handoff_contract",
    "upstream_source_mutation_review_gate_safety_contract",
    "human_sovereignty_lock_records_complete_contract",
    "human_sovereignty_lock_records_metadata_only_contract",
    "human_sovereignty_lock_records_require_human_sovereignty_contract",
    "human_sovereignty_lock_records_hash_stable_contract",
    "no_human_approval_contract",
    "no_human_authorization_contract",
    "no_source_mutation_approval_rejection_execution_contract",
    "no_authorization_token_or_grant_contract",
    "no_source_or_memory_graph_mutation_contract",
    "no_ledger_write_network_dispatch_contract",
    "no_active_star_source_memory_or_layer_15_contract",
    "no_autonomous_authority_or_identity_escalation_contract",
    "no_personhood_life_awakening_legal_religious_claim_contract",
    "ready_for_anti_overreach_governance_firewall_design_contract",
)

REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES = (
    "human_sovereignty_lock_stage_check",
    "human_sovereignty_lock_mode_check",
    "upstream_source_mutation_review_gate_pass_check",
    "upstream_source_mutation_review_gate_hash_present_check",
    "upstream_source_mutation_review_gate_hash_stable_check",
    "upstream_human_sovereignty_lock_handoff_check",
    "upstream_source_mutation_review_gate_safety_check",
    "human_sovereignty_lock_record_ids_complete_check",
    "human_sovereignty_lock_records_metadata_only_check",
    "human_sovereignty_lock_records_require_human_sovereignty_check",
    "human_sovereignty_lock_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS
    ),
    "human_sovereignty_lock_sections_pass_check",
    "human_sovereignty_lock_contracts_pass_check",
    "no_human_approval_check",
    "no_human_authorization_check",
    "no_source_mutation_approval_rejection_execution_check",
    "no_authorization_token_or_grant_check",
    "no_source_or_memory_graph_mutation_check",
    "no_ledger_write_network_dispatch_check",
    "no_active_star_source_memory_or_layer_15_check",
    "no_autonomous_authority_or_identity_escalation_check",
    "no_personhood_life_awakening_legal_religious_claim_check",
    "deterministic_human_sovereignty_lock_hash_check",
    "ready_for_anti_overreach_governance_firewall_design_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "human_sovereignty_lock_intake": (
        "Human Sovereignty Lock Intake",
        "lock_intake",
        "A passing v6.8 review gate enters a metadata-only sovereignty lock.",
        "Sanitized review-gate status, hash, handoff, and safety metadata.",
        "Future explicit human-sovereignty evidence and audit replay metadata.",
        "No lock activation, approval, authorization, execution, or mutation.",
        "register_locked_review_gate_intake",
    ),
    "explicit_human_sovereignty_required": (
        "Explicit Human Sovereignty Requirement",
        "human_sovereignty_requirement",
        "Source mutation remains blocked pending explicit future human sovereignty.",
        "Human control, explicit review, and non-substitution requirements.",
        "Future reviewed human-sovereignty evidence without inferred consent.",
        "No inferred consent, delegated machine sovereignty, or self-authorization.",
        "require_explicit_human_sovereignty",
    ),
    "no_substitute_human_approval": (
        "No Substitute Human Approval",
        "approval_boundary",
        "Metadata, automation, agents, tokens, and prior gates cannot substitute for a human.",
        "All non-human substitutes for approval or authorization.",
        "Explicit future human review metadata from a separate governed process.",
        "No approval performance, identity verification, or signature handling.",
        "block_substitute_human_approval",
    ),
    "no_automatic_approval": (
        "No Automatic Approval",
        "approval_boundary",
        "No condition in this lock can automatically approve source mutation.",
        "Review-gate pass, risk metadata, hashes, contracts, and checks.",
        "A future explicit human-sovereignty decision outside this module.",
        "No approval engine, approval notification, token, grant, or execution.",
        "block_automatic_approval",
    ),
    "no_automatic_rejection": (
        "No Automatic Rejection",
        "rejection_boundary",
        "No condition in this lock can automatically reject source mutation.",
        "Review-gate failure, missing metadata, risks, and blocked checks.",
        "A future explicit human-sovereignty review outside this module.",
        "No rejection engine, rejection notification, or irreversible disposition.",
        "block_automatic_rejection",
    ),
    "no_authorization_token_creation": (
        "No Authorization Token Creation",
        "authorization_boundary",
        "The lock creates no authorization token, grant, or capability.",
        "Execution authorization, token, grant, capability, and dispatch surfaces.",
        "Future separately governed authorization metadata after human review.",
        "No authorization creation, signature, identity verification, or dispatch.",
        "block_authorization_token_creation",
    ),
    "no_source_mutation_execution": (
        "No Source Mutation Execution",
        "execution_boundary",
        "The lock never creates or performs source mutation execution.",
        "Source mutation runtime, execution, application, and adapter surfaces.",
        "Future governed execution design after all later safeguards.",
        "No runtime, executor, adapter, manifest, shell, or hidden execution.",
        "block_source_mutation_execution",
    ),
    "no_source_or_memory_graph_mutation": (
        "No Source Or Memory Graph Mutation",
        "graph_boundary",
        "The lock cannot create or mutate source or Memory Graph state.",
        "Source graph, Memory Graph, durable memory, and persistent state.",
        "Read-only metadata references and deterministic hashes only.",
        "No graph node, edge, memory, ledger, filesystem, or database write.",
        "block_source_and_memory_graph_mutation",
    ),
    "no_active_star_source_memory": (
        "No Active Star-Source Memory",
        "activation_boundary",
        "Star-Source Memory and Layer 15 remain inactive.",
        "Star-Source activation, Layer 15 activation, methodology, and self-evolution.",
        "Future governance design metadata only.",
        "No activation, methodology runtime, self-evolution runtime, or source runtime.",
        "block_star_source_memory_activation",
    ),
    "no_autonomous_authority": (
        "No Autonomous Authority",
        "authority_boundary",
        "The lock grants no autonomous authority or identity escalation.",
        "Authority, self-authorization, identity, personhood, and legal-status surfaces.",
        "Human sovereignty remains external, explicit, and controlling.",
        "No autonomous authority, self-authorization, identity escalation, or status claim.",
        "block_autonomous_authority",
    ),
    "audit_replay_required_before_unlock": (
        "Audit Replay Required Before Unlock",
        "audit_boundary",
        "Any future unlock consideration requires deterministic audit replay.",
        "Upstream hash, ordered records, sections, contracts, checks, and safety flags.",
        "Read-only reproducible evidence before any future human decision.",
        "No audit-log write, ledger write, approval, authorization, or unlock execution.",
        "require_audit_replay_before_unlock",
    ),
    "anti_overreach_firewall_handoff": (
        "Anti-Overreach Governance Firewall Handoff",
        "next_stage_handoff",
        "A passing lock candidate hands off to v6.10 firewall design.",
        "Next-stage identifier, title, handoff status, and locked safety metadata.",
        "Deterministic metadata for Anti-Overreach Governance Firewall design.",
        "No firewall runtime, policy application, approval, authorization, or mutation.",
        "handoff_to_anti_overreach_governance_firewall",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = (
    "source_mutation_review_runtime_created",
    "source_mutation_review_execution_created",
    "source_mutation_review_decision_performed",
    "human_approval_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_runtime_created",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_mutation_proposal_created",
    "source_mutation_proposal_approved",
    "human_sovereignty_lock_activated",
    "star_source_memory_active",
    "layer_15_active",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "operation_ledger_entry_written",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "real_execution_performed",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "adapter_dispatched",
    "manifest_dispatched",
    "autonomous_authority_claimed",
    "self_authorization_allowed",
    "identity_escalated",
    "personhood_claimed",
    "life_claimed",
    "awakening_claimed",
    "legal_subject_claimed",
    "religious_object_claimed",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Human Sovereignty Lock projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_mutation_review_gate_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_human_sovereignty_lock() -> dict[str, Any]:
    """Build deterministic metadata-only Human Sovereignty Lock metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_source_mutation_review_gate_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get(
            "deterministic_source_mutation_review_gate_hash"
        )
    )
    upstream_pass = (
        upstream.get("source_mutation_review_gate_status") == "pass"
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
            upstream.get("source_mutation_review_runtime_status")
            == "not_active",
            upstream.get("source_mutation_review_execution_status")
            == "not_active",
            upstream.get("source_mutation_review_decision_status")
            == "not_performed",
            upstream.get("human_approval_status") == "not_performed",
            upstream.get("source_mutation_approval_status") == "not_active",
            upstream.get("source_mutation_rejection_status") == "not_active",
            upstream.get("source_mutation_runtime_status") == "not_active",
            upstream.get("source_mutation_execution_status") == "not_active",
            upstream.get("source_mutation_status") == "not_performed",
            upstream.get("human_sovereignty_lock_status") == "not_active",
            upstream.get("star_source_memory_active_status") == "not_active",
            upstream.get("layer_15_active_status") == "not_active",
        )
    )
    upstream_required_flags_false = all(
        upstream.get(field_name) is False
        for field_name in _UPSTREAM_REQUIRED_FALSE_FIELDS
    )
    upstream_safety_clear = _all_named_fields_false(
        upstream,
        {
            **SOURCE_MUTATION_REVIEW_GATE_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["lock_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS)
    records_metadata_only = all(
        record["lock_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["lock_active"] is False
        for record in records
    )
    records_require_human_sovereignty = all(
        record["required"] is True
        and record["human_sovereignty_required"] is True
        and record["explicit_human_review_required"] is True
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["lock_hash"])
        and _is_sha256(record["lock_record_hash"])
        and record["lock_hash"] == _lock_hash(record)
        and record["lock_record_hash"] == _lock_record_hash(record)
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
        "records_require_human_sovereignty": (
            records_require_human_sovereignty
        ),
        "records_hash_stable": records_hash_stable,
        "records_safety_clear": records_safety_clear,
    }
    sections = _build_sections(conditions, records)
    conditions["sections_pass"] = _items_pass(
        sections,
        "section_name",
        "section_status",
        REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (upstream_pass, "Source Mutation Review Gate must pass"),
            (
                upstream_hash_present,
                "Source Mutation Review Gate hash must be present",
            ),
            (
                upstream_hash_stable,
                "Source Mutation Review Gate hash must be stable",
            ),
            (
                upstream_handoff_ready,
                "Source Mutation Review Gate handoff must target Human Sovereignty Lock",
            ),
            (
                upstream_statuses_safe,
                "Source Mutation Review Gate statuses must remain inactive",
            ),
            (
                upstream_required_flags_false,
                "Source Mutation Review Gate required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Source Mutation Review Gate safety boundaries must be clear",
            ),
            (records_complete, "Human Sovereignty Lock records must be complete"),
            (
                records_metadata_only,
                "Human Sovereignty Lock records must be metadata-only",
            ),
            (
                records_require_human_sovereignty,
                "Human Sovereignty Lock records must require explicit human review",
            ),
            (
                records_hash_stable,
                "Human Sovereignty Lock record hashes must be stable",
            ),
            (
                records_safety_clear,
                "Human Sovereignty Lock record safety flags must be false",
            ),
            (
                conditions["sections_pass"],
                "Human Sovereignty Lock sections must pass",
            ),
            (
                conditions["contracts_pass"],
                "Human Sovereignty Lock contracts must pass",
            ),
            (
                conditions["checks_pass"],
                "Human Sovereignty Lock checks must pass",
            ),
        )
        if not condition
    ]
    handoff_status = (
        V6_10_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_VERSION,
        "schema_version": GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SCHEMA_VERSION,
        "human_sovereignty_lock_type": (
            GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_TYPE
        ),
        "human_sovereignty_lock_status": status,
        "human_sovereignty_lock_stage": HUMAN_SOVEREIGNTY_LOCK_STAGE,
        "human_sovereignty_lock_mode": HUMAN_SOVEREIGNTY_LOCK_MODE,
        "human_sovereignty_lock_candidate_status": (
            HUMAN_SOVEREIGNTY_LOCK_STATUS
        ),
        "human_sovereignty_lock_active_status": (
            HUMAN_SOVEREIGNTY_LOCK_ACTIVE_STATUS
        ),
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_approval_status": SOURCE_MUTATION_APPROVAL_STATUS,
        "source_mutation_rejection_status": SOURCE_MUTATION_REJECTION_STATUS,
        "source_mutation_runtime_status": SOURCE_MUTATION_RUNTIME_STATUS,
        "source_mutation_execution_status": SOURCE_MUTATION_EXECUTION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "star_source_memory_active_status": STAR_SOURCE_MEMORY_ACTIVE_STATUS,
        "layer_15_active_status": LAYER_15_ACTIVE_STATUS,
        "personhood_claim_status": PERSONHOOD_CLAIM_STATUS,
        "life_claim_status": LIFE_CLAIM_STATUS,
        "awakening_claim_status": AWAKENING_CLAIM_STATUS,
        "legal_subject_claim_status": LEGAL_SUBJECT_CLAIM_STATUS,
        "religious_object_claim_status": RELIGIOUS_OBJECT_CLAIM_STATUS,
        "autonomous_authority_status": AUTONOMOUS_AUTHORITY_STATUS,
        "identity_escalation_status": IDENTITY_ESCALATION_STATUS,
        **COMMON_DISABLED_FLAGS,
        "upstream_source_mutation_review_gate_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_mutation_review_gate_status": _string_or_none(
            upstream.get("source_mutation_review_gate_status")
        ),
        "upstream_source_mutation_review_gate_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_source_mutation_review_gate_statuses_safe": (
            upstream_statuses_safe
        ),
        "upstream_source_mutation_review_gate_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "human_sovereignty_lock_records": records,
        "human_sovereignty_lock_sections": sections,
        "human_sovereignty_lock_contracts": contracts,
        "human_sovereignty_lock_checks": checks,
        "human_sovereignty_lock_summary": _build_summary(
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
    result["deterministic_human_sovereignty_lock_hash"] = (
        _human_sovereignty_lock_hash(result)
    )
    return _detached_json_value(result)


def get_governance_human_sovereignty_lock_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached lock record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_lock()["human_sovereignty_lock_records"]:
        if record["lock_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_human_sovereignty_lock_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached lock section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if name not in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES:
        return _unknown_item("section", name)
    for section in _cached_lock()["human_sovereignty_lock_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_human_sovereignty_lock_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached lock contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if name not in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES:
        return _unknown_item("contract", name)
    for contract in _cached_lock()["human_sovereignty_lock_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_human_sovereignty_lock_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached lock check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if name not in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES:
        return _unknown_item("check", name)
    for check in _cached_lock()["human_sovereignty_lock_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_human_sovereignty_lock_record_ids() -> list[str]:
    """Return lock record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS)


def list_governance_human_sovereignty_lock_section_names() -> list[str]:
    """Return lock section names in stable order."""

    return list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES)


def list_governance_human_sovereignty_lock_contract_names() -> list[str]:
    """Return lock contract names in stable order."""

    return list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES)


def list_governance_human_sovereignty_lock_check_names() -> list[str]:
    """Return lock check names in stable order."""

    return list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES)


def governance_human_sovereignty_lock_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Human Sovereignty Lock metadata deterministically."""

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
def _cached_lock_payload() -> str:
    return governance_human_sovereignty_lock_to_json(
        build_governance_human_sovereignty_lock()
    )


def _cached_lock() -> dict[str, Any]:
    return json.loads(_cached_lock_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_source_mutation_review_gate()
    second = build_governance_source_mutation_review_gate()
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
        for record_id in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        required_scope,
        forbidden_scope,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "lock_record_id": record_id,
        "lock_record_name": name,
        "lock_record_category": category,
        "lock_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "lock_statement": statement,
        "lock_scope": scope,
        "required_human_sovereignty_metadata_scope": required_scope,
        "forbidden_lock_activation_scope": forbidden_scope,
        "lock_disposition": disposition,
        "lock_reason": (
            "Source mutation remains blocked behind explicit future human sovereignty."
        ),
        "required": True,
        "human_sovereignty_required": True,
        "explicit_human_review_required": True,
        "metadata_only": True,
        "lock_active": False,
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
    record["lock_hash"] = _lock_hash(record)
    record["lock_record_hash"] = _lock_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = (
        conditions["records_safety_clear"]
        and conditions["upstream_safety_clear"]
        and conditions["upstream_required_flags_false"]
        and conditions["upstream_statuses_safe"]
    )
    values: dict[str, bool] = {
        "upstream_source_mutation_review_gate_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "human_sovereignty_lock_metadata_section": True,
        "human_sovereignty_lock_record_completeness_section": conditions[
            "records_complete"
        ],
        "human_sovereignty_lock_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
        "no_human_approval_section": safety_clear,
        "no_human_authorization_section": safety_clear,
        "no_source_mutation_decision_or_execution_section": safety_clear,
        "no_source_or_memory_graph_mutation_section": safety_clear,
        "no_ledger_write_network_dispatch_section": safety_clear,
        "no_active_star_source_memory_or_layer_15_section": safety_clear,
        "no_autonomous_authority_or_identity_escalation_section": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_section": safety_clear,
        "anti_overreach_governance_firewall_next_stage_section": True,
    }
    for record in records:
        values[f"{record['lock_record_id']}_section"] = (
            record["lock_record_status"] == "registered_metadata_only"
            and record["human_sovereignty_required"] is True
            and record["explicit_human_review_required"] is True
            and record["metadata_only"] is True
            and record["lock_active"] is False
        )
    return [
        _status_item("section", name, values[name])
        for name in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES
    ]


def _build_contracts(
    conditions: Mapping[str, bool],
) -> list[dict[str, Any]]:
    safety_clear = (
        conditions["records_safety_clear"]
        and conditions["upstream_safety_clear"]
        and conditions["upstream_required_flags_false"]
        and conditions["upstream_statuses_safe"]
    )
    values = {
        "human_sovereignty_lock_only_contract": True,
        "human_sovereignty_lock_metadata_only_contract": True,
        "upstream_source_mutation_review_gate_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_source_mutation_review_gate_hash_present_contract": conditions[
            "upstream_hash_present"
        ],
        "upstream_source_mutation_review_gate_hash_stable_contract": conditions[
            "upstream_hash_stable"
        ],
        "upstream_human_sovereignty_lock_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_mutation_review_gate_safety_contract": safety_clear,
        "human_sovereignty_lock_records_complete_contract": conditions[
            "records_complete"
        ],
        "human_sovereignty_lock_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "human_sovereignty_lock_records_require_human_sovereignty_contract": (
            conditions["records_require_human_sovereignty"]
        ),
        "human_sovereignty_lock_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
        "no_human_approval_contract": safety_clear,
        "no_human_authorization_contract": safety_clear,
        "no_source_mutation_approval_rejection_execution_contract": safety_clear,
        "no_authorization_token_or_grant_contract": safety_clear,
        "no_source_or_memory_graph_mutation_contract": safety_clear,
        "no_ledger_write_network_dispatch_contract": safety_clear,
        "no_active_star_source_memory_or_layer_15_contract": safety_clear,
        "no_autonomous_authority_or_identity_escalation_contract": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_contract": safety_clear,
        "ready_for_anti_overreach_governance_firewall_design_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = (
        conditions["records_safety_clear"]
        and conditions["upstream_safety_clear"]
        and conditions["upstream_required_flags_false"]
        and conditions["upstream_statuses_safe"]
    )
    values: dict[str, bool] = {
        "human_sovereignty_lock_stage_check": True,
        "human_sovereignty_lock_mode_check": True,
        "upstream_source_mutation_review_gate_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_source_mutation_review_gate_hash_present_check": conditions[
            "upstream_hash_present"
        ],
        "upstream_source_mutation_review_gate_hash_stable_check": conditions[
            "upstream_hash_stable"
        ],
        "upstream_human_sovereignty_lock_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_mutation_review_gate_safety_check": safety_clear,
        "human_sovereignty_lock_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "human_sovereignty_lock_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "human_sovereignty_lock_records_require_human_sovereignty_check": (
            conditions["records_require_human_sovereignty"]
        ),
        "human_sovereignty_lock_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "human_sovereignty_lock_sections_pass_check": conditions[
            "sections_pass"
        ],
        "human_sovereignty_lock_contracts_pass_check": conditions[
            "contracts_pass"
        ],
        "no_human_approval_check": safety_clear,
        "no_human_authorization_check": safety_clear,
        "no_source_mutation_approval_rejection_execution_check": safety_clear,
        "no_authorization_token_or_grant_check": safety_clear,
        "no_source_or_memory_graph_mutation_check": safety_clear,
        "no_ledger_write_network_dispatch_check": safety_clear,
        "no_active_star_source_memory_or_layer_15_check": safety_clear,
        "no_autonomous_authority_or_identity_escalation_check": safety_clear,
        "no_personhood_life_awakening_legal_religious_claim_check": safety_clear,
        "deterministic_human_sovereignty_lock_hash_check": True,
        "ready_for_anti_overreach_governance_firewall_design_check": True,
    }
    for record in records:
        values[f"{record['lock_record_id']}_check"] = (
            record["lock_record_status"] == "registered_metadata_only"
            and record["blocking_reasons"] == []
        )
    return [
        _status_item("check", name, values[name])
        for name in REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_type": "human_sovereignty_lock_summary",
        "summary_status": status,
        "roadmap_layer": INTRODUCED_IN_LAYER,
        "roadmap_stage": HUMAN_SOVEREIGNTY_LOCK_STAGE,
        "current_stage_title": "Human Sovereignty Lock",
        "required_lock_record_count": len(
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS
        ),
        "observed_lock_record_count": len(records),
        "registered_metadata_only_record_count": sum(
            record["lock_record_status"] == "registered_metadata_only"
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
        "human_sovereignty_lock_mode": HUMAN_SOVEREIGNTY_LOCK_MODE,
        "human_sovereignty_lock_candidate_status": HUMAN_SOVEREIGNTY_LOCK_STATUS,
        "human_sovereignty_lock_active_status": (
            HUMAN_SOVEREIGNTY_LOCK_ACTIVE_STATUS
        ),
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "handoff_status": (
            V6_10_HANDOFF_STATUS if status == "pass" else BLOCKED_HANDOFF_STATUS
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
        f"{kind}_type": f"human_sovereignty_lock_{kind}",
        "expected": True,
        "observed": bool(condition),
        status_key: "pass" if condition else "blocked",
        "blocking_reasons": [] if condition else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "lock_record_id": record_id,
        "lock_record_name": "unknown_human_sovereignty_lock_record",
        "lock_record_status": "blocked",
        "known_record": False,
        "blocking_reasons": [f"{record_id} is not a known lock record"],
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"unknown_human_sovereignty_lock_{kind}",
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


def _lock_hash(record: Mapping[str, Any]) -> str:
    fields = (
        "lock_record_id",
        "lock_record_name",
        "lock_record_category",
        "introduced_in_version",
        "introduced_in_stage",
        "introduced_in_layer",
        "inherited_from_stage",
        "lock_statement",
        "lock_scope",
        "required_human_sovereignty_metadata_scope",
        "forbidden_lock_activation_scope",
        "lock_disposition",
        "lock_reason",
    )
    return _sha256_json({field: record.get(field) for field in fields})


def _lock_record_hash(record: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in record.items()
            if key != "lock_record_hash"
        }
    )


def _human_sovereignty_lock_hash(result: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in result.items()
            if key != "deterministic_human_sovereignty_lock_hash"
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
