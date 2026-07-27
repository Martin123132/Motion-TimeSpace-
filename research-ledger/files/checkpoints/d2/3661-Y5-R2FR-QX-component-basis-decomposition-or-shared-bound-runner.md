# 3661 - QX component basis decomposition or shared bound runner

**Status:** 3661 decomposes Q_X into source-current, EM-binding, mass/nuclear, source-measure, material-marker, and boundary components; no component is zero-claimed, and the shared WEP/R10/gamma/PPN arenas now point to the same basis.

**Claim ceiling:** no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed.

## Main result

`Q_X` is now decomposed into a component basis:

`Q_X = beta_source_alpha_bar*b_alpha + B_source_EM*f_EM + B_source_m*b_m + B_source_nuc*b_nuc + b_J_source_bar + b_material_marker_bar + b_boundary_bar + B_X`.

Until a parent theorem signs cancellations, the active policy is the absolute no-cancellation envelope. This matters because the same component basis feeds WEP, R10, Cassini gamma, and source-calibration/PPN; it is not allowed to tune a separate coupling for each arena.

## Component basis rows
- `QXB3661_0_beta_source_alpha`: `beta_source_alpha_bar*b_alpha` - MISSING_PARENT_SOURCE_CURRENT_THEOREM -> WEP;R10;gamma;PPN;orbital
- `QXB3661_1_EM_binding`: `B_source_EM*f_EM` - FORMULA_DERIVED_NUMERIC_COMPOSITION_MISSING -> WEP;R10;gamma;EM
- `QXB3661_2_mass_scale`: `B_source_m*b_m` - MISSING_MASS_SENSITIVITY_OWNER -> WEP;R10;gamma;PPN
- `QXB3661_3_nuclear_binding`: `B_source_nuc*b_nuc` - MISSING_NUCLEAR_BINDING_SENSITIVITY -> WEP;R10;gamma
- `QXB3661_4_source_measure`: `b_J_source_bar` - MISSING_SOURCE_MEASURE_DESCENT -> WEP;R10;gamma;PPN;orbital
- `QXB3661_5_material_marker`: `b_material_marker_bar` - COUNTERMODEL_LIVE_PARENT_BAN_MISSING -> WEP;R10;gamma
- `QXB3661_6_boundary`: `b_boundary_bar+B_X` - MISSING_BOUNDARY_SILENCE_SIGNATURE -> gamma;PPN;orbital

## No-cancellation envelopes
- `QXE3661_0_source_basis_sum`: BASIS_DECOMPOSITION_DERIVED_VALUES_MISSING - `Q_X = beta_source_alpha_bar*b_alpha + B_source_EM*f_EM + B_source_m*b_m + B_source_nuc*b_nuc + b_J_source_bar + b_material_marker_bar + b_boundary_bar + B_X`
- `QXE3661_1_no_cancellation_bound`: NO_CANCELLATION_ENVELOPE_ACTIVE - `|Q_X| <= |beta_source_alpha_bar*b_alpha| + |B_source_EM*f_EM| + |B_source_m*b_m| + |B_source_nuc*b_nuc| + |b_J_source_bar| + |b_material_marker_bar| + |b_boundary_bar| + |B_X|`

## Component zero audit
- `QZA3661_0_beta_source_alpha`: ZERO_NOT_SIGNED_MISSING_PARENT_SOURCE_CURRENT_THEOREM - parent signs zero/absence of source-current/charge-normalization drift
- `QZA3661_1_EM_binding`: ZERO_NOT_SIGNED_FORMULA_DERIVED_NUMERIC_COMPOSITION_MISSING - parent signs zero/absence of EM Coulomb binding sensitivity
- `QZA3661_2_mass_scale`: ZERO_NOT_SIGNED_MISSING_MASS_SENSITIVITY_OWNER - parent signs zero/absence of ordinary mass-scale sensitivity
- `QZA3661_3_nuclear_binding`: ZERO_NOT_SIGNED_MISSING_NUCLEAR_BINDING_SENSITIVITY - parent signs zero/absence of nuclear binding/source sensitivity
- `QZA3661_4_source_measure`: ZERO_NOT_SIGNED_MISSING_SOURCE_MEASURE_DESCENT - parent signs zero/absence of source measure/current normalization sensitivity
- `QZA3661_5_material_marker`: ZERO_NOT_SIGNED_COUNTERMODEL_LIVE_PARENT_BAN_MISSING - parent signs zero/absence of explicit material marker leakage
- `QZA3661_6_boundary`: ZERO_NOT_SIGNED_MISSING_BOUNDARY_SILENCE_SIGNATURE - parent signs zero/absence of boundary/domain/hair sensitivity

## Shared bound arenas
- `SBA3661_0_WEP`: `WEP/MICROSCOPE` / `eta_AB` - BOUND_ANCHOR_READY_COMPONENT_VALUES_MISSING
- `SBA3661_1_R10`: `short-range fifth force` / `alpha_X(lambda_X)` - SYMBOLIC_CURVE_REQUIRED_COMPONENT_VALUES_MISSING
- `SBA3661_2_gamma`: `Cassini/PPN gamma` / `delta_gamma_MTS` - BOUND_ANCHOR_READY_COMPONENT_VALUES_MISSING
- `SBA3661_3_PPN_orbital_source`: `PPN/orbital source calibration` / `q_GM_source_abs;Delta_PPN_MTS` - MIXED_BOUND_INTERFACE_READY_VALUES_MISSING

## Claim gates
- `CG3661_0_basis`: PASSED_DERIVATION - Q_X component basis decomposed
- `CG3661_1_no_cancellation`: PASSED_POLICY_GATE - absolute no-cancellation envelope active
- `CG3661_2_zero_audit`: PASSED_AUDIT - each component zero route audited
- `CG3661_3_shared_arenas`: PASSED_MAPPING_GATE - WEP/R10/gamma/PPN arenas mapped to same basis
- `CG3661_4_no_claim`: ACTIVE_GUARD - no local-GR/gamma/WEP/R10 pass claimed
- `CG3661_5_next`: EM_BINDING_COMPONENT_NEXT - next step should fill easiest component

## Next checkpoint

`3662-Y5-R2FR-EM-binding-component-first-fill-or-zero-theorem.md` via `scripts/Y5_R2FR_3662_EM_binding_component_first_fill_or_zero_theorem.py`.

## Sources
- `next_3660`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3660_NEXT_TARGET.csv` exists=True needle_found=True
- `proof_3660`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3660_QX_ZERO_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `input_pack_3660`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3660_GAMMA_BOUND_INPUT_PACK.csv` exists=True needle_found=True
- `formulas_3660`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3660_GAMMA_BOUND_FORMULAS.csv` exists=True needle_found=True
- `composition_schema_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_COMPOSITION_MATRIX_SCHEMA_ROWS.csv` exists=True needle_found=True
- `material_theorem_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `source_current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `gm_rows_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv` exists=True needle_found=True
- `local_bounds`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
