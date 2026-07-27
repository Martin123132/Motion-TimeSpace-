# 1035 Y5 R10 K_X Green-kernel normalization and profile integral

**Status:** The R10 theory-side kernel is now reduced to a clean conditional law: a finite local mode with quadratic residue `Z_X` gives a Yukawa Green kernel, and the observable coefficient is a **source-test product** `alpha_X = K_X^R10 beta_s beta_t + epsilon_tail`. This is useful progress, but not a claim: `Z_X`, `lambda_X`, `beta_s`, `beta_t`, the R10 harmonic profile, and the retained-tail envelope are still missing.

**Important correction:** the universal coupling branch is not naturally linear in `c_g`. A two-body fifth-force exchange uses source and test charges. If both legs are universal Weyl legs, the leading Yukawa coefficient is proportional to `c_g^2` unless the source leg has already been explicitly packed into `Qbar_XH`.

**Claim ceiling:** no numeric `K_X`, no R10 pass, no `alpha=0` local claim, no linear-`c_g` score, no unity `tau_R10` shortcut, and no GitHub/formalization-workbench action is allowed from 1035.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1035_0_1034_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1034_NEXT_TARGET.csv | true | true | 1034 handoff selecting K_X/profile-integral target. |
| SRC1035_1_1034_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv | true | true | 1034 missing K_X/Qbar/tau/c_g/tail projection pack. |
| SRC1035_2_1034_convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1034_SOURCE_TEST_PROFILE_CONVENTION.csv | true | true | 1034 source/test profile placeholders. |
| SRC1035_3_1034_bound_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | true | true | 1034 external curve review candidate, not a live claim curve. |
| SRC1035_4_1034_alpha_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv | true | true | 1034 alpha-bound summary and anchor rows. |
| SRC1035_5_1033_tau_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | true | true | 1033 factorization into K_X, Qbar_XH, tau_R10, c_g, and retained tails. |
| SRC1035_6_631_charge_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv | true | true | 631 source/test charge law showing universal branch gives alpha proportional to c_g squared. |
| SRC1035_7_live_mts_placeholder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\R10_alpha_lambda_curve_MTS_source_normalization.csv | true | true | Live MTS alpha(lambda) prediction remains placeholder-only. |
| SRC1035_8_bound_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | true | true | Existing R10 runner used for nonclaim smoke validation. |

## Kernel derivation audit
| derivation_id | step | mathematical_result | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| KXD1035_0_parent_quadratic_operator | isolate the finite local response mode | S_X^(2)=-1/2 int [Z_X (partial X)^2 + Z_X lambda_X^-2 X^2] + int X J_X | CONDITIONAL_OPERATOR_FORM | parent-signed Z_X, range/mass relation, X normalization, and source-current definition | false |
| KXD1035_1_static_green_function | invert the static operator | (nabla^2-lambda_X^-2) X = -J_X/Z_X; G_lambda(r)=exp(-r/lambda)/(4 pi r) | DERIVED_CONDITIONAL_GREEN_KERNEL | proof that MTS local finite branch really reduces to this operator and not derivative/disformal/tensor response | false |
| KXD1035_2_point_body_yukawa_match | match the Green solution to the R10 Yukawa convention | alpha_X(lambda_X)=K_X^pt beta_s beta_t with K_X^pt fixed by the parent normalization; in canonical mass-normalized units K_X^pt=1/(4 pi G_N Z_X) | CONDITIONAL_NORMALIZATION_LAW | whether beta_i already absorbs sqrt(4 pi G_N Z_X), and SI/hbar/c conversion convention | false |
| KXD1035_3_extended_body_overlap | replace point bodies by source/test support integrals | F_ST(lambda,R)=R exp(R/lambda)/(M_s M_t) int rho_s(x) rho_t(y) exp(-\|R+x-y\|/lambda)/\|R+x-y\| d^3x d^3y | DERIVED_PROFILE_FORM_FACTOR_CONTRACT | actual R10 geometry/material density/support and harmonic torque projection | false |
| KXD1035_4_R10_harmonic_projection | map potential energy to the measured R10 torque harmonics | K_X^R10(lambda)=K_X^pt * F_ST(lambda) * Pi_R10, with Pi_R10 the experiment-specific torque/readout projection | CONDITIONAL_R10_PROJECTION_CONTRACT | Fourier-Bessel R10 geometry or official torque kernels for the MTS source current | false |
| KXD1035_5_verdict | decide whether K_X(lambda) is numeric | K_X(lambda) has a derived shape contract but no numeric parent-signed value | NOT_NUMERIC_CURRENT_CORPUS | Z_X, lambda_X, beta_s, beta_t, R10 profile/harmonic projection, and retained-tail envelope | false |

## Source/test charge split
| charge_id | branch | source_charge | test_charge | alpha_law | status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BETA1035_0_product_law | generic finite X exchange | beta_s(lambda) | beta_t(lambda) | alpha_X(lambda)=K_X^R10(lambda) beta_s(lambda) beta_t(lambda) + epsilon_tail(lambda) | REQUIRED_PRODUCT_FORM | false | This prevents accidentally treating a two-body exchange as linear in one coupling. |
| BETA1035_1_universal_weyl | universal conformal matter-frame response | beta_s=c_g times source profile if source matter mass depends on X | beta_t=c_g times test/readout profile if test mass depends on X | alpha_X proportional to K_X^R10 c_g^2, not K_X c_g, unless Qbar_XH explicitly already contains one c_g | CONDITIONAL_CG_SQUARED_WARNING | false | Refines the 1033 shorthand: Qbar_XH must be interpreted as the source leg, not a free magic prefactor. |
| BETA1035_2_quotient_zero | quotient-only matter action | beta_s=0 | beta_t=0 | alpha_X=0 if and only if the quotient-zero premises are parent-signed | CONDITIONAL_ZERO_BRANCH | false | A zero branch would beat R10 cleanly, but it is not available as a naked assumption. |
| BETA1035_3_composition_or_disformal | composition/disformal/stress response | beta_s plus stress/support terms | beta_t plus material/readout terms | alpha_X requires extra composition, WEP, clock, and stress projection rows | MIXED_BRANCH_BLOCKED | false | This branch cannot be scored by a scalar Yukawa row alone. |

## Profile integral contract
| profile_id | required_object | definition | formula | status | needed_for_score | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PROF1035_0_source_support | rho_s^X(x) | source-body X charge density normalized to the same mass/current convention as beta_s | Q_s(lambda)=int_source rho_s^X(x) d^3x with finite-size corrections entering F_ST | MISSING_SOURCE_SUPPORT | R10 attractor/test-body material density and parent X charge density rule | false |
| PROF1035_1_test_support | rho_t^X(y) | test-body/readout X charge density normalized to beta_t | Q_t(lambda)=int_test rho_t^X(y) d^3y with torsion readout projection | MISSING_TEST_SUPPORT | pendulum/detector support, readout convention, and material trace law | false |
| PROF1035_2_pair_overlap | F_ST(lambda,R) | extended-body correction that reduces to 1 in the point-body limit under the chosen convention | R exp(R/lambda)/(M_s M_t) int rho_s rho_t exp(-r_xy/lambda)/r_xy d^3x d^3y | SYMBOLIC_FORM_FACTOR_ONLY | geometry/material integrals or official Fourier-Bessel kernel | false |
| PROF1035_3_R10_harmonic | Pi_R10(lambda) | maps the source/test potential overlap to the 18 omega and 120 omega torque harmonics used by Eot-Wash | Pi_R10 = projected_torque_kernel[MTS source current] / projected_torque_kernel[unit-alpha Yukawa] | MISSING_R10_HARMONIC_KERNEL | R10 geometry kernel, harmonic weights, and separation distribution | false |
| PROF1035_4_measured_G_calibration | Newton normalization | same G_N and mass normalization used by the experiment and by the MTS weak-field limit | alpha is dimensionless only after dividing the X interaction by -G_N M_s M_t/r or its torque equivalent | MISSING_PARENT_NEWTON_MATCH | MTS-to-Newton local limit and measured-G calibration convention | false |

## K_X factorization rows
| factor_id | factor | symbolic_value | units | status | missing_for_claim | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| KXF1035_0_KX_point | K_X^pt | 1/(4 pi G_N Z_X) if beta_i are mass-normalized parent charges that do not already absorb Z_X or G_N | dimensionless after parent charge convention; otherwise parent-declared | SYMBOLIC_CONDITIONAL | Z_X and charge-unit convention | false | false |
| KXF1035_1_range | lambda_X | lambda_X = 1/m_X in natural units, or hbar/(m_X c) in SI mass units | m | MISSING_PARENT_RANGE_RELATION | parent mass/kinetic row for finite X mode | false | false |
| KXF1035_2_profile | F_ST(lambda) | extended-body Yukawa overlap normalized to the point-body alpha convention | dimensionless | SYMBOLIC_ONLY | R10 source/test support and material density rule | false | false |
| KXF1035_3_harmonic | Pi_R10(lambda) | R10 torque harmonic projection ratio for MTS current versus unit-alpha Yukawa current | dimensionless | MISSING_EXPERIMENTAL_PROJECTION | Fourier-Bessel torque kernel or official numerical kernel | false | false |
| KXF1035_4_total | K_X^R10(lambda) | K_X^pt * F_ST(lambda) * Pi_R10(lambda) | dimensionless alpha-normalized factor | NOT_NUMERIC_CURRENT_CORPUS | all KXF1035_0 through KXF1035_3 inputs | false | false |

## MTS alpha prediction template
| model_id | branch_id | lambda_value | alpha_predicted | derivation_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | KX_profile_product_template | MISSING_PARENT_LAMBDA_X | MISSING_KX_BETA_SOURCE_BETA_TEST_TAILS | template_invalid_missing_parent_ZX_lambda_beta_profile_and_promoted_bound | false | Skeleton row only; do not score. |
| MTS_source_normalized_Newton_branch | universal_weyl_cg_squared_template | MISSING_PARENT_LAMBDA_X | MISSING_NUMERIC_KX_TIMES_CG_SQUARED | template_invalid_missing_cg_ZX_profile_and_source_test_charge_signoff | false | This row blocks accidental linear-c_g scoring. |
| MTS_source_normalized_Newton_branch | quotient_zero_template | ALL_LOCAL_R10_RANGE | MISSING_SIGNED_ZERO_THEOREM | template_invalid_missing_no_shadow_matter_action_zero_theorem | false | Closure-only until the parent action proves the quotient-zero branch. |

## Join readiness
| join_id | side | object | current_status | ready_for_join | needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| JOIN1035_0_bound_curve | external | alpha_bound(lambda) | REVIEW_CANDIDATE_NONCLAIM | false | official supplement table or human QA promotion | false |
| JOIN1035_1_KX | theory | K_X^R10(lambda) | SYMBOLIC_CONDITIONAL | false | Z_X, lambda_X, G_N convention, profile, and harmonic projection | false |
| JOIN1035_2_beta_source | theory | beta_s(lambda) | MISSING_SOURCE_CHARGE | false | parent matter action source-leg charge | false |
| JOIN1035_3_beta_test | theory | beta_t(lambda) | MISSING_TEST_CHARGE | false | tau_R10/readout projection and parent c_g or zero theorem | false |
| JOIN1035_4_tail_envelope | theory | epsilon_tail(lambda) | MISSING_ABSOLUTE_ENVELOPE | false | no-cancellation absolute envelope for all retained components | false |

## Runner smoke status
| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| SMOKE1035_0_runner_status | 0 | 0 | 1 | false | false | blocked_nonclaim |

## Placeholder refusal runner
| refusal_id | object | current_status | refusal_status | failure_reasons | score_eligible | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| REF1035_0_alpha_boundlambda | alpha_bound(lambda) | REVIEW_CANDIDATE_NONCLAIM | rejected_missing_or_nonclaim_join_input | NOT_READY_FOR_JOIN;CLAIM_POLICY_FALSE | false | false |
| REF1035_1_K_X^R10lambda | K_X^R10(lambda) | SYMBOLIC_CONDITIONAL | rejected_missing_or_nonclaim_join_input | NOT_READY_FOR_JOIN;CLAIM_POLICY_FALSE | false | false |
| REF1035_2_beta_slambda | beta_s(lambda) | MISSING_SOURCE_CHARGE | rejected_missing_or_nonclaim_join_input | MISSING_SOURCE_CHARGE;NOT_READY_FOR_JOIN;CLAIM_POLICY_FALSE | false | false |
| REF1035_3_beta_tlambda | beta_t(lambda) | MISSING_TEST_CHARGE | rejected_missing_or_nonclaim_join_input | MISSING_TEST_CHARGE;NOT_READY_FOR_JOIN;CLAIM_POLICY_FALSE | false | false |
| REF1035_4_epsilon_taillambda | epsilon_tail(lambda) | MISSING_ABSOLUTE_ENVELOPE | rejected_missing_or_nonclaim_join_input | MISSING_ABSOLUTE_ENVELOPE;NOT_READY_FOR_JOIN;CLAIM_POLICY_FALSE | false | false |
| REF1035_runner_smoke | R10 existing runner smoke | blocked_nonclaim | runner_correctly_refused_claim | NO_VALID_MTS_ROWS_OR_NONCLAIM_BOUND_ROWS | false | false |

## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CGATE1035_0_green_kernel | K_X(lambda) is derived numerically | false | Green kernel form is conditional but Z_X/range/source-current normalization are missing | false | false |
| CGATE1035_1_charge_product | R10 alpha is linear in c_g | false | two-body exchange requires beta_source beta_test; universal branch is proportional to c_g^2 unless source leg already includes c_g | false | false |
| CGATE1035_2_profile_integral | R10 finite-size/profile projection is ready | false | source/test support, material charge, and R10 harmonic projection are missing | false | false |
| CGATE1035_3_runner_claim | existing R10 runner grants a pass | false | nonclaim smoke has no valid MTS rows and no promoted bound curve rows | false | false |
| CGATE1035_4_zero_branch | local R10 is zero by quotient descent | false | zero branch remains conditional until no-shadow matter action theorem is signed | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1035_0_kernel_status | K_X has a derived conditional Green-kernel form but no numeric value. | the static Yukawa inverse is fixed once Z_X and lambda_X exist, but the parent action has not supplied them. | derive/source the parent X quadratic row: Z_X, M_X/lambda_X, source current J_X, and beta normalization | false |
| DEC1035_1_coupling_status | The R10 coupling must be source-test product beta_s beta_t. | a fifth-force Yukawa exchange couples two bodies; universal c_g generally enters twice. | split Qbar_XH and tau_R10 into explicit beta_source and beta_test rows | false |
| DEC1035_2_score_status | R10 scoring remains blocked, correctly. | the external curve is still nonclaim and the MTS alpha prediction is symbolic. | use 1035 template only for schema smoke, not evidence | false |
| DEC1035_3_next_target | Next target is parent X quadratic action and beta source/test split. | that is the shortest route to making K_X and c_g/c_g^2 mathematically owned rather than fitted or guessed. | 1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1035_SUMMARY | pass | 1035 K_X Green-kernel/profile-integral validation summary | 2026-06-14T06:54:58.406063+00:00 |
| V1035_0_sources_exist | pass | all 1035 source paths exist and expected needles are present | 2026-06-14T06:54:58.406076+00:00 |
| V1035_1_green_kernel_contract | pass | static Yukawa Green-kernel form is written | 2026-06-14T06:54:58.406081+00:00 |
| V1035_2_no_numeric_KX_claim | pass | K_X remains explicitly nonnumeric/nonclaim | 2026-06-14T06:54:58.406084+00:00 |
| V1035_3_charge_product_law | pass | source-test product law and universal c_g-squared warning are present | 2026-06-14T06:54:58.406087+00:00 |
| V1035_4_profile_missing_explicit | pass | R10 harmonic/profile and Newton normalization gaps are explicit | 2026-06-14T06:54:58.406090+00:00 |
| V1035_5_kx_factorization_blocked | pass | K_X factorization rows refuse scoring | 2026-06-14T06:54:58.406092+00:00 |
| V1035_6_mts_template_schema | pass | MTS nonclaim template has the runner-required schema | 2026-06-14T06:54:58.406095+00:00 |
| V1035_7_mts_template_nonclaim | pass | MTS template rows remain valid_for_claim=false | 2026-06-14T06:54:58.406097+00:00 |
| V1035_8_join_readiness_blocked | pass | all join inputs remain blocked/nonclaim | 2026-06-14T06:54:58.406100+00:00 |
| V1035_9_runner_smoke_refuses_claim | pass | existing runner refuses the nonclaim 1035 smoke rows | 2026-06-14T06:54:58.406102+00:00 |
| V1035_10_claim_gates_blocked | pass | all claim gates remain closed | 2026-06-14T06:54:58.406104+00:00 |
| V1035_11_next_target_written | pass | next target row is present | 2026-06-14T06:54:58.406107+00:00 |
| V1035_12_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T06:54:58.406109+00:00 |
| V1035_13_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T06:54:58.406112+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md | derive or demote the parent finite-X quadratic action row that supplies Z_X, lambda_X/M_X, J_X, beta_source, beta_test, and the c_g versus c_g^2 coupling law | parent action coefficient, kinetic residue sign, range relation, source current, source/test charge split, quotient-zero alternative, disformal/composition tail routing, R10 alpha template update | invented numeric K_X, invented c_g, unity tau shortcut, linear-c_g scoring without source leg, R10 pass claim, formalization-workbench edits, GitHub action | false |
