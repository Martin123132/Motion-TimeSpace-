# 1949 Y5 R2FR: R11 PTF Source or Kappa/CTF Normalization

## Verdict

1949 simplifies the Cassini gamma problem. The previous runner listed `kappa_R`, `C_TF`, `U_solar_frame`, inverse-Laplacian boundary data, and `P_TF[R11_ij]` separately. That is sufficient, but for the first Cassini smoke gate it is not minimal.

The observable combination is one dimensionless projected slip amplitude: `S_TF := -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]`. The runner can therefore become `abs(S_TF) <= gamma_bound_policy`.

This does not prove Cassini safety. It tightens the next target: either derive/source `S_TF` directly, prove `S_TF=0`, or later decompose it into `kappa_R/C_TF/P_TF` for cross-test consistency. Common-mode residuals remain outside this gamma-only compression.

## Source Register

| branch_id | source_id | source_path | purpose | required_needles | status | issue | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1948_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1948-Y5-R2FR-Cassini-slip-bound-smoke-runner-or-PTF-source-fill.md | 1949 R11 PTF source or kappa/CTF normalization | RUN1948_0_live_input_scan;NEXT1948_0_primary;VAL1948_OVERALL | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1948_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1948_VALIDATION.csv | 1949 R11 PTF source or kappa/CTF normalization | VAL1948_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1948_input_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_INPUT_AUDIT.csv | 1949 R11 PTF source or kappa/CTF normalization | AUD1948_1_SBI1947_1_kappa_R;AUD1948_5_SBI1947_6_PTF_amplitude | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1948_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_SMOKE_RUNNER.csv | 1949 R11 PTF source or kappa/CTF normalization | BLOCKED_MISSING_REQUIRED_INPUTS;BLOCKED_THEOREM_ZERO_NOT_PARENT_SIGNED | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1948_failures | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1948_CASSINI_SLIP_FAILURE_MODE_LEDGER.csv | 1949 R11 PTF source or kappa/CTF normalization | MISSING_KAPPA_R;MISSING_PROJECTED_R11_TF_AMPLITUDE | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1944_derivation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv | 1949 R11 PTF source or kappa/CTF normalization | WFE1944_5_delta_gamma_source_law;DELTA_GAMMA_SOURCE_LAW_SYMBOLIC | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CASSINI_BOUND_POLICY_CANDIDATES.csv | 1949 R11 PTF source or kappa/CTF normalization | CBP1947_2_abs_two_sigma_screen;6.700000e-05 | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_INPUT_LEDGER.csv | 1949 R11 PTF source or kappa/CTF normalization | SBI1947_0_gamma_bound_policy;SBI1947_6_PTF_amplitude | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Product Compression

| branch_id | compression_id | statement | result | runner_effect | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCOMP1949_0_start | 1944/1948 runner uses delta_gamma_R11 ~= -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]. | START_FROM_EXISTING_RUNNER_FORM | separate kappa_R, C_TF, U_solar, inverse-Laplacian, and P_TF inputs are sufficient but not minimal | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCOMP1949_1_define_dimensionless_slip | Define S_TF := -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij]. | OBSERVABLE_PRODUCT_DEFINED | Cassini gamma only needs S_TF, not each microscopic factor separately | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCOMP1949_2_acceptance_rule | The local Cassini smoke comparison becomes abs(S_TF) <= gamma_bound_policy. | RUNNER_RULE_COMPRESSED | a parent theorem S_TF=0 or a direct bound on S_TF is enough for the gamma gate | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCOMP1949_3_identifiability_guard | Cassini alone cannot identify kappa_R, C_TF, and P_TF separately if only their product enters the observable. | DO_NOT_OVERPARAMETERIZE_CASSINI_GATE | next work should fill S_TF directly or source a parent decomposition only if needed by other tests | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | PCOMP1949_4_common_mode_guard | This compression only covers traceless spatial gamma slip; common-mode r^2/effective-G terms stay in Newtonian/cosmology gates. | SCOPE_GUARD_RECORDED | prevents a Cassini-safe common mode from being mislabelled as local-GR proof | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Kappa/CTF/PTF Status

| branch_id | status_id | symbol | current_status | compressed_role | still_needed_separately_for | claim_impact | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | KCP1949_0_kappa_R | kappa_R | MISSING_SEPARATE_NORMALIZATION | absorbed into S_TF product for Cassini gamma | cross-test consistency, action normalization, and non-Cassini residual predictions | not separately fatal to Cassini smoke if S_TF is sourced directly | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | KCP1949_1_C_TF | C_TF | MISSING_WEAK_FIELD_NORMALIZATION | absorbed into S_TF product after convention/gauge choice | deriving PPN beta/alpha residuals and comparing independent gauges | not separately fatal to Cassini smoke if S_TF is sourced directly | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | KCP1949_2_PTF | P_TF[R11_ij] | MISSING_PROJECTED_R11_TF_AMPLITUDE | numerator of S_TF product | theorem-zero proof, source profile, and cross-arena predictions | fatal unless S_TF itself is theorem-zero or directly bounded | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | KCP1949_3_U_and_boundary | U_solar_frame,nabla^{-2}_local | MISSING_FRAME_AND_BOUNDARY_CONVENTION | included in dimensionless S_TF amplitude | turning an operator-level source into a solar-system observable | fatal unless S_TF is supplied as an already projected dimensionless observable | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Compressed Input Ledger

| branch_id | input_id | symbol | definition | current_value | units | status | source_ref | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CSI1949_0_gamma_bound_policy | gamma_bound_policy | private conservative Cassini screening threshold from 1947 | 6.700000e-05 | dimensionless | NUMERIC_POLICY_AVAILABLE_NONCLAIM | CBP1947_2_abs_two_sigma_screen | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CSI1949_1_S_TF | S_TF | -(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij] | MISSING | dimensionless | MISSING_COMPRESSED_SLIP_AMPLITUDE | PCOMP1949_1_define_dimensionless_slip | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CSI1949_2_S_TF_zero_theorem | S_TF=0 | parent-signed theorem-zero route equivalent to P_TF zero or projected slip silence | NOT_PARENT_SIGNED | boolean/theorem | MISSING_PARENT_SIGNED_ZERO_THEOREM | RUN1948_1_theorem_zero_branch | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Runner Update

| branch_id | runner_id | prediction | acceptance_rule | current_prediction | runner_status | missing_inputs | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1949_0_compressed_schema | delta_gamma_R11 ~= S_TF | abs(S_TF) <= gamma_bound_policy | MISSING_COMPRESSED_SLIP_AMPLITUDE | SCHEMA_SIMPLIFIED_INPUTS_MISSING | S_TF or parent-signed S_TF=0 | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1949_1_theorem_zero_shortcut | S_TF=0 | 0 <= gamma_bound_policy | NOT_PARENT_SIGNED | WOULD_PASS_IF_PARENT_SIGNED_BLOCKED | parent-signed projected slip zero theorem | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Claim Gate

| branch_id | gate_id | claim | status | reason | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_0_product_compression | Cassini gamma slip gate can be compressed to one dimensionless S_TF product. | PASS_NONCLAIM | algebraic compression follows from the 1944/1948 runner equation | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_1_overparameterization_guard | Separate kappa_R/C_TF/P_TF are not individually required for a first Cassini smoke comparison if S_TF is supplied. | PASS_NONCLAIM | only the product enters delta_gamma_R11 at this order | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_2_S_TF_numeric | MTS supplies numeric S_TF. | FAIL_BLOCKED | compressed slip amplitude is missing | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_3_S_TF_zero_theorem | MTS parent signs S_TF=0. | FAIL_BLOCKED | projected slip zero theorem remains unsigned | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_4_Cassini_pass | MTS passes Cassini gamma. | FAIL_BLOCKED | no numeric or theorem-zero S_TF exists | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_5_local_GR_PPN | MTS derives local GR/PPN. | FAIL_BLOCKED | Cassini S_TF and other PPN residuals remain open | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1949_6_public_claim | 1949 is public-ready Cassini/local-GR evidence. | FAIL_BLOCKED | private compression checkpoint only | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Decision Ledger

| branch_id | decision_id | decision | reason | next_action | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1949_0_compression | CASSINI_GATE_REDUCED_TO_S_TF | the observable only sees the dimensionless projected slip product at leading weak-field order | fill S_TF directly, prove S_TF=0, or only then decompose into kappa_R/C_TF/P_TF for cross-test consistency | False | False | 2026-06-19T23:36:24.954976+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1949_1_primary_target | TARGET_DIMENSIONLESS_STF_SOURCE_NEXT | one projected observable amplitude is a cleaner first target than three separately unidentifiable factors | derive/source S_TF from R11 local operator, or prove projected slip zero | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Next Target

| branch_id | next_id | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1949_0_primary | selected | 1950-Y5-R2FR-dimensionless-STF-slip-source-or-zero-theorem.md | scripts/Y5_R2FR_dimensionless_STF_slip_source_or_zero_theorem_1950.py | derive/source the compressed dimensionless slip amplitude S_TF or prove S_TF=0 from the local R11 branch | numeric/source-backed S_TF row, parent-signed S_TF=0 theorem, or explicit blocker ledger keeping Cassini blocked | do not claim Cassini/local-GR pass unless S_TF is numeric below bound or theorem-zero | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Project Status Snapshot

| branch_id | snapshot_id | status | strongest_result | what_improved | still_missing | claim_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1949_0_project_position | CASSINI_GATE_COMPRESSED_TO_DIMENSIONLESS_STF_SLIP_AMPLITUDE | delta_gamma_R11 ~= S_TF, where S_TF=-(kappa_R/(C_TF U_solar)) nabla^{-2}_local P_TF[R11_ij] | the next local-GR target is one observable amplitude rather than a pile of separately unidentifiable coefficients | numeric/source-backed S_TF or parent-signed S_TF=0 theorem | Cassini/local-GR public claims remain blocked | False | False | 2026-06-19T23:36:24.954976+00:00 |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1949_00_sources | PASS | all local source paths exist and needles found | False | False |
| VAL1949_01_product_compression | PASS | S_TF product and runner rule defined | False | False |
| VAL1949_02_coefficient_status | PASS | coefficient statuses remain nonclaim and PTF tracked | False | False |
| VAL1949_03_compressed_inputs | PASS | compressed S_TF input missing as intended | False | False |
| VAL1949_04_runner_update | PASS | compressed runner schema remains blocked | False | False |
| VAL1949_05_claim_gates | PASS | only compression nonclaim gates pass; claims blocked | False | False |
| VAL1949_06_decision | PASS | dimensionless STF source selected | False | False |
| VAL1949_07_next_target | PASS | 1950 S_TF target selected | False | False |
| VAL1949_08_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1949_09_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1949_10_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\CASSINI_PRODUCT_COMPRESSION_1949_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\P8_Y5_PARENT_QLOC_1949_CLAIM_GATE_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1949_DIMENSIONLESS_STF_SOURCE_OR_ZERO_THEOREM_QUEUE.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1949\P8_Y5_PARENT_QLOC_1949_CLAIM_GATE.csv | False | False |
| VAL1949_11_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1949_12_formalization_untouched | PASS | formalization_1949_artifact_count=0 | False | False |
| VAL1949_OVERALL | PASS | 1949 R11 PTF source or kappa CTF normalization | False | False |
