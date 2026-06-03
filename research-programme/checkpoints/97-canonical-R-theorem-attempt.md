# 97 - Canonical R Theorem Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 96 wrote the contract:

```text
field metric for m
normalized boundary charge for R
trace-projection Ward identity
```

and asked whether these can actually fix:

```text
a_F = 1
```

instead of merely choosing it.

## 2. Short Verdict

```text
theorem_status =
canonical_R_theorem_not_derived
```

```text
aF1_status =
explicit_canonical_closure_for_empirical_testing
```

```text
promotion_allowed =
false
```

Plain English:

```text
The three-part theorem route gives a clean conditional theorem schema, but not a completed parent-action construction. The current corpus still lacks a normalized boundary charge Q_* and lacks a Ward identity fixing partial Gamma_eff/partial R = L_cg^-2.
```

So `a_F=1` is now officially demoted to a labelled canonical closure, not a derived amplitude.

Boxing-score version:

```text
We threw the proper punch and it did not land clean. But this is not a canvas job. We forced the amplitude branch into honest shape: no fake theorem, no hidden knob, still testable.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\canonical_R_theorem_attempt.py
```

Run:

```text
research-programme\runs\20260531-135201-canonical-R-theorem-attempt
```

Generated:

```text
source_checkpoint_register.csv
flrw_eta1_product_inputs.csv
theorem_attempts.csv
conditional_theorem_chain.csv
no_go_tests.csv
closure_label_register.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
canonical_R_theorem_not_derived_aF1_demoted_to_closure
```

## 4. What Was Tried

| Attempt | Would fix | Result |
|---|---|---|
| field metric plus potential | `m` scale, `lambda_R`, local `F_2` bookkeeping | partial template |
| normalized boundary charge | `R` unit scale and `DeltaR` cap | conditional only |
| trace-projection Ward identity | `a_F=1` | missing |
| relative entropy/distance functional | positivity and bounded contrast | speculative, unavailable |
| combined three-part theorem | `a_F=1` and `DeltaR=0.223600` to `0.460135` | conditional schema only |
| pure canonical redefinition | bookkeeping discipline | valid closure fallback |

The closest theorem schema is:

```text
S_m fixes the field metric of m;
Q_* fixes the unit boundary charge scale of R;
Ward identity fixes partial Gamma_eff/partial R = L_cg^-2;
therefore a_F = 1.
```

But the current corpus supplies only the schema, not the missing theorem pieces.

## 5. Conditional Theorem Chain

The chain would be:

```text
1. Parent field metric fixes m units.
2. R(m_L;X_B)=0 fixes additive zero.
3. Normalized boundary charge fixes R unit scale.
4. Same R drives relaxation and trace projection.
5. Ward identity fixes partial Gamma_eff/partial R = L_cg^-2.
6. Therefore a_F=1 is forced.
7. Parent endpoint equations predict DeltaR.
8. B_mem = DeltaR/3 on eta=1, a_F=1 branch.
```

Current status:

```text
steps 2 and 4 are conditional;
steps 1, 3, 5, and 7 are not derived;
step 6 therefore fails;
step 8 is identity-only, not prediction.
```

That is the decisive result.

## 6. No-Go Tests

| Test | Finding | Result |
|---|---|---|
| Noether identity alone | relates field equations but does not fix a numerical coefficient | fail as derivation |
| field metric alone | fixes `m` units but leaves `R` scale as a coupling | partial only |
| bounded contrast assumption | gives useful `a_F` bounds but does not derive them | closure only |
| action coefficient rescaling | `c_R R` can be absorbed unless `c_R` is fixed | fail as derivation |
| post-fit endpoint matching | choosing `DeltaR` after `B_mem` is circular | fail as prediction |

Important warning:

```text
writing down an action term is not enough.
```

The coefficient must be owned.

## 7. Closure Demotion

The branch label is now:

```text
canonical_R_closure
```

with fixed choices:

```text
eta = 1
a_F = 1
p = 3
u3 = 1/4
```

Derived or conditionally derived parts:

```text
p=3                  conditional shape route;
u3=1/4               conditional cell route;
eta=1                conditional FLRW L_cg route.
```

Closure parts:

```text
a_F=1                canonical convention;
DeltaR               read from fitted B_mem;
R unit scale          not parent-derived.
```

Allowed use:

```text
fair empirical scorecard branch with transparent amplitude debt.
```

Forbidden use:

```text
field-theory support claim from B_mem amplitude.
```

## 8. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `theorem_attempt_made` | pass | field metric, normalized boundary charge, and Ward identity routes were tested |
| `field_metric_constructed` | partial | template fixes `m` scale in principle, not `R` scale or trace coefficient |
| `normalized_boundary_charge_derived` | fail | no theorem fixes `Q_*` independently of `B_mem` |
| `trace_projection_Ward_identity_derived` | fail | no identity fixes `partial Gamma_eff/partial R=L_cg^-2` |
| `R_rescaling_degeneracy_broken` | fail | `R->c_R R` remains unbroken |
| `DeltaR_predicted_pre_fit` | fail | target still comes from fitted `B_mem` |
| `concrete_parent_action_found` | fail | only a conditional schema was found |
| `aF1_demoted_to_closure` | pass | `a_F=1` is explicitly labelled canonical closure |
| `empirical_testing_allowed` | pass | closure is disciplined enough for scorecard tests |
| `support_claim_allowed` | fail | amplitude support remains blocked |

## 9. Interpretation

Allowed statement:

```text
MTS has a disciplined canonical-R closure branch: eta=1, a_F=1, p=3, u3=1/4, with transparent amplitude debt.
```

Forbidden statement:

```text
MTS derives a_F=1 or predicts B_mem from the parent action.
```

Reason:

```text
the normalized boundary charge and trace-projection Ward identity are not derived.
```

This is a useful narrowing:

```text
the branch is no longer a loose fit;
it is a labelled closure with known theorem debts and a clear empirical role.
```

## 10. Decision

Decision:

```text
canonical_R_theorem =
not derived
```

Decision:

```text
a_F = 1 =
explicit canonical closure for empirical testing
```

Decision:

```text
DeltaR target for future theorem =
0.223600 to 0.460135
```

Decision:

```text
main failure =
missing normalized boundary charge and missing trace-projection Ward identity
```

## 11. Next Target

The highest-value next step is no longer another broad amplitude theorem.

Choose one of two disciplined routes:

```text
Route A: empirical scorecard retest using the labelled canonical_R_closure branch;
Route B: narrower normalized-boundary-charge theorem attempt.
```

Recommendation:

```text
Route A first.
```

Reason:

```text
the theorem route just failed at the missing Q_* and Ward identity. The closure is now honest enough to return to testing and ask whether it stays competitive as a labelled branch.
```

Concrete next file:

```text
98-canonical-R-closure-scorecard-plan.md
```

Purpose:

```text
define the exact fair retest matrix for canonical_R_closure against LCDM, wCDM, CPL, and existing MTS variants, with no amplitude-promotion language.
```
