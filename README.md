# Hermes Memory Fabric Plugin

This repository is the standalone plugin extraction of the in-tree Hermes Memory Fabric prototype. The original prototype lived inside `hermes-agent`; this package is laid out so the memory provider and evidence-repair modules do not depend on being imported from the Hermes main repository.

## Install

Editable install from this directory:

```bash
cd /Users/han/hermes-memory-fabric-plugin
python3 -m pip install -e .
```

With `uv`:

```bash
cd /Users/han/hermes-memory-fabric-plugin
uv pip install -e .
```

Hermes plugin-directory install:

```bash
mkdir -p ~/.hermes/plugins/memory
ln -s /Users/han/hermes-memory-fabric-plugin ~/.hermes/plugins/memory/memory-fabric
```

Copying the directory to `~/.hermes/plugins/memory/memory-fabric` also works.

## v0.1 Behavior

Version 0.1 is intentionally read-only. The provider lifecycle is available, but it does not perform durable memory writes, does not invoke a real token write executor, and does not expose Memory Fabric tools to the model by default.

`MemoryFabricProvider.get_tool_schemas()` returns an empty list in v0.1. The copied tool modules use a local registry shim for standalone tests and future adapter work, but the provider does not publish those tools until the standalone adapter boundary is reviewed.

## Layout

- `src/hermes_memory_fabric/`: extracted Memory Fabric and evidence-repair modules.
- `src/hermes_memory_fabric/provider.py`: Hermes-compatible provider wrapper.
- `src/hermes_memory_fabric/tools/`: callable tool wrappers using the local registry shim.
- `tests/`: extracted and standalone-scoped tests.
- `benchmarks/hermes_memory_bench/`: copied benchmark fixture.
- `docs/share-hermes-memory-with-codex-openclaw.md`: copied guide when present in the prototype branch.

## Limitations

- No provider tools are exposed in v0.1.
- Registry registration is local to this package and does not import Hermes core `tools.registry`.
- Hermes core provider-manager and third-party provider tests are copied for reference but excluded from standalone pytest collection.

