# 110 - Endpoint Charge Equation Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 109 found:

```text
DeltaR = 2/9
B_mem = 2/27
```

is a strong locked empirical target, but not derived.

This checkpoint asks whether the target can be sharpened into an endpoint equation rather than just a number.

## 2. Short Verdict

```text
endpoint_charge_status =
exact_endpoint_quadratic_target_found_not_derived
```

```text
promotion_allowed =
false
```

Plain English:

```text
There is now a very sharp endpoint equation target:
27 R^2 - 12 R + 1 = 0.
```

Its roots are:

```text
R_today = 1/9
R_early = 1/3
DeltaR = 2/9
B_mem = DeltaR/3 = 2/27
```

This is not a parent-action derivation yet. But it is a cleaner theorem target than the previous loose boundary-charge language.

Boxing-score version:

```text
We have not won the title. But now we know the exact punch we need to train: make the parent action throw 27R^2 - 12R + 1 = 0 without us taping the number to its glove.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\endpoint_charge_equation_attempt.py
```

Run:

```text
research-programme\runs\20260531-150750-endpoint-charge-equation-attempt
```

Generated:

```text
source_register.csv
endpoint_equation_candidates.csv
derivation_chain.csv
no_go_shortcuts.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
endpoint_quadratic_target_found_not_derived
```

## 4. Best Endpoint Equation

The best exact target is:

```text
27 R^2 - 12 R + 1 = 0
```

or:

```text
3^3 R^2 - (3 x 4) R + 1 = 0.
```

The coefficient interpretation is:

| Coefficient | Candidate owner | Status |
|---:|---|---|
| `27 = 3^3` | spatial determinant route behind `p=3` | conditional, not action-derived |
| `12 = 3 x 4` | spatial trace times 3+1 cell normalization behind `u3=1/4` | conditional, not action-derived |
| `1` | unit normalized boundary charge | missing `Q_*` theorem |

The roots are:

```text
R = (12 +/- 6) / 54
```

so:

```text
R_low = 1/9
R_high = 1/3
DeltaR = R_high - R_low = 2/9.
```

Then, on the current locked branch:

```text
eta = 1
a_F = 1
B_mem = DeltaR / 3 = 2/27.
```

## 5. Why This Is Better Than the Previous Shortcut

Checkpoint 109 had the tempting route:

```text
(2/3)(1/3) = 2/9.
```

That is too weak by itself because degree-counting is not charge dynamics.

The new target is better:

```text
endpoint stationarity equation -> two endpoint roots -> DeltaR.
```

It turns the amplitude problem into:

```text
derive an endpoint Euler equation for R.
```

That is a real field-theory-shaped problem.

## 6. Candidate Equation Ledger

| Candidate | Equation | Result |
|---|---|---|
| spatial-cell endpoint quadratic | `27R^2 - 12R + 1 = 0` | best exact theorem target, not derived |
| trace-square endpoint pair | `R_high=1/3`, `R_low=(1/3)^2` | equivalent schema, not variational |
| relative degree product | `DeltaR=(2/3)(1/3)` | motivation only |
| built-to-order polynomial | `(R-1/9)(R-1/3)=0` | rejected as circular if roots are inserted by hand |

The difference matters:

```text
If the parent action derives the coefficient structure 3^3 and 3x4, this becomes theory.
If we merely write the roots by hand, it remains numerology.
```

## 7. Derivation Chain Status

| Step | Statement | Status |
|---:|---|---|
| 1 | Let `R=Q_boundary/Q_*` be the normalized endpoint charge entering `Gamma_eff` | required, not derived |
| 2 | Use `p=3` as the spatial determinant coefficient `3^3` | conditional from prior branch |
| 3 | Use `u3=1/4` as the 3+1 cell coefficient `4` | conditional from prior branch |
| 4 | Require endpoint stationarity to produce `3^3 R^2 - 3*4 R + 1 = 0` | new theorem target |
| 5 | Roots become `R_today=1/9`, `R_early=1/3` | mathematical consequence if step 4 holds |
| 6 | `DeltaR=2/9`, `B_mem=2/27` | mathematical consequence if parent contract holds |

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `exact_endpoint_equation_found` | pass as target | quadratic gives roots `1/9` and `1/3` |
| `coefficients_reuse_existing_branch_numbers` | pass conditional | `27=3^3`, `12=3x4` reuse existing `p/u3` structural numbers |
| `endpoint_equation_parent_derived` | fail | no action variation currently yields the quadratic |
| `Qstar_charge_unit_derived` | fail | normalized charge unit remains missing |
| `post_fit_circularity_removed` | fail | equation was sought after `2/27` succeeded |
| `empirical_branch_upgrade` | pass | `2/27` can be named as a predeclared locked-amplitude branch |
| `support_claim_allowed` | fail | exact target is not an action theorem |

## 9. No-Go Rules

Rejected:

```text
write a polynomial with desired roots and call it a derivation.
```

Rejected:

```text
derive 2/9 from form-degree counting alone.
```

Rejected:

```text
reuse C_coh inside a parent action as if checkpoint 80 did not demote that route.
```

Rejected:

```text
fit endpoint roots branch by branch.
```

These rules keep the new nice number from becoming a trap.

## 10. Current Standing

The branch is now:

```text
canonical_R_2over27_locked_amplitude
```

with the exact theorem target:

```text
R endpoint equation:
27R^2 - 12R + 1 = 0.
```

Status:

```text
empirically strong;
mathematically sharpened;
not parent-derived.
```

This is much better than a free amplitude. It is still not a unified field theory.

## 11. Decision

Decision:

```text
endpoint_equation_status =
target_found_not_derived
```

Decision:

```text
best_equation_target =
27 R^2 - 12 R + 1 = 0
```

Decision:

```text
root_pair =
R_today = 1/9,
R_early = 1/3
```

Decision:

```text
locked_amplitude =
B_mem = 2/27
```

## 12. Next Target

There are two honest next moves:

```text
Route A:
try to build a parent variational term that yields
27R^2 - 12R + 1 = 0
without inserting the roots by hand.
```

or:

```text
Route B:
predeclare B_mem=2/27 as a frozen branch for external CMB/growth/BAO holdouts.
```

Recommendation:

```text
Route A once.
```

Pass condition:

```text
The coefficient structure 3^3 and 3x4 follows from the parent action, normalized charge, and trace/cell projection.
```

Fail condition:

```text
The equation can only be written by choosing a potential to match the target roots.
```
