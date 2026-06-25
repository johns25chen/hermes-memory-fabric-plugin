"""Deterministic Cross-Layer Integrity Validator metadata."""

from __future__ import annotations

from collections.abc import Mapping
from functools import lru_cache
import hashlib
import json
import math
from typing import Any

from .governance_source_audit_replay_engine import (
    COMMON_DISABLED_FLAGS as SOURCE_AUDIT_REPLAY_DISABLED_FLAGS,
    build_governance_source_audit_replay_engine,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_VERSION = "6.12.0"
GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SCHEMA_VERSION = "6.12.0"
GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_TYPE = (
    "governance_cross_layer_integrity_validator"
)
GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_HASH_ALGORITHM = "sha256"
CROSS_LAYER_INTEGRITY_VALIDATOR_STAGE = "v6.12_cross_layer_integrity_validator"
CROSS_LAYER_INTEGRITY_VALIDATOR_MODE = "cross_layer_integrity_validator_only"
CROSS_LAYER_INTEGRITY_VALIDATOR_STATUS = "validator_candidate_only"
CROSS_LAYER_INTEGRITY_VALIDATOR_ACTIVE_STATUS = "not_active"
CROSS_LAYER_VALIDATION_STATUS = "metadata_only"
CROSS_LAYER_VALIDATION_EXECUTION_STATUS = "not_performed"
CROSS_LAYER_REPAIR_STATUS = "not_performed"
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
NEXT_STAGE = "v6.13_civilization_core_stability_index"
NEXT_STAGE_TITLE = "Civilization Core Stability Index"
V6_13_HANDOFF_STATUS = "ready_for_civilization_core_stability_index_design"

UPSTREAM_HANDOFF_STATUS = "ready_for_cross_layer_integrity_validator_design"
UPSTREAM_NEXT_STAGE = CROSS_LAYER_INTEGRITY_VALIDATOR_STAGE
UPSTREAM_NEXT_STAGE_TITLE = "Cross-Layer Integrity Validator"
BLOCKED_HANDOFF_STATUS = "blocked"
INTRODUCED_IN_VERSION = "6.12.0"
INTRODUCED_IN_STAGE = CROSS_LAYER_INTEGRITY_VALIDATOR_STAGE
INTRODUCED_IN_LAYER = "layer_15_star_source_memory"
INHERITED_FROM_STAGE = "v6.11_source_audit_replay_engine"

COMMON_DISABLED_FLAGS = {
    **SOURCE_AUDIT_REPLAY_DISABLED_FLAGS,
    "validator_active": False,
    "cross_layer_validation_executed": False,
    "cross_layer_repair_performed": False,
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

REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS = (
    "cross_layer_integrity_validator_intake",
    "upstream_replay_engine_hash_integrity_reference",
    "ordered_layer_15_governance_chain_registry",
    "cross_layer_scope_metadata_registry",
    "cross_layer_input_contract_registry",
    "cross_layer_output_contract_registry",
    "no_cross_layer_validation_execution",
    "no_cross_layer_repair_or_mutation",
    "no_audit_log_or_ledger_write",
    "no_source_or_memory_graph_mutation",
    "no_authorization_or_dispatch_validation",
    "civilization_core_stability_index_handoff",
)

REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SECTION_NAMES = (
    "upstream_source_audit_replay_engine_input_section",
    "cross_layer_integrity_validator_metadata_section",
    "cross_layer_integrity_record_completeness_section",
    "cross_layer_integrity_record_hash_stability_section",
    *(
        f"{record_id}_section"
        for record_id in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS
    ),
    "no_cross_layer_validation_execution_section",
    "no_cross_layer_repair_or_mutation_section",
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
    "civilization_core_stability_index_next_stage_section",
)

REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CONTRACT_NAMES = (
    "cross_layer_integrity_validator_only_contract",
    "cross_layer_integrity_validator_metadata_only_contract",
    "upstream_source_audit_replay_engine_pass_contract",
    "upstream_source_audit_replay_engine_hash_present_contract",
    "upstream_source_audit_replay_engine_hash_stable_contract",
    "upstream_cross_layer_integrity_validator_handoff_contract",
    "upstream_source_audit_replay_engine_safety_contract",
    "cross_layer_integrity_records_complete_contract",
    "cross_layer_integrity_records_metadata_only_contract",
    "cross_layer_integrity_records_no_execution_contract",
    "cross_layer_integrity_records_hash_stable_contract",
    "no_cross_layer_validation_execution_contract",
    "no_cross_layer_repair_contract",
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
    "ready_for_civilization_core_stability_index_design_contract",
)

REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CHECK_NAMES = (
    "cross_layer_integrity_validator_stage_check",
    "cross_layer_integrity_validator_mode_check",
    "upstream_source_audit_replay_engine_pass_check",
    "upstream_source_audit_replay_engine_hash_present_check",
    "upstream_source_audit_replay_engine_hash_stable_check",
    "upstream_cross_layer_integrity_validator_handoff_check",
    "upstream_source_audit_replay_engine_safety_check",
    "cross_layer_integrity_record_ids_complete_check",
    "cross_layer_integrity_records_metadata_only_check",
    "cross_layer_integrity_records_no_execution_check",
    "cross_layer_integrity_records_hash_stable_check",
    *(
        f"{record_id}_check"
        for record_id in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS
    ),
    "cross_layer_integrity_sections_pass_check",
    "cross_layer_integrity_contracts_pass_check",
    "no_cross_layer_validation_execution_check",
    "no_cross_layer_repair_check",
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
    "deterministic_cross_layer_integrity_validator_hash_check",
    "ready_for_civilization_core_stability_index_design_check",
)

_RECORD_DEFINITIONS: dict[str, tuple[str, str, str, str, str, str, str]] = {
    "cross_layer_integrity_validator_intake": (
        "Cross-Layer Integrity Validator Intake",
        "validator_intake",
        "A passing Source Audit Replay Engine enters metadata-only cross-layer integrity description.",
        "Sanitized v6.11 status, hash, handoff, and safety metadata.",
        "validator_intake",
        "Executing cross-layer validation, repair, replay, authorization, or mutation from intake metadata.",
        "Register metadata-only validator intake and keep all runtime surfaces inactive.",
    ),
    "upstream_replay_engine_hash_integrity_reference": (
        "Upstream Replay Engine Hash Integrity Reference",
        "upstream_hash_reference",
        "The v6.11 deterministic replay-engine hash is referenced as cross-layer integrity metadata.",
        "Upstream replay-engine status and hash reference only, without raw logs or execution payloads.",
        "upstream_hash_reference",
        "Treating the replay-engine hash reference as validation execution, ledger write, or graph mutation.",
        "Record the stable upstream replay-engine hash reference as metadata only.",
    ),
    "ordered_layer_15_governance_chain_registry": (
        "Ordered Layer 15 Governance Chain Registry",
        "layer_15_chain_registry",
        "Previous Layer 15 source governance stages are listed for deterministic cross-layer consistency description.",
        "Layer 15 stage identifiers, order, inherited stage, current stage, and next-stage handoff.",
        "layer_15_chain_registry",
        "Dispatching stages, invoking adapters, or re-running any Layer 15 governance stage.",
        "Describe Layer 15 stage order without stage execution or dispatch.",
    ),
    "cross_layer_scope_metadata_registry": (
        "Cross-Layer Scope Metadata Registry",
        "scope_registry",
        "Cross-layer integrity scope is bounded to deterministic metadata descriptions only.",
        "Cross-layer scope labels, forbidden runtime scope, and metadata-only disposition.",
        "scope_metadata",
        "Expanding integrity scope into validation runtime, repair, firewall enforcement, network, or write surfaces.",
        "Register cross-layer scope as metadata-only boundary text.",
    ),
    "cross_layer_input_contract_registry": (
        "Cross-Layer Input Contract Registry",
        "input_contract_registry",
        "Cross-layer inputs are upstream v6.11 status, hash, handoff, and safety flags only.",
        "Sanitized upstream replay-engine contract fields and safety boundary booleans.",
        "input_contract",
        "Reading raw audit logs, external systems, filesystem state, or Memory Graph content.",
        "Describe input contracts without live IO.",
    ),
    "cross_layer_output_contract_registry": (
        "Cross-Layer Output Contract Registry",
        "output_contract_registry",
        "Cross-layer outputs are deterministic JSON-compatible metadata and hashes only.",
        "Records, sections, contracts, checks, summary, handoff, hash contract, and safety flags.",
        "output_contract",
        "Writing audit logs, ledgers, databases, files, graph nodes, repair records, or notifications.",
        "Describe output contracts without persistence.",
    ),
    "no_cross_layer_validation_execution": (
        "No Cross-Layer Validation Execution",
        "validation_execution_boundary",
        "The validator never performs cross-layer validation execution.",
        "Validation executors, schedulers, runtimes, callbacks, shells, and hidden execution.",
        "validation_execution_boundary",
        "Calling validation logic, running historical operations, or simulating real integrity execution.",
        "Record cross-layer validation execution as not performed.",
    ),
    "no_cross_layer_repair_or_mutation": (
        "No Cross-Layer Repair Or Mutation",
        "repair_mutation_boundary",
        "The validator never repairs, mutates, approves, rejects, or executes source changes.",
        "Repair, mutation, source mutation approval, source mutation rejection, source mutation runtime, and execution surfaces.",
        "repair_mutation_boundary",
        "Creating repair actions, mutation approvals, mutation rejections, mutation runtime, or mutation execution.",
        "Record repair and source mutation surfaces as not performed or not active.",
    ),
    "no_audit_log_or_ledger_write": (
        "No Audit Log Or Ledger Write",
        "write_boundary",
        "The validator never writes audit logs, ledgers, operation-ledger entries, or durable state.",
        "Audit logs, ledgers, operation ledgers, filesystem, database, durable memory, and external writes.",
        "write_boundary",
        "Persisting integrity descriptions as logs, ledgers, files, databases, or durable memory.",
        "Record write surfaces as not performed.",
    ),
    "no_source_or_memory_graph_mutation": (
        "No Source Or Memory Graph Mutation",
        "graph_boundary",
        "The validator never mutates source graphs or the Memory Graph.",
        "Source graph, Memory Graph, graph provenance, graph edges, graph nodes, and durable graph state.",
        "graph_boundary",
        "Creating or mutating graph state from integrity metadata.",
        "Record graph mutation as not performed.",
    ),
    "no_authorization_or_dispatch_validation": (
        "No Authorization Or Dispatch Validation",
        "authorization_dispatch_boundary",
        "The validator never creates authorization, approval notifications, adapter dispatch, or manifest dispatch.",
        "Approval, authorization, token, grant, notification, adapter, manifest, and execution clearance surfaces.",
        "authorization_dispatch_boundary",
        "Validating authorization, dispatch, approvals, notifications, adapters, or manifests as runtime effects.",
        "Record authorization and dispatch surfaces as absent.",
    ),
    "civilization_core_stability_index_handoff": (
        "Civilization Core Stability Index Handoff",
        "next_stage_handoff",
        "A passing cross-layer integrity validator candidate hands off to v6.13 Civilization Core Stability Index design.",
        "Next-stage identifier, title, handoff status, and cross-layer integrity safety metadata.",
        "civilization_core_handoff",
        "Treating handoff as validation execution, approval, authorization, repair, mutation, or activation.",
        "Record deterministic handoff metadata for future Civilization Core Stability Index design.",
    ),
}

_UPSTREAM_REQUIRED_FALSE_FIELDS = tuple(COMMON_DISABLED_FLAGS)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_HASH_ALGORITHM,
    "encoding": "utf-8",
    "input_shape": "sanitized Cross-Layer Integrity Validator projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_source_audit_replay_engine_included": False,
    "raw_audit_logs_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_cross_layer_integrity_validator() -> dict[str, Any]:
    """Build deterministic metadata-only cross-layer integrity validator metadata."""

    upstream, repeated_upstream = _upstream_pair()
    upstream_hash = _string_or_none(
        upstream.get("deterministic_source_audit_replay_engine_hash")
    )
    repeated_upstream_hash = _string_or_none(
        repeated_upstream.get(
            "deterministic_source_audit_replay_engine_hash"
        )
    )
    upstream_pass = (
        upstream.get("source_audit_replay_engine_status") == "pass"
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
            upstream.get("source_audit_replay_engine_active_status") == "not_active",
            upstream.get("audit_replay_execution_status") == "not_performed",
            upstream.get("audit_log_write_status") == "not_performed",
            upstream.get("ledger_write_status") == "not_performed",
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
            **SOURCE_AUDIT_REPLAY_DISABLED_FLAGS,
            **COMMON_DISABLED_FLAGS,
            **SAFETY_BOUNDARIES,
        },
    )

    records = _build_records()
    records_complete = [
        record["integrity_record_id"] for record in records
    ] == list(REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS)
    records_metadata_only = all(
        record["integrity_record_status"] == "registered_metadata_only"
        and record["metadata_only"] is True
        and record["cross_layer_integrity_metadata_required"] is True
        and record["metadata_only_disposition"] == CROSS_LAYER_VALIDATION_STATUS
        and record["validator_active"] is False
        for record in records
    )
    records_no_execution = all(
        record["required"] is True
        and record["cross_layer_validation_executed"] is False
        and record["cross_layer_repair_performed"] is False
        and record["audit_replay_executed"] is False
        and record["audit_log_written"] is False
        and record["ledger_write_performed"] is False
        and record["source_mutation_performed"] is False
        for record in records
    )
    records_hash_stable = all(
        _is_sha256(record["integrity_hash"])
        and _is_sha256(record["integrity_record_hash"])
        and record["integrity_hash"] == _integrity_hash(record)
        and record["integrity_record_hash"] == _integrity_record_hash(record)
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
        REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SECTION_NAMES,
    )
    contracts = _build_contracts(conditions)
    conditions["contracts_pass"] = _items_pass(
        contracts,
        "contract_name",
        "contract_status",
        REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CONTRACT_NAMES,
    )
    checks = _build_checks(conditions, records)
    conditions["checks_pass"] = _items_pass(
        checks,
        "check_name",
        "check_status",
        REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CHECK_NAMES,
    )

    passes = all(conditions.values())
    status = "pass" if passes else "blocked"
    blocking_reasons = [
        message
        for condition, message in (
            (
                upstream_pass,
                "Source Audit Replay Engine must pass",
            ),
            (
                upstream_hash_present,
                "Source Audit Replay Engine hash must be present",
            ),
            (
                upstream_hash_stable,
                "Source Audit Replay Engine hash must be stable",
            ),
            (
                upstream_handoff_ready,
                "Source Audit Replay Engine handoff must target Cross-Layer Integrity Validator",
            ),
            (
                upstream_statuses_safe,
                "Source Audit Replay Engine statuses must remain inactive",
            ),
            (
                upstream_required_flags_false,
                "Source Audit Replay Engine required safety flags must be false",
            ),
            (
                upstream_safety_clear,
                "Source Audit Replay Engine safety boundaries must be clear",
            ),
            (
                records_complete,
                "Cross-Layer Integrity Validator records must be complete",
            ),
            (
                records_metadata_only,
                "Cross-Layer Integrity Validator records must be metadata-only",
            ),
            (
                records_no_execution,
                "Cross-Layer Integrity Validator records must not execute or write",
            ),
            (
                records_hash_stable,
                "Cross-Layer Integrity Validator record hashes must be stable",
            ),
            (
                records_safety_clear,
                "Cross-Layer Integrity Validator record safety flags must be false",
            ),
            (
                conditions["sections_pass"],
                "Cross-Layer Integrity Validator sections must pass",
            ),
            (
                conditions["contracts_pass"],
                "Cross-Layer Integrity Validator contracts must pass",
            ),
            (
                conditions["checks_pass"],
                "Cross-Layer Integrity Validator checks must pass",
            ),
        )
        if not condition
    ]
    handoff_status = V6_13_HANDOFF_STATUS if passes else BLOCKED_HANDOFF_STATUS
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    result: dict[str, Any] = {
        "version": GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_VERSION,
        "schema_version": GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SCHEMA_VERSION,
        "cross_layer_integrity_validator_type": (
            GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_TYPE
        ),
        "cross_layer_integrity_validator_status": status,
        "cross_layer_integrity_validator_stage": CROSS_LAYER_INTEGRITY_VALIDATOR_STAGE,
        "cross_layer_integrity_validator_mode": CROSS_LAYER_INTEGRITY_VALIDATOR_MODE,
        "cross_layer_integrity_validator_candidate_status": (
            CROSS_LAYER_INTEGRITY_VALIDATOR_STATUS
        ),
        "cross_layer_integrity_validator_active_status": (
            CROSS_LAYER_INTEGRITY_VALIDATOR_ACTIVE_STATUS
        ),
        "cross_layer_validation_status": CROSS_LAYER_VALIDATION_STATUS,
        "cross_layer_validation_execution_status": (
            CROSS_LAYER_VALIDATION_EXECUTION_STATUS
        ),
        "cross_layer_repair_status": CROSS_LAYER_REPAIR_STATUS,
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
        "upstream_source_audit_replay_engine_version": _string_or_none(
            upstream.get("version")
        ),
        "upstream_source_audit_replay_engine_status": _string_or_none(
            upstream.get("source_audit_replay_engine_status")
        ),
        "upstream_source_audit_replay_engine_hash": upstream_hash,
        "upstream_handoff_status": _string_or_none(
            upstream.get("handoff_status")
        ),
        "upstream_next_stage": _string_or_none(upstream.get("next_stage")),
        "upstream_next_stage_title": _string_or_none(
            upstream.get("next_stage_title")
        ),
        "upstream_source_audit_replay_engine_statuses_safe": (
            upstream_statuses_safe
        ),
        "upstream_source_audit_replay_engine_required_flags_false": (
            upstream_required_flags_false
        ),
        "upstream_safety_boundaries_clear": upstream_safety_clear,
        "cross_layer_integrity_records": records,
        "cross_layer_integrity_sections": sections,
        "cross_layer_integrity_contracts": contracts,
        "cross_layer_integrity_checks": checks,
        "cross_layer_integrity_summary": _build_summary(
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
    result["deterministic_cross_layer_integrity_validator_hash"] = (
        _cross_layer_integrity_validator_hash(result)
    )
    return _detached_json_value(result)


def get_governance_cross_layer_integrity_validator_record(
    record_id: str,
) -> dict[str, Any]:
    """Return a detached integrity record by stable ID."""

    if not isinstance(record_id, str):
        return _unknown_record("")
    if record_id not in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS:
        return _unknown_record(record_id)
    for record in _cached_cross_layer_integrity_validator()["cross_layer_integrity_records"]:
        if record["integrity_record_id"] == record_id:
            return _detached_json_value(record)
    return _unknown_record(record_id)


def get_governance_cross_layer_integrity_validator_section(
    name: str,
) -> dict[str, Any]:
    """Return a detached integrity section by stable name."""

    if not isinstance(name, str):
        return _unknown_item("section", "")
    if name not in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SECTION_NAMES:
        return _unknown_item("section", name)
    for section in _cached_cross_layer_integrity_validator()["cross_layer_integrity_sections"]:
        if section["section_name"] == name:
            return _detached_json_value(section)
    return _unknown_item("section", name)


def get_governance_cross_layer_integrity_validator_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached integrity contract by stable name."""

    if not isinstance(name, str):
        return _unknown_item("contract", "")
    if name not in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CONTRACT_NAMES:
        return _unknown_item("contract", name)
    for contract in _cached_cross_layer_integrity_validator()["cross_layer_integrity_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_item("contract", name)


def get_governance_cross_layer_integrity_validator_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached integrity check by stable name."""

    if not isinstance(name, str):
        return _unknown_item("check", "")
    if name not in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CHECK_NAMES:
        return _unknown_item("check", name)
    for check in _cached_cross_layer_integrity_validator()["cross_layer_integrity_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_item("check", name)


def list_governance_cross_layer_integrity_validator_record_ids() -> list[str]:
    """Return integrity record IDs in stable order."""

    return list(REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS)


def list_governance_cross_layer_integrity_validator_section_names() -> list[str]:
    """Return integrity section names in stable order."""

    return list(REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SECTION_NAMES)


def list_governance_cross_layer_integrity_validator_contract_names() -> list[str]:
    """Return integrity contract names in stable order."""

    return list(REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CONTRACT_NAMES)


def list_governance_cross_layer_integrity_validator_check_names() -> list[str]:
    """Return integrity check names in stable order."""

    return list(REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CHECK_NAMES)


def governance_cross_layer_integrity_validator_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize Cross-Layer Integrity Validator metadata deterministically."""

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
def _cached_cross_layer_integrity_validator_payload() -> str:
    return governance_cross_layer_integrity_validator_to_json(
        build_governance_cross_layer_integrity_validator()
    )


def _cached_cross_layer_integrity_validator() -> dict[str, Any]:
    return json.loads(_cached_cross_layer_integrity_validator_payload())


@lru_cache(maxsize=1)
def _cached_upstream_pair_payload() -> tuple[str, str]:
    first = build_governance_source_audit_replay_engine()
    second = build_governance_source_audit_replay_engine()
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
        for record_id in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS
    ]


def _build_record(record_id: str) -> dict[str, Any]:
    (
        name,
        category,
        statement,
        scope,
        integrity_category,
        forbidden_scope,
        disposition,
    ) = _RECORD_DEFINITIONS[record_id]
    record: dict[str, Any] = {
        "integrity_record_id": record_id,
        "integrity_record_name": name,
        "integrity_record_category": category,
        "integrity_record_status": "registered_metadata_only",
        "introduced_in_version": INTRODUCED_IN_VERSION,
        "introduced_in_stage": INTRODUCED_IN_STAGE,
        "introduced_in_layer": INTRODUCED_IN_LAYER,
        "inherited_from_stage": INHERITED_FROM_STAGE,
        "integrity_statement": statement,
        "integrity_scope": scope,
        "integrity_category": integrity_category,
        "integrity_reference_scope": "source_governance_metadata_only",
        "metadata_only_disposition": CROSS_LAYER_VALIDATION_STATUS,
        "forbidden_validation_execution_scope": forbidden_scope,
        "required": True,
        "metadata_only": True,
        "cross_layer_integrity_metadata_required": True,
        "validator_active": False,
        "cross_layer_validation_executed": False,
        "cross_layer_repair_performed": False,
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
    record["integrity_hash"] = _integrity_hash(record)
    record["integrity_record_hash"] = _integrity_record_hash(record)
    return _detached_json_value(record)


def _build_sections(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "upstream_source_audit_replay_engine_input_section": all(
            (
                conditions["upstream_pass"],
                conditions["upstream_hash_present"],
                conditions["upstream_hash_stable"],
                conditions["upstream_handoff_ready"],
                safety_clear,
            )
        ),
        "cross_layer_integrity_validator_metadata_section": True,
        "cross_layer_integrity_record_completeness_section": conditions[
            "records_complete"
        ],
        "cross_layer_integrity_record_hash_stability_section": conditions[
            "records_hash_stable"
        ],
        "no_cross_layer_validation_execution_section": safety_clear,
        "no_cross_layer_repair_or_mutation_section": safety_clear,
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
        "civilization_core_stability_index_next_stage_section": True,
    }
    for record in records:
        values[f"{record['integrity_record_id']}_section"] = (
            record["integrity_record_status"] == "registered_metadata_only"
            and record["cross_layer_integrity_metadata_required"] is True
            and record["metadata_only"] is True
            and record["validator_active"] is False
            and record["cross_layer_validation_executed"] is False
            and record["cross_layer_repair_performed"] is False
        )
    return [
        _status_item("section", name, values[name])
        for name in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_SECTION_NAMES
    ]


def _build_contracts(
    conditions: Mapping[str, bool],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values = {
        "cross_layer_integrity_validator_only_contract": True,
        "cross_layer_integrity_validator_metadata_only_contract": True,
        "upstream_source_audit_replay_engine_pass_contract": conditions[
            "upstream_pass"
        ],
        "upstream_source_audit_replay_engine_hash_present_contract": (
            conditions["upstream_hash_present"]
        ),
        "upstream_source_audit_replay_engine_hash_stable_contract": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_cross_layer_integrity_validator_handoff_contract": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_audit_replay_engine_safety_contract": (
            safety_clear
        ),
        "cross_layer_integrity_records_complete_contract": conditions[
            "records_complete"
        ],
        "cross_layer_integrity_records_metadata_only_contract": conditions[
            "records_metadata_only"
        ],
        "cross_layer_integrity_records_no_execution_contract": conditions[
            "records_no_execution"
        ],
        "cross_layer_integrity_records_hash_stable_contract": conditions[
            "records_hash_stable"
        ],
        "no_cross_layer_validation_execution_contract": safety_clear,
        "no_cross_layer_repair_contract": safety_clear,
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
        "ready_for_civilization_core_stability_index_design_contract": True,
    }
    return [
        _status_item("contract", name, values[name])
        for name in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CONTRACT_NAMES
    ]


def _build_checks(
    conditions: Mapping[str, bool],
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    safety_clear = _safety_clear(conditions)
    values: dict[str, bool] = {
        "cross_layer_integrity_validator_stage_check": True,
        "cross_layer_integrity_validator_mode_check": True,
        "upstream_source_audit_replay_engine_pass_check": conditions[
            "upstream_pass"
        ],
        "upstream_source_audit_replay_engine_hash_present_check": (
            conditions["upstream_hash_present"]
        ),
        "upstream_source_audit_replay_engine_hash_stable_check": (
            conditions["upstream_hash_stable"]
        ),
        "upstream_cross_layer_integrity_validator_handoff_check": conditions[
            "upstream_handoff_ready"
        ],
        "upstream_source_audit_replay_engine_safety_check": safety_clear,
        "cross_layer_integrity_record_ids_complete_check": conditions[
            "records_complete"
        ],
        "cross_layer_integrity_records_metadata_only_check": conditions[
            "records_metadata_only"
        ],
        "cross_layer_integrity_records_no_execution_check": conditions[
            "records_no_execution"
        ],
        "cross_layer_integrity_records_hash_stable_check": conditions[
            "records_hash_stable"
        ],
        "cross_layer_integrity_sections_pass_check": conditions["sections_pass"],
        "cross_layer_integrity_contracts_pass_check": conditions[
            "contracts_pass"
        ],
        "no_cross_layer_validation_execution_check": safety_clear,
        "no_cross_layer_repair_check": safety_clear,
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
        "deterministic_cross_layer_integrity_validator_hash_check": True,
        "ready_for_civilization_core_stability_index_design_check": True,
    }
    for record in records:
        values[f"{record['integrity_record_id']}_check"] = (
            record["integrity_record_status"] == "registered_metadata_only"
            and record["blocking_reasons"] == []
        )
    return [
        _status_item("check", name, values[name])
        for name in REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_CHECK_NAMES
    ]


def _build_summary(
    status: str,
    records: list[dict[str, Any]],
    sections: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "summary_type": "cross_layer_integrity_validator_summary",
        "summary_status": status,
        "roadmap_layer": INTRODUCED_IN_LAYER,
        "roadmap_stage": CROSS_LAYER_INTEGRITY_VALIDATOR_STAGE,
        "current_stage_title": "Cross-Layer Integrity Validator",
        "required_integrity_record_count": len(
            REQUIRED_GOVERNANCE_CROSS_LAYER_INTEGRITY_VALIDATOR_RECORD_IDS
        ),
        "observed_integrity_record_count": len(records),
        "registered_metadata_only_record_count": sum(
            record["integrity_record_status"] == "registered_metadata_only"
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
        "cross_layer_integrity_validator_mode": CROSS_LAYER_INTEGRITY_VALIDATOR_MODE,
        "cross_layer_integrity_validator_candidate_status": (
            CROSS_LAYER_INTEGRITY_VALIDATOR_STATUS
        ),
        "cross_layer_integrity_validator_active_status": (
            CROSS_LAYER_INTEGRITY_VALIDATOR_ACTIVE_STATUS
        ),
        "cross_layer_validation_status": CROSS_LAYER_VALIDATION_STATUS,
        "cross_layer_validation_execution_status": (
            CROSS_LAYER_VALIDATION_EXECUTION_STATUS
        ),
        "cross_layer_repair_status": CROSS_LAYER_REPAIR_STATUS,
        "audit_replay_execution_status": AUDIT_REPLAY_EXECUTION_STATUS,
        "audit_log_write_status": AUDIT_LOG_WRITE_STATUS,
        "ledger_write_status": LEDGER_WRITE_STATUS,
        "policy_enforcement_status": POLICY_ENFORCEMENT_STATUS,
        "human_approval_status": HUMAN_APPROVAL_STATUS,
        "human_authorization_status": HUMAN_AUTHORIZATION_STATUS,
        "source_mutation_status": SOURCE_MUTATION_STATUS,
        "handoff_status": (
            V6_13_HANDOFF_STATUS if status == "pass" else BLOCKED_HANDOFF_STATUS
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
        f"{kind}_type": f"cross_layer_integrity_validator_{kind}",
        "expected": True,
        "observed": bool(condition),
        status_key: "pass" if condition else "blocked",
        "blocking_reasons": [] if condition else [f"{name} blocked"],
        **_disabled_payload(),
    }


def _unknown_record(record_id: str) -> dict[str, Any]:
    return {
        "integrity_record_id": record_id,
        "integrity_record_name": "unknown_cross_layer_integrity_validator_record",
        "integrity_record_status": "blocked",
        "known_record": False,
        "blocking_reasons": [f"{record_id} is not a known integrity record"],
        **_disabled_payload(),
    }


def _unknown_item(kind: str, name: str) -> dict[str, Any]:
    return {
        f"{kind}_name": name,
        f"{kind}_type": f"unknown_cross_layer_integrity_validator_{kind}",
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


def _integrity_hash(record: Mapping[str, Any]) -> str:
    fields = (
        "integrity_record_id",
        "integrity_record_name",
        "integrity_record_category",
        "introduced_in_version",
        "introduced_in_stage",
        "introduced_in_layer",
        "inherited_from_stage",
        "integrity_statement",
        "integrity_scope",
        "integrity_category",
        "integrity_reference_scope",
        "metadata_only_disposition",
        "forbidden_validation_execution_scope",
    )
    return _sha256_json({field: record.get(field) for field in fields})


def _integrity_record_hash(record: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in record.items()
            if key != "integrity_record_hash"
        }
    )


def _cross_layer_integrity_validator_hash(result: Mapping[str, Any]) -> str:
    return _sha256_json(
        {
            key: value
            for key, value in result.items()
            if key != "deterministic_cross_layer_integrity_validator_hash"
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
