> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The source map reverses a mass trend; one radial prediction survives the tested completions

**Private, 21 November 2026.** Shared launch at FIRE-2 m12i snapshot 590. Same retained/reset waves, fixed occupation, metric coupling, source bank, grids and historical tolerances. No new galaxy fit or data release. The new data are three snapshots of **one simulation**, not three Milky Way observations. [Equations](DERIVATION.md) · [Inputs and replay](REPLAY.md).

## 1. Locate the failure, not just its symptom

The gas-plus-star mass of the simulation inside 30.091 kpc is **increasing by 2.819 solar masses/year** on the unequal-spacing local estimate. The tapered component used to transfer its evolution onto Milky Way baryons instead **decreases by 30.852 solar masses/year**. This is not evidence for rapid Milky Way outflow. The old map weights changes by where the mass is, not by which mass moved. The mismatch is exact at the level of the retained groups:

- A single normalization equal to the terminal local-to-simulation mass ratio, 0.40777, would give **+1.149** solar masses/year. The contribution from the *differences* in the fixed group weights is **−32.001**, giving −30.852. The two largest negative contributions are from near-plane 6–8 and 8–10 kpc groups. This decomposition does not identify individual trajectories.
- The actual simulated exterior, 30.091–500 kpc, changes by **−0.445**, not the required **+30.852**. Appending it without modification leaves −31.297 solar masses/year. The adjacent left and right estimates for the hybrid itself are +0.992 and −34.037: the weighted central estimate is not an instantaneous measurement.
- A *conditional* completion balances each angular cone, allocating its required opposite rate by the measured exterior mass distribution at 590. The integrated mismatch is below 2e−14 solar masses/year. This constructs a mass-balanced **rate**, not a velocity field or an explanation of how the material gets there.

Mass budget (not bundled here) · 84-group breakdown per slope (not bundled here) · raw exterior and conditional completion (not bundled here).

## 2. Measure the shell flow where velocities actually exist

All four HDF5 pieces and both phases at 589/590/591 are accounted for. At 590, 1,932,242 particles lie in the saved guard aperture; 717,276 and 612,408 lie in the two original weighted shell halves. Relative to the archived source, the largest 590 group mass difference is 5.0e−12, and the field reproduction difference is 3.15e−13 relative. These are arithmetic controls, not independent galaxy evidence.

| Fine-grid mass-window cubic, solar masses/Myr³ | Inner half | Outer half |
|---|---:|---:|
| Raw FIRE measured current term, catalog-centred proper velocities | −516.59 | −526.70 |
| Raw FIRE remaining radial–angle term (part of previous line) | −0.434 | +1.552 |
| Raw FIRE instantaneous gradient part | −516.15 | −528.26 |
| Raw FIRE density-weight change over next 2.221 Myr | −3335.41 | −857.87 |
| Hybrid part determined by waves and adjacent density estimate | −158.35 | −730.41 |

The small raw residual is not imposed: gas/stars give −2.167/+1.733 and +2.299/−0.747 in the two halves. Changing from catalog bulk velocity to the three-epoch trajectory changes the joint residuals to −1.264/+3.211. The trajectory and catalog bulk differ by 11.35 km/s. Forward/backward drifts of the same particles reproduce the four joint instantaneous mass/force gradient moments to within **0.0145%** at the finer step. The actual adjacent density histories do *not* reproduce them with this accuracy. The left spacing is 22.210 Myr versus 2.221 Myr on the right; bulk-frame, evolving flow, particle mass and phase changes are distinct from numerical drift error.

Do not add the raw current to the hybrid table: it is not that source's current. Under the previous total-variation speed bound, canceling the two hybrid determined mass terms would require at least 21.34/74.22 km/s in radial motion; for the force readout the corresponding necessary speeds are 932/667 km/s. These are not measured velocities or sufficient conditions. The gas diagnostic tests the gravitational kernel; additional hydrodynamic response is not computed. Phase/centre comparison (not bundled here) · hybrid mass and gravity (not bundled here) · [particle drift](evidence-001.zip) (archive member: `particle-drift-64.csv`).

## 3. A cancellation the theory gives us

For the scalar moment of inertia divided by two, the entire unknown cubic current kernel is the gradient of a known scalar. **Any compact internal circulation drops out exactly.** We derived this before using the neighboring density histories and checked it on explicit non-spherical orbits, a closed circulating current, and a nonzero exterior flux. This replaces an arbitrary internal velocity profile by an independently testable density change and explicit source/boundary terms. It does not assert equilibrium.

At 388.41 kpc, the calculated interior contribution to the coupled-minus-reset curvature is **+5.334 million solar masses kpc²/Myr²**. Its cubic bulk term is **−39,058 solar masses kpc²/Myr³** on the centered history (wave −49,375; density +10,317). For the neighboring left/right estimates it is −49,726/−37,991. The centered coarse calculation gives −39,170 (0.29% difference); increasing volume quadrature order on the fine history changes the result by less than 1e−13 relative. These describe the derivatives of a contrast at launch, not a persistent expansion rate or a measured galaxy size.

The center-slope cone-balanced completion above changes the cubic density contribution by **+9.32**, or **0.024%** of the interior total. For the other explicitly tested reservoirs, even placing the entire balancing rate at 30–45 kpc changes the centered total by only 0.45–0.47%. These scenarios are not a confidence interval or a bound on every possible local exchange. Beyond the retained wave domain a spherical compensator drops out analytically at equal wave norm. For one-sign supply entirely outside that domain the general angular bound is 5.994e−10 kpc²/Myr² per unit of absolute mass rate (less than 0.019 solar masses kpc²/Myr³ for the centered compensation). Interior sources, mixed-sign turnover, nonmetric forces and different histories are not covered by that bound.

Virial integrals and weak checks (not bundled here) · conditional exterior sensitivities (not bundled here) · [explicit orbit and surface tests](evidence-001.zip) (archive member: `virial-analytic-controls.csv`) · validation (not bundled here).

**Next:** freeze the local mass weight onto the material at launch instead of reassigning it whenever mass crosses a group boundary. Start with saved stars and the existing 590 positions/velocities, then separate gas and stellar mass exchange. Compare its density slopes with the old snapshot-weighted map and its currents with the unchanged shell and virial controls. Report empty donor cells and keep the initial fine-scale density mismatch visible; do not refit the force or claim that FIRE's transport is the Milky Way's.
