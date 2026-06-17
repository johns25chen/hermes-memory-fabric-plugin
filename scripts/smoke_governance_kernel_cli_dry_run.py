#!/usr/bin/env python3
"""Smoke test for the governance kernel CLI dry-run facade."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_kernel_cli_dry_run import (  # noqa: E402
    build_governance_kernel_cli_dry_run_result,
    governance_kernel_cli_dry_run_to_json,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


SCRIPT = REPO_ROOT / "scripts" / "governance_kernel_cli_dry_run.py"

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "5.0.0",
        "initialization_scope": "cli-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "cli-smoke",
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
        "requested_scope": "cli-smoke",
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
                "actor": "cli-smoke",
                "created_at": f"2026-06-16T00:00:{index:02d}Z",
                "payload": {
                    **_PAYLOADS[event_type],
                    "duplicate": "cli-sensitive-value",
                    "nested": {
                        "secret": "cli-sensitive-value",
                        "token": "cli-token-value",
                        "visible": "safe",
                    },
                    "sequence": index,
                },
                "previous_event_id": previous_event_id,
                "schema_version": "5.0.0",
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
        "cli-sensitive-value",
        "cli-token-value",
    ):
        if blocked in serialized:
            raise AssertionError("sensitive_leak")


def _assert_direct_mode(payload: dict[str, object]) -> dict[str, object]:
    first = build_governance_kernel_cli_dry_run_result(payload)
    second = build_governance_kernel_cli_dry_run_result(payload)
    first_json = governance_kernel_cli_dry_run_to_json(first)
    second_json = governance_kernel_cli_dry_run_to_json(second)
    if first_json != second_json:
        raise AssertionError("deterministic_json")
    if first["dry_run_status"] != "pass":
        raise AssertionError(str(payload["mode"]))
    _assert_safety(first)
    _assert_no_sensitive_leak(first_json)
    return first


def _run_script(
    args: list[str],
    *,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        input=input_text,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )


def main() -> int:
    try:
        events = _events()
        direct_payloads: list[dict[str, object]] = [
            {"mode": "validate_event", "event": events[0]},
            {"mode": "canonicalize_event", "event": events[0]},
            {"mode": "canonicalize_sequence", "events": events},
            {"mode": "replay_sequence", "events": events},
            {"mode": "audit_report", "events": events},
            {"mode": "local_store_replay", "events": events},
        ]
        direct_results = [
            _assert_direct_mode(payload)
            for payload in direct_payloads
        ]

        replay_result = direct_results[3]["result"]
        audit_result = direct_results[4]["result"]
        store_result = direct_results[5]["result"]
        if replay_result["current_state"] != "finalized":
            raise AssertionError("replay_sequence.final_state")
        if audit_result["final_state"] != "finalized":
            raise AssertionError("audit_report.final_state")
        if store_result["final_state"] != "finalized":
            raise AssertionError("local_store_replay.final_state")

        stdin_payload = json.dumps(
            {"mode": "replay_sequence", "events": events},
            sort_keys=True,
        )
        first_stdin = _run_script([], input_text=stdin_payload)
        second_stdin = _run_script([], input_text=stdin_payload)
        if first_stdin.returncode != 0 or second_stdin.returncode != 0:
            raise AssertionError("stdin_returncode")
        if first_stdin.stderr != "" or second_stdin.stderr != "":
            raise AssertionError("stdin_stderr")
        if first_stdin.stdout != second_stdin.stdout:
            raise AssertionError("stdin_determinism")
        stdin_result = json.loads(first_stdin.stdout)
        if stdin_result["result"]["current_state"] != "finalized":
            raise AssertionError("stdin_final_state")
        _assert_safety(stdin_result)
        _assert_no_sensitive_leak(first_stdin.stdout)

        inline_payload = json.dumps(
            {"mode": "audit_report", "events": events},
            sort_keys=True,
        )
        first_inline = _run_script(["--input-json", inline_payload])
        second_inline = _run_script(["--input-json", inline_payload])
        if first_inline.returncode != 0 or second_inline.returncode != 0:
            raise AssertionError("inline_returncode")
        if first_inline.stderr != "" or second_inline.stderr != "":
            raise AssertionError("inline_stderr")
        if first_inline.stdout != second_inline.stdout:
            raise AssertionError("inline_determinism")
        inline_result = json.loads(first_inline.stdout)
        if inline_result["result"]["final_state"] != "finalized":
            raise AssertionError("inline_final_state")
        _assert_safety(inline_result)
        _assert_no_sensitive_leak(first_inline.stdout)
    except Exception as exc:
        print(
            f"governance_kernel_cli_dry_run=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_kernel_cli_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
