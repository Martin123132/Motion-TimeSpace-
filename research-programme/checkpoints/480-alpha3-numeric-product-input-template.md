# 480 - Alpha3 Numeric Product Input Template

Private alpha3/input-contract checkpoint. This is not a public alpha3 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoints 477-479 narrowed the alpha3 obstruction to a concrete product problem:

```text
abs(W_i_alpha3 * epsilon_i_flux) <= 4e-20
```

for each active alpha3 source channel, unless a parent theorem proves that channel exactly zero.

This checkpoint writes the fill-ready input template. It does not fill the numbers. It prevents the next step from hiding behind vague words like "small", "screened", or "probably zero".

## 2. Run Manifest

| Field | Value |
| --- | --- |
| Script | `scripts/alpha3_numeric_product_input_template.py` |
| Run directory | `runs\20260604-093000-alpha3-numeric-product-input-template` |
| Generated UTC | `2026-06-03T23:57:49.582462+00:00` |
| Status | `alpha3_numeric_product_input_template_written_unfilled_no_alpha3_mu_extra_PPN_Newton_or_local_GR_pass` |
| Claim ceiling | `alpha3_numeric_product_template_only_no_alpha3_pass_no_mu_extra_zero_PPN_Newton_or_local_GR_pass` |
| Next target | `481-Qcoh-parent-projector-algebra-or-closure.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 469-fill-or-zero-highest-pressure-mu-extra-row.md | True | identified alpha3 as boundary/domain highest-pressure product pair |
| 470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md | True | boundary alpha3 conditional theorem route and coefficient need |
| 477-alpha3-bound-product-evaluator.md | True | strict alpha3 product evaluator |
| 479-R11-domain-source-normalization-zero-or-fill.md | True | R11/domain zero rejected and fill requirements written |
| source-intake\mts_residuals\P8_ALPHA3_BOUND_PRODUCT_INPUT.csv | True | current evaluator input rows |
| source-intake\mts_residuals\P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv | True | current evaluator output rows |
| source-intake\mts_residuals\P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv | True | boundary/domain/total alpha3 fill skeleton |
| source-intake\mts_residuals\R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv | True | domain sibling fill requirements from R11 zero-or-fill |
| source-intake\mts_residuals\P8_mu_extra_boundary_coefficients.csv | True | boundary coefficient artifact |
| source-intake\mts_residuals\P8_mu_extra_domain_projector_coefficients.csv | True | domain coefficient artifact |
| scripts/alpha3_numeric_product_input_template.py | True | this checkpoint generator |

## 4. Product Input Template

| input_id | channel | target_row | observable | product_symbol | coefficient_symbol | epsilon_symbol | coefficient_value | epsilon_value | explicit_product_value | product_units | target_bound | bound_units | acceptance_gate | theorem_zero_certificate | numeric_source_file | formula_reference | assumptions | no_cancellation_policy | current_status | valid_for_claim | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A3_BOUNDARY_NUMERIC_OR_ZERO | boundary_monopole_shift | R7_alpha3 | alpha3 | W_boundary_alpha3_epsilon_boundary_flux | W_boundary_alpha3 | epsilon_boundary_flux | FILL_NUMERIC_OR_THEOREM_ZERO | FILL_NUMERIC_OR_THEOREM_ZERO | FILL_NUMERIC_PRODUCT_OR_ZERO_CERTIFICATE | dimensionless | 4e-20 | dimensionless | abs(alpha3_boundary) <= 4e-20 with source path, units, and no hidden cancellation | MISSING_PARENT_BOUNDARY_NO_FLUX_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state local frame, source normalization, boundary collar, stationarity, and no hidden cancellation | must pass individually unless parent cancellation identity is derived before fitting | template_unfilled | false | supply boundary theorem-zero certificate or numeric W_boundary_alpha3 epsilon_boundary_flux product |
| A3_DOMAIN_NUMERIC_OR_ZERO | domain_projector_mass | R7_alpha3 | alpha3 | W_domain_alpha3_epsilon_domain_flux | W_domain_alpha3 | epsilon_domain_flux | FILL_NUMERIC_OR_THEOREM_ZERO | FILL_NUMERIC_OR_THEOREM_ZERO | FILL_NUMERIC_PRODUCT_OR_ZERO_CERTIFICATE | dimensionless | 4e-20 | dimensionless | abs(alpha3_domain) <= 4e-20 and R11/vector rows are zero or scored | MISSING_PARENT_DOMAIN_NO_LEAK_AND_R11_SILENCE_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state local coframe, domain selector, projector stress, R11 operator status, source normalization, and no hidden cancellation | must pass individually; total cancellation cannot rescue a failed domain row | template_unfilled | false | supply domain theorem-zero certificate or numeric W_domain_alpha3 epsilon_domain_flux product plus sibling rows |
| A3_TOTAL_GUARD | combined_mu_extra_alpha3 | R7_alpha3 | alpha3 | alpha3_mu_extra_total | sum_of_scored_channels | not_applicable | SUM_ONLY_AFTER_INDIVIDUAL_CHANNELS_SCORE | not_applicable | MISSING_CHANNEL_VALUES | dimensionless | 4e-20 | dimensionless | total and every active channel pass unless parent identity enforces exact cancellation | MISSING_PARENT_CANCELLATION_IDENTITY_IF_USED | not_applicable_until_channels_score | MISSING_TOTAL_POLICY_REFERENCE | total alpha3 cannot be scored by post-fit cancellation | individual channels pass first unless a parent identity forces exact cancellation before fitting | guard_only | false | do not total-score until boundary and domain products are theorem-zero or numeric |

The two live products are:

```text
W_boundary_alpha3 * epsilon_boundary_flux
W_domain_alpha3 * epsilon_domain_flux
```

Each must be individually theorem-zero or below `4e-20`. The total row is a guard, not a shortcut.

## 5. Domain Sibling Requirements

| input_id | channel | target_row | observable | coefficient_or_product | r11_family | candidate_value | candidate_units | target_bound | acceptance_gate | theorem_zero_certificate | numeric_source_file | formula_reference | assumptions | required_before_domain_alpha3_claim | current_status | valid_for_claim | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DSR_R5_alpha1_NUMERIC_OR_ZERO | domain_projector_mass | R5_alpha1 | alpha1 | W_domain_alpha1_epsilon_domain_vector | vector_preferred_frame | FILL_NUMERIC_OR_THEOREM_ZERO | dimensionless_or_declared_operator_units | 1e-04 | numeric/theorem-zero vector coefficient; no local domain frame | MISSING_PARENT_ZERO_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state coframe, source normalization, R11/operator status, and no tuned cancellation | true | template_unfilled | false | derive parent zero or fill numeric coefficient/product with source path and assumptions |
| DSR_R6_alpha2_NUMERIC_OR_ZERO | domain_projector_mass | R6_alpha2 | alpha2 | W_domain_alpha2_epsilon_domain_vector | vector_preferred_frame | FILL_NUMERIC_OR_THEOREM_ZERO | dimensionless_or_declared_operator_units | 2e-09 | numeric/theorem-zero vector coefficient; no local domain frame | MISSING_PARENT_ZERO_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state coframe, source normalization, R11/operator status, and no tuned cancellation | true | template_unfilled | false | derive parent zero or fill numeric coefficient/product with source path and assumptions |
| DSR_R7_alpha3_NUMERIC_OR_ZERO | domain_projector_mass | R7_alpha3 | alpha3 | W_domain_alpha3_epsilon_domain_flux | vector_preferred_frame;source_normalization_operator;projector_domain_stress | FILL_NUMERIC_OR_THEOREM_ZERO | dimensionless_or_declared_operator_units | 4e-20 | abs(product) <= 4e-20 or theorem-zero no-leak | MISSING_PARENT_ZERO_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state coframe, source normalization, R11/operator status, and no tuned cancellation | self | template_unfilled | false | derive parent zero or fill numeric coefficient/product with source path and assumptions |
| DSR_R8_xi_NUMERIC_OR_ZERO | domain_projector_mass | R8_xi | xi | W_domain_xi_epsilon_domain_anisotropy | projector_domain_stress;vector_preferred_frame | FILL_NUMERIC_OR_THEOREM_ZERO | dimensionless_or_declared_operator_units | 4e-09 | numeric/theorem-zero anisotropy coefficient | MISSING_PARENT_ZERO_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state coframe, source normalization, R11/operator status, and no tuned cancellation | true | template_unfilled | false | derive parent zero or fill numeric coefficient/product with source path and assumptions |
| DSR_R11_EH_operator_ledger_NUMERIC_OR_ZERO | domain_projector_mass | R11_EH_operator_ledger | non_EH_operator_coefficients | c_domain_source_normalization_operator | source_normalization_operator;projector_domain_stress | FILL_NUMERIC_OR_THEOREM_ZERO | dimensionless_or_declared_operator_units | symbolic | operator row has source path, units, normalization, weak-field map, and no MISSING fields | MISSING_PARENT_ZERO_CERTIFICATE | MISSING_NUMERIC_SOURCE | MISSING_FORMULA_REFERENCE | must state coframe, source normalization, R11/operator status, and no tuned cancellation | true | template_unfilled | false | derive parent zero or fill numeric coefficient/product with source path and assumptions |

The domain alpha3 row cannot be isolated from preferred-frame, anisotropy, and R11/source-normalization siblings.

If the domain sector still carries R5/R6/R8/R11 leakage, a standalone alpha3 zero is not a local-GR pass.

## 6. Total Guard

| guard_id | rule | current_status | failure_mode_prevented | valid_for_claim |
| --- | --- | --- | --- | --- |
| TG0_individual_first | boundary and domain alpha3 products must pass individually before total alpha3 can be scored | active | post-fit cancellation between hidden boundary and domain fluxes | false |
| TG1_parent_cancellation_identity | a total cancellation claim is allowed only if a parent identity is derived before fitting | not_present | tuned cancellation masquerading as field-theory prediction | false |
| TG2_domain_siblings | domain alpha3 cannot pass while R5/R6/R8/R11 sibling rows remain missing or unscored | active | closing alpha3 while preferred-frame/source-normalization leakage survives elsewhere | false |
| TG3_source_path_required | numeric products require source file, formula reference, units, assumptions, and bound comparison | active | unsourced tiny number inserted after the fact | false |

## 7. Route Update

| route_id | target | current_status | accepted_for_claim | next_action |
| --- | --- | --- | --- | --- |
| A3_boundary_product | W_boundary_alpha3 epsilon_boundary_flux | template_unfilled | false | fill numeric product or parent no-flux certificate |
| A3_domain_product | W_domain_alpha3 epsilon_domain_flux | template_unfilled_requires_R11_siblings | false | 481-Qcoh-parent-projector-algebra-or-closure.md |
| A3_total_guard | alpha3_mu_extra_total | guard_only_no_cancellation | false | wait for individual channel pass or parent cancellation theorem |

## 8. Validation

| rule_id | rule | result | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| V480_0_sources | all cited source paths exist | pass | missing_sources=0 | traceability only |
| V480_1_product_template | boundary, domain, and total alpha3 rows are present | pass | product_rows=3; columns_ok=True | alpha3 inputs are now concrete |
| V480_2_domain_siblings | domain sibling rows cover R5/R6/R7/R8/R11 | pass | sibling_rows=5; columns_ok=True | domain alpha3 cannot be isolated from R11/vector leaks |
| V480_3_total_guard | total alpha3 no-cancellation policy is explicit | pass | guard_rows=4 | no cancellation-by-fit |
| V480_4_unfilled_default | template rows are not claim-valid before numbers or theorem certificates are supplied | pass | claim_valid_rows=0 | no alpha3 promotion |
| V480_5_claim_ceiling | no alpha3, mu_extra, Newton, PPN, or local-GR pass is granted | pass | template_unfilled; claim_allowed=false | input contract only |

## 9. Decision

| decision_id | status | meaning | next_action |
| --- | --- | --- | --- |
| D0_template | written | alpha3 has a fill-ready numeric/theorem-zero input template | source-intake\mts_residuals\P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv |
| D1_boundary | unfilled | boundary product requires numeric W_boundary_alpha3 epsilon_boundary_flux or a parent no-flux certificate | derive boundary no-flux or fill A3_BOUNDARY_NUMERIC_OR_ZERO |
| D2_domain | unfilled_highest_pressure | domain product requires W_domain_alpha3 epsilon_domain_flux plus R11/domain sibling rows | derive parent no-leak/R11 silence or fill A3_DOMAIN_NUMERIC_OR_ZERO |
| D3_total | guard_only | total alpha3 cannot be used for cancellation-by-fit | score individual channels first |
| D4_promotion | forbidden | no alpha3 pass, mu_extra zero, PPN, Newtonian-limit, or local-GR pass is earned | 481-Qcoh-parent-projector-algebra-or-closure.md |

## 10. Claim Ceiling

Allowed:

```text
alpha3 now has a fill-ready numeric/theorem-zero product template.
boundary, domain, and total guard rows are explicit.
domain sibling rows are explicit.
```

Not allowed:

```text
alpha3 passes.
mu_extra is zero.
R11/domain source normalization is silent.
MTS passes PPN, Newton, or local GR.
```

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `481-Qcoh-parent-projector-algebra-or-closure.md` | attempt parent Q_coh/P_coh/domain algebra before committing to numeric closure fills |
| 2 | `482-local-residual-vector-from-domain-source-fill.md` | once product rows are filled, propagate them into the residual vector |
| 3 | `483-alpha3-product-evaluator-refresh.md` | rerun alpha3 evaluator after numeric/theorem rows exist |
