# 1643 - Pi_R Mstar Source Acquisition And Current PPN Bound Runner

**Private status:** nonclaim checkpoint. No PPN pass, local-GR pass, Newton pass, orbital pass, WEP pass, clock pass, EM pass, or R10 pass is claimed.

## Verdict

The current external PPN gamma bound is now source-backed for the finite residual branch. The conservative internal envelope staged here is:

```text
Cassini: gamma - 1 = (2.1 +/- 2.3) x 10^-5
|Delta gamma|max,2sigma = |2.1|e-5 + 2*2.3e-5 = 6.7e-5
```

That is useful, but it does **not** score MTS. The normalized runner still refuses to run because the MTS-side numerator and denominator are missing:

```text
|q_R| = k_W |Pi_R| c^2/(2 G M_*)
|Pi_R| <= (2 G M_*/(k_W c^2)) |Delta gamma|max
```

`Pi_R_boundary_abs`, `B_zero_flux`, same-frame `M_*`, parent-signed `k_W`, and the absolute no-cancellation vector are still missing or conditional. Cassini gives the external wall; MTS still has to supply the thing being thrown at the wall.

## Local Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1642_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1642-Y5-R2FR-minimal-boundary-variation-clause-or-PiR-Mstar-source-fill.md | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1642_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1642_VALIDATION.csv | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1642_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1642_NEXT_TARGET.csv | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1642_fill | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1642_PIR_MSTAR_SOURCE_FILL_ROWS.csv | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1642_rule | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1642_NORMALIZED_PPN_SCORE_RULE.csv | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1639_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1639_NR_LAW_CONDITIONAL.csv | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 05_reciprocity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\05-reciprocity-theorem-attempt.md | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1006_denominator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |
| 1016_selector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md | True | True | 1643 normalized finite Pi_R/PPN source acquisition runner |

## External Source Register

| external_id | observable | source_label | source_url | doi | reported_result | abs_delta_gamma_envelope_2sigma | valid_bound_source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXT1643_0_Cassini_gamma | PPN_gamma | Bertotti, Iess, Tortora 2003 Cassini radio link test | https://pubmed.ncbi.nlm.nih.gov/14508481/ | 10.1038/nature01997 | gamma = 1 + (2.1 +/- 2.3) x 10^-5 | 6.7e-5 | True |
| EXT1643_1_ephemerides_consistency_review | PPN_framework_consistency | Fienga and Minazzoli 2023 Living Reviews in Relativity | https://link.springer.com/article/10.1007/s41114-023-00047-0 | 10.1007/s41114-023-00047-0 | planetary ephemeris tests require consistent framework/refit treatment; correlated parameters need caution |  | False |

## Normalized PPN Input Status

| input_id | quantity | current_value | source_backed | input_status | valid_for_runner |
| --- | --- | --- | --- | --- | --- |
| IN1643_0_PiR_boundary_abs | Pi_R_boundary_abs | MISSING_BOUND_VALUE | False | MISSING_SOURCE_ROW | False |
| IN1643_1_Bzero_flux | B_zero_flux | MISSING_B_ZERO_FLUX | False | MISSING_SOURCE_ROW | False |
| IN1643_2_Mstar_same_frame | M_star_same_frame | MISSING_SAME_FRAME_PARENT_SOURCE_MASS | False | MISSING_SOURCE_ROW | False |
| IN1643_3_kW_tail | k_W_tail | CONDITIONAL_k_W_EQUALS_1_FROM_CORPUS_NOT_PARENT_SIGNED | True | CONDITIONAL_NOT_PARENT_SIGNED | False |
| IN1643_4_Delta_gamma_bound | Delta_gamma_abs_max | 6.7e-5 | True | SOURCE_BACKED_BOUND_AVAILABLE_NONCLAIM | True |
| IN1643_5_absolute_vector | absolute_local_residual_vector | MISSING_ABSOLUTE_VECTOR_GUARD | False | MISSING_SOURCE_ROW | False |

## Normalized PPN Runner

| run_id | formula | available_inputs | missing_inputs | runner_status | result |
| --- | --- | --- | --- | --- | --- |
| RUN1643_0_input_gate | all inputs must be source-backed or parent-signed before scoring | Delta_gamma_abs_max source-backed; k_W_tail corpus-conditional only | Pi_R_boundary_abs;B_zero_flux;M_star_same_frame;absolute_local_residual_vector;parent-signed k_W_tail | NOT_SCORED_MISSING_INPUTS | BLOCKED |
| RUN1643_1_finite_qR_bound | |q_R| = k_W |Pi_R| c^2/(2 G M_*) | none claim-valid for Pi_R/Mstar/kW product | Pi_R_boundary_abs;M_star_same_frame;parent-signed k_W_tail | NOT_SCORED_MISSING_INPUTS | BLOCKED |
| RUN1643_2_gamma_bound_inversion | |Pi_R| <= (2 G M_*/(k_W c^2)) * 6.7e-5 | Delta_gamma_abs_max=6.7e-5 from Cassini 2sigma envelope | M_star_same_frame;parent-signed k_W_tail;Pi_R projection convention | FORMULA_READY_NOT_SCORED | BLOCKED |
| RUN1643_3_R10_guard | massless Q_R/r is not alpha(lambda) | none | finite carrier/range if R10 is ever reopened | R10_ROUTE_REFUSED | BLOCKED |

## Source Acquisition Blockers

| blocker_id | missing_input | blocker_type | why_needed | repair |
| --- | --- | --- | --- | --- |
| BLK1643_0_PiR | Pi_R_boundary_abs | MISSING_NUMERATOR | sets the physical reciprocal hair amplitude | derive Pi_R=0 or source absolute boundary-tail coefficient with units |
| BLK1643_1_Bzero | B_zero_flux | MISSING_BOUNDARY_REFERENCE_INPUT | exact boundary bookkeeping can shift Pi_R/source mass | source theorem-zero or finite linked-boundary flux row |
| BLK1643_2_Mstar | M_star_same_frame | MISSING_NONCIRCULAR_DENOMINATOR | normalizes Q_R/Pi_R into dimensionless q_R without borrowing orbital GM | derive same-frame Hilbert/Noether source mass or M_H_ref |
| BLK1643_3_kW | parent-signed k_W_tail | CONDITIONAL_TAIL_NORMALIZATION | converts Q_R into the 1/r coefficient of R_AB | derive W(r) radial equation/integration convention from parent action |
| BLK1643_4_no_cancellation | absolute_local_residual_vector | MISSING_NO_CANCELLATION_GUARD | prevents Pi_R from being hidden by unrelated residual cancellations | assemble absolute local residual vector across Pi_R, q_loc, frame, readout, source-mass channels |

## Decisions

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1643_0_gamma | PPN_GAMMA_BOUND_SOURCE_BACKED_CASSINI_ANCHOR | Cassini supplies gamma=1+(2.1+/-2.3)e-5; 2sigma envelope 6.7e-5 is staged as a nonclaim bound input | keep gamma bound available but do not score until MTS numerator/denominator inputs exist |
| DEC1643_1_runner | NORMALIZED_PPN_RUNNER_REFUSES_MISSING_MTS_INPUTS | Pi_R, B_zero, Mstar, parent kW, and no-cancellation vector are missing or conditional | attack same-frame Mstar denominator first because it blocks every finite bound |
| DEC1643_2_ephemerides | EPHEMERIDES_USED_AS_CONSISTENCY_CAUTION_NOT_BOUND | current reviews emphasize framework consistency and correlations; no ephemeris gamma row is imported as a simple standalone bound | only use ephemeris constraints after a same-framework MTS refit path exists |

## Claim Gates

| gate_id | claim | status | blocker |
| --- | --- | --- | --- |
| CG1643_0_gamma_bound | external PPN gamma bound acquired | PASS_AS_BOUND_INPUT_ONLY | not an MTS pass; only one external bound row is source-backed |
| CG1643_1_PPN_score | MTS finite Pi_R branch passes PPN gamma | BLOCKED | Pi_R, Mstar, parent kW, and no-cancellation inputs are missing |
| CG1643_2_local_GR | local GR recovered through reciprocal-hair branch | BLOCKED | Pi_R zero theorem remains unsigned and finite residual runner is not score-ready |
| CG1643_3_R10 | massless reciprocal tail is finite-range R10 evidence | BLOCKED | massless Q_R/r remains local/PPN/orbital |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1644-Y5-R2FR-Mstar-same-frame-source-mass-owner-or-noncircular-denominator-blocker.md | scripts/Y5_R2FR_Mstar_same_frame_source_mass_owner_or_noncircular_denominator_blocker.py | derive or source M_star_same_frame/M_H_ref as a parent Hilbert/Noether source mass denominator before orbital fitting; if it fails, keep a noncircular-denominator blocker ledger | either M_star is parent-signed/source-backed in the same frame as Pi_R/q_R/PPN, or every finite Pi_R bound remains blocked by a noncircular denominator failure |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1643_0_sources_exist | PASS | all 1643 local source paths exist |
| VAL1643_1_needles_found | PASS | all 1643 local source needles found |
| VAL1643_2_external_gamma_source | PASS | Cassini gamma external source and 2sigma envelope are recorded |
| VAL1643_3_gamma_input_filled | PASS | Delta gamma input is source-backed as a bound row |
| VAL1643_4_mts_inputs_missing | PASS | all MTS numerator/denominator/no-cancellation inputs remain missing or conditional |
| VAL1643_5_runner_refuses_scoring | PASS | normalized PPN runner refuses scoring |
| VAL1643_6_blockers_complete | PASS | source acquisition blockers cover PiR, Bzero, Mstar, kW, and no-cancellation |
| VAL1643_7_decisions_recorded | PASS | required 1643 decisions are recorded |
| VAL1643_8_claim_gates_safe | PASS | gamma bound gate is input-only and all MTS claims remain forbidden |
| VAL1643_9_next_target_selected | PASS | next target selects Mstar same-frame denominator ownership |
| VAL1643_10_csv_parse | PASS | all generated 1643 CSVs parse |
| VAL1643_11_no_mts_claim_flags | PASS | all 1643 generated rows keep MTS claim/no-score flags false |
| VAL1643_12_branch_copies | PASS | branch/quarantine copies exist |
| VAL1643_13_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1643_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1643_15_formalization_untouched | PASS | no 1643 outputs found under formalization-workbench |
| VAL1643_OVERALL | PASS | 1643 PiR/Mstar source acquisition and current PPN bound runner validation |
