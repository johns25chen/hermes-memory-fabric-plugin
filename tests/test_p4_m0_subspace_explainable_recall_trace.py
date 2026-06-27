from __future__ import annotations

import io
import json
import tomllib
from dataclasses import asdict
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_recall_pack import run_recall_pack_export
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def test_recall_result_includes_explainable_trace_fields(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    memory = _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="trace",
        content="Recall trace project namespace source lifecycle mechanics.",
        source="trace-test",
    )

    result = store.recall(
        "recall trace project namespace source lifecycle missing",
        project="hermes-memory-fabric",
        namespace="trace",
    )[0]
    trace = result.trace

    assert result.memory_id == memory.id
    assert result.score == 6
    assert result.matched_terms == ("recall", "trace", "project", "namespace", "source", "lifecycle")
    assert trace.query == "recall trace project namespace source lifecycle missing"
    assert trace.query_terms == (
        "recall",
        "trace",
        "project",
        "namespace",
        "source",
        "lifecycle",
        "missing",
    )
    assert trace.matched_terms == result.matched_terms
    assert trace.score == result.score
    assert trace.rank == 1
    assert trace.memory_id == memory.id
    assert trace.project == "hermes-memory-fabric"
    assert trace.namespace == "trace"
    assert trace.source == "trace-test"
    assert trace.lifecycle == "active"
    assert trace.include_stale is False
    assert trace.include_archived is False
    assert trace.explanation == (
        "Matched 6 query terms: recall, trace, project, namespace, source, lifecycle."
    )


def test_trace_rank_is_deterministic_and_starts_at_one(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    first = _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="trace",
        content="Rank trace alpha beta gamma.",
    )
    second = _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="trace",
        content="Rank trace alpha.",
    )

    results = store.recall("rank trace alpha beta gamma", project="hermes-memory-fabric")

    assert [result.memory_id for result in results] == [first.id, second.id]
    assert [result.trace.rank for result in results] == [1, 2]


def test_trace_is_deterministic_for_same_store_and_query(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="trace",
        content="Deterministic trace repeats matched terms.",
    )

    first = [asdict(result.trace) for result in store.recall("deterministic trace matched")]
    second = [asdict(result.trace) for result in store.recall("deterministic trace matched")]

    assert first == second


def test_trace_respects_lifecycle_default_and_include_flags(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    active = _approved_memory(store, project="p", namespace="n", content="Lifecycle trace active memory.")
    stale = _approved_memory(store, project="p", namespace="n", content="Lifecycle trace stale memory.")
    archived = _approved_memory(store, project="p", namespace="n", content="Lifecycle trace archived memory.")
    store.set_memory_lifecycle(stale.id, "stale", actor="human")
    store.set_memory_lifecycle(archived.id, "archived", actor="human")

    default_results = store.recall("lifecycle trace")
    included_results = store.recall("lifecycle trace", include_stale=True, include_archived=True)

    assert [result.memory_id for result in default_results] == [active.id]
    assert default_results[0].trace.lifecycle == "active"
    assert default_results[0].trace.include_stale is False
    assert default_results[0].trace.include_archived is False
    assert {result.memory_id for result in included_results} == {active.id, stale.id, archived.id}
    assert {result.trace.lifecycle for result in included_results} == {"active", "stale", "archived"}
    assert {result.trace.include_stale for result in included_results} == {True}
    assert {result.trace.include_archived for result in included_results} == {True}


def test_operator_recall_includes_trace_metadata(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="operator",
        content="Operator trace metadata source lifecycle.",
        source="operator-trace-test",
    )

    exit_code, payload, stderr = _run_operator(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "operator trace metadata source lifecycle",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    trace = payload["results"][0]["trace"]
    assert trace == {
        "explanation": "Matched 5 query terms: operator, trace, metadata, source, lifecycle.",
        "include_archived": False,
        "include_stale": False,
        "lifecycle": "active",
        "matched_terms": ["operator", "trace", "metadata", "source", "lifecycle"],
        "memory_id": memory.id,
        "namespace": "operator",
        "project": "hermes-memory-fabric",
        "query": "operator trace metadata source lifecycle",
        "query_terms": ["operator", "trace", "metadata", "source", "lifecycle"],
        "rank": 1,
        "score": 5,
        "source": "operator-trace-test",
    }


def test_recall_pack_export_includes_explainable_trace_metadata(tmp_path):
    store = create_workspace_subspace_memory_store(tmp_path)
    memory = _approved_memory(
        store,
        project="hermes-memory-fabric",
        namespace="pack",
        content="Recall pack explainable trace metadata.",
    )

    exit_code, pack, stderr = _run_recall_pack(
        [
            "--workspace-root",
            str(tmp_path),
            "--query",
            "recall pack explainable trace",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "pack",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert f"### 1. {memory.id}" in pack
    assert "#### Explainable Trace" in pack
    assert "- Rank: 1" in pack
    assert "- Query Terms: recall, pack, explainable, trace" in pack
    assert "- Matched Terms: recall, pack, explainable, trace" in pack
    assert "- Include Stale: false" in pack
    assert "- Include Archived: false" in pack
    assert "- Explanation: Matched 4 query terms: recall, pack, explainable, trace." in pack


def test_recall_trace_generation_does_not_create_proposal_memory_or_audit_records(tmp_path):
    store = SubspaceMemoryStore(tmp_path)
    _approved_memory(store, project="p", namespace="n", content="Read only trace recall memory.")
    before = _store_files(tmp_path)

    results = store.recall("read only trace")

    assert len(results) == 1
    assert _store_files(tmp_path) == before


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_explainable_recall_trace():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m0_subspace_explainable_recall_trace" not in entry_points


def _approved_memory(
    store: SubspaceMemoryStore,
    *,
    project: str,
    namespace: str,
    content: str,
    source: str = "trace-test",
):
    proposal = store.propose_memory(
        project=project,
        namespace=namespace,
        content=content,
        source=source,
    )
    return store.approve_proposal(proposal.id, approver="human")


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
