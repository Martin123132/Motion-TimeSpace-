# 1546 - T_source Worldtube Normalization or Source Profile Acquisition

## Verdict
- `T_source_norm` is now defined as a legal source/worldtube normalization problem, not a fitted orbital-GM input.
- The clean candidate is `T_source_norm := ||delta S_matter/delta q||_{source,W}` or an equivalent same-frame Hilbert/Noether worldtube norm.
- Orbital `GM` import is explicitly rejected because it would smuggle the Newtonian readout into the source-side proof.
- No numeric/source-backed compact profile, units, dual norm, or arena profile map exists yet.
- No local GR/Newton/PPN/R10/clock/orbital claim is promoted.

## Source Register
| source_id | source_path | exists | purpose |
| --- | --- | --- | --- |
| SRC1546_0_1545_doc | 1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_1_1545_validation | source-intake/mts_residuals/P8_Y5_BRR545_1545_VALIDATION.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_2_1545_tsource | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1545_TSOURCE_NORM_GATE.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_3_1545_scg | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1545_SCG_ENVELOPE_STATUS_NONCLAIM.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_4_1544_projection | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_5_1543_arenas | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_6_source_current | source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_7_source_owner | source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_8_source_normalization_owner | source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_9_source_measure_flux | source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |
| SRC1546_10_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | input evidence for T_source_norm worldtube/source-profile normalization |

## Worldtube Requirements
| requirement_id | requirement | statement | current_status | reason |
| --- | --- | --- | --- | --- |
| WT1546_0_same_frame | same observed frame | source current, compact worldtube, clocks, photons, and orbital/readout maps must use the same e_obs/q_loc frame | CONDITIONAL_NOT_PARENT_DERIVED | SC0 and source-normalization owner rows remain conditional |
| WT1546_1_source_current | Hilbert/Noether current | tau_a^mu or T^{mu nu} is defined by variation of S_matter in the observed coframe before readout/scoring | CONDITIONAL_DEFINITION_ONLY | definition exists but not converted into compact source norm |
| WT1546_2_worldtube_domain | compact worldtube W | W must include support, boundary/excision convention, source profile, and exterior matching domain | MISSING_WORLDTUBE_PROFILE | no compact profile is source-backed here |
| WT1546_3_no_orbital_GM_import | no orbital GM import | T_source_norm cannot be set equal to fitted orbital GM or Kepler mass readout | REJECTED_SHORTCUT | orbital GM is an arena output/calibration target, not the source-side norm input |
| WT1546_4_norm_pairing | local dual norm | T_source_norm must be paired with C_qm so 1/2*T_source_norm*C_qm has E* forcing units | MISSING_NORM_AND_UNITS | cannot score until units and dual pairing are declared |
| WT1546_5_arena_compatibility | arena compatibility | one source profile must feed R10, PPN, clock, and orbital projections without retuning per arena | MISSING_ARENA_PROFILE_MAP | projection rows exist but profile-to-arena map is missing |

## T_source Definition Candidates
| definition_id | candidate | formula | current_status | reason |
| --- | --- | --- | --- | --- |
| TDEF1546_0_abstract_norm | abstract source-dual norm | T_source_norm := \|\|delta S_matter/delta q\|\|_{source,W} | DEFINITION_CANDIDATE | cleanest theory-side definition, but requires q/source norm and W profile |
| TDEF1546_1_Hilbert_worldtube | Hilbert-current worldtube norm | T_source_norm := \|\|T^{mu nu}[e_obs,psi]\|\|_{W,E*} or equivalent tau_a^mu norm | CONDITIONAL_CANDIDATE | requires same-frame Hilbert current and compact-body profile |
| TDEF1546_2_Noether_charge | Noether/Hamiltonian charge norm | T_source_norm may be bounded by an owned source charge only if source measure and flux closure are parent-derived | CONDITIONAL_NOT_CURRENTLY_AVAILABLE | source-measure theorem says charge identity is not parent-derived |
| TDEF1546_3_orbital_GM | orbital GM import | T_source_norm := GM_orbit or fitted Kepler mass | REJECTED | would smuggle the Newtonian readout into the source-side proof |
| TDEF1546_4_current_verdict | T_source_norm verdict | definition candidates exist, but no numeric/source-backed T_source_norm is available | NOT_SCORE_READY | needs worldtube profile, units, norm, and source path |

## Provenance Runner
| runner_id | check | current_status | reason |
| --- | --- | --- | --- |
| TPR1546_0_source_current | source_current_definition | CONDITIONAL_AVAILABLE | Hilbert/Noether current definition exists conditionally, but parent same-frame source theorem is unsigned |
| TPR1546_1_worldtube_profile | compact_worldtube_profile | MISSING | no compact profile/support/domain/excision convention is sourced |
| TPR1546_2_units | units_and_dual_norm | MISSING | T_source_norm units and pairing with C_qm are not declared |
| TPR1546_3_no_orbital_import | no_orbital_GM_import | PASS_GUARD | orbital GM import is explicitly rejected |
| TPR1546_4_arena_map | arena_profile_map | MISSING | R10/PPN/clock/orbit compatibility maps are not sourced |
| TPR1546_5_score_status | T_source_norm_score | REFUSED_NOT_SCORE_READY | missing profile, units, norm, source path, and arena map |

## Arena Compatibility
| arena_id | arena | compatibility_requirement | current_status |
| --- | --- | --- | --- |
| TARENA1546_0_R10 | R10 | source/test body convention, lambda profile, material/source profile, and T_source_norm norm must be mapped into Pi_R10 | MISSING_R10_PROFILE_MAP |
| TARENA1546_1_PPN | PPN | worldtube stress/current must map into weak-field source variables and PPN gauge response | MISSING_PPN_PROFILE_MAP |
| TARENA1546_2_clock | clock | same source profile must coexist with clock/readout sensitivity and calibration convention | MISSING_CLOCK_PROFILE_MAP |
| TARENA1546_3_orbital | orbital | orbital readout may compare against source norm but cannot define it | MISSING_ORBITAL_PROFILE_MAP |
| TARENA1546_4_local_GR | local GR | source profile must enter N_lock/Kmetric projection without absorbing residuals into GM calibration | BLOCKED_NO_CLAIM |

## Claim Gates
| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1546_0_requirements | worldtube requirements written | PASS_NONCLAIM | same-frame, current, profile, units, no-orbital-import, and arena map requirements are explicit |
| GATE1546_1_definition | T_source_norm definition candidate | PASS_NONCLAIM | definition candidates written but not score-ready |
| GATE1546_2_no_orbital_import | orbital GM import rejected | PASS_GUARD | source norm cannot be imported from orbital readout |
| GATE1546_3_Tsource_score | T_source_norm score-ready | BLOCKED | profile, units, norm, source path, and arena map missing |
| GATE1546_4_Scg_score | S_cg_norm computable | BLOCKED | T_source_norm and other envelope terms missing |
| GATE1546_5_local_GR | local GR/Newton/PPN claim | BLOCKED_NO_CLAIM | source/worldtube normalization remains nonclaim |

## Decision
| decision_id | decision | result | rationale |
| --- | --- | --- | --- |
| DEC1546_0_progress | T_source_norm is now a legal worldtube/source-profile problem. | WORLDTUBE_GATE_WRITTEN | source strength cannot be a fitted orbital readout |
| DEC1546_1_no_score | Do not score T_source_norm yet. | PROFILE_AND_UNITS_MISSING | no source-backed compact profile or norm exists |
| DEC1546_2_no_claim | Keep local claims blocked. | CLAIM_BLOCKED | S_cg remains noncomputable |
| DEC1546_3_next | Next target is the compact profile template/acquisition pack. | NEXT_1547_WORLD_PROFILE | make profile rows fillable for R10/PPN/clock/orbit without retuning per arena |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1546_0_sources_exist | PASS | all cited 1546 source paths exist |
| VAL1546_1_worldtube_requirements | PASS | all worldtube/source-profile requirements written |
| VAL1546_2_orbital_import_rejected | PASS | orbital GM import rejected |
| VAL1546_3_definition_candidates | PASS | definition candidates remain nonclaim/not score-ready |
| VAL1546_4_runner_refuses_score | PASS | T_source_norm runner refuses scoring |
| VAL1546_5_arena_maps | PASS | arena compatibility rows written |
| VAL1546_6_claim_gates_block | PASS | local GR claim remains blocked |
| VAL1546_7_decision_next | PASS | decision selects compact worldtube profile template next |
| VAL1546_8_next_target | PASS | next target is compact worldtube profile template and arena map |
| VAL1546_9_csv_parse | PASS | all generated 1546 CSVs parse cleanly |
| VAL1546_10_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1546_11_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1546_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1546_13_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1546_14_overall | PASS | 1546 defines the legal T_source_norm worldtube/source-profile requirements, rejects orbital GM import, keeps T_source non-score-ready, and selects compact profile template next |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT1546_0_1547 | 1547-Y5-compact-worldtube-profile-template-and-arena-map.md | scripts/Y5_compact_worldtube_profile_template_and_arena_map.py | create fillable compact-worldtube/source-profile rows for R10, PPN, clock, and orbital projections with units, support/domain conventions, and no per-arena retuning | do not use placeholder numeric profiles; do not import orbital GM as source norm; do not claim local GR or arena passes |
