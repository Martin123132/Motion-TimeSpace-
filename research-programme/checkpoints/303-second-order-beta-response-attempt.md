# 303 - Second-Order Beta Response Attempt

Private local-bound checkpoint. This is not a public local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 302 left the standard PPN blocker:

```text
beta_minus_1.
```

This checkpoint asks:

```text
can beta be derived for trace-only epsilon_loc leakage?
```

Short answer:

```text
the beta-zero condition can be derived exactly.
```

But:

```text
the parent theory has not yet proved the condition.
```

## Weak-Field Setup

Write the local weak-field temporal metric as:

```text
g_00 = -1 + 2 A U - 2 B U^2 + O(U^3).
```

The first-order locally fitted Newtonian potential is:

```text
U_obs = A U.
```

Rewriting in terms of `U_obs` gives:

```text
g_00 = -1 + 2 U_obs - 2 (B/A^2) U_obs^2 + ...
```

Therefore:

```text
beta_eff = B/A^2.
```

Now expand:

```text
A = 1 + a1 epsilon_loc,
B = 1 + b1 epsilon_loc.
```

Then:

```text
beta_eff - 1 = (b1 - 2a1) epsilon_loc + O(epsilon_loc^2).
```

So:

```text
c_beta = b1 - 2a1.
```

## Beta-Zero Condition

Beta is safe at linear order if:

```text
b1 = 2a1.
```

Equivalently:

```text
B = A^2
```

to the relevant order.

Physics meaning:

```text
the trace-only leakage must complete as a GR-like local mass/GM renormalization.
```

If it does, beta is just absorbed into the fitted first-order potential:

```text
beta_eff = 1.
```

That is the good route.

## Failure Mode

If the leakage changes only the linear potential:

```text
A = 1 + epsilon_loc,
B = 1,
```

then:

```text
c_beta = -2.
```

So the old safety guard:

```text
c_beta = 1
```

is too optimistic for a linear-only leak.

Until `B=A^2` is parent-derived, the conservative guard should be:

```text
|c_beta| = 2.
```

## Cases

| Case | Result |
|---|---|
| exact selector silence | beta zero |
| GR mass renormalization | beta zero conditionally |
| linear-only trace leak | beta active, `c_beta=-2` |
| half-completed nonlinear response | beta active |
| over-completed response | beta active |

So the beta branch is not hopeless.

It is precise:

```text
derive B=A^2,
or keep beta guarded.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| beta formula derived | pass | `beta_eff=B/A^2` |
| beta-zero condition identified | pass | `b1=2a1` |
| parent proves `B=A^2` | fail | no second-order field equation yet |
| linear-only leak guarded | pass | use `|c_beta|=2` guard |
| official PPN claim allowed | fail | no local-GR/PPN promotion |
| fifth-force gradient closed | fail | still open |
| `B_mem` parent-derived | fail | amplitude unchanged |

## Decision

Decision:

```text
second_order_beta_zero_condition_derived_nonlinear_completion_not_parent_owned
```

Meaning:

```text
beta is safe if epsilon_loc is a GR-like mass renormalization,
but not if it is merely an added linear trace potential.
```

What improved:

```text
the beta problem is now one exact condition:
B=A^2.
```

What did not improve:

```text
the parent action has not yet proved B=A^2.
```

So:

```text
local GR remains unpromoted.
```

Boxing-score version:

```text
Beta finally showed its tell:
if the second punch follows the square of the first, we slip it.
If not, beta lands clean.
No belt until the combo is parent-owned.
```

## Machine Artifacts

Script:

```text
scripts/second_order_beta_response_attempt.py
```

Run:

```text
runs/20260601-000126-second-order-beta-response-attempt
```

Output files:

```text
runs/20260601-000126-second-order-beta-response-attempt/results/source_register.csv
runs/20260601-000126-second-order-beta-response-attempt/results/beta_formula.csv
runs/20260601-000126-second-order-beta-response-attempt/results/beta_cases.csv
runs/20260601-000126-second-order-beta-response-attempt/results/runner_policy_update.csv
runs/20260601-000126-second-order-beta-response-attempt/results/derivation_gates.csv
runs/20260601-000126-second-order-beta-response-attempt/results/next_targets.csv
runs/20260601-000126-second-order-beta-response-attempt/results/decision.csv
```

## Next Step

Immediate implementation target:

```text
update the epsilon_loc runner so the conservative beta guard is |c_beta|=2
unless B=A^2 is derived.
```

Then:

```text
build the fifth-force gradient runner.
```

Reason:

```text
gamma, clock, matter, and beta now have conditional guardrails;
the remaining local leakage danger is spatial gradient/fifth-force behaviour.
```
