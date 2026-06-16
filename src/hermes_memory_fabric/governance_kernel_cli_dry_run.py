"""Deterministic local CLI dry-run facade for governance event inspection."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
import sys
from typing import Any

from .event_driven_governance_kernel import replay_governance_events
from .governance_event_canonicalizer import (
    canonicalize_governance_event,
    canonicalize_governance_event_sequence,
)
from .governance_event_schema_registry import (
    sanitize_governance_event,
    validate_event_against_schema_registry,
)
from .governance_local_event_store_dry_run import (
    append_governance_events_to_local_store_dry_run,
    build_governance_local_event_store_replay_report_dry_run,
    create_governance_local_event_store_dry_run,
)
from .governance_replay_audit_report import (
    build_governance_replay_audit_report,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION = "5.0.0"
GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION = "5.0.0"
GOVERNANCE_KERNEL_CLI_MODE = "local_cli_dry_run_only"
GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM = "sha256"

_EVENT_MODES = frozenset({"validate_event", "canonicalize_event"})
_SEQUENCE_MODES = frozenset(
    {
        "canonicalize_sequence",
        "replay_sequence",
        "audit_report",
        "local_store_replay",
    }
)
_SUPPORTED_MODES = _EVENT_MODES | _SEQUENCE_MODES

_CLI_HASH_FIELDS = (
    "version",
    "schema_version",
    "cli_mode",
    "requested_mode",
    "dry_run_status",
    "result",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_CLI_HASH_FIELDS),
    "input_shape": "sanitized governance CLI dry-run result projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_payload_included": False,
    "sensitive_fields_included": False,
}


def build_governance_kernel_cli_dry_run_result(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a deterministic local CLI dry-run result."""

    if not isinstance(payload, Mapping):
        return _blocked_result(
            requested_mode=None,
            result=None,
            blocking_reasons=["payload must be a mapping"],
        )

    requested_mode = _requested_mode_for_output(payload)
    if not _json_compatible(payload):
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=[
                "payload must contain deterministic JSON-compatible values"
            ],
        )

    detached_payload = _detached_json_value(payload)
    if not isinstance(detached_payload, dict):
        return _blocked_result(
            requested_mode=None,
            result=None,
            blocking_reasons=["payload must be a mapping"],
        )

    requested_mode = _requested_mode_for_output(detached_payload)
    mode = detached_payload.get("mode")
    if not isinstance(mode, str) or not mode.strip():
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=["mode must be a non-empty string"],
        )
    if mode not in _SUPPORTED_MODES:
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=["mode is not supported"],
        )

    try:
        if mode == "validate_event":
            event, event_reasons = _required_event(detached_payload)
            if event_reasons:
                return _blocked_result(
                    requested_mode=requested_mode,
                    result=None,
                    blocking_reasons=event_reasons,
                )
            return _validate_event_result(requested_mode, event)

        if mode == "canonicalize_event":
            event, event_reasons = _required_event(detached_payload)
            if event_reasons:
                return _blocked_result(
                    requested_mode=requested_mode,
                    result=None,
                    blocking_reasons=event_reasons,
                )
            return _canonicalize_event_result(requested_mode, event)

        events, events_reasons = _required_events(detached_payload)
        if events_reasons:
            return _blocked_result(
                requested_mode=requested_mode,
                result=None,
                blocking_reasons=events_reasons,
            )

        if mode == "canonicalize_sequence":
            return _canonicalize_sequence_result(requested_mode, events)
        if mode == "replay_sequence":
            return _replay_sequence_result(requested_mode, events)
        if mode == "audit_report":
            return _audit_report_result(requested_mode, events)
        if mode == "local_store_replay":
            return _local_store_replay_result(requested_mode, detached_payload, events)
    except (TypeError, ValueError):
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=["governance CLI dry run failed closed"],
        )

    return _blocked_result(
        requested_mode=requested_mode,
        result=None,
        blocking_reasons=["mode is not supported"],
    )


def governance_kernel_cli_dry_run_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a CLI dry-run result deterministically."""

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


def main(
    argv: Sequence[str] | None = None,
    stdin_text: str | None = None,
) -> int:
    """Run the local JSON CLI dry-run interface."""

    input_text, mode_override, arg_reasons = _parse_args(
        list(argv) if argv is not None else sys.argv[1:]
    )
    if arg_reasons:
        result = _blocked_result(
            requested_mode=mode_override,
            result=None,
            blocking_reasons=arg_reasons,
        )
        print(governance_kernel_cli_dry_run_to_json(result), end="")
        return 1

    if input_text is None:
        input_text = stdin_text if stdin_text is not None else sys.stdin.read()

    try:
        decoded = json.loads(input_text)
    except json.JSONDecodeError:
        result = _blocked_result(
            requested_mode=mode_override,
            result=None,
            blocking_reasons=["input must be valid JSON"],
        )
        print(governance_kernel_cli_dry_run_to_json(result), end="")
        return 1

    if mode_override is not None:
        if not isinstance(decoded, Mapping):
            result = _blocked_result(
                requested_mode=mode_override,
                result=None,
                blocking_reasons=["payload must be a mapping"],
            )
            print(governance_kernel_cli_dry_run_to_json(result), end="")
            return 1
        decoded = {**dict(decoded), "mode": mode_override}

    result = build_governance_kernel_cli_dry_run_result(decoded)
    print(governance_kernel_cli_dry_run_to_json(result), end="")
    return 0 if result["dry_run_status"] == "pass" else 1


def _validate_event_result(
    requested_mode: str | None,
    event: Mapping[str, Any],
) -> dict[str, Any]:
    result = validate_event_against_schema_registry(event)
    return _result(
        requested_mode=requested_mode,
        dry_run_status="pass" if result["valid"] is True else "blocked",
        result=result,
        blocking_reasons=result["blocking_reasons"],
    )


def _canonicalize_event_result(
    requested_mode: str | None,
    event: Mapping[str, Any],
) -> dict[str, Any]:
    try:
        result = canonicalize_governance_event(event)
    except ValueError as exc:
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=_canonicalization_reasons(exc),
        )
    return _result(
        requested_mode=requested_mode,
        dry_run_status="pass",
        result=result,
        blocking_reasons=[],
    )


def _canonicalize_sequence_result(
    requested_mode: str | None,
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    result = canonicalize_governance_event_sequence(events)
    return _result(
        requested_mode=requested_mode,
        dry_run_status=(
            "pass"
            if result["canonicalization_status"] == "pass"
            else "blocked"
        ),
        result=result,
        blocking_reasons=result["blocking_reasons"],
    )


def _replay_sequence_result(
    requested_mode: str | None,
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    result = replay_governance_events(events)
    return _result(
        requested_mode=requested_mode,
        dry_run_status=(
            "pass" if result["audit_status"] == "pass" else "blocked"
        ),
        result=result,
        blocking_reasons=result["blocking_reasons"],
    )


def _audit_report_result(
    requested_mode: str | None,
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    result = build_governance_replay_audit_report(events)
    return _result(
        requested_mode=requested_mode,
        dry_run_status=(
            "pass"
            if result["audit_report_status"] == "pass"
            else "blocked"
        ),
        result=result,
        blocking_reasons=result["blocking_reasons"],
    )


def _local_store_replay_result(
    requested_mode: str | None,
    payload: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    store = payload.get("store", create_governance_local_event_store_dry_run())
    if not isinstance(store, Mapping):
        return _blocked_result(
            requested_mode=requested_mode,
            result=None,
            blocking_reasons=["store must be a mapping"],
        )

    append_result = append_governance_events_to_local_store_dry_run(
        store,
        events,
    )
    replay_report = build_governance_local_event_store_replay_report_dry_run(
        append_result["store"],
    )
    result = {
        "append_sequence": append_result,
        "final_state": replay_report["final_state"],
        "replay_report": replay_report,
    }
    blocking_reasons = _deduplicate(
        [
            *append_result["blocking_reasons"],
            *replay_report["blocking_reasons"],
            *replay_report["replay_audit_report"]["blocking_reasons"],
        ]
    )
    dry_run_status = (
        "pass"
        if append_result["append_sequence_status"] == "pass"
        and replay_report["replay_report_status"] == "pass"
        else "blocked"
    )
    return _result(
        requested_mode=requested_mode,
        dry_run_status=dry_run_status,
        result=result,
        blocking_reasons=blocking_reasons,
    )


def _required_event(
    payload: Mapping[str, Any],
) -> tuple[Mapping[str, Any], list[str]]:
    event = payload.get("event")
    if not isinstance(event, Mapping):
        return {}, ["event must be a mapping"]
    return event, []


def _required_events(
    payload: Mapping[str, Any],
) -> tuple[list[Mapping[str, Any]], list[str]]:
    events = payload.get("events")
    if isinstance(events, (str, bytes, bytearray, Mapping)):
        return [], ["events must be a sequence of mappings"]
    if not isinstance(events, Sequence):
        return [], ["events must be a sequence of mappings"]
    event_sequence = list(events)
    if not all(isinstance(event, Mapping) for event in event_sequence):
        return [], ["events must be a sequence of mappings"]
    return event_sequence, []


def _result(
    *,
    requested_mode: str | None,
    dry_run_status: str,
    result: Any,
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    output = {
        "version": GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION,
        "schema_version": GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION,
        "cli_mode": GOVERNANCE_KERNEL_CLI_MODE,
        "requested_mode": requested_mode,
        "dry_run_status": dry_run_status,
        "result": _detached_json_value(result),
        "blocking_reasons": _deduplicate(list(blocking_reasons)),
        "hash_algorithm": GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    output["deterministic_cli_hash"] = _deterministic_cli_hash(output)
    return _detached_json_value(output)


def _blocked_result(
    *,
    requested_mode: str | None,
    result: Any,
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    return _result(
        requested_mode=requested_mode,
        dry_run_status="blocked",
        result=result,
        blocking_reasons=blocking_reasons,
    )


def _requested_mode_for_output(payload: Mapping[str, Any]) -> str | None:
    sanitized_payload = sanitize_governance_event(payload)
    mode = sanitized_payload.get("mode")
    return mode if isinstance(mode, str) else None


def _parse_args(
    argv: Sequence[str],
) -> tuple[str | None, str | None, list[str]]:
    input_text: str | None = None
    mode_override: str | None = None
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--input-json":
            if index + 1 >= len(argv):
                return None, mode_override, ["--input-json requires a value"]
            input_text = argv[index + 1]
            index += 2
            continue
        if arg == "--mode":
            if index + 1 >= len(argv):
                return input_text, None, ["--mode requires a value"]
            mode_override = argv[index + 1]
            index += 2
            continue
        return input_text, mode_override, ["unknown argument"]
    return input_text, mode_override, []


def _canonicalization_reasons(exc: ValueError) -> list[str]:
    message = str(exc)
    prefix = "governance event canonicalization blocked: "
    details = message[len(prefix) :] if message.startswith(prefix) else message
    return _deduplicate(
        [reason.strip() for reason in details.split(";") if reason.strip()]
    )


def _deterministic_cli_hash(result: Mapping[str, Any]) -> str:
    hash_input = {
        field: result[field]
        for field in _CLI_HASH_FIELDS
    }
    serialized = json.dumps(
        hash_input,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _json_compatible(value: Any) -> bool:
    if isinstance(value, Mapping):
        return all(
            isinstance(key, str) and _json_compatible(nested_value)
            for key, nested_value in value.items()
        )
    if isinstance(value, list):
        return all(_json_compatible(item) for item in value)
    if value is None or isinstance(value, (str, bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    return False


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION",
    "GOVERNANCE_KERNEL_CLI_HASH_ALGORITHM",
    "GOVERNANCE_KERNEL_CLI_MODE",
    "GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION",
    "HASH_INPUT_CONTRACT",
    "SAFETY_BOUNDARIES",
    "build_governance_kernel_cli_dry_run_result",
    "governance_kernel_cli_dry_run_to_json",
    "main",
]
