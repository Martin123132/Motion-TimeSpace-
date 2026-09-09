# Parent nonlinear motion: characteristic, energy and preparation bounds

Private continuation, 2026-09-08. This derives a quantitative sufficient
extension of the finite-time linear preparation result from the retained
parent interaction. It does not assume nonlinear vacuum preparation.

## 1. Action and normalization, before inserting any coefficient

The selected 5203/5208/5211 action on a fixed static background is

```text
L_chi = -K X/2 - m^2 chi^2/2 + Q(X),
X=g^{mu nu} partial_mu chi partial_nu chi,
K=1+2u_O4 C^2,    Q(0)=Q'(0)=0.
```

Signature is (-,+,+,+); X has NO factor 1/2. The function Q here is precisely
the interaction called P_ge2 in 5211, not the full canonical Lagrangian.
In 5209's homogeneous Lorentzian convention Y=-X and
L=Y/2+sum c_n Y^n, so Q(X)=sum (-1)^n c_n X^n. The quartic coefficient is
unchanged and odd powers change sign. The general absolute-coefficient
envelopes below do not depend on those odd-power signs. The explicit signed
sound-speed control uses the convention and c2 sign stated in 5209.

Fix the renormalization scale when varying the action. Arbitrarily promoting
that scale or its coefficients to position-dependent functions would add
source terms not included here.

The exact retained Euler equation and its principal tensor are

```text
E_chi = nabla_mu[(K-2Q') nabla^mu chi]-m^2 chi=0,
H^{mu nu}=(K-2Q')g^{mu nu}-4Q'' p^mu p^nu,
p_mu=partial_mu chi.
```

Derivatives of K belong to lower-order terms, not to H. The companion
independently differentiates the Lagrangian with respect to all four field
gradients and verifies -L_(p_mu p_nu)=H^{mu nu}.

## 2. A common spacelike slicing and bounded characteristic cone

Use an orthonormal frame attached to the static slices and define
U=p_0^2+sum_i p_i^2. This is a positive norm, not the Lorentz scalar X;
|X|<=U, whereas small |X| alone does NOT control a nearly null gradient.
Assume a classical solution on the finite causal region with U<=U_star,
K>=k0>0 and N<=N_max. Define

```text
D1=sum_(n=2)^N n |b_n| U_star^(n-1),
D2=sum_(n=2)^N n(n-1) |b_n| U_star^(n-2),
D0_over_U=sum_(n=2)^N |b_n| U_star^(n-1),
Q(X)=sum b_n X^n,
eta=(2D1+4U_star D2)/k0.
```

Then ||H-K g^{-1}||_Euclidean,op <= eta K. If eta<1, H has one negative
and three positive eigenvalues, -H^{00}>=K(1-eta), and the original time
slices remain spacelike for the motion principal tensor. Its characteristic
normal speeds obey

```text
c_min^2=(1-eta)/(1+eta),
c_max^2=(1+eta)/(1-eta).
```

This is obtained by applying the perturbation norm to a characteristic
covector (-omega,k): |omega^2-|k|^2|<=eta(omega^2+|k|^2).
The resulting outer cone is a sufficient finite-propagation envelope.
In tortoise coordinates the causal-domain gate becomes
S_initial+c_max t <= S_domain. A compact-support boundary in exact vacuum
can have a sharper speed, but that sharpening is not needed here.

For Q=b2 X^2, the two rest-frame principal factors are
K-4b2 X and K-12b2 X. On a timelike homogeneous gradient Y=-X>0,

```text
c_s^2=(K+4b2 Y)/(K+12b2 Y),
c_s^2-1=-8b2 Y/(K+12b2 Y).
```

Thus a negative b2 can give a slightly wider low-energy characteristic cone.
It must not be rounded to exactly the metric cone or interpreted, by itself,
as either a proof of acausality or a proof of ultraviolet causal completion.

These principal-tensor issues are standard in k-essence. The normalization
here is derived from the MTS action, not copied across different conventions.
See Babichev, Mukhanov and Vikman, [arXiv:0708.0561, section 2](https://arxiv.org/pdf/0708.0561)
(checked 2026-09-08), for the effective-metric and common-Cauchy-slice framework.
No global-causality conclusion for MTS is imported from that paper.

## 3. Nonlinear energy is comparable to the quadratic energy

On this fixed background, the canonical Killing energy density of Q is

```text
Delta e_Q=-2Q' p_0^2-Q.
```

The positive quadratic density is e_K=(K U+m^2 chi^2)/2. Hence, uniformly,

```text
theta=(4D1+2D0_over_U)/k0,
|Delta e_Q| <= theta e_K,
(1-theta)E_K <= E_total <= (1+theta)E_K.
```

For the displayed polynomial, eta>=theta term by term for every n>=2.
Thus eta<1 also guarantees theta<1. With no external force, the full
nonlinear Killing energy is conserved because the background and coefficients
are static. Consequently

```text
sqrt(E_K(t)/E_K(0)) <= R_E=sqrt((1+theta)/(1-theta)).
```

This is not a claim that the complete metric-varied O4 stress is pointwise
positive; the fixed-background energy is the same control norm used in the
previous Hilbert-source estimate.

The extra metric-varied interaction stress is exactly
T_Q,mu nu=-2Q' p_mu p_nu+g_mu nu Q. For a smooth test tensor with frame
operator norm H_op and trace bound H_tr,

```text
|integral sqrt(-g) h^{mu nu} T_Q,mu nu|
 <= (2/k0)[2D1 H_op+D0_over_U H_tr] integral E_K(t) dt.
```

Thus the interaction's own gravitational source is bounded rather than
silently removed. Add this contribution to the already derived canonical
and full O4 smear bounds.

## 4. Compare to the physical linear evolution, not a forced flat surrogate

Let chi_lin solve the retained quadratic equation with the SAME initial
data on the SAME fixed background. Set z=B(chi-chi_lin), B=r sqrt(K), using
the spherical harmonic decomposition only for the linear operator. Then

```text
z_tt+H_K z = F_Q,
z(0)=z_t(0)=0,
F_Q=-2N^2 B/K nabla_mu(Q' nabla^mu chi).
```

The right side is evaluated on the nonlinear field. It is not declared to
be prescribed, small, or independent of its second time derivative.
The positive quadratic energy identity gives directly

```text
sqrt(2E_K[z](t)) <= integral_0^t ||F_Q||_(L2(ds dOmega)) dtau.
```

This comparison avoids an unnecessary free-wave Gronwall exponential on the
nonlinear difference. It also includes every angular mode generated by Q;
the nonlinear solution need not stay inside the initial angular band.

Writing H2(t)=||nabla nabla chi||_(L2(proper spatial volume)), with the
Euclidean frame norm on the four-by-four Hessian, the chain rule gives

```text
nabla_mu(Q' p^mu)=Q' Box chi+2Q'' p^mu p^nu nabla_mu nabla_nu chi,
|Box chi|<=2 |nabla nabla chi|_frame,
||F_Q|| <= [4 N_max^(3/2)/sqrt(k0)](D1+U_star D2) H2(t).
```

The lapse/kinetic factor follows from ds=a dr/N and B=r sqrt(K), not a
flat-space volume substitution. Introduce the actual solution's integrated
regularity budget

```text
B_H = integral_0^t H2(tau)/sqrt(2E_K(tau)) dtau,
zeta_Q = [4 N_max^(3/2)/sqrt(k0)](D1+U_star D2) R_E B_H.
```

The zero-energy solution is treated separately as the exact zero solution.
For nonzero initial energy, zeta_Q bounds the nonlinear error norm relative
to sqrt(E_K(0)). If epsilon_lin is the existing full linear local-energy
fraction, the resulting sufficient nonlinear bound is

```text
E_K,obs[chi](t)/E_K(0)
 <= min(R_E^2, [sqrt(epsilon_lin(t))+zeta_Q]^2).
```

For initial angular tails, use the corresponding weighted low-band/high-band
linear fraction inside epsilon_lin. A spatial remainder is decomposed only
in chi_lin, where superposition is legitimate. Never add two nonlinear
cutoff evolutions as if they superposed. The full difference z already
contains nonlinear mode coupling and coherent source excitation.

A target delta permits the explicit budget

```text
B_H <= [sqrt(delta)-sqrt(epsilon_lin)] /
       {[4 N_max^(3/2)/sqrt(k0)](D1+U_star D2) R_E},
```

provided the numerator is positive and the causal-domain and eta gates hold.
No clipping at 1 is used: E_K is not the exactly conserved nonlinear energy.

### Eliminate the second-time-derivative input with the parent equation

The Hessian budget need not require future acceleration as an independent
datum. In the same orthonormal frame write M=|(Hess chi)_0i| and
S=|(Hess chi)_ij|_F. Solving the principal equation for its 00 component gives

```text
|(Hess chi)_00|
 <= [2 eta M+sqrt(3)(1+eta)S
     +(|grad K| sqrt(U)+m^2 |chi|)/K]/(1-eta),
|Hess chi|_F <= C_M M+C_S S
                +(|grad K| sqrt(U)+m^2|chi|)/[k0(1-eta)],
C_M=sqrt(2)+2eta/(1-eta),
C_S=1+sqrt(3)(1+eta)/(1-eta).
```

Mixed and spatial covariant derivatives are determined by the Cauchy field,
velocity and their spatial derivatives on a static slice. On a finite region
where N>=N_min>0 and |grad K|<=kappa_K, the energy controls the lower terms:

```text
H2/sqrt(2E_K)
 <= [C_M ||(Hess chi)_0i||_2+C_S ||(Hess chi)_ij||_2]/sqrt(2E_K)
    +kappa_K/[sqrt(N_min) k0^(3/2)(1-eta)]
    +m/[sqrt(N_min) k0(1-eta)].
```

For m=0 the last term is zero, not a division by a mass gap. Thus the next
regularity problem is explicitly a propagated spatial/velocity derivative
budget, rather than an unspecified external force or independently chosen
second time derivative. The companion solves the acceleration equation in
both-sign controls and checks this estimate. Propagating these Cauchy norms
from initial data in the coupled system remains necessary.

## 5. Source-owned coefficients and what can be evaluated honestly

At one fixed RG scale k, write b_n=(-1)^n a_n k^(4-4n) in the 5209
Lorentzian-Y convention, and x=U_star/k^4. The envelopes are dimensionless:

```text
D1=sum n |a_n| x^(n-1),
U_star D2=sum n(n-1)|a_n| x^(n-1),
eta=sum 2n(2n-1)|a_n| x^(n-1)/k0,
theta=sum (4n+2)|a_n| x^(n-1)/k0.
```

The companion reads the actual 4958 N=6 and N=8 endpoints in BOTH schemes,
checks the 5209 source-lock hash, and uses their stored a2,...,aN. No new
coefficient fit or regeneration of the historical trajectory is needed.
It evaluates 0<x<=0.1, the declared local-polynomial range. Using the positive
frame norm U, rather than only the Lorentz invariant |X|, is an additional
restriction necessary for the principal-tensor bound.

This is a resolved finite-polynomial result at its stored massless endpoint,
not a bound on every uncomputed higher-order term or every RG scale. 5209
records the finite-mass/control-domain separation; one cannot take k~m_gap
and declare the full local polynomial valid at a huge gradient. The weak-star
reference and illustrative k0 envelopes are not a joint physical matching of
all dimensional coefficients and a measured star. All physical claim flags
remain false.

## 6. Metric backreaction: the exact additional source is identifiable

For an actual metric g and the static comparison metric g0, let K and K0
be their respective curvature-dependent kinetic factors. Using the g0
connection, define

```text
A^{mu nu}=K g^{mu nu}-K0 g0^{mu nu},
B^nu=g^{mu nu} partial_mu K-g0^{mu nu} partial_mu K0
     -K g^{alpha beta}(Gamma[g]^nu_ab-Gamma[g0]^nu_ab).
```

Then L_g-L_g0=A^{mu nu} nabla0_mu nabla0_nu+B^nu partial_nu for
L_g=div_g(K grad_g)-m^2. In the comparison wave equation the geometry source
is +(N0^2 B0/K0)(A:Hess0 chi+B^nu p_nu), while the nonlinear source uses
-2(N0^2 B0/K0)div_g(Q' grad_g chi). This identity does not omit connection
or kinetic-gradient terms.

For finite frame bounds A_star,B_star, the geometry source satisfies

```text
||F_geometry|| <= N0_max^(3/2)/sqrt(k0)
                 [A_star ||Hess0 chi||_2+B_star ||grad chi||_2].
```

Its integrated norm adds to the difference estimate. However, the fixed-g
Killing-energy conservation argument must NOT be reused when g evolves.
Deriving bounds on A, B and the metric work term from the coupled equations
is an additional task, not accomplished by writing this exact identity.

## 7. The condition that has not been smuggled in

A small U_star does not imply a small B_H. For example a compactly enveloped
field (epsilon/omega) cos(omega r) can keep its first gradient bounded while
its Hessian grows with omega. The companion includes this negative control.
Thus the result is a sufficient/a-posteriori estimate for a classical solution
with verified gradient and regularity budgets, not a proof of global smooth
existence or of those budgets from arbitrary initial data. EFT momentum
control and a coupled higher-regularity energy estimate are needed to close
that remaining step. Quantum-state preparation is also not supplied by this
classical argument.

Local sources: 5203 canonical action; 5208 selected trajectory; 5209 finite-mass
P(X) gate and source_provenance.csv; 5211 local truncation;
source-intake/functional_rg/4958/essential_functional_GR_trajectory.csv;
DERIVATION-20260908-finite-time-causal-escape-and-forcing.md and its executed
finite-time-initial/result.json. Exact paths and hashes are retained by the
companion, scripts/parent_nonlinear_motion_comparison_20260908.py.
