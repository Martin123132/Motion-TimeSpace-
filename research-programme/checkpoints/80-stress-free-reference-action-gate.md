# 80 - Stress-Free Reference Action Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 79 left one narrow survival path for the local `C_coh` route:

```text
auxiliary_clock_cell_status =
conditional_route_survives_only_as_pure_constraint_or_topological_reference
```

and set the kill rule:

```text
If the next action cannot write a reference action whose stress is on-shell zero/pure gauge/topological,
then C_coh local route -> diagnostic closure only.
```

This checkpoint tests that rule.

## 2. Short Verdict

```text
stress_free_reference_action_status =
failed_as_parent_action
```

```text
local_Ccoh_route_status =
demoted_to_diagnostic_closure
```

```text
local_GR_status =
not_derived
```

Plain English:

```text
Stress-free topological/gauge reference structures can support diagnostics,
but they do not own both u and D as physical parent equations.
```

So the `C_coh` local-transition route is no longer promoted as the route to derived local GR.

## 3. Candidate Actions Tested

| Candidate | Owns `u`? | Owns `D`? | Stress result | Verdict |
|---|---:|---:|---|---|
| physical reference dust | yes | yes | nonzero dust stress | reject |
| khronon/aether clock | yes | no | preferred-frame propagating stress | reject for clean local GR |
| multiplier unit/advection constraints | partial | partial | multiplier stress generically nonzero | reject unless multipliers vanish |
| metric-independent topological cell current | no/indirect | yes | stress-free if metric-independent | support only |
| gauge-fixed labels only | gauge only | gauge only | stress-free | closure only |

The key obstruction is that owning `u` physically requires metric-normalized time direction:

```text
u_mu = -nabla_mu T / sqrt(-X_T).
```

Once this appears nontrivially inside an action, metric variation enters the stress tensor.

## 4. Obstructions

The attempted stress-free parent action fails for five linked reasons:

1. metric dependence is required to define a unit `u`;
2. multiplier constraints can act as sources;
3. `C_coh` inside the action reintroduces metric variation;
4. topological cell currents can own `D` but not `u`;
5. pure gauge labels are stress-free but not physical selectors.

The cleanest possible safe structure is:

```text
gauge/topological reference bookkeeping
```

but that downgrades the route to:

```text
diagnostic closure
```

not:

```text
parent-derived local GR.
```

## 5. Gate Results

| Gate | Result | Meaning |
|---|---|---|
| stress_free_parent_action_found | fail | no stress-free action owns both `u` and `D` physically |
| stress_free_D_owner_found | partial pass | topological currents can own `D` |
| `C_coh` inside action allowed | fail | action coupling reintroduces stress/metric variation |
| local_GR_branch_promoted | fail | no derivation |
| diagnostic_closure_route_allowed | pass | useful internal benchmark remains |
| continue local parent route | fail | checkpoint 77 kill condition triggers |

This is not a total failure of MTS.

It is a failure of this specific local parent-action tunnel.

## 6. Demotion Register

| Route piece | New status | Allowed use |
|---|---|---|
| `C_coh` inside parent action | demoted | not used as derived local GR mechanism |
| auxiliary clock/cell reference | diagnostic closure only | internal frame/cell benchmark |
| topological `D` current | support structure | boundary/conservation bookkeeping |
| local GR reduction | unresolved, not derived | must be solved another way or treated empirically |

This matters because the theory discipline improves:

```text
We stop pretending a selector is a derivation.
```

## 7. What Survives

The following still survives:

- `C_coh` as a diagnostic/closure selector;
- topological/domain-current bookkeeping as support;
- empirical closure testing against data;
- amplitude-normalization work;
- a future local-GR derivation route if it does not hide behind `u/D` selectors.

The following does not survive:

```text
C_coh as a parent-action local-GR derivation via auxiliary clock/cell ownership.
```

## 8. What This Means Strategically

This checkpoint prevents a bad kind of theory drift.

If we kept going here, we would likely add more fields to avoid the fact that the reference sector either:

```text
gravitates
```

or:

```text
is only gauge/topological bookkeeping.
```

Neither gives the wanted result:

```text
MTS reduces to GR locally by derivation.
```

So the honest move is to demote this branch and pivot.

## 9. Recommended Pivot

Next checkpoint should decide between:

| Route | Why it is now sensible |
|---|---|
| amplitude normalization gate | central cross-sector parameter work remains unresolved |
| empirical closure testing | closure-level MTS can still be stress-tested honestly |
| perturbation/lensing/growth contract | needed for serious cosmology comparison |
| new local-GR route | deferred until a genuinely new mechanism appears |

Recommended next target:

```text
81-post-local-route-pivot-decision.md
```

Purpose:

```text
Choose the next high-value route after demoting the local C_coh parent-action branch.
```

## 10. Run Artifact

Script:

```text
research-programme\scripts\stress_free_reference_action_gate.py
```

Run directory:

```text
research-programme\runs\20260531-120531-stress-free-reference-action-gate
```

Generated tables:

```text
source_checkpoint_register.csv
action_candidates.csv
obstructions.csv
gate_results.csv
demotion_register.csv
next_route_options.csv
decision.csv
```

Status readout:

```text
stress_free_reference_parent_action_failed_local_Ccoh_demoted
```

## 11. Next Target

Create:

```text
81-post-local-route-pivot-decision.md
```

Acceptance:

```text
Do not continue the hidden-selector local route.
Choose the next route by promotion value: amplitude, empirical closure tests, perturbations, or a genuinely new local-GR mechanism.
```
