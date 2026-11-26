# Frequency comparison at one receiver, not a potential interpreted as a clock

**Scope.** Use the leading weak-field scalar metric of the retained branch, in conformal Newtonian coordinates with c=1 and a common potential Ψ=Φ at this order. This is an explicit *conditional* optical readout. The calculation does not derive subleading gravitational slip, a photon mass, or a new light coupling. The clock worldlines are supported at fixed comoving radii, so there is no peculiar Doppler term. Different worldlines give a different observable.

Put identical ideal frequency standards at the two boundaries of each shell, and a receiver halfway between in comoving radius. The receiver compares the two incident frequencies at **one and the same proper-time event**. Positive Y means the outer transmitter is seen at higher frequency than the inner one. Both unperturbed paths have length d=(r_high−r_low)/2, so common expansion redshift, receiver clock rate, and the transformation of its chosen reception time cancel in the differential at first metric order. This geometry is designed to remove a common clock drift, not to model an existing observed pair of clocks.

## A frequency difference derived two ways

The radial line element is a²[−(1+2Ψ)dη²+(1−2Φ)dχ²]. Along a null ray |dχ/dη|=1+Ψ+Φ at first order. For fixed reception time η_o the emission time is η_e=η_o−d+∫(Ψ+Φ) ds, evaluated on the undeflected path at (η_o−d+s,χ(s)). Proper clock intervals obey dτ=a(1+Ψ)dη. Write Δ for high-path minus low-path and ℋ=aH for the conformal expansion rate at unperturbed emission. Taking the derivative of the emission time with respect to reception time, including the shift of the emission scale factor, gives

    Y = ΔΨ_e + ∫ Δ(Ψ'+Φ') ds + ℋ_e ∫ Δ(Ψ+Φ) ds.

The prime is a partial conformal-time derivative at fixed radius. The expansion term must not be dropped merely because both paths have equal unperturbed length. The receiver lapse cancels. A spatially uniform potential of arbitrary time dependence cancels identically between equal paths. We store all three terms, the signed emission-delay difference and their sum.

In the leading common-potential limit, integrate the time term by parts *along the ray*. The high path moves inward (dχ/ds=−1), the low outward (+1), and both finish at the same potential. This gives the independent force form

    Y = −ΔΨ_e + 2∫(∂χΨ_high + ∂χΨ_low) ds + 2ℋ_e∫ΔΨ ds.

The second implementation uses spatial forces without calculating a time derivative. A third check differences the emission-delay differences of two closely spaced receptions. For the analytic manufactured potential (p+qη)χ², with K=r_high²−r_low², both give Y=K[(p+qη_e)(1+ℋd)+qd+ℋ qd²/3]. Repeating after adding any spatially uniform term leaves Y unchanged. The controls also test a pure homogeneous field, which must vanish.

## Numerical and physical conventions

Use the folded positive streams, the compact wave kinetic energy, and both models' own self-consistent metric. After Δln a=0.004 evolve another 0.084 comoving Mpc of conformal time, storing 17 actual metric snapshots within a light crossing rather than taking a difference of sparse cosmological epochs. Set reception to 0.082 comoving Mpc of conformal time into this dense interval; d is 0.05, 0.075 or 0.05 Mpc. A common time-dependent offset is removed from each potential snapshot; it cancels in the differential. Reconstruct the retained piecewise-quadratic-in-radius metric, linearly in time; split each ray integral at every crossed temporal and spatial knot. Coarse sampling of these same snapshots tests temporal reconstruction, not an independent global time integrator. Opposite-pulse light metrics are evolved independently on the native grid. Compare four heavy meshes at common pulse *coefficient*, not at silently rescaled physical drive. The nominal speed names the original mesh's normalization of the test impulse. Report background and pulse-induced results separately.

This calculation concerns the differential part linear both in the scalar metric and, for the tangent packets, in the launched impulse. Higher metric orders, freely falling transmitter velocities, vector/tensor modes and the matter and gravity sources of slip have not been put into this signal. The observable is not the full clock response of a galaxy and is not evidence from observed clocks. Standard longitudinal-gauge conventions: [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072). For observable redshift including projected potentials see [Challinor & Lewis](https://arxiv.org/abs/1105.5292). The equal-arm setup, matter histories and numerical response here are local calculations.

