# 1228 Y5/R10 MICROSCOPE User-Assisted Package Intake Contract

**Current verdict:** 1228 creates a strict local intake contract for future user-assisted CMSM/MICROSCOPE files. No official files are currently accepted for parsing, and `tau_WEP` remains symbolic-only.

**Main progress:** the drop-zone now exists under `source-intake/microscope/`, with raw/docs/metadata/derived/quarantine lanes, checksum inventory rules, provenance requirements, parser prechecks, and refusal gates.

**Practical consequence:** if official CMSM files are later downloaded manually, rerunning this script will inventory them and still refuse claims unless source URL, package id, checksum, license/access, and schema documentation are all present.

## Source Register

| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1228_0_1227_next | source-intake/mts_residuals/P8_Y5_R10_1227_NEXT_TARGET.csv | 1228-Y5-R10-MICROSCOPE-user-assisted-package-intake-contract.md | 1227 handoff to strict user-assisted package intake | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1227_NEXT_TARGET.csv | True | True | False | False |
| SRC1228_1_manual_instructions | source-intake/mts_residuals/P8_Y5_R10_1227_MANUAL_ACQUISITION_INSTRUCTIONS.csv | MAN1227_2_download_raw | manual download and reporting instructions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1227_MANUAL_ACQUISITION_INSTRUCTIONS.csv | True | True | False | False |
| SRC1228_2_parser_contract | source-intake/mts_residuals/P8_Y5_R10_1227_FUTURE_PARSER_CONTRACT.csv | PARSE1227_0_required_columns | future parser required fields | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1227_FUTURE_PARSER_CONTRACT.csv | True | True | False | False |
| SRC1228_3_package_status | source-intake/mts_residuals/P8_Y5_R10_1227_PACKAGE_MAP_STATUS.csv | PKG1227_0_official_arrays | package map remains missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1227_PACKAGE_MAP_STATUS.csv | True | True | False | False |
| SRC1228_4_access_blockers | source-intake/mts_residuals/P8_Y5_R10_1227_ACCESS_BLOCKER_LEDGER.csv | ABLOCK1227_0_local_tcp | CMSM access blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1227_ACCESS_BLOCKER_LEDGER.csv | True | True | False | False |
| SRC1228_5_required_objects | source-intake/mts_residuals/P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv | OBJ1226_0_official_CMSM_arrays | official tau_WEP data object requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1226_REQUIRED_DATA_OBJECTS.csv | True | True | False | False |
| SRC1228_6_tau_formula | source-intake/mts_residuals/P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | FORM1225_0_tau_WEP_functional | tau_WEP formula to be fed by accepted official files | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv | True | True | False | False |

## Intake Directory Contract

| directory_id | absolute_path | allowed_contents | forbidden_contents | current_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DIR1228_0_raw | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\raw | unmodified official CMSM downloaded package files only | handmade arrays, transformed files, renamed extracts without source metadata | READY_EMPTY_OR_WAITING | False | False |
| DIR1228_1_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\docs | official documentation, readme, data dictionary, license/access notes | unsourced notes used as data dictionary | READY_EMPTY_OR_WAITING | False | False |
| DIR1228_2_metadata | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\metadata | manifests, checksums, package provenance CSVs | claim flags or inferred package identities without source URL | READY_EMPTY_OR_WAITING | False | False |
| DIR1228_3_derived | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\derived | future parsed products from verified official files | derived tau_WEP values before schema/provenance gates pass | READY_EMPTY_OR_WAITING | False | False |
| DIR1228_4_quarantine | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine | files that exist locally but fail provenance/schema checks | any file promoted to parser input from quarantine | READY_EMPTY_OR_WAITING | False | False |

## Expected Package Classes

| class_id | expected_content | required_for | minimum_acceptance | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| CLASS1228_0_readout_arrays | official SUEP/SUREF readout arrays with time/session/segment/gx/gz/Sxx/Sxz/masks/calibration flags | K_eta and measured acceleration/readout part of tau_WEP | official source URL/package id, checksum, schema documentation, units, session coverage | False | False |
| CLASS1228_1_docs_dictionary | CMSM data dictionary/readme/product convention documentation | column meanings, eta normalization N_eta, frames, units, license/access | official document provenance and citation | False | False |
| CLASS1228_2_orbit_attitude_masks | orbit/attitude/session/mask products | orbit average and mask operator in tau_WEP | official source URL/package id, time convention, coordinate frame, units | False | False |
| CLASS1228_3_material_source_weight | Ti/Pt material response or source-weight convention inputs | R_material(TiPt) and Delta_w_TiPt branch | source-weight convention, material composition provenance, numeric prior or theorem-zero source | False | False |

## Local File Inventory

| inventory_id | relative_path | absolute_path | size_bytes | sha256 | package_class_guess | provenance_sidecar_found | schema_documentation_found | accepted_for_parser | refusal_reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INV1228_0_no_files | source-intake/microscope/raw;source-intake/microscope/docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope | 0 | NO_FILES | no_local_files | False | False | False | NO_OFFICIAL_FILES_PRESENT | False | False |

## Checksum Manifest

| checksum_id | relative_path | sha256 | size_bytes | source_url | package_id | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SHA1228_0_no_files | NO_FILES | NO_FILES | 0 | MISSING_SOURCE_URL | MISSING_PACKAGE_ID | False | False |

## Provenance Schema

| field_id | required_field | description | acceptance_rule | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| PROV1228_0_source_url | source_url | exact CMSM/official URL or portal package location used to obtain the file | must be nonempty and official before parser acceptance | False | False |
| PROV1228_1_package_id | package_id_or_aip_id | CMSM package name, AIP id, product id, or official export identifier | must link local file to portal metadata | False | False |
| PROV1228_2_checksum | sha256 | local file checksum computed after download | must be recorded before parsing and preserved unchanged | False | False |
| PROV1228_3_license_access | license_or_access_status | public/open/license accepted/login required/manual acquisition status | must be known before derived products are shared or claimed | False | False |
| PROV1228_4_schema_doc | schema_document_path | local official documentation defining columns, units, frames, and product convention | readout arrays cannot be parsed for tau_WEP without it | False | False |

## File Validation Rules

| rule_id | rule | failure_effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| RULE1228_0_path | file must be under source-intake/microscope/raw or source-intake/microscope/docs | quarantine/refuse | False | False |
| RULE1228_1_unmodified | raw files must be unmodified official packages, not manually edited extracts | quarantine/refuse | False | False |
| RULE1228_2_provenance | source_url, package id, checksum, access/license, and schema docs must be present | parser_refuses | False | False |
| RULE1228_3_columns | readout arrays must expose time, session/segment, SU, gx/gz/Sxx/Sxz, masks, calibration flags, orbit/attitude convention | tau_WEP_not_scoreable | False | False |
| RULE1228_4_no_claim | passing intake is not a WEP/local-GR claim; it only permits parser precheck | claim_allowed_always_false | False | False |

## Acceptance Gate Matrix

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| ACCEPT1228_0_files_present | official-looking files present locally | BLOCKED | local_file_count=0 | False | False |
| ACCEPT1228_1_provenance | provenance sidecar/manifest complete | BLOCKED | source_url/package_id/license/schema metadata not filled | False | False |
| ACCEPT1228_2_schema | schema documentation available | BLOCKED | no official data dictionary accepted | False | False |
| ACCEPT1228_3_parser | parser may read arrays | BLOCKED | requires files plus provenance plus schema | False | False |
| ACCEPT1228_4_tau_WEP | tau_WEP may be evaluated | BLOCKED | parser precheck and source/material product inputs not passed | False | False |

## Refusal Ledger

| refusal_id | target | refusal_reason | minimum_to_reconsider | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| REF1228_0_no_files | MICROSCOPE package intake | NO_OFFICIAL_FILES_PRESENT | official files under allowed paths plus provenance/source URL/checksum/schema documentation | False | False |
| REF1228_1_tau_WEP | tau_WEP parser/evaluation | INTAKE_GATES_BLOCKED | ACCEPT1228_0 through ACCEPT1228_3 pass; source/material inputs still separately required | False | False |

## Parser Precheck

| precheck_id | required_before_parser | current_status | future_check | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| PRE1228_0_readout_columns | accepted readout array file plus official schema docs | BLOCKED_NO_ACCEPTED_ARRAYS | verify time/session/segment/SU/gx/gz/Sxx/Sxz/masks/calibration/frames | False | False |
| PRE1228_1_metadata | accepted metadata/data dictionary | BLOCKED_NO_ACCEPTED_DOCUMENTATION | verify units, frames, product convention, version, license/access, citation | False | False |
| PRE1228_2_tau_output_guard | all parser checks pass | BLOCKED | tau_WEP output remains nonclaim until product runner and source-weight gates pass | False | False |

## Tau WEP Feed Update

| feed_id | target | update | tau_WEP_status | valid_prediction_rows_delta | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| FEED1228_0_to_1227 | PARSE1227 future parser contract | local drop-zone and intake contract created; no accepted files yet | WAITING_FOR_OFFICIAL_FILES | 0 | False | False |
| FEED1228_1_to_1225 | FORM1225_0_tau_WEP_functional | no parser/evaluation allowed until intake gates pass | SYMBOLIC_ONLY_NONCLAIM | 0 | False | False |

## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1228_0_dropzone_created | create local official-file drop-zone | machine CMSM access is blocked but user/browser/manual acquisition may succeed later | if files appear, rerun intake and refuse until provenance/schema gates pass | False | False |
| DEC1228_1_no_parser_without_docs | do not write a concrete parser yet | parser column assumptions would be speculative without official schema documentation | return to local-GR source-coupling derivation while data branch waits | False | False |
| DEC1228_2_data_pending | keep MICROSCOPE data branch pending but ready | intake gate can verify future files, but no official files are present now | work the analytic local-GR source-coupling contract without WEP claim promotion | False | False |

## Claim Gates

| gate_id | gate | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1228_0_sources | source path and needle audit | PASS | all local handoff sources are traceable | False | False |
| GATE1228_1_directories | intake directories available | PASS | raw/docs/metadata/derived/quarantine directories exist under source-intake/microscope | False | False |
| GATE1228_2_files | official files accepted | BLOCKED | no accepted official files with provenance/schema | False | False |
| GATE1228_3_parser | parser may run | BLOCKED | parser prechecks are blocked | False | False |
| GATE1228_4_tau_WEP | tau_WEP/local-GR/WEP claim permission | BLOCKED | intake contract only; no physical claim | False | False |

## Next Target

| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1228_0_1229 | 1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md | scripts/Y5_R10_data_pending_local_GR_source_coupling_contract.py | with MICROSCOPE official files pending, return to the analytic local-GR source-coupling contract and derive the exact conditions for universal source coupling without WEP claim promotion | the data branch stays ready for future official files, while the GR/Newton reduction branch gets a sharper source-coupling theorem or finite-residual contract | do not claim WEP/local-GR/PPN, do not use surrogate arrays as official, do not set tau_WEP to one, do not edit formalization-workbench or push GitHub | False | False |

## Validation

| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1228_0_sources_exist | all cited local sources exist | PASS | 7/7 sources exist | False | False |
| VAL1228_1_needles_found | all cited local needles found | PASS | 7/7 needles found | False | False |
| VAL1228_2_directories_exist | all intake directories exist | PASS | DIR1228_0_raw; DIR1228_1_docs; DIR1228_2_metadata; DIR1228_3_derived; DIR1228_4_quarantine | False | False |
| VAL1228_3_inventory_nonclaim | local inventory rows are nonclaim | PASS | inventory_rows=1 | False | False |
| VAL1228_4_no_claim_checksums | checksum manifest has no claimable rows | PASS | checksum_rows=1 | False | False |
| VAL1228_5_acceptance_blocks_parser | parser and tau gates remain blocked | PASS | parser/tau acceptance gates blocked | False | False |
| VAL1228_6_refusal_present | refusal ledger exists | PASS | REF1228_0_no_files; REF1228_1_tau_WEP | False | False |
| VAL1228_7_tau_feed_nonclaim | tau_WEP feed remains nonclaim | PASS | valid_prediction_rows_delta=0 for tau feeds | False | False |
| VAL1228_8_claim_gates_blocked | claim gates keep physical claims blocked | PASS | file/parser/tau claim gates blocked | False | False |
| VAL1228_9_next_target_local_GR | next target returns to analytic local-GR source coupling | PASS | 1229-Y5-R10-data-pending-local-GR-source-coupling-contract.md | False | False |
| VAL1228_10_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout claim-bearing tables | False | False |
| VAL1228_11_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1228_SOURCE_REGISTER.csv:7; P8_Y5_R10_1228_INTAKE_DIRECTORY_CONTRACT.csv:5; P8_Y5_R10_1228_EXPECTED_PACKAGE_CLASSES.csv:4; P8_Y5_R10_1228_LOCAL_FILE_INVENTORY.csv:1; P8_Y5_R10_1228_CHECKSUM_MANIFEST.csv:1; P8_Y5_R10_1228_PROVENANCE_SCHEMA.csv:5; P8_Y5_R10_1228_FILE_VALIDATION_RULES.csv:5; P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv:5; P8_Y5_R10_1228_REFUSAL_LEDGER.csv:2; P8_Y5_R10_1228_PARSER_PRECHECK.csv:3; P8_Y5_R10_1228_TAU_WEP_FEED_UPDATE.csv:2; P8_Y5_R10_1228_DECISION_LEDGER.csv:3; P8_Y5_R10_1228_CLAIM_GATES.csv:5; P8_Y5_R10_1228_NEXT_TARGET.csv:1 | False | False |
| VAL1228_12_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_after_run_start_count=0 | False | False |
| VAL1228_13_overall | overall 1228 validation | PASS | 1228 creates strict CMSM intake drop-zone and refuses parser/tau claims until official files and metadata pass gates | False | False |
