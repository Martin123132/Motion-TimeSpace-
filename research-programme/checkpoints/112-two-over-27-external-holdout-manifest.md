# 112 - Two-Over-27 External Holdout Manifest

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 111 found:

```text
U(R)=9R^3-6R^2+R
```

can formally generate:

```text
27R^2 - 12R + 1 = 0
```

but the coefficients and endpoint arrow are not parent-derived.

So the honest next move is empirical discipline:

```text
freeze B_mem = 2/27 before external tests.
```

No more letting the amplitude float while asking whether the branch is real.

## 2. Short Verdict

```text
holdout_status =
Bmem_2over27_predeclared_for_external_holdouts
```

```text
theory_promotion_allowed =
false
```

Plain English:

```text
The locked branch is now formally predeclared for future external holdouts.
```

That means:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
eta = 1
a_F = 1
```

are frozen before scoring.

Boxing-score version:

```text
No moving the feet after the bell. If 2/27 is real, it has to dance under the lights without changing shoes.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\two_over_27_external_holdout_manifest.py
```

Run:

```text
research-programme\runs\20260531-151317-two-over-27-external-holdout-manifest
```

Generated:

```text
source_register.csv
frozen_branch_register.csv
holdout_queue.csv
discipline_gates.csv
command_templates.csv
decision.csv
status.json
```

Status:

```text
Bmem_2over27_predeclared_for_external_holdouts
```

## 4. Frozen Branch Register

| Branch | `p` | `u3` | `DeltaR` | `B_mem` | `eta` | `a_F` | Fit status |
|---|---:|---:|---:|---:|---:|---:|---|
| `canonical_R_2over27_locked_amplitude` | 3 | 0.25 | 2/9 | 2/27 | 1 | 1 | `B_mem_frozen_not_fitted` |

Claim ceiling:

```text
predeclared_empirical_holdout_branch_not_theory_prediction
```

## 5. Holdout Queue

| Holdout | Role | Rule | Priority |
|---|---|---|---:|
| CMB distance prior | external background distance | `B_mem` fixed at `2/27`; no calibration rescue not given to baselines | 1 |
| growth `fσ8` | structure growth | background fixed; perturbation/growth response predeclared before scoring | 2 |
| BAO-only DR1/DR2 release | SN-independent distance stress | no SN refit; DR1 and DR2 both reported | 3 |
| Pantheon split rechecks | robustness, not true holdout | fixed amplitude; same split masks for every model | 4 |
| future non-SN cosmology | true future validation | `B_mem=2/27` frozen before data ingestion | 5 |

The important distinction:

```text
Pantheon split rechecks are useful debugging;
CMB/growth/BAO-only/future data are the real holdout pressure.
```

## 6. Discipline Gates

| Gate | Requirement |
|---|---|
| amplitude freeze | `B_mem` must equal `2/27` in every holdout score |
| same baseline data | baselines and MTS use identical rows, covariance, nuisance assumptions, and release labels |
| no theory promotion | holdout success can upgrade empirical status, not parent-action derivation |
| edge and failure reporting | prior-edge and convergence failures reported symmetrically |
| predeclared growth response | growth/CMB perturbation response fixed before scoring |

Any failure gets labelled before interpretation:

```text
amplitude_unfrozen_invalidates_holdout
baseline_asymmetry_invalidates_scorecard
overclaim_invalidates_interpretation
hidden_instability_invalidates_scorecard
growth_rescue_knob_invalidates_holdout
```

## 7. Implementation Notes

The existing SN+BAO runner does not yet expose:

```text
--locked-B-mem
```

So the next coding target is not a long run. It is a dry-run-capable locked-branch runner.

Command templates were written as design targets:

```text
scripts/locked_2over27_CMB_growth_holdout.py --dry-run
scripts/locked_2over27_BAO_only_release_test.py --dry-run
```

They must write:

```text
runs/<timestamp>/run_config.json
runs/<timestamp>/results/*.csv
runs/<timestamp>/status.json
```

and must not sit watching a long computation.

## 8. Claim Ceiling

Allowed:

```text
B_mem=2/27 is now a predeclared locked empirical branch for external holdout testing.
```

Forbidden:

```text
MTS predicts B_mem=2/27.
```

Reason:

```text
the parent action still has not derived the endpoint quadratic, coefficients, charge unit, or endpoint arrow.
```

## 9. Decision

Decision:

```text
frozen_branch =
canonical_R_2over27_locked_amplitude
```

Decision:

```text
locked_B_mem =
2/27
```

Decision:

```text
locked_DeltaR =
2/9
```

Decision:

```text
next_action =
implement_dry_run_locked_2over27_CMB_or_BAO_only_runner
```

## 10. Next Target

Create:

```text
113-locked-2over27-runner-dryrun-design.md
```

Purpose:

```text
design the first dry-run-only runner for locked B_mem=2/27 external testing.
```

Recommended first target:

```text
BAO-only DR1/DR2
```

Reason:

```text
it is closest to the existing SN+BAO machinery,
does not need perturbation theory,
and tests whether the locked amplitude survives without SN shape information.
```

After that:

```text
CMB distance/growth.
```
