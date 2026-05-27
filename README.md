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

## Hermes Integration

Hermes memory provider runtime loads providers through its directory-based
`plugins.memory` loader. Install the v0.8.0 shim after installing this package:

```bash
python scripts/install_memory_fabric_shim.py
```

Then run the no-model smoke:

```bash
PYTHON=/Users/han/.hermes/hermes-agent/.venv/bin/python bash scripts/smoke_memory_fabric_hermes.sh
```

See [docs/HERMES_INTEGRATION.md](docs/HERMES_INTEGRATION.md) for the loader
details, optional real chat smoke, and rollback instructions.

## v0.9.0 Active Context Quality Harness

v0.9.0 adds a deterministic local harness for validating
`MemoryFabricProvider` active context packets. It proves bounded,
project-scoped, explainable context selection and rejection behavior without
network calls, real model calls, durable writes, graph writes, token writes,
approval-audit writes, operation-ledger writes, executor calls, or provider
tool exposure.

Run it with:

```bash
python scripts/run_active_context_quality_harness.py
```

See [docs/ACTIVE_CONTEXT_QUALITY_HARNESS.md](docs/ACTIVE_CONTEXT_QUALITY_HARNESS.md)
for JSON output, fail-threshold usage, fixture details, and the separate manual
Hermes chat smoke.

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

Hermes Memory Bench v0.2 adds the `v02` suite under
`benchmarks/hermes_memory_bench/`. It deterministically measures Recall Fusion
v2 selection and rejection quality, Subspace Index isolation, archived and
high-risk gating, temporal/conflict handling, explanation quality, and no-write
safety without network calls or durable memory side effects.

Civilization Core / Hermes Memory Fabric Active Context Composer v0.1 adds a
deterministic context-packet layer over Recall Fusion v2. It composes selected
subspace summaries and the highest-value selected memories into a bounded
`active_context_packet`, explains selected and rejected memories/subspaces, and
keeps the same read-only/no-write/no-token/no-executor/no-provider-tool policy
surface.

Provider Runtime Integration v0.1 wires Active Context Composer into
`MemoryFabricProvider` through provider-level `build_active_context(...)`,
`summarize_active_context(...)`, `explain_active_context(...)`, and
`validate_active_context(...)` methods. The provider keeps conservative local
defaults, exposes no tools by default, and performs no durable memory, graph,
token, approval-audit, config, ledger, or executor writes.

## Layout

- `src/hermes_memory_fabric/`: extracted Memory Fabric and evidence-repair modules.
- `src/hermes_memory_fabric/provider.py`: Hermes-compatible provider wrapper.
- `src/hermes_memory_fabric/tools/`: callable tool wrappers using the local registry shim.
- `tests/`: extracted and standalone-scoped tests.
- `benchmarks/hermes_memory_bench/`: deterministic smoke and v0.2 benchmark fixtures.
- `benchmarks/active_context_quality/`: deterministic v0.9 active context quality fixtures.
- `docs/share-hermes-memory-with-codex-openclaw.md`: copied guide when present in the prototype branch.

## Limitations

- No provider tools are exposed in v0.1.
- Registry registration is local to this package and does not import Hermes core `tools.registry`.
- Hermes core provider-manager and third-party provider tests are copied for reference but excluded from standalone pytest collection.
