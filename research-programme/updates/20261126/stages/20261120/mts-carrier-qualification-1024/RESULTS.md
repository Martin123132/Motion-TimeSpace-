> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A carrier-skipping step at q=1024: tide is not a proxy for every matter field

**Outcome.** On an explicitly off-phase short evolution (8¼ fast rotations), one large step agrees with 132 resolved steps to **1.119 ppm or better in every signed tidal readout**. The recovered angular matter-energy change agrees closely as well. However, the small spherically symmetric wave–cold energy contrast and constraint defects are appreciably resolution dependent even between resolved clocks. The skip is **not qualified for the full evolution**. This experiment is a simulation at fixed preparation, not another galaxy measurement.

## Same clock, different diagnostics

Six independently prepared q=1024 launches use the previous formation, branches and coupling. Twelve signed/zero, wave/dust and original/ADM trajectories were each integrated on five clocks directly from launch. Every clock lands off the initial carrier phase; no fine step is appended to manufacture the test time. All use the same 3 Mpc near domain and 160 cells per Mpc. The duration is 8.25/4096 of the full physical time. The four or eight short RK subdivisions in the *independent Newton evolution* give a matched normalizing tide at the actual clock time. Their largest difference is 0.000010 ppm of that tide. The predeclared launch-linear estimate of the scale differs by less than 1.8 ppm *of the scale*. No tolerance change.

| Worst absolute difference from 132 steps | 1 step | 4 steps | 33 steps | 66 steps |
|---|---:|---:|---:|---:|
| Signed proper-aperture tide, ppm of independent Newton change | 1.1185 | 0.5181 | 0.1795 | 0.0777 |
| Total signed energy, monopole RMS difference / reference RMS | 30.45% | 16.29% | 8.14% | 6.92% |
| Same energy comparison, quadrupole (ppm) | 0.739 | 0.547 | 0.181 | 0.132 |

Here “signed” is (wave host − wave zero) − (dust host − dust zero). The four proper tidal channels use the two widths and two readouts. Matter RMS is on grid radii 0.6–2.1 Mpc, not the same observer as the tidal detector. Each table entry is a maximum over the stated controls; the reference is the most resolved numerical history, not a postulated continuum solution. The 30.45% is of an exceptionally small *differential monopole increment* (~1.1 × 10⁻²⁸ in source units for the worst branch), not 30% of the energy or a measured galaxy discrepancy. Taking all energy differences at 46 decimal digits confirms the effect is in the saved field histories, not merely in the arithmetic used to score them. It does not isolate which evolution term causes it.

## Kinematic subtraction and constraint check

Write w for the complex log-envelope, z for the transformed velocity, K for the expansion trace and μ for the local inverse carrier length. In the rotating frame the normalized normal derivative is Π/μ = exp(w)[z + K/(2μ) − i]. The rest-subtracted excitation is exp(w)[z + K/(2μ)]. The common −i times the wave can dominate a comparison of the first quantity. The one-step vs 132-step host-minus-zero relative RMS errors are at most 1.49 × 10⁻¹² in the full normalized momentum but 1.87 × 10⁻⁴ in the rest-subtracted one. Cold dust has no complex phase; neither comparison invents one for it.

The normal-frame massive-wave energy minus its conserved-charge rest-energy density is algebraically

    E − E_charge = (ρ_h/2) exp(2 Re w) [ |z + K/(2μ)|² + exp(−2ℓ)|∂r w|²/μ² ].

This follows by completing the square in the two real normal quadratures; the charge term in these conventions is ρ_h exp(2 Re w)(1−Im z). These expressions use the retained monopole plus linear quadrupole algebra; they do not prove energy conservation over a finite domain. The code checks the energy identity for the saved increments. A 65-digit independent perturbation of both angular amplitudes checks the material-energy formula. Obtaining a tiny energy by subtracting large binary64 curvature terms lost precision on the nonzero-metric synthetic fixture: absolute discrepancy 2.64 × 10⁻¹⁷ before rounding the displayed number. We used a direct high-precision matter calculation for that fixture; the zero-metric-displacement H cross-check is retained.

The Hamiltonian and both momentum residuals were evaluated in ordinary arithmetic and again with 40 decimal digits, adding the geometric increments separately. H is reconstructed from the two independent curvature expressions and the momenta from geometry minus matter currents. A deliberately nonzero-constraint state checks their signs. After cancellation of the four members, both coarse and resolved time differences can be comparable to or larger than the small reference defects. The one-step largest interior RMS shifts were 1.09 × 10⁻¹⁹ (H), 2.47 × 10⁻²¹ (radial momentum constraint) and 4.58 × 10⁻²⁶ (polar momentum constraint), each in its native normalization. Neither the local constraint residual nor the microscopic velocity is assigned the tidal ppm threshold.

**Next numerical test:** on these same saved launches compare one evolved host-minus-zero increment against subtracting two independently evolved full histories. Evolve metric derivatives, homogeneous expansion and the heavy rest density in a representation that preserves the small signed increments, then rerun the same off-phase endpoint before extending the clock or increasing q. Do not infer the high-speed behavior from the short tide alone.

**LMC observational result stays separate.** The fixed-occupation density/force derivation and all eight original bands (not bundled here) and the independent density-to-force integral (not bundled here) remain authoritative. This experiment supplies neither a new LMC occupation nor new galaxy bands.

## Replay

Python 3.13 with NumPy, SciPy and mpmath and the sealed sibling folders. In this folder run with `python -B`: `local_case.py`, then `evolve.py original` and `evolve.py adm`, then `carrier_readings.py`, `matched_newton.py`, `excitation.py`, `constraint_floor.py`, `signed_energy.py`, and `verify.py`. The procedures protect old results and write only here; at most two one-thread numerical workers. All 60 trajectories' endpoint increments and the six launch banks are retained. See clock-by-clock tides (not bundled here), stable signed energies (not bundled here), excitation (not bundled here) and precise constraint comparisons (not bundled here).
