# 5162 - Shared-mode nested transition zoom and resolved-q gate

Marker: `MTS_5162_SHARED_MODE_NESTED_TRANSITION_ZOOM_Q_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5162 executes the transition zoom required by checkpoint 5161.
It does not add a galactic force. The global `192^3` periodic PM force is
retained and a local zero-Dirichlet correction solves the difference between
the fine and prolonged coarse Lagrangian density contrasts. Source and force
tapers vanish before the local boundary, and the weighted correction has zero
net momentum. The correction is multiplied by the numerical reliability
factor `N_cell/(1+N_cell)`, where `N_cell` is the coarse-density estimate of
particles per fine cell; unresolved particle shot noise therefore cannot act
as a new physical source.

## 1. Controls

Both Gaussian-force controls, the homogeneous lattice and the taper ordering
pass. The largest analytic Gaussian force error is
`0.014083024791743393`. The homogeneous nested force is
`0.0`. The largest executed source-boundary
ratio is `0.004129904468415234` and the largest centre
step is `0.18085950283162297` Mpc. Unconstrained candidate
centres can move by `0.9293048337853592` Mpc, so
the interface enforces overlapping local boxes and independently requires its
final tracked centre to agree with the final halo; the largest residual is
`0.0` Mpc.

## 2. Resolved transition

The local grids are 128 and 160 in a fixed four-edge-radius box. Their
three-cell resolved radii are `33.9111567809293` and
`27.128925424743443` kpc, both below the frozen
`36.43917542575495` kpc transition. Four paired runs
execute `424673280` particle-step updates.

At the frozen transition,

```text
q_parent                          = 1.858483853942984;
q_nested_128                      = 3.342318295377389;
q_nested_160                      = 3.688824512640355;
resolution difference            = 0.34650621726296604;
fine-grid phase half-range       = 0.3415301479555537;
parent-minus-fine absolute value = 1.830340658697371;
q selection gate                 = NOT_SELECTED.
```

The profile convergence gate is `PASS`.
The q result is diagnostic and nonclaim even if selected because it contains
one antithetic phase pair rather than an ensemble.

## 3. Edge and machine-cog limits

The local interface begins outside `1.25 R_edge`, so the transition and the
entire target edge lie inside the untapered force-correction region. Even so,
the compact edge is not promoted to a formation claim because the local box
size was chosen from the frozen edge and the calculation is designed to test
`q`, not select `p=2`.

The action, metric, `G_N`, visible source, Maxwell stress and Poynting momentum
are unchanged. The local GR/Newton/Mercury branch and the galactic occupied
branch remain states of one parent law. If q fails after numerical convergence,
the free collisionless state does not derive the parent phase flow and an
actual parent interaction or wave stress is required; no closure may be
inserted to repair it.

All `29` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. Galaxy inputs were read-only
and no GitHub action occurred.
