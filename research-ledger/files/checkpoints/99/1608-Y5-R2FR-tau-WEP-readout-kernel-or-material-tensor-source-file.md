# 1608 - R2/fR tau_WEP Readout Kernel Or Material Tensor Source File

## Verdict
- 1608 turns the WEP/tau problem into a strict input contract: `tau_WEP = N_eta^{-1}<K_CMSM, S_Earth x M_TiPt>` in one branch-locked convention.
- The exact amplitude law remains conditional: `|Delta_w_TiPt| <= 2.8e-15/tau_min` only after a sourced `tau_min>0` exists.
- No live official CMSM/readout/source/material/alignment files are present; templates are written only as quarantine input contracts.
- The parent nondegeneracy theorem is not in the corpus; symbolic readout structure alone does not exclude the null-space countermodel.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1608_0_1607_doc | 1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md | True | True | DEC1607_2_next; NEXT_1608_TAU_WEP_READOUT_KERNEL_OR_MATERIAL_TENSOR_SOURCE_FILE |
| SRC1608_1_1607_validation | source-intake/mts_residuals/P8_Y5_BRR545_1607_VALIDATION.csv | True | True | VAL1607_OVERALL; PASS |
| SRC1608_2_1607_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1607_NEXT_TARGET.csv | True | True | 1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md; tau_WEP |
| SRC1608_3_1607_bound | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1607_BOUND_INVERSION_AUDIT.csv | True | True | BIA1607_0_electron_proxy_product; BOUND_INVERSION_PROXY_DETECTED |
| SRC1608_4_1596_law | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv | True | True | TCL1596_2_delta_w_amplitude_law; EXACT_CONDITIONAL_AMPLITUDE_LAW |
| SRC1608_5_1596_audit | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv | True | True | TFA1596_4_readout_matrix; OFFICIAL_ARRAYS_NOT_IMPORTED |
| SRC1608_6_1596_acq | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv | True | True | TSA1596_0_readout_matrix; SOURCE_NEEDED |
| SRC1608_7_1597_tau | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv | True | True | TLB1597_3_current_corpus_verdict; TAU_LOWER_BOUND_NOT_DERIVED |
| SRC1608_8_1597_null | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1597_NULL_SPACE_COUNTERMODEL.csv | True | True | NSC1597_0_linear_space_model; tau_WEP can vanish |
| SRC1608_9_1597_inputs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1597_REQUIRED_NONDEGENERACY_INPUTS.csv | True | True | NDI1597_3_alignment; MISSING_CRITICAL |
| SRC1608_10_1598_kernel | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv | True | True | MKS1598_1_official_CMSM_arrays; OFFICIAL_ARRAYS_NOT_IMPORTED |
| SRC1608_11_1598_requirements | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1598_ALIGNMENT_IMPORT_REQUIREMENTS.csv | True | True | AIR1598_2_K_CMSM; MISSING_OFFICIAL_ARRAYS |
| SRC1608_12_1598_probe | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1598_CMSM_PORTAL_PROBE_SYNTHESIS.csv | True | True | CPS1598_3_current_shell_probe; TIMEOUT_OR_NO_USABLE_FILELIST |
| SRC1608_13_1598_nondeg | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1598_PARENT_NONDEGENERACY_AUDIT.csv | True | True | PNA1598_2_data_theorem_equivalence; OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_STILL_REQUIRED |
| SRC1608_14_1455_readout | source-intake/microscope/branch_locked_wep/coefficients/official_readout_acquisition_ledger_nonclaim_1455.csv | True | True | KC1455_6_parser_gate; NONCLAIM_ONLY |
| SRC1608_15_1456_kinputs | source-intake/microscope/branch_locked_wep/coefficients/official_KCMSM_bound_inputs_nonclaim_1456.csv | True | True | KBI1456_6_data_portal; POINTER_ONLY_ACCESS_UNVERIFIED |
| SRC1608_16_1456_worldtube | source-intake/microscope/branch_locked_wep/coefficients/source_worldtube_projection_theorem_attempt_1456.csv | True | True | SWP1456_6_verdict; THEOREM_CONDITIONAL_NOT_PROMOTED |
| SRC1608_17_1457_pilot | source-intake/microscope/branch_locked_wep/coefficients/source_worldtube_pilot_ledger_nonclaim_1457.csv | True | True | PILOT1457_7_verdict; PILOT_BLOCKED_NONCLAIM |
| SRC1608_18_1465_capture_plan | source-intake/microscope/branch_locked_wep/coefficients/CMSM_session_filelist_capture_plan_nonclaim_1465.csv | True | True | CAP1465_1_filelist_fields; MISSING_FILELIST |
| SRC1608_19_1466_capture_workflow | source-intake/microscope/branch_locked_wep/coefficients/CMSM_browser_session_capture_workflow_nonclaim_1466.csv | True | True | CAP1466_5_import_guard; GUARD_ACTIVE_NONCLAIM |
| SRC1608_20_1600_har | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1600_HAR_INTAKE_STATUS.csv | True | True | HAR1600_0_input_folder_empty; NO_HAR_JSON_CSV_EVIDENCE_PRESENT |

## tau_WEP Readout Contract

| contract_id | object | status | needed_to_promote |
| --- | --- | --- | --- |
| TAU1608_0_definition | tau_WEP | FORMAL_DEFINITION_ONLY | K_CMSM, S_Earth, M_TiPt, N_eta, units/sign convention and source anchors |
| TAU1608_1_amplitude_law | Delta_w_TiPt | EXACT_CONDITIONAL_LAW | strictly positive tau_min with official data or parent nondegeneracy theorem |
| TAU1608_2_null_space_guard | tau_min | NO_SHORTCUT_LEMMA_RETAINED | alignment lower bound c_min or direct nonzero projection computation |
| TAU1608_3_no_unity | tau_eff=1 shortcut | SHORTCUT_FORBIDDEN | real tau calculation or parent theorem |
| TAU1608_4_verdict | tau_WEP lower-bound status | TAU_WEP_NOT_EVALUATED | official input import or parent nondegeneracy theorem |

## Official Input Import Schema

| schema_id | field | required_policy |
| --- | --- | --- |
| OIS1608_0_file_role | file_role | K_CMSM_readout/source_worldtube/material_tensor/normalization/alignment_result/filelist |
| OIS1608_1_source_path_or_url | source_path_or_url | official local path, URL, DOI, or parent theorem path |
| OIS1608_2_checksum_or_theorem_id | checksum_or_theorem_id | sha256/checksum for files or theorem id for exact parent proof |
| OIS1608_3_required_columns | required_columns | time/session/orbit/masks/gx/gz/Sxx/Sxz/material/source/tau fields as role requires |
| OIS1608_4_units | units | declared SI/dimensionless units |
| OIS1608_5_sign_convention | sign_convention | MICROSCOPE axis, TA6V-minus-PtRh10, eta sign and absolute convention |
| OIS1608_6_basis | basis | same MTS parent WEP/source basis |
| OIS1608_7_no_bound_inversion | no_bound_inversion | true for claim-grade import |
| OIS1608_8_no_tau_unity | no_tau_unity | true for claim-grade import |
| OIS1608_9_valid_for_claim | valid_for_claim | false until all gates pass |
| OIS1608_10_claim_allowed | claim_allowed | false until full branch validation passes |

## Official Input Templates

| template_id | file_role | required_columns | parser_status |
| --- | --- | --- | --- |
| TPL1608_0_K_CMSM_readout | K_CMSM_readout | time_s;session_id;orbit_phase;gx;gz;Sxx;Sxz;mask_flag;calibration_flag;axis_sign;units | TEMPLATE_ONLY_NOT_IMPORTABLE |
| TPL1608_1_source_worldtube | source_worldtube | radius_or_depth;density_or_stress_proxy;source_response;orbit_kernel;units;source_anchor | TEMPLATE_ONLY_NOT_IMPORTABLE |
| TPL1608_2_material_tensor | material_tensor | component;sensitivity_value;uncertainty;units;sign_convention;basis;source_anchor | TEMPLATE_ONLY_NOT_IMPORTABLE |
| TPL1608_3_normalization | normalization | N_eta;eta_convention;absolute_or_signed;units;source_anchor | TEMPLATE_ONLY_NOT_IMPORTABLE |
| TPL1608_4_alignment_result | alignment_result | K_norm;V_norm;projection_value;c_min;tau_min;uncertainty;assumptions | TEMPLATE_ONLY_NOT_IMPORTABLE |
| TPL1608_5_filelist | filelist | dataset_id;product_id;file_name;file_role;byte_count;checksum;download_url;licence | TEMPLATE_ONLY_NOT_IMPORTABLE |

## Input Inventory

| inventory_id | file_role | exists | row_count | status |
| --- | --- | --- | --- | --- |
| INV1608_0_K_CMSM_readout | K_CMSM_readout | False | 0 | MISSING_INPUT_FILE |
| INV1608_1_source_worldtube | source_worldtube | False | 0 | MISSING_INPUT_FILE |
| INV1608_2_material_tensor | material_tensor | False | 0 | MISSING_INPUT_FILE |
| INV1608_3_normalization | normalization | False | 0 | MISSING_INPUT_FILE |
| INV1608_4_alignment_result | alignment_result | False | 0 | MISSING_INPUT_FILE |
| INV1608_5_filelist | filelist | False | 0 | MISSING_INPUT_FILE |
| INV1608_6_1607_material_tensor_passthrough | 1607_material_tensor_passthrough | False | 0 | MISSING_INPUT_FILE |

## Material Tensor Passthrough

| passthrough_id | source | status | reason |
| --- | --- | --- | --- |
| MTP1608_0_1607_template | source-intake/microscope/quarantine/1607/input/TiPt_parent_material_response_tensor_TEMPLATE.csv | TEMPLATE_EXISTS_NONIMPORTABLE | 1607 created schema/template only; no live Ti/Pt parent tensor file was supplied |
| MTP1608_1_live_1607_file | source-intake/microscope/quarantine/1607/input/TiPt_parent_material_response_tensor.csv | LIVE_FILE_MISSING | no source-backed material tensor file exists to import into tau_WEP |

## Nondegeneracy Theorem Status

| theorem_id | current_status | missing_input | effect |
| --- | --- | --- | --- |
| NDG1608_0_target | THEOREM_NOT_IN_CORPUS | parent geometry/readout theorem or official alignment computation | tau_min cannot be derived |
| NDG1608_1_symbolic_K_limit | SYMBOLIC_KERNEL_INSUFFICIENT | numeric K_CMSM arrays or parent non-null projection theorem | null-space countermodel survives |
| NDG1608_2_data_theorem_equivalence | OFFICIAL_READOUT_OR_PARENT_ALIGNMENT_REQUIRED | filelist/checksums/arrays/material/source vector or theorem | 1609 should target source-pack capture or nondegeneracy proof |

## tau Lower-Bound Status

| tau_status_id | requirement | ready | blocker |
| --- | --- | --- | --- |
| TLS1608_0_K_CMSM | official readout/design matrix | False | MKS1598_1 and KBI1456_2/3 missing official arrays |
| TLS1608_1_source_worldtube | Earth/source worldtube vector | False | TFA1596_0 and PILOT1457 missing source profile/orbit weighting |
| TLS1608_2_material_tensor | Ti/Pt material tensor | False | 1607 full parent tensor missing |
| TLS1608_3_normalization | eta product normalization N_eta | False | TFA1596_5 normalization not filled |
| TLS1608_4_alignment | c_min or nonzero projection | False | NDI1597_3 MISSING_CRITICAL |
| TLS1608_5_tau_min | strictly positive tau_min | False | no K/source/material/alignment package |
| TLS1608_6_verdict | tau_WEP score-ready | False | official input or parent nondegeneracy missing |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1608_0_tau_import | tau_WEP requires official K_CMSM, source worldtube, material tensor, normalization and alignment in one basis | all live input files missing | TAU_WEP_NOT_EVALUATED | no Delta_w bound or WEP score |
| RUN1608_1_nondegeneracy | parent theorem must exclude K_CMSM null-space countermodel with c_min>0 | no parent nondegeneracy theorem present | REJECT_TAU_MIN_THEOREM | tau lower bound remains missing |
| RUN1608_2_shortcut_firewall | tau_eff=1, bound inversion, surrogate arrays and symbolic K alone cannot score WEP | only symbolic/proxy/workflow rows exist | SHORTCUTS_REJECTED | all local/WEP claims stay blocked |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1608_0_K_CMSM | official readout/design matrix | BLOCKED | no official arrays/filelist/checksums imported |
| CG1608_1_tau_min | positive tau_WEP lower bound | BLOCKED | alignment/nondegeneracy missing |
| CG1608_2_material_tensor | live material tensor import | BLOCKED | 1607 live file missing |
| CG1608_3_bound_conversion | convert product bound to Delta_w bound | BLOCKED | tau_min missing |
| CG1608_4_WEP_score | MICROSCOPE/WEP score | BLOCKED | K/source/material/tau/readout gates open |
| CG1608_5_local_GR | Newton/local-GR source claim | BLOCKED | coupling/material/tau branch unresolved |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1608_0_tau_route | TAU_WEP_IMPORT_CONTRACT_READY_NO_LIVE_INPUTS | schema/templates exist, but official K/source/material/normalization/alignment files are missing | capture/import official CMSM source pack or provide equivalent source-backed files |
| DEC1608_1_theorem_route | PARENT_NONDEGENERACY_NOT_DERIVED | symbolic readout structure does not exclude the null-space countermodel | derive c_min>0 alignment theorem or compute c_min from official data |
| DEC1608_2_next | NEXT_1609_CMSM_SOURCE_PACK_CAPTURE_OR_PARENT_NONDEGENERACY_THEOREM | the next decisive object is either official filelist/checksum/source-pack capture or parent non-null projection proof | build/import CMSM source-pack capture rows, or attempt the parent nondegeneracy theorem directly |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1609-Y5-R2FR-CMSM-source-pack-capture-or-parent-nondegeneracy-theorem.md | scripts/Y5_R2FR_CMSM_source_pack_capture_or_parent_nondegeneracy_theorem.py | capture/import official CMSM source-pack metadata/checksums/readout files, or derive parent nondegeneracy c_min>0 for the WEP readout pairing | source-pack filelist/checksum/readout rows accepted as nonclaim input, or parent theorem excluding the tau_WEP null-space countermodel; no WEP/local-GR claim until all gates pass | do not use tau_eff=1, surrogate arrays, bound inversion, symbolic K alone, closure-only zero, measured-G absorption, or public/local-GR claims |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1608_0_sources_exist | PASS | all cited 1608 local source paths exist |
| VAL1608_1_needles_found | PASS | all required 1608 source needles found |
| VAL1608_2_tau_contract | PASS | tau_WEP contract recorded and not evaluated |
| VAL1608_3_import_schema | PASS | official input import schema written |
| VAL1608_4_templates_nonimportable | PASS | official input templates remain nonimportable |
| VAL1608_5_live_inputs_missing | PASS | all live 1608/1607 input files are missing |
| VAL1608_6_material_passthrough_blocked | PASS | 1607 material tensor live file is missing |
| VAL1608_7_nondegeneracy_missing | PASS | nondegeneracy route remains open |
| VAL1608_8_tau_not_ready | PASS | tau branch remains not score-ready |
| VAL1608_9_runner_rejects_shortcuts | PASS | runner rejects tau/readout shortcuts |
| VAL1608_10_claim_gates_closed | PASS | all 1608 claim gates remain closed |
| VAL1608_11_decision_next | PASS | decision selects 1609 CMSM source-pack or nondegeneracy theorem |
| VAL1608_12_csv_parse | PASS | all generated 1608 CSVs parse |
| VAL1608_13_claim_safety_flags | PASS | no generated 1608 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed |
| VAL1608_14_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1608_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1608_16_formalization_untouched | PASS | no 1608 outputs found under formalization-workbench |
| VAL1608_OVERALL | PASS | 1608 tau_WEP readout kernel or material tensor source-file validation |
