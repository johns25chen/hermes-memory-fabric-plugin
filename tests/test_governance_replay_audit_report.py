from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import hermes_memory_fabric.governance_replay_audit_report as replay_audit_module
from hermes_memory_fabric.governance_event_schema_registry import (
    SAFETY_BOUNDARIES,
)
from hermes_memory_fabric.governance_replay_audit_report import (
    ERROR_CATEGORY_TAXONOMY,
    REPLAY_AUDIT_HASH_ALGORITHM,
    REPLAY_AUDIT_REPORT_VERSION,
    REPLAY_AUDIT_SCHEMA_VERSION,
    build_governance_replay_audit_report,
    governance_replay_audit_report_to_json,
)


CORE_MODULE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "hermes_memory_fabric"
    / "governance_replay_audit_report.py"
)

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": "6.5.0",
        "initialization_scope": "test",
    },
    "proposal_submitted": {
        "proposal_id": "proposal-1",
        "proposal_type": "test",
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
        "requested_scope": "test",
    },
    "blocked": {
        "reason": "test-block",
    },
}


def _event(
    event_id: str,
    event_type: str,
    previous_event_id: str | None,
    payload: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_type": event_type,
        "actor": "test-actor",
        "created_at": f"2026-06-15T00:00:{event_id[-1:]}Z",
        "payload": (
            payload
            if payload is not None
            else dict(_PAYLOADS.get(event_type, {}))
        ),
        "previous_event_id": previous_event_id,
        "schema_version": "6.5.0",
    }


def _full_events() -> list[dict[str, object]]:
    event_types = tuple(_PAYLOADS)[:-1]
    events: list[dict[str, object]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(event_types, start=1):
        event_id = f"event-{index}"
        events.append(
            _event(
                event_id,
                event_type,
                previous_event_id,
                {**_PAYLOADS[event_type], "sequence": index},
            )
        )
        previous_event_id = event_id
    return events


def _rechain(events: list[dict[str, object]]) -> None:
    previous_event_id: str | None = None
    for event in events:
        event["previous_event_id"] = previous_event_id
        previous_event_id = str(event["event_id"])


def test_public_versions_and_hash_algorithm():
    assert REPLAY_AUDIT_REPORT_VERSION == "6.5.0"
    assert REPLAY_AUDIT_SCHEMA_VERSION == "6.5.0"
    assert REPLAY_AUDIT_HASH_ALGORITHM == "sha256"


def test_valid_full_sequence_reports_pass_and_finalized():
    result = build_governance_replay_audit_report(_full_events())

    assert result["version"] == "6.5.0"
    assert result["audit_report_status"] == "pass"
    assert result["replay_status"] == "pass"
    assert result["canonicalization_status"] == "pass"
    assert result["final_state"] == "finalized"
    assert result["accepted_event_count"] == 8
    assert result["rejected_event_count"] == 0
    assert result["blocking_reasons"] == []
    assert result["error_categories"] == []
    assert result["transition_policy_version"] == "6.5.0"
    assert result["transition_policy_registry_version"] == "6.5.0"
    assert len(result["policy_evaluation_summaries"]) == 8
    assert all(
        summary["valid_transition"] is True
        for summary in result["policy_evaluation_summaries"]
    )


def test_valid_partial_sequence_reports_current_state():
    result = build_governance_replay_audit_report(_full_events()[:3])

    assert result["audit_report_status"] == "pass"
    assert result["final_state"] == "review_ready"
    assert result["next_allowed_events"] == ["dry_run_approved", "blocked"]


def test_report_is_deterministic_across_repeated_runs():
    events = _full_events()

    first = build_governance_replay_audit_report(events)
    second = build_governance_replay_audit_report(events)

    assert first == second
    assert first["audit_report_hash"] == second["audit_report_hash"]


def test_report_hash_changes_when_payload_changes():
    events = _full_events()
    changed = deepcopy(events)
    changed[2]["payload"]["sequence"] = 99  # type: ignore[index]

    first = build_governance_replay_audit_report(events)
    second = build_governance_replay_audit_report(changed)

    assert first["audit_report_hash"] != second["audit_report_hash"]
    assert (
        first["deterministic_sequence_hash"]
        != second["deterministic_sequence_hash"]
    )


def test_report_hash_changes_when_event_order_changes():
    events = _full_events()
    changed = deepcopy(events)
    changed[2], changed[3] = changed[3], changed[2]
    _rechain(changed)

    first = build_governance_replay_audit_report(events)
    second = build_governance_replay_audit_report(changed)

    assert first["audit_report_hash"] != second["audit_report_hash"]
    assert (
        first["deterministic_sequence_hash"]
        != second["deterministic_sequence_hash"]
    )


def test_report_hash_changes_when_policy_aware_outcome_changes(monkeypatch):
    events = _full_events()
    original = build_governance_replay_audit_report(events)
    original_replay = replay_audit_module.replay_governance_events

    def changed_replay(
        replay_events: list[dict[str, object]],
    ) -> dict[str, object]:
        result = deepcopy(original_replay(replay_events))
        result["transition_history"][0]["policy_evaluation"][
            "next_state"
        ] = "policy-outcome-changed"
        return result

    monkeypatch.setattr(
        replay_audit_module,
        "replay_governance_events",
        changed_replay,
    )
    changed = build_governance_replay_audit_report(events)

    assert original["audit_report_hash"] != changed["audit_report_hash"]
    assert original["deterministic_sequence_hash"] == (
        changed["deterministic_sequence_hash"]
    )


def test_report_includes_canonical_replay_hashes_and_contract():
    result = build_governance_replay_audit_report(_full_events())

    assert len(result["deterministic_sequence_hash"]) == 64
    assert len(result["deterministic_replay_hash"]) == 64
    assert len(result["audit_report_hash"]) == 64
    assert result["canonical_sequence"]["deterministic_sequence_hash"] == (
        result["deterministic_sequence_hash"]
    )
    assert result["hash_input_contract"]["algorithm"] == "sha256"
    assert result["hash_input_contract"]["raw_events_included"] is False
    assert (
        result["hash_input_contract"]["sensitive_fields_included"] is False
    )
    assert "policy_evaluation_summaries" in (
        result["hash_input_contract"]["hash_fields"]
    )


def test_accepted_event_summaries_are_deterministic_and_sanitized():
    event = _full_events()[0]
    event["payload"]["secret"] = "hidden-value"  # type: ignore[index]
    event["payload"]["duplicate"] = "hidden-value"  # type: ignore[index]

    first = build_governance_replay_audit_report([event])
    second = build_governance_replay_audit_report([event])
    serialized = json.dumps(first["accepted_event_summaries"], sort_keys=True)

    assert first["accepted_event_summaries"] == (
        second["accepted_event_summaries"]
    )
    assert first["accepted_event_summaries"][0]["event_id"] == "event-1"
    assert '"secret"' not in serialized
    assert "hidden-value" not in serialized


def test_rejected_event_summaries_are_deterministic_and_sanitized():
    event = _event(
        "event-1",
        "unknown",
        None,
        {
            "secret": "hidden-value",
            "duplicate": "hidden-value",
        },
    )

    first = build_governance_replay_audit_report([event])
    second = build_governance_replay_audit_report([event])
    serialized = json.dumps(first["rejected_event_summaries"], sort_keys=True)

    assert first["rejected_event_summaries"] == (
        second["rejected_event_summaries"]
    )
    assert "unknown_event_type" in (
        first["rejected_event_summaries"][0]["error_categories"]
    )
    assert '"secret"' not in serialized
    assert "hidden-value" not in serialized


def test_unknown_event_type_is_blocked_and_categorized():
    result = build_governance_replay_audit_report(
        [_event("event-1", "unknown", None)]
    )

    assert result["audit_report_status"] == "blocked"
    assert "unknown_event_type" in result["error_categories"]


def test_invalid_payload_schema_is_blocked_and_categorized():
    event = _event(
        "event-1",
        "governance_kernel_initialized",
        None,
        {"kernel_version": "6.5.0"},
    )

    result = build_governance_replay_audit_report([event])

    assert result["audit_report_status"] == "blocked"
    assert "invalid_payload_schema" in result["error_categories"]


def test_duplicate_event_id_is_blocked_and_categorized():
    events = _full_events()[:2]
    events[1]["event_id"] = "event-1"
    events[1]["previous_event_id"] = "event-1"

    result = build_governance_replay_audit_report(events)

    assert result["audit_report_status"] == "blocked"
    assert "duplicate_event_id" in result["error_categories"]


def test_invalid_previous_event_chain_is_blocked_and_categorized():
    events = _full_events()[:2]
    events[1]["previous_event_id"] = "wrong-event"

    result = build_governance_replay_audit_report(events)

    assert result["audit_report_status"] == "blocked"
    assert "invalid_previous_event_chain" in result["error_categories"]


def test_invalid_transition_is_blocked_and_categorized():
    result = build_governance_replay_audit_report(
        [_event("event-1", "review_completed", None)]
    )

    assert result["audit_report_status"] == "blocked"
    assert result["canonicalization_status"] == "pass"
    assert "invalid_state_transition" in result["error_categories"]


def test_blocked_event_is_categorized():
    result = build_governance_replay_audit_report(
        [_event("event-1", "blocked", None)]
    )

    assert result["audit_report_status"] == "blocked"
    assert result["final_state"] == "blocked"
    assert result["accepted_event_count"] == 1
    assert result["rejected_event_count"] == 0
    assert "blocked_event" in result["error_categories"]


def test_malformed_event_is_blocked_and_categorized():
    event = _full_events()[0]
    del event["actor"]

    result = build_governance_replay_audit_report([event])

    assert result["audit_report_status"] == "blocked"
    assert "malformed_event" in result["error_categories"]


def test_non_finite_values_are_blocked_and_json_compatible():
    event = _full_events()[0]
    event["payload"]["measurement"] = math.inf  # type: ignore[index]

    result = build_governance_replay_audit_report([event])
    serialized = governance_replay_audit_report_to_json(result)

    assert result["audit_report_status"] == "blocked"
    assert "canonicalization_error" in result["error_categories"]
    assert "Infinity" not in serialized


def test_sensitive_keys_and_values_do_not_leak_anywhere():
    sensitive = {
        "approval_phrase": "approval-value",
        "stdout_tail": "tail-value",
        "stdout": "stdout-value",
        "raw_logs": "logs-value",
        "token": "token-value",
        "api_key": "api-value",
        "secret": "secret-value",
        "password": "password-value",
        "credential": "credential-value",
    }
    event = _full_events()[0]
    event["payload"]["nested"] = sensitive  # type: ignore[index]
    event["payload"]["duplicate"] = "token-value"  # type: ignore[index]

    result = build_governance_replay_audit_report([event])
    serialized = governance_replay_audit_report_to_json(result)

    for key, value in sensitive.items():
        assert f'"{key}"' not in serialized
        assert value not in serialized


def test_input_events_are_not_mutated():
    events = _full_events()
    original = deepcopy(events)

    build_governance_replay_audit_report(events)

    assert events == original


def test_json_serialization_is_deterministic():
    result = build_governance_replay_audit_report(_full_events())

    first = governance_replay_audit_report_to_json(result)
    second = governance_replay_audit_report_to_json(result)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["audit_report_status"] == "pass"


def test_all_safety_fields_remain_false():
    result = build_governance_replay_audit_report(_full_events())

    for key in SAFETY_BOUNDARIES:
        assert result[key] is False
        assert result["safety_boundaries"][key] is False


def test_error_category_taxonomy_is_stable():
    result = build_governance_replay_audit_report(_full_events())

    assert result["error_category_taxonomy"] == list(
        ERROR_CATEGORY_TAXONOMY
    )


def test_module_has_no_execution_or_external_side_effect_surfaces():
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
        "event_driven_governance_kernel",
        "governance_event_canonicalizer",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
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
        "github",
        "openclaw",
        "composio",
        "memory_write",
        "subprocess",
        "socket",
        "urllib",
    ):
        assert forbidden not in source.casefold()
