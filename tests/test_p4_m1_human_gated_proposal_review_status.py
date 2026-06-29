from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_human_gated_proposal_review_status import (
    HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY,
    HumanGatedProposalReviewStatusItem,
    human_gated_proposal_review_status_as_dicts,
    human_gated_proposal_review_status_ids,
    human_gated_proposal_review_status_report,
    list_human_gated_proposal_review_status_items,
    render_human_gated_proposal_review_status_markdown,
)


REVIEW_IDS = (
    "proposal-visible",
    "scope-boundary-visible",
    "source-visible",
    "content-review-required",
    "decision-not-taken",
    "recall-plan-visible",
    "lifecycle-plan-visible",
    "do-not-retry-plan-visible",
    "automation-boundary-intact",
)

DATACLASS_FIELDS = {
    "review_order",
    "review_id",
    "review_name",
    "human_review_question",
    "allowed_system_output",
    "prohibited_automation",
    "ready_signal",
    "blocking_signal",
    "p4_m0_or_p4_m1_dependency",
}

DISABLED_STATUS_FLAGS = (
    "memory_write_enabled",
    "approval_enabled",
    "rejection_enabled",
    "proposal_mutation_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
    "v7_started",
    "productization_started",
)

PROHIBITED_MEMORY_LOOP_COMMANDS = {
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
    "import",
    "bulk-import",
    "ingest",
    "auto-ingest",
    "auto-approve",
    "auto-reject",
    "fetch-source",
    "source-fetch",
    "lookup-source",
    "source-lookup",
    "browse-source",
    "web-fetch",
    "web-search",
    "verify-source",
    "source-verdict",
    "trust-source",
    "score-source",
    "accept-evidence",
    "reject-evidence",
    "write-provenance",
    "provenance-write",
    "create-provenance",
    "update-provenance",
    "delete-provenance",
    "mutate-source",
    "update-source",
    "mutate-evidence",
    "update-evidence",
    "mutate-citation",
    "update-citation",
    "write-memory",
    "mutate-proposal",
    "update-proposal",
    "inject",
    "call-agent",
    "execute",
    "deploy",
    "api",
    "mcp",
    "connector",
}


def test_review_status_order_is_deterministic():
    assert [item.review_order for item in list_human_gated_proposal_review_status_items()] == list(
        range(1, 10)
    )
    assert human_gated_proposal_review_status_ids() == REVIEW_IDS
    assert human_gated_proposal_review_status_ids() == human_gated_proposal_review_status_ids()


def test_review_status_has_exactly_9_items():
    assert len(list_human_gated_proposal_review_status_items()) == 9


def test_review_ids_match_required_review_ids():
    assert human_gated_proposal_review_status_ids() == REVIEW_IDS


def test_every_item_has_required_non_empty_fields():
    for item in list_human_gated_proposal_review_status_items():
        assert item.review_name.strip()
        assert item.human_review_question.strip()
        assert item.allowed_system_output.strip()
        assert item.prohibited_automation.strip()
        assert item.ready_signal.strip()
        assert item.blocking_signal.strip()
        assert item.p4_m0_or_p4_m1_dependency.strip()


def test_markdown_render_contains_all_9_review_ids():
    markdown = render_human_gated_proposal_review_status_markdown()

    for review_id in REVIEW_IDS:
        assert review_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_human_gated_proposal_review_status_markdown()

    assert "read-only proposal review status only" in markdown
    assert "advisory only" in markdown
    assert "does not write memory" in markdown
    assert "does not approve memory" in markdown
    assert "does not reject memory" in markdown
    assert "does not mutate proposal records" in markdown
    assert "does not bulk import memory" in markdown
    assert "does not call agents" in markdown
    assert "No approval or rejection is performed by this status." in markdown


def test_dict_conversion_is_deterministic():
    first = human_gated_proposal_review_status_as_dicts()
    second = human_gated_proposal_review_status_as_dicts()

    assert first == second
    assert [item["review_id"] for item in first] == list(REVIEW_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = human_gated_proposal_review_status_report()
    second = human_gated_proposal_review_status_report()

    assert first == second
    assert first["phase"] == "P4-M1.1"
    assert first["feature"] == "Human-Gated Proposal Review Status"
    assert first["mode"] == "read-only"
    assert first["review_item_count"] == 9
    assert first["boundary"] == HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY


def test_status_report_has_advisory_flag_true():
    assert human_gated_proposal_review_status_report()["review_status_advisory_only"] is True


def test_status_report_has_all_disabled_flags_set_to_false():
    status = human_gated_proposal_review_status_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert human_gated_proposal_review_status_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_review_status_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "review-status", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.1 Human-Gated Proposal Review Status\n")
    assert "## Status Report" in stdout
    assert HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY in stdout
    assert "No approval or rejection is performed by this status." in stdout


def test_operator_memory_loop_review_status_format_markdown_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "review-status",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.1 Human-Gated Proposal Review Status\n")


def test_operator_memory_loop_review_status_format_json_returns_deterministic_json(tmp_path):
    args = [
        "memory-loop",
        "review-status",
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
    assert payload["boundary"] == HUMAN_GATED_PROPOSAL_REVIEW_STATUS_BOUNDARY
    assert payload["count"] == 9
    assert payload["status"] == human_gated_proposal_review_status_report()
    assert [item["review_id"] for item in payload["items"]] == list(REVIEW_IDS)
    assert set(payload["items"][0]) == DATACLASS_FIELDS


def test_operator_review_status_command_is_read_only_and_creates_no_local_storage(tmp_path):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["memory-loop", "review-status", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "review-status",
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


def test_operator_review_status_command_creates_no_proposals(tmp_path):
    _run_operator(["memory-loop", "review-status", "--workspace-root", str(tmp_path)])

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_review_status_command_creates_no_approved_memories(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "review-status",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == {
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
    }
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


def test_existing_p4_m0_project_seed_approval_runbook_still_works(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["project-seed", "approval-runbook", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M0.8 Seed Approval Runbook\n")
    assert not (tmp_path / ".local").exists()


def test_existing_recall_trace_still_passes_through_focused_suite(tmp_path):
    proposal_id = _propose(tmp_path, "P4-M1.1 keeps existing recall trace behavior intact.")
    approve_code, approve_payload, approve_stderr, _ = _run_operator(
        [
            "approve",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--approver",
            "human",
        ]
    )
    recall_code, recall_payload, recall_stderr, _ = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "recall trace behavior",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
        ]
    )

    assert approve_code == 0
    assert approve_stderr == ""
    assert approve_payload["status"] == "approved"
    assert recall_code == 0
    assert recall_stderr == ""
    assert recall_payload["count"] == 1
    trace = recall_payload["results"][0]["trace"]
    assert trace["query"] == "recall trace behavior"
    assert trace["matched_terms"] == ["recall", "trace", "behavior"]
    assert trace["rank"] == 1


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_human_gated_proposal_review_status():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_human_gated_proposal_review_status" not in entry_points


def test_custom_markdown_render_accepts_read_only_items():
    item = HumanGatedProposalReviewStatusItem(
        review_order=1,
        review_id="custom-review",
        review_name="Custom review",
        human_review_question="Can the human review the custom item?",
        allowed_system_output="Review status text only.",
        prohibited_automation="No write.",
        ready_signal="Visible custom review.",
        blocking_signal="Hidden custom review.",
        p4_m0_or_p4_m1_dependency="P4-M1 read-only boundary.",
    )

    markdown = render_human_gated_proposal_review_status_markdown([item])

    assert "custom-review" in markdown
    assert "Can the human review the custom item?" in markdown


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


def _propose(tmp_path: Path, content: str) -> str:
    exit_code, payload, stderr, _ = _run_operator(
        [
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--content",
            content,
            "--source",
            "operator-test",
        ]
    )
    assert exit_code == 0
    assert stderr == ""
    return str(payload["proposal_id"])
