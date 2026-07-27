# 3470 - Executable Coefficient Vector Runner And Input Templates

**Current verdict:** the WEP-first coefficient-vector runner is now executable. It reads row templates, separates numeric, missing, theorem-zero and common-mode rows, and refuses both missing-input and cancellation-style passes.

**Concrete progress:** current dry-run result is `FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND` with known absolute contribution `5.600000000000e-15` against `eta_bound=2.800000000000e-15`. This is exactly the discipline gate we needed: fill or prove rows, then rerun.

## Source Register
| timestamp_utc | source_id | source_type | source_path | source_url | exists_or_url_present | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-29T02:44:20.784710+00:00 | script_3470 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3470_executable_coefficient_vector_runner_and_input_templates.py |  | True | generator and dry-run runner | False |
| 2026-06-29T02:44:20.784710+00:00 | doc_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3469-Y5-R2FR-visible-coefficient-owner-contract-or-multiarena-vector-runner.md |  | True | 3469 handoff | False |
| 2026-06-29T02:44:20.784710+00:00 | next_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_NEXT_TARGET.csv |  | True | 3470 target statement | False |
| 2026-06-29T02:44:20.784710+00:00 | contract_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv |  | True | visible coefficient owner contract | False |
| 2026-06-29T02:44:20.784710+00:00 | schema_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_MULTIARENA_VECTOR_RUNNER_SCHEMA.csv |  | True | multi-arena schema | False |
| 2026-06-29T02:44:20.784710+00:00 | dryrun_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_WEP_VECTOR_DRYRUN.csv |  | True | previous WEP dry-run | False |
| 2026-06-29T02:44:20.784710+00:00 | blockers_3469 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_BLOCKER_LEDGER.csv |  | True | previous blocker ledger | False |
| 2026-06-29T02:44:20.784710+00:00 | vector_3468 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv |  | True | retained coefficient vector | False |
| 2026-06-29T02:44:20.784710+00:00 | envelope_3468 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_NO_CANCELLATION_VECTOR_ENVELOPE.csv |  | True | no-cancellation envelope | False |
| 2026-06-29T02:44:20.784710+00:00 | alpha_bound_3465 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv |  | True | alpha WEP bound | False |
| 2026-06-29T02:44:20.784710+00:00 | mass_row_3466 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv |  | True | mass WEP bound | False |
| 2026-06-29T02:44:20.784710+00:00 | local_bounds | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv |  | True | empirical local bounds | False |

## Arena Config Template
| arena_id | arena | observable | bound_abs | bound_units | pass_rule | claim_policy | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARENA3470_0_WEP_TiPt | WEP_MICROSCOPE_TiPt | eta_TiPt_abs | 2.800000000000e-15 | dimensionless | all included live rows numeric or theorem_zero; absolute_sum <= bound_abs; no signed cancellation | valid_for_claim only if every live row has source path and no MISSING markers | EXECUTABLE_NOW_FOR_DRYRUN | False |
| ARENA3470_1_CLOCKS | CLOCKS_SPECTRA | delta_ln_frequency | MISSING_CLOCK_BOUND | dimensionless | schema hook only until clock sensitivity rows exist | blocked | HOOK_ONLY_INPUTS_MISSING | False |
| ARENA3470_2_R10 | R10_SHORT_RANGE | alpha_lambda_prediction | MISSING_BOUND_CURVE_ROW_SELECTION | dimensionless | schema hook only until MTS numerator and lambda row exist | blocked | HOOK_ONLY_NUMERATOR_MISSING | False |

## WEP Vector Input Template
| input_id | arena | symbol | component_role | include_in_envelope | theorem_zero | sensitivity_abs | product_abs_bound | units | source_path | status | missing_marker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WVI3470_0_b_alpha | WEP_MICROSCOPE_TiPt | b_alpha | visible_alpha_product | True | False | 1.989808886825e-03 | 1.407170315973e-12 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv | NUMERIC_SINGLE_CHANNEL_BOUND |  | False |
| WVI3470_1_b_mhat | WEP_MICROSCOPE_TiPt | b_mhat | visible_mass_ratio_product | True | False | 3.314967641189e-03 | 8.446537954729e-13 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv | NUMERIC_SINGLE_CHANNEL_BOUND |  | False |
| WVI3470_2_b_me | WEP_MICROSCOPE_TiPt | b_me | electron_mass_or_yukawa_product | True | False | MISSING_DELTA_Q_ME_TIPT | MISSING_D_ME_EFF_BOUND | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | MISSING_LIVE_COMPONENT | MISSING_DELTA_Q_ME_TIPT;MISSING_D_ME_EFF_BOUND | False |
| WVI3470_3_b_bind | WEP_MICROSCOPE_TiPt | b_bind | nuclear_binding_product | True | False | MISSING_EXACT_BINDING_TENSOR | FOLDED_ONLY_IN_PROXY_MASS_CHANNEL | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | MISSING_OR_FOLDED_LIVE_COMPONENT | MISSING_EXACT_BINDING_TENSOR;MISSING_SEPARATE_D_BIND_EFF_BOUND | False |
| WVI3470_4_b_readout | WEP_MICROSCOPE_TiPt | b_readout | readout_radiative_product | True | False | MISSING_READOUT_SENSITIVITY | MISSING_D_READOUT_EFF_BOUND | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | MISSING_LIVE_COMPONENT | MISSING_READOUT_SENSITIVITY;MISSING_D_READOUT_EFF_BOUND | False |
| WVI3470_5_direct_shadow_projector | WEP_MICROSCOPE_TiPt | direct_shadow_projector | nonconstant_source_residual | True | False | 1.0 | MISSING_DIRECT_SHADOW_PROJECTOR_BOUND | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_BLOCKER_LEDGER.csv | MISSING_LIVE_COMPONENT | MISSING_DIRECT_SHADOW_PROJECTOR_BOUND | False |
| WVI3470_6_b_common | WEP_MICROSCOPE_TiPt | b_common | common_calibration_mode | False | True | 0.0 | 0.0 | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv | IGNORED_COMMON_MODE_NOT_WEP_NUMERATOR |  | False |

## Multi-Arena Schema Hooks
| hook_id | arena | input_file | runner_output | next_fill | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HOOK3470_0_WEP | WEP_MICROSCOPE_TiPt | P8_Y5_R2FR_3470_WEP_VECTOR_INPUT_TEMPLATE.csv | P8_Y5_R2FR_3470_WEP_VECTOR_RUNNER_RESULTS.csv | replace MISSING markers with sourced numeric sensitivity/product rows or theorem_zero=true | EXECUTABLE | False |
| HOOK3470_1_CLOCKS | CLOCKS_SPECTRA | future_CLOCK_VECTOR_INPUT_TEMPLATE.csv | future_CLOCK_VECTOR_RUNNER_RESULTS.csv | clock sensitivity coefficients and clock bounds | SCHEMA_HOOK_ONLY | False |
| HOOK3470_2_R10 | R10_SHORT_RANGE | future_R10_ALPHA_NUMERATOR_INPUT_TEMPLATE.csv | future_R10_ALPHA_RUNNER_RESULTS.csv | lambda row, bound curve row, MTS alpha numerator/source-test normalization | SCHEMA_HOOK_ONLY | False |

## WEP Vector Runner Results
| result_id | symbol | include_in_envelope | theorem_zero | sensitivity_abs | product_abs_bound | abs_contribution | row_status | blocker | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WRR3470_0_b_alpha | b_alpha | True | False | 1.989808886825e-03 | 1.407170315973e-12 | 2.799999999999e-15 | NUMERIC_LIVE_COMPONENT |  | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3465_ALPHA_ONLY_BOUND_CALCULATION.csv | False |
| WRR3470_1_b_mhat | b_mhat | True | False | 3.314967641189e-03 | 8.446537954729e-13 | 2.800000000000e-15 | NUMERIC_LIVE_COMPONENT |  | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv | False |
| WRR3470_2_b_me | b_me | True | False | MISSING_DELTA_Q_ME_TIPT | MISSING_D_ME_EFF_BOUND | MISSING | BLOCKING_MISSING_LIVE_INPUT | MISSING_DELTA_Q_ME_TIPT;MISSING_D_ME_EFF_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | False |
| WRR3470_3_b_bind | b_bind | True | False | MISSING_EXACT_BINDING_TENSOR | FOLDED_ONLY_IN_PROXY_MASS_CHANNEL | MISSING | BLOCKING_MISSING_LIVE_INPUT | MISSING_EXACT_BINDING_TENSOR;MISSING_SEPARATE_D_BIND_EFF_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | False |
| WRR3470_4_b_readout | b_readout | True | False | MISSING_READOUT_SENSITIVITY | MISSING_D_READOUT_EFF_BOUND | MISSING | BLOCKING_MISSING_LIVE_INPUT | MISSING_READOUT_SENSITIVITY;MISSING_D_READOUT_EFF_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3468_RETAINED_COEFFICIENT_VECTOR.csv | False |
| WRR3470_5_direct_shadow_projector | direct_shadow_projector | True | False | 1.0 | MISSING_DIRECT_SHADOW_PROJECTOR_BOUND | MISSING | BLOCKING_MISSING_LIVE_INPUT | MISSING_DIRECT_SHADOW_PROJECTOR_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_BLOCKER_LEDGER.csv | False |
| WRR3470_6_b_common | b_common | False | True | 0.0 | 0.0 | 0.000000000000e+00 | IGNORED_COMMON_MODE_OR_NOT_IN_WEP_NUMERATOR |  | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv | False |
| WRR3470_SUMMARY | WEP_VECTOR_SUMMARY | True | False | included_live_rows=6;numeric_live_rows=2;theorem_zero_rows=0 | eta_bound=2.800000000000e-15 | 5.600000000000e-15 | FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND | b_me:MISSING_DELTA_Q_ME_TIPT;MISSING_D_ME_EFF_BOUND;b_bind:MISSING_EXACT_BINDING_TENSOR;MISSING_SEPARATE_D_BIND_EFF_BOUND;b_readout:MISSING_READOUT_SENSITIVITY;MISSING_D_READOUT_EFF_BOUND;direct_shadow_projector:MISSING_DIRECT_SHADOW_PROJECTOR_BOUND | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3470_executable_coefficient_vector_runner_and_input_templates.py | False |

## Runner Refusal Rules
| rule_id | condition | runner_action | valid_for_claim |
| --- | --- | --- | --- |
| REF3470_0_missing_live | any included row has MISSING marker and theorem_zero=false | fail blocked; do not claim | False |
| REF3470_1_known_sum_exceeds | known absolute contribution sum exceeds arena bound | fail blocked even before missing rows are filled | False |
| REF3470_2_no_cancellation | signed cancellation is required for pass | fail blocked; absolute envelope only | False |
| REF3470_3_common_mode | row is common calibration mode | exclude from WEP numerator but keep Newton/G guard | False |

## Claim Gates
| gate_id | gate | pass | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG3470_0_templates_written | WEP vector input and arena config templates exist | True | input_rows=7 | False | False |
| CG3470_1_runner_executes | runner evaluates numeric, missing and common-mode rows | True | numeric=2;missing=4;summary=FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND | False | False |
| CG3470_2_WEP_pass | WEP vector passes absolute envelope | False | FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND | False | False |
| CG3470_3_multiarena_hooks | clock and R10 hooks are present | True | hooks written but input rows missing | False | False |
| CG3470_4_local_GR_claim | local GR/Newton/Maxwell source coupling derived | False | blocked by WEP vector failure and missing clock/R10/local source rows | False | False |

## Decision Ledger
| decision_id | decision | reason | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3470_0_runner_progress | Use the 3470 WEP vector runner as the reusable local-source discipline tool. | It reads templates, computes absolute contributions, and refuses missing/cancellation passes. | Fill or zero the highest-pressure missing WEP rows. | False | False |
| DEC3470_1_current_WEP_status | Current WEP vector is blocked, not failed as a theory claim. | FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND | Either theorem-zero b_alpha/b_mhat via visible coefficient owner, or fill b_me/b_bind/readout/direct residual rows and lower the absolute sum. | False | False |
| DEC3470_2_next | Next best move is first missing-row fill: b_me/clock-material sensitivity or theorem-zero contract. | The runner is now reusable; progress comes from filling rows or proving them zero. | 3471 should target b_me and clock/material sensitivity, or derive no electron-mass coefficient from the visible coefficient owner contract. | False | False |

## Validation
| validation_id | pass | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL3470_0_local_sources_exist | True | all local sources exist | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_1_templates_written | True | input_rows=7;arena_rows=3 | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_2_runner_blocks_correctly | True | FAIL_BLOCKED_MISSING_LIVE_COMPONENTS_AND_KNOWN_ABS_SUM_EXCEEDS_BOUND | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_3_common_mode_ignored | True | b_common excluded from WEP numerator | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_4_hooks_present | True | CLOCKS_SPECTRA;R10_SHORT_RANGE;WEP_MICROSCOPE_TiPt | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_5_local_GR_claim_blocked | True | local source claim remains false | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_6_no_claim_rows | True | all claim_allowed and valid_for_claim flags remain false | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_7_csv_parse | True | P8_Y5_R2FR_3470_SOURCE_REGISTER.csv:12;P8_Y5_R2FR_3470_ARENA_CONFIG_TEMPLATE.csv:3;P8_Y5_R2FR_3470_WEP_VECTOR_INPUT_TEMPLATE.csv:7;P8_Y5_R2FR_3470_MULTIARENA_SCHEMA_HOOKS.csv:3;P8_Y5_R2FR_3470_WEP_VECTOR_RUNNER_RESULTS.csv:8;P8_Y5_R2FR_3470_RUNNER_REFUSAL_RULES.csv:4;P8_Y5_R2FR_3470_CLAIM_GATES.csv:5;P8_Y5_R2FR_3470_DECISION_LEDGER.csv:3;P8_Y5_R2FR_3470_NEXT_TARGET.csv:1 | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_8_formalization_untouched_by_3470 | True | formalization_exists=True; 3470_outputs_in_formalization=0 | 2026-06-29T02:44:20.800260+00:00 |
| VAL3470_SUMMARY | True | PASS | 2026-06-29T02:44:20.800260+00:00 |

## Next Target
| next_doc | next_script | objective | success_gate | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3471-Y5-R2FR-bme-clock-material-row-or-electron-mass-zero-theorem.md | scripts/Y5_R2FR_3471_bme_clock_material_row_or_electron_mass_zero_theorem.py | Try to prove b_me=0 from the visible coefficient owner contract; if not, fill the first electron-mass/clock-material sensitivity row needed by the 3470 vector runner. | Either b_me is theorem-zero, or WEP/clocks receive a sourced b_me sensitivity/product row that the 3470 runner can read. | GitHub action; formalization-workbench edits; public WEP/local-GR claim; cancellation pass. | False | False |

## Short Readout
- Executable now: WEP vector dry-run.
- Numeric now: alpha and `b_mhat` one-channel rows.
- Blocking now: `b_me`, `b_bind`, `b_readout`, direct/shadow/projector, plus known absolute sum already above the bound.
- Next move: fill or theorem-zero the first missing live row, probably `b_me`.
