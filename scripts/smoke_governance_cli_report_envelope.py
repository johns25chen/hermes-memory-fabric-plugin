#!/usr/bin/env python3
"""Smoke test for the governance CLI report envelope."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_cli_report_envelope import (  # noqa: E402
    build_governance_cli_report_envelope,
)
from hermes_memory_fabric.governance_kernel_cli_dry_run import (  # noqa: E402
    build_governance_kernel_cli_dry_run_result,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "5.9.0",
        "initialization_scope": "cli-envelope-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "cli-envelope-smoke",
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
        "requested_scope": "cli-envelope-smoke",
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
                "actor": "cli-envelope-smoke",
                "created_at": f"2026-06-16T00:00:{index:02d}Z",
                "payload": {
                    **_PAYLOADS[event_type],
                    "duplicate": "envelope-sensitive-value",
                    "nested": {
                        "secret": "envelope-sensitive-value",
                        "token": "envelope-token-value",
                        "visible": "safe",
                    },
                    "sequence": index,
                },
                "previous_event_id": previous_event_id,
                "schema_version": "5.9.0",
            }
        )
        previous_event_id = event_id
    return events


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                if value.get(key) is not False:
                    raise AssertionError(key)
                if boundaries.get(key) is not False:
                    raise AssertionError(f"safety_boundaries.{key}")
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_no_sensitive_leak(serialized: str) -> None:
    for blocked in (
        '"secret"',
        '"token"',
        "envelope-sensitive-value",
        "envelope-token-value",
    ):
        if blocked in serialized:
            raise AssertionError("sensitive_leak")


def _assert_envelope(payload: dict[str, object]) -> dict[str, object]:
    cli_result = build_governance_kernel_cli_dry_run_result(payload)
    first = build_governance_cli_report_envelope(cli_result)
    second = build_governance_cli_report_envelope(cli_result)
    if first["envelope_status"] != "pass":
        raise AssertionError(str(payload["mode"]))
    if first["envelope_type"] != "governance_cli_report_envelope":
        raise AssertionError("envelope_type")
    if first["source_report_version"] != "5.9.0":
        raise AssertionError("source_report_version")
    if first["deterministic_report_hash"] != second["deterministic_report_hash"]:
        raise AssertionError("report_hash_stability")
    if first["deterministic_envelope_hash"] != second["deterministic_envelope_hash"]:
        raise AssertionError("envelope_hash_stability")
    if first["report_metadata"]["star_cosmos_entry_claimed"] is not False:
        raise AssertionError("star_cosmos_entry_claimed")
    if first["report_metadata"]["no_execution"] is not True:
        raise AssertionError("no_execution")
    if first["report_metadata"]["no_writes"] is not True:
        raise AssertionError("no_writes")
    _assert_safety(first)
    _assert_no_sensitive_leak(json.dumps(first, sort_keys=True))
    return first


def main() -> int:
    try:
        events = _events()
        envelopes = [
            _assert_envelope({"mode": "validate_event", "event": events[0]}),
            _assert_envelope({"mode": "canonicalize_sequence", "events": events}),
            _assert_envelope({"mode": "replay_sequence", "events": events}),
            _assert_envelope({"mode": "audit_report", "events": events}),
            _assert_envelope({"mode": "local_store_replay", "events": events}),
        ]
        for envelope in envelopes[2:]:
            if envelope["report_summary"].get("final_state") != "finalized":
                raise AssertionError("final_state")
    except Exception as exc:
        print(
            f"governance_cli_report_envelope=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_cli_report_envelope=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
