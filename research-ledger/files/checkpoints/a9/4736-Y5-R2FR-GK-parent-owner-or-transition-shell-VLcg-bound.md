# 4736 Y5 R2FR: G_K Parent Owner Or Transition-Shell V_Lcg Bound

Generated: `2026-07-07T23:22:16+00:00`

## Summary

- Work is local-only and private.
- Target: prove `G_K` is parent-owned/q-basic, or turn its failure into a sourceable local bound.
- Result: exact conditional theorem exists, but scalar ownership of `K_B` is not enough.
- The transition-shell numerical rows are severe: constant trace and `U_B^2` both remain quarantined, with dry PPN proxy ratios of order `1e16`.

## Exact G_K Owner Fork

Use the covariant parent form:

```text
Y_a = P_a^b nabla_b ln K_B
G_K = (h^ab Y_a Y_b)^(1/2)
```

Then `D_v G_K=0` follows only if:

```text
D_v K_B = 0
D_v P_a^b = 0
D_v h^ab = 0
D_v connection/readout/support/boundary = 0
```

This is the precise fork: `K_B` scalar descent is necessary but not sufficient.

## Theorem Rows

- `GK4736_0_covariant_definition`: Let Y_a=P_a^b nabla_b ln K_B and G_K=(h^{ab}Y_aY_b)^(1/2); the radial source-model expression is the 1D proxy.
- `GK4736_1_exact_conditional_zero`: If K_B, P_a^b, h^{ab}, support, boundary and readout all descend through q, then D_v G_K=0 away from G_K=0.
- `GK4736_2_zero_set_caveat`: At G_K=0 the norm derivative is singular unless a regularized norm or separate homogeneous branch is used; FLRW uses the Hubble-cap branch.
- `GK4736_3_scalar_owner_not_enough`: K_B q-basic alone is insufficient because D_v G_K can still receive projector, connection, support and boundary/readout terms.

## K_B Owner Audit

- `KB4736_0_constructor`: K_B = w_C C_abs + w_R R_abs + eta_H H_bg^2/c^2
- `KB4736_1_exact_qbasic_condition`: D_v K_B=0 if C_abs, R_abs, H_bg and all weights descend/fix under q.
- `KB4736_2_weight_firewall`: w_C, w_R and eta_H cannot be chosen by sector or local test arena.
- `KB4736_3_floor_owner`: H_bg floor must be background q-basic on the local branch; otherwise V_LH feeds V_Lcg.

## G_K Bound

- `VGTK4736_0_definition`: V_GK := sup_local |D_v ln G_K| on the nonzero-gradient branch.
- `VGTK4736_1_parent_bound`: V_GK <= V_KB_grad + V_projector + V_metric + V_connection + V_support + V_boundary + V_readout.
- `VGTK4736_2_KB_grad`: V_KB_grad covers P nabla(D_v ln K_B), K_B zero/floor sensitivity and gradient-commutator terms.
- `VGTK4736_3_projector_connection`: V_projector+V_metric+V_connection vanish only if the local spatial projector/connection descend through q.
- `VGTK4736_4_support_boundary`: V_support+V_boundary covers transition-shell support motion and integration/readout boundary terms.

## Transition Shell Numeric Rows

- `TRANS4736_0_source_shell`: status `source_model_transition_shell_quarantined`, U_B `0.49999999997126643`, trace proxy `0.9999704774230199`, PPN ratio ``.
- `TRANS4736_1_constant_F_bound`: status `fails_dry_ppn_proxy_by_large_margin`, U_B `0.49999999997126643`, trace proxy `0.9999704774230199`, PPN ratio `2.2821012202909584e+16`.
- `TRANS4736_2_U_power_bound`: status `U_B_power_does_not_rescue_transition`, U_B `0.49999999997126643`, trace proxy `0.9999704774230199`, PPN ratio `2.3737930624621344e+16`.

## Propagation

- `PROP4736_0_to_VGk`: V_GK <= V_KB_grad + V_projector + V_metric + V_connection + V_support + V_boundary + V_readout
- `PROP4736_1_to_VLcg`: V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK
- `PROP4736_2_to_transition`: Transition shell requires q_current/K_hat cancellation or a dedicated current solver; U_B^2 is not enough there.

## Promotion Gates

- `GATE4736_0_exact_GK_theorem`: Promote G_K q-basic only if K_B plus projector/metric/connection/support/readout all descend.
- `GATE4736_1_zero_set_regularized`: Handle G_K=0 branch with FLRW/Hubble-cap or regularized norm before using ln G_K.
- `GATE4736_2_transition_bound`: Transition shell cannot pass from constant F or U_B^2 dry bound.
- `GATE4736_3_next_solver`: Move to transition current solver or exact K_hat cancellation identity.
- `GATE4736_4_no_public_claim`: No local-GR, PPN, R10 or Newtonian-limit pass from this checkpoint.

## Decision

`GK_QBASIC_OWNER_EXACT_CONDITIONAL_UNSIGNED_TRANSITION_SHELL_BOUND_FORCES_CURRENT_OR_KHAT_IDENTITY_NONCLAIM`

## Next Target

`4737-Y5-R2FR-transition-shell-current-solver-or-Khat-cancellation-identity.md`

No GitHub action was performed.
