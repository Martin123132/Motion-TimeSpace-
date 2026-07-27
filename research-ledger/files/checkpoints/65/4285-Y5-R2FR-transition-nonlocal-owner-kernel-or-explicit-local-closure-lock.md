# 4285 - transition nonlocal owner kernel or explicit local closure lock

Marker: `PPC4161_TRANSITION_NONLOCAL_OWNER_KERNEL_OR_EXPLICIT_CLOSURE_LOCK_4285`

Decision: `PARENT_NONLOCAL_OWNER_KERNEL_NOT_DERIVED_TRANSITION_LOCAL_SAFETY_LOCKED_AS_EXPLICIT_NOLEAK_CLOSURE_NONCLAIM`

4285 locks the failed transition-shell local safety route as explicit no-leak closure:

```text
P_metric,loc = 0,
P_Q + P_gal + P_cos + P_metric,loc = 1,
theta_closure = {P_Q, P_gal, P_cos, xi_Q},
```

because the parent nonlocal owner/kernel theorem is not derived.
