# 2656 - Official MICROSCOPE Readout Data Dry-Run Or Source-Worldtube Residual Bound

## Purpose

This checkpoint tests the fork selected by 2655. It checks whether official MICROSCOPE readout data are locally available or web-visible as machine-readable arrays; if not, it derives the exact residual-bound contract that would make the point-source source-worldtube branch legitimate without smuggling in a shortcut.

## Result

- No official MICROSCOPE CMSM/readout arrays are present in the local drop folder; only helper/template files are present.
- Public web-facing sources found in this pass are papers, mission pages, or press/provenance pages, not machine-readable gx/gz/Sxx/Sxz arrays.
- A useful formal inequality is now staged: the source-worldtube residual must be bounded by parent coupling, source vector/profile, material tensor, readout kernel and tau_WEP factors.
- The inequality is not a claim: C_parent, R_source, R_material, K_CMSM, residual norm bounds and tau_WEP remain missing or unsigned.
- The next target is 2657: parent coupling/source/material contraction zero theorem, or a finite WEP coefficient pack.

## Source Register

| source_id | role | path | exists | needles_required | missing_needles | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2656_2655_doc | immediate handoff selecting readout dry-run/source residual bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2655-Y5-R2FR-WEP-source-worldtube-point-source-reduction-or-official-readout-data-runner.md | True | 4 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |
| SRC2656_1901_doc | measured-G anti-hiding guard and source-vector fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1901-Y5-R2FR-measured-G-common-mode-guard-or-source-vector-fill.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |
| SRC2656_1071_doc | kernel skeleton, SUEP segment table and numeric tau gap | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |
| SRC2656_1075_doc | surrogate design matrix and surrogate-as-official refusal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1075-Y5-R10-surrogate-design-matrix-tau-shape-smoke-runner.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |
| SRC2656_1084_doc | readout import gate and profile weighting gap | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |
| SRC2656_1424_doc | official CMSM import lock and parent-map caveat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1424-Y5-R10-RAB-parent-TiPt-source-vector-map-or-official-CMSM-import-lock.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T03:43:18.251173+00:00 |

## Web Acquisition Probe

| probe_id | source_url | source_label | observed_role | machine_readable_arrays_found | status | claim_use | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WEBP2656_0_arxiv_data_processing | https://arxiv.org/abs/2201.10841 | MICROSCOPE Mission scenario, ground segment and data processing | mission/data-processing paper and CMSM provenance | False | PUBLIC_DOC_SOURCE_ONLY_NOT_ARRAYS | source/provenance ledger only | False | 2026-06-23T03:43:18.254372+00:00 |
| WEBP2656_1_final_results_arxiv | https://arxiv.org/abs/2209.15487 | MICROSCOPE mission final WEP result | final-result/bound provenance | False | BOUND_PROVENANCE_ONLY_NOT_READOUT_ARRAYS | source/provenance ledger only | False | 2026-06-23T03:43:18.254372+00:00 |
| WEBP2656_2_HAL_processing | https://hal.science/hal-03564498/document | HAL mirror of data-processing paper | candidate PDF source; local cached fetch is bot-check HTML | False | PUBLIC_DOC_OR_BOTCHECK_NOT_ARRAY_EXPORT | source/provenance ledger only | False | 2026-06-23T03:43:18.254372+00:00 |
| WEBP2656_3_CNES_project_page | https://cnes.fr/en/projects/microscope | CNES MICROSCOPE project page | mission overview/provenance | False | MISSION_PAGE_NOT_ARRAY_EXPORT | source/provenance ledger only | False | 2026-06-23T03:43:18.254372+00:00 |
| WEBP2656_4_ONERA_press_page | https://onera.fr/en/presse/communiques-presse/final-results-of-microscope-mission-achieve-record-levels-of-precision | ONERA final-results press page | public final-result context | False | PRESS_PAGE_NOT_ARRAY_EXPORT | source/provenance ledger only | False | 2026-06-23T03:43:18.254372+00:00 |

## Local CMSM Drop Inventory

| inventory_id | path | name | extension | size_bytes | file_magic | classification | candidate_official_array | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LCI2656_000 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\README_2001_DROP_CMSM_EXPORTS_HERE.txt | README_2001_DROP_CMSM_EXPORTS_HERE.txt | .txt | 379 | 2001 CMS | HELPER_OR_TEMPLATE_NOT_DATA | False | False | 2026-06-23T03:43:18.249641+00:00 |
| LCI2656_001 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm\TEMPLATE_2001_expected_official_array_schema.csv | TEMPLATE_2001_expected_official_array_schema.csv | .csv | 453 | segment_ | HELPER_OR_TEMPLATE_NOT_DATA | False | False | 2026-06-23T03:43:18.249641+00:00 |

## Official Readout Data Dry-Run

| dryrun_id | object | required_content | current_evidence | current_status | blocks_claim | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ODR2656_0_schema_contract | official MICROSCOPE CMSM/readout export | time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, orbit/attitude convention, units and checksum/manifest | 1424/1084/1071 contracts plus local drop-folder template | SCHEMA_CONTRACT_STAGED | True | False | False |
| ODR2656_1_local_inventory | local CMSM drop folder | at least one candidate official array file with recognized data extension and non-template name | candidate_array_files=0; folder=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | NO_OFFICIAL_ARRAY_CANDIDATES_FOUND | True | False | False |
| ODR2656_2_web_probe | web-facing MICROSCOPE sources | machine-readable arrays or official archive/schema, not only papers/pages | arXiv/HAL/CNES/ONERA sources provide papers/mission context; no machine-readable array export identified in this pass | PUBLIC_DOCS_FOUND_ARRAY_EXPORT_NOT_FOUND | True | False | False |
| ODR2656_3_surrogate_lock | surrogate design matrix | proof of equivalence to official arrays before any physical tau_WEP use | 1075 surrogate matrix exists but is explicitly SURROGATE_ONLY | SURROGATE_AVAILABLE_NONCLAIM_NOT_OFFICIAL | True | False | False |
| ODR2656_4_botcheck_lock | HAL/local cached candidate PDFs | valid PDF/data magic; bot-check HTML cannot be data | 2655/2654 caches include bot-check HTML for HAL candidates | BOTCHECK_HTML_REJECTED_AS_DATA | True | False | False |
| ODR2656_5_verdict | official readout data dry-run | complete array/schema/manifest pack or validated exact reconstruction | local folder has helper/template files only and web probe did not identify an array export | OFFICIAL_MICROSCOPE_READOUT_DRYRUN_BLOCKED_NONCLAIM | True | False | False |

## Source-Worldtube Residual Bound Attempt

| attempt_id | claim_piece | formal_statement | status | derivation_or_gap | source_anchor | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRB2656_0_target | finite source-worldtube residual bound | Replace the point-source shortcut by an inequality bounding eta_res from the difference between the true source/readout worldtube kernel and the calibrated common-mode monopole kernel. | TARGET_SHARP | this is the mathematically honest way to approach local GR/Newton reduction without pretending Earth/source structure vanishes | 2655:PSL2655_6_acceptance;1901:GMG1901_5_verdict | False | False |
| SRB2656_1_operator_decomposition | kernel residual decomposition | Let K_true = K_CM + deltaK_source + deltaK_multipole + deltaK_readout + deltaK_frame. Then \|eta_res\| <= \|\|DeltaR_TiPt\|\| \|\|C_parent\|\| \|\|R_source\|\| \|\|deltaK_total\|\| plus declared tau_WEP normalization error. | FORMAL_INEQUALITY_DERIVED | triangle inequality and operator norm bookkeeping are valid, but every norm must be parent/data sourced before scoring | 1424:SRCMAP1424_0_R_source through SRCMAP1424_4_calibration_guard;1071:KER1071_6_verdict | False | False |
| SRB2656_2_common_mode_limit | Newton/GR common-mode limit | If C_parent has no relative matter/source component and deltaK_total is universal/common-mode, the residual contributes no differential WEP signal after the measured-G guard. | EXACT_CONDITIONAL_ZERO | this is a clean GR-like reduction condition; MTS still lacks parent-signed no relative component/source-label forgetting | 1901:GMG1901_1_algebraic_absorption;1450 common-mode guard | False | False |
| SRB2656_3_shell_point_source_warning | spherical/point-source shortcut limit | A shell/Gauss point-source theorem is exact only for the universal exterior monopole; non-spherical, profile-weighted or composition-relative source charges must be bounded, not erased. | POINT_SOURCE_SHORTCUT_REJECTED_FOR_RELATIVE_CHANNELS | MICROSCOPE altitude is not a magic small-parameter proof; source composition, multipoles, masks and readout frame still matter | 2655:PSR2655_3_source_composition_profile;1071:EXT1071_7_suep_segment_table | False | False |
| SRB2656_4_bound_target | WEP tolerance target | \|eta_res\| must be below the MICROSCOPE Ti/Pt bound envelope only after the residual product is expressed in dimensionless eta units with source, material, parent coupling, readout and tau_WEP factors. | BOUND_TARGET_DECLARED_NOT_NUMERIC | the 2.8e-15 bound is a target; it is not a prediction and cannot close missing C_parent/R_source/R_material/K_CMSM/tau_WEP | 1080:BOUND1080_0_MICROSCOPE_WEP_source_charge;2655:ODT2655_0_bound_pdf | False | False |
| SRB2656_5_verdict | source-worldtube residual bound closes point-source branch | Current MTS corpus supplies a numeric or theorem-zero finite source-worldtube residual bound strong enough to legalize the point-source WEP branch. | SOURCE_WORLDTUBE_RESIDUAL_BOUND_NOT_NUMERICALLY_CLOSED | the operator inequality is useful, but C_parent, source vector/profile, material tensor, K_CMSM, tau_WEP and numeric residual norms remain missing or nonclaim | SRB2656_0_target through SRB2656_4_bound_target | False | False |

## Residual Bound Input Contract

| input_id | input | required_form | current_artifact | current_status | units | blocks_claim | score_ready | valid_prediction_row | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIC2656_0_eta_bound | MICROSCOPE Ti/Pt eta bound | dimensionless bound/provenance only | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\wep-sources\1899\MICROSCOPE_final_results_arxiv_2209_15487.pdf | SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY | dimensionless eta | True | False | False | False |
| BIC2656_1_C_parent | parent coupling/operator coefficient | parent-owned C_parent or theorem-zero relative coupling | MISSING | MISSING_PARENT_COUPLING_OWNER | declared parent/source units | True | False | False | False |
| BIC2656_2_R_source | Earth/source vector and profile | profile/worldtube-weighted source vector in same parent basis, or common-mode zero theorem | MISSING | MISSING_SOURCE_PROFILE_WEIGHTING | dimensionless source vector or normalized kernel | True | False | False | False |
| BIC2656_3_R_material | TA6V-PtRh10 material response tensor | full material response tensor to parent residual basis | MISSING | MISSING_FULL_MATERIAL_TENSOR | dimensionless sensitivities per basis component | True | False | False | False |
| BIC2656_4_K_CMSM | official MICROSCOPE readout kernel | official arrays or validated exact reconstruction with masks/orbit/attitude/units | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope_cmsm | OFFICIAL_ARRAYS_NOT_IMPORTED | time, m s^-2, s^-2 and dimensionless kernel columns | True | False | False | False |
| BIC2656_5_deltaK_norms | finite source/readout residual norms | numeric operator norm bounds for source profile, multipoles, readout frame and masks | MISSING | MISSING_RESIDUAL_NORM_BOUNDS | dimensionless eta contribution or declared kernel norm | True | False | False | False |
| BIC2656_6_tau_WEP | tau_WEP projection/contraction normalization | derived/sourced tau_WEP or retained nuisance prior; tau=1 shortcut forbidden | MISSING | TAU_WEP_PROJECTION_NOT_DERIVED | dimensionless | True | False | False | False |
| BIC2656_7_acceptance | source-worldtube residual bound product | all factors sourced/zeroed and no-cancellation absolute envelope below eta bound | NONCLAIM_CONTRACT_ONLY | RESIDUAL_BOUND_PRODUCT_NOT_EXECUTABLE | dimensionless eta envelope | True | False | False | False |

## Dry-Run Cases

| case_id | official_arrays | template_only | surrogate_as_official | botcheck_as_data | bound_inequality_only | c_parent | source_vector | material_tensor | tau_wep_unity | uses_cancellation | expected_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2656_0_no_official_arrays | False | False | False | False | False | False | False | False | False | False | REFUSED_OFFICIAL_ARRAYS_MISSING | False |
| DRY2656_1_template_only | False | True | False | False | False | False | False | False | False | False | REFUSED_TEMPLATE_ONLY_NOT_DATA | False |
| DRY2656_2_surrogate | False | False | True | False | False | False | False | False | False | False | REFUSED_SURROGATE_AS_OFFICIAL | False |
| DRY2656_3_botcheck | True | False | False | True | False | False | False | False | False | False | REFUSED_BOTCHECK_HTML_AS_DATA | False |
| DRY2656_4_inequality_only | True | False | False | False | True | False | False | False | False | False | REFUSED_INEQUALITY_ONLY_MISSING_NUMERIC_FACTORS | False |
| DRY2656_5_parent_coupling | True | False | False | False | False | False | True | True | False | False | REFUSED_PARENT_COUPLING_OWNER_MISSING | False |
| DRY2656_6_source_vector | True | False | False | False | False | True | False | True | False | False | REFUSED_SOURCE_VECTOR_MISSING | False |
| DRY2656_7_material_tensor | True | False | False | False | False | True | True | False | False | False | REFUSED_MATERIAL_TENSOR_MISSING | False |
| DRY2656_8_tau_unity | True | False | False | False | False | True | True | True | True | False | REFUSED_TAU_WEP_UNITY_SHORTCUT | False |
| DRY2656_9_cancellation | True | False | False | False | False | True | True | True | False | True | REFUSED_CANCELLATION_ONLY | False |
| DRY2656_10_counterfactual | True | False | False | False | False | True | True | True | False | False | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | False |

## Dry-Run Results

| case_id | computed_status | expected_status | status_match | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| DRY2656_0_no_official_arrays | REFUSED_OFFICIAL_ARRAYS_MISSING | REFUSED_OFFICIAL_ARRAYS_MISSING | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_1_template_only | REFUSED_TEMPLATE_ONLY_NOT_DATA | REFUSED_TEMPLATE_ONLY_NOT_DATA | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_2_surrogate | REFUSED_SURROGATE_AS_OFFICIAL | REFUSED_SURROGATE_AS_OFFICIAL | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_3_botcheck | REFUSED_BOTCHECK_HTML_AS_DATA | REFUSED_BOTCHECK_HTML_AS_DATA | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_4_inequality_only | REFUSED_INEQUALITY_ONLY_MISSING_NUMERIC_FACTORS | REFUSED_INEQUALITY_ONLY_MISSING_NUMERIC_FACTORS | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_5_parent_coupling | REFUSED_PARENT_COUPLING_OWNER_MISSING | REFUSED_PARENT_COUPLING_OWNER_MISSING | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_6_source_vector | REFUSED_SOURCE_VECTOR_MISSING | REFUSED_SOURCE_VECTOR_MISSING | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_7_material_tensor | REFUSED_MATERIAL_TENSOR_MISSING | REFUSED_MATERIAL_TENSOR_MISSING | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_8_tau_unity | REFUSED_TAU_WEP_UNITY_SHORTCUT | REFUSED_TAU_WEP_UNITY_SHORTCUT | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_9_cancellation | REFUSED_CANCELLATION_ONLY | REFUSED_CANCELLATION_ONLY | True | False | False | 2026-06-23T03:43:18.251150+00:00 |
| DRY2656_10_counterfactual | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM | True | False | False | 2026-06-23T03:43:18.251150+00:00 |

## Claim Gates

| gate_id | condition | current_status | source_anchor | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG2656_0_official_arrays | official MICROSCOPE readout arrays are locally available and schema-validated | FAIL_OFFICIAL_ARRAYS_NOT_IMPORTED | P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_OFFICIAL_READOUT_DATA_DRYRUN.csv:ODR2656_5_verdict | False | False |
| CG2656_1_residual_bound | source-worldtube residual inequality has numeric/theorem-zero factors | FAIL_SOURCE_WORLDTUBE_RESIDUAL_BOUND_NOT_NUMERICALLY_CLOSED | P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_WORLDTUBE_RESIDUAL_BOUND_ATTEMPT.csv:SRB2656_5_verdict | False | False |
| CG2656_2_bound_inputs | C_parent, source vector, material tensor, K_CMSM, deltaK norms and tau_WEP are filled or theorem-zero | FAIL_RESIDUAL_BOUND_PRODUCT_NOT_EXECUTABLE | P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_RESIDUAL_BOUND_INPUT_CONTRACT.csv:BIC2656_7_acceptance | False | False |
| CG2656_3_no_shortcuts | template-only, surrogate, bot-check, inequality-only, tau=1 and cancellation shortcuts are refused | PASS_GUARDS_ENFORCED_BUT_NONCLAIM | P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_READOUT_BOUND_DRYRUN_RESULTS.csv | False | False |
| CG2656_4_verdict | WEP source-worldtube residual branch can support local-GR/WEP claim | CLAIM_BLOCKED | CG2656_0_official_arrays through CG2656_3_no_shortcuts | False | False |

## Decision Ledger

| decision_id | decision | reason | status | next_dependency | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2656_0_data | DO_NOT_RUN_OFFICIAL_READOUT_SCORE | local CMSM drop folder has helper/template files only; web-facing public sources found in this pass are documents/pages, not machine-readable arrays | OFFICIAL_DATA_ROUTE_BLOCKED_NONCLAIM | user-supplied official CMSM export or independently validated reconstruction | False |
| DEC2656_1_bound | KEEP_SOURCE_RESIDUAL_BOUND_AS_FORMAL_CONTRACT | the operator-norm inequality is valid as a contract, but no numeric residual envelope exists without C_parent/source/material/K_CMSM/tau inputs | RESIDUAL_BOUND_CONTRACT_STAGED_NONCLAIM | parent coupling/material/source contraction theorem or source-backed coefficient pack | False |
| DEC2656_2_next | SELECT_2657_PARENT_COUPLING_SOURCE_CONTRACTION_THEOREM | official data cannot create a prediction; the leap forward is to derive or bound the parent coupling/source/material contraction that would make any readout meaningful | NEXT_TARGET_SELECTED | 2657 parent coupling/source contraction zero theorem or finite coefficient pack | False |

## Next Target

| branch_id | next_id | status | next_doc | next_script | target | must_include | must_exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | NEXT2656_0_selected | selected | 2657-Y5-R2FR-parent-coupling-source-material-contraction-zero-or-finite-WEP-coefficient-pack.md | scripts/Y5_R2FR_parent_coupling_source_material_contraction_zero_or_finite_WEP_coefficient_pack_2657.py | Try to derive the parent coupling/source/material contraction zero theorem that would make WEP local-GR reduction legal; if it fails, stage finite WEP coefficient rows with explicit units and no claim. | C_parent owner; source vector/profile; material tensor; K_CMSM side gate; tau_WEP dependency; no measured-G hiding; no cancellation; finite coefficient pack if theorem fails | GitHub action, formalization-workbench edits, official arrays as parent ontology, tau_WEP=1, bound-only WEP claim, surrogate readout as evidence | False | False |

## Project Status Snapshot

| status_id | area | summary | risk_level | project_meaning | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| STAT2656_0_data | MICROSCOPE official readout | the local drop folder contains only helper/template files, and public web sources found are documents rather than array exports | DATA_ROUTE_BLOCKED_UNTIL_EXPORT | we cannot accidentally score the WEP branch from fake arrays or a paper PDF | wait for official export or validated reconstruction; keep deriving meanwhile | False |
| STAT2656_1_theory | source-worldtube residual bound | a real operator-norm contract is now staged: eta_res is bounded by parent coupling, source, material, readout and tau factors | FORMAL_CONTRACT_PROGRESS_INPUTS_MISSING | this turns the point-source argument from handwave into an auditable theorem target | derive the parent coupling/source/material contraction theorem | False |
| STAT2656_2_project_overview | GR/Newton reduction bridge | the branch has moved away from data-polishing and back to the right derivation choke point: parent coupling/source/material contraction | GOOD_HARD_PROBLEM | the path is still alive, but the next win must be a theorem or a finite coefficient pack, not another surrogate run | 2657 parent coupling contraction zero or finite WEP coefficient pack | False |

## Branch Copies

| copy_id | path | exists | parseable_csv | purpose | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2656_MICROSCOPE_READOUT_BOUND_INPUT_CONTRACT_NONCLAIM.csv | True | True | 2656 official readout/source residual bound nonclaim handoff | False |
| local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\WEP_source_worldtube_residual_bound_2656_NONCLAIM.csv | True | True | 2656 official readout/source residual bound nonclaim handoff | False |
| source_weight | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\WEP_SOURCE_RESIDUAL_BOUND_2656_NONCLAIM.csv | True | True | 2656 official readout/source residual bound nonclaim handoff | False |
| microscope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_2656_MICROSCOPE_READOUT_DRYRUN.csv | True | True | 2656 official readout/source residual bound nonclaim handoff | False |
| quarantine | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\2656\P8_Y5_2656_READOUT_BOUND_DRYRUN_RESULTS.csv | True | True | 2656 official readout/source residual bound nonclaim handoff | False |

## Validation

| timestamp_utc | checkpoint | branch_id | valid_for_claim | claim_allowed | validation_id | status | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_00_sources | PASS | all cited source paths exist and required needles are present |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_01_web_probe | PASS | web probe rows record public docs/pages only, not array exports |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_02_local_inventory | PASS | local CMSM drop folder has no candidate official array files |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_03_official_dryrun | PASS | official readout dry-run remains blocked/nonclaim |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_04_residual_bound | PASS | source-worldtube residual inequality is staged but not numerically closed |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_05_bound_inputs | PASS | residual-bound input contract is nonclaim/not score-ready |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_06_dryrun | PASS | dry-run refuses missing arrays, template-only, surrogate, bot-check, inequality-only, missing factors, tau=1 and cancellation |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_07_claim_gates_false | PASS | claim remains blocked |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_08_next_target | PASS | 2657 parent coupling/source/material contraction target is recorded |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_09_branch_copies | PASS | branch copies exist and parse |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_10_csv_parse | PASS | all generated CSVs parse cleanly |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_11_formalization_untouched | PASS | no 2656 outputs are written under formalization-workbench |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_12_pycache_absent | PASS | scripts __pycache__ absent |
| 2026-06-23T03:43:19.504541+00:00 | 2656 | Y5_R2FR_MICROSCOPE_READOUT_DRYRUN_OR_SOURCE_RESIDUAL_BOUND_2656 | False | False | VAL2656_OVERALL | PASS | 2656 blocks official-data scoring, stages source-worldtube residual bound contract, and selects parent coupling/source/material contraction next |
