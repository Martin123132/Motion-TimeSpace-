# 3660 - QX source-charge zero proof or gamma bound input pack

**Status:** 3660 derives Q_X=sum_A int rho_A Q_A^X d^3x and the conditional Q_X=0 theorem, refuses the unsigned zero, and stages the gamma-bound input pack for the nonzero source-charge branch.

**Claim ceiling:** no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed.

## Main result

`Q_X` is no longer just a missing coupling label. It is the integrated local source charge

`Q_X = int_source d^3x J_X = sum_A int_source d^3x rho_A Q_A^X`,

with `Q_A^X = partial ln M_A^eff/partial Xhat` from the material/source sensitivity law.

Therefore the clean local-GR route is now exact but conditional: if every ordinary-matter constituent has `Q_A^X=0`, the source measure has no X-dependent normalization, and boundary hair is absent, then `Q_X=0`, `A_X=0`, and the local gamma profile vanishes.

Current MTS does not yet sign those parent clauses, so 3660 refuses the zero claim and writes the nonclaim gamma-bound input pack. The nonzero branch must score

`A_X ~= Q_X/(4*pi*Z_X)`

inside the Cassini envelope for `delta_gamma_MTS`.

## QX zero proof attempt
- `QXZ3660_0_source_definition`: SOURCE_CHARGE_DEFINITION_DERIVED - `Q_X = int_source d^3x J_X = sum_A int_source d^3x rho_A Q_A^X`
- `QXZ3660_1_material_sensitivity_link`: QX_REDUCED_TO_MATERIAL_SENSITIVITY_MATRIX - `Q_A^X = partial ln M_A^eff/partial Xhat`
- `QXZ3660_2_zero_condition`: CONDITIONAL_QX_ZERO_THEOREM_DERIVED - `forall A: Q_A^X=0 and b_J_source=0 and B_X=0 => Q_X=0`
- `QXZ3660_3_countermodel`: NONZERO_SOURCE_CHARGE_COUNTERMODEL_LIVE - `Q_A^X = beta_source_alpha,A*b_alpha + B_A^EM*f_EM + B_A^m*b_m + B_A^nuc*b_nuc + b_J_source,A + b_material_marker,A + b_boundary,A`
- `QXZ3660_4_current_verdict`: PARENT_QX_ZERO_UNSIGNED_BOUND_PACK_REQUIRED - `Q_X=0 not accepted; build gamma-bound input pack for Q_X/Z_X branch`

## QX zero-clause audit
- `QZA3660_0_representation_descent`: UNSIGNED - matter representation labels fixed or quotient-owned
- `QZA3660_1_source_measure_descent`: UNSIGNED - particle/source measure and current normalization descend through q
- `QZA3660_2_no_material_marker`: UNSIGNED - no independent material marker chi_A(X_N)
- `QZA3660_3_no_binding_leak`: UNSIGNED - mass/binding pieces have no live X sensitivity or are sourced and bounded
- `QZA3660_4_source_hamiltonian_owner`: UNSIGNED - weak-field source Hamiltonian fixes active/inertial source map
- `QZA3660_5_boundary_no_hair`: UNSIGNED - boundary hair B_X does not inject exterior profile amplitude
- `QZA3660_6_total`: NOT_SIGNED - all Q_X zero clauses hold together

## Gamma-bound input pack
- `GBI3660_0_QX`: `Q_X` - MISSING_PARENT_ZERO_OR_SOURCE_COMPOSITION
- `GBI3660_1_QA`: `Q_A_X` - MISSING_COMPONENT_SENSITIVITIES
- `GBI3660_2_ZX`: `Z_X` - MISSING_PARENT_QUADRATIC_ACTION
- `GBI3660_3_lambdaX`: `lambda_X` - MISSING_PARENT_HESSIAN_OR_RANGE
- `GBI3660_4_AX`: `A_X` - MISSING_QX_ZX_INPUTS
- `GBI3660_5_kH`: `k_H` - MISSING_WEAK_FIELD_PROJECTION
- `GBI3660_6_kG`: `k_G` - MISSING_WEAK_FIELD_PROJECTION
- `GBI3660_7_gamma_kernel`: `K_gamma_profile` - MISSING_GAMMA_GEOMETRY_KERNEL
- `GBI3660_8_boundary_readout_source`: `C_other_gamma` - MISSING_COMPONENT_BOUNDS

## Bound formulas
- `GBF3660_0_amplitude`: `profile amplitude` - substitute into C_gradient_TF_gamma
- `GBF3660_1_gamma_profile_envelope`: `gamma profile envelope` - Cassini gamma nonclaim score formula once inputs are real
- `GBF3660_2_zero_shortcut`: `source-charge zero shortcut` - theorem-zero route if parent signs source-charge descent

## Decisions
- `DEC3660_0_zero_route`: DERIVED_CONDITIONALLY_UNSIGNED - if parent matter/source descent signs every Q_A^X zero clause, local gamma profile amplitude vanishes
- `DEC3660_1_bound_route`: INPUT_PACK_READY_PLACEHOLDERS_REFUSED - if Q_X is nonzero or unsigned, next work must source the profile/operator inputs before any score

## Claim gates
- `CG3660_0_QX_definition`: PASSED_DERIVATION - Q_X source charge definition derived
- `CG3660_1_QX_zero`: PASSED_CONDITIONAL_THEOREM - Q_X=0 theorem derived conditionally
- `CG3660_2_countermodel`: ACTIVE_GUARD - nonzero Q_X branch remains legal
- `CG3660_3_bound_pack`: PASSED_INPUT_PACK - gamma-bound input pack staged
- `CG3660_4_no_claim`: ACTIVE_GUARD - no local-GR/gamma pass claimed
- `CG3660_5_next`: QX_COMPONENT_BASIS_NEXT - next step decomposes Q_X or sources the profile inputs

## Next checkpoint

`3661-Y5-R2FR-QX-component-basis-decomposition-or-shared-bound-runner.md` via `scripts/Y5_R2FR_3661_QX_component_basis_decomposition_or_shared_bound_runner.py`.

## Sources
- `next_3659`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3659_NEXT_TARGET.csv` exists=True needle_found=True
- `constant_theorem_3659`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3659_CONSTANT_FIELD_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `profile_inputs_3659`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3659_PROFILE_INPUT_ACQUISITION_ROWS.csv` exists=True needle_found=True
- `source_gate_3659`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3659_SOURCE_CHARGE_GATE_ROWS.csv` exists=True needle_found=True
- `validation_3659`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3659_VALIDATION.csv` exists=True needle_found=True
- `current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `material_theorem_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATTER_SENSITIVITY_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `material_rows_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3651_MATERIAL_SENSITIVITY_ROWS.csv` exists=True needle_found=True
- `gm_rows_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv` exists=True needle_found=True
- `local_bounds_R3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
