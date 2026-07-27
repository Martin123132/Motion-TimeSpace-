# 3651 - Matter representation source sensitivity or composition matrix row

**Status:** 3651 derives the material/source sensitivity law and EM Coulomb binding row, then stages a nonclaim composition matrix for WEP/R10/PPN/orbital tests.

**Claim ceiling:** no material-sensitivity zero theorem, WEP, R10, PPN, orbital, local-GR/Newton, or source-calibration pass is claimed.

## Main result

The useful forward step is that the composition problem now has a formula. The source charge vector is `Q_A^X = partial ln M_A^eff / partial Xhat`; its leading EM channel is `B_A^EM = partial ln M_A / partial ln alpha_EM ~= E_C/(M_A c^2)` with `E_C=a_C Z(Z-1)A^(-1/3)` before isotope/mixture sourcing.

If matter labels, current/source measure, and binding data are fixed representation or quotient-owned data, this matrix can theorem-zero. Current MTS does not yet sign that parent clause, so the matrix is staged as nonclaim evidence plumbing rather than a WEP/R10 pass.

## Theorem rows
- `MSS3651_0_representation_descent`: `EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED` — b_material_marker=0, beta_charge_lattice=0, and explicit source-label leakage vanish under this parent-action signature.
- `MSS3651_1_mass_sensitivity_law`: `SOURCE_CHARGE_VECTOR_DERIVED` — Composition dependence is not a vague missing item: it is the coefficient vector Q_A^X.
- `MSS3651_2_EM_binding_law`: `EM_BINDING_FORMULA_DERIVED_SYMBOLICALLY` — This gives the concrete composition row needed for WEP/R10 once material isotopes or mixture weights are sourced.
- `MSS3651_3_WEP_R10_projection`: `COMMON_SOURCE_TEST_MATRIX_DERIVED` — The composition matrix ties the coupling branch directly to empirical tests without assuming local silence.
- `MSS3651_4_PPN_orbital_projection`: `SOURCE_CALIBRATION_GUARD_DERIVED` — The same composition/source matrix must feed PPN and orbital residual vectors before claiming a GR/Newton limit.
- `MSS3651_5_material_countermodel`: `COUNTERMODEL_LIVE` — Matter/source sensitivities cannot be declared zero from WEP notation or from a fitted GR background alone.
- `MSS3651_6_verdict`: `FAIL_CURRENT_CLAIM_MATTER_SENSITIVITY_UNSIGNED` — Current MTS has a derived matrix law but not a parent-signed zero theorem; composition rows remain nonclaim.

## Sensitivity rows
- `MSR3651_0_QA_vector`: `Q_A_X` — MATERIAL_COMPONENT_VALUES_REQUIRED
- `MSR3651_1_BAEM`: `B_A_EM` — SOURCE_CONSTANT_AND_ISOTOPE_TABLE_REQUIRED
- `MSR3651_2_Coulomb_energy`: `E_C` — A_Z_aC_SOURCE_REQUIRED
- `MSR3651_3_DeltaQ`: `DeltaQ_AB_X` — TEST_BODY_COMPOSITION_REQUIRED
- `MSR3651_4_Qsource`: `Q_source_X` — SOURCE_BODY_COMPOSITION_REQUIRED
- `MSR3651_5_tau_WEP`: `tau_WEP` — LOCAL_DOMAIN_MAP_REQUIRED
- `MSR3651_6_tau_R10`: `tau_R10` — LOCAL_DOMAIN_MAP_AND_LAMBDA_REQUIRED
- `MSR3651_7_tau_PPN`: `tau_PPN` — WEAK_FIELD_SOURCE_MAP_REQUIRED
- `MSR3651_8_tau_orbital`: `tau_orbital` — ORBITAL_SOURCE_MAP_REQUIRED
- `MSR3651_9_total_guard`: `q_matter_source_abs` — SCHEMA_READY_VALUES_MISSING

## Composition schema rows
- `CMS3651_0_material_schema`: `material_A` — MATERIAL_TABLE_SCHEMA_READY_VALUES_MISSING
- `CMS3651_1_test_A`: `test_body_A` — TEST_A_COMPOSITION_REQUIRED
- `CMS3651_2_test_B`: `test_body_B` — TEST_B_COMPOSITION_REQUIRED
- `CMS3651_3_source_body`: `source_body_S` — SOURCE_BODY_COMPOSITION_REQUIRED
- `CMS3651_4_pair_matrix`: `DeltaQ_AB_X` — PAIR_MATRIX_READY_VALUES_MISSING
- `CMS3651_5_yukawa_matrix`: `Q_source_X_Q_test_X` — YUKAWA_PRODUCT_READY_VALUES_MISSING
- `CMS3651_6_no_cancellation`: `composition_no_cancellation_guard` — ACTIVE_NONCLAIM_GUARD

## Projection rows
- `MPR3651_0_WEP`: `MICROSCOPE_WEP` — COMPOSITION_VALUES_MISSING
- `MPR3651_1_R10`: `R10_short_range` — MTS_AND_BOUND_INPUTS_MISSING
- `MPR3651_2_PPN`: `PPN_source_calibration` — SOURCE_HAMILTONIAN_MAP_MISSING
- `MPR3651_3_orbital`: `orbital_source_calibration` — ORBITAL_DATA_MAP_MISSING
- `MPR3651_4_clock`: `clock_crosscheck` — CROSS_CHANNEL_BRIDGE_NOT_SCORE_READY
- `MPR3651_5_EM`: `EM_stress_material` — EM_SOURCE_OWNER_UNSIGNED
- `MPR3651_6_total`: `all_local_arenas` — NO_CANCELLATION_POLICY_ACTIVE

## Decisions
- `DEC3651_0_derivation`: `MATERIAL_SENSITIVITY_LAW_DERIVED` — The material/source sensitivity law is now derived as Q_A^X=partial ln M_A^eff/partial Xhat, with EM Coulomb binding B_A^EM ~= E_C/(M_A c^2).
- `DEC3651_1_verdict`: `PARENT_MATTER_SENSITIVITY_UNSIGNED` — Current MTS does not parent-sign representation/source measure/material/binding closure, so Q_A^X is not zero-claimed.
- `DEC3651_2_matrix`: `COMPOSITION_MATRIX_SCHEMA_CREATED_NOT_SCORE_READY` — Composition matrix schema is staged with units, formulas, source-path hooks, tau links, and no-cancellation guards, but numeric material values are absent.
- `DEC3651_3_next`: `WEAK_FIELD_SOURCE_HAMILTONIAN_NEXT` — Next target is weak-field source Hamiltonian/GM calibration: derive how Q_A^X enters Newtonian source mass and PPN residuals or keep a bounded source-calibration vector.

## Next checkpoint

`3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md` via `scripts/Y5_R2FR_3652_weak_field_source_Hamiltonian_GM_calibration_or_source_vector_bound.py`.

## Sources
- `next_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md` exists=True needle_found=True
- `beta_rows_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_BETA_SOURCE_ALPHA_ROWS.csv` exists=True needle_found=True
- `projection_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_TEST_PROJECTION_ROWS.csv` exists=True needle_found=True
- `matrix_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv` exists=True needle_found=True
- `vertex_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv` exists=True needle_found=True
- `em_lock_989`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
- `doc_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md` exists=True needle_found=True
