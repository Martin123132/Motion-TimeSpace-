# Recovering the wave from two prepared moments

**For this single coherent heavy species with a specified homogeneous background and metric, the retained switch density and current determine both initial perturbation quadratures at every one of the 782 tested nonzero wavenumbers.** No stored perturbation field, later pressure, rotation-curve fit, phase adjustment or photon readout supplied an initial coefficient. The two moments themselves are established preparation inputs computed in earlier work, not newly derived cosmological initial conditions. This is a reconstruction on saved backgrounds, not an observational holdout or a theorem for all populations.

## The actual inverse

At η₀=88.4 conformal Mpc, write the unknowns as c=(f₀,w₀/M₀), M=am. Integrate two homogeneous unit solutions and the zero-initial solution driven by −vX. Project the three onto the saved density/current matching rule. This gives y=A c+h, where h is the particular solution and the current row is scaled by 2M*/k for the conditioning test. All 782 matrices have rank two; the largest condition number is **1.00399**, median **1.00209** (unscaled rows: 28.23–229.42). Worst amplification from subtracting the forced offset is 1.102 in the recorded norm. The Wronskian reproduces the expansion damping law to 4.35e−11 fraction. Changing the quadrature step or width, polynomial degree or sampling of the projection shifts the primary inferred state by less than 3.3e−8%. One row alone leaves an unconstrained quadrature. Zero wavenumber, vanishing background or an unspecified mixed state are not covered.

## Withheld pressure and the difference between two numerical conventions

The first, continuous-field inverse recovers the original initial state to **0.0000661%** or better on the two-quadrature norm. It also passes the inherited 2e−6 mode-normalized switch-pressure test for every mode. But **nine switch pressures fail 0.5% on pressure's own scale**. Applying the continuous solution at the exact source readout times alone does not fix this. The old native matching run used a tabulated homogeneous field and velocity, rather than a freshly integrated homogeneous oscillator, both to drive the perturbation and to form the stress. Pressure subtracts the kinetic and potential terms and is particularly sensitive near a zero.

| Switch construction | Worst relative pressure error | Modes missing 0.5% |
|---|---:|---:|
| Continuous inverse and continuous switch readout | 49.54% | 9 |
| Same state sampled at original source knots | 51.16% | 8 |
| Tabulated field and velocity in readout only | 0.09655% | 0 |
| Tabulated driving and readout, but retain continuous inverse seed | 1.143% | 1 |
| **Density/current inverse, driving and readout all in native preparation convention** | **0.000298%** | **0** |

The readout-only change was a diagnostic, not the adopted preparation. For the consistent last row the largest state error against the unused native launch is **0.0000522%**, the worst condition number is again 1.00399, and the maximum switch-pressure error is 3.89e−13 of the inherited mode norm. At k=1.4140559454 Mpc⁻¹ the native switch pressure is −1.09255946e−7; the consistent inverse predicts −1.09256271e−7. Direct replay of the original pressure samples reproduces their stored projection on all 782 rows. No velocity-zero division occurs in the inverse. This follow-up reuses the same previously exposed 782 modes; pressure never appears on its right-hand side.

## What reaches the gravity solver

On their own metrics, both continuously propagated reconstructions reproduce the earlier microscopic histories. For the initial continuous-map test, projected density, momentum and pressure of each microscopic replay are within 0.033% over the 31 supported late centers. The *old approximate fluid* still misses 43 pressures on their own scale: recovering its microscopic input does not silently modify its constitutive law. The previous stage tested a separate pressure correction. On the much smaller differences between projected branches, 24 density, 159 momentum and 11 pressure mode histories miss 0.5%; these stricter subtractions must not be reported as passing.

The native-prepared coefficients were then used on the actual continuous resolved and matched metrics, keeping the original mode pairs, metric coupling and 5 output probes. The signed field equation source, conjugate momentum source, energy, trace, current and shear have all been frozen together over 88.4–90.45 Mpc. From 89.65 to 90.4 the six resolved source controls agree with the native forcing bank to **0.000529% or better**, on their own peaks. The matched-minus-resolved quadratic current agrees with the earlier independently initialized conditional calculation within **0.0145% of that small difference itself**, and its rate within **0.00795%**. There is no independently exported post-switch matched microscopic field; that branch comparison is between two calculations, not a new observation. The initial shell phases and the homogeneous preparation are still input physics.

**Next:** use the consistently prepared heavy source bundle in the paired gravity/memory histories from the switch, rather than changing only the current on a later saved state. Preserve the pre-switch entry state and its averaging history, test the resolved control, evolve the two original gravity grids, and freeze photon energy and current before scoring the cumulative discrepancy. Check any contribution already supplied by the matched shear or pressure closure so it is not counted twice. No new photon prediction was scored in this stage; **0.65971% through 90.4** remains the cumulative reference on the original small photon correction, with the 0.5% gate unchanged.

## Reproducibility

PROTOCOL.md, SWITCH.md and NATIVE-MAP.md distinguish the initial prediction from the exposed follow-ups. inverse-freeze.json, forecast.json, switch-freeze.json, native-map-freeze.json and bundle-freeze.json identify the forecasts. Both metric source packets retain signed complex values, all five outputs and the current rate. mode-recovery.csv lists every mode, not just exceptions. The legacy loader needed a task-local module-name collision cleared after inversion; its numerical inverse was not repeated or changed. The irregular native layout ends before 90.45; the native-map replay requires only the switch projection's actual right wing and did not extrapolate across the later gap. The continuous later evolution uses its own full metric. No edits to older checkpoints, baseline banks or source data.
