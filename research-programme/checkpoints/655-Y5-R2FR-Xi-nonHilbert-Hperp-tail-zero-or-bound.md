# 4639 — Xi_nonHilbert/Hperp tail zero or bound

Marker: `PPC4161_XI_NONHILBERT_HPERP_TAIL_ZERO_OR_BOUND_4639`

## Result

4639 imports the older `N_src_nonHilbert/Hperp` theorem into the current 4638 R10 tail. The current tail is

`Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner`.

The second component is now given a sharp route:

`Xi_nonHilbert := K_NH N_src_nonHilbert`,

with

`H_L = H_q + Hperp`, `H_q in ker(Dq)`, `Hperp=(1-Pi_kerDq)H_L`,

and

`S_cg_nonHilbert = S_A Hperp^A + R_src_readout`.

Therefore, if `Hperp=0` or `S_A Hperp^A=0`, and `R_src_readout=0`, then `Xi_nonHilbert=0`. If not, the finite branch is

`|Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)`.

This is progress, not a claim: `K_NH`, the Hperp component certificates, `R_src_readout`, and the Noether/improvement flux clauses remain unsigned.

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | line | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4639 | SRC4639_00_4638_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4638_VALIDATION.csv | True | VAL4638_OVERALL | True | 18 | 4638 validation. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_01_4638_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4638_XI_TAIL_REDUCTION_ROWS.csv | True | XR4638_2_reduced_tail | True | 4 | current four-component Xi_tail gate. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_02_4638_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md | True | Xi_tail := Xi_src_hidden + Xi_nonHilbert | True | 25 | human-readable reduced tail. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_03_4318_priority | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md | True | P4318_1 | True | 66 | old ladder selected N_src_nonHilbert/Hperp first. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_04_4318_canon | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md | True | NR4318_0_Nsrc | True | 43 | canonical N_src_nonHilbert row. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_05_4319_marker | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md | True | PPC4161_NONHILBERT_HPERP_SOURCE_SUPPORT_ZERO_OR_BOUND_ROW_4319 | True | 3 | Hperp source-support zero/bound theorem. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_06_4319_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md | True | TH4319_3_exact_zero | True | 53 | exact N_src_nonHilbert zero branch. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_07_4319_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md | True | F4319_5_bound | True | 88 | finite Dq/Hperp source-support bound. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_08_4320_source_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md | True | Dq_source_readout[Hperp] | True | 15 | highest-leverage Dq component. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_09_4320_Nsrc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md | True | F4320_1_Nsrc | True | 65 | N_src finite formula handoff. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_10_4431_nonHilbert_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md | True | NH4431_0_nonHilbert_zero_theorem | True | 44 | Noether/improvement zero theorem. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_11_4431_current_gap | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md | True | NH4431_1_current_gap | True | 45 | current non-Hilbert gap retained. | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | SRC4639_12_4635_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv | True | lambda_m | True | 1 | R10 vector curve points. | False | 2026-07-06T19:39:56.759405+00:00 |

## Import audit

| checkpoint | audit_id | input | mapped_to_current_tail | status | law | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4639 | AUD4639_0_object_map | N_src_nonHilbert from 4318/4319 | Xi_nonHilbert | MAPPED_AS_DIMENSIONLESS_PROJECTED_SOURCE_BYPASS | Xi_nonHilbert := K_NH N_src_nonHilbert with K_NH the current R10 projection normalization | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | AUD4639_1_exact_zero | TH4319_3_exact_zero | Xi_nonHilbert=0 | CONDITIONAL_ZERO_AVAILABLE | Hperp=0 or S_A Hperp^A=0, and R_src_readout=0 => N_src_nonHilbert=0 => Xi_nonHilbert=0 | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | AUD4639_2_finite_bound | F4319_5_bound / F4320_1_Nsrc | |Xi_nonHilbert| bound | BOUND_ROUTE_READY_INPUTS_MISSING | |Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||) | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | AUD4639_3_noether_bypass | NH4431_0_nonHilbert_zero_theorem / NH4431_1_current_gap | Noether/improvement bypass risk | EXACT_THEOREM_STAGED_BUT_UNSIGNED | owned exact improvements with zero compact projected flux cannot source Xi_nonHilbert; spin/boundary/readout/flux pieces remain open | False | False | 2026-07-06T19:39:56.759405+00:00 |

## Formula rows

| checkpoint | formula_id | formula | basis | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4639 | F4639_0_quotient_split | H_L = H_q + Hperp, H_q in ker(Dq), Hperp=(1-Pi_kerDq)H_L | 4319 Hperp strip | IMPORTED | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | F4639_1_source_pairing | S_cg_nonHilbert = S_A Hperp^A + R_src_readout | 4319 source-pairing split | IMPORTED | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | F4639_2_exact_zero | if Hperp=0 or S_A Hperp^A=0, and R_src_readout=0, then Xi_nonHilbert=0 | TH4319_3_exact_zero plus current Xi projection | CONDITIONAL_ZERO_NOT_GLOBAL_CLAIM | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | F4639_3_finite_bound | |Xi_nonHilbert| <= K_NH ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||) | F4319_5_bound/F4320_1_Nsrc with dimensionless R10 projection K_NH | BOUND_READY_KNH_AND_COMPONENT_VALUES_MISSING | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | F4639_4_reduced_tail_after_zero | if Xi_src_hidden=0 and Xi_nonHilbert=0, then Xi_tail := Xi_boundary_history + Xi_transition_inner | 4638 reduced tail plus 4639 zero branch | CONDITIONAL_REDUCTION_ONLY | False | False | 2026-07-06T19:39:56.759405+00:00 |

## Hperp/Dq component status

| checkpoint | component_id | component | role | current_status | zero_gate | bound_gate | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4639 | HC4639_0 | Dq_source_readout[Hperp] | highest leverage because it feeds both E_Dq,Hperp and R_src_readout | MISSING_PARENT_SIGNATURE | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_1 | Dq_geom[Hperp] | geometry/coframe descent component | PROFILE_ROUTE_AVAILABLE_VALUES_MISSING | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_2 | Dq_EM[Hperp] | EM/Hodge/current descent component | ROUTE_AVAILABLE_VALUES_MISSING | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_3 | Dq_tau[Hperp] | clock/reference-time descent component | ROUTE_OPEN | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_4 | Dq_matter[Hperp] | matter action descent component | ROUTE_OPEN | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_5 | Dq_boundary_projector[Hperp] | boundary/projector ownership component | ROUTE_OPEN | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_6 | Dq_theta_marker[Hperp] | marker/selector component | ROUTE_OPEN | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | HC4639_7 | Dq_coeff[Hperp] | coefficient/normalization component | ROUTE_OPEN | Dq_i[Hperp]=0 from parent quotient/factorization certificate | epsilon_i >= ||Dq_i[Hperp]|| feeds E_Dq,Hperp | False | False | 2026-07-06T19:39:56.759405+00:00 |

## Tail reduction rows

| checkpoint | row_id | definition | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4639 | XR4639_0_input_from_4638 | Xi_tail := Xi_src_hidden + Xi_nonHilbert + Xi_boundary_history + Xi_transition_inner | INPUT_FROM_4638 | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | XR4639_1_nonHilbert_zero_branch | if Hperp=0 or S_A Hperp^A=0, and R_src_readout=0, then Xi_nonHilbert=0 | CONDITIONAL_ZERO_ROUTE_IMPORTED | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | XR4639_2_reduced_tail_after_two_zeros | if Xi_src_hidden=0 and Xi_nonHilbert=0, then Xi_tail := Xi_boundary_history + Xi_transition_inner | TWO_COMPONENT_REDUCTION_CONDITIONAL | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | XR4639_3_finite_gate | |Xi_src_hidden| + |Xi_nonHilbert| + |Xi_boundary_history| + |Xi_transition_inner| <= alpha_bound(lambda_mem) | R10_GATE_RETAINS_NONCANCELLATION | False | False | 2026-07-06T19:39:56.759405+00:00 |

## R10 reduced-tail smoke runner

| checkpoint | run_id | branch | lambda_mem_m | Xi_src_hidden_abs | Xi_nonHilbert_abs | Xi_boundary_history_abs | Xi_transition_inner_abs | Xi_tail_abs | alpha_bound_vector | result | reason | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4639 | RUN4639_0_live_missing_inputs | current live corpus |  |  |  |  |  |  |  | FAIL_CLOSED | missing source-backed K_NH, Hperp/Dq values, remaining tail values and lambda_mem | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | RUN4639_1_two_component_zero_control | Xi_src_hidden and Xi_nonHilbert zero | 0.0001 | 0 | 0 | 0 | 0 | 0 | 0.0755863083618 | SMOKE_PASS_NONCLAIM | absolute reduced tail sits inside digitized vector bound for this toy/control row | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | RUN4639_2_nonHilbert_pass_100um | finite non-Hilbert smoke | 0.0001 | 0 | 0.04 | 0 | 0 | 0.04 | 0.0755863083618 | SMOKE_PASS_NONCLAIM | absolute reduced tail sits inside digitized vector bound for this toy/control row | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | RUN4639_3_nonHilbert_fail_100um | finite non-Hilbert smoke | 0.0001 | 0 | 0.08 | 0 | 0 | 0.08 | 0.0755863083618 | SMOKE_FAIL_NONCLAIM | absolute reduced tail exceeds digitized vector bound | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | RUN4639_4_boundary_transition_pass_200um | after two zeros, remaining pair smoke | 0.0002 | 0 | 0 | 0.02 | 0.01 | 0.03 | 0.0315709160515 | SMOKE_PASS_NONCLAIM | absolute reduced tail sits inside digitized vector bound for this toy/control row | False | False | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | RUN4639_5_boundary_transition_fail_200um | after two zeros, remaining pair smoke | 0.0002 | 0 | 0 | 0.02 | 0.02 | 0.04 | 0.0315709160515 | SMOKE_FAIL_NONCLAIM | absolute reduced tail exceeds digitized vector bound | False | False | 2026-07-06T19:39:56.759405+00:00 |

## Claim blockers

| checkpoint | blocker_id | blocker | detail | blocks_claim | next_action | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4639 | BLK4639_0 | MISSING_K_NH_PROJECTION | dimensionless map from N_src_nonHilbert to Xi_nonHilbert is not source-backed | True | retain in non-Hilbert source ledger | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | BLK4639_1 | MISSING_HPERP_ZERO_OR_COMPONENT_VALUES | Dq_i[Hperp] component zeros/epsilons are not parent-signed | True | retain in non-Hilbert source ledger | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | BLK4639_2 | MISSING_R_SRC_READOUT_ZERO_OR_BOUND | R_src_readout remains an explicit source-readout residual | True | retain in non-Hilbert source ledger | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | BLK4639_3 | NONHILBERT_NOETHER_FLUX_GAPS | spin/boundary/readout/improvement compact flux pieces remain open | True | retain in non-Hilbert source ledger | 2026-07-06T19:39:56.759405+00:00 |
| 4639 | BLK4639_4 | REMAINING_XI_BOUNDARY_TRANSITION | Xi_boundary_history and Xi_transition_inner remain live after the conditional two-component reduction | True | 4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md | 2026-07-06T19:39:56.759405+00:00 |

## Decision

| checkpoint | decision_id | decision | selected_next_target | claim_allowed | reason | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4639 | DEC4639_0 | XI_NONHILBERT_REDUCED_TO_HPERP_SOURCE_PAIRING_ZERO_OR_BOUND_NONCLAIM | 4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md | False | Xi_nonHilbert now has a concrete exact-zero or finite-bound route, but its parent signatures and the remaining boundary/transition pair remain open | 2026-07-06T19:39:56.759405+00:00 |

## Validation

| checkpoint | validation_id | status | detail | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4639 | VAL4639_0_sources_exist | PASS | all cited source paths exist | 2026-07-06T19:39:56.932770+00:00 |
| 4639 | VAL4639_1_needles_found | PASS | all cited source needles are present | 2026-07-06T19:39:56.932782+00:00 |
| 4639 | VAL4639_2_Xi_map | PASS | N_src_nonHilbert mapped to Xi_nonHilbert | 2026-07-06T19:39:56.932785+00:00 |
| 4639 | VAL4639_3_exact_zero_imported | PASS | Hperp exact zero branch imported | 2026-07-06T19:39:56.932788+00:00 |
| 4639 | VAL4639_4_bound_formula_present | PASS | finite Xi_nonHilbert bound formula present | 2026-07-06T19:39:56.932791+00:00 |
| 4639 | VAL4639_5_component_matrix_present | PASS | all eight Hperp/Dq components listed | 2026-07-06T19:39:56.932794+00:00 |
| 4639 | VAL4639_6_two_component_reduction | PASS | two-component tail reduction row present | 2026-07-06T19:39:56.932797+00:00 |
| 4639 | VAL4639_7_runner_live_fail_closed | PASS | live missing-input row fails closed | 2026-07-06T19:39:56.932800+00:00 |
| 4639 | VAL4639_8_runner_has_pass_and_fail_controls | PASS | runner has pass and fail controls | 2026-07-06T19:39:56.932802+00:00 |
| 4639 | VAL4639_9_all_generated_rows_nonclaim | PASS | generated theory rows remain nonclaim | 2026-07-06T19:39:56.932805+00:00 |
| 4639 | VAL4639_10_doc_marker | PASS | post-checkpoint doc marker present | 2026-07-06T19:39:56.932808+00:00 |
| 4639 | VAL4639_11_formal_marker | PASS | formal checkpoint marker present | 2026-07-06T19:39:56.932810+00:00 |
| 4639 | VAL4639_12_claim_registered | PASS | claim row registered | 2026-07-06T19:39:56.932813+00:00 |
| 4639 | VAL4639_13_spine_marker | PASS | spine marker appended | 2026-07-06T19:39:56.932815+00:00 |
| 4639 | VAL4639_14_packet_marker | PASS | packet marker appended | 2026-07-06T19:39:56.932818+00:00 |
| 4639 | VAL4639_15_public_stage_clean | PASS | public stage not modified | 2026-07-06T19:39:56.932820+00:00 |
| 4639 | VAL4639_16_backup_repo_clean | PASS | backup repo not modified | 2026-07-06T19:39:56.932823+00:00 |
| 4639 | VAL4639_OVERALL | PASS | 4639 validation passed | 2026-07-06T19:39:56.932830+00:00 |
