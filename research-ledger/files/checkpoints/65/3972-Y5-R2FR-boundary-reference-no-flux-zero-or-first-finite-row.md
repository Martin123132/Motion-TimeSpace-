# 3972 - Boundary Reference No-Flux Zero Or First Finite Row

Timestamp: `2026-07-01T16:01:27+00:00`

## Result

3972 tried the clean route first:

```text
B_zero_flux = 0
Delta_symp = 0
```

That would close the scalar/reference boundary contribution:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref = 0
```

The current corpus does not parent-sign that zero. The reference lock and exact/improvement no-flux arguments remain conditional, so this checkpoint promotes the finite nonclaim row instead:

```text
epsilon_boundary_reference_abs = (|B_zero_flux| + |Delta_symp|)/M_H_ref
```

## Why This Moves The Framework

This is not another vague missing-item ledger. It turns one concrete boundary obstruction into a scoreable object with numerator terms, denominator, units, source requirements, and local-GR feed-through:

```text
epsilon_mu_extra_total <= epsilon_boundary_reference_abs
                        + epsilon_boundary_vector_tensor_normal_abs
                        + |Delta_PiM|
                        + |epsilon_domain_projector|
                        + remaining_channels_abs
```

## Decision

No local-GR claim is made. The scalar/reference boundary row is now ready to be filled or theorem-zeroed later.

Next target:

```text
3973-Y5-R2FR-boundary-vector-tensor-normal-flux-zero-or-coefficient-row.md
```

That step should attack the remaining boundary hair: vector, trace-free tensor, normal exchange, and derivative-silence terms.

Source needles found: `23/23`.
