# 1084-Y5-R10 DD source-profile weighting or MICROSCOPE readout import gate

## Current verdict
1084 gets a real derivation step: for a finite-range spherical source, the Earth source vector is not automatically the bulk vector; it is a radial-kernel weighted charge vector. The bulk source vector is recovered only in the long-range limit lambda_WEP >> R_E. Since MTS has not yet derived lambda_WEP, the parent-to-DD map, or the official MICROSCOPE readout normalization, the branch remains nonclaim.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1084_0_1083_next | source-intake/mts_residuals/P8_Y5_R10_1083_NEXT_TARGET.csv | true | true | 1083 handoff. |
| SRC1084_1_1083_validation | source-intake/mts_residuals/P8_Y5_BRR545_1083_VALIDATION.csv | true | true | 1083 validation summary. |
| SRC1084_2_1083_source_vector | source-intake/mts_residuals/P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv | true | true | bulk DD source vector candidate. |
| SRC1084_3_1083_products | source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv | true | true | source-material product nonclaim rows. |
| SRC1084_4_1083_caveats | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | true | true | profile gate from 1083. |
| SRC1084_5_1083_common_mode | source-intake/mts_residuals/P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv | true | true | common-mode theorem remains unsigned. |
| SRC1084_6_1082_readout | source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv | true | true | readout arrays missing. |
| SRC1084_7_1081_delta | source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv | true | true | test-material deltas. |
| SRC1084_8_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Web source register
| web_source_id | role | source_url | extraction_status |
| --- | --- | --- | --- |
| WEB1084_0_PREM_IRIS | density/radius profile source for future weighting | https://ds.iris.edu/spud/earthmodel/10131390 | SOURCE_IDENTIFIED_NOT_IMPORTED |
| WEB1084_1_YUKAWA_NONHOMOGENEOUS_SPHERE | finite-range shell-weighting kernel reference | https://arxiv.org/pdf/2507.02723 | FORMULA_REFERENCE_ONLY_NONCLAIM |
| WEB1084_2_MCDONOUGH_2003_TABLE5 | core/mantle/bulk composition table target | https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf | MANUAL_TABLE_TARGET_CANDIDATE_NONCLAIM |
| WEB1084_3_MICROSCOPE_ORBIT | orbit/readout context | https://comptes-rendus.academie-sciences.fr/physique/item/10.5802/crphys.24.pdf | ORBIT_CONTEXT_ONLY_NONCLAIM |

## Kernel derivation ledger
| kernel_id | claim | formula_or_condition | status | claim_blocker |
| --- | --- | --- | --- | --- |
| K1084_0_angular_integral | external finite-range spherical source reduces to a radial kernel | for r>R, angular integral gives common exp(-r/lambda)/r factor times int rho(r') q(r') r'^2 sinh(r'/lambda)/(r'/lambda) dr' | DERIVED_AS_KERNEL_CONTRACT | kernel is external DD/Yukawa profile algebra, not yet MTS parent-derived |
| K1084_1_effective_source_charge | profile-weighted source charge can be defined | Q_eff(lambda)=int rho q W_lambda dr / int rho W_lambda dr, W_lambda=4*pi*r^2*sinh(r/lambda)/(r/lambda) | DERIVED_AS_NONCLAIM_PROFILE_RULE | requires lambda owner and sourced rho(r), q(r) |
| K1084_2_long_range_limit | bulk source vector is recovered in the long-range limit | lambda >> R_E makes sinh(r/lambda)/(r/lambda)=1+O(R_E^2/lambda^2), so Q_eff tends the mass-weighted source average | LONG_RANGE_LIMIT_CONDITIONALLY_DERIVED | MTS has not derived that the WEP carrier range is long compared with Earth radius |
| K1084_3_finite_range_profile_dependency | finite-range branch is surface/profile sensitive | as lambda decreases, W_lambda favors larger r and the effective source vector tends the near-surface layer composition | FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED | no PREM/compositional shell vector and no MTS lambda_WEP selection |
| K1084_4_orbit_factor | 710 km orbit is a common first-pass amplitude factor for a spherical source | outside-source r=R_E+h appears in the common exp(-r/lambda)/r and force derivative factor, not in Q_eff(lambda), under spherical symmetry | READOUT_AMPLITUDE_SEPARATED_NONCLAIM | actual MICROSCOPE readout uses time-dependent gx/gz/Sxx/Sxz/masks not imported here |

## Core/mantle composition candidate
| layer_id | layer | element | wt_percent | normalized_layer_mass_fraction | extraction_status |
| --- | --- | --- | --- | --- | --- |
| LAYER1084_mantle_Fe | mantle | Fe | 6.26 | 6.295886553354117e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_O | mantle | O | 44 | 4.425223775520467e-01 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Si | mantle | Si | 21 | 2.112038620134768e-01 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Mg | mantle | Mg | 22.8 | 2.293070501860605e-01 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Ni | mantle | Ni | 0.2 | 2.011465352509303e-03 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Ca | mantle | Ca | 2.53 | 2.544503670924268e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Al | mantle | Al | 2.35 | 2.363471789198431e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_S | mantle | S | 0.03 | 3.017198028763954e-04 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_mantle_Cr | mantle | Cr | 0.26 | 2.614904958262094e-03 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Fe | core | Fe | 85.5 | 8.592964824120602e-01 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_O | core | O | 0 | 0.000000000000000e+00 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Si | core | Si | 6 | 6.030150753768844e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Mg | core | Mg | 0 | 0.000000000000000e+00 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Ni | core | Ni | 5.2 | 5.226130653266332e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Ca | core | Ca | 0 | 0.000000000000000e+00 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Al | core | Al | 0 | 0.000000000000000e+00 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_S | core | S | 1.9 | 1.909547738693467e-02 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |
| LAYER1084_core_Cr | core | Cr | 0.9 | 9.045226130653266e-03 | TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM |

## Core/mantle DD charge vectors
| layer_charge_id | layer | mass_fraction_candidate | Q_alpha_Coulomb_layer | Q_surface_binding_layer | status |
| --- | --- | --- | --- | --- | --- |
| LC1084_mantle | mantle | 6.751640585562846e-01 | 1.399469878526843e-03 | -1.311954404402867e-02 | NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM |
| LC1084_core | core | 3.248359414437154e-01 | 2.301637295368259e-03 | -1.001356198854927e-02 | NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM |

## Source-profile weighting grid
| profile_row_id | lambda_over_R_E | Q_alpha_Coulomb_eff | Q_surface_binding_eff | delta_alpha_vs_1083_bulk | delta_surface_vs_1083_bulk | status |
| --- | --- | --- | --- | --- | --- | --- |
| PROFILE1084_long_range_mass_average | inf | 1.692526280716369e-03 | -1.211060943892973e-02 | 1.265593965497089e-06 | 8.572761027716633e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_100 | 1.000000000000000e+02 | 1.692524617269224e-03 | -1.211061516584570e-02 | 1.263930518351653e-06 | 8.567034111752608e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_10 | 1.000000000000000e+01 | 1.692360485136874e-03 | -1.211118023996419e-02 | 1.099798386001473e-06 | 8.001959993257299e-06 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_1 | 1.000000000000000e+00 | 1.676581961405922e-03 | -1.216550254273797e-02 | -1.467872534494964e-05 | -4.632034278051825e-05 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_0p3 | 3.000000000000000e-01 | 1.566643716855408e-03 | -1.254399793994519e-02 | -1.246169698954644e-04 | -4.248157399877363e-04 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_0p1 | 1.000000000000000e-01 | 1.411202486112003e-03 | -1.307915102168801e-02 | -2.800582006388687e-04 | -9.599688217305606e-04 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |
| PROFILE1084_lambda_over_RE_0p03 | 3.000000000000000e-02 | 1.399470198540753e-03 | -1.311954294228475e-02 | -2.917904882101187e-04 | -1.000360742327303e-03 | NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM |

## Profile closure gates
| gate_id | claim_component | gate_pass | condition | current_status |
| --- | --- | --- | --- | --- |
| PCG1084_0_long_range_bulk_limit | bulk source vector suffices | conditional | derive lambda_WEP >> R_E or massless/common long-range source carrier from parent action | CONDITION_NOT_PARENT_SIGNED |
| PCG1084_1_finite_range_profile | finite-range source profile vector | false | import PREM density plus shell composition profile and choose lambda_WEP | MISSING_PREM_IMPORT_AND_LAMBDA_OWNER |
| PCG1084_2_source_charge_basis | DD profile vector is an MTS source vector | false | derive parent-to-DD coefficient/source basis map | PARENT_TO_DD_MAP_NOT_DERIVED |

## MICROSCOPE readout import gate
| readout_id | needed_object | required_content | current_status | claim_blocker |
| --- | --- | --- | --- | --- |
| RIG1084_0_CMSM_arrays | official MICROSCOPE CMSM/export arrays | time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention | OFFICIAL_ARRAYS_NOT_IMPORTED | unit or surrogate readout cannot become physical tau_WEP |
| RIG1084_1_product_convention | eta_AB product normalization | map from source response x material response x readout kernel to reported Eotvos eta | NORMALIZATION_NOT_FILLED | numeric profile products are scale probes only |
| RIG1084_2_surrogate_limit | surrogate design matrix relation to official readout | proof surrogate kernel has same units/normalization as official arrays | SURROGATE_AVAILABLE_NONCLAIM | cannot replace official readout for a WEP claim |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- |
| APR1084_0_profile_weighted_product_stub | 0 | 1 | 1 | false | reject missing lambda_WEP, parent-to-DD map, and official readout |

## Product comparison rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1084_0_profile_rule | source-profile rule | conditional | false | radial kernel rule derived as external DD/Yukawa algebra, but physical source needs lambda/profile |
| CG1084_1_long_range_bulk | bulk source vector suffices | conditional | false | requires parent-signed lambda_WEP >> R_E or massless common carrier |
| CG1084_2_parent_to_DD | MTS parent-to-DD map | false | false | still not derived |
| CG1084_3_readout | MICROSCOPE official readout | false | false | CMSM/export arrays and eta normalization not imported |
| CG1084_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DECISION1084_0 | source-profile algebra is now explicit | finite-range spherical source weighting reduces to a hyperbolic radial kernel and has a clean long-range bulk limit | derive lambda_WEP from parent action before using either bulk or finite-range profile rows as physical |
| DECISION1084_1 | MICROSCOPE readout import remains a separate hard gate | 710 km orbit and spherical source profile do not substitute for gx/gz/Sxx/Sxz/masks/timing/product normalization | either acquire official arrays or continue parent-side derivation of the coefficient/range owner |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1084_0_local_sources_exist | pass | all cited local source paths and needles are present |
| V1084_1_web_sources_recorded | pass | web source urls/provenance are recorded as nonclaim |
| V1084_2_kernel_contract | pass | profile kernel and long-range/finite-range rules are explicit |
| V1084_3_layer_composition_numeric | pass | core/mantle composition candidate rows are numeric |
| V1084_4_layer_charges_numeric | pass | core/mantle DD charges are numeric |
| V1084_5_profile_grid_numeric_nonclaim | pass | profile weighting grid is numeric and nonclaim |
| V1084_6_profile_gates_block_claim | pass | profile closure gates retain lambda/profile/parent blockers |
| V1084_7_readout_gate_blocks_claim | pass | readout import gates remain nonclaim |
| V1084_8_prediction_missing_nonclaim | pass | generic prediction row remains missing lambda/parent/readout inputs |
| V1084_9_bound_numeric | pass | MICROSCOPE bound import is positive numeric |
| V1084_10_product_runner_refuses | pass | generic product runner reports no valid prediction rows and claim false |
| V1084_11_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1084_12_next_target | pass | 1085 handoff written |
| V1084_13_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1084_14_csv_parse | pass | all 1084 CSV outputs parse cleanly |
| V1084_15_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1084_SUMMARY | pass | finite-range source-profile kernel derived as nonclaim; long-range bulk limit conditional; lambda/readout/parent gates remain closed |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1084_0_1085 | 1085-Y5-R10-WEP-range-owner-or-long-range-limit-theorem.md | derive whether the local WEP carrier/source response is long range enough for the bulk Earth vector, or retain lambda-dependent profile rows and route to PREM/readout import; do not claim WEP/local-GR | parent mass/range operator; lambda_WEP >> R_E condition; relation to R10 lambda; parent-to-DD coefficient pressure point; readout import fallback | measured-G absorption; unit source proxy; DD profile smoke as MTS claim; GitHub; formalization edits |

