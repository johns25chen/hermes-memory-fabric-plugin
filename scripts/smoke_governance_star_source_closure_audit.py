#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_star_source_closure_audit import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS,
    SAFETY_BOUNDARIES,
    build_governance_star_source_closure_audit,
)


REQUIRED_FALSE_RECORD_FLAGS = (
    "star_source_closure_audit_active",
    "star_source_closure_executed",
    "source_handoff_migration_performed",
    "source_handoff_export_performed",
    "source_handoff_import_performed",
    "memory_or_source_migration_performed",
    "stability_index_executed",
    "stability_score_runtime_created",
    "stability_monitoring_performed",
    "cross_layer_validation_executed",
    "cross_layer_repair_performed",
    "audit_replay_executed",
    "audit_log_written",
    "ledger_write_performed",
    "operation_ledger_entry_written",
    "human_approval_performed",
    "human_authorization_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "adapter_dispatched",
    "manifest_dispatched",
    "autonomous_authority_claim_allowed",
    "self_authorization_allowed",
    "identity_escalation_allowed",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
)


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in (*COMMON_DISABLED_FLAGS, *SAFETY_BOUNDARIES):
            if key in value and value[key] is not False:
                raise AssertionError(key)
        for nested in value.values():
            _assert_safety(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_safety(nested)


def main() -> int:
    try:
        first = build_governance_star_source_closure_audit()
        second = build_governance_star_source_closure_audit()
        if first != second:
            raise AssertionError("build stability")

        expected = {
            "version": "6.15.0",
            "star_source_closure_audit_status": "pass",
            "star_source_closure_audit_stage": (
                "v6.15_star_source_closure_audit"
            ),
            "star_source_closure_audit_mode": (
                "star_source_closure_audit_only"
            ),
            "star_source_closure_audit_candidate_status": (
                "star_source_closure_audit_candidate_only"
            ),
            "star_source_closure_audit_active_status": "not_active",
            "closure_audit_status": "metadata_only",
            "source_handoff_execution_status": "not_performed",
            "source_handoff_migration_status": "not_performed",
            "source_handoff_export_status": "not_performed",
            "source_handoff_import_status": "not_performed",
            "memory_or_source_migration_status": "not_performed",
            "stability_index_execution_status": "not_performed",
            "stability_score_runtime_status": "not_performed",
            "stability_monitoring_status": "not_performed",
            "cross_layer_validation_execution_status": "not_performed",
            "cross_layer_repair_status": "not_performed",
            "audit_replay_execution_status": "not_performed",
            "audit_log_write_status": "not_performed",
            "ledger_write_status": "not_performed",
            "policy_enforcement_status": "not_performed",
            "human_approval_status": "not_performed",
            "human_authorization_status": "not_performed",
            "source_mutation_approval_status": "not_active",
            "source_mutation_rejection_status": "not_active",
            "source_mutation_runtime_status": "not_active",
            "source_mutation_execution_status": "not_active",
            "source_mutation_status": "not_performed",
            "star_source_memory_active_status": "not_active",
            "layer_15_active_status": "not_active",
            "upstream_source_handoff_boundary_status": "pass",
            "upstream_handoff_status": (
                "ready_for_star_source_closure_audit_design"
            ),
            "upstream_next_stage": "v6.15_star_source_closure_audit",
            "upstream_next_stage_title": "Star-Source Closure Audit",
            "handoff_status": "ready_for_civilization_core_stable_kernel_design",
            "next_stage": "v6.16_civilization_core_stable_kernel",
            "next_stage_title": "Civilization Core Stable Kernel",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_source_handoff_boundary_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second[
            "upstream_source_handoff_boundary_hash"
        ]:
            raise AssertionError("upstream hash stability")

        records = first["star_source_closure_audit_records"]
        if [record["closure_record_id"] for record in records] != list(
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS
        ):
            raise AssertionError("record ids")
        for record in records:
            if record["closure_record_status"] != "registered_metadata_only":
                raise AssertionError(record["closure_record_id"])
            if record["metadata_only_disposition"] != "metadata_only":
                raise AssertionError("metadata only disposition")
            if record["star_source_closure_audit_metadata_required"] is not True:
                raise AssertionError("integrity metadata")
            if record["metadata_only"] is not True:
                raise AssertionError("metadata only")
            for field_name in REQUIRED_FALSE_RECORD_FLAGS:
                if record[field_name] is not False:
                    raise AssertionError(field_name)

        for container, status_key in (
            ("star_source_closure_audit_sections", "section_status"),
            ("star_source_closure_audit_contracts", "contract_status"),
            ("star_source_closure_audit_checks", "check_status"),
        ):
            if not all(
                item[status_key] == "pass" and item["blocking_reasons"] == []
                for item in first[container]
            ):
                raise AssertionError(container)

        closure_hash = first["deterministic_star_source_closure_audit_hash"]
        if not isinstance(closure_hash, str) or len(closure_hash) != 64:
            raise AssertionError("integrity hash")
        if closure_hash != second["deterministic_star_source_closure_audit_hash"]:
            raise AssertionError("integrity hash stability")
        json.dumps(first, ensure_ascii=True, sort_keys=True, allow_nan=False)
        _assert_safety(first)
    except AssertionError as exc:
        print(
            f"governance_star_source_closure_audit=failed:{exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_star_source_closure_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
