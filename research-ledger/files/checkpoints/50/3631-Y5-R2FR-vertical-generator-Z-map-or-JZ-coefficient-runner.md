# 3631 Y5 R2FR vertical generator Z map or J_Z coefficient runner

**Status:** 3631 turns the loose DCdagger clue into an exact vertical-generator test: solve Omega_flat(e_X)=DCdagger[X], then require Dq[e_X]=0 and proper/zero boundary charge. It also writes the required observable map R_local=MZ+N Dq_leak+B_boundary. Current MTS does not yet claim verticality or Z-observable lock because q, Omega/P/J, boundary charge, and full-rank residual map are unsigned; Dq leak and J_Z coefficient rows remain staged.

**Claim ceiling:** no verticality, quotient descent, `J_Z=0`, local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, or EM-source claim is allowed from 3631.

## Core result

3631 turns the old `DCdagger` clue into a hard test:

```text
Omega_flat(e_X)_A = DCdagger_A[X]
Dq[e_X] = 0
Q_boundary[e_X] = 0 / exact / proper
```

If those three lines are parent-owned, `e_X` is a genuine vertical generator. Separately, the physical residual map must be:

```text
R_local^i = M^i_A Z^A + N^i_a Dq_leak^a + B^i_boundary + O(Z^2)
```

So `Z=0` only helps local GR if `M` covers the actual observable rows or the uncovered rows are independently zero/bounded.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3630 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3630_NEXT_TARGET.csv | True | True | 3630 selected the vertical-generator and Z-observable map as the next unsigned premise. |
| parent_action_3630 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv | True | True | parent-action clause requiring Z directions to be vertical to q. |
| signature_audit_3630 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3630_PARENT_SIGNATURE_AUDIT.csv | True | True | current vertical-generator blocker. |
| field_chart_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv | True | True | candidate parent field chart containing Q, R_phys, Z, matter, and boundary blocks. |
| dq_tests_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv | True | True | prior Dq tests showing Z verticality is not closed. |
| dq_leaks_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv | True | True | nonclaim Dq leak rows to carry forward if verticality fails. |
| dcdagger_591 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_591_DCDAGGER_FORMULA.csv | True | True | DCdagger/Omega-flat comparison can be sharpened into a vertical-generator reconstruction test. |
| omega_compare_591 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv | True | True | prior verdict that the formula exists but lacks parent Omega/P/J ownership. |
| noether_583 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv | True | True | Noether momentum-map vertical generator contract. |
| lx_candidates_669 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv | True | True | vertical constraint is the best active theorem route if an actual generator can be supplied. |
| local_residual_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv | True | True | R0-R11 observable target rows for the Z-observable map. |
| jz_coeffs_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv | True | True | J_Z coefficient rows to merge with any retained Dq leak. |

## Vertical generator test

| test_id | statement | formula | pass_condition | current_status |
| --- | --- | --- | --- | --- |
| VGT3631_0_chart_split | Use a local parent chart Phi=(Q_vis,R_phys,Z,phi,Psi,theta,B) and treat q(Phi)=Q_vis only if the parent action adopts this split before readout. | Dq[e_A]=D_Q q[e_A^Q]+D_R q[e_A^R]+D_Z q[e_A^Z]+D_B q[e_A^B] | q is an explicit parent map and the chosen e_A gives zero in every visible matter/source/readout/boundary component. | CHART_CANDIDATE_EXISTS_NOT_PARENT_ADOPTED |
| VGT3631_1_naive_Z_generator | The tempting generator e_A=partial/partial Z^A is vertical only in a product chart where q is independent of Z. | Dq[partial_ZA]=partial q/partial Z^A | partial_Z q=0 for coframe, source/readout, theta markers, and boundary/projector data. | NOT_PROVED_RETAIN_DQ_Z_LEAK |
| VGT3631_2_compensated_vertical_generator | If q has Z-dependence, a compensated generator can be written formally but is not automatically a parent symmetry. | e_A=partial_ZA-C_A^I partial_QI, with D_Q q[C_A]=D_ZA q when D_Q q has a right inverse | C_A is parent-defined, local, covariant, not after-solve fitted, and does not move observed matter/source data physically. | FORMAL_REPAIR_WRITTEN_NOT_ADMISSIBLE_WITHOUT_PARENT_OWNER |
| VGT3631_3_constraint_first_escape | The cleanest route is to make Z a first-class constrained/vertical variable before matter coupling, not to hide its visible effect afterwards. | S_parent=S_obs[q]+int Lambda^A C_A; e_epsilon^i={Phi^i,G[epsilon]}; Dq[e_epsilon]=0; Q_boundary[epsilon]=0/proper | constraint algebra closes, Noether charge is differentiable, and boundary charge is zero/proper on compact local collars. | BEST_ROUTE_SELECTED_NOT_CLOSED |
| VGT3631_4_verdict | Current corpus has a computable vertical-generator test but not a parent-signed generator. | Z vertical iff Dq[e_A]=0 and e_A comes from parent Noether/constraint/Omega data before readout. | VGT3631_0 through VGT3631_3 pass together. | VERTICAL_GENERATOR_NOT_CLAIMED |

## DCdagger to vertical generator

| map_id | statement | formula | meaning | current_status |
| --- | --- | --- | --- | --- |
| DVG3631_0_reconstruction_equation | DCdagger becomes a vertical-generator test only after it is matched to the field-space symplectic form. | Omega_flat(e_X)_A = DCdagger_A[X] | if Omega is invertible/modded by gauge, e_X=Omega^{-1}DCdagger[X] is the candidate generator. | FORMULA_PROGRESS_PARENT_OMEGA_MISSING |
| DVG3631_1_verticality_gate | The reconstructed generator must be invisible to the quotient. | Dq[Omega^{-1}DCdagger[X]]=0 | this is the exact bridge from the DCdagger machinery to quotient descent. | TEST_WRITTEN_NOT_RUNNABLE_WITHOUT_Q_AND_OMEGA |
| DVG3631_2_boundary_charge_gate | A vertical generator still fails local GR if its Hamiltonian boundary charge is improper or physical. | G[epsilon]=int Sigma epsilon^A C_A + int_boundary Q_epsilon; require Q_epsilon=0/exact/proper and delta G differentiable | prevents a fake vertical proof that leaves alpha3/source-normalization flux on the collar. | BOUNDARY_CHARGE_NOT_DERIVED |
| DVG3631_3_parent_owner_gate | P, J, theta, Omega, and q must come from one parent action, not separate fits. | delta L=E_i delta Phi^i+d theta; C_X=-nabla P+J; DCdagger=Omega_flat(e_X) | same-parent ownership is the criterion that keeps this a field theory rather than closure bookkeeping. | SAME_PARENT_OWNER_MISSING |
| DVG3631_4_verdict | DCdagger has been mapped to the actual vertical-generator contract, but the contract is unsigned. | parent L -> theta/Omega/P/J/q -> e_X=Omega^{-1}DCdagger -> Dq[e_X]=0 -> Q_boundary proper | this is the right target for a derivation; if it fails, Dq and J_Z coefficients must be scored. | DCDAGGER_TO_VERTICAL_MAP_CONDITIONAL_NO_CLAIM |

## Z observable map

| map_id | observable | map_formula | condition_for_use | rank_gate | current_status |
| --- | --- | --- | --- | --- | --- |
| ZOM3631_0_q_loc | q_loc^nu | Z_q^nu = Pi_q Z | q_loc^nu=P_loc nabla_mu T_GK^{mu nu} | the Z basis must span this residual component with no hidden null leakage | MISSING_Z_TO_QLOC_PROJECTION |
| ZOM3631_1_gamma_beta | gamma_minus_1;beta_minus_1 | Z_PPN_scalar = Pi_gamma_beta Z | weak-field metric solution maps Z stress/source to gamma,beta | the Z basis must span this residual component with no hidden null leakage | MISSING_WEAK_FIELD_Z_METRIC_SOLUTION |
| ZOM3631_2_preferred_frame | alpha1;alpha2;alpha3;xi | Z_PF^I = Pi_PF^I Z + boundary_flux^I | preferred-frame/location projections must include collar and source-current terms | the Z basis must span this residual component with no hidden null leakage | MISSING_PREFERRED_FRAME_Z_PROJECTION |
| ZOM3631_3_Newton_source | delta_Newton_MTS;mu_extra;alpha(lambda) | Z_N = Pi_M L^{-1}J_Z plus Dq_Z source leak | Newton/R10 depends on source-normalization and finite-range profile, not only bulk q_loc | the Z basis must span this residual component with no hidden null leakage | MISSING_SOURCE_MASS_AND_RANGE_MAP |
| ZOM3631_4_clock_WEP_Gdot | alpha_clock;eta_source_AB;Gdot/G | Z_clock/source/time = Pi_clock/source/time Z | clock/WEP/Gdot need same observed coframe and species/source charge descent | the Z basis must span this residual component with no hidden null leakage | MISSING_CLOCK_WEP_TIME_MAP |
| ZOM3631_5_EM_flux | w_EM;Phi_EM_boundary | Z_EM = physical F-sector stress or coupling leakage, not hidden q_loc | Poynting/Maxwell flux must be counted as physical stress/current unless absent or boundary-silent | the Z basis must span this residual component with no hidden null leakage | MISSING_EM_FLUX_SEPARATION_MAP |
| ZOM3631_6_R11 | non_EH_operator_coefficients | Z_R11 = operator-family projection of retained Z/Dq/J_Z terms | R11 needs executable operator coefficients for any retained non-EH/source-normalization branch | the Z basis must span this residual component with no hidden null leakage | MISSING_EXECUTABLE_R11_Z_VECTOR |
| ZOM3631_7_verdict | full local residual vector | R_local^i = M^i_A Z^A + N^i_a Dq_leak^a + B^i_boundary + O(Z^2) | M has full row coverage for R0-R11 or unspanned components have independent theorem-zero/bounds | FULL_RANK_OR_BOUND_EVERY_MISSING_COMPONENT | Z_OBSERVABLE_MAP_NOT_CLAIMED_BOUND_ROWS_REQUIRED |

## Dq leak and J_Z coefficient rows

| row_id | type | quantity | formula_or_template | affected_channel | minimum_inputs | score_status |
| --- | --- | --- | --- | --- | --- | --- |
| DQL3631_0_Dq_Z | Dq_leak | Dq_Z_norm | MISSING_NUMERIC_OR_THEOREM_ZERO | Z normal-form quotient leak | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_1_Dq_phi | Dq_leak | Dq_phi_norm | MISSING_NUMERIC_OR_THEOREM_ZERO | phi improvement quotient leak | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_2_Dq_RAB_Jq | Dq_leak | Dq_RAB_or_Jq_norm | MISSING_NUMERIC_OR_THEOREM_ZERO | R_AB/J_q cell-visible leak | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_3_DObs_e | Dq_leak | DObs_e_Dq_leak | MISSING_NUMERIC_OR_THEOREM_ZERO | observed geometry channel | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_4_Dsource_readout | Dq_leak | Dsource_readout_Dq_leak | MISSING_NUMERIC_OR_THEOREM_ZERO | Newton/source/readout channel | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_5_Dtheta_marker | Dq_leak | Dtheta_marker_Dq_leak | MISSING_NUMERIC_OR_THEOREM_ZERO | constants/material marker channel | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_6_boundary_projector | Dq_leak | Dboundary_projector_Dq_leak | MISSING_NUMERIC_OR_THEOREM_ZERO | boundary and projector channel | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| DQL3631_7_Scg_envelope | Dq_leak | S_cg_norm | 0.5\|\|T\|\|_source*C_qm + S_direct + S_source_norm_extra + S_boundary | absolute no-cancellation envelope | numeric norm or theorem-zero; units; source path; no-cancellation guard | not_scoreable |
| JZC3631_0_gamma | J_Z_coefficient | gamma_minus_1 | K_gamma_JZ * \|\|L^{-1}J_Z\|\|_gamma | R3_gamma | MISSING_K_GAMMA_JZ_AND_L_INV_PROFILE; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_1_beta | J_Z_coefficient | beta_minus_1 | K_beta_JZ * \|\|L^{-1}J_Z\|\|_beta + delta_beta_source | R4_beta | MISSING_SECOND_ORDER_JZ_PROJECTION; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_2_preferred_frame | J_Z_coefficient | alpha1;alpha2;alpha3;xi | P_PF(L^{-1}J_Z + boundary flux) | R5_R6_R7_R8 | MISSING_PREFERRED_FRAME_PROJECTION_AND_BOUNDS; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_3_Newton_source | J_Z_coefficient | delta_Newton_MTS;alpha(lambda);mu_extra | delta_mu_JZ = K_mu_JZ * Pi_M(L^{-1}J_Z) | R10_R11_Newton | MISSING_SOURCE_MASS_AND_RANGE_PROFILE; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_4_clock | J_Z_coefficient | alpha_clock_redshift | K_clock_JZ * frame_clock_projection(L^{-1}J_Z) | R2_clock | MISSING_CLOCK_FRAME_PROJECTION; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_5_WEP_source | J_Z_coefficient | eta_source_AB | Delta_AB ln mu_obs[J_Z] | R1_WEP_source_charge | MISSING_SPECIES_SOURCE_COUPLING; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_6_Gdot | J_Z_coefficient | Gdot_over_G | partial_t ln mu_obs[J_Z] | R9_Gdot | MISSING_TIME_DRIFT_SOURCE_PROJECTION; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_7_EM_flux | J_Z_coefficient | w_EM;Phi_EM_boundary | K_EM_JZ * Poynting_or_bound_flux_projection | ENV3625_5_EM_source | MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION; L inverse/profile; observable projection; bound source | not_scoreable |
| JZC3631_8_R11_operator | J_Z_coefficient | non_EH_operator_coefficients | c_JZ_operator_vector from retained L^{-1}J_Z operator family | R11_EH_operator_ledger | MISSING_EXECUTABLE_OPERATOR_VECTOR; L inverse/profile; observable projection; bound source | not_scoreable |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3631_0_DCd_to_vertical | DCdagger is no longer just boundary algebra: the exact generator test is Omega_flat(e_X)=DCdagger[X] followed by Dq[e_X]=0. | REAL_DERIVATION_TARGET_WRITTEN | source or construct parent Omega, q, P, J and boundary charge to run the test |
| DEC3631_1_Z_map | Z cannot be treated as physical merely by naming it; the required map is R_local=MZ+N Dq_leak+B_boundary. | OBSERVABLE_MAP_CONTRACT_WRITTEN | derive M and prove full-rank coverage or bound each unspanned component |
| DEC3631_2_current_claim | Verticality and Z-observable lock are not claimed; Dq leak and J_Z coefficient rows remain live. | NO_CLAIM | carry both leak families into the next owner-or-bound runner |
| DEC3631_3_next_target | Next target should try the constraint-first/Omega owner route, because it is the only path that can make Z genuinely vertical without after-solve compensation. | NEXT_TARGET_SELECTED | 3632-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3632-Y5-R2FR-Omega-owner-constraint-generator-or-DqJZ-bound-pack.md | scripts/Y5_R2FR_3632_Omega_owner_constraint_generator_or_DqJZ_bound_pack.py | attempt to construct or source the same-parent Omega/theta/P/J/q owner needed to solve Omega_flat(e_X)=DCdagger and verify Dq[e_X]=0; if not, package Dq leak and J_Z rows into executable coefficient inputs | parent Omega, q, P, J, and boundary charge are signed from one action and produce a proper vertical e_X, or every failed piece is converted into source-ready Dq/J_Z coefficient rows |
