# Common acceleration versus relative motion

**What was supplied.** We stay on the positive quadratic, nonrelativistic heavy-wave branch in the common metric. In physical units the Hamiltonian per unit mass is \(-(\hbar/m_h)^2\nabla^2/2+\Phi+U\) and \(\nabla^2\Phi=4\pi G(\rho_w+\rho_b)\). The compact ordinary component is the previous collisionless, spherical, circularly supported population, equal in the two tangential senses, not an isotropic gas with a newly chosen sound speed. Its mass and physical radius are held fixed when the wave occupation changes. Both calculations start on their own stationary loaded, positive, nodeless wave with the corresponding isolated mass. This is a choice of prepared population, not a rule for galaxy formation.

**1. What common gravity fixes.** Let \(\boldsymbol\Delta=X_b-X_w\). The self-energies are translation invariant. The mutual energy for rigid translations is \(\int\rho_b(x)\Phi_w(x+\Delta)d^3x\). The linear term vanishes by spherical symmetry; the Hessian is isotropic, with trace \(\int\rho_b\nabla^2\Phi_w\). Thus
\[
 E_{\rm mut}(\Delta)-E_{\rm mut}(0)=\tfrac12 k|\Delta|^2+O(|\Delta|^4),\quad
 k=\frac{4\pi G}{3}\int\rho_w\rho_b\,d^3x .
\]
The force on the cloud is \(-k\Delta\), the wave gets the opposite. The Hessian in the two translations has blocks \(kI,-kI;-kI,kI\): no spring acts on their common position. With no overlap the quadratic coefficient is zero. This follows as well from the antisymmetry of the isolated Newton kernel or the Newtonian field stress integrated over a surface at infinity. A supported exterior, flux through a boundary, or prescribed external matter must be counted separately. Here the ordinary density vanishes smoothly at its surface and the satellite does external work. The common acceleration is removed only as a choice of frame. Reduced mass \(\mu=M_wM_b/(M_w+M_b)\) gives rigid frequency squared \(k/\mu\), not a normal-mode assertion for the live fields.

**2. A live ordinary dipole from orbits, not a tether.** Use wave units in which \(\nabla^2\Phi=\rho\), background amplitude \(u\), radial mass \(m(r)=\int_0^r s^2\rho_b ds\). For a single applied dipole along \(e\), express an orbit displacement as \(\delta x=[n,t]W[n,t]^T e+E h(h\cdot e)\), \(h=n\times t\); write its inertial velocity with coefficients \(P,P_h\). This spans the parity-even response to a scalar potential; linear superposition gives the vector source. \(n,t\) rotate with \(J=\bigl(\begin{smallmatrix}0&-\Omega\\ \Omega&0\end{smallmatrix}\bigr)\), \(\Omega^2=\Phi_0'/r\). Direct differentiation and Newton's equation give
\[
 \dot W=P-[J,W],\qquad
 \dot P=-[J,P]-{\rm diag}(\Phi_0'',\Omega^2)W-{\rm diag}(V',V/r),
 \qquad \ddot E=-\Omega^2 E-V/r .
\]
Here \(V(r)e\cdot n\) is the perturbed potential. This includes advected orbital phase and transverse motion. A monopolar radial epicycle by itself is not this equation.

Write \(A=W_{11},D=W_{22}\). At fixed direction \(n\), averaging the orbit tangents gives mean displacement \(A n(n\cdot e)+(D+E)(I-nn^T)e/2\). Mass transport \(-\nabla\cdot(\rho_b\delta x)\) gives the dipolar density
\[
 d_b=-(r^2\rho_b A)'/r^2+\rho_b(D+E)/r.
\]
With \(L=\int_0^r s^2\rho_b(A+D+E)ds,\ B=\int_r^\infty \rho_b(D+E-2A)\,ds/s\), its isolated field is \(V_b=-(L/r^2+rB)/3\), \(V'_b=(2L/r^3-B)/3-\rho_b A\). A shared shift \(A=D=E=1\) gives exactly \(-\Phi_b'\) and cancels the self force from shifting orbits in the background field. Off-diagonal dyads do not contribute to the instantaneous density but evolve and feed back.

**3. Removing cancellation without removing the response.** The acceleration of the mass originally enclosed by a circular orbit due to its own component, relative to the background, is exactly \(B(r)/3\). Indeed the local mean is \([\Omega_b^2(2A-D-E)+B]/3\), where \(\Omega_b^2=m/r^3\); integrate with \(dm\) and use \(B'=\rho_b(2A-D-E)/r\). Internal terms cancel. This is an identity for the *Lagrangian* group; it does not discard material at the edge of an Eulerian sphere. Define its center \(P_c=L/(3m)\) and encode each orbit relative to that center by \(S=W-P_c I,\ S_h=E-P_c\). Then, in the cloud center frame,
\[
 P_c(r)=-\int_r^{R_b}\frac{m'}{3m}({\rm tr}\,S+S_h)\,ds,\qquad P_c(R_b)=0 .
\]
For the self part of the relative acceleration, the radial diagonal term is simply \(2\Omega_b^2 S_{11}\); both tangential diagonals have \(-\Omega_b^2 S_{22,h}\). Off-diagonal accelerations retain their background Hessian terms. External forces use their local value minus the acceleration they give the enclosed ensemble; this is not a screening prescription. A harmonic wave potential with curvature \(h_0=u(0)^2/3\) contributes exactly \(-h_0 S\) to the internal equation. Subtract this analytic term before integrating the remaining nonharmonic wave tide. It leaves the relative translation free to evolve. Smooth manufactured dyads verify the transformation against direct Poisson forces; the unstable pre-transformation discretization is not a physical prediction.

**4. Wave response and equal exchange.** In the translating wave frame let the real and imaginary dipole perturbations be \(a(r),b(r)\), omitting the directional factor. With \(H_1=-\tfrac12(\partial_r^2+2\partial_r/r-2/r^2)+\Phi_0-\epsilon\),
\[
 \dot a=H_1 b,\qquad
 \dot b=-H_1 a-u(\delta\Phi_{wi}+\delta\Phi_{bi}-\Delta\Phi_b'+U_1+\ddot X_w r).
\]
The induced wave density is \(2ua\). The wave center and boost removed from internal variables are \(-u'\) and \(ru\); \(H_1(ru)=-u'\). Their physical motion is integrated, not pinned. The moment \((2/3M_w)\int r^3 u a\,dr\) and its velocity vanish in this frame. The off-center physical satellite contributes its real dipole after subtracting the uniform point acceleration.

Let \(A_i,D_i,E_i\) now denote the reconstructed displacements relative to the *whole* cloud center, \(\langle f\rangle_b=M_b^{-1}\int r^2\rho_b f\,dr\). The force per cloud mass from changing the internal states is
\[
 f_{\rm pol}=-\tfrac13\langle \delta\Phi_{wi}'+2\delta\Phi_{wi}/r\rangle_b,\qquad
 f_{\rm shape}=-\tfrac13\langle \Phi_w'' A_i+(\Phi_w'/r)(D_i+E_i)\rangle_b .
\]
Thus the relative response obeys the useful identity
\[
 \ddot\Delta+(k/\mu)\Delta =
 \langle g_s\rangle_b-\langle g_s\rangle_w+
 (1+M_b/M_w)(f_{\rm pol}+f_{\rm shape}) .
\]
Only the applied external averages enter the total center acceleration. The internal forces in the two equations sum to zero; imposing zero *relative* motion instead would be wrong. Each of these three sources can be propagated with the same retarded oscillator kernel; their sum reconstructs the live displacement even though the polarization source itself requires evolving the wave. Independent signed-volume force and mutual-energy checks are in the control tables.

**5. Normalization and interpretation.** To keep the ordinary source physically identical for a different wave length unit \(f=\ell/\ell_{\rm illustrative}\), its dimensionless density scales as \(f^4\rho_b(fr)\), its potential as \(f^2\Phi_b(fr)\). The ground-state boundary conditions are regularity, isolated exterior potential, vanishing tail at the large box and fixed wave mass. A simple rescaling of both objects together would answer a different question. All reported offsets are derivatives at zero perturbing strength times the reference satellite mass, in a common instantaneous Newtonian spatial frame. A relative centroid needs both a specified ordinary tracer and a way to observe a mass centroid. It is not an absolute acceleration, a fitted halo center, or a determination of occupation.
