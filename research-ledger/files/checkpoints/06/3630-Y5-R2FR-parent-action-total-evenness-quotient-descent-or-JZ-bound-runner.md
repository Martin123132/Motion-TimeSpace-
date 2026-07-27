# 3630 Y5 R2FR parent-action total evenness, quotient descent, or J_Z bound runner

**Status:** 3630 writes the single parent-action clause that would genuinely kill the coupling: Z must be a vertical generator of q, matter/source/boundary terms must descend to q or be even/quadratic, extra source charges must be orthogonal, and boundary natural sources must vanish. Under those clauses J_Z=0 follows. Current MTS has this as a strong theorem target, not a claim, because the vertical generator, matter/source descent, boundary source, K_metric match, and Z-to-observable map remain unsigned.

**Claim ceiling:** no local-GR, Newton, PPN, R10/R11, WEP, clock, Gdot, EM-source, `K_hat=K_metric`, or `J_Z=0` claim is allowed from 3630.

## Core result

This is the clean parent-action theorem target:

```text
S_parent = S_EH[g] + S_even[Z,g] + S_matter[gbar(q),Psi,theta(q)]
         + S_source[Pi_M(q)J_H(q,Psi)] + S_boundary[B(q),ref] + S_phys_flux[F,Psi,g]
Dq[e_A] = 0,  Z = Z^A e_A
J_A = (1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A |_{Z=0}
```

If the non-response terms depend on the parent only through `q`, or enter only through even/quadratic local amplitudes with zero boundary natural source, then `J_A=0`. With a positive `L_AB`, this derives `Z=0` in the compact local branch. The theorem is good; the present corpus has not yet signed the required parent maps.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_NEXT_TARGET.csv | True | True | 3629 selected the parent-action total-evenness/quotient-descent target. |
| coupling_law_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv | True | True | exact source-coupling law to be killed or bounded. |
| zero_routes_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_JZ_ZERO_ROUTE_AUDIT.csv | True | True | quotient descent, evenness, quadratic activation, charge-current, and boundary zero routes. |
| coefficient_rows_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv | True | True | fallback coefficient rows if J_Z cannot be theorem-zero. |
| quotient_matter_626 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md | True | True | matter quotient descent criterion used in the parent-action theorem. |
| response_doublet_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv | True | True | source-coupling and PPN-lock conditions for the response doublet. |
| double_zero_memory | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv | True | True | quadratic activation condition for memory/domain coupling. |
| domain_parent_clause | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv | True | True | existing domain parent-action clause to be absorbed into the total parent action. |
| charge_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_charge_current_equality_DIRECT_ATTEMPT.csv | True | True | source-normalization/extra-charge orthogonality condition. |
| ppn_envelope_3625 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv | True | True | local-GR envelope that J_Z bound rows must feed if theorem-zero fails. |

## Parent-action clause

| clause_id | object | mathematical_clause | why_needed | current_status |
| --- | --- | --- | --- | --- |
| PAC3630_0_variables | parent variables and quotient | Phi_parent with q:Phi_parent->Q_MTS; local response basis e_A has Dq[e_A]=0; Z^A are coordinates along this vertical response basis | without Dq[e_A]=0, quotient descent cannot imply delta S/delta Z=0 | CLAUSE_WRITTEN_VERTICAL_GENERATOR_NOT_PARENT_MAPPED |
| PAC3630_1_total_action | single admissible parent action | S_parent=S_EH[g]+S_even[Z,g]+S_matter[gbar(q),Psi,theta(q)]+S_source[Pi_M(q)J_H(q,Psi)]+S_boundary[B(q),ref]+S_phys_flux[F,Psi,g] | puts response, matter, measured source, boundary, and physical EM/radiation flux into one action instead of separate closure ledgers | SUFFICIENT_PARENT_ACTION_CLAUSE_WRITTEN_NOT_CURRENT_CORPUS_SIGNED |
| PAC3630_2_even_response | response sector | S_even=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB nabla Z^A nabla Z^B+O(Z^4)] with no odd Z terms | keeps the 3628 F1=0 mechanism and supplies a positive operator L_AB | FORMAL_MECHANISM_FROM_3628_RETAINED |
| PAC3630_3_matter_descent | ordinary matter action | S_matter depends on Phi_parent only through q(Phi_parent), with no representative Weyl/disformal coefficient and no hidden Z-linear matter spurion | kills J_Z^matter by quotient descent instead of tuning a coupling to zero | 626_CRITERION_AVAILABLE_BUT_NOT_PARENT_SIGNED |
| PAC3630_4_source_normalization | measured mass/source current | Pi_M, J_H, G_eff, M_eff, and reference charge are q-data or fixed constants; Pi_M(Q_extra)=0 for non-EH/domain/memory/range/connection charges | prevents measured GM from absorbing a hidden J_Z source and calling it Newton | CHARGE_CURRENT_ORTHOGONALITY_NOT_PARENT_DERIVED |
| PAC3630_5_quadratic_activation | domain/memory activation | any local selector/memory coupling enters through f(Z) or f(chi) with f(0)=f_prime(0)=0, e.g. norm-square/determinant/topological pairing | forbids a linear memory/source term from regenerating Z in the local branch | SUFFICIENT_REQUIREMENT_KNOWN_PARENT_ORIGIN_MISSING |
| PAC3630_6_boundary | boundary and symplectic handoff | boundary variation in the Z direction is zero or fixed-reference: B_A=0 and no linked-surface preferred-frame/source flux remains | bulk J_Z=0 is meaningless if the collar boundary reintroduces alpha3 or source-normalization leakage | BOUNDARY_NATURAL_SOURCE_NOT_SIGNED |
| PAC3630_7_physical_flux_separation | Maxwell/Poynting/radiation stress | physical flux fields F enter S_phys_flux with their own Hilbert stress and current; they are counted as matter/EM stress, not hidden in q_loc closure | keeps the Poynting-vector idea useful without using it to fake a vacuum GR plateau | ACTION_POLICY_WRITTEN_EM_MAPPING_DEFERRED |

## J_Z zero theorem derivation

| step_id | derivation_step | formula | result | status |
| --- | --- | --- | --- | --- |
| THM3630_0_define_source | Define the response source | J_A=(1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A \|_{Z=0} | J_A is the only linear obstruction to Z=0 after the even response action is chosen. | DERIVED_FROM_3629 |
| THM3630_1_even_bulk | Even response bulk has no linear term | delta S_even/delta Z^A \|_{0}=0, delta T_GK/delta Z^A \|_{0}=0 after Gamma_0 subtraction | the 3628 F1=0 result survives inside the total parent action. | CONDITIONAL_PASS_FOR_RESPONSE_SECTOR |
| THM3630_2_matter_descent | Quotient matter descent kills matter source | delta_Z S_matter = (delta Sbar_matter/delta q) Dq[e_A] delta Z^A = 0 because Dq[e_A]=0 | J_A^matter=0 if Z is vertical and S_matter descends to Q_MTS. | VALID_THEOREM_STEP_PARENT_PREMISES_UNSIGNED |
| THM3630_3_source_descent | Source-normalization descent kills measured-mass source | delta_Z S_source = (delta S_source/delta(Pi_M J_H)) delta_Z[Pi_M(q)J_H(q,Psi)] = 0 | mu_extra and J_Z source-normalization terms vanish only if Pi_M and J_H are q-owned and extra charges are orthogonal. | VALID_THEOREM_STEP_CHARGE_CURRENT_PREMISES_UNSIGNED |
| THM3630_4_quadratic_activation | Quadratic memory/domain activation kills selector source | delta_Z[f(Z)L_mem]\|0 = f_prime(0)L_mem delta Z = 0 when f(0)=f_prime(0)=0 | domain/memory coupling does not re-source local Z at first order under the p>=2 activation rule. | VALID_THEOREM_STEP_PARENT_ORIGIN_UNSIGNED |
| THM3630_5_boundary | Boundary natural source must vanish | delta S_boundary\|collar = int_boundary B_A delta Z^A; require B_A=0 or fixed-reference exact term | bulk J_A=0 promotes only if boundary Z-source and linked preferred-frame/source flux are absent. | BOUNDARY_PREMISE_UNSIGNED |
| THM3630_6_conclusion | Conditional J_Z theorem | if THM3630_1..THM3630_5 pass, then J_A=0 and L_AB Z^B+O(Z^2)=0; with positive L_AB and fixed boundary, Z=0 | this would derive the local response plateau instead of assuming it. | CONDITIONAL_THEOREM_PROVED_CURRENT_CORPUS_NOT_SIGNED |

## Parent-signature audit

| audit_id | required_signature | current_status | blocks |
| --- | --- | --- | --- |
| SIG3630_0_q_map | q:Phi_parent->Q_MTS parent-defined | MISSING_PARENT_Q_MAP_IN_THIS_BRANCH | blocks quotient-descent proof |
| SIG3630_1_vertical_generator | Z^A basis equals ker(Dq) vertical directions | MISSING_DQ_VERTICAL_GENERATOR_MAP | blocks delta_Z S_matter=0 |
| SIG3630_2_matter_descent | S_matter=Sbar_matter[q(Phi),Psi,theta] | NOT_SIGNED_FROM_626 | blocks J_A^matter zero and c_g zero |
| SIG3630_3_source_descent | Pi_M,J_H,M_eff,G_eff are q-owned/source-current orthogonal | NOT_PARENT_DERIVED | blocks Newton/source-normalization claim |
| SIG3630_4_quadratic_origin | p>=2 activation follows from symmetry/norm/determinant/topology | REQUIREMENT_DERIVED_ORIGIN_MISSING | blocks selector/memory zero promotion |
| SIG3630_5_boundary | B_A=0 or fixed exact boundary with no local flux | BOUNDARY_NATURAL_SOURCE_OPEN | blocks alpha3/source flux silence |
| SIG3630_6_Kmetric | K_hat equals K_metric for the chosen S_GK | UNSIGNED_FROM_3628 | blocks Gamma/Khat parent ownership |
| SIG3630_7_Z_physical | Z^A equals the physical q_loc/PPN/Newton/source residual vector | MISSING_Z_TO_OBSERVABLE_MAP | blocks using the theorem as local-GR evidence |
| SIG3630_8_verdict | all parent-action signature clauses pass | FAIL_CURRENT_CORPUS_NO_CLAIM | requires 3631 vertical/q/source map or J_Z coefficients |

## Bound requirements if theorem fails

| bound_id | target_row | observable | if_theorem_fails_prediction | minimum_inputs | score_status |
| --- | --- | --- | --- | --- | --- |
| JZB3630_0_gamma | R3_gamma | gamma_minus_1 | K_gamma_JZ * \|\|L^{-1}J_Z\|\|_gamma | MISSING_K_GAMMA_JZ_AND_L_INV_PROFILE; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_1_beta | R4_beta | beta_minus_1 | K_beta_JZ * \|\|L^{-1}J_Z\|\|_beta + delta_beta_source | MISSING_SECOND_ORDER_JZ_PROJECTION; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_2_preferred_frame | R5_R6_R7_R8 | alpha1;alpha2;alpha3;xi | P_PF(L^{-1}J_Z + boundary flux) | MISSING_PREFERRED_FRAME_PROJECTION_AND_BOUNDS; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_3_Newton_source | R10_R11_Newton | delta_Newton_MTS;alpha(lambda);mu_extra | delta_mu_JZ = K_mu_JZ * Pi_M(L^{-1}J_Z) | MISSING_SOURCE_MASS_AND_RANGE_PROFILE; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_4_clock | R2_clock | alpha_clock_redshift | K_clock_JZ * frame_clock_projection(L^{-1}J_Z) | MISSING_CLOCK_FRAME_PROJECTION; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_5_WEP_source | R1_WEP_source_charge | eta_source_AB | Delta_AB ln mu_obs[J_Z] | MISSING_SPECIES_SOURCE_COUPLING; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_6_Gdot | R9_Gdot | Gdot_over_G | partial_t ln mu_obs[J_Z] | MISSING_TIME_DRIFT_SOURCE_PROJECTION; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_7_EM_flux | ENV3625_5_EM_source | w_EM;Phi_EM_boundary | K_EM_JZ * Poynting_or_bound_flux_projection | MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB3630_8_R11_operator | R11_EH_operator_ledger | non_EH_operator_coefficients | c_JZ_operator_vector from retained L^{-1}J_Z operator family | MISSING_EXECUTABLE_OPERATOR_VECTOR; MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3630_0_theorem | A single parent-action clause is now written that is mathematically sufficient for J_Z=0. | CONDITIONAL_THEOREM_PROGRESS | try to parent-map Z as a vertical generator of q and prove matter/source descent |
| DEC3630_1_current_ceiling | The current corpus still cannot claim J_Z=0 because q, vertical generator, matter descent, source descent, boundary source, K_metric, and Z-observable map are unsigned. | NO_CLAIM | do not promote local GR/Newton/PPN; keep bound rows active |
| DEC3630_2_best_next | The highest-leverage next step is not another broad audit: it is the vertical generator and Z-to-observable map. | NEXT_TARGET_SELECTED | 3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3631-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md | scripts/Y5_R2FR_3631_vertical_generator_Z_map_or_JZ_coefficient_runner.py | map Z^A/DCdagger-like local residual coordinates to actual parent quotient vertical generators e_A in ker(Dq), then map Z^A to q_loc/PPN/Newton/source observables; if either map fails, prepare J_Z coefficients for scoring | Dq[e_A]=0 is parent-signed, Z^A is the physical local residual coordinate, and delta_Z S_matter/source can be evaluated; otherwise each observable receives an explicit J_Z coefficient row |
