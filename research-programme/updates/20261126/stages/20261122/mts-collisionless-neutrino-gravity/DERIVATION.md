# From the geodesic law to the gravity sources

## Conventions and inputs
This is a conditional GR matter calculation *within* the retained common-metric branch. Minimal metric coupling and a freely propagating thermal neutrino distribution are inputs, not newly derived MTS constants. Linear scalar gauge/hierarchy conventions: [Ma & Bertschinger (1995)](https://arxiv.org/abs/astro-ph/9506072); compare the second-order kinetic framework of [Pitrou (2008/2009)](https://arxiv.org/abs/0809.3036). The signed sums, direct massive source, boost matching, preparation changes, and cold/heavy response below are computed for this project. No independent vector, tensor, isocurvature, or primordial second-order mode has been supplied. The Fourier panel contains the retained long–short couplings, not all pairs in the Universe.

Use conformal Newtonian scalar metric
\(ds^2=a^2[-e^{2A}d\eta^2+e^{2B}d{\bf x}^2]\);
\(A=\psi+\psi_2-\psi^2,\ B=-\phi-\phi_2-\phi^2\) through second order (no factorial on the order-two coefficient). With normal-frame momentum \(q=a|{\bf p}_{phys}|,\ \epsilon=(q^2+a^2m^2)^{1/2},\ v=q/\epsilon\), write \(\delta f=W\Theta,\ W=-q f'_0,\ w=\partial_{\ln q}\ln W\). Thermal \(q\) in the code is in present neutrino-temperature units, and \(m\) in the matching units. Let \(n\) be the propagation direction, \(P_n=1-nn^T\). Hamilton's equations for covariant momenta \(p_i=e^B q n_i\) give
\[
{\bf x}'=e^{A-B}v n,\quad (\ln q)'=-B'-e^{A-B}n\cdot\nabla A/v,\quad
 n'=-e^{A-B}P_n(\nabla A/v-v\nabla B).
\]
For a collisionless species the derivative of \(f\) along this trajectory vanishes. Subtract the first-order equation and the linear action of the second-order metric \(\phi_2'-n\cdot\nabla\psi_2/v\). With \(G=\phi+\psi\) the remaining source of \(\Theta^{(2)}\) is
\[
2\phi\phi'+n\cdot(\nabla\psi^2-G\nabla\psi)/v
-vG\,n\cdot\nabla\Theta+
P_n(\nabla\psi/v+v\nabla\phi)\cdot\nabla_n\Theta+
(-\phi'+n\cdot\nabla\psi/v)(\partial_{\ln q}\Theta+w\Theta).
\]
Here \(\Theta\) on the right is first order. For an FD distribution \(w=1-q\tanh(q/2)\). Only *after energy weighting* in the massless case does integration by parts replace \(w\) by \(-4\). For a massive species the momentum-dependent speed and shape derivative must stay inside the integral.

## What the first-order distribution is
Expand \(\Theta(n)=\sum_l(-i)^l(2l+1)\Theta_lP_l(n\cdot\hat k)\). For \(U=\Theta-\phi\), the Fourier streaming equation has forcing \(-ik\mu(v\phi+\psi/v)\). Its retarded solution uses \(j_l(k\int v\,d\eta)\) for the incoming low moments and \(k(v\phi+\psi/v)j'_l\) under the time integral. Differentiate both the source amplitude and the comoving travel distance with respect to \(\ln q\); in particular \(d v/d\ln q=v(1-v^2)\). Start from the early regular linear thermal state with the native low angular moments and negligible higher moments; test moving that early surface and thinning the stored first-order metric. This does not specify the second-order incident state. The independent high-angular native calculations, including massive density, momentum and shear, are in the two independent-incident tables.

## How the gravitational source is counted only once
The retained stress already includes the velocity-squared part \(4e_r S(V_r,V_r)/3+(\rho_m+p_m)S(V_m,V_m)\) in its own scalar projection and background units. Taylor-expand an isotropic distribution under a small boost \(\beta\):
\(q'/q=1-n\cdot\beta/v+\beta^2/(2v^2)+(1-v^{-2})(n\cdot\beta)^2/2\).
The coefficient multiplying \((n\cdot\beta)^2\) in \(\delta f/W\) is \((1-w/2)/v^2-1/2\). The normal quadrupole corresponding to the existing bulk is
\[
 C_2(q)=-\tfrac{2}{15}[(1-w/2)/v^2-1/2] S(V,V)
\]
in the saved \(S\) convention (massless energy-integrated \(C_2=-S/3\)). The solver variable is the total normal moment minus \(C_2\) in the quadrupole alone. Thus the streaming equation adds \(L[C]-C'\): \(-2kv C_2/3\) in \(l=1\), \(-C_2'\) in \(l=2\), \(3kv C_2/7\) in \(l=3\). The original linear metric force, velocity-squared stress, and photon response are not added again. Direct integral of the massive boost reproduces its independently retained bulk stress (boost-normalization.csv).

## Independent energy and momentum test
Write \(\rho,J_i,P_{ij}\) for physical normal-frame density, flux and stress, \(\Pi=P_{ii}\), \({\cal H}=a'/a\). With vanishing shift the time and spatial components of \(\nabla_\mu T^\mu{}_\nu=0\) give
\[
 \rho'+({\cal H}+B')(3\rho+\Pi)+e^{A-B}[\partial_i J_i+2\partial_i(A+B)J_i]=0 ,
\]
\[
 J_i'+4({\cal H}+B')J_i+e^{A-B}[\partial_jP_{ij}+
 (\rho\delta_{ij}+P_{ij})\partial_j A+(3P_{ij}-\Pi\delta_{ij})\partial_j B]=0 .
\]
For example the densitized spatial momentum is \(a^4e^{4B}J_i\). These are independent of the angular hierarchy projection. The quadratic energy driving term is \((3\rho_1+\Pi_1)\phi'+6(\rho_0+p_0)\phi\phi'-G\partial_iJ_{1i}-2\partial_i(\psi-\phi)J_{1i}\). For momentum take the quadratic part of the second equation, using \(J_{1i}=-i\hat p_i j\) and \(P_{1ij}=\Pi_1\delta_{ij}/3-s(\hat p_i\hat p_j-\delta_{ij}/3)\). Multiply all source terms by the same background conversion factor used by the parent. The explicit streaming and homogeneous dilution are common to both sides of this *source* comparison. Compare to the zeroth and first moments of the independently projected geodesic driver, integrated against \(W q^2\epsilon\) and \(Wq^3\); no fitted scale or longitudinal projection adjustment. Omitting the lapse/spatial flux-gradient term or the spatial-metric/shear contraction is a negative control. This tests collisionless scalar energy and longitudinal momentum transfer; it is distinct from testing exact energy balance of every retained species.

## Finite incident history and readout
The predeclared 16- and 32-cell windows are on an independently sampled **first-order** native metric ending at the main launch. Over each window evolve the normal second-order moments with the quadratic source above, free streaming, and the earlier surface's instantaneous boosted quadrupole. A second-order metric particular solution prior to the join is not included. At the join subtract that window's closing bulk. Save also the induced density and flux but do not inject them into a launch constrained to keep total density and momentum fixed. Compare added quadrupole alone, added higher moments alone, and both on top of the full main-window coupled solution. Higher moments cannot change initial density, flux or shear, but can stream into the quadrupole later. The two preparations are controlled finite-window alternatives, not rigorous bounds over possible incoming states.

For each final nonzero complex scalar \(O\) report \(|O_{test}-O_{ref}|/|O_{ref}|\) on each probe. The lapse is \(\psi\), and the scalar Weyl potential is \((\phi+\psi)/2\). A refinement error on an increment is distinguished from the size of that increment relative to the original final perturbation; see the per-probe CSVs.
