from __future__ import annotations

import io
import json
import tomllib
from pathlib import Path

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_recall_pack import run_recall_pack_export
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def test_approved_memory_defaults_to_active_lifecycle(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    memory = _approved_memory(store, content="Default active lifecycle memory.")

    assert memory.lifecycle == "active"
    assert _memory_records(tmp_path)[0]["lifecycle"] == "active"


def test_old_memory_record_without_lifecycle_is_read_as_active(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Old record remains active for recall.")
    records = _memory_records(tmp_path)
    records[0].pop("lifecycle")
    _write_memory_records(tmp_path, records)

    reopened = SubspaceMemoryStore(tmp_path)
    results = reopened.recall("old active")

    assert [result.memory_id for result in results] == [memory.id]
    assert results[0].lifecycle == "active"


def test_valid_lifecycle_transitions_work(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Lifecycle transition memory.")

    stale = store.set_memory_lifecycle(memory.id, "stale", actor="human", reason="manual review")
    archived = store.set_memory_lifecycle(memory.id, "archived", actor="human")
    active = store.set_memory_lifecycle(memory.id, "active", actor="human")

    assert stale.lifecycle == "stale"
    assert archived.lifecycle == "archived"
    assert active.lifecycle == "active"
    assert _memory_records(tmp_path)[0]["lifecycle"] == "active"


def test_invalid_lifecycle_state_is_rejected(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Invalid lifecycle is rejected.")

    with pytest.raises(ValueError, match="invalid_lifecycle_state"):
        store.set_memory_lifecycle(memory.id, "deleted", actor="human")


def test_lifecycle_update_requires_existing_memory_id(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match="memory_not_found"):
        store.set_memory_lifecycle("memory:missing", "stale", actor="human")


def test_lifecycle_update_creates_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Lifecycle audit event memory.")

    store.set_memory_lifecycle(memory.id, "stale", actor="human", reason="manual stale mark")

    event = store.list_audit_events()[-1]
    assert event.event_type == "memory_lifecycle_updated"
    assert event.target_id == memory.id
    assert event.actor == "human"
    assert event.detail == {
        "previous_lifecycle": "active",
        "lifecycle": "stale",
        "reason": "manual stale mark",
    }


def test_lifecycle_update_does_not_create_proposal_or_memory_records(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Lifecycle update rewrites existing memory record.")
    proposals_before = _line_count(tmp_path / "proposals.jsonl")
    memories_before = _line_count(tmp_path / "memories.jsonl")

    store.set_memory_lifecycle(memory.id, "archived", actor="human")

    assert _line_count(tmp_path / "proposals.jsonl") == proposals_before
    assert _line_count(tmp_path / "memories.jsonl") == memories_before


def test_default_recall_returns_active_memories_only(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    active = _approved_memory(store, content="Lifecycle keyword active memory.")
    stale = _approved_memory(store, content="Lifecycle keyword stale memory.")
    archived = _approved_memory(store, content="Lifecycle keyword archived memory.")
    store.set_memory_lifecycle(stale.id, "stale", actor="human")
    store.set_memory_lifecycle(archived.id, "archived", actor="human")

    results = store.recall("lifecycle keyword")

    assert [result.memory_id for result in results] == [active.id]
    assert results[0].lifecycle == "active"


def test_stale_memories_are_excluded_from_default_recall(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Stale lifecycle recall memory.")
    store.set_memory_lifecycle(memory.id, "stale", actor="human")

    assert store.recall("stale lifecycle") == []


def test_archived_memories_are_excluded_from_default_recall(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Archived lifecycle recall memory.")
    store.set_memory_lifecycle(memory.id, "archived", actor="human")

    assert store.recall("archived lifecycle") == []


def test_explicit_include_stale_recalls_stale_memory(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Explicit stale lifecycle memory.")
    store.set_memory_lifecycle(memory.id, "stale", actor="human")

    results = store.recall("explicit stale", include_stale=True)

    assert [result.memory_id for result in results] == [memory.id]
    assert results[0].lifecycle == "stale"


def test_explicit_include_archived_recalls_archived_memory(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Explicit archived lifecycle memory.")
    store.set_memory_lifecycle(memory.id, "archived", actor="human")

    results = store.recall("explicit archived", include_archived=True)

    assert [result.memory_id for result in results] == [memory.id]
    assert results[0].lifecycle == "archived"


def test_manual_operator_lifecycle_command_updates_lifecycle_and_outputs_json(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Operator lifecycle command memory.")

    exit_code, payload, stderr = _run_operator(
        [
            "lifecycle",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory.id,
            "--state",
            "stale",
            "--actor",
            "human",
            "--reason",
            "manual operator mark",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload == {
        "lifecycle": "stale",
        "memory_id": memory.id,
        "previous_lifecycle": "active",
        "status": "approved",
        "storage_root": str(tmp_path / ".local" / "subspace_memory"),
    }


def test_operator_recall_respects_lifecycle_default_and_include_flags(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    active = _approved_memory(store, content="Operator lifecycle active result.")
    stale = _approved_memory(store, content="Operator lifecycle stale result.")
    archived = _approved_memory(store, content="Operator lifecycle archived result.")
    store.set_memory_lifecycle(stale.id, "stale", actor="human")
    store.set_memory_lifecycle(archived.id, "archived", actor="human")

    default_code, default_payload, default_stderr = _run_operator(
        ["recall", "--workspace-root", str(tmp_path), "--query", "operator lifecycle"]
    )
    include_code, include_payload, include_stderr = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "operator lifecycle",
            "--include-stale",
            "--include-archived",
        ]
    )

    assert default_code == 0
    assert default_stderr == ""
    assert [result["memory_id"] for result in default_payload["results"]] == [active.id]
    assert include_code == 0
    assert include_stderr == ""
    assert {result["memory_id"] for result in include_payload["results"]} == {
        active.id,
        stale.id,
        archived.id,
    }
    assert {result["lifecycle"] for result in include_payload["results"]} == {
        "active",
        "stale",
        "archived",
    }


def test_recall_pack_export_includes_lifecycle_metadata(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Recall pack lifecycle metadata memory.")

    exit_code, pack, stderr = _run_recall_pack(
        ["--workspace-root", str(tmp_path), "--query", "recall pack lifecycle"]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"### 1. {memory.id}" in pack
    assert "- Lifecycle: active" in pack


def test_recall_pack_export_respects_lifecycle_default_and_include_flags(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    stale = _approved_memory(store, content="Recall pack stale lifecycle memory.")
    archived = _approved_memory(store, content="Recall pack archived lifecycle memory.")
    store.set_memory_lifecycle(stale.id, "stale", actor="human")
    store.set_memory_lifecycle(archived.id, "archived", actor="human")

    default_code, default_pack, default_stderr = _run_recall_pack(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "recall pack lifecycle",
            "--include-empty",
        ]
    )
    stale_code, stale_pack, stale_stderr = _run_recall_pack(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "recall pack lifecycle",
            "--include-stale",
        ]
    )
    archived_code, archived_pack, archived_stderr = _run_recall_pack(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "recall pack lifecycle",
            "--include-archived",
        ]
    )

    assert default_code == 0
    assert default_stderr == ""
    assert "No approved recall results matched this query." in default_pack
    assert stale_code == 0
    assert stale_stderr == ""
    assert f"### 1. {stale.id}" in stale_pack
    assert "- Lifecycle: stale" in stale_pack
    assert archived_code == 0
    assert archived_stderr == ""
    assert f"### 1. {archived.id}" in archived_pack
    assert "- Lifecycle: archived" in archived_pack


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_lifecycle_state():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m0_subspace_lifecycle" not in entry_points


def _approved_memory(store: SubspaceMemoryStore, *, content: str):
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="lifecycle",
        content=content,
        source="lifecycle-test",
    )
    return store.approve_proposal(proposal.id, approver="human")


def _memory_records(storage_root: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in (storage_root / "memories.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_memory_records(storage_root: Path, records: list[dict[str, object]]) -> None:
    (storage_root / "memories.jsonl").write_text(
        "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    payload = json.loads(stdout.getvalue()) if stdout.getvalue() else {}
    return exit_code, payload, stderr.getvalue()


def _run_recall_pack(argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_recall_pack_export(argv, stdout=stdout, stderr=stderr)

    return exit_code, stdout.getvalue(), stderr.getvalue()
