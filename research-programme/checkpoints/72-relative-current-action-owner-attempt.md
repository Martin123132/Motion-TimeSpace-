# Relative Current Action Owner Attempt

## 1. Purpose

This file follows:

```text
71-relative-boundary-current-construction-attempt.md
```

Checkpoint 71 constructed the formal object:

```text
J_rel = (j_3,b_2)
```

with:

```text
d_rel J_rel = 0.
```

This checkpoint asks:

```text
Can a parent/topological action derive that current, instead of merely naming
it?
```

Short answer:

```text
closure can be imposed, but physical representative selection is not derived.
```

That means the pure relative-current route is support structure, not the full
local-GR derivation.

## 2. Machine Run

Implemented:

```text
scripts/relative_current_action_owner_attempt.py
```

Successful run:

```text
runs/20260531-113740-relative-current-action-owner-attempt/status.json
```

Readout:

```text
closure_imposable_selection_not_derived
```

Generated:

```text
runs/20260531-113740-relative-current-action-owner-attempt/results/source_checkpoint_register.csv
runs/20260531-113740-relative-current-action-owner-attempt/results/action_candidate_ledger.csv
runs/20260531-113740-relative-current-action-owner-attempt/results/variation_attempt_chain.csv
runs/20260531-113740-relative-current-action-owner-attempt/results/selection_tests.csv
runs/20260531-113740-relative-current-action-owner-attempt/results/gate_results.csv
runs/20260531-113740-relative-current-action-owner-attempt/results/decision.csv
```

## 3. What Works

A closure owner can be written:

```text
S_closure = <Lambda_rel, d_rel J_rel>.
```

Varying the multiplier gives:

```text
d_rel J_rel = 0.
```

So the relative current can be made closed by a parent variational term.

That helps conservation bookkeeping.

But the reverse variation gives only:

```text
d_rel^dagger Lambda_rel = 0
```

or the corresponding formal adjoint condition.

It does not say:

```text
choose the physical representative that is zero in local bound domains and
nonzero in FLRW.
```

So closure is not enough.

## 4. Best Live Route

The best live route is:

```text
BF_plus_boundary_polarization
```

Schematic:

```text
S =
integral B wedge F[A]
+ integral_boundaryD Pi(C_coh) wedge b_2.
```

Why it is attractive:

```text
BF flatness keeps local propagating hair down;
Pi(C_coh) can bias the boundary class by coherent expansion.
```

Local branch:

```text
C_coh = 0 -> Pi(0)=0 -> no boundary polarization.
```

FLRW branch:

```text
C_coh = 1 -> Pi(1) nonzero -> expansion class allowed.
```

But this is still not a derivation unless:

```text
Pi(C_coh)
```

is parent-derived.

Otherwise `Pi` is just a new selector function.

## 5. What Fails

The action does not select:

```text
p = 3
u_3 = 1/4
b_mem
```

It also does not complete:

```text
Bianchi conservation
```

because:

```text
Pi(C_coh)
```

reopens:

```text
delta C_coh
```

terms.

So the topology route helps with formal closure, but it does not magically
solve the amplitude/representative problem.

## 6. Gate Result

Gate result:

```text
action_owner_attempted              pass
drel_closure_obtained              pass formal
physical_representative_selected    fail
local_zero_possible                 pass conditional
FLRW_nonzero_possible               pass contract
PPN_wall_stress_avoided             pass conditional
Bianchi_completed                   fail
p3_u3_bmem_selected                 fail
local_GR_promoted                   fail
support_claim_allowed               fail
```

That is blunt:

```text
closure yes;
selection no.
```

## 7. Decision

Decision:

```text
relative_current_action_owner_status =
closure_imposable_selection_not_derived
```

Meaning:

```text
an action can impose d_rel J_rel = 0;
it does not derive the physical local-zero/FLRW-nonzero representative;
it does not derive p=3, u_3=1/4, or b_mem.
```

Decision:

```text
local_GR_route_status =
formal_conservation_support_not_derivation
```

The relative current is useful, but should now be demoted to:

```text
closure/conservation support
```

not treated as the thing that completes the local-GR reduction.

## 8. Next Target

Create:

```text
73-local-route-blocker-ledger-and-promotion-gate.md
```

Purpose:

```text
stop digging sub-branches for a moment and compile the exact blocker ledger:
what is solved, what is formal support, and what still blocks promotion.
```

Pass condition:

```text
the local route has a clear promotion checklist and no hidden “almost solved”
claims.
```

Fail condition:

```text
we keep generating elegant closure machinery without facing the remaining
selection/amplitude/Bianchi blockers.
```
