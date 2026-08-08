# 3473: Full DD Multiarena Rank Or Parent Source-Owner Proof

## Current Verdict
- **Real movement:** adding Eöt-Wash Be/Ti to the full DD basis raises the current WEP source matrix to rank `2`.
- **Still not enough:** the full source space has four channels, so the current WEP-only matrix leaves nullspace dimension `2`.
- **Meaning:** the coupling problem is now sharply located as two surviving source directions, not a vague missing-coupling complaint.
- **No claim:** this does not pass WEP/local-GR; it tells us exactly what remains to derive or source.

## Matrix Rows
| row_id | arena | left_minus_right | Delta_Q_hatm_full | Delta_Q_delta_m | Delta_Q_m_e | Delta_Q_e_full | eta_abs_bound | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | TA6V_minus_PtRh10 | -2.688964583060e-03 | -1.930433521432e-04 | 3.122760108200e-05 | -1.935818782604e-03 | 2.755102040816e-15 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv | False |
| MATRIX3473_1_EOTWASH_Be_minus_Ti | EOTWASH_BETI_EARTH_FIELD | EOTWASH_Be_minus_EOTWASH_Ti | -7.223420685310e-03 | 5.359772364790e-05 | -8.670220001900e-06 | -1.567089808460e-03 | 3.828000000000e-13 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv | False |

## Rank Ledger
| rank_id | rows | columns | rank | nullspace_dimension | singular_value_max | singular_value_min | condition_number_nonzero_singulars | row_cosine | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RANK3473_0_full_DD_two_arena_matrix | 2 | 4 | 2 | 2 | 8.007732690414e-03 | 1.236490072429e-03 | 6.476180334130e+00 | 9.149387041559e-01 | RANK_TWO_NOT_FULL_RANK | False |

## Nullspace Basis
| basis_id | D_hatm_eff | D_delta_m_eff | D_me_eff | D_e_eff | check | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NULL3473_0 | -3.784756097299e-15 | 1.596888439135e-01 | 9.871673987372e-01 | 0.000000000000e+00 | A*v approximately zero by construction | UNCONSTRAINED_SOURCE_DIRECTION | False |
| NULL3473_1 | -4.104528142347e-02 | -9.869924107528e-01 | 0.000000000000e+00 | 1.554389461788e-01 | A*v approximately zero by construction | UNCONSTRAINED_SOURCE_DIRECTION | False |

## Component Bound Status
| component_id | symbol | finite_bound_from_current_WEP_rows | nullspace_support_abs_max | reason | next_requirement | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CBS3473_D_hatm_eff | D_hatm_eff | False | 4.104528142347e-02 | current two WEP rows leave a nullspace direction that changes this component | parent source-owner theorem or independent clock/R10/WEP rows | False |
| CBS3473_D_delta_m_eff | D_delta_m_eff | False | 9.869924107528e-01 | current two WEP rows leave a nullspace direction that changes this component | parent source-owner theorem or independent clock/R10/WEP rows | False |
| CBS3473_D_me_eff | D_me_eff | False | 9.871673987372e-01 | current two WEP rows leave a nullspace direction that changes this component | parent source-owner theorem or independent clock/R10/WEP rows | False |
| CBS3473_D_e_eff | D_e_eff | False | 1.554389461788e-01 | current two WEP rows leave a nullspace direction that changes this component | parent source-owner theorem or independent clock/R10/WEP rows | False |

## Parent Source-Owner Route
| attempt_id | claim_tested | result | blocker | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PARENT3473_0_reuse_3472_source_owner | Can the source-owner theorem close instead of adding arenas? | UNCHANGED_UNSIGNED | 3472 already established the theorem is coherent but not parent-signed | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv | False |
| PARENT3473_1_rank_implication | If the theorem is signed, rank tests become consistency checks rather than coefficient bounds. | EXACT_CONDITIONAL | requires VisibleSourceOwner + readout preservation clauses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv | False |

## Material Rows
| material_charge_id | arena | material_id | composition_basis | Q_hatm_full | Q_delta_m | Q_m_e | Q_e_full | source_path | valid_for_claim | A_context | Z | formula_source_path |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAT3473_MICROSCOPE_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | PtRh10 | full Damour-Donoghue four-charge basis; mass-fraction alloy average; F_A=1 proxy | 8.516478830914e-02 | 3.279393239319e-04 | 2.219509917169e-04 | 4.185347621992e-03 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv | False |  |  |  |
| MAT3473_MICROSCOPE_TA6V | MICROSCOPE_TIPT_EARTH_FIELD | TA6V | full Damour-Donoghue four-charge basis; mass-fraction alloy average; F_A=1 proxy | 8.247582372608e-02 | 1.348959717887e-04 | 2.531785927989e-04 | 2.249528839388e-03 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv | False |  |  |  |
| MAT3473_EOTWASH_Be | EOTWASH_BETI_EARTH_FIELD | EOTWASH_Be | nominal pure natural element; Eot-Wash source identifies test-body element, not isotope/binding tensor | 7.535894969073e-02 | 1.909345109962e-04 | 2.441135349859e-04 | 7.166302683548e-04 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv | False | 9.012200000000e+00 | 4.000000000000e+00 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external-sources\damour_donoghue_1007.2792_source\DamourDonoghueEPfinal.tex |
| MAT3473_EOTWASH_Ti | EOTWASH_BETI_EARTH_FIELD | EOTWASH_Ti | nominal pure natural element; Eot-Wash source identifies test-body element, not isotope/binding tensor | 8.258237037604e-02 | 1.373367873483e-04 | 2.527837549878e-04 | 2.283720076815e-03 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv | False | 4.786700000000e+01 | 2.200000000000e+01 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external-sources\damour_donoghue_1007.2792_source\DamourDonoghueEPfinal.tex |

## Claim Gates
| gate_id | requirement | passed | evidence | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG3473_0_matrix_rank | full DD multiarena WEP matrix rank computed | True | rank=2; nullspace_dimension=2 | False |
| CG3473_1_full_component_bounds | current arenas produce finite bounds on all four source coefficients | False | all components remain unbounded along at least one null direction | False |
| CG3473_2_parent_source_owner | parent theorem zeros the source vector | False | source-owner theorem remains unsigned | False |
| CG3473_3_no_claim | no WEP/local-GR/source-coupling pass is claimed | True | all rows valid_for_claim=false | False |

## Decision
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3473_0_rank_result | Two WEP arenas raise the full DD source matrix to rank 2, not rank 4. | rank=2; nullspace_dimension=2; row_cosine=9.149387041559e-01 | False | False |
| DEC3473_1_project_status | The coupling problem is not a single missing coefficient; it is a two-dimensional unresolved source family after current WEP rows. | parent theorem or independent clock/R10/local rows are required to remove/bound the remaining null directions | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3474-Y5-R2FR-nullspace-killing-source-owner-contract-or-clock-R10-row.md | scripts/Y5_R2FR_3474_nullspace_killing_source_owner_contract_or_clock_R10_row.py | Target the two surviving full-DD null directions: either derive a parent source-owner clause that zeros them, or add an independent clock/R10/local row whose sensitivity is not in the current WEP row span. | At least one null direction is killed by theorem or by a sourced independent arena row; no single-channel ceiling is treated as evidence. | GitHub action; formalization-workbench edits; public WEP/local-GR claim; cancellation-tuned coefficient choices. | False | False |

## Source Register
| timestamp_utc | source_id | source_type | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-29T03:05:19.632298+00:00 | script_3473 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3473_full_DD_multiarena_rank_or_parent_source_owner_proof.py | True | generator | False |
| 2026-06-29T03:05:19.632298+00:00 | doc_3472 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3472-Y5-R2FR-visible-source-owner-theorem-or-full-DD-vector-upgrade.md | True | 3472 handoff | False |
| 2026-06-29T03:05:19.632298+00:00 | next_3472 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_NEXT_TARGET.csv | True | 3473 target statement | False |
| 2026-06-29T03:05:19.632298+00:00 | theorem_3472 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv | True | source-owner theorem attempt | False |
| 2026-06-29T03:05:19.632298+00:00 | microscope_3472 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3472_DD_FOUR_CHARGE_PAIR_VECTOR.csv | True | full DD MICROSCOPE pair vector | False |
| 2026-06-29T03:05:19.632298+00:00 | matrix_3265 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv | True | two-arena eta bounds and reduced DD rows | False |
| 2026-06-29T03:05:19.632298+00:00 | material_3265 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv | True | Eot-Wash Be/Ti A/Z material context | False |
| 2026-06-29T03:05:19.632298+00:00 | eotwash_source | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external-sources\eotwash_0712.0607_source\ep.tex | True | Eot-Wash Be/Ti source | False |
| 2026-06-29T03:05:19.632298+00:00 | dd_tex | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external-sources\damour_donoghue_1007.2792_source\DamourDonoghueEPfinal.tex | True | Damour-Donoghue full four-charge formulas | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3473_0_sources_exist | True | all local sources exist | False |
| VAL3473_1_csv_parse | True | all output csv files parse | False |
| VAL3473_2_matrix_shape | True | rows=2; cols=4 | False |
| VAL3473_3_matrix_finite | True | all matrix values finite | False |
| VAL3473_4_rank_two | True | rank=2 | False |
| VAL3473_5_nullspace_dim_two | True | dim=2; basis_rows=2 | False |
| VAL3473_6_components_unbounded | True | all four component bounds remain nonclaim/unbounded | False |
| VAL3473_7_no_claim | True | all 3473 rows valid_for_claim=false | False |
| VAL3473_8_no_formalization_outputs | True | no outputs under formalization-workbench | False |
| VAL3473_9_git_formalization_clean | True | NOT_A_GIT_REPOSITORY | False |
| VAL3473_SUMMARY | True | PASS | False |
