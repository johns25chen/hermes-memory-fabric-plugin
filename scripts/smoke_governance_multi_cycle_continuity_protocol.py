#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_multi_cycle_continuity_protocol import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES,
    REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES,
    REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS,
    REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_multi_cycle_continuity_protocol,
    governance_multi_cycle_continuity_protocol_to_json,
    list_governance_multi_cycle_continuity_check_names,
    list_governance_multi_cycle_continuity_contract_names,
    list_governance_multi_cycle_continuity_record_ids,
    list_governance_multi_cycle_continuity_section_names,
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

REQUIRED_TRUE_RECORD_FLAGS = (
    "human_review_required",
    "source_mutation_proposal_required_for_change",
    "invariant_validation_required",
    "root_conflict_resolver_required",
    "audit_replay_required",
)

REQUIRED_FALSE_RECORD_FLAGS = (
    "direct_mutation_allowed",
    "autonomous_override_allowed",
    "self_authorization_allowed",
    "continuity_runtime_created",
    "continuity_enforcement_runtime_created",
    "continuity_self_repair_created",
    "continuity_scheduler_created",
    "continuity_runtime_activated",
    "source_graph_created",
    "source_graph_mutated",
    "memory_graph_mutated",
    "persistent_memory_write_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "real_ledger_write_performed",
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
    "continuity_runtime_activation_allowed",
    "continuity_memory_write_allowed",
    "continuity_source_mutation_created",
    "source_mutation_proposal_created",
    "source_mutation_proposal_approved",
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
        first = build_governance_multi_cycle_continuity_protocol()
        second = build_governance_multi_cycle_continuity_protocol()
        if first != second:
            raise AssertionError("protocol changed between builds")

        expected = {
            "version": "6.8.0",
            "schema_version": "6.8.0",
            "multi_cycle_continuity_protocol_status": "pass",
            "multi_cycle_continuity_protocol_stage": (
                "v6.6_multi_cycle_continuity_protocol"
            ),
            "multi_cycle_continuity_protocol_mode": (
                "multi_cycle_continuity_protocol_only"
            ),
            "multi_cycle_continuity_mode": "metadata_only",
            "multi_cycle_continuity_protocol_candidate_status": (
                "protocol_candidate_only"
            ),
            "multi_cycle_continuity_protocol_active_status": "not_active",
            "continuity_runtime_status": "not_active",
            "continuity_enforcement_status": "not_active",
            "continuity_mutation_status": "forbidden_without_human_review",
            "cycle_linking_status": "metadata_only",
            "cycle_recovery_status": "metadata_only",
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
            "upstream_root_governance_conflict_resolver_version": "6.8.0",
            "upstream_root_governance_conflict_resolver_status": "pass",
            "upstream_handoff_status": (
                "ready_for_multi_cycle_continuity_protocol_design"
            ),
            "upstream_next_stage": "v6.6_multi_cycle_continuity_protocol",
            "upstream_next_stage_title": "Multi-Cycle Continuity Protocol",
            "handoff_status": (
                "ready_for_source_mutation_proposal_boundary_design"
            ),
            "next_stage": "v6.7_source_mutation_proposal_boundary",
            "next_stage_title": "Source Mutation Proposal Boundary",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first[
            "upstream_root_governance_conflict_resolver_hash"
        ]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if (
            upstream_hash
            != second["upstream_root_governance_conflict_resolver_hash"]
        ):
            raise AssertionError("upstream hash stability")

        if list_governance_multi_cycle_continuity_record_ids() != list(
            REQUIRED_MULTI_CYCLE_CONTINUITY_RECORD_IDS
        ):
            raise AssertionError("record ids")
        if list_governance_multi_cycle_continuity_section_names() != list(
            REQUIRED_MULTI_CYCLE_CONTINUITY_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_multi_cycle_continuity_contract_names() != list(
            REQUIRED_MULTI_CYCLE_CONTINUITY_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_multi_cycle_continuity_check_names() != list(
            REQUIRED_MULTI_CYCLE_CONTINUITY_CHECK_NAMES
        ):
            raise AssertionError("check names")

        records = first["multi_cycle_continuity_records"]
        if len(records) != 16:
            raise AssertionError("record count")
        for record in records:
            if record["continuity_record_status"] != "registered_metadata_only":
                raise AssertionError(record["continuity_record_id"])
            for required_field in (
                "continuity_statement",
                "continuity_scope",
                "preserved_governance_scope",
                "forbidden_activation_scope",
                "continuity_disposition",
                "continuity_boundary_hash",
                "continuity_record_hash",
            ):
                if not record[required_field]:
                    raise AssertionError(required_field)
            for required_flag in REQUIRED_TRUE_RECORD_FLAGS:
                if record[required_flag] is not True:
                    raise AssertionError(required_flag)
            for forbidden_flag in REQUIRED_FALSE_RECORD_FLAGS:
                if record[forbidden_flag] is not False:
                    raise AssertionError(forbidden_flag)
            if record["blocking_reasons"] != []:
                raise AssertionError(record["continuity_record_id"])

        if not all(
            section["section_status"] == "pass"
            and section["blocking_reasons"] == []
            for section in first["multi_cycle_continuity_sections"]
        ):
            raise AssertionError("sections")
        if not all(
            contract["contract_status"] == "pass"
            and contract["blocking_reasons"] == []
            for contract in first["multi_cycle_continuity_contracts"]
        ):
            raise AssertionError("contracts")
        if not all(
            check["check_status"] == "pass"
            and check["blocking_reasons"] == []
            for check in first["multi_cycle_continuity_checks"]
        ):
            raise AssertionError("checks")

        _assert_safety(first)
        protocol_hash = first[
            "deterministic_multi_cycle_continuity_protocol_hash"
        ]
        if protocol_hash != second[
            "deterministic_multi_cycle_continuity_protocol_hash"
        ]:
            raise AssertionError("protocol hash stability")
        if not isinstance(protocol_hash, str) or len(protocol_hash) != 64:
            raise AssertionError("protocol hash shape")

        _assert_no_sensitive_leak(
            {
                "records": first["multi_cycle_continuity_records"],
                "sections": first["multi_cycle_continuity_sections"],
                "contracts": first["multi_cycle_continuity_contracts"],
                "checks": first["multi_cycle_continuity_checks"],
                "summary": first["multi_cycle_continuity_summary"],
                "json": governance_multi_cycle_continuity_protocol_to_json(
                    first
                ),
            }
        )
    except AssertionError as exc:
        print(
            f"governance_multi_cycle_continuity_protocol=failed:{exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_multi_cycle_continuity_protocol=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
