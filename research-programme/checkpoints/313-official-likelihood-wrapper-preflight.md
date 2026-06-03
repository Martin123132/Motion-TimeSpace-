# 313 - Official Likelihood Wrapper Preflight

Private empirical preflight checkpoint. This is not a public cosmology, CMB, local-GR, galaxy, or parent-field-theory claim.

## Purpose

Checkpoint 312 said the next real empirical upgrade is:

```text
official/full-likelihood-style SN+BAO+growth wrapper.
```

This checkpoint does not score that wrapper.

It freezes the preflight contract:

```text
data assets,
baseline parity,
model matrix,
run graph,
dry-run commands,
claim ceilings,
and long-run policy.
```

## Wrapper Components

| Component | Status | Claim Limit |
|---|---|---|
| SN full-cov no-SH0ES | runner supports full covariance, full selected rows, and `mb-corr` branch | late-time background only |
| DESI DR1/DR2 BAO split | DR1/DR2 mean/covariance files present | release robustness only |
| H(z) source-lock | existing source-locked competitive draw | independent H(z) holdout only |
| growth covariance | existing source-locked preferred/draw under GR-proxy gate | no perturbation promotion |
| ELG grid | existing non-Gaussian grid competitive draw | no official joint-likelihood claim |
| CMB bridge | contract/readiness only | no CMB pass claim |

## Important Command Fix

The current SN+BAO runner uses:

```text
--include-calibrators
```

as the optional flag.

Therefore the no-SH0ES branch is the default calibrator-excluded branch.

So future commands must not use:

```text
--exclude-calibrators
```

because that flag does not exist in the runner.

That is now corrected in the generated command queue.

## Dry-Run First Policy

The next empirical run must start with:

```text
phase = dry-run
```

for both:

```text
DESI DR2 full-cov no-SH0ES,
DESI DR1 full-cov no-SH0ES.
```

Only after dry-run gates pass should scoring run with:

```text
--phase short-smoke
--sn-covariance-mode full
--sn-max-rows 0
--sn-observable mb-corr
wide CPL w0/wa boxes
```

## Baseline Parity

The wrapper must score:

```text
LCDM,
wCDM,
CPL,
MTS_fixed_2over27_no_clock,
MTS_Bmem_zero,
MTS fitted-parameter ablations only as diagnostics.
```

Rules:

```text
same rows,
same covariances,
same nuisance policy,
same release split,
same jackknife/sensitivity reporting,
same edge-hit punishment.
```

No model gets to skip a punch.

## Acceptance Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | preflight traceable |
| data assets present | pass | local assets exist for wrapper dry-run |
| official source refresh available | pass | source/manifest guard exists |
| dry-run commands corrected | pass | no nonexistent `--exclude-calibrators` flag |
| baseline parity defined | pass | same judges for MTS and baselines |
| wrapper scores executed | fail | this is preflight only |
| stable evidence allowed | fail | no stable evidence language |
| long-run policy written | pass | VS Code / completion-marker workflow retained |

## Long-Run Workflow

For actual scoring:

```text
run from VS Code terminal,
write outputs under runs/<timestamp>-...,
write status.json,
write COMPLETE.txt,
then prompt Codex again.
```

No waiting loop.

No token-burning spectator mode.

## Decision

Decision:

```text
official_likelihood_wrapper_preflight_ready_dryrun_first_no_scores_or_claims
```

Claim ceiling:

```text
preflight_and_wrapper_contract_only_no_stable_evidence_or_theory_promotion
```

Meaning:

```text
the empirical wrapper is ready for dry-run,
but no new score or support claim has been produced.
```

Boxing-card version:

```text
We are not announcing the fight result.
We have checked the ring, the gloves, the judges, the rules,
and spotted the bad shoelace before the bell.
```

## Machine Artifacts

Script:

```text
scripts/official_likelihood_wrapper_preflight.py
```

Run:

```text
runs/20260601-000136-official-likelihood-wrapper-preflight
```

Output files:

```text
runs/20260601-000136-official-likelihood-wrapper-preflight/results/source_register.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/data_asset_inventory.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/wrapper_components.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/model_baseline_matrix.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/likelihood_run_graph.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/dryrun_command_queue.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/acceptance_gates.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/claim_ceilings.csv
runs/20260601-000136-official-likelihood-wrapper-preflight/results/decision.csv
```
