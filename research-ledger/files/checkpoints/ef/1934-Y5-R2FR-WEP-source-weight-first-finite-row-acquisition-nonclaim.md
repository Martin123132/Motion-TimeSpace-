# 1934 Y5 R2FR: WEP Source-Weight First Finite Row Acquisition Nonclaim

## Verdict

1934 acquires a real source-backed MICROSCOPE Ti/Pt WEP bound as the first finite source-weight row. This is **not** an MTS WEP pass: the MTS projection from source-weight residuals to `eta_TiPt` is still missing.

Recorded bound: `eta_TiPt = -1.500e-15` with statistical sigma `2.300e-15`, systematic sigma `1.500e-15`, quadrature sigma `2.746e-15`, and reported no-violation level `2.700e-15`.

## Local Source Register

| branch_id | source_key | source_path | needed_for | needles | status | missing_needles | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1933-Y5-R2FR-coefficient-descent-typing-proof-or-finite-source-row-selection.md | 1934 WEP source-weight first finite nonclaim row | SEL1933_1_WEP_source_weight;VAL1933_OVERALL | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1933_VALIDATION.csv | 1934 WEP source-weight first finite nonclaim row | VAL1933_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_selection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1933_FINITE_ROW_SELECTION.csv | 1934 WEP source-weight first finite nonclaim row | SEL1933_1_WEP_source_weight;SELECTED_FIRST_FINITE_ROW | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_closure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1933_MINIMAL_CLOSURE.csv | 1934 WEP source-weight first finite nonclaim row | CLOS1933_0_minimal_descent_clause;EXPLICIT_CLOSURE_UNLESS_PARENT_SIGNED | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1933_CLAIM_GATE.csv | 1934 WEP source-weight first finite nonclaim row | CG1933_3_WEP_finite_row;FAIL_BLOCKED | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1933_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1933_NEXT_TARGET.csv | 1934 WEP source-weight first finite nonclaim row | NEXT1933_0_primary;WEP-source-weight | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Web Source Register

| branch_id | web_source_id | title | url | doi | journal_reference | used_for | extraction_method | confidence | status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1934_0_MICROSCOPE_PRL | MICROSCOPE mission: final results of the test of the Equivalence Principle | https://arxiv.org/abs/2209.15487 | https://doi.org/10.1103/PhysRevLett.129.121102 | Phys. Rev. Lett. 129, 121102 (2022) | modern WEP mission anchor and Ti/Pt eta result | web_browse_arxiv_abstract_2026-06-19 | high | WEB_SOURCE_RECORDED | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEB1934_1_MICROSCOPE_CQG | Result of the MICROSCOPE Weak Equivalence Principle test | https://arxiv.org/abs/2209.15488 | https://doi.org/10.1088/1361-6382/ac84be | Class. Quantum Grav. 39, 204009 (2022) | eta definition, combined 2.7e-15 level, same-material null check | web_browse_arxiv_abstract_2026-06-19 | high | WEB_SOURCE_RECORDED | False | False | 2026-06-19T22:28:31.175321+00:00 |

## WEP Bound Row

| branch_id | bound_id | observable | definition | test_masses | central_value | stat_sigma | syst_sigma | combined_sigma_quadrature | reported_no_violation_level_abs_eta | same_material_null_sigma_PtPt | units | source_url | source_doi | crosscheck_url | crosscheck_doi | extraction_status | valid_for_claim | claim_allowed | claim_blocker | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | WEP1934_0_MICROSCOPE_TiPt_eta | eta_Ti_Pt | eta(A,B)=2(a_A-a_B)/(a_A+a_B) | Titanium alloy; Platinum alloy | -1.5e-15 | 2.3e-15 | 1.5e-15 | 2.745906043549196e-15 | 2.7e-15 | 1.1e-15 | dimensionless | https://arxiv.org/abs/2209.15488 | https://doi.org/10.1088/1361-6382/ac84be | https://arxiv.org/abs/2209.15487 | https://doi.org/10.1103/PhysRevLett.129.121102 | SOURCE_BACKED_OBSERVABLE_BOUND | False | False | MTS source-weight-to-eta projection and material charges are not yet derived | 2026-06-19T22:28:31.175321+00:00 |

## MTS Projection Requirements

| branch_id | requirement_id | needed_input | target_formula_or_object | status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_0_projection_map | derive eta_pred from MTS source-weight residual | eta_pred = P_WEP[Delta w_TiPt, tau_WEP, source field, Earth composition] | MISSING_MTS_PROJECTION_MAP | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_1_material_charges | define MTS charges for Ti alloy and Pt alloy | Delta Q_TiPt or equivalent composition sensitivity | MISSING_MATERIAL_CHARGE_LEDGER | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_2_tau_WEP | derive or source tau_WEP normalization | dimensionless transfer from local source residual to differential acceleration | MISSING_TAU_WEP | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_3_environment_source | define Earth/source environment entering the WEP test | source field, gradient, orbital configuration, screening/plateau assumptions | MISSING_ARENA_SOURCE_MODEL | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_4_sign_units | fix sign and unit convention | eta_pred must be dimensionless and comparable to MICROSCOPE eta | MISSING_UNIT_SIGN_CONTRACT | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | REQ1934_5_acceptance_rule | define bound comparison rule | abs(eta_pred) <= selected eta bound with declared confidence level | MISSING_ACCEPTANCE_RULE | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Nonclaim Smoke Row

| branch_id | smoke_id | observable | eta_bound_abs | eta_bound_units | mts_prediction_symbolic | Delta_w_TiPt | tau_WEP | Q_Earth | local_source_profile | comparison_status | valid_for_claim | claim_allowed | claim_blocker | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SMOKE1934_0_MTS_WEP_source_weight_placeholder | eta_Ti_Pt | 2.7e-15 | dimensionless | eta_pred = P_WEP(Delta_w_TiPt, tau_WEP, Q_Earth, local_source_profile) | MISSING_MTS_SOURCE_WEIGHT_DIFFERENCE | MISSING_TAU_WEP | MISSING_SOURCE_ENVIRONMENT | MISSING_LOCAL_PROFILE | SCHEMA_READY_NUMERIC_CLAIM_BLOCKED | False | False | symbolic MTS inputs are placeholders | 2026-06-19T22:28:31.175321+00:00 |

## Claim Gate

| branch_id | gate_id | claim | status | reason | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_0_source_bound | MICROSCOPE WEP observable bound is source-backed | PASS_NONCLAIM | real eta bound row recorded with URL and DOI | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_1_mts_projection | MTS predicts eta_Ti_Pt numerically | FAIL_BLOCKED | projection map and material charges missing | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_2_tau_WEP | tau_WEP is derived or sourced | FAIL_BLOCKED | tau_WEP remains missing | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_3_WEP_pass | MTS passes MICROSCOPE WEP | FAIL_BLOCKED | no numeric eta_pred comparison allowed | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_4_local_GR_Newton | local GR/Newton source coupling is derived | FAIL_BLOCKED | WEP row is evidence plumbing, not source-coupling theorem | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1934_5_public_claim | 1934 supports public WEP/local-GR claim | FAIL_BLOCKED | all MTS rows remain claim=false | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Decision Ledger

| branch_id | decision_id | decision | rationale | next_action | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1934_0_bound_acquired | MICROSCOPE_TIPT_BOUND_ACQUIRED_NONCLAIM | This is the cleanest modern WEP source bound for composition-dependent acceleration. | derive the MTS WEP projection map before any pass/fail comparison | False | False | 2026-06-19T22:28:31.175321+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1934_1_claim_status | NO_WEP_OR_LOCAL_GR_CLAIM | A real experimental bound does not become an MTS test until eta_pred is derived from MTS quantities. | build material charge and tau_WEP requirements ledger | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Next Target

| branch_id | route_id | selection_status | target_doc | target_script | objective | success_condition | do_not | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1934_0_primary | selected | 1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md | scripts/Y5_R2FR_MTS_WEP_eta_projection_map_or_material_charge_ledger_1935.py | derive eta_pred for MICROSCOPE Ti/Pt from MTS source-weight residuals, or create a material-charge/tau_WEP ledger that keeps the WEP comparison blocked | a symbolic-to-numeric MTS WEP projection contract with all needed inputs named, or an explicit blocker ledger with claim=false | do not set tau_WEP=1, invent Ti/Pt material charges, absorb Delta w into measured G, claim WEP pass, claim local GR, or modify formalization-workbench | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Project Status Snapshot

| branch_id | snapshot_id | status | summary | strongest_result | missing_piece | claim_position | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1934_0_project_position | REAL_WEP_BOUND_ACQUIRED_NONCLAIM | 1934 adds a source-backed MICROSCOPE Ti/Pt eta bound but does not treat it as an MTS pass. | eta_TiPt central=-1.500e-15, combined_sigma=2.746e-15, reported level=2.700e-15 | MTS eta projection map, Ti/Pt material charges, tau_WEP, and acceptance rule | WEP/local-GR/Newton claims remain blocked | False | False | 2026-06-19T22:28:31.175321+00:00 |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1934_00_local_sources | PASS | all local source paths exist and needles found | False | False |
| VAL1934_01_web_sources | PASS | MICROSCOPE web sources recorded with arXiv URLs | False | False |
| VAL1934_02_bound_row | PASS | positive dimensionless eta bound with DOI recorded | False | False |
| VAL1934_03_projection_requirements | PASS | MTS projection blockers explicitly named | False | False |
| VAL1934_04_nonclaim_smoke | PASS | smoke row remains symbolic and blocked | False | False |
| VAL1934_05_claim_gates | PASS | only source-bound gate passes as nonclaim; all claim flags false | False | False |
| VAL1934_06_decision | PASS | bound acquired decision recorded | False | False |
| VAL1934_07_next_target | PASS | 1935 MTS WEP projection target selected | False | False |
| VAL1934_08_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1934_09_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1934_10_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\MICROSCOPE_WEP_SOURCE_WEIGHT_BOUND_ROW_1934_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\P8_Y5_PARENT_QLOC_1934_WEP_BOUND_ROW_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1934_MTS_WEP_PROJECTION_MAP_ACQUISITION_QUEUE.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1934\P8_Y5_PARENT_QLOC_1934_CLAIM_GATE.csv | False | False |
| VAL1934_11_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1934_12_formalization_untouched | PASS | formalization_1934_artifact_count=0 | False | False |
| VAL1934_OVERALL | PASS | 1934 WEP source-weight first finite row acquisition nonclaim | False | False |
