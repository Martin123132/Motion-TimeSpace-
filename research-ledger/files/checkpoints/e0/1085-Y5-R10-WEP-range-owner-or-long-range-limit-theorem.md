# 1085-Y5-R10 WEP range owner or long-range limit theorem

## Current verdict
1085 does not prove the long-range shortcut. The exact range relation already exists, lambda_X=sqrt(Z_X/M_X^2), and 1084 proves that the bulk Earth source vector is safe only in the long-range limit. But the current parent stack still does not own Z_X, M_X^2, a zero-mass/no-pole theorem, a parent-to-DD map, or the official MICROSCOPE readout. So the honest result is: lambda_WEP is still a missing parent input, and finite-profile/readout/coupling gates remain live.

## Local source register
| source_id | relative_path | exists | needle_found | note |
| --- | --- | --- | --- | --- |
| SRC1085_0_1084_next | source-intake/mts_residuals/P8_Y5_R10_1084_NEXT_TARGET.csv | true | true | 1084 handoff. |
| SRC1085_1_1084_validation | source-intake/mts_residuals/P8_Y5_BRR545_1084_VALIDATION.csv | true | true | 1084 validation summary. |
| SRC1085_2_1084_kernel | source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv | true | true | source-profile kernel and long-range condition. |
| SRC1085_3_1084_profile_grid | source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv | true | true | lambda-dependent profile grid. |
| SRC1085_4_1084_profile_gates | source-intake/mts_residuals/P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv | true | true | bulk long-range gate. |
| SRC1085_5_1084_readout | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | true | true | official readout import gate. |
| SRC1085_6_1025_second_variation | source-intake/mts_residuals/P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv | true | true | lambda_X=sqrt(Z_X/M_X^2) relation. |
| SRC1085_7_1025_hessian_audit | source-intake/mts_residuals/P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv | true | true | parent Hessian ownership failed. |
| SRC1085_8_1026_metric_attempt | source-intake/mts_residuals/P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv | true | true | parent field-space metric missing. |
| SRC1085_9_1037_no_pole | source-intake/mts_residuals/P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv | true | true | no-pole route audit. |
| SRC1085_10_1038_omega | source-intake/mts_residuals/P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv | true | true | Omega/DCX no-pole certificate failed. |
| SRC1085_11_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | true | MICROSCOPE WEP bound row. |

## Web source register
| web_source_id | role | source_url | status |
| --- | --- | --- | --- |
| WEB1085_0_YUKAWA_PROFILE_KERNEL | finite-range profile-kernel reference inherited from 1084 | https://arxiv.org/pdf/2507.02723 | REFERENCE_ONLY_NONCLAIM |
| WEB1085_1_MICROSCOPE_FINAL_BOUND | WEP bound source | https://arxiv.org/abs/2209.15487 | BOUND_SOURCE_ONLY_PREDICTION_NONCLAIM |
| WEB1085_2_MICROSCOPE_ORBIT | Earth-source readout distance context | https://comptes-rendus.academie-sciences.fr/physique/item/10.5802/crphys.24.pdf | ORBIT_CONTEXT_ONLY_NONCLAIM |

## Range-owner theorem attempt
| attempt_id | branch | statement | result | missing_for_claim |
| --- | --- | --- | --- | --- |
| ROW1085_0_exact_range_relation | massive scalar-like residual | lambda_WEP = lambda_X = sqrt(Z_X/M_X^2) after canonicalizing O_X=-nabla_i(Z_X nabla^i)+M_X^2 | RELATION_DERIVED_VALUES_MISSING | same-branch Z_X, M_X^2, units, source current, and boundary/readout convention |
| ROW1085_1_no_pole_escape | no physical X pole / quotient branch | if X is pure quotient/gauge before variation, lambda_WEP is absent and finite source profile disappears | NO_POLE_NOT_CLOSED | parent Omega, DC_X, all-field v_X, Q_X/K_boundary, degree count, matter descent |
| ROW1085_2_massless_long_range | massless/common long-range carrier | M_X^2=0 or protected massless source carrier gives lambda_WEP=infinity and bulk source vector is profile-safe | LONG_RANGE_THEOREM_NOT_SIGNED | symmetry protecting zero mass plus source/readout normalization and no fifth-force contradiction |
| ROW1085_3_short_range_residual | finite short-range residual | finite lambda_WEP requires the 1084 profile kernel, orbit attenuation, PREM/shell profile, and official readout | FINITE_PROFILE_BRANCH_RETAINED | lambda_WEP owner, PREM/composition shell profile, official MICROSCOPE readout, parent-to-DD map |
| ROW1085_4_verdict | 1085 range owner | MTS currently proves lambda_WEP >> R_E or lambda_WEP=infinity | RANGE_OWNER_NOT_DERIVED | parent-owned range theorem or sourced finite-range profile/readout branch |

## Long-range thresholds
| threshold_id | lambda_over_R_E | lambda_m | equivalent_m_X_eV_if_relativistic | static_operator_condition | bulk_vector_status |
| --- | --- | --- | --- | --- | --- |
| LRT1085_lambda_over_RE_1 | 1 | 6.371000000000000e+06 | 3.097268566943965e-14 | M_X^2/Z_X <= 1/(1 R_E)^2 | profile_sensitive |
| LRT1085_lambda_over_RE_3 | 3 | 1.911300000000000e+07 | 1.032422855647988e-14 | M_X^2/Z_X <= 1/(3 R_E)^2 | profile_sensitive |
| LRT1085_lambda_over_RE_10 | 10 | 6.371000000000000e+07 | 3.097268566943965e-15 | M_X^2/Z_X <= 1/(10 R_E)^2 | bulk_limit_candidate_nonclaim |
| LRT1085_lambda_over_RE_30 | 30 | 1.911300000000000e+08 | 1.032422855647988e-15 | M_X^2/Z_X <= 1/(30 R_E)^2 | bulk_limit_candidate_nonclaim |
| LRT1085_lambda_over_RE_100 | 100 | 6.371000000000000e+08 | 3.097268566943965e-16 | M_X^2/Z_X <= 1/(100 R_E)^2 | bulk_limit_candidate_nonclaim |
| LRT1085_lambda_over_RE_1000 | 1000 | 6.371000000000000e+09 | 3.097268566943965e-17 | M_X^2/Z_X <= 1/(1000 R_E)^2 | bulk_limit_candidate_nonclaim |

## Profile influence readout
| influence_id | lambda_over_R_E | delta_alpha_vs_two_layer_long_range | delta_surface_vs_two_layer_long_range | max_abs_profile_shift | surface_orbit_attenuation_exp_minus_h_over_lambda | interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| INF1085_long_range_mass_average | inf | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 1.000000000000000e+00 | bulk_limit |
| INF1085_lambda_over_RE_100 | 1.000000000000000e+02 | -1.663447145002286e-09 | -5.726915969228585e-09 | 5.726915969228585e-09 | 9.988861960035464e-01 | bulk_limit |
| INF1085_lambda_over_RE_10 | 1.000000000000000e+01 | -1.657955794949657e-07 | -5.708010344593339e-07 | 5.708010344593339e-07 | 9.889176197198385e-01 | bulk_limit |
| INF1085_lambda_over_RE_1 | 1.000000000000000e+00 | -1.594431931044695e-05 | -5.489310380824008e-05 | 5.489310380824008e-05 | 8.945428496554392e-01 | finite_profile_live |
| INF1085_lambda_over_RE_0p3 | 3.000000000000000e-01 | -1.258825638609609e-04 | -4.333885010154599e-04 | 4.333885010154599e-04 | 6.897163089642564e-01 | finite_profile_live |
| INF1085_lambda_over_RE_0p1 | 1.000000000000000e-01 | -2.813237946043660e-04 | -9.685415827582790e-04 | 9.685415827582790e-04 | 3.281039706656655e-01 | finite_profile_live |
| INF1085_lambda_over_RE_0p03 | 3.000000000000000e-02 | -2.930560821756160e-04 | -1.008933503355019e-03 | 1.008933503355019e-03 | 2.436155208612123e-02 | finite_profile_live |

## R10-WEP consistency ledger
| consistency_id | claim | current_status | implication_if_true | required_evidence |
| --- | --- | --- | --- | --- |
| RWC1085_0_same_lambda_object | R10 lambda_X and WEP lambda_WEP are the same parent range | NOT_PARENT_SIGNED | short-range R10 candidates cannot simultaneously justify bulk Earth WEP source vector; long-range WEP candidates must face long-range fifth-force/WEP constraints | single parent kinetic/mass operator and arena projection showing the same lambda in both observables |
| RWC1085_1_independent_lambdas | R10 lambda and WEP lambda are independent | FORBIDDEN_UNLESS_PARENT_SPLITS_FIELDS | requires two distinct fields/operators, otherwise range choice is post hoc | field decomposition with separate Z/M blocks and separate source/readout maps |
| RWC1085_2_bulk_shortcut | use 1083 bulk Earth vector without lambda theorem | REJECTED | would hide the finite-range source-profile dependence found in 1084 | lambda_WEP >> R_E or source common-mode/no-pole theorem |
| RWC1085_3_r10_pressure | R10 bound curve can score this branch now | REJECTED | would require alpha(lambda), K_X(lambda), Qbar_XH(lambda), qbar_XT, and real bound curve in one convention | the 1033/1034/R10 projection stack plus parent range owner |

## Range acquisition schema
| schema_id | needed_object | current_status | claim_blocker |
| --- | --- | --- | --- |
| RAS1085_0_parent_operator | O_X=-nabla_i(Z_X nabla^i)+M_X^2 | MISSING_PARENT_HESSIAN_VALUES | lambda cannot be owned without same-branch Z_X and M_X^2 |
| RAS1085_1_long_range_certificate | lambda_WEP lower bound or zero-mass theorem | MISSING_LONG_RANGE_THEOREM | bulk Earth source vector remains conditional |
| RAS1085_2_finite_profile | finite lambda source-profile branch | MISSING_PREM_AND_LAMBDA_OWNER | 1084 two-layer grid is smoke only |
| RAS1085_3_readout_product | MICROSCOPE readout normalization | OFFICIAL_ARRAYS_NOT_IMPORTED | source profile alone is not a reported Eotvos prediction |
| RAS1085_4_parent_to_DD_map | C_parent -> (c_alpha,c_surface) | PARENT_TO_DD_MAP_NOT_DERIVED | DD source vector remains external comparator |

## Product runner status
| runner_id | valid_prediction_rows | valid_bound_rows | comparison_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- |
| APR1085_0_range_owner_product_stub | 0 | 1 | 1 | false | reject missing lambda_WEP range owner, parent-to-DD map, and official readout |

## Product comparison rows
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |

## Claim gates
| gate_id | claim_component | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG1085_0_range_owner | lambda_WEP owned | false | false | ROW1085_4_verdict=RANGE_OWNER_NOT_DERIVED |
| CG1085_1_bulk_vector | bulk Earth vector is physical source vector | false | false | requires lambda_WEP >> R_E, no-pole, or common-mode theorem |
| CG1085_2_R10_WEP_same_range | R10/WEP range consistency | false | false | same-lambda or split-field branch not parent-signed |
| CG1085_3_parent_to_DD_map | DD source vector is MTS source vector | false | false | parent-to-DD coefficient map remains missing |
| CG1085_4_product_runner | WEP product runner | false | false | valid_prediction_rows=0 |

## Decision ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DECISION1085_0 | long-range bulk shortcut is not available yet | lambda_WEP >> R_E is a theorem condition, not a data-fitting convenience, and current parent files only provide the lambda relation | attack parent source-current/coupling zero or fill the finite-profile/readout inputs |
| DECISION1085_1 | range and amplitude cannot be chosen independently | the same parent operator must own lambda_X, K_X, Qbar_XH, qbar_XT, and the DD coefficient map | return to the coupling/source-current owner before scoring WEP |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V1085_0_local_sources_exist | pass | all cited local source paths and needles are present |
| V1085_1_web_sources_recorded | pass | web source urls/provenance are recorded as nonclaim |
| V1085_2_range_theorem_attempt_complete | pass | range-owner attempt ends in explicit nonclaim verdict |
| V1085_3_thresholds_numeric | pass | lambda and mass-equivalent thresholds are numeric |
| V1085_4_profile_influence_numeric | pass | profile influence rows are numeric |
| V1085_5_R10_WEP_consistency_blocks_shortcuts | pass | R10/WEP lambda consistency shortcuts are blocked |
| V1085_6_acquisition_schema_nonclaim | pass | range/profile/readout acquisition schema remains nonclaim |
| V1085_7_prediction_missing_nonclaim | pass | generic prediction row remains missing range owner inputs |
| V1085_8_bound_numeric | pass | MICROSCOPE bound import is positive numeric |
| V1085_9_product_runner_refuses | pass | generic product runner reports no valid prediction rows and claim false |
| V1085_10_claim_gates_safe | pass | all claim gates deny WEP/local-GR claim |
| V1085_11_next_target | pass | 1086 handoff written |
| V1085_12_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work |
| V1085_13_csv_parse | pass | all 1085 CSV outputs parse cleanly |
| V1085_14_formalization_untouched | pass | formalization-workbench modified-file count remains zero |
| V1085_SUMMARY | pass | range-owner theorem not derived; bulk Earth shortcut remains conditional; finite profile/readout/coupling gates remain live |

## Next target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT1085_0_1086 | 1086-Y5-R10-WEP-source-current-zero-or-parent-DD-map-first-row.md | try the derivation-first route for WEP: prove the parent source/test composition current vanishes or map the first parent coefficient into the DD alpha/surface basis; if neither closes, retain finite-profile/readout acquisition | J_X/qbar_XT source-current zero attempt; C_parent to DD coefficient map; same-branch normalization; no-pole/common-mode alternatives; nonclaim fallback rows | measured-G absorption; fitted lambda choice; unit source proxy; DD smoke as MTS claim; GitHub; formalization edits |

