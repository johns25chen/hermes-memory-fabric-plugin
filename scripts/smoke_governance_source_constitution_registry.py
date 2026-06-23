#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_source_constitution_registry import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES,
    REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES,
    REQUIRED_SOURCE_CONSTITUTION_RULE_IDS,
    REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_source_constitution_registry,
    governance_source_constitution_registry_to_json,
    list_governance_source_constitution_check_names,
    list_governance_source_constitution_contract_names,
    list_governance_source_constitution_rule_ids,
    list_governance_source_constitution_section_names,
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
        first = build_governance_source_constitution_registry()
        second = build_governance_source_constitution_registry()
        if first != second:
            raise AssertionError("registry changed between builds")

        expected = {
            "version": "6.7.0",
            "schema_version": "6.7.0",
            "source_constitution_registry_status": "pass",
            "source_constitution_registry_stage": (
                "v6.1_source_constitution_registry"
            ),
            "source_constitution_registry_mode": (
                "source_constitution_registry_only"
            ),
            "source_constitution_mode": "metadata_only",
            "source_constitution_status": "registry_candidate_only",
            "source_constitution_active_status": "not_active",
            "layer_15_constitution_status": "registry_candidate_only",
            "star_source_memory_active_status": "not_active",
            "source_provenance_status": "not_active",
            "origin_provenance_ledger_status": "not_created",
            "methodology_reverse_inference_status": "not_active",
            "self_evolution_status": "not_active",
            "upstream_star_source_entry_candidate_version": "6.7.0",
            "upstream_star_source_entry_candidate_status": "pass",
            "upstream_handoff_status": (
                "ready_for_source_constitution_registry_design"
            ),
            "handoff_status": "ready_for_origin_provenance_ledger_design",
            "next_stage": "v6.2_origin_provenance_ledger",
            "next_stage_title": "Origin Provenance Ledger",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_star_source_entry_candidate_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second["upstream_star_source_entry_candidate_hash"]:
            raise AssertionError("upstream hash stability")
        if (
            first["upstream_star_source_entry_next_stage"]
            != "v6.1_source_constitution_registry"
            or first["upstream_star_source_entry_next_stage_title"]
            != "Source Constitution Registry"
        ):
            raise AssertionError("upstream next stage")

        if list_governance_source_constitution_rule_ids() != list(
            REQUIRED_SOURCE_CONSTITUTION_RULE_IDS
        ):
            raise AssertionError("rule ids")
        if list_governance_source_constitution_section_names() != list(
            REQUIRED_SOURCE_CONSTITUTION_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_source_constitution_contract_names() != list(
            REQUIRED_SOURCE_CONSTITUTION_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_source_constitution_check_names() != list(
            REQUIRED_SOURCE_CONSTITUTION_CHECK_NAMES
        ):
            raise AssertionError("check names")

        for rule in first["source_constitution_rules"]:
            if rule["rule_status"] != "registered_metadata_only":
                raise AssertionError(rule["rule_id"])
            if rule["human_review_required_for_change"] is not True:
                raise AssertionError(rule["rule_id"])
            if rule["source_mutation_proposal_required"] is not True:
                raise AssertionError(rule["rule_id"])
            if rule["direct_mutation_allowed"] is not False:
                raise AssertionError(rule["rule_id"])
            if rule["autonomous_override_allowed"] is not False:
                raise AssertionError(rule["rule_id"])

        if any(
            item["section_status"] != "pass"
            for item in first["source_constitution_sections"]
        ):
            raise AssertionError("section status")
        if any(
            item["contract_status"] != "pass"
            for item in first["source_constitution_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            item["check_status"] != "pass"
            for item in first["source_constitution_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first["deterministic_source_constitution_registry_hash"]
        second_hash = second["deterministic_source_constitution_registry_hash"]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if first["blocking_reasons"] != []:
            raise AssertionError("blocking_reasons")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "rules": first["source_constitution_rules"],
                "sections": first["source_constitution_sections"],
                "contracts": first["source_constitution_contracts"],
                "checks": first["source_constitution_checks"],
                "summary": first["source_constitution_summary"],
                "hash": first_hash,
                "json": governance_source_constitution_registry_to_json(first),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_source_constitution_registry=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
