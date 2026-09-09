# Finite-time causal escape and forcing: a quantitative preparation window

Private continuation of the horizon theorem, 2026-09-08. The aim here is an
actual finite-time inequality, not identification of asymptotic decay with
rapid preparation. This does not replace the remaining nonlinear/quantum
state and higher-operator requirements.

## 1. Keep the physical operator; choose only a comparison equation

On the same regular static spherical background, let s be the tortoise
coordinate, B=r sqrt(K), and y=B chi_ell. The exact quadratic motion equation is

```text
y_tt + [-partial_s^2 + V_ell] y = F_ell,
V_ell=B_ss/B+N^2[m^2/K+ell(ell+1)/r^2].
```

K=1+2u C^2 and m are unchanged. The comparison operator is the flat, massless
radial wave operator `H0_ell=-partial_s^2+ell(ell+1)/s^2`; it is NOT substituted
for the parent. Its bounded residual on a finite causal interval is

```text
W_ell=V_ell-ell(ell+1)/s^2
      =V_0+ell(ell+1)[N^2/r^2-1/s^2].
```

Both brackets extend continuously to a regular center. Thus the method covers
finite angular bands, not merely a chosen spherical mode. The regular center
condition and the physical flux-matching conditions remain in force.

Assume initial displacement and velocity are supported inside s<=S0. For the
unforced equation, finite propagation gives support inside A(t)=S0+t. This
is a causal support statement, not a reflecting wall. If a force is included,
its support must be inside the same specified causal region, or A must be
enlarged to include its causal support.

## 2. Derive the finite-time bound

Write E_ref for the positive energy of H0_ell, and let y_free have the same
initial data. Define Y=sqrt(2E_ref[y]), D=sqrt(2E_ref[y-y_free]). On the support
interval, the regular radial field vanishes at both endpoints, so
`||y||_2 <= A(t)||y_s||_2/pi`. If `v_L(A)` bounds |W_ell| for every ell<=L,
energy differentiation and Duhamel's formula give

```text
c(t)=v_L(A(t)) A(t)/pi,    J(t)=integral_0^t c(tau) dtau,
Y(t) <= Y(0) exp(J(t)),
D(t) <= Y(0)[exp(J(t))-1]                         (F=0).
```

For a fixed upper bound v_L on the whole chosen causal region,
`J(t)<=v_L[S0 t+t^2/2]/pi`.

The flat 3D Kirchhoff solution samples initial data on spheres of radius t.
For |x|<=S and t>S0+S, these spheres miss the initial support. Consequently
y_free and its derivatives vanish on s<=S, for ALL angular harmonics. Hence

```text
E_ref,obs[y(t)] <= E_ref[y(0)] [exp(J(t))-1]^2,
t>S0+S.
```

This is a finite escape WINDOW estimate. It is useful if J at the first
clearing time is small; its upper bound grows at later times and is not
advertised as an all-time decay rate.

## 3. Convert to the retained positive quadratic motion energy

The energy which bounds the full Hilbert-source smear is

```text
2 E_K = integral [|y_t|^2+|y_s-b y|^2+U_ell |y|^2] ds,
b=B_s/B=1/s+beta(s),
U_ell=N^2[m^2/K+ell(ell+1)/r^2].
```

This is the positive fixed-background quadratic energy, not an assertion that
every pointwise component of the full metric-varied O4 stress is positive.

On an observation interval s<=S, the exact boundary identity gives
`||y_s-y/s||^2=||y_s||^2-|y(S)|^2/S <= ||y_s||^2`.
Also `||y||<=S||y_s||/sqrt(2)` there. Thus

```text
C_obs=max{1, (1+beta_max S/sqrt(2))^2+S^2 M_obs/2, A_ang,max},
M_obs=sup N^2 m^2/K, A_ang=N^2 s^2/r^2,
E_K,obs <= C_obs E_ref,obs.
```

At initial time the compact-support endpoint term is zero. If
`eta0=beta_max,0 S0/pi<1`, the reverse triangle inequality yields

```text
C_init=max{1,(1-eta0)^(-2),1/A_ang,min},
E_ref(0) <= C_init E_K(0).
```

If eta0>=1 this coarse conversion fails; the directly computed initial
E_ref remains an admissible input. No physical instability follows from
failure of this norm estimate.

For an unforced angular band the result is therefore

```text
E_K,obs(t)/E_K(0)
 <= min{1, C_obs C_init [exp(J_L(t))-1]^2},  t>S0+S.
```

All constants are determined by geometry, the retained coupling and the
initial support. A target fraction delta requires
`J_L <= log(1+sqrt(delta/(C_obs C_init)))`.

For a constant envelope v_L>0 write this last threshold as J_delta. The
target's end time is bounded by
`t_delta=-S0+sqrt(S0^2+2 pi J_delta/v_L)` and by the finite causal domain's
end time. A nonempty interval [t_clear,t_end] requires t_end>t_clear>S0+S.
Throughout it, `integral E_K,obs dt <= delta E_K(0)(t_end-t_clear)` for the
unforced low band. This supplies the energy-time factor in the existing full
Hilbert-source smear bound, not an instantaneous pointwise PPN coefficient.
The runner reports the available window for a declared illustrative target
delta=1e-4. That target is not an experimental tolerance or fitted parameter.

## 4. Angular tails and forcing are not silently set to zero

For the full unforced spherical operator define the conserved angular energy
moment `S_q=sum_ell,m [1+ell(ell+1)]^q E_K,ell,m`, q>0. Then

```text
E_high(L) <= S_q/[1+(L+1)(L+2)]^q,
E_K,obs <= C_obs C_init E_low(0) [exp(J_L)-1]^2 + E_high(0).
```

An exactly radial reference has E_high=0 by its declared data, but this must
not be assigned to arbitrary data. A claimed small total fraction requires
both the low-band estimate and a supplied/derived angular-tail budget.

For a supplied force the bandwise energy estimate instead contains

```text
D(t) <= Y(0)[exp(J(t))-1]
        + integral_0^t exp[J(t)-J(tau)] ||F(tau)||_2 dtau.
```

The second term explicitly controls continued excitation. For non-bandlimited
forcing the angular energy budget must also be updated, using
`sqrt(2 S_q(t)) <= sqrt(2 S_q(0)) + integral ||(1-Delta_Omega)^(q/2) F|| dt`.
The unforced high-band budget cannot be reused unchanged.

For a supplied integrated force budget `L_F=integral_0^t ||F|| dtau`, monotonicity
of J gives the implementable, conservative absolute-energy estimate

```text
E_K,obs(t) <= (C_obs/2) [sqrt(2 E_ref(0)) expm1(J) + exp(J) L_F]^2.
```

There is no clipping at the initial energy when forcing is present. The
companion checks this against a manufactured compact forced wave, not just
positivity of an arbitrary placeholder. On the flat half-line take
`y=t^2 psi/2`, `psi=sin^2(pi s)` on [0,1], zero outside. Then
`F=psi-t^2 psi_ss/2`, zero initial data, and
`E=(3 t^2/8+pi^2 t^4/8)/2`. The analytic force budget
`L_F<=t sqrt(3/8)+t^3 sqrt(2 pi^4)/6` must bound its nonzero energy even
after the unforced clearing time. Omitting the source must fail that control.
The C1 spatial matching makes this a valid energy solution with piecewise
smooth force; no delta-function boundary source is introduced.

In the selected linearization F=0 follows from the parent equation, rather
than a source cancellation fitted to data. Nonlinear derivative interactions
and metric/fluid backreaction can act as F, but bounding them requires their
actual coefficients, regularity and hyperbolicity control. They are not
assumed small merely because the linear bound is small.

### Noncompact initial data: retain a spatial remainder, not a vacuum axiom

For general finite-energy data, choose a smooth radial cutoff and split BOTH
initial field and velocity into compact data and a remainder. Let their exact
positive quadratic energies be E_compact and E_remainder. These are computed
after the cutoff: derivative-of-cutoff terms belong to the energies and
cannot be discarded. They do not generally add to the original energy.

Linearity, conservation of the remainder's global energy, and the triangle
inequality in the local energy norm then give

```text
E_obs(t) <= [sqrt(epsilon(t) E_compact)+sqrt(E_remainder)]^2
```

within the compact component's clearing window. Here epsilon is the band
bound from section 3; use the angular decomposition and its tail separately.
Spatial pieces are NOT orthogonal: simply adding their energies would miss
interference. Thus a small total target additionally needs a genuinely small
remainder/incoming budget. The extension makes that dependence quantitative
instead of imposing exact compact support on every admissible state. It does
not assert that arbitrary extended matter/quantum states supply that budget.

## 5. Obtain explicit background envelopes rather than sampled suprema

Use G_N=c=hbar=1; restoring only G_N while retaining c=1 replaces rho,p by
G_N rho,G_N p. Let the
nonnegative density and pressure decrease outwards, with surface R, mass mu,
central rho_c,p_c, central lapse N_c, and H^2=Lambda/3>=0. For a chosen finite
causal radius r_max, derive

```text
d0=4 pi rho_c/3,
zeta=2(d0 mu^2)^(1/3),
f_min=1-zeta-H^2 r_max^2 > 0,
N_min=min(N_c,sqrt(f_min)), v_min=N_min sqrt(f_min).
```

The mass inequality uses `mu(r)<=min(d0 r^3,mu)`, so it includes the entire
stellar interior. Let rho_H and rho_HH bound EOS density derivatives with
respect to enthalpy on its central-to-surface range, and define

```text
g=[d0+4 pi p_c+H^2]/f_min,
f1=8 pi rho_c+2 d0+2 H^2,
n1=max(g,f1/(2 f_min)), v1=n1+f1/(2 f_min),
d2=4 pi rho_H g/15,
d1=3 d2+4 pi rho_H g/3,
a1=3 d2+4 pi(rho_c+p_c)g,
h2=g+R^2(a1+g f1)/f_min,
rho2=rho_HH(g R)^2+rho_H h2,
d_second=3 d1+3 d2+4 pi rho2/3.
```

These follow from TOV-Lambda, `|H_enthalpy'|<=g r`, the EOS chain rule, and
the exact Weyl quantity `D=mu(r)/r^3-4 pi rho(r)/3`. Specifically,
`0<=D<=min(d0,d2 r^2)`, `|D'|<=d1 r`, `|D''|<=d_second`.
Outside the star rho'=rho''=0, so the same conservative bounds continue to
hold. Lambda cancels from C^2=48D^2, not from the metric or the TOV equation.

For these bounded-potential formulas the density must match the vacuum C1,
with bounded piecewise second derivative; in particular rho(R)=rho'(R)=0.
The retained gamma=3/2 reference satisfies this surface condition. A density
jump or a jump in its first derivative requires explicit interface terms
and is not covered by silently reusing these suprema.

Consequently valid K/derivative envelopes on the causal region are

```text
k_min=1-96 |u| d0^2 > 0,
k1=192 |u| d0 d1,
k2=192 |u|[(d1 r_max)^2+d0 d_second],
|K'|<=k1 r, |K''|<=k2.
```

With N<=1 and v=N sqrt(f)<=1, set

```text
V0_bound=k1/k_min+k2/(2 k_min)+(k1 r_max)^2/(4 k_min^2)
         +v1[1+k1 r_max^2/(2 k_min)]+m^2/k_min,
Va_bound=2 d0+H^2+2 v1/(3 v_min),
v_L=V0_bound+L(L+1) Va_bound,
beta_slope=v1/(3 v_min)+k1/(2 k_min).
```

To see the angular cancellation explicitly, integrate `|v'|<=v1 r` to obtain
`|v(r)-r/s|<=v1 r^2/(3 v_min)`. Combine this with
`N^2-v^2=N^2(1-f)` to bound `|N^2/r^2-1/s^2|<=Va_bound`.
The same identity gives `|beta|<=beta_slope r`. Also
`N_min^2<=A_ang<=1/v_min^2`. These are analytic envelopes, not maxima inferred
from a finite sample grid.

## 6. Lambda-TOV reference and physical scope

The companion retains the existing gamma=3/2 material EOS but integrates
TOV-Lambda in dimensionless variables to handle weak stars without a huge
raw radial integration range. With central enthalpy h_c, raw central density
rho_c, `L0^2=h_c/(4 pi rho_c)`, z=r/L0, n=mu/(h_c L0), theta=h/h_c and
`lambda_ratio=H_raw^2/(4 pi rho_c)`, its equations are

```text
dn/dz=z^2 rho(h_c theta)/rho_c,
dtheta/dz=-[n+z^3(p/rho_c-lambda_ratio)]/
           [z^2(1-2 h_c n/z-h_c lambda_ratio z^2)].
```

The first zero of theta defines the surface. Conversion to R=1 produces
mu/R, H^2 R^2, N_c and the central EOS derivative inputs above. Lambda=0 is
checked against the frozen existing stellar solver. Nonzero Lambda and both
signs of u are explicit controls, not a new fitted damping parameter.

`scripts/parent_finite_time_escape_20260908.py` evaluates these reference
families and the analytic bound. The sampled background checks and ODE
refinement comparison are diagnostics, NOT interval-certified stellar data.
Any numerical claim about a real star still requires conservative sourced
background inputs, an initial energy/angular/forcing budget and an actual
observable's response. The complete Hilbert-source estimate then uses the
finite-window energy integral; it does not become a pointwise PPN claim.

The data and observation are initially specified inside areal radius R.
The code uses `S0=S=R/v_min` as upper bounds on their tortoise radii, and
`beta_max=beta_slope R` only on that physical areal region. It first converts
the physical local energy there, then enlarges the positive reference-energy
integral to s<=S. It does not claim the same beta bound on the larger areal
region r<=S. With r_max=4R, the explicit gate S0+t<=r_max guarantees that the
coefficient envelopes include the entire causal support, since r<=s.

Sources: `5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md`,
`DERIVATION-20260907-whole-star-localization-and-static-validity.md`,
`DERIVATION-20260908-cosmological-horizon-and-linear-local-preparation.md`,
and `scripts/parent_O4_star_profile_20260907.py`.

External comparison-equation reference: Jared Speck, MIT 18.152, Fall 2011,
[Lecture 12, Theorem 1.1 and Remark 1.0.1, p. 1](https://ocw.mit.edu/courses/18-152-introduction-to-partial-differential-equations-fall-2011/940561a138578640826f762b5a57bcad_MIT18_152F11_lec_12.pdf),
checked 2026-09-08. This supports the flat Kirchhoff/Huygens step only.
The curved-operator residual, geometry envelopes, norm conversion and forcing
budget are the derivations here; no curved-space rate is borrowed from it.
