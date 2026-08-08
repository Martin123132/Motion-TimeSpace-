# 3938 - Orbital Ephemeris Source Acquisition and Delta_cal Score Runner

Timestamp: `2026-07-01T12:22:00+00:00`

## Result

Built the first executable orbital/ephemeris source-acquisition and `Delta_cal` score runner.

This checkpoint does more than repeat that inputs are missing:

- imports source-backed comparator rows from `local_bound_claims.csv`;
- carries `R9_Gdot`, `R3_gamma`, `R4_beta`, `R5_alpha1`, `R6_alpha2`, `R7_alpha3`, and `R8_xi` into the orbital runner;
- preserves `R10` only as a finite-range escape lane;
- creates an absolute no-cancellation `Delta_cal_abs_envelope`;
- separates private-branch zero from fallback empirical scoring.

## Hard Score Contract

The fallback score is:

`Delta_cal_abs = |Delta_charge| + |Delta_Poisson| + |Delta_Gauss| + |Delta_orbit| + |mu_extra| + |Delta_G| + |Delta_flux| + |partial_r ln mu_obs| + |d ln G_eff/dt + d ln M_eff/dt| + |Delta_frame_species_range| + |Delta_PPN_source|`.

No fitted cancellation counts. A component either has a parent-signed zero, a numeric/source-backed bound, or it blocks the score.

## Current Verdict

- Private branch: `Delta_cal=0` remains a private conditional result.
- Fallback branch: blocked because MTS component amplitudes are not numeric/source-backed yet.
- Bound side: some comparator bounds now import cleanly.
- Claim side: no public Newton/orbital/local-GR claim.

## Source Register

- Source rows found: `15/15`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3938_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3938_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3938_ORBITAL_BOUND_IMPORTS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3938_ORBITAL_SOURCE_ACQUISITION_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3938_DELTA_CAL_SCORE_RUNNER.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3938_DELTA_CAL_COMPONENT_STATUS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3938_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3938_NEXT_TARGET.csv`

## Next Target

`3939-Y5-R2FR-parent-sign-or-bound-Delta-cal-components.md`
