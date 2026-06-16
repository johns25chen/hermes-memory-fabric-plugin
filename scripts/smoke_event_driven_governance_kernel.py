#!/usr/bin/env python3
"""Smoke test for the local event-driven governance kernel."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.event_driven_governance_kernel import (  # noqa: E402
    SAFETY_BOUNDARIES,
    replay_governance_events,
)

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "4.9.0",
        "initialization_scope": "local-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "kernel-smoke",
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
        "requested_scope": "local-smoke",
    },
}


def _events() -> list[dict[str, object]]:
    event_types = [
        "governance_kernel_initialized",
        "proposal_submitted",
        "review_completed",
        "dry_run_approved",
        "dry_run_prepared",
        "dry_run_completed",
        "attestation_submitted",
        "finalization_requested",
    ]
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(event_types, start=1):
        event_id = f"event-{index}"
        events.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "actor": "local-smoke",
                "created_at": f"2026-06-14T00:00:0{index}Z",
                "payload": {**_PAYLOADS[event_type], "sequence": index},
                "previous_event_id": previous_event_id,
                "schema_version": "4.9.0",
            }
        )
        previous_event_id = event_id
    return events


def main() -> int:
    try:
        events = _events()
        first = replay_governance_events(events)
        second = replay_governance_events(events)
        if first["current_state"] != "finalized":
            raise AssertionError("current_state")
        if first["audit_status"] != "pass":
            raise AssertionError("audit_status")
        if first["replay_safe"] is not True:
            raise AssertionError("replay_safe")
        if first["transition_policy_version"] != "4.9.0":
            raise AssertionError("transition_policy_version")
        if first["transition_policy_registry_version"] != "4.9.0":
            raise AssertionError("transition_policy_registry_version")
        for key in SAFETY_BOUNDARIES:
            if first.get(key) is not False:
                raise AssertionError(key)
        if (
            first["deterministic_replay_hash"]
            != second["deterministic_replay_hash"]
        ):
            raise AssertionError("deterministic_replay_hash")
    except Exception as exc:
        print(f"event_driven_governance_kernel=failed {exc}", file=sys.stderr)
        return 1

    print("event_driven_governance_kernel=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
