# 1205 Y5/R10 First B_T Or eps_P Source Row Fill

**Current verdict:** 1205 does not find an accepted numeric source row for either `||B_T||` or `eps_P/C_CK/Delta_P`. It therefore refuses to fill a fake value and converts the result into a stricter blocker ledger plus pressure targets.

**Main progress:** the corpus scan distinguishes templates/target thresholds from evidence rows. The harsh equal-split target remains `q_boundary <= 1.17233215026e-05` and `q_projector <= 1.17233215026e-05`, while the boundary trace product route requires `||n.K_T|| ||P_loc V|| <= 1.17233215026e-05`.

## Source Register

| source_id | local_path | needle | purpose | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1205_0_1204_next | 1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound.md | NEXT1204_0_1205 | handoff requesting first B_T or eps_P source-row fill | True | True | False | False |
| SRC1205_1_1204_schemas | source-intake/mts_residuals/P8_Y5_R10_1204_SOURCE_READY_BOUND_ROWS.csv | SBR1204_3_projector_finite_bound | source-ready boundary/projector row schemas | True | True | False | False |
| SRC1205_2_1204_targets | source-intake/mts_residuals/P8_Y5_R10_1204_BOUNDARY_PROJECTOR_FINITE_TARGETS.csv | FBP1204_WR10F1202_2_brutal_100x_boundary_projector_split | finite target inequalities for B_T and Delta_P | True | True | False | False |
| SRC1205_3_1204_epsilon | source-intake/mts_residuals/P8_Y5_R10_1204_PROJECTOR_EPSILON_TARGETS.csv | EPT1204_WR10F1202_2_brutal_100x_G1 | eps_P target grid for projector leakage | True | True | False | False |
| SRC1205_4_1171_bc_template | source-intake/mts_residuals/P8_Y5_R10_1171_FIRST_FINITE_BC_BOUND_ROW.csv | FBC1171_0_first_boundary_bound_row | older finite boundary-bound schema precedent | True | True | False | False |
| SRC1205_5_1172_bc_symbolic | source-intake/mts_residuals/P8_Y5_R10_1172_BC_BOUND_FILLED_FROM_JC_SCHEMA.csv | BCF1172_0_symbolic_bound | symbolic finite-bound route with numeric inputs missing | True | True | False | False |
| SRC1205_6_1175_projector | source-intake/mts_residuals/P8_Y5_R10_1175_PROJECTOR_LEAK_BOUND_ROWS.csv | PLB1175_0_first_projector_leak_row | older projector leakage bound schema precedent | True | True | False | False |
| SRC1205_7_1197_template | source-intake/mts_residuals/P8_Y5_R10_1197_COKERNEL_BOUND_INPUT_TEMPLATE.csv | MISSING_B_T_BOUNDARY_NORM | R10/PPN/clock/orbital q_DT input template still missing B_T | True | True | False | False |

## Corpus Scan Candidates

| scan_id | file | row_count | keyword_rows | numeric_hint_cells | missing_marker_rows | accepted_source_rows | classification | example_rows | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCAN1205_000 | source-intake/mts_residuals/P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv | 8 | 1 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row1:T1_scalar_boundary_action | False | False |
| SCAN1205_001 | source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv | 9 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:CC4_boundary_variation_equals_projected_source_variation | False | False |
| SCAN1205_002 | source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | 9 | 2 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:Delta_PiM \| row8:Delta_PPN | False | False |
| SCAN1205_003 | source-intake/mts_residuals/P8_charge_current_equality_STATUS.csv | 6 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row1:charge-current equality parent-derived | False | False |
| SCAN1205_004 | source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv | 9 | 1 |  | 9 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:Z2_calibrated_PiM_flux_conservation | False | False |
| SCAN1205_005 | source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv | 11 | 1 |  | 11 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row7:LRV_QCOH_PROJECTOR_OWNERSHIP | False | False |
| SCAN1205_006 | source-intake/mts_residuals/P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:D505_0_local_parent_action_form | False | False |
| SCAN1205_007 | source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv | 5 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:QB516_3_PPN_metric_tail | False | False |
| SCAN1205_008 | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv | 8 | 1 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:SM509_5_no_extra_channel | False | False |
| SCAN1205_009 | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_DECISION.csv | 4 | 1 |  | 0 | 0 | TARGET_OR_TEMPLATE_ONLY | row3:D509_3 | False | False |
| SCAN1205_010 | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv | 8 | 2 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row1:SMR509_1_Delta_PiM \| row7:SMR509_7_Delta_PPN | False | False |
| SCAN1205_011 | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_SOURCE_REGISTER.csv | 14 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row9:source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | False | False |
| SCAN1205_012 | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | 3 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:T509_2_no_extra_mass_channel | False | False |
| SCAN1205_013 | source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv | 11 | 1 |  | 11 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:A3_boundary_class_topological | False | False |
| SCAN1205_014 | source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv | 8 | 2 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:MR510_3_projector_hair \| row7:MR510_7_PPN_tail | False | False |
| SCAN1205_015 | source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv | 8 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row6:P510_6 | False | False |
| SCAN1205_016 | source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | 4 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:T510_2_MTS_transfer_condition | False | False |
| SCAN1205_017 | source-intake/mts_residuals/P8_Y5_BRR545_1199_VALIDATION.csv | 11 | 1 |  | 2 | 0 | TARGET_OR_TEMPLATE_ONLY | row10:V1199_SUMMARY | False | False |
| SCAN1205_018 | source-intake/mts_residuals/P8_Y5_BRR545_607_VALIDATION.csv | 10 | 1 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row3:V607_3_exponent_gate_keeps_p_unpromoted | False | False |
| SCAN1205_019 | source-intake/mts_residuals/P8_Y5_BRR545_620_VALIDATION.csv | 9 | 1 |  | 2 | 0 | TARGET_OR_TEMPLATE_ONLY | row2:V620_2_residual_basis_complete | False | False |
| SCAN1205_020 | source-intake/mts_residuals/P8_Y5_BRR545_621_DECISION.csv | 4 | 1 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row2:D621_2_residual_priors | False | False |
| SCAN1205_021 | source-intake/mts_residuals/P8_Y5_BRR545_621_VALIDATION.csv | 10 | 1 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row5:V621_5_component_status_complete | False | False |
| SCAN1205_022 | source-intake/mts_residuals/P8_Y5_BRR545_695_VALIDATION.csv | 15 | 3 |  | 2 | 0 | TARGET_OR_TEMPLATE_ONLY | row3:V695_3_zero_not_promoted \| row7:V695_7_product_bound_nonclaim | False | False |
| SCAN1205_023 | source-intake/mts_residuals/P8_Y5_BRR545_700_VALIDATION.csv | 12 | 2 |  | 2 | 0 | TARGET_OR_TEMPLATE_ONLY | row5:V700_5_Delta_Poisson_fill_unfilled \| row11:V700_11_status_nonclaim | False | False |
| SCAN1205_024 | source-intake/mts_residuals/P8_Y5_BRR545_701_VALIDATION.csv | 14 | 4 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row2:V701_2_700_Delta_Poisson_still_unfilled \| row3:V701_3_zero_theorem_audit_blocks | False | False |
| SCAN1205_025 | source-intake/mts_residuals/P8_Y5_BRR545_702_VALIDATION.csv | 13 | 2 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row6:V702_6_delta_candidate_unfilled \| row12:V702_12_status_nonclaim | False | False |
| SCAN1205_026 | source-intake/mts_residuals/P8_Y5_BRR545_703_VALIDATION.csv | 15 | 2 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row8:V703_8_Delta_Poisson_update_unfilled \| row14:V703_14_status_nonclaim | False | False |
| SCAN1205_027 | source-intake/mts_residuals/P8_Y5_BRR545_704_VALIDATION.csv | 14 | 2 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row7:V704_7_Delta_Poisson_update_unfilled \| row13:V704_13_status_nonclaim | False | False |
| SCAN1205_028 | source-intake/mts_residuals/P8_Y5_BRR545_705_VALIDATION.csv | 14 | 1 |  | 2 | 0 | TARGET_OR_TEMPLATE_ONLY | row13:V705_13_status_nonclaim | False | False |
| SCAN1205_029 | source-intake/mts_residuals/P8_Y5_BRR545_706_VALIDATION.csv | 14 | 1 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row13:V706_13_status_nonclaim | False | False |
| SCAN1205_030 | source-intake/mts_residuals/P8_Y5_BRR545_735_VALIDATION.csv | 17 | 1 |  | 1 | 0 | TARGET_OR_TEMPLATE_ONLY | row8:V735_8_boundary_theorem_steps_present | False | False |
| SCAN1205_031 | source-intake/mts_residuals/P8_Y5_BRR545_764_VALIDATION.csv | 16 | 1 |  | 0 | 0 | TARGET_OR_TEMPLATE_ONLY | row7:V764_7_btheta_components_retained | False | False |
| SCAN1205_032 | source-intake/mts_residuals/P8_Y5_BRR545_983_VALIDATION.csv | 13 | 1 |  | 0 | 0 | TARGET_OR_TEMPLATE_ONLY | row4:V983_4_delta_proxies_nonzero | False | False |
| SCAN1205_033 | source-intake/mts_residuals/P8_Y5_BRR545_REFERENCE_LOCK_THEOREM_ATTEMPT.csv | 6 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:RLT548_4_projector_and_extra_symplectic_contamination | False | False |
| SCAN1205_034 | source-intake/mts_residuals/P8_Y5_EULER_WARD_CHAIN_TEST.csv | 6 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:EW538_5_local_readout | False | False |
| SCAN1205_035 | source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv | 9 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row6:EX522_6_projector_stress | False | False |
| SCAN1205_036 | source-intake/mts_residuals/P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv | 4 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:OM522_2_PPN_source_vector | False | False |
| SCAN1205_037 | source-intake/mts_residuals/P8_Y5_EXTRA_MASS_ROUTE_UPDATE.csv | 5 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:Y5_RADIAL_SOURCE_HAIR | False | False |
| SCAN1205_038 | source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv | 6 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:AG523_5_no_overclaim | False | False |
| SCAN1205_039 | source-intake/mts_residuals/P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row6:GO523_6_PPN_residual_vector | False | False |
| SCAN1205_040 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_BOUND_FILL_ROW.csv | 1 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:MISSING_PARENT_ANOMALY_ZERO_OR_BOUND | False | False |
| SCAN1205_041 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_EXTRA_CHARGE_CHANNEL_MAP.csv | 9 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row6:projector variation shifts mass charge through the annulus | False | False |
| SCAN1205_042 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv | 6 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:GPT540_5_full_PPN_vector | False | False |
| SCAN1205_043 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv | 8 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:HPT553_5_no_extra_charge | False | False |
| SCAN1205_044 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:RA540_3_extra_mass_channels | False | False |
| SCAN1205_045 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:SMT540_4_no_extra_mass_channels | False | False |
| SCAN1205_046 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | 8 | 2 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:HSM541_4_zero_extra_source_channels \| row7:HSM541_7_PPN_followthrough | False | False |
| SCAN1205_047 | source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv | 8 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:HSS541_4_extra_channels | False | False |
| SCAN1205_048 | source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv | 9 | 1 |  | 9 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row8:HWT536_8_weak_field_readout_after_charge_glue | False | False |
| SCAN1205_049 | source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | 10 | 2 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:PAC537_3_local_EH_symplectic_fixed_point \| row9:PAC537_9_second_order_PPN_stability | False | False |
| SCAN1205_050 | source-intake/mts_residuals/P8_Y5_MEFF_FLUX_BOUND_UPDATE.csv | 4 | 1 |  | 4 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:Y5B_9_q_loc_projection | False | False |
| SCAN1205_051 | source-intake/mts_residuals/P8_Y5_MINIMAL_PARENT_ACTION_TEST_CASES.csv | 3 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:EW538_C_residual_bound_branch | False | False |
| SCAN1205_052 | source-intake/mts_residuals/P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv | 6 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:DAT537_5_local_readout | False | False |
| SCAN1205_053 | source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv | 6 | 1 |  | 1 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:PIF537_5_Gauss_readout_residual | False | False |
| SCAN1205_054 | source-intake/mts_residuals/P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv | 17 | 1 |  | 17 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:AUD536_4 | False | False |
| SCAN1205_055 | source-intake/mts_residuals/P8_Y5_PIM_OWNER_DECISION.csv | 5 | 1 |  | 0 | 0 | TARGET_OR_TEMPLATE_ONLY | row3:D521_3_radial_bound | False | False |
| SCAN1205_056 | source-intake/mts_residuals/P8_Y5_PIM_OWNER_ROUTE_UPDATE.csv | 5 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:Y5_RADIAL_SOURCE_HAIR | False | False |
| SCAN1205_057 | source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv | 5 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:PI521_0_Delta_PiM | False | False |
| SCAN1205_058 | source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv | 12 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row11:MTS_local_GR_branch | False | False |
| SCAN1205_059 | source-intake/mts_residuals/P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row6:MEX524_6_no_cancellation_PPN_envelope | False | False |
| SCAN1205_060 | source-intake/mts_residuals/P8_Y5_PPN_RESIDUAL_VECTOR.csv | 12 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row11:PPN524_11_total_PPN_envelope | False | False |
| SCAN1205_061 | source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv | 7 | 1 |  | 6 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:QBF1011_3_PPN_metric_tail | False | False |
| SCAN1205_062 | source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_RUNNER.csv | 7 | 1 |  | 6 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row3:QBR1011_3_PPN_metric_tail | False | False |
| SCAN1205_063 | source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv | 8 | 1 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row7:OBS1013_7_calibration_PPN_tail | False | False |
| SCAN1205_064 | source-intake/mts_residuals/P8_Y5_R10_1013_OBSTRUCTION_RUNNER.csv | 8 | 1 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row7:OBR1013_7_calibration_PPN_tail | False | False |
| SCAN1205_065 | source-intake/mts_residuals/P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv | 6 | 1 |  | 6 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:PCC1014_4_Delta_PiM | False | False |
| SCAN1205_066 | source-intake/mts_residuals/P8_Y5_R10_1014_RUNNER.csv | 6 | 1 |  | 6 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:PCR1014_4_Delta_PiM | False | False |
| SCAN1205_067 | source-intake/mts_residuals/P8_Y5_R10_1063_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv | 4 | 1 |  | 4 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:PRED1063_0_WEP_relative_source_weight | False | False |
| SCAN1205_068 | source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv | 5 | 1 |  | 5 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:REQ1064_0_WEP_species | False | False |
| SCAN1205_069 | source-intake/mts_residuals/P8_Y5_R10_1064_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv | 5 | 1 |  | 5 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:PRED1064_0_WEP_relative_source_weight | False | False |
| SCAN1205_070 | source-intake/mts_residuals/P8_Y5_R10_1094_WEP_SOURCE_CONTEXT_LEDGER.csv | 5 | 1 |  | 3 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row1:CTX1094_1_material_response | False | False |
| SCAN1205_071 | source-intake/mts_residuals/P8_Y5_R10_1095_NUMERIC_ROW_REQUIREMENTS.csv | 5 | 1 |  | 2 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:NR1095_2_material_delta | False | False |
| SCAN1205_072 | source-intake/mts_residuals/P8_Y5_R10_1130_ID_VARIATION_LEDGER.csv | 5 | 1 |  | 5 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row1:VAR1130_1_delta_Pcoh | False | False |
| SCAN1205_073 | source-intake/mts_residuals/P8_Y5_R10_1148_SOURCE_OWNER_ZERO_THEOREM_AUDIT.csv | 8 | 2 |  | 8 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row4:OWN1148_4_no_extra_mass_projection \| row6:OWN1148_6_second_order_stability | False | False |
| SCAN1205_074 | source-intake/mts_residuals/P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv | 10 | 2 |  | 10 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row7:GLUE1150_7_extra_exchange_silence \| row8:GLUE1150_8_Gauss_orbital_after_glue | False | False |
| SCAN1205_075 | source-intake/mts_residuals/P8_Y5_R10_1167_RUNNER_DRY_RUN.csv | 4 | 1 |  | 3 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:RUN1167_0_continuity_law | False | False |
| SCAN1205_076 | source-intake/mts_residuals/P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv | 7 | 2 |  | 7 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row2:VTC1193_2_balance_action \| row4:VTC1193_4_observable_response | False | False |
| SCAN1205_077 | source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv | 6 | 3 |  | 5 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:DTR1194_0_PPN_gamma_beta_first_row \| row2:DTR1194_2_R10_alpha_lambda_slot | False | False |
| SCAN1205_078 | source-intake/mts_residuals/P8_Y5_R10_1195_DT_ADJOINT_COKERNEL_THEOREM.csv | 7 | 1 |  | 0 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row5:DTA1195_5_bound_if_cokernel_survives | False | False |
| SCAN1205_079 | source-intake/mts_residuals/P8_Y5_R10_1195_FIRST_RESPONSE_SOURCE_ROWS.csv | 3 | 2 |  | 3 | 0 | SYMBOLIC_OR_MISSING_INPUTS_ONLY | row0:FRS1195_0_PPN_gamma_beta_source_row \| row1:FRS1195_1_R10_alpha_lambda_source_row | False | False |

## Source Fill Attempt

| attempt_id | component | candidate_source_status | filled_value | units | source_path | comparison_target | target_context | passes_target | blocked_by | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FILL1205_0_boundary_finite_BT | q_boundary=\|\|B_T\|\| | NO_ACCEPTED_NUMERIC_SOURCE_ROW_FOUND |  | dimensionless q_DT budget units after same-frame normalization |  | 1.17233215026e-05 | harsh W=100 boundary/projector equal split | False | missing K_T_normal_trace_norm;missing P_locV_trace_norm;missing trace_pairing_bound;missing source_path | False | False |
| FILL1205_1_projector_epsP | q_projector=\|\|Delta_P\|\| or eps_P\|\|G_res\|\| | NO_ACCEPTED_NUMERIC_SOURCE_ROW_FOUND |  | dimensionless q_DT budget units after same-frame normalization |  | 1.17233215026e-05 | harsh W=100 boundary/projector equal split | False | missing Delta_P_norm;missing eps_P;missing G_res_norm;missing C_CK;missing C_CK_eps_P;missing source_path | False | False |

## Bound Pressure Targets

| pressure_id | component | target_context | required_bound | factorized_condition | if_second_factor_normalized_to_1 | if_equal_factors_each_less_than | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRS1205_0_boundary_only_trace_bound | q_boundary | harsh W=100, only q_boundary live | 2.34466430052e-05 | \|\|n.K_T\|\|_{H-1/2} * \|\|P_loc V\|\|_{H1/2} <= required_bound | 2.34466430052e-05 | 0.0048421733762 | TARGET_ONLY_NO_SOURCE_VALUE | False | False |
| PRS1205_1_boundary_split_trace_bound | q_boundary | harsh W=100, q_boundary/q_projector equal split | 1.17233215026e-05 | \|\|n.K_T\|\|_{H-1/2} * \|\|P_loc V\|\|_{H1/2} <= required_bound | 1.17233215026e-05 | 0.00342393362999 | TARGET_ONLY_NO_SOURCE_VALUE | False | False |
| PRS1205_2_projector_only_delta_bound | q_projector | harsh W=100, only q_projector live | 2.34466430052e-05 | \|\|Delta_P\|\| <= required_bound | 2.34466430052e-05 |  | TARGET_ONLY_NO_SOURCE_VALUE | False | False |
| PRS1205_3_projector_split_eps_G1 | eps_P | harsh W=100, q_projector split, assumed \|\|G_res\|\|=1 | 1.17233215026e-05 | eps_P * \|\|G_res\|\| <= required_bound and C_CK*eps_P < 1 | 1.17233215026e-05 |  | TARGET_ONLY_NO_SOURCE_VALUE | False | False |

## Blocker Ledger

| blocker_id | component | missing_input | why_it_blocks | best_derivation_route | fallback_source_route | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK1205_0_boundary_missing_trace_norms | q_boundary | K_T_normal_trace_norm and P_locV_trace_norm or direct trace_pairing_bound | 1204 finite row can compare only after the boundary pairing bound is numeric in the same local norm | derive n_mu K_T^(mu nu)=0 from parent boundary action, or derive a trace estimate from a sourced K_T boundary equation | fill SBR1204_1 with boundary_geometry_path, K_T normal norm, P_locV trace norm, units, and source_path | False | False |
| BLK1205_1_projector_missing_eps_constants | q_projector | Delta_P_norm or eps_P, G_res_norm, C_CK, and C_CK_eps_P | projector absorption needs C_CK eps_P<1 and finite scoring needs eps_P\|\|G_res\|\| below threshold | derive nabla P_loc=0/coframe lock/domain-motion silence from parent quotient geometry | fill SBR1204_3 with Delta_P_norm or eps_P*G_res_norm plus C_CK and source_path | False | False |
| BLK1205_2_same_domain_guard | q_boundary and q_projector | single parent-owned local domain/norm for boundary, projector, q_DT, and R10 readout | a boundary estimate in one domain cannot be combined with a projector estimate in another | define the local test domain and P_loc from the parent quotient map before numeric comparison | carry all rows as nonclaim until domain_id and norm_id match | False | False |

## Comparison Ledger

| comparison_id | component | candidate_value | target | comparison_status | claim_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMP1205_0_current_BT | q_boundary | MISSING | 1.17233215026e-05 | BLOCKED_NO_NUMERIC_SOURCE_ROW | NONCLAIM | False | False |
| CMP1205_1_current_epsP | q_projector | MISSING | 1.17233215026e-05 | BLOCKED_NO_NUMERIC_SOURCE_ROW | NONCLAIM | False | False |
| CMP1205_2_scan_verdict | corpus_scan | 0 | at least one accepted source row | NO_ACCEPTED_SOURCE_ROWS_IN_SCAN | NONCLAIM | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1205_0_BT_source | real numeric B_T finite-bound row | BLOCKED | scan found symbolic templates/targets but no source-backed trace_pairing_bound | False | False |
| GATE1205_1_epsP_source | real numeric eps_P/C_CK/Delta_P row | BLOCKED | scan found symbolic projector-leak rows/targets but no source-backed eps_P or Delta_P_norm | False | False |
| GATE1205_2_no_fabrication | no placeholder promoted | ACTIVE_GUARD | 1205 refuses to fill a numeric source row from target thresholds or symbolic formulas | False | False |
| GATE1205_3_R10_local_GR | R10/local-GR branch | BLOCKED | boundary/projector components remain missing; R10/local-GR pass is not claimable | False | False |

## Decision Ledger

| decision_id | condition | decision | result | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DEC1205_0_verdict | no accepted numeric source row found for B_T or eps_P/C_CK/Delta_P | do not fill the component value; convert the attempt into a stricter blocker ledger plus pressure targets | target remains q_boundary or q_projector <= 1.17233215026e-05 for harsh equal split; accepted_source_rows=0 | derive the missing value from parent geometry rather than keep scanning: either K_T boundary trace law or P_loc/coframe leakage smallness | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1205_0_1206 | 1206-Y5-R10-KT-boundary-trace-law-or-Ploc-leakage-smallness-derivation.md | scripts/Y5_R10_KT_boundary_trace_law_or_Ploc_leakage_smallness_derivation.py | derive one of the two missing numeric/source laws from parent geometry: either a K_T normal trace zero/bound or a P_loc leakage eps_P/C_CK smallness theorem | one component gets a parent-derived zero theorem or a formula whose remaining inputs are lower-level geometric constants, not an undefined B_T/eps_P placeholder | do not rescan templates as evidence, do not claim R10/local-GR pass, do not edit formalization-workbench, do not push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1205_0_sources_exist | all cited local sources exist | PASS | 8/8 sources exist | False | False |
| VAL1205_1_needles_found | all cited source needles found | PASS | 8/8 needles found | False | False |
| VAL1205_2_scan_nonempty | corpus scan found candidate/template rows | PASS | scan_rows=430 | False | False |
| VAL1205_3_no_accepted_sources | no numeric source row is falsely accepted | PASS | accepted_source_rows=0 | False | False |
| VAL1205_4_fill_attempts_blocked | source-fill attempts remain blocked rather than fabricated | PASS | attempt_rows=2 | False | False |
| VAL1205_5_pressure_positive | pressure targets are positive | PASS | pressure_rows=4 | False | False |
| VAL1205_6_blockers_cover_components | blocker ledger covers boundary and projector | PASS | q_boundary,q_projector,q_boundary and q_projector | False | False |
| VAL1205_7_comparison_blocked | current comparison does not claim pass | PASS | BLOCKED_NO_NUMERIC_SOURCE_ROW;BLOCKED_NO_NUMERIC_SOURCE_ROW;NO_ACCEPTED_SOURCE_ROWS_IN_SCAN | False | False |
| VAL1205_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout | False | False |
| VAL1205_9_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1205_SOURCE_REGISTER.csv:8; P8_Y5_R10_1205_CORPUS_SCAN_CANDIDATES.csv:430; P8_Y5_R10_1205_SOURCE_FILL_ATTEMPT.csv:2; P8_Y5_R10_1205_BOUND_PRESSURE_TARGETS.csv:4; P8_Y5_R10_1205_BLOCKER_LEDGER.csv:3; P8_Y5_R10_1205_COMPARISON_LEDGER.csv:3; P8_Y5_R10_1205_CLAIM_GATES.csv:4; P8_Y5_R10_1205_DECISION_LEDGER.csv:1; P8_Y5_R10_1205_NEXT_TARGET.csv:1 | False | False |
| VAL1205_10_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1205_11_overall | overall 1205 validation | PASS | 1205 source-fill audit is reproducible and nonclaim | False | False |
