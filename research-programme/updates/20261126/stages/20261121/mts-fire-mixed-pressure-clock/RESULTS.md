> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What the gas does to the saved two-clock experiment

**Result.** Pressure in the simulated gas opposes a small part of the leading paired gas clock signal for both tested adiabatic indices and both reconstructions using the measured gas support. The pressure surface at the inner observer has the opposite sign to the uniform-bin estimate. Independently, a closed-path test rejects assigning a single autonomous scalar pressure to the reweighted gas while keeping the original gas acceleration. These questions are distinct from how the heat energy itself gravitates; that source is now evaluated separately.

All figures below are conditional on the retained FIRE-driven preparation, not observational bounds. “Paired” means coupled minus reset; “represented” means the saved positive template weighting, not all native gas. No new fit. [Mathematical derivation](DERIVATION.md) · [numerical replay](REPLAY.md).

## Pressure in the two-clock readout

Fourth derivatives in Myr⁻⁴ for represented gas, γ=5/3. At finite multipole cap 64 the two radial interfaces must be included.

| Paired model | Smooth volume | Inner surface | Outer surface | Total |
|---|---:|---:|---:|---:|
| Uniform physical volume in each original bin | +3.7101e−19 | −2.3289e−20 | −2.1422e−19 | +1.3349e−19 |
| Recorded support; cubic spline | +2.9842e−19 | +8.0493e−19 | −1.6295e−19 | +9.4040e−19 |
| Recorded support; Wendland C2 | +3.0428e−19 | +8.0648e−19 | −1.5722e−19 | +9.5354e−19 |

- **At 0.24 Myr:** the cubic term is +1.3000e−22 in the fractional clock rate, opposing 4.22e−8 of the leading **gas-only** paired term. This is a Taylor coefficient evaluated at the pilot duration, not another full hydrodynamic evolution. At γ=7/5 the cubic fourth derivative is +4.4958e−19. Raw gas in the aperture gives +2.6682e−18 at γ=5/3; it is not the represented source.
- **Individual controls:** reset −8.8876e−17 and coupled −8.7936e−17 (cubic, γ=5/3); subtracting recovers the independently evaluated +9.4040e−19. Four numerical angular replicates span +9.188 to +9.600e−19 in the weak paired estimate. A finer interpolation grid on the same first seed shifts it by +3.19e−22. Independent force projection gives +9.2022e−19; the difference is smaller than the empirical 3.87e−20 standard error of the paired strong-minus-weak numerical estimator. Four draws are not an uncertainty budget for gas physics.
- **Why the inner sign flips:** retaining the actual angles but the uniform radial bin still gives −1.46e−20. Replacing just the radial weights by the measured supports gives +8.23e−19; the full 3D result is +8.05e−19. The result comes primarily from which gas overlaps the probe, not from a new angular fit. Exactly 29,708 native supports intersect the inner sphere, 45,076 the outer. No exterior-centred cloud reaches either probe. Direct ring evaluation confirms positive inner and negative outer sheet terms for both shapes. The outer cubic cap-64 sheet is only 59.2% of the separate infinite-angular sheet; do not extrapolate the **total** without also resolving the regular term. Resolution and leverage (not bundled here).
- **Advection of a passive tag instead:** cubic paired total +8.851e−19; four-seed span [+7.437e−19,+1.012e−18]. This uses the full raw gas force on the original tagged support, including 25,708 buffered exterior centres. The raw uniform-bin symmetric-face value instead gives −3.721e−19; the range from allowable two-sided pressure traces spans both signs. A sharp cell label and a cell-integrated thermal reservoir alone do not determine that interface product.

Cell dual calculation (not bundled here) · [cloud estimates and numerical differences, all arms](evidence-001.zip) (archive member: `clock-summary.csv`) · surface decomposition (not bundled here) · [caps versus direct ring integration](evidence-001.zip) (archive member: `trace-angular-limit.csv`).

## The coupling test: identical acceleration is not free

For an independently conserved isotropic fluid to carry density \(w\rho\) but follow the raw pressure acceleration, the circulation of \(w\,dp\) must vanish on every closed path. On the two small loops around the original probe neighbourhoods the cubic-source circulations are **−43,271** and **+2,595** in solar masses (km/s)²/kpc³, i.e. −0.901% and +0.0218% of the sum of the absolute path contributions. The independent jump calculation agrees. The Wendland values are −49,152 and +3,371. These are deterministic failures of zero for the reconstructed sources, not statistical claims about a real galaxy. Complete path and source values (not bundled here).

Material conservation tells us what force is missing under the passive interpretation: **pressure traction \(p\nabla w\)**, with an opposite term in the complementary stress of a real subdivision. There is no free gravitational coupling in this identity. Rest-mass continuity for an advected label does not imply stress–energy conservation for its share in isolation. Here 3,142 of 356,864 aperture cells have \(w>1\); the maximum is 59.976. Those cells carry 58.56% of the represented gas mass and 73.93% of its internal energy. The excess gas mass in those cells alone is 4.6675e9 solar masses, even though the represented total is smaller than the original aperture gas mass. Thus \(1-w\) is not a physical positive second fluid everywhere. This is an obstruction to a specific interpretation of the reweighting, not evidence for extra galactic mass. Reservoir accounting (not bundled here).

## Heat as a source of the gravitational field

In the three-radius compensated gravitational force, the **paired second time derivative from the represented heat energy alone** is:

| Reconstruction, γ=5/3 | Surface transport | Interior adiabatic work | Sum (m/s²/Myr²) |
|---|---:|---:|---:|
| Uniform cell volume | −3.6865e−26 | +4.5448e−27 | −3.2320e−26 |
| Measured supports, cubic | −1.0937e−26 | +4.4367e−27 | −6.5007e−27 |
| Measured supports, Wendland | −1.0752e−26 | +4.4314e−27 | −6.3208e−27 |

The heat carried through the surfaces sets the sign in these preparations; compression offsets part of it. Refining the cloud integration and changing the angular draw gives a 0.11% change to the net cubic result. The individual cubic accelerations' second derivatives are +8.5563e−25 (reset) and +8.4913e−25 (coupled). Heat has zero initial arm contrast, so the leading difference due to this coefficient alone is the tabulated value times \(t^2/2\), not an acceleration jump at launch. [Both gas definitions and adiabatic indices](evidence-001.zip) (archive member: `normal-summary.csv`) · individual spheres and arms (not bundled here).

**Next decisive calculation:** propagate the *raw* gas momentum under the common gravity and pressure response with the label carried along, and measure its opposite interface traction on the same faces. Use a bounded split as a no-free-parameter conservation control; keep the actual overweight template a readout unless a positive physical redistribution and compensating stress are supplied. Compare to the separately pressurized effective gas at the same short times. That tests a source choice directly rather than adjusting a coefficient until the clocks agree.
