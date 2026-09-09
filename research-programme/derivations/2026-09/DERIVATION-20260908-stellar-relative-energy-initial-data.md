# Stellar relative energy: replace the unknown nonlinear Hessian budget

Private continuation, 2026-09-08. This is a new comparison argument, not an
edit to the frozen nonlinear comparison. It derives an initial-data budget
for the **linear reference**, then removes derivatives of the actual
nonlinear solution from the comparison estimate. It does not prove that
arbitrary nonlinear initial data remain on the admissible kinetic branch.

## 1. Retained parent and physical surface

Use the same fixed-scale, fixed static background action as 5203/5208/5211:

```text
ds^2=-N^2 dt^2+h_ij dx^i dx^j,
L=-K X/2-m^2 chi^2/2+Q(X),  X=-v^2+|d|_h^2,
v=chi_t/N, d=D chi, K=1+2u_O4 C^2, Q=sum_(n>=2) b_n X^n.
```

All coefficients and the metric are time independent. The domain contains
the causal support up to T, with N_min>0, K>=k0>0. There is no flux through
the outer boundary before T. No cosmological-horizon constant is substituted
for this finite-domain lower lapse bound.

At the static material surface require continuity of chi, its time and
tangential derivatives, and the normal flux N(K-2Q') d_n. For the selected
smooth material star, rho=rho'=0 at the surface, but rho'' can jump. K and
its first derivative are continuous, with bounded piecewise second
derivatives. Do NOT replace that star by a globally smooth density profile.

The quadratic reference has continuous normal derivative because its
coefficients are continuous and its linear conormal flux is continuous.
Consequently its nonlinear conormal flux is also continuous. A kinetic
coefficient with a VALUE jump would not have this property; in that case
the reference defect below includes a surface distribution. Such a jump
is explicitly excluded, not discarded during integration by parts.

## 2. Partial Legendre transform and a convex domain

Let Pi=(K-2Q')v and e=Pi v-L. Then

```text
e_Pi=v, e_d=(K-2Q')d, e_chi=m^2 chi,
Pi_t=div_h(N e_d)-N e_chi,
d_t=D(N e_Pi), chi_t=N e_Pi.
```

The conserved Hamiltonian is integral sqrt(h) N e. Write the derivative
variables in energy units w=(Pi/sqrt(K), sqrt(K)d). This is a static,
position-dependent change of variables; it does not commute freely with
spatial derivatives. Conjugating the canonical skew-adjoint operator by
this change retains all its derivatives of K, frame and lapse.

Use the previous bounds D1, D2, eta=(2D1+4U_*D2)/k0<1, and define

```text
eps=2D1/k0, ell=(1+eta)/(1-eta),
h0=(1-eta)/(1+eta)^2, h1=1/h0.
```

A sufficient convex canonical domain at every point is

```text
|w|^2 <= k0 (1-eps)^2 U_*.
```

It guarantees a unique inverse v(Pi,d) inside v^2+|d|^2<=U_*. Indeed, at
fixed d the derivative of Pi with respect to v is a=-H^{00}>=K(1-eta),
and its two endpoint values bracket the specified Pi. The displayed ball
is contained in the corresponding endpoint ellipsoid. Line segments in
this ball stay inside it; this matters for Taylor's theorem.

Set b=L_vd, C=-L_dd=H_spatial. The Hamiltonian Hessian is exactly

```text
delta^2 e=(delta Pi-b.delta d)^2/a+delta d.C.delta d+m^2 delta chi^2.
```

Since a/K in [1-eta,1+eta], |b|/K<=eta and C/K lies between
(1-eta)I and (1+eta)I, shear factorization gives

```text
h0 |delta w|^2+m^2 delta chi^2
 <= delta^2 e <= h1 |delta w|^2+m^2 delta chi^2.
```

This is a finite-domain convexity statement, not global convexity of a
finite P(X) polynomial. The inverse velocity-gradient map obeys
sqrt(K)|delta(v,d)| <= ell |delta w| along the segment.

For D3=sum n(n-1)(n-2)|b_n|U_*^(n-3), define

```text
T3=12D2 sqrt(U_*)+8D3 U_*^(3/2),
M3=T3 ell^3/k0^(3/2).
```

The chain rule gives ||D^3 L||<=T3 in physical (v,d) variables. Under the
partial Legendre transform its third variation is minus D^3 L evaluated
on the three lifted directions (delta v,delta d), where
delta v=(delta Pi-b.delta d)/a. Thus ||e_www||<=M3. The potential is
quadratic and has no third derivative. These bounds include both signs
of the parent coefficients and all retained polynomial orders.

## 3. Exact relative-energy identity

Let bar-chi be the solution of the **physical quadratic** stellar equation
with the same initial chi and v as the nonlinear solution. Define its
canonical state using the nonlinear map, not Pi=K bar-v:

```text
bar-Pi=(K-2Q'(bar-X))bar-v,
R_Pi=bar-Pi_t-div_h[N(K-2Q'(bar-X))bar-d]+Nm^2 bar-chi
    =2N div_g(Q'(bar-X) grad_g bar-chi).
```

Its d and chi evolution have zero defect. In particular the two canonical
states coincide initially: relative energy is exactly zero, not O(Q).

Let q=(w,chi), r=(bar-w,bar-chi), and H=integral sqrt(h) N e. Define

```text
E_rel=integral sqrt(h) N [e(q)-e(r)-e'(r).(q-r)].
```

For a static skew-adjoint Hamiltonian operator J, q_t=J H'(q) and
r_t=J H'(r)+R. Direct differentiation and integration by parts give

```text
dE_rel/dt = integral sqrt(h) N {
 r_t.[e'(q)-e'(r)-e''(r)(q-r)] - R.[e'(q)-e'(r)] }.
```

R in this formula is transformed to the same coordinates as q. Its only
nonzero contribution is equivalently -N R_Pi(v-bar-v) before normalizing.
Static spatial variation of K and the metric creates no omitted work term.
At the surface the integration-by-parts pairings cancel by continuity of
time derivatives and the physical fluxes. At the regular center the area
factor and smooth Cartesian field remove an artificial inner boundary.

Taylor's integral remainder and convexity yield

```text
a_ref(t)=(M3/h0)||bar-w_t||_infinity,
Y=sqrt(2E_rel),
Y' <= (a_ref/2)Y + ell/sqrt(k0 h0) ||sqrt(N) R_Pi||_2.
```

There is no Hessian of the actual nonlinear solution on the right side.
This is the useful cancellation: differentiating the nonlinear difference
as an external force was demanding more regularity than this norm needs.

The reference defect satisfies

```text
||sqrt(N) R_Pi||_2
 <= 4N_max^(3/2)(D1+U_*D2) ||Hess bar-chi||_2.
```

The L2 Hessian norm uses proper spatial volume and the positive frame norm.
Combining the integrated inequality with E_K[chi-bar-chi]<=ell^2 E_rel/h0
and conservation E_K[bar-chi]=E0 gives

```text
C0=4N_max^(3/2)(D1+U_*D2)/sqrt(k0),
zeta_rel(t)=C0 ell^2/h0 integral_0^t
 exp[0.5 integral_tau^t a_ref(s) ds]
 ||Hess bar-chi(tau)||_2/sqrt(2E0) dtau,

E_K,obs[chi](t)/E0 <= [sqrt(epsilon_lin(t))+zeta_rel(t)]^2.
```

The previous energy comparison can additionally cap the result by R_E^2
while the admissible branch holds. It is NOT clipped at one. The existing
linear angular/spatial-tail rules still apply to epsilon_lin, not by
superposing nonlinear evolutions. For Q=0, C0=M3=zeta_rel=0 exactly.

For bounded reference budgets B2 and M_t, put
Hess_L2/sqrt(2E0)<=B2 and ||bar-w_t||_infinity<=M_t. Then

```text
zeta_rel <= C0 ell^2/h0 B2 T exprel[(M3 M_t/2h0)T],
exprel(z)=(exp(z)-1)/z, exprel(0)=1.
```

The next sections derive B2 and M_t from initial quadratic graph energies.
The estimate applies to classical solutions in the convex domain. A weak
solution extension would additionally require the correct Hamiltonian
inequality, trace/defect justification and existence; none is assumed here.

## 4. Initial graph energies retain the actual interface

Write f_j=partial_t^j bar-chi and E_j=E_K[f_j](0). Time differentiation
commutes with the fixed physical operator and with the static transmission
conditions. Therefore E_j(t)=E_j(0), for j=0,1,2,3, whenever the initial
operator-domain compatibility holds. Compute higher initial time derivatives
recursively from f_(j+2)=L_sp f_j, not from a later solution or a fit.

This is a real restriction: an arbitrary globally smooth function crossing
the surface need not belong to the higher transmission-operator domain.
Compact smooth data supported away from the material surface give a
nonempty compatible class. Piecewise compatible data are also allowed.
Do not differentiate K three times across its second-derivative jump.

For Cartesian derivatives, let

```text
bar-chi_tt=A^ij partial_ij bar-chi+B^i partial_i bar-chi-c bar-chi,
A=N^2 h^{-1},
B^j=N^2/(N K sqrt(h)) partial_i(N K sqrt(h) h^ij),
c=N^2 m^2/K.
```

Assume bounded coefficients on the support and

```text
eps_A=sup|A-I|_F<1, gap=1-eps_A,
A1=sup|partial A|_F, B0=sup|B|, B1=sup|partial B|_F,
c0=sup|c|, c1=sup|partial c|,
ct=inf(K sqrt(h)/N),
cs=inf[N K sqrt(h) lambda_min(h^{-1})].
```

The epsilon_A gate is a sufficient weak-geometry perturbation method, NOT
a necessary condition for elliptic regularity. Failure of that gate is
reported as an unavailable estimate, not an unstable star.

For compact support in a Cartesian ball of radius R_domain, set P=R_domain/pi.
Define bounds on unweighted Euclidean L2 derivative norms:

```text
L1_j=sqrt(2E_j/cs),
L0_j=P L1_j
      (also take min with sqrt(2E_(j-1)/ct) when j>=1),
L2_j=[sqrt(2E_(j+1)/ct)+B0 L1_j+c0 L0_j]/gap,
L3_j=[sqrt(2E_(j+2)/cs)+(A1+B0)L2_j
       +(B1+c0)L1_j+c1 L0_j]/gap.
```

Proof: ||partial^2 f||_2=||Delta f||_2 by Fourier transform. Absorb
(I-A):partial^2 f using eps_A<1. Differentiate this equation ONCE and
repeat the same absorption for the vector gradient. B is Lipschitz for
the selected C1,1 kinetic coefficient; its weak first derivative contains
no surface delta. Only A1 and B1 enter. This avoids the invalid global
third derivative of K. The Poincare constant is the first Dirichlet
eigenvalue pi^2/R_domain^2 of a three-dimensional ball.

For any positive inverse length mu, Fourier Cauchy-Schwarz gives exactly

```text
||f||_infinity <= (8 pi mu)^(-1/2)(mu^2||f||_2+||partial^2 f||_2),
||partial f||_infinity
 <= (8 pi mu)^(-1/2)(mu^2||partial f||_2+||partial^3 f||_2).
```

Here integral_R3 (mu^2+|xi|^2)^(-2) dxi=pi^2/mu. These explicit constants
replace an unspecified Sobolev constant. Let F_j and G_j denote the two
right sides using L0_j,L2_j and L1_j,L3_j. Then

```text
U_ref <= (F_1/N_min)^2+lambda_max(h^{-1}) G_0^2,
M_t <= sqrt(K_max)(1+eta)
       sqrt[(F_2/N_min)^2+lambda_max(h^{-1}) G_1^2].
```

Thus E0 through E3 determine the reference pointwise derivative bound.
E0 through E2 suffice for its gradient bound. Check the stricter canonical
ball as well: K_max(1+eps)^2 U_ref<=k0(1-eps)^2 U_* is sufficient.
Compact support and a hard frequency cutoff are not imposed together.

## 5. Convert the linear Hessian budget to the same physical norm

An economical alternative to Cartesian Christoffel bounds is the spatial
Bochner identity. Let a_*=sup|D log N|, kappa_K=sup|D K|, and let
Ric_h>=-R_minus h. On the regular whole star, with no external boundary
flux, ||D^2 f||_2<=||Delta_h f||_2+sqrt(R_minus)||Df||_2.
The linear equation and its conserved time-commuted energy give

```text
B2=C1 sqrt(E1/E0)+C2,
C1=2sqrt(N_max)/(sqrt(k0) N_min^2)
   +sqrt(2)/(sqrt(k0) N_min^(3/2)),
C2=[(2+sqrt(2))a_*+kappa_K/k0+sqrt(R_minus)]/sqrt(N_min k0)
   +m/(k0 sqrt(N_min)).
```

For m=0 the last term is zero. The proof uses Hess_00=f_2/N^2-a.Df_0,
Hess_0i=D_i f_1/N-a_i f_1/N and the spatial Bochner identity, bounding the
full Frobenius norm by |Hess_00|+sqrt(2)|Hess_0i|+|Hess_ij|_F.
No surface curvature distribution exists for this C2 spatial metric.
In the selected spherical chart the Ricci eigenvalues are -f'/r and
(1-f-r f'/2)/r^2. For f=1-2M(r)/r-H^2r^2, a safe negative bound is
R_minus=2d0, d0=4pi rho_c/3, since rho,H^2>=0 and M/r^3<=d0.

## 6. Explicit stellar coefficient envelopes

Use the previous finite-time proof's d0, fmin, Nmin, g, f1, n1, k0, k1,
k2 and h2, where |f'|<=f1 r, |(log N)'|<=n1 r, |K'|<=k1 r,
|K''|<=k2. Let L=R_domain=4R and z0=2d0+H^2. The companion reproduces
these analytic quantities from the FROZEN numerical reference profiles;
it does not refit or rerun their TOV integrations.

```text
f2=8pi rho_H g R^2+4d0+2H^2,
n2=max(h2, f2/(2fmin)+(f1 L)^2/(2fmin^2)),
Kmax=1+96|u_O4|d0^2,
eps_A=sqrt(3)(1-Nmin^2 fmin),
A1=L(2sqrt(3)n1+f1+2z0),
q0=f1/2+2z0+n1+k1/k0,
B0=q0 L,
q1=f2/2+2(f1+z0)+f1 L^2(n1+k1/k0)
   +n2+k2/k0+(k1 L/k0)^2,
B1=q1+2n1 q0 L^2+sqrt(2)q0,
c0=m^2/k0, c1=c0(2n1+k1/k0)L,
ct=k0, cs=Nmin k0 sqrt(fmin),
a_*=n1 L, kappa_K=k1 L, R_minus=2d0.
```

These use N<=1 and 0<f<=1 in the stated stellar reference normalization.
For A, the radial and tangential eigenvalues are N^2 f and N^2. For B,
B=N^2[f'/2+2(f-1)/r+f((log N)'+(log K)')] n. The apparent 1/r factors
have regular Cartesian limits, bounded using |1-f|<=z0 r^2. No sampled
supremum is being renamed an analytic envelope. Reference profile inputs
remain numerical, not interval-certified measured stellar parameters.

## 7. Scope, controls and next physical step

This removes the previous **actual-solution Hessian budget** from the
energy comparison and replaces it with finite initial graph energies of a
compatible physical linear reference. It is a derived conditional
inhomogeneous comparison, not merely a renamed missing derivative.

The condition that remains is specific: the nonlinear solution must exist
through T and stay in the displayed convex canonical ball, including its
physical transmission conditions. Relative L2 energy alone cannot prevent
pointwise concentration or shocks. It would be wrong to promote this into
a global nonlinear existence theorem or automatic rho_local preparation.
Generic k-essence caustic mechanisms are a reason to retain this condition,
not evidence that the present small prepared branch actually develops them.

Validation must include the exact Legendre/relative-energy identities,
both coefficient signs, the zero-coupling baseline, transmission failure
when an excluded kinetic jump is introduced, and independent numerical
evolution of a spatially varying Hamiltonian control. A discrete control
validates the identity and implementation, NOT continuum stellar regularity.
Source-owned trajectory coefficients may evaluate eta and M3; combining
them with a dimensionless control is not joint physical RG/star matching.

Next: use a compatible stellar initial-data packet to test the finite-time
canonical-domain margin, rather than impose vacuum or erase the interaction.
Metric backreaction/work and the quantum incoming state remain separate.

Method references, checked 2026-09-08:
- [Giesselmann, Lattanzio, Tzavaras, relative energy for Hamiltonian flows](https://arxiv.org/abs/1510.00801): methodological context only; the MTS identity is derived above, not a theorem imported from a fluid system.
- [Andersson and Oliynyk, transmission wave equations](https://arxiv.org/abs/1401.0277): time differentiation and elliptic recovery motivate respecting interfaces; their full existence theorem is not asserted for this gradient-dependent parent.
- [Babichev, k-essence caustics](https://arxiv.org/abs/1602.00735): supports retaining, rather than assuming, a nonlinear continuation gate.

Frozen local sources and executed checks are recorded by
`scripts/stellar_relative_energy_20260908.py` in a fresh output directory.
All full-local-GR, PPN, complete-P(X), quantum-preparation and empirical
claim flags remain false.
