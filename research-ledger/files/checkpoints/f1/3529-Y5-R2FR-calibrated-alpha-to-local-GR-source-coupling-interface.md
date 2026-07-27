# 3529 - Calibrated Alpha To Local GR Source-Coupling Interface

## Summary
- **Alpha loop closed for baseline work:** `alpha_EM` is calibrated, not derived. That lets the local Maxwell stress be used without pretending MTS predicts alpha.
- **Source interface written:** calibrated Maxwell stress, matter Hilbert stress, total Hilbert current, `G_N/kappa`, Einstein target and Poisson/Newton target are now separated.
- **Key identity retained:** internal EM/matter Lorentz exchange cancels only in `T_total=T_matter+T_EM`; Poynting belongs inside EM Hilbert stress unless external/radiative flux is present.
- **No local-GR claim:** `G_N/kappa`, source normalization, residual EH operators and the full PPN vector are still open.
- **Next throat:** the Newton-constant analogue of alpha: derive or calibrate `G_N/kappa`, then close/bound the Hilbert source denominator and Poisson limit.

## Local Source Target
`G_mn + Lambda g_mn = kappa_0 (T_matter + T_EM)_mn + DeltaE_res_mn`

Weak static target:

`nabla^2 U = 4*pi*G_N*rho_H + residual_source_terms`

This is not claimed yet. It is the contract the remaining local branch has to satisfy.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| script_3529 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3529_calibrated_alpha_to_local_GR_source_coupling_interface.py | True | 3529 generator | False |
| doc_3528 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3528-Y5-R2FR-unique-F2-parent-domain-inheritance-or-calibrated-alpha-constant-contract.md | True | calibrated alpha contract | False |
| next_3528 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3528_NEXT_TARGET.csv | True | 3528-selected source-coupling interface target | False |
| status_3528 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_unique_F2_or_calibrated_alpha_status.csv | True | 3528 canonical alpha status | False |
| contract_3528 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv | True | calibrated alpha contract rows | False |
| composite_3524 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3524_COMPOSITE_THEOREMS.csv | True | shared owner theorem for local source coupling | False |
| kernel_req_3524 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv | True | local kernel value requirements | False |
| em_owner_3503 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv | True | observed Hodge, Maxwell stress and total Hilbert current theorem | False |
| hilbert_gate_3503 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv | True | total Hilbert current closure gates | False |
| hodge_3504 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv | True | Hodge uniqueness and conformal caveat | False |
| local_gr_2633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv | True | conditional local GR/Newton theorem | False |
| normal_gate_2633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv | True | parent normal form gate for local GR | False |
| local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | local empirical bounds for WEP, clocks, PPN, Gdot and R10 | False |

## Source-Coupling Interface
| interface_id | piece | type | mathematical_form | role_in_source_coupling | remaining_gap | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SCI3529_0_calibrated_alpha | alpha_EM baseline | CALIBRATED_CONSTANT | alpha_EM=alpha_0; C_XF2=0 by calibration unless a nonzero branch is proposed | fixes local Maxwell normalization without claiming a derived alpha theorem | nonzero alpha drift/source branches still need WEP/clock/R10 bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3528_CALIBRATED_ALPHA_CONTRACT.csv | False |
| SCI3529_1_calibrated_Maxwell_stress | EM Hilbert stress | DERIVED_IDENTITY_GIVEN_CALIBRATED_ACTION | T_EM^{mu nu}=lambda_0(F^{mu a}F^nu_a - 1/4 g_obs^{mu nu}F^2) plus only explicitly retained residual terms | places Poynting and EM binding energy inside the Hilbert source rather than as a separate force | requires observed Hodge/coframe, same current owner and no readout backreaction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv | False |
| SCI3529_2_total_Hilbert_current | matter plus EM source | DERIVED_CONDITIONAL_IDENTITY | nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda; nabla_mu T_total^{mu nu}=0 | internal Lorentz exchange cancels only in total Hilbert stress | J_Q/source current and projector closure remain unsigned | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3503_TOTAL_HILBERT_CURRENT_CLOSURE_GATE.csv | False |
| SCI3529_3_kappa_G_calibration | gravitational coupling | CALIBRATED_CONSTANT_OR_PARENT_OWNER | kappa_0=8*pi*G_N/c^4 in the local effective branch unless a parent kappa owner is later derived | sets the overall Newtonian source strength after calibration | MTS kappa/G_N source normalization and no fitted-GM transfer still need gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv | False |
| SCI3529_4_local_field_equation | local GR equation target | EXACT_CONDITIONAL_NOT_CLAIMED | G_mn+Lambda g_mn = kappa_0(T_matter+T_EM)_mn + DeltaE_res_mn | separates the GR target from residual operators and source-normalization leaks | DeltaE_res, source normalization, no-shadow coframe and PPN vector must be zero or bounded | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_CONDITIONAL_LOCAL_GR_THEOREM.csv | False |
| SCI3529_5_Newtonian_limit | Newton/Poisson readout | EXACT_CONDITIONAL_NOT_CLAIMED | nabla^2 U = 4*pi*G_N*rho_H + residual_source_terms | defines the route by which GR reduces to Newton inside the MTS branch | source denominator, M_H_ref, boundary class and PPN/Newton residual vector still missing values | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv | False |

## Calibrated Constants
| constant_id | symbol | status | allowed_use | forbidden_use | next_gate | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CON3529_0_alpha | alpha_0 | CALIBRATED_NOT_DERIVED | local Maxwell normalization and baseline EM stress | claiming MTS predicts alpha or using alpha to cancel source residuals | nonzero C_XF2 branches go to WEP/clock/R10 bounds | False |
| CON3529_1_kappa_G | kappa_0 or G_N | CALIBRATED_UNLESS_PARENT_OWNER_DERIVED | local Einstein/Newton coupling after calibration | claiming Newton's constant is derived before kappa/source-normalization owner exists | kappa/G_N source-normalization and M_H_ref owner | False |
| CON3529_2_c_clock | c and clock/ruler conventions | OBSERVED_READOUT_OR_UNIT_CONVENTION_WITH_CAVEATS | local units and Maxwell/GR expression matching | using light-cone agreement to fix conformal/source scale | clock/source/conformal scale owner | False |
| CON3529_3_Lambda | Lambda_local | NEGLIGIBLE_OR_CALIBRATED_FOR_LOCAL_LIMIT | ignored in short-range Newtonian systems or carried as calibrated cosmological term | hiding local residual curvature/source terms inside Lambda | cosmology branch handles Lambda/memory separately | False |

## Residual Ledger
| residual_id | residual | formula_or_role | arena | current_status | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RES3529_0_epsilon_J | Hilbert current/source normalization | epsilon_J measures mismatch between the physical source current and common Hilbert current | Newton/PPN/orbital/source-normalization | MISSING_CURRENT_OWNER_OR_NUMERIC_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv | False |
| RES3529_1_Delta_w_label | source-label/material prefactor | Delta_w_label=P_perp w_source | WEP/R10/PPN/clock/orbital | MISSING_VALUE_OR_THEOREM_ZERO | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv | False |
| RES3529_2_Delta_Hodge_EM | EM Hodge/constitutive mismatch | *_EM-*_obs plus constitutive/readout components | Maxwell limit/light-cone/Poynting/clock/PPN | CONDITIONAL_ZERO_ROUTE_NOT_CLAIMED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv | False |
| RES3529_3_epsilon_Poynting | external/radiative EM flux leakage | boundary integral of Poynting flux or stress-flux drift after total-current closure | Gdot/clock/source drift/orbital | MISSING_POYNTING_PROJECTION_AND_FLUX_VALUE | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3524_KERNEL_VALUE_REQUIREMENTS.csv | False |
| RES3529_4_kappa_G_source | kappa/G_N/source denominator | a1=1/(2*kappa_MTS) and its measured G_N relation before fitted-GM transfer | Newtonian Poisson/PPN/orbital | BLOCKED_COEFFICIENT_OWNER_UNSIGNED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv | False |
| RES3529_5_DeltaE_res | non-EH operator/residual field equation terms | DeltaE_res_mn in the public field equation | R11/local operator closure/PPN | BLOCKED_RESIDUAL_SECTOR_ZERO_OR_BOUNDS_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_NORMAL_DOBS_EH_SYNTHESIS_2633_PARENT_NORMAL_FORM_GATE.csv | False |
| RES3529_6_PPN_vector | full local PPN vector | gamma,beta,preferred-frame,source,endpoint,readout and q_loc/Khat residuals | Cassini/LLR/pulsars/solar-system | BLOCKED_FULL_VECTOR_VALUES_MISSING | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | False |

## Canonical Status
| status_id | quantity | value | meaning | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| STAT3529_0_alpha | alpha_loop | closed_as_calibrated_baseline | alpha no longer blocks the local source spine unless a nonzero C_XF2 branch is proposed | not a derived-alpha claim | False |
| STAT3529_1_EM_stress | calibrated_Maxwell_stress | usable_conditional_identity | variation of calibrated Maxwell action gives EM Hilbert stress/Poynting bookkeeping on observed geometry | source interface clarified but Hodge/current gates remain | False |
| STAT3529_2_GR_Newton | local_GR_Newton_reduction | exact_conditional_not_claimed | Einstein/Poisson form is written with calibrated constants and explicit residuals | no local-GR pass until residuals and PPN vector close | False |
| STAT3529_3_next | next_best_target | kappa_G_source_normalization_and_Newtonian_limit_gate | the decisive next move is G_N/kappa/source denominator and Poisson/PPN residuals | moves project back to GR/Newton derivability | False |

## Decision Ledger
| decision_id | decision | rationale | effect | claim_allowed |
| --- | --- | --- | --- | --- |
| DEC3529_0_use_calibrated_alpha | use calibrated alpha in the baseline local Maxwell stress | 3528 labelled alpha honestly, so the source spine can proceed without deriving alpha first | prevents alpha loop from stalling GR/Newton work | False |
| DEC3529_1_do_not_claim_GR | do not claim local GR/Newton pass | G_N/kappa/source normalization, residual EH operator silence and PPN vector remain open | keeps claim discipline while writing the correct interface | False |
| DEC3529_2_next_kappa_source | target kappa/G_N and source normalization next | this is the Newton-constant analogue of the alpha decision and directly controls the Poisson limit | next step attacks the GR-to-Newton reduction spine | False |

## Next Target
| next_doc | next_script | objective | success_gate | why_next | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| 3530-Y5-R2FR-kappa-G-source-normalization-and-Newtonian-limit-gate.md | scripts/Y5_R2FR_3530_kappa_G_source_normalization_and_Newtonian_limit_gate.py | Decide the G_N/kappa analogue of the alpha issue: derive or explicitly calibrate the gravitational coupling, then test whether the Hilbert source denominator and Newtonian Poisson limit can be closed or bounded without fitted-GM smuggling. | A ledger separates derived kappa identities, calibrated G_N, source-denominator residuals and PPN/Newton bound rows; no Newton/local-GR claim is allowed without source normalization and full PPN vector gates. | 3529 exposes kappa/G_N and source normalization as the next hard throat after calibrated alpha. | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3529_0_sources_exist | True | all cited local source paths exist | False |
| VAL3529_1_alpha_calibrated | True | alpha is used only as calibrated baseline | False |
| VAL3529_2_EM_stress_identity_present | True | calibrated Maxwell Hilbert stress identity is present | False |
| VAL3529_3_Einstein_and_Poisson_targets_present | True | Einstein and Newtonian target equations written with residuals | False |
| VAL3529_4_residuals_cover_GR_throat | True | source normalization, kappa/G, DeltaE and PPN vector residuals present | False |
| VAL3529_5_no_claim_flags_true | True | no local-GR/Newton/alpha claim is promoted | False |
| VAL3529_6_next_target_selected | True | 3530 kappa/G/source-normalization target selected | False |
| VAL3529_7_csvs_parse | True | source_register; interface; constants; residuals; status; canonical_status; decision_ledger; next_target | False |
| VAL3529_8_outputs_stay_in_post_checkpoint_work | True | root=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work | False |
| VAL3529_9_formalization_workbench_not_targeted | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench | False |
| VAL3529_SUMMARY | True | PASS | False |
