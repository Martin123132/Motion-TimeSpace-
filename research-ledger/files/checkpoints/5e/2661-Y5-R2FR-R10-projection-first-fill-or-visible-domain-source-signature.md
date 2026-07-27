# 2661 - R10 Projection First Fill Or Visible Domain Source Signature

## Purpose

This checkpoint wires the first R10 slice of the coupling residual vector into the existing alpha(lambda) comparator. It deliberately keeps the rows nonclaim until the projection factors and bound curve are real.

## Result

- The R10 projection formula is explicit: `alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g + alpha_tail_abs(lambda)`.
- The current candidate rows are symbolic and use anchor-only bound smoke rows, so the existing comparator correctly refuses claim scoring.
- The useful next target is not a victory lap and not a full data scrape yet: derive/source the R10 profile normalization and `tau_R10` map first.
- No R10, local-GR, PPN, WEP, clock, orbital or Newton claim is allowed.

## Source Register

| source_id | role | path | exists | needles_required | missing_needles | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2661_2660_doc | immediate handoff selecting R10 projection first-fill | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |
| SRC2661_563_doc | source-backed anchor-only R10 bound smoke and nonclaim runner precedent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |
| SRC2661_437_doc | R10 alpha(lambda) executable curve contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\437-R10-alpha-lambda-executable-curve-contract.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |
| SRC2661_947_doc | prior R10 projection fill attempt and bound interface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |
| SRC2661_1029_doc | finite c_g and tau_R10 source requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |
| SRC2661_2659_doc | visible-domain theorem remains unsigned, so c_g remains finite/residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:16:17.720002+00:00 |

## Projection Slice

| branch_id | slice_id | quantity | required_formula | current_fill | missing_input | status | source_ref | score_ready | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_0_formula | alpha_R10(lambda) | alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10 c_g + alpha_tail_abs(lambda) | symbolic_only | K_X(lambda);Qbar_XH;tau_R10;c_g;tail envelope | PROJECTION_FORMULA_READY_NONCLAIM | 2660:APM2660_0_R10;947:PFA947_0_R10_projection | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_1_tau_R10 | tau_R10 | dimensionless map from parent coupling normalization to Yukawa alpha(lambda) convention | MISSING_TAU_R10 | source/test profile, geometry convention, range profile, same-frame normalization | MISSING_ARENA_PROJECTION | 1029:TAU1029_0_R10 | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_2_KX | K_X(lambda) | finite-range kernel/shape factor for the X channel in the R10 source-test geometry | MISSING_K_X_LAMBDA | kernel theorem or sourced profile convention | MISSING_PROFILE_KERNEL | 563:B563_1_no_numeric_MTS_alpha | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_3_Qbar_XH | Qbar_XH | source/Hamiltonian charge projection for the X channel | MISSING_QBAR_XH | source-current owner, Hilbert/source normalization, no-hidden-tail theorem or numeric row | MISSING_SOURCE_CHARGE_PROJECTION | 563:B563_1_no_numeric_MTS_alpha | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_4_cg | c_g | parent common-frame coefficient or theorem-zero from visible-domain signature | MISSING_C_G | visible-domain theorem or finite c_g source | MISSING_PARENT_COEFFICIENT | 2659:FRV2659_0_c_g_common_frame | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_5_bound_curve | alpha_bound(lambda) | full external alpha(lambda) bound curve or explicitly labelled anchor-only smoke rows | anchor_only_rows_available_nonclaim | digitized/full machine-readable curve for claim use | ANCHOR_ONLY_NONCLAIM | 563:R10_ANCHOR rows;437:C10_2_bound_match | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_6_no_cancellation | alpha_tail_abs(lambda) | absolute envelope for marker/source/non-Hilbert tails | MISSING_TAIL_ENVELOPE | b_alpha, b_mass, q_nonH/domain tails and projections | MISSING_TAIL_BOUND | 2660:ENV2660_0_R10 | False | False | 2026-06-23T04:16:17.723664+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | R10P2661_7_verdict | R10 projection slice | all factors numeric/source-backed or theorem-zero, with full bound curve for claims | symbolic_anchor_smoke_only | tau_R10, K_X(lambda), Qbar_XH, c_g, tail envelope, claim-valid bound curve | R10_PROJECTION_NOT_SCORE_READY | this checkpoint | False | False | 2026-06-23T04:16:17.723664+00:00 |

## Factor Gate

| branch_id | factor_id | factor | status | next_action | blocks_score | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_0_tau_R10 | tau_R10 | MISSING_ARENA_PROJECTION | derive/source R10 source-test transfer factor | True | False | 2026-06-23T04:16:17.723689+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_1_KX | K_X(lambda) | MISSING_PROFILE_KERNEL | derive/source finite-range kernel over lambda | True | False | 2026-06-23T04:16:17.723689+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_2_Qbar_XH | Qbar_XH | MISSING_SOURCE_CHARGE_PROJECTION | derive/source Hilbert/source charge projection | True | False | 2026-06-23T04:16:17.723689+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_3_cg | c_g | MISSING_PARENT_COEFFICIENT | derive visible-domain zero or source finite c_g | True | False | 2026-06-23T04:16:17.723689+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_4_tail | alpha_tail_abs(lambda) | MISSING_TAIL_ENVELOPE | source/derive marker and non-Hilbert tails | True | False | 2026-06-23T04:16:17.723689+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | FAC2661_5_bound | alpha_bound(lambda) | ANCHOR_ONLY_FULL_CURVE_MISSING | digitize/import full claim-valid bound curve | True | False | 2026-06-23T04:16:17.723689+00:00 |

## Candidate MTS Curve

| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_coupling_vector_R10_projection_2661 | R10_projection_symbolic_smoke_nonclaim | R10_alpha_lambda_curve_MTS_2661_PROJECTION_SMOKE_NONCLAIM | 3.86e-5 | m | K_X(lambda)*Qbar_XH*tau_R10*c_g + alpha_tail_abs(lambda) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_2661_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha_projection_symbolic | symbolic_R10_projection_nonclaim_missing_tau_K_Qbar_cg_tail | 2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md::R10P2661_0_formula | 2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md | anchor_only_bound_rows;missing_projection_factors;no_tau_one;no_cancellation | false | 2661 candidate row intentionally symbolic; comparator must reject it for claim scoring. |
| MTS_coupling_vector_R10_projection_2661 | R10_projection_symbolic_smoke_nonclaim | R10_alpha_lambda_curve_MTS_2661_PROJECTION_SMOKE_NONCLAIM | 5.6e-5 | m | K_X(lambda)*Qbar_XH*tau_R10*c_g + alpha_tail_abs(lambda) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_2661_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha_projection_symbolic | symbolic_R10_projection_nonclaim_missing_tau_K_Qbar_cg_tail | 2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md::R10P2661_0_formula | 2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md | anchor_only_bound_rows;missing_projection_factors;no_tau_one;no_cancellation | false | 2661 candidate row intentionally symbolic; comparator must reject it for claim scoring. |

## Candidate Bound Curve

| bound_id | dataset_id | lambda_value | lambda_units | alpha_bound | alpha_bound_source | digitization_method | source_file | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Lee_Adelberger_Cook_Fleischer_Heckel_2020_PRL124101101 | 3.86e-5 | m | 1.0 | https://pubmed.ncbi.nlm.nih.gov/32216404/; https://arxiv.org/abs/2002.11761; doi:10.1103/PhysRevLett.124.101101 | anchor_only_non_curve_from_alpha_equals_1_threshold_statement | https://arxiv.org/abs/2002.11761 | false | 2661 reused anchor-only noncurve smoke row; Modern source-backed anchor only: gravitational-strength Yukawa interactions limited to ranges below 38.6 um at 95 percent confidence; not a full alpha(lambda) curve. |
| R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Kapner_Cook_Adelberger_Gundlach_Heckel_Hoyle_Swanson_2007_PRL98021101 | 5.6e-5 | m | 1.0 | https://arxiv.org/abs/hep-ph/0611184; doi:10.1103/PhysRevLett.98.021101 | anchor_only_non_curve_from_abs_alpha_le_1_threshold_statement | https://arxiv.org/abs/hep-ph/0611184 | false | 2661 reused anchor-only noncurve smoke row; Continuity anchor only: inverse-square law holds with abs(alpha)<=1 down to lambda=56 um at 95 percent confidence; not a full alpha(lambda) curve. |

## Runner Summary

| summary_id | mts_curve | bound_curve | output_dir | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUNSUM2661_0_projection_smoke | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_2661_PROJECTION_SMOKE_NONCLAIM.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_2661_ANCHOR_SMOKE.csv | runs/2661-R10-projection-smoke/results | 2 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | False | 2026-06-23T04:16:17.746159+00:00 |

## Nonclaim Anchor Check

| check_id | rows | numeric_positive | anchor_only | full_curve_available | valid_for_claim | status | issues | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ANCH2661_0_anchor_rows | 2 | True | True | False | False | PASS_NONCLAIM_ANCHOR_SMOKE |  | 2026-06-23T04:16:17.746188+00:00 |

## Claim Gates

| branch_id | gate_id | requirement | current_status | evidence_ref | gate_pass | blocks_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | CG2661_0_projection_factors | tau_R10, K_X, Qbar_XH, c_g and tail envelope are numeric/source-backed or theorem-zero | FAIL_FACTORS_MISSING | FAC2661 rows | False | True | False | 2026-06-23T04:16:17.746194+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | CG2661_1_bound_curve | full claim-valid alpha(lambda) bound curve is available | FAIL_ANCHOR_ONLY_NONCLAIM | ANCH2661_0_anchor_rows | False | True | False | 2026-06-23T04:16:17.746194+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | CG2661_2_runner | R10 comparator passes with valid MTS and bound rows | FAIL_RUNNER_BLOCKED | RUNSUM2661_0_projection_smoke | False | True | False | 2026-06-23T04:16:17.746194+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | CG2661_3_visible_domain | visible-domain zero switch is parent-signed | FAIL_VISIBLE_DOMAIN_UNSIGNED | 2660:VDP2660_5_verdict | False | True | False | 2026-06-23T04:16:17.746194+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | CG2661_4_verdict | R10 projection can support a claim | CLAIM_BLOCKED | factors missing; anchor only; runner false | False | True | False | 2026-06-23T04:16:17.746194+00:00 |

## Decision Ledger

| branch_id | decision_id | decision | reason | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | DEC2661_0_projection_status | R10 projection formula is wired but not score-ready | the current row is symbolic and the external bound rows are anchor-only noncurve smoke rows | do not claim R10; fill tau_R10/profile convention or acquire a full curve first | False | False | 2026-06-23T04:16:17.746203+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | DEC2661_1_best_next | try the profile/projection derivation before external curve digitization | a full bound curve still cannot score without K_X, Qbar_XH, tau_R10 and c_g/tail values | derive/source R10 source-test profile normalization and tau_R10 map | False | False | 2026-06-23T04:16:17.746203+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | DEC2661_2_data_policy | anchor rows remain useful only for smoke tests | they validate units/schema and threshold bookkeeping but cannot replace a full alpha(lambda) curve | keep anchor rows nonclaim and preserve comparator refusal | False | False | 2026-06-23T04:16:17.746203+00:00 |

## Next Target

| branch_id | next_id | status | next_doc | next_script | task | must_include | must_exclude | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | NEXT2661_0_selected | selected | 2662-Y5-R2FR-R10-profile-normalization-and-tau-map-or-bound-curve-digitizer.md | scripts/Y5_R2FR_R10_profile_normalization_and_tau_map_or_bound_curve_digitizer_2662.py | derive/source the R10 source-test profile normalization and tau_R10 map first; only then digitize/import a full alpha(lambda) bound curve if useful | Yukawa convention, source/test geometry profile, K_X(lambda), Qbar_XH normalization, tau_R10 units, no tau=1 shortcut, no-cancellation tail policy | R10 pass claim, alpha=1 anchor as full curve, invented finite c_g, closure-only zero as derived theorem, GitHub action, formalization-workbench edits | False | False | 2026-06-23T04:16:17.746217+00:00 |

## Project Status Snapshot

| branch_id | status_id | topic | status | detail | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | STAT2661_0_progress | R10 projection | WIRED_AND_MACHINE_REFUSED | projection formula and candidate rows now run through the existing comparator and fail safely | False | False | 2026-06-23T04:16:17.746221+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | STAT2661_1_data | external R10 bound | ANCHOR_ONLY_NONCLAIM | 2020/2007 anchors are source-backed threshold smoke rows, not a full curve | False | False | 2026-06-23T04:16:17.746221+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | STAT2661_2_theory | MTS-side factors | MISSING_PROJECTION_AND_COEFFICIENTS | tau_R10, K_X, Qbar_XH, c_g and tails remain the live blockers | False | False | 2026-06-23T04:16:17.746221+00:00 |
| Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | STAT2661_3_next | best route | PROFILE_NORMALIZATION_FIRST | derive/source the R10 projection map before spending effort on full bound digitization | False | False | 2026-06-23T04:16:17.746221+00:00 |

## Branch Copies

| copy_id | role | source | destination | exists | parseable_csv | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COPY2661_queue | R10 projection factor queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_PROJECTION_2661_FACTOR_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2661_R10_PROJECTION_INPUT_QUEUE_NONCLAIM.csv | True | True | False | 2026-06-23T04:16:17.751609+00:00 |
| COPY2661_local_bounds | R10 anchor-bound smoke copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_2661_ANCHOR_SMOKE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_projection_2661_NONCLAIM.csv | True | True | False | 2026-06-23T04:16:17.751609+00:00 |
| COPY2661_source_weight | R10 projection slice | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_PROJECTION_2661_PROJECTION_SLICE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\R10_PROJECTION_2661_NONCLAIM.csv | True | True | False | 2026-06-23T04:16:17.751609+00:00 |
| COPY2661_microscope | R10 factor gate local residual copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_PROJECTION_2661_FACTOR_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_2661_R10_PROJECTION_FACTOR_GATE.csv | True | True | False | 2026-06-23T04:16:17.751609+00:00 |
| COPY2661_quarantine | R10 runner refusal summary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_PROJECTION_2661_RUNNER_SUMMARY.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\2661\P8_Y5_2661_R10_RUNNER_SUMMARY.csv | True | True | False | 2026-06-23T04:16:17.751609+00:00 |

## Validation

| timestamp_utc | checkpoint | branch_id | valid_for_claim | claim_allowed | validation_id | status | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_00_sources | PASS | all cited source paths exist and required needles are present |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_01_projection | PASS | R10 projection slice is explicit and not score-ready |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_02_factors | PASS | all projection factors block score until sourced |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_03_candidates_nonclaim | PASS | candidate MTS and bound rows are present and nonclaim |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_04_runner_refuses | PASS | existing comparator refuses symbolic/nonclaim rows |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_05_anchor_smoke | PASS | anchor rows are numeric-positive but nonclaim/noncurve |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_06_claim_gates_blocked | PASS | claim gates block R10 claim |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_07_next_target | PASS | 2662 R10 profile/tau map target selected |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_08_branch_copies | PASS | branch copies exist and parse |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_09_csv_parse | PASS | all generated CSVs parse cleanly |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_10_formalization_untouched | PASS | no 2661 outputs are written under formalization-workbench |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_11_pycache_absent | PASS | scripts __pycache__ absent |
| 2026-06-23T04:16:19.000331+00:00 | 2661 | Y5_R2FR_R10_PROJECTION_FIRST_FILL_2661 | False | False | VAL2661_OVERALL | PASS | 2661 wires the R10 projection slice, runs the existing comparator as a nonclaim smoke, blocks scoring, and selects R10 profile/tau normalization next |
