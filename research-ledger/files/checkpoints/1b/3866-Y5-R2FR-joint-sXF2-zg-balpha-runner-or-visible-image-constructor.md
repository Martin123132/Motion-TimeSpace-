# 3866 — Joint sXF2 / z_g / b_alpha Runner Or Visible Image Constructor

Generated: `2026-07-01T05:45:49+00:00`

## Purpose

3865 gave the exact finite identity and warned that alpha-only bounds cannot isolate `s_XF2`. This checkpoint makes that warning executable.

## Runner Law

`b_alpha_X = 2 z_g - s_XF2`

`|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|`

## Parent Constructor Route

`The derivation route closes only if the parent constructs the visible coefficient image category A_vis=Image(ParentGenerate) with no independent Coeff(F_Q^2), no hidden-visible Hom, and radiative/readout stability.`

## Acceptance Rule

`A claim row is allowed only if the image theorem is parent-signed, or every arena row has numeric same-domain b_alpha, z_g and s_XF2/projection inputs, source paths, units, and a valid external bound.`

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3866_00_3865_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3865_VISIBLE_OPERATOR_IMAGE_THEOREM.csv | True | True | 3865 runner handoff |
| SRC3866_01_3865_joint | source-intake\mts_residuals\P8_Y5_R2FR_3865_SXF2_ZG_BALPHA_JOINT_BOUND.csv | True | True | 3865 runner acceptance |
| SRC3866_02_3865_gates | source-intake\mts_residuals\P8_Y5_R2FR_3865_CLAIM_GATES.csv | True | True | 3865 next target gate |
| SRC3866_03_3865_validation | source-intake\mts_residuals\P8_Y5_BRR545_3865_VALIDATION.csv | True | True | previous validation |
| SRC3866_04_3864_bound | source-intake\mts_residuals\P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv | True | True | 3864 lambdaF2 bound |
| SRC3866_05_3679_identity | source-intake\mts_residuals\P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv | True | True | canonical alpha/current/F2 identity |
| SRC3866_06_3679_live | source-intake\mts_residuals\P8_Y5_R2FR_3679_SXF2_CANONICAL_MAP_ROWS.csv | True | True | two-knob branch |
| SRC3866_07_3679_bound | source-intake\mts_residuals\P8_Y5_R2FR_3679_SXF2_BOUND_INPUT_ROWS.csv | True | True | s_XF2 alpha clock route |
| SRC3866_08_3680_zg_components | source-intake\mts_residuals\P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv | True | True | z_g component decomposition |
| SRC3866_09_3680_zg_verdict | source-intake\mts_residuals\P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv | True | True | z_g zero verdict |
| SRC3866_10_3508_zg | source-intake\mts_residuals\P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv | True | True | z_g source reduction |
| SRC3866_11_3118_balpha | source-intake\mts_residuals\P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv | True | True | b_alpha product template |
| SRC3866_12_1052_clock | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | True | True | alpha clock bound |
| SRC3866_13_1052_wep | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | True | True | alpha WEP projection |
| SRC3866_14_1052_r10 | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | True | True | alpha R10 product |
| SRC3866_15_2766_image | source-intake\mts_residuals\P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv | True | True | visible image verdict |
| SRC3866_16_2659_hom | source-intake\mts_residuals\P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv | True | True | typed no-Hom theorem |
| SRC3866_17_3118_hom | source-intake\mts_residuals\P8_Y5_R2FR_3118_NO_HIDDEN_VISIBLE_COEFFICIENT_HOM_GATE.csv | True | True | hidden F2 countermodel |

## Runner Theorem

| theorem_id | claim_piece | status | result |
| --- | --- | --- | --- |
| JRI3866_0_identity | joint alpha/current/F2 identity | DERIVED | EXACT_LINEAR_IDENTITY |
| JRI3866_1_runner_law | same-arena no-cancellation bound | NONCLAIM_RUNNER_READY | EXECUTABLE_BOUND_LAW |
| JRI3866_2_image_constructor | visible image constructor route | CURRENTLY_UNSIGNED | CONSTRUCTOR_ROUTE_DEFINED_NOT_CLOSED |
| JRI3866_3_acceptance_rule | runner acceptance rule | IMPLEMENTED | STRICT_ACCEPTANCE_RULE |
| JRI3866_4_current_verdict | strict current verdict | CURRENT_NONCLAIM | JOINT_RUNNER_BLOCKED_CORRECTLY |
| JRI3866_5_next_handoff | next target | COUPLING_ROUTE_EXECUTABLE | NEXT_GATE_IS_INPUT_ACQUISITION_OR_IMAGE_CONSTRUCTION |

## Input Schema

| input_id | arena | symbol | requirement | current_status |
| --- | --- | --- | --- | --- |
| SCHEMA3866_0 | all | arena | required | present |
| SCHEMA3866_1 | all | tau_A | required | missing |
| SCHEMA3866_2 | all | b_alpha_tau | required | missing_or_source_only |
| SCHEMA3866_3 | all | z_g_tau | required | missing |
| SCHEMA3866_4 | all | s_XF2_tau | optional | missing |
| SCHEMA3866_5 | all | external_bound | required for scoring | partial |
| SCHEMA3866_6 | all | projection_consistency | required | missing |

## Dryrun Cases

| case_id | arena | input_status | b_alpha_tau | z_g_tau | external_bound |
| --- | --- | --- | --- | --- | --- |
| CASE3866_0_all_missing | clock | MISSING_MTS_PRODUCTS | MISSING_BALPHA_TIMES_TAU_CLOCK | MISSING_ZG_TIMES_TAU_CLOCK | 2.1e-18 |
| CASE3866_1_alpha_only_clock | clock | ALPHA_SOURCE_BOUND_ONLY | 2.1e-18 | MISSING_ZG_TIMES_TAU_CLOCK | 2.1e-18 |
| CASE3866_2_zg_zero_unsigned | clock | ZG_ZERO_ASSUMED_NOT_PARENT_SIGNED | 2.1e-18 | 0 | 2.1e-18 |
| CASE3866_3_toy_numeric_nonclaim | clock | TOY_NUMERIC_NO_SOURCE | 2.0e-18 | 1.0e-18 | 5.0e-18 |
| CASE3866_4_R10_template | R10 | R10_PROJECTION_INPUTS_MISSING | MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL | MISSING_ZG_R10_PROJECTION | MISSING_VALID_ALPHA_BOUND_CURVE |

## Dryrun Results

| result_id | arena | computed_abs_s_XF2_tau_bound | passes_bound | runner_verdict | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| RES_CASE3866_0_all_missing | clock | MISSING | False | BLOCKED_MISSING_JOINT_INPUTS | False |
| RES_CASE3866_1_alpha_only_clock | clock | MISSING | False | BLOCKED_ALPHA_ONLY_NO_ZG | False |
| RES_CASE3866_2_zg_zero_unsigned | clock | 2.100000000000e-18 | True | BLOCKED_ZG_ZERO_UNSIGNED | False |
| RES_CASE3866_3_toy_numeric_nonclaim | clock | 4.000000000000e-18 | True | TOY_PASS_NONCLAIM | False |
| RES_CASE3866_4_R10_template | R10 | MISSING | False | BLOCKED_R10_PROJECTION_INPUTS_MISSING | False |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| G3866_0_identity | PASS_EXACT_IDENTITY_AND_RUNNER_LAW | False | b_alpha_X=2z_g-s_XF2 and |s tau| bound are implemented |
| G3866_1_alpha_only | PASS_ALPHA_ONLY_BLOCKED | False | alpha clock source bound without z_g projection is blocked |
| G3866_2_zg_unsigned | PASS_ZG_ZERO_UNSIGNED_BLOCKED | False | z_g=0 must be parent-signed before direct s_XF2 bound is claimable |
| G3866_3_results_nonclaim | PASS_DRYRUN_NONCLAIM | False | 5 dryrun rows generated with claim_allowed=false |
| G3866_4_next | PASS_3867_SOURCE_INPUT_ACQUISITION_OR_IMAGE_CONSTRUCTOR_TARGET | False | the runner exists; progress now needs source-backed inputs or parent image construction |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| D3866_0 | Build the runner before claiming any finite bound. | The branch now has executable nonclaim failure modes instead of prose-only warnings. |
| D3866_1 | Reject alpha-only and unsigned z_g=0 routes. | The coupling throat cannot be bypassed by clock alpha data alone. |
| D3866_2 | Next step must supply inputs or construct the parent image category. | Further progress should be either source acquisition/projection or actual parent-category construction. |

## Bottom Line

3866 turns the coupling fork into a usable tool: if the parent image theorem closes, the no-extra-F2 route can promote; if it does not, the finite branch must be scored jointly with `s_XF2`, `z_g`, and `b_alpha` in the same arena. Current clock/WEP/R10 rows are correctly blocked because `z_g` and MTS-side projection inputs are missing.

Next target: `3867-Y5-R2FR-source-backed-joint-alpha-current-F2-input-acquisition-or-image-constructor.md`.
