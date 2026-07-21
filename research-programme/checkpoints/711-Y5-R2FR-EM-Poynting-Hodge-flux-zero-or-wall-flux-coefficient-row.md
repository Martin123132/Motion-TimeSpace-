# 4695 - Y5/R2FR EM/Poynting Hodge Flux Zero Or Wall-Flux Coefficient Row

Marker: `PPC4161_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695`

Decision: `EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_CURRENT_BRANCH_NONCLAIM`

## Result

4695 imports the EM/Poynting fork:

```text
S_EM=-(4 mu0)^-1 int F wedge *_obs F
T_EM=delta S_EM/delta g_obs
S_Poynting^i=-T_EM^i_nu tau^nu
```

Zero route:

```text
Delta_Hodge_EM=c_Poynt_extra=Phi_wall_Poynting=epsilon_nonminimal_EM=0
=> Q_bulk_EM/Poynting=0.
```

Bound route:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max(
  M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall|
  + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|
).
```

This makes the Poynting/background-field idea testable: open or radiative collars are not erased; they become sourceable wall-flux rows.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | SRC4695_00_4694_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4694_NEXT_TARGET.csv | True | 4695-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md | True | 2 | 4694 selected EM/Poynting target. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_01_4694_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4694_STATUS.csv | True | PPC4161_QBULK_HILBERT_EM_POYNTING_CURRENT_BRANCH_4694 | True | 2 | 4694 current branch status. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_02_4607_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_EM_POYNTING_HODGE_FLUX_THEOREM.csv | True | EMF4607_3_finite_EM_bound | True | 5 | 4607 EM/Poynting theorem. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_03_4607_hodge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_HODGE_OWNER_ROWS.csv | True | HG4607_2_conformal_guard | True | 4 | 4607 Hodge owner rows. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_04_4607_flux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_POYNTING_FLUX_ROWS.csv | True | FX4607_2_closed_domain_wall | True | 4 | 4607 Poynting flux rows. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_05_4607_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_EM_BULK_BOUND_UPDATE_ROWS.csv | True | EB4607_1_bound_route | True | 3 | 4607 EM bulk update. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_06_4607_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_CLAIM_BLOCKERS.csv | True | MIS4607_1_wall_flux | True | 3 | 4607 blockers. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_07_4607_controls | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_CONTROL_ROWS.csv | True | CTRL4607_2_local_not_global | True | 4 | 4607 controls. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_08_4607_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_STATUS.csv | True | EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_SCHEMA_READY_NONCLAIM | True | 2 | 4607 status. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_09_4607_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4607_NEXT_TARGET.csv | True | 4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | True | 2 | 4607 next target. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_10_4607_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4607_VALIDATION.csv | True | VAL4607_OVERALL | True | 18 | 4607 validation passed. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_11_4608_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_STATUS.csv | True | RETAINED_BULK_SOURCE_CURRENT_ZERO_OR_COMPONENT_ROWS_READY_NONCLAIM | True | 2 | 4608 retained-current rung exists. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_12_4608_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4608_NEXT_TARGET.csv | True | 4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md | True | 2 | 4608 next target. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_13_4608_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4608_VALIDATION.csv | True | VAL4608_OVERALL | True | 20 | 4608 validation passed. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_14_formal623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\623-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md | True | S_Poynting^i=-T_EM^i_nu | True | 16 | formal EM/Poynting gate. | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SRC4695_15_formal624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | True | J_retained := J_direct | True | 14 | formal retained-current handoff. | False | 2026-07-07T19:22:23+00:00 |

## EM/Poynting Hodge Flux Theorem

| checkpoint | theorem_id | statement | formula | consequence | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | EMF4695_0_once_only | On the public observed-Hodge Maxwell branch, Poynting is a component of Hilbert EM stress and is counted once. | S_EM=-(4 mu0)^-1 int F wedge *_obs F; T_EM=delta S_EM/delta g_obs; S_Poynting^i=-T_EM^i_nu tau^nu | c_Poynt_extra=0 in the single source functional branch. | ONCE_ONLY_THEOREM_DERIVED_CONDITIONAL | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | EMF4695_1_same_Hodge | Same-Hodge ownership zeros Delta_Hodge_EM only when the Maxwell action uses *_obs[e_obs(q)] with no independent constitutive tensor/readout Hodge. | S_Maxwell=-(4 mu0)^-1 int F wedge *_obs[e_obs(q)] F => Delta_Hodge_EM=0 | Gauge invariance alone is insufficient; constitutive countermodels remain unless object language excludes them. | SAME_HODGE_ZERO_CONDITIONAL_NOT_PARENT_SIGNED | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | EMF4695_2_no_wall_flux | The direct Poynting wall coefficient is zero only in a stationary isolated local collar with no incoming/background radiation and no current crossing the collar. | Phi_wall_Poynting=int_boundary T_EM(tau,n) dSigma dt=0 | Open/radiative/nonstationary systems retain a finite wall-flux coefficient. | LOCAL_NO_FLUX_THEOREM_CONDITIONAL_NOT_GLOBAL | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | EMF4695_3_finite_EM_bound | If same-Hodge or no-flux is unsigned, EM/Poynting feeds Q_bulk through a no-cancellation envelope. | \|Q_bulk_EM/Poynting\| <= W_lambda_max(M_ref\|Delta_Hodge_EM\| + \|c_Poynt_extra Phi_wall\| + \|Phi_wall_Poynting\| + M_ref\|epsilon_nonminimal_EM\|) | The Poynting branch is either theorem-silent or sourceable; it is not a closure axiom. | BOUND_FORMULA_DERIVED_VALUES_MISSING | False | False | 2026-07-07T19:22:23+00:00 |

## Hodge Owner Rows

| checkpoint | row_id | quantity | zero_condition | bound_formula | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | HG4695_0_same_Hodge_zero | Delta_Hodge_EM_zero | fixed e_obs, g_obs, orientation and S_EM=-(4mu0)^-1 int F wedge *_obs F with no independent chi_EM | Delta_Hodge_EM=0 | CONDITIONAL_ZERO_NOT_GLOBAL | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | HG4695_1_Hodge_envelope | Delta_Hodge_EM_abs | all constitutive residuals zero in the same parent-visible branch | \|\|Delta_Hodge_EM\|\| <= \|\|Delta_chi_principal\|\| + \|\|Delta_chi_skewon\|\| + L\|\|dtheta_EM\|\| + \|C_Hodge_hidden\| + \|C_Hodge_readout\| + \|Delta_orientation_flux\| | BOUND_DERIVED_VALUES_MISSING | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | HG4695_2_conformal_guard | Delta_conformal_scale_guard | clock/source/impedance/alpha normalization also fixed, not merely EM cone/Hodge on two-forms | retain scale/source normalization rows if only conformal cone agreement is proved | ANTI_OVERCLAIM_GUARD_ACTIVE | False | False | 2026-07-07T19:22:23+00:00 |

## Poynting Flux Rows

| checkpoint | row_id | quantity | zero_condition | bound_formula | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | FX4695_0_stationary_zero | Phi_wall_Poynting_zero | stationary isolated source collar, time_avg(dU_EM/dt)=0, time_avg(int J.E dV)=0, no external radiation/current crossing wall | Phi_wall_Poynting=0 | CONDITIONAL_LOCAL_ZERO_NOT_GLOBAL | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | FX4695_1_wall_flux_bound | Phi_wall_Poynting_abs | not zeroed on open/radiative/nonstationary source collars | \|Phi_wall_Poynting\| <= \|dU_EM/dt\| + \|int_W J.E dV\| + \|Phi_incoming\| + \|Phi_apparatus\| | FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | FX4695_2_closed_domain_wall | epsilon_Poynting_flux | closed stationary wall or finite measured/modelled wall-flux bound | epsilon_Poynting_flux=\|int_wall S_EM dot dA dt\|/E_pos | MISSING_POYNTING_FLUX_BOUND | False | False | 2026-07-07T19:22:23+00:00 |

## EM Bulk Bound Update Rows

| checkpoint | row_id | quantity | formula | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | EB4695_0_zero_route | Q_bulk_EM/Poynting | Delta_Hodge_EM=0, c_Poynt_extra=0, Phi_wall_Poynting=0, epsilon_nonminimal_EM=0 => Q_bulk_EM/Poynting=0 | CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | EB4695_1_bound_route | Q_bulk_EM_Poynting_abs | \|Q_bulk_EM/Poynting\| <= W_lambda_max(M_ref\|Delta_Hodge_EM\| + \|c_Poynt_extra Phi_wall\| + \|Phi_wall_Poynting\| + M_ref\|epsilon_nonminimal_EM\|) | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-07T19:22:23+00:00 |

## Claim Blockers

| checkpoint | blocker_id | missing_object | why_it_matters | best_next_action | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | MIS4695_0_Hodge | parent-signed same-Hodge/visible Maxwell action branch or numeric Delta_Hodge_EM envelope | without it EM constitutive mismatch can source Q_bulk | prove same-Hodge zero or fill Delta_Hodge components | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | MIS4695_1_wall_flux | stationary no-wall-flux proof or Phi_wall_Poynting bound | open EM flux is the live Poynting source-current channel | fill wall flux coefficient or prove local stationary collar | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | MIS4695_2_nonminimal | no-extra-F2/nonminimal EM source coupling zero or bound | nonminimal EM couplings survive even if ordinary Poynting is once-only | route through retained/source current rows | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | MIS4695_3_downstream | retained bulk, edge, shadow, denominator/projector, qbar_XT and arena kernels | EM/Poynting closure alone is not a local-GR claim | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | False | False | 2026-07-07T19:22:23+00:00 |

## Survivor Update

| checkpoint | survivor_id | residual_family | status_after_4695 | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | SURV4695_0_once_only | c_Poynt_extra | zero only if no extra Poynting/background source is added after T_EM | keep once-only guard active | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SURV4695_1_hodge | Delta_Hodge_EM_abs | same-Hodge zero or constitutive/readout/orientation envelope remains | return if EM branch remains live | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SURV4695_2_wall_flux | Phi_wall_Poynting_abs | stationary local collar zero or finite wall flux coefficient | source if open/radiative | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SURV4695_3_nonminimal | epsilon_nonminimal_EM | nonminimal EM/source multiplier route remains a coefficient if unsigned | fold into retained/source rows if needed | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | SURV4695_4_retained | Q_bulk_retained_abs | next live bulk numerator after EM/Poynting isolation | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | False | False | 2026-07-07T19:22:23+00:00 |

## Controls

| checkpoint | control_id | control | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4695 | CTRL4695_0_once_only | Do not add Poynting as an extra source after Maxwell stress has already been varied into T_EM. | ACTIVE | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | CTRL4695_1_same_Hodge_not_gauge | Gauge covariance alone does not prove same-Hodge; independent chi_EM or readout Hodge remains a coefficient. | ACTIVE | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | CTRL4695_2_local_not_global | Stationary no-flux is a local collar theorem, not a cosmology/global EM erasure. | ACTIVE | False | False | 2026-07-07T19:22:23+00:00 |
| 4695 | CTRL4695_3_no_claim_from_schema | Hodge/flux coefficient schemas do not imply local-GR, R10, PPN, clock or orbital success. | ACTIVE | False | False | 2026-07-07T19:22:23+00:00 |

## Decision

| checkpoint | decision | summary | next_target | public_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4695 | EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_CURRENT_BRANCH_NONCLAIM | 4695 imports the EM/Poynting same-Hodge/no-wall-flux gate. Poynting is counted once as Hilbert EM stress on the public observed-Hodge branch; if same-Hodge or no local stationary collar is unsigned, the branch becomes explicit Delta_Hodge_EM/Phi_wall_Poynting/nonminimal coefficient rows. | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | False | False | 2026-07-07T19:22:23+00:00 |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | local_GR_public_claim | next_target | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | PPC4161_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695 | L-537 | EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_CURRENT_BRANCH_NONCLAIM | once-only EM/Poynting theorem; same-Hodge conditional zero and envelope; local stationary no-wall-flux theorem and finite flux bound; EM bulk bound update | parent-signed same-Hodge branch; numeric Delta_Hodge_EM envelope; stationary no-wall-flux proof or numeric Phi_wall_Poynting; nonminimal EM zero/bound; R10/PPN/local-GR pass | PRIVATE_NONCLAIM | False | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | False | 2026-07-07T19:22:23+00:00 |

## Next Target

| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4695 | NT4695_0 | 4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md | After EM/Poynting is isolated, the next live bulk numerator is retained source current: J_direct, J_mem, marker/readout tails. | prove retained/direct/memory/readout source-current silence in the same parent branch | fill Jdirect_abs, Jmem_abs, Jmarker_abs and Jreadout_abs as nonclaim source rows | False | 2026-07-07T19:22:23+00:00 |

## Validation

| checkpoint | check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4695 | VAL4695_0_sources_exist | True | all source-register paths exist | False |
| 4695 | VAL4695_1_needles_found | True | all source-register needles found | False |
| 4695 | VAL4695_2_once_only | True | once-only theorem present | False |
| 4695 | VAL4695_3_hodge_rows | True | Hodge rows present | False |
| 4695 | VAL4695_4_flux_rows | True | flux rows present | False |
| 4695 | VAL4695_5_bound_update | True | EM bulk bound update present | False |
| 4695 | VAL4695_6_next_retained | True | next retained-current target selected | False |
| 4695 | VAL4695_7_claim_row_exists | True | claims register contains L-537 | False |
| 4695 | VAL4695_8_formal_doc | True | formal doc exists with marker | False |
| 4695 | VAL4695_9_post_doc | True | post checkpoint exists with marker | False |
| 4695 | VAL4695_10_spine_marker | True | spine marker written | False |
| 4695 | VAL4695_11_packet_marker | True | packet marker written | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_SOURCE_REGISTER | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_SOURCE_REGISTER.csv parses with 16 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv parses with 4 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_HODGE_OWNER_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_HODGE_OWNER_ROWS.csv parses with 3 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv parses with 3 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_EM_BULK_BOUND_UPDATE_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_EM_BULK_BOUND_UPDATE_ROWS.csv parses with 2 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_CLAIM_BLOCKERS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_CLAIM_BLOCKERS.csv parses with 4 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_SURVIVOR_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_SURVIVOR_UPDATE.csv parses with 5 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_CONTROL_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_CONTROL_ROWS.csv parses with 4 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_DECISION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_DECISION.csv parses with 1 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_STATUS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_STATUS.csv parses with 1 rows | False |
| 4695 | VAL4695_csv_P8_Y5_R2FR_4695_NEXT_TARGET | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4695_NEXT_TARGET.csv parses with 1 rows | False |
| 4695 | VAL4695_12_no_claim_rows_true | True | generated rows keep valid_for_claim false | False |
| 4695 | VAL4695_13_pycache_absent | True | scripts __pycache__ absent | False |
| 4695 | VAL4695_OVERALL | True | PASS | False |
