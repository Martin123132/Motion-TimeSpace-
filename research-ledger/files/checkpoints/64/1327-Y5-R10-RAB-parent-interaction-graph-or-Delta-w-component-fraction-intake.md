# 1327: RAB Parent Interaction Graph Or Delta-w Component Fraction Intake

**Current verdict:** 1327 does not close the parent interaction graph. The graph route remains exact conditional math, but no current edge counts as parent-signed connectedness evidence.

**Main progress:** the finite `Delta_w_TiPt` route is now source-intake ready: six component fractions for both TA6V and PtRh10 have explicit required source/method rows, and the validator handoff keeps all current proxy/toy rows quarantined.

**Decision:** no `Delta_w=0`, WEP, or local-GR claim. Next move is either a bounded source acquisition pass for real component fractions, or another graph-edge owner proof reentry.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1327_0_1326_next | source-intake/mts_residuals/P8_Y5_R10_1326_NEXT_TARGET.csv | NEXT1326_0_1327 | True | True | handoff into graph certificate or component-fraction intake | False | False |
| SRC1327_1_1326_finite | source-intake/mts_residuals/P8_Y5_R10_1326_FINITE_DELTA_W_PRIOR_CONTRACT.csv | FDW1326_2_component_formula | True | True | current Delta_w component formula | False | False |
| SRC1327_2_1232_graph | source-intake/mts_residuals/P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv | IGC1232_4_verdict | True | True | parent graph certificate attempt | False | False |
| SRC1327_3_1232_edges | source-intake/mts_residuals/P8_Y5_R10_1232_ORDINARY_MATTER_GRAPH_EDGE_AUDIT.csv | EDGE1232_0_electron_photon | True | True | ordinary matter graph edge audit | False | False |
| SRC1327_4_1233_validator | source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | fraction_value | True | True | component fraction schema | False | False |
| SRC1327_5_1233_dryrun | source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv | NO_CANDIDATE_FILES_PRESENT | True | True | validator dry-run status | False | False |
| SRC1327_6_1233_edge | source-intake/mts_residuals/P8_Y5_R10_1233_GRAPH_EDGE_DEMOTION_LEDGER.csv | EDGE1232_0_electron_photon | True | True | electron-photon edge demotion | False | False |
| SRC1327_7_1234_edges | source-intake/mts_residuals/P8_Y5_R10_1234_GRAPH_EDGE_STATUS_UPDATE.csv | EM_OWNER_UNIQUENESS_NOT_CLOSED | True | True | EM owner edge update | False | False |
| SRC1327_8_1235_edges | source-intake/mts_residuals/P8_Y5_R10_1235_GRAPH_EDGE_STATUS_UPDATE.csv | QCD_COLOR_EDGE_STAGED_NOT_SIGNED | True | True | QCD edge update | False | False |
| SRC1327_9_1236_edges | source-intake/mts_residuals/P8_Y5_R10_1236_GRAPH_EDGE_STATUS_UPDATE.csv | DEEPENED_BUT_NOT_SIGNED | True | True | latest edge status update | False | False |
| SRC1327_10_1232_pack | source-intake/mts_residuals/P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv | FSP1232_1_isotopic_abundances_masses | True | True | Ti/Pt component fraction source requirements | False | False |
| SRC1327_11_1232_quarantine | source-intake/mts_residuals/P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv | QUAR1232_0_983_proxy_vectors | True | True | toy/proxy quarantine policy | False | False |
| SRC1327_12_1231_map | source-intake/mts_residuals/P8_Y5_R10_1231_DELTA_W_COMPONENT_MAP.csv | DWM1231_1_TiPt_difference | True | True | Delta_w component map | False | False |

## Parent Graph Certificate Audit
| graph_id | target | current_status | evidence | blocks | counts_for_delta_w_zero | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GRAPH1327_0_connected_graph | parent ordinary-matter interaction graph certificate | GRAPH_CERTIFICATE_NOT_CLOSED | P8_Y5_R10_1232_INTERACTION_GRAPH_CERTIFICATE_ATTEMPT.csv:IGC1232_4_verdict | build parent interaction graph certificate or keep component-fraction source pack | False | False | False |
| GRAPH1327_1_edge_rollup | all useful graph edges parent-signed | NO_EDGE_COUNTS_FOR_CONNECTED_GRAPH | P8_Y5_R10_1233/1234/1235/1236_GRAPH_EDGE_STATUS_UPDATE | EM owner uniqueness, unique F2 certificate, QCD strong-sector owner, bound-state transfer, source-label forgetting | False | False | False |
| GRAPH1327_2_fallback_intake | strict component-fraction intake matrix | SOURCE_READY_MATRIX_REQUIRED | P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv;P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | no accepted fraction rows, no component priors, no tau_WEP | False | False | False |

## Graph Edge Status Rollup
| edge_id | latest_status | reason | counts_for_connected_graph | runner_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| EDGE1232_0_electron_photon | BLOCKED_BY_CERTIFICATE_NOT_DERIVED | typed certificate would close hidden branch but is not parent-derived; independent F2/readout branches remain open | False | graph_zero_refused | False | False |
| EDGE1232_1_quark_photon | PENDING | not attempted in 1236 | False | graph_zero_refused | False | False |
| EDGE1232_2_quark_gluon | DEEPENED_BUT_NOT_SIGNED | strong-sector owner, bound-state transfer, and source-label forgetting remain missing | False | graph_zero_refused | False | False |

## Delta-w Component Intake Matrix
| intake_id | material_id | component_id | target_quantity | required_source_or_method | current_evidence | current_status | required_columns | acceptance_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFI1327_TA6V_electron | TA6V | electron | electron/leptonic energy fraction | Z, isotope mix, electron rest/chemical binding convention, material mass normalization | Y_e proxy rows available from 983/1076 | PROXY_ONLY_NOT_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_electron | PtRh10 | electron | electron/leptonic energy fraction | Z, isotope mix, electron rest/chemical binding convention, material mass normalization | Y_e proxy rows available from 983/1076 | PROXY_ONLY_NOT_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_TA6V_light_quark | TA6V | light_quark | light-quark mass fraction | nucleon sigma terms or selected phenomenological mass-decomposition basis with citations | none in parent MTS basis | MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_light_quark | PtRh10 | light_quark | light-quark mass fraction | nucleon sigma terms or selected phenomenological mass-decomposition basis with citations | none in parent MTS basis | MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_TA6V_QCD_gluon | TA6V | QCD_gluon | QCD/gluon/nuclear bulk fraction | mass budget convention, residual bulk term, and no double-counting rule | none in parent MTS basis | MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_QCD_gluon | PtRh10 | QCD_gluon | QCD/gluon/nuclear bulk fraction | mass budget convention, residual bulk term, and no double-counting rule | none in parent MTS basis | MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_TA6V_EM_Coulomb | TA6V | EM_Coulomb | EM/Coulomb binding fraction | nuclear Coulomb energy model or DD alpha/Coulomb basis explicitly marked external | DD alpha/Coulomb smoke delta in 1080/1081 | SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_EM_Coulomb | PtRh10 | EM_Coulomb | EM/Coulomb binding fraction | nuclear Coulomb energy model or DD alpha/Coulomb basis explicitly marked external | DD alpha/Coulomb smoke delta in 1080/1081 | SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_TA6V_nuclear_surface | TA6V | nuclear_surface | nuclear surface/asymmetry fraction | nuclear binding/surface/asymmetry model with isotope/alloy averaging | DD surface smoke delta in 1080/1081 | SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_nuclear_surface | PtRh10 | nuclear_surface | nuclear surface/asymmetry fraction | nuclear binding/surface/asymmetry model with isotope/alloy averaging | DD surface smoke delta in 1080/1081 | SMOKE_DELTA_AVAILABLE_NOT_FULL_FRACTION | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_TA6V_measure_readout | TA6V | measure_readout | measure/readout reentry fraction | official CMSM/MICROSCOPE arrays accepted by 1228 gates plus source-worldtube/readout normalization | 1228 intake contract only | DATA_PENDING | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |
| CFI1327_PtRh10_measure_readout | PtRh10 | measure_readout | measure/readout reentry fraction | official CMSM/MICROSCOPE arrays accepted by 1228 gates plus source-worldtube/readout normalization | 1228 intake contract only | DATA_PENDING | row_id;material_id;component_id;fraction_value;fraction_uncertainty;basis_convention;source_path_or_url;extraction_method;valid_for_claim | WAITING_FOR_SOURCE_ROW | False | False |

## Component Intake Validator Handoff
| handoff_id | object | current_status | source | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| VALHAND1327_0_directories | component-fraction intake directories | READY | P8_Y5_R10_1233_COMPONENT_FRACTION_DIRECTORY_CONTRACT.csv | future raw/accepted/rejected component fraction rows have a controlled location | False | False |
| VALHAND1327_1_schema | component-fraction schema | REQUIRED_FIELDS_LOCKED | P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | candidate rows without numeric/source/basis/provenance fields are rejected | False | False |
| VALHAND1327_2_dryrun | current candidate scan | NO_CANDIDATE_FILES_PRESENT | P8_Y5_R10_1233_COMPONENT_FRACTION_VALIDATOR_DRYRUN.csv:DRY1233_0_candidate_scan | no accepted component-fraction rows currently exist | False | False |
| VALHAND1327_3_proxy_quarantine | toy/proxy material rows | QUARANTINED | P8_Y5_R10_1232_TOY_PROXY_QUARANTINE.csv | proxy Y_e, DD smoke deltas, and one-pair cancellation cannot feed claim rows | False | False |

## Delta-w Runner Update
| runner_id | target | input_status | missing_inputs | runner_status | claim_effect | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1327_0_graph_certificate | Delta_w_TiPt=0 via connected parent graph | GRAPH_CERTIFICATE_NOT_CLOSED | parent-signed vertices;parent-signed nonzero morphism edges;source functor;measure/current/readout owner | REFUSED_NO_ZERO_PROMOTION | no Delta_w=0, WEP, local-GR, or source-coupling pass | False | False | False | False |
| RUN1327_1_component_intake | Delta_w_TiPt=sum_c DeltaF_c delta_w_c + DeltaK_TiPt | SOURCE_READY_MATRIX_STAGED_NO_ROWS_ACCEPTED | accepted component fractions;component priors;readout residual;official tau_WEP | REFUSED_NOT_SCOREABLE | finite Delta_w branch is now intake-ready but nonclaim | False | False | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1327_0_no_template_edge_count | count graph template edges as connected parent graph evidence | REFUSED until edge status counts_for_connected_graph=true with parent proof | ENFORCED | False | False |
| SHORT1327_1_no_proxy_fractions | use Y_e/neutron/coulomb proxy vectors as component energy fractions | REFUSED by QUAR1232 and component schema gates | ENFORCED | False | False |
| SHORT1327_2_no_DD_smoke_as_parent_basis | use DD smoke alpha/surface deltas as MTS parent component fractions | REFUSED unless explicitly labelled external nonclaim comparator | ENFORCED | False | False |
| SHORT1327_3_no_threshold_prior | use the WEP bound as a Delta_w prior | REFUSED; threshold is a comparison fence only | ENFORCED | False | False |
| SHORT1327_4_no_local_GR_claim | claim GR/Newton source reduction from graph/intake scaffolding | REFUSED until graph theorem or finite residual bounds close with Bianchi/readout gates | ENFORCED | False | False |

## Decision Ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1327_0_graph_not_signed | do not claim parent graph connectedness | latest edge rollup has no edge counting for connected graph and the graph certificate remains template/conditional | Delta_w zero route remains alive but refused | False | False |
| DEC1327_1_component_intake_ready | stage source-ready Delta_w component-fraction intake matrix | finite fallback now needs real component fractions, component priors, and tau_WEP rather than proxy rows | future data rows have strict schema/provenance gates | False | False |
| DEC1327_2_next_best | next target should be a source acquisition dry-run or one more edge-owner proof | no candidate fraction rows are present and graph edges are still unsigned | 1328 should either fetch/source component-fraction references or attack EM/QCD owner certificate | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1327_0_1328 | 1328-Y5-R10-RAB-component-fraction-source-acquisition-or-EM-QCD-edge-owner-reentry.md | scripts/Y5_R10_RAB_component_fraction_source_acquisition_or_EM_QCD_edge_owner_reentry.py | try a bounded source acquisition pass for claim-grade component fractions; if not available, re-enter EM/QCD edge owner proof with exact blocker rows | either candidate fraction sources are staged with provenance and still nonclaim, or the next graph edge owner proof is narrowed without claiming connectedness | do not use proxy/toy rows, WEP thresholds, or template graph edges as evidence; do not claim Delta_w=0 or local GR | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1327_0_sources_exist | registered source paths exist and anchors are found | PASS | 13/13 source anchors found |
| VAL1327_1_graph_refused | parent interaction graph certificate remains refused | PASS | GRAPH1327_0_connected_graph=GRAPH_CERTIFICATE_NOT_CLOSED;GRAPH1327_1_edge_rollup=NO_EDGE_COUNTS_FOR_CONNECTED_GRAPH;GRAPH1327_2_fallback_intake=SOURCE_READY_MATRIX_REQUIRED |
| VAL1327_2_no_edges_count | latest graph edge rollup has no parent-signed connected edges | PASS | EDGE1232_0_electron_photon=BLOCKED_BY_CERTIFICATE_NOT_DERIVED;EDGE1232_1_quark_photon=PENDING;EDGE1232_2_quark_gluon=DEEPENED_BUT_NOT_SIGNED |
| VAL1327_3_component_intake_matrix | component intake matrix covers six components for TA6V and PtRh10 | PASS | component_intake_rows=12 |
| VAL1327_4_validator_handoff_nonclaim | validator handoff keeps accepted rows at zero and proxy rows quarantined | PASS | dryrun_status=NO_CANDIDATE_FILES_PRESENT;accepted_rows=0 |
| VAL1327_5_runner_refuses | graph and component intake runners remain refused | PASS | RUN1327_0_graph_certificate=REFUSED_NO_ZERO_PROMOTION;RUN1327_1_component_intake=REFUSED_NOT_SCOREABLE |
| VAL1327_6_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1327_0_no_template_edge_count;SHORT1327_1_no_proxy_fractions;SHORT1327_2_no_DD_smoke_as_parent_basis;SHORT1327_3_no_threshold_prior;SHORT1327_4_no_local_GR_claim |
| VAL1327_7_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1327_8_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1327_9_next_target_1328 | next target routes to component source acquisition or EM/QCD edge owner reentry | PASS | 1328-Y5-R10-RAB-component-fraction-source-acquisition-or-EM-QCD-edge-owner-reentry.md |
| VAL1327_10_overall | overall 1327 validation | PASS | 1327 refuses graph zero, stages source-ready component intake matrix, and preserves nonclaim gates |
