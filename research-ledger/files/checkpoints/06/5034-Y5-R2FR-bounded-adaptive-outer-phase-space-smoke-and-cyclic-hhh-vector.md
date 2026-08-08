# 5034 — bounded adaptive outer phase-space smoke and cyclic `hhh` vector

## Exact outer measure

The normalized three-body variables used since checkpoint 5010 obey

```text
dmu = dx dOmega_s/(4 pi) dOmega_d/(4 pi)
    = dx (ds_z/2) (dd_z/2) dphi_g/(2 pi) dphi_r/(2 pi).
```

The fixed-event causal kernel computes both normalized azimuth contour
averages. With `s_z=2u_s-1` and `d_z=2u_d-1`, the remaining measure is exactly

```text
integral_[0,1]^3 du_x du_s du_d K(x,s_z,d_z).
```

There is no residual Jacobian and no fitted normalization. The direct cut is
`D_hhh/G^3=(-2/pi) E[K]`, exactly as in checkpoints 5017 and 5026.

## Sheet assignment

Each Sobol event and each direct/crossed argument is transported independently
from `z=0.3+i epsilon_0` along the canonical near-boundary Feynman homotopy to
`z_target+i 0.08`. Projective root tracking and
crossing-group consistency must pass before its kernel is evaluated. Topology
descriptors are audit labels only; no nearest representative and no
class-constant kernel approximation is used.

All arguments, including the five physical ones, remain on this common positive
regulator surface for the smoke. The rejected real-endpoint pilot put collision
poles directly on the terminal relative contour: it produced 12 topology
failures and three finite but unconverged kernels in 36 jobs. Moving to finite
positive epsilon is not a fit; it restores the contour definition. The
epsilon-to-zero limit remains a separate required calculation.

A raised-then-horizontal path is not substituted when the canonical path is
expensive. At the first Sobol event and `z=-3+0.08i`, both paths can be tracked,
but their net winding signatures differ. The runner therefore increases the
canonical Feynman discretization up to its declared bound instead of silently
changing sheets.

## Restart contract

Run `bounded_smoke_eps008_v2` writes an immutable `config.json`, atomic topology and
kernel files, one terminal JSON per job, `status.json`, `partial_results.json`,
and `log.txt`. It stops between complete kernels at the requested wall/job
boundary. Reusing the run id with a changed config is rejected by digest.

Current state: **COMPLETE_WITH_REPAIR**; terminal jobs
`36/36`; failures
`0`; unconverged finite jobs
`0`.

## Primary cyclic smoke

| z | cyclic D_hhh/G3 | computed nonlocal | fixed 5018 target | event triplets |
|---:|---:|---:|---:|---:|
| -0.6 | `187.20059-8.5522348i` | 125.74658 | 28.710948 | 2/2 |
| -0.3 | `73.631174-4.5728718i` | -13.748749 | -9.0094229 | 2/2 |
| 0 | `51.588107-4.0362784i` | -44.433786 | -20.453828 | 2/2 |
| 0.3 | `65.508951+15.037658i` | -21.870971 | -8.9409342 | 2/2 |
| 0.6 | `55.782011+0.83993771i` | -5.6720002 | 28.771322 | 2/2 |

The local `stu` projection is computed from the predicted cyclic vector alone.
The fixed 5018 target is loaded only afterward; `target_fitted=false`.

The predicted local coefficient is `96.0218929 +/- 20.4029052` across the two
independent scrambles. The nonlocal RMS difference from the fixed 5018 target
is `47.6800628`. The five computed-minus-target values are
`(97.0356,-4.73933,-23.9800,-12.9300,-34.4433)`, with corresponding
two-scramble standard errors `(27.3605,10.6973,13.9468,23.6646,43.2898)`.
These are variance diagnostics, not precision significances: two outer points
cannot establish convergence, and the finite `0.08` regulator leaves visible
imaginary and crossing-asymmetric components. The mismatch therefore selects
an epsilon and outer-scramble ladder; it is not yet an `hhh` or MTS rejection.

## Global-node audit

| z | paired tier relative difference |
|---:|---:|
| 0 | 2.205e-10 |

## Decision

The bounded smoke matrix completed. Its numerical vector is diagnostic only.

- Exact outer-measure reduction: **derived**.
- Eventwise projective Feynman classifier: **implemented**.
- Representative-class interpolation: **not used**.
- Finite-epsilon production precision: **not claimed**.
- Epsilon-to-zero limit, crossing-complete `hhh`, UV coefficient, local GR and full MTS: **open**.


## Extreme-argument repair

The sole terminal failure in the bounded matrix was the first scramble at
`z=-9+0.08i`. Its canonical Feynman root tracker had projective step `0.1312`
at the original 12288-step ceiling. The isolated repair changed no event,
target, contour, residue rule, quadrature tier, or normalization. It only
increased the same canonical path to `24576` steps,
where the maximum projective step is
`0.0684553`. The repaired
kernel is `45063.7809116-2113.19347698i`; its adaptive residual is
`2.69757e-11`. No raised-path result or
representative-class interpolation enters the merged vector.

Marker: `MTS_5034_BOUNDED_ADAPTIVE_OUTER_PHASE_SPACE_SMOKE`.
