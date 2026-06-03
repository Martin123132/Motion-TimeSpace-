# 246 - Auxiliary Nohair Rank-Bracket or Local EH Pivot

Private local-derivation checkpoint. This is not a public beta, PPN, local-GR,
or field-theory completion claim.

## 1. Trigger

Checkpoint 245 left the next local gate:

```text
N6 auxiliary no-hair.
```

Question:

```text
are X/J_rel/V_def truly constrained auxiliary fields with no exterior
propagating hair,
or should we pivot back to the local EH exterior operator?
```

## 2. Machine Artifact

Script:

```text
scripts/auxiliary_nohair_rank_bracket_or_local_EH_pivot.py
```

Run:

```text
runs/20260601-000063-auxiliary-nohair-rank-bracket-or-local-EH-pivot
```

Command:

```text
python scripts/auxiliary_nohair_rank_bracket_or_local_EH_pivot.py --timestamp 20260601-000063
```

Status:

```text
N6_auxiliary_nohair_rank_necessary_not_sufficient_bracket_blocked_EH_exterior_pivot_selected_no_promotion
```

Claim ceiling:

```text
N6_route_decision_no_auxiliary_nohair_or_local_EH_promotion
```

## 3. N6 Test

The good route remains:

```text
X_nu is a multiplier,
not a propagating vector field.
```

Necessary condition:

```text
rank d^2 L / d dot(X) d dot(X) = 0.
```

This can be satisfied by the first-order route.

But rank-zero is not enough.

The real no-hair proof requires:

```text
pi_X^nu ~= 0,
C_X^nu = -nabla_mu P[Y]^{mu nu} + J_eff[Y]^nu ~= 0,
{C_X^nu(x), C_X^rho(y)} closes on parent constraints.
```

That bracket cannot be computed honestly yet because:

```text
the parent Y symplectic structure is missing.
```

So:

```text
auxiliary-by-assertion is rejected.
```

## 4. Route Decision

| route | decision |
|---|---|
| continue constraint algebra now | defer |
| declare auxiliary by rank only | reject |
| pivot to local EH exterior stack | select |

Reason:

```text
bracket calculation without the parent Poisson/symplectic structure is theatre.
```

The local EH exterior stack can be written now as a finite sufficiency theorem,
as long as every unresolved N-gate remains visible.

## 5. EH Exterior Sufficiency Stack

The metric-only exterior route needs:

| condition | status |
|---|---|
| ordinary matter absent outside compact source | exterior definition |
| `N1_Meff` conserved monopole | conditional gate |
| `N2_no_TF` no trace-free/shear stress | conditional gate |
| `N3` strict coframe/universal matter | conditional gate |
| `N4` exact relative memory | conditional gate |
| `N5` projector stress Bianchi-safe | open |
| `N6` auxiliary no-hair | open |
| metric-only two-derivative exterior action | target |

If all hold, the target exterior action is:

```text
S_ext[g] =
(16 pi G)^-1 int_E sqrt(-g)(R - 2 Lambda_eff)
+ boundary.
```

Then:

```text
G_mu_nu + Lambda_eff g_mu_nu = 0.
```

For compact Solar-System PPN order:

```text
G_mu_nu = 0,
```

and the static spherical exterior is Schwarzschild:

```text
beta = 1.
```

This is still conditional.

## 6. What Improved

Before this checkpoint:

```text
N6 could tempt us into saying "rank zero, therefore harmless".
```

After this checkpoint:

```text
rank zero is explicitly only a necessary condition,
the bracket route is deferred until parent symplectic structure exists,
and the EH exterior stack is selected as the next disciplined target.
```

That is useful because it prevents the local branch from winning by paperwork.

## 7. What Still Fails

Still not derived:

```text
X/J_rel/V_def no-hair,
P[Y] or V_def constitutive owner,
parent symplectic structure,
projector stress cancellation,
metric-only EH exterior operator.
```

So this checkpoint does not claim:

```text
auxiliary no-hair,
beta = 1,
PPN pass,
local GR.
```

## 8. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| rank-zero `X` kinetic condition identified | conditional pass |
| constraint algebra closed | fail |
| auxiliary no-hair declared by rank only | fail |
| local EH exterior pivot selected | pass |
| local GR or PPN promoted | fail |

## 9. Decision

Decision:

```text
N6_auxiliary_nohair_rank_necessary_not_sufficient_bracket_blocked_EH_exterior_pivot_selected_no_promotion
```

Meaning:

```text
N6 cannot be honestly derived from rank-zero alone. The next move is to write a
local EH exterior sufficiency stack with every unresolved N-gate explicit.
```

Main gain:

```text
the no-hair route is prevented from becoming handwaving.
```

Main failure:

```text
N6, N5, and the metric-only EH exterior are still not parent-derived.
```

## 10. Next Target

Create:

```text
247-local-EH-exterior-sufficiency-stack-no-promotion.md
```

Purpose:

```text
write the exact sufficient theorem for beta/local GR from N1-N6 plus a
metric-only exterior action, while keeping every assumption visible.
```

Pass condition:

```text
the stack is internally complete and does not hide any non-metric exterior
sector.
```

Fail condition:

```text
the exterior is declared Einstein-Hilbert because local tests need it.
```
