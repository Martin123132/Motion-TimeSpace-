# Which flow do these two galaxy histories actually determine?

All derivatives here are at the shared launch, snapshot 590, and are **differences** between the inherited wave and the reset wave, at the same fixed wave occupation. Neither simulation nor foreground chooses the galactic occupation. Keep the positive matter particles of FIRE separate from the continuum density inferred from the retained hybrid potential. FIRE gas also has non-gravitational forces; applying a collisionless cubic kernel to its current is a diagnostic, not a hydrodynamic simulation of a new force.

## Measure the previously missing projection on a real simulation

Let \(d=h_c-h_r\), \(W(r)\) be the old mass or gravity window, and \(J\) the common initial ordinary mass current. The cubic field term is \(-\int\rho\,\nabla W\cdot\nabla\dot d\); its current kernel is \(K=-3\,{\rm Hess}(W)\nabla d-{\rm Hess}(d)\nabla W\). In a shell set
\[
 F=W'(d_r+2d/r),\quad H=-2(W''-W'/r)(d_r-d/r),\quad
 S'=\langle H\rangle_\Omega,\ S(r_{\rm out})=0,\quad D=S-F .
\]
Continue \(D\) as a constant inside the shell and zero outside. Then \(K=\nabla D+(H-\langle H\rangle)\,\mathbf e_r\). This fixes the sign of the density test: \(\int J\cdot\nabla D=\int\dot\rho D\) for conserved matter with no surface term. The only remaining current moment is \(\int J_r(H-\langle H\rangle)\). Direct particle sums evaluate both terms; no current is inferred by fitting the same density differences. Independent checks drift the *same particles* by equal positive/negative small times and read out \(D\) itself. Separate snapshot differences include changes of particle mass and phase, flow over a finite interval, and a moving origin. They need not equal the instantaneous velocity readout.

The retained input is instead \(\delta m_j(t)=m_{{\rm MW},j}(M_{{\rm FIRE},g(j)}(t)/M_{{\rm FIRE},g(j)}(600)-1)\). It defines **densities**, not a per-particle velocity distribution. Reconstruct each adjacent hybrid field with exactly that positive-aperture map, the original even multipoles through 64, and the original angular and radial collocation. Include the weak density at radial element faces. The unequal-spacing derivative at 590 is \((h_R s_L+h_L s_R)/(h_L+h_R)\); this is an interpolating estimate, not a certified error bound or a new assumed evolution between samples.

## A global radial observable that does not need a fitted internal current

Take \(I=\tfrac12\int r^2\rho\,d^3x\) about a common inertial origin (or common nonrotating translating origin with potential difference unchanged). This is the scalar moment of inertia divided by two, not an equilibrium assumption. At the launch of otherwise identical collisionless distributions,
\[
 \delta I''=-\int\rho\,\mathbf x\cdot\nabla d,\qquad
 \delta I'''=-\int\rho\,\mathbf x\cdot\nabla\dot d-\int J\cdot\nabla B,\qquad
 B=2d+\mathbf x\cdot\nabla d .
\]
Indeed \(3\nabla d+({\rm Hess}\,d)\mathbf x=\nabla B\). This works in **three dimensions without assuming spherical symmetry**. An internal divergence-free current of compact support cannot contribute to this cubic; no such cancellation is guaranteed for the two old tapered shell weights. Direct integration of two orbits in time-dependent, nondiagonal quadratic potentials tests this independently of source reconstruction.

For a ball and \(\dot\rho+\nabla\cdot J=s\), the interior current term is
\[
 -\int J\cdot\nabla B=-\int B(\dot\rho-s)-\oint B J_n .
\]
The numerical “interior cubic” is the first wave term and the density-rate bulk term: it is **not** the entire time derivative of an aperture cut with moving particles. An actual source can add its own contrast moments; inserting \(s\) in the continuity identity does not derive dynamics for created/destroyed matter. The surface test in the code has a nonzero radial flow and remains correct after adding a constant to \(d\); dropping the flux fails it. Open-Green potentials use zero at infinity. Unbounded second moments need not exist: interpret the global identity for finite moments/decaying tails or retain explicit boundary terms.

Compute \(d,\dot d,d_r,d_{rr}\) directly from interior and exterior wave multipoles, using \(2\Re(\psi^*\dot\psi)\) from each saved Hamiltonian. Compute every density pairing independently (i) from the piecewise Laplacian plus all internal derivative jumps, and (ii) by integrating the full Poisson operator by parts including its outer derivative term. No Milky Way velocities enter either calculation. The Poisson boundary derivative here is **not** the unknown ordinary current flux.

## What would make the supplied mass history a conserved one?

Check the **total** change of the tapered transfer rather than presuming it integrates to zero. If the surrounding density is otherwise static, a nonzero total rate requires an exchange, a boundary flux, or an additional evolving mass component. An explicit instantaneous sensitivity test puts the opposite rate into normalized exterior shells, not a fitted density. Radius is distributed as \(30s^2(1-s)^2\,ds\), \(0<s<1\), and angular mass as \(1+\eta P_2\), for \(\eta=-1,0,2\). The shift of the density cubic is \(+\dot M_{\rm tr}\langle B\rangle_{\rm shell}\), in physical units. These are alternatives at **fixed saved wave preparation**, not self-consistently re-evolved halos. A declining shell needs existing mass to lose; zero net rate does not determine a physical transport path or its energy.

Outside the retained wave support, \(d_\ell(r)\propto r^{-\ell-1}\) and \(B_\ell=(1-\ell)d_\ell\). Equal conserved wave norms give zero exterior differential monopole, so a spherical reservoir **entirely outside the wave** drops out of this density term regardless of radius. The angular absolute bound at the wave boundary is \(\sum_\ell\sqrt{2\ell+1}|B_\ell(R)|\); it bounds the whole vacuum exterior. For a one-sign compensating reservoir multiply it by \(|\dot M_{\rm tr}|\); for general opposing gains and losses replace that with the *total variation* of the rate. The same angular bound times unsigned mass flux bounds the finite-surface current term; knowing only the net flux does not suffice. Neither vacuum exterior nor spherical reservoirs are assumptions about the actual LMC environment.
