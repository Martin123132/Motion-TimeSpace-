# 4696 - Retained Bulk Source Current With 4695 EM/Poynting Insertion

Marker: `PPC4161_RETAINED_BULK_SOURCE_CURRENT_BRANCH_4696`

Claim register: `L-538`

Generated UTC: `2026-07-07T19:28:46+00:00`

## Result
This checkpoint does **not** claim local GR. It takes the retained source-current split seriously and inserts the new 4695 EM/Poynting gate into the memory component:

```text
J_retained = J_direct + J_mem + J_marker + J_readout
```

with

```text
|J_mem^EM_open| <= C_EM_source W_lambda_max(
  M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall|
  + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|
) / |M_H_ref|.
```

So Poynting is now placed exactly: ordinary Maxwell Poynting belongs to Hilbert EM stress; only a named wall-flux/nonminimal/source coefficient remains as retained current.

## Source Register
| checkpoint | source_id | source_path | path_exists | needle | needle_found | source_line | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | SRC4696_00_4695_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_STATUS.csv | True | PPC4161_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695 | True | 2 | 4695 current EM/Poynting gate. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_01_4695_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_NEXT_TARGET.csv | True | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | True | 2 | 4695 selects retained-current as next target. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_02_4695_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4695_VALIDATION.csv | True | VAL4695_OVERALL | True | 27 | 4695 validation passed. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_03_4695_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv | True | EMF4695_3_finite_EM_bound | True | 5 | 4695 finite EM/Poynting bound. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_04_4695_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_EM_BULK_BOUND_UPDATE_ROWS.csv | True | EB4695_1_bound_route | True | 3 | 4695 EM bulk update row. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_05_4695_flux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv | True | FX4695_1_wall_flux_bound | True | 3 | 4695 Poynting wall flux bound. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_06_4695_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_CLAIM_BLOCKERS.csv | True | MIS4695_1_wall_flux | True | 3 | 4695 keeps wall flux as live input if unsigned. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_07_4608_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_RETAINED_BULK_SOURCE_CURRENT_THEOREM.csv | True | RET4608_0_decomposition | True | 2 | 4608 retained current decomposition. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_08_4608_direct | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_JDIRECT_ROWS.csv | True | JD4608_0_total | True | 2 | 4608 direct current row. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_09_4608_memory | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_JMEM_ROWS.csv | True | JM4608_1_EM_open | True | 3 | 4608 memory EM-open row. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_10_4608_marker | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_JMARKER_ROWS.csv | True | JMK4608_0_total | True | 2 | 4608 marker row. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_11_4608_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_JREADOUT_ROWS.csv | True | JR4608_0_total | True | 2 | 4608 readout row. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_12_4608_qbulk | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_QBULK_RETAINED_UPDATE_ROWS.csv | True | QBR4608_0_retained | True | 2 | 4608 retained bulk update. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_13_4608_controls | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_CONTROL_ROWS.csv | True | CTRL4608_2_poynting_not_hidden | True | 4 | 4608 control against hiding Poynting. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_14_4608_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_NEXT_TARGET.csv | True | 4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md | True | 2 | 4608 next target. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_15_4608_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4608_VALIDATION.csv | True | VAL4608_OVERALL | True | 20 | 4608 validation passed. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_16_formal624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | True | J_retained := J_direct | True | 14 | formal retained-current addendum. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SRC4696_17_formal711 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\711-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md | True | \|Q_bulk_EM/Poynting\| <= W_lambda_max | True | 27 | formal 4695 EM/Poynting bound. | False | 2026-07-07T19:28:46+00:00 |

## Retained Theorem Rows
| checkpoint | theorem_id | component | derived_relation | zero_condition | fallback_bound | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | RET4696_0_decomposition | retained bulk source current | J_retained := J_direct+J_mem+J_marker+J_readout | J_direct=J_mem=J_marker=J_readout=0 in the same parent branch | \|Q_bulk_retained\| <= W_lambda_max(\|J_direct_abs\|+\|J_mem_abs\|+\|J_marker_abs\|+\|J_readout_abs\|) | DERIVED_DECOMPOSITION_NO_CANCELLATION | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | RET4696_1_direct | J_direct | J_direct=0 follows if the parent object language has no non-Hilbert direct source slot, no source-only weights, one action-scale owner and no hidden marker return. | GATE2508_0 through GATE2508_6 pass plus SCI2642_2 non-Hilbert channels vanish | \|J_direct\| <= \|J_nonHilbert\|+\|epsilon_wA_source_weight\|+\|epsilon_kappaA_source\|+\|epsilon_action_scale\|+\|epsilon_noHom\|+\|epsilon_hidden_marker\| | CONDITIONAL_ZERO_COUNTERMODELS_RETAINED | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | RET4696_2_memory | J_mem | J_mem_live = J_mem^EM_open+J_mem^nonHilbert+J_mem^dyn_exchange+J_mem^boundary_readout after source-kernel silence. | strict source-kernel branch, EM/Poynting no-flux, no retained non-Hilbert current, stationary exchange closure and boundary/readout neutrality | \|J_mem\| <= \|J_mem^EM_open\|+\|J_mem^nonHilbert\|+\|J_mem^dyn_exchange\|+\|J_mem^boundary_readout\| | REDUCED_MEMORY_VECTOR_NOT_CLOSED | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | RET4696_3_marker | J_marker | J_marker=0 only if fixed spurions, material constants, common/disformal frames, alpha/clock constants and source-boundary tails are quotient-owned or absent. | NMT1850 no-marker theorem plus no source-boundary tail and no hidden marker Hom | \|J_marker\| <= \|epsilon_hidden_marker\|+\|b_A\|+\|b_alpha\|+\|c_g\|+\|b_dis\|+\|q_source_boundary_tail\| | MARKER_ZERO_NOT_CLOSED_COMPONENT_ROWS_READY | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | RET4696_4_readout | J_readout | J_readout=0 if readout is pure post-solution reporting, absent from S_parent and forbidden to re-enter through reduced EFT, projector, worldtube, material or calibration maps. | variation-before-readout plus parent-domain exclusion of readout/projector/source-worldtube re-entry | J_readout <= J_PiM_comm+J_Ploc_comm+J_worldtube_comm+J_material_comm+J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint | CONDITIONAL_POSTPROCESSING_ZERO_PARENT_DOMAIN_UNSIGNED | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | RET4696_5_bulk_update | Q_bulk retained insertion | Q_bulk_abs <= Q_bulk_Hilbert_abs+Q_bulk_EM/Poynting_abs+Q_bulk_retained_abs with Q_bulk_retained_abs sourced by the four retained tails. | ordinary Hilbert, EM/Poynting and all retained tails vanish in the same parent branch | \|Q_bulk_retained\| <= W_lambda_max(\|J_direct_abs\|+\|J_mem_abs\|+\|J_marker_abs\|+\|J_readout_abs\|) | BULK_RETAINED_UPDATE_READY_NONCLAIM | False | False | 2026-07-07T19:28:46+00:00 |

## 4695 EM Memory Insertion
| checkpoint | row_id | quantity | derived_relation | 4695_bound_inserted | zero_condition | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | JME4696_0_4695_insertion | J_mem_EM_open_abs | \|J_mem^EM_open\| <= C_EM_source/M_H_ref * \|Q_bulk_EM/Poynting\|_4695 | \|J_mem^EM_open\| <= C_EM_source W_lambda_max(M_ref\|Delta_Hodge_EM\|+\|c_Poynt_extra Phi_wall\|+\|Phi_wall_Poynting\|+M_ref\|epsilon_nonminimal_EM\|)/\|M_H_ref\| | same-Hodge Maxwell branch, c_Poynt_extra=0, stationary no-wall-flux collar, epsilon_nonminimal_EM=0 and source-coupling projection finite in the same parent branch | EM_MEMORY_COMPONENT_REDUCED_TO_4695_HODGE_FLUX_INPUTS_VALUES_MISSING | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | JME4696_1_no_double_count | Poynting_placement_control | Ordinary Poynting flux is counted either as Hilbert EM stress/Q_bulk_EM or as an explicit retained nonminimal/source flux term, never both. | If it is ordinary Maxwell stress, use EB4695_1; if it is nonminimal/source-tail flux, keep it under J_mem or epsilon_nonminimal_EM with a named coefficient. | one stress/source owner and no hidden reduced-action feedback | NO_DOUBLE_COUNT_CONTROL_ACTIVE | False | False | 2026-07-07T19:28:46+00:00 |

## Updated Retained Bulk Bound
| checkpoint | row_id | quantity | update_formula | zero_condition | required_inputs | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | QBR4696_0_retained_with_4695_EM | Q_bulk_retained_abs | \|Q_bulk_retained\| <= W_lambda_max(\|J_direct\|+\|J_marker\|+\|J_readout\|+\|J_mem_nonHilbert\|+\|J_mem_dyn_exchange\|+\|J_mem_boundary_readout\|+C_EM_source(M_ref\|Delta_Hodge_EM\|+\|c_Poynt_extra Phi_wall\|+\|Phi_wall_Poynting\|+M_ref\|epsilon_nonminimal_EM\|)/\|M_H_ref\|) | all retained components and the 4695 EM/Hodge/flux/nonminimal inputs vanish in the same parent branch | J_direct_abs;J_marker_abs;J_readout_abs;J_mem_nonHilbert_abs;J_mem_dyn_exchange_abs;J_mem_boundary_readout_abs;Delta_Hodge_EM_abs;Phi_wall_Poynting_abs;epsilon_nonminimal_EM;C_EM_source;M_H_ref;W_lambda_max | RETAINED_BOUND_TIGHTENED_WITH_4695_EM_INSERTION_VALUES_MISSING | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | QBR4696_1_bulk_total | Q_bulk_abs | \|Q_bulk\| <= \|Q_bulk_Hilbert\|+\|Q_bulk_EM/Poynting\|+\|Q_bulk_retained\| | Hilbert, EM/Poynting and retained bulk tails vanish in the same branch | 4694 Hilbert rows;4695 EM/Poynting rows;4696 retained rows | QBULK_TOTAL_STILL_NONCLAIM | False | False | 2026-07-07T19:28:46+00:00 |
| 4696 | QBR4696_2_QbarXH | Qbar_XH_abs | \|Qbar_XH\| <= (\|\|Pi_M^H\|\|(\|Q_bulk\|+\|Q_edge\|+\|Q_shadow\|)+\|E_PiM_comm\|)/M_lower | bulk retained plus edge/shadow plus denominator/projector commute and vanish | Q_bulk_abs;Q_edge_abs;Q_shadow_abs;Pi_M norm;E_PiM_comm;M_lower | QBARXH_STILL_BLOCKED_BY_EDGE_SHADOW_AND_DENOMINATOR | False | False | 2026-07-07T19:28:46+00:00 |

## Survivors
| checkpoint | survivor_id | object | meaning | status | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | SURV4696_0_direct | J_direct_abs | direct non-Hilbert/source-weight/action-scale current | source-slot theorem or finite coefficient still needed | prove no source-only object language or fill absolute coefficient row | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SURV4696_1_memory_EM | J_mem_EM_open_abs | retained memory current sourced by EM/Poynting flux after 4695 insertion | reduced to Delta_Hodge_EM/Phi_wall_Poynting/epsilon_nonminimal_EM inputs | prove same-Hodge stationary collar or source those finite inputs | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SURV4696_2_memory_nonEM | J_mem_nonHilbert_abs+J_mem_dyn_exchange_abs+J_mem_boundary_readout_abs | non-EM memory source tails | symbolic values missing | close non-Hilbert/dynamic/boundary readout source-current clauses | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SURV4696_3_marker | J_marker_abs | material/frame/constant/source-boundary marker source current | no-marker theorem not closed | prove quotient ownership of material constants/frames or bound marker coefficients | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SURV4696_4_readout | J_readout_abs | post-solution readout/projector/worldtube/material/EFT/calibration re-entry | parent-domain exclusion not fully signed | turn readout schema into parent-domain certificate or source finite components | False | 2026-07-07T19:28:46+00:00 |
| 4696 | SURV4696_5_next_numerator | Q_edge_abs | source worldtube/boundary shell flux numerator after retained bulk is named | next live source-side numerator | 4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md | False | 2026-07-07T19:28:46+00:00 |

## Blockers
| checkpoint | blocker_id | missing_object | why_it_matters | best_next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4696 | MIS4696_0_same_branch | same-branch zero certificate for J_direct, J_mem, J_marker and J_readout | retained-current cancellation is forbidden, so one live component keeps Q_bulk_retained live | prove all retained components vanish under the same parent assumptions or keep absolute bound rows | False | 2026-07-07T19:28:46+00:00 |
| 4696 | MIS4696_1_EM_inputs | Delta_Hodge_EM, Phi_wall_Poynting, epsilon_nonminimal_EM and C_EM_source | 4695 converts Poynting intuition into named finite inputs; it does not erase them | prove same-Hodge stationary collar or source finite coefficients | False | 2026-07-07T19:28:46+00:00 |
| 4696 | MIS4696_2_direct_marker_readout | parent-owned no-source-slot, no-marker and readout-exclusion certificates | these are the remaining places source coupling can hide after Hilbert/EM cleanup | derive parent-domain exclusion clauses or fill nonclaim coefficient rows | False | 2026-07-07T19:28:46+00:00 |
| 4696 | MIS4696_3_downstream | Q_edge, Q_shadow, denominator/projector, qbar_XT and arena kernels | retained bulk alone is not a local-GR/R10/PPN/clock/orbit pass | 4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md | False | 2026-07-07T19:28:46+00:00 |

## Controls
| checkpoint | control_id | control | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4696 | CTRL4696_0_no_cancellation | Use absolute retained-current component sums; do not cancel direct, memory, marker or readout pieces against each other. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | CTRL4696_1_same_branch | A zero proof must use the same parent branch for direct, EM/Poynting, non-Hilbert, marker and readout clauses. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | CTRL4696_2_poynting_once | Poynting is not a magic extra force term; ordinary Maxwell Poynting is Hilbert EM stress unless a named nonminimal/source coefficient is present. | False | 2026-07-07T19:28:46+00:00 |
| 4696 | CTRL4696_3_no_claim_from_symbolic_rows | Symbolic retained-current bounds cannot score R10, WEP, PPN, clock or orbital tests. | False | 2026-07-07T19:28:46+00:00 |

## Decision
| checkpoint | branch | decision | reason | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- |
| 4696 | MTS_R2FR_Y5_RETAINED_BULK_SOURCE_CURRENT_GATE_4696 | RETAINED_BULK_SOURCE_CURRENT_WITH_4695_EM_INSERTION_NONCLAIM | The retained-current gate now imports the 4695 EM/Poynting result: EM memory is not waved away; it is reduced to same-Hodge, wall-flux and nonminimal source inputs. Direct, marker and readout tails remain live unless parent-signed. | False | 2026-07-07T19:28:46+00:00 |

## Next Target
| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4696 | NT4696_0 | 4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md | After retained bulk is componentized and EM/Poynting is inserted, the next source-side numerator term is Q_edge: source worldtube/boundary shell flux. | prove fixed source worldtube, compact collar, no birth/death shell and zero source-boundary flux in the same branch | fill Qedge shell/worldtube/corner flux rows as nonclaim finite inputs | False | 2026-07-07T19:28:46+00:00 |
