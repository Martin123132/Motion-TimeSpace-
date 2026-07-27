# 1483 - MICROSCOPE Source-File Acquisition Ledger Or Symbolic Tau Functional Lock

## Verdict
- No official MICROSCOPE arrays were imported into live claim files; the ONERA/CMSM/REGARDS routes are recorded as acquisition targets only.
- The useful advance is the tau lock: `tau_eff_X` is now an explicit symbolic functional of readout, source, masks, orbit weights, sign convention, and branch id.
- This keeps the local-GR/WEP branch honest: future data can fill values, but `tau_eff=1`, bound inversion, DD-only basis, and mixed-branch shortcuts stay forbidden.

## Acquisition Ledger
| acquisition_id | source_kind | current_status | next_action |
|---|---|---|---|
| ACQ1483_0_ONERA_data_page | official announcement page | PORTAL_POINTER_ONLY | open portal and capture official package/filelist/checksum metadata before import |
| ACQ1483_1_ONERA_english_node | official announcement page | PORTAL_POINTER_ONLY | prefer portal filelist over hand-entered URLs |
| ACQ1483_2_CMSM_portal | official data portal | BROWSER_PORTAL_NEEDED_NO_LOCAL_ARRAYS | capture package id, module id, filenames, checksums, license, and schema |
| ACQ1483_3_REGARDS_CNES_route | official data portal | BROWSER_PORTAL_NEEDED_NO_LOCAL_ARRAYS | capture official package metadata; do not infer package identities |
| ACQ1483_4_CQG_analysis | primary analysis paper | SCHEMA_ANCHOR_ONLY | use for required columns and model semantics, not as machine-array source |
| ACQ1483_5_PRL_result | primary result paper | BOUND_PROVENANCE_ONLY | use as bound/provenance; forbid bound-inversion into C_parent |
| ACQ1483_6_OCA_context | institutional mission page | PORTAL_CONTEXT_ONLY | use as route corroboration; still require official portal filelist |

## Package Checklist
| check_id | required_item | current_status | why_required |
|---|---|---|---|
| PKG1483_0_package_id | official package id / module id | MISSING | required before any download is treated as official |
| PKG1483_1_filelist | portal file list with filenames and product categories | MISSING | needed to distinguish raw/calibrated/aux/orbit products |
| PKG1483_2_checksums | checksums or reproducible hash manifest | MISSING | guards against silent file mutation |
| PKG1483_3_license_access | license/access terms and citation requirement | MISSING | needed for source provenance |
| PKG1483_4_data_dictionary | official data dictionary/schema | MISSING | needed before parser can read arrays |
| PKG1483_5_readout_arrays | accelerometer/readout arrays with timestamps and masks | MISSING_LIVE_FILE | needed for K_CMSM |
| PKG1483_6_attitude_orbit | attitude, angular velocity/acceleration, orbit position/velocity | MISSING_LIVE_FILE | needed for projection and orbit average |
| PKG1483_7_session_masks | science session, calibration, glitch/onboard masks | MISSING_LIVE_FILE | needed for final-analysis weighting |
| PKG1483_8_source_worldtube | Earth/source profile or source projection model | MISSING_LIVE_FILE | needed for R_source |
| PKG1483_9_units_axes | axis orientation, units, sign/body-order convention | PARTIAL_PENDING | needed to lock tau sign and compare to eta |
| PKG1483_10_branch_lock | same-parent-branch id across all inputs | GUARD_ONLY_NONCLAIM | prevents mixed-basis claims |
| PKG1483_11_C_parent | theorem-zero or sourced finite parent coefficient | MISSING_LIVE_FILE | needed for a real MTS prediction |
| PKG1483_12_material_tensor | full TA6V-minus-PtRh10 parent-basis material tensor | MISSING_LIVE_FILE | needed for R_material |

## Tau Functional Lock
| lock_id | symbol | current_status | missing_for_evaluation | numeric_value |
|---|---|---|---|---|
| TAULOCK1483_0_domain | domain | MISSING_LIVE_READOUT_MATRIX | none | NOT_EVALUATED |
| TAULOCK1483_1_readout_kernel | K_CMSM^a | MISSING_LIVE_READOUT_MATRIX | official readout/design matrix | NOT_EVALUATED |
| TAULOCK1483_2_source_kernel | R_source_a^X | MISSING_SOURCE_WORLDTUBE | source profile/orbit shell weighting | NOT_EVALUATED |
| TAULOCK1483_3_mask_weight | W(t,s) | MISSING_MASK_AND_WEIGHT_RULE | official data dictionary | NOT_EVALUATED |
| TAULOCK1483_4_product_convention | eta/order/sign | PARTIAL_PENDING_NONCLAIM | official convention row without pending fields | NOT_EVALUATED |
| TAULOCK1483_5_branch_lock | branch_id | GUARD_EXISTS_NONCLAIM | parent-owned branch proof | NOT_EVALUATED |
| TAULOCK1483_6_output | tau_eff_X | SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT | all above inputs | NOT_EVALUATED |
| TAULOCK1483_7_forbidden_shortcuts | refusal rule | ACTIVE_REFUSAL_RULE | none; this is locked now | NOT_EVALUATED |

## Tau Input Schema
| schema_id | column | type | requirement |
|---|---|---|---|
| TAUSCHEMA1483_0 | same_parent_branch_id | string | must equal active branch id |
| TAUSCHEMA1483_1 | session_id | string | official MICROSCOPE session/segment id |
| TAUSCHEMA1483_2 | time_s_or_phase | number/string | seconds with epoch or orbit phase key |
| TAUSCHEMA1483_3 | accepted_mask | boolean/int | official analysis mask after cuts |
| TAUSCHEMA1483_4 | axis | string | sensitive X axis or declared transformed axis |
| TAUSCHEMA1483_5 | K_CMSM_component | string | readout/source component label |
| TAUSCHEMA1483_6 | K_CMSM_value | number | readout kernel value |
| TAUSCHEMA1483_7 | K_CMSM_units | string | units/convention for readout kernel |
| TAUSCHEMA1483_8 | R_source_component | string | source basis component label |
| TAUSCHEMA1483_9 | R_source_value | number | source worldtube/projection value |
| TAUSCHEMA1483_10 | R_source_units | string | units/convention for source component |
| TAUSCHEMA1483_11 | orbit_weight | number | weight in accepted average |
| TAUSCHEMA1483_12 | product_sign | number/string | declared sign/body-order convention |
| TAUSCHEMA1483_13 | source_url_or_path | string | official file/source path |
| TAUSCHEMA1483_14 | checksum_or_package_id | string | provenance identifier |

## Parser Refresh
| parser_id | target_exists | parser_status | refusal_reason |
|---|---|---|---|
| PARSE1483_0_live_readout | False | REFUSED_TARGET_ABSENT | required live target does not exist |
| PARSE1483_1_readout_requirements | True | REFUSED_PENDING_OR_NONCLAIM_FIELDS | target exists but contains pending/missing/nonclaim markers or false claim flags |
| PARSE1483_2_source_worldtube | False | REFUSED_TARGET_ABSENT | required live target does not exist |
| PARSE1483_3_product_convention | True | REFUSED_PENDING_OR_NONCLAIM_FIELDS | target exists but contains pending/missing/nonclaim markers or false claim flags |
| PARSE1483_4_branch_guard | True | REFUSED_PENDING_OR_NONCLAIM_FIELDS | target exists but contains pending/missing/nonclaim markers or false claim flags |
| PARSE1483_5_C_parent_import | False | REFUSED_TARGET_ABSENT | required live target does not exist |
| PARSE1483_6_material_tensor | False | REFUSED_TARGET_ABSENT | required live target does not exist |

## C Parent Interaction Points
| interaction_id | current_status | why_it_matters |
|---|---|---|
| CPI1483_0_factorization | MISSING_C_PARENT_IMPORT | tau lock supplies only tau_eff_X; it does not determine C_parent_X |
| CPI1483_1_no_bound_inversion | ACTIVE_REFUSAL_RULE | prevents circular fit-as-prediction |
| CPI1483_2_zero_certificate | NOT_PROVEN | closure preference remains invalid |
| CPI1483_3_finite_import | MISSING_IMPORT_ROW | keeps finite residual route honest |
| CPI1483_4_tau_dependency | TAU_SYMBOLIC_ONLY | blocks WEP score even if C_parent is later found |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
|---|---|---|
| REJ1483_0_no_source_file_import | OFFICIAL_PACKAGE_NOT_IMPORTED | no official portal package/filelist/checksum was imported |
| REJ1483_1_readout_absent | MISSING_LIVE_READOUT_MATRIX | K_CMSM target file remains absent |
| REJ1483_2_source_absent | MISSING_SOURCE_WORLDTUBE | R_source target file remains absent |
| REJ1483_3_tau_symbolic | TAU_EFF_SYMBOLIC_ONLY | tau functional is locked but not evaluated |
| REJ1483_4_product_pending | PENDING_PRODUCT_SIGN_UNITS_ORBIT | product convention still carries pending fields |
| REJ1483_5_C_parent_absent | MISSING_C_PARENT_IMPORT | parent coefficient/theorem-zero import remains absent |
| REJ1483_6_material_absent | MISSING_FULL_PARENT_MATERIAL_TENSOR | full material tensor remains absent |
| REJ1483_7_no_local_claim | CLAIM_PROMOTION_FORBIDDEN | no WEP/local-GR/Newton claim can be promoted |

## No-Claim Gates
| gate_id | gate_pass | detail |
|---|---|---|
| GATE1483_0_source_routes_recorded | True | ONERA/CMSM/REGARDS/CQG/PRL/OCA source routes are recorded |
| GATE1483_1_no_import | True | no live readout/source file was fabricated |
| GATE1483_2_tau_locked | True | symbolic tau functional and required columns are explicit |
| GATE1483_3_tau_not_evaluated | True | all tau rows keep numeric_value=NOT_EVALUATED |
| GATE1483_4_parser_refuses_score | True | parser refresh keeps score_permission=false |
| GATE1483_5_C_parent_independent | True | C_parent remains independent and missing |
| GATE1483_6_claim_flags_false | True | all generated claim flags remain false |

## Decision Ledger
- `DEC1483_0_do_not_download_blind`: do not pull anonymous portal/browser payloads into live claim files - source acquisition remains ledger-only.
- `DEC1483_1_lock_tau_contract`: lock tau_eff as a symbolic functional rather than a unit-kernel shortcut - tau_eff=1 remains forbidden.
- `DEC1483_2_keep_C_parent_separate`: keep C_parent as the coupling bottleneck, not a data-derived fit - next derivation must still attack the coupling slot.
- `DEC1483_3_next_target`: next step should build a parent-basis material/source/tau product interface - 1484 should define the branch-locked product interface and refusal tests.

## Validation
| check_id | result | detail |
|---|---|---|
| VAL1483_0_sources | PASS | all cited local source paths exist |
| VAL1483_1_acquisition_routes | PASS | official source routes recorded without importing unsourced arrays |
| VAL1483_2_package_checklist_blocked | PASS | official package checklist remains nonclaim |
| VAL1483_3_tau_symbolic | PASS | tau functional locked but not evaluated |
| VAL1483_4_tau_schema | PASS | tau input schema locked with values missing |
| VAL1483_5_parser_refuses | PASS | parser refresh refuses score paths |
| VAL1483_6_C_parent_separate | PASS | C_parent interaction points remain independent/nonclaim |
| VAL1483_7_rejection_blocks | PASS | rejection ledger blocks claim |
| VAL1483_8_gates | PASS | no-claim gates pass |
| VAL1483_9_decisions | PASS | decision ledger keeps claim false |
| VAL1483_10_next_target | PASS | 1484 handoff written |
| VAL1483_11_csv_parse | PASS | all generated 1483 CSVs parse cleanly |
| VAL1483_12_branch_copies | PASS | branch/quarantine copies written |
| VAL1483_13_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1483_14_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1483_15_claim_flags_false | PASS | all prediction/claim flags remain false |
| VAL1483_16_overall | PASS | 1483 records official acquisition routes and locks symbolic tau_eff without opening a claim |

## Next Target
| next_id | next_target | script | objective |
|---|---|---|---|
| NEXT1483_0_1484 | 1484-Y5-R10-RAB-branch-locked-WEP-product-interface-or-C-parent-coupling-derivation.md | scripts/Y5_R10_RAB_branch_locked_WEP_product_interface_or_C_parent_coupling_derivation.py | define the complete branch-locked WEP product interface connecting C_parent, R_material, R_source, and tau_eff; then try again to derive or theorem-zero the C_parent coupling slot |
