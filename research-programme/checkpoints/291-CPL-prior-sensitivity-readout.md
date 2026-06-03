# 291 - CPL Prior Sensitivity Readout

Private empirical robustness checkpoint. This is not a public cosmology, CMB, local-GR, or parent-field-theory claim.

## Purpose

Checkpoint 290 showed:

```text
DESI DR1/DR2 no-SH0ES release split is qualitatively survived,
but CPL hits a prior edge in both releases.
```

That made the baseline comparison too muddy for stronger language.

This checkpoint tests:

```text
is the CPL edge just a too-narrow wa box,
or does the baseline keep running into edge/pathology under wider freedom?
```

## Runner Patch

Patched:

```text
scripts/cosmo_SN_BAO_closure_runner.py
```

Change:

```text
added --cpl-w0-lower and --cpl-w0-upper
```

so CPL prior sensitivity can test:

```text
w0 and wa together,
not only wa.
```

This matters because the first `wa`-only widening moved the edge from:

```text
wa = -2
```

to:

```text
w0 = -0.2.
```

## Machine Artifacts

wa-wide runs:

```text
runs/20260601-102601-cosmo-SN-BAO-short-smoke
runs/20260601-102620-cosmo-SN-BAO-short-smoke
```

w0+wa-wide runs:

```text
runs/20260601-102748-cosmo-SN-BAO-short-smoke
runs/20260601-102803-cosmo-SN-BAO-short-smoke
```

Readout script:

```text
scripts/CPL_prior_sensitivity_readout.py
```

Readout run:

```text
runs/20260601-000114-CPL-prior-sensitivity-readout
```

Status:

```text
CPL_prior_sensitivity_reveals_baseline_edge_migration_DR2_clean_DR1_still_edge
```

Claim ceiling:

```text
baseline_prior_sensitivity_diagnostic_only_no_stable_evidence_or_parent_promotion
```

## Edge Migration

Default CPL prior:

```text
w0 in [-2, -0.2]
wa in [-2, 2]
```

Wide `wa` only:

```text
w0 in [-2, -0.2]
wa in [-5, 5]
```

Wide `w0 + wa` box:

```text
w0 in [-3, 1]
wa in [-5, 5]
```

Edge readout:

| Release | Prior box | CPL edge |
|---|---|---|
| DR2 | default | `wa=-2` |
| DR1 | default | `wa=-2` |
| DR2 | wide `wa` only | `w0=-0.2` |
| DR1 | wide `wa` only | `w0=-0.2` |
| DR2 | wide `w0+wa` | none |
| DR1 | wide `w0+wa` | `wa=-5` |

So:

```text
DR2 CPL can be made edge-free with a wider CPL box.
DR1 CPL still wants to run to an edge.
```

That is an important baseline diagnostic.

## CPL Score Sensitivity

Relative to default CPL:

| Release | Wider prior | CPL delta chi2 |
|---|---|---:|
| DR2 | wide `wa` only | -0.19739917696026055 |
| DR2 | wide `w0+wa` | -0.19739994265961514 |
| DR1 | wide `wa` only | -0.844181638077032 |
| DR1 | wide `w0+wa` | -1.9599596604100498 |

So the DR1 CPL baseline is much more prior-sensitive than DR2 in this short-smoke setup.

## Fixed MTS vs CPL

| Release | Prior box | delta chi2 | delta AIC | delta BIC |
|---|---|---:|---:|---:|
| DR2 | default | 1.6462134456770627 | -0.35378655432293726 | -3.925940586500701 |
| DR2 | wide `w0+wa` | 1.8436133883366779 | -0.15638661166332213 | -3.728540643841086 |
| DR1 | default | 1.5383962700390157 | -0.4616037299609843 | -4.029948233722081 |
| DR1 | wide `w0+wa` | 3.4983559304490655 | 1.4983559304490655 | -2.069988573312031 |

Interpretation:

```text
DR2: MTS still beats CPL by AIC/BIC when CPL is edge-free, but CPL has better raw chi2.
DR1: MTS still beats CPL by BIC, but loses AIC and raw chi2; CPL still edge-hits wa=-5.
```

So the honest statement is:

```text
MTS remains BIC-competitive against flexible CPL,
but the CPL baseline is prior-sensitive and DR1 remains unstable.
```

This is not a clean win.

It is not a collapse either.

## Other Comparisons

Changing CPL priors does not change MTS vs LCDM or MTS vs wCDM because those fits are unchanged.

From checkpoint 290:

```text
DR2 vs LCDM: MTS improves chi2/AIC but loses BIC by about 2.93.
DR1 vs LCDM: MTS improves chi2 but loses AIC/BIC, with BIC gap about 4.44.
DR1/DR2 vs wCDM: MTS still beats wCDM by chi2/AIC/BIC.
```

That remains the fair global short-smoke readout.

## Gates

| Gate | Result | Meaning |
|---|---|---|
| runner supports CPL `w0` override | pass | prior sensitivity can be tested |
| DR2 full CPL box edge-free | pass | DR2 CPL comparison cleaner |
| DR1 full CPL box edge-free | fail | DR1 still hits `wa=-5` |
| MTS edges all prior boxes | pass | no MTS edge flags |
| MTS vs CPL DR2 full box | pass mixed | MTS wins AIC/BIC, raw chi2 worse |
| MTS vs CPL DR1 full box | unstable mixed | MTS wins BIC only; CPL edge remains |
| stable evidence allowed | fail | diagnostic only |

## Decision

Decision:

```text
CPL_prior_sensitivity_reveals_baseline_edge_migration_DR2_clean_DR1_still_edge
```

Meaning:

```text
the baseline edge was real, not a harmless formatting issue.
```

DR2 can be cleaned by widening CPL priors:

```text
MTS still wins AIC/BIC against CPL there.
```

DR1 remains unstable:

```text
CPL runs to wa=-5,
and the MTS advantage against CPL weakens to BIC-only.
```

What improves:

```text
the scorecard is fairer and more symmetric.
```

What does not improve:

```text
no stable cosmology evidence claim is allowed.
```

Boxing-score version:

```text
We let CPL swing with a longer reach.
In DR2, it stopped grabbing the ropes and MTS still nicked the cards on AIC/BIC.
In DR1, CPL sprinted to the far rope again and made the round messy.
Good diagnostic. Not a title belt.
```

## Output Files

```text
runs/20260601-000114-CPL-prior-sensitivity-readout/results/source_register.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/score_readout.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/fixed_branch_comparison.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/CPL_edge_migration.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/CPL_score_sensitivity.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/MTS_fixed_vs_CPL_shift.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/gate_results.csv
runs/20260601-000114-CPL-prior-sensitivity-readout/results/decision.csv
```

## Next Step

The short-smoke scorecard is now disciplined enough to stop squeezing this tiny 250-SN branch.

Recommended next:

```text
move to a stronger evidence mode:
full-sample/full-covariance if runtime permits,
or a non-SN holdout/radial/growth branch if we want a faster independent check.
```

Near-term best:

```text
non-SN holdout first if time/tokens are tight,
full covariance when we are ready to let a longer run go.
```
