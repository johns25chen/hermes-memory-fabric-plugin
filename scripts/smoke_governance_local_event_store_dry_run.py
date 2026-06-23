#!/usr/bin/env python3
"""Smoke test for the local governance event store dry-run contract."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_local_event_store_dry_run import (  # noqa: E402
    SAFETY_BOUNDARIES,
    append_governance_events_to_local_store_dry_run,
    build_governance_local_event_store_replay_report_dry_run,
    create_governance_local_event_store_dry_run,
    read_governance_local_event_store_dry_run,
)


_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "6.7.0",
        "initialization_scope": "local-event-store-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "local-event-store-smoke",
    },
    "review_completed": {
        "review_id": "review-1",
        "review_status": "complete",
    },
    "dry_run_approved": {
        "approval_id": "approval-1",
        "approved_for": "plan-preparation-only",
    },
    "dry_run_prepared": {
        "dry_run_id": "dry-run-1",
        "plan_id": "plan-1",
    },
    "dry_run_completed": {
        "dry_run_id": "dry-run-1",
        "completion_status": "recorded-only",
    },
    "attestation_submitted": {
        "attestation_id": "attestation-1",
        "attestation_status": "recorded-only",
    },
    "finalization_requested": {
        "finalization_id": "finalization-1",
        "requested_scope": "local-event-store-smoke",
    },
}


def _events() -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(_PAYLOADS, start=1):
        event_id = f"event-{index}"
        events.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "actor": "local-smoke",
                "created_at": f"2026-06-16T00:00:{index:02d}Z",
                "payload": {
                    **_PAYLOADS[event_type],
                    "duplicate": "local-store-sensitive-value",
                    "nested": {
                        "secret": "local-store-sensitive-value",
                        "token": "local-store-token-value",
                        "visible": "safe",
                    },
                    "sequence": index,
                },
                "previous_event_id": previous_event_id,
                "schema_version": "6.7.0",
            }
        )
        previous_event_id = event_id
    return events


def _assert_safety(result: dict[str, object]) -> None:
    boundaries = result.get("safety_boundaries")
    if not isinstance(boundaries, dict):
        raise AssertionError("safety_boundaries")
    for key in SAFETY_BOUNDARIES:
        if result.get(key) is not False:
            raise AssertionError(key)
        if boundaries.get(key) is not False:
            raise AssertionError(f"safety_boundaries.{key}")


def main() -> int:
    try:
        events = _events()
        empty_store = create_governance_local_event_store_dry_run()
        first_append = append_governance_events_to_local_store_dry_run(
            empty_store,
            events,
        )
        second_append = append_governance_events_to_local_store_dry_run(
            create_governance_local_event_store_dry_run(),
            events,
        )
        if first_append["append_sequence_status"] != "pass":
            raise AssertionError("append_sequence_status")
        if first_append["appended_event_count"] != len(events):
            raise AssertionError("appended_event_count")

        store = first_append["store"]
        read_result = read_governance_local_event_store_dry_run(store)
        first_replay = (
            build_governance_local_event_store_replay_report_dry_run(store)
        )
        second_replay = (
            build_governance_local_event_store_replay_report_dry_run(
                second_append["store"]
            )
        )
        if read_result["event_count"] != len(events):
            raise AssertionError("event_count")
        if first_replay["final_state"] != "finalized":
            raise AssertionError("final_state")
        if (
            first_append["deterministic_store_hash"]
            != read_result["deterministic_store_hash"]
            or first_append["deterministic_store_hash"]
            != second_append["deterministic_store_hash"]
        ):
            raise AssertionError("deterministic_store_hash")
        for hash_field in (
            "deterministic_replay_hash",
            "deterministic_sequence_hash",
            "audit_report_hash",
        ):
            if first_replay[hash_field] != second_replay[hash_field]:
                raise AssertionError(hash_field)

        _assert_safety(empty_store)
        _assert_safety(first_append)
        _assert_safety(store)
        _assert_safety(read_result)
        _assert_safety(first_replay)
        _assert_safety(first_replay["replay_audit_report"])

        serialized = json.dumps(
            {
                "append": first_append,
                "read": read_result,
                "replay": first_replay,
            },
            sort_keys=True,
        )
        if '"secret"' in serialized:
            raise AssertionError("sensitive_key")
        if '"token"' in serialized:
            raise AssertionError("sensitive_key")
        if "local-store-sensitive-value" in serialized:
            raise AssertionError("sensitive_value")
        if "local-store-token-value" in serialized:
            raise AssertionError("sensitive_value")
    except Exception as exc:
        print(
            f"governance_local_event_store_dry_run=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_local_event_store_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
