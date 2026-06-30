from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_final_boundary_audit_closure import (
    FINAL_BOUNDARY_AUDIT_BOUNDARY,
    FinalBoundaryAuditItem,
    final_boundary_audit_as_dicts,
    final_boundary_audit_item_ids,
    final_boundary_audit_report,
    list_final_boundary_audit_items,
    render_final_boundary_audit_markdown,
)


AUDIT_ITEM_IDS = (
    "checklist-boundary-audit",
    "proposal-review-boundary-audit",
    "recall-verification-boundary-audit",
    "lifecycle-verification-boundary-audit",
    "do-not-retry-boundary-audit",
    "source-provenance-boundary-audit",
    "decision-readiness-boundary-audit",
    "manual-decision-preview-boundary-audit",
    "governance-pack-export-boundary-audit",
    "p4-m1-read-only-corridor-closure",
    "p4-m2-not-started",
    "v7-productization-not-started",
    "automation-boundary-intact",
)

DATACLASS_FIELDS = {
    "audit_order",
    "audit_id",
    "audit_name",
    "source_status_surface",
    "closure_question",
    "closure_signal",
    "allowed_closure_output",
    "prohibited_automation",
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
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
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
    "start-p4-m2",
    "p4-m2",
    "start-v7",
    "productize",
}


def test_final_boundary_audit_item_order_is_deterministic():
    assert [
        item.audit_order for item in list_final_boundary_audit_items()
    ] == list(range(1, 14))
    assert final_boundary_audit_item_ids() == AUDIT_ITEM_IDS
    assert final_boundary_audit_item_ids() == final_boundary_audit_item_ids()


def test_final_boundary_audit_has_exactly_13_items():
    assert len(list_final_boundary_audit_items()) == 13


def test_audit_item_ids_match_required_audit_item_ids():
    assert final_boundary_audit_item_ids() == AUDIT_ITEM_IDS


def test_every_item_has_required_non_empty_fields():
    for item in list_final_boundary_audit_items():
        assert item.audit_name.strip()
        assert item.source_status_surface.strip()
        assert item.closure_question.strip()
        assert item.closure_signal.strip()
        assert item.allowed_closure_output.strip()
        assert item.prohibited_automation.strip()
        assert item.blocking_signal.strip()
        assert item.p4_m0_or_p4_m1_dependency.strip()


def test_markdown_render_contains_all_13_audit_item_ids():
    markdown = render_final_boundary_audit_markdown()

    for audit_id in AUDIT_ITEM_IDS:
        assert audit_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_final_boundary_audit_markdown()

    assert "read-only final boundary audit / closure only" in markdown
    assert "advisory only" in markdown
    assert "for human audit and P4-M1 closure review only" in markdown
    assert "P4-M1 closure is not P4-M2 execution" in markdown
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
    assert "does not start P4-M2" in markdown
    assert "does not start v7" in markdown
    assert "does not productize" in markdown
    assert "does not grant authorization semantics" in markdown
    assert "does not grant execution semantics" in markdown
    assert "No decision recommendation is performed by this closure report." in markdown
    assert "No decision ranking is performed by this closure report." in markdown
    assert "No automatic readiness verdict is performed by this closure report." in markdown
    assert "No decision execution is performed by this closure report." in markdown
    assert "No approval or rejection is performed by this closure report." in markdown
    assert "No memory writing is performed by this closure report." in markdown
    assert "No proposal mutation is performed by this closure report." in markdown
    assert "No lifecycle mutation is performed by this closure report." in markdown
    assert "No do-not-retry mutation is performed by this closure report." in markdown
    assert "No source/provenance mutation is performed by this closure report." in markdown
    assert "No API/MCP/connector behavior is performed by this closure report." in markdown
    assert "P4-M2 is not started by this closure report." in markdown
    assert "v7 is not started by this closure report." in markdown
    assert "Productization is not started by this closure report." in markdown


def test_dict_conversion_is_deterministic():
    first = final_boundary_audit_as_dicts()
    second = final_boundary_audit_as_dicts()

    assert first == second
    assert [item["audit_id"] for item in first] == list(AUDIT_ITEM_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = final_boundary_audit_report()
    second = final_boundary_audit_report()

    assert first == second
    assert first["phase"] == "P4-M1.9"
    assert first["feature"] == "Final Boundary Audit / Closure"
    assert first["mode"] == "read-only"
    assert first["audit_item_count"] == 13
    assert first["boundary"] == FINAL_BOUNDARY_AUDIT_BOUNDARY


def test_status_report_has_required_true_flags():
    status = final_boundary_audit_report()

    assert status["final_boundary_audit_read_only"] is True
    assert status["closure_report_advisory_only"] is True
    assert status["human_audit_and_closure_review_only"] is True
    assert status["p4_m1_closure_only"] is True


def test_status_report_has_p4_m2_started_false():
    assert final_boundary_audit_report()["p4_m2_started"] is False


def test_status_report_has_all_disabled_flags_set_to_false():
    status = final_boundary_audit_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert final_boundary_audit_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_final_boundary_audit_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "final-boundary-audit", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.9 Final Boundary Audit / Closure\n")
    assert "## Status Report" in stdout
    assert FINAL_BOUNDARY_AUDIT_BOUNDARY in stdout
    for audit_id in AUDIT_ITEM_IDS:
        assert audit_id in stdout
    assert "No decision recommendation is performed by this closure report." in stdout
    assert "No decision ranking is performed by this closure report." in stdout
    assert "No automatic readiness verdict is performed by this closure report." in stdout
    assert "No decision execution is performed by this closure report." in stdout
    assert "No approval or rejection is performed by this closure report." in stdout
    assert "No memory writing is performed by this closure report." in stdout
    assert "No proposal mutation is performed by this closure report." in stdout
    assert "No lifecycle mutation is performed by this closure report." in stdout
    assert "No do-not-retry mutation is performed by this closure report." in stdout
    assert "No source/provenance mutation is performed by this closure report." in stdout
    assert "No API/MCP/connector behavior is performed by this closure report." in stdout
    assert "P4-M2 is not started by this closure report." in stdout
    assert "v7 is not started by this closure report." in stdout
    assert "Productization is not started by this closure report." in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_memory_loop_final_boundary_audit_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "final-boundary-audit",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.9 Final Boundary Audit / Closure\n")


def test_operator_memory_loop_final_boundary_audit_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "final-boundary-audit",
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
    assert payload["boundary"] == FINAL_BOUNDARY_AUDIT_BOUNDARY
    assert payload["count"] == 13
    assert payload["status"] == final_boundary_audit_report()
    assert [item["audit_id"] for item in payload["items"]] == list(AUDIT_ITEM_IDS)
    assert set(payload["items"][0]) == DATACLASS_FIELDS


def test_operator_final_boundary_audit_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["memory-loop", "final-boundary-audit", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "final-boundary-audit",
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


def test_operator_final_boundary_audit_command_creates_no_proposals(tmp_path):
    _run_operator(
        ["memory-loop", "final-boundary-audit", "--workspace-root", str(tmp_path)]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_final_boundary_audit_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "final-boundary-audit",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_final_boundary_audit_command_creates_no_boundary_or_state_changes(
    tmp_path,
):
    _run_operator(
        ["memory-loop", "final-boundary-audit", "--workspace-root", str(tmp_path)]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "decisions.jsonl").exists()
    assert not (storage_root / "readiness.jsonl").exists()
    assert not (storage_root / "previews.jsonl").exists()
    assert not (storage_root / "governance_pack.jsonl").exists()
    assert not (storage_root / "final_boundary_audit.jsonl").exists()
    assert not (storage_root / "closure.jsonl").exists()
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


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_decision_recommendation_readiness_mutation_p4_m2_v7_productization_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_memory_loop_checklist_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "checklist",
        "# P4-M1.0 Human-Gated Memory Loop Checklist\n",
    )


def test_existing_p4_m1_1_memory_loop_review_status_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "review-status",
        "# P4-M1.1 Human-Gated Proposal Review Status\n",
    )


def test_existing_p4_m1_2_memory_loop_recall_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "recall-verification-status",
        "# P4-M1.2 Human-Gated Recall Verification Status\n",
    )


def test_existing_p4_m1_3_memory_loop_lifecycle_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "lifecycle-verification-status",
        "# P4-M1.3 Human-Gated Lifecycle Verification Status\n",
    )


def test_existing_p4_m1_4_memory_loop_do_not_retry_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "do-not-retry-verification-status",
        "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n",
    )


def test_existing_p4_m1_5_memory_loop_source_provenance_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "source-provenance-verification-status",
        "# P4-M1.5 Source / Provenance Verification Status\n",
    )


def test_existing_p4_m1_6_memory_loop_decision_readiness_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "decision-readiness-status",
        "# P4-M1.6 Decision Readiness Status\n",
    )


def test_existing_p4_m1_7_memory_loop_manual_decision_preview_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "manual-decision-preview",
        "# P4-M1.7 Manual Decision Preview\n",
    )


def test_existing_p4_m1_8_memory_loop_governance_pack_export_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "governance-pack-export",
        "# P4-M1.8 Governance Pack Export\n",
    )


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_final_boundary_audit():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_final_boundary_audit_closure" not in entry_points
    assert "final-boundary-audit" not in entry_points


def test_custom_markdown_render_accepts_read_only_audit_items():
    item = FinalBoundaryAuditItem(
        audit_order=1,
        audit_id="custom-final-boundary-audit",
        audit_name="Custom final boundary audit",
        source_status_surface="Custom read-only status surface.",
        closure_question="Is the custom surface read-only?",
        closure_signal="Custom surface is visible.",
        allowed_closure_output="Manual closure text only.",
        prohibited_automation="No decision recommendation, ranking, readiness verdict, or execution.",
        blocking_signal="Custom surface is hidden.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only boundary.",
    )

    markdown = render_final_boundary_audit_markdown([item])

    assert "custom-final-boundary-audit" in markdown
    assert "Is the custom surface read-only?" in markdown


def _assert_existing_command_still_works(
    tmp_path: Path,
    command: str,
    expected_prefix: str,
) -> None:
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", command, "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(expected_prefix)
    assert not (tmp_path / ".local").exists()


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
