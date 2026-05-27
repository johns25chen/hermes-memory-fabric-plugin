# Active Context Quality Harness

The v0.9.0 Active Context Quality Harness is a deterministic local check for
`MemoryFabricProvider` active-context behavior. It loads JSON fixtures from
`benchmarks/active_context_quality/fixtures/v09_cases.json`, calls the provider
methods below, and scores each case against explicit expectations:

- `build_active_context(...)`
- `explain_active_context(...)`
- `summarize_active_context(...)`
- `validate_active_context(...)`

## What It Proves

- Matching project memory is selected into bounded active context packets.
- Unrelated project memory is rejected and excluded from `compact_context_text`.
- Archived memory is rejected by default.
- Context budgets are respected.
- High-risk memory is rejected unless the case explicitly allows that risk.
- Temporal conflicts prefer current/newer memory over superseded memory.
- The active context policy remains read-only and reports no durable memory,
  graph, token, approval-audit, operation-ledger, config, executor, or provider
  tool writes.
- `MemoryFabricProvider.get_tool_schemas()` remains `[]`.

## What It Does Not Prove

- It does not call a real model.
- It does not validate generated assistant answer quality.
- It does not call the network.
- It does not test Hermes installation or directory-shim loading.
- It does not perform durable memory writes, graph writes, token writes,
  approval audit writes, operation-ledger writes, or executor calls.
- It does not prove real chat integration beyond the provider API boundary.

## Commands

Run the default human-readable harness:

```bash
python scripts/run_active_context_quality_harness.py
```

Print machine-readable JSON:

```bash
python scripts/run_active_context_quality_harness.py --json
```

Fail if the fixture does not score perfectly:

```bash
python scripts/run_active_context_quality_harness.py --fail-on-score-below 1.0
```

Use a custom fixture file:

```bash
python scripts/run_active_context_quality_harness.py --cases path/to/cases.json
```

## Optional Manual Hermes Chat Smoke

This is a separate manual integration check. It is not part of the harness, and
the harness does not call a real model by default.

```bash
hermes chat -Q -q "Reply exactly and only with this token: MEMORY_FABRIC_CHATQ_OK"
```
