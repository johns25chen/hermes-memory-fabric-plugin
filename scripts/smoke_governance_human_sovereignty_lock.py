#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from hermes_memory_fabric.governance_human_sovereignty_lock import (  # noqa: E402
    COMMON_DISABLED_FLAGS,
    REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS,
    SAFETY_BOUNDARIES,
    build_governance_human_sovereignty_lock,
)


REQUIRED_FALSE_RECORD_FLAGS = (
    "lock_active",
    "human_approval_performed",
    "human_authorization_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "operation_ledger_entry_written",
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
        first = build_governance_human_sovereignty_lock()
        second = build_governance_human_sovereignty_lock()
        if first != second:
            raise AssertionError("build stability")

        expected = {
            "version": "6.9.0",
            "human_sovereignty_lock_status": "pass",
            "human_sovereignty_lock_stage": "v6.9_human_sovereignty_lock",
            "human_sovereignty_lock_mode": "human_sovereignty_lock_only",
            "human_sovereignty_lock_candidate_status": "lock_candidate_only",
            "human_sovereignty_lock_active_status": "not_active",
            "human_approval_status": "not_performed",
            "human_authorization_status": "not_performed",
            "source_mutation_approval_status": "not_active",
            "source_mutation_rejection_status": "not_active",
            "source_mutation_runtime_status": "not_active",
            "source_mutation_execution_status": "not_active",
            "source_mutation_status": "not_performed",
            "star_source_memory_active_status": "not_active",
            "layer_15_active_status": "not_active",
            "upstream_source_mutation_review_gate_status": "pass",
            "upstream_handoff_status": (
                "ready_for_human_sovereignty_lock_design"
            ),
            "upstream_next_stage": "v6.9_human_sovereignty_lock",
            "upstream_next_stage_title": "Human Sovereignty Lock",
            "handoff_status": (
                "ready_for_anti_overreach_governance_firewall_design"
            ),
            "next_stage": "v6.10_anti_overreach_governance_firewall",
            "next_stage_title": "Anti-Overreach Governance Firewall",
        }
        for key, expected_value in expected.items():
            if first[key] != expected_value:
                raise AssertionError(key)

        upstream_hash = first[
            "upstream_source_mutation_review_gate_hash"
        ]
        if not isinstance(upstream_hash, str) or len(upstream_hash) != 64:
            raise AssertionError("upstream hash")
        if upstream_hash != second[
            "upstream_source_mutation_review_gate_hash"
        ]:
            raise AssertionError("upstream hash stability")

        records = first["human_sovereignty_lock_records"]
        if [record["lock_record_id"] for record in records] != list(
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS
        ):
            raise AssertionError("record ids")
        for record in records:
            if record["lock_record_status"] != "registered_metadata_only":
                raise AssertionError(record["lock_record_id"])
            if record["human_sovereignty_required"] is not True:
                raise AssertionError("human sovereignty")
            if record["explicit_human_review_required"] is not True:
                raise AssertionError("explicit human review")
            if record["metadata_only"] is not True:
                raise AssertionError("metadata only")
            for field_name in REQUIRED_FALSE_RECORD_FLAGS:
                if record[field_name] is not False:
                    raise AssertionError(field_name)

        for container, status_key in (
            ("human_sovereignty_lock_sections", "section_status"),
            ("human_sovereignty_lock_contracts", "contract_status"),
            ("human_sovereignty_lock_checks", "check_status"),
        ):
            if not all(
                item[status_key] == "pass"
                and item["blocking_reasons"] == []
                for item in first[container]
            ):
                raise AssertionError(container)

        lock_hash = first["deterministic_human_sovereignty_lock_hash"]
        if not isinstance(lock_hash, str) or len(lock_hash) != 64:
            raise AssertionError("lock hash")
        if lock_hash != second[
            "deterministic_human_sovereignty_lock_hash"
        ]:
            raise AssertionError("lock hash stability")
        json.dumps(first, ensure_ascii=True, sort_keys=True, allow_nan=False)
        _assert_safety(first)
    except AssertionError as exc:
        print(
            f"governance_human_sovereignty_lock=failed:{exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_human_sovereignty_lock=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
