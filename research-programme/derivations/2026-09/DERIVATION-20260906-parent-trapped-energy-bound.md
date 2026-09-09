# Parent motion sector: gravitational binding and a derived trapped-energy bound

2026-09-06. Private companion; D4/5513 remains the numerical owner.

## Outcome

The preceding free-field dispersion lemma cannot simply be promoted to every
gravitating background. The selected quadratic motion field can have
below-mass bound modes on a static, horizonless, asymptotically Schwarzschild
background. That is ordinary gravitational binding, not an MTS-specific
failure. More usefully, a **uniform bound on the total below-threshold energy
excited by localized initial data** can be derived without setting its
occupation to zero. This bound includes all modes below the mass threshold,
not just a chosen ground state.

These statements concern the retained linear motion equation on a specified
fixed metric. They do not prove the full nonlinear preparation history,
exclude all other spectral obstructions, or supply a measured PPN residual.
No new dimensional parameter or damping coefficient is introduced.

## 1. Exact static operator from the selected parent

Use signature `(-,+,+,+)`, `c=hbar=1`, and `m=m_gap>0`. On a static background

```text
ds^2=-N(x)^2 dt^2+h_ij(x) dx^i dx^j,
K_0(x)=1+2 u_O4 C^2(x)>0,
w=K_0 sqrt(h)/N,
a^{ij}=N sqrt(h) K_0 h^{ij}.
```

Since `P_X(0)=0`, linearization of the sourced equation in 5211/5344 gives

```text
chi_tt + L chi = 0,
L=-w^(-1) partial_i(a^{ij} partial_j) + N^2 m^2/K_0,
<f,Lf>_w = q[f]
 = integral [a^{ij} partial_i f* partial_j f + N sqrt(h) m^2 |f|^2] d^3x.
```

The inner product is `integral w f* g d^3x`. A regular, complete spatial
slice with smooth positive coefficients defines the positive self-adjoint
operator through this quadratic form. A conservative Dirichlet exterior
problem is another allowed mathematical realization, explicitly different
from an absorbing horizon. No moving background or dissipative boundary is
silently assigned this operator.

There is also a useful exact normalization identity. Set `kroot=sqrt(K_0)`
and `chi=v/kroot`:

```text
nabla_mu(K_0 nabla^mu chi)-m^2 chi
 = kroot [Box_g v - (m^2/K_0 + Box_g kroot/kroot) v].
```

Thus the extra scalar potential relative to minimally coupled mass `m` is
`m^2(1/K_0-1)+Box_g sqrt(K_0)/sqrt(K_0)`. In a Schwarzschild asymptotic end,
`C^2=O(r^-6)`; a finite constant `u_O4` changes this potential only at short
range. This does not remove the long-range Newtonian attraction.

## 2. Why gravitational binding must be considered

Write `mu=G_N M` in these units. For `N=1-mu/r+O(r^-2)` and
`h_ij=(1+2mu/r)delta_ij+O(r^-2)`, the quadratic form relative to threshold is

```text
q[f]-m^2||f||_w^2
 = integral [|grad f|^2 - (2 mu m^2/r)|f|^2] d^3x
   + asymptotically shorter-range and metric-gradient terms.
```

For a fixed annular test profile `F` and `f_R(x)=R^(-3/2)F(x/R)`, the
kinetic term is of order `R^-2`, whereas the attractive term is of order
`-mu m^2/R`. Hence sufficiently distant shells have a negative
threshold-relative Rayleigh quotient. This is the variational origin of the
binding; a tiny attraction cannot be discarded solely because it is tiny.

For the standard massive Klein-Gordon operator, Sussman proves infinitely
many below-threshold modes for an appropriate class of static horizonless
asymptotically Schwarzschild geometries. His theorem does not cover the full
black-hole exterior. The selected `K_0` normalization above identifies the
short-range modification that must be retained when applying this spectral
reasoning to MTS. This is an application of established binding physics,
not a newly discovered effect. [Primary source](https://arxiv.org/abs/2312.00959)

The usual weak-field, slow-envelope expansion independently yields

```text
i partial_t psi = [-Delta/(2m) + m Phi] psi,
Phi=-mu/r,
a_B=1/(mu m^2),
E_n=-m (mu m)^2/(2 n^2).
```

Here `a_B` is a gravitational length scale, not a new coupling. These
hydrogenic formulas require weak binding and a state lying in the appropriate
exterior/background corridor; they are not an exact star spectrum.
[Nonrelativistic-expansion reference](https://arxiv.org/abs/1812.05181)

Checkpoint 5208 explicitly selected `Lambda_cal=0` as a branch hypothesis.
That is not a license to identify the actual cosmological state with a
globally empty static background. If nonzero Lambda, cosmological expansion,
absorption, or metric backreaction is retained, the operator and its spectral
threshold must be reconsidered. In particular, infinitely distant static
shells cannot be used as a proof about a finite cosmological patch.

The time/gravity link is explicit here: the same lapse `d tau=N dt` that
relates stationary proper time to coordinate time enters `N^2 m^2/K_0` in
the wave operator. For `K_0=1`, its weak-field departure from `m^2` supplies
the attractive well. No extra motion-specific gravitational charge was added.

## 3. Bound all below-threshold excitation, rather than assert zero occupation

Assume global bounds on the stated coordinate slice:

```text
a^{ij} z_i z_j >= kappa |z|^2,                  kappa>0,
0<w_min<=w(x),
m^2[w-N sqrt(h)] <= b/r,                       b>=0,
theta=inf_x N^2/K_0 > 0.
```

One explicit choice is
`b=m^2 sup_x {r [sqrt(h)/N (K_0-N^2)]_+}`. These are geometry/parent
coefficient norms, not fitted arena constants. If any is infinite or loses
the stated sign, the resulting bound is unavailable, not a zero residual.
Let `P_b=1_[0,m^2)(L)` be the orthogonal spectral projector in `L2(w dx)`.

### Gradient control on the entire subspace

For `f` in the range of `P_b`, spectral calculus gives
`q[f]-m^2||f||_w^2<=0`. The Euclidean three-dimensional Hardy inequality gives

```text
kappa ||grad f||_2^2
 <= b integral |f|^2/r
 <= 2 b ||f||_2 ||grad f||_2,
||grad f||_2 <= (2b/kappa)||f||_2.
```

For completeness, Hardy follows by integrating
`div(x/r^2)=1/r^2` against `|f|^2` and using Cauchy-Schwarz, then extending
from smooth compact data. Conservative exterior Dirichlet data are extended
by zero; arbitrary boundary conditions do not automatically permit this step.

An adequate, deliberately non-sharp Sobolev constant is `C_S=4` in
`||f||_6<=C_S||grad f||_2`. One elementary proof applies the coordinate
fundamental-theorem-of-calculus bounds and iterated Cauchy-Schwarz to obtain
`||h||_(3/2)<=||grad h||_1`, then takes `h=|f|^4`. Holder gives
`||f||_6^4<=4||f||_6^3||grad f||_2`. Approximation covers the energy domain.

For a bounded region `Omega` with finite volume and `w_Omega=sup_Omega w`,

```text
||1_Omega P_b||_(w->w) <= min(1, epsilon_Omega),
epsilon_Omega = (2 b C_S/kappa) sqrt(w_Omega/w_min) |Omega|^(1/3).
```

This follows from Holder on `Omega`, Sobolev, the gradient bound, and the
weight bounds. Taking the Hilbert-space adjoint gives the same estimate for
`P_b 1_Omega`. Thus **any** `L2(w dx)` datum supported in `Omega` has small
below-threshold projection when `epsilon_Omega` is small. There is no
assumption that it was prepared orthogonal to every bound mode.

### Conserved modal-energy bound

For initial displacement `f` and velocity `g` both supported in `Omega`,
define `E_total=(||g||_w^2+q[f])/2`. For `E_total>0`, since `L<m^2` on this subspace,

```text
E_b=(||P_b g||_w^2+||L^(1/2)P_b f||_w^2)/2,
E_b <= (epsilon_Omega^2/2) (||g||_w^2+m^2||f||_w^2),
q[f]>=m^2 theta ||f||_w^2,
E_b/E_total <= min(1, epsilon_Omega^2 max(1,theta^(-1))).
```

This is an exact conditional bound for the specified quadratic operator.
Zero total energy gives the trivial zero solution under the stated positivity.
`E_b` is conserved by its linear evolution. If the complementary sector
has local energy decay, the positive local-energy triangle inequality gives
`limsup E_Omega(t)<=E_b`; that complementary decay is a separate spectral
and propagation requirement, not proved merely by removing `P_b`.
Embedded eigenvalues or other obstructions above the chosen threshold are
not bounded by pretending they belong to `P_b`.

### A local observable bound on the static coherent-state branch

The canonical momentum on this slice is `Pi=w chi_t`. For a coherent
displacement of the positive static quadratic vacuum and fixed real smears
`F,G` supported in `Omega`, the Weyl phase is
`I=integral [F chi+G w chi_t] d^3x`. The positive energy density gives

```text
|I| <= sqrt(2 E_Omega)
       sqrt(integral_Omega [F^2/(m^2 N sqrt(h)) + G^2 w] d^3x).
```

The difference of the displaced and vacuum Weyl expectations is at most
`|I|`. For the trapped component, replace `E_Omega` by its conserved global
`E_b`. If the complementary component disperses locally, the same expression
with `E_b` bounds the late-time limsup for the full coherent displacement.
This is an observable residual bound, not an identification with the binary
parent occupation or a statement about interacting quantum covariances.

## 4. Explicit Schwarzschild-exterior coefficient envelopes

These furnish a calculable reference example, not an imposed reflecting
surface for the actual motion field. Let the isotropic exterior be
`r>=R_star>mu/2`, with conservative Dirichlet data if used as a standalone
operator. Put

```text
z_star=mu/(2R_star),  N_star=(1-z_star)/(1+z_star),
r_A=r(1+mu/(2r))^2,
C^2=48 mu^2/r_A^6,
delta=96 |u_O4| mu^2/[R_star(1+z_star)^2]^6 < 1.
```

Direct substitution and monotonicity give valid global envelopes:

```text
kappa=(1-z_star^2)(1-delta),
w_min=1-delta,
w_Omega<=(1+delta)(1+z_star)^7/(1-z_star),
theta>=N_star^2/(1+delta),
b<=2 mu m^2 (1+z_star)^5/(1-z_star)
   +96 |u_O4| mu^2 m^2/[R_star^5(1-z_star)(1+z_star)^5].
```

In the weak-field, negligible-curvature-correction limit, `b~2mu m^2` and
the other dimensionless envelopes tend to one. For a ball of radius `R`,
the conservative projection bound then scales as
`epsilon_Omega~16(4pi/3)^(1/3) R/a_B`. The energy bound scales as `(R/a_B)^2`.
These are suppression scalings, not zero-occupation axioms. A regular stellar
interior requires its own global coefficient envelopes; exterior values
alone are insufficient. A very small mass can make `a_B` much larger than
the physically valid static region, so a formal static bound spectrum is not
automatically an important local signal.

Dimension check in the stated units: `mu` and `a_B` have length, `m` has
inverse length, `u_O4` has length to the fourth power, and `b` has inverse
length. The remaining coefficient envelopes and `epsilon_Omega` are
dimensionless. The normalization of `G_N` remains the already calibrated
one; neither the binding calculation nor this bound derives its SI value.

## 5. Exact nonlinear forcing entry and remaining scope

On this fixed metric the displayed full motion equation can be rearranged as

```text
chi_tt+L chi = J_nl,
J_nl=-(2N^2/K_0) nabla_mu[P_X nabla^mu chi].
```

It is solution-dependent and can contain second time derivatives. No
existence theorem is inferred from the rearrangement. Projection and the
positive linear energy yield

```text
sqrt(E_b(t)) <= sqrt(E_b(0))
              +(1/sqrt(2)) integral_0^t ||P_b J_nl(s)||_w ds.
```

Thus nonlinear feeding must be estimated rather than silently removed.
Radiation-induced depletion is also possible in some nonlinear wave models,
but requires a nonzero, derived resonance coefficient and appropriate
spectral control. A theorem for a different nonlinearity or a finite number
of bound modes cannot be imported as a theorem for this parent.
[Mechanism reference](https://arxiv.org/abs/chao-dyn/9807003)

The useful advance is an initial trapped-energy upper bound from geometry,
parent coefficients and localization. It is not global purification,
the parent's binary density-matrix occupation, full Hilbert-stress control
including curvature variations, or a PPN/clock/orbital result. Homogeneous
cosmological occupation and indefinitely incoming disturbances are not
localized finite-energy data and need their own sourced bounds. Nonlinear
and higher-operator effects remain explicit. The exact selected prepared
GR/Newton/Maxwell branch is unchanged, as is the fair GR-plus-massive-scalar
baseline for the binding calculation.

## Reproduction

`scripts/parent_trapped_energy_bound_20260906.py` checks exact algebra,
Rayleigh-shell examples, coefficient envelopes, the flat negative control,
and the derived suppression scaling. It uses dimensionless illustrative
parameters, not an MTS mass or fitted curvature coefficient. The calculations
must run between D4 workers. Passing finite checks is not a proof of a PDE
theorem or evidence that actual parent data satisfy all the hypotheses.
Provenance and results reside in `source-intake/local-preparation/20260906/`
under the `trapped-energy-` prefix; no physical claim flag is promoted.

### Executed checks

After D4 record 39 completed and all 23 main validation rows passed, the
companion ran alone on one core at BelowNormal priority. Final in-memory
compilation and dry-run passed, followed by **16/16 checks** in approximately
0.12 numerical seconds. The script refused competing numerical execution
during the earlier live-worker dry-run. No main state change or bytecode
cache was produced by the companion.

Exact annular profile constants are `A=308/25` and `B=33/50`, with the
notation of the kinetic and inverse-radius Rayleigh ratios. The sampled
Schwarzschild-shell quantity `R*(Rayleigh-m^2)` approaches `-2B=-1.32`;
at `R=16384`, the zero-curvature-coefficient example gives
`-1.319196606982332`. Flat and repulsive controls do not bind in these
examples. Both signs of the illustrative curvature coefficient respect the
derived envelopes, and the radius-squared/mass-fourth suppression scaling
passes its checks. These quadratures are resolution-checked numerical
examples, **not interval eigenvalue certificates or measured MTS inputs**.

Result: `source-intake/local-preparation/20260906/trapped-energy-checks.json`.
SHA-256: `551da9d8c956e4091ac8a6ff63905f35d0453a42f568d3ae11321aec0d8e5005`.
The result records source, script and provenance hashes and leaves all
physical claim flags false. The next derivation is to control the displayed
nonlinear feeding term or its actual radiative depletion, while retaining
cosmological/incoming state data rather than declaring them absent.
