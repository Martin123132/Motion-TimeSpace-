# 91 - Bmem, p, and u3 Parent-Ownership Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 90 changed the cosmology judging frame:

```text
MTS does not need a knockout;
MTS can win or draw on points if it is cleaner, edge-free, and structurally owned;
but closure amplitudes cannot be treated as theory proof.
```

This checkpoint asks the real bottleneck question:

```text
Can B_mem, p, and u3 be owned by the parent theory rather than treated as good-fitting closure furniture?
```

## 2. Short Verdict

```text
ownership_gate_status =
shape_partially_owned_amplitude_not_predicted
```

```text
promotion_allowed =
false
```

Plain English:

```text
p=3 and u3=1/4 now have a coherent conditional parent route. B_mem is empirically well-behaved and order-one plausible, but still not predicted.
```

This is a better place than pure phenomenology, but not yet a derived field theory.

## 3. Machine Artifact

Script:

```text
research-programme\scripts\Bmem_p_u3_parent_ownership_gate.py
```

Run:

```text
research-programme\runs\20260531-132046-Bmem-p-u3-parent-ownership-gate
```

Generated:

```text
source_checkpoint_register.csv
cosmology_parameter_evidence.csv
ownership_attempts.csv
equation_chain.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
Bmem_p_u3_parent_ownership_gate_written_not_promoted
```

## 4. Ownership Ledger

| Quantity | Current owner route | Status | What is earned | What is missing |
|---|---|---|---|---|
| `p` | `I_M = det(Q_coh)` with three spatial coherent-load eigenvalues | conditional shape derivation | cubic exposure is no longer just fitted by taste | parent action/current for `Q_coh` |
| `u3` | 3+1 coherent observer-cell normalization `C4` | conditional cell normalization | `X_FLRW = 4N`, hence `u3 = 1/4`, if the cell route is owned | proof that the clock leg normalizes but is not a fourth exposure eigenvalue |
| `B_mem` | memory-stress amplitude corridor | order-one corridor only | positive, non-edge, plausible scale across tested branches | prediction of sign, magnitude, exchange law, and conservation owner |

So the branch is not just wallpaper. But the amplitude still has to earn its passport.

## 5. Conditional Derivation Chain

The best current chain is:

```text
Theta^i_j = h^{i alpha} h_{j beta} nabla_alpha u^beta
```

```text
Q^i_j = 4 integral_t^t0 P_coh[Theta]^i_j d tau
```

In FLRW:

```text
Q^i_j = 4N delta^i_j
```

Then:

```text
I_M = det(Q_coh) = (4N)^3
```

and:

```text
F(N) = 1 - exp[-I_M] = 1 - exp[-(N/(1/4))^3].
```

This gives:

```text
p = 3
u3 = 1/4
```

conditionally.

The important subtlety:

```text
the exposure is spatial, so it has three eigenvalues;
the normalization is 3+1, so the load scale gets the factor four.
```

That split is promising, but it is not yet action-derived.

## 6. Why This Is Better Than a Fit

Previously, a hostile critic could say:

```text
you picked p=3 and u3=1/4 because they fitted nicely.
```

The better answer now is:

```text
p=3 follows from a spatial determinant if Q_coh is the parent coherent-load tensor;
u3=1/4 follows from 3+1 cell normalization if C4 owns the load scale.
```

This is not a full derivation.

But it is a real structural narrowing:

```text
the future parent theory must own Q_coh, C4, and the spatial-vs-3+1 split.
```

If it cannot do that, the branch stays closure-only.

## 7. Empirical Amplitude Evidence

Fixed-branch `B_mem` across inspected runs:

| Branch | `B_mem` | Edge flag |
|---|---:|---:|
| SH0ES diagonal 250-row DR2 | 0.138740 | no |
| no-SH0ES full-cov 250-row DR2 | 0.139015 | no |
| no-SH0ES full-cov 250-row DR1 | 0.153378 | no |
| no-SH0ES diagonal full-sample DR2 | 0.098134 | no |
| no-SH0ES full-cov full-sample DR2 | 0.074533 | no |

Range:

```text
B_mem = 0.074533 to 0.153378
```

This is good behavior:

```text
positive;
not edge-hitting;
same broad scale across splits;
smaller in the stricter full-sample/full-cov branch.
```

But it is still fitted.

The current amplitude corridor is:

```text
B_mem ~ a_F DeltaR / (3 eta^2).
```

For `eta = 1`, the observed range would need:

```text
a_F DeltaR ~ 0.224 to 0.460.
```

That is not absurd. It is also not a prediction.

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `p3_shape_owned_by_spatial_determinant` | pass conditional | `det(Q_coh)` gives cubic exposure once `Q` is owned |
| `u3_quarter_owned_by_3plus1_cell` | pass conditional | `C4` gives `X_FLRW = 4N`, but the split is not action-derived |
| `Bmem_non_edge_in_fixed_branch` | pass | five fixed-branch values inspected, zero edge hits |
| `Bmem_parent_predicted` | fail | only an order-one corridor exists |
| `fitted_u3_ablation_stable` | fail | fitted `u3` branches hit `u3 = 0.05` and/or `B_mem` edge |
| `single_parent_owner_satisfied` | fail | `S_cell/S_stress` contract exists but is not yet derived |
| `support_claim_allowed` | fail | conditional ownership is not field-theory derivation |

The fitted-`u3` failure is actually clarifying:

```text
free u3 can become a rescue knob;
fixed u3=1/4 is the cleaner branch if the cell route can be derived.
```

## 9. Interpretation

Allowed statement:

```text
The MTS cosmology closure now has a conditional structural route for p=3 and u3=1/4, and the fitted B_mem amplitude is non-edge across the tested branches.
```

Forbidden statement:

```text
MTS derives the cosmology amplitude and activation law from a parent field theory.
```

Reason:

```text
Q_coh, C4, and B_mem still lack a completed parent action/stress/conservation derivation.
```

## 10. Decision

Decision:

```text
p_status =
conditionally_owned_shape_not_promoted
```

Decision:

```text
u3_status =
conditional_3plus1_cell_scale_not_promoted
```

Decision:

```text
Bmem_status =
non_edge_empirical_amplitude_with_order_one_corridor_not_prediction
```

Overall:

```text
cosmology_branch_status =
empirically_competitive_closure_candidate_pending_parent_amplitude_owner
```

This means:

```text
MTS is still in the fight on the cosmology card;
the shape is becoming structurally motivated;
the amplitude is the next wall.
```

## 11. Next Target

Create:

```text
92-memory-stress-amplitude-prediction-attempt.md
```

Purpose:

```text
try to derive or tightly bound B_mem from a memory stress/conservation exchange law instead of fitting it.
```

Pass condition:

```text
S_stress or an equivalent conserved exchange current predicts the sign and order of B_mem, ideally narrowing B_mem without using SN+BAO best fits.
```

Fail condition:

```text
B_mem remains a fitted closure amplitude, so the cosmology branch stays explicitly closure-only even if it keeps winning rounds on points.
```
