# 96 - Parent R Normalization Contract

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 95 found:

```text
a_F = 1 is the cleanest canonical closure choice,
but it is not parent-derived.
```

The hard obstruction was:

```text
R -> c_R R
a_F -> a_F / c_R
```

which leaves:

```text
a_F DeltaR
```

unchanged.

This checkpoint writes the exact contract a future parent action must satisfy to kill that degeneracy.

## 2. Short Verdict

```text
contract_status =
R_normalization_contract_written_not_derived
```

```text
promotion_allowed =
false
```

Plain English:

```text
We now know exactly what the parent action must prove. It must fix the field metric of m, the zero and unit scale of R, the unit trace projection coefficient, and the endpoint solution before cosmology fitting. The contract is sharp, but not yet satisfied.
```

Boxing-score version:

```text
This is a corner-instruction round. We did not land the theorem, but we stopped shadow-boxing: the next punch is now precisely defined.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\parent_R_normalization_contract.py
```

Run:

```text
research-programme\runs\20260531-134620-parent-R-normalization-contract
```

Generated:

```text
source_checkpoint_register.csv
flrw_eta1_product_inputs.csv
parent_R_contract_clauses.csv
candidate_theorem_routes.csv
degeneracy_breakers.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
R_normalization_contract_written_not_derived
```

## 4. The Contract

For `a_F=1` to become more than a convention, a future parent action must satisfy all of:

| Clause | Required statement | Status |
|---|---|---|
| C0 | `[Gamma_eff]=L^-2`, `[L_cg]=L`, `R` and `F` dimensionless, and `K_MTS` owns the trace/tensor split | partial scaffold |
| C1 | parent action fixes the coordinate/metric of `m`, e.g. a canonical or invariant field-space metric `G_mm(m,X_B)` | missing |
| C2 | `R(m_L;X_B)=0` or `R_L(X_B)` is fixed by the action, not chosen after fitting | conditional |
| C3 | `R` has a parent-fixed unit scale, e.g. `0<=R-R_L<=1` or a normalized boundary charge equals one | missing |
| C4 | the same `R` drives memory relaxation: `nabla_mu J_m^mu = -gamma_B delta R/delta m + [1-Pi_B]S_cg` | conditional |
| C5 | unit trace projection: `Gamma_eff=L_cg^-2[F_L+(R-R_L)]` | missing |
| C6 | a Ward/Noether/coarse-graining identity forbids independent `a_F` | missing |
| C7 | local guard: `F_2=lambda_R` is PPN-safe, preferably by high `gamma_B`, not huge `lambda_R` | conditional guard |
| C8 | endpoint equations predict `DeltaR=0.223600` to `0.460135` for `a_F=1` before SN+BAO | missing |
| C9 | `R` scale, `a_F`, `lambda_R`, `gamma_B`, and endpoints are fixed before data scoring | policy pass, theory missing |

So the actual promotion path is not vague:

```text
C1 + C3 + C5 + C6 + C8
```

are the theorem debt.

## 5. Degeneracy Breakers

| Degeneracy | Transformation | Required breaker |
|---|---|---|
| additive `R` shift | `R -> R + c0(X_B)` | action-fixed `R_L` or `R(m_L;X_B)=0` |
| multiplicative `R` scale | `R -> c_R R`, `a_F -> a_F/c_R` | normalized charge, bounded contrast, or Ward-fixed trace coefficient |
| `m` coordinate scale | `m -> c_m m` | parent field metric or kinetic term |
| cosmology/local split | keep `a_F DeltaR` fixed while changing `a_F lambda_R` | same `R` controls endpoint amplitude and local `F_2` |
| post-fit endpoint choice | choose `DeltaR` after seeing `B_mem` | parent endpoint solution predicts `DeltaR` before fitting |

The main enemy is still:

```text
multiplicative R scale.
```

Until that is broken, `a_F=1` is clean bookkeeping, not physics.

## 6. Candidate Theorem Routes

| Route | Would fix | Current status |
|---|---|---|
| field metric plus potential | `m` units, `lambda_R`, `Delta m`, local `F_2` bookkeeping | best primary route |
| normalized boundary charge | `R` unit scale and `DeltaR` cap | best amplitude route |
| trace-projection Ward identity | `a_F=1` | needed for promotion |
| relative entropy/distance functional | positive sign and possibly bounded contrast | speculative candidate |
| pure canonical convention | bookkeeping only | closure fallback |

The best theorem route is therefore a three-part lock:

```text
field metric for m
normalized boundary charge for R
Ward identity for the trace projection coefficient
```

If any one of those is missing, the amplitude remains closure-level.

## 7. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `exact_contract_written` | pass | C0-C9 now specify what must be proved |
| `source_paths_exist` | pass | all cited source checkpoints exist |
| `R_additive_zero_condition` | pass conditional | `R-R_L` is used consistently, but action-level zero fixing remains open |
| `R_unit_scale_derived` | fail | no parent charge/metric kills `R -> c_R R` yet |
| `aF_equals_1_derived` | fail | unit trace coefficient remains canonical closure |
| `Ward_identity_available` | fail | no identity fixes `partial Gamma_eff/partial R=L_cg^-2` |
| `local_F2_guard_preserved` | pass conditional | `F_2=lambda_R` plus high-mobility screening remains the safe route |
| `DeltaR_predicted_pre_fit` | fail | `DeltaR` range still comes from fitted `B_mem` |
| `closure_use_allowed` | pass | `a_F=1` can be used as a labelled canonical closure |
| `support_claim_allowed` | fail | contract-only status is not field-theory promotion |

## 8. Interpretation

Allowed statement:

```text
The MTS post-checkpoint cosmology branch has an explicit parent-action contract for promoting the canonical amplitude choice eta=1, a_F=1.
```

Forbidden statement:

```text
MTS has derived eta=1, a_F=1, and DeltaR from the parent action.
```

Reason:

```text
eta=1 is conditional on the L_cg Hubble cap;
a_F=1 is still a trace-normalization convention;
DeltaR is still inferred from fitted B_mem.
```

The value of this checkpoint is discipline:

```text
future work cannot wave at "parent action" generally.
It must satisfy C1, C3, C5, C6, and C8 specifically.
```

## 9. Current Best Private Branch

For testing, the cleanest labelled closure remains:

```text
eta = 1
a_F = 1
DeltaR = 0.223600 to 0.460135
```

This is not arbitrary-looking anymore.

But the exact label must be:

```text
canonical closure branch,
not derived amplitude branch.
```

## 10. Decision

Decision:

```text
contract_status =
R_normalization_contract_written_not_derived
```

Decision:

```text
allowed_closure =
a_F = 1 with DeltaR target 0.223600 to 0.460135
```

Decision:

```text
promotion_blocker =
missing R unit scale and missing trace projection Ward identity
```

Decision:

```text
primary_theorem_route =
field_metric_plus_normalized_boundary_charge_plus_trace_projection_Ward_identity
```

## 11. Next Target

Create:

```text
97-canonical-R-theorem-attempt.md
```

Purpose:

```text
attempt the primary theorem route: can a parent field metric plus normalized boundary charge plus trace-projection identity actually fix R and make a_F=1 unavoidable?
```

Pass condition:

```text
at least one concrete parent-action construction breaks the R-rescaling degeneracy without using SN+BAO amplitudes.
```

Fail condition:

```text
no construction breaks the degeneracy; a_F=1 is permanently demoted to explicit canonical closure for empirical testing.
```
