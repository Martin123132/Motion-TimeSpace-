# 306 - Trace-Source Profile Theorem Attempt

Private local-theory checkpoint. This is not a public fifth-force, local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 305 showed:

```text
nonzero epsilon_loc is safe only if the trace source is exactly silent,
constant,
tiny,
or very flat over the local test scale.
```

This checkpoint asks:

```text
can the flat trace-source profile be derived?
```

Short answer:

```text
there is a clean conditional theorem.
```

But:

```text
the parent theory has not derived its boundary/no-source conditions.
```

## Profile Equation

Let the local scalar trace source be:

```text
s_D = Lambda_D Tr(P_iso q_r).
```

Use a minimal effective profile functional:

```text
F_s = integral_D [
  kappa_s/2 |grad s_D|^2
  + m_s^2/2 (s_D-s0)^2
  - j_s s_D
].
```

The profile equation is:

```text
(-kappa_s Laplacian + m_s^2) s_D
= m_s^2 s0 + j_s.
```

A fifth-force-like residual is controlled by:

```text
grad s_D.
```

## Flat-Profile Sufficient Condition

If:

```text
j_s = constant,
s0 = constant,
n.grad s_D | boundary D = 0,
m_s^2 > 0,
```

then the solution is constant:

```text
s_D = (m_s^2 s0 + j_s)/m_s^2.
```

Therefore:

```text
grad s_D = 0.
```

So nonzero `epsilon_loc` can be fifth-force safe if it is:

```text
a constant/unobservable local trace renormalization.
```

This is the best flat-profile route.

## What Fails

Flatness is not automatic.

It fails if:

```text
j_s(x) is spatially varying,
boundary values mismatch,
local trace coupling is localized,
or the parent action permits trace-source gradients.
```

Those cases generically give:

```text
grad s_D != 0.
```

Then the fifth-force runner remains necessary.

## No-Go Checks

| Claim | Result | Reason |
|---|---|---|
| trace-only source automatically means no fifth force | fail | tensor trace does not fix spatial profile |
| constant profile can be assumed locally | fail as derivation | needs boundary/no-source theorem |
| mass term always screens safely | partial | can still make gradients near sources |
| beta-bounded leakage is automatically safe | fail | beta does not test spatial force |

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| profile equation constructed | pass | flatness has a theorem target |
| constant profile sufficient condition | conditional pass | Neumann/no-source gives `grad s_D=0` |
| profile parent-derived | fail | boundary/no-source conditions not derived |
| localized source safe | fail | gradients generically appear |
| official fifth-force claim allowed | fail | no official bound/profile scale |
| local GR promoted | fail | selector/profile theorem conditional |
| `B_mem` parent-derived | fail | amplitude unchanged |

## Decision

Decision:

```text
trace_source_flat_profile_conditional_neumann_theorem_not_parent_derived
```

Meaning:

```text
nonzero local leakage can be fifth-force safe if it is a constant trace renormalization,
but the parent theory has not derived the required local profile conditions.
```

What improved:

```text
the flat-profile condition is now precise:
Neumann/no-flux boundary plus no spatially varying local source.
```

What did not improve:

```text
the parent action has not proved those conditions.
```

So:

```text
local GR remains unpromoted.
```

Boxing-score version:

```text
We found how to make the fifth-force punch miss:
make the trace source a flat background, not a local jab.
But the corner still has to prove that is the stance the theory actually takes.
```

## Machine Artifacts

Script:

```text
scripts/trace_source_profile_theorem_attempt.py
```

Run:

```text
runs/20260601-000129-trace-source-profile-theorem-attempt
```

Output files:

```text
runs/20260601-000129-trace-source-profile-theorem-attempt/results/source_register.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/profile_equation.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/solution_classes.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/gradient_implications.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/no_go_tests.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/promotion_gates.csv
runs/20260601-000129-trace-source-profile-theorem-attempt/results/decision.csv
```

## Next Step

The local branch has now been squeezed hard enough for this round.

Recommended next:

```text
write a local-branch status ledger,
then pivot back to stronger empirical holdout testing.
```

Reason:

```text
local GR is much better gated,
but still conditional;
the framework now needs empirical pressure again.
```
