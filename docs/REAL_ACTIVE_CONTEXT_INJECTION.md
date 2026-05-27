# Real Active Context Injection

v1.0.0 implements the standalone provider side of Hermes real active context
injection.

## Hermes Injection Path

Hermes already owns the runtime injection pipeline:

1. `agent.memory_manager.MemoryManager.prefetch_all(query)` calls each memory
   provider through `provider.prefetch(query, session_id=session_id)`.
2. Non-empty provider prefetch text is merged into Hermes
   `_ext_prefetch_cache`.
3. `conversation_loop` injects `_ext_prefetch_cache` into the current user
   message at API-call time.
4. The injected memory context is ephemeral. It is not persisted to the
   session database.

## Why v1.0.0 Implements `prefetch`

Before v1.0.0, `MemoryFabricProvider.prefetch(...)` returned an empty string.
That meant Hermes could load and activate the Memory Fabric provider, but the
real injection path had no active Memory Fabric context to inject.

v1.0.0 routes `prefetch(...)` through the existing read-only active context
composer:

1. Runtime memory candidates are supplied in memory only.
2. `prefetch(...)` calls `MemoryFabricProvider.build_active_context(...)`.
3. The active context packet is validated.
4. Valid, non-empty `packet["compact_context_text"]` is returned to Hermes.
5. Missing candidates, invalid packets, and exceptions fail closed to `""`.

## What This Proves

The v1.0.0 contract proves that the standalone plugin can produce bounded,
deterministic active context text for Hermes' real user-message injection path.
It also proves that provider tools remain hidden:

```python
MemoryFabricProvider().get_tool_schemas() == []
```

The focused tests and smoke script verify matching candidate selection,
unrelated and rejected memory exclusion, archived-memory rejection by default,
high-risk gating, context budget enforcement, defensive copying, and no provider
runtime file writes.

## What This Does Not Prove

This does not prove end-to-end model behavior, answer quality, or whether a
live model uses the injected context in a specific way.

It also does not add persistent storage, graph writes, token writes, approval
audit writes, config mutation, network access, executor calls, or provider tool
exposure.

## No Real Model Call By Default

The default validation path is local and deterministic:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/smoke_real_active_context_injection.py
```

The smoke instantiates `MemoryFabricProvider` with runtime candidates, calls
`provider.prefetch(...)`, asserts selected context appears, asserts unrelated
and rejected context does not appear, and asserts provider tools remain empty.
It does not call a real model.

## Manual Real Chat Smoke

A manual Hermes real chat smoke remains separate. Use it only when explicitly
checking the full Hermes runtime and model-call path. The standalone plugin
contract intentionally keeps its default proof local, read-only, and no-model.
