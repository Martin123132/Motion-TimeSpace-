# Physical cold norm, clock mean and controlled remainder

## 1. The norm follows the retained cold-fluid coordinates
In the inherited physical-energy coordinates a cold-fluid density contrast carries weight sqrt(rho) H/k.
The heavy relative variables (delta,W) did not yet carry that weight. Thus define
h=sqrt(rho_h) H/k and D=diag(h,h,1,...), with the two h entries at the heavy slots, not necessarily the start of the array.
This positive quadratic norm has the same physical units as the other matter coordinates; it is an energy-type norm, not a claim that an arbitrary perturbation's conserved Hamiltonian is positive.
The baseline has no heavy block and D=I.

This normalization does not change an observable or erase growth. For example, density contrast is recovered by division by h, which changes during expansion. All physical readouts need the inverse endpoint map.

Let zeta_N=B zeta be the previously derived fully coupled scalar/matter/metric system. For u=D zeta,
A=D B D^-1+D_N D^-1.
The derivative term must be retained:
h_N/h=eta0-1/2+(3/2+b)cos(2theta),
using rho_h,N=(-1+3cos(2theta))rho_h and H_N/H=eta0+b cos(2theta).
Consequently one cannot just rescale the old averaged matrix and ignore this connection.

## 2. Clock mean and its primitive
The physical phase clock is theta_N=omega=mu-(3/2)sin(2theta).
Its weighted cosine average is zero over a half-turn. At fixed slow state,
Abar=D Bbar D^-1+(eta0-1/2)P_h.
The energy-coordinate primitive is independently
C=D Q D^-1+q_gamma P_h,
where
q_gamma=-(3/2+b)/3 log[1-(3/(2mu))sin(2theta)]
with its angle mean subtracted.
Use log1p numerically: mu is about2.8e8 at this cold midpoint.
These exact formulas independently check the sampled Fourier primitive; they are not fitted to it.

For u=(I+C)chi the exact transformed equation is
chi_N=(Abar+E)chi,
E=(I+C)^-1[A C-C Abar-D_sigma C f].
The physical slow flow is f=f0+cos(2theta)fc. Its gamma connection and primitive drift are both included.

## 3. Why rapid streaming does not force a huge growth bound
For x_N=A x, d||x||/dN <= mu_2(A)||x||, where mu_2 is the largest eigenvalue of (A+A^T)/2.
The massive-neutrino remote-tail streaming entries in the retained energy weights are opposites:
k v/H times ell/sqrt[(2ell+1)(2ell-1)] and its negative.
They cancel in the symmetric part. The retained tail diagonal is -(3-v²)/2.
Thus the full G192 logarithmic norm reduces to the core/first-tail symmetric block and the remote-tail diagonal maximum; it is not proportional to the largest free-streaming frequency.

The phase-dependent primitive has support only on the core and the ell=3 boundary. Multiplication by the nearest-neighbour streaming generator extends its remainder support through ell=4, not through the entire hierarchy. This support statement does not truncate the evolved G192 hierarchy.

## 4. Controlled transfer statement, with endpoints
Suppose ALONG THE ACTUAL PATH that mu_2(Abar)<=g, ||E||<=e and ||C||<=q<1.
Using the identical initial state and both periodic endpoint maps,
||u_exact-u_approx||/||u_initial||
<= (1+q)/(1-q) exp(g DeltaN) [exp(e DeltaN)-1].
This follows from variation of constants and the logarithmic-norm inequality.
The original variables require D_final^-1 and the retained S/physical-readout maps. No density-contrast bound may be quoted without those conversions.

A midpoint value of g,e,q is not proof of these pathwise hypotheses. Likewise, a rigorous bound for the retained Fourier polynomials is not automatically a bound for their unsampled analytic remainder. Numerical refinements and independent native checks are retained as evidence, with those scopes separated.

## 5. Finite-polynomial bound without throwing away stiff commutator cancellation
For Fourier A_j,C_j,d_j, form A C-C Abar-d. Keep the central contribution A_0 C_j-C_j Abar as a commutator-like difference before taking norms.
Convolve active harmonics|j|<=8 explicitly. Bound all remaining finite-polynomial coefficients by norm sums:
tail_A*sum_C+(active_A+||Abar||)*tail_C+tail_d.
Divide the resulting numerator bound by1-sum||C_j||.
This bounds every phase of those finite polynomials; it is not just the largest sampled phase.

## 6. Physical history and remaining calculation
All numerical inputs come from the sealed cold coupled-coefficient stage and the accepted saved cold background, not a new cosmology fit.
No late perturbation preparation or microscopic phase is invented.
After the local remainder is qualified, extend/control these constants over the saved coefficient path and include the saved background uncertainty. Only then use the transport statement for the retained early preparation and matched GR/spatial-Poisson comparisons.
