from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

import pytest

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m0_subspace_project_seed import (
    get_project_memory_seed,
    project_memory_seed_ids,
)
from hermes_memory_fabric.p4_m0_subspace_seed_approval_runbook import (
    SEED_APPROVAL_RUNBOOK_BOUNDARY,
    SeedApprovalRunbookEntry,
    get_seed_approval_runbook_entry,
    list_seed_approval_runbook_entries,
    render_seed_approval_runbook_markdown,
    seed_approval_runbook_as_dicts,
    seed_approval_runbook_seed_ids,
)


RUNBOOK_SEED_IDS = (
    "civilization-core-identity",
    "subspace-memory-system-role",
    "v6-16-stable-kernel-boundary",
    "no-v7-without-human-authorization",
    "no-productization-no-deployment-boundary",
    "p4-m0-human-gated-chain",
    "manual-operator-validation-discipline",
    "do-not-retry-and-lifecycle-governance",
)


DATACLASS_FIELDS = {
    "order",
    "seed_id",
    "approval_stage",
    "rationale",
    "manual_propose_example",
    "manual_approve_note",
    "recall_query",
    "validation_expectation",
    "boundary",
}


def test_runbook_seed_order_is_deterministic():
    assert seed_approval_runbook_seed_ids() == RUNBOOK_SEED_IDS
    assert seed_approval_runbook_seed_ids() == tuple(
        entry.seed_id for entry in list_seed_approval_runbook_entries()
    )
    assert seed_approval_runbook_seed_ids() == tuple(
        entry.seed_id for entry in list_seed_approval_runbook_entries()
    )


def test_runbook_seed_ids_match_p4_m0_7_project_seed_ids():
    assert set(seed_approval_runbook_seed_ids()) == set(project_memory_seed_ids())


def test_every_entry_references_existing_project_seed():
    for entry in list_seed_approval_runbook_entries():
        assert get_project_memory_seed(entry.seed_id).seed_id == entry.seed_id


def test_every_entry_has_non_empty_rationale():
    for entry in list_seed_approval_runbook_entries():
        assert entry.rationale.strip()


def test_every_entry_has_non_empty_manual_propose_example():
    for entry in list_seed_approval_runbook_entries():
        assert entry.manual_propose_example.strip()
        assert f"--seed-id {entry.seed_id}" in entry.manual_propose_example


def test_every_entry_has_non_empty_manual_approve_note():
    for entry in list_seed_approval_runbook_entries():
        assert entry.manual_approve_note.strip()
        assert "approve command" in entry.manual_approve_note


def test_every_entry_has_non_empty_recall_query():
    for entry in list_seed_approval_runbook_entries():
        assert entry.recall_query.strip()


def test_every_entry_has_non_empty_validation_expectation():
    for entry in list_seed_approval_runbook_entries():
        assert entry.validation_expectation.strip()


def test_every_entry_boundary_says_no_automatic_approval_or_no_bulk_import():
    for entry in list_seed_approval_runbook_entries():
        assert "no automatic approval" in entry.boundary
        assert "no bulk import" in entry.boundary


def test_unknown_seed_id_raises_seed_approval_runbook_entry_not_found():
    with pytest.raises(ValueError, match="seed_approval_runbook_entry_not_found"):
        get_seed_approval_runbook_entry("missing-seed")


def test_empty_seed_id_raises_validation_error():
    with pytest.raises(ValueError, match="seed_id_must_be_non_empty"):
        get_seed_approval_runbook_entry(" ")


def test_markdown_render_contains_all_seed_ids():
    markdown = render_seed_approval_runbook_markdown()

    for seed_id in RUNBOOK_SEED_IDS:
        assert seed_id in markdown


def test_markdown_render_contains_human_guidance_boundary():
    markdown = render_seed_approval_runbook_markdown()

    assert "This runbook is human guidance only." in markdown


def test_markdown_render_contains_no_automatic_approval_boundary():
    markdown = render_seed_approval_runbook_markdown()

    assert "no automatic approval" in markdown


def test_markdown_render_contains_no_bulk_import_boundary():
    markdown = render_seed_approval_runbook_markdown()

    assert "does not bulk import" in markdown
    assert "no bulk import" in markdown


def test_dict_conversion_is_deterministic():
    first = seed_approval_runbook_as_dicts()
    second = seed_approval_runbook_as_dicts()

    assert first == second
    assert [entry["seed_id"] for entry in first] == list(RUNBOOK_SEED_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_operator_project_seed_approval_runbook_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["project-seed", "approval-runbook", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M0.8 Seed Approval Runbook\n")
    assert "Manual propose example" in stdout
    assert "Manual approve note" in stdout
    assert "Recall query" in stdout


def test_operator_project_seed_approval_runbook_format_markdown_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "project-seed",
            "approval-runbook",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M0.8 Seed Approval Runbook\n")


def test_operator_project_seed_approval_runbook_format_json_returns_deterministic_json(tmp_path):
    args = [
        "project-seed",
        "approval-runbook",
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
    assert payload["boundary"] == SEED_APPROVAL_RUNBOOK_BOUNDARY
    assert payload["count"] == 8
    assert [entry["seed_id"] for entry in payload["entries"]] == list(RUNBOOK_SEED_IDS)
    assert set(payload["entries"][0]) == DATACLASS_FIELDS


def test_operator_runbook_commands_are_read_only_and_create_no_storage_files(tmp_path):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["project-seed", "approval-runbook", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "project-seed",
            "approval-runbook",
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


def test_operator_runbook_does_not_create_proposal_records(tmp_path):
    _run_operator(["project-seed", "approval-runbook", "--workspace-root", str(tmp_path)])

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_runbook_does_not_create_approved_memory_records(tmp_path):
    _run_operator(
        [
            "project-seed",
            "approval-runbook",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_no_approve_all_import_or_bulk_import_command_is_exposed():
    commands = _project_seed_commands()

    assert "approve-all" not in commands
    assert "import" not in commands
    assert "bulk-import" not in commands


def test_existing_project_seed_propose_still_creates_exactly_one_pending_proposal(tmp_path):
    exit_code, payload, stderr, _ = _run_operator(
        [
            "project-seed",
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            "civilization-core-identity",
            "--actor",
            "human",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["status"] == "pending"
    assert _line_count(tmp_path / ".local" / "subspace_memory" / "proposals.jsonl") == 1
    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_existing_approve_command_can_still_approve_one_proposal(tmp_path):
    proposal_id = _propose_seed(tmp_path, "civilization-core-identity")

    exit_code, payload, stderr, _ = _run_operator(
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

    assert exit_code == 0
    assert stderr == ""
    assert payload["status"] == "approved"
    assert payload["proposal_id"] == proposal_id
    assert _line_count(tmp_path / ".local" / "subspace_memory" / "memories.jsonl") == 1


def test_approved_seed_can_still_be_recalled_and_includes_p4_m0_5_trace(tmp_path):
    _approve_seed(tmp_path, "p4-m0-human-gated-chain")

    exit_code, payload, stderr, _ = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "human-gated proposal approval",
            "--project",
            "civilization-core",
            "--namespace",
            "project-seed",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["count"] == 1
    trace = payload["results"][0]["trace"]
    assert trace["rank"] == 1
    assert trace["query"] == "human-gated proposal approval"
    assert trace["matched_terms"] == ["human", "gated", "proposal", "approval"]


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_seed_approval_runbook():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m0_subspace_seed_approval_runbook" not in entry_points


def test_custom_markdown_render_accepts_read_only_entries():
    entry = SeedApprovalRunbookEntry(
        order=1,
        seed_id="civilization-core-identity",
        approval_stage="foundation",
        rationale="Custom rationale.",
        manual_propose_example="project-seed propose --seed-id civilization-core-identity",
        manual_approve_note="Use the existing approve command.",
        recall_query="identity",
        validation_expectation="Recall identity.",
        boundary="no automatic approval and no bulk import",
    )

    markdown = render_seed_approval_runbook_markdown([entry])

    assert "Custom rationale." in markdown
    assert "civilization-core-identity" in markdown


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _project_seed_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            project_seed_parser = action.choices["project-seed"]
            break
    else:
        raise AssertionError("project-seed parser not found")

    for action in project_seed_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("project-seed subcommands not found")


def _propose_seed(tmp_path: Path, seed_id: str) -> str:
    exit_code, payload, stderr, _ = _run_operator(
        [
            "project-seed",
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            seed_id,
            "--actor",
            "human",
        ]
    )
    assert exit_code == 0
    assert stderr == ""
    return str(payload["proposal_id"])


def _approve_seed(tmp_path: Path, seed_id: str) -> str:
    proposal_id = _propose_seed(tmp_path, seed_id)
    exit_code, payload, stderr, _ = _run_operator(
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
    assert exit_code == 0
    assert stderr == ""
    return str(payload["memory_id"])


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines()) if path.exists() else 0
