# 1226 Y5/R10 MICROSCOPE Readout Source Acquisition Ledger

**Current verdict:** 1226 identifies the official MICROSCOPE/CMSM acquisition target and the exact objects needed for `tau_WEP`, but it does **not** acquire or enumerate official array packages. No data rows are fabricated.

**Main progress:** the bridge from symbolic `tau_WEP` to real data is now concrete: official CMSM arrays, eta product normalization, source worldtube/profile weighting, orbit/attitude/masks, Ti/Pt source-weight tensor, `Delta_w_TiPt`, and metadata are all listed as required objects.

**Practical consequence:** the next move is a safe portal/package map or access-blocker pass. Surrogates can be used only for smoke tests, never for WEP/local-GR claims.

## Source Register

| source_id | source_type | location | needle_or_evidence | purpose | absolute_path_or_url | source_recorded | evidence_recorded | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1226_0_1225_next | local | source-intake/mts_residuals/P8_Y5_R10_1225_NEXT_TARGET.csv | 1226-Y5-R10-MICROSCOPE-readout-source-acquisition-ledger.md | 1225 handoff to MICROSCOPE readout/source acquisition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1225_NEXT_TARGET.csv | True | True | False | False |
| SRC1226_1_1225_acquisition | local | source-intake/mts_residuals/P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv | ACQ1225_0_official_readout_arrays | tau_WEP required data objects | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv | True | True | False | False |
| SRC1226_2_1225_formula | local | source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | FORM1225_0_tau_WEP_functional | symbolic tau_WEP functional contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | True | True | False | False |
| SRC1226_3_1084_readout_gate | local | source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | RIG1084_0_CMSM_arrays | existing readout import gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv | True | True | False | False |
| SRC1226_4_1083_source_vector | local | source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | SCG1083_0_profile_weighting | existing source worldtube/profile weighting gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv | True | True | False | False |
| SRC1226_5_CMSM_portal | web | https://cmsm-ds.onera.fr/ | official MICROSCOPE data portal; web probe showed REGARDS OSS landing page, but no package enumeration captured in this run | primary public data portal for MICROSCOPE data/documentation | https://cmsm-ds.onera.fr/ | True | True | False | False |
| SRC1226_6_arxiv_ground_segment | web | https://arxiv.org/abs/2201.10841 | mission paper says CNES provided raw data and ONERA provided the Science Mission Centre of MICROSCOPE | provenance for CNES/ONERA/CMSM ground segment and data processing | https://arxiv.org/abs/2201.10841 | True | True | False | False |
| SRC1226_7_CNES_project | web | https://cnes.fr/en/projects/microscope | CNES project page identifies MICROSCOPE mission, partners, final results milestone, and Ti/Pt test masses | official mission/project provenance | https://cnes.fr/en/projects/microscope | True | True | False | False |
| SRC1226_8_CQG_result_data_availability | web | https://doi.org/10.1088/1361-6382/ac84be | data availability statement points to https://cmsm-ds.onera.fr/ after embargo | published result data-availability provenance | https://doi.org/10.1088/1361-6382/ac84be | True | True | False | False |
| SRC1226_9_Moriond_data_available | web | https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf | slides state data and documentation are available at https://cmsm-ds.onera.fr/ | secondary public pointer to data and documentation portal | https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf | True | True | False | False |

## Public Portal Probe

| probe_id | url | probe_method | observed_status | package_enumeration_status | download_status | interpretation | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PORT1226_0_CMSM_landing | https://cmsm-ds.onera.fr/ | web_open plus local PowerShell Invoke-WebRequest check | WEB_OPENED_REGARDS_OSS; POWERSHELL_REMOTE_CONNECT_FAILED | NOT_ENUMERATED | NO_DATA_DOWNLOADED | portal exists as the right target, but this run did not obtain a machine-readable package list | False | False |
| PORT1226_1_public_literature | https://arxiv.org/abs/2201.10841; https://doi.org/10.1088/1361-6382/ac84be | web search/open of public paper pages and snippets | DATA_PORTAL_PROVENANCE_FOUND | NO_ARRAY_FILE_NAMES_IDENTIFIED | NO_DATA_DOWNLOADED | literature proves where data should be, not the exact file objects needed by tau_WEP | False | False |

## Required Data Objects

| object_id | tau_WEP_role | required_content | expected_source | local_status | acquisition_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OBJ1226_0_official_CMSM_arrays | K_eta readout kernel and measured acceleration channel | time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention | https://cmsm-ds.onera.fr/ | NOT_PRESENT_IN_POST_CHECKPOINT_WORK | MISSING_PACKAGE_ENUMERATION | False | False |
| OBJ1226_1_eta_product_convention | normalization N_eta from source/material/readout response to reported Eotvos eta | data dictionary or analysis documentation defining product normalization and reported eta_AB convention | CMSM documentation or CQG data-analysis documentation | NOT_PRESENT_IN_POST_CHECKPOINT_WORK | MISSING_DOCUMENT_OBJECT | False | False |
| OBJ1226_2_source_worldtube | R_source and K_source Earth/source profile weighting | Earth/source stress/current profile and orbit-weighted source vector in observed local frame | CMSM source/orbit products plus Earth model documentation | NOT_PRESENT_IN_POST_CHECKPOINT_WORK | MISSING_SOURCE_PROFILE_OBJECT | False | False |
| OBJ1226_3_orbit_attitude_masks | orbit/session average and mask operator | orbit, attitude, time/session ids, masks, and segment definitions matched to SUEP/SUREF sessions | CMSM mission scenario/data products | NOT_PRESENT_IN_POST_CHECKPOINT_WORK | MISSING_ORBIT_MASK_OBJECT | False | False |
| OBJ1226_4_TiPt_material_tensor | R_material(TiPt) response to source-weight channel | TA6V minus PtRh10 source-weight response tensor, not only alpha/Coulomb delta-Q | MICROSCOPE material docs plus MTS source-weight convention | MATERIAL_PAIR_ONLY | MISSING_SOURCE_WEIGHT_TENSOR | False | False |
| OBJ1226_5_Delta_w_prior | finite source-weight amplitude multiplying tau_WEP | numeric Delta_w_TiPt prior width or parent theorem-zero proof, same convention as tau_WEP | MTS parent coupling derivation or source-backed finite prior | MISSING_NUMERIC_PRIOR_WIDTH | MISSING_THEORY_OR_PRIOR_INPUT | False | False |
| OBJ1226_6_reproducibility_metadata | schema and provenance for future runner | license/access status, file checksums, version/date, units, columns, session coverage, and citation | CMSM portal metadata or manually recorded data dictionary | NOT_PRESENT_IN_POST_CHECKPOINT_WORK | MISSING_METADATA | False | False |

## Acquisition Blocker Ledger

| blocker_id | object_id | blocker | required_resolution | claim_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| BLOCK1226_0_arrays | OBJ1226_0_official_CMSM_arrays | MISSING_PACKAGE_ENUMERATION | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_1_convention | OBJ1226_1_eta_product_convention | MISSING_DOCUMENT_OBJECT | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_2_worldtube | OBJ1226_2_source_worldtube | MISSING_SOURCE_PROFILE_OBJECT | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_3_masks | OBJ1226_3_orbit_attitude_masks | MISSING_ORBIT_MASK_OBJECT | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_4_tensor | OBJ1226_4_TiPt_material_tensor | MISSING_SOURCE_WEIGHT_TENSOR | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_5_prior | OBJ1226_5_Delta_w_prior | MISSING_THEORY_OR_PRIOR_INPUT | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |
| BLOCK1226_6_metadata | OBJ1226_6_reproducibility_metadata | MISSING_METADATA | acquire official object with provenance, or record a hard access blocker; do not fabricate substitute rows | tau_WEP remains SYMBOLIC_ONLY_NONCLAIM | False | False |

## No Surrogate Policy

| policy_id | forbidden_substitute | allowed_use | claim_rule | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| SURR1226_0_official_arrays_only | handmade gx/gz/Sxx/Sxz arrays or approximate orbital kernels | software smoke tests only, labelled surrogate and valid_for_claim=false | official CMSM/export arrays or exact equivalence proof required | ACTIVE | False | False |
| SURR1226_1_no_literature_to_arrays | using published eta result or paper equations as if they were time-series arrays | provenance, priors, and shape of analysis model | papers prove the target data exist, not the tau_WEP kernel | ACTIVE | False | False |
| SURR1226_2_no_tau_unity | setting tau_WEP=1 | none for claims | tau_WEP must be evaluated from source/worldtube/readout or theorem-zero | ACTIVE | False | False |

## Local Staging Manifest

| staging_id | future_local_path | contents | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| STAGE1226_0_raw | source-intake/microscope/raw/ | unmodified official downloaded packages, checksums, and access notes | DIRECTORY_NOT_CREATED_NO_DATA_DOWNLOADED | False | False |
| STAGE1226_1_docs | source-intake/microscope/docs/ | data dictionaries, CMSM documentation, readout convention notes, license/access metadata | DIRECTORY_NOT_CREATED_NO_DOCS_DOWNLOADED | False | False |
| STAGE1226_2_derived | source-intake/microscope/derived/ | future tau_WEP derived products generated from raw official objects | DIRECTORY_NOT_CREATED_NO_DERIVED_PRODUCTS | False | False |

## Tau WEP Feed Update

| feed_id | target | update | tau_WEP_status | valid_prediction_rows_delta | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| FEED1226_0_to_tau_WEP | FORM1225_0_tau_WEP_functional | public data portal and provenance identified, but no official array package enumerated or downloaded | SYMBOLIC_ONLY_NONCLAIM | 0 | False | False |
| FEED1226_1_to_source_weight_product | PROD1224_0_source_weight | source-weight product remains not scoreable because tau_WEP and Delta_w_TiPt are still missing | NOT_NUMERIC | 0 | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1226_0_portal_found_not_claim | record CMSM portal as the official acquisition target, not as acquired data | the run found public provenance but did not enumerate or download official packages | build a portal/package map or access-blocker probe | False | False |
| DEC1226_1_no_surrogate | forbid surrogate arrays for tau_WEP claim | tau_WEP depends on official readout/source/orbit conventions | only use surrogate data for smoke tests with valid_for_claim=false | False | False |
| DEC1226_2_data_plumbing_bottleneck | treat readout/source acquisition as the next bottleneck | the local-GR source-weight branch is now theory-contracted but not empirically scoreable | attempt a safe package-map/download dry run into D-drive staging paths | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1226_0_sources | local and web source register | PASS | local sources and public provenance URLs are recorded | False | False |
| GATE1226_1_portal_enumeration | CMSM package enumeration | BLOCKED | portal identified but package list not captured | False | False |
| GATE1226_2_required_objects | official readout/source objects acquired | BLOCKED | all required data objects remain missing/nonclaim | False | False |
| GATE1226_3_no_surrogate | no surrogate-as-claim | PASS | surrogate policy is active and blocks claim promotion | False | False |
| GATE1226_4_tau_WEP | tau_WEP numeric/source-backed | BLOCKED | tau_WEP remains symbolic-only | False | False |
| GATE1226_5_local_GR_WEP | local GR/WEP claim permission | BLOCKED | 1226 is acquisition plumbing only | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1226_0_1227 | 1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md | scripts/Y5_R10_MICROSCOPE_portal_package_map_or_access_blocker.py | attempt a safe CMSM portal/package map and dry-run download plan; if machine access fails, record exact access blockers and manual acquisition instructions | official package names/metadata are mapped or a hard blocker ledger explains why they could not be obtained, with no fabricated data rows | do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1226_0_local_sources_exist | all cited local sources exist | PASS | 5/5 local sources exist | False | False |
| VAL1226_1_local_needles_found | all cited local needles found | PASS | 5/5 local needles found | False | False |
| VAL1226_2_web_sources_recorded | web provenance URLs recorded | PASS | SRC1226_5_CMSM_portal; SRC1226_6_arxiv_ground_segment; SRC1226_7_CNES_project; SRC1226_8_CQG_result_data_availability; SRC1226_9_Moriond_data_available | False | False |
| VAL1226_3_required_objects_complete | required tau_WEP objects are listed | PASS | OBJ1226_0_official_CMSM_arrays; OBJ1226_1_eta_product_convention; OBJ1226_2_source_worldtube; OBJ1226_3_orbit_attitude_masks; OBJ1226_4_TiPt_material_tensor; OBJ1226_5_Delta_w_prior; OBJ1226_6_reproducibility_metadata | False | False |
| VAL1226_4_no_fabricated_acquisition | no official data object is falsely acquired | PASS | all required objects remain missing/package-unenumerated | False | False |
| VAL1226_5_blockers_materialized | missing objects have blockers | PASS | blocker_rows=7 | False | False |
| VAL1226_6_no_surrogate_policy | surrogate-as-claim policy active | PASS | SURR1226_0_official_arrays_only; SURR1226_1_no_literature_to_arrays; SURR1226_2_no_tau_unity | False | False |
| VAL1226_7_tau_feed_nonclaim | tau_WEP feed remains nonclaim | PASS | valid_prediction_rows_delta=0 for tau/product feeds | False | False |
| VAL1226_8_claim_gates_blocked | claim gates keep physical claims blocked | PASS | portal/object/tau/local claim gates blocked | False | False |
| VAL1226_9_next_target_package_map | next target stages package map/access blocker | PASS | 1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md | False | False |
| VAL1226_10_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout claim-bearing tables | False | False |
| VAL1226_11_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1226_SOURCE_REGISTER.csv:10; P8_Y5_R10_1226_PUBLIC_PORTAL_PROBE.csv:2; P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv:7; P8_Y5_R10_1226_ACQUISITION_BLOCKER_LEDGER.csv:7; P8_Y5_R10_1226_NO_SURROGATE_POLICY.csv:3; P8_Y5_R10_1226_LOCAL_STAGING_MANIFEST.csv:3; P8_Y5_R10_1226_TAU_WEP_FEED_UPDATE.csv:2; P8_Y5_R10_1226_DECISION_LEDGER.csv:3; P8_Y5_R10_1226_CLAIM_GATES.csv:6; P8_Y5_R10_1226_NEXT_TARGET.csv:1 | False | False |
| VAL1226_12_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1226_13_overall | overall 1226 validation | PASS | 1226 identifies official MICROSCOPE acquisition targets and blocks tau_WEP claims until real packages are mapped/acquired | False | False |
