# 383 - Local-Bound Runner V2 From Retained Residuals

Private local-bound/runner checkpoint. This is not a public WEP, PPN, preferred-frame, fifth-force, Einstein-Hilbert, boundary, bulk-field, source-normalization, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 382 wrote the parent local action contract.

That contract is useful because it says:

```text
if a parent-action premise is not derived,
the corresponding residual does not disappear.
```

It goes into a fallback row.

This checkpoint turns those fallback rows into a local-bound runner v2.

The runner separates:

```text
derived zero,
conditional zero,
closure zero,
budget-only,
contingent budget,
unscored parameterized.
```

That separation matters.

Without it, a closure assumption can accidentally be scored like a theorem.

Or a fifth-force row can be reduced to one fake scalar number.

Or a missing coefficient can be mistaken for a pass.

V2 blocks that.

Current result:

```text
retained residuals classified,
budget rows loaded,
fifth-force kept parameterized,
GR/null baseline policy recorded,
no PPN or local-GR pass claimed.
```

## 2. Machine Artifact

Script:

```text
scripts/local_bound_runner_v2_from_retained_residuals.py
```

Run:

```text
runs/20260602-011500-local-bound-runner-v2-from-retained-residuals
```

Outputs:

```text
results/source_register.csv
results/state_definitions.csv
results/retained_residual_runner_matrix.csv
results/derived_zero_branch_register.csv
results/pressure_ranking.csv
results/baseline_comparison_policy.csv
results/local_test_queue.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
local_bound_runner_v2_matrix_written_retained_residuals_classified_budget_only_no_PPN_or_local_GR_pass
```

Claim ceiling:

```text
local_bound_runner_v2_only_no_WEP_PPN_EH_fifth_force_boundary_bulk_source_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Runner States

The runner has seven allowed states:

| State | Meaning | Score policy |
|---|---|---|
| `derived_zero` | parent theorem derives zero | may be treated as zero if source path is recorded |
| `conditional_zero` | zero if a named premise is assumed | conditional branch only |
| `closure_zero` | zero by explicit closure axiom | labelled closure branch only |
| `budget_only` | numeric source lock exists but coefficient is missing | emit suppression budget, no pass |
| `contingent_budget` | guardrail applies only if channel exists | keep row; do not count unless derived |
| `unscored_parameterized` | needs range/coupling/profile | retain force-law contract, no scalar score |
| `failed_open` | no theorem, coefficient, or closure | blocks local-GR promotion |

This is the core discipline:

```text
not every zero is the same zero.
```

There is a huge difference between:

```text
derived zero
```

and:

```text
closure zero.
```

The runner keeps that difference visible.

## 4. Retained Residual Matrix

| Row | Observable | State | Source lock | Allowed output |
|---|---|---|---:|---|
| `R1` | `eta_WEP` | budget-only | `2.8e-15` | suppression budget only |
| `R2` | `alpha_clock_redshift` | budget-only | `3.1e-5` | budget only |
| `R3` | `gamma_minus_1` | budget-only | `2.3e-5` | budget only |
| `R4` | `beta_minus_1` | budget-only | `7.8e-5` | budget only |
| `R5` | `alpha1` | budget-only | `1.0e-4` | budget only |
| `R6` | `alpha2` | budget-only | `2.0e-9` | budget only |
| `R7` | `alpha3` | contingent budget | `4.0e-20` | only if channel exists |
| `R8` | `xi` | budget-only | `4.0e-9` | budget only |
| `R9` | `Gdot/G` | contingent budget | `9.6e-15 yr^-1` | only if time-variation channel exists |
| `R10` | `delta_G_or_fifth_force_yukawa` | unscored parameterized | `alpha(lambda)` | no scalar score |

Every numeric row still has:

```text
coefficient_status = missing.
```

Therefore every numeric row is:

```text
pressure,
not pass.
```

## 5. Main Pressure Ranking

The ready rows rank as:

| Rank | Observable | Scale | Meaning |
|---:|---|---:|---|
| 1 | `alpha3` | `4.0e-20` | brutal but contingent |
| 2 | `eta_WEP` | `2.8e-15` | hardest always-relevant ready row |
| 3 | `Gdot/G` | `9.6e-15 yr^-1` | contingent time-drift row |
| 4 | `alpha2` | `2.0e-9` | strong preferred-frame row |
| 5 | `xi` | `4.0e-9` | preferred-location/aniso row |
| 6 | `gamma_minus_1` | `2.3e-5` | classic PPN light/curvature row |
| 7 | `alpha_clock_redshift` | `3.1e-5` | clock/redshift row |
| 8 | `beta_minus_1` | `7.8e-5` | second-order/radial row |
| 9 | `alpha1` | `1.0e-4` | preferred-frame row |

But the practical top theorem target is still:

```text
eta_WEP.
```

Why?

Because `alpha3` and `Gdot/G` are contingent.

`eta_WEP` is active as soon as one-coframe/common-species coupling is not derived.

So WEP remains the knife at the throat.

Friendly knife.

But still a knife.

## 6. Fifth-Force Policy

The fifth-force row remains:

```text
unscored_parameterized.
```

It cannot become a scalar score until MTS derives one of:

```text
alpha_Y(lambda_Y),
alpha_X(lambda_X),
a source-normalized nonlocal spectral kernel,
or a theorem-zero/no-force result.
```

So:

```text
delta_G_or_fifth_force_yukawa
```

is retained as a force-law contract.

Not a pass.

Not a fail.

Not a one-number scoreboard.

## 7. Conditional-Zero Register

The runner records the conditional zero branches:

| Branch | Would zero | Missing premise |
|---|---|---|
| one coframe if parent-selected | direct WEP/clock/nonmetric matter vertices | one coframe/common `F(C_D)` not derived |
| `phi_C` zero theorem | common-mode gradients | boundary-state/trivial-class theorem not parent-derived |
| class-only boundary | `B_TF`, `B_0i` sources | class-only boundary action not parent-derived |
| bulk-X mass gap | source-free regular bulk `X` hair | positive/source-free operator not parent-derived |
| EH full stack | non-EH local operator coefficients | full local-GR stack not closed |

This is useful because it shows where a future theorem lands.

If one of these premises is derived, the runner can move a row from:

```text
budget_only
```

to:

```text
derived_zero.
```

Until then, no row gets that upgrade.

## 8. Baseline Policy

The runner now has an explicit baseline rule:

| Policy | Meaning |
|---|---|
| GR baseline explicit | each row records the GR/null value |
| same pipeline when possible | future tests should run the GR/null branch through the same code path |
| no fifth-force shortcut | range/coupling/profile required |
| closure label visible | closure zero never becomes derived zero |
| budget not pass | source locks produce ceilings, not victories |

This addresses the fair-comparison point:

```text
if GR also fails a pipeline, inspect the pipeline.
if only MTS fails, the branch owes repair.
if MTS ties within labelled budget, that is a useful defensive round.
```

That is the clean Mayweather route.

No fake haymakers.

## 9. Local Test Queue

The next local tests should be:

| Priority | Test | Rows | Output |
|---:|---|---|---|
| 1 | WEP species budget stress | `eta_WEP` | symbolic/numeric budget matrix |
| 2 | boundary/bulk gamma-beta budget | `gamma`, `beta` | coefficient sensitivity matrix |
| 3 | preferred-frame / `xi` budget | `alpha1`, `alpha2`, `alpha3`, `xi` | source-locked coefficient budgets |
| 4 | source-normalization guard | `Gdot/G`, fifth-force | contingent/unscored guardrail |
| 5 | GR/null baseline pipeline | all numeric-ready rows | baseline sanity check |

None of these are pass/fail claims yet.

They are stress tests.

The job is to find which residuals are survivable, which need theorem-zero, and which are too expensive to carry.

## 10. Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source paths exist |
| state definitions written | pass | seven runner states defined |
| retained residual matrix written | pass | ten retained observable rows classified |
| numeric budget rows loaded | pass | seven budget-only rows and two contingent rows |
| unscored parameterized rows retained | pass | fifth-force/delta-G row requires range/coupling/profile |
| baseline policy written | pass | GR/null baseline and same-pipeline policy recorded |
| pass claims blocked | pass | coefficients missing and states conditional |
| local GR or PPN promoted | fail | parent-action contract remains unsatisfied |
| claim ceiling enforced | pass | no WEP/PPN/EH/fifth-force/boundary/bulk/source/local-GR pass |

## 11. Decision

Decision:

```text
local_bound_runner_v2_matrix_written_retained_residuals_classified_budget_only_no_PPN_or_local_GR_pass
```

Meaning:

```text
the local empirical side now has a disciplined runner matrix.
```

It can apply pressure.

It cannot flatter the theory.

It separates:

```text
derived zeros,
conditional zeros,
closure zeros,
budgets,
contingent rows,
and unscored force laws.
```

No promotion:

```text
WEP not passed,
PPN not passed,
preferred-frame not passed,
fifth-force not scored,
EH not derived,
local GR not derived.
```

## 12. Next Target

Next:

```text
384 - Parent Action First Variation Obstruction Map
```

Aim:

```text
attempt the first explicit variation of the minimal parent action contract
and identify which block obstructs closure first.
```

Why this next:

```text
383 gives the runner.
```

But the route to derived local GR still needs:

```text
variation,
not just classification.
```

So the next move is to take the 382 contract and ask:

```text
when we vary it, where does the first unavoidable unowned term appear?
```
