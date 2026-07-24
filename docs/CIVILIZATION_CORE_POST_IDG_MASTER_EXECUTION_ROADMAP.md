# Civilization Core Post-IDG Master Execution Roadmap

## 1. Status, Purpose, and Authority Boundary / 状态、目的与权限边界

This document is the controlling post-IDG execution-planning route. It coordinates future Human Owner decisions by defining the stage sequence, entry checks, closeout comparisons, and drift controls that must govern later repository tasks.

This route is navigation and planning control, not implementation authority. It does not alter the repository-established IDG outcome: IDG.4 remains `DEFER`; implementation readiness remains `NOT-ESTABLISHED`; implementation does not start; product implementation remains `NOT-AUTHORIZED`; and every execution authority remains `NONE`, including implementation, deployment, launch, release, version, and tag authority.

The package version remains `6.16.0`. V6 continuation remains `NEVER`. V7 runtime implementation remains `DEFER`. Automatic successor work remains `NONE`.

The stage route below is newly adopted by Human Owner planning direction. It organizes possible future decisions without converting any possible stage into approved work.

## 2. Repository-Effective Baseline / 仓库生效基线

The repository-effective baseline for adoption is commit `4fe763f74cb8e4ab22cac122f8ab0a5b37dc8715`, with package version `6.16.0`.

At that baseline, the repository records:

- the completed R0 governance/design state, including the Stable Kernel and closed V6 design-governance arc;
- a completed documentary IDG.0 through IDG.4 chain: IDG.0 entry review, IDG.1 evidence package, IDG.2 V7 documentary designation, IDG.3 independent readiness review, and IDG.4 Human Owner decision;
- the final IDG.4 outcome `DEFER` / `IMPLEMENTATION-DECISION-DEFERRED-NO-AUTHORIZATION`;
- GOV-MAINT-03 closed after its known defects were reconciled;
- GOV-MAINT-04 complete with no new concrete maintenance defect found; and
- GOV-MAINT-05 cancelled, not completed work and never to be represented as completed work.

These are repository-established governance and documentary facts. They do not establish that the entire Civilization Core product is complete, implemented, operational, secure, deployed, launched, or released.

## 3. Master Stage Map / 主阶段图

The following ordered map is the newly adopted planning route. A stage name describes a controlled decision or execution position; it does not itself grant authority.

### R0 — Stable Kernel and Governance Design Closure

- **Purpose:** Preserve the closed V6 Stable Kernel and completed governance/design foundation.
- **Entry conditions:** Historical V1–V6 work and terminal closure are repository-effective.
- **Required deliverables:** Stable Kernel seal, boundary governance, terminal roadmap, productization framing, and the completed IDG.0–IDG.4 documentary chain.
- **Exit criteria:** The design/governance state is traceable, V6 is closed, and IDG.4 records `DEFER` with no authorization.
- **Prohibited jumps or interpretations:** Do not equate design closure with product completion, runtime implementation, readiness, release, or a V6 successor.
- **Status at roadmap adoption:** `COMPLETE`.

### R1 — Post-IDG Master Roadmap Adoption

- **Purpose:** Adopt one controlling route for future stage selection, checkpointing, and closeout comparison.
- **Entry conditions:** R0 is complete; IDG.4 is repository-effective as `DEFER`; the Human Owner has directed adoption of a fixed post-IDG route.
- **Required deliverables:** This master roadmap, its ordered stage map, checkpoint protocol, closeout protocol, and drift rules.
- **Exit criteria:** This roadmap is merged without changing code, version, tags, or execution authority.
- **Prohibited jumps or interpretations:** Adoption does not start R2, authorize implementation, or create automatic successor work.
- **Status at roadmap adoption:** `COMPLETE-UPON-MERGE`.

### R2 — Product Direction and MVP Decision

- **Purpose:** Select, by a separate Human Owner decision, a primary product direction and a bounded MVP hypothesis.
- **Entry conditions:** R1 is merged; a pre-task roadmap checkpoint is on-route; a bounded R2 task is separately selected.
- **Required deliverables:** Target user and problem, core workflows, MVP scope and non-goals, success metrics, boundaries, and validation plan.
- **Exit criteria:** A Human Owner decision records selection, deferral, or rejection with all required R2 fields and no implied implementation authority.
- **Prohibited jumps or interpretations:** Do not treat recommendations, productization documents, UI names, or MVP scope as selected before that decision; do not start R3 or implementation automatically.
- **Status at roadmap adoption:** `NOT-STARTED` and `NEXT`.

### R3 — Pre-Implementation Evidence and Readiness Establishment

- **Purpose:** Produce the substantive evidence required to determine whether implementation readiness can be established for the selected R2 direction.
- **Entry conditions:** R2 has an affirmative, bounded Human Owner product/MVP decision; R3 evidence scope and authorities are separately approved.
- **Required deliverables:** Product, technical-feasibility, operating-model, security/privacy, and any concretely necessary external-dependency evidence, with criteria and provenance.
- **Exit criteria:** The bounded evidence set is complete enough for independent R4 reassessment, with gaps and limitations explicit.
- **Prohibited jumps or interpretations:** Documentation volume alone is not evidence sufficiency; no prototype, test, research, or external work occurs without its bounded authority; R3 does not authorize implementation.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R4 — Implementation Readiness Reassessment and Human Owner Decision

- **Purpose:** Independently reassess the R3 evidence and record a Human Owner readiness disposition.
- **Entry conditions:** R3 exit criteria are met and its evidence package is fixed, traceable, and reviewable.
- **Required deliverables:** Independent reassessment, gap statement, disposition rationale, and Human Owner outcome of `READY`, `DEFER`, or `REJECT`.
- **Exit criteria:** One allowed outcome is recorded; only `READY` may make a separate bounded implementation decision eligible for consideration.
- **Prohibited jumps or interpretations:** `READY` is not implementation authorization; `DEFER` and `REJECT` cannot enter R5; documentary review cannot manufacture readiness.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R5 — Bounded Implementation Authorization

- **Purpose:** Decide whether to authorize a precisely bounded implementation scope.
- **Entry conditions:** R4 records `READY`; a separate Human Owner implementation-decision task is selected; scope, owners, controls, stop conditions, and rollback boundaries are explicit.
- **Required deliverables:** Written bounded authorization or denial, authorized scope, forbidden scope, acceptance criteria, evidence obligations, and revocation/stop conditions.
- **Exit criteria:** An explicit Human Owner authorization exists for a bounded R6 slice, or the route stops without implementation.
- **Prohibited jumps or interpretations:** R4 `READY`, roadmap adoption, or a merged document cannot imply authorization; no broad product, deployment, release, version, or tag authority follows.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R6 — Core Runtime Vertical Slice

- **Purpose:** Implement and verify the smallest authorized end-to-end core runtime capability.
- **Entry conditions:** R5 explicitly authorizes the slice; acceptance, test, safety, evidence, and rollback requirements are fixed.
- **Required deliverables:** The bounded working slice, tests, implementation evidence, known limitations, and closeout comparison.
- **Exit criteria:** Authorized acceptance criteria pass and no unapproved scope is included; failures or gaps are disclosed.
- **Prohibited jumps or interpretations:** A vertical slice is not a complete product, production readiness, deployment permission, or release authority; scope may not expand by convenience.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R7 — Integration and Product Operation Surfaces

- **Purpose:** Add only the authorized integrations and operator-facing surfaces required to operate the R6 capability as the bounded product direction.
- **Entry conditions:** R6 closes successfully; concrete integration and product-operation needs are evidenced and separately authorized.
- **Required deliverables:** Authorized integration surfaces, operator workflows, permission behavior, operational controls, tests, and evidence.
- **Exit criteria:** Required bounded surfaces work together under explicit controls and meet their acceptance criteria.
- **Prohibited jumps or interpretations:** Do not infer additional APIs, dependencies, platforms, autonomous operations, deployment, security completion, or release readiness.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R8 — SEC-GOV Security Governance

- **Purpose:** Apply security, privacy, threat, abuse, permission, and governance assessment to the concrete authorized implementation.
- **Entry conditions:** A concrete authorized R6/R7 implementation exists with stable enough boundaries for assessment; SEC-GOV scope is separately authorized.
- **Required deliverables:** Threat and privacy analysis, control evidence, findings, remediation dispositions, residual-risk statement, and Human Owner security-governance decision.
- **Exit criteria:** Required controls and remediation criteria pass, residual risks are explicit, and the Human Owner records the bounded disposition.
- **Prohibited jumps or interpretations:** SEC-GOV does not start before a concrete authorized implementation exists; paperwork is not security proof; security review is not deployment or release authority.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R9 — System Validation and Pilot Readiness

- **Purpose:** Validate the integrated system against product, technical, operational, security, privacy, and governance criteria and decide pilot readiness.
- **Entry conditions:** R7 integration closes and R8 security-governance criteria are satisfied for the bounded system.
- **Required deliverables:** System validation results, failure and recovery evidence, operational runbooks, pilot criteria, limitations, and readiness decision.
- **Exit criteria:** A bounded pilot-readiness decision is supported by passing criteria and explicit residual risks.
- **Prohibited jumps or interpretations:** Validation does not imply real-world pilot permission, production deployment, launch, release, or general safety.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R10 — MVP Real-World Pilot

- **Purpose:** Run an explicitly authorized, bounded real-world MVP pilot to test user value and operating safety.
- **Entry conditions:** R9 records pilot readiness; participants, data, permissions, safeguards, metrics, support, stop conditions, and pilot authority are explicit.
- **Required deliverables:** Pilot plan, consent/permission records where applicable, observed metrics, incidents and responses, user evidence, and pilot closeout.
- **Exit criteria:** Pilot outcomes and safety/operational evidence are complete enough for an R11 decision, with no unresolved blocker concealed.
- **Prohibited jumps or interpretations:** Pilot readiness is not pilot authority; a pilot is not general availability, launch, release, or permission to expand users or data scope.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R11 — REL Release, Version, Deployment, and Tag Decision

- **Purpose:** Decide separately whether the validated pilot result may proceed to any release, version, deployment, launch, or tag action.
- **Entry conditions:** Implementation, security governance, system validation, and pilot closeout are complete; explicit release-decision authority exists.
- **Required deliverables:** REL evidence package and separate Human Owner decisions for release, version, deployment, launch, and tag scope as applicable.
- **Exit criteria:** Each relevant authority is explicitly granted or denied and any authorized action has bounded conditions; absent authority remains `NONE`.
- **Prohibited jumps or interpretations:** REL does not start before implementation, security, validation, pilot readiness, and explicit release authority; no one authority implies another.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R12 — Product Portfolio Expansion

- **Purpose:** Consider evidence-led expansion beyond the first product/MVP into additional product directions.
- **Entry conditions:** The initial product has working capability and credible user-value, safety, operating, and governance evidence; expansion consideration is separately selected.
- **Required deliverables:** Direction-specific evidence, prioritization decision, bounded scope, non-goals, risks, and authority requirements.
- **Exit criteria:** The Human Owner selects, defers, or rejects each proposed expansion without implying implementation authority.
- **Prohibited jumps or interpretations:** Do not expand from naming, aspiration, roadmap position, or pilot novelty; each product direction repeats applicable readiness and authority gates.
- **Status at roadmap adoption:** `NOT-STARTED`.

### R13 — Higher Memory Runtime Evolution

- **Purpose:** Consider higher memory-layer runtime evolution only after demonstrated product capability and evidence justify it.
- **Entry conditions:** Relevant working capability, user value, safety evidence, and governance evidence exist; a separate Human Owner evolution decision is opened.
- **Required deliverables:** Evidence-based need, bounded proposal, risks, governance implications, readiness assessment, and explicit decision.
- **Exit criteria:** The proposal is selected, deferred, or rejected with any later implementation still subject to bounded authority.
- **Prohibited jumps or interpretations:** Documentary layer names, V7 designation, version-number pressure, or portfolio ambition cannot activate a runtime or bypass prior gates.
- **Status at roadmap adoption:** `NOT-STARTED`.

## 4. R2 Product and MVP Decision / R2 产品与 MVP 决定

R2 is the next substantive stage. It must decide:

- the primary product direction;
- the target user;
- the concrete user problem;
- three to five core workflows;
- the MVP scope;
- explicit non-goals;
- success metrics;
- data, permission, and governance boundaries; and
- the product hypothesis and validation plan.

The recommended first product direction is **Civilization Core Governed Memory Control Plane**. This is a recommendation for R2 consideration, not an approved or selected product decision.

Potential initial surfaces may include:

- Operator Console;
- Memory Governance UI; and
- Evidence / Review / Approval Dashboard.

Neither the recommendation nor these potential surfaces are selected until a separate Human Owner R2 decision records that selection. R2 must remain a decision task and must not contain implementation work.

## 5. R3 Evidence and Readiness Establishment / R3 证据与就绪建立

If R2 affirmatively selects a direction and a separately authorized R3 begins, R3 must distinguish the following evidence classes:

- **Product evidence:** Evidence that the identified users experience the stated problem, can use the proposed workflows, and value the bounded outcome under defined success metrics.
- **Technical feasibility evidence:** Bounded prototypes, tests, measurements, and integration findings sufficient to evaluate the selected MVP without pretending a prototype is production implementation.
- **Operating-model evidence:** Ownership, support, review, approval, incident, recovery, continuity, and day-to-day operating evidence for the bounded use case.
- **Security and privacy evidence:** Data classification, permissions, threat and abuse analysis, privacy constraints, controls, and residual-risk evidence appropriate to the selected scope.
- **External facts only when a concrete external dependency exists:** Current external research or verification is required only when a named dependency, platform, law, standard, service, market fact, or other external condition is indispensable to the bounded decision.

More internal documentation alone cannot establish readiness. R3 must produce decision-relevant substantive evidence under explicit authority; it must not merely restate the existing corpus.

## 6. R4 Readiness Reassessment / R4 就绪重评

R4 permits exactly three readiness outcomes:

- `READY`: the bounded evidence establishes readiness for separate implementation-authorization consideration;
- `DEFER`: the evidence does not yet establish readiness and the decision is postponed without implementation authority; or
- `REJECT`: the bounded implementation direction is declined on the assessed basis.

Only `READY`, followed by a separate Human Owner bounded implementation decision, may permit R5 consideration. `READY` alone does not authorize R5 execution, and neither `DEFER` nor `REJECT` permits R5 consideration.

## 7. R5 through R11 Execution Corridor / R5 至 R11 执行走廊

The controlling corridor order is:

`R5 bounded authorization` → `R6 vertical slice` → `R7 integration surfaces` → `R8 SEC-GOV` → `R9 system validation` → `R10 real-world pilot` → `R11 REL decision`.

This order may not be compressed or reinterpreted as concurrent blanket authority. SEC-GOV does not start before a concrete authorized implementation exists. REL does not start before implementation, security, validation, pilot readiness, and explicit release authority.

The V7 documentary designation is not package version `v7.0.0`. At roadmap adoption, the package remains `6.16.0`, and no version or tag authority exists.

## 8. R12 and R13 Long-Term Expansion / R12 与 R13 长期扩展

Possible product expansion must be considered in this risk-aware order:

1. Personal Brain;
2. Team Memory System;
3. AI Agent Memory Constitution Layer; and
4. Enterprise Knowledge Governance.

This ordering is a planning sequence, not approval of any direction. Each expansion requires its own product evidence, boundary decision, readiness work, and bounded authority.

Higher memory-layer runtime evolution must be driven by working capability, user value, safety evidence, and governance evidence—not by naming or version-number pressure.

## 9. Roadmap Checkpoint Protocol / 路线图检查点协议

The following checkpoint must appear before every new repository task. Concrete values must be supplied; placeholders are the reusable field contract.

```text
ROADMAP_CHECKPOINT
MASTER_ROADMAP=POST-IDG-MASTER-EXECUTION-ROADMAP
CURRENT_BASELINE=<main commit>
CURRENT_STAGE=<R0-R13>
CURRENT_SUBSTAGE=<specific substage>
LAST_COMPLETED_STAGE=<stage>
LAST_COMPLETED_EVIDENCE=<PR/commit/file/tests>
NEXT_PLANNED_STAGE=<stage>
ENTRY_CONDITIONS=<state>
BLOCKERS=<specific blockers>
AUTHORIZED_SCOPE=<current bounded scope>
FORBIDDEN_JUMPS=<prohibited stages>
DRIFT_STATUS=<ON-ROUTE|DRIFTED>
CORRECTION_REQUIRED=<YES|NO>
```

The checkpoint is a prerequisite for task selection, not authority for the task it describes. If it shows drift, unmet entry conditions, or absent authority, the task must stop or be corrected before work begins.

## 10. Stage Closeout Comparison Protocol / 阶段收尾对比协议

The following comparison must appear after every stage or material substage completion. It compares the bounded plan with actual output before any successor is selected.

```text
STAGE_CLOSEOUT_COMPARISON
PLANNED_STAGE=<stage>
PLANNED_OUTPUTS=<planned deliverables>
ACTUAL_OUTPUTS=<actual deliverables>
EXIT_CRITERIA_TOTAL=<count>
EXIT_CRITERIA_PASSED=<count>
UNMET_CRITERIA=<specific unmet criteria>
UNPLANNED_CHANGES=<specific changes>
ROADMAP_DEVIATION=<NONE|PRESENT>
CORRECTIVE_ACTION=<action>
NEXT_STAGE_ALLOWED=<YES|NO>
```

A closeout comparison records conformance; it does not automatically authorize the next stage.

## 11. Drift Detection and Correction Rules / 漂移检测与纠正规则

The following rules control every future task under this roadmap:

1. No concrete defect means no GOV-MAINT task.
2. A clean audit stops instead of generating another audit.
3. Every task must map to one roadmap stage.
4. A task that maps to no stage is drift.
5. Documentation volume is not product progress.
6. Design completion is not implementation completion.
7. No stage may skip its entry conditions.
8. No task may create authority by implication.
9. A detected drift must be disclosed and corrected in the same response.
10. After each merged PR, roadmap comparison precedes successor selection.
11. No automatic successor work.
12. Human Owner decisions remain required at every authority transition.

When drift is detected, the active response must name the planned stage, the actual deviation, the affected entry or exit condition, and the corrective action. Unauthorized work must not be normalized as roadmap progress.

## 12. Adoption and Next Stage / 采用与下一阶段

Adoption of this roadmap completes R1 upon merge. The repository then points to R2 as the next planned stage.

R2 does not begin automatically. The next repository task must be a bounded R2 Product Direction and MVP Decision task, preceded by the roadmap checkpoint. No implementation code is authorized.

## 13. Final Machine State / 最终机器状态

```text
ROADMAP_ID=POST-IDG-MASTER-EXECUTION-ROADMAP
ROADMAP_STATUS=ACTIVE
ROADMAP_BASE_COMMIT=4fe763f74cb8e4ab22cac122f8ab0a5b37dc8715
R0_STATUS=COMPLETE
R1_STATUS=COMPLETE-UPON-MERGE
CURRENT_STAGE=R1
NEXT_PLANNED_STAGE=R2
R2_STATUS=NOT-STARTED
R3_STATUS=NOT-STARTED
R4_STATUS=NOT-STARTED
R5_STATUS=NOT-STARTED
R6_STATUS=NOT-STARTED
R7_STATUS=NOT-STARTED
R8_STATUS=NOT-STARTED
R9_STATUS=NOT-STARTED
R10_STATUS=NOT-STARTED
R11_STATUS=NOT-STARTED
R12_STATUS=NOT-STARTED
R13_STATUS=NOT-STARTED
GOV_MAINT_03_STATUS=CLOSED
GOV_MAINT_04_AUDIT=COMPLETE-NO-DEFECT
GOV_MAINT_05=CANCELLED
HUMAN_OWNER_IMPLEMENTATION_DECISION=DEFER
IMPLEMENTATION_DECISION_BASIS=READINESS-NOT-ESTABLISHED
IMPLEMENTATION_READINESS=NOT-ESTABLISHED
IMPLEMENTATION_START=NO
PRODUCT_IMPLEMENTATION=NOT-AUTHORIZED
IMPLEMENTATION_AUTHORITY=NONE
DEPLOYMENT_AUTHORITY=NONE
LAUNCH_AUTHORITY=NONE
RELEASE_AUTHORITY=NONE
VERSION_AUTHORITY=NONE
TAG_AUTHORITY=NONE
PACKAGE_VERSION=6.16.0
V6_CONTINUATION=NEVER
V7_RUNTIME_IMPLEMENTATION=DEFER
AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_REPOSITORY_TASK_CLASS=R2-PRODUCT-AND-MVP-DECISION
ROADMAP_DRIFT_CONTROL=ACTIVE
```
