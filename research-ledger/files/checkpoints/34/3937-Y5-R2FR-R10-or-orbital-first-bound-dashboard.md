# 3937 - R10 or Orbital First Bound Dashboard

Timestamp: `2026-07-01T12:14:09+00:00`

## Result

Built the route-choice dashboard between `R10/Yukawa` and `orbital/ephemeris`.

The selected first route is `orbital/ephemeris`, not because R10 is unimportant, but because orbital scoring tests the core reduction:

`parent source -> weak-field Poisson -> Gauss monopole -> slow-orbit measured GM -> Newtonian inverse-square residual`.

That is closer to the "does MTS really reduce to GR/Newton?" spine than an immediate alpha(lambda) fight.

## Orbital Dashboard

The new dashboard tracks:

- `epsilon_Delta_cal`: measured GM versus dressed Hilbert source.
- `epsilon_r(r)`: radial inverse-square hair that cannot be hidden in a constant GM calibration.
- `epsilon_Poisson_Gauss`: weak-field operator and Gauss surface consistency.
- `epsilon_orbit`: slow test-body readout.
- `delta_ln_mu_obs`: source/G drift and active-inertial source calibration.
- `Delta_PPN_orbital`: shared PPN/orbital residual vector.
- `alpha(lambda)_escape`: only sent to R10 if finite-range residuals survive.

## R10 Status

R10 remains queued, but not promoted:

- executable nonclaim score rows exist;
- full source-backed alpha(lambda) ownership is still missing;
- MTS alpha numerator/source/test/profile rows are still symbolic or blocked;
- no R10/local short-range claim is allowed from this checkpoint.

## Claim Gate

No public orbital, R10, local-GR, or Newtonian-reduction claim is made here. The private theorem branch is allowed to say "zero inside the branch"; every fallback row still needs source-backed numbers or parent-signed zero clauses.

## Source Register

- Source rows found: `16/16`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3937_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3937_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3937_R10_OR_ORBITAL_READINESS_COMPARISON.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3937_ORBITAL_EPHEMERIS_BOUND_DASHBOARD.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3937_R10_DEFERRED_QUEUE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3937_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3937_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3937_NEXT_TARGET.csv`

## Next Target

`3938-Y5-R2FR-orbital-ephemeris-source-acquisition-and-Delta-cal-score-runner.md`
