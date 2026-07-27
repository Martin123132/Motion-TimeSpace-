# 1547 - Compact Worldtube Profile Template and Arena Map

## Verdict
- A shared compact-source template now exists for `W_src`, `J_q`, `T_source_norm`, support/domain conventions, and arena projections.
- The important guard is now explicit: arenas may have different projection operators, but they may not retune the compact profile parameters independently.
- R10, PPN, clock, orbital, and local-GR rows are fillable contracts only; no numeric profile or claim row is promoted.
- Orbital `GM`, R10 bound curves, clock calibration, and PPN fitted residuals remain forbidden as source-normalization inputs.
- Next step is to attempt one shared symbolic profile row, or write the exact source-data acquisition ledger if the parent action cannot supply it yet.

## Source Register
| source_id | source_path | exists | purpose |
| --- | --- | --- | --- |
| SRC1547_0_1546_doc | 1546-Y5-Tsource-worldtube-normalization-or-source-profile-acquisition.md | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_1_1546_validation | source-intake/mts_residuals/P8_Y5_BRR545_1546_VALIDATION.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_2_1546_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1546_NEXT_TARGET.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_3_1546_worldtube | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1546_WORLDTUBE_REQUIREMENTS.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_4_1546_tsource_def | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1546_TSOURCE_DEFINITION_CANDIDATES.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_5_1546_arena | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1546_TSOURCE_ARENA_COMPATIBILITY.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_6_1543_arenas | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_7_1544_projection | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_8_source_current | source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_9_source_owner | source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_10_source_normalization_owner | source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_11_source_measure_flux | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_12_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | input evidence for compact worldtube profile template and arena map |
| SRC1547_13_r10_review_curve | source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | True | input evidence for compact worldtube profile template and arena map |

## Compact Profile Template
| profile_id | arena | worldtube_symbol | source_current_symbol | normalization_condition | projection_symbol | current_status |
| --- | --- | --- | --- | --- | --- | --- |
| WTP1547_0_shared_core | shared_core | W_src | J_q := delta S_matter / delta q or same-frame tau_a^mu equivalent | T_source_norm := \|\|J_q\|\|_{source,W_src,E*}; not orbital GM | feeds Pi_R10, Pi_PPN, Pi_clock, Pi_orbital, and Pi_local through fixed theta_src | TEMPLATE_ONLY_MISSING_PARENT_PROFILE |
| WTP1547_1_R10 | R10 | W_R10 := projection of W_src into short-range lab geometry | J_q[W_src] carried into Pi_R10(lambda) | use shared T_source_norm; R10 may only supply Pi_R10(lambda) | alpha_R10(lambda) <= Pi_R10(lambda; W_src)*N_pair | MISSING_R10_PROFILE_MAP |
| WTP1547_2_PPN | PPN | W_PPN := weak-field exterior of W_src | J_q[W_src] and T^{mu nu}[e_obs, psi] moments | same T_source_norm; PPN response matrix cannot redefine source strength | Delta_PPN <= Pi_PPN[W_src,gauge]*N_lock | MISSING_PPN_PROFILE_MAP |
| WTP1547_3_clock | clock | W_clock := W_src seen by local redshift/frequency readout | J_q[W_src] with clock sensitivity split from source normalization | same T_source_norm; clock sensitivity is an arena projection coefficient | \|delta ln nu\| <= Pi_clock[W_src,readout]*N_lock | MISSING_CLOCK_PROFILE_MAP |
| WTP1547_4_orbital | orbital | W_orb := compact source plus orbital exterior matching zone | J_q[W_src] with orbital response map separated from Kepler mass readout | same T_source_norm; orbital GM is output/comparison only | \|delta a/a\| <= Pi_orbital[W_src]*N_lock | MISSING_ORBITAL_PROFILE_MAP |
| WTP1547_5_local_GR | local_GR | W_local := local compact source plus GR exterior comparison region | J_q[W_src] inserted into S_cg_norm and N_lock | same T_source_norm; no absorption into Newtonian mass calibration | residual_local <= Pi_local[W_src]*N_lock | BLOCKED_NO_CLAIM |

## Support and Domain Conventions
| convention_id | convention | requirement | current_status |
| --- | --- | --- | --- |
| SUP1547_0_same_frame | same-frame convention | all source, clock, photon, orbital, and metric readouts use the same e_obs/q_loc frame | CONDITIONAL_NOT_PARENT_SIGNED |
| SUP1547_1_compact_support | compact support | W_src must define interior support, exterior domain, and matching surface | MISSING_SOURCE_PROFILE |
| SUP1547_2_regularization | regularization/excision | point or ring limits require a regulator/excision rule before norms are finite | MISSING_REGULATOR |
| SUP1547_3_boundary_flux | boundary flux | flux/leakage through partial W_src must be included or proved zero | MISSING_BOUNDARY_LEDGER |
| SUP1547_4_unit_pairing | dual norm units | T_source_norm and C_qm units must pair into the S_cg envelope units | MISSING_UNITS |
| SUP1547_5_shared_parameters | shared profile parameters | theta_src may be projected differently by arenas but cannot be fitted independently per arena | PASS_GUARD_NONCLAIM |
| SUP1547_6_source_provenance | source path provenance | every numeric profile row must cite parent/source text, extraction method, and confidence | MISSING_NUMERIC_PROFILE |

## Arena Map Requirements
| map_id | arena | projection_contract | required_inputs | current_status |
| --- | --- | --- | --- | --- |
| MAP1547_0_R10 | R10 | alpha_R10(lambda) <= Pi_R10(lambda; W_src, theta_src) * [U_B_max*S_cg_norm + C_inner*\|Q_m^H\|] | lambda; bound curve; source/test body geometry; material convention; Pi_R10 operator; shared theta_src | MISSING_R10_PROFILE_MAP |
| MAP1547_1_PPN | PPN | Delta_PPN <= Pi_PPN(W_src, gauge, theta_src) * N_lock | weak-field metric map; response matrix; gauge convention; source multipoles; shared theta_src | MISSING_PPN_PROFILE_MAP |
| MAP1547_2_clock | clock | \|delta ln nu\| <= Pi_clock(W_src, readout, theta_src) * N_lock | clock sensitivity matrix; constants split; calibration convention; no shadow-clock frame; shared theta_src | MISSING_CLOCK_PROFILE_MAP |
| MAP1547_3_orbital | orbital | \|delta a/a\| or \|delta GM/GM\| <= Pi_orbital(W_src, theta_src) * N_lock | source measure; flux closure; exterior matching; orbital readout map; shared theta_src | MISSING_ORBITAL_PROFILE_MAP |
| MAP1547_4_local_GR | local_GR | residual_local <= Pi_local(W_src, theta_src) * N_lock with S_cg and boundary terms explicit | Kmetric conversion; PPN residual vector; source/boundary residuals; hidden-kernel terms; shared theta_src | BLOCKED_NO_CLAIM |

## No-Retuning Guard
| guard_id | guard | statement | current_status |
| --- | --- | --- | --- |
| NRT1547_0_shared_theta | theta_src shared | the compact profile parameters are selected once before arena projection | PASS_GUARD_NONCLAIM |
| NRT1547_1_projection_only | arena projection only | arenas may have Pi_arena operators but may not redefine T_source_norm | PASS_GUARD_NONCLAIM |
| NRT1547_2_no_orbital_GM_import | no orbital GM import | Kepler/ephemeris GM is a comparison output, not a source-normalization input | PASS_GUARD_NONCLAIM |
| NRT1547_3_no_bound_curve_fit | no R10 bound-curve fit as source | alpha(lambda) bound data cannot define the source current profile | PASS_GUARD_NONCLAIM |
| NRT1547_4_no_clock_calibration_absorption | no clock calibration absorption | frequency calibration cannot hide source residuals | PASS_GUARD_NONCLAIM |
| NRT1547_5_failure_policy | failure policy | if one arena needs a different theta_src, the shared-profile branch fails or splits into an explicit closure | PASS_GUARD_NONCLAIM |

## Refusal Runner
| runner_id | check | current_status | reason |
| --- | --- | --- | --- |
| RUN1547_0_profile_numeric | source-backed compact profile present | REFUSED_MISSING_PROFILE | no numeric/source-backed W_src or J_q profile has been supplied |
| RUN1547_1_units | units and dual norm declared | REFUSED_MISSING_UNITS | T_source_norm/C_qm dual pairing remains unscored |
| RUN1547_2_support | support/domain/excision complete | REFUSED_MISSING_DOMAIN | support and boundary conventions are templates only |
| RUN1547_3_no_orbital_import | orbital GM shortcut blocked | PASS_GUARD | orbital GM import remains rejected |
| RUN1547_4_no_retuning | per-arena retuning blocked | PASS_GUARD | theta_src must be shared across arena projections |
| RUN1547_5_arena_maps | arena projection maps computable | REFUSED_MISSING_ARENA_MAPS | Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local are not sourced |
| RUN1547_6_score_status | T_source_norm score-ready | REFUSED_NOT_SCORE_READY | template rows are legal scaffolding, not claim rows |

## Claim Gates
| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1547_0_template | compact profile template written | PASS_NONCLAIM | fillable shared W_src rows exist |
| GATE1547_1_support | support/domain conventions written | PASS_NONCLAIM | support, regularization, boundary, unit, and provenance needs are explicit |
| GATE1547_2_no_retuning | no per-arena retuning guard | PASS_GUARD | shared theta_src rule is explicit |
| GATE1547_3_Tsource_score | T_source_norm score-ready | BLOCKED | numeric/source-backed compact profile and units missing |
| GATE1547_4_arena_scores | R10/PPN/clock/orbital score-ready | BLOCKED_NO_CLAIM | arena projection maps remain missing |
| GATE1547_5_local_GR | local GR/Newton reduction claim | BLOCKED_NO_CLAIM | local residual vector cannot be closed from template rows |

## Decision
| decision_id | decision | result | rationale |
| --- | --- | --- | --- |
| DEC1547_0_progress | The worldtube profile branch now has a fillable shared-template contract. | PROFILE_TEMPLATE_WRITTEN | we can ask for one source profile instead of retuning every arena |
| DEC1547_1_no_score | Do not score T_source_norm yet. | PROFILE_UNITS_AND_ARENA_MAPS_MISSING | current rows are scaffolding only |
| DEC1547_2_guard | Per-arena retuning is forbidden. | NO_RETUNING_RULE_ACTIVE | otherwise R10, PPN, clock, and orbit would become separate patches |
| DEC1547_3_next | Next target is a shared symbolic profile runner or source-data acquisition ledger. | NEXT_1548_SHARED_PROFILE | try to instantiate the first shared W_src/J_q row, or record exactly why it cannot yet be sourced |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1547_0_sources_exist | PASS | all cited 1547 source paths exist |
| VAL1547_1_profile_template_arenas | PASS | profile template covers shared core, R10, PPN, clock, orbital, and local_GR |
| VAL1547_2_support_conventions | PASS | support/domain/unit/provenance conventions written |
| VAL1547_3_arena_maps | PASS | arena map requirements remain explicitly blocked |
| VAL1547_4_no_retuning_guard | PASS | shared theta/no-retuning guard active |
| VAL1547_5_orbital_import_rejected | PASS | orbital GM import remains rejected |
| VAL1547_6_runner_refuses_score | PASS | profile runner refuses scoring |
| VAL1547_7_claim_gates_block | PASS | local GR claim remains blocked |
| VAL1547_8_decision_next | PASS | decision selects shared profile runner/source acquisition next |
| VAL1547_9_next_target | PASS | next target is shared worldtube profile runner or source acquisition |
| VAL1547_10_csv_parse | PASS | all generated 1547 CSVs parse cleanly |
| VAL1547_11_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1547_12_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1547_13_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1547_14_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1547_15_overall | PASS | 1547 writes the compact worldtube profile template, support/domain conventions, arena map requirements, and no-retuning guard while keeping all local claims blocked |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT1547_0_1548 | 1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md | scripts/Y5_shared_worldtube_profile_symbolic_runner_or_source_data_acquisition.py | try to instantiate one shared symbolic compact-source profile with units/support conventions, or produce a source acquisition ledger if parent inputs are absent | do not insert numeric placeholder profiles; do not tune profile parameters per arena; do not claim R10, PPN, clock, orbital, or local-GR passes |
