# Civilization Core POST-IDG R6.1 Replacement Operator Evaluation Reauthorization Decision

## 1. Purpose

This document is the sole artifact of the documentation-only governance task
`POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_REAUTHORIZATION_DECISION`.
It records a bounded professional decision about whether and how a replacement
Human Operator evaluation may be prepared after the original Checkpoint B
attempt became an invalid measurement.

The selected design is a new, predeclared, onboarded experiment. It is not a
retry, repair, continuation, reconstruction, or reinterpretation of the
invalid attempt. The replacement asks whether governed structured review
improves human decision quality and safety detection without unacceptable
burden after the operator first receives a fixed, non-scored explanation of
the interface and review concepts.

This document creates no implementation, replacement corpus, session runner,
Evidence document, Human Operator observation, learning result, persistence,
proposal, execution, deployment, release, or successor work. While unmerged,
it creates no current implementation authority.

## 2. Controlling repository state

The controlling baseline is commit
`a536c49c6b11a85af3a0e07b94cc794f7b44d52b`, the merge of PR #369. The package
version remains locked at `6.16.0`.

At that baseline:

- R6.1 Checkpoint A is complete and repository-effective;
- the existing in-memory evaluation engine is
  `governed_memory_operator_evaluation`;
- its focused tests and original twelve-trial corpus are valid repository
  artifacts;
- the original corpus SHA-256 is
  `6b5bfaae62e4b0f36954b10a4fe1481ac44812e3f15a47616895b47218455591`;
- the original corpus is retired from any further scored Human Operator
  session because scored material from it was exposed; and
- implementation authority for new work is currently none.

This reauthorization preserves, rather than weakens or replaces, the existing
engine's in-memory, non-persisted, non-applied, fail-closed, no-promotion,
no-proposal, no-execution, no-model, and no-network boundaries.

## 3. Invalid original-session record

The original R6.1 Checkpoint B attempt has the terminal disposition
`INVALID-MEASUREMENT`. During that attempt:

1. the first scored candidate was displayed;
2. model assistance supplied a trial-specific recommendation and rationale;
3. the session was interrupted before completion;
4. no complete observation was recorded;
5. no observation was persisted;
6. no Evidence document was created; and
7. no commit, push, pull request, tag, version change, dependency change, or
   repository implementation change occurred.

Those facts are historical invalidation facts only. They are not Human
Operator evidence, a partial success, a scored result, an observation, a
learning gain, a burden finding, or a basis for any aggregate. The attempt
must never be completed retrospectively, imputed, reconstructed, converted to
a substantive result, or cited as usable learning evidence.

## 4. Root-cause assessment

The immediate invalidation had three jointly sufficient causes: scored
candidate exposure, trial-specific model assistance, and interruption. Once
the candidate and answer-oriented assistance had been presented, answer-key
independence and unassisted Human Operator judgment could no longer be
established. Interruption then prevented a complete, attestable observation
set.

The governance design also left an avoidable usability risk: the operator was
asked to work directly with engineering-oriented concepts and manually supply
instrumentation values without a fixed, non-scored onboarding phase. That
made outside explanation more likely and made burden measurements less
reliable. The corrective design therefore separates onboarding from scoring,
adds a deterministic plain-Chinese terminal interface, and instruments time,
actions, and rework automatically.

This is a measurement-procedure failure, not evidence that the existing
Checkpoint A engine, tests, or corpus artifacts are defective. The original
corpus is nevertheless unusable for another scored session because exposure
cannot be undone.

## 5. Reauthorization decision

Once this decision is repository-effective, authorize exactly the bounded
task:

`POST_IDG_R6_1_REPLACEMENT_ONBOARDED_OPERATOR_EVALUATION`

The task is authorized only through the exact write set, two checkpoints,
practice/scored design, interface contract, validation corridor, Evidence
rules, and prohibitions in this document.

The replacement experiment is a new measurement with a completely new scored
corpus. It is not a retry of the invalid session. No part of the invalid
attempt may populate, prefill, influence, or substitute for a replacement
observation.

## 6. Replacement experiment identity

The replacement retains exactly:

- two conditions: `UNGOVERNED-RAW-REVIEW` and
  `GOVERNED-STRUCTURED-REVIEW`;
- six matched scenario classes;
- six matched pairs;
- twelve scored trials;
- one Human Operator;
- one project, `civilization-core`; and
- the `SYNTHETIC` input classification.

It adds exactly four non-scored practice examples before the scored session
and a deterministic local terminal surface named
`governed_memory_operator_session`.

The learning question remains bounded to decision correctness, critical
safety/scope/promotion detection, rationale completeness, human burden, and
the already authorized PEX-02, PEX-05, and PEX-06 measurements. It does not
measure broad-user value, product-market fit, production readiness, or
generalizability.

This bounded design has no statistical significance and cannot support broad-user generalization.

## 7. Operator and data boundary

The complete operator and data boundary is:

- exactly one actual Human Operator;
- exactly one project: `civilization-core`;
- synthetic input only;
- local execution only;
- no network access;
- no external services;
- no model calls;
- no real personal, confidential, production, credential, customer, or
  third-party data;
- no observation persistence before valid final Evidence creation;
- no durable adoption;
- no real proposal creation, application, or authorization;
- no memory persistence, promotion, recall, correction, revocation, or
  deletion;
- no execution or continuation; and
- no substitution of tests, fixtures, Codex, a model, an assistant, a
  subagent, or another person for the Human Operator.

All runtime session state, practice progress, scored observations, event
records, timing values, condition scores, and attestations must remain in
memory until the complete valid session can be finalized.

## 8. Non-scored onboarding phase

The future interface must present exactly four
`NON-SCORED-PRACTICE` examples. Each example must use a synthetic candidate
that never appears in the replacement scored corpus or original scored
corpus. Taken together, the four examples must teach the four supported
outcomes in plain Chinese, with one example whose correct practice answer is
each of:

1. `approve_real_proposal_creation`;
2. `request_changes`;
3. `reject`; and
4. `defer`.

Before practice, the interface must explain in plain Chinese:

- project scope means that the candidate belongs to the one declared project;
- provenance means the declared origin and traceable basis of the candidate;
- risk means whether the candidate is within the supported risk boundary;
- governance means the declared controls and prohibited side effects;
- fail closed means stopping without action when required facts or boundaries
  are invalid or unavailable;
- no promotion means candidate content cannot promote itself into any later
  state;
- non-applied means a review result has not created, applied, persisted, or
  adopted memory; and
- `approve_real_proposal_creation` permits only a later, separately governed
  proposal-creation step and does not itself create, apply, persist, adopt, or
  authorize memory.

For each practice example, the operator must submit an outcome, reason/boundary
selection, and non-blank rationale before the interface reveals the fixed
correct practice answer and explanation. Feedback may appear only after that
submission and only for that practice example.

Practice interaction must collect no scored observation, enter no scored
event stream, contribute nothing to condition aggregates or the learning
decision, and create no Evidence record. A future valid Evidence document may
record only completion metadata for the four practice examples, clearly
labelled non-scored; it must not represent practice answers as scored trial
evidence.

## 9. Replacement scored-corpus design

The replacement corpus must contain exactly twelve newly written scored
candidates in six matched pairs and preserve these scenario classes and
counterbalanced condition positions:

| Sequence | Pair and class | Condition |
|---:|---|---|
| 1 | Pair 1, `VALID-LOW-RISK`, variant A | `UNGOVERNED-RAW-REVIEW` |
| 2 | Pair 1, `VALID-LOW-RISK`, variant B | `GOVERNED-STRUCTURED-REVIEW` |
| 3 | Pair 2, `PROJECT-SCOPE-MISMATCH`, variant A | `GOVERNED-STRUCTURED-REVIEW` |
| 4 | Pair 2, `PROJECT-SCOPE-MISMATCH`, variant B | `UNGOVERNED-RAW-REVIEW` |
| 5 | Pair 3, `UNSAFE-WRITE-GOVERNANCE`, variant A | `UNGOVERNED-RAW-REVIEW` |
| 6 | Pair 3, `UNSAFE-WRITE-GOVERNANCE`, variant B | `GOVERNED-STRUCTURED-REVIEW` |
| 7 | Pair 4, `UNSUPPORTED-HIGH-RISK`, variant A | `GOVERNED-STRUCTURED-REVIEW` |
| 8 | Pair 4, `UNSUPPORTED-HIGH-RISK`, variant B | `UNGOVERNED-RAW-REVIEW` |
| 9 | Pair 5, `MISSING-OR-INVALID-PROVENANCE`, variant A | `UNGOVERNED-RAW-REVIEW` |
| 10 | Pair 5, `MISSING-OR-INVALID-PROVENANCE`, variant B | `GOVERNED-STRUCTURED-REVIEW` |
| 11 | Pair 6, `CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION`, variant A | `GOVERNED-STRUCTURED-REVIEW` |
| 12 | Pair 6, `CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION`, variant B | `UNGOVERNED-RAW-REVIEW` |

The pair variants must be semantically matched for class and intended
difficulty while using distinct candidate contents. The replacement must use:

- twelve entirely new candidate contents;
- twelve entirely new candidate IDs;
- twelve entirely new source IDs;
- twelve entirely new fixture IDs;
- twelve unique canonical candidate SHA-256 digests;
- zero canonical candidate-digest overlap with the original corpus; and
- no exact candidate repetition within the replacement corpus.

Canonical digest serialization must reuse the existing engine's deterministic
candidate canonicalization rather than introduce a weaker comparison. The
future tests must compute all original-corpus candidate digests and all
replacement-corpus candidate digests and prove that the two sets are
disjoint.

The replacement corpus file and its SHA-256 must be locked before a scored
session starts. No scored candidate may be displayed to the operator or any
answering assistant before the one valid replacement session begins. Corpus,
condition order, metric definitions, event definitions, hidden scoring
fields, and scoring rules may not change after session start.

The existing in-memory evaluation engine must be reused without modifying or
weakening its boundaries. The new session runner may adapt deterministic
plain-language selections into the engine's exact existing machine values,
but must not change the engine or its scoring semantics.

## 10. Plain-language interface contract

The only authorized new runtime surface is the deterministic local terminal
interface `governed_memory_operator_session`. It must:

- display concise Chinese explanations instead of requiring the operator to
  interpret raw engineering-only labels;
- preserve and display the exact underlying candidate and authorized packet
  data without semantic rewriting;
- display every outcome with a Chinese label and its exact machine value;
- make the same fixed glossary available before practice, during practice,
  before scoring, and during every scored trial;
- never recommend an answer or rationale for a scored trial;
- never reveal scenario class, expected outcome, expected reason code,
  correctness, hidden scoring data, pair answer key, condition aggregate, or
  learning result during the scored session;
- allow review and edits only within the current unlocked trial;
- show a complete final confirmation screen containing the current candidate
  identity, outcome, reason/boundary selections, and rationale before lock;
- require an explicit lock confirmation distinct from ordinary input;
- detect when rationale input is blank or merely duplicates an outcome option
  label or machine value, warn the operator, and require deliberate rationale
  re-entry and confirmation rather than silently accepting it;
- permit correction within the current trial without invalidating the whole
  session;
- prohibit navigation back to any previously locked trial; and
- retain all observations only in memory until twelve trials, two condition
  score sets, and final attestations are complete.

The interface must use deterministic prompts, validation, transitions, and
mapping tables. Terminal rendering may improve comprehension but must not add,
omit, summarize, infer, or alter candidate facts.

## 11. Outcome and glossary semantics

The fixed outcome display must use exactly these mappings:

| Chinese label | Exact machine value | Plain-language meaning |
|---|---|---|
| 允许后续创建真实提案步骤 | `approve_real_proposal_creation` | 仅允许以后进入另一个受治理的提案创建步骤；当前不创建、不应用、不持久化、不采纳记忆 |
| 要求修改 | `request_changes` | 当前材料或边界需要修改；当前不继续、不应用 |
| 拒绝 | `reject` | 当前候选不被接受；当前不继续、不应用 |
| 暂缓 | `defer` | 当前信息、风险或条件不足；保持关闭并等待另行授权 |

The fixed glossary must explain the selectable reason and consequence concepts
in plain Chinese and map them deterministically to these existing exact reason
codes:

| Plain-language concept | Existing machine code |
|---|---|
| 只陈述了结果，尚未指出依据 | `OUTCOME_ONLY` |
| 候选满足本次低风险接纳边界 | `VALID_ACCEPTANCE` |
| 项目范围一致性边界 | `SCOPE_BOUNDARY` |
| 治理与禁止写入边界 | `GOVERNANCE_BOUNDARY` |
| 支持的风险等级边界 | `RISK_BOUNDARY` |
| 来源与可追溯依据边界 | `PROVENANCE_BOUNDARY` |
| 候选内容不能推动状态或调用工具 | `PROMOTION_BOUNDARY` |
| 已解释为何事实或边界支持所选结果 | `EXPLAINS_OUTCOME` |
| 结果保持未应用 | `NON_APPLIED_CONSEQUENCE` |
| 信息或边界不满足时保持关闭 | `FAIL_CLOSED_CONSEQUENCE` |
| 不发生状态提升 | `NO_PROMOTION_CONSEQUENCE` |
| 认为候选已获提升授权的误解声明 | `PROMOTION_AUTHORIZED_MISUNDERSTANDING` |

The glossary is generic and immutable for the session. It must contain no
candidate-specific example, scenario hint, expected answer, preferred option,
trial diagnosis, or trial-specific rationale. Plain-language selection must
not remove the operator's responsibility to choose the outcome, reasoning
boundary, consequence, and rationale.

## 12. Human-input and instrumentation contract

For every scored trial, the actual operator must explicitly provide:

- one supported outcome;
- a non-blank rationale that is not silently accepted from an option label;
- plain-language reason/boundary and consequence selections that map
  deterministically to existing reason codes.

After the six trials in each condition, the operator must explicitly provide:

- perceived usefulness as an integer from 1 through 5; and
- perceived governance burden as an integer from 1 through 5.

After all twelve trials and both condition score sets, the operator must
explicitly attest that no scored answer key was viewed and no outside
trial-specific assistance was used. The attestations may not be defaulted,
inferred, preselected, or supplied by another actor.

The operator must not manually type elapsed milliseconds, action count, or
correction/rework count. The interface must instrument those values
automatically and deterministically.

### 12.1 Human time

Per-trial human time starts when the complete scored packet is first rendered
and available for operator input. It ends only when the final trial-lock
confirmation is accepted. It includes glossary viewing, review, validation
messages, edits, and confirmation within that trial. A monotonic clock must be
used. Human time must be stored in milliseconds separately from every system
runtime or latency measurement; system execution time must never be added to,
subtracted from, substituted for, or presented as human time.

### 12.2 Exact action-count event types

For scored trials only, one operator action is counted for each accepted
interface transition of exactly one of these event types:

1. `GLOSSARY_OPENED`;
2. `GLOSSARY_CLOSED`;
3. `OUTCOME_SUBMITTED`;
4. `REASON_BOUNDARIES_SUBMITTED`;
5. `RATIONALE_SUBMITTED`;
6. `REVIEW_REQUESTED`;
7. `OUTCOME_EDITED`;
8. `REASON_BOUNDARIES_EDITED`;
9. `RATIONALE_EDITED`;
10. `LOCK_CONFIRMATION_DECLINED`; and
11. `TRIAL_LOCK_CONFIRMED`.

Each occurrence counts as one. Keystrokes, terminal rendering, system calls,
clock reads, hidden scoring, rejected malformed input that causes no accepted
state transition, practice actions, and condition-score or final-attestation
inputs do not enter a trial's operator action count. The future implementation
must preserve the raw ordered action-event list so that every reported count
equals the number of listed events.

### 12.3 Exact correction/rework event types

For scored trials only, one correction/rework is counted for each occurrence
of exactly one of these event types:

1. `OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION`;
2. `REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION`;
3. `RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION`; and
4. `LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW`.

A changed value must differ from the last accepted value. Same-value
resubmission, glossary use, initial entry, review display, rejected malformed
input, and system-side validation do not count as rework. A declined lock
counts once each time the operator returns from final confirmation to edit or
review the current trial. The raw ordered rework-event list must be retained
in memory, and the reported rework count must equal its length.

No model scoring, semantic prose grading, inferred Human Operator judgment,
inferred selection, fabricated value, or synthetic substitute is authorized.
Correctness and rationale completeness may be calculated only by the existing
deterministic exact-value and reason-code rules after the session is complete.

### 12.4 Exact rationale and aggregate rules

The existing deterministic rationale-completeness rubric remains:

- 0: blank, unrelated, or no usable reason;
- 1: states an outcome but identifies no material evidence or boundary;
- 2: identifies one relevant fact or boundary;
- 3: identifies the relevant fact or boundary and explains why it supports the
  selected outcome; and
- 4: satisfies score 3 and explicitly preserves the relevant non-applied,
  no-promotion, or fail-closed consequence.

The score must be derived only from explicit reason-code selections. Prose
style, writing quality, semantic similarity, and unstated inferred intent are
not scoring inputs.

For each condition, finalization must report:

- correct outcomes out of six;
- critical unsafe/scope/promotion detections out of five;
- state-promotion misunderstandings;
- median rationale completeness;
- median human completion time;
- median operator action count;
- total correction/rework count;
- perceived usefulness; and
- perceived governance burden.

### 12.5 Exact learning-decision and PEX rules

`LEARNING-SUPPORTS-CONTINUED-GOVERNED-EVALUATION` is permitted only when all
of these are true:

- governed correctness is at least baseline correctness;
- governed correctness is at least five of six;
- governed critical detection is five of five;
- governed state-promotion misunderstandings are zero;
- governed median rationale completeness is at least baseline;
- governed total correction/rework is no greater than baseline;
- governed median human completion time is no greater than 150 percent of
  baseline;
- governed median action count is no more than two actions above baseline;
- governed perceived usefulness is at least four of five; and
- governed perceived governance burden is at most three of five.

`LEARNING-GAIN-WITH-BURDEN-HOLD` applies only when governed safety or decision
quality improves but at least one burden, time, action, correction, usefulness,
or burden-score threshold fails. `NO-SUPPORT-FOR-EXPANSION` applies when
governed safety and decision quality do not improve and governed burden is
equal or worse. `INVALID-MEASUREMENT` applies whenever any invalidation rule in
section 14 is met. No invalid measurement may be converted to one of the three
substantive decisions.

PEX-02 measures only governed candidate, review, and decision system time,
excluding human time; it reports sample size and calculation method and has a
P95 target no greater than 2,000 ms. PEX-05 measures only system time from
detection to visible held/fail-closed status, excluding human acknowledgement
and resolution time; reasons remain visible, authorize no action, and the P95
target is no greater than 1,000 ms. PEX-06 remains exactly 100 sequential
bounded engine operations and requires no unexpected repository or storage
mutation, unauthorized authority transition, crash, unhandled exception, or
silent loss of status/audit result. PEX-06 is bounded stability evidence, not
production reliability.

## 13. Assistance boundary

The scored session must be answer-key-free and independently completed by the
one Human Operator. During scoring:

- no trial-specific recommendation, diagnosis, suggested outcome, suggested
  reason code, or suggested rationale is permitted;
- no model, Codex, assistant, subagent, external person, external service, or
  hidden answer material may choose or shape an answer;
- the operator may use only the exact candidate/packet display, deterministic
  interface prompts, and fixed glossary;
- generic interface mechanics may be explained only by the predeclared fixed
  interface text, never by live trial-specific help; and
- any outside trial-specific assistance makes the complete session invalid.

The interface must fail closed if the operator cannot affirm both final
attestations. It must not attempt to judge whether an attestation is truthful;
it must preserve the explicit human statement and apply the deterministic
invalidation rule.

## 14. Invalidation rules

The interface must create no partial Evidence. The complete attempt must
produce `INVALID-MEASUREMENT` and no Evidence document if any of these occurs:

- any scored trial is missing;
- the locked trial order is violated;
- a candidate is repeated;
- the original corpus is used for scoring;
- any scored candidate was exposed before the valid replacement session;
- outside trial-specific assistance is used;
- Human Operator observations are fabricated, inferred, substituted, or
  supplied by a non-operator;
- human time and system time are conflated;
- hidden answer material is exposed;
- corpus content or digest, conditions, metrics, action-event definitions,
  rework-event definitions, hidden scoring fields, or scoring rules change
  after session start;
- required raw observations, action events, rework events, or timing records
  are unavailable;
- an outcome, non-blank confirmed rationale, reason/boundary selection,
  condition score, or final attestation is missing;
- the session is interrupted before all observations, scores, and final
  attestations are complete; or
- any other fail-closed corpus or observation invariant in the existing engine
  is violated.

Invalid state must remain in memory only and must not create an Evidence file.
A failed or interrupted attempt may not be silently restarted with the same
replacement scored corpus. Any further replacement requires another explicit,
repository-effective governance decision and another completely new scored
corpus.

## 15. Exact future write set

Once this decision is repository-effective, the replacement task may create
exactly these four future files:

1. `src/hermes_memory_fabric/governed_memory_operator_session.py`
2. `tests/test_governed_memory_operator_session.py`
3. `docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json`
4. `docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md`

No fifth future file is authorized. In particular, these existing files must
remain byte-for-byte unchanged:

- `src/hermes_memory_fabric/governed_memory_operator_evaluation.py`;
- `tests/test_governed_memory_operator_evaluation.py`; and
- `docs/CIVILIZATION_CORE_POST_IDG_R6_1_OPERATOR_EVALUATION_SCENARIO_CORPUS.json`.

## 16. Replacement Checkpoint A

Replacement Checkpoint A is
`HARNESS-AND-NEW-CORPUS-READINESS`. It may create only future files 1, 2, and
3. It must:

- implement the deterministic local terminal interface;
- define and validate exactly four non-scored practice examples;
- validate exactly twelve new scored candidates and six pairs;
- lock the replacement corpus and SHA-256;
- prove that all candidate IDs, source IDs, and fixture IDs are new;
- prove that replacement canonical candidate digests are unique and have zero
  overlap with original-corpus candidate digests;
- prove that scored operator packets and the glossary expose no hidden answer
  fields or trial-specific answer hints;
- prove the exact Chinese-label-to-machine-value mappings;
- prove edit-before-lock, rationale confirmation, and no-return-after-lock
  behavior;
- prove automatic human timing and exact action/rework event instrumentation;
- prove human/system time separation;
- prove that interruption or incomplete input creates no Evidence;
- prove no runtime state file, persistence, adoption, real proposal, execution,
  network, model, external service, or continuation;
- preserve compatibility with the existing engine's correctness, detection,
  rationale, aggregate, learning-decision, PEX-02, PEX-05, and PEX-06
  behavior; and
- stop with future file 4 absent.

Checkpoint A is a mandatory stop. Harness readiness is not a Human Operator
observation or learning result, and it does not authorize Checkpoint B until
Checkpoint A is repository-effective.

## 17. Replacement Checkpoint B

Replacement Checkpoint B is
`ACTUAL-HUMAN-OPERATOR-SESSION`. It may start only after Replacement
Checkpoint A is repository-effective and its locked corpus remains unchanged.
It requires the actual one Human Operator and may create only future file 4,
the replacement Evidence document.

The Evidence document may be created only after:

- all four practice examples are completed under the non-scored rules;
- all twelve scored trials are completed and locked in exact order;
- both condition usefulness and burden scores are supplied;
- all raw observation, action, rework, human-time, and system-time records are
  available;
- both final attestations are explicitly affirmed;
- all invalidation checks pass; and
- deterministic finalization succeeds.

If any condition is not met, Checkpoint B ends as an invalid measurement with
no Evidence document. It may not create a placeholder, partial, draft, or
failure Evidence file.

## 18. Future focused-test requirements

The new focused tests must cover at least:

1. the exact `governed_memory_operator_session` local-session surface;
2. exactly four practice examples;
3. one practice example for each exact supported outcome;
4. practice feedback only after practice-answer submission;
5. practice examples and events excluded from scored observations, metrics,
   aggregates, and learning decisions;
6. exactly twelve scored trials and six matched pairs;
7. the exact counterbalanced order in section 9;
8. entirely new candidate content, candidate IDs, source IDs, and fixture IDs;
9. unique replacement candidate digests and zero overlap with every original
   corpus candidate digest;
10. Chinese outcome labels mapping to exact machine outcomes;
11. plain-language reason selections mapping to exact existing reason codes;
12. a fixed glossary containing no trial-specific answer;
13. no scenario class, expected fields, correctness, scoring data, pair answer
    key, aggregate, or result in scored displays;
14. exact candidate and packet data preserved by rendering;
15. current-trial editing before lock;
16. blank and option-label-only rationale rejection and explicit rationale
    confirmation;
17. final confirmation before lock;
18. no return to a locked trial;
19. automatic monotonic human-time measurement from packet display through
    lock;
20. all and only the exact action event types in section 12.2 counted;
21. all and only the exact rework event types in section 12.3 counted;
22. raw event-list lengths exactly matching reported counts;
23. human and system time kept separate;
24. interruption producing no Evidence;
25. explicit no-answer-key and no-outside-assistance attestations required;
26. incomplete sessions unable to finalize;
27. original corpus, changed corpus, repeated candidate, exposed candidate,
    wrong order, missing raw record, and changed-rule cases failing closed;
28. existing correctness and critical-detection behavior remaining compatible;
29. existing project-scope, unsafe-input, promotion-misunderstanding, and
    rationale-completeness behavior remaining compatible;
30. existing condition aggregates and all learning-decision rules remaining
    compatible;
31. PEX-02, PEX-05, and exact 100-operation PEX-06 behavior remaining
    compatible;
32. no caller-input mutation and deterministic output;
33. no runtime state files or observation persistence;
34. no promotion;
35. no proposal creation or application;
36. no execution or continuation;
37. no network, connector, external service, model, Codex, or assistant use;
    and
38. no existing-file modification.

Synthetic observations may appear only as explicitly labelled test fixtures
for deterministic behavior. They must never be presented as an actual Human
Operator session or copied into Evidence.

## 19. Future validation corridor

Replacement Checkpoint A must use the narrowest relevant validation first and
then the inherited compatibility corridor:

1. syntax validation of only the new runner and new focused test;
2. the new focused test;
3. the existing operator-evaluation focused test;
4. the existing R6.0 focused and compatibility suites;
5. the inherited Evidence compatibility suite; and
6. a fresh temporary local environment proving deterministic corpus/packet
   behavior, original-corpus non-overlap, no hidden answer display, fail-closed
   interruption, no caller-input mutation, and no runtime files or side
   effects.

Validation must run locally with network and model access absent. It must
verify that the three authorized Checkpoint A files are the only changes and
that the replacement Evidence file is absent. Checkpoint A validation may use
synthetic fixtures but may not start, simulate as real, or claim an actual
Human Operator session.

Before Checkpoint B, repository state must be checked against the
repository-effective Checkpoint A commit and locked hashes. After a complete
session, deterministic finalization and all invalidation checks must pass
before the sole Evidence write. No validation result can cure contamination,
missing observation data, or an interrupted session.

## 20. Replacement Evidence requirements

Only a valid Replacement Checkpoint B may create the replacement Evidence
document. It must record:

- the invalid original-session disposition as historical context only, with no
  learning value attributed to it;
- this repository-effective reauthorization decision's SHA-256;
- the locked replacement corpus SHA-256;
- the original corpus SHA-256 used only for canonical candidate non-overlap
  proof;
- the session runner SHA-256;
- the session focused-test SHA-256;
- four practice-example completion records clearly marked non-scored;
- exact twelve scored trial records;
- exact counterbalanced condition order;
- raw explicit Human Operator observations;
- raw ordered interface action events and exact counts;
- raw ordered correction/rework events and exact counts;
- raw human timing;
- raw system timing recorded separately;
- condition aggregates;
- every threshold evaluation;
- the exact deterministic learning decision;
- PEX-02, PEX-05, and PEX-06 dispositions;
- every invalidation check and its pass state;
- the final no-answer-key and no-outside-assistance attestations;
- interpretation limits for one operator, one project, one fixed synthetic
  corpus, and one completed session;
- changes, if any, to MU-02, MU-03, MU-09, MU-11, PST-05, and PST-06;
- all twenty-two material unknowns, with zero silently resolved; and
- an explicit statement that no automatic successor authority was created.

The Evidence must make no broad-user, product-market-fit, production,
persistence, security, privacy, IAM, lifecycle, deployment, release, or
successor-authority claim. It must not treat a practice answer, test fixture,
invalid original-session event, or inferred value as a scored observation.

## 21. Prohibitions

Neither this decision nor the future replacement task authorizes:

- modification of the existing engine, its test, or the original corpus;
- a fifth file or any runtime state, cache, database, log, token, configuration,
  `.codex`, `AGENTS.md`, `AGENTS.override.md`, or `uv.lock` file;
- dependency, package-version, build-system, tag, release, or deployment
  changes;
- network access, APIs, MCP, connectors, external services, models, agents, or
  model-based scoring;
- actual or inferred personal, confidential, production, credential, customer,
  or third-party data;
- fabricated, substituted, reconstructed, or semantically graded Human
  Operator observations;
- partial Evidence or Evidence from an invalid attempt;
- reuse of either the original scored corpus or a failed replacement scored
  corpus;
- persistence, adoption, promotion, real proposal creation/application,
  execution, or continuation;
- conversion of the invalid original attempt into success or substantive
  learning; or
- automatic implementation, Checkpoint B, successor work, commit, push, pull
  request, merge, tag, or release.

## 22. Authority semantics

This documentation task is complete only as an unmerged decision artifact and
creates no present implementation authority. Repository effectiveness requires
the normal separately governed merge process; this document does not perform
or authorize that merge.

Once repository-effective, authority becomes bounded only to:

- the exact replacement task named in section 5;
- the exact four-file future write set in section 15;
- the exact two-checkpoint protocol in sections 16 and 17;
- the exact four-example practice and twelve-trial scored design;
- the exact local terminal interface and instrumentation contract;
- the existing engine reused without modification; and
- every prohibition, invalidation rule, test requirement, and validation gate
  in this document.

Authority does not transfer to another operator, project, corpus, session,
surface, file, service, model, lifecycle operation, deployment, release, or
successor task. Checkpoint A is the next allowed task only after repository
effectiveness. Checkpoint B is not automatic. No work follows automatically
from any learning decision.

## 23. Machine-readable reauthorization state

```text
TASK_ID=POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_REAUTHORIZATION_DECISION
BASE_COMMIT=a536c49c6b11a85af3a0e07b94cc794f7b44d52b
ALLOWED_WRITE_FILE_COUNT=1

R6_1_CHECKPOINT_A_STATUS=COMPLETE
R6_1_CHECKPOINT_A_REPOSITORY_EFFECTIVE=TRUE

R6_1_ORIGINAL_CHECKPOINT_B_STATUS=INVALID-MEASUREMENT
R6_1_ORIGINAL_CHECKPOINT_B_REPOSITORY_EFFECTIVE=FALSE
R6_1_ORIGINAL_EVIDENCE_STATUS=NOT-CREATED
R6_1_ORIGINAL_HUMAN_OBSERVATIONS_PERSISTED=FALSE
R6_1_ORIGINAL_RESULT_CONVERTED_TO_SUCCESS=FALSE

INVALIDATION_REASON_COUNT=3
INVALIDATION_REASONS=FIRST_SCORED_CANDIDATE_EXPOSED,TRIAL_SPECIFIC_MODEL_ASSISTANCE,SESSION_INTERRUPTED

REPLACEMENT_REAUTHORIZATION_DECISION=AUTHORIZE
AUTHORIZED_REPLACEMENT_TASK=POST_IDG_R6_1_REPLACEMENT_ONBOARDED_OPERATOR_EVALUATION
AUTHORIZED_RUNTIME_SURFACE=governed_memory_operator_session

REPLACEMENT_PRACTICE_EXAMPLE_COUNT=4
REPLACEMENT_SCORED_TRIAL_COUNT=12
REPLACEMENT_PAIR_COUNT=6
REPLACEMENT_CONDITION_COUNT=2
REPLACEMENT_PROJECT_COUNT=1
REPLACEMENT_OPERATOR_COUNT=1
REPLACEMENT_INPUT_CLASSIFICATION=SYNTHETIC

REPLACEMENT_CORPUS_MUST_BE_NEW=TRUE
ORIGINAL_CORPUS_REUSE_FOR_SCORED_SESSION=PROHIBITED
ORIGINAL_CANDIDATE_DIGEST_OVERLAP_ALLOWED=FALSE

PRACTICE_PHASE_SCORED=FALSE
PRACTICE_PHASE_CORRECT_ANSWER_FEEDBACK=AFTER-PRACTICE-ANSWER-ONLY
SCORED_SESSION_TRIAL_SPECIFIC_ASSISTANCE=PROHIBITED
SCORED_SESSION_MODEL_ASSISTANCE=PROHIBITED
SCORED_SESSION_FIXED_GLOSSARY=AUTHORIZED

HUMAN_TIME_INSTRUMENTATION=AUTOMATIC-DETERMINISTIC
OPERATOR_ACTION_COUNT_INSTRUMENTATION=AUTOMATIC-DETERMINISTIC
CORRECTION_REWORK_COUNT_INSTRUMENTATION=AUTOMATIC-DETERMINISTIC
MODEL_SCORING_AUTHORIZED=FALSE
HUMAN_OBSERVATION_FABRICATION_AUTHORIZED=FALSE

AUTHORIZED_REPLACEMENT_WRITE_FILE_COUNT=4
AUTHORIZED_REPLACEMENT_WRITE_FILE_1=src/hermes_memory_fabric/governed_memory_operator_session.py
AUTHORIZED_REPLACEMENT_WRITE_FILE_2=tests/test_governed_memory_operator_session.py
AUTHORIZED_REPLACEMENT_WRITE_FILE_3=docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json
AUTHORIZED_REPLACEMENT_WRITE_FILE_4=docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md

EXISTING_OPERATOR_EVALUATION_ENGINE_MODIFICATION_AUTHORIZED=FALSE
EXISTING_OPERATOR_EVALUATION_TEST_MODIFICATION_AUTHORIZED=FALSE
ORIGINAL_OPERATOR_EVALUATION_CORPUS_MODIFICATION_AUTHORIZED=FALSE

REPLACEMENT_CHECKPOINT_COUNT=2
REPLACEMENT_CHECKPOINT_A=HARNESS-AND-NEW-CORPUS-READINESS
REPLACEMENT_CHECKPOINT_B=ACTUAL-HUMAN-OPERATOR-SESSION

DURABLE_ADOPTION_AUTHORITY=NONE
PERSISTENT_STORAGE_AUTHORITY=NONE
REAL_PROPOSAL_AUTHORITY=NONE
EXECUTION_AUTHORITY=NONE
CONTINUATION_AUTHORITY=NONE
EXTERNAL_SERVICE_AUTHORITY=NONE
DEPLOYMENT_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE

R6_1_REPLACEMENT_REAUTHORIZATION_STATUS=COMPLETE-UNMERGED
R6_1_REPLACEMENT_REAUTHORIZATION_REPOSITORY_EFFECTIVE=FALSE

CURRENT_IMPLEMENTATION_AUTHORITY_FOR_NEW_WORK=NONE
ON_REPOSITORY_EFFECTIVENESS_IMPLEMENTATION_AUTHORITY=BOUNDED
ON_REPOSITORY_EFFECTIVENESS_IMPLEMENTATION_AUTHORITY_SCOPE=EXACT-R6_1-REPLACEMENT-TASK-ONLY

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_CHECKPOINT_A
```

The reauthorization decision is complete and unmerged. It creates no present
implementation authority and does not start the replacement implementation or
Human Operator session.
