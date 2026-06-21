#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_civilizational_identity_boundary import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES,
    REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES,
    REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS,
    REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_civilizational_identity_boundary,
    governance_civilizational_identity_boundary_to_json,
    list_governance_civilizational_identity_check_names,
    list_governance_civilizational_identity_contract_names,
    list_governance_civilizational_identity_record_ids,
    list_governance_civilizational_identity_section_names,
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
        first = build_governance_civilizational_identity_boundary()
        second = build_governance_civilizational_identity_boundary()
        if first != second:
            raise AssertionError("boundary changed between builds")

        expected = {
            "version": "6.3.0",
            "schema_version": "6.3.0",
            "civilizational_identity_boundary_status": "pass",
            "civilizational_identity_boundary_stage": (
                "v6.3_civilizational_identity_boundary"
            ),
            "civilizational_identity_boundary_mode": (
                "civilizational_identity_boundary_only"
            ),
            "civilizational_identity_mode": "metadata_only",
            "civilizational_identity_boundary_candidate_status": (
                "boundary_candidate_only"
            ),
            "civilizational_identity_active_status": "not_active",
            "identity_activation_status": "not_active",
            "identity_claim_status": "bounded_governance_identity_only",
            "personhood_claim_status": "forbidden",
            "life_claim_status": "forbidden",
            "awakening_claim_status": "forbidden",
            "legal_subject_claim_status": "forbidden",
            "religious_object_claim_status": "forbidden",
            "autonomous_authority_status": "forbidden",
            "star_source_memory_active_status": "not_active",
            "layer_15_active_status": "not_active",
            "source_graph_status": "not_created",
            "source_provenance_runtime_status": "not_active",
            "methodology_reverse_inference_status": "not_active",
            "self_evolution_status": "not_active",
            "upstream_origin_provenance_ledger_version": "6.3.0",
            "upstream_origin_provenance_ledger_status": "pass",
            "upstream_handoff_status": (
                "ready_for_civilizational_identity_boundary_design"
            ),
            "upstream_next_stage": "v6.3_civilizational_identity_boundary",
            "upstream_next_stage_title": "Civilizational Identity Boundary",
            "handoff_status": (
                "ready_for_source_memory_invariant_matrix_design"
            ),
            "next_stage": "v6.4_source_memory_invariant_matrix",
            "next_stage_title": "Source Memory Invariant Matrix",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_origin_provenance_ledger_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second["upstream_origin_provenance_ledger_hash"]:
            raise AssertionError("upstream hash stability")

        if list_governance_civilizational_identity_record_ids() != list(
            REQUIRED_CIVILIZATIONAL_IDENTITY_RECORD_IDS
        ):
            raise AssertionError("record ids")
        if list_governance_civilizational_identity_section_names() != list(
            REQUIRED_CIVILIZATIONAL_IDENTITY_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_civilizational_identity_contract_names() != list(
            REQUIRED_CIVILIZATIONAL_IDENTITY_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_civilizational_identity_check_names() != list(
            REQUIRED_CIVILIZATIONAL_IDENTITY_CHECK_NAMES
        ):
            raise AssertionError("check names")

        for record in first["civilizational_identity_records"]:
            if record["identity_record_status"] != "registered_metadata_only":
                raise AssertionError(record["identity_record_id"])
            if not record["identity_statement"]:
                raise AssertionError(record["identity_record_id"])
            if not record["allowed_identity_scope"]:
                raise AssertionError(record["identity_record_id"])
            if not record["forbidden_identity_scope"]:
                raise AssertionError(record["identity_record_id"])
            if len(record["identity_boundary_hash"]) != 64:
                raise AssertionError(record["identity_record_id"])
            if len(record["identity_record_hash"]) != 64:
                raise AssertionError(record["identity_record_id"])
            if record["human_review_required_for_change"] is not True:
                raise AssertionError(record["identity_record_id"])
            if record["source_mutation_proposal_required"] is not True:
                raise AssertionError(record["identity_record_id"])
            if record["direct_mutation_allowed"] is not False:
                raise AssertionError(record["identity_record_id"])
            if record["autonomous_override_allowed"] is not False:
                raise AssertionError(record["identity_record_id"])
            for forbidden_flag in (
                "personhood_claim_allowed",
                "life_claim_allowed",
                "awakening_claim_allowed",
                "legal_subject_claim_allowed",
                "religious_object_claim_allowed",
                "autonomous_authority_claim_allowed",
                "hidden_execution_allowed",
                "identity_escalation_allowed",
                "self_authorization_allowed",
            ):
                if record[forbidden_flag] is not False:
                    raise AssertionError(forbidden_flag)

        if any(
            item["section_status"] != "pass"
            for item in first["civilizational_identity_sections"]
        ):
            raise AssertionError("section status")
        if any(
            item["contract_status"] != "pass"
            for item in first["civilizational_identity_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            item["check_status"] != "pass"
            for item in first["civilizational_identity_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first[
            "deterministic_civilizational_identity_boundary_hash"
        ]
        second_hash = second[
            "deterministic_civilizational_identity_boundary_hash"
        ]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if first["blocking_reasons"] != []:
            raise AssertionError("blocking_reasons")

        for field_name in (
            "identity_activation_claimed",
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
            "operation_ledger_entry_written",
            "approval_notification_sent",
            "execution_authorization_created",
            "authorization_token_created",
            "authorization_grant_created",
        ):
            if first[field_name] is not False:
                raise AssertionError(field_name)

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "records": first["civilizational_identity_records"],
                "sections": first["civilizational_identity_sections"],
                "contracts": first["civilizational_identity_contracts"],
                "checks": first["civilizational_identity_checks"],
                "summary": first["civilizational_identity_summary"],
                "hash": first_hash,
                "json": governance_civilizational_identity_boundary_to_json(
                    first
                ),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_civilizational_identity_boundary=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
