# 2019 Y5 R2FR: A-Frame GR-Source Decomposition PiAres Zero Or Residual Normalization

Private checkpoint. This converts the 2018 residual target into a proper source decomposition and no-double-count gate.

## Current Verdict

The decomposition is now explicit: `Q_A^total = Q_A^GR + Q_A^proper/exact + Q_A^res`. The measured GR/Hamiltonian source piece is not evidence for an extra force; it is the Newtonian source. The only A-frame object that belongs in R10/PPN/clock/orbital tests is the residual charge `Q_A^res`, normalized by a same-frame `M_H_ref`.

`Pi_A_res=0` is still not a claim. It requires four locks at once: stable `M_H_ref`, a parent-owned `Pi_GR/H` projector, boundary exact/proper silence, and no-double-count orthogonality. Current MTS has the correct contract but not the signatures.

So the route improves again: the coupling bottleneck is now a concrete no-double-count theorem. Either every A boundary charge is measured GR source or exact gauge, or the residual A charge becomes the only finite source row to test.

## Source Register

| source_id | source_path | status | needles | note |
| --- | --- | --- | --- | --- |
| SRC2019_00_2018_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2018-Y5-R2FR-Aframe-source-boundary-action-PiA-zero-or-finite-PiA-source-prior.md | EXISTS_NEEDLES_CONFIRMED | NEXT2018_0_2019;SBA2018_4_residual_charge_target;VAL2018_OVERALL | 2018 handoff to GR-source decomposition and residual normalization. |
| SRC2019_01_2017_generator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2017-Y5-R2FR-Aframe-split-gauge-generator-boundary-charge-zero-or-finite-A-source-row.md | EXISTS_NEEDLES_CONFIRMED | SGG2017_2_constraint_candidate;SGG2017_3_boundary_charge;VAL2017_OVERALL | A split generator and total boundary charge skeleton. |
| SRC2019_02_1017_reference_lock | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md | EXISTS_NEEDLES_CONFIRMED | HRL1017_5_MHref_denominator;MHR1017_0_M_H_ref_denominator;DEC1017_1_no_MHref_shortcut | Hamiltonian source denominator and no-shortcut guard. |
| SRC2019_03_1014_projector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md | EXISTS_NEEDLES_CONFIRMED | PCT1014_0_product_rule;PCT1014_2_commutator_zero;DEC1014_1_Hodge_route_retained | Pi_M commutator/projector variation obstruction. |
| SRC2019_04_1015_hilbert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md | EXISTS_NEEDLES_CONFIRMED | SOL1015_1_source_measure;SOL1015_3_de_rham_equality;REB1015_5_M_H_ref | same Hilbert source measure and source equality conditions. |
| SRC2019_05_1019_boundary_projector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md | EXISTS_NEEDLES_CONFIRMED | PO1019_0_projector_definition;DC1019_0_orthogonal_split;DEC1019_1_best_route | boundary exactness, projector orthogonality, and no-double-count guard. |
| SRC2019_06_2018_audit_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2018_AFRAME_SOURCE_BOUNDARY_ACTION_AUDIT.csv | EXISTS_NEEDLES_CONFIRMED | SBA2018_2_total_PiA_identity;SBA2018_8_verdict | 2018 source-boundary action audit CSV. |
| SRC2019_07_2018_prior_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2018_AFRAME_RESIDUAL_SOURCE_PRIOR_ROWS.csv | EXISTS_NEEDLES_CONFIRMED | PR2018_2_PiA_res;PR2018_5_MH_normalization | 2018 residual source-prior rows. |
| SRC2019_08_1017_reference_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv | EXISTS_NEEDLES_CONFIRMED | HRL1017_5_MHref_denominator;HRL1017_6_FB5540_zero_law | reference lock law CSV. |
| SRC2019_09_671_boundary_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv | EXISTS_NEEDLES_CONFIRMED | BCG671_4_projector_orthogonality;BCG671_6_no_double_count;BCG671_7_verdict | boundary charge owner, projector, and no-double-count gates. |

## GR-Source Decomposition

| decomp_id | object | formula | status | derivation | missing_before_claim | parent_signed |
| --- | --- | --- | --- | --- | --- | --- |
| GSD2019_0_total_charge | total A split charge | Q_A^total[epsilon]=int_partialSigma epsilon_a Pi_A^{n a,total} + improvement_total | TOTAL_CHARGE_FORM_INHERITED_FROM_2017 | 2017 gives the split generator boundary term. | total charge contains GR source and residual pieces; it is not a zero target. | false |
| GSD2019_1_GR_source_piece | GR/Hamiltonian source piece | Q_A^GR[epsilon] := Pi_GR/H[Q_A^total] = delta_epsilon H_tau^GR[e_pub,psi]/delta epsilon with M_H_ref = G_ref^-1 int_S Q_tau | CONDITIONAL_DEFINITION_NOT_PARENT_SIGNED | if e=dX+A and matter is public-frame-only, the A variation pulls back to the tetrad/Hilbert source charge. | stable M_H_ref, tau lock, source worldtube, and fixed reference remain unsigned. | false |
| GSD2019_2_proper_exact_piece | proper/exact boundary piece | Q_A^proper/exact[epsilon]=0 for epsilon\|partial=0 or Q_A=d_boundary b_A with fixed closed boundary and no kernel derivative term | CONDITIONAL_BOUNDARY_EXACTNESS_ONLY | proper gauge and exact boundary forms are the legitimate zero channels. | boundary class, cohomology, corner terms, kernel derivative terms, and counterterms are not parent-signed. | false |
| GSD2019_3_residual_definition | residual A source charge | Q_A^res := Q_A^total - Q_A^GR - Q_A^proper/exact; Pi_A^{n,res} defined by Q_A^res=int_partial epsilon_a Pi_A^{n a,res}+improvements | RESIDUAL_DEFINITION_DERIVED_AS_BOOKKEEPING | this isolates extra A hair after measured GR source charge and pure gauge/exact pieces are removed. | bookkeeping identity is not a zero theorem; each subtracted piece must be parent-owned. | false |
| GSD2019_4_cocycle_decomposition | residual boundary cocycle | K_A^res = K_A^total - K_A^GR/Hamiltonian - K_A^proper/exact | RESIDUAL_COCYCLE_DEFINITION_DERIVED_AS_BOOKKEEPING | bulk split shifts are abelian, so any surviving obstruction is boundary/source/reference residue. | bracket computation and reference/counterterm silence are missing. | false |
| GSD2019_5_no_double_count_projector | no-double-count source projector | Pi_GR/H[Q_A^res]=0 and Pi_res[Q_A^GR]=0 with Q_total=Q_GR orthogonal_sum Q_res orthogonal_sum Q_exact | PROJECTOR_ORTHOGONALITY_REQUIRED_NOT_DERIVED | residual A hair must not be counted once as measured mass and again as fifth-force hair. | Pi_M^H definition, symplectic block, reference silence, and source/edge independence are unsigned. | false |
| GSD2019_6_zero_theorem_contract | Pi_A_res zero theorem | Pi_A^{res}=0 and K_A^{res}=0 if public-frame source measure, M_H_ref, exact/proper boundary class, and projector orthogonality all close | VALID_CONDITIONAL_THEOREM_CONTRACT | this is the local-GR route: all A boundary charge is either measured GR source or pure gauge/exact. | the required clauses are spread across unsigned 1017, 1019, 1045, and 2018 gates. | false |
| GSD2019_7_finite_residual_fallback | residual-normalized finite A branch | alpha_A^res(lambda)=K_A(lambda) Qbar_AH^res(lambda) qbar_AT /(4*pi*Z_A*G_ref) plus absolute tails, normalized by M_H_ref | SCHEMA_READY_VALUES_MISSING | if residual zero fails, compare only the residual source charge, not total measured mass. | Z_A, lambda_A, K_A, Qbar_AH^res, qbar_AT, M_H_ref, and promoted bound rows are missing. | false |
| GSD2019_8_verdict | GR-source decomposition for A-frame residual | Q_A^total=Q_A^GR+Q_A^proper/exact+Q_A^res and only Q_A^res is test/fifth-force material | DECOMPOSITION_WRITTEN_RESIDUAL_ZERO_NOT_SIGNED | the A-coupling problem is now a no-double-count residual source-normalization problem. | M_H_ref, projector orthogonality, exact boundary class, and residual coefficients remain unsigned. | false |

## Residual-Normalized Rows

| row_id | symbol | meaning | status | numeric_value | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RN2019_0_M_H_ref | M_H_ref | same-frame Hamiltonian/Noether source denominator | MISSING_STABLE_MH_REF | MISSING | mass_or_charge | false | false |
| RN2019_1_QA_total | Q_A^total | raw A split boundary charge from 2017 generator | FORMULA_ONLY_NOT_ZERO_TARGET | MISSING | A-charge | false | false |
| RN2019_2_QA_GR | Q_A^GR | measured GR/Hamiltonian source contribution to A variation | MISSING_GR_SOURCE_MAP | MISSING | A-charge | false | false |
| RN2019_3_QA_exact | Q_A^proper/exact | proper gauge or exact boundary contribution | MISSING_BOUNDARY_EXACTNESS_CERTIFICATE | MISSING | A-charge | false | false |
| RN2019_4_QA_res | Q_A^res | extra residual A source charge after subtraction | CORRECT_ZERO_OR_BOUND_TARGET_MISSING_VALUE | MISSING | A-charge | false | false |
| RN2019_5_KA_res | K_A^res | residual boundary cocycle | MISSING_BRACKET_AND_REFERENCE_LOCK | MISSING | charge_algebra_units | false | false |
| RN2019_6_Qbar_AH_res | Qbar_AH^res(lambda) | Hamiltonian/source projection of residual A charge | MISSING_PROJECTOR_OR_BOUND | MISSING | dimensionless_or_declared | false | false |
| RN2019_7_qbar_AT | qbar_AT | test/readout coupling to residual A | MISSING_TEST_LEG | MISSING | dimensionless | false | false |
| RN2019_8_alphaA_res | alpha_A^res(lambda) | Yukawa-equivalent residual A strength | MISSING_ALL_JOIN_INPUTS | MISSING | dimensionless | false | false |
| RN2019_9_no_cancellation_guard | abs_envelope_Ares | absolute sum of residual A plus retained boundary/source tails | NOT_COMPUTED_COMPONENTS_MISSING | MISSING | dimensionless | false | false |

## Claim Gates

| gate_id | gate | passed_for_nonclaim | passed_for_claim | reason |
| --- | --- | --- | --- | --- |
| CG2019_0_decomposition_written | Q_A total decomposition is explicit | true | false | GR, proper/exact, and residual pieces are separated |
| CG2019_1_total_not_scored | Q_A_total is not used as fifth-force source | true | false | prevents measured-mass double counting |
| CG2019_2_MHref_owned | M_H_ref is stable same-frame denominator | false | false | 1017 source-measure/reference locks remain unsigned |
| CG2019_3_projector_orthogonal | GR source and residual A projectors are orthogonal | false | false | Pi_M^H definition, symplectic block, and source independence are not derived |
| CG2019_4_boundary_exact | proper/exact boundary piece is theorem-zero | false | false | boundary cohomology/counterterm/cocycle gates remain open |
| CG2019_5_PiAres_zero | Pi_A_res and K_A_res vanish | false | false | requires M_H_ref, projector orthogonality, boundary exactness, and matter/source silence together |
| CG2019_6_residual_score_ready | finite residual A comparator row is score-ready | false | false | all residual coefficients and test/source legs are missing |
| CG2019_7_local_GR_Newton | local GR/Newton reduction from A branch is derived | false | false | residual zero theorem is not parent-signed |

## Refusal Runner

| refusal_id | attempted_claim | verdict | reason | accepted_for_claim |
| --- | --- | --- | --- | --- |
| REF2019_0_score_total_QA | score Q_A_total as fifth-force source | REFUSE | Q_A_total includes measured GR/Hamiltonian mass source and would double count Newtonian mass. | false |
| REF2019_1_MHref_shortcut | use orbital GM, bare mass, or reference 1 as M_H_ref | REFUSE | 1017 forbids replacing the source theorem denominator with the readout being derived. | false |
| REF2019_2_PiAres_zero | claim Pi_A_res=0 | REFUSE | M_H_ref, projector orthogonality, boundary exactness, and source/functor silence are not signed together. | false |
| REF2019_3_KAres_zero | claim K_A_res=0 | REFUSE | residual boundary bracket and reference/counterterm silence are uncomputed. | false |
| REF2019_4_residual_score | score alpha_A_res(lambda) | REFUSE | Z_A, lambda_A, K_A, Qbar_AH_res, qbar_AT, profile, and bounds are missing. | false |
| REF2019_5_local_GR | claim local GR/Newton reduction | REFUSE | A residual source theorem remains open and finite residual rows are nonclaim. | false |

## Decision Ledger

| decision_id | verdict | rationale | next_action |
| --- | --- | --- | --- |
| DEC2019_0_result | A_FRAME_SOURCE_DECOMPOSITION_WRITTEN_RESIDUAL_ZERO_UNSIGNED | Q_A_total is now decomposed into measured GR/Hamiltonian source, proper/exact boundary, and residual A hair. Only the residual belongs in local fifth-force tests. | do not score total A charge; attack M_H_ref/Pi_GR owner and projector orthogonality next |
| DEC2019_1_route_status | LOCAL_GR_ROUTE_IS_NOW_A_NO_DOUBLE_COUNT_THEOREM | To reduce to GR/Newton, MTS must show every A boundary charge is either the ordinary measured source or pure gauge/exact, with no residual projection. | derive M_H_ref plus Pi_GR map before attempting R10/PPN scoring |
| DEC2019_2_testing_status | FINITE_A_TESTING_REQUIRES_RESIDUAL_NORMALIZATION | If residual A survives, its amplitude must be normalized by same-frame M_H_ref and absolute-summed with no cancellation against unknown boundary/source tails. | create residual rows only after source/test legs and M_H_ref are sourced |

## Branch Copies

| copy_id | path | exists | note |
| --- | --- | --- | --- |
| COPY2019_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_GR_SOURCE_DECOMPOSITION_2019_NONCLAIM.csv | true | A-frame GR-source decomposition nonclaim copy |
| COPY2019_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2019_AFRAME_RESIDUAL_SOURCE_STATUS_NONCLAIM.csv | true | A-frame residual source claim-gate status nonclaim copy |
| COPY2019_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2019_AFRAME_RESIDUAL_NORMALIZED_SOURCE_QUEUE.csv | true | A-frame residual-normalized source queue |

## Next Target

| target_id | next_doc | objective | required_inputs | excluded |
| --- | --- | --- | --- | --- |
| NEXT2019_0_2020 | 2020-Y5-R2FR-Aframe-MHref-PiGR-owner-or-PiAres-first-row.md | derive the same-frame Hamiltonian source denominator M_H_ref and Pi_GR/H map needed to subtract measured GR mass from Q_A_total; if not, create the first residual-normalized Pi_A_res row without claims | Q_tau integral; fixed H_ref; tau lock; source worldtube; public tetrad source measure; Pi_GR/H projector; no-double-count proof; M_H_ref units; Pi_A_res schema | orbital GM denominator; bare mass shortcut; total Q_A scoring; reference-only zero; cancellation between unknown residuals; R10/local-GR claim; GitHub; formalization-workbench edits |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL2019_00_sources | PASS | all cited source paths exist and needles are found |
| VAL2019_01_decomposition_written | PASS | Q_A total decomposition is explicit |
| VAL2019_02_total_not_scored | PASS | total Q_A scoring is refused |
| VAL2019_03_projector_gate_present | PASS | no-double-count projector gate is present |
| VAL2019_04_zero_not_promoted | PASS | Pi_A_res zero is not falsely promoted |
| VAL2019_05_residual_rows_nonclaim | PASS | residual-normalized rows remain missing/nonclaim |
| VAL2019_06_claim_gates_blocked | PASS | all claim gates remain blocked |
| VAL2019_07_refusals_active | PASS | refusals remain active |
| VAL2019_08_csv_parse | PASS | all generated CSV outputs parse cleanly |
| VAL2019_09_branch_copies | PASS | branch-copy CSVs exist and parse |
| VAL2019_10_no_formalization_edits | PASS | formalization-workbench modified-file count remains 0 for this run |
| VAL2019_11_output_scope | PASS | all outputs are under post-checkpoint-work |
| VAL2019_OVERALL | PASS | 2019 A-frame GR-source decomposition Pi_A_res zero or residual normalization |
