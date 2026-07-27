# 1625 — Finite `Z_R` Prior Row Builder And Arena Projection Schema

## Status

Private checkpoint. This does **not** claim local GR/Newton recovery, R10, PPN, clock, or orbital success. It turns the finite-residual route into a strict source-row contract.

## Why This Exists

`1624` ended the current primitive-constructor loop: the motion/time/space primitive route does not yet derive the parent object language or the no-vertical-metric theorem. The honest next move is therefore finite-prior plumbing: if `Z_R`, `M_R^2`, `J_R`, or `B_R` are nonzero, the branch must say how large they are, where that number came from, and how it projects into real tests.

## Source Register

| source_id | source_path | exists | needles_found |
| --- | --- | --- | --- |
| 1624_doc | 1624-Y5-R2FR-primitive-constructor-derivation-or-ZR-prior-acquisition.md | True | True |
| 1624_validation | source-intake/mts_residuals/P8_Y5_BRR545_1624_VALIDATION.csv | True | True |
| 1624_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1624_NEXT_TARGET.csv | True | True |
| 1624_acquisition | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1624_FINITE_ZR_PRIOR_ACQUISITION_PLAN.csv | True | True |
| 1624_claim_gate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1624_CLAIM_GATE.csv | True | True |
| 1624_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1624_DECISION.csv | True | True |
| 1262_prior_requirements | source-intake/mts_residuals/P8_Y5_R10_1262_ZR_PRIOR_ENVELOPE_REQUIREMENTS.csv | True | True |
| 1264_source_requirements | source-intake/mts_residuals/P8_Y5_R10_1264_FINITE_ZR_SOURCE_ROW_REQUIREMENTS.csv | True | True |
| 1265_runner_schema | source-intake/mts_residuals/P8_Y5_R10_1265_FINITE_ZR_BOUND_RUNNER_SCHEMA.csv | True | True |
| 1563_fallback_ledger | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv | True | True |
| 1564_intake_status | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1564_FINITE_ZR_INTAKE_STATUS.csv | True | True |
| 1565_source_intake | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1565_FINITE_ZR_SOURCE_ROW_INTAKE.csv | True | True |
| 1566_validator_rules | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RULES.csv | True | True |
| 1566_validator_summary | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_SUMMARY.csv | True | True |
| 1623_prior_rows | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1623_FINITE_ZR_PRIOR_ROWS.csv | True | True |
| 1262_countermodel | source-intake/mts_residuals/P8_Y5_R10_1262_LEGAL_COUNTERMODEL_AUDIT.csv | True | True |

## Finite Prior Row Builder

| prior_builder_id | coefficient_symbol | coefficient_role | required_units | current_status |
| --- | --- | --- | --- | --- |
| PB1625_0_ZR | Z_R | kinetic residue / vertical-gradient coefficient | declared kinetic normalization units | MISSING_SOURCE_BACKED_INPUT |
| PB1625_1_MR2 | M_R^2 | mass gap / screening range owner | mass^2 or length^-2 after declared normalization | MISSING_SOURCE_BACKED_INPUT |
| PB1625_2_JR | J_R | matter/source coupling to the R_AB residual channel | source-current units compatible with the normalized R_AB equation | MISSING_SOURCE_BACKED_INPUT |
| PB1625_3_BR | B_R | boundary/defect/readout tail coefficient | boundary flux or alpha-tail units after stated projection | MISSING_SOURCE_BACKED_INPUT |

## Arena Projection Schema

| projection_id | projection_symbol | arena | observable_output | current_status |
| --- | --- | --- | --- | --- |
| AP1625_0_tau_R10 | tau_R10 | R10 / short-range fifth-force bound | alpha_R(lambda) or an explicitly equivalent residual-force amplitude | MISSING_ARENA_PROJECTION |
| AP1625_1_tau_PPN | tau_PPN | PPN / weak-field local-GR recovery | gamma-1, beta-1, preferred-frame/source residual vector, or theorem-zero equivalent | MISSING_ARENA_PROJECTION |
| AP1625_2_tau_clock | tau_clock | clock / local time-drift channel | Gdot/G, frequency drift, redshift residual, or clock-comparison amplitude | MISSING_ARENA_PROJECTION |
| AP1625_3_tau_orbital | tau_orbital | orbital / ephemeris / binary-dynamics channel | perihelion drift, range residual, GM drift, inverse-square residual, or binary timing residual | MISSING_ARENA_PROJECTION |

## Nonclaim Intake Template

These rows are deliberately invalid as evidence: they contain `MISSING` markers so the runner refuses them.

| template_row_id | row_type | coefficient_symbol | current_status | rejection_reason |
| --- | --- | --- | --- | --- |
| TEMPLATE1625_0_ZR | coefficient_source_row_template_not_live | Z_R | TEMPLATE_REJECTED_NONCLAIM | template row only; contains MISSING markers and cannot be scored |
| TEMPLATE1625_1_MR2 | coefficient_source_row_template_not_live | M_R^2 | TEMPLATE_REJECTED_NONCLAIM | template row only; contains MISSING markers and cannot be scored |
| TEMPLATE1625_2_JR | coefficient_source_row_template_not_live | J_R | TEMPLATE_REJECTED_NONCLAIM | template row only; contains MISSING markers and cannot be scored |
| TEMPLATE1625_3_BR | coefficient_source_row_template_not_live | B_R | TEMPLATE_REJECTED_NONCLAIM | template row only; contains MISSING markers and cannot be scored |
| TEMPLATE1625_0_tau_R10 | arena_projection_row_template_not_live | tau_R10 | TEMPLATE_REJECTED_NONCLAIM | template row only; arena relation has no numeric/source-backed kernel |
| TEMPLATE1625_1_tau_PPN | arena_projection_row_template_not_live | tau_PPN | TEMPLATE_REJECTED_NONCLAIM | template row only; arena relation has no numeric/source-backed kernel |
| TEMPLATE1625_2_tau_clock | arena_projection_row_template_not_live | tau_clock | TEMPLATE_REJECTED_NONCLAIM | template row only; arena relation has no numeric/source-backed kernel |
| TEMPLATE1625_3_tau_orbital | arena_projection_row_template_not_live | tau_orbital | TEMPLATE_REJECTED_NONCLAIM | template row only; arena relation has no numeric/source-backed kernel |

## Runner Refusal Gates

| gate_id | failure_status | severity | current_status |
| --- | --- | --- | --- |
| RG1625_0_docs_not_live | DOCS_TEMPLATE_NOT_LIVE_INTAKE | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_1_required_columns | MISSING_REQUIRED_COLUMNS_OR_EMPTY_FIELD | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_2_no_missing_markers | PLACEHOLDER_MARKER_PRESENT | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_3_numeric_or_theorem_zero | NO_NUMERIC_OR_THEOREM_ZERO_EVIDENCE | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_4_units_and_normalization | UNITS_OR_NORMALIZATION_MISSING | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_5_source_path_anchor | SOURCE_PATH_OR_ANCHOR_INVALID | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_6_arena_projection | ARENA_PROJECTION_MISSING | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_7_no_claim_flags | CLAIM_FLAG_TRUE_REJECTED | hard_reject | ACTIVE_HARD_REJECT |
| RG1625_8_local_GR_lock | LOCAL_GR_CLAIM_BLOCKED | hard_reject | ACTIVE_HARD_REJECT |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1625_0_finite_priors | finite Z_R/M_R^2/J_R/B_R priors claim-ready | BLOCKED | row builder exists, but no live source-backed coefficient rows are accepted |
| CG1625_1_R10 | R10 alpha(lambda) comparison | BLOCKED | tau_R10 kernel and alpha bound/source rows are not connected to live coefficients |
| CG1625_2_PPN | PPN/local-GR residual vector | BLOCKED | tau_PPN map is schema-only and finite residuals are not numerically bounded |
| CG1625_3_clock | clock/time-drift comparison | BLOCKED | tau_clock kernel lacks source-backed coefficient and observable bound |
| CG1625_4_orbital | orbital/ephemeris comparison | BLOCKED | tau_orbital kernel lacks source-backed coefficient and observable bound |
| CG1625_5_local_GR | derived local GR/Newton recovery | BLOCKED | neither theorem-zero nor finite-prior comparison branch is closed |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1625_0_schema | FINITE_ZR_PRIOR_ROW_BUILDER_STAGED_NONCLAIM | the local branch now has explicit source-row requirements for Z_R, M_R^2, J_R, and B_R | use the row builder only as a validator target, not as evidence |
| DEC1625_1_arena | ARENA_PROJECTION_SCHEMA_STAGED_NONCLAIM | R10, PPN, clock, and orbital tests now have named tau projections with required observables | hunt for numeric/source-backed kernels or write blocker rows |
| DEC1625_2_runner | RUNNER_REFUSES_PLACEHOLDERS_AND_DOC_TEMPLATES | any MISSING/template/docs-only row is hard rejected before scoring | scan raw/accepted intake and corpus for a first live candidate row |
| DEC1625_3_next | NEXT_1626_LIVE_SOURCE_ROW_VALIDATOR_AND_FIRST_PRIOR_HUNT | the schema is now clear enough to start looking for real inputs without smuggling claims | build validator/hunt runner for live source rows and blocker ledger |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1626-Y5-R2FR-finite-ZR-live-source-row-validator-and-first-prior-hunt.md | scripts/Y5_R2FR_finite_ZR_live_source_row_validator_and_first_prior_hunt.py | scan raw/accepted R_AB intake plus current corpus for source-backed finite Z_R, M_R^2, J_R, B_R, tau_R10, tau_PPN, tau_clock, and tau_orbital rows; accept none unless 1625 gates pass | either at least one live row passes strict source/unit/normalization/arena checks as nonclaim, or a precise blocker ledger identifies the missing coefficient source |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1625_0_sources_exist | PASS | all cited 1625 local source paths exist |
| VAL1625_1_needles_found | PASS | all required 1625 source needles found |
| VAL1625_2_builder_coefficients | PASS | Z_R, M_R^2, J_R, B_R builder rows present |
| VAL1625_3_arena_symbols | PASS | tau_R10, tau_PPN, tau_clock, tau_orbital projection rows present |
| VAL1625_4_nonclaim_flags | PASS | all generated 1625 rows remain nonclaim/non-score-ready |
| VAL1625_5_template_rejected | PASS | template rows contain MISSING markers and are explicitly rejected |
| VAL1625_6_runner_hard_rejects | PASS | all runner gates are active hard rejects |
| VAL1625_7_runner_locks | PASS | runner refuses docs templates, placeholders, and local-GR claims |
| VAL1625_8_claim_gates_closed | PASS | all claim gates are blocked |
| VAL1625_9_decision_next | PASS | decision selects live source row validator and first prior hunt next |
| VAL1625_10_next_target_selected | PASS | next target selected |
| VAL1625_11_docs_copied | PASS | RAB docs templates copied as nonclaim files |
| VAL1625_12_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1625_13_csv_parse | PASS | all generated 1625 CSVs parse |
| VAL1625_14_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1625_15_formalization_untouched | PASS | no 1625 outputs found under formalization-workbench |
| VAL1625_OVERALL | PASS | 1625 finite Z_R prior row builder and arena projection schema validation |
