# 77 - Local Route Demote-or-Continue Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 76 found a useful but incomplete Noether structure:

```text
S_gate = int sqrt(-g) C_coh[g,u,D] L_mem[g,u,Q,...]
```

Its stress bookkeeping requires:

```text
nabla_mu T_gate^munu =
E_Q L_xi Q
+ E_u L_xi u
+ E_D L_xi D
+ E_mem L_xi fields.
```

The failure was precise rather than vague:

```text
E_u and E_D are not derived.
```

Therefore the local route now has only two honest options:

1. demote the current C_coh-gated construction to a closure/diagnostic tool; or
2. allow one bounded attempt to construct a parent owner for u and D.

## 2. Short Verdict

```text
local_route_decision =
continue_one_bounded_parent_uD_owner_attempt
```

```text
current_Ccoh_gate_status =
demoted_to_closure_until_parent_uD_owner
```

This means the current local route is not promoted to derived local GR.

It also means we do not abandon the route yet, because checkpoint 76 exposed a concrete missing object: a parent owner for the observer congruence u and the averaging/domain object D.

## 3. Why Not Demote Immediately?

Immediate demotion is safe, but it would throw away the most direct route before testing the exact failure point.

Checkpoint 76 did not say:

```text
local route impossible
```

It said:

```text
local route requires parent E_u and E_D equations
```

So the disciplined next move is not endless exploration. It is one bounded parent-owner attempt with explicit kill conditions.

## 4. Why Not Continue Unbounded?

Unbounded continuation is rejected.

The route has already accumulated enough scaffolding:

- C_coh selectors;
- chi_D gates;
- relative currents;
- boundary cohomology;
- memory action contracts;
- local silence conditions.

Those pieces are useful as support structure, but they cannot keep substituting for the missing parent equations. If the next step cannot make u and D owned rather than hand-chosen, the local branch must be downgraded.

## 5. Decision Matrix

| Criterion | Best option |
|---|---|
| attacks checkpoint 76 failure directly | bounded u/D owner attempt |
| has clear failure mode | bounded u/D owner attempt |
| avoids endless scaffolding | bounded attempt or demote |
| preserves derivation ambition | bounded u/D owner attempt |
| keeps empirical interpretation clean | bounded u/D first, then amplitude or empirical tests |

The selected option is therefore:

```text
continue_one_bounded_parent_uD_owner_attempt
```

## 6. Current Demotion Labels

| Route piece | Label now | Can promote only if |
|---|---|---|
| C_coh-gated memory action | conditional closure, not field theory | parent u/D owner closes exchange |
| local bulk silence | conditional support | stationary bound domains are derived |
| FLRW background activity | background contract | memory action gives background and perturbation equations |
| relative current support | formal conservation support | parent action selects physical representative and amplitude |

This is the important guardrail: the local route is not dead, but it is not allowed to pretend it is already GR.

## 7. Bounded Attempt Contract

Checkpoint 78 must try to construct:

```text
parent owner for u and D
```

It must satisfy these gates:

| Gate | Required result | Kill condition |
|---|---|---|
| u owner | observer congruence has parent equation, constraint, or coframe origin | u is chosen only to make C_coh work |
| D owner | domain/boundary follows from a variational, constraint, or topological rule | D is just a smoothing/window choice |
| Noether exchange | E_u and E_D absorb the C_coh exchange terms | boundary or perturbation exchange remains uncontrolled |
| local/FLRW limits | same owner gives local quiet bulk and FLRW active background | one branch is saved by damaging the other |
| no new stress | owner is constrained/topological or stress-bounded | new field creates a PPN-scale source |

## 8. Hard Kill Conditions

If any of these happen, the local transition route is demoted to closure-only:

```text
u_frame_chosen_by_hand
D_or_averaging_window_chosen_by_hand
Bianchi_requires_frozen_Ccoh
new_stress_or_scale_unbounded
quiet_bulk_only_boundary_fails
```

The biggest danger is simple:

```text
C_coh works only because we hide the hard parts in u or D.
```

That is not allowed.

## 9. Gate Results

| Gate | Result |
|---|---|
| current_local_route_promoted | fail |
| demotion_label_applied | pass |
| bounded_uD_attempt_allowed | pass |
| unbounded_subbranching_allowed | fail |
| amplitude_pivot_now | defer |
| empirical_test_now | defer |
| support_claim_allowed | fail |

This keeps the theory honest without prematurely burying the route.

## 10. Run Artifact

Script:

```text
research-programme\scripts\local_route_demote_or_continue_gate.py
```

Run directory:

```text
research-programme\runs\20260531-115514-local-route-demote-or-continue-gate
```

Generated tables:

```text
source_checkpoint_register.csv
fork_options.csv
decision_matrix.csv
demotion_labels.csv
bounded_attempt_gates.csv
kill_conditions.csv
gate_results.csv
decision.csv
```

Status readout:

```text
demoted_current_route_bounded_parent_uD_attempt_allowed
```

## 11. Next Target

Create:

```text
78-parent-uD-owner-contract.md
```

Purpose:

```text
Attempt to derive or strictly contract the parent equations that own u and D.
```

Acceptance:

```text
Either E_u/E_D ownership is made non-arbitrary, or the local C_coh route is demoted to diagnostic closure.
```

Plain English:

```text
No more smuggling the local GR reduction through a hidden selector.
Either the parent action owns the selector, or the selector is just a useful closure knob.
```
