# 964 Y5 R10: Parent No-Higher-Derivative Minimality Theorem Or R2/fR Nonclaim Runner

Status: `Y5_R10_964_minimality_theorem_not_proven_R2FR_nonclaim_runner_rejects_current_inputs`

Claim ceiling: no parent minimality theorem, R2/fR zero, R10 pass, PPN pass, EH, Newton, measured-GM, or local-GR claim is made.

## Readout

The best derivation shot was taken and it does not close yet. To activate the 962 theorem, MTS needs a parent no-higher-derivative/minimality theorem: no natural marker functor, no scalar/class extension, and no integrated-out sector that regenerates `R^2`, `f(R)`, or a scalaron.

Current corpus does not prove that. Countermodels like `EH + epsilon R^2`, an auxiliary scalar that integrates out to `R^2`, and marker-prefactor `F(sigma)R` remain legal unless the primitive quotient/minimality theorem is strengthened.

The practical gain is that the empirical fallback is now safer: the nonclaim runner rejects placeholders, unsigned zero theorems, anchor-only bounds, and missing full-curve data. No little gremlin can sneak a “pass” through the side door.

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 963_doc | handoff: parent second-order signature failed and runner spec written | true | true | 963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md |
| 963_runner_spec | R2/fR runner spec with missing-input gates | true | true | source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv |
| 962_proof | relative theorem that P6 activates | true | true | source-intake/mts_residuals/P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv |
| 440_second_order | metric-only second-order sector counterchecks | true | true | 440-metric-only-second-order-sector-reduction-attempt.md |
| 439_premise_ladder | P6 second-order parent blocker | true | true | 439-EH-only-exterior-parent-premise-ladder.md |
| 423_minimality | minimality/no-extension theorem failure source | true | true | 423-parent-action-minimality-no-extension-theorem-attempt.md |
| 413_no_marker | marker-extension counterexample source | true | true | 413-no-marker-parent-action-theorem-attempt.md |
| 710_scalar_descent | scalar no-prefactor/no-kinetic candidate clauses | true | true | 710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md |
| R11_executable | R2/fR retained-row source | true | true | source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv |

## Minimality Theorem Attempt

| attempt_id | theorem_piece | status | why_not_closed | consequence |
| --- | --- | --- | --- | --- |
| MIN964_0_target | parent no-higher-derivative minimality theorem | target_defined_not_proven | minimality/no-extension is not derived from a universal property of the parent object | does not activate the 962 R2/fR zero theorem |
| MIN964_1_primitive_quotient | Q_MTS is a primitive minimal quotient object | not_derived | a legal extended quotient can still append covariant material/invariant marker variables | extra scalar generators can remain legal |
| MIN964_2_no_integrated_out_tower | integrating out hidden sectors cannot generate f(R)/R^2 | not_derived | E_A=0 or a large mass is not enough unless source/readout and metric variation vanish | R2/fR can re-enter after reduction even if not written in the primitive ansatz |
| MIN964_3_Ostrogradsky_regular | regularity/stability forbids higher derivatives | insufficient_as_theorem | R^2/f(R) can be recast as a scalar-tensor theory, so simple derivative-order distaste is not a mathematical exclusion | stability is a guide, not a zero certificate |
| MIN964_4_descent_signature | scalar/class action descent | candidate_clause_only | quotient geometry has not yet forced scalar/class labels to be readout-only and stressless | scalar-tensor/f(R)-like leakage remains retained |
| MIN964_5_verdict | activate 962 c_R2=c_fR zero theorem | THEOREM_NOT_PROVEN_CURRENT_CORPUS | countermodels remain legal unless minimality/no-extension is strengthened | must either keep deriving minimality or use nonclaim runner for finite scalar branch |

## Countermodel Ledger

| counter_id | countermodel | why_legal_without_gate | damage | currently_killed |
| --- | --- | --- | --- | --- |
| CM964_0_EH_plus_R2 | S = S_EH + epsilon int sqrt(-g) R^2 | local, 4D, diffeo-invariant, metric-only, same observed frame, and Ward-compatible | adds scalar trace pole/fourth-order metric equation unless epsilon=0 or decoupled | false |
| CM964_1_auxiliary_scalar_integrated_out | S = S_EH + int sqrt(-g)[-1/2 M^2 phi^2 + beta phi R] | auxiliary scalar can look nonpropagating before solving its equation | solving phi ~ beta R/M^2 generates beta^2 R^2/(2M^2) | false |
| CM964_2_marker_prefactor | S = int sqrt(-g) F(sigma_marker) R + S_sigma | a covariant marker or quotient-invariant scalar can be appended unless no-extension is proven | scalar-tensor/f(R)-like PPN, WEP, clock, and R10 leakage | false |
| CM964_3_nonlocal_memory_kernel | S = S_EH + int sqrt(-g) R Box^{-1} R or compact memory kernel | history/memory language can be covariant and source-owned if not explicitly forbidden | nonlocal scalar response can mimic finite-range or time-varying source normalization | false |
| CM964_4_topological_safe_case | 4D Gauss-Bonnet exact topological/boundary combination | allowed as harmless only if exact combination and boundary flux are controlled | safe case, but does not rescue generic R2/fR row | conditional_safe_not_current_row |

## R2/fR Nonclaim Input Template

| input_id | row_type | coefficient_value | alpha_predicted | lambda_predicted_um | source_file | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| R2IN964_0_mts_prediction_required | mts_prediction | MISSING_PARENT_INPUT | MISSING_ALPHA | MISSING_LAMBDA | MISSING_SOURCE_FILE | false |
| R2IN964_1_zero_theorem_switch | zero_theorem | 0_if_parent_signed_else_MISSING | 0_if_parent_signed_else_MISSING | not_applicable_if_zero | 962_relative_theorem_plus_964_minimality_signature | false |
| R2IN964_2_Lee2020_anchor | bound_anchor | not_applicable | not_applicable | 38.6 | https://arxiv.org/abs/2002.11761 | false |
| R2IN964_3_full_curve_required | bound_curve | not_applicable | not_applicable | MISSING_DIGITIZED_CURVE | MISSING_FULL_CURVE_SOURCE_EXTRACTION | false |

## R2/fR Nonclaim Runner Result

| run_id | row_type | accepted_for_scoring | claim_allowed | verdict | missing_fields |
| --- | --- | --- | --- | --- | --- |
| R2RUN964_0_mts_prediction_required | mts_prediction | false | false | REJECTED_MISSING_PARENT_OR_BOUND_INPUTS | coefficient_value;coefficient_units;alpha_predicted;lambda_predicted_um;mass_eV;screening_flag;source_file |
| R2RUN964_1_zero_theorem_switch | zero_theorem | false | false | REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED | coefficient_value;alpha_predicted |
| R2RUN964_2_Lee2020_anchor | bound_anchor | false | false | REJECTED_ANCHOR_ONLY_NON_CURVE | none |
| R2RUN964_3_full_curve_required | bound_curve | false | false | REJECTED_MISSING_PARENT_OR_BOUND_INPUTS | lambda_predicted_um;mass_eV;source_file |
| R2RUN964_VERDICT | runner_verdict | false | false | R2FR_BRANCH_BLOCKED_NONCLAIM | parent_zero_signature_or_numeric_prediction_and_full_curve |

## Claim Gate

| gate_id | claim | current_evidence | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- |
| CGATE964_0_minimality_theorem | parent no-higher-derivative/minimality theorem is proven | theorem attempt fails at all decisive clauses | false | false |
| CGATE964_1_R2FR_zero | c_R2=c_fR=0 in MTS | 964 minimality theorem not proven | false | false |
| CGATE964_2_runner_scoring | finite R2/fR branch can be scored | runner rejects all rows as missing/anchor-only/nonclaim | false | false |
| CGATE964_3_local_GR | local GR/Newton branch promotes | R2/fR remains blocked; connection/source gates remain outside this checkpoint | false | false |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC964_0_theorem_result | no-higher-derivative/minimality theorem | not_proven | EH+R2, auxiliary scalar integrated-out, marker-prefactor, and nonlocal memory countermodels remain legal without stronger parent minimality | try the primitive quotient/no-natural-marker theorem directly or accept R2/fR as retained residual |
| DEC964_1_runner_result | R2/fR nonclaim runner | runner_shell_strictly_rejects_current_inputs | all current rows are parent-missing, zero-theorem-unsigned, anchor-only, or full-curve-missing | only run scoring after either parent zero theorem or real finite scalar prediction plus full curve exists |
| DEC964_2_best_next | next hinge | decide_minimality_vs_connection | R2/fR is boxed but blocked by primitive minimality; connection/torsion is the other big EH gate | best derivation route is now primitive quotient/no-natural-marker theorem; pragmatic route is R2/fR full-curve/nonclaim runner |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V964_0_sources_checked | pass | all cited local source paths exist and needles were found | 2026-06-13T23:33:22.526493+00:00 |
| V964_1_theorem_not_proven | pass | minimality/no-higher-derivative theorem remains unproven | 2026-06-13T23:33:22.526506+00:00 |
| V964_2_countermodels_live | pass | countermodels remain live or conditionally safe only | 2026-06-13T23:33:22.526509+00:00 |
| V964_3_template_nonclaim | pass | all input template rows valid_for_claim=false | 2026-06-13T23:33:22.526512+00:00 |
| V964_4_runner_rejects_all | pass | strict runner rejects all current rows and permits no claim | 2026-06-13T23:33:22.526514+00:00 |
| V964_5_claim_gates_false | pass | claim gates all false | 2026-06-13T23:33:22.526517+00:00 |
| V964_6_decisions_ready | pass | decision ledger has three rows | 2026-06-13T23:33:22.526519+00:00 |
| V964_7_next_target_ready | pass | next target row written | 2026-06-13T23:33:22.526521+00:00 |
| V964_8_formalization_untouched | pass | formalization-workbench modified-file count since script start is zero | 2026-06-13T23:33:22.526524+00:00 |
| V964_9_outputs_inside_post_checkpoint | pass | all outputs resolve inside post-checkpoint-work | 2026-06-13T23:33:22.526526+00:00 |
| V964_10_validation_rows_ready | pass | 964 validation pack assembled | 2026-06-13T23:33:22.526532+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md | try to prove the primitive quotient/no-natural-marker theorem that would forbid scalar/marker extensions; if it fails, start full-curve R10 intake for the retained R2/fR branch without making a claim | universal property; local invariant algebra triviality; marker countermodels; scalar extension kill condition; optional Lee2020 full-curve extraction manifest | EH/local-GR claim, torsion full proof unless selected next, invented coefficients, GitHub action, formalization-workbench edits | false |
