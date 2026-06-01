# v2.0.0 Token Authority Boundary Contract Dry Run

v2.0.0 adds a deterministic dry-run layer after the v1.9.0 Approval Token
Issuance Dry Run. v1.9 proves that an approved review outcome can become a
token issuance draft candidate without creating any token. v2.0 takes that
draft candidate and defines the authority boundary that a future real token
system would have to satisfy before any real issuance can exist.

`ready` still does not issue a token. It only means the v1.9 source candidate
is safe, the requested authority scope is valid, expiry is positive, and future
revocation and audit boundaries are mandatory. The report contains no token
value, no token id, and no usable credential.

## Token Authority Boundary

The token authority boundary is a declarative contract candidate. It describes
what future token authority may define, and what this dry run must forbid.

Allowed future authority actions are limited to:

- `define_token_scope`
- `define_token_expiry`
- `define_token_revocation`
- `define_token_audit_requirements`
- `define_executor_boundary`
- `define_ledger_boundary`

Forbidden future authority actions are:

- `issue_real_approval_token`
- `create_token_value`
- `write_token_file`
- `append_operation_ledger`
- `invoke_real_executor`
- `apply_memory_proposal`
- `write_memory`
- `write_graph`
- `write_config`
- `write_sqlite`
- `write_approval_audit`
- `expose_provider_tools`

## Boundaries

Scope boundary: `authority_scope` must be a non-empty list of non-empty strings.
The default is `["memory_proposal_apply_preview_only"]`.

Expiry boundary: `expiry_seconds` must be a positive integer. The default is
`900`.

Revocation boundary: `revocation_required` must be `true`. A future real token
system must define revocation before issuance can be considered.

Audit boundary: `audit_required` must be `true`. This dry run does not write
approval audit files, but it requires future audit semantics to be defined.

Ledger boundary: `ledger_required` is always `true`, but this dry run never
appends an operation ledger entry. It only records that a future boundary is
required.

Executor boundary: `executor_boundary_required` is always `true`, but this dry
run never invokes or implements executor behavior. It only records that a future
executor boundary is required.

## Status Behavior

The result is `ready` only when the source v1.9 candidate is exactly safe:

- `version == "1.9.0"`
- `token_issuance_status == "ready"`
- `required_next_step == "manual_token_issuance_review_required_no_token_created"`
- no approval token was issued
- token id and token value are null
- no usable token is created
- all no-write flags remain false
- `provider_tools == []`
- authority scope, expiry, revocation, and audit inputs are valid

The result is `locked` for missing source keys, wrong source version or status,
wrong next step, unsafe token fields, unsafe no-write flags, provider tools,
empty or invalid scope, non-positive expiry, or disabled revocation/audit.

## Relationship To Earlier Dry Runs

v1.5 creates a candidate proposal preview from read-only candidates. v1.6 audits
executor surface lockdown. v1.7 creates an approval intent dry run. v1.8 records
a human review outcome dry run. v1.9 creates a token issuance draft candidate
without issuing a token. v2.0 defines the authority boundary contract candidate
that must be reviewed before a later, separate real token design can exist.

Real token issuance remains later and separate because this layer is only a
contract dry run. It does not sign, persist, issue, audit, execute, or apply
anything.

## No-Token / No-Write Guarantees

The v2.0 report always returns:

- `approval_token_issued == false`
- `approval_token_id == null`
- `approval_token_value == null`
- `creates_usable_token == false`
- `creates_real_proposal == false`
- `writes_proposal_files == false`
- `writes_operation_ledger == false`
- `writes_memory == false`
- `writes_graph == false`
- `writes_config == false`
- `writes_sqlite == false`
- `writes_token_files == false`
- `writes_approval_audit == false`
- `invokes_real_executor == false`
- `applies_proposals == false`
- `provider_tools == []`

The CLI writes JSON only to stdout by default. With `--output`, it writes only
to the explicit requested path and refuses outputs under `HERMES_HOME` or
`~/.hermes`.
