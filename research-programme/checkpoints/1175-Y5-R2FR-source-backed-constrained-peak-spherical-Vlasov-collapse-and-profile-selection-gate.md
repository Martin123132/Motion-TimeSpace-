# 5159 - Source-backed constrained-peak spherical Vlasov collapse and profile-selection gate

Marker: `MTS_5159_CONSTRAINED_PEAK_SPHERICAL_VLASOV_COLLAPSE_GATE`.

Date: `2026-07-20`.

## Decision

This checkpoint performs the first genuinely nonlinear, shell-crossing
formation calculation after the covariance and state gates. It freezes the
checkpoint-5156 Planck-normalized adiabatic comparator, conditions one
top-hat patch at exactly one covariance standard deviation, and evolves the
resulting cold spherical phase-space sheet from `a=0.02` to `a=1`.
No `q_parent`, transition radius, edge radius, edge power, halo mass or
profile amplitude is adjusted after evolution.

The result is deliberately narrower than a full cosmological claim. A
spherical conditional mean has zero angular momentum and therefore cannot
become the isotropic Eddington state constructed at checkpoint 5154. The run
tests whether this least-stochastic nonlinear branch nevertheless selects the
same density/support shape. It does not substitute for the residual Gaussian
field, tidal torques or a wave-resolved core.

## 1. Frozen Gaussian constraint

For the source-backed power spectrum `P_X(k)`, the top-hat covariance is

```text
sigma_R^2 = integral dlnk Delta_X^2(k) W^2(kR),
Cov(q,R)  = integral dlnk Delta_X^2(k) W(kq)W(kR).
```

The exact conditional mean for the fixed one-sigma constraint is

```text
delta_R=sigma_R,
delta_bar(q)=delta_R Cov(q,R)/sigma_R^2.
```

This uses all 4096 source modes for each locked mass and has no stochastic
seed. The maximum relative disagreement with the independently executed
checkpoint-5156 patch sigma is
`0.0`.

## 2. Nonlinear equations actually integrated

Each Lagrangian shell carries its exact background mass. The growing-mode
Zel'dovich initial data are

```text
x(q,a_i)=q[1-D_i delta_bar(q)/3],
P(q,a_i)=a_i^2 E_i f_i D_i[-q delta_bar(q)/3],
P=a^2 dx/dt/H0.
```

After every shell crossing the enclosed mass is re-sorted. The KDK system is

```text
dx/da=P/(a^3 E),
dP/da=F_delta/(a^2 E),
F_delta=-G[M(<|x|)-4pi rho_m0 |x|^3/3]
        sign(x)|x|/[H0^2(|x|^2+epsilon^2)^(3/2)].
```

The base execution contains `6` nonlinear runs,
`48000` evolved shells and
`18000` base KDK steps. Every base branch
undergoes shell crossing; the first crossing scale factor spans
`0.3064394931565472` to
`0.5897107563693249`.

## 3. Exact radial-sheet obstruction

For a spherical potential,

```text
dL/dt = r cross (-grad Phi)=0.
```

The conditional-mean growing mode has `L=0`, hence all characteristics retain
`L=0`. No amount of radial shell crossing can turn this phase-space sheet into
the positive isotropic `f(E)` state from checkpoint 5154. This is an exact
subbranch no-go, not a numerical failure. Any formation proof for that state
must retain the residual covariance and nonspherical tidal torques, or derive
another parent collision/interaction that changes angular momentum.

## 4. No-refit profile result

Both parent mappings are scored against both predeclared references and all
three locked masses. The fixed-edge motion-mass ratios span
`0.5639697785525986` to
`7.4250800627151685`. The no-refit velocity-squared
log-RMSE spans `0.3831486509284557` to
`0.7406070274151968` dex over resolved bins.

Resolved transition diagnostics exist for
`6` of
`12` scores. Their inferred `q` range is
`-1.3874270392792307` to
`0.6222102147179054`, compared with the frozen parent range
`1.8496934455116607` to `1.858483853942984`.

The radial branch selects a compact universal `p=2` edge in
`0` of `12`
scores. Its smallest density ratio immediately outside versus inside the
fixed edge is `0.4566901309657973`. Therefore a
smooth vacuum edge is not promoted merely because an equilibrium with that
edge exists.

## 5. Numerical controls

The exactly homogeneous shell control has maximum comoving drift
`0.0`. The early growing
mode agrees with its independent Zel'dovich enclosed-density prediction to
`0.0032607463063611952`. The fixed UGC09133
benchmark was repeated across shell count, step count and softening controls;
the convergence envelope in fixed-edge mass ratio is
`0.4667440830072318` and the resolved
velocity log-RMSE span is
`0.5990970882923841`.

Those nonlinear spans fail the predeclared ten-percent/0.1-dex convergence
gate, so the displayed `q` and profile-RMSE values are diagnostics only and
must not be read as a physical rejection of `q_parent`. This is a fail-closed
pipeline result. All `7` base/convergence
rows nevertheless retain exterior excess density far above the compact-edge
threshold and none selects `p=2`; the minimum control exterior/interior ratio
is `0.20465370939473415`. The exact radial
angular-momentum obstruction is independent of this numerical sensitivity.

## 6. Machine-cog verdict

No action coefficient, metric, matter charge, `G_N`, electromagnetic source
or local parameter changed. The local zero-state remains the same
GR/Newton/Maxwell branch, including Poynting momentum in the common Hilbert
source. Galactic occupation is a different solution/state of that same law.

The present result is consequently:

```text
source-backed nonlinear shell crossing                   = executed;
profile/edge parameters refitted                         = no;
radial conditional mean becomes isotropic Eddington DF   = rejected exactly;
quantitative radial q/profile convergence                 = failed closed;
compact p=2 edge across every control                      = absent;
radial branch as full q/core/p=2 formation route          = rejected by exact phase-space obstruction;
local GR/Newton/Maxwell cog modified                      = no;
full stochastic 3D Vlasov formation                       = not yet executed;
wave-resolved core selection                              = not yet executed;
parent primordial covariance                              = still conditional.
```

The next legitimate formation calculation is now sharply specified: retain
the residual Gaussian covariance in a paired constrained realization, evolve
its nonspherical tidal field, and score only radii resolved by a convergence
ladder. The radial mean must not be rerun under new labels, and a successful
3-D outer profile still requires a separate wave/density-matrix zoom before a
full MTS galaxy claim.

Primary method references:

- constrained Gaussian fields: https://arxiv.org/abs/astro-ph/9507024
- particle-mesh control: https://arxiv.org/abs/1603.00476
- FDM transfer: https://arxiv.org/abs/astro-ph/0003365
- covariant 2PI state: https://arxiv.org/abs/hep-ph/0409233
- compact Vlasov states: https://arxiv.org/abs/gr-qc/9812061

All `33` validations pass. Every generated row is
nonclaim. The protected `formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. The galaxy corpus was
read-only and no GitHub action occurred.
