# Codex Task Summary Ingestion Dry Run

v1.3.0 adds a deterministic dry-run pipeline that turns structured Codex task
summaries into local Memory Fabric candidate JSONL records.

## Why Codex Task Summaries Come First

Completed Codex task summaries are the smallest useful ingestion source after
the v1.1.0 JSONL adapter. They already contain explicit project intent, changed
files, validation evidence, boundary limits, version notes, and results. That
makes them good candidate input without reading Hermes graph storage, session
logs, operation ledgers, write proposals, or external services.

## What It Proves

The dry run proves that the standalone plugin can:

- parse structured local task summaries;
- preserve validation evidence and boundary limitations as candidate content;
- generate deterministic candidate ids and JSONL output;
- mark every generated candidate as read-only, proposal-governed, and dry-run;
- feed the generated JSONL back through v1.1.0 `candidate_jsonl_path` and
  `MemoryFabricProvider.prefetch(...)`.

## What It Does Not Prove

This does not implement durable memory ingestion. It does not modify Hermes
Agent, implement SQLite, write to `~/.hermes/memory`, write graph state, create
operation-ledger events, create write proposals, call a real model, use the
network, call executors, mutate auth/config, or expose provider tools.

## Dry-Run Safety

Default behavior is dry-run. If `--output` is omitted, JSONL is printed to
stdout. If `--output` is provided, the CLI writes only to that explicit path. It
does not create or update `~/.hermes` by default.

Every candidate has governance flags:

```json
{"read_only":true,"proposal_governed":true,"dry_run":true}
```

The generated governance metadata also records false values for Memory Fabric
write, graph, token, approval-audit, operation-ledger, executor, and provider
tool surfaces.

## Candidate Schema

Each generated JSONL object includes:

- `id`: deterministic id derived from source, project id, candidate kind, and
  grounded content.
- `content`: explicit summary section text only.
- `project_id`: CLI project id, default `hermes-memory-fabric`.
- `entity_ids`: currently the project id.
- `source`: CLI source label, default `codex-task-summary`.
- `provenance`: dry-run ingestion metadata, input hash, and source section line
  ranges.
- `risk_level`: `low` by default, `high` when grounded content includes terms
  such as auth, token, credential, write, approval, executor, deletion, or
  migration.
- `governance`: read-only, proposal-governed, dry-run policy flags.
- `created_at`: deterministic dry-run timestamp.
- `tags`: `codex-task-summary`, `dry-run`, candidate kind, and source section
  tags.

## Example Command

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/ingest_codex_task_summary_dry_run.py \
  --input benchmarks/candidate_ingestion/fixtures/v13_codex_task_summary.txt \
  --output /tmp/codex-task-summary-candidates.jsonl \
  --print-summary
```

Omit `--output` to print JSONL to stdout:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/ingest_codex_task_summary_dry_run.py \
  --input benchmarks/candidate_ingestion/fixtures/v13_codex_task_summary.txt
```

## Using The Output With v1.1 JSONL Loading

Use the generated file as the existing v1.1 `candidate_jsonl_path`:

```python
from hermes_memory_fabric import MemoryFabricProvider

provider = MemoryFabricProvider(
    runtime_config={
        "project_scope": "hermes-memory-fabric",
        "candidate_jsonl_path": "/tmp/codex-task-summary-candidates.jsonl",
        "candidate_jsonl_required_fields": ["id", "content"],
    }
)

context = provider.prefetch("Codex task summary ingestion dry run")
```

The provider still performs the existing bounded read, relevance selection,
risk gating, context budget enforcement, and no-provider-tool checks.
