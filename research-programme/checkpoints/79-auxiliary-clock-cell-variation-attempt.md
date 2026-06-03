# 79 - Auxiliary Clock/Cell Variation Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 78 selected the least-bad route for owning the missing variables:

```text
selected_route =
auxiliary_clock_cell_reference
```

The proposed ownership map was:

```text
u_mu = -nabla_mu T / sqrt(-X_T)
```

and:

```text
J_D^mu = star(dX^1 wedge dX^2 wedge dX^3),
nabla_mu J_D^mu = 0.
```

This checkpoint asks the sharp question:

```text
Does this route genuinely own u and D without adding forbidden local stress?
```

## 2. Short Verdict

```text
auxiliary_clock_cell_status =
conditional_route_survives_only_as_pure_constraint_or_topological_reference
```

```text
local_GR_status =
not_derived
```

Plain English:

```text
The clock/cell route can formally own the missing u and D terms,
but it survives only if the reference sector is pure constraint/topological/on-shell stressless.
```

If the reference fields behave like dust, aether, khronon, or a phase-field boundary layer, the local route fails.

## 3. Variation Blocks

| Block | What variation gives | Stress verdict |
|---|---|---|
| clock gradient definition | `E_T` can replace loose `E_u` terms | safe only without standalone clock kinetic energy |
| unit vector multiplier | enforces `u_mu u^mu = -1` | dangerous if multiplier stress remains |
| cell label current | `E_XI` can replace loose `E_D` terms | safe only if topological/constraint-like |
| domain indicator | advection/no-flux constraint | unsafe if it becomes a phase field with gradient energy |
| `C_coh L_mem` gate | `delta C_coh` enters `E_T`, `E_XI`, `E_Q`, boundary terms | still open |

So the variation does not collapse immediately, but it does not promote the route either.

## 4. Noether Repair Attempt

Checkpoint 76 had:

```text
E_u L_xi u
E_D L_xi D
```

The auxiliary route attempts:

```text
E_u L_xi u -> E_T L_xi T + projection/unit-constraint terms
```

and:

```text
E_D L_xi D -> E_XI L_xi X^I
```

or:

```text
E_D L_xi D -> E_J L_xi J_D.
```

At identity level this is promising:

```text
u and D are no longer arbitrary knobs.
```

But identity-level ownership is not enough.

The stress tensor of the reference sector is the real gate.

## 5. Stress Channels

| Channel | Result |
|---|---|
| physical dust energy | forbidden |
| aether/khronon kinetic terms | forbidden unless separately bounded, so not usable as the clean local-GR route |
| residual constraint multiplier stress | must vanish or cancel on shell |
| phase-field boundary energy | forbidden |
| pure constraint/topological reference | only viable channel |

This is a narrow tunnel.

The route is not:

```text
add a new field and hope it is small.
```

It must be:

```text
add reference structure that owns the bookkeeping but does not gravitate as new local matter.
```

## 6. Limit Gates

| Gate | Status | Reason |
|---|---|---|
| local bound quiet bulk | conditional open | needs proof stationary bound cells follow from the owner |
| FLRW active background | conditional open | same owner must make `C_coh -> 1` cosmologically |
| PPN reference stress | narrow contract pass only | survives only if stress is on-shell zero or pure gauge |
| boundary transition | fail open | surface current cancellation is not derived |
| full local-GR promotion | fail | route is not yet a theorem |

The survival of this branch is now highly constrained.

That is good theory hygiene: if it lives, it lives through a small door.

## 7. What Was Actually Gained

Before checkpoint 79, the local route had an ugly loophole:

```text
choose u and D so C_coh behaves.
```

After checkpoint 79, that loophole is closed.

The only acceptable route is:

```text
T and X^I/J_D are parent-owned reference variables,
their equations absorb the C_coh exchange,
and their stress is zero, pure gauge, topological, or strictly bounded.
```

That is a real mathematical target.

## 8. What Is Still Missing

The branch still lacks:

1. a written stress-free reference action;
2. proof that multiplier stress vanishes or cancels;
3. explicit boundary current cancellation;
4. explicit local-cell stationary theorem;
5. explicit FLRW-active theorem from the same owner.

So:

```text
derived_local_GR =
false
```

but:

```text
local_route_not_dead =
true, only under stress-free reference contract
```

## 9. Kill Rule After This Checkpoint

If the next action cannot write a reference action whose stress is on-shell zero/pure gauge/topological, then:

```text
C_coh local route -> diagnostic closure only
```

and we should move to either:

```text
amplitude normalization
```

or:

```text
empirical closure testing
```

No more expanding the local branch with new physical fields.

## 10. Run Artifact

Script:

```text
research-programme\scripts\auxiliary_clock_cell_variation_attempt.py
```

Run directory:

```text
research-programme\runs\20260531-120154-auxiliary-clock-cell-variation-attempt
```

Generated tables:

```text
source_checkpoint_register.csv
variation_blocks.csv
stress_channels.csv
noether_closure_attempt.csv
limit_gates.csv
decision.csv
```

Status readout:

```text
conditional_route_survives_only_as_stress_free_reference
```

## 11. Next Target

Create:

```text
80-stress-free-reference-action-gate.md
```

Purpose:

```text
Try to write the exact stress-free reference action or prove that this cannot be done without leaving residual local stress.
```

Expected fork:

```text
If stress-free/topological reference ownership works, continue to boundary-current closure.
If it fails, demote the local C_coh route and stop trying to derive local GR through this branch.
```
