# What the metric couples to, and what the sky measures

## Stationary equation and which normalization is fixed

Use the existing positive quadratic heavy eigenfield, not the unreduced two-pole theory and not a fitted MTS rotation law. The retained common-metric action is in the adjacent MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md. The Newtonian stationary equation for a real envelope \(f\), normalized so that \(\rho=f^2\) is mass per volume, is
\[
 -\tfrac12\kappa^2\Delta f+\Phi f=\epsilon f,\qquad
 \Delta\Phi=4\pi G(\rho_{\rm compact}+\rho_{\rm bulge}+\eta\rho_*+\rho_{\rm HI}+\rho_{\rm H2}+f^2),
 \qquad \kappa=\hbar/m_h .
\]
The conserved norm is a mass here; divide by the pole mass for particle occupation in this approximation. For a real fast field the nonrelativistic envelope norm is an adiabatic invariant, not an exact fundamental complex-field charge. Neither the norm nor the choice of this stationary branch follows from a local star count. Fixed norm = the previous gas-loaded matched value. Matched norm solves \(R_a g_{\rm in}=V_a^2\) at the same outer Cepheid point; the fixed-scale spherical control gets the same option. No star-dependent change to \(G,\kappa\), stellar heights or environmental box.

The stellar multiplier is the [McKee et al. Table 1](https://arxiv.org/abs/1509.05334) full local column divided by each unscaled full template column. Transferring that solar factor to the entire disk, preserving all radial shapes and relative populations, is a hypothesis, not an observed radial rescaling. The two conventions are not two statistically independent galaxy realizations. Possible bulge overlap and the census versus surviving-mass conventions have not disappeared. The full \(z\) column does not simultaneously enforce the \(1.1\)-kpc column or the midplane density.

Let \(L\) be the constrained second variation at the earlier gas-loaded state (including variation of its Poisson potential), with \(P\) the tangent projection at fixed norm. The frozen incremental response solves \(PLP f_\eta=-P(\Phi_* f)\). In the matched wave add the independently computed norm direction \(f_{\ln N}\) with coefficient \(-[g_*+\partial_\eta g_{\rm wave}|_N]_a/[\partial_{\ln N}g_{\rm wave}]_a\). The comparison halo amplitude obeys \(A'= -g_{*,a}/h_a\) exactly. These are predictions for derivatives, not substitute solutions across the finite column change. A central difference around the inherited state tests the linearization without fitting a derivative.

## Stress selected by metric variation

Use signature \((-+++)\). Minimal coupling gives \(T_{\mu\nu}=\partial_\mu h\,\partial_\nu h-\frac12g_{\mu\nu}[(\partial h)^2+(m_hc/\hbar)^2h^2]\), with overall field units fixed by matching the rest density. Take a stationary real standing envelope, no mean phase flow, with local weak-field lapse \(1+\Phi/c^2\). One convenient normalization is \(h=\sqrt2\,\kappa f\cos[(c^2+\epsilon)t/\kappa]\), \(x^0=ct\). Then the cycle-averaged kinetic-time minus rest-mass term, divided by two, is \((\epsilon-\Phi)f^2\) at retained order: the lapse contributes the minus \(\Phi\) term. Dropping that term would give the wrong gravitational work. Spatial derivatives give the leading, order-\(\rho v^2\), stress in local orthonormal axes:
\[
 S_{ij}=\kappa^2 f_i f_j+\delta_{ij}[(\epsilon-\Phi)f^2-\tfrac12\kappa^2|\nabla f|^2].
\]
This is invariant under a common shift of the potential and eigenvalue. Only the combination \(\epsilon-\Phi\) enters. In the stationary equation, \((\epsilon-\Phi)f=-\kappa^2\Delta f/2\), so the equivalent on-shell expression is
\[
 S_{ij}=\kappa^2 f_i f_j-\delta_{ij}\tfrac14\kappa^2\Delta(f^2),\qquad
 \partial_j S_{ij}=-f^2\partial_i\Phi .
\]
For the divergence, the two derivatives of \(|\nabla f|^2\) cancel; the remaining terms proportional to \(f_i\) vanish by the stationary equation. In particular the stress is not the one-parameter pressure of an isotropic fluid. The momentum-flux tensor \(\Pi_{ij}=\kappa^2(f_i f_j-f f_{ij})/2\) has the same divergence but
\[
 S_{ij}-\Pi_{ij}=\tfrac14\kappa^2(\partial_i\partial_j-\delta_{ij}\Delta)\rho .
\]
This identically divergence-free term matters for local traction/metric stress. Equating conserved force divergences is insufficient to choose a relativistic source. The fast mean, unoccupied low pole, weak static potential, negligible interactions and absence of a phase-gradient flow are limitations here.

## Independent force and kinetic moment checks

Integrate over the upper half of the spherical numerical domain. With no streaming, reflection symmetry and Dirichlet wall \(f=0\), the exact identities within this approximation are
\[
 2\pi\int R S_{zz}(R,0)\,dR=\int_{z>0}\rho\,\partial_z\Phi\,dV+
 \tfrac12\kappa^2\int_{\rm cap}\mu(\partial_r f)^2\,dA .
\]
The cap normal is outward and the equatorial outward normal points downward. At the spherical wall tangential derivatives vanish but the radial derivative need not. A box wall is not being declared a physical edge of the Milky Way. With \(i=z\), multiply the balance by \(z\) and integrate by parts; the full-volume result is \(\kappa^2\int f_z^2=\int\rho z\partial_z\Phi+\oint z S_{zj}n_j\). Summing \(x,y\) gives the separate transverse check with \(f_R^2,R\partial_R\Phi\). The surface integral of \(\nabla(f^2)\) vanishes at a Dirichlet wall; hence \(\int {\rm tr} S=\kappa^2\int|\nabla f|^2=2K\). Dimensions are respectively mass times acceleration for the first identity, or mass times speed squared for the virials. A spherical NFW density without a distribution function does not predict its own material pressure; its **force** is tested on exactly the same data, but assigning it this specific wave identity would be an unfair control.

For the numerical check, reconstruct \(f,\partial_r f,\partial_\mu f,\Delta f\) from the saved finite field, not a radial difference of the observed accelerations. Compute the independent wave potential by interior/exterior multipole integrals with physical mass \(v^2L/G\); include the gas sheet potential and its exact vertical derivative, stellar multipoles, spherical bulge and compact potential. Compare plane traction calculated both from the Hilbert expression containing the eigenvalue and from its on-shell spatial form. Also check the gradient integral against the diagonal spectral \(2K\). The discrete projected equation can have an excellent norm residual even while these continuum checks retain a finite error. \(\int{\rm tr} S/(M c^2)\) measures the size of the **wave stress trace**, not the full post-Newtonian correction to an orbit or to lensing.

## What two force vectors can and cannot tell us

For positive inward force \(g\), physical \(g_z\), at spherical radius \(r=\sqrt{R^2+z^2}\), \(a_r=(-Rg+zg_z)/r\) and \(a_\theta=(-zg-Rg_z)/r\). Reflection across the plane reverses \(a_\theta\), not \(a_r\). A spherical field cancels out of \(a_\theta\) exactly for any radial mass. This checks the angular source with no halo-shape assumption beyond symmetry. The two polarities and different sites of [Lim et al. Fig. 9](https://arxiv.org/html/2305.13358v3) do not constitute independent likelihood factors; they are force estimates from the equilibrium of common stellar tracers.

More generally, an arbitrary positive spherical dark density need not look like the fixed 16-kpc NFW profile. For any allowed total radial acceleration \([l_i,u_i]\), the required dark enclosed mass lies in \((a_{r,b}-[u_i,l_i])r_i^2/G\). The two sides constrain the same mass. Intersect these intervals with \(0\le M_1\le M_2\le M_a\), where the outer mass is fixed by the shared speed after subtracting the luminous force. All constraints are affine in \((\eta,M_1,M_2)\). If one additionally demands dark density nonincreasing with radius, the three average shell densities from \(0,r_1,r_2,R_a\) must be nonincreasing; this is also sufficient **at the three radii**, by a piecewise-constant spherical density. No interpolated witness is a physical MTS state or a preferred halo. Minimizing a common scale factor on the actual upper and lower pointwise band widths diagnoses the size of an incompatibility; it is **not** chi square, a confidence level, or a combined significance.

A separate force readout uses the secular aberration of distant quasars. The transverse aberration drift is \(\dot{\boldsymbol n}=[I-\boldsymbol n\boldsymbol n^T]\boldsymbol a_\odot/c\) to first order. The smooth Galactic acceleration here is evaluated at the published solar position, not obtained by dividing the outer calibration speed squared by the solar radius. Compare its dipole amplitude to [Gaia EDR3](https://arxiv.org/abs/2012.02036). This uses a different measurement principle, not an assertion that Gaia catalogues, reference frames or historical model development are independent; external acceleration and local substructure are not modeled.

## Two follow-through diagnostics

Write the monotone radial mass deficit as D = M2_min − q M1_max with q = (r2/r1)^3. Subtracting a fraction t of the spherical bulge from the ordinary source raises the allowed dark masses by t B1 and t B2. A necessary repair is t(q B1 − B2) ≥ D. The polar force is unchanged. The bound uses the actual enclosed bulge masses, not its asymptotic total. An ideal mass deficit wholly inside r1 would require at least D/(q−1). These estimates do not apply as enclosed-mass formulae to signed disk forces. For a more restrictive cusp with r times density nonincreasing, shell masses per increment in r² must be nonincreasing. The mass and cusp certificates use positive, spherical dark material only; neither is an assumption about the actual nonspherical wave.

The two equivalent continuum plane stresses differ on a numerical state by a known residual. On-shell form minus direct form equals f times [(Phi−epsilon) f − kappa² Laplacian(f)/2]. Project that residual on the retained orthonormal even Legendre modes at each radius. At the plane, integrate its projection times 2 pi R f and independently integrate each complementary potential-times-envelope component. Kinetic and chemical terms are in the retained angular span. The sum reconstructs the measured stress difference without fitting; the spherical potential has no high-angular part. This diagnoses residual directions, not a posteriori corrections inserted into either force.

