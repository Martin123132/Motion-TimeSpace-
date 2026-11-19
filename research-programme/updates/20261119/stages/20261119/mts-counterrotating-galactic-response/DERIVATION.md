# What changes when equal numbers rotate in opposite directions?
The parent Schrödinger–Poisson limit, ordinary potential, outward-vacuum Poisson matching and kinetic coefficient are the same as in the preceding stage. In its units write the common Hamiltonian as \(H=T+U+P[\rho]\), where \(P\) is the linear attractive Poisson map. Let \(u\) and \(v_\pm=v(r,\theta)e^{\pm i\phi}\) be normalized in the inherited volume measure, with squared norms \(N\), not one. The mixture has density \((1-f)|u|^2+f|v|^2\) and opposite currents of identical magnitude. Their azimuthal stress is proportional to \(f|v|^2/(r\sin\theta)^2\), not zero. Orthogonality under azimuthal integration alone would not cancel interference in the *local* density of a coherent superposition; this calculation requires an incoherent, number-diagonal occupation. The azimuthal kinetic term is in the full harmonic eigenvalue, not added again as an effective force.

On the saved ground potential we diagonalize \(H\) in the mirror-even \(|m|=1\) sector. The angular functions are \(\sqrt{(2\ell+1)/[\ell(\ell+1)]}\,P_\ell^1(\cos\theta)\), odd degrees \(\ell=1,3,\ldots\), orthonormal on the northern half in \(d\cos\theta\); the southern half is its reflection. The radial functions are the normalized spherical Bessel modes of those same degrees. This enforces regularity on the axis and at the origin. The excited density uses **ordinary even Legendre** multipoles for its gravitational potential; the density is not itself an \(m=1\) source.

## The derivative with no new force parameter

Write \(s=\sqrt{1-f}\,u_f\), so \(\|s\|^2=(1-f)N\); at \(f=0\), \(s=u\). Normalize both counter-rotating representatives to \(N\), with equal weights \(f/2\). A dot denotes differentiation at zero transfer. The change of source and its ground-state equation are
\[
 \dot\rho=2u\dot s+|v_0|^2,\qquad
 (H_0-\epsilon_0)\dot s+uP[2u\dot s]=\dot\epsilon\,u-uP[|v_0|^2],
 \quad 2\langle u,\dot s\rangle=-N .
\]
There is no missing term involving \(\dot v\): its density is multiplied by \(f\). Split \(\dot s=-u/2+w\), project the linear equation on \(u^\perp\), and solve for \(w\) with the inherited constrained Hessian. That yields the force response including both the direct population swap and gravitational relaxation of the remaining ground population. It is not a sum of two fixed halo templates.

To retain the original circular speed at its one calibration radius let \(d_N\) be the ground-only solution differentiated in \(\ln N\). With \(g_A\) the inward force there, the implicit mass response is \(\nu=-\partial_f g_A/\partial_{\ln N}g_A\); add \(\nu\,\partial_{\ln N}\) to every fixed-number derivative. Thus this comparison does not pick a second free amplitude from the polar or quasar data. The fixed-number ensemble does not receive this adjustment.

## Independent finite test

At each specified positive fraction, solve the ground eigenproblem with the excited self-gravity as an external potential, then rediagonalize the excited sector in the complete potential including ground and excited gravity, until the excited vector no longer changes. Ground gravity is recomputed at every step. When required, update the total norm until the total outer acceleration reproduces the saved one-point calibration. For each readout calculate the forward secants at \(h,h/2,h/4\); their combination \((D_h-6D_{h/2}+8D_{h/4})/3\) removes the first two truncation terms without evaluating an unphysical negative occupation. This tests the tangent of the discretized branch; changing the angular/radial basis independently tests resolution. The field is nonrelativistic and stationary here; neither linear response nor existence of these solutions proves formation, coherent preparation, dynamical stability, or relativistic continuation.
