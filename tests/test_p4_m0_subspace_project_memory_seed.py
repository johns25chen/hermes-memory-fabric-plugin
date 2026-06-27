from __future__ import annotations

import io
import json
import tomllib
from pathlib import Path

import pytest

from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_project_seed import (
    PROJECT_MEMORY_SEED_NAMESPACE,
    PROJECT_MEMORY_SEED_PROJECT,
    PROJECT_MEMORY_SEED_SOURCE,
    get_project_memory_seed,
    list_project_memory_seeds,
    project_memory_seed_ids,
    render_project_memory_seed_pack,
)
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


REQUIRED_SEED_IDS = (
    "civilization-core-identity",
    "subspace-memory-system-role",
    "v6-16-stable-kernel-boundary",
    "p4-m0-human-gated-chain",
    "no-v7-without-human-authorization",
    "no-productization-no-deployment-boundary",
    "manual-operator-validation-discipline",
    "do-not-retry-and-lifecycle-governance",
)


def test_seed_list_is_deterministic():
    assert project_memory_seed_ids() == REQUIRED_SEED_IDS
    assert project_memory_seed_ids() == tuple(seed.seed_id for seed in list_project_memory_seeds())
    assert project_memory_seed_ids() == tuple(seed.seed_id for seed in list_project_memory_seeds())


def test_seed_ids_are_unique():
    seed_ids = project_memory_seed_ids()

    assert len(seed_ids) == len(set(seed_ids))


def test_required_seed_ids_are_present():
    assert project_memory_seed_ids() == REQUIRED_SEED_IDS


def test_every_seed_uses_required_metadata():
    for seed in list_project_memory_seeds():
        assert seed.project == PROJECT_MEMORY_SEED_PROJECT == "civilization-core"
        assert seed.namespace == PROJECT_MEMORY_SEED_NAMESPACE == "project-seed"
        assert seed.source == PROJECT_MEMORY_SEED_SOURCE == "p4-m0.7-project-memory-seed"
        assert seed.confidence == 1.0
        assert "p4-m0.7" in seed.tags
        assert "project-seed" in seed.tags
        assert seed.seed_id in seed.tags


def test_unknown_seed_id_raises_project_memory_seed_not_found():
    with pytest.raises(ValueError, match="project_memory_seed_not_found"):
        get_project_memory_seed("missing-seed")


def test_empty_seed_id_raises_validation_error():
    with pytest.raises(ValueError, match="seed_id_must_be_non_empty"):
        get_project_memory_seed(" ")


def test_render_seed_pack_contains_all_seed_ids_and_boundary_statement():
    pack = render_project_memory_seed_pack()

    for seed_id in REQUIRED_SEED_IDS:
        assert seed_id in pack
    assert "This seed pack is human-provided context only." in pack
    assert "It does not approve memory." in pack
    assert "It does not write approved memory." in pack
    assert "It does not authorize execution." in pack
    assert "It does not call agents." in pack


def test_list_show_and_pack_are_read_only_and_create_no_storage_files(tmp_path):
    list_code, _, list_stderr, _ = _run_operator(
        ["project-seed", "list", "--workspace-root", str(tmp_path)]
    )
    show_code, _, show_stderr, _ = _run_operator(
        [
            "project-seed",
            "show",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            "civilization-core-identity",
        ]
    )
    pack_code, _, pack_stderr, pack_stdout = _run_operator(
        ["project-seed", "pack", "--workspace-root", str(tmp_path)]
    )

    assert list_code == 0
    assert list_stderr == ""
    assert show_code == 0
    assert show_stderr == ""
    assert pack_code == 0
    assert pack_stderr == ""
    assert "# P4-M0.7 Project Memory Seed Pack" in pack_stdout
    assert not (tmp_path / ".local").exists()


def test_operator_project_seed_list_returns_deterministic_json(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["project-seed", "list", "--workspace-root", str(tmp_path)]
    )
    second_code, second_payload, second_stderr, second_stdout = _run_operator(
        ["project-seed", "list", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert stderr == ""
    assert second_code == 0
    assert second_stderr == ""
    assert stdout == second_stdout
    assert payload == second_payload
    assert payload["count"] == 8
    assert [seed["seed_id"] for seed in payload["seeds"]] == list(REQUIRED_SEED_IDS)
    assert "content" not in payload["seeds"][0]


def test_operator_project_seed_show_returns_one_seed(tmp_path):
    exit_code, payload, stderr, _ = _run_operator(
        [
            "project-seed",
            "show",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            "no-v7-without-human-authorization",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["seed_id"] == "no-v7-without-human-authorization"
    assert payload["project"] == "civilization-core"
    assert payload["namespace"] == "project-seed"
    assert "No v7 work starts" in payload["content"]


def test_operator_project_seed_pack_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["project-seed", "pack", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M0.7 Project Memory Seed Pack\n")
    assert "civilization-core-identity" in stdout


def test_operator_project_seed_propose_creates_exactly_one_pending_proposal(tmp_path):
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
    store = create_workspace_subspace_memory_store(tmp_path)
    proposals_path = tmp_path / ".local" / "subspace_memory" / "proposals.jsonl"
    proposal_lines = _line_count(proposals_path)
    proposal_record = json.loads(proposals_path.read_text(encoding="utf-8").splitlines()[0])

    assert exit_code == 0
    assert stderr == ""
    assert payload["seed_id"] == "civilization-core-identity"
    assert payload["status"] == "pending"
    assert payload["project"] == "civilization-core"
    assert payload["namespace"] == "project-seed"
    assert payload["requires_human_approval"] is True
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")
    assert proposal_lines == 1
    assert proposal_record["source"] == "p4-m0.7-project-memory-seed:proposed-by:human"
    assert proposal_record["tags"] == [
        "civilization-core-identity",
        "p4-m0.7",
        "project-seed",
    ]
    assert [event.event_type for event in store.list_audit_events()] == ["proposal_created"]


def test_operator_project_seed_propose_does_not_create_approved_memory_record(tmp_path):
    exit_code, _, stderr, _ = _run_operator(
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
    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_project_seed_propose_requires_actor(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "project-seed",
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            "civilization-core-identity",
        ]
    )

    assert exit_code != 0
    assert payload == {}
    assert stdout == ""
    assert "the following arguments are required: --actor" in stderr


def test_operator_project_seed_propose_requires_valid_seed_id(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "project-seed",
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--seed-id",
            "missing-seed",
            "--actor",
            "human",
        ]
    )

    assert exit_code == 1
    assert payload == {}
    assert stdout == ""
    assert "project_memory_seed_not_found" in stderr
    assert not (tmp_path / ".local").exists()


def test_proposed_seed_can_be_approved_later_by_existing_approve_command(tmp_path):
    proposal_id = _propose_seed(tmp_path, "p4-m0-human-gated-chain")

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


def test_approved_seed_can_be_recalled_by_existing_recall_command(tmp_path):
    _approve_seed(tmp_path, "p4-m0-human-gated-chain")

    exit_code, payload, stderr, _ = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "human-gated",
            "--project",
            "civilization-core",
            "--namespace",
            "project-seed",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["count"] == 1
    assert payload["results"][0]["project"] == "civilization-core"
    assert payload["results"][0]["namespace"] == "project-seed"


def test_approved_seed_recall_includes_p4_m0_5_explainable_trace(tmp_path):
    _approve_seed(tmp_path, "manual-operator-validation-discipline")

    _, payload, _, _ = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "validation deterministic",
        ]
    )

    trace = payload["results"][0]["trace"]
    assert trace["rank"] == 1
    assert trace["query"] == "validation deterministic"
    assert trace["matched_terms"] == ["validation", "deterministic"]
    assert trace["explanation"] == "Matched 2 query terms: validation, deterministic."


def test_approved_seed_can_be_marked_stale_with_lifecycle_command(tmp_path):
    memory_id = _approve_seed(tmp_path, "manual-operator-validation-discipline")

    exit_code, payload, stderr, _ = _run_operator(
        [
            "lifecycle",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory_id,
            "--state",
            "stale",
            "--actor",
            "human",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["memory_id"] == memory_id
    assert payload["lifecycle"] == "stale"


def test_approved_seed_can_be_marked_do_not_retry_with_p4_m0_6_command(tmp_path):
    memory_id = _approve_seed(tmp_path, "do-not-retry-and-lifecycle-governance")

    exit_code, payload, stderr, _ = _run_operator(
        [
            "do-not-retry",
            "set",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory_id,
            "--reason",
            "manual guard",
            "--actor",
            "human",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["memory_id"] == memory_id
    assert payload["do_not_retry"]["reason"] == "manual guard"


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_project_seed():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m0_subspace_project_seed" not in entry_points


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


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
