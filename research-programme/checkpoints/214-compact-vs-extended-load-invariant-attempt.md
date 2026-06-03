# 214 - Compact vs Extended Load Invariant Attempt

Private theory checkpoint. This is not a public local-GR, galaxy, SPARC, BAO,
CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 213 showed that:

```text
x = R_D / L_cg
```

is useful but insufficient.

It can tell us whether a domain is smooth enough, but not whether the domain is:

```text
compact-source / exterior-vacuum shell
```

or:

```text
extended galaxy/load support.
```

The stress case was:

```text
dwarf_3kpc.
```

It has low `x`, so an `x`-only selector can misread it as local, even though it
is an extended load domain.

## 2. Machine Artifact

Script:

```text
scripts/compact_vs_extended_load_invariant_attempt.py
```

Run:

```text
runs/20260601-000031-compact-vs-extended-load-invariant-attempt
```

Command:

```text
python scripts/compact_vs_extended_load_invariant_attempt.py --timestamp 20260601-000031
```

Status:

```text
compact_extended_load_invariant_candidate_margin_separates_proxies_parent_QJ_missing
```

Claim ceiling:

```text
load_morphology_candidate_no_parent_selector_or_galaxy_promotion
```

## 3. Candidate Invariant

Define a load-support score:

```text
E_L = s_80 (1 + A_I)/2 + F_edge.
```

where:

| term | meaning |
|---|---|
| `s_80 = r_80/R_D` | radius enclosing 80% of matter/load support divided by domain radius |
| `A_I = 1 - 3 lambda_min/Tr(I)` | inertia/load anisotropy |
| `F_edge` | outer-collar load fraction or relative boundary-current term |

This is the right kind of object because it asks:

```text
where does the load live inside the domain?
```

not just:

```text
how small is the domain compared with L_cg?
```

## 4. Proxy Separation

Representative compact local shells:

```text
solar_1AU_shell,
solar_Mercury_shell,
earth_GPS_shell.
```

Representative extended loads:

```text
dwarf_3kpc_extended_load,
milky_way_8kpc_disk,
outer_spiral_30kpc_disk,
massive_ETG_5kpc,
cluster_1Mpc_extended_bound.
```

The candidate score gives:

```text
compact_max_E_L = 0.1236
extended_min_E_L = 0.48875
margin_width = 0.36515
extended_min / compact_max = 3.9542880258899673.
```

That is a clean representative margin.

Most importantly:

```text
dwarf_3kpc
```

is repaired:

```text
candidate class = extended_load.
```

So the exact failure from checkpoint 213 is addressed at proxy level.

## 5. What This Does Not Prove

This is not yet a theorem.

The candidate uses:

```text
r_80,
r_99,
A_I,
F_edge.
```

The parent theory still has to define these from:

```text
Q,
J_rel,
T_matter,
or an MTS load current.
```

Without that, the invariant is a disciplined closure object.

It is not a derived domain selector.

## 6. Parent Contract

A future parent action must supply:

| clause | requirement |
|---|---|
| `L1` | invariant load measure `dmu_L` |
| `L2` | covariant support/inertia tensor |
| `L3` | boundary-current or outer-collar load term |
| `L4` | topological phase gap or threshold-free compact/extended class |
| `L5` | metric variation and Bianchi/stress accounting |

Until those exist:

```text
no local-GR or galaxy promotion is allowed.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| candidate invariant written | pass |
| dwarf `x`-gate failure repaired | pass |
| representative stress cases classified | conditional pass |
| ambiguous cases exposed | pass |
| `Q/J_rel` parent owner derived | fail |
| galaxy/local selector promoted | fail |

## 8. Decision

Decision:

```text
compact_extended_load_invariant_candidate_margin_separates_proxies_parent_QJ_missing
```

Meaning:

```text
we now have a concrete compact-vs-extended load morphology candidate that fixes
the dwarf-domain failure in proxy tests.
```

But:

```text
the parent owner of the load measure and boundary current is still missing.
```

## 9. Next Target

Next target:

```text
215-QJrel-load-morphology-parent-owner-attempt.md
```

The exact next question:

```text
Can Q and J_rel define dmu_L, A_I, and F_edge from the parent structure, or must
E_L remain a fixed morphology closure?
```
