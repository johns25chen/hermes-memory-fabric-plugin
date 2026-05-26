"""Small local registry shim for standalone Memory Fabric tool wrappers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from threading import RLock
from typing import Any, Callable


@dataclass(frozen=True)
class ToolEntry:
    name: str
    toolset: str
    schema: dict[str, Any]
    handler: Callable[..., Any]
    check_fn: Callable[..., Any] | None = None
    requires_env: list[str] | None = None
    is_async: bool = False
    description: str = ""
    emoji: str = ""
    max_result_size_chars: int | float | None = None
    dynamic_schema_overrides: Callable[..., Any] | None = None


class LocalToolRegistry:
    """Minimal registry API used by copied tool modules and tests."""

    def __init__(self) -> None:
        self._entries: dict[str, ToolEntry] = {}
        self._lock = RLock()

    def register(
        self,
        *,
        name: str,
        toolset: str,
        schema: dict[str, Any],
        handler: Callable[..., Any],
        check_fn: Callable[..., Any] | None = None,
        requires_env: list[str] | None = None,
        is_async: bool = False,
        description: str = "",
        emoji: str = "",
        max_result_size_chars: int | float | None = None,
        dynamic_schema_overrides: Callable[..., Any] | None = None,
        override: bool = False,
    ) -> None:
        entry = ToolEntry(
            name=name,
            toolset=toolset,
            schema=schema,
            handler=handler,
            check_fn=check_fn,
            requires_env=requires_env or [],
            is_async=is_async,
            description=description or str(schema.get("description", "")),
            emoji=emoji,
            max_result_size_chars=max_result_size_chars,
            dynamic_schema_overrides=dynamic_schema_overrides,
        )
        with self._lock:
            self._entries[name] = entry

    def get_entry(self, name: str) -> ToolEntry | None:
        with self._lock:
            return self._entries.get(name)

    def get_tool_names_for_toolset(self, toolset: str) -> list[str]:
        with self._lock:
            return sorted(
                entry.name for entry in self._entries.values() if entry.toolset == toolset
            )

    def get_definitions(self, toolsets: set[str] | None = None) -> list[dict[str, Any]]:
        with self._lock:
            entries = list(self._entries.values())
        definitions = []
        for entry in entries:
            if toolsets is not None and entry.toolset not in toolsets:
                continue
            definitions.append({"type": "function", "function": dict(entry.schema)})
        return definitions


registry = LocalToolRegistry()


def tool_error(message: Any, **extra: Any) -> str:
    payload = {"error": str(message)}
    payload.update(extra)
    return json.dumps(payload, ensure_ascii=False)

