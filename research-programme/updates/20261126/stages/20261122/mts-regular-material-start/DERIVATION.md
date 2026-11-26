# A regular material start for the scalar constraints

## Which physics is input?

Use the retained single metric, scalar GR constraints, minimal particle couplings, saved cold and heavy scalar potentials/backgrounds, and the same classical Fourier phases/long–short pairs as the previous stage. This tests their mutual compatibility; it does not infer an action from GR, calibrate Newton's constant, or use an observed curvature to choose a starting potential. No independent second-order vector, tensor, isocurvature or primordial spectral distortion is injected. Conformal time and inverse wavenumber are in Mpc (light speed one); the metric potentials and the thermal brightness are dimensionless. These are complex amplitudes of specified modes, not power spectra.

The linear relativistic hierarchy and regular-mode method are standard ([Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072)); see [Pitrou, Uzan & Bernardeau](https://arxiv.org/abs/1003.0481) for second-order relativistic cosmology and [Pettinari](https://arxiv.org/abs/1405.2280) for the distinction between primordial and evolution-generated signals. The derivation and runs below apply those physical assumptions to our saved signed panel and canonical fields; the external calculations are not the MTS runs.

## Initial conditions before horizon entry

Use exponential metric potentials \(A=\psi_1+\psi_2-\psi_1^2,\ B=-\phi_1-\phi_2-\phi_1^2\), no factorial on order two. Square brackets below denote the retained signed Fourier convolution, both orderings. In the adiabatic radiation limit \(\mathcal H\eta=1,\ R=(e_r+e_{\nu,m})/e_{\rm rad}\); normalize the incoming linear curvature to one before inserting its actual complex amplitudes. The gravity energy constraint yields \(\delta_{r1}=-2P\) with \(P=\psi_1\). Dipole streaming gives \(N_{11}=k\eta P/6\), quadrupole streaming \(N_{12}=(k\eta)^2P/30\). Thus shear times the radiation density survives at leading order and yields \(C=\phi_1=(1+2R/5)P\). The logarithmic radiation curvature \(\zeta=B+\ln(E_r/\bar E_r)/4=1\) then fixes \(P=-1/(3/2+2R/5)\). Dropping a quadrupole merely because it is of order \(\eta^2\) would be wrong.

At quadratic order the time and energy constraints give \(\eta F=-\psi_2+3[P^2]/2,\ \delta_{r2}=-2\psi_2+4[P^2]\). Expansion of the same curvature therefore yields
\[
 Y=\phi_2+\psi_2/2=-\zeta_2-[C^2]+[P^2]/2 .
\]
Writing the collisionless dipole and quadrupole as \(\eta(d_1+k\psi_2/6)\) and \(\eta^2(d_2+k^2\psi_2/30)\), respectively, their streaming equations give \(d_1=k[P^2]/3+S_1(0)\) and \(d_2=kd_1/5+\lim_{\eta\to0}S_2/(2\eta)\). Here \(S_\ell\) is the direct local-angle geodesic source in the retained conventions. With \({\cal S}\) the scalar longitudinal shear projection and \(V=P/2\) the coefficient of the baryon velocity potential, the traceless spatial equation gives
\[
 (3/2+2R/5)\psi_2 = Y+
 \{4(1-R){\cal S}(V,V)-12R d_2-Q\}/k^2,\qquad
 \phi_2=Y-\psi_2/2 .
\]
The Fourier Hessian in \(Q\) carries a **minus** sign: \(\partial_i\partial_j e^{ipx}=-p_i p_j e^{ipx}\). Both its ordered projections have this sign. The first implementation reversed these in the analytical start only. Enforcing its own symbolic slip and momentum identities did not catch that error; comparison with the actual finite-surface source did. Earlier numerical packets are retained and excluded from the adopted restart.

Let \(\theta_1=-P/2,\ \theta_2=\zeta_2+\phi_2+[C^2],\ B_2=-\phi_2-[C^2]\). Expand the background scalar along \(\tilde a=a e^{-\theta}\), and its canonical momentum including the volume factor \(e^{3B}\). For \(v=b'\), \(N=\ln a\):
\[
 f_2=-b_N\theta_2+\tfrac12 b_{NN}[\theta_1^2],\qquad
 w_2=(v-v_N)\theta_2+\tfrac12(v-2v_N+v_{NN})[\theta_1^2]
      +3(v-v_N)[-C\theta_1]+v(3B_2+\tfrac92[C^2]).
\]
Here \(b_N=v/\mathcal H,\ b_{NN}=v_N/\mathcal H-v\mathcal H'/\mathcal H^3\). This involves no division by the field velocity. Densitized dust and photon coordinates are \(d_2=3\zeta_2+9[1^2]/2,\ x_{\gamma2}=4\zeta_2+8[1^2]\); dust velocity divergence begins at \(k^2\eta(\psi_2-[P^2]/2)/2\). The regular photon and neutrino momenta are not arbitrary reservoirs. The finite-surface constraints, using evolving densities, set the actual metric after these leading-order starts. Free \(\zeta_2\) (zero or one unit of the local squared linear curvature for the tests) is a separate primordial datum, not a coupling.

## Coupled flight and two determinations of gravity

All source files use 782 exact incident wavenumbers, five mixed Fourier modes and 1,281 log-spaced native time levels. The collisionless angular driver uses 321 levels from the native metric; the source interpolation is in log conformal time. Use the prior canonical scalar equations, forced dust number and momentum, Thomson photon and baryon transfer, photon intensity and polarization moments through order six, and collisionless moments through order eighteen. Thomson loss, gain, kinetic and rate sources are included for the quadrupoles, and direct higher-angular forcing is retained. Incident photon/polarization moments of orders four to seven used inside that forcing use the leading tight-coupling recurrence; orders two and three are native. Final \(k_{\rm leg,max}/\dot\kappa\) is only 0.001035. In the evolution the large opacity is **not** set to infinity: propagate \(W=j_\gamma+(e_b/e_\gamma)t_b\) and \(B_s=j_\gamma-4t_b/3\) to keep the stiff slip separate from conserved momentum. For cold and MTS use identical algorithms, cutoffs, grids and tests.

For the normal collisionless integrated brightness evolve \(N_0-\phi_2\), so the normal energy has an explicit linear metric coefficient. If \(E=E_*+C_E\phi_2,\ J=J_*\) are the summed material energy and longitudinal current (in the upstream rescaled stress convention), the two constraints give
\[
 F=-J_*/(2k^2),\qquad
 \phi_2=(U-E_*/2+3\mathcal H F)/(k^2+C_E/2),\quad
 \psi_2=\phi_2+(S-Q)/k^2 .
\]
The cold/baryonic \(C_E\) contribution is \(3(e_c+e_b)\), photon \(4e_\gamma\), scalar \(3\sum v_s^2\), ultrarelativistic neutrino \(4e_r+3(e_{\nu,m}+p_{\nu,m})\). The alternative algorithm only sets these two constraints at launch, thereafter evolving \(\phi_2'=-F-\mathcal H\psi_2+F_q\) and the spatial trace equation for \(F'\) with independently assembled material trace \(E-3P\). They share the underlying field equations, not independently fitted histories.

Third-order two-stage Radau IIA in log time is the adopted solver; second-order stiffly accurate SDIRK is an independent time discretization. Columns with zero and nonzero \(\zeta_2\) share exactly the same operator and forcing. Compare their difference with independent **linear** native transfers at the exact five output wavenumbers, including the heavy scalar. This checks signs, scaling and mode propagation; by itself it would cancel errors in the common quadratic forcing, hence the separate finite-surface, angular, trace and time checks.

## Microscopic information at the endpoint

For collisionless initially thermal particles at unit propagation speed a ray transports a log-temperature perturbation \(\vartheta\), \(f=f_0(qe^{-\vartheta})\). With \(W=-\partial_{\ln q} f_0,\ w=\partial_{\ln q}\ln W=1-q\tanh(q/2)\), expansion gives
\[
 F_2(q)=\delta f_2/W=\vartheta_2-\tfrac12 w[\vartheta_1^2],\quad
 F_{2,\ell}(q)=N_\ell+(w+4)Z_\ell,\qquad
 Z_\ell=-\tfrac12[\vartheta_1^2]_\ell .
\]
Integration by parts gives \(\langle w\rangle_{q^3 W}=-4\); the second channel is invisible in massless integrated brightness. It is not identically zero in the distribution. Two evaluations: (1) project both first-order incident distributions on their actual directions about each output mode and integrate their product on the sky; (2) differentiate the direct collisionless source with respect to \(w\), evolve its response through free streaming from the projected initial square. Both include the signed mixed pairs. A second angular rule and four thermal momentum orders test the reconstruction. Its spectral shape is independent of the free curvature **for this specified undistorted initial thermal distribution**. A separate primordial spectral distortion is not constrained here.

For fixed reconstructed moments at the endpoint, the spectral contribution to massive energy is proportional to \(Z_0\int W(w+4)q^2(\epsilon-q)dq\); shear to \(-Z_2\int W(w+4)(q^4/\epsilon-q^3)dq\), normal current exactly zero. Subtracting the analytically zero massless term avoids numerical cancellation. This tests the instantaneous gravity error in replacing \(F_2(q)\) by \(N\); it does not bound all earlier or later mass-dependent transport. The main flight uses relativistic common-speed propagation, enforces finite-mass thermal stress for the brightness channel, and compares with a massless-stress control. A full massive propagation of this momentum-dependent state is the next physical check. No initial distribution is recovered by fitting late potentials.
