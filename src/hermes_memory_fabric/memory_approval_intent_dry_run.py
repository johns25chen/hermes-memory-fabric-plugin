"""v1.7 dry-run adapter from v1.5 proposal previews to approval intent."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from hermes_memory_fabric.memory_executor_surface_lockdown_audit import (
    audit_executor_surface_lockdown,
)


MEMORY_APPROVAL_INTENT_DRY_RUN_VERSION = "1.7.0"
SOURCE_PREVIEW_VERSION = "1.5.0"
INTENT_KIND = "memory_write_proposal_approval_intent_candidate"

SOURCE_REQUIRED_KEYS = (
    "version",
    "dry_run",
    "accepted_count",
    "rejected_count",
    "locked_count",
    "created_real_proposal",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_memory",
    "writes_graph",
    "writes_config",
    "writes_sqlite",
    "writes_token_files",
    "writes_approval_audit",
    "applies_proposals",
    "provider_tools",
    "proposal_previews",
    "rejected_candidates",
    "safety_summary",
)

SOURCE_FALSE_WRITE_FLAGS = (
    "created_real_proposal",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_memory",
    "writes_graph",
    "writes_config",
    "writes_sqlite",
    "writes_token_files",
    "writes_approval_audit",
    "applies_proposals",
)

INTENT_NO_WRITE_FLAGS = {
    "approval_token_issued": False,
    "approval_token_id": None,
    "creates_real_proposal": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_memory": False,
    "writes_graph": False,
    "writes_config": False,
    "writes_sqlite": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_executor": False,
    "applies_proposals": False,
    "provider_tools": [],
}


def run_memory_approval_intent_dry_run(
    source_preview: Mapping[str, Any],
    *,
    repo_root: str | Path = ".",
) -> dict[str, Any]:
    """Create a deterministic approval-intent candidate from a v1.5 preview.

    The result is an intent object only. It does not issue tokens, create real
    proposals, append ledgers, invoke executors, or write memory.
    """

    source = deepcopy(dict(source_preview)) if isinstance(source_preview, Mapping) else {}
    audit_report = audit_executor_surface_lockdown(repo_root)
    validation = _validate_source_preview(source)
    audit_snapshot = _audit_snapshot(audit_report)
    accepted_count = _count(source.get("accepted_count"))
    locked_count = _count(source.get("locked_count"))
    rejected_count = _count(source.get("rejected_count"))
    status = _approval_intent_status(validation, audit_snapshot, accepted_count=accepted_count)

    result = {
        "version": MEMORY_APPROVAL_INTENT_DRY_RUN_VERSION,
        "dry_run": True,
        "approval_intent_status": status,
        "approval_intent_id": _approval_intent_id(source, audit_snapshot),
        "source_preview_version": source.get("version"),
        "source_accepted_count": accepted_count,
        "source_locked_count": locked_count,
        "source_rejected_count": rejected_count,
        "intent_kind": INTENT_KIND,
        "intent_summary": _intent_summary(
            status=status,
            accepted_count=accepted_count,
            locked_count=locked_count,
            rejected_count=rejected_count,
            validation=validation,
            audit_snapshot=audit_snapshot,
        ),
        "human_review_required": True,
        "required_human_decision": _required_human_decision(status),
        **deepcopy(INTENT_NO_WRITE_FLAGS),
        "safety_summary": _safety_summary(validation, audit_snapshot),
        "source_preview_snapshot": source,
    }
    return deepcopy(result)


def memory_approval_intent_dry_run(
    source_preview: Mapping[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias for the v1.7 approval-intent dry-run entry point."""

    return run_memory_approval_intent_dry_run(source_preview, **kwargs)


def approval_intent_dry_run_to_json(result: Mapping[str, Any]) -> str:
    """Serialize an approval-intent dry-run result deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _validate_source_preview(source: Mapping[str, Any]) -> dict[str, Any]:
    missing = [key for key in SOURCE_REQUIRED_KEYS if key not in source]
    errors = [f"missing_{key}" for key in missing]

    if source.get("version") != SOURCE_PREVIEW_VERSION:
        errors.append("source_preview_version_must_be_1.5.0")
    if source.get("dry_run") is not True:
        errors.append("source_preview_dry_run_must_be_true")

    true_write_flags = [flag for flag in SOURCE_FALSE_WRITE_FLAGS if source.get(flag) is True]
    errors.extend(f"source_{flag}_must_be_false" for flag in true_write_flags)

    provider_tools = source.get("provider_tools")
    if provider_tools != []:
        errors.append("source_provider_tools_must_be_empty")

    count_errors = []
    for key in ("accepted_count", "locked_count", "rejected_count"):
        if key in source and not _is_non_negative_int(source.get(key)):
            count_errors.append(f"{key}_must_be_non_negative_int")
    errors.extend(count_errors)

    return {
        "valid": not errors,
        "errors": _dedupe(errors),
        "missing_keys": missing,
        "true_write_flags": true_write_flags,
        "provider_tools": deepcopy(provider_tools),
    }


def _approval_intent_status(
    validation: Mapping[str, Any],
    audit_snapshot: Mapping[str, Any],
    *,
    accepted_count: int,
) -> str:
    if validation.get("valid") is not True:
        return "rejected"
    if audit_snapshot.get("audit_status") != "pass":
        return "rejected"
    if accepted_count > 0:
        return "ready"
    return "locked"


def _audit_snapshot(audit_report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": audit_report.get("version"),
        "dry_run": audit_report.get("dry_run"),
        "audit_status": audit_report.get("audit_status"),
        "provider_tools": deepcopy(audit_report.get("provider_tools")),
        "forbidden_files_present": len(audit_report.get("forbidden_files_present", [])),
        "forbidden_calls": len(audit_report.get("forbidden_calls", [])),
        "forbidden_write_surfaces": len(audit_report.get("forbidden_write_surfaces", [])),
        "missing_no_write_flags": len(audit_report.get("missing_no_write_flags", [])),
        "v15_boundary_status": audit_report.get("v15_boundary_status"),
        "writes_hermes_home": False,
    }


def _intent_summary(
    *,
    status: str,
    accepted_count: int,
    locked_count: int,
    rejected_count: int,
    validation: Mapping[str, Any],
    audit_snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "status": status,
        "ready_for_human_review": status == "ready",
        "source_accepted_count": accepted_count,
        "source_locked_count": locked_count,
        "source_rejected_count": rejected_count,
        "source_preview_valid": validation.get("valid") is True,
        "source_errors": list(validation.get("errors", [])),
        "audit_status": audit_snapshot.get("audit_status"),
        "v16_audit_required": True,
        "v16_audit_passed": audit_snapshot.get("audit_status") == "pass",
        "approval_token_issued": False,
        "creates_real_proposal": False,
        "writes_any_memory_state": False,
    }


def _safety_summary(
    validation: Mapping[str, Any],
    audit_snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "adapter": "memory_approval_intent_dry_run",
        "version": MEMORY_APPROVAL_INTENT_DRY_RUN_VERSION,
        "dry_run_only": True,
        "source_preview_required_version": SOURCE_PREVIEW_VERSION,
        "source_preview_valid": validation.get("valid") is True,
        "source_preview_errors": list(validation.get("errors", [])),
        "v16_executor_surface_lockdown_audit": audit_snapshot,
        "human_review_required": True,
        "approval_token_issued": False,
        "approval_token_id": None,
        "creates_real_proposal": False,
        "writes_proposal_files": False,
        "writes_operation_ledger": False,
        "writes_memory": False,
        "writes_graph": False,
        "writes_config": False,
        "writes_sqlite": False,
        "writes_token_files": False,
        "writes_approval_audit": False,
        "invokes_real_executor": False,
        "applies_proposals": False,
        "provider_tools": [],
        "create_memory_write_proposal_called": False,
        "approval_tokens_created": False,
        "operation_ledger_appended": False,
        "memory_written": False,
        "executor_invoked": False,
    }


def _approval_intent_id(source: Mapping[str, Any], audit_snapshot: Mapping[str, Any]) -> str:
    payload = {
        "version": MEMORY_APPROVAL_INTENT_DRY_RUN_VERSION,
        "intent_kind": INTENT_KIND,
        "source_preview_version": source.get("version"),
        "source_accepted_count": source.get("accepted_count"),
        "source_locked_count": source.get("locked_count"),
        "source_rejected_count": source.get("rejected_count"),
        "source_dry_run": source.get("dry_run"),
        "source_write_flags": {flag: source.get(flag) for flag in SOURCE_FALSE_WRITE_FLAGS},
        "source_provider_tools": source.get("provider_tools"),
        "proposal_preview_ids": _proposal_preview_ids(source.get("proposal_previews")),
        "rejected_candidate_ids": _rejected_candidate_ids(source.get("rejected_candidates")),
        "audit_status": audit_snapshot.get("audit_status"),
        "v15_boundary_status": audit_snapshot.get("v15_boundary_status"),
    }
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "approval-intent-dry-run-" + hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:32]


def _proposal_preview_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    ids: list[str] = []
    for item in value:
        if isinstance(item, Mapping):
            ids.append(str(item.get("candidate_id", "")))
        else:
            ids.append("")
    return ids


def _rejected_candidate_ids(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    ids: list[str] = []
    for item in value:
        if isinstance(item, Mapping):
            ids.append(str(item.get("candidate_id", "")))
        else:
            ids.append("")
    return ids


def _required_human_decision(status: str) -> str:
    if status == "ready":
        return "review_approval_intent_candidate"
    if status == "locked":
        return "none_no_accepted_source_previews"
    return "repair_source_preview_or_v16_audit_before_review"


def _is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and value >= 0 and not isinstance(value, bool)


def _count(value: Any) -> int:
    if _is_non_negative_int(value):
        return int(value)
    return 0


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


__all__ = [
    "MEMORY_APPROVAL_INTENT_DRY_RUN_VERSION",
    "SOURCE_PREVIEW_VERSION",
    "INTENT_KIND",
    "SOURCE_REQUIRED_KEYS",
    "SOURCE_FALSE_WRITE_FLAGS",
    "INTENT_NO_WRITE_FLAGS",
    "run_memory_approval_intent_dry_run",
    "memory_approval_intent_dry_run",
    "approval_intent_dry_run_to_json",
]
