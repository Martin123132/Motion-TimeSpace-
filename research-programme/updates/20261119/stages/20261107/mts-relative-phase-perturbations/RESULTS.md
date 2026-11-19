# Relative-phase perturbations: saved local result

Completed 2026-11-07, continuing the retained MTS branch and its accepted
cold background. No new fit, replacement action or GitHub operation.

## What moves forward

The heavy scalar's exact density and relative-phase equations are now
explicit, with pressure, current and both metric injections retained.
Their leading homogeneous density equation contains the derived restoring
term k^4/(4a^2 m^2 H^2); it was not inserted as a dust approximation or
fitted coefficient. The mass and original action remain inherited inputs.

The rapid carrier can be separated by an explicit invertible coordinate
map. We bound its omitted homogeneous remainder AND the error from using
the saved mean background. A second, exact affine map retains the metric
source derivatives and endpoint shifts for the next coupled calculation.
See DERIVATION.md and relative_math.py / forced_map.py.

## Cold interval and unchanged gate

The parent-frozen interval is
a=[0.36273334952836184,0.46575884027469494], span 0.25 e-fold,
using its original 162 cold epochs. All three inherited comoving
wavenumbers and the 2e-5 numerical gate are unchanged.

| k (Mpc^-1) | Homogeneous phase bound | Background-replacement contribution | Combined bound |
|---|---:|---:|---:|
| 0.32497672865575244 | 1.230294804e-5 | 2.159607524e-6 | 1.446255556e-5 |
| 0.6499534573115049 | 3.109976184e-6 | 2.159607556e-6 | 5.269583740e-6 |
| 1.2999069146230098 | 8.118966913e-7 | 2.159615772e-6 | 2.971512463e-6 |

All three combined bounds pass. They bound the absolute Euclidean
operator error of the HOMOGENEOUS (delta,W) transfer, per unit initial
state, not fractional observational errors. They do not include arbitrary
metric forcing. The analytic inequalities use numerically qualified
parent endpoints, not formal directed-rounding interval arithmetic.

The baseline is its existing CDM block on its own saved background.
It has no heavy-scalar averaging uncertainty; ordinary solver/background
uncertainties are still present.

## Tests and cross-checks

- Ten exact symbolic identities: six relative-coordinate/readout identities
  and four affine metric-source identities.
- 147 resolved early coefficient states, seven identities per state:
  worst scaled residual 1.191681584e-11, below algebra gate 1e-10.
- 588 GR/spatial-Poisson linear-row fixture checks across both backgrounds:
  worst residual 4.280385558e-18. These are algebra fixtures, not data fits.
- 459 independent-phase reconstructions of the harmonic remainder:
  worst scaled residual 1.376426290e-21.
- Eighteen short prescribed-source integrations and eighteen cold free-block
  integrations: both models, three wavenumbers and all three inherited
  solver controls. Every run completes and passes unchanged gates.
- Original-canonical versus exact-affine evolution: worst scaled discrepancy
  1.074280390e-8; fine-run maximum 9.020510674e-11.
- Cold transfer refinement: maximum absolute entry difference
  1.258371185e-11. Liouville determinant identity, evaluated independently
  using H at the saved endpoints/epochs: maximum 1.258393389e-11.
- The baseline velocity law is checked independently. Zero heavy density
  correctly rejects the scalar relative coordinate.
- Omitting the source-derivative term leaves a nonzero matrix residual
  with norm 0.001087401087 on an early reference point. No smallness
  assumption hides this term.

The scaled discrepancy used in the early coefficient/evolution checks is
max |left-right|/(1+|left|+|right|), not a relative error near a zero crossing.
Cold transfer refinement and determinant errors above are absolute.

## What the baseline comparison says

For the same initial unit-density basis vector, the terminal MTS-minus-CDM
free-transfer entries (delta,W) are:

| Wavenumber label | Delta delta | Delta W |
|---|---:|---:|
| half | -4.817618748e-7 | 3.501972485e-6 |
| balanced | -7.708180712e-6 | 5.603142479e-5 |
| double | -1.233285148e-4 | 8.964682449e-4 |

These are mathematical transfer-basis differences, not fitted amplitudes
or observational detections. The half-case difference is smaller than
the conservative phase/background envelope; do not advertise it as a
resolved physical separation. The complete matrices and both controls
are in cold-transfer-01/result.json.

## Saved evidence and next step

- coefficient-01/result.json and coefficients.csv: inherited window,
  phase-uniform coefficient bounds and source hashes.
- cold-transfer-01/result.json and heavy/cold packets: free-block transfers,
  complete error budget and independent solver results.
- validation-01/result.json and packets: early same-source canonical versus
  affine comparisons, both metric-channel fixtures and zero-density check.
- audit-01/result.json: independent harmonic/determinant checks, input
  integrity, numerical summary and software versions.
- The historical unexecuted drafts remain in draft-at-resumption; the
  historical pause and launcher date-parsing diagnosis remain readable.
- closeout.json seals this stage after cleanup; CLEANUP.json records the
  exact owned worker identities and their exits.

Next: use the derived metric rows to transform the heavy scalar and the
other matter TOGETHER, retaining the quadrature enthalpy defect and physical
initial-mode projection. That turns this controlled free block into the
coupled GR/spatial-Poisson comparison on the same frozen cold interval.
No late microscopic phase, new observational fit or cosmological initial
mode was invented in this stage.
