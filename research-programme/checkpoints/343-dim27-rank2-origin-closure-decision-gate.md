# 343 - Dim-27/Rank-2 Origin Closure Decision Gate

Private derivation checkpoint. This is not a public cosmology, CMB, local-GR, PPN, perturbation-theory, or unified-field claim.

## Purpose

Checkpoint 342 left one final amplitude-origin target:

```text
derive dim(V_cell)=27 and rank(P_active)=2,
or demote the amplitude to closure.
```

This checkpoint does that decision gate.

Short answer:

```text
dim=27 and rank=2 have useful conditional templates,
but they are not parent-derived.
```

Therefore:

```text
B_mem = 2/27 is now frozen as an explicit closure value.
```

This does not throw away the branch. It stops overclaiming it.

## Machine Artifact

Script:

```text
scripts/dim27_rank2_origin_closure_decision_gate.py
```

Run:

```text
runs/20260601-211500-dim27-rank2-origin-closure-decision-gate
```

Status:

```text
dim27_rank2_not_parent_derived_amplitude_frozen_as_explicit_closure
```

Claim ceiling:

```text
amplitude_closure_decision_no_Bmem_parent_derivation_claim
```

## Dimension Result

The best dimension route remains:

```text
dim(V_cell)=3 x 3 x 3 = 27.
```

This has strong semantic fit for an MTS-style finite fibre.

But the verifier finds the obvious degeneracy:

```text
27,
9 x 3,
3 x 9,
3 x 3 x 3.
```

All give the same denominator.

So:

```text
the number 27 alone does not derive the three ternary parent factors.
```

The parent action would need to prove:

```text
why exactly three factors,
why exactly ternary,
why this finite fibre,
and why it is not a labelled species vector.
```

That proof is not currently present.

## Rank Result

The best rank route is:

```text
a rank-2 source/readout plane.
```

A possible geometric template is:

```text
2D transverse plane inside one ternary factor,
with the other two factors fixed to reference states.
```

That gives:

```text
rank(P_active)=2.
```

But it requires extra assumptions:

```text
the transverse plane is parent-selected,
the two reference states are parent-selected,
the readout has no marker action.
```

Also, if we instead take the full transverse factor across the other two ternary factors:

```text
rank = 2 x 3 x 3 = 18,
```

which gives:

```text
q_trace = 2/3,
```

not:

```text
2/27.
```

So the desired rank-2 construction is a readout/anchoring construction, not a bulk fibre theorem.

## Degeneracy Audit

The verifier records:

| Degeneracy | Size | Meaning |
|---|---:|---|
| coordinate rank-2 choices | 351 | two basis states can be chosen many ways |
| continuous rank-2 subspaces | 50-dimensional | `Gr(2,27)` has many rank-2 planes |
| dimension factorizations | multiple | many parent stories give 27 |
| marker extension | unbounded | EFT coefficients return if marker allowed |

This is the core reason the derivation should stop here.

The algebra:

```text
identity current + rank 2 / dimension 27
```

is sharp.

The parent ownership:

```text
why that rank,
why that dimension,
why no marker,
```

is not established.

## Closure Update

| Quantity | New status | Allowed claim | Forbidden claim |
|---|---|---|---|
| `B_mem` | explicit closure value | fixed closure branch / empirical target | parent-derived amplitude |
| `epsilon_H` | closure/fitted coupling unless parent theorem supplied | set to 1 in locked branch | unconditionally derived normalization |
| `q_trace` | conditional algebraic identity | exact if rank/dim assumed | derived from parent action |
| `H_star/H0` | closure/theorem target | fixed to 1 in lead branch | parent-derived calibration |

This is the right discipline lock.

## Gate Results

| Gate | Result |
|---|---|
| source paths exist | pass |
| `dim=27` template exists | pass |
| `dim=27` parent-derived | fail |
| `rank=2` template exists | pass |
| `rank=2` parent-derived | fail |
| full screen factor rejected for `2/27` | pass |
| coordinate rank-2 degeneracy identified | pass |
| continuous rank-2 degeneracy identified | pass |
| marker extension forbidden | fail |
| effective stability parent-derived | fail |
| `epsilon_H` parent-derived unconditionally | fail |
| `B_mem` parent promotion allowed | fail |
| amplitude demoted to explicit closure | pass |
| empirical branch retained | pass |

## What This Means

This is not a collapse of the MTS programme.

It means the amplitude claim is now properly labelled:

```text
B_mem = 2/27
```

is:

```text
a locked empirical closure branch,
an algebraically sharp theorem target,
and a serious test object.
```

It is not:

```text
a parent-derived result.
```

That is exactly the kind of discipline a serious theory needs.

## Standing

The fair status is now:

```text
amplitude route frozen as closure until a genuinely new parent theorem appears.
```

The empirical status remains:

```text
2/27 is still the lead branch to test.
```

The theory-building status becomes:

```text
move on from amplitude derivation and pressure-test other gates.
```

## Next Target

Next:

```text
move_from_amplitude_derivation_to_empirical_and_other_theory_gates.
```

Recommended next work:

```text
1. update the local claim ledger so B_mem=2/27 is explicitly closure, not derived;
2. run or prepare the next empirical robustness branch using the locked closure;
3. return to independent theory gates: H_star=H0, local GR/PPN, growth/CMB bridge, or conservation/Bianchi accounting.
```

The clean move is to stop spending turns trying to squeeze a derivation out of the amplitude and start using the closure branch as a disciplined test pillar.
