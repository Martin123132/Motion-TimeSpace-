# 369 - Source-Locked Closure-Branch Local-Bound Runner

Private runner checkpoint. This is not a public WEP, clock, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 368 wrote the residual gate for the labelled class-metric branch:

```text
ghat_mn = exp(phi_C) g_mn.
```

This checkpoint turns the gate into a runner.

The runner rule is:

```text
ready source-locked rows get budgets,
quarantined rows stay visible but unscored,
missing coefficients block pass claims.
```

This is the fair local scorecard.

It does not claim local GR.

## 2. Machine Artifact

Script:

```text
scripts/source_locked_closure_branch_local_bound_runner.py
```

Run:

```text
runs/20260601-221000-source-locked-closure-branch-local-bound-runner
```

Outputs:

```text
results/source_register.csv
results/runner_policy.csv
results/ready_budget_rows.csv
results/quarantine_rows.csv
results/pressure_ranking.csv
results/baseline_comparison_rows.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
closure_branch_local_bound_runner_built_budget_only_no_coefficients_no_pass_claim
```

Claim ceiling:

```text
source_locked_closure_runner_only_no_WEP_clock_PPN_fifth_force_EH_or_local_GR_pass
```

Source paths missing:

```text
0
```

## 3. Runner Policy

| Policy | Meaning |
|---|---|
| ready rows are budgets | source-locked scales exist, but MTS coefficients are missing |
| quarantined rows are retained | preferred-frame, `xi`, and fifth-force stay visible but unscored |
| closure labels visible | class metric is closure/theorem target, not derived local GR |
| GR baseline explicit | GR is the comparison target; MTS must earn suppression |
| missing coefficients block pass | no coefficient, no local-bound pass |

This is the important discipline move:

```text
the runner is allowed to pressure the theory,
but not allowed to flatter it.
```

## 4. Ready Budget Rows

| Residual | Source-locked scale | Terms | Equal-share ceiling | Status |
|---|---:|---:|---:|---|
| `eta_WEP` | `2.8e-15` | 3 | `9.33333e-16` | hardest ready gate, budget only |
| `gamma_minus_1` | `2.3e-5` | 4 | `5.75e-6` | budget only |
| `alpha_clock_redshift` | `3.1e-5` | 2 | `1.55e-5` | budget only |
| `beta_minus_1` | `7.8e-5` | 3 | `2.6e-5` | budget only |

The equal-share ceiling is not physics.

It is an engineering guardrail:

```text
if there are N unknown unit-scale residual terms,
each term must fit under target/N.
```

Every ready row has:

```text
coefficient_status = missing.
```

Therefore:

```text
pass_claim_allowed = no.
```

## 5. Quarantined Rows

| Residual | Why quarantined |
|---|---|
| preferred-frame `alpha1/alpha2` | no numeric source lock here; marker/projector covariance not proved |
| preferred-location / anisotropy `xi` | no numeric source lock here |
| `delta_G` / fifth force | no dedicated source lock or force coefficient map here |

This prevents fake precision.

These rows are not safe.

They are simply not scored yet.

## 6. Pressure Ranking

The ready rows rank by source-locked scale:

| Rank | Residual | Scale |
|---:|---|---:|
| 1 | `eta_WEP` | `2.8e-15` |
| 2 | `gamma_minus_1` | `2.3e-5` |
| 3 | `alpha_clock_redshift` | `3.1e-5` |
| 4 | `beta_minus_1` | `7.8e-5` |

So the hardest loaded local round remains:

```text
WEP / species universality.
```

That matches the theory side:

```text
representative invariance helps,
but species-specific F_A(C_D) is still not parent-forbidden.
```

## 7. Baseline Comparison

| Arena | Baseline | MTS closure requirement |
|---|---|---|
| local GR | `gamma=1`, `beta=1`, no WEP/clock violation | residual vector below source-locked budgets |
| universal matter | one metric/coframe | derive universal `F(C_D)` and no representative vertices |
| exterior operator | Einstein-Hilbert local dynamics | derive EH or retain/bound residual operator |
| stress pipeline | apply comparable baseline tests where possible | do not mistake pipeline failure for MTS-only failure |

This is the boxing-score version:

```text
if GR also fails a test pipeline, the pipeline is suspect.
if only MTS fails, the branch owes a repair.
if MTS ties within budget, that is a good defensive round.
```

## 8. What Blocks A Pass

Every pass claim is currently blocked by at least one of:

```text
missing residual coefficients,
missing common-mode phi_C gradient bound,
species universality not derived,
preferred-frame / xi / fifth-force source locks missing,
Einstein-Hilbert exterior operator not derived.
```

So the runner status is:

```text
budget-only local pressure runner.
```

Not:

```text
PPN pass.
```

## 9. Decision

Decision:

```text
closure_branch_local_bound_runner_built_budget_only_no_coefficients_no_pass_claim
```

Meaning:

```text
the class-metric closure branch now has a source-locked local-bound runner
with four budget rows and three quarantined rows.
```

No promotion:

```text
WEP not passed,
clock not passed,
PPN not passed,
fifth-force not scored,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 10. Next Target

Next:

```text
370 - Common-Mode phi_C Coefficient Map
```

Aim:

```text
derive or parameterize local phi_C gradients against Newtonian potential,
then map coefficients into clock, gamma, beta, and fifth-force rows.
```

That is the next useful testing step.

The runner now exists.

The branch must now put numbers, zero theorems, or explicit failures into the rows.
