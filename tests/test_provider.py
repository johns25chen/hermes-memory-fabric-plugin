from __future__ import annotations

import pytest

from hermes_memory_fabric import MemoryFabricProvider, register


def test_provider_v0_1_contract_is_read_only():
    provider = MemoryFabricProvider()

    assert provider.name == "memory-fabric"
    assert provider.is_available() is True

    provider.initialize("session-1", hermes_home="/tmp/hermes-test")

    assert provider.session_id == "session-1"
    assert provider.hermes_home == "/tmp/hermes-test"
    assert "read-only" in provider.system_prompt_block()
    assert provider.prefetch("anything") == ""
    assert provider.get_tool_schemas() == []
    assert provider.get_config_schema() == []
    provider.queue_prefetch("anything")
    provider.sync_turn("user", "assistant")
    provider.save_config({}, "/tmp/hermes-test")
    provider.shutdown()


def test_provider_does_not_handle_tools_in_v0_1():
    provider = MemoryFabricProvider()

    with pytest.raises(NotImplementedError):
        provider.handle_tool_call("memory_fabric_search", {})


def test_register_adds_memory_provider():
    class Context:
        def __init__(self) -> None:
            self.providers = []

        def register_memory_provider(self, provider) -> None:
            self.providers.append(provider)

    ctx = Context()

    register(ctx)

    assert len(ctx.providers) == 1
    assert isinstance(ctx.providers[0], MemoryFabricProvider)

