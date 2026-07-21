# 5032 — projective causal topology grid and corrected event kernel

## Result

The finite-`x` relative homotopy has been promoted from one event to a
nine-event kinematic stress grid. The correct causal continuation is the
horizontal `z=x+i epsilon` path followed by the vertical lift to
`z=1.5+0.08i`, with `epsilon -> 0+`. Collision roots are transported on the
Riemann sphere rather than judged only in logarithmic coordinates.

All nine events pass projective tracking. They form eight net-winding
topology classes. A representative of every class is invariant under both
`epsilon -> epsilon/10` and homotopy-step doubling. No required refinement
fails.

This checkpoint also supersedes checkpoint 5031's fixed-event topology and
integral. The corrected baseline topology is `(0,2,0,2)`, not `(7,6,7,8)`,
and the corrected fixed-event value is

    I_crossed = 11.4916741 - 13.2855826 i,

with conservative global-quadrature refinement scale `0.00953866`.

## Why checkpoint 5031 is superseded

Two errors were found by the regulator stress test.

First, collision roots followed the selected causal path while the relative
chamber endpoints were independently retransported along straight chords
from the physical point. Surface intersections were therefore being computed
between objects transported by different homotopies. The endpoint transport
now follows the same ordered causal path as the collision roots, and the final
integral uses the resulting lifted endpoint logarithms directly.

Second, the old assignment gate used Euclidean distance in `log xi`. A root
passing smoothly through zero or infinity on the Riemann sphere has an
unbounded logarithmic displacement, so the old gate forced excessive sampling
and could turn a harmless projective passage into a false contour crossing.
For finite roots `r` and `s`, the assignment cost is now the chordal distance

    d_ch(r,s)=|r-s|/sqrt[(1+|r|^2)(1+|s|^2)].

Transitions whose two endpoints are safely beyond the instantaneous radial
range of the finite chamber contour are excluded only when their chordal step
is below `0.1`. Required topology is then checked again under step doubling,
so this exclusion is not accepted from one discretization alone.

The old raised/direct and finite-regulator agreement was therefore agreement
of the wrong transported object. It is retained as derivation history, not as
current evidence.

## `+i0` regulator limit

At the baseline event, independently passing projective runs give the same
net signature for

    epsilon = 3e-4, 1e-4, 3e-5, 1e-5, 1e-6.

The stable four-chamber counts are

    (0, 2, 0, 2).

Finite regulators `0.003` and `0.001` lie on different pre-asymptotic sheets
and are not valid substitutes for the `epsilon -> 0+` limit. The grid uses
`epsilon=1e-5`; every topology-class representative also passes at `1e-6`.

## Nine-event topology grid

| event | `(x,s_z,d_z)` | chambers | net crossings | effective steps |
|---|---|---:|---|---:|
| E00 | `(0.37,0.23,-0.31)` | 4 | `(0,2,0,2)` | 1536 |
| E01 | `(0.12,-0.65,0.45)` | 1 | `(12)` | 12288 |
| E02 | `(0.20,0.62,-0.55)` | 1 | `(12)` | 6144 |
| E03 | `(0.32,-0.25,-0.70)` | 1 | `(6)` | 3072 |
| E04 | `(0.48,0.70,0.12)` | 2 | `(0,0)` | 1536 |
| E05 | `(0.65,-0.72,-0.18)` | 1 | `(2)` | 3072 |
| E06 | `(0.82,0.35,0.72)` | 2 | `(4,6)` | 1536 |
| E07 | `(0.50,0.00,0.00)` | 1 | `(0)` | 768 |
| E08 | `(0.72,0.82,-0.78)` | 2 | `(0,6)` | 3072 |

E01 and E02 share one class; the other seven events define distinct classes.
The maximum accepted projective step is `0.0989703` on the base grid and
`0.0996902` across required refinements, both below the conservative `0.1`
gate.

Raised and direct path diagnostics match the canonical topology in only
`4/16` cases. They are not required to match: the Feynman `+i0` continuation
defines the sheet. Their disagreement demonstrates that the path prescription
is physically consequential rather than a cosmetic numerical choice.

## Corrected baseline kernel

At global-node levels 24 and 32, both using relative orders 128 and 192:

| global nodes | order-192 corrected value | relative-order residual |
|---:|---:|---:|
| 24 | `11.4941307-13.2763657i` | `8.49037e-5` |
| 32 | `11.4916741-13.2855826i` | `8.47749e-5` |

The global-node difference is `0.00953866`, or `5.43018e-4` relative. All
local residue determinations pass. The four surviving winding roots have
residues classified as numerical zero at both quadrature levels, so the net
topological residue correction is `0` at tested precision.

The corrected value differs from checkpoint 5031's reported value by
`0.0861411`. Checkpoint 5031's numerical value must therefore not be used in
subsequent phase-space work.

## Decision

- Coherent endpoint and collision transport: **derived and implemented**.
- Projective zero/infinity root transport: **derived and implemented**.
- Baseline `epsilon -> 0+` topology: **stable across five regulators**.
- Nine-event topology grid: **passed**.
- Eight-class regulator and step refinement: **passed**.
- Corrected baseline crossed event kernel: **passed at smoke precision**.
- Representative integral kernels for the other seven classes: **open**.
- Outer `x`, `s_z`, and `d_z` phase-space integration: **open**.
- Crossing-complete `hhh` cut and UV coefficient: **not yet claimed**.
- Local GR and full MTS: **not claimed**.

Next: evaluate one corrected integral kernel per remaining topology class,
require residue and relative-order convergence, and use those kernels to
design a bounded adaptive outer phase-space smoke run. Do not launch the full
outer integral before the class representatives pass.
