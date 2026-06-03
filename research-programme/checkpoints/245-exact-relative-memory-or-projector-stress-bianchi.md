# 245 - Exact Relative Memory or Projector-Stress Bianchi

Private local-derivation checkpoint. This is not a public `q_loc`, beta, PPN,
local-GR, or field-theory completion claim.

## 1. Trigger

Checkpoint 244 preserved the ordinary mass channel:

```text
absolute S^2 flux -> M_eff.
```

The next gate is:

```text
N4/N5.
```

After ordinary mass is preserved, the relative memory sector must be exact or
pure gauge, and projector stress must not fake conservation.

## 2. Machine Artifact

Script:

```text
scripts/exact_relative_memory_or_projector_stress_bianchi.py
```

Run:

```text
runs/20260601-000062-exact-relative-memory-or-projector-stress-bianchi
```

Command:

```text
python scripts/exact_relative_memory_or_projector_stress_bianchi.py --timestamp 20260601-000062
```

Status:

```text
N4_exact_relative_memory_gate_locked_N5_projector_stress_Bianchi_obligation_open_no_q_loc_or_PPN_promotion
```

Claim ceiling:

```text
N4_N5_conditional_gate_no_q_loc_beta_or_local_GR_promotion
```

## 3. Exact Relative Memory Gate

The non-cheating projector split is:

```text
P_mem = 1 - Pi_M - Pi_TF - Pi_matter.
```

So the relative memory current has:

```text
no absolute S^2 mass flux,
no trace-free shear block,
no direct matter/clock block.
```

If the parent source identity gives:

```text
d_rel(P_mem J_rel) = 0,
```

then on:

```text
Sigma_ext ~= S^2 x I
```

with relative boundary primitive:

```text
H^2(Sigma_ext, partial Sigma_ext)=0.
```

Therefore:

```text
P_mem J_rel = d_rel A_rel.
```

If:

```text
A_rel|boundary
```

is pure gauge or boundary-cancelled, then:

```text
d_rel(P_mem J_rel)=d_rel^2 A_rel=0.
```

With the source identity:

```text
q_loc^nu = -P_loc d_rel(P_mem J_rel)^nu = 0.
```

That is the N4 gate.

## 4. The N5 Trap

N4 is not enough by itself.

If the projector depends on the metric or boundary metric, then:

```text
delta_g P_mem != 0.
```

So:

```text
T_projector
= -(2/sqrt(-g)) delta S_projector / delta g
```

must either:

```text
vanish by the same exact/pure-gauge theorem,
```

or:

```text
be retained in the total Bianchi ledger.
```

Forbidden shortcut:

```text
use P_mem to make q_loc vanish,
then drop delta P_mem/delta g.
```

That is fake conservation.

## 5. Bianchi-Safe Options

There are only three routes:

| route | verdict |
|---|---|
| projector stress vanishes | possible, not derived |
| projector stress retained in total stress | formal route, not computed |
| projector stress dropped | rejected |

The total ledger must contain:

```text
T_matter
+ T_metric
+ T_Meff
+ T_TF
+ T_rel
+ T_projector
+ T_X
+ T_boundary.
```

and satisfy:

```text
nabla_mu T_total^{mu nu}=0
```

on shell.

## 6. What Improved

Before this checkpoint:

```text
relative memory exactness and projector stress were adjacent blockers.
```

After this checkpoint:

```text
N4 is locked as a conditional topology theorem,
N5 is the conservation police that decides whether N4 is usable.
```

Meaning:

```text
relative memory can be harmless only if exactness and Bianchi accounting travel
together.
```

## 7. What Still Fails

Still not derived:

```text
P_mem from the parent boundary metric,
the parent source identity,
the A_rel representative,
T_projector = 0,
or the full retained projector-stress conservation law.
```

Still open:

```text
N6 auxiliary no-hair,
metric-only Einstein-Hilbert exterior,
beta = 1,
local GR.
```

So this checkpoint does not claim:

```text
q_loc = 0 publicly,
beta = 1,
PPN pass,
local GR.
```

## 8. Coefficient Status

| residual | status after 245 |
|---|---|
| `beta - 1` | still open; q_loc piece conditionally sharpened |
| `G_eff/G - 1` | unchanged; `N1` conditional |
| `gamma - 1` | unchanged; `N2` conditional |
| `Phi - Psi` | unchanged; `N2` conditional |
| `epsilon_matter` | unchanged; `N3` conditional |
| `alpha_clock` | unchanged direct-vertex gate; metric/C branch open |

## 9. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| `N4` exact relative memory topology chain written | conditional pass |
| `q_loc` public silence claimed | fail |
| `N5` projector stress cleared | fail |
| dropped projector-stress route rejected | pass |
| local GR or PPN promoted | fail |

## 10. Decision

Decision:

```text
N4_exact_relative_memory_gate_locked_N5_projector_stress_Bianchi_obligation_open_no_q_loc_or_PPN_promotion
```

Meaning:

```text
relative memory harmlessness now has a precise exactness theorem and an
explicit conservation police gate.
```

Main gain:

```text
we no longer allow P_mem to be used as a magic eraser.
```

Main failure:

```text
projector stress and auxiliary no-hair remain open, so q_loc, beta, PPN, and
local GR are not promoted.
```

## 11. Next Target

Create:

```text
246-auxiliary-nohair-rank-bracket-or-local-EH-pivot.md
```

Purpose:

```text
attack N6 by deciding whether X/J_rel/V_def are constrained auxiliary fields
with no exterior propagating hair, or pivot back to the local EH exterior
operator.
```

Pass condition:

```text
the rank/bracket tests close and X/J_rel/V_def carry no exterior degrees,
```

or:

```text
the metric-only exterior action is derived independently.
```

Fail condition:

```text
auxiliary fields are declared harmless because the desired exterior is GR.
```
