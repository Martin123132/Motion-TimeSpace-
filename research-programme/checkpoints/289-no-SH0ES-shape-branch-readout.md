# 289 - no-SH0ES Shape Branch Readout

Private empirical robustness checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 285 found the generic 250-SN + DESI DR2 branch was:

```text
competitive but mixed,
with the fixed MTS branch beating wCDM/CPL by BIC but not LCDM by BIC.
```

This checkpoint tests whether that pattern depends on the local-H0 / SH0ES-style calibrated distance-modulus column.

The no-SH0ES branch uses:

```text
SN observable: m_b_corr
SN nuisance: analytic offset fitted symmetrically for every model
calibrators: excluded
BAO: DESI DR2 unchanged
SN rows: first 250 selected rows
```

So the test is:

```text
does the fixed branch survive when the SN side is shape + nuisance offset only?
```

## Machine Artifacts

Dry run:

```text
runs/20260601-101526-cosmo-SN-BAO-closure-dryrun
```

Scoring run:

```text
runs/20260601-101537-cosmo-SN-BAO-short-smoke
```

Readout script:

```text
scripts/no_SH0ES_shape_branch_readout.py
```

Readout run:

```text
runs/20260601-000112-no-SH0ES-shape-branch-readout
```

Status:

```text
no_SH0ES_shape_branch_pattern_survives_but_stable_evidence_blocked_by_CPL_edge
```

Claim ceiling:

```text
SN_BAO_no_SH0ES_shape_short_smoke_only_no_stable_evidence_or_parent_promotion
```

## Core Result

The no-SH0ES branch preserves the same qualitative pattern as checkpoint 285.

| Model | chi2 | AIC | BIC | Edge flag |
|---|---:|---:|---:|---|
| LCDM | 131.5009550908185 | 137.5009550908185 | 148.2174171873518 | false |
| wCDM | 130.2836741623527 | 138.2836741623527 | 152.57229029106375 | false |
| CPL | 127.20909790995228 | 137.20909790995228 | 155.0698680708411 | true |
| MTS fixed `p=3, u3=1/4` | 128.85531135562934 | 136.85531135562934 | 151.1439274843404 | false |
| MTS `B_mem=0` | 131.5009550908185 | 137.5009550908185 | 148.2174171873518 | false |
| MTS fitted `p` | 128.8390623386259 | 138.8390623386259 | 156.6998324995147 | false |
| MTS fitted `u3` | 128.60829573815718 | 138.60829573815718 | 156.469065899046 | false |

Important:

```text
the only prior-edge flag is CPL wa = -2.0.
no MTS branch hits a prior edge.
```

So this is not stable evidence, but it is a useful robustness result.

## Fixed Branch Comparisons

Against LCDM:

```text
delta_chi2 = -2.645643735189168
delta_AIC  = -0.645643735189168
delta_BIC  =  2.926510296988596
```

Interpretation:

```text
MTS improves raw chi2 and AIC, but loses BIC to LCDM.
```

Against wCDM:

```text
delta_chi2 = -1.4283628067233565
delta_AIC  = -1.4283628067233565
delta_BIC  = -1.4283628067233565
```

Interpretation:

```text
MTS beats wCDM on raw chi2, AIC, and BIC.
```

Against CPL:

```text
delta_chi2 =  1.6462134456770627
delta_AIC  = -0.35378655432293726
delta_BIC  = -3.925940586500701
```

Interpretation:

```text
CPL has lower raw chi2, but MTS wins AIC/BIC because CPL pays parameter tax.
This comparison is unstable because CPL hits the wa prior edge.
```

## Pressure Comparison

Switching from `MU_SH0ES` to `m_b_corr` with a nuisance offset barely changes the fixed-branch comparison pattern.

| Baseline | Pressure `delta_BIC` | no-SH0ES `delta_BIC` | Shift |
|---|---:|---:|---:|
| LCDM | 2.926542374532005 | 2.926510296988596 | -0.000032077543409 |
| wCDM | -1.4284562012850586 | -1.4283628067233565 | 0.000093394561702 |
| CPL | -3.9265438799764922 | -3.925940586500701 | 0.000603293475791 |

So the pattern is not being driven by the `MU_SH0ES` column in this short-smoke setup.

This is good news for robustness:

```text
the fixed branch did not collapse when local-calibration pressure was removed.
```

But the result is still:

```text
mixed, not stable evidence.
```

## Ablation Readout

The fitted-shape ablations still do not justify their extra freedom:

| Ablation | delta chi2 vs fixed | delta AIC vs fixed | delta BIC vs fixed | Status |
|---|---:|---:|---:|---|
| MTS fitted `p` | -0.016249017003445942 | 1.983750982996554 | 5.555905015174318 | not promoted |
| MTS fitted `u3` | -0.24701561747215806 | 1.752984382527842 | 5.325138414705606 | not promoted |
| MTS `B_mem=0` | 2.645643735189168 | 0.645643735189168 | -2.926510296988596 | LCDM-limit negative control |

So:

```text
freeing p or u3 still buys small raw chi2 improvements but loses information criteria.
```

## Residual Diagnostics

| Model | SN RMS | BAO RMS | BAO max abs |
|---|---:|---:|---:|
| LCDM | 0.22727727217832216 | 0.304790120735797 | 0.6057532918378783 |
| wCDM | 0.227314178072089 | 0.2791456857078921 | 0.6061638199892379 |
| CPL | 0.2275730438108063 | 0.2137409022624065 | 0.5631697925638832 |
| MTS fixed `p=3, u3=1/4` | 0.22728500597833926 | 0.24147565450034292 | 0.6024259007106956 |
| MTS `B_mem=0` | 0.22727727217832216 | 0.304790120735797 | 0.6057532918378783 |
| MTS fitted `p` | 0.22728712794957054 | 0.24180697753168456 | 0.6029241527866027 |
| MTS fitted `u3` | 0.22731806419225295 | 0.23332213412920846 | 0.5962441097369187 |

Again the movement is mostly BAO-side; SN residuals are close across all models.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| dry-run schema | pass | no-SH0ES inputs validated before scoring |
| no-SH0ES mode | pass | `sn_observable=mb-corr`, calibrators excluded |
| convergence | pass | all models converged |
| prior edges | fail | CPL hits `wa=-2.0` |
| MTS prior edges | pass | no MTS branch edge-hit |
| fixed branch competitiveness | mixed | beats wCDM/CPL BIC, not LCDM BIC |
| calibration pressure shift | pass | pattern shift is tiny |
| ablation tax | pass | fitted `p/u3` not promoted |
| stable evidence allowed | fail | diagnostic only |

## What This Does and Does Not Mean

Allowed:

```text
The fixed no-clock shape branch survives the no-SH0ES 250-SN + DESI DR2 short-smoke qualitatively.
```

Allowed:

```text
The preference pattern is essentially unchanged when switching from MU_SH0ES to m_b_corr with a nuisance offset.
```

Not allowed:

```text
MTS has stable cosmology evidence.
B_mem is derived.
MTS passes CMB.
MTS derives local GR.
MTS is a finished parent field theory.
```

Boxing-score version:

```text
We took away the local-H0 shove and the fixed branch stayed on its feet.
It still does not win every judge's card, but it did not need SH0ES pressure to keep moving.
```

## Output Files

Scoring results:

```text
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/data_schema_report.csv
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/fit_summary.csv
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/baseline_comparison.csv
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/prior_edge_table.csv
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/amplitude_policy.csv
runs/20260601-101537-cosmo-SN-BAO-short-smoke/results/residuals.csv
```

Readout results:

```text
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/source_register.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/score_readout.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/fixed_branch_comparison.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/pressure_vs_noSH0ES_scores.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/pressure_vs_noSH0ES_fixed_branch_deltas.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/ablation_readout.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/prior_edge_readout.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/residual_summary.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/gate_results.csv
runs/20260601-000112-no-SH0ES-shape-branch-readout/results/decision.csv
```

## Next Step

Run:

```text
DESI DR1 vs DR2 fixed-branch robustness.
```

Purpose:

```text
test whether the same no-SH0ES/fixed-shape pattern survives BAO release changes.
```
