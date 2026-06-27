from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore
from hermes_memory_fabric.p4_m0_subspace_workspace import (
    WorkspaceSubspaceMemoryConfig,
    create_workspace_subspace_memory_store,
    resolve_workspace_subspace_memory_root,
)


def test_default_workspace_storage_root_resolves_under_local_subspace_memory(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    resolved = resolve_workspace_subspace_memory_root(workspace)

    assert resolved == workspace / ".local" / "subspace_memory"


def test_workspace_config_exposes_resolved_storage_root(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    config = WorkspaceSubspaceMemoryConfig(workspace_root=workspace)

    assert config.storage_root == workspace / ".local" / "subspace_memory"


def test_explicit_workspace_root_is_required():
    with pytest.raises(ValueError, match="workspace_root_must_be_explicit"):
        resolve_workspace_subspace_memory_root(None)  # type: ignore[arg-type]


def test_missing_workspace_root_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="workspace_root_must_exist"):
        resolve_workspace_subspace_memory_root(tmp_path / "missing")


def test_non_directory_workspace_root_is_rejected(tmp_path):
    workspace_file = tmp_path / "workspace-file"
    workspace_file.write_text("not a directory", encoding="utf-8")

    with pytest.raises(ValueError, match="workspace_root_must_be_directory"):
        resolve_workspace_subspace_memory_root(workspace_file)


def test_absolute_storage_dir_is_rejected(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    with pytest.raises(ValueError, match="storage_dir_must_be_relative"):
        resolve_workspace_subspace_memory_root(workspace, storage_dir=tmp_path / "outside")


@pytest.mark.parametrize("storage_dir", ["../outside", ".local/../outside", "safe/../../outside"])
def test_parent_directory_escape_is_rejected(tmp_path, storage_dir):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    with pytest.raises(ValueError, match="storage_dir_must_not_escape_workspace"):
        resolve_workspace_subspace_memory_root(workspace, storage_dir=storage_dir)


def test_factory_returns_subspace_memory_store_using_workspace_root(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    store = create_workspace_subspace_memory_store(workspace)

    assert isinstance(store, SubspaceMemoryStore)
    assert store.storage_root == workspace / ".local" / "subspace_memory"


def test_workspace_store_propose_approve_recall_and_audit(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    store = create_workspace_subspace_memory_store(workspace)

    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="workspace",
        content="Workspace store persists approved memory locally.",
        source="workspace-test",
    )
    memory = store.approve_proposal(proposal.id, approver="human")
    results = store.recall("workspace approved", project="hermes-memory-fabric")
    events = store.list_audit_events()

    assert memory.proposal_id == proposal.id
    assert [result.memory_id for result in results] == [memory.id]
    assert [event.event_type for event in events] == ["proposal_created", "proposal_approved"]
    assert store.storage_root == workspace / ".local" / "subspace_memory"


def test_workspace_store_writes_no_files_outside_storage_root(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    storage_root = workspace / ".local" / "subspace_memory"
    store = create_workspace_subspace_memory_store(workspace)
    proposal = store.propose_memory(project="p", namespace="n", content="workspace-only files")
    store.approve_proposal(proposal.id, approver="human")

    all_files = [path for path in workspace.rglob("*") if path.is_file()]
    outside_files = [path for path in all_files if not path.is_relative_to(storage_root)]

    assert outside_files == []
    assert sorted(path.name for path in storage_root.iterdir()) == [
        "audit.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
    ]


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
