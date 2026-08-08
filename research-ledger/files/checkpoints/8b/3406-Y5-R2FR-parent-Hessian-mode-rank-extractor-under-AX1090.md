# 3406 - Y5/R2FR parent Hessian mode-rank extractor under AX1090

## Verdict

- 3406 turns the spin-2/EH selector into a concrete parent-Hessian pole test.
- The invariant object is `G_pub = R H^{-1} R^T`: local tests see public metric pole residues, not field-label choices like `Z_i` and `U_i` separately.
- The current corpus has the formula and useful toy laws, but it does not yet supply the parent `H_AB`, readout derivative `R`, source covector `J_A`, zero-mode class, or boundary class needed to prove TT-only rank.
- Therefore the EH selector is not claimed. The next non-circular move is a minimal source table for `H_AB/R/J`; the fallback is a residue-bound pack for surviving non-EH poles.

## Hessian Extractor Contract
| contract_id | object | required_identity | why_needed | current_evidence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HEX3406_0_stationary_branch | first variation | F_A := delta S_parent/delta Phi^A /_{Phi0}=0 modulo q-basic gauge and fixed boundary terms | a Hessian/mode count around a non-extremal branch is not a physical local vacuum spectrum | 3093 marks branch extremum missing for extra Xhat rows | NOT_PARENT_SIGNED | False |
| HEX3406_1_parent_Hessian | quadratic parent action | S_2=1/2 int delta Phi^A H_AB(k) delta Phi^B + 1/2 int T^{mn} R_{mn,A}(k) delta Phi^A | H_AB and readout map R define the physical pole/residue spectrum without field-redefinition games | 3316 derives the formula but not the entries | FORMULA_DERIVED_INPUTS_MISSING | False |
| HEX3406_2_public_metric_propagator | observable exchange | G_pub_{mnab}(k)=R_{mn,A}(k)[H^{-1}(k)]^{AB}R_{ab,B}(k) | the local tests see public metric exchange, not arbitrary field labels Z_i and U_i | 3316 exact readout derivation | INVARIANT_FORMULA_DERIVED | False |
| HEX3406_3_massless_spin2_pole | TT spin-2 residue | G_pub = G_ref P^(2)/k^2 + analytic/contact + no extra long-range pole | this is the concrete parent-Hessian version of 'only massless spin-2 is long-range' | 3405 states target; no parent Hessian pole extraction exists | TARGET_NOT_EXTRACTED | False |
| HEX3406_4_extra_mode_residues | scalar/vector/connection/domain/bulk residues | for each extra pole i: B_i=Res_i(T_s G_pub T_t)/Res_GR is zero, gapped-and-bounded, or source/readout silent | an extra field is harmless only if its observable residue is zero/below locks, not merely renamed | 3316 residue-ratio formula; R11 rows lack H_AB/R entries | RESIDUE_FORMULA_DERIVED_VALUES_MISSING | False |
| HEX3406_5_gauge_and_zero_modes | nullspace classification | ker H = q-basic diffeomorphism gauge only; edge/domain zero modes have zero charge or are fixed | extra zero modes are long-range hair unless first-class gauge or boundary-silent | 2858/3202 mark constraint class, boundary charge and zero modes open | ZERO_MODE_AUDIT_OPEN | False |
| HEX3406_6_self_adjoint_boundary | boundary class | H is self-adjoint on the local compact exterior with fixed annulus/reference and no unsourced flux | pole/rank extraction is meaningless if boundary flux supplies hidden physical modes | 3202 and 3403 retain boundary/reference gates | BOUNDARY_CLASS_NOT_PARENT_SIGNED | False |

## Mode-Rank Theorem
| step_id | statement | proof | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MRT3406_0_invariant_spectrum | The physically relevant local spectrum is the pole/residue decomposition of G_pub=R H^{-1} R^T. | Under nonsingular field redefinitions Phi->M Phi, H->M^T H M and R->R M, so R H^{-1} R^T is unchanged. | mode-rank must be read from public exchange poles, not from chosen variable names | DERIVED_FROM_3316 | False |
| MRT3406_1_TT_rank_condition | If G_pub has one positive massless spin-2 pole and no scalar/vector/connection/domain long-range pole with nonzero residue, then PNF3405_1 is signed. | The long-range phase space seen by matter/readout contains only the two TT polarizations of the public metric. Gauge zero modes are quotient redundancies and do not count. | the spin-2 bootstrap route in 3405 becomes active | EXACT_CONDITIONAL_THEOREM | False |
| MRT3406_2_extra_pole_no_go | A nonzero extra pole residue in G_pub blocks local-GR promotion unless it is bounded below the relevant local tests. | Any extra pole changes the two-source exchange, yielding finite-range, PPN, WEP, clock or preferred-frame signatures depending on spin and coupling. | extra modes become explicit residual rows instead of hidden closure assumptions | OBSTRUCTION_THEOREM | False |
| MRT3406_3_current_verdict | The current corpus has the invariant formula and several conditional toy laws, but no parent-owned H_AB/R extraction sufficient to prove TT-only rank. | 3093, 3316, 3317 and 3405 all keep parent Hessian entries, source/readout residues, zero-mode class and boundary class unsigned. | mode-rank is not claimed; the next task is to source or symbolically derive H_AB and R blocks | NOT_CLAIM_LEVEL | False |

## Public Propagator Tests
| test_id | test | formula | pass_condition | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PPT3406_0_field_redefinition | G_pub invariance under Phi -> M Phi | R H^{-1} R^T = (R M)(M^T H M)^{-1}(M^T R^T) | identity holds algebraically | PASS_FORMAL | False |
| PPT3406_1_massless_pole | positive GR pole | Res_{k^2=0}[T G_pub T] = G_ref T P^(2) T | positive residue, correct Hilbert source, same G_ref | FORMULA_READY_RESIDUE_NOT_EXTRACTED | False |
| PPT3406_2_scalar_residue | extra scalar pole silence | B_0 = Res_{k^2=-m_0^2}[T G_pub T]_{scalar}/Res_GR | B_0=0, m_0 infinite, or finite-range/PPN bound pass | R2_FR_SCALAR_INPUTS_MISSING | False |
| PPT3406_3_spin2_ghost_residue | massive spin-2/Weyl pole silence | B_2 = Res_{k^2=-m_2^2}[T G_pub T]_{massive spin2}/Res_GR | B_2=0 or bounded; sign/ghost handled by parent stability | RICCI_WEYL_INPUTS_MISSING | False |
| PPT3406_4_zero_mode_charge | nullspace is gauge not hair | v in ker H => R v=0 and J v=0 unless v is q-basic diffeo gauge | no physical zero mode with source/readout overlap | ZERO_MODE_CLASS_OPEN | False |

## Minimal Two-Channel Hessian Law
| law_id | statement | consequence | source | valid_for_claim |
| --- | --- | --- | --- | --- |
| M2H3406_0_ansatz | For Phi=(h,x), a minimal public Hessian test has H(p)=[[a p, b0+b1 p],[b0+b1 p, M2+z p]], R=(1,u), p=k^2. | This is the smallest algebraic model that can fake or spoil a GR pole. | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv | False |
| M2H3406_1_massless_condition | D(0)=-b0^2, so a GR-like massless pole at p=0 requires b0=0. | constant h-x mixing must be forbidden by symmetry/constraint, not fitted away. | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv | False |
| M2H3406_2_finite_pole | After b0=0, D(p)=p[a M2+(a z-b1^2)p] and p_f=-a M2/(a z-b1^2). | derivative mixing generically creates a finite pole unless absent, unobserved, or bounded. | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv | False |
| M2H3406_3_public_residue | A finite pole is physical only if R adj(H) R^T is nonzero at p_f. | source/readout silence is a residue theorem, not a variable-name theorem. | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv | False |

## Mode Family Triage
| operator_id | operator_family | mode_channel | required_hessian_test | current_status | claim_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| B530_0_source_AB | source_normalization_operator | source_readout_q_loc | same source/readout residue and q_loc projection split | unfilled | False | False |
| B530_1_R2_fR_scalar | R2_fR_scalar_mode | spin0_scalar | scalar pole residue B_0=0/gapped/bounded in G_pub | template_only | False | False |
| B530_2_Ricci_Weyl | Ricci_Weyl_squared | massive_spin2_or_four_derivative | massive spin-2 pole residue B_2=0/bounded and stability sign handled | template_only | False | False |
| B530_3_scalar_class | scalar_tensor_class_metric | spin0_scalar | scalar pole residue B_0=0/gapped/bounded in G_pub | unfilled_retained | False | False |
| B530_4_boundary | boundary_topological_terms | edge_boundary | edge zero mode fixed/topological/source-blind or explicit boundary residue bound | template_only | False | False |
| B530_5_projector_domain | projector_domain_stress | extra_domain_bulk_memory | kernel/domain/bulk pole absent, massive, source-silent or bounded | unfilled_retained | False | False |
| B530_6_nonlocal_memory | nonlocal_memory_kernel | extra_domain_bulk_memory | kernel/domain/bulk pole absent, massive, source-silent or bounded | template_only | False | False |
| B530_7_q_loc | q_loc_Gamma_Khat | source_readout_q_loc | same source/readout residue and q_loc projection split | provisional_budget_not_claim | False | False |
| B530_8_torsion_nonmetricity | torsion_nonmetricity | connection | connection Hessian algebraic/gauge or zero source/readout residue | template_only | False | False |
| B530_9_vector_preferred_frame | vector_preferred_frame | spin1_preferred_frame | vector pole absent/aligned/gapped and alpha_i residues below locks | unfilled_retained | False | False |
| B530_10_bulk_X | bulk_X_force_law | extra_domain_bulk_memory | kernel/domain/bulk pole absent, massive, source-silent or bounded | unfilled_retained | False | False |
| B530_11_readout_frame | observed_readout_frame | source_readout_q_loc | same source/readout residue and q_loc projection split | unfilled_retained | False | False |

## Hessian Input Status
| input_id | needed_input | available_now | best_source | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HIS3406_0_HAB | symbolic parent Hessian block H_AB(k) around the local branch | formula for use exists; actual parent entries not extracted | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv | MISSING_PARENT_ENTRIES | False |
| HIS3406_1_Rmap | public metric readout derivative R_{mn,A}=delta g_pub_mn/delta Phi^A | identity candidate for effective v1 metric; same observed coframe unsigned | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3174_EFFECTIVE_HESSIAN_EXTRACTION.csv | PARTIAL_READOUT_CANDIDATE | False |
| HIS3406_2_Jsource | source covector J_A from descended Hilbert matter/EM action | Hilbert source clause conditional; not parent-signed for all sectors | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md | CONDITIONAL_NOT_PARENT_SIGNED | False |
| HIS3406_3_gauge_kernel | classification of ker H into q-basic diffeo gauge versus physical zero modes | degree-count audits mark constraint class and boundary charge open | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3202_COERCIVITY_AND_ZERO_MODE_GATE.csv | ZERO_MODE_CLASS_OPEN | False |
| HIS3406_4_boundary_domain | self-adjoint boundary/domain class for H and no unsourced edge charge | conditional coercivity and zero-mode gates, no parent boundary certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3202_COERCIVITY_AND_ZERO_MODE_GATE.csv | BOUNDARY_CERTIFICATE_MISSING | False |
| HIS3406_5_residue_units | common units/sign convention for residue ratios B_i against G_ref | 3316 ratio formula; no source-backed residues | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3316_HESSIAN_READOUT_DERIVATION.csv | NORMALIZATION_FORMULA_READY_VALUES_MISSING | False |

## Residue Bound Interface
| bound_id | quantity | bound_formula | required_inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RBI3406_0_spin0 | B_0(lambda_0) | /B_0/ <= min(PPN_gamma_scalar, beta_scalar, R10_alpha(lambda_0), clock/WEP if sourced) | scalar pole mass, residue sign, source/readout overlap, screening/local profile | FORMULA_READY_INPUTS_MISSING | False |
| RBI3406_1_massive_spin2 | B_2(lambda_2) | /B_2/ <= min(PPN_gamma_beta, finite-range spin2, stability/ghost exclusion) | Weyl/Ricci coefficient, massive spin2 pole, residue, sign/stability rule | FORMULA_READY_INPUTS_MISSING | False |
| RBI3406_2_connection | B_conn | /B_conn/ <= min(clock, WEP, lightcone, spin, PPN connection projections) | torsion/nonmetricity Hessian, hypermomentum/source coupling, readout overlap | FORMULA_READY_INPUTS_MISSING | False |
| RBI3406_3_domain_memory_bulk | B_X(lambda_X) | /B_X/ <= /R_X H_X^{-1} J_X/ / /R_h H_h^{-1} J_h/ and arena-specific locks | H_X, R_X, J_X, boundary flux, local profile and arena projection | FORMULA_READY_INPUTS_MISSING | False |

## Selector Impact
| impact_id | target | if_3406_passes | if_3406_fails | current_result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SIM3406_0_EH_selector | PNF3405_1 mode-rank premise | parent owns TT-only long-range mode rank; 3405 EH selector can promote to the next source/readout gates | non-EH residual bound pack is mandatory | FORMULA_READY_NOT_EXTRACTED | False |
| SIM3406_1_beta_gamma | beta/gamma metric core | extra scalar/four-derivative metric poles are zero; EH beta/gamma core becomes parent-owned conditional on source/readout | scalar/Ricci/Weyl residues must be scored against PPN/R10 | BLOCKED_BY_HAB_RMAP_INPUTS | False |
| SIM3406_2_q_loc | q_loc preferred-frame vector | q_loc can be treated as residual divergence of owned sectors; still needs projection split | q_loc remains separate beta/alpha_i/xi danger | PROJECTION_SPLIT_STILL_REQUIRED | False |
| SIM3406_3_EM_Maxwell | Maxwell/Poynting Hilbert stress | EM stress lives in source covector J_A through same public metric exchange | hidden Hodge/current readout residues remain explicit source-sector tests | SOURCE_COVECTOR_CONDITIONAL | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3406_0_public_formula | invariant public Hessian propagator formula is available | True | 3316 and 3406 use G_pub=R H^{-1} R^T | False | False |
| GATE3406_1_parent_HAB | parent Hessian H_AB and readout R are extracted from MTS parent action | False | formula exists but entries/source maps remain missing or conditional | False | False |
| GATE3406_2_TT_only | only long-range public mode is positive massless spin-2 | False | extra scalar/vector/connection/domain residues are not proven zero or bounded | False | False |
| GATE3406_3_EH_selector | 3405 EH selector is parent-signed | False | mode-rank premise remains unextracted | False | False |
| GATE3406_4_local_GR | local GR/PPN is derived | False | requires EH selector plus source/readout/q_loc vector gates | False | False |

## Decision Ledger
| decision_id | finding | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3406_0_progress | the mode-rank test is now concrete and field-redefinition invariant | local tests see pole residues of G_pub=R H^{-1} R^T, not arbitrary Z_i/U_i labels | source or symbolically derive the actual parent H_AB and R blocks | False |
| DEC3406_1_verdict | current corpus does not yet prove TT-only long-range rank | parent Hessian entries, readout derivative, source covector, zero-mode class and boundary class remain unsigned | do not claim EH selector; build a minimal Hessian source table or go to residual bounds | False |
| DEC3406_2_best_next | best next target is the minimal parent-Hessian input pack | without H_AB/R/J rows, every later PPN/R10 bound is just a placeholder; with them, the EH selector can be scored cleanly | construct 3407 minimal H_AB/R/J source table and refuse unsourced entries | False |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3407-Y5-R2FR-minimal-parent-Hessian-source-table-under-AX1090.md | scripts/Y5_R2FR_3407_minimal_parent_Hessian_source_table.py | construct the minimal source-backed H_AB, R_mn,A and J_A table required to evaluate G_pub pole residues | this is the first non-circular way to decide whether the parent really has only the TT spin-2 public pole | False |
| 3408-Y5-R2FR-derivative-order-residue-bound-pack-under-AX1090.md | scripts/Y5_R2FR_3408_derivative_order_residue_bound_pack.py | if H_AB/R/J cannot be sourced, convert all surviving non-EH pole channels into no-cancellation empirical bound rows | this is the honest fallback if the derivation route cannot currently close | False |
| 3409-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md | scripts/Y5_R2FR_3409_q_loc_U2_alpha_vector_projection_split.py | separate q_loc beta, alpha_i/alpha3 and xi projections after the Hessian-mode fork | q_loc remains the highest-danger vector guard once the spin-2 pole story is clarified | False |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3406_0_sources | all registered sources exist | True | sources=17 |
| VAL3406_1_contract | Hessian extractor contract written | True |  |
| VAL3406_2_theorem | mode-rank theorem written | True |  |
| VAL3406_3_propagator | public propagator tests written | True |  |
| VAL3406_4_two_channel | minimal two-channel Hessian law written | True |  |
| VAL3406_5_triage | R11 mode families triaged | True |  |
| VAL3406_6_inputs | Hessian input status records missing H_AB/R/J | True |  |
| VAL3406_7_gates | TT-only/local-GR gates remain blocked | True |  |
| VAL3406_8_no_overclaim | all generated rows are nonclaim | True |  |
| VAL3406_9_scope | no 3406 output path targets formalization-workbench | True |  |
| VAL3406_10_next | next target is minimal parent-Hessian source table | True |  |
| VAL3406_11_overall | 3406 validation overall | True | all required checks passed |
