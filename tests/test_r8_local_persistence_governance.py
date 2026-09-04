from __future__ import annotations

# BEGIN CONTRACT_2_2_FROZEN_ORACLE
CONTRACT_VERSION = "2.2.0"
DECISION_SCHEMA = "hermes.local-mutation-decision.v1"
SNAPSHOT_SCHEMA = "hermes.subspace-memory.snapshot.v2"
SNAPSHOT_FILE = "snapshot.json"
LOCK_FILE = ".snapshot.lock"
DECISION_FIELDS = frozenset(
    {
        "schema_version",
        "contract_version",
        "operation",
        "workspace_scope",
        "storage_scope",
        "project",
        "namespace",
        "target",
        "payload_sha256",
        "expected_sequence",
        "decision_id",
        "issued_at",
        "expires_at",
        "audit",
    }
)
AUDIT_FIELDS = frozenset({"actor", "role", "approver"})
MUTATION_RECORD_FIELDS = frozenset(
    {
        "sequence",
        "decision_id",
        "operation",
        "project",
        "namespace",
        "target",
        "payload_sha256",
        "audit_event_sha256",
        "previous_record_sha256",
        "record_sha256",
    }
)
OPERATIONS = (
    "PROPOSE_MEMORY",
    "APPROVE_PROPOSAL",
    "REJECT_PROPOSAL",
    "SET_MEMORY_LIFECYCLE",
    "SET_DO_NOT_RETRY",
    "CLEAR_DO_NOT_RETRY",
)
PAYLOAD_FIELDS = {
    "PROPOSE_MEMORY": ("project", "namespace", "content", "source", "tags", "confidence"),
    "APPROVE_PROPOSAL": ("proposal_id", "approver", "note"),
    "REJECT_PROPOSAL": ("proposal_id", "reviewer", "reason"),
    "SET_MEMORY_LIFECYCLE": ("memory_id", "lifecycle", "actor", "reason"),
    "SET_DO_NOT_RETRY": ("memory_id", "reason", "actor", "alternative"),
    "CLEAR_DO_NOT_RETRY": ("memory_id", "actor", "reason"),
}
TARGET_RULES = {
    "PROPOSE_MEMORY": "proposal:<sha256(canonical logical payload)[:32]>",
    "APPROVE_PROPOSAL": "proposal_id",
    "REJECT_PROPOSAL": "proposal_id",
    "SET_MEMORY_LIFECYCLE": "memory_id",
    "SET_DO_NOT_RETRY": "memory_id",
    "CLEAR_DO_NOT_RETRY": "memory_id",
}
PROTOCOL = {
    "decision_json": {
        "encoding": "UTF-8 without BOM",
        "object_only": True,
        "duplicate_keys": "reject",
        "non_finite_numbers": "reject",
        "unknown_fields": "reject",
        "scalar_types": "exact bool/int/float/string/null; bool is not int",
    },
    "canonicalization": {
        "algorithm": "json.dumps(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)",
        "preserve_business_strings": True,
        "preserve_unicode": True,
        "preserve_case": True,
        "preserve_string_whitespace": True,
        "preserve_array_order": True,
        "digest_input": "independently constructed normalized logical mutation payload",
    },
    "scope": {
        "workspace_scope": "absolute lexical workspace root supplied to the trusted store factory",
        "storage_scope": "absolute lexical storage root confined below workspace_scope",
    },
    "time": {
        "format": "RFC3339 UTC YYYY-MM-DDTHH:MM:SSZ",
        "clock_tolerance_seconds": 0,
        "valid_when": "issued_at <= injected_utc_now < expires_at",
        "clock_injection": "SubspaceMemoryStore(clock=callable returning aware UTC datetime)",
        "lock_timeout_seconds": 5.0,
        "lock_clock": "single monotonic deadline with non-blocking lock attempts",
    },
    "limits": {
        "decision_utf8_bytes": 16384,
        "identifier_chars": 256,
        "scope_chars": 4096,
        "audit_value_chars": 256,
        "business_string_chars": 65536,
        "tags_count": 128,
        "snapshot_utf8_bytes": 16777216,
        "proposals_count": 10000,
        "memories_count": 10000,
        "audit_events_count": 50000,
        "consumed_decision_ids_count": 50000,
        "mutation_records_count": 50000,
    },
    "snapshot": {
        "required_fields": (
            "schema_version",
            "contract_version",
            "sequence",
            "consumed_decision_ids",
            "proposals",
            "memories",
            "audit_events",
            "mutation_records",
            "previous_snapshot_sha256",
            "last_mutation",
            "snapshot_sha256",
        ),
        "sequence_initial": 0,
        "consumed_decisions_location": "top-level consumed_decision_ids array",
        "digest_coverage": "canonical full snapshot excluding snapshot_sha256",
        "previous_provenance": "commit binds previous_snapshot_sha256 to the locked prior snapshot digest; restart does not prove prior snapshot bytes",
        "mutation_record_digest": "sha256(canonical mutation record excluding record_sha256)",
        "mutation_record_chain": "first previous_record_sha256 is 64 zeroes; each later value equals the prior record_sha256",
        "read_integrity": "validate current snapshot, saved relationships, record chain, and sequential business transitions without hashing historical snapshot prefixes",
        "c22_i007": "current structure semantics digest and saved mutation relationships are validated; historical snapshot bytes are not re-proved after restart",
    },
}
ERROR_CODES = (
    "BLOCK_DECISION_REQUIRED_OR_MALFORMED",
    "BLOCK_DECISION_BINDING_MISMATCH",
    "BLOCK_DECISION_TIME_INVALID",
    "BLOCK_STALE_SEQUENCE",
    "BLOCK_DECISION_REPLAY",
    "BLOCK_PATH_CONFINEMENT",
    "BLOCK_SNAPSHOT_INTEGRITY",
    "BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT",
    "BLOCK_SNAPSHOT_VERSION_UNSUPPORTED",
    "BLOCK_LOCK_TIMEOUT",
    "WRITE_ABORTED_PRECOMMIT",
    "COMMIT_DURABILITY_UNCERTAIN_RECONCILE_REQUIRED",
)
RECEIPT_FIELDS = frozenset(
    {
        "contract_version",
        "operation",
        "decision_id",
        "workspace_scope",
        "storage_scope",
        "project",
        "namespace",
        "target",
        "payload_sha256",
        "previous_sequence",
        "committed_sequence",
        "previous_snapshot_sha256",
        "committed_snapshot_sha256",
        "operator_identity_authenticated",
        "decision_schema_validated",
        "decision_scope_bound",
        "decision_replay_protected",
        "commit_status",
    }
)
CASE_ORACLES = {
    "MD01": "constructor and factory perform zero filesystem mutation",
    "MD02": "missing decision blocks before filesystem mutation",
    "MD03": "malformed decision blocks before filesystem mutation",
    "MD04": "duplicate JSON key blocks before filesystem mutation",
    "MD05": "missing or unknown decision field blocks",
    "MD06": "wrong contract version blocks",
    "MD07": "wrong operation blocks",
    "MD08": "wrong workspace scope blocks",
    "MD09": "wrong storage scope blocks",
    "MD10": "wrong project or namespace blocks",
    "MD11": "wrong target blocks",
    "MD12": "modified payload or digest mismatch blocks",
    "MD13": "expired decision blocks",
    "MD14": "not-yet-valid decision blocks",
    "MD15": "stale expected sequence blocks",
    "MD16": "consumed decision id replay blocks",
    "MD17": "valid decision commits once and increments sequence once",
    "MD18": "receipt never claims operator identity authentication",
    "PATH01": "workspace symlink blocks",
    "PATH02": "absolute or parent traversal storage path blocks",
    "PATH03": "storage symlink blocks",
    "PATH04": "non-regular snapshot blocks",
    "PATH05": "pre-commit path identity change blocks",
    "ATOM01": "write failure preserves prior snapshot and decision",
    "ATOM02": "file fsync failure preserves prior snapshot and decision",
    "ATOM03": "read-back mismatch preserves prior snapshot and decision",
    "ATOM04": "replace failure preserves prior snapshot and decision",
    "ATOM05": "success uses write fsync read-back replace directory-fsync order",
    "ATOM06": "directory fsync failure reports durability uncertain",
    "ATOM07": "read-only reconcile identifies committed state without retry",
    "ATOM08": "same-sequence competition permits one commit",
    "INT01": "top-level digest tamper blocks",
    "INT02": "rehashed semantic tamper blocks",
    "INT03": "saved decision audit payload and record-chain tamper blocks; prior snapshot bytes are commit-time provenance only",
    "INT04": "resource limit excess blocks",
    "INT05": "legacy or mixed snapshot blocks",
    "CLI01": "invalid CLI decision blocks with zero store mutation",
    "CLI02": "valid CLI decision invokes one mutation and exposes no mint API",
    "REG01": "propose approve reject recall behavior remains correct",
    "REG02": "lifecycle do-not-retry seed and workspace behavior remains correct",
}
# END CONTRACT_2_2_FROZEN_ORACLE

import hashlib
import fcntl
import io
import json
import errno
import os
import stat
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

import pytest

from hermes_memory_fabric.p4_m0_subspace_memory import SubspaceMemoryStore
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store
import hermes_memory_fabric.r8_local_persistence_governance as governance_module
from hermes_memory_fabric.r8_local_persistence_governance import (
    GovernanceError,
    canonical_json,
)


NOW = datetime(2026, 8, 31, 0, 0, 0, tzinfo=UTC)
PROPOSE_PAYLOAD = {
    "project": "project",
    "namespace": "namespace",
    "content": "payload text",
    "source": "local",
    "tags": [],
    "confidence": 1.0,
}


def _store(tmp_path):
    return SubspaceMemoryStore(tmp_path, clock=lambda: NOW)


def _independent_sha256(value):
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _independent_target(payload):
    return f"proposal:{_independent_sha256(payload)[:32]}"


def _independent_record_sha256(record):
    return _independent_sha256(
        {key: value for key, value in record.items() if key != "record_sha256"}
    )


def _rehash_snapshot(snapshot):
    snapshot["snapshot_sha256"] = _independent_sha256(
        {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    )


def _decision(store, operation, payload, target, *, sequence, decision_id="decision-1", **changes):
    value = {
        "schema_version": DECISION_SCHEMA,
        "contract_version": CONTRACT_VERSION,
        "operation": operation,
        "workspace_scope": str(store._governance.workspace_root),
        "storage_scope": str(store.storage_root),
        "project": changes.pop("project", payload.get("project", "project")),
        "namespace": changes.pop("namespace", payload.get("namespace", "namespace")),
        "target": target,
        "payload_sha256": _independent_sha256(payload),
        "expected_sequence": sequence,
        "decision_id": decision_id,
        "issued_at": "2026-08-30T23:59:00Z",
        "expires_at": "2026-08-31T00:01:00Z",
        "audit": {"actor": "test-operator"},
    }
    value.update(changes)
    return value


def _propose(store, *, sequence, decision_id="decision-1", payload=PROPOSE_PAYLOAD):
    decision = _decision(
        store,
        "PROPOSE_MEMORY",
        payload,
        _independent_target(payload),
        sequence=sequence,
        decision_id=decision_id,
    )
    return store.propose_memory(**payload, decision=decision)


def _expect_block(store, decision, code):
    before = list(store.storage_root.parent.iterdir()) if store.storage_root.parent.exists() else []
    with pytest.raises(GovernanceError, match=code):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
    after = list(store.storage_root.parent.iterdir()) if store.storage_root.parent.exists() else []
    assert after == before


@pytest.mark.parametrize(
    ("scenario", "expected"),
    [
        pytest.param("constructor", "no-write", id="md01"),
        pytest.param("missing", "BLOCK_DECISION_REQUIRED_OR_MALFORMED", id="md02"),
        pytest.param("malformed", "BLOCK_DECISION_REQUIRED_OR_MALFORMED", id="md03"),
        pytest.param("duplicate", "BLOCK_DECISION_REQUIRED_OR_MALFORMED", id="md04"),
        pytest.param("field-set", "BLOCK_DECISION_REQUIRED_OR_MALFORMED", id="md05"),
        pytest.param("contract", "BLOCK_DECISION_BINDING_MISMATCH", id="md06"),
        pytest.param("operation", "BLOCK_DECISION_BINDING_MISMATCH", id="md07"),
        pytest.param("workspace", "BLOCK_DECISION_BINDING_MISMATCH", id="md08"),
        pytest.param("storage", "BLOCK_DECISION_BINDING_MISMATCH", id="md09"),
        pytest.param("project-namespace", "BLOCK_DECISION_BINDING_MISMATCH", id="md10"),
        pytest.param("target", "BLOCK_DECISION_BINDING_MISMATCH", id="md11"),
        pytest.param("payload", "BLOCK_DECISION_BINDING_MISMATCH", id="md12"),
        pytest.param("expired", "BLOCK_DECISION_TIME_INVALID", id="md13"),
        pytest.param("future", "BLOCK_DECISION_TIME_INVALID", id="md14"),
        pytest.param("stale", "BLOCK_STALE_SEQUENCE", id="md15"),
        pytest.param("replay", "BLOCK_DECISION_REPLAY", id="md16"),
        pytest.param("valid", "committed", id="md17"),
        pytest.param("receipt", "identity-false", id="md18"),
    ],
)
def test_contract_2_1_decision_cases(tmp_path, scenario, expected):
    root = tmp_path / "store"
    store = _store(root)
    if scenario == "constructor":
        assert not root.exists()
        return
    if scenario == "missing":
        decision = None
    elif scenario == "malformed":
        decision = "{"
    elif scenario == "duplicate":
        decision = '{"schema_version":"a","schema_version":"b"}'
    else:
        decision = _decision(store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0)
        changes = {
            "field-set": ("extra", True), "contract": ("contract_version", "2.0.0"),
            "operation": ("operation", "APPROVE_PROPOSAL"), "workspace": ("workspace_scope", "/wrong"),
            "storage": ("storage_scope", "/wrong"), "project-namespace": ("project", "wrong"),
            "target": ("target", "proposal:wrong"), "payload": ("payload_sha256", "0" * 64),
            "expired": ("expires_at", "2026-08-31T00:00:00Z"),
            "future": ("issued_at", "2026-08-31T00:00:01Z"), "stale": ("expected_sequence", 1),
        }
        if scenario in changes:
            key, value = changes[scenario]
            decision[key] = value
    if scenario in {"valid", "receipt"}:
        proposal = store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
        assert proposal.id == _independent_target(PROPOSE_PAYLOAD)
        assert store.current_sequence == 1
        assert store.last_receipt is not None
        assert store.last_receipt.operator_identity_authenticated is False
        return
    if scenario == "replay":
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
        with pytest.raises(GovernanceError, match=expected):
            store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
        return
    with pytest.raises(GovernanceError, match=expected):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)


@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param("workspace-symlink", id="path01"), pytest.param("escape", id="path02"),
        pytest.param("storage-symlink", id="path03"), pytest.param("non-regular", id="path04"),
        pytest.param("identity-change", id="path05"),
    ],
)
def test_contract_2_1_path_cases(tmp_path, monkeypatch, scenario):
    if scenario == "escape":
        with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
            SubspaceMemoryStore(tmp_path / "outside", workspace_root=tmp_path / "workspace")
        return
    real = tmp_path / "real"
    real.mkdir()
    root = tmp_path / "store"
    if scenario in {"workspace-symlink", "storage-symlink"}:
        root.symlink_to(real, target_is_directory=True)
        store = _store(root)
    else:
        store = _store(root)
        decision = _decision(store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0)
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
        if scenario == "non-regular":
            store._governance.snapshot_path.unlink()
            store._governance.snapshot_path.mkdir()
        else:
            before = store._governance.snapshot_path.read_bytes()
            moved = tmp_path / "moved"
            calls = 0
            original_assert = store._governance._assert_storage_identity

            def replace_parent_before_final_identity_check(directory_fd, expected):
                nonlocal calls
                calls += 1
                if calls == 2:
                    root.rename(moved)
                    root.symlink_to(real, target_is_directory=True)
                return original_assert(directory_fd, expected)

            monkeypatch.setattr(
                store._governance,
                "_assert_storage_identity",
                replace_parent_before_final_identity_check,
            )
            payload = {**PROPOSE_PAYLOAD, "content": "second payload"}
            second = _decision(
                store,
                "PROPOSE_MEMORY",
                payload,
                _independent_target(payload),
                sequence=1,
                decision_id="decision-2",
            )
            with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
                store.propose_memory(**payload, decision=second)
            assert (moved / SNAPSHOT_FILE).read_bytes() == before
            assert not (real / SNAPSHOT_FILE).exists()
            assert not list(moved.glob(".snapshot.*.stage"))
            return
    with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
        store.read_snapshot() if hasattr(store, "read_snapshot") else store._governance.read_snapshot()


@pytest.mark.parametrize(
    "stage",
    [
        pytest.param("write", id="atom01"), pytest.param("file-fsync", id="atom02"),
        pytest.param("read-back", id="atom03"), pytest.param("replace", id="atom04"),
        pytest.param("success-order", id="atom05"), pytest.param("directory-fsync", id="atom06"),
        pytest.param("reconcile", id="atom07"), pytest.param("competition", id="atom08"),
    ],
)
def test_contract_2_1_atomic_cases(tmp_path, monkeypatch, stage):
    root = tmp_path / "store"
    if stage == "competition":
        root.mkdir()
        (root / LOCK_FILE).write_bytes(b"")
        barrier = threading.Barrier(2)
        payloads = [
            {**PROPOSE_PAYLOAD, "content": "competitor one"},
            {**PROPOSE_PAYLOAD, "content": "competitor two"},
        ]
        stores = [_store(root), _store(root)]
        decisions = [
            _decision(
                stores[index],
                "PROPOSE_MEMORY",
                payload,
                _independent_target(payload),
                sequence=0,
                decision_id=f"competition-{index}",
            )
            for index, payload in enumerate(payloads)
        ]

        def compete(index):
            barrier.wait(timeout=5)
            try:
                stores[index].propose_memory(**payloads[index], decision=decisions[index])
                return "committed"
            except GovernanceError as exc:
                return exc.code

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(compete, index) for index in range(2)]
            outcomes = [future.result(timeout=10) for future in futures]
        assert outcomes.count("committed") == 1
        assert outcomes.count("BLOCK_STALE_SEQUENCE") == 1
        final = _store(root)._governance.read_snapshot()
        assert final["sequence"] == 1
        assert len(final["consumed_decision_ids"]) == 1
        return

    store = _store(root)
    _propose(store, sequence=0)
    if stage == "reconcile":
        reopened = _store(root)
        monkeypatch.setattr(
            governance_module.os,
            "replace",
            lambda *args, **kwargs: pytest.fail("reconcile must not replace"),
        )
        assert reopened._governance.reconcile("decision-1") == {
            "sequence": 1,
            "decision_consumed": True,
            "snapshot_sha256": reopened._governance.read_snapshot()["snapshot_sha256"],
        }
        return

    payload = {**PROPOSE_PAYLOAD, "content": f"atomic {stage}"}
    decision = _decision(
        store,
        "PROPOSE_MEMORY",
        payload,
        _independent_target(payload),
        sequence=1,
        decision_id=f"decision-{stage}",
    )
    before = store._governance.snapshot_path.read_bytes()
    original_write = governance_module.os.write
    original_read = governance_module.os.read
    original_fsync = governance_module.os.fsync
    original_replace = governance_module.os.replace
    stage_fds = set()
    order = []

    if stage == "write":
        monkeypatch.setattr(governance_module.os, "write", lambda *args: (_ for _ in ()).throw(OSError("write fault")))
    elif stage == "file-fsync":
        monkeypatch.setattr(governance_module.os, "fsync", lambda *args: (_ for _ in ()).throw(OSError("file fsync fault")))
    elif stage == "read-back":
        read_calls = 0

        def mismatching_read(fd, size):
            nonlocal read_calls
            read_calls += 1
            if read_calls == 3:
                return b""
            return original_read(fd, size)

        monkeypatch.setattr(governance_module.os, "read", mismatching_read)
    elif stage == "replace":
        monkeypatch.setattr(governance_module.os, "replace", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("replace fault")))
    elif stage == "directory-fsync":
        def fail_directory_fsync(fd):
            if stat.S_ISDIR(os.fstat(fd).st_mode):
                raise OSError("directory fsync fault")
            return original_fsync(fd)

        monkeypatch.setattr(governance_module.os, "fsync", fail_directory_fsync)
    elif stage == "success-order":
        original_open = governance_module.os.open

        def observed_open(path, flags, *args, **kwargs):
            fd = original_open(path, flags, *args, **kwargs)
            if isinstance(path, str) and path.startswith(".snapshot.") and path.endswith(".stage"):
                stage_fds.add(fd)
            return fd

        def observed_write(fd, data):
            if fd in stage_fds and "write" not in order:
                order.append("write")
            return original_write(fd, data)

        def observed_fsync(fd):
            if fd in stage_fds:
                order.append("file-fsync")
            elif stat.S_ISDIR(os.fstat(fd).st_mode):
                order.append("directory-fsync")
            return original_fsync(fd)

        def observed_read(fd, size):
            if fd in stage_fds and "read-back" not in order:
                order.append("read-back")
            return original_read(fd, size)

        def observed_replace(*args, **kwargs):
            order.append("replace")
            return original_replace(*args, **kwargs)

        monkeypatch.setattr(governance_module.os, "open", observed_open)
        monkeypatch.setattr(governance_module.os, "write", observed_write)
        monkeypatch.setattr(governance_module.os, "fsync", observed_fsync)
        monkeypatch.setattr(governance_module.os, "read", observed_read)
        monkeypatch.setattr(governance_module.os, "replace", observed_replace)

    if stage == "directory-fsync":
        with pytest.raises(GovernanceError, match="COMMIT_DURABILITY_UNCERTAIN_RECONCILE_REQUIRED"):
            store.propose_memory(**payload, decision=decision)
        reconciled = store._governance.reconcile(f"decision-{stage}")
        assert reconciled["decision_consumed"] is True
        assert reconciled["sequence"] == 2
        assert store.last_receipt is not None
        assert store.last_receipt.decision_id == "decision-1"
        return
    if stage == "success-order":
        store.propose_memory(**payload, decision=decision)
        assert order == ["write", "file-fsync", "read-back", "replace", "directory-fsync"]
        return
    with pytest.raises(GovernanceError, match="WRITE_ABORTED_PRECOMMIT"):
        store.propose_memory(**payload, decision=decision)
    assert store._governance.snapshot_path.read_bytes() == before
    assert store._governance.reconcile(f"decision-{stage}")["decision_consumed"] is False
    assert not list(root.glob(".snapshot.*.stage"))


@pytest.mark.parametrize(
    "scenario",
    [
        pytest.param("digest", id="int01"), pytest.param("semantic", id="int02"),
        pytest.param("provenance", id="int03"), pytest.param("limit", id="int04"),
        pytest.param("legacy", id="int05"),
    ],
)
def test_contract_2_1_integrity_cases(tmp_path, scenario):
    store = _store(tmp_path / "store")
    _propose(store, sequence=0)
    path = store._governance.snapshot_path
    value = json.loads(path.read_text(encoding="utf-8"))
    if scenario == "digest":
        value["snapshot_sha256"] = "0" * 64
    elif scenario == "semantic":
        value["proposals"][0]["confidence"] = "1.0"
    elif scenario == "provenance":
        value["last_mutation"]["decision_id"] = "unconsumed-decision"
    elif scenario == "limit":
        value["consumed_decision_ids"] = [f"decision-{index}" for index in range(50001)]
        value["sequence"] = len(value["consumed_decision_ids"])
    else:
        value["schema_version"] = "legacy"
    if scenario != "digest":
        value["snapshot_sha256"] = _independent_sha256(
            {key: item for key, item in value.items() if key != "snapshot_sha256"}
        )
    path.write_text(canonical_json(value) + "\n", encoding="utf-8")
    expected = "BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT" if scenario == "limit" else "BLOCK_SNAPSHOT_INTEGRITY"
    with pytest.raises(GovernanceError, match=expected):
        store._governance.read_snapshot()


@pytest.mark.parametrize("valid", [pytest.param(False, id="cli01"), pytest.param(True, id="cli02")])
def test_contract_2_1_cli_cases(tmp_path, valid):
    from hermes_memory_fabric.p4_m0_subspace_operator import build_parser
    parser = build_parser()
    command_names = set()
    pending = [parser]
    while pending:
        current = pending.pop()
        for action in current._actions:
            choices = getattr(action, "choices", None)
            if isinstance(choices, dict):
                command_names.update(choices)
                pending.extend(choices.values())
    assert command_names.isdisjoint({"mint", "sign", "attest"})
    storage = tmp_path / ".local" / "subspace_memory"
    decision_store = SubspaceMemoryStore(storage, workspace_root=tmp_path, clock=lambda: NOW)
    decision = _decision(
        decision_store,
        "PROPOSE_MEMORY",
        PROPOSE_PAYLOAD,
        _independent_target(PROPOSE_PAYLOAD),
        sequence=0,
        issued_at="2000-01-01T00:00:00Z",
        expires_at="2999-01-01T00:00:00Z",
    )
    stdout = io.StringIO()
    stderr = io.StringIO()
    argv = [
        "propose", "--workspace-root", str(tmp_path), "--project", "project",
        "--namespace", "namespace", "--content", "payload text", "--source", "local",
        "--confidence", "1.0", "--mutation-decision-json",
        json.dumps(decision) if valid else "{}",
    ]
    code = run_operator_command(argv, stdout=stdout, stderr=stderr)
    if not valid:
        assert code == 2
        assert json.loads(stderr.getvalue()) == {
            "code": "BLOCK_DECISION_REQUIRED_OR_MALFORMED",
            "disposition": "BLOCK",
        }
        assert stdout.getvalue() == ""
        assert not (tmp_path / ".local").exists()
        return
    assert code == 0
    assert stderr.getvalue() == ""
    result = json.loads(stdout.getvalue())
    assert result["proposal_id"] == _independent_target(PROPOSE_PAYLOAD)
    assert (storage / SNAPSHOT_FILE).is_file()


@pytest.mark.parametrize("flow", [pytest.param("proposal", id="reg01"), pytest.param("workspace", id="reg02")])
def test_contract_2_1_regression_cases(tmp_path, flow):
    if flow == "proposal":
        store = _store(tmp_path / "store")
        approved_proposal = _propose(store, sequence=0, decision_id="reg-propose-approved")
        approve_payload = {"proposal_id": approved_proposal.id, "approver": "human", "note": "approved"}
        approved = store.approve_proposal(
            approved_proposal.id,
            approver="human",
            note="approved",
            decision=_decision(
                store, "APPROVE_PROPOSAL", approve_payload, approved_proposal.id,
                sequence=1, decision_id="reg-approve", project=approved_proposal.project,
                namespace=approved_proposal.namespace,
            ),
        )
        rejected_payload = {**PROPOSE_PAYLOAD, "content": "rejected unique phrase"}
        rejected_proposal = _propose(
            store, sequence=2, decision_id="reg-propose-rejected", payload=rejected_payload
        )
        reject_payload = {"proposal_id": rejected_proposal.id, "reviewer": "human", "reason": "reject"}
        rejected = store.reject_proposal(
            rejected_proposal.id,
            reviewer="human",
            reason="reject",
            decision=_decision(
                store, "REJECT_PROPOSAL", reject_payload, rejected_proposal.id,
                sequence=3, decision_id="reg-reject", project=rejected_proposal.project,
                namespace=rejected_proposal.namespace,
            ),
        )
        assert rejected.status == "rejected"
        assert [result.memory_id for result in store.recall("payload")] == [approved.id]
        assert store.recall("rejected") == []
        assert store.current_sequence == 4
        return

    store = create_workspace_subspace_memory_store(tmp_path)
    payload = {**PROPOSE_PAYLOAD, "content": "restart lifecycle memory"}
    common_time = {"issued_at": "2000-01-01T00:00:00Z", "expires_at": "2999-01-01T00:00:00Z"}
    proposal = store.propose_memory(
        **payload,
        decision=_decision(
            store, "PROPOSE_MEMORY", payload, _independent_target(payload),
            sequence=0, decision_id="workspace-propose", **common_time,
        ),
    )
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id,
        approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="workspace-approve", project=proposal.project,
            namespace=proposal.namespace, **common_time,
        ),
    )
    lifecycle_payload = {"memory_id": memory.id, "lifecycle": "archived", "actor": "human", "reason": "retired"}
    store.set_memory_lifecycle(
        memory.id, "archived", actor="human", reason="retired",
        decision=_decision(
            store, "SET_MEMORY_LIFECYCLE", lifecycle_payload, memory.id, sequence=2,
            decision_id="workspace-lifecycle", project=memory.project,
            namespace=memory.namespace, **common_time,
        ),
    )
    set_payload = {"memory_id": memory.id, "reason": "unsafe", "actor": "human", "alternative": "inspect"}
    store.set_do_not_retry(
        memory.id, reason="unsafe", actor="human", alternative="inspect",
        decision=_decision(
            store, "SET_DO_NOT_RETRY", set_payload, memory.id, sequence=3,
            decision_id="workspace-set-dnr", project=memory.project,
            namespace=memory.namespace, **common_time,
        ),
    )
    clear_payload = {"memory_id": memory.id, "actor": "human", "reason": "resolved"}
    store.clear_do_not_retry(
        memory.id, actor="human", reason="resolved",
        decision=_decision(
            store, "CLEAR_DO_NOT_RETRY", clear_payload, memory.id, sequence=4,
            decision_id="workspace-clear-dnr", project=memory.project,
            namespace=memory.namespace, **common_time,
        ),
    )
    reopened = create_workspace_subspace_memory_store(tmp_path)
    results = reopened.recall("restart", include_archived=True)
    assert len(results) == 1
    assert results[0].lifecycle == "archived"
    assert results[0].do_not_retry is None
    assert reopened.current_sequence == 5


def test_lock_symlink_is_rejected_before_snapshot_io(tmp_path):
    root = tmp_path / "store"
    root.mkdir()
    attack_target = tmp_path / "attack.lock"
    attack_target.write_bytes(b"unchanged")
    (root / LOCK_FILE).symlink_to(attack_target)
    store = _store(root)
    decision = _decision(
        store,
        "PROPOSE_MEMORY",
        PROPOSE_PAYLOAD,
        _independent_target(PROPOSE_PAYLOAD),
        sequence=0,
    )

    with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)

    assert attack_target.read_bytes() == b"unchanged"
    assert not (root / SNAPSHOT_FILE).exists()


def test_non_regular_lock_rejection_closes_opened_lock_fd(tmp_path, monkeypatch):
    root = tmp_path / "store"
    root.mkdir()
    os.mkfifo(root / LOCK_FILE)
    store = _store(root)
    decision = _decision(
        store,
        "PROPOSE_MEMORY",
        PROPOSE_PAYLOAD,
        _independent_target(PROPOSE_PAYLOAD),
        sequence=0,
    )
    original_open = os.open
    opened_lock_fds = []

    def capture_lock_fd(path, flags, *args, **kwargs):
        fd = original_open(path, flags, *args, **kwargs)
        if path == LOCK_FILE:
            opened_lock_fds.append(fd)
        return fd

    monkeypatch.setattr(governance_module.os, "open", capture_lock_fd)

    with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)

    assert len(opened_lock_fds) == 1
    with pytest.raises(OSError) as closed:
        os.fstat(opened_lock_fds[0])
    assert closed.value.errno == errno.EBADF
    assert not (root / SNAPSHOT_FILE).exists()
    assert store._governance.reconcile("decision-1")["decision_consumed"] is False


def test_rehashed_nested_proposal_type_tamper_is_rejected(tmp_path):
    store = _store(tmp_path / "store")
    _propose(store, sequence=0)
    path = store._governance.snapshot_path
    value = json.loads(path.read_text(encoding="utf-8"))
    value["proposals"][0]["confidence"] = "1.0"
    value["snapshot_sha256"] = hashlib.sha256(
        canonical_json({key: item for key, item in value.items() if key != "snapshot_sha256"}).encode("utf-8")
    ).hexdigest()
    path.write_text(canonical_json(value) + "\n", encoding="utf-8")

    with pytest.raises(GovernanceError, match="BLOCK_SNAPSHOT_INTEGRITY"):
        store._governance.read_snapshot()


def test_propose_decision_binds_and_preserves_raw_business_strings_and_tag_order(tmp_path):
    store = _store(tmp_path / "store")
    payload = {
        "project": "project",
        "namespace": "namespace",
        "content": "  Payload \N{SNOWMAN}  ",
        "source": " Local ",
        "tags": ["z", "a", "z"],
        "confidence": 1.0,
    }
    decision = _decision(
        store,
        "PROPOSE_MEMORY",
        payload,
        _independent_target(payload),
        sequence=0,
    )

    proposal = store.propose_memory(**payload, decision=decision)

    assert proposal.content == payload["content"]
    assert proposal.source == payload["source"]
    assert proposal.tags == tuple(payload["tags"])


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        pytest.param("content", 123, "content_must_be_non_empty", id="content-type"),
        pytest.param("source", True, "source_must_be_non_empty", id="source-type"),
        pytest.param("tags", ["tag"] * 129, "tags_exceed_count_limit", id="tags-count"),
        pytest.param("tags", ["valid", 1], "tag_must_be_non_empty_string", id="tag-type"),
        pytest.param("confidence", True, "confidence_must_be_finite_number", id="confidence-bool"),
        pytest.param("confidence", "1.0", "confidence_must_be_finite_number", id="confidence-string"),
        pytest.param("content", "x" * 65537, "content_exceeds_character_limit", id="business-string-limit"),
    ],
)
def test_invalid_business_types_and_limits_fail_before_filesystem_mutation(tmp_path, field, value, message):
    root = tmp_path / "store"
    payload = {**PROPOSE_PAYLOAD, field: value}
    store = _store(root)

    with pytest.raises(ValueError, match=message):
        store.propose_memory(**payload, decision={})

    assert not root.exists()


def test_contract_limits_accept_exact_business_and_tag_boundaries(tmp_path):
    store = _store(tmp_path / "store")
    payload = {
        **PROPOSE_PAYLOAD,
        "content": "x" * 65536,
        "tags": [f"tag-{index}" for index in range(128)],
    }
    decision = _decision(
        store, "PROPOSE_MEMORY", payload, _independent_target(payload), sequence=0,
        decision_id="boundary-decision",
    )

    proposal = store.propose_memory(**payload, decision=decision)

    assert len(proposal.content) == 65536
    assert len(proposal.tags) == 128


@pytest.mark.parametrize(
    "operation",
    [
        "PROPOSE_MEMORY", "APPROVE_PROPOSAL", "REJECT_PROPOSAL",
        "SET_MEMORY_LIFECYCLE", "SET_DO_NOT_RETRY", "CLEAR_DO_NOT_RETRY",
    ],
)
def test_all_six_mutations_reject_explicit_empty_decision_without_test_minting(tmp_path, operation):
    store = _store(tmp_path / "store")
    if operation == "PROPOSE_MEMORY":
        before = list(tmp_path.iterdir())
        with pytest.raises(GovernanceError, match="BLOCK_DECISION_REQUIRED_OR_MALFORMED"):
            store.propose_memory(**PROPOSE_PAYLOAD, decision={})
        assert list(tmp_path.iterdir()) == before
        return

    proposal = _propose(store, sequence=0, decision_id="setup-propose")
    if operation in {"APPROVE_PROPOSAL", "REJECT_PROPOSAL"}:
        before = store._governance.snapshot_path.read_bytes()
        if operation == "APPROVE_PROPOSAL":
            call = lambda: store.approve_proposal(proposal.id, approver="human", decision={})
        else:
            call = lambda: store.reject_proposal(
                proposal.id, reviewer="human", reason="reject", decision={}
            )
        with pytest.raises(GovernanceError, match="BLOCK_DECISION_REQUIRED_OR_MALFORMED"):
            call()
        assert store._governance.snapshot_path.read_bytes() == before
        return

    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="setup-approve", project=proposal.project, namespace=proposal.namespace,
        ),
    )
    if operation == "CLEAR_DO_NOT_RETRY":
        set_payload = {"memory_id": memory.id, "reason": "guard", "actor": "human", "alternative": None}
        memory = store.set_do_not_retry(
            memory.id, reason="guard", actor="human",
            decision=_decision(
                store, "SET_DO_NOT_RETRY", set_payload, memory.id, sequence=2,
                decision_id="setup-dnr", project=memory.project, namespace=memory.namespace,
            ),
        )
    before = store._governance.snapshot_path.read_bytes()
    calls = {
        "SET_MEMORY_LIFECYCLE": lambda: store.set_memory_lifecycle(
            memory.id, "stale", actor="human", decision={}
        ),
        "SET_DO_NOT_RETRY": lambda: store.set_do_not_retry(
            memory.id, reason="guard", actor="human", decision={}
        ),
        "CLEAR_DO_NOT_RETRY": lambda: store.clear_do_not_retry(
            memory.id, actor="human", decision={}
        ),
    }
    with pytest.raises(GovernanceError, match="BLOCK_DECISION_REQUIRED_OR_MALFORMED"):
        calls[operation]()
    assert store._governance.snapshot_path.read_bytes() == before


def test_receipt_fields_are_linked_to_the_committed_snapshot(tmp_path):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="receipt-decision")
    snapshot = store._governance.read_snapshot()
    receipt = store.last_receipt

    assert receipt is not None
    assert receipt.operation == "PROPOSE_MEMORY"
    assert receipt.decision_id == snapshot["last_mutation"]["decision_id"]
    assert receipt.payload_sha256 == snapshot["last_mutation"]["payload_sha256"]
    assert receipt.committed_sequence == snapshot["sequence"]
    assert receipt.committed_snapshot_sha256 == snapshot["snapshot_sha256"]
    assert receipt.previous_snapshot_sha256 == snapshot["previous_snapshot_sha256"]
    assert receipt.target == proposal.id
    assert receipt.operator_identity_authenticated is False


def test_clear_do_not_retry_without_existing_warning_remains_a_valid_mutation(tmp_path):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="clear-empty-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id,
        approver="human",
        decision=_decision(
            store,
            "APPROVE_PROPOSAL",
            approve_payload,
            proposal.id,
            sequence=1,
            decision_id="clear-empty-approve",
            project=proposal.project,
            namespace=proposal.namespace,
        ),
    )
    clear_payload = {"memory_id": memory.id, "actor": "human", "reason": None}

    cleared = store.clear_do_not_retry(
        memory.id,
        actor="human",
        decision=_decision(
            store,
            "CLEAR_DO_NOT_RETRY",
            clear_payload,
            memory.id,
            sequence=2,
            decision_id="clear-empty",
            project=memory.project,
            namespace=memory.namespace,
        ),
    )

    assert cleared.do_not_retry is None
    assert store.current_sequence == 3
    assert store.list_audit_events()[-1].detail["previous_do_not_retry"] is None


@pytest.mark.parametrize("window", ["lock-open", "snapshot-open", "stage-read-back"])
def test_parent_replacement_is_detected_across_actual_io_windows(tmp_path, monkeypatch, window):
    root = tmp_path / "store"
    moved = tmp_path / "moved"
    attacker = tmp_path / "attacker"
    attacker.mkdir()
    store = _store(root)
    sequence = 0
    if window != "lock-open":
        _propose(store, sequence=0, decision_id="setup-propose")
        sequence = 1
    payload = {**PROPOSE_PAYLOAD, "content": f"window {window}"}
    decision = _decision(
        store, "PROPOSE_MEMORY", payload, _independent_target(payload), sequence=sequence,
        decision_id=f"window-{window}",
    )
    original_open = governance_module.os.open
    original_lseek = governance_module.os.lseek
    attacked = False

    def replace_parent():
        nonlocal attacked
        if not attacked:
            root.rename(moved)
            root.symlink_to(attacker, target_is_directory=True)
            attacked = True

    def window_open(path, flags, *args, **kwargs):
        if (
            (window == "lock-open" and path == LOCK_FILE)
            or (window == "snapshot-open" and path == SNAPSHOT_FILE)
        ):
            replace_parent()
        return original_open(path, flags, *args, **kwargs)

    def window_lseek(fd, offset, whence):
        if window == "stage-read-back":
            replace_parent()
        return original_lseek(fd, offset, whence)

    monkeypatch.setattr(governance_module.os, "open", window_open)
    monkeypatch.setattr(governance_module.os, "lseek", window_lseek)

    with pytest.raises(GovernanceError, match="BLOCK_PATH_CONFINEMENT"):
        store.propose_memory(**payload, decision=decision)

    assert attacked is True
    assert not (attacker / SNAPSHOT_FILE).exists()
    assert not list(moved.glob(".snapshot.*.stage"))


@pytest.mark.parametrize("surface", ["memory-link", "audit-target", "last-payload-link"])
def test_rehashed_nested_relationship_tamper_is_rejected(tmp_path, surface):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="setup-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    store.approve_proposal(
        proposal.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="setup-approve", project=proposal.project, namespace=proposal.namespace,
        ),
    )
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if surface == "memory-link":
        snapshot["memories"][0]["proposal_id"] = "proposal:" + "0" * 32
    elif surface == "audit-target":
        snapshot["audit_events"][-1]["target_id"] = "proposal:" + "0" * 32
    else:
        snapshot["audit_events"][-1]["actor"] = "different-approver"
    snapshot["snapshot_sha256"] = _independent_sha256(
        {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    )
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")

    with pytest.raises(GovernanceError, match="BLOCK_SNAPSHOT_INTEGRITY"):
        store._governance.read_snapshot()


def test_invalid_snapshot_is_reported_by_real_cli_without_internal_exception_text(tmp_path):
    storage = tmp_path / ".local" / "subspace_memory"
    store = SubspaceMemoryStore(storage, workspace_root=tmp_path, clock=lambda: NOW)
    _propose(store, sequence=0, decision_id="setup-propose")
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    snapshot["audit_events"][0]["detail"] = {"status": "forged"}
    snapshot["snapshot_sha256"] = _independent_sha256(
        {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    )
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    code = run_operator_command(
        ["recall", "--workspace-root", str(tmp_path), "--query", "payload"],
        stdout=stdout,
        stderr=stderr,
    )

    assert code == 2
    assert stdout.getvalue() == ""
    assert json.loads(stderr.getvalue()) == {
        "code": "BLOCK_SNAPSHOT_INTEGRITY",
        "disposition": "BLOCK",
    }


def test_contract_2_2_records_all_six_operations_and_preserves_null_clear(tmp_path):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="record-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id,
        approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="record-approve", project=proposal.project,
            namespace=proposal.namespace,
        ),
    )
    lifecycle_payload = {
        "memory_id": memory.id, "lifecycle": "stale", "actor": "human", "reason": None,
    }
    store.set_memory_lifecycle(
        memory.id, "stale", actor="human",
        decision=_decision(
            store, "SET_MEMORY_LIFECYCLE", lifecycle_payload, memory.id, sequence=2,
            decision_id="record-lifecycle", project=memory.project,
            namespace=memory.namespace,
        ),
    )
    set_payload = {
        "memory_id": memory.id, "reason": "guard", "actor": "human", "alternative": None,
    }
    store.set_do_not_retry(
        memory.id, reason="guard", actor="human",
        decision=_decision(
            store, "SET_DO_NOT_RETRY", set_payload, memory.id, sequence=3,
            decision_id="record-set", project=memory.project, namespace=memory.namespace,
        ),
    )
    clear_payload = {"memory_id": memory.id, "actor": "human", "reason": None}
    store.clear_do_not_retry(
        memory.id, actor="human",
        decision=_decision(
            store, "CLEAR_DO_NOT_RETRY", clear_payload, memory.id, sequence=4,
            decision_id="record-clear", project=memory.project, namespace=memory.namespace,
        ),
    )
    store.clear_do_not_retry(
        memory.id, actor="human",
        decision=_decision(
            store, "CLEAR_DO_NOT_RETRY", clear_payload, memory.id, sequence=5,
            decision_id="record-clear-null", project=memory.project,
            namespace=memory.namespace,
        ),
    )
    reject_payload = {**PROPOSE_PAYLOAD, "content": "record reject"}
    rejected = _propose(store, sequence=6, decision_id="record-propose-reject", payload=reject_payload)
    reject_operation_payload = {
        "proposal_id": rejected.id, "reviewer": "human", "reason": "reject",
    }
    store.reject_proposal(
        rejected.id, reviewer="human", reason="reject",
        decision=_decision(
            store, "REJECT_PROPOSAL", reject_operation_payload, rejected.id, sequence=7,
            decision_id="record-reject", project=rejected.project,
            namespace=rejected.namespace,
        ),
    )

    snapshot = store._governance.read_snapshot()
    records = snapshot["mutation_records"]
    assert {record["operation"] for record in records} == set(OPERATIONS)
    assert [record["sequence"] for record in records] == list(range(1, 9))
    assert [record["decision_id"] for record in records] == snapshot["consumed_decision_ids"]
    assert records[0]["previous_record_sha256"] == "0" * 64
    assert all(
        current["previous_record_sha256"] == previous["record_sha256"]
        for previous, current in zip(records, records[1:])
    )
    assert snapshot["last_mutation"] == {
        key: records[-1][key] for key in ("decision_id", "operation", "payload_sha256")
    }
    assert snapshot["memories"][0]["do_not_retry"] is None


@pytest.mark.parametrize(
    "surface",
    ["early-decision", "record-chain", "audit-payload", "record-payload", "orphan-proposal", "final-state"],
)
def test_contract_2_2_rehashed_saved_relationship_tamper_is_rejected(tmp_path, surface):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="tamper-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="tamper-approve", project=proposal.project,
            namespace=proposal.namespace,
        ),
    )
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if surface == "early-decision":
        snapshot["consumed_decision_ids"][0] = "different-early-decision"
    elif surface == "record-chain":
        snapshot["mutation_records"][1]["previous_record_sha256"] = "f" * 64
    elif surface == "audit-payload":
        snapshot["audit_events"][0]["actor"] = "forged-source"
        snapshot["mutation_records"][0]["audit_event_sha256"] = _independent_sha256(
            snapshot["audit_events"][0]
        )
        snapshot["mutation_records"][0]["record_sha256"] = _independent_record_sha256(
            snapshot["mutation_records"][0]
        )
        snapshot["mutation_records"][1]["previous_record_sha256"] = snapshot["mutation_records"][0]["record_sha256"]
        snapshot["mutation_records"][1]["record_sha256"] = _independent_record_sha256(
            snapshot["mutation_records"][1]
        )
    elif surface == "record-payload":
        snapshot["mutation_records"][0]["payload_sha256"] = "f" * 64
        snapshot["mutation_records"][0]["record_sha256"] = _independent_record_sha256(
            snapshot["mutation_records"][0]
        )
        snapshot["mutation_records"][1]["previous_record_sha256"] = snapshot["mutation_records"][0]["record_sha256"]
        snapshot["mutation_records"][1]["record_sha256"] = _independent_record_sha256(
            snapshot["mutation_records"][1]
        )
    elif surface == "orphan-proposal":
        orphan = dict(snapshot["proposals"][0])
        orphan["content"] = "orphan"
        orphan["id"] = _independent_target(
            {
                "project": orphan["project"], "namespace": orphan["namespace"],
                "content": orphan["content"], "source": orphan["source"],
                "tags": orphan["tags"], "confidence": orphan["confidence"],
            }
        )
        snapshot["proposals"].append(orphan)
    else:
        snapshot["memories"][0]["lifecycle"] = "archived"
    _rehash_snapshot(snapshot)
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")

    with pytest.raises(GovernanceError, match="BLOCK_SNAPSHOT_INTEGRITY"):
        store._governance.read_snapshot()


def test_contract_2_2_legacy_v1_snapshot_blocks_without_rewrite(tmp_path):
    root = tmp_path / "store"
    root.mkdir()
    snapshot = {
        "schema_version": "hermes.subspace-memory.snapshot.v1",
        "contract_version": "2.1.0",
        "sequence": 0,
        "consumed_decision_ids": [],
        "proposals": [],
        "memories": [],
        "audit_events": [],
        "previous_snapshot_sha256": "0" * 64,
        "last_mutation": None,
        "snapshot_sha256": "",
    }
    _rehash_snapshot(snapshot)
    raw = (canonical_json(snapshot) + "\n").encode("utf-8")
    (root / SNAPSHOT_FILE).write_bytes(raw)
    store = _store(root)

    with pytest.raises(GovernanceError, match="BLOCK_SNAPSHOT_VERSION_UNSUPPORTED"):
        store._governance.read_snapshot()

    assert (root / SNAPSHOT_FILE).read_bytes() == raw


def test_contract_2_2_rejects_contract_2_1_decision_as_binding_mismatch(tmp_path):
    store = _store(tmp_path / "store")
    decision = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD,
        _independent_target(PROPOSE_PAYLOAD), sequence=0,
    )
    decision["contract_version"] = "2.1.0"

    with pytest.raises(GovernanceError, match="BLOCK_DECISION_BINDING_MISMATCH"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)

    assert not store.storage_root.exists()


def test_lifecycle_and_do_not_retry_competition_preserves_both_updates(tmp_path, monkeypatch):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="race-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    memory = store.approve_proposal(
        proposal.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="race-approve", project=proposal.project,
            namespace=proposal.namespace,
        ),
    )
    entered = threading.Event()
    release = threading.Event()
    original_transact = store._governance.transact

    def pause_lifecycle(decision, **kwargs):
        if kwargs["operation"] == "SET_MEMORY_LIFECYCLE":
            entered.set()
            assert release.wait(timeout=5)
        return original_transact(decision, **kwargs)

    monkeypatch.setattr(store._governance, "transact", pause_lifecycle)
    lifecycle_payload = {
        "memory_id": memory.id, "lifecycle": "stale", "actor": "life", "reason": None,
    }
    lifecycle_decision = _decision(
        store, "SET_MEMORY_LIFECYCLE", lifecycle_payload, memory.id, sequence=3,
        decision_id="race-lifecycle", project=memory.project, namespace=memory.namespace,
    )
    set_payload = {
        "memory_id": memory.id, "reason": "guard", "actor": "dnr", "alternative": None,
    }
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                store.set_memory_lifecycle, memory.id, "stale", actor="life",
                decision=lifecycle_decision,
            )
            assert entered.wait(timeout=5)
            store.set_do_not_retry(
                memory.id, reason="guard", actor="dnr",
                decision=_decision(
                    store, "SET_DO_NOT_RETRY", set_payload, memory.id, sequence=2,
                    decision_id="race-dnr", project=memory.project, namespace=memory.namespace,
                ),
            )
            release.set()
            result = future.result(timeout=5)
    finally:
        release.set()
    snapshot = store._governance.read_snapshot()
    assert result.lifecycle == "stale"
    assert snapshot["memories"][0]["lifecycle"] == "stale"
    assert snapshot["memories"][0]["do_not_retry"]["reason"] == "guard"
    assert snapshot["sequence"] == 4
    assert snapshot["consumed_decision_ids"][-2:] == ["race-dnr", "race-lifecycle"]
    assert store.last_receipt is not None
    assert store.last_receipt.decision_id == "race-lifecycle"
    assert store.last_receipt.committed_sequence == 4


def test_real_lock_timeout_preserves_snapshot_and_decision(tmp_path, monkeypatch):
    root = tmp_path / "store"
    root.mkdir()
    lock_path = root / LOCK_FILE
    lock_path.write_bytes(b"")
    locked = threading.Event()
    release = threading.Event()

    def hold_lock():
        fd = os.open(lock_path, os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            locked.set()
            assert release.wait(timeout=5)
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    worker = threading.Thread(target=hold_lock, daemon=True)
    worker.start()
    assert locked.wait(timeout=5)
    monkeypatch.setattr(governance_module, "LOCK_TIMEOUT_SECONDS", 0.05)
    store = _store(root)
    decision = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD),
        sequence=0, decision_id="lock-timeout",
    )
    started = time.monotonic()
    try:
        with pytest.raises(GovernanceError, match="BLOCK_LOCK_TIMEOUT"):
            store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
    finally:
        release.set()
        worker.join(timeout=5)
    assert not worker.is_alive()
    assert time.monotonic() - started < 2
    assert not (root / SNAPSHOT_FILE).exists()
    assert store._governance.reconcile("lock-timeout")["decision_consumed"] is False


def test_deep_decision_json_returns_stable_governance_error_without_content(tmp_path):
    root = tmp_path / "store"
    store = _store(root)
    decision = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0,
    )
    raw = canonical_json(decision)
    raw = raw.replace(
        '"audit":{"actor":"test-operator"}',
        '"audit":' + "[" * 2000 + "null" + "]" * 2000,
    )
    with pytest.raises(GovernanceError) as captured:
        store.propose_memory(**PROPOSE_PAYLOAD, decision=raw)
    assert captured.value.code == "BLOCK_DECISION_REQUIRED_OR_MALFORMED"
    assert str(captured.value) == "BLOCK_DECISION_REQUIRED_OR_MALFORMED"
    assert not root.exists()


def test_contract_2_2_missing_field_namespace_and_actual_payload_changes_block(tmp_path):
    store = _store(tmp_path / "store")
    valid = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0,
    )
    missing = dict(valid)
    missing.pop("expires_at")
    with pytest.raises(GovernanceError, match="BLOCK_DECISION_REQUIRED_OR_MALFORMED"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=missing)
    wrong_namespace = {**valid, "namespace": "wrong"}
    with pytest.raises(GovernanceError, match="BLOCK_DECISION_BINDING_MISMATCH"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=wrong_namespace)
    changed_payload = {**PROPOSE_PAYLOAD, "content": "actually changed"}
    with pytest.raises(GovernanceError, match="BLOCK_DECISION_BINDING_MISMATCH"):
        store.propose_memory(**changed_payload, decision=valid)
    assert not store.storage_root.exists()


def test_contract_2_2_previous_snapshot_digest_is_bound_at_commit(tmp_path):
    store = _store(tmp_path / "store")
    first = _propose(store, sequence=0, decision_id="previous-first")
    before = store._governance.read_snapshot()
    payload = {"proposal_id": first.id, "approver": "human", "note": None}
    store.approve_proposal(
        first.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", payload, first.id, sequence=1,
            decision_id="previous-second", project=first.project, namespace=first.namespace,
        ),
    )
    after = store._governance.read_snapshot()
    receipt = store.last_receipt
    assert receipt is not None
    assert after["previous_snapshot_sha256"] == before["snapshot_sha256"]
    assert receipt.previous_snapshot_sha256 == before["snapshot_sha256"]
    assert receipt.committed_snapshot_sha256 == after["snapshot_sha256"]


def test_contract_2_2_well_formed_previous_digest_rewrite_is_outside_restart_guarantee(tmp_path):
    store = _store(tmp_path / "store")
    _propose(store, sequence=0, decision_id="previous-rewrite")
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    snapshot["previous_snapshot_sha256"] = "f" * 64
    _rehash_snapshot(snapshot)
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")

    reopened = store._governance.read_snapshot()

    assert reopened["previous_snapshot_sha256"] == "f" * 64


def test_contract_2_2_decision_and_snapshot_byte_limits_are_real(tmp_path):
    root = tmp_path / "store"
    store = _store(root)
    decision = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0,
    )
    oversized_decision = canonical_json(decision) + " " * 16385
    with pytest.raises(GovernanceError, match="BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT"):
        store.propose_memory(**PROPOSE_PAYLOAD, decision=oversized_decision)
    assert not root.exists()

    root.mkdir()
    (root / SNAPSHOT_FILE).write_bytes(b" " * 16777217)
    with pytest.raises(GovernanceError, match="BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT"):
        store._governance.read_snapshot()


@pytest.mark.parametrize(
    ("field", "count"),
    [
        ("proposals", 10001),
        ("memories", 10001),
        ("audit_events", 50001),
        ("consumed_decision_ids", 50001),
        ("mutation_records", 50001),
    ],
)
def test_contract_2_2_all_snapshot_collection_limits_are_enforced(field, count):
    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA,
        "contract_version": CONTRACT_VERSION,
        "sequence": 0,
        "consumed_decision_ids": [],
        "proposals": [],
        "memories": [],
        "audit_events": [],
        "mutation_records": [],
        "previous_snapshot_sha256": "0" * 64,
        "last_mutation": None,
        "snapshot_sha256": "0" * 64,
    }
    snapshot[field] = [None] * count
    with pytest.raises(GovernanceError, match="BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT"):
        governance_module._validate_snapshot(snapshot)


@pytest.mark.parametrize("surface", ["proposal-content", "memory-content", "audit-detail", "record-target", "tags"])
def test_contract_2_2_rehashed_nested_resource_limits_are_enforced(tmp_path, surface):
    store = _store(tmp_path / "store")
    proposal = _propose(store, sequence=0, decision_id="resource-propose")
    approve_payload = {"proposal_id": proposal.id, "approver": "human", "note": None}
    store.approve_proposal(
        proposal.id, approver="human",
        decision=_decision(
            store, "APPROVE_PROPOSAL", approve_payload, proposal.id, sequence=1,
            decision_id="resource-approve", project=proposal.project,
            namespace=proposal.namespace,
        ),
    )
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if surface == "proposal-content":
        snapshot["proposals"][0]["content"] = "x" * 65537
    elif surface == "memory-content":
        snapshot["memories"][0]["content"] = "x" * 65537
    elif surface == "audit-detail":
        snapshot["audit_events"][0]["detail"]["status"] = "x" * 65537
    elif surface == "record-target":
        snapshot["mutation_records"][0]["target"] = "x" * 257
    else:
        snapshot["proposals"][0]["tags"] = ["tag"] * 129
    _rehash_snapshot(snapshot)
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")
    with pytest.raises(GovernanceError, match="BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT"):
        store._governance.read_snapshot()


def test_contract_2_2_valid_top_level_with_mixed_record_format_is_rejected(tmp_path):
    store = _store(tmp_path / "store")
    _propose(store, sequence=0, decision_id="mixed-propose")
    path = store._governance.snapshot_path
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    snapshot["mutation_records"] = [dict(snapshot["last_mutation"])]
    _rehash_snapshot(snapshot)
    path.write_text(canonical_json(snapshot) + "\n", encoding="utf-8")
    with pytest.raises(GovernanceError, match="BLOCK_SNAPSHOT_INTEGRITY"):
        store._governance.read_snapshot()


def test_deep_mapping_and_snapshot_json_have_stable_error_channels(tmp_path):
    store = _store(tmp_path / "store")
    decision = _decision(
        store, "PROPOSE_MEMORY", PROPOSE_PAYLOAD, _independent_target(PROPOSE_PAYLOAD), sequence=0,
    )
    nested = None
    for _ in range(2000):
        nested = [nested]
    decision["audit"] = {"actor": nested}
    with pytest.raises(GovernanceError) as decision_error:
        store.propose_memory(**PROPOSE_PAYLOAD, decision=decision)
    assert decision_error.value.code == "BLOCK_DECISION_REQUIRED_OR_MALFORMED"

    _propose(store, sequence=0, decision_id="deep-snapshot")
    path = store._governance.snapshot_path
    raw = path.read_text(encoding="utf-8")
    raw = raw.replace(
        '"detail":{"status":"pending"}',
        '"detail":{"status":' + "[" * 2000 + "null" + "]" * 2000 + "}",
    )
    path.write_text(raw, encoding="utf-8")
    with pytest.raises(GovernanceError) as snapshot_error:
        store._governance.read_snapshot()
    assert snapshot_error.value.code == "BLOCK_SNAPSHOT_INTEGRITY"


def test_contract_2_2_lock_timeout_default_is_five_seconds():
    assert governance_module.LOCK_TIMEOUT_SECONDS == 5.0
