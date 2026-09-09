# Coupled scalar radiation: derive the stellar response rather than freeze it

2026-09-06. Private continuation. D4/5513 retains numerical ownership.

## Scope

The preceding contact calculation and exterior gravitational source now
extend to a material interior through the linearized Einstein constraints
and fluid conservation. The matter response is forced by the bound motion
mode; it is not set to zero or represented by a fitted damping constant.

The reference is the retained canonical Einstein-scalar-fluid system with
the quartic scalar interaction. A causal barotropic material law supplies
ordinary source data. Neither that law nor the reference star is claimed
to be selected by the full MTS cosmological history. Nonzero O4 and other
higher operators remain outside this first numerical coupled solve.

## 1. Background and perturbation conventions

Use `ds^2=-N^2dt^2+a^2dr^2+r^2dOmega^2`, `f=a^-2=1-2mu(r)/r`,
`nu=ln N`, `h=rho+p`, and `c_s^2=dp/drho`. The static equations are

```text
mu'=4pi G_N r^2 rho,
nu'=(mu+4pi G_N r^3 p)/(r^2 f),
p'=-h nu',
nu'+a'/a=4pi G_N r h/f=:J.
```

Let the first-order scalar be `chi=A phi(r)cos(omega t)` and set
`sigma=2omega`. All quantities below denote coefficients of
`A^2 cos(sigma t)`, except the third-harmonic scalar source. The fluid
coordinate displacement is `xi`; its Lagrangian pressure perturbation is
`P=Delta p`. Eulerian quantities are

```text
delta p=P-xi p',
delta rho=P/c_s^2-xi rho'.
```

Define the scalar energy/pressure harmonics and scalar radial-metric drive

```text
rho_chi,2=[-omega^2 phi^2/N^2+f phi'^2+m^2phi^2]/4,
p_chi,2=[-omega^2 phi^2/N^2+f phi'^2-m^2phi^2]/4,
B_s=pi G_N r phi phi'.
```

## 2. Derive the forced material equations

Particle conservation gives
`Delta rho/h=-[xi'+(2/r+a'/a)xi+B]`, where `B=delta ln a`.
The time/flux Einstein equation gives the geometrical mass harmonic

```text
mu_2=-4pi G_N r^2 h xi+pi G_N f r^2 phi phi',
B=mu_2/(r f)=-J xi+B_s.
```

Substitution eliminates the metric perturbation from the continuity equation:

```text
xi'=(nu'-2/r)xi-P/(h c_s^2)-B_s.
```

The fluid Euler equation is
`delta p'=h sigma^2 a^2 xi/N^2-(delta rho+delta p)nu'-h C'`,
where `C=delta ln N`. The linearized polar lapse constraint is

```text
C'=(2nu'+1/r)B+4pi G_N r a^2(delta p+p_chi,2).
```

Using the TOV and angular Einstein equations then gives

```text
P'=h[sigma^2 a^2/N^2+nu'^2+4nu'/r-8pi G_N a^2p]xi
       -(nu'+J)P
       -h[(nu'+1/r)B_s+4pi G_N r a^2 p_chi,2].
```

Thus the two unknown material functions satisfy an explicit driven linear
boundary-value problem. At the center, `xi~xi_1 r` and
`P(0)=-3h(0)c_s^2(0)xi_1`; at a free surface, `P(R_*)=0`. The source
terms are regular at the center. A zero displacement/pressure response
does not solve these equations when the displayed scalar drive is nonzero.

There is an independent constraint identity. From the scalar eigen-equation,

```text
[pi G_N f r^2 phi phi']'
 =4pi G_N r^2(rho_chi,2-h B_s).
```

The derivative of the fluid part of `mu_2`, using the forced continuity
equation, is `4pi G_N r^2(delta rho+h B_s)`. Their sum proves the
linearized Hamiltonian constraint
`mu_2'=4pi G_N r^2(delta rho+rho_chi,2)`. Freezing the matter would miss
the compensating term. No extra gravitational charge was assigned to it.

## 3. The spectral gap belongs to the fluid operator, not an invented friction

Set `zeta=r^2 xi/N`, and define

```text
Pi=a N^3 h c_s^2/r^2,
W_f=a^3 N h/r^2,
Q=a N^3 h[nu'^2+4nu'/r-8pi G_N a^2p]/r^2,
F_s=(nu'+1/r)B_s+4pi G_N r a^2 p_chi,2.
```

The forced system becomes

```text
(Pi zeta')'+(Q+sigma^2 W_f)zeta
 =a N^2 h F_s-(a N^2 h c_s^2 B_s)'.
```

For `H_f zeta=-(Pi zeta')'-Q zeta`, the weak forcing is
`-integral[a N^2 h F_s v+a N^2 h c_s^2 B_s v']dr`.
This also avoids differentiating a numerically sampled source. With the
regular/free boundary conditions the unforced operator is the standard
self-adjoint radial pulsation problem. Its coefficients and boundaries are
checked against [Kokkotas and Ruoff](https://arxiv.org/pdf/gr-qc/0011093).
The scalar forcing terms above follow from this parent and conservation,
not from a borrowed matter damping model.

If a positive lowest fluid eigenvalue `Omega_f,0^2` is established and
`sigma^2<Omega_f,0^2`, the resolvent norm is bounded by
`1/(Omega_f,0^2-sigma^2)` in the appropriate weighted Hilbert norm.
This is a conditional spectral bound, not dissipative relaxation. At a
resonance, solvability and dynamics must be treated explicitly. Finite
Galerkin eigenvalues are not automatically rigorous continuum lower bounds.

## 4. Complete retained metric forcing and its on-shell subtraction

Given the material solution, compute `B` and `C'` from the constraints and
fix `C(infinity)=0` to preserve the asymptotic clock. The cubic scalar source
from the metric is valid inside as well as outside:

```text
s_g=[-2omega^2 C+(2omega^2-N^2m^2)B]phi
                    +(N^2/(2a^2))(C'-B')phi'.
```

This contains the time-dependent lapse/radial-metric contribution; its
omission would violate the preceding harmonic derivation. The total
retained third-harmonic source is `s_g+s_contact`, before taking an outgoing
spectral norm. The interference term cannot be dropped merely because
each separate density is nonnegative.

An additional exact subtraction removes the large lapse-value contribution:

```text
s_g=(L-9omega^2)(C phi/4)+R_g,
R_g=(2omega^2-N^2m^2)B phi
     +(N^2/(4a^2))[C''+(2/r+nu'-a'/a)C']phi
     +(N^2/(2a^2))(2C'-B')phi'.
```

Green's identity again makes the operator-image term nonradiating if the
regular-center and decay boundary terms vanish. At finite radius its
explicit Wronskian boundary term is retained. This is not removal of a
physical flux: it removes a zero-overlap part before numerical integration.

No noisy second derivative of a reconstructed lapse is needed. Differentiate
its first-order constraint, use
`nu''=-nu'^2+nu'a'/a-(nu'-a'/a)/r+8pi G_N a^2p`, the Euler equation for
`delta p'`, and the scalar eigen-equation for `p_chi,2'`. Likewise
`B'=4pi G_N r a^2(delta rho+rho_chi,2)-B(1/r-2a'/a)` follows directly
from the Hamiltonian constraint. These provide local coefficients for `R_g`.

### Independent first-derivative evaluation

The first numerical pilot exposed a cancellation problem in the literal
lapse-value integral, not permission to weaken the overlap gate. Its two
raw-versus-reduced residuals were about `1.09e-2` and `1.90e-3`, while the
two reduced overlaps differed by about `5.9e-8` relatively. A separate
NumPy-boolean JSON serialization bug was fixed without changing those
numerics; the complete failing pack is retained as
`source-intake/local-preparation/20260906/coupled-fluid-radiation-pilot-serialized.json`.
That pack fails one of twelve checks. Its radiation result is not accepted
merely because the reduced formula converges.

There is a second exact, independently evaluable expression which uses
neither the lapse value `C` nor its second derivative. Let `u` be the regular
continuum mode, `W=a r^2/N`, `p_r=N r^2/a`, and
`F=p_r(u phi'-u' phi)`. The two eigen-equations give

```text
F'=8omega^2 W u phi.
H=(2omega^2-N^2m^2)B phi+N^2/(2a^2)(C'-B')phi'.
I_first=integral[W u H+C' F/4]dr.
I_raw=I_first-[C F/4]_boundaries.
I_reduced-I_first=[p_r C' u phi/4]_boundaries.
```

Thus the outer condition `C=0` used by this finite-radius solver makes
`I_first` an integration-by-parts evaluation of the original overlap.
The finite `C'` boundary term is still required when comparing it with
`I_reduced`. The regular-center boundary vanishes in the limit.
This is an algebraic change of quadrature, not a new source, gauge change,
fit, or relaxed tolerance. In particular the first-derivative integral
tests the reduced source without using the reconstructed `C''`.

The extended runner records the naive lapse-value overlap and its residual
under explicit `metric_naive_*` diagnostic fields. It evaluates the direct
overlap through this Green identity for the unchanged `1e-4` comparison
gate. Numerical validation of that replacement must be inspected separately;
the earlier failed pack and both earlier source versions are preserved.

## 5. A causal, responsive reference star

The reference constitutive law can itself be supplied by a covariant
irrotational-fluid action, rather than by a stress tensor with no variational
origin. Let `Y=-g^{mu nu}partial_mu Theta partial_nu Theta>0` and, on its
material branch, choose

```text
S_fluid=integral sqrt(-g) P_fluid(Y),
P_fluid(Y)=(sqrt(Y)-m_b)^2/(4K),  sqrt(Y)>m_b,
n=2sqrt(Y) P_fluid,Y=(sqrt(Y)-m_b)/(2K),
rho=2Y P_fluid,Y-P_fluid=m_b n+K n^2.
```

Metric variation yields the perfect-fluid Hilbert stress; varying `Theta`
conserves its particle current. Thus `p=K n^2` and
`c_s^2=dp/drho=2K n/(m_b+2K n)<1`. The vacuum continuation is not a region
of negative density: the material branch ends at zero pressure/density.
The moving free surface is part of the source problem. The reference below
sets `m_b=1`. This action makes the reference material dynamics explicit;
it does not derive `K`, `m_b` or the Standard Model from MTS.

The numerical reference uses `p=K rho_0^2`, `rho=rho_0+p`, where `rho_0`
is rest density. Its sound speed is
`c_s^2=2K rho_0/(1+2K rho_0)`, strictly between zero and one in its material
interior. This is an ordinary effective matter law, not a derived Standard
Model equation of state or an observed stellar profile. Its parameters are
declared source inputs rather than new motion-sector couplings.

Set `G_N=K=1` in the background reference units and choose central
`rho_0=0.05`. Integrate TOV to the zero-enthalpy surface, using
`H=ln(1+2K rho_0)` and `H'=-nu'`. Then rescale to scalar-mass coordinates
for the bound/continuum calculation. Varying the dimensionless
`alpha_G=mu m` in this family is not a fit to observations.

The forced fluid solve uses the derived center and free-pressure boundary
conditions. A small positive enthalpy cutoff regularizes the numerical
surface; its thin outer layer is explicitly extrapolated and tested by
changing the cutoff. It is not an imposed rigid surface. Two scalar/metric
accuracies and outer radii, plus two Galerkin meshes for the unforced fluid
spectrum, test the finite calculation. ODE, source-subtraction and boundary
residuals must pass before any reference channel is described as converged.

For this gamma-two EOS, writing `s=R_*-r`, one has `h~h_1 s`,
`c_s^2~nu'_s s` and a regular `P~P_2 s^2`. The pressure equation therefore
gives `P/(h c_s^2) -> -(V_s xi-F_s)/(2nu'_s)`, with
`V_s=sigma^2 a_s^2/N_s^2+nu_s'^2+4nu'_s/R_*`. This regularity relation,
not a rigid `xi=0` or an artificial finite-density zero pressure, supplies
the cutoff boundary condition. The last thin layer continues `xi` linearly
and `P/(h c_s^2)` constantly; its error is tested by the shrinking cutoff.

The overall scalar amplitude remains a perturbation parameter: the computed
metric response coefficients require `A^2 |B|, A^2 |C| << 1`. A unit source
profile is not permission to apply a large physical field amplitude.

## 6. Units and claim boundary

For normalized scalar modes, restoring units gives
`D_total=G_N^2 m^8 D_dimensionless`, where the contact term enters the
dimensionless source with `zeta_c=c_2 m^2/G_N`. The preceding historical
matching data fix this coefficient comparison without inventing a
lifetime. If `r=zeta_c I_contact/I_g`, the exact relative two-source density
correction is `2r+r^2`. Recording this expression avoids subtracting nearly
equal floating-point numbers when the matching ratio is tiny.

The reference remains a retained-order, asymptotically static calculation.
It does not derive the actual cosmological state, all higher-operator
corrections, a universal attractor or a measured PPN residual. Its material
response and radiation must be solved rather than assumed, and an unproved
nonlinear long-time theorem is not replaced by passing finite checks.

## Execution

Implementation: `scripts/parent_coupled_fluid_radiation_20260906.py`, using
the extended radial solver. The previous `2026-09-07T02:09:59+01:00`
handoff correctly left this pilot pending while D4 record 43 was live.
Record 43 subsequently accepted its region at `03:14:47+01:00`, reaching
`216/2/0` with 23/23 main checks passing. All the following companion runs
were executed sequentially, one core and BelowNormal, before record 44.

### Completed finite reference tests, 2026-09-07

- The original callback regression passes **13/13** checks.
- The first coupled run exposed a JSON boolean serialization error; its
  log and exact original runner are retained. The serialization-only fix
  reproduces the same numerical results and saves the failed **11/12** pack.
- The Green-identity quadrature passes **12/12**, without changing the
  reference source or the `1e-4` overlap comparison threshold.
- The final strengthened run passes **21/21**: four exact rational fixtures
  including a wrong-boundary-sign control, bound-mode matching/Rayleigh and
  outgoing normalization checks on the causal star, the material BVP,
  boundary/cutoff and fluid-spectrum checks, the two independent overlaps,
  and state/source preservation. These fixtures test the implementation;
  the algebraic argument is given above, not inferred from a few numbers.
- The final radial default-path regression again passes **13/13**.
  The formerly validated uniform-star numerical results are unchanged.

For `alpha_G=0.005`, `G_N=K=m_b=1` background reference units and
central rest density `0.05`, the TOV mass is `0.08615943212132027`,
radius `1.1083444458121763`, and compactness `0.07773705407815173`.
After rescaling to scalar-mass coordinates:

| Quantity | Coarse | Fine |
| --- | ---: | ---: |
| Scalar/continuum relative tolerance | 2e-9 | 2e-11 |
| Outer radius in Bohr radii | 22 | 28 |
| Surface enthalpy fraction | 1e-6 | 1e-8 |
| Reduced metric overlap, central scalar value one | 0.0005303403269409253 | 0.0005303403476805909 |
| First-derivative versus reduced relative residual | 6.260844625714858e-5 | -7.72828501758475e-6 |
| Normalized metric density, unit dimensionless gravitational coupling | 6.986238397563826e-28 | 6.986231342874685e-28 |

The two densities differ by approximately `1.01e-6` relatively.
The fine material ODE residual is `1.53e-8`; bound matching and Rayleigh
relative residuals are approximately `2.43e-14` and `4.08e-13`.
The first 192-cell fluid eigenvalue is `45.51570011179669`, versus the
forcing frequency squared `3.9998999799899537`. This establishes that
the sampled finite reference solve is not near that computed mode, not
a rigorous continuum spectral lower bound.

The naive lapse-value integral remains cancellation-limited (about
`1.09e-2` and `1.91e-3` disagreement in the final pack). It is explicitly
retained as a failing diagnostic, not reported as having passed. Acceptance
uses the mathematically equivalent first-derivative evaluation and the
independent second-derivative source, with the unchanged threshold.

The fine contact overlap is `-0.003473488431781066`. Inserting the historical
matched coefficient ratios solely as a non-claim comparison gives relative
interference corrections of approximately `1.175e-118` and `1.173e-118`
in this reference. This is not a physical lifetime or permission to carry
those coefficients across an unproved scale evolution.

### Reproducibility and remaining target

All result files below are under
`source-intake/local-preparation/20260906/`. Their exact earlier runners
are retained as `coupled-fluid-radiation-runner-v1.py`, `-v2.py`,
`-v3.py` and `radial-overlap-runner-v3.py`; older radial v1/v2 remain.
Each archived script hash was matched to its corresponding saved result.

| Result | SHA256 |
| --- | --- |
| `coupled-fluid-radiation-pilot-serialized.json` (failed numerical pack) | `fc781f2f33fd5887db077f655baef11c07b0c8df94c54f494536c00f400789be` |
| `coupled-fluid-radiation-green-pilot.json` | `dd8c273231bc349c4ccbd6bcd3b983743f95abf9501519d53b9fd9a7b16a0a73` |
| `coupled-fluid-radiation-green-validated.json` | `1ca59a0dfabfbfad7056a87c608efc17985938664ee61c1fce8a8bcc4d151a53` |
| `radial-overlap-green-regression.json` | `1aa14f265cb71a88e6fd9ad9a384eba16ab936f2c9d189d749310d4374f2200f` |

Final coupled runner SHA256:
`8ff603adeab3c55076282b2bc7a6d4af6ef3955fa2895c487fdd46debc75151f`.
Final radial runner:
`4025f991b298c8c7ce441238be5fc944f524cd1e2d24556b023ac3902db1ffb9`.
All cited current source hashes agree. Compilation/dry-run pass, no Python
bytecode was created, and the D4 record-43 state remained
`565ee775558e7019d00b3a2bde749f0ffb5c2d5a28816f06d4792087b13442f6`
through every companion run. There were no original-workbench or GitHub edits.

The responsive canonical reference is now implemented, rather than merely
listed as missing. The next physical extension is to derive the retained
O4 contribution to metric/matter forcing from the same parent action.
Changing `K_0(r)` in the scalar equation alone is not that extension: its
metric variation and perturbative EFT treatment also matter. Keep the
actual cosmological preparation, nonlinear long-time control and matched
scale evolution open; none is supplied by this finite radiation calculation.
