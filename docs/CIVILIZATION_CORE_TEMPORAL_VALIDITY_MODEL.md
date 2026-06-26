# Civilization Core Temporal Validity Model / 文明之核时间有效性模型

## 2. Model Status

This is a docs-only temporal-validity model document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates document.

It is temporal-model candidate only.

It creates no temporal storage.

It creates no temporal query logic.

It creates no automatic expiration.

It creates no stale-memory detector.

It creates no supersession engine.

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

The vocabulary in this document is candidate methodology only. It does not approve implementation, productization, connector adoption, dependency adoption, external project behavior, durable memory writing, graph mutation, automatic authorization, or automatic execution.

## 3. Why Temporal Validity Matters

Memory can be true once and wrong later.

Project status, versions, roles, prices, laws, schedules, external repo facts, and user preferences may become stale.

Recall without time scope can create false authority: a prior fact may appear current, a historical note may appear prescriptive, or a failed attempt may block a path after the environment has changed.

Temporal validity is needed before lifecycle, failed-attempt memory, explainable recall, connector governance, and P4 can be considered safely.

Time metadata is not truth.

Temporal confidence is not approval.

Human review remains required before any temporal claim is trusted, promoted, written, updated, deleted, shown as current, shown as historical only, or used as decision input.

## 4. Temporal Validity Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| `observed_at` | yes | A reviewer needs to know when a claim was observed. | Candidate field only; it does not prove current truth. |
| `valid_from` | yes | Some claims are scoped to a known start time, version, or status boundary. | Candidate field only; it does not activate temporal storage. |
| `valid_until` | yes | Some claims should stop being read as current after a known boundary. | Candidate field only; it does not create automatic expiration. |
| `source_timestamp` | yes | Source creation or update time may help review temporal scope. | Candidate field only; it is not proof that a claim remains valid. |
| `review_required` | yes | Temporal uncertainty should be visible before use. | Review marker only; it is not approval or execution permission. |
| `unknown_time_scope` | yes | Unknown time scope must be explicit instead of hidden. | Candidate warning only; it does not resolve uncertainty. |
| `stale_reason` | yes | A stale candidate should explain why time risk exists. | Candidate explanation only; it does not run a detector. |
| `superseded_by` | yes | A reviewer may need to see a newer or narrower candidate claim. | Candidate reference only; it does not overwrite old records. |
| `conflict_source` | yes | Conflicting temporal evidence should be inspectable. | Candidate reference only; it does not choose a winner. |
| temporal confidence | yes | Reviewers need qualitative risk vocabulary. | Human-review vocabulary only; it is not an automated score. |
| temporal recall question | yes | Recall should expose time-scope questions before trust. | Documented question only; it does not implement recall behavior. |
| temporal write proposal | yes | Future write proposals should include time evidence. | Proposal criteria only; no durable writer follows. |
| temporal update proposal | yes | Future updates should explain what changed and what is superseded. | Proposal criteria only; no mutation follows. |
| temporal deletion proposal | yes | Future deletion proposals should distinguish temporal, privacy, conflict, and error reasons. | Proposal criteria only; no deletion follows. |
| automatic expiration | no | Expiration behavior would be implementation, not model vocabulary. | Excluded; no automatic expiration or expiry transition is created. |
| stale-memory detector | no | Detection behavior would be runtime capability. | Excluded; no stale-memory detector is created. |
| temporal query engine | no | Query behavior would be implementation. | Excluded; no temporal query engine or query logic is created. |
| Memory Graph mutation | no | Graph writes would change durable memory surfaces. | Excluded; no Memory Graph mutation is created. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Temporal Object Types

| Object type | What it is | Temporal question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| memory candidate | A proposed memory item that has not been approved. | When was this observed, and is its time scope reviewable? | Claim, source reference, `observed_at` or `source_timestamp`, time-scope note. | Do not infer approved memory, durable write, or current truth. |
| approved memory record | A future record a human may approve under separate governance. | Does the approval scope still match the time-bound evidence? | Approval note, source reference, reviewer scope, temporal fields if known. | Do not infer indefinite validity or unrelated future authority. |
| stale memory record | A record whose claim may no longer be current. | Why might the claim be stale, and should use be blocked? | Prior claim, stale reason, conflict or newer source, review requirement. | Do not infer automatic deletion or automatic replacement. |
| superseded memory record | A record narrowed or replaced by later evidence. | What newer or more specific evidence may supersede it? | Old record, successor reference, reason for possible supersession, reviewer note. | Do not infer silent overwrite or loss of audit trail. |
| rejected memory record | A candidate rejected by review. | Is rejection time-bound or permanently out of scope? | Rejection reason, source reference, review timestamp if known. | Do not infer erased evidence or permanent impossibility outside stated scope. |
| recall result | A surfaced memory candidate or record. | Should it be read as current, time-bound, historical only, or blocked? | Recall reason, source path, temporal fields, uncertainty note. | Do not infer action permission or durable adoption. |
| recall trace | The explanation path for why recall surfaced. | Did the trace expose observation time, source time, and uncertainty? | Source path, inference markers, time-scope notes, conflict notes. | Do not infer authorization, execution, or graph mutation. |
| temporal claim | Any claim whose validity depends on time, version, environment, or supersession. | What time interval or observation boundary controls this claim? | Claim text, temporal fields, source evidence, uncertainty note. | Do not infer timeless truth. |
| project status claim | A claim about branch, merge, tag, roadmap, status, or completion state. | Was this true only for a repository state or review moment? | Local git state, docs evidence, observation time, scope note. | Do not infer future status without current verification. |
| version claim | A claim about package version, tag, release, or stage identity. | Which version and repository state does the claim describe? | Local file, tag, log, doc reference, observed state. | Do not infer a successor version or release continuation. |
| external source claim | A claim about an external project, source, benchmark, or public fact. | When was the external fact observed, and how volatile is it? | Dated source, access context, source timestamp if available. | Do not infer current live fact from an old snapshot. |
| connector/source claim | A claim about a source, connector, sync, credential, or external API. | What time window controls trust, sync, permission, or policy? | Source class, credential/sync note if applicable, review requirement. | Do not infer adapter, sync behavior, or MCP/API operation surface. |
| failed attempt record | A bounded record of a failed action, command, tool path, design, or assumption. | Under which tool version, repo state, branch, network condition, or preference did it fail? | Attempt summary, failure evidence, scope, time/scope note. | Do not infer permanent prohibition or broad future impossibility. |
| do-not-retry candidate | A candidate rule that a failed path should not be repeated under stated conditions. | What exact conditions make retry unsafe or wasteful? | Failed attempt record, scope, exception condition, review note. | Do not infer automatic authority or indefinite ban. |
| human review decision | A future human-scoped candidate decision about temporal use. | What did the reviewer decide, and for what time/scope boundary? | Evidence packet, reviewer note, decision scope, candidate next state. | Do not infer execution, write, deployment, or P4 activation. |

## 6. Temporal Field Candidates

This is a document template only, not schema implementation.

| Field | Meaning | When to use | Evidence requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `observed_at` | When the claim or source state was observed. | Use when recording a claim that may become stale. | Local observation, source note, or review note. | Do not infer that the claim is still true. |
| `valid_from` | Earliest known validity boundary. | Use when a claim begins at a known version, date, event, or status. | Source evidence for the start boundary. | Do not infer broad prior validity. |
| `valid_until` | Latest known validity boundary or end condition. | Use when a claim has a known expiry, closure, or status end. | Source evidence for the end boundary. | Do not create automatic expiration behavior. |
| `source_timestamp` | Timestamp attached to the source itself. | Use when the source provides a creation/update time. | Source-visible timestamp or local file/git evidence. | Do not treat source time as current truth. |
| `reviewed_at` | When a human review occurred. | Use for future reviewed candidate decisions. | Reviewer note or governance record. | Do not treat review time as approval unless explicitly scoped. |
| `review_required` | Whether temporal use needs human review. | Use when time scope is uncertain, volatile, conflicted, or stale-prone. | Reason for review requirement. | Do not infer block removal or approval. |
| `stale_reason` | Why a claim may no longer be valid. | Use when newer evidence, volatility, or context change raises risk. | Source, conflict, environment, or reviewer note. | Do not infer automatic stale detection. |
| `superseded_by` | Candidate successor that may replace or narrow this claim. | Use when later evidence may supersede older evidence. | Successor reference and rationale. | Do not infer silent overwrite. |
| `supersedes` | Prior claim this candidate may replace or narrow. | Use in update proposals and supersession candidates. | Prior record reference and replacement rationale. | Do not infer deletion of the prior record. |
| `conflict_source` | Source that conflicts with the claim. | Use when evidence disagrees. | Conflict source reference and scope note. | Do not infer which source wins automatically. |
| `conflict_observed_at` | When the conflicting source was observed. | Use when conflict timing matters. | Observation time or source timestamp. | Do not infer the conflict is resolved. |
| `unknown_time_scope` | Time scope is not reliably known. | Use when observation, source, or validity windows are missing. | Explicit note explaining the gap. | Do not infer evergreen status. |
| `temporal_confidence` | Qualitative confidence in time scope. | Use to help human review, not to decide automatically. | Time-scope evidence and uncertainty note. | Do not treat confidence as approval. |
| `temporal_scope_note` | Plain-language summary of time boundaries. | Use when fields need human-readable context. | Source/context evidence or reviewer note. | Do not treat prose as implementation schema. |
| `recommended_next_state` | Suggested candidate state for review. | Use in proposals or review packets. | Rationale tied to evidence and risk. | Do not infer automatic state transition. |
| `blocked_reason` | Reason temporal use must stop. | Use when evidence gap or risk prevents safe use. | Boundary, conflict, stale, privacy, or authority reason. | Do not infer permanent ban outside scope. |

These fields create no storage format, parser, validator, lifecycle system, temporal query engine, stale-memory detector, expiration behavior, supersession engine, durable writer, API, adapter, or graph mutation.

## 7. Temporal Status Vocabulary

| Status label | Meaning | Allowed use | Human review requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `current_candidate` | The claim may be current but is not reviewed. | Use for candidate evidence with plausible current scope. | Required before trust or promotion. | Do not infer truth or approval. |
| `current_reviewed` | A human reviewed the claim as current within stated scope. | Use only with explicit reviewer scope. | Required and must remain scoped. | Do not infer indefinite validity. |
| `time_bound` | The claim has an explicit validity window or event boundary. | Use for date-, version-, branch-, source-, or event-scoped claims. | Required when use matters. | Do not infer validity outside the boundary. |
| `stale_candidate` | The claim may be stale. | Use when staleness risk exists but is not fully reviewed. | Required before current use. | Do not infer automatic deletion. |
| `stale_reviewed` | A human reviewed and marked the claim stale within scope. | Use only with stale reason and reviewer note. | Required. | Do not infer audit removal. |
| `superseded` | A later or more specific claim may replace or narrow the old claim. | Use when successor evidence is recorded. | Required before treating replacement as safe. | Do not infer silent overwrite. |
| `conflicted` | Evidence disagrees. | Use when sources, times, scopes, or interpretations conflict. | Required before use. | Do not infer automatic resolution. |
| `unknown_time_scope` | Reliable time scope is missing. | Use when observation/source/validity time is unknown. | Required before current use. | Do not infer evergreen status. |
| `blocked_temporal_use` | Temporal risk prevents use. | Use when time uncertainty, conflict, stale risk, or boundary risk is too high. | Required to unblock. | Do not infer permanent prohibition outside the stated reason. |
| `evergreen_candidate` | The claim may be broadly stable but still needs review. | Use for low-volatility candidate claims. | Required before durable trust. | Do not infer timeless truth. |
| `historical_only` | The claim should be shown as history, not current guidance. | Use for past states, old failures, old prices, old roles, old versions, or superseded claims. | Required when the distinction affects decisions. | Do not infer current authority. |

## 8. Temporal Confidence Candidate

Future docs may use this non-implemented temporal confidence vocabulary:

| Candidate label | Meaning |
| --- | --- |
| `high` | Time scope is clear and evidence is current enough for review. |
| `medium` | Time scope is mostly clear but needs review. |
| `low` | Time scope is weak, old, or conflict-prone. |
| `unknown` | No reliable time scope. |
| `blocked` | Temporal risk prevents use. |

This is not an automated score.

This is not freshness calculation.

This is not approval.

This is not execution permission.

Human operator review remains required.

## 9. Temporal Recall Questions

Future docs may evaluate recall with time awareness by asking:

- when was this memory observed?
- when was the source created or updated?
- is the claim still likely valid?
- does the memory have a `valid_until` boundary?
- does a newer memory supersede it?
- is there a conflict source?
- is the time scope unknown?
- should the recall be blocked until review?
- should the recall be shown as historical only?
- did recall hide uncertainty?

Recall should distinguish current candidate, reviewed current claim, time-bound claim, historical-only claim, stale candidate, superseded claim, conflicted claim, and blocked temporal use.

This document creates no recall implementation.

This document creates no temporal query implementation.

## 10. Temporal Write / Update / Delete Proposal Criteria

Future memory mutation proposals may use these candidate criteria:

- write proposal must include `observed_at` or `source_timestamp`;
- write proposal must state whether the claim is time-bound or evergreen candidate;
- update proposal must identify what it supersedes;
- update proposal must preserve the old record for audit;
- deletion proposal must explain whether removal is temporal, privacy, conflict, or error related;
- stale marking must preserve audit trail;
- supersession must not silently overwrite;
- no automatic durable writer;
- no automatic promotion.

Write, update, deletion, stale marking, supersession, rejection, and promotion are governance concepts here.

They are not active mutation behavior.

They require explicit future human scope before any implementation discussion.

## 11. Staleness Model Candidates

| Staleness category | What it means | Typical evidence | Review question | Prohibited inference |
| --- | --- | --- | --- | --- |
| `source_stale` | The source may be old or no longer maintained. | Source timestamp, newer source, missing update context. | Is the source still appropriate for this claim? | Do not infer source invalidity without review. |
| `project_status_stale` | A project status claim may no longer match current state. | Git state, branch state, merge status, roadmap status. | Is the status still true for the relevant repo state? | Do not infer current status from old planning notes. |
| `version_stale` | A version or release claim may be outdated. | Version file, tag, changelog, release note, log evidence. | Which version does the claim describe? | Do not infer successor versions. |
| `role_or_owner_stale` | A role, owner, reviewer, maintainer, or responsibility claim may have changed. | Ownership docs, review notes, project records. | Is this role still assigned and in scope? | Do not infer current authority from old role text. |
| `market_or_price_stale` | Price, market, ranking, popularity, or demand claims may change quickly. | Dated source or review note. | Is the claim still current enough for review? | Do not infer current price, ranking, stars, forks, or demand. |
| `legal_or_policy_stale` | Law, policy, terms, compliance, or safety claims may change. | Dated policy source, legal review note, jurisdiction scope. | Does this require fresh review before use? | Do not infer legal or policy advice. |
| `user_preference_stale` | A user preference may have changed. | User correction, dated instruction, project preference note. | Is the preference still current and scoped? | Do not freeze the user to old preferences. |
| `workflow_stale` | A command, process, approval path, or review route may have changed. | Current docs, local commands, recent task evidence. | Does the workflow still apply to this workspace? | Do not infer old workflow authority. |
| `environment_stale` | Tooling, credentials, network state, branch, dependency, or OS state may have changed. | Local environment check, failure record, branch state. | Is the environment condition still present? | Do not infer permanent failure. |
| `unknown_staleness` | Staleness risk cannot be judged from available evidence. | Missing timestamp, missing source, missing scope. | Should use be blocked until review? | Do not infer safe current use. |

## 12. Supersession Model Candidates

Candidate supersession rules:

- newer source may supersede older source only after review;
- more specific source may supersede generic source only after review;
- user correction may supersede assistant assumption only after review;
- repo git state may supersede prior planning doc only after review;
- merged PR may supersede branch-state assumption only after review;
- supersession must preserve old record;
- supersession must record why replacement is safe;
- supersession must not delete audit trail.

Supersession is a reviewed relationship between claims.

It is not an automatic replacement mechanism.

It is not permission to delete history.

It is not a durable write by itself.

## 13. Conflict Model Candidates

| Conflict type | What it means | Evidence required | Review action | Prohibited inference |
| --- | --- | --- | --- | --- |
| direct conflict | Two claims cannot both be true under the same scope. | Both claims, sources, time scope, and conflict note. | Block current use or choose a reviewed scope. | Do not pick a winner automatically. |
| partial conflict | Claims overlap but differ in one field, scope, or condition. | Overlap description, differing fields, source references. | Narrow the scope or mark review required. | Do not flatten the claims into one. |
| scope conflict | Claims apply to different branches, projects, roles, users, environments, or versions. | Scope evidence for each claim. | Separate scopes before use. | Do not generalize one scope to all. |
| time conflict | Claims disagree because they come from different observation times. | `observed_at`, `source_timestamp`, or event order. | Decide whether one is historical only, stale, or current reviewed. | Do not infer newer means true. |
| source conflict | Sources disagree or have different trust levels. | Source references, trust notes, provenance notes. | Compare source authority and require review. | Do not treat citation count as truth. |
| interpretation conflict | The same evidence supports multiple readings. | Evidence text, interpretation notes, uncertainty note. | Record ambiguity and require human review. | Do not convert interpretation into fact. |
| unknown conflict | Conflict risk is suspected but not enough evidence exists. | Missing evidence note and risk reason. | Mark blocked or review required. | Do not infer safe use. |

## 14. Failed Attempt Temporal Validity

Failed-attempt memory should age.

A failure may be valid only for a tool version.

A failure may be valid only for a repo state.

A failure may be valid only for a branch.

A failure may be valid only for a network condition.

A failure may be valid only for a user preference.

Do-not-retry must include time/scope notes.

Old failures may become historical only.

Failed-attempt memory must not freeze future improvement.

Future failed-attempt docs should distinguish "do not repeat this exact path under the same conditions" from "this path can never work." The first may be useful memory. The second requires strong evidence and human review.

## 15. Connector and External Source Temporal Risk

External sources and connectors have temporal risks:

| Risk | Meaning | Safe model response |
| --- | --- | --- |
| source last updated unknown | The source may be stale but lacks visible update time. | Mark unknown time scope and require review. |
| source stale but still retrieved | Retrieval may surface old source material as if current. | Mark stale candidate or historical only. |
| connector sync lag | A connector may not reflect the latest source state. | Require sync-time evidence before current use. |
| repeated sync conflict | Multiple sync results may disagree over time. | Record conflict source and block temporal use until review. |
| external API behavior changes | External behavior may change without local code changes. | Treat behavior claims as time-bound. |
| credential or permission time window | Access may depend on temporary credential or permission state. | Record scope and review before reuse. |
| legal/policy change | Legal, policy, or terms context may change. | Require fresh human review. |
| price/market data volatility | Prices and market data can change quickly. | Do not reuse without current evidence. |
| repo activity volatility | Stars, forks, watchers, issues, PRs, releases, and commit status can change. | Treat as dated snapshot only. |
| web source volatility | Web pages can change, disappear, or be rewritten. | Preserve source timestamp or mark unknown. |

This document adds no connector, adapter, MCP/API surface, sync behavior, or action behavior.

## 16. Human Review Gate Readiness for Temporal Claims

Before any later P4 consideration, a human reviewer must be able to see:

- `observed_at`;
- `source_timestamp`;
- `valid_from` / `valid_until` if known;
- `unknown_time_scope`;
- `stale_reason`;
- `superseded_by`;
- `conflict_source`;
- whether a claim should be marked `historical_only`;
- whether temporal use should be blocked without side effect;
- that reviewer decision is recorded as candidate only.

P4 remains paused.

P4 requires explicit human confirmation later.

Human review readiness means the reviewer can inspect and decide. It does not mean the system can write, update, delete, expire, query, supersede, execute, or authorize automatically.

## 17. Candidate Examples

These examples are illustrative only.

| Claim type | Likely temporal risk | Required temporal fields | Safe candidate status | Prohibited inference |
| --- | --- | --- | --- | --- |
| project version claim | Version may change after observation. | `observed_at`, `source_timestamp`, `temporal_scope_note`. | `time_bound` or `current_candidate`. | Do not infer successor version or release continuation. |
| merged PR status | Branch and merge state may change. | `observed_at`, source reference, `temporal_scope_note`. | `current_candidate` until reviewed. | Do not infer future branch state. |
| external repo popularity claim | Stars, forks, watchers, and activity can change. | `observed_at`, `source_timestamp` if available, `unknown_time_scope` if missing. | `historical_only` or `blocked_temporal_use` without current evidence. | Do not infer live popularity. |
| product price claim | Price may change by time, region, or plan. | `observed_at`, source reference, `valid_until` if known. | `time_bound` or `blocked_temporal_use`. | Do not infer current price. |
| user preference claim | User preference may change. | `observed_at`, source/user note, `review_required`. | `current_candidate` or `unknown_time_scope`. | Do not freeze old preference as permanent. |
| failed command memory | Failure may depend on environment, version, branch, or network. | `observed_at`, environment scope, `blocked_reason`. | `historical_only` or scoped do-not-retry candidate. | Do not infer permanent impossibility. |
| legal/policy claim | Legal and policy context can change. | `observed_at`, `source_timestamp`, jurisdiction/scope note. | `blocked_temporal_use` until review. | Do not infer legal advice. |
| tool login status | Credential and session state can change. | `observed_at`, environment scope, `valid_until` if known. | `current_candidate` only with current check. | Do not infer future access. |

## 18. Candidate Future Sequence

Recommended docs-only sequence:

1. Memory Lifecycle Taxonomy
2. Failed Attempt Memory / Do-Not-Retry Rules
3. Explainable Recall Trace Template
4. Connector Governance Taxonomy
5. Memory Ontology Mapping
6. External Product Explanation Candidate
7. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

## 19. Prohibited Implementation Rules

Do not implement temporal storage.

Do not implement temporal query engine.

Do not implement stale-memory detector.

Do not implement automatic expiration.

Do not implement supersession engine.

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

Do not treat temporal confidence as approval.

Do not treat freshness as truth.

Do not treat newer source as automatic supersession.

## 20. Stop Conditions

If temporal model turns into code, stop.

If temporal model turns into tests, stop.

If temporal model turns into stale detector, stop.

If temporal model turns into expiration logic, stop.

If temporal model turns into temporal query engine, stop.

If temporal model turns into Memory Graph mutation, stop.

If temporal model turns into durable writer, stop.

If temporal model turns into dependency adoption, stop.

If temporal model turns into adapter work, stop.

If temporal model turns into MCP/API operation surface, stop.

If temporal model turns into authorization/execution semantics, stop.

If temporal model starts P4, stop.

If temporal model starts v7 implementation, stop.

If temporal model starts MVP/product deployment, stop.

If temporal model starts changing old docs, stop.

If `pyproject.toml` version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 21. Final Model Statement

This document defines temporal validity candidates only.

It does not evaluate live memory.

It does not implement temporal behavior.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
