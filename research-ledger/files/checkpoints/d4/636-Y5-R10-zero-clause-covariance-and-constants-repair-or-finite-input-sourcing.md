# 636 Y5 R10 zero clause covariance and constants repair or finite input sourcing

Status: `Y5_R10_covariance_no_shadow_repair_contract_written_constants_and_parent_inputs_still_block_claim`  
Claim ceiling: `repair_contract_and_finite_input_sourcing_only_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md`

## Verdict
- This checkpoint improves the zero branch: covariance is no longer vague once `q` is required to be equivariant and `Obs` natural.
- The no-shadow-frame rule is now a sharper observable-completeness gate: anything that changes ordinary matter is either quotient-owned or a finite coupling, not hidden.
- The route still does **not** close because the parent action has not derived `q/Obs`, and EM/particle/clock/material constants remain live coupling channels.
- Therefore `c_g=0` is still not claimed; the finite branch remains pressure-only until beta/Z/lambda/tau inputs are sourced.

## Source Register
| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC636_0 | 635-Y5-R10-zero-clause-consistency-review-or-two-leg-numeric-input-runner.md | true | immediate 635 checkpoint | false |
| SRC636_1 | source-intake/mts_residuals/P8_Y5_BRR545_635_VALIDATION.csv | true | 635 validation gate | false |
| SRC636_2 | source-intake/mts_residuals/P8_Y5_R10_635_ZERO_CLAUSE_CONSISTENCY_REVIEW.csv | true | 635 zero-clause consistency blockers | false |
| SRC636_3 | source-intake/mts_residuals/P8_Y5_R10_635_ZERO_CLAUSE_ADOPTION_GATE.csv | true | 635 adoption gate | false |
| SRC636_4 | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_INPUT_STATUS.csv | true | 635 finite input missing ledger | false |
| SRC636_5 | source-intake/mts_residuals/P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv | true | 635 pressure-only two-leg runner | false |
| SRC636_6 | source-intake/mts_residuals/P8_Y5_R10_634_ZERO_BRANCH_PARENT_CLAUSE_DRAFT.csv | true | 634 proposed quotient-only parent clause | false |
| SRC636_7 | source-intake/mts_residuals/P8_Y5_R10_634_ZERO_CLAUSE_CONSEQUENCE_CHAIN.csv | true | 634 conditional consequence chain | false |
| SRC636_8 | source-intake/mts_residuals/P8_Y5_R10_632_TWO_LEG_ENVELOPE_RUNNER.csv | true | 632 two-leg envelope source | false |
| SRC636_9 | 241-C-silence-screening-or-parent-selection-theorem.md | true | conformal/source-frame warning | false |
| SRC636_10 | 360-universal-matter-coupling-theorem-attempt.md | true | universal matter coupling attempt | false |
| SRC636_11 | 565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md | true | vertical observation theorem ingredient | false |
| SRC636_12 | 566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md | true | no-marker primitive quotient ingredient | false |
| SRC636_13 | source-intake/external_papers/Andersen_2026_phase_current_CHARGE_CONTRACT.csv | true | EM/charge compatibility warning | false |
| SRC636_14 | scripts/Y5_R10_zero_clause_covariance_and_constants_repair_or_finite_input_sourcing.py | true | this checkpoint generator | false |

## Covariance Repair Lemma
| lemma_id | object | repair_statement | local_zero_use | closes_635_blocker | remaining_gap | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CV636_0_parent_quotient_equivariance | q: Phi_parent -> Q_obs | q must be a parent-defined quotient map equivariant under diffeomorphism, local Lorentz, and internal gauge actions: q(F.Phi)=F_Q.q(Phi). | if v_X in ker(Dq)_Phi, then Dq_Phi[v_X]=0 in every representative because equivariance carries zero to zero | covariance_if_parent_action_supplies_q | q is still a selector contract, not derived from the parent action | true | false |
| CV636_1_observable_functor_naturality | Obs: Q_obs -> E_obs | Obs must be a natural observable functor: Obs(F_Q.Q)=F_E.Obs(Q), with observed coframe/metric/connection built only from Q_obs. | partial_X e_obs = DObs_Q(Dq[v_X]) = 0 for vertical local Xhat directions | covariance_if_Obs_is_parent_defined | Obs is not yet constructed from primitive MTS variables | true | false |
| CV636_2_matter_action_descent | S_matter | ordinary matter action must descend: S_m[Phi,Psi,theta]=Sbar_m[Obs(q(Phi)),Psi,theta], up to Ward/exact boundary terms. | delta_v S_m = (delta Sbar_m/dE_obs) DObs(Dq[v]) + (partial Sbar_m/partial theta_A) delta_v theta_A, so the matter current vanishes only if theta_A is also vertical-silent | links_covariance_to_constants | constant ownership is the remaining live channel | true | false |

## No Shadow Frame Gate
| gate_id | rule | effect_on_shadow_frames | status | remaining_gap | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NS636_0_observable_completeness | any field/function that changes ordinary rods, clocks, masses, charges, or free-fall is an ordinary observable and must factor through Q_obs | a hidden A_g(Xhat), B_g(Xhat), or material-frame map either factors through q or violates the definition of ordinary observed geometry | candidate_repair_contract | requires parent action to prove Q_obs is complete, not merely declared complete | true | false |
| NS636_1_forbidden_representative_channel | representative-only Xhat dependence may remain in gravitational/effective sectors, but it cannot enter ordinary matter preparation variables | prevents a killed fifth-force leg from reappearing as mass normalization, clock normalization, or source geometry | candidate_repair_contract | must be checked against EM, particle, time, and material-composition sectors | true | false |
| NS636_2_honesty_test | if a proposed extra frame affects an experiment, it is not hidden; it is either quotient-owned or finite-coupled | turns no-shadow-frame from policy into a falsifiable classification test | useful_gate_not_theorem | classification is ready, source derivation is not | true | false |

## Constant Ownership Audit
| constant_id | sector | symbol_or_family | required_ownership | zero_clause_condition | audit_status | failure_mode | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CA636_0_c_light | geometry/clocks | c | causal-cone/observed-geometry quotient data | no independent partial_Xhat c after units and observed metric are fixed | candidate_silent_if_E_obs_parent_owned | disformal shadow cone creates clock/PPN residuals | true | false |
| CA636_1_em_charge | EM/charge | e, alpha_EM, gauge coupling | quotient/topological/representation data, not a smooth material scalar e(Xhat) | partial_Xhat alpha_EM=0 or variation is topological/integer and not a fifth-force scalar | open_blocker | clocks, spectra, WEP composition, and charge-sector work reopen the coupling | true | false |
| CA636_2_particle_masses | particle/matter | m_A, Yukawa data, binding energies | fixed matter representation or quotient-owned low-energy parameter | partial_Xhat ln m_A=0 for all ordinary species or universal absorbed unit change with no composition residue | open_blocker | composition-dependent scalar charge gives WEP and clock signals | true | false |
| CA636_3_clock_transitions | time/clocks | nu_clock, Rydberg, nuclear transition data | derived from quotient-owned EM/mass/nuclear parameters | partial_Xhat ln nu_clock=0 after all underlying constants are audited | open_blocker | clock drift appears even when direct metric coupling is zero | true | false |
| CA636_4_material_labels | composition/source preparation | species label A, isotope fraction, source density normalization | matter representation/preparation data independent of vertical representative choice | delta_Xhat theta_A=0 for source and test bodies | open_blocker | source/test beta legs survive as preparation-dependent charges | true | false |
| CA636_5_Newton_G_measured | local gravity/operator | G_N, GM, source normalization | operator/metric normalization after EH/PPN reduction, not matter fifth-force coupling | no Xhat-dependent source normalization remains after quotient and boundary terms | open_blocker | measured GM carries hidden source-normalization residual even if c_g=0 | true | false |

## Zero Branch Repair Status
| repair_id | 635_blocker | 636_result | why_not_closed | next_requirement | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RS636_0_covariance | CR635_1_covariance | repair_contract_written | equivariance/naturality conditions are stated but not derived from a parent action | construct q and Obs from parent variables and symmetry group action | true | false |
| RS636_1_no_shadow_frame | CR635_2_no_shadow_frame | observable_completeness_gate_written | ordinary observable completeness is a strong parent principle, not yet a theorem | prove all matter-affecting frame functions factor through q or are excluded by variation | true | false |
| RS636_2_constants | CR635_3_constants | constant_ownership_audit_written | EM, particle masses, clock transitions, and source labels remain unsourced | derive zero constant variations or move them into finite beta/tau rows | true | false |
| RS636_3_boundary | CR635_4_boundary | not_repaired_this_checkpoint | boundary/projector/domain silence remains outside the covariance/constants pass | derive Ward/exact/no-hair boundary projection silence | true | false |
| RS636_4_gr_limit | CR635_5_gr_limit | not_repaired_this_checkpoint | killing direct matter coupling does not prove EH-only or PPN residual zero | derive local EH/PPN/operator reduction separately | true | false |

## Finite Input Sourcing Ledger
| input_id | symbol | required_if_zero_fails | preferred_source | current_source_status | units | blocks_arena | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FI636_0_beta_source | beta_source | source-body scalar charge beta_s = delta ln m_source / delta Xhat or delta S_source / delta Xhat | parent matter action variation with composition/source model | missing_parent_numeric | dimensionless | R10;WEP;orbital;source_normalization | false |
| FI636_1_beta_test | beta_test | test-body scalar charge beta_t including composition dependence | parent matter action variation for ordinary test material | missing_parent_numeric | dimensionless | R10;WEP;clock | false |
| FI636_2_Z_eff | Z_eff | quadratic normalization of the exchanged local Xhat/residual mode | second variation/Hessian of parent local action around local vacuum | missing_parent_numeric | action_normalization | all finite-coupling rows | false |
| FI636_3_MX_lambda | M_X^2, lambda_X | range of the exchanged mode, lambda_X=sqrt(Z_eff/M_X^2) after unit convention is fixed | parent Hessian plus local boundary/domain spectrum | missing_parent_numeric | m^-2;m | R10;orbital;PPN | false |
| FI636_4_profile_tau_R10 | profile_factor(lambda), tau_R10 | geometry/source-shape conversion between beta_s beta_t/Z_eff and alpha(lambda) | R10 apparatus/source geometry projection plus validated alpha(lambda) curve | pressure_only_from_632_635 | dimensionless | R10 scoring | false |
| FI636_5_cross_arena_tau | tau_WEP,tau_clock,tau_PPN,tau_orbital | same beta law mapped into each local arena | composition sensitivities, clock sensitivities, weak-field metric map, orbital source normalization | missing_arena_projection | dimensionless | WEP;clock;PPN;orbital | false |
| FI636_6_constant_sensitivities | d ln alpha_EM/dXhat, d ln m_A/dXhat, d ln nu/dXhat | constant-sector beta/tau bridge if constants are not vertical-silent | EM/particle/time-sector parent derivation | missing_parent_numeric | dimensionless_per_Xhat_unit | WEP;clock;EM | false |

## Adoption Gate
| gate_id | requirement | result | detail | adoption_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AG636_0_repair_attempted | covariance, no-shadow, and constants blockers attempted before finite scoring | pass | repair_rows=5;constant_rows=6 | false | false |
| AG636_1_parent_signed_zero_clause | q, Obs, matter descent, constant silence, boundary silence, and GR/operator limit are parent-signed | blocked | claim_blockers=5;open_constants=5 | false | false |
| AG636_2_finite_branch_scoreable | all beta/Z/lambda/profile/cross-arena finite inputs are numeric and source-owned | blocked | finite input ledger remains source-ready but non-numeric | false | false |
| AG636_3_claim_status | no local-test claim is made from a repair contract | pass | c_g_zero_claimed=false;finite_branch_scoreable=false;local_GR=false | false | false |

## Decision
| decision_id | decision | meaning | status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D636_0_main_verdict | Y5_R10_covariance_no_shadow_repair_contract_written_constants_and_parent_inputs_still_block_claim | the zero branch now has a sharper covariant/observable-completeness contract, but the parent action and constants still have to earn it | derivation_progress_not_claim | 637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md | false |
| D636_1_covariance | repair_contract_written_not_theorem | equivariance of q and naturality of Obs would stop gauge-fixed smuggling, but q and Obs are not yet derived | candidate_repair | 637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md | false |
| D636_2_constants | constants_are_the_live_coupling_channel | EM charge, masses, clocks, and source labels are the places Xhat can still sneak back into matter | core_blocker | 637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md | false |
| D636_3_finite_branch | finite_input_sourcing_ledger_ready_nonclaim | if the zero branch fails, the exact beta/Z/lambda/tau inputs needed for R10/WEP/PPN/clock/orbital pressure are now named | source_ready_not_scoreable | 637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md | false |

## Next Contract
| contract_id | required_output | success_condition | if_success | if_fail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NC636_0_parent_q_derivation | derive q and Obs from the parent action/symmetry structure, not from a post-hoc readout convention | equivariance and naturality are consequences of the parent variational setup | covariance/no-shadow blockers can be downgraded | zero clause remains closure-only | false |
| NC636_1_constant_ownership | prove or reject vertical silence for EM charge, masses, clock frequencies, species labels, and measured GM | all ordinary matter constants either factor through Q_obs/topological data or become finite beta/tau inputs | constants blocker closes or becomes numeric finite branch | local branch cannot claim WEP/clock silence | false |
| NC636_2_finite_numeric_inputs | fill beta_source,beta_test,Z_eff,M_X^2,lambda_X,profile_factor,tau_arena if zero branch cannot close | finite branch becomes scoreable without placeholder source legs | run private R10/WEP/PPN/clock/orbital pressure matrix | finite branch remains qualitative only | false |

## Nonclaim Summary
| status | claim_ceiling | covariance_contract_written | observable_completeness_gate_written | constants_closed | zero_clause_adopted | claim_blockers | open_constant_rows | finite_missing_rows | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_covariance_no_shadow_repair_contract_written_constants_and_parent_inputs_still_block_claim | repair_contract_and_finite_input_sourcing_only_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass | true | true | false | false | 5 | 5 | 6 | 637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md | false |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V636_0_source_paths_exist | pass | missing=0 |
| V636_1_prior_635_clean | pass | prior_rows=9;prior_fails=0 |
| V636_2_covariance_contract_complete_nonclaim | pass | covariance_rows=3;claim_rows=0 |
| V636_3_no_shadow_gate_complete_nonclaim | pass | no_shadow_rows=3;claim_rows=0 |
| V636_4_constants_audited_open_nonclaim | pass | constant_rows=6;open_constants=5;claim_rows=0 |
| V636_5_repair_status_blocks_claim | pass | repair_rows=5;claim_rows=0 |
| V636_6_finite_input_ledger_nonclaim_missing | pass | finite_rows=7;missing_finite=6;claim_rows=0 |
| V636_7_adoption_blocked | pass | gate_rows=4;adoption_allowed=false |
| V636_8_next_contract_written | pass | contract_rows=3 |
| V636_9_no_local_claim | pass | zero_clause_adopted=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |

## Interpretation
The clean mathematical shape is now visible: if ordinary matter is a functor of the observed quotient only, then vertical local representative motion has no matter current. That is the elegant route. The price is that constants cannot be allowed to ride along as hidden material markers. If charge, mass, clock frequency, or source normalization varies with `Xhat`, the zero branch fails and the theory must use the finite two-leg branch.
