# 252 - Topological Projector Parent Action Skeleton

Private derivation checkpoint. This is a parent-action skeleton, not a finished
parent action, local-GR proof, PPN pass, CMB bridge, or `B_mem = 2/27`
derivation.

## 1. Trigger

Checkpoint 251 found the clean N5 route:

```text
P_mem must be metric-independent and topological/relative in the local
exterior, not Hodge/orthogonal/least-energy.
```

This checkpoint asks whether that condition can be owned by a parent action
rather than left as a closure axiom.

## 2. Machine Artifact

Script:

```text
scripts/topological_projector_parent_action_skeleton.py
```

Run:

```text
runs/20260601-000069-topological-projector-parent-action-skeleton
```

Command:

```text
python scripts/topological_projector_parent_action_skeleton.py --timestamp 20260601-000069
```

Status:

```text
topological_projector_parent_skeleton_written_N5_action_route_conditional_FLRW_Bmem_and_N6_open_no_promotion
```

Claim ceiling:

```text
parent_skeleton_only_no_Bmem_derivation_or_local_GR_promotion
```

## 3. Skeleton

The minimal N5-compatible skeleton is:

```text
S_parent =
  S_EH[g]
  + S_matter[Omega_D e, matter]
  + int Xi wedge d_rel J_rel
  + int Upsilon wedge (P_D J_rel - d_rel A_rel)
  + S_operator[P_D^2=P_D, d_rel P_D=P_D d_rel]
  + S_boundary.
```

The important move is not the notation. The important move is:

```text
all projector/memory ownership terms are wedge/topological terms with no Hodge
star, no metric inner product, and no sqrt(-g) bulk potential.
```

If `P_D` is induced by domain/topology/relative-chain data rather than by the
metric, then:

```text
delta_g P_D = 0
```

inside the local exterior.

## 4. Bulk Metric Variation

The local exterior ledger becomes:

| sector | bulk metric variation |
|---|---|
| EH | gives `G_mn + Lambda g_mn` |
| ordinary matter | zero when `T_matter|E = 0` |
| relative closure term | zero if wedge/topological only |
| projection exactness term | zero if `delta_g P_D = 0` |
| operator contract | zero if chain/topological data only |
| boundary term | boundary-only, still shear-checked |

So N5 can be conditionally closed by construction:

```text
T_projector_mn|bulk = 0.
```

But only under the strict topological projector contract.

## 5. What This Derives

This does derive a real sufficient mechanism:

```text
metric-independent relative projector + exact/topological action
=> no bulk projector stress.
```

That is stronger than saying the projector stress “should vanish”.

It gives the parent action a specific job:

```text
own P_mem as P_D, a relative cohomology chain projector.
```

## 6. What It Does Not Derive

This does not yet derive:

```text
B_mem = 2/27,
the FLRW memory projection,
N6 auxiliary no-hair,
boundary trace-free shear silence,
M_eff/G_eff source normalization,
local PPN,
CMB safety.
```

So the bridge has a support beam, not the full road deck.

## 7. FLRW Compatibility Gate

The same `P_D` must reduce to the cosmology projector:

```text
P_D local exterior -> topological no-hair / no bulk stress,
P_D FLRW reduction -> memory projection and eventually B_mem = 2/27.
```

If this fails, then the local projector is only a local repair and the unified
claim weakens.

The no-clock branch remains protected:

```text
domain labels may organize the reduction,
but they cannot become a physical global clock.
```

## 8. Claim Policy

Allowed:

```text
a minimal N5-compatible parent skeleton exists conditionally.
```

Forbidden:

```text
the parent action is complete,
B_mem = 2/27 is derived,
local GR is derived,
PPN is passed.
```

Not supported:

```text
this route is empty.
```

It is not empty. It is a narrow route, but it is a route.

## 9. Decision

Decision:

```text
topological_projector_parent_skeleton_written_N5_action_route_conditional_FLRW_Bmem_and_N6_open_no_promotion
```

Meaning:

```text
N5 now has an action-level skeleton, conditional on P_D being a
metric-independent relative-chain projector. The next hard gate is whether the
same P_D can produce the FLRW memory projection and B_mem = 2/27 without
reintroducing a clock or sidecar rule.
```

Main gain:

```text
the local projector-stress obstruction has a precise parent-action route.
```

Main blocker:

```text
the route must unify with FLRW and close N6, or it stays a local closure
mechanism.
```

## 10. Next Target

Next:

```text
253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md
```

Purpose:

```text
try to derive the FLRW memory projection from the same P_D skeleton. If the
2/27 coefficient does not come out from topology/rank/averaging, keep B_mem as
an empirical closure theorem-target rather than pretending it is derived.
```
