# 2018 Y5 R2FR: A-Frame Source-Boundary Action PiA Zero Or Finite PiA Source Prior

Private checkpoint. This tests whether the source/boundary action kills the A-frame boundary charge, or whether finite A source rows must be retained.

## Current Verdict

The target changes in an important way. The total `Pi_A^n` should **not** be forced to zero. In the strict e-only branch, varying `A` at fixed `X` is just varying the public tetrad, so `Pi_A^{n,total}` inherits the ordinary tetrad/Hilbert source momentum. A compact mass source should carry that; otherwise we erase the Newtonian source itself.

The correct local-GR zero theorem is therefore residual: split `Pi_A^{n,total}=Pi_GR/Hamiltonian^n + Pi_A^{n,res} + proper/exact boundary pieces`. The GR/Hamiltonian piece is the measured mass source. The object that must vanish or be bounded is `Pi_A^{n,res}` and its cocycle `K_boundary^{A,res}`.

This is a genuine route improvement: the coupling bottleneck is no longer just 'missing coupling'. It is now a source-normalization/no-double-count problem. No local-GR/R10/PPN claim is made yet because the residual decomposition and Hamiltonian normalization are still unsigned.

## Source Register

| source_id | source_path | status | needles | note |
| --- | --- | --- | --- | --- |
| SRC2018_00_2017_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md | EXISTS_NEEDLES_CONFIRMED | NEXT2017_0_2018;SGG2017_3_boundary_charge;VAL2017_OVERALL | 2017 handoff to source-boundary Pi_A zero or finite source-prior row. |
| SRC2018_01_2010_no_spurion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md | EXISTS_NEEDLES_CONFIRMED | NSP2010_0_matter_functor;NSP2010_5_boundary_source_measure;NSP2010_6_verdict | A-frame ordinary matter/source no-spurion clauses. |
| SRC2018_02_2012_PiA_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md | EXISTS_NEEDLES_CONFIRMED | NHA2012_0_target;FQA2012_1_PiA;DEC2012_1_best_derivation_route | finite Pi_A/Q_A rows and source-neutrality target. |
| SRC2018_03_2013_boundary_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md | EXISTS_NEEDLES_CONFIRMED | BNA2013_1_variation_formula;BNA2013_3_fixed_boundary_risk;VAL2013_OVERALL | prior boundary/source neutrality attempt and countermodel. |
| SRC2018_04_410_functor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\410-quotient-matter-functor-theorem-attempt.md | EXISTS_NEEDLES_CONFIRMED | S_matter = sum_A S_A;delta S_matter / delta Z_I;local_GR_promoted | early quotient matter functor theorem and counterexample warning. |
| SRC2018_05_1045_functor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md | EXISTS_NEEDLES_CONFIRMED | MFS1045_0_parent_field_quotient;VLG1045_3_boundary_lift;DEC1045_0_theorem_shape | matter functor descent signature and boundary-lift gap. |
| SRC2018_06_767_reaudit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv | EXISTS_NEEDLES_CONFIRMED | PMR767_0_explicit_parent_matter_functor;PMR767_5_domain_selection_predata | parent matter functor reaudit. |
| SRC2018_07_HSM541_source_measure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | EXISTS_NEEDLES_CONFIRMED | HSM541_1_integrable_charge;HSM541_2_observed_worldtube_source;HSM541_4_zero_extra_source_channels | Hamiltonian/source-measure contract. |
| SRC2018_08_667_boundary_action | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv | EXISTS_NEEDLES_CONFIRMED | PBA667_2_boundary_action;PBA667_3_charge_definition;PBA667_5_denominator_rule | parent boundary-action ansatz and charge definition. |
| SRC2018_09_671_boundary_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv | EXISTS_NEEDLES_CONFIRMED | BCG671_1_proper_gauge;BCG671_5_boundary_cocycle;BCG671_7_verdict | boundary charge owner/proper/exact/cocycle gates. |
| SRC2018_10_reciprocal_neutrality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\06-reciprocal-charge-source-neutrality.md | EXISTS_NEEDLES_CONFIRMED | Pi_R = 0 -> Q_R = 0;fixed source R_AB boundary;Q_R neutrality is the missing source theorem | analogy showing source momentum zero is a real source theorem, not a conservation shortcut. |

## Source-Boundary Action Audit

| attempt_id | object | formula | status | derivation | why_not_claim | claim_result | parent_signed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SBA2018_0_source_action_domain | parent source/boundary action | S_source+boundary = S_src[Psi,e,omega[e],theta] + B_GR[e] + B_ref + B_extra | CONDITIONAL_E_ONLY_SOURCE_GRAMMAR | if no direct X/A/Phi_MTS/q_loc/source-marker argument exists, visible matter is split-gauge invariant. | the actual parent source/boundary action and B_extra exclusion are not signed. | nonclaim | false |
| SBA2018_1_variation_split | source variation under e=dX+A | delta S_src = int_W E_e^a_mu delta e_a^mu + int_partialW Pi_e^{n a} delta e_a + ... with delta e = d(delta X)+delta A | CHAIN_RULE_FORM_DERIVED_CONDITIONAL | A variation at fixed X pulls back to the tetrad/coframe variation. | Pi_e and boundary terms require the parent symplectic/source measure. | nonclaim | false |
| SBA2018_2_total_PiA_identity | total A normal momentum | Pi_A^{n a,total} = Pi_e^{n a} + Pi_A^{n a,extra} + Pi_A^{n a,edge} | TOTAL_PIA_IS_NOT_THE_RIGHT_ZERO_TARGET | in the e-only branch Pi_A inherits the ordinary tetrad/Hilbert source momentum. | ordinary compact mass sources should have a nonzero GR/Hilbert source momentum. | do_not_set_total_PiA_to_zero | false |
| SBA2018_3_split_charge_cancellation | combined split transformation | delta_epsilon X=epsilon, delta_epsilon A=-D epsilon, delta_epsilon e=0, so delta_epsilon S_src=0 inside e-only grammar | SPLIT_INVARIANCE_NOT_TOTAL_CHARGE_ZERO | the X and A variations cancel in the public tetrad channel. | cancellation of the combined generator does not imply Pi_A^{n,total}=0. | nonclaim | false |
| SBA2018_4_residual_charge_target | extra A charge after GR source subtraction | Pi_A^{n,res} := Pi_A^{n,total} - Pi_e^{n,GR/Hamiltonian}[M_H,e_pub] - Pi_A^{n,proper/exact} | CORRECT_ZERO_TARGET_IDENTIFIED | local GR needs no extra A hair beyond the measured GR/Hamiltonian source charge, not zero total source momentum. | the GR/Hamiltonian subtraction map and exact/proper boundary class are not parent-owned yet. | residual_zero_target_nonclaim | false |
| SBA2018_5_matter_functor_implication | no-spurion matter/source silence | partial_A_direct S_src\|e = 0 and partial_marker S_src = 0 if matter functor is strictly public-frame only | DIRECT_SPURION_SOURCE_BLOCKED_CONDITIONALLY | e-only/no-marker grammar kills direct representative-field source coupling. | 1045/767 keep matter functor and boundary lift unsigned. | nonclaim | false |
| SBA2018_6_Kboundary_residual | boundary cocycle after source subtraction | K_boundary^{A,res}=K_boundary^{A,total}-K_boundary^{GR/Hamiltonian}-K_boundary^{proper/exact} | RESIDUAL_COCYCLE_TARGET_IDENTIFIED | bulk split shifts are abelian; only boundary/source/reference terms can leave an obstruction. | the parent bracket, Q_A differentiability, and reference subtraction are missing. | nonclaim | false |
| SBA2018_7_counterexample | ordinary massive e-only source | S_src=-m int ds[e] is split-invariant but delta S_src/delta A = delta S_src/delta e is not zero | COUNTEREXAMPLE_TO_TOTAL_PIA_ZERO | a source can be perfectly public-frame-only and still carry the GR stress/mass source. | therefore Pi_A^{total}=0 is too strong and would erase Newtonian mass. | blocks_total_zero_shortcut | false |
| SBA2018_8_verdict | source-boundary Pi_A zero theorem | Pi_A^{n,res}=0 and K_boundary^{A,res}=0 are the viable local-GR targets; Pi_A^{n,total}=0 is rejected | TOTAL_ZERO_REJECTED_RESIDUAL_ZERO_NOT_SIGNED | the route now separates GR/Newton source charge from extra A hair. | residual subtraction, source normalization, boundary exactness, and matter functor descent are still unsigned. | finite_residual_rows_retained | false |

## Residual Source-Prior Rows

| prior_id | symbol | meaning | status | numeric_value | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PR2018_0_PiA_total | Pi_A^{n,total} | normal A momentum at source/boundary | NOT_ZERO_TARGET_GR_SOURCE_INCLUDED | MISSING | action/A/area | false | false |
| PR2018_1_PiA_GR | Pi_e^{n,GR/Hamiltonian} | ordinary tetrad/Hamiltonian source momentum to be absorbed into measured mass | MISSING_GR_SOURCE_SUBTRACTION_MAP | MISSING | action/e/area | false | false |
| PR2018_2_PiA_res | Pi_A^{n,res} | extra A source momentum after GR/proper/exact subtraction | CORRECT_ZERO_OR_BOUND_TARGET | MISSING | action/A/area | false | false |
| PR2018_3_QA_res | Q_A^{res}[epsilon] | int_partial epsilon_a Pi_A^{n,res a} plus residual improvements | MISSING_RESIDUAL_BOUNDARY_CHARGE | MISSING | A-charge | false | false |
| PR2018_4_Kboundary_res | K_boundary^{A,res} | residual split-gauge boundary cocycle | MISSING_RESIDUAL_BRACKET | MISSING | charge algebra units | false | false |
| PR2018_5_MH_normalization | M_H_ref | measured Hamiltonian/Noether mass denominator used to remove GR source charge | MISSING_SOURCE_NORMALIZATION | MISSING | mass | false | false |
| PR2018_6_alphaA_res | alpha_A^{res}(lambda_A) | R10 Yukawa-equivalent amplitude from residual A hair only | MISSING_ZA_KAPPA_LAMBDA_P00_PROFILE | MISSING | dimensionless | false | false |
| PR2018_7_PPN_res | delta_PPN_A^{res} | PPN residual vector after GR source subtraction | MISSING_ARENA_PROJECTION | MISSING | dimensionless | false | false |

## Claim Gates

| gate_id | gate | passed_for_nonclaim | passed_for_claim | reason |
| --- | --- | --- | --- | --- |
| CG2018_0_total_zero_rejected | total Pi_A zero is rejected as a GR-source eraser | true | false | ordinary e-only mass sources can have nonzero Pi_A=Pi_e |
| CG2018_1_residual_target_written | Pi_A residual zero target is explicit | true | false | Pi_A_res = Pi_A_total - Pi_GR/Hamiltonian - proper/exact pieces |
| CG2018_2_matter_functor_sufficient | matter functor alone proves Pi_A_res=0 | false | false | functor kills direct spurions, not boundary/source/reference residuals |
| CG2018_3_PiA_res_zero | Pi_A_res=0 is parent-derived | false | false | GR subtraction map, source normalization, and boundary exactness are unsigned |
| CG2018_4_Kboundary_res_zero | K_boundary_A_res=0 is parent-derived | false | false | boundary bracket/reference subtraction are not computed |
| CG2018_5_finite_residual_score | finite residual A source row is score-ready | false | false | numeric/source-backed residual coefficients missing |
| CG2018_6_local_GR_Newton | local GR/Newton reduction from A branch is derived | false | false | residual zero theorem remains unsigned |

## Refusal Runner

| refusal_id | attempted_claim | verdict | reason | accepted_for_claim |
| --- | --- | --- | --- | --- |
| REF2018_0_total_PiA_zero | claim Pi_A^{total}=0 | REFUSE | would erase ordinary GR/Newton source momentum for e-only massive matter; correct target is residual Pi_A. | false |
| REF2018_1_matter_functor_zero | claim no-spurion matter functor proves source-boundary zero | REFUSE | it blocks direct spurions but does not compute boundary momentum, source normalization, or exact/proper charge. | false |
| REF2018_2_residual_zero | claim Pi_A^{res}=0 | REFUSE | GR/Hamiltonian subtraction map, M_H_ref, boundary exactness, and K_boundary residual are unsigned. | false |
| REF2018_3_finite_residual_score | score finite A residual | REFUSE | Pi_A_res, Q_A_res, Z_A, lambda_A, kappa_A, P_00, and arena projections are missing. | false |
| REF2018_4_local_GR | claim local GR/Newton derivation | REFUSE | A branch is sharper but residual source theorem is not closed. | false |

## Decision Ledger

| decision_id | verdict | rationale | next_action |
| --- | --- | --- | --- |
| DEC2018_0_result | TOTAL_PIA_ZERO_REJECTED_RESIDUAL_PIA_TARGET_IDENTIFIED | The source-boundary action attempt shows that total Pi_A should include the ordinary tetrad/Hilbert source momentum in the e-only branch. Killing total Pi_A would also kill the Newtonian source. | target Pi_A_res and K_boundary_A_res, not total Pi_A |
| DEC2018_1_actual_progress | A_COUPLING_BOTTLENECK_IS_NOW_A_GR_SOURCE_SUBTRACTION_PROBLEM | The correct local-GR question is whether the A boundary charge is only the GR/Hamiltonian mass source or whether an extra residual A charge remains. | derive the GR-source decomposition and no-double-count projector next |
| DEC2018_2_testing_status | FINITE_A_TESTING_REMAINS_BLOCKED_BUT_BETTER_NORMALIZED | Future R10/PPN rows must use residual A hair after measured-mass normalization, not total source momentum. | do not score A residuals until Pi_A_res, M_H_ref, and projection coefficients are real |

## Branch Copies

| copy_id | path | exists | note |
| --- | --- | --- | --- |
| COPY2018_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_SOURCE_BOUNDARY_PIA_2018_NONCLAIM.csv | true | A-frame source-boundary Pi_A audit nonclaim copy |
| COPY2018_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2018_AFRAME_PIA_RESIDUAL_STATUS_NONCLAIM.csv | true | A-frame Pi_A residual claim-gate status nonclaim copy |
| COPY2018_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2018_AFRAME_PIA_RESIDUAL_SOURCE_PRIOR_QUEUE.csv | true | A-frame Pi_A residual source-prior queue |

## Next Target

| target_id | next_doc | objective | required_inputs | excluded |
| --- | --- | --- | --- | --- |
| NEXT2018_0_2019 | 2019-Y5-R2FR-Aframe-GR-source-decomposition-PiAres-zero-or-residual-normalization.md | derive the decomposition Pi_A_total = Pi_GR/Hamiltonian + Pi_A_res + proper/exact boundary terms, prove Pi_A_res=0 and K_boundary_A_res=0 if possible, or build residual-normalized finite A rows | GR/tetrad source momentum; Hamiltonian mass M_H_ref; public tetrad source measure; boundary exact/proper class; K_boundary residual bracket; no-double-count projector; Pi_A_res units; R10/PPN residual routing | total Pi_A zero shortcut; matter-functor-only zero; measured mass double counting; invented residual coefficients; R10/local-GR claim; GitHub; formalization-workbench edits |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL2018_00_sources | PASS | all cited source paths exist and needles are found |
| VAL2018_01_total_zero_rejected | PASS | total Pi_A zero shortcut is rejected |
| VAL2018_02_residual_target_written | PASS | Pi_A residual target is explicit |
| VAL2018_03_counterexample_present | PASS | e-only massive source counterexample blocks total-zero overclaim |
| VAL2018_04_verdict_nonclaim | PASS | residual zero not falsely promoted |
| VAL2018_05_priors_nonclaim | PASS | residual source-prior rows remain missing/nonclaim |
| VAL2018_06_claim_gates_blocked | PASS | all claim gates remain blocked |
| VAL2018_07_refusals_active | PASS | refusals remain active |
| VAL2018_08_csv_parse | PASS | all generated CSV outputs parse cleanly |
| VAL2018_09_branch_copies | PASS | branch-copy CSVs exist and parse |
| VAL2018_10_no_formalization_edits | PASS | formalization-workbench modified-file count remains 0 for this run |
| VAL2018_11_output_scope | PASS | all outputs are under post-checkpoint-work |
| VAL2018_OVERALL | PASS | 2018 A-frame source-boundary action Pi_A zero or finite Pi_A source prior |
