# 4155 - Worldtube Hilbert Source Measure And Poynting Flux Lock

Timestamp UTC: `2026-07-02T11:14:10+00:00`  
Branch: `MTS_R2FR_Y5_WORLDTUBE_HILBERT_POYNTING_4155`  
Decision: `WORLDTUBE_HILBERT_SOURCE_MEASURE_AND_POYNTING_ONCE_LOCK_DERIVED_CONDITIONALLY_PIM_HTAU_GLUE_NEXT`

## Purpose
4154 showed that Newton still fails unless `M_H` is the right closed source charge and `mu_extra` does not hide field/source flux.

This checkpoint locks the source-measure and Poynting accounting as far as the current parent route allows.

## Worldtube Source Measure
The source mass is not bare matter mass and not an orbital fit.

The clean definition is:

`M_H^dress[W;tau]=H_tau[S_outer]-H_tau[S_ref]=ell_M(Pi_M J_H_total)`.

with

`J_H_total=J_matter+J_EM+J_binding+dB_impr+J_rest_retained`.

The worldtube is parent-owned:

`W_H=closure(supp J_H_total)`.

If `J_H`, `tau`, `e_obs`, support, linked surfaces, and references are all same-branch and q-basic, source/worldtube selector leakage vanishes conditionally.

## Poynting Once-Only Lock
The Poynting vector is not decorative and not an extra patch:

`T_EM^{0i}=S_Poynting^i/c^2`.

Matter and EM exchange internally:

`nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda`,

`nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda`.

Therefore the conserved object is total matter+EM Hilbert stress. A trial extra source

`M_trial=ell_M(Pi_M J_H_total)+c_Poynt_extra int_boundary S_Poynting dot n dA`

double-counts the same energy flux, so the once-only branch forces

`c_Poynt_extra=0`.

## Stationary No-Flux Branch
The Poynting identity is:

`D_tau E_EM[V]+int_boundary S_Poynting dot n dA = -int_V J dot E dV + improvements`.

For a stationary isolated exterior collar with no imposed incoming/background radiation:

`time_avg(Phi_EM_rad)=0`.

Bound Coulomb/magnetostatic energy is still in `M_H`; it is not zeroed out. Only net leakage through the boundary is zeroed.

## Residual Branch
If the source is radiative, nonstationary, background-driven, or nonminimal, retain:

`|epsilon_EM_extra| <= (|Delta U_EM|+|W_matter|+|Phi_external|+|B_improvement|)/(|M_H| c^2)`.

Also retain explicit rows for:

- `C_XF2`;
- `Delta_Hodge_EM`;
- `C_EM_readout`;
- `epsilon_closed_source_failure`.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| dressed source measure | CONDITIONAL LOCK | source mass is Hilbert/Hamiltonian charge |
| Poynting once-only | CONDITIONAL LOCK | minimal EM flux counted once inside `J_H_total` |
| stationary no-flux | CONDITIONAL ZERO | closed local stationary collar has no net Poynting leakage |
| radiative/nonminimal EM | RETAINED | explicit residual coefficients required |
| Pi_M/H_tau glue | UNSIGNED | next source-measure bottleneck |
| Newton/local GR | NOT CLAIMED | this closes only a source-accounting subproblem |

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_WORLDTUBE_SOURCE_LOCK.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_POYNTING_ONCE_LOCK.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_FLUX_ZERO_OR_BOUND.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_RESIDUAL_COEFFICIENT_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_NEWTON_IMPACT_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4155_NEXT_TARGET.csv`

## Next Target
- `4156-Y5-R2FR-PiM-Htau-same-charge-glue-or-radial-source-residual.md`
- Prove `Pi_M J_H_total` and `H_tau` are the same parent source charge before readout, or retain radial/source-measure residual rows.
