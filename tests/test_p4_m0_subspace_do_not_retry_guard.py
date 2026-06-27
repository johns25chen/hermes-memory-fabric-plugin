from __future__ import annotations

import io
import json
import tomllib
from dataclasses import asdict
from pathlib import Path

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_recall_pack import run_recall_pack_export
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def test_approved_memory_defaults_to_no_do_not_retry_metadata(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    memory = _approved_memory(store, content="Default do not retry metadata is absent.")

    assert memory.do_not_retry is None
    result = store.recall("default metadata")[0]
    assert result.do_not_retry is None
    assert result.do_not_retry_warning is None


def test_old_memory_record_without_do_not_retry_reads_as_no_warning(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Old do not retry record remains readable.")
    records = _memory_records(tmp_path)
    records[0].pop("do_not_retry", None)
    _write_memory_records(tmp_path, records)

    reopened = SubspaceMemoryStore(tmp_path)
    result = reopened.recall("old readable")[0]

    assert result.memory_id == memory.id
    assert result.do_not_retry is None
    assert result.do_not_retry_warning is None


def test_set_do_not_retry_stores_reason_actor_alternative_and_updated_at(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Manual do not retry metadata memory.")

    updated = store.set_do_not_retry(
        memory.id,
        reason="Tried before and failed.",
        actor="human",
        alternative="Use the documented fallback.",
    )

    assert updated.do_not_retry is not None
    assert updated.do_not_retry.enabled is True
    assert updated.do_not_retry.reason == "Tried before and failed."
    assert updated.do_not_retry.actor == "human"
    assert updated.do_not_retry.alternative == "Use the documented fallback."
    assert updated.do_not_retry.updated_at.endswith("Z")
    assert _memory_records(tmp_path)[0]["do_not_retry"]["reason"] == "Tried before and failed."


def test_set_do_not_retry_requires_existing_memory_id(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match="memory_not_found"):
        store.set_do_not_retry("memory:missing", reason="manual reason", actor="human")


def test_set_do_not_retry_requires_non_empty_reason(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Reason validation memory.")

    with pytest.raises(ValueError, match="reason_must_be_non_empty"):
        store.set_do_not_retry(memory.id, reason=" ", actor="human")


def test_set_do_not_retry_requires_non_empty_actor(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Actor validation memory.")

    with pytest.raises(ValueError, match="actor_must_be_non_empty"):
        store.set_do_not_retry(memory.id, reason="manual reason", actor=" ")


def test_clear_do_not_retry_removes_metadata(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Clear do not retry metadata memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")

    cleared = store.clear_do_not_retry(memory.id, actor="human", reason="manual clear")

    assert cleared.do_not_retry is None
    assert _memory_records(tmp_path)[0]["do_not_retry"] is None
    assert store.recall("clear metadata")[0].do_not_retry is None


def test_clear_do_not_retry_requires_existing_memory_id(tmp_path):
    store = SubspaceMemoryStore(tmp_path)

    with pytest.raises(ValueError, match="memory_not_found"):
        store.clear_do_not_retry("memory:missing", actor="human")


def test_set_do_not_retry_creates_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Set audit event memory.")

    store.set_do_not_retry(
        memory.id,
        reason="manual reason",
        actor="human",
        alternative="manual alternative",
    )

    event = store.list_audit_events()[-1]
    assert event.event_type == "memory_do_not_retry_set"
    assert event.target_id == memory.id
    assert event.actor == "human"
    assert event.detail == {
        "reason": "manual reason",
        "alternative": "manual alternative",
    }


def test_clear_do_not_retry_creates_audit_event(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Clear audit event memory.")
    set_memory = store.set_do_not_retry(memory.id, reason="manual reason", actor="human")

    store.clear_do_not_retry(memory.id, actor="human", reason="manual clear")

    event = store.list_audit_events()[-1]
    assert event.event_type == "memory_do_not_retry_cleared"
    assert event.target_id == memory.id
    assert event.actor == "human"
    assert event.detail == {
        "previous_do_not_retry": asdict(set_memory.do_not_retry),
        "reason": "manual clear",
    }


def test_set_and_clear_do_not_create_proposal_or_memory_records(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Set and clear rewrites existing memory row.")
    proposals_before = _line_count(tmp_path / "proposals.jsonl")
    memories_before = _line_count(tmp_path / "memories.jsonl")

    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    store.clear_do_not_retry(memory.id, actor="human")

    assert _line_count(tmp_path / "proposals.jsonl") == proposals_before
    assert _line_count(tmp_path / "memories.jsonl") == memories_before


def test_default_recall_includes_do_not_retry_warning_when_active(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Active retry warning recall memory.")
    store.set_do_not_retry(
        memory.id,
        reason="Tried before.",
        actor="human",
        alternative="Use the safe path.",
    )

    result = store.recall("active retry warning")[0]

    assert result.memory_id == memory.id
    assert result.do_not_retry is not None
    assert result.do_not_retry.reason == "Tried before."
    assert result.do_not_retry_warning == (
        "DO NOT RETRY: This memory is marked do-not-retry by human. "
        "Reason: Tried before. Alternative: Use the safe path."
    )


def test_stale_do_not_retry_memory_is_excluded_by_default_lifecycle_rules(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Stale retry warning recall memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    store.set_memory_lifecycle(memory.id, "stale", actor="human")

    assert store.recall("stale retry warning") == []


def test_include_stale_recalls_stale_do_not_retry_memory_with_warning(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Include stale retry warning recall memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    store.set_memory_lifecycle(memory.id, "stale", actor="human")

    result = store.recall("include stale retry", include_stale=True)[0]

    assert result.memory_id == memory.id
    assert result.lifecycle == "stale"
    assert result.do_not_retry is not None
    assert "DO NOT RETRY" in str(result.do_not_retry_warning)


def test_archived_do_not_retry_memory_is_excluded_by_default_lifecycle_rules(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Archived retry warning recall memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    store.set_memory_lifecycle(memory.id, "archived", actor="human")

    assert store.recall("archived retry warning") == []


def test_include_archived_recalls_archived_do_not_retry_memory_with_warning(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Include archived retry warning recall memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    store.set_memory_lifecycle(memory.id, "archived", actor="human")

    result = store.recall("include archived retry", include_archived=True)[0]

    assert result.memory_id == memory.id
    assert result.lifecycle == "archived"
    assert result.do_not_retry is not None
    assert "DO NOT RETRY" in str(result.do_not_retry_warning)


def test_operator_set_command_outputs_deterministic_json_with_do_not_retry(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Operator set do not retry memory.")

    exit_code, payload, stderr = _run_operator(
        [
            "do-not-retry",
            "set",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory.id,
            "--reason",
            "operator reason",
            "--actor",
            "human",
            "--alternative",
            "operator alternative",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["memory_id"] == memory.id
    assert payload["status"] == "approved"
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")
    assert payload["do_not_retry"]["enabled"] is True
    assert payload["do_not_retry"]["reason"] == "operator reason"
    assert payload["do_not_retry"]["actor"] == "human"
    assert payload["do_not_retry"]["alternative"] == "operator alternative"
    assert payload["do_not_retry"]["updated_at"].endswith("Z")


def test_operator_clear_command_outputs_deterministic_json_with_previous_do_not_retry(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Operator clear do not retry memory.")
    set_payload = _run_operator(
        [
            "do-not-retry",
            "set",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory.id,
            "--reason",
            "operator reason",
            "--actor",
            "human",
        ]
    )[1]

    exit_code, payload, stderr = _run_operator(
        [
            "do-not-retry",
            "clear",
            "--workspace-root",
            str(tmp_path),
            "--memory-id",
            memory.id,
            "--actor",
            "human",
            "--reason",
            "operator clear",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload == {
        "do_not_retry": None,
        "memory_id": memory.id,
        "previous_do_not_retry": set_payload["do_not_retry"],
        "status": "approved",
        "storage_root": str(tmp_path / ".local" / "subspace_memory"),
    }


def test_operator_recall_includes_do_not_retry_metadata_and_advisory_warning(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Operator recall retry warning metadata.")
    store.set_do_not_retry(memory.id, reason="operator reason", actor="human")

    exit_code, payload, stderr = _run_operator(
        ["recall", "--workspace-root", str(tmp_path), "--query", "operator recall retry"]
    )

    assert exit_code == 0
    assert stderr == ""
    result = payload["results"][0]
    assert result["memory_id"] == memory.id
    assert result["do_not_retry"]["reason"] == "operator reason"
    assert result["do_not_retry_warning"] == (
        "DO NOT RETRY: This memory is marked do-not-retry by human. Reason: operator reason."
    )


def test_recall_pack_includes_do_not_retry_warning_section(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Recall pack retry warning section memory.")
    store.set_do_not_retry(
        memory.id,
        reason="pack reason",
        actor="human",
        alternative="pack alternative",
    )

    exit_code, pack, stderr = _run_recall_pack(
        ["--workspace-root", str(tmp_path), "--query", "recall pack retry"]
    )

    assert exit_code == 0
    assert stderr == ""
    assert "#### Do-Not-Retry Warning" in pack
    assert "- Enabled: true" in pack
    assert "- Reason: pack reason" in pack
    assert "- Alternative: pack alternative" in pack
    assert "- Actor: human" in pack
    assert "- Advisory: This warning is human-provided context only. It does not automatically block or authorize action." in pack


def test_explainable_trace_remains_present_when_do_not_retry_warning_is_present(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(store, content="Trace remains with retry warning memory.")
    store.set_do_not_retry(memory.id, reason="trace reason", actor="human")

    result = store.recall("trace retry warning")[0]
    exit_code, pack, stderr = _run_recall_pack(
        ["--workspace-root", str(tmp_path), "--query", "trace retry warning"]
    )

    assert result.trace.memory_id == memory.id
    assert result.trace.rank == 1
    assert exit_code == 0
    assert stderr == ""
    assert "#### Do-Not-Retry Warning" in pack
    assert "#### Explainable Trace" in pack
    assert pack.index("#### Do-Not-Retry Warning") < pack.index("#### Explainable Trace")


def test_do_not_retry_recall_warning_generation_is_read_only(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(store, content="Read only retry warning generation memory.")
    store.set_do_not_retry(memory.id, reason="manual reason", actor="human")
    before = _store_files(tmp_path)

    result = store.recall("read only retry")[0]

    assert result.do_not_retry_warning is not None
    assert _store_files(tmp_path) == before


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_do_not_retry_guard():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "do_not_retry" not in entry_points
    assert "p4_m0_subspace_do_not_retry" not in entry_points


def _approved_memory(store: SubspaceMemoryStore, *, content: str):
    proposal = store.propose_memory(
        project="hermes-memory-fabric",
        namespace="do-not-retry",
        content=content,
        source="do-not-retry-test",
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


def _store_files(storage_root: Path) -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted(storage_root.iterdir())
        if path.is_file()
    }
