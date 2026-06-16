#!/usr/bin/env python3
"""Smoke test for the governance dry-run validation matrix."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_SRC = REPO_ROOT / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_dry_run_validation_matrix import (  # noqa: E402
    build_governance_dry_run_validation_matrix,
    governance_dry_run_validation_matrix_to_json,
    list_governance_dry_run_validation_matrix_fixture_names,
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
    "fixture-approval-phrase-4-9",
    "fixture-stdout-tail-4-9",
    "fixture-stdout-4-9",
    "fixture-raw-logs-4-9",
    "fixture-token-4-9",
    "fixture-api-key-4-9",
    "fixture-secret-4-9",
    "fixture-password-4-9",
    "fixture-credential-4-9",
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


def _row_map(matrix: dict[str, object]) -> dict[str, dict[str, object]]:
    rows = matrix["matrix_rows"]
    if not isinstance(rows, list):
        raise AssertionError("matrix_rows")
    return {row["fixture_name"]: row for row in rows if isinstance(row, dict)}


def _assert_no_sensitive_leak(matrix: dict[str, object]) -> None:
    rows = _row_map(matrix)
    protected = {
        "row": rows["sensitive_redaction_sequence"],
        "summary": matrix["matrix_summary"],
        "hashes": {
            "matrix": matrix["deterministic_validation_matrix_hash"],
            "fixture_pack": matrix["fixture_pack_hash"],
            "fixture": rows["sensitive_redaction_sequence"]["fixture_hash"],
            "audit": rows["sensitive_redaction_sequence"]["audit_report_hash"],
            "cli": rows["sensitive_redaction_sequence"]["cli_hash"],
            "envelope": rows["sensitive_redaction_sequence"]["envelope_hash"],
        },
        "json": governance_dry_run_validation_matrix_to_json(matrix),
    }
    serialized = json.dumps(protected, sort_keys=True)
    for blocked in SENSITIVE_BLOCKED_TERMS:
        if blocked in serialized:
            raise AssertionError("sensitive_metadata_leak")


def main() -> int:
    try:
        first = build_governance_dry_run_validation_matrix()
        second = build_governance_dry_run_validation_matrix()
        rows = _row_map(first)

        if first["validation_matrix_status"] != "pass":
            raise AssertionError("validation_matrix_status")
        if first["row_count"] != len(EXPECTED_FIXTURE_NAMES):
            raise AssertionError("row_count")
        if first["matrix_summary"]["fixture_names"] != EXPECTED_FIXTURE_NAMES:
            raise AssertionError("fixture_names")
        if (
            list_governance_dry_run_validation_matrix_fixture_names()
            != EXPECTED_FIXTURE_NAMES
        ):
            raise AssertionError("list_fixture_names")
        if (
            first["deterministic_validation_matrix_hash"]
            != second["deterministic_validation_matrix_hash"]
        ):
            raise AssertionError("validation_matrix_hash_stability")
        if rows["valid_full_sequence"]["observed_final_state"] != "finalized":
            raise AssertionError("valid_full_sequence.finalized")
        if rows["valid_full_sequence"]["row_status"] != "pass":
            raise AssertionError("valid_full_sequence.pass")
        if rows["valid_partial_sequence"]["row_status"] != "pass":
            raise AssertionError("valid_partial_sequence.pass")
        if rows["valid_partial_sequence"]["observed_final_state"] == "finalized":
            raise AssertionError("valid_partial_sequence.finalized")
        for name in BLOCKED_FIXTURE_NAMES:
            row = rows[name]
            if row["row_status"] != "blocked":
                raise AssertionError(f"{name}.blocked")
            if row["observed_fixture_status"] != "blocked":
                raise AssertionError(f"{name}.observed_blocked")
        for row in rows.values():
            if row["expectation_match"] is not True:
                raise AssertionError(f"{row['fixture_name']}.expectation")

        _assert_safety(first)
        _assert_no_sensitive_leak(first)
    except Exception as exc:
        print(
            f"governance_dry_run_validation_matrix=failed {exc}",
            file=sys.stderr,
        )
        return 1

    print("governance_dry_run_validation_matrix=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
