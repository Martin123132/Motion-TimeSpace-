# 1227 Y5/R10 MICROSCOPE Portal Package Map Or Access Blocker

**Current verdict:** 1227 does **not** obtain a package map. It identifies the likely REGARDS/CMSM endpoint family, but local machine access to `cmsm-ds.onera.fr:443` is blocked, so no package names, URLs, AIP ids, checksums, or arrays are claimed.

**Main progress:** the acquisition route is now exact: candidate REGARDS endpoints are listed, package rows are deliberately left missing, access blockers are explicit, and a no-surrogate parser/intake contract is staged for future official files.

**Practical consequence:** `tau_WEP` remains symbolic-only. The next safe move is user-assisted package intake or a retry from a network/browser session that can reach CMSM.

## Source Register

| source_id | source_type | location | needle_or_evidence | purpose | absolute_path_or_url | source_recorded | evidence_recorded | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1227_0_1226_next | local | source-intake/mts_residuals/P8_Y5_R10_1226_NEXT_TARGET.csv | 1227-Y5-R10-MICROSCOPE-portal-package-map-or-access-blocker.md | 1226 handoff to CMSM package-map/access-blocker target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1226_NEXT_TARGET.csv | True | True | False | False |
| SRC1227_1_1226_required_objects | local | source-intake/mts_residuals/P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv | OBJ1226_0_official_CMSM_arrays | required official MICROSCOPE/tau_WEP data objects | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv | True | True | False | False |
| SRC1227_2_1226_portal_probe | local | source-intake/mts_residuals/P8_Y5_R10_1226_PUBLIC_PORTAL_PROBE.csv | PORT1226_0_CMSM_landing | previous CMSM portal probe result | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1226_PUBLIC_PORTAL_PROBE.csv | True | True | False | False |
| SRC1227_3_1226_no_surrogate | local | source-intake/mts_residuals/P8_Y5_R10_1226_NO_SURROGATE_POLICY.csv | SURR1226_0_official_arrays_only | no surrogate-as-claim policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1226_NO_SURROGATE_POLICY.csv | True | True | False | False |
| SRC1227_4_REGARDS_overview | web | https://regardsoss.github.io/ | REGARDS provides OpenSearch/GeoJSON/STAC discovery and HTTP serving of files | REGARDS platform behavior and expected portal capabilities | https://regardsoss.github.io/ | True | True | False | False |
| SRC1227_5_REGARDS_catalog_api | web | https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/api-swagger | catalog API includes complex search, engine searches, downloads, and OAuth2 authorization | candidate API route and auth expectations | https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/api-swagger | True | True | False | False |
| SRC1227_6_REGARDS_services | web | https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/service-plugins | catalog service plugin endpoint /api/v1/rs-catalog/services/{serviceId}/apply | candidate bulk download/service route | https://regardsoss.github.io/docs/1.14/development/backend/services/catalog/service-plugins | True | True | False | False |
| SRC1227_7_CMSM_portal | web | https://cmsm-ds.onera.fr/ | official CMSM data portal target from 1226 provenance | target portal for package enumeration | https://cmsm-ds.onera.fr/ | True | True | False | False |

## Network Probe

| probe_id | target | method | dns_status | addresses | tcp_status | error | package_map_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NET1227_0_CMSM_tcp | https://cmsm-ds.onera.fr/ | socket.getaddrinfo plus socket.create_connection timeout=5s | RESOLVED | 144.204.32.18 | CONNECT_FAILED | ConnectionRefusedError(10061, 'No connection could be made because the target machine actively refused it', None, 10061, None) | BLOCK_PACKAGE_ENUMERATION | False | False |
| NET1227_1_prior_curl_probe | https://cmsm-ds.onera.fr/* candidate routes | PowerShell curl.exe -I -L --max-time 15 | NOT_RECORDED_SEPARATELY |  | CONNECT_FAILED | curl: (7) Failed to connect to cmsm-ds.onera.fr port 443 after about 2.2s | BLOCK_PACKAGE_ENUMERATION | False | False |

## REGARDS Endpoint Candidates

| endpoint_id | url_or_template | route_type | purpose | auth_expectation | probe_status | map_result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| END1227_0_landing | https://cmsm-ds.onera.fr/ | landing | portal landing page | PUBLIC_UI_OR_REDIRECT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_1_user_project | https://cmsm-ds.onera.fr/user/microscope | ui | possible REGARDS project UI route noted in external references | PUBLIC_UI_OR_REDIRECT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_2_complex_search | https://cmsm-ds.onera.fr/api/v1/rs-catalog/complex/search | api_post | REGARDS complex search endpoint | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_3_opensearch_datasets | https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/opensearch/datasets/search | api_get | REGARDS engine dataset search | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_4_opensearch_dataobjects | https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/opensearch/dataobjects/search | api_get | REGARDS engine dataobject search | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_5_stac_collections | https://cmsm-ds.onera.fr/api/v1/rs-catalog/engines/stac/collections/search | api_get | REGARDS STAC-style collections search candidate | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_6_api_docs | https://cmsm-ds.onera.fr/api/v1/rs-catalog/v3/api-docs | api_get | possible instance OpenAPI docs | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_7_service_apply | https://cmsm-ds.onera.fr/api/v1/rs-catalog/services/{serviceId}/apply | api_post_template | REGARDS catalog service plugin route for bulk operations | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |
| END1227_8_download_file | https://cmsm-ds.onera.fr/api/v1/rs-catalog/downloads/{aip_id}/files/{checksum} | download_template | REGARDS file download route once AIP/checksum are known | REGARDS_OAUTH2_OR_PUBLIC_ROLE_DEPENDENT | NOT_PROBED_CONNECT_BLOCKED | NO_PACKAGE_NAMES | False | False |

## Package Map Status

| package_id | needed_for | expected_name_patterns | mapped_package_name | mapped_url | metadata_status | download_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PKG1227_0_official_arrays | OBJ1226_0_official_CMSM_arrays | SUEP;SUREF;science sessions;accelerometer;gx;gz;Sxx;Sxz;masks;calibration | MISSING_PACKAGE_NAME | MISSING_PACKAGE_URL | MISSING_METADATA | NOT_DOWNLOADED | False | False |
| PKG1227_1_documentation | OBJ1226_1_eta_product_convention;OBJ1226_6_reproducibility_metadata | documentation;data dictionary;product convention;eta;readme;license | MISSING_PACKAGE_NAME | MISSING_PACKAGE_URL | MISSING_METADATA | NOT_DOWNLOADED | False | False |
| PKG1227_2_orbit_attitude | OBJ1226_2_source_worldtube;OBJ1226_3_orbit_attitude_masks | orbit;attitude;session;segment;masks;time | MISSING_PACKAGE_NAME | MISSING_PACKAGE_URL | MISSING_METADATA | NOT_DOWNLOADED | False | False |
| PKG1227_3_material_response | OBJ1226_4_TiPt_material_tensor;OBJ1226_5_Delta_w_prior | material;Ti;PtRh;source-weight;composition;test mass | MISSING_PACKAGE_NAME | MISSING_PACKAGE_URL | MISSING_METADATA | NOT_DOWNLOADED | False | False |

## Access Blocker Ledger

| blocker_id | blocker | evidence | impact | resolution | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| ABLOCK1227_0_local_tcp | LOCAL_MACHINE_CANNOT_CONNECT_TO_CMSM_HTTPS | NET1227_0_CMSM_tcp plus prior curl probe | cannot enumerate or download official packages from this run | retry from browser/user network, VPN-free network, or user-assisted portal download | False | False |
| ABLOCK1227_1_api_auth_unknown | REGARDS_API_AUTH_OR_PUBLIC_ROLE_UNKNOWN | REGARDS catalog API docs list REGARDS_OAUTH2 for catalog/search/download endpoints | even with connectivity, API may require browser session/public-role token | inspect portal UI session/network calls or use public UI export/download if available | False | False |
| ABLOCK1227_2_no_package_identifiers | NO_AIP_ID_CHECKSUM_OR_PACKAGE_URL | package map rows all MISSING_PACKAGE_NAME/MISSING_PACKAGE_URL | download route cannot be constructed safely | obtain package metadata before any download attempt | False | False |
| ABLOCK1227_3_no_data_dictionary | NO_DATA_DICTIONARY_OR_COLUMN_SCHEMA | OBJ1226 required object metadata remains missing | parser/tau_WEP runner cannot interpret arrays even if files appear | download documentation/readme/data dictionary with the raw packages | False | False |

## Download Dry-Run Plan

| step_id | action | condition_to_execute | future_destination | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DRY1227_0_do_not_execute | download | mapped_package_url and license/access status are known | source-intake/microscope/raw/ | BLOCKED_NO_PACKAGE_URL | False | False |
| DRY1227_1_checksum | compute checksums | official files exist locally | source-intake/microscope/metadata/checksums.csv | BLOCKED_NO_FILES | False | False |
| DRY1227_2_manifest | write package manifest | package metadata and local file paths exist | source-intake/microscope/metadata/package_manifest.csv | BLOCKED_NO_METADATA | False | False |

## Manual Acquisition Instructions

| manual_step_id | instruction | success_evidence | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| MAN1227_0_open_portal | Open https://cmsm-ds.onera.fr/ in a normal browser and enter the MICROSCOPE project area. | screenshot or copied package list showing CMSM/MICROSCOPE package names | do not rename or reinterpret files before provenance is recorded | False | False |
| MAN1227_1_search_terms | Search for SUEP, SUREF, science sessions, accelerometer, readout, documentation, orbit, attitude, masks, gx, gz, Sxx, and Sxz. | package names, metadata fields, access/license status, and any data dictionary URLs | do not substitute paper equations for arrays | False | False |
| MAN1227_2_download_raw | If official downloads are available, save unmodified packages under source-intake/microscope/raw/ and docs under source-intake/microscope/docs/. | local file paths plus checksums and source URLs | do not mark valid_for_claim=true until parser verifies schema/units | False | False |
| MAN1227_3_report_blocker | If login/manual acceptance is required, record the exact screen text and whether account/request access is needed. | access-blocker note or portal export instructions | do not bypass access controls | False | False |

## Future Parser Contract

| parser_id | future_input | required_fields | first_validation | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PARSE1227_0_required_columns | official readout array files | time;session_id;segment_id;instrument/SU;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude/orbit convention | columns exist, units documented, sampling rate/session coverage recorded | WAITING_FOR_OFFICIAL_FILES | False | False |
| PARSE1227_1_metadata | CMSM data dictionary/readme | license/access status;citation;version/date;file checksums;units;coordinate frames;product convention | metadata links every parsed column to official documentation | WAITING_FOR_DOCUMENTATION | False | False |
| PARSE1227_2_tau_output | parsed official arrays and source/orbit/material products | tau_WEP_value_or_distribution;normalization;uncertainty;masking;session coverage;nonclaim flag until reviewed | tau_WEP product remains nonclaim until source-weight runner passes all gates | WAITING_FOR_INPUTS | False | False |

## Tau WEP Feed Update

| feed_id | target | update | tau_WEP_status | valid_prediction_rows_delta | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| FEED1227_0_to_1225 | ACQ1225_0_official_readout_arrays | package map attempted, but connectivity/package identifiers are blocked | SYMBOLIC_ONLY_NONCLAIM | 0 | False | False |
| FEED1227_1_to_1226 | OBJ1226 required data objects | required objects remain missing; manual acquisition instructions and parser contract staged | NO_OFFICIAL_ARRAYS_LOCAL | 0 | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1227_0_no_package_map | do not claim a CMSM package map | local machine cannot connect to CMSM and no package identifiers were obtained | user-assisted/browser portal package list or retry from a network that can reach CMSM | False | False |
| DEC1227_1_no_download | do not download or create raw data rows | there is no mapped package URL, AIP id, checksum, or license/access state | only execute dry-run download plan after package metadata exists | False | False |
| DEC1227_2_parser_ready | stage parser contract rather than parser code | without official files, parser code would be speculative and risk accepting wrong columns | build parser only after package docs reveal schema | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1227_0_sources | local and web source register | PASS | local handoff sources and web/API documentation sources are recorded | False | False |
| GATE1227_1_connectivity | local machine can reach CMSM portal | BLOCKED | tcp_status=CONNECT_FAILED | False | False |
| GATE1227_2_package_map | official package map | BLOCKED | package names/URLs/AIP ids/checksums are missing | False | False |
| GATE1227_3_download | official package download | BLOCKED | download dry run is blocked until package URL and license/access are known | False | False |
| GATE1227_4_parser | readout parser implementation | BLOCKED | schema/data dictionary not acquired | False | False |
| GATE1227_5_tau_WEP_claim | tau_WEP/local-GR/WEP claim permission | BLOCKED | no official data objects are mapped or local | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1227_0_1228 | 1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md | scripts/Y5_R10_MICROSCOPE_user_assisted_package_intake_contract.py | prepare a strict intake contract for user-assisted CMSM package files: allowed paths, required checksums, metadata fields, and parser refusal gates | if files appear under source-intake/microscope, the runner can verify provenance/schema or refuse them without claims | do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1227_0_local_sources_exist | all cited local sources exist | PASS | 4/4 local sources exist | False | False |
| VAL1227_1_local_needles_found | all cited local needles found | PASS | 4/4 local needles found | False | False |
| VAL1227_2_web_sources_recorded | web/API documentation sources recorded | PASS | SRC1227_4_REGARDS_overview; SRC1227_5_REGARDS_catalog_api; SRC1227_6_REGARDS_services; SRC1227_7_CMSM_portal | False | False |
| VAL1227_3_endpoint_candidates_staged | REGARDS endpoint candidates are staged | PASS | END1227_0_landing; END1227_1_user_project; END1227_2_complex_search; END1227_3_opensearch_datasets; END1227_4_opensearch_dataobjects; END1227_5_stac_collections; END1227_6_api_docs; END1227_7_service_apply; END1227_8_download_file | False | False |
| VAL1227_4_no_package_names_claimed | no package names or URLs are fabricated | PASS | all package rows remain MISSING_PACKAGE_NAME/MISSING_PACKAGE_URL | False | False |
| VAL1227_5_downloads_blocked | download plan is dry-run only | PASS | DRY1227_0_do_not_execute; DRY1227_1_checksum; DRY1227_2_manifest | False | False |
| VAL1227_6_blockers_recorded | access blockers are recorded | PASS | ABLOCK1227_0_local_tcp; ABLOCK1227_1_api_auth_unknown; ABLOCK1227_2_no_package_identifiers; ABLOCK1227_3_no_data_dictionary | False | False |
| VAL1227_7_parser_contract_nonclaim | future parser contract remains nonclaim | PASS | PARSE1227_0_required_columns; PARSE1227_1_metadata; PARSE1227_2_tau_output | False | False |
| VAL1227_8_tau_feed_nonclaim | tau_WEP feed remains nonclaim | PASS | valid_prediction_rows_delta=0 for tau feeds | False | False |
| VAL1227_9_claim_gates_blocked | claim gates keep physical claims blocked | PASS | connectivity/package/download/parser/tau claim gates blocked | False | False |
| VAL1227_10_next_target_intake | next target stages user-assisted intake contract | PASS | 1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md | False | False |
| VAL1227_11_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout claim-bearing tables | False | False |
| VAL1227_12_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1227_SOURCE_REGISTER.csv:8; P8_Y5_R10_1227_NETWORK_PROBE.csv:2; P8_Y5_R10_1227_REGARDS_ENDPOINT_CANDIDATES.csv:9; P8_Y5_R10_1227_PACKAGE_MAP_STATUS.csv:4; P8_Y5_R10_1227_ACCESS_BLOCKER_LEDGER.csv:4; P8_Y5_R10_1227_DOWNLOAD_DRY_RUN_PLAN.csv:3; P8_Y5_R10_1227_MANUAL_ACQUISITION_INSTRUCTIONS.csv:4; P8_Y5_R10_1227_FUTURE_PARSER_CONTRACT.csv:3; P8_Y5_R10_1227_TAU_WEP_FEED_UPDATE.csv:2; P8_Y5_R10_1227_DECISION_LEDGER.csv:3; P8_Y5_R10_1227_CLAIM_GATES.csv:6; P8_Y5_R10_1227_NEXT_TARGET.csv:1 | False | False |
| VAL1227_13_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1227_14_overall | overall 1227 validation | PASS | 1227 maps REGARDS/CMSM route candidates, records access blockers, and refuses fabricated package rows | False | False |
