# 386 - Local-Bound Runner V2 Smoke Matrix

Private local-bound/WEP/PPN smoke checkpoint. This is not a public WEP, PPN, preferred-frame, fifth-force, Einstein-Hilbert, source-normalization, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 385 left the observed-coframe pullback active:

```text
Pi_I^matter
```

was classified but not cancelled.

So this checkpoint does the fair empirical thing:

```text
run retained local residual rows through a small smoke matrix,
include a GR/null baseline in the same evaluator,
and refuse to call budgets passes.
```

This answers one important worry:

```text
are we only stress-testing MTS, or are we checking the baseline too?
```

Answer:

```text
the GR/null baseline is explicitly run.
```

It is sane:

```text
zero residual stays inside every source-locked local row.
```

The MTS retained rows then become:

```text
suppression budgets,
not victories,
not final failures,
and not local-GR derivations.
```

This is the Mayweather route:

```text
same ring,
same scoring system,
no fake knockout claim.
```

## 2. Machine Artifact

Script:

```text
scripts/local_bound_runner_v2_smoke_matrix.py
```

Run:

```text
runs/20260602-014500-local-bound-runner-v2-smoke-matrix
```

Outputs:

```text
results/source_register.csv
results/local_numeric_rows.csv
results/unscored_rows.csv
results/smoke_scenarios.csv
results/baseline_sanity_matrix.csv
results/residual_smoke_matrix.csv
results/suppression_budget_summary.csv
results/pullback_row_join.csv
results/verdict_table.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
local_bound_runner_v2_smoke_matrix_written_GR_null_baseline_sane_retained_pullback_rows_budgeted_no_local_GR_pass
```

Claim ceiling:

```text
local_bound_smoke_matrix_only_no_WEP_PPN_preferred_frame_fifth_force_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Numeric Rows

The smoke matrix carries nine numeric local rows:

| Row | Observable | State | Source lock | Meaning |
|---|---|---|---:|---|
| `R1` | `eta_WEP` | budget-only | `2.8e-15` | hardest always-relevant WEP row |
| `R2` | `alpha_clock_redshift` | budget-only | `3.1e-5` | clock/common-mode row |
| `R3` | `gamma_minus_1` | budget-only | `2.3e-5` | light/curvature PPN row |
| `R4` | `beta_minus_1` | budget-only | `7.8e-5` | nonlinear/radial PPN row |
| `R5` | `alpha1` | budget-only | `1.0e-4` | preferred-frame row |
| `R6` | `alpha2` | budget-only | `2.0e-9` | hard preferred-frame row |
| `R7` | `alpha3` | contingent budget | `4.0e-20` | brutal only if channel exists |
| `R8` | `xi` | budget-only | `4.0e-9` | preferred-location/aniso row |
| `R9` | `Gdot/G` | contingent budget | `9.6e-15 yr^-1` | time-drift row if channel exists |

And one unscored row:

| Row | Observable | Status |
|---|---|---|
| `R10` | `delta_G_or_fifth_force_yukawa` | not scalar-scored until range, coupling, source charge, and screening/profile are supplied |

So fifth force is still:

```text
force-law contract,
not one fake number.
```

## 4. Smoke Scenarios

Seven scenarios were run across the nine numeric rows:

| Scenario | What it tests | Result role |
|---|---|---|
| `GR_null_baseline` | zero residual through same evaluator | baseline sanity |
| `conditional_derived_zero_control` | what a theorem-zero would look like | not currently available |
| `one_tenth_budget_control` | retained coefficient safely below source lock | diagnostic only |
| `edge_budget_control` | retained coefficient exactly at source lock | unstable edge |
| `ten_times_over_budget_control` | retained coefficient too large | smoke failure |
| `floor_leak_1e_minus_12` | tiny-looking absolute leak | exposes brutal rows |
| `unit_coupling_stress` | order-one retained coupling | required suppression factors |

Important:

```text
inside budget
```

does not mean:

```text
derived pass.
```

It means only:

```text
if this coefficient really existed at this size,
the row would sit inside the source lock.
```

The theory still owes the coefficient, theorem-zero, or closure label.

## 5. Baseline Result

The GR/null baseline row is clean:

| Scenario | Inside | Edge | Over budget | Verdict |
|---|---:|---:|---:|---|
| `GR_null_baseline` | `9` | `0` | `0` | baseline sane |

That matters.

If the baseline had failed, the pipeline would be suspect.

It did not.

So the smoke runner can now be used fairly:

```text
GR/null sanity first,
MTS retained-row stress second.
```

## 6. Smoke Verdicts

The scenario summary:

| Scenario | Inside | Edge | Over budget | Verdict |
|---|---:|---:|---:|---|
| `GR_null_baseline` | `9` | `0` | `0` | baseline sane |
| `conditional_derived_zero_control` | `9` | `0` | `0` | diagnostic only |
| `one_tenth_budget_control` | `9` | `0` | `0` | diagnostic only |
| `edge_budget_control` | `0` | `9` | `0` | diagnostic only |
| `ten_times_over_budget_control` | `0` | `0` | `9` | diagnostic only |
| `floor_leak_1e_minus_12` | `6` | `0` | `3` | diagnostic only |
| `unit_coupling_stress` | `0` | `0` | `9` | diagnostic only |

The most useful line is:

```text
floor_leak_1e_minus_12
```

because it shows that a coefficient can look tiny and still be too large for:

```text
eta_WEP,
alpha3 if channel exists,
and Gdot/G if time-drift channel exists.
```

So the local branch needs real structural suppression.

Handwaving "small" is not enough.

## 7. Suppression Budget Summary

Order-one retained couplings fail every numeric row.

Required absolute coefficient ceilings for unit response:

| Observable | State | Required ceiling |
|---|---|---:|
| `eta_WEP` | budget-only | `2.8e-15` |
| `alpha2` | budget-only | `2.0e-9` |
| `xi` | budget-only | `4.0e-9` |
| `gamma_minus_1` | budget-only | `2.3e-5` |
| `alpha_clock_redshift` | budget-only | `3.1e-5` |
| `beta_minus_1` | budget-only | `7.8e-5` |
| `alpha1` | budget-only | `1.0e-4` |
| `alpha3` | contingent budget | `4.0e-20` |
| `Gdot/G` | contingent budget | `9.6e-15 yr^-1` |

The pressure ranking is therefore:

```text
alpha3 is numerically most brutal but contingent.
eta_WEP is the hardest always-relevant ready row.
```

That is exactly the runner-v2 stance.

## 8. Pullback Join

The retained pullback pieces map to the runner like this:

| Pullback piece | Rows | Smoke status |
|---|---|---|
| representative `Cperp` | clock/gamma if leakage survives | conditional gauge zero or budget |
| physical common `C_D` | clock, gamma, fifth force, `Gdot/G` | common-mode budget or unscored |
| physical species `C_D` | `eta_WEP`, composition force | hardest active budget |
| projector/domain selector | `alpha1`, `alpha2`, `xi`, gamma | preferred-frame budget |
| boundary selector | gamma, beta, alpha rows, WEP boundary | boundary budget |
| bulk `X` selector/charge | fifth force, gamma, beta, WEP if charged | unscored or budget |

This is the key lesson from 385 carried into 386:

```text
Cperp might be gauge.
C_D species response is not killed by representative invariance.
```

So:

```text
eta_WEP stays live until identity coframe or parent species symmetry/common F is derived.
```

## 9. What This Proves

This checkpoint proves only a narrow thing:

```text
the local-bound runner can evaluate GR/null and retained residual rows
without confusing baseline sanity, budget stress, and pass claims.
```

It also proves:

```text
order-one retained local couplings are impossible under the source locks,
unless the channel is absent, theorem-zero, gauge-zero, or closure-zero.
```

And it proves:

```text
the local problem is not vague anymore.
```

It is a coefficient/theorem problem.

For `eta_WEP`, unit response needs roughly:

```text
|coefficient| <= 2.8e-15.
```

That is why a real derivation matters.

## 10. What This Does Not Prove

This does not prove:

```text
WEP pass,
PPN pass,
preferred-frame pass,
fifth-force pass,
EH reduction,
or local GR.
```

It also does not prove:

```text
MTS fails.
```

It proves:

```text
if retained pullbacks are real local couplings,
they must be structurally killed, source-normalized, or extremely suppressed.
```

That is the honest state.

The branch is alive only if the next theory move supplies one of:

```text
identity coframe,
parent species symmetry/common F,
local common-mode silence/source normalization,
Ward-owned no-hair counterstress,
or explicit labelled closure.
```

## 11. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| numeric local rows loaded | pass | nine numeric rows plus one unscored force-law row |
| GR/null baseline same pipeline | pass | nine baseline rows evaluated with zero residual |
| smoke scenarios written | pass | seven scenarios times nine rows gives sixty-three smoke rows |
| unit coupling not mistaken for pass | pass | all nine unit-coupling rows are over budget |
| `eta_WEP` pressure visible | pass | unit eta severity is about `3.57e14` |
| fifth force kept unscored | pass | `delta_G`/Yukawa row still needs range/coupling/source charge |
| WEP/PPN/local GR promoted | fail | no derived coefficients and no parent cancellation of `Pi_I^matter` |
| claim ceiling enforced | pass | no WEP/PPN/preferred-frame/fifth-force/EH/local-GR pass |

## 12. Decision

Decision:

```text
local_bound_runner_v2_smoke_matrix_written_GR_null_baseline_sane_retained_pullback_rows_budgeted_no_local_GR_pass
```

Meaning:

```text
the fair-comparison local runner exists.
```

GR/null does not break the pipeline.

MTS retained pullback terms are now quantified as pressure rows.

The state is:

```text
not dead,
not passed,
sharper.
```

The most important pressure:

```text
eta_WEP remains the hardest always-relevant ready row.
```

The next theory decision is unavoidable:

```text
either local matter sees the identity/metric coframe,
or the class-metric pullback is retained as explicit closure/counterstress.
```

## 13. Next Target

Next:

```text
387 - Identity Coframe Or Class-Metric Fork
```

Aim:

```text
split the local theory honestly into:
1. strict identity/metric coframe branch,
2. retained class-metric pullback branch.
```

Pass condition:

```text
one branch gets a parent-action theorem route,
or the pullback branch is explicitly demoted to closure/counterstress.
```

Why this next:

```text
386 shows the local budgets are too tight for vague smallness.
```

So the next move must be structural:

```text
derive the local coupling architecture,
or stop pretending the local branch is derived GR.
```
