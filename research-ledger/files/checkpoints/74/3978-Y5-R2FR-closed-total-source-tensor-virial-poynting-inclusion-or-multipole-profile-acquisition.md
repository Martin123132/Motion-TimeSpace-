# 3978 - Closed Total Source Tensor-Virial Poynting Inclusion Or Multipole Profile Acquisition

Timestamp: `2026-07-01T16:40:29+00:00`

## Result

3978 takes the source-side route seriously.

The strongest honest zero certificate is:

```text
Z_source_Q_zero =
  Z_closed_worldtube
* Z_total_balance
* Z_stationary_TF_virial
* Z_surface_exchange_zero
* Z_Poynting_included
* Z_GR_multipole_routing
* Z_exterior_vacuum_annulus

Z_source_Q_zero = 1
=> Q_lm^source,res = 0 for l >= 1
```

## What This Actually Proves

Tensor virial can suppress the integrated tracefree stress residual of a closed stationary total source:

```text
d2I_TF/dt2 = 2 int_W T_TF^tot d3x + surface_TF + exchange_TF
```

So if `d2I_TF/dt2=0` and the surface/exchange terms vanish, `int_W T_TF^tot d3x=0`.

That does **not** erase real GR mass quadrupoles. Those must be routed into the GR comparator before judging extra MTS residual hair:

```text
Q_lm^source,res := P_residual(Q_lm^total - Q_lm^GR_baseline)
```

## Poynting Decision

The Poynting vector is not deleted. It is either included inside the closed total Hilbert/Maxwell source or retained as:

```text
epsilon_EM_Poynting_TF
```

Internal `S_EM` circulation is allowed. Only the total boundary flux is constrained.

## Fallback Bound

Until the certificate is parent-signed:

```text
epsilon_source_l_ge_1 <=
  epsilon_closed_source_failure
+ epsilon_tensor_virial_TF
+ epsilon_quad_residual_TF
+ epsilon_EM_Poynting_TF
+ epsilon_apparatus_TF
```

No local-GR, SO3, or EM-origin claim is made.

Next target:

```text
3979-Y5-R2FR-GR-baseline-residual-projector-contract-or-source-profile-runner.md
```

Source needles found: `28/28`.
