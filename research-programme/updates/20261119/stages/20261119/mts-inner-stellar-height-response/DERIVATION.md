# A fixed-column gravity test and the energy available to the odd field

## Which part of the parent is tested?

Take the already-retained nonrelativistic massive bath in its weak, common Newtonian metric. In the inherited wave units its energy variation gives the Schrödinger kinetic term, ordinary potential times density, and the Newton self-energy with its factor 1/2. Varying that self-energy gives the full Poisson potential, not half of it. No external-galaxy occupation or coupling is calibrated here. The reference is the saved Milky Way stationary ground state in the measured-population foreground; the even counter-rotating density and the spherical NFW halo are comparison states. “Matched” means one outer circular speed, not a fit across dynamical data. A separate fixed-number/amplitude calculation does not enforce that speed on the changed source.

## How a changing thickness contributes to gravity

For a living thin-star column \(\Sigma_t(R)\), take \(p_h=e^{-|z|/h}/(2h)\). The imposed perturbation is exactly \(\delta\rho=\Sigma_t[p_{h'}-p_h]\). It integrates to zero at each radius (and at each azimuth in the sector experiment). At fixed density source the three-dimensional potential is \(-G\int\delta\rho/|\mathbf x-\mathbf x'|\,d^3x'\). The wedge force is computed in actual sectors; this is not the force of their mean scale height. The nonlinear axisymmetric wave sees the azimuthally averaged **density** for the sector-average variant. The odd-harmonic experiment instead solves for the linear response to the cosine and sine parts separately.

The symmetric exponential has \(\langle z^2\rangle=2h^2\). Since \(r^2 P_2=z^2-R^2/2\), the axisymmetric exterior quadrupole change is \(\int dA\,2\Sigma_t(h'^2-h^2)\). The azimuthal dipole vanishes at fixed column. In the real mirror-even \(m=1\) basis used by the code, \(r^3 B_{31}=-(3/2)\sqrt{7/12}\,R(4z^2-R^2)\) before the normalized sine/cosine factor. The terms constant in z cancel and the exterior octupole follows from the same second vertical moment weighted by R and the azimuthal harmonic. The exterior field computation and these direct integrals agree (see exterior-moments.csv). Neither identity implies a zero force inside the disk.

For a stationary wave \(u\), project the differentiated eigen-equation onto the complement of \(u\) before inverting the static Hessian. At fixed number \(\langle u,\delta u\rangle=0\). At fixed outer speed, add the already-derived derivative with respect to log particle number times the unique shift cancelling the total outer radial-force change. Freeze this tangent before the nonlinear solve. The NFW control uses the ordinary-force change plus, on its matched branch only, the normalization change required by exactly the same speed.

## Collective response is not a freely chosen occupation

Write the perturbed wave as \(e^{-i\epsilon_0 t}(u+a+i b)\). For a real spatial shape whose amplitude is \(s(t)\), projection onto the equatorially even \(|m|=1\) sector gives
\[
 \dot a=L_- b,\qquad -\dot b=L_+ a+s J,\qquad
 L_-=H_1-\epsilon_0,\quad L_+a=L_-a+2\Pi[uP_1(ua)],\quad J=\Pi(u\,\delta U_1).
\]
\(P_1\) is the self-gravitating Poisson solve with isolated exterior; the factor two is from the density variation. \(m=1\) perturbations are orthogonal to the ground state without a number multiplier. Setting \(L_+=L_-\) gives the frozen-potential comparison; the self-consistent static answer is \(a=-L_+^{-1}J\). These displacements are coherent: a squared displacement is not evidence for an incoherent halo population. Because only one azimuthal wedge was measured, completing the other side with a copy rotated by \(\pi\) preserves the observations but kills **all** odd forcing.

For \(L_-=CC^T\) put \(a=Cy\); then \(\ddot y+C^TL_+Cy=-s C^TJ\). In one normal coordinate the energy in excess of final equilibrium is \(\dot q^2+\omega^2(q+F/\omega^2)^2\), in the real-wave energy normalization. With initially unperturbed state and one monotone buildup from 0 to 1,
\[
 E_{\rm free}=\sum_j\frac{|F_j|^2}{\omega_j^2}\left|\int e^{i\omega_j t} ds(t)\right|^2
 \le J^TL_+^{-1}J .
\]
Equality for a sudden switch; no adiabaticity assumption is needed. This is not a bound on repeated passages, a rotating pattern, an incoming wave, multiple evolving shapes, or energy imparted during the galaxy's entire lifetime. The inherited factor \(v_{\rm unit}^2/N\) converts to physical energy per unit wave mass. The comparison \(0.01(\epsilon_1-\epsilon_0)\) is the initial energy slope for one percent transfer in the frozen background, **not** a claimed nonlinear threshold for creating a real galaxy population.

A floor \(L_+\succeq cI>0\) gives the conservative bound \(\|u\,\delta U_1\|^2/c\), using the full quadrature norm before state-basis projection. An approximate smallest Ritz value is not itself a lower bound. The independent matrix construction in coercivity.py uses \(L_+=L_--\sum_\ell B_\ell B_\ell^T\). Each \(B_\ell\) is the overlap of the product of the ground wave and wave basis with the isolated Poisson basis, multiplied by \(\sqrt{2}\,r_{\rm edge}/k_{\ell n}\) for its dimensionless roots. It checks matrix action against the matrix-free operator and factors \(L_+-0.30 I\). The saved factorization allowance uses \(\gamma_{n+1}\|L\|_1\|L\|_\infty\) for the shifted Cholesky factor. For an approximate static solution \(a\), the quadratic value \(-2J^Ta-a^TL_+a\) underestimates the exact compliance by \((J+L_+a)^TL_+^{-1}(J+L_+a)\), bounded by the squared defect divided by the floor. These are numerical statements about the assembled finite model, not interval bounds on source extraction or a proof for unrepresented continuum modes.

## What if the same asymmetry rotates?

The monotone result alone does not answer this objection. For the same spatial template changing orientation and amplitude, every cosine/sine drive doublet takes the form A(t) R(theta) F, with R an orthogonal rotation. This uses the axisymmetric background; it does not require measuring the far side. Between drive increments free propagation preserves the quadratic energy norm. Applying the triangle inequality to the rotated increments gives

    sqrt(E_free) <= sqrt(S) V,      V = integral sqrt(dA² + A² dtheta²).

S is the sudden-switch energy of the template or its larger validated ceiling. Include jumps by their path length and start with an unexcited field. The two tangent vectors RF and R'F are perpendicular and equally long in every doublet. Thus V is shared by all frequencies; a pattern speed need not be selected. One rise to unit amplitude and n turns at that amplitude gives V=1+2πn. For the tested fine model even reaching the reference energy requires V at least 2645.2, or at least 420.84 such turns. This necessary bound says nothing about a different source, a pre-excited field or a far larger past amplitude.

For a sudden rise followed by uniform rotation at Ω, let I(k,T)=T exp(ikT/2) sinc(kT/2), with sinc(x)=sin(x)/x. Each doublet's free energy relative to its step value is (|1+iΩ I(ω+Ω,T)|² + |1−iΩ I(ω−Ω,T)|²)/2. At fundamental resonance for n whole periods this is 1+2π²n² for that doublet. Direct quadrature checks the formula at four saved frequencies. This synthetic control favors excitation; it is not a measured pattern speed, duration or formation mechanism.

## An inverse test that does not choose a halo profile

At height z the magnitude of vertical gravity from a **spherical**, nonnegative extra density is \(G M(<r) |z|/r^3\), \(r^2=R^2+z^2\). Subtract the same signed ordinary gravity from each SEGUE force; infer a required mass and its printed width for each row, with no parametric halo fit. Add nonnegative origin, the same outer speed, and optionally the Gaia radial intervals. At each ordered radius take the maximum over all preceding lower mass bounds. There exists a nondecreasing enclosed mass exactly when this prefix maximum does not exceed the local upper bound (combine equal radii). Thus for intervals \([l_i-tw_i,u_i+tw_i]\) the least common expansion is the positive part of \(\max_{r_i\le r_j}(l_i-u_j)/(w_i+w_j)\); zero-width pairs must already be compatible. The independent audit obtains the same values by monotone feasibility and bisection. This is a consistency diagnostic for spherical residual gravity at a fixed ordinary source, not a Gaussian significance, an inferred negative density, or a restriction on arbitrary flattened mass.
