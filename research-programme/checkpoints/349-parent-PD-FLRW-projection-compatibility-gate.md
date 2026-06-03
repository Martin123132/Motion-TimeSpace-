# 349 - Parent P_D / FLRW Projection Compatibility Gate

Private derivation checkpoint. This is not a public local-GR, PPN, CMB, cosmology, or `B_mem = 2/27` derivation claim.

## 1. Purpose

This checkpoint keeps the project aimed at the two hard targets:

1. connect MTS to GR in the local weak-field/exterior limit,
2. make as much as possible derived from a parent structure rather than closure-fitted later.

The immediate gate is whether the same parent projector `P_D` can do both jobs:

```text
local compact exterior -> topological/no-bulk-stress projector -> possible GR silence
FLRW cosmology         -> coherent memory projector             -> cubic memory shape
```

If those are two unrelated operators, the programme becomes a patchwork.
If they are two limits/representations of one parent object, the GR route and cosmology route remain structurally unified.

## 2. Run Ledger

Script:

```text
scripts/parent_PD_FLRW_projection_compatibility_gate.py
```

Run directory:

```text
runs/20260601-223000-parent-PD-FLRW-projection-compatibility-gate
```

Command:

```text
python scripts/parent_PD_FLRW_projection_compatibility_gate.py --timestamp 20260601-223000
```

Status:

```text
parent_PD_same_operator_bridge_conditionally_coherent_FLRW_shape_only_Bmem_and_local_GR_stay_unpromoted
```

Claim ceiling:

```text
same_projector_shape_bridge_only_no_parent_PD_Bmem_or_local_GR_promotion
```

Outputs:

```text
results/source_register.csv
results/PD_limit_compatibility.csv
results/same_operator_bridge.csv
results/amplitude_debt_register.csv
results/local_GR_dependency_register.csv
results/gate_results.csv
results/decision.csv
```

## 3. Starting Point From 348

Checkpoint 348 gave N5 a conditional local theorem:

```text
P_D metric-independent/topological
    => delta_g S_projector|bulk = 0
    => T_projector_munu|bulk = 0
```

That matters because the local GR route needs the non-Einstein/projector sector to stop sourcing the compact exterior.

But 348 also exposed the no-free-lunch problem:

```text
stress-free topological projector locally
    cannot by itself generate
FLRW memory density, pressure, or B_mem = 2/27.
```

So the next question is not "can we make the local projector vanish?".
It is:

```text
Can one parent P_D have a local stress-free representation and a cosmological coherent-memory representation?
```

## 4. Exact Compatibility Contract

The parent action must not merely contain two named projectors.
It must define one object before either limit is taken:

```text
P_D : relative chain/cohomology data of domain D -> active/coherent projected sector
```

Then the two relevant reductions are:

```text
P_D | local compact exterior = P_top
P_D | FLRW homogeneous sector = P_iso
```

where:

```text
P_top = metric-independent topological/relative-chain projector
P_iso = coherent homogeneous/isotropic memory projector
```

The local branch requires:

```text
delta_g P_top = 0
delta_g S_top|bulk = 0
T_top_munu|bulk = 0
```

The FLRW branch requires:

```text
Q^i_j = X_FLRW delta^i_j
I_M|FLRW = det(Q^i_j) = X_FLRW^3
```

This gives a same-object shape bridge.
It does not yet give the amplitude bridge.

## 5. Derivation Attempt

Assume the parent object is defined on the domain's relative topological data before metric specialization.
Then local and FLRW are not separate laws; they are different symmetry reductions.

### 5.1 Local Exterior Reduction

In a compact exterior domain with fixed relative-chain class:

```text
P_D -> P_top
```

If `P_top` is built from chain maps, incidence maps, boundary maps, and wedge/relative pairings, with no Hodge star, inverse metric, least-energy metric norm, or `sqrt(-g)` bulk potential, then:

```text
delta_g P_top = 0
delta_g S_top|bulk = 0
T_top_munu|bulk = 0
```

That is the local N5 result.
It is the piece needed for GR silence.

### 5.2 FLRW Reduction

In the homogeneous/isotropic quotient:

```text
P_D -> P_iso
```

Any owned spatial coherent-load tensor compatible with FLRW symmetry must take the form:

```text
Q^i_j = X_FLRW delta^i_j
```

If the parent invariant is determinant exposure, then:

```text
I_M|FLRW = det(Q^i_j) = X_FLRW^3.
```

So the same parent projector can conditionally explain why the cosmological memory shape is cubic.

### 5.3 What Does Not Follow

The following do not follow from the topological projector alone:

```text
B_mem = 2/27
dim(V_cell) = 27
rank(P_active) = 2
kappa_mem = 1
```

At most, the topological projector suggests a rank-fraction target:

```text
B_mem = kappa_mem Tr(P_active) / dim(V_cell).
```

To derive `2/27`, the parent theory still has to prove:

```text
dim(V_cell) = 27
Tr(P_active) = 2
kappa_mem = 1
```

Those remain amplitude debts, not wins.

## 6. GR-Recovery Meaning

The local GR reduction needs the local field equation to collapse to the Einstein exterior:

```text
E_munu =
G_munu - 8 pi G T_matter_munu - T_MTS_munu = 0
```

The GR branch is viable only if:

```text
T_MTS_munu|local bulk = 0
boundary shear/no-hair terms vanish or are bounded below PPN limits
nabla^mu T_matter_munu = 0
the remaining local bulk action is metric-only Einstein-Hilbert
```

Then:

```text
G_munu = 8 pi G T_matter_munu
```

and the usual GR-to-Newton/PPN machinery can apply.

Checkpoint 349 improves the first item conditionally:

```text
metric-independent P_D => local topological no-bulk-stress
```

It does not yet prove the full GR limit.
The full promotion still needs the parent action to own `P_D`, prove the boundary no-hair condition, and compute the PPN residual vector.

## 7. No-Free-Lunch Split

The honest structure is:

```text
parent P_D
  -> topological selection sector
       -> local no-bulk-stress / GR-silence candidate

  -> metric stress-response sector
       -> FLRW density, pressure, memory amplitude
```

This is acceptable only if both sectors live in one conserved parent stress ledger.

It is not acceptable to say:

```text
topological term has no stress locally
```

and then also say:

```text
the same stress-free term produces the cosmological H^2 amplitude
```

without an additional metric response/normalization theorem.

That would be cheating.

## 8. Gate Results

| Gate | Result | Meaning |
|---|---:|---|
| source paths exist | pass | cited post-checkpoint sources are present |
| local topological no-bulk-stress | conditional pass | 348 supplies N5 under metric-independent `P_D` |
| FLRW shape from same projector | conditional pass | same abstract `P_D` can reduce to a coherent scalar-load shape |
| same operator not sidecar | conditional pass | define `P_D` before local/FLRW reduction |
| parent owns `P_D` | fail | still a skeleton/contract object |
| `B_mem = 2/27` parent-derived | fail | `dim=27`, `rank=2`, and `kappa_mem=1` remain closure debts |
| local GR or PPN promoted | fail | conditional projector silence is not a full GR theorem |
| claim ceiling enforced | pass | no public/theory-complete claim made |

## 9. What Actually Improved

Before this gate, there was a risk that the local branch and FLRW branch were using two unrelated tricks.

After this gate, the cleanest viable contract is:

```text
one pre-metric relative-chain P_D
  local representation -> topological/no-bulk-stress
  FLRW representation  -> coherent scalar memory shape
```

That is real structural progress.
It is not yet the final derivation.

The current honest status is:

```text
same-projector compatibility: conditionally coherent
local GR recovery: conditional, not promoted
FLRW cubic shape: conditional, not amplitude-derived
B_mem = 2/27: closure/theorem-target only
```

## 10. Next Target

Next checkpoint:

```text
350-parent-PD-ownership-and-cell-state-derivation-gate.md
```

Attack the exact missing derivations:

```text
derive P_D from parent variation,
derive the finite cell state space,
derive or reject dim(V_cell)=27,
derive or reject rank(P_active)=2,
derive or reject kappa_mem=1.
```

If that works, the theory becomes more than a neat compatibility bridge.
If it fails, `P_D` remains conditional and `B_mem` stays closure-locked while the local GR branch continues through PPN/no-hair gates.

## 11. Decision

```text
parent_PD_same_operator_bridge_conditionally_coherent_FLRW_shape_only_Bmem_and_local_GR_stay_unpromoted
```

The same-parent-projector route is still alive.
It is the right direction because it connects the two things that matter most:

```text
recover GR locally,
derive rather than patch.
```

But the promotion line has not been crossed.
