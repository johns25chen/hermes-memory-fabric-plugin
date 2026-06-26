# Civilization Core Failed Attempt Memory / Do-Not-Retry Rules / 文明之核失败经验记忆与禁止重试规则

## 2. Rules Status

This is a docs-only failed-attempt memory and do-not-retry rules document.

It is based on the sealed `v6.16.0` Civilization Core Stable Kernel.

It is based on the merged Memory Evaluation Candidates document.

It is based on the merged Temporal Validity Model document.

It is based on the merged Memory Lifecycle Taxonomy document.

It is rules-candidate only.

It creates no failed-attempt storage.

It creates no do-not-retry enforcement.

It creates no retry blocker logic.

It creates no failure detector logic.

It creates no automatic rule creation.

It creates no automatic blocking.

It creates no automatic retry prevention.

It creates no lifecycle storage.

It creates no lifecycle state machine.

It creates no lifecycle transition logic.

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

The rules in this document are candidate governance vocabulary only. They do not approve implementation, productization, connector adoption, dependency adoption, external project behavior, durable memory writing, graph mutation, automatic authorization, automatic blocking, or automatic execution.

## 3. Why Failed Attempt Memory Matters

Repeated failed paths waste operator time.

Failed attempts can protect future work only when scoped precisely. A failed command, design assumption, workflow, tool behavior, environment condition, or assistant assumption is useful only when a later reviewer can see what failed, what evidence showed failure, and which scope controlled that failure.

Do-not-retry is useful only as reviewed candidate guidance, not law.

Failure memory must preserve evidence, context, tool version, repo state, branch, network condition, and user preference scope when relevant.

Old failures may become historical only.

Failed-attempt memory must not freeze future improvement.

Failed-attempt state is not truth.

Retry-risk confidence is not approval.

Human review remains required before a failed attempt is treated as current guidance, before a do-not-retry candidate is accepted, before a retry is blocked by human decision, or before a failed path is narrowed, superseded, rejected, or marked historical only.

## 4. Failed Attempt Boundary

| Area | Included? | Reason | Boundary |
| --- | --- | --- | --- |
| failed attempt record | yes | Future docs need a bounded way to describe a failed action, command, assumption, or path. | Candidate vocabulary only; no storage behavior follows. |
| failure evidence | yes | A failure without evidence can become folklore. | Evidence requirement only; it is not automatic detection. |
| failure scope | yes | Scope prevents one narrow failure from blocking adjacent work. | Scope fields only; they do not create enforcement. |
| retry-risk note | yes | A reviewer needs visible risk before repeating a path. | Qualitative note only; it is not approval or denial. |
| do-not-retry candidate | yes | Some paths should not be repeated under the same conditions without review. | Candidate guidance only; not automatic law. |
| scoped block reason | yes | A reviewer needs to see why a retry is risky. | Review vocabulary only; no retry blocker logic. |
| exception condition | yes | Future improvements, new evidence, user approval, or environment changes may permit retry. | Human-readable condition only; no automatic unblocking. |
| historical-only failure | yes | Old failures can remain useful without current authority. | Lifecycle label only; not deletion or current block. |
| superseded failure | yes | Later success or better evidence may narrow an old failure. | Relationship label only; not an overwrite. |
| narrowed failure rule | yes | Scope may be reduced when evidence supports a narrower reading. | Review vocabulary only; not silent mutation. |
| user correction | yes | User corrections can reject assistant assumptions or narrow a failed path. | Evidence for review only; not automatic durable memory. |
| tool/version scope | yes | Tool behavior can change across versions. | Scope field only; it does not query tool versions. |
| repo/branch scope | yes | Failure may depend on a repository state or branch. | Scope field only; it does not inspect branches. |
| network/environment scope | yes | Failures may depend on network, credentials, permissions, or local environment. | Scope field only; no connector or environment monitor. |
| automatic retry blocking | no | Automatic blocking would be behavior, not rules vocabulary. | Excluded; no automatic retry blocking is created. |
| automatic failure detection | no | Detection would require runtime or tool behavior. | Excluded; no automatic failure detection is created. |
| automatic rule creation | no | Rule creation requires review and scope. | Excluded; no automatic rule creation is created. |
| enforcement behavior | no | Enforcement would turn candidate rules into operation. | Excluded; no enforcement behavior is created. |
| Memory Graph mutation | no | Graph writes would change durable memory surfaces. | Excluded; no Memory Graph mutation is created. |
| P4 gate activation | no | P4 requires explicit human confirmation later. | Excluded; P4 remains paused. |

## 5. Failed Attempt Object Types

These object types may later receive failed-attempt labeling in docs or review packets. This section defines vocabulary only, not schema or behavior.

| Object type | What it is | Failure question | Required evidence | Prohibited inference |
| --- | --- | --- | --- | --- |
| failed attempt candidate | A proposed description of a failed action or path. | What exactly failed, and under which scope? | Attempt summary, observed signal, source reference, scope note. | Do not infer approved memory, durable write, or permanent impossibility. |
| failed command record | A command or shell workflow that did not produce the expected result. | Did the same command fail under the same repo, branch, tool, and environment scope? | Command, expected result, actual result, error output if available. | Do not infer all related commands are unsafe. |
| failed design assumption | An architecture or planning assumption later shown to be wrong or unsupported. | Which assumption failed, and what evidence corrected it? | Assumption text, correction source, reviewer note if available. | Do not infer the whole design area is invalid. |
| failed workflow path | A multi-step process that failed or led to boundary risk. | Which step failed, and what condition controlled the failure? | Workflow steps, failure signal, scope, blocked reason. | Do not infer every alternate workflow is blocked. |
| failed tool behavior note | A note that a tool behaved unexpectedly or was unavailable. | Was the behavior tied to version, auth, platform, or session state? | Tool name, tool version if known, observed output, environment scope. | Do not infer future tool behavior without current evidence. |
| failed network/environment condition | A failure caused or plausibly caused by local environment, permissions, credentials, or network. | Which environment condition was observed? | Error output, environment scope, network scope, observed time. | Do not infer permanent outage or global failure. |
| rejected assistant assumption | A user or evidence source rejected an assistant's assumption. | What did the assistant assume, and what corrected it? | Assumption text, correction, source or user preference scope. | Do not infer deletion of the record or broad assistant prohibition. |
| do-not-retry candidate | A proposed rule to avoid repeating a specific failed path under stated conditions. | What exact retry should not be repeated without review? | Failed attempt reference, blocked retry, scope, exception condition. | Do not infer automatic authority or indefinite ban. |
| narrowed do-not-retry candidate | A candidate whose blocked path was reduced to a narrower scope. | What old scope was too broad, and what narrower scope remains? | Original candidate, narrowing evidence, reviewer note if available. | Do not infer the original evidence was erased. |
| superseded failure record | A failure record limited by later success or stronger evidence. | What later evidence changes how the old failure should be read? | Old failure, successor evidence, supersession rationale. | Do not infer silent overwrite or audit removal. |
| historical-only failure record | A failure retained as past context, not current guidance. | Why is the failure historical rather than current? | Observed time, temporal scope, reason for historical-only status. | Do not infer uselessness or deletion. |
| blocked retry candidate | A candidate saying retry should pause until review or new evidence. | What makes retry unsafe or wasteful right now? | Blocked reason, evidence gap or failure signal, scope. | Do not infer permanent law outside the stated scope. |
| safe retry candidate | A candidate saying retry may be reasonable after review and changed scope. | What changed enough to permit retry consideration? | Changed scope, new evidence, exception condition, reviewer note if available. | Do not infer approval to execute. |
| human review decision | A future human-scoped decision about failure and retry status. | What did the reviewer decide, and with what scope? | Evidence packet, reviewer note, decision scope, recommended next state. | Do not infer execution, write, deployment, or P4 activation. |

## 6. Failure Evidence Fields

This is a document template only, not schema implementation.

| Field | Meaning | When required | Evidence requirement | Prohibited inference |
| --- | --- | --- | --- | --- |
| `attempt_id` | A stable discussion identifier for the attempt. | Required when multiple attempts may be compared. | Human-assigned or document-local identifier. | Do not infer durable storage or global identity. |
| `attempt_summary` | Short description of what was tried. | Required for every failed-attempt candidate. | Plain-language summary tied to the observed attempt. | Do not infer completeness by summary alone. |
| `attempted_action` | The concrete action, command, workflow, prompt, assumption, or design path. | Required for retry-risk review. | Exact command/workflow text when available, or precise prose. | Do not generalize beyond the described action. |
| `expected_result` | What the operator expected to happen. | Required when failure depends on mismatch. | Expected output, intended state, or review goal. | Do not infer the expectation was correct. |
| `actual_result` | What happened instead. | Required for every failure claim. | Observed output, state, error, user correction, or source evidence. | Do not infer root cause from result alone. |
| `failure_signal` | The visible signal that the attempt failed. | Required for failure classification. | Error, mismatch, rejection, blocked state, or boundary violation. | Do not infer automatic failure detection. |
| `error_output` | Error text or diagnostic output when available. | Required when a command/tool produced it. | Verbatim or summarized local output with scope note. | Do not infer broad failure outside the output scope. |
| `observed_at` | When the failure was observed. | Required when time, version, branch, tool, or environment may change. | Local observation time, source timestamp, or note that time is unknown. | Do not infer the failure is still current. |
| `tool_version` | Tool or dependency version relevant to the failure. | Required when tool behavior may vary by version. | Local version output or explicit unknown marker. | Do not infer all versions behave the same. |
| `repo_state` | Repository state relevant to the attempt. | Required for repo-dependent failures. | Git status, commit/log context, or source doc context. | Do not infer future repo state. |
| `branch_name` | Branch where the failure happened. | Required for branch-sensitive failures. | Local branch evidence or explicit unknown marker. | Do not infer other branches are affected. |
| `command_or_workflow` | The command, prompt path, or workflow sequence. | Required for command and workflow failures. | Exact command where safe, or step list. | Do not infer every adjacent workflow is blocked. |
| `environment_scope` | Local OS, permissions, credentials, sandbox, or tool session context. | Required when environment may explain failure. | Environment note, permission output, or explicit unknown marker. | Do not infer global environment failure. |
| `network_scope` | Network, proxy, remote service, or offline condition. | Required when network could affect the result. | Error output, connection note, or explicit unknown marker. | Do not infer permanent remote failure. |
| `user_preference_scope` | User instruction or preference that affects retry status. | Required when failure or block depends on user preference. | User instruction, correction, or scoped preference note. | Do not freeze old preference as permanent. |
| `source_reference` | Local doc, command output, user message, or review packet supporting the record. | Required for reviewable candidates. | Inspectable source path or bounded source description. | Do not treat source existence as approval. |
| `retry_risk` | Qualitative label for retry risk. | Required before suggesting safe retry, blocked retry, or do-not-retry. | Tied to failure evidence and scope. | Do not treat risk confidence as approval. |
| `blocked_reason` | Why retry should pause or be avoided under stated conditions. | Required for blocked retry and do-not-retry candidates. | Evidence-backed reason and scope. | Do not infer permanent prohibition outside scope. |
| `exception_condition` | What change or review could permit reconsideration. | Required for do-not-retry candidates when known. | Tool/version/environment/user/evidence change or explicit unknown. | Do not infer automatic unblocking. |
| `reviewer_note` | Human review comment or decision note. | Required for reviewed status. | Explicit reviewer note. | Do not infer execution permission. |
| `recommended_next_state` | Candidate lifecycle state for later review. | Recommended for review packets. | Rationale tied to evidence. | Do not infer automatic transition. |

These fields create no storage format, parser, validator, failure detector, retry blocker, enforcement rule, lifecycle state machine, temporal query engine, durable writer, API, adapter, or graph mutation.

## 7. Failure Category Vocabulary

| Failure category | Meaning | Typical evidence | Review question | Prohibited inference |
| --- | --- | --- | --- | --- |
| `command_failure` | A command did not complete or produced the wrong result. | Command, exit/error output, expected vs actual result. | Is the failure specific to command, args, branch, tool, or environment? | Do not infer all command paths are blocked. |
| `tool_login_failure` | A tool failed because login, session, entitlement, or credential state was wrong or unavailable. | Auth error, status output, session note. | Is this still true for the current credential state? | Do not infer permanent account or tool failure. |
| `network_failure` | Network, proxy, remote endpoint, or connectivity affected the attempt. | Connection error, timeout, proxy note, offline condition. | Did network condition change before retry? | Do not infer source content or remote service status beyond evidence. |
| `permission_failure` | Local permission, approval, sandbox, or access blocked the attempt. | Permission error, approval decision, blocked operation note. | Which permission scope controlled the failure? | Do not infer all permissions are unavailable. |
| `branch_state_failure` | Branch, commit, merge, or repo state made the attempt invalid. | Branch name, git status, log, missing file. | Does the failure apply to this branch only? | Do not infer other branches fail. |
| `version_mismatch_failure` | Tool, package, protocol, or doc version mismatch caused or contributed to failure. | Version output, package file, incompatibility message. | Which version range is affected? | Do not infer all versions are incompatible. |
| `dirty_worktree_failure` | Existing changes made the attempted action unsafe or invalid. | `git status`, changed-file list, protected file note. | Which files and actions were unsafe? | Do not infer clean worktree retry is blocked. |
| `protected_file_failure` | Attempt would touch a forbidden file or surface. | User constraint, changed-file check, path evidence. | Which file rule was violated or nearly violated? | Do not infer all docs work is blocked. |
| `test_failure` | A test, smoke, lint, or validation command failed. | Test command, output, failing assertion or check. | Is the failure due to code, environment, or test assumptions? | Do not infer benchmark or implementation authority. |
| `documentation_scope_failure` | Work drifted outside allowed docs-only or allowed-file scope. | Diff/status evidence, user constraint, file path. | What boundary was crossed? | Do not infer implementation is needed to fix it. |
| `prompt_scope_failure` | A prompt, instruction, or assistant response exceeded the requested scope. | User correction, prompt text, overreach note. | What exact instruction was violated? | Do not infer all related prompts are unsafe. |
| `hallucinated_assumption_failure` | A claim or plan relied on unsupported facts. | Correction, missing source, contradicted local evidence. | What evidence is required before reuse? | Do not infer truth from confidence. |
| `external_source_stale_failure` | Old or volatile external source material caused a wrong or risky recommendation. | Dated source, stale note, changed context. | Is fresh source review required? | Do not infer current live facts from old source. |
| `connector_risk_failure` | Connector, sync, API, credential, or source-class risk distorted memory or recommendation. | Connector/source note, sync lag, credential state, source mismatch. | Which connector/source risk must be reviewed? | Do not infer connector adoption or operation surface. |
| `user_preference_violation` | Attempt contradicted current user instruction or preference scope. | User instruction, correction, task constraint. | Was the preference current, scoped, and relevant? | Do not infer permanent preference outside scope. |
| `process_overreach_failure` | Work turned candidate docs into implementation, productization, P4, v7, or operation semantics. | Diff, wording, status, changed surface. | Which boundary must stop the work? | Do not repair by expanding implementation. |
| `unknown_failure` | The failure signal exists but cause or scope is not reliable. | Partial output, missing evidence, uncertainty note. | What evidence is missing before retry? | Do not infer safe retry or permanent block. |

## 8. Retry-Risk Vocabulary

These are non-implemented retry-risk labels.

| Retry-risk label | Meaning | Allowed use | Required evidence | Human review requirement | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| `safe_to_retry_after_review` | Retry may be reasonable after a human checks evidence and scope. | Use when failure was narrow or conditions appear corrected. | Changed condition, prior evidence, remaining risks. | Required before action. | Do not infer execution approval. |
| `retry_with_changed_scope` | Retry may be reasonable only if branch, command, workflow, file scope, or goal changes. | Use when same broad idea remains valid but the prior path failed. | Prior failed path and changed-scope explanation. | Required to confirm new scope. | Do not infer the old path is safe. |
| `retry_only_with_new_evidence` | Retry should wait for new evidence. | Use when old evidence is missing, stale, or contradicted. | Evidence gap and source needed. | Required before treating evidence as sufficient. | Do not infer current truth. |
| `retry_only_after_environment_change` | Retry depends on changed tool, credential, permission, network, or local environment. | Use for environment-sensitive failures. | Prior environment scope and changed condition. | Required if change affects decision. | Do not infer automatic unblocking. |
| `retry_only_after_user_approval` | Retry requires explicit user approval because scope, risk, or preference is sensitive. | Use when user instruction or high-risk boundary controls retry. | User preference scope, blocked reason, requested approval point. | Required and explicit. | Do not infer approval from silence. |
| `do_not_retry_candidate` | A specific failed path should not be repeated under the same conditions without review. | Use for precise, evidenced failed paths. | Failed attempt, blocked retry, scope, exception condition. | Required before any accepted block. | Do not infer automatic law. |
| `blocked_until_review` | Retry should pause until a reviewer examines evidence. | Use when risk, scope, or evidence gap is too high. | Blocked reason and missing review need. | Required to unblock. | Do not infer permanent prohibition. |
| `historical_only_failure` | Failure is retained as past context, not current retry guidance. | Use for old, superseded, or environment-bound failures. | Observed time, historical reason, scope. | Required if it affects decisions. | Do not infer uselessness. |
| `superseded_failure` | Later evidence may limit or replace the failure's current guidance. | Use when later success, version change, or better source exists. | Old failure and successor/narrowing evidence. | Required before treating successor as active. | Do not infer erasure. |
| `unknown_retry_risk` | Retry risk cannot be judged. | Use when evidence or scope is missing. | Missing-evidence note and known risk flags. | Required before retry guidance. | Do not infer safe retry or block. |

## 9. Do-Not-Retry Candidate Rules

Do-not-retry starts as candidate, not law.

It must describe the exact failed path.

It must describe the exact blocked retry.

It must include evidence.

It must include scope.

It must include exception condition.

It must include review requirement.

It must not block adjacent improved approaches.

It must not block future tool, version, or environment improvements.

It must not override user instruction without review.

It must not become automatic enforcement.

A valid candidate says: "do not repeat this exact path under these same conditions without review." It does not say: "this goal is impossible" or "no future path may work."

## 10. Scoped Retry Decision Matrix

| Situation | Candidate label | Required evidence | Safe next action | Prohibited action |
| --- | --- | --- | --- | --- |
| same command, same branch, same error | `do_not_retry_candidate` or `blocked_until_review` | Command, branch, error output, observed time. | Pause and review exact failure scope. | Re-run blindly or broaden block to all commands. |
| same idea, changed implementation | `retry_with_changed_scope` | Prior failed path and changed design/workflow. | Review whether the new path avoids the old failure. | Treat old failure as proof the idea is impossible. |
| same tool, newer version | `retry_only_after_environment_change` | Prior tool version, new version evidence, old error. | Review version-specific risk before retry. | Assume new version is automatically safe or unsafe. |
| same repo, different branch | `retry_with_changed_scope` | Prior branch, new branch, repo-state difference. | Check branch-specific applicability. | Apply branch failure to all branches without evidence. |
| same command, network changed | `retry_only_after_environment_change` | Prior network failure and changed network condition. | Review whether network was controlling factor. | Treat old network failure as permanent. |
| same workflow, user preference changed | `retry_only_after_user_approval` or `retry_with_changed_scope` | Old preference, new user instruction, affected workflow. | Ask or document scope before retry. | Freeze the user to old preference. |
| previous failure had missing evidence | `unknown_retry_risk` or `retry_only_with_new_evidence` | Evidence gap, missing output, unknown scope. | Gather reviewable evidence before guidance. | Convert weak memory into do-not-retry. |
| previous failure superseded by later success | `superseded_failure` or `historical_only_failure` | Old failure, later success, scope comparison. | Preserve old evidence and narrow current guidance. | Erase old record or claim universal success. |
| failure involved protected file or dirty worktree | `blocked_until_review` | Status output, protected path, user constraint. | Stop and review changed-file scope. | Modify protected files or clean worktree destructively. |
| failure involved P4/v7/product overreach | `do_not_retry_candidate` or `blocked_until_review` | Overreach text, boundary source, task constraint. | Return to docs-only candidate boundary. | Start P4, v7 implementation, MVP, or product deployment. |

## 11. Temporal Interaction

Failed-attempt memory must interact with the Temporal Validity Model by preserving time and scope instead of pretending that a past failure is timeless.

A failure may be valid only for a tool version.

A failure may be valid only for a repo state.

A failure may be valid only for a branch.

A failure may be valid only for a network condition.

A failure may be valid only for a user preference.

Old failures may become `historical_only`.

Retry rules must preserve `observed_at`.

Retry rules should preserve `valid_until` or `exception_condition` when known.

Unknown time scope should require review.

Temporal labels do not expire, query, supersede, block, unblock, write, or delete anything by themselves.

## 12. Lifecycle Interaction

Failed-attempt memory must interact with the Memory Lifecycle Taxonomy by starting weak and becoming stronger only through review.

Failed attempt starts as `proposed` or `candidate`.

Do-not-retry starts as `candidate`.

Review can mark `active_time_bound`.

Review can mark `historical_only`.

Review can mark `superseded`.

Review can mark `rejected`.

Review can block use.

Stale failure does not mean delete.

Superseded failure does not mean erase.

Rejected do-not-retry does not erase evidence.

Lifecycle labels do not create lifecycle storage, state machine behavior, transition behavior, automatic promotion, automatic rejection, automatic archival, automatic deletion, automatic expiration, or stale detection.

## 13. Supersession and Narrowing Rules

Later successful retry may supersede old failure only after review.

Changed tool version may narrow old failure scope.

Changed branch may narrow old failure scope.

Changed network condition may narrow old failure scope.

Changed user preference may narrow old failure scope.

Better evidence may narrow or reject do-not-retry.

Supersession must preserve old failure evidence.

Narrowing must preserve original blocked path.

Narrowing must not erase audit trail.

Supersession and narrowing are review concepts here. They are not a supersession engine, replacement mechanism, hidden overwrite, or deletion path.

## 14. Anti-Overblocking Rules

Do not block broad categories from one narrow failure.

Do not block improved approaches.

Do not block user-approved retry.

Do not block fresh evidence review.

Do not block different branch, version, or environment unless evidence supports it.

Do not turn assistant caution into system law.

Do not treat failed attempt as proof of impossibility.

Do not hide uncertainty.

Do not delete failure evidence when narrowing or superseding.

Do-not-retry candidate language must stay precise enough that a future reviewer can ask: "same path, same scope, same evidence, same risk?" If the answer is no, the candidate should be narrowed, reviewed, or treated as historical only.

## 15. Connector and External Source Failure Risk

External sources and connectors can fail in ways that create wrong recommendations or overconfident memory.

| Risk | Meaning | Safe rules response |
| --- | --- | --- |
| stale external source caused wrong recommendation | A source snapshot was treated as current when it was old or context-bound. | Mark time scope and require fresh review before current use. |
| connector sync lag caused wrong memory | Synced content lagged behind source state. | Treat connector output as candidate and require sync-time evidence. |
| missing timestamp caused false current claim | A claim lacked `observed_at` or source time. | Mark unknown time scope and review required. |
| external API behavior changed | A remote behavior claim no longer matched later behavior. | Treat as time-bound and version/source scoped. |
| credential state changed | Login, token, role, or entitlement changed between attempts. | Scope failure to credential state and require review before retry. |
| repository activity changed | Repo activity, releases, commits, issues, PRs, stars, forks, or watchers changed after observation. | Treat prior activity claims as historical unless freshly verified under separate scope. |
| web source disappeared or changed | A page moved, vanished, or changed content. | Preserve source reference and mark stale or unknown scope. |
| source trust was overestimated | A source was treated as more authoritative than evidence allowed. | Record trust risk and require human review. |
| external benchmark was treated as local approval | External results were overread as governance permission. | Mark process overreach and block implementation inference. |

This document adds no connector, adapter, MCP/API surface, sync behavior, action behavior, or enforcement behavior.

## 16. Human Review Gate Readiness for Failed Attempt Decisions

Before any later P4 consideration, a human reviewer must be able to see:

- failed action;
- evidence;
- `observed_at`;
- `tool_version` if relevant;
- `repo_state` / `branch_name` if relevant;
- `environment_scope` / `network_scope` if relevant;
- `user_preference_scope` if relevant;
- `retry_risk`;
- `blocked_reason`;
- `exception_condition`;
- that reviewer can reject do-not-retry without side effect;
- that reviewer can mark `historical_only` without side effect;
- that reviewer decision is recorded as candidate only.

P4 remains paused.

P4 requires explicit human confirmation later.

Human review readiness means a reviewer can inspect, accept, reject, block, defer, narrow, supersede, or mark historical-only without hidden mutation, hidden enforcement, hidden write, hidden execution, hidden operation surface, or hidden product launch.

## 17. Candidate Examples

These examples are illustrative only.

| Example | Failed memory type | Likely retry-risk label | Required evidence | Safe next state | Prohibited inference |
| --- | --- | --- | --- | --- | --- |
| command failed because worktree was dirty | failed command record | `blocked_until_review` or `retry_with_changed_scope` | Command, `git status`, affected files. | Retry only after review of clean or intended worktree scope. | Do not infer the command is impossible. |
| command failed because branch was wrong | failed command record | `retry_with_changed_scope` | Branch name, expected branch, error or mismatch. | Review correct-branch retry. | Do not infer every branch fails. |
| push failed because network/proxy failed | failed network/environment condition | `retry_only_after_environment_change` | Network/proxy error and observed time. | Retry only after network condition review. | Do not infer remote repository state. |
| Codex suggested prompt should not be run | rejected assistant assumption | `retry_only_after_user_approval` | Prompt text, user correction, scope. | Keep assumption rejected or ask for explicit approval. | Do not turn caution into system law. |
| old tool login failure | failed tool behavior note | `historical_only_failure` or `retry_only_after_environment_change` | Tool name, auth error, observed time, session scope. | Recheck only under current credential scope. | Do not infer current login failure. |
| rejected assistant assumption | rejected assistant assumption | `blocked_until_review` | Assumption, correction, source or user instruction. | Retain rejected evidence. | Do not erase or broaden the rejection. |
| failed productization overreach | failed workflow path | `do_not_retry_candidate` | Overreach wording, boundary doc, task scope. | Return to docs-only candidate status. | Do not build MVP or product deployment. |
| stale external source recommendation | external source stale failure | `retry_only_with_new_evidence` | Source reference, missing/stale timestamp, wrong recommendation. | Fresh source review under separate scope. | Do not invent live facts. |

## 18. Candidate Future Sequence

Recommended docs-only sequence:

1. Explainable Recall Trace Template
2. Connector Governance Taxonomy
3. Memory Ontology Mapping
4. External Product Explanation Candidate
5. P4 Decision Gate Checklist

This document does not start any of them.

P4 remains paused.

P4 requires explicit human confirmation later.

Each future item must remain docs-only unless the human operator separately and explicitly scopes a different kind of work.

## 19. Prohibited Implementation Rules

Do not implement failed-attempt storage.

Do not implement do-not-retry enforcement.

Do not implement retry blocker logic.

Do not implement failure detector logic.

Do not implement automatic rule creation.

Do not implement automatic blocking.

Do not implement automatic retry prevention.

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

Do not treat failed-attempt memory as proof of impossibility.

Do not treat do-not-retry as automatic law.

Do not treat retry-risk confidence as approval.

Do not treat historical-only failure as useless.

Do not treat superseded failure as erased.

## 20. Stop Conditions

If failed-attempt rules turn into code, stop.

If failed-attempt rules turn into tests, stop.

If failed-attempt rules turn into failed-attempt storage, stop.

If failed-attempt rules turn into retry blocker logic, stop.

If failed-attempt rules turn into do-not-retry enforcement, stop.

If failed-attempt rules turn into failure detector logic, stop.

If failed-attempt rules turn into automatic rule creation, stop.

If failed-attempt rules turn into automatic blocking, stop.

If failed-attempt rules turn into lifecycle storage, stop.

If failed-attempt rules turn into state machine, stop.

If failed-attempt rules turn into transition engine, stop.

If failed-attempt rules turn into stale detector, stop.

If failed-attempt rules turn into expiration logic, stop.

If failed-attempt rules turn into temporal query engine, stop.

If failed-attempt rules turn into Memory Graph mutation, stop.

If failed-attempt rules turn into durable writer, stop.

If failed-attempt rules turn into dependency adoption, stop.

If failed-attempt rules turn into adapter work, stop.

If failed-attempt rules turn into MCP/API operation surface, stop.

If failed-attempt rules turn into authorization/execution semantics, stop.

If failed-attempt rules start P4, stop.

If failed-attempt rules start v7 implementation, stop.

If failed-attempt rules start MVP/product deployment, stop.

If failed-attempt rules start changing old docs, stop.

If `pyproject.toml` version changes, stop.

If `uv.lock` appears, stop.

If tag creation is suggested, stop.

## 21. Final Rules Statement

This document defines failed-attempt memory and do-not-retry rule candidates only.

It does not evaluate live memory.

It does not implement retry blocking.

It does not implement enforcement.

It does not authorize implementation.

`v6.16.0` remains sealed.

Future work must preserve boundary and require explicit human approval.
