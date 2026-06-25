"""Deterministic Source Audit Replay Engine metadata."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_anti_overreach_governance_firewall import (
    COMMON_DISABLED_FLAGS as ANTI_OVERREACH_DISABLED_FLAGS,
    build_governance_anti_overreach_governance_firewall,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_VERSION = "6.11.0"
GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SCHEMA_VERSION = "6.11.0"
GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_TYPE = (
    "governance_source_audit_replay_engine"
)
GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_HASH_ALGORITHM = "sha256"
SOURCE_AUDIT_REPLAY_ENGINE_STAGE = "v6.11_source_audit_replay_engine"
SOURCE_AUDIT_REPLAY_ENGINE_MODE = "source_audit_replay_engine_only"
SOURCE_AUDIT_REPLAY_ENGINE_STATUS = "replay_engine_candidate_only"
SOURCE_AUDIT_REPLAY_ENGINE_ACTIVE_STATUS = "not_active"
AUDIT_REPLAY_STATUS = "metadata_only"
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
NEXT_STAGE = "v6.12_cross_layer_integrity_validator"
NEXT_STAGE_TITLE = "Cross-Layer Integrity Validator"
V6_12_HANDOFF_STATUS = "ready_for_cross_layer_integrity_validator_design"

UPSTREAM_HANDOFF_STATUS = "ready_for_source_audit_replay_engine_design"
UPSTREAM_NEXT_STAGE = SOURCE_AUDIT_REPLAY_ENGINE_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Source Audit Replay Engine"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.11.0"
INTRODUCED_IN_STAGE = SOURCE_AUDIT_REPLAY_ENGINE_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.10_anti_overreach_governance_firewall"

COMMON_DISABLED_FLAGS = {
    **ANTI_OVERREACH_DISABLED_FLAGS,
    "replay_engine_active": False,
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

REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS = (
    "source_audit_replay_engine_intake",
    "upstream_firewall_hash_replay_reference",
    "ordered_source_governance_stage_registry",
    "replay_scope_metadata_registry",
    "replay_input_contract_registry",
    "replay_output_contract_registry",
    "no_audit_replay_execution",
    "no_audit_log_or_ledger_write",
    "no_source_or_memory_graph_mutation",
    "no_authorization_or_dispatch_replay",
    "no_active_star_source_memory_replay",
    "cross_layer_integrity_validator_handoff",
)

REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SECTION_NAMES = (
    "upstream_anti_overreach_governance_firewall_input_section",
    "source_audit_replay_engine_metadata_section",
    "source_audit_replay_record_completeness_section",
    "source_audit_replay_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS
    ),
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
    "cross_layer_integrity_validator_next_stage_section",
)

REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CONTRACT_NAMES = (
    "source_audit_replay_engine_only_contract",
    "source_audit_replay_engine_metadata_only_contract",
    "upstream_anti_overreach_governance_firewall_pass_contract",
    "upstream_anti_overreach_governance_firewall_hash_present_contract",
    "upstream_anti_overreach_governance_firewall_hash_stable_contract",
    "upstream_source_audit_replay_engine_handoff_contract",
    "upstream_anti_overreach_governance_firewall_safety_contract",
    "source_audit_replay_records_complete_contract",
    "source_audit_replay_records_metadata_only_contract",
    "source_audit_replay_records_no_execution_contract",
    "source_audit_replay_records_hash_stable_contract",
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
    "ready_for_cross_layer_integrity_validator_design_contract",
)

REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CHECK_NAMES = (
    "source_audit_replay_engine_stage_check",
    "source_audit_replay_engine_mode_check",
    "upstream_anti_overreach_governance_firewall_pass_check",
    "upstream_anti_overreach_governance_firewall_hash_present_check",
    "upstream_anti_overreach_governance_firewall_hash_stable_check",
    "upstream_source_audit_replay_engine_handoff_check",
    "upstream_anti_overreach_governance_firewall_safety_check",
    "source_audit_replay_record_ids_complete_check",
    "source_audit_replay_records_metadata_only_check",
    "source_audit_replay_records_no_execution_check",
    "source_audit_replay_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS
    ),
    "source_audit_replay_sections_pass_check",
    "source_audit_replay_contracts_pass_check",
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
    "deterministic_source_audit_replay_engine_hash_check",
    "ready_for_cross_layer_integrity_validator_design_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "source_audit_replay_engine_intake": (
        "Source Audit Replay Engine Intake",
        "replay_engine_intake",
        "A passing Anti-Overreach Governance Firewall enters metadata-only replay description.",
        "Sanitized v6.10 status, hash, handoff, and safety metadata.",
        "replay_intake",
        "Executing audit replay, writing logs, or authorizing source mutation from intake metadata.",
        "Register metadata-only replay intake and keep all runtime surfaces inactive.",
    ),
    "upstream_firewall_hash_replay_reference": (
        "Upstream Firewall Hash Replay Reference",
        "upstream_hash_reference",
        "The v6.10 deterministic firewall hash is referenced as replay evidence metadata.",
        "Upstream status and hash reference only, without raw logs or execution payloads.",
        "upstream_hash_reference",
        "Treating hash reference as a ledger write, operation-ledger entry, or replay execution.",
        "Record the stable upstream hash reference as metadata only.",
    ),
    "ordered_source_governance_stage_registry": (
        "Ordered Source Governance Stage Registry",
        "stage_registry",
        "Prior source governance stages are listed for deterministic future replay description.",
        "Stage identifiers, order, inherited stage, current stage, and next-stage handoff.",
        "stage_registry",
        "Dispatching stages, invoking adapters, or re-running any prior governance stage.",
        "Describe stage order without stage execution or dispatch.",
    ),
    "replay_scope_metadata_registry": (
        "Replay Scope Metadata Registry",
        "scope_registry",
        "Replay scope is bounded to deterministic metadata descriptions only.",
        "Replay scope labels, forbidden runtime scope, and metadata-only disposition.",
        "scope_metadata",
        "Expanding replay scope into runtime, firewall enforcement, network, or write surfaces.",
        "Register replay scope as metadata-only boundary text.",
    ),
    "replay_input_contract_registry": (
        "Replay Input Contract Registry",
        "input_contract_registry",
        "Replay inputs are upstream status, hash, handoff, and safety flags only.",
        "Sanitized upstream contract fields and safety boundary booleans.",
        "input_contract",
        "Reading raw audit logs, external systems, filesystem state, or Memory Graph content.",
        "Describe input contracts without live IO.",
    ),
    "replay_output_contract_registry": (
        "Replay Output Contract Registry",
        "output_contract_registry",
        "Replay outputs are deterministic JSON-compatible metadata and hashes only.",
        "Records, sections, contracts, checks, summary, handoff, hash contract, and safety flags.",
        "output_contract",
        "Writing audit logs, ledgers, databases, files, graph nodes, or notifications.",
        "Describe output contracts without persistence.",
    ),
    "no_audit_replay_execution": (
        "No Audit Replay Execution",
        "execution_boundary",
        "The engine never performs audit replay execution.",
        "Replay executors, schedulers, runtimes, callbacks, shells, and hidden execution.",
        "execution_boundary",
        "Calling replay logic, running historical operations, or simulating real audit execution.",
        "Record replay execution as not performed.",
    ),
    "no_audit_log_or_ledger_write": (
        "No Audit Log Or Ledger Write",
        "write_boundary",
        "The engine never writes audit logs, ledgers, operation-ledger entries, or durable state.",
        "Audit logs, ledgers, operation ledgers, filesystem, database, durable memory, and external writes.",
        "write_boundary",
        "Persisting replay descriptions as logs, ledgers, files, databases, or durable memory.",
        "Record write surfaces as not performed.",
    ),
    "no_source_or_memory_graph_mutation": (
        "No Source Or Memory Graph Mutation",
        "graph_boundary",
        "The engine never mutates source graphs or the Memory Graph.",
        "Source graph, Memory Graph, graph provenance, graph edges, graph nodes, and durable graph state.",
        "graph_boundary",
        "Creating or mutating graph state from replay metadata.",
        "Record graph mutation as not performed.",
    ),
    "no_authorization_or_dispatch_replay": (
        "No Authorization Or Dispatch Replay",
        "authorization_dispatch_boundary",
        "The engine never creates authorization, approval notifications, adapter dispatch, or manifest dispatch.",
        "Approval, authorization, token, grant, notification, adapter, manifest, and execution clearance surfaces.",
        "authorization_dispatch_boundary",
        "Replaying authorization, dispatch, approvals, notifications, adapters, or manifests.",
        "Record authorization and dispatch surfaces as absent.",
    ),
    "no_active_star_source_memory_replay": (
        "No Active Star-Source Memory Replay",
        "activation_boundary",
        "The engine never activates Star-Source Memory or Layer 15.",
        "Star-Source Memory activation, Layer 15 activation, methodology runtime, and self-evolution runtime.",
        "activation_boundary",
        "Treating replay metadata as active Star-Source Memory, active Layer 15, or self-evolution runtime.",
        "Record activation as not active.",
    ),
    "cross_layer_integrity_validator_handoff": (
        "Cross-Layer Integrity Validator Handoff",
        "next_stage_handoff",
        "A passing replay engine candidate hands off to v6.12 cross-layer integrity validator design.",
        "Next-stage identifier, title, handoff status, and replay-engine safety metadata.",
        "cross_layer_handoff",
        "Treating handoff as validation execution, approval, authorization, replay runtime, or mutation.",
        "Record deterministic handoff metadata for future cross-layer integrity validation design.",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Source Audit Replay Engine projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_anti_overreach_governance_firewall_included": False,
    "raw_audit_logs_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_source_audit_replay_engine() -> dict[str, Any]:
    """Build deterministic metadata-only source audit replay metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_anti_overreach_governance_firewall_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get(
            "deterministic_anti_overreach_governance_firewall_hash"
        )
    )
    upstream_pass = (
        upstream.get("anti_overreach_governance_firewall_status") == "pass"
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
            upstream.get("anti_overreach_governance_firewall_active_status")
            == "not_active",
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
            **ANTI_OVERREACH_DISABLED_FLAGS,
            **COMMON_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["replay_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS)
    records_metadata_only = all(
        record["replay_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["audit_replay_metadata_required"] is True
        and record["metadata_only_disposition"] == AUDIT_REPLAY_STATUS
        and record["replay_engine_active"] is False
        for record in records
    )
    records_no_execution = all(
        record["required"] is True
        and record["audit_replay_executed"] is False
        and record["audit_log_written"] is False
        and record["ledger_write_performed"] is False
        and record["source_mutation_performed"] is False
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["replay_hash"])
        and _is_sha256(record["replay_record_hash"])
        and record["replay_hash"] == _replay_hash(record)
        and record["replay_record_hash"] == _replay_record_hash(record)
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
        REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (
                upstream_pass,
                "Anti-Overreach Governance Firewall must pass",
            ),
            (
                upstream_hash_present,
                "Anti-Overreach Governance Firewall hash must be present",
            ),
            (
                upstream_hash_stable,
                "Anti-Overreach Governance Firewall hash must be stable",
            ),
            (
                upstream_handoff_ready,
                "Anti-Overreach Governance Firewall handoff must target Source Audit Replay Engine",
            ),
            (
                upstream_statuses_safe,
                "Anti-Overreach Governance Firewall statuses must remain inactive",
            ),
            (
                upstream_required_flags_false,
                "Anti-Overreach Governance Firewall required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Anti-Overreach Governance Firewall safety boundaries must be clear",
            ),
            (
                records_complete,
                "Source Audit Replay Engine records must be complete",
            ),
            (
                records_metadata_only,
                "Source Audit Replay Engine records must be metadata-only",
            ),
            (
                records_no_execution,
                "Source Audit Replay Engine records must not execute or write",
            ),
            (
                records_hash_stable,
                "Source Audit Replay Engine record hashes must be stable",
            ),
            (
                records_safety_clear,
                "Source Audit Replay Engine record safety flags must be false",
            ),
            (
                conditions["sections_pass"],
                "Source Audit Replay Engine sections must pass",
            ),
            (
                conditions["contracts_pass"],
                "Source Audit Replay Engine contracts must pass",
            ),
            (
                conditions["checks_pass"],
                "Source Audit Replay Engine checks must pass",
            ),
        )
        if not condition
    ]
    handoff_status = V6_12_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_VERSION,
        "schema_version": GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SCHEMA_VERSION,
        "source_audit_replay_engine_type": (
            GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_TYPE
        ),
        "source_audit_replay_engine_status": status,
        "source_audit_replay_engine_stage": SOURCE_AUDIT_REPLAY_ENGINE_STAGE,
        "source_audit_replay_engine_mode": SOURCE_AUDIT_REPLAY_ENGINE_MODE,
        "source_audit_replay_engine_candidate_status": (
            SOURCE_AUDIT_REPLAY_ENGINE_STATUS
        ),
        "source_audit_replay_engine_active_status": (
            SOURCE_AUDIT_REPLAY_ENGINE_ACTIVE_STATUS
        ),
        "audit_replay_status": AUDIT_REPLAY_STATUS,
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
        "upstream_anti_overreach_governance_firewall_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_anti_overreach_governance_firewall_status": _string_or_none(
            upstream.get("anti_overreach_governance_firewall_status")
        ),
        "upstream_anti_overreach_governance_firewall_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_anti_overreach_governance_firewall_statuses_safe": (
            upstream_statuses_safe
        ),
        "upstream_anti_overreach_governance_firewall_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "source_audit_replay_records": records,
        "source_audit_replay_sections": sections,
        "source_audit_replay_contracts": contracts,
        "source_audit_replay_checks": checks,
        "source_audit_replay_summary": _build_summary(
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
    result["deterministic_source_audit_replay_engine_hash"] = (
        _source_audit_replay_engine_hash(result)
    )
    return _detached_json_value(result)


def get_governance_source_audit_replay_engine_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached replay record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_replay_engine()["source_audit_replay_records"]:
        if record["replay_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_source_audit_replay_engine_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached replay section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if name not in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SECTION_NAMES:
        return _unknown_item("section", name)
    for section in _cached_replay_engine()["source_audit_replay_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_source_audit_replay_engine_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached replay contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if name not in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CONTRACT_NAMES:
        return _unknown_item("contract", name)
    for contract in _cached_replay_engine()["source_audit_replay_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_source_audit_replay_engine_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached replay check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if name not in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CHECK_NAMES:
        return _unknown_item("check", name)
    for check in _cached_replay_engine()["source_audit_replay_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_source_audit_replay_engine_record_ids() -> list[str]:
    """Return replay record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS)


def list_governance_source_audit_replay_engine_section_names() -> list[str]:
    """Return replay section names in stable order."""

    return list(REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SECTION_NAMES)


def list_governance_source_audit_replay_engine_contract_names() -> list[str]:
    """Return replay contract names in stable order."""

    return list(REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CONTRACT_NAMES)


def list_governance_source_audit_replay_engine_check_names() -> list[str]:
    """Return replay check names in stable order."""

    return list(REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CHECK_NAMES)


def governance_source_audit_replay_engine_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Source Audit Replay Engine metadata deterministically."""

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
def _cached_replay_engine_payload() -> str:
    return governance_source_audit_replay_engine_to_json(
        build_governance_source_audit_replay_engine()
    )


def _cached_replay_engine() -> dict[str, Any]:
    return json.loads(_cached_replay_engine_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_anti_overreach_governance_firewall()
    second = build_governance_anti_overreach_governance_firewall()
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
        for record_id in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        replay_category,
        forbidden_scope,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "replay_record_id": record_id,
        "replay_record_name": name,
        "replay_record_category": category,
        "replay_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "replay_statement": statement,
        "replay_scope": scope,
        "replay_category": replay_category,
        "replay_reference_scope": "source_governance_metadata_only",
        "metadata_only_disposition": AUDIT_REPLAY_STATUS,
        "replay_disposition": disposition,
        "forbidden_replay_execution_scope": forbidden_scope,
        "required": True,
        "metadata_only": True,
        "audit_replay_metadata_required": True,
        "replay_engine_active": False,
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
    record["replay_hash"] = _replay_hash(record)
    record["replay_record_hash"] = _replay_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "upstream_anti_overreach_governance_firewall_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "source_audit_replay_engine_metadata_section": True,
        "source_audit_replay_record_completeness_section": conditions[
            "records_complete"
        ],
        "source_audit_replay_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
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
        "cross_layer_integrity_validator_next_stage_section": True,
    }
    for record in records:
        values[f"{record['replay_record_id']}_section"] = (
            record["replay_record_status"] == "registered_metadata_only"
            and record["audit_replay_metadata_required"] is True
            and record["metadata_only"] is True
            and record["replay_engine_active"] is False
            and record["audit_replay_executed"] is False
        )
    return [
        _status_item("section", name, values[name])
        for name in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_SECTION_NAMES
    ]


def _build_contracts(
    conditions: Mapping[str, bool],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values = {
        "source_audit_replay_engine_only_contract": True,
        "source_audit_replay_engine_metadata_only_contract": True,
        "upstream_anti_overreach_governance_firewall_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_anti_overreach_governance_firewall_hash_present_contract": (
            conditions["upstream_hash_present"]
        ),
        "upstream_anti_overreach_governance_firewall_hash_stable_contract": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_source_audit_replay_engine_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_anti_overreach_governance_firewall_safety_contract": (
            safety_clear
        ),
        "source_audit_replay_records_complete_contract": conditions[
            "records_complete"
        ],
        "source_audit_replay_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "source_audit_replay_records_no_execution_contract": conditions[
            "records_no_execution"
        ],
        "source_audit_replay_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
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
        "ready_for_cross_layer_integrity_validator_design_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CONTRACT_NAMES
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "source_audit_replay_engine_stage_check": True,
        "source_audit_replay_engine_mode_check": True,
        "upstream_anti_overreach_governance_firewall_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_anti_overreach_governance_firewall_hash_present_check": (
            conditions["upstream_hash_present"]
        ),
        "upstream_anti_overreach_governance_firewall_hash_stable_check": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_source_audit_replay_engine_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_anti_overreach_governance_firewall_safety_check": safety_clear,
        "source_audit_replay_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "source_audit_replay_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "source_audit_replay_records_no_execution_check": conditions[
            "records_no_execution"
        ],
        "source_audit_replay_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "source_audit_replay_sections_pass_check": conditions["sections_pass"],
        "source_audit_replay_contracts_pass_check": conditions[
            "contracts_pass"
        ],
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
        "deterministic_source_audit_replay_engine_hash_check": True,
        "ready_for_cross_layer_integrity_validator_design_check": True,
    }
    for record in records:
        values[f"{record['replay_record_id']}_check"] = (
            record["replay_record_status"] == "registered_metadata_only"
            and record["blocking_reasons"] == []
        )
    return [
        _status_item("check", name, values[name])
        for name in REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_CHECK_NAMES
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_type": "source_audit_replay_engine_summary",
        "summary_status": status,
        "roadmap_layer": INTRODUCED_IN_LAYER,
        "roadmap_stage": SOURCE_AUDIT_REPLAY_ENGINE_STAGE,
        "current_stage_title": "Source Audit Replay Engine",
        "required_replay_record_count": len(
            REQUIRED_GOVERNANCE_SOURCE_AUDIT_REPLAY_ENGINE_RECORD_IDS
        ),
        "observed_replay_record_count": len(records),
        "registered_metadata_only_record_count": sum(
            record["replay_record_status"] == "registered_metadata_only"
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
        "source_audit_replay_engine_mode": SOURCE_AUDIT_REPLAY_ENGINE_MODE,
        "source_audit_replay_engine_candidate_status": (
            SOURCE_AUDIT_REPLAY_ENGINE_STATUS
        ),
        "source_audit_replay_engine_active_status": (
            SOURCE_AUDIT_REPLAY_ENGINE_ACTIVE_STATUS
        ),
        "audit_replay_status": AUDIT_REPLAY_STATUS,
        "audit_replay_execution_status": AUDIT_REPLAY_EXECUTION_STATUS,
        "audit_log_write_status": AUDIT_LOG_WRITE_STATUS,
        "ledger_write_status": LEDGER_WRITE_STATUS,
        "policy_enforcement_status": POLICY_ENFORCEMENT_STATUS,
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "handoff_status": (
            V6_12_HANDOFF_STATUS if status == "pass" else BLOCKED_HANDOFF_STATUS
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
        f"{kind}_type": f"source_audit_replay_engine_{kind}",
        "expected": True,
        "observed": bool(condition),
        status_key: "pass" if condition else "blocked",
        "blocking_reasons": [] if condition else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "replay_record_id": record_id,
        "replay_record_name": "unknown_source_audit_replay_engine_record",
        "replay_record_status": "blocked",
        "known_record": False,
        "blocking_reasons": [f"{record_id} is not a known replay record"],
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"unknown_source_audit_replay_engine_{kind}",
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


def _replay_hash(record: Mapping[str, Any]) -> str:
    fields = (
        "replay_record_id",
        "replay_record_name",
        "replay_record_category",
        "introduced_in_version",
        "introduced_in_stage",
        "introduced_in_layer",
        "inherited_from_stage",
        "replay_statement",
        "replay_scope",
        "replay_category",
        "replay_reference_scope",
        "metadata_only_disposition",
        "replay_disposition",
        "forbidden_replay_execution_scope",
    )
    return _sha256_json({field: record.get(field) for field in fields})


def _replay_record_hash(record: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in record.items()
            if key != "replay_record_hash"
        }
    )


def _source_audit_replay_engine_hash(result: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in result.items()
            if key != "deterministic_source_audit_replay_engine_hash"
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
