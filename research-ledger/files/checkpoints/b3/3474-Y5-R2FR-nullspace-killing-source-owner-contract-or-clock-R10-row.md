# 3474: Nullspace-Killing Source-Owner Contract Or Clock/R10 Row

## Current Verdict
- **Real movement:** the sourced Yb E3/E2 clock alpha row raises the conditional sensitivity rank from `2` to `3`.
- **One null direction killed:** the previous null direction with `D_e` support is removed by the clock alpha row.
- **One null direction remains:** the survivor is the `D_delta_m/D_me` mass/electron-mass direction.
- **No claim:** the clock row is product-only until clock-time transport and `Xhat` normalization are parent-owned.

## Theorem Route
| attempt_id | route | claim_tested | mathematical_form | result | blocker | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NSK3474_0_parent_source_owner | theorem | VisibleSourceOwner zeros every source-channel coefficient before arenas are applied. | Theta_vis=q^*Theta_bar or fixed superselection => D_hatm=D_delta_m=D_me=D_e=0 | UNCHANGED_UNSIGNED | 3469/3472 owner clauses are exact conditionals but not parent-action signatures | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv | False |
| NSK3474_1_clock_transport | theorem | A clock alpha product row can be treated as the same underlying D_e source direction as WEP only if arena transport is parent-owned. | D_e^clock = T_clock<-source D_e and D_e^WEP = T_WEP<-source D_e with declared transport maps | TRANSPORT_CONTRACT_REQUIRED | clock tau/time and Xhat normalization remain product-only; no standalone D_e claim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1321_CLOCK_PRODUCT_SCHEMA.csv | False |

## Clock Sensitivity Row
| clock_row_id | arena | clock_pair | observable | D_hatm_eff | D_delta_m_eff | D_me_eff | D_e_eff | product_bound_1sigma_yr_inv | product_bound_2sigma_yr_inv | source_path | bound_source_path | rank_use | claim_policy | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLK3474_0_YbE3E2_alpha | CLOCK_YbE3E2_ALPHA_DRIFT | 171Yb+ E3 / 171Yb+ E2 | d ln(nu_E3/nu_E2)/dt | 0.000000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | -6.950000000000e+00 | 2.1e-18 | 3.2e-18 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv | sensitivity_vector_only | product-only; no standalone D_e without clock transport/tau map | False |

## Augmented Matrix
| aug_row_id | arena | row_type | raw_D_hatm_eff | raw_D_delta_m_eff | raw_D_me_eff | raw_D_e_eff | unit_D_hatm_eff | unit_D_delta_m_eff | unit_D_me_eff | unit_D_e_eff | bound | bound_units | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | WEP_material_difference | -2.688964583060e-03 | -1.930433521432e-04 | 3.122760108200e-05 | -1.935818782604e-03 | -8.101582343661e-01 | -5.816203839712e-02 | 9.408565034832e-03 | -5.832429095003e-01 | 2.755102040816e-15 | dimensionless_eta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv | False |
| MATRIX3473_1_EOTWASH_Be_minus_Ti | EOTWASH_BETI_EARTH_FIELD | WEP_material_difference | -7.223420685310e-03 | 5.359772364790e-05 | -8.670220001900e-06 | -1.567089808460e-03 | -9.772403143565e-01 | 7.251115307874e-03 | -1.172974535102e-03 | -2.120080504461e-01 | 3.828000000000e-13 | dimensionless_eta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv | False |
| MATRIX3474_2_CLOCK_YbE3E2_alpha | CLOCK_YbE3E2_ALPHA_DRIFT | clock_alpha_sensitivity | 0.000000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | -6.950000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | -1.000000000000e+00 | 2.1e-18 | yr^-1_product_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv | False |

## Rank Ledger
| rank_id | rows | columns | rank | nullspace_dimension | previous_rank | previous_nullspace_dimension | rank_gain | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RANK3474_0_WEP_plus_clock_alpha | 3 | 4 | 3 | 1 | 2 | 2 | 1 | RANK_THREE_ONE_NULL_DIRECTION_REMAINS | False |

## New Nullspace
| basis_id | D_hatm_eff | D_delta_m_eff | D_me_eff | D_e_eff | check | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NULL3474_0 | -3.905698758629e-15 | 1.596888439135e-01 | 9.871673987372e-01 | 0.000000000000e+00 | augmented_matrix*v approximately zero | SURVIVING_UNCONSTRAINED_SOURCE_DIRECTION | False |

## Previous Null Direction Impact
| kill_id | previous_basis_id | clock_row_dot_previous_null | abs_dot | effect | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| KILL3474_NULL3473_0 | NULL3473_0 | 0.000000000000e+00 | 0.000000000000e+00 | SURVIVES_CLOCK_ALPHA_ROW | previous null direction has no D_e support | False |
| KILL3474_NULL3473_1 | NULL3473_1 | -1.080300675943e+00 | 1.080300675943e+00 | KILLED_BY_CLOCK_ALPHA_ROW | clock alpha row measures D_e component | False |

## Claim Gates
| gate_id | requirement | passed | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG3474_0_parent_theorem | parent source-owner theorem signs zero source vector | False | theorem route unchanged unsigned | False |
| CG3474_1_clock_row_independent | sourced clock row raises rank | True | rank=3; rank_gain=1 | False |
| CG3474_2_null_direction_killed | at least one 3473 null direction is killed | True | killed_count=1 | False |
| CG3474_3_full_closure | all source directions are bounded or theorem-zero | False | nullspace_dimension=1; clock row is product-only | False |
| CG3474_4_no_claim | no WEP/local-GR/clock pass claimed | True | all generated rows valid_for_claim=false | False |

## Decision
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3474_0_rank_lift | Add the Yb E3/E2 clock alpha row as a conditional independent sensitivity row. | rank rises from 2 to 3; NULL3473_1 is killed | False | False |
| DEC3474_1_remaining_gap | The surviving null direction is the mass/electron-mass combination, not the alpha direction. | NULL3473_0 survives because the clock alpha row has no D_delta_m/D_me sensitivity. | False | False |
| DEC3474_2_no_shortcut | Do not convert the clock product bound into a standalone D_e or WEP bound. | clock tau/time transport and Xhat normalization remain missing, so this is rank geometry only. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3475-Y5-R2FR-surviving-mass-electron-null-direction-theorem-or-clock-mu-row.md | scripts/Y5_R2FR_3475_surviving_mass_electron_null_direction_theorem_or_clock_mu_row.py | Target the remaining D_delta_m/D_me null direction: derive the parent electron/quark mass-ratio owner theorem, or add a sourced clock/spectroscopy sensitivity row involving mu or nuclear mass ratios. | The final null direction is killed by theorem or by an independent sourced mu/nuclear/electron-mass sensitivity row; no clock tau shortcut or standalone coefficient claim. | GitHub action; formalization-workbench edits; public WEP/local-GR claim; converting clock product bounds into standalone coefficients without transport. | False | False |

## Source Register
| timestamp_utc | source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 2026-06-29T03:11:24.450746+00:00 | script_3474 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3474_nullspace_killing_source_owner_contract_or_clock_R10_row.py | True | generator | False |
| 2026-06-29T03:11:24.450746+00:00 | doc_3473 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3473-Y5-R2FR-full-DD-multiarena-rank-or-parent-source-owner-proof.md | True | 3473 handoff | False |
| 2026-06-29T03:11:24.450746+00:00 | next_3473 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_NEXT_TARGET.csv | True | 3474 target statement | False |
| 2026-06-29T03:11:24.450746+00:00 | matrix_3473 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MULTIARENA_MATRIX.csv | True | two-WEP-row full DD matrix | False |
| 2026-06-29T03:11:24.450746+00:00 | nullspace_3473 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS.csv | True | two surviving WEP null directions | False |
| 2026-06-29T03:11:24.450746+00:00 | rank_3473 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_RANK_LEDGER.csv | True | previous rank ledger | False |
| 2026-06-29T03:11:24.450746+00:00 | source_owner_3472 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv | True | source-owner theorem attempt | False |
| 2026-06-29T03:11:24.450746+00:00 | contract_3469 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv | True | visible coefficient owner contract | False |
| 2026-06-29T03:11:24.450746+00:00 | clock_sensitivity_646 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv | True | clock alpha sensitivity source rows | False |
| 2026-06-29T03:11:24.450746+00:00 | clock_bound_647 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv | True | clock alpha product bounds | False |
| 2026-06-29T03:11:24.450746+00:00 | clock_schema_1321 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1321_CLOCK_PRODUCT_SCHEMA.csv | True | clock product no-shortcut schema | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3474_0_sources_exist | True | all local sources exist | False |
| VAL3474_1_csv_parse | True | all output csv files parse | False |
| VAL3474_2_augmented_shape | True | rows=3; cols=4 | False |
| VAL3474_3_augmented_finite | True | all normalized matrix entries finite | False |
| VAL3474_4_rank_three | True | rank=3 | False |
| VAL3474_5_nullspace_dim_one | True | dim=1; basis_rows=1 | False |
| VAL3474_6_kills_one_previous_null | True | killed_count=1 | False |
| VAL3474_7_no_claim | True | all 3474 rows valid_for_claim=false | False |
| VAL3474_8_no_formalization_outputs | True | no outputs under formalization-workbench | False |
| VAL3474_9_git_formalization_clean | True | NOT_A_GIT_REPOSITORY | False |
| VAL3474_SUMMARY | True | PASS | False |
