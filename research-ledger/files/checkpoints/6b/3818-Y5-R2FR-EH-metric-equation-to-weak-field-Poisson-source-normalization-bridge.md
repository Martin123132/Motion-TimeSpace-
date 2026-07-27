# 3818 - EH Metric Equation To Weak-Field Poisson Source-Normalization Bridge

## Status

- Status: `PASS_NONCLAIM_EH_TO_POISSON_THEOREM_AND_SOURCE_NORMALIZATION_GATES_BUILT`
- Claim level: private, nonclaim theorem bridge.
- Validation pass: `true`
- Main result: the EH-to-Poisson algebra is clean conditionally; the live blocker is source normalization, not the linearized GR calculation.

## EH To Poisson

The conditional weak-field bridge is:

```text
G_mu_nu + Lambda g_mu_nu + DeltaE_res_mu_nu = kappa_0 T_total_mu_nu
kappa_0 = 8*pi*G_ref/c^4
g_00 = -(1 + 2 Phi/c^2)
G_00^(1) = 2 nabla^2 Phi/c^2
T_00 = rho_H c^2

=> nabla^2 Phi = 4*pi*G_ref rho_H
```

This is exact conditional algebra, not a local-GR claim. It requires the EH operator, sign/gauge convention, same-frame Hilbert source, and residual operator silence or finite bounds.

## G Policy

We do **not** need to derive the numerical value of Newton's constant to reduce to GR. GR itself calibrates `G`. The MTS requirement is stricter in a different way:

```text
one fixed parent/calibrated G_ref
one Hilbert/Hamiltonian source mass
no arena-by-arena fitted GM absorption
```

If `kappa/G` is not parent-owned or superselected, its leakage enters finite product-lock residuals rather than being hidden in `GM`.

## Source Normalization Gate

The Poisson source must be:

```text
M_H_ref = int_D rho_H d^3x
        = c^-2 (H_tau[S_outer] - H_ref)
```

and the exterior source selector must satisfy:

```text
d(Pi_M J_H)=0
W_source = closure(supp J_H[tau])
```

Current status: this is still blocked by `M_H_ref`, `Pi_M` origin, commutator, worldtube glue, boundary/reference and measured-GM calibration.

## Finite Fallbacks

3818 emits:

```text
R_EH_Poisson_GM_total =
  R_EH_owner + R_Poisson_norm + R_GM_calibration
  + R_PiM_JH_flux + R_PPN_readout_tail
```

These rows keep the bridge scoreable without claiming Newton or local GR early.

## Next Target

`3819-Y5-R2FR-MHref-PiM-JH-source-selector-and-GM-anti-circularity-bridge.md`

Next we attack the actual remaining throat: `M_H_ref`, `Pi_M J_H`, worldtube selector, and anti-circular measured-GM calibration.

## Machine Outputs

- `source-intake\mts_residuals\P8_Y5_R2FR_3818_SOURCE_REGISTER.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_EH_METRIC_EQUATION_TEMPLATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_KAPPA_GREF_POLICY_AND_RESIDUALS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_FINITE_EH_POISSON_GM_RESIDUAL_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_CLAIM_GATES.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_DECISION_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_NEXT_TARGET.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3818_STATUS.csv`
- `source-intake\mts_residuals\P8_Y5_BRR545_3818_VALIDATION.csv`
