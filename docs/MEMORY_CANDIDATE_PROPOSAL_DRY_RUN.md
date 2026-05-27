# Memory Candidate Proposal Dry Run

v1.5.0 adds an isolated adapter that converts v1.3.1 Memory Fabric candidate
dicts into the existing Memory Block and proposal preview chain. It is a dry-run
only path: it creates in-memory preview objects and never creates real proposal,
ledger, token, audit, memory, graph, config, provider, network, or model side
effects.

## Why An Isolated Adapter

v1.3.1 candidate JSONL is intentionally simple: each row is a raw candidate
record with `id`, `content`, provenance, governance, risk, and tags. The
proposal/governance modules added earlier expect Memory Block chain objects, not
raw candidate dicts. Passing raw candidates directly to
`validate_memory_block_candidate` or proposal validators fails because required
Memory Block fields such as `block_type`, `status`, `version`, `policy`,
`mutation_policy`, and `direct_write_allowed` are absent.

The v1.5.0 adapter keeps that translation in one module:

`src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py`

This keeps v1.3.1 candidate ingestion separate from proposal preview plumbing
and avoids changing Hermes Agent or provider tool exposure.

## Why The Bridge Writer Is Not Called

`memory_fabric_bridge.create_memory_write_proposal` is not a dry-run helper. It
appends a proposal JSONL record and an operation-ledger event. v1.5.0 must prove
candidate-to-preview compatibility without durable writes, so the adapter never
imports or calls that function.

The result explicitly reports:

- `created_real_proposal: false`
- `writes_proposal_files: false`
- `writes_operation_ledger: false`
- `writes_memory: false`
- `writes_graph: false`
- `writes_config: false`
- `writes_sqlite: false`
- `writes_token_files: false`
- `writes_approval_audit: false`
- `applies_proposals: false`
- `provider_tools: []`

## Reused Modules

The adapter reuses only existing in-memory builders and validators:

- `memory_blocks`
- `memory_block_review_queue`
- `memory_review_decision_gate`
- `memory_proposal_draft_builder`
- `memory_proposal_governance_gate`
- `memory_governance_submission_packet`
- `memory_human_review_outcome_gate`
- `memory_real_proposal_creation_plan`
- `memory_real_proposal_dry_run`

The chain stops at `memory_real_proposal_dry_run`, which is still preview-only.

## Intentionally Not Touched

The v1.5.0 adapter intentionally does not call:

- `memory_fabric_bridge.create_memory_write_proposal`
- `memory_human_approval_token_*`
- `real_write_executor_*`
- `memory_real_proposal_write_lock_gate`
- provider tool exposure paths

The write-lock gate remains token-adjacent, so the minimum v1.5.0 path does not
need it.

## Safety Boundaries

Default behavior is dry-run only.

The adapter accepts low-risk candidates only by default. Non-allowed risk levels
are locked, so a high-risk candidate does not enter the Memory Block chain.

The adapter requires:

- `governance.dry_run == true`
- `governance.read_only == true`
- `governance.proposal_governed == true`

The adapter rejects candidates whose governance asserts any known real-write or
token/executor/provider side effect, including proposal-file writes, operation
ledger writes, memory writes, graph writes, token-file writes, approval-audit
writes, real proposal creation, proposal application, governance submission,
real token executor invocation, or provider tool exposure.

The adapter deep-copies candidate inputs and does not mutate caller-owned dicts.

## Schema Mapping

Accepted v1.3.1 candidates are mapped into Memory Block candidates as follows:

| v1.3.1 candidate field | Memory Block destination |
| --- | --- |
| `project_id` | `project_scope` |
| `content` | `content` |
| `id` | `source_fact_ids[0]` and metadata |
| `tags` | `metadata.tags` |
| `provenance` | `metadata.provenance` |
| `source` | `metadata.source` |
| `source_id` | `metadata.source_id` and `source_event_id` |
| `risk_level` | `metadata.risk_level` |
| `governance` | `metadata.governance` |

The adapter uses `block_type = "project_context"` for the minimum v1.5.0 path.
`status`, `version`, `policy`, `mutation_policy`, and `direct_write_allowed`
are supplied through `create_memory_block_candidate(...)` so they satisfy the
existing Memory Block validation contract.

## CLI Usage

Print the dry-run result to stdout:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/propose_memory_candidates_dry_run.py \
  --input /tmp/codex-task-summary-candidates.jsonl
```

Write the dry-run result only to an explicit output path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/propose_memory_candidates_dry_run.py \
  --input /tmp/codex-task-summary-candidates.jsonl \
  --output /tmp/memory-candidate-proposal-dry-run.json \
  --print-summary
```

The CLI refuses output paths under `HERMES_HOME` and never writes to
`~/.hermes` by default.

## What This Proves

v1.5.0 proves that low-risk v1.3.1 candidate JSONL can be converted into valid
Memory Block candidates and valid read-only proposal preview chain outputs. It
also proves that the adapter can reuse the existing in-memory proposal validators
without creating proposal files, operation ledger events, memory writes, graph
writes, token files, approval audit files, or provider tools.

## What This Does Not Prove

v1.5.0 does not prove real proposal creation, human approval token issuance,
write-lock eligibility, real write executor behavior, provider tool exposure,
Hermes Agent integration, model behavior, network behavior, or durable memory
application. Those remain intentionally outside this dry-run adapter.
