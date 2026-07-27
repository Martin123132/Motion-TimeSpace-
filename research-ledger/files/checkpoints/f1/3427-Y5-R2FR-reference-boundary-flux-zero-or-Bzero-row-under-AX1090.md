# 3427 - Reference Boundary Flux Zero or Bzero Row

## Summary
- This checkpoint attacks the `H_ref/B_zero/Delta_symp` part of `PC3400_3`.
- In the Hilbert-identity branch from 3426, `B_zero` is not a magic missing equality term: `Pi_M^H J_H = J_H`, so the old topological exact-correction debt is absent.
- Exact charge improvements integrate to zero on closed homologous linked surfaces when corner data are fixed.
- A fixed `H_ref` is legal only if selected by the parent branch before source/readout; otherwise it is a hidden `GM` calibration knob.
- The public EH/Hilbert subcharge has a conditional zero route for `Delta_symp^EH` under fixed `tau`, reference, boundary and source-free exterior conditions.
- Full MTS boundary flux is **not** claimed: residual `Z/Y6/projector/hidden` flux remains and points straight at the no-extra-mass/Y6 gate.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| doc_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md | True | PiM handoff to reference/boundary lock | False |
| pim_theorem_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv | True | Hilbert-identity PiM theorem | False |
| pim_update_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3426_PC3400_3_UPDATE.csv | True | PC3400_3 PiM update | False |
| icomm_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3426_ICOMM_BOUND_ROWS.csv | True | Icomm/R_eq/projector bound rows | False |
| next_3426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3426_NEXT_TARGET.csv | True | machine-readable 3427 target | False |
| doc_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md | True | Hamiltonian source charge integrability split | False |
| eh_integrability_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_EH_INTEGRABILITY_SUBTHEOREM.csv | True | EH/Hilbert subcharge integrability | False |
| charge_decomp_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_MTS_CHARGE_DECOMPOSITION.csv | True | MTS charge residual decomposition | False |
| bounds_3425 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv | True | Hamiltonian/PiM residual rows | False |
| boundary_3420 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv | True | Hodge/no-flux boundary theorem | False |
| projector_3420 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3420_PROJECTOR_OWNER_GATE.csv | True | boundary normal/projector owner gate | False |
| lock_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv | True | older reference-lock law | False |
| schema_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv | True | M_H_ref/reference/boundary schema | False |
| hwt_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | True | Hilbert worldtube parent action contract | False |
| r_eq_rows_1015 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv | True | R_eq/B_zero/I_commutator retained rows | False |
| pim_input_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv | True | PiM boundary/source input template | False |

## Reference Lock Theorem
| step_id | claim | identity | status | missing_to_promote | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RLT3427_0_branch_reference | The local Hilbert-identity source branch may use a fixed reference functional selected before source readout. | H_ref := H_tau[g_ref,e_ref,tau,S_ref], with delta_source H_ref = 0 | EXACT_IF_REFERENCE_SELECTED_BY_PARENT_BRANCH | parent must name the reference class and forbid source/radius/readout dependence | False |
| RLT3427_1_closed_surface_improvement | Exact charge improvements do not change a closed linked surface charge when corner data are fixed. | Q_tau -> Q_tau + dY_tau gives integral_S dY_tau = integral_boundary(S) Y_tau = 0 for closed S | MATHEMATICAL_ZERO_FOR_CLOSED_SURFACE | surfaces must be closed, homologous and selected before readout | False |
| RLT3427_2_reference_derivative_silence | A fixed reference cannot absorb measured-GM calibration. | partial_{source,r,t,frame,lambda} H_ref = 0 | EXACT_IF_RLT3427_0_PARENT_SIGNED | reference rule must be written in the parent action, not chosen after fitting | False |
| RLT3427_3_Hilbert_identity_no_Bzero | In the Hilbert-identity PiM branch, there is no topological-Hilbert exact correction B_zero to prove. | Pi_M^H J_H = J_H, so Pi_M^H J_H - J_H = 0, not dB_zero | EXACT_FOR_HILBERT_IDENTITY_BRANCH | old independent topological PiM must remain demoted | False |
| RLT3427_4_old_topological_Bzero | Old topological PiM still needs B_zero_flux=0 if used. | Pi_M^top J_H - Pi_M^H J_H = dB_zero + R_eq | NOT_PROVED_RETAIN_BOUND_ROW | same-object theorem, zero boundary flux and R_eq=0 | False |
| RLT3427_5_verdict | Reference shift and B_zero can be killed in the Hilbert-identity branch, conditionally on fixed reference and closed surfaces. | Delta_ref=0 and B_zero_flux^H=0; old topological B_zero remains retained | PARTIAL_PC3400_3_IMPROVEMENT | parent signature for reference/surface class and no residual symplectic flux | False |

## Boundary Flux Theorem
| step_id | claim | identity | status | missing_to_promote | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BFT3427_0_annulus_balance | The Hamiltonian charge difference across homologous linked surfaces equals constraint plus boundary leakage in the annulus. | H_tau[S2]-H_tau[S1] = int_A C_tau + Flux_boundary + Flux_extra | COVARIANT_PHASE_SPACE_BALANCE | explicit parent C_tau and flux decomposition | False |
| BFT3427_1_EH_source_free_zero | For the public EH/Hilbert subcharge in a source-free exterior, the constraint flux vanishes. | int_A C_tau^EH = 0 | EXACT_IF_EH_BRANCH_AND_SOURCE_FREE_EXTERIOR | compact exterior must exclude source support and use same tau | False |
| BFT3427_2_fixed_boundary_zero | Fixed Dirichlet/asymptotic/corner data kill symplectic boundary leakage for the EH subcharge. | Delta_symp^EH = int_boundary(delta Q_tau^EH - i_tau Theta_EH)_leak = 0 | EXACT_IF_BOUNDARY_CONDITIONS_FIXED | parent must define the local boundary class and corner rule | False |
| BFT3427_3_no_flux_vector_consistency | This is compatible with the 3420 no-flux condition for q_loc vector silence. | P_V n_mu B_GK^{mu nu}=0 is the vector-sector analogue of no compact linked boundary source | CONSISTENT_WITH_3420_NOT_INDEPENDENTLY_SIGNED | same boundary class must serve charge and q_loc vector gates | False |
| BFT3427_4_MTS_extra_flux | Residual MTS/Z/Y6/projector sectors can still create boundary or symplectic flux. | Delta_symp^MTS = Delta_symp^EH + Delta_symp^Z + Delta_symp^extra + Delta_symp^projector | RETAIN_RESIDUAL_BOUND_ROWS | Z fixed point, Y6 no-extra-mass, projector/hidden-sector no-hair | False |
| BFT3427_5_verdict | EH/reference boundary flux can be conditionally zero, but full MTS boundary flux is not yet closed. | Delta_symp^EH=0; Delta_symp^MTS_residual must be zeroed or bounded | PARTIAL_THEOREM_NOT_LOCAL_GR | component zero proofs or source-backed B_zero/Delta_symp/H_ref rows | False |

## Boundary Branch Split
| branch_id | branch | reference_result | boundary_result | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BBS3427_0_Hilbert_identity_EH | Hilbert-identity PiM plus public EH/Hilbert subcharge | Delta_ref=0 if H_ref is parent-fixed | B_zero_flux=0 for closed homologous surfaces; Delta_symp^EH=0 under fixed boundary data | BEST_CONDITIONAL_ROUTE | False |
| BBS3427_1_old_topological | old topological PiM same-object route | reference still must be fixed | B_zero_flux and R_eq remain unproved | DEMIT_TO_BOUND_BRANCH_UNLESS_SAME_OBJECT_PROOF | False |
| BBS3427_2_hidden_boundary | hidden/domain/projector/Y6 boundary charge | not killed by EH reference theorem | Delta_symp_extra and Delta_extra_mass remain | RETAIN_FOR_PC3400_4_OR_BOUND | False |
| BBS3427_3_verdict | preferred local branch | sign fixed H_ref for public EH/Hilbert branch | use closed-surface exact-improvement zero; retain only MTS residual flux rows | PARTIAL_PC3400_3_CLOSE | False |

## Bzero Bound Rows
| bound_id | quantity | definition | bound_formula | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BZR3427_0_reference_shift | Delta_ref_over_MH | reference subtraction shift normalized by dressed source charge | 0 if H_ref is parent-fixed and derivative-silent; otherwise /H_ref_shift//M_H_ref | CONDITIONAL_ZERO_NEEDS_PARENT_REFERENCE_SIGNATURE | False |
| BZR3427_1_Bzero_Hilbert_identity | B_zero_flux^H | exact boundary improvement flux in Hilbert-identity branch | 0 for closed homologous surfaces with fixed corner data | CONDITIONAL_THEOREM_ZERO | False |
| BZR3427_2_Bzero_topological | B_zero_flux^top | old topological-Hilbert exact correction flux | M_H_ref^-1 /int_boundary dB_zero/ | MISSING_SAME_OBJECT_BOUNDARY_ZERO_PROOF_OR_VALUE | False |
| BZR3427_3_Delta_symp_EH | Delta_symp^EH_over_MH | public EH/Hilbert symplectic boundary leakage | 0 under fixed tau, reference, boundary and corner conditions | CONDITIONAL_THEOREM_ZERO | False |
| BZR3427_4_Delta_symp_residual | Delta_symp^residual_over_MH | Z/Y6/projector/hidden-sector symplectic or boundary leakage | M_H_ref^-1 /Delta_symp^Z+Delta_symp^Y6+Delta_symp^projector+Delta_symp^hidden/ | MISSING_RESIDUAL_NO_HAIR_OR_VALUES | False |
| BZR3427_5_total | epsilon_boundary_reference_after_3427 | no-cancellation boundary/reference residual after Hilbert-identity branch split | Delta_ref_over_MH+B_zero_flux^top+Delta_symp^residual_over_MH | FORMULA_READY_VALUES_MISSING | False |

## PC3400_3 Update
| pc_piece | before_3427 | after_3427 | remaining | valid_for_claim |
| --- | --- | --- | --- | --- |
| PC3400_3_reference | reference named but not locked | can be signed if parent fixes H_ref before source/readout | actual parent reference class still not adopted in core | False |
| PC3400_3_Bzero | B_zero_flux retained from old topological equality | zero in Hilbert-identity branch; retained only for old topological branch | old topological same-object proof if that branch is used | False |
| PC3400_3_Delta_symp_EH | symplectic leakage broadly open | zero for public EH subcharge under fixed boundary conditions | MTS residual sectors can still leak | False |
| PC3400_3_verdict | PiM/reference/boundary all blocking | PiM and EH/reference-boundary pieces have conditional theorem routes | parent adoption, tau/MHref row, residual MTS flux, PC3400_4 no-extra-mass/Y6 | False |

## Promotion Gates
| gate_id | claim | gate_status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG3427_0_reference_branch | fixed-reference zero is available in the Hilbert-identity source branch | PASS_CONDITIONAL_THEOREM | H_ref fixed before readout gives derivative silence | False |
| PG3427_1_Bzero_Hilbert_identity | B_zero_flux is zero for the Hilbert-identity branch | PASS_CONDITIONAL_THEOREM | there is no topological-Hilbert exact correction; closed-surface exact improvements integrate to zero | False |
| PG3427_2_old_topological_Bzero | old topological branch has zero B_zero_flux | FAIL_CURRENT | same-object equality and boundary flux proof remain absent | False |
| PG3427_3_full_boundary_flux | full MTS symplectic/boundary flux is zero | PARTIAL_ONLY | EH subcharge yes; Z/Y6/projector/hidden residual flux remains | False |
| PG3427_4_PC3400_3 | full PC3400_3 is signed | PARTIAL_ONLY | PiM/reference/Bzero improved; MHref/tau/residual flux still need closure | False |
| PG3427_5_local_GR | local GR/Newton/PPN branch is derived | BLOCKED | PC3400_4 no-extra-mass/Y6, lambda-star, q_loc and second-order PPN gates remain open | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3427_0_reference_not_a_fit | A fixed EH/Hilbert reference is legal only if selected before source/readout. | otherwise H_ref can absorb measured GM and become a hidden calibration knob | treat H_ref zero as conditional theorem, not current claim | False |
| DEC3427_1_Bzero_branch_split | B_zero debt belongs to the old topological branch, not the Hilbert-identity branch. | Pi_M^H J_H = J_H has no topological-Hilbert exact correction | keep old topological PiM demoted unless same-object equality closes | False |
| DEC3427_2_progress | PC3400_3 is now mostly reduced to residual MTS flux plus MHref/tau bookkeeping. | PiM commutator, EH reference shift, and Hilbert-identity Bzero have conditional zero routes | attack no-extra-mass/Y6 because residual flux now points there | False |
| DEC3427_3_next | Next target should be no-extra-mass/Y6 monopole silence or bound. | remaining residual boundary flux is dominated by extra/Z/Y6/projector charge channels | 3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md | False |

## Next Target
| target | script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md | scripts/Y5_R2FR_3428_no_extra_mass_Y6_monopole_silence_or_bound.py | exclude hidden/domain/memory/projector/Y6 extra monopole source charge in the calibrated Hilbert-identity branch, or emit Delta_extra_mass/Y6 source-bound rows | 3427 gives conditional zero routes for fixed reference and Hilbert-identity Bzero; remaining source-charge danger is extra monopole/Y6 hair | False |
| 3429-Y5-R2FR-MHref-tau-source-row-instantiation-or-refusal-under-AX1090.md | scripts/Y5_R2FR_3429_MHref_tau_source_row_instantiation_or_refusal.py | instantiate a concrete M_H_ref/tau/source row for a toy compact source branch or refuse with exact missing columns | needed after no-extra-mass to make the bound branch scoreable | False |

## Runner Nonclaim
| runner_id | script | mode | summary | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN3427_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3427_reference_boundary_flux_zero_or_Bzero_row.py | REFERENCE_BOUNDARY_FLUX_ZERO_OR_BZERO_ROW | fixed-reference and Hilbert-identity Bzero zero routes written; old topological Bzero and residual MTS symplectic flux retained; local GR not claimed | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3427_0_sources_exist | all cited source paths exist | True | 16/16 source paths exist |
| VAL3427_1_outputs_scoped | all outputs are in post-checkpoint-work | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| VAL3427_2_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false throughout generated rows |
| VAL3427_3_reference_theorem | fixed-reference theorem exists | True | RLT3427_2 present |
| VAL3427_4_Bzero_split | Hilbert-identity Bzero zero and old topological Bzero retention are both explicit | True | BZR3427_1 and BZR3427_2 present |
| VAL3427_5_full_flux_not_claimed | full MTS boundary flux remains unclaimed | True | residual MTS flux retained |
| VAL3427_6_bound_rows | Bzero/Delta_symp/H_ref bound rows exist | True | BZR3427_5 present |
| VAL3427_7_local_GR_blocked | local GR remains blocked | True | no local-GR claim promoted |
| VAL3427_8_next_target | next target attacks no-extra-mass/Y6 | True | 3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md |
| VAL3427_9_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3427_10_overall | 3427 reference/boundary checkpoint is internally valid | True | PASS |

## Bottom Line
This trims the boundary/reference problem sharply. In the Hilbert-identity branch, reference and exact-boundary issues have clean conditional zero routes. What remains is not vague boundary fog; it is residual MTS source-charge hair, mainly extra/Y6/projector/hidden monopole flux.
