# A tide at a specified release, not an instantaneous stream age

Each calculation uses the archived pericentre time, cluster velocity and position for that preparation and direction. Both ordinary-matter prescriptions start with exactly those coordinates and the same signed wave. This is a source replacement at the launch, not a new backwards reconstruction of a cluster orbit. Conditional source, no new calibration.

## What the ordinary source actually is

Apply the archived 581/600 and 586/600 FIRE mass ratios in cylindrical-angle/spherical-radius bins (specifically |z|/r and r) to the retained Milky Way stellar and gas source. Use its original 25–30 kpc taper and symmetric 160 kpc integration boundary, not a spherical point-mass approximation. Time interpolation of density is linear between these snapshots; Newton's force is linear in the density. The “native” comparator is the archived ordinary potential as used by the tracer, including its radial interpolation. The independent 581 mass check uses the exterior monopole of the saved potential. The 586 check uses the archived total transferred mass. The model is not a measurement of the historical Milky Way or of individual stellar escape dates.

Define T = a(X+s) − a(X) for each external source. Add the same full signed wave, the 590 mass-matched static wave monopole of that preparation, or neither. The opposite signed wave evaluated at the same coordinates is a diagnostic, not that rival orbit's independently determined pericentre. Computing the numerator and denominator of the source-to-sign ratio at identical coordinates isolates the force comparison from the release-date difference. A common source correction larger than a sign contrast is **not** a lower bound on the uncertainty of the sign contrast: much of that correction might cancel.

## Relative energy and position

Use a nonrotating frame translating with the cluster. With s the stellar offset, u its relative velocity and a_cl the cluster acceleration, E = |u|²/2 + Phi_cl(s), so E' = u·T. At release u is azimuthal and T meridional: E' vanishes for *all* the controls even with a time-dependent source. Differentiating once gives, in coherent units,

E'' = (T+a_cl)·T + u_phi [(V_phi+u_phi) a_R(star)/R_star − V_phi a_R(centre)/R_centre].

The last term comes from rotation of the two cylindrical radial unit vectors, not from an azimuthal force. The explicit time derivatives and meridional directional derivatives of the two force components are orthogonal to u at this instant. This is why the kinematic centred-difference check may freeze meridional components for this derivative only. The first nonzero work has coefficient E''/2, not E''. Forces in (km/s)²/kpc convert to kpc/Myr² by (1/977.7922216807892)².

For direct minus native ordinary gravity, D, matched initial wave and cluster states give delta s'' = D(star) − D(centre). The next derivative is the difference of material derivatives of D at the two positions: apply partial_t + v_R partial_R + v_z partial_z to each meridional component, then add the azimuthal term v_phi D_R/R. Initial changes of wave self-gravity and its first time derivative both vanish by identical initial wave density and current. Thus delta s = delta s'' t²/2 + delta s''' t³/6 + o(t³) for a smooth neighbourhood, including a live wave. This does not justify keeping the wave unchanged at later times.

At a fixed launch, take the signed-wave minus opposite-wave contrast of E'', then the direct-minus-native contrast of that difference. All terms linear in acceleration (the cluster and the turning terms) cancel. Only the cross term survives: 2 (T_direct_ord − T_native_ord)·(T_wave_signed − T_wave_opposite), times the squared unit conversion used above. This tests explicitly whether the relatively large common correction cancels from the small signature. It does not identify the cancellation over an entire orbit.

## How the same source starts changing the wave

For a matched Schrödinger–Poisson initial state the density and its first derivative match. Subtract the momentum equations: only the changed ordinary gravity remains in the initial derivative of the mass current. The kinetic/quantum stress and self-potential are identical initially. In the translating frame, delta j' = rho [D(x) − D(X)]. Continuity gives

delta rho'' / rho = 4 pi G (rho_direct − rho_native) − grad(log rho)·[D(x) − D(X)].

Positions are compared at the same offset in the two initially coincident, nonrotating frames. At the centre the current change is zero but its divergence need not vanish. A spatially uniform added acceleration drops out. We evaluate the value and spatial gradient of the actual separately back-evolved complex waves at the passage, not a ground-state surrogate. The Fourier/angular and radial shape coefficients retain their signed phase; only the 590 reverse initial condition used conjugation. Finite differences of the direct force test its divergence against the independent local positive density. The native density is obtained from the Laplacian of its actual represented potential, not the unprojected baryon mass. These are continuum initial derivatives evaluated on the represented wave; a finite-basis projected later solution need not preserve them on a 60 pc scale.

## What can the velocities measure?

For two independent velocity errors sigma_i and a frozen pair of Gaussian predictions with equal priors, optimal two-state accuracy is Phi(sqrt(sum[(delta_i/sigma_i)²])/2). The ambiguous-date comparison picks one admissible pair of opposite signs; it bounds uniform performance from above, without a probability distribution for escape dates. It does not estimate the population-average success rate. The typical-precision diagnostic uses each possible assignment of two *distinct* quoted uncertainties to the two mock stars; catalogue stars are not assumed to occupy these launch states. Removing an unknown common velocity zero point leaves the difference of the two velocities with variance sigma_1²+sigma_2². There is no measurement of a flow sign in these calculations.
