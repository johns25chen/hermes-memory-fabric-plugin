# Civilization Core Memory Lifecycle Taxonomy / 文明之核记忆生命周期分类法

## 2. Taxonomy Status

This is a docs-only memory lifecycle taxonomy document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates document.

It is based on the merged Temporal Validity Model document.

It is lifecycle-taxonomy candidate only.

It creates no lifecycle storage.

It creates no lifecycle state machine.

It creates no lifecycle transition logic.

It creates no automatic promotion.

It creates no automatic rejection.

It creates no automatic archival.

It creates no stale-memory detector.

It creates no automatic expiration.

It creates no supersession engine.

It creates no temporal query logic.

It creates no benchmark implementation.

It creates no evaluation runner.

It adds no tests.

It makes no code changes.

It makes no README changes.

It makes no existing doc changes.

It makes no package version change.

It creates no tag.

It creates no `v6.17`.

It creates no v7 implementation authorization.

It does not start P4.

It creates no product implementation authorization.

It creates no MVP.

It creates no runtime / dependency / adapter activation.

It creates no MCP/API operation surface.

It mutates no Memory Graph.

It adds no durable writer.

It adds no authorization/execution semantics.

The vocabulary in this document is candidate taxonomy only. It does not approve implementation, productization, connector adoption, dependency adoption, external project behavior, durable memory writing, graph mutation, automatic authorization, or automatic execution.

## 3. Why Lifecycle Taxonomy Matters

Memory needs named states before it can be reviewed safely.

Candidate, reviewed, approved, stale, superseded, rejected, blocked, historical, and archived are different meanings. Collapsing them into one generic "memory" label can make an unreviewed claim look like active authority too early.

Temporal validity needs lifecycle vocabulary to express stale and historical-only records without deleting them or treating them as current.

Failed-attempt memory needs lifecycle vocabulary to prevent permanent overblocking. A failed command, assumption, or path may be useful as scoped evidence without becoming a permanent prohibition.

Explainable recall needs lifecycle vocabulary to explain why a memory surfaced: it may surface because it is approved, because it is historical context, because it is stale and needs review, or because it is blocked from use.

Connector governance needs lifecycle vocabulary to avoid treating source snapshots as live memory. A connector result, external source snapshot, or synced artifact may be candidate evidence only until reviewed.

Lifecycle state is not truth.

Lifecycle confidence is not approval.

Human review remains required before any future memory is trusted, promoted, written, updated, deleted, shown as current, or used as decision input.

## 4. Lifecycle Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| candidate state | yes | A proposed memory item must be visibly unapproved. | Document label only; it is not durable memory. |
| review state | yes | Review status must be visible before trust. | Document label only; review status is not approval. |
| approved state | yes | Future docs need a word for human-scoped approval. | Candidate vocabulary only; approval requires separate governance. |
| active/use state | yes | Future review may need to distinguish reviewed use from candidate evidence. | Vocabulary only; it does not activate recall, write, or execution behavior. |
| stale state | yes | Time-risk needs a lifecycle label. | Label only; it does not detect staleness or delete records. |
| superseded state | yes | Later evidence may narrow or replace older evidence. | Relationship label only; it does not overwrite or erase history. |
| rejected state | yes | Rejected candidates should remain explainable. | Review vocabulary only; it is not automatic deletion. |
| blocked state | yes | Some records must not be used until review. | Review vocabulary only; it is not permanent law outside stated scope. |
| historical-only state | yes | Past-state memory can remain useful without current authority. | Label only; it does not create temporal query behavior. |
| archived state | yes | Future docs may need a word for retained but inactive records. | Label only; it does not move or store anything. |
| deletion proposal state | yes | Future deletion requests need review vocabulary. | Proposal label only; it does not delete. |
| failed-attempt lifecycle | yes | Failed attempts need scoped lifecycle handling. | Candidate vocabulary only; it must not freeze future improvement. |
| do-not-retry lifecycle | yes | Do-not-retry rules need candidate, blocked, narrowed, or rejected states. | Candidate vocabulary only; it is not automatic authority. |
| connector/source lifecycle | yes | External source snapshots and connector results may age or conflict. | Candidate vocabulary only; no connector or sync behavior follows. |
| lifecycle confidence | yes | Reviewers need qualitative evidence-strength language. | Human-review vocabulary only; it is not a score or approval. |
| lifecycle transition vocabulary | yes | Future docs need names for proposed state changes. | Vocabulary only; no transition engine is created. |
| automatic lifecycle transition | no | Automatic transition would be behavior, not taxonomy. | Excluded; no automatic lifecycle transition is created. |
| lifecycle state machine | no | A state machine would define operational behavior. | Excluded; no lifecycle state machine is created. |
| lifecycle storage | no | Storage would change durable surfaces. | Excluded; no lifecycle storage is created. |
| Memory Graph mutation | no | Graph writes would change durable memory surfaces. | Excluded; no Memory Graph mutation is created. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Lifecycle Object Types

These object types may later receive lifecycle labels in docs or review packets. This section defines vocabulary only, not schema or behavior.

| Object type | What it is | Lifecycle question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| memory candidate | A proposed memory item that has not been approved. | Is it still merely proposed, or ready for review? | Claim, source reference, temporal scope note, risk flags. | Do not infer truth, approval, durable write, or current authority. |
| recall result | A surfaced candidate or record. | Why did it surface, and what state should a reviewer see? | Recall reason, source reference, provenance path, lifecycle label. | Do not infer action permission, write permission, or trust. |
| recall trace | The explanation path for recall. | Does the trace expose candidate, reviewed, stale, conflicted, or historical status? | Source path, inference markers, conflict notes, temporal notes. | Do not infer authorization, execution, or graph mutation. |
| write proposal | A proposal to add future durable memory under separate governance. | Should it remain proposed, move to review, or be rejected? | Source, claim, reason for memory, risk flags, reviewer note if any. | Do not infer automatic durable writer or automatic promotion. |
| update proposal | A proposal to change a future memory record. | What prior state would be changed, and what next state is proposed? | Existing record reference, proposed next state, conflict notes, audit note. | Do not infer silent overwrite or state transition. |
| deletion proposal | A proposal to delete, hide, or retire a future memory record. | Is deletion requested, rejected, or blocked pending review? | Record reference, deletion reason, audit-preservation note, reviewer note. | Do not infer erasure or audit removal. |
| approved memory record | A future human-reviewed memory record under separate governance. | Is it approved candidate, active reviewed, or time-bound? | Approval scope, reviewer note, source reference, temporal fields if known. | Do not infer indefinite validity or automatic active use. |
| rejected memory record | A candidate rejected by review. | Why was it rejected, and is the rejection scoped? | Rejection reason, source reference, reviewer note, risk flags. | Do not infer deletion of evidence or permanent impossibility. |
| stale memory record | A record whose claim may no longer be current. | Is staleness candidate or reviewed, and what is the stale reason? | Stale reason, source timestamp or observed time, conflict notes. | Do not infer automatic deletion or replacement. |
| superseded memory record | A record narrowed or replaced by later evidence. | What supersedes it, and what old evidence remains useful? | Old record, successor reference, `superseded_by`, reviewer note. | Do not infer erasure, overwrite, or hidden mutation. |
| historical memory record | A record retained as past context. | Should it be shown as historical only rather than current guidance? | Source reference, temporal scope note, reason it is historical. | Do not infer current authority or uselessness. |
| archived memory record | A retained but inactive record. | Is it archived candidate or archived reviewed? | Archive reason, source reference, reviewer note if reviewed. | Do not infer deletion, storage movement, or current use. |
| failed attempt record | A bounded record of a failed action, command, assumption, or path. | Is it candidate, active time-bound, historical only, or rejected? | Attempt summary, failure evidence, scope, temporal note. | Do not infer permanent prohibition. |
| do-not-retry candidate | A proposed rule to avoid a failed path under stated conditions. | Is it candidate, blocked, narrowed, superseded, or rejected after review? | Failed attempt record, blocked behavior, scope, exception condition. | Do not infer automatic authority or indefinite ban. |
| external source candidate | An external source or project used as methodology/reference evidence. | Is it source snapshot, stale candidate, conflicted, or review required? | Source name, source class, observation context, temporal note. | Do not infer dependency, adapter, or current live fact. |
| connector/source candidate | A candidate source or connector class for later review. | What trust, sync, action, credential, and stale-source risks exist? | Source type, risk flags, provenance path, review requirement. | Do not infer connector implementation or API surface. |
| human review decision | A future human-scoped candidate decision. | What state did the reviewer choose, and with what scope? | Evidence packet, reviewer note, decision scope, proposed next state. | Do not infer execution, write, deployment, or P4 activation. |

## 6. Lifecycle State Vocabulary

These are document labels only, not schema or implementation.

| Candidate lifecycle state | Meaning | Allowed use | Required evidence | Human review requirement | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| `proposed` | A lifecycle item has been suggested but not shaped enough for candidate review. | Use for early write, update, deletion, or classification proposals. | Claim or proposal summary, source hint, reason for proposal. | Required before any trust or promotion. | Do not infer candidate completeness or truth. |
| `candidate` | The item is reviewable candidate evidence. | Use when source, claim, and scope are visible enough for review. | Claim, source reference, temporal scope note, risk flags. | Required before approval or active use. | Do not infer approved memory or durable write. |
| `under_review` | A reviewer is actively considering the item. | Use for visible review flow in docs. | Candidate packet and review scope. | Required and not yet complete. | Do not infer approval, rejection, or mutation. |
| `review_required` | The item cannot be safely used without human review. | Use for uncertainty, conflict, stale risk, authority risk, or missing evidence. | Reason for review requirement and known evidence gaps. | Required before use. | Do not infer block removal or approval. |
| `approved_candidate` | A reviewer has approved the candidate within a stated scope, but it is not automatically active memory. | Use only with explicit reviewer scope. | Reviewer note, source reference, approved scope, risk flags. | Required and must remain scoped. | Do not infer automatic active memory or timeless truth. |
| `active_reviewed` | A reviewed item may be used within its stated scope. | Use only for human-reviewed, scope-bound use language. | Reviewer note, source reference, provenance path, scope. | Required. | Do not infer execution permission or indefinite validity. |
| `active_time_bound` | A reviewed item may be used only within a known time, version, branch, tool, or source scope. | Use for bounded current use. | `valid_from` / `valid_until` if known, observed time, scope note. | Required. | Do not infer use outside the boundary. |
| `stale_candidate` | The item may be stale but has not been reviewed as stale. | Use when age, newer evidence, or volatility creates risk. | Stale reason candidate, source timestamp or observed time. | Required before current use. | Do not infer deletion or rejection. |
| `stale_reviewed` | A reviewer marked the item stale within scope. | Use only with a stale reason and reviewer note. | Stale reason, reviewer note, source/conflict evidence. | Required. | Do not infer audit removal or automatic replacement. |
| `superseded` | Later or narrower evidence may replace or limit the item. | Use when successor evidence is visible. | `superseded_by`, old claim, successor reference, rationale. | Required before treating successor as active. | Do not infer erasure or silent overwrite. |
| `conflicted` | Evidence disagrees or interpretation is unstable. | Use when sources, times, scopes, or readings conflict. | Conflict notes, conflict source, provenance path. | Required before use. | Do not infer automatic resolution or winner. |
| `rejected` | A reviewer rejected the candidate within a stated scope. | Use for rejected memory or rejected assumptions. | Rejection reason, source reference, reviewer note. | Required. | Do not infer deletion or permanent impossibility outside scope. |
| `blocked` | Lifecycle risk prevents use until review or separate decision. | Use for authority, privacy, conflict, stale, or boundary risks. | Blocked reason, risk flags, source reference if available. | Required to unblock. | Do not infer permanent law outside stated reason. |
| `historical_only` | The item is retained as past context, not current guidance. | Use for old project states, old prices, old failures, or superseded claims. | Temporal scope note, reason for historical-only treatment. | Required when use would affect decisions. | Do not infer current authority or uselessness. |
| `archived_candidate` | The candidate is retained for reference but not active. | Use for old, incomplete, or deferred candidate material. | Archive reason and source reference. | Required before any later reuse. | Do not infer deletion or reviewed archival. |
| `archived_reviewed` | A reviewer has marked a record as retained but inactive. | Use only with reviewer scope. | Reviewer note, archive reason, source reference. | Required. | Do not infer storage movement or deletion. |
| `deletion_proposed` | Deletion, hiding, or removal has been proposed. | Use for deletion requests only. | Deletion reason, target reference, audit-preservation note. | Required before any removal. | Do not infer deletion. |
| `deletion_rejected` | A deletion proposal was rejected. | Use when deletion is not accepted under the reviewed scope. | Rejection reason, reviewer note, retained audit note. | Required. | Do not infer the original record is approved for active use. |
| `unknown_lifecycle` | The lifecycle state cannot be judged from available evidence. | Use when evidence, source, or review status is missing. | Missing-evidence note and risk flags. | Required before use. | Do not infer safe current use. |

## 7. Lifecycle Transition Vocabulary

These are candidate transition labels for future documents. No transition engine is created.

| Candidate transition label | Meaning | Allowed evidence | Required human action | Prohibited automatic behavior |
| --- | --- | --- | --- | --- |
| `propose` | Put a claim or decision into proposal form. | Claim, source hint, reason for memory. | Human review before trust. | Do not write or promote automatically. |
| `request_review` | Ask for human review of a candidate. | Candidate packet, risk flags, source reference. | Reviewer accepts, rejects, blocks, or defers later. | Do not treat request as approval. |
| `approve_candidate` | Mark a candidate as approved within a stated scope. | Evidence packet, reviewer note, source reference. | Explicit reviewer approval. | Do not activate memory automatically. |
| `mark_active_reviewed` | Mark reviewed use within scope. | Reviewer note, scope, provenance path. | Explicit reviewer decision. | Do not execute, write, or broaden scope automatically. |
| `mark_time_bound` | Mark use as constrained by time, version, branch, tool, source, or user scope. | Temporal fields, scope note, source evidence. | Reviewer confirms boundary if use matters. | Do not expire or query automatically. |
| `mark_stale_candidate` | Mark possible staleness before review. | Age, volatility, newer source, stale reason candidate. | Reviewer decides later use. | Do not delete or reject automatically. |
| `mark_stale_reviewed` | Mark reviewed staleness. | Stale reason, reviewer note, conflict/source evidence. | Reviewer explicitly marks stale. | Do not delete or supersede automatically. |
| `mark_superseded` | Link old evidence to a possible successor. | Old claim, successor reference, supersession rationale. | Reviewer confirms relationship. | Do not overwrite or erase automatically. |
| `mark_conflicted` | Mark unresolved conflict. | Conflict source, conflict notes, provenance path. | Reviewer decides whether to block, narrow, or defer. | Do not resolve conflict automatically. |
| `reject_candidate` | Reject a candidate within scope. | Rejection reason, source reference, reviewer note. | Reviewer explicitly rejects. | Do not erase evidence automatically. |
| `block_use` | Prevent use until separate review or decision. | Blocked reason, risk flags, evidence gap. | Reviewer or operator confirms block scope. | Do not create permanent prohibition outside scope. |
| `mark_historical_only` | Retain as past context, not current guidance. | Temporal scope note, historical reason, source reference. | Reviewer confirms if decision-impacting. | Do not hide or delete automatically. |
| `archive_candidate` | Retain candidate material as inactive. | Archive reason and source reference. | Human accepts archive label. | Do not move storage or delete automatically. |
| `archive_reviewed` | Mark reviewed inactive retention. | Reviewer note, archive reason, source reference. | Explicit reviewer decision. | Do not infer active use or deletion. |
| `propose_deletion` | Request deletion, hiding, or removal. | Target reference, deletion reason, audit note. | Human review required. | Do not delete automatically. |
| `reject_deletion` | Reject a deletion proposal. | Rejection reason and reviewer note. | Reviewer explicitly rejects deletion. | Do not promote the target record automatically. |
| `defer_review` | Leave the item unresolved until more evidence or scope exists. | Missing evidence note, risk flags, next review need. | Reviewer or operator chooses deferral. | Do not silently approve or reject. |
| `reopen_review` | Reconsider a prior decision due to new evidence or scope change. | New source, conflict, stale reason, or changed scope. | Human explicitly reopens review. | Do not reopen automatically. |

## 8. Lifecycle Evidence Requirements

| Field | Why it matters | When required | Prohibited inference |
| --- | --- | --- | --- |
| `claim` | States what the memory says or proposes. | Required for proposed, candidate, approved, rejected, stale, superseded, conflicted, and historical items. | Do not treat claim text as truth. |
| `source_reference` | Lets a reviewer inspect where the claim came from. | Required for any reviewable lifecycle label. | Do not treat citation as approval. |
| `source_timestamp` | Helps distinguish old source material from current evidence. | Required when source time is available or temporal risk matters. | Do not infer current validity from source time. |
| `observed_at` | Records when the claim or source state was observed. | Required for volatile facts, repo status, failed attempts, and external source snapshots when known. | Do not infer the claim is still true. |
| `provenance_path` | Shows how source evidence became a memory candidate. | Required for recall traces, write proposals, approved candidates, and conflict review. | Do not infer Memory Graph mutation. |
| `temporal_scope_note` | Explains whether the claim is current, time-bound, historical, or unknown. | Required for active time-bound, stale, superseded, historical-only, failed-attempt, and external source items. | Do not infer timeless validity. |
| `conflict_notes` | Makes disagreement visible. | Required for conflicted states and recommended when evidence is partial. | Do not infer automatic resolution. |
| `stale_reason` | Explains why the item may no longer be current. | Required for `stale_candidate` and `stale_reviewed`. | Do not infer deletion or rejection. |
| `superseded_by` | Shows the possible successor or narrowing evidence. | Required for `superseded`. | Do not infer erasure of the old record. |
| `reviewer_note` | Captures human scope and rationale. | Required for reviewed states, rejection, deletion rejection, archival reviewed, and active reviewed use. | Do not infer execution permission. |
| `risk_flags` | Makes authority, privacy, connector, conflict, stale, or boundary risks visible. | Required when use could affect decisions or external surfaces. | Do not infer risk is resolved because it is named. |
| `recommended_next_state` | Helps route future review. | Optional for proposals and review packets. | Do not infer automatic state transition. |
| `blocked_reason` | Explains why use must stop. | Required for `blocked` and recommended for high-risk `unknown_lifecycle`. | Do not infer permanent prohibition outside scope. |

These fields are evidence vocabulary only. They create no storage format, parser, validator, transition rule, lifecycle state machine, durable writer, API, adapter, or graph mutation.

## 9. Lifecycle and Temporal Validity Interaction

Current does not mean timeless. A current-looking lifecycle state may still need `observed_at`, `source_timestamp`, `valid_from`, `valid_until`, or a plain-language temporal scope note.

Stale does not mean delete. A stale record may be useful as warning, history, or evidence of prior state.

Superseded does not mean erase. A superseded record should preserve old evidence, old scope, and the successor reference.

Historical-only does not mean useless. Historical-only memory can explain why a decision was made, why a path failed, or why a later correction exists.

`unknown_time_scope` should usually require review before current use.

`active_time_bound` must preserve `valid_from` / `valid_until` if known.

`stale_candidate` must preserve `stale_reason`.

`superseded` must preserve `superseded_by`.

Conflict must preserve `conflict_source` or equivalent conflict notes.

Human review remains required before lifecycle and temporal labels are trusted, promoted, updated, deleted, or used as decision input.

## 10. Lifecycle Confidence Candidate

Future docs may use this non-implemented lifecycle confidence vocabulary:

| Candidate label | Meaning |
| --- | --- |
| `high` | Lifecycle state has clear evidence and review scope. |
| `medium` | Lifecycle state is plausible but needs review. |
| `low` | Lifecycle state has weak or incomplete evidence. |
| `unknown` | Lifecycle state cannot be judged. |
| `blocked` | Lifecycle risk prevents use. |

This is not an automated score.

This is not lifecycle calculation.

This is not approval.

This is not execution permission.

Human operator review remains required.

## 11. Write / Update / Delete Lifecycle Criteria

Future memory mutation proposals may use these candidate criteria:

- write proposal starts as `proposed` or `candidate`;
- write proposal must show source and reason for memory;
- update proposal must show prior state and proposed next state;
- update proposal must preserve old record for audit;
- deletion proposal must distinguish privacy, error, conflict, duplicate, stale, and user-requested reasons;
- deletion proposal must not erase audit trail unless separately governed;
- rejected deletion must remain explainable;
- no automatic durable writer;
- no automatic promotion;
- no automatic deletion.

Write, update, deletion, rejection, approval, staleness, archival, and supersession are governance concepts here.

They are not active mutation behavior.

They require explicit future human scope before any implementation discussion.

## 12. Failed Attempt / Do-Not-Retry Lifecycle

Failed attempt starts as `candidate`.

Do-not-retry starts as `candidate`, not law.

Failed attempt can be `active_time_bound` only within tool, version, repo, branch, network, or user-preference scope.

Old failed attempts may become `historical_only`.

Do-not-retry may be `blocked`, narrowed, `superseded`, or `rejected` after review.

Failed-attempt memory must not freeze future improvement.

Failed-attempt memory must preserve evidence and scope.

A useful failed-attempt lifecycle label says "do not repeat this exact path under these same conditions without review." It does not say "this path can never work."

## 13. Connector and External Source Lifecycle Risk

External source and connector lifecycle risks include:

| Risk | Meaning | Safe taxonomy response |
| --- | --- | --- |
| source snapshot may become stale | A source captured at one time may not describe the current world. | Mark candidate, stale candidate, historical-only, or review required. |
| connector result may be candidate only | A connector result may be raw evidence rather than approved memory. | Keep as candidate until reviewed. |
| synced data may conflict with prior source | Later sync or source material may disagree with earlier evidence. | Mark conflicted and preserve conflict notes. |
| external API behavior may change | Source behavior can drift without local repo changes. | Treat behavior claims as time-bound candidate evidence. |
| credential or permission state may expire | Access may depend on temporary credentials or roles. | Require temporal scope and review before reuse. |
| external repo activity may change | Activity, popularity, releases, issues, and commits are volatile. | Treat as dated snapshot only unless freshly verified under a separate scope. |
| web source may disappear or be rewritten | Web pages can change, move, or vanish. | Preserve source timestamp if available or mark unknown lifecycle / review required. |
| connector/source candidate may be overtrusted | Source enthusiasm can become operation drift. | Do not approve memory without review. |

Connector/source candidate must not become approved memory without review.

This document adds no connector, adapter, MCP/API surface, sync behavior, or action behavior.

## 14. Human Review Gate Readiness for Lifecycle Decisions

Before any later P4 consideration, a human reviewer must be able to see:

- current lifecycle state;
- proposed next state;
- `source_reference`;
- `provenance_path`;
- `temporal_scope_note`;
- `stale_reason` if stale;
- `superseded_by` if superseded;
- `conflict_notes` if conflicted;
- that reviewer can reject without side effect;
- that reviewer can block use without side effect;
- that reviewer decision is recorded as candidate only.

P4 remains paused.

P4 requires explicit human confirmation later.

Human review readiness means the reviewer can inspect, accept, reject, block, defer, narrow, or request more evidence. It does not mean the system can write, update, delete, archive, promote, execute, authorize, query, or mutate automatically.

## 15. Candidate Examples

These examples are illustrative only.

| Memory type | Likely lifecycle state | Required evidence | Safe next state | Prohibited inference |
| --- | --- | --- | --- | --- |
| newly proposed user preference memory | `proposed` or `candidate` | User statement, observed time, scope note, risk flags. | `request_review` or `approved_candidate` after review. | Do not infer permanent preference. |
| merged PR status memory | `active_time_bound` or `historical_only` | Local git evidence, source reference, observed time, branch scope. | `active_reviewed` only if reviewed for current repo state. | Do not infer future branch state. |
| old project branch assumption | `stale_candidate` or `historical_only` | Prior branch note, observed time, stale reason. | `mark_stale_reviewed` or `mark_historical_only`. | Do not infer current branch truth. |
| outdated product price memory | `stale_candidate` or `blocked` | Dated source, price scope, stale reason. | `historical_only` or review with current source under separate scope. | Do not infer current price. |
| failed command memory | `candidate` or `active_time_bound` | Command, failure evidence, tool/repo/branch/network scope. | scoped do-not-retry candidate or `historical_only`. | Do not infer permanent impossibility. |
| rejected assistant assumption | `rejected` | Assumption text, correction source, rejection reason. | Retain as explainable rejected record. | Do not infer deletion or broad ban. |
| external repo popularity snapshot | `historical_only` or `review_required` | Dated source snapshot and observation context. | Review only with fresh evidence under separate scope. | Do not infer live popularity. |
| connector source result | `candidate` or `conflicted` | Source type, sync/credential note, provenance path, conflict notes if any. | `request_review` or `block_use`. | Do not infer approved memory, adapter, or operation surface. |

## 16. Candidate Future Sequence

Recommended docs-only sequence:

1. Failed Attempt Memory / Do-Not-Retry Rules
2. Explainable Recall Trace Template
3. Connector Governance Taxonomy
4. Memory Ontology Mapping
5. External Product Explanation Candidate
6. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

## 17. Prohibited Implementation Rules

Do not implement lifecycle storage.

Do not implement lifecycle state machine.

Do not implement lifecycle transition engine.

Do not implement automatic promotion.

Do not implement automatic rejection.

Do not implement automatic archival.

Do not implement automatic deletion.

Do not implement stale-memory detector.

Do not implement automatic expiration.

Do not implement supersession engine.

Do not implement temporal query engine.

Do not implement evaluation runner.

Do not implement benchmark runner.

Do not add tests.

Do not add dependencies.

Do not add adapters.

Do not create runtime-activation bridge.

Do not create MCP/API operation surface.

Do not mutate Memory Graph.

Do not add durable writer.

Do not add authorization/execution semantics.

Do not start P4.

Do not start v7 implementation.

Do not build MVP.

Do not implement Operator Console.

Do not tag post-terminal docs.

Do not change package version.

Do not change existing docs.

Do not change README.

Do not change source, tests, scripts, or config.

Do not treat lifecycle state as truth.

Do not treat lifecycle confidence as approval.

Do not treat `approved_candidate` as automatic active memory.

Do not treat stale as automatic deletion.

Do not treat superseded as automatic erasure.

## 18. Stop Conditions

If lifecycle taxonomy turns into code, stop.

If lifecycle taxonomy turns into tests, stop.

If lifecycle taxonomy turns into lifecycle storage, stop.

If lifecycle taxonomy turns into state machine, stop.

If lifecycle taxonomy turns into transition engine, stop.

If lifecycle taxonomy turns into automatic promotion, stop.

If lifecycle taxonomy turns into automatic deletion, stop.

If lifecycle taxonomy turns into stale detector, stop.

If lifecycle taxonomy turns into expiration logic, stop.

If lifecycle taxonomy turns into temporal query engine, stop.

If lifecycle taxonomy turns into Memory Graph mutation, stop.

If lifecycle taxonomy turns into durable writer, stop.

If lifecycle taxonomy turns into dependency adoption, stop.

If lifecycle taxonomy turns into adapter work, stop.

If lifecycle taxonomy turns into MCP/API operation surface, stop.

If lifecycle taxonomy turns into authorization/execution semantics, stop.

If lifecycle taxonomy starts P4, stop.

If lifecycle taxonomy starts v7 implementation, stop.

If lifecycle taxonomy starts MVP/product deployment, stop.

If lifecycle taxonomy starts changing old docs, stop.

If `pyproject.toml` version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 19. Final Taxonomy Statement

This document defines memory lifecycle taxonomy candidates only.

It does not evaluate live memory.

It does not implement lifecycle behavior.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
