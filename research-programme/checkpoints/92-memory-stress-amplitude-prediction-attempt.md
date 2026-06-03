# 92 - Memory-Stress Amplitude Prediction Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 91 found:

```text
p = 3 and u3 = 1/4 have a conditional structural route;
B_mem is positive and non-edge across inspected branches;
B_mem is still fitted, not parent-predicted.
```

This checkpoint asks whether `B_mem` can be derived or tightly bounded by a memory-stress/conservation exchange law.

## 2. Short Verdict

```text
amplitude_prediction_status =
bounded_order_one_corridor_not_prediction
```

```text
promotion_allowed =
false
```

Plain English:

```text
B_mem now has a sharper stress-exchange corridor and a useful scale bound. It still does not have a no-fit parent prediction.
```

This is progress, but not promotion.

## 3. Machine Artifact

Script:

```text
research-programme\scripts\memory_stress_amplitude_prediction_attempt.py
```

Run:

```text
research-programme\runs\20260531-132504-memory-stress-amplitude-prediction-attempt
```

Generated:

```text
source_checkpoint_register.csv
stress_exchange_equations.csv
source_profile_summary.csv
amplitude_corridor_grid.csv
eta_bound_table.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
memory_stress_amplitude_bounded_not_predicted
```

## 4. Stress-Exchange Chain

The usable chain is:

```text
Omega_M(N) = Omega_M0 + B_mem F(N)
```

so:

```text
S_M(N) = dOmega_M/dN = B_mem dF/dN
```

and:

```text
integral_0^infinity S_M dN = B_mem.
```

This means:

```text
B_mem is the integrated memory-source budget.
```

The parent trace corridor remains:

```text
B_mem = a_F DeltaR / (3 eta^2)
eta = H0 L_cg / c.
```

Therefore:

```text
B_mem >= 0
```

if:

```text
a_F > 0
DeltaR >= 0.
```

That condition gives a plausible sign law, but only conditionally.

## 5. Source Profile

For the retained fixed branch:

```text
u3 = 1/4
F(N) = 1 - exp[-(N/u3)^3].
```

The memory source peaks at:

```text
N_peak = 0.218395
z_peak = 0.244079
max(dF/dN) = 4.701727.
```

The fitted fixed-branch amplitude range:

```text
B_mem = 0.074533 to 0.153378.
```

So the peak memory-source strength is:

```text
max S_M = 0.350435 to 0.721144.
```

This gives the amplitude a concrete stress-exchange shape. It still does not predict the normalization.

## 6. Amplitude Corridor

The observed fixed-branch values require:

```text
a_F DeltaR = 3 B_mem eta^2.
```

Representative parent budgets:

| Branch | `B_mem` | `eta` | required `a_F DeltaR` | Readout |
|---|---:|---:|---:|---|
| strict full-sample full-cov DR2 | 0.074533 | 1.0 | 0.223600 | order-one |
| full-sample diagonal DR2 | 0.098134 | 1.0 | 0.294403 | order-one |
| 250-row DR2 | 0.139015 | 1.0 | 0.417044 | order-one |
| 250-row DR1 | 0.153378 | 1.0 | 0.460135 | order-one |

For horizon-scale coarse graining:

```text
eta = 1
```

the required parent contrast is:

```text
a_F DeltaR = 0.223600 to 0.460135.
```

That is not ridiculous. In fact it is nicely order-one-ish.

But it is not a prediction because `a_F`, `DeltaR`, and `eta` are still adjustable inside the corridor.

## 7. Bound Earned

If the parent contrast obeys:

```text
0 < a_F DeltaR <= 1,
```

then:

```text
B_mem <= 1 / (3 eta^2).
```

Using the largest inspected fixed-branch value:

```text
B_mem = 0.153378,
```

the bound becomes:

```text
eta <= 1.474203
```

or:

```text
L_cg <= 1.474203 c/H0.
```

That is a real tightening:

```text
super-horizon coarse-graining much above ~1.5 c/H0 would require a parent contrast larger than one.
```

For a stricter half-budget:

```text
a_F DeltaR <= 0.5,
```

the largest inspected branch requires approximately:

```text
eta <= 1.042.
```

So the amplitude is naturally compatible with a horizon-scale or sub-horizon `L_cg`, but not predicted by it.

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `fixed_Bmem_positive` | pass | range is positive: `0.074533` to `0.153378` |
| `fixed_Bmem_non_edge` | pass | zero edge hits across five inspected fixed-branch values |
| `eta1_order_one_budget` | pass | `eta=1` needs `a_F DeltaR = 0.223600` to `0.460135` |
| `unit_budget_eta_bound` | pass conditional | if `a_F DeltaR <= 1`, then `eta <= 1.474203` |
| `sign_predicted` | pass conditional | positive sign follows only if `a_F > 0` and `DeltaR >= 0` are derived |
| `magnitude_predicted_without_fit` | fail | `eta`, `a_F`, and `DeltaR` remain free within a corridor |
| `conservation_exchange_owned` | open | source identity exists, but stress exchange is not varied from an action |
| `promotion_allowed` | fail | a bound/corridor is not a no-fit prediction |

## 9. Interpretation

Allowed statement:

```text
B_mem is a positive, non-edge integrated memory-source budget, and its fitted scale is compatible with an order-one parent trace corridor for horizon-scale coarse graining.
```

Forbidden statement:

```text
MTS predicts B_mem.
```

Reason:

```text
the parent theory has not derived eta, a_F, DeltaR, endpoint ordering, or the stress-exchange tensor variation.
```

## 10. Decision

Decision:

```text
Bmem_prediction_status =
bounded_order_one_corridor_not_prediction
```

Decision:

```text
allowed_use =
tight prior/corridor discipline for future tests
```

Decision:

```text
forbidden_use =
field-theory support claim from fitted B_mem
```

The boxing translation:

```text
B_mem did not win by knockout.
But it did not get exposed as a nonsense knob either.
It now has a fair scorecard constraint: stay positive, non-edge, and inside the parent corridor.
```

## 11. Next Target

Create:

```text
93-Lcg-trace-contrast-owner-gate.md
```

Purpose:

```text
try to derive eta = H0 L_cg/c, a_F, or DeltaR before running more support fits.
```

Priority order:

1. derive or bound `L_cg` from the coherent-domain/coarse-graining rule;
2. derive the sign and range of `DeltaR` from endpoint memory relaxation;
3. derive `a_F` from trace-coupling normalization;
4. only then turn the corridor into a predictive prior.

Pass condition:

```text
the parent theory narrows B_mem before looking at SN+BAO fit results.
```

Fail condition:

```text
B_mem remains a fitted closure amplitude, with the current corridor used only as a discipline bound.
```
