# 4750 Y5 R2FR: q_tr Parent-Rank Test And Cquar/CTT Source Runner

Generated: `2026-07-08T00:59:02+00:00`

## Purpose

4750 turns the 4749 coupling result into an executable source runner. The live branch remains blocked because no parent-owned numeric rows for `J_q`, `J_K`, `s_min(J_q)`, `C_quar_kernel`, or `C_TT_kernel` have been sourced yet. The canonical rows are smoke tests only.

## Core Test

The parent quarantine operator is:

```text
D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{mu nu}.
```

The static symbol lower bound is:

```text
c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel.
```

The short route is:

```text
rank(J_q)=dim(chi) and s_q=s_min(J_q)>0 => c_quar >= s_q^2 - C_quar_kernel.
```

## Source Schema

- `QTRSCHEMA4750_0_Jq`: J_q
- `QTRSCHEMA4750_1_rankJq`: rank(J_q)
- `QTRSCHEMA4750_2_sminJq`: s_min(J_q)
- `QTRSCHEMA4750_3_JK`: J_K
- `QTRSCHEMA4750_4_sminJK`: s_min(J_K)
- `QTRSCHEMA4750_5_penalties`: C_cross,C_quar_kernel
- `QTRSCHEMA4750_6_TT`: C_TT_kernel
- `QTRSCHEMA4750_7_static`: C_P,L_loc,Pi_owner

## Cquar Runner

- `CQUAR4750_0_live_fail_closed`: FAIL_CLOSED_MISSING_PARENT_INPUTS
- `CQUAR4750_1_algebraic_rule`: RULE_READY_SOURCE_MISSING
- `CQUAR4750_2_algebraic_shortcut`: RULE_READY_SOURCE_MISSING
- `CQUAR4750_3_canonical_smoke`: PIPELINE_PASS_NONCLAIM

## CTT Runner

- `CTT4750_0_live_fail_closed`: FAIL_CLOSED_MISSING_TT_PROJECTOR_AND_BOUNDARY_INPUTS
- `CTT4750_1_zero_condition`: ZERO_RULE_READY_SOURCE_MISSING
- `CTT4750_2_finite_bound_rule`: BOUND_RULE_READY_SOURCE_MISSING
- `CTT4750_3_canonical_zero_smoke`: PIPELINE_PASS_NONCLAIM

## Static Gap Score Runner

- `STATIC4750_0_live_fail_closed`: FAIL_CLOSED_MISSING_STATIC_ARENA_INPUTS
- `STATIC4750_1_canonical_gap_smoke`: PIPELINE_PASS_NONCLAIM
- `STATIC4750_2_promotion_rule`: RULE_READY_SOURCE_MISSING

## Promotion Gates

- `GATE4750_0_parent_Jq`: BLOCKED_MISSING_PARENT_MAP
- `GATE4750_1_Cquar`: BLOCKED_MISSING_PENALTY_BOUNDS
- `GATE4750_2_CTT`: BLOCKED_MISSING_TT_CERTIFICATE
- `GATE4750_3_static`: BLOCKED_MISSING_STATIC_ARENA_INPUTS
- `GATE4750_4_claim`: FAIL_CLOSED_NONCLAIM

## Route Matrix

- `ROUTE4750_0_Jq_rank_source`: Source parent J_q, rank(J_q), and s_min(J_q)
- `ROUTE4750_1_TT_zero_source`: Source parent Pi_TT/P_loc and boundary/readout silence
- `ROUTE4750_2_static_numeric_smoke`: Run real static gap score after source rows exist

## Decision

`QTR_PARENT_RANK_RUNNER_AND_CQUAR_CTT_SOURCE_ROWS_STAGED_FAIL_CLOSED_NONCLAIM`

## Next Target

`4751-Y5-R2FR-qtr-map-source-search-or-static-gap-numeric-smoke.md`
