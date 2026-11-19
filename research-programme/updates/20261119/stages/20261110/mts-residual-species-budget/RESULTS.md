# Remaining metric budget: derived and independently reproduced

2026-11-10, private retained-framework checkpoint. Previous stage:
`mts-source-complete-radiation-20261110`, seal
`0a86b2f000bc55519d823f60034a8a204d81117184468cab04f689398e670197`.
All original/corrected fine trajectories are reused. No new evolution,
native build, production background, physical grid, coefficient or fit.

## What changed scientifically

The remaining error is no longer an unattributed consistency residual.
Its dominant source is derived from the existing massive-neutrino sector:

    K_nu=kz [S_background-(4/3)sum native_density_weights].

The same mismatch occurs in the cold baseline and in MTS. It is a mismatch
between finite numerical representations of standard thermal-neutrino
stress, not a newly proposed physical non-conservation law or MTS coupling.

Seven budget/node/constraint identities are verified algebraically. The
neutrino formula predicts the independently evaluated source residual with
maximum relative error 7.06e-11 across the 72 case/mode/time evaluations.
The zero-mismatch ablation does not predict the nonzero residual. The native
source coefficients and monopole/dipole equations are checked directly.

## Paired evidence

The background and perturbation enthalpies differ fractionally by about
-1.0415655e-5 at the first probe, nearly identically in both backgrounds.
Analytic differentiation of the source weights leaves this defect intact;
it is not an artifact of the prior 16/32 finite-difference stencil.

| Corrected case | Max absolute neutrino budget | Max stencil-minus-analytic budget | Signed fraction of sampled metric residual |
|---|---:|---:|---:|
| Cold | 9.6533973e-14 | 5.10e-24 | 0.99817 to 1.00163 |
| Native heavy | 5.8460817e-15 | 4.48e-25 | 0.99593 to 1.00214 |
| Canonical D0 | 5.8460817e-15 | 4.48e-25 | 0.99592 to 1.00220 |
| Canonical D01 | 5.8460817e-15 | 4.48e-25 | 0.99592 to 1.00220 |

Budgets use 8 pi G a^2-scaled stress per conformal time (Mpc^-3).
The last column compares `-K_nu/(2k^2)` with the independently differentiated
metric residual. It is a signed attribution, not a probability or a positive
partition; values slightly above one reflect other signed contributions and
derivative errors. It is not a claim that every remaining term is neutrino.

Before the previous source repair, this contribution was only about 0.0103%
of the heavy metric residual; the missing scalar radiation source dominated.
This confirms that we are not recycling the old explanation for a new error.

The slow-field synchronous budget is below about 4.9e-28 at these probes.
Baryon pressure contributes at most 3.01e-19 in cold and 2.45e-20 in heavy.
Finite-difference CDM/baryon budgets are larger than their analytic tiny
budgets. The latter involve severe cancellation; their tiny-budget-relative
prediction errors can reach 8.05e-4. They are not silently treated as exact
numerical passes. Their equation-level identities remain explicit, and they
do not explain the dominant 1e-13/1e-15 neutrino budget.

## The first simpler explanation failed; the full one was tested

The continuous Fermi-Dirac background and perturbation integrals agree to
about 3.5e-16 relative in the reference calculation. But the five-node rule
alone explains only about 1.12e-6 fractional error, not the full 1.04e-5.
`continuum-reference.json` keeps that failed comparison; it was not weakened.

We then reproduced the native background's own 100-step momentum integral
and 1400-point table interpolation. It matches the extracted native
background to at most 1.75e-14 relative. Its error is about -9.30e-6 relative
to the continuum reference. Together with the five-node perturbation error,
this predicts the full enthalpy mismatch to at most 1.69e-9 relative accuracy.

At the cold initial probe, the independent background sequence is:

| Diagnostic steps | Enthalpy minus continuum reference |
|---:|---:|
| 100 | -9.6617747e-5 |
| 200 | -6.0225183e-6 |
| 400 | -3.7622251e-7 |
| 800 | -2.3575298e-8 |

These enthalpies are normalized to the native massless reference, not the
physical source units of the earlier table. The derived lower-endpoint
expansion predicts the 100-step error successively to 0.356%, 3.47e-5 and
1.29e-6 relative accuracy at orders h^4, h^6 and h^8. No coefficient is fitted.
The production grid/background and all trajectories remain untouched.

An earlier reader attempt also failed because it interpreted unsuffixed
Fortran constants as double rather than REAL32 literals promoted to double.
Its receipt is retained; the corrected reader passes the unchanged common-
mass check. See CONTINUUM-LITERAL-REPAIR.md. This coding repair and the later
rejected physical subhypothesis are distinguished in the validation ledger.

## Reproducibility and implications

- `species-budget.json`: all seven species, both gauges and 144 original/
  corrected case/time/stencil comparisons.
- `neutrino-prediction-result.json`: frozen node prediction and analytic
  derivatives; `metric-source-budget.csv`: the measured metric attribution.
- `continuum-reference.json`: failed five-node-only explanation plus passing
  continuous-integral identity. Do not relabel its overall flag as passing.
- `background-reference-result.json`: actual native background reproduction,
  diagnostic refinement and derived endpoint coefficients.
- `constraint-bound.json` and DERIVATION.md connect the intrinsic source
  budget to the metric defect without imposing conservation as an axiom.
- 88 validation checks pass; these include provenance, compilation and
  preserved negative results, not 88 separate physics discoveries.

This removes a specific ambiguity about the paired consistency floor. It
does not improve an observational likelihood or choose a galactic wave
population. No old result, Galaxy file, public repository or other worker
was changed. Read NEXT.md for the bounded continuation; do not rerun the
completed evolutions or keep halving the same derivative stencil.
