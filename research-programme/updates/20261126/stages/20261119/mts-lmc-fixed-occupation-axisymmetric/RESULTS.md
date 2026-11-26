# The LMC drives inward redistribution, not the missing inner polar force
19 November 2026 · Local fixed-occupation calculation · No parameters fitted

We propagated the vertically even, axisymmetric response of both saved Schrödinger–Poisson grounds through all six previously archived [Vasiliev MW–LMC simulations](https://zenodo.org/records/8015660). These are alternative histories, not six independent measurements or a confidence interval. The primary calculation starts with no added perturbation at the first archived epoch; it does not identify a galaxy’s formation occupation. The comparison retains the earlier direct satellite field, lowest live m=2 wave and the original signed force bands. No new fit, changed tolerance or new data. Static NFW receives the same direct tide and has no wave response; it is not a live collisionless-wake simulation.

## What the sky test says

At z=+1.5 kpc, the table gives the range over the two backgrounds and six histories. Negative radial is inward. All accelerations, including the observing intervals, are in 10⁻¹⁰ m/s².

| R (kpc) | Component | Added m=0 acceleration | Combined MTS prediction | Original band |
|---:|---|---:|---:|---:|
| 6 | radial | −0.01314 to −0.00645 | −1.71306 to −1.67357 | −2.55240 to −2.23033 |
| 6 | polar | −0.000558 to −0.000235 | 0.42315 to 0.45351 | 0.57340 to 0.76899 |
| 8.3 | radial | −0.01348 to −0.00663 | −1.62077 to −1.58771 | −2.19995 to −1.95934 |
| 8.3 | polar | −0.000520 to −0.000241 | 0.25041 to 0.25739 | 0.23752 to 0.36475 |

The southern probes are evaluated against **their own** original intervals. The added radial force there is equal and the added polar force opposite; the previous direct-field subtotal is not reflected. At 6 kpc the response supplies **1.08–2.44%** of the missing radial force across both hemispheres; at 8.3 it supplies **1.47–3.77%**. Both models remain outside both radial bands and the inner polar bands; both stay inside the outer polar bands. All 192 primary component comparisons, including controls, are in final-force-comparison.csv.

## Where the effect comes from

- The first-order induced density is twice the product of ground amplitude and real wave displacement. Orthogonality to the ground conserves total number but not enclosed number. The LMC adds **1.67–3.48 × 10⁸ solar masses of wave density inside the 6.185-kpc sphere** through the inner probe; equal mass leaves its exterior. For the 8.434-kpc sphere the increase is 3.16–6.59 × 10⁸ solar masses. This is signed redistribution at the present epoch, not mass delivered by the LMC. Global linear occupation changes by less than 3.0 × 10⁻¹⁸ of the ground; continuity assessed using an independent surface current agrees within 1.47 × 10⁻⁶ relative.
- The induced spherical density accounts for most of the additional inward gravity but contributes **zero** polar force. For the northern inner polar force, quadrupolar *incident potential* supplies −0.000601 to −0.000273; the spherical incident potential on the already flattened ground supplies a smaller positive term. Source-split and density-split tables explicitly distinguish these two decompositions.
- A sequence of static equilibria would get the **opposite present polar sign**: +0.000147 to +0.000273 at the inner north probe. In the evolved response the last ~122 Myr contribute −0.00224 to −0.00167 there, outweighing +0.00132 to +0.00177 from the preceding ~367 Myr. These are signed contributions to the present amplitude, not incremental particle masses or additive energies. Starting in equilibrium with its initial derivative instead of starting at rest retains the negative sign. The positive static derivative itself agrees with independent nonlinear stationary solutions for L2M10 on both foregrounds (largest derivative mismatch 7.94 × 10⁻⁹); the sign reversal is dynamical.

## Could a different axisymmetric shape at the same excitation energy work?

Not on the tested linearized backgrounds. Instead of multiplying the predicted profile by an arbitrary factor, we allowed **any** fixed-number displacement on the full spatial discretization and minimized its quadratic energy subject to all the force bands. For each orbit/foreground, compare that least energy with the actual energy in the LMC-driven axisymmetric wave, including its velocity. Matching the signed north and south requirements takes **353–813 times the driven energy** (65–156 times the driven squared wave norm). Even allowing an unrestricted reflection-odd field to repair the north/south differences for free leaves a requirement of **334–777 times** the driven energy (unrounded 334.41–777.47). The field reconstructed from the minimizing dual weights realizes the bound in this linear system; the numerical bordered-inertia check yields exactly one constraint-negative pivot on both foregrounds, on both domain sizes. The ratios are essentially unchanged in the larger box (353.24–812.76 for the unrelaxed energy test).

This compares quadratic perturbation energies **at the final epoch**, not the total mechanical energy of the orbit or a bound on energy in other azimuthal modes. The minimizing field is a diagnostic, not a prepared MTS state. Fixed occupation here means fixed to first order about the specified ground; this is not a nonlinear time-dependent galaxy calculation.

## Numerical scope and restart

Same original source histories and bands. Finer source radius, angular projection and time controls change the enriched force by at most 1.31 × 10⁻⁷, 3.9 × 10⁻¹¹ and 4.23 × 10⁻⁶ relative respectively. Increasing the force-enriched wave basis changes it by at most 5.86 × 10⁻⁷. The coarser four-substep time check (1.87 × 10⁻⁴) and plain unenriched/medium-bank comparison (up to 0.285%) are not counted as meeting 2 × 10⁻⁵. Increasing the outer boundary from 30 to 40 ground lengths changes the small polar force by up to **0.2264%**, radial by up to 0.0094%; the largest absolute force change across either component is 9.44 × 10⁻⁷ in table units. This does **not** establish infinite-domain convergence to the inherited relative tolerance. It changes **none** of the tested band decisions. The post-400-kpc ground-weighted source omission in the wider test bounds the instantaneous driving-vector norm, not the error in propagated force.

DERIVATION.md gives the projected equations; REPLAY.md gives reproduction instructions. The states directory saves the actual density multipoles and time series. Results can be checked locally with python -B verify_axis.py after sealing. NEXT.md targets the remaining nonaxisymmetric response without counting the previously evolved m=2 component twice.
