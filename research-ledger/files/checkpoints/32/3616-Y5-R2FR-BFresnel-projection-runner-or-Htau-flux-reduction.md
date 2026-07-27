# 3616 Y5 R2FR: B_Fresnel projection runner or H_tau flux reduction

## Verdict
- The project is no longer merely saying `K_Fresnel missing`: the exact comparison contract is now written.
- The GRB bound constrains `xi`; MTS must first predict an effective polarization rotation `Delta_theta_MTS`, then invert it into `xi_MTS_eff`.
- The comparator is deliberately blocked until the root-split coefficient and MTS amplitude are parent-owned.

## Projection bridge
- Source model: `E_pm^2 = p^2 +/- 2 xi p^3/M_pl`.
- First-order split: `omega_pm = k +/- xi k^2/M_pl`.
- Rotation inversion: `xi_eff = Delta_theta_MTS M_pl H0/(k_obs^2 I(z))`.
- MTS contract: `|xi_MTS_eff| <= K_Fresnel(z, band, observer) B_Fresnel_MTS`.
- Projection coefficient: `K_Fresnel := M_pl H0 K_theta/(k_obs^2 I(z))`.

## What remains genuinely missing
- `K_theta`: the linearized root-split coefficient from the principal constitutive/Fresnel residual.
- `B_Fresnel_MTS`: the parent-owned amplitude of the MTS principal-cone residual.
- GRB bandpass averaging: finite energy bands and spectrum weighting must be included before any score.

## Comparator
- `P8_Y5_R2FR_3616_PROJECTION_RUNNER_TEMPLATE.csv` creates rows for GRB 061122 and GRB 140206A.
- `P8_Y5_R2FR_3616_GRB_BOUND_COMPARATOR_SMOKE.csv` proves the runner refuses to score missing parent inputs.
- This is the right kind of blocked result: the observable bound is real, the bridge is explicit, and the missing pieces are sharply local.

## H_tau backup reduction
- `I_EH_stationary_boundary` is zero if the boundary generator is exactly stationary, no radiative news crosses the surface, and corners are fixed.
- `I_matter_EM_flux` is zero if matter/EM fields are stationary and no material or Poynting flux crosses the boundary.
- Otherwise both terms now have residual envelopes rather than vague missingness.

## Next target
- `3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md`.
- First route: derive `K_theta` from the linearized Fresnel quartic.
- Backup route: source or theorem-zero the stationarity/no-flux clauses.

## Claim status
- `NO_CLAIM`: this is a derivation and comparator-architecture checkpoint.
