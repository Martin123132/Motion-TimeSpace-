# 3015 — PPN Kernel from Local Closure Residual Envelope under AX1090

Status: `Y5_R2FR_3015_PPN_kernel_contract_staged_gamma_alpha3_next`

## Verdict

3015 moves us closer to the actual GR/Newton target. R10 is no longer the main boxing ring; PPN is.

The PPN comparator side is present, and the fixed measured-`GM` guard is active. But the MTS prediction side is still a kernel contract, not a score: `K_PPN`, weak-field source frame, PPN gauge/readout map, and closure-component values are missing.

The useful result is a componentwise PPN residual vector:

`Delta_PPN_abs = (|gamma-1|, |beta-1|, |alpha1|, |alpha2|, |alpha3|, |xi|)`.

Every component is tied to the local-closure envelope, and every component remains nonclaim until source-frame and kernel owners are signed.

## Source Register

| source_id | exists | role | status |
| --- | --- | --- | --- |
| SRC3015_00_3014_doc | True | previous checkpoint R10 demotion and PPN route | PRESENT |
| SRC3015_01_3014_next | True | 3015 target definition | PRESENT |
| SRC3015_02_3014_closure | True | local closure residual envelope | PRESENT |
| SRC3015_03_3014_ppn_handoff | True | PPN handoff and no-shortcut guard | PRESENT |
| SRC3015_04_ppn_bounds_2513 | True | source-backed comparator rows | PRESENT |
| SRC3015_05_ppn_kernel_2513 | True | existing PPN source-weight kernel skeleton | PRESENT |
| SRC3015_06_measured_GM_guard_2513 | True | fixed measured-GM no-absorb guard | PRESENT |
| SRC3015_07_normalized_ppn_inputs_1640 | True | older missing normalized PPN input ledger | PRESENT |
| SRC3015_08_common_frame_kernel_2489 | True | common-frame conformal/disformal PPN kernel rows | PRESENT |
| SRC3015_09_gk_ppn_2559 | True | GK stress PPN residual ledger | PRESENT |
| SRC3015_10_ppn_bound_2631 | True | PPN comparator bound ledger | PRESENT |
| SRC3015_11_rankzero_envelope_2968 | True | rank-zero residual projection envelope | PRESENT |

## PPN Kernel Contract

| kernel_id | observable | status | blocks_claim |
| --- | --- | --- | --- |
| PPNK3015_0_gamma | gamma_minus_1 | KERNEL_CONTRACT_WRITTEN_VALUES_MISSING | MISSING_K_GAMMA; MISSING_SOURCE_FRAME; MISSING_READOUT_GAUGE |
| PPNK3015_1_beta | beta_minus_1 | SECOND_ORDER_KERNEL_MISSING | MISSING_BETA_SECOND_ORDER_KERNEL; MISSING_SOURCE_NORMALIZATION |
| PPNK3015_2_alpha1 | alpha1 | PREFERRED_FRAME_KERNEL_MISSING | MISSING_FRAME_VECTOR; MISSING_ENDPOINT_KERNEL |
| PPNK3015_3_alpha2 | alpha2 | VECTOR_DOMAIN_KERNEL_MISSING | MISSING_DOMAIN_PROJECTOR_KERNEL |
| PPNK3015_4_alpha3 | alpha3 | SOURCE_EXCHANGE_KERNEL_ULTRATIGHT_MISSING | MISSING_SOURCE_CURRENT_OWNER; ULTRATIGHT_BOUND_REQUIRES_THEOREM_ZERO_OR_STRONG_NUMERIC_BOUND |
| PPNK3015_5_xi | xi | BOUNDARY_DOMAIN_KERNEL_MISSING | MISSING_BOUNDARY_DOMAIN_RESPONSE |
| PPNK3015_6_total | PPN_abs_vector | VECTOR_SCHEMA_READY_VALUES_MISSING | MISSING_ALL_COMPONENT_VALUES_OR_ZERO_THEOREMS |

## PPN Residual Vector

| vector_id | components | status | fixed_GM_policy |
| --- | --- | --- | --- |
| PVEC3015_0_template | gamma_minus_1_abs; beta_minus_1_abs; alpha1_abs; alpha2_abs; alpha3_abs; xi_abs | TEMPLATE_ONLY_NONCLAIM | only one proven common universal scalar may be absorbed into measured GM |
| PVEC3015_1_no_cancellation | absolute component envelope | GUARD_ACTIVE_VALUES_MISSING | relative/source/time/frame weights survive fixed-GM calibration |

## Comparator Links

| link_id | observable | upper_bound | source_dataset | current_status |
| --- | --- | --- | --- | --- |
| CLINK3015_0_gamma_minus_1 | gamma_minus_1 | 2.3e-05 | Cassini_Shapiro_gamma_2003 | COMPARATOR_ONLY_NOT_MTS_PREDICTION |
| CLINK3015_1_beta_minus_1 | beta_minus_1 | 7.8e-05 | Will_2014_PPN_beta_table | COMPARATOR_ONLY_NOT_MTS_PREDICTION |
| CLINK3015_2_alpha1 | alpha1 | 1e-04 | Will_2014_PPN_alpha1_table | COMPARATOR_ONLY_NOT_MTS_PREDICTION |
| CLINK3015_3_alpha2 | alpha2 | 2e-09 | Will_2014_PPN_alpha2_table | COMPARATOR_ONLY_NOT_MTS_PREDICTION |
| CLINK3015_4_alpha3 | alpha3 | 4e-20 | Will_2014_PPN_alpha3_table | COMPARATOR_ONLY_NOT_MTS_PREDICTION |
| CLINK3015_5_xi | xi | 4e-09 | Will_2014_PPN_xi_table | COMPARATOR_ONLY_NOT_MTS_PREDICTION |

## Fixed GM Guard

| guard_id | rule | current_status | blocks |
| --- | --- | --- | --- |
| GMG3015_0_common_mode | one constant, universal, range/time/species/frame independent source normalization may be absorbed into measured GM only after universality is proved | CONDITIONAL_CALIBRATION_RULE_ONLY | absorbing relative/source/frame residuals into fitted GM |
| GMG3015_1_relative_weight | relative species/source weights survive fixed-GM calibration | LIVE_RESIDUAL | claiming WEP-clean or one-body calibrated source shifts are GR |
| GMG3015_2_range_time_frame | range/time/frame/source-profile dependence cannot be hidden in a constant GM fit | LIVE_RESIDUAL | PPN/R10/orbital consistency shortcuts |
| GMG3015_3_readout | PPN gauge/readout map must be fixed before comparing gamma/beta | MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION | fake beta/gamma closure by post-fit calibration |

## Blocker Ledger

| blocker_id | blocking_condition | precise_missing_object | next_attack |
| --- | --- | --- | --- |
| BLK3015_0_K_PPN | MISSING_K_PPN_RESPONSE_KERNEL | linear and second-order weak-field response maps from closure residual components to gamma,beta,alpha_i,xi | derive K_gamma first under fixed source frame, then beta second-order kernel |
| BLK3015_1_source_frame | MISSING_WEAK_FIELD_SOURCE_FRAME_AND_PPN_GAUGE | observed coframe, PPN gauge, source mass convention and readout map | lock source frame and measured-GM convention before any numeric bound comparison |
| BLK3015_2_component_values | MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS | eps_JH_Z_abs, eps_JNH_abs, eps_B_abs, Delta_readout_abs_A, Q_cdb_abs, eps_projector_abs, E_DqZ_A | fill or theorem-zero closure residual components one by one |
| BLK3015_3_alpha3_ultratight | ALPHA3_SOURCE_EXCHANGE_ULTRATIGHT | source-current conservation/exchange theorem or extremely small numeric bound | route alpha3 to source-current zero theorem or keep as leading PPN blocker |
| BLK3015_4_no_cancellation | NO_CANCELLATION_VECTOR_NOT_NUMERIC | componentwise absolute PPN vector with no offsetting source families | keep componentwise absolute vector until a parent identity signs a cancellation |

## Dry-Run Results

| dryrun_id | check | passed | result_status |
| --- | --- | --- | --- |
| DR3015_0_comparators | PPN comparator rows are linked | True | COMPARATOR_SIDE_READY_NONCLAIM |
| DR3015_1_kernel_values | K_PPN numeric/source-signed kernel values exist | False | BLOCKED_NONCLAIM |
| DR3015_2_fixed_GM | fixed measured-GM guard is active | True | GUARD_ACTIVE |
| DR3015_3_prediction_row | valid PPN prediction row exists | False | BLOCKED_NONCLAIM |
| DR3015_4_claim | PPN/local-GR claim allowed | False | CLAIM_FORBIDDEN |

## Promotion Gates

| gate_id | gate | result | notes |
| --- | --- | --- | --- |
| GATE3015_0_sources_exist | all cited local source paths exist | True | 3015 only cites current local ledgers |
| GATE3015_1_comparators_linked | PPN comparator bounds are linked | True | comparator side is present but not an MTS prediction |
| GATE3015_2_fixed_GM_guard | fixed measured-GM no-absorb guard is active | True | only one proven common scalar can be absorbed |
| GATE3015_3_kernel_values | K_PPN values/source-signed kernels exist | False | kernel contracts written; values missing |
| GATE3015_4_prediction_row | valid PPN prediction row exists | False | source frame, gauge, component values and no-cancellation vector are missing |
| GATE3015_5_PPN_claim | PPN/local-GR pass claim allowed | False | PPN is now structured, not passed |

## Decision Ledger

| decision_id | decision | rationale |
| --- | --- | --- |
| DEC3015_0_status | 3015 builds the PPN kernel contract from the local-closure residual envelope, but no PPN pass is claimed. | The comparator side exists and the fixed-GM guard is active; the theory side still needs K_PPN, source frame, gauge/readout map and component values. |
| DEC3015_1_priority | Gamma and alpha3 are the next sharpest PPN targets. | Gamma is the cleanest weak-field metric response entry; alpha3 is ultratight and forces source-current conservation discipline. |

## Next Target

| next_id | target_doc | mission | success_condition |
| --- | --- | --- | --- |
| NEXT3015_0_3016 | 3016-Y5-R2FR-gamma-and-alpha3-PPN-kernel-first-derivation-under-AX1090.md | Try to derive the first two concrete PPN kernels from the closure envelope: gamma as weak-field metric response, alpha3 as source-current exchange/conservation guard. | gamma and alpha3 rows either get source-signed kernel formulas with explicit missing coefficients, or are blocked by exact source-frame/current-conservation clauses; no PPN claim. |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3015_00_sources_exist | True | every cited local source path exists | P8_Y5_R2FR_3015_SOURCE_REGISTER.csv |
| VAL3015_01_csv_parse | True | generated CSV rows parse cleanly | all generated CSV artifacts import with csv.DictReader |
| VAL3015_02_comparators_linked | True | PPN comparator rows are linked but not promoted as predictions | P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv |
| VAL3015_03_kernel_contracts_written | True | component PPN kernel contracts are explicit with blockers | P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv |
| VAL3015_04_fixed_GM_guard_active | True | fixed measured-GM no-absorb guard is active | P8_Y5_R2FR_3015_FIXED_GM_GUARD.csv |
| VAL3015_05_prediction_not_valid | True | no valid PPN prediction row is claimed | P8_Y5_R2FR_3015_PROMOTION_GATES.csv |
| VAL3015_06_claims_blocked | True | PPN/local-GR claims remain blocked | P8_Y5_R2FR_3015_PROMOTION_GATES.csv |
| VAL3015_07_missing_markers_nonclaim | True | rows with MISSING markers are never valid_for_claim=true | all 3015 generated ledgers |
| VAL3015_08_outputs_scoped | True | no generated file is outside post-checkpoint-work | generated path scope check |
| VAL3015_09_formalization_not_targeted | True | formalization-workbench is not modified by this checkpoint | output target list excludes formalization-workbench |
| VAL3015_10_next_target_selected | True | next target selects gamma and alpha3 PPN kernel derivation | P8_Y5_R2FR_3015_NEXT_TARGET.csv |
| VAL3015_99_overall | True | all 3015 validation checks pass | aggregate of VAL3015_00 through VAL3015_10 |

## Files Written

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_PPN_RESIDUAL_VECTOR_TEMPLATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_FIXED_GM_GUARD.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_BLOCKER_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_DRYRUN_RESULTS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_PROMOTION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3015_BRANCH_COPIES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3015_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\PPN_kernel_from_local_closure_envelope_3015_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\PPN_residual_vector_template_3015_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\fixed_GM_guard_for_PPN_closure_3015_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR3015_PPN_SOURCE_FRAME_AND_KERNEL_OWNER_NEXT.csv`

## Hard Guardrails Still Active

- No PPN/local-GR pass claim.
- No fitted-`GM` absorption of source residuals.
- No hidden cancellation between PPN components.
- No comparator-bound inversion into theory coefficients.
- No `formalization-workbench` edits.
- No GitHub action.
