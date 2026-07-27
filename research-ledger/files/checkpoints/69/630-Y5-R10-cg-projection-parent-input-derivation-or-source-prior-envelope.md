# 630 Y5 R10 cg projection parent input derivation or source prior envelope

Status: `Y5_R10_coupling_derivation_gate_built_cg_zero_not_proven_finite_projection_envelope_written`  
Claim ceiling: `coupling_derivation_checkpoint_only_no_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md`

## Verdict
- The gut feeling was right: the coupling is now isolated as the local-theory bottleneck.
- A clean `c_g=0` route exists in principle, but it still requires a parent-signed matter-frame descent proof.
- If coupling survives, the finite projection law must separate source and test legs before R10/PPN/clocks can mean anything.
- This checkpoint therefore writes a nonclaim pressure envelope, not a pass.

## Source Register
| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC630_0 | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | true | immediate R10 c_g projection smoke runner | false |
| SRC630_1 | source-intake/mts_residuals/P8_Y5_BRR545_629_VALIDATION.csv | true | 629 validation gate | false |
| SRC630_2 | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | review-candidate R10 pressure samples | false |
| SRC630_3 | source-intake/mts_residuals/P8_Y5_R10_629_CG_PROJECTION_CONTRACT.csv | true | c_g projection contract from 629 | false |
| SRC630_4 | 628-Y5-R10-real-local-bound-input-sources-for-cg-or-Zcg-proof.md | true | real local bound source acquisition | false |
| SRC630_5 | 627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md | true | c_g zero-proof attempt and acquisition ledger | false |
| SRC630_6 | source-intake/mts_residuals/P8_Y5_R10_627_ZERO_PROOF_AUDIT.csv | true | prior zero-proof clause audit | false |
| SRC630_7 | source-intake/mts_residuals/P8_Y5_R10_627_CG_ACQUISITION_LEDGER.csv | true | prior c_g/tau acquisition ledger | false |
| SRC630_8 | 626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md | true | quotient-invariant matter action signature attempt | false |
| SRC630_9 | 625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md | true | representative Weyl/disformal exclusion attempt | false |
| SRC630_10 | scripts/Y5_R10_cg_projection_parent_input_derivation_or_source_prior_envelope.py | true | this checkpoint generator | false |

## Zero-Coupling Theorem Audit
| clause_id | zero_clause | formal_condition | derivation_status | if_signed | if_unsigned | supports_cg_zero | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZC630_0_parent_matter_frame | matter frame depends only on quotient geometry | g_m = g_m[q(Phi), Psi_m, theta] with no representative X dependence | not_parent_signed | partial_X S_matter = 0 and c_g=0 follows at the matter-frame level | representative common-frame leakage remains possible | necessary_not_sufficient | false |
| ZC630_1_vertical_generator | local residual X is vertical in the quotient fibre | Dq[v_X]=0 on the local matter branch before variation | conditional_not_parent_signed | X shifts are gauge/representative changes, not matter charges | X can remain a physical scalar/local geometric datum | necessary_not_sufficient | false |
| ZC630_2_action_descent | matter action descends to the quotient | Lie_vX S_matter = 0 up to owned gauge/boundary terms | not_parent_signed | test and source legs both vanish for vertical X | c_g must be derived or bounded as a physical coupling | central_clause | false |
| ZC630_3_no_representative_weyl_disformal | no fixed representative Weyl/disformal matter coefficient | A_g(X), B_g(X), and disformal Pi terms are absent, quotient-owned, or auxiliary | not_parent_signed | no hidden c_g re-enters through rods/clocks | c_g or disformal residue can reappear in local tests | necessary_not_sufficient | false |
| ZC630_4_boundary_projection_silence | vertical boundary/exact terms have zero R10/local projection | boundary contribution to Lie_vX S_matter has no source/test observable leg | not_parent_signed | edge terms cannot fake a finite R10 coupling | boundary/non-Hilbert residual can source a finite projection | necessary_not_sufficient | false |
| ZC630_5_zero_verdict | c_g=0 theorem | ZC630_0..ZC630_4 jointly signed by parent action | not_proven | alpha_MTS_R10(lambda)=0 for all lambda and local GR route gets a serious boost | finite projection envelope is required | false | false |

## Finite Coupling Derivation
| step_id | derivation_step | equation | meaning | status | needed_parent_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FD630_0_matter_frame_expansion | Introduce local representative matter-frame response | g_m = A_g(X)^2 g_q + disformal_terms; A_g(X)=1+c_g Xhat+O(Xhat^2) | c_g is the first derivative of the matter-frame scale with respect to the normalized local residual mode | conditional_definition_not_parent_value | matter frame functional A_g or proof A_g independent of Xhat | false |
| FD630_1_source_test_current | Vary the matter action with respect to Xhat | delta S_matter/delta Xhat = c_g tau_A T_matter + disformal/current terms | ordinary nonrelativistic matter sources the residual through its trace unless descent kills the derivative | conditional_projection_form | source and test current normalization plus tau_A for each arena | false |
| FD630_2_static_mode_equation | Linearize the residual mode around the local vacuum | Z_eff (nabla^2 - lambda_X^-2) Xhat = -J_X | Z_eff and lambda_X set the strength/range of any local Yukawa-like exchange | conditional_linear_response | Z_eff, M_X^2, lambda_X=sqrt(Z_eff/M_X^2), source current J_X | false |
| FD630_3_green_function_projection | Solve the static Green-function response | Xhat(r) proportional to J_X exp(-r/lambda_X)/(4 pi Z_eff r) | the residual appears as a finite-range Yukawa correction if its source/test legs survive | formal_shape_derived_inputs_missing | apparatus/source profile Qbar_XH(lambda;lambda_X) and boundary condition | false |
| FD630_4_observable_alpha_linear_product | Match the response to the R10 Yukawa alpha convention | alpha_MTS_R10(lambda)=abs(c_g tau_R10(lambda) K_X Qbar_XH(lambda;lambda_X) qbar_XT/Z_eff) | this is the previous linear-product formula if source-leg physics is already absorbed into K_X Qbar_XH qbar_XT | derived_as_contract_not_numeric | c_g,tau_R10,K_X,Qbar_XH,qbar_XT,Z_eff,lambda_X | false |
| FD630_5_observable_alpha_two_leg_branch | Keep source and test legs separate | alpha_MTS_R10(lambda)=abs(beta_source(lambda) beta_test(lambda))/(4 pi G_eff Z_eff) times profile factors | if c_g controls both source and test legs then the bound pressures c_g squared, not c_g linearly | ambiguity_explicit | whether c_g is a one-leg readout coefficient or a universal two-leg matter coupling | false |
| FD630_6_claim_gate | Score against R10 only after both theory and bound rows are promoted | abs(alpha_MTS_R10(lambda_i)) <= alpha_bound(lambda_i) for every source-backed lambda_i | 629 pressure samples are coefficient targets, not evidence of a pass | blocked_for_claim | physical alpha rows plus promoted source-backed R10 curve | false |

## Parent Input Targets
| input_id | symbol | definition | units | current_status | required_derivation | failure_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PI630_0_c_g | c_g | d ln A_g/dXhat at the local vacuum, or zero by quotient descent | dimensionless | unsourced | vary the parent matter frame with respect to the local residual representative | no R10/PPN/clock/orbital coupling can be scored | false |
| PI630_1_tau_R10 | tau_R10(lambda) | dimensionless source/test projection for Eot-Wash geometry and material response | dimensionless | unsourced | map local residual current into the R10 Yukawa-alpha observable | R10 data cannot be used as a physical MTS test | false |
| PI630_2_K_X | K_X | parent kernel/normalization converting residual source current to observable potential strength | schema_required | unsourced | read off from the parent quadratic action and normalization convention | linear-product alpha is symbolic | false |
| PI630_3_Qbar_XH | Qbar_XH(lambda;lambda_X) | source/profile response of the local residual mode in the experimental geometry | schema_required | unsourced | solve/profile-average the residual Green-function response | source leg remains a placeholder | false |
| PI630_4_qbar_XT | qbar_XT | test-body/readout charge or projection of the local residual onto matter | schema_required | unsourced | derive test-leg charge from matter variation or prove it vanishes | cannot tell linear from two-leg coupling branch | false |
| PI630_5_Z_eff | Z_eff | effective kinetic normalization of the local residual mode | action_normalization | unsourced | extract from parent quadratic Hessian in the local sector | alpha normalization is arbitrary | false |
| PI630_6_lambda_X | lambda_X | residual range, sqrt(Z_eff/M_X^2) | m | unsourced | derive M_X^2 from parent Hessian/eigenvalue or prove no finite range | cannot place the residual on the R10 curve | false |

## R10 Product Pressure Envelope
| envelope_id | sample_id | lambda_value | lambda_units | alpha_bound_review_candidate | linear_product_bound | linear_product | two_leg_unit_profile_coupling_bound | two_leg_note | pressure_class | diagnostic_weight | source | lambda_numeric_positive | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PE630_0 | PS629_0 | 5.9e-06 | m | 897932.29287 | 897932.29287 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 947.592894058 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | weak_pressure_alpha_bound_above_100 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_1 | PS629_1 | 1e-05 | m | 41538.8057283 | 41538.8057283 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 203.810710534 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | weak_pressure_alpha_bound_above_100 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_2 | PS629_2 | 2e-05 | m | 183.665577985 | 183.665577985 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 13.552327401 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | weak_pressure_alpha_bound_above_100 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_3 | PS629_3 | 3.86e-05 | m | 0.991537244704 | 0.991537244704 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 0.995759631992 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | strong_pressure_alpha_bound_0p1_to_1 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_4 | PS629_4 | 5.6e-05 | m | 0.300428094431 | 0.300428094431 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 0.548113213151 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | strong_pressure_alpha_bound_0p1_to_1 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_5 | PS629_5 | 0.0001 | m | 17.5879273456 | 17.5879273456 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 4.19379629281 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | moderate_pressure_alpha_bound_1_to_100 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_6 | PS629_6 | 0.0003 | m | 0.215104553289 | 0.215104553289 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 0.463793653783 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | strong_pressure_alpha_bound_0p1_to_1 | pressure_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_7 | PS629_7 | 0.000608 | m | 0.00234466430052 | 0.00234466430052 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 0.048421733762 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | knife_edge_pressure_alpha_bound_below_0p01 | tightest_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |
| PE630_8 | PS629_8 | 0.001 | m | 0.00998933369038 | 0.00998933369038 | abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | 0.099946654223 | if alpha roughly c_eff^2 with unit profile, then abs(c_eff)<=sqrt(alpha_bound); profile factors still missing | knife_edge_pressure_alpha_bound_below_0p01 | tightest_sample | source-intake/mts_residuals/P8_Y5_R10_629_REVIEW_CURVE_PRESSURE_SAMPLES.csv | true | false |

## Scalar Coupling Ambiguity Ledger
| ambiguity_id | branch | alpha_law | when_valid | risk | next_resolution | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| AMB630_0_zero_branch | quotient-descent zero coupling | alpha_MTS_R10(lambda)=0 | matter action descends to quotient and X is purely vertical with silent boundary terms | currently not parent-signed | prove matter-frame variation has no Xhat derivative | false |
| AMB630_1_linear_source_absorbed | linear product with source leg absorbed | alpha=abs(c_g*tau_R10*K_X*Qbar_XH*qbar_XT/Z_eff) | K_X Qbar_XH qbar_XT already contains the source charge while c_g is the test/readout coupling | can hide a second matter leg unless source/test definitions are explicit | derive source and test currents separately | false |
| AMB630_2_two_leg_universal | standard scalar-like two-leg coupling | alpha proportional to beta_source*beta_test; universal matter coupling gives alpha proportional to c_g^2 | the same common-frame derivative controls both source and test bodies | R10 pressure on c_g is sqrt(alpha_bound/profile), not alpha_bound directly | derive whether c_g belongs to one leg, both legs, or neither | false |
| AMB630_3_disformal_residue | Weyl/disformal mixed coupling | alpha receives c_g plus d_g_Pi/profile terms | representative disformal channel survives matter-frame descent | conformal c_g scoring understates the local-test channel | keep disformal branch blocked until matter frame is varied | false |

## Next Derivation Contract
| contract_id | required_output | success_condition | if_success | if_fail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NDC630_0_define_matter_frame | explicit g_matter[q(Phi),Xhat,Psi,theta] or proof of no Xhat dependence | partial g_matter/partial Xhat is zero or a symbolic expression with units/source | c_g zero theorem or finite c_g expression becomes possible | coupling branch remains closure-only | false |
| NDC630_1_vary_matter_action | delta S_matter/delta Xhat and source/test currents | source and test legs are separated instead of hidden in K_X/Qbar/qbar | linear-vs-squared ambiguity is resolved | R10 pressure envelope remains only diagnostic | false |
| NDC630_2_match_to_yukawa_alpha | normalization map from Xhat Green function to Eot-Wash alpha(lambda) | all factors in alpha_MTS_R10 have owner equations and units | nonclaim numeric/prior scans can be meaningful | no local empirical score is legitimate | false |
| NDC630_3_cross_arena_consistency | same c_g/tau_A branch mapped to R10, PPN, clocks, and orbital tests | one coupling choice does not solve R10 while breaking PPN/clocks by construction | local-GR reduction can be tested as a coupled system | route is phenomenological patchwork and must be demoted | false |

## Nonclaim Summary
| status | claim_ceiling | c_g_zero_proven | finite_cg_numeric | linear_vs_two_leg_resolved | pressure_rows | tightest_review_alpha_bound | tightest_review_lambda_m | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_coupling_derivation_gate_built_cg_zero_not_proven_finite_projection_envelope_written | coupling_derivation_checkpoint_only_no_R10_WEP_PPN_clock_or_local_GR_pass | false | false | false | 9 | 0.00234466430052 | 0.000608 | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |

## Decision
| decision_id | decision | meaning | status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D630_0_main_verdict | Y5_R10_coupling_derivation_gate_built_cg_zero_not_proven_finite_projection_envelope_written | the coupling problem is now explicitly isolated as the next theory bottleneck | progress_but_not_claim | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |
| D630_1_zero_route | c_g_zero_not_proven | quotient descent would be beautiful but remains unsigned at the parent matter-frame level | blocked_for_claim | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |
| D630_2_finite_route | finite_projection_envelope_written | if coupling survives, R10 constrains the effective product strongly around the review-curve tight spots | diagnostic_pressure_only | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |
| D630_3_branch_ambiguity | linear_vs_two_leg_coupling_must_be_resolved | this is probably the missing gearbox: source/test coupling ownership decides whether local tests are safe | next_required | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |
| D630_4_claim_ceiling | coupling_derivation_checkpoint_only_no_R10_WEP_PPN_clock_or_local_GR_pass | no local-GR, R10, WEP, PPN, clock, or orbital pass follows from 630 | hard_guardrail | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md | false |

## Route Update
| route_id | allowed_after_630 | forbidden_after_630 | next_action |
| --- | --- | --- | --- |
| RU630_0_allowed | Treat coupling as the primary local-theory bottleneck. | Claim local GR reduction before deriving matter-frame variation. | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md |
| RU630_1_allowed | Use R10 pressure envelope as a private target for the effective product. | Use review-candidate pressure samples as public exclusion/pass evidence. | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md |
| RU630_2_allowed | Resolve whether c_g is zero, one-leg, two-leg, or disformal-mixed. | Hide source/test legs inside a single fitted symbol. | 631-Y5-R10-matter-frame-variation-cg-zero-or-source-test-charge-law.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V630_0_source_paths_exist | pass | missing=0 |
| V630_1_prior_629_clean | pass | prior_rows=9;prior_fails=0 |
| V630_2_zero_theorem_attempted_not_promoted | pass | zero_rows=6;zero_verdict=not_proven |
| V630_3_finite_projection_law_written | pass | finite_rows=7 |
| V630_4_parent_inputs_remain_nonclaim | pass | input_rows=7;claim_rows=0 |
| V630_5_pressure_envelope_numeric_nonclaim | pass | pressure_rows=9;numeric_nonclaim=9;tightest=0.00234466430052 |
| V630_6_coupling_ambiguity_explicit | pass | ambiguity_rows=4 |
| V630_7_next_derivation_contract_written | pass | contract_rows=4 |
| V630_8_no_local_claim | pass | c_g_zero=false;finite_coupling_numeric=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |
