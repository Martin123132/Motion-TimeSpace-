# Parent nonlinear transfer: conservative energy, cubic source and outgoing radiation

2026-09-06. Private companion; checkpoint 5513 remains the D4 numerical owner.

## What is derived

The leading derivative interaction supplies an explicit cubic forcing and a
third-harmonic radiation channel. Its strength is a functional of the parent
Wilson coefficient, mode and outgoing continuum resolvent, not a new damping
parameter. The same calculation supplies a finite-time upper bound on feeding
of trapped modes. No sign-definite sink follows for arbitrary initial states.

The source and conservation identities below are exact at the retained
quartic order. The outgoing power is a leading forced-response result;
the resulting slow-amplitude law is **conditional**, not a nonlinear
stability theorem for the full MTS parent. A nonzero interaction is not by
itself proof of a nonzero radiative overlap.

## 1. Fix the convention before importing a coefficient

Use the 4942/5211 Lorentzian convention, signature `(-,+,+,+)`, `c=hbar=1`:

```text
X=g^{mu nu} partial_mu chi partial_nu chi,
L_chi=-K_0(x) X/2-m^2 chi^2/2+F(X),
K_0=1+2u_O4 C^2,
F(X)=c_2 X^2+O(X^3).
```

Here `F` is only the interaction tail. It is not the Euclidean/full kinetic
function with slope `1/2` in 4956 or the total `P` used in 5184. Likewise
the `X=(nabla psi)^2/2` coordinate in 4951 must not be silently identified
with this `X`. Under `X_half=X/2`, a coefficient multiplying `X_half^2`
must be divided by four to obtain `c_2` here.

For the timelike variable `Y=-X`, the quadratic-in-gradient interaction is
unchanged: `c_2 X^2=c_2 Y^2`. The Lorentzian stress ratios stated in 5209
therefore imply, in its specified canonical matching convention,

```text
c_2(k)=A_2(k) G_N^2,
F_XX(0)=2c_2(k).
```

This is a coefficient map, not a new fitted value or permission to extrapolate
an Euclidean coefficient without matching. The renormalization scale and
scheme must remain those of the controlled parent trajectory. In particular,
5209 forbids promoting its small-gradient polynomial to `k~m_gap~H` on the
fitted cosmological background. Neither that extrapolation nor an arena
retuning is used here.

There are real controlled coefficient rows available, not just a symbolic
placeholder. The companion selects the two `N=0` rows of 5209's
`controlled_PX_background_scan.csv`: both have `x_control=0.1` and
`k=0.0021445733504065682 eV`, with `A_2=-1110.6967397038904` and
`-1109.001269446347` in its two regulator insertions. It reconstructs `c_2`
using the hash-locked 5208 Newton normalization and checks the original
stress ratio independently. These are historical resolved-order matching
rows, not a new fit, a universal scale-independent coefficient, or a
computed decay rate. The older `c_X2_eV_minus4` value must not simply be
used at every matching scale.

## 2. Exact retained energy and nonlinear feeding

On the preceding static metric `ds^2=-N^2 dt^2+h_ij dx^i dx^j`, set
`w=K_0 sqrt(h)/N`, and keep its positive linear operator `L` and below-mass
projector `P_b` from the trapped-energy companion. Then

```text
K_eff=K_0-4c_2 X,
chi_tt+L chi=J_3,
J_3=-(4c_2 N^2/K_0) nabla_mu(X nabla^mu chi).
```

Terms `F=O(X^3)` add fifth-and-higher amplitude sources; they are not set to
zero in a claim about the full parent. The displayed equation is quasilinear:
`J_3` includes second derivatives and is evaluated on a solution, not treated
as an independent external forcing in an existence proof.

Writing `T=chi_t^2/N^2`, `S=h^{ij}partial_i chi partial_j chi`, the canonical
momentum and static-time energy density, per coordinate volume, are

```text
Pi=(sqrt(h)/N)(K_0-4c_2 X) chi_t,
e=N sqrt(h) [K_0(T+S)/2+m^2 chi^2/2
             +c_2(3T^2-2TS-S^2)],
flux^i=-N sqrt(h)(K_0-4c_2 X)chi_t h^{ij}partial_j chi,
partial_t e+partial_i flux^i=0.
```

These follow from the time-independent action; `c_2` is constant in
spacetime at the fixed matching scale. Quartic energy need not be positive
on arbitrarily large gradients. In a local orthonormal frame the principal
matrix is

```text
G^{mu nu}=(K_0-4c_2 X)g^{mu nu}-8c_2 v^mu v^nu,
v_mu=partial_mu chi.
```

A sufficient perturbative hyperbolicity condition is
`12|c_2|(T+S)<K_0`. Merely checking `K_eff>0` is insufficient away from the
zero-gradient branch. For a pure spatial gradient with positive `c_2`, the
longitudinal coefficient `K_0-12c_2 S` can change sign first.
Hyperbolicity is not a claim that the nonlinear characteristic cone equals
the GR metric cone; causal/UV constraints require their own matching analysis.

The quadratic modal energy is not the full conserved nonlinear energy.
Its change can have either sign; time reversal reverses energy exchange
without changing the underlying Hamiltonian. This rules out identifying the
interaction with an unconditional friction coefficient.

## 3. A quantitative feeding bound with a parent coefficient

Let `|v|_E^2=T+S` and let `|H|_E` be the Euclidean component norm of
`H_ab=nabla_a nabla_b chi` in that orthonormal frame. Since

```text
nabla_mu(X nabla^mu chi)=X Box chi+2v^a v^b H_ab,
|X|<=|v|_E^2,  |Box chi|<=2|H|_E,
|J_3|<=16|c_2|(N^2/K_0)|v|_E^2 |H|_E,
```

the earlier positive modal-energy estimate becomes

```text
sqrt(E_b(t)) <= sqrt(E_b(0))
 +8 sqrt(2)|c_2| ||N^2/K_0||_infinity
  integral_0^t ||v(s)||_infinity^2 ||H(s)||_L2(w) ds.
```

The spacetime Hessian norm and time integral must be finite and controlled
on the actual solution. This is a finite-time upper bound on nonlinear
feeding, not an assumed decay law. The previous localized-initial-data
bound controls `E_b(0)`; the equation above states exactly what further
solution norms are needed to carry it forward. A homogeneous cosmological
state is not replaced by a localized datum.

## 4. Derive the actual first and third harmonics

For a real linear bound mode `L phi=omega^2 phi`, `0<omega<m`, normalized
by `||phi||_w=1`, insert `chi=A phi cos(omega t)` at fixed small `A`.
Define

```text
U=h^{ij}partial_i phi partial_j phi,
V=omega^2 phi^2/N^2,
D_N(Y Dphi)=(N sqrt(h))^(-1)
             partial_i[N sqrt(h)Y h^{ij}partial_j phi].
```

Direct trigonometric expansion, including the time derivative of `X`, gives

```text
J_3=A^3 [s_1 cos(omega t)+s_3 cos(3omega t)],
s_1=-(c_2 N^2/K_0)[(omega^2 phi/N^2)(U-3V)+D_N((3U-V)Dphi)],
s_3=-(c_2 N^2/K_0)[(3omega^2 phi/N^2)(U+V)+D_N((U+V)Dphi)].
```

The first harmonic produces a leading self-frequency shift
`delta omega=-A^2<phi,s_1>_w/(2omega)` for an isolated, nondegenerate mode.
It is not dissipation. Multiple resonant bound modes require a coupled
amplitude system. Slowly varying `A` introduces additional derivative terms
whose remainders must be bounded, not silently discarded in a theorem.

## 5. Outgoing energy transfer, not energy disappearance

Let `P_c` denote the absolutely continuous spectral projector of the stated
linear operator, not merely `1-P_b` if other spectrum exists. For
`Omega=3omega>m`, set `S_3=P_c s_3`. If the outgoing limiting resolvent
exists on this source, define

```text
R_+(Omega)=[L-(Omega+i0)^2]^(-1),
D_3=Im <S_3,R_+(Omega)S_3>_w
   =pi <S_3,delta(L-Omega^2)S_3>_w >= 0.
```

The spectral density pairing is a limiting-absorption quantity; a positive
finite regulator value alone does not establish a positive limit. The
outgoing forced response to `A^3 S_3 cos(Omega t)` has averaged power

```text
P_out=(Omega/2) A^6 D_3.
```

Indeed the real response is `A^3 Re[e^(-iOmega t)R_+ S_3]`; multiplying its
time derivative by the real source and averaging gives precisely this
factor and sign. Total Hamiltonian energy includes the radiated field.
An advanced/incoming response reverses the power sign. An outgoing state
condition is therefore an explicit preparation/boundary input, not a new
term in the parent action.

If this is the leading open channel, nonlinear normal-form remainders are
controlled, and `D_3>0`, leading energy balance gives

```text
E_mode=omega^2 A^2/2+O(A^4),
A_dot=-gamma_3 A^5+subleading terms,
gamma_3=3D_3/(2omega),
A_leading(t)=A_0[1+4gamma_3 A_0^4 t]^(-1/4).
```

The modal energy then has an inverse-square-root leading tail, not an
exponential relaxation gap. Without unit normalization, divide `gamma_3`
by `||phi||_w^2`. Since `s_3` is linear in `c_2`, the nonnegative response
strength is quadratic in that coefficient. This does not fix its magnitude
or prove it is nonzero for an actual parent mode.

With `||phi||_w=1`, dimensions are `[phi]=length^(-3/2)`,
`[A]=length^(1/2)`, `[D_3]=length^(-4)` and `[gamma_3]=length^(-3)`.
It is `gamma_3 A^4`, not `gamma_3` alone, that has inverse-time units.
This is another reason not to treat the coefficient as an arbitrary constant
relaxation rate. The mode-rescaling check preserves emitted power and energy.

Nonlinear radiation of bound modes is an established mechanism in suitable
wave equations. Soffer and Weinstein prove it under spectral, decay and
nonzero-overlap hypotheses. Their non-derivative model is not the present
quasilinear interaction, and its theorem cannot be imported to cover this
parent's possible infinite bound spectrum. The source and normalization
above are derived for the displayed MTS interaction rather than copied from
their amplitude convention. [Primary reference](https://arxiv.org/abs/chao-dyn/9807003)

## 6. An exact radial formula for the curved-parent channel

For a static, spherical, horizonless background in areal radius, write
`ds^2=-N(r)^2dt^2+a(r)^2dr^2+r^2dOmega^2`. This is a conditional geometry
specialization, not a fitted potential or a claim that the parent selects
that geometry. For a spherical source (constant angular profile, not a
unit-normalized spherical harmonic), the actual quadratic operator becomes

```text
W=K_0 a r^2/N,  p=N K_0 r^2/a,  V=N a r^2 m^2,
L_0 f=W^(-1)[-(p f')'+V f],
||f||_w^2=4pi integral_0^infinity W |f|^2 dr.
```

Consequently the already-derived `s_3` can be evaluated without replacing
the metric by a flat continuum: use `U=phi'^2/a^2` and
`D_N(Y Dphi)=(N a r^2)^(-1)(N r^2 Y phi'/a)'`. The mode and coefficients
must still solve the specified background problem, including its interior.

At an open continuum frequency `Omega`, let `u_reg` be a real homogeneous
solution satisfying the regular-center/self-adjoint inner boundary
condition, and let `u_out` be its outgoing counterpart. Suppose limiting
absorption holds, no embedded eigenvalue obstructs this frequency, and the
source pairings converge. Define the constant Wronskian and outward current

```text
mathcal_W=p(u_reg u_out'-u_reg' u_out) != 0,
j_out=Im(p u_out^* u_out') > 0,
I_3=integral_0^infinity u_reg W s_3 dr.
```

The radial resolvent kernel with respect to measure `W dr` is
`G(r,r')=-u_reg(r_<)u_out(r_>)/mathcal_W`. The minus sign is fixed by the
unit derivative jump of `-(p G')'`. Thus the asymptotic outgoing amplitude
is `-I_3/mathcal_W`. Green's identity, with no inward energy flux through
the self-adjoint inner boundary, gives the exact on-shell density

```text
D_3=4pi j_out |I_3/mathcal_W|^2,
P_out=(Omega/2) A^6 D_3.
```

In this single radial channel, strict positivity is therefore precisely a
nonvanishing *computed overlap*, not a choice of damping constant. Rescaling
either homogeneous solution leaves this expression invariant. Discrete
off-resonant modes contribute only a real resolvent term; one may use the
unprojected `s_3` in this overlap under the stated spectral assumptions.
Long-range metric phases belong in `u_out`, not in an unproved flat-kernel
replacement. Nonspherical channels and absorbing horizons need their own
boundary/current accounting.

Two independent controls fix the normalization. For `N=a=K_0=1`,
`u_reg=sin(kr)/(kr)`, `u_out=exp(ikr)/r`, `k=sqrt(Omega^2-m^2)`, one has
`mathcal_W=-1` and `j_out=k`. A radial Gaussian then reproduces the Fourier
spectral formula. Conversely `s_3=(L_0-Omega^2)f`, with sufficiently decaying
regular `f`, has `I_3=0` by integration by parts. The script tests this
cancellation using `f=exp(-r^2/(2 sigma^2))`; it does not substitute that
reference profile for a parent eigenmode.

This converts the outgoing coefficient into a definite one-dimensional
boundary-value/overlap calculation on a chosen parent background. No actual
curved eigenmode or its radiative overlap has yet been computed here.

## 7. Decisive zero-channel controls and claim boundary

- For `3omega<=m`, this free/asymptotically massive third-harmonic continuum
  channel is unavailable; thresholds need their own analysis. Higher
  harmonics or other fields are not thereby ruled out.
- A nonzero localized source can have zero on-shell overlap. For example,
  `S=(L-Omega^2)f` has zero spectral density at `Omega^2` whenever the
  limiting-density pairing is regular. Off-shell response is not radiation.
  With a regulator `eta` in `L-Omega^2-i eta`, its response obeys the exact
  bound `0<=D_eta<=eta||f||_w^2`, so the positive finite-regulator response
  still has zero limit. This regulator has spectral-energy-squared units;
  it is not a fitted lifetime.
- A homogeneous oscillation does not supply a localized continuum source;
  it cannot be counted as escaping radiation by this formula.
- Binding frequencies, eigenfunctions, the actual continuum kernel and the
  controlled matching scale must be supplied by the parent/background. A
  Gaussian forcing example does not provide them.
- A flat continuum plus an approximate gravitational bound profile is not
  automatically a controlled rate estimate: small metric corrections can
  compete with a strongly cancelled on-shell overlap.
- Nonlinear hyperbolicity, other mode couplings, full metric/EM backreaction
  and higher-operator corrections remain separate obligations. None is
  switched off by a positive illustrative radiation check.

There is now a calculable transfer mechanism and a conservative feeding
bound, not a fitted decay constant. Full nonlinear preparation and a numeric
PPN/clock/orbital residual remain unclaimed. The exact selected prepared
GR/Newton/Maxwell branch and its one-time calibrations are retained.

## Reproducibility

The companion script is `scripts/parent_nonlinear_transfer_20260906.py`.
It checks the quartic energy balance, independent harmonic reconstruction,
hyperbolicity negative control, forcing bound, outgoing spectral
normalization and a nonradiating source with nonzero off-shell response.
The Gaussian continuum examples are dimensionless tests, not parent-mode
predictions. It runs only between D4 workers and records provenance/results
under `source-intake/local-preparation/20260906/nonlinear-transfer-`.
Finite tests are not a full nonlinear PDE proof. All physical claim flags
remain false regardless of test outcome.

The flat Gaussian forcing check also has an independent surface-flux
normalization. For `k=sqrt(Omega^2-m^2)`, the outgoing Green function is
`exp(ikr)/(4pi r)`. With unitary spatial Fourier convention its far-field
amplitude is `sqrt(pi/2) S_hat(k n)`. Integrating the averaged outward energy
flux gives `(Omega k/2) integral |amplitude(n)|^2 dOmega`. For the radial
Gaussian this equals `Omega D_3/2`, independently checking the spectral
power formula and its sign. This is still a reference-source test, not the
actual curved parent mode.

### Execution and retained numerical failure

Executed between D4 records 40 and 41 on 2026-09-06, after verifying record
40's completion marker, saved state and all 23 main validation rows. The
companion's final in-memory compilation and dry-run passed; all 12 listed
local sources and their hashes were verified. **28/28 companion checks
pass**, with 0.4180691 seconds of numerical runtime. No competing numerical
worker or Python cache was created, and the D4 state hash is unchanged.

The initial suite had one genuine failure: the nonradiating regulated
quadrature exceeded its exact vanishing upper bound at the smallest
regulator. The original Gaussian channel's coarse/fine check alone did not
detect that error. Its result is retained as
`source-intake/local-preparation/20260906/nonlinear-transfer-checks-initial-quadrature-failure.json`
(SHA256 `465e8dfa94c620ecef2f8068916dfa223765347dafb1ff9e0eb79452d96ebb1f`).

The original angle transformation smoothed only its lower endpoint. Replacing
it with `theta=theta_min+(theta_max-theta_min)sin^2(pi z/2)` resolves both
endpoints. No prior acceptance threshold was loosened. Two additional checks
require nonradiating coarse/fine agreement and the independent exact identity
`D_eta[(L-Omega^2)f]=eta||f||^2-eta^2 D_eta[f]`, each to relative `1e-7`.
At `eta=0.0125`, the corrected nonradiating result is
`0.008682072331504786`, rather than `0.008722867665815592`; coarse/fine
values agree beyond the imposed tolerance. This correction supplies a
negative-control success, not a new physical radiation signal.

The source-backed reconstructions give `c_2=-4.999069422579752e-110 eV^-4`
and `-4.9914383805334426e-110 eV^-4` at the stated matching scale. Both
reproduce the historical stress ratios to relative `2.22e-16`. These remain
controlled historical coupling rows, not numeric decay coefficients.

The passing result is
`source-intake/local-preparation/20260906/nonlinear-transfer-checks.json`
(SHA256 `8b745cc20ee7ee8687266cfa55bc4e8989eaabb71954b121fc2ca921dfbfe883`).
It records source/script/provenance hashes and keeps every broad physical
claim false. The next physical calculation is the actual curved-background
bound mode and outgoing overlap in section 6, not another Gaussian example
or an assumed positive rate.
