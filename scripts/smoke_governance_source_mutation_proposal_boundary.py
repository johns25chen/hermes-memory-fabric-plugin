#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_source_mutation_proposal_boundary import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CHECK_NAMES,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CONTRACT_NAMES,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS,
    REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_source_mutation_proposal_boundary,
    governance_source_mutation_proposal_boundary_to_json,
    list_governance_source_mutation_proposal_boundary_check_names,
    list_governance_source_mutation_proposal_boundary_contract_names,
    list_governance_source_mutation_proposal_boundary_record_ids,
    list_governance_source_mutation_proposal_boundary_section_names,
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
    "required",
    "human_review_required",
    "source_mutation_review_gate_required",
    "source_constitution_alignment_required",
    "origin_provenance_preservation_required",
    "civilizational_identity_boundary_required",
    "source_memory_invariant_validation_required",
    "root_governance_conflict_resolution_required",
    "multi_cycle_continuity_required",
    "audit_replay_required",
    "proposal_metadata_only",
)

REQUIRED_FALSE_RECORD_FLAGS = (
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
    "proposal_auto_creation_allowed",
    "proposal_auto_approval_allowed",
    "proposal_runtime_activation_allowed",
    "proposal_memory_write_allowed",
    "proposal_source_graph_mutation_allowed",
    "proposal_memory_graph_mutation_allowed",
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
        first = build_governance_source_mutation_proposal_boundary()
        second = build_governance_source_mutation_proposal_boundary()
        if first != second:
            raise AssertionError("boundary changed between builds")

        expected = {
            "version": "6.9.0",
            "schema_version": "6.9.0",
            "source_mutation_proposal_boundary_status": "pass",
            "source_mutation_proposal_boundary_stage": (
                "v6.7_source_mutation_proposal_boundary"
            ),
            "source_mutation_proposal_boundary_mode": (
                "source_mutation_proposal_boundary_only"
            ),
            "source_mutation_proposal_mode": "metadata_only",
            "source_mutation_proposal_boundary_candidate_status": (
                "proposal_boundary_candidate_only"
            ),
            "source_mutation_proposal_boundary_active_status": "not_active",
            "source_mutation_runtime_status": "not_active",
            "source_mutation_execution_status": "not_active",
            "source_mutation_proposal_creation_status": "not_active",
            "source_mutation_proposal_approval_status": "not_active",
            "source_mutation_review_status": "not_active",
            "source_mutation_review_gate_status": "not_active",
            "source_mutation_status": "not_performed",
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
            "upstream_multi_cycle_continuity_protocol_version": "6.9.0",
            "upstream_multi_cycle_continuity_protocol_status": "pass",
            "upstream_handoff_status": (
                "ready_for_source_mutation_proposal_boundary_design"
            ),
            "upstream_next_stage": "v6.7_source_mutation_proposal_boundary",
            "upstream_next_stage_title": "Source Mutation Proposal Boundary",
            "handoff_status": "ready_for_source_mutation_review_gate_design",
            "next_stage": "v6.8_source_mutation_review_gate",
            "next_stage_title": "Source Mutation Review Gate",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_multi_cycle_continuity_protocol_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second[
            "upstream_multi_cycle_continuity_protocol_hash"
        ]:
            raise AssertionError("upstream hash stability")

        stable_lists = (
            (
                list_governance_source_mutation_proposal_boundary_record_ids(),
                REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_RECORD_IDS,
            ),
            (
                list_governance_source_mutation_proposal_boundary_section_names(),
                REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_SECTION_NAMES,
            ),
            (
                list_governance_source_mutation_proposal_boundary_contract_names(),
                REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CONTRACT_NAMES,
            ),
            (
                list_governance_source_mutation_proposal_boundary_check_names(),
                REQUIRED_SOURCE_MUTATION_PROPOSAL_BOUNDARY_CHECK_NAMES,
            ),
        )
        for observed, required in stable_lists:
            if observed != list(required):
                raise AssertionError("stable registry")

        records = first["source_mutation_proposal_boundary_records"]
        if len(records) != 16:
            raise AssertionError("record count")
        for record in records:
            if record["proposal_boundary_record_status"] != (
                "registered_metadata_only"
            ):
                raise AssertionError(record["proposal_boundary_record_id"])
            for required_field in (
                "proposal_boundary_statement",
                "proposal_boundary_scope",
                "required_proposal_metadata_scope",
                "forbidden_proposal_activation_scope",
                "proposal_boundary_disposition",
                "proposal_boundary_hash",
                "proposal_boundary_record_hash",
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
                raise AssertionError(record["proposal_boundary_record_id"])

        for container, status_key in (
            ("source_mutation_proposal_boundary_sections", "section_status"),
            ("source_mutation_proposal_boundary_contracts", "contract_status"),
            ("source_mutation_proposal_boundary_checks", "check_status"),
        ):
            if not all(
                item[status_key] == "pass" and item["blocking_reasons"] == []
                for item in first[container]
            ):
                raise AssertionError(container)

        _assert_safety(first)
        boundary_hash = first[
            "deterministic_source_mutation_proposal_boundary_hash"
        ]
        if boundary_hash != second[
            "deterministic_source_mutation_proposal_boundary_hash"
        ]:
            raise AssertionError("boundary hash stability")
        if not isinstance(boundary_hash, str) or len(boundary_hash) != 64:
            raise AssertionError("boundary hash shape")

        _assert_no_sensitive_leak(
            {
                "records": first["source_mutation_proposal_boundary_records"],
                "sections": first["source_mutation_proposal_boundary_sections"],
                "contracts": first[
                    "source_mutation_proposal_boundary_contracts"
                ],
                "checks": first["source_mutation_proposal_boundary_checks"],
                "summary": first["source_mutation_proposal_boundary_summary"],
                "json": governance_source_mutation_proposal_boundary_to_json(
                    first
                ),
            }
        )
    except AssertionError as exc:
        print(
            f"governance_source_mutation_proposal_boundary=failed:{exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_source_mutation_proposal_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
