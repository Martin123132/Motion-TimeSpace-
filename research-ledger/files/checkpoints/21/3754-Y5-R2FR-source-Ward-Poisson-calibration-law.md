# 3754 — Source Ward / Poisson Calibration Law

## Status

`WARD_BALANCE_POISSON_COEFFICIENT_DERIVED_CONSTANT_COUPLING_OPEN`.

This checkpoint attacks the coupling issue directly. The projector can define the mass channel, but Newtonian mechanics needs both a source Ward/no-flux law and a same-frame EH/Poisson calibration.

## Ward / Flux Law
- `WL3754_0_same_frame_source` `definition_bridge`: J_H[tau] is the Hilbert/coframe source current from the same observed matter action and same observed time generator tau.
- `WL3754_1_noether_identity` `conditional_ward_law`: For a diffeomorphism-invariant parent matter action on matter shell, nabla_mu T_H^{mu nu}=q_exchange^nu, with q_exchange^nu=0 only when all non-Hilbert/exchange owners are absent or mapped.
- `WL3754_2_observed_time_current` `conditional_mass_current_law`: If tau or xi is an observed stationary/Killing/Hamiltonian generator, j_M^mu=T_H^{mu nu}xi_nu obeys nabla_mu j_M^mu = xi_nu q_exchange^nu plus generator-normalization terms.
- `WL3754_3_projected_current` `projector_step_derived`: With the 3753 topological projector, J_M=Pi_M J_H has dJ_M=Pi_M dJ_H because dPi_M=0 in the parent topological block.
- `WL3754_4_charge_rate` `stokes_balance_law`: For a worldtube slab C between two linking surfaces, Delta ell_M(J_H)=int_C dJ_M = -Phi_side + int_C Pi_M q_exchange.
- `WL3754_5_conservation_condition` `exact_conditional_closure`: d ell_M(J_H)=0 follows if Phi_side=0 and Pi_M q_exchange=0.
- `WL3754_6_flux_bound` `fallback_bound`: |d ln M_eff/dt| <= (|Phi_side|+int|Pi_M q_exchange|)/(abs(ell_M(J_H))*Delta t)

## Poisson Calibration
- `PC3754_0_parent_field_equation` `conditional_field_equation`: G_mn + Lambda g_mn = kappa_eff T_H_mn + DeltaE_res_mn
- `PC3754_1_weak_field_00` `standard_weak_field_bridge`: In the same observed frame and nonrelativistic limit, G_00 ~= 2 nabla^2 Phi/c^2 and T_00 ~= rho_H c^2.
- `PC3754_2_poisson_coefficient` `derived_coefficient_law`: nabla^2 Phi = (kappa_eff c^4/2) rho_H + Delta_Poisson = 4 pi G_eff rho_H + Delta_Poisson.
- `PC3754_3_topological_mass_density` `source_charge_definition`: M_eff := k_M ell_M(J_H), rho_eff := k_M q_M where q_M is the local density of the projected charge current.
- `PC3754_4_gauss_monopole` `conditional_gauss_law`: For a closed source with zero residual flux, surface_integral grad Phi dot dS = 4 pi G_eff M_eff.
- `PC3754_5_orbital_readout` `derived_readout_identity`: a_r=-partial_r Phi=-G_eff M_eff/r^2 + a_res, so mu_obs=G_eff M_eff + mu_extra.
- `PC3754_6_G_value_policy` `anti_overclaim_policy`: The numerical value of G_eff is not derived unless kappa_eff or k_M is predicted by the parent action; otherwise only universality and derivative silence can be claimed.

## Coupling Ladder
- `LAD3754_0_projector` `PASSED_CONDITIONAL`: Pi_M topological projector — closed by 3753 signature conditionally
- `LAD3754_1_ward` `CONDITIONAL_NOT_PARENT_SIGNED`: d ell_M(J_H)=0 — derived iff no side flux and no projected exchange
- `LAD3754_2_mass` `DEFINITION_READY_KM_OPEN`: M_eff=k_M ell_M(J_H) — definition requires parent source units k_M
- `LAD3754_3_EH` `CONDITIONAL_NOT_PARENT_SIGNED`: EH left-hand dominance — needed before Poisson coefficient counts
- `LAD3754_4_poisson` `DERIVED_CONDITIONAL`: nabla^2 Phi=4*pi*G_eff rho_eff — coefficient law derived if EH/source residuals vanish
- `LAD3754_5_G` `GLOBAL_COUPLING_OPEN`: G_eff=kappa_eff c^4/(8*pi) — universality/constancy not yet parent-derived
- `LAD3754_6_orbit` `OPEN`: mu_obs=G_eff M_eff — requires zero mu_extra and no radial/range hair
- `LAD3754_7_ppn` `OPEN`: gamma,beta,etc. — requires second-order residual vector

## Residuals If A Rung Fails
- `RES3754_0_mass_flux` `dln_Meff_dt`: (Phi_side + Pi_M q_exchange volume)/M_eff -> Gdot/orbital/source-normalization
- `RES3754_1_poisson_residual` `Delta_Poisson`: DeltaE_res_00 plus non-Hilbert/source residual terms in weak-field limit -> Newton/PPN gamma beta
- `RES3754_2_mu_extra` `mu_extra/(G_eff M_eff)`: boundary + bulk + domain + memory + range + connection monopole corrections -> Kepler, R10, PPN, source normalization
- `RES3754_3_Gdot` `dln_Geff_dt`: dln kappa_eff_dt plus any source-unit drift -> LLR/Gdot
- `RES3754_4_species` `eta_source_AB`: composition dependence of k_M, kappa_eff, or ell_M source weighting -> WEP/source charge
- `RES3754_5_range_radial` `partial_r ln mu_obs and alpha(lambda)`: radial/range dependence of coupling or extra source channel -> inverse-square/R10
- `RES3754_6_frame` `Delta_frame_source`: source frame differs from orbital/clock frame -> WEP/clocks/preferred-frame
- `RES3754_7_beta_source` `delta_beta_source`: second-order source-normalization correction -> PPN beta

## Claim Gates
- `CG3754_0_sources` pass=`True`: all 3754 source paths exist — path hygiene
- `CG3754_1_ward_balance` pass=`True`: mass-charge Stokes/Ward balance derived — d ell_M law now has explicit flux/exchange terms
- `CG3754_2_flux_zero` pass=`False`: mass flux closure d ell_M=0 fully proved — requires no side flux and no projected exchange theorem
- `CG3754_3_poisson_coeff` pass=`True`: EH-to-Poisson coefficient bridge derived — G_eff := kappa_eff c^4/(8*pi)
- `CG3754_4_constant_G` pass=`False`: constant universal G_eff parent-derived — global coupling superselection still open
- `CG3754_5_mu_obs` pass=`False`: mu_obs=G_eff M_eff with mu_extra=0 proved — mu_extra/range/radial rows remain open
- `CG3754_6_residual_vector` pass=`True`: fallback residual vector emitted — keeps failed coupling premises testable
- `CG3754_7_local_newton` pass=`False`: Newton inverse-square source calibration claim allowed — not until CG3754_2,4,5 pass
- `CG3754_8_local_gr` pass=`False`: local GR/PPN claim allowed — second-order PPN and full residual vector still open

## Decisions
- `DEC3754_0_real_advance` `WARD_BALANCE_AND_POISSON_COEFFICIENT_DERIVED_CONDITIONALLY`: 3754 turns coupling into equations: charge drift equals side flux plus projected exchange, and the EH weak-field coefficient gives G_eff=kappa_eff c^4/(8*pi).
- `DEC3754_1_no_magic_G` `NUMERICAL_G_NOT_DERIVED`: Without a parent absolute kappa/k_M normalization theorem, MTS can aim to derive universality and silence of derivative/source hair, not the measured number of G.
- `DEC3754_2_key_blocker` `GLOBAL_COUPLING_SUPERSELECTION_AND_NO_FLUX`: The next hard pieces are constant universal kappa_eff and no projected source/exchange flux.
- `DEC3754_3_testing_path` `FAILED_COUPLING_PREMISES_MAP_TO_GDOT_WEP_R10_ORBITAL`: If any coupling premise fails, it becomes a residual row rather than a hidden calibration.

## Next Target
- `3755-Y5-R2FR-global-kappa-superselection-or-coupling-residual-vector.md`: prove kappa_eff/G_eff is a global source-blind, range-blind, time/radius/frame independent coupling sector, or emit executable Gdot/WEP/R10/radial/source residual rows

## Source Register
- `SRC3754_0_3753_next` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3753_NEXT_TARGET.csv`
- `SRC3754_1_3753_checks` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3753_PROJECTOR_THEOREM_CHECKS.csv`
- `SRC3754_2_3753_coupling` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3753_REDUCED_HOP_AND_SOURCE_COUPLING.csv`
- `SRC3754_3_flux_contract` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PiM_flux_closure_Ward_topological_CONTRACT.csv`
- `SRC3754_4_source_ward` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_current_Ward_universality_CONTRACT.csv`
- `SRC3754_5_ward_owner` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Ward_source_owner_identity_CONTRACT.csv`
- `SRC3754_6_poisson_gauss` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv`
- `SRC3754_7_hilbert_monopole` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Hilbert_monopole_calibration_CONTRACT.csv`
- `SRC3754_8_global_coupling` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_global_coupling_superselection_CONTRACT.csv`
- `SRC3754_9_meff_flux` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv`
- `SRC3754_10_residual_map` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv`
- `SRC3754_11_poisson_gates` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3530_POISSON_PPN_GATES.csv`
- `SRC3754_12_newton_bounds` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3530_NEWTON_PPN_BOUND_ROWS.csv`
- `SRC3754_13_completion_gates` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv`
- `SRC3754_14_constant_gm` exists=`True`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv`
