# 5164 - Mass-conserving visible--motion initial-value response gate

Marker: `MTS_5164_MASS_CONSERVING_VISIBLE_MOTION_INITIAL_VALUE_GATE`.

Date: `2026-07-20`.

## What was changed

Checkpoint 5163 showed that the existing visible Hilbert source has enough
leverage but tested it with a scalar response efficiency. That scalar has now
been removed. The checkpoint-5162 antithetic `NESTED160` particle states are
regenerated, their physical positions and velocities are retained, and the
motion particles are evolved through the spherical Newtonian projection of
the same checkpoint-4947 Einstein source.

The source split is mass-conserving. If `d_i` marks particles initially inside
the fixed halo edge, then

```text
m_g,i(lambda)=m_p-lambda Delta_m d_i,
Delta_m=M_b,obs(R_edge)/N_d,
M_g(<r,lambda)=sum_(i<r)m_g,i-M_background(<r)
              +lambda M_b,obs(<r).
```

Consequently `N_d Delta_m=M_b,obs(R_edge)` and the total source outside the
edge is independent of `lambda` exactly. Measured condensed baryons are
`0.48348752008544155` of the donor
particles' cosmic baryon allotment. The remaining baryons stay particle-tied;
they are not deleted. No new coupling, response efficiency or target inversion
is used.

## Initial-value calculation

The isolated source-response system retains the actual three-dimensional
position, velocity and angular-momentum samples of both antithetic
cosmological phases. The primary matrix uses exact-mass radial compression;
the near-boundary branch is repeated with every original particle. The force
is spherical only in its source projection:

```text
d2 x_i/dt2=-G_N M_g(<r_i,t) x_i/(r_i^2+epsilon^2)^(3/2).
```

`epsilon` is one half of the inherited `NESTED160` force cell. Source growth
is tested with predeclared impulsive, Newton-freefall, one-orbit and converging
adiabatic clocks. Their values are fixed before the parent `q` is read. Each
source run has a matched `lambda=0` control, and the response estimator applies
the source/control ratio to the regenerated checkpoint-5162 profile so that
isolated-control relaxation is not mistaken for a coupling.

The regenerated fine-grid value is `q=3.688824512640322` versus
the stored `q=3.688824512640355`. The baseline no-refit velocity-
squared RMSE is `0.42140386547507747` dex.
Its transition velocity-squared ratio is `0.20525141123436702`.

## Result

The predeclared histories span corrected `q` from
`2.2069358661442315` to `2.9057196818657376` and
RMSE from `0.2655573403086304` to
`0.34984502366610953` dex. Histories inside the existing
checkpoint-5162 `q` envelope: `[]`.

The mass-conserving circular adiabatic comparator gives
`q=0.23704123622245601` and RMSE
`0.116709324250618` dex. The dynamic adiabatic
four-to-eight-orbit `q` difference is
`0.05747733879589889`; the doubled-time-step-resolution
difference is `0.003481376334322217`.

The near-boundary one-orbit branch gives primary, doubled-timestep and full-
particle values `q=2.2069358661442315`,
`2.196497562958223` and
`2.2235536913099607`. Its refinement interval intersects
the inherited parent band: `True`.
This is a numerical compatibility statement only; the one-orbit condensation
clock was predeclared but has not been selected by the parent field equations.
Its primary RMSE is `0.27569297375275253` dex and its transition velocity-
squared ratio is `0.3841731626520422`: the source roughly doubles the baseline
transition support, but a substantial amplitude deficit remains.

Route decision: **ONE_ORBIT_VISIBLE_SOURCE_RESPONSE_INTERSECTS_PARENT_BAND_UNDER_NUMERICAL_REFINEMENT_BUT_ASSEMBLY_HISTORY_NOT_PARENT_SELECTED**.

This is a genuine forward initial-value response calculation, not an inverse
efficiency fit. It does not yet derive the baryonic condensation history from
Maxwell/radiative hydrodynamics, so every row remains nonclaim. The calculation
either supplies a controlled source-response bound or identifies precisely
what source-history dynamics must be derived next.

## Claim boundary

```text
same-G_N two-component force derived                 = yes;
condensed plus diffuse baryon mass conserved         = yes;
scalar response efficiency removed                   = yes;
three-dimensional inherited orbital state evolved    = yes;
baryonic condensation history parent-selected        = no;
local GR/Newton/Maxwell branch modified               = no;
galaxy or full-MTS claim                              = false.
```

All `23` validation rows pass. Source hashes are
unchanged and the protected `formalization-workbench` digest is
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. The galaxy source was
read-only and no GitHub action occurred.
