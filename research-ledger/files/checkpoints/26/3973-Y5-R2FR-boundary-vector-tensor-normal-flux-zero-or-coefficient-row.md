# 3973 - Boundary Vector Tensor Normal Flux Zero Or Coefficient Row

Timestamp: `2026-07-01T16:07:53+00:00`

## Result

3973 decomposes the remaining boundary hair instead of leaving it as a single foggy blocker:

```text
K_B = K_trace h + K_TF + 2 n_(mu J_B_nu) + V_B + derivative/reference pieces
```

The harmless case is now sharp:

```text
S_B = int_boundary sqrt(|gamma|) F(scalars)
D_A scalars = 0
no marker vector/current/shear label
fixed observed coframe
no normal exchange
derivative silence

=> V_B = Pi_B = J_B = D_B = 0
```

That is a real conditional lemma, not a closure axiom. It is **not** promoted because the current parent action does not yet own those premises.

## Coefficient Fallback

If the parent-action proof fails, the boundary hair now has fillable rows:

```text
epsilon_boundary_vector_tensor_normal_abs
W_boundary_alpha1_epsilon_boundary_vector
W_boundary_alpha2_epsilon_boundary_vector
W_boundary_alpha3_epsilon_boundary_normal
W_boundary_xi_epsilon_boundary_TF
W_boundary_beta_epsilon_boundary_hair
dln_mu_boundary_dt
```

These feed:

```text
epsilon_boundary
epsilon_mu_extra_total
Delta_B_single_mass
Delta_PPN_source_abs
```

## Decision

No local-GR claim is made. But the next target is now more ambitious and cleaner: parent-own the boundary action premises, because that would kill the whole boundary hair vector rather than chasing one coefficient at a time.

Next target:

```text
3974-Y5-R2FR-parent-boundary-action-scalar-marker-free-contract-or-coefficient-values.md
```

Source needles found: `28/28`.
