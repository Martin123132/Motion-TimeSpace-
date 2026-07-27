# 631 Y5 R10 matter frame variation cg zero or source test charge law

Status: `Y5_R10_matter_frame_variation_derived_conditional_two_leg_law_cg_zero_not_signed`  
Claim ceiling: `conditional_matter_variation_only_no_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md`

## Verdict
- The matter-frame variation gives the missing coupling law in conditional form.
- If the matter frame and matter constants are quotient-only, `J_X=0` and the `c_g=0` branch follows.
- If a conformal representative matter frame survives, `J_X` is a trace current and ordinary source/test bodies both carry charge.
- Therefore a finite universal coupling is naturally two-legged: `alpha` scales like a source charge times a test charge, not primitive linear `c_g`.
- The old linear row survives only as compressed notation if the source leg is explicitly owned elsewhere.

## Source Register
| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC631_0 | 630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md | true | immediate coupling derivation gate | false |
| SRC631_1 | source-intake/mts_residuals/P8_Y5_BRR545_630_VALIDATION.csv | true | 630 validation gate | false |
| SRC631_2 | source-intake/mts_residuals/P8_Y5_R10_630_R10_PRODUCT_PRESSURE_ENVELOPE.csv | true | R10 product pressure envelope | false |
| SRC631_3 | source-intake/mts_residuals/P8_Y5_R10_630_SCALAR_COUPLING_AMBIGUITY_LEDGER.csv | true | linear-vs-two-leg ambiguity ledger | false |
| SRC631_4 | source-intake/mts_residuals/P8_Y5_R10_630_PARENT_INPUT_TARGETS.csv | true | parent input targets | false |
| SRC631_5 | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | true | R10 c_g projection smoke runner | false |
| SRC631_6 | 627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md | true | c_g zero proof attempt | false |
| SRC631_7 | 626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md | true | quotient-invariant matter action signature attempt | false |
| SRC631_8 | scripts/Y5_R10_matter_frame_variation_cg_zero_or_source_test_charge_law.py | true | this checkpoint generator | false |

## Matter Frame Cases
| case_id | matter_frame | partial_X_g_m | matter_current | alpha_law | status | what_must_be_proven | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MF631_0_quotient_only | g_m = g_q[q(Phi),theta] | 0 | J_X=0 | alpha_MTS_R10(lambda)=0 | clean_zero_if_parent_signed | Xhat is vertical and all matter measure/coframe/connection data descend to the quotient | false |
| MF631_1_conformal_representative | g_m = A_g(Xhat)^2 g_q | 2 c_g g_m at Xhat=0 where c_g=d ln A_g/dXhat | J_X = c_g T_m plus sign convention | alpha proportional to beta_source beta_test | conditional_two_leg_law | A_g is a parent-owned physical function rather than a forbidden representative choice | false |
| MF631_2_disformal_representative | g_m = A_g(Xhat)^2 g_q + B_g(Xhat) U_mu U_nu | 2 c_g g_m + b_g U_mu U_nu plus connection/normalization terms | J_X = c_g T_m + 0.5 b_g T^{mu nu} U_mu U_nu + ... | alpha receives Weyl plus disformal/profile terms | blocked_mixed_branch | whether disformal terms are absent, auxiliary, quotient-owned, or physical | false |
| MF631_3_explicit_mass_dependence | m_i=m_i(Xhat,theta) even if g_m descends | 0 but partial_X ln m_i may be nonzero | J_X = sum_i beta_i rho_i with beta_i=d ln m_i/dXhat | composition-dependent scalar charge unless beta_i is universal or zero | blocked_mass_channel | standard masses/constants must be quotient-owned or their Xhat dependence derived | false |

## Variation Derivation
| line_id | statement | equation | derivation_status | consequence | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| VD631_0_action | Start with a minimally-coupled matter action in its physical matter frame. | S_m = integral d^4x sqrt(-g_m) L_m(psi,D_m psi,g_m,m_i) | standard_variational_identity | all local coupling information enters through the Xhat dependence of g_m, D_m, and m_i | false |
| VD631_1_stress_variation | Define the stress tensor by varying the matter metric. | delta S_m = 1/2 integral sqrt(-g_m) T_m^{mu nu} delta g^m_{mu nu} + matter EOM terms | derived_identity_up_to_sign_convention | on matter equations of motion, Xhat couples through T_m^{mu nu} partial_X g^m_{mu nu} | false |
| VD631_2_general_current | Vary with respect to the normalized residual Xhat. | J_X = delta S_m/delta Xhat = 1/2 sqrt(-g_m) T_m^{mu nu} partial_Xhat g^m_{mu nu} + sqrt(-g_m) sum_i (partial_Xhat ln m_i) m_i n_i + ... | conditional_general_current | zero coupling requires every Xhat derivative in the matter frame and explicit matter constants to vanish or be pure gauge | false |
| VD631_3_conformal_current | For a pure conformal representative matter frame, the trace current is unavoidable unless c_g=0. | if g_m=A_g^2 g_q then partial_Xhat g_m=2 c_g g_m and J_X = sqrt(-g_m) c_g T_m | derived_conditional_theorem | ordinary nonrelativistic matter has T_m approximately -rho, so source and test bodies both carry scalar charge | false |
| VD631_4_zero_condition | The clean local-GR-safe branch is an exact matter-frame descent condition. | partial_Xhat g_m=0 and partial_Xhat ln m_i=0 and boundary_Xhat current=0 imply J_X=0 | proved_as_conditional_zero_lemma | if parent action signs this, c_g=0 and all R10/PPN/clock source currents vanish at leading order | false |
| VD631_5_nonzero_condition | If the conformal derivative survives, the finite force is naturally two-legged. | V_X(r) = - beta_s beta_t m_s m_t exp(-r/lambda_X)/(4 pi Z_eff r) times profile factors | derived_static_exchange_form | matching to Newton gives alpha_X = beta_s beta_t/(4 pi G_eff Z_eff) times profile factors | false |
| VD631_6_linear_row_interpretation | A linear c_g alpha row is only primitive if the source leg has already been absorbed into another factor. | alpha_linear=abs(c_g K_X Qbar_XH qbar_XT tau_R10/Z_eff) is shorthand, not the raw matter variation, unless K_X Qbar_XH qbar_XT contains beta_source | branch_resolution | future runners must record whether alpha is one-leg-compressed or two-leg-universal | false |

## Source-Test Charge Law
| charge_id | object | definition | source_leg | test_leg | observable_law | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q631_0_universal_weyl_charge | beta_i | beta_i = partial_Xhat ln m_i^eff = c_g for universal conformal matter-frame response | beta_source=c_g times composition/profile factor | beta_test=c_g times composition/profile factor | alpha_X proportional to c_g^2 for universal source/test coupling | conditional_derived | false |
| Q631_1_quotient_zero_charge | beta_i | beta_i=0 if matter frame and particle masses are quotient-only | 0 | 0 | alpha_X=0 | conditional_zero_lemma | false |
| Q631_2_composition_channel | beta_i | beta_i=c_g+partial_Xhat ln m_i^bare plus binding-energy sensitivities | composition-weighted beta_source | composition-weighted beta_test | WEP/composition tests become coupled to R10 rather than optional | blocked_until_mass_constants_owned | false |
| Q631_3_disformal_charge | beta_i plus b_g velocity/stress projection | J_X includes 0.5 b_g T^{mu nu} U_mu U_nu if disformal matter-frame terms survive | stress/profile source leg | stress/profile test leg | not reducible to pure conformal alpha without extra projection terms | blocked_mixed_branch | false |

## Coupling Branch Resolution
| branch_id | branch | derived_result | selected_for_claim | why | next_test | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BR631_0_zero | quotient-only matter descent | J_X=0 | false | conditional zero lemma is proven, but parent action has not signed the matter frame | derive or source explicit parent matter frame | false |
| BR631_1_two_leg | universal conformal matter-frame coupling | J_X=c_g T_m and alpha_X proportional to c_g^2 times profile/normalization factors | false | this is the natural finite branch from variation, but c_g,Z_eff,lambda_X,profiles are not sourced | build two-leg nonclaim envelope runner and parent selector | false |
| BR631_2_linear_compressed | linear alpha with source leg absorbed | alpha_linear is allowed only as shorthand after defining where beta_source went | false | using it as primitive would hide a matter leg | require metadata: one_leg_compressed=true/false and source_leg_owner | false |
| BR631_3_disformal_or_mass | extra representative/mass channel | J_X receives stress/mass-sensitivity terms beyond c_g T | false | would make local tests harder, not easier, unless parent action forbids it | prove no disformal/mass Xhat channel or add separate blocked projection schema | false |

## R10 Alpha Translation
| translation_id | lambda_value | lambda_units | review_alpha_bound | if_linear_compressed_bound | if_two_leg_unit_profile_bound_on_abs_c_eff | physical_interpretation | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AT631_0 | 5.9e-06 | m | 897932.29287 | 897932.29287 | 947.592894058 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_1 | 1e-05 | m | 41538.8057283 | 41538.8057283 | 203.810710534 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_2 | 2e-05 | m | 183.665577985 | 183.665577985 | 13.552327401 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_3 | 3.86e-05 | m | 0.991537244704 | 0.991537244704 | 0.995759631992 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_4 | 5.6e-05 | m | 0.300428094431 | 0.300428094431 | 0.548113213151 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_5 | 0.0001 | m | 17.5879273456 | 17.5879273456 | 4.19379629281 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_6 | 0.0003 | m | 0.215104553289 | 0.215104553289 | 0.463793653783 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_7 | 0.000608 | m | 0.00234466430052 | 0.00234466430052 | 0.048421733762 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |
| AT631_8 | 0.001 | m | 0.00998933369038 | 0.00998933369038 | 0.099946654223 | two-leg conformal branch pressures c_eff by sqrt(alpha_bound); linear branch pressures the already-compressed product directly | nonclaim_review_candidate_pressure_only | false |

## c_g Zero Gate
| gate_id | zero_requirement | derived_status | currently_signed | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ZG631_0_metric | partial_Xhat g_matter = 0 | sufficient_component | false | trace current c_g T_m survives | false |
| ZG631_1_connection_measure | partial_Xhat measure/coframe/connection matter data = 0 or pure gauge | required_component | false | coupling leaks through rods/clocks/derivatives | false |
| ZG631_2_masses_constants | partial_Xhat ln m_i and constants/sensitivities = 0 or quotient-owned | required_component | false | composition-dependent WEP/clock channel | false |
| ZG631_3_boundary | vertical boundary current has no local/R10 projection | required_component | false | edge current fakes finite source leg | false |
| ZG631_4_total | all zero gates signed by parent action | not_passed | false | finite two-leg/source-test law remains live | false |

## Next Selector Contract
| contract_id | required_output | must_distinguish | pass_condition | blocked_if | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NS631_0_parent_selector | choose or derive the actual parent matter-frame class | quotient-only vs conformal representative vs disformal/mass channel | one branch is selected by parent action text/equations, not by convenience | matter frame remains implicit | false |
| NS631_1_two_leg_runner | nonclaim runner for alpha proportional to beta_source beta_test | linear compressed product from true two-leg scalar exchange | metadata records source_leg_owner,test_leg_owner,Z_eff,lambda_X,profile | any owner is MISSING_PARENT_INPUT | false |
| NS631_2_cross_arena_charge | same beta_i/c_g branch mapped to R10, WEP, PPN, clock, and orbital rows | universal trace coupling from composition-dependent mass/constant coupling | one charge law gives all arena projections or explicitly blocks them | R10 is treated in isolation | false |

## Nonclaim Summary
| status | claim_ceiling | cg_zero_parent_signed | trace_current_derived | default_finite_branch | linear_formula_status | tightest_review_alpha_bound | tightest_two_leg_unit_profile_bound | tightest_lambda_m | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_matter_frame_variation_derived_conditional_two_leg_law_cg_zero_not_signed | conditional_matter_variation_only_no_R10_WEP_PPN_clock_or_local_GR_pass | false | true | two_leg_universal_unless_source_leg_absorbed | compressed_not_primitive | 0.00234466430052 | 0.048421733762 | 0.000608 | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |

## Decision
| decision_id | decision | meaning | status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D631_0_main_verdict | Y5_R10_matter_frame_variation_derived_conditional_two_leg_law_cg_zero_not_signed | the matter-frame variation gives a real conditional theorem: zero iff matter frame descends; otherwise a trace/source-test law | derivation_progress_not_claim | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |
| D631_1_cg_zero | c_g_zero_conditional_not_parent_signed | c_g=0 follows from partial_Xhat matter data all vanishing, but that parent selector is still missing | blocked_for_claim | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |
| D631_2_two_leg | finite_universal_coupling_is_two_leg | if matter sees Xhat through a conformal frame, source and test both couple; alpha scales like c_g^2 times profiles | branch_resolution | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |
| D631_3_linear_row | linear_alpha_must_be_marked_source_absorbed | the previous linear formula is acceptable only as compressed notation with source-leg ownership metadata | schema_repair_required | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |
| D631_4_claim_ceiling | conditional_matter_variation_only_no_R10_WEP_PPN_clock_or_local_GR_pass | no local test pass follows until the parent matter-frame selector is derived | hard_guardrail | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md | false |

## Route Update
| route_id | allowed_after_631 | forbidden_after_631 | next_action |
| --- | --- | --- | --- |
| RU631_0_allowed | Use the conditional zero lemma: if all Xhat matter-frame derivatives vanish, c_g=0. | Claim c_g=0 before deriving the actual parent matter frame. | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md |
| RU631_1_allowed | Treat universal finite coupling as two-legged by default. | Use a primitive linear c_g R10 row without source-leg ownership metadata. | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md |
| RU631_2_allowed | Carry WEP/clock/PPN risk with any composition or mass channel. | Use R10 alone to bless a coupling branch. | 632-Y5-R10-parent-matter-frame-selector-or-two-leg-coupling-envelope-runner.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V631_0_source_paths_exist | pass | missing=0 |
| V631_1_prior_630_clean | pass | prior_rows=9;prior_fails=0 |
| V631_2_matter_frame_cases_complete | pass | frame_cases=4 |
| V631_3_variation_derives_trace_current | pass | variation_rows=7;trace_current=true |
| V631_4_two_leg_law_explicit | pass | charge_rows=4;two_leg_present=true |
| V631_5_zero_gate_not_passed | pass | zero_rows=5;total_status=not_passed |
| V631_6_R10_translation_numeric_nonclaim | pass | translation_rows=9;numeric_nonclaim=9 |
| V631_7_no_branch_claim_selected | pass | branch_rows=4;claim_rows=0 |
| V631_8_next_selector_contract_written | pass | selector_rows=3 |
| V631_9_no_local_claim | pass | c_g_zero=false;finite_numeric=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |
