> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Relativistic matter rates, the origin, and the clock test

The instantaneous Einstein constraints test spatial consistency. A second question is whether the *same matter* transports the reconstructed metric correctly in time. The stored snapshots, initial gauges and conserved rest measures are kept fixed; none of the measured rates sets a coefficient.

## Massive geodesics on this metric

With canonical covariant radial momentum p per unit rest mass and conformal time η, minimal metric coupling gives the Hamiltonian

    H_particle = a exp(U) γ,        γ²=1+exp(2V)p²/a².

The two Hamilton equations are

    X_η = exp(U+2V)p/(aγ),
    p_η = −a exp(U)[γ U_X + exp(2V)p² V_X/(a²γ)].

The gradients know the orientation of the signed stream coordinate X. At leading order these are p/a and −a∂_X φ_Newton. They are not an extra force, a best-fit clock factor or a speed-independent displacement. At fixed initial labels one can forecast the change in the rate of the *Newtonian part* of the potential span before evolving. If δv is the first equation minus p/a, its contribution is −a²/2 ∫ Σ(8πG D₀) δv_out dr over the two radii. This uses the signed radial speed of each stream and the geometric shell theorem. It does not purport to be the change in the rate of every relativistic stress term.

[Instantaneous positive/negative trajectory tests](evidence-001.zip) (archive member: `material.py`) separately substitute the corrected speed, and the corrected speed plus momentum equation, on both sides of the initial slice. They also test sensitivity to how an exactly equivalent initial continuous mass element is divided into labels. Pointwise force evaluation only at the ends of a highly folded mass element is not generally an energy-consistent discrete rule. For the live test, vary the *material-element Hamiltonian* with its original mass weighting. If L_i are linear label shapes, M_ij=∫L_iL_j dM, then

    M X_η = ∫ L ∂H_particle/∂p dM,       M p_η = −∫ L ∂H_particle/∂X dM.

The same consistent mass matrix occurs on both sides of the canonical pairing ∫p X_η dM. The control projects the Newtonian generator by the same rule. The [projection](evidence-001.zip) (archive member: `galerkin.py`) splits integrals across folds and metric cells, preserves endpoint conditions and tests the positive mass recovered for each input element. The live solver recomputes both constraints and the shear-preserving lapse at each midpoint. The streams inside the regularized core still do not constitute a separately evolved isotropic 3D core distribution; the claim is an exterior short-time test.

## The wave origin is not an independent amplitude

The represented wave is u=rψ=r+Σ b_k sin(k r). Independent endpoint data are u(0)=0 and the retained exterior value. The smooth limit is ψ(0)=1+Σ k b_k. In a kicked sine-grid code the phase applied to a stored ψ(0) need not equal the limit reconstructed from the nonzero sine samples after that kick. The difference has no mass in the original quadrature, whose volume weight vanishes at zero. Interpolating that number as if it were an extra measured wave datum spreads it over a nonzero volume. The first evolution step can then appear to change the exterior gravitational mass instantly. We retained the initial failing periodic-time tests and corrected only this representation in the separately named regular-origin history series. No previous research file was changed.

There is a different finite-grid effect: multiplication by a potential at native sine nodes followed by interpolation is not pointwise multiplication off-grid. [The generator check](evidence-001.zip) (archive member: `wave_generator.py`) integrates 2 Re(u* u_η) against the analytic, constant-interior shell readout, with separate free and potential generators. Integration by parts matches the free drift to the two-radius current independently. The potential kick would be *pure phase everywhere* in the continuum; its projected density-rate residual is measured, not set to zero. The higher grids sample the same saved initial wave, not new formation data.

## Which wave equations actually follow from the scalar action?

For two phase quadratures of the real field define z,w as in [the stress derivation](DERIVATION.md) and P=b⁶w. Strip a carrier phase exp(−im t) and the homogeneous amplitude a⁻³ᐟ². With N=exp(U), normal expansion h, and dη=dt/a, the canonical Klein–Gordon equations on this metric are

    z_η = (3aH/2 + i a m) z − i a m N P/b⁶,
    P_η = (−3aH/2 + i a m) P − i a m N b⁶ z
          + i N b²/(a m) [z_rr + (2/r+2b_r/b+U_r) z_r].

The time derivative of b⁶ cancels the normal-frame scalar damping term using h=(H−∂t V)/N. Thus both equations use the same lapse and spatial metric. For q=Re(z*P), the two mass terms and background dilution cancel out of the Wronskian balance,

    ∂η(r² q) = −∂r [ r² N b² Im(z*∂r z)/(a m) ].

For the balanced initial lift this current is the saved Schrödinger current times exp(U+2V). This is the same metric factor in the massive geodesic speed; the gamma factor belongs to particles using canonical covariant momentum, not to this wave Wronskian. A phase-pair Wronskian conserved by the quadratic equations is not proof of a fundamental U(1) charge for a single real scalar. The [canonical flux check](evidence-001.zip) (archive member: `canonical_wave.py`) evaluates the unsimplified two time derivatives on the reconstructed state and independently evaluates currents at shell faces. A nonrelativistic complex envelope is not an exact relativistic positive-frequency preparation merely because the flux closes; see also [Namjoo, Guth & Kaiser](https://arxiv.org/abs/1712.00445). Reimposing z=w on every successive slice would discard a canonical degree of freedom. Evolving z and P through a finite interval is distinct from the instantaneous check.

## Light paths on the reconstructed histories

The held comoving ends of each shell transmit identical clock frequencies to one receiver at their midpoint. For the exact scalar metric of this calculation the inverse radial null speed is f=exp(−U−V). Integrate backwards from a single reception event over comoving distance s: dη/ds=−f, with the high and low rays following opposite radii. Write δ=η−(η_o−s) and J=∂η/∂η_o. Then δ'=−expm1(−U−V) and (ln J)'=f(U_η+V_η). For each emitter ν_o/ν_e=(a_e/a_o) exp(U_e−U_o) J. Common receiver factors cancel. We integrate the light-time shift instead of subtracting two near-identical large travel times. The remaining expansion difference is evaluated over the very small differential emission interval at its midpoint. The static expanding analytic control, uniform moving potential control, and direct difference of two neighbouring pulse emission times test this computation.

The retained original Newtonian matter is sampled over 0.084 comoving Mpc of conformal time on the interior side of each saved epoch. Every sampled slice is solved again, rather than promoting one instantaneous potential difference to a frequency shift. Compares (i) both potentials replaced by the Newtonian solution, (ii) both replaced by the reconstructed spatial potential, and (iii) separately reconstructed lapse and spatial potentials; the worldlines and ray solver are identical in all three. The records separate the effect of changing the spatial metric from the lapse–spatial difference. Holding the comoving clocks in place excludes peculiar Doppler effects. These are synthetic frequency differences and matching diagnostics, not detections.

