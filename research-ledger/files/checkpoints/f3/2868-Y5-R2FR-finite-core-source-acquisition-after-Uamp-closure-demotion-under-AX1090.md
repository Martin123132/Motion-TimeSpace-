# 2868 - Y5 R2FR Finite Core Source Acquisition After U_amp Closure Demotion Under AX1090

Status: `Y5_R2FR_2868_finite_core_acquisition_pack_updated_runner_refused_corpus_scan_next`

## Private Verdict

2868 turns the post-2867 situation into an acquisition contract.

`U_amp` is useful closure machinery, but it is not a parent theorem in the current corpus. So it cannot be used as `theorem_zero_authority`, cannot fill `sigma_R_source_sign`, and cannot unlock `A_total`.

The finite route now requires a source-backed row set:

```text
first triplet: Q_CAB, q_R_eff, sigma_R_source_sign, shared Green convention
second layer: boundary/tail and measured GM glue
third layer: b_R/no-shadow plus full local residual vector
```

The strict runner template is deliberately still invalid. It contains missing values, missing source paths, missing conventions, and missing full-vector rows. This is a feature, not a bug: it prevents closure-only algebra from being laundered into an empirical claim.

The next useful move is not another proof gate. It is a corpus-wide scan/ranker for actual finite/source-backed rows, with exact source requests for anything still missing.

## Source Register

| source_id | role | path_exists | anchors_found | missing_anchors | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2868_0_2867_doc | 2867 demoted U_amp route and selected finite acquisition | True | True |  | False |
| SRC2868_1_2867_demotion | closure-only demotion ledger | True | True |  | False |
| SRC2868_2_2867_hessian | conditional Hessian law but no parent sigma | True | True |  | False |
| SRC2868_3_2867_next | handoff target | True | True |  | False |
| SRC2868_4_2867_validation | 2867 validation | True | True |  | False |
| SRC2868_5_2866_rollup | core amplitude blocker rollup | True | True |  | False |
| SRC2868_6_2865_blockers | sign/common Green/full-vector blockers | True | True |  | False |
| SRC2868_7_2864_blockers | q_R_eff blocker ledger | True | True |  | False |
| SRC2868_8_2863_blockers | Q_CAB blocker ledger | True | True |  | False |
| SRC2868_9_2862_requests | first-row source request pack | True | True |  | False |
| SRC2868_10_2862_rejections | semantic rejection rules | True | True |  | False |
| SRC2868_11_2861_scan | first row source scan | True | True |  | False |
| SRC2868_12_2861_accept | first row acceptance test | True | True |  | False |
| SRC2868_13_2860_doc | older finite acquisition pack | True | True |  | False |
| SRC2868_14_2860_pack | 2860 finite acquisition rows | True | True |  | False |
| SRC2868_15_2860_preflight | 2860 strict import refusal | True | True |  | False |
| SRC2868_16_2860_template | 2860 placeholder template | True | True |  | False |
| SRC2868_17_2860_validation | 2860 validation | True | True |  | False |
| SRC2868_18_2859_queue | fallback queue | True | True |  | False |
| SRC2868_19_2854_scan | real source acquisition scan | True | True |  | False |
| SRC2868_20_2854_blockers | real source blockers | True | True |  | False |
| SRC2868_21_script | 2868 generator self-check | True | True |  | False |

## Finite Core Acquisition Pack

| acquisition_id | quantity | required_object | minimum_value | current_blocker | priority | accepted_source_present | numeric_or_theorem_zero_present | ready_for_strict_runner | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACQ2868_0_Q_CAB | Q_CAB | finite target-map/source monopole | real number or parent-zero theorem in the shared radial convention | MISSING_PARENT_INPUT | first_triplet | False | False | False | False |
| ACQ2868_1_q_R_eff | q_R_eff | finite residual-curvature Green charge | real number or source-zero theorem in same convention as Q_CAB | MISSING_SOURCE_NORMALIZATION | first_triplet | False | False | False | False |
| ACQ2868_2_sigma_R_source_sign | sigma_R_source_sign | operator/Green/source sign | signed convention row, not profile sigma and not post-hoc cancellation sign | MISSING_OPERATOR_GREEN_SIGN_OWNER | first_triplet | False | False | False | False |
| ACQ2868_3_common_Green | shared Green/radial convention | same exterior normalization for C_AB and delta_R | one convention defining C_AB=Q_CAB/(4*pi*r)+... and delta_R=sigma*q_R_eff exp(-r/ell)/(4*pi*r)+... | MISSING_COMMON_GREEN_CONVENTION | first_triplet | False | False | False | False |
| ACQ2868_4_boundary_tail | K_amp/B_CAB/B_R/tail | boundary/improvement/tail row | zero/exact/included theorem or finite arena-projected bound | MISSING_SHARED_MEASURE_AND_BOUNDARY_CLASS | second_triplet | False | False | False | False |
| ACQ2868_5_measured_GM | M_source/GM | worldtube source measure and weak-field metric readout | same-frame measured GM denominator/source normalization | MISSING_GM_PARENT_GLUE | second_triplet | False | False | False | False |
| ACQ2868_6_b_R_or_no_shadow | b_R/no-shadow | profile leak coefficient or theorem-zero owner | finite coefficient or parent no-shadow theorem | MISSING_B_R_OR_NO_SHADOW_THEOREM | third_triplet | False | False | False | False |
| ACQ2868_7_full_local_vector | full PPN/local residual vector | same-branch local residual rows | finite/theorem rows for gamma,beta,preferred-frame,conservation,clock,orbital,q_loc,endpoint/readout | MISSING_FULL_VECTOR_CLOSURE | third_triplet | False | False | False | False |

## Source Row Schema

| schema_id | fields | requirement | purpose | field_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SCHEMA2868_0_identity | row_id;branch_id;arena_id | nonempty strings | identifies one branch and test arena | False | False |
| SCHEMA2868_1_Q_CAB | Q_CAB_value;Q_CAB_units;Q_CAB_source_path;Q_CAB_equation_anchor | finite numeric/theorem-zero with source | target-map numerator leg | False | False |
| SCHEMA2868_2_q_R_eff | q_R_eff_value;q_R_eff_units;q_R_eff_source_path;q_R_eff_equation_anchor;ell_R_value | finite numeric/theorem-zero with source | R-sector numerator leg | False | False |
| SCHEMA2868_3_sigma | sigma_R_source_sign;sign_convention;sigma_source_path;sigma_equation_anchor | signed source convention only | couples q_R_eff to Q_CAB | False | False |
| SCHEMA2868_4_green | common_green_convention;operator_pair;radial_4pi_convention | no MISSING markers | prevents sign/radial mismatch | False | False |
| SCHEMA2868_5_boundary_tail | boundary_policy;tail_bound;tail_source_path | zero/exact/included/finite bound | prevents hidden homogeneous modes | False | False |
| SCHEMA2868_6_GM | GM_value;GM_units;GM_source_path;GM_readout_convention | measured same-frame source denominator | normalizes PPN/local residuals | False | False |
| SCHEMA2868_7_full_vector | gamma;beta;alpha_i;xi;zeta_i;clock;orbital;q_loc;endpoint | finite/theorem-zero vector | prevents gamma-only local-GR claim | False | False |
| SCHEMA2868_8_claim_flags | control_only;score_ready;valid_prediction_row;valid_for_claim;claim_allowed | all false until every row passes | runner safety | False | False |

## Strict Runner Import Template

| row_id | branch_id | arena_id | Q_CAB_value | q_R_eff_value | sigma_R_source_sign | common_green_convention | boundary_policy | GM_value | full_vector_status | theorem_zero_authority | numeric_value_present | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAND2868_0_finite_core_import_template_nonclaim | R2FR_local_PPN_constant_limit_after_Uamp_closure_demotion | R10_PPN_CLOCK_ORBITAL_LOCAL_VECTOR | MISSING_Q_CAB | MISSING_q_R_eff | MISSING_sigma_R_source_sign | MISSING_COMMON_GREEN_CONVENTION | MISSING_BOUNDARY_POLICY | MISSING_GM | MISSING_FULL_LOCAL_VECTOR | UAMP_CLOSURE_ONLY_NOT_AUTHORITY | False | False |

## Row Readiness Preflight

| preflight_id | field | value_or_marker | requirement | preflight_passed | failure_reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PF2868_0_Q_CAB_value | Q_CAB_value | MISSING_Q_CAB | finite numeric or accepted theorem-zero | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_1_q_R_eff_value | q_R_eff_value | MISSING_q_R_eff | finite numeric or accepted theorem-zero | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_2_sigma_sign | sigma_R_source_sign | MISSING_sigma_R_source_sign | signed source convention | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_3_common_green | common_green_convention | MISSING_COMMON_GREEN_CONVENTION | shared radial/Green convention | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_4_boundary_tail | boundary_policy/tail_bound | MISSING_BOUNDARY_POLICY;MISSING_TAIL_BOUND | boundary zero/exact/included/finite tail | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_5_GM | GM_value | MISSING_GM | measured same-frame GM/source denominator | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_6_full_vector | full_vector_status | MISSING_FULL_LOCAL_VECTOR | full same-branch local residual vector | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_7_source_paths | all source paths | Q_CAB=blank;q_R_eff=blank;sigma=blank;tail=blank;GM=blank | existing source paths with anchors | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_8_claim_authority | theorem_zero_authority | UAMP_CLOSURE_ONLY_NOT_AUTHORITY | parent-signed theorem or finite rows only | False | MISSING_OR_CLOSURE_ONLY_INPUT | False |
| PF2868_OVERALL | strict_import_template | template remains placeholder-only after U_amp demotion | all finite source rows and conventions present | False | REFUSED_MISSING_PROVENANCE_OR_INPUTS | False |

## Test Arena Projection Requirements

| arena_id | arena | required_inputs | acceptable_output | status | arena_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ARENA2868_0_R10 | short-range fifth-force/R10 | Q_CAB,q_R_eff,sigma,common Green,ell_R,boundary/tail,source mass | alpha(lambda) row or theorem-zero residual | BLOCKED | False | False |
| ARENA2868_1_PPN | solar-system PPN | A_total,GM,b_R,boundary/full vector | gamma,beta,preferred-frame/conservation rows | BLOCKED | False | False |
| ARENA2868_2_clocks | clock/local time tests | clock residual row plus same branch GM/source convention | clock residual bound or theorem-zero | BLOCKED | False | False |
| ARENA2868_3_orbital | orbital dynamics | measured GM glue, endpoint/readout, preferred-frame vector | perihelion/range/residual rows | BLOCKED | False | False |
| ARENA2868_4_local_GR | full local GR/Newton reduction | all amplitude rows plus full local residual vector | no gamma-only pass; all channels closed | BLOCKED | False | False |

## Acceptance Gates

| gate_id | criterion | result | reason | gate_passed | guard_passed_nonclaim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| GATE2868_0_first_triplet | Q_CAB, q_R_eff and sigma_R_source_sign all source-backed in one convention | FAIL | all three remain missing/source-incomplete | False | False | False |
| GATE2868_1_common_green | common Green/radial/sign convention accepted | FAIL | 2865 common Green verdict is not accepted | False | False | False |
| GATE2868_2_boundary_tail | boundary/tail zero/exact/included or finite bound | FAIL | boundary/worldtube/tail inputs missing | False | False | False |
| GATE2868_3_measured_GM | measured same-frame GM/source denominator accepted | FAIL | GM parent glue remains conditional/open | False | False | False |
| GATE2868_4_full_vector | same-branch full local residual vector closed | FAIL | full vector missing | False | False | False |
| GATE2868_5_no_closure_loophole | U_amp closure-only route cannot substitute for finite rows | PASS_GUARD_ONLY | 2867 demotion blocks theorem-zero shortcut | False | True | False |
| GATE2868_6_runner | strict runner can score | FAIL | preflight refuses template | False | False | False |

## Runner Refusal

| runner_id | attempt | status | reason | runner_ready | score_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RUNREF2868_0_template | strict runner import template | REFUSED | contains MISSING_* markers and blank source paths | False | False | False |
| RUNREF2868_1_Uamp | U_amp closure-only authority | REFUSED | closure-only is not theorem-zero authority | False | False | False |
| RUNREF2868_2_sigma_profile | sigma_R_profile as source sign | REFUSED | profile import rejected by 2862/2865 | False | False | False |
| RUNREF2868_3_partial_triplet | score with only one or two numerator/sign rows | REFUSED | A_total needs all first triplet rows in one convention | False | False | False |
| RUNREF2868_4_local_GR | local GR/Newton claim | REFUSED | GM and full vector not closed | False | False | False |

## Source Priority Queue

| priority_id | rank | task | quantities | why_next | selected_for_next | claim_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRI2868_0_triplet_scan | 1 | corpus scan for first triplet | Q_CAB,q_R_eff,sigma_R_source_sign,common Green | needed before any A_total scoring | True | False | False |
| PRI2868_1_boundary_tail | 2 | boundary/tail source row | K_amp,B_CAB,B_R,H_R,C_AB_reg | prevents hidden homogeneous/tail residuals | False | False | False |
| PRI2868_2_GM | 3 | measured GM glue | M_source,GM,H_tau,metric 1/r readout | needed for PPN/Newton normalization | False | False | False |
| PRI2868_3_full_vector | 4 | full local vector | beta,preferred,conservation,clock,orbital,q_loc,endpoint | needed to avoid gamma-only claim | False | False | False |
| PRI2868_4_empirical_runner | 5 | strict runner smoke only after rows pass | A_total/R10/PPN/local vector | testing step after source-backed rows | False | False | False |

## Decision Ledger

| decision_id | decision | result | because | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2868_0_post_demotion | U_amp closure-only status is now enforced in finite acquisition. | CARRIED_FORWARD | the closure route cannot unlock theorem-zero or runner scoring | False |
| DEC2868_1_pack | Finite source acquisition pack is updated for post-2867 requirements. | COMPLETE_NONCLAIM | Q_CAB, q_R_eff, sigma, common Green, boundary/tail, GM and full vector are all explicit rows | False |
| DEC2868_2_runner | Strict runner remains refused. | LOCKED | template contains placeholders and missing provenance | False |
| DEC2868_3_next | Next step is automated corpus scan/ranking for real finite rows. | SELECTED_2869 | we need actual source-backed rows, not another abstract gate | False |

## Next Target

| next_id | status | target_doc | target_script | mission | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2868_0_2869 | selected_primary | 2869-Y5-R2FR-core-finite-row-corpus-scan-and-source-request-under-AX1090.md | scripts/Y5_R2FR_core_finite_row_corpus_scan_and_source_request_under_AX1090_2869.py | scan the current corpus for actual finite/source-backed rows for Q_CAB, q_R_eff, sigma_R_source_sign, common Green convention, boundary/tail, measured GM and full local vector; rank candidates, reject placeholders/profile imports/Uamp closure authority, and emit exact source requests for any still-missing rows | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2868_0_acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2868_FINITE_CORE_ACQUISITION_PACK.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\RAB_FINITE_CORE_ACQUISITION_PACK_2868_NONCLAIM.csv | finite core acquisition pack nonclaim copy | True | False |
| COPY2868_1_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2868_RUNNER_REFUSAL.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\RAB_STRICT_RUNNER_REFUSAL_2868_NONCLAIM.csv | strict runner refusal nonclaim copy | True | False |
| COPY2868_2_next_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2868_NEXT_TARGET.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2868_core_finite_row_corpus_scan_NEXT.csv | RAB queue handoff to 2869 corpus scan | True | False |
| COPY2868_3_arena | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2868_TEST_ARENA_PROJECTION_REQUIREMENTS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\RAB_TEST_ARENA_PROJECTION_REQUIREMENTS_2868_NONCLAIM.csv | test arena projection requirements nonclaim copy | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2868_0_sources_exist | True | all registered source paths exist | 2026-06-24T14:07:35.841022+00:00 |
| VAL2868_1_source_anchors | True | all registered anchors were found | 2026-06-24T14:07:35.841033+00:00 |
| VAL2868_2_acquisition_covers_core | True | acquisition pack covers core triplet, common Green, boundary/tail, GM and full vector | 2026-06-24T14:07:35.841036+00:00 |
| VAL2868_3_schema_written | True | strict finite source row schema written | 2026-06-24T14:07:35.841039+00:00 |
| VAL2868_4_template_nonclaim | True | runner template remains placeholder/nonclaim | 2026-06-24T14:07:35.841042+00:00 |
| VAL2868_5_preflight_refuses | True | preflight rejects every missing input | 2026-06-24T14:07:35.841044+00:00 |
| VAL2868_6_arena_blocked | True | all test arenas remain blocked until finite rows exist | 2026-06-24T14:07:35.841047+00:00 |
| VAL2868_7_gates_fail_closed | True | acceptance gates fail closed | 2026-06-24T14:07:35.841049+00:00 |
| VAL2868_8_runner_refused | True | strict runner remains refused | 2026-06-24T14:07:35.841052+00:00 |
| VAL2868_9_next_target_2869 | True | core finite row corpus scan selected next | 2026-06-24T14:07:35.841054+00:00 |
| VAL2868_10_outputs_exist | True | all generated output paths exist before validation write | 2026-06-24T14:07:35.841057+00:00 |
| VAL2868_11_branch_outputs_exist | True | branch copies were written | 2026-06-24T14:07:35.841059+00:00 |
| VAL2868_12_csv_parse | True | all generated CSV outputs parse | 2026-06-24T14:07:35.841061+00:00 |
| VAL2868_13_cited_paths_exist | True | all cited local file/copy paths in generated rows exist | 2026-06-24T14:07:35.841064+00:00 |
| VAL2868_14_no_claim_flags | True | no claim/score/prediction flags are true | 2026-06-24T14:07:35.841066+00:00 |
| VAL2868_15_generated_under_post_checkpoint | True | all generated artifacts remain under post-checkpoint-work | 2026-06-24T14:07:35.841069+00:00 |
| VAL2868_16_formalization_untouched | True | formalization-workbench was not modified during this run | 2026-06-24T14:07:35.841071+00:00 |
| VAL2868_17_pycache_absent | True | scripts __pycache__ absent during validation | 2026-06-24T14:07:35.841073+00:00 |
| VAL2868_OVERALL | True | 2868 updates the finite core source acquisition pack after U_amp closure demotion, refuses the strict runner, keeps every local-test arena blocked, and selects a corpus-wide finite-row scan for 2869. | 2026-06-24T14:07:35.841080+00:00 |
