> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Source, inertia and the clock are three different uses of a weight

The preceding material-coupling test (not bundled here) found that \(w\,dp\) does not integrate to a scalar pressure for the reconstructed gas. Here we actually evolve the gas, project the changing raw and effective sources onto the same observable, and test whether gravitational reciprocity permits treating a statistical weight as a physical coupling.

## The material calculation

Use meridional coordinates \(x=(R,z)\); rotate about the axis and reflect across the central plane as in the source. A triangle of signed plane area \(A>0\) has exact volume \(V=(4\pi/3)A\sum_a R_a\), not \(4\pi r^2\,dr\) for a generic displacement. The interpolation \(X=\sum N_a x_a\) is affine inside it. A gas mass \(m_i\) initially uniform per physical volume in this triangle has corner masses \(m_{ia}=m_i(\sum R+R_a)/(4\sum R)\). Initial thermal energy \(U_{i0}\) and mass are obtained by separate positive quadrature of the reconstructed native mass and thermal densities. Snapshot kernels smooth each native centre before assigning the original spatial label \(w_i\); this implements the *cell-labelled material* construction, not a gas of separately labelled overlapping clouds. Each original label cell is retained when the mechanical mesh is subdivided. The reference density is represented by its triangle average thereafter.

With fixed entropy use \(U_i(V)=U_{i0}(V/V_{i0})^{1-\gamma}\); \(p_i=-\partial U_i/\partial V\). The outward pressure force on a corner is \(F_{ia}=p_i\partial_{x_a}V_i\). At a free vertex the raw equation is \(m_a\ddot x_a=m_a g(x_a)+F_a\), \(F_a=\sum_i F_{ia}\), \(m_a=\sum_i m_{ia}\). The field \(g\) is the gradient of a time-frozen interpolated potential from the corresponding retained wave, common to both matter prescriptions in each arm; we use its radial derivative in the interpolation. No new mass, rest frame, or metric coupling was fitted. The unmodelled foreground is not an imposed new acceleration. Gravity is not recomputed from the moving pressure patches in this experiment: those patches alone do not constitute a complete galaxy.

For a positive split \(f_i=w_i/\max_{\rm aperture} w\), \(f_a=\sum_i m_{ia}f_i/m_a\),
\[
 Q_a=f_a F_a-\sum_i f_i F_{ia},\qquad
 \frac{d}{dt}(m_a f_a v_a)=m_af_a g+\sum_i f_iF_{ia}+Q_a .
\]
Compute the complementary stress from its actual separate corner sum with \(1-f_i\). Its exchange is exactly opposite. \(Q_a\) is a discretization of the pressure traction on a moving label; in the continuum \(\nabla_\mu(fT^{\mu\nu})=p h^{\mu\nu}\partial_\mu f\) for an initially conserved perfect fluid with an advected label. No fitted force is added to raw motion. Multiplying the label equation by \(v_a\) gives the additional independent test
\[
 \Delta\left[\sum_a m_af_a(v_a^2/2+\Phi_a)+\sum_i f_i U_i\right]
 =\int dt\,\sum_a v_a\cdot Q_a.
\]
The fixed outside nodes can carry reaction forces but do no work. Momentum in the report is the two *meridional generalized components* of the reflected, axisymmetric system summed over identified free interior nodes, not net Cartesian momentum of both mirror halves. The label impulse, gravity and own-pressure impulse are booked separately. For the **effective** alternative, replace both corner masses and thermal reservoirs by \(w_i m_{ia},w_i U_{i0}\), and evolve *its own* positions and pressure. Constant scaling of all weights cannot alter these paths.

## A prediction frozen by the equations, checked by actually evolving

Let \(C(X)=\int_{\rm core} w\,dm\,K(X)\) with the original two-probe clock kernel and cap 64. Use the same tagged masses in both prescriptions; only the paths differ. The two arms are reset and coupled. At rest write \(d=g_c-g_r\), \(e=P_{\rm eff}-P_{\rm raw}\), where \(P\) denotes the full nodal pressure *acceleration*, and \(DP\) its derivative under a common displacement. Fixed boundary nodes have zero displacement and acceleration. For the difference “effective minus passive, coupled minus reset”, the second derivative vanishes. Where the material problem is smooth, its first possible nonzero term has the **analytical coefficient**
\[
 C_{\times}^{(4)}
 =DC\!\left[(DP_{\rm eff}-DP_{\rm raw})d+(Dg_c-Dg_r)e\right]
 +6D^2 C[d,e].
\]
This follows by applying \(C^{(4)}=DC[Db\,b]+3D^2C[b,b]\) to each autonomous start \(\ddot X=b(X)\). It includes gravity evaluated at different positions and the changing readout, not just the mixed pressure Hessian of the prior stage. The pressure derivative is calculated analytically by differentiating \(p_i\nabla V_i\); finite displacements independently check it. In the clock Hessian there is a regular tensor and a radial sheet \(nn[\partial_r K]\delta(r-p_j)\). We integrate both. For the direct clock readout, all four transported configurations use common initial material coordinates with quadrature split at the union of their exact intersections with the probe sphere. Mass stays in the integration measure even as the probe cuts different material. Numerically stable Green and Legendre differences avoid subtracting two almost equal absolute potentials. The launch coefficient is a result at each fixed mesh, not automatically its continuum limit in the presence of a discontinuous label.

## What propagates when a pressure label jumps

Take a small plane normal to a label interface. In its initially freely falling frame freeze the smooth raw density and pressure to \(\rho_0,p_0\). The physical gas with an advected label has no acoustic wave from that label alone: pressure stress and label traction balance. The separately pressurized model instead has initial states \((w_L\rho_0,0,w_Lp_0)\), \((w_R\rho_0,0,w_Rp_0)\). Both sound speeds are \(c_s=\sqrt{\gamma p_0/\rho_0}\); **equal sound speeds do not imply equal pressures**. We use the classical ideal-gas Euler Riemann solution, not a new MTS wave law ([Ketcheson, LeVeque & del Razo, Euler chapter](https://www.clawpack.org/riemann_book/html/Euler.html)). The rarefaction follows the isentropic characteristic and the shock satisfies the mass, momentum and energy jump conditions. Pressure and normal velocity coincide across the star contact. Solving these equations for the saved face states predicts a contact kick with leading weak-jump velocity \(c_s\ln(w_L/w_R)/(2\gamma)\). Independently evolve the same data in conservative mass, momentum, energy and compare the full velocity and pressure profiles, not just the contact velocity.

For this **planar test only**, the induced gravitational field can also be derived without a halo or coupling choice. In \(x=c_s t\,\xi+a_{\rm wave}t^2/2\), write \(\hat\rho=\rho/\rho_0,\ \hat v=v_{\rm flow}/c_s\) in the freely falling frame. Subtract the translated passive step \(\hat\rho_{\rm ref}=w_L\) or \(w_R\). Continuity integrates to
\[
 I(\xi)=\int_{-\infty}^{\xi}(\hat\rho-\hat\rho_{\rm ref})\,d\eta
       =\xi(\hat\rho-\hat\rho_{\rm ref})-\hat\rho\,\hat v,\qquad
 \delta g=-4\pi G\rho_0 c_s t\, I .
\]
The field perturbation vanishes beyond both fronts because the **net surface mass perturbation is zero**. Nevertheless the pressure impulse gives a finite dipole per area \((p_L-p_R)t^2/2\) and a far-side potential difference \(-2\pi G(p_L-p_R)t^2\). Integrating the density and field directly checks both signs. These are isolated one-dimensional half-space predictions; front speeds here are acoustic, not the propagation speed of gravity. Finite transverse sizes, the other angular/radial faces, actual gas velocities, cooling, and a complete metric would be required to extrapolate them to a sky clock.

## The additional gravitational reciprocity condition

In the retained weak-field coupling \(H_{\rm int}=\int \rho_{\rm grav}\Phi_w\,d^3x\), moving a conserved material measure \(w\,dm\) gives virtual work \(\int w\,dm\,g_w\cdot\eta\). An independently inertial *raw* fluid with universal metric acceleration requires \(\int dm\,g_w\cdot\eta\) for the same displacement. Equality for every admissible interior variation requires \((1-w)g_w=0\) almost everywhere, unless the complementary source/interaction participates. Pressure exchange at a label face cannot repair a bulk mismatch even in a pressureless region. This is an action–reaction test on a **hypothetical hybrid**; it does not assert that the previously reciprocal represented-mass pilot used that hybrid.

For a smooth retained forcing \(g\) define \(I_j=\int dm\,w^j |g|^2,\ j=0,1,2\). The sharp minimum relative RMS acceleration mismatch over *any one scalar rescaling* of the weight is
\[
 \min_\alpha\bigl[\int dm\,|(\alpha w-1)g|^2/I_0\bigr]^{1/2}
 =\sqrt{1-I_1^2/(I_0 I_2)}.
\]
The minimizer is only a diagnostic lower bound, not a proposed rescaling of Newton's constant. The full aperture calculation uses both wave fields and their difference, gas and stars separately. The angular and radial force of an actual source replacement is independently computed by applying the same Poisson law to the raw, tagged and signed-difference mass maps. A weighted empirical representation can still be perfectly legitimate if **it is the physical population being modelled**, with its own inertia and stress. Conversely a label may be a passive *observable* of full raw matter; it then must not silently be the only source seen by the wave. A physical positive transport model between the simulated and target hosts is another possibility; their data are not interchangeable.
