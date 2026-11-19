# A genuinely different calculation from adding a pair of box modes
In a statistically isotropic volume with the retained primordial scalar spectrum, at linear order the two-sided physical velocity-space power is

    P_F,v(k_v) = Hc c A² e^(−2d) ∫[k_x,∞] (k dk/2π) P_R(k)
                  × [B D_b(k) + (k_x/k)² U_b(k)]² ,
    k_x = Hc c k_v,   B=2−0.7(γ−1)−(γ−1)d,   d=(k_v b₀/2)².

This follows by integrating over the two transverse wavevectors (k_perp dk_perp = k dk); Hc c converts the 1D comoving length into km/s. It is the linear counterpart of the synthetic sightline operator, not a nonlinear flux fit. The two-dimensional transverse phase-space measure is essential: the discrete-box percentage from adding a pair of vectors is not a continuum tail measurement.

At the actual z=4.2, k_v=0.0794328 s/km row, the directly sourced band 7.05231–7.79092 Mpc⁻¹ contributes **0.0071201 km/s** (MTS), **0.0172645 km/s** (same state made pressureless at z=99), and **2.58070 km/s** (all-cold), conditional on the chosen gas-heating and optical-depth history. Values interpolate the integrand between four source knots, not the microscopic transfer seeds. Trapezoid versus shape-preserving cubic differs by 0.080–0.087% here, not at the 2×10⁻⁵ standard. The three new midpoints are frozen in mapped-frozen-midpoint-kernels.csv; no direct parent evaluation there has been counted as a pass. At z=5.4 the radial minimum already equals the largest source knot: **no finite band is available**, not zero total absorption.

The tabulated upper-edge integrand per d ln k is still 0.0620, 0.1501, and 22.51 km/s respectively. Its value is not an extrapolation rule; the known finite-band power cannot give an upper bound on missing positive auto-power. A larger thermal width at fixed k_v damps the whole kernel and does not remove this transverse uncertainty. Extend the direct wave/cold source bank and look for convergence of cumulative integrals and their ratios separately; do not assume convergence of a ratio proves convergence of either power.

Only mapped-continuous-band.csv, mapped-continuous-integrand.csv and mapped-frozen-midpoint-kernels.csv are authoritative. The three REJECTED-unmapped files document an indexing error in the first summary: increasing k had been paired with a descending redshift array. The replacement joins against the saved survey rows and verifies k_x/(Hc c) against the original velocity bin. No box, energy, linear-transfer, primordial-mode or sightline calculation used the rejected summaries.

