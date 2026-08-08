# 3659 - Parent local constant-field theorem or profile input acquisition

**Status:** 3659 derives the local exterior profile law and the constant-field theorem: the gamma-relevant profile amplitude is controlled by Q_X/Z_X, so Q_X=0 is the clean local-GR route and nonzero Q_X must be bounded.

**Claim ceiling:** no MTS gamma prediction, local-GR pass, PPN pass, Newtonian pass, source-calibration pass, WEP/R10/clock/orbital pass, or EH-dominance pass is claimed.

## Main result

The local gamma problem has narrowed to the coupling/source-charge gate.

For a stable local extra field, the exterior equation has the schematic form

`Z_X (nabla^2-lambda_X^-2) deltaX = 0` outside the compact source,

so with no growing mode the exterior profile is

`deltaX(r)=A_X exp(-r/lambda_X)/r`.

The amplitude is not magic: `A_X ~= Q_X/(4*pi*Z_X)` in canonical Green normalization. Therefore the clean local-GR route is `Q_X=0` plus no boundary hair, which gives `deltaX=0` and kills the gamma STF profile. If `Q_X` is not zero, the theory must bound `Q_X/Z_X`, `lambda_X`, `k_H`, and `k_G` against Cassini gamma.

## Constant-field theorem attempt
- `CFT3659_0_local_linearized_EOM`: LINEAR_LOCAL_EOM_FORM_DERIVED_CONDITIONALLY - `Z_X*(nabla^2-lambda_X^-2)*deltaX = -J_X`
- `CFT3659_1_exterior_profile`: EXTERIOR_PROFILE_LAW_DERIVED - `J_X=0 outside source => deltaX=A_X*exp(-r/lambda_X)/r`
- `CFT3659_2_amplitude_source_charge`: COUPLING_IS_THE_PROFILE_AMPLITUDE_GATE - `A_X ~= Q_X/(4*pi*Z_X) for the canonical Green normalization`
- `CFT3659_3_constant_field_zero`: CONDITIONAL_CONSTANT_FIELD_ZERO_THEOREM_DERIVED - `Q_X=0 and no_boundary_hair and Z_X>0 and lambda_X^2>0 => deltaX=0 => C_gradient_TF_gamma=0`
- `CFT3659_4_current_MTS_status`: PARENT_SOURCE_CHARGE_ZERO_UNSIGNED - `need parent Q_X=0 or sourced A_X,lambda_X,k_H,k_G`

## Profile/source input rows
- `PI3659_0_QX_source`: `Q_X` - MISSING_PARENT_SOURCE_CHARGE_ZERO_OR_NUMERIC_SOURCE
- `PI3659_1_ZX`: `Z_X` - MISSING_PARENT_QUADRATIC_ACTION_NORMALIZATION
- `PI3659_2_lambdaX`: `lambda_X` - MISSING_PARENT_MASS_OR_RANGE
- `PI3659_3_AX`: `A_X` - MISSING_QX_ZX_NUMERIC_INPUTS
- `PI3659_4_kH`: `k_H` - MISSING_WEAK_FIELD_OPERATOR_PROJECTION
- `PI3659_5_kG`: `k_G` - MISSING_WEAK_FIELD_OPERATOR_PROJECTION
- `PI3659_6_boundary_hair`: `B_X` - MISSING_BOUNDARY_SILENCE_SIGNATURE

## Source-charge gates
- `SCG3659_0_matter_descent_zero`: `Q_X` - UNSIGNED_BUT_NOW_IDENTIFIED_AS_GAMMA_CRITICAL
- `SCG3659_1_nonzero_charge_bound`: `Q_X/Z_X` - BOUND_ROUTE_READY_INPUTS_MISSING

## Claim gates
- `CG3659_0_exterior_profile`: PASSED_DERIVATION - exterior local profile law derived
- `CG3659_1_coupling_gate`: PASSED_DERIVATION - profile amplitude tied to source charge
- `CG3659_2_constant_field`: PASSED_CONDITIONAL_THEOREM - constant-field zero theorem derived conditionally
- `CG3659_3_no_claim`: ACTIVE_GUARD - no local-GR/gamma pass claimed
- `CG3659_4_next`: SOURCE_CHARGE_ZERO_OR_BOUND_NEXT - next step targets Q_X zero proof or bound acquisition

## Next checkpoint

`3660-Y5-R2FR-QX-source-charge-zero-proof-or-gamma-bound-input-pack.md` via `scripts/Y5_R2FR_3660_QX_source_charge_zero_proof_or_gamma_bound_input_pack.py`.

## Sources
- `next_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_NEXT_TARGET.csv` exists=True needle_found=True
- `radial_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_RADIAL_STF_DERIVATION_ROWS.csv` exists=True needle_found=True
- `profiles_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv` exists=True needle_found=True
- `interface_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3658_GAMMA_SCORE_INTERFACE_ROWS.csv` exists=True needle_found=True
- `validation_3658`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3658_VALIDATION.csv` exists=True needle_found=True
- `source_current_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md` exists=True needle_found=True
- `matter_sensitivity_3651`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md` exists=True needle_found=True
- `weak_field_3652`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md` exists=True needle_found=True
- `local_bounds_R3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` exists=True needle_found=True
