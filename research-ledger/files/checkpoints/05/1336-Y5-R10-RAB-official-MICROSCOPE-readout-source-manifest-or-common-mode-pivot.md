# 1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot

**Current verdict:** 1336 does not score WEP and does not claim local GR. It turns the MICROSCOPE side into an acquisition-ready manifest, confirms no official readout/source/product files are locally present, and parks the finite-electron WEP route.

**Main progress:** the official data route now has named directories, expected schemas, source strings, anti-shortcut gates, and a runner waitstate. Because the real arrays and product convention are still absent, the next best move is the parent common-mode/no-source-prefactor derivation route.

**Decision:** pivot next to common-mode parent-action premise reduction unless real official MICROSCOPE files are imported first.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1336_0_1335_next | source-intake/mts_residuals/P8_Y5_R10_1335_NEXT_TARGET.csv | NEXT1335_0_1336 | True | True | selected 1336 target | False | False |
| SRC1336_1_1335_manifest | source-intake/mts_residuals/P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv | MAN1335_0_readout_arrays | True | True | official input waitstate from 1335 | False | False |
| SRC1336_2_1335_waitstate | source-intake/mts_residuals/P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv | WAIT1335_0_official_arrays | True | True | readout/source blocker list | False | False |
| SRC1336_3_1335_contract | source-intake/mts_residuals/P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv | tau_eff_e | True | True | symbolic WEP product contract | False | False |
| SRC1336_4_1335_validation | source-intake/mts_residuals/P8_Y5_BRR545_1335_VALIDATION.csv | VAL1335_10_overall | True | True | 1335 pass gate | False | False |
| SRC1336_5_1069_provenance | source-intake/mts_residuals/P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv | PROV1069_1_R0_direct_geometry | True | True | PRL final eta provenance | False | False |
| SRC1336_6_1070_external | source-intake/mts_residuals/P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv | EXT1070_5_CQG_data_availability | True | True | CQG readout/data-availability provenance | False | False |
| SRC1336_7_1072_external | source-intake/mts_residuals/P8_Y5_R10_1072_EXTERNAL_SOURCE_LEDGER.csv | EXT1072_1_ONERA_data_available | True | True | ONERA/CMSM portal provenance | False | False |
| SRC1336_8_1072_api | source-intake/mts_residuals/P8_Y5_R10_1072_CMSM_REGARDS_API_CANDIDATE_ENDPOINTS.csv | API1072_1_dataset_search | True | True | candidate REGARDS API endpoints | False | False |
| SRC1336_9_1072_probe | source-intake/mts_residuals/P8_Y5_R10_1072_PORTAL_ROUTE_PROBE.csv | https://cmsm-ds.onera.fr/user/microscope | True | True | previous portal route probe | False | False |

## Web Source Candidate Register
| web_id | url | source_type | expected_use | local_support | acquisition_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WEB1336_0_ONERA_public_data_page | https://microscope.onera.fr/fr/publication/microscope-data-are-available | official mission data page | points users to the MICROSCOPE CMSM portal | SRC1336_7_1072_external | SOURCE_STRING_RECORDED_NOT_IMPORTED | False | False |
| WEB1336_1_CMSM_MICROSCOPE_portal | https://cmsm-ds.onera.fr/user/microscope | official data portal | download/export official readout, calibrated, auxiliary, and orbit products | SRC1336_7_1072_external;SRC1336_9_1072_probe | PORTAL_TARGET_RECORDED_ARRAYS_NOT_IMPORTED | False | False |
| WEB1336_2_CQG_final_result | https://arxiv.org/abs/2209.15488 | final MICROSCOPE CQG analysis paper | eta formula, readout axis, segment/orbit counts, analysis band, data availability statement | SRC1336_6_1070_external | SOURCE_STRING_RECORDED_FORMULAE_ALREADY_LEDGERED | False | False |
| WEB1336_3_PRL_final_result | https://arxiv.org/abs/2209.15487 | final MICROSCOPE PRL result | eta_TiPt bound anchor and mission context | SRC1336_5_1069_provenance | SOURCE_STRING_RECORDED_BOUND_ANCHOR_ALREADY_LEDGERED | False | False |

## Local MICROSCOPE Intake Audit
| audit_id | absolute_path | purpose | exists | file_count | usable_for_claim_now | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LOCAL1336_0_base | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope | MICROSCOPE intake root | True | 12 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_1_raw | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\raw | raw download quarantine/incoming source | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_2_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\docs | downloaded documentation/manuals | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_3_derived | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\derived | future reproducible derived products | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_4_quarantine | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine | uncertain files not usable for claim | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_5_metadata | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\metadata | schemas, manifests, validation outputs | True | 12 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_6_official_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\official_readout | official exported MICROSCOPE readout arrays | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_7_source_worldtube | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\source_worldtube | Earth/source profile and orbit weighting inputs | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_8_product_convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\product_convention | eta/product/readout convention evidence | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |
| LOCAL1336_9_branch_classifier | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_classifier | same-parent-branch classifier inputs | True | 0 | False | DIRECTORY_READY_FILES_PENDING | False | False |

## Official Readout Schema
| schema_id | column | dtype | definition | source_requirement | required_status | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| READSCHEMA1336_0_time_s | time_s | float | seconds or mission time with declared epoch | official readout export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_1_session_id | session_id | string | MICROSCOPE science session/segment id | official readout export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_2_orbit_id | orbit_id | string/integer | orbit identifier or reconstructable orbit phase key | official orbit/readout export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_3_axis | axis | string | reported accelerometer axis; sensitive X axis must be explicit | CQG/readout metadata | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_4_gx_m_s2 | gx_m_s2 | float | gravity projection on x in m/s^2 | official or reproducible CQG design matrix | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_5_gz_m_s2 | gz_m_s2 | float | gravity projection on z in m/s^2 | official or reproducible CQG design matrix | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_6_Sxx | Sxx | float | gravity-gradient/readout design column Sxx | official or reproducible CQG design matrix | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_7_Sxz | Sxz | float | gravity-gradient/readout design column Sxz | official or reproducible CQG design matrix | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_8_mask_flag | mask_flag | boolean/string | mask/quality flag matching final analysis cuts | official readout export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_9_calibration_flag | calibration_flag | boolean/string | calibration state or exclusion marker | official readout export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_10_attitude_or_axis | attitude_quaternion_or_axis | string/float-array | attitude or axis convention sufficient to reproduce projection | official auxiliary/orbit export | required | MISSING_OFFICIAL_FILE | False | False |
| READSCHEMA1336_11_source_url_or_path | source_url_or_path | string | official file path, URL, or DOI-backed source | local import manifest | required | MISSING_OFFICIAL_FILE | False | False |

## Source Worldtube Schema
| schema_id | column | dtype | definition | source_requirement | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRCSCHEMA1336_0_time_or_orbit_phase | time_s_or_orbit_phase | float | time or orbit phase matched to readout rows | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_1_radius_m | radius_m | float | source-shell radius in metres | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_2_density_kg_m3 | density_kg_m3 | float | mass/stress density profile used for source weighting | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_3_source_component | source_component | string | Earth/source component or stress/current slot | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_4_kernel_weight | kernel_weight | float | projection/readout/source weight for the component | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_5_model_or_dataset | model_or_dataset | string | PREM/geopotential/or official mission auxiliary product name | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |
| SRCSCHEMA1336_6_source_url_or_path | source_url_or_path | string | source-backed path or URL | source profile plus orbit/readout projection must be reproducible | MISSING_SOURCE_WORLDTUBE_FILE | False | False |

## Product Convention Schema
| schema_id | field | dtype | definition | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PRODSCHEMA1336_0_eta_formula | eta_formula | string | eta(A,B)=2(a_A-a_B)/(a_A+a_B) or the exact mission convention used | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_1_sign_convention | sign_convention | string | which body order and which readout axis define positive eta | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_2_tau_eff_definition | tau_eff_definition | string | tau_eff = K_readout*S_source*O_orbit in a single observed branch | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_3_readout_kernel_units | readout_kernel_units | string | units that convert design/readout columns into eta response | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_4_source_kernel_units | source_kernel_units | string | units of the source-worldtube weighted response | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_5_orbit_average_rule | orbit_average_rule | string | averaging/masking rule matching the final reported eta channel | MISSING_PRODUCT_CONVENTION_FILE | False | False |
| PRODSCHEMA1336_6_branch_lock | branch_lock | string | same parent branch id for coefficient, material contrast, source, readout, and bound | MISSING_PRODUCT_CONVENTION_FILE | False | False |

## Branch Classifier Schema
| schema_id | field | dtype | definition | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| BRANCHSCHEMA1336_0_same_parent_branch_id | same_parent_branch_id | string | single identifier linking epsilon_e, DeltaF_e, tau_eff_e, source worldtube, readout kernel, and eta bound | MISSING_PARENT_BRANCH_CLASSIFIER | False | False |
| BRANCHSCHEMA1336_1_forbidden_mixing_rule | forbidden_mixing_rule | string | explicit rule rejecting products assembled from incompatible parent branches or surrogate/readout conventions | MISSING_PARENT_BRANCH_CLASSIFIER | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1336_0_no_sensitivity_claim | use epsilon_e sensitivity rows as WEP evidence | REFUSED | ENFORCED | False | False |
| SHORT1336_1_no_surrogate_arrays | treat dry-run/reconstructed arrays as official MICROSCOPE arrays | REFUSED | ENFORCED | False | False |
| SHORT1336_2_no_unity_tau | set tau_eff_e=1 without readout/source/product derivation | REFUSED | ENFORCED | False | False |
| SHORT1336_3_no_local_GR_claim | claim WEP or local-GR reduction from acquisition manifest only | REFUSED | ENFORCED | False | False |

## Common-Mode Pivot Decision
| decision_id | route | current_state | because | next_action | selected_now | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PIVOT1336_0_official_data_route | finite electron WEP data-intake route | PAUSED_WAITING_FOR_OFFICIAL_INPUTS | official readout arrays, source worldtube, product convention, and same-branch classifier are not locally present | only resume after source-backed files exist in official_readout/source_worldtube/product_convention/branch_classifier | False | False | False |
| PIVOT1336_1_common_mode_theory_route | parent common-mode/source-prefactor derivation route | SELECTED_NEXT | data plumbing is acquisition-ready but not filled; the derivation route attacks the actual coupling gap directly | reduce the no-source-prefactor/common-mode clause to the smallest parent action premise or exhibit an admissible countermodel | True | False | False |

## Runner Status
| runner_id | target | input_status | runner_status | score_ready | reason | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1336_0_schema_manifest | official MICROSCOPE readout/source/product manifest | SCHEMAS_WRITTEN_SOURCE_STRINGS_RECORDED | ACQUISITION_READY_NONCLAIM | False | schemas and directories exist but official files are absent | False | False | False |
| RUN1336_1_WEP_product | epsilon_e WEP product | WAITSTATE_PERSISTENT | BLOCKED_NOT_SCOREABLE | False | tau_eff_e remains source/readout/product-convention undefined | False | False | False |
| RUN1336_2_common_mode_pivot | parent common-mode/no-source-prefactor theorem | THEORY_ROUTE_SELECTED | NEXT_DERIVATION_TARGET | False | the coupling gap is now cleaner than the data route for immediate progress | False | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1336_0_1337 | 1337-Y5-R10-RAB-common-mode-parent-action-premise-reduction-or-readout-data-intake.md | scripts/Y5_R10_RAB_common_mode_parent_action_premise_reduction_or_readout_data_intake.py | try to reduce the common-mode/no-source-prefactor condition to the smallest parent action premise while keeping the official MICROSCOPE intake route parked and schema-ready | either derive a stronger parent common-mode condition, exhibit the smallest admissible countermodel, or import real official readout/source/product files without scoring them | do not claim WEP/local-GR from this manifest, do not use surrogate arrays as official data, do not branch-mix finite coefficients | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1336_0_sources_exist | registered local source paths exist and anchors are found | PASS | 10/10 source anchors found |
| VAL1336_1_web_strings_recorded | official web source strings are recorded | PASS | https://microscope.onera.fr/fr/publication/microscope-data-are-available;https://cmsm-ds.onera.fr/user/microscope;https://arxiv.org/abs/2209.15488;https://arxiv.org/abs/2209.15487 |
| VAL1336_2_official_dirs_ready | official intake directories exist | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\official_readout;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\source_worldtube;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\product_convention;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_classifier |
| VAL1336_3_official_files_absent | official readout/source/product/branch files are not silently present | PASS | official_readout=0;source_worldtube=0;product_convention=0;branch_classifier=0 |
| VAL1336_4_schemas_complete | readout, source, product, and branch schemas are present | PASS | readout=12;source=7;product=7;branch=2 |
| VAL1336_5_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1336_0_no_sensitivity_claim;SHORT1336_1_no_surrogate_arrays;SHORT1336_2_no_unity_tau;SHORT1336_3_no_local_GR_claim |
| VAL1336_6_common_mode_pivot_selected | common-mode theory route is selected while data files are absent | PASS | PIVOT1336_1_common_mode_theory_route selected |
| VAL1336_7_runner_blocks_score | runner refuses WEP/local-GR scoring | PASS | RUN1336_0_schema_manifest=ACQUISITION_READY_NONCLAIM;RUN1336_1_WEP_product=BLOCKED_NOT_SCOREABLE;RUN1336_2_common_mode_pivot=NEXT_DERIVATION_TARGET |
| VAL1336_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false where present |
| VAL1336_9_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1336_10_next_target_1337 | next target routes to common-mode parent premise reduction or official intake | PASS | 1337-Y5-R10-RAB-common-mode-parent-action-premise-reduction-or-readout-data-intake.md |
| VAL1336_11_overall | overall 1336 validation | PASS | 1336 makes MICROSCOPE intake source-ready, blocks WEP scoring, and selects the common-mode coupling derivation route |
