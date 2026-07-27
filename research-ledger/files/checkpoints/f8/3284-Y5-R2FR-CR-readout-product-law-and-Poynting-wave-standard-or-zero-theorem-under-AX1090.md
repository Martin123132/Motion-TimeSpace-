# 3284 - C_R readout product law and Poynting wave standard or zero theorem under AX1090

## Summary

3284 turns the readout branch into an exact algebraic object:

`R_alpha_readout = product_s R_s^{n_s}`

so

`C_R = L_v ln R_alpha_readout = sum_s n_s L_v ln R_s`.

This means `C_R=0` is not a wish. It follows if every readout factor is q-basic, or shift-protected, across the same parent public-readout functor. The factors are now named: clock/action standards, light-cone/rod standards, Hodge/impedance, Poynting flux, detector/material response, charge-calibration guard, and projection kernels.

The Poynting result is sharper than before: Poynting is allowed, but it has one legal home. It is either the public Maxwell stress flux `T_EM^{0i}`, or it is a separate named background residual in `E_res_munu`. It cannot be counted in both.

Pure readout bound inherited from the alpha row:

`|C_R| <= 1.389797711495e-12` if `C_J=0`, `C_Z=0`, and `C_R` is the only live alpha/readout slope.

## C_R Product Law Theorem
| theorem_id | claim_piece | proof_status | missing_for_claim |
| --- | --- | --- | --- |
| CRPL3284_0_definition | define C_R as the vertical readout multiplier | DEFINITION_PLUS_3273_DECOMPOSITION | C_J and C_Z zero/fixed routes are separate; R_alpha_readout must be parent-owned or finite-sourced. |
| CRPL3284_1_product_law | exact readout product law | EXACT_LOG_DERIVATIVE_THEOREM | the actual standard factors and exponents must be parent-declared before scoring. |
| CRPL3284_2_qbasic_zero_theorem | readout-zero route | EXACT_CONDITIONAL_ZERO_THEOREM | q-basic status for clocks/rods/action units, charge standards, Hodge/impedance, Poynting flux, and material detectors is unsigned. |
| CRPL3284_3_shift_zero_theorem | shift-protected readout route | EXACT_CONDITIONAL_WARD_THEOREM | the action/effective/readout Ward identity is not parent-signed. |
| CRPL3284_4_poynting_no_double_count | Poynting placement rule | ACCOUNTING_IDENTITY_AND_GUARD | parent must decide public Maxwell/Hodge branch versus independent background flux branch. |
| CRPL3284_5_current_verdict | C_R current status | NOT_PROMOTED_CURRENT_CORPUS | parent-owned readout functor or numeric source-backed factor slopes. |

## Readout Factor Ledger
| factor_id | readout_factor | slope_symbol | role | current_status |
| --- | --- | --- | --- | --- |
| CRFCT3284_0_phase_action_clock | R_phase_action_clock | C_phase := L_v ln R_phase_action_clock | clock/action/frequency unit used to make alpha dimensionless | CLOCK_DIRECT_PRODUCT_WAITSTATE |
| CRFCT3284_1_lightcone_rods | R_light_rods | C_light := L_v ln R_light_rods | speed-of-light/rod/time conversion from public coframe | SAME_PUBLIC_METRIC_UNSIGNED |
| CRFCT3284_2_hodge_impedance | R_Hodge_impedance | C_H := L_v ln R_Hodge_impedance | Hodge star/impedance standard converting field amplitudes to energy and spectra | CONSTITUTIVE_HODGE_ROUTE_OPEN |
| CRFCT3284_3_poynting_flux_standard | R_Poynting_flux | C_S := L_v ln R_Poynting_flux | EM energy-flux/radiation-pressure calibration from T_EM^{0i} | PLACEMENT_RULE_DERIVED_OWNER_UNSIGNED |
| CRFCT3284_4_material_detector | R_material_detector | C_mat := L_v ln R_material_detector | detector/material/spectroscopy response to alpha or EM stress | MATERIAL_TENSOR_MISSING |
| CRFCT3284_5_charge_calibration_guard | R_charge_standard | C_Qread := L_v ln R_charge_standard | charge/current calibration if it is not already the C_J owner | DO_NOT_DOUBLE_COUNT_WITH_CJ |
| CRFCT3284_6_instrument_projection | R_projection_kernel | C_inst := L_v ln R_projection_kernel | experiment/orbit/sampling/kernel conversion from physical residual to observable | KERNEL_AND_TAU_NOT_SCORE_READY |

## Poynting Standard Branch Table
| branch_id | branch | condition | C_R_effect | source_side_effect | blocked_by |
| --- | --- | --- | --- | --- | --- |
| POY3284_0_public_metric_Maxwell | public Maxwell stress | H=Z_Q *_{g_pub}F and Z_Q/readout factors are q-basic or parent-fixed | C_S=0; Poynting is T_EM^{0i} in the same public geometry | include T_EM in T_total once | Hodge/impedance/readout parent ownership unsigned |
| POY3284_1_constitutive_medium | background constitutive chi | chi is local, reciprocal, positive, nonbirefringent, nondispersive and reduces to metric Hodge | if chi is q-basic, C_H=C_S=0; otherwise finite EM-medium/readout slopes remain | derive public cone/Hodge but not EH operator | chi-to-Hodge theorem not parent-signed |
| POY3284_2_independent_background_flux | non-EM MTS background energy flow | flux is not the Maxwell Poynting vector and has its own stress/residual variable | not a readout rescue; it belongs in E_res_munu or a named residual stress | may source gravity only as explicit E_res/T_res component | needs separate field, stress, conservation and no-double-counting certificate |
| POY3284_3_forbidden_double_count | Poynting counted as both T_EM and hidden background flux | same EM energy flux used twice | invalid | forbidden by energy accounting | route rejected, not retained |

## First C_R Slope Rows
| row_id | case | C_R_prediction | C_R_abs_bound | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CRP3284_0_product_formula_ready_missing | general C_R product law | MISSING_NUMERIC_SUM_NS_CS | 1.389797711495e-12 | FORMULA_READY_NUMERIC_INPUTS_MISSING | false |
| CRP3284_1_qbasic_readout_zero_conditional | all readout factors q-basic | 0 | 1.389797711495e-12 | THEOREM_ZERO_CONDITIONAL_NONCLAIM | false |
| CRP3284_2_poynting_public_stress_conditional | Poynting is public T_EM flux | 0_if_public_Hodge_and_flux_standard_qbasic | 1.389797711495e-12 | THEOREM_ZERO_CONDITIONAL_NONCLAIM | false |
| CRP3284_3_constitutive_medium_symbolic | nonmetric constitutive or impedance readout | n_H*C_H + n_S*C_S + n_mat*C_mat + ... | 1.389797711495e-12 | SYMBOLIC_ONLY_NONCLAIM | false |
| CRP3284_4_clock_direct_product_waitstate | clock/spectroscopy alpha readout | MISSING_DIRECT_P_CLOCK_ALPHA_OR_FACTOR_SLOPES | 1.389797711495e-12 | REFUSE_OR_FAIL | false |
| CRP3284_5_half_bound_smoke | numeric smoke C_R inside pure-readout envelope | 6.948988557475e-13 | 1.389797711495e-12 | SMOKE | false |
| CRP3284_6_twice_bound_smoke | numeric smoke C_R outside pure-readout envelope | 2.779595422990e-12 | 1.389797711495e-12 | SMOKE | false |

## C_R Bound Runner
| row_id | C_R_prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CRP3284_0_product_formula_ready_missing | MISSING_NUMERIC_SUM_NS_CS | MISSING | REFUSE_OR_FAIL | true | false |
| CRP3284_1_qbasic_readout_zero_conditional | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| CRP3284_2_poynting_public_stress_conditional | 0_if_public_Hodge_and_flux_standard_qbasic | N/A | CONDITIONAL_NONNUMERIC_NONCLAIM | true | false |
| CRP3284_3_constitutive_medium_symbolic | n_H*C_H + n_S*C_S + n_mat*C_mat + ... | N/A | SYMBOLIC_NONNUMERIC_NONCLAIM | true | false |
| CRP3284_4_clock_direct_product_waitstate | MISSING_DIRECT_P_CLOCK_ALPHA_OR_FACTOR_SLOPES | MISSING | REFUSE_OR_FAIL | true | false |
| CRP3284_5_half_bound_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| CRP3284_6_twice_bound_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3284_0_product_law_derived | true | false | C_R=sum_s n_s L_v ln R_s is exact once readout factors are declared. |
| GATE3284_1_qbasic_zero_theorem | true | false | if every factor descends through q, C_R=0; parent ownership is unsigned. |
| GATE3284_2_poynting_placement_guard | true | false | Poynting is public T_EM flux or independent E_res flux, never both. |
| GATE3284_3_finite_CR_slope_sourced | false | false | no numeric source-backed C_R factor slopes are supplied in 3284. |
| GATE3284_4_no_empirical_shortcut | true | false | clock/MICROSCOPE/PPN bounds are not scored without a parent readout coefficient or zero theorem. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3284_0_product_law | C_R is now a factorized readout product, not a vague readout leak. | future work can attack a named factor slope or prove all factors q-basic. | false |
| DEC3284_1_poynting | Poynting is admitted as a serious route to public Hodge/stress, but not as double-counted hidden energy. | this keeps the user's Poynting intuition while enforcing conservation/accounting. | false |
| DEC3284_2_zero_route | The best zero route is a parent q-basic readout functor across clocks, charge standards, Hodge/impedance, Poynting flux, material response and kernels. | this is one proof target, not seven disconnected missing ledgers. | false |
| DEC3284_3_next_work | Next should try to prove the public readout functor theorem or source the first finite factor slope. | forces a derivation/source fork instead of data-only testing. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3284_0_3285 | 3285-Y5-R2FR-public-readout-functor-zero-proof-or-first-CR-factor-slope-under-AX1090.md | Try to prove one parent public-readout functor theorem: clocks/rods/action units, charge standards, Hodge/impedance, Poynting flux, material detector response, and projection kernels all factor through q; if that fails, source the first finite C_R factor slope row using the 3284 product law. | Do not score clock/MICROSCOPE/PPN data or claim C_R=0 unless the factor map is parent-owned; do not double-count Poynting as both T_EM and background E_res. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3284_0_sources_exist | all cited source paths exist | true |  |
| VAL3284_1_sources_parse | all cited source paths parse | true |  |
| VAL3284_2_outputs_parse | all 3284 non-validation output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3284_3_product_law_present | exact product law theorem row is present | true |  |
| VAL3284_4_factor_coverage | readout factors include clock Hodge Poynting material charge kernel | true |  |
| VAL3284_5_poynting_no_double_count | Poynting branch table includes forbidden double-count row | true |  |
| VAL3284_6_prediction_rows_nonclaim | all C_R prediction rows remain nonclaim | true |  |
| VAL3284_7_runner_expectations | C_R runner expectations all match | true | CRP3284_0_product_formula_ready_missing=REFUSE_OR_FAIL;CRP3284_1_qbasic_readout_zero_conditional=PASS_NUMERIC_NONCLAIM;CRP3284_2_poynting_public_stress_conditional=CONDITIONAL_NONNUMERIC_NONCLAIM;CRP3284_3_constitutive_medium_symbolic=SYMBOLIC_NONNUMERIC_NONCLAIM;CRP3284_4_clock_direct_product_waitstate=REFUSE_OR_FAIL;CRP3284_5_half_bound_smoke=PASS_NUMERIC_NONCLAIM;CRP3284_6_twice_bound_smoke=FAIL_BOUND |
| VAL3284_8_claim_gates_false | no 3284 gate allows local-GR/alpha/Maxwell claim | true |  |
| VAL3284_9_next_target_public_readout | next target is public readout functor or finite factor slope | true |  |
| VAL3284_10_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3284_11_overall | 3284 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T16:17:12.067516+00:00
