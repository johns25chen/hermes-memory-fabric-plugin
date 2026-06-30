from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m1_human_gated_memory_loop_checklist import (
    HUMAN_GATED_MEMORY_LOOP_BOUNDARY,
    HumanGatedMemoryLoopChecklistItem,
    human_gated_memory_loop_checklist_as_dicts,
    human_gated_memory_loop_checklist_gate_ids,
    human_gated_memory_loop_status_report,
    list_human_gated_memory_loop_checklist_items,
    render_human_gated_memory_loop_checklist_markdown,
)


GATE_IDS = (
    "human-intent-requested",
    "candidate-presented",
    "human-content-review",
    "human-approve-or-reject",
    "recall-verification",
    "lifecycle-optional",
    "do-not-retry-optional",
    "automation-boundary-confirmed",
)

DATACLASS_FIELDS = {
    "gate_order",
    "gate_id",
    "gate_name",
    "required_human_action",
    "allowed_system_output",
    "prohibited_automation",
    "validation_signal",
    "p4_m0_dependency",
}

DISABLED_STATUS_FLAGS = (
    "memory_write_enabled",
    "approval_enabled",
    "rejection_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
    "v7_started",
    "productization_started",
)

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
    "inject",
    "call-agent",
    "execute",
    "deploy",
    "api",
    "mcp",
    "connector",
}


def test_checklist_gate_order_is_deterministic():
    assert [item.gate_order for item in list_human_gated_memory_loop_checklist_items()] == list(range(1, 9))
    assert human_gated_memory_loop_checklist_gate_ids() == GATE_IDS
    assert human_gated_memory_loop_checklist_gate_ids() == human_gated_memory_loop_checklist_gate_ids()


def test_checklist_has_exactly_8_gates():
    assert len(list_human_gated_memory_loop_checklist_items()) == 8


def test_gate_ids_match_required_gate_ids():
    assert human_gated_memory_loop_checklist_gate_ids() == GATE_IDS


def test_every_item_has_required_non_empty_fields():
    for item in list_human_gated_memory_loop_checklist_items():
        assert item.gate_name.strip()
        assert item.required_human_action.strip()
        assert item.allowed_system_output.strip()
        assert item.prohibited_automation.strip()
        assert item.validation_signal.strip()
        assert item.p4_m0_dependency.strip()


def test_markdown_render_contains_all_8_gate_ids():
    markdown = render_human_gated_memory_loop_checklist_markdown()

    for gate_id in GATE_IDS:
        assert gate_id in markdown


def test_markdown_render_contains_read_only_boundary_and_disabled_actions():
    markdown = render_human_gated_memory_loop_checklist_markdown()

    assert "read-only checklist/status only" in markdown
    assert "does not write memory" in markdown
    assert "does not approve memory" in markdown
    assert "does not reject memory" in markdown
    assert "does not bulk import memory" in markdown
    assert "does not call agents" in markdown


def test_dict_conversion_is_deterministic():
    first = human_gated_memory_loop_checklist_as_dicts()
    second = human_gated_memory_loop_checklist_as_dicts()

    assert first == second
    assert [item["gate_id"] for item in first] == list(GATE_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = human_gated_memory_loop_status_report()
    second = human_gated_memory_loop_status_report()

    assert first == second
    assert first["phase"] == "P4-M1.0"
    assert first["feature"] == "Human-Gated Memory Loop Checklist"
    assert first["mode"] == "read-only"
    assert first["checklist_count"] == 8
    assert first["boundary"] == HUMAN_GATED_MEMORY_LOOP_BOUNDARY


def test_status_report_has_all_disabled_flags_set_to_false():
    status = human_gated_memory_loop_status_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert human_gated_memory_loop_status_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_checklist_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "checklist", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.0 Human-Gated Memory Loop Checklist\n")
    assert "## Status Report" in stdout
    assert HUMAN_GATED_MEMORY_LOOP_BOUNDARY in stdout


def test_operator_memory_loop_checklist_format_markdown_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "checklist",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M1.0 Human-Gated Memory Loop Checklist\n")


def test_operator_memory_loop_checklist_format_json_returns_deterministic_json(tmp_path):
    args = [
        "memory-loop",
        "checklist",
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
    assert payload["boundary"] == HUMAN_GATED_MEMORY_LOOP_BOUNDARY
    assert payload["count"] == 8
    assert payload["status"] == human_gated_memory_loop_status_report()
    assert [item["gate_id"] for item in payload["items"]] == list(GATE_IDS)
    assert set(payload["items"][0]) == DATACLASS_FIELDS


def test_operator_checklist_command_is_read_only_and_creates_no_local_storage(tmp_path):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["memory-loop", "checklist", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "checklist",
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


def test_operator_checklist_command_creates_no_proposals(tmp_path):
    _run_operator(["memory-loop", "checklist", "--workspace-root", str(tmp_path)])

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_checklist_command_creates_no_approved_memories(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "checklist",
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
        "manual-authorization-evidence-envelope",
        "human-confirmation-snapshot-contract",
        "execution-preconditions-snapshot-map",
        "execution-risk-acknowledgement-map",
        "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    }
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


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
    proposal_id = _propose(tmp_path, "P4-M1.0 keeps existing recall trace behavior intact.")
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


def test_no_pyproject_entry_point_is_added_for_human_gated_memory_loop_checklist():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m1_human_gated_memory_loop_checklist" not in entry_points


def test_custom_markdown_render_accepts_read_only_items():
    item = HumanGatedMemoryLoopChecklistItem(
        gate_order=1,
        gate_id="custom-gate",
        gate_name="Custom gate",
        required_human_action="Human reviews custom gate.",
        allowed_system_output="Checklist text only.",
        prohibited_automation="No write.",
        validation_signal="Visible custom gate.",
        p4_m0_dependency="P4-M0 manual boundary.",
    )

    markdown = render_human_gated_memory_loop_checklist_markdown([item])

    assert "custom-gate" in markdown
    assert "Human reviews custom gate." in markdown


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
