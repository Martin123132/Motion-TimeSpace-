# 3434 - Source-Normalized Poisson Limit and First PPN Residual Stack

## Summary
- This checkpoint derives the clean part: in the public EH/Hilbert branch, the weak static 00 equation gives the standard Poisson coefficient.
- It also draws the hard line: a correct Poisson coefficient is not yet Newtonian mechanics unless the same `M_H_ref`, `tau`, source frame, Gauss surface, and Kepler readout are locked.
- Every non-EH/source-normalization residual is carried forward explicitly: `epsilon_mu`, `q_loc`, domain/projector, boundary, non-EH operators, range/radial hair, species/frame split, and second-order PPN source residue.
- Result: conditional Newton stack is cleaner, but current MTS is still nonclaim until residual rows are theorem-zero or score-ready.
- The next useful move is no longer another broad audit; it is making one high-leverage residual row executable or derived-zero.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| doc_3433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3433-Y5-R2FR-MHref-tau-source-normalization-lock-or-residual-vector-under-AX1090.md | True | M_H_ref/tau source-normalization handoff | False |
| source_lock_3433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv | True | source-lock theorem | False |
| epsilon_mu_3433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3433_EPSILON_MU_RESIDUAL_VECTOR.csv | True | epsilon_mu residual vector | False |
| newton_ppn_3433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3433_NEWTON_PPN_READOUT_GATES.csv | True | Newton/PPN gate split | False |
| next_3433 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3433_NEXT_TARGET.csv | True | 3434 target declaration | False |
| source_stack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | source-normalized Newton branch stack | False |
| source_residual_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | True | source-normalization residual vector template | False |
| constant_gm_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | True | constant GM residual runner input | False |
| local_gr_domain_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv | True | local GR residual vector rows | False |
| mu_extra_scorecard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv | True | mu_extra local bound scorecard | False |
| mu_extra_summary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv | True | mu_extra channel bound summary | False |
| qloc_operator_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv | True | q_loc PPN/R10 operator rows | False |
| qloc_bound_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv | True | q_loc residual bound pack | False |
| domain_ppn_3431 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_PPN_COEFFICIENT_UPDATE.csv | True | domain projector PPN coefficient rows | False |
| hidden_bound_3430 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv | True | hidden/projector bound rows | False |
| worldtube_510 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | True | worldtube source-measure theorem | False |
| source_measure_509 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | True | source-measure flux theorem | False |
| symbol_map_512 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv | True | local GR action symbol map | False |
| fixed_point_511 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv | True | local GR fixed-point conditions | False |
| constant_kappa_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_KAPPA_DECISION.csv | True | constant kappa route decision | False |
| mhref_candidates_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv | True | M_H_ref candidate/source row schema | False |

## Source-Normalized Poisson Limit Theorem
| theorem_id | statement | formula | status | condition_or_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PL3434_0_field_equation | In the public EH/Hilbert branch, the weak static 00 equation has the standard Poisson coefficient. | g_00=-1+2 Phi/c^2, T_00=rho_H c^2, kappa_eff=8 pi G0/c^4 => nabla^2 Phi=4 pi G0 rho_H | CONDITIONAL_EH_DERIVATION | EH-only exterior, same observed frame, constant universal kappa/G0, and Hilbert source density | False |
| PL3434_1_source_denominator | The source density must integrate to the same tau-normalized Hamiltonian/Hilbert denominator. | int_D rho_H d^3x = M_H_ref = c^-2(H_tau[S_outer]-H_ref) | CONDITIONAL_SOURCE_NORMALIZATION | source-specific M_H_ref row with tau/surface/reference/units/source path is missing | False |
| PL3434_2_residual_poisson | If source-normalization residuals survive, Poisson's equation carries explicit residual source terms. | nabla^2 Phi=4 pi G0 rho_H + S_epsilon_mu + S_q_loc + S_domain + S_boundary + S_nonEH | RESIDUAL_SOURCE_FORM | residual profiles and Green/source maps are missing | False |
| PL3434_3_gauss_surface | The Gauss monopole equals the same M_H_ref only if residual volume and boundary terms vanish or are bounded. | oint_S grad Phi.dS = 4 pi G0 M_H_ref + int_D S_res d^3x + oint_boundary R_boundary | CONDITIONAL_GAUSS_LOCK | PiM/source closure, boundary silence, radial/range residuals not closed | False |
| PL3434_4_newtonian_potential | Outside a compact source, the inverse-square potential follows only after the residual monopole and finite-range pieces vanish. | Phi(r)=-G0 M_H_ref/r + deltaPhi_res(r); deltaPhi_res=0 required for pure Newton | CONDITIONAL_INVERSE_SQUARE | range/radial/q_loc/domain/boundary maps are not zero or score-ready | False |
| PL3434_5_scope_limit | First-order Newton/Poisson success is not local GR; beta/gamma/preferred-frame rows remain separate obligations. | Poisson pass does not imply gamma-1=0, beta-1=0, alpha_i=0, xi=0 | NO_OVERCLAIM_RULE | second-order PPN source/operator stack still open | False |

## Kepler Readout Theorem
| theorem_id | statement | formula | status | condition_or_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| KR3434_0_slow_body | A slow test body reads the same potential only if its matter action uses the same observed metric/coframe. | S_test=-m int ds[g_obs] => d^2 x^i/dt^2=-partial_i Phi + O(v^2/c^2) | CONDITIONAL_GEODESIC_READOUT | same observed frame/source variation theorem remains unsigned | False |
| KR3434_1_kepler | Kepler/Newton GM follows when the Gauss monopole and orbital readout use the same M_H_ref. | a_r=-G0 M_H_ref/r^2; v^2 r=G0 M_H_ref | CONDITIONAL_KEPLER_LOCK | same M_H_ref/tau, no frame split, no range/radial hair | False |
| KR3434_2_residual_acceleration | Any source-normalization or finite-range residual becomes an orbital acceleration correction, not a hidden GM shift. | a_r=-G0 M_H_ref/r^2 - partial_r deltaPhi_res(r) + a_frame + a_q_loc | RESIDUAL_KEPLER_FORM | residual profiles, test-body coupling, and frame map missing | False |
| KR3434_3_calibration_split | A constant universal offset in GM can be calibrated away, but radial/range/species/time/frame derivatives cannot. | GM_obs=G0 M_H_ref(1+epsilon0) is harmless only if D_i epsilon0=0 for all local/source/range/frame directions | NO_CALIBRATION_CHEAT_APPLIED | derivative-zero identities or residual values missing | False |

## First PPN Residual Stack
| ppn_id | observable | source_formula | target | current_status | blocks_Newton | blocks_local_GR | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PPRS3434_0_gamma | gamma_minus_1 | gamma_minus_1 = R_gamma[c_nonEH_operator_vector, epsilon_mu, epsilon_q_loc, epsilon_boundary, epsilon_range] | 2.3e-5 dimensionless or derived zero | BLOCKED_MAP_VALUES_MISSING | False | True | False |
| PPRS3434_1_beta | beta_minus_1 | beta_minus_1 = R_beta[delta_beta_source, epsilon_radial_Meff, epsilon_boundary, epsilon_nonEH, epsilon_q_loc] | 7.8e-5 dimensionless or derived zero | BLOCKED_SECOND_ORDER_SOURCE_STACK | False | True | False |
| PPRS3434_2_alpha1 | alpha1 | alpha1 = W_domain_alpha1 epsilon_domain_vector + R_alpha1[q_loc/frame/vector] | 1e-4 dimensionless or derived zero | BLOCKED_DOMAIN_FRAME_VALUES_MISSING | False | True | False |
| PPRS3434_3_alpha2 | alpha2 | alpha2 = W_domain_alpha2 epsilon_domain_vector + R_alpha2[q_loc/frame/vector] | 2e-9 dimensionless or derived zero | BLOCKED_DOMAIN_FRAME_VALUES_MISSING | False | True | False |
| PPRS3434_4_alpha3 | alpha3 | alpha3 = W_domain_alpha3 epsilon_domain_flux + W_boundary_alpha3 epsilon_boundary_flux + R_alpha3[q_loc] | 4e-20 dimensionless or derived zero | BLOCKED_TIGHT_FLUX_ROW | indirect_source_normalization | True | False |
| PPRS3434_5_xi | xi | xi = W_domain_xi epsilon_domain_anisotropy + R_xi[boundary/projector/STF] | 4e-9 dimensionless or derived zero | BLOCKED_PROJECTOR_STF_ROW | False | True | False |
| PPRS3434_6_zeta_conservation | zeta_i / conservation rows | zeta_i = R_zeta[source nonconservation, q_loc exchange, boundary flux, frame split] | derived conservation or explicit row bounds | BLOCKED_SOURCE_CONSERVATION_MAP | if source flux changes M_H_ref | True | False |
| PPRS3434_7_R10_range | alpha(lambda) | alpha(lambda)=R_R10[epsilon_range, q_loc Yukawa source, nonEH operator, bulk_X] | real alpha_bound(lambda) curve or derived zero | BLOCKED_CURVE_AND_SOURCE_MAP_MISSING | if finite-range force survives | True | False |
| PPRS3434_8_Gdot | Gdot_over_G | dln mu_obs/dt = dln G_eff/dt + dln M_H_ref/dt + d epsilon_mu/dt | 9.6e-15 yr^-1 or derived zero | BLOCKED_TIME_DERIVATIVE_VALUES_MISSING | time-dependent GM | True | False |

## Residual Visibility Matrix
| residual_id | residual | enters_poisson | enters_kepler | enters_ppn | current_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RVM3434_0_epsilon_mu | epsilon_mu_residual_vector | S_epsilon_mu | delta GM_obs and derivative hair | beta/gamma/source-normalization rows | derive zero or fill vector values | False |
| RVM3434_1_q_loc | epsilon_q_loc_TGK_mass | effective source-exchange term | a_q_loc or finite-range tail | inverse-divergence PPN operator and R10 Yukawa row | needs I_div/source map or Hilbert-owner zero | False |
| RVM3434_2_domain | epsilon_domain_projector_abs | domain source-normalization term | frame/domain calibration split | alpha1/alpha2/alpha3/xi and R11 rows | operator-bound values or fixed-topological zero | False |
| RVM3434_3_boundary | epsilon_boundary_symplectic_abs | surface/source charge shift | boundary monopole/collar acceleration | alpha3, xi, Gdot, beta rows | boundary flux zero or coefficient values | False |
| RVM3434_4_nonEH_operator | c_nonEH_operator_vector | modified weak-field operator | non-inverse-square or changed coefficient | gamma/beta/R10/R11 | derive EH-only exterior or executable operator vector | False |
| RVM3434_5_frame_species_range | delta_frame_source + eta_source_AB + alpha(lambda) | source density/readout mismatch | composition/range/frame-dependent acceleration | WEP, clocks, preferred-frame, R10 | same-frame/source universality theorem or data-ready residual rows | False |

## Score Readiness Gate
| gate_id | item | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRG3434_0_poisson_derivation | EH Poisson coefficient | PASS_CONDITIONAL_EH_ONLY | source purity and same-frame M_H_ref row | False |
| SRG3434_1_kepler_readout | Kepler/inverse-square readout | FORMULA_READY_BLOCKED | same observed frame, no radial/range hair, no q_loc acceleration | False |
| SRG3434_2_ppn_stack | first PPN residual stack | STRUCTURED_NOT_SCORE_READY | operator maps and numeric/theorem-zero residual values | False |
| SRG3434_3_r10 | R10/fifth-force row | BLOCKED_CURVE_AND_SOURCE_MAP | real alpha(lambda) curve plus MTS alpha(lambda) source map | False |
| SRG3434_4_no_overclaim | Newton vs local GR distinction | PASS_GUARD | PPN still blocked even if Poisson is conditionally derived | False |

## PC3400 Newton/PPN Update
| pc_id | requirement | 3434_result | signed_part | open_part | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PC3400_Newton | source-normalized Newton/Poisson limit | EH/Hilbert Poisson coefficient and Kepler formula derived conditionally | Poisson coefficient in EH public branch | same M_H_ref/tau/source purity and residual-zero/value rows | CONDITIONAL_NOT_PROMOTED | False |
| PC3400_PPN | local GR/PPN through required order | first PPN residual stack assembled | no-overclaim guard and residual visibility | gamma/beta/preferred-frame/R10/Gdot rows not score-ready | BLOCKED_NOT_PROMOTED | False |

## Promotion Gates
| gate_id | gate | result | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG3434_0_poisson | Poisson coefficient derived | PASS_CONDITIONAL_EH_ONLY | PL3434_0 | False |
| PG3434_1_newton_claim | Newtonian mechanics derived for current MTS | BLOCKED | same M_H_ref/tau, residual-zero/value rows and Kepler readout remain unsigned | False |
| PG3434_2_ppn_stack | first PPN residual stack exists | PASS_STRUCTURE_VALUES_MISSING | PPRS3434 rows | False |
| PG3434_3_local_GR | local GR is derived | BLOCKED | PPN, q_loc, source-normalization, range/radial and second-order rows remain open | False |
| PG3434_4_empirical_ready | residuals can be tested numerically | FAIL_VALUES_MISSING | no q_loc/domain/boundary/R10/operator numeric maps | False |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3434_0_real_progress | Accept conditional EH Poisson derivation as real progress but not a current MTS claim. | it nails the coefficient route while preserving residual honesty. | attack residual-zero/value rows instead of re-deriving Poisson | False |
| DEC3434_1_no_newton_overreach | Do not call Newton recovered until Kepler readout and residual source purity are signed. | a correct Poisson coefficient can still have extra source, range, frame or q_loc hair. | derive same-frame slow-body readout or fill acceleration residuals | False |
| DEC3434_2_next | Next target should make one residual row score-ready rather than broaden the audit. | the symbolic stack is now coherent; empirical robustness needs executable rows. | build first score-ready residual runner for source-normalization/R10 or derive one zero theorem | False |

## Next Target
| target_doc | target_script | objective | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3435-Y5-R2FR-first-score-ready-source-normalization-residual-runner-or-zero-row-under-AX1090.md | scripts/Y5_R2FR_3435_first_score_ready_source_normalization_residual_runner_or_zero_row.py | choose one high-leverage residual row and make it score-ready: either theorem-zero it or create executable numeric/source inputs, starting with radial/range source hair or q_loc-to-R10 map | at least one residual row moves from FORMULA_READY_VALUES_MISSING to DERIVED_ZERO or SCORE_READY_NONCLAIM with real units and source path | False |

## Runner Nonclaim
| runner_id | purpose | rule | current_value | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN3434_0 | prevent Poisson-to-GR overclaim | Poisson coefficient does not promote Newton/PPN/local-GR unless source denominator, Kepler readout and residual rows close | claim_allowed=false | False |
| RUN3434_1 | keep residuals visible | epsilon_mu, q_loc, domain, boundary, nonEH, range and frame residuals must enter PPN/R10/source rows | residual_visibility_required=true | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3434_0_sources_exist | all cited source paths exist | True | 21/21 source paths exist |
| VAL3434_1_outputs_scoped | all outputs are in post-checkpoint-work | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| VAL3434_2_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false throughout generated rows |
| VAL3434_3_poisson_coefficient | EH Poisson coefficient derivation is present | True | conditional EH Poisson row present |
| VAL3434_4_residual_poisson | residual source terms are retained in Poisson equation | True | S_res terms visible |
| VAL3434_5_kepler_readout | Kepler readout is conditional and residual-corrected | True | conditional Kepler and residual acceleration rows present |
| VAL3434_6_ppn_stack | first PPN residual stack covers major rows | True | 9 PPN/residual rows |
| VAL3434_7_visibility_matrix | major residuals are mapped to Poisson/Kepler/PPN visibility | True | 6 visibility rows |
| VAL3434_8_no_overclaim_gate | Poisson-to-GR overclaim is explicitly blocked | True | Newton/GR distinction guard present |
| VAL3434_9_local_GR_blocked | local GR remains blocked until residual rows close | True | no local-GR claim promoted |
| VAL3434_10_next_target | next target makes one residual row score-ready or zero | True | 3435-Y5-R2FR-first-score-ready-source-normalization-residual-runner-or-zero-row-under-AX1090.md |
| VAL3434_11_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3434_12_overall | 3434 Poisson/PPN checkpoint is internally valid | True | PASS |

## Bottom Line
This is the clean boxing round: MTS can now say the EH/Hilbert branch has the right Poisson coefficient conditionally, but it cannot call the match won until source-normalization and PPN residuals are either zero or below bounds. No fitted `GM` carpet. No Poisson-to-GR overclaim.
