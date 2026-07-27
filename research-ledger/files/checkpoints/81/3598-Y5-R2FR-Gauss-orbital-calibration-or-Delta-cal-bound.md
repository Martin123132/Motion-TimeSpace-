# 3598 - Gauss/orbital calibration or Delta_cal bound

## Verdict
3598 derives the exact conditional bridge from dressed Hilbert source to measured Newtonian `GM`: source charge must pass through the same-frame weak-field Poisson equation, Gauss surface flux, and slow inverse-square orbital readout.

This is the key discipline point: `M_source^dress` is not automatically what planets feel.  It becomes `mu_obs=G_eff M_H` only when `Delta_cal=0` and the derivative-hair channels are silent by theorem or bounded with real rows.

## Calibration Theorem Gate
- `GOC3598_0_target`: TARGET_IMPORTED - Connect M_source^dress[W;tau]=ell_M(Pi_M J_H_total) to Poisson/Gauss/orbital measured GM, or retain Delta_cal, partial_r ln mu_obs and d ln G_eff/dt bounds.
- `GOC3598_1_source_monopole_input`: SOURCE_INPUT_IMPORTED - mu_parent := G_eff M_H[Pi_M J_H_total] with M_H already dressed by matter, EM/Poynting, binding and permitted boundary terms.
- `GOC3598_2_weak_field_Poisson_bridge`: CONDITIONAL_POISSON_DERIVATION - If the same observed frame is used and the local exterior operator is EH at leading order, g_00=-1-2 Phi/c^2 gives nabla^2 Phi=4 pi G_eff rho_H + R_Poisson.
- `GOC3598_3_Gauss_surface_bridge`: CONDITIONAL_GAUSS_DERIVATION - For any enclosing surface S, mu_Gauss(S) := (1/4 pi) integral_S grad Phi dot dS = G_eff M_H(enclosed) + Delta_Gauss.
- `GOC3598_4_orbital_readout_bridge`: CONDITIONAL_ORBITAL_DERIVATION - For a slow nearly circular observed-frame test body, mu_obs(r) := r^2 |a_r| = v^2 r = mu_Gauss + Delta_orbit when finite-range, direct-force, frame, multipole and radial-hair corrections are absent.
- `GOC3598_5_exact_Delta_cal_identity`: EXACT_RESIDUAL_DECOMPOSITION - Delta_cal := mu_obs - G_eff M_H[Pi_M J_H_total] = Delta_Poisson + Delta_Gauss + Delta_orbit + mu_extra + Delta_frame + Delta_G + Delta_flux + Delta_range + Delta_PPN_source.
- `GOC3598_6_derivative_hair_identity`: EXACT_DERIVATIVE_IDENTITY - For X in {t,r,A,lambda,frame,domain}, D_X ln mu_obs = D_X ln G_eff + D_X ln M_H + D_X ln(1+epsilon_cal), where epsilon_cal=Delta_cal/(G_eff M_H).
- `GOC3598_7_conditional_calibration_theorem`: CONDITIONAL_ZERO_THEOREM_DERIVED - If the source charge is parent-owned, the weak-field operator is EH with standard coefficient, Gauss residuals vanish, slow bodies read the same Phi as inverse-square acceleration, mu_extra=0, G_eff is constant/universal, derivative hair is silent, and first-order normalization is PPN-stable, then Delta_cal=0 and mu_obs=G_eff M_H[Pi_M J_H_total].
- `GOC3598_8_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - Current MTS has the calibration chain but not the proof: Delta_cal, partial_r ln mu_obs, d ln G_eff/dt, d ln M_eff/dt, mu_extra, frame split, range dependence, and PPN source stability remain active nonclaim rows.

## Delta_cal Residuals
- `DCR3598_0_total` / `Delta_cal_total`: ACTIVE_NONCLAIM - mu_obs - G_eff M_H[Pi_M J_H_total]
- `DCR3598_1_source_charge` / `Delta_charge`: INHERITED_OPEN - B_xi/G_eff - M_H[Pi_M J_H_total]
- `DCR3598_2_Poisson` / `Delta_Poisson`: OPEN_OPERATOR_COEFFICIENT_REQUIRED - nabla^2 Phi - 4 pi G_eff rho_H
- `DCR3598_3_Gauss` / `Delta_Gauss`: OPEN_GAUSS_SURFACE_REQUIRED - mu_Gauss(S) - G_eff M_H(enclosed)
- `DCR3598_4_orbit` / `Delta_orbit`: OPEN_ORBITAL_READOUT_REQUIRED - mu_obs(r)-mu_Gauss(S_r)
- `DCR3598_5_mu_extra` / `mu_extra`: OPEN_EXTRA_MASS_REQUIRED - mu_extra_boundary_bulk_domain + mu_extra_range + mu_extra_projector + mu_extra_EM + mu_extra_nonEH
- `DCR3598_6_constant_Geff` / `Delta_G`: OPEN_COUPLING_SUPERSELECTION_REQUIRED - D_X ln G_eff or G_eff-G0
- `DCR3598_7_flux` / `Delta_flux`: OPEN_FLUX_CLOSURE_REQUIRED - integral_annulus d(Pi_M J_H_total)
- `DCR3598_8_radial_hair` / `partial_r_ln_mu_obs`: OPEN_RADIAL_NO_HAIR_REQUIRED - partial_r ln mu_obs
- `DCR3598_9_time_hair` / `dln_Geff_dt_plus_dln_Meff_dt`: OPEN_TIME_DRIFT_REQUIRED - d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_cal)/dt
- `DCR3598_10_frame_species_range` / `Delta_frame_species_range`: OPEN_UNIVERSALITY_REQUIRED - delta_frame_source + eta_source_AB + alpha(lambda)
- `DCR3598_11_PPN` / `Delta_PPN_source`: DOWNSTREAM_PPN_OPEN - (gamma-1,beta-1,alpha1,alpha2,alpha3,xi)_source

## Bound Rows
- `GOB3598_0_epsilon_Delta_cal` / `epsilon_Delta_cal`: BOUND_REQUIRED_CRITICAL - abs(mu_obs-G_eff M_H[Pi_M J_H_total])/abs(G_eff M_H)
- `GOB3598_1_epsilon_Poisson` / `epsilon_Poisson`: BOUND_REQUIRED - norm(nabla^2 Phi-4 pi G_eff rho_H)/norm(4 pi G_eff rho_H)
- `GOB3598_2_epsilon_Gauss` / `epsilon_Gauss`: BOUND_REQUIRED - abs(mu_Gauss-G_eff M_H)/abs(G_eff M_H)
- `GOB3598_3_epsilon_orbit` / `epsilon_orbit`: BOUND_REQUIRED - abs(mu_obs-mu_Gauss)/abs(mu_Gauss)
- `GOB3598_4_epsilon_mu_extra` / `epsilon_mu_extra`: BOUND_REQUIRED_CRITICAL - abs(mu_extra)/(abs(G_eff M_H))
- `GOB3598_5_dln_Geff_dt` / `dln_Geff_dt`: BOUND_REQUIRED - d ln G_eff/dt
- `GOB3598_6_dln_Meff_dt` / `dln_Meff_dt`: BOUND_REQUIRED - d ln M_H[Pi_M J_H_total]/dt
- `GOB3598_7_partial_r_ln_mu_obs` / `partial_r_ln_mu_obs`: BOUND_REQUIRED_CRITICAL - partial_r ln mu_obs
- `GOB3598_8_eta_source_AB` / `eta_source_AB`: BOUND_REQUIRED - source/test species derivative of mu_obs
- `GOB3598_9_alpha_lambda` / `alpha(lambda)`: BOUND_REQUIRED - finite-range/source-normalization Yukawa amplitude curve
- `GOB3598_10_delta_frame_source` / `delta_frame_source`: BOUND_REQUIRED - frame/source pullback mismatch in mu_obs
- `GOB3598_11_delta_beta_source` / `delta_beta_source`: BOUND_REQUIRED_DOWNSTREAM - second-order source-normalized PPN beta/gamma residue
- `GOB3598_12_epsilon_calibration_total` / `epsilon_calibration_total`: TOTAL_BOUND_BRANCH_ACTIVE - sum of epsilon_Delta_cal, epsilon_Poisson, epsilon_Gauss, epsilon_orbit, epsilon_mu_extra, derivative hair, frame/species/range and PPN source residuals

## Promotion Gates
- `PROM3598_0_calibration_theorem`: PASS_CONDITIONAL_THEOREM - Delta_cal is zero only if the full source-to-Poisson-to-Gauss-to-orbit chain closes
- `PROM3598_1_measured_GM_claim`: FAIL_CURRENT_CLAIM - Delta_cal, mu_extra, derivative hair, constant G_eff, inverse-square readout and PPN stability remain unsigned
- `PROM3598_2_derivative_hair_visible`: PASS_GUARD - time/radial hair rows are explicit and cannot be hidden inside measured GM
- `PROM3598_3_no_fitted_cancellation`: PASS_GUARD - cancellation counts only if parent identity forces it
- `PROM3598_4_bound_pack`: PASS_NONCLAIM - rows are source-ready but not numeric/score-ready
- `PROM3598_5_no_Newton_or_GR_claim`: PASS_GUARD - this is a conditional route, not a local-GR pass

## Status
- `GAUSS_ORBITAL_CALIBRATION_THEOREM_CONDITIONAL_DELTA_CAL_BOUND_ACTIVE`: 3598 derives the exact bridge required for Newtonian mechanics: a dressed Hilbert source becomes observed orbital GM only through same-frame Poisson, Gauss surface flux, inverse-square slow-orbit readout, zero extra monopoles, constant universal G_eff, derivative-hair silence, and PPN source stability.
- Decision: retain the conditional theorem, keep Delta_cal and derivative-hair rows as nonclaim bounds, and attack the constant-G_eff / radial-time-hair gate next
- Still missing: EH weak-field coefficient, Gauss residual zero, inverse-square orbit readout, zero mu_extra, G_eff superselection, Pi_M flux conservation, partial_r ln mu_obs silence, dln_Geff_dt/dln_Meff_dt silence, source universality, range independence, frame pullback, and second-order PPN source stability

## Validation
- `VAL3598_0_sources_exist`: PASS (all required 3598 source paths exist)
- `VAL3598_1_needles_found`: PASS (all selected 3598 source anchors found)
- `VAL3598_2_outputs_exist`: PASS (all pre-validation 3598 csv output files written)
- `VAL3598_3_csv_parse`: PASS (source_register:20; calibration_theorem:9; delta_cal_residuals:12; bound_rows:13; promotion_gates:6; status:1; next_target:1; canonical_status:1)
- `VAL3598_4_calibration_theorem_present`: PASS (Gauss/orbital conditional calibration theorem row present)
- `VAL3598_5_Delta_cal_explicit`: PASS (Delta_cal residual and bound rows are explicit)
- `VAL3598_6_derivative_hair_explicit`: PASS (time/radial derivative hair rows present)
- `VAL3598_7_claim_blocked`: PASS (current measured-GM calibration claim is blocked)
- `VAL3598_8_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3598_9_no_Newton_GR_claim`: PASS (Newton/PPN/local-GR claim guard is active)
- `VAL3598_10_no_fitted_cancellation_guard`: PASS (no fitted-cancellation guard present)
- `VAL3598_11_next_target_selected`: PASS (3599 constant G_eff/radial-time hair target selected)
- `VAL3598_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3598_13_formalization_workbench_untouched`: PASS (no 3598 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3598_0` -> `3599-Y5-R2FR-constant-Geff-radial-time-hair-zero-or-bound.md`
- Objective: try to prove the constant universal G_eff/kappa superselection and radial/time derivative silence for mu_obs, or fill dln_Geff_dt, dln_Meff_dt, partial_t_epsilon_mu and partial_r_ln_mu_obs bound rows
