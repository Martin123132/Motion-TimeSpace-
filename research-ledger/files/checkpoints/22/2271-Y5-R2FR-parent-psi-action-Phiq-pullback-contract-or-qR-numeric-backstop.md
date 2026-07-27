# 2271 - Y5/R2FR Parent psi Action Phi/q Pullback Contract Or q_R Numeric Backstop

## Verdict

2271 turns the `psi -> g -> (Phi,q)` problem into a precise pullback contract. The exact inverse channel map is now written: `A=exp(2Phi+q/2)`, `B=exp(-2Phi+q/2)`, `C_tt=1-A`, and `C_rr=B-1`. Therefore the q-direction in covariance space is `partial_q C_tt=-A/2`, `partial_q C_rr=B/2`, while the Phi-direction is `partial_Phi C_tt=-2A`, `partial_Phi C_rr=-2B`.

That is real progress: any future derivation of finite `M_R^2`, source `j_R`, or theorem-zero `q=0` now has an exact covariance tangent to work with. But the current corpus still lacks the objects needed to pull back `A_MTS[psi]`: smoothing kernel, local projection convention, psi lift for the q tangent, effective action definition, q absence/verticality proof, matter/readout source leg, and no-gradient operator inventory.

So no local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made. The next move is either construct a minimal lawful psi covariance lift or build a strict nonclaim `q_R` profile template.

## Source Register
| source_id | source_key | source_path | exists | needles_present | validation_overall_pass | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2271_00_2270_doc | 2270_doc | 2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md | True | True |  | handoff: q is covariance mismatch; pullback contract selected |
| SRC2271_01_2270_validation | 2270_validation | source-intake/mts_residuals/P8_Y5_BRR545_2270_VALIDATION.csv | True | True | True | confirms 2270 passed before 2271 starts |
| SRC2271_02_2270_map | 2270_map | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2270_PSI_COVARIANCE_TO_PHIQ_MAP.csv | True | True |  | machine-readable psi covariance to Phi/q map |
| SRC2271_03_2270_stiffness | 2270_stiffness | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2270_STIFFNESS_SOURCE_ATTEMPT.csv | True | True |  | machine-readable missing stiffness/source pullback inputs |
| SRC2271_04_2268_split | 2268_split | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2268_PHI_Q_VARIABLE_SPLIT.csv | True | True |  | Phi/q exact variable split |
| SRC2271_05_micro_action | micro_action | core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md | True | True |  | primitive psi action and covariance metric source |
| SRC2271_06_macro_action | macro_action | core-mts-framework/action-principle/the-motion-timespace-action-principle.md | True | True |  | macro psi-gradient smoothing statement |

## Covariance Pullback Formulas
| formula_id | object | formula | use | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PBF2271_0_inverse_map | Phi/q to covariance-channel map | A=exp(2Phi+q/2), B=exp(-2Phi+q/2), C_tt=1-A, C_rr=B-1 | turns a proposed Phi/q history into the covariance components the psi map must realize | EXACT_FORMULA | False |
| PBF2271_1_q_tangent | q-direction at fixed Phi | partial_q C_tt=-A/2, partial_q C_rr=B/2; at q=0 this is (-exp(2Phi)/2, exp(-2Phi)/2) | defines the covariance tangent whose Hessian would be M_R^2 | EXACT_TANGENT | False |
| PBF2271_2_phi_tangent | Phi-direction at fixed q | partial_Phi C_tt=-2A, partial_Phi C_rr=-2B | separates Newton-potential motion from reciprocal-strain motion in covariance space | EXACT_TANGENT | False |
| PBF2271_3_q_zero_channel_relation | reduced branch relation | q=0 iff (1-C_tt)(1+C_rr)=1; equivalently C_rr=C_tt/(1-C_tt) | the exact relation a parent psi covariance theorem must prove | EXACT_CONDITIONAL | False |
| PBF2271_4_weak_channel | linear weak-field channel | q=(C_rr-C_tt)+O(C^2) | first diagnostic for any psi covariance model or numerical backstop | DERIVED_LINEAR_TEST | False |

## Pullback Contract
| contract_id | required_object | acceptance_test | current_status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PBC2271_0_smoothing_kernel | coarse-graining/smoothing operator | define <partial_mu psi partial_nu psi>_smooth, domain, boundary, covariance, and local static radial projection | MISSING_EXPLICIT_KERNEL | without the kernel there is no computable C_tt or C_rr from psi | False |
| PBC2271_1_metric_projection | sign/frame/areal convention | declare how g_tt,g_rr are projected into A=T^2 and B=S in the local branch | PARTIAL_CONVENTION_ONLY | q and Phi are not invariantly defined until the local observer/radial frame is fixed | False |
| PBC2271_2_lift | right-inverse/lift from (Phi,q) tangent to psi variations | construct delta_q psi and delta_Phi psi such that their covariance variations match PBF2271_1 and PBF2271_2 | MISSING_PSI_LIFT | Hessians of A_MTS[psi] along q cannot be computed without a lift | False |
| PBC2271_3_effective_action | parent effective action Gamma[Phi,q] | define whether Gamma is a constrained pullback, extremized action, averaged action, or effective action after integrating microscopic psi modes | MISSING_EFFECTIVE_ACTION_DEFINITION | M_R^2 and j_R depend on which parent action is actually varied | False |
| PBC2271_4_q_absence_or_verticality | q absent/vertical theorem | prove q is absent from the image of the psi map, or q variations are quotient-vertical with matter/readout descent | MISSING_ABSENCE_VERTICALITY_PROOF | this is the only route to derived q=0 without finite residual scoring | False |
| PBC2271_5_stiffness_hessian | M_R^2 | compute second_q Gamma at q=0 in declared units and prove sign/positivity if using finite stiffness | MISSING_MR2 | without M_R^2 the finite q_R branch has no theory coefficient | False |
| PBC2271_6_source_leg | j_R | compute first q-source leg from matter/readout with J_R=j_R L+O(L^2) | MISSING_JR | without j_R the q_R ratio cannot be formed | False |
| PBC2271_7_no_gradient_guard | q operator inventory | show the pullback does not generate nabla q kinetic/boundary momentum, or explicitly retain W_q and Q_R hair | MISSING_OPERATOR_INVENTORY | finite algebraic q_R is safe only if it does not secretly become a Q_R/r hair field | False |
| PBC2271_8_verdict | claim-grade Phi/q pullback package | PBC2271_0 through PBC2271_7 pass jointly | PULLBACK_CONTRACT_UNSIGNED | current corpus cannot yet derive local GR or score finite q_R from psi | False |

## Hessian / Source Ledger
| ledger_id | target | definition | needed_inputs | current_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HSL2271_0_MR2_definition | M_R^2 | M_R^2 := second derivative of Gamma[Phi,q] with respect to q at q=0, normalized to L_q=-1/2 M_R^2 q^2 | effective action Gamma; psi lift delta_q psi; units; background Phi; density convention | MISSING_EFFECTIVE_ACTION_AND_LIFT | False | False |
| HSL2271_1_jR_definition | j_R | J_R=j_R L+O(L^2), where J_R is the q-directed matter/readout source | matter/readout action in Phi/q variables; source normalization; L=2GM/(rc^2) convention | MISSING_MATTER_READOUT_PULLBACK | False | False |
| HSL2271_2_qR_ratio | q_R | q_R=j_R/M_R^2 for the algebraic finite branch | HSL2271_0 and HSL2271_1 with compatible units and no-gradient guard | MISSING_RATIO_INPUTS | False | False |
| HSL2271_3_absence_switch | q=0 theorem | q theorem-zero can replace q_R only if q is absent/vertical before variation | q absence/vertical proof plus matter/readout descent | THEOREM_ZERO_FALSE_CURRENT_CORPUS | False | False |

## q_R Numeric Backstop Intake
| backstop_id | target | purpose | required_fields | current_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NB2271_0_covariance_data | C_tt;C_rr profile | if analytic pullback fails, a toy/numeric psi covariance model must output C_tt and C_rr before q can be estimated | psi_profile; smoothing_kernel; C_tt(r); C_rr(r); frame; units; source_path | MISSING_NUMERIC_PROFILE | False | False |
| NB2271_1_q_profile | q(r) | compute q=ln[(1-C_tt)(1+C_rr)] and weak q_R coefficient | q_profile; L_profile; fit_window; q_R_fit; uncertainty; no_gradient_policy | MISSING_Q_PROFILE | False | False |
| NB2271_2_comparator_gate | local bounds | screen a parent/numeric q_R after it exists | PPN/R10/clock/orbital bounds; projection kernels; no-cancellation guard | COMPARATOR_ONLY_NOT_THEORY_VALUE | False | False |

## Refusal Runner
| refusal_id | attempted_claim | runner_result | blocked_by | score_eligible | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2271_0_pullback_claim | A_MTS[psi] has been pulled back to Gamma[Phi,q] | BLOCKED | PBC2271_8_verdict=PULLBACK_CONTRACT_UNSIGNED | False | False |
| REF2271_1_q_zero | q is absent/vertical and local GR is derived | BLOCKED | PBC2271_4_q_absence_or_verticality missing | False | False |
| REF2271_2_finite_qR | finite q_R can be scored | BLOCKED | M_R^2, j_R, and no-gradient guard missing | False | False |
| REF2271_3_numeric_backstop | numeric q_R backstop is live | BLOCKED | C_tt/C_rr/q profiles and fit window missing | False | False |

## Claim Gates
| claim_id | claim | gate_pass | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2271_0_formulas | covariance pullback formulas are exact | False | formula readiness is not a physical derivation claim | False |
| CG2271_1_pullback | parent pullback exists | False | smoothing kernel, lift, and effective action missing | False |
| CG2271_2_zero | q theorem-zero/local GR | False | q absence/vertical proof missing | False |
| CG2271_3_finite | finite q_R coefficient | False | M_R^2 and j_R missing | False |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2271_0_formula_gain | PULLBACK_TANGENTS_LOCKED | the q and Phi covariance tangents are now explicit, so future Hessian/source work has a target direction | use PBF2271_1 and PBF2271_2 for any q Hessian/source calculation | False |
| DEC2271_1_contract | PARENT_PULLBACK_CONTRACT_UNSIGNED | kernel, lift, effective action, q absence/verticality, M_R^2, j_R, and no-gradient guard are missing | do not claim derived local GR or finite q_R | False |
| DEC2271_2_backstop | NUMERIC_BACKSTOP_DEFINED_NOT_LIVE | numeric path needs C_tt/C_rr profiles from a declared psi model before q_R can be estimated | build a minimal covariance toy/lift only as nonclaim scaffolding | False |
| DEC2271_3_next | MINIMAL_COVARIANCE_LIFT_OR_QR_PROFILE_NEXT | the next productive step is to attempt a minimal lift that realizes delta_q C, or produce a numeric q profile template | 2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md | False |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT2271_0_primary | 2272-Y5-R2FR-minimal-psi-covariance-lift-or-qR-profile-template.md | scripts/Y5_R2FR_minimal_psi_covariance_lift_or_qR_profile_template_2272.py | try to construct a minimal psi covariance lift realizing the Phi/q tangents; if no lawful lift is possible, create a strict nonclaim q_R profile template | selected | a lift supplies computable q Hessian/source directions, or the q_R profile template is ready but blocked until source data exist |

## Branch Copies
| copy_id | source_path | target_path | target_exists | target_parses | reason |
| --- | --- | --- | --- | --- | --- |
| BC2271_contract | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_PULLBACK_CONTRACT.csv | source-intake/rab-sector/acquisition-queue/JR2271_PHIQ_PULLBACK_CONTRACT_NONCLAIM.csv | True | True | Phi/q pullback contract copied as nonclaim queue |
| BC2271_backstop | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_QR_NUMERIC_BACKSTOP_INTAKE.csv | source-intake/rab-sector/acquisition-queue/JR2271_QR_NUMERIC_BACKSTOP_INTAKE_NONCLAIM.csv | True | True | q_R numeric backstop intake copied as nonclaim queue |
| BC2271_branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_CLAIM_GATES.csv | source-intake/microscope/branch_locked_wep/residuals/RAB_psi_action_Phiq_pullback_refusal_2271.csv | True | True | branch-locked WEP/local refusal gates |
| BC2271_beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2271_DECISION_LEDGER.csv | source-intake/beta-source/docs/RAB_PSI_ACTION_PHIQ_PULLBACK_2271_NONCLAIM.csv | True | True | portable pullback decision ledger |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2271_0_sources_exist | PASS | all cited source paths exist |
| VAL2271_1_needles_present | PASS | all cited source needles are present |
| VAL2271_2_prior_validation | PASS | 2270 validation passes |
| VAL2271_3_formulas | PASS | inverse map and covariance tangents are written |
| VAL2271_4_contract_unsigned | PASS | pullback contract is written and unsigned |
| VAL2271_5_hessian_nonclaim | PASS | M_R^2/j_R/q_R ledger remains nonclaim |
| VAL2271_6_backstop_nonclaim | PASS | numeric backstop remains nonclaim |
| VAL2271_7_refusal_blocks | PASS | refusal runner blocks local claims |
| VAL2271_8_claim_gates_blocked | PASS | claim gates are all blocked |
| VAL2271_9_next_selected | PASS | 2272 target selected |
| VAL2271_10_csv_parse | PASS | all generated 2271 CSVs parse |
| VAL2271_11_no_claim_flags | PASS | no generated score/claim/gate flags are true |
| VAL2271_12_branch_copies | PASS | branch/queue copies exist and parse |
| VAL2271_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2271_14_formalization_no_2271 | PASS | formalization-workbench has no 2271 output files |
| VAL2271_OVERALL | PASS | 2271 locks Phi/q covariance tangents, writes the parent pullback contract, keeps q_R nonclaim, and selects 2272 |

## Working Interpretation

This is a good narrowing step. We are no longer saying vaguely that `psi` creates geometry. We know exactly what `psi` must do in the local branch: either forbid the q tangent, make it quotient-vertical, or give it a computable Hessian/source ratio. The missing beam is now the lift from covariance-channel variations back into lawful `psi` variations.