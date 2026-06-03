# 305 - Fifth-Force Gradient Runner

Private local-bound checkpoint. This is not a public fifth-force, local-GR, PPN, cosmology, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 304 fixed the beta guard and left the next local danger:

```text
grad(Lambda_D Tr(P_iso q_r)).
```

This checkpoint builds a runner for the question:

```text
if epsilon_loc is nonzero, does its spatial profile create a local fifth-force-like acceleration?
```

## Runner Definition

The proxy acceleration ratio is:

```text
gradient_ratio = epsilon_loc * shape_factor * L_test / L_profile.
```

Meaning:

```text
epsilon_loc = local trace-source amplitude,
L_test = local system/test length scale,
L_profile = scale over which the trace source varies,
shape_factor = dimensionless gradient shape.
```

If:

```text
epsilon_loc=0
```

or:

```text
shape_factor=0
```

then the fifth-force proxy is exactly zero.

If `epsilon_loc` is nonzero, the source must be sufficiently flat:

```text
L_profile >= epsilon_loc * shape_factor * L_test / bound.
```

## Results

Exact/constant cases pass:

```text
exact_silence_no_gradient
constant_trace_source
```

Flat or tiny leakage can pass:

```text
beta_bounded_flat_profile
tiny_selector_strict_profile_pass
```

Local gradient fail probe fails:

```text
beta_bounded_local_gradient_fail
```

This is the intended behaviour.

The runner is not rubber-stamping the branch.

## Interpretation

The local story is now sharper:

```text
nonzero epsilon_loc is not automatically safe.
```

It is safe only if at least one of these holds:

```text
1. exact selector silence,
2. spatially constant/unobservable trace source,
3. profile scale much larger than the local test scale,
4. tiny enough epsilon_loc after selector suppression.
```

Otherwise:

```text
the fifth-force channel can fail even if gamma/beta proxy gates pass.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | runner traceable |
| gradient runner constructed | pass | nonzero `epsilon_loc` faces spatial-gradient gate |
| exact or constant sources pass | pass | zero gradient is safe in proxy runner |
| flat profile pass exists | pass | nonzero leakage can pass if flat enough |
| local gradient failure probe fails | pass | runner catches dangerous leakage |
| official fifth-force claim allowed | fail | proxy/internal bounds only |
| local GR promoted | fail | selector/profile not parent-derived |
| `B_mem` parent-derived | fail | amplitude unchanged |

## Decision

Decision:

```text
fifth_force_gradient_runner_ready_nonzero_epsilon_requires_flat_profile_no_local_GR_promotion
```

Meaning:

```text
the local branch now has a fifth-force gradient gate,
but it is still proxy-level and not a local-GR proof.
```

What improved:

```text
nonzero local leakage must now make weight in gamma, beta, and gradient channels.
```

What did not improve:

```text
the parent theory has not derived the selector or the trace-source profile.
```

So:

```text
local GR remains unpromoted.
```

Boxing-score version:

```text
We checked the footwork now, not just the punches.
Even if beta is guarded, a bad spatial gradient still gets clipped.
Only silence, flatness, or tiny leakage survives.
```

## Machine Artifacts

Script:

```text
scripts/fifth_force_gradient_runner.py
```

Run:

```text
runs/20260601-000128-fifth-force-gradient-runner
```

Output files:

```text
runs/20260601-000128-fifth-force-gradient-runner/results/source_register.csv
runs/20260601-000128-fifth-force-gradient-runner/results/bound_manifest_proxy.csv
runs/20260601-000128-fifth-force-gradient-runner/results/candidate_profiles.csv
runs/20260601-000128-fifth-force-gradient-runner/results/gradient_results.csv
runs/20260601-000128-fifth-force-gradient-runner/results/promotion_gates.csv
runs/20260601-000128-fifth-force-gradient-runner/results/decision.csv
```

## Next Step

The remaining local-theory target is:

```text
derive the trace-source profile,
or require exact selector silence locally.
```

If we stop pushing local theory here, the honest empirical next step is:

```text
return to stronger cosmology/holdout testing,
while local GR remains conditional.
```
