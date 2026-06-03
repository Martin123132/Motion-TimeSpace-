# 237 - Local EH Exterior Action Contract

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 236 selected the next route:

```text
attack the local Einstein-Hilbert exterior operator.
```

This checkpoint asks:

```text
can MTS earn the exterior GR limit,
or are we only borrowing GR because local tests demand it?
```

## 2. Machine Artifact

Script:

```text
scripts/local_EH_exterior_action_contract.py
```

Run:

```text
runs/20260601-000054-local-EH-exterior-action-contract
```

Command:

```text
python scripts/local_EH_exterior_action_contract.py --timestamp 20260601-000054
```

Status:

```text
local_EH_exterior_action_contract_sharp_metric_only_gate_written_parent_reduction_not_derived_no_promotion
```

Claim ceiling:

```text
EH_exterior_contract_only_no_parent_metric_reduction_or_PPN_promotion
```

## 3. Exterior Contract

Define the compact exterior:

```text
E = {r > R_shell}.
```

The exact contract is:

```text
T_matter|E = 0,
Pi_M J -> M_eff,
nabla M_eff = 0,
T_TF|E = 0,
Pi_matter = 0,
P_mem J_rel = d_rel A_rel,
d_rel(P_mem J_rel) = 0,
T_projector = 0 or boundary-cancelled,
X/J_rel/V_def carry no exterior hair.
```

If all of that holds, the parent exterior reduces to:

```text
S_ext[g] =
(16 pi G_eff)^-1
int_E sqrt(-g)(R - 2 Lambda_eff)
+ boundary.
```

This is the metric-only exterior action contract.

It is not derived yet.

## 4. EH Chain

If the exterior parent action is:

```text
local,
diffeomorphism invariant,
metric-only,
second-order,
four-dimensional,
```

then the Lovelock/EH gate gives:

```text
G_mu_nu + Lambda_eff g_mu_nu = 0.
```

For compact Solar-System PPN scales, the constant `Lambda_eff` term is a
background correction, not the local beta issue, so:

```text
G_mu_nu = 0
```

to local PPN order.

For static spherical exterior:

```text
g_00 = -1 + 2U - 2U^2 + O(U^3),
```

therefore:

```text
beta = 1.
```

So beta is not mystical.

It is earned only if the exterior action contract is earned.

## 5. What Is Not Derived

The parent corpus does not yet derive:

```text
metric-only exterior reduction,
no exterior X/J_rel/V_def hair,
conserved M_eff source normalization,
T_projector cancellation,
universal matter/clock coupling,
two-derivative local metric operator.
```

So this checkpoint does not claim:

```text
MTS derives local GR,
MTS passes PPN,
MTS derives beta = 1.
```

It says:

```text
the exact conditions under which those statements would become derivable are
now written.
```

## 6. Why This Helps

Before this checkpoint:

```text
local EH exterior
```

was a route label.

After this checkpoint it is a hard contract:

```text
E1-E8 must be parent-owned before local GR is promoted.
```

That prevents the cheap move:

```text
outside the shell is GR because we need it to be.
```

The theory must instead prove:

```text
outside the shell, MTS has no non-metric exterior degrees left.
```

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| EH exterior contract written | pass |
| Lovelock/EH conditional chain written | pass |
| beta condition sharpened | pass |
| metric-only exterior parent-derived | fail |
| local EH operator derived | fail |
| local GR or PPN promoted | fail |

The pass rows define the route.

The fail rows stop overclaiming.

## 8. Decision

Decision:

```text
local_EH_exterior_action_contract_sharp_metric_only_gate_written_parent_reduction_not_derived_no_promotion
```

Meaning:

```text
MTS earns local EH only if all non-metric exterior sectors reduce to a conserved
monopole or vanish/boundary-cancel, leaving a local metric-only
diffeomorphism-invariant two-derivative action.
```

Main gain:

```text
the exact conditions for deriving GR outside a compact collar are explicit.
```

Main failure:

```text
metric-only exterior reduction and no-hair remain unproved.
```

## 9. Next Target

Create:

```text
238-metric-only-exterior-reduction-or-nohair-theorem.md
```

Purpose:

```text
try to prove or reject the key reduction:
outside the compact collar, all MTS non-metric sectors are either zero,
pure boundary terms, or conserved M_eff.
```

Pass condition:

```text
S_parent|E -> S_ext[g;G_eff,Lambda_eff,M_eff]
```

without extra exterior fields.

Fail condition:

```text
metric-only exterior is inserted as a PPN rescue assumption.
```
