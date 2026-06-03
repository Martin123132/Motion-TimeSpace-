# 93 - Lcg Trace-Contrast Owner Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 92 found:

```text
B_mem is positive and non-edge;
B_mem fits an order-one parent corridor;
B_mem is still not predicted because eta, a_F, and DeltaR remain loose.
```

This checkpoint asks whether `eta = H0 L_cg/c`, `a_F`, or `DeltaR` can be owned before more support fitting.

## 2. Short Verdict

```text
owner_gate_status =
eta_conditionally_locked_trace_product_not_predicted
```

```text
promotion_allowed =
false
```

Plain English:

```text
The FLRW L_cg rule can conditionally lock eta = 1, which tightens the B_mem corridor a lot. But the remaining product a_F DeltaR is still inferred from the fit rather than predicted by the parent theory.
```

So this is a useful tightening, not a promotion.

## 3. Machine Artifact

Script:

```text
research-programme\scripts\Lcg_trace_contrast_owner_gate.py
```

Run:

```text
research-programme\runs\20260531-132942-Lcg-trace-contrast-owner-gate
```

Generated:

```text
source_checkpoint_register.csv
owner_candidates.csv
equation_chain.csv
eta_product_budget.csv
predictive_prior_test.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
Lcg_eta_conditionally_locked_trace_product_not_predicted
```

## 4. What Was Earned

The current universal `L_cg` closure is:

```text
L_cg = [L_H^-2 + alpha_K G_K^2]^-1/2.
```

For homogeneous FLRW:

```text
G_K = 0
```

so:

```text
L_cg = L_H = c/H_bg.
```

At the present background:

```text
eta = H0 L_cg/c = 1.
```

This matters because the amplitude corridor becomes:

```text
B_mem = a_F DeltaR / 3
```

instead of:

```text
B_mem = a_F DeltaR / (3 eta^2)
```

with freely drifting `eta`.

This is the good news:

```text
eta is no longer arbitrary inside the homogeneous cosmology branch if the L_cg Hubble-cap rule is accepted.
```

## 5. What Is Still Not Earned

The problem moves to:

```text
a_F DeltaR.
```

With:

```text
eta = 1,
```

the inspected fixed-branch values require:

```text
a_F DeltaR = 3 B_mem.
```

Numerically:

| Branch | `B_mem` | required `a_F DeltaR` |
|---|---:|---:|
| strict full-sample full-cov DR2 | 0.074533 | 0.223600 |
| full-sample diagonal DR2 | 0.098134 | 0.294403 |
| 250-row SH0ES diagonal DR2 | 0.138740 | 0.416221 |
| 250-row no-SH0ES full-cov DR2 | 0.139015 | 0.417044 |
| 250-row no-SH0ES full-cov DR1 | 0.153378 | 0.460135 |

This range is:

```text
a_F DeltaR = 0.223600 to 0.460135.
```

That is a nice order-one parent contrast budget.

But the parent theory still has to predict it.

## 6. Owner Candidates

| Owner | Conditional result | Status |
|---|---|---|
| `L_cg / eta` | FLRW Hubble cap gives `eta = 1` today | conditional background owner, not parent theorem |
| `DeltaR` | positive if endpoint memory relaxation orders early state above present state | sign conditional, magnitude open |
| `a_F` | positive if trace coupling has relaxing/attractive sign | sign conditional, normalization open |
| `a_F DeltaR` | with `eta=1`, product must be `3 B_mem` | corridor budget only |

The key non-identifiability:

```text
B_mem only fixes the product a_F DeltaR.
```

It does not separately fix:

```text
a_F
DeltaR.
```

So a parent theorem must now pick one or both.

## 7. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `free_or_fit_chosen_Lcg_rejected` | pass | sector/fitted/residual-selected `L_cg` was already rejected |
| `FLRW_eta1_from_Lcg_coherence` | pass conditional | homogeneous FLRW gives `G_K=0`, `L_cg=L_H`, `eta=1` today |
| `eta_parent_derived` | fail | the `L_cg` coherence rule remains closure, not microscopic dynamics |
| `eta1_product_order_one` | pass | `eta=1` gives `a_F DeltaR = 0.223600` to `0.460135` |
| `DeltaR_sign_condition` | pass conditional | positive `DeltaR` requires derived endpoint relaxation ordering |
| `aF_sign_condition` | pass conditional | positive `a_F` is plausible but not action-normalized |
| `aF_DeltaR_separately_predicted` | fail | only the product is constrained |
| `predictive_Bmem_prior_earned` | fail | the narrow window comes from fitted `B_mem`, not parent theory |
| `support_claim_allowed` | fail | conditional `eta=1` plus order-one product is still a corridor |

## 8. Interpretation

Allowed statement:

```text
The current L_cg coherence rule conditionally fixes eta = 1 on the homogeneous present FLRW branch, reducing the B_mem problem to an order-one trace-contrast product a_F DeltaR.
```

Forbidden statement:

```text
MTS predicts B_mem from L_cg.
```

Reason:

```text
the L_cg rule is still a closure rule, and a_F DeltaR is not predicted before the fit.
```

## 9. Why This Still Helps

Before this checkpoint, the amplitude corridor had three loose pieces:

```text
eta;
a_F;
DeltaR.
```

Now, on the homogeneous FLRW branch, `eta` has a conditional lock:

```text
eta = 1.
```

That leaves one product:

```text
a_F DeltaR.
```

This is a real narrowing. The amplitude problem is no longer "anything can happen." It is:

```text
derive a trace-contrast product of roughly 0.22 to 0.46.
```

That is a much sharper target.

## 10. Decision

Decision:

```text
eta_status =
eta_equals_1_conditionally_from_FLRW_Hubble_cap_not_parent_derived
```

Decision:

```text
trace_product_status =
aF_DeltaR_order_one_required_not_predicted
```

Decision:

```text
Bmem_prior_status =
wide_corridor_tightened_to_eta1_product_but_not_predictive
```

Overall:

```text
cosmology_branch_status =
still_empirically_competitive_closure_candidate
```

## 11. Next Target

Create:

```text
94-endpoint-relaxation-DeltaR-gate.md
```

Purpose:

```text
try to derive the sign and approximate range of DeltaR from a monotone endpoint-relaxation or Lyapunov trace functional.
```

Pass condition:

```text
DeltaR is positive and order-one before using SN+BAO best fits, so B_mem gets a real predictive prior when combined with eta=1 and a_F normalization.
```

Fail condition:

```text
DeltaR remains a post-fit contrast, so B_mem remains corridor-bound closure.
```
