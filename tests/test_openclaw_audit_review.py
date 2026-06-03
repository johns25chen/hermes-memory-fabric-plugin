import json

from hermes_memory_fabric.openclaw_audit_review import build_openclaw_audit_review


def _write_jsonl(repo_root, records):
    path = repo_root / "jobs" / "audit" / "approved_employee_tasks.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def test_reads_jsonl_and_projects_only_allowlisted_fields(tmp_path):
    _write_jsonl(
        tmp_path,
        [
            {
                "review_result": {
                    "decision": "approved",
                    "stdout": "nested secret stdout",
                    "approval_phrase": "nested approval phrase",
                },
                "audit_id": "audit-1",
                "created_at": "2026-06-03T00:00:00+00:00",
                "source_dryrun_job_id": "dryrun-1",
                "approved_job_id": "approved-1",
                "agent": "openclaw",
                "risk_level": "low",
                "status": "approved",
                "exit_code": 0,
                "assistant_text": "safe summary",
                "task_preview": "safe task preview",
                "log_path": "jobs/logs/audit-1.log",
                "approval_phrase": "top-level secret phrase",
                "stdout_tail": "top-level secret stdout tail",
                "stdout": "top-level full stdout",
                "unexpected": "must not be returned",
            }
        ],
    )

    result = build_openclaw_audit_review(repo_root=tmp_path)

    assert result["status"] == "openclaw_audit_review_ready"
    assert result["read_only"] is True
    assert result["would_mutate_memory"] is False
    assert result["invokes_openclaw"] is False
    assert result["writes_files"] is False
    assert result["summary"]["total_entry_count"] == 1
    assert result["summary"]["returned_entry_count"] == 1
    assert result["summary"]["sensitive_fields_removed_count"] >= 3

    entry = result["entries"][0]
    assert entry["audit_id"] == "audit-1"
    assert entry["review_result"]["decision"] == "approved"
    assert "unexpected" not in entry

    serialized = json.dumps(result, ensure_ascii=False)
    assert "top-level secret phrase" not in serialized
    assert "top-level secret stdout tail" not in serialized
    assert "top-level full stdout" not in serialized
    assert "nested secret stdout" not in serialized
    assert "nested approval phrase" not in serialized
    assert "approval_phrase" not in serialized
    assert "stdout_tail" not in serialized
    assert "stdout" not in serialized


def test_missing_audit_jsonl_returns_safe_report(tmp_path):
    result = build_openclaw_audit_review(repo_root=tmp_path)

    assert result["status"] == "missing_audit_log"
    assert result["entries"] == []
    assert "approved_audit_jsonl_not_found" in result["blocking_reasons"]
    assert result["read_only"] is True
    assert result["would_mutate_memory"] is False


def test_invalid_jsonl_lines_are_reported_without_raw_content(tmp_path):
    path = tmp_path / "jobs" / "audit" / "approved_employee_tasks.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '{"audit_id": "audit-1", "status": "approved"}\n'
        '{"approval_phrase": "do not leak", bad json\n',
        encoding="utf-8",
    )

    result = build_openclaw_audit_review(repo_root=tmp_path)

    assert result["status"] == "openclaw_audit_review_ready_with_warnings"
    assert result["summary"]["invalid_jsonl_line_count"] == 1
    assert result["invalid_jsonl_lines"][0]["line_number"] == 2
    assert "do not leak" not in json.dumps(result, ensure_ascii=False)


def test_limit_returns_latest_entries(tmp_path):
    _write_jsonl(
        tmp_path,
        [
            {"audit_id": "audit-1", "status": "approved"},
            {"audit_id": "audit-2", "status": "approved"},
            {"audit_id": "audit-3", "status": "approved"},
        ],
    )

    result = build_openclaw_audit_review(repo_root=tmp_path, limit=2)

    assert [entry["audit_id"] for entry in result["entries"]] == ["audit-2", "audit-3"]


def test_blocks_path_outside_repo_root(tmp_path):
    outside = tmp_path.parent / "outside-approved.jsonl"
    outside.write_text('{"audit_id": "audit-outside"}\n', encoding="utf-8")

    result = build_openclaw_audit_review(repo_root=tmp_path, audit_path=outside)

    assert result["status"] == "blocked"
    assert "audit_path_must_be_inside_repo_root" in result["blocking_reasons"]
    assert result["entries"] == []


def test_blocks_directory_audit_path_without_crashing(tmp_path):
    audit_dir = tmp_path / "jobs" / "audit"
    audit_dir.mkdir(parents=True)

    result = build_openclaw_audit_review(repo_root=tmp_path, audit_path=audit_dir)

    assert result["status"] == "blocked"
    assert "approved_audit_path_is_directory" in result["blocking_reasons"]
    assert result["entries"] == []
    assert result["read_only"] is True
    assert result["would_mutate_memory"] is False
