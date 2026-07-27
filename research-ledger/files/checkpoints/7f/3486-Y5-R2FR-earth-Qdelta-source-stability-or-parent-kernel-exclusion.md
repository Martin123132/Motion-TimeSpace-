# 3486: Earth `Q_delta` Source Stability Or Parent Kernel Exclusion

## Current Verdict
- **Good news:** inside the DD Earth proxy, `Q_delta_m_Earth` is not a numerical fluke; a conservative Fe-only-minus-negative lower bound remains positive.
- **Important mechanism:** the 3485 rank closure depends on this nonzero Earth neutron-excess component.
- **Sharp guard:** forcing `Q_delta_m_Earth=0` destroys the rank closure.
- **Still private/nonclaim:** this is DD-proxy stability, not yet parent MTS source ownership.

## Positivity Bounds
| bound_id | statement | value | derivation | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| QDEL3486_0_baseline_sum | Baseline Earth DD proxy has positive Q_delta_m_Earth. | 4.448443445187e-05 | sum over normalized composition rows of f_i * 0.0017*(A_i-2Z_i)/A_i | POSITIVE_IN_DD_PROXY_NONCLAIM_PARENT_MAP_MISSING | False |
| QDEL3486_1_fe_dominance | Iron alone dominates the positive neutron-excess contribution. | 3.750760958797e-05 | f_Fe=3.204486280793e-01 times q_delta_Fe=1.170471841705e-04 | DOMINANT_ANCHOR | False |
| QDEL3486_2_negative_rows | The negative H/O correction is much smaller than the Fe contribution. | -5.342108795250e-07 | sum of negative weighted Q_delta_m rows in the current target table | NEGATIVE_CORRECTION_SMALL | False |
| QDEL3486_3_fe_only_lower_bound | A conservative Fe-only-minus-negative correction lower bound remains positive. | 3.697339870845e-05 | weighted_Fe_Qdelta + all negative weighted rows, dropping every other positive support row | STRICTLY_POSITIVE_WITH_CURRENT_TARGET_ROWS | False |
| QDEL3486_4_critical_fe_fraction | Minimum Fe fraction required to beat all current negative corrections even if all other positive rows are dropped. | 4.564064341324e-03 | |negative_total| / q_delta_Fe | ACTUAL_FE_FRACTION_EXCEEDS_CRITICAL_BY_FACTOR_7.021124246166e+01 | False |
| QDEL3486_5_positive_total | Total positive support excluding sign cancellations. | 4.501864533139e-05 | sum positive weighted rows | POSITIVE_SUPPORT_LEDGER | False |

## Rank Stress Tests
| scenario_id | description | Q_delta_m_Earth_used | rank_with_best_3485_row | min_singular_value | condition_number | closure_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| STRESS3486_0_baseline | baseline Q_delta_m_Earth from 3482 | 4.448443445187e-05 | 4 | 4.431522265308e-05 | 1.690393478510e+05 | rank_closes | False |
| STRESS3486_1_fe_only_lower | Fe-only-minus-negative lower bound; all other positive support dropped | 3.697339870845e-05 | 4 | 3.683275770953e-05 | 2.033791875217e+05 | rank_closes | False |
| STRESS3486_2_no_fe_extreme | unphysical diagnostic removing Fe contribution while retaining all other rows | 6.976824863900e-06 | 4 | 6.950286118434e-06 | 1.077799706300e+06 | rank_closes | False |
| STRESS3486_3_forced_zero_failure | forced Q_delta_m_Earth=0 diagnostic | 0.000000000000e+00 | 3 | 3.804703364156e-19 | 1.968883148086e+19 | rank_fails | False |

## Theorems
| theorem_id | statement | proof | result | valid_for_claim |
| --- | --- | --- | --- | --- |
| THM3486_0_DD_proxy_Qdelta_positive | Within the current bulk Earth DD proxy, Q_delta_m_Earth is strictly positive under a conservative Fe-only-minus-negative bound. | The Fe weighted neutron-excess term exceeds the total negative H/O correction even after dropping every other positive contribution. | lower_bound=3.697339870845e-05 | False |
| THM3486_1_rank_depends_on_Qdelta_nonzero | The 3485 rank closure depends on Q_delta_m_Earth being nonzero. | Forcing Q_delta_m_Earth to zero collapses the best 3485 augmented system back to rank 3. | forced_zero_rank=3 | False |
| THM3486_2_parent_gap | This proves stability only in the DD proxy, not yet in parent MTS source transport. | The source vector still comes from composition plus DD charge formulas; the parent MTS action has not supplied the quotient/source-current map. | conditional closure strengthened, local-GR claim still forbidden | False |

## Decisions
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3486_0_DD_proxy_stability | Keep the same-vector DD branch alive and upgraded from algebraic accident to proxy-stable conditional closure. | baseline rank=4; conservative lower-bound rank=4. | False | False |
| DEC3486_1_no_public_claim | Do not claim local GR/source-coupling pass from this checkpoint. | the parent MTS source-current/transport map is still unsigned, and the condition number remains large. | False | False |
| DEC3486_2_best_next_attack | Move from DD-proxy stability to parent-source ownership: derive the quotient/source-current map that makes Q_Earth the actual MTS local source. | that is the shortest path from conditional local-rank closure toward a serious local-GR reduction. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3487-Y5-R2FR-parent-source-map-for-DD-earth-vector-or-local-rank-closure-demotion.md | scripts/Y5_R2FR_3487_parent_source_map_for_DD_earth_vector_or_local_rank_closure_demotion.py | Try to derive the parent MTS source-current/quotient map that makes the DD Earth vector a legitimate local source row; otherwise demote 3485-3486 to DD-proxy evidence only. | parent action gives J_q and transport/readout map reducing to the DD Earth source vector, with no arena-specific source amplitude shortcut | treating DD proxy as parent-owned; claiming local GR; using WEP as linear same-vector row; hiding condition number | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3486_0_sources_exist | True | all local source rows exist | False |
| VAL3486_1_csv_parse | True | source_register:8; element_qdelta:14; positivity_bounds:6; rank_stress:4; theorems:3; decisions:3; next_target:1 | False |
| VAL3486_2_positive_lower_bound | True | lower_bound=3.697339870845e-05 | False |
| VAL3486_3_forced_zero_rank_fails | True | rank=3 | False |
| VAL3486_4_lower_bound_rank_closes | True | rank=4; cond=2.033791875217e+05 | False |
| VAL3486_5_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3486_6_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3486_SUMMARY | True | PASS | False |

_Generated: 2026-06-29T04:21:06.245907+00:00_
