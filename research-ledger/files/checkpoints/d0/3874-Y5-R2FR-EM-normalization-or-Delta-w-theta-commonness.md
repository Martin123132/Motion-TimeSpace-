# 3874 — EM Normalization or Delta-w Theta Commonness

Generated: `2026-07-01T06:39:05+00:00`

## Result

3874 makes the key EM/source-coupling split:

`Write the effective observed Maxwell block as Z_Q_eff = Z_cal[1+deltaZ_act(X,A,readout)] and g_J_eff = g_cal[1+deltag_act(X,A,readout)]. A universal q-basic constant Z_cal/g_cal is an absolute calibration debt, not a local source-coupling residual; local WEP/R10/clock/PPN/source tests only see active non-common pieces: vertical derivatives, material/source dependence, hidden-visible F2 maps, radiative/readout regeneration, and current-normalization mismatch.`

So the stationary local source envelope after 3873 becomes:

`B_EM_scale_stationary_active <= b_Z_active + b_J + |b_alpha_active| + |C_XF2_active| + |C_JQ| + |Delta_M_EM_binding| + |C_EM_readout|`

This is a forward move because a universal calibrated `alpha/mu0` is no longer treated as an active local failure. The theory still cannot claim local GR/Maxwell source closure because the active pieces remain unsigned.

## Source Register

Resolved `20/20` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3874_00_3873_next | source-intake\mts_residuals\P8_Y5_R2FR_3873_NEXT_TARGET.csv | True | 3873 selected EM normalization/Delta_w target |
| SRC3874_01_3873_update | source-intake\mts_residuals\P8_Y5_R2FR_3873_PHI_EM_BOUNDARY_COEFFICIENT_UPDATE.csv | True | stationary EM envelope after Poynting zero |
| SRC3874_02_3873_retained | source-intake\mts_residuals\P8_Y5_R2FR_3873_RETAINED_EM_SOURCE_RESIDUALS.csv | True | retained EM source residuals |
| SRC3874_03_3865_image | source-intake\mts_residuals\P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv | True | visible operator image theorem |
| SRC3874_04_3865_joint | source-intake\mts_residuals\P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv | True | s_XF2/z_g/b_alpha joint identity |
| SRC3874_05_3864_f2 | source-intake\mts_residuals\P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv | True | constant lambda guard |
| SRC3874_06_3864_audit | source-intake\mts_residuals\P8_Y5_R2FR_3864_OPERATOR_DOMAIN_AUDIT.csv | True | operator-domain audit constant lambda |
| SRC3874_07_3864_lambda | source-intake\mts_residuals\P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv | True | active F2 residual bound |
| SRC3874_08_3863_mno | source-intake\mts_residuals\P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv | True | Maxwell normalization theorem |
| SRC3874_09_3863_em | source-intake\mts_residuals\P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv | True | EM source-scale envelope |
| SRC3874_10_3863_charge | source-intake\mts_residuals\P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv | True | unique F2/current slot audit |
| SRC3874_11_3809_mn | source-intake\mts_residuals\P8_Y5_R2FR_3809_MAXWELL_NORMALIZATION_THEOREM.csv | True | absolute alpha versus local drift split |
| SRC3874_12_3791_zem | source-intake\mts_residuals\P8_Y5_R2FR_3791_ZEM_FIXED_NORMALIZATION_THEOREM.csv | True | Z_EM normalization/readout guard |
| SRC3874_13_3791_guard | source-intake\mts_residuals\P8_Y5_R2FR_3791_OPERATOR_BASIS_COUNTEREXAMPLE_GUARD.csv | True | operator counterexample guard |
| SRC3874_14_1057_ct | source-intake\mts_residuals\P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv | True | F2 counterterm ledger |
| SRC3874_15_765_mki | source-intake\mts_residuals\P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv | True | Maxwell kinetic inheritance gate |
| SRC3874_16_3528_status | source-intake\mts_residuals\P8_EM_unique_F2_or_calibrated_alpha_status.csv | True | calibrated alpha local branch |
| SRC3874_17_3464_alpha | source-intake\mts_residuals\P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv | True | EM action normalization proof verdict |
| SRC3874_18_3465_owner | source-intake\mts_residuals\P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv | True | EM owner package audit verdict |
| SRC3874_19_3503_bound | source-intake\mts_residuals\P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv | True | EM Hodge/Maxwell/current owner bound vector |

## EM Normalization Split Theorem

| theorem_id | piece | statement | status |
| --- | --- | --- | --- |
| ENS3874_0_rescaling_class | Maxwell normalization convention class | A_Q -> s A_Q moves normalization between F_Q^2 and A_Q.J_Q, so bare Z_Q/w_EM is not physical until charge-current convention is fixed. | EXACT_CONVENTION_GUARD |
| ENS3874_1_calibration_split | constant calibration split | Write the effective observed Maxwell block as Z_Q_eff = Z_cal[1+deltaZ_act(X,A,readout)] and g_J_eff = g_cal[1+deltag_act(X,A,readout)]. A universal q-basic constant Z_cal/g_cal is an absolute calibration debt, not a local source-coupling residual; local WEP/R10/clock/PPN/source tests only see active non-common pieces: vertical derivatives, material/source dependence, hidden-visible F2 maps, radiative/readout regeneration, and current-normalization mismatch. | EXACT_LOCAL_VS_ABSOLUTE_SPLIT |
| ENS3874_2_active_identity | active alpha-current-F2 identity | b_alpha_active = 2 z_g_active - s_XF2_active | EXACT_ACTIVE_LINEAR_IDENTITY |
| ENS3874_3_parent_zero_route | parent image zero route | If visible coefficient image/fullness, no hidden-visible Hom, radiative/readout image stability, fixed T_Q norm, and same-current owner all hold, then s_XF2_active=z_g_active=b_alpha_active=C_XF2_active=C_JQ=0. | EXACT_CONDITIONAL_ZERO_ROUTE |
| ENS3874_4_calibrated_branch | calibrated local Maxwell branch | If the parent zero route is unsigned, use measured alpha/mu0 as universal calibration and retain only active residual rows for local tests. | CALIBRATED_BRANCH_ALLOWED_NONCLAIM |
| ENS3874_5_scope_guard | not a proof of absolute constants | The split does not derive alpha, mu0, charge quantum, or Newton G; it only classifies what can affect local source coupling after calibration. | SCOPE_GUARD |

## Active Residual Definition

| residual_id | quantity | definition | classification |
| --- | --- | --- | --- |
| AR3874_0_Z_cal | Z_cal | universal q-basic Maxwell calibration constant | CALIBRATION_NOT_LOCAL_RESIDUAL |
| AR3874_1_lambda0 | lambda_0 F_Q^2 | constant hidden-independent F2 coefficient | CONSTANT_NOT_LOCAL_RESIDUAL |
| AR3874_2_sXF2_active | s_XF2_active | D_X ln lambda_active or non-common F2 coefficient derivative | ACTIVE_RESIDUAL |
| AR3874_3_zg_active | z_g_active | D_X ln g_J_eff active current normalization | ACTIVE_RESIDUAL |
| AR3874_4_balpha_active | b_alpha_active | 2 z_g_active - s_XF2_active | ACTIVE_RESIDUAL_IDENTITY |
| AR3874_5_CXF2_active | C_XF2_active | hidden-visible or motion/time coefficient multiplying F^2 | ACTIVE_OPERATOR_RESIDUAL |
| AR3874_6_CJQ | C_JQ | charge/current convention mismatch after calibration | ACTIVE_CURRENT_RESIDUAL |
| AR3874_7_CEM_readout | C_EM_readout | apparatus/loop/readout regenerated F2 or alpha response | ACTIVE_READOUT_RESIDUAL |

## Stationary Source Envelope Update

| update_id | target | formula | status |
| --- | --- | --- | --- |
| EUP3874_0_previous | B_EM_scale_stationary | B_EM_scale_stationary <= b_Z+b_J+\|b_alpha\|+\|w_EM\|+\|C_XF2\|+\|C_JQ\|+\|Delta_M_EM_binding\| | PREVIOUS_MIXED_FORM |
| EUP3874_1_active | B_EM_scale_stationary_active | B_EM_scale_stationary_active <= b_Z_active + b_J + \|b_alpha_active\| + \|C_XF2_active\| + \|C_JQ\| + \|Delta_M_EM_binding\| + \|C_EM_readout\| | REFINED_ACTIVE_SOURCE_ENVELOPE |
| EUP3874_2_parent_zero | B_EM_scale_stationary_active | if parent image + fixed norm + same-current + readout stability + EM binding once-only all close, then B_EM_scale_stationary_active -> \|Delta_M_EM_binding_once_residual\| | EXACT_CONDITIONAL_REDUCTION |
| EUP3874_3_no_claim | local_GR_EM_source | no local-GR claim until active residuals or binding/source accounting are zeroed/bounded on the same arena domain | NONCLAIM_GATE |

## Branch Decision Table

| branch_id | branch | condition | consequence | status |
| --- | --- | --- | --- | --- |
| BRD3874_0_derived_parent | derived-parent EM branch | parent image/fullness + fixed T_Q norm + same-current + readout stability | sets active EM normalization residuals to zero | BEST_BUT_UNSIGNED |
| BRD3874_1_calibrated_local | calibrated local Maxwell branch | measured alpha/mu0 are universal q-basic inputs; retain active residuals only | lets local GR reduction proceed without absolute-alpha overclaim | DEFAULT_WORKING_BRANCH |
| BRD3874_2_active_bound | finite active-residual branch | use clock/WEP/R10/PPN/orbital source rows for s_XF2_active,z_g_active,C_XF2_active,CJQ | empirical robustness path if theorem route stalls | BOUND_BRANCH_READY |
| BRD3874_3_reject_shortcut | reject alpha-only shortcut | b_alpha_active=2z_g_active-s_XF2_active | alpha data cannot bound F2 unless z_g/current normalization is also zeroed or bounded | GUARD_ACTIVE |

## Claim Gates

| gate_id | status | detail | claim_allowed |
| --- | --- | --- | --- |
| G3874_0_sources | PASS | 20/20 sources resolved | False |
| G3874_1_split | PASS | constant calibration removed from local residual scoring | False |
| G3874_2_active_identity | PASS | b_alpha_active = 2 z_g_active - s_XF2_active | False |
| G3874_3_residual_basis | PASS | C_EM_readout,C_JQ,C_XF2_active,Z_cal,b_alpha_active,lambda_0 F_Q^2,s_XF2_active,z_g_active | False |
| G3874_4_envelope | PASS | B_EM_scale_stationary_active <= b_Z_active + b_J + \|b_alpha_active\| + \|C_XF2_active\| + \|C_JQ\| + \|Delta_M_EM_binding\| + \|C_EM_readout\| | False |
| G3874_5_default_branch | PASS | calibrated branch | False |
| G3874_6_no_claim | PASS | valid_for_claim=false throughout | False |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3874_0 | 3875-Y5-R2FR-CJQ-current-owner-or-active-residual-runner.md | attack the current-normalization leg C_JQ/z_g_active, because alpha/F2 bounds cannot isolate Maxwell normalization until the same-current owner is zeroed or numerically bounded | 3874 split off universal calibration; the largest remaining degeneracy is z_g/C_JQ in b_alpha_active=2 z_g_active-s_XF2_active |

## Bottom Line

3874 is useful because it stops us wasting effort on the wrong thing. A common calibrated Maxwell constant is allowed as local input; the local-GR threat is the active residual vector `s_XF2_active`, `z_g_active`, `C_XF2_active`, `C_JQ`, `C_EM_readout`, and EM binding/source accounting. The next best move is `C_JQ/z_g_active`: without same-current/current-normalization closure, alpha data cannot isolate the F2 coefficient.
