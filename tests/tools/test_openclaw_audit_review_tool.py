import json

from hermes_memory_fabric.tools.local_registry import registry
from hermes_memory_fabric.tools.openclaw_audit_review_tool import openclaw_audit_review_tool


def _write_jsonl(repo_root, records):
    path = repo_root / "jobs" / "audit" / "approved_employee_tasks.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def test_tool_reads_jsonl_and_returns_markdown(tmp_path):
    _write_jsonl(
        tmp_path,
        [
            {
                "audit_id": "audit-1",
                "approved_job_id": "approved-1",
                "agent": "openclaw",
                "status": "approved",
                "approval_phrase": "must not leak",
                "stdout_tail": "must not leak tail",
            }
        ],
    )

    result = json.loads(
        openclaw_audit_review_tool({"repo_root": str(tmp_path), "format": "markdown"})
    )

    assert result["success"] is True
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["would_mutate_memory"] is False
    assert result["invokes_openclaw"] is False
    assert result["writes_files"] is False
    assert result["status"] == "openclaw_audit_review_ready"
    assert result["entries"][0]["audit_id"] == "audit-1"
    assert "OpenClaw Audit Review" in result["markdown"]

    serialized = json.dumps(result, ensure_ascii=False)
    assert "must not leak" not in serialized
    assert "must not leak tail" not in serialized
    assert "approval_phrase" not in serialized
    assert "stdout_tail" not in serialized
    assert "stdout" not in serialized


def test_tool_rejects_invalid_input_shape():
    result = json.loads(openclaw_audit_review_tool("bad"))

    assert result["success"] is False
    assert "args must be an object" in result["error"]


def test_tool_rejects_invalid_limit(tmp_path):
    result = json.loads(openclaw_audit_review_tool({"repo_root": str(tmp_path), "limit": 0}))

    assert result["success"] is False
    assert "limit must be an integer between 1 and 200" in result["error"]


def test_tool_missing_file_is_safe(tmp_path):
    result = json.loads(openclaw_audit_review_tool({"repo_root": str(tmp_path)}))

    assert result["success"] is True
    assert result["status"] == "missing_audit_log"
    assert result["entries"] == []
    assert result["would_mutate_memory"] is False


def test_tool_is_registered_under_memory_toolset():
    entry = registry.get_entry("openclaw_audit_review")

    assert entry is not None
    assert entry.toolset == "memory"
    assert entry.handler is openclaw_audit_review_tool
