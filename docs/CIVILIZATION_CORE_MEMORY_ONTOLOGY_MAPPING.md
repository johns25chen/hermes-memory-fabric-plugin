# Civilization Core Memory Ontology Mapping / 文明之核记忆本体映射

## 2. Mapping Status

This is a docs-only memory ontology mapping document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates.

It is based on the merged Temporal Validity Model.

It is based on the merged Memory Lifecycle Taxonomy.

It is based on the merged Failed Attempt Memory / Do-Not-Retry Rules.

It is based on the merged Explainable Recall Trace Template.

It is based on the merged Connector Governance Taxonomy.

It is ontology-mapping candidate only.

It creates:

- no ontology storage
- no ontology schema implementation
- no graph database behavior
- no Memory Graph behavior
- no Memory Graph mutation
- no graph traversal
- no ontology query logic
- no relationship inference
- no automatic classification
- no automatic mapping
- no automatic promotion
- no automatic memory writing
- no connector logic
- no connector storage
- no connector sync
- no API calls
- no MCP tools
- no adapter behavior
- no recall storage
- no recall engine
- no retrieval logic
- no ranking logic
- no trace persistence
- no benchmark implementation
- no evaluation runner
- no tests
- no code changes
- no README changes
- no existing doc changes
- no package version change
- no tag
- no `v6.17`
- no v7 implementation authorization
- no P4 start
- no product implementation authorization
- no MVP
- no runtime / dependency / adapter activation
- no MCP/API operation surface
- no durable writer
- no authorization/execution semantics

The mapping below is vocabulary for future human review only. It is not implementation approval, not product approval, not active Star-Source Memory behavior, not active Layer 15 behavior, and not permission to automate memory classification.

## 3. Why Memory Ontology Mapping Matters

The recent memory governance documents now define multiple vocabularies: candidate evaluation, temporal validity, lifecycle state, failed attempts, do-not-retry rules, explainable recall traces, and connector/source governance.

Without a mapping layer, object types can drift or be confused. A memory candidate, temporal status, lifecycle state, failed attempt, recall trace, and connector source are different objects with different review questions.

Relationship words must not imply graph mutation. A word such as `supports`, `contradicts`, or `supersedes` can help a reviewer name a relation, but it does not create a graph edge, graph traversal path, relationship inference, or Memory Graph mutation.

Evidence, claim, inference, review, approval, authorization, and execution must remain separate. Evidence may support a claim. A claim may become a memory candidate. An inference may explain why evidence matters. None of those becomes approval, authorization, execution permission, or durable memory writing by vocabulary alone.

Ontology mapping helps reviewers understand what kind of memory object they are looking at before they decide whether the item is source evidence, a candidate claim, a lifecycle label, a time-scope warning, a failed-attempt warning, a recall explanation packet, a connector/source snapshot, or an evaluation question.

Ontology mapping is not a schema.

Ontology mapping is not a Memory Graph.

Ontology mapping is not permission to automate.

Human review remains required before any future memory object is trusted, promoted, approved, blocked, written, queried, retrieved, connected, or used as decision input.

## 4. Ontology Mapping Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| object family vocabulary | yes | Reviewers need high-level families before classifying objects. | Vocabulary only; no storage or schema follows. |
| object type vocabulary | yes | Reviewers need names for candidate memory-related objects. | Candidate labels only; no automatic classification. |
| relationship vocabulary | yes | Reviewers need bounded words for source, claim, conflict, and review relations. | Relationship words only; not graph edges or traversal. |
| attribute vocabulary | yes | Reviewers need shared field names for evidence packets. | Document fields only; not implemented schema. |
| evidence/claim/inference mapping | yes | Review must keep source evidence, claims, and derivations separate. | Review guidance only; no automatic promotion. |
| temporal mapping | yes | Time scope prevents stale or historical material from appearing current. | Review vocabulary only; no temporal query logic. |
| lifecycle mapping | yes | Candidate, approved, stale, blocked, rejected, and historical states differ. | Labels only; no state machine or transition behavior. |
| failed-attempt mapping | yes | Failed paths need scoped review vocabulary. | Candidate warning only; no failure store. |
| do-not-retry mapping | yes | Retry-risk guidance needs precise scope. | Candidate guidance only; no enforcement. |
| recall trace mapping | yes | Recall explanation should expose reason, source path, and uncertainty. | Explanation packet only; no recall engine or trace persistence. |
| connector/source mapping | yes | Connector and source snapshots need risk and provenance labels. | Source evidence only; no connector logic, sync, or API surface. |
| evaluation mapping | yes | Evaluation questions need review vocabulary. | Question vocabulary only; no tests, runner, or benchmark. |
| conflict/uncertainty mapping | yes | Conflicts and unknowns must stay visible. | Does not resolve or block automatically. |
| human review readiness | yes | Reviewers need enough context to accept, reject, block, or defer. | Readiness is candidate status only. |
| ontology schema | no | A schema would define implemented structure. | Excluded. |
| graph database | no | Graph database behavior would be implementation. | Excluded. |
| Memory Graph behavior | no | Memory Graph behavior would change runtime or durable semantics. | Excluded. |
| Memory Graph mutation | no | Mutation would write or alter graph state. | Excluded. |
| graph traversal | no | Traversal would be implemented behavior. | Excluded. |
| relationship inference | no | Inferring relationships would automate review. | Excluded. |
| automatic classification | no | Classification must remain human-reviewed. | Excluded. |
| automatic promotion | no | Promotion requires explicit governance. | Excluded. |
| durable memory writing | no | Writing memory requires separate governed approval. | Excluded. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Memory Object Families

| Object family | Meaning | Source document family | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| source object | A local, user, connector-like, external, or tool-observed source reference. | Connector Governance Taxonomy, Document Index, local repo docs. | Inspectable source reference, source type, source path or location, observation context. | Do not infer truth, approval, source ingestion, connector adoption, or durable access. |
| evidence object | A bounded observation extracted or summarized from a source object. | Memory Evaluation Candidates, Explainable Recall Trace Template, Connector Governance Taxonomy. | Source reference, evidence summary, extraction or transformation note when relevant. | Do not infer the evidence is a claim, approved memory, authorization, or current truth. |
| claim object | A statement proposed from evidence or operator context. | Memory Evaluation Candidates, Temporal Validity Model, Lifecycle Taxonomy. | Claim summary, source reference, evidence basis, temporal and lifecycle notes. | Do not infer the claim is fact, approved memory, or active guidance. |
| inference object | An explicit reasoning step derived from evidence and claim. | Explainable Recall Trace Template, Memory Evaluation Candidates. | Inference note, evidence basis, uncertainty note. | Do not infer source fact, approval, automatic relationship, or hidden authority. |
| memory candidate object | A claim or packet proposed for future memory review. | Memory Evaluation Candidates, Lifecycle Taxonomy. | Claim, evidence summary, source reference, temporal status, lifecycle state. | Do not infer durable memory write, active memory, or automatic promotion. |
| lifecycle object | A label describing proposed, reviewed, stale, rejected, blocked, archived, or historical state. | Memory Lifecycle Taxonomy. | Lifecycle label, state reason, reviewer note if reviewed. | Do not infer automatic transition, storage, deletion, or approval. |
| temporal object | A label or field group describing observation time, source time, validity, staleness, conflict, or historical scope. | Temporal Validity Model. | `observed_at`, `source_timestamp`, temporal note, unknown marker when missing. | Do not infer current truth, temporal query behavior, stale detection, expiration, or supersession behavior. |
| failed-attempt object | A bounded description of an attempted action, failed assumption, failed command, or failed workflow. | Failed Attempt Memory / Do-Not-Retry Rules. | Attempted action, actual result, failure signal, scope, observed time when known. | Do not infer permanent impossibility, enforcement, or failure storage. |
| do-not-retry object | A scoped candidate rule warning against retrying a specific failed path under stated conditions. | Failed Attempt Memory / Do-Not-Retry Rules. | Failed attempt reference, retry risk, blocked reason, exception condition. | Do not infer automatic law, indefinite ban, retry blocker, or enforcement. |
| recall trace object | A packet explaining why an item surfaced and how to review it. | Explainable Recall Trace Template. | Recall reason, source path, evidence summary, claim summary, inference note, status notes. | Do not infer recall storage, retrieval behavior, approval, authorization, or execution permission. |
| connector/source object | A source or result candidate from connector-like, API-like, sync-like, external, repo, file, or tool surface. | Connector Governance Taxonomy. | Source type, source location, observed_at, source or sync timestamp when known, risk notes. | Do not infer connector logic, connector storage, connector sync, API calls, MCP tools, adapter behavior, or source ingestion. |
| evaluation object | A question, dimension, evidence packet, or result candidate for human evaluation. | Memory Evaluation Candidates. | Evaluation question, dimension, evidence basis, confidence note, boundary note. | Do not infer tests, benchmark runner, score automation, approval, or implementation. |
| conflict object | A visible disagreement between sources, claims, times, lifecycle states, permissions, or interpretations. | Temporal Validity Model, Lifecycle Taxonomy, Connector Governance Taxonomy. | Conflict note, source references when available, unknown marker when missing. | Do not infer automatic resolution or winner. |
| uncertainty object | A visible unknown, missing source, missing time, missing state, missing relation, or confidence gap. | Memory Evaluation Candidates, Explainable Recall Trace Template. | Uncertainty note and known evidence gaps. | Do not infer safe use, rejection, approval, or automatic block. |
| human review object | A future human-scoped decision or review note about a candidate mapping. | All governance docs. | Evidence packet, reviewer note, decision scope, recommended next state. | Do not infer side effects, durable writes, P4 activation, execution, or authorization. |
| boundary rule object | A rule stating what must not be inferred or implemented. | Boundary Constitution, Release Book, FAQ, all post-terminal docs. | Boundary statement, source document, prohibited inference. | Do not treat boundary prose as executable enforcement logic. |

## 6. Memory Object Type Mapping

| Object type | Object family | Source doc | Required fields | Safe use | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| `memory_candidate` | memory candidate object | Memory Evaluation Candidates; Lifecycle Taxonomy | `object_id`, `claim_summary`, `source_reference`, `temporal_status`, `lifecycle_state`, `prohibited_inference` | Review a proposed memory item. | Do not infer approved memory, durable write, truth, or active guidance. |
| `approved_candidate` | lifecycle object | Memory Lifecycle Taxonomy | `object_id`, `reviewer_note`, `source_reference`, `lifecycle_state`, `boundary_note` | Mark human-scoped approval as candidate vocabulary. | Do not infer active memory, timeless validity, or automatic promotion. |
| `active_reviewed_memory` | lifecycle object | Memory Lifecycle Taxonomy | `object_id`, `reviewer_note`, `source_reference`, `temporal_status`, `boundary_note` | Describe reviewed use within scope. | Do not infer execution permission or indefinite validity. |
| `active_time_bound_memory` | temporal object | Temporal Validity Model; Lifecycle Taxonomy | `object_id`, `observed_at`, `source_timestamp`, `temporal_status`, `lifecycle_state` | Describe reviewed use bounded by time, version, branch, source, or event. | Do not infer use outside the boundary. |
| `stale_candidate` | temporal object | Temporal Validity Model; Lifecycle Taxonomy | `object_id`, `stale_reason` or `uncertainty_note`, `source_reference`, `observed_at` when known | Flag possible staleness before review. | Do not infer deletion, rejection, or automatic expiration. |
| `stale_reviewed_memory` | lifecycle object | Memory Lifecycle Taxonomy; Temporal Validity Model | `object_id`, `reviewer_note`, `stale_reason`, `source_reference`, `temporal_status` | Mark reviewed staleness within scope. | Do not infer audit removal or replacement. |
| `superseded_memory` | lifecycle object | Temporal Validity Model; Lifecycle Taxonomy | `object_id`, `superseded_by`, `source_reference`, `conflict_note`, `reviewer_note` when available | Preserve old evidence with a successor reference. | Do not infer erasure, overwrite, or automatic supersession. |
| `conflicted_memory` | conflict object | Memory Lifecycle Taxonomy; Temporal Validity Model | `object_id`, `conflict_note`, `source_reference`, `uncertainty_note` | Surface unresolved disagreement. | Do not infer which side wins or that conflict is resolved. |
| `rejected_memory` | lifecycle object | Memory Lifecycle Taxonomy | `object_id`, `reviewer_note`, `source_reference`, `boundary_note` | Preserve rejected candidate reasoning. | Do not infer deletion, permanent impossibility, or hidden approval of the opposite claim. |
| `blocked_memory` | lifecycle object | Memory Lifecycle Taxonomy; Failed Attempt Rules | `object_id`, `blocked_reason`, `source_reference`, `boundary_note`, `recommended_next_state` | Pause use pending review or separate decision. | Do not infer permanent law or enforcement. |
| `historical_only_memory` | temporal object | Temporal Validity Model; Lifecycle Taxonomy | `object_id`, `temporal_status`, `evidence_summary`, `source_reference`, `boundary_note` | Retain past context without current guidance. | Do not infer uselessness, deletion, or current authority. |
| `archived_candidate` | lifecycle object | Memory Lifecycle Taxonomy | `object_id`, `source_reference`, `lifecycle_state`, `reviewer_note` when available | Retain inactive candidate material. | Do not infer storage movement, deletion, or reviewed use. |
| `deletion_proposed` | lifecycle object | Memory Lifecycle Taxonomy | `object_id`, `source_reference`, `reviewer_note` if any, `boundary_note` | Name a future deletion proposal. | Do not infer deletion, erasure, or audit removal. |
| `failed_attempt_record` | failed-attempt object | Failed Attempt Memory / Do-Not-Retry Rules | `object_id`, `attempted_action`, `actual_result`, `failure_signal`, `source_reference`, `observed_at` when known | Preserve scoped failure context. | Do not infer permanent impossibility, storage, or retry enforcement. |
| `do_not_retry_candidate` | do-not-retry object | Failed Attempt Memory / Do-Not-Retry Rules | `object_id`, `failed_attempt_status`, `retry_risk`, `blocked_reason`, `exception_condition`, `scope_boundary` | Warn that a specific retry needs review. | Do not infer automatic law, indefinite ban, or blocker logic. |
| `recall_trace_packet` | recall trace object | Explainable Recall Trace Template | `object_id`, `recall_reason`, `source_path`, `evidence_summary`, `claim_summary`, `inference_note`, status notes | Explain why an item surfaced. | Do not infer storage, approval, authorization, execution, or retrieval logic. |
| `connector_result_candidate` | connector/source object | Connector Governance Taxonomy | `object_id`, `source_type`, `source_location`, `observed_at`, `connector_source_risk`, `prohibited_inference` | Review connector-like source evidence. | Do not infer connector implementation, sync, API calls, or adoption. |
| `external_source_candidate` | source object | Landscape Report; Connector Governance Taxonomy | `object_id`, `source_reference`, `source_type`, `observed_at` if known, `uncertainty_note` | Treat external material as snapshot or methodology reference. | Do not infer live facts, dependency, adapter, or implementation approval. |
| `tool_observation_candidate` | evidence object | Connector Governance Taxonomy; Comprehensive Audit Report | `object_id`, `source_type`, `source_location`, `observed_at`, `evidence_summary` | Use bounded tool output as local evidence. | Do not infer broad tool capability or permission to act. |
| `evaluation_candidate` | evaluation object | Memory Evaluation Candidates | `object_id`, `evaluation_question`, `evidence_summary`, `confidence_note`, `boundary_note` | Frame a reviewable evaluation topic. | Do not infer benchmark runner, tests, or approval. |
| `evaluation_question` | evaluation object | Memory Evaluation Candidates | `object_id`, `evaluation_question`, `source_reference`, `boundary_note` | Ask what reviewers should inspect. | Do not infer it is a test, check, or benchmark. |
| `human_review_decision` | human review object | All governance docs | `object_id`, `reviewer_note`, `source_reference`, `recommended_next_state`, `boundary_note` | Record a scoped candidate decision for future docs. | Do not infer side effects, durable write, P4 activation, authorization, or execution. |
| `unknown_memory_object` | uncertainty object | All governance docs | `object_id`, `uncertainty_note`, `source_reference` if available, `prohibited_inference` | Mark unknown type and require review. | Do not infer safety, rejection, approval, classification, or current use. |

## 7. Relationship Vocabulary

These are relationship words only. They are not graph edges, not graph traversal, not automatic inference, not ontology query logic, and not Memory Graph mutation.

| Relationship label | Meaning | Allowed use | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| `sourced_from` | Object cites a source reference. | Link source object to evidence, claim, trace, or review packet in prose. | Inspectable source reference or explicit unknown marker. | Do not infer approval, truth, graph edge, or source ingestion. |
| `extracted_from` | Evidence was taken from a source. | Mark extraction or excerpt summary. | Source path and extraction note. | Do not infer complete or lossless transfer. |
| `transformed_from` | Evidence changed through summary, conversion, filtering, or normalization. | Mark transformation risk. | Transformation note and source reference. | Do not infer unchanged meaning. |
| `claims` | A claim object states something proposed for review. | Separate claim from evidence. | Claim summary and source reference. | Do not infer fact or approved memory. |
| `supports` | Evidence may support a claim. | Name a support relation for reviewer inspection. | Evidence summary and claim summary. | Do not infer proof, approval, or automatic confidence. |
| `contradicts` | Evidence or claim conflicts with another claim. | Mark direct disagreement. | Conflict note and source references when available. | Do not infer winner or automatic resolution. |
| `narrows` | Later evidence may reduce the scope of an older claim. | Describe scoped correction. | Old claim, newer/narrower evidence, boundary note. | Do not infer silent overwrite. |
| `supersedes` | A candidate may replace or limit prior material. | Label successor relation for review. | Successor evidence and old claim reference. | Do not infer erasure, deletion, or automatic promotion. |
| `superseded_by` | Prior material points to possible successor evidence. | Preserve old record with successor reference. | Prior object, successor reference, rationale. | Do not infer old evidence is removed. |
| `conflicts_with` | Objects disagree by source, time, lifecycle, permission, or interpretation. | Make unresolved conflict visible. | Conflict note and available sources. | Do not infer resolution. |
| `derived_inference_from` | Inference was derived from stated evidence or claim. | Mark reasoning step. | Inference note and evidence basis. | Do not infer source fact, claim approval, or relationship inference. |
| `has_temporal_scope` | Object has a time, version, branch, source, or event boundary. | Attach temporal review vocabulary. | `observed_at`, `source_timestamp`, or temporal note. | Do not infer temporal query behavior or current truth. |
| `has_lifecycle_state` | Object carries a lifecycle label. | Attach lifecycle review vocabulary. | Lifecycle state and state reason. | Do not infer state transition or storage. |
| `has_confidence_note` | Object has qualitative evidence-strength context. | Surface confidence for human review. | Confidence note tied to evidence. | Do not infer score automation or approval. |
| `has_uncertainty_note` | Object has explicit unknowns or gaps. | Preserve missing or weak evidence. | Uncertainty note. | Do not infer safe use or automatic block. |
| `has_failed_attempt` | Object relates to a scoped failure record. | Connect claim, warning, or trace to failed-attempt context. | Failed attempt reference and failure signal. | Do not infer permanent impossibility or failure storage. |
| `has_do_not_retry_candidate` | Object relates to a candidate do-not-retry rule. | Mark retry risk. | Failed attempt, blocked reason, exception condition. | Do not infer enforcement or automatic law. |
| `has_recall_trace` | Object has an explanation packet. | Link review object to trace packet in prose. | Trace packet reference and recall reason. | Do not infer trace persistence, approval, or retrieval logic. |
| `has_connector_source` | Object includes connector-like or source-risk context. | Surface connector/source risk. | Source type, source location, observed_at, risk note. | Do not infer connector adoption, API/MCP surface, or sync. |
| `has_evaluation_question` | Object is tied to a review question. | Attach evaluation vocabulary. | Evaluation question and evidence basis. | Do not infer test or benchmark. |
| `requires_human_review` | Object cannot be safely used without human review. | Mark review requirement. | Reason for review, evidence gaps, conflict, stale risk, or boundary note. | Do not infer rejection, approval, or automatic block. |
| `blocked_by_boundary` | A boundary rule prevents interpretation or action. | Explain why use must stop or remain candidate-only. | Boundary rule object or source doc. | Do not infer executable enforcement. |
| `historical_context_for` | Old object provides context for a current review. | Preserve history without current authority. | Temporal status and source reference. | Do not infer current guidance. |
| `unknown_relationship` | Relationship cannot be classified from available evidence. | Mark mapping gap. | Unknown reason and available evidence. | Do not infer any relationship, edge, or inference. |

## 8. Attribute Vocabulary

This is not a schema implementation. These are common review attributes only.

| Attribute | Meaning | When required | Evidence requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `object_id` | Document-local identifier for discussion. | Required when multiple objects are compared. | Human-assigned or explicit unknown marker. | Do not infer durable storage or global identity. |
| `object_type` | Candidate object type label. | Required for reviewable mapping. | One type from this document or documented unknown. | Do not infer approval or automatic classification. |
| `object_family` | High-level family label. | Required for reviewable mapping. | One family from this document or documented unknown. | Do not infer implementation hierarchy. |
| `source_reference` | Inspectable source reference supporting the object. | Required for claim-bearing objects. | Local doc path, git evidence, user instruction, tool observation, or unknown marker. | Do not infer governance approval. |
| `source_path` | Human-readable path from source to evidence, claim, or trace. | Required when provenance matters. | Source, extraction, transformation, claim, and inference notes. | Do not infer source graph traversal. |
| `source_type` | Class of source. | Required for connector/source, external, tool, and local evidence. | Source type label or unknown marker. | Do not infer trust from type alone. |
| `source_location` | Human-readable source location or descriptor. | Required when safely describable. | Path, doc, repo ref, URL descriptor, account-scoped descriptor, or unknown marker. | Do not infer approval or durable access. |
| `observed_at` | When the source, claim, or object was observed. | Required when time may affect validity and when known. | Local observation, git evidence, source packet note, or unknown marker. | Do not infer current truth. |
| `source_timestamp` | Timestamp attached to the source itself. | Required when source provides it or freshness matters. | Source-visible timestamp, local file/git evidence, or unknown marker. | Do not infer source is current. |
| `sync_timestamp` | Time associated with a sync-like result. | Required for sync result candidates when known. | Sync metadata, result packet note, or unknown marker. | Do not infer live sync or live truth. |
| `evidence_summary` | Summary of what evidence shows. | Required for claim-bearing objects. | Source-backed bounded summary. | Do not infer truth, approval, or authorization. |
| `claim_summary` | Summary of the proposed claim. | Required when object asserts a claim. | Claim text or faithful summary with source reference. | Do not infer fact or approved memory. |
| `inference_note` | Explicit reasoning derived from evidence and claim. | Required when reasoning is added. | Derivation and uncertainty note. | Do not present inference as source fact. |
| `temporal_status` | Candidate time-scope label. | Required when time, staleness, or historical status matters. | Temporal evidence or unknown marker. | Do not infer current truth or temporal query behavior. |
| `lifecycle_state` | Candidate lifecycle label. | Required when trust state matters. | Lifecycle reason and reviewer note if reviewed. | Do not infer automatic transition or storage. |
| `confidence_note` | Qualitative evidence-strength note. | Required for high-risk or uncertain use. | Evidence quality explanation. | Do not infer score automation or approval. |
| `conflict_note` | Description of known or possible disagreement. | Required when conflict exists or comparison is missing. | Conflict source, conflict summary, or unknown conflict marker. | Do not infer resolution. |
| `uncertainty_note` | What remains unknown or weak. | Required when evidence is incomplete. | Missing source, missing time, missing state, or confidence gap. | Do not hide uncertainty or infer safety. |
| `failed_attempt_status` | Whether object relates to a failed attempt. | Required when failure evidence appears. | Attempt summary, failure signal, actual result, or not-applicable marker. | Do not infer permanent impossibility. |
| `do_not_retry_status` | Whether object relates to do-not-retry candidate guidance. | Required when retry risk appears. | Blocked path, blocked reason, exception condition, review requirement. | Do not infer enforcement. |
| `connector_source_risk` | Risk from connector-like, API-like, sync-like, external, or source-class evidence. | Required for connector/source and external snapshots. | Risk type and source basis. | Do not infer connector adoption or trust scoring. |
| `evaluation_question` | Human review question. | Required for evaluation objects. | Question tied to evidence and boundary. | Do not infer test or benchmark. |
| `reviewer_note` | Human review comment or decision note. | Required only when review occurred. | Explicit reviewer note and scope. | Do not infer execution, write, or authorization permission. |
| `recommended_next_state` | Candidate next review or lifecycle state. | Recommended for review packets. | Rationale tied to evidence, risk, and uncertainty. | Do not infer automatic transition. |
| `prohibited_inference` | What must not be concluded from the object. | Required for high-risk objects and boundary rules. | Explicit boundary statement. | Do not treat the prohibition as executable logic. |
| `boundary_note` | Boundary source or scope note. | Required when object could be overread. | Local governance source or task constraint. | Do not infer implementation authorization. |

## 9. Evidence / Claim / Inference Mapping

A source object produces an evidence object when a reviewer can inspect where the evidence came from.

An evidence object may support a claim object when the claim summary remains separate from the evidence summary.

A claim object may be reviewed as a memory candidate when source, evidence, time scope, lifecycle state, conflict, uncertainty, and prohibited inference are visible.

An inference object must be explicitly derived and labeled. The inference note must say what evidence it uses and what remains uncertain.

Inference does not become claim unless reviewed.

Claim does not become approved memory unless reviewed.

Evidence does not become authorization.

Absence of evidence must be represented as uncertainty, not filled with invented fact.

Conflicting evidence must create a conflict object or conflict note.

There is no automatic promotion from source to evidence, evidence to claim, claim to memory candidate, memory candidate to approved candidate, approved candidate to active reviewed memory, or review packet to durable memory write.

## 10. Temporal Validity Mapping

A temporal object stores review vocabulary only.

`observed_at` and `source_timestamp` must remain separate. `observed_at` records when the source or claim was observed. `source_timestamp` records time attached to the source itself.

`sync_timestamp` must remain separate when connector/sync source evidence exists.

`valid_from` and `valid_until` may be unknown. Unknown validity must be visible rather than silently treated as evergreen.

`unknown_time_scope` requires review.

`stale_candidate` is not deletion.

`historical_only` is not useless.

`superseded_by` is not erasure.

Current use requires current evidence or review.

This mapping creates no temporal query logic, no stale-memory detector, and no automatic expiration.

It creates no supersession engine. Supersession vocabulary preserves old evidence and candidate successor references for human review.

## 11. Lifecycle Mapping

Lifecycle labels do not trigger transitions. They are ontology mapping words only.

| Lifecycle state | Ontology meaning | Safe use | Prohibited inference |
| --- | --- | --- | --- |
| `proposed` | Suggested but not shaped enough for candidate review. | Early classification or memory proposal discussion. | Do not infer candidate completeness or truth. |
| `candidate` | Reviewable candidate evidence. | Use when source, claim, and scope are visible enough for review. | Do not infer approved memory or durable write. |
| `under_review` | A reviewer is considering the object. | Show ongoing human review context. | Do not infer approval, rejection, or mutation. |
| `review_required` | Use is unsafe without human review. | Mark stale, conflict, authority, uncertainty, source, or boundary risk. | Do not infer approval or block removal. |
| `approved_candidate` | Human approval within stated scope, not automatically active memory. | Record scoped review vocabulary. | Do not infer active use, timeless truth, or promotion. |
| `active_reviewed` | Reviewed item may be used within stated scope. | Describe scope-bound reviewed use. | Do not infer execution permission or indefinite validity. |
| `active_time_bound` | Reviewed item may be used only within known time, version, branch, tool, source, or event scope. | Preserve a bounded current-use label. | Do not infer use outside the boundary. |
| `stale_candidate` | Item may be stale but has not been reviewed as stale. | Flag possible staleness. | Do not infer deletion, rejection, or expiration. |
| `stale_reviewed` | Reviewer marked the item stale within scope. | Preserve reviewed stale status. | Do not infer audit removal or replacement. |
| `superseded` | Later or narrower evidence may replace or limit the item. | Link old evidence to successor reference. | Do not infer erasure, overwrite, or automatic successor approval. |
| `conflicted` | Evidence, time, scope, source, or interpretation disagrees. | Mark unresolved conflict. | Do not infer automatic resolution or winner. |
| `rejected` | Reviewer rejected candidate within stated scope. | Preserve rejection reason. | Do not infer deletion or permanent impossibility outside scope. |
| `blocked` | Lifecycle risk prevents use until review or separate decision. | Pause unsafe use. | Do not infer permanent law or enforcement. |
| `historical_only` | Retained as past context, not current guidance. | Keep old project state, source snapshot, or failure context visible. | Do not infer current authority or uselessness. |
| `archived_candidate` | Candidate retained for reference but not active. | Mark inactive candidate material. | Do not infer deletion or reviewed archival. |
| `archived_reviewed` | Reviewer marked a record as retained but inactive. | Preserve reviewed inactive status. | Do not infer storage movement or active use. |
| `deletion_proposed` | Deletion, hiding, or removal has been proposed. | Name deletion request for review. | Do not infer deletion or erasure. |
| `deletion_rejected` | Deletion proposal was rejected. | Preserve rejection of deletion. | Do not infer active approval of the target record. |
| `unknown_lifecycle` | Lifecycle state cannot be judged from available evidence. | Mark missing review state. | Do not infer safe current use. |

## 12. Failed Attempt and Do-Not-Retry Mapping

Failed-attempt and do-not-retry vocabulary maps failed paths into scoped review objects only.

| Object type | Ontology meaning | Required evidence | Safe use | Prohibited inference |
| --- | --- | --- | --- | --- |
| `failed_attempt_record` | A bounded record of a failed path. | Attempted action, actual result, failure signal, source reference, scope. | Preserve warning context. | Do not infer permanent impossibility or storage. |
| `failure_signal` | Visible sign that the attempt failed. | Error, mismatch, rejection, blocked state, or boundary violation. | Explain why the attempt is considered failed. | Do not infer root cause automatically. |
| `attempted_action` | Concrete action, command, workflow, prompt, assumption, or design path. | Precise command/workflow text when safe, or precise prose. | Scope a failure narrowly. | Do not generalize beyond the described action. |
| `actual_result` | What happened instead of the expected result. | Observed output, state, error, user correction, or source evidence. | Ground the failure record. | Do not infer broad failure outside evidence. |
| `retry_risk` | Qualitative risk of repeating the path. | Failure evidence, scope, exception condition, uncertainty note. | Guide human review. | Do not infer approval or enforcement. |
| `blocked_reason` | Why retry should pause or be avoided under stated conditions. | Evidence-backed reason and scope. | Explain a candidate block. | Do not infer permanent prohibition outside scope. |
| `exception_condition` | What change or review could permit reconsideration. | Tool/version/environment/user/evidence change or unknown marker. | Prevent overblocking. | Do not infer automatic unblocking. |
| `do_not_retry_candidate` | Candidate rule against repeating a specific failed path under stated conditions. | Failed attempt reference, blocked retry, scope, exception condition. | Require review before retry. | Do not infer automatic law or indefinite ban. |
| `scope_boundary` | Exact scope controlling the failure or retry risk. | Branch, version, command, environment, permission, network, or user-scope note. | Prevent overbroad memory. | Do not infer adjacent scopes are blocked. |
| `historical_failure_context` | Old or superseded failure retained as past context. | Observed time, historical reason, source reference. | Retain learning without current authority. | Do not infer uselessness or current block. |

A failed attempt is not proof of impossibility.

A do-not-retry candidate is not automatic law.

A retry blocker is not implemented.

An old failure may be `historical_only`.

An improved future path requires review, not automatic block.

## 13. Explainable Recall Trace Mapping

`recall_trace_packet` is an explanation object, not a memory object by itself.

`recall_reason` is relationship/context vocabulary. It names why an item may have surfaced, but it does not implement retrieval, ranking, or explanation generation.

`source_path` must stay visible so reviewers can inspect source, extraction, transformation, claim, and inference path.

Evidence, claim, and inference must stay separated.

`temporal_status` must stay visible.

`lifecycle_state` must stay visible.

`connector_source_risk` must stay visible if relevant.

`safe_use` and `unsafe_use` must remain review guidance only.

A recall trace is not approval.

A recall trace is not authorization.

A recall trace is not execution permission.

This mapping creates no trace persistence.

## 14. Connector Governance Mapping

A connector result starts as a candidate source/evidence object.

An API result snapshot is observation, not authorization.

A sync result snapshot is not live truth.

Permission to read is not permission to act.

Credential scope must stay visible.

Permission scope must stay visible.

`connector_source_risk` maps into uncertainty, conflict, and freshness review. It can mark stale source risk, missing timestamp risk, sync lag risk, partial extraction risk, transformation loss risk, permission scope risk, credential expiry risk, source rewrite risk, source disappearance risk, conflicting source risk, trust overread risk, benchmark overread risk, live fact overread risk, connector action overread risk, or unknown connector risk.

Connector evidence is not Memory Graph mutation.

Connector trace is not connector adoption.

This mapping creates no connector logic, no API/MCP/adapter implementation, and no source ingestion.

It also creates no connector storage, connector sync, credential handling, permission handling, source polling, source freshness checks, automatic trust scoring, or source promotion.

## 15. Evaluation Mapping

Evaluation vocabulary maps future review questions into candidate ontology terms only.

| Evaluation object | Meaning | Required evidence | Safe use | Prohibited inference |
| --- | --- | --- | --- | --- |
| `evaluation_candidate` | A proposed topic for memory quality review. | Candidate scope, evidence basis, boundary note. | Frame what should be reviewed. | Do not infer evaluation runner or approval. |
| `evaluation_question` | A human-readable review question. | Question text and source context. | Ask what evidence should be inspected. | Do not infer a test. |
| `evaluation_dimension` | A quality dimension such as relevance, correctness, provenance, temporal validity, conflict awareness, confidence, lifecycle clarity, recall explainability, write safety, update safety, deletion safety, failed-attempt usefulness, do-not-retry precision, connector risk clarity, privacy/locality clarity, human review readiness, regression/replay usefulness, or operator usability. | Dimension and review purpose. | Organize human evaluation. | Do not infer automated scoring. |
| `evaluation_evidence` | Source-backed evidence used to answer an evaluation question. | Source reference, evidence summary, uncertainty note. | Support review. | Do not infer approval. |
| `evaluation_result_candidate` | Candidate conclusion from a human or future review packet. | Evaluation question, evidence, confidence note, reviewer note if reviewed. | Preserve review result as candidate. | Do not infer promotion, benchmark pass, or implementation. |
| `human_review_required` | Marker that evaluation cannot conclude safely without review. | Missing evidence, conflict, stale risk, authority risk, or boundary note. | Stop overreading. | Do not infer rejection or approval. |
| `benchmark_reference_snapshot` | Benchmark-related source reference for question design. | Source reference, observed_at if known, scope, uncertainty. | Inform evaluation questions. | Do not infer local benchmark approval or pass rate. |
| `confidence_note` | Qualitative evidence-strength explanation. | Evidence quality and uncertainty. | Help a reviewer calibrate trust. | Do not infer score automation or approval. |
| `boundary_note` | Boundary that limits use of the evaluation object. | Local governance source or task constraint. | Prevent implementation drift. | Do not infer executable enforcement. |

An evaluation candidate is not benchmark runner.

An evaluation question is not test.

Evaluation evidence is not approval.

A benchmark reference is not local benchmark approval.

This mapping adds no tests, no evaluation runner, and no benchmark implementation.

## 16. Conflict and Uncertainty Mapping

Conflict and uncertainty objects preserve unresolved review gaps.

| Label | Meaning | Required evidence | Safe use | Prohibited inference |
| --- | --- | --- | --- | --- |
| direct conflict | Two claims directly disagree. | Both claim summaries and source references when available. | Mark unresolved disagreement. | Do not choose a winner. |
| partial conflict | Claims overlap but disagree only in scope, time, source, or interpretation. | Conflict note and scope note. | Narrow review question. | Do not flatten to direct contradiction. |
| time conflict | Sources or claims disagree by observation time, source time, validity window, or currentness. | Temporal notes and source references when available. | Require temporal review. | Do not infer current truth. |
| lifecycle conflict | Lifecycle labels disagree or are unsupported. | Lifecycle notes and reviewer evidence when available. | Require lifecycle review. | Do not infer active state. |
| source conflict | Source references disagree, are missing, or have different trust/freshness risks. | Source notes and conflict note. | Require source review. | Do not infer source authority. |
| interpretation conflict | Evidence can support multiple readings. | Evidence summary, competing interpretation notes. | Preserve ambiguity. | Do not infer the assistant's reading is fact. |
| permission conflict | Read/view/action/credential scope is unclear or inconsistent. | Permission scope, credential scope, uncertainty note. | Stop permission overread. | Do not infer permission to act. |
| unknown conflict | A conflict is suspected but not classifiable. | Unknown conflict note and known evidence gaps. | Require review. | Do not infer safety or resolution. |
| unknown source | Source is missing or cannot be inspected. | Missing source note. | Block factual presentation. | Do not present as sourced fact. |
| unknown time scope | Observation time, source time, or validity boundary is missing. | Missing time note. | Require review before current use. | Do not infer evergreen truth. |
| unknown lifecycle | Lifecycle state cannot be judged. | Missing review/lifecycle note. | Require review before use. | Do not infer active or approved state. |
| unknown relationship | Relationship cannot be classified. | Unknown relationship note. | Avoid invented relation. | Do not infer edge, traversal, or relationship inference. |

A conflict object does not choose a winner.

An uncertainty object does not block automatically.

An unresolved conflict cannot be presented as fact.

A missing source must be visible.

There is no automatic resolution.

## 17. Human Review Readiness for Ontology Mapping

Before any later P4 consideration, a reviewer must be able to:

- identify object family;
- identify object type;
- inspect source reference;
- inspect evidence summary;
- separate claim and inference;
- see temporal status;
- see lifecycle state;
- see failed-attempt / do-not-retry status when relevant;
- see recall trace when relevant;
- see connector/source risk when relevant;
- see conflict and uncertainty;
- see prohibited inference;
- reject mapping without side effect;
- block use without side effect.

A reviewer decision is recorded as candidate only.

P4 remains paused.

P4 requires explicit human confirmation later.

## 18. Non-Authorization Rules

Ontology mapping is not truth.

Object type is not approval.

Relationship label is not graph edge.

Relationship label is not graph traversal.

Source path is not governance approval.

Evidence is not authorization.

Claim is not approved memory.

Inference is not fact.

Lifecycle label is not automatic transition.

Temporal label is not current truth.

Connector source is not connector adoption.

Recall trace is not approval.

Evaluation question is not test.

Benchmark reference is not local benchmark approval.

Mapping is not Memory Graph mutation.

Mapping is not durable memory write.

## 19. Candidate Examples

These examples are illustrative only, not live facts.

| Example | Object family | Object type | Relationship labels | Required attributes | Safe reviewer action | Prohibited inference |
| --- | --- | --- | --- | --- | --- | --- |
| user preference memory candidate with temporal uncertainty | memory candidate object | `memory_candidate` | `sourced_from`, `claims`, `has_temporal_scope`, `has_uncertainty_note`, `requires_human_review` | `object_id`, `claim_summary`, `source_reference`, `observed_at` or unknown marker, `temporal_status`, `uncertainty_note` | Ask whether the preference is current and scoped. | Do not infer durable preference or current truth. |
| failed command remembered as historical failure context | failed-attempt object | `failed_attempt_record` | `sourced_from`, `has_failed_attempt`, `historical_context_for` | `attempted_action`, `actual_result`, `failure_signal`, `source_reference`, `temporal_status` | Retain as warning context. | Do not infer permanent command ban. |
| connector API response treated as source snapshot | connector/source object | `connector_result_candidate` | `sourced_from`, `has_connector_source`, `has_temporal_scope`, `requires_human_review` | `source_type`, `source_location`, `observed_at`, `source_timestamp` or unknown marker, `connector_source_risk` | Review snapshot risk and permission scope. | Do not infer API adoption, live truth, or authorization. |
| stale product/market claim treated as time-bound evidence | temporal object | `stale_candidate` | `sourced_from`, `has_temporal_scope`, `has_uncertainty_note` | `claim_summary`, `source_reference`, `observed_at`, `temporal_status`, `confidence_note` | Mark current use as review required. | Do not infer current live fact. |
| rejected assistant assumption mapped as historical-only correction | lifecycle object | `rejected_memory` | `sourced_from`, `contradicts`, `historical_context_for`, `has_lifecycle_state` | `claim_summary`, `source_reference`, `reviewer_note`, `lifecycle_state`, `boundary_note` | Preserve correction and prevent repeated assumption. | Do not infer deletion or broad prohibition. |
| benchmark reference mapped as evaluation question | evaluation object | `evaluation_question` | `sourced_from`, `has_evaluation_question`, `requires_human_review` | `evaluation_question`, `source_reference`, `confidence_note`, `boundary_note` | Use as review prompt. | Do not infer benchmark runner, score, or local approval. |
| merged repo doc mapped as local governance evidence | evidence object | `tool_observation_candidate` or `external_source_candidate` if outside repo | `sourced_from`, `supports`, `has_lifecycle_state` | `source_path`, `evidence_summary`, `observed_at` if relevant, `boundary_note` | Cite as local governance evidence. | Do not infer implementation authorization. |
| recall trace mapped as explanation packet | recall trace object | `recall_trace_packet` | `has_recall_trace`, `sourced_from`, `derived_inference_from`, `requires_human_review` | `recall_reason`, `source_path`, `evidence_summary`, `claim_summary`, `inference_note`, status notes | Inspect why the item surfaced. | Do not infer approval, storage, or execution permission. |
| conflicted source mapped as unresolved conflict object | conflict object | `conflicted_memory` | `conflicts_with`, `has_uncertainty_note`, `requires_human_review` | `conflict_note`, `source_reference`, `uncertainty_note`, `prohibited_inference` | Keep both sides visible and require review. | Do not choose a winner automatically. |

## 20. Candidate Future Sequence

Recommended docs-only sequence:

1. External Product Explanation Candidate
2. P4 Decision Gate Checklist

This document does not start either of them.

P4 remains paused.

P4 requires explicit human confirmation later.

## 21. Prohibited Implementation Rules

Do not implement ontology storage.

Do not implement ontology schema.

Do not implement graph database behavior.

Do not implement Memory Graph behavior.

Do not mutate Memory Graph.

Do not implement graph traversal.

Do not implement ontology query logic.

Do not implement relationship inference.

Do not implement automatic classification.

Do not implement automatic mapping.

Do not implement automatic promotion.

Do not implement automatic memory writing.

Do not implement connector logic.

Do not implement connector storage.

Do not implement connector sync.

Do not implement API calls.

Do not implement MCP tools.

Do not implement adapter behavior.

Do not implement credential handling.

Do not implement permission handling.

Do not implement source ingestion.

Do not implement source polling.

Do not implement source freshness checks.

Do not implement automatic trust scoring.

Do not implement recall storage.

Do not implement recall engine.

Do not implement retrieval logic.

Do not implement ranking logic.

Do not implement trace persistence.

Do not implement source graph traversal.

Do not implement automated explanation generation.

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

Do not treat ontology mapping as truth.

Do not treat relationship label as graph edge.

Do not treat relationship label as graph traversal.

Do not treat object type as approval.

Do not treat mapping as Memory Graph mutation.

Do not treat mapping as durable memory write.

Do not treat connector source as connector adoption.

Do not treat recall trace as approval.

Do not treat evaluation question as test.

## 22. Stop Conditions

If memory ontology mapping turns into code, stop.

If memory ontology mapping turns into tests, stop.

If memory ontology mapping turns into ontology schema, stop.

If memory ontology mapping turns into graph database behavior, stop.

If memory ontology mapping turns into Memory Graph behavior, stop.

If memory ontology mapping turns into Memory Graph mutation, stop.

If memory ontology mapping turns into graph traversal, stop.

If memory ontology mapping turns into ontology query logic, stop.

If memory ontology mapping turns into relationship inference, stop.

If memory ontology mapping turns into automatic classification, stop.

If memory ontology mapping turns into automatic mapping, stop.

If memory ontology mapping turns into automatic promotion, stop.

If memory ontology mapping turns into automatic memory writing, stop.

If memory ontology mapping turns into connector logic, stop.

If memory ontology mapping turns into connector storage or sync, stop.

If memory ontology mapping turns into API calls or MCP tools, stop.

If memory ontology mapping turns into adapter behavior, stop.

If memory ontology mapping turns into source ingestion or polling, stop.

If memory ontology mapping turns into recall engine or retrieval logic, stop.

If memory ontology mapping turns into trace persistence, stop.

If memory ontology mapping turns into failed-attempt storage or do-not-retry enforcement, stop.

If memory ontology mapping turns into lifecycle storage/state machine/transition logic, stop.

If memory ontology mapping turns into temporal query, stale detector, automatic expiration, or supersession engine, stop.

If memory ontology mapping turns into dependency adoption, stop.

If memory ontology mapping turns into MCP/API operation surface, stop.

If memory ontology mapping turns into durable writer, stop.

If memory ontology mapping turns into authorization/execution semantics, stop.

If memory ontology mapping starts P4, stop.

If memory ontology mapping starts v7 implementation, stop.

If memory ontology mapping starts MVP/product deployment, stop.

If memory ontology mapping starts changing old docs, stop.

If pyproject version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 23. Final Mapping Statement

This document defines memory ontology mapping candidates only.

It does not evaluate live memory.

It does not implement ontology behavior.

It does not implement graph behavior.

It does not implement Memory Graph behavior.

It does not mutate Memory Graph.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
