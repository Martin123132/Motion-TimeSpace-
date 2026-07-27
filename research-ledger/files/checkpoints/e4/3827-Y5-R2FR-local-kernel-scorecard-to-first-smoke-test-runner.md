# 3827 — Local Kernel Scorecard To First Smoke-Test Runner

Private checkpoint. This is the first runnable local-arena dry run from the 3826 compact-exterior source kernel. It deliberately does not claim any physics pass.

Generated: `2026-07-01T01:46:56+00:00`

## What Ran

The runner loaded the 3826 kernel scorecard, arena closure matrix, residual bundle, and roadmap, then checked that each local arena resolves its declared kernel clauses. The output is not a fit. It is a schema/failure-mode smoke test.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3827_0_3826_doc | 3826-Y5-R2FR-compact-exterior-source-kernel-closure-scorecard.md | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_1_3826_scorecard | source-intake\mts_residuals\P8_Y5_R2FR_3826_KERNEL_CLAUSE_SCORECARD.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_2_3826_arena_matrix | source-intake\mts_residuals\P8_Y5_R2FR_3826_ARENA_CLOSURE_MATRIX.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_3_3826_residuals | source-intake\mts_residuals\P8_Y5_R2FR_3826_SOURCE_KERNEL_RESIDUAL_BUNDLE.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_4_3826_roadmap | source-intake\mts_residuals\P8_Y5_R2FR_3826_ZERO_OR_SOURCE_ROW_ROADMAP.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_5_3826_gates | source-intake\mts_residuals\P8_Y5_R2FR_3826_CLAIM_GATES.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_6_3826_validation | source-intake\mts_residuals\P8_Y5_BRR545_3826_VALIDATION.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_7_3822_local_ledger | source-intake\mts_residuals\P8_Y5_R2FR_3822_LOCAL_ARENA_SOURCE_LEDGER.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_8_3822_test_rows | source-intake\mts_residuals\P8_Y5_R2FR_3822_LOCAL_TEST_READY_SOURCE_ROWS.csv | True | True | input_for_local_arena_dry_run_runner |
| SRC3827_9_3825_first_rows | source-intake\mts_residuals\P8_Y5_R2FR_3825_FIRST_SOURCE_READY_BOUNDARY_MHREF_ROWS.csv | True | True | input_for_local_arena_dry_run_runner |

## Smoke Results

| smoke_id | arena | kernel_input_resolution | smoke_status | claim_allowed | blocking_inputs |
| --- | --- | --- | --- | --- | --- |
| SMOKE3827_R10 | R10 short-range alpha(lambda) | PASS | PASS_SCHEMA_CLAIM_BLOCKED | False | numeric MTS alpha numerator; boundary/MHref rows; parent-owned source scale; real bound curve |
| SMOKE3827_WEP | weak equivalence principle composition tests | PASS | PASS_SCHEMA_INPUT_BLOCKED | False | composition source normalizer; material stress closure; readout-map descent |
| SMOKE3827_PPN | local PPN gamma/beta and preferred-frame residuals | PASS | PASS_SCHEMA_PROOF_BLOCKED | False | metric readout descent; gamma/beta residual coefficients; independent source mass |
| SMOKE3827_clock | clock redshift and local time transport | PASS | PASS_SCHEMA_SOURCE_ROWS_NONCLAIM | False | clock readout transport; boundary/reference lock; H_tau-H_ref row |
| SMOKE3827_orbital | orbital systems and Newtonian limit | PASS | PASS_SCHEMA_ANTI_CIRCULARITY_GUARD | False | independent M and G split; source selector; PPN/readout tail |
| SMOKE3827_EM | electromagnetic stress and Poynting/wave coupling | PASS | PASS_SCHEMA_EXTENSION_BLOCKED | False | same-current ownership; Poynting flux boundary term; radiative readout naturality |

## Failure Mode Ledger

| failure_id | severity | failure_mode | blocks | first_fix |
| --- | --- | --- | --- | --- |
| FAIL3827_0_R10_source_numerator | HIGH | numeric MTS alpha numerator is absent or nonclaim | R10 alpha(lambda) claim | derive or source K_X Qbar_XH qbar_XT numerator and keep row valid_for_claim=false until provenance exists |
| FAIL3827_1_boundary_MHref | HIGH | boundary/reference lock and M_H_ref denominator rows are source-ready but not claim-valid | R10, clock, EM, and local-source normalization claims | fill FSR3825 rows or prove exact boundary/reference zero using the same compact exterior source |
| FAIL3827_2_PPN_readout_tail | CRITICAL | metric readout descent has no parent-signed gamma/beta/preferred-frame residual vector | local GR/Newton recovery claim | derive or bound R_PPN_readout_tail with gamma-1, beta-1, alpha1, alpha2, clock, and orbital subrows |
| FAIL3827_3_GM_smuggling_guard | HIGH | orbital mu=GM remains validation-output product evidence, not independent source normalization | Newton constant/source-mass derivation claim | obtain independent M/G split or derive source normalization without using fitted orbital mu as input |
| FAIL3827_4_WEP_material_stress | MEDIUM | composition/material stress normalizer is not source-owned | WEP composition claim | separate universal compact-kernel terms from material-dependent stress residuals |
| FAIL3827_5_EM_Poynting_flux | MEDIUM | Poynting/vector-wave stress route lacks same-current source ownership and boundary flux row | Maxwell/EM stress extension claim | add Poynting flux boundary/source row under the same Pi_M and R_eq kernel |

## Priority Source-Fill Queue

| priority | queue_id | target | why_first | acceptable_outcome |
| --- | --- | --- | --- | --- |
| 1 | QUEUE3827_0_PPN_readout_tail | R_PPN_readout_tail | this is the direct local GR/Newton proof edge; without it the compact kernel cannot produce PPN residuals | derive zero route or emit finite residual vector with units, source path, and valid_for_claim=false |
| 2 | QUEUE3827_1_boundary_MHref | B_zero_flux; Delta_symp; M_H_ref | these rows control R10/clock/EM source normalization and prevent hidden denominator tricks | source-backed nonclaim rows before any local pass language |
| 3 | QUEUE3827_2_independent_source_ledger | independent source mass/scale rows | prevents fitted GM and fitted alpha from becoming hidden inputs | source ledger has numeric provenance while claim gates stay closed |
| 4 | QUEUE3827_3_R10_bound_and_MTS_alpha | R10 alpha(lambda) | R10 can become the quickest empirical sanity check once parent numerator exists | R10 comparator runs and reports blocked/stable without claiming pass from placeholders |
| 5 | QUEUE3827_4_EM_Poynting_source_stress | EM stress/Poynting boundary row | captures Martin's wave/Poynting intuition without letting EM shortcut the local-GR source proof | EM extension remains tied to the same compact source kernel |

## PPN Readout-Tail First Rows

| row_id | observable | symbolic_residual | source_status | valid_for_claim | next_action |
| --- | --- | --- | --- | --- | --- |
| PPN3827_0_gamma_minus_one | gamma-1 | delta_gamma_MTS | MISSING_PARENT_SIGNED_READOUT | False | derive zero from readout naturality or emit finite bound row |
| PPN3827_1_beta_minus_one | beta-1 | delta_beta_MTS | MISSING_SECOND_ORDER_SOURCE_COUPLING | False | derive quadratic source-kernel coefficient or bound it independently |
| PPN3827_2_preferred_frame | alpha1, alpha2 preferred-frame residuals | delta_alpha1_MTS;delta_alpha2_MTS | MISSING_FRAME_DESCENT_SIGNATURE | False | prove frame terms vanish or emit preferred-frame finite residual vector |
| PPN3827_3_clock_tau | clock redshift/time-transport residual | delta_tau_clock_MTS | MISSING_CLOCK_READOUT_TRANSPORT | False | link tau_clock to boundary/MHref row rather than independent local-time ansatz |
| PPN3827_4_orbital_mu_guard | orbital mu=GM validation residual | delta_mu_orbital_guard_MTS | PRODUCT_ONLY_GM_GUARD | False | keep mu as output check until independent M/G split exists |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3827_0_runner_executes | PASS_NONCLAIM | False | 6 local arena smoke rows emitted |
| GATE3827_1_no_claim_pass | PASS_GUARD | False | all results are schema, input-blocked, proof-blocked, source-row, guard, or extension modes |
| GATE3827_2_local_GR_Newton | BLOCKED | False | R_PPN_readout_tail remains missing and is selected as 3828 |
| GATE3827_3_R10 | BLOCKED_DRY_RUN_ONLY | False | real MTS numerator and boundary/MHref rows are still absent |
| GATE3827_4_EM | BLOCKED_EXTENSION_NONCLAIM | False | Poynting flux/source-current boundary row is not yet parent-owned |
| GATE3827_5_next_derivation | PASS_ACTIONABLE_NEXT | False | 3828 targets PPN readout-tail descent or finite residual vector |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3827_0_testing_started | local testing has started in dry-run mode | future work can now distinguish schema failure, missing source inputs, and missing derivation |
| DEC3827_1_not_yet_claimable | no local arena is claimable from the dry run | the project avoids post-hoc local-GR claims while still moving toward tests |
| DEC3827_2_next_derivation | go after R_PPN_readout_tail next | 3828 should derive zero conditions or emit first finite residual vector rows |

## Bottom Line

3827 moves the project from prose blockers to executable dry-run blockers:

- all six local arenas resolve their 3826 kernel clauses;
- every arena remains nonclaim;
- the local-GR/Newton edge is now sharply identified as `R_PPN_readout_tail`;
- R10 and EM are not discarded, but they are downstream of source numerator/boundary/current rows;
- orbital `mu=GM` remains a guardrail output, not an input.

Next target: `3828-Y5-R2FR-PPN-readout-tail-descent-or-first-residual-vector-bound.md`.
