# 270 - `Cperp` Residual-Shift Constraint Attempt

Private derivation checkpoint. This is not a public local-GR, CMB, BAO, or unified-field claim.

## Purpose

Checkpoint 269 left the exact next burden:

```text
derive Cperp -> Cperp + eta_perp
```

as a parent first-class constraint, quotient redundancy, or relative-exact cohomology representative.

This checkpoint asks:

```text
Can Cperp really be gauge,
or is projected matter metric only closure?
```

## Machine Artifact

Script:

```text
scripts/Cperp_residual_shift_constraint_attempt.py
```

Run:

```text
runs/20260601-000088-Cperp-residual-shift-constraint-attempt
```

Status:

```text
Cperp_residual_shift_first_class_route_conditionally_consistent_parent_no_Cperp_action_missing
```

Claim ceiling:

```text
Cperp_constraint_internal_only_no_local_GR_or_unification_promotion
```

## Main Result

The first-class route is algebraically consistent:

```text
G[eta] = integral pi_perp eta_perp
```

with:

```text
P_D eta_perp = 0
```

generates:

```text
delta Cperp = eta_perp.
```

The self-algebra is Abelian:

```text
{G[eta], G[xi]} = 0.
```

So the shift symmetry is mathematically available.

But the real test is Hamiltonian preservation:

```text
{G[eta], H} = - integral eta_perp delta H / delta Cperp.
```

For the constraint to be first-class, we need:

```text
delta H / delta Cperp approx 0.
```

That means the parent action must contain no physical `Cperp` dependence.

## Necessary Conditions

For `Cperp` to be genuine gauge, the parent action must satisfy:

| Condition | Required form | Status |
|---|---|---|
| no `Cperp` matter metric | `S_matter[psi, exp(P_D C)g]` | conditional previous |
| no `Cperp` kinetic term | no `dot(Cperp)^2` | not parent-derived |
| no `Cperp` gradient stiffness | no physical `(nabla Cperp)^2` | not parent-derived |
| no `Cperp` potential | `V` depends on `C_D` / class variables only | not parent-derived |
| relative-exact boundary | compact local `Cperp` is exact/trivial | conditional support |
| action-owned projector | `P_D` from varied domain variables | conditional previous |
| predeclared domain scale | `L_D` / `L_cg` before scoring | open |

This is the key conclusion:

```text
Cperp can be gauge only if it is absent from physical dynamics.
```

If the parent action gives `Cperp` a kinetic term, gradient energy, potential, or matter coupling, then:

```text
Cperp is a real local field again.
```

## Degrees of Freedom

| Branch | Local DOF | Verdict |
|---|---:|---|
| first-class `Cperp` | `0` | conditional pass if all conditions hold |
| second-class / heavy `Cperp` | `0 or 1 effective` | not lead; needs extreme suppression |
| ordinary scalar `Cperp` | `1` | rejected as lead |
| projected-metric closure | not parent-counted | allowed only if labelled |

The good branch is:

```text
pi_perp approx 0
```

as a first-class constraint.

The bad branch is:

```text
Cperp has ordinary dynamics.
```

## Cohomology Support

Checkpoint 231 gives useful supporting topology:

```text
local compact shell relative memory class can be exact
after ordinary mass flux and shear are projected away.
```

That supports the idea:

```text
compact local Cperp is an exact representative,
not a matter observable.
```

But it is not enough.

We still need:

```text
matter observables live on the quotient class P_D C.
```

That is not parent-derived yet.

## What Failed

The checkpoint did **not** derive:

```text
delta H / delta Cperp approx 0.
```

Equivalently, it did not derive the parent no-`Cperp` action principle.

So the result is:

```text
first-class route is conditionally consistent,
but not parent-derived.
```

## Decision

Decision:

```text
Cperp_residual_shift_first_class_route_conditionally_consistent_parent_no_Cperp_action_missing
```

Meaning:

```text
Cperp residual shift can be a first-class redundancy only if pi_perp approx 0
is preserved by a parent Hamiltonian with no physical Cperp dependence.
```

The algebraic route is consistent and supported by relative-exact local cohomology.

But:

```text
the parent no-Cperp action principle is not derived.
```

Therefore:

```text
the projected metric selector remains a theorem target,
not a promotion.
```

## Current Theory Status

This is useful narrowing.

We are no longer vaguely saying:

```text
Cperp is screened.
```

We now know the exact demand:

```text
Cperp must be pure gauge / exact representative,
with no physical Hamiltonian dependence.
```

That is cleaner, harsher, and more field-theoretic.

## Next Target

Next step:

```text
construct_parent_no_Cperp_action_or_demote_projected_metric_selector_to_closure
```

Pass route:

```text
parent action depends on C_D and relative classes only,
with Cperp appearing only as gauge representative / constraint variable.
```

Fail route:

```text
projected matter metric is an imposed effective closure.
```

## Claim Gates

| Gate | Result |
|---|---|
| candidate shift generator | conditional pass |
| self algebra | pass |
| Hamiltonian invariance | not derived |
| relative-exact support | partial |
| ordinary scalar `Cperp` | rejected as lead |
| metric selector promotion | blocked |
| local-GR/unification promotion | forbidden |

## Validation

- Script compiles in `.venv-score`.
- Run completed and wrote `DONE.txt`.
- CSV outputs parse cleanly.
- Cited source paths exist.
- No changes were made to `formalization-workbench`.
- Claim ceiling remains internal only; no local-GR or unification promotion is allowed.
