# 1669 - Dq Leak Bound Source Pack Units And Arena Projections

**Private status:** source-pack plumbing only. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1669` turns the retained `Dq` leak language from `1668` into an arena-ready acquisition pack.

```text
What improved:
each retained leak now has a unit convention,
each local arena R0-R11 has a projection requirement,
R10 has a 1503-compatible source-pack template,
and all rows are explicitly nonclaim/non-scoring.

What did not improve:
there is still no numeric Dq leak,
no parent-signed theorem-zero,
no R10 alpha(lambda) curve claim row,
and no local GR/Newton reduction.
```

This is useful because it stops the local branch from drifting into vibes. Every leak either has to die by theorem or enter the ring as a bounded residual.

## Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1668_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md | True | True | 1669 Dq leak unit/projection/source-pack input |
| 1668_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1668_VALIDATION.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| 1668_source_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1668_DQ_LEAK_SOURCE_PACK_SCHEMA.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| 1668_next_target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1668_NEXT_TARGET.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| local_bound_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| local_residual_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| r10_formula_register | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1503_COUPLING_FORMULA_REGISTER.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| r10_bound_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1503_COUPLING_CLOSURE_BOUND_ROW_CONTRACT.csv | True | True | 1669 Dq leak unit/projection/source-pack input |
| r10_verticality_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1504_R10_RESIDUAL_VERTICALITY_CONTRACT.csv | True | True | 1669 Dq leak unit/projection/source-pack input |

## Unit Conventions

| component_id | symbol | channel | unit_convention | status | needed_source_inputs |
| --- | --- | --- | --- | --- | --- |
| Dq_Z | Dq_Z_norm | Z normal-form quotient leak | dimensionless only after q-basis and arena norm are parent-declared; otherwise arena-dependent | UNIT_CONVENTION_STAGED_INPUTS_MISSING | q(Phi), Z basis, Dq[partial_Z], norm convention, arena projection |
| Dq_phi | Dq_phi_norm | phi improvement quotient leak | dimensionless after phi normalization and boundary/domain convention; otherwise arena-dependent | UNIT_CONVENTION_STAGED_INPUTS_MISSING | phi action, q dependence, Dq[partial_phi], boundary/domain convention |
| Dq_RAB_Jq | Dq_RAB_or_Jq_norm | R_AB/J_q cell-visible leak | dimensionless after cell-map normalization; otherwise arena-dependent | UNIT_CONVENTION_STAGED_INPUTS_MISSING | q cell map or parent constraint that removes R_AB/J_q before matter/readout |
| C_qm | C_qm=||DObs_e[Dq[v]]|| | geometry pullback/source stress | dimensionless coframe/Jacobian norm if variations are normalized to unit observed-frame displacement | UNIT_CONVENTION_STAGED_INPUTS_MISSING | observed coframe functor, parent q map, local weak-field norm, v selection |
| S_direct | S_direct | direct matter/source dependence | E* forcing/action-gradient units until converted by a local Green/readout operator | UNIT_CONVENTION_STAGED_INPUTS_MISSING | matter/source action domain exclusion or derivative bound |
| S_boundary | S_boundary | compact boundary/source-memory coupling | E* or boundary-charge units until boundary projector and arena conversion are fixed | UNIT_CONVENTION_STAGED_INPUTS_MISSING | Q_X/B_X boundary charge, compact-support convention, projection norm |
| Dtheta_marker | Dtheta_marker_Dq_leak | constants/material markers | dimensionless derivative of measured constants/material markers with respect to retained Dq direction | UNIT_CONVENTION_STAGED_INPUTS_MISSING | mass/charge/clock constant owner or marker derivative bound |
| S_cg_envelope | S_cg_norm <= 0.5||T||_source*C_qm + S_direct + S_source_norm_extra + S_boundary | absolute no-cancellation envelope | E* forcing units until every component and conversion operator is source-backed | UNIT_CONVENTION_STAGED_INPUTS_MISSING | all component rows above, source stress norm, and no-cancellation conversion operator |

## Arena Projection Matrix

| arena_row_id | observable | empirical_upper_bound | empirical_units | leak_components | projection_status | predicted_residual |
| --- | --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | C_qm; Dq_Z; Dq_RAB_Jq | MISSING_OBSERVED_COFRAME_DERIVATIVE | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | S_direct; Dtheta_marker; S_cg_envelope | MISSING_MATERIAL_SOURCE_MAP | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R2_clock_redshift | alpha_clock_redshift | 2.48e-05 | dimensionless | Dq_phi; Dtheta_marker; C_qm | MISSING_CLOCK_READOUT_MAP | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R3_gamma | gamma_minus_1 | 2.3e-05 | dimensionless | C_qm; Dq_RAB_Jq; Dq_Z | MISSING_WEAK_FIELD_METRIC_RESPONSE | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R4_beta | beta_minus_1 | 7.8e-05 | dimensionless | C_qm; Dq_RAB_Jq; S_cg_envelope | MISSING_POST_NEWTONIAN_SECOND_ORDER_RESPONSE | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R5_alpha1 | alpha1 | 1e-04 | dimensionless | S_boundary; Dq_RAB_Jq; C_qm | MISSING_VECTOR_FRAME_PROJECTION | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R6_alpha2 | alpha2 | 2e-09 | dimensionless | S_boundary; Dq_RAB_Jq; C_qm | MISSING_ALPHA2_VECTOR_ANISOTROPY_MAP | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R7_alpha3 | alpha3 | 4e-20 | dimensionless | S_boundary; S_direct; Dtheta_marker | MISSING_DOMAIN_EXCHANGE_ZERO_OR_BOUND | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R8_xi | xi | 4e-09 | dimensionless | S_boundary; Dq_RAB_Jq; Dtheta_marker | MISSING_PREFERRED_LOCATION_PROJECTION | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R9_Gdot | Gdot_over_G | 9.6e-15 | yr^-1 | Dtheta_marker; S_direct; C_qm | MISSING_LOCAL_TIME_DERIVATIVE_MAP | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | Dq_Z; Dq_phi; Dq_RAB_Jq; C_qm; S_direct; S_boundary; Dtheta_marker | MISSING_R10_FIELD_MAP_AND_BOUND_CURVE | MISSING_NUMERIC_OR_THEOREM_ZERO |
| R11_EH_operator_ledger | non_EH_operator_coefficients | symbolic | operator family | Dq_Z; Dq_phi; Dq_RAB_Jq; S_cg_envelope | MISSING_OPERATOR_COEFFICIENT_VECTOR | MISSING_NUMERIC_OR_THEOREM_ZERO |

## R10 Source Pack Template

The R10 rows are schema-valid but not claim-valid. The live comparison remains:

```text
alpha_a = - beta_a s_a c^2 / (4 pi G_N Z_a)
|sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i)
```

| component_id | lambda_value | delta_w_a | Z_a | s_a | beta_a | alpha_predicted | tau_R10_a | alpha_bound | parent_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dq_Z | MISSING_R10_RANGE | MISSING_DQ_LEAK_AMPLITUDE_OR_THEOREM_ZERO | MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO | MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO | MISSING_MATTER_READOUT_COEFFICIENT_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO | MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE | CLOSURE_NONCLAIM_MISSING_R10_FIELD_MAP |
| Dq_phi | MISSING_R10_RANGE | MISSING_DQ_LEAK_AMPLITUDE_OR_THEOREM_ZERO | MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO | MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO | MISSING_MATTER_READOUT_COEFFICIENT_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO | MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE | CLOSURE_NONCLAIM_MISSING_R10_FIELD_MAP |
| Dq_RAB_Jq | MISSING_R10_RANGE | MISSING_DQ_LEAK_AMPLITUDE_OR_THEOREM_ZERO | MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO | MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO | MISSING_MATTER_READOUT_COEFFICIENT_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO | MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE | CLOSURE_NONCLAIM_MISSING_R10_FIELD_MAP |
| C_qm | MISSING_R10_RANGE | MISSING_DQ_LEAK_AMPLITUDE_OR_THEOREM_ZERO | MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO | MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO | MISSING_MATTER_READOUT_COEFFICIENT_OR_THEOREM_ZERO | MISSING_NUMERIC_OR_THEOREM_ZERO | MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO | MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE | CLOSURE_NONCLAIM_MISSING_R10_FIELD_MAP |

## PPN/WEP/Clock/Orbit Template Preview

| arena_row_id | observable | empirical_bound | required_leak_inputs | predicted_value | comparison_status |
| --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | 2.8e-15 | C_qm; Dq_Z; Dq_RAB_Jq | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | S_direct; Dtheta_marker; S_cg_envelope | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R2_clock_redshift | alpha_clock_redshift | 2.48e-05 | Dq_phi; Dtheta_marker; C_qm | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R3_gamma | gamma_minus_1 | 2.3e-05 | C_qm; Dq_RAB_Jq; Dq_Z | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R4_beta | beta_minus_1 | 7.8e-05 | C_qm; Dq_RAB_Jq; S_cg_envelope | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R5_alpha1 | alpha1 | 1e-04 | S_boundary; Dq_RAB_Jq; C_qm | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R6_alpha2 | alpha2 | 2e-09 | S_boundary; Dq_RAB_Jq; C_qm | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |
| R7_alpha3 | alpha3 | 4e-20 | S_boundary; S_direct; Dtheta_marker | MISSING_NUMERIC_OR_THEOREM_ZERO | BLOCKED_PENDING_SOURCE_INPUTS |

## Bound Comparison Placeholders

| arena_row_id | observable | bound_value | bound_status | predicted_value | comparison_ready | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | 2.8e-15 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R2_clock_redshift | alpha_clock_redshift | 2.48e-05 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R3_gamma | gamma_minus_1 | 2.3e-05 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R4_beta | beta_minus_1 | 7.8e-05 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R5_alpha1 | alpha1 | 1e-04 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R6_alpha2 | alpha2 | 2e-09 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R7_alpha3 | alpha3 | 4e-20 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R8_xi | xi | 4e-09 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R9_Gdot | Gdot_over_G | 9.6e-15 | BOUND_SOURCE_RECORDED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha(lambda) | CURVE_REQUIRED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |
| R11_EH_operator_ledger | non_EH_operator_coefficients | symbolic | OPERATOR_LEDGER_REQUIRED | MISSING_NUMERIC_OR_THEOREM_ZERO | False | False |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| D1669_0_pack_status | DQ_LEAK_SOURCE_PACK_ARENA_READY_NONCLAIM | 1668 leak symbols now have unit conventions, source requirements, and R0-R11 projection placeholders | do not score until parent-signed theorem-zero or numeric source rows exist |
| D1669_1_R10_status | R10_REMAINS_CURVE_AND_COEFFICIENT_BLOCKED | alpha(lambda), tau_R10, lambda, beta, source coupling, and kinetic normalization are all missing or symbolic | use R10 template only as a nonclaim acquisition checklist |
| D1669_2_best_next_domino | TARGET_CQM_OR_DQZ_FIRST | C_qm and Dq_Z sit closest to observed coframe descent and therefore feed WEP, PPN, and R10 rather than one arena only | attempt theorem-zero for observed coframe functor DObs_e[Dq[v]], and if it fails emit first finite C_qm/Dq_Z bound row |
| D1669_3_safety | NO_LOCAL_GR_NEWTON_CLAIM | a source pack is infrastructure, not a derivation of GR/Newton or an empirical pass | keep all local claims false until bound comparison rows become real and pass gates |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1669_0_Dq_numeric_or_zero | each retained Dq leak has numeric source row or theorem-zero | False | BLOCKED | all retained leak rows still contain MISSING_* inputs |
| CG1669_1_arena_projection | each arena has source-backed projection from Dq leak to observable | False | BLOCKED | R0-R11 projection matrix is schema-only |
| CG1669_2_R10 | R10 alpha(lambda) comparison can be scored | False | NO_CLAIM | R10 bound curve and parent coefficients missing |
| CG1669_3_WEP_PPN_clock_orbit | WEP/PPN/clock/orbital rows pass | False | NO_CLAIM | predicted residuals are placeholders |
| CG1669_4_local_GR_Newton | local GR/Newton reduction follows | False | NO_CLAIM | 1669 only prepares leak bounds; it does not prove q_loc=0 |
| CG1669_5_public_claim | public/local claim safe | False | NO_CLAIM | private checkpoint only |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md | scripts/Y5_R2FR_Cqm_DqZ_observed_coframe_zero_or_first_finite_bound_row.py | try to prove DObs_e[Dq[v]]=0 for the retained C_qm/Dq_Z leak; if that fails, emit the first finite nonclaim C_qm/Dq_Z source row with arena projections | either a parent-signed theorem-zero for C_qm/Dq_Z or a finite source-backed nonclaim row ready for WEP/PPN/R10 smoke comparison |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1669_0_sources_exist | PASS | all cited 1669 source paths exist and needles are present |
| VAL1669_1_leak_units_complete | PASS | all 1668 retained leak components have unit/source conventions |
| VAL1669_2_all_arenas_mapped | PASS | R0-R11 local arenas are mapped to Dq leak projection needs |
| VAL1669_3_R10_contract_fields | PASS | R10 source-pack template includes the 1503 contract fields |
| VAL1669_4_R10_remains_blocked | PASS | R10 rows remain blocked until parent coefficients and curve are real |
| VAL1669_5_local_templates_nonclaim | PASS | PPN/WEP/clock/orbit source templates remain nonclaim |
| VAL1669_6_bound_placeholders_nonclaim | PASS | bound comparison placeholders are not score-ready |
| VAL1669_7_claim_gates_safe | PASS | all claim gates keep local claims false |
| VAL1669_8_no_mts_claim_flags | PASS | all 1669 generated rows keep claim/no-score flags false |
| VAL1669_9_missing_not_ready | PASS | no row containing MISSING_* is marked source-backed, claim-ready, or score-ready |
| VAL1669_10_next_target_selected | PASS | next target selects C_qm/Dq_Z theorem-zero or finite bound row |
| VAL1669_11_csv_parse | PASS | all generated 1669 CSVs parse |
| VAL1669_12_branch_copies | PASS | branch/quarantine copies exist |
| VAL1669_13_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1669_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1669_15_formalization_untouched | PASS | no 1669 outputs found under formalization-workbench |
| VAL1669_OVERALL | PASS | 1669 Dq leak source-pack units and arena projections validation |

## Working Interpretation

This is the clean empirical bridge, not the prize itself. The best next attack is `C_qm`/`Dq_Z`: either prove the observed coframe functor kills the retained vertical leak, or write the first finite nonclaim bound row. If `C_qm` goes to zero by theorem, several local arenas tighten at once. If it does not, we at least stop guessing and start measuring the leak.
