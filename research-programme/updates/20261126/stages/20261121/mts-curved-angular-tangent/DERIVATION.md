# First variation on nonzero curved monopoles

Use the actual retained common-metric quadrupole truncation: for any pair of spherical and angular coefficients a=(a₀,a₂), b=(b₀,b₂), multiplication keeps (a₀b₀,a₀b₂+a₂b₀); an analytic f contributes f′(a₀)a₂ in the angular slot. This is linear in the angular perturbations, **not** a linearization of the spherical gravity, expansion or matter histories. The same rule applies to the canonical heavy number/phase chart, dust, ordinary matter and surrounding stress. Spatial derivatives and the retarded time integrator preserve this linearity in exact arithmetic. The absolute host and its matched zero-environment reference have different spherical histories. Both spherical histories are evolved, not replaced by flat or frozen ones.

Let b denote their monopoles and let z denote the stored angular metric, extrinsic, matter and current increments on both members. Angular launch profiles (including analytic reference derivatives) are l, and the angular incident bank is e(t). On the retained branch,

    z′ = A[b(t)] z + B[b(t)] l + C[b(t)] e(t).

The fast linear generator in the wave chart is included by the original exponential integrator. For signed host-minus-reference coordinates, A is triangular: the shared state propagates with its own coefficients and the signed state also receives the difference of host and reference operators acting on the shared state. One cannot in general evolve the signed part on only one arbitrary monopole.

The implementation constructs the action of these three maps by homogeneity, not by subtracting two nearly equal complete solutions. For a free tangent, zero the *angular* launch profile, its spatial references and angular incident inputs. Keep both spherical launches and spherical incident columns. Evolve the angular state jointly with all its induced matter/current components. A known test pulse changes only angular chart slot 7 by −2A(r/w)⁴exp[−(r/w)²] at the saved time; it neither adds particles nor changes a coupling. Independent +A, −A and 2³²A runs test sign reversal and scale on the tangent equations (the last is an arithmetic control, not a physical source). Compare to **each** prior +/− perturbed curved trajectory minus its own native no-pulse control; do not rely only on their odd difference.

For the no-added-pulse run, propagate (i) the actual saved angular increment z at tick 960 with both angular forcing inputs zero, (ii) zero increment with the true launch and reference gradients, (iii) zero increment with the true time-dependent angular environmental drive. Every contribution uses the *same* full monopoles; each sees the same gravity–matter feedback operator. This separation is conditional on the epoch and chart, not a division of the Universe into independent species. Recombine the signed and shared angular states, restore the unchanged monopoles once, and evaluate the ordinary full-model geometry, material current, weak integral and proper apertures. Adding three full proper-distance readings would count the background three times. The untouched launch and external source still contribute to all full physical readouts. The gate compares the paired wave-minus-cold result to the original matched Newton plus propagating-stress prediction, at 20 ppm of the Newton scale.

## Independent continuum metric for the impulse

In flat, unit-lapse vacuum the linear spatial ADM equation is ḧᵢⱼ=Δhᵢⱼ+∂ᵢ∂ⱼ tr h−∂ᵢ∂ₖhₖⱼ−∂ⱼ∂ₖhₖᵢ. Start at h=0 with ḣ=V=−2K. In Fourier space resolve along n=k/|k|, Π=I−nnᵀ. The transverse block obeys the ordinary wave equation; the mixed longitudinal-transverse velocity is constant; ḧ_nn=−k²tr h_perp. Consequently:

    h(k,t)=t V + [sin(kt)/k−t] [ΠVΠ+nnᵀ tr(ΠVΠ)].

No scalar-only or traceless-transverse projection has been made. In coordinates x/w, the launch K/A is a Gaussian times the polynomial 2s²Q−2s[x(Qx)ᵀ+(Qx)xᵀ]+s(xᵀQx)I+(xᵀQx)xxᵀ, s=|x|², tr Q=0. Gaussian differentiation gives its transform after factoring out π^(3/2) exp(−k²/4):

    (3−2k²+k⁴/8)Q + (3/2−k²/8)[k(Qk)ᵀ+(Qk)kᵀ]
    + (−1+k²/16)(kᵀQk)I + (kᵀQk)kkᵀ/16.

Read off the two diagonal amplitudes, the cross amplitude and the angular trace-free amplitude by rotating Q relative to one radial sightline. Fourier differentiation gives independent field derivatives. The flat Hamiltonian coefficient for physical metric amplitudes L,b,v,d is

    H₂ = −4b″ + (4L′−12b′−12v′)/r + (16L+8b−24v+12d)/r².

It follows from δR=∂ᵢ∂ⱼhᵢⱼ−Δ tr h in the same chart. Compare against the separately derived scalar Hankel wave, the old constraint reader applied to exact metric samples, the old reader applied to the *evolved* flat grid metric, and the live curved/matter result. These distinguish analytic curvature, measurement stencil error, numerical field evolution and physical-background effects at the same radius. Probe the actual first cell as well as the inclusive inner norm; a good integral cannot certify a failed point. No new observational data or quantum-measure assumption.
