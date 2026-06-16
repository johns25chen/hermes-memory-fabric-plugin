from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

from hermes_memory_fabric.governance_dry_run_fixture_pack import (
    GOVERNANCE_DRY_RUN_FIXTURE_HASH_ALGORITHM,
    GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE,
    GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
    GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
    SAFETY_BOUNDARIES,
    build_governance_dry_run_fixture_pack,
    get_governance_dry_run_fixture,
    governance_dry_run_fixture_pack_to_json,
    list_governance_dry_run_fixture_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_dry_run_fixture_pack.py"
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

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase-4-10",
    "fixture-stdout-tail-4-10",
    "fixture-stdout-4-10",
    "fixture-raw-logs-4-10",
    "fixture-token-4-10",
    "fixture-api-key-4-10",
    "fixture-secret-4-10",
    "fixture-password-4-10",
    "fixture-credential-4-10",
)


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert value[key] is False
                assert boundaries[key] is False
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_string_keys_and_finite_values(value: object) -> None:
    if isinstance(value, dict):
        assert all(isinstance(key, str) for key in value)
        for nested_value in value.values():
            _assert_string_keys_and_finite_values(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_string_keys_and_finite_values(item)
    elif isinstance(value, float):
        assert math.isfinite(value)


def _fixture(name: str) -> dict[str, object]:
    return build_governance_dry_run_fixture_pack()["fixtures"][name]


def _protected_sensitive_fixture_json() -> str:
    fixture = _fixture("sensitive_redaction_sequence")
    protected = {
        key: value
        for key, value in fixture.items()
        if key != "events"
    }
    return json.dumps(protected, sort_keys=True)


def test_public_constants():
    assert GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION == "4.10.0"
    assert GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION == "4.10.0"
    assert (
        GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE
        == "governance_dry_run_fixture_pack"
    )
    assert GOVERNANCE_DRY_RUN_FIXTURE_HASH_ALGORITHM == "sha256"


def test_fixture_pack_shape_is_deterministic():
    first = build_governance_dry_run_fixture_pack()
    second = build_governance_dry_run_fixture_pack()

    assert first == second
    assert first["version"] == "4.10.0"
    assert first["schema_version"] == "4.10.0"
    assert first["fixture_pack_type"] == "governance_dry_run_fixture_pack"
    assert first["fixture_pack_status"] == "pass"
    assert first["fixture_count"] == len(EXPECTED_FIXTURE_NAMES)
    assert len(first["deterministic_fixture_pack_hash"]) == 64
    assert set(first["fixtures"]) == set(EXPECTED_FIXTURE_NAMES)


def test_fixture_names_are_stable_and_complete():
    assert list_governance_dry_run_fixture_names() == EXPECTED_FIXTURE_NAMES
    assert (
        build_governance_dry_run_fixture_pack()["fixture_names"]
        == EXPECTED_FIXTURE_NAMES
    )


def test_get_fixture_by_name_returns_detached_copies():
    first = get_governance_dry_run_fixture("valid_full_sequence")
    original = deepcopy(first)
    first["events"][0]["payload"]["sequence"] = 99  # type: ignore[index]
    first["validation_summary"]["observed_final_state"] = "mutated"  # type: ignore[index]

    second = get_governance_dry_run_fixture("valid_full_sequence")

    assert second == original
    assert second["events"][0]["payload"]["sequence"] == 1  # type: ignore[index]
    assert (
        second["validation_summary"]["observed_final_state"]  # type: ignore[index]
        == "finalized"
    )


def test_unknown_fixture_name_returns_blocked_style_result():
    result = get_governance_dry_run_fixture("missing_fixture")
    second = get_governance_dry_run_fixture("missing_fixture")

    assert result == second
    assert result["fixture_name"] == "missing_fixture"
    assert result["expected_status"] == "blocked"
    assert result["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert result["cli_dry_run_result"]["dry_run_status"] == "blocked"  # type: ignore[index]
    assert len(result["deterministic_fixture_hash"]) == 64


def test_valid_full_sequence_reports_pass_and_finalized():
    fixture = _fixture("valid_full_sequence")

    assert fixture["expected_status"] == "pass"
    assert fixture["validation_summary"]["observed_status"] == "pass"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_final_state"] == "finalized"  # type: ignore[index]
    assert fixture["replay_audit_report"]["final_state"] == "finalized"  # type: ignore[index]
    assert fixture["cli_dry_run_result"]["dry_run_status"] == "pass"  # type: ignore[index]
    assert fixture["cli_report_envelope"]["envelope_status"] == "pass"  # type: ignore[index]


def test_valid_partial_sequence_reports_pass_and_non_final_state():
    fixture = _fixture("valid_partial_sequence")

    assert fixture["validation_summary"]["observed_status"] == "pass"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_final_state"] == "review_ready"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_final_state"] != "finalized"  # type: ignore[index]


def test_blocked_event_sequence_reports_blocked():
    fixture = _fixture("blocked_event_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_final_state"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "blocked_event"
    ]


def test_duplicate_event_id_sequence_reports_duplicate_category():
    fixture = _fixture("duplicate_event_id_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "duplicate_event_id"
    ]


def test_invalid_previous_event_chain_sequence_reports_invalid_chain_category():
    fixture = _fixture("invalid_previous_event_chain_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "invalid_previous_event_chain"
    ]


def test_invalid_transition_sequence_reports_invalid_transition_category():
    fixture = _fixture("invalid_transition_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "invalid_state_transition"
    ]


def test_invalid_payload_schema_sequence_reports_invalid_payload_category():
    fixture = _fixture("invalid_payload_schema_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "invalid_payload_schema"
    ]


def test_malformed_event_sequence_reports_malformed_category():
    fixture = _fixture("malformed_event_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "malformed_event"
    ]


def test_unknown_event_type_sequence_reports_unknown_event_category():
    fixture = _fixture("unknown_event_type_sequence")

    assert fixture["validation_summary"]["observed_status"] == "blocked"  # type: ignore[index]
    assert fixture["validation_summary"]["observed_error_categories"] == [  # type: ignore[index]
        "unknown_event_type"
    ]


def test_sensitive_redaction_sequence_keeps_raw_inputs_only_in_events():
    fixture = _fixture("sensitive_redaction_sequence")
    raw_events = json.dumps(fixture["events"], sort_keys=True)

    assert '"secret"' in raw_events
    assert "fixture-secret-4-10" in raw_events
    assert fixture["validation_summary"]["sensitive_fields_omitted"] is True  # type: ignore[index]
    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in _protected_sensitive_fixture_json()


def test_sensitive_values_do_not_leak_in_reports_envelopes_or_hashes():
    fixture = _fixture("sensitive_redaction_sequence")
    protected_parts = {
        "validation_summary": fixture["validation_summary"],
        "replay_audit_report": fixture["replay_audit_report"],
        "cli_dry_run_result": fixture["cli_dry_run_result"],
        "cli_report_envelope": fixture["cli_report_envelope"],
        "deterministic_fixture_hash": fixture["deterministic_fixture_hash"],
    }
    serialized = json.dumps(protected_parts, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_raw_sensitive_values_do_not_appear_in_other_fixture_events():
    pack = build_governance_dry_run_fixture_pack()
    non_sensitive_events = [
        fixture["events"]
        for name, fixture in pack["fixtures"].items()
        if name != "sensitive_redaction_sequence"
    ]
    serialized = json.dumps(non_sensitive_events, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_fixture_hashes_stable_across_repeated_runs():
    first = build_governance_dry_run_fixture_pack()
    second = build_governance_dry_run_fixture_pack()

    assert first["fixture_hashes"] == second["fixture_hashes"]
    for name in EXPECTED_FIXTURE_NAMES:
        assert (
            first["fixtures"][name]["deterministic_fixture_hash"]
            == second["fixtures"][name]["deterministic_fixture_hash"]
        )


def test_fixture_pack_hash_stable_across_repeated_runs():
    first = build_governance_dry_run_fixture_pack()
    second = build_governance_dry_run_fixture_pack()

    assert (
        first["deterministic_fixture_pack_hash"]
        == second["deterministic_fixture_pack_hash"]
    )


def test_fixture_pack_json_is_deterministic():
    pack = build_governance_dry_run_fixture_pack()
    original = deepcopy(pack)

    first = governance_dry_run_fixture_pack_to_json(pack)
    second = governance_dry_run_fixture_pack_to_json(pack)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["fixture_pack_status"] == "pass"
    assert pack == original


def test_all_safety_fields_remain_false():
    pack = build_governance_dry_run_fixture_pack()

    _assert_safety(pack)


def test_all_mapping_keys_are_strings_and_floats_are_finite():
    pack = build_governance_dry_run_fixture_pack()

    _assert_string_keys_and_finite_values(pack)


def test_fixture_pack_module_has_only_local_standard_library_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert imported_roots <= {
        "__future__",
        "collections",
        "governance_cli_report_envelope",
        "governance_event_schema_registry",
        "governance_kernel_cli_dry_run",
        "governance_replay_audit_report",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
        "math",
        "typing",
    }
    assert called_names.isdisjoint(
        {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
        }
    )
    for forbidden in (
        "subprocess",
        "socket",
        "filesystem",
        "database",
        "network",
        "url" + "open",
        "urllib" + "." + "request",
        "requests" + ".",
        "github",
        "openclaw",
        "composio",
        "memory_graph",
        "memory graph",
        "operation_ledger",
        "write",
        "execution",
    ):
        assert forbidden not in source.casefold()
