# Civilization Core R8 Slice 3 Provider/Federation Boundary Contract

## 1. Contract identity and authority

```text
CONTRACT_ID=CIVILIZATION_CORE_R8_SLICE_3_PROVIDER_FEDERATION_BOUNDARY
CONTRACT_VERSION=1.0.0
STATUS=DESIGN-ONLY-PENDING-IMPLEMENTATION-AUTHORIZATION
PACKAGE_BASELINE_VERSION=6.16.0
LOCAL_PERSISTENCE_CONTRACT_VERSION=2.2.0
AUTOMATIC_SUCCESSOR_WORK=NONE
```

This document defines the admission contract for provider and federation candidates that have already entered the local process. It is a design artifact only. It does not implement or authorize production code, tests, networking, persistence, or any successor work.

The contract boundary is after a candidate has been loaded or supplied to the local process and before any candidate-source merge, retrieval/fusion, active-context composition, or persistence path. A candidate whose decision is `REVIEW` or `BLOCK` MUST NOT enter merge, retrieval, context composition, or persistence. `REVIEW` is quarantine for separate human review, never provisional admission.

This Slice does not implement network access, remote discovery, connectors, OAuth, credentials, synchronization, remote persistence, or cross-project sharing. It does not redefine Slice 1 or Slice 2. All durable local persistence remains independently governed by Slice 2 Local Persistence Contract 2.2.0.

## 2. Trust and source classification

Every admission envelope has exactly one `source_class`:

- `LOCAL_CALLER`: a candidate supplied through a locally trusted call path whose canonical source identity is injected by that path, outside the payload.
- `LOCAL_PROVIDER`: a candidate supplied by a provider whose identity and permitted capabilities are present in local configuration at evaluation time.
- `EXTERNAL_FEDERATED_CANDIDATE`: a candidate attributed to another system, provider, workspace, or trust domain whose external identity cannot be authenticated by Contract 1.0.0.

Four concepts MUST remain distinct:

1. A provenance claim inside the payload is untrusted content. It MAY be retained as data but MUST NOT establish or override identity, class, scope, capability, or trust.
2. A canonical source identity injected by a locally trusted call path is authoritative for `LOCAL_CALLER` only.
3. A provider identity matched against local configuration is authoritative only for the locally registered provider record and its configured bounds.
4. An external identity is unauthenticated in this Slice, even when its payload claims a known name or provenance.

Envelope fields that share names with payload fields are authoritative only when constructed by the trusted local boundary. Payload fields with those names MUST NOT be copied into authoritative envelope fields merely because they exist or match expected syntax.

An `EXTERNAL_FEDERATED_CANDIDATE` cannot receive `ALLOW` under Contract 1.0.0. A structurally valid external candidate may receive `REVIEW` only when a trusted local ingestion path or a local review-only provider descriptor supplies its canonical envelope while its external identity remains unauthenticated. An external candidate with neither basis receives `BLOCK`, as does an unknown, disabled, or unregistered claimed provider. Neither a plausible payload provenance claim nor a `REVIEW` result upgrades external identity to trusted identity.

## 3. Admission envelope

The admission evaluator receives an immutable request scope, an immutable current-batch context, an immutable local provider-registry snapshot, an immutable candidate payload, and an authoritative envelope constructed outside that payload.

The minimum authoritative envelope is:

| Field | Type and normalized form | Requirement |
| --- | --- | --- |
| `provider_id` | non-empty ASCII identifier string, 1-128 characters, lowercase, pattern `[a-z0-9][a-z0-9._-]*` | Required; injected by trusted local path or resolved from local registry, never trusted from payload. |
| `source_class` | exact enum string | One of the three classes in section 2. |
| `source_instance` | non-empty ASCII identifier string, 1-256 characters, pattern `[A-Za-z0-9][A-Za-z0-9._:/-]*` | Required canonical local instance locator; not a secret or credential. |
| `candidate_id` | non-empty ASCII identifier string, 1-256 characters, pattern `[A-Za-z0-9][A-Za-z0-9._:/-]*` | Required and stable within its source instance. |
| `project` | non-empty canonical string, 1-256 characters | Required for every candidate; exact request binding applies. |
| `workspace` | non-empty canonical absolute workspace identifier, 1-1024 characters | Required for every candidate; exact request binding applies. It identifies scope but grants no filesystem authority. |
| `namespace` | non-empty canonical string, 1-256 characters | Required for every candidate; exact request binding applies. |
| `capabilities` | immutable array of unique, lexicographically sorted enum strings | Required. Contract 1.0.0 recognizes only `READ_CANDIDATE`. |
| `payload_digest` | lowercase `sha256:` followed by exactly 64 hexadecimal characters | Required and verified against the immutable candidate payload. |
| `request_id` | lowercase canonical UUID string | Required; structural validation and current-batch uniqueness only in Contract 1.0.0. |

Text fields MUST already be in the canonical form above. The evaluator MUST NOT silently trim, case-fold, Unicode-normalize, resolve paths, or substitute defaults, because doing so can collapse distinct identities or scopes. Non-canonical input is malformed. Unknown envelope fields are rejected as malformed in 1.0.0 so that later fields cannot acquire accidental semantics.

The payload MUST be representable as JSON without NaN, infinity, duplicate object keys, or non-string object keys. `payload_digest` is computed from a versioned canonical JSON representation: UTF-8, object keys sorted by Unicode code point, no insignificant whitespace, JSON literals in lowercase, and strings/numbers serialized deterministically. The implementation MUST expose the canonicalization version in its internal decision binding and tests. If the loader has authoritative immutable raw bytes, it MAY use a separately versioned raw-byte digest mode, but a batch MUST use one declared mode and MUST NOT compare digests across modes.

The compound candidate identity is:

```text
(provider_id, source_instance, candidate_id)
```

`candidate_id` alone is never a federation-wide identity. A collision involving the same compound identity but different payload digests, scopes, source classes, or capabilities is blocking. The same bare `candidate_id` from different compound identities remains distinct and MUST NOT trigger replacement by bare ID during merge.

## 4. Scope and capability rules

The trusted request context supplies exact `project`, `workspace`, and `namespace` values. Admission requires equality of all three envelope fields to their request-context counterparts. The comparison is performed only after both sides have independently passed their canonical-form validation; no prefix, parent-directory, alias, case-insensitive, wildcard, or empty-value match is permitted.

Missing request scope is a caller error and blocks the batch. Missing candidate scope blocks every non-local candidate and, in Contract 1.0.0, also makes any local envelope malformed because all three fields are required. No candidate may broaden, inherit, or infer scope from payload content.

Only a candidate with exactly the explicit `READ_CANDIDATE` capability may become retrieval-eligible. A missing capability, unknown capability, duplicate capability, capability outside the provider's local registration, or attempted capability escalation is `BLOCK`. Local provider registration MAY be narrower than the envelope; the intersection is not silently accepted because that would conceal an escalation attempt.

Provider trust, human review, and retrieval admission grant no local persistence capability. `READ_CANDIDATE`, `ALLOW`, and `REVIEW` MUST NOT be translated into a write decision. Any later persistence request is a separate operation with separate authority and MUST traverse Slice 2 Contract 2.2.0 without inherited approval.

## 5. Deterministic decision model

The evaluator returns exactly one decision: `ALLOW`, `REVIEW`, or `BLOCK`. Precedence is `BLOCK` over `REVIEW` over `ALLOW`. Evaluation MUST collect stable reason codes in a fixed contract order; it MUST NOT let input iteration order, provider order, or payload content change decision priority.

### 5.1 `BLOCK`

Any one of the following produces `BLOCK`:

- `BLOCK_MALFORMED_ENVELOPE`: missing, unknown, mistyped, empty, oversized, or non-canonical envelope field;
- `BLOCK_PROVIDER_UNKNOWN_OR_UNREGISTERED`: unknown, disabled, or unregistered `provider_id`, including an external payload that merely claims a registered name;
- `BLOCK_SCOPE_REQUIRED` or `BLOCK_SCOPE_MISMATCH`: absent trusted request scope, absent candidate scope, or any non-exact `project`, `workspace`, or `namespace` binding;
- `BLOCK_CAPABILITY_REQUIRED`, `BLOCK_CAPABILITY_UNKNOWN`, or `BLOCK_CAPABILITY_ESCALATION`: missing `READ_CANDIDATE`, any unrecognized capability, or capability outside the locally authoritative grant;
- `BLOCK_PAYLOAD_DIGEST_MISMATCH`: malformed digest, digest-mode mismatch, or recomputed digest mismatch;
- `BLOCK_COMPOUND_ID_CONFLICT`: the same compound identity occurs in the current batch with inconsistent payload digest, scope, class, or capabilities;
- `BLOCK_SOURCE_CLASS_DOWNGRADE`: authoritative evidence requires a less trusted class than the envelope declares, or any path tries to relabel external data as local;
- `BLOCK_REQUEST_ID_DUPLICATE_IN_BATCH`: a `request_id` is reused by a different admission item in the same batch; and
- any internal invariant failure that prevents a deterministic, fail-closed result.

A blocked candidate is excluded before merge. It cannot replace an earlier candidate and cannot appear as a retrievable or context item.

### 5.2 `REVIEW`

`REVIEW` applies only when there is no blocking condition, the source class is `EXTERNAL_FEDERATED_CANDIDATE`, and a trusted local ingestion path or local review-only provider descriptor established the canonical envelope without authenticating the external identity. A future separately authorized policy may add another explicitly reviewable condition. In Contract 1.0.0, external identity is not authenticated, so no external candidate is allowable for retrieval. Review records are quarantined metadata receipts only and MUST NOT contain payload content.

### 5.3 `ALLOW`

`ALLOW` requires all of the following:

- the envelope, payload and request binding are valid;
- the canonical identity came from a trusted `LOCAL_CALLER` path or matches an enabled `LOCAL_PROVIDER` registration;
- source class has not been upgraded or downgraded;
- all three scopes match exactly;
- capabilities are exactly and locally authorized as `READ_CANDIDATE`;
- payload digest matches;
- current-batch request and compound-identity checks pass; and
- no `REVIEW` or `BLOCK` condition exists.

Only `ALLOW` candidates may enter candidate-source merge and retrieval. Downstream code MUST compare the decision enum explicitly to `ALLOW`; truthiness, absence of errors, and `REVIEW` are insufficient.

## 6. Replay boundary

A stateless pure function cannot determine whether a syntactically valid `request_id` appeared in a historical batch. This contract therefore does not claim historical replay protection.

Contract 1.0.0 selects the minimum no-new-persistent-state model: validate the canonical UUID structure of `request_id` and require uniqueness within the immutable current-batch context. The batch context is authoritative only for that evaluation. Cross-batch historical replay detection is a future independent capability requiring a separately designed authoritative replay context or governed state; it is neither inferred from process memory nor delegated to payload claims.

If a future contract supplies an immutable authoritative replay context from a trusted caller, that extension requires separate versioning, implementation authorization, lifecycle limits, and tests. It MUST NOT be implied by this 1.0.0 decision receipt.

## 7. Receipt and binding

Every evaluated candidate produces a stable, minimal receipt containing only:

- contract version and digest mode/version;
- decision and ordered reason codes;
- `provider_id`, `source_class`, `source_instance`, and `candidate_id`;
- `payload_digest`;
- `request_id`;
- a deterministic digest of the exact canonical request scope; and
- a deterministic digest of the authoritative provider-registry snapshot used for the decision.

The receipt MUST NOT include payload content, excerpts, secrets, credentials, arbitrary exception text, filesystem contents, or network identifiers not already present in the bounded envelope. Receipt ordering and serialization MUST be deterministic. The decision is thereby bound to the candidate input digest and exact request scope, without leaking candidate content.

## 8. Integration and invariants

Current repository call-path facts at the 6.16.0 baseline are:

- `MemoryFabricProvider.set_runtime_memory_candidates()` accepts local in-process candidates;
- `MemoryFabricProvider._candidate_jsonl_candidates_snapshot()` loads configured JSONL candidates through `load_candidate_jsonl_source()`;
- `MemoryFabricProvider._prefetch_memory_candidates_snapshot()` currently calls `_merge_candidate_sources()`;
- `MemoryFabricProvider.build_active_context()` calls `compose_active_context()`;
- `compose_active_context()` calls `fuse_memory_retrieval_v2()`; and
- `MemoryFabricProvider.get_tool_schemas()` returns an empty list.

The recommended integration point is the candidate-source boundary in `src/hermes_memory_fabric/provider.py`: after each source has produced immutable candidate/envelope pairs, but before `_merge_candidate_sources()`. The direct public `build_active_context()` route must pass through the same admission function before `compose_active_context()` so callers cannot bypass the boundary. The implementation should reuse one small admission function rather than duplicate policy at loaders and composers.

The implementation MUST preserve these invariants:

- caller-owned envelopes, payloads, request context, registry snapshots, and candidate collections are never modified in place;
- only deep-copied `ALLOW` candidates are passed forward;
- decision and receipt bind to the input digest and exact request scope;
- merging uses compound identity and never bare candidate ID across sources;
- `REVIEW` and `BLOCK` candidates cannot enter merge, retrieval, context composition, or persistence;
- Provider tool schemas remain empty and `exposes_provider_tools` remains false;
- no network access, connector execution, credential handling, implicit write, graph write, operation-ledger write, or local persistence is introduced;
- Slice 1 and Slice 2 contracts retain their existing ownership and semantics; and
- failures are fail-closed and do not partially admit a batch item.

## 9. Implementation boundary and future gates

All items in this section are recommendations pending separate implementation authorization. They are not a write authorization and do not assert that every listed path must change.

### 9.1 Proposed minimum implementation write set — pending implementation authorization

1. `src/hermes_memory_fabric/provider_federation_boundary.py` — only if a separate module is the smallest maintainable home for immutable envelope validation, deterministic decision logic, digest binding, and minimal receipts.
2. `src/hermes_memory_fabric/provider.py` — integrate admission after candidate loading and before `_merge_candidate_sources()`, and route direct `build_active_context()` candidates through the same gate before composition.
3. `tests/test_provider_federation_boundary.py` — focused contract cases for envelope, trust, scope, capabilities, digest, collision, replay-batch behavior, receipt minimization, and input immutability.
4. `tests/test_provider.py` — only the minimal integration assertions needed to prove that rejected/review candidates cannot reach merge/composition and the Provider tool surface remains empty.

`src/hermes_memory_fabric/__init__.py` is explicitly not presumed to require modification. The authorized implementation task must re-trace imports and the real call chain against its exact baseline, then remove any unnecessary candidate path from the write set. Existing candidate-loader or retrieval tests should be modified only if a focused integration assertion cannot be expressed in the two proposed test paths above.

### 9.2 Proposed test gates — pending implementation authorization

The implementation decision must define exact commands only after the final write set is known. It must not predeclare an unsupported test count. At minimum, the categories are:

- envelope schema, canonicalization, payload-authority separation, digest verification, and stable receipt tests;
- trusted local caller, registered local provider, unknown provider, and external federation classification tests;
- exact project/workspace/namespace binding and missing-scope fail-closed tests;
- explicit `READ_CANDIDATE`, unknown capability, and escalation tests;
- compound-identity conflict, bare-ID non-collision, source-class downgrade, UUID structure, and current-batch uniqueness tests;
- proof that `REVIEW` and `BLOCK` never reach merge, retrieval, context composition, or persistence;
- input and registry immutability tests;
- Provider integration regression, including empty tool schemas and no-write policy flags;
- focused regressions for candidate JSONL loading, runtime candidates, candidate merging, retrieval fusion, and active-context composition;
- the repository's required full validation at the implementation baseline; and
- a fresh independent read-only review that does not inherit implementation PASS and separately checks contract conformance, exact changed paths, test evidence, no network/write expansion, and Slice 2 isolation.

No runtime proof engine, persistent replay ledger, network simulator, provider-discovery system, or speculative abstraction is required by this contract.

## 10. Non-authorities and exit condition

This contract does not authorize code or test creation, config changes, dependency or version changes, staging, commit, push, PR, merge, tag, release, deployment, provider registration, external federation enablement, historical replay storage, or automatic successor work.

Contract design completion means only that the boundary is specified for a later implementation-decision gate. A later implementation remains ineligible until the Human Owner separately approves an exact baseline, minimum write set, verification corridor, and stop conditions.
