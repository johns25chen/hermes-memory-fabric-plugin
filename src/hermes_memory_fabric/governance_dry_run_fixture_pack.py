"""Deterministic local fixture pack for governance dry-run validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_cli_report_envelope import (
    build_governance_cli_report_envelope,
)
from .governance_event_schema_registry import sanitize_governance_event
from .governance_kernel_cli_dry_run import (
    build_governance_kernel_cli_dry_run_result,
)
from .governance_replay_audit_report import (
    build_governance_replay_audit_report,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION = "5.5.0"
GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION = "5.5.0"
GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE = "governance_dry_run_fixture_pack"
GOVERNANCE_DRY_RUN_FIXTURE_HASH_ALGORITHM = "sha256"

FIXTURE_NAMES = (
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
)

_FIXTURE_HASH_EXCLUDES = (
    "deterministic_fixture_hash",
    "events",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_DRY_RUN_FIXTURE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "fixture_hash_excludes": list(_FIXTURE_HASH_EXCLUDES),
    "fixture_hash_uses_sanitized_events": True,
    "input_shape": "sanitized fixture pack projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_events_included": False,
    "sensitive_fields_included": False,
}

_PAYLOADS: dict[str, dict[str, str]] = {
    "governance_kernel_initialized": {
        "kernel_version": GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
        "initialization_scope": "fixture-pack",
    },
    "proposal_submitted": {
        "proposal_id": "fixture-proposal",
        "proposal_type": "fixture-pack",
    },
    "review_completed": {
        "review_id": "fixture-review",
        "review_status": "complete",
    },
    "dry_run_approved": {
        "approval_id": "fixture-approval",
        "approved_for": "plan-preparation-only",
    },
    "dry_run_prepared": {
        "dry_run_id": "fixture-dry-run",
        "plan_id": "fixture-plan",
    },
    "dry_run_completed": {
        "dry_run_id": "fixture-dry-run",
        "completion_status": "recorded-only",
    },
    "attestation_submitted": {
        "attestation_id": "fixture-attestation",
        "attestation_status": "recorded-only",
    },
    "finalization_requested": {
        "finalization_id": "fixture-finalization",
        "requested_scope": "fixture-pack",
    },
    "blocked": {
        "reason": "fixture-blocked",
    },
}

_FULL_SEQUENCE_EVENT_TYPES = tuple(_PAYLOADS)[:-1]
_SENSITIVE_VALUES = {
    "approval_phrase": "fixture-approval-phrase-4-10",
    "stdout_tail": "fixture-stdout-tail-4-10",
    "stdout": "fixture-stdout-4-10",
    "raw_logs": "fixture-raw-logs-4-10",
    "token": "fixture-token-4-10",
    "api_key": "fixture-api-key-4-10",
    "secret": "fixture-secret-4-10",
    "password": "fixture-password-4-10",
    "credential": "fixture-credential-4-10",
}


def build_governance_dry_run_fixture_pack() -> dict[str, Any]:
    """Build the governance fixture pack."""

    fixtures = {
        spec["fixture_name"]: _build_fixture(spec)
        for spec in _fixture_specs()
    }
    fixture_names = list(FIXTURE_NAMES)
    fixture_hashes = {
        name: fixtures[name]["deterministic_fixture_hash"]
        for name in fixture_names
    }
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    pack: dict[str, Any] = {
        "version": GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
        "schema_version": GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
        "fixture_pack_type": GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE,
        "fixture_pack_status": (
            "pass"
            if all(
                fixtures[name]["validation_summary"]["matches_expectations"]
                is True
                for name in fixture_names
            )
            else "blocked"
        ),
        "fixtures": fixtures,
        "fixture_names": fixture_names,
        "fixture_count": len(fixture_names),
        "fixture_hashes": fixture_hashes,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    pack["deterministic_fixture_pack_hash"] = _fixture_pack_hash(pack)
    return _detached_json_value(pack)


def get_governance_dry_run_fixture(name: str) -> dict[str, Any]:
    """Return a detached fixture by stable name."""

    if not isinstance(name, str) or name not in FIXTURE_NAMES:
        return _unknown_fixture(name if isinstance(name, str) else "")
    return _detached_json_value(
        build_governance_dry_run_fixture_pack()["fixtures"][name]
    )


def list_governance_dry_run_fixture_names() -> list[str]:
    """Return stable fixture names."""

    return list(FIXTURE_NAMES)


def governance_dry_run_fixture_pack_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize fixture pack data deterministically."""

    return (
        json.dumps(
            dict(result),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _fixture_specs() -> tuple[dict[str, Any], ...]:
    return (
        {
            "fixture_name": "valid_full_sequence",
            "fixture_kind": "valid_finalizing_sequence",
            "expected_status": "pass",
            "expected_final_state": "finalized",
            "expected_error_categories": [],
            "events": _full_sequence("valid_full_sequence"),
        },
        {
            "fixture_name": "valid_partial_sequence",
            "fixture_kind": "valid_non_final_sequence",
            "expected_status": "pass",
            "expected_final_state": "review_ready",
            "expected_error_categories": [],
            "events": _full_sequence("valid_partial_sequence")[:3],
        },
        {
            "fixture_name": "blocked_event_sequence",
            "fixture_kind": "blocked_event_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["blocked_event"],
            "events": _blocked_event_sequence(),
        },
        {
            "fixture_name": "duplicate_event_id_sequence",
            "fixture_kind": "duplicate_event_id_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["duplicate_event_id"],
            "events": _duplicate_event_id_sequence(),
        },
        {
            "fixture_name": "invalid_previous_event_chain_sequence",
            "fixture_kind": "invalid_previous_event_chain_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["invalid_previous_event_chain"],
            "events": _invalid_previous_event_chain_sequence(),
        },
        {
            "fixture_name": "invalid_transition_sequence",
            "fixture_kind": "invalid_transition_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["invalid_state_transition"],
            "events": _invalid_transition_sequence(),
        },
        {
            "fixture_name": "invalid_payload_schema_sequence",
            "fixture_kind": "invalid_payload_schema_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["invalid_payload_schema"],
            "events": _invalid_payload_schema_sequence(),
        },
        {
            "fixture_name": "malformed_event_sequence",
            "fixture_kind": "malformed_event_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["malformed_event"],
            "events": _malformed_event_sequence(),
        },
        {
            "fixture_name": "unknown_event_type_sequence",
            "fixture_kind": "unknown_event_type_sequence",
            "expected_status": "blocked",
            "expected_final_state": "blocked",
            "expected_error_categories": ["unknown_event_type"],
            "events": _unknown_event_type_sequence(),
        },
        {
            "fixture_name": "sensitive_redaction_sequence",
            "fixture_kind": "sensitive_redaction_sequence",
            "expected_status": "pass",
            "expected_final_state": "finalized",
            "expected_error_categories": [],
            "events": _sensitive_redaction_sequence(),
        },
    )


def _build_fixture(spec: Mapping[str, Any]) -> dict[str, Any]:
    events = _detached_json_value(spec["events"])
    replay_audit_report = build_governance_replay_audit_report(events)
    cli_dry_run_result = build_governance_kernel_cli_dry_run_result(
        {
            "mode": "audit_report",
            "events": events,
        }
    )
    cli_report_envelope = build_governance_cli_report_envelope(
        cli_dry_run_result
    )
    validation_summary = _validation_summary(
        spec,
        replay_audit_report,
        cli_dry_run_result,
        cli_report_envelope,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    fixture: dict[str, Any] = {
        "version": GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
        "schema_version": GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
        "fixture_pack_type": GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE,
        "fixture_name": spec["fixture_name"],
        "fixture_kind": spec["fixture_kind"],
        "expected_status": spec["expected_status"],
        "expected_final_state": spec["expected_final_state"],
        "expected_error_categories": list(spec["expected_error_categories"]),
        "events": events,
        "validation_summary": validation_summary,
        "replay_audit_report": replay_audit_report,
        "cli_dry_run_result": cli_dry_run_result,
        "cli_report_envelope": cli_report_envelope,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    fixture["deterministic_fixture_hash"] = _fixture_hash(fixture)
    return _detached_json_value(fixture)


def _validation_summary(
    spec: Mapping[str, Any],
    replay_audit_report: Mapping[str, Any],
    cli_dry_run_result: Mapping[str, Any],
    cli_report_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    observed_status = (
        "pass"
        if replay_audit_report["audit_report_status"] == "pass"
        and cli_dry_run_result["dry_run_status"] == "pass"
        and cli_report_envelope["envelope_status"] == "pass"
        else "blocked"
    )
    observed_error_categories = list(
        replay_audit_report["error_categories"]
    )
    expected_error_categories = list(spec["expected_error_categories"])
    expected_final_state = spec["expected_final_state"]
    observed_final_state = replay_audit_report["final_state"]
    sensitive_fields_omitted = (
        _events_omit_sensitive_fields(spec["events"])
        or
        replay_audit_report.get("sensitive_fields_omitted") is True
        or cli_report_envelope["report_summary"].get(
            "sensitive_fields_omitted"
        )
        is True
    )
    return {
        "fixture_name": spec["fixture_name"],
        "fixture_kind": spec["fixture_kind"],
        "expected_status": spec["expected_status"],
        "observed_status": observed_status,
        "expected_final_state": expected_final_state,
        "observed_final_state": observed_final_state,
        "expected_error_categories": expected_error_categories,
        "observed_error_categories": observed_error_categories,
        "event_count": replay_audit_report["replay_outcome"][
            "event_count"
        ],
        "accepted_event_count": replay_audit_report[
            "accepted_event_count"
        ],
        "rejected_event_count": replay_audit_report[
            "rejected_event_count"
        ],
        "audit_report_hash": replay_audit_report["audit_report_hash"],
        "deterministic_replay_hash": replay_audit_report[
            "deterministic_replay_hash"
        ],
        "deterministic_sequence_hash": replay_audit_report[
            "deterministic_sequence_hash"
        ],
        "deterministic_cli_hash": cli_dry_run_result[
            "deterministic_cli_hash"
        ],
        "deterministic_envelope_hash": cli_report_envelope[
            "deterministic_envelope_hash"
        ],
        "sensitive_fields_omitted": sensitive_fields_omitted,
        "matches_expected_status": (
            observed_status == spec["expected_status"]
        ),
        "matches_expected_final_state": (
            observed_final_state == expected_final_state
        ),
        "matches_expected_error_categories": (
            observed_error_categories == expected_error_categories
        ),
        "matches_expectations": (
            observed_status == spec["expected_status"]
            and observed_final_state == expected_final_state
            and observed_error_categories == expected_error_categories
        ),
    }


def _event(
    fixture_name: str,
    index: int,
    event_type: str,
    previous_event_id: str | None,
    payload: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    event_payload = (
        dict(payload)
        if payload is not None
        else {
            **_PAYLOADS[event_type],
            "fixture_name": fixture_name,
            "sequence": index,
        }
    )
    return {
        "event_id": f"{fixture_name}-event-{index:02d}",
        "event_type": event_type,
        "actor": "governance-fixture-pack",
        "created_at": f"2026-06-16T04:08:{index:02d}Z",
        "payload": event_payload,
        "previous_event_id": previous_event_id,
        "schema_version": GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
    }


def _full_sequence(fixture_name: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    previous_event_id: str | None = None
    for index, event_type in enumerate(_FULL_SEQUENCE_EVENT_TYPES, start=1):
        event = _event(
            fixture_name,
            index,
            event_type,
            previous_event_id,
        )
        events.append(event)
        previous_event_id = event["event_id"]
    return events


def _blocked_event_sequence() -> list[dict[str, Any]]:
    fixture_name = "blocked_event_sequence"
    first = _event(fixture_name, 1, "governance_kernel_initialized", None)
    second = _event(
        fixture_name,
        2,
        "blocked",
        first["event_id"],
    )
    return [first, second]


def _duplicate_event_id_sequence() -> list[dict[str, Any]]:
    fixture_name = "duplicate_event_id_sequence"
    first = _event(fixture_name, 1, "governance_kernel_initialized", None)
    second = _event(
        fixture_name,
        2,
        "proposal_submitted",
        first["event_id"],
    )
    second["event_id"] = first["event_id"]
    return [first, second]


def _invalid_previous_event_chain_sequence() -> list[dict[str, Any]]:
    fixture_name = "invalid_previous_event_chain_sequence"
    first = _event(fixture_name, 1, "governance_kernel_initialized", None)
    second = _event(
        fixture_name,
        2,
        "proposal_submitted",
        "missing-prior-event",
    )
    return [first, second]


def _invalid_transition_sequence() -> list[dict[str, Any]]:
    fixture_name = "invalid_transition_sequence"
    first = _event(fixture_name, 1, "governance_kernel_initialized", None)
    second = _event(
        fixture_name,
        2,
        "dry_run_completed",
        first["event_id"],
    )
    return [first, second]


def _invalid_payload_schema_sequence() -> list[dict[str, Any]]:
    fixture_name = "invalid_payload_schema_sequence"
    return [
        _event(
            fixture_name,
            1,
            "governance_kernel_initialized",
            None,
            {
                "kernel_version": GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
                "fixture_name": fixture_name,
                "sequence": 1,
            },
        )
    ]


def _malformed_event_sequence() -> list[dict[str, Any]]:
    fixture_name = "malformed_event_sequence"
    event = _event(
        fixture_name,
        1,
        "governance_kernel_initialized",
        None,
    )
    del event["actor"]
    return [event]


def _unknown_event_type_sequence() -> list[dict[str, Any]]:
    fixture_name = "unknown_event_type_sequence"
    return [
        _event(
            fixture_name,
            1,
            "mystery_event",
            None,
            {
                "fixture_name": fixture_name,
                "observation": "local",
                "sequence": 1,
            },
        )
    ]


def _sensitive_redaction_sequence() -> list[dict[str, Any]]:
    fixture_name = "sensitive_redaction_sequence"
    events = _full_sequence(fixture_name)
    events[0]["payload"] = {
        **events[0]["payload"],
        **_SENSITIVE_VALUES,
        "duplicate_marker": _SENSITIVE_VALUES["secret"],
        "nested": {
            "visible": "safe",
            "token": _SENSITIVE_VALUES["token"],
        },
    }
    return events


def _unknown_fixture(name: str) -> dict[str, Any]:
    cli_dry_run_result = build_governance_kernel_cli_dry_run_result(
        {"mode": "unknown_fixture"}
    )
    cli_report_envelope = build_governance_cli_report_envelope(
        cli_dry_run_result
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    fixture: dict[str, Any] = {
        "version": GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
        "schema_version": GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
        "fixture_pack_type": GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE,
        "fixture_name": name,
        "fixture_kind": "unknown_fixture",
        "expected_status": "blocked",
        "expected_final_state": "blocked",
        "expected_error_categories": ["unknown_fixture_name"],
        "events": [],
        "validation_summary": {
            "fixture_name": name,
            "fixture_kind": "unknown_fixture",
            "expected_status": "blocked",
            "observed_status": "blocked",
            "expected_final_state": "blocked",
            "observed_final_state": "blocked",
            "expected_error_categories": ["unknown_fixture_name"],
            "observed_error_categories": ["unknown_fixture_name"],
            "blocking_reasons": ["fixture name is not recognized"],
            "matches_expectations": True,
        },
        "replay_audit_report": None,
        "cli_dry_run_result": cli_dry_run_result,
        "cli_report_envelope": cli_report_envelope,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    fixture["deterministic_fixture_hash"] = _fixture_hash(fixture)
    return _detached_json_value(fixture)


def _fixture_hash(fixture: Mapping[str, Any]) -> str:
    hash_input = {
        key: fixture[key]
        for key in fixture
        if key not in _FIXTURE_HASH_EXCLUDES
    }
    hash_input["sanitized_events"] = _sanitized_events(
        fixture.get("events", [])
    )
    return _hash_json_value(hash_input)


def _fixture_pack_hash(pack: Mapping[str, Any]) -> str:
    hash_input = {
        "version": pack["version"],
        "schema_version": pack["schema_version"],
        "fixture_pack_type": pack["fixture_pack_type"],
        "fixture_pack_status": pack["fixture_pack_status"],
        "fixture_names": pack["fixture_names"],
        "fixture_count": pack["fixture_count"],
        "fixture_hashes": pack["fixture_hashes"],
        "hash_input_contract": pack["hash_input_contract"],
        "safety_boundaries": pack["safety_boundaries"],
    }
    return _hash_json_value(hash_input)


def _sanitized_events(events: Any) -> list[Any]:
    if isinstance(events, (str, bytes, bytearray, Mapping)):
        return []
    try:
        event_sequence = list(events)
    except TypeError:
        return []
    sanitized: list[Any] = []
    for event in event_sequence:
        if isinstance(event, Mapping):
            sanitized.append(sanitize_governance_event(event))
        else:
            sanitized.append({"malformed_event": True})
    return _detached_json_value(sanitized)


def _events_omit_sensitive_fields(events: Any) -> bool:
    if isinstance(events, (str, bytes, bytearray, Mapping)):
        return False
    try:
        event_sequence = list(events)
    except TypeError:
        return False
    return any(
        isinstance(event, Mapping)
        and sanitize_governance_event(event).get("sensitive_fields_omitted")
        is True
        for event in event_sequence
    )


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        _detached_json_value(value),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            _reject_non_finite(value),
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _reject_non_finite(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError("mapping keys must be strings")
        return {key: _reject_non_finite(value[key]) for key in value}
    if isinstance(value, list):
        return [_reject_non_finite(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("floats must be finite")
        return value
    raise ValueError("value must be deterministic JSON-compatible")


__all__ = [
    "GOVERNANCE_DRY_RUN_FIXTURE_HASH_ALGORITHM",
    "GOVERNANCE_DRY_RUN_FIXTURE_PACK_TYPE",
    "GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION",
    "GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION",
    "SAFETY_BOUNDARIES",
    "build_governance_dry_run_fixture_pack",
    "get_governance_dry_run_fixture",
    "governance_dry_run_fixture_pack_to_json",
    "list_governance_dry_run_fixture_names",
]
