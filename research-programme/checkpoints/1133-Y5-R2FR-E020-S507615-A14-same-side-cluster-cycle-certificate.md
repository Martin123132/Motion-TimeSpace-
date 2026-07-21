# 5117 - E020 S507615 A14 same-side cluster-cycle certificate

## Failure isolated

The first execution of `E020__S507615_N0000__A14__primary24` did not fail on
residue stability. It exhausted the unchanged adaptive integration cap with
`4108` composite intervals, relative error `2.1895202689681583`, and two
global pole models. Runtime was `6363.42 s`. Increasing the interval cap or
weakening the `5e-5` convergence gate was not authorized.

## Derived repair

Checkpoint 5095 already established the relevant Cauchy identity at `E040`:
for a finite cluster of correction poles with one common orientation, a
positively oriented disk containing that cluster and excluding every other
pole and the measure pole at zero equals the sum of the individual residues.

The identity is independent of epsilon. Its use remains locally guarded:

1. build connected components only from corrections with the same sign;
2. compute the component center and maximum root extent;
3. find the nearest excluded pole or zero;
4. require a contour radius strictly between the extent and excluded distance;
5. require isolation ratio below `0.1`; otherwise retain the individual route.

This changes numerical representation of an already-required residue sum. It
does not insert a closure term, delete a pole, or modify the contour class.

## Independent numerical gate

The exact E020 job was evaluated at 24 and 48 global-residue nodes with the
production profile, tolerance and interval cap unchanged.

| residue nodes | relative residual | clusters | maximum isolation ratio |
|---:|---:|---:|---:|
| 24 | `4.4382303458905644e-5` | 1472 | `0.010846102551545899` |
| 48 | `4.4333521326187423e-5` | 1472 | `0.010846102551545899` |

Both runs converge below `5e-5`; their final values agree to
`2.9371898151125674e-12` relative. No removable-collision fallback was used.
All thirteen validation checks pass.

## Production replay

The production runner now applies the cluster cycle only to the exact
certified E020 job, with the parent E040 scope unchanged. Replay converges in
`93.17 s`, using 74 intervals rather than exhausting 4108. The retained
highest-order value is
`-244488.52478604103 - 3760.5191204678063 i`.

This is a numerical contour certificate, not an MTS physics claim.

## Outputs

- `scripts/Y5_R2FR_5117_E020_S507615_A14_same_side_cluster_cycle_certificate.py`
- `source-intake/functional_rg/5117/E020_S507615_A14_same_side_cluster_cycle_certificate.json`
- `source-intake/functional_rg/5117/E020_S507615_A14_clustered_residue_nodes_24.json`
- `source-intake/functional_rg/5117/E020_S507615_A14_clustered_residue_nodes_48.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5117_VALIDATION.csv`
