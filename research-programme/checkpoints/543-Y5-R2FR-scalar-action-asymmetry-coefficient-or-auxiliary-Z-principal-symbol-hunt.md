# 4527 — Scalar Action-Asymmetry Coefficient Or Auxiliary Z Principal-Symbol Hunt

Marker: `PPC4161_SCALAR_ACTION_ASYMMETRY_COEFFICIENT_OR_AUXILIARY_Z_PRINCIPAL_SYMBOL_HUNT_4527`  
Packet marker: `PPC4161_PACKET_SCALAR_ACTION_ASYMMETRY_COEFFICIENT_OR_AUXILIARY_Z_PRINCIPAL_SYMBOL_HUNT_4527`  
Decision: `ACTION_ODD_FORCE_AND_VERTICAL_PRINCIPAL_SYMBOL_LAWS_DERIVED_NO_EXISTING_PARENT_ZERO_SOURCE_YET_DUAL_RUNNER_INPUTS_READY`  
Claim: `L-369`  
Status: private conditional non-claim; action/principal-symbol laws derived, parent values not sourced.

## What Moved

4527 turns the remaining parent-Z gap into a hard field-theory fork.

```text
S_odd = (S[z] - S[I_q z]) / 2
A_A = delta S_odd / delta z^A |_{z=0}
K_AB^{mu nu} = d^2 L / d(nabla_mu z^A)d(nabla_nu z^B)
```

If `A_A=0` and `K_AB^{mu nu}=0` are found in the existing parent action, the rank-zero local branch becomes much more derivable. If either survives, it is no longer a vague missing piece: `A_A` feeds the algebraic residual and `K_AB` selects either finite-range scoring or a stability/long-range guard. A new auxiliary constraint is explicitly refused unless it descends from existing MTS variables with stress/Ward/matter readout included.

## Action Odd-Force Theorem

| theorem_id | statement | formula | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AOF4527_0_odd_even_split | In a parent vertical collar, split the action into I_q-even and I_q-odd pieces. | S_even=(S[z]+S[I_q z])/2; S_odd=(S[z]-S[I_q z])/2 | only S_odd can source the first vertical force at z=0 | DERIVED | False |
| AOF4527_1_first_force | The dangerous scalar/action residual is the first variation of S_odd at the local section. | A_A := delta S_odd/delta z^A |_{z=0}; F_A(0)=A_A | F_1=0 follows if and only if A_A=0 in every physical vertical source direction | DERIVED | False |
| AOF4527_2_epsilon_link | The 4526 action-asymmetry scalar epsilon_I is not itself the force, but it bounds the force only after a local Lipschitz/diameter control is sourced. | ||A|| <= C_I epsilon_I / ell_z, with C_I and ell_z sourced from the parent collar | epsilon_I needs collar constants before entering alpha/PPN scoring numerically | BOUND_FORM_DERIVED_VALUES_MISSING | False |
| AOF4527_3_scalar_channel_projection | The 128 scalar survivor coefficients are the components of A_A projected onto z_theta, z_dotB and z_Lcg. | a_i = e_i^A A_A / N_i, i in {theta,dotB,Lcg} | a_theta, a_dotB and a_Lcg are no longer vague blockers; they are action-odd force components | PROJECTION_DERIVED_NORMALIZATION_MISSING | False |
| AOF4527_4_no_parentless_auxiliary | Adding a new Lagrange multiplier or auxiliary action can force A_A=0, but 1192 shows that this is closure unless the variable, stress, Ward identity and matter readout are already parent-owned. | new constraint action != MTS derivation unless it descends from existing S_parent | 4527 refuses the magic auxiliary shortcut | NO_CLOSURE_SHORTCUT | False |

## Auxiliary Z Principal-Symbol Test

| test_id | test | formula | if_zero_or_signed | if_nonzero | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| APS4527_0_vertical_quadratic_form | extract vertical second-order parent Lagrangian | L_z^(2)=1/2 K_AB^{mu nu} nabla_mu z^A nabla_nu z^B + 1/2 M_AB z^A z^B + A_A z^A | K=0 gives auxiliary/rank-zero branch; M_AB and A_A decide lock/residual | rank/sign of K selects finite-range or instability branch | FORMULA_DERIVED_PARENT_K_MISSING | False |
| APS4527_1_principal_symbol | compute physical vertical principal symbol | Z_AB(xi)=K_AB^{mu nu} xi_mu xi_nu on Q_phys after gauge/constraint reduction | rank(Z_AB)=0 becomes parent-derived | use 4519 finite-range classifier | SOURCE_SWEEP_REQUIRED | False |
| APS4527_2_rank_zero_gate | rank-zero algebraic branch | rank Z=0 and M_AB coercive => M_AB z^B=-A_A-R_A^other | if A_A and other RHS vanish, z=0 | finite algebraic residual bound via m_min^{-1} sum_abs RHS | MISSING_K_ZERO_MMIN_A_ZERO | False |
| APS4527_3_finite_range_gate | finite-range branch | M_AB v_i = mu_i^2 Z_AB v_i; lambda_i=1/mu_i | not applicable if rank Z=0 | alpha_i(lambda_i) runner must score source/test charges and bound curve | READY_IF_K_NONZERO_VALUES_SOURCED | False |
| APS4527_4_torsion_analogy_limit | use 4451 only as structural analogy | no kinetic term -> algebraic equation, but only for the sector whose parent action actually lacks kinetic terms | helps define the required proof shape | does not prove parent Z is auxiliary | ANALOGY_NOT_SOURCE | False |

## Branch Decision Matrix

| branch_id | condition | result | current_status | next_input | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BDM4527_0_parent_even_auxiliary | A_A=0, K_AB^{mu nu}=0, M_AB coercive/constraint-owned in one existing parent branch | rank-zero local GR/Newton route becomes materially stronger | NOT_PROVED | existing parent action source for A_A=0 and K=0 | False |
| BDM4527_1_action_odd_rank_zero | K=0 but A_A or scalar components survive | algebraic residual z=-M^{-1}A feeds PPN/R10/clock/orbit via 4524 | SCORING_BRANCH_READY_VALUES_MISSING | A_A components and m_min | False |
| BDM4527_2_finite_range | rank K > 0 with positive generalized eigenvalues | finite range alpha(lambda) branch; no rank-zero claim | SCORING_BRANCH_READY_VALUES_MISSING | Z_AB, M_AB, Qbar_XS, qbar_XT, bound curve | False |
| BDM4527_3_bad_sign_or_zero_mode | K or M has wrong sign, massless physical zero mode, or unconstrained null | stability/long-range local-test branch opens | GUARD_READY_VALUES_MISSING | constraint algebra, spectrum and local-test residual vector | False |
| BDM4527_4_current_verdict | current corpus | no parent-zero source found; dual runner/input route remains live | NO_CLAIM | 4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md | False |

## Coefficient Updates

| coefficient_id | quantity | definition | formula | source_needed | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| COF4527_0_A_odd_force | A_A | vertical action-odd force vector | A_A=delta S_odd/delta z^A|_0 | existing parent action in vertical collar and I_q action | FORMULA_FILLED_VALUE_MISSING | False |
| COF4527_1_CI_over_ellz | C_I/ell_z | collar constant converting epsilon_I action defect to force norm | ||A|| <= (C_I/ell_z) epsilon_I | local collar diameter/norm and action regularity constant | BOUND_FORM_FILLED_VALUE_MISSING | False |
| COF4527_2_Kvert | K_AB^{mu nu} | vertical kinetic/principal coefficient | partial^2 L / partial(nabla_mu z^A) partial(nabla_nu z^B) | parent quadratic action expansion | PRINCIPAL_SYMBOL_ROW_READY_VALUE_MISSING | False |
| COF4527_3_rankZ | rank Z_AB | rank of physical vertical principal symbol after gauge/constraint reduction | rank[K_AB^{mu nu} xi_mu xi_nu] on Q_phys | Kvert plus constraint/gauge reduction | CLASSIFIER_READY_VALUE_MISSING | False |
| COF4527_4_mu_lambda | mu_i, lambda_i | finite-range generalized eigenvalues if rankZ>0 | M v_i=mu_i^2 Z v_i; lambda_i=1/mu_i | Z/M eigenpair with units | FINITE_RANGE_ROW_READY_IF_RANK_POSITIVE | False |
| COF4527_5_alpha_projection | alpha_i(lambda_i) | observable finite-range or algebraic residual projection | rankZ>0: alpha_i=K_i Qbar_iS qbar_iT/(G_N M_S m_T M_i^2); rankZ=0: |delta O|<=K_obs m_min^{-1} sum_abs RHS | source/test charges, calibration, K_obs/K_i, m_min or M_i, bound curve | RUNNER_LINK_READY_VALUES_MISSING | False |

## Claim Gates

| gate_id | gate | status | valid_for_claim |
| --- | --- | --- | --- |
| CG4527_0_action_theorem | action odd force theorem derived | PASS_CONDITIONAL | False |
| CG4527_1_principal_test | vertical principal symbol test derived | PASS_CONDITIONAL | False |
| CG4527_2_parent_zero | existing parent source proves A_A=0 and K=0 | BLOCKED_NOT_FOUND | False |
| CG4527_3_no_closure_auxiliary | no new parentless auxiliary constraint promoted | PASS_FIREWALL | False |
| CG4527_4_local_GR | local GR/Newton/R10/PPN claim | BLOCKED | False |

## Decision

| decision_id | decision | meaning | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC4527_0 | ACTION_ODD_FORCE_AND_VERTICAL_PRINCIPAL_SYMBOL_LAWS_DERIVED_NO_EXISTING_PARENT_ZERO_SOURCE_YET_DUAL_RUNNER_INPUTS_READY | The action-asymmetry and vertical-principal-symbol laws are now explicit. If existing parent action yields A_A=0 and K=0, the rank-zero route strengthens; if not, the same terms feed finite residual or finite-range scoring. No new auxiliary closure is adopted. | 4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md | False |

## Sources

| checkpoint | source_id | role | path | exists | needle | needle_found | line | evidence_snippet | note | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4527 | SRC4527_00_formal4526 | 4526 formal handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\542-PPC4161-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md | True | PPC4161_VERTICAL_INVOLUTION_SOURCE_HUNT_OR_FIRST_SOURCE_NORMALIZED_COEFFICIENT_FILL_4526 | True | 3 | Marker: `PPC4161_VERTICAL_INVOLUTION_SOURCE_HUNT_OR_FIRST_SOURCE_NORMALIZED_COEFFICIENT_FILL_4526` | vertical involution source hunt | False |
| 4527 | SRC4527_01_post4526 | 4526 post handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4526-Y5-R2FR-vertical-involution-source-hunt-or-first-source-normalized-coefficient-fill.md | True | 4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md | True | 70 | | DEC4526_0 | LEAKAGE_PARITY_BRIDGES_TO_PARENT_Z_ONLY_CONDITIONALLY_GR_PARITY_SOURCE_SUBPIECES_ZERO_SCALAR_ACTION_COEFFICIENTS_LIVE | The corpus contains a usable conditional leakage parity lemma and private GR-parity source narrowing, but not a parent-owned full vertical involution. The branch moves forward by converting the surviving scalar/action/wave defects into source-normalized coefficient rows. | 4527-Y5-R2FR-scalar-action-asymmetry-coefficient-or-auxiliary-Z-principal-symbol-hunt.md | False | | declared 4527 target | False |
| 4527 | SRC4527_02_val4526 | 4526 validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4526_VALIDATION.csv | True | VAL4526_OVERALL | True | 9 | VAL4526_OVERALL,PASS,4526 vertical involution source hunt and coefficient fill | previous validation pass | False |
| 4527 | SRC4527_03_bridge4526 | 4526 bridge theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv | True | BRG4526_1_action_evenness | True | 3 | BRG4526_1_action_evenness,"If S_parent, measure, coframe, connection, projector and boundary class commute with I_q, then the first vertical force in the leakage subbundle vanishes.",S[I_q Phi]=S[Phi] => P_L delta_z S|_0=0,DERIVED_CONDITIONAL_NOT_SOURCED,reduces F_1=0 to a concrete action-invariance source hunt,False | action evenness bridge | False |
| 4527 | SRC4527_04_coeff4526 | 4526 coefficient rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_FIRST_SOURCE_NORMALIZED_COEFFICIENT_ROWS.csv | True | COF4526_0_epsilon_I | True | 2 | COF4526_0_epsilon_I,epsilon_I,normalized action-asymmetry defect under the candidate parent involution,epsilon_I := ||S_parent[Phi]-S_parent[I_q Phi]||/(V_loc E_ref),FORMULA_FILLED_SOURCE_VALUE_MISSING,"if nonzero, feeds retained J_A before alpha/PPN/clock/orbit projection",MISSING_NUMERIC_ACTION_DEFECT,False | action asymmetry coefficient | False |
| 4527 | SRC4527_05_hunt4526 | 4526 source hunt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4526_VERTICAL_INVOLUTION_SOURCE_HUNT.csv | True | HUNT4526_4_parent_action_invariance | True | 6 | HUNT4526_4_parent_action_invariance,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4195_PARENT_SIGNATURE_AUDIT.csv,2,4195 audit marks S_parent[Phi]=S_parent[R_L Phi] as missing.,SIG4525_0_vertical_involution,NOT_FOUND,epsilon_I/action-asymmetry row remains live,False | parent action invariance not found | False |
| 4527 | SRC4527_06_theorem4525 | 4525 parent Z theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv | True | QEZ4525_2_rank_zero_from_auxiliary_verticality | True | 4 | QEZ4525_2_rank_zero_from_auxiliary_verticality,no vertical kinetic term gives rank zero,"If z is an auxiliary vertical coordinate and the parent Lagrangian contains no nabla z nabla z term on the physical quotient, the z principal symbol is zero and the local branch is algebraic.",partial L/partial(nabla_mu z^A)=0 => Z_AB=0 in the z principal block,DERIVED_CONDITIONAL,False | rank zero from auxiliary verticality | False |
| 4527 | SRC4527_07_sig4525 | 4525 signature rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4525_PARENT_SIGNATURE_REQUIREMENTS.csv | True | SIG4525_1_auxiliary_vertical_coordinate | True | 3 | SIG4525_1_auxiliary_vertical_coordinate,z has no independent kinetic/principal term on Q_phys,NOT_FOUND_IN_SOURCES,rank(Z_AB)=0 is derived,finite-range branch with lambda_X and alpha_X is required,False | auxiliary vertical coordinate needed | False |
| 4527 | SRC4527_08_classifier4519 | 4519 branch classifier | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4519_FINITE_RANGE_OR_RANK_ZERO_BRANCH_CLASSIFIER.csv | True | FRC4519_1_finite_range | True | 3 | FRC4519_1_finite_range,finite-range Yukawa,rank(Z_AB)>0 on a physical source-coupled quotient and mu_i^2>0,lambda_i=1/mu_i and alpha_i(lambda_i) must be scored against R10 bound curve,do not fabricate lambda from M_AB alone,FINITE_RANGE_CONTRACT_READY_INPUTS_MISSING,False | finite range if rank Z positive | False |
| 4527 | SRC4527_09_residual4519 | 4519 residual vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4519_RANK_ZERO_ALGEBRAIC_RESIDUAL_VECTOR.csv | True | RZR4519_0_normal_form | True | 2 | RZR4519_0_normal_form,algebraic rank-zero equation,M_AB Z^B = J_A + B_A + C_A^CDB + R_A^src/readout/projector,M_AB invertible/first-class and RHS=0,Z_alg = M^{-1}(J+B+CDB+R),False | rank zero residual equation | False |
| 4527 | SRC4527_10_torsion4451 | 4451 no-kinetic auxiliary analogy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4451_DERIVATION_ROWS.csv | True | D4451_0_local_action | True | 2 | D4451_0_local_action,"The safe torsion branch is an auxiliary Cartan branch, not a propagating torsion theory.","Use the local private IR action S = S_EC[e,omega] + c_T int T^A wedge *T_A + S_m[e,psi] and explicitly exclude D T kinetic terms in this branch. Then varying omega cannot produce a wave equation for torsion; it produces an algebraic constraint.",A finite c_T is not automatically a new long-range force.,AUXILIARY_TORSION_BRANCH_WRITTEN,False | no kinetic term gives algebraic branch in torsion analogy | False |
| 4527 | SRC4527_11_torsion_outcome4451 | 4451 failure mode | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4451_OUTCOME_ROWS.csv | True | OUT4451_3_failure_mode | True | 5 | OUT4451_3_failure_mode,parent action with D T kinetic or ker L_T != 0,branch_reopens,"then c_T is a real extra local mode and must be bounded, not hidden",False | kinetic or kernel reopens finite/contact branch | False |
| 4527 | SRC4527_12_aux_caution1192 | 1192 auxiliary closure caution | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1192-Y5-R10-parent-phi-source-or-active-Gamma-bound-first-score-row.md | True | D1192_1_phi_source_not_parent_signed | True | 79 | | D1192_1_phi_source_not_parent_signed | do_not_adopt_auxiliary_phi_constraint | a Lagrange multiplier can force the equation but would be a new closure sector unless stress/Ward/matter readout are derived | look for moment-closure or parent tracefree-sector origin | False | | do not add parentless auxiliary constraint | False |

## Validation

| validation_id | status | detail |
| --- | --- | --- |
| VAL4527_00_sources | PASS | all source paths exist and source needles are found |
| VAL4527_01_action_theorem | PASS | action odd force theorem and no-closure firewall present |
| VAL4527_02_principal_test | PASS | principal symbol and finite-range gate present |
| VAL4527_03_coefficients | PASS | force, Kvert and runner projection rows present |
| VAL4527_04_claims_blocked | PASS | all claim gates remain blocked |
| VAL4527_05_csv_parse | PASS | all generated CSV files parse and have rows |
| VAL4527_06_pycache_absent | PASS | scripts __pycache__ absent after cleanup |
| VAL4527_OVERALL | PASS | 4527 action asymmetry and principal symbol laws |

## Next

`4528-Y5-R2FR-existing-parent-Z-kinetic-block-source-sweep-or-epsilonI-first-bound-row.md`.
