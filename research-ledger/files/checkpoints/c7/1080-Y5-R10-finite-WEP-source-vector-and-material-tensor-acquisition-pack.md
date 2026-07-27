# 1080 - Finite WEP source-vector and material-tensor acquisition pack

## Current verdict
1080 turns the finite WEP route from a vague missing-input complaint into a source-anchored acquisition pack. MICROSCOPE gives the TA6V/PtRh10 composition context and readout model, Damour-Donoghue supplies an external phenomenological alpha/surface charge basis already used by the smoke rows, and McDonough-Sun identifies the Earth-composition reference. This is not a claim-ready MTS product: the same-basis objects C_parent, R_source^Earth, full R_TA6V - R_PtRh10, and K_MICROSCOPE are still missing or nonclaim.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1080_0_1079_next | source-intake/mts_residuals/P8_Y5_R10_1079_NEXT_TARGET.csv | true | true | 1079 handoff. |
| SRC1080_1_1079_validation | source-intake/mts_residuals/P8_Y5_BRR545_1079_VALIDATION.csv | true | true | 1079 validation summary. |
| SRC1080_2_1079_contract | source-intake/mts_residuals/P8_Y5_R10_1079_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv | true | true | finite WEP contract. |
| SRC1080_3_1079_vector | source-intake/mts_residuals/P8_Y5_R10_1079_FINITE_VECTOR_TEMPLATE_NONCLAIM.csv | true | true | finite vector template. |
| SRC1080_4_1079_material | source-intake/mts_residuals/P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv | true | true | material tensor contract. |
| SRC1080_5_1061_material_convention | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | true | MICROSCOPE material convention. |
| SRC1080_6_1053_charge_matrix | source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv | true | true | smoke composition charge matrix. |
| SRC1080_7_1052_projection | source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | true | true | WEP alpha/surface projection thresholds. |
| SRC1080_8_1075_tau_shape | source-intake/mts_residuals/P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv | true | true | surrogate readout status. |
| SRC1080_9_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Web/source candidate register
| web_source_id | role | source_url | extraction_status |
| --- | --- | --- | --- |
| WEB1080_0_MICROSCOPE_SF2A_2023 | MICROSCOPE test-mass composition and measurement model | https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | SOURCE_IDENTIFIED_AND_SUMMARIZED |
| WEB1080_1_DAMOUR_DONOGHUE_2010 | external phenomenological material-charge basis | https://arxiv.org/abs/1007.2792 | SOURCE_IDENTIFIED_FOR_PHENOMENOLOGICAL_BASIS_ONLY |
| WEB1080_2_MCDONOUGH_SUN_1995 | Earth/source composition reference candidate | https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/ | REFERENCE_IDENTIFIED_NOT_VECTORIZED |
| WEB1080_3_MICROSCOPE_RESULTS_2023 | official analysis/readout/data-portal context | https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf | SOURCE_IDENTIFIED_ARRAYS_NOT_IMPORTED |

## Material composition and tensor candidates
| material_id | object | mapped_basis | numeric_components | status | missing_for_claim |
| --- | --- | --- | --- | --- | --- |
| MAT1080_0_PtRh10_MICROSCOPE | PtRh10 | MICROSCOPE_COMPOSITION_CONTEXT_ONLY | composition_context_numeric | SOURCE_BACKED_COMPOSITION_CONTEXT | parent response basis and full material tensor |
| MAT1080_1_TA6V_MICROSCOPE | TA6V | MICROSCOPE_COMPOSITION_CONTEXT_ONLY | composition_context_numeric | SOURCE_BACKED_COMPOSITION_CONTEXT | parent response basis and full material tensor |
| MAT1080_2_delta_alpha_smoke | R_TA6V_minus_PtRh10 alpha/Coulomb smoke component | DD_ALPHA_COULOMB_EXTERNAL_PHENOMENOLOGICAL | Delta_Q_alpha_Coulomb=-1.989808886825e-03;abs=1.989808886825e-03 | SMOKE_NUMERIC_NOT_FULL_TENSOR | MTS parent basis; source vector; tau/readout; coefficient owner |
| MAT1080_3_delta_surface_smoke | R_TA6V_minus_PtRh10 surface/binding smoke component | DD_SURFACE_BINDING_EXTERNAL_PHENOMENOLOGICAL | Delta_Q_surface_binding=-3.306456347405e-03;abs=3.306456347405e-03 | SMOKE_NUMERIC_NOT_FULL_TENSOR | MTS parent basis; source vector; tau/readout; coefficient owner |
| MAT1080_4_full_tensor_upgrade | R_TA6V_minus_PtRh10 full material tensor | MISSING_MTS_PARENT_BASIS | MISSING_FULL_MATERIAL_TENSOR | MISSING_FOR_CLAIM | parent basis and full response map |

## Earth source-vector candidates
| source_vector_id | object | basis | status | missing_for_claim |
| --- | --- | --- | --- | --- |
| EARTH1080_0_source_role | R_source^Earth | observed MICROSCOPE source leg | SOURCE_ROLE_IDENTIFIED | composition/profile vector in the same parent basis as R_material and C_parent |
| EARTH1080_1_bulk_composition_reference | R_source^Earth | bulk Earth composition reference candidate | REFERENCE_IDENTIFIED_NOT_VECTORIZED | extract elemental/geophysical composition table and map to parent/source basis |
| EARTH1080_2_parent_basis_block | R_source^Earth | MISSING_MTS_PARENT_BASIS | MISSING_FOR_CLAIM | MTS must choose/derive the basis before Earth composition becomes a source vector |
| EARTH1080_3_common_mode_alternative | R_source^Earth common-mode theorem | THEOREM_ROUTE | THEOREM_ROUTE_NOT_SIGNED | parent theorem that source response is universal/common-mode without measured-G absorption |

## C_parent coefficient contract
| coefficient_id | object | candidate_basis | value | status | missing_for_claim |
| --- | --- | --- | --- | --- | --- |
| CP1080_0_definition | C_parent | MISSING_MTS_PARENT_BASIS | MISSING_PARENT_COEFFICIENT | MISSING_FOR_CLAIM | derive from parent action or explicitly source as finite phenomenological coefficient |
| CP1080_1_current_owner_partial | C_parent | current-owner subtheorem | NO_NUMERIC_COEFFICIENT_SUPPLIED | PARTIAL_THEOREM_NOT_COEFFICIENT | pre-variation action/species weights or finite coefficient still unresolved |
| CP1080_2_DD_basis_external | C_parent in Damour-Donoghue basis | DD_ALPHA_SURFACE_EXTERNAL | MISSING_DD_COEFFICIENT_VECTOR | PHENOMENOLOGICAL_BASIS_AVAILABLE_NONCLAIM | MTS-to-DD basis map and coefficient derivation |

## MICROSCOPE readout gate
| readout_id | object | status | missing_for_claim |
| --- | --- | --- | --- |
| READ1080_0_measurement_equation | K_MICROSCOPE readout model | MODEL_STRUCTURE_SOURCE_BACKED | official arrays/masks or validated reconstruction in the same product convention |
| READ1080_1_CMSM_portal | official CMSM data portal | OFFICIAL_PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED | download/import gx,gz,Sxx,Sxz/masks or user-assisted official export |
| READ1080_2_surrogate_matrix | surrogate K_MICROSCOPE | SURROGATE_AVAILABLE_NONCLAIM | official arrays and parent material/source map |
| READ1080_3_physical_tau | physical tau_WEP | NOT_ACQUIRED | official arrays plus C_parent/R_source/R_material product basis |

## Finite WEP input pack
| input_id | object | candidate_value | status | blocks_claim |
| --- | --- | --- | --- | --- |
| FIP1080_0_product_formula | P_WEP finite product | P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE | FORMULA_READY_NONCLAIM | all numeric input rows still required |
| FIP1080_1_C_parent | C_parent | MISSING_PARENT_COEFFICIENT | MISSING_FOR_CLAIM | no MTS coupling magnitude or basis owner |
| FIP1080_2_R_source | R_source^Earth | REFERENCE_IDENTIFIED_NOT_VECTORIZED | MISSING_FOR_CLAIM | no same-basis Earth source vector |
| FIP1080_3_R_material | R_TA6V - R_PtRh10 | DD smoke delta alpha/surface rows available; full tensor missing | PARTIAL_SMOKE_NUMERIC_NONCLAIM | external smoke basis not parent MTS basis; full tensor missing |
| FIP1080_4_K_readout | K_MICROSCOPE | surrogate available; official portal identified; arrays not imported | SURROGATE_ONLY_NONCLAIM | official arrays or validated reconstruction required |

## Nonclaim product candidate
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED1080_0_WEP_finite_input_pack_nonclaim | P_WEP_relative_source_weight | MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_NUMERIC_PRODUCT | ACQUISITION_PACK_READY_PRODUCT_MISSING | false |

## Bound import
| bound_id | product_symbol | bound_value | bound_units | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND1080_0_MICROSCOPE_WEP_source_charge | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | true |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR1080_0_WEP_finite_input_pack_product_stub | 0 | 1 | false | reject acquisition-pack rows until same-basis numeric product exists |

## Product comparison rows
| comparison_id | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1080_0_source_references | external source references | true | false | web/local source references are identified, but references are not same-basis MTS vectors |
| CG1080_1_material_context | MICROSCOPE material composition context | true | false | TA6V/PtRh10 compositions and smoke deltas are available, but full parent tensor is missing |
| CG1080_2_source_vector | R_source^Earth | false | false | Earth composition reference is not vectorized in MTS/DD basis |
| CG1080_3_C_parent | C_parent | false | false | parent coupling coefficient and basis owner are missing |
| CG1080_4_readout | K_MICROSCOPE | false | false | official arrays not imported; surrogate remains nonclaim |
| CG1080_5_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC1080_0_pack_value | finite WEP acquisition pack is now source-anchored but not score-ready | MICROSCOPE material/readout references, DD material charge basis, and Earth composition reference are named | do not claim; instantiate a basis only as a nonclaim smoke runner |
| DEC1080_1_main_blocker | main missing object is same-basis ownership | C_parent, R_source, R_material, and K_readout must share one basis/convention | either derive MTS parent basis or explicitly adopt DD basis as external nonclaim comparator |
| DEC1080_2_next_route | build a DD-basis finite WEP smoke runner as the next practical test scaffold | it can test pipeline algebra without pretending it is MTS-derived | 1081 should instantiate DD alpha/surface rows, source proxy policy, and runner refusal gates |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1080_0_sources_exist | pass | all cited local source paths and needles are present |
| V1080_1_web_sources_identified | pass | web source candidates are recorded with URLs |
| V1080_2_material_context | pass | MICROSCOPE material compositions are recorded |
| V1080_3_material_smoke_nonclaim | pass | material smoke rows remain nonclaim and full tensor is missing |
| V1080_4_earth_source_not_vectorized | pass | Earth/source reference is identified but not vectorized |
| V1080_5_C_parent_missing | pass | C_parent remains missing |
| V1080_6_readout_gate | pass | readout gate records official portal and surrogate nonclaim |
| V1080_7_input_pack_nonclaim | pass | finite input pack remains nonclaim |
| V1080_8_prediction_nonclaim_missing | pass | prediction row remains missing same-basis numeric product |
| V1080_9_bound_numeric | pass | bound import is positive numeric |
| V1080_10_runner_refuses | pass | runner reports no valid prediction rows and claim false |
| V1080_11_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1080_12_next_target | pass | 1081 handoff written |
| V1080_13_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1080_14_csv_parse | pass | all 1080 CSV outputs parse cleanly |
| V1080_15_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1080_SUMMARY | pass | finite WEP acquisition pack source-anchored; same-basis C_parent/R_source/R_material/K_readout still missing; claim blocked |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1080_0_1081 | 1081-Y5-R10-DD-basis-finite-WEP-smoke-runner-or-parent-basis-derivation.md | try to derive the MTS parent WEP basis; if it remains unsigned, instantiate a Damour-Donoghue alpha/surface finite-WEP smoke runner with explicit source-proxy policy and strict nonclaim gates. | MTS parent basis attempt; DD alpha/surface basis; Earth source proxy policy; TA6V/PtRh10 smoke deltas; MICROSCOPE readout gate; product runner refusal | MTS claim from DD basis; toy vector as evidence; measured-G absorption; tau=1; public claim; GitHub; formalization edits |

