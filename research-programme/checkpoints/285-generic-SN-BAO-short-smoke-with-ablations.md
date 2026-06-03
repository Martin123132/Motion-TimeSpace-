# 285 - Generic SN+BAO Short-Smoke With Ablations

Private empirical-readiness checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 284 repaired the generic SN+BAO manifest. This checkpoint runs the repaired generic short smoke on:

```text
Pantheon+ / SH0ES, first 250 non-calibrator SN rows, diagonal covariance mode
DESI DR2 BAO mean + covariance, 13 rows
```

The goal is not to win the title belt. The goal is to check whether the fixed no-clock branch stays in the ring when the generic runner, fair baselines, and required ablations are active.

## Machine Artifacts

Scoring run:

```text
runs/20260601-095321-cosmo-SN-BAO-short-smoke
```

Readout script:

```text
scripts/generic_SN_BAO_short_smoke_with_ablations_readout.py
```

Readout run:

```text
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout
```

Status:

```text
generic_SN_BAO_short_smoke_scored_but_unstable_due_to_CPL_edge
```

Claim ceiling:

```text
SN_BAO_short_smoke_closure_score_only_prior_edge_blocks_stable_evidence
```

## Core Result

All models converged.

The fixed MTS branch is competitive but mixed in this smaller generic 250-SN run:

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---|
| LCDM | 130.30836712447285 | 136.30836712447285 | 147.02482922100614 | false |
| wCDM | 129.09121166811215 | 137.09121166811215 | 151.3798277968232 | false |
| CPL | 126.01714531462581 | 136.0171453146258 | 153.87791547551464 | true |
| MTS fixed `p=3, u3=1/4` | 127.66275546682708 | 135.6627554668271 | 149.95137159553815 | false |
| MTS `B_mem=0` | 130.30836712447285 | 136.30836712447285 | 147.02482922100614 | false |
| MTS fitted `p` | 127.64652272774671 | 137.6465227277467 | 155.50729288863553 | false |
| MTS fitted `u3` | 127.41590638968422 | 137.4159063896842 | 155.27667655057306 | false |

Important:

```text
the only prior-edge flag is CPL wa = -2.0.
no MTS branch hits a prior edge.
```

But the run status correctly blocks stable evidence language because any edge-hit baseline means the branch comparison is not clean enough.

## Fixed Branch Comparisons

Against LCDM:

```text
delta_chi2 = -2.645611657645773
delta_AIC  = -0.6456116576457589
delta_BIC  =  2.926542374532005
```

Interpretation:

```text
MTS improves raw chi2 and AIC, but loses BIC to LCDM in this 250-SN generic short smoke.
```

Against wCDM:

```text
delta_chi2 = -1.4284562012850728
delta_AIC  = -1.4284562012850586
delta_BIC  = -1.4284562012850586
```

Interpretation:

```text
MTS beats wCDM on raw chi2, AIC, and BIC in this run.
```

Against CPL:

```text
delta_chi2 =  1.6456101522012716
delta_AIC  = -0.3543898477987
delta_BIC  = -3.9265438799764922
```

Interpretation:

```text
CPL has lower raw chi2, but MTS beats CPL on AIC/BIC because CPL pays more parameter tax.
This comparison is unstable because CPL hits the wa prior edge.
```

## Ablation Readout

The fitted-shape ablations do not justify their extra freedom:

| Ablation | delta chi2 vs fixed | delta AIC vs fixed | delta BIC vs fixed | Status |
|---|---:|---:|---:|---|
| MTS fitted `p` | -0.016232739080365377 | 1.9837672609196204 | 5.555921293097384 | not promoted |
| MTS fitted `u3` | -0.24684907714285487 | 1.7531509228571167 | 5.325304955034909 | not promoted |
| MTS `B_mem=0` | 2.645611657645773 | 0.6456116576457589 | -2.926542374532005 | LCDM-limit negative control |

This is useful for the derivation programme:

```text
the data do not currently force p or u3 away from the fixed no-clock branch in this short smoke.
```

It does not prove `p=3`, `u3=1/4`, or `B_mem=2/27`.

## Residual Diagnostics

| Model | SN RMS | BAO RMS | BAO max abs |
|---|---:|---:|---:|
| LCDM | 0.22727696872707082 | 0.3047901126491495 | 0.6057531574431394 |
| wCDM | 0.22731382309519324 | 0.27914656773384194 | 0.6061623832834968 |
| CPL | 0.2275723309664068 | 0.2137411169119344 | 0.5631693239218158 |
| MTS fixed `p=3, u3=1/4` | 0.22728469165807005 | 0.241475876033619 | 0.6024258105996978 |
| MTS `B_mem=0` | 0.22727696872707082 | 0.3047901126491495 | 0.6057531574431394 |
| MTS fitted `p` | 0.22728680795206133 | 0.24180717501535265 | 0.6029234144013067 |
| MTS fitted `u3` | 0.22731757621650894 | 0.2333241981985706 | 0.5962442895270748 |

The fixed branch mainly improves the BAO residual side relative to LCDM/wCDM, while SN residuals are nearly tied across the whole set.

## Gate Results

| Gate | Result | Meaning |
|---|---|---|
| data schema | pass | Pantheon+/DESI DR2 paths validated |
| convergence | pass | all models converged |
| prior edges | fail | CPL hits `wa=-2.0` |
| MTS prior edges | pass | no MTS edge flags |
| fixed branch competitiveness | mixed | beats wCDM/CPL BIC, not LCDM BIC |
| ablation tax | pass | fitted `p` and `u3` not promoted |
| stable evidence allowed | fail | status remains unstable |
| negative control | pass | `B_mem=0` returns LCDM exactly |

## What This Does and Does Not Mean

Allowed:

```text
In the repaired generic 250-SN + DESI DR2 short smoke, the fixed no-clock MTS branch remains competitive but mixed: it beats wCDM and CPL by BIC, improves chi2/AIC over LCDM, but does not beat LCDM by BIC.
```

Allowed:

```text
Fitting p or u3 is not justified by AIC/BIC here, so the fixed branch remains the disciplined branch to keep deriving around.
```

Not allowed:

```text
B_mem is derived.
MTS has stable cosmology evidence from this run.
MTS passes CMB.
MTS derives local GR.
MTS is a finished parent field theory.
```

This is a decent sparring round: no knockout, no collapse, and the ablations did not expose the fixed branch as an arbitrary tune.

## Output Files

Scoring results:

```text
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/data_schema_report.csv
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/fit_summary.csv
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/baseline_comparison.csv
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/prior_edge_table.csv
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/amplitude_policy.csv
runs/20260601-095321-cosmo-SN-BAO-short-smoke/results/residuals.csv
```

Readout results:

```text
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/source_register.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/score_readout.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/fixed_branch_comparison.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/ablation_readout.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/prior_edge_readout.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/residual_summary.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/gate_results.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/next_actions.csv
runs/20260601-000108-generic-SN-BAO-short-smoke-with-ablations-readout/results/decision.csv
```

## Next Step

Empirical branch:

```text
run the no-SH0ES shape branch next.
```

Theory branch:

```text
derive or reject the memory-stress normalization that would make B_mem=2/27 a theorem rather than a closure amplitude.
```

Recommended order:

```text
no-SH0ES short branch first,
then DESI DR1/DR2 split,
then return to the amplitude derivation with the empirical target pinned down.
```
