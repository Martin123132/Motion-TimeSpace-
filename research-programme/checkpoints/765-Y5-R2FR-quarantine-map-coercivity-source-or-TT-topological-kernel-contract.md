# 4749 Y5 R2FR: Quarantine Map Coercivity Source Or TT Topological Kernel Contract

Generated: `2026-07-08T00:50:51+00:00`

## Summary

- Work is local-only and private.
- This checkpoint turns the quarantine coupling candidate into a rank/singular-value test.
- Parent quarantine map:

```text
X_quar=(X_q,X_K)
q_tr = J_q X_q
K_own = J_K X_K
D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{mu nu}
sigma_quar^dagger(p)chi = (J_q^dagger chi, -i p_mu J_K^dagger chi)
```

- Coercivity route:

```text
if s_q=s_min(J_q)>0:
  ||sigma_quar^dagger(p)chi||^2 >= s_q^2 ||chi||^2

c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel
```

- TT route:

```text
exact TT divergence => c_TT=0
TT must be topological/superpotential or carried as C_TT_kernel
```

- No local-GR or local-test claim is made.

## Quarantine Map Contract

- `QMC4749_0_parent_fields`: X_quar=(X_q,X_K), q_tr=J_q X_q, K_own=J_K X_K
- `QMC4749_1_operator`: D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{mu nu}
- `QMC4749_2_static_symbol`: sigma_quar^dagger(p)chi = (J_q^dagger chi, -i p_mu J_K^dagger chi)
- `QMC4749_3_rank_condition`: rank(J_q)=dim(chi) or s_min(J_q)>0
- `QMC4749_4_kernel_condition`: ker(J_q^dagger) cap ker(p_mu J_K^dagger)=0 for every spatial p
- `QMC4749_5_nonclaim`: If J_q/J_K are not parent-owned, carry C_quar_kernel and do not score.

## Quarantine Rank / Coercivity Test

- `QRT4749_0_symbol_norm`: ||sigma_quar^dagger(p)chi||^2 = ||J_q^dagger chi||^2 + |p|_h^2||J_K^dagger chi||^2 + cross_terms
- `QRT4749_1_algebraic_lower`: if s_q:=s_min(J_q)>0 then ||sigma_quar^dagger(p)chi||^2 >= s_q^2||chi||^2
- `QRT4749_2_K_lower`: if s_K:=s_min(J_K)>0 then K channel adds |p|_h^2 s_K^2||chi||^2 for p!=0
- `QRT4749_3_combined_constant`: c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel
- `QRT4749_4_static_unit`: on unit spatial cotangent p_min=1, c_quar >= s_q^2+s_K^2-C_cross-C_quar_kernel
- `QRT4749_5_blocker`: numeric c_quar requires J_q,J_K,weights,cross terms and kernel projection sources

## TT Topological Kernel Contract

- `TTK4749_0_exact_TT_kernel`: p_mu Pi_TT(p)^{mu nu}_{ab}=0 => P_loc nabla_mu Pi_TT[U]^{mu nu}=0 in the exact static symbol
- `TTK4749_1_topological_owner`: S_TT must be boundary/topological/superpotential with zero bulk local metric response
- `TTK4749_2_zero_condition`: C_TT_kernel=0 if Pi_TT/P_loc are parent-fixed, transverse, no boundary/corner/readout leakage
- `TTK4749_3_bound_condition`: C_TT_kernel <= C_nonTT + C_projector + C_boundary_TT + C_readout_TT
- `TTK4749_4_forbidden_route`: Do not set c_TT>0 for exact transverse TT divergence

## Updated Static Gap Bound

- `GAP4749_0_effective_DN`: c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel
- `GAP4749_1_quar_insert`: c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel
- `GAP4749_2_static_gap`: lambda_1^stat >= [min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)
- `GAP4749_3_residual`: C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2+(C_Dstat^2+C_boundary_stat) C_P L_loc^2 / c_DN_eff)
- `GAP4749_4_claim_gate`: score_ready only if c_DN_eff>0 and all constants/projections/kernel bounds are source-backed

## Source Value Ledger

- `SRCVAL4749_0_Jq`: J_q
- `SRCVAL4749_1_JK`: J_K
- `SRCVAL4749_2_sq`: s_q=s_min(J_q)
- `SRCVAL4749_3_sK`: s_K=s_min(J_K)
- `SRCVAL4749_4_Ccross`: C_cross
- `SRCVAL4749_5_Cquar`: C_quar_kernel
- `SRCVAL4749_6_CTT`: C_TT_kernel
- `SRCVAL4749_7_projectors`: Pi_TT/P_loc/Q_perp symbols
- `SRCVAL4749_8_static`: C_P,L_loc,Pi_owner,c_TFRI

## Route Matrix

- `ROUTE4749_0_qtr_rank`: source/prove J_q full-rank and s_q>0
- `ROUTE4749_1_TT_kernel`: source C_TT_kernel=0 or finite bound from topological/superpotential contract
- `ROUTE4749_2_K_channel`: source J_K and s_K to strengthen static nonzero-p gap
- `ROUTE4749_3_static_score`: score static PPN/R10 now

## Promotion Gates

- `GATE4749_0_sources`: pass_internal
- `GATE4749_1_quar_contract`: conditional_pass
- `GATE4749_2_rank_bound`: conditional_pass_nonclaim
- `GATE4749_3_TT_contract`: conditional_pass_nonclaim
- `GATE4749_4_missing_values`: closed_unsigned
- `GATE4749_5_score`: closed_unsigned
- `GATE4749_6_no_claim`: closed_firewall

## Decision

`QUARANTINE_COERCIVITY_REDUCED_TO_QTR_PARENT_RANK_SMIN_AND_KOWN_KERNEL_TT_TOPOLOGICAL_CONTRACT_STAGED_NONCLAIM`

## Next Target

`4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md`
