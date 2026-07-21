# 4748 Y5 R2FR: TT Quarantine Symbol Hardening And Static Gap Smoke Runner

Generated: `2026-07-08T00:45:18+00:00`

## Summary

- Work is local-only and private.
- This checkpoint hardens the two owner symbols that were schematic in 4747.
- TT result:

```text
D_TT[U]^nu = P_loc nabla_mu Pi_TT[U]^{mu nu}
sigma_TT^dagger(p)xi_ab = -i Pi_TT^*(p)_ab^{mu nu} p_mu P_loc^*(p) xi_nu
p_mu Pi_TT(p)^{mu nu}_ab = 0 for exact transverse TT
=> c_TT=0 for exact TT divergence
```

- Therefore TT is not a positive static gap source in the exact-TT route; it must be topological/superpotential or carried as `C_TT_kernel`.
- Quarantine result:

```text
D_quar[K,q]^nu = q_tr^nu + nabla_mu K_own^{mu nu}
sigma_quar,K^dagger(p)chi_mu_nu = -i p_mu chi_nu
sigma_quar,q^dagger(p)chi_nu = chi_nu
```

- Therefore quarantine is the better coercive candidate if the `q_tr/K_own` parent map is nondegenerate.
- A canonical static gap smoke runner is added, but it is explicitly nonclaim.

## TT Symbol Hardening

- `TT4748_0_parent_operator`: D_TT[U]^nu := P_loc nabla_mu Pi_TT[U]^{mu nu}
- `TT4748_1_adjoint_symbol`: sigma_TT^dagger(p)xi_ab = -i Pi_TT^*(p)_{ab}^{mu nu} p_mu P_loc^*(p) xi_nu
- `TT4748_2_exact_TT_transversality`: p_mu Pi_TT(p)^{mu nu}_{ab}=0 for an exact transverse TT projector
- `TT4748_3_gap_consequence`: c_TT=0 for exact transverse TT-divergence owner unless parent uses nonexact/weighted TT map
- `TT4748_4_owner_role`: TT owner must be boundary/topological/superpotential kernel or carried as C_TT_kernel
- `TT4748_5_projector_blocker`: sigma(Pi_TT), sigma(P_loc), boundary behavior and nonlocal projector order remain parent inputs

## Quarantine Symbol Hardening

- `QUAR4748_0_parent_operator`: D_quar[K,q]^nu := q_tr^nu + nabla_mu K_own^{mu nu}
- `QUAR4748_1_adjoint_symbol_K`: sigma_quar,K^dagger(p)chi_{mu nu} = -i p_mu chi_nu
- `QUAR4748_2_adjoint_symbol_q`: sigma_quar,q^dagger(p)chi_nu = chi_nu
- `QUAR4748_3_coercivity_candidate`: ||sigma_quar^dagger(p)chi||^2 >= (w_q^2 + w_K^2 |p|_h^2)||chi||^2 minus map-kernel leakage
- `QUAR4748_4_blocker`: if q_tr is derived with a kernel or K_own has gauge-null directions, carry C_quar_kernel
- `QUAR4748_5_static_constant`: c_quar >= inf(w_q^2 + w_K^2 |p|_h^2) - C_quar_kernel

## DN Constant Update

- `DNU4748_0_previous`: c_DN >= min(c_TFRI,c_TT,c_quar)-C_mix
- `DNU4748_1_TT_revision`: exact TT divergence gives c_TT=0 and should be projected into C_TT_kernel/topological sector
- `DNU4748_2_effective_gap`: c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel
- `DNU4748_3_live_blockers`: numeric c_DN_eff needs c_TFRI,c_quar,C_mix_eff,C_TT_kernel and boundary complementing data
- `DNU4748_4_claim_gate`: claim requires C_TT_kernel=0 or sourced below threshold plus c_DN_eff>0

## Static Gap Smoke Runner

- `SMOKE4748_0_live_missing`: FAIL_CLOSED
- `SMOKE4748_1_canonical_pipeline`: PIPELINE_PASS_NONCLAIM
- `SMOKE4748_2_TT_gap_rejected`: REJECTED_AS_GAP_SOURCE

## Static Score Gate

- `SSG4748_0_TT`: closed_until_kernel_contract
- `SSG4748_1_quar`: closed_until_parent_map
- `SSG4748_2_smoke`: nonclaim_pipeline_only
- `SSG4748_3_static_score`: closed_missing_sources
- `SSG4748_4_lorentzian`: separate_route

## Route Matrix

- `ROUTE4748_0_quarantine_source`: derive/source q_tr and K_own parent maps to prove c_quar>0
- `ROUTE4748_1_TT_topological`: write TT topological/superpotential kernel contract with C_TT_kernel=0 or bound
- `ROUTE4748_2_static_gap_numeric`: replace smoke constants with sourced L_loc,C_P,c_TFRI,c_quar,Pi_owner
- `ROUTE4748_3_claim_now`: claim local static/PPN pass

## Promotion Gates

- `GATE4748_0_sources`: pass_internal
- `GATE4748_1_TT_hardening`: conditional_pass
- `GATE4748_2_quar_hardening`: conditional_pass
- `GATE4748_3_smoke`: conditional_pass_nonclaim
- `GATE4748_4_numeric_gap`: closed_unsigned
- `GATE4748_5_static_score`: closed_unsigned
- `GATE4748_6_no_claim`: closed_firewall

## Decision

`TT_DIVERGENCE_SYMBOL_HARDENED_AS_KERNEL_TOPOLOGICAL_NOT_GAP_SOURCE_QUARANTINE_SYMBOL_COERCIVE_CANDIDATE_STATIC_SMOKE_NONCLAIM`

## Next Target

`4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md`
