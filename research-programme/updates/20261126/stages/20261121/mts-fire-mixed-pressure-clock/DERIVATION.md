> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# One gas field, three different gravitational questions

Start from the retained [reciprocal wave–matter pilot](../mts-fire-live-poisson-feedback/RESULTS.md) and its adiabatic energy variation (not bundled here). The relative launch acceleration is the difference of the two original wave accelerations \(a=-\nabla(\Phi_{\rm coupled}-\Phi_{\rm reset})\); the two individual accelerations are also evaluated separately. Deformation is \(X=x+s a\), \(s=t^2/2\), at this order. The angular/radial coordinates and temperatures here come from a simulation, not from measurements of Galactic clocks. No wave mass, occupation, observer, time step, metric coupling or measured rotation speed was adjusted.

## Pressure moving ordinary mass: fourth derivative of the clock

[Machine-specific or private operational passage omitted.]

Independent force form: \(\partial_j(pB_{ij})=\gamma p\,\partial_i D+B_{ij}\partial_jp\), since the tide is a Hessian. Integrate this against \(\nabla K\), with the actual radial and angular faces of the represented pressure. The exterior face of the truncated raw-cell control is part of that mathematical model, not a measured physical vacuum interface. For constant pressure and homogeneous dilation of a ball, a probe monopole strictly inside has zero regular bulk; its exact sheet equals the independent surface traction at the outer material surface. This fixes the sign directly.

## Resolving a probe without inferring a gas law from the answer

The native gas records supply positions, energy, mass and **full support radius** \(h\). They do not supply a unique continuum pressure interpolation. Use positive normalized 3D cubic spline and Wendland C2 as alternatives; neither is an assertion that meshless finite-mass hydro applied these pressure forces. For an isotropic cloud at \(r_i,\mu_i\), its shell moment per unit mass is
\[
 p^2\int W_i(|p\hat n-x_i|)P_l(\mu)\,d\Omega
 ={2\pi p\over r_i}P_l(\mu_i)\int_{|p-r_i|}^{\min(h_i,p+r_i)}
 sW_i(s)P_l\!\left(1-{s^2-(p-r_i)^2\over 2pr_i}\right)ds .
\]
This azimuthal addition theorem replaces a noisy shell finite difference. A separate direct azimuth integral at the observer gives the infinite-angular-resolution **sheet alone**. Keep the original cap for the whole clock; do not splice that isolated limit onto a finite-cap bulk integral. The bulk uses stratified kernel-radius quadrature and antithetic angles; four common-seed replicates, the two arms and a finer numerical field interpolation are stored separately. Seed spans are not confidence limits on the gas physics.

## Why a reweighted source cannot just inherit an autonomous scalar pressure

An effective material can be assigned \(p_{\rm eff}\propto\sum_i w_i m_i u_i W_i\). A different model transports the *launch* weight \(w(x_0)\) on the underlying gas and tests its actual acceleration. For the latter, the mixed material virtual work tests \(w\nabla K\), not \(\nabla K\) on a separately compressed effective gas. In smooth regions with \(p_{\rm eff}=wp\) their difference is \(-\int p\,\nabla w\cdot B\nabla K\). In a cell reconstruction two fields may jump at the same face, so the value assigned to their product matters. The smooth-force implementation instead integrates the original \(W_i,\nabla W_i\) pressure force with \(w(x_0)-w_i\), retaining even raw clouds with exterior centres if they overlap the tagged aperture.

There is a sharper test, independent of the fourth-order clock. In the Newtonian gas rest frame, to have **both** the original acceleration and an independently closed scalar pressure for density \(w\rho\) requires \(dp_{\rm eff}=w\,dp\), hence \(dw\wedge dp=0\) and zero circulation on every contractible loop. A rectangular loop crossing one radial label face, with points A,B on that face, has exact circulation \((w_+-w_-)(p_B-p_A)\) with the recorded orientation. Evaluate all six path segments and the jump formula independently. Radial faces are the nearest to the two already fixed probe radii, and A,B lie at one-quarter and three-quarters of their observer angular bin, with no selection on the pressure. The two tested reconstructions violate the necessary condition. This rejects **that specific scalar shortcut** for these inputs; it does not reject gravity, pressurelessness of collisionless stars, or the wave equation.

In signature \((-+++)\), units \(c=1\), \(T^{\mu\nu}=(e+p)u^\mu u^\nu+p g^{\mu\nu}\). For \(\nabla_\mu T^{\mu\nu}=0,\ u^\mu\nabla_\mu w=0\),
\[
 \nabla_\mu(wT^{\mu\nu})=p\,h^{\nu\mu}\nabla_\mu w,\qquad h^{\mu\nu}=g^{\mu\nu}+u^\mu u^\nu .
\]
It is a spatial pressure traction, not a newly fitted interaction. For a true split \(f,1-f\) these exchange currents cancel pointwise; if the full stress exchanges with its surroundings there is also \(fQ^\nu\). Heat flux, anisotropic stress, mass creation or changing labels require their own contributions. The actual empirical transport weights exceed one in some cells: the algebraic complement is then not everywhere positive. Rescaling by the maximum is a useful positive conservation control, **not** an unchanged normalization or a physical prescription. A statistical tracer is allowed such weights. Interpreting its stress as the whole independently conserved Einstein source is the additional assumption that fails.

## Internal energy gravitating: a separate second derivative

The retained scalar normal constraint (not bundled here) needs the ordinary densitized energy as well as the leading Newtonian mass. At matched initial specific energy the heat term has no initial arm contrast. At fixed entropy \(u(X)=u_0 J^{1-\gamma}\); \(J=1+sD+O(s^2)\). The isolated \(dm\,u/c^2\) contribution for test function \(F\) therefore gives
\[
  M''_{\rm heat}[F]=\int {dm\,u_0\over c^2}
                [a\cdot\nabla F-(\gamma-1)FD].
\]
Using \(F=1_{r<p}\) gives the **negative outward energy flux** through the surface plus integrated compression work inside. With energy in (km/s)², use \(c\) in km/s, not the pressure-work time conversion. Spherically averaged inward radial acceleration in the outward-positive coordinate is \(-GM(<p)/p^2\). Use the retained three radii and their fixed compensating weights, which annihilate \(1/r^2\) and \(r\), giving a coefficient in m/s²/Myr². The subtraction is performed on the same represented or raw gas in both arms. Scalar isotropic pressure has no comoving trace-free stress; this heat source enters the spatial constraint and, holding the other terms in the slip fixed, its particular contribution is common to the two scalar forces. This is **not** replacing the lapse source by \(\rho+3p/c^2\). Bulk velocity stress, the ordinary kinetic-energy change, wave/metric product terms, dissipation and boundary work are not set by this heat term.

The volume estimate is calculated separately for the cell model and the two cloud models. In the latter, integrate the intersection of each normalized cloud with a sphere exactly to quadrature precision for its centre-value tidal trace, then sample only the small variation of the trace within the cloud. Integrate the surface flux by the shell-moment identity above, including the midpoint. The uniform-ball check \(M_{\rm heat}(<p,s)/M_0=(1+s\lambda)^{-3\gamma}\) tests the relative flux/work signs; all three physical shell rows and the compensated sum are retained.
