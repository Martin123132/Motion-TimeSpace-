# 4117 - parent-action total evenness quotient descent or J_Z bound runner

## Verdict
4117 imports the `3630` parent-action theorem into the active `411x` spine. The theorem is strong and clean: if `Z` is vertical to the quotient and all non-response terms descend to `q` or enter even/quadratic with zero boundary natural source, then `J_Z=0` follows.

This is still not a claim. The current corpus has the theorem target, not the signed parent maps.

## Strongest Current Result
- `PARENT_ACTION_JZ_ZERO_THEOREM_IMPORTED_VERTICAL_Z_MAP_NEXT`
- 4117 imports the sufficient parent-action theorem for J_Z=0 into the active spine: Z must be vertical to q, matter/source/boundary terms must descend to q or enter even/quadratic, extra source charges must be orthogonal, and boundary natural sources must vanish.
- The coupling zero is now a single parent-action signature target rather than disconnected closure wishes. It is mathematically enough, but not parent-signed.

## Parent-Action Clause
| clause_id | object | mathematical_clause | current_status |
| --- | --- | --- | --- |
| PAC4117_0_variables | parent variables and quotient | q:Phi_parent->Q_MTS; local response basis e_A has Dq[e_A]=0; Z^A coordinates vertical response basis | CLAUSE_WRITTEN_VERTICAL_GENERATOR_NOT_PARENT_MAPPED |
| PAC4117_1_total_action | single admissible parent action | S_parent=S_EH+S_even+S_matter[gbar(q),Psi,theta(q)]+S_source[Pi_M(q)J_H(q,Psi)]+S_boundary[B(q),ref]+S_phys_flux | SUFFICIENT_PARENT_ACTION_CLAUSE_WRITTEN_NOT_CURRENT_CORPUS_SIGNED |
| PAC4117_2_even_response | response sector | S_even=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB nabla Z^A nabla Z^B+O(Z^4)] | FORMAL_MECHANISM_FROM_3628_RETAINED |
| PAC4117_3_matter_descent | ordinary matter action | S_matter depends on Phi_parent only through q(Phi_parent), no representative Weyl/disformal or hidden Z-linear spurion | 626_CRITERION_AVAILABLE_BUT_NOT_PARENT_SIGNED |
| PAC4117_4_source_normalization | measured mass/source current | Pi_M,J_H,G_eff,M_eff and reference charge are q-data/fixed constants; Pi_M(Q_extra)=0 | CHARGE_CURRENT_ORTHOGONALITY_NOT_PARENT_DERIVED |
| PAC4117_5_quadratic_activation | domain/memory activation | f(0)=f_prime(0)=0, e.g. norm-square/determinant/topological pairing | SUFFICIENT_REQUIREMENT_KNOWN_PARENT_ORIGIN_MISSING |
| PAC4117_6_boundary | boundary and symplectic handoff | boundary variation in Z direction is zero/fixed-reference: B_A=0 and no linked-surface preferred-frame/source flux | BOUNDARY_NATURAL_SOURCE_NOT_SIGNED |
| PAC4117_7_physical_flux | Maxwell/Poynting/radiation stress | physical flux fields enter S_phys_flux with own Hilbert stress/current; count as matter/EM stress, not hidden q_loc closure | ACTION_POLICY_WRITTEN_EM_MAPPING_DEFERRED |

## J_Z Zero Theorem
| step_id | formula | result | status |
| --- | --- | --- | --- |
| THM4117_0_define_source | J_A=(1/sqrt(-g)) delta(S_matter+S_source+S_boundary)/delta Z^A |_{Z=0} | J_A is the only linear obstruction to Z=0 after even response action | DERIVED_FROM_3629 |
| THM4117_1_even_bulk | delta S_even/delta Z^A|0=0 and delta T_GK/delta Z^A|0=0 | 3628 F1=0 survives inside total parent action | CONDITIONAL_PASS_FOR_RESPONSE_SECTOR |
| THM4117_2_matter_descent | delta_Z S_matter=(delta Sbar/delta q)Dq[e_A]delta Z^A=0 | J_A^matter=0 if Z is vertical and S_matter descends to Q_MTS | VALID_THEOREM_STEP_PARENT_PREMISES_UNSIGNED |
| THM4117_3_source_descent | delta_Z S_source=0 when Pi_M and J_H are q-owned and extra charges orthogonal | measured mass/source-normalization terms vanish before GM fitting | VALID_THEOREM_STEP_CHARGE_CURRENT_PREMISES_UNSIGNED |
| THM4117_4_quadratic_activation | delta_Z[f(Z)L_mem]|0=f_prime(0)L_mem delta Z=0 | domain/memory coupling does not re-source local Z at first order | VALID_THEOREM_STEP_PARENT_ORIGIN_UNSIGNED |
| THM4117_5_boundary | delta S_boundary|collar=int_boundary B_A delta Z^A; require B_A=0/fixed exact | bulk J_A=0 promotes only if boundary Z-source/flux absent | BOUNDARY_PREMISE_UNSIGNED |
| THM4117_6_conclusion | if THM4117_1..5 pass, then J_A=0 and L_AB Z^B+O(Z^2)=0; positive L_AB plus fixed boundary gives Z=0 | would derive local response plateau rather than assuming it | CONDITIONAL_THEOREM_PROVED_CURRENT_CORPUS_NOT_SIGNED |

## Parent-Signature Audit
| audit_id | required_signature | current_status | blocks |
| --- | --- | --- | --- |
| SIG4117_0_q_map | q:Phi_parent->Q_MTS parent-defined | MISSING_PARENT_Q_MAP_IN_THIS_BRANCH | blocks quotient-descent proof |
| SIG4117_1_vertical_generator | Z^A basis equals ker(Dq) vertical directions | MISSING_DQ_VERTICAL_GENERATOR_MAP | blocks delta_Z S_matter=0 |
| SIG4117_2_matter_descent | S_matter=Sbar_matter[q(Phi),Psi,theta] | NOT_SIGNED_FROM_626 | blocks J_A^matter zero and c_g zero |
| SIG4117_3_source_descent | Pi_M,J_H,M_eff,G_eff q-owned/source-current orthogonal | NOT_PARENT_DERIVED | blocks Newton/source-normalization claim |
| SIG4117_4_quadratic_origin | p>=2 activation follows from symmetry/norm/determinant/topology | REQUIREMENT_DERIVED_ORIGIN_MISSING | blocks selector/memory zero promotion |
| SIG4117_5_boundary | B_A=0 or fixed exact boundary with no local flux | BOUNDARY_NATURAL_SOURCE_OPEN | blocks alpha3/source flux silence |
| SIG4117_6_Kmetric | K_hat equals K_metric for chosen S_GK | UNSIGNED_FROM_3628 | blocks Gamma/Khat parent ownership |
| SIG4117_7_Z_physical | Z^A equals physical q_loc/PPN/Newton/source residual vector | MISSING_Z_TO_OBSERVABLE_MAP | blocks using theorem as local-GR evidence |
| SIG4117_8_verdict | all parent-action signature clauses pass | FAIL_CURRENT_CORPUS_NO_CLAIM | requires 4118 vertical/q/source map or J_Z coefficients |

## Bound Requirements If Theorem Fails
| bound_id | target_row | observable | minimum_inputs | score_status |
| --- | --- | --- | --- | --- |
| JZB4117_0_gamma | R3_gamma | gamma_minus_1 | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_1_beta | R4_beta | beta_minus_1 | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_2_preferred_frame | R5_R6_R7_R8 | alpha1;alpha2;alpha3;xi | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_3_Newton_source | R10_R11_Newton | delta_Newton_MTS;alpha(lambda);mu_extra | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_4_clock | R2_clock | alpha_clock_redshift | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_5_WEP_source | R1_WEP_source_charge | eta_source_AB | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_6_Gdot | R9_Gdot | Gdot_over_G | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_7_EM_flux | ENV3625_5_EM_source | w_EM;Phi_EM_boundary | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |
| JZB4117_8_R11_operator | R11_EH_operator_ledger | non_EH_operator_coefficients | MISSING_L_OPERATOR_NORM; MISSING_OBSERVABLE_PROJECTION; MISSING_BOUND_SOURCE_PATH | not_scoreable |

## Decisions
| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC4117_0_theorem | A single parent-action clause is now in the active spine and is mathematically sufficient for J_Z=0. | CONDITIONAL_THEOREM_PROGRESS | try to parent-map Z as vertical generator of q and prove matter/source descent |
| DEC4117_1_current_ceiling | Current corpus still cannot claim J_Z=0 because q, vertical generator, matter descent, source descent, boundary source, K_metric and Z-observable map are unsigned. | NO_CLAIM | do not promote local GR/Newton/PPN; keep bound rows active |
| DEC4117_2_best_next | Highest-leverage next step is vertical generator and Z-to-observable map, not another broad audit. | NEXT_TARGET_SELECTED | 4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md |

## Next Target
| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 4118-Y5-R2FR-vertical-generator-Z-map-or-JZ-coefficient-runner.md | scripts/Y5_R2FR_4118_vertical_generator_Z_map_or_JZ_coefficient_runner.py | map Z^A/DCdagger-like local residual coordinates to actual parent quotient vertical generators e_A in ker(Dq), then map Z^A to q_loc/PPN/Newton/source observables; if either map fails, prepare J_Z coefficients for scoring | Dq[e_A]=0 is parent-signed, Z^A is the physical local residual coordinate, and delta_Z S_matter/source can be evaluated; otherwise each observable receives an explicit J_Z coefficient row |
