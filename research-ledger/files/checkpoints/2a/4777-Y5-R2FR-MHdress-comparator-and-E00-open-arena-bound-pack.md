# 4777 — MHdress Comparator and E00 Open-Arena Bound Pack

Generated: `2026-07-08T04:00:27+00:00`

## Result

4777 fills the first observed `GM` comparator row without cheating:

```text
mu_sun_nominal = 1.3271244e+20 m^3 s^-2
M_GM_sun_cal = mu_sun_nominal/G_cal = 1.988409870698051e+30 kg
sigma(M_GM_sun_cal) = 4.468805426856864e+25 kg
```

But:

```text
M_H^dress is still H_tau[S_link] - H_ref.
Observed GM/G_cal is only a comparator, not the definition of M_H^dress.
```

The open-branch `E_00` residual is now an executable envelope:

```text
nabla^2 Phi_N = 4*pi*G_cal*rho_H + (c^2/2)E_00
mu_obs = G_cal*M_H^dress + (c^2/(8*pi))*int_W E_00 dV + residuals.
```

## MHdress / GM Comparator Rows

| row_id | quantity | formula_or_value | status |
| --- | --- | --- | --- |
| GM4777_0_primary_mass_definition | M_H^dress | M_H^dress[W_H;tau] := H_tau[S_link;tau,e_obs] - H_ref[Sigma_ref;tau,e_obs] | PRIMARY_MTS_SOURCE_MASS_DEFINITION_NO_NUMERIC_ROW_YET |
| GM4777_1_observed_mu_sun | mu_sun_nominal | 1.3271244e+20 | SOURCE_BACKED_OBSERVED_GM_COMPARATOR |
| GM4777_2_mass_comparator_from_mu | M_GM_sun_cal := mu_sun_nominal/G_cal | 1.988409870698051e+30 | SOURCE_BACKED_COMPARATOR_ONLY_NOT_MHDRESS_DEFINITION |
| GM4777_3_mass_residual | Delta_MH_sun | (M_H^dress - M_GM_sun_cal)/M_GM_sun_cal | COMPARATOR_RESIDUAL_READY_VALUE_MISSING |
| GM4777_4_uncertainty_policy | sigma_mu_and_sigma_M | sigma_mu_nominal=0.0; sigma_M_from_G=4.468805426856864e+25 | UNCERTAINTY_POLICY_READY |

## E00 Poisson Envelope

| row_id | quantity | formula_or_bound | status |
| --- | --- | --- | --- |
| E004777_0_poisson_residual | E_00 | nabla^2 Phi_N = 4*pi*G_cal*rho_H + (c^2/2)E_00 | DERIVED_FROM_4719 |
| E004777_1_integrated_mu_shift | Delta_mu_E00 | Delta_mu_E00 = (c^2/(8*pi))*int_W E_00 dV | EXECUTABLE_ENVELOPE_DERIVED_VALUES_MISSING |
| E004777_2_observed_mu_balance | mu_obs_balance | mu_obs = G_cal*M_H^dress + Delta_mu_E00 + Delta_mu_boundary + Delta_mu_profile + Delta_mu_readout | BALANCE_LAW_DERIVED_NONCLAIM |
| E004777_3_relative_envelope | eta_E00_abs | eta_E00_abs <= c^2*int_W \|E_00\| dV/(8*pi*mu_ref) | BOUND_FORM_READY_VALUES_MISSING |
| E004777_4_spherical_sup_bound | E00_sup_sphere_required | if \|E_00\|<=E00_sup on radius R, then eta_E00_abs <= c^2*E00_sup*R^3/(6*mu_ref) | SPHERICAL_ENVELOPE_READY_R_TOLERANCE_MISSING |

## Open Newton / Orbital Score Status

| status_id | object | status | score_effect |
| --- | --- | --- | --- |
| OSS4777_0_Gcal | G_cal/kappa_eff | FILLED_4776 | SI normalization ready |
| OSS4777_1_mu_comparator | solar GM comparator | FILLED_SOURCE_BACKED_COMPARATOR | can compare against M_H^dress once M_H^dress exists |
| OSS4777_2_MHdress | M_H^dress numeric/source functional | MISSING_PRIMARY_MTS_MASS_VALUE | blocks Newton/orbital pass |
| OSS4777_3_E00 | E_00 bound/input | BOUND_FORM_READY_VALUE_MISSING | blocks open Poisson residual pass |
| OSS4777_4_product_gate | open Newton/orbital score | BLOCKED_UNTIL_MHDRESS_AND_E00_FILLED_OR_ZEROED | no empirical claim |

## Anti-Circularity Audit

| audit_id | rule | status |
| --- | --- | --- |
| AC4777_0_no_GM_definition | M_GM_sun_cal=mu_sun/G_cal is a comparator only; M_H^dress remains H_tau-H_ref. | PASS_COMPARATOR_ONLY |
| AC4777_1_G_uncertainty | Solar nominal GM is exact as a conversion constant, but converting it to kg inherits CODATA G uncertainty. | PASS_UNCERTAINTY_ATTACHED |
| AC4777_2_E00_not_zeroed | E_00 is not set to zero in open arenas; it is integrated into Delta_mu_E00. | PASS_OPEN_RESIDUAL_RETAINED |
| AC4777_3_boundary_profile_readout | Boundary, profile and readout residuals remain separate from E_00 and from M_H^dress. | PASS_NO_CANCELLATION |

## Unit Contract

| unit_id | object | unit_check | status |
| --- | --- | --- | --- |
| UC4777_0_mu | mu_obs and G_cal*M_H^dress | G_cal*M has m^3 kg^-1 s^-2 * kg = m^3 s^-2 | UNITS_PASS |
| UC4777_1_E00_integral | Delta_mu_E00=(c^2/(8*pi))*int E_00 dV | c^2 * (m^-2*m^3) = m^3 s^-2 | UNITS_PASS |
| UC4777_2_eta | eta_E00_abs | Delta_mu_E00/mu_ref is dimensionless | UNITS_PASS |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4777_0_MHdress_runner | Hamiltonian mass source-functional runner | SELECTED_NEXT |
| RT4777_1_E00_input | E_00 support/radius/tolerance input row | SELECTED_NEXT_PARALLEL |
| RT4777_2_boundary_profile | boundary/profile/readout residual ledger | QUEUED |

## Decision

`MHDRESS_ORBITAL_GM_COMPARATOR_ROW_AND_E00_POISSON_ENVELOPE_DERIVED_OBSERVED_GM_IS_COMPARATOR_NOT_DEFINITION_MHDRESS_NUMERIC_AND_E00_VALUES_STILL_OPEN_NONCLAIM`

## Next Target

`4778-Y5-R2FR-Hamiltonian-mass-source-functional-runner-or-E00-bound-input.md`
