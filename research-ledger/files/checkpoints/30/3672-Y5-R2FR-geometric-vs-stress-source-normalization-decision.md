# 3672 - Geometric vs stress source normalization decision

**Status:** 3672 stops using one overloaded k_H coupling. The scalar-slip amplitude is split into a dimensionless geometric branch xi_H_geo=|k_H_geo*f_EM/Z_X| and a stress-energy branch xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X| with Sigma_H in J/m.

This checkpoint resolves the coupling ambiguity by refusing to let one symbol do two incompatible jobs.

## Decision
- If the Hessian-STF term is part of the parent geometric field equation, use the normalized branch:
  `P_TF[D_bD_b Y]=k_H_geo P_TF[D_bD_b X_b]`, so `C_parent_H=1` by convention and `xi_H_geo=|k_H_geo*f_EM/Z_X|`.
- If the term is a stress-energy source, use:
  `pi_TF=Sigma_H P_TF[partial_i partial_j X_b]*(f_EM/Z_X)`, so `xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X|`.
- These are not interchangeable until the parent action/first variation says where the operator lives.

`kappa_E=8*pi*G_ref/c^4=2.076647442845e-43 m/J` for the stress-route conversion row.

Strongest inherited scalar-slip row: `YX3671_eta_100_zeta_215.032` gives `|k_H_geo*f_EM/Z_X| <= 2.979212325428e-05` or `|Sigma_H*f_EM/Z_X| <= 1.434625957185e+38 J/m`.

No Cassini/local-GR claim follows from this: the row is a units-clean bridge, not a sourced coefficient.

## Decision rows
- `DEC3672_0_do_not_merge_routes`: DECISION_LOCKED_NONCLAIM - `Do not use one symbol k_H for both branches.`
- `DEC3672_1_geometric_branch`: PREFERRED_INTERNAL_ROUTE_IF_PARENT_ACTION_PLACES_TERM_IN_DELTA_E - `xi_H_geo=|k_H_geo*f_EM/Z_X|`
- `DEC3672_2_stress_branch`: SOURCE_NORMALIZATION_ROUTE_REQUIRES_STRESS_LEDGER - `xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X|`
- `DEC3672_3_do_not_claim_equivalence`: CLAIM_GUARDRAIL_LOCKED - `xi_H = xi_H_geo or xi_H_stress depending on signed parent placement`
- `DEC3672_4_next_route`: SELECT_GEOMETRIC_PARENT_OWNER_HUNT - `hunt parent action first; retain stress branch as bounded fallback`

## Unit ledger
- `UL3672_0_Y`: `Y=Phi-Psi` [dimensionless] - LOCKED
- `UL3672_1_Xb`: `X_b=e^{-rho/eta}/rho` [dimensionless] - LOCKED_BY_3671_NORMALIZATION
- `UL3672_2_geo`: `k_H_geo` [dimensionless] - DEFINED_NONCLAIM
- `UL3672_3_stress`: `Sigma_H` [J/m] - DEFINED_NONCLAIM
- `UL3672_4_kappa`: `kappa_E=8*pi*G_ref/c^4` [m/J] - CONVENTIONAL_CONSTANT_ROW_NONCLAIM
- `UL3672_5_xi`: `xi_H` [dimensionless] - BRIDGE_VARIABLE_NONCLAIM

## Dual branch bounds
- `GB3672_eta_0.01_zeta_215.032`: `|k_H_geo*f_EM/Z_X| <= 2.995098963045e+40`; `|Sigma_H*f_EM/Z_X| <= 1.442276094271e+83 J/m`
- `GB3672_eta_0.01_zeta_1000`: `|k_H_geo*f_EM/Z_X| <= 3.754234935503e+40`; `|Sigma_H*f_EM/Z_X| <= 1.807834521184e+83 J/m`
- `GB3672_eta_0.01_zeta_2000`: `|k_H_geo*f_EM/Z_X| <= 4.118255332132e+40`; `|Sigma_H*f_EM/Z_X| <= 1.983126864563e+83 J/m`
- `GB3672_eta_0.1_zeta_215.032`: `|k_H_geo*f_EM/Z_X| <= 7.844214566002e+00`; `|Sigma_H*f_EM/Z_X| <= 3.777345352014e+43 J/m`
- `GB3672_eta_0.1_zeta_1000`: `|k_H_geo*f_EM/Z_X| <= 9.832404364550e+00`; `|Sigma_H*f_EM/Z_X| <= 4.734748981310e+43 J/m`
- `GB3672_eta_0.1_zeta_2000`: `|k_H_geo*f_EM/Z_X| <= 1.072904806379e+01`; `|Sigma_H*f_EM/Z_X| <= 5.166523619961e+43 J/m`

## Parent-owner requirements
- `POR3672_0_parent_operator_location`: MISSING_PARENT_ACTION_MAPPING - locate Hessian-STF in parent first variation
- `POR3672_1_dimensionless_normalization`: CONVENTION_DEFINED_NEEDS_PARENT_SIGNOFF - fix X_b and derivative convention
- `POR3672_2_source_descent`: MISSING_IF_STRESS_ROUTE - stress-energy descent if RHS route used
- `POR3672_3_boundary_kernel`: MISSING_BOUNDARY_CERTIFICATE - STF inversion boundary silence
- `POR3672_4_other_floors`: MISSING_FLOOR_BOUNDS - C_other_gamma and quadratic floors

## Claim gates
- `CG3672_0_split`: PASS_DECISION - geometric/stress split
- `CG3672_1_units`: PASS_NONCLAIM_LEDGER - unit ledger
- `CG3672_2_geo_claim`: BLOCKED_PARENT_MAPPING - geometric route claim
- `CG3672_3_stress_claim`: BLOCKED_SOURCE_DESCENT - stress route claim
- `CG3672_4_gamma_claim`: BLOCKED_NONCLAIM - Cassini/local-GR claim

## Next target
`3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md` via `scripts/Y5_R2FR_3673_parent_action_Hessian_STF_operator_location.py`.

## Sources
- `handoff_3671`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3671_NEXT_TARGET.csv` exists=True needle_found=True
- `doc_3671`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3671-Y5-R2FR-Hessian-STF-parent-normalization-or-kH-source-coefficient.md` exists=True needle_found=True
- `forks_3671`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3671_NORMALIZATION_FORK_ROWS.csv` exists=True needle_found=True
- `kernels_3671`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3671_SCALAR_SLIP_KERNEL_ROWS.csv` exists=True needle_found=True
- `bounds_3671`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3671_CONDITIONAL_XIH_BOUND_ROWS.csv` exists=True needle_found=True
- `weak_response_2477`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md` exists=True needle_found=True
- `metric_inputs_3384`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv` exists=True needle_found=True
- `common_mode_3060`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv` exists=True needle_found=True
