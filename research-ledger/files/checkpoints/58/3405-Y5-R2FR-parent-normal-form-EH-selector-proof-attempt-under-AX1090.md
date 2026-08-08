# 3405 - Y5/R2FR parent normal-form EH selector proof attempt under AX1090

## Verdict

- 3405 makes a real derivation move: EH is selected from a two-derivative q-basic metric normal form, or equivalently from a massless spin-2 bootstrap with universal Hilbert source.
- This does not yet prove MTS owns EH. It reduces the hard target to parent Hessian/mode-rank extraction plus vertical-kernel silence.
- If the parent has only the long-range q-basic spin-2 metric and the leading local action is two-derivative, the local quotient action is `sqrt(-g)(C0+C1 R)+dB`, so EH follows.
- If that premise fails, the theory must carry a derivative-order/non-EH residual bound instead of claiming local GR.

## Parent Normal-Form Hypotheses
| hypothesis_id | statement | math_form | why_less_smuggly | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PNF3405_0_q_basic_observable | The local observable geometry is one q-basic metric/coframe, not a representative-dependent mixture. | Lie_v g_obs=0 for v in ker(Dq); S_matter and PPN readout use g_obs through O(U^2). | This is an MTS quotient statement, not a GR premise. | PARTIAL_NOT_SIGNED_THROUGH_OU2 | False |
| PNF3405_1_mode_rank | The compact local vacuum quotient has only the massless spin-2 observed metric as a long-range propagating mode. | rank phase space = 2 transverse-traceless modes; no scalar, vector, torsion, nonmetricity, memory, domain or bulk-X long-range charge. | This replaces 'assume EH' with a measurable/derivable mode-count target. | NOT_PARENT_SIGNED_R11_FAMILIES_RETAINED | False |
| PNF3405_2_two_derivative_normal_form | The leading local quotient action at the tested weak-field order is a two-derivative normal form. | L_eff=L_0+L_2+dB+L_{>=4}; L_{>=4} either zero or bounded by (ell_*/L)^2. | This gives an exact EH route if true and a quantitative residual route if false. | NEW_3405_SELECTOR_FORMULATION_NOT_PARENT_SIGNED | False |
| PNF3405_3_universal_Hilbert_source | The spin-2 mode couples to one descended Hilbert stress tensor before calibration. | delta S_matter/delta g_obs -> T_total; h_mn T_total^mn is the universal linear coupling. | This imports the self-coupling consistency theorem only after MTS owns the source. | STRONG_CONDITIONAL_FROM_3340_NOT_PARENT_SIGNED | False |
| PNF3405_4_vertical_kernel_silence | Vertical variables either are gauge/constraints or have a double-zero/gapped coupling to the local source/readout. | C_X(Phi0)=0, DC_X(Phi0)=0, M_X^2>0, and no source charge; otherwise keep residual R_X. | It blocks hidden scalar/vector/domain hair without pretending those sectors do not exist. | OPEN_FOR_ACTUAL_R11_ROWS | False |
| PNF3405_5_connection_normal_form | Independent connection variables are algebraic/gauge in the local branch or reduce to Levi-Civita. | delta_Gamma S gives nabla^Gamma g_obs=0 plus projective gauge; torsion/nonmetricity source/readout residuals vanish or are bounded. | It targets the connection leak directly instead of hiding it inside EH notation. | NOT_PARENT_SIGNED | False |
| PNF3405_6_fixed_boundary_topology | Boundary/reference/projector terms are fixed before readout and are exact, topological, or source-blind. | delta_g B_ref=0; B_zero_flux=0; Delta_symp=0; no post-readout subtraction. | It prevents boundary bookkeeping from acting as a hidden mass/PPN fit. | CONDITIONAL_STOKES_ROUTE_NOT_PARENT_SIGNED | False |
| PNF3405_7_common_branch_Gref | The same branch constant G_ref normalizes field equation, Hilbert/Pi_M source, and readout. | kappa_MTS=8*pi*G_ref/c^4; mu=G_ref M_H[Pi_M J_H]; U=mu/r. | It allows GR-style calibration of G while forbidding split-G closure tricks. | FIRST_ORDER_STAGED_SECOND_ORDER_OPEN | False |

## EH Selector Proof Attempt
| step_id | claim | derivation | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SEL3405_0_project_parent_to_quotient | Parent variation descends to an observed quotient action plus vertical residuals. | For q-basic variations delta g_obs=Dq delta Phi, delta S_parent=<E_obs,delta g_obs>+<E_vert,delta Phi_vert>. PNF3405_0 and PNF3405_4 set E_vert=0 or put it into R_vert. | selection can be done on S_eff[g_obs] with explicit residuals instead of on the full uncontrolled parent | DERIVED_CONDITIONAL | False |
| SEL3405_1_two_derivative_basis | The only local diffeomorphism-invariant scalar-density basis at derivative order <=2 is sqrt(-g)(C0+C1 R) plus a boundary term. | At zero derivatives the scalar is constant. At two derivatives, contractions of second derivatives of g reduce, up to a divergence, to the Ricci scalar; connection-first form gives the same normal form after imposing metric compatibility. | S_eff^{<=2}=int sqrt(-g)(C0+C1 R)+dB | DERIVED_MATH_NORMAL_FORM | False |
| SEL3405_2_field_equation | Variation of the two-derivative normal form gives EH field equations. | delta int sqrt(-g)R gives G_mn plus boundary; delta int sqrt(-g)C0 gives Lambda g_mn; fixed boundary/reference terms do not alter local equations. | E_mn=C1 G_mn - (C0/2) g_mn | DERIVED_MATH_NORMAL_FORM | False |
| SEL3405_3_source_coupling | Universal Hilbert coupling fixes the right-hand source without source-only weights. | PNF3405_3 makes h_mn couple to T_total^mn from the same descended action; Ward identity enforces common conservation with the left-hand tensor. | G_mn+Lambda g_mn=kappa_* T_total_mn plus explicit residuals | EXACT_IF_HILBERT_SOURCE_SIGNED | False |
| SEL3405_4_spin2_bootstrap_equivalence | The same result follows from massless spin-2 consistency: a two-derivative spin-2 field universally coupled to its Hilbert stress bootstraps to EH. | Linear gauge invariance requires conserved source coupling; iterating the spin-2 field's own stress-energy self-coupling gives the nonlinear Einstein tensor completion. | EH is selected by mode-count plus universal source, not by aesthetic preference | DERIVED_STANDARD_SELECTOR_IF_MODE_RANK_SIGNED | False |
| SEL3405_5_nonEH_survival | Every non-EH operator survives unless it is outside the two-derivative normal form, topological/boundary, vertical-silent, or quantitatively suppressed. | R^2, f(R), Weyl^2, scalar/vector, torsion/nonmetricity, nonlocal memory, domain/projector and bulk-X terms are not eliminated by covariance alone. | 3405 gives an exact selector only if PNF3405_1..6 are parent-signed; otherwise use residual bound law | OBSTRUCTION_DERIVED | False |

## Spin-2 Bootstrap Route
| route_id | requirement | test_or_derivation | if_passes | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SPIN3405_0_linear_mode | linearized observed geometry has only a massless spin-2 mode | show the parent Hessian around the local vacuum has TT metric kernel only; scalar/vector/connection/domain kernels are constrained or gapped | linear kinetic term is Fierz-Pauli up to normalization | NOT_YET_EXTRACTED_FROM_PARENT_HESSIAN | False |
| SPIN3405_1_gauge_identity | linearized gauge symmetry is the q-basic diffeomorphism symmetry | derive delta h_mn=partial_m xi_n+partial_n xi_m from quotient redundancy rather than assuming GR diffeomorphism | source must be conserved and coupled universally | PLAUSIBLE_FROM_Q_BASIC_BRANCH_NOT_SIGNED | False |
| SPIN3405_2_self_coupling | the spin-2 field couples to the total Hilbert stress including its own stress | use the 3340 Hilbert source clause and parent Noether identity to forbid separate source weights | nonlinear completion is EH at two derivatives | CONDITIONAL_FROM_3340 | False |
| SPIN3405_3_MTS_gain | MTS owns the mode-rank and source-universality premises | prove vertical kernel silence and common Hilbert source from parent action | EH selector becomes an MTS theorem, not an imported GR axiom | THIS_IS_NOW_THE_CENTRAL_TARGET | False |

## Derivative-Order Residual Bound
| bound_id | operator_class | normal_form_status | residual_law | needed_inputs | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DOB3405_0_four_derivative_metric | R2/fR/Ricci2/Weyl2 | outside exact two-derivative selector | /E_4///E_EH/ <= C_4*(ell_4/L_local)^2 after source/readout projection | C_4 sign/norm; ell_4 or mass scale; weak-field projection to beta/gamma/R10; boundary status | BOUND_ROUTE_IF_NOT_ZERO | False |
| DOB3405_1_extra_fields | scalar/vector/bulk-X/memory/domain | outside metric-only spin-2 selector unless constrained/gapped | /E_X///E_EH/ <= /Q_X/*/K_X//(M_X^2 L_local^2) + contact/readout terms | Q_X,K_X,M_X^2, source charge, local profile, PPN/fifth-force projection | BOUND_ROUTE_IF_DOUBLE_ZERO_FAILS | False |
| DOB3405_2_connection | torsion/nonmetricity/metric-affine | outside Levi-Civita normal form unless algebraic/gauge | /E_conn///E_EH/ <= C_T/T//L_local + C_Q/Q//L_local plus clock/light/source maps | connection field equations, hypermomentum/source coupling, clock/light/PPN projection | BOUND_ROUTE_IF_LC_PROOF_FAILS | False |
| DOB3405_3_boundary_projector | boundary/reference/projector/domain stress | silent only if exact/topological/fixed before readout | /E_boundary///E_EH/ <= /B_zero_flux/+/Delta_symp/+/projector_stress_beta_equiv/ | fixed annulus, reference variation, projector stress, source-worldtube matching | BOUND_ROUTE_IF_STOKES_ZERO_FAILS | False |

## Non-EH Operator Triage
| operator_id | operator_family | selector_bucket | current_evidence | current_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| B530_0_source_AB | source_normalization_operator | requires same-source/readout ownership or q_loc vector split | A_source and B_source missing; measured-GM chain unfilled | unfilled | False | False |
| B530_1_R2_fR_scalar | R2_fR_scalar_mode | killed by exact two-derivative normal form; otherwise four-derivative bound | R11 skeleton/template only | template_only | False | False |
| B530_2_Ricci_Weyl | Ricci_Weyl_squared | killed by exact two-derivative normal form; otherwise four-derivative bound | R11 skeleton/template only | template_only | False | False |
| B530_3_scalar_class | scalar_tensor_class_metric | killed by mode-rank/vertical-kernel silence; otherwise extra-field residual bound | retained; no local silence theorem | unfilled_retained | False | False |
| B530_4_boundary | boundary_topological_terms | killed by fixed topological/boundary/projector silence; otherwise boundary/projector bound | boundary rows retained; no no-flux theorem promoted | template_only | False | False |
| B530_5_projector_domain | projector_domain_stress | killed by fixed topological/boundary/projector silence; otherwise boundary/projector bound | domain/projector rows retained; alpha3 lock extremely tight | unfilled_retained | False | False |
| B530_6_nonlocal_memory | nonlocal_memory_kernel | killed by mode-rank/vertical-kernel silence; otherwise extra-field residual bound | template only; cosmology memory cannot be imported as local silence | template_only | False | False |
| B530_7_q_loc | q_loc_Gamma_Khat | requires same-source/readout ownership or q_loc vector split | provisional compact-shell budget only; U2 normalization not proved | provisional_budget_not_claim | False | False |
| B530_8_torsion_nonmetricity | torsion_nonmetricity | killed by Levi-Civita connection normal form; otherwise connection residual bound | P4 rows are template-only; metric compatibility not parent-derived | template_only | False | False |
| B530_9_vector_preferred_frame | vector_preferred_frame | killed by mode-rank/vertical-kernel silence; otherwise extra-field residual bound | retained; no zero theorem | unfilled_retained | False | False |
| B530_10_bulk_X | bulk_X_force_law | killed by mode-rank/vertical-kernel silence; otherwise extra-field residual bound | operator/source map not parent-derived | unfilled_retained | False | False |
| B530_11_readout_frame | observed_readout_frame | requires same-source/readout ownership or q_loc vector split | same-readout theorem open | unfilled_retained | False | False |

## Selector Result
| result_id | statement | mathematical_result | what_is_new | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RES3405_0_exact_selector | PNF3405_0 through PNF3405_7 imply the local two-derivative quotient field equation is EH with one Hilbert source and one G_ref. | S_eff=int sqrt(-g_obs)(C0+C1 R[g_obs])+S_matter[g_obs]+dB+R_silent; variation gives G_mn+Lambda g_mn=kappa_*T_mn | 3405 replaces the loose 'assume EH/Lovelock' gap with a parent normal-form + spin-2 mode-count contract. | EXACT_CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED | False |
| RES3405_1_partial_derivation | The two-derivative basis calculation itself is closed: if the parent has reduced to a two-derivative metric action, EH follows. | L_0+L_2+dB = sqrt(-g)(C0+C1 R)+dB | The remaining derivation target is no longer 'derive all of GR'; it is 'derive two-derivative massless spin-2 quotient normal form'. | DERIVED_MATH_NOT_MTS_SIGNATURE | False |
| RES3405_2_fallback_bound | If PNF3405_1 or PNF3405_2 fails, MTS must carry non-EH residual bounds, not claim local GR. | Delta_PPN <= Delta_EH_selector_abs + sum_i /E_i/E_EH/_projection with no cancellation credit | Non-EH rows now have a single normal-form residual law instead of scattered placeholders. | BOUND_CONTRACT_READY_VALUES_MISSING | False |

## Local-GR Impact
| impact_id | quantity | if_selector_signed | remaining_if_not_signed | valid_for_claim |
| --- | --- | --- | --- | --- |
| IM3405_0_Newton | Delta_Newton_v_coupled | zero after common G_ref and Hilbert/PiM source lock | source kappa/readout/PiM mass residual remains | False |
| IM3405_1_beta | kappa_v | eta/source/operator lanes collapse; PiM/boundary/readout/coupling/q_loc still require their matching silence clauses | use 3403 reduced envelope plus derivative-order residual law | False |
| IM3405_2_gamma | gamma-1 | EH metric core gives gamma=1 before residuals | R2/scalar/vector/connection/readout maps must be bounded | False |
| IM3405_3_preferred_frame | alpha_i, alpha3, xi | mode-rank and q_loc vector silence can kill preferred-frame/domain leakage | q_loc/vector/domain/projector projections remain high-risk | False |
| IM3405_4_Maxwell_EM_stress | EM/Poynting stress ownership | same Hilbert source puts Maxwell/Poynting stress on the source side before boundary bookkeeping | hidden Hodge/current normalization and boundary-flux shadow rows remain | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3405_0_two_derivative_math | two-derivative metric normal form selects EH | True | the scalar-density basis at <=2 derivatives is sqrt(-g)(C0+C1R)+dB | False | False |
| GATE3405_1_parent_mode_rank | MTS parent local vacuum has only massless spin-2 q-basic metric modes | False | parent Hessian/mode-rank extraction has not been performed and R11 families remain live | False | False |
| GATE3405_2_vertical_silence | vertical/extra sectors are gauge, gapped double-zero, or source/readout silent | False | actual scalar/vector/torsion/memory/domain/bulk-X rows lack parent-owned zero coefficients | False | False |
| GATE3405_3_EH_selector | MTS derives the EH selector rather than importing it | False | the selector theorem is exact conditional but parent normal-form hypotheses are unsigned | False | False |
| GATE3405_4_local_GR | local GR/PPN is derived | False | beta/gamma/source/readout/q_loc vector gates remain downstream of the selector | False | False |

## Decision Ledger
| decision_id | finding | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3405_0_real_progress | 3405 derives the EH selector from a smaller target: two-derivative massless spin-2 quotient normal form plus universal Hilbert source | the EH problem is no longer a foggy GR-import issue; it is a parent Hessian/mode-rank and vertical-silence problem | extract or bound the parent Hessian/mode-rank normal form | False |
| DEC3405_1_not_done | MTS still does not own EH at claim level | R11 non-EH families survive generic covariance and require either signed zero coefficients or derivative-order bounds | do not publish local-GR claim; continue proof attempt or populate non-EH residual bounds | False |
| DEC3405_2_best_next | the best next target is parent Hessian/mode-rank extraction | if only TT spin-2 is long-range, the spin-2 bootstrap plus Hilbert source gives the cleanest EH derivation route | build 3406 parent Hessian mode-rank extractor; q_loc vector split remains second target | False |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3406-Y5-R2FR-parent-Hessian-mode-rank-extractor-under-AX1090.md | scripts/Y5_R2FR_3406_parent_Hessian_mode_rank_extractor.py | extract the local vacuum Hessian/mode-rank signature needed for the spin-2 EH bootstrap route | this is the constructive way to prove or reject the central PNF3405_1 premise rather than circling the EH selector | False |
| 3407-Y5-R2FR-derivative-order-residual-bound-pack-under-AX1090.md | scripts/Y5_R2FR_3407_derivative_order_residual_bound_pack.py | if mode-rank extraction cannot zero non-EH rows, turn the four-derivative/extra-field residual laws into scored bound inputs | this is the fallback route that prevents a failed EH proof from wasting the local-GR program | False |
| 3408-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md | scripts/Y5_R2FR_3408_q_loc_U2_alpha_vector_projection_split.py | separate q_loc beta, alpha_i/alpha3 and xi projections after the selector/mode-rank fork | q_loc remains the highest-danger preferred-frame guard after EH-selector progress | False |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3405_0_sources | all registered sources exist | True | sources=21 |
| VAL3405_1_hypotheses | parent normal-form hypotheses written | True |  |
| VAL3405_2_selector_math | EH selector proof includes two-derivative basis | True |  |
| VAL3405_3_spin2 | spin-2 bootstrap route written | True |  |
| VAL3405_4_bound_law | fallback derivative-order residual law written | True |  |
| VAL3405_5_operator_triage | R11 beta families triaged | True |  |
| VAL3405_6_result | selector result distinguishes math from MTS claim | True |  |
| VAL3405_7_gates | EH/local-GR claim gates remain blocked | True |  |
| VAL3405_8_no_overclaim | all generated rows are nonclaim | True |  |
| VAL3405_9_scope | no 3405 output path targets formalization-workbench | True |  |
| VAL3405_10_next | next target is Hessian/mode-rank extraction | True |  |
| VAL3405_11_overall | 3405 validation overall | True | all required checks passed |
