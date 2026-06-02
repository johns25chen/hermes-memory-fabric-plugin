# Governed Memory Approval Request Dry Run

v2.6.0 adds a deterministic approval-request envelope dry run for the v2.5.0
governed memory proposal review gate. It consumes
`run_governed_memory_proposal_review_gate_dry_run(proposal_path)` and builds
structured approval request envelopes only for decisions marked
`approve_candidate`.

Rejected, deferred, and risk-note decisions remain blocked source decisions.
They are reported in `blocked_decisions` and never become approval request
envelopes.

## Report Shape

`build_governed_memory_approval_request_dry_run(proposal_path)` returns a
JSON-serializable report containing:

- The source proposal path and SHA-256 digest.
- The consumed review-gate version and status.
- Decision, approve-candidate, approval-request, and blocked-decision counts.
- Deterministic `approval_request_id` values for each envelope.
- The source `proposal_id`, `decision_id`, `entry_key`, `target_surface`, and
  `review_reason` for each envelope.

For the current
`docs/CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md` fixture, the dry run
creates 15 approval request envelopes and keeps 3 blocked decisions out of the
approval path.

## Safety Boundary

This dry run creates envelopes only:

- It does not issue approval tokens.
- It does not create usable token values.
- It does not write Hermes memory.
- It does not mutate the Memory Graph.
- It does not append operation ledger entries.
- It does not write config or SQLite state.
- It does not invoke a real executor.
- It does not expose provider tools.
- It does not modify Hermes Agent.
- It does not use the network.

## Smoke

```bash
PYTHONPATH="$PWD/src:$PWD" python3 scripts/smoke_governed_memory_approval_request_dry_run.py
```

Expected output:

```text
governed_memory_approval_request_dry_run=passed
```
