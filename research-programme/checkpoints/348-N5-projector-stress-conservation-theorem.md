# 348 - N5 Projector-Stress Conservation Theorem

Private derivation checkpoint. This is not a public local-GR, PPN, CMB, cosmology, or `B_mem=2/27` derivation claim.

## Purpose

Checkpoint 347 reduced the local-GR problem to the sharp blocker:

```text
N5_projector_stress_Bianchi_safe.
```

This checkpoint attacks N5 directly.

The question is:

```text
Can projector stress be killed or retained honestly enough for the local GR route?
```

Short answer:

```text
yes, conditionally: a metric-independent topological/relative-chain projector has no bulk projector stress.
```

But:

```text
parent ownership and FLRW compatibility remain open,
so this is not a full local-GR or amplitude derivation.
```

## Machine Artifact

Script:

```text
scripts/N5_projector_stress_conservation_theorem.py
```

Run:

```text
runs/20260601-221500-N5-projector-stress-conservation-theorem
```

Key outputs:

```text
results/source_register.csv
results/N5_theorem_pieces.csv
results/projector_stress_fork_table.csv
results/unresolved_bridge_ledger.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
N5_conditionally_closed_by_metric_independent_topological_projector_parent_ownership_and_FLRW_stress_bridge_open
```

Claim ceiling:

```text
conditional_N5_theorem_only_no_local_GR_PPN_or_Bmem_derivation
```

Source paths missing:

```text
0
```

## The Theorem

Let the local projector sector be owned by:

```text
P_D
```

where `P_D` is not a Hodge projector, not a least-energy projector, and not an orthogonal projector defined by a metric inner product.

Instead, require:

```text
P_D = relative-chain / cohomology projector,
metric independent in the local exterior.
```

Then the local projector action must be built only from metric-free objects:

```text
wedge products,
chain pairings,
boundary incidence maps,
relative cohomology classes,
topological constraints.
```

Forbidden in the local bulk projector sector:

```text
Hodge star,
inverse metric,
sqrt(-g) bulk potential,
DeWitt/Hodge boundary metric,
least-energy minimization,
metric-dependent orthogonality.
```

Then:

```text
delta_g S_projector|bulk = 0.
```

So:

```text
T_projector_munu|bulk
= -2/sqrt(-g) delta S_projector / delta g^munu
= 0.
```

This conditionally closes N5 in the local exterior.

## Why This Is Not Cheating

This does not drop projector stress.

It gives an exact condition under which bulk projector stress is absent:

```text
there is no metric dependence to vary in the local bulk projector sector.
```

That is different from:

```text
the stress is inconvenient, so ignore it.
```

The forbidden branch remains forbidden:

```text
metric-dependent projector + dropped stress = fake conservation.
```

## Fork Table

| Fork | Bulk `T_projector` | Bianchi status | Local-GR effect |
|---|---|---|---|
| metric-independent topological projector | zero | safe | N5 conditionally cleared |
| boundary-only projector stress | zero in bulk | safe if boundary variation owned | bulk EH can continue |
| retained bulk projector stress | nonzero | safe if retained | modified exterior, not GR without residual bounds |
| dropped projector stress | ignored | fake conservation | forbidden |
| Hodge/orthogonal projector | generically nonzero | must be retained | metric-only EH fails unless extra cancellation theorem supplied |

This is a useful sharpening.

Before:

```text
N5 was an open hard blocker.
```

Now:

```text
N5 has a conditional theorem route and a clear no-go route.
```

## The No-Free-Lunch Split

There is a catch, and it matters.

The same property that protects local GR:

```text
metric-independent / topological / no bulk metric variation
```

also means:

```text
the local projector sector cannot by itself generate FLRW stress energy.
```

So N5 local silence does not derive:

```text
B_mem = 2/27,
kappa_mem,
epsilon_H = 1,
or the FLRW memory stress amplitude.
```

To affect `H^2`, the cosmological memory sector still needs:

```text
a metric stress-response / exchange-normalization theorem.
```

Therefore the structure must split:

```text
topological projector sector
    -> local silence / no bulk projector stress

metric stress-response sector
    -> FLRW memory density and pressure
```

The future parent action has to show these are two limits of one framework, not two unrelated patches.

## Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited N5/local-GR sources exist |
| topological no-bulk-stress theorem written | pass | metric-independent wedge/chain projector has `delta_g S_projector|bulk=0` |
| Hodge projector no-go preserved | pass | metric-dependent projectors must retain stress |
| dropped stress forbidden | pass | fake conservation route remains rejected |
| N5 parent-owned | fail | parent action skeleton exists but `P_D` selection is not derived |
| FLRW same operator proved | fail | local `P_D` not proven to reduce to cosmological memory projector |
| `B_mem` or `kappa_mem` derived | fail | topological local silence does not fix stress amplitude |
| local GR or PPN promoted | fail | N5 is conditional; other local gates remain open |
| claim ceiling enforced | pass | no local-GR/PPN/amplitude promotion |

## Decision

Decision:

```text
N5_conditionally_closed_by_metric_independent_topological_projector_parent_ownership_and_FLRW_stress_bridge_open
```

Meaning:

```text
N5 is no longer just "please make projector stress vanish."
It has an exact conditional theorem:
metric-independent topological projector => no bulk projector stress.
```

But:

```text
the parent action must still derive that projector,
prove it is the same object used in FLRW/cosmology,
and add a separate stress-response sector for cosmological memory.
```

## What This Does For GR

This improves the local-GR route.

If the parent action owns `P_D` as a metric-independent topological projector, then:

```text
N5 can be marked conditionally safe.
```

Then the remaining local-GR route becomes:

```text
N0: unique physical metric/coframe,
N2: no trace-free/shear boundary stress,
N3: no scalar/vector local hair,
N4: exact relative memory,
N5: topological projector no bulk stress,
N6: metric-only EH exterior.
```

That is not solved, but it is a more serious finite target.

## Next Target

Next:

```text
349 - Parent P_D / FLRW Projection Compatibility Gate
```

Pass condition:

```text
derive P_D from the parent action as a relative-chain/cohomology projector,
and show that:

local exterior limit -> topological no-bulk projector stress,
FLRW limit -> the memory projection used in the cosmology branch.
```

Fail condition:

```text
use one projector for local GR silence
and a different unrelated projector for cosmology.
```

That would be a patch, not a unified field-theory spine.

## Bottom Line

This is a useful round.

We did not get:

```text
MTS derives local GR.
```

We did get:

```text
N5 can be conditionally closed without cheating,
if the projector is topological/metric-independent.
```

The next derivation fight is now:

```text
prove the parent action owns that projector,
and prove the same projector also gives the FLRW memory branch.
```

That is exactly the kind of work that moves MTS from closure model toward field theory.
