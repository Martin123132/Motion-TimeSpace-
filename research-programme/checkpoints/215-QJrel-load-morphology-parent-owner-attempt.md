# 215 - QJrel Load Morphology Parent Owner Attempt

Private theory checkpoint. This is not a public local-GR, galaxy, SPARC, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 214 produced a useful compact-vs-extended morphology candidate:

```text
E_L = s_80 (1 + A_I)/2 + F_edge.
```

It repaired the `dwarf_3kpc` failure at proxy level.

This checkpoint asks:

```text
Can Q and J_rel actually own that invariant?
```

## 2. Machine Artifact

Script:

```text
scripts/QJrel_load_morphology_parent_owner_attempt.py
```

Run:

```text
runs/20260601-000032-QJrel-load-morphology-parent-owner-attempt
```

Command:

```text
python scripts/QJrel_load_morphology_parent_owner_attempt.py --timestamp 20260601-000032
```

Status:

```text
QJrel_matter_support_owner_partial_Jrel_threshold_missing_closure_retained
```

Claim ceiling:

```text
load_morphology_parent_owner_partial_no_selector_or_galaxy_promotion
```

## 3. Owner Split

The clean split is:

| object | best owner |
|---|---|
| `s_80`, `r_99` | matter/load support measure |
| `A_I` | support inertia tensor, optionally with `Q` anisotropy sidecar |
| `F_edge` | `J_rel` or outer boundary current |

The matter-support part can be written:

```text
dmu_m = sqrt(h) |T_matter| d^3x.
```

Then:

```text
int_B(r80) dmu_m = 0.8 int_D dmu_m.
```

and:

```text
I_ab = int_D X_a X_b dmu_m.
```

That is a real partial owner if the domain and matter frame are already owned.

## 4. Why Q Alone Fails

`Q` is useful but cannot be the sole owner.

Reason:

```text
stationary compact local systems can have Q ~= 0.
```

So `Q` alone may see no coherent volume load even though the compact matter
support still exists.

That means:

```text
Q cannot by itself distinguish a compact source from empty space.
```

It can be an anisotropy/routing sidecar, but not the full support measure.

## 5. Why Jrel Is Still The Weak Link

The edge term wants:

```text
F_edge = ||J_rel_outer|| / (int_D dmu_L + epsilon).
```

This is the right kind of object because it separates:

```text
true exterior-vacuum shell
```

from:

```text
extended/transition boundary support.
```

But the representative:

```text
J_rel
```

is still not parent-derived.

So the edge term remains formal.

## 6. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| `Q` sole-owner route | fail |
| matter support owns `r80/r99/inertia` | partial pass |
| `J_rel` owns edge term | fail/open |
| hybrid `E_L` parent-derived | fail |
| selector/galaxy promotion | fail |

## 7. Decision

Decision:

```text
QJrel_matter_support_owner_partial_Jrel_threshold_missing_closure_retained
```

Meaning:

```text
the morphology invariant has a plausible owner split, but not a parent theorem.
```

The best honest branch is:

```text
matter support owns the bulk support shape,
Q supplies anisotropy/routing sidecar,
J_rel is the missing boundary owner.
```

## 8. What This Improves

This is still progress.

It means the local-vs-galaxy selector is no longer a pure hand label.

It can be written as a concrete fixed closure:

```text
compact shell = small support percentile + large vacuum collar + low edge current.
extended load = large support percentile and/or nonzero edge current.
```

But:

```text
the field theory has not derived the selector.
```

## 9. Next Target

Next target:

```text
216-load-morphology-sidecar-galaxy-test-plan.md
```

The practical next question:

```text
Can this fixed sidecar be attached to future local/galaxy tests without changing
the galaxy repo or smuggling fit knobs?
```
