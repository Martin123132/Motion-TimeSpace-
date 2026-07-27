# 560 - Y5 R10 Source-Normalized Alpha Law from Parent or Runner Real-Data Fill

Generated: 2026-06-04T16:18:31.540251+00:00  
Run: `runs/20260604-150500-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill`  
Status: `Y5_R10_source_normalized_alpha_law_conditionally_derived_parent_inputs_missing_no_R10_pass`  
Claim ceiling: `conditional_alpha_law_only_no_fifth_force_Newton_PPN_or_local_GR_pass`

## 1. Verdict

The parent finite-range route gives a clean conditional law:

```text
alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T
                 /(4*pi*Z_X*G_obs*M_H*m_T)
```

with

```text
a_X/a_GR = alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X).
```

That is real progress: the missing R10 object is no longer vague. It is an exact source-normalized coefficient once the parent action supplies `Z_X`, `lambda_X`, `Q_X`, `q_X^T`, `Pi_M^H`, and the measured-GM normalization.

But it is not yet a pass. The formula is symbolic because those parent-owned inputs remain missing. The existing R10 runner still correctly rejects the placeholder MTS and bound curves.

## 2. Derivation Attempt

| step_id | derivation_step | mathematical_form | result | why_it_matters | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AL560_0_parent_quadratic_branch | assume the surviving local finite-range branch is represented by one parent-owned scalar/vector-silent mode X in the weak-field static limit | S_X^(2)=int d^4x[-(Z_X/2)(partial X)^2-(Z_X/2)m_X^2 X^2+X J_X] | conditional_starting_point | without Z_X, m_X, and J_X the strength cannot be normalized | not_claimable_parent_inputs_missing | false |
| AL560_1_static_euler_equation | vary X and take the static exterior limit | Z_X(-Delta+m_X^2)X=J_X | conditional_eom_written | this is the exact operator needed before the mass-gap/no-hair or Yukawa branch can be scored | not_claimable_operator_not_parent_derived | false |
| AL560_2_exterior_green_function | solve the positive finite-range static Green problem outside a compact source | X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r), lambda_X=1/m_X | conditional_profile_derived | lambda is fixed by the parent mass gap; Q_X carries source, boundary, projector, and finite-size ownership | not_claimable_QX_lambda_missing | false |
| AL560_3_source_charge_definition | collect the monopole source that survives into the exterior field | Q_X^H(lambda)=int_H d^3x J_X(x) F_lambda(x)+Q_boundary+Q_projector+Q_memory | definition_written_not_filled | finite-size and nonlocal pieces change alpha even when the same lambda is used | not_claimable_source_charge_missing | false |
| AL560_4_test_body_coupling | let a test body with parent-owned charge q_X^T respond to X | V_X(r)=-s_X q_X^T X(r) | conditional_test_potential_written | R10 is a force on matter; if q_X^T is not zero or universal, WEP/species rows also open | not_claimable_test_charge_missing | false |
| AL560_5_newton_comparison | compare the X potential with the measured Newtonian potential in the same frame | V_N(r)=-G_obs M_H m_T/r | normalization_anchor_written | alpha must be dimensionless and normalized to observed GM, not to a free symbolic scale | not_claimable_measured_GM_split_missing | false |
| AL560_6_exact_alpha_law | divide the Yukawa potential by the Newtonian potential in the R10 convention | alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T) | conditional_exact_law_derived | this is the missing MTS-side alpha(lambda) formula, but it is not numeric until every parent input is owned | conditional_formula_only | false |
| AL560_7_acceleration_residual | differentiate the potential to match the accepted fifth-force acceleration row | a_X/a_GR=alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X) | R10_mapping_recovered | the derived alpha law plugs into the existing 437/559 runner once lambda and alpha rows are numeric | not_claimable_runner_rows_missing | false |
| AL560_8_zero_conditions | read exact local suppression conditions from the multiplicative alpha law | alpha_X=0 if Pi_M^H Q_X^H=0 or q_X^T=0, or by a parent Ward/no-hair theorem setting the whole physical spectral source to zero | zero_routes_identified | mass gap alone is not a zero; the zero must hit the source, test charge, projection, or physical mode | not_claimable_zero_conditions_not_signed | false |
| AL560_9_multimode_memory_extension | generalize finite-range memory/nonlocal tails to a spectral sum or envelope | delta a/a_GR=sum_i alpha_i(1+r/lambda_i)exp(-r/lambda_i) or int dlnlambda alpha(lambda)(1+r/lambda)exp(-r/lambda) | conditional_extension_written | a memory tail cannot be hidden in one scalar; it needs theorem-zero or an executable alpha envelope | not_claimable_envelope_missing | false |

## 3. Formula Register

| formula_id | object | expression | required_parent_inputs | R10_mapping | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| F560_0_parent_action | quadratic finite-range parent branch | S_X^(2)=int d^4x[-(Z_X/2)(partial X)^2-(Z_X/2)m_X^2 X^2+X J_X] | Z_X;m_X_squared;J_X;sign_convention;allowed_spin_sector | operator source for alpha(lambda) branch | conditional_not_parent_owned | false |
| F560_1_static_operator | static Euler equation | Z_X(-Delta+m_X^2)X=J_X | positive Z_X;positive m_X_squared;source-free exterior or source charge | sets whether theorem-zero or Yukawa curve is needed | conditional_not_signed | false |
| F560_2_exterior_profile | compact-source Yukawa profile | X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r); lambda_X=1/m_X | Q_X^H(lambda_X);lambda_X;Z_X;boundary/projector/memory source treatment | source-normalized field profile | conditional_not_numeric | false |
| F560_3_test_potential | test body potential | V_X(r)=-s_X q_X^T Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r) | q_X^T;species universality;sign s_X | compare directly against Yukawa correction to Newtonian potential | conditional_not_numeric | false |
| F560_4_exact_alpha_law | source-normalized R10 strength | alpha_X(lambda_X)=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T) | Pi_M^H projection;Q_X^H;q_X^T;Z_X;G_obs;M_H;m_T;s_X | alpha_predicted column in R10_alpha_lambda_curve_MTS_source_normalization.csv | derived_conditional_formula | false |
| F560_5_acceleration_ratio | R10 acceleration residual | a_X/a_GR=alpha_X(lambda_X)(1+r/lambda_X)exp(-r/lambda_X) | same alpha_X and lambda_X;R10 convention;measured-G normalization | comparison against alpha_bound(lambda) | convention_recovered | false |
| F560_6_multimode_or_memory_tail | non-single-mode extension | delta a/a_GR=sum_i alpha_i(1+r/lambda_i)exp(-r/lambda_i) or int dlnlambda alpha(lambda)(1+r/lambda)exp(-r/lambda) | positive spectral measure or conservative envelope;no tuned cancellation;source normalization per mode | sampled alpha_envelope(lambda) rows | conditional_extension_only | false |

## 4. Parent Input Debts

| input_id | symbol | definition | needed_for | current_status | zero_route | coefficient_route | source_owner | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PI560_0_ZX | Z_X | canonical kinetic/operator normalization of the finite-range parent mode | exact 4*pi normalization of alpha_X | missing_parent_action_coefficient | not a normal zero route unless mode is nonpropagating by constraint | derive Z_X>0 and include it in alpha denominator | parent action | false |
| PI560_1_mX | m_X_squared;lambda_X | positive local mass gap and its range lambda_X=1/m_X | lambda_value column and Yukawa/no-hair operator sign | m_X_not_parent_derived | positive mass gap helps no-hair only with zero source and zero boundary flux | derive numeric or symbolic lambda grid from parent spectrum | parent action;bulk/memory/range operator | false |
| PI560_2_JX | J_X | matter, boundary, projector, domain, and memory source entering the X equation | Q_X^H(lambda) and source-free no-hair decision | source_terms_not_parent_split | prove J_X=0 in compact local exterior and no hidden boundary/projector source | integrate J_X into Q_X^H(lambda) | source-normalization ledger plus parent action | false |
| PI560_3_QX | Q_X^H(lambda) | source monopole/form-factor charge generating the exterior X profile | alpha numerator | Q_X_not_parent_derived | derive Pi_M^H Q_X^H=0 or Q_X^H=0 | write source integral with finite-size, boundary, projector, and memory pieces | Hamiltonian/source projection branch | false |
| PI560_4_qtest | q_X^T | test-body charge/coupling to the X field | force on matter and WEP/species status | q_test_not_parent_derived | derive q_X^T=0 for all ordinary local test bodies | derive universal q_X^T/m_T or species-dependent residual | matter coupling sector | false |
| PI560_5_PiM | Pi_M^H | Hamiltonian mass projection from X charge into measured local mass/force sector | decide whether nonzero X is gravitationally silent or force-bearing | PiM_projection_not_derived | derive Pi_M^H Q_X^H=0 by parent Ward identity | derive nonzero projection coefficient and score R10 | Hamiltonian/mass projection branch | false |
| PI560_6_measured_GM | G_obs*M_H*m_T | same-frame observed Newtonian normalization used in R10 | dimensionless alpha_X | measured_GM_split_not_closed | constant universal calibration only if range/species/time/radial derivatives vanish | normalize alpha against measured GM and retain residual derivatives | measured-GM/source-normalization branch | false |
| PI560_7_sign | s_X | sign convention for attractive/repulsive X exchange relative to R10 alpha | alpha sign and absolute-bound comparison | sign_convention_not_parent_fixed | sign does not zero alpha; bounds use abs(alpha) unless source says otherwise | derive sign from coupling and kinetic convention | parent action/coupling convention | false |
| PI560_8_boundary_flux | Q_boundary;boundary_flux | boundary/domain contribution to exterior X charge | no-hair theorem or source charge | boundary_flux_zero_not_derived | derive zero boundary flux and regular decaying exterior solution | include boundary charge in Q_X^H(lambda) | boundary/domain branch | false |
| PI560_9_memory_kernel | alpha_memory(lambda) | spectral/envelope representation of nonlocal memory tail | memory branch cannot hide as one scalar if range dependent | memory_envelope_not_derived | derive local stable kernel silence and zero spectral source | sample conservative alpha_envelope(lambda) rows | memory/time-flow branch | false |
| PI560_10_bound_curve | alpha_bound(lambda) | external R10 inverse-square/fifth-force bound in same convention | runner comparison | digitized_bound_curve_missing | not needed only if theorem-zero is fully signed | digitize/source bound rows and run comparator | empirical local-bound data branch | false |

## 5. Local Suppression / Zero Conditions

| condition_id | condition | formula | sufficient_for_alpha_zero | current_status | repair | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Z560_0_absent_test_charge | ordinary local test bodies do not couple to X | q_X^T=0 for every allowed T | yes_for_that_branch | not_derived | derive matter coupling silence from parent action; otherwise fill q_X^T | false |
| Z560_1_absent_projected_source | source charge is physically present but Hamiltonian-mass projection is zero | Pi_M^H[Q_X^H(lambda)]=0 | yes_for_R10_force_projection | not_derived | prove projection Ward identity; otherwise fill projection coefficient | false |
| Z560_2_source_free_nohair | positive operator, zero source, zero boundary flux, regular decaying solution | Z_X>0; m_X^2>0; J_X=0; boundary_flux=0 => X=0 | yes_if_all_premises_parent_signed | operator_and_source_premises_open | derive operator sign plus source/boundary/projector silence | false |
| Z560_3_gauge_topological_absence | finite-range-looking variable is gauge/topological and has no local stress or matter charge | delta_g S_X=0 and delta_m S_X=0 in local compact sector | yes_if_parent_identity_signed | not_derived | show X has no physical propagator/source in local branch | false |
| Z560_4_universal_GM_calibration | surviving monopole is constant universal calibration, not finite-range hair | D_lambda epsilon=D_species epsilon=D_t epsilon=D_r epsilon=0 | no_but_can_remove_R10_if_truly_not_range_dependent | not_parent_fixed | derive derivative silence and absorbed measured-GM normalization | false |
| Z560_5_multimode_Ward_zero | multiple ranges cancel only by exact parent identity, not tuning | rho_alpha(lambda)=0 as a signed physical spectral measure by Ward/no-source theorem | yes_if_identity_zeroes_measure | not_derived | derive spectral source measure or emit conservative envelope | false |
| Z560_6_bound_below_R10 | nonzero finite-range force survives but lies below external bounds | abs(alpha_predicted(lambda_i))<=alpha_bound(lambda_i) for every valid row | no_but_can_pass_R10_bound | not_evaluable_no_numeric_rows | fill MTS and bound curves then run comparator | false |

## 6. Runner Fill Template

This is a non-claim template only. It is deliberately separate from `R10_alpha_lambda_curve_MTS_source_normalization.csv` so the 559 placeholder rejection remains intact.

| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | bulk_X_parent_source_normalized_law | R10_alpha_lambda_curve_MTS_source_normalization | MISSING_PARENT_DERIVED_LAMBDA_X | m | s_X*PiM_H_QX(lambda_X)*q_X_test/(4*pi*Z_X*G_obs*M_H*m_test) | MISSING_DIGITIZED_ALPHA_BOUND | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | Yukawa_potential_and_acceleration_ratio | conditional_formula_not_numeric_missing_parent_inputs | 560-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill.md | source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_FORMULA_REGISTER.csv | canonical or declared Z_X; same-frame measured-GM; no tuned cancellation; source/test charges parent-owned | false | template only; do not copy into claim curve until lambda and alpha are numeric or theorem-zero is signed |

## 7. Runner Dry-Run Recheck

| summary_id | runner_results_dir | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_560_RECHECK | runs/20260604-150500-Y5-R10-source-normalized-alpha-law-from-parent-or-runner-real-data-fill/results/runner | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False |

## 8. Evaluator

| gate_id | gate | result | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| E560_0_alpha_formula | derive source-normalized alpha law from parent finite-range branch | conditional_pass | alpha_X=s_X Pi_M^H[Q_X^H(lambda_X)] q_X^T/(4*pi*Z_X*G_obs*M_H*m_T) | false |
| E560_1_parent_inputs | parent-owned Z_X, lambda_X, Q_X, q_test, PiM, measured-GM normalization | fail_current_claim | all required quantities remain missing or retained-unfilled in source ledgers | false |
| E560_2_theorem_zero | prove alpha(lambda)=0 without curve data | fail_current_claim | zero conditions are identified but not parent-signed | false |
| E560_3_runner_data | supply executable numeric MTS alpha and external bound rows | fail_current_claim | existing 559 runner still sees placeholder curves only | false |
| E560_4_R10_status | R10/fifth-force pass | fail_current_claim | conditional formula is not a valid runner row | false |
| E560_5_local_GR_status | Newton/PPN/local-GR promotion | fail_current_claim | R10 plus Cextra/radial/source-normalization gates remain open | false |

## 9. Obstruction Ledger

| obstruction_id | blocked_object | reason | repair | valid_for_claim |
| --- | --- | --- | --- | --- |
| O560_0_ZX_missing | exact alpha normalization | parent action has not supplied canonical or noncanonical X kinetic normalization | derive Z_X and sign from parent branch | false |
| O560_1_lambda_missing | lambda_value row | m_X/lambda_X is not parent-derived for the surviving branch | derive mass gap or spectral range grid | false |
| O560_2_source_charge_missing | Q_X^H(lambda) | matter, boundary, projector, and memory source pieces are not integrated into a parent-owned charge | derive source integral or theorem-zero source absence | false |
| O560_3_test_charge_missing | q_X^T | test-body coupling is not proven zero, universal, or numeric | derive matter coupling silence or charge coefficient | false |
| O560_4_PiM_missing | Hamiltonian force projection | nonzero X may be projection-silent, but Pi_M^H is not derived | prove Pi_M^H Q_X^H=0 or fill projection coefficient | false |
| O560_5_bound_curve_missing | runner comparison | external alpha_bound(lambda) rows are still placeholders | source/digitize bound curve in the R10 convention | false |
| O560_6_memory_tail_unmapped | non-single-mode finite-range branch | memory/nonlocal tail has no spectral alpha(lambda) envelope | derive theorem-zero for the tail or emit conservative envelope rows | false |

## 10. Decision

| decision_id | decision | meaning | status | next_target |
| --- | --- | --- | --- | --- |
| D560_0_conditional_law_derived | source_normalized_alpha_law_written | the parent finite-range branch implies an exact conditional alpha(lambda) formula | conditional_progress | 561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md |
| D560_1_no_claim | R10_still_blocked | the formula has missing parent inputs and cannot be treated as evidence or a valid curve row | R10_pass_false | 561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md |
| D560_2_zero_routes_exposed | zero_requires_source_test_projection_or_Ward_identity | mass gap alone cannot remove the fifth-force row; alpha zero must be source/test/projection/no-hair zero | derivation_guidance | 561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md |
| D560_3_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 11. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md | R10 runner dry-run showing placeholder rows are rejected | True |
| 558-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem.md | exact R10 branch schema and no-range theorem failure | True |
| 557-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill.md | bulk/memory/range Yukawa contract and mass-gap guardrail | True |
| 437-R10-alpha-lambda-executable-curve-contract.md | accepted R10 alpha(lambda) convention and curve contract | True |
| 380-bulk-X-mass-gap-source-normalized-force-law.md | source-normalized finite-range force-law debt | True |
| source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv | current MTS-side placeholder curve retained unchanged | True |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | current bound-side placeholder curve retained unchanged | True |
| source-intake/local_bounds/local_bound_claims.csv | local bound manifest naming the R10 fifth-force test | True |
| source-intake/mts_residuals/P8_Y5_BRR545_559_VALIDATION.csv | previous validation gate | True |
| source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv | mu_extra coefficient vector with bulk_X_Yukawa_tail retained | True |
| source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv | source-normalization channel ownership ledger | True |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv | bulk-X force-law quantity ledger | True |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv | bulk-X gate results showing alpha/lambda not parent-derived | True |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | reusable R10 curve validator/comparator | True |
| scripts/Y5_R10_source_normalized_alpha_law_from_parent_or_runner_real_data_fill.py | this checkpoint generator | True |

## 12. Validation

| check_id | result | detail |
| --- | --- | --- |
| V560_0_source_paths_exist | pass | missing=0 |
| V560_1_prior_559_clean | pass | prior_validation_rows=10;prior_fails=0 |
| V560_2_conditional_formula_written | pass | exact conditional alpha formula registered |
| V560_3_parent_inputs_complete_as_debts | pass | parent_input_rows=11;claim_rows=0 |
| V560_4_zero_conditions_not_overclaimed | pass | zero_condition_rows=7;claim_rows=0 |
| V560_5_existing_placeholders_unchanged_as_blockers | pass | mts_curve_rows=2;bound_curve_rows=2 |
| V560_6_runner_still_blocks_placeholders | pass | valid_mts=0;valid_bound=0;R10_pass=False |
| V560_7_template_not_claimable | pass | fill_rows=1;claim_fill_rows=0;claim_evaluator_rows=0 |
| V560_8_no_overclaim | pass | R10_pass=false; fifth_force=false; Cextra=false; radial_closure=false; Newton=false; PPN=false; local_GR=false |

## 13. Route Update

| route_id | allowed_after_560 | forbidden_after_560 | next_action |
| --- | --- | --- | --- |
| RU560_0_allowed | MTS may cite the conditional alpha formula as a derivation target | MTS may not claim R10/fifth-force pass or local GR from a symbolic formula | derive or zero Q_X, q_test, PiM_H, Z_X, and lambda_X |
| RU560_1_allowed | MTS may choose theorem-zero or executable curve as the next branch | MTS may not use tuned cancellation among ranges without a parent Ward identity | 561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md |

## 14. Claim Ceiling

Allowed:

```text
MTS has conditionally derived the exact source-normalized alpha law for a finite-range parent branch.
MTS has identified the exact local suppression conditions for alpha_X -> 0.
```

Forbidden:

```text
MTS has supplied a numeric alpha(lambda) curve.
MTS has proved alpha(lambda)=0.
MTS has passed R10/fifth-force, Newton, PPN, Cextra, radial closure, or local GR.
```

## 15. Practical Read

This is one of those useful uncomfortable checkpoints: the algebra itself is not the problem anymore. The problem has been converted into five hard parent-owned fills:

```text
Z_X,
lambda_X,
Pi_M^H Q_X^H(lambda_X),
q_X^T,
measured-GM normalization.
```

If any of the numerator pieces is theorem-zero, R10 can die cleanly. If not, the same formula gives the MTS curve row the runner will judge. No vibes, no hidden scalar pass, but also no mystery left about what the next bolt is.

## 16. Next Target

`561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md`

Next: derive or zero the source/test charge and Hamiltonian projection in the numerator. If that numerator cannot be zeroed, fill the coefficient route and then the R10 curve.
