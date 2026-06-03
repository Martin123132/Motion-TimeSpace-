# 247 - Local EH Exterior Sufficiency Stack, No Promotion

Private local-derivation checkpoint. This is not a public beta, PPN, local-GR,
or field-theory completion claim.

## 1. Trigger

Checkpoint 246 selected the next disciplined route:

```text
write the exact sufficient theorem for beta/local GR from N1-N6 plus a
metric-only exterior action, while keeping every assumption visible.
```

This checkpoint writes that theorem.

## 2. Machine Artifact

Script:

```text
scripts/local_EH_exterior_sufficiency_stack_no_promotion.py
```

Run:

```text
runs/20260601-000064-local-EH-exterior-sufficiency-stack-no-promotion
```

Command:

```text
python scripts/local_EH_exterior_sufficiency_stack_no_promotion.py --timestamp 20260601-000064
```

Status:

```text
local_EH_exterior_sufficiency_stack_complete_as_conditional_theorem_parent_N_gates_open_no_promotion
```

Claim ceiling:

```text
EH_sufficiency_stack_only_no_parent_reduction_beta_or_local_GR_promotion
```

## 3. Sufficiency Theorem

If the compact exterior satisfies:

```text
T_matter|E = 0,
N1_Meff,
N2_no_TF,
N3_universal_strict_coframe,
N4_exact_relative_memory,
N5_projector_stress_Bianchi_safe,
N6_auxiliary_nohair,
```

and if the remaining exterior action is:

```text
local,
four-dimensional,
diffeomorphism invariant,
metric-only,
second-order,
```

then:

```text
S_ext[g] =
(16 pi G)^-1 int_E sqrt(-g)(R - 2 Lambda_eff)
+ boundary.
```

So:

```text
G_mu_nu + Lambda_eff g_mu_nu = 0.
```

For compact Solar-System PPN order:

```text
G_mu_nu = 0.
```

For static spherical exterior:

```text
g_00 = -1 + 2U - 2U^2 + O(U^3),
beta = 1.
```

That is the local EH sufficiency theorem.

## 4. Premise Status

| premise | current status |
|---|---|
| ordinary matter absent | exterior definition |
| `N1_Meff` | conditional gate |
| `N2_no_TF` | conditional gate |
| `N3` strict coframe | conditional gate |
| `N4` exact relative memory | conditional gate |
| `N5` projector stress | open |
| `N6` auxiliary no-hair | open |
| metric-only second-order operator | target, not derived |

So:

```text
the theorem is internally complete,
but the parent theory has not satisfied its premises.
```

## 5. Hidden-Sector Audit

Every known non-metric exterior sector must be:

```text
zero,
pure boundary,
conserved M_eff,
or explicitly retained in a conserved stress ledger.
```

Current audit:

| sector | allowed exterior status | current disposition |
|---|---|---|
| `M_eff` mass flux | conserved monopole | conditional `N1` |
| trace-free shear | zero | conditional `N2` |
| direct matter/clock vertex | absent | conditional `N3` |
| relative memory `J_rel` | exact/pure gauge boundary | conditional `N4` |
| projector stress | zero or retained | open `N5` |
| `X/J_rel/V_def` auxiliary sector | no exterior degrees | open `N6` |
| boundary primitive `A_rel` | pure gauge/boundary-cancelled | open within `N4/N6` |

Nothing is allowed to disappear by prose.

## 6. Claim Discipline

Allowed claim:

```text
if all premises hold, beta=1 follows.
```

Not allowed:

```text
MTS derives beta=1 now,
MTS passes PPN now,
MTS derives local GR now.
```

Also not supported:

```text
the local branch is dead.
```

Reason:

```text
the sufficiency stack is coherent and has not hit a contradiction,
but it is not yet parent-owned.
```

## 7. What Improved

Before this checkpoint:

```text
local GR was a route made of many conditional gates.
```

After this checkpoint:

```text
local GR is a finite premise stack.
```

This is useful because it makes the next work obvious:

```text
derive or reject each remaining premise.
```

## 8. What Still Fails

Still not derived:

```text
N5 projector-stress zero/retained theorem,
N6 auxiliary no-hair,
parent metric-only exterior reduction,
parent owners for several conditional gates.
```

Therefore:

```text
local GR is not promoted.
```

## 9. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| EH sufficiency theorem internally written | pass |
| hidden nonmetric exterior sectors audited | pass |
| all premises parent-derived | fail |
| beta/local GR promoted | fail |

## 10. Decision

Decision:

```text
local_EH_exterior_sufficiency_stack_complete_as_conditional_theorem_parent_N_gates_open_no_promotion
```

Meaning:

```text
the local branch now has a complete conditional theorem: if N1-N6 and
metric-only exterior reduction hold, local EH and beta=1 follow.
```

Main gain:

```text
local GR is now a finite premise stack rather than a vague hope.
```

Main failure:

```text
N5, N6, parent metric-only reduction, and several parent owners remain unproved.
```

## 11. Next Target

Create:

```text
248-projector-stress-zero-or-retained-theorem.md
```

Purpose:

```text
attack N5 directly: either prove projector stress vanishes under the same
topological/pure-gauge conditions, or keep it explicitly in a conserved total
stress ledger.
```

Pass condition:

```text
T_projector = 0,
```

or:

```text
nabla_mu(T_metric + T_Meff + T_TF + T_rel + T_projector + T_boundary)^{mu nu}=0
```

is derived from a parent variational identity.

Fail condition:

```text
projector stress is ignored because the EH stack needs it gone.
```
