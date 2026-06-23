#!/usr/bin/env python3
"""Smoke test for the local governance event schema registry."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_event_schema_registry import (  # noqa: E402
    ALLOWED_EVENT_TYPES,
    CANONICAL_EVENT_SCHEMA_VERSION,
    SAFETY_BOUNDARIES,
    governance_event_schema_registry_to_json,
    validate_event_against_schema_registry,
)


_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "6.8.0",
        "initialization_scope": "local-smoke",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "schema-smoke",
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
    "blocked": {
        "reason": "local-smoke-block",
    },
}

_SENSITIVE_KEYS = (
    "approval_phrase",
    "stdout_tail",
    "stdout",
    "raw_logs",
    "token",
    "api_key",
    "secret",
    "password",
    "credential",
)


def main() -> int:
    try:
        first_serializations: list[str] = []
        second_serializations: list[str] = []
        sensitive_values: list[str] = []
        for index, event_type in enumerate(ALLOWED_EVENT_TYPES, start=1):
            event_sensitive_values = {
                key: f"sensitive-{index}-{key}"
                for key in _SENSITIVE_KEYS
            }
            sensitive_values.extend(event_sensitive_values.values())
            event = {
                "event_id": f"event-{index}",
                "event_type": event_type,
                "actor": "local-smoke",
                "created_at": f"2026-06-15T00:00:{index:02d}Z",
                "payload": {
                    **_PAYLOADS[event_type],
                    "nested": event_sensitive_values,
                },
                "previous_event_id": None,
                "schema_version": CANONICAL_EVENT_SCHEMA_VERSION,
            }
            first = validate_event_against_schema_registry(event)
            second = validate_event_against_schema_registry(event)
            if first["valid"] is not True:
                raise AssertionError(event_type)
            if not isinstance(first["sanitized_event"], Mapping):
                raise AssertionError("sanitized_event")
            if first["schema_version"] != "6.8.0":
                raise AssertionError("schema_version")
            for key in SAFETY_BOUNDARIES:
                if first.get(key) is not False:
                    raise AssertionError(key)
            first_serializations.append(
                governance_event_schema_registry_to_json(first)
            )
            second_serializations.append(
                governance_event_schema_registry_to_json(second)
            )

        if first_serializations != second_serializations:
            raise AssertionError("deterministic_json")
        serialized = "".join(first_serializations)
        for key in _SENSITIVE_KEYS:
            if f'"{key}"' in serialized:
                raise AssertionError("sensitive_key")
        for value in sensitive_values:
            if value in serialized:
                raise AssertionError("sensitive_value")
    except Exception as exc:
        print(
            f"governance_event_schema_registry=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_event_schema_registry=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
