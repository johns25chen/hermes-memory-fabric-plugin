from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_governance_pack_export import (
    GOVERNANCE_PACK_EXPORT_BOUNDARY,
    GovernancePackSection,
    governance_pack_as_dicts,
    governance_pack_export_report,
    governance_pack_section_ids,
    list_governance_pack_sections,
    render_governance_pack_markdown,
)


SECTION_IDS = (
    "checklist-pack-section",
    "proposal-review-pack-section",
    "recall-verification-pack-section",
    "lifecycle-verification-pack-section",
    "do-not-retry-pack-section",
    "source-provenance-pack-section",
    "decision-readiness-pack-section",
    "manual-decision-preview-pack-section",
    "unified-governance-pack",
    "export-not-decision",
    "automation-boundary-intact",
)

DATACLASS_FIELDS = {
    "section_order",
    "section_id",
    "section_name",
    "source_status_surface",
    "export_purpose",
    "allowed_export_output",
    "prohibited_automation",
    "human_audit_signal",
    "blocking_signal",
    "p4_m0_or_p4_m1_dependency",
}

DISABLED_STATUS_FLAGS = (
    "automatic_decision_recommendation_enabled",
    "decision_ranking_enabled",
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
    "API",
    "MCP",
    "connector",
}


def test_governance_pack_section_order_is_deterministic():
    assert [
        section.section_order for section in list_governance_pack_sections()
    ] == list(range(1, 12))
    assert governance_pack_section_ids() == SECTION_IDS
    assert governance_pack_section_ids() == governance_pack_section_ids()


def test_governance_pack_has_exactly_11_sections():
    assert len(list_governance_pack_sections()) == 11


def test_section_ids_match_required_section_ids():
    assert governance_pack_section_ids() == SECTION_IDS


def test_every_section_has_required_non_empty_fields():
    for section in list_governance_pack_sections():
        assert section.section_name.strip()
        assert section.source_status_surface.strip()
        assert section.export_purpose.strip()
        assert section.allowed_export_output.strip()
        assert section.prohibited_automation.strip()
        assert section.human_audit_signal.strip()
        assert section.blocking_signal.strip()
        assert section.p4_m0_or_p4_m1_dependency.strip()


def test_markdown_render_contains_all_11_section_ids():
    markdown = render_governance_pack_markdown()

    for section_id in SECTION_IDS:
        assert section_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_governance_pack_markdown()

    assert "read-only governance pack export only" in markdown
    assert "advisory only" in markdown
    assert "for human audit, archive, handoff, and review only" in markdown
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
    assert "No decision recommendation is performed by this export." in markdown
    assert "No decision ranking is performed by this export." in markdown
    assert "No automatic readiness verdict is performed by this export." in markdown
    assert "No decision execution is performed by this export." in markdown
    assert "No approval or rejection is performed by this export." in markdown
    assert "No memory writing is performed by this export." in markdown
    assert "No proposal mutation is performed by this export." in markdown
    assert "No lifecycle mutation is performed by this export." in markdown
    assert "No do-not-retry mutation is performed by this export." in markdown
    assert "No source/provenance mutation is performed by this export." in markdown
    assert "No API/MCP/connector behavior is performed by this export." in markdown


def test_dict_conversion_is_deterministic():
    first = governance_pack_as_dicts()
    second = governance_pack_as_dicts()

    assert first == second
    assert [section["section_id"] for section in first] == list(SECTION_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = governance_pack_export_report()
    second = governance_pack_export_report()

    assert first == second
    assert first["phase"] == "P4-M1.8"
    assert first["feature"] == "Governance Pack Export"
    assert first["mode"] == "read-only"
    assert first["pack_section_count"] == 11
    assert first["boundary"] == GOVERNANCE_PACK_EXPORT_BOUNDARY


def test_status_report_has_required_true_flags():
    status = governance_pack_export_report()

    assert status["governance_pack_export_read_only"] is True
    assert status["governance_pack_export_advisory_only"] is True
    assert status["human_audit_archive_handoff_review_only"] is True


def test_status_report_has_all_disabled_flags_set_to_false():
    status = governance_pack_export_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert governance_pack_export_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_governance_pack_export_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "governance-pack-export", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.8 Governance Pack Export\n")
    assert "## Status Report" in stdout
    assert GOVERNANCE_PACK_EXPORT_BOUNDARY in stdout
    for section_id in SECTION_IDS:
        assert section_id in stdout
    assert "No decision recommendation is performed by this export." in stdout
    assert "No decision ranking is performed by this export." in stdout
    assert "No automatic readiness verdict is performed by this export." in stdout
    assert "No decision execution is performed by this export." in stdout
    assert "No approval or rejection is performed by this export." in stdout
    assert "No memory writing is performed by this export." in stdout
    assert "No proposal mutation is performed by this export." in stdout
    assert "No lifecycle mutation is performed by this export." in stdout
    assert "No do-not-retry mutation is performed by this export." in stdout
    assert "No source/provenance mutation is performed by this export." in stdout
    assert "No API/MCP/connector behavior is performed by this export." in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_memory_loop_governance_pack_export_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "governance-pack-export",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.8 Governance Pack Export\n")


def test_operator_memory_loop_governance_pack_export_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "governance-pack-export",
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
    assert payload["boundary"] == GOVERNANCE_PACK_EXPORT_BOUNDARY
    assert payload["count"] == 11
    assert payload["status"] == governance_pack_export_report()
    assert [section["section_id"] for section in payload["sections"]] == list(SECTION_IDS)
    assert set(payload["sections"][0]) == DATACLASS_FIELDS


def test_operator_governance_pack_export_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["memory-loop", "governance-pack-export", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "governance-pack-export",
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


def test_operator_governance_pack_export_command_creates_no_proposals(tmp_path):
    _run_operator(
        ["memory-loop", "governance-pack-export", "--workspace-root", str(tmp_path)]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_governance_pack_export_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "governance-pack-export",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_governance_pack_export_command_creates_no_decision_readiness_preview_governance_pack_memory_proposal_lifecycle_do_not_retry_source_provenance_files_or_state_changes(
    tmp_path,
):
    _run_operator(
        ["memory-loop", "governance-pack-export", "--workspace-root", str(tmp_path)]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "decisions.jsonl").exists()
    assert not (storage_root / "readiness.jsonl").exists()
    assert not (storage_root / "previews.jsonl").exists()
    assert not (storage_root / "governance_pack.jsonl").exists()
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


def test_existing_p4_m1_7_memory_loop_manual_decision_preview_still_works(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "manual-decision-preview", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.7 Manual Decision Preview\n")
    assert not (tmp_path / ".local").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_governance_pack_export():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_governance_pack_export" not in entry_points
    assert "governance-pack-export" not in entry_points


def test_custom_markdown_render_accepts_read_only_sections():
    section = GovernancePackSection(
        section_order=1,
        section_id="custom-pack-section",
        section_name="Custom pack section",
        source_status_surface="Custom read-only status surface.",
        export_purpose="Package a custom read-only section.",
        allowed_export_output="Manual export text only.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, or execution.",
        human_audit_signal="Visible custom section.",
        blocking_signal="Hidden custom section.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only boundary.",
    )

    markdown = render_governance_pack_markdown([section])

    assert "custom-pack-section" in markdown
    assert "Package a custom read-only section." in markdown


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
