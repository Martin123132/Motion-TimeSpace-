# 3737 - EM/Poynting Response Coefficients from Hodge/Maxwell

## Status
- `B_EM_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING`
- EM/Poynting `B_EM` entries now have Hodge/Maxwell coefficient formulas.
- `beta_EM` remains blocked because constitutive, field, marker, and tail norms are not source-owned.

## Coefficient Rows
- `BEM3737_0_poynting_chi` `BME3735_B3732_EM_poynting_chi`: Poynting theorem residual delta(partial_t u + div S) from constitutive/Hodge variation obeys ||y_poynting|| <= C_poynting_chi ||h_chi|| on fixed fields. -> `C_poynting_chi` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_FIELD_NORM`
- `BEM3737_1_poynting_current` `BME3735_B3732_EM_poynting_current`: delta(J dot E) gives ||y_poynting|| <= C_JdotE ||h_Jem|| with C_JdotE controlled by local electric-field/readout norm. -> `C_JdotE` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_E_FIELD_NORM`
- `BEM3737_2_stress_frame` `BME3735_B3732_EM_stress_frame`: metric/frame variation changes Maxwell stress and its divergence, so ||y_stress|| <= C_TEM_frame ||h_frame||. -> `C_TEM_frame` | status `DERIVED_SHAPE_COEFFICIENT_MISSING_STRESS_NORM`
- `BEM3737_3_wave_chi` `BME3735_B3732_EM_wave_chi`: linearized Maxwell wave operator in a constitutive medium gives ||y_wave|| <= C_wave_chi ||h_chi||. -> `C_wave_chi` | status `CONDITIONAL_MAXWELL_WAVE_FORMULA`
- `BEM3737_4_pol_chi` `BME3735_B3732_EM_pol_chi`: anisotropic or parity-odd pieces of h_chi project into polarization/birefringence residuals through C_birefringence. -> `C_birefringence` | status `CONDITIONAL_CONSTITUTIVE_POLARIZATION_FORMULA`
- `BEM3737_5_charge_marker` `BME3735_B3732_EM_charge_marker`: charge/fine-structure marker variation perturbs continuity/readout as ||y_charge|| <= C_charge_marker ||h_alpha||. -> `C_charge_marker` | status `BOUND_SCHEMA_READY_VALUES_MISSING`
- `BEM3737_6_tail` `BME3735_B3732_EM_tail`: retained EM boundary/non-Hilbert/material tails project into all EM observables through C_EM_tail_projection. -> `C_EM_tail_projection` | status `BOUND_SCHEMA_READY_VALUES_MISSING`

## Required Inputs
- `C_poynting_chi` = `MISSING_POYNTING_CHI_OPERATOR_NORM` | constitutive/Hodge perturbation to Poynting residual
- `C_JdotE` = `MISSING_J_DOT_E_OPERATOR_NORM` | source-current perturbation to Poynting residual
- `C_TEM_frame` = `MISSING_TEM_FRAME_OPERATOR_NORM` | metric/frame perturbation to Maxwell stress residual
- `C_wave_chi` = `MISSING_WAVE_CHI_OPERATOR_NORM` | constitutive perturbation to wave residual
- `C_birefringence` = `MISSING_BIREFRINGENCE_OPERATOR_NORM` | anisotropic Hodge perturbation to polarization residual
- `C_charge_marker` = `MISSING_CHARGE_MARKER_OPERATOR_NORM` | charge/fine-structure marker perturbation to continuity/readout residual
- `C_EM_tail_projection` = `MISSING_EM_TAIL_PROJECTION_NORM` | retained EM tail projection to observables

## Theorem Rows
- `THM3737_0_Poynting` `DERIVED_HODGE_MAXWELL_SHAPE`: Poynting theorem residual responds to constitutive/Hodge variation and source-current variation through C_poynting_chi and C_JdotE. | This derives the y_poynting rows from Hodge/Maxwell bookkeeping.
- `THM3737_1_Maxwell_stress` `DERIVED_STRESS_SHAPE`: Maxwell stress residual responds to frame/metric perturbation through C_TEM_frame. | This keeps EM stress tied to H^X rather than assumed Maxwell recovery.
- `THM3737_2_wave_polarization` `CONDITIONAL_CONSTITUTIVE_SHAPE`: Wave and polarization residuals are controlled by constitutive/Hodge perturbations, with birefringence separated from scalar wave-speed response. | This separates isotropic propagation shifts from anisotropic/polarization effects.
- `THM3737_3_charge_marker` `ANTI_OVERCLAIM`: Charge/fine-structure marker variation and EM tail terms are not killed by Maxwell identities; they need no-marker/no-tail theorems or finite bounds. | Prevents hiding charge/readout coupling or retained tail coupling in the EM sector.
- `THM3737_4_claim_gate` `ANTI_SMUGGLING`: B_EM shapes are sharper but not numeric/source-owned; beta_EM remains blocked in 3735. | Shape derivation is progress, not an EM/Maxwell pass.

## Decisions
- `DEC3737_0_progress` `B_EM_HODGE_MAXWELL_SHAPES_SHARPENED` | The EM/Poynting response matrix is no longer anonymous: Poynting, stress, wave, polarization, charge, and tail rows have Hodge/Maxwell formulas.
- `DEC3737_1_marker_tail_block` `CHARGE_MARKER_AND_EM_TAILS_REMAIN_EXPLICIT` | Maxwell identities do not prove away marker constants or hidden/tail terms.
- `DEC3737_2_next` `NEXT_ASSEMBLE_BETA_INTERFACE_OR_ATTACK_2PN` | Both B_NP and B_EM now have sharpened shapes; the next disciplined step is a beta assembly/interface ledger, then focused 2PN beta or numeric norm acquisition.

## Next Target
- `3738-Y5-R2FR-beta-assembly-interface-and-open-coefficient-ledger.md`
- Objective: combine sharpened `B_NP` and `B_EM` coefficient rows with 3735 beta contracts and emit the open-input ledger for beta assembly.
