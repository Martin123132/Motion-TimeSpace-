> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A finite, on-shell stress source with exactly zero scalar-density contrast

The two columns in the [force experiment](SOURCE-NORMALIZATION.md) need not be independent. Is a source that changes the tensor tide but gives no differential Newton density artificial? Here is one **built from the ordinary Maxwell equations of the retained action**. Unlike an imposed mechanical stress this needs no arbitrary counter-source. Unlike the electric–magnetic dual test, the canonical stress is *not* identical. This is a second geometry, with its own cross-polarized detector, not a proposed correction to the two existing radial readings.

Use signature −+++, c=1, Heaviside–Lorentz electromagnetic units and the same κ=8πG as in the scalar tide. Work to leading weak gravity and quadratic order in the free field. In cylindrical coordinates (s,φ,z), choose a common length L, f=exp[−(s²+z²)/(2L²)]. Both initial magnetic fields vanish. Prepare the sum and the difference of two electric fields:

    E_a = A (s/L) f e_φ ,
    E_p = B [s z/L² e_s + (2−s²/L²) e_z] f .

The second shape is curl(s f e_φ); the first is toroidal and axisymmetric. Both satisfy the source-free Gauss constraint and have finite energy. A and B specify the prepared fields, not gravitational fit parameters. Under free Maxwell evolution the toroidal-electric family has poloidal magnetic field; the poloidal-electric family has toroidal magnetic field. The cross terms in squared electric and magnetic norms vanish separately **at every position and time**. Thus the two preparations have equal energy density everywhere, not merely equal integrated energy. Their momentum difference is toroidal; it has zero divergence. It need not vanish after launch. In Fourier language the scalar energy and longitudinal-current sources are both absent. The relative sign therefore changes no Newtonian density source.

At launch Δ denotes preparation (+) minus (−). Both momentum densities vanish and identical gravitational constraint data are allowed. The spatial stress in an orthonormal frame has

    ΔT_zφ = −2 A B (s/L)(2−s²/L²) f² .

It changes sign at s=√2 L. In leading Einstein gravity ΔR_zφ=κ ΔT_zφ: a cross-Ricci readout, not a trace of the radial force. To show this is not solely a vector or constraint effect, take a spatial Fourier mode along +x with transform exp(−ikx). The yz component is already transverse and trace-free. With F(k)=π^(3/2) L³ exp[−(kL)²/4], direct transformation gives

    ΔT̃_yz^TT(k,0) = i A B F(k) (kL)³/4 .

The toroidal and poloidal pulse energies at launch are E_a=π^(3/2)L³ A²/2 and E_p=5π^(3/2)L³ B²/4. The latter follows from integrating [s²z²/L⁴+(2−s²/L²)²]f². Thus for positive A,B the absolute launch source divided by √(E_a E_p) is √(8/5) (kL)³ exp[−(kL)²/4]/4. Relative orientation fixes the sign. Both pulse energies and one width suffice; a wave-specific gravitational coupling is neither measured nor inserted.

With equal, vanishing differential free tensor data the curvature responds immediately: Δḧ_yz^TT(k,0)=2κ ΔT̃_yz^TT(k,0). A density-only Newton forecast for this contrast is identically zero. The imaginary Fourier amplitude is the phase of a real spatially odd source. The k³ suppression and zero integrated shear are retained, not replaced by a uniform shear. It is a Fourier-resolved response; this is not a prediction for a radiative flux at a distant observatory.

**Beyond the initial instant.** The Fourier electric fields at wave vectors p and q=k−p evolve with cos(|p|t) and cos(|q|t); the magnetic fields grow with −i(p×E₀) sin(|p|t)/|p| and its q counterpart. Therefore each stress pair drives at frequencies |p|−|q| and |p|+|q|. For a cosine drive the retarded solution of h″+k²h=2κΠ gives the unit-source Green integral

    J(k,ω,t) = [cos(ωt)−cos(kt)]/(k²−ω²)
             = (t²/2) sinc[(k+ω)t/2] sinc[(k−ω)t/2],

where sinc(x)=sin(x)/x. This form is regular even for collinear, resonant momenta. The Gaussian convolution is centred at k/2. Verification (not bundled here) compares this propagating solution with direct causal integration over the time-dependent stress, two momentum quadratures, the analytic launch, a real-space launch derivative and free Maxwell fields away from the axis. Signs, initial data and units are fixed before any samples. No adjustable tensor normalization.

The corresponding observable is the spatial Fourier component of the TT-projected relative acceleration: −ΔR₀y₀z^TT = Δḧ_yz^TT/2 = κΔT̃_yz^TT−k²Δh_yz^TT/2. Two independent time-difference spacings on the retarded metric check this tidal readout, using the smooth even continuation at launch. An array resolving the mode is needed; a single point cannot perform a TT projection. The ±45° arms in the transverse plane give twice this cross tide on differencing. For the standard gravitational-wave framework see [Carroll, chapter on linearized gravity](https://arxiv.org/abs/gr-qc/9712019); the finite packet, its normalization and the causal convolution here are separate calculations.

This calculation uses the Einstein and minimal Maxwell terms. On a curved cosmological formation, with matter currents, incoming tensors, quantum matching or higher-order operators, extra terms can enter. The separately calculated [dual-packet difference](MAXWELL-DUAL-PACKET.md) is sensitive to the curvature–photon vertex in a different channel. Neither calculation assumes an observational measurement of either signal.
