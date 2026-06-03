# 396 - Local-GR Reduction Sufficiency Stack Audit

Private local-GR sufficiency checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoints 391-395 cleaned the GR-facing identity branch:

```text
identity coframe closes the direct matter/coframe pullback by label.
EH, source, boundary, bulk, preferred-frame, domain, fifth-force, and PPN debts remain.
```

This checkpoint is the referee:

```text
Are we now at derived local GR?
```

Answer:

```text
No.
```

But we are at a useful place:

```text
the local-GR programme is coherent,
the residual vector is finite,
the runner-v3 inputs are now explicit,
and no hidden promotion is needed.
```

## 2. Run Manifest

Script:

```text
scripts/local_GR_reduction_sufficiency_stack_audit.py
```

Expected run directory:

```text
runs/<timestamp>-local-GR-reduction-sufficiency-stack-audit
```

Expected result files:

```text
results/source_register.csv
results/status_legend.csv
results/local_GR_sufficiency_stack.csv
results/promotion_gate_matrix.csv
results/observable_row_rollup.csv
results/theorem_vs_closure_inventory.csv
results/runner_v3_readiness.csv
results/failure_to_action_map.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

## 3. Status Legend

| Status | Meaning |
|---|---|
| `derived_zero` | parent theorem derives zero or harmless form |
| `closure_zero` | explicit branch assumption; useful for tests, not public theorem |
| `conditional_theorem` | theorem shape works if premises are assumed |
| `retained_residual` | coefficient/operator remains in modified-gravity ledger |
| `budget_ready` | source lock exists, but MTS coefficient is missing |
| `unscored_parameterized` | force/range/source profile missing |
| `failed_open` | parent premise not derived and blocks promotion |

## 4. Sufficiency Stack

| Rung | Premise | Current status | Runner-v3 state |
|---:|---|---:|---|
| 1 | identity/parent-selected observed coframe | `closure_zero` | direct WEP/coframe row closure-labelled |
| 2 | EH operator selection | `failed_open` | non-EH operator coefficients retained |
| 3 | source-normalized Newtonian limit | `conditional_theorem` | `delta_G/Gdot/beta/fifth-force` rows retained |
| 4 | boundary no-hair | `conditional_theorem` | boundary coefficients retained |
| 5 | bulk-X no-hair or scored force | `unscored_parameterized` | bulk-X or force-law row retained |
| 6 | preferred-frame/domain/projector no-hair | `budget_ready` | `alpha_i/xi/Gdot` rows retained |
| 7 | fifth-force range/coupling | `unscored_parameterized` | `alpha(lambda)` still missing |
| 8 | PPN coefficient derivation | `budget_ready` | runner-ready, no pass |
| 9 | total Ward force closure | `retained_residual` | Ward/flux rows retained |

This is the honest stack. Only one item is actually closed in the identity branch, and even that is closure-labelled rather than parent-derived.

## 5. Promotion Gates

| Promotion | Current result | Allowed claim | Forbidden claim |
|---|---:|---|---|
| identity branch testing | allowed internal | identity-branch runner can be tested | parent-derived WEP |
| WEP parent-derived | fail | none | public WEP pass |
| EH local operator | fail | conditional theorem shape | EH derived |
| source-normalized Newtonian limit | fail | weak-field algebra/contract | Newtonian reduction derived |
| boundary/bulk no-hair | fail | conditional kill switches | no-hair pass |
| preferred-frame/domain pass | fail | source-locked budgets | preferred-frame PPN pass |
| fifth-force pass | fail | parameterized unscored row | fifth-force passed |
| local-GR reduction | fail | coherent test programme | MTS reduces to GR locally |

So the boxing read is: MTS is still in the fight, moving much cleaner, but the judges cannot award “local GR reduction” yet.

## 6. Observable Rollup

| Row | Post-396 state |
|---|---|
| `eta_WEP` | direct coframe row closure-zero only inside identity branch |
| `alpha_clock` | budget/closure-dependent, no pass |
| `gamma-1` | retained budget-only |
| `beta-1` | retained budget-only |
| `alpha1` | retained budget-only |
| `alpha2` | retained budget-only |
| `alpha3` | retained contingent budget |
| `xi` | retained budget-only, not folded into `gamma` |
| `Gdot/G` | retained contingent budget |
| fifth-force/`delta_G` | unscored parameterized until `alpha(lambda)` or source theorem exists |

## 7. What Is Strong

The current branch has real structure:

- The direct WEP/coframe problem is isolated and closure-labelled, not mixed with the rest.
- EH selection is separated from WEP, so no fake “matter sees metric therefore GR” shortcut.
- Source normalization now has explicit weak-field algebra.
- Boundary and bulk are joined into one force/flux contract.
- Preferred-frame rows are fairer because coframe slip is not double-counted.
- Runner-v3 can now be built without smuggling a public claim.

## 8. What Still Blocks Local GR

The hard blockers are:

```text
EH operator parent derivation,
constant universal source normalization,
boundary radial/flux no-hair,
bulk-X theorem-zero or alpha_X(lambda_X),
domain/projector/vector gauge/topology/Ward ownership,
fifth-force alpha(lambda),
parent-derived PPN coefficients.
```

None of those are impossible by inspection, but none are currently earned.

## 9. Runner-v3 Readiness

Runner-v3 should now use:

| Component | Input status |
|---|---|
| GR/null baseline | ready from runner-v2 smoke |
| identity branch labels | ready from 391/395 |
| operator residuals | ready from 392 |
| source-normalization rows | ready from 393 |
| boundary/bulk rows | ready from 394 |
| preferred-frame/domain rows | ready from 395 |
| promotion policy | ready from this audit |

Acceptance rule:

```text
No row with closure-only, conditional, retained, budget-only, or unscored status may be treated as a local-GR pass.
```

## 10. Gate Results

| Gate | Status | Evidence |
|---|---:|---|
| source paths exist | pass | all cited source paths exist |
| status legend written | pass | status classes recorded |
| local-GR stack classified | pass | sufficiency rungs classified |
| identity branch runner-ready | pass | closure labels and residual policies explicit |
| blocking rungs remain | fail | EH/source/boundary/bulk/domain/fifth-force/PPN/Ward debts remain |
| observable rollup written | pass | local rows rolled up |
| runner-v3 readiness written | pass | runner components specified |
| local-GR promoted | fail | no promotion allowed |
| claim ceiling enforced | pass | no WEP/EH/Newton/PPN/fifth-force/boundary/bulk/domain/local-GR pass |

## 11. Decision

Decision:

```text
local_GR_reduction_sufficiency_stack_audit_written_identity_branch_clean_but_EH_source_boundary_bulk_domain_PPN_gates_open_runner_v3_ready_no_local_GR_pass
```

Interpretation:

```text
The identity branch is clean enough for runner-v3.
It is not derived local GR.
Direct coframe/WEP pullback is closure-zero by label.
EH, source normalization, boundary, bulk, domain/projector,
fifth-force, PPN coefficients, and total Ward closure remain open.
The framework is coherent and test-ready as a residual stack.
No local-GR claim is allowed.
```

Claim ceiling:

```text
local_GR_sufficiency_stack_audit_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass
```

## 12. Next Target

397 - Local Bound Runner v3 From Identity Stack

Task:

```text
implement runner-v3 with identity-branch closures,
retained EH/source/boundary/bulk/domain residuals,
same-pipeline GR/null baseline,
and no promotion.
```

Pass condition:

```text
all retained local rows are emitted as derived_zero, closure_zero,
conditional, budget_only, contingent_budget, retained_residual,
or unscored_parameterized with no false pass.
```
