#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_star_cosmos_closure_handoff_audit import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    build_governance_star_cosmos_closure_handoff_audit,
    governance_star_cosmos_closure_handoff_audit_to_json,
    list_governance_star_cosmos_closure_handoff_audit_check_names,
    list_governance_star_cosmos_closure_handoff_audit_contract_names,
    list_governance_star_cosmos_closure_handoff_audit_section_names,
)


SENSITIVE_BLOCKED_TERMS = (
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
    '"sandbox_runtime_payload"',
    '"sandbox_result_payload"',
    '"rollback_payload"',
    '"quarantine_payload"',
    '"incident_payload"',
    '"audit_log_payload"',
    '"closure_record_payload"',
    '"source_provenance_payload"',
    '"source_evolution_payload"',
    '"source_graph_mutation_payload"',
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
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
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
    lowered = json.dumps(value, sort_keys=True).lower()
    for blocked in SENSITIVE_BLOCKED_TERMS:
        candidate = blocked if blocked.startswith("/") else blocked.lower()
        if candidate in lowered:
            raise AssertionError(blocked)


def main() -> int:
    try:
        first = build_governance_star_cosmos_closure_handoff_audit()
        second = build_governance_star_cosmos_closure_handoff_audit()
        if first != second:
            raise AssertionError("audit changed between builds")

        expected_top_level = {
            "version": "6.1.0",
            "schema_version": "6.1.0",
            "star_cosmos_closure_handoff_audit_status": "pass",
            "star_cosmos_closure_handoff_audit_stage": (
                "v5.13_star_cosmos_closure_handoff_audit"
            ),
            "star_cosmos_closure_handoff_audit_mode": (
                "star_cosmos_closure_handoff_audit_only"
            ),
            "star_cosmos_closure_mode": "metadata_only",
            "star_cosmos_closure_status": "closure_candidate_only",
            "layer_14_closure_status": "closure_candidate_only",
            "v6_handoff_status": (
                "ready_for_star_source_entry_candidate_design"
            ),
            "star_source_entry_status": "not_entered",
            "star_source_memory_active_status": "not_active",
            "star_cosmos_entry_status": "candidate_only",
            "post_sandbox_review_boundary_version": "6.1.0",
            "post_sandbox_review_boundary_status": "pass",
            "star_cosmos_closure_handoff_status": (
                "ready_for_v6_star_source_entry_candidate_design"
            ),
            "handoff_status": "ready_for_v6_star_source_entry_candidate_design",
        }
        for key, expected in expected_top_level.items():
            if first[key] != expected:
                raise AssertionError(key)

        if len(first["post_sandbox_review_boundary_hash"]) != 64:
            raise AssertionError("post_sandbox_review_boundary_hash")
        metadata = first["star_cosmos_closure_metadata"]
        if (
            metadata["star_cosmos_closure_metadata_type"]
            != "layer_14_star_cosmos_closure_handoff_audit_metadata"
        ):
            raise AssertionError("star_cosmos_closure_metadata_type")
        if metadata["star_cosmos_closure_metadata_mode"] != "metadata_only":
            raise AssertionError("star_cosmos_closure_metadata_mode")

        inventory = first["v5_layer_stack_closure_inventory"]
        if len(inventory) != 13:
            raise AssertionError("inventory count")
        for item in inventory:
            if item["layer_stage_status"] != "sealed_metadata_boundary":
                raise AssertionError("layer_stage_status")
            if item["layer_stage_execution_status"] != "no_execution":
                raise AssertionError("layer_stage_execution_status")

        if list_governance_star_cosmos_closure_handoff_audit_section_names() != list(
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES
        ):
            raise AssertionError("section names")
        if list_governance_star_cosmos_closure_handoff_audit_contract_names() != list(
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES
        ):
            raise AssertionError("contract names")
        if list_governance_star_cosmos_closure_handoff_audit_check_names() != list(
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES
        ):
            raise AssertionError("check names")

        if any(
            item["section_status"] != "pass"
            for item in first["star_cosmos_closure_sections"]
        ):
            raise AssertionError("section status")
        if any(
            item["contract_status"] != "pass"
            for item in first["star_cosmos_closure_contracts"]
        ):
            raise AssertionError("contract status")
        if any(
            item["check_status"] != "pass"
            for item in first["star_cosmos_closure_checks"]
        ):
            raise AssertionError("check status")

        first_hash = first[
            "deterministic_star_cosmos_closure_handoff_audit_hash"
        ]
        second_hash = second[
            "deterministic_star_cosmos_closure_handoff_audit_hash"
        ]
        if first_hash != second_hash or len(first_hash) != 64:
            raise AssertionError("deterministic hash")
        if first["blocking_reasons"] != []:
            raise AssertionError("blocking_reasons")

        _assert_safety(first)
        _assert_no_sensitive_leak(
            {
                "metadata": metadata,
                "inventory": inventory,
                "sections": first["star_cosmos_closure_sections"],
                "contracts": first["star_cosmos_closure_contracts"],
                "checks": first["star_cosmos_closure_checks"],
                "summary": first["star_cosmos_closure_summary"],
                "hash": first_hash,
                "json": governance_star_cosmos_closure_handoff_audit_to_json(
                    first
                ),
            }
        )
    except (AssertionError, KeyError, TypeError, ValueError):
        return 1

    print("governance_star_cosmos_closure_handoff_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
