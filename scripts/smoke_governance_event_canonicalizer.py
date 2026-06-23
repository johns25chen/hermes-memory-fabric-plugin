#!/usr/bin/env python3
"""Smoke test for deterministic governance event canonicalization."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_event_canonicalizer import (  # noqa: E402
    canonicalize_governance_event_sequence,
)
from hermes_memory_fabric.governance_event_schema_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "6.8.0",
        "initialization_scope": "local-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "canonicalizer-smoke",
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
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(_PAYLOADS, start=1):
        event_id = f"event-{index}"
        events.append(
            {
                "event_id": event_id,
                "event_type": event_type,
                "actor": "local-smoke",
                "created_at": f"2026-06-15T00:00:{index:02d}Z",
                "payload": {
                    **_PAYLOADS[event_type],
                    "duplicate": "smoke-secret-value",
                    "nested": {
                        "secret": "smoke-secret-value",
                        "visible": "safe",
                    },
                    "sequence": index,
                },
                "previous_event_id": previous_event_id,
                "schema_version": "6.8.0",
            }
        )
        previous_event_id = event_id
    return events


def main() -> int:
    try:
        events = _events()
        first = canonicalize_governance_event_sequence(events)
        second = canonicalize_governance_event_sequence(events)
        if first["canonicalization_status"] != "pass":
            raise AssertionError("canonicalization_status")
        if first["canonical_event_count"] != len(events):
            raise AssertionError("canonical_event_count")
        if (
            first["deterministic_sequence_hash"]
            != second["deterministic_sequence_hash"]
        ):
            raise AssertionError("deterministic_sequence_hash")
        for key in SAFETY_BOUNDARIES:
            if first.get(key) is not False:
                raise AssertionError(key)
            if first["safety_boundaries"].get(key) is not False:
                raise AssertionError(f"safety_boundaries.{key}")
        serialized = json.dumps(first, sort_keys=True)
        if '"secret"' in serialized:
            raise AssertionError("sensitive_key")
        if "smoke-secret-value" in serialized:
            raise AssertionError("sensitive_value")
    except Exception as exc:
        print(
            f"governance_event_canonicalizer=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_event_canonicalizer=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
