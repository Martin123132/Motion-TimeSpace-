# 95 - Trace-Coupling aF Normalization Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 94 reduced the remaining memory-amplitude target to:

```text
eta = 1
a_F DeltaR = 0.223600 to 0.460135
```

and found:

```text
if DeltaR <= 1,   a_F >= 0.460135
if DeltaR <= 0.5, a_F >= 0.920271
```

This checkpoint asks whether `a_F` can be derived or normalized before using cosmology fits.

## 2. Short Verdict

```text
aF_gate_status =
aF_order_one_canonical_viable_not_parent_derived
```

```text
promotion_allowed =
false
```

Plain English:

```text
a_F = 1 is the cleanest current private closure choice. It makes the required DeltaR range 0.223600 to 0.460135, which is natural-sized and locally plausible if lambda_R is order-one. But a_F = 1 is still a normalization choice, not yet an action theorem.
```

Boxing-score version:

```text
MTS wins useful style points here. The amplitude is no longer a random knob; it has a natural canonical setting. But the referee cannot score this as a derived field-theory punch until the parent action fixes the normalization of R.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\trace_coupling_aF_normalization_gate.py
```

Run:

```text
research-programme\runs\20260531-134132-trace-coupling-aF-normalization-gate
```

Generated:

```text
source_checkpoint_register.csv
flrw_eta1_product_inputs.csv
trace_normalization_contract.csv
aF_candidate_normalizations.csv
aF_DeltaR_F2_compatibility.csv
normalization_degeneracies.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
aF_order_one_canonical_viable_not_parent_derived
```

## 4. The Core Obstruction

The current trace projection is:

```text
Gamma_eff = L_cg^-2 [F_L(X_B) + a_F (R(m;X_B)-R(m_L;X_B))]
```

The problem is a rescaling degeneracy:

```text
R -> c_R R
a_F -> a_F / c_R
```

The product:

```text
a_F DeltaR
```

does not change if `DeltaR` rescales with `R`.

Therefore `a_F` cannot be called derived until the parent action fixes the absolute normalization of `R`.

This is the hard blocker:

```text
derive a parent field metric / charge normalization / Ward identity for R,
or label a_F = 1 as a canonical closure convention.
```

## 5. What Was Earned

The sign is conditionally aligned:

```text
a_F > 0
DeltaR >= 0
=> B_mem > 0.
```

The order-one range is now sharp:

```text
a_F >= 0.460135      if DeltaR <= 1
a_F >= 0.920271      if DeltaR <= 0.5
```

The canonical choice:

```text
a_F = 1
```

gives:

```text
DeltaR = 0.223600 to 0.460135.
```

That is the nicest current branch:

```text
eta = 1
a_F = 1
DeltaR ~ 0.22 to 0.46
```

It is simple, positive, order-one, and compatible with the endpoint-relaxation picture.

## 6. Candidate Normalizations

| Candidate | `a_F` | Readout | Status |
|---|---:|---|---|
| canonical unit trace coupling | 1.000000 | `DeltaR=0.223600` to `0.460135` | best closure choice, not derivation |
| minimum unit-`DeltaR` coupling | 0.460135 | highest branch needs `DeltaR=1` | lower bound if `DeltaR<=1` |
| half-budget coupling | 0.920271 | highest branch needs `DeltaR=0.5` | lower bound if `DeltaR<=0.5` |
| weak trace coupling | 0.250000 | highest branch needs `DeltaR=1.840541` | disfavored if `DeltaR` is unit-bounded |
| strong trace coupling | 2.000000 | `DeltaR=0.111800` to `0.230068` | possible, but raises local `F_2` |
| negative trace coupling | -1.000000 | needs negative `DeltaR` for positive `B_mem` | rejected for the positive-relaxation branch |

So the theory should not drift toward:

```text
a_F << 1
```

unless it also derives a larger-than-unit endpoint contrast. The clean corridor is:

```text
0.46 <= a_F <= O(1 to 2)
```

with `a_F=1` as the most disciplined private closure convention.

## 7. Local Safety Coupling

The local branch sees:

```text
F_2 = a_F lambda_R.
```

This means a cosmologically convenient `a_F` is not free locally.

The script tested toy compatibility windows using:

```text
DeltaR_cap in {0.5, 1.0}
lambda_R in {0.25, 0.5, 1, 2, 4}
F2_cap in {0.5, 1, 2}
```

Result:

```text
18/30 toy local-F2 windows allow canonical a_F = 1.
```

Interpretation:

```text
a_F = 1 is locally plausible if lambda_R is order-one or smaller;
a_F = 1 becomes dangerous if lambda_R is stiff.
```

This reinforces the previous design rule:

```text
screen locally through high gamma_B mobility,
not through huge lambda_R stiffness.
```

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `aF_positive_sign` | pass conditional | positive `a_F` matches positive `B_mem` if `DeltaR>=0` |
| `aF_order_one_required` | pass bound | `a_F>=0.460135` for `DeltaR<=1`, or `a_F>=0.920271` for `DeltaR<=0.5` |
| `canonical_aF1_viable` | pass conditional | `a_F=1` gives `DeltaR=0.223600` to `0.460135` |
| `canonical_aF1_derived` | fail | unit coefficient is a clean convention, not an action result |
| `R_rescaling_degeneracy_broken` | fail | `a_F` can be moved into the definition of `R` |
| `local_F2_overlap_exists` | pass conditional | `18/30` toy windows allow canonical `a_F=1` |
| `stiff_lambdaR_safe_for_aF1` | fail open | stiff `lambda_R` can make `F_2` unsafe |
| `boundary_charge_predicts_aF` | fail | current boundary budget is inferred from fitted `B_mem` |
| `support_claim_allowed` | fail | `a_F` is bounded/natural, not derived |

## 9. Interpretation

Allowed statement:

```text
The post-checkpoint cosmology branch now has a disciplined canonical amplitude convention: eta=1, a_F=1, and a positive endpoint contrast DeltaR~0.22-0.46.
```

Forbidden statement:

```text
MTS derives a_F=1 from the parent field theory.
```

Reason:

```text
the parent action has not fixed the absolute normalization of R or produced a Ward/Noether identity for the trace projection coefficient.
```

This is not grim. It is the difference between:

```text
random fitted amplitude
```

and:

```text
explicit canonical closure with a known derivation debt.
```

That is progress.

## 10. Decision

Decision:

```text
aF_status =
positive_order_one_and_canonical_unit_viable_but_not_parent_derived
```

Decision:

```text
best_private_closure_choice =
use a_F = 1 as canonical trace normalization,
which implies DeltaR = 0.223600 to 0.460135.
```

Decision:

```text
hard_blocker =
R_rescaling_degeneracy_and_missing_action_Ward_identity
```

Decision:

```text
local_safety_rule =
keep lambda_R order-one or screen through gamma_B so F_2=a_F lambda_R stays small.
```

## 11. Next Target

Create:

```text
96-parent-R-normalization-contract.md
```

Purpose:

```text
write the exact contract a future parent action must satisfy to fix R normalization and make a_F=1 more than a convention.
```

Pass condition:

```text
the parent action fixes the scale of R independently of SN+BAO and makes the unit trace coefficient unavoidable.
```

Fail condition:

```text
a_F=1 remains an explicit closure convention, acceptable for disciplined testing but not promotable as field-theory evidence.
```
