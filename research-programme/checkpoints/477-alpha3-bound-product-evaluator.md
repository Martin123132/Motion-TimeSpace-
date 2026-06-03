# 477 - Alpha3 Bound Product Evaluator

Private alpha3/PPN bound checkpoint. This is not a public alpha3 pass, PPN pass, Newtonian-limit pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `476` wired the coefficient runner but left the hardest row unresolved:

```text
abs(W_domain_alpha3 * epsilon_domain_flux) <= 4e-20.
```

This checkpoint turns the alpha3 row into a strict evaluator.

Short answer:

```text
Evaluator yes.
Alpha3 pass no.
Boundary and domain products are still missing.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/alpha3_bound_product_evaluator.py` |
| Run directory | `runs\20260603-013000-alpha3-bound-product-evaluator` |
| Status | `alpha3_bound_product_evaluator_written_boundary_and_domain_inputs_missing_no_mu_extra_PPN_Newton_or_local_GR_pass` |
| Claim ceiling | `alpha3_bound_product_evaluator_only_no_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass` |
| Next target | `478-determinant-current-parent-ownership-or-demotion.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md | True | boundary alpha3 scalar/no-flux lemma and missing parent ownership |
| 472-domain-projector-alpha3-no-leak-or-R11-link.md | True | domain alpha3 no-leak attempt and R11 link requirement |
| 473-R11-domain-projector-operator-vector-minimum-fill.md | True | R11 domain rows exist but are not claim-valid |
| 476-double-zero-memory-coupling-origin-or-coefficient-runner.md | True | p>=2 memory gate requirement and missing numeric products |
| source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv | True | source-locked alpha3 bound rows |
| source-intake\mts_residuals\P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv | True | boundary/domain/total alpha3 fill skeleton |
| source-intake\mts_residuals\P8_mu_extra_boundary_coefficients.csv | True | boundary alpha3 coefficient/theorem row |
| source-intake\mts_residuals\P8_mu_extra_domain_projector_coefficients.csv | True | domain alpha3 coefficient/theorem row |
| source-intake\mts_residuals\P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_INPUT.csv | True | latest domain coefficient runner input template |
| source-intake\mts_residuals\P8_DOUBLE_ZERO_COEFFICIENT_RUNNER_RESULTS.csv | True | latest domain coefficient runner result status |
| source-intake\mts_residuals\R11_nonEH_operator_vector_executable.csv | True | R11 vector path; parseable but zero claim-valid rows |
| scripts/alpha3_bound_product_evaluator.py | True | this checkpoint generator |

## 4. The Rule

For each active alpha3 source channel:

```text
abs(W_i_alpha3 * epsilon_i_flux) <= 4e-20
```

or:

```text
theorem-zero source accepted by explicit parent-premise gates.
```

No post-fit cancellation is allowed unless a parent identity exists before scoring.

## 5. Theorem-Zero Gates

| gate_id | channel | theorem_zero_route | required_premises | current_status | accepted_as_zero | blocking_reason |
| --- | --- | --- | --- | --- | --- | --- |
| TG_boundary_zero | boundary_monopole_shift | scalar stationary boundary action with no tangential vector, no normal momentum flux, full stress variation | scalar-only boundary data; no material marker; stationary compact collar; Ward/boundary flux closure | conditional_lemma_not_parent_owned | false | 470 boundary lemma is conditional and no numeric product is supplied |
| TG_domain_zero | domain_projector_mass | p>=2 memory gate plus local zero plus topological projector plus R11 source-normalization silence | double-zero parent origin; local b_D=0 or c_D=0; metric-independent P_MTS,D; R11 valid rows | not_parent_derived | false | 476 derives p>=2 as a requirement only; local zero/topological/R11 gates remain open |
| TG_total_cancellation | combined_mu_extra_alpha3 | parent identity forcing alpha3_boundary + alpha3_domain + other channels = 0 | identity before fitting; common normalization; no post-hoc cancellation | not_present | false | policy requires individual channel pass unless parent cancellation identity is derived |

No theorem-zero gate is accepted in the current corpus.

## 6. Product Inputs

| input_id | channel | target_row | observable | product_symbol | coefficient_symbol | epsilon_symbol | coefficient_value | epsilon_value | explicit_product_value | theorem_zero_status | premise_status | target_bound | source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A3_boundary | boundary_monopole_shift | R7_alpha3 | alpha3 | W_boundary_alpha3_epsilon_boundary_flux | W_boundary_alpha3 | epsilon_boundary_flux | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | 0_IF_SCALAR_STATIONARY_BOUNDARY_PREMISES_ARE_PARENT_OWNED_ELSE_MISSING_NUMERIC_PRODUCT | conditional_zero_lemma_parent_owner_missing | 4e-20 | 470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md |
| A3_domain | domain_projector_mass | R7_alpha3 | alpha3 | W_domain_alpha3_epsilon_domain_flux | W_domain_alpha3 | epsilon_domain_flux | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | 0_IF_PARENT_DERIVES_P_GE_2_GATE_AND_LOCAL_ZERO_AND_TOPOLOGICAL_PROJECTOR_AND_R11_SILENCE_ELSE_PRODUCT_REQUIRED | p_ge_2_required_but_not_parent_derived | 4e-20 | 476-double-zero-memory-coupling-origin-or-coefficient-runner.md |
| A3_total | combined_mu_extra_alpha3 | R7_alpha3 | alpha3 | alpha3_mu_extra_total | sum_of_scored_channels | not_applicable | MISSING_CHANNEL_VALUES | not_applicable | MISSING_CHANNEL_VALUES | 0_ONLY_IF_EACH_CHANNEL_PASSES_OR_PARENT_CANCELLATION_IDENTITY_EXISTS | parent_cancellation_identity_not_present | 4e-20 | source-intake\mts_residuals\P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv |

The domain row is still the highest pressure:

```text
W_domain_alpha3 * epsilon_domain_flux.
```

## 7. Evaluation

| input_id | channel | target_row | observable | product_symbol | predicted_alpha3 | target_bound | abs_le_bound | evaluation_status | valid_for_claim | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A3_boundary | boundary_monopole_shift | R7_alpha3 | alpha3 | W_boundary_alpha3_epsilon_boundary_flux | MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO | 4e-20 | false | not_scoreable_inputs_missing | false | missing numeric product and theorem-zero gate not accepted |
| A3_domain | domain_projector_mass | R7_alpha3 | alpha3 | W_domain_alpha3_epsilon_domain_flux | MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO | 4e-20 | false | not_scoreable_inputs_missing | false | missing numeric product and theorem-zero gate not accepted |
| A3_total | combined_mu_extra_alpha3 | R7_alpha3 | alpha3 | alpha3_mu_extra_total | MISSING_CHANNEL_VALUES | 4e-20 | false | not_scoreable_total_missing_channels | false | individual alpha3 channels have not passed and no parent cancellation identity exists |

Current result:

```text
not scoreable;
no channel passes;
valid_for_claim=false for every row.
```

## 8. Total Guard

| guard_id | rule | current_result | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| G_total_no_cancellation_by_fit | alpha3 total can pass only if each active channel passes individually or a parent cancellation identity is derived before fitting | fail_for_claim | individual_pass=False; total_pass=False | no total alpha3 or mu_extra-zero promotion |
| G_boundary_channel | boundary alpha3 must be theorem-zero or abs(W_boundary_alpha3 epsilon_boundary_flux)<=4e-20 | not_scoreable_inputs_missing | MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO | boundary alpha3 retained |
| G_domain_channel | domain alpha3 must be theorem-zero or abs(W_domain_alpha3 epsilon_domain_flux)<=4e-20 | not_scoreable_inputs_missing | MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO | domain alpha3 retained |
| G_R11_dependency | domain channel also needs R11 source-normalization/operator rows claim-valid or theorem-zero | fail_for_claim | R11_claimable_rows=0 | R11 blocks domain alpha3 promotion |

This stops the cheap move:

```text
boundary bad + domain bad = fitted cancellation.
```

No. Each source channel must pass unless the parent action derives a cancellation identity.

## 9. Validation

| rule_id | rule | result | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| V477_0_sources | all cited source paths exist | pass | missing_sources=0 | traceability only |
| V477_1_inputs | boundary, domain, and total alpha3 inputs are present | pass | boundary_monopole_shift;combined_mu_extra_alpha3;domain_projector_mass | evaluator is complete for current alpha3 channels |
| V477_2_bound | individual alpha3 rows use 4e-20 bound | pass | boundary_monopole_shift=4e-20;domain_projector_mass=4e-20;combined_mu_extra_alpha3=4e-20 | source lock carried into evaluator |
| V477_3_theorem_zero | theorem-zero gates are explicit and not accepted without parent premises | pass | theorem_rows=3 accepted=0 | no hidden zero claim |
| V477_4_claim_rows | no alpha3 evaluation row is claim-valid with missing products | fail_for_claim | valid_for_claim_true=0 | no alpha3/PPN/local-GR pass |
| V477_5_total_guard | total alpha3 cannot pass by cancellation-by-fit | pass | guard_rows=4 | total alpha3 retained |

## 10. Decision

| decision_id | status | meaning | next_action |
| --- | --- | --- | --- |
| D0_evaluator | written | alpha3 now has a concrete product evaluator for boundary, domain, and total rows | fill numeric products or theorem-zero sources |
| D1_boundary_alpha3 | not_scoreable | boundary theorem-zero route is conditional and W_boundary_alpha3 epsilon_boundary_flux is missing | derive scalar boundary premises or supply numeric product |
| D2_domain_alpha3 | not_scoreable_highest_pressure | domain product W_domain_alpha3 epsilon_domain_flux is missing and R11 has zero claim-valid rows | derive determinant/current parent ownership or supply numeric product |
| D3_total_alpha3 | not_promoted | no cancellation-by-fit is allowed; individual channels must pass or parent identity must exist | keep total alpha3 retained |
| D4_promotion | forbidden | no alpha3 pass, mu_extra zero, PPN, Newtonian-limit, or local-GR pass is earned | 478-determinant-current-parent-ownership-or-demotion.md |

## 11. Claim Ceiling

Allowed:

```text
MTS has a strict alpha3 product evaluator.
```

Allowed:

```text
The exact missing products and theorem-zero gates are identified.
```

Forbidden:

```text
MTS passes alpha3.
```

Forbidden:

```text
MTS passes mu_extra zero, PPN, Newton, or local GR.
```

## 12. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `478-determinant-current-parent-ownership-or-demotion.md` | best current domain-alpha3 theorem-zero clue is det(Q_coh), but it is not parent-owned |
| 2 | `479-R11-domain-source-normalization-zero-or-fill.md` | R11 source-normalization still blocks domain alpha3 |
| 3 | `480-alpha3-numeric-product-input-template.md` | if derivation stalls, make the coefficient input template ready for actual numeric fitting |
