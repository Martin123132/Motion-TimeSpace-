# 113 - Locked 2/27 BAO-Only Runner and Score

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 112 predeclared:

```text
canonical_R_2over27_locked_amplitude
```

with:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
```

and set the first non-SN stress target:

```text
BAO-only DR1/DR2 release test.
```

This checkpoint implements the dry-run-capable runner and performs the short BAO-only score.

## 2. Short Verdict

```text
BAO_only_status =
locked_2over27_BAO_only_release_pass
```

```text
theory_promotion_allowed =
false
```

Plain English:

```text
The locked B_mem=2/27 branch survives the BAO-only DR1/DR2 release test.
```

It beats `LCDM` on BAO-only chi2/AIC/BIC in both DESI DR2 and DESI DR1, without fitting `B_mem`.

This is a good empirical discipline result. It is not a parent-action derivation.

Boxing-score version:

```text
This was a clean away round. No SN corner advice, no amplitude retune, and 2/27 still landed.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\locked_2over27_BAO_only_release_test.py
```

Dry-run:

```text
research-programme\runs\20260531-151952-locked-2over27-BAO-only-dryrun
```

Score run:

```text
research-programme\runs\20260531-151959-locked-2over27-BAO-only-score
```

Generated:

```text
bao_release_load_report.csv
model_register.csv
fit_summary.csv
prior_edge_table.csv
locked_branch_comparisons.csv
release_gates.csv
residuals.csv
decision.csv
status.json
```

## 4. Test Contract

The locked branch was:

```text
MTS_locked_2over27:
Omega_m fitted;
BAO alpha fitted analytically;
B_mem fixed at 2/27;
p fixed at 3;
u3 fixed at 1/4.
```

Baselines:

```text
LCDM
wCDM
CPL
MTS_Bmem_zero
MTS_fitted_Bmem_diagnostic
```

Important:

```text
MTS_fitted_Bmem_diagnostic is diagnostic only.
It is not the holdout branch.
```

The actual holdout branch is:

```text
B_mem frozen.
```

## 5. Data Releases

| Release | Rows | Quantities | Status |
|---|---:|---|---|
| DESI DR2 primary | 13 | `DH_over_rs`, `DM_over_rs`, `DV_over_rs` | pass |
| DESI DR1 primary | 12 | `DH_over_rs`, `DM_over_rs`, `DV_over_rs` | pass |

This is not a fully future holdout because the BAO releases were already part of the broader cosmology work. But it is SN-independent:

```text
no Pantheon shape information;
no SN nuisance offset;
no SN refit;
no B_mem refit.
```

## 6. Fit Table

| Release | Model | chi2 BAO | AIC | BIC | Edge flag |
|---|---|---:|---:|---:|---|
| DR2 | `LCDM` | 10.270745 | 14.270745 | 15.400644 | false |
| DR2 | `wCDM` | 9.040778 | 15.040778 | 16.735626 | false |
| DR2 | `CPL` | 5.859329 | 13.859329 | 16.119127 | true |
| DR2 | `MTS_locked_2over27` | 8.162376 | 12.162376 | 13.292275 | false |
| DR2 | `MTS_fitted_Bmem_diagnostic` | 7.622754 | 13.622754 | 15.317602 | false |
| DR1 | `LCDM` | 12.740353 | 16.740353 | 17.710166 | false |
| DR1 | `wCDM` | 12.704717 | 18.704717 | 20.159437 | false |
| DR1 | `CPL` | 9.969896 | 17.969896 | 19.909522 | true |
| DR1 | `MTS_locked_2over27` | 11.891979 | 15.891979 | 16.861792 | false |
| DR1 | `MTS_fitted_Bmem_diagnostic` | 11.611980 | 17.611980 | 19.066700 | false |

The only edge-hit model is baseline `CPL`, with:

```text
wa = -2
```

in both DR1 and DR2. The locked branch is edge-free.

## 7. Locked Branch Release Gates

| Release | Gate | Delta chi2 vs LCDM | Delta AIC vs LCDM | Delta BIC vs LCDM | Delta chi2 vs fitted Bmem |
|---|---|---:|---:|---:|---:|
| DESI DR2 | pass | -2.108369 | -2.108369 | -2.108369 | +0.539622 |
| DESI DR1 | pass | -0.848374 | -0.848374 | -0.848374 | +0.279999 |

Readout:

```text
DR2: locked 2/27 beats LCDM on BAO-only IC.
DR1: locked 2/27 still beats LCDM on BAO-only IC, but more weakly.
```

This preserves the earlier release pattern:

```text
DR1 softens the result,
but does not reverse it.
```

## 8. Flexible Baseline Comparisons

| Release | Reference | Delta chi2 | Delta AIC | Delta BIC | Readout |
|---|---|---:|---:|---:|---|
| DR2 | `wCDM` | -0.878401 | -2.878401 | -3.443351 | locked wins AIC/BIC |
| DR2 | `CPL` | +2.303047 | -1.696953 | -2.826852 | locked wins AIC/BIC by parsimony |
| DR2 | fitted `B_mem` diagnostic | +0.539622 | -1.460378 | -2.025327 | locked small penalty, better IC |
| DR1 | `wCDM` | -0.812738 | -2.812738 | -3.297644 | locked wins AIC/BIC |
| DR1 | `CPL` | +1.922083 | -2.077917 | -3.047730 | locked wins AIC/BIC by parsimony |
| DR1 | fitted `B_mem` diagnostic | +0.279999 | -1.720001 | -2.204907 | locked small penalty, better IC |

This is the useful part:

```text
the fitted-amplitude diagnostic improves raw chi2,
but the locked branch wins AIC/BIC because it does not spend the amplitude parameter.
```

That is exactly the discipline we needed.

## 9. Interpretation

Allowed statement:

```text
The predeclared locked branch B_mem=2/27 survives a BAO-only DR1/DR2 release stress test and remains competitive without SN shape information or amplitude refitting.
```

Forbidden statement:

```text
MTS predicts BAO from first principles.
```

Reason:

```text
the background form, endpoint amplitude, and perturbation theory are still closure-level.
```

Also forbidden:

```text
BAO-only success proves the unified field theory.
```

This result upgrades empirical seriousness, not derivational status.

## 10. Gate Results

| Gate | Result |
|---|---|
| BAO DR1/DR2 data load | pass |
| dry-run before score | pass |
| `B_mem=2/27` frozen | pass |
| same BAO rows/covariances for baselines and MTS | pass |
| locked branch edge-free | pass |
| DR2 release gate | pass |
| DR1 release gate | pass |
| theory promotion | fail |

## 11. Decision

Decision:

```text
locked_2over27_BAO_only =
release_pass
```

Decision:

```text
empirical_status =
stronger_than_SN_BAO_only_because_SN_removed_for_this_stress
```

Decision:

```text
theory_status =
unchanged_not_parent_derived
```

Decision:

```text
next_action =
CMB_distance_prior_locked_2over27_dry_run
```

## 12. Next Target

Create:

```text
114-locked-2over27-CMB-distance-dryrun.md
```

Purpose:

```text
prepare a dry-run-only CMB distance-prior test for the locked branch.
```

Important:

```text
Do not fit B_mem.
Do not use CMB calibration freedom not given to baselines.
Do not claim perturbation-level success from a distance-prior smoke test.
```

Pass condition:

```text
data paths, covariance, model assumptions, nuisance/calibration handling, and output contracts are validated before scoring.
```
