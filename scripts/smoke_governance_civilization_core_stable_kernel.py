#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_civilization_core_stable_kernel import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS,
    SAFETY_BOUNDARIES,
    build_governance_civilization_core_stable_kernel,
)


REQUIRED_FALSE_RECORD_FLAGS = (
    "civilization_core_stable_kernel_active",
    "stable_kernel_activated",
    "stable_kernel_runtime_created",
    "kernel_execution_performed",
    "system_finalization_performed",
    "final_autonomy_created",
    "final_authority_created",
    "closure_audit_executed",
    "closure_decision_performed",
    "finalization_performed",
    "source_handoff_executed",
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
        first = build_governance_civilization_core_stable_kernel()
        second = build_governance_civilization_core_stable_kernel()
        if first != second:
            raise AssertionError("build stability")

        expected = {
            "version": "6.16.0",
            "civilization_core_stable_kernel_status": "pass",
            "civilization_core_stable_kernel_stage": (
                "v6.16_civilization_core_stable_kernel"
            ),
            "civilization_core_stable_kernel_mode": (
                "civilization_core_stable_kernel_design_only"
            ),
            "civilization_core_stable_kernel_candidate_status": (
                "civilization_core_stable_kernel_candidate_only"
            ),
            "civilization_core_stable_kernel_active_status": "not_active",
            "stable_kernel_status": "metadata_only",
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
            "stable_kernel_activation_status": "not_performed",
            "stable_kernel_runtime_status": "not_performed",
            "kernel_execution_status": "not_performed",
            "system_finalization_status": "not_performed",
            "final_autonomy_status": "not_active",
            "final_authority_status": "not_active",
            "closure_audit_execution_status": "not_performed",
            "closure_decision_status": "not_performed",
            "finalization_status": "not_performed",
            "upstream_star_source_closure_audit_status": "pass",
            "upstream_handoff_status": (
                "ready_for_civilization_core_stable_kernel_design"
            ),
            "upstream_next_stage": "v6.16_civilization_core_stable_kernel",
            "upstream_next_stage_title": "Civilization Core Stable Kernel",
            "handoff_status": "v6_series_terminal_boundary_ready",
            "next_stage": "v6_series_terminal_boundary",
            "next_stage_title": "V6 Series Terminal Boundary",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first["upstream_star_source_closure_audit_hash"]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second[
            "upstream_star_source_closure_audit_hash"
        ]:
            raise AssertionError("upstream hash stability")

        records = first["civilization_core_stable_kernel_records"]
        if [record["kernel_record_id"] for record in records] != list(
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS
        ):
            raise AssertionError("record ids")
        for record in records:
            if record["kernel_record_status"] != "registered_metadata_only":
                raise AssertionError(record["kernel_record_id"])
            if record["metadata_only_disposition"] != "metadata_only":
                raise AssertionError("metadata only disposition")
            if record["civilization_core_stable_kernel_metadata_required"] is not True:
                raise AssertionError("integrity metadata")
            if record["metadata_only"] is not True:
                raise AssertionError("metadata only")
            for field_name in REQUIRED_FALSE_RECORD_FLAGS:
                if record[field_name] is not False:
                    raise AssertionError(field_name)

        for container, status_key in (
            ("civilization_core_stable_kernel_sections", "section_status"),
            ("civilization_core_stable_kernel_contracts", "contract_status"),
            ("civilization_core_stable_kernel_checks", "check_status"),
        ):
            if not all(
                item[status_key] == "pass" and item["blocking_reasons"] == []
                for item in first[container]
            ):
                raise AssertionError(container)

        kernel_hash = first["deterministic_civilization_core_stable_kernel_hash"]
        if not isinstance(kernel_hash, str) or len(kernel_hash) != 64:
            raise AssertionError("integrity hash")
        if kernel_hash != second["deterministic_civilization_core_stable_kernel_hash"]:
            raise AssertionError("integrity hash stability")
        json.dumps(first, ensure_ascii=True, sort_keys=True, allow_nan=False)
        _assert_safety(first)
    except AssertionError as exc:
        print(
            f"governance_civilization_core_stable_kernel=failed:{exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_civilization_core_stable_kernel=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
