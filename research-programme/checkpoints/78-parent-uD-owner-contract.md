# 78 - Parent u/D Owner Contract

Private checkpoint. This is not a public claim.

## 1. Why This Exists

Checkpoint 76 showed the exact conservation failure:

```text
nabla_mu T_gate^munu =
E_Q L_xi Q
+ E_u L_xi u
+ E_D L_xi D
+ E_mem L_xi fields.
```

The route only becomes field-theoretic if `u` and `D` are owned by the parent structure.

Checkpoint 77 then set the fork:

```text
Either E_u/E_D ownership is made non-arbitrary,
or the local C_coh route is demoted to diagnostic closure.
```

This checkpoint writes the exact contract a future parent action must satisfy.

## 2. Short Verdict

```text
parent_uD_owner_status =
contract_route_found_not_derived
```

```text
selected_route =
auxiliary_clock_cell_reference
```

Plain English:

```text
The best route is to make u come from a clock/reference field and make D come from comoving cell labels or an equivalent conserved 3-form current.
```

This is not yet a derivation of local GR.

It is the first clean route that can own both missing objects without immediately declaring a new propagating fifth-force field.

## 3. Rejected Routes

| Candidate | Why it fails or gets downgraded |
|---|---|
| external observer and window | just chooses `u` and `D` by hand |
| Einstein-aether/khronon | owns `u`, but risks new propagating local preferred-frame physics |
| Brown-Kuchar dust as physical dust | owns `u` and `D`, but adds stress-energy |
| pure topological relative current | helps conservation bookkeeping but does not own `u` |

These are still useful templates, but not promotable as the local-GR route.

## 4. Selected Contract

The selected parent route has this skeleton:

```text
S_parent =
S_GR[g]
+ S_matter[g, psi]
+ S_mem[g, Q, ...]
+ S_ref[g, T, X^I, multipliers]
+ S_gate[g, Q, C_coh(T, X^I, g)]
```

where:

```text
u_mu = -nabla_mu T / sqrt(-X_T)
```

and:

```text
X_T = g^ab nabla_a T nabla_b T < 0.
```

The domain object is not a hand-picked averaging window. It must come from comoving cell labels:

```text
X^I, I = 1,2,3
```

or an equivalent conserved current:

```text
J_D^mu = star(dX^1 wedge dX^2 wedge dX^3),
nabla_mu J_D^mu = 0.
```

Then `D` is a material/comoving cell, not a smoothing choice.

## 5. What This Buys Us

Checkpoint 76 had loose terms:

```text
E_u L_xi u
E_D L_xi D
```

The parent route must replace them with:

```text
E_T L_xi T
E_XI L_xi X^I
```

or:

```text
E_J L_xi J_D.
```

That gives the conservation proof somewhere honest to put the `C_coh` exchange terms.

In other words:

```text
C_coh cannot be a magic switch.
It must be a derived functional of parent-owned reference structure.
```

## 6. The Main Danger

This route can easily cheat.

If `T` behaves like a real khronon/aether field, it can create preferred-frame physics.

If `X^I` behaves like physical dust, it can add stress-energy.

If `chi_D` is selected after the fact, then `D` is still hand-picked.

So the required stress guard is:

```text
S_ref must be auxiliary, constrained, topological, gauge/reference-like,
or otherwise stress-bounded below local PPN sensitivity.
```

If not, the local route fails.

## 7. Required Limit Tests

| Limit | Required result |
|---|---|
| local bound quiet bulk | stationary comoving cell gives average expansion -> 0 and `C_coh -> 0` |
| FLRW active background | cosmological comoving cell gives shear/vorticity -> 0 and `C_coh -> 1` |
| PPN local residual | reference sector adds no measurable preferred-frame/fifth-force stress |
| boundary transition | surface exchange is a controlled current, not a hidden source |

The same parent owner must produce both local silence and FLRW activity.

No branch-specific switch is allowed.

## 8. Exact Kill Tests

Checkpoint 79 must fail the route if any answer is yes:

```text
Can T be chosen freely to force C_coh?
Can X^I or chi_D be chosen after seeing the desired local/FLRW behavior?
Does conservation require delta C_coh = 0?
Does the reference sector source a new weak-field potential?
Does the construction need one owner for local systems and a different owner for FLRW?
```

If yes, the local transition route becomes:

```text
diagnostic_closure_only
```

not:

```text
derived_local_GR
```

## 9. Minimal Promotion Conditions

To promote this route even one step, checkpoint 79 must show:

1. `T` variation produces a real equation or constraint, not a chosen frame.
2. `X^I` or `J_D` variation produces a real domain/boundary rule.
3. `delta C_coh` terms are absorbed by parent equations or boundary currents.
4. the reference sector has no dangerous local stress.
5. local bound systems and FLRW use the same parent rule.

Until then:

```text
local_GR_status =
not_derived
```

## 10. Run Artifact

Script:

```text
research-programme\scripts\parent_uD_owner_contract.py
```

Run directory:

```text
research-programme\runs\20260531-115848-parent-uD-owner-contract
```

Generated tables:

```text
source_checkpoint_register.csv
owner_candidates.csv
selected_contract_terms.csv
noether_identity_map.csv
limit_conditions.csv
kill_tests.csv
decision.csv
```

Status readout:

```text
parent_uD_contract_route_found_not_derived
```

## 11. Next Target

Create:

```text
79-auxiliary-clock-cell-variation-attempt.md
```

Purpose:

```text
Attempt the explicit variation of the auxiliary clock/cell sector and audit whether its stress is zero, bounded, or fatal.
```

Expected fork:

```text
If the auxiliary sector owns u and D without new local stress, continue.
If it cannot, demote the C_coh local route and move to amplitude/empirical closure testing.
```
