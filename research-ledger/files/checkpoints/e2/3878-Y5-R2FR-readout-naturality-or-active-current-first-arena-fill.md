# 3878 - Readout Naturality or Active-Current First Arena Fill

Generated: `2026-07-01T07:02:36+00:00`

## Result

3878 sharpens the 3877 `b_tail` object by splitting it into a common calibrated source scale and relative material/source tails:

`For every tail coefficient X_A in {R_A,c_A_pre,w_A,kappa_A,J_A_measure,K_arena,R_rad,A}, write X_A=X_* x_A with X_* common across ordinary matter and x_A relative. Then D_Xhat ln X_A = D_Xhat ln X_* + D_Xhat ln x_A. If x_A is q-basic/natural on a connected ordinary-matter/source category, the relative term vanishes; the common term is not a WEP/material source charge and may be absorbed into one calibrated G/source normalization only if it is derivative-silent in time, range, frame, arena and readout domain.`

The relative tail carried by composition/readout/source tests is:

`b_tail_rel,A := b_readout_rel,A + b_source_slot_rel,A + b_rad_rel,A`

The common branch is:

`z_tail_common := D_Xhat ln R_* + D_Xhat ln c_* + D_Xhat ln w_* + D_Xhat ln kappa_* + D_Xhat ln J_* + D_Xhat ln K_* + D_Xhat ln R_rad,*`

and it remains live unless:

`b_common_drift := |D_t ln C_*| + |D_r ln C_*| + |D_frame ln C_*| + |D_lambda ln C_*| + |Delta_domain(C_*)| = 0`

So the calibrated active-current runner becomes:

`|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_common_drift`

## Why This Matters

This prevents two bad moves at once. We do not falsely punish MTS for needing one calibrated coupling scale, because GR itself uses a calibrated `G_N`. But we also do not hide a drifting source normalization inside `G_N`; any time/range/frame/domain drift remains `b_common_drift`.

## Source Register

Resolved `29/29` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3878_00_3877_next | source-intake\mts_residuals\P8_Y5_R2FR_3877_NEXT_TARGET.csv | True | 3877 selected readout naturality or first arena fill |
| SRC3878_01_3877_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3877_TAIL_DECOMPOSITION_THEOREM.csv | True | tail zero theorem |
| SRC3878_02_3877_common_gap | source-intake\mts_residuals\P8_Y5_R2FR_3877_TAIL_OWNER_CLAUSE_AUDIT.csv | True | readout naturality clause |
| SRC3878_03_3877_arena_lock | source-intake\mts_residuals\P8_Y5_R2FR_3877_TAIL_OWNER_CLAUSE_AUDIT.csv | True | arena domain lock clause |
| SRC3878_04_3877_tail_contract | source-intake\mts_residuals\P8_Y5_R2FR_3877_READOUT_SOURCE_SLOT_RAD_TAIL_CONTRACT.csv | True | b_tail contract |
| SRC3878_05_3877_runner | source-intake\mts_residuals\P8_Y5_R2FR_3877_ACTIVE_RUNNER_FILL_ROWS.csv | True | b_tail active runner |
| SRC3878_06_3868_readout | source-intake\mts_residuals\P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv | True | readout kernel missing |
| SRC3878_07_3868_delta_w | source-intake\mts_residuals\P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv | True | source weight missing |
| SRC3878_08_3868_kernel | source-intake\mts_residuals\P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv | True | arena kernel missing |
| SRC3878_09_3867_projection | source-intake\mts_residuals\P8_Y5_R2FR_3867_SOURCE_BACKED_INPUT_SCHEMA.csv | True | projection consistency schema |
| SRC3878_10_3867_zg | source-intake\mts_residuals\P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv | True | z_g decomposition runner candidate |
| SRC3878_11_3509_source_domain | source-intake\mts_residuals\P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv | True | typed source-domain theorem |
| SRC3878_12_3509_connected | source-intake\mts_residuals\P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv | True | connected source weights collapse |
| SRC3878_13_3509_common | source-intake\mts_residuals\P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv | True | common scalar reclassification |
| SRC3878_14_3510_common_identity | source-intake\mts_residuals\P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv | True | common scale identity |
| SRC3878_15_3510_common_guard | source-intake\mts_residuals\P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv | True | common scale guard |
| SRC3878_16_3510_Newton | source-intake\mts_residuals\P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv | True | Newton-Poisson calibrated source chain |
| SRC3878_17_1230_naturality | source-intake\mts_residuals\P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv | True | connected naturality lemma |
| SRC3878_18_1230_absorb | source-intake\mts_residuals\P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv | True | common factor absorption |
| SRC3878_19_1230_measure | source-intake\mts_residuals\P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv | True | measure owner extension |
| SRC3878_20_1231_graph | source-intake\mts_residuals\P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv | True | interaction graph collapse |
| SRC3878_21_1231_forgetting | source-intake\mts_residuals\P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv | True | source label forgetting |
| SRC3878_22_1231_arena_wep | source-intake\mts_residuals\P8_Y5_R10_1231_ARENA_RESIDUAL_LAWS.csv | True | first arena residual law |
| SRC3878_23_3871_measure | source-intake\mts_residuals\P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv | True | measure Jacobian reentry |
| SRC3878_24_3872_total_bj | source-intake\mts_residuals\P8_Y5_R2FR_3872_FIRST_CANDIDATE_BJ_COEFFICIENT_ROWS.csv | True | executable b_J envelope |
| SRC3878_25_3873_poynting_zero | source-intake\mts_residuals\P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv | True | stationary Poynting boundary zero |
| SRC3878_26_3502_readout_rad | source-intake\mts_residuals\P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv | True | readout/radiative EM regeneration |
| SRC3878_27_3503_cem_readout | source-intake\mts_residuals\P8_Y5_R2FR_3503_EM_HODGE_CURRENT_BOUND_VECTOR.csv | True | C_EM_readout retained |
| SRC3878_28_1223_readout | source-intake\mts_residuals\P8_Y5_R10_1223_MINIMAL_PROOF_CONTRACTS.csv | True | effective/readout proof contract |

## Common-Mode Calibrated Tail Theorem

| theorem_id | piece | statement | status |
| --- | --- | --- | --- |
| CMT3878_0_split | common-relative tail split | For every tail coefficient X_A in {R_A,c_A_pre,w_A,kappa_A,J_A_measure,K_arena,R_rad,A}, write X_A=X_* x_A with X_* common across ordinary matter and x_A relative. Then D_Xhat ln X_A = D_Xhat ln X_* + D_Xhat ln x_A. If x_A is q-basic/natural on a connected ordinary-matter/source category, the relative term vanishes; the common term is not a WEP/material source charge and may be absorbed into one calibrated G/source normalization only if it is derivative-silent in time, range, frame, arena and readout domain. | EXACT_ALGEBRAIC_SPLIT |
| CMT3878_1_relative_zero | relative naturality route | If the relative factors x_A form a natural automorphism over a connected ordinary-matter/source category and source labels are quotient-forgotten before readout, D_Xhat ln x_A=0. | EXACT_CONDITIONAL_RELATIVE_ZERO |
| CMT3878_2_common_reclassification | common scale is not species poison | A common tail scale C_* cannot create WEP composition charge by itself; it renormalizes calibrated source coupling instead. | EXACT_RECLASSIFICATION |
| CMT3878_3_common_guard | common scale is not free magic | C_* is harmless only after one calibration if it is derivative-silent in time, range, frame, arena, and readout domain. | ANTI_BACKFILL_GUARD |
| CMT3878_4_Newton_payoff | Newton/GR connection | With fixed kappa_ref, fixed common source scale, and the same Hilbert source in the weak-field 00 equation, the Poisson coefficient is recovered as one calibrated coupling rather than a material-dependent patch. | EXACT_CONDITIONAL_NEWTON_CHAIN |
| CMT3878_5_verdict | 3878 status | The current branch cannot claim b_tail=0, but it has converted the active tail problem into relative material/source tails plus one common calibrated drift channel. | RUNNER_NARROWED_NONCLAIM |

## Domain-Lock Clause Audit

| clause_id | owner_clause | current_status | residual_if_missing |
| --- | --- | --- | --- |
| DLC3878_0_readout_common_factor | readout factors admit common-relative split | EXACT_IF_READOUT_FUNCTOR_SIGNED | b_readout_rel |
| DLC3878_1_source_weight_connectedness | source weights collapse by connected naturality | EXACT_CONDITIONAL_FROM_1230_1231 | D_X ln(w_A/w_*) |
| DLC3878_2_current_coefficient | pre-current coefficients share the same owner | CONDITIONAL_NOT_PARENT_SIGNED | D_X ln(c_A_pre/c_*) |
| DLC3878_3_selector | source selector has no material label | CONDITIONAL_NOT_PARENT_SIGNED | D_X ln(kappa_A/kappa_*) |
| DLC3878_4_measure | measure Jacobian species-blind | MISSING_MEASURE_DESCENT | D_X ln(J_A_measure/J_*) |
| DLC3878_5_arena_kernel | arena kernel common convention | MISSING_ARENA_DOMAIN_LOCK | D_X ln(K_arena,A/K_*) |
| DLC3878_6_radiative | radiative/readout closure common | UNSIGNED_READOUT_RAD_CLOSURE | D_X ln(R_rad,A/R_rad,*) |
| DLC3878_7_common_calibration | common scale derivative silence | NOT_DERIVED_RETAIN_COMMON_DRIFT | b_common_drift |

## Relative Tail Contract

| contract_id | quantity | formula_or_definition | status |
| --- | --- | --- | --- |
| RTC3878_0_relative_tail | b_tail_rel,A | b_tail_rel,A := b_readout_rel,A + b_source_slot_rel,A + b_rad_rel,A | RUNNER_FILL_NONCLAIM |
| RTC3878_1_common_tail | z_tail_common | z_tail_common := D_Xhat ln R_* + D_Xhat ln c_* + D_Xhat ln w_* + D_Xhat ln kappa_* + D_Xhat ln J_* + D_Xhat ln K_* + D_Xhat ln R_rad,* | COMMON_CALIBRATION_CHANNEL_RETAINED |
| RTC3878_2_common_drift | b_common_drift | b_common_drift := \|D_t ln C_*\| + \|D_r ln C_*\| + \|D_frame ln C_*\| + \|D_lambda ln C_*\| + \|Delta_domain(C_*)\| | MISSING_COMMON_SCALE_DERIVATIVE_SILENCE |
| RTC3878_3_readout_rel | b_readout_rel,A | b_readout_rel,A := \|D_Xhat ln(R_A/R_*)\| + \|delta_readout_domain,A-delta_readout_domain,*\| | MISSING_READOUT_NATURALITY_OR_BOUND |
| RTC3878_4_source_slot_rel | b_source_slot_rel,A | b_source_slot_rel,A := \|D_Xhat ln(c_A_pre/c_*)\| + \|D_Xhat ln(w_A/w_*)\| + \|D_Xhat ln(kappa_A/kappa_*)\| + \|D_Xhat ln(J_A_measure/J_*)\| + \|D_Xhat ln(K_arena,A/K_*)\| | MISSING_RELATIVE_SOURCE_SLOT_ZERO_OR_BOUND |
| RTC3878_5_rad_rel | b_rad_rel,A | b_rad_rel,A := \|D_Xhat ln(R_rad,A/R_rad,*)\| + \|delta_lambda_readout,A-delta_lambda_readout,*\| + \|delta_J_eff,A-delta_J_eff,*\| + \|Phi_EM_rad,A-Phi_EM_rad,*\| | MISSING_RELATIVE_RAD_CLOSURE_OR_BOUND |
| RTC3878_6_composition_gate | composition_residual | composition tests see b_tail_rel,A-B, not pure common C_* | RELATIVE_BRANCH_ONLY |
| RTC3878_7_absolute_gate | absolute_source_residual | Newton/PPN/orbital source normalization sees b_common_drift unless G_ref/kappa/source projector are fixed in one convention | COMMON_BRANCH_STILL_LIVE |

## First Arena Fill Readiness

| readiness_id | arena | calibrated_tail_use | status | missing_for_claim |
| --- | --- | --- | --- | --- |
| AFR3878_0_calibrated_Newton | Newton/Poisson/local_GR | use common mode as one calibrated G_eff only if b_common_drift=0 and same Hilbert source enters Poisson/orbital/PPN | BEST_NEXT_DERIVATION_ROUTE | kappa_ref;G_ref;M_H projector;common drift;boundary terms |
| AFR3878_1_WEP | MICROSCOPE_WEP | WEP sees relative tail b_tail_rel,Ti-Pt times tau_WEP/material kernel | NOT_SCOREABLE | DeltaF_TiPt,c;official tau_WEP;readout kernel;relative coefficient values |
| AFR3878_2_clocks | clock_alpha | clock rows see readout/radiative relative coefficient under one clock convention | NOT_SCOREABLE | b_alpha_tau;z_g_tau;s_XF2_tau;clock readout normalization |
| AFR3878_3_R10 | R10_short_range | R10 sees relative source/test tail and finite-range kernel, not common calibrated G alone | NOT_SCOREABLE | real alpha_bound(lambda);K_R10(lambda);beta source/test;profile convention |
| AFR3878_4_PPN_orbital | PPN_orbital | PPN/orbits require common source drift plus relative source-profile tails under one worldtube convention | NOT_SCOREABLE | tau_PPN;tau_orbital;source profile;projector stress;common drift |

## Calibrated Runner Update

| update_id | runner_field | rule | status |
| --- | --- | --- | --- |
| RUNU3878_0_previous | z_g_active | \|z_g_active\| <= b_Qstar + b_Noether + b_tail | previous packed form |
| RUNU3878_1_split | b_tail | b_tail -> b_tail_rel + b_common_drift after one calibrated common scale is separated | COMMON_RELATIVE_SPLIT |
| RUNU3878_2_calibrated_runner | z_g_active,cal | \|z_g_active,cal\| <= b_Qstar + b_Noether + b_tail_rel + b_common_drift | RUNNER_SCHEMA_REFINED |
| RUNU3878_3_WEP_guard | composition tests | relative material/source tails use b_tail_rel; common C_* alone is not a WEP source charge | RELATIVE_ONLY_FOR_COMPOSITION |
| RUNU3878_4_Newton_guard | Newton/PPN/source normalization | common C_* still needs b_common_drift=0 or explicit source-backed drift bound | COMMON_DRIFT_LIVE |
| RUNU3878_5_no_claim | claim_allowed | false until b_Qstar,b_Noether,b_tail_rel,b_common_drift and s_XF2_active are zero-proved or sourced in one domain | NO_CLAIM |

## Claim Gates

| gate_id | status | detail | claim_allowed |
| --- | --- | --- | --- |
| G3878_0_sources | PASS | 29/29 sources resolved | False |
| G3878_1_common_theorem | PASS | common-relative split | False |
| G3878_2_relative_zero | PASS | connected naturality route | False |
| G3878_3_common_guard | PASS | common drift retained | False |
| G3878_4_contracts | PASS | absolute_source_residual,b_common_drift,b_rad_rel,A,b_readout_rel,A,b_source_slot_rel,A,b_tail_rel,A,composition_residual,z_tail_common | False |
| G3878_5_arena | PASS | Newton common-mode route selected | False |
| G3878_6_runner | PASS | \|z_g_active,cal\| <= b_Qstar + b_Noether + b_tail_rel + b_common_drift | False |
| G3878_7_no_claim | PASS | valid_for_claim=false throughout | False |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3878_0 | 3879-Y5-R2FR-calibrated-GN-common-tail-to-Newton-Poisson-chain.md | attack the common branch directly: derive whether the universal tail scale can be fixed once as G_N/kappa_ref and kept derivative-silent across Newton, PPN, orbital and clock/source domains | 3878 separates relative material tails from common calibrated source drift; the next local-GR leap is proving the common scale is a fixed coupling rather than a hidden time/range/frame source residual |

## Bottom Line

This is the cleanest route I can see right now: split the coupling problem into `b_tail_rel` and `b_common_drift`. `b_tail_rel` is the thing that would poison WEP/material/source tests. `b_common_drift` is the GR/Newton coupling problem: can MTS fix one universal source scale once, the way GR uses one `G_N`, without letting it drift by time, range, frame, or readout domain? That is now the next target.
