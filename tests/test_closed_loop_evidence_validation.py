from __future__ import annotations

import json

from hermes_memory_fabric.closed_loop_evidence_validation import (
    build_closed_loop_evidence_validation,
)


def _valid_evidence() -> dict[str, object]:
    return {
        "natural_language_task": {
            "task_text": "Implement v2.9.0 evidence validation.",
            "task_boundary": "Validate evidence completeness without executing the workflow.",
            "human_operator_confirmed_boundary": True,
        },
        "codex_cli_implementation": {
            "codex_cli_used": True,
            "repository_inspected": True,
            "files_changed": ["src/hermes_memory_fabric/closed_loop_evidence_validation.py"],
            "change_summary": "Added read-only closed-loop evidence validator.",
            "codex_did_not_commit": True,
        },
        "terminal_or_openclaw_validation": {
            "validation_commands": [".venv/bin/python scripts/smoke_closed_loop_evidence_validation.py"],
            "validation_passed": True,
            "controlled_validation_only": True,
            "no_real_world_execution": True,
            "no_openclaw_autonomous_execution": True,
        },
        "chatgpt_review": {
            "diff_reviewed": True,
            "tests_reviewed": True,
            "governance_boundaries_reviewed": True,
            "no_sensitive_output_exposed": True,
        },
        "human_operator_decision": {
            "merge_decision_by_human": True,
            "human_final_authority": True,
        },
        "github_record": {
            "pr_recorded": True,
            "commit_recorded": True,
            "release_intended": False,
        },
    }


def test_valid_evidence_passes():
    result = build_closed_loop_evidence_validation(_valid_evidence())

    assert result["version"] == "2.9.0"
    assert result["status"] == "closed_loop_evidence_ready"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["would_mutate_memory"] is False
    assert result["invokes_openclaw"] is False
    assert result["writes_files"] is False
    assert result["would_call_github_api"] is False
    assert result["would_merge_pr"] is False
    assert result["would_create_tag"] is False
    assert result["authorization_granted"] is False
    assert result["openclaw_execution_authorized"] is False
    assert result["missing_evidence"] == []
    assert result["blocking_reasons"] == []


def test_missing_codex_cli_participation_blocks():
    evidence = _valid_evidence()
    evidence["codex_cli_implementation"] = {
        "codex_cli_used": False,
        "repository_inspected": True,
        "files_changed": ["src/hermes_memory_fabric/closed_loop_evidence_validation.py"],
        "change_summary": "Added validator.",
        "codex_did_not_commit": True,
    }

    result = build_closed_loop_evidence_validation(evidence)

    assert result["status"] == "blocked"
    assert "codex_cli_implementation.codex_cli_used" in result["missing_evidence"]
    assert "required_evidence_missing_or_incomplete" in result["blocking_reasons"]


def test_release_intended_without_tag_recorded_blocks():
    evidence = _valid_evidence()
    evidence["github_record"]["release_intended"] = True

    result = build_closed_loop_evidence_validation(evidence)

    assert result["status"] == "blocked"
    assert "github_record.tag_recorded" in result["missing_evidence"]
    assert "release_tag_record_required_when_release_intended" in result["blocking_reasons"]


def test_sensitive_fields_are_not_leaked_in_serialized_output():
    evidence = _valid_evidence()
    evidence["terminal_or_openclaw_validation"]["stdout"] = "raw stdout must not leak"
    evidence["terminal_or_openclaw_validation"]["stdout_tail"] = "tail must not leak"
    evidence["human_operator_decision"]["approval_phrase"] = "phrase must not leak"
    evidence["github_record"]["api_token"] = "token must not leak"
    evidence["chatgpt_review"]["raw_logs"] = {"secret": "secret must not leak"}

    result = build_closed_loop_evidence_validation(evidence)
    serialized = json.dumps(result, ensure_ascii=False)

    assert result["status"] == "blocked"
    assert result["sensitive_field_count"] >= 5
    assert "raw stdout must not leak" not in serialized
    assert "tail must not leak" not in serialized
    assert "phrase must not leak" not in serialized
    assert "token must not leak" not in serialized
    assert "secret must not leak" not in serialized
    assert "approval_phrase" not in serialized
    assert "stdout_tail" not in serialized
    assert "stdout" not in serialized
    assert "api_token" not in serialized
    assert "raw_logs" not in serialized
