# 3942 - Constraint Green-Map Uniqueness or Homogeneous Mass-Mode Bound

Timestamp: `2026-07-01T12:49:52+00:00`

## Result

3942 attacks the free-monopole danger directly.

The key discipline point is:

`asymptotic flatness alone does not kill a source-free C/r mode`.

A `C/r` mode is just the Newton/Schwarzschild mass monopole. If we let it in without source ownership, we have smuggled measured `GM` instead of deriving it.

## Conditional Theorem

In the weak-field local limit, the difference of two source-equivalent constraint solutions obeys:

`nabla^2 delta Phi = 0`.

Its exterior monopole piece is:

`delta Phi_hom = C_1/r + ...`

and the mass-kernel charge is:

`R_kernel = -C_1/G_* = (1/(4*pi*G_*)) int_{S_infty} grad(delta Phi).dS`.

Therefore:

`Z_ref_charge and Z_no_incoming and Z_same_tau_surface and Z_no_extra_boundary_charge => R_kernel=0`.

## Current Verdict

- Progress: the free homogeneous mass mode is isolated exactly.
- Honest guard: asymptotic flatness alone is rejected as a proof.
- Conditional win: `R_kernel=0` inside a charge-fixed, no-incoming, same-surface, no-extra-boundary local branch.
- Public claim: still blocked until `M_H_ref` and the homogeneous reference-charge anchor are source-owned.

## Bound Route

If the zero switch is not signed:

`|R_kernel|/M_H_ref <= epsilon_ref_charge + epsilon_incoming_mass + epsilon_surface_flux + epsilon_boundary_charge + epsilon_radiative_mass_flux`.

That keeps the free monopole as a finite no-cancellation row rather than hiding it in calibration.

## Source Register

- Source rows found: `14/14`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3942_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3942_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3942_GREEN_MAP_KERNEL_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3942_HOMOGENEOUS_MODE_AUDIT.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3942_BOUNDARY_CONDITION_SWITCH.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3942_RKERNEL_BOUND_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3942_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3942_NEXT_TARGET.csv`

## Next Target

`3943-Y5-R2FR-MHref-positive-same-frame-reference-charge-or-Rkernel-source-row.md`
