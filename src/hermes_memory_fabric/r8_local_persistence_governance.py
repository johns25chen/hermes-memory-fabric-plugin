from __future__ import annotations

import fcntl
import hashlib
import json
import math
import os
import stat
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, TypeVar


CONTRACT_VERSION = "2.2.0"
DECISION_SCHEMA = "hermes.local-mutation-decision.v1"
SNAPSHOT_SCHEMA = "hermes.subspace-memory.snapshot.v2"
LEGACY_SNAPSHOT_SCHEMA = "hermes.subspace-memory.snapshot.v1"
SNAPSHOT_FILE = "snapshot.json"
LOCK_FILE = ".snapshot.lock"
GENESIS_DIGEST = "0" * 64
MAX_DECISION_BYTES = 16_384
MAX_SNAPSHOT_BYTES = 16_777_216
MAX_IDENTIFIER_CHARS = 256
MAX_SCOPE_CHARS = 4_096
MAX_AUDIT_CHARS = 256
MAX_BUSINESS_STRING_CHARS = 65_536
MAX_TAGS = 128
MAX_PROPOSALS = 10_000
MAX_MEMORIES = 10_000
MAX_AUDIT_EVENTS = 50_000
MAX_CONSUMED_DECISIONS = 50_000
MAX_MUTATION_RECORDS = 50_000
LOCK_TIMEOUT_SECONDS = 5.0
LOCK_RETRY_SECONDS = 0.01

OPERATIONS = frozenset(
    {
        "PROPOSE_MEMORY",
        "APPROVE_PROPOSAL",
        "REJECT_PROPOSAL",
        "SET_MEMORY_LIFECYCLE",
        "SET_DO_NOT_RETRY",
        "CLEAR_DO_NOT_RETRY",
    }
)
DECISION_FIELDS = frozenset(
    {
        "schema_version", "contract_version", "operation", "workspace_scope",
        "storage_scope", "project", "namespace", "target", "payload_sha256",
        "expected_sequence", "decision_id", "issued_at", "expires_at", "audit",
    }
)
AUDIT_FIELDS = frozenset({"actor", "role", "approver"})
SNAPSHOT_FIELDS = frozenset(
    {
        "schema_version", "contract_version", "sequence", "consumed_decision_ids",
        "proposals", "memories", "audit_events", "mutation_records", "previous_snapshot_sha256",
        "last_mutation", "snapshot_sha256",
    }
)
PROPOSAL_FIELDS = frozenset(
    {
        "schema_version", "id", "project", "namespace", "kind", "content",
        "source", "tags", "confidence", "status", "created_at", "updated_at",
        "reviewer", "approver", "reason", "note",
    }
)
MEMORY_FIELDS = frozenset(
    {
        "schema_version", "id", "proposal_id", "project", "namespace", "kind",
        "content", "source", "tags", "confidence", "status", "created_at",
        "updated_at", "approver", "note", "lifecycle", "do_not_retry",
    }
)
DO_NOT_RETRY_FIELDS = frozenset({"enabled", "reason", "alternative", "actor", "updated_at"})
AUDIT_EVENT_FIELDS = frozenset(
    {
        "schema_version", "id", "kind", "event_type", "target_id", "project",
        "namespace", "actor", "created_at", "detail",
    }
)
LAST_MUTATION_FIELDS = frozenset({"decision_id", "operation", "payload_sha256"})
MUTATION_RECORD_FIELDS = frozenset(
    {
        "sequence", "decision_id", "operation", "project", "namespace", "target",
        "payload_sha256", "audit_event_sha256", "previous_record_sha256",
        "record_sha256",
    }
)
PAYLOAD_FIELDS = {
    "PROPOSE_MEMORY": frozenset({"project", "namespace", "content", "source", "tags", "confidence"}),
    "APPROVE_PROPOSAL": frozenset({"proposal_id", "approver", "note"}),
    "REJECT_PROPOSAL": frozenset({"proposal_id", "reviewer", "reason"}),
    "SET_MEMORY_LIFECYCLE": frozenset({"memory_id", "lifecycle", "actor", "reason"}),
    "SET_DO_NOT_RETRY": frozenset({"memory_id", "reason", "actor", "alternative"}),
    "CLEAR_DO_NOT_RETRY": frozenset({"memory_id", "actor", "reason"}),
}
_HEX_DIGITS = frozenset("0123456789abcdef")
_OPEN_DIRECTORY_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_CLOEXEC", 0)
_OPEN_NOFOLLOW = getattr(os, "O_NOFOLLOW", 0)


class GovernanceError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class MutationReceipt:
    contract_version: str
    operation: str
    decision_id: str
    workspace_scope: str
    storage_scope: str
    project: str
    namespace: str
    target: str
    payload_sha256: str
    previous_sequence: int
    committed_sequence: int
    previous_snapshot_sha256: str
    committed_snapshot_sha256: str
    operator_identity_authenticated: bool
    decision_schema_validated: bool
    decision_scope_bound: bool
    decision_replay_protected: bool
    commit_status: str


T = TypeVar("T")


def canonical_json(value: Any) -> str:
    _reject_non_finite(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def payload_sha256(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(dict(payload)).encode("utf-8")).hexdigest()


def proposal_target(payload: Mapping[str, Any]) -> str:
    return f"proposal:{payload_sha256(payload)[:32]}"


def build_decision_payload(
    *, operation: str, workspace_scope: str | Path, storage_scope: str | Path,
    project: str, namespace: str, target: str, payload: Mapping[str, Any],
    expected_sequence: int, decision_id: str, issued_at: str, expires_at: str,
    audit: Mapping[str, str | None] | None = None,
) -> dict[str, Any]:
    """Build data for a trusted caller; this does not authenticate or attest identity."""
    return {
        "schema_version": DECISION_SCHEMA,
        "contract_version": CONTRACT_VERSION,
        "operation": operation,
        "workspace_scope": str(Path(workspace_scope).absolute()),
        "storage_scope": str(Path(storage_scope).absolute()),
        "project": project,
        "namespace": namespace,
        "target": target,
        "payload_sha256": payload_sha256(payload),
        "expected_sequence": expected_sequence,
        "decision_id": decision_id,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "audit": dict(audit or {}),
    }


class GovernedSnapshotStore:
    def __init__(
        self, storage_root: str | Path, *, workspace_root: str | Path | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        if storage_root is None:
            raise ValueError("storage_root_must_be_explicit")
        self.storage_root = Path(storage_root).expanduser().absolute()
        self.workspace_root = Path(workspace_root).expanduser().absolute() if workspace_root is not None else self.storage_root
        self._clock = clock or (lambda: datetime.now(UTC))
        self.snapshot_path = self.storage_root / SNAPSHOT_FILE
        self.lock_path = self.storage_root / LOCK_FILE
        self.last_receipt: MutationReceipt | None = None
        self._validate_lexical_scope()

    def current_sequence(self) -> int:
        return int(self.read_snapshot()["sequence"])

    def read_snapshot(self) -> dict[str, Any]:
        directory_fd = self._open_storage_directory(create=False)
        if directory_fd is None:
            return _genesis_snapshot()
        try:
            return self._read_snapshot_at(directory_fd)
        finally:
            os.close(directory_fd)

    def reconcile(self, decision_id: str) -> dict[str, Any]:
        snapshot = self.read_snapshot()
        return {
            "sequence": snapshot["sequence"],
            "decision_consumed": decision_id in snapshot["consumed_decision_ids"],
            "snapshot_sha256": snapshot["snapshot_sha256"],
        }

    def transact(
        self, decision: Mapping[str, Any] | str | bytes | None, *, operation: str,
        project: str | None, namespace: str | None, target: str, payload: Mapping[str, Any],
        mutate: Callable[[dict[str, Any], str, Mapping[str, Any]], T],
    ) -> tuple[T, MutationReceipt]:
        parsed = self._validate_static_decision(
            decision, operation=operation, project=project, namespace=namespace,
            target=target, payload=payload,
        )
        directory_fd: int | None = None
        lock_fd: int | None = None
        try:
            directory_fd = self._open_storage_directory(create=True)
            assert directory_fd is not None
            storage_identity = _file_identity(os.fstat(directory_fd))
            lock_fd = os.open(
                LOCK_FILE,
                os.O_RDWR | os.O_CREAT | getattr(os, "O_CLOEXEC", 0) | _OPEN_NOFOLLOW,
                0o600,
                dir_fd=directory_fd,
            )
        except GovernanceError:
            if directory_fd is not None:
                os.close(directory_fd)
            raise
        except OSError:
            if lock_fd is not None:
                os.close(lock_fd)
            if directory_fd is not None:
                os.close(directory_fd)
            raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None
        try:
            assert lock_fd is not None and directory_fd is not None
            try:
                self._validate_open_regular_file(directory_fd, LOCK_FILE, lock_fd)
            except OSError:
                raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None
            deadline = time.monotonic() + LOCK_TIMEOUT_SECONDS
            while True:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise GovernanceError("BLOCK_LOCK_TIMEOUT") from None
                    time.sleep(min(LOCK_RETRY_SECONDS, remaining))
            self._assert_storage_identity(directory_fd, storage_identity)
            self._validate_open_regular_file(directory_fd, LOCK_FILE, lock_fd)
            before = self._read_snapshot_at(directory_fd)
            if parsed["decision_id"] in before["consumed_decision_ids"]:
                raise GovernanceError("BLOCK_DECISION_REPLAY")
            if type(parsed["expected_sequence"]) is not int or parsed["expected_sequence"] != before["sequence"]:
                raise GovernanceError("BLOCK_STALE_SEQUENCE")
            working = json.loads(canonical_json(before))
            audit_count = len(working["audit_events"])
            mutation_at = _format_utc(self._clock())
            result = mutate(working, mutation_at, parsed)
            if len(working["audit_events"]) != audit_count + 1:
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            previous_digest = before["snapshot_sha256"]
            working["sequence"] = before["sequence"] + 1
            working["consumed_decision_ids"].append(parsed["decision_id"])
            working["previous_snapshot_sha256"] = previous_digest
            audit_event = working["audit_events"][-1]
            record = {
                "sequence": working["sequence"],
                "decision_id": parsed["decision_id"],
                "operation": operation,
                "project": parsed["project"],
                "namespace": parsed["namespace"],
                "target": target,
                "payload_sha256": parsed["payload_sha256"],
                "audit_event_sha256": hashlib.sha256(
                    canonical_json(audit_event).encode("utf-8")
                ).hexdigest(),
                "previous_record_sha256": (
                    before["mutation_records"][-1]["record_sha256"]
                    if before["mutation_records"] else GENESIS_DIGEST
                ),
                "record_sha256": "",
            }
            record["record_sha256"] = _mutation_record_digest(record)
            working["mutation_records"].append(record)
            working["last_mutation"] = {
                "decision_id": parsed["decision_id"],
                "operation": operation,
                "payload_sha256": parsed["payload_sha256"],
            }
            self._validate_resource_limits(working)
            working["snapshot_sha256"] = _snapshot_digest(working)
            _validate_snapshot(working)
            self._atomic_commit(directory_fd, storage_identity, working)
            receipt = MutationReceipt(
                contract_version=CONTRACT_VERSION, operation=operation,
                decision_id=parsed["decision_id"], workspace_scope=str(self.workspace_root),
                storage_scope=str(self.storage_root), project=parsed["project"], namespace=parsed["namespace"],
                target=target, payload_sha256=parsed["payload_sha256"],
                previous_sequence=before["sequence"], committed_sequence=working["sequence"],
                previous_snapshot_sha256=previous_digest,
                committed_snapshot_sha256=working["snapshot_sha256"],
                operator_identity_authenticated=False, decision_schema_validated=True,
                decision_scope_bound=True, decision_replay_protected=True,
                commit_status="COMMITTED",
            )
            self.last_receipt = receipt
            return result, receipt
        except GovernanceError:
            raise
        except OSError:
            raise GovernanceError("WRITE_ABORTED_PRECOMMIT") from None
        except (RecursionError, OverflowError):
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT") from None
        finally:
            if lock_fd is not None:
                os.close(lock_fd)
            if directory_fd is not None:
                os.close(directory_fd)

    def _validate_static_decision(self, decision: Any, **binding: Any) -> dict[str, Any]:
        value = _parse_decision(decision)
        if set(value) != DECISION_FIELDS:
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        if value.get("schema_version") != DECISION_SCHEMA or value.get("contract_version") != CONTRACT_VERSION:
            raise GovernanceError("BLOCK_DECISION_BINDING_MISMATCH")
        audit = value.get("audit")
        if not isinstance(audit, dict) or not set(audit).issubset(AUDIT_FIELDS):
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        for item in audit.values():
            if item is not None and (not isinstance(item, str) or len(item) > MAX_AUDIT_CHARS):
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        try:
            if len(canonical_json(value).encode("utf-8")) > MAX_DECISION_BYTES:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        except (RecursionError, TypeError, ValueError, OverflowError):
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED") from None
        _validate_logical_payload(binding["operation"], binding["payload"])
        expected = {
            "operation": binding["operation"], "workspace_scope": str(self.workspace_root),
            "storage_scope": str(self.storage_root), "target": binding["target"],
            "payload_sha256": payload_sha256(binding["payload"]),
        }
        if binding["project"] is not None:
            expected["project"] = binding["project"]
        if binding["namespace"] is not None:
            expected["namespace"] = binding["namespace"]
        if binding["operation"] not in OPERATIONS or any(value.get(k) != v for k, v in expected.items()):
            raise GovernanceError("BLOCK_DECISION_BINDING_MISMATCH")
        for name in ("project", "namespace", "target", "decision_id"):
            if not isinstance(value.get(name), str) or not value[name] or len(value[name]) > MAX_IDENTIFIER_CHARS:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        if not _is_sha256(value.get("payload_sha256")):
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        if any(not isinstance(value.get(name), str) or len(value[name]) > MAX_SCOPE_CHARS for name in ("workspace_scope", "storage_scope")):
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        if type(value.get("expected_sequence")) is not int or value["expected_sequence"] < 0:
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        issued = _parse_utc(value.get("issued_at"))
        expires = _parse_utc(value.get("expires_at"))
        now = self._clock()
        if now.tzinfo is None:
            raise GovernanceError("BLOCK_DECISION_TIME_INVALID")
        now = now.astimezone(UTC).replace(microsecond=0)
        if issued > now or now >= expires or issued >= expires:
            raise GovernanceError("BLOCK_DECISION_TIME_INVALID")
        return value

    def _validate_lexical_scope(self) -> None:
        try:
            self.storage_root.relative_to(self.workspace_root)
        except ValueError:
            raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None

    def _open_storage_directory(self, *, create: bool) -> int | None:
        self._validate_lexical_scope()
        current_fd = os.open(self.storage_root.anchor, _OPEN_DIRECTORY_FLAGS)
        try:
            for part in self.storage_root.parts[1:]:
                try:
                    next_fd = os.open(part, _OPEN_DIRECTORY_FLAGS | _OPEN_NOFOLLOW, dir_fd=current_fd)
                except FileNotFoundError:
                    if not create:
                        os.close(current_fd)
                        return None
                    try:
                        os.mkdir(part, 0o700, dir_fd=current_fd)
                    except FileExistsError:
                        pass
                    next_fd = os.open(part, _OPEN_DIRECTORY_FLAGS | _OPEN_NOFOLLOW, dir_fd=current_fd)
                if not stat.S_ISDIR(os.fstat(next_fd).st_mode):
                    os.close(next_fd)
                    raise GovernanceError("BLOCK_PATH_CONFINEMENT")
                os.close(current_fd)
                current_fd = next_fd
            return current_fd
        except GovernanceError:
            os.close(current_fd)
            raise
        except OSError:
            os.close(current_fd)
            raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None

    def _read_snapshot_at(self, directory_fd: int) -> dict[str, Any]:
        snapshot_fd: int | None = None
        try:
            snapshot_fd = os.open(
                SNAPSHOT_FILE,
                os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | _OPEN_NOFOLLOW,
                dir_fd=directory_fd,
            )
        except FileNotFoundError:
            return _genesis_snapshot()
        except OSError:
            raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None
        try:
            self._validate_open_regular_file(directory_fd, SNAPSHOT_FILE, snapshot_fd)
            size = os.fstat(snapshot_fd).st_size
            if size > MAX_SNAPSHOT_BYTES:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
            chunks: list[bytes] = []
            remaining = MAX_SNAPSHOT_BYTES + 1
            while remaining:
                chunk = os.read(snapshot_fd, min(65_536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            if len(raw) > MAX_SNAPSHOT_BYTES:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
            value = _strict_json_loads(raw.decode("utf-8"), malformed="BLOCK_SNAPSHOT_INTEGRITY")
            _validate_snapshot(value)
            return value
        except GovernanceError:
            raise
        except (OSError, UnicodeError, ValueError, TypeError, RecursionError, OverflowError):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY") from None
        finally:
            if snapshot_fd is not None:
                os.close(snapshot_fd)

    def _validate_open_regular_file(self, directory_fd: int, name: str, file_fd: int) -> None:
        opened = os.fstat(file_fd)
        entry = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(opened.st_mode) or stat.S_ISLNK(entry.st_mode):
            raise GovernanceError("BLOCK_PATH_CONFINEMENT")
        if _file_identity(opened) != _file_identity(entry):
            raise GovernanceError("BLOCK_PATH_CONFINEMENT")

    def _assert_storage_identity(self, directory_fd: int, expected: tuple[int, int]) -> None:
        opened = os.fstat(directory_fd)
        try:
            lexical = os.stat(self.storage_root, follow_symlinks=False)
        except OSError:
            raise GovernanceError("BLOCK_PATH_CONFINEMENT") from None
        if (
            not stat.S_ISDIR(opened.st_mode)
            or not stat.S_ISDIR(lexical.st_mode)
            or _file_identity(opened) != expected
            or _file_identity(lexical) != expected
        ):
            raise GovernanceError("BLOCK_PATH_CONFINEMENT")

    def _validate_resource_limits(self, snapshot: dict[str, Any]) -> None:
        if len(snapshot["proposals"]) > MAX_PROPOSALS or len(snapshot["memories"]) > MAX_MEMORIES:
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        if (
            len(snapshot["audit_events"]) > MAX_AUDIT_EVENTS
            or len(snapshot["consumed_decision_ids"]) > MAX_CONSUMED_DECISIONS
            or len(snapshot["mutation_records"]) > MAX_MUTATION_RECORDS
        ):
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")

    def _atomic_commit(
        self,
        directory_fd: int,
        storage_identity: tuple[int, int],
        snapshot: dict[str, Any],
    ) -> None:
        data = (canonical_json(snapshot) + "\n").encode("utf-8")
        if len(data) > MAX_SNAPSHOT_BYTES:
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        stage_name = f".snapshot.{uuid.uuid4().hex}.stage"
        stage_fd: int | None = None
        replaced = False
        try:
            stage_fd = os.open(
                stage_name,
                os.O_RDWR | os.O_CREAT | os.O_EXCL | getattr(os, "O_CLOEXEC", 0) | _OPEN_NOFOLLOW,
                0o600,
                dir_fd=directory_fd,
            )
            self._validate_open_regular_file(directory_fd, stage_name, stage_fd)
            view = memoryview(data)
            while view:
                written = os.write(stage_fd, view)
                if written <= 0:
                    raise OSError("short_write")
                view = view[written:]
            os.fsync(stage_fd)
            os.lseek(stage_fd, 0, os.SEEK_SET)
            read_back = bytearray()
            while len(read_back) < len(data):
                chunk = os.read(stage_fd, len(data) - len(read_back))
                if not chunk:
                    break
                read_back.extend(chunk)
            if bytes(read_back) != data:
                raise GovernanceError("WRITE_ABORTED_PRECOMMIT")
            os.close(stage_fd)
            stage_fd = None
            self._assert_storage_identity(directory_fd, storage_identity)
            os.replace(stage_name, SNAPSHOT_FILE, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
            replaced = True
            stage_name = ""
            os.fsync(directory_fd)
        except GovernanceError:
            raise
        except OSError:
            if replaced:
                raise GovernanceError("COMMIT_DURABILITY_UNCERTAIN_RECONCILE_REQUIRED") from None
            raise GovernanceError("WRITE_ABORTED_PRECOMMIT") from None
        finally:
            if stage_fd is not None:
                try:
                    os.close(stage_fd)
                except OSError:
                    pass
            if stage_name:
                try:
                    os.unlink(stage_name, dir_fd=directory_fd)
                except OSError:
                    pass


def _parse_decision(decision: Any) -> dict[str, Any]:
    if decision is None:
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
    try:
        if isinstance(decision, bytes):
            if len(decision) > MAX_DECISION_BYTES:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
            value = _strict_json_loads(decision.decode("utf-8"), malformed="BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        elif isinstance(decision, str):
            if len(decision.encode("utf-8")) > MAX_DECISION_BYTES:
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
            value = _strict_json_loads(decision, malformed="BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        elif isinstance(decision, Mapping):
            value = dict(decision)
            _reject_non_finite(value)
        else:
            raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
    except GovernanceError:
        raise
    except (UnicodeError, ValueError, TypeError, OverflowError, RecursionError):
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED") from None
    if not isinstance(value, dict):
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
    return value


def _strict_json_loads(text: str, *, malformed: str) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise GovernanceError(malformed)
            result[key] = value
        return result
    def constant(_: str) -> Any:
        raise GovernanceError(malformed)
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except GovernanceError:
        raise
    except (json.JSONDecodeError, TypeError, RecursionError):
        raise GovernanceError(malformed) from None


def _reject_non_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non_finite_number")
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("non_string_object_key")
            _reject_non_finite(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_non_finite(item)


def _parse_utc(value: Any) -> datetime:
    if not isinstance(value, str) or len(value) != 20 or not value.endswith("Z"):
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except ValueError:
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED") from None
    return parsed


def _format_utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise GovernanceError("BLOCK_DECISION_TIME_INVALID")
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _genesis_snapshot() -> dict[str, Any]:
    value = {
        "schema_version": SNAPSHOT_SCHEMA, "contract_version": CONTRACT_VERSION,
        "sequence": 0, "consumed_decision_ids": [], "proposals": [], "memories": [],
        "audit_events": [], "mutation_records": [], "previous_snapshot_sha256": GENESIS_DIGEST,
        "last_mutation": None, "snapshot_sha256": "",
    }
    value["snapshot_sha256"] = _snapshot_digest(value)
    return value


def _snapshot_digest(snapshot: Mapping[str, Any]) -> str:
    material = {key: value for key, value in snapshot.items() if key != "snapshot_sha256"}
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def _mutation_record_digest(record: Mapping[str, Any]) -> str:
    material = {key: value for key, value in record.items() if key != "record_sha256"}
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def _validate_snapshot(value: Any) -> None:
    if isinstance(value, dict) and value.get("schema_version") == LEGACY_SNAPSHOT_SCHEMA:
        raise GovernanceError("BLOCK_SNAPSHOT_VERSION_UNSUPPORTED")
    if not isinstance(value, dict) or set(value) != SNAPSHOT_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if value["schema_version"] != SNAPSHOT_SCHEMA or value["contract_version"] != CONTRACT_VERSION:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if type(value["sequence"]) is not int or value["sequence"] < 0:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    for field in ("consumed_decision_ids", "proposals", "memories", "audit_events", "mutation_records"):
        if not isinstance(value[field], list):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if (
        len(value["consumed_decision_ids"]) > MAX_CONSUMED_DECISIONS
        or len(value["proposals"]) > MAX_PROPOSALS
        or len(value["memories"]) > MAX_MEMORIES
        or len(value["audit_events"]) > MAX_AUDIT_EVENTS
        or len(value["mutation_records"]) > MAX_MUTATION_RECORDS
    ):
        raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
    if any(not _valid_identifier(item) for item in value["consumed_decision_ids"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if len(value["consumed_decision_ids"]) != len(set(value["consumed_decision_ids"])):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if value["sequence"] != len(value["consumed_decision_ids"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if value["sequence"] != len(value["audit_events"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if value["sequence"] != len(value["mutation_records"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if not _is_sha256(value["previous_snapshot_sha256"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if not _is_sha256(value["snapshot_sha256"]):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if value["snapshot_sha256"] != _snapshot_digest(value):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    proposals = [_validate_proposal_record(record) for record in value["proposals"]]
    memories = [_validate_memory_record(record) for record in value["memories"]]
    audits = [_validate_audit_record(record) for record in value["audit_events"]]
    records = [_validate_mutation_record(record) for record in value["mutation_records"]]
    _validate_audit_relationships(audits, proposals, memories)
    if value["sequence"] == 0:
        if (
            value["last_mutation"] is not None
            or value["previous_snapshot_sha256"] != GENESIS_DIGEST
            or proposals
            or memories
            or audits
            or records
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        return
    mutation = value["last_mutation"]
    if not isinstance(mutation, dict) or set(mutation) != LAST_MUTATION_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if (
        mutation["decision_id"] != value["consumed_decision_ids"][-1]
        or mutation["operation"] not in OPERATIONS
        or not _is_sha256(mutation["payload_sha256"])
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    expected_event = {
        "PROPOSE_MEMORY": "proposal_created",
        "APPROVE_PROPOSAL": "proposal_approved",
        "REJECT_PROPOSAL": "proposal_rejected",
        "SET_MEMORY_LIFECYCLE": "memory_lifecycle_updated",
        "SET_DO_NOT_RETRY": "memory_do_not_retry_set",
        "CLEAR_DO_NOT_RETRY": "memory_do_not_retry_cleared",
    }[mutation["operation"]]
    if audits[-1]["event_type"] != expected_event:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if mutation != {
        key: records[-1][key] for key in ("decision_id", "operation", "payload_sha256")
    }:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _validate_snapshot_history(
        consumed_decision_ids=value["consumed_decision_ids"],
        proposals=proposals,
        memories=memories,
        audits=audits,
        records=records,
    )


def _validate_proposal_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != PROPOSAL_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _reject_record_resource_excess(
        record,
        identifiers=("project", "namespace"),
        business_strings=("content", "source", "reviewer", "approver", "reason", "note"),
        tags=("tags",),
    )
    if (
        record["schema_version"] != "p4-m0.subspace-memory.v1"
        or record["kind"] != "subspace_memory_proposal"
        or not _valid_prefixed_id(record["id"], "proposal:", 32)
        or not _valid_identifier(record["project"])
        or not _valid_identifier(record["namespace"])
        or not _valid_business_string(record["content"], required=True)
        or not _valid_business_string(record["source"], required=True)
        or not _valid_tags(record["tags"])
        or not _valid_confidence(record["confidence"])
        or record["status"] not in {"pending", "approved", "rejected"}
        or not _valid_utc(record["created_at"])
        or not _valid_utc(record["updated_at"])
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    expected_target = proposal_target(
        {
            "project": record["project"], "namespace": record["namespace"],
            "content": record["content"], "source": record["source"],
            "tags": list(record["tags"]), "confidence": record["confidence"],
        }
    )
    if record["id"] != expected_target:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    for field in ("reviewer", "approver", "reason", "note"):
        if record[field] is not None and not _valid_business_string(record[field], required=False):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if record["status"] == "pending" and any(record[field] is not None for field in ("reviewer", "approver", "reason", "note")):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if record["status"] == "approved" and (
        not _valid_business_string(record["approver"], required=True)
        or record["reviewer"] is not None
        or record["reason"] is not None
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if record["status"] == "rejected" and (
        not _valid_business_string(record["reviewer"], required=True)
        or not _valid_business_string(record["reason"], required=True)
        or record["approver"] is not None
        or record["note"] is not None
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    return record


def _validate_memory_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != MEMORY_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _reject_record_resource_excess(
        record,
        identifiers=("project", "namespace"),
        business_strings=("content", "source", "approver", "note"),
        tags=("tags",),
    )
    warning = record["do_not_retry"]
    if isinstance(warning, dict):
        _reject_record_resource_excess(
            warning,
            business_strings=("reason", "alternative", "actor"),
        )
    if (
        record["schema_version"] != "p4-m0.subspace-memory.v1"
        or record["kind"] != "approved_subspace_memory"
        or not _valid_prefixed_id(record["id"], "memory:p4-m0.subspace-memory.v1:", 16)
        or not _valid_prefixed_id(record["proposal_id"], "proposal:", 32)
        or not _valid_identifier(record["project"])
        or not _valid_identifier(record["namespace"])
        or not _valid_business_string(record["content"], required=True)
        or not _valid_business_string(record["source"], required=True)
        or not _valid_tags(record["tags"])
        or not _valid_confidence(record["confidence"])
        or record["status"] != "approved"
        or record["lifecycle"] not in {"active", "stale", "archived"}
        or not _valid_utc(record["created_at"])
        or not _valid_utc(record["updated_at"])
        or not _valid_business_string(record["approver"], required=True)
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if record["note"] is not None and not _valid_business_string(record["note"], required=False):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    expected_memory_id = (
        "memory:p4-m0.subspace-memory.v1:"
        + hashlib.sha256(
            canonical_json({"proposal_id": record["proposal_id"]}).encode("utf-8")
        ).hexdigest()[:16]
    )
    if record["id"] != expected_memory_id:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if warning is not None and not _valid_do_not_retry(warning):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    return record


def _validate_audit_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != AUDIT_EVENT_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _reject_record_resource_excess(
        record,
        identifiers=("target_id", "project", "namespace"),
        business_strings=("actor",),
    )
    if (
        record["schema_version"] != "p4-m0.subspace-memory.v1"
        or record["kind"] != "subspace_memory_audit_event"
        or not _valid_prefixed_id(record["id"], "audit:p4-m0.subspace-memory.v1:", 16)
        or record["event_type"] not in {
            "proposal_created", "proposal_approved", "proposal_rejected",
            "memory_lifecycle_updated", "memory_do_not_retry_set",
            "memory_do_not_retry_cleared",
        }
        or not _valid_identifier(record["target_id"])
        or not _valid_identifier(record["project"])
        or not _valid_identifier(record["namespace"])
        or not _valid_business_string(record["actor"], required=True)
        or not _valid_utc(record["created_at"])
        or not isinstance(record["detail"], dict)
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _validate_nested_business_value(record["detail"])
    expected_id = (
        "audit:p4-m0.subspace-memory.v1:"
        + hashlib.sha256(
            canonical_json(
                {
                    "event_type": record["event_type"],
                    "target_id": record["target_id"],
                    "actor": record["actor"],
                    "created_at": record["created_at"],
                    "detail": record["detail"],
                }
            ).encode("utf-8")
        ).hexdigest()[:16]
    )
    if record["id"] != expected_id:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    return record


def _validate_mutation_record(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != MUTATION_RECORD_FIELDS:
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    _reject_record_resource_excess(
        record,
        identifiers=("decision_id", "project", "namespace", "target"),
    )
    if (
        type(record["sequence"]) is not int
        or record["sequence"] < 1
        or record["operation"] not in OPERATIONS
        or not _valid_identifier(record["decision_id"])
        or not _valid_identifier(record["project"])
        or not _valid_identifier(record["namespace"])
        or not _valid_identifier(record["target"])
        or not _is_sha256(record["payload_sha256"])
        or not _is_sha256(record["audit_event_sha256"])
        or not _is_sha256(record["previous_record_sha256"])
        or not _is_sha256(record["record_sha256"])
        or record["record_sha256"] != _mutation_record_digest(record)
    ):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    return record


def _validate_snapshot_history(
    *,
    consumed_decision_ids: list[str],
    proposals: list[dict[str, Any]],
    memories: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> None:
    proposal_cursor = 0
    proposal_state: dict[str, dict[str, Any]] = {}
    memory_state: dict[str, dict[str, Any]] = {}
    memory_order: list[str] = []
    previous_record_sha256 = GENESIS_DIGEST
    event_for_operation = {
        "PROPOSE_MEMORY": "proposal_created",
        "APPROVE_PROPOSAL": "proposal_approved",
        "REJECT_PROPOSAL": "proposal_rejected",
        "SET_MEMORY_LIFECYCLE": "memory_lifecycle_updated",
        "SET_DO_NOT_RETRY": "memory_do_not_retry_set",
        "CLEAR_DO_NOT_RETRY": "memory_do_not_retry_cleared",
    }

    for index, (decision_id, event, record) in enumerate(
        zip(consumed_decision_ids, audits, records), start=1
    ):
        if (
            record["sequence"] != index
            or record["decision_id"] != decision_id
            or record["previous_record_sha256"] != previous_record_sha256
            or record["audit_event_sha256"]
            != hashlib.sha256(canonical_json(event).encode("utf-8")).hexdigest()
            or event["event_type"] != event_for_operation[record["operation"]]
            or event["target_id"] != record["target"]
            or event["project"] != record["project"]
            or event["namespace"] != record["namespace"]
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")

        operation = record["operation"]
        detail = event["detail"]
        if operation == "PROPOSE_MEMORY":
            if proposal_cursor >= len(proposals):
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            proposal = proposals[proposal_cursor]
            proposal_cursor += 1
            if (
                proposal["id"] in proposal_state
                or proposal["id"] != record["target"]
                or proposal["status"] != "pending"
                or proposal["created_at"] != event["created_at"]
                or proposal["updated_at"] != event["created_at"]
                or proposal["source"] != event["actor"]
                or detail != {"status": "pending"}
            ):
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            proposal_state[proposal["id"]] = proposal
            linked_payload = {
                "project": proposal["project"], "namespace": proposal["namespace"],
                "content": proposal["content"], "source": proposal["source"],
                "tags": list(proposal["tags"]), "confidence": proposal["confidence"],
            }
        elif operation in {"APPROVE_PROPOSAL", "REJECT_PROPOSAL"}:
            if proposal_cursor >= len(proposals):
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            prior = proposal_state.get(record["target"])
            proposal = proposals[proposal_cursor]
            proposal_cursor += 1
            expected_status = "approved" if operation == "APPROVE_PROPOSAL" else "rejected"
            if prior is None or prior["status"] != "pending" or proposal["id"] != record["target"]:
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            expected = dict(prior)
            expected["status"] = expected_status
            expected["updated_at"] = event["created_at"]
            if operation == "APPROVE_PROPOSAL":
                expected["approver"] = event["actor"]
                expected["note"] = detail.get("note")
            else:
                expected["reviewer"] = event["actor"]
                expected["reason"] = detail.get("reason")
            if canonical_json(proposal) != canonical_json(expected):
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            proposal_state[proposal["id"]] = proposal
            if operation == "APPROVE_PROPOSAL":
                memory_id = detail.get("memory_id")
                expected_memory_id = (
                    "memory:p4-m0.subspace-memory.v1:"
                    + hashlib.sha256(
                        canonical_json({"proposal_id": proposal["id"]}).encode("utf-8")
                    ).hexdigest()[:16]
                )
                if memory_id != expected_memory_id or memory_id in memory_state:
                    raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
                memory_state[memory_id] = {
                    "schema_version": proposal["schema_version"],
                    "id": memory_id,
                    "proposal_id": proposal["id"],
                    "project": proposal["project"],
                    "namespace": proposal["namespace"],
                    "kind": "approved_subspace_memory",
                    "content": proposal["content"],
                    "source": proposal["source"],
                    "tags": proposal["tags"],
                    "confidence": proposal["confidence"],
                    "status": "approved",
                    "created_at": event["created_at"],
                    "updated_at": event["created_at"],
                    "approver": event["actor"],
                    "note": detail["note"],
                    "lifecycle": "active",
                    "do_not_retry": None,
                }
                memory_order.append(memory_id)
                linked_payload = {
                    "proposal_id": record["target"], "approver": event["actor"],
                    "note": detail["note"],
                }
            else:
                linked_payload = {
                    "proposal_id": record["target"], "reviewer": event["actor"],
                    "reason": detail["reason"],
                }
        else:
            current = memory_state.get(record["target"])
            if current is None:
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            updated = dict(current)
            if operation == "SET_MEMORY_LIFECYCLE":
                if detail["previous_lifecycle"] != current["lifecycle"]:
                    raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
                updated["lifecycle"] = detail["lifecycle"]
                linked_payload = {
                    "memory_id": record["target"], "lifecycle": detail["lifecycle"],
                    "actor": event["actor"], "reason": detail["reason"],
                }
            elif operation == "SET_DO_NOT_RETRY":
                updated["do_not_retry"] = {
                    "enabled": True, "reason": detail["reason"],
                    "alternative": detail["alternative"], "actor": event["actor"],
                    "updated_at": event["created_at"],
                }
                linked_payload = {
                    "memory_id": record["target"], "reason": detail["reason"],
                    "actor": event["actor"], "alternative": detail["alternative"],
                }
            else:
                if canonical_json(detail["previous_do_not_retry"]) != canonical_json(current["do_not_retry"]):
                    raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
                updated["do_not_retry"] = None
                linked_payload = {
                    "memory_id": record["target"], "actor": event["actor"],
                    "reason": detail["reason"],
                }
            updated["updated_at"] = event["created_at"]
            memory_state[record["target"]] = updated

        if (
            record["project"] != event["project"]
            or record["namespace"] != event["namespace"]
            or record["payload_sha256"] != payload_sha256(linked_payload)
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        previous_record_sha256 = record["record_sha256"]

    if proposal_cursor != len(proposals):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    replayed_memories = [memory_state[memory_id] for memory_id in memory_order]
    if canonical_json(replayed_memories) != canonical_json(memories):
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")


def _validate_snapshot_relationships(
    proposals: list[dict[str, Any]], memories: list[dict[str, Any]]
) -> None:
    proposal_versions: dict[str, list[dict[str, Any]]] = {}
    for record in proposals:
        proposal_versions.setdefault(record["id"], []).append(record)
    for versions in proposal_versions.values():
        first = versions[0]
        if first["status"] != "pending":
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        terminal_seen = False
        immutable = ("project", "namespace", "content", "source", "tags", "confidence", "created_at")
        for record in versions[1:]:
            if any(canonical_json(record[field]) != canonical_json(first[field]) for field in immutable):
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            if terminal_seen or record["status"] == "pending":
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            terminal_seen = True
    memory_ids: set[str] = set()
    for memory in memories:
        if memory["id"] in memory_ids:
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        memory_ids.add(memory["id"])
        approved = next(
            (
                proposal
                for proposal in reversed(proposal_versions.get(memory["proposal_id"], []))
                if proposal["status"] == "approved"
            ),
            None,
        )
        if approved is None or any(
            canonical_json(memory[field]) != canonical_json(approved[field])
            for field in ("project", "namespace", "content", "source", "tags", "confidence", "approver", "note")
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")


def _validate_audit_relationships(
    audits: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
    memories: list[dict[str, Any]],
) -> None:
    proposal_by_id = {proposal["id"]: proposal for proposal in proposals}
    memory_by_id = {memory["id"]: memory for memory in memories}
    for event in audits:
        if event["event_type"].startswith("proposal_"):
            target = proposal_by_id.get(event["target_id"])
        else:
            target = memory_by_id.get(event["target_id"])
        if target is None or (
            event["project"] != target["project"]
            or event["namespace"] != target["namespace"]
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        detail = event["detail"]
        if event["event_type"] == "proposal_created" and detail != {"status": "pending"}:
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        if event["event_type"] == "proposal_approved":
            if set(detail) != {"memory_id", "note", "status"} or detail["status"] != "approved":
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
            memory = memory_by_id.get(detail["memory_id"])
            if memory is None or memory["proposal_id"] != event["target_id"]:
                raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        if event["event_type"] == "proposal_rejected" and (
            set(detail) != {"reason", "status"}
            or detail["status"] != "rejected"
            or not _valid_business_string(detail["reason"], required=True)
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        if event["event_type"] == "memory_lifecycle_updated" and (
            set(detail) != {"previous_lifecycle", "lifecycle", "reason"}
            or detail["previous_lifecycle"] not in {"active", "stale", "archived"}
            or detail["lifecycle"] not in {"active", "stale", "archived"}
            or (detail["reason"] is not None and not _valid_business_string(detail["reason"], required=False))
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        if event["event_type"] == "memory_do_not_retry_set" and (
            set(detail) != {"reason", "alternative"}
            or not _valid_business_string(detail["reason"], required=True)
            or (
                detail["alternative"] is not None
                and not _valid_business_string(detail["alternative"], required=False)
            )
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
        if event["event_type"] == "memory_do_not_retry_cleared" and (
            set(detail) != {"previous_do_not_retry", "reason"}
            or (
                detail["previous_do_not_retry"] is not None
                and not _valid_do_not_retry(detail["previous_do_not_retry"])
            )
            or (detail["reason"] is not None and not _valid_business_string(detail["reason"], required=False))
        ):
            raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")


def _payload_from_audit_event(
    event: dict[str, Any],
    proposals: list[dict[str, Any]],
    memories: list[dict[str, Any]],
) -> dict[str, Any]:
    proposal = next(
        (record for record in reversed(proposals) if record["id"] == event["target_id"]),
        None,
    )
    memory = next(
        (record for record in memories if record["id"] == event["target_id"]),
        None,
    )
    detail = event["detail"]
    if event["event_type"] == "proposal_created":
        assert proposal is not None
        return {
            "project": proposal["project"], "namespace": proposal["namespace"],
            "content": proposal["content"], "source": proposal["source"],
            "tags": list(proposal["tags"]), "confidence": proposal["confidence"],
        }
    if event["event_type"] == "proposal_approved":
        return {"proposal_id": event["target_id"], "approver": event["actor"], "note": detail["note"]}
    if event["event_type"] == "proposal_rejected":
        return {"proposal_id": event["target_id"], "reviewer": event["actor"], "reason": detail["reason"]}
    assert memory is not None
    if event["event_type"] == "memory_lifecycle_updated":
        return {
            "memory_id": event["target_id"], "lifecycle": detail["lifecycle"],
            "actor": event["actor"], "reason": detail["reason"],
        }
    if event["event_type"] == "memory_do_not_retry_set":
        return {
            "memory_id": event["target_id"], "reason": detail["reason"],
            "actor": event["actor"], "alternative": detail["alternative"],
        }
    return {
        "memory_id": event["target_id"], "actor": event["actor"],
        "reason": detail["reason"],
    }


def _validate_logical_payload(operation: Any, payload: Any) -> None:
    if operation not in PAYLOAD_FIELDS or not isinstance(payload, Mapping) or set(payload) != PAYLOAD_FIELDS[operation]:
        raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
    for field, value in payload.items():
        if field in {"project", "namespace", "proposal_id", "memory_id"}:
            if not _valid_identifier(value):
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        elif field == "tags":
            if not isinstance(value, list) or not _valid_tags(value):
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        elif field == "confidence":
            if not _valid_confidence(value):
                raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
        elif field == "lifecycle":
            if value not in {"active", "stale", "archived"}:
                raise GovernanceError("BLOCK_DECISION_REQUIRED_OR_MALFORMED")
        elif value is not None and not _valid_business_string(value, required=field not in {"note", "reason", "alternative"}):
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")


def _valid_identifier(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and len(value) <= MAX_IDENTIFIER_CHARS


def _reject_record_resource_excess(
    record: Mapping[str, Any], *, identifiers: tuple[str, ...] = (),
    business_strings: tuple[str, ...] = (), tags: tuple[str, ...] = (),
) -> None:
    if any(
        isinstance(record.get(field), str)
        and len(record[field]) > MAX_IDENTIFIER_CHARS
        for field in identifiers
    ):
        raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
    if any(
        isinstance(record.get(field), str)
        and len(record[field]) > MAX_BUSINESS_STRING_CHARS
        for field in business_strings
    ):
        raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
    for field in tags:
        value = record.get(field)
        if isinstance(value, (list, tuple)) and (
            len(value) > MAX_TAGS
            or any(
                isinstance(item, str) and len(item) > MAX_BUSINESS_STRING_CHARS
                for item in value
            )
        ):
            raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")


def _valid_business_string(value: Any, *, required: bool) -> bool:
    return (
        isinstance(value, str)
        and len(value) <= MAX_BUSINESS_STRING_CHARS
        and (not required or bool(value.strip()))
    )


def _valid_tags(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and len(value) <= MAX_TAGS
        and all(_valid_business_string(item, required=True) for item in value)
    )


def _valid_confidence(value: Any) -> bool:
    return (
        type(value) in {int, float}
        and math.isfinite(value)
        and 0.0 <= value <= 1.0
    )


def _valid_do_not_retry(value: Any) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == DO_NOT_RETRY_FIELDS
        and value["enabled"] is True
        and _valid_business_string(value["reason"], required=True)
        and _valid_business_string(value["actor"], required=True)
        and _valid_utc(value["updated_at"])
        and (
            value["alternative"] is None
            or _valid_business_string(value["alternative"], required=False)
        )
    )


def _valid_utc(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        _parse_utc(value)
    except GovernanceError:
        return False
    return True


def _valid_prefixed_id(value: Any, prefix: str, hex_length: int) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(prefix)
        and len(value) == len(prefix) + hex_length
        and set(value[len(prefix):]).issubset(_HEX_DIGITS)
    )


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value).issubset(_HEX_DIGITS)


def _validate_nested_business_value(value: Any) -> None:
    if value is None or type(value) in {bool, int}:
        return
    if type(value) is float:
        if math.isfinite(value):
            return
        raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")
    if isinstance(value, str):
        if len(value) <= MAX_BUSINESS_STRING_CHARS:
            return
        raise GovernanceError("BLOCK_UNSUPPORTED_OR_RESOURCE_LIMIT")
    if isinstance(value, list):
        for item in value:
            _validate_nested_business_value(item)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for item in value.values():
            _validate_nested_business_value(item)
        return
    raise GovernanceError("BLOCK_SNAPSHOT_INTEGRITY")


def _file_identity(value: os.stat_result) -> tuple[int, int]:
    return value.st_dev, value.st_ino


def receipt_as_dict(receipt: MutationReceipt) -> dict[str, Any]:
    return asdict(receipt)
