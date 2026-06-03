# 156 - Clock Projection Functional Theorem Or Demotion

Private theorem-target checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 155 said the BAO clock/projection route had one clean demand:

```text
derive a signed observer/coframe/domain-boundary scalar C_clock[Q_coh,D],
or demote the projection route to closure-only.
```

The obvious locked memory shapes failed because they were single-signed or saturated. The danger was that the BAO projection route would become:

```text
fit zeta(z), call it physics.
```

This checkpoint tests whether there is a more structural signed functional.

Short answer:

```text
do not demote yet.
```

A specific cell-balanced clock functional was identified:

```text
Theta_clock = B_mem * (1/24) * X_D * F_D * (1 - X_D/4).
```

It is not derived from an action yet. But it is no longer just a polynomial redshift closure. It is a precise theorem target.

## 2. Machine Artifact

Script:

```text
scripts/clock_projection_functional_theorem_or_demotion.py
```

Run:

```text
runs/20260531-235959-clock-projection-functional-theorem-or-demotion
```

Generated:

```text
source_register.csv
cell_clock_functional_contract.csv
cell_balance_candidate_scorecard.csv
cell_balance_predictions.csv
comparator_scorecard.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
cell_balanced_clock_functional_identified_as_theorem_target_not_parent_derived
```

Claim ceiling:

```text
cell_balanced_clock_functional_theorem_target_not_field_theory_promotion
```

## 3. Candidate Functional

Define the coherent domain load:

```text
X_D = (1/u3) integral P_coh[Theta] d tau.
```

On FLRW:

```text
X_D = N/u3.
```

Use the retained determinant-memory activation:

```text
F_D = 1 - exp(-X_D^3).
```

The new signed clock candidate is:

```text
Theta_clock = B_mem * kappa_4 * X_D * F_D * (1 - X_D/4),
```

with:

```text
kappa_4 = 1/24.
```

Interpretation:

```text
X_D        = coherent load;
F_D        = memory exposure activation;
1-X_D/4    = 3+1 cell-balance sign factor;
1/24       = four-form / oriented-cell combinatorial scale target.
```

The sign crossing now has a structural place:

```text
X_D = 4.
```

If `u3 = 1/4`, this is:

```text
N = 1.
```

That matters because the sign change is no longer chosen as an arbitrary BAO crossing redshift. It is tied to the same 3+1 cell language already used in the `u3 = 1/4` candidate.

## 4. Numerical Result

Primary candidate:

```text
Theta_clock = B_mem * (1/24) * X_D * F_D * (1 - X_D/4),
X_D = N/u3,
u3 = 0.2429466120286312.
```

Machine score:

```text
RMS theta residual     = 0.00020904931393610123
max abs theta residual = 0.0003119383426994998
sign matches           = 6/6
```

The fitted scale wanted by the same shape is:

```text
kappa_fit = 0.0423308397893
```

Structural candidate:

```text
1/24 = 0.0416666666667
```

Fractional difference:

```text
0.0159401549424
```

That is a real clue. It is close enough to be worth attacking as a theorem, not close enough to call a derivation.

## 5. Quarter Branch

Fully structural version:

```text
u3 = 1/4,
kappa_4 = 1/24.
```

Machine score:

```text
RMS theta residual     = 0.00045105058457094795
max abs theta residual = 0.0007252665780135815
sign matches           = 6/6
zero crossing          = N = 1
```

This is weaker than the fitted-`u3` version, but still sign-correct and not embarrassing.

Readout:

```text
the fixed-quarter branch survives as a rough theorem target.
```

It must be tested directly. We cannot quietly use fitted `u3` forever if the theory wants `u3=1/4`.

## 6. Comparator Scorecard

| model | RMS theta residual | max residual | sign matches | status |
|---|---:|---:|---:|---|
| best previous locked memory shape | 0.002310660545127938 | 0.0037397117654248964 | 3/6 | fail_sign_structure |
| affine redshift closure | 0.0007235770095008313 | 0.0009748974723691466 | 5/6 | fail_sign_structure |
| quadratic redshift closure | 0.000039642300236917174 | 0.00004812631199293312 | 6/6 | fit_shape_but_unowned |
| cell balance, fitted `u3`, fixed `1/24` | 0.00020904931393610123 | 0.0003119383426994998 | 6/6 | strong_theorem_target_not_derived |
| cell balance, `u3=1/4`, fixed `1/24` | 0.00045105058457094795 | 0.0007252665780135815 | 6/6 | viable_theorem_target_not_derived |

The quadratic closure still fits best numerically. That is expected because it is a free shape.

The important point is different:

```text
the cell-balanced functional has a physical grammar and fixed structural constants,
yet still lands near the required target.
```

That is the Mayweather route: not a haymaker, but clean enough to keep scoring.

## 7. Theorem Contract

For this to become physics, a parent action must derive every term:

| object | required parent meaning | current status |
|---|---|---|
| `X_D` | coherent domain load from `P_coh[Theta]` | conditional from prior work |
| `F_D` | determinant memory exposure `1-exp(-X_D^3)` | contract identified, action missing |
| `1-X_D/4` | signed 3+1 cell-balance boundary factor | new theorem target |
| `1/24` | four-form / oriented-cell combinatorial scale | numerically close, not derived |
| `Theta_clock` | physical clock map, not gauge lapse | candidate contract only |
| matter-clock coupling | makes redshift calibration observable | missing |

The no-smuggling version of the theorem is:

```text
the parent observer/coframe action must produce
Theta_clock = B_mem * (1/24) * X_D * F_D * (1 - X_D/4)
before looking at BAO residuals.
```

If the factor `(1-X_D/4)` or `1/24` is chosen after fitting the BAO table, the route demotes.

## 8. Gates

Machine gate result:

| gate | status | evidence |
|---|---|---|
| source paths | pass | all cited artifacts exist |
| signed shape without polynomial closure | pass_theorem_target | fixed candidate gives 6/6 signs |
| structural amplitude lock | pass_clue_not_derivation | `kappa_fit` is 1.594% from `1/24` |
| fixed quarter branch | pass_rough_theorem_target | sign-correct, rougher |
| parent action / observer coupling | fail_missing | no action variation yet |
| gauge safety | fail_missing | must not be removable lapse |
| local silence | pass_conditional | if `X_D=0`, then `Theta_clock=0` |
| empirical retest | open | BAO/SN/H(z)/CMB not rerun with fixed map |
| demotion decision | do_not_demote_yet | specific theorem target exists |
| promotion | fail | no field-theory promotion |

## 9. Decision

Current fair status:

```text
cell_balanced_clock_functional_identified_as_theorem_target_not_parent_derived
```

Meaning:

```text
projection is not demoted today;
the route has gained a precise signed functional;
the functional is not yet derived from a parent action;
the redshift/clock map is not yet proven physical rather than gauge;
no public support claim is allowed.
```

This is a better result than expected from checkpoint 155. The previous state was:

```text
we need a signed clock scalar.
```

The current state is:

```text
we have a compact candidate signed clock scalar,
with structural constants that are close to the target.
```

That is progress. It is not victory.

## 10. Next Target

Next checkpoint:

```text
157-cell-balanced-clock-map-fixed-branch-retest.md
```

Task:

```text
run the fixed cell-balanced clock map as a deterministic branch through BAO/SN/H(z),
with both fitted-u3 and u3=1/4 variants,
and compare against the existing baselines without giving it extra fitted redshift freedom.
```

Acceptance logic:

```text
if it helps BAO but breaks SN/H(z), demote;
if it holds BAO/SN/H(z) competitively, keep it as the leading bridge theorem target;
if it only works with refitted kappa or redshift-polynomial freedom, demote to closure.
```

The boxer’s-card version:

```text
MTS did not win the title here,
but it landed a clean counterpunch.
Now we test whether it can stay on its feet for the next round.
```
