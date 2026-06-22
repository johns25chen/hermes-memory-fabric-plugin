#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_root_governance_conflict_resolver import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS,
    REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_root_governance_conflict_resolver,
    governance_root_governance_conflict_resolver_to_json,
    list_governance_root_governance_conflict_check_names,
    list_governance_root_governance_conflict_contract_names,
    list_governance_root_governance_conflict_record_ids,
    list_governance_root_governance_conflict_section_names,
)


SENSITIVE_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    '"source_record_payload"',
    '"source_graph_payload"',
    '"source_provenance_payload"',
    '"methodology_inference_payload"',
    '"self_evolution_payload"',
    '"operation_ledger_entry_payload"',
    '"network_target"',
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call_instruction",
    "shell_" + "command",
    "git " + "push",
    "g" + "h api",
)

FORBIDDEN_RECORD_FLAGS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "conflict_runtime_created",
    "conflict_enforcement_runtime_created",
    "conflict_self_repair_created",
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
    "hidden_execution_allowed",
    "real_execution_performed",
    "adapter_dispatched",
    "manifest_dispatched",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "identity_escalation_allowed",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
    "autonomous_authority_claim_allowed",
)

TOP_LEVEL_FALSE_FIELDS = (
    "root_governance_conflict_resolver_active",
    "root_governance_conflict_resolved",
    "root_governance_conflict_resolution_executed",
    "conflict_runtime_created",
    "conflict_enforcement_runtime_created",
    "conflict_self_repair_created",
    "conflict_runtime_activated",
    "conflict_enforcement_runtime_activated",
    "autonomous_mutation_resolver_created",
    "active_conflict_execution_runtime_created",
    "source_rule_mutation_engine_created",
    "source_graph_creation_performed",
    "source_graph_mutation_performed",
    "source_memory_invariant_matrix_active",
    "invariant_runtime_created",
    "invariant_enforcement_runtime_created",
    "invariant_self_repair_created",
    "civilizational_identity_active",
    "identity_activation_claimed",
    "identity_claim_escalated",
    "identity_boundary_mutated",
    "identity_boundary_mutation_without_review",
    "star_source_memory_active",
    "layer_15_active",
    "personhood_claimed",
    "life_claimed",
    "awakening_claimed",
    "legal_subject_claimed",
    "religious_object_claimed",
    "autonomous_authority_claimed",
    "identity_escalated",
    "source_provenance_runtime_created",
    "source_graph_created",
    "source_graph_mutated",
    "real_ledger_write_performed",
    "origin_provenance_ledger_written",
    "operation_ledger_entry_written",
    "methodology_runtime_created",
    "self_evolution_runtime_created",
    "real_execution_performed",
    "adapter_dispatched",
    "manifest_dispatched",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "memory_graph_mutated",
    "review_notification_sent",
    "approval_notification_sent",
    "execution_authorization_created",
    "authorization_surface_created",
    "authorization_token_created",
    "authorization_grant_created",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "identity_escalation_allowed",
    "hidden_execution_allowed",
    "unapproved_mutation_allowed",
)


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_DISABLED_FLAGS:
            if key in value and value[key] is not False:
                raise AssertionError(key)
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                if value.get(key) is not False:
                    raise AssertionError(key)
                if boundaries.get(key) is not False:
                    raise AssertionError(key)
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_no_sensitive_leak(value: object) -> None:
    payload = json.dumps(value, sort_keys=True).lower()
    for term in SENSITIVE_TERMS:
        candidate = term if term.startswith("/") else term.lower()
        if candidate in payload:
            raise AssertionError(term)


def main() -> int:
    try:
        first = build_governance_root_governance_conflict_resolver()
        second = build_governance_root_governance_conflict_resolver()
        if first != second:
            raise AssertionError("resolver changed between builds")

        expected = {
            "version": "6.5.0",
            "schema_version": "6.5.0",
            "root_governance_conflict_resolver_status": "pass",
            "root_governance_conflict_resolver_stage": (
                "v6.5_root_governance_conflict_resolver"
            ),
            "root_governance_conflict_resolver_mode": (
                "root_governance_conflict_resolver_only"
            ),
            "root_governance_conflict_mode": "metadata_only",
            "root_governance_conflict_resolver_candidate_status": (
                "resolver_candidate_only"
            ),
            "root_governance_conflict_resolver_active_status": "not_active",
            "conflict_runtime_status": "not_active",
            "conflict_enforcement_status": "not_active",
            "conflict_mutation_status": "forbidden_without_human_review",
            "star_source_memory_active_status": "not_active",
            "layer_15_active_status": "not_active",
            "source_graph_status": "not_created",
            "source_provenance_runtime_status": "not_active",
            "methodology_reverse_inference_status": "not_active",
            "self_evolution_status": "not_active",
            "personhood_claim_status": "forbidden",
            "life_claim_status": "forbidden",
            "awakening_claim_status": "forbidden",
            "legal_subject_claim_status": "forbidden",
            "religious_object_claim_status": "forbidden",
            "autonomous_authority_status": "forbidden",
            "upstream_source_memory_invariant_matrix_version": "6.5.0",
            "upstream_source_memory_invariant_matrix_status": "pass",
            "upstream_handoff_status": (
                "ready_for_root_governance_conflict_resolver_design"
            ),
            "upstream_next_stage": (
                "v6.5_root_governance_conflict_resolver"
            ),
            "upstream_next_stage_title": "Root Governance Conflict Resolver",
            "handoff_status": (
                "ready_for_multi_cycle_continuity_protocol_design"
            ),
            "next_stage": "v6.6_multi_cycle_continuity_protocol",
            "next_stage_title": "Multi-Cycle Continuity Protocol",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_source_memory_invariant_matrix_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second["upstream_source_memory_invariant_matrix_hash"]:
            raise AssertionError("upstream hash stability")

        if list_governance_root_governance_conflict_record_ids() != list(
            REQUIRED_ROOT_GOVERNANCE_CONFLICT_RECORD_IDS
        ):
            raise AssertionError("record ids")
        if list_governance_root_governance_conflict_section_names() != list(
            REQUIRED_ROOT_GOVERNANCE_CONFLICT_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_root_governance_conflict_contract_names() != list(
            REQUIRED_ROOT_GOVERNANCE_CONFLICT_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_root_governance_conflict_check_names() != list(
            REQUIRED_ROOT_GOVERNANCE_CONFLICT_CHECK_NAMES
        ):
            raise AssertionError("check names")

        for record in first["root_governance_conflict_records"]:
            if record["conflict_record_status"] != "registered_metadata_only":
                raise AssertionError(record["conflict_record_id"])
            for required_field in (
                "conflict_trigger_scope",
                "protected_governance_scope",
                "forbidden_resolution_scope",
                "deterministic_resolution_disposition",
                "conflict_boundary_hash",
                "conflict_record_hash",
            ):
                if not record[required_field]:
                    raise AssertionError(required_field)
            for required_flag in (
                "human_review_required",
                "source_mutation_proposal_required",
                "invariant_validation_required",
                "audit_replay_required",
            ):
                if record[required_flag] is not True:
                    raise AssertionError(required_flag)
            for forbidden_flag in FORBIDDEN_RECORD_FLAGS:
                if record[forbidden_flag] is not False:
                    raise AssertionError(forbidden_flag)
            if record["blocking_reasons"] != []:
                raise AssertionError(record["conflict_record_id"])

        if not all(
            section["section_status"] == "pass"
            and section["blocking_reasons"] == []
            for section in first["root_governance_conflict_sections"]
        ):
            raise AssertionError("sections")
        if not all(
            contract["contract_status"] == "pass"
            and contract["blocking_reasons"] == []
            for contract in first["root_governance_conflict_contracts"]
        ):
            raise AssertionError("contracts")
        if not all(
            check["check_status"] == "pass" and check["blocking_reasons"] == []
            for check in first["root_governance_conflict_checks"]
        ):
            raise AssertionError("checks")

        for field_name in TOP_LEVEL_FALSE_FIELDS:
            if first[field_name] is not False:
                raise AssertionError(field_name)
        _assert_safety(first)

        if (
            first["deterministic_root_governance_conflict_resolver_hash"]
            != second["deterministic_root_governance_conflict_resolver_hash"]
        ):
            raise AssertionError("resolver hash stability")
        if len(first["deterministic_root_governance_conflict_resolver_hash"]) != 64:
            raise AssertionError("resolver hash shape")

        _assert_no_sensitive_leak(
            {
                "records": first["root_governance_conflict_records"],
                "sections": first["root_governance_conflict_sections"],
                "contracts": first["root_governance_conflict_contracts"],
                "checks": first["root_governance_conflict_checks"],
                "summary": first["root_governance_conflict_summary"],
                "json": governance_root_governance_conflict_resolver_to_json(first),
            }
        )
    except AssertionError as exc:
        print(f"governance_root_governance_conflict_resolver=failed:{exc}", file=sys.stderr)
        return 1

    print("governance_root_governance_conflict_resolver=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
