# 3648 Y5 R2FR no-marker constant superselection or alphaEM mass clock coefficient row

**Status:** 3648 consolidates the no-marker constant-superselection theorem, rejects current zero-claim status for alpha_EM/mass/clock/material channels, and creates explicit b_alpha, b_mu, b_mA, b_nuc, b_clock, sensitivity, and qbar_constants rows.

**Claim ceiling:** no constant-zero, local-GR/Newton, R10, PPN, clock, WEP, orbital, or EM stress pass is claimed.

## Main result

The clean route is exact: if every ordinary-matter constant or marker `theta_I` is fixed representation data or factors through `q`, then `Dq[v_X]=0` gives `Lie_vX theta_I=0`. That would set `b_alpha`, mass-ratio coefficients, clock coefficients, and material-marker charge to zero.

Current MTS does not yet parent-sign the no-extra-F2, no-mass-vertex, no-clock-readout, and no-marker clauses. The coefficient rows therefore stay live and nonclaim.

## Theorem rows
- `CST3648_0_statement`: EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED — If all theta_I close in one parent branch, b_alpha=b_mass=b_clock=b_material=0 and qbar_constants_abs=0.
- `CST3648_1_alpha_EM`: FAIL_CURRENT_CLAIM_RETAIN_B_ALPHA — Current corpus does not parent-sign unique-F2/no-extra-F2/readout closure; b_alpha remains live.
- `CST3648_2_mass_ratios`: FAIL_CURRENT_CLAIM_RETAIN_B_MASS — Mass/material channels stay live without a parent matter-spectrum theorem.
- `CST3648_3_clock_transitions`: CLOCK_THEOREM_INHERITS_CONSTANT_DEBT — Clock sensitivities are useful anchors, not a zero proof.
- `CST3648_4_material_markers`: MATERIAL_MARKER_ZERO_UNSIGNED — Composition/WEP and R10 material-response rows remain live.
- `CST3648_5_verdict`: FAIL_CURRENT_CLAIM_COEFFICIENT_ROWS_REQUIRED — The theorem is clean but unsigned; coefficient rows are required.

## Constant/marker audit
- `CMA3648_0_alpha_EM`: `b_alpha` — MISSING_ALPHA_OWNER_OR_B_ALPHA (clock;EM spectra;WEP;R10;EM_Maxwell_stress)
- `CMA3648_1_mass_ratio`: `b_mu;b_mA` — MISSING_MATTER_SPECTRUM_OWNER_OR_B_MASS (clock;WEP;composition;R10)
- `CMA3648_2_nuclear_binding`: `b_nuc;b_binding` — MISSING_BINDING_SENSITIVITY_ROWS (WEP;composition;R10)
- `CMA3648_3_clock`: `b_clock_i` — MISSING_CLOCK_PROJECTION (clock;redshift;alpha drift)
- `CMA3648_4_material_marker`: `b_material;S_A` — MISSING_NO_MARKER_THEOREM_OR_SENSITIVITIES (WEP;composition;source_test_R10)
- `CMA3648_5_source_weight`: `q_source_weight` — MISSING_SOURCE_WEIGHT_LOCK (R10;GM calibration;orbital)
- `CMA3648_6_total`: `qbar_constants_abs` — SCHEMA_READY_VALUES_MISSING (all_local_arenas)

## Coefficient rows
- `CP3648_0_b_alpha`: `b_alpha` — MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM
- `CP3648_1_b_mu`: `b_mu` — MISSING_B_MU_OR_PARENT_ZERO_THEOREM
- `CP3648_2_b_mA`: `b_mA` — MISSING_B_MA_OR_MATERIAL_SENSITIVITY
- `CP3648_3_b_nuc`: `b_nuc;b_binding` — MISSING_BINDING_COEFFICIENTS
- `CP3648_4_b_clock`: `b_clock_i` — MISSING_CLOCK_CONSTANT_PROJECTION
- `CP3648_5_sensitivities`: `S_A;S_alpha;S_clock;f_binding` — MISSING_SENSITIVITY_VECTOR
- `CP3648_6_qbar_constants`: `qbar_constants_abs` — SCHEMA_READY_VALUES_MISSING

## Observable projections
- `OP3648_0_clock_alpha`: `clock_alpha_sensitivity` — SENSITIVITIES_AVAILABLE_MTS_PROJECTION_MISSING
- `OP3648_1_clock_redshift`: `clock_redshift_LPI` — ANCHOR_AVAILABLE_CLOCK_MAP_MISSING
- `OP3648_2_WEP`: `WEP_composition` — ANCHOR_AVAILABLE_COMPOSITION_MATRIX_MISSING
- `OP3648_3_R10`: `R10_short_range` — BOUND_AND_MTS_COMPONENTS_NOT_CLAIM_READY
- `OP3648_4_EM_stress`: `EM_Maxwell_stress` — EM_THEOREM_OR_B_ALPHA_ROW_REQUIRED
- `OP3648_5_PPN_source`: `PPN_source_calibration` — NOT_SCORE_READY
- `OP3648_6_total_guard`: `all_local_arenas` — NO_CANCELLATION_POLICY_ACTIVE

## Decisions
- `DEC3648_0_theorem_shape`: CONSTANT_SUPERSELECTION_THEOREM_SHAPE_EXACT — No-marker constant superselection is a clean chain-rule theorem if constants are fixed representation data or quotient-owned.
- `DEC3648_1_current_verdict`: PARENT_CONSTANT_SIGNATURE_UNSIGNED — Current MTS cannot claim b_alpha, b_mass, or b_clock vanish because no-extra-F2, no-mass-vertex, and no-clock-readout signatures are unsigned.
- `DEC3648_2_coefficients`: CONSTANT_COEFFICIENT_ROWS_CREATED_NOT_SCORE_READY — b_alpha, b_mu, b_mA, b_nuc, b_clock_i, and sensitivity rows are retained as nonclaim rows.
- `DEC3648_3_next`: EM_MAXWELL_STRESS_OR_FEM_NEXT — Next target should attack EM/Maxwell specifically: unique F^2 normalization and no f_X(X)F^2 counterterm, or b_alpha remains live.

## Next target

`3649-Y5-R2FR-EM-Maxwell-same-frame-stress-or-fEM-coefficient-row.md` via `scripts/Y5_R2FR_3649_EM_Maxwell_same_frame_stress_or_fEM_coefficient_row.py`.

## Sources
- `next_3647`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3647_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3647`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3647-Y5-R2FR-observed-frame-no-shadow-theorem-or-cg-bdis-coefficient-row.md` exists=True needle_found=True
- `nomarker_736`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv` exists=True needle_found=True
- `blindness_594`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_594_MATTER_BLINDNESS_GATE.csv` exists=True needle_found=True
- `no_shadow_1046`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md` exists=True needle_found=True
- `pack_1028`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md` exists=True needle_found=True
- `const_1047`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md` exists=True needle_found=True
- `no_extra_1048`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md` exists=True needle_found=True
- `constant_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_constant_sector_universality_CONTRACT.csv` exists=True needle_found=True
- `constant_ownership_637`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv` exists=True needle_found=True
- `constant_zero_638`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv` exists=True needle_found=True
- `clock_sensitivity_646`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv` exists=True needle_found=True
- `clock_projection_646`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_646_CLOCK_PROJECTION_LEDGER.csv` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
