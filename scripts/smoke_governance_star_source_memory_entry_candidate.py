#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_star_source_memory_entry_candidate import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_star_source_memory_entry_candidate,
    governance_star_source_memory_entry_candidate_to_json,
    list_governance_star_source_memory_entry_candidate_check_names,
    list_governance_star_source_memory_entry_candidate_contract_names,
    list_governance_star_source_memory_entry_candidate_section_names,
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
    '"sandbox_runtime_payload"',
    '"sandbox_result_payload"',
    '"rollback_payload"',
    '"quarantine_payload"',
    '"incident_payload"',
    '"audit_log_payload"',
    '"closure_record_payload"',
    '"operation_ledger_entry_payload"',
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
        first = build_governance_star_source_memory_entry_candidate()
        second = build_governance_star_source_memory_entry_candidate()
        if first != second:
            raise AssertionError("candidate changed between builds")

        expected = {
            "version": "6.1.0",
            "schema_version": "6.1.0",
            "star_source_memory_entry_candidate_status": "pass",
            "star_source_memory_entry_candidate_stage": (
                "v6.0_star_source_memory_entry_candidate"
            ),
            "star_source_memory_entry_candidate_mode": (
                "star_source_entry_candidate_only"
            ),
            "star_source_memory_mode": "metadata_only",
            "star_source_entry_status": "entry_candidate_only",
            "star_source_memory_active_status": "not_active",
            "layer_15_entry_status": "entry_candidate_only",
            "source_provenance_status": "not_active",
            "methodology_reverse_inference_status": "not_active",
            "self_evolution_status": "not_active",
            "v6_entry_status": "entry_candidate_only",
            "v6_handoff_acceptance_status": "accepted_as_metadata_only",
            "star_cosmos_closure_handoff_audit_version": "6.1.0",
            "star_cosmos_closure_handoff_audit_status": "pass",
            "handoff_status": "ready_for_source_constitution_registry_design",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["star_cosmos_closure_handoff_audit_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("star_cosmos_closure_handoff_audit_hash")

        metadata = first["star_source_entry_metadata"]
        if (
            metadata["star_source_entry_metadata_type"]
            != "layer_15_star_source_memory_entry_candidate_metadata"
            or metadata["star_source_entry_metadata_mode"] != "metadata_only"
        ):
            raise AssertionError("star_source_entry_metadata")
        if (
            metadata["star_source_entry_next_stage"]
            != "v6.1_source_constitution_registry"
            or metadata["star_source_entry_next_stage_title"]
            != "Source Constitution Registry"
            or metadata["star_source_entry_handoff_status"]
            != "ready_for_source_constitution_registry_design"
        ):
            raise AssertionError("star_source_entry_next_stage")
        for key in (
            "source_provenance_entry_metadata",
            "methodology_reverse_inference_entry_metadata",
            "self_evolution_entry_metadata",
        ):
            if first[key]["entry_metadata_mode"] != "metadata_only":
                raise AssertionError(key)

        if list_governance_star_source_memory_entry_candidate_section_names() != list(
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_star_source_memory_entry_candidate_contract_names() != list(
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_star_source_memory_entry_candidate_check_names() != list(
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if any(
            item["section_status"] != "pass"
            for item in first["star_source_entry_sections"]
        ):
            raise AssertionError("section status")
        if any(
            item["contract_status"] != "pass"
            for item in first["star_source_entry_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            item["check_status"] != "pass"
            for item in first["star_source_entry_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first[
            "deterministic_star_source_memory_entry_candidate_hash"
        ]
        second_hash = second[
            "deterministic_star_source_memory_entry_candidate_hash"
        ]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if first["blocking_reasons"] != []:
            raise AssertionError("blocking_reasons")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "provenance": first["source_provenance_entry_metadata"],
                "methodology": first[
                    "methodology_reverse_inference_entry_metadata"
                ],
                "evolution": first["self_evolution_entry_metadata"],
                "sections": first["star_source_entry_sections"],
                "contracts": first["star_source_entry_contracts"],
                "checks": first["star_source_entry_checks"],
                "summary": first["star_source_entry_summary"],
                "hash": first_hash,
                "json": governance_star_source_memory_entry_candidate_to_json(
                    first
                ),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_star_source_memory_entry_candidate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
