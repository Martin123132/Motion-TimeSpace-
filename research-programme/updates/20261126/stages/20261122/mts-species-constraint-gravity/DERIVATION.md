> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Gravity determined by a specified material state

## Which density/current?
Use the retained metric and signs (not bundled here) and thermal hierarchy (not bundled here). This is an order-two scalar perturbation on each of the two saved radiation-era backgrounds, with no factorial on the quadratic coefficient. Units are comoving Mpc, \(c=1\); write \(e=8\pi G a^2 E_\perp\) and \(j=\mathrm{div}J\) for the longitudinal divergence of the **spatial covector** normal flux in the parent's units. The orthonormal current must be multiplied by \(e^B\), \(e^{2B}=1-2\phi_1-2\phi_2\); forgetting this first-order factor gives an erroneous mixed current. \(S\) denotes scalar-projected shear, \(D=e-3p\), \(h=a'/a\). Products below mean the actual signed long–short Fourier contraction, not products of absolute values. The conventional linear species/adiabatic framework is reviewed in [Ma & Bertschinger](https://arxiv.org/abs/astro-ph/9506072); the following inventory and numerical tests are on the retained MTS inputs.

* Canonical scalar \(b\), \(v=b'\), \(m_a=am\): with evolved field and canonical momentum perturbations \(f,w\),
  \(e_2=v w+m_a^2 b f+3v^2\phi_2+e_Q\);
  \(j_2=k^2 v f+j_Q\);
  \(D_2=-2v w+4m_a^2 b f-6v^2\phi_2+D_Q\).
  The saved \(Q\) terms contain normal kinetic energy, gradients and the quadratic potential from the parent field action. Treat the slow field and (where present) the heavy field separately. A field absent on the cold control contributes zero.
* Cold rest matter: evolved canonical number contrast \(d_2\) and covariant velocity divergence \(t_2\). With first-order coordinate number \(d_1\) and velocity \(u_i\), the normal trace is \(e_0[d_2+3\phi_2+3\phi_1 d_1+15\phi_1^2/2-|u|^2/2]\). Normal energy adds \(e_0|u|^2\); current is \(e_0[t_2+\mathrm{div}((d_1+3\phi_1)u)]\). These follow from \(E=e_0(1+d)e^{-3B}\gamma,\ J_i=e_0(1+d)e^{-3B}u_i,\ \gamma^2=1+e^{-2B}|u|^2\). Apply to CDM and cold baryons separately; photon work and momentum transfer remain active.
* Photons: the evolved \(g_x,g_j\) denote the coordinate density and coordinate flux divergence. Thus \(e_2=e_\gamma[g_x+4\phi_2+4\phi_1(D_{\gamma1}-\phi_1)]\), \(j_2=e_\gamma[g_j+3\mathrm{div}(\phi_1v_{\gamma1})]\), \(D_2=0\). Use the retained intrinsic and boosted shear.
* Neutrinos: integrate normal distribution monopoles with \(Wq^2\epsilon\), dipoles with \(kWq^3\), trace with \(Wq^2(am)^2/\epsilon\), and quadrupoles with the signed shear weight. Convert the normal dipole into covector divergence by subtracting the \(\mathrm{div}(\phi_1 {\bf j}_{\perp1})\) contraction. For massless temperature moments the density/dipole normalization is \(4e_r\). The shifted hierarchy's instantaneous boosted quadrupole is added once; no extra bulk energy or flux is added to its unshifted normal monopole/dipole. The legacy first-order neutrino current versus the reconstructed incident distribution is a separate convergence control.

## Solving gravity without an unassigned component
At fixed canonical and distribution variables,
\[
 e_{\rm sp}=E_*+C_\phi\phi_2,\quad
 C_\phi=3\sum_\mathrm{fields}v^2+3(e_c+e_b)+4e_\gamma,
 \qquad j_{\rm sp}=J_* .
\]
The neutrino monopole is normal, not coordinate, so it adds **no** \(4e_\nu\) to this derivative. With the saved quadratic Hamiltonian source \(U\),
\[
 F_2=-J_*/(2k^2),\qquad
 \phi_2=[U-E_*/2+3hF_2]/[k^2+C_\phi/2],\quad
 \psi_2=\phi_2+(S-Q)/k^2 .
\]
Evaluate this only on the initial surface, then evolve the trace and matter independently. Compare with using it on every slice while evolving the *same* microscopic laws. Zero residual at the first step of the first method or at every step of the second is construction, not evidence. The first method's subsequent residuals and the two methods' independent late potentials are evidence. The original compensated and two material-join histories are also replayed with the exact older output values.

## Where the discrepancy lives
For each species reconstruct \(X=e_2/e_\gamma-4X_0\phi_2+X_Q\), \(Y=j_2/e_\gamma-J_Q\), and its trace analog \(T\). Energy and longitudinal momentum conservation can be written \(X'=-Y+s_x,\ Y'=\omega^2 X+s_y\) with \(\omega=k/\sqrt3\) and
\[
 s_x=hT-T_0\phi_2'+X_{\rm force},\quad
 s_y=k^2[-T/3+(4X_0-T_0)(\psi_2+\phi_2)/3-T_0\phi_2+
 2(S/e_\gamma+S_{\rm shift})/3]+Y_{\rm force}.
\]
Heat and current transferred by Thomson scattering enter the photon/baryon balance with opposite signs. All quadratic terms are computed from that species' background and *linear* energy, flux, trace and shear. In the rotating pair \((X,Y/\omega)\), the propagator \(R(\omega\Delta\eta)\) is a planar rotation. Integrating each projected source after multiplication by \(R^{-1}\) gives its particular solution without differencing small measured residuals. The difference between metric-required and named normal sources is the transported initial difference plus: the coordinate conversion, the integral of the parent-minus-summed forcing, and aggregate-minus-summed propagation defects. The measured normal residual is computed directly before attributing these terms. Different terms can cancel, and the thinned Simpson control limits the attribution of very small remainders.

A trace-free, shear-free component that starts only at order two contributes no homogeneous background, first-order quadratic forcing, trace, or shear in this calculation. Its normal density and covector divergence in \(e_\gamma\) units therefore obey precisely this *homogeneous* oscillator equation. Take its two complex initial values solely from the unassigned inventory, evolve them analytically, then infer gravity from named matter plus that test component. Reproducing the old gravity this way locates the missing datum; it does **not** establish a new physical species. Reversing its sign or freezing it in the rotating variables' lab frame are negative controls.

## Actual material preparations, not an invisible fluid
At fixed original metric let \(\delta e,\delta j\) be the energy/current to supply. For a common fractional adiabatic density displacement \(\tau\) and common velocity potential \(V\),
\[
 \tau=\delta e/(3\sum_s H_s),\qquad V=\delta j/(k^2\sum_s H_s),\qquad H_s=e_s+p_s .
\]
Use the same finite thermal quadrature for boost and temperature normalization as for the actual material; its enthalpy is checked against the independent native background. Canonical scalar increments are \(\delta f=vV,\ \delta w=3v\tau-m_a^2 bV\); they require no division by \(v\). CDM and baryons receive \((3\tau,k^2V)\) in number/velocity; photon coordinates receive \((4\tau,4k^2V/3)\); the neutrino normal distribution receives \(\delta\Theta_0=\tau,\ \delta\Theta_1=kV/(3v_q)\) with \(v_q=q/\epsilon\). Alternatively apply only the photon or massless-neutrino changes with its own enthalpy denominator. These prescriptions satisfy the same initial constraints exactly and evolve with existing, unequal stress and collision laws. The common fractional density initial condition does not prove absence of intrinsic entropy pressure in a canonical scalar or specify the primordial growing mode. A single local displacement along the background flow would require \(\tau=-hV\); its necessary comoving-density combination \(\delta e+3h\,\delta j/k^2\) is independently tested.

For an added copy of the native regular linear growing mode, the supplied vector at fixed canonical baseline and original potential has direction \((e_1-C_\phi\phi_1,j_1)\), not \((e_1,j_1)\). The two transfer coefficients are real on each scalar Fourier wave; one complex amplitude accounts for its whole phase. Divide each component by its own nonzero required magnitude and project the normalized target onto that single complex amplitude. This gives a lower bound on the best possible joint fractional RMS; it is a diagnostic allowing **more** freedom than an independently predicted amplitude, not an adopted fit. Even freeing the two real coefficients leaves a phase-only lower bound \(\sqrt{(1-|\cos(\arg\delta e-\arg\delta j)|)/2}\). This is not a prohibition on nonlinear adiabatic prehistory: many earlier pairs can have different phases.

Finally, at fixed first-order inputs all these order-two perturbations are linear-affine in initial states. A convex mixture of the three tested allocations therefore has a final complex endpoint inside the triangle of their three values. A separating direction \(u\), \(|u|=1\), such that all three normalized differences have \(\mathrm{Re}(\bar u z)>0.005\), certifies failure of the whole triangle without fitting any coefficient. This bound concerns these preparations with a common allocation for density and momentum, not every allowed distribution or every earlier source.
