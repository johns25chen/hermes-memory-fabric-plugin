from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_manual_decision_preview import (
    MANUAL_DECISION_PREVIEW_BOUNDARY,
    ManualDecisionPreviewFrame,
    list_manual_decision_preview_frames,
    manual_decision_preview_as_dicts,
    manual_decision_preview_ids,
    manual_decision_preview_report,
    render_manual_decision_preview_markdown,
)


PREVIEW_IDS = (
    "checklist-preview",
    "proposal-review-preview",
    "recall-verification-preview",
    "lifecycle-verification-preview",
    "do-not-retry-preview",
    "source-provenance-preview",
    "decision-readiness-preview",
    "unified-human-review-frame",
    "decision-not-recommended",
    "automation-boundary-intact",
)

DATACLASS_FIELDS = {
    "preview_order",
    "preview_id",
    "preview_name",
    "human_preview_question",
    "source_status_surface",
    "allowed_preview_output",
    "prohibited_automation",
    "human_review_signal",
    "blocking_signal",
    "p4_m0_or_p4_m1_dependency",
}

DISABLED_STATUS_FLAGS = (
    "automatic_decision_recommendation_enabled",
    "automatic_readiness_verdict_enabled",
    "decision_execution_enabled",
    "approval_enabled",
    "rejection_enabled",
    "memory_write_enabled",
    "memory_record_mutation_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "do_not_retry_guard_mutation_enabled",
    "retry_policy_mutation_enabled",
    "source_fetching_enabled",
    "source_provenance_mutation_enabled",
    "provenance_write_enabled",
    "memory_injection_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
    "v7_started",
    "productization_started",
)

EXPECTED_MEMORY_LOOP_COMMANDS = {
    "checklist",
    "review-status",
    "recall-verification-status",
    "lifecycle-verification-status",
    "do-not-retry-verification-status",
    "source-provenance-verification-status",
    "decision-readiness-status",
    "manual-decision-preview",
    "governance-pack-export",
    "final-boundary-audit",
    "manual-execution-hardening",
    "execution-surface-contract",
    "execution-contract-validation-matrix",
    "manual-authorization-evidence-envelope",
    "human-confirmation-snapshot-contract",
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
    "execution-decision-silence-non-consent-map",
    "execution-decision-negative-evidence-non-override-map",
    "execution-decision-conflicting-evidence-isolation-map",
    "execution-decision-evidence-precedence-prohibition-map",
    "final-non-execution-boundary-audit",
    "p4-m2-closure-handoff-contract",
    "governed-transition-intake-boundary-contract",
    "governed-transition-intake-request-envelope-contract",
    "governed-transition-intake-evidence-reference-envelope-contract",
    "governed-transition-intake-declared-human-context-envelope-contract",
    "governed-transition-intake-target-phase-envelope-contract",
    "governed-transition-intake-declared-transition-reason-envelope-contract",
    "governed-transition-intake-declared-transition-constraint-envelope-contract",
        "governed-transition-intake-declared-transition-dependency-envelope-contract",
    "governed-transition-intake-declared-transition-impact-envelope-contract",
    "governed-transition-intake-declared-transition-risk-envelope-contract",
    "governed-transition-intake-declared-transition-assumption-envelope-contract",
    "governed-transition-intake-declared-transition-safeguard-envelope-contract",
    "governed-transition-intake-package-assembly-envelope-contract",
    "governed-transition-intake-final-non-validation-boundary-audit",
    "governed-transition-intake-closure-handoff-contract",
    "governed-transition-intake-phase-closure-review",
    "governed-transition-intake-final-phase-handoff-summary",
    "entry-gate-design-boundary-contract",
    "entry-gate-design-request-envelope-contract",
    "evidence-reference-envelope-contract",
}

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "authorize",
    "authorization",
    "authorize-decision",
    "decision-authorization",
    "grant-authorization",
    "revoke-authorization",
    "validate-authorization-envelope",
    "live-authorization-validation",
    "decide",
    "decision",
    "execute-decision",
    "decision-execute",
    "recommend-decision",
    "decision-recommendation",
    "rank-decision",
    "readiness-verdict",
    "automatic-readiness",
    "validation-verdict",
    "validate-contract",
    "validate-execution-contract",
    "live-validation",
    "input-validation",
    "record-validation",
    "mark-ready",
    "mark-not-ready",
    "approve",
    "reject",
    "approve-all",
    "reject-all",
    "approve-proposal",
    "reject-proposal",
    "approve-memory",
    "reject-memory",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "update-proposal",
    "lifecycle-set",
    "lifecycle-update",
    "lifecycle-mutate",
    "do-not-retry",
    "mark-do-not-retry",
    "guard-set",
    "guard-update",
    "retry-policy-set",
    "retry-policy-update",
    "fetch-source",
    "source-fetch",
    "lookup-source",
    "source-lookup",
    "browse-source",
    "web-fetch",
    "web-search",
    "verify-source",
    "trust-source",
    "score-source",
    "write-provenance",
    "provenance-write",
    "mutate-source",
    "mutate-provenance",
    "mutate-evidence",
    "mutate-citation",
    "archive",
    "stale",
    "cleanup",
    "delete",
    "import",
    "bulk-import",
    "ingest",
    "auto-ingest",
    "auto-approve",
    "auto-reject",
    "inject",
    "inject-memory",
    "call-agent",
    "execute",
    "deploy",
    "api",
    "mcp",
    "connector",
    "API",
    "MCP",
}


def test_manual_decision_preview_frame_order_is_deterministic():
    assert [
        frame.preview_order for frame in list_manual_decision_preview_frames()
    ] == list(range(1, 11))
    assert manual_decision_preview_ids() == PREVIEW_IDS
    assert manual_decision_preview_ids() == manual_decision_preview_ids()


def test_manual_decision_preview_has_exactly_10_frames():
    assert len(list_manual_decision_preview_frames()) == 10


def test_preview_ids_match_required_preview_ids():
    assert manual_decision_preview_ids() == PREVIEW_IDS


def test_every_frame_has_required_non_empty_fields():
    for frame in list_manual_decision_preview_frames():
        assert frame.preview_name.strip()
        assert frame.human_preview_question.strip()
        assert frame.source_status_surface.strip()
        assert frame.allowed_preview_output.strip()
        assert frame.prohibited_automation.strip()
        assert frame.human_review_signal.strip()
        assert frame.blocking_signal.strip()
        assert frame.p4_m0_or_p4_m1_dependency.strip()


def test_markdown_render_contains_all_10_preview_ids():
    markdown = render_manual_decision_preview_markdown()

    for preview_id in PREVIEW_IDS:
        assert preview_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_manual_decision_preview_markdown()

    assert "read-only manual decision preview only" in markdown
    assert "advisory only" in markdown
    assert "for human inspection only" in markdown
    assert "does not recommend a decision" in markdown
    assert "does not rank decisions" in markdown
    assert "does not automatically determine readiness" in markdown
    assert "does not emit an automatic readiness verdict" in markdown
    assert "does not make decisions" in markdown
    assert "does not execute decisions" in markdown
    assert "does not approve memory" in markdown
    assert "does not reject memory" in markdown
    assert "does not approve proposals" in markdown
    assert "does not reject proposals" in markdown
    assert "does not write memory" in markdown
    assert "does not create memory records" in markdown
    assert "does not update memory records" in markdown
    assert "does not delete memory records" in markdown
    assert "does not mutate proposal records" in markdown
    assert "does not mutate lifecycle records" in markdown
    assert "does not mutate do-not-retry guard state" in markdown
    assert "does not mutate retry policy" in markdown
    assert "does not fetch sources" in markdown
    assert "does not browse the web" in markdown
    assert "does not call external APIs" in markdown
    assert "does not call connectors" in markdown
    assert "does not create API/MCP/connector behavior" in markdown
    assert "does not automatically trust a source" in markdown
    assert "does not write provenance" in markdown
    assert "does not mutate source/provenance/evidence/citation records" in markdown
    assert "does not inject memory into agents" in markdown
    assert "does not bulk import memory" in markdown
    assert "does not auto-ingest chat history" in markdown
    assert "does not auto-ingest files" in markdown
    assert "does not auto-ingest external systems" in markdown
    assert "does not call agents" in markdown
    assert "does not start v7" in markdown
    assert "does not productize" in markdown
    assert "does not grant authorization semantics" in markdown
    assert "does not grant execution semantics" in markdown
    assert "No decision recommendation is performed by this preview." in markdown
    assert "No decision ranking is performed by this preview." in markdown
    assert "No automatic readiness verdict is performed by this preview." in markdown
    assert "No decision execution is performed by this preview." in markdown
    assert "No approval or rejection is performed by this preview." in markdown
    assert "No memory writing is performed by this preview." in markdown
    assert "No proposal mutation is performed by this preview." in markdown
    assert "No lifecycle mutation is performed by this preview." in markdown
    assert "No do-not-retry mutation is performed by this preview." in markdown
    assert "No source/provenance mutation is performed by this preview." in markdown
    assert "No API/MCP/connector behavior is performed by this preview." in markdown


def test_dict_conversion_is_deterministic():
    first = manual_decision_preview_as_dicts()
    second = manual_decision_preview_as_dicts()

    assert first == second
    assert [frame["preview_id"] for frame in first] == list(PREVIEW_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = manual_decision_preview_report()
    second = manual_decision_preview_report()

    assert first == second
    assert first["phase"] == "P4-M1.7"
    assert first["feature"] == "Manual Decision Preview"
    assert first["mode"] == "read-only"
    assert first["preview_frame_count"] == 10
    assert first["boundary"] == MANUAL_DECISION_PREVIEW_BOUNDARY


def test_status_report_has_advisory_and_human_inspection_flags_true():
    status = manual_decision_preview_report()

    assert status["manual_decision_preview_advisory_only"] is True
    assert status["human_inspection_only"] is True


def test_status_report_has_all_disabled_flags_set_to_false():
    status = manual_decision_preview_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert manual_decision_preview_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_manual_decision_preview_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.7 Manual Decision Preview\n")
    assert "## Status Report" in stdout
    assert MANUAL_DECISION_PREVIEW_BOUNDARY in stdout
    for preview_id in PREVIEW_IDS:
        assert preview_id in stdout
    assert "No decision recommendation is performed by this preview." in stdout
    assert "No automatic readiness verdict is performed by this preview." in stdout
    assert "No decision execution is performed by this preview." in stdout
    assert "No approval or rejection is performed by this preview." in stdout
    assert "No memory writing is performed by this preview." in stdout
    assert "No proposal mutation is performed by this preview." in stdout
    assert "No lifecycle mutation is performed by this preview." in stdout
    assert "No do-not-retry mutation is performed by this preview." in stdout
    assert "No source/provenance mutation is performed by this preview." in stdout
    assert "No API/MCP/connector behavior is performed by this preview." in stdout


def test_operator_memory_loop_manual_decision_preview_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.7 Manual Decision Preview\n")


def test_operator_memory_loop_manual_decision_preview_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "manual-decision-preview",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    exit_code, payload, stderr, stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert exit_code == 0
    assert stderr == ""
    assert second_code == 0
    assert second_stderr == ""
    assert stdout == second_stdout
    assert payload == second_payload
    assert payload["boundary"] == MANUAL_DECISION_PREVIEW_BOUNDARY
    assert payload["count"] == 10
    assert payload["status"] == manual_decision_preview_report()
    assert [frame["preview_id"] for frame in payload["frames"]] == list(PREVIEW_IDS)
    assert set(payload["frames"][0]) == DATACLASS_FIELDS


def test_operator_manual_decision_preview_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert json_code == 0
    assert json_stderr == ""
    assert not (tmp_path / ".local").exists()


def test_operator_manual_decision_preview_command_creates_no_proposals(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_manual_decision_preview_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_manual_decision_preview_command_creates_no_decision_readiness_preview_memory_proposal_lifecycle_do_not_retry_source_provenance_files_or_state_changes(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "manual-decision-preview",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "decisions.jsonl").exists()
    assert not (storage_root / "readiness.jsonl").exists()
    assert not (storage_root / "previews.jsonl").exists()
    assert not (storage_root / "memories.jsonl").exists()
    assert not (storage_root / "proposals.jsonl").exists()
    assert not (storage_root / "lifecycle.jsonl").exists()
    assert not (storage_root / "do_not_retry.jsonl").exists()
    assert not (storage_root / "sources.jsonl").exists()
    assert not (storage_root / "provenance.jsonl").exists()
    assert not (storage_root / "evidence.jsonl").exists()
    assert not (storage_root / "citations.jsonl").exists()
    assert not (storage_root / "audit.jsonl").exists()
    assert not (tmp_path / ".local").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_decision_recommendation_readiness_mutation_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_memory_loop_checklist_still_works(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "checklist", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.0 Human-Gated Memory Loop Checklist\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_1_memory_loop_review_status_still_works(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "review-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.1 Human-Gated Proposal Review Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_2_memory_loop_recall_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "recall-verification-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.2 Human-Gated Recall Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_3_memory_loop_lifecycle_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "lifecycle-verification-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.3 Human-Gated Lifecycle Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_4_memory_loop_do_not_retry_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "do-not-retry-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_5_memory_loop_source_provenance_verification_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "source-provenance-verification-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.5 Source / Provenance Verification Status\n")
    assert not (tmp_path / ".local").exists()


def test_existing_p4_m1_6_memory_loop_decision_readiness_status_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "decision-readiness-status",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.6 Decision Readiness Status\n")
    assert not (tmp_path / ".local").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_manual_decision_preview():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_manual_decision_preview" not in entry_points
    assert "manual-decision-preview" not in entry_points


def test_custom_markdown_render_accepts_read_only_frames():
    frame = ManualDecisionPreviewFrame(
        preview_order=1,
        preview_id="custom-preview",
        preview_name="Custom preview",
        human_preview_question="Can the human review the custom preview frame?",
        source_status_surface="Custom read-only status surface.",
        allowed_preview_output="Manual preview text only.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, or execution.",
        human_review_signal="Visible custom preview.",
        blocking_signal="Hidden custom preview.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only boundary.",
    )

    markdown = render_manual_decision_preview_markdown([frame])

    assert "custom-preview" in markdown
    assert "Can the human review the custom preview frame?" in markdown


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _memory_loop_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:
        raise AssertionError("memory-loop parser not found")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("memory-loop subcommands not found")
