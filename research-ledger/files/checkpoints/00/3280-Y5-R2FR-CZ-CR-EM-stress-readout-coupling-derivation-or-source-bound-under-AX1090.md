# 3280 - C_Z/C_R EM stress-readout coupling derivation or source-bound gate under AX1090

## Summary

3280 moves the coupling work off the now-demoted finite `C_J` branch and attacks the EM side directly. The result is not a public Maxwell/alpha/local-GR claim. It is a sharper derivation gate:

`Poynting/wave/F_Q-only response lives in EM stress, constitutive boundary terms, and readout transfer. It does not secretly fix source-current normalization.`

The useful object is now

`q_EM^nu = P_loc[Q_Z^nu + nabla_mu T_readout^{mu nu} + boundary/no-flux leakage]`,

where `Q_Z^nu` is the stress-exchange term produced when `Z_Q` is not parent-fixed. Therefore local GR/Newton/Maxwell recovery needs either `q_EM^nu=0` by parent theorem or finite source-bound rows for `C_Z/C_R`.

## EM Stress / Readout Derivation
| derivation_id | object | formula | result | status |
| --- | --- | --- | --- | --- |
| DER3280_0_starting_block | EM kinetic/source/readout block | S_EM=int mu_obs[-Z_Q F_Q^2/4 + s_J kappa_J A_Q_mu J_Q^mu] + S_readout[g_obs,*_obs,hbar,c,...] | C_Z and C_R are now the live alpha/source-coupling slopes, not hidden C_J compensators. | STARTING_BLOCK_FIXED |
| DER3280_1_EM_stress | Hilbert EM stress | T_EM^{mu nu}=Z_Q(F_Q^{mu rho}F_Q^nu_rho - 1/4 g_obs^{mu nu}F_Q^2) + constitutive/readout boundary terms | Poynting/wave energy is proportional to Z_Q in the observed coframe. | EXACT_FROM_ASSUMED_BLOCK |
| DER3280_2_Z_exchange | Maxwell stress exchange residual | nabla_mu T_EM^{mu nu}=s_J kappa_J F_Q^nu_mu J_Q^mu + Q_Z^nu, with Q_Z^nu ~ -(1/4)F_Q^2 nabla^nu Z_Q plus owner/boundary terms | A floating Z_Q becomes a real stress-exchange residual, not a current-normalization escape hatch. | POYNTING_DIAGNOSTIC_THEOREM |
| DER3280_3_observer_Poynting | observer-frame energy flow | u_EM=Z_Q(E^2+B^2)/2; S_EM^i=Z_Q(E x B)^i; partial_t u_EM+div S_EM=-s_J kappa_J E.J + Z_Q/readout-gradient exchange | The user's Poynting/background-field intuition is placed in C_Z/C_R stress/readout, not discarded. | FLOW_ROUTE_MAPPED |
| DER3280_4_readout_slope | dimensionless alpha/readout transfer | alpha_obs proportional to kappa_J^2/(Z_Q R_alpha); C_e=2C_J-C_Z-C_R, C_R=L_X ln R_alpha | Readout/Hodge/coframe/hbar*c leakage is independent debt unless quotient-fixed. | READOUT_CONTRACT_EXPLICIT |
| DER3280_5_qEM_residual | local residual vector | q_EM^nu=P_loc[Q_Z^nu + nabla_mu T_readout^{mu nu} + boundary/no-flux leakage] | Local GR/Newton/Maxwell recovery requires q_EM^nu=0 by parent theorem or a sourced finite bound. | LOCAL_RESIDUAL_GATE_BUILT |

## C_Z / C_R Owner Gate
| gate_id | coefficient | current_status | blocking_evidence | result_if_signed |
| --- | --- | --- | --- | --- |
| CZCR3280_0_unique_Z_owner | C_Z=L_X ln Z_Q | NOT_SIGNED | 1099/1100 retain fixed-gauge-norm and no-extra-F2 debt. | C_Z=0 at tree level |
| CZCR3280_1_no_extra_F2 | C_Z residual | COUNTERTERM_RETAINED | 1099 EXC rows say diffeomorphism and U1 gauge invariance do not forbid f_X F_Q^2. | hidden-visible gauge kinetic leak removed |
| CZCR3280_2_F_only_response | stress/readout residual, not C_J | SOURCE_BACKED_PLACEMENT | 3276/3278 prove magnetization current is identically conserved and belongs in stress/Poynting residuals. | prevents smuggling F-only physics into source-current normalization |
| CZCR3280_3_readout_owner | C_R=L_X ln R_alpha | UNSIGNED | 3273, 1099, and 1100 all retain readout/radiative closure as unsigned. | C_R=0 |
| CZCR3280_4_CJ_not_reopened | C_J | DEMOTED_TO_CLOSURE_ONLY | 3279 closure demotion. | C_Z/C_R are attacked directly without hidden C_J cancellation |

## Source-Bound Rows
| row_id | C_Z | C_R | C_J | C_e_prediction | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ZRB3280_0_CZ_zero_if_unique_owner_signed | 0 | MISSING_READOUT_OR_ZERO_THEOREM | 0_if_parent_exact_U1_current_owner_signed_else_closure_only | MISSING | CZ_THEOREM_ZERO_CONDITIONAL_CANNOT_SCORE_ALPHA_ALONE | false |
| ZRB3280_1_CR_zero_if_readout_signed | MISSING_CZ_OR_ZERO_THEOREM | 0 | 0_if_parent_exact_U1_current_owner_signed_else_closure_only | MISSING | CR_THEOREM_ZERO_CONDITIONAL_CANNOT_SCORE_ALPHA_ALONE | false |
| ZRB3280_2_hidden_F2_CZ_missing | L_X ln(C_P N_Q + lambda_A + f_X + delta_lambda_rad) | 0_if_readout_signed_else_MISSING | 0_if_current_owner_signed_else_closure_only | MISSING_NUMERIC_CZ_COUNTERTERM_SLOPE | COUNTERTERM_RETAINED_NUMERIC_SLOPE_MISSING | false |
| ZRB3280_3_readout_CR_missing | 0_if_unique_Z_owner_signed_else_MISSING | L_X ln R_alpha_readout | 0_if_current_owner_signed_else_closure_only | MISSING_NUMERIC_READOUT_SLOPE | READOUT_REENTRY_RETAINED_NUMERIC_SLOPE_MISSING | false |
| ZRB3280_4_combined_ZR_bound_contract | C_Z | C_R | 0_if_current_owner_signed_else_closure_only | -C_Z-C_R_if_CJ_zero | COMBINATION_BOUND_ONLY_NO_SEPARATE_CZ_CR_VALUES | false |
| ZRB3280_5_half_bound_CZ_smoke | -6.948988557475e-13 | 0 | 0 | 6.948988557475e-13 | SMOKE | false |
| ZRB3280_6_twice_bound_CZ_smoke | -2.779595422990e-12 | 0 | 0 | 2.779595422990e-12 | SMOKE | false |

## Bound Runner
| row_id | C_e_prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ZRB3280_0_CZ_zero_if_unique_owner_signed | MISSING | MISSING | REFUSE_OR_FAIL | true | false |
| ZRB3280_1_CR_zero_if_readout_signed | MISSING | MISSING | REFUSE_OR_FAIL | true | false |
| ZRB3280_2_hidden_F2_CZ_missing | MISSING_NUMERIC_CZ_COUNTERTERM_SLOPE | MISSING | REFUSE_OR_FAIL | true | false |
| ZRB3280_3_readout_CR_missing | MISSING_NUMERIC_READOUT_SLOPE | MISSING | REFUSE_OR_FAIL | true | false |
| ZRB3280_4_combined_ZR_bound_contract | -C_Z-C_R_if_CJ_zero | MISSING | REFUSE_OR_FAIL | true | false |
| ZRB3280_5_half_bound_CZ_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| ZRB3280_6_twice_bound_CZ_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3280_0_derivation_present | true | false | q_EM^nu=P_loc[Q_Z^nu+nabla_mu T_readout^{mu nu}+boundary] built as the direct Poynting/readout route. |
| GATE3280_1_CZ_owner_signed | false | false | C_Z remains blocked by gauge-norm/no-extra-F2/radiative counterterm debt. |
| GATE3280_2_CR_readout_signed | false | false | C_R remains unsigned. |
| GATE3280_3_CJ_not_used_as_compensator | true | false | 3279 demotion is carried forward. |
| GATE3280_4_runner_expectations | true | false | ZRB3280_0_CZ_zero_if_unique_owner_signed=REFUSE_OR_FAIL;ZRB3280_1_CR_zero_if_readout_signed=REFUSE_OR_FAIL;ZRB3280_2_hidden_F2_CZ_missing=REFUSE_OR_FAIL;ZRB3280_3_readout_CR_mis... |
| GATE3280_5_no_public_claim | true | false | 3280 is derivation plus source-bound gate only. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3280_0_poynting_placement | Poynting/wave response belongs in EM stress/readout residuals, not in C_J. | the background-field intuition now has a precise mathematical home: Z_Q-weighted stress flow and q_EM residuals. | false |
| DEC3280_1_CZ_status | C_Z is the sharpest next derivation target. | C_Z has a concrete owner theorem and a concrete counterexample f_X(Xhat)F_Q^2; this is less woolly than generic readout closure. | false |
| DEC3280_2_CR_status | C_R remains independent readout debt. | even a perfect tree-level Maxwell owner is not enough unless observed alpha readout factors through quotient-fixed data. | false |
| DEC3280_3_bound_status | The alpha envelope bounds only the combination 2C_J-C_Z-C_R, not standalone C_Z or C_R. | future numeric rows must say which side conditions are signed; no compensating cancellations are allowed. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3280_0_3281 | 3281-Y5-R2FR-unique-Maxwell-kinetic-owner-or-CZ-finite-bound-row-under-AX1090.md | Try to close C_Z first: derive a unique parent Maxwell kinetic owner/no-extra-F2 theorem from T_Q/gauge-norm data, or build a finite C_Z source-bound row without using C_J or C_... | Do not claim alpha/Maxwell/local-GR from compact U1 alone; C_Z needs fixed gauge norm, no independent F_Q^2 counterterm, radiative/readout guard, source paths, units, and noncla... |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3280_0_sources_exist | all cited source paths exist | true |  |
| VAL3280_1_sources_parse | all cited source paths parse | true |  |
| VAL3280_2_outputs_parse | all 3280 output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3280_3_qEM_residual_present | q_EM residual route is explicitly derived | true | DER3280_5_qEM_residual |
| VAL3280_4_CZ_CR_not_falsely_signed | C_Z and C_R gates remain unsigned/nonclaim | true | CZCR3280_0_unique_Z_owner=NOT_SIGNED;CZCR3280_1_no_extra_F2=COUNTERTERM_RETAINED;CZCR3280_2_F_only_response=SOURCE_BACKED_PLACEMENT;CZCR3280_3_readout_owner=UNSIGNED;CZCR3280_4_... |
| VAL3280_5_bound_rows_nonclaim | all CZ/CR source-bound rows remain nonclaim | true |  |
| VAL3280_6_runner_expectations | bound runner expectations all match | true | ZRB3280_0_CZ_zero_if_unique_owner_signed=REFUSE_OR_FAIL;ZRB3280_1_CR_zero_if_readout_signed=REFUSE_OR_FAIL;ZRB3280_2_hidden_F2_CZ_missing=REFUSE_OR_FAIL;ZRB3280_3_readout_CR_mis... |
| VAL3280_7_claim_gates_false | no 3280 gate allows alpha/Maxwell/local-GR claim | true | all claim_allowed=false |
| VAL3280_8_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3280_9_overall | 3280 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T15:40:31.045462+00:00
