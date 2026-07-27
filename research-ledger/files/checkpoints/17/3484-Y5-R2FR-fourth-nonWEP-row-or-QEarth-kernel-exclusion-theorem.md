# 3484: Fourth Non-WEP Row Or `Q_Earth` Kernel Exclusion Theorem

## Current Verdict
- The 3483 blind direction is real and is dominantly `D_delta_m_eff`.
- A fourth non-WEP row can close the same-vector branch only if it projects onto that blind vector.
- The local CSV scan was performed instead of guessing; no row is promoted to a claim.
- Three primary hyperfine/isotope candidate sources were acquired locally for the next extraction pass.

## Blind Probe
| probe_id | D_hatm_eff | D_delta_m_eff | D_me_eff | D_e_eff | interpretation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PROBE3484_0_current_blind_vector | -5.503904639594e-04 | 9.999998477930e-01 | 3.852733247716e-05 | -0.000000000000e+00 | the surviving same-vector blind direction is overwhelmingly D_delta_m_eff-like | False |
| PROBE3484_1_current_rank |  |  |  |  | rank(Q_Earth plus current two clock rows)=3; need rank 4 or parent exclusion of the blind kernel | False |

## Projection Theorems
| theorem_id | statement | proof | result | valid_for_claim |
| --- | --- | --- | --- | --- |
| THM3484_0_projection_gate | A fourth non-WEP row closes the current same-vector blind direction only if its vector has nonzero projection on the 3483 null vector. | The current row span has codimension one; a new row raises rank from 3 to 4 exactly when it is not orthogonal to the null vector. | scanner found 5 row(s) that algebraically close rank before source/claim filtering; 0 are claim-valid rows. | False |
| THM3484_1_delta_m_target | The missing direction is dominantly D_delta_m_eff, so another alpha/me/hatm-only clock row is unlikely to close the local branch. | The 3483 null vector has unit component nearly entirely in D_delta_m_eff. | target hyperfine/isotope sources must be basis-mapped before use; quark-mass average sensitivity is not automatically D_delta_m_eff sensitivity. | False |

## Scan Summary
- Files scanned: `30388`
- Rows scanned: `230951`
- Numeric four-channel vectors found: `12`
- Blind vector used: `(-5.503904639594e-04, 9.999998477930e-01, 3.852733247716e-05, -0.000000000000e+00)`

## External Acquisition Targets
| target_id | local_source_path | source_url | needed_extraction | projection_test | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EXT3484_0_hyperfine_nuclear_magnetic_moments | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external_sources\Flambaum_Tedesco_2006_nuclear_magnetic_moments_quark_masses_atomic_clocks.pdf | https://arxiv.org/abs/nucl-th/0601050 | sensitivity vector in DD four-channel basis, especially whether any term maps to D_delta_m_eff rather than only D_hatm_eff | abs(row dot u_blind_3483) > 0 after basis mapping | SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING | False |
| EXT3484_1_isotope_comparison_quark_mass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external_sources\Berengut_Flambaum_Kava_2011_isotope_comparisons_quark_mass_variation.pdf | https://arxiv.org/abs/1109.1893 | isotope clock/comparison sensitivity to quark-mass variation and its map to the D_delta_m_eff blind direction | abs(row dot u_blind_3483) > 0 after basis mapping | SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING | False |
| EXT3484_2_hyperfine_radius_quark_mass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external_sources\Dinh_Dunning_Dzuba_Flambaum_2009_hyperfine_radius_quark_mass_variation.pdf | https://arxiv.org/abs/0903.2090 | hyperfine/radius sensitivity row; reject if it only spans already-covered hatm/me/e directions | abs(row dot u_blind_3483) > 0 after basis mapping | SOURCE_ACQUIRED_COEFFICIENT_EXTRACTION_PENDING | False |

## Top Local Projection Candidates
| candidate_id | file | line_hint | row_label | classification | projection_on_3483_blind | rank_if_added_to_QEarth_plus_clocks | closes_current_rank_if_source_valid | row_valid_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCAN3484_0001 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS.csv | 3 | P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS:3 | formula_or_charge_vector_not_observable | -9.869696695942e-01 | 4 | True | False | False |
| SCAN3484_0000 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS.csv | 2 | P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS:2 | formula_or_charge_vector_not_observable | 1.597268525343e-01 | 4 | True | False | False |
| SCAN3484_0002 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3474_AUGMENTED_NULLSPACE_BASIS.csv | 2 | P8_Y5_R2FR_3474_AUGMENTED_NULLSPACE_BASIS:2 | unclassified_numeric_vector | 1.597268525343e-01 | 4 | True | False | False |
| SCAN3484_0003 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3474_AUGMENTED_WEP_CLOCK_MATRIX.csv | 2 | MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | clock_or_clock_candidate | -5.771576369105e-02 | 4 | True | False | False |
| SCAN3484_0004 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3474_AUGMENTED_WEP_CLOCK_MATRIX.csv | 3 | MATRIX3473_1_EOTWASH_Be_minus_Ti | clock_or_clock_candidate | 7.788932762642e-03 | 4 | True | False | False |
| SCAN3484_0007 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv | 2 | MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | wep_row_forbidden_for_same_vector_linear_closure | -5.771576369105e-02 | 4 | False | False | False |
| SCAN3484_0008 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv | 3 | MATRIX3473_1_EOTWASH_Be_minus_Ti | wep_row_forbidden_for_same_vector_linear_closure | 7.788932762642e-03 | 4 | False | False | False |
| SCAN3484_0010 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv | 5 | MATRIX3475_3_CLOCK_SrCs_mu_q_alpha | clock_or_clock_candidate | -6.793204236979e-19 | 3 | False | False | False |
| SCAN3484_0011 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_CLOCK_MU_SENSITIVITY_SOURCE.csv | 2 | CLK3475_0_SrCs_mu_q_alpha | clock_or_clock_candidate | -6.793204236979e-19 | 3 | False | False | False |
| SCAN3484_0005 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3474_AUGMENTED_WEP_CLOCK_MATRIX.csv | 4 | MATRIX3474_2_CLOCK_YbE3E2_alpha | clock_or_clock_candidate | 0.000000000000e+00 | 3 | False | False | False |
| SCAN3484_0006 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3474_CLOCK_ALPHA_SENSITIVITY_ROW.csv | 2 | CLK3474_0_YbE3E2_alpha | clock_or_clock_candidate | 0.000000000000e+00 | 3 | False | False | False |
| SCAN3484_0009 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv | 4 | MATRIX3474_2_CLOCK_YbE3E2_alpha | clock_or_clock_candidate | 0.000000000000e+00 | 3 | False | False | False |

## Decisions
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3484_0_no_existing_claim_row | No existing row is promoted to a same-vector local-GR/WEP closure claim. | the scan is algebraic and source/transport filters remain nonclaim; WEP rows remain forbidden as linear closures on the same-vector branch. | False | False |
| DEC3484_1_best_attack | Extract one genuine non-WEP hyperfine/isotope sensitivity vector and test its projection on the 3483 blind vector. | 5 algebraic closing rows were found in local CSVs before claim filtering; external candidate sources are now local PDFs. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3485-Y5-R2FR-hyperfine-isotope-DD-basis-extraction-or-delta-m-kernel-exclusion.md | scripts/Y5_R2FR_3485_hyperfine_isotope_DD_basis_extraction_or_delta_m_kernel_exclusion.py | Extract a source-backed hyperfine/isotope sensitivity row into the DD four-channel basis and test whether it has nonzero projection on the 3483 blind vector. | rank(Q_Earth, current clock rows, new non-WEP row)=4 with sourced basis map, or parent theorem excludes the D_delta_m_eff-like kernel | mapping average quark-mass sensitivity to D_delta_m_eff without a source; using WEP rows linearly; claiming local GR | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3484_0_sources_exist | True | all local and acquired external sources exist | False |
| VAL3484_1_csv_parse | True | source_register:7; blind_probe:2; projection_theorems:2; existing_vector_scan:12; external_acquisition:3; decision_ledger:2; next_target:1 | False |
| VAL3484_2_scanner_coverage | True | files=30388; rows=230951; numeric_vectors=12 | False |
| VAL3484_3_current_rank_still_three | True | rank=3 | False |
| VAL3484_4_no_claim_valid_closure | True | candidate rows are scan/projection rows only | False |
| VAL3484_5_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3484_SUMMARY | True | PASS | False |

_Generated: 2026-06-29T04:27:23.690001+00:00_
