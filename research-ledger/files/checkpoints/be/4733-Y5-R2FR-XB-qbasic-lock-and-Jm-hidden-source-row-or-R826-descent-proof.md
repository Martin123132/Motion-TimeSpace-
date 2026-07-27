# 4733 - XB q-basic Lock and Jm Hidden Source Row or R826 Descent Proof

Generated: `2026-07-07T23:05:42+00:00`

## Purpose

4733 attacks the narrow proof left by 4732: if `X_B` is fixed/q-basic, then `R_826(q;X_B)` descends and the hidden branch force disappears.

## What Actually Moved

- The exact descent law is now explicit: for vertical `v`, `D_v R_826(q;X_B)=R_826,XB D_v X_B`.
- Therefore `R_826` descent is exact if `D_v X_B=0`.
- Existing `X_B` work gives a disciplined, anti-retuning candidate bundle, but not a parent q-basic theorem.
- The fallback is now sharper: `|J_m_hidden| <= L_R826_XB V_XB + C_I826 V_I + C_grad826 V_gradI + C_marker826 V_marker + C_rad826 V_rad + C_boundary826 V_boundary`.

## X_B Lock Theorem

- `XBT4733_0_target`: TARGET_SHARP
- `XBT4733_1_exact_chain_rule`: EXACT_DERIVED_CHAIN_RULE
- `XBT4733_2_qbasic_sufficient_clause`: EXACT_IF_PARENT_QBASIC
- `XBT4733_3_current_evidence`: CANDIDATE_GATE_TESTED_NOT_PARENT_DERIVED
- `XBT4733_4_Lcg_gap`: LCG_QBASIC_UNSIGNED
- `XBT4733_5_transition_gap`: TRANSITION_QCURRENT_UNSIGNED
- `XBT4733_6_verdict`: XB_LOCK_NOT_PROMOTED_SOURCE_ROW_REQUIRED

## X_B Component Audit

- `XBC4733_0_A_curv`: LCG_AND_CURVATURE_OWNER_UNSIGNED
- `XBC4733_1_E_theta`: THETA_FRAME_OWNER_UNSIGNED
- `XBC4733_2_I_mat`: MATTER_SMOOTHING_FLOOR_UNSIGNED
- `XBC4733_3_I_rot_shear`: FLOW_FRAME_OWNER_UNSIGNED
- `XBC4733_4_I_grad_Bgrad_dotB`: TRANSITION_GRADIENT_GATE_UNSIGNED
- `XBC4733_5_Lcg`: LCG_PARENT_THEOREM_NOT_DERIVED
- `XBC4733_6_trace_suppression`: TRACE_CLOSURE_NOT_PARENT_DERIVED
- `XBC4733_7_verdict`: V_XB_RETAINED

## R826 Descent Rows

- `RDX4733_0_descent_formula`: EXACT_CHAIN_RULE
- `RDX4733_1_zero_case`: EXACT_IF_XB_LOCK_SIGNED
- `RDX4733_2_bound_case`: BOUND_FORMULA_DERIVED_VALUES_MISSING
- `RDX4733_3_euler_insert`: JM_HIDDEN_INSERT_WRITTEN
- `RDX4733_4_B826_insert`: B826_BOUND_INSERT_NONCLAIM

## Jm Hidden Source Row

- `JMH4733_0_master`: MISSING_COMPONENT_VALUES
- `JMH4733_1_VXB`: MISSING_VXB_ZERO_OR_VALUE
- `JMH4733_2_LR826XB`: MISSING_LR826XB_VALUE
- `JMH4733_3_CI826_VI`: MISSING_CI826_OR_VI_VALUE
- `JMH4733_4_transition_tail`: MISSING_TRANSITION_TAIL_BOUND
- `JMH4733_5_units_domain`: MISSING_UNITS_DOMAIN_SOURCE_PATHS
- `JMH4733_6_acceptance`: FALSE_NOW

## Gates

- `GATE4733_0_sources_verified`: NONE
- `GATE4733_1_chain_rule_derived`: STRUCTURE_ONLY_NOT_CLAIM
- `GATE4733_2_XB_parent_qbasic_signed`: XB_PARENT_LOCK_UNSIGNED
- `GATE4733_3_Lcg_parent_owned`: LCG_PARENT_THEOREM_MISSING
- `GATE4733_4_transition_current_closed`: TRANSITION_CURRENT_UNSIGNED
- `GATE4733_5_Jm_hidden_sourced`: JMHIDDEN_VALUES_MISSING
- `GATE4733_6_B826_claim_ready`: B826_NONCLAIM

## Decision

`XB_QBASIC_R826_DESCENT_EXACT_CONDITIONAL_XB_PARENT_LOCK_UNSIGNED_VXB_JMHIDDEN_SOURCE_ROW_CREATED_NONCLAIM`

## Next Target

`4734-Y5-R2FR-VXB-source-amplitude-and-R826-XB-Lipschitz-row-or-parent-qbasic-proof.md`
