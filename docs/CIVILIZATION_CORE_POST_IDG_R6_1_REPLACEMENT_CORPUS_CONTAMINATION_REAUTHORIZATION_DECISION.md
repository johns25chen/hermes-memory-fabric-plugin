# Civilization Core Post-IDG R6.1 Replacement Corpus Contamination Reauthorization Decision

## 1. Purpose

This document records the final governance disposition of the contaminated, never-effective replacement evaluation work and conditionally authorizes a clean-room successor. It is documentation-only, creates no implementation, and grants no current implementation authority.

TASK_ID=POST_IDG_R6_1_REPLACEMENT_CORPUS_CONTAMINATION_REAUTHORIZATION_DECISION
BASE_COMMIT=ace33ad27a8021f2a9a4a94186f5852ff10d16c0
ALLOWED_WRITE_FILE_COUNT=1

## 2. Controlling repository state

The controlling package version is 6.16.0. PR #371 is closed, was never merged, and its invalid implementation never became repository-effective. The retired implementation is not a repository artifact. Current implementation authority is none.

PR_371_STATUS=CLOSED-UNMERGED
CONTAMINATED_FEATURE_COMMIT=a0e44c1f69cf4df27c2765480c78d6e67b18b333
CONTAMINATED_CORPUS_SHA256=be58fee2405420e97d80c5f50419ee476b434bcae3adc73a602b048687278b31

## 3. PR 371 contamination event

During a pre-merge PR audit, a diff-returning interface exposed the scored corpus and hidden answer material to an answering assistant. The repository owner did not receive candidate contents in terminal output. This contamination is an audit-procedure failure, not Human Operator evidence.

EXPOSURE_CHANNEL=GITHUB-PR-DIFF-RETURNING-INTERFACE
ANSWERING_ASSISTANT_SCORED_CORPUS_EXPOSURE=TRUE
REPOSITORY_OWNER_SCORED_CORPUS_EXPOSURE=FALSE

## 4. Measurement disposition

No actual Human Operator session started, no Human Operator observation was recorded, and no Evidence document was created. No scored result exists. No learning conclusion, reliability conclusion, product conclusion, or statistical significance exists. Test data and audit exposure must not be represented as Human Operator evidence.

ACTUAL_HUMAN_OPERATOR_SESSION_STATUS=NOT-STARTED
HUMAN_OBSERVATIONS_RECORDED=FALSE
EVIDENCE_DOCUMENT_STATUS=NOT-CREATED
INVALID_RESULT_CONVERTED_TO_SUCCESS=FALSE

## 5. Permanent retirement decision

The contaminated corpus and implementation are permanently retired. They may not be reused, copied, reconstructed, recovered, or treated as partial success. Authorization of V2 does not validate, repair, continue, or convert PR #371.

CONTAMINATED_CORPUS_STATUS=PERMANENTLY-RETIRED
CONTAMINATED_CORPUS_REUSE_AUTHORIZED=FALSE
CONTAMINATED_IMPLEMENTATION_REUSE_AUTHORIZED=FALSE
CLEAN_ROOM_REIMPLEMENTATION_REQUIRED=TRUE

## 6. Root-cause assessment

The root cause was use of a content-returning audit path on sealed scored material before merge. The failure crossed the evaluation blindness boundary by returning corpus and answer-oriented material to an answering assistant. It did not create a repository-effective implementation, an operator observation, or a valid measurement.

## 7. Reauthorization decision

Only after this document is merged and repository-effective, it authorizes the clean-room successor task and only its Checkpoint A. Merging this decision authorizes only V2 Checkpoint A. Checkpoint B remains unauthorized until V2 Checkpoint A is independently validated, merged, and repository-effective.

REAUTHORIZATION_DECISION=AUTHORIZE
AUTHORIZED_SUCCESSOR_TASK=POST_IDG_R6_1_REPLACEMENT_V2_ONBOARDED_OPERATOR_EVALUATION
AUTHORIZED_CHECKPOINT_A=POST_IDG_R6_1_REPLACEMENT_V2_OPERATOR_EVALUATION_CHECKPOINT_A
AUTHORIZED_CHECKPOINT_B=POST_IDG_R6_1_REPLACEMENT_V2_OPERATOR_EVALUATION_CHECKPOINT_B
AUTHORIZED_RUNTIME_SURFACE=governed_memory_operator_session

## 8. Clean-room successor identity

The successor must be implemented only from the repository-effective authorization documents, the unchanged existing evaluation engine, the unchanged existing engine tests, the unchanged original corpus, and the cryptographic denylist in this document.

It must not read, checkout, fetch, inspect, recover, copy, or use the contaminated feature commit, the PR #371 diff or patch, the retired source implementation, the retired test implementation, the retired corpus contents, or any log or transcript containing retired corpus material.

It must create freshly authored source code, freshly authored focused tests, four freshly authored non-scored practice examples, twelve freshly authored scored candidates forming six matched pairs, and a new replacement corpus SHA-256.

NEW_REPLACEMENT_PRACTICE_COUNT=4
NEW_REPLACEMENT_SCORED_TRIAL_COUNT=12
NEW_REPLACEMENT_PAIR_COUNT=6
NEW_REPLACEMENT_CORPUS_MUST_BE_NEW=TRUE

## 9. Retired-corpus cryptographic denylist

The denylist is comparison-only and contains hashes, schema metadata, and retired source identities only. It contains no retired candidate text, candidate IDs, source IDs, fixture IDs, expected outcomes, reason codes, answer keys, or other raw retired corpus content.

<!-- BEGIN RETIRED CORPUS IDENTITY DENYLIST -->

```json
{"candidate_content_sha256":["11fb4b71962d944e2fd54a23b2ffd2b250cbd701afdcd0841196f925ba644c68","21e9abf4f9105e1e45a46ce73b848880cfea03e7f45d4a352127631b79633aeb","3657d74820d681b1fc1bf163f7cfa4fbb60edd5aff2684f803abaa0917261313","49a74b9eef6eb31c49bbc30b4a3d8539cbe696334cb89d12ea2189a371f72d19","54667abed98dcd693fa1744522b67895164a8770faf15cd8b3e97ca4d1327660","6a6bf5d8c0120a047d0b67fde02d8d016902deea50a40a9f9d7790ebe72a8dfb","75821eff650296e305273485365d7c7602ba76eadd11612fcc04546e5df787d2","a0241c15c12617fd198fda354025ce198081d0664dcd40ce1bf9784be35b63a7","a995c7d49cdd3f6c12acdb9021e4ba5c3d5ad03f9c4074c119d80212b228b102","aa521c272a691520d5c145dcbb4336a8f2484ca499b995395e9a5824544f65af","d2dd9d02a175b61fbacf32e8cb427c966d8f256f1ee882ce72a7fc1ade6bdb6a","d533830c1c2c5b399ab21132ea10721667547467ddb0b2221a1e135555244045"],"candidate_id_sha256":["043273097cf740116a02c837cc3f0f717566351825ecd5d5b779b3e4e54b3783","09d57b2de53984bc95ea4a61bf1be7be4a453725ce3b6aac3a636529a8f6309a","1cc4d2927f4ab5fa8ad150634b24a579f8f3e646cc8e689b338104fdb9d28d4a","1ce605c3834dcdce8dd40bc3d87bd28f85721fb60efe9267f16d801d5eb2fa88","2758f7168a26b9750fcaa5867d4be4ef11caf413448df0cd4043f89a529b7813","4e3e323ebb1a8167a9f79fff7d00ca15010b7311b2f25cb6f67593bab849af1e","61ce4b788e7c9763e6a6f7861d36a2bd5394fa25cef79e4f56326c955befe670","666d5a9eb4b61fa9a65df4e20018134ec11c6fad7abd83c49937dd5e92bc92fd","6a868ecc17f36be30730c28e221c0f49bc78e46ab1f26fa3fa4a5c6258c77826","94b5139488a36c322ab1f125a2e1b1453d2f36f07fbf324bcd006a71b739237e","a2fb163ed9c6341f4b777968ea6c080c5dba2e186984ad3075695bc39991a846","b5d4902b4e6b9af600d2a5f635d02332a5a021bce85b9ff9db2a7b15161c3cf6"],"candidate_mapping_sha256":["040b468403ec1ce7a1925c8f8c5142241f586dc8df478dd59826a9d3ef2a3aa4","3cd6d08d1ad842d6c70bace221643dd4c2d47ff5fad5dd27906e2599a055598f","3efae8f280676193944e2dd2b55f726069e0aba38a536d6ca7d9c6c4d7b36f61","50b0e43c5428b825a2627ae0a8ace49b979608f8c704ebdc1a94cd2c614c7796","5bde428ebf54aae306744c5a107d6ccbb76301de3b969d022eff7afb7c98d2a9","696b7f9c1e310fe430859db751bc05c586402d32d32c50eb08f042339b836509","81ad07c181464beec62d634d0df95f148040cbbf6c7ec13689ab89b8c3750625","85fbf77a29a4ccc9fb18ef27e1cc5e1551380b29402049c489f54d9759e58c4b","aded16d322857d1e3ae0a3c7524adf888314ef7315bc861b09b33b10204cc63e","c99e5b70010a3c7e063eb5e967fce0ea0c3830e98634533ecca8c2dc2b72717a","d3bb16bfd2badeeebba8f10351334b7393dc7550695e3ebc81afadfbad73f251","dbacefb4f3ac8a9dd53ad7fa670dcc1d8aa029a2654f4243428b811087a01a03"],"fixture_identity_sha256":["64021ac122768de7c1e46685c73e18ec83282f6a5d36d72506cf73b8c8898740","67e42faeb860c8d5edd25a93938ca3ef953404072c1749449aa2ac09b768a455","791891ec7ea508258033c2666695f14187200f4c22e28a8199366732cb4be778","79b38b01a0ef286a933782e21f53b384ea9ff3e6e66e05f589c78ca2456b44b7","7cd88b0dd4ffb2f9851dd910dc4aefeb1045ac66f4d0d2e1b901ee0aa012ba27","8402ea6a3325e4bb5ea481f31e447a3527085148953dec091a4462c9a5c9f534","95dcf1bb96403a4b5ef47c02eea51e55ddcce33256b517371b7229e0ef74e34a","a9e56588b0960b1d63b5576bf25f611589dc93f9ea74ad07ceedfda16586788b","aea8b43102163e47cfaa92fdd63a51dab40fef3e532d332529958157e934c25b","c2b080b73e708eb626bb2e1caa0567c8b4246b5547a0000e3253d86ed6a2e7a6","e5793693a41171c2cda434263127f509de45589ae6b04062499cd51e2409aa0f","fa0d4baacf8a5ededdf1b022bf37632dcd4cef0f87d4f1ef4147527444c2995e"],"schema_version":"1","source_corpus_sha256":"be58fee2405420e97d80c5f50419ee476b434bcae3adc73a602b048687278b31","source_feature_commit":"a0e44c1f69cf4df27c2765480c78d6e67b18b333","source_id_sha256":["3d0074268c0a0b8aade219b14ba3f49c7b6fbfdd07231c659ada2177ae32ca8c","3d6f697af157ebc8e7638703cabc90ce58221199f41387960486b67aca4b7afb","55cb05406944e2814dee3a7d6c2038190170617737c467c14bcd7ab44b8c20fb","625798d3bfa5c2512e39aaa9fb849be82ad6fd2d92fb8ad9e398ad3442dda5a3","879b88a3c3686f03c8b8d73d9dd6199e5e800f152104ceab6cc8f84802910ceb","98fa7645ffce26e345934519386c857cb3f7aebbb194beff74d80697db5d98d6","b26c7db22b36332158a8a00922e74bc754059a3819d3ef192e3aededf1c34328","b4be880aeb60ca4344c3c86082704a1c8424d3c10d3d9a584967c54870adb52c","bcfe7a95d581718d61e42094f8378bdb8487ffe6cb9ae25ae2041103d235a798","cffd308aa68db67e1a9f01324ccfce9671c91f2b9fd20c3d40ce447e0f3f51e1","e262cb38d1909ce4a125a92a38d286463fa5c140ae7794ed5b1e82161775c099","f7550eccad78ae1bb20f2c70120cfda29765a29f7c23eeb627fbe3cec9982651"]}
```

<!-- END RETIRED CORPUS IDENTITY DENYLIST -->

RETIRED_IDENTITY_DENYLIST_ENTRY_COUNT=12
RETIRED_IDENTITY_DENYLIST_SHA256=dc85a0ce497e48cd49426fa639e0dfe2a6d6dff3039322413498ca7db426474a
RETIRED_IDENTITY_DENYLIST_USE=COMPARISON-ONLY
FUTURE_ACCESS_TO_CONTAMINATED_FEATURE_COMMIT=PROHIBITED
FUTURE_ACCESS_TO_PR_371_DIFF_OR_PATCH=PROHIBITED

## 10. New-corpus independence requirements

The new scored corpus must have zero overlap with both the original repository-effective corpus and every applicable hash set in the retired denylist. Opaque machine validation must prove zero overlap for canonical candidate mapping digests, candidate-content hashes, candidate-ID hashes, source-ID hashes, and fixture-identity hashes.

ORIGINAL_CORPUS_DIGEST_OVERLAP_ALLOWED=FALSE
CONTAMINATED_CORPUS_DIGEST_OVERLAP_ALLOWED=FALSE
CONTAMINATED_CONTENT_HASH_OVERLAP_ALLOWED=FALSE
CONTAMINATED_CANDIDATE_ID_HASH_OVERLAP_ALLOWED=FALSE
CONTAMINATED_SOURCE_ID_HASH_OVERLAP_ALLOWED=FALSE
CONTAMINATED_FIXTURE_IDENTITY_HASH_OVERLAP_ALLOWED=FALSE

## 11. Non-scored practice independence

The four NON-SCORED-PRACTICE examples must be freshly authored, must not disclose or encode scored answers, and must not reuse retired practice or scored material. They remain outside scoring and may demonstrate only the permitted interface mechanics and fixed glossary.

## 12. Operator eligibility boundary

The repository owner is ineligible to act as the scored operator because the owner has viewed old answer-oriented material. An answering assistant is never eligible to act as the scored operator.

The future scored operator must be a distinct independent human who has viewed none of the old expected-outcome material, old answer-oriented mappings, original scored answer key, retired scored corpus, new scored corpus, or new answer key. If such an operator is unavailable, Checkpoint B must not start.

SCORED_OPERATOR_REQUIREMENT=INDEPENDENT-UNEXPOSED-HUMAN
REPOSITORY_OWNER_ELIGIBLE_AS_SCORED_OPERATOR=FALSE
ANSWERING_ASSISTANT_ELIGIBLE_AS_SCORED_OPERATOR=FALSE

## 13. Sealed development protocol

Development may use deterministic machine processing of the new corpus, but new scored content must never be rendered to the repository owner, an answering assistant, logs, comments, summaries, or terminal output. Opaque hashing, schema validation, digest comparison, and test execution are permitted only when candidate content is not printed, logged, quoted, or returned to an assistant.

Any pre-session exposure retires the complete new corpus and requires another repository-effective governance decision.

## 14. Sealed PR review and audit protocol

For any future PR containing a scored corpus, audit is restricted to PR number, title, state, base and head branch, exact head SHA, draft and mergeable state, changed filenames only, file counts, line counts, whole-file SHA-256 values, safe aggregate corpus counts, test and CI status, and opaque machine validation results.

Audit must not access a PR diff, PR patch, per-file patch, Files Changed corpus content, corpus file content through a connector, `git show`, `cat`, `sed`, `grep`, `head`, `tail`, equivalent corpus rendering, or any tool response containing diff or file contents.

PR_AUDIT_MODE=SEALED-METADATA-ONLY
PR_DIFF_ACCESS_AUTHORIZED=FALSE
PR_PATCH_ACCESS_AUTHORIZED=FALSE
CORPUS_FILE_CONTENT_ACCESS_AUTHORIZED=FALSE
OPAQUE_HASH_AND_MACHINE_VALIDATION_AUTHORIZED=TRUE

## 15. Retained interface and instrumentation contract

The successor retains the repository-effective design: runtime surface `governed_memory_operator_session`; exactly four NON-SCORED-PRACTICE examples; exactly twelve scored trials and six matched pairs; the same six scenario classes; the same counterbalanced condition structure; one project, `civilization-core`; SYNTHETIC input only; fixed Chinese outcome and glossary mappings; automatic monotonic Human time; exact action-event instrumentation; exact correction/rework instrumentation; current-trial editing before lock; final confirmation before lock; no return to locked trials; all session state in memory; and no persistence.

It also retains no Evidence during Checkpoint A and no model, network, connector, external service, proposal, application, promotion, execution, or continuation.

## 16. Exact future write set

The conditional future authority is limited to exactly these four paths:

1. `src/hermes_memory_fabric/governed_memory_operator_session.py`
2. `tests/test_governed_memory_operator_session.py`
3. `docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json`
4. `docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md`

No other future path is authorized by this decision.

AUTHORIZED_FUTURE_WRITE_FILE_COUNT=4
AUTHORIZED_FUTURE_WRITE_FILE_1=src/hermes_memory_fabric/governed_memory_operator_session.py
AUTHORIZED_FUTURE_WRITE_FILE_2=tests/test_governed_memory_operator_session.py
AUTHORIZED_FUTURE_WRITE_FILE_3=docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json
AUTHORIZED_FUTURE_WRITE_FILE_4=docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md

## 17. Replacement V2 Checkpoint A

Checkpoint A is clean-room harness and corpus readiness only. After this decision becomes repository-effective, Checkpoint A may create only future files 1 through 3. It must establish fresh authorship, retained-contract conformance, sealed handling, a new corpus digest, and all required zero-overlap proofs. It must create no Evidence and start no Human Operator session.

CHECKPOINT_A_WRITE_FILE_COUNT=3

## 18. Replacement V2 Checkpoint B

Checkpoint B is the actual Human Operator session. It may begin only after Checkpoint A is independently validated, merged, and repository-effective, and only if an eligible independent unexposed human is available. After a valid complete Human Operator session, Checkpoint B may create only future file 4.

CHECKPOINT_B_WRITE_FILE_COUNT=1

## 19. Validation corridor

Independent validation must verify the exact branch and base, single-file scope of this decision, all 24 ordered headings, every required machine-readable line exactly once, marker uniqueness, exact compact denylist bytes, denylist manifest SHA-256, twelve entries in every identity array, document hygiene, final newline, and absence of trailing whitespace.

Future Checkpoint A validation must operate without rendering scored content. It must verify the unchanged engine and engine tests, exact retained counts and pair structure, six scenario classes, counterbalancing, SYNTHETIC-only input, in-memory/no-persistence behavior, instrumentation, editing and locking rules, newly authored practice and scored material, the new corpus SHA-256, and all required zero-overlap dimensions.

## 20. Evidence requirements

No Evidence is authorized or created by this decision or Checkpoint A. Checkpoint B Evidence may be created only after a valid complete session by an eligible independent human. It must truthfully distinguish recorded Human observations from machine validation and must not expose sealed corpus or answer-key content.

## 21. Prohibitions

This decision grants no durable adoption, persistent storage, real proposal, execution, continuation, external service, deployment, release, version, or tag authority. It grants no model, network, connector, application, promotion, or automatic successor work.

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

## 22. Authority semantics

This document is complete but unmerged and is not repository-effective. Current implementation authority for new work remains none. Repository effectiveness changes authority only to bounded authority for the exact Replacement V2 Checkpoint A scope; it does not authorize Checkpoint B or any automatic continuation.

REAUTHORIZATION_STATUS=COMPLETE-UNMERGED
REAUTHORIZATION_REPOSITORY_EFFECTIVE=FALSE
CURRENT_IMPLEMENTATION_AUTHORITY_FOR_NEW_WORK=NONE
ON_REPOSITORY_EFFECTIVENESS_IMPLEMENTATION_AUTHORITY=BOUNDED
ON_REPOSITORY_EFFECTIVENESS_IMPLEMENTATION_AUTHORITY_SCOPE=EXACT-REPLACEMENT-V2-CHECKPOINT-A-ONLY

## 23. Incident lineage and interpretation limits

The incident lineage is limited to a closed, unmerged PR, a never-effective invalid feature commit, a retired corpus identity, and an audit-procedure exposure to an answering assistant. It supplies no Human Operator evidence. No learning conclusion exists. No reliability or product conclusion exists. No statistical significance exists.

The retired implementation is not a repository artifact. Authorization of V2 does not validate, repair, continue, or convert PR #371. Merging this decision authorizes only V2 Checkpoint A. Checkpoint B remains unauthorized until V2 Checkpoint A is independently validated, merged, and repository-effective.

## 24. Machine-readable reauthorization state

The following state is controlling and must be interpreted with the preceding boundaries.

AUTOMATIC_SUCCESSOR_WORK=NONE
NEXT_ALLOWED_TASK=POST_IDG_R6_1_REPLACEMENT_CORPUS_CONTAMINATION_REAUTHORIZATION_INDEPENDENT_VALIDATION_AND_COMMIT
