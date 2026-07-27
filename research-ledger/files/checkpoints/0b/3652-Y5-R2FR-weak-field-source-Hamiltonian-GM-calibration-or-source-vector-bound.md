# 3652 - Weak-field source Hamiltonian, GM calibration, or source-vector bound

**Status:** 3652 derives the fitted-GM/source-Hamiltonian calibration law, the Poisson source condition, and the PPN/orbital residual vector, while keeping all rows nonclaim.

**Claim ceiling:** no weak-field source Hamiltonian, Newtonian, PPN, orbital, R10, WEP, local-GR, or calibrated-source pass is claimed.

## Main result

The weak-field gate is now explicit. Orbital/Newtonian data measure `mu_fit=(GM)_fit`; this equals `G_obs M_S^eff` only after the source Hamiltonian, active/inertial source identity, metric readout, and boundary/domain terms are owned. The derived calibration law is `delta ln mu_obs = delta ln G_obs + delta ln M_S^eff + q_metric + q_readout + q_boundary + q_source`.

This means matching orbits is not by itself a local-GR proof: fitted `GM` can absorb source calibration. Current MTS does not yet sign the weak-field source Hamiltonian and PPN zero vector, so `q_GM_source_abs` and `Delta_PPN_MTS` remain nonclaim residual rows.

## Theorem rows
- `WFH3652_0_parent_source_Hamiltonian`: `EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED` — If the parent action signs this, fitted GM is not a separate source-coupling knob.
- `WFH3652_1_GM_calibration_law`: `GM_DEGENERACY_LAW_DERIVED` — Newtonian recovery must prove or bound the source-calibration vector, not only match orbits.
- `WFH3652_2_Poisson_source_law`: `POISSON_SOURCE_CONDITION_DERIVED` — The Newtonian limit requires rho_active=rho_inertial and residual source terms theorem-zero or bounded.
- `WFH3652_3_fifth_force_projection`: `YUKAWA_SOURCE_PROJECTION_DERIVED` — R10 cannot be scored until K_X, Z_X, lambda_X, Q_S^X, and Q_T^X are sourced or theorem-zero.
- `WFH3652_4_PPN_vector_law`: `PPN_RESIDUAL_VECTOR_DERIVED` — A GR/PPN limit needs a vector zero theorem or bounded residual vector across all components.
- `WFH3652_5_orbital_guard`: `ORBITAL_GM_DEGENERACY_GUARD_DERIVED` — The orbital branch must use the same q_source vector as WEP/R10/PPN.
- `WFH3652_6_GR_Newton_zero_conditions`: `LOCAL_GR_CONTRACT_DERIVED` — This is the local-GR gate: not impossible, but it must be signed as one branch rather than imported from GR notation.
- `WFH3652_7_verdict`: `FAIL_CURRENT_CLAIM_WEAK_FIELD_SOURCE_HAMILTONIAN_UNSIGNED` — Current MTS has a derived weak-field source-calibration law but not a local GR/Newton pass.

## GM/source calibration rows
- `GMC3652_0_mu_fit`: `mu_fit` — ORBITAL_SOURCE_DATA_REQUIRED
- `GMC3652_1_delta_mu`: `delta_ln_mu_obs` — COMPONENT_VALUES_REQUIRED
- `GMC3652_2_Qsource`: `Q_source_X` — SOURCE_BODY_CHARGE_REQUIRED
- `GMC3652_3_Qtest`: `Q_test_X` — TEST_BODY_CHARGE_REQUIRED
- `GMC3652_4_alpha_ST`: `alpha_ST` — R10_COMPONENTS_REQUIRED
- `GMC3652_5_rho_source`: `rho_active_minus_inertial` — ACTIVE_INERTIAL_IDENTITY_REQUIRED
- `GMC3652_6_PPN_vector`: `Delta_PPN_MTS` — PPN_COMPONENT_MAP_REQUIRED
- `GMC3652_7_orbital_vector`: `Delta_orbital_MTS` — ORBITAL_VECTOR_REQUIRED
- `GMC3652_8_total_guard`: `q_GM_source_abs` — SCHEMA_READY_VALUES_MISSING

## PPN/orbital residual vector
- `PVR3652_0_gamma`: `gamma_minus_1` — METRIC_AND_SOURCE_MAP_REQUIRED
- `PVR3652_1_beta`: `beta_minus_1` — METRIC_AND_SOURCE_MAP_REQUIRED
- `PVR3652_2_alpha1`: `alpha1` — PREFERRED_FRAME_SOURCE_MAP_REQUIRED
- `PVR3652_3_alpha2`: `alpha2` — PREFERRED_FRAME_SOURCE_MAP_REQUIRED
- `PVR3652_4_alpha3`: `alpha3` — SOURCE_FLUX_SILENCE_REQUIRED
- `PVR3652_5_xi`: `xi` — PREFERRED_LOCATION_SOURCE_MAP_REQUIRED
- `PVR3652_6_Gdot`: `Gdot_over_G` — TIME_DRIFT_SOURCE_MAP_REQUIRED
- `PVR3652_7_R10`: `alpha_lambda_R10` — R10_CURVE_AND_MTS_COMPONENTS_REQUIRED
- `PVR3652_8_total`: `PPN_orbital_source_abs` — SCHEMA_READY_VALUES_MISSING

## Projection rows
- `WFP3652_0_Newton`: `Newtonian_Poisson` — SOURCE_IDENTITY_UNSIGNED
- `WFP3652_1_PPN`: `local_GR_PPN` — PPN_VECTOR_NOT_SCORE_READY
- `WFP3652_2_orbital`: `orbital_dynamics` — ORBITAL_VECTOR_NOT_SCORE_READY
- `WFP3652_3_WEP`: `WEP_crosscheck` — COMPOSITION_VALUES_MISSING
- `WFP3652_4_R10`: `R10_crosscheck` — R10_COMPONENTS_MISSING
- `WFP3652_5_clock`: `clock_readout_crosscheck` — READOUT_SOURCE_BRIDGE_MISSING
- `WFP3652_6_total`: `all_local_arenas` — NO_CANCELLATION_POLICY_ACTIVE

## Decisions
- `DEC3652_0_derivation`: `GM_CALIBRATION_LAW_DERIVED` — Weak-field source calibration is derived: fitted GM equals G_obs times effective source mass plus metric/readout/boundary/source residuals.
- `DEC3652_1_verdict`: `PARENT_WEAK_FIELD_SOURCE_HAMILTONIAN_UNSIGNED` — Current MTS does not parent-sign weak-field source Hamiltonian, active/inertial source identity, PPN metric vector, readout, and boundary silence together.
- `DEC3652_2_rows`: `SOURCE_CALIBRATION_VECTOR_CREATED_NOT_SCORE_READY` — q_GM_source_abs, Delta_PPN_MTS, Delta_orbital_MTS, alpha_ST, and source-density residual rows are staged as nonclaim bounds.
- `DEC3652_3_next`: `NEWTON_PPN_ZERO_VECTOR_GATE_NEXT` — Next target is the Newton-Poisson/PPN zero-vector gate: derive the metric weak-field coefficients and close or retain every local-GR residual component.

## Next checkpoint

`3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md` via `scripts/Y5_R2FR_3653_Newton_Poisson_PPN_zero_vector_gate_or_local_GR_residual_fit.py`.

## Sources
- `next_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md` exists=True needle_found=True
- `sens_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv` exists=True needle_found=True
- `proj_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_PROJECTION_ROWS.csv` exists=True needle_found=True
- `theorem_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `bounds_R1_WEP`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R3_gamma`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R4_beta`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R9_Gdot`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `bounds_R10`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `matrix_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv` exists=True needle_found=True
