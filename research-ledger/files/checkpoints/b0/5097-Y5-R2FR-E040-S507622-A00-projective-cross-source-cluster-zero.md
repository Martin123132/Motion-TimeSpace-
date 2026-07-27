# 5097 — E040/S507622/A00 projective cross-source cluster zero

## Result

The `E040__S507622_N0000__A00__coarse12` obstruction is residue-only. Its adaptive integral already satisfies `0.00048137016215086544 < 0.0005`; the gate fails because two pair-local probes attempt to resolve a residue of order `1e-7` by subtracting nearly cancelling contours.

The coincident labels are not a same-source pinch. Every pair joins `direct:g2:<factor>` to `subtraction:decay:<factor>`, which occur in separate additive summands of the finite-plus integrand.

## Exact kinematic identity

Let the soft fraction be `x`, `r=sqrt(1-x)`, and let `gamma`, `beta` be the recoil boost. For the second recoil daughter,

`E_2/r = gamma(1 + beta u)`

and its coefficient along the soft direction is

`(gamma-1)u + gamma beta`.

At

`u_* = -(1+gamma)/(gamma beta) = -gamma beta/(gamma-1)`,

the two expressions become `-1` and `0`. Hence

`p_g2(q_*) = -sqrt(1-x) p_decay(q_*)`.

The relative stereographic roots are the reciprocal, nonzero roots of

`a q^2 + (c_soft c_decay - u_*)q + a = 0`,

where `a=(sin(theta_soft) sin(theta_decay))/2`.

## Cauchy consequence

Projectively proportional null momenta have identical four factor roots. The four `g2/decay` coincidences therefore occur at the same relative root, but the factor poles within each additive source remain simple and mutually separated. A local residue of either additive summand is holomorphic through a collision with a pole belonging only to the other summand. Since `q_* != 0`,

`Res_q[(sum Res_z I)/q] = 0`.

This proves zero for the exact event, argument, projective root pair, source labels, and physical ownerships certified by 5097. It does not reinstate a broad cross-source theorem and is not physical evidence for MTS.

## Outputs

- `scripts/Y5_R2FR_5097_E040_S507622_A00_projective_cross_source_cluster_zero.py`
- `source-intake/functional_rg/5097/E040_S507622_A00_projective_cross_source_cluster_zero.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5097_VALIDATION.csv`
