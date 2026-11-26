# Heavy-field energy and propagation of the gravity constraint, 89.65–90.4 Mpc

**The large heavy-energy term is real, but it is not by itself a missing force.** In the explicit field equations the direct lapse work cancels exactly. The remaining fast curvature work cancels again when paired with the heavy part of the gravitational constraint. Writing that balance before subtracting the two histories identifies a more specific question: **is it consistent to use the resolved wave’s quadratic current on the averaged branch?** This stage verifies the current on the resolved branch; it does not assume an answer on the averaged branch.

## Independent field test

We launched both heavy perturbations from 89.65 with their stored fields and conjugate momenta, using only the saved potentials, prescribed quadratic sources and background histories to drive them. No later field value, energy-rate measurement or phase alignment was used as a target in this solve. The differences in field and conjugate momentum at all fifteen later endpoints agree with the earlier calculation to better than 2.4e-8% of their respective difference scales on both gravity grids. This is an independent two-variable evolution conditioned on the saved metric, not an independent prediction of that metric.

| Joint visibility result | p16 | p32 |
|---|---:|---:|
| Frozen target: explicit heavy energy-rate difference, projected along full gap | +0.404436 | +0.404466 |
| Independent field-equation prediction | +0.404436 | +0.404461 |
| Error in predicted two-channel vector, % of the target’s own norm | 0.000061% | 0.007703% |
| Within independent prediction: direct different curvature histories | +0.419122 | +0.418993 |
| Within independent prediction: inherited perturbation difference at 89.65 | −0.000870 | −0.000864 |

Signed entries are percentage points on the *original small photon correction*. The direct curvature term is 6(am_h)² b v Φ; Ψ still drives f and w. The six driven responses sum to the independently evolved difference without a fitted phase, and halving the maximum step changes the reconstructed field difference by under 5e-8%. The energy-rate difference agrees pointwise with the previously saved rate to 0.035% on p16 and 0.054% on p32, worst at the last endpoint. Endpoint interpolation was not discarded.

## What survives in the full constraint

The heavy scalar contributes 3v²/2 to D, the coefficient multiplying Φ in the energy constraint. Its derivative carries a compensating term. PROPAGATION.md derives the resulting identity for R=Φ_E′−P_J. In this form the common curvature is eliminated with the energy constraint, leaving the geometric sources, metric slip, a background/current term and the component energy–momentum balances. The rapid direct curvature term is **not** an independent source to add back. Nor does the identity require each interacting component to conserve energy separately.

| Signed contributions to the density residual in the combined equation | p16 | p32 |
|---|---:|---:|
| Heavy prescribed quadratic current | +0.407138 | +0.407086 |
| Heavy background-table consistency terms | +0.057571 | +0.057622 |
| All heavy external inputs together, including the current above | +0.403012 | +0.402961 |
| Remaining non-heavy component exchange | +0.016138 | +0.016134 |
| Geometry sources, slip and Fq | +0.008538 | +0.008537 |
| Background combination times total current | −0.033219 | −0.033227 |
| **Net density residual from full constraint** | **+0.452054** | **+0.452041** |

Rows overlap where explicitly indicated; use propagation-scores.json for the complete additive breakdown. The companion’s own reduced exchange is below 2e-13% on the joint photon scale, **not** a statement that it can be removed from the evolution. The full constraint independently reproduces the prior density-residual photon vector within 0.00963% and 0.01520% of its own norm respectively; time-domain differences on the matched-minus-resolved residual are 0.102% and 0.154% or less. Adding back the unchanged incoming and other route terms gives **0.65971% and 0.65970%**. Reorganizing the equations explains the miss; it does not pass the 0.5% gate.

## A microscopic control and the next actual test

The quadratic current q_J is a contraction of the first-order field and its normal momentum, not a free coupling. We rebuilt it from the 782 resolved input wave numbers, and differentiated both legs using the native linear field equations. The rebuilt values reproduced the tabulated currents at all five output wave numbers; worst rate difference was **0.000217%** of the corresponding native derivative peak. No input mode failed the 0.5% field- or momentum-derivative check (worst 0.00124%). A sign error or poor differentiation of the *resolved* current is therefore an unlikely explanation for +0.407 on this interval. Although both branches use the same q_J, the constraint weights its value and derivative differently through H and D.

The post-switch averaged export has zero entries in both microscopic field columns at **all** 782 wave numbers. Those zeros mark the averaged representation; they are not physical empty-wave initial conditions. **Next:** carry the pre-switch microscopic perturbations through the matched metric, separately replay the resolved branch as a control, and build the matched q_J from those predicted modes. Before calling it the averaged branch’s current, compare the coarse-grained stress to the saved matched density, pressure and current. A failure there is evidence against that reconstruction, not permission to normalize it to the photons. The earlier first-order banks cover 83.15–89.65 and overlap the newer source inputs. No older checkpoint, fit, launch, data selection or GitHub repository was changed.
