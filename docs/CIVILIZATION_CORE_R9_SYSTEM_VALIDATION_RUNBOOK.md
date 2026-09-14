# Civilization Core R9 Isolated System Validation Runbook

Run from `/Users/han/hermes-memory-fabric-plugin` at commit
`f39399491b9ec408900a4e11539a4392b36f3aa6`. Use only synthetic fixtures. The
commands below require zsh, the existing `.venv`, and no network or model.

## Inputs and binding

The ALLOW command uses observation mode. Its canonical payload is
`{"operation":"R7_REAL_USE_OBSERVATION_VALIDATION","project_id":"CIVILIZATION-CORE","operator":"FOUNDER-OPERATOR","observation":<fixture>,"confirm_real_use_observation":true}`.
The expected SHA-256 is `e991a975983c3818756cbb002c68c716f6042ba39023d284bb86c53f6d34ced8`.

The BLOCK command uses legacy mode with the candidate fixture and the literal
arguments below. Its canonical payload follows `build_legacy_payload`; the
expected SHA-256 is `28e7dafbf7d04b51e789fca3d693c210c8f7ad185486c7340d86f310583fedbb`.
Canonical JSON is UTF-8, keys sorted, separators `,` and `:`, Unicode preserved,
and non-finite numbers rejected. Recompute both bindings independently before
execution; do not use the production validator to create expected values.

## ALLOW real entry

```zsh
r9_allow_workspace="$(mktemp -d /tmp/r9-allow-workspace.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m hermes_memory_fabric.p4_m0_subspace_operator continuity \
  --workspace-root "$r9_allow_workspace" \
  --project-id CIVILIZATION-CORE --operator FOUNDER-OPERATOR \
  --real-use-observation-json "$(<tests/fixtures/r9/continuity_allow_observation.json)" \
  --confirm-real-use-observation \
  --security-envelope-json "$(<tests/fixtures/r9/continuity_allow_security_envelope.json)"
```

Expected: exit `0`, empty stderr, one compact stdout JSON line,
`security_decision={"code":"security_policy_allowed","disposition":"ALLOW"}`,
`terminal=true`, `non_persisted=true`, `benefit_inference_allowed=false`, the
documented measurement scope, and null baseline scope. The workspace and both
input files must be unchanged.

## Sensitive BLOCK real entry

Use a distinct new workspace:

```zsh
r9_block_workspace="$(mktemp -d /tmp/r9-block-workspace.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m hermes_memory_fabric.p4_m0_subspace_operator continuity \
  --workspace-root "$r9_block_workspace" \
  --project-id CIVILIZATION-CORE --operator FOUNDER-OPERATOR \
  --query "R9 synthetic sensitive continuity" \
  --candidate-json "$(<tests/fixtures/r9/continuity_block_sensitive_observation.json)" \
  --outcome defer --rationale "Synthetic human review." \
  --corrected-outcome request_changes --correction-rationale "Synthetic correction." \
  --revocation-rationale "Synthetic terminal revocation." \
  --input-classification SENSITIVE \
  --confirm-human-review --confirm-scope-check --confirm-correction \
  --confirm-revocation --confirm-no-apply \
  --security-envelope-json "$(<tests/fixtures/r9/continuity_block_sensitive_security_envelope.json)"
```

Expected: exit `2`, empty stdout, and one compact stderr JSON line containing
only `code=sensitive_classification_blocked`, `disposition=BLOCK`, and a
sanitized `receipt_id`. It must contain no candidate, query, rationale, digest,
or payload binding, and create no workspace or downstream persistence artifact.

## Focused corridor

Confirm all four paths exist, then run once with a 9000-second outer limit:

```zsh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src .venv/bin/python -m pytest -p no:cacheprovider -q \
  tests/test_p4_m0_subspace_operator.py \
  tests/test_provider_federation_boundary.py \
  tests/test_r8_local_persistence_governance.py \
  tests/test_r8_security_governance.py
```

Pass requires exit `0`; report actual collection and terminal summary without
assuming a count.

## Isolated Hermes no-model smoke

The source-only preflight may use an already-installed Hermes Python, but its
Hermes runtime identity and the Memory Fabric distribution are separate facts.
For the validated isolated route, build the authenticated source copy with the
declared `setuptools.build_meta` backend, install its wheel into a new
repository-external environment with index and dependency resolution disabled,
and reuse the existing local Hermes loader and dependencies read-only. Verify
that the isolated site-packages precedes every reused dependency path, the
distribution and both entry points come from the wheel, `hermes_memory_fabric`
comes from the isolated installation, and `plugins.memory` comes from the
recorded real Hermes checkout. Do not use `PYTHONPATH=src` as installation
evidence.

```zsh
r9_hermes_home="/exclusive/evidence/directory/hermes-home"
r9_python="/exclusive/evidence/directory/hermes-isolated-venv/bin/python"
PYTHONDONTWRITEBYTECODE=1 "$r9_python" scripts/install_memory_fabric_shim.py --hermes-home "$r9_hermes_home"
HERMES_HOME="$r9_hermes_home" EXPECTED_VERSION=6.16.0 \
  PYTHON="$r9_python" PYTHONPATH= \
  bash scripts/smoke_memory_fabric_hermes.sh
```

Pass requires exit `0`, actual version `6.16.0`, `memory-fabric` discovery and
load, empty tool schemas, and `build_active_context`. Record imported module
paths and distinguish the plugin distribution version from the Hermes runtime
version and loader path. The 2026-09-14 isolated run used the existing local
Hermes loader (`hermes-agent==0.18.2`), loaded the plugin distribution as
`6.16.0` from the isolated environment, and exited `0`. Its only smoke-time
filesystem addition was the Hermes-generated default `SOUL.md` inside the fresh
`HERMES_HOME`; the shim files were unchanged and no default Hermes home changed.

## Evidence, interruption, and recovery

Before each long command record its exact argv, cwd, input hashes, output paths,
and process identity. Capture stdout, stderr, exit code, `/usr/bin/time -l`
measurements, and before/after recursive file manifests. Product and smoke
commands have a 60-second limit; focused pytest has 9000 seconds. Treat RSS as
a measurement, not a 512 MiB product gate, and stop expanding evidence near
50 MiB.

After interruption, inspect the recorded PID/PGID and receipts. Observe a still
running matching process; reuse an identical-input PASS; run only if never
started; recover facts before any rerun when terminal state is unclear. Only a
documented fixture, runbook, or isolation setup error permits one corrected
rerun while preserving the first result. Stop on implementation failure,
timeout, leakage, unexpected write, or inability to recover. Temporary data may
be retained for review; removal is outside this runbook and must target only a
verified task-owned path.
