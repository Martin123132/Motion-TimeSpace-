# 248 - Projector-Stress Zero or Retained Theorem

Private local-derivation checkpoint. This is not a public `q_loc`, beta, PPN,
local-GR, or field-theory completion claim.

## 1. Trigger

Checkpoint 247 made local GR a finite premise stack.

The nearest hard blocker is:

```text
N5_projector_stress.
```

The question:

```text
does T_projector vanish,
or must it be retained in the Bianchi ledger?
```

## 2. Machine Artifact

Script:

```text
scripts/projector_stress_zero_or_retained_theorem.py
```

Run:

```text
runs/20260601-000065-projector-stress-zero-or-retained-theorem
```

Command:

```text
python scripts/projector_stress_zero_or_retained_theorem.py --timestamp 20260601-000065
```

Status:

```text
projector_stress_zero_route_not_derived_retained_Bianchi_ledger_written_metric_only_gate_open_no_promotion
```

Claim ceiling:

```text
N5_projector_stress_fork_no_metric_only_EH_beta_or_local_GR_promotion
```

## 3. Projector Variation

For a schematic projector action:

```text
S_proj = 1/2 <J, P_mem J>_B,
```

the metric variation contains:

```text
delta_g S_proj
= 1/2 <J, delta_g B P_mem J>
+ 1/2 <J, B delta_g P_mem J>
+ source variations.
```

Since:

```text
P_mem = 1 - Pi_M - Pi_TF - Pi_matter,
```

we have:

```text
delta P_mem
= -delta Pi_M
- delta Pi_TF
- delta Pi_matter.
```

So projector stress cannot be assumed away.

It has named owners:

```text
T_Meff,
T_TF,
T_rel,
T_projector,
T_boundary.
```

## 4. Zero-Stress Route

To prove:

```text
T_projector = 0,
```

the parent theory must show:

```text
delta_g B = 0,
delta_g P_mem = 0,
or all projected-current support is exact/pure boundary with no bulk variation.
```

Current status:

```text
not derived.
```

Why:

```text
the boundary Hodge/DeWitt metric is metric-dependent,
the boundary primitive A_rel is not parent-selected,
and N1-N4 are conditional gates rather than parent theorems.
```

So:

```text
T_projector = 0
```

is not earned yet.

## 5. Retained-Stress Route

The honest Bianchi route is:

```text
T_total =
T_metric
+ T_Meff
+ T_TF
+ T_rel
+ T_projector
+ T_X
+ T_boundary.
```

Then require:

```text
nabla_mu T_total^{mu nu}=0
```

on shell from the parent variational identity.

This is the only valid route unless zero-stress is proven.

But it creates a fork:

| case | consequence |
|---|---|
| `T_projector = 0` | metric-only EH stack can continue |
| `T_projector` boundary-only | EH stack can continue with boundary term |
| bulk `T_projector` retained | Bianchi may be safe, but exterior is not metric-only EH |
| `T_projector` dropped | fake conservation; forbidden |

## 6. N5 Result

The result is:

```text
N5 is not closed.
```

But it is now sharply split:

```text
for local GR, T_projector must be zero or boundary-only;
for general consistency, T_projector must at least be retained.
```

So the local EH stack survives only if:

```text
T_projector has no bulk exterior stress.
```

## 7. What Improved

Before this checkpoint:

```text
projector stress was an open warning.
```

After this checkpoint:

```text
projector stress has an exact fork:
zero/boundary-only -> EH route can continue,
bulk retained -> modified exterior,
dropped -> invalid.
```

This is good discipline.

It keeps the theory honest.

## 8. What Still Fails

Still not derived:

```text
T_projector = 0,
T_projector boundary-only,
or the full parent variational Bianchi identity.
```

Therefore:

```text
metric-only EH exterior is not promoted,
beta = 1 is not promoted,
local GR is not promoted.
```

## 9. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| projector zero-stress theorem derived | fail |
| retained projector-stress ledger written | pass |
| metric-only EH compatible `N5` cleared | fail |
| dropped projector stress route rejected | pass |
| local GR or PPN promoted | fail |

## 10. Decision

Decision:

```text
projector_stress_zero_route_not_derived_retained_Bianchi_ledger_written_metric_only_gate_open_no_promotion
```

Meaning:

```text
N5 is now a precise fork. Zero-stress is not derived; retained stress is the
honest Bianchi contract; bulk retained stress prevents metric-only EH.
```

Main gain:

```text
projector stress can no longer hide.
```

Main failure:

```text
T_projector zero/boundary-only status is still not parent-derived.
```

## 11. Next Target

Create:

```text
249-projector-boundary-only-condition-or-metric-only-reduction-fail.md
```

Purpose:

```text
try to prove projector stress is boundary-only under exact/pure-gauge relative
memory, or explicitly mark the metric-only EH reduction as blocked by bulk
projector stress.
```

Pass condition:

```text
T_projector|bulk exterior = 0
```

with any remaining term moved to a well-posed boundary variation.

Fail condition:

```text
bulk projector stress is silently treated as compatible with vacuum EH.
```
