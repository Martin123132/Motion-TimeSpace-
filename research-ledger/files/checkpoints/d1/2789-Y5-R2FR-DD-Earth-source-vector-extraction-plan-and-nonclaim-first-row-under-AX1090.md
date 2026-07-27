# 2789 - DD Earth-source vector extraction plan and nonclaim first row under AX1090

## Private Verdict

2789 replaces the fake unit source proxy with a real first DD-basis bulk Earth/source vector row, but it is still strictly nonclaim. The row is useful: it gives numeric source-side alpha/Coulomb and surface/binding components and source-material product scales. It is not yet the physical MICROSCOPE source vector, because shell/profile/worldtube weighting, parent-to-DD coefficient map, source common-mode theorem, and official readout are still missing.

## Source Register
| row_id | source_key | exists | needle_found | source_role |
| --- | --- | --- | --- | --- |
| SRC2789_00_2788_next | 2788_next | True | True | current handoff into DD Earth-source vector extraction |
| SRC2789_01_2788_validation | 2788_validation | True | True | 2788 validation baseline |
| SRC2789_02_2788_earth_fill | 2788_earth_fill | True | True | Earth/source vector still not vectorized |
| SRC2789_03_2788_chain_rule | 2788_chain_rule | True | True | DD product projection contract |
| SRC2789_04_2788_dd_reuse | 2788_dd_reuse | True | True | DD material smoke reuse rows |
| SRC2789_05_1083_web | 1083_web | True | True | R10 web/source register precedent |
| SRC2789_06_1083_bulk | 1083_bulk | True | True | R10 bulk Earth composition candidate rows |
| SRC2789_07_1083_formulas | 1083_formulas | True | True | R10 DD charge formula ledger |
| SRC2789_08_1083_first_vector | 1083_first_vector | True | True | R10 first DD Earth-source vector |
| SRC2789_09_1083_product | 1083_product | True | True | R10 source-material product precedent |
| SRC2789_10_1083_common_mode | 1083_common_mode | True | True | R10 common-mode alternative |
| SRC2789_11_1083_next | 1083_next | True | True | R10 next target after first source vector |
| SRC2789_12_1084_next | 1084_next | True | True | R10 source-profile/range/readout route |
| SRC2789_13_local_bounds | local_bounds | True | True | MICROSCOPE WEP bound row |

## Web/Source Register
| web_source_id | role | source_url | extraction_method | confidence_level |
| --- | --- | --- | --- | --- |
| WEB2789_0_MCDONOUGH_2003_TABLE5 | bulk Earth composition table target | https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf | manual table-target transcription into candidate rows; not a machine-readable official table import | medium_for_nonclaim_source_vector; insufficient_for_claim |
| WEB2789_1_MCDONOUGH_SUN_1995 | composition provenance continuity | https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/ | provenance link only; no new numeric extraction from this page | source-continuity-only |
| WEB2789_2_DAMOUR_DONOGHUE_2010 | external DD alpha/surface charge basis | https://arxiv.org/abs/1007.2792 | reuse existing local smoke convention rather than promote the external basis to MTS | good_for_external_comparator; not_MTS_derived |
| WEB2789_3_MICROSCOPE_FINAL | WEP bound source | https://arxiv.org/abs/2209.15487 | bound import only; official readout arrays still not imported | bound_source_backed; prediction_nonclaim |

## Bulk Earth Composition Target
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

## DD Charge Formula Ledger
| formula_id | component | formula | status | claim_blocker |
| --- | --- | --- | --- | --- |
| DDF2789_0_alpha_Coulomb | Q_alpha_Coulomb | 7.7e-4 * Z*(Z-1) / A^(4/3) | IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM | not derived from MTS parent action |
| DDF2789_1_surface_binding | Q_surface_binding | -0.036 / A^(1/3) - 1.4e-4 * Z*(Z-1) / A^(4/3) | IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM | not derived from MTS parent action |

## DD Earth Element Charges
| charge_id | element | normalized_mass_fraction | Q_alpha_Coulomb | Q_surface_binding | status |
| --- | --- | --- | --- | --- | --- |
| DEC2789_Fe | Fe | 3.204486280793110e-01 | 2.344723780428300e-03 | -9.844654239096180e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_O | O | 2.974163829361106e-01 | 1.069600591217690e-03 | -1.448137995258006e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Si | Si | 1.612257160024034e-01 | 1.641583111802184e-03 | -1.214190494296728e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Mg | Mg | 1.542159022631684e-01 | 1.443678501255962e-03 | -1.269056467662487e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Ni | Ni | 1.822551572201082e-02 | 2.552098562268836e-03 | -9.727488601627405e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Ca | Ca | 1.712397356298818e-02 | 2.133370410517903e-03 | -1.090751606663728e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Al | Al | 1.592229120769077e-02 | 1.484282178281719e-03 | -1.227253733942705e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_S | S | 6.408972561586221e-03 | 1.814473415280355e-03 | -1.166211549639282e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Cr | Cr | 4.706589224914881e-03 | 2.190129976531516e-03 | -1.004343398724057e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Na | Na | 1.802523532946125e-03 | 1.295681074675742e-03 | -1.289623344975959e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_P | P | 7.009813739234929e-04 | 1.662316164004202e-03 | -1.176537418875018e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_Mn | Mn | 8.011215701982776e-04 | 2.212134431485813e-03 | -9.872095200293592e-03 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_C | C | 7.009813739234929e-04 | 8.397946248744923e-04 | -1.587233653860189e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |
| DEC2789_H | H | 3.004205888243541e-04 | 0.000000000000000e+00 | -3.590450883531453e-02 | NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM |

## DD Earth Source Vector First Row
| source_vector_id | source_body | basis | Q_alpha_Coulomb_Earth | Q_surface_binding_Earth | status | claim_blocker |
| --- | --- | --- | --- | --- | --- | --- |
| DD_EARTH2789_0_bulk_weighted | Earth | DD_Q_alpha_Coulomb_Q_surface_binding | 1.691260686750872e-03 | -1.211918219995745e-02 | NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM | bulk Earth source is not shell/profile/worldtube weighted and parent-to-DD/readout maps remain missing |

## DD Source-Material Product
| product_id | component | source_material_product | product_abs | required_abs_coefficient_max_if_single_component | required_abs_coefficient_max_if_equal_component | status |
| --- | --- | --- | --- | --- | --- | --- |
| DD_PRODUCT2789_0_alpha | Q_alpha_Coulomb | 3.365285544434638e-06 | 3.365285544434638e-06 | 8.320244933243532e-10 |  | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |
| DD_PRODUCT2789_1_surface | Q_surface_binding | -4.007154691040701e-05 | 4.007154691040701e-05 | 6.987501646143863e-11 |  | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |
| DD_PRODUCT2789_2_combined_abs | Q_alpha_Coulomb + Q_surface_binding | -3.670626136597237e-05 | 4.343683245484165e-05 |  | 6.446142229433907e-11 | NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM |

## Source Vector Caveat Gates
| gate_id | claim_component | gate_pass | status | reason |
| --- | --- | --- | --- | --- |
| SCG2789_0_profile_weighting | Earth source profile/worldtube weighting | False | MISSING_SOURCE_PROFILE_WEIGHTING | bulk composition is not the same object as the orbit- and shell-weighted source vector seen by MICROSCOPE |
| SCG2789_1_parent_to_DD_map | C_parent -> DD coefficient map | False | MISSING_PARENT_OPERATOR_BASIS_MAP | alpha/surface DD basis remains external comparator not an MTS-derived basis |
| SCG2789_2_official_readout | K_MICROSCOPE official readout | False | OFFICIAL_ARRAYS_NOT_IMPORTED | gx/gz/Sxx/Sxz/masks/timing arrays or validated export are not yet in the product convention |
| SCG2789_3_no_measured_G_absorption | source response treatment | False | NO_ABSORPTION_SHORTCUT_ALLOWED | measured-G absorption would hide the finite WEP branch instead of deriving or bounding it |

## Common-Mode Alternative
| route_id | claim | status | gap |
| --- | --- | --- | --- |
| CMA2789_0_theorem_target | Earth source vector cancels as a universal common mode | THEOREM_TARGET_DEFINED | must be proven before replacing the explicit source vector |
| CMA2789_1_counterpressure | source vector may be ignored | NOT_SIGNED | finite WEP products generally contain source x test-material response unless parent action kills the source leg |
| CMA2789_2_verdict | common-mode route closes 2789 | SOURCE_COMMON_MODE_NOT_SIGNED | retain explicit source-vector acquisition route |

## Product Stub And Bound
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED2789_0_DD_bulk_Earth_source_not_MTS_product | P_WEP_relative_source_weight | MISSING_PARENT_TO_DD_MAP_OR_PROFILE_READOUT_NORMALIZATION | BULK_EARTH_DD_SOURCE_NUMERIC_BUT_MTS_PRODUCT_MISSING | False |

| bound_id | observable | upper_bound | units | valid_bound_row |
| --- | --- | --- | --- | --- |
| BOUND2789_0_MICROSCOPE_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | True |

| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR2789_0_DD_bulk_Earth_source_product_stub | 0 | 1 | False | reject DD bulk Earth source row as MTS product |

## Claim Gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2789_0_source_vector | physical R_source^Earth | False | False | candidate is bulk-composition DD vector, not shell/profile/worldtube weighted |
| CG2789_1_parent_to_DD_map | MTS parent-to-DD coefficient map | False | False | PTD2788_6_verdict=PARENT_TO_DD_MAP_NOT_DERIVED_BUT_CONDITIONAL_CHAIN_RULE_WRITTEN |
| CG2789_2_official_readout | K_MICROSCOPE readout | False | False | official arrays/masks/timing not imported |
| CG2789_3_common_mode | source common-mode cancellation | False | False | CMA2789_2_verdict=SOURCE_COMMON_MODE_NOT_SIGNED |
| CG2789_4_product_runner | WEP product runner | False | False | valid_prediction_rows=0 |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DECISION2789_0 | DD Earth source vector first row is numeric but nonclaim | bulk composition can be transformed into the external DD alpha/surface basis, but profile/readout/parent maps are missing | do not treat this as an MTS WEP prediction |
| DECISION2789_1 | explicit source-vector route remains open | common-mode theorem is not signed and measured-G absorption is forbidden | refine source profile weighting or import MICROSCOPE readout arrays before trying a physical product |
| DECISION2789_2 | range/profile question is now unavoidable | bulk Earth vector assumes the relevant carrier samples the whole Earth coherently | 2790 should choose profile weighting/readout import or derive long-range source condition |

## Validation
| validation_id | passed | detail |
| --- | --- | --- |
| VAL2789_0_sources | True | every cited source path exists and source needle was found |
| VAL2789_1_web_sources_recorded | True | web/source candidates are recorded |
| VAL2789_2_bulk_mass_normalized | True | bulk Earth mass fractions normalize to one |
| VAL2789_3_formula_rows | True | DD charge formula rows are present |
| VAL2789_4_element_charges_numeric | True | element DD charges are numeric |
| VAL2789_5_source_vector_numeric_nonclaim | True | bulk Earth source vector is numeric but nonclaim |
| VAL2789_6_source_product_numeric_nonclaim | True | source-material products are numeric but nonclaim |
| VAL2789_7_caveat_gates_block | True | source-vector caveat gates block claims |
| VAL2789_8_common_mode_not_signed | True | common-mode route remains unsigned |
| VAL2789_9_prediction_nonclaim_missing | True | prediction row remains missing parent/profile/readout inputs |
| VAL2789_10_bound_numeric | True | bound import is positive numeric |
| VAL2789_11_runner_refuses | True | generic product runner refuses DD source row as MTS product |
| VAL2789_12_claim_gates_safe | True | all claim gates deny WEP/local-GR claim |
| VAL2789_13_next_target | True | 2790 handoff written |
| VAL2789_14_branch_outputs | True | branch copies exist and contain rows |
| VAL2789_15_csv_parse | True | all generated CSV outputs parse cleanly |
| VAL2789_16_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true |
| VAL2789_17_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work |
| VAL2789_18_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run |
| VAL2789_19_pycache_absent | True | scripts __pycache__ absent at validation write |
| VAL2789_OVERALL | True | 2789 constructs the first numeric DD-basis bulk Earth/source vector and source-material products as nonclaim rows. The scaffold improves empirical plumbing, but parent-to-DD map, source profile/worldtube weighting, common-mode theorem, and official readout remain blocking gates. |

## Next Target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2789_0_2790 | 2790-Y5-R2FR-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate-under-AX1090.md | choose whether to refine the DD Earth source vector with shell/profile/worldtube weighting or begin the official MICROSCOPE readout import gate; keep parent-to-DD map blocked and no MTS claim | Earth shell/profile targets; candidate weighting kernels; CMSM/readout array requirements; product convention; strict claim gates | unit source proxy as physical source; measured-G absorption; DD profile smoke as MTS claim; GitHub; formalization edits |
