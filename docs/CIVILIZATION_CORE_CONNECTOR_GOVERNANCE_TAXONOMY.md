# Civilization Core Connector Governance Taxonomy / 文明之核连接器治理分类法

## 2. Taxonomy Status

This is a docs-only connector governance taxonomy document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates.

It is based on the merged Temporal Validity Model.

It is based on the merged Memory Lifecycle Taxonomy.

It is based on the merged Failed Attempt Memory / Do-Not-Retry Rules.

It is based on the merged Explainable Recall Trace Template.

It is connector-governance taxonomy candidate only.

It creates:

- no connector logic
- no connector storage
- no connector sync
- no API calls
- no MCP tools
- no adapter behavior
- no credential handling
- no permission handling
- no source ingestion
- no source polling
- no source freshness checks
- no automatic trust scoring
- no automatic source promotion
- no automatic memory writing
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
- no Memory Graph mutation
- no durable writer
- no authorization/execution semantics

The taxonomy below is vocabulary for future human review only. It is not connector adoption, not product implementation approval, and not a permission grant.

## 3. Why Connector Governance Matters

Connectors and external sources can look more authoritative than they are because they often arrive with tool names, source names, account context, API shapes, timestamps, or formatted result packets. Civilization Core must prevent that appearance of authority from becoming unreviewed memory.

A connector result is evidence, not approved memory.

A sync result is a snapshot, not live truth.

An API output is an observation, not authorization.

A file or document connector output may be stale, partial, permission-bound, account-scoped, transformed, or missing important context.

External source material can change after observation.

A missing timestamp must not become current truth.

Credential and permission scope must be visible when relevant because read access, view access, account identity, and source availability can shape what was observed.

Connector/source confidence is not approval.

Human review remains required before connector-derived evidence, external source material, API results, sync results, file/document connector results, tool observations, or source snapshots influence later governance decisions.

## 4. Connector Governance Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| connector result candidate | yes | A future connector result may need classification before review. | Candidate evidence only; not approved memory or behavior. |
| external source snapshot | yes | External material may inform methodology or source evidence. | Snapshot only; not live truth or dependency approval. |
| API result snapshot | yes | API output may carry useful observed evidence. | Observation only; not authorization or API adoption. |
| file/document connector result | yes | Files and documents can be source evidence with extraction limits. | Evidence label only; no connector or ingestion behavior. |
| tool observation | yes | Tool output may be local evidence under a stated scope. | Bounded observation only; not general permission. |
| sync result | yes | Sync outcome may show state at an observed time. | Snapshot only; not live truth or sync implementation. |
| source timestamp | yes | Source-provided time affects freshness and validity. | Time evidence only; not current-truth proof. |
| observed_at | yes | Observation time separates when Codex or a reviewer saw evidence from source time. | Review field only; no time query behavior. |
| source location | yes | Reviewers need to know where evidence came from. | Citation is not approval. |
| provenance path | yes | Reviewers need the path from source to evidence. | Path description only; no graph traversal. |
| credential scope | yes | Account or credential context may constrain evidence. | Scope note only; no credential handling. |
| permission scope | yes | Read/view limits may shape what was available. | Scope note only; no permission handling. |
| freshness note | yes | Freshness risk must be visible. | Qualitative note only; no automatic freshness check. |
| trust note | yes | Trust assumptions must remain inspectable. | Not automatic trust scoring. |
| transformation note | yes | Extraction, summary, format conversion, or filtering can lose meaning. | Note only; no transformation pipeline. |
| conflict note | yes | Conflicts must be visible before use. | Does not resolve conflicts automatically. |
| human review readiness | yes | A reviewer needs enough fields to accept, reject, block, or defer. | Readiness is candidate status only. |
| connector implementation | no | Implementation would be behavior, not taxonomy. | Excluded. |
| adapter implementation | no | Adapter behavior would activate a surface. | Excluded. |
| MCP/API operation surface | no | Operation surfaces can authorize or execute actions. | Excluded. |
| source ingestion | no | Ingestion would move source material into a system. | Excluded. |
| source polling | no | Polling would create recurring behavior. | Excluded. |
| automatic freshness check | no | Automated freshness would be runtime behavior. | Excluded. |
| automatic source promotion | no | Promotion would change governance state. | Excluded. |
| Memory Graph mutation | no | Graph mutation would be durable state change. | Excluded. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Connector / Source Object Types

These object types may later receive connector/source governance labeling. This section defines vocabulary only, not schema, storage, ingestion, sync, connector behavior, or API/MCP/adapter implementation.

| Object type | What it is | Governance question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| connector result candidate | A result attributed to a possible connector surface. | What source, scope, and risk should a reviewer see before use? | Source type, source location, connector name if any, observed evidence, risk notes. | Do not infer connector implementation or approved memory. |
| external source candidate | External material proposed as evidence or methodology context. | Is the source role clear and bounded? | Source location, observed_at when known, source timestamp when known, trust/freshness notes. | Do not infer live fact, dependency, or adoption. |
| API result candidate | A response or output attributed to an API-like source. | What was observed, under which context, and what is volatile? | Query/action context, observed_at, response summary, credential/permission scope if relevant. | Do not infer authorization, API calls, or current truth. |
| file connector result | A file-derived result from a future connector class. | Is the file complete, current, and permission-safe? | File/source location, observed_at, extracted evidence, transformation note. | Do not infer ingestion, storage, or file authority. |
| document connector result | A document-derived result from a future connector class. | What document portion supports the claim? | Document location, source timestamp if known, excerpt summary, transformation note. | Do not infer full-document truth or current validity. |
| email connector result | Email-derived evidence under account and permission scope. | Is the message private, partial, time-bound, or account-scoped? | Source location descriptor, sender/recipient scope if allowed, timestamp, permission note. | Do not infer permission to act or write. |
| calendar connector result | Calendar-derived evidence under time and account scope. | Is the event source current and scoped? | Calendar source descriptor, event time if known, observed_at, permission note. | Do not infer attendance, authority, or action permission. |
| repository connector result | Repository-derived evidence from files, commits, branches, or tags. | Does repo state support the claim under the inspected branch/time? | Repo path, branch, git evidence, observed_at. | Do not infer future repo state or release meaning. |
| web source snapshot | A web page or web-derived observation captured at a time. | What was observed, and how volatile is it? | Source location, observed_at, source timestamp if visible, freshness note. | Do not infer current live truth. |
| tool observation candidate | Output from a local or future tool under a bounded run context. | What command/tool context produced the observation? | Tool name, command or action context, output summary, observed_at. | Do not infer broad tool capability or permission. |
| sync result candidate | A snapshot produced by sync-like behavior in a future system. | What was synchronized, when, and what could lag? | Sync timestamp, source timestamp if known, source location, sync lag note. | Do not infer live truth or sync implementation. |
| transformed source candidate | Evidence altered by extraction, summary, conversion, filtering, or normalization. | What changed between source and evidence? | Transformation note, source reference, extracted evidence. | Do not infer lossless source transfer. |
| stale source candidate | Evidence that may no longer be current. | Why might this source be stale? | Observed_at, source timestamp if known, freshness note, stale risk. | Do not infer deletion or uselessness. |
| conflicted source candidate | Evidence that conflicts with another source or claim. | What conflicts and what remains unresolved? | Conflict note, source references, temporal notes. | Do not infer automatic resolution. |
| permission-bound source candidate | Evidence limited by read/view/account permissions. | What permission scope shaped observation? | Permission scope, access scope, reviewer note if available. | Do not infer write or action permission. |
| credential-bound source candidate | Evidence dependent on credential scope or credential state. | Which credential context shaped observation? | Credential scope, observed_at, access note. | Do not infer durable access or credential handling. |
| human review decision | A future human-scoped decision about connector/source use. | Did the reviewer accept, reject, block, or defer source use? | Evidence packet, reviewer note, decision scope, recommended next state. | Do not infer side effects, durable write, or P4 activation. |

## 6. Connector Evidence Fields

This is a document template only, not schema implementation.

| Field | Meaning | When required | Evidence requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `source_id` | Document-local identifier for the source or result. | Required when multiple sources are compared. | Human-assigned ID or explicit unknown marker. | Do not infer durable storage or global identity. |
| `source_type` | Candidate type of source. | Required for reviewable connector/source evidence. | One source type from this taxonomy or documented extension. | Do not infer trust from type alone. |
| `source_location` | Human-readable location or descriptor. | Required when source can be described safely. | Local path, repo reference, URL descriptor, account-scoped descriptor, or unknown marker. | Do not treat location as approval. |
| `connector_name` | Name of the connector or connector class if any. | Required when evidence is connector-derived or connector-like. | Explicit name, future approved label, or not-applicable marker. | Do not infer connector adoption. |
| `connector_result_type` | Kind of result returned or described. | Required for connector-like evidence. | Raw, extracted, transformed, sync, tool, or unknown label. | Do not infer behavior. |
| `query_or_action_context` | The human question, command, query, or action context that produced the observation. | Required when output depends on query/action scope. | Plain-language prompt, command summary, or context descriptor. | Do not infer authorization to repeat action. |
| `observed_at` | When the source/result was observed. | Required when known; required as unknown marker for volatile claims. | Local observation time, source packet time, git evidence, or unknown marker. | Do not infer current truth. |
| `source_timestamp` | Timestamp attached to the source itself. | Required when the source provides one or freshness matters. | Source-visible timestamp, file/git timestamp evidence, or unknown marker. | Do not infer source is current. |
| `sync_timestamp` | Time associated with a sync result. | Required for sync result candidates when known. | Sync metadata, result packet note, or unknown marker. | Do not infer live sync or live truth. |
| `credential_scope` | Credential or account context that shaped access. | Required when credentials or account identity may affect evidence. | Scope descriptor or unknown marker; no secret values. | Do not infer credential handling or ongoing access. |
| `permission_scope` | Read/view/share scope that shaped access. | Required when permissions may affect evidence. | Scope descriptor, reviewer note, or unknown marker. | Do not infer write/action permission. |
| `access_scope` | Practical reach of the observation. | Required when source may be partial, private, or account-scoped. | Bounded description of accessible subset. | Do not infer full-source coverage. |
| `extracted_evidence` | Evidence extracted or summarized from the source. | Required for claim-bearing source use. | Bounded excerpt summary or source-backed observation. | Do not convert evidence into truth. |
| `transformation_note` | How extraction, summary, conversion, or filtering changed source material. | Required when evidence is not raw. | Description of transformation or not-applicable marker. | Do not infer lossless conversion. |
| `provenance_path` | Path from source to evidence to claim. | Required when review depends on traceability. | Source, extraction step, transformation note, claim linkage. | Do not infer source graph traversal. |
| `trust_note` | Qualitative trust context. | Required for external, connector, API, sync, and tool-derived evidence. | Source basis, uncertainty, reviewer note, or unknown trust marker. | Do not infer automatic trust scoring. |
| `freshness_note` | Qualitative freshness context. | Required for volatile or time-sensitive evidence. | Observed_at, source timestamp, sync timestamp, or unknown marker. | Do not infer automatic freshness checks. |
| `conflict_note` | Known or possible conflict with another source or claim. | Required when conflict exists or comparison is missing. | Conflict source, conflict summary, or unknown conflict marker. | Do not resolve conflict automatically. |
| `lifecycle_state` | Candidate lifecycle label for the evidence/source. | Required when state affects use. | Lifecycle label with supporting reason. | Do not infer automatic transition or storage. |
| `temporal_status` | Candidate temporal label for the evidence/source. | Required when time affects use. | Temporal label with source time, observation time, or unknown marker. | Do not infer temporal approval. |
| `recall_trace_reference` | Link or descriptor for a recall trace packet if applicable. | Required when the source appears in recall explanation. | Trace ID, document-local reference, or not-applicable marker. | Do not infer trace persistence. |
| `reviewer_note` | Human review comment or decision note. | Required only when review occurred. | Reviewer note and scope. | Do not infer execution or write permission. |
| `recommended_next_state` | Candidate next review or lifecycle state. | Recommended for review packets. | Rationale tied to evidence, risk, and uncertainty. | Do not infer automatic promotion. |
| `prohibited_inference` | What must not be concluded from the evidence. | Required for high-risk connector/source evidence. | Explicit boundary statement. | Do not treat prohibition as executable logic. |

## 7. Source Type Vocabulary

| Source type | Meaning | Allowed use | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| `local_repo_doc` | A document in the local repository. | Ground repo-governance claims. | File path and relevant section or summary. | Do not infer docs authorize implementation. |
| `local_git_state` | Local branch, commit, tag, status, or log evidence. | Ground repo-state claims. | Command output summary and observed_at. | Do not infer future state or remote truth. |
| `user_instruction` | Direct instruction from the human operator. | Bound task scope and constraints. | Prompt text or summarized instruction. | Do not infer broad future approval. |
| `uploaded_file` | File supplied by the user for this or a future task. | Use as bounded source evidence. | File identity, observed_at, transformation note if summarized. | Do not infer source freshness or ownership beyond scope. |
| `connector_file_result` | File result attributed to a connector-like surface. | Classify file evidence risks. | Source location, access scope, observed_at, transformation note. | Do not infer file connector implementation. |
| `connector_email_result` | Email result attributed to a connector-like surface. | Classify account, privacy, and permission risk. | Timestamp if known, permission scope, credential scope, evidence summary. | Do not infer permission to act. |
| `connector_calendar_result` | Calendar result attributed to a connector-like surface. | Classify event/time/account evidence. | Event/source time if known, account scope, observed_at. | Do not infer attendance or authority. |
| `connector_contact_result` | Contact result attributed to a connector-like surface. | Classify person/contact evidence risk. | Source descriptor, permission scope, observed_at. | Do not infer outreach permission. |
| `connector_repository_result` | Repository result attributed to a connector-like surface. | Classify branch/file/commit evidence. | Repo location, branch/ref if known, observed_at, git evidence. | Do not infer release approval. |
| `connector_drive_result` | Drive or cloud-file result attributed to a connector-like surface. | Classify shared-file and permission risk. | File descriptor, permission scope, observed_at, transformation note. | Do not infer durable access or sync. |
| `external_web_snapshot` | Web source observed at a time. | Support snapshot-based external evidence. | Source location, observed_at, source timestamp if known. | Do not infer current live truth. |
| `external_api_snapshot` | API-like response observed at a time. | Support snapshot-based API evidence. | Query/action context, observed_at, source timestamp if any. | Do not infer API authorization or current status. |
| `tool_output_snapshot` | Output from a tool run or tool-like observation. | Support bounded local or future tool evidence. | Tool name, context, observed_at, output summary. | Do not infer broad tool capability. |
| `benchmark_reference_snapshot` | Benchmark-related source reference. | Inform evaluation questions. | Source, observed_at, benchmark scope, uncertainty. | Do not infer local benchmark approval or pass rate. |
| `product_or_market_snapshot` | Product, market, pricing, ranking, activity, release, issue, or PR-related snapshot. | Use only with freshness warnings. | Source location, observed_at, source timestamp if known. | Do not infer current facts without fresh review. |
| `unknown_source_type` | Source type cannot be reliably classified. | Mark review gap. | Reason for unknown type and available evidence. | Do not infer trust, freshness, or approval. |

## 8. Connector Risk Vocabulary

| Risk label | Meaning | Allowed use | Required evidence | Human review requirement | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| `stale_source_risk` | Source may no longer be current. | Mark time-sensitive evidence. | Old/unknown source time, volatility, or newer-source possibility. | Required before current use. | Do not infer deletion. |
| `missing_timestamp_risk` | Observation or source time is absent. | Mark insufficient time context. | Missing observed_at, source_timestamp, or sync_timestamp. | Required before current use. | Do not infer evergreen truth. |
| `sync_lag_risk` | Sync result may lag behind source state. | Mark sync-result uncertainty. | Sync timestamp/source timestamp gap or unknown sync time. | Required before relying on sync state. | Do not infer live truth. |
| `partial_extraction_risk` | Evidence covers only part of the source. | Mark excerpt, filter, or scope limits. | Extraction scope or missing coverage note. | Required before broad use. | Do not infer full-source coverage. |
| `transformation_loss_risk` | Meaning may have changed during transformation. | Mark summaries, conversions, or normalized outputs. | Transformation note. | Required before high-impact use. | Do not infer lossless conversion. |
| `permission_scope_risk` | Permissions limited the observation. | Mark account/view/read constraints. | Permission scope or unknown marker. | Required before action or sharing. | Do not infer write/action permission. |
| `credential_expiry_risk` | Credential state may have changed. | Mark credential-bound evidence. | Credential scope and observed_at or unknown marker. | Required before treating behavior as current. | Do not infer ongoing access. |
| `source_rewrite_risk` | Source content may have changed after observation. | Mark mutable source classes. | Source class, observed_at, source timestamp if known. | Required before current use. | Do not infer current content. |
| `source_disappearance_risk` | Source may become unavailable. | Mark non-local or account-bound evidence. | Source location and availability uncertainty. | Required before durable reliance. | Do not infer source permanence. |
| `conflicting_source_risk` | Another source or claim disagrees. | Mark unresolved conflict. | Conflict note and source references if known. | Required before deciding. | Do not choose a winner automatically. |
| `trust_overread_risk` | Source reputation may be overread as truth. | Mark authoritative-looking sources. | Trust note and evidence limitation. | Required before promotion. | Do not infer approval from reputation. |
| `benchmark_overread_risk` | Benchmark reference may be overread as local proof. | Mark benchmark or leaderboard references. | Benchmark scope and local non-implementation note. | Required before evaluation use. | Do not infer local benchmark pass or approval. |
| `live_fact_overread_risk` | Volatile claim may be treated as current without fresh review. | Mark product, market, price, ranking, activity, release, issue, PR, or status claims. | Observed_at and freshness note. | Required before current use. | Do not infer live fact. |
| `connector_action_overread_risk` | Observation may be overread as permission to act. | Mark API/tool/connector outputs. | Action context, permission scope, prohibited inference. | Required before any future action. | Do not infer authorization. |
| `unknown_connector_risk` | Risk cannot be classified yet. | Mark insufficient evidence. | Unknown reason and available fields. | Required before use. | Do not infer safety. |

## 9. Trust and Provenance Vocabulary

These labels are non-implemented trust/provenance vocabulary. This is not automatic trust scoring.

| Label | Meaning | Evidence requirement | Review requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `source_observed` | Source was observed under stated scope. | Source location, observed_at if known, evidence summary. | Required before trust. | Do not infer truth. |
| `source_unverified` | Source has not been verified beyond observation. | Observation note and missing verification reason. | Required before use. | Do not infer falsehood or truth. |
| `source_review_required` | Source needs human review before use. | Risk note or missing evidence field. | Required. | Do not infer rejection. |
| `source_reviewed_candidate` | Human reviewed source as candidate evidence within scope. | Reviewer note and review scope. | Already reviewed for stated scope only. | Do not infer durable approval. |
| `source_conflicted` | Source conflicts with another source or claim. | Conflict note and references if known. | Required before use. | Do not infer resolution. |
| `source_stale_candidate` | Source may be stale. | Freshness note, observed_at/source time, or unknown marker. | Required before current use. | Do not infer deletion. |
| `source_historical_only` | Source should inform history, not current guidance. | Historical reason and temporal note. | Required if used for current decisions. | Do not infer uselessness. |
| `source_permission_bound` | Source access depends on permission scope. | Permission scope and access scope. | Required before action/sharing. | Do not infer write permission. |
| `source_credential_bound` | Source access depends on credential/account context. | Credential scope and observed_at. | Required before current behavior claims. | Do not infer ongoing access. |
| `source_transformed` | Evidence was transformed from original source. | Transformation note and provenance path. | Required before high-impact use. | Do not infer raw-source equivalence. |
| `source_unknown_trust` | Trust cannot be assessed yet. | Unknown reason and available evidence. | Required before reliance. | Do not infer safety or approval. |

## 10. Freshness and Temporal-Risk Rules

`observed_at` should be visible when known.

`source_timestamp` should be visible when known.

`sync_timestamp` should be visible when known.

Unknown timestamp must be marked.

Source freshness must not be assumed.

A current-looking connector result may still be stale.

Web/API/source content may change after observation.

External product/market/source claims require fresh review before current use.

A stale source does not mean delete.

A historical source does not mean useless.

Temporal confidence is not approval.

Temporal notes are candidate review aids only. They do not create temporal query logic, automatic expiration, stale-memory detection, supersession behavior, or freshness automation.

## 11. Permission and Credential Scope Rules

Credential scope must be visible when relevant.

Permission scope must be visible when relevant.

Access may change after observation.

Permission to read is not permission to write.

Permission to view is not authorization to act.

A connector result may be private, partial, or account-scoped.

Credential expiry may make old connector behavior historical only.

Missing permission scope requires review.

No credential handling is implemented.

No permission handling is implemented.

Permission and credential notes are review vocabulary only. They do not create access checks, secret storage, credential refresh, permission enforcement, sharing logic, or action authority.

## 12. Sync and Result-State Vocabulary

| Result-state label | Meaning | Required evidence | Safe next state | Prohibited inference |
| --- | --- | --- | --- | --- |
| `raw_result_candidate` | A result kept close to original observation. | Source location, observed_at, context. | Review for extraction or rejection. | Do not infer truth. |
| `extracted_result_candidate` | Evidence extracted from a raw result. | Extracted evidence, source reference, extraction scope. | Review for transformation risk. | Do not infer full-source coverage. |
| `transformed_result_candidate` | Evidence changed by summary, conversion, or normalization. | Transformation note and provenance path. | Review for loss and conflict. | Do not infer raw equivalence. |
| `partial_result_candidate` | Result covers only part of source or query scope. | Access/extraction scope and missing coverage note. | Defer, narrow, or request review. | Do not infer completeness. |
| `stale_result_candidate` | Result may be old or no longer current. | Freshness note, observed_at, source/sync timestamp if known. | Mark historical, refresh by future approved process, or review. | Do not infer deletion. |
| `conflicted_result_candidate` | Result disagrees with another source or claim. | Conflict note and source references if known. | Human review or block current use. | Do not resolve automatically. |
| `permission_bound_result` | Result depends on read/view/account permission. | Permission scope and access scope. | Human review before action/sharing. | Do not infer write permission. |
| `credential_bound_result` | Result depends on credential/account state. | Credential scope and observed_at. | Human review before current behavior claims. | Do not infer ongoing access. |
| `reviewed_result_candidate` | Human reviewed the result as candidate evidence. | Reviewer note, scope, recommended next state. | Candidate use within scope or further review. | Do not infer durable memory write. |
| `rejected_result_candidate` | Human rejected the result for stated scope. | Rejection reason and source reference. | Preserve reason as candidate history if needed. | Do not infer deletion of evidence. |
| `historical_result_snapshot` | Result is useful as history, not current guidance. | Historical reason, observed_at/source time if known. | Use as historical context only. | Do not infer current authority. |
| `unknown_result_state` | Result state cannot be classified yet. | Unknown reason and available fields. | Human review required. | Do not infer safety. |

## 13. Allowed Evidence vs Prohibited Inference

| Evidence surface | Allowed evidence use | Prohibited inference |
| --- | --- | --- |
| connector result | Classify as candidate evidence with source, scope, time, trust, freshness, and permission notes. | Do not infer connector implementation, approved memory, sync, action, or truth. |
| external source page | Use as observed snapshot or methodology context. | Do not infer live truth, dependency approval, or source permanence. |
| API response | Use as bounded observation with query/action context. | Do not infer authorization, API adoption, current status, or permission to act. |
| uploaded file | Use as user-provided source evidence under task scope. | Do not infer current truth, complete coverage, or durable memory write. |
| repo file | Use as local governance evidence. | Do not infer old docs changed or authorize implementation. |
| git log | Use as local repository history evidence. | Do not invent release meanings, PR meanings, or future state beyond inspected log. |
| tool output | Use as bounded observation from a command or tool context. | Do not infer broad capability, permission, or future behavior. |
| benchmark reference | Use as evaluation-question context. | Do not infer local benchmark implementation, pass rate, or approval. |
| product/market snapshot | Use only as time-bound source evidence with freshness warning. | Do not infer current price, rank, release, issue, PR, activity, or market truth. |
| email/calendar/contact result | Use as account-scoped evidence with permission and privacy notes. | Do not infer permission to write, contact, schedule, disclose, or act. |
| web source | Use as observed external snapshot. | Do not infer current live content without fresh review. |
| transformed summary | Use as review aid with transformation note. | Do not infer raw-source equivalence or lossless extraction. |

## 14. Lifecycle Interaction

Connector governance interacts with the Memory Lifecycle Taxonomy by keeping connector/source evidence in visible candidate states before any later human decision.

A connector result starts as candidate.

Reviewed connector evidence may still be time-bound.

A stale source does not mean deletion.

A superseded source does not mean erasure.

A rejected source candidate must preserve reason.

A blocked source must show `blocked_reason`.

A `historical_only` source must show why it is historical, not current guidance.

Lifecycle confidence is not approval.

Lifecycle labels in connector governance do not create lifecycle storage, a lifecycle state machine, transition logic, automatic promotion, automatic rejection, archival, deletion, stale-memory detection, automatic expiration, or supersession behavior.

## 15. Temporal Validity Interaction

Connector governance interacts with the Temporal Validity Model by separating observation time, source time, and sync time.

`source_timestamp`, `observed_at`, and `sync_timestamp` must be separated.

`valid_from` and `valid_until` may be unknown.

`unknown_time_scope` requires review.

Source freshness must be explicit.

Volatile external claims must be treated as time-bound.

Product, market, price, ranking, activity, release, issue, PR, and benchmark claims are volatile.

Current use requires fresh review.

No temporal query logic is implemented.

Temporal validity interaction in this document is taxonomy only. It does not implement source freshness checks, temporal queries, stale detection, automatic expiration, automatic source refresh, or supersession logic.

## 16. Explainable Recall Trace Interaction

Connector governance interacts with the Explainable Recall Trace Template by making connector/source evidence paths visible without turning recall explanation into adoption.

A connector/source trace must show `source_type`.

A connector/source trace must show `source_location`.

A connector/source trace must show `observed_at` when known.

A connector/source trace must show `source_timestamp` when known.

A connector/source trace must show `transformation_note` when applicable.

A connector/source trace must show `connector_source_risk`.

A connector/source trace must separate evidence / claim / inference.

A connector/source trace must not become connector adoption.

A connector/source trace must not become authorization.

Trace interaction in this document does not implement recall storage, recall engine behavior, retrieval logic, ranking logic, trace persistence, source graph traversal, or automated explanation generation.

## 17. Failed Attempt Interaction

Connector governance interacts with Failed Attempt Memory / Do-Not-Retry Rules by classifying connector-related failures as scoped candidates, not permanent prohibitions.

Connector failures may be failed-attempt candidates.

Sync lag failure may be recorded as candidate.

A stale source recommendation may be failed-attempt candidate.

A credential failure may be credential-bound failure.

A permission failure may be permission-bound failure.

Connector result overread may be process-overreach failure.

A do-not-retry candidate must remain scoped.

A connector failure must not block improved future connector use without review.

Failed-attempt interaction in this document does not implement failed-attempt storage, do-not-retry enforcement, retry blocker logic, connector failure detection, or automatic blocking.

## 18. Human Review Gate Readiness for Connector Decisions

Before any later P4 consideration, connector/source decisions are review-ready only when the reviewer can inspect the bounded evidence and reject, block, defer, or narrow use without side effect.

Readiness criteria:

- reviewer can see `source_type`
- reviewer can see `source_location`
- reviewer can see `connector_name` if any
- reviewer can see `query_or_action_context` if any
- reviewer can see `observed_at`
- reviewer can see `source_timestamp` / `sync_timestamp` if known
- reviewer can see `credential_scope` / `permission_scope` if relevant
- reviewer can see `extracted_evidence`
- reviewer can see `transformation_note`
- reviewer can see `trust_note`
- reviewer can see `freshness_note`
- reviewer can see `conflict_note`
- reviewer can see `prohibited_inference`
- reviewer can reject source use without side effect
- reviewer can block source use without side effect
- reviewer decision is recorded as candidate only
- P4 remains paused
- P4 requires explicit human confirmation later

Human review readiness is not approval, not product implementation authorization, not a connector build plan, and not P4 activation.

## 19. Non-Authorization Rules

Connector result is not truth.

External source is not approval.

API response is not authorization.

Sync result is not live truth.

Source freshness is not assumed.

Permission to read is not permission to write.

Permission to view is not permission to act.

Source path is not governance approval.

Benchmark reference is not local benchmark approval.

Connector trace is not connector adoption.

Connector candidate is not adapter implementation.

Connector evidence is not Memory Graph mutation.

Connector result is not durable memory write.

These rules apply to docs, review packets, future proposals, source snapshots, tool observations, API-like outputs, sync-like outputs, file/document connector-like results, and external methodology references.

## 20. Candidate Examples

These examples are illustrative only. They are generic examples, not live facts, not connector results, and not implementation approval.

| Example | Source type | Likely connector risk | Required fields | Safe reviewer action | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| connector file result with missing timestamp | `connector_file_result` | `missing_timestamp_risk`, `partial_extraction_risk` | source_location, observed_at or unknown marker, extracted_evidence, transformation_note, prohibited_inference | Mark review required or historical-only until time scope is clear. | Do not infer file is current or fully ingested. |
| API response with volatile current status | `external_api_snapshot` | `live_fact_overread_risk`, `source_rewrite_risk` | query_or_action_context, observed_at, source_timestamp if known, freshness_note | Require fresh review before current use. | Do not infer current status or authorization. |
| uploaded file used as source evidence | `uploaded_file` | `transformation_loss_risk`, `partial_extraction_risk` | source_id, source_location, observed_at, extracted_evidence, transformation_note | Accept as bounded candidate evidence or request narrower citation. | Do not infer durable memory write. |
| web source snapshot with stale risk | `external_web_snapshot` | `stale_source_risk`, `source_rewrite_risk` | source_location, observed_at, source_timestamp if known, freshness_note | Treat as time-bound or historical until reviewed. | Do not infer current live truth. |
| git log used as local evidence | `local_git_state` | `live_fact_overread_risk` if broadened beyond local state | branch/ref context, observed_at, command output summary | Use for local repo history under inspected scope. | Do not invent release meanings or future state. |
| benchmark reference overread as approval | `benchmark_reference_snapshot` | `benchmark_overread_risk`, `trust_overread_risk` | source_location, observed_at, benchmark scope, prohibited_inference | Use only to shape evaluation questions. | Do not infer local benchmark approval or pass. |
| connector sync lag causing wrong recommendation | `sync_result_candidate` | `sync_lag_risk`, `stale_source_risk` | sync_timestamp, source_timestamp if known, freshness_note, failed-attempt note if applicable | Mark as failed-attempt candidate and require review. | Do not infer sync result is live truth. |
| permission-bound email/calendar/contact result | `connector_email_result`, `connector_calendar_result`, or `connector_contact_result` | `permission_scope_risk`, `credential_expiry_risk` | permission_scope, credential_scope, observed_at, access_scope, extracted_evidence | Restrict to candidate evidence and require human review before use. | Do not infer permission to write, contact, schedule, or act. |

## 21. Candidate Future Sequence

Recommended docs-only sequence:

1. Memory Ontology Mapping
2. External Product Explanation Candidate
3. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

The sequence is reading and documentation control only. It is not implementation planning, product approval, connector adoption, dependency work, adapter work, source ingestion, sync behavior, API/MCP operation design, or v7 implementation authorization.

## 22. Prohibited Implementation Rules

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

Do not implement automatic source promotion.

Do not implement automatic memory writing.

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

Do not treat connector result as truth.

Do not treat connector source trace as connector adoption.

Do not treat API response as authorization.

Do not treat sync result as live truth.

Do not treat permission to read as permission to act.

Do not treat connector evidence as Memory Graph mutation.

## 23. Stop Conditions

If connector governance taxonomy turns into code, stop.

If connector governance taxonomy turns into tests, stop.

If connector governance taxonomy turns into connector logic, stop.

If connector governance taxonomy turns into connector storage, stop.

If connector governance taxonomy turns into connector sync, stop.

If connector governance taxonomy turns into API calls, stop.

If connector governance taxonomy turns into MCP tools, stop.

If connector governance taxonomy turns into adapter behavior, stop.

If connector governance taxonomy turns into credential handling, stop.

If connector governance taxonomy turns into permission handling, stop.

If connector governance taxonomy turns into source ingestion, stop.

If connector governance taxonomy turns into source polling, stop.

If connector governance taxonomy turns into freshness checks, stop.

If connector governance taxonomy turns into automatic trust scoring, stop.

If connector governance taxonomy turns into automatic source promotion, stop.

If connector governance taxonomy turns into automatic memory writing, stop.

If connector governance taxonomy turns into recall engine or retrieval logic, stop.

If connector governance taxonomy turns into trace persistence, stop.

If connector governance taxonomy turns into Memory Graph mutation, stop.

If connector governance taxonomy turns into durable writer, stop.

If connector governance taxonomy turns into dependency adoption, stop.

If connector governance taxonomy turns into MCP/API operation surface, stop.

If connector governance taxonomy turns into authorization/execution semantics, stop.

If connector governance taxonomy starts P4, stop.

If connector governance taxonomy starts v7 implementation, stop.

If connector governance taxonomy starts MVP/product deployment, stop.

If connector governance taxonomy starts changing old docs, stop.

If `pyproject.toml` version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 24. Final Taxonomy Statement

This document defines connector governance taxonomy candidates only.

It does not evaluate live connector data.

It does not implement connector behavior.

It does not implement sync behavior.

It does not implement source ingestion.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
