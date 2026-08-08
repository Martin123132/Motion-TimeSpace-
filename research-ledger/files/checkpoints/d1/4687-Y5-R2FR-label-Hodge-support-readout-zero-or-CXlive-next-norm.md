# 4687 - Y5/R2FR Label/Hodge/Support/Readout Zero Or C_X Live Next Norm

Marker: `PPC4161_LABEL_HODGE_SUPPORT_READOUT_GATE_CURRENT_BRANCH_4687`

Decision: `LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM`

## Result

4687 imports the label/Hodge/support/readout gate:

```text
C_X^post4687 = C_X^std_weight_live + C_X^LHRS_live
             + C_X^boundary + C_X^nonHilbert.

C_X^LHRS_live = C_X^label + C_X^Hodge + C_X^support + C_X^readout.
```

The LHRS block vanishes only in one same parent branch:

```text
label-forgetting + same Maxwell-Hodge owner + q-basic regular support
+ pure post-variation readout => C_X^LHRS_live=0.
```

Otherwise `C_X^LHRS_live` enters `A_mem/A_h` as an explicit finite norm. No local-GR, R10 or PPN claim is promoted here.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | SRC4687_00_4686_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4686_NEXT_TARGET.csv | True | 4687-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md | True | 2 | 4686 selected label/Hodge/support/readout target. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_01_4686_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4686_STATUS.csv | True | PPC4161_CONSTANT_STANDARD_SOURCE_WEIGHT_GATE_CURRENT_BRANCH_4686 | True | 2 | 4686 current branch status. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_02_4599_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv | True | LHRS4599_4_combined | True | 6 | 4599 combined label/Hodge/support/readout zero theorem. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_03_4599_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv | True | N4599_4_total | True | 6 | 4599 finite LHRS norm rows. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_04_4599_body | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv | True | BU4599_0_Csplit | True | 2 | 4599 body-charge envelope update. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_05_4599_next_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv | True | C4599_4_LHRS | True | 6 | 4599 next norm row for C_X^LHRS_live. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_06_4599_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_STATUS.csv | True | PPC4161_LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_CXLIVE_NEXT_NORM_4599 | True | 2 | 4599 status. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_07_4599_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4599_NEXT_TARGET.csv | True | 4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | True | 2 | 4599 next target. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_08_4599_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4599_VALIDATION.csv | True | VAL4599_OVERALL | True | 17 | 4599 validation passed. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_09_4600_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_STATUS.csv | True | PPC4161_BOUNDARY_NONHILBERT_ZERO_OR_FINAL_CXLIVE_NORM_4600 | True | 2 | 4600 next rung exists. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_10_4600_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_NEXT_TARGET.csv | True | 4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md | True | 2 | 4600 next target. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_11_4600_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4600_VALIDATION.csv | True | VAL4600_OVERALL | True | 20 | 4600 validation passed. | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SRC4687_12_formal615 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\615-PPC4161-label-Hodge-support-readout-zero-or-CXlive-next-norm.md | True | C_X^LHRS_live = C_X^label + C_X^Hodge + C_X^support + C_X^readout | True | 21 | formal label/Hodge/support/readout gate. | False | 2026-07-07T18:45:32+00:00 |

## Label / Hodge / Support / Readout Zero Theorem

| checkpoint | theorem_id | target | zero_branch | formula | finite_branch | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | LHRS4687_0_label | C_X^label | source functor consumes only total variational objects T_total,J_total; source labels, constructor tags, spurions and post-readout markers are not arguments of the parent source map | F_src(T_total,J_total) has no A-label or marker slot => C_X^label=0 | \|C_X^label\| <= \|Delta_label_X\| | EXACT_CONDITIONAL_LABEL_ZERO_COUNTERMODEL_RETAINED | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | LHRS4687_1_Hodge | C_X^Hodge | Maxwell/current sector uses the same observed metric, coframe and orientation owner as the local source projection; no independent chi_EM, hidden constitutive tensor, readout Hodge or orientation residual is allowed | Delta_Hodge_EM=0 => C_X^Hodge=0 | \|\|Delta_Hodge_EM\|\| <= \|\|Delta_chi_principal\|\|+\|\|Delta_chi_skewon\|\|+L\|\|dtheta_EM\|\|+\|C_Hodge_hidden\|+\|C_Hodge_readout\|+\|Delta_orientation_flux\| | SAME_HODGE_ZERO_OR_NO_CANCELLATION_BOUND_READY | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | LHRS4687_2_support | C_X^support | source support is q-basic, regular and finite-perimeter with fixed collar, zero boundary trace, no birth/death shell, no threshold mask and no hidden side flux | rho_H^tr\|partial W=0 and mu_birth=0 => E_boundary_birth=0 => C_X^support=0 | Phi_A*(int_partialW \|rho_H^tr\|\|V_n\| dSigma + \|\|mu_birth\|\|_TV)/\|M_H_ref\| plus retained support terms | REYNOLDS_ZERO_OR_SHELL_NORM_READY | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | LHRS4687_3_readout | C_X^readout | variation happens before readout, and readout is pure postprocessing on the solved parent quotient with no action, effective-action, coefficient or source-worldtube reentry | Pi_CoeffSource([delta_parent,R_post]T_H)=0 => C_X^readout=0 | \|\|C_R\|\| from projector/source-worldtube, EFT/prevariation, calibration feedback, material/clock response and arena kernels | PURE_POSTPROCESSING_ZERO_OR_COMMUTATOR_BOUND_READY | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | LHRS4687_4_combined | C_X^LHRS_live | LHRS4687_0 through LHRS4687_3 all pass in the same parent branch without cancellation or fitted-calibration hiding | C_X^LHRS_live=C_X^label+C_X^Hodge+C_X^support+C_X^readout=0 | \|C_X^LHRS_live\| <= \|C_X^label\|+\|C_X^Hodge\|+\|C_X^support\|+\|C_X^readout\| | COMBINED_ZERO_OR_ABSOLUTE_SUM_READY | False | False | 2026-07-07T18:45:32+00:00 |

## LHRS Norm Rows

| checkpoint | norm_id | symbol | definition | finite_bound | observable_link | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | N4687_0_label | Delta_label_X | source-label/constructor/spurion return norm | source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding | WEP/R10/PPN source-label sensitivity | VALUE_MISSING_NONCLAIM | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | N4687_1_Hodge | Delta_Hodge_EM_X | same-Hodge/constitutive mismatch norm | source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding | EM/Poynting/alpha/clock source sensitivity | VALUE_MISSING_NONCLAIM | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | N4687_2_support | Delta_support_X | Reynolds support-boundary/source-worldtube norm | source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding | source mass/support/orbital/WEP kernels | VALUE_MISSING_NONCLAIM | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | N4687_3_readout | C_R_X | readout/variation commutator norm | source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding | WEP/R10/PPN/clock/orbit readout kernels | VALUE_MISSING_NONCLAIM | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | N4687_4_total | C_X^LHRS_live | combined label-Hodge-support-readout live norm | source-backed value or same-branch zero certificate required; no cancellation or fitted-calibration hiding | A_mem/A_h numerator input | ABSOLUTE_SUM_READY_VALUES_MISSING | False | False | 2026-07-07T18:45:32+00:00 |

## Body-Charge Envelope Update

| checkpoint | update_id | target | formula | zero_condition | finite_bound | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | BU4687_0_Csplit | C_X live after 4687 | C_X^post4687 = C_X^std_weight_live + C_X^LHRS_live + C_X^boundary + C_X^nonHilbert | C_X^LHRS_live=0 only if label, Hodge, support and readout zero theorems pass in the same parent branch | \|C_X^post4687\| <= \|C_X^std_weight_live\|+\|C_X^LHRS_live\|+\|C_X^boundary\|+\|C_X^nonHilbert\| | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | BU4687_1_memory | A_mem | \|A_mem\| <= [exp(R/lambda_mem) int_body (\|\|B_mem_eff\|\|\|\|R_obs\|\| + \|\|C_mem^post4687\|\|\|\|T\|\| + \|\|J_mem_live\|\|) dV + \|\|Q_boundary_mem\|\|]/(4*pi\|\|Z_mem\|\|) | B_mem_eff=C_mem^post4687=J_mem_live=Q_boundary_mem=0 | label/Hodge/support/readout pieces now enter through C_mem^LHRS_live | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | BU4687_2_fibre | A_h | \|A_h\| <= [exp(R/lambda_h) int_body (\|\|B_h\|\|\|\|R_obs\|\| + \|\|C_h^post4687\|\|\|\|T\|\| + \|\|J_h_live\|\|) dV + \|\|Q_boundary_h\|\|]/(4*pi\|\|Z_h\|\|) | B_h=C_h^post4687=J_h_live=Q_boundary_h=0 | label/Hodge/support/readout pieces now enter through C_h^LHRS_live | False | False | 2026-07-07T18:45:32+00:00 |

## C_X Live Next Norm Rows

| checkpoint | coefficient_id | symbol | role | derive_first | finite_fallback | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | C4687_0_label | C_X^label | source-label/constructor leakage | prove total-source functor has no label/spurion/readout slot | Delta_label_X | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | C4687_1_Hodge | C_X^Hodge | Maxwell-Hodge/constitutive leakage | prove same-Hodge visible Maxwell action and no independent chi_EM/readout/orientation residual | Delta_Hodge_EM_X | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | C4687_2_support | C_X^support | source-support/worldtube leakage | prove q-basic regular zero-trace support with no shell/threshold/side flux | Delta_support_X | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | C4687_3_readout | C_X^readout | readout/projection commutator leakage | prove variation-before-readout and pure postprocessing no-reentry | C_R_X | MISSING_PARENT_ZERO_OR_VALUE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | C4687_4_LHRS | C_X^LHRS_live | combined label-Hodge-support-readout live norm | all four subrows zero in same branch | absolute sum of C4687_0..3 | NEXT_NORM_ROW_READY_VALUES_MISSING | False | False | 2026-07-07T18:45:32+00:00 |

## Survivor Update

| checkpoint | survivor_id | residual_family | status_after_4687 | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | SURV4687_0_LHRS | label/Hodge/support/readout C_X rows | zero-or-norm law imported; no numeric LHRS norms yet | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SURV4687_1_CX_post4687 | C_X post4687 live vector | boundary and non-Hilbert/shadow leakage remain | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SURV4687_2_A_mem_A_h | body-charge envelopes | A_mem/A_h updated to use C_mem^post4687/C_h^post4687 | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SURV4687_3_standard_weight | constant/standard/source-weight rows | unchanged from 4686 and still explicit | carry into final C_X vector | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | SURV4687_4_global_parent | EH/global parent/material projection | unchanged public blockers | keep promotion firewall active | False | False | 2026-07-07T18:45:32+00:00 |

## Controls

| checkpoint | control_id | rule | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4687 | CTRL4687_0 | Do not zero label leakage unless the source functor consumes total variational objects and has no source-label, marker or spurion slot. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | CTRL4687_1 | Do not zero Hodge leakage unless Maxwell, current and source projection use the same metric/coframe/orientation owner. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | CTRL4687_2 | Do not zero support leakage unless source worldtubes are q-basic regular with zero trace and no birth/death shell or threshold mask. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | CTRL4687_3 | Do not zero readout leakage unless variation strictly precedes pure postprocessing and the readout cannot reenter the action or source coefficient. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | CTRL4687_4 | A_mem/A_h must carry C_X^LHRS_live until every LHRS branch is zeroed or source-valued. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |
| 4687 | CTRL4687_5 | Next target is boundary/non-Hilbert leakage, not public local-GR scoring. | ACTIVE | False | False | 2026-07-07T18:45:32+00:00 |

## Decision

| checkpoint | decision | summary | next_target | public_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4687 | LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM | 4687 imports the 4599 label/Hodge/support/readout gate into the current branch. These four routes vanish only if source labels are forgotten, Maxwell uses the same observed Hodge owner, support is q-basic regular with no shell or side flux, and readout is pure post-variation postprocessing in the same parent branch. Otherwise C_X^LHRS_live remains an explicit norm inside A_mem/A_h. | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | False | False | 2026-07-07T18:45:32+00:00 |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | local_GR_public_claim | next_target | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | PPC4161_LABEL_HODGE_SUPPORT_READOUT_GATE_CURRENT_BRANCH_4687 | L-529 | LABEL_HODGE_SUPPORT_READOUT_ZERO_OR_NORM_INSERTED_CURRENT_BRANCH_NONCLAIM | source-label zero-or-norm law; same-Hodge/constitutive zero-or-norm law; support/worldtube zero-or-Reynolds norm law; readout/projection commutator zero-or-norm law; C_X^post4687 and A_mem/A_h envelope update | parent-signed label/Hodge/support/readout zero in one branch; numeric LHRS norm values; boundary/non-Hilbert C_X rows; local-GR/R10/PPN scoring | PRIVATE_NONCLAIM | False | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | False | 2026-07-07T18:45:32+00:00 |

## Next Target

| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4687 | NT4687_0 | 4688-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | After label/Hodge/support/readout are isolated, the remaining C_X live family is boundary plus non-Hilbert/shadow current leakage. | prove boundary neutrality and no non-Hilbert/shadow source covector in the same parent branch | fill final C_X boundary/non-Hilbert norm row and insert into A_mem/A_h | False | 2026-07-07T18:45:32+00:00 |

## Validation

| checkpoint | check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4687 | VAL4687_0_sources_exist | True | all source-register paths exist | False |
| 4687 | VAL4687_1_needles_found | True | all source-register needles found | False |
| 4687 | VAL4687_2_four_zero_branches | True | four LHRS zero branches plus combined row present | False |
| 4687 | VAL4687_3_norm_rows | True | LHRS finite norm total present | False |
| 4687 | VAL4687_4_body_update | True | A_mem/A_h post4687 update present | False |
| 4687 | VAL4687_5_next_norm_rows | True | C_X live next norm rows present | False |
| 4687 | VAL4687_6_next_boundary_nonHilbert | True | next boundary/non-Hilbert target selected | False |
| 4687 | VAL4687_7_claim_row_exists | True | claims register contains L-529 | False |
| 4687 | VAL4687_8_formal_doc | True | formal doc exists with marker | False |
| 4687 | VAL4687_9_post_doc | True | post checkpoint exists with marker | False |
| 4687 | VAL4687_10_spine_marker | True | spine marker written | False |
| 4687 | VAL4687_11_packet_marker | True | packet marker written | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_SOURCE_REGISTER | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_SOURCE_REGISTER.csv parses with 13 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv parses with 5 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_CX_LABEL_HODGE_SUPPORT_READOUT_NORM | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv parses with 5 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_BODY_CHARGE_ENVELOPE_LABEL_HODGE_READOUT_UPDATE.csv parses with 3 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_CXLIVE_NEXT_NORM_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_CXLIVE_NEXT_NORM_ROWS.csv parses with 5 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_SURVIVOR_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_SURVIVOR_UPDATE.csv parses with 5 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_CONTROL_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_CONTROL_ROWS.csv parses with 6 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_DECISION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_DECISION.csv parses with 1 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_STATUS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_STATUS.csv parses with 1 rows | False |
| 4687 | VAL4687_csv_P8_Y5_R2FR_4687_NEXT_TARGET | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4687_NEXT_TARGET.csv parses with 1 rows | False |
| 4687 | VAL4687_12_no_claim_rows_true | True | generated rows keep valid_for_claim false | False |
| 4687 | VAL4687_13_pycache_absent | True | scripts __pycache__ absent | False |
| 4687 | VAL4687_OVERALL | True | PASS | False |
