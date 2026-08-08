# 3483: Quadratic DD WEP Source Runner Or External `S_Eq` Lower Bound

## Current Verdict
- **Real derivation result:** on the same-visible-vector branch, WEP is quadratic: `eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C)`.
- **Important consequence:** WEP has an exact source-hyperplane blind family `Q_Earth dot C = 0`, so WEP alone cannot bound the four-channel coefficient vector.
- **Scope correction:** the 3475 full-rank linear inversion is only valid on the external-amplitude branch after `|S_Eq| >= L_E > 0`; it is not valid on the same-vector DD branch.
- **Not dead:** the same-vector route remains mathematically meaningful, but it now needs one more independent non-WEP row or a parent source lower-bound theorem.
- **No claim:** no local-GR, WEP, clock, or source-coupling pass is claimed here.

## Earth Source Vector Used
- `Q_Earth = (8.084214456451e-02, 4.448443445187e-05, 2.678039885446e-04, 1.950532087854e-03)` in the full-DD four-channel proxy basis.
- `||Q_Earth|| = 8.086612771152e-02`.

## Quadratic WEP Theorems
| theorem_id | statement | derivation | consequence | numeric_support | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| THM3483_0_same_vector_substitution | If the Earth source amplitude is S_Eq = Q_Earth dot C, then every Earth-source WEP row is quadratic in C. | eta_AB = S_Eq(DeltaQ_AB dot C) = (Q_Earth dot C)(DeltaQ_AB dot C). | The two WEP rows cannot be inserted as independent linear rows in the 3475 rank matrix on this branch. | ||Q_Earth||=8.086612771152e-02 | False |
| THM3483_1_source_hyperplane_escape | Same-vector WEP has an exact unbounded blind family whenever Q_Earth dot C = 0. | For any amplitude r and any unit u in ker(Q_Earth), eta_AB(r u)=r^2(Q_Earth dot u)(DeltaQ_AB dot u)=0. | WEP alone cannot globally bound coefficient amplitude in the same-vector branch. | dim ker(Q_Earth)=3 because Q_Earth is nonzero in four channels. | False |
| THM3483_2_clock_rows_needed_or_source_lower_bound | A local coefficient bound needs either a parent lower bound |S_Eq| >= L_E > 0, enough independent linear non-WEP observables, or a parent rule excluding the Q_Earth dot C = 0 family. | Quadratic WEP products vanish on ker(Q_Earth), so additional rank must come from clocks/EM/orbital rows or from a source theorem. | The next derivation target is not another WEP normalizer; it is the missing fourth independent transport/readout row or a source-lower-bound theorem. | tested in rank ledger below | False |

## Blind Direction Ledger
| blind_id | condition | rank | null_dim | unit_null_D_hatm_eff | unit_null_D_delta_m_eff | unit_null_D_me_eff | unit_null_D_e_eff | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BLIND3483_0_QEarth_kernel | Q_Earth dot C = 0 source hyperplane | 1 | 3 | -5.502628357623e-04 | 9.999998486054e-01 | 0.000000000000e+00 | 0.000000000000e+00 | unbounded amplitude direction exists | False |
| BLIND3483_1_both_deltaQ_kernel | DeltaQ_MICROSCOPE dot C = 0 and DeltaQ_EotWash dot C = 0 | 2 | 2 | -0.000000000000e+00 | 1.596888439135e-01 | 9.871673987372e-01 | 0.000000000000e+00 | unbounded amplitude direction exists | False |
| BLIND3483_2_QEarth_plus_two_clocks | Q_Earth dot C = 0 plus both current clock product rows vanish | 3 | 1 | -5.503904639594e-04 | 9.999998477930e-01 | 3.852733247716e-05 | -0.000000000000e+00 | unbounded amplitude direction exists | False |
| BLIND3483_3_QEarth_plus_clocks_plus_one_WEP_delta | Q_Earth dot C = 0 plus clocks plus first DeltaQ row | 4 | 0 | 0.000000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | 0.000000000000e+00 | no null direction in four-channel proxy | False |

## Directional Smoke Summary
| summary_id | value | detail | valid_for_claim |
| --- | --- | --- | --- |
| DIR3483_0_sample_size | 525 | deterministic basis/null/random unit directions | False |
| DIR3483_1_finite_wep_min | 3.379963279037e-06 | smallest same-vector WEP amplitude envelope among sampled non-silent directions | False |
| DIR3483_2_finite_wep_max | 4.583013332644e+04 | largest finite same-vector WEP amplitude envelope among sampled non-silent directions | False |
| DIR3483_3_wep_silent_count | 2 | sampled directions where same-vector WEP product is exactly silent in floating arithmetic | False |
| DIR3483_4_clock_product_min | 3.021582733813e-19 | nonclaim clock product envelope; not a coefficient bound without transport normalization | False |
| DIR3483_5_clock_silent_count | 6 | sampled directions where current clock rows are silent | False |

## Branch Comparison
| branch_id | model | math_form | can_use_3475_linear_rank | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR3483_0_external_amplitude_linear | S_Eq is parent-owned and independent of visible C | eta_AB = S_Eq(DeltaQ_AB dot C) | only after |S_Eq| >= L_E > 0 is derived | blocked_by_missing_parent_lower_bound | False |
| BR3483_1_same_visible_vector_quadratic | S_Eq = Q_Earth dot C | eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C) | no | blind_null_dim_with_two_clock_rows=1 | False |
| BR3483_2_zero_source_current | J_q projects to local source silence | S_Eq = 0 | no | conditional_zero_not_parent_signed | False |

## Decision Ledger
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3483_0_3475_rank_scope | The 3475 full-rank result survives only on the external-amplitude branch, not on the same-visible-vector DD branch. | same-vector WEP rows are quadratic products and have a source-hyperplane escape. | False | False |
| DEC3483_1_same_vector_status | The same-vector branch is not dead, but it is under-ranked with the current two clock rows. | Q_Earth plus the two current clock rows has null_dim=1; WEP is silent on Q_Earth dot C=0. | False | False |
| DEC3483_2_best_next_attack | Add or derive a fourth independent non-WEP transport/readout row, or prove a parent lower bound that excludes Q_Earth dot C=0. | this is the shortest route to restoring a real four-channel local coefficient bound without smuggling S_Eq=1. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3484-Y5-R2FR-fourth-nonWEP-row-or-QEarth-kernel-exclusion-theorem.md | scripts/Y5_R2FR_3484_fourth_nonWEP_row_or_QEarth_kernel_exclusion_theorem.py | Try to close the one-dimensional blind direction by deriving a fourth independent non-WEP readout row, or prove a parent theorem excluding Q_Earth dot C = 0. | rank(Q_Earth, clock/readout rows) = 4 or a parent-signed source lower bound exists | using WEP rows as linear rank rows on the same-vector branch; setting S_Eq=1; claiming local GR | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3483_0_sources_exist | True | all local sources exist | False |
| VAL3483_1_csv_parse | True | input_register:7; quadratic_theorem:3; blind_directions:4; directional_smoke:525; directional_summary:6; branch_comparison:3; decision_ledger:3; next_target:1 | False |
| VAL3483_2_inputs_present | True | earth_norm=8.086612771152e-02; wep_rows=2; clock_rows=2 | False |
| VAL3483_3_source_hyperplane_exists | True | rank=1; null_dim=3 | False |
| VAL3483_4_current_clock_rows_under_ranked | True | rank=3; null_dim=1 | False |
| VAL3483_5_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3483_6_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3483_SUMMARY | True | PASS | False |

_Generated: 2026-06-29T03:53:51.998871+00:00_
