# 2475 Y5 R2FR First Real Local Arena Coefficient Source Acquisition

**Status:** first real local arena bound anchor acquired, but no MTS local-test claim is allowed. The R10/Eöt-Wash 2020 alpha=1 threshold at lambda 38.6 micrometers is source-backed by PRL/PubMed/arXiv metadata. The stress-bound runner remains blocked because `E_GK_bound`, `C_metric`, and `K_R10` are still missing.

**Meaning:** this reduces the external-bound side of the local test pipeline. It does not reduce the theory-side coefficient gap. The next step is the harder bridge: map GK stress residuals to a Yukawa alpha(lambda) kernel without fitted-GM or M_H_ref shortcuts.

## Source Register
| source_id | source_path | exists | missing_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2475_00_2474_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md | True |  | True | handoff selecting first real coefficient/bound source acquisition |
| SRC2475_01_2473_missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv | True |  | True | missing local arena kernel/bound inputs |
| SRC2475_02_R10_provenance | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_BOUND_SOURCE_PROVENANCE.csv | True |  | True | R10 source-backed threshold provenance |
| SRC2475_03_R10_candidate_QA | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv | True |  | True | local QA for vector curve review candidate |
| SRC2475_04_R10_review_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True |  | True | nonclaim digitized candidate curve with recovered alpha=1 anchor |

## Acquisition Ledger
| acquisition_id | arena | source_id | title | source_url | doi | extraction_method | acquired_content | acquisition_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACQ2475_0_R10_anchor | R10_short_range | EOTWASH_2020_PRL124101101 | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761; https://doi.org/10.1103/PhysRevLett.124.101101 | 10.1103/PhysRevLett.124.101101 | 95_percent_gravitational_strength_Yukawa_threshold_anchor | alpha=1 excluded for lambda >= 38.6 micrometers | SOURCE_BACKED_ANCHOR_NONCURVE | nonclaim because this is an external bound anchor, not an MTS stress prediction coefficient |
| ACQ2475_1_R10_review_curve | R10_short_range | R10_VECTOR_2020_REVIEW_CANDIDATE | Eot-Wash 2020 Fig. 5b vector candidate | local file: source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | 10.1103/PhysRevLett.124.101101 | axis_calibrated_vector_path_extraction_review_candidate | 390 candidate alpha(lambda) rows; alpha=1 anchor recovery passes review candidate QA | REVIEW_CANDIDATE_NONCLAIM | requires official supplemental table or human visual QA before any live claim use |
| ACQ2475_2_PPN | PPN_solar_system | not_acquired | PPN bound source |  |  | not_attempted_this_checkpoint | deferred because R10 source hierarchy was already locally staged | BLOCKED_DEFERRED | future source acquisition needed |

## Candidate Bound Rows
| bound_id | arena | bound_kind | lambda_value | lambda_units | bound_symbol | bound_value | bound_units | confidence | source_id | source_path_or_url | data_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND2475_R10_ANCHOR_ALPHA1_38P6UM | R10_short_range | lambda_threshold | 3.86e-05 | m | alpha_bound | 1.0 | dimensionless | 95_percent | EOTWASH_2020_PRL124101101 | https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761 | anchor_only_non_curve | False |
| BOUND2475_R10_REVIEW_NEAREST_ALPHA1 | R10_short_range | lambda_candidate_nearest_alpha1 | 3.866316691563022e-05 | m | alpha_bound | 0.9915372447041295 | dimensionless | review_candidate | R10_VECTOR_2020_REVIEW_0154 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | review_candidate_requires_human_or_official_QA | False |

## Runner Input Candidates
| runner_input_id | arena | E_GK_bound | C_metric | K_arena | arena_bound | units | bound_row_id | valid_for_claim | block_reasons | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN2475_R10_ANCHOR_INPUT | R10_short_range |  |  |  | 1.0 | dimensionless | BOUND2475_R10_ANCHOR_ALPHA1_38P6UM | False | MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;ANCHOR_ONLY_NONCURVE | False |
| RUN2475_R10_REVIEW_INPUT | R10_short_range |  |  |  | 0.9915372447041295 | dimensionless | BOUND2475_R10_REVIEW_NEAREST_ALPHA1 | False | MISSING_E_GK_BOUND;MISSING_C_METRIC;MISSING_K_R10;REVIEW_CANDIDATE_NONCLAIM | False |

## Units Validation
| validation_id | target_id | lambda_units_ok | bound_units_ok | status | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| UNIT2475_BOUND2475_R10_ANCHOR_ALPHA1_38P6UM | BOUND2475_R10_ANCHOR_ALPHA1_38P6UM | True | True | PASS_UNITS_NONCLAIM | False |
| UNIT2475_BOUND2475_R10_REVIEW_NEAREST_ALPHA1 | BOUND2475_R10_REVIEW_NEAREST_ALPHA1 | True | True | PASS_UNITS_NONCLAIM | False |
| UNIT2475_RUN2475_R10_ANCHOR_INPUT | RUN2475_R10_ANCHOR_INPUT | not_applicable | True | BLOCKED_MISSING_RUNNER_COEFFICIENTS | False |
| UNIT2475_RUN2475_R10_REVIEW_INPUT | RUN2475_R10_REVIEW_INPUT | not_applicable | True | BLOCKED_MISSING_RUNNER_COEFFICIENTS | False |

## Claim Gates
| gate_id | claim | gate_status | reason | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE2475_0_real_bound_anchor | A real source-backed R10 bound anchor is recorded. | PASS_AS_BOUND_SOURCE | Eot-Wash 2020 alpha=1 threshold anchor recorded with DOI/URLs | True | False |
| GATE2475_1_full_curve | A full valid-for-claim alpha(lambda) curve is acquired. | BLOCKED | digitized curve remains review_candidate_nonclaim | False | False |
| GATE2475_2_runner_claim | Runner has enough sourced MTS coefficients to claim local compatibility. | BLOCKED | E_GK_bound, C_metric and K_R10 missing | False | False |
| GATE2475_3_no_fitted_GM | No fitted-GM shortcut used. | PASS_GUARDRAIL | R10 source anchor does not define MTS source strength by orbital GM | True | False |
| GATE2475_4_local_GR | local GR/PPN branch passes. | BLOCKED | external bound acquisition is not a GR derivation | False | False |
| GATE2475_5_no_GitHub | No public/GitHub update. | PASS_GUARDRAIL | private source acquisition only | True | False |

## Decision Ledger
| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC2475_0_anchor_acquired | Keep Eöt-Wash 2020 as first real R10 bound anchor. | source-backed DOI/URL and threshold value are available | bound source gap partially reduced |
| DEC2475_1_no_curve_promotion | Do not promote the digitized curve. | review candidate still needs official supplemental table or human visual QA | claim discipline retained |
| DEC2475_2_next | Next source or derive K_R10/C_metric/E_GK_bound mapping. | external bound alone cannot run the stress-bound test | 2476 selected |

## Next Target
| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2475_0_selected | selected | 2476-Y5-R2FR-R10-kernel-and-Cmetric-source-map-or-blocker.md | scripts/Y5_R2FR_R10_kernel_and_Cmetric_source_map_or_blocker_2476.py | try to source or derive the R10 arena kernel K_R10 and C_metric mapping from GK stress bound to alpha(lambda); if absent, write a blocker ledger | kernel/mapping source audit, dimensional bridge, missing coefficient blocker, no fitted-GM guardrail, claim gates | no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists |
| --- | --- | --- | --- | --- |
| candidate_bound_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_first_real_local_bound_candidates_2475_NONCLAIM.csv | True | True |
| runner_input_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_first_real_runner_input_candidates_2475_NONCLAIM.csv | True | True |
| acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_ACQUISITION_LEDGER.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2475_FIRST_REAL_LOCAL_BOUND_ACQUISITION_NONCLAIM.csv | True | True |

## Validation
| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2475_00_sources_exist | PASS | all cited local source paths exist and needles are present |  |
| VAL2475_01_real_anchor | PASS | R10 alpha=1 threshold anchor recorded |  |
| VAL2475_02_urls_doi | PASS | source URL and DOI recorded |  |
| VAL2475_03_units | PASS | units validation rows pass or block as expected |  |
| VAL2475_04_runner_blocked | PASS | runner input candidates remain nonclaim |  |
| VAL2475_05_missing_coefficients | PASS | runner rows still block missing MTS coefficients |  |
| VAL2475_06_claim_gates_safe | PASS | no claim gate allows local-GR/R10 claim |  |
| VAL2475_07_next_target_written | PASS | 2476 R10 kernel/Cmetric source map selected |  |
| VAL2475_08_branch_copies | PASS | nonclaim branch copies exist |  |
| VAL2475_09_no_formalization_artifacts | PASS | no 2475 artifacts were written to formalization-workbench |  |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_SOURCE_REGISTER | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_SOURCE_REGISTER.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_ACQUISITION_LEDGER | PASS | CSV parses with 3 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_ACQUISITION_LEDGER.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS | PASS | CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES | PASS | CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_UNITS_VALIDATION | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_UNITS_VALIDATION.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_CLAIM_GATES | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_CLAIM_GATES.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_DECISION_LEDGER | PASS | CSV parses with 3 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_DECISION_LEDGER.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_NEXT_TARGET | PASS | CSV parses with 1 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_NEXT_TARGET.csv |
| VAL2475_CSV_P8_Y5_GK_BOUND_SOURCE_2475_BRANCH_COPIES | PASS | CSV parses with 3 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_BOUND_SOURCE_2475_BRANCH_COPIES.csv |
| VAL2475_COPY_CSV_candidate_bound_rows | PASS | copy CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_first_real_local_bound_candidates_2475_NONCLAIM.csv |
| VAL2475_COPY_CSV_runner_input_candidates | PASS | copy CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\GK_first_real_runner_input_candidates_2475_NONCLAIM.csv |
| VAL2475_COPY_CSV_acquisition_queue | PASS | copy CSV parses with 3 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2475_FIRST_REAL_LOCAL_BOUND_ACQUISITION_NONCLAIM.csv |
| VAL2475_OVERALL | PASS | 2475 acquires a real R10 bound anchor but keeps MTS runner claims blocked pending kernel/Cmetric/E_GK coefficients |  |
