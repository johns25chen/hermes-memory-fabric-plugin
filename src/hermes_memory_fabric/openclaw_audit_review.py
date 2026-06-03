"""Read-only OpenClaw approved audit JSONL review."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


OPENCLAW_AUDIT_REVIEW_VERSION = "2.7.0"
OPENCLAW_AUDIT_REVIEW_DEFAULT_PATH = "jobs/audit/approved_employee_tasks.jsonl"

ALLOWED_REVIEW_FIELDS = (
    "review_result",
    "audit_id",
    "created_at",
    "source_dryrun_job_id",
    "approved_job_id",
    "agent",
    "risk_level",
    "status",
    "exit_code",
    "assistant_text",
    "task_preview",
    "log_path",
)

FORBIDDEN_REVIEW_FIELDS = (
    "approval_phrase",
    "stdout_tail",
    "stdout",
)


def build_openclaw_audit_review(
    repo_root: str | Path = ".",
    audit_path: str | Path | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    if not isinstance(limit, int) or limit < 1:
        return _base_report(
            repo_root=repo_root,
            audit_path=audit_path,
            status="blocked",
            entries=[],
            blocking_reasons=["limit_must_be_positive_integer"],
            required_actions=["provide_valid_limit"],
            invalid_jsonl_lines=[],
            total_entry_count=0,
            returned_entry_count=0,
            sensitive_fields_removed_count=0,
        )

    root = Path(repo_root).expanduser().resolve(strict=False)
    resolved_path = _resolve_audit_path(root, audit_path)
    if not _is_relative_to(resolved_path, root):
        return _base_report(
            repo_root=root,
            audit_path=resolved_path,
            status="blocked",
            entries=[],
            blocking_reasons=["audit_path_must_be_inside_repo_root"],
            required_actions=["use_repo_local_approved_audit_jsonl"],
            invalid_jsonl_lines=[],
            total_entry_count=0,
            returned_entry_count=0,
            sensitive_fields_removed_count=0,
        )

    if not resolved_path.exists():
        return _base_report(
            repo_root=root,
            audit_path=resolved_path,
            status="missing_audit_log",
            entries=[],
            blocking_reasons=["approved_audit_jsonl_not_found"],
            required_actions=["run_governed_approval_request_dry_run_first"],
            invalid_jsonl_lines=[],
            total_entry_count=0,
            returned_entry_count=0,
            sensitive_fields_removed_count=0,
        )

    if resolved_path.is_dir():
        return _base_report(
            repo_root=root,
            audit_path=resolved_path,
            status="blocked",
            entries=[],
            blocking_reasons=["approved_audit_path_is_directory"],
            required_actions=["provide_approved_audit_jsonl_file"],
            invalid_jsonl_lines=[],
            total_entry_count=0,
            returned_entry_count=0,
            sensitive_fields_removed_count=0,
        )

    entries: list[dict[str, Any]] = []
    invalid_jsonl_lines: list[dict[str, Any]] = []
    sensitive_fields_removed_count = 0

    for line_number, line in enumerate(_read_lines(resolved_path), start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            invalid_jsonl_lines.append({"line_number": line_number, "error": exc.msg})
            continue

        if not isinstance(raw, dict):
            invalid_jsonl_lines.append(
                {"line_number": line_number, "error": "jsonl_record_must_be_object"}
            )
            continue

        sensitive_fields_removed_count += _count_forbidden_keys(raw)
        entries.append(_project_review_entry(raw))

    returned_entries = entries[-limit:]
    status = _status_for(entries, invalid_jsonl_lines)

    blocking_reasons: list[str] = []
    required_actions: list[str] = []
    if status == "blocked":
        blocking_reasons.append("approved_audit_jsonl_contains_no_valid_object_records")
        required_actions.append("repair_approved_audit_jsonl")
    elif invalid_jsonl_lines:
        required_actions.append("inspect_invalid_jsonl_lines")

    return _base_report(
        repo_root=root,
        audit_path=resolved_path,
        status=status,
        entries=returned_entries,
        blocking_reasons=blocking_reasons,
        required_actions=required_actions,
        invalid_jsonl_lines=invalid_jsonl_lines,
        total_entry_count=len(entries),
        returned_entry_count=len(returned_entries),
        sensitive_fields_removed_count=sensitive_fields_removed_count,
    )


def report_to_json(report: Mapping[str, Any]) -> str:
    return json.dumps(dict(report), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _resolve_audit_path(root: Path, audit_path: str | Path | None) -> Path:
    if audit_path is None:
        return (root / OPENCLAW_AUDIT_REVIEW_DEFAULT_PATH).resolve(strict=False)
    candidate = Path(audit_path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve(strict=False)


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()


def _project_review_entry(raw: Mapping[str, Any]) -> dict[str, Any]:
    projected: dict[str, Any] = {}
    for field_name in ALLOWED_REVIEW_FIELDS:
        if field_name in raw:
            projected[field_name] = _sanitize_value(raw[field_name])
    return projected


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): _sanitize_value(inner)
            for key, inner in value.items()
            if str(key) not in FORBIDDEN_REVIEW_FIELDS
        }
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    return value


def _count_forbidden_keys(value: Any) -> int:
    if isinstance(value, dict):
        count = sum(1 for key in value if str(key) in FORBIDDEN_REVIEW_FIELDS)
        return count + sum(_count_forbidden_keys(inner) for inner in value.values())
    if isinstance(value, list):
        return sum(_count_forbidden_keys(item) for item in value)
    return 0


def _status_for(entries: list[dict[str, Any]], invalid_jsonl_lines: list[dict[str, Any]]) -> str:
    if entries and invalid_jsonl_lines:
        return "openclaw_audit_review_ready_with_warnings"
    if entries:
        return "openclaw_audit_review_ready"
    if invalid_jsonl_lines:
        return "blocked"
    return "no_approved_audit_entries"


def _base_report(
    *,
    repo_root: str | Path,
    audit_path: str | Path | None,
    status: str,
    entries: list[dict[str, Any]],
    blocking_reasons: list[str],
    required_actions: list[str],
    invalid_jsonl_lines: list[dict[str, Any]],
    total_entry_count: int,
    returned_entry_count: int,
    sensitive_fields_removed_count: int,
) -> dict[str, Any]:
    root = Path(repo_root).expanduser().resolve(strict=False)
    resolved_path = _resolve_audit_path(root, audit_path)
    return {
        "version": OPENCLAW_AUDIT_REVIEW_VERSION,
        "status": status,
        "dry_run": True,
        "read_only": True,
        "read_only_memory": True,
        "would_mutate_memory": False,
        "invokes_openclaw": False,
        "writes_files": False,
        "source_path": _display_path(root, resolved_path),
        "summary": {
            "total_entry_count": total_entry_count,
            "returned_entry_count": returned_entry_count,
            "invalid_jsonl_line_count": len(invalid_jsonl_lines),
            "sensitive_fields_removed_count": sensitive_fields_removed_count,
            "allowed_fields": list(ALLOWED_REVIEW_FIELDS),
        },
        "entries": entries,
        "invalid_jsonl_lines": invalid_jsonl_lines,
        "blocking_reasons": blocking_reasons,
        "required_actions": required_actions,
    }


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
