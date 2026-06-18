"""Deterministic local report envelope for governance CLI dry-run results."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_kernel_cli_dry_run import (
    build_governance_kernel_cli_dry_run_result,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION = "5.8.0"
GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION = "5.8.0"
GOVERNANCE_CLI_REPORT_ENVELOPE_TYPE = "governance_cli_report_envelope"
GOVERNANCE_CLI_REPORT_ENVELOPE_HASH_ALGORITHM = "sha256"
SOURCE_REPORT_TYPE = "governance_kernel_cli_dry_run"

_SENSITIVE_KEYS = frozenset(
    {
        "approval_phrase",
        "stdout_tail",
        "stdout",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
    }
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_CLI_REPORT_ENVELOPE_HASH_ALGORITHM,
    "encoding": "utf-8",
    "envelope_hash_excludes": ["deterministic_envelope_hash"],
    "envelope_hash_scope": "full sanitized envelope projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_cli_result_included": False,
    "report_hash_scope": "sanitized wrapped CLI dry-run report only",
    "sensitive_fields_included": False,
}


def build_governance_cli_report_envelope(
    cli_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Wrap one governance CLI dry-run result in a deterministic envelope."""

    if not isinstance(cli_result, Mapping):
        return _envelope(
            report=None,
            requested_mode=None,
            dry_run_status="blocked",
            source_report_version=None,
            malformed_reasons=["cli_result must be a mapping"],
            sensitive_fields_omitted=False,
        )

    compatibility_reasons = _json_compatibility_reasons(cli_result)
    if compatibility_reasons:
        return _envelope(
            report=None,
            requested_mode=None,
            dry_run_status="blocked",
            source_report_version=None,
            malformed_reasons=compatibility_reasons,
            sensitive_fields_omitted=False,
        )

    sensitive_values = _collect_sensitive_scalar_values(cli_result)
    sanitized_report, sensitive_fields_omitted = _sanitize_value(
        cli_result,
        sensitive_values,
    )
    if not isinstance(sanitized_report, dict):
        return _envelope(
            report=None,
            requested_mode=None,
            dry_run_status="blocked",
            source_report_version=None,
            malformed_reasons=["cli_result must sanitize to a mapping"],
            sensitive_fields_omitted=sensitive_fields_omitted,
        )

    malformed_reasons = _cli_result_malformed_reasons(sanitized_report)
    source_dry_run_status = sanitized_report.get("dry_run_status")
    dry_run_status = (
        source_dry_run_status
        if source_dry_run_status in {"pass", "blocked"}
        else "blocked"
    )
    source_report_version = sanitized_report.get("version")
    requested_mode = sanitized_report.get("requested_mode")
    return _envelope(
        report=sanitized_report,
        requested_mode=requested_mode if isinstance(requested_mode, str) else None,
        dry_run_status=dry_run_status,
        source_report_version=(
            source_report_version
            if isinstance(source_report_version, str)
            else None
        ),
        malformed_reasons=malformed_reasons,
        sensitive_fields_omitted=(
            sensitive_fields_omitted
            or _sensitive_fields_omitted_in_report(sanitized_report)
        ),
    )


def build_governance_cli_report_envelope_from_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a CLI dry-run result from a payload and wrap it locally."""

    cli_result = build_governance_kernel_cli_dry_run_result(payload)
    return build_governance_cli_report_envelope(cli_result)


def governance_cli_report_envelope_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a report envelope deterministically."""

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


def _envelope(
    *,
    report: Mapping[str, Any] | None,
    requested_mode: str | None,
    dry_run_status: str,
    source_report_version: str | None,
    malformed_reasons: Sequence[str],
    sensitive_fields_omitted: bool,
) -> dict[str, Any]:
    malformed_reason_list = _deduplicate(list(malformed_reasons))
    report_value = _detached_json_value(report) if report is not None else None
    report_summary = _report_summary(
        report_value,
        requested_mode=requested_mode,
        dry_run_status=dry_run_status,
        malformed_reasons=malformed_reason_list,
        sensitive_fields_omitted=sensitive_fields_omitted,
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    envelope_status = (
        "pass"
        if dry_run_status == "pass" and not malformed_reason_list
        else "blocked"
    )
    envelope: dict[str, Any] = {
        "version": GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION,
        "schema_version": GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION,
        "envelope_type": GOVERNANCE_CLI_REPORT_ENVELOPE_TYPE,
        "envelope_status": envelope_status,
        "source_report_type": SOURCE_REPORT_TYPE,
        "source_report_version": source_report_version,
        "requested_mode": requested_mode,
        "dry_run_status": dry_run_status,
        "report": report_value,
        "report_summary": report_summary,
        "report_metadata": _report_metadata(),
        "deterministic_report_hash": _hash_json_value(report_value),
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    envelope["deterministic_envelope_hash"] = _deterministic_envelope_hash(
        envelope
    )
    return _detached_json_value(envelope)


def _report_metadata() -> dict[str, Any]:
    return {
        "envelope_created_by": "local_cli_report_envelope_dry_run",
        "local_only": True,
        "deterministic": True,
        "no_execution": True,
        "no_writes": True,
        "no_external_calls": True,
        "star_soul_13_5_transition_corridor": True,
        "star_cosmos_entry_claimed": False,
    }


def _report_summary(
    report: Any,
    *,
    requested_mode: str | None,
    dry_run_status: str,
    malformed_reasons: Sequence[str],
    sensitive_fields_omitted: bool,
) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "requested_mode": requested_mode,
        "dry_run_status": dry_run_status,
        "blocking_reason_count": _blocking_reason_count(
            report,
            malformed_reasons,
        ),
        "sensitive_fields_omitted": sensitive_fields_omitted,
        "safety_status": "safe",
    }
    nested_result = report.get("result") if isinstance(report, Mapping) else None
    for key, value in (
        ("final_state", _first_report_value(nested_result, ("final_state", "current_state"))),
        ("event_count", _first_report_value(nested_result, ("event_count",))),
        (
            "accepted_event_count",
            _first_report_value(nested_result, ("accepted_event_count",)),
        ),
        (
            "rejected_event_count",
            _first_report_value(nested_result, ("rejected_event_count",)),
        ),
    ):
        if value is not None:
            summary[key] = value
    return summary


def _first_report_value(value: Any, keys: Sequence[str]) -> Any:
    if not isinstance(value, Mapping):
        return None
    for key in keys:
        candidate = value.get(key)
        if isinstance(candidate, (str, int)) and not isinstance(candidate, bool):
            return candidate
    for nested_key in (
        "final_report",
        "replay_outcome",
        "replay_report",
        "replay_audit_report",
    ):
        nested_value = value.get(nested_key)
        nested_candidate = _first_report_value(nested_value, keys)
        if nested_candidate is not None:
            return nested_candidate
    return None


def _blocking_reason_count(
    report: Any,
    malformed_reasons: Sequence[str],
) -> int:
    reasons = list(malformed_reasons)
    if isinstance(report, Mapping):
        report_reasons = report.get("blocking_reasons")
        if isinstance(report_reasons, list):
            reasons.extend(
                reason for reason in report_reasons if isinstance(reason, str)
            )
    return len(_deduplicate(reasons))


def _cli_result_malformed_reasons(report: Mapping[str, Any]) -> list[str]:
    reasons: list[str] = []
    if not isinstance(report.get("version"), str):
        reasons.append("cli_result version must be a string")
    if report.get("dry_run_status") not in {"pass", "blocked"}:
        reasons.append("cli_result dry_run_status must be pass or blocked")
    requested_mode = report.get("requested_mode")
    if requested_mode is not None and not isinstance(requested_mode, str):
        reasons.append("cli_result requested_mode must be a string or null")
    if "result" not in report:
        reasons.append("cli_result result field is required")
    blocking_reasons = report.get("blocking_reasons")
    if not isinstance(blocking_reasons, list) or not all(
        isinstance(reason, str) for reason in blocking_reasons
    ):
        reasons.append("cli_result blocking_reasons must be a list of strings")
    return _deduplicate(reasons)


def _json_compatibility_reasons(value: Any) -> list[str]:
    reasons: list[str] = []

    def inspect(nested_value: Any) -> None:
        if isinstance(nested_value, Mapping):
            for key, child_value in nested_value.items():
                if not isinstance(key, str):
                    reasons.append("mapping keys must be strings")
                    continue
                inspect(child_value)
            return
        if isinstance(nested_value, list):
            for item in nested_value:
                inspect(item)
            return
        if nested_value is None or isinstance(nested_value, (str, bool, int)):
            return
        if isinstance(nested_value, float):
            if not math.isfinite(nested_value):
                reasons.append("floats must be finite")
            return
        reasons.append("values must be deterministic JSON-compatible")

    inspect(value)
    return _deduplicate(reasons)


def _collect_sensitive_scalar_values(
    value: Any,
    *,
    sensitive_context: bool = False,
) -> set[tuple[type[Any], Any]]:
    collected: set[tuple[type[Any], Any]] = set()
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            nested_sensitive = (
                sensitive_context
                or isinstance(key, str)
                and key.casefold() in _SENSITIVE_KEYS
            )
            collected.update(
                _collect_sensitive_scalar_values(
                    nested_value,
                    sensitive_context=nested_sensitive,
                )
            )
        return collected
    if isinstance(value, list):
        for item in value:
            collected.update(
                _collect_sensitive_scalar_values(
                    item,
                    sensitive_context=sensitive_context,
                )
            )
        return collected
    if sensitive_context and (
        isinstance(value, str)
        or isinstance(value, int)
        and not isinstance(value, bool)
        or isinstance(value, float)
        and math.isfinite(value)
    ):
        collected.add((type(value), value))
    return collected


def _sanitize_value(
    value: Any,
    sensitive_values: set[tuple[type[Any], Any]],
) -> tuple[Any, bool]:
    if isinstance(value, Mapping):
        sanitized: dict[str, Any] = {}
        sensitive_fields_omitted = False
        for key in sorted(key for key in value if isinstance(key, str)):
            if key.casefold() in _SENSITIVE_KEYS:
                sensitive_fields_omitted = True
                continue
            nested_value, nested_omitted = _sanitize_value(
                value[key],
                sensitive_values,
            )
            sanitized[key] = nested_value
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized, sensitive_fields_omitted
    if isinstance(value, list):
        sanitized_items: list[Any] = []
        sensitive_fields_omitted = False
        for item in value:
            nested_value, nested_omitted = _sanitize_value(
                item,
                sensitive_values,
            )
            sanitized_items.append(nested_value)
            sensitive_fields_omitted = (
                sensitive_fields_omitted or nested_omitted
            )
        return sanitized_items, sensitive_fields_omitted
    if (
        isinstance(value, str)
        or isinstance(value, int)
        and not isinstance(value, bool)
        or isinstance(value, float)
        and math.isfinite(value)
    ) and (type(value), value) in sensitive_values:
        return "<sensitive value omitted>", True
    return value, False


def _sensitive_fields_omitted_in_report(value: Any) -> bool:
    if isinstance(value, Mapping):
        if value.get("sensitive_fields_omitted") is True:
            return True
        return any(
            _sensitive_fields_omitted_in_report(nested_value)
            for nested_value in value.values()
        )
    if isinstance(value, list):
        return any(_sensitive_fields_omitted_in_report(item) for item in value)
    return False


def _deterministic_envelope_hash(envelope: Mapping[str, Any]) -> str:
    hash_input = {
        key: envelope[key]
        for key in envelope
        if key != "deterministic_envelope_hash"
    }
    return _hash_json_value(hash_input)


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


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
    "GOVERNANCE_CLI_REPORT_ENVELOPE_HASH_ALGORITHM",
    "GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION",
    "GOVERNANCE_CLI_REPORT_ENVELOPE_TYPE",
    "GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION",
    "HASH_INPUT_CONTRACT",
    "SAFETY_BOUNDARIES",
    "build_governance_cli_report_envelope",
    "build_governance_cli_report_envelope_from_payload",
    "governance_cli_report_envelope_to_json",
]
