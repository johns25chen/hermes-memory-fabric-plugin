# v1.7.0 Approval Intent Dry Run

v1.7.0 adds a deterministic dry-run layer that converts a v1.5.0 Memory
Candidate Proposal Dry Run preview into an approval intent candidate for later
human review.

Approval Intent comes after v1.6.0 Executor Surface Lockdown Audit because the
intent layer is adjacent to approval, token, executor, ledger, and write
surfaces. Before creating an intent candidate, v1.7.0 calls the v1.6.0 static
audit as a read-only gate and requires `audit_status == "pass"`.

## What It Is

Approval Intent Dry Run is an in-memory report object with:

- a stable `approval_intent_id`;
- source v1.5 preview counts and version;
- `approval_intent_status` of `ready`, `locked`, or `rejected`;
- a compact v1.6 audit snapshot in `safety_summary`;
- explicit no-write and no-executor flags;
- a full `source_preview_snapshot` for review context.

`ready` means the source preview is v1.5.0, has at least one accepted preview,
has no write flags set, exposes no provider tools, and the v1.6 audit passes.

`locked` means the source preview is otherwise valid and the v1.6 audit passes,
but `accepted_count == 0`.

`rejected` means required source keys are missing, a source write flag is true,
provider tools are exposed, the source version is not v1.5.0, or the v1.6 audit
fails.

## What It Is Not

Approval Intent Dry Run is not approval token issuance. It does not create token
ids or token files.

It is not proposal creation. It does not call
`memory_fabric_bridge.create_memory_write_proposal`, create proposal records, or
write proposal files.

It is not ledger append. It does not append operation ledger records or approval
audit records.

It is not executor behavior. It does not invoke, implement, or plan a real write
executor action.

It is not durable memory mutation. It does not write memory, graph, config,
SQLite, audit, token, ledger, or proposal state, and it exposes no provider
tools.

## Relation To v1.5 And v1.6

v1.5.0 produces proposal dry-run previews from read-only Memory Fabric
candidates. v1.7.0 accepts that preview object as input and creates a reviewable
approval intent candidate only.

v1.6.0 audits the repository surface before v1.7.0 can mark an intent `ready`.
The audit remains read-only and must pass with no provider tools, no forbidden
write proposal calls, no forbidden write surfaces, no missing no-write flags,
and a passing v1.5 boundary check.

## CLI

Stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/create_approval_intent_dry_run.py \
  --input /tmp/memory-candidate-proposal-dry-run.json
```

Explicit output path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/create_approval_intent_dry_run.py \
  --input /tmp/memory-candidate-proposal-dry-run.json \
  --output /tmp/approval-intent-dry-run.json \
  --print-summary
```

The CLI writes only to an explicit `--output` path when provided and refuses
outputs under `HERMES_HOME` or `~/.hermes`.
