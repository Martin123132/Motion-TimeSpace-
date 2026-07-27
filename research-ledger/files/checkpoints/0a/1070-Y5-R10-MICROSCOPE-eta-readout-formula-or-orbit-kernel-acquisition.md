# 1070 - MICROSCOPE eta readout formula or orbit-kernel acquisition

## Current verdict
1070 closes a real plumbing gap: the official MICROSCOPE eta definition and delta_x readout identification are now source-backed. It does **not** close the WEP/local-GR branch, because the full tau_WEP projection, source worldtube, material tensor, and direct parent product are still absent.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1070_0_1069_next | source-intake/mts_residuals/P8_Y5_R10_1069_NEXT_TARGET.csv | true | true | 1069 handoff selecting eta/readout acquisition. |
| SRC1070_1_1069_first_tau | source-intake/mts_residuals/P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv | true | true | first source-backed WEP bound/readout anchor. |
| SRC1070_2_1069_provenance | source-intake/mts_residuals/P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv | true | true | MICROSCOPE provenance ledger. |
| SRC1070_3_1069_fill | source-intake/mts_residuals/P8_Y5_R10_1069_READOUT_FILL_MATRIX.csv | true | true | eta formula remained partial in 1069. |
| SRC1070_4_1069_requirements | source-intake/mts_residuals/P8_Y5_R10_1069_REMAINING_TAU_REQUIREMENTS.csv | true | true | remaining tau/readout requirements. |
| SRC1070_5_1068_orbit | source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv | true | true | MICROSCOPE orbit/readout requirements. |
| SRC1070_6_1068_force | source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv | true | true | observed-frame eta map requirement. |
| SRC1070_7_1068_tau_pack | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | true | true | tau_WEP acquisition pack. |
| SRC1070_8_1068_worldtube | source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv | true | true | source worldtube gap. |
| SRC1070_9_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | true | Ti/Pt material convention. |
| SRC1070_10_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | local MICROSCOPE bound source rows. |
| SRC1070_11_708_wep | source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv | true | true | WEP source/test charge vector gap. |
| SRC1070_12_1062_parent | source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv | true | true | prior parent product theorem blocker. |

## External MICROSCOPE source ledger
| external_id | doi | source_lines | extracted_item | source_backed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EXT1070_0_CQG_eta_formula | 10.1088/1361-6382/ac84be | arXiv abstract; DLR/IOP PDF front matter | eta(A,B)=2(a_A-a_B)/(a_A+a_B) | true | false |
| EXT1070_1_CQG_result_readout | 10.1088/1361-6382/ac84be | PDF lines 1216-1223 | eta(Ti,Pt) is identified with delta_x; final value is [-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15 | true | false |
| EXT1070_2_CQG_measurement_axis | 10.1088/1361-6382/ac84be | PDF lines 341-346 | test-mass accelerations are sampled at 4 Hz and the differential acceleration is computed along the sensitive X axis | true | false |
| EXT1070_3_CQG_orbit_segments | 10.1088/1361-6382/ac84be | PDF lines 1226-1231 | SUREF Pt/Pt used 13 segments/598 orbits/41 days; SUEP Pt/Ti used 19 segments/1362 orbits/94 days | true | false |
| EXT1070_4_CQG_analysis_band | 10.1088/1361-6382/ac84be | PDF lines 918-924 | parameter estimation uses bands around f_EP and 2 f_EP; a wider-domain check increases uncertainty but does not noticeably shift parameters | true | false |
| EXT1070_5_CQG_data_availability | 10.1088/1361-6382/ac84be | PDF lines 1274-1276 | science data are available from https://cmsm-ds.onera.fr/ | true | false |
| EXT1070_6_PRL_eta_bound_anchor | 10.1103/PhysRevLett.129.121102 | PRL/arXiv abstract and 1069 local bound row | Ti/Pt final result supplies the source-backed 2.8e-15 WEP bound anchor already imported in 1069 | true | false |

## Eta readout rows
| eta_id | formula_or_item | units | status | MTS_impact | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ETA1070_0_formula | eta_AB = 2(a_A-a_B)/(a_A+a_B) | dimensionless | SOURCE_BACKED_FORMULA_FILLED | observable convention acquired; not a tau_WEP prediction | false |
| ETA1070_1_delta_x_identification | eta(Ti,Pt) approximately equals measured delta_x in the MICROSCOPE convention | dimensionless | SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED | links the official eta observable to the instrument differential channel | false |
| ETA1070_2_result_value | Ti/Pt eta measured=-1.5e-15; one_sigma=2.74590604355e-15; upper_bound=2.8e-15 | dimensionless | SOURCE_BACKED_RESULT_CONTEXT_FILLED | bound row remains a nonclaim comparator; direct row R0_identity_coframe_direct remains separate | false |
| ETA1070_3_sign_pair_convention | A/B sign is source-backed for eta_AB, but not yet mapped onto MTS TA6V_minus_PtRh10 sign convention | dimensionless | PARTIAL_SIGN_CONTEXT_ONLY | absolute-value score can use the bound, but signed model comparison still needs material/readout orientation | false |
| ETA1070_4_verdict | eta formula and delta_x readout are filled; tau_WEP and direct product are not | dimensionless | FORMULA_FILLED_NOT_TAU | this upgrades data plumbing, not local-GR/WEP closure | false |

## Orbit/readout kernel source rows
| orbit_id | component | source_backed_value | status | missing_for_tau | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ORK1070_0_sampling_axis | sample/readout axis | 4 Hz acceleration sampling; differential acceleration along sensitive X axis | SOURCE_BACKED_PARTIAL_READOUT_ROW | full map from parent residual to X-axis eta channel | false |
| ORK1070_1_segments_orbits | segment/orbit exposure | SUEP Pt/Ti 19 segments, 1362 orbits, 94 days; SUREF Pt/Pt 13 segments, 598 orbits, 41 days | SOURCE_BACKED_PARTIAL_ORBIT_ROW | time-dependent orbit/attitude weights and source line-of-sight kernel | false |
| ORK1070_2_spin_session | spin/session planning | analysis is organized around f_EP and 2f_EP bands; earlier session metadata references V2/V3 spin rates and long sessions | SOURCE_BACKED_PARTIAL_SPIN_ROW | machine-readable attitude/spin kernel | false |
| ORK1070_3_frequency_band | frequency-domain analysis band | fit bands around f_EP and 2f_EP | SOURCE_BACKED_PARTIAL_ANALYSIS_KERNEL | exact weighting/filter operator for an MTS predicted signal | false |
| ORK1070_4_data_availability | data portal | https://cmsm-ds.onera.fr/ | SOURCE_BACKED_DATA_PORTAL | downloaded data products, schema, and reproducible kernel extraction | false |
| ORK1070_5_verdict | orbit/averaging kernel verdict | partial metadata acquired, not a full orbit/attitude/averaging kernel | PARTIAL_ORBIT_METADATA_NOT_TAU_KERNEL | full kernel or source-worldtube row | false |

## Readout fill matrix update
| fill_id | component | current_status | evidence_rows | blocks_claim |
| --- | --- | --- | --- | --- |
| RFM1070_0_eta_bound | MICROSCOPE eta bound | SOURCE_BACKED_BOUND_ANCHOR_PRESENT | WTS1069_0; ETA1070_2 | false |
| RFM1070_1_eta_formula | eta_AB formula | SOURCE_BACKED_FORMULA_FILLED | ETA1070_0 | false |
| RFM1070_2_delta_x | eta to delta_x readout identification | SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED | ETA1070_1 | false |
| RFM1070_3_sampling_axis | 4 Hz X-axis measurement row | SOURCE_BACKED_PARTIAL_READOUT_ROW | ORK1070_0 | true |
| RFM1070_4_orbit_metadata | orbit/segment metadata | SOURCE_BACKED_PARTIAL_ORBIT_ROW | ORK1070_1; ORK1070_3 | true |
| RFM1070_5_full_orbit_kernel | full orbit/attitude/averaging kernel | MISSING_FULL_KERNEL | none | true |
| RFM1070_6_source_worldtube | Earth/source worldtube | MISSING_SOURCE_WORLDTUBE | SWT1068_5_verdict | true |
| RFM1070_7_material_tensor | Ti/Pt material response tensor | MISSING_MATERIAL_TENSOR | MCON1061_0_test_pair | true |
| RFM1070_8_direct_product | direct P_WEP product | MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL | THM1062_4_tau_WEP_projection | true |

## Tau impact ledger
| impact_id | new_input | impact | remaining_gap | claim_policy |
| --- | --- | --- | --- | --- |
| TAI1070_0_formula_does_not_define_tau | eta_AB formula | defines the observable normalization only | tau_WEP/source product still absent | no scoreable MTS prediction |
| TAI1070_1_readout_axis_partial | 4 Hz X-axis readout row | constrains the observed channel | no parent residual to X-axis projection operator | partial kernel only |
| TAI1070_2_orbit_partial | segment/orbit/frequency metadata | identifies exposure and analysis bands | no machine-readable orbit/attitude/averaging kernel | partial source-backed acquisition |
| TAI1070_3_no_unity_shortcut | bound plus formula | does not license tau_WEP=1 or Delta_w=0 | direct product theorem or full projection kernel | shortcut forbidden |
| TAI1070_4_verdict | 1070 acquisition pack | readout plumbing improved | tau_WEP remains missing | WEP/local-GR claim remains blocked |

## Nonclaim product candidate
| prediction_id | arena | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PRED1070_0_WEP_eta_formula_or_orbit_kernel_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL | MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL | false |

## Bound import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_type | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BOUND1070_0_MICROSCOPE_R1_eta_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source_backed_upper_bound_anchor | true |

## Product runner status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| APR1070_0_WEP_product_stub | 1 | 1 | 0 | 1 | false | reject eta/readout-only placeholder prediction and keep claim false |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1070_0_eta_formula_acquired | eta formula | true | false | source-backed observable definition, not an MTS prediction |
| CG1070_1_orbit_metadata_partial | orbit/readout metadata | true | false | partial metadata only; full kernel missing |
| CG1070_2_full_orbit_kernel | full orbit/attitude/averaging kernel | false | false | MISSING_FULL_KERNEL |
| CG1070_3_tau_WEP_numeric | tau_WEP numeric/direct product | false | false | MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL |
| CG1070_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |
| CG1070_5_local_GR_WEP_claim | local-GR/WEP pass | false | false | eta formula acquired but WEP product remains unscored |

## Decision ledger
| decision_id | decision | evidence | consequence |
| --- | --- | --- | --- |
| DEC1070_0_readout_acquired | eta formula and delta_x identification are now source-backed nonclaim rows | ETA1070_0_formula; ETA1070_1_delta_x_identification | readout convention no longer the first blocker |
| DEC1070_1_orbit_partial_only | orbit/readout metadata is useful but not a tau kernel | ORK1070_5_verdict | do not score MTS against MICROSCOPE yet |
| DEC1070_2_best_next | move to full orbit kernel or source-worldtube acquisition | RFM1070_5_full_orbit_kernel; RFM1070_6_source_worldtube | 1071 should try the first tau_WEP projection component |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1070_0_sources_exist | pass | all cited local paths and needles are present |
| V1070_1_external_provenance | pass | CQG DOI and data portal recorded |
| V1070_2_eta_formula_dimensionless | pass | eta formula filled as dimensionless |
| V1070_3_bound_numeric | pass | bound import has positive numeric value |
| V1070_4_orbit_partial_not_kernel | pass | orbit acquisition remains partial |
| V1070_5_full_kernel_still_missing | pass | full kernel is not silently filled |
| V1070_6_tau_still_missing | pass | tau verdict remains blocked |
| V1070_7_prediction_nonclaim_missing | pass | prediction row stays nonclaim and missing |
| V1070_8_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1070_9_claim_gates_safe | pass | all claim gates deny public/local-GR/WEP claim |
| V1070_10_next_target | pass | 1071 handoff written |
| V1070_11_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1070_12_csv_parse | pass | all 1070 CSV outputs parse cleanly |
| V1070_13_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1070_SUMMARY | pass | formula acquired; orbit metadata partial; tau/product claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1070_0_1071 | 1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md | acquire or derive the first full tau_WEP projection component: either an official MICROSCOPE orbit/attitude/averaging kernel usable in the eta readout map, or an Earth/source-worldtube row; keep product scoring blocked until all required tau/direct-product components exist. | orbit ephemeris/attitude/averaging kernel; source worldtube profile; eta formula integration; material tensor; Xhat normalization; URL/DOI/data portal provenance; refusal gates | tau=1; Delta_w=0 by taste; measured-G absorption of relative weights; cancellation; public WEP/local-GR claim; GitHub; formalization edits |

