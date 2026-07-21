# 5146 E040/A10 conditioned-annulus global-cycle replay

## Result

The A10 ceiling was not an MTS-only failure and was not repaired by relaxing
the outer tolerance or interval cap. The second reciprocal chamber was feeding
the outer Gauss estimator an ill-conditioned inner Cauchy average. Its old
radius `0.2 rho_1` approached the Laurent origin closely enough that increasing
the outer interval count merely accumulated inner roundoff.

For every adjacent pair of finite pole moduli `rho_i < rho_(i+1)`, the
minimax representative is

`R_i = sqrt(rho_i rho_(i+1))`.

On each finite annulus,

`d(R)=min(log(R/rho_1), log(rho_2/R))`

has its unique maximum at `R_*`, where

`d(R_*) = 0.5 log(rho_2/rho_1)`.

The signed residue corrections preserve the requested fixed-ownership Cauchy
cycle when the representative radius moves across finite poles. Among annuli
whose log clearance satisfies the design error budget, the center nearest the
unit circle minimizes avoidable Laurent-origin/large-radius amplification. A
96/192-node ladder then tests the unmodelled prefactor directly. Therefore this
is a numerical representative change, not a change of pole ownership or of the
physical integrand.

## Locked replay

- inner-node ladder: `[96, 192]`
- ladder strict gates: `[True, True]`
- cross-node relative difference: `1.8245861794256666e-11`
- selected inner nodes: `192`
- run counts: `{'completed_converged': 51, 'completed_unconverged': 1, 'failed': 0, 'missing': 508}`
- first incomplete row: `E020__S512503_N0000__A10__primary24`
- validation failures: `[]`

No outer tolerance, outer interval cap, physics parameter, formal-workbench
file, or GitHub state changed. This checkpoint is numerical infrastructure and
does not by itself establish a UV, local-GR, or full-MTS claim.

The machine/cog criterion remains explicit: later physics acceptance requires
one parent mechanism that preserves local GR/Mercury behaviour while activating
the galactic sector without a hand-switched law.
