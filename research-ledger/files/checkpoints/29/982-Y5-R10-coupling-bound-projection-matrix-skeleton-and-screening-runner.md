# 982 Y5 R10: Coupling Bound Projection Matrix Skeleton And Screening Runner

Status: `Y5_R10_982_projection_matrix_skeleton_written_screening_runner_blocks_all_claims_missing_MTS_projection_maps`

Claim ceiling: screening infrastructure only. No WEP, `Gdot`, `alpha3`, R10, PPN, Newtonian-limit, or local-GR pass is claimed.

## Readout

981 gave source-backed observational anchors. 982 turns those anchors into the actual map we need:

`observable_vector = ProjectionMatrix * MTS_residual_coefficient_vector`.

The runner is intentionally conservative. It accepts that numeric source bounds exist, but refuses to score any MTS coefficient while the projection matrix contains `MISSING_*` entries. This prevents the classic mistake of treating an experimental bound as if it were already a bound on the theory's private coefficient.

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 981_doc | handoff selecting projection matrix/screening runner | true | true | 981-Y5-R10-finite-coupling-prior-source-acquisition-bkappa-Gdot-alpha3.md |
| 981_candidates | source-backed observational candidate bounds | true | true | source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv |
| 981_web_sources | web provenance ledger | true | true | source-intake/mts_residuals/P8_Y5_R10_981_WEB_SOURCE_LEDGER.csv |
| 981_anchor_reconciliation | local anchor/source reconciliation | true | true | source-intake/mts_residuals/P8_Y5_R10_981_LOCAL_ANCHOR_RECONCILIATION.csv |
| 980_fallback | finite-prior fallback selected after no-marker theorem rejection | true | true | source-intake/mts_residuals/P8_Y5_R10_980_FINITE_PRIOR_FALLBACK.csv |
| 979_priority | coupling-prior priority rows | true | true | source-intake/mts_residuals/P8_Y5_R10_979_QBAR_PRIOR_SOURCE_PRIORITY.csv |
| 978_qbar_rows | qbar/source prior row schema | true | true | source-intake/mts_residuals/P8_Y5_R10_978_QBAR_SOURCE_PRIOR_RUNNER_ROWS.csv |
| 622_doc | parent matter sector component definitions | true | true | 622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md |
| 417_boundary | alpha3/Gdot local anchor source | true | true | 417-boundary-exchange-nohair-theorem-attempt.md |

## Coefficient Slots

| coefficient_id | component | parameter | meaning | current_status | units | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| COEF982_0_b_kappa_source_weight | b_kappa | species_source_weight_splitting | composition/species dependence of active gravitational source normalization | MISSING_PARENT_UNIVERSAL_SOURCE_OR_NUMERIC_PROJECTION | dimensionless | false |
| COEF982_1_b_kappa_running | b_kappa | d_ln_Geff_dXhat_or_dlnGdt | local/environmental running of effective gravitational coupling | MISSING_XHAT_TIME_ENVIRONMENT_MAP | dimensionless per Xhat or yr^-1 | false |
| COEF982_2_b_theta_constants | b_theta | d_ln_alpha_EM_dXhat and d_ln_mass_ratio_dXhat | MTS dependence of ordinary matter constants | MISSING_CONSTANT_SUPERSELECTION_OR_CLOCK_EM_PRIOR | dimensionless | false |
| COEF982_3_b_m_marker | b_m | marker_coupling_projection | unclassified material/quotient marker coupling | MISSING_MARKER_TAXONOMY_OR_BOUND | dimensionless | false |
| COEF982_4_K_boundary_alpha3 | boundary_alpha3_flux | K_boundary_alpha3 | boundary/local projection into preferred-frame alpha3-like residual | MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX | dimensionless | false |
| COEF982_5_qbarXT_vec | qbarXT_vec | P_A_qbarXT_vec | ordinary/local test-body residual vector after failed theorem-zero route | MISSING_K_X_QBAR_XH_LAMBDA_AND_BOUND_CURVE | dimensionless vector projection | false |

## Projection Matrix Skeleton

| projection_id | observable | source_prior | screening_bound | bound_units | projection_formula | required_projection_inputs | missing_marker | runner_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PMAT982_0_WEP_eta_TiPt | eta_TiPt | CP981_0_b_kappa_species_split_WEP | 6.992e-15 | dimensionless | eta_TiPt = S_TiPt_bkappa*b_kappa + S_TiPt_btheta*b_theta + S_TiPt_bm*b_m + S_TiPt_bNH*b_NH | S_TiPt_bkappa,S_TiPt_btheta,S_TiPt_bm,S_TiPt_bNH,composition_charge_basis | MISSING_SOURCE_CHARGE_PROJECTION | not_scoreable | false |
| PMAT982_1_Gdot_orbital | Gdot_over_G | CP981_1_kappa_running_Gdot | 2.420e-14 | yr^-1 | Gdot/G = (d ln Geff/d Xhat)*(d Xhat/dt)_local + B_boundary_time | dXhat_dt_local,environment_profile,clock_or_orbital_epoch_map,B_boundary_time | MISSING_ENVIRONMENT_PROFILE_AND_XHAT_TIME_MAP | not_scoreable | false |
| PMAT982_2_alpha3_strong_pulsar | alpha3_hat_strong | CP981_2_alpha3_strong_pulsar | 4.000e-20 | dimensionless | alpha3_hat = P_strong_boundary*K_boundary_alpha3 + P_strong_bkappa*b_kappa + P_strong_spin*B_spin | strong_to_local_matching,P_strong_boundary,P_strong_bkappa,P_strong_spin,compactness_sensitivity | MISSING_STRONG_TO_LOCAL_PPN_PROJECTION | not_scoreable | false |
| PMAT982_3_alpha3_weak_solar | alpha3_weak_solar | CP981_3_alpha3_weak_solar | 6.000e-10 | dimensionless | alpha3_weak = P_weak_boundary*K_boundary_alpha3 + P_weak_bkappa*b_kappa + P_weak_frame*b_g | P_weak_boundary,P_weak_bkappa,P_weak_frame,local_preferred_frame_map | MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX | not_scoreable | false |
| PMAT982_4_R10_alpha_lambda | alpha_lambda_R10 | QSP978_7_qbarXT_vec plus R10 bound curve | MISSING_REAL_ALPHA_LAMBDA_BOUND_FOR_THIS_ROW | dimensionless | alpha_pred(lambda)=K_X*Qbar_XH(lambda)*P_A_qbarXT_vec | K_X,Qbar_XH(lambda),P_A_qbarXT_vec,lambda_X,source_backed_alpha_bound(lambda) | MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE | not_scoreable | false |

## Screening Runner

| screen_id | observable | numeric_bound_present | projection_inputs_missing_count | missing_marker | screen_result | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCREEN982_0_WEP_eta_TiPt | eta_TiPt | true | 5 | MISSING_SOURCE_CHARGE_PROJECTION | blocked_missing_projection | false | false |
| SCREEN982_1_Gdot_orbital | Gdot_over_G | true | 4 | MISSING_ENVIRONMENT_PROFILE_AND_XHAT_TIME_MAP | blocked_missing_projection | false | false |
| SCREEN982_2_alpha3_strong_pulsar | alpha3_hat_strong | true | 5 | MISSING_STRONG_TO_LOCAL_PPN_PROJECTION | blocked_missing_projection | false | false |
| SCREEN982_3_alpha3_weak_solar | alpha3_weak_solar | true | 4 | MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX | blocked_missing_projection | false | false |
| SCREEN982_4_R10_alpha_lambda | alpha_lambda_R10 | false | 5 | MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE | blocked_missing_projection | false | false |

## Identity Sanity Rows

| sanity_id | observable | identity_assumption | identity_bound_on_slot | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| IS982_0_WEP_identity | eta_TiPt | S_TiPt_bkappa=1 and all other sensitivities zero | abs(b_kappa) <= 6.992e-15 | composition/source-charge projection is not derived; identity assumption is a debug convention only | false |
| IS982_1_Gdot_identity | Gdot_over_G | dXhat/dt=1 yr^-1 and no boundary term | abs(d_ln_Geff/dXhat) <= 2.420e-14 | Xhat time/environment map is missing | false |
| IS982_2_alpha3hat_identity | alpha3_hat_strong | P_strong_boundary=1 and no strong/local mismatch | abs(K_boundary_alpha3) <= 4.000e-20 | strong-field alpha3_hat is not automatically local weak-field alpha3 | false |
| IS982_3_alpha3weak_identity | alpha3_weak_solar | P_weak_boundary=1 and other channels zero | abs(K_boundary_alpha3) <= 6.000e-10 | weak-field projection matrix is missing and source is preliminary | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CGATE982_0_projection_matrix_written | projection matrix skeleton exists | true | false | skeleton existence is not a physics pass |
| CGATE982_1_WEP_score | b_kappa is bounded by MICROSCOPE | false | false | source-charge/composition sensitivity matrix is missing |
| CGATE982_2_Gdot_score | kappa-running branch is bounded | false | false | Xhat time/environment map is missing |
| CGATE982_3_alpha3_score | K_boundary_alpha3 is bounded | false | false | strong/weak alpha3 projection matrices are missing |
| CGATE982_4_R10_score | R10 alpha(lambda) branch is scoreable | false | false | K_X, Qbar_XH(lambda), P_A qbarXT vector, lambda_X, and source-backed bound curve are missing |
| CGATE982_5_local_GR | local GR/Newton/PPN/R10 branch passes | false | false | screening-only runner blocks every arena while projections are missing |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC982_0_matrix | projection discipline | projection_matrix_skeleton_written | each observational anchor now has an explicit map from MTS coefficient slots to measured channel | fill one projection map rather than adding more source anchors |
| DEC982_1_screening_runner | runner status | screening_runner_blocks_all_claims | numeric source bounds exist but every row has missing MTS projection inputs | keep identity assumptions as debug-only rows |
| DEC982_2_best_next | next checkpoint | WEP_source_charge_projection_first | WEP/source-splitting is the most direct b_kappa pressure and maps onto the universal-source theorem gap | write 983 WEP/source-charge projection matrix attempt for MICROSCOPE Ti/Pt |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V982_0_sources | pass | all local handoff/source files exist and needles are found | 2026-06-14T01:40:34.399291+00:00 |
| V982_1_coefficients_nonclaim | pass | coefficient slots are explicit missing-input nonclaim rows | 2026-06-14T01:40:34.399303+00:00 |
| V982_2_projection_rows_nonclaim | pass | projection rows keep MISSING_* markers | 2026-06-14T01:40:34.399306+00:00 |
| V982_3_screening_blocks | pass | screening runner blocks every claim while projections are missing | 2026-06-14T01:40:34.399309+00:00 |
| V982_4_identity_rows_nonclaim | pass | identity sanity rows are debug-only nonclaim rows | 2026-06-14T01:40:34.399311+00:00 |
| V982_5_claim_gates_safe | pass | claim gates do not allow local-GR or coefficient-bound claims | 2026-06-14T01:40:34.399314+00:00 |
| V982_6_next_decision | pass | 983 WEP/source-charge projection selected | 2026-06-14T01:40:34.399316+00:00 |
| V982_7_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T01:40:34.399318+00:00 |
| V982_8_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T01:40:34.399321+00:00 |
| V982_READY | pass | 982 checkpoint pack validation summary | 2026-06-14T01:40:34.399324+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 983-Y5-R10-WEP-source-charge-projection-matrix-MICROSCOPE-TiPt.md | derive or skeletonize the composition/source-charge projection from MICROSCOPE Ti/Pt eta into MTS b_kappa, b_theta, and marker slots | Ti/Pt composition sensitivity placeholders, b_kappa vs b_theta separation, source-charge basis, nonclaim screening row | claiming WEP pass, invented composition coefficients, local-GR promotion, GitHub action, formalization-workbench edits | false |
