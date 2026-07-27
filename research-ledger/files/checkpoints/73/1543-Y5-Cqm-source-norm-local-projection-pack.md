# 1543 - C_qm Source-Norm Local Projection Pack

## Verdict
- The finite coupling route is now test-shaped: source-side inputs are separated from arena projection coefficients.
- The source envelope remains `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.
- R10, PPN, clock, orbital, and local-GR projections are explicit, but every one remains noncomputable because the MTS-side inputs/projections are missing.
- `C_qm` is the best next target because it can theorem-zero the stress-mediated term before source-size normalization enters.
- No R10, PPN, clock, orbital, local GR, or Newton claim is promoted.

## Source Register
| source_id | source_path | exists | purpose |
| --- | --- | --- | --- |
| SRC1543_0_1542_doc | 1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_1_1542_validation | source-intake/mts_residuals/P8_Y5_BRR545_1542_VALIDATION.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_2_1542_cqm | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_3_1542_scg | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1542_SCG_RUNNER_NONCLAIM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_4_1541_coupling | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_5_1540_chain | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_6_1539_inputs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_7_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_8_r10_curve_candidate | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_9_r10_runner | scripts/R10_alpha_lambda_bound_prediction_runner.py | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_10_source_current | source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_11_source_normalization_owner | source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_12_source_measure_flux | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_13_boundary_certificate | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_14_cg_no_shadow | 1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md | True | input evidence for C_qm source-norm and local arena projection pack |
| SRC1543_15_single_public_metric | 1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md | True | input evidence for C_qm source-norm and local arena projection pack |

## Finite Input Provenance Pack
| input_id | symbol | definition_or_formula | needed_evidence | current_status | role |
| --- | --- | --- | --- | --- | --- |
| FIN1543_0_C_qm | C_qm | \|\|DObs_e[Dq[v_m]]\|\| in declared local norm | zero theorem or finite coefficient with units and source path | MISSING_DQVM_DERIVATIVE_OR_PARENT_ZERO | highest leverage input; if zero, stress-mediated geometry coupling vanishes |
| FIN1543_1_T_source_norm | T_source_norm | \|\|delta S_matter/delta q\|\|_source for the compact body/worldtube | source current normalization, compact-source profile, same-frame Hilbert/Noether current | MISSING_SOURCE_NORM | not expected to be zero for matter; needed to scale the C_qm leakage |
| FIN1543_2_S_direct_m | S_direct_m | direct memory dependence in matter/source action | parent no-direct-memory theorem or finite residual coefficient | MISSING_ACTION_DOMAIN_EXCLUSION_OR_VALUE | if nonzero, q-kernel alone would not silence the source |
| FIN1543_3_S_source_norm_extra | S_source_norm_extra | extra memory leakage in source calibration beyond Hilbert q-pullback | source-normalization descent theorem or finite source-calibration residual | MISSING_SOURCE_NORMALIZATION_RESIDUAL | protects against hiding coupling in measured GM/calibration |
| FIN1543_4_S_boundary_m | S_boundary_m | compact inner/domain/boundary memory leakage | Q_m^H/C_inner/domain support theorem or finite boundary norm | MISSING_BOUNDARY_CHARGE_AND_DOMAIN_NORM | prevents exterior-vacuum language from erasing compact-source charge |
| FIN1543_5_S_cg_norm | S_cg_norm | finite no-cancellation envelope | S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m | SCHEMA_READY_INPUTS_MISSING | feeds N_pair and then all local arena projections |

## Arena Projection Pack
| arena_id | arena | projection_formula | required_inputs | current_status |
| --- | --- | --- | --- | --- |
| ARENA1543_0_R10 | R10 short-range inverse-square tests | alpha_R10(lambda) <= Pi_R10(lambda) * [U_B_max*S_cg_norm + C_inner*\|Q_m^H\|] | Pi_R10(lambda); lambda profile; K_X; U_B_max; C_inner; Q_m^H; valid bound curve | MISSING_ARENA_PROJECTION |
| ARENA1543_1_PPN | PPN gamma/beta/preferred-frame | \|Delta_PPN\| <= Pi_PPN * N_lock with first-pair contribution inserted by S_cg_norm envelope | Pi_PPN response matrix; gauge convention; weak-field metric map; hidden-kernel residuals | MISSING_PPN_RESPONSE_MATRIX |
| ARENA1543_2_clock | clock/redshift/fine-structure style tests | \|delta ln nu\| <= Pi_clock * N_lock plus separate constant/readout sensitivity rows | clock sensitivity matrix; calibration convention; no shadow-clock frame; constants split | MISSING_CLOCK_PROJECTION |
| ARENA1543_3_orbital | orbital/source-GM/local acceleration systems | \|delta a/a\| or \|delta GM/GM\| <= Pi_orbital * N_lock | worldtube source profile; same-frame mass charge; orbital readout map; support/domain residuals | MISSING_ORBITAL_SOURCE_PROJECTION |
| ARENA1543_4_local_GR | local GR/Newton reduction gate | local residual vector <= Pi_local * N_lock with all source, boundary, and hidden-kernel terms included | N_lock; Kmetric conversion; PPN residual vector; q-kernel or finite coupling proof | BLOCKED_NO_CLAIM |

## Bound Anchor Links
| anchor_id | observable | status_summary | source_path | current_status |
| --- | --- | --- | --- | --- |
| BOUND1543_0_R10_curve_candidate | R10 alpha(lambda) | review-candidate/nonclaim curve available for smoke plumbing only | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | BOUND_AVAILABLE_NONCLAIM_MTS_PROJECTION_MISSING |
| BOUND1543_1_local_bound_claims | PPN/WEP/clock/orbital local bound ledger | local bound anchors exist but do not make MTS rows score-ready | source-intake/local_bounds/local_bound_claims.csv | ANCHORS_AVAILABLE_PROJECTIONS_MISSING |
| BOUND1543_2_R10_runner | existing R10 comparator | runner can reject placeholders once MTS projection rows are generated | scripts/R10_alpha_lambda_bound_prediction_runner.py | RUNNER_AVAILABLE_INPUTS_MISSING |

## Projection Runner
| runner_id | quantity | formula | current_status | reason |
| --- | --- | --- | --- | --- |
| RUN1543_0_Scg | S_cg_norm | 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m | NOT_COMPUTABLE | finite source-pack inputs missing |
| RUN1543_1_Npair | N_pair | U_B_max*S_cg_norm + C_inner*\|Q_m^H\| | NOT_COMPUTABLE | first-pair inputs remain missing |
| RUN1543_2_R10 | alpha_R10(lambda) | Pi_R10(lambda)*N_pair | NOT_COMPUTABLE | Pi_R10 and MTS N_pair missing; bound curve is nonclaim review candidate |
| RUN1543_3_PPN | PPN residual vector | Pi_PPN*N_lock | NOT_COMPUTABLE | response matrix and N_lock missing |
| RUN1543_4_clock_orbital | clock/orbital residuals | Pi_clock/orbital*N_lock | NOT_COMPUTABLE | arena projection rows missing |

## Claim Gates
| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1543_0_inputs_named | finite source inputs named | PASS_NONCLAIM | all C_qm/S_cg source-pack rows exist |
| GATE1543_1_arenas_named | local arenas named | PASS_NONCLAIM | R10, PPN, clock, orbital, and local-GR projection rows exist |
| GATE1543_2_Scg_score | S_cg_norm score-ready | BLOCKED | finite source inputs missing |
| GATE1543_3_R10_score | R10 score-ready | BLOCKED | MTS projection and valid bound comparison rows missing |
| GATE1543_4_PPN_clock_orbital_score | PPN/clock/orbital score-ready | BLOCKED | arena projections and N_lock missing |
| GATE1543_5_local_GR | local GR/Newton/PPN claim | BLOCKED_NO_CLAIM | no q-kernel, no finite source bound, and no arena projection pass |

## Decision
| decision_id | decision | result | rationale |
| --- | --- | --- | --- |
| DEC1543_0_progress | Local projection pack written. | FINITE_ROUTE_NOW_TEST_SHAPED | the finite coupling route now has source-side inputs and arena projection slots |
| DEC1543_1_priority | Prioritize C_qm provenance or zero theorem. | C_QM_FIRST | C_qm is the unique coefficient that can kill the stress-mediated term before matter-source size enters |
| DEC1543_2_no_claim | Do not run public/local claims. | CLAIM_BLOCKED | projection formulas are schema-only and values are missing |
| DEC1543_3_next | Next target is C_qm zero/provenance runner. | NEXT_1544_CQM_PROVENANCE | settle whether C_qm is theorem-zero or a sourced finite coefficient |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1543_0_sources_exist | PASS | all cited 1543 source paths exist |
| VAL1543_1_inputs_complete | PASS | finite source input rows are complete |
| VAL1543_2_arenas_complete | PASS | R10/PPN/clock/orbital projection rows are complete |
| VAL1543_3_bound_anchors | PASS | bound anchor links written |
| VAL1543_4_runner_blocked | PASS | R10 runner remains not computable |
| VAL1543_5_claim_gates_block | PASS | local GR claim remains blocked |
| VAL1543_6_decision_next | PASS | decision selects C_qm provenance next |
| VAL1543_7_next_target | PASS | next target is C_qm zero theorem or finite provenance runner |
| VAL1543_8_csv_parse | PASS | all generated 1543 CSVs parse cleanly |
| VAL1543_9_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1543_10_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1543_11_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1543_12_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1543_13_overall | PASS | 1543 writes the finite C_qm source-norm and local arena projection pack, keeps all projections noncomputable/nonclaim, and selects C_qm zero/provenance next |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT1543_0_1544 | 1544-Y5-Cqm-zero-theorem-or-finite-provenance-runner.md | scripts/Y5_Cqm_zero_theorem_or_finite_provenance_runner.py | try to close C_qm=0 from a parent q/v_m/observed-coframe theorem; if not, require finite C_qm provenance with units, source path, normalization, and local projection contract | do not use WEP/covariance/Ward shortcuts; do not insert placeholder C_qm; do not claim R10/PPN/local GR |
