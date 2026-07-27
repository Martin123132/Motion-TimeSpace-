# 3011 — Local-Bound Acquisition Matrix for `q_loc`, `Delta_K`, and the Coupling Vector under AX1090

Status: `Y5_R2FR_3011_local_bound_acquisition_matrix_staged_R10_first_3012_next`

## Verdict

3011 turns the 3010 local-residual interface into a concrete acquisition board. It does **not** claim local GR, Newton, PPN, WEP, clock/EM or R10 success.

The useful gain is that the missing pieces are now split by arena instead of being one foggy phrase called "the coupling":

- R10 needs a real `alpha_bound(lambda)` curve **and** a `q_loc -> alpha(lambda)` normalization.
- PPN needs the weak-field response kernel and fixed measured-GM/source-frame convention.
- clocks/EM need the `alpha_EM` owner or theorem-zero plus `tau_clock`.
- WEP needs the executable material/source/readout/tau pack, not just the MICROSCOPE bound anchor.
- orbital tests need an acceleration projection that does not hide the residual inside fitted orbital GM.

## Source Register

| source_id | exists | role | status |
| --- | --- | --- | --- |
| SRC3011_00_3010_doc | True | parent checkpoint narrative and guardrails | PRESENT |
| SRC3011_01_3010_arena_matrix | True | 3010 arena handoff | PRESENT |
| SRC3011_02_3010_q_loc_interface | True | q_loc/Delta_K/coupling bound interface | PRESENT |
| SRC3011_03_R10_bound_contract_2702 | True | R10 bound curve digitization contract | PRESENT |
| SRC3011_04_R10_anchor_gate_2410 | True | R10 anchor-only admission gate | PRESENT |
| SRC3011_05_PPN_bound_interface_2513 | True | existing PPN comparator rows | PRESENT |
| SRC3011_06_PPN_normalized_inputs_1640 | True | PPN missing-input ledger | PRESENT |
| SRC3011_07_WEP_input_pack_1899 | True | WEP executable input pack ledger | PRESENT |
| SRC3011_08_clock_bound_fill_2675 | True | clock/species first-fill ledger | PRESENT |
| SRC3011_09_clock_tau_pack_2599 | True | clock tau source pack | PRESENT |
| SRC3011_10_clock_bound_import_1321 | True | clock bound import ledger | PRESENT |
| SRC3011_11_clock_alpha_sensitivity_646 | True | clock alpha sensitivity source ledger | PRESENT |
| SRC3011_12_orbit_template_1735 | True | PPN/WEP/clock/orbit source-pack template | PRESENT |
| SRC3011_13_measured_GM_guard_2513 | True | measured-GM no-absorb guard | PRESENT |
| SRC3011_14_GM_transfer_PiM_2595 | True | GM/source-normalization obstruction rows | PRESENT |

## Acquisition Matrix

| matrix_id | arena | observable | blocker_status | first_acquisition_row | priority |
| --- | --- | --- | --- | --- | --- |
| LAM3011_0_R10 | R10 short-range | alpha(lambda) | MISSING_FULL_CURVE_AND_QLOC_TO_YUKAWA_MAP | FNR3011_0_R10_2020_anchor_smoke; FNR3011_1_R10_2007_anchor_smoke; FNR3011_2_R10_full_curve_requirement | 1 |
| LAM3011_1_PPN | PPN | gamma-1; beta-1; alpha_i; zeta_i; xi | MISSING_K_PPN_AND_SOURCE_NORMALIZATION | FNR3011_3_PPN_comparator_smoke | 2 |
| LAM3011_2_clocks_EM | clocks/EM | redshift; clock drift; alpha_EM variation | MISSING_ALPHA_OWNER_AND_TAU_CLOCK_MAP | FNR3011_4_clock_alpha_smoke | 3 |
| LAM3011_3_WEP | WEP/composition | eta_AB; source/test composition residual | BOUND_ANCHOR_PRESENT_EXECUTABLE_INPUTS_MISSING | FNR3011_5_WEP_input_pack_smoke | 4 |
| LAM3011_4_orbital | orbital/source mass | extra acceleration; source-mass drift; orbital residuals | MISSING_ORBITAL_ACCELERATION_MAP_AND_GM_DENOMINATOR_OWNER | FNR3011_6_orbital_source_pack_smoke | 5 |
| LAM3011_5_total | all local arenas | local GR/Newton/PPN/WEP/R10 gate | TOTAL_LOCAL_CLAIM_BLOCKED | FNR3011_7_total_no_claim_guard | 6 |

## Required Source Files

| source_req_id | arena | current_status | units | next_action |
| --- | --- | --- | --- | --- |
| RSF3011_0_R10_full_curve | R10 short-range | MISSING_FULL_CURVE | lambda m; alpha dimensionless | digitize curve with figure/table provenance and extraction confidence |
| RSF3011_1_R10_anchor_smoke | R10 short-range | ANCHORS_PRESENT_NONCURVE | lambda m; alpha dimensionless | copy anchors only to smoke row ledger, not live claim file |
| RSF3011_2_R10_projection | R10 short-range | MISSING_QLOC_TO_YUKAWA_MAP | declared q_loc source units to dimensionless alpha | build R10 dry-run schema and fail closed when kernel/source normalization missing |
| RSF3011_3_PPN_bounds | PPN | COMPARATOR_PRESENT_NOT_MTS_PREDICTION | dimensionless | connect comparator to K_PPN kernel and measured-GM no-absorb guard |
| RSF3011_4_PPN_projection | PPN | MISSING_SOURCE_NORMALIZATION_AND_KERNELS | dimensionless residual vector plus source mass/frame metadata | derive or source K_PPN and source-normalization inputs |
| RSF3011_5_clock_pack | clocks/EM | MISSING_PARENT_ALPHA_OWNER_AND_TAU_CLOCK | yr^-1 or dimensionless per declared time coordinate | prove EM owner zero or source b_alpha and tau_clock_time |
| RSF3011_6_WEP_pack | WEP/composition | BOUND_ANCHOR_ONLY_INPUT_PACK_NOT_EXECUTABLE | dimensionless eta after acceleration normalization | fill WIP1899_1 through WIP1899_7 or theorem-reduce them |
| RSF3011_7_orbital_pack | orbital/source mass | TEMPLATE_PRESENT_EXECUTABLE_ROW_MISSING | m s^-2 or dimensionless fixed-GM vector | derive q_loc acceleration map and bind to measured-GM guard |

## Projection Quantities

| quantity_id | arena | symbol | current_status | required_units |
| --- | --- | --- | --- | --- |
| PQ3011_0_K_R10 | R10 short-range | K_R10(lambda,x) | MISSING_DERIVED_KERNEL | kernel units inverse to q_loc volume/source units, final alpha dimensionless |
| PQ3011_1_lambda_X | R10 short-range | lambda_X | MISSING_PARENT_RANGE_MAP | m |
| PQ3011_2_C_q_to_alpha | R10 short-range | C_q_to_alpha | MISSING_SOURCE_CHARGE_NORMALIZATION | dimensionless after declared source normalization |
| PQ3011_3_K_PPN | PPN | K_PPN^a_nu | MISSING_KERNEL_AND_GAUGE | dimensionless residual per q_loc unit |
| PQ3011_4_P_clock | clocks/EM | P_clock | MISSING_TAU_CLOCK_AND_ALPHA_OWNER | yr^-1 or dimensionless per clock observable |
| PQ3011_5_P_WEP_eta | WEP/composition | P_WEP_eta_AB | MISSING_MATERIAL_SOURCE_READOUT_MAPS | dimensionless eta |
| PQ3011_6_P_orbital | orbital/source mass | P_orbital_accel | MISSING_ACCELERATION_MAP | m s^-2 or declared dimensionless fixed-GM vector |
| PQ3011_7_total_no_cancellation | all local arenas | epsilon_local_total_abs | COMPONENTS_MISSING_TOTAL_BLOCKED | declared residual norm per arena |

## First Nonclaim Rows

| row_id | arena | row_type | status | blocker |
| --- | --- | --- | --- | --- |
| FNR3011_0_R10_2020_anchor_smoke | R10 short-range | bound_anchor_smoke | ANCHOR_ONLY_NON_CURVE | cannot interpolate arbitrary lambda/support from one threshold anchor |
| FNR3011_1_R10_2007_anchor_smoke | R10 short-range | bound_anchor_smoke | ANCHOR_ONLY_NON_CURVE | continuity anchor only; not modern dense bound curve |
| FNR3011_2_R10_full_curve_requirement | R10 short-range | required_full_curve | MISSING_FULL_CURVE | R10 scoring requires positive numeric curve rows and q_loc-to-alpha projection |
| FNR3011_3_PPN_comparator_smoke | PPN | comparator_bundle_smoke | COMPARATOR_PRESENT_NOT_MTS_PREDICTION | K_PPN/source normalization/no-cancellation vector missing |
| FNR3011_4_clock_alpha_smoke | clocks/EM | clock_bound_bundle_smoke | COMPARISON_SIDE_ONLY_NONCLAIM | b_alpha and tau_clock_time missing |
| FNR3011_5_WEP_input_pack_smoke | WEP/composition | WEP_input_pack_smoke | BOUND_ANCHOR_PRESENT_EXECUTABLE_INPUTS_MISSING | source/material/readout/tau/parent residual rows missing |
| FNR3011_6_orbital_source_pack_smoke | orbital/source mass | orbital_source_pack_smoke | TEMPLATE_PRESENT_EXECUTABLE_ROW_MISSING | acceleration map and denominator ownership missing |
| FNR3011_7_total_no_claim_guard | all local arenas | no_claim_guard | TOTAL_LOCAL_CLAIM_BLOCKED | component residuals not theorem-zero or source-backed numeric |

## Blocker Ledger

| blocker_id | arena | blocking_condition | unblocks_when |
| --- | --- | --- | --- |
| BLK3011_0_R10_curve | R10 short-range | MISSING_FULL_CURVE | dense source-backed alpha_bound(lambda) curve or official machine-readable table is present |
| BLK3011_1_R10_projection | R10 short-range | MISSING_QLOC_TO_YUKAWA_MAP | K_R10, lambda_X and C_q_to_alpha are derived or source-backed |
| BLK3011_2_PPN_kernel | PPN | MISSING_K_PPN_AND_GAUGE | K_PPN prediction rows exist in same source/frame/readout convention as comparator rows |
| BLK3011_3_clock_owner | clocks/EM | MISSING_ALPHA_OWNER_AND_TAU_CLOCK | no alpha_EM(X) vertex is proved or finite b_alpha and tau_clock_time rows are sourced |
| BLK3011_4_WEP_executability | WEP/composition | WIP1899_1_TO_WIP1899_7_MISSING | source/material/readout/force/tau/residual inputs are filled or theorem-reduced |
| BLK3011_5_orbital_GM | orbital/source mass | MISSING_ORBITAL_ACCELERATION_MAP_AND_GM_DENOMINATOR_OWNER | acceleration projection is derived and measured-GM absorption guard passes |
| BLK3011_6_total_no_cancellation | all local arenas | NO_CANCELLATION_ENVELOPE_NOT_NUMERIC | each retained component is theorem-zero or bounded in an absolute residual norm |

## Promotion Gates

| gate_id | gate | result | notes |
| --- | --- | --- | --- |
| GATE3011_0_source_register | all cited local source refs exist | True | 3011 only cites existing local ledgers as evidence; future targets may be missing artifacts |
| GATE3011_1_nonclaim_policy | every generated arena/input row remains nonclaim | True | 3011 is acquisition plumbing, not evidence of local-GR pass |
| GATE3011_2_R10_anchor_policy | R10 threshold anchors never become valid curve rows | True | anchors are preserved as smoke/provenance only |
| GATE3011_3_projection_required | no bound row is score-ready without same-arena projection quantities | True | matrix explicitly separates bound data from q_loc/Delta_K/coupling projection |
| GATE3011_4_GM_guard | orbital/PPN lanes cannot absorb residuals into fitted GM | True | 2513 measured-GM no-absorb guard is linked before any orbital/PPN score |
| GATE3011_5_local_claims | local GR/Newton/PPN/WEP/R10 pass allowed | False | component projections and full bound rows are still missing |

## Decision Ledger

| decision_id | decision | rationale |
| --- | --- | --- |
| DEC3011_0_status | 3011 converts 3010 into a source-acquisition matrix, not a claim. | The local bridge now has explicit q_loc/Delta_K/coupling interfaces, but every arena still lacks at least one required projection or source-backed bound artifact. |
| DEC3011_1_priority | R10 is selected as the first executable acquisition lane. | R10 has the cleanest observable target alpha(lambda), existing source hierarchy, and a well-defined curve-vs-anchor blocker. |
| DEC3011_2_PPN_second | PPN remains second because it is the real local-GR guardrail. | PPN catches fake GR recovery, but needs a source-frame/gauge kernel before it can score MTS. |
| DEC3011_3_total_branch | Total local-GR/Newton branch stays blocked until no-cancellation residual envelope is theorem-zero or numeric. | A serious field-theory claim cannot rest on cancellation between Delta_K, Ward, matter and readout terms. |

## Next Target

| next_id | target_doc | mission | success_condition |
| --- | --- | --- | --- |
| NEXT3011_0_3012 | 3012-Y5-R2FR-R10-first-source-backed-bound-rows-and-dryrun-schema-under-AX1090.md | Acquire or stage real source-backed R10 alpha_bound(lambda) rows and dry-run the q_loc-to-alpha schema while keeping all MTS prediction rows nonclaim unless parent coefficients are sourced. | full curve rows or an explicit blocker ledger exist; anchors remain valid_for_claim=false; dry-run refuses to score without K_R10, lambda_X and source normalization. |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3011_00_sources_exist | True | every cited local source path exists | P8_Y5_R2FR_3011_SOURCE_REGISTER.csv |
| VAL3011_01_csv_parse | True | generated CSV rows parse cleanly | all generated CSV artifacts import with csv.DictReader |
| VAL3011_02_r10_anchors_positive | True | anchor smoke rows have positive numeric lambda and alpha values | FNR3011_0 and FNR3011_1 |
| VAL3011_03_no_claim_rows | True | no 3011 row is valid for claim or claim allowed | base() claim fields |
| VAL3011_04_anchor_only_not_curve | True | R10 threshold anchors remain noncurve nonclaim rows | FNR3011_0 and FNR3011_1 |
| VAL3011_05_missing_markers_nonclaim | True | rows with MISSING markers are never valid_for_claim=true | first nonclaim row ledger |
| VAL3011_06_local_claims_blocked | True | local GR/Newton/PPN/WEP/R10 claim remains blocked | claim flags false across ledgers |
| VAL3011_07_outputs_scoped | True | no generated file is outside post-checkpoint-work | generated path scope check |
| VAL3011_08_formalization_not_targeted | True | formalization-workbench is not modified by this checkpoint | output target list excludes formalization-workbench |
| VAL3011_09_next_target_selected | True | next target selects R10 first source-backed acquisition | P8_Y5_R2FR_3011_NEXT_TARGET.csv |
| VAL3011_99_overall | True | all 3011 validation checks pass | aggregate of VAL3011_00 through VAL3011_09 |

## Files Written

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_LOCAL_BOUND_ACQUISITION_MATRIX.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_REQUIRED_SOURCE_FILES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_PROJECTION_QUANTITIES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_FIRST_NONCLAIM_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_ARENA_BLOCKER_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_PROMOTION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3011_BRANCH_COPIES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3011_VALIDATION.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_acquisition_matrix_3011_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\required_source_files_3011_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\first_nonclaim_local_rows_3011_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR3011_R10_FIRST_SOURCE_BACKED_BOUND_ROWS_NEXT_NONCLAIM.csv`

## Hard Guardrails Still Active

- No local-GR/Newton/PPN/WEP/R10 pass claim.
- No anchor-only R10 curve claim.
- No hidden-coupling cancellation.
- No bound inversion.
- No EH-only import.
- No orbital-GM denominator shortcut.
- No GitHub action.
- No `formalization-workbench` edits.
