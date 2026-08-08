# 1029 Y5 R10 c_g no-shadow-frame theorem or first numeric coupling row

**Status:** The no-shadow-frame theorem now has an exact conditional derivation: if the matter/readout frame either is not an independent parent argument, or factors only through the parent quotient `q`, then `c_g = Lie_vX ln A_g = 0` follows by chain rule. Current MTS still cannot claim this because the single-public-metric/no-extra-frame parent action clause and q-kernel ownership are not signed.

**Claim ceiling:** no `c_g=0`, finite-`c_g`, R10, WEP, clock, EM, PPN, orbital, local-GR/Newton, or source-zero pass is allowed from 1029.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1029_0_1028_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1028_NEXT_TARGET.csv | true | true | 1028 handoff to c_g/no-shadow frame target. |
| SRC1029_1_1028_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv | true | true | 1028 identifies no-shadow-frame as a missing theorem. |
| SRC1029_2_1028_bound_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv | true | true | 1028 c_g row and projection requirements. |
| SRC1029_3_1028_links | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1028_OBSERVABLE_LINK_MAP.csv | true | true | 1028 observable map for c_g. |
| SRC1029_4_943_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv | true | true | 943 no-shadow-frame rule as contract. |
| SRC1029_5_944_frame_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv | true | true | 944 c_g frame-leak bound row. |
| SRC1029_6_945_obs_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_945_OBS_E_FUNCTOR_AUDIT.csv | true | true | 945 representative Weyl counterexample. |
| SRC1029_7_945_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_945_KERNEL_TEST.csv | true | true | 945 kernel test for representative Weyl variation. |
| SRC1029_8_946_interface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv | true | true | 946 empirical c_g interface. |
| SRC1029_9_947_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv | true | true | 947 c_g parent value/projection gap. |
| SRC1029_10_951_provenance | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv | true | true | 951 finite coefficient provenance gate. |
| SRC1029_11_952_intake | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv | true | true | 952 coefficient intake template. |

## No-shadow-frame theorem audit
| theorem_id | claim | mathematical_form | derivation_step | current_status | missing_for_claim | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NST1029_0_define_shadow_frame | A shadow frame is an ordinary matter/readout frame not uniquely equal to the quotient-owned observed coframe. | e_m = A_g(Xhat) e_obs or g_m = A_g(Xhat)^2 g_obs, with c_g := Lie_vX ln A_g | definition | DEFINITION_SHARP | none at definition level | cannot name the retained frame coupling | false |
| NST1029_1_chain_rule_zero | If A_g factors only through q, vertical X cannot change it. | A_g(Phi)=Abar(q(Phi)) and Dq[v_X]=0 => Lie_vX ln A_g = D ln Abar[Dq(v_X)] = 0 | valid conditional proof | CONDITIONAL_THEOREM_VALID | parent-signed q-kernel and factorization of A_g through q | c_g must be retained as finite | false |
| NST1029_2_no_extra_frame_slot | The parent matter action contains no independent A_g(Xhat) frame slot. | Allowed[S_matter] = Sbar[Psi,e_obs(q(Phi)),omega[e_obs],theta(q)] and excludes Sbar[Psi,A_g(Xhat)e_obs,...] | action-domain exclusion | EXACT_CONTRACT_NOT_PARENT_SIGNED | single-public-metric/no-extra-frame parent action clause | universal scalar-tensor-like c_g remains legal | false |
| NST1029_3_observability_rule | Any frame that changes rods, clocks, masses, charges, free fall, or source readout is observable and must be in q or retained. | A_g affects experiment => A_g in Q_obs or coefficient row c_g retained | no-shadow-frame rule | CONTRACT_AVAILABLE_NOT_THEOREM | parent proof that observable frame data cannot be hidden in representative variables | field-renaming can hide the same coupling in masses, G_eff, or source normalization | false |
| NST1029_4_common_mode_limit | A constant common conformal normalization can be calibrated, but an X-dependent derivative is physical unless theorem-zero. | A_g=A_0 is unit/G calibration; Lie_vX ln A_g=c_g produces trace/source coupling when X varies | calibration separation | CONDITIONAL_PHYSICS_GUARD | source-measure and local weak-field projection that separates calibration from finite coupling | do not treat common WEP silence as c_g=0 | false |
| NST1029_5_matter_variation_trace | Finite c_g is the first-order matter-frame source coupling. | delta_X S_matter contains (1/2) sqrt(-g) T^{mu nu} delta_X g_m,mu nu ~ sqrt(-g) T c_g delta Xhat | local variation shape | FORMULA_SHAPE_VALID_SIGN_CONVENTION_TO_BE_FIXED | normalization of Xhat, sign convention, trace/source support, and arena projection | only absolute-bound envelope may be used | false |
| NST1029_6_verdict | c_g=0 no-shadow-frame theorem is derived in the current corpus. | NST1029_1 plus NST1029_2 plus NST1029_3 with parent signatures => c_g=0 | attempt verdict | FAIL_CURRENT_CLAIM | parent-signed single-public-metric/no-extra-frame clause and q-kernel ownership | stage c_g intake/provenance and tau projection rows | false |

## Counterexample ledger
| counterexample_id | weak_premise | construction | failure | required_repair | blocks_cg_zero | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CE1029_0_scalar_tensor_common_frame | universal matter coupling or WEP compliance | e_m=A_g(Xhat)e_obs with the same A_g for every ordinary species | composition WEP can be quiet while a common trace coupling/fifth-force remains | parent no-extra-frame theorem or numeric c_g/tau projections | true | false |
| CE1029_1_einstein_jordan_relabel | choose e_obs as the matter frame by notation | move A_g(Xhat) into masses, G_eff, or source normalization by a frame rename | c_g disappears from one ledger and reappears as b_A, b_alpha, or source-normalization residual | same-frame/source-measure ledger across matter, clocks, and active source | true | false |
| CE1029_2_constant_unit_absorption | common conformal factor is just units | A_g=A_0 is absorbable, but A_g(Xhat)=A_0 exp(c_g Xhat) is not if Xhat varies locally | calibration removes only the constant mode, not the derivative coupling | prove Lie_vX A_g=0 or bound c_g with profile/arena projection | true | false |
| CE1029_3_disformal_partner | killing the Weyl coefficient kills all frame leakage | g_m=A_g^2 g_obs+B_g(Xhat)U_muU_nu with c_g=0 but b_dis nonzero | preferred-frame/PPN/clock leakage survives the c_g branch | also close b_dis or retain it in the total qbarXT envelope | false | false |
| CE1029_4_boundary_source_support | matter-frame c_g=0 is enough for local GR | ordinary matter frame is clean but non-Hilbert current or support shift carries source coupling | local source normalization can remain non-GR even with c_g=0 | q_nonH and Delta_W_support theorem-zero or numeric bound rows | false | false |

## c_g intake template
| intake_id | coefficient_symbol | branch_type | candidate_value | units | candidate_source_path | source_row_id | derivation_status | comparison_bound | comparison_bound_source | claim_policy | ready_for_provenance_gate | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CGI1029_0_zero_theorem_branch | c_g | parent_zero_theorem | PARENT_SIGNED_TRUE_REQUIRED | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_PARENT_SIGNED_NO_SHADOW_FRAME_THEOREM | zero theorem must close before bypassing finite bounds | P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv | NONCLAIM_UNTIL_FULL_LOCAL_STACK_CLOSES | false | false |
| CGI1029_1_finite_cg_R10 | c_g | finite_value | MISSING_PARENT_INPUT | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_DERIVATION_STATUS | alpha_bound(lambda) / \|K_X(lambda) Qbar_XH tau_R10\| | P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv;P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv | NONCLAIM_UNTIL_CG_AND_TAU_R10_ARE_SOURCED | false | false |
| CGI1029_2_finite_cg_PPN_gamma | c_g | finite_value | MISSING_PARENT_INPUT | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_DERIVATION_STATUS | 2.3e-05 / \|M_gamma tau_PPN\| | P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv | NONCLAIM_UNTIL_RESPONSE_MATRIX_AND_GAUGE_ARE_SOURCED | false | false |
| CGI1029_3_finite_cg_PPN_beta | c_g | finite_value | MISSING_PARENT_INPUT | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_DERIVATION_STATUS | 7.8e-05 / \|M_beta tau_beta\| | P8_Y5_R10_946_CG_BA_BOUND_INTERFACE.csv | NONCLAIM_UNTIL_RESPONSE_MATRIX_AND_GAUGE_ARE_SOURCED | false | false |
| CGI1029_4_finite_cg_clock_common | c_g | finite_value_or_parent_zero | MISSING_PARENT_INPUT | dimensionless | MISSING_PARENT_SOURCE | MISSING_SOURCE_ROW_ID | MISSING_DERIVATION_STATUS | requires clock projection and separation from b_A/b_alpha | P8_Y5_R10_1028_OBSERVABLE_LINK_MAP.csv | NONCLAIM_COMMON_MODE_NOT_WEP_ONLY | false | false |

## Tau projection requirements
| projection_id | projection_symbol | arena | required_formula | required_inputs | current_status | source_hint | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TAU1029_0_R10 | tau_R10 | R10 short-range inverse-square/fifth-force | alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g plus retained marker/source tails | K_X(lambda);Qbar_XH;tau_R10;c_g;source/test material convention;lambda profile | MISSING_TAU_R10_AND_PARENT_CG | P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv:PFA947_0_R10_projection | false | false |
| TAU1029_1_PPN_gamma_beta | tau_PPN | PPN gamma/beta | gamma_minus_1,beta_minus_1 = response_operator(profile,gauge) * tau_PPN * c_g | M_gamma;M_beta;tau_PPN;gauge;weak-field order;disformal separation | MISSING_PPN_RESPONSE_MATRIX | P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv:PFA947_1_PPN_projection | false | false |
| TAU1029_2_clock_common | tau_clock | atomic clocks/readout | delta ln nu = tau_clock c_g + S_A b_A + S_alpha b_alpha after calibration separation | clock sensitivities;calibration convention;standalone c_g versus b_A/b_alpha split | MISSING_CLOCK_COMMON_MODE_PROJECTION | P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv:FMB1028_3_tau_clock | false | false |
| TAU1029_3_WEP_limit | tau_WEP_common_mode | WEP/composition | common c_g alone is not a differential WEP signal; WEP constrains differences or marker coefficients | material sensitivities and b_A/b_alpha rows if composition signal is used | WEP_ONLY_ZERO_FORBIDDEN | P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv:BI947_2_bA_WEP_alpha | false | false |
| TAU1029_4_orbital_source | tau_orbital | orbital/source support/local GR | source residual = tau_orbital c_g + q_nonH + Delta_W_support terms | source-measure selector;worldtube support;hidden-current silence;profile convention | MISSING_SOURCE_SUPPORT_PROJECTION | P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv:FMB1028_4_tau_orbital | false | false |

## Provenance dry run
| dryrun_id | coefficient_symbol | arena_or_branch | candidate_value | provenance_status | failure_reasons | score_eligible | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CGD1029_0_0_zero_theorem_branch | c_g | parent_zero_theorem | PARENT_SIGNED_TRUE_REQUIRED | rejected_missing_provenance | candidate_value_or_parent_signed_true;candidate_source_path;source_row_id;derivation_status | false | false | false |
| CGD1029_1_1_finite_cg_R10 | c_g | finite_value | MISSING_PARENT_INPUT | rejected_missing_provenance | candidate_value_or_parent_signed_true;candidate_source_path;source_row_id;derivation_status | false | false | false |
| CGD1029_2_2_finite_cg_PPN_gamma | c_g | finite_value | MISSING_PARENT_INPUT | rejected_missing_provenance | candidate_value_or_parent_signed_true;candidate_source_path;source_row_id;derivation_status | false | false | false |
| CGD1029_3_3_finite_cg_PPN_beta | c_g | finite_value | MISSING_PARENT_INPUT | rejected_missing_provenance | candidate_value_or_parent_signed_true;candidate_source_path;source_row_id;derivation_status | false | false | false |
| CGD1029_4_4_finite_cg_clock_common | c_g | finite_value_or_parent_zero | MISSING_PARENT_INPUT | rejected_missing_provenance | candidate_value_or_parent_signed_true;candidate_source_path;source_row_id;derivation_status | false | false | false |

## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CGATE1029_0_sources | all 1029 cited sources exist | true | validated by source register | false | false |
| CGATE1029_1_cg_zero | c_g=0 by parent no-shadow-frame theorem | false | NST1029_6 fails current claim because no-extra-frame parent clause is unsigned | false | false |
| CGATE1029_2_finite_cg_score | finite c_g row can be scored | false | candidate value, source path, derivation status, and tau projections are missing | false | false |
| CGATE1029_3_WEP_shortcut | WEP silence proves c_g=0 | false | a common Weyl coupling can be composition-blind while still producing fifth-force/PPN effects | false | false |
| CGATE1029_4_no_cancellation | unknown marker/source tails may cancel c_g | true | cancellation is forbidden; each component must be theorem-zero or separately bounded | false | false |
| CGATE1029_5_local_GR | local GR/Newton or R10/PPN pass is established | false | 1029 is theorem audit plus provenance intake only | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1029_0_derivation | The c_g zero theorem is mathematically clean under a single-public-metric/no-extra-frame parent clause. | if A_g is absent as an independent argument or factors through q, then verticality gives Lie_vX ln A_g=0 by chain rule. | try to derive the no-extra-frame parent clause from the action domain rather than assert it | false |
| DEC1029_1_current_status | Current MTS does not yet prove c_g=0. | representative Weyl frame, scalar-tensor common-frame, and frame-relabel counterexamples remain legal unless the parent action excludes them. | retain c_g as a nonclaim coefficient row | false |
| DEC1029_2_intake | The first c_g intake/provenance template is staged. | finite or zero-theorem branches now require candidate value, source path, source row id, derivation status, units, bound link, and tau projections. | do not score c_g until the intake and tau projection rows are real | false |
| DEC1029_3_next_target | Next target is single-public-metric parent action derivation or c_g provenance gate. | this is the exact parent clause needed to turn no-shadow frame from a closure into a theorem; failing that, c_g must enter a strict provenance gate. | 1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1029_SUMMARY | pass | 1029 c_g no-shadow theorem/provenance validation summary | 2026-06-14T06:17:56.075101+00:00 |
| V1029_0_sources_exist | pass | all cited source paths exist and expected needles are present | 2026-06-14T06:17:56.075054+00:00 |
| V1029_1_theorem_rows_complete | pass | no-shadow theorem audit covers definition, chain rule, no-extra-frame, observability, calibration, trace variation, and verdict | 2026-06-14T06:17:56.075066+00:00 |
| V1029_2_cg_zero_not_claimed | pass | c_g=0 remains nonclaim | 2026-06-14T06:17:56.075069+00:00 |
| V1029_3_counterexamples_complete | pass | counterexamples cover common frame, relabel, calibration, disformal partner, and source support | 2026-06-14T06:17:56.075071+00:00 |
| V1029_4_counterexamples_block | pass | common-frame counterexample blocks WEP-only c_g zero | 2026-06-14T06:17:56.075074+00:00 |
| V1029_5_intake_complete | pass | c_g intake rows cover zero theorem, R10, PPN gamma/beta, and clock common-mode branches | 2026-06-14T06:17:56.075076+00:00 |
| V1029_6_intake_nonclaim | pass | intake rows refuse placeholder promotion | 2026-06-14T06:17:56.075079+00:00 |
| V1029_7_tau_requirements_complete | pass | tau requirements cover R10, PPN, clocks, WEP limit, and orbital/source support | 2026-06-14T06:17:56.075081+00:00 |
| V1029_8_dryrun_rejects_placeholders | pass | provenance dry run rejects every placeholder c_g row | 2026-06-14T06:17:56.075084+00:00 |
| V1029_9_claim_gates_blocked | pass | all claim gates refuse promotion | 2026-06-14T06:17:56.075086+00:00 |
| V1029_10_no_cancellation_guard | pass | no-cancellation guard is active | 2026-06-14T06:17:56.075089+00:00 |
| V1029_11_decision_next | pass | decision ledger selects the 1030 target | 2026-06-14T06:17:56.075091+00:00 |
| V1029_12_next_target_written | pass | 1030 next target row is present | 2026-06-14T06:17:56.075093+00:00 |
| V1029_13_no_overclaim | pass | all generated rows remain valid_for_claim=false | 2026-06-14T06:17:56.075096+00:00 |
| V1029_14_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T06:17:56.075098+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | derive the parent action clause that ordinary matter has only one public metric/coframe argument and no A_g(Xhat) shadow-frame slot; if this fails, route c_g through the 1029/951 provenance gate with sourced tau_R10 and tau_PPN projections | matter action domain, observed coframe uniqueness, quotient functor, no extra frame argument, no field-rename hiding, c_g source path, tau_R10, tau_PPN, provenance gate | WEP-only proof, notation-only matter-frame choice, placeholder c_g values, cancellation with b_A/b_alpha/q_nonH/support, local-GR/R10/PPN claim, GitHub action, formalization-workbench edits | false |

