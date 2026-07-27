# 1948 Y5 R2FR: Cassini Slip Bound Smoke Runner or PTF Source Fill

## Verdict

1948 turns the Cassini gamma branch into an executable discipline gate. The runner reads the 1947 input ledger, accepts the private conservative screening value `gamma_bound_policy=6.7e-5`, then refuses to evaluate `delta_gamma_R11` because the MTS-side inputs are still missing.

This is good failure, not dead-end failure. The local-GR branch now has a runner that blocks precisely on `kappa_R`, `C_TF`, `U_solar_frame`, the boundary-conditioned inverse Laplacian, and `P_TF[R11_ij]`. The theorem-zero branch also blocks unless `P_TF[R11_ij]=0` is parent-signed.

Next target: fill or derive the first real `P_TF/kappa_R/C_TF` row from the R11 operator branch, or prove the parent-zero theorem. Until then, no Cassini/local-GR claim.

## Source Register

| branch_id | source_id | source_path | purpose | required_needles | status | issue | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1947-Y5-R2FR-boundary-kernel-isotropy-or-Cassini-slip-bound-inputs.md | 1948 Cassini slip bound smoke runner | RUN1947_0_slip_bound_schema;SBI1947_1_kappa_R;VAL1947_OVERALL | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1947_VALIDATION.csv | 1948 Cassini slip bound smoke runner | VAL1947_OVERALL;PASS | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_INPUT_LEDGER.csv | 1948 Cassini slip bound smoke runner | SBI1947_0_gamma_bound_policy;MISSING_PROJECTED_R11_TF_AMPLITUDE | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_RUNNER_SCHEMA.csv | 1948 Cassini slip bound smoke runner | RUN1947_0_slip_bound_schema;SCHEMA_READY_INPUTS_MISSING | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CASSINI_BOUND_POLICY_CANDIDATES.csv | 1948 Cassini slip bound smoke runner | CBP1947_2_abs_two_sigma_screen;6.700000e-05 | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1947_claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1947_CLAIM_GATE.csv | 1948 Cassini slip bound smoke runner | CG1947_3_numeric_slip_prediction;FAIL_BLOCKED | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1944_derivation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv | 1948 Cassini slip bound smoke runner | WFE1944_5_delta_gamma_source_law;P_TF[R11_ij] | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | 1942_web | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1942_WEB_SOURCE_REGISTER.csv | 1948 Cassini slip bound smoke runner | WEB1942_0_CASSINI_GAMMA;nature01997 | EXISTS_NEEDLES_CONFIRMED |  | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Input Audit

| branch_id | audit_id | symbol | source_input_id | source_status | current_value | numeric_available | required_for_numeric_runner | audit_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_0_SBI1947_0_gamma_bound_policy | gamma_bound_policy | SBI1947_0_gamma_bound_policy | CANDIDATE_POLICY_ONLY_NOT_FINAL_CLAIM_RULE | 6.700000e-05 | True | True | NUMERIC_POSITIVE_AVAILABLE_NONCLAIM | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_1_SBI1947_1_kappa_R | kappa_R | SBI1947_1_kappa_R | MISSING_KAPPA_R | MISSING | False | True | MISSING_KAPPA_R | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_2_SBI1947_2_C_TF | C_TF | SBI1947_2_C_TF | MISSING_C_TF | MISSING | False | True | MISSING_C_TF | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_3_SBI1947_3_U_solar_frame | U_solar_frame | SBI1947_3_U_solar_frame | MISSING_U_SOLAR_FRAME | MISSING | False | True | MISSING_U_SOLAR_FRAME | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_4_SBI1947_4_inverse_laplacian | nabla^{-2}_local | SBI1947_4_inverse_laplacian | MISSING_BOUNDARY_CONDITIONED_INVERSE_LAPLACIAN | MISSING | False | True | MISSING_BOUNDARY_CONDITIONED_INVERSE_LAPLACIAN | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_5_SBI1947_6_PTF_amplitude | P_TF[R11_ij] | SBI1947_6_PTF_amplitude | MISSING_PROJECTED_R11_TF_AMPLITUDE | MISSING | False | True | MISSING_PROJECTED_R11_TF_AMPLITUDE | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | AUD1948_6_source_profile | source_profile/worldtube | SBI1947_5_source_profile | MISSING_SOURCE_PROFILE_AND_AVERAGING | MISSING | False | False | MISSING_PROFILE_FOR_REFINED_RUNNER | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Smoke Runner

| branch_id | runner_id | branch | can_run_numeric | numeric_prediction | bound_policy | comparison | runner_status | missing_inputs | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1948_0_live_input_scan | live_1947_inputs | False | NOT_EVALUATED | 6.700000e-05 | NOT_EVALUATED_MISSING_INPUTS | BLOCKED_MISSING_REQUIRED_INPUTS | kappa_R;C_TF;U_solar_frame;nabla^{-2}_local;P_TF[R11_ij] | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1948_1_theorem_zero_branch | theorem_zero_P_TF | False | 0 if P_TF[R11_ij]=0 is parent-signed | 6.700000e-05 | WOULD_PASS_IF_THEOREM_SIGNED | BLOCKED_THEOREM_ZERO_NOT_PARENT_SIGNED | PARENT_SIGNED_P_TF_ZERO_THEOREM | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | RUN1948_2_numeric_comparison | numeric | False | NOT_EVALUATED | 6.700000e-05 | NOT_EVALUATED_MISSING_INPUTS | BLOCKED_MISSING_REQUIRED_INPUTS | kappa_R;C_TF;U_solar_frame;nabla^{-2}_local;P_TF[R11_ij] | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Failure Mode Ledger

| branch_id | failure_id | symbol | failure_mode | effect_on_runner | required_fix | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_0_SBI1947_1_kappa_R | kappa_R | MISSING_KAPPA_R | numeric Cassini slip comparison blocked | derive or source numeric kappa_R with units and source path | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_1_SBI1947_2_C_TF | C_TF | MISSING_C_TF | numeric Cassini slip comparison blocked | derive or source numeric C_TF with units and source path | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_2_SBI1947_3_U_solar_frame | U_solar_frame | MISSING_U_SOLAR_FRAME | numeric Cassini slip comparison blocked | derive or source numeric U_solar_frame with units and source path | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_3_SBI1947_4_inverse_laplacian | nabla^{-2}_local | MISSING_BOUNDARY_CONDITIONED_INVERSE_LAPLACIAN | numeric Cassini slip comparison blocked | derive or source numeric nabla^{-2}_local with units and source path | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_4_SBI1947_6_PTF_amplitude | P_TF[R11_ij] | MISSING_PROJECTED_R11_TF_AMPLITUDE | numeric Cassini slip comparison blocked | derive or source numeric P_TF[R11_ij] with units and source path | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | FAIL1948_5_claim_policy | gamma_bound_policy | POLICY_CANDIDATE_NOT_FINAL_CLAIM_RULE | even with inputs, public claim needs explicit confidence convention | choose and justify 1sigma/2sigma/conservative policy before public claim | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Claim Gate

| branch_id | gate_id | claim | status | reason | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_0_runner_implemented | Cassini slip smoke runner exists and parses live inputs. | PASS_NONCLAIM | runner rows scan inputs and report missing required quantities | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_1_failure_modes_explicit | Every missing numeric input has an explicit failure mode. | PASS_NONCLAIM | failure ledger records missing kappa_R/C_TF/U/inverse-Laplacian/P_TF | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_2_numeric_prediction | MTS predicts a numeric Cassini delta_gamma_R11. | FAIL_BLOCKED | required numeric inputs are missing | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_3_theorem_zero | P_TF[R11_ij]=0 is parent-signed. | FAIL_BLOCKED | theorem-zero branch remains conditional only | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_4_Cassini_pass | MTS passes Cassini gamma. | FAIL_BLOCKED | no theorem-zero or numeric bounded prediction exists | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_5_local_GR_PPN | MTS derives local GR/PPN. | FAIL_BLOCKED | Cassini gamma remains blocked and other PPN residuals remain open | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | CG1948_6_public_claim | 1948 is public-ready local-GR evidence. | FAIL_BLOCKED | private smoke-runner checkpoint only | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Decision Ledger

| branch_id | decision_id | decision | reason | next_action | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1948_0_runner_status | CASSINI_SMOKE_RUNNER_IMPLEMENTED_BLOCKED_AS_DESIGNED | the runner now fails cleanly rather than letting a missing coefficient masquerade as a result | fill the first R11 slip numerator/normalization row or prove P_TF zero | False | False | 2026-06-19T23:32:58.371155+00:00 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | DEC1948_1_primary_missing_input | TARGET_P_TF_OR_KAPPA_CTF_SOURCE_FILL_NEXT | without P_TF amplitude and kappa_R/C_TF normalization the runner cannot compute delta_gamma_R11 | attempt to derive/source P_TF[R11_ij], kappa_R, and C_TF from the R11 operator branch | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Next Target

| branch_id | next_id | priority | target_doc | target_script | objective | acceptance_output | nonclaim_rule | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1948_0_primary | selected | 1949-Y5-R2FR-R11-PTF-source-or-kappa-CTF-normalization.md | scripts/Y5_R2FR_R11_PTF_source_or_kappa_CTF_normalization_1949.py | derive or source the first real R11 traceless-spatial amplitude/normalization row: P_TF[R11_ij], kappa_R, and C_TF; otherwise keep Cassini runner blocked | numeric/source-backed or theorem-zero P_TF/kappa_R/C_TF rows, or explicit nonclaim blocker ledger | do not claim Cassini/local-GR pass unless 1948 runner receives real inputs or a parent-signed P_TF zero theorem | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Project Status Snapshot

| branch_id | snapshot_id | status | strongest_result | what_improved | still_missing | claim_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | SNAP1948_0_project_position | CASSINI_SLIP_SMOKE_RUNNER_EXISTS_AND_BLOCKS_MISSING_INPUTS | runner detects missing kappa_R, C_TF, U_solar_frame, inverse-Laplacian boundary, and P_TF amplitude before any Cassini comparison | Cassini local-GR gate is now executable as a discipline tool rather than prose | kappa_R;C_TF;U_solar_frame;nabla^{-2}_local;P_TF[R11_ij] | Cassini/local-GR public claims remain blocked | False | False | 2026-06-19T23:32:58.371155+00:00 |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1948_00_sources | PASS | all local source paths exist and needles found | False | False |
| VAL1948_01_input_audit | PASS | numeric gamma policy available and required MTS inputs missing | False | False |
| VAL1948_02_runner_blocks_cleanly | PASS | smoke runner blocks numeric and theorem-zero branches cleanly | False | False |
| VAL1948_03_failure_modes | PASS | failure modes recorded for missing inputs | False | False |
| VAL1948_04_claim_gates | PASS | runner nonclaim passes only; all claim gates blocked | False | False |
| VAL1948_05_decision | PASS | PTF/kappa/CTF source fill selected | False | False |
| VAL1948_06_next_target | PASS | 1949 PTF/kappa/CTF target selected | False | False |
| VAL1948_07_claim_flags_safe | PASS | claim flags all false | False | False |
| VAL1948_08_csv_parse | PASS | all generated CSVs parse with rows | False | False |
| VAL1948_09_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\CASSINI_SLIP_SMOKE_RUNNER_1948_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\P8_Y5_PARENT_QLOC_1948_CLAIM_GATE_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1948_R11_PTF_OR_KAPPA_CTF_SOURCE_FILL_QUEUE.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\1948\P8_Y5_PARENT_QLOC_1948_CLAIM_GATE.csv | False | False |
| VAL1948_10_pycache_absent | PASS | scripts __pycache__ absent | False | False |
| VAL1948_11_formalization_untouched | PASS | formalization_1948_artifact_count=0 | False | False |
| VAL1948_OVERALL | PASS | 1948 Cassini slip bound smoke runner or PTF source fill | False | False |
