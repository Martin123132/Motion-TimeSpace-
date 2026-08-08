# 5157 - Composite motion clock, charge-entropy adiabatic state-preparation re-entry gate

Marker: `MTS_5157_COMPOSITE_MOTION_CLOCK_ADIABATIC_STATE_PREPARATION_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5156 proved that an action Hessian does not select a statistical
state. This checkpoint therefore attempts a parent mechanism rather than
running an expensive collapse from a borrowed covariance. The corpus already
contains the checkpoint-4890 Cartesian pair

```text
Z=X_1+iX_2=A exp(-i m_X U).
```

Its polar decomposition is exact, its phase supplies a timelike WKB flow, and
its amplitude supplies a conserved neutral motion density. The pair can reduce
the arbitrary functions `n_k,c_k` to one common curvature covariance plus one
global charge-to-entropy yield **if** a one-clock reheating law produces that
yield. The isolated quadratic pair cannot generate a nonzero charge from zero,
so the active parent has not yet earned this state law. The result is a real
conditional derivation and an equally real source obstruction, not a claim.

## 1. Exact Cartesian-to-clock map

For two degenerate neutral real modes,

```text
(grad X_1)^2+(grad X_2)^2
 =(grad A)^2+m_X^2 A^2(grad U)^2,
J_X^mu=m_X A^2 u^mu,
u_mu=-grad_mu U,
div J_X=0.
```

The symbolic identities pass exactly: kinetic identity
`True` and current identity
`True`. Varying the amplitude gives

```text
(grad U)^2+1=Box A/(m_X^2 A).
```

Thus `U` is a proper-time flow only where the WKB ratios are small. At `A=0`
the polar chart is undefined, but `X_1=X_2=0` is a completely regular
Cartesian vacuum with zero pair stress. This distinction prevents a clock
coordinate singularity from being mislabelled as a physical local coupling.

The internal `U(1)_X` is global and neutral. It is not electromagnetic charge.
Maxwell, Lorentz force and Poynting momentum continue to use the checkpoint-4947
Hilbert source without another coefficient.

## 2. Dust, motion and time from the same occupied state

In the controlled WKB branch,

```text
n_X=m_X A^2+corrections,
rho_X=m_X n_X=m_X^2 A^2+O(H^2 A^2),
p_X/rho_X=O(H^2/m_X^2),
n_X a^3=constant.
```

The largest executed equality pressure proxy is `7.917149134876045e-15`. The same
nonrelativistic envelope gives the checkpoint-5155 Schrodinger--Poisson system,
so this is not a new galaxy force. It is one candidate microscopic identity
for the motion occupation and its clock.

## 3. Exact charge-to-entropy adiabatic theorem

After a one-clock production event, suppose

```text
J_X^mu=n_X u^mu,       div J_X=0,
s^mu=s u^mu,           div s=0.
```

Then

```text
u.grad ln(n_X/s)=0.
```

The symbolic transport residual is exactly
`0`. If the production
hypersurface has one spatially uniform yield `Y_X=n_X/s`, separate-universe
evolution gives

```text
S_Xgamma=delta ln(n_X/s)=delta_X-3 delta_gamma/4=0,
P_SS=P_RS=0.
```

This is stronger than choosing a convenient Gaussian covariance after the
fact. It is also conditional: the current parent does not yet derive the
one-clock charge-production operator or its noise.

For the three locked masses the required present yield spans
`4.399658552450225e+17` to `1.561995092172403e+20`. Planck 2018 gives the 95 percent scale-invariant
uncorrelated CDI bound `beta_iso(k=0.05/Mpc)<0.038`. Any uncorrelated production
noise must therefore have fractional rms below `9.10081172951104e-06` for the
checkpoint-5156 curvature amplitude.

For comparison, retaining the real misalignment state as a light uncorrelated
spectator gives the conditional range

```text
H_inf < 389344004363.5486 ... 1690046539761.0183 GeV.
```

That is a bound on an unprepared branch, not a derivation of its state.

## 4. Exact charge-generation obstruction

The same conservation law that makes the clock branch disciplined prevents
the isolated pair from creating its own net charge:

```text
Q_X(t_initial)=0  =>  Q_X(t)=0.
```

A charge present before 60 inflationary e-folds is diluted in density by
`exp(-180)=6.714184288211594e-79`. A viable route therefore needs either a
parent boundary charge or an explicit charge-asymmetric one-clock production
operator after inflation. Symmetric gravitational pair production cannot be
renamed as net charge. If no such operator can be derived, the clock-charge
branch must be rejected and the real-scalar state remains external data.

Checkpoint 4896 retired the full diagonal bath cosmology. This checkpoint does
not restore it. Only the coherent Cartesian pair is being tested for separate
re-entry; checkpoint 4897 remains the active metric-only background until the
re-entry gates close.

## 5. Machine-cog inheritance

With the same `m_X`, `Omega_X` and a genuinely adiabatic production state, the
checkpoint-5156 sound speed, radiation transfer and patch calculation are
unchanged. Its `1050` of
`1050` patches remain inside the one-sigma
linear collapse gate. Locally, the Cartesian vacuum leaves GR/Newton/Maxwell
untouched; in an occupied galaxy the same neutral Hilbert stress gravitates.
No arena switch or galaxy-only coupling is introduced.

This does **not** derive the nonlinear `q_parent` profile, finite wave core or
`p=2` edge. Those remain the next no-refit dynamical test.

## 6. Status and next calculation

```text
Cartesian pair to amplitude plus clock                 = exact;
neutral Noether current and WKB dust                   = derived;
local Cartesian zero-stress branch                     = exact;
charge/entropy adiabatic theorem                       = exact conditional;
arbitrary covariance reduced to curvature plus Y_X    = conditional advance;
net charge generation from isolated quadratic pair    = rejected exactly;
one-clock production operator and stochastic noise    = not parent-derived;
active-parent pair re-entry                            = not promoted;
q/core/p=2 nonlinear formation                         = not derived.
```

The next derivation target is narrow and constructive: search the existing
parent vertices for a post-inflation charge-asymmetric source whose local rate
depends on the same clock and whose stationary/local residue vanishes. If none
exists, reject this re-entry rather than inventing one. Once state production
is owned, execute the frozen no-refit Vlasov-volume plus wave/density-matrix
zoom and score `q_parent`, core and edge directly.

Primary source for the isocurvature bound:
https://arxiv.org/abs/1807.06211. All generated rows remain nonclaim. The
protected `formalization-workbench` digest remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No
GitHub action occurred.
