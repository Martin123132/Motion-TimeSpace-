# 651 Y5/R10 WEP Alpha-Sensitivity Source Fill or Screening Stress Test

## Verdict

- Status: `Y5_R10_WEP_alpha_sensitivity_source_fill_stress_test_blocks_unit_source_screen_nonclaim`
- Claim ceiling: `WEP_alpha_sensitivity_stress_test_only_no_WEP_or_local_GR_claim`
- The MICROSCOPE Ti/Pt WEP row is now connected to a source-backed smoke model for alpha/Coulomb and nuclear-binding composition charges.
- The result is not a WEP pass: the shared clock screen alone is not enough if the WEP force source normalization is order unity.
- With `|kappa_alpha|=1`, `S_lab_alpha=2.933e-08`, and unit source normalization, the alpha/Coulomb row predicts `eta~5.84e-11`, far above `2.8e-15`.
- Therefore the finite-alpha branch needs either a parent-derived common-geometry zero theorem or a source-normalization suppression target of order `beta_source_alpha <= 5e-5` in this smoke model.

## Source Register

| source_id | source_type | label | path_or_url | exists_or_reachable | role |
| --- | --- | --- | --- | --- | --- |
| S651_0 | local_path | checkpoint_650_doc | 650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md | true | prior cross-arena screening contract |
| S651_1 | local_path | validation_650 | source-intake/mts_residuals/P8_Y5_BRR545_650_VALIDATION.csv | true | prior validation |
| S651_2 | local_path | screen_rule_650 | source-intake/mts_residuals/P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv | true | shared screen variable owner |
| S651_3 | local_path | projection_requirements_650 | source-intake/mts_residuals/P8_Y5_R10_650_ARENA_PROJECTION_REQUIREMENTS.csv | true | WEP missing-projection clause |
| S651_4 | local_path | local_bound_matrix_639 | source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv | true | MICROSCOPE bound ledger row |
| S651_5 | local_path | bound_input_ledger_645 | source-intake/mts_residuals/P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv | true | WEP numeric bound source slot |
| S651_6 | local_path | WEP_species_universality_371 | 371-WEP-species-universality-or-active-eta-runner.md | true | prior WEP species universality no-go |
| S651_7 | local_path | WEP_observed_coframe_373 | 373-one-observed-coframe-parent-selector-or-WEP-closure.md | true | prior one-coframe closure contract |
| S651_8 | local_path | WEP_common_F_388 | 388-WEP-species-symmetry-common-F-parent-selector-attempt.md | true | prior species-blind geometry functor contract |
| S651_9 | local_path | generator_script_651 | scripts/Y5_R10_WEP_alpha_sensitivity_source_fill_or_screening_stress_test.py | true | this checkpoint generator |
| S651_10 | web_source | MICROSCOPE_final_PRL_arxiv | https://arxiv.org/abs/2209.15487 | not_checked_by_local_validator | source for Ti/Pt WEP result eta(Ti,Pt) and mission final result |
| S651_11 | web_source | MICROSCOPE_material_alloys | https://microscope3.sciencesconf.org/conference/microscope3/pages/2013_Hardy_ASR_Validation_of_the_in_flight_calibration_procedures_for_the_MICROSCOPE_space_mission_.pdf | not_checked_by_local_validator | source for PtRh10 and TA6V alloy mass-fraction model |
| S651_12 | web_source | Damour_Donoghue_2010_dilaton_charges | https://arxiv.org/abs/1007.2792 | not_checked_by_local_validator | source for alpha/Coulomb and nuclear-binding composition charges |
| S651_13 | web_source | Damour_2012_review_two_charge_model | https://www.theisticscience.com/papers/tree/Gravity/Damour_2012_Class._Quantum_Grav._29_184001.pdf | not_checked_by_local_validator | source for simplified Q1 prime/Q2 prime charge formulas used as a smoke estimate |

## MICROSCOPE Material Model

| material_model_id | material_id | element | mass_fraction | Z | A_used | model_limit |
| --- | --- | --- | --- | --- | --- | --- |
| MM651_PtRh10_Pt | PtRh10 | Pt | 0.900000 | 78 | 195.0 | mass-fraction alloy average with nominal A values; not a full isotope/chemical material model |
| MM651_PtRh10_Rh | PtRh10 | Rh | 0.100000 | 45 | 103.0 | mass-fraction alloy average with nominal A values; not a full isotope/chemical material model |
| MM651_TA6V_Ti | TA6V | Ti | 0.900000 | 22 | 48.0 | mass-fraction alloy average with nominal A values; not a full isotope/chemical material model |
| MM651_TA6V_Al | TA6V | Al | 0.060000 | 13 | 27.0 | mass-fraction alloy average with nominal A values; not a full isotope/chemical material model |
| MM651_TA6V_V | TA6V | V | 0.040000 | 23 | 51.0 | mass-fraction alloy average with nominal A values; not a full isotope/chemical material model |

## Damour-Donoghue Charge Estimate

| charge_row_id | material_id | charge_kind | formula | charge_value | claim_grade |
| --- | --- | --- | --- | --- | --- |
| Q651_PtRh10_alpha | PtRh10 | Q_alpha_Coulomb | Q1_prime = 7.7e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged | 3.996544904717e-03 | source_backed_smoke_estimate_not_full_material_model |
| Q651_PtRh10_surface | PtRh10 | Q_surface_binding | Q2_prime = -0.036/A^(1/3)-1.4e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged | -7.081912827580e-03 | source_backed_smoke_estimate_not_full_material_model |
| Q651_TA6V_alpha | TA6V | Q_alpha_Coulomb | Q1_prime = 7.7e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged | 2.006736017892e-03 | source_backed_smoke_estimate_not_full_material_model |
| Q651_TA6V_surface | TA6V | Q_surface_binding | Q2_prime = -0.036/A^(1/3)-1.4e-4*Z*(Z-1)/A^(4/3), alloy mass-fraction averaged | -1.038836917498e-02 | source_backed_smoke_estimate_not_full_material_model |
| Q651_delta_TA6V_minus_PtRh10_alpha_Coulomb | TA6V_minus_PtRh10 | Delta_Q_alpha_Coulomb | Delta Q = Q(TA6V)-Q(PtRh10) | -1.989808886825e-03 | stress_test_only |
| Q651_delta_TA6V_minus_PtRh10_surface_binding | TA6V_minus_PtRh10 | Delta_Q_surface_binding | Delta Q = Q(TA6V)-Q(PtRh10) | -3.306456347405e-03 | stress_test_only |

## WEP Alpha Stress Test

| stress_id | channel | eta_bound_used | shared_screen_used | delta_Q_TA6V_minus_PtRh10_abs | unit_source_eta_prediction | overshoot_factor_vs_MICROSCOPE | required_abs_beta_source_max | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WAS651_0_alpha_Coulomb | alpha/Coulomb composition channel | 2.800000e-15 | S_lab_alpha from 650 | 1.989808886825e-03 | 5.836031862511e-11 | 2.084297e+04 | 4.797780522732e-05 | unit_source_fails_requires_source_normalization_or_zero_theorem |
| WAS651_1_surface_binding | nuclear surface/binding composition channel | 2.800000e-15 | S_lab_alpha from 650 | 3.306456347405e-03 | 9.697707515141e-11 | 3.463467e+04 | 2.887280314062e-05 | unit_source_fails_requires_source_normalization_or_zero_theorem |
| WAS651_2_clock_screen_only | cross-arena rule diagnostic | 2.800000e-15 | S_lab_alpha from 650 | not_applicable | not_applicable | not_applicable | not_applicable | clock_screen_alone_is_not_a_WEP_pass_because_force_source_normalization_is_independent |

## Screening Option Gates

| gate_id | route | condition | current_result | WEP_result_if_closed | status |
| --- | --- | --- | --- | --- | --- |
| WG651_0_common_geometry_zero | prove species-blind geometry / common observed coframe | parent action forces all matter to one ehat and forbids F_A(C_D), m_A(C_D), alpha_A(C_D) | conditional_only_from_373_388 | direct composition alpha channel zero | best_derivation_route_not_yet_parent_signed |
| WG651_1_source_normalization_bound | derive small beta_source for local Earth/Test-mass force | beta_source_alpha <= about 5e-5 for alpha/Coulomb unit-kappa stress row, or stronger if surface channel included | not_derived | finite alpha branch can survive WEP without a zero theorem | numeric_target_written |
| WG651_2_same_screen_only | use clock screen S_lab_alpha with no source-normalization theorem | eta_AB = Delta Q * S_lab_alpha for unit source | fails_by_four_orders_in_smoke_estimate | not_applicable | rejected_as_claim_route |
| WG651_3_arena_specific_WEP_screen | invent S_WEP different from S_clock | S_WEP << S_clock without parent domain reason | forbidden_by_650_no_special_pleading | invalid | policy_fail |

## Decision

| decision_id | route | decision | why | next_target |
| --- | --- | --- | --- | --- |
| D651_0 | WEP_alpha_sensitivity_source_fill | source_backed_smoke_estimate_written | MICROSCOPE materials and Damour-Donoghue charges give a nonzero Ti/Pt alpha-composition lever arm | 652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md |
| D651_1 | clock_screen_only | rejected_as_WEP_claim_route | with unit source normalization the shared clock screen still overshoots MICROSCOPE by about four orders | 652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md |
| D651_2 | best_next_theorem | derive_source_normalization_or_common_geometry_zero | WEP now needs either beta_source suppression, species-blind one-coframe theorem, or alpha channel absence | 652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md |

## Next Contract

| contract_id | work_item | acceptance_condition |
| --- | --- | --- |
| NC651_0 | Try to prove a common-geometry zero theorem for the WEP alpha/composition channel. | parent action forbids species-dependent F_A, m_A, alpha_A and leaves one observed coframe for all matter |
| NC651_1 | If zero theorem fails, derive or source beta_source_alpha for Earth/test-mass force normalization. | beta_source_alpha is parent-derived/source-backed and below the numeric target written in 651 |
| NC651_2 | Upgrade the alloy smoke estimate only if exact isotope/material charge data are needed. | full material model replaces nominal A mass-fraction averaging before any claim |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V651_0_local_source_paths_exist | pass | all cited local source paths exist |
| V651_1_prior_650_validation_clean | pass | 650 validation remains clean |
| V651_2_material_fractions_sum_to_one | pass | material fraction sums: {'PtRh10': 1.0, 'TA6V': 1.0} |
| V651_3_delta_charges_nonzero | pass | Ti/Pt alpha and surface charge differences are nonzero at smoke level |
| V651_4_unit_source_overshoots | pass | unit-source WEP smoke overshoots MICROSCOPE by more than four orders |
| V651_5_beta_target_written | pass | source-normalization target below 5e-5 is written |
| V651_6_clock_screen_not_WEP_pass | pass | clock screen alone is explicitly not a WEP pass |
| V651_7_zero_and_bound_routes_present | pass | zero theorem and source-bound routes are both present |
| V651_8_arena_specific_screen_forbidden | pass | arena-specific WEP screen is forbidden |
| V651_9_all_rows_nonclaim | pass | all output rows remain nonclaim |
| V651_10_decision_selects_652 | pass | decision and next contract point to 652 |
| V651_11_summary_blocks_WEP_claim | pass | summary blocks WEP claim and records beta target |
| V651_12_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is not fatal, but it is properly sharp: WEP is saying `do not confuse local time-drift screening with force-source suppression`.
- The cleanest survival route is still the derivation route: one observed coframe, species-blind geometry, no species-dependent alpha or mass class functions.
- If that theorem fails, the finite-alpha branch needs a real source-normalization derivation, not another phenomenological knob.

## Nonclaim Summary

| status | MICROSCOPE_eta_bound | shared_screen_kappa_one | delta_Q_alpha_Coulomb_abs | unit_source_eta_alpha_Coulomb | required_beta_source_alpha_max | WEP_claim | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_WEP_alpha_sensitivity_source_fill_stress_test_blocks_unit_source_screen_nonclaim | 2.800e-15 | 2.933e-08 | 1.990e-03 | 5.836e-11 | 4.798e-05 | false | source-force normalization beta_source or common-geometry zero theorem is missing | 652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md |
