# Parent radial radiation: remove the off-shell part before measuring escape

2026-09-06. Private companion. D4/5513 remains the main numerical owner.

## Result and exact scope

The cubic source can be separated into a term with **exactly zero on-shell
overlap** and an explicit geometry/gradient remainder. This is more useful
than simply asking whether a nonzero nonlinear term radiates. It identifies
which part of that term can actually transfer energy into an outgoing mode.

The identity below retains the radial kinetic coefficient `K=K_0(r)`.
The first numerical application uses the regular GR uniform-density-star
metric and `K=1`, with the *same covariant operator* used for its bound mode
and its scattering mode. It is not a Gaussian source or a flat continuum
attached to an unrelated binding potential. It is also not a solution of
the full higher-operator parent, an actual cosmological state, or a measured
decay rate. Geometry selection, incoming state, nonzero O4 corrections and
full nonlinear remainders are not erased by a successful reference solve.

## 1. An operator lower bound opens the channel

For the preceding positive static operator,
`L >= m^2 theta`, with `theta=inf N^2/K`. Every below-threshold eigenmode
therefore satisfies `m sqrt(theta)<=omega<m`. If `theta>1/9`, its third
harmonic obeys `3omega>m` without fitting an eigenfrequency to open a channel.
This is a kinematic statement; a nonzero overlap is still required.

For a Schwarzschild exterior in the earlier isotropic notation, a sufficient
condition is `[(1-z_star)/(1+z_star)]^2/(1+delta)>1/9`. Equivalently,
`z_star<(3-sqrt(1+delta))/(3+sqrt(1+delta))`, with positive numerator.
An actual regular interior needs its own lapse/kinetic lower bound. A horizon
does not satisfy this argument merely because a surface outside it does.

## 2. Exact on-shell subtraction for the radial parent

Use the areal-radius metric and radial operator from the nonlinear-transfer
companion. Let `K>0`, `W=K a r^2/N`, `p=N K r^2/a`, and
`L phi=omega^2 phi`. The real mode is not required to be normalized here.
Write `U=phi'^2/a^2` and

```text
eta_N=N'/N,  eta_K=K'/K,
A_sub=c_2 omega^2(2omega^2+m^2)/[2(3omega^2+m^2)].
```

`A_sub` is a derived subtraction coefficient, not the oscillation amplitude
or a new coupling. Assume `N,K -> 1` at the asymptotic end. The product rule
and the bound-mode equation give the exact identity

```text
(L-9omega^2)phi^3
 =-2(3omega^2+N^2 m^2/K)phi^3-6N^2 phi U.
```

Expanding the previously derived third-harmonic source, and eliminating
`phi''` with that same eigen-equation, gives

```text
s_3=A_sub (L-9omega^2)phi^3+R_3,
R_3=C_0 phi^3+C_1 phi U+C_2 phi'^3+C_3 phi^2 phi',

C_0=2A_sub(3omega^2+N^2m^2/K)
       -c_2[2omega^4/(K N^2)+omega^2m^2/K^2],
C_1=6A_sub N^2-c_2(2omega^2/K+3N^2m^2/K^2),
C_2=c_2 N^2/(K a^4) [4/r+2eta_N+3eta_K],
C_3=c_2 omega^2/(K a^2) [2eta_N+eta_K].
```

Thus nonzero `K` and its radial derivative have explicit places in the
on-shell source; they have not been silently identified with zero.
These formulas concern the retained quartic interaction on a fixed metric.
Higher powers of the gradient add higher-amplitude sources.

For a regular continuum solution `u_reg` at `Omega=3omega`, Green's identity
gives, on any finite radial interval,

```text
integral W u_reg [s_3-R_3] dr
 =A_sub [p(u_reg' phi^3-u_reg (phi^3)')]_inner^outer.
```

The boundary term vanishes for the regular-center, decaying-bound-mode
problem. Hence the exact radiation overlap can be evaluated with `R_3`
instead of `s_3`. This removes a large off-shell contribution before the
oscillatory numerical integration. Neither a physical damping term nor a
numerical regulator is introduced. At interfaces, the matching of the
field and its self-adjoint flux must be included; arbitrary jumps cannot
be ignored in the boundary identity.

## 3. The first weak-binding term is not zero

The following is a **conditional asymptotic calculation**, not a uniform
error theorem for the actual parent. Set `K=1` at leading curvature order,
`mu=G_N M`, `alpha_G=mu m<<1`, `kappa=mu m^2`. In the Schwarzschild exterior
`N^2=1-2mu/r`, `a^2=N^-2`. On the weakly bound lowest radial branch,
`omega=m+O(alpha_G^2 m)` and `phi~phi_c exp(-kappa r)` outside a sufficiently
small regular core. The exact remainder then has the first term

```text
R_3=-(11/2)c_2 mu m^4 phi^3/r + higher-order terms.
```

The coefficient follows directly from
`C_0=c_2 omega^2(N^2-1)
 [m^2(2omega^2+m^2)/(3omega^2+m^2)+2omega^2/N^2]` at `K=1`.
Its linear Schwarzschild expansion is `-2*(3/4+2)=-11/2`.
The large constant term in `s_3` by itself is not the correct radiation
source; it partly belongs to the subtracted operator image.

At this leading order the continuum regular mode is `sin(kr)/(kr)`,
`k=sqrt(9omega^2-m^2)~sqrt(8)m`. Keeping the bound envelope during the
integration, rather than integrating a nondecaying constant, gives

```text
integral_0^infinity r exp(-3kappa r) sin(kr)/(kr) dr
 =1/(k^2+9kappa^2),
I_3,leading=-(11/16)c_2 mu m^2 phi_c^3.
```

This exposes a candidate nonzero radiative coefficient with a definite
sign. Taking a weak-binding limit inside the exact integral still needs
control of the core, the Coulomb scattering phase, kinetic corrections and
the remainder. A finite list of numerical examples cannot prove those
uniform bounds, and the existence of an open channel alone does not do so.

The weak-binding family must stay inside the EFT regime. One admissible
limiting path holds the physical regular body and dimensional Wilson
coefficients fixed while reducing `m`; then `alpha_G` and `m R_*` both
decrease. It does not shrink a physical star through the curvature cutoff
at fixed `m`. Nonzero core `K-1` remains part of the exact formula in section
2; its controlled small-source-size contribution is a remainder obligation,
not something proved absent by the `K=1` numerical reference.

With unit mode normalization, the leading hydrogenic central value is
`phi_c=(kappa^3/pi)^(1/2)`. The corresponding leading density scales as

```text
D_3,leading=[121 sqrt(8)/(64 pi^2)] c_2^2 m^12 alpha_G^11.
```

The dependence on `c_2^2` is required: reversing the Wilson-coefficient sign
reverses the source, not the sign of outgoing power. This expression is not
an experimentally established rate, and no extrapolation to the physical
ultralight mass is validated by a larger-alpha reference calculation.

## 4. A regular geometry and a consistent bound/continuum solve

For numerical control choose a uniform-density GR star, compactness
`C=mu/R_*<4/9`. Its prescribed matter distribution is common GR source data
for this reference family, not an arena-specific MTS charge. Interior:

```text
h=1-2mu r^2/R_*^3,
N=[3sqrt(1-2C)-sqrt(h)]/2,  a=h^(-1/2).
```

Exterior: `N=sqrt(1-2mu/r)`, `a=1/N`. The central lapse is positive; a
regular center replaces an invented reflecting stellar surface. These
metrics and gravitational bound-state comparisons are discussed by
[Lehn, Chabysheva and Hiller](https://arxiv.org/abs/1711.00735).

The equation used here is derived independently from our action:

```text
phi''+[2/r+N'/N-a'/a]phi'
       +a^2(omega^2/N^2-m^2)phi=0   (K=1).
```

In particular, `Na=1` is not imposed on the interior. Nor is its Hilbert
weight replaced by a spatial volume normalization: our mode norm is
`4pi integral (a/N)r^2 phi^2 dr`. Separate integrations on either side of
the stellar surface preserve the correct matching. The reference contains
idealized matter and is not presented as a reconstructed real star.

The script sets `m=c_2=1` only as a dimensionless calculation. It finds the
bound eigenvalue by matching regular outward and decaying inward solutions;
both the original and reduced third-harmonic sources are then integrated
against the regular continuum of the same metric. The outgoing solution
retains the Schwarzschild Coulomb logarithmic phase. Two asymptotic orders,
two tolerances and two outer radii test the finite calculation. The explicit
finite-boundary subtraction identity and an independently integrated
Rayleigh quotient are checked as well.

Restoring units and a normalized bound mode gives
`D_3=c_2^2 m^12 D_dimensionless`. For an unnormalized mode, divide by its
norm cubed before applying this scaling. The historical controlled `c_2`
rows from the previous companion provide a matching coefficient, but do not
provide the actual stellar/cosmological geometry or initial amplitude.

## 5. Physical scale and remaining theorem boundary

The stored parent gap is of order its fitted `H_0`. Then
`H_0 a_B=(H_0/m)^2/(mu H_0)` can be very large for a local gravitating body.
An asymptotically static bound cloud can extend far beyond a physically
valid static cosmological patch. The already derived small local projection
bound remains useful, but this global static calculation cannot be used to
claim preparation of the actual expanding state. The source's tiny quartic
coefficient also cannot be converted into rapid universal relaxation without
a calculated amplitude and time comparison.

The selected prepared two-derivative GR/Newton/Maxwell branch remains intact.
This work investigates a physical route toward preparation rather than
replacing it with an axiom. Full O4/higher-operator control, nonlinear
mode-mixing/backreaction, continuum error bounds and actual state history
remain separate from a positive converged reference density.

## 6. Do not omit the same-order gravitational source

The contact calculation is not the complete cubic parent source. The
canonical scalar stress is quadratic in amplitude and perturbs the metric
at that order; applying the perturbed wave operator to the first-order
field produces another third-harmonic source at **the same amplitude order**.
The parent already supplies its coupling through calibrated `G_N`.

In polar-areal gauge, with the asymptotic clock fixed, consider a vacuum
Schwarzschild exterior `f=1-2mu/r`, `N^2=f`, `a^2=1/f`, and canonical
`chi=A phi cos(omega t)`. Define the oscillating metric pieces by

```text
delta ln(a)=A^2 B(r) cos(2omega t),
delta ln(N)=A^2 C(r) cos(2omega t).
```

The static order-`A^2` metric piece also exists but produces only a first
harmonic at the cubic source order considered here. Let `M_2` denote the
coefficient of `A^2 cos(2omega t)` in the geometrical mass function, not a
new fitted mass. The canonical Einstein constraints give

```text
M_2=pi G_N f r^2 phi phi',
B=pi G_N r phi phi',
C'=pi G_N [phi phi'/f
            +r(phi'^2-(omega^2/f^2+m^2/f)phi^2)],
C(r)=-integral_r^infinity C'(s) ds.
```

For example, the bound eigen-equation gives
`(f r^2 phi phi')'=r^2[f phi'^2+(m^2-omega^2/f)phi^2]`.
This proves the oscillating Hamiltonian constraint. The time/flux
constraint independently fixes the same `M_2`; it is not an arbitrarily
chosen oscillation of the central source. These are exterior formulas with
no other oscillating exterior matter. A consistent dynamical matter
interior, matching and any incoming metric perturbations still matter.

Varying the full time-dependent wave operator, including
`(a_t/a-N_t/N)chi_t`, gives

```text
s_3,gravity=[-2omega^2 C+(2omega^2-fm^2)B]phi
                 +(f^2/2)(C'-B')phi'.
```

Omitting the time-derivative metric term gives the wrong third harmonic.
This source is derived from Einstein-scalar coupling, not an additional
friction coefficient. The spherical Einstein-scalar constraints are also
given in [Valdez-Alvarado, Urena-Lopez and Becerril](https://arxiv.org/pdf/1107.3135);
their potential self-interaction is not our derivative interaction, and no
oscillaton stability theorem is imported here.

For characteristic momentum of order `m`, dimensional comparison of the
contact and tree-gravity four-scalar amplitudes gives
`|c_2|m^2/G_N`. Using the already hash-locked historical gap and matching
coefficients makes this ratio extremely small. It is **not** a ratio of
actual decay rates: propagators, mode shapes, cancellations and scale
matching still enter. It nevertheless prevents us from treating the
contact source as the complete leading nonlinear dynamics.

The two stored matching schemes give `8.967803654087034e-120` and
`8.954114368949628e-120` for this dimensional ratio. These use the historical
gap and the already controlled matching scale, not a newly selected local
renormalization scale. Their smallness does not prove the sign or magnitude
of a total on-shell overlap.

Both sources occupy the same harmonic/channel. The outgoing density is
`D_total=Im<S_contact+S_gravity,R_+(S_contact+S_gravity)>`, including the
interference term. It is not generally `D_contact+D_gravity`. Positivity of
the spectral measure gives
`|sqrt(D_gravity)-sqrt(D_contact)|<=sqrt(D_total)
 <=sqrt(D_gravity)+sqrt(D_contact)` for these two sources. No universal
positive lower bound follows without their actual overlaps.

The best next physical calculation is therefore the combined source with
consistent metric/matter response, not ever more precise contact-only
rates. The explicit exterior source above starts that calculation. It does
not pretend that the regular-star reference has already solved its dynamical
matter interior or the full nonlinear preparation problem.

## Execution record

The radial script is `scripts/parent_radial_overlap_20260906.py`; provenance
and immutable tagged numerical outputs are under
`source-intake/local-preparation/20260906/radial-overlap-*`. Twelve solves
cover six `(alpha_G,C)` cases, each at tolerances `2e-9` and `2e-11` with
outer radii `22/alpha_G` and `28/alpha_G` in inverse-mass units. Fine rows:

| alpha_G | C | omega/m | I_3 / I_3,leading | normalized D_dimensionless |
| ---: | ---: | ---: | ---: | ---: |
| 0.04 | 0.10 | 0.9991893657898462 | 0.9100944103858272 | 3.690821221192322e-16 |
| 0.02 | 0.10 | 0.9997993372629267 | 1.0080768439600039 | 1.702825383069631e-19 |
| 0.01 | 0.10 | 0.9999499586845101 | 1.0163048044723213 | 6.922688740889927e-23 |
| 0.005 | 0.10 | 0.9999874974205036 | 1.0107814828505524 | 2.999298021847271e-26 |
| 0.02 | 0.05 | 0.9997993493863320 | 0.8916915280470727 | 1.1349320083456303e-19 |
| 0.01 | 0.05 | 0.9999499588718527 | 0.9858132012618998 | 6.229305613468028e-23 |

These are positive, converged reference densities, not interval-certified
lower bounds for all bodies or for the physical parent gap. The departure
from the asymptotic coefficient is not monotone; no monotone convergence
theorem or fitted extrapolation is asserted. Interior sensitivity is visible
and retained rather than tuned away.

- `radial-overlap-pilot.json`: 12/12 checks pass.
- `radial-overlap-weak-binding.json`: 12/12 checks pass.
- `radial-overlap-softer-star.json`: 13/13 checks pass, including the exact
  nonconstant-`K` identity. The earlier runner is preserved as
  `radial-overlap-runner-v1.py`; its hash matches the first two run records.
- `scripts/parent_metric_cubic_source_20260906.py` checks the exterior
  Hamiltonian, flux and lapse constraints, the independent metric harmonics,
  the coupling reconstruction and the interference counterexample: 11/11
  checks pass. Its current immutable result is `metric-cubic-checks-final.json`;
  the initial pre-finalization result and runner are retained separately.

All execution is between D4 records 42 and 43, on one core at BelowNormal
priority. Main state hash
`3bef068fc32eba5b3869e5942a6fa27b85a9a35cd5610d2ed23872b93fc2825e`
is preserved across these tests. No broad local-GR, actual-preparation or
full-parent-rate flag is promoted. Numerical checks demonstrate the stated
finite reference calculations, not a full nonlinear PDE theorem.
