# Returning ordinary gravity to the wave

This stage retains the common weak metric and its already fixed wave occupation. Quantities in the Poisson calculation are physical kpc, solar masses, (km/s)² and Myr. A "clock" is the leading difference of fractional rates of stationary probes at cylindrical \((R,z)=(8.3,1.5)\) and \((6,1.5)\) kpc; it is not the proper time of a moving gas parcel. The source is the previously represented positive FIRE-to-target mass, not a measurement inside the Milky Way.

### Push mass; do not interpolate a clock amplitude

Let \(K(t_r,s,\mu)= -G\sum_{\ell=0,2,\ldots,64}P_\ell(\mu_{\rm obs}) P_\ell(\mu)h_\ell(t_r,s)\), where \(h_\ell=\min(t_r,s)^\ell/\max(t_r,s)^{\ell+1}\). This is the retained open Poisson potential of unit ring mass. For displaced ordinary sources \(X_j=x_j+t^2a_j/2\), compute \(\Phi_o=\sum m_j K(X_j)\) without transferring masses between histogram bins. The source-position derivative gives
\[
\Phi_o''=\sum_j m_j \big(a_{rj}\partial_s + a_{\theta j}s^{-1}\partial_\theta\big)K.
\]
Here \(s\partial_s h_\ell/h_\ell\) is \(\ell\) inside the probe and \(-(\ell+1)\) outside. Keep both pieces: the exterior angular field acts even though its monopole produces no interior acceleration. The independent displaced solve accumulates exact interior/exterior moments in each target-separated interval and sweeps them onto every wave radial node and both clocks. It carries constant parcel masses. The 700-kpc exterior monopole is an independent mass check. With matched initial phase space and non-gravitational forces, the common acceleration cancels in the contrast \(a=a_{\rm coupled}-a_{\rm reset}\); the two individual wave kicks are an isolation experiment, not the total physical force on the disk.

### The interaction fixes the returning force

The interaction energy is bilinear in the two mass densities:
\[
 E_{ow}=\int \rho_w\,\Phi_o\,dV=\int \rho_o\,\Phi_w\,dV,\qquad
 F_j=-\partial_{X_j}E_{ow}.
\]
At fixed wave and with the ordinary matter initially comoving, let it be displaced by \(t^2 a/2\). With the conjugate force \(a=-\nabla\Phi_w\), the interaction curvature is \(-\int\rho_o|a|^2dV\) in consistent mechanical units; ordinary kinetic energy gains the opposite curvature. The same polarization gives \(-\int\rho_o a_i\cdot a_j\,dV\) for two different driving/test densities, including their signed difference. This is one work transaction, not a total covariant conservation theorem.

For the actual wave discretization, form radial wave-mass moments from the Hamiltonian's own angular weights and radial mass matrix. Differentiating their discrete pairing with the ring kernel gives a unique conjugate acceleration, with no adjustable coupling. Contrast this with integrating the smooth finite-element wave density first and differentiating its continuous potential. The two approximate the same continuum operator but are **not identical at fixed resolution**. A work check must use an operator and its own derivative on both sides. The physical discretization error is reported separately from the floating-point residual of the exact discrete identity.

### Predict the response of the wave

Write \(U=\Phi_o''/v_*^2\), with time measured in Myr, and \(T_*\) for the wave time unit. Against the same reference nonlinear wave and background history, the added potential is \(t^2 U/2\). Let \(F\) be the unperturbed wave time derivative and \(J\) its real-linear Jacobian including self-gravity. On the retained finite-dimensional system,
\[
 \delta\psi=t^3 b+t^4 c+O(t^5),\quad
 b=-i\,{\cal M}(U)\psi_0/(6T_*),\qquad
 c=\big(Jb-i{\cal M}(U)F_0/(2T_*)\big)/4 .
\]
\({\cal M}\) is the existing projected multiplication, not pointwise multiplication on an enlarged space. The state change orthogonal to \(\psi_0\) removes the arbitrary global phase. For the quadratic wave clock \(Q\), the predicted fourth-order coefficient is \(DQ_{\psi_0}c+DQ_{F_0}b\); the cubic is \(DQ_{\psi_0}b\). Clock differences are evaluated by midpoint polarization rather than subtracting nearly identical full rates. For a local continuum density an instantaneous pure phase cannot change the density. A tiny nonzero cubic in the finite projected clock is reported rather than set to zero. Taylor coefficients of a sharp-shell field need not approximate high-frequency components of the state at finite time: compare radial-spread sources and directly integrated observables before interpreting them.

The absolute wave-kick prescription applies each arm's \(U_a\); the reset-referenced prescription leaves reset unchanged and applies \(U_c-U_r\) in coupled. They give the same leading *ordinary* clock contrast but need not produce identical *wave* responses. Both use the same verified catalogue-nearby ordinary background for this prescribed-curvature test.

### First correction from the measured material motion

For a shared initial velocity \(v\) and the paired wave acceleration \(a=-\nabla d\), use the linear-in-force impulse on the common straight characteristic:
\[
 D(t)=t^2\int_0^1(1-u)\,[a(x+utv)+ut\,\partial_t a(x+utv)]du,\quad
 \delta C(t)=\int dm\,\nabla K_C(x+tv)\cdot D(t).
\]
The time derivative of the wave acceleration is computed from the two saved Schrödinger equations. For a smooth readout the cubic derivative is the sum of \(3(v\cdot\nabla)\nabla K_C\cdot a\) and \(\nabla K_C\cdot[\partial_t a+(v\cdot\nabla)a]\). The gradient of the finite-multipole clock kernel instead jumps at each probe radius; crossing contributions must be evaluated on their correct side. Direct quadrature of the time-displaced readout preserves them. Positive and negative short times are derivative probes around launch, not backwards-measured simulation histories. This test uses the actual saved gas and stellar positions and velocities only on \(5.75\le r<9\) kpc. Do not add it to the full-grid curvature without subtracting the overlapping contribution. It does not simulate the full pressure or momentum-transfer terms.

### Autonomous two-way pilot, separate from the sourced interval

On the isolated gravity branch the common launch potential stays fixed. Add only \(\Phi_o(X)-\Phi_o(X_0)\) to the wave so the original field is not counted twice. The mechanical force is \(-\nabla\Phi_w(\psi)\) on the moving ordinary particles. It is not the spatial derivative of the field at the fixed reference positions. The wave still carries its original kinetic operator and nonlinear wave self-gravity. The matter is cold and initially at rest in this diagnostic. Its evolving self-gravity on *itself*, thermal stress, feedback momentum, and acceleration by the rest of the galaxy are omitted. The two sectors are nonetheless live to *each other*.

Advance by endpoint half kicks/drift with the ordinary force derived above; solve the original implicit nonlinear wave equation with the endpoint-averaged moving potential, then recompute the kick from the updated wave and moved particles. No adjustable energy offset is used. The discrete bilinear product rule splits the interaction change into the part due to moving source and the part due to changing wave density. For each step the former is \(\langle(\rho_{w1}+\rho_{w0})/2,\Phi_{o1}-\Phi_{o0}\rangle\). Compare the accumulated term with minus the change of ordinary kinetic energy, and separately with the change of wave plus interaction energy. Their sum is the total energy residual of this autonomous subsystem. Wave norm conservation alone would not test it.
