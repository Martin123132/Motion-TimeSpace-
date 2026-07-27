# 4776 — Gcal Normalization or Open-Arena First-Value Pack

Generated: `2026-07-08T03:53:25+00:00`

## Result

4776 fills the first open-arena value from 4775:

```text
G_cal/kappa_eff normalization = FILLED_SOURCE_BACKED_CALIBRATION_ROW
kappa_cal := 8*pi*G_N/c^4 = 2.076647442844972e-43 m J^-1
sigma(kappa_cal) = 4.667112902128249e-48 m J^-1
```

This is calibration, not derivation:

```text
G_cal = G_N(CODATA/NIST) for SI comparison.
MTS does not yet predict the numerical value of G_N.
```

## Constants Provenance

| constant_id | symbol | value | standard_uncertainty | units | source_basis |
| --- | --- | --- | --- | --- | --- |
| CONST4776_0_c | c | 299792458 | 0 | m s^-1 | NIST/CODATA 2022; exact SI defining constant |
| CONST4776_1_GN | G_N | 6.67430000e-11 | 1.50000000e-15 | m^3 kg^-1 s^-2 | NIST/CODATA 2022 recommended value; calibration datum only |
| CONST4776_2_CODATA_schedule | CODATA_cycle | 2022 adjustment current; 2026 adjustment closes 2026-12-31 and results expected 2027 | not_applicable | metadata | CODATA TGFC states 2026 adjustment closing date and 2022 as last regular adjustment |

## Kappa / Gcal Normalization

| norm_id | quantity | formula | value | status |
| --- | --- | --- | --- | --- |
| KG4776_0_definition | kappa_cal | kappa_cal := 8*pi*G_N/c^4 | 2.076647442844972e-43 | SOURCE_BACKED_CALIBRATION_ROW |
| KG4776_1_inverse | G_cal | G_cal := c^4*kappa_eff/(8*pi); calibration sets kappa_eff=kappa_cal for SI comparisons | 6.67430000e-11 | SOURCE_BACKED_CALIBRATION_ROW_NOT_PREDICTION |
| KG4776_2_field_equation | local SI field equation | G_mu_nu + Lambda_eff g_mu_nu = kappa_cal T_H_mu_nu + E_fail_mu_nu | ready_for_units_calibrated_private/open comparisons | UNIT_NORMALIZATION_READY_NONCLAIM |

## Open-Arena First-Value Status

| value_id | quantity | status_before | status_after | claim_effect |
| --- | --- | --- | --- | --- |
| FV4776_0_Gcal | G_cal/kappa_eff normalization | MISSING_CALIBRATION_SOURCE_ROW | FILLED_SOURCE_BACKED_CALIBRATION_ROW | enables SI comparison; does not predict G_N |
| FV4776_1_MH_dress | M_H^dress | MISSING_SOURCE_BACKED_MASS_ROW | STILL_OPEN_NEXT_TARGET | blocks orbital/Newton real-arena scoring |
| FV4776_2_E00 | E_00 residual | MISSING_OPEN_ARENA_E00_BOUND | STILL_OPEN_NEXT_TARGET | blocks quantitative Poisson residual pass/fail |
| FV4776_3_boundary_flux | F_boundary/Poynting/radiation flux | MISSING_BOUNDARY_FLUX_LEDGER | STILL_OPEN | blocks open EM/Poynting local claims |
| FV4776_4_PPN_transfer | Pi_PPN residual transfer matrix | MISSING_PPN_TRANSFER_MATRIX | STILL_OPEN | blocks open PPN empirical scoring |
| FV4776_5_R10_alpha | alpha(lambda) local fifth-force row | MISSING_R10_NUMERIC_ROW | STILL_OPEN | blocks R10 claim |
| FV4776_6_orbital_profile | orbital profile/multipole residual | MISSING_ORBITAL_PROFILE_ROW | STILL_OPEN | blocks real orbital branch scoring |

## Unit Contract

| unit_id | equation_or_object | unit_statement | status |
| --- | --- | --- | --- |
| UC4776_0_curvature | G_mu_nu + Lambda_eff g_mu_nu | m^-2 | UNITS_PASS |
| UC4776_1_Poisson | nabla^2 Phi_N = 4*pi*G_cal*rho_H | s^-2 on both sides when Phi_N has m^2 s^-2 and rho_H has kg m^-3 | UNITS_PASS |
| UC4776_2_orbit | a_r=-G_cal*M_H^dress/r^2 | m s^-2 | UNITS_PASS |

## No-Circularity Audit

| audit_id | rule | status |
| --- | --- | --- |
| NC4776_0_calibration_not_prediction | Using CODATA G_N fills a calibration boundary condition; it is not a derivation of G_N from MTS. | PASS_FIREWALL |
| NC4776_1_GR_same_status | kappa_cal makes the private/effective branch comparable in SI units; it does not promote B_GR to a public parent selector. | PASS_SCOPE_LOCK |
| NC4776_2_open_values_still_open | M_H^dress, E_00, boundary flux, PPN transfer, R10 and orbital profile are not silently filled by the G calibration row. | PASS_OPEN_GATES_RETAINED |

## Route Selection

| route_id | route | selection_status |
| --- | --- | --- |
| RT4776_0_MHdress_E00 | M_H^dress comparator and E_00 open-arena bound pack | SELECTED_NEXT |
| RT4776_1_boundary_flux | Poynting/boundary flux ledger | QUEUED |
| RT4776_2_PPN_R10 | PPN transfer and R10 alpha row | QUEUED |

## Decision

`GCAL_KAPPA_CODATA_CALIBRATION_ROW_SOURCE_BACKED_KAPPA_EFF_DERIVED_FROM_G_AND_C_MHDRESS_E00_BOUNDARY_PPN_R10_ORBITAL_VALUES_STILL_OPEN_NONCLAIM`

## Next Target

`4777-Y5-R2FR-MHdress-comparator-and-E00-open-arena-bound-pack.md`
