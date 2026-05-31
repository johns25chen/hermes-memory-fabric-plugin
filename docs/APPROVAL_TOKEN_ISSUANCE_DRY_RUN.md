# v1.9.0 Approval Token Issuance Dry Run

v1.9.0 adds a deterministic dry-run layer after the v1.8.0 Approval Intent
Review Gate Dry Run. It accepts a v1.8 approved review outcome candidate and
returns an approval token issuance dry-run candidate.

## Why It Follows v1.8

v1.8 records the human review outcome for a v1.7 approval intent. Its
`approved` state means the reviewer decision was represented safely and the
source no-write boundary held. It still does not issue a token.

v1.9 is the next dry-run step: it checks that the v1.8 review outcome is exactly
the approved, no-token, no-write outcome expected before any later token
issuance design can be considered.

## Token Issuance Dry-Run Candidate

A token issuance dry-run candidate is an in-memory report object with:

- a stable `token_draft_id`;
- a stable `token_intent_id`;
- `token_kind == "approval_token_issuance_draft_candidate"`;
- issuer and issuance reason metadata;
- source review gate version, status, outcome id, reviewer decision, and next
  step;
- a `required_next_step`;
- explicit no-token, no-write, and no-executor flags;
- a full `source_review_outcome_snapshot`.

It is only a draft candidate. It is not persisted, not authoritative, and not a
usable approval token.

## Statuses

`ready` means the source review outcome is version `1.8.0`, has
`review_gate_status == "approved"`, has `reviewer_decision == "approve"`, has
`required_next_step == "manual_review_outcome_recorded_no_token_issued"`, keeps
all source no-write flags safe, and exposes no provider tools.

`locked` means the source is missing required keys, is not version `1.8.0`, is
not approved, was not an approve decision, has the wrong required next step, has
unsafe no-write flags, or exposes provider tools.

## Why Ready Still Does Not Issue A Token

`ready` only means the dry-run candidate is ready for a separate manual token
issuance review. It deliberately creates no token authority and sets
`required_next_step == "manual_token_issuance_review_required_no_token_created"`.

This separation keeps review recording, token drafting, and any future real
issuance boundary independent.

## Why Token Fields Remain Null

`approval_token_id` and `approval_token_value` remain `null` because v1.9 does
not mint or reserve real token identifiers, does not generate token strings,
and does not persist token material. The deterministic ids in v1.9 identify
only the dry-run draft and intent candidate.

## Real Token Issuance Is Later And Separate

Real token issuance would need its own governed design, file policy, audit
model, authority boundary, and execution separation. v1.9 intentionally does
not reuse older token, review, executor, proposal, ledger, bridge, provider
tool, model, or network paths.

## Relation To v1.5, v1.6, v1.7, And v1.8

v1.5.0 creates proposal dry-run previews from read-only Memory Fabric
candidates. It does not create real proposals.

v1.6.0 audits executor, token, ledger, write-lock, bridge, and provider-tool
surfaces before approval-adjacent layers can proceed.

v1.7.0 converts a safe v1.5 preview plus passing v1.6 audit into an approval
intent candidate.

v1.8.0 converts a ready v1.7 intent plus an explicit reviewer decision into a
review outcome candidate. Its approved status still creates no token.

v1.9.0 converts an approved v1.8 review outcome into a token issuance dry-run
candidate. It still creates no usable token and writes no state.

## CLI

Stdout JSON:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/issue_approval_token_dry_run.py \
  --input /tmp/approval-intent-review-outcome-dry-run.json
```

Explicit output path:

```bash
PYTHONPATH="$PWD/src:$PWD" python scripts/issue_approval_token_dry_run.py \
  --input /tmp/approval-intent-review-outcome-dry-run.json \
  --issuer manual-human-review \
  --reason "reviewed for token issuance draft" \
  --output /tmp/approval-token-issuance-dry-run.json \
  --print-summary
```

The CLI writes only to an explicit `--output` path when provided and refuses
outputs under `HERMES_HOME` or `~/.hermes`.

## No-Write Guarantees

The dry run sets:

- `dry_run == true`;
- `approval_token_issued == false`;
- `approval_token_id == null`;
- `approval_token_value == null`;
- `creates_usable_token == false`;
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

It does not create usable tokens, token files, proposal files, operation ledger
records, approval audit records, memory, graph/config/SQLite state, executor
actions, provider tools, model calls, network calls, or writes under Hermes
home.
