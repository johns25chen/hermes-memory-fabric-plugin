# Civilization Core Explainable Recall Trace Template / 文明之核可解释召回轨迹模板

## 2. Template Status

This is a docs-only explainable recall trace template document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates document.

It is based on the merged Temporal Validity Model document.

It is based on the merged Memory Lifecycle Taxonomy document.

It is based on the merged Failed Attempt Memory / Do-Not-Retry Rules document.

It is trace-template candidate only.

It creates no recall storage.

It creates no recall engine.

It creates no retrieval logic.

It creates no ranking logic.

It creates no trace persistence.

It creates no source graph traversal.

It creates no automated explanation generation.

It creates no approval logic.

It creates no authorization logic.

It creates no execution logic.

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

The template in this document is candidate governance vocabulary only. It does not approve implementation, productization, connector adoption, dependency adoption, external project behavior, durable memory writing, graph mutation, automatic authorization, automatic explanation, automatic approval, or automatic execution.

## 3. Why Explainable Recall Matters

Memory recall without explanation can look like authority.

A recalled memory must show why it surfaced before a reviewer treats it as useful.

The source path must be visible so the reviewer can inspect where the recalled item came from.

Evidence, claim, and inference must be separated. Evidence is what the source shows. Claim is what the memory says. Inference is what a reviewer or assistant derives from evidence and claim.

Temporal validity must be visible so old, time-bound, stale, superseded, conflicted, or historical-only material does not appear current by accident.

Lifecycle state must be visible so proposed, candidate, approved candidate, active reviewed, stale, superseded, rejected, blocked, and historical-only records are not collapsed into one generic "memory" label.

Failed-attempt and do-not-retry status must be visible when relevant so failed paths can reduce repeated waste without becoming hidden law.

Connector and source risk must be visible so external snapshots, connector results, source lag, missing timestamps, or overread benchmark references do not become approved memory.

Explanation is not approval.

Explanation is not authorization.

Explanation is not execution permission.

Human review remains required before a recalled item is trusted, promoted, blocked, rejected, used as current guidance, or routed into any later governance decision.

## 4. Explainable Recall Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| recall reason | yes | A reviewer needs to know why the item surfaced. | Candidate label only; it is not retrieval behavior. |
| source path | yes | Source visibility prevents unsupported authority. | Human-readable path only; no source graph traversal follows. |
| evidence excerpt summary | yes | The trace should show what the source supports. | Summary only; it is not source adoption or truth by itself. |
| claim summary | yes | The trace should show what the memory says. | Claim text remains reviewable and may be wrong. |
| inference note | yes | Derived reasoning must be marked. | Inference is not fact, approval, or permission. |
| temporal status | yes | Time scope controls stale and historical use. | Candidate status only; no temporal query behavior follows. |
| lifecycle status | yes | Reviewers need candidate, approved, stale, blocked, and historical labels. | Candidate label only; no lifecycle storage or transition behavior follows. |
| failed-attempt status | yes | Failed paths need scope before reuse. | Trace label only; no failed-attempt storage follows. |
| do-not-retry status | yes | Risky retries need visible candidate status. | Candidate note only; no enforcement follows. |
| conflict note | yes | Disagreement must be surfaced before trust. | Trace does not resolve the conflict. |
| uncertainty note | yes | Unknowns must not be hidden. | Trace does not remove uncertainty. |
| confidence note | yes | Reviewer needs qualitative evidence strength. | Confidence is not approval or score automation. |
| connector/source risk note | yes | External or connector-derived material can be stale, lagged, or overread. | Risk note only; no connector or adapter follows. |
| human review readiness | yes | The trace should show whether a reviewer can inspect the item safely. | Readiness is candidate status only; review remains human. |
| approval decision | no | Approval requires separate explicit human scope. | Excluded; no approval decision is created. |
| authorization decision | no | Authorization is a separate governance act. | Excluded; no authorization decision is created. |
| execution decision | no | Execution cannot follow from recall explanation. | Excluded; no execution decision is created. |
| recall engine | no | Engine behavior would be implementation. | Excluded; no recall engine is created. |
| retrieval logic | no | Retrieval behavior would be implementation. | Excluded; no retrieval logic is created. |
| ranking logic | no | Ranking behavior would be implementation. | Excluded; no ranking logic is created. |
| trace persistence | no | Persistence would create durable behavior. | Excluded; no trace persistence is created. |
| Memory Graph mutation | no | Graph writes would change durable memory surfaces. | Excluded; no Memory Graph mutation is created. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Recall Trace Object Types

These object types may later receive recall trace labeling in docs or review packets. This section defines vocabulary only, not schema or behavior.

| Object type | What it is | Recall explanation question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| recalled memory candidate | A proposed memory item surfaced for review. | Why did this unapproved candidate surface? | Claim, source reference, recall reason, temporal and lifecycle notes. | Do not infer truth, approval, durable write, or current authority. |
| recalled approved memory record | A future human-scoped approved candidate or reviewed record surfaced for context. | Does the approval scope match the current question? | Reviewer note, source path, lifecycle state, temporal scope. | Do not infer indefinite validity or execution permission. |
| recalled stale memory record | A record surfaced because it may be old or unsafe for current use. | Why might this memory be stale, and what source shows that risk? | Stale reason, observed time or source time, conflict or newer source note. | Do not infer deletion or automatic replacement. |
| recalled superseded memory record | A prior record surfaced because later evidence may narrow or replace it. | What later evidence may supersede the old claim? | Old claim, successor reference, `superseded_by`, reviewer note if available. | Do not infer erasure, overwrite, or hidden mutation. |
| recalled historical-only record | A record surfaced as past context, not current guidance. | Why is this history rather than current instruction? | Temporal scope note, historical reason, source path. | Do not infer current authority or uselessness. |
| recalled failed attempt record | A failed action, command, assumption, tool behavior, or workflow surfaced as warning context. | What failed, under which conditions, and why is it relevant now? | Attempt summary, failure signal, actual result, scope, observed time if known. | Do not infer permanent impossibility or automatic block. |
| recalled do-not-retry candidate | A candidate rule surfaced because a similar retry may be risky. | What exact retry is risky under which stated conditions? | Failed attempt reference, blocked behavior, retry risk, exception condition. | Do not infer automatic law or indefinite ban. |
| recalled external source candidate | An external methodology or source snapshot surfaced for comparison or context. | What source role does it play, and what must not be overread? | Source name, source class, source timestamp or unknown marker, risk note. | Do not infer live fact, dependency, adapter, or adoption. |
| recalled connector/source candidate | A connector, sync, source, API, or external surface candidate surfaced for risk review. | What source or connector risk should a reviewer see? | Source type, source location, trust/sync/timestamp notes, risk flags. | Do not infer connector implementation, MCP/API surface, sync, or action behavior. |
| recall trace packet | A human-readable packet explaining why recall happened and how to review it. | Can the reviewer see reason, source path, evidence, claim, inference, status, conflict, and risk? | Trace fields, evidence summary, source path, uncertainty note, recommended next state. | Do not infer storage, automation, approval, or authorization. |
| human review decision | A future human-scoped decision about how to treat a recalled item. | What did the reviewer decide, and with what scope? | Evidence packet, reviewer note, decision scope, recommended next state. | Do not infer execution, durable write, deployment, or P4 activation. |

## 6. Recall Trace Field Template

This is a document template only, not schema implementation.

| Field | Meaning | When required | Evidence requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `trace_id` | Document-local identifier for the explanation packet. | Required when multiple traces may be compared. | Human-assigned or review-packet identifier. | Do not infer durable storage or global identity. |
| `recall_context` | Plain-language context that led to recall. | Required for every trace packet. | User question, review need, task scope, or operator context. | Do not infer retrieval logic. |
| `user_or_operator_question` | The question the recall is meant to help answer. | Required when a trace responds to a human prompt or review task. | Exact or summarized question. | Do not infer that recall answered it correctly. |
| `recalled_item_id` | Identifier for the surfaced item. | Required when available. | Existing local ID, document-local ID, or explicit unknown marker. | Do not infer durable memory record. |
| `recalled_item_type` | Object type of the surfaced item. | Required for every trace packet. | One of the trace object types or a documented extension. | Do not infer lifecycle approval from type alone. |
| `recall_reason` | Candidate label explaining why the item surfaced. | Required for every trace packet. | Evidence-backed reason from the vocabulary below or `unknown_recall_reason`. | Do not infer ranking or retrieval behavior. |
| `source_reference` | Inspectable source reference supporting the trace. | Required for reviewable traces. | Local doc path, user message reference, command output summary, or future-approved source descriptor. | Do not treat citation as approval. |
| `source_path` | Human-readable path from source to recalled item. | Required when provenance matters. | Source type, location, extraction step, transformation note, inference marker. | Do not infer source graph traversal or Memory Graph mutation. |
| `evidence_summary` | Summary of what the source shows. | Required for claim-bearing traces. | Source-backed evidence in bounded prose. | Do not convert evidence into truth or permission. |
| `claim_summary` | Summary of what the recalled item says. | Required when the recalled item contains a claim. | Claim text or faithful summary with source reference. | Do not treat claim as fact. |
| `inference_note` | Marked reasoning derived from evidence and claim. | Required when any derivation occurs. | Explicit note that this is inference and why it follows. | Do not present inference as source fact. |
| `temporal_status` | Time-scope label such as current candidate, time-bound, stale, superseded, historical, conflicted, or unknown. | Required when time could affect use. | `observed_at`, `source_timestamp`, validity note, stale reason, or unknown marker. | Do not infer current validity. |
| `observed_at` | When the source or claim was observed. | Required when known for volatile, repo-state, external, failed-attempt, or status claims. | Local observation note, git evidence, source timestamp, or explicit unknown marker. | Do not infer the claim remains current. |
| `source_timestamp` | Timestamp attached to the source itself. | Required when the source provides one or time risk matters. | Source-visible timestamp, local file/git evidence, or unknown marker. | Do not infer current truth from source time. |
| `lifecycle_state` | Candidate lifecycle label for the recalled item. | Required when trust state matters. | Lifecycle evidence, reviewer note if reviewed, or unknown marker. | Do not infer automatic active memory. |
| `failed_attempt_status` | Whether the item relates to a failed attempt. | Required when failure evidence appears. | Attempt summary, failure signal, actual result, scope, or not-applicable marker. | Do not infer permanent impossibility. |
| `do_not_retry_status` | Whether the item relates to do-not-retry candidate guidance. | Required when retry risk appears. | Blocked path, blocked reason, exception condition, review requirement. | Do not infer enforcement. |
| `conflict_note` | Direct, partial, time, source, interpretation, or unknown conflict note. | Required when disagreement or missing comparison exists. | Conflict source, conflict summary, or unknown conflict marker. | Do not choose a winner automatically. |
| `uncertainty_note` | What remains unknown or weak. | Required when evidence is incomplete or scope is unclear. | Missing source, missing time, missing reviewer, unknown scope, or confidence gap. | Do not hide uncertainty. |
| `confidence_note` | Qualitative evidence-strength note. | Recommended for every trace; required for high-risk use. | Evidence quality explanation, not numeric automation. | Do not treat confidence as approval. |
| `connector_source_risk` | Risk from external source, connector, sync, API, snapshot, or source class. | Required for external or connector-derived traces. | Risk type and source basis. | Do not infer connector adoption. |
| `reviewer_note` | Human review comment or decision note. | Required only when human review occurred. | Explicit reviewer note and scope. | Do not infer execution permission. |
| `recommended_next_state` | Candidate next lifecycle or review state. | Recommended for review packets. | Rationale tied to evidence, risk, and uncertainty. | Do not infer automatic transition. |
| `prohibited_action` | Action that must not follow from the trace. | Required for high-risk traces. | Boundary source, risk note, or task constraint. | Do not treat prohibition text as implementation logic. |

These fields create no storage format, parser, validator, trace database, source graph traversal, recall engine, retrieval logic, ranking logic, temporal query engine, lifecycle state machine, failed-attempt store, durable writer, API, adapter, or graph mutation.

## 7. Evidence / Claim / Inference Separation

Evidence is what the source shows.

Claim is what the memory says.

Inference is what the reviewer or assistant derives from evidence and claim.

Inference must be marked as inference.

Uncertainty must be visible.

Source absence must be visible.

Conflicting evidence must be visible.

An explanation must not convert inference into fact.

An explanation must not convert evidence into approval.

An explanation must not convert recall into permission.

Evidence excerpt summaries should be conservative. If the source is missing, stale, incomplete, or only partially relevant, the trace must say so rather than filling the gap.

Claim summaries should preserve scope. A claim about one branch, one date, one tool version, one operator instruction, one source snapshot, or one failed command must not be broadened into a universal rule.

Inference notes should show the reasoning step and the uncertainty. If the reasoning depends on reviewer judgment, the trace must keep the decision candidate-only.

## 8. Recall Reason Vocabulary

These are candidate recall reason labels only. They create no recall engine, retrieval behavior, ranking behavior, or automated explanation behavior.

| Recall reason | Meaning | Allowed use | Required evidence | Human review requirement | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| `direct_source_match` | The item directly matches a source phrase, identifier, path, or known local artifact. | Use when source and item visibly align. | Source reference and evidence summary. | Required before trust or use. | Do not infer truth or approval. |
| `project_context_match` | The item matches the current project, branch, file, stage, or task context. | Use for repo-local or project-scoped recall. | Project context, source path, and scope note. | Required before current guidance. | Do not infer future repo state. |
| `temporal_relevance` | The item matters because time, version, observation, or staleness affects use. | Use when time scope is central. | `observed_at`, `source_timestamp`, validity note, stale or unknown marker. | Required before current use. | Do not infer temporal approval. |
| `lifecycle_relevance` | The item matters because candidate, approved, stale, superseded, rejected, blocked, or historical state affects interpretation. | Use when trust state controls use. | Lifecycle label and supporting source or reviewer note. | Required before trust. | Do not infer automatic active memory. |
| `failed_attempt_relevance` | The item matters because a prior failed attempt may inform review. | Use when failure evidence or retry risk is relevant. | Attempt summary, failure signal, scope, actual result if known. | Required before treating as guidance. | Do not infer permanent impossibility. |
| `do_not_retry_relevance` | The item matters because a do-not-retry candidate may apply. | Use when a same-scope retry could repeat a failed path. | Failed attempt reference, blocked path, blocked reason, exception condition. | Required before any block. | Do not infer automatic law. |
| `conflict_warning` | The item surfaced because conflict may affect use. | Use when sources, times, scopes, or interpretations disagree. | Conflict note and source path or unknown marker. | Required before deciding. | Do not choose a winner automatically. |
| `stale_warning` | The item surfaced because it may be out of date. | Use for volatile claims or old source material. | Stale reason and temporal evidence or unknown marker. | Required before current use. | Do not infer deletion. |
| `supersession_warning` | The item surfaced because later or narrower evidence may supersede it. | Use when successor evidence exists or is suspected. | Old claim, successor reference if known, supersession rationale. | Required before replacement. | Do not infer erasure or overwrite. |
| `historical_context` | The item surfaced as past context. | Use when a record explains prior state but should not guide current action. | Historical reason and temporal scope. | Required if decision-impacting. | Do not infer current authority. |
| `user_preference_context` | The item surfaced because a user instruction or preference may affect interpretation. | Use only with scoped user preference evidence. | User instruction, correction, observed context, or unknown-time note. | Required if preference controls action. | Do not freeze old preference as permanent. |
| `connector_source_context` | The item surfaced because a connector, external source, sync, API, or source snapshot is relevant. | Use for external or connector-derived material. | Source type, source location, source time or unknown marker, risk note. | Required before use. | Do not infer connector adoption or live source truth. |
| `governance_boundary_context` | The item surfaced because a boundary rule affects safe interpretation. | Use for no-write, no-authorization, no-execution, no-v6.17, no-P4, or similar boundaries. | Boundary source and prohibited inference. | Required before proceeding near boundary. | Do not infer implementation permission. |
| `unknown_recall_reason` | The reason cannot be reliably explained from available evidence. | Use when reason is missing or weak. | Missing-reason note and known evidence gaps. | Required before trust or use. | Do not infer relevance, truth, approval, or permission. |

## 9. Source Path Template

Future docs may describe source paths with this candidate template:

| Source path element | Meaning | Required note |
| --- | --- | --- |
| `source_type` | Local doc, user instruction, git evidence, command output, external snapshot, connector result, or review packet. | Mark external, connector, and volatile sources explicitly. |
| `source_location` | Human-readable path, file, section, message, command, or source descriptor. | Use inspectable local paths when available. |
| `source_timestamp` | Timestamp from the source when known. | Mark unknown when missing. |
| `observed_at` | When the source state was observed. | Mark unknown when not recorded. |
| `extracted_evidence` | What was extracted from the source. | Keep evidence separate from claim and inference. |
| `transformation_note` | How evidence became a memory candidate or trace summary. | Do not hide summarization, compression, or selection. |
| `inference_step` | Any derived reasoning. | Mark as inference, not source fact. |
| `uncertainty_step` | Missing source, missing time, conflict, low confidence, or scope gap. | Make uncertainty visible. |
| `reviewer_step` | Human review note if one exists. | Do not invent review. |
| `final_trace_note` | Conservative explanation of why the item surfaced and what must not be inferred. | Must not authorize action. |

No source graph traversal is implemented.

No connector is added.

No Memory Graph mutation is added.

No durable writer is added.

## 10. Temporal Validity Trace Requirements

Recall traces must show temporal validity when time, version, branch, tool, source state, user preference, or external volatility could affect interpretation.

`observed_at` should be visible when known.

`source_timestamp` should be visible when known.

`valid_from` should be visible when known.

`valid_until` should be visible when known.

`unknown_time_scope` must be visible when time scope is not reliable.

`stale_reason` must be visible if stale or stale-candidate status is relevant.

`superseded_by` must be visible if superseded or supersession-candidate status is relevant.

`conflict_source` must be visible if conflict exists.

`historical_only` must be visible when current use is unsafe.

Temporal confidence is not approval.

A trace may say that a memory was observed at a known time, has a source timestamp, appears time-bound, or may be stale. It must not claim that the memory is current unless the trace has evidence and human review scope for that current-use claim.

## 11. Lifecycle Trace Requirements

Recall traces must show lifecycle state when trust, review, staleness, supersession, rejection, blocking, or historical use affects interpretation.

`proposed` / `candidate` must be visibly unapproved.

`approved_candidate` must not be treated as automatic active memory.

`active_reviewed` must remain scoped.

`active_time_bound` must show time/scope boundary.

`stale_candidate` must not be treated as deletion.

`superseded` must not be treated as erasure.

`rejected` must not be hidden.

`blocked` must show `blocked_reason`.

`historical_only` must show why it is history, not current guidance.

Lifecycle confidence is not approval.

Lifecycle labels are document vocabulary for review. They do not create lifecycle storage, lifecycle state machine behavior, transition behavior, active memory use, deletion, archival, or durable mutation.

## 12. Failed Attempt / Do-Not-Retry Trace Requirements

Recall traces must show failed-attempt and do-not-retry status when a recalled item warns about a failed path, risky retry, rejected assumption, failed command, failed workflow, or old blocked action.

Failed attempt evidence must be visible.

`attempted_action` must be visible when known.

`actual_result` or `failure_signal` must be visible.

`tool_version` should be visible when relevant.

`repo_state` should be visible when relevant.

`branch_name` should be visible when relevant.

`retry_risk` must be visible when relevant.

`blocked_reason` must be visible when relevant.

`exception_condition` must be visible when known.

Do-not-retry starts as candidate, not law.

Failed attempt must not become proof of impossibility.

Old failures may be `historical_only`.

A valid failed-attempt trace explains what failed, under what conditions, what evidence showed the failure, and what must not be retried without review. It does not block adjacent improved approaches and does not enforce anything automatically.

## 13. Conflict and Uncertainty Trace Requirements

Direct conflict must be visible.

Partial conflict must be visible.

Time conflict must be visible.

Source conflict must be visible.

Interpretation conflict must be visible.

Unknown conflict must be visible.

Uncertainty must be shown instead of hidden.

The trace must not choose a winner automatically.

The trace must not present unresolved conflict as fact.

Conflict notes should identify whether the conflict is between sources, times, scopes, reviewer interpretations, lifecycle states, failed-attempt outcomes, or missing evidence. If the conflict type is unknown, the trace must say unknown rather than silently resolving it.

## 14. Connector and External Source Trace Risk

External and connector-derived material can be useful as methodology or evidence, but it can also be overread. Recall traces must make these risks visible when relevant.

| Risk | Meaning | Required trace response | Prohibited inference |
| --- | --- | --- | --- |
| stale external source | The source snapshot may no longer be current. | Show source time, observed time, and stale risk. | Do not infer live fact. |
| connector sync lag | Connector result may lag behind source state. | Show sync uncertainty or unknown marker. | Do not infer current source truth. |
| missing source timestamp | The source lacks reliable time metadata. | Show `unknown_time_scope`. | Do not infer evergreen validity. |
| source trust overestimated | Source existence may be mistaken for authority. | Show trust and review requirement. | Do not infer approval. |
| external API behavior changed | External behavior may differ from prior observation. | Show observation scope and review need. | Do not infer current API behavior. |
| web source disappeared or changed | Web content may be unavailable or modified later. | Show snapshot/source uncertainty. | Do not infer stable evidence. |
| external benchmark overread as local approval | A benchmark reference may be mistaken for governance approval. | Show benchmark reference as evidence only. | Do not infer local benchmark approval. |
| connector result treated as approved memory | A connector output may be mistaken for reviewed memory. | Show candidate lifecycle state. | Do not infer approved memory. |
| source snapshot treated as live memory | A source snapshot may be mistaken for current recall. | Show source snapshot status and temporal risk. | Do not infer live memory. |

No connector, adapter, MCP/API surface, sync behavior, action behavior, trace persistence, or enforcement behavior is added.

## 15. Human Review Gate Readiness for Recall Traces

Before any later P4 consideration, a recall trace is review-ready only if:

- reviewer can see why the memory surfaced;
- reviewer can see source path;
- reviewer can see evidence summary;
- reviewer can see claim summary;
- reviewer can see inference note;
- reviewer can see temporal status;
- reviewer can see lifecycle state;
- reviewer can see failed-attempt / do-not-retry status when relevant;
- reviewer can see conflict and uncertainty notes;
- reviewer can reject the recall without side effect;
- reviewer can block use without side effect;
- reviewer decision is recorded as candidate only;
- P4 remains paused;
- P4 requires explicit human confirmation later.

Review readiness means a human can inspect a bounded trace. It does not mean the trace is approved, trusted, authorized, persisted, or executable.

## 16. Non-Authorization Rules

Recall is not truth.

Trace is not approval.

Explanation is not authorization.

Evidence is not execution permission.

Confidence is not approval.

Source path is not governance approval.

Historical context is not current guidance.

Do-not-retry trace is not automatic law.

Connector source trace is not connector adoption.

Benchmark reference is not local benchmark approval.

No recall trace may collapse evidence, claim, inference, review, approval, authorization, and execution into one state.

## 17. Candidate Examples

These examples are illustrative only. They are generic examples, not live facts, not current status claims, and not implementation scenarios.

| Example | Recalled item type | Likely recall reason | Required trace fields | Safe reviewer action | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| recalled current project version memory | recalled approved memory record or recalled memory candidate | `project_context_match` / `temporal_relevance` | `source_reference`, `source_path`, `claim_summary`, `temporal_status`, `observed_at`, `lifecycle_state` | Verify local package/version evidence before use. | Do not infer successor version or future release. |
| recalled merged PR status | recalled historical-only record or recalled approved memory record | `project_context_match` / `historical_context` | `source_reference`, `evidence_summary`, `claim_summary`, `observed_at`, `temporal_status` | Treat as repo-state context and recheck if current status matters. | Do not infer future branch state. |
| recalled stale product price memory | recalled stale memory record | `stale_warning` / `temporal_relevance` | `source_timestamp`, `observed_at`, `stale_reason`, `uncertainty_note` | Mark review required before any current use. | Do not infer current price. |
| recalled old failed command memory | recalled failed attempt record | `failed_attempt_relevance` | `attempted_action`, `actual_result`, `failure_signal`, `repo_state`, `branch_name`, `observed_at` | Compare scope before retry. | Do not infer all related commands fail. |
| recalled do-not-retry candidate | recalled do-not-retry candidate | `do_not_retry_relevance` | `blocked_reason`, `retry_risk`, `exception_condition`, `reviewer_note` if available | Pause same-scope retry until review. | Do not infer automatic enforcement. |
| recalled rejected assistant assumption | recalled historical-only record or recalled failed attempt record | `conflict_warning` / `user_preference_context` | `claim_summary`, `evidence_summary`, `conflict_note`, `reviewer_note` if available | Preserve correction and avoid repeating the same assumption. | Do not infer deletion of all related context. |
| recalled external repo popularity snapshot | recalled external source candidate | `connector_source_context` / `stale_warning` | `source_timestamp`, `observed_at`, `connector_source_risk`, `uncertainty_note` | Treat as dated snapshot requiring fresh review. | Do not infer current stars, forks, watchers, or ranking. |
| recalled connector source result | recalled connector/source candidate | `connector_source_context` | `source_type`, `source_location`, `connector_source_risk`, `temporal_status`, `lifecycle_state` | Review source trust, sync, and candidate status. | Do not infer connector adoption, sync behavior, or approved memory. |

## 18. Candidate Future Sequence

The safe docs-only sequence after this template, if separately requested and explicitly scoped later, is:

1. Connector Governance Taxonomy
2. Memory Ontology Mapping
3. External Product Explanation Candidate
4. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

## 19. Prohibited Implementation Rules

Do not implement recall storage.

Do not implement recall engine.

Do not implement retrieval logic.

Do not implement ranking logic.

Do not implement trace persistence.

Do not implement source graph traversal.

Do not implement automated explanation generation.

Do not implement approval logic.

Do not implement authorization logic.

Do not implement execution logic.

Do not implement failed-attempt storage.

Do not implement do-not-retry enforcement.

Do not implement lifecycle storage.

Do not implement lifecycle state machine.

Do not implement lifecycle transition engine.

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

Do not treat recall as truth.

Do not treat trace as approval.

Do not treat explanation as authorization.

Do not treat evidence as execution permission.

Do not treat connector source trace as connector adoption.

## 20. Stop Conditions

If explainable recall template turns into code, stop.

If explainable recall template turns into tests, stop.

If explainable recall template turns into recall storage, stop.

If explainable recall template turns into recall engine, stop.

If explainable recall template turns into retrieval logic, stop.

If explainable recall template turns into ranking logic, stop.

If explainable recall template turns into trace persistence, stop.

If explainable recall template turns into source graph traversal, stop.

If explainable recall template turns into automated explanation generation, stop.

If explainable recall template turns into approval logic, stop.

If explainable recall template turns into authorization/execution semantics, stop.

If explainable recall template turns into Memory Graph mutation, stop.

If explainable recall template turns into durable writer, stop.

If explainable recall template turns into dependency adoption, stop.

If explainable recall template turns into adapter work, stop.

If explainable recall template turns into MCP/API operation surface, stop.

If explainable recall template starts P4, stop.

If explainable recall template starts v7 implementation, stop.

If explainable recall template starts MVP/product deployment, stop.

If explainable recall template starts changing old docs, stop.

If pyproject version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 21. Final Template Statement

This document defines explainable recall trace template candidates only.

It does not evaluate live memory.

It does not implement recall behavior.

It does not implement trace persistence.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
