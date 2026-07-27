# 3691 - Vertical q-map source-current orthogonality or J_A coefficient acquisition

**Status:** VERTICAL_SOURCE_ORTHOGONALITY_CONDITIONAL_NOT_SIGNED_JA_COEFFICIENT_ACQUISITION_ROWS_INSTALLED

This checkpoint tests the exact route for killing the matter/source part of the canonical coupling `J_A`. The algebra is clean: if the canonical `Z` directions are truly vertical and matter/source currents descend through the quotient, the corresponding source terms vanish. The current corpus does not yet sign those parent premises, so coefficient acquisition rows remain live.

## Main result

`Dq[e_A]=0` is the verticality test.

`delta_Z S_matter=(delta Sbar_matter/delta q)Dq[e_A]delta Z^A`, so `J_A^matter=0` only after verticality plus matter q-descent.

`delta_Z S_source=0` only if `Pi_M,J_H,M_eff,G_eff` are q-owned or orthogonal to vertical charges.

`eps_JH_Z_abs <= C_matter*Dq_Z_norm + eps_theta_marker + eps_direct_Z + eps_source_weight + eps_matter_boundary`.

## Vertical gates
- `VQ3691_0_parent_q`: MISSING_PARENT_Q_MAP - parent quotient map -> R_qmap
- `VQ3691_1_generator`: MISSING_DQ_VERTICAL_GENERATOR_MAP - vertical generator -> R_Zvertical
- `VQ3691_2_naive_Z`: NOT_PROVED_RETAIN_DQ_Z_LEAK - naive partial_Z generator -> Dq_Z_norm
- `VQ3691_3_compensated`: FORMAL_REPAIR_NOT_PARENT_ADMISSIBLE - compensated generator -> Dq_comp_residual
- `VQ3691_4_DCd`: TEST_WRITTEN_NOT_RUNNABLE_WITHOUT_Q_OMEGA_BOUNDARY - DCdagger generator test -> R_DCd_vertical
- `VQ3691_5_constraint_first`: BEST_ROUTE_SELECTED_NOT_CLOSED - constraint-first route -> R_constraint_owner
- `VQ3691_6_verdict`: VERTICAL_Q_MAP_NOT_CLAIMED - verticality for canonical Z -> R_qmap+R_Zvertical+Dq_Z_norm

## Source orthogonality
- `SO3691_0_matter`: CONDITIONAL_ZERO_NOT_PARENT_SIGNED - ordinary Hilbert matter leg -> eps_JH_Z_abs
- `SO3691_1_source_current`: CONDITIONAL_ZERO_SOURCE_LOCK_UNSIGNED - source current leg -> eps_source_current
- `SO3691_2_EM_charge`: CONDITIONAL_ZERO_COUNTERMODEL_LIVE - EM/source normalization leg -> beta_source_alpha
- `SO3691_3_projector_PiM`: PIM_DERIVATIVE_COMMUTATOR_OPEN - Pi_M projector derivative -> epsilon_DPiM+I_commutator
- `SO3691_4_readout_marker`: MARKER_SOURCE_SLOT_UNSIGNED - theta/material/source marker -> eps_theta_marker+Delta_w_abs
- `SO3691_5_boundary`: BOUNDARY_SOURCE_OPEN - boundary/source-worldtube leg -> eps_B_abs
- `SO3691_6_verdict`: MATTER_SOURCE_ORTHOGONALITY_NOT_CLAIMED - matter/source orthogonality for J_A -> R_Jmatter+R_Jsource

## Coefficient acquisition
- `JAC3691_0_Dq`: MISSING_NUMERIC_OR_THEOREM_ZERO - `Dq_Z_norm` in all observed arenas -> q map, Z basis, q/Z norms, source/readout descent
- `JAC3691_1_JH`: BOUND_FORM_READY_VALUES_MISSING - `eps_JH_Z_abs` in Newton;PPN;R10;WEP;clock;orbital;EM -> C_matter, Dq_Z value, theta/no-marker, source-weight, matter-boundary rows
- `JAC3691_2_master`: MASTER_BOUND_FORM_READY_VALUES_MISSING - `Delta_A source-current residual` in Newton;PPN;R10;WEP;clock;orbital;EM -> M_AB, L_A, source components, DqZ map, units
- `JAC3691_3_Newton`: MISSING_SOURCE_MASS_AND_RANGE_PROFILE - `K_mu_JA` in Newton;R10;R11 -> source mass/range profile, Pi_M, L inverse, worldtube source
- `JAC3691_4_PPN`: MISSING_PPN_PROJECTIONS - `K_gamma_JA,K_beta_JA,P_PF` in PPN gamma,beta,alpha_i,xi -> PPN projection, L inverse, boundary/source profile
- `JAC3691_5_clock_WEP_Gdot`: MISSING_CLOCK_WEP_TIME_PROJECTION - `K_clock_JA,Delta_AB ln mu_obs,partial_t ln mu_obs` in clocks;WEP;ephemeris -> frame/species/source/time projection
- `JAC3691_6_EM`: MISSING_EM_SOURCE_NORMALIZATION - `beta_source_alpha,K_EM_JA` in EM;WEP;clock;orbital -> charge/source representation, material sensitivities, EM flux normalization
- `JAC3691_7_R11`: MISSING_EXECUTABLE_OPERATOR_VECTOR - `c_JA_operator_vector` in R11/non-EH operators -> executable operator coefficients and domain norms

## Decisions
- `DEC3691_0_vertical`: VERTICAL_TEST_EXACT_NOT_SIGNED - Dq[e_A]=0 is the correct test, but q/Omega/boundary parent ownership is missing -> do not claim J_A matter/source zero
- `DEC3691_1_source`: SOURCE_ORTHOGONALITY_CONDITIONAL - matter/source/EM current zero laws are exact only under quotient/source-current descent -> retain eps_JH_Z_abs, beta_source_alpha and PiM derivative residuals
- `DEC3691_2_coefficients`: COEFFICIENT_ACQUISITION_ROWS_INSTALLED - if the zero theorem fails, required J_A coefficients are now named by arena -> source K_mu_JA, K_gamma_JA, beta_source_alpha and L inverse profiles
- `DEC3691_3_next`: NEXT_BEST_TARGET - constraint-first Omega owner is the only route that can truly sign verticality -> run 3692 Omega-owner constraint generator or Dq/J_A coefficient runner
- `DEC3691_4_private`: PRIVATE_NONCLAIM - no local-GR/Newton/GitHub/public claim -> continue private derivation

## Claim gates
- `CG3691_0_vertical`: BLOCKED_Q_OMEGA_BOUNDARY_OWNER - claim Dq[e_A]=0 because q, Omega/DCdagger, and boundary charge are not parent-signed
- `CG3691_1_JA_matter_source`: BLOCKED_DESCENT_ORTHOGONALITY - claim J_A^matter=J_A^source=0 because matter/source/PiM/JH descent is conditional only
- `CG3691_2_JA_total`: BLOCKED_BOUNDARY_SELECTOR_FLUX_ZMAP - claim J_A=0 because boundary, selector, flux and Z observable map remain open
- `CG3691_3_score`: BLOCKED_COEFFICIENTS - score PPN/R10/WEP/clock/EM because arena coefficients and L inverse/source profiles are missing
- `CG3691_4_public`: BLOCKED_PRIVATE - public/GitHub promotion because private checkpoint only

## Next target
`3692-Y5-R2FR-Omega-owner-constraint-generator-or-DqJA-coefficient-runner.md` via `scripts/Y5_R2FR_3692_Omega_owner_constraint_generator_or_DqJA_coefficient_runner.py`.

## Sources
- `handoff_3690`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3690_NEXT_TARGET.csv` exists=True needle_found=True
- `ja_gates_3690`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3690_JA_ZERO_GATE_ROWS.csv` exists=True needle_found=True
- `ja_decomp_3690`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3690_JA_DECOMPOSITION_ROWS.csv` exists=True needle_found=True
- `arena_3690`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3690_JA_ARENA_TEMPLATE_ROWS.csv` exists=True needle_found=True
- `vertical_3631`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_VERTICAL_GENERATOR_TEST.csv` exists=True needle_found=True
- `dcdagger_3631`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_DCDAGGER_VERTICAL_GENERATOR_MAP.csv` exists=True needle_found=True
- `dq_leak_3631`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_DQ_Z_LEAK_AND_JZ_COEFFICIENTS.csv` exists=True needle_found=True
- `zmap_3631`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3631_Z_OBSERVABLE_MAP.csv` exists=True needle_found=True
- `source_2642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `bounds_2642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv` exists=True needle_found=True
- `leak_2643`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv` exists=True needle_found=True
- `em_current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `pim_lock_2579`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_EH_DESCENT_COUPLING_PIM_2579_COUPLING_PIM_LOCK_GATE.csv` exists=True needle_found=True
