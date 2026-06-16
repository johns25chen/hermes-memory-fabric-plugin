#!/usr/bin/env python3
"""Smoke test for the governance dry-run fixture pack."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_dry_run_fixture_pack import (  # noqa: E402
    build_governance_dry_run_fixture_pack,
    list_governance_dry_run_fixture_names,
)
from hermes_memory_fabric.governance_transition_policy_registry import (  # noqa: E402
    SAFETY_BOUNDARIES,
)


EXPECTED_FIXTURE_NAMES = [
    "valid_full_sequence",
    "valid_partial_sequence",
    "blocked_event_sequence",
    "duplicate_event_id_sequence",
    "invalid_previous_event_chain_sequence",
    "invalid_transition_sequence",
    "invalid_payload_schema_sequence",
    "malformed_event_sequence",
    "unknown_event_type_sequence",
    "sensitive_redaction_sequence",
]

BLOCKED_FIXTURE_NAMES = [
    "blocked_event_sequence",
    "duplicate_event_id_sequence",
    "invalid_previous_event_chain_sequence",
    "invalid_transition_sequence",
    "invalid_payload_schema_sequence",
    "malformed_event_sequence",
    "unknown_event_type_sequence",
]

SENSITIVE_BLOCKED_TERMS = [
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase-4-8",
    "fixture-stdout-tail-4-8",
    "fixture-stdout-4-8",
    "fixture-raw-logs-4-8",
    "fixture-token-4-8",
    "fixture-api-key-4-8",
    "fixture-secret-4-8",
    "fixture-password-4-8",
    "fixture-credential-4-8",
]


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


def _assert_no_sensitive_metadata_leak(fixture: dict[str, object]) -> None:
    raw_events = json.dumps(fixture["events"], sort_keys=True)
    if "fixture-secret-4-8" not in raw_events or '"secret"' not in raw_events:
        raise AssertionError("raw_sensitive_input_missing")

    protected = {
        key: value
        for key, value in fixture.items()
        if key != "events"
    }
    protected_json = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in protected_json:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_dry_run_fixture_pack()
        second = build_governance_dry_run_fixture_pack()
        if first["fixture_pack_status"] != "pass":
            raise AssertionError("fixture_pack_status")
        if first["fixture_count"] != len(EXPECTED_FIXTURE_NAMES):
            raise AssertionError("fixture_count")
        if first["fixture_names"] != EXPECTED_FIXTURE_NAMES:
            raise AssertionError("fixture_names")
        if list_governance_dry_run_fixture_names() != EXPECTED_FIXTURE_NAMES:
            raise AssertionError("list_fixture_names")
        if (
            first["deterministic_fixture_pack_hash"]
            != second["deterministic_fixture_pack_hash"]
        ):
            raise AssertionError("fixture_pack_hash_stability")

        fixtures = first["fixtures"]
        for name in EXPECTED_FIXTURE_NAMES:
            fixture = fixtures[name]
            if not fixture["deterministic_fixture_hash"]:
                raise AssertionError(f"{name}.fixture_hash")
            if (
                fixture["deterministic_fixture_hash"]
                != second["fixtures"][name]["deterministic_fixture_hash"]
            ):
                raise AssertionError(f"{name}.fixture_hash_stability")

        if (
            fixtures["valid_full_sequence"]["validation_summary"][
                "observed_final_state"
            ]
            != "finalized"
        ):
            raise AssertionError("valid_full_sequence.finalized")

        for name in BLOCKED_FIXTURE_NAMES:
            fixture = fixtures[name]
            if fixture["validation_summary"]["observed_status"] != "blocked":
                raise AssertionError(f"{name}.blocked")
            if fixture["cli_dry_run_result"]["dry_run_status"] != "blocked":
                raise AssertionError(f"{name}.cli_blocked")
            if fixture["cli_report_envelope"]["envelope_status"] != "blocked":
                raise AssertionError(f"{name}.envelope_blocked")

        _assert_safety(first)
        _assert_no_sensitive_metadata_leak(
            fixtures["sensitive_redaction_sequence"]
        )
    except Exception as exc:
        print(
            f"governance_dry_run_fixture_pack=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_dry_run_fixture_pack=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
