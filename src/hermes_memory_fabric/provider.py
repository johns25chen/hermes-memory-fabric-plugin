"""Hermes-compatible Memory Fabric provider wrapper."""

from __future__ import annotations

from typing import Any

try:
    from agent.memory_provider import MemoryProvider
except Exception:  # pragma: no cover - standalone test fallback
    from .memory_provider import MemoryProvider


class MemoryFabricProvider(MemoryProvider):
    """Read-only Memory Fabric provider shell for standalone plugin loading."""

    name = "memory-fabric"

    def __init__(self) -> None:
        self.session_id = ""
        self.hermes_home = ""
        self.initialized_kwargs: dict[str, Any] = {}

    def is_available(self) -> bool:
        return True

    def initialize(self, session_id: str, **kwargs: Any) -> None:
        self.session_id = session_id
        self.hermes_home = str(kwargs.get("hermes_home", ""))
        self.initialized_kwargs = dict(kwargs)

    def system_prompt_block(self) -> str:
        return (
            "Memory Fabric is available in read-only standalone plugin mode. "
            "It preserves governed recall and evidence-repair boundaries, "
            "does not write durable memory, and does not invoke token write executors."
        )

    def prefetch(self, query: str, *, session_id: str = "") -> str:
        return ""

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


def register(ctx: Any) -> None:
    """Register the Memory Fabric provider with a Hermes plugin context."""

    ctx.register_memory_provider(MemoryFabricProvider())

