# 3680 - z_g current owner or alpha bound route for s_XF2

**Status:** ZG_ZERO_NOT_PROVED_TWO_KNOB_ALPHA_SOURCE_ROUTE_FORMALIZED_NONCLAIM

This checkpoint bridges the older current-owner work into the new `s_XF2` throat. The result is not `z_g=0`; the result is a sharper object: `z_g` is now a component vector, and alpha data is a two-knob constraint.

## Main result

`z_g = D_Xhat ln g_J` is **not proven zero**.

The exact identity remains:

`b_alpha_X = 2 z_g - s_XF2`.

So clock/WEP/R10 alpha evidence cannot be used as direct `s_XF2` evidence until either `z_g=0` is parent-signed or `z_g` is separately bounded.

The direct current leg is decomposed as:

`z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A`.

For source arenas the extension is:

`z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A`.

## z_g zero audit
- `ZG3680_0_target`: TARGET_NOT_PROVED - z_g=0 current-normalization theorem -> would make s_XF2=-b_alpha_X and let alpha/clock/WEP routes hit the Maxwell kinetic residual directly
- `ZG3680_1_compact_lattice`: PARTIAL_SUPPORT_ONLY - fixed representation charge labels -> compact U(1) helps with relative labels but not the continuous current unit or Maxwell kinetic normalization
- `ZG3680_2_noether_current_owner`: EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED - same Noether current owner -> Ward/Noether conservation can define the current form, but not the calibration amplitude unless owner/readout clauses sign
- `ZG3680_3_post_current_rescale`: KILLED_CONDITIONALLY_NOT_PARENT_SIGNED - post-variation c_A current rescale -> 1815/1816 narrow this loophole but do not close it for the current corpus
- `ZG3680_4_pre_action_weight`: SURVIVES_CURRENT_OWNER - pre-variation action/source weight -> this is mostly a source/WEP/Newton coupling leg, not a direct alpha spectroscopy leg, but it blocks source-calibration claims
- `ZG3680_5_readout_worldtube_transfer`: MISSING_ARENA_TRANSFER_KERNEL - source/readout/worldtube transfer -> arena data can otherwise see a different current than the parent variation current
- `ZG3680_6_ward_limit`: CONSERVATION_NOT_CALIBRATION - Ward identity alone -> conservation survives current rescaling and does not fix alpha/current normalization by itself
- `ZG3680_7_verdict`: THEOREM_NOT_PROVED_RETAIN_TWO_KNOB_ROUTE - current corpus proves z_g=0 -> z_g=0 is not claimed; b_alpha_X=2 z_g-s_XF2 must remain a two-knob identity

## Component decomposition
- `ZGD3680_0_definition`: MISSING_ZERO_OR_NUMERIC_BOUND - `z_g = D_Xhat ln g_J`
- `ZGD3680_1_core_decomposition`: NO_CANCELLATION_COMPONENTS_UNFILLED - `z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A`
- `ZGD3680_2_lattice_term`: PARTIAL_ZERO_ONLY_IF_TQ_LATTICE_SIGNED - `z_lattice,A = D_Xhat ln n_A`
- `ZGD3680_3_noether_term`: MISSING_PARENT_CURRENT_OWNER_OR_BOUND - `z_Noether,A = D_Xhat ln Z_JA`
- `ZGD3680_4_post_current_term`: MISSING_READOUT_ORDER_THEOREM_OR_C_A_BOUND - `z_cA_post,A = D_Xhat ln c_A`
- `ZGD3680_5_readout_term`: MISSING_READOUT_TRANSFER_KERNEL_OR_BOUND - `z_readout,A = D_Xhat ln R_A`
- `ZGD3680_6_source_arena_extension`: SOURCE_ARENA_EXTENSION_LIVE - `z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A`
- `ZGD3680_7_two_knob_identity`: DERIVED_IDENTITY_RETAINED - `b_alpha_X = 2 z_g - s_XF2`

## Two-knob bound route
- `TKB3680_0_identity`: DERIVED_IDENTITY_NONCLAIM - `b_alpha_X` -> `b_alpha_X = 2 z_g - s_XF2`; not a bound
- `TKB3680_1_sXF2_budget_O1`: PRIVATE_TARGET_NOT_EVIDENCE - `abs(s_XF2)` -> `3.724015406785e-06`; target budget only
- `TKB3680_2_sXF2_budget_4pi`: PRIVATE_TARGET_NOT_EVIDENCE - `abs(s_XF2)` -> `2.963477300701e-07`; target budget only
- `TKB3680_3_clock_product`: SOURCE_BACKED_PRODUCT_NOT_STANDALONE_COEFFICIENT - `abs((2 z_g - s_XF2) * tau_clock)` -> `2.100000000000e-18`; requires tau_clock and shared Xhat normalization before scoring z_g/s_XF2
- `TKB3680_4_clock_if_tau_known`: FORMULA_READY_INPUTS_MISSING - `abs(2 z_g - s_XF2)` -> `B_clock/abs(tau_clock)`; not score-ready until tau_clock is sourced
- `TKB3680_5_direct_if_zg_zero`: CONDITIONAL_ON_ZG_ZERO_AND_TAU_CLOCK - `abs(s_XF2)` -> `B_clock/abs(tau_clock)`; this is the clean win route, but both inputs are missing
- `TKB3680_6_if_zg_bounded`: FORMULA_READY_INPUTS_MISSING - `abs(s_XF2)` -> `B_alpha + 2*B_zg`; keeps the current-normalization ambiguity explicit
- `TKB3680_7_wep_alpha_projection`: SOURCE_BACKED_TARGET_NOT_MTS_PREDICTION - `abs(P_WEP_alpha)` -> `4.797780522732e-05`; requires beta_source_alpha, tau_WEP and material/source map
- `TKB3680_8_dd_alpha_threshold`: SOURCE_BACKED_THRESHOLD_NO_MTS_COEFFICIENT - `abs(c_alpha_DD or b_alpha)` -> `8.320244933244e-10`; requires a parent-owned c_alpha or theorem-zero

## Source arena transfer
- `SAR3680_0_clock`: MISSING_TAU_CLOCK_XHAT - clock/spectroscopy sees `b_alpha_X = 2 z_g - s_XF2` and needs tau_clock
- `SAR3680_1_wep`: MISSING_BETA_SOURCE_ALPHA_AND_MATERIAL_MAP - MICROSCOPE/WEP sees `beta_source_alpha,A*(2 z_g - s_XF2) plus z_source,A tails` and needs tau_WEP/material tensor/source map
- `SAR3680_2_r10`: MISSING_R10_ALPHA_SOURCE_PROJECTION - R10/short-range sees `K_X Qbar_XH qbar_XT with alpha/source component rows` and needs tau_R10/lambda_X/source profile
- `SAR3680_3_ppn_newton`: MISSING_SOURCE_UNIVERSALITY_VECTOR - PPN/Newton/source calibration sees `z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A` and needs source-worldtube/GM calibration/PPN source vector

## Decisions
- `DEC3680_0_zg_zero`: THEOREM_NOT_PROVED - z_g=0 is not derived -> keep z_g live in b_alpha_X=2 z_g-s_XF2
- `DEC3680_1_real_progress`: PROMOTED_TO_COMPONENT_VECTOR - z_g is no longer vague -> target components rather than restating the coupling problem
- `DEC3680_2_best_derivation_route`: DERIVATION_FIRST - variation-before-readout/order is the nearest derivation lever -> attack post-current c_A/readout order or import a bound row
- `DEC3680_3_best_empirical_route`: BOUND_ROUTE_READY_NOT_SCORE_READY - alpha data must be used as a two-knob bound -> build two-knob runner only after tau_clock/tau_WEP or z_g bound exists
- `DEC3680_4_claim_discipline`: PRIVATE_NONCLAIM - no local-GR/Maxwell/WEP/R10 claim -> continue privately

## Claim gates
- `CG3680_0_zg_zero`: BLOCKED_NONCLAIM - claim z_g=0 because current owner, readout order, no source slot and source transfer are not parent-signed
- `CG3680_1_direct_sXF2_alpha`: BLOCKED_ZG_LIVE - treat alpha/clock as direct s_XF2 bound because b_alpha_X=2 z_g-s_XF2 remains two-knob
- `CG3680_2_score_two_knob`: BLOCKED_PROJECTIONS_MISSING - score z_g/s_XF2 two-knob runner because tau_clock, tau_WEP, beta_source_alpha and arena source maps are missing
- `CG3680_3_source_universality`: BLOCKED_SOURCE_WEIGHTS - claim source-current universality/Newton source calibration because pre-action weights, worldtube transfer and non-Hilbert bypass remain open
- `CG3680_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private derivation checkpoint only

## Next target
`3681-Y5-R2FR-post-current-cA-readout-order-zero-or-zg-component-bound.md` via `scripts/Y5_R2FR_3681_post_current_cA_readout_order_zero_or_zg_component_bound.py`.

## Sources
- `handoff_3679`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3679_NEXT_TARGET.csv` exists=True needle_found=True
- `map_3679`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv` exists=True needle_found=True
- `bounds_3679`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv` exists=True needle_found=True
- `gate_3507`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3507_PARENT_OWNER_GATE.csv` exists=True needle_found=True
- `source_theorem_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_SOURCE_CURRENT_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `source_audit_3650`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3650_CHARGE_CURRENT_CLAUSE_AUDIT.csv` exists=True needle_found=True
- `current_theorem_1814`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv` exists=True needle_found=True
- `current_audit_1814`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1814_CURRENT_OWNER_AUDIT.csv` exists=True needle_found=True
- `no_rescale_1815`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv` exists=True needle_found=True
- `post_pre_1815`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1815_POST_PRE_RESCALE_SPLIT_AUDIT.csv` exists=True needle_found=True
- `readout_order_1816`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv` exists=True needle_found=True
- `selector_order_1816`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1816_SOURCE_SELECTOR_ORDER_AUDIT.csv` exists=True needle_found=True
- `tq_1100`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1100_TQ_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `ward_1101`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv` exists=True needle_found=True
- `alpha_clock_1052`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv` exists=True needle_found=True
- `alpha_wep_1052`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv` exists=True needle_found=True
- `alpha_req_1098`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv` exists=True needle_found=True
- `alpha_source_runner_3508`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_alpha_source_bound_runner_results.csv` exists=True needle_found=True
