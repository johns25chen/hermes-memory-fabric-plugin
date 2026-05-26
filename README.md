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

Civilization Core / Memory Fabric Subspace Index v0.1 adds deterministic,
read-only project, agent, risk, archive, global, and custom memory domains.
The index validates subspace descriptors and registries, resolves subspaces by
id, selects only context-relevant subspaces, and reports explicit no-write,
no-graph-write, no-token-write, no-executor, and no-provider-tool policy flags.

Hermes Memory Fabric Recall Fusion v2 adds a read-only, deterministic recall
layer over Subspace Index. `fuse_memory_retrieval_v2(...)` activates governed
subspaces when a registry is provided, boosts memories that match selected
subspace ids or project/agent scopes, and explains selected and rejected
memories. Public helpers `explain_memory_retrieval_v2_result(...)` and
`summarize_memory_retrieval_v2_result(...)` expose selection reasons, rejected
subspaces, score components, and no-write/no-executor policy flags. v2 uses
local lexical scoring only; it does not call external APIs, write durable
memory, write graph state, write token files, write approval audits, or expose
provider tools.

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
