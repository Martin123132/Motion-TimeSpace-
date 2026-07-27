# 3927 - B_escape Component Bound Pack: Projector/Domain, Boundary, History

Timestamp: `2026-07-01T11:20:06+00:00`

## Result

Built the `B_escape` component formula pack.

Projector/domain:

`epsilon_domain_projector_abs <= C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref + C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref + C_chi||delta_g chi_D|| + |Phi_D|/M_H_ref`.

Boundary/harmonic:

`B_boundary_harmonic := |P00_boundary| + |B_harmonic_boundary| + |Phi_B|/M_H_ref + |tau_wall_TF|/M_H_ref`.

History/nonlocal:

`B_history := K_hist[exp(-gamma_mem Delta t)||X_mem(t0)|| + (1-exp(-gamma_mem Delta t))sup||J_open+B_lift||/lambda_gap] + B_nonlocal_kernel`.

Derivative hair:

`B_deriv := |partial_t xi_1| + |partial_r xi_1| + |Delta_AB xi_1| + |delta_frame xi_1|`.

Total:

`|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs`.

## Meaning

The escape obstruction is now executable in structure: every major term has a formula, input list, and runner row. It is still not score-ready because source values or theorem-zero certificates are missing. The first target is projector/domain stress because it feeds the widest set of local-GR residuals.

## Source Register

- Source rows found: `20/20`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3927_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3927_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3927_BESCAPE_RUNNER_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3927_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3927_NEXT_TARGET.csv`

## Next Target

`3928-Y5-R2FR-projector-domain-certificate-or-first-Bescape-source-values.md`
