# JSONL Candidate Source

v1.1.0 adds a conservative local JSONL candidate source for
`MemoryFabricProvider.prefetch(...)`.

## Why JSONL Is The v1.1.0 Source

JSONL is the smallest persistent source that can prove the provider can load
candidate records from disk while keeping the standalone plugin boundary
read-only. It avoids coupling v1.1.0 to Hermes graph storage, operation ledgers,
write proposals, session logs, SQLite schema design, or any external service.

## What It Proves

The JSONL source proves that `MemoryFabricProvider` can:

- read bounded candidate records from an existing local file;
- merge them with explicit runtime candidates;
- deduplicate by `id`, preferring explicit runtime candidates over JSONL;
- reuse the existing `prefetch -> build_active_context -> compact_context_text`
  path;
- keep provider tools hidden with `get_tool_schemas() == []`.

The existing active context composer still decides relevance and safety. Project
scope, archived-memory exclusion, unsafe-governance rejection, high-risk gating,
memory limits, and context budget limits continue to happen after loading.

## What It Does Not Prove

The JSONL source does not prove end-to-end model behavior or answer quality. It
does not implement SQLite, read the Hermes graph DB, read operation ledgers, read
write proposals, read session logs, write durable memory, write graph state,
write token files, write approval audits, mutate auth/config, call executors, or
call a real model.

## Format Requirements

Configure the provider with `runtime_config`:

```python
MemoryFabricProvider(
    runtime_config={
        "project_scope": "hermes-memory-fabric",
        "candidate_jsonl_path": "/path/to/candidates.jsonl",
        "candidate_jsonl_max_lines": 1000,
        "candidate_jsonl_max_bytes": 1048576,
        "candidate_jsonl_required_fields": ["id", "content"],
        "candidate_jsonl_ignore_invalid_lines": True,
    }
)
```

Each non-blank line must be one JSON object. Blank lines are ignored. Invalid
lines are ignored by default. Missing files, directories, remote URLs, unreadable
files, or exhausted zero limits return no JSONL candidates.

Example line:

```json
{"id":"v11-selected-project","content":"Hermes v1.1 JSONL candidate source selected project memory.","project_id":"hermes-memory-fabric","entity_ids":["hermes-memory-fabric"],"created_at":"2026-05-27T00:00:00Z","source":"fixture","provenance":"fixture:v11:selected-project","risk_level":"low","governance":{"read_only":true,"proposal_governed":true}}
```

## Safety Boundary

The provider only opens an existing local JSONL file for bounded reads. It does
not create the file, write to the file, mutate `~/.hermes`, use the network, call
a model, expose tools, write durable memory, write graph state, write token
files, write approval audits, write operation ledgers, call executors, or mutate
auth/config.

## SQLite Is Deferred

SQLite is intentionally deferred. v1.1.0 is only the adapter proof that a
persistent candidate source can feed the already-reviewed active context path.
Schema ownership, migration policy, locking, provenance, and Hermes graph
boundaries remain separate design work.
