# 94 - Endpoint Relaxation DeltaR Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 93 reduced the cosmology amplitude problem to:

```text
eta = 1              conditional on the FLRW Hubble-cap L_cg rule
B_mem = a_F DeltaR / 3
a_F DeltaR = 0.223600 to 0.460135
```

This checkpoint asks whether endpoint relaxation can derive `DeltaR` rather than leaving it as a post-fit contrast.

## 2. Short Verdict

```text
DeltaR_gate_status =
DeltaR_sign_and_order_bound_conditional_not_prediction
```

```text
promotion_allowed =
false
```

Plain English:

```text
The relaxation-functional route can conditionally give the right sign for DeltaR and shows that the required amplitude is an order-one contrast, not a ridiculous number. But it still does not predict DeltaR before the SN+BAO fit.
```

So this is a useful points-scoring round, not a knockout.

## 3. Machine Artifact

Script:

```text
research-programme\scripts\endpoint_relaxation_DeltaR_gate.py
```

Run:

```text
research-programme\runs\20260531-133627-endpoint-relaxation-DeltaR-gate
```

Generated:

```text
source_checkpoint_register.csv
flrw_eta1_product_inputs.csv
relaxation_functional_contract.csv
DeltaR_candidate_models.csv
required_DeltaR_by_aF.csv
quadratic_displacement_budget.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
DeltaR_sign_and_order_bound_conditional_not_prediction
```

## 4. Relaxation Contract

The candidate local endpoint functional is:

```text
R(m;X_B)=R_L(X_B)+1/2 lambda_R(X_B)[m-m_L(X_B)]^2+O([m-m_L]^3)
```

with:

```text
lambda_R > 0.
```

Then the trace-coupled function:

```text
F(m;X_B)=F_L(X_B)+a_F[R(m;X_B)-R(m_L;X_B)]
```

gives:

```text
F_1 = a_F partial_m R|m_L = 0.
```

This is good because the relaxed local endpoint has no linear trace force.

The proposed relaxation equation is:

```text
nabla_mu J_m^mu = -gamma_B partial_m R + [1-Pi_B]S_cg.
```

If source leakage is off and `gamma_B>0`, the Lyapunov form is:

```text
dR/dtau = -gamma_B(partial_m R)^2 <= 0.
```

That can give:

```text
DeltaR = R_early - R_today >= 0.
```

But only if the parent theory proves the endpoint ordering and the cosmological arrow.

## 5. What Was Earned

From checkpoint 93:

```text
a_F DeltaR = 3 B_mem = 0.223600 to 0.460135.
```

If `DeltaR` is normalized as:

```text
0 <= DeltaR <= 1,
```

then all inspected fixed branches require:

```text
a_F >= 0.460135.
```

If the stronger half-budget is imposed:

```text
0 <= DeltaR <= 0.5,
```

then:

```text
a_F >= 0.920271.
```

This is useful because it turns the amplitude issue into a sharp parent-action target:

```text
derive a positive trace coupling a_F of order one,
and derive a positive endpoint contrast DeltaR of order 0.2 to 0.5 if a_F is near one.
```

## 6. Required DeltaR by Trace Coupling

| `a_F` | required `DeltaR` range | Interpretation |
|---:|---:|---|
| 0.25 | 0.894398 to 1.840541 | too large for a unit-bounded `DeltaR` on the high branch |
| 0.50 | 0.447199 to 0.920271 | fits unit contrast, not half-budget |
| 0.460135 | 0.485943 to 1.000000 | minimum `a_F` if `DeltaR<=1` |
| 1.00 | 0.223600 to 0.460135 | clean order-one window |
| 2.00 | 0.111800 to 0.230068 | clean smaller endpoint contrast |

So the cleanest route is not:

```text
make DeltaR huge.
```

It is:

```text
a_F ~ 1
DeltaR ~ 0.22 to 0.46
eta = 1
```

with all three coming from the parent theory.

## 7. Candidate Mechanisms

| Candidate | Earns | Status |
|---|---|---|
| strict convex Lyapunov endpoint | `DeltaR>=0` if endpoint ordering is proved | conditional sign owner |
| bounded normalized contrast | converts the fit into `a_F>=0.460135` if `DeltaR<=1` | conditional order window |
| quadratic displacement route | `DeltaR=1/2 lambda_R (Delta m)^2` | magnitude template, not prediction |
| high-mobility screening | local relaxation without huge `lambda_R` | preferred local-safe route |
| stiff-`R` route | can manufacture amplitude | rejected as default route |
| flat/nonconvex `R` | no controlled sign or ordering | fail |

The important local warning is:

```text
F_2 = a_F lambda_R = a_F mu_B/gamma_B.
```

So using a huge `lambda_R` to force the cosmology amplitude is dangerous because the same stiffness feeds local trace residuals. The safer route is high mobility:

```text
large gamma_B,
not huge lambda_R.
```

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `DeltaR_positive_from_convex_relaxation` | pass conditional | Lyapunov-like `R` gives non-negative `DeltaR` if today is downstream |
| `endpoint_ordering_parent_derived` | fail | the parent action has not proven the cosmological endpoint ordering |
| `DeltaR_order_one_window_available` | pass conditional | `eta=1` needs `a_F DeltaR=0.223600` to `0.460135` |
| `DeltaR_predicted_without_SN_BAO_fit` | fail | the numerical window still comes from fitted `B_mem` |
| `aF_lower_bound_if_DeltaR_le1` | pass bound | if `DeltaR<=1`, then `a_F>=0.460135` |
| `aF_lower_bound_if_DeltaR_le_half` | pass bound | if `DeltaR<=0.5`, then `a_F>=0.920271` |
| `stiff_R_default_route_safe` | fail open | large `lambda_R` threatens local PPN through `F_2` |
| `high_mobility_route_preferred` | pass conditional | local screening should come from `gamma_B` rather than stiffness |
| `support_claim_allowed` | fail | sign/order bounds are not yet a prior prediction of `B_mem` |

## 9. Interpretation

Allowed statement:

```text
Given the current eta=1 FLRW branch, a convex endpoint-relaxation functional can conditionally explain the positive sign of B_mem and reduce the amplitude target to an order-one trace coupling times an order-one endpoint contrast.
```

Forbidden statement:

```text
MTS predicts B_mem from endpoint relaxation.
```

Reason:

```text
DeltaR is not yet predicted before fitting, and a_F is not action-normalized.
```

The boxing-score version:

```text
MTS scored points here because the target number is natural-sized and the sign has a plausible mechanism. It did not win the round outright because the actual amplitude is still selected after looking at cosmology.
```

## 10. Decision

Decision:

```text
DeltaR_status =
positive_sign_and_order_one_window_conditional_not_prediction
```

Decision:

```text
aF_if_unit_DeltaR =
a_F must be at least 0.460135
```

Decision:

```text
aF_near_one_readout =
if a_F is order-one near 1, DeltaR required is 0.223600 to 0.460135
```

Decision:

```text
local_safety_preference =
prefer high-gamma_B mobility screening over large-lambda_R stiffness
```

## 11. Next Target

Create:

```text
95-trace-coupling-aF-normalization-gate.md
```

Purpose:

```text
try to derive or bound a_F from the parent trace-coupling normalization, instead of treating it as a free dimensionless knob.
```

Pass condition:

```text
a_F is forced into an order-one positive range before SN+BAO fitting, ideally near the 0.46 to 1+ corridor required by the DeltaR gate.
```

Fail condition:

```text
a_F remains a chosen normalization, so B_mem remains a closure amplitude even though the sign and scale are now disciplined.
```
