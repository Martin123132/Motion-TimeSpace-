# 3433 - MHref/Tau Source-Normalization Lock or Residual Vector

## Summary
- This checkpoint connects the previous `q_loc`, domain, boundary, PiM, and extra-sector residuals to the actual measured Newtonian source strength.
- The central rule is simple: MTS may use a measured constant `G0` only as a universal calibration, not as a bin for hidden derivative/source/range/frame/projector hair.
- The clean theorem is conditional: one observed `tau`, one fixed reference, one positive same-frame `M_H_ref`, closed projected Hilbert mass flux, constant kappa, and zero/bounded residuals imply protected Newtonian `GM`.
- Current MTS does not yet pass that lock; therefore `epsilon_mu` becomes the explicit residual vector for Newton/PPN/R10/clocks.
- This is the bridge from formal local-GR derivation to empirical scoring: no residual can disappear into a fitted `GM` unless it is universal and derivative-free.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| doc_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3432-Y5-R2FR-GammaKhat-q_loc-Hilbert-owner-or-residual-bound-under-AX1090.md | True | q_loc handoff | False |
| next_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_NEXT_TARGET.csv | True | 3433 target declaration | False |
| qloc_bound_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv | True | q_loc residual bound pack | False |
| qloc_operator_3432 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv | True | q_loc source-normalization operator handoff | False |
| mhref_candidates_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv | True | M_H_ref candidate rows | False |
| hpi_bounds_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv | True | Hamiltonian/PiM residual bounds | False |
| pc3400_3_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv | True | PC3400_3 lock audit | False |
| promotion_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_PROMOTION_GATES.csv | True | prior promotion gates | False |
| icomm_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3426_ICOMM_BOUND_ROWS.csv | True | PiM commutator bounds | False |
| bzero_3427 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv | True | boundary/reference bounds | False |
| hidden_bound_3430 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv | True | hidden/projector residual bounds | False |
| domain_bound_3431 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv | True | domain/projector operator bounds | False |
| source_measure_theorem_509 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | True | source-measure/Meff flux theorem | False |
| source_measure_residual_509 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv | True | source-measure residual map | False |
| worldtube_theorem_510 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | True | worldtube source-measure theorem | False |
| worldtube_proof_510 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv | True | worldtube proof sketch | False |
| constant_gm_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | True | constant GM residual runner input | False |
| constant_kappa_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_KAPPA_DECISION.csv | True | constant kappa decision | False |
| source_normalized_stack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalized_Newton_branch_STACK.csv | True | source-normalized Newton branch stack | False |
| source_residual_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | True | source-normalization residual vector template | False |

## MHref/Tau Source Lock Theorem
| theorem_id | statement | formula | status | condition_or_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SL3433_0_definition | Measured Newtonian source strength must be built from one same-frame Hamiltonian/Hilbert source denominator. | mu_obs := G0 M_H_ref (1+epsilon_mu), M_H_ref:=c^-2(H_tau[S_outer]-H_ref) | DEFINITION_LOCK_CANDIDATE | tau, surface, reference, units and source path must be fixed in one row | False |
| SL3433_1_same_tau | The time generator tau must be the same for source charge, clock normalization, orbital readout, and boundary subtraction. | tau_source=tau_clock=tau_orbit=tau_boundary=tau_obs | NECESSARY_LOCK_THEOREM | parent observed coframe/asymptotic normalization not fully derived | False |
| SL3433_2_flux_closure | If the projected Hilbert mass current is closed in the compact exterior, M_H_ref has no radial/time leakage. | d(Pi_M J_H)=0 and boundary flux=0 => partial_r M_H_ref=0 and partial_tau M_H_ref=0 | CONDITIONAL_FLUX_THEOREM | PiM chain-map, source-current descent, and boundary silence not all signed | False |
| SL3433_3_constant_kappa | A universal constant kappa can be absorbed into G0 only if it is source-blind, range-blind, frame-blind, and time/radius independent. | D_t kappa=D_r kappa=D_A kappa=D_lambda kappa=D_frame kappa=0 | CONDITIONAL_GLOBAL_CALIBRATION_RULE | topological kappa route is conditional/not adopted as current parent proof | False |
| SL3433_4_residual_identity | Any failure of the source lock enters an observable residual vector, not a hidden recalibration. | delta ln mu_obs = delta ln G_eff + delta ln M_H_ref + delta epsilon_mu + delta_frame + delta_range + delta_species | EXACT_ACCOUNTING_RULE | numeric values and row-specific maps missing | False |
| SL3433_5_newton_limit | Newtonian recovery follows only after EH/Poisson source coefficient, Gauss surface equality, and inverse-square readout share the same M_H_ref. | nabla^2 Phi=4 pi G0 rho_H, integral gradPhi.dS=4 pi G0 M_H_ref, a_r=-G0 M_H_ref/r^2 | CONDITIONAL_NEWTON_STACK | same-frame source/readout and residual-zero gates still open | False |
| SL3433_6_no_calibration_cheat | A single fitted GM can hide a universal constant offset, but it cannot hide derivative, range, species, frame, q_loc, boundary, or PPN hair. | constant epsilon0 may be absorbed; D_i epsilon_mu, alpha(lambda), eta_AB, beta/gamma/alpha_i/xi residuals cannot | NO_CHEAT_RULE | requires row-by-row residual vector before claims | False |
| SL3433_7_verdict | Current MTS has a legitimate EH/Hilbert denominator route but not a full source-normalization lock. | source_lock_current=false; epsilon_mu_residual_vector retained | PARTIAL_EH_ROUTE_RESIDUAL_VECTOR_REQUIRED | tau/reference/PiM/q_loc/domain/boundary/extra/source-frame rows | False |

## Same-Frame MHref/Tau Audit
| audit_id | lock | current_evidence | pass_now | blocker | residual_symbol | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SFA3433_0_tau_lock | tau observed-time generator | 3425 defines epsilon_tau_lock and partial tau naming | False | tau not parent-selected as one observed source/clock/orbit/boundary generator | epsilon_tau_lock | False |
| SFA3433_1_reference | fixed derivative-silent H_ref | 3427 fixed reference theorem helps under Hilbert-identity branch | False | reference functional/background class not parent-derived for full MTS branch | epsilon_reference | False |
| SFA3433_2_PiM_chain | PiM Hilbert-current chain map | 3426 identity branch can make I_comm=0 conditionally | False | identity/inclusion branch not parent-adopted across source readout | epsilon_PiM_comm | False |
| SFA3433_3_MHref_positive | positive same-frame M_H_ref denominator | 3425 EH candidate denominator exists | False | no source-specific claim-ready row with tau/surface/reference/units/source path | epsilon_HPiM_after_EH_lock | False |
| SFA3433_4_q_loc | q_loc contributes no extra source-normalization hair | 3432 decomposes q_loc residual | False | Hilbert owner and Khat identity are unsigned; bound values missing | epsilon_q_loc_TGK_mass | False |
| SFA3433_5_domain_boundary_extra | domain/projector/boundary/extra mass are zero or bounded | 3427/3430/3431 provide bound formulas | False | no numeric or parent-signed zero rows for domain/boundary/hidden totals | epsilon_domain_projector_abs + epsilon_boundary_symplectic_abs + epsilon_extra_mass | False |
| SFA3433_6_same_frame | source frame equals matter/clock/orbital frame | source-normalized Newton stack has SN0 as first rung | False | same observed coframe/source variation theorem not parent-derived | delta_frame_source | False |
| SFA3433_7_second_order | second-order PPN source closure | constant GM runner keeps beta source residue deferred | False | first-order Newton matching does not clear beta/gamma/PPN | delta_beta_source | False |

## Epsilon Mu Residual Vector
| row_id | residual | formula | target_or_bound | source_link | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EMU3433_0_constant_Geff | dln_Geff_dt / D_r G_eff / source/range/frame G_eff | delta ln G_eff contributes directly to delta ln mu_obs | Gdot 9.6e-15 yr^-1; range/source/frame rows require zero or bounds | P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | CONDITIONAL_KAPPA_ROUTE_NOT_CLAIMED | False |
| EMU3433_1_MHref_flux | dln_MHref_dt / radial M_H_ref leakage | delta ln M_H_ref = epsilon_tau_lock + epsilon_reference + epsilon_PiM_comm + epsilon_boundary_flux | mass conservation / beta / Gdot / radial hair locks | P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_2_q_loc | epsilon_q_loc_TGK_mass | epsilon_q_loc_TGK_mass <= sum(abs(QRB3432_0..QRB3432_5)) | PPN/R10/source-normalization after M_H_ref map | P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_3_domain_projector | epsilon_domain_projector_abs | epsilon_domain_projector_abs <= sum(abs(DPOB3431_0..DPOB3431_3)) | alpha1/alpha2/alpha3/xi/source-normalization | P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_4_boundary_reference | epsilon_boundary_symplectic_abs | (/B_zero/+/Delta_symp/+/Delta_H_ref/+/Phi_boundary/)/M_H_ref | orbital GM, clocks/Gdot, alpha3 | P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_5_hidden_extra | epsilon_hidden_total_abs / epsilon_extra_mass | absolute hidden/projector/extra-sector sum, no cancellations | local GR/Newton/PPN/R10/clocks/orbital | P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_6_species_frame | eta_source_AB + delta_frame_source | Delta_AB ln mu_obs=0 and Delta_frame ln mu_obs=0 only under same-frame universal source theorem | eta_source_AB <= 2.8e-15 or derived zero; frame residual below WEP/clock/operator locks | P8_source_normalization_residual_vector_TEMPLATE.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_7_range_radial | alpha(lambda) + partial_r_ln_mu_obs | finite-range/radial source hair cannot be absorbed into one local GM calibration | verified alpha(lambda) curve or no-finite-range theorem; radial no-hair/PPN bound | P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | FORMULA_READY_VALUES_MISSING | False |
| EMU3433_8_second_order | delta_beta_source and second-order PPN source residue | first-order Poisson success does not set beta-1 or nonlinear source terms to zero | beta_minus_1 <= 7.8e-5 or derived second-order closure | P8_source_normalization_residual_vector_TEMPLATE.csv | DEFERRED_BUT_BLOCKS_LOCAL_GR | False |

## Newton/PPN Readout Gates
| gate_id | gate | result | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| NPG3433_0_EH_subcharge | public EH/Hilbert subcharge exists | PASS_CONDITIONAL_SUBTHEOREM | 3425 public EH/Hilbert subcharge route | False |
| NPG3433_1_same_MHref | same M_H_ref controls source, metric 1/r, and orbit | FAIL_CURRENT | source-specific M_H_ref row missing | False |
| NPG3433_2_constant_universal_G | G/kappa is universal and derivative-free | CONDITIONAL_NOT_ADOPTED | constant kappa route exists only as conditional decision | False |
| NPG3433_3_Poisson | EH weak-field equation reduces to Poisson with Hilbert source | CONDITIONAL_EH_ONLY | source-normalized stack SN5, but residual source purity is not proven | False |
| NPG3433_4_inverse_square | same charge gives pure inverse-square orbital readout | NOT_DERIVED | SN9 and finite-range/radial rows remain open | False |
| NPG3433_5_PPN | PPN beta/gamma/preferred-frame rows are controlled | BLOCKED | domain/q_loc/boundary/source-normalization rows missing values | False |

## PC3400 Source-Coupling Update
| pc_id | requirement | 3433_result | signed_part | open_part | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PC3400_3 | H_tau/PiM/M_H_ref source denominator lock | same-frame theorem and epsilon_mu residual vector written | EH/Hilbert subcharge route remains conditionally valid | tau/reference/PiM/source-specific M_H_ref row not parent-signed | PARTIAL_NOT_PROMOTED | False |
| PC3400_4 | no extra compact-source mass | q_loc/domain/boundary/hidden residuals are now explicitly injected into epsilon_mu | no calibration-cheat rule prevents hiding these channels in fitted GM | zero certificates or numeric bounds missing | PARTIAL_NOT_PROMOTED | False |

## Promotion Gates
| gate_id | gate | result | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG3433_0_source_lock_theorem | M_H_ref/tau source lock theorem exists | PASS_CONDITIONAL_THEOREM | SL3433 rows | False |
| PG3433_1_epsilon_mu_vector | source-normalization residual vector is assembled | PASS_SYMBOLIC_VALUES_MISSING | EMU3433 rows | False |
| PG3433_2_Newton | Newtonian source coupling is derived for current MTS | BLOCKED | same-frame M_H_ref/tau and residual-zero rows missing | False |
| PG3433_3_PPN | local GR/PPN is derived | BLOCKED | second-order PPN, q_loc, domain, boundary, source-normalization rows remain open | False |
| PG3433_4_score_ready | residual vector can be scored numerically | FAIL_VALUES_MISSING | no numeric M_H_ref/q_loc/domain/boundary/source maps | False |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3433_0_G_constant | Treat G0 as an allowed universal calibration only after derivative/source/range/frame hair is zero or bounded. | GR also uses a measured Newton constant, but it cannot hide local non-universal residuals. | separate constant offset from derivative/residual vector | False |
| DEC3433_1_MHref | Do not use bare rest mass as the source denominator. | the exterior charge must include Hilbert/Hamiltonian dressing and binding energy in the same frame. | fill source-specific M_H_ref row or keep epsilon_HPiM residual | False |
| DEC3433_2_next | Next route should derive the source-normalized Poisson limit with residual terms visible. | this connects field-theory source coupling to actual Newtonian mechanics without importing GR by assumption. | derive Poisson/Kepler stack or produce first score-ready residual runner | False |

## Next Target
| target_doc | target_script | objective | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3434-Y5-R2FR-source-normalized-Poisson-limit-and-first-PPN-residual-stack-under-AX1090.md | scripts/Y5_R2FR_3434_source_normalized_Poisson_limit_and_first_PPN_residual_stack.py | derive the source-normalized Poisson/Newton limit from the EH/Hilbert branch while carrying epsilon_mu/q_loc/domain/boundary residuals into the first PPN residual stack | Poisson coefficient and Kepler readout are derived conditionally, with every non-EH/source-normalization residual visible as a score-ready or blocked row | False |

## Runner Nonclaim
| runner_id | purpose | rule | current_value | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN3433_0 | prevent GM calibration cheat | only a universal constant offset may be absorbed into G0; derivative/source/range/frame/q_loc/domain/boundary terms must remain explicit | claim_allowed=false | False |
| RUN3433_1 | force same-frame denominator | Newton/PPN claims require one tau-normalized M_H_ref source denominator or an explicit epsilon_mu residual vector | epsilon_mu_vector_required=true | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3433_0_sources_exist | all cited source paths exist | True | 20/20 source paths exist |
| VAL3433_1_outputs_scoped | all outputs are in post-checkpoint-work | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| VAL3433_2_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false throughout generated rows |
| VAL3433_3_source_lock_theorem | M_H_ref/tau source lock theorem exists | True | source-normalized Newton theorem present as conditional stack |
| VAL3433_4_no_calibration_cheat | GM calibration cheat is explicitly forbidden | True | constant offset separated from derivative/range/source hair |
| VAL3433_5_locks_not_promoted | same-frame locks are not falsely promoted | True | all same-frame locks remain unsigned |
| VAL3433_6_epsilon_mu_vector | epsilon_mu residual vector covers major source-normalization channels | True | 9 epsilon_mu rows |
| VAL3433_7_newton_ppn_gates | Newton and PPN gates are separated | True | Poisson conditional and PPN blocked rows present |
| VAL3433_8_pc3400_updates | PC3400 source-coupling updates exist | True | PC3400_3 and PC3400_4 updated as partial |
| VAL3433_9_local_GR_blocked | local GR remains blocked until residual rows close | True | no local-GR claim promoted |
| VAL3433_10_next_target | next target attacks Poisson/PPN source-normalized readout | True | 3434-Y5-R2FR-source-normalized-Poisson-limit-and-first-PPN-residual-stack-under-AX1090.md |
| VAL3433_11_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3433_12_overall | 3433 M_H_ref/tau source-normalization checkpoint is internally valid | True | PASS |

## Bottom Line
This is a proper engineering lock: `G` can be measured, but it cannot be used as a carpet. If q_loc/domain/boundary/hidden/source-frame residuals exist, they must show up in `epsilon_mu`, PPN, R10, clocks, or orbital rows. That keeps the route to Newton/GR honest.
