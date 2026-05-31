# v1.8.0 Approval Intent Review Gate Dry Run

v1.8.0 adds a deterministic dry-run review gate after v1.7.0 Approval Intent
Dry Run. It accepts a v1.7 approval intent object and one explicit reviewer
decision, then returns a review outcome candidate.

## Why It Follows v1.7

v1.7 produces the approval intent candidate from the v1.5 proposal dry-run
preview and the v1.6 executor-surface lockdown audit. v1.8 is the next read-only
step: it records how a reviewer would classify that intent without converting
the decision into authority to write.

The review gate only accepts v1.7.0 intents with `approval_intent_status ==
"ready"`, `human_review_required == true`, safe no-write flags, and
`provider_tools == []`. Anything else locks the review gate.

## Review Outcome Candidate

A review outcome candidate is an in-memory report object with:

- a stable `review_outcome_id`;
- `review_outcome_kind == "approval_intent_review_outcome_candidate"`;
- source approval intent version, status, id, and human-review marker;
- reviewer decision and optional reason;
- a `required_next_step`;
- explicit no-write and no-executor flags;
- a full `source_approval_intent_snapshot`.

It is only a candidate. It is not persisted, not authoritative, and not a token.

## Statuses

`approved` means the source v1.7 intent is valid and safe, the source status is
`ready`, human review is required, no source write flags are unsafe, no provider
tools are exposed, and the reviewer decision is `approve`.

`changes_requested` means the source v1.7 intent is valid and safe and the
reviewer decision is `request_changes`.

`rejected` means the source v1.7 intent is valid and safe and the reviewer
decision is `reject`.

`locked` means the source intent is missing required keys, is not version
`1.7.0`, is not `ready`, has unsafe no-write flags, exposes provider tools, has
an unexpected token id, lacks required human review, or the reviewer decision is
unsupported.

## Why Approved Does Not Issue A Token

`approved` is a review outcome candidate only. It confirms that a reviewer
decision can be represented safely and deterministically. It deliberately does
not grant write authority.

Approval token issuance is a later separate layer because token creation has a
different security boundary: it can create durable authority and must have its
own gate, audit trail, token file policy, and execution separation. v1.8 does
not call token modules, proposal writers, operation-ledger appenders, or
executors.

## Relation To v1.5, v1.6, And v1.7

v1.5.0 creates proposal dry-run previews from read-only Memory Fabric
candidates. It does not create real proposals.

v1.6.0 audits executor, token, ledger, write-lock, bridge, and provider-tool
surfaces before approval-adjacent layers can proceed.

v1.7.0 converts a safe v1.5 preview plus passing v1.6 audit into an approval
intent candidate.

v1.8.0 converts a ready v1.7 intent plus an explicit reviewer decision into a
review outcome candidate. It does not issue approval tokens or advance into
real execution.

## CLI

Stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/review_approval_intent_dry_run.py \
  --input /tmp/approval-intent-dry-run.json \
  --decision approve
```

Explicit output path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/review_approval_intent_dry_run.py \
  --input /tmp/approval-intent-dry-run.json \
  --decision request_changes \
  --reason "needs narrower scope" \
  --output /tmp/approval-intent-review-outcome-dry-run.json \
  --print-summary
```

The CLI writes only to an explicit `--output` path when provided and refuses
outputs under `HERMES_HOME` or `~/.hermes`.

## No-Write Guarantees

The review gate sets:

- `dry_run == true`;
- `approval_token_issued == false`;
- `approval_token_id == null`;
- `creates_real_proposal == false`;
- `writes_proposal_files == false`;
- `writes_operation_ledger == false`;
- `writes_memory == false`;
- `writes_graph == false`;
- `writes_config == false`;
- `writes_sqlite == false`;
- `writes_token_files == false`;
- `writes_approval_audit == false`;
- `invokes_real_executor == false`;
- `applies_proposals == false`;
- `provider_tools == []`.

It does not create proposals, append operation ledger records, invoke executors,
write memory, write graph/config/SQLite state, write token files, write approval
audit records, call models, make network calls, or write under Hermes home.
