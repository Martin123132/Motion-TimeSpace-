# 236 - Local EH Operator or Constraint Algebra Decision

Private route-decision checkpoint. This is not a public local-GR, PPN, clock,
WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 235 left two honest next routes:

```text
compute the X/P_mem constraint algebra,
or attack the local Einstein-Hilbert exterior operator.
```

This checkpoint chooses the next attack.

## 2. Machine Artifact

Script:

```text
scripts/local_EH_operator_or_constraint_algebra_decision.py
```

Run:

```text
runs/20260601-000053-local-EH-operator-or-constraint-algebra-decision
```

Command:

```text
python scripts/local_EH_operator_or_constraint_algebra_decision.py --timestamp 20260601-000053
```

Status:

```text
local_EH_operator_route_selected_constraint_algebra_deferred_no_local_GR_or_PPN_promotion
```

Claim ceiling:

```text
route_decision_only_no_EH_or_constraint_algebra_promotion
```

## 3. Route Comparison

| route | value | blocker | decision |
|---|---|---|---|
| `X/P_mem` constraint algebra | direct no-hair proof | missing parent symplectic form | defer |
| local EH exterior operator | direct beta/Schwarzschild route | parent exterior action not derived | select |
| empirical local-bound runner | numerical pressure test | coefficients not parent-derived | not yet |

The constraint-algebra route is real.

But right now it asks for:

```text
{C_X(x), C_X(y)}
```

without the parent symplectic structure.

That is not a useful calculation yet.

The local EH route can be attacked now because it has a clean finite contract.

## 4. Local EH Exterior Contract

The next derivation target is:

```text
S_ext[g] =
(16 pi G_eff)^-1
int_E sqrt(-g)(R - 2 Lambda_eff)
+ boundary,
```

with:

```text
T_matter|E = 0,
Pi_M charge = M_eff constant,
T_TF = 0,
Pi_matter = 0,
d_rel(P_mem J_rel) = 0,
T_projector = 0 or boundary-cancelled,
X/J_rel/V_def carry no exterior hair.
```

If this holds, then:

```text
G_mu_nu + Lambda_eff g_mu_nu = 0.
```

For compact Solar-System PPN:

```text
G_mu_nu = 0
```

to local order.

Then the static spherical exterior is Schwarzschild:

```text
g_00 = -1 + 2U - 2U^2 + O(U^3),
```

so:

```text
beta = 1.
```

## 5. Why Constraint Algebra Is Deferred

The constraint route still needs:

```text
parent Y symplectic structure,
boundary symplectic metric,
P[Y] ownership,
P_mem ownership,
boundary primitive ownership.
```

Without these, computing brackets is theatre.

So it is not abandoned.

It is parked until the parent symplectic owner exists.

## 6. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| route comparison written | pass |
| local EH selected as next target | pass |
| constraint algebra solved | fail |
| local EH operator derived | fail |
| local GR or PPN promoted | fail |

This is a route decision, not a theory win.

## 7. Decision

Decision:

```text
local_EH_operator_route_selected_constraint_algebra_deferred_no_local_GR_or_PPN_promotion
```

Meaning:

```text
the next attack should be the local Einstein-Hilbert exterior operator, not the
X/P_mem constraint algebra. The algebra route is real but blocked by the
missing parent symplectic structure.
```

Main gain:

```text
the local route now has a disciplined next target instead of looping over
missing symplectic data.
```

Main failure:

```text
neither EH operator nor constraint algebra is derived in this checkpoint.
```

## 8. Next Target

Create:

```text
237-local-EH-exterior-action-contract.md
```

Purpose:

```text
try to derive or sharply reject the exterior metric-only Einstein-Hilbert
action contract.
```

Pass condition:

```text
the parent MTS exterior reduces to a metric-only, diffeomorphism-invariant,
second-order action with no exterior memory hair.
```

Fail condition:

```text
the exterior is assumed to be GR because that is what local tests need.
```
