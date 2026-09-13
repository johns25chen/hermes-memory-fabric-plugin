"""Hermes-compatible Memory Fabric provider wrapper."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable, Mapping
import re
import uuid

try:
    from agent.memory_provider import MemoryProvider
except Exception:  # pragma: no cover - standalone test fallback
    from .memory_provider import MemoryProvider

from .candidate_jsonl_source import (
    DEFAULT_CANDIDATE_JSONL_IGNORE_INVALID_LINES,
    DEFAULT_CANDIDATE_JSONL_MAX_BYTES,
    DEFAULT_CANDIDATE_JSONL_MAX_LINES,
    load_candidate_jsonl_source,
)
from .memory_active_context_composer import (
    DEFAULT_CONTEXT_BUDGET_CHARS,
    DEFAULT_MAX_ACTIVE_SUBSPACES,
    DEFAULT_MEMORY_LIMIT,
    compose_active_context,
    explain_active_context_packet,
    summarize_active_context_packet,
    validate_active_context_packet,
)
from .provider_federation_boundary import admit_candidate_batch, canonical_payload_digest


PROVIDER_RUNTIME_INTEGRATION_POLICY = {
    "read_only": True,
    "would_write_memory": False,
    "would_modify_config": False,
    "would_write_graph": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_token_write_executor": False,
    "implements_real_token_write_executor": False,
    "exposes_provider_tools": False,
}

DEFAULT_PROVIDER_RUNTIME_CONFIG = {
    "project_scope": None,
    "agent_scope": None,
    "max_active_subspaces": DEFAULT_MAX_ACTIVE_SUBSPACES,
    "memory_limit": DEFAULT_MEMORY_LIMIT,
    "context_budget_chars": DEFAULT_CONTEXT_BUDGET_CHARS,
    "include_archived": False,
    "allowed_risk_levels": None,
    "required_tags": None,
    "candidate_jsonl_path": None,
    "candidate_jsonl_max_lines": DEFAULT_CANDIDATE_JSONL_MAX_LINES,
    "candidate_jsonl_max_bytes": DEFAULT_CANDIDATE_JSONL_MAX_BYTES,
    "candidate_jsonl_required_fields": None,
    "candidate_jsonl_ignore_invalid_lines": DEFAULT_CANDIDATE_JSONL_IGNORE_INVALID_LINES,
    "admission_scope": None,
    "provider_registry_snapshot": None,
    "runtime_candidate_source": None,
    "candidate_jsonl_source": None,
    "direct_candidate_source": None,
}
PROVIDER_RUNTIME_CONFIG_FIELDS = tuple(DEFAULT_PROVIDER_RUNTIME_CONFIG)


class MemoryFabricProvider(MemoryProvider):
    """Read-only Memory Fabric provider shell for standalone plugin loading."""

    name = "memory-fabric"
    runtime_integration_policy = PROVIDER_RUNTIME_INTEGRATION_POLICY

    def __init__(
        self,
        runtime_memory_candidates: Iterable[Mapping[str, Any]] | None = None,
        runtime_config: Mapping[str, Any] | None = None,
        **runtime_config_overrides: Any,
    ) -> None:
        self.session_id = ""
        self.hermes_home = ""
        self.initialized_kwargs: dict[str, Any] = {}
        config = dict(runtime_config) if isinstance(runtime_config, Mapping) else {}
        config.update(runtime_config_overrides)
        self.runtime_config = _normalize_provider_runtime_config(config)
        self._runtime_memory_candidates: list[dict[str, Any]] = []
        self.set_runtime_memory_candidates(runtime_memory_candidates)

    def is_available(self) -> bool:
        return True

    def initialize(self, session_id: str, **kwargs: Any) -> None:
        self.session_id = session_id
        self.hermes_home = str(kwargs.get("hermes_home", ""))
        self.initialized_kwargs = deepcopy(dict(kwargs))
        runtime_overrides = _extract_provider_runtime_config(kwargs)
        if runtime_overrides:
            self.runtime_config = _normalize_provider_runtime_config(
                {**self.runtime_config, **runtime_overrides}
            )

    def system_prompt_block(self) -> str:
        return (
            "Memory Fabric is available in read-only standalone plugin mode. "
            "The provider can prepare bounded active context packets, performs "
            "no durable writes or token executor invocation, and exposes no "
            "tools by default."
        )

    def build_active_context(
        self,
        *,
        query: str,
        memory_candidates: Iterable[Mapping[str, Any]],
        subspace_registry: Mapping[str, Any] | None = None,
        context: Mapping[str, Any] | None = None,
        project_scope: str | None = None,
        agent_scope: str | None = None,
        entity_ids: Iterable[str] | None = None,
        now: Any | None = None,
        max_active_subspaces: int | None = None,
        memory_limit: int | None = None,
        context_budget_chars: int | None = None,
        include_archived: bool | None = None,
        allowed_risk_levels: Iterable[str] | None = None,
        required_tags: Iterable[str] | None = None,
        include_rejected: bool = False,
        admission_scope: Mapping[str, Any] | None = None,
        provider_registry_snapshot: Mapping[str, Any] | None = None,
        candidate_source_descriptor: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build a deterministic, read-only active context packet."""
        runtime_config = self._active_context_runtime_config(
            project_scope=project_scope,
            agent_scope=agent_scope,
            max_active_subspaces=max_active_subspaces,
            memory_limit=memory_limit,
            context_budget_chars=context_budget_chars,
            include_archived=include_archived,
            allowed_risk_levels=allowed_risk_levels,
            required_tags=required_tags,
        )
        candidates = _copy_runtime_memory_candidates(memory_candidates)
        admitted_candidates = self._admit_candidate_sources(
            sources=[
                (
                    (
                        candidate_source_descriptor
                        if candidate_source_descriptor is not None
                        else self.runtime_config.get("direct_candidate_source")
                    ),
                    candidates,
                )
            ],
            request_scope=(
                admission_scope
                if admission_scope is not None
                else self.runtime_config.get("admission_scope")
            ),
            provider_registry_snapshot=(
                provider_registry_snapshot
                if provider_registry_snapshot is not None
                else self.runtime_config.get("provider_registry_snapshot")
            ),
        )
        return self._compose_active_context(
            query=query,
            memory_candidates=admitted_candidates,
            subspace_registry=subspace_registry,
            context=context,
            entity_ids=entity_ids,
            now=now,
            include_rejected=include_rejected,
            runtime_config=runtime_config,
        )

    def _compose_active_context(
        self,
        *,
        query: str,
        memory_candidates: Iterable[Mapping[str, Any]],
        subspace_registry: Mapping[str, Any] | None,
        context: Mapping[str, Any] | None,
        entity_ids: Iterable[str] | None,
        now: Any | None,
        include_rejected: bool,
        runtime_config: Mapping[str, Any],
    ) -> dict[str, Any]:
        return compose_active_context(
            query=query,
            memory_candidates=memory_candidates,
            subspace_registry=subspace_registry,
            context=context,
            project_scope=runtime_config["project_scope"],
            agent_scope=runtime_config["agent_scope"],
            entity_ids=entity_ids,
            now=now,
            max_active_subspaces=runtime_config["max_active_subspaces"],
            memory_limit=runtime_config["memory_limit"],
            context_budget_chars=runtime_config["context_budget_chars"],
            include_archived=runtime_config["include_archived"],
            allowed_risk_levels=runtime_config["allowed_risk_levels"],
            required_tags=runtime_config["required_tags"],
            include_rejected=include_rejected,
        )

    def summarize_active_context(self, packet: Mapping[str, Any]) -> dict[str, Any]:
        """Summarize an active context packet without side effects."""
        return summarize_active_context_packet(packet)

    def explain_active_context(self, packet: Mapping[str, Any]) -> dict[str, Any]:
        """Explain selected and rejected active context items without side effects."""
        return explain_active_context_packet(packet)

    def validate_active_context(self, packet: Mapping[str, Any]) -> dict[str, Any]:
        """Validate an active context packet without side effects."""
        return validate_active_context_packet(packet)

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        try:
            candidates = self._prefetch_memory_candidates_snapshot()
            if not candidates:
                return ""

            runtime_config = self._active_context_runtime_config(
                project_scope=self.runtime_config.get("project_scope"),
                agent_scope=None,
                max_active_subspaces=None,
                memory_limit=None,
                context_budget_chars=None,
                include_archived=None,
                allowed_risk_levels=None,
                required_tags=None,
            )
            packet = self._compose_active_context(
                query=str(query),
                memory_candidates=candidates,
                subspace_registry=None,
                context=None,
                entity_ids=None,
                now=None,
                include_rejected=False,
                runtime_config=runtime_config,
            )
            validity = self.validate_active_context(packet)
            if validity != {"valid": True, "errors": []}:
                return ""

            compact_context_text = packet.get("compact_context_text")
            if not isinstance(compact_context_text, str) or not compact_context_text:
                return ""
            return compact_context_text
        except Exception:
            return ""

    def set_runtime_memory_candidates(self, candidates: Iterable[Mapping[str, Any]] | None) -> None:
        self._runtime_memory_candidates = _copy_runtime_memory_candidates(candidates)

    def clear_runtime_memory_candidates(self) -> None:
        self._runtime_memory_candidates = []

    def queue_prefetch(self, query: str, *, session_id: str = "") -> None:
        return None

    def sync_turn(
        self,
        user_content: str,
        assistant_content: str,
        *,
        session_id: str = "",
    ) -> None:
        return None

    def get_tool_schemas(self) -> list[dict[str, Any]]:
        return []

    def handle_tool_call(
        self,
        tool_name: str,
        args: dict[str, Any],
        **kwargs: Any,
    ) -> str:
        raise NotImplementedError("Memory Fabric provider exposes no tools in v0.1.")

    def shutdown(self) -> None:
        return None

    def get_config_schema(self) -> list[dict[str, Any]]:
        return []

    def save_config(self, values: dict[str, Any], hermes_home: str) -> None:
        return None

    def _active_context_runtime_config(
        self,
        *,
        project_scope: str | None,
        agent_scope: str | None,
        max_active_subspaces: int | None,
        memory_limit: int | None,
        context_budget_chars: int | None,
        include_archived: bool | None,
        allowed_risk_levels: Iterable[str] | None,
        required_tags: Iterable[str] | None,
    ) -> dict[str, Any]:
        overrides = {
            "project_scope": project_scope,
            "agent_scope": agent_scope,
            "max_active_subspaces": max_active_subspaces,
            "memory_limit": memory_limit,
            "context_budget_chars": context_budget_chars,
            "include_archived": include_archived,
            "allowed_risk_levels": allowed_risk_levels,
            "required_tags": required_tags,
        }
        effective = dict(self.runtime_config)
        effective.update({key: value for key, value in overrides.items() if value is not None})
        return _normalize_provider_runtime_config(effective)

    def _runtime_memory_candidates_snapshot(self) -> list[dict[str, Any]]:
        return deepcopy(self._runtime_memory_candidates)

    def _prefetch_memory_candidates_snapshot(self) -> list[dict[str, Any]]:
        admitted = self._admit_candidate_sources(
            sources=[
                (
                    self.runtime_config.get("candidate_jsonl_source"),
                    self._candidate_jsonl_candidates_snapshot(),
                ),
                (
                    self.runtime_config.get("runtime_candidate_source"),
                    self._runtime_memory_candidates_snapshot(),
                ),
            ],
            request_scope=self.runtime_config.get("admission_scope"),
            provider_registry_snapshot=self.runtime_config.get("provider_registry_snapshot"),
        )
        return _merge_candidate_sources(admitted_candidates=admitted)

    def _admit_candidate_sources(
        self,
        *,
        sources: Iterable[tuple[Any, Iterable[Mapping[str, Any]]]],
        request_scope: Any,
        provider_registry_snapshot: Any,
    ) -> list[dict[str, Any]]:
        prepared: list[dict[str, Any]] = []
        for descriptor, candidates in sources:
            for candidate in candidates:
                prepared.append(
                    _candidate_admission_item(
                        payload=candidate,
                        source_descriptor=descriptor,
                        request_scope=request_scope,
                    )
                )
        if not prepared:
            return []
        result = admit_candidate_batch(
            request_scope=request_scope if isinstance(request_scope, Mapping) else {},
            provider_registry_snapshot=(
                provider_registry_snapshot
                if isinstance(provider_registry_snapshot, Mapping)
                else {}
            ),
            items=prepared,
        )
        allowed: list[dict[str, Any]] = []
        for prepared_item, receipt in zip(prepared, result["receipts"], strict=True):
            if receipt["decision"] != "ALLOW":
                continue
            candidate = deepcopy(prepared_item["payload"])
            candidate["provider_federation_identity"] = {
                "provider_id": receipt["provider_id"],
                "source_class": receipt["source_class"],
                "source_instance": receipt["source_instance"],
                "candidate_id": receipt["candidate_id"],
                "request_id": receipt["request_id"],
                "payload_digest": receipt["payload_digest"],
                "request_scope_digest": receipt["request_scope_digest"],
            }
            allowed.append(candidate)
        return allowed

    def _candidate_jsonl_candidates_snapshot(self) -> list[dict[str, Any]]:
        path = self.runtime_config.get("candidate_jsonl_path")
        if not path:
            return []
        return load_candidate_jsonl_source(
            path,
            max_lines=self.runtime_config.get("candidate_jsonl_max_lines"),
            max_bytes=self.runtime_config.get("candidate_jsonl_max_bytes"),
            required_fields=self.runtime_config.get("candidate_jsonl_required_fields"),
            ignore_invalid_lines=bool(self.runtime_config.get("candidate_jsonl_ignore_invalid_lines", True)),
        )


def register(ctx: Any) -> None:
    """Register the Memory Fabric provider with a Hermes plugin context."""

    ctx.register_memory_provider(MemoryFabricProvider())


def _extract_provider_runtime_config(values: Mapping[str, Any]) -> dict[str, Any]:
    extracted: dict[str, Any] = {}
    for nested_key in ("runtime_config", "provider_runtime_config", "active_context_config"):
        nested = values.get(nested_key)
        if isinstance(nested, Mapping):
            extracted.update(
                {field: deepcopy(nested[field]) for field in PROVIDER_RUNTIME_CONFIG_FIELDS if field in nested}
            )
    extracted.update(
        {field: deepcopy(values[field]) for field in PROVIDER_RUNTIME_CONFIG_FIELDS if field in values}
    )
    return extracted


def _normalize_provider_runtime_config(values: Mapping[str, Any] | None) -> dict[str, Any]:
    raw = dict(DEFAULT_PROVIDER_RUNTIME_CONFIG)
    if isinstance(values, Mapping):
        raw.update({field: deepcopy(values[field]) for field in PROVIDER_RUNTIME_CONFIG_FIELDS if field in values})
    return {
        "project_scope": _optional_text(raw.get("project_scope")),
        "agent_scope": _optional_text(raw.get("agent_scope")),
        "max_active_subspaces": _non_negative_int(
            raw.get("max_active_subspaces"),
            DEFAULT_PROVIDER_RUNTIME_CONFIG["max_active_subspaces"],
        ),
        "memory_limit": _non_negative_int(raw.get("memory_limit"), DEFAULT_PROVIDER_RUNTIME_CONFIG["memory_limit"]),
        "context_budget_chars": _non_negative_int(
            raw.get("context_budget_chars"),
            DEFAULT_PROVIDER_RUNTIME_CONFIG["context_budget_chars"],
        ),
        "include_archived": bool(raw.get("include_archived", DEFAULT_PROVIDER_RUNTIME_CONFIG["include_archived"])),
        "allowed_risk_levels": _optional_list(raw.get("allowed_risk_levels")),
        "required_tags": _optional_list(raw.get("required_tags")),
        "candidate_jsonl_path": _optional_text(raw.get("candidate_jsonl_path")),
        "candidate_jsonl_max_lines": _non_negative_int(
            raw.get("candidate_jsonl_max_lines"),
            DEFAULT_PROVIDER_RUNTIME_CONFIG["candidate_jsonl_max_lines"],
        ),
        "candidate_jsonl_max_bytes": _non_negative_int(
            raw.get("candidate_jsonl_max_bytes"),
            DEFAULT_PROVIDER_RUNTIME_CONFIG["candidate_jsonl_max_bytes"],
        ),
        "candidate_jsonl_required_fields": _optional_list(raw.get("candidate_jsonl_required_fields")),
        "candidate_jsonl_ignore_invalid_lines": bool(
            raw.get(
                "candidate_jsonl_ignore_invalid_lines",
                DEFAULT_PROVIDER_RUNTIME_CONFIG["candidate_jsonl_ignore_invalid_lines"],
            )
        ),
        "admission_scope": _optional_mapping(raw.get("admission_scope")),
        "provider_registry_snapshot": _optional_mapping(raw.get("provider_registry_snapshot")),
        "runtime_candidate_source": _optional_mapping(raw.get("runtime_candidate_source")),
        "candidate_jsonl_source": _optional_mapping(raw.get("candidate_jsonl_source")),
        "direct_candidate_source": _optional_mapping(raw.get("direct_candidate_source")),
    }


def _optional_list(value: Any) -> list[Any] | None:
    if value is None:
        return None
    if isinstance(value, (str, bytes, bytearray)):
        return [str(value)]
    try:
        return deepcopy(list(value))
    except TypeError:
        return [deepcopy(value)]


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _optional_mapping(value: Any) -> dict[str, Any] | None:
    return deepcopy(dict(value)) if isinstance(value, Mapping) else None


def _copy_runtime_memory_candidates(candidates: Iterable[Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    if candidates is None:
        return []
    copied: list[dict[str, Any]] = []
    for candidate in candidates:
        if isinstance(candidate, Mapping):
            copied.append(deepcopy(dict(candidate)))
    return copied


def _merge_candidate_sources(*, admitted_candidates: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    positions_by_identity: dict[tuple[str, str, str], int] = {}
    for candidate in admitted_candidates:
        identity_map = candidate.get("provider_federation_identity")
        if not isinstance(identity_map, Mapping):
            continue
        identity = tuple(
            str(identity_map.get(field, ""))
            for field in ("provider_id", "source_instance", "candidate_id")
        )
        copied = deepcopy(dict(candidate))
        if identity in positions_by_identity:
            merged[positions_by_identity[identity]] = copied
        else:
            positions_by_identity[identity] = len(merged)
            merged.append(copied)
    return deepcopy(merged)


def _candidate_admission_item(
    *,
    payload: Mapping[str, Any],
    source_descriptor: Any,
    request_scope: Any,
) -> dict[str, Any]:
    copied_payload = deepcopy(dict(payload))
    if not isinstance(source_descriptor, Mapping) or not isinstance(request_scope, Mapping):
        return {"envelope": {}, "payload": copied_payload}
    provider_id = source_descriptor.get("provider_id")
    source_class = source_descriptor.get("source_class")
    source_instance = source_descriptor.get("source_instance")
    if not all(isinstance(value, str) for value in (provider_id, source_class, source_instance)):
        return {"envelope": {}, "payload": copied_payload}
    candidate_source_key = copied_payload.get("id")
    if (
        not isinstance(candidate_source_key, str)
        or not 1 <= len(candidate_source_key) <= 256
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", candidate_source_key) is None
    ):
        return {"envelope": {}, "payload": copied_payload}
    try:
        payload_digest = canonical_payload_digest(copied_payload)
        scope_material = canonical_payload_digest(
            {field: request_scope.get(field) for field in ("project", "workspace", "namespace")}
        )
    except (TypeError, ValueError):
        payload_digest = "sha256:" + ("0" * 64)
        scope_material = "invalid-scope"
    identity_material = f"{provider_id}|{source_instance}|{candidate_source_key}"
    candidate_id = candidate_source_key
    request_material = f"{identity_material}|{scope_material}|{payload_digest}"
    request_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"request|{request_material}"))
    envelope = {
        "provider_id": provider_id,
        "source_class": source_class,
        "source_instance": source_instance,
        "candidate_id": candidate_id,
        "project": request_scope.get("project"),
        "workspace": request_scope.get("workspace"),
        "namespace": request_scope.get("namespace"),
        "capabilities": ["READ_CANDIDATE"],
        "payload_digest": payload_digest,
        "request_id": request_id,
    }
    return {"envelope": envelope, "payload": copied_payload}


def _non_negative_int(value: Any, default: int) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default
