#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_origin_provenance_ledger import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES,
    REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES,
    REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS,
    REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_origin_provenance_ledger,
    governance_origin_provenance_ledger_to_json,
    list_governance_origin_provenance_check_names,
    list_governance_origin_provenance_contract_names,
    list_governance_origin_provenance_record_ids,
    list_governance_origin_provenance_section_names,
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
        first = build_governance_origin_provenance_ledger()
        second = build_governance_origin_provenance_ledger()
        if first != second:
            raise AssertionError("ledger changed between builds")

        expected = {
            "version": "6.4.0",
            "schema_version": "6.4.0",
            "origin_provenance_ledger_status": "pass",
            "origin_provenance_ledger_stage": (
                "v6.2_origin_provenance_ledger"
            ),
            "origin_provenance_ledger_mode": (
                "origin_provenance_ledger_only"
            ),
            "origin_provenance_mode": "metadata_only",
            "origin_provenance_ledger_candidate_status": (
                "ledger_candidate_only"
            ),
            "origin_provenance_ledger_active_status": "not_active",
            "origin_provenance_ledger_write_status": "not_written",
            "upstream_source_constitution_registry_version": "6.4.0",
            "upstream_source_constitution_registry_status": "pass",
            "upstream_handoff_status": (
                "ready_for_origin_provenance_ledger_design"
            ),
            "upstream_next_stage": "v6.2_origin_provenance_ledger",
            "upstream_next_stage_title": "Origin Provenance Ledger",
            "handoff_status": (
                "ready_for_civilizational_identity_boundary_design"
            ),
            "next_stage": "v6.3_civilizational_identity_boundary",
            "next_stage_title": "Civilizational Identity Boundary",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_source_constitution_registry_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second["upstream_source_constitution_registry_hash"]:
            raise AssertionError("upstream hash stability")

        if list_governance_origin_provenance_record_ids() != list(
            REQUIRED_ORIGIN_PROVENANCE_RECORD_IDS
        ):
            raise AssertionError("record ids")
        if list_governance_origin_provenance_section_names() != list(
            REQUIRED_ORIGIN_PROVENANCE_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_origin_provenance_contract_names() != list(
            REQUIRED_ORIGIN_PROVENANCE_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_origin_provenance_check_names() != list(
            REQUIRED_ORIGIN_PROVENANCE_CHECK_NAMES
        ):
            raise AssertionError("check names")

        for record in first["origin_provenance_records"]:
            if (
                record["provenance_record_status"]
                != "registered_metadata_only"
            ):
                raise AssertionError(record["provenance_record_id"])
            if not record["rule_origin_reason"]:
                raise AssertionError(record["provenance_record_id"])
            if not record["rule_origin_boundary"]:
                raise AssertionError(record["provenance_record_id"])
            if not record["rule_inheritance_path"]:
                raise AssertionError(record["provenance_record_id"])
            if len(record["rule_source_hash"]) != 64:
                raise AssertionError(record["provenance_record_id"])
            if len(record["provenance_record_hash"]) != 64:
                raise AssertionError(record["provenance_record_id"])
            if record["human_review_required_for_change"] is not True:
                raise AssertionError(record["provenance_record_id"])
            if record["source_mutation_proposal_required"] is not True:
                raise AssertionError(record["provenance_record_id"])
            if record["direct_mutation_allowed"] is not False:
                raise AssertionError(record["provenance_record_id"])
            if record["autonomous_override_allowed"] is not False:
                raise AssertionError(record["provenance_record_id"])

        if any(
            item["section_status"] != "pass"
            for item in first["origin_provenance_sections"]
        ):
            raise AssertionError("section status")
        if any(
            item["contract_status"] != "pass"
            for item in first["origin_provenance_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            item["check_status"] != "pass"
            for item in first["origin_provenance_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first["deterministic_origin_provenance_ledger_hash"]
        second_hash = second["deterministic_origin_provenance_ledger_hash"]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if first["blocking_reasons"] != []:
            raise AssertionError("blocking_reasons")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "records": first["origin_provenance_records"],
                "sections": first["origin_provenance_sections"],
                "contracts": first["origin_provenance_contracts"],
                "checks": first["origin_provenance_checks"],
                "summary": first["origin_provenance_summary"],
                "hash": first_hash,
                "json": governance_origin_provenance_ledger_to_json(first),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_origin_provenance_ledger=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
