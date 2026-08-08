# 603 Y5 R10 parent primitive for N_D or unit-map channel fill

Generated: 2026-06-05T19:01:54.923066+00:00  
Status: `Y5_R10_ND_zero_nonzero_primitive_candidate_derived_conditionally_parent_kernel_and_normalization_missing`  
Claim ceiling: `conditional_ND_primitive_candidate_only_no_q_loc_zero_R10_WEP_PPN_or_local_GR_pass`  
Next target: `604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md`  
Run root: `runs/20260605-190154-Y5-R10-parent-primitive-for-ND-or-unit-map-channel-fill`

## Verdict
- We can sharpen `N_D`: the best selector primitive is the activation product `A_D=b_D c_D`, where `b_D` is the projected MTS boundary IR spectral factor and `c_D` is the non-exact relative boundary-class factor.
- This gives the right threshold-free branch logic: local projected gap or local trivial relative class makes `A_D=0`; coherent FLRW with an Ohmic projected bath and nontrivial expansion class gives `A_D>0`.
- The determinant current `J_C=det_h(P_coh Q) Omega_D/V_D` should not be the selector by itself; it is better treated as the cubic/double-zero memory amplitude once the branch is active.
- This is a conditional derivation, not a parent theorem. The decisive missing parent input is now the `P_MTS,D` boundary kernel block and the normalization that turns `A_D` into an action variable.

## Candidate Primitive
```text
b_D = lim_(omega->0+) rho[P_MTS,D B_D, P_MTS,D B_D](omega)/omega
c_D = || Pi_rel [J_B]_D ||_rel
A_D = b_D c_D
```

Then:

```text
local gap or local trivial class -> A_D = 0
FLRW Ohmic bath plus nontrivial class -> A_D > 0
```

This is the strongest version of `N_D` so far because it does not need an empirical threshold. But it still needs a parent-owned projector, pairing, and normalization.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md | True | immediate 602 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_602_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_602_BOUND_DOMAIN_SELECTOR_DERIVATION_ATTEMPT.csv | True | N_D missing primitive target |
| source-intake/mts_residuals/P8_Y5_R10_602_UNIT_MAP_FORK_STATUS.csv | True | unit-map fallback status |
| 308-selector-parent-theorem-attempt.md | True | spectral/topological selector b_D and c_D |
| 309-MTS-boundary-projector-contract-attempt.md | True | P_MTS boundary projector contract |
| 415-local-trivial-class-selector-theorem-attempt.md | True | local trivial class chain and blockers |
| 478-determinant-current-parent-ownership-or-demotion.md | True | det(Q_coh) shape support but ownership failure |
| 481-Qcoh-parent-projector-algebra-or-closure.md | True | trace projector algebra and parent ownership contract |
| 275-JC-three-form-memory-current-from-Q.md | True | J_C determinant memory current shape |
| 276-coherent-domain-projector-from-parent-variables.md | True | fixed-D coherent trace projector |
| 277-domain-free-boundary-Euler-equation.md | True | shape derivative/free-boundary route |
| 279-representative-selection-boundary-polarization-no-go.md | True | selector-function underdetermination no-go |
| 60-relative-cohomology-boundary-contract.md | True | relative local-zero/FLRW-nonzero contract |
| 61-bound-domain-boundary-theorem-attempt.md | True | volume-flow identity |
| 475-domain-selector-parent-action-clause-or-coefficient-fill.md | True | double-zero selector action clause |
| 476-double-zero-memory-coupling-origin-or-coefficient-runner.md | True | p>=2 requirement and coefficient fallback |
| scripts/Y5_R10_parent_primitive_for_ND_or_unit_map_channel_fill.py | True | this checkpoint generator |

## N_D Primitive Derivation Attempt
| primitive_id | candidate_object | mathematical_form | derivation_attempt | local_readout | FLRW_readout | result | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NDP603_0_boundary_spectral_factor | b_D | b_D = lim_{omega->0+} rho_MTS,D(omega)/omega, rho_MTS,D = rho[P_MTS,D B_D, P_MTS,D B_D] | Use a parent boundary spectral density after ordinary baths are removed by P_MTS,D. | closed/gapped projected local boundary channel gives b_D=0 | Ohmic coherent MTS boundary channel gives b_D=eta>0 | conditional_factor | P_MTS,D boundary kernel and ordinary/MTS orthogonality are not parent-derived | false |
| NDP603_1_relative_class_factor | c_D | c_D = \|\| Pi_rel [J_B]_D \|\|_rel | Use the norm or topological size of the non-exact relative boundary-memory class. | exact/trivial local relative class gives c_D=0 | nontrivial expansion relative class gives c_D>0 | conditional_factor | relative norm/topological pairing and local trivial class are not parent-derived | false |
| NDP603_2_activation_product | A_D = b_D c_D | A_D := b_D c_D | Take the product so either local gap or local trivial class switches the branch off, without introducing a fitted threshold. | if b_D=0 or c_D=0 then A_D=0 | if b_D>0 and c_D>0 then A_D>0 | zero_nonzero_primitive_conditionally_derived | A_D still needs parent units/normalization before it can be the action variable chi_D | false |
| NDP603_3_coherent_trace_factor | X_D | X_D := (1/3)<Tr_h Q>_D or equivalently the coherent trace/volume-flow scalar in the fixed-D branch | Use the unique trace projector from 481 and the fixed-domain coherent projection from 276. | stationary selected domain gives X_D=0 through the scalar volume-flow channel | coherent FLRW gives X_D nonzero and isotropic | fixed_D_algebra_pass | Q, D, P_coh, and local X_D=0 are not parent-owned | false |
| NDP603_4_cubic_memory_current | J_C | J_C = det_h(P_coh Q) Omega_D/V_D = (X_D/3)^3 Omega_D/V_D | Use the determinant of the coherent trace-projected load to supply the p=3/double-zero memory amplitude. | if X_D=0 then J_C=0 with first and second derivative zero in X_D | FLRW coherent trace gives nonzero cubic memory current | shape_derived_conditionally | parent ownership of Q_coh/P_coh/D and Ward stress accounting are missing | false |
| NDP603_5_best_combined_contract | N_D/A_D plus J_C | use A_D=b_D c_D as branch activation and J_C=det_h(P_coh Q) Omega_D/V_D as memory amplitude | Separate the selector question from the amplitude question: A_D decides zero/nonzero branch; J_C supplies the cubic/double-zero current once the branch is active. | A_D=0 and/or J_C=0 can silence the selected local scalar-domain branch | A_D>0 and J_C!=0 keep coherent cosmology active | best_candidate_contract_not_parent_theorem | normalization, boundary kernel block, local class theorem, domain selection, R11 and Bianchi debts remain | false |

## Zero-Nonzero Lemma
| lemma_id | statement | proof_status | proof_sketch | not_proved | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ZNL603_0_local_gap | projected local spectral gap implies b_D=0 | proved_from_premise | if rho_MTS,D(omega)=0 for 0<omega<omega_gap, then lim rho/omega=0 | the parent action forces the projected local gap | false |
| ZNL603_1_local_trivial_class | local exact/trivial relative class implies c_D=0 | proved_from_premise | Pi_rel kills exact relative representatives, so the projected class norm vanishes | the local branch is always exact/trivial in the parent theory | false |
| ZNL603_2_activation_zero | b_D=0 or c_D=0 implies A_D=b_D c_D=0 | algebra_pass | product activation has zero if either required local-silence premise holds | A_D normalization and action coupling are parent-owned | false |
| ZNL603_3_FLRW_active | Ohmic coherent bath plus nontrivial expansion class implies A_D>0 | conditional_pass | b_D=eta>0 and c_D>0 give A_D>0 | FLRW bath/class are parent-derived rather than imposed | false |
| ZNL603_4_double_zero_gate | A_D=0 with p>=2 selector gate gives local first-variation silence for the gated memory term | conditional_pass | delta(A_D^p L)=p A_D^(p-1)L delta A_D + A_D^p delta L, which vanishes at A_D=0 for p>=2 | p>=2 and A_D are both derived by a single deeper parent principle | false |
| ZNL603_5_counterexample_guard | without P_MTS,D, ordinary local baths can make b_D>0 and falsely activate N_D | guard_pass | generic local EM/matter/environmental spectral density need not be gapped in the unprojected channel | ordinary/MTS sector split by a parent boundary kernel | false |

## Parent Ownership Gate
| gate_id | required_parent_input | needed_for | current_status | failure_if_missing | next_repair | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| POG603_0_boundary_kernel_block | K_boundary block diagonalizes ordinary and MTS boundary channels | P_MTS,D and b_D | not_derived | ordinary local baths can activate the selector | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md | false |
| POG603_1_relative_topological_pairing | Pi_rel and the norm/topological pairing for [J_B]_D are parent-owned | c_D | not_derived | relative exactness/triviality remains closure | derive relative complex/topological pairing or retain residual | false |
| POG603_2_domain_selection | physical D and its boundary embedding are selected by Euler/topological law | A_D, X_D, J_C | not_derived | fixed-D algebra remains after-the-fact domain choice | bound-domain selector theorem or unit-map demotion | false |
| POG603_3_normalization | units and scale that convert A_D into chi_D without fitted threshold | action variable chi_D | open | A_D is zero/nonzero only, not a physical action coefficient | derive normalization from boundary kernel or make closure label explicit | false |
| POG603_4_Qcoh_parent_variable | Q_{mu nu} and P_coh are action/Noether variables with retained metric variation | X_D and J_C | algebra_known_parent_ownership_missing | det(P_coh Q) is shape support only, not theorem-zero | derive Q/P_coh owner or keep determinant branch closure-only | false |
| POG603_5_R11_Bianchi | R11/source-normalization and Ward/Bianchi stress ledgers are closed or scored | local-GR/PPN/R10 promotion | blocked | q_loc/source residuals can survive despite selector zero | R11 zero-or-fill plus local residual vector | false |

## Unit-Map Fork Status
| fork_id | route | status | why | required_next_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| UMF603_0_derivation_status | N_D derivation | partial_conditionally_sharpened | A_D=b_D c_D gives a clean zero/nonzero activation primitive if P_MTS and relative class are parent-owned | parent boundary kernel block for P_MTS,D | false |
| UMF603_1_unit_map_status | compact-shell unit map | still_deferred_but_closer | if the boundary kernel block cannot be derived next, the primitive route should demote and the unit-map channel should be chosen | R10 alpha(lambda), PPN vector, WEP, or clock channel plus units/coefficient | false |
| UMF603_2_no_score | local-bound evidence | no_claim | proxy 7.432631961576971e-06 still lacks channel conversion and A_D/J_C are not observable residuals | source-backed coefficient rows or theorem-zero certificates | false |

## Runner Update
| runner_id | previous_status | new_status | reason | still_needed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RU603_0_ND_primitive | N_D_parent_primitive_missing | zero_nonzero_candidate_A_D_written | A_D=b_D c_D is threshold-free and has the desired local-zero/FLRW-active branch logic | parent-owned P_MTS,D, relative class theorem, and normalization | false |
| RU603_1_cubic_memory_amplitude | det_Qcoh_shape_support_not_owned | retained_as_amplitude_not_selector_owner | J_C=det_h(P_coh Q) supplies p=3 shape once Qcoh/domain are owned, but it does not by itself select D | Q/P_coh/D parent ownership and Ward stress accounting | false |
| RU603_2_local_GR_stack | q_loc_and_R11_open | still_open | A_D zero would silence only the selector-gated scalar/domain term, not all local residuals | R11, source normalization, boundary charge, and q_loc exchange-owner terms | false |
| RU603_3_unit_map | fallback_unfilled | defer_one_more_step_or_demote_after_P_MTS | P_MTS boundary kernel is now the decisive derivation target | if P_MTS fails, choose physical unit-map channel and score closure | false |

## Decision
| decision_id | decision | meaning | claim_status | next_target |
| --- | --- | --- | --- | --- |
| D603_0_activation_primitive | accept A_D=b_D c_D as the best N_D candidate primitive | it is threshold-free and gives the right zero/nonzero branch logic when the spectral and relative factors are owned | conditional_candidate_only | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |
| D603_1_memory_amplitude | keep J_C=det_h(P_coh Q) as the amplitude/current clue | J_C gives the cubic/double-zero memory shape but does not solve selector/domain ownership | shape_support_only | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |
| D603_2_main_blocker | attack P_MTS boundary kernel next | without a parent ordinary/MTS sector split, A_D can be polluted by ordinary local baths | next_derivation_gate | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |
| D603_3_promotion | forbid local-GR/PPN/R10 promotion | N_D is not parent-normalized or action-owned; q_loc/R11/boundary debts remain open | forbidden | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |

## Route Update
| route_id | allowed_after_603 | forbidden_after_603 | next_action |
| --- | --- | --- | --- |
| RU603_0_allowed | use A_D=b_D c_D as the precise N_D theorem target | call A_D a parent action variable before P_MTS, c_D pairing, and normalization are derived | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |
| RU603_1_allowed | use J_C=det_h(P_coh Q) as the cubic memory amplitude clue | use determinant shape support as local-GR or alpha3 evidence | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |
| RU603_2_allowed | demote to unit-map scoring if P_MTS kernel block fails | continue stacking conditional selectors without choosing scoring fallback | 604-Y5-R10-PMTS-boundary-kernel-block-or-unit-map-channel-fill.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V603_0_source_paths_exist | pass | missing=0 |
| V603_1_prior_602_clean | pass | prior_rows=8;prior_failures=0;selector_rows=6;unit_rows=3 |
| V603_2_ND_activation_candidate_written | pass | A_D=b_D c_D zero/nonzero primitive present |
| V603_3_cubic_amplitude_kept_separate | pass | J_C determinant is amplitude/shape support, not selector ownership |
| V603_4_zero_nonzero_lemma_and_counterguard | pass | local_zero=True;FLRW=True;guard=True |
| V603_5_parent_blockers_visible | pass | P_MTS_blocker=True;normalization_open=True;local_GR_open=True |
| V603_6_unit_map_unfilled_and_no_claim_rows | pass | unit_unfilled=True;claim_rows=0 |
| V603_7_no_R10_or_local_GR_claim | pass | claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is a good squeeze. `N_D` is no longer a foggy placeholder; it has a concrete best candidate, `A_D=b_D c_D`. The remaining lock is brutally specific: prove the parent boundary kernel really splits ordinary bath channels from MTS memory channels. If that block structure fails, we stop calling this derivation and take the compact-shell unit-map scoring branch.
