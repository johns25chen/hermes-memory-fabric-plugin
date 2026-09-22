# Ordinary handoff record protocol (operation extension, 1.4)

This is the current contract for the new `ordinary-handoff` CLI operation only.
It does not revise historical R8/R9 contracts or closure decisions. Package
version stays 6.16.0. Existing `continuity` operations retain their 1.3 envelopes,
validation rules, receipts and mandatory correction/revocation workflows.

## Scope and meaning

`R10_ORDINARY_HANDOFF_RECORD_VALIDATION` validates one caller-provided record.
It reuses candidate validation, provider/federation admission, security policy,
payload binding and caller authority attestation. It never composes active
context, retrieves prior sessions, writes storage, calls a model or network, or
permits continuation. Even a successfully accepted record grants **no candidate
use authority**. Unknown events are retained as unknown, never treated as evidence
of safety or absence. A revoked record cannot become usable via this operation.

Authority and event facts are caller declarations, not independent authentication
of real-world events. A valid record is not evidence of task completion, value,
efficiency, automatic memory recovery or R10 acceptance. Synthetic tests are not
real-user pilot evidence.

## Input record

All top-level fields below are required; unrecognized fields are rejected.
The candidate is an existing v1.3.1 proposal-governed, read-only, low-risk candidate
with id/content/project_id/entity_ids/source/source_id/provenance/risk_level/
governance/created_at/tags. Its project must be CIVILIZATION-CORE, provenance must
be nonempty, and any explicit project/workspace/namespace fields must match scope.
Existing candidate validation and fixed LOCAL_CALLER admission apply before any
review/event processing. BLOCK or REVIEW never proceeds to event processing.

```json
{
  "scope": {
    "project": "CIVILIZATION-CORE",
    "workspace": "/workspace/r7-project-continuity",
    "namespace": "r7-value-signal"
  },
  "input_classification": "NON_SENSITIVE",
  "candidate": {"...": "supply the complete approved candidate, not this placeholder"},
  "human_review": {"status": "NOT_PROVIDED"},
  "correction": {"status": "NOT_OCCURRED"},
  "revocation": {"status": "NOT_OCCURRED"},
  "measurement": {"status": "NOT_MEASURED"},
  "value_evaluation": {"status": "NOT_PROVIDED"}
}
```

Use SYNTHETIC only for synthetic material. Classification does not override
source, human decision, scope or candidate validation. The example is a shape,
not executable input: replace the candidate placeholder with actual approved data.

| Field | States and exact additional fields |
|---|---|
| human_review | NOT_PROVIDED: none. PROVIDED: `outcome`, nonblank `rationale`; outcome uses the existing supported review outcomes. |
| correction | NOT_OCCURRED or UNKNOWN: none. OCCURRED: `corrected_outcome`, nonblank `rationale`; requires PROVIDED review and a supported outcome different from that review. |
| revocation | NOT_OCCURRED or UNKNOWN: none. OCCURRED: `target`, `target_candidate_id`, nonblank `rationale`; requires PROVIDED review and known correction status. |
| measurement | NOT_MEASURED: none. MEASURED: nonnegative finite numeric `seconds` (not boolean), `caller_observed: true`. |
| value_evaluation | NOT_PROVIDED: none. PROVIDED: strictly boolean `worthwhile`. |

No extra facts may accompany an absent/unknown state. Missing mandatory facts,
unsupported states and contradictory combinations fail closed. Zero is allowed
only as an explicitly reported measured value; false is allowed only as an
explicit negative evaluation. Neither is a missing-value default.

For revocation, `target_candidate_id` must equal this record's candidate id.
`target` must be CORRECTION when correction OCCURRED, otherwise HUMAN_REVIEW
when correction NOT_OCCURRED. UNKNOWN correction cannot establish the current
revocation target. The reference denotes the single validated review/correction
for this candidate **inside this bound record**; it is not a persistent record id
or a claim of independently authenticated historical lineage. A caller cannot
revoke an arbitrary external record through this mode.

Provided reviews reuse the governed learning slice and human-review validator;
occurred corrections reuse the existing correction constructor/validator. A
revocation of a correction uses the existing revocation validation. A standalone
revocation references the validated original review, without manufacturing a
correction. All resulting processing is in memory and record-only, and no event
can grant application/continuation rights. A review conclusion such as rejection
is an observed fact; it is not reinterpreted as approval to use the candidate.

## Binding and security envelope

New operation identity: `R10_ORDINARY_HANDOFF_RECORD_VALIDATION`.
New envelope and attestation version: `1.4`. Old operations still require `1.3`;
versions and operation identities are not interchangeable.

The canonical payload is exactly:

```python
payload = {
    "operation": "R10_ORDINARY_HANDOFF_RECORD_VALIDATION",
    "project_id": "CIVILIZATION-CORE",
    "operator": "FOUNDER-OPERATOR",
    "workspace": "/workspace/r7-project-continuity",
    "record": record,
    "confirm_ordinary_handoff": True,
}
```

Use the existing canonical JSON convention: `json.dumps(payload, sort_keys=True,
separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')` and
SHA256 hex. The digest includes all candidate content, scope and observation
fields; changing any requires rebinding. `build_handoff_payload` is the production
helper. JSON must have no duplicate keys or nonfinite constants.

The envelope has the existing common fields plus mandatory string `workspace`:

```python
envelope = {
    "schema_name": "GOVERNED-MEMORY-SECURITY-DECISION-ENVELOPE",
    "version": "1.4",
    "operation": "R10_ORDINARY_HANDOFF_RECORD_VALIDATION",
    "request_reference": "r8-request:" + uuid.uuid4().hex,
    "payload_binding_sha256": hashlib.sha256(canonical_payload_bytes).hexdigest(),
    "project_id": "CIVILIZATION-CORE",
    "namespace": "R7_PROJECT_CONTINUITY",
    "workspace": "/workspace/r7-project-continuity",
    "operator_role": "FOUNDER-OPERATOR",
    "requested_effect": "READ_ONLY_NON_PERSISTENT_TERMINAL_ASSESSMENT",
    "security_classification": record["input_classification"],
    "security_classification_source": "CALLER_DECLARATION",
    "source_trust": "LOCAL_CALLER_PROVIDED",
    "source_lineage_class": "CALLER_SUBMISSION",
    "human_decision": "APPROVE_READ_ONLY_EXECUTION",
}
# Only use this declaration when the actual owner has authorized this execution.
envelope["authority_attestation"] = {
    **envelope,
    "attestation_type": "CALLER_AUTHORITY_ATTESTATION",
    "attestation_version": "1.4",
    "attested": True,
}
```

No measurement_scope/baseline_measurement_scope fields belong to this new
operation. No comparative benefit is inferred. Envelope namespace
R7_PROJECT_CONTINUITY identifies the governance operation; record namespace
r7-value-signal identifies the existing fixed candidate-admission scope. Both
are checked, not substituted for each other. The mandatory CLI workspace-root
is this **logical admission workspace**, not an output directory or permission
to read that directory. The operation does not create it. Evidence should be
saved separately by the caller in an authorized directory.

Inherited rules are unchanged: sensitive or unknown source data BLOCK; provider
or federated sources require REVIEW; denied execution BLOCK; authority, operation,
classification and payload mismatches BLOCK. There is no new persistence authority.

## CLI and receipt

After creating genuine `record.json` and `envelope.json`, the caller can invoke
this shape from the repository with its existing environment (not an automatic
pilot authorization):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m hermes_memory_fabric.p4_m0_subspace_operator ordinary-handoff \
  --workspace-root /workspace/r7-project-continuity \
  --project-id CIVILIZATION-CORE --operator FOUNDER-OPERATOR \
  --record-json "$(cat /approved/evidence/record.json)" \
  --security-envelope-json "$(cat /approved/evidence/envelope.json)" \
  --confirm-ordinary-handoff
```

Paths are placeholders. JSON arguments can be visible to local processes; use
only authorized material. This command loads the supplied JSON strings and does
not read candidate source paths. Legacy flags are not accepted in this command.

Exit 0 means ordinary-handoff-record-accepted and record_accepted=true only.
The fixed success projection contains security_decision, sanitized_receipt,
correction_status, revocation_status, measurement_status, value_evaluation_status,
terminal/non_authoritative/non_applied/non_persisted=true;
candidate_use_authorized/continuation_authorized/benefit_inference_allowed and
all automatic_* flags=false. It does not include content, source text, rationale,
raw durations, worthwhile values, task_completed or a value assessment. Actual
observations remain in the caller's bound input, not copied into the receipt.
The receipt is not a signature, encryption or replay protection.

Exit 2 means argument/JSON/envelope or security BLOCK; exit 3 means REVIEW;
exit 1 means rejected record or downstream validation failure. Failures produce
only fixed, minimized error fields on stderr and no success stdout. No successful
product result is inferred from a wrapper exit. This implementation does not
perform a real pilot, independent review, R10 closure or Checkpoint B transition.
