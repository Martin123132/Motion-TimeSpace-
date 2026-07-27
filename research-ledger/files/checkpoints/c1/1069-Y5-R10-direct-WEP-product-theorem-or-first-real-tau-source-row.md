# 1069 — Direct WEP Product Theorem Or First Real tau Source Row

**Current verdict:** direct `P_WEP_relative_source_weight` is still the cleanest theory route, but the theorem does not close because parent variation to `eta_AB` is missing.

**Progress:** the first real MICROSCOPE eta/readout provenance row is now acquired from `local_bound_claims.csv`: numeric bound, units, URL, and DOI are recorded. This is not `tau_WEP` and not a prediction.

**Runner result:** strict product scoring remains blocked with `valid_prediction_rows=0`.

## Direct WEP Product Theorem Attempt
| theorem_id | claim | formal_move | attempt_result | gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DWT1069_0_target | derive P_WEP_relative_source_weight directly from parent variation | delta S_parent -> source residual -> eta_AB without splitting into Delta_w_TiPt and tau_WEP | TARGET_SHARPENED | needs source variation, force/readout map, and observed-frame eta convention | false |
| DWT1069_1_variation_route | parent variation gives the differential acceleration observable | P_WEP := readout_eta[delta_e S_matter, source worldtube, orbit average, material response] | FORMALLY_CLEAN_IF_ALL_MAPS_EXIST | 1068 shows those maps are acquisition rows, not derived objects | false |
| DWT1069_2_theorem_zero_route | direct product is theorem-zero | P_WEP=0 if source-scalar exclusion/action-scale owner or WEP projection silence is parent-signed | CONDITIONAL_ONLY | SSE1066 and ASO1067 verdicts are still unsigned | false |
| DWT1069_3_finite_route | direct product is a numeric finite prediction | P_WEP = abs(parent predicted eta_AB residual) in dimensionless MICROSCOPE convention | MISSING_NUMERIC_PARENT_PRODUCT | no source worldtube/orbit/readout/material/Xhat pack yet | false |
| DWT1069_4_no_shortcuts | refuse false direct products | reject tau=1, Delta_w=0 by taste, measured-G absorption of relative weights, and cancellation | REFUSAL_RULE_ACTIVE | none; this is a guard, not a derivation | false |
| DWT1069_5_verdict | direct WEP product theorem | parent variation to eta_AB product | DIRECT_PRODUCT_THEOREM_NOT_DERIVED | direct product remains preferred route, but first real source/readout row is needed for finite branch | false |


## First Real tau / Readout Source Rows
| tau_source_id | pack_component | fills_1068_row | dataset_id | row_id | observable | upper_bound | units | reference_url | doi | source_backed | claim_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WTS1069_0_MICROSCOPE_eta_source_charge_proxy | eta/readout bound anchor | TAP1068_2_eta_readout; ORB1068_2_eta_convention | MICROSCOPE_final_TiPt_source_charge_proxy | R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | https://arxiv.org/abs/2209.15487 | 10.1103/PhysRevLett.129.121102 | true | false | false |
| WTS1069_1_MICROSCOPE_direct_geometry_context | direct eta context | FRM1068_1_eta_mapping | MICROSCOPE_final_TiPt | R0_identity_coframe_direct | eta_WEP_direct_geometry | 2.8e-15 | dimensionless | https://arxiv.org/abs/2209.15487 | 10.1103/PhysRevLett.129.121102 | true | false | false |
| WTS1069_2_MICROSCOPE_material_smoke_context | material pair context | TAP1068_3_material_response; MAT1068_0_pair_convention | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION | MCON1061_0_test_pair | TA6V_minus_PtRh10 convention | not_applicable | dimensionless convention | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | not_applicable | internal_smoke_context | false | false |


## Provenance
| provenance_id | dataset_id | row_id | observable | reference_url | doi | use_in_1069 | source_backed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PROV1069_0_R1_source_charge | MICROSCOPE_final_TiPt_source_charge_proxy | R1_WEP_source_charge | eta_WEP_source_charge | https://arxiv.org/abs/2209.15487 | 10.1103/PhysRevLett.129.121102 | primary nonclaim source-charge/readout bound anchor | true | false |
| PROV1069_1_R0_direct_geometry | MICROSCOPE_final_TiPt | R0_identity_coframe_direct | eta_WEP_direct_geometry | https://arxiv.org/abs/2209.15487 | 10.1103/PhysRevLett.129.121102 | direct eta context, not source-weight prediction | true | false |


## Readout Fill Matrix
| matrix_id | component | filled_by | fill_status | still_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RFM1069_0_eta_bound | eta_AB upper bound/readout anchor | WTS1069_0_MICROSCOPE_eta_source_charge_proxy | SOURCE_BACKED_ANCHOR_FILLED | parent product; tau_WEP; orbit kernel; source worldtube; material tensor | false |
| RFM1069_1_eta_formula | eta_AB formula/sign/readout convention | local bound row only | PARTIAL_CONTEXT_ONLY | official formula/readout extraction row and parent force-map derivation | false |
| RFM1069_2_orbit_kernel | MICROSCOPE orbit/averaging kernel | none | MISSING | orbit/altitude/time/attitude averaging source | false |
| RFM1069_3_source_worldtube | Earth/source worldtube | none | MISSING | source profile, composition/source-charge convention, finite-source correction | false |
| RFM1069_4_material_tensor | Ti/Pt material response tensor | WTS1069_2 material pair smoke context | PAIR_CONTEXT_ONLY | full material/source response tensor | false |
| RFM1069_5_direct_product | direct parent P_WEP product | none | MISSING | parent variation to dimensionless eta_AB residual | false |


## Remaining Requirements
| requirement_id | requirement | current_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| REQ1069_0_direct_product | derive numeric/theorem-zero P_WEP_relative_source_weight directly | MISSING_DIRECT_PARENT_PRODUCT | try parent variation force/readout kernel | false |
| REQ1069_1_readout_formula | official MICROSCOPE eta_AB formula/sign/readout convention | PARTIAL_BOUND_PROVENANCE_ONLY | extract formula/source row from MICROSCOPE paper or local corpus | false |
| REQ1069_2_orbit_kernel | MICROSCOPE orbit/attitude/averaging kernel | MISSING_ORBIT_KERNEL | source official orbit/readout metadata | false |
| REQ1069_3_source_worldtube | Earth/source worldtube and source charge convention | MISSING_SOURCE_WORLDTUBE | source Earth profile or theorem-reduce to calibrated point-source convention | false |
| REQ1069_4_material_tensor | Ti/Pt source-weight material response tensor | MISSING_MATERIAL_TENSOR | source material model or derive theorem reducing to Delta_w_TiPt | false |
| REQ1069_5_xhat_norm | shared Xhat/chi_X normalization | MISSING_XHAT_NORMALIZATION | derive shared branch normalization or direct product | false |


## WEP Product Candidate
| prediction_id | arena | product_symbol | product_value | product_units | product_source | inputs_present | required_inputs | derivation_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1069_0_WEP_direct_or_tau_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_DIRECT_PRODUCT_OR_TAU_WEP_SPLIT_PRODUCT | dimensionless | source-intake/mts_residuals/P8_Y5_R10_1069_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv | MICROSCOPE_R1_eta_bound=2.8e-15;reference=https://arxiv.org/abs/2209.15487;doi=10.1103/PhysRevLett.129.121102 | direct parent P_WEP product OR tau_WEP source/orbit/readout pack plus Delta_w_TiPt | MISSING_DIRECT_PRODUCT_AND_TAU_SPLIT_PRODUCT | false | 1069 acquired the first real readout/bound provenance row only; prediction remains missing. |


## WEP Bound Import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_source | source_row | bound_type | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND1069_0_WEP_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | numeric_bound_anchor_nonclaim | true | MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction. |


## Runner Status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR1069_0_WEP_direct_or_tau_product | 1 | 1 | 0 | 1 | 1 | 0 | 1 | false | 2026-06-14T10:54:53.700551+00:00 |


## Runner Comparisons
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1069_0_direct_product_theorem | direct P_WEP product theorem is derived | false | parent variation to eta_AB remains missing | false | false |
| CG1069_1_first_real_source_row | first real MICROSCOPE eta/readout source row is acquired | true | R1 source-charge proxy row has numeric bound, units, URL, and DOI provenance | false | false |
| CG1069_2_tau_WEP_numeric | tau_WEP is numeric or theorem-zero | false | source row is a bound/readout anchor, not tau_WEP | false | false |
| CG1069_3_runner_score | WEP product can be scored | false | strict runner has valid_prediction_rows=0 | false | false |
| CG1069_4_local_GR_WEP | local GR/WEP coupling branch is derived | false | direct product and tau acquisition branches remain open | false | false |


## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1069_0_direct_product_status | direct WEP product theorem is not derived | parent variation still lacks eta_AB force/readout and source worldtube maps | keep direct theorem as preferred route, but acquire readout/formula data next | false |
| DEC1069_1_first_source_row_status | first real MICROSCOPE eta/readout source row is acquired as nonclaim provenance | local bound row R1 supplies numeric bound, units, URL, DOI, and reference note | extract official eta_AB formula/readout convention or orbit kernel | false |
| DEC1069_2_best_next | next target is MICROSCOPE eta formula/readout extraction or orbit kernel | the first source row gives a bound anchor but not a projection functional | 1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md | false |


## Source Register
| source_id | relative_path | exists | needle | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC1069_0_1068_next | source-intake/mts_residuals/P8_Y5_R10_1068_NEXT_TARGET.csv | true | 1069-Y5-R10-direct-WEP-product-theorem | true | false |
| SRC1069_1_1068_fallback | source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv | true | DPF1068_0_preferred_route | true | false |
| SRC1069_2_1068_pack | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | true | TAP1068_2_eta_readout | true | false |
| SRC1069_3_1068_orbit | source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | true | ORB1068_2_eta_convention | true | false |
| SRC1069_4_1068_force | source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | true | FRM1068_1_eta_mapping | true | false |
| SRC1069_5_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | true | SWT1068_5_verdict | true | false |
| SRC1069_6_1068_material | source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv | true | MAT1068_5_verdict | true | false |
| SRC1069_7_1067_tau | source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv | true | TAQ1067_3_direct_product_option | true | false |
| SRC1069_8_1062_parent | source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv | true | THM1062_6_verdict | true | false |
| SRC1069_9_1063_source | source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv | true | THM1063_5_verdict | true | false |
| SRC1069_10_1066_scalar | source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv | true | SSE1066_5_verdict | true | false |
| SRC1069_11_1067_action | source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv | true | ASO1067_5_verdict | true | false |
| SRC1069_12_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | MCON1061_0_test_pair | true | false |
| SRC1069_13_708_wep | source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv | true | PGW708_0_R1_WEP | true | false |
| SRC1069_14_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | R1_WEP_source_charge | true | false |
| SRC1069_15_393_common | 393-source-normalized-Newtonian-limit-under-identity-closure.md | true | Only a constant, universal, range-independent | true | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1069_SUMMARY | pass | 1069 direct WEP product theorem / first real tau source-row validation summary | 2026-06-14T10:54:55.597118+00:00 |
| V1069_1_sources_exist_and_needles | pass | every cited source path exists and every source needle was found | 2026-06-14T10:54:53.701883+00:00 |
| V1069_2_direct_theorem_not_promoted | pass | direct product theorem remains unproved | 2026-06-14T10:54:53.701897+00:00 |
| V1069_3_first_real_source_row_acquired | pass | first real MICROSCOPE eta/readout source row acquired with numeric bound and units | 2026-06-14T10:54:53.701902+00:00 |
| V1069_4_provenance_has_url_doi | pass | provenance rows contain source URL and DOI | 2026-06-14T10:54:53.701913+00:00 |
| V1069_5_readout_matrix_partial_only | pass | readout matrix records first filled anchor while orbit kernel remains missing | 2026-06-14T10:54:53.701919+00:00 |
| V1069_6_remaining_requirements_written | pass | remaining direct/tau requirements are written as nonclaim rows | 2026-06-14T10:54:53.701924+00:00 |
| V1069_7_prediction_nonclaim | pass | WEP product prediction remains nonclaim | 2026-06-14T10:54:53.701928+00:00 |
| V1069_8_bound_anchor_numeric | pass | WEP bound anchor is numeric | 2026-06-14T10:54:53.701933+00:00 |
| V1069_9_runner_refuses_placeholder | pass | strict runner refuses missing direct/tau product | 2026-06-14T10:54:53.701937+00:00 |
| V1069_10_claim_gates_safe | pass | first source-row gate passes only as nonclaim provenance and all claims remain blocked | 2026-06-14T10:54:53.701942+00:00 |
| V1069_11_next_target_written | pass | next target selects eta formula/readout or orbit kernel acquisition | 2026-06-14T10:54:53.701945+00:00 |
| V1069_12_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T10:54:53.707001+00:00 |
| V1069_13_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T10:54:55.597100+00:00 |


## Next Target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md | extract the official MICROSCOPE eta_AB formula/readout convention and, if available, the first orbit/averaging kernel row; keep all rows nonclaim until a direct P_WEP product or tau_WEP projection exists. | eta_AB definition, sign/absolute-value convention, test-mass pair convention, orbit/attitude/averaging source row, URL/DOI provenance, unit checks, runner refusal gates | setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits | false |

