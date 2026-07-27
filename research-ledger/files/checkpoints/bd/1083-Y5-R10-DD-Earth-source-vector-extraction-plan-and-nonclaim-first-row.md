# 1083-Y5-R10 DD Earth source vector extraction plan and nonclaim first row

## Current verdict
1083 builds the first numeric DD-basis Earth source-vector candidate from a bulk-Earth composition table target and the existing alpha/surface smoke convention. This is useful plumbing, not a claim: the row is bulk-weighted rather than shell/profile/worldtube weighted, the parent-to-DD coefficient map is still unsigned, the official MICROSCOPE readout arrays are still missing, and the common-mode shortcut is not proven.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1083_0_1082_next | source-intake/mts_residuals/P8_Y5_R10_1082_NEXT_TARGET.csv | true | true | 1082 handoff. |
| SRC1083_1_1082_validation | source-intake/mts_residuals/P8_Y5_BRR545_1082_VALIDATION.csv | true | true | 1082 validation summary. |
| SRC1083_2_1082_earth_fill | source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv | true | true | Earth source vectorization gap. |
| SRC1083_3_1082_parent_to_DD | source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv | true | true | parent-to-DD map remains unsigned. |
| SRC1083_4_1082_readout_fill | source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv | true | true | MICROSCOPE readout arrays still missing. |
| SRC1083_5_1081_delta | source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv | true | true | DD material delta import. |
| SRC1083_6_1081_basis | source-intake/mts_residuals/P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv | true | true | DD basis schema. |
| SRC1083_7_1080_web | source-intake/mts_residuals/P8_Y5_R10_1080_WEB_SOURCE_CANDIDATE_REGISTER.csv | true | true | web source candidate register. |
| SRC1083_8_1080_earth | source-intake/mts_residuals/P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv | true | true | Earth source route gates. |
| SRC1083_9_1080_readout | source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv | true | true | MICROSCOPE readout gate. |
| SRC1083_10_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Web source register
| web_source_id | role | source_url | extraction_method | confidence_level |
| --- | --- | --- | --- | --- |
| WEB1083_0_MCDONOUGH_2003_TABLE5 | bulk Earth composition table target | https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf | manual table-target transcription into candidate rows; not a machine-readable official table import | medium_for_nonclaim_source_vector; insufficient_for_claim |
| WEB1083_1_MCDONOUGH_SUN_1995 | composition provenance continuity | https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/ | provenance link only; no new numeric extraction from this page | source-continuity-only |
| WEB1083_2_DAMOUR_DONOGHUE_2010 | external DD alpha/surface charge basis | https://arxiv.org/abs/1007.2792 | reuse existing local smoke convention rather than promote the external basis to MTS | good_for_external_comparator; not_MTS_derived |
| WEB1083_3_MICROSCOPE_FINAL | WEP bound source | https://arxiv.org/abs/2209.15487 | bound import only; official readout arrays still not imported | bound_source_backed; prediction_nonclaim |

## Bulk Earth composition target
| element | wt_percent | normalized_mass_fraction | Z | A | extraction_status |
| --- | --- | --- | --- | --- | --- |
| Fe | 32 | 3.204486280793110e-01 | 26 | 55.845 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| O | 29.7 | 2.974163829361106e-01 | 8 | 15.999 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Si | 16.1 | 1.612257160024034e-01 | 14 | 28.085 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Mg | 15.4 | 1.542159022631684e-01 | 12 | 24.305 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Ni | 1.82 | 1.822551572201082e-02 | 28 | 58.693 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Ca | 1.71 | 1.712397356298818e-02 | 20 | 40.078 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Al | 1.59 | 1.592229120769077e-02 | 13 | 26.982 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| S | 0.64 | 6.408972561586221e-03 | 16 | 32.06 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Cr | 0.47 | 4.706589224914881e-03 | 24 | 51.996 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Na | 0.18 | 1.802523532946125e-03 | 11 | 22.99 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| P | 0.07 | 7.009813739234929e-04 | 15 | 30.974 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| Mn | 0.08 | 8.011215701982776e-04 | 25 | 54.938 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| C | 0.07 | 7.009813739234929e-04 | 6 | 12.011 | TABLE_TARGET_CANDIDATE_NONCLAIM |
| H | 0.03 | 3.004205888243541e-04 | 1 | 1.008 | TABLE_TARGET_CANDIDATE_NONCLAIM |

## DD charge formula ledger
| formula_id | component | formula | status | claim_blocker |
| --- | --- | --- | --- | --- |
| DDF1083_0_alpha_Coulomb | Q_alpha_Coulomb | 7.7e-4 * Z*(Z-1) / A^(4/3) | IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM | not derived from MTS parent action |
| DDF1083_1_surface_binding | Q_surface_binding | -0.036 / A^(1/3) - 1.4e-4 * Z*(Z-1) / A^(4/3) | IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM | not derived from MTS parent action |

## DD Earth element charges
| charge_id | element | weighted_Q_alpha_Coulomb | weighted_Q_surface_binding | status |
| --- | --- | --- | --- | --- |
| DEC1083_Fe | Fe | 7.513635186631846e-04 | -3.154705944833544e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_O | O | 3.181167390262909e-04 | -4.306999645419867e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Si | Si | 2.646654125777605e-04 | -1.957587318063021e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Mg | Mg | 2.226381826491269e-04 | -1.957086881834798e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Ni | Ni | 4.651331247075188e-05 | -1.772884964446413e-04 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Ca | Ca | 3.653177850976983e-05 | -1.867800167629656e-04 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Al | Al | 2.363317307698712e-05 | -1.954069133756159e-04 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_S | S | 1.162891033225943e-05 | -7.474217822643107e-05 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Cr | Cr | 1.030804214870631e-05 | -4.727031818549037e-05 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Na | Na | 2.335495628295949e-06 | -2.324576427955864e-05 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_P | P | 1.165252668538896e-06 | -8.247308163554105e-06 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_Mn | Mn | 1.772188609241588e-06 | -7.908748408006081e-06 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_C | C | 5.886803899580859e-07 | -1.112621227420521e-05 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC1083_H | H | 0.000000000000000e+00 | -1.078645368575442e-05 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |

## DD Earth source vector first row
| source_vector_id | basis | Q_alpha_Coulomb_Earth | Q_surface_binding_Earth | status | claim_blocker |
| --- | --- | --- | --- | --- | --- |
| DD_EARTH1083_0_bulk_weighted | DD_Q_alpha_Coulomb_Q_surface_binding | 1.691260686750872e-03 | -1.211918219995745e-02 | NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM | bulk Earth source is not shell/profile/worldtube weighted and parent-to-DD/readout maps remain missing |

## DD source-material product nonclaim
| product_id | component | source_material_product | product_abs | eta_bound | status |
| --- | --- | --- | --- | --- | --- |
| DD_PRODUCT1083_0_alpha | Q_alpha_Coulomb | 3.365285544434638e-06 | 3.365285544434638e-06 | 2.800000000000000e-15 | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |
| DD_PRODUCT1083_1_surface | Q_surface_binding | -4.007154691040701e-05 | 4.007154691040701e-05 | 2.800000000000000e-15 | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |
| DD_PRODUCT1083_2_combined_abs | Q_alpha_Coulomb + Q_surface_binding | -3.670626136597237e-05 | 4.343683245484165e-05 | 2.800000000000000e-15 | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |

## Source vector caveat gate
| gate_id | claim_component | gate_pass | status | reason |
| --- | --- | --- | --- | --- |
| SCG1083_0_profile_weighting | Earth source profile/worldtube weighting | false | MISSING_SOURCE_PROFILE_WEIGHTING | bulk composition is not the same object as the orbit- and shell-weighted source vector seen by MICROSCOPE |
| SCG1083_1_parent_to_DD_map | C_parent -> DD coefficient map | false | MISSING_PARENT_OPERATOR_BASIS_MAP | alpha/surface DD basis remains external comparator not an MTS-derived basis |
| SCG1083_2_official_readout | K_MICROSCOPE official readout | false | OFFICIAL_ARRAYS_NOT_IMPORTED | gx/gz/Sxx/Sxz/masks/timing arrays or validated export are not yet in the product convention |
| SCG1083_3_no_measured_G_absorption | source response treatment | false | NO_ABSORPTION_SHORTCUT_ALLOWED | measured-G absorption would hide the finite WEP branch instead of deriving or bounding it |

## Common-mode alternative
| route_id | claim | status | gap |
| --- | --- | --- | --- |
| CMA1083_0_theorem_target | Earth source vector cancels as a universal common mode | THEOREM_TARGET_DEFINED | must be proven before replacing the explicit source vector |
| CMA1083_1_counterpressure | source vector may be ignored | NOT_SIGNED | finite WEP products generally contain source x test-material response unless parent action kills the source leg |
| CMA1083_2_verdict | common-mode route closes 1083 | SOURCE_COMMON_MODE_NOT_SIGNED | retain explicit source-vector acquisition route |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- |
| APR1083_0_DD_Earth_source_vector_product_stub | 0 | 1 | 1 | false | reject missing MTS coefficient map and official readout |

## Product comparison rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1083_0_source_vector | physical R_source^Earth | false | false | candidate is bulk-composition DD vector, not shell/profile/worldtube weighted |
| CG1083_1_parent_to_DD_map | MTS parent-to-DD coefficient map | false | false | PTD1082_4_verdict=PARENT_TO_DD_MAP_NOT_DERIVED |
| CG1083_2_official_readout | K_MICROSCOPE readout | false | false | official arrays/masks/timing not imported |
| CG1083_3_common_mode | source common-mode cancellation | false | false | CMA1083_2_verdict=SOURCE_COMMON_MODE_NOT_SIGNED |
| CG1083_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DECISION1083_0 | DD Earth source vector first row is numeric but nonclaim | bulk composition can be transformed into the external DD alpha/surface basis, but profile/readout/parent maps are missing | do not treat this as an MTS WEP prediction |
| DECISION1083_1 | explicit source-vector route remains open | common-mode theorem is not signed and measured-G absorption is forbidden | refine source profile weighting or import MICROSCOPE readout arrays before trying a physical product |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1083_0_local_sources_exist | pass | all cited local source paths and needles are present |
| V1083_1_web_sources_recorded | pass | web source urls/provenance are recorded as nonclaim |
| V1083_2_composition_target_numeric | pass | bulk Earth composition target rows are numeric and normalized |
| V1083_3_DD_formulas_present | pass | DD alpha/surface formulas are present |
| V1083_4_element_charges_numeric | pass | per-element DD charges are numeric |
| V1083_5_source_vector_numeric_nonclaim | pass | Earth DD source vector first row is numeric but nonclaim |
| V1083_6_products_numeric_nonclaim | pass | source-material products are numeric and nonclaim |
| V1083_7_caveats_block_claim | pass | profile/readout/parent/no-absorption caveats block claims |
| V1083_8_common_mode_unsigned | pass | common-mode alternative remains unsigned |
| V1083_9_prediction_missing_nonclaim | pass | generic prediction row remains missing parent/readout inputs |
| V1083_10_bound_numeric | pass | MICROSCOPE bound import is positive numeric |
| V1083_11_product_runner_refuses | pass | generic product runner reports no valid prediction rows and claim false |
| V1083_12_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1083_13_next_target | pass | 1084 handoff written |
| V1083_14_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1083_15_csv_parse | pass | all 1083 CSV outputs parse cleanly |
| V1083_16_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1083_SUMMARY | pass | DD Earth source vector first row built as numeric nonclaim; parent-to-DD/readout/profile gates remain closed |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1083_0_1084 | 1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md | choose whether to refine the DD Earth source vector with shell/profile/worldtube weighting or begin the official MICROSCOPE readout import gate; keep parent-to-DD map blocked and no MTS claim | Earth shell/profile targets; candidate weighting kernels; CMSM/readout array requirements; product convention; strict claim gates | unit source proxy as physical source; measured-G absorption; DD smoke as MTS claim; GitHub; formalization edits |

