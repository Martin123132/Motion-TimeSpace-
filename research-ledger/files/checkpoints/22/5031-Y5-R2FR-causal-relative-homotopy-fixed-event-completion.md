# 5031 — causal relative homotopy and fixed-event completion

## Result

The failed endpoint-joined logarithmic spiral from checkpoint 5029 has been
replaced by a causal homotopy of the complete off-unit collision set. At the
fixed finite-`x` event

    x=0.37,  s_z=0.23,  d_z=-0.31,  z=1.5+0.08i,

the crossed nested two-azimuth integral now passes independent topology,
residue, relative-order, and inner-global-quadrature gates.

This is a fixed-event completion only. The integrations over `x`, `s_z`, and
`d_z` remain open.

## Causal homotopy law

Write the relative azimuth as `xi=exp(u)`. For physical chamber `i`, let
`a_i(t)` and `b_i(t)` be the continuously lifted logarithms of its two moving
pinch endpoints while the scattering cosine follows an upper-half-plane path
`z(t)`. The simple reference surface is

    u_i(t,s)=a_i(t)+s[b_i(t)-a_i(t)],   0<=s<=1.

For every collision `p_k(t)` between global poles with opposite physical
ownership, define its lifted surface coordinate

    q_ik(t)=[log p_k(t)-a_i(t)]/[b_i(t)-a_i(t)].

An interior sign change of `Im q_ik`, with `0<Re q_ik<1`, is an intersection
of the collision worldline with the reference surface. Its winding correction
is

    n_ik=+1  for Im q: positive -> negative,
    n_ik=-1  for Im q: negative -> positive.

This turns the previously qualitative statement “the spiral crosses off-unit
collisions” into an executable integer homotopy law.

The four physical chambers contain respectively

    (7, 6, 7, 8)

interior collision crossings. The complete target-root and winding signature
is identical for:

- a raised vertical-then-horizontal upper-half-plane path;
- a direct upper-half-plane path;
- regulators `0.003` and `0.001`;
- `96` and `192` homotopy steps.

The maximum accepted log-root assignment step falls from `0.4280` at 96 steps
to `0.2159` at 192 steps. No winding-sign inconsistency occurs.

## Relative residue completion

For the global-cycle value `F_i(xi;z)` in chamber `i`, each relevant collision
has relative residue

    R_ik=(1/2 pi i) integral F_i(xi;z) dxi/xi.

The causal chamber is the straight transported chamber plus the integer
collision loops,

    I_i^causal=I_i^straight + sum_k n_ik R_ik.

Near-target poles are subtracted in `u` before quadrature,

    F_i(exp u) -> F_i(exp u)-sum_k R_ik/(u-u_ik),

and the subtracted terms are restored by their exact straight-segment
logarithms. Inner and outer local residue circles either agree within the
stability threshold or both classify the candidate as numerical zero.

The summed topological correction is

    Delta I_top=-0.0020232063-0.0861173190 i.

Its global-node-24 and global-node-32 determinations differ by only
`9.06e-11`.

## Convergence gate

At relative orders 128 and 192:

| inner global nodes | order 128 | order 192 | relative-order residual |
|---:|---:|---:|---:|
| 24 | `11.4930019-13.3636760i` | `11.4921075-13.3624831i` | `8.46e-5` |
| 32 | `11.4882558-13.3711791i` | `11.4896509-13.3716999i` | `8.45e-5` |

The order-192 global-node refinement difference is `0.00954`, or
`5.41e-4` relative. The fixed-event value is therefore recorded conservatively
as

    I_crossed=11.4897-13.3717 i,
    numerical refinement scale <=0.00954.

This value is not the rejected checkpoint-5028 spiral value. It includes the
full causal collision winding correction and a converged pole-subtracted
relative integral.

## Decision

- Full off-unit collision homotopy at the fixed event: **derived**.
- Path, regulator, and homotopy-step invariance: **passed**.
- Relative residues and pole subtraction: **passed**.
- Fixed-event crossed two-azimuth integral: **passed at smoke precision**.
- Outer `x`, `s_z`, and `d_z` phase-space integrations: **open**.
- Crossing-complete `hhh` cut and UV coefficient: **not yet claimed**.
- Local GR and full MTS: **not claimed**.

Next: use the fixed-event causal cycle as the event kernel, test a small
multi-event grid for topology changes, and only then launch the bounded outer
phase-space integration.

