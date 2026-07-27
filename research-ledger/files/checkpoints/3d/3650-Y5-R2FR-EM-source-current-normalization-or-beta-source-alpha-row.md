# 3650 - EM source-current normalization or beta_source_alpha row

**Status:** 3650 derives the conditional source-current normalization theorem, shows Ward conservation is insufficient by itself, and creates explicit beta_source_alpha/source-test coupling rows.

**Claim ceiling:** no beta_source_alpha=0, source-current owner, local-GR/Newton, WEP, R10, PPN, clock, orbital, or EM stress pass is claimed.

## Main result

The source-current throat is sharper than the earlier ledger: gauge invariance gives `nabla_mu J_Q^mu=0`, but it does **not** by itself fix source/test charge normalization. The exact zero theorem needs the same compact `T_Q` owner in `S_EM` and `D_Q`, fixed representation labels `rho_A(T_Q)`, a quotient-owned current/source measure, and no material/source marker `chi_A(X_N)`.

Under those clauses, `Q_A^eff=int_Sigma dSigma_mu J_A^mu` has `beta_source_alpha,A = Lie_vX ln Q_A^eff = 0`. Current MTS does not yet sign those clauses, so `beta_source_alpha` and source/test sensitivity rows remain live.

## Theorem rows
- `SCT3650_0_parent_current_action`: `EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED` — If T_Q, rho_A(T_Q), theta_A, particle-number measure, and source Hamiltonian descend through q or fixed representation data, EM source normalization is not an extra fitted coupling.
- `SCT3650_1_Ward_identity`: `WARD_CONSERVATION_NOT_ENOUGH` — Charge conservation is necessary but not sufficient for beta_source_alpha=0.
- `SCT3650_2_beta_zero_law`: `BETA_ZERO_LAW_DERIVED_CONDITIONALLY` — beta_source_alpha,A=0 is derivable only from a parent representation/source-measure theorem, not from notation.
- `SCT3650_3_force_projection`: `OBSERVABLE_ENVELOPE_DERIVED` — This connects the coupling throat to WEP, R10, clocks, PPN/source calibration, and EM stress without assuming cancellations.
- `SCT3650_4_current_rescaling_countermodel`: `COUNTERMODEL_LIVE` — Source/test EM charge can float independently of the Maxwell kinetic coefficient unless the parent matter functor forbids it.
- `SCT3650_5_verdict`: `FAIL_CURRENT_CLAIM_SOURCE_CURRENT_OWNER_UNSIGNED` — The derivation path is precise but unsigned; beta_source_alpha and source/test sensitivity rows remain live.

## Source-current audit
- `SCA3650_0_TQ_same_owner`: `beta_source_alpha;b_alpha` — PARTIAL_UNSIGNED
- `SCA3650_1_rep_lattice`: `beta_charge_lattice` — UNSIGNED
- `SCA3650_2_current_measure`: `b_J_source` — UNSIGNED
- `SCA3650_3_material_marker`: `b_material_marker` — UNSIGNED
- `SCA3650_4_EM_binding_sensitivity`: `B_A_EM;DeltaQ_EM_AB` — MISSING_SENSITIVITY_MATRIX
- `SCA3650_5_Ward_boundary`: `b_boundary_current` — UNSIGNED
- `SCA3650_6_total`: `q_source_EM_abs` — SOURCE_CURRENT_OWNER_UNSIGNED

## beta/source coefficient rows
- `BSA3650_0_beta_zero`: `beta_source_alpha_zero_candidate` — MISSING_PARENT_SOURCE_CURRENT_THEOREM
- `BSA3650_1_beta_source_alpha`: `beta_source_alpha` — MISSING_SOURCE_CURRENT_NORMALIZATION
- `BSA3650_2_beta_charge_lattice`: `beta_charge_lattice` — MISSING_CHARGE_LATTICE_OWNER
- `BSA3650_3_bJ_source`: `b_J_source` — MISSING_CURRENT_MEASURE_DESCENT
- `BSA3650_4_bmaterial`: `b_material_marker` — MISSING_MATERIAL_MARKER_DESCENT
- `BSA3650_5_BAEM`: `B_A_EM` — MISSING_EM_BINDING_SENSITIVITY_MATRIX
- `BSA3650_6_boundary`: `b_boundary_current` — MISSING_BOUNDARY_CURRENT_CLOSURE
- `BSA3650_7_total_guard`: `q_source_EM_abs` — SCHEMA_READY_VALUES_MISSING

## Observable projections
- `SP3650_0_Ward`: `charge_current_Ward` — CONSERVATION_READY_NORMALIZATION_UNSIGNED
- `SP3650_1_WEP`: `WEP_source_charge` — COMPOSITION_MATRIX_MISSING
- `SP3650_2_R10`: `R10_short_range_source_charge` — MTS_AND_BOUND_INPUTS_NOT_CLAIM_READY
- `SP3650_3_clock`: `clock_alpha_crosscheck` — CROSS_CHANNEL_RULE_MISSING
- `SP3650_4_PPN`: `PPN_source_calibration` — SOURCE_HAMILTONIAN_OWNER_MISSING
- `SP3650_5_EM`: `EM_Maxwell_stress_source` — SAME_FRAME_SOURCE_OWNER_UNSIGNED
- `SP3650_6_orbital`: `orbital_source_mass_charge` — ORBITAL_SOURCE_MAP_MISSING
- `SP3650_7_total_guard`: `all_local_arenas` — NO_CANCELLATION_POLICY_ACTIVE

## Decisions
- `DEC3650_0_theorem_shape`: `SOURCE_CURRENT_THEOREM_SHAPE_EXACT` — The source-current zero route is mathematically clear: fixed T_Q plus fixed matter representation/source measure gives beta_source_alpha=0.
- `DEC3650_1_current_verdict`: `PARENT_SOURCE_CURRENT_OWNER_UNSIGNED` — Current MTS does not parent-sign representation labels, current measure, material source markers, or boundary/source flux silence.
- `DEC3650_2_coefficients`: `BETA_SOURCE_ROWS_CREATED_NOT_SCORE_READY` — beta_source_alpha, beta_charge_lattice, b_J_source, b_material_marker, B_A_EM, b_boundary_current, and q_source_EM_abs remain nonclaim rows.
- `DEC3650_3_next`: `MATTER_REPRESENTATION_SOURCE_SENSITIVITY_NEXT` — Next target is matter representation/source sensitivity: either prove material labels and EM binding sensitivities are quotient-owned, or build the composition matrix rows.

## Next checkpoint

`3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md` via `scripts/Y5_R2FR_3651_matter_representation_source_sensitivity_or_composition_matrix_row.py`.

## Sources
- `next_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md` exists=True needle_found=True
- `coeff_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_FEM_BALPHA_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `proj_3649`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3649_EM_OBSERVABLE_PROJECTION_ROWS.csv` exists=True needle_found=True
- `em_lock_989`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv` exists=True needle_found=True
- `alpha_audit_1047`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv` exists=True needle_found=True
- `vertex_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv` exists=True needle_found=True
- `matrix_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv` exists=True needle_found=True
- `doc_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md` exists=True needle_found=True
- `doc_1054`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md` exists=True needle_found=True
- `doc_1055`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
