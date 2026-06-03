# 397 - Local Bound Runner v3 From Identity Stack

Private local-bound/runner checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 396 said the identity branch is coherent and runner-ready, but not derived local GR.

This checkpoint turns that audit into a machine-readable runner:

```text
runner-v3 =
  identity closure labels
  + retained EH/source/boundary/bulk/domain residuals
  + same-pipeline GR/null baseline
  + no false promotion.
```

The rule is simple:

```text
closure_zero is not derived_zero.
budget_only is not pass.
contingent_budget is not pass or fail unless the channel exists.
unscored_parameterized is not a scalar fifth-force score.
retained_residual is not local GR.
```

## 2. Run Manifest

Script:

```text
scripts/local_bound_runner_v3_from_identity_stack.py
```

Expected run directory:

```text
runs/<timestamp>-local-bound-runner-v3-from-identity-stack
```

Expected result files:

```text
results/source_register.csv
results/state_definitions.csv
results/runner_v3_matrix.csv
results/identity_closure_register.csv
results/retained_residual_families.csv
results/baseline_sanity_matrix.csv
results/residual_smoke_matrix.csv
results/scenario_summary.csv
results/suppression_budget_summary.csv
results/unscored_parameterized_rows.csv
results/promotion_policy.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Runner States

| State | Meaning | Claim policy |
|---|---|---|
| `derived_zero` | parent theorem derives zero/harmless form | usable only with all coupled rows closed |
| `closure_zero` | explicit branch assumption | no parent-derived claim |
| `conditional_theorem` | valid if extra premises are assumed | no promotion until premises derived |
| `retained_residual` | operator/coefficient remains | no local-GR pass |
| `budget_only` | source lock exists, coefficient missing | budget, not pass |
| `contingent_budget` | guardrail applies only if channel exists | guardrail only |
| `unscored_parameterized` | range/coupling/profile missing | no scalar score |
| `failed_open` | parent theorem absent | blocks promotion |

## 4. Runner-v3 Matrix

| Row | Observable | State | Source lock / status |
|---|---|---:|---|
| `R0` | `eta_WEP_direct_geometry` | `closure_zero` | `2.8e-15`, closure-labelled |
| `R1` | `eta_WEP_source_charge` | `contingent_budget` | `2.8e-15`, if source-charge channel exists |
| `R2` | `alpha_clock_redshift` | `budget_only` | `3.1e-5` |
| `R3` | `gamma_minus_1` | `budget_only` | `2.3e-5` |
| `R4` | `beta_minus_1` | `budget_only` | `7.8e-5` |
| `R5` | `alpha1` | `budget_only` | `1.0e-4` |
| `R6` | `alpha2` | `budget_only` | `2.0e-9` |
| `R7` | `alpha3` | `contingent_budget` | `4.0e-20`, if flux/nonconservation channel exists |
| `R8` | `xi` | `budget_only` | `4.0e-9` |
| `R9` | `Gdot/G` | `contingent_budget` | `9.6e-15 yr^-1`, if time-drift channel exists |
| `R10` | fifth-force / `delta_G` | `unscored_parameterized` | `alpha(lambda)` required |
| `R11` | non-EH operator coefficients | `retained_residual` | symbolic operator ledger |

This split matters. Direct WEP/coframe geometry is closed inside the identity branch, but source-charge WEP risk is not automatically closed.

## 5. Same-Pipeline Smoke

Runner-v3 keeps the same fairness rule as runner-v2:

```text
run GR/null baseline through the same evaluator first.
```

Smoke scenarios:

| Scenario | Purpose |
|---|---|
| `GR_null_baseline` | pipeline sanity |
| `identity_closure_zero_control` | closure row visibility |
| `one_tenth_budget_control` | safe toy retained coefficient |
| `edge_budget_control` | unstable edge case |
| `ten_times_over_budget_control` | explicit over-budget failure |
| `floor_leak_1e_minus_12` | shows which rows are brutal |
| `unit_coupling_stress` | order-one retained coupling must fail |

The GR/null baseline should be inside every numeric source lock. If it is not, the pipeline is bad before MTS is judged.

## 6. Retained Families

| Family | State | Rows |
|---|---:|---|
| EH operator residuals | `retained_residual` | `gamma`, `beta`, `xi`, fifth force, source normalization |
| source-normalization residuals | `retained_residual` | `delta_G`, `Gdot/G`, `beta`, fifth force, WEP-source |
| boundary/bulk residuals | `retained_residual` | `gamma`, `beta`, `alpha_i`, `xi`, fifth force |
| preferred-frame/domain residuals | budget/contingent | `alpha1`, `alpha2`, `alpha3`, `xi`, `Gdot/G` |
| fifth-force range residuals | `unscored_parameterized` | fifth-force / `delta_G` |

## 7. Promotion Policy

| Condition present | Promotion |
|---|---|
| `closure_zero` | internal branch testing only |
| `budget_only` | no pass |
| `contingent_budget` | guardrail only |
| `unscored_parameterized` | no fifth-force/`delta_G` pass |
| `retained_residual` | no local-GR pass |

Current runner-v3 has all of those states, so local-GR promotion is blocked by construction.

## 8. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| state definitions written | pass | runner-v3 states recorded |
| runner-v3 matrix written | pass | local rows/families emitted |
| identity closure label visible | pass | direct WEP/coframe row is `closure_zero` |
| GR/null baseline same evaluator | pass | numeric rows checked |
| unscored/retained rows preserved | pass | fifth-force and operator families retained |
| false pass blocked | pass | non-derived rows have `claim_allowed=false` |
| local-GR/PPN promoted | fail | no promotion allowed |
| claim ceiling enforced | pass | no WEP/EH/Newton/PPN/fifth-force/boundary/bulk/domain/local-GR pass |

## 9. Decision

Decision:

```text
local_bound_runner_v3_from_identity_stack_written_GR_null_baseline_sane_identity_closure_labelled_retained_residuals_budgeted_no_PPN_or_local_GR_pass
```

Interpretation:

```text
Runner-v3 now implements the post-identity local stack.
GR/null baseline is sane.
Direct coframe/WEP geometry is closure_zero by label.
Source-charge WEP, clock, gamma, beta, alpha_i, xi, Gdot/G,
fifth-force, and EH/operator families remain budgeted,
contingent, unscored, or retained.
No WEP, EH, Newtonian, PPN, fifth-force, boundary/bulk/domain,
or local-GR pass is claimed.
```

Claim ceiling:

```text
local_bound_runner_v3_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass
```

## 10. Next Target

398 - Parent Action Contract v2 After Identity Stack

Task:

```text
write the exact parent-action obligations needed to turn each runner-v3
closure/conditional/retained/budget/unscored row into a derived row.
```

Pass condition:

```text
every runner-v3 non-derived state has a parent-action obligation.
```
