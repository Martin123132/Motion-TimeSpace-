# 1201 - Y5/R10 W_R10 official kernel source or toy-kernel smoke row

**Current verdict:** no official or geometry-sourced `W_R10` kernel values are acquired in the current corpus. 1201 therefore creates a transparent toy `W_R10=1` smoke row only to exercise the R10 inequality gate.

**Main progress:** the runner now computes actual toy pass/fail rows against the nonclaim 2020 R10 curve samples. This is not physics evidence; it is plumbing proof that the gate can bite once real `W_R10` and `q_DT` values exist.

**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.

## Source register

| source_id | relative_path | needle | role | exists | needle_found |
| --- | --- | --- | --- | --- | --- |
| SRC1201_0_1200_next | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | NEXT1200_0_1201 | direct 1201 handoff. | True | True |
| SRC1201_1_1200_denominator | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | WRK1200_0_unit_alpha_denominator | unit-alpha denominator source-pack requirement. | True | True |
| SRC1201_2_1200_numerator | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | WRK1200_1_qDT_numerator | qDT numerator source-pack requirement. | True | True |
| SRC1201_3_1200_profile | 1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md | QPE1200_0_total_envelope | qDT profile-envelope requirement. | True | True |
| SRC1201_4_1034_status | 1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md | R10B1034_4_official_supplement_table_status | official supplement table not acquired. | True | True |
| SRC1201_5_1035_harmonic | 1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md | KXF1035_3_harmonic | R10 harmonic kernel remains missing. | True | True |
| SRC1201_6_437_yukawa | 437-R10-alpha-lambda-executable-curve-contract.md | Yukawa_potential | R10 Yukawa convention. | True | True |
| SRC1201_7_R10_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | R10_VECTOR_2020_REVIEW_0000 | nonclaim numeric R10 review curve for smoke rows. | True | True |
| SRC1201_8_APS_supplement_attempt | source-intake/local_bounds/downloads/aps_prl_124_101101/link_aps_supplemental_attempt.html | Just a moment | local artifact documenting blocked supplement acquisition attempt. | True | True |
| SRC1201_9_arxiv_pdf | source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf |  | local PRL/arXiv PDF artifact; existence checked only. | True | True |

## Official kernel audit

| audit_id | source_url | local_artifact | wanted_object | finding | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OKA1201_0_APS_DOI_page | https://link.aps.org/doi/10.1103/PhysRevLett.124.101101 | source-intake/local_bounds/downloads/aps_prl_124_101101/link_aps_supplemental_attempt.html | machine-readable R10 torque/readout kernel or alpha(lambda) supplement | DOI/source page exists, but current local artifact does not provide a usable W_R10 torque kernel table | OFFICIAL_KERNEL_NOT_ACQUIRED | False | False |
| OKA1201_1_EotWash_ISL_page | https://www.npl.washington.edu/eotwash/inverse-square-law | web_checked_no_local_kernel_table | experiment geometry/harmonic kernel sufficient for D_Y and N_DT | public page gives experiment/publication context but not the numerical torque kernel needed for W_R10 | PUBLIC_CONTEXT_NOT_KERNEL | False | False |
| OKA1201_2_arXiv_PRL_pdf | https://arxiv.org/abs/2002.11761 | source-intake/local_bounds/downloads/arxiv_2002_11761/2002.11761.pdf | geometry/harmonic response kernel | paper/PDF anchors the R10 force-law and harmonic-design context but not a ready machine-readable W_R10 kernel for arbitrary q_DT profiles | PAPER_CONTEXT_NOT_NUMERIC_KERNEL | False | False |
| OKA1201_3_review_curve_candidate | https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | external alpha_bound(lambda) curve | numeric review-candidate bound curve exists, but it is not the W_R10 response kernel and remains valid_for_claim=false | EXTERNAL_BOUND_ONLY_NOT_WR10 | False | False |
| OKA1201_4_verdict | multiple official/public sources checked | 1201 audit | official/geometry W_R10 kernel | no source-backed W_R10 kernel values are available in the current local corpus; proceed with toy smoke row only | MOVE_TO_TOY_KERNEL_SMOKE_NONCLAIM | False | False |

## Toy kernel definition

| toy_id | quantity | toy_value | definition | reason_for_toy | physics_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TOY1201_0_definition | toy W_R10(lambda) | 1.0 | Set D_Y=1 and N_DT=1 for every sampled lambda, purely to exercise join arithmetic. | official/geometry W_R10 kernel not acquired | TOY_NOT_PHYSICS_NOT_EVIDENCE | False | False |
| TOY1201_1_qDT_smoke_value | toy q_DT_bound | 1.0 | Set q_DT_bound=1 dimensionless in toy units so the sample curve produces both pass and fail rows. | tests inequality logic without inventing MTS source/profile values | TOY_NOT_PHYSICS_NOT_EVIDENCE | False | False |
| TOY1201_2_no_promotion_guard | promotion policy | valid_for_claim=false;claim_allowed=false | Toy W_R10 rows cannot be merged into live R10 or local-GR evidence tables. | prevents smoke-test arithmetic from becoming a claim | GUARD_ACTIVE | False | False |

## Toy smoke rows

| smoke_id | bound_id | lambda_value | lambda_units | alpha_bound | D_Y_unit_alpha_toy | N_DT_unit_profile_toy | W_R10_toy | q_DT_bound_toy | alpha_DT_bound_toy | qDT_allowed_if_WR10_1 | toy_pass | row_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMK1201_0_toy_WR10_join | R10_VECTOR_2020_REVIEW_0000 | 5.894419132271889e-06 | m | 897932.2928704522 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 897932.2928704522 | True | toy_computed_nonclaim_not_physics | False | False |
| SMK1201_1_toy_WR10_join | R10_VECTOR_2020_REVIEW_0195 | 7.355973827852426e-05 | m | 0.14850286746800798 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.14850286746800798 | False | toy_computed_nonclaim_not_physics | False | False |
| SMK1201_2_toy_WR10_join | R10_VECTOR_2020_REVIEW_0351 | 0.000608078322298804 | m | 0.002344664300519378 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.002344664300519378 | False | toy_computed_nonclaim_not_physics | False | False |
| SMK1201_3_toy_WR10_join | R10_VECTOR_2020_REVIEW_0389 | 0.0010099153351819316 | m | 0.019113309433552817 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.019113309433552817 | False | toy_computed_nonclaim_not_physics | False | False |

## Runner output

| run_id | runner_status | rows_computed | toy_pass_count | toy_fail_count | expected_behavior | physics_interpretation | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1201_0_toy_WR10_smoke_runner | toy_computed_nonclaim | 4 | 1 | 3 | mixed pass/fail is acceptable and proves inequality gate executes | none; toy W_R10 and qDT values are not source-backed | False | False |

## Claim gates

| gate_id | claim | status | why | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G1201_0_official_WR10 | official/geometry W_R10 kernel is sourced | BLOCKED_OFFICIAL_KERNEL_NOT_ACQUIRED | available official/public sources do not provide a machine-readable W_R10 kernel in the current corpus | False | False |
| G1201_1_toy_WR10 | toy W_R10 can support physics scoring | BLOCKED_TOY_ONLY | toy D_Y=N_DT=1 is an arithmetic smoke test, not an experiment geometry/readout model | False | False |
| G1201_2_R10_pass | MTS qDT passes R10 | BLOCKED_NO_SOURCE_BACKED_WR10_OR_QDT_PROFILE | real W_R10 and qDT profile/envelope values remain missing | False | False |
| G1201_3_local_GR | MTS local-GR reduction is established | BLOCKED_NO_LOCAL_GR_CLAIM | 1201 only exercises runner logic; it does not close parent, PPN, R10, or boundary/cokernel gates | False | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1201_0_official_kernel | official_WR10_kernel_not_found | local/web-visible official/public sources do not supply a ready response kernel table for arbitrary qDT profiles | either obtain dissertation/geometry kernel data or construct a conservative geometry toy with all assumptions explicit | False |
| D1201_1_toy_runner | toy_kernel_smoke_runner_created | the R10 join logic can now compute pass/fail rows while remaining nonclaim | replace toy D_Y/N_DT with source-backed kernel values or a transparent conservative geometry model | False |
| D1201_2_best_next | build_conservative_geometry_kernel_or_qDT_profile_family | official kernel acquisition is blocked, so the next useful private step is a conservative geometry model or qDT profile family that remains explicitly nonclaim | 1202 should build a conservative geometry-kernel model with documented assumptions, or fill qDT profile components first | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1201_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1201_1_official_kernel_audit | pass | official/geometry W_R10 kernel audit completed and remains not acquired | False |
| V1201_2_toy_kernel_nonclaim | pass | toy kernel rows are explicitly nonclaim | False |
| V1201_3_smoke_rows_compute | pass | toy smoke rows compute numeric pass/fail inequality with at least one pass and one fail | False |
| V1201_4_runner_nonclaim | pass | toy runner executes but remains nonclaim | False |
| V1201_5_claim_gates_blocked | pass | all 1201 claim gates and next target remain blocked/nonclaim | False |
| V1201_6_all_science_rows_nonclaim | pass | all generated science rows keep valid_for_claim=false | False |
| V1201_7_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1201_8_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1201_SUMMARY | pass | 1201 records that official W_R10 kernel values are not acquired, creates a toy W_R10=1 smoke row, proves the R10 inequality gate executes with mixed pass/fail rows, and keeps every output nonclaim | False |

## Next target

| next_id | next_target | objective | include | exclude | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1201_0_1202 | 1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family.md | replace the toy W_R10 smoke row with either a conservative geometry-kernel model or a qDT profile family, still nonclaim, so the R10 runner becomes physically interpretable enough for private stress tests | declared geometry assumptions; denominator positivity; harmonic weights; qDT profile family; absolute-sum guard; nonclaim sample run | official-kernel claim without source; promoted review curve; local-GR/R10 pass; tuned cancellation; GitHub; formalization edits | False | False |
