# 302 - Epsilon-Loc Parent Coefficient Map Attempt

Private local-bound checkpoint. This is not a public local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 301 built the `epsilon_loc` runner, but left a key weakness:

```text
the residual coefficients were proxy/manifest-level.
```

This checkpoint asks:

```text
can the parent/open-sector structure derive the coefficients?
```

Short answer:

```text
partly.
```

The common-mode and universal-coupling pieces help.

But:

```text
beta and fifth-force gradients remain open.
```

## Conditional Coefficient Map

If the open-sector local leakage is trace-only and common-mode:

```text
delta Phi = delta Psi,
```

then:

```text
c_gamma = 0
c_slip = 0
```

at leading weak-field order.

If matter and clocks couple only through the metric/coframe:

```text
c_clock = 0
c_matter = 0.
```

That is the good news.

It means the harsh direct-matter failure mode in checkpoint 301 is avoidable if universal metric coupling is parent-owned.

## What Remains Open

The dangerous channels are:

```text
beta_minus_1
fifth_force_gradient
```

`beta` remains open because:

```text
it needs a second-order weak-field temporal metric solution.
```

The fifth-force gradient remains open because:

```text
grad(Lambda_D Tr(P_iso q_r))
```

could be nonzero if the local selector is not exactly zero.

So for bounded leakage, the recommended internal runner policy is:

```text
c_gamma = 0
c_beta = 1 as a safety guard
c_clock = 0
c_matter = 0
c_fifth_force = 1 as a safety guard
```

This is better than the previous toy proxy.

It is still not a PPN proof.

## Response Cases

| Case | Result |
|---|---|
| exact selector silence | all local residuals zero |
| trace-only common mode | `gamma` safe, beta open |
| anisotropic stress leakage | gamma/slip active danger |
| direct matter/clock coupling | WEP/LPI danger |

So the local branch has a sharp requirement:

```text
either exact silence,
or trace-only common-mode leakage with beta/fifth-force guards passed.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | attempt traceable |
| gamma coefficient derived | conditional pass | `c_gamma=0` under trace-only common mode |
| clock/matter coefficients zero | conditional pass | universal metric coupling needed |
| beta coefficient derived | fail | second-order solution missing |
| fifth-force gradient derived | fail | local source profile missing |
| official PPN claim allowed | fail | coefficient map incomplete |
| epsilon runner policy improved | pass | use common-mode plus beta/gradient guards |
| `B_mem` parent-derived | fail | amplitude unchanged |

## Decision

Decision:

```text
epsilon_loc_parent_coefficients_partially_derived_common_mode_beta_and_fifth_force_open
```

Meaning:

```text
the local coefficient map improved,
but local GR is still not promoted.
```

What improved:

```text
gamma/slip can be killed by trace-only common-mode response,
and direct clock/matter failures can be killed by universal coupling.
```

What did not improve:

```text
beta and fifth-force gradients still need real derivations or bounds.
```

Boxing-score version:

```text
We slipped the jab: gamma and matter coupling can be made safe.
But beta is still standing in the centre of the ring,
and the fifth-force hook is not accounted for yet.
```

## Machine Artifacts

Script:

```text
scripts/epsilon_loc_parent_coefficient_map_attempt.py
```

Run:

```text
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt
```

Output files:

```text
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/source_register.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/coefficient_derivation.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/metric_response_cases.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/recommended_runner_policies.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/coefficient_gates.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/next_targets.csv
runs/20260601-000125-epsilon-loc-parent-coefficient-map-attempt/results/decision.csv
```

## Next Step

The next local-theory target is:

```text
derive the second-order beta response,
or build the fifth-force gradient runner.
```

Recommended:

```text
try the second-order beta solution first.
```

Reason:

```text
beta is the remaining standard PPN channel blocking even a conditional local-GR story.
```
