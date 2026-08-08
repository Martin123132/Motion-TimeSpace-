# 4743 Y5 R2FR: Kernel Projection Boundary Data Kill Test Or Adjoint Gap Source Value

Generated: `2026-07-08T00:09:01+00:00`

## Summary

- Work is local-only and private.
- This checkpoint attacks `Pi_0 m` directly.
- The kernel kill theorem is:

```text
m in ker(D_adj)
gamma_boundary m = 0
UCP(D_adj,W_loc)
-----------------
m=0
```

- The quotient-safe version also requires gauge/representative kernel modes to be parent-projected:

```text
Pi_0 m = Pi_phys Pi_0 m + Pi_gauge Pi_0 m
Pi_gauge Pi_0 m = 0
Pi_phys Pi_0 m = 0 or bounded
```

- Therefore `C_zeroMode=0` is not asserted; it is reduced to boundary trace, quotient projection, and physical-kernel tests.
- If those are not parent-signed, `C_zeroMode` remains the first finite source value.

## Kernel Kill Theorem

- `KKT4743_0_kernel_membership`: m in ker(D_adj) means D_adj m=0 on W_loc
- `KKT4743_1_trace_map`: gamma_boundary m := m|partial W_loc
- `KKT4743_2_unique_continuation_kill`: D_adj m=0 and gamma_boundary m=0 and UCP(D_adj,W_loc) => m=0
- `KKT4743_3_quotient_kill`: Pi_0 m = Pi_phys Pi_0 m + Pi_gauge Pi_0 m; parent quotient requires Pi_gauge Pi_0 m=0
- `KKT4743_4_kernel_bound`: ||Pi_0 m|| <= C_trace||gamma_boundary m|| + C_q||Pi_gauge Pi_0 m|| + C_phys||Pi_phys Pi_0 m||
- `KKT4743_5_exact_zero_branch`: gamma_boundary m=0, Pi_gauge Pi_0 m=0, Pi_phys Pi_0 m=0 => C_zeroMode=0

## Boundary Trace Contract

- `BTC4743_0_boundary_trace`: gamma_boundary m=0
- `BTC4743_1_boundary_flux`: B_adj[m]=0
- `BTC4743_2_fixed_collar`: D_v(partial W_loc)=0
- `BTC4743_3_fixed_domain`: D_v Dom(D_adj)=0
- `BTC4743_4_compact_support`: supp(m) compact in interior(W_loc)
- `BTC4743_5_topological_boundary`: delta_g S_boundary=0 in bulk(W_loc)

## Zero-Mode Family Test

- `ZMF4743_0_killing`: Killing/vector mode
- `ZMF4743_1_conformal`: conformal-Killing mode
- `ZMF4743_2_harmonic_scalar`: harmonic scalar mode
- `ZMF4743_3_TT`: TT/superpotential mode
- `ZMF4743_4_green`: Green inverse kernel
- `ZMF4743_5_corner`: corner/edge mode
- `ZMF4743_6_physical_kernel`: physical kernel mode

## C_zeroMode Bound Law

- `CZB4743_0_definition`: C_zeroMode := ||Pi_0 m||/a_ref
- `CZB4743_1_trace_bound`: C_zeroMode <= (C_trace/a_ref)||gamma_boundary m|| + (C_q/a_ref)||Pi_gauge Pi_0 m|| + (C_phys/a_ref)||Pi_phys Pi_0 m||
- `CZB4743_2_exact_trace_case`: gamma_boundary m=0 and Pi_gauge Pi_0 m=0 and Pi_phys Pi_0 m=0 => C_zeroMode=0
- `CZB4743_3_amplitude_insert`: A_m <= sqrt(C_zeroMode^2 + (C_Dadj^2 + C_boundary)/lambda_1^adj)

## Adjoint Gap Source Protocol

- `GAP4743_0_principal_symbol`: compute sigma(D_adj)(x,k)
- `GAP4743_1_boundary_condition`: choose parent-owned Dirichlet/compact-support/topological boundary class
- `GAP4743_2_gap_definition`: lambda_1^adj=first positive eigenvalue of D_adj^*D_adj
- `GAP4743_3_toy_runner`: toy collar eigenvalue smoke run
- `GAP4743_4_claim_gate`: lambda_1^adj>0 plus C_zeroMode=0 plus C_boundary=0

## Route Matrix

- `ROUTE4743_0_parent_boundary_trace`: find or write parent boundary trace contract for m
- `ROUTE4743_1_CzeroMode_source`: carry C_zeroMode as finite source row
- `ROUTE4743_2_gap_runner`: build toy adjoint spectral-gap runner
- `ROUTE4743_3_claim_now`: claim local-GR pass

## Promotion Gates

- `GATE4743_0_sources`: pass_internal
- `GATE4743_1_kernel_theorem`: conditional_pass
- `GATE4743_2_boundary_contract`: closed_unsigned
- `GATE4743_3_quotient_contract`: closed_unsigned
- `GATE4743_4_CzeroMode`: closed_unsigned
- `GATE4743_5_gap`: closed_unsigned
- `GATE4743_6_no_claim`: closed_firewall

## Decision

`KERNEL_PROJECTION_KILL_THEOREM_DERIVED_CONDITIONALLY_BOUNDARY_TRACE_AND_QUOTIENT_DATA_UNSIGNED_CZEROMODE_BOUND_STAGED_NONCLAIM`

## Next Target

`4744-Y5-R2FR-parent-boundary-trace-contract-or-CzeroMode-source-runner.md`
