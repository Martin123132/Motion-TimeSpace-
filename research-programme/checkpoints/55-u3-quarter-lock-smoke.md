# u3 Quarter-Lock Smoke

## 1. Purpose

This file follows:

```text
54-coherent-domain-and-u3-origin.md
```

The previous checkpoint found a structural scale candidate:

```text
u_3 = 1/4.
```

This checkpoint asks:

```text
If we freeze u_3 = 1/4 with no refit, does the branch survive the same internal
background, growth, CMB-distance, and H(z) guardrails as fitted C2?
```

Short answer:

```text
yes. The fixed-quarter branch survives and is slightly better than fitted C2 on
the internal no-refit smoke metrics used here.
```

That is a real discipline gain: one fitted transition-scale freedom can be
replaced by a structural candidate without immediately breaking the branch.

It is still not evidence. Tiny dragon, still in quarantine.

## 2. Machine Run

Implemented:

```text
scripts/u3_quarter_lock_smoke.py
```

Successful run:

```text
runs/20260531-104003-u3-quarter-lock-smoke/status.json
```

Readout:

```text
u3_quarter_lock_retained_as_less_free_closure_candidate
```

Generated:

```text
runs/20260531-104003-u3-quarter-lock-smoke/results/source_checkpoint_register.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_background_scores.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_growth_CMB_scores.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_guardrail_comparison.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_activation_shape.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_growth_predictions.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/u3_quarter_CMB_predictions.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/gate_results.csv
runs/20260531-104003-u3-quarter-lock-smoke/results/decision.csv
```

## 3. Frozen Branch

Compared:

```text
fitted C2:     u_3 = 0.2429466120286312
quarter lock:  u_3 = 0.25
```

No refit was allowed. The only change was:

```text
replace fitted u_3 with u_3 = 1/4 in F(N)=1-exp[-(N/u_3)^3].
```

The fractional shift is:

```text
frac_delta_u3_quarter_vs_fitted = 0.029032666528963875
```

So this is a genuine fixed-scale test, not a parameter massage.

## 4. Guardrail Result

Against fitted C2:

```text
Delta chi2 SN+BAO+H(z)      = -0.007460191927748383
Delta chi2 primary growth   = -0.06039645656001014
Delta chi2 CMB distance     = -0.01691758480516344
Delta chi2 H(z)             =  0.00019303445924023777
Delta chi2 growth+CMB+H(z)  = -0.0771210069059336
failed guardrails           = []
```

Interpretation:

```text
u_3 = 1/4 does not damage the internal fixed-row guardrails.
```

In this smoke it is very slightly better than fitted C2 overall, but that must
not be overplayed because this is not an official likelihood and not a fresh
holdout.

## 5. Why This Matters

Before this checkpoint:

```text
u_3 was inherited from the fitted C2 N50.
```

After this checkpoint:

```text
u_3 = 1/4 is a less-free closure candidate that survives the same no-refit
internal guardrails.
```

That moves the branch in the correct direction:

```text
from fitted shape scale
to structural scale candidate
to future derivation target.
```

This is exactly the kind of narrowing a field-theory programme needs.

## 6. What Still Fails

Gate result:

```text
u3_quarter_no_refit_branch_evaluated          pass
quarter_lock_not_materially_worse_than_C2     pass
model_freedom_reduced                         pass
u3_parent_derived                             fail
support_claim_allowed                         fail
```

Still missing:

```text
parent derivation of u_3 = 1/4;
parent derivation of the coherent domain D;
b_mem amplitude origin;
Bianchi/conservation ownership;
perturbation and lensing response;
official CMB likelihood;
fresh independent holdout.
```

So the quarter lock is retained, but not promoted.

## 7. Decision

Decision:

```text
u3_quarter_lock_status = retained_as_less_free_closure_candidate
```

Meaning:

```text
the fitted C2 transition scale can provisionally be replaced by u_3=1/4;
the replacement survived the short no-refit guardrails;
the branch is now less phenomenological than before;
the quarter value must still be derived from a parent cell/coherence theorem.
```

Allowed wording:

```text
The u_3=1/4 quarter-lock branch is retained as a less-free internal closure
candidate.
```

Forbidden wording:

```text
u_3=1/4 is proven;
the parent theory derives the activation scale;
this is empirical support for MTS.
```

## 8. Next Target

Create:

```text
56-u3-quarter-parent-cell-theorem-attempt.md
```

Purpose:

```text
try to derive u_3 = 1/4 from a parent 3+1 cell/coherence normalization rather
than treating the quarter value as a lucky near-lock.
```

Pass condition:

```text
the parent variables define a 3+1 coherence cell, normalization, or invariant
whose dimensionless activation scale is 1/4 before looking at the smoke score.
```

Fail condition:

```text
u_3 = 1/4 remains numerically cute but theoretically unowned.
```
