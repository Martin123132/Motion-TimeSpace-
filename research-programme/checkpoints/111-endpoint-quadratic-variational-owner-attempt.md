# 111 - Endpoint Quadratic Variational Owner Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 110 found the exact endpoint target:

```text
27 R^2 - 12 R + 1 = 0
```

with roots:

```text
R_today = 1/9
R_early = 1/3
DeltaR = 2/9
B_mem = 2/27
```

This checkpoint asks whether a parent variational term can produce that endpoint equation rather than merely naming it.

## 2. Short Verdict

```text
variational_owner_status =
formal_term_written_but_not_parent_derived
```

```text
promotion_allowed =
false
```

Plain English:

```text
We can write a clean variational term whose Euler equation is the endpoint quadratic, but we cannot yet derive its coefficients or endpoint arrow from the parent theory.
```

That means the amplitude target is sharper, but still not promoted.

Boxing-score version:

```text
We found the combination. We have not proved the boxer learned it naturally; right now it still looks coached.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\endpoint_quadratic_variational_owner_attempt.py
```

Run:

```text
research-programme\runs\20260531-151049-endpoint-quadratic-variational-owner-attempt
```

Generated:

```text
source_register.csv
action_candidates.csv
stability_table.csv
endpoint_arrow_options.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
variational_owner_written_but_not_parent_derived
```

## 4. Formal Term

The cleanest formal potential is:

```text
U(R) = 9R^3 - 6R^2 + R.
```

Its variation gives:

```text
dU/dR = 27R^2 - 12R + 1.
```

So the endpoint equation:

```text
dU/dR = 0
```

has exactly the desired roots:

```text
R = 1/9
R = 1/3.
```

The coefficient story would be:

```text
9R^3      determinant-like cubic endpoint energy
-6R^2     trace-cell quadratic exchange
+R        unit normalized charge source
```

But that is an interpretation, not a derivation.

## 5. Candidate Action Ledger

| Candidate | Term | Result | Failure mode |
|---|---|---|---|
| determinant-trace-cell potential | `U(R)=9R^3-6R^2+R` | best writeable owner, not derived | coefficients arranged to match target |
| Lagrange multiplier endpoint constraint | `Lambda(27R^2-12R+1)` | rejected as derivation | constraint simply imposes the result |
| Ward-identity generated potential | unknown Ward-fixed determinant/trace functional | best future route | identity unavailable |
| relative charge pairing action | `<J_rel,J_rel>_Q + boundary pairing` | conditional only | charge metric, `Q_*`, and representative not derived |

This is useful because it blocks the cheap move:

```text
just add a multiplier and call it physics.
```

No. That would be the same fitted amplitude wearing a judge's robe.

## 6. Stability and Arrow Problem

For:

```text
U(R)=9R^3-6R^2+R
```

the curvature is:

```text
U''(R)=54R-12.
```

So:

| Root | `R` | `U''` | Role for standard relaxation down `U` |
|---|---:|---:|---|
| today candidate | `1/9` | `-6` | maximum |
| early candidate | `1/3` | `+6` | minimum |

That is the key obstruction.

If standard relaxation follows:

```text
dR/dtau = -gamma dU/dR
```

then `R=1/3` is stable and `R=1/9` is unstable.

But the desired cosmological reading is:

```text
early high endpoint -> today low endpoint
1/3 -> 1/9.
```

To get that, the theory needs either:

```text
relaxation down -U
```

or:

```text
a derived first-order boundary arrow:
nabla_mu J_R^mu = -gamma A_arrow(C_exp)(27R^2-12R+1)
```

with the sign of `A_arrow` fixed by the parent theory.

That sign cannot be chosen after fitting.

## 7. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `variational_term_can_be_written` | pass formal | `U(R)` has the desired derivative |
| `coefficients_parent_forced` | fail | no symmetry or Ward identity fixes `9,-6,1` |
| `endpoint_arrow_derived` | fail | stability direction must be owned |
| `Qstar_charge_metric_derived` | fail | normalized charge measure remains missing |
| `constraint_trick_rejected` | pass | multiplier-imposed endpoint equation is not counted |
| `support_claim_allowed` | fail | formal potential is not a parent action theorem |

## 8. What This Means

The current best theory object is:

```text
endpoint quadratic theorem target:
27R^2 - 12R + 1 = 0.
```

The current best variational object is:

```text
formal potential:
U(R)=9R^3-6R^2+R.
```

The current blockers are:

```text
1. derive the coefficients;
2. derive the normalized charge unit Q_*;
3. derive the cosmological endpoint arrow;
4. avoid using a multiplier as a hidden postulate.
```

So this does not give field-theory promotion.

It does give a very precise parent-action target.

## 9. Claim Ceiling

Allowed:

```text
MTS now has a locked empirical amplitude branch B_mem=2/27 and an exact endpoint quadratic that a future parent action must derive.
```

Forbidden:

```text
MTS derives B_mem=2/27 from U(R).
```

Reason:

```text
U(R) is currently a formal owner candidate, not a coefficient-derived parent action.
```

## 10. Decision

Decision:

```text
variational_owner =
written_but_not_parent_derived
```

Decision:

```text
best_formal_term =
U(R)=9R^3-6R^2+R
```

Decision:

```text
main_failure =
coefficients_and_endpoint_arrow_not_derived
```

Decision:

```text
locked_empirical_branch =
B_mem=2/27 remains live
```

## 11. Next Target

The theory route has now had its clean shot.

Next target should be empirical discipline:

```text
112-two-over-27-external-holdout-manifest.md
```

Purpose:

```text
predeclare B_mem=2/27 as a frozen branch for external holdouts:
CMB distance priors, growth diagnostics, BAO-only variants, and later non-SN checks.
```

Pass condition:

```text
the amplitude is frozen before scoring and no branch refits B_mem.
```

Fail condition:

```text
2/27 only survives where it was rationalized from the original SN+BAO primary branch.
```
