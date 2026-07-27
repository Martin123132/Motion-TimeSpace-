# 3425 - Hamiltonian Reference/PiM Integrability Lock or MHref Row

## Summary
- This checkpoint upgrades the old 1017 reference-lock problem using the 3424 source-action candidate.
- Real progress: the public EH/Hilbert part of the candidate has a standard integrable Hamiltonian charge route under fixed `tau`, fixed reference, stationary local boundary data, and source-free exterior.
- That means the legal denominator can be a dressed `M_H_ref^EH = c^-2(H_tau^EH[S]-H_ref^EH)` in the candidate branch, not bare mass and not orbital `GM`.
- But full MTS does **not** inherit the charge yet: residual `Z`, `Pi_M`, boundary/reference, projector, and extra/Y6 charge pieces remain outside the EH subtheorem.
- So `PC3400_3` is partially improved: EH/Hilbert integrability can be conditionally signed, but PiM chain-map equality and reference/boundary silence still block the current Y5-zero claim.
- The next best move is `Pi_M`: prove it is a parent-fixed chain map with `[d,Pi_M]J_H=0`, or demote it to an explicit `I_commutator`/projector-stress bound.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| doc_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md | True | minimal source-action handoff | False |
| action_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv | True | candidate local parent source action | False |
| pc3400_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3424_PC3400_ADOPTION_AUDIT.csv | True | PC3400 partial adoption audit | False |
| bounds_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3424_RETAINED_SOURCE_BOUND_ROWS.csv | True | retained source-bound rows after action candidate | False |
| next_3424 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3424_NEXT_TARGET.csv | True | machine-readable 3425 target | False |
| doc_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md | True | prior Hamiltonian/PiM reference lock | False |
| lock_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv | True | older lock-law split | False |
| schema_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv | True | older M_H_ref first-row schema | False |
| runner_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_FIRST_ROW_RUNNER.csv | True | older first-row refusal runner | False |
| hsm_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | True | Hamiltonian source-measure contract | False |
| hwt_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | True | Hilbert worldtube parent action contract | False |
| hwt_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv | True | Hilbert worldtube glue theorem attempt | False |
| worldtube_measure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | True | GR-style worldtube source-measure theorem | False |
| source_measure_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv | True | source-measure theorem attempt | False |
| r_eq_rows_1015 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv | True | R_eq/B_zero/I_commutator fallback rows | False |
| parent_clauses_3400 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv | True | PC3400 source-coupling clauses | False |
| boundary_3420 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3420_HODGE_BOUNDARY_SILENCE_THEOREM.csv | True | boundary/no-flux silence conditions | False |
| fixed_point_3421 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3421_EULER_FIXED_POINT_THEOREM.csv | True | Euler fixed-point theorem if source terms vanish | False |

## EH Integrability Subtheorem
| step_id | claim | identity | status | missing_to_promote | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EHI3425_0_covariant_phase_space | The public EH plus Hilbert matter part has the standard covariant-phase-space Hamiltonian variation. | delta H_tau^EH[S] = integral_S (delta Q_tau^EH - i_tau Theta_EH) | KNOWN_CONDITIONAL_FOR_PAD3424_PUBLIC_EH_SECTOR | MTS must adopt PAD3424_1/PAD3424_2 as the actual local parent branch | False |
| EHI3425_1_integrability | For fixed tau, fixed asymptotic/reference data, and stationary local boundary conditions, the EH charge is integrable. | curl(delta H_tau^EH)=integral_S i_tau omega_EH = 0 | EH_SUBTHEOREM_CAN_BE_SIGNED_CONDITIONALLY | tau/reference/boundary lock and no residual MTS symplectic flux | False |
| EHI3425_2_radial_closure | In a compact source-free exterior annulus, the EH Hamiltonian charge is surface-independent. | H_tau^EH[S2]-H_tau^EH[S1]=int_A C_tau^EH=0 | EH_SUBTHEOREM_CAN_BE_SIGNED_CONDITIONALLY | source-free exterior and boundary flux silence for the MTS residual sectors | False |
| EHI3425_3_MHref_EH | The legal denominator is a dressed charge, not bare mass or orbital GM. | M_H_ref^EH := c^-2 (H_tau^EH[S_outer]-H_ref^EH) | DEFINITION_GUARDRAIL_PLUS_EH_BRANCH_CANDIDATE | explicit reference rule and same-frame source support | False |
| EHI3425_4_MTS_transfer | MTS inherits the EH charge only if all residual Hamiltonian pieces are zero or explicitly bounded. | H_tau^MTS = H_tau^EH + Delta H_Z + Delta H_PiM + Delta H_boundary + Delta H_extra + Delta H_ref | TRANSFER_THEOREM_NOT_CURRENT_CLAIM | Z fixed point, PiM chain map, boundary/reference silence, no-extra-mass/Y6 | False |
| EHI3425_5_verdict | 3424 lets us sign the EH/Hilbert subcharge route, but not the full MTS Hamiltonian/PiM lock. | epsilon_HPiM = 0 only if Delta H_Z=Delta H_PiM=Delta H_boundary=Delta H_extra=Delta H_ref=0 | PARTIAL_DERIVATION_REAL_RESIDUALS_REMAIN | component zero proofs or source-backed M_H_ref-normalized rows | False |

## MTS Charge Decomposition
| component_id | charge_piece | variation_or_flux | zero_or_lock_condition | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HDC3425_0_EH_Hilbert | H_tau^EH[g_obs,T_H] | delta H_tau^EH = integral_S(delta Q_tau^EH - i_tau Theta_EH) | fixed tau/reference and stationary source-free exterior | CONDITIONAL_EH_LOCK | False |
| HDC3425_1_Z_sector | Delta H_Z | integral_S(delta Q_tau^Z - i_tau Theta_Z) | 3421 fixed point gives Z=0 and no linear source current | PENDING_Y5_Y6_LAMBDA_SOURCE_GATES | False |
| HDC3425_2_PiM_chain | Delta H_PiM | I_commutator = integral_A [d,Pi_M]J_H plus projector-stress response | Pi_M is parent-fixed covariantly constant chain map on Hilbert current space | OPEN_BIGGEST_PC3400_3_RESIDUAL | False |
| HDC3425_3_boundary_reference | Delta H_boundary + Delta H_ref | B_zero_flux + Delta_symp + H_ref_shift | boundary/reference rule fixed once; compact linked flux zero | OPEN_REFERENCE_LOCK | False |
| HDC3425_4_extra_mass | Delta H_extra | nonEH/domain/memory/range/frame/Y6 monopole flux | no-hair/safe-class theorem or explicit source-backed bound | OPEN_PC3400_4_RESIDUAL | False |
| HDC3425_5_total | H_tau^MTS-H_ref^MTS | H_EH plus all Delta H components | HDC3425_0 locked and HDC3425_1 through HDC3425_4 zero/bounded | NOT_LOCKED_FOR_CURRENT_MTS | False |

## PC3400_3 Lock Audit
| lock_id | required_lock | can_3424_candidate_supply | remaining_obstruction | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| P3L3425_0_tau_fixed | one tau used for source, charge, clocks and readout | partially: tau is named in branch data | tau selection by parent coframe/asymptotic structure not derived | PARTIAL | False |
| P3L3425_1_integrability_curl | field-space curl of delta H_tau^MTS vanishes | yes for public EH/Hilbert subcharge under fixed boundary conditions | Z/PiM/boundary/extra-sector symplectic curls uncomputed | PARTIAL_EH_ONLY | False |
| P3L3425_2_reference_lock | H_ref is fixed once and derivative-silent | names fixed reference but does not select it | reference functional and allowed background class not parent-derived | OPEN | False |
| P3L3425_3_PiM_chain_map | Pi_M maps Hilbert current to the same charge without commutator hair | no, Pi_M is branch data but not constructed | [d,Pi_M]J_H and projector stress remain active | OPEN | False |
| P3L3425_4_MHref_positive | M_H_ref is positive dressed same-frame source denominator | conditionally for EH source charge | needs explicit surface/source system row or theorem-zero residual transfer | PARTIAL_EH_DENOMINATOR_ONLY | False |
| P3L3425_5_verdict | PC3400_3 is signed | not fully | PiM chain map, reference lock, and residual MTS charge pieces | FAIL_CURRENT_PC3400_3 | False |

## MHref Candidate Rows
| row_id | quantity | definition | candidate_value_or_theorem | claim_readiness | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MHC3425_0_EH_theorem_denominator | M_H_ref^EH | dressed EH/Hilbert source denominator in the 3424 public metric branch | M_H_ref^EH := c^-2(H_tau^EH[S_outer]-H_ref^EH) | THEOREM_CANDIDATE_NEEDS_REFERENCE_AND_SOURCE_ROW | False |
| MHC3425_1_integrability_curl_EH | delta_H_tau_EH_nonintegrable_over_MH | field-space curl obstruction for the public EH/Hilbert subcharge | 0 if fixed tau/stationary boundary/reference conditions are signed | CONDITIONAL_ZERO_NOT_CURRENT_CLAIM | False |
| MHC3425_2_integrability_curl_MTS_residual | delta_H_tau_MTS_residual_over_MH | non-EH/Z/PiM/boundary/extra-sector symplectic curl normalized by M_H_ref | MISSING_SECTOR_OWNER_OR_BOUND | RETAINED | False |
| MHC3425_3_MHref_source_row_schema | claim-ready M_H_ref row | source-specific dressed charge with tau, surface, reference, units and source path | system_id;tau_id;surface_outer;Q_tau_integral;H_ref;M_H_ref;units;source_path;assumptions | SCHEMA_READY_NO_VALUE | False |
| MHC3425_4_total_FB5540_after_EH | epsilon_HPiM_after_EH_lock | remaining Hamiltonian/PiM residual after the public EH subcharge is conditionally locked | epsilon_Z_charge + epsilon_PiM_comm + epsilon_boundary_ref + epsilon_extra_mass + epsilon_tau | FORMULA_READY_VALUES_MISSING | False |

## Residual Bound Rows
| bound_id | quantity | definition | bound_formula | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HBR3425_0_tau_lock | epsilon_tau_lock | mismatch among source/charge/clock/readout time generators | 0 if tau is parent-selected by e_obs and fixed boundary data; else source-backed mismatch norm | THEOREM_OR_VALUE_MISSING | False |
| HBR3425_1_reference | epsilon_reference | reference subtraction shift normalized by M_H_ref | /H_ref_shift//M_H_ref + /partial_source H_ref//M_H_ref | REFERENCE_RULE_MISSING | False |
| HBR3425_2_PiM_commutator | epsilon_PiM_comm | PiM chain-map/commutator and projector-stress leakage | /I_commutator//M_H_ref + /T_PiM/_PPN | PIM_CHAIN_MAP_OR_VALUE_MISSING | False |
| HBR3425_3_Z_charge | epsilon_Z_charge | residual Z-sector Hamiltonian charge after fixed-point branch | 0 if Z=0 source-free fixed point is signed; else C_HZ //Z// | PENDING_SOURCE_CURRENT_AND_LAMBDA_STAR | False |
| HBR3425_4_boundary_flux | epsilon_boundary_flux | boundary/symplectic flux through compact linked surfaces | (/B_zero_flux/+/Delta_symp/)/M_H_ref | BOUNDARY_NO_FLUX_NOT_PARENT_SIGNED | False |
| HBR3425_5_extra_mass | epsilon_extra_mass | extra/Y6/domain/memory/projector monopole source charge | /Delta_extra_mass//M_H_ref | NO_EXTRA_MASS_THEOREM_MISSING | False |
| HBR3425_6_total | epsilon_HPiM_after_EH_lock | no-cancellation Hamiltonian/PiM residual after EH subtheorem | epsilon_tau_lock+epsilon_reference+epsilon_PiM_comm+epsilon_Z_charge+epsilon_boundary_flux+epsilon_extra_mass | FORMULA_READY_VALUES_MISSING | False |

## Promotion Gates
| gate_id | claim | gate_status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG3425_0_EH_subcharge | public EH/Hilbert subcharge has a legitimate integrability route | PASS_CONDITIONAL_SUBTHEOREM | 3424 candidate supplies EH public geometry and Hilbert matter source | False |
| PG3425_1_MTS_full_integrability | full MTS Hamiltonian charge is integrable | FAIL_CURRENT | Z/PiM/boundary/reference/extra-sector curls are not zeroed | False |
| PG3425_2_MHref_claim_ready | M_H_ref is stable and claim-ready | NOT_PROMOTED | source-specific Q_tau integral, reference rule and residual transfer are missing | False |
| PG3425_3_PC3400_3 | PC3400_3 Htau/PiM chain is signed | PARTIAL_ONLY | EH subcharge yes; PiM chain-map/reference lock no | False |
| PG3425_4_Y5_zero | Y5 source current is zero after Hamiltonian lock | BLOCKED | epsilon_HPiM_after_EH_lock and no-extra-mass rows remain | False |
| PG3425_5_local_GR | local GR/Newton/PPN branch is derived | BLOCKED | Y5 not fully zero, Y6/extra mass, lambda-star, q_loc and second-order PPN remain open | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3425_0_real_progress | The Hamiltonian charge problem is no longer all-or-nothing. | the 3424 action candidate gives a legitimate EH/Hilbert integrable subcharge under standard fixed-reference conditions | keep the EH charge as the parent candidate denominator while proving or bounding residual charge hair | False |
| DEC3425_1_not_finished | Full PC3400_3 is still not signed. | PiM chain-map equality, reference selection, boundary flux and extra-sector charges remain outside the EH subtheorem | attack PiM chain-map first, then no-extra-mass/Y6 | False |
| DEC3425_2_MHref_policy | M_H_ref may be the dressed EH/Hilbert source charge only in the candidate branch, not bare mass or orbital GM. | using orbital GM or a reference-only denominator would circularly normalize the theorem with its target | require Q_tau integral, fixed reference, surface, tau and source path before any score row | False |
| DEC3425_3_best_next | Next target should construct PiM as a chain map or demote it to an I_commutator bound. | after EH integrability, PiM is the largest PC3400_3 object-specific obstruction | 3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md | False |

## Next Target
| target | script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md | scripts/Y5_R2FR_3426_PiM_chain_map_identity_or_Icommutator_bound.py | prove Pi_M is a parent-fixed chain map on the Hilbert current space with [d,Pi_M]J_H=0 and no projector stress, or emit I_commutator/projector-stress bound rows | 3425 conditionally locks the EH/Hilbert subcharge; PiM is now the largest specific PC3400_3 residual | False |
| 3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md | scripts/Y5_R2FR_3427_reference_boundary_flux_zero_or_Bzero_row.py | prove fixed H_ref and compact linked boundary/symplectic flux silence, or emit B_zero_flux/Delta_symp/H_ref_shift rows | reference and boundary rows are the other PC3400_3 residuals after PiM | False |

## Runner Nonclaim
| runner_id | script | mode | summary | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN3425_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3425_Hamiltonian_reference_PiM_integrability_lock_or_MHref_row.py | HAMILTONIAN_REFERENCE_PIM_INTEGRABILITY_LOCK_OR_MHREF_ROW | EH/Hilbert integrability subtheorem conditionally inherited by 3424 candidate; full MTS PC3400_3 remains blocked by PiM/reference/boundary/Z/extra residuals; MHref and residual bound rows staged nonclaim | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3425_0_sources_exist | all cited source paths exist | True | 18/18 source paths exist |
| VAL3425_1_outputs_scoped | all outputs are in post-checkpoint-work | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| VAL3425_2_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false throughout generated rows |
| VAL3425_3_EH_subtheorem | EH/Hilbert integrability subtheorem is present | True | EHI3425_1 present |
| VAL3425_4_MTS_transfer_not_claimed | full MTS transfer remains unclaimed | True | MTS residual curls remain open |
| VAL3425_5_MHref_rows | M_H_ref candidate/source-row schema exists | True | MHC3425_3 present |
| VAL3425_6_residual_bounds | residual Hamiltonian/PiM bound rows exist | True | HBR3425_6 present |
| VAL3425_7_local_GR_blocked | local GR remains blocked | True | no local-GR claim promoted |
| VAL3425_8_next_target | next target attacks PiM chain map | True | 3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md |
| VAL3425_9_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3425_10_overall | 3425 Hamiltonian/PiM checkpoint is internally valid | True | PASS |

## Bottom Line
This is a useful narrowing. The Hamiltonian source charge is no longer pure fog: the EH/Hilbert subcharge is a legitimate inherited mechanism inside the 3424 candidate. The remaining danger is exactly the MTS-specific charge hair: `Pi_M`, reference/boundary flux, `Z`, and extra/Y6 monopole terms.
