"""Read-only OpenClaw approved audit review tool."""

from __future__ import annotations

import json
from typing import Any

from hermes_memory_fabric.openclaw_audit_review import (
    OPENCLAW_AUDIT_REVIEW_DEFAULT_PATH,
    build_openclaw_audit_review,
)
from hermes_memory_fabric.tools.local_registry import registry, tool_error


OPENCLAW_AUDIT_REVIEW_SCHEMA = {
    "name": "openclaw_audit_review",
    "description": (
        "Read-only review of approved OpenClaw audit JSONL records. It reads "
        "jobs/audit/approved_employee_tasks.jsonl, returns only an allowlisted "
        "field projection, never executes OpenClaw, and never exposes approval "
        "phrases or stdout payloads."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "repo_root": {"type": "string"},
            "audit_path": {
                "type": "string",
                "description": f"Repo-local JSONL path. Defaults to {OPENCLAW_AUDIT_REVIEW_DEFAULT_PATH}.",
            },
            "limit": {"type": "integer", "minimum": 1, "maximum": 200},
            "format": {"type": "string", "enum": ["json", "markdown"]},
        },
    },
}


def openclaw_audit_review_tool(args: dict[str, Any], **kwargs) -> str:
    if not isinstance(args, dict):
        return tool_error("args must be an object.", success=False)

    validated = _validate_args(args)
    if validated is not None:
        return validated

    payload = build_openclaw_audit_review(
        repo_root=args.get("repo_root", "."),
        audit_path=args.get("audit_path"),
        limit=args.get("limit", 20),
    )
    payload["success"] = True
    payload["read_only"] = True
    payload["read_only_memory"] = True
    payload["would_mutate_memory"] = False
    payload["invokes_openclaw"] = False
    payload["writes_files"] = False
    if str(args.get("format", "")).lower() == "markdown":
        payload["markdown"] = _render_markdown(payload)
    return json.dumps(payload, ensure_ascii=False)


def _validate_args(args: dict[str, Any]) -> str | None:
    for field_name in ("repo_root", "audit_path", "format"):
        value = args.get(field_name)
        if value is not None and not isinstance(value, str):
            return tool_error(f"{field_name} must be a string when provided.", success=False)

    limit = args.get("limit")
    if limit is not None and (not isinstance(limit, int) or limit < 1 or limit > 200):
        return tool_error("limit must be an integer between 1 and 200.", success=False)

    fmt = args.get("format")
    if fmt is not None and fmt not in {"json", "markdown"}:
        return tool_error("format must be either json or markdown.", success=False)

    return None


def _render_markdown(payload: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    lines = [
        "### OpenClaw Audit Review",
        f"- Status: {payload.get('status')}",
        f"- Source: {payload.get('source_path')}",
        f"- Total entries: {summary.get('total_entry_count', 0)}",
        f"- Returned entries: {summary.get('returned_entry_count', 0)}",
        f"- Invalid JSONL lines: {summary.get('invalid_jsonl_line_count', 0)}",
        f"- Sensitive fields removed: {summary.get('sensitive_fields_removed_count', 0)}",
    ]
    for entry in payload.get("entries", []):
        lines.append(f"- Audit: {entry.get('audit_id') or entry.get('approved_job_id') or 'unknown'}")
        lines.append(f"  Status: {entry.get('status')}")
        lines.append(f"  Agent: {entry.get('agent')}")
    return "\n".join(lines)


def check_openclaw_audit_review_requirements() -> bool:
    return True


registry.register(
    name="openclaw_audit_review",
    toolset="memory",
    schema=OPENCLAW_AUDIT_REVIEW_SCHEMA,
    handler=openclaw_audit_review_tool,
    check_fn=check_openclaw_audit_review_requirements,
    emoji="🧠",
)
