# 2512 — Tau-WEP Lower Bound or Parent Nondegeneracy Proof

**Current verdict:** `tau_WEP` is not derivable as a number from the current corpus. What is derivable is the exact conditional nondegeneracy theorem: if the MICROSCOPE readout kernel and Ti/Pt source-material vector have a positive alignment floor, then `|tau_WEP| >= tau_min > 0` and the `2511` product bound converts into a `Delta_w_TiPt` width.

**Hard blocker:** nonzero source and material factors do not imply nonzero `tau_WEP`; the source/material vector can live in `ker(K_CMSM)`. Therefore `tau_WEP=1` and generic nonzero assumptions are forbidden.

**Strategic pivot:** the WEP tau route is now cleanly caged and data/theorem-gated. For the GR/Newton bridge, the next theory-first target is the PPN source-weight response kernel in a fixed measured-GM convention.

## Source Register
| source_id | source_path | path_exists | found_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2512_0_2511_tau_target | 2511-Y5-R2FR-first-source-weight-input-row-WEP-product-or-PPN-source-kernel.md | True | NEXT2511_0_selected;WPROD2511_3_amplitude_inversion | True | authoritative target: tau lower bound or parent nondegeneracy proof |
| SRC2512_1_tau_contract_1608 | source-intake/microscope/quarantine/1608/TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv | True | TAU1608_1_amplitude_law;TAU1608_2_null_space_guard | True | existing tau definition, amplitude inversion, and null-space guard |
| SRC2512_2_export_contract_2121 | source-intake/source-weight/docs/AFRAME_CMSM_EXPORT_2121_NONCLAIM.csv | True | CMSM2121_6_tau_min;IMP2121_2_tau | True | live MICROSCOPE artifact gate and tau-min export contract |
| SRC2512_3_drop_request_1704 | source-intake/microscope/branch_locked_wep/source/MICROSCOPE_WEP_data_request_update_1704.md | True | P_WEP_tau_min_lower_bound.csv;Non-Claim Guardrail | True | exact requested live artifacts and nonclaim rule |
| SRC2512_4_public_probe_1705 | source-intake/microscope/branch_locked_wep/source/MICROSCOPE_public_source_probe_1705.md | True | Current Blocker;P_WEP_K_CMSM_readout.csv | True | records public-source probe blocker for live readout arrays |
| SRC2512_5_nondeg_contract_1990 | source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1990_TAU_NONDEGENERACY_CONTRACT_NONCLAIM.csv | True | WEP1990_0_tau_min_certificate_slot;MISSING_NONDEGENERACY_CERTIFICATE | True | old tau-min certificate slot remains unsigned |
| SRC2512_6_tau_pack_1996 | source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1996_TAU_WEP_PROJECTION_PACK_NONCLAIM.csv | True | WEP1996_0_tau_pack_contract;MISSING_DIRECT_PRODUCT_AND_MISSING_TAU_PACK | True | tau WEP projection pack requirement |
| SRC2512_7_readout_provenance_1997 | source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1997_MICROSCOPE_READOUT_PROVENANCE_NONCLAIM.csv | True | WEP1997_0_readout_anchor;READOUT_BOUND_ANCHOR_ONLY | True | MICROSCOPE readout provenance is currently a bound anchor only |
| SRC2512_8_fallback_pack_1749 | source-intake/microscope/branch_locked_wep/residuals/R2FR_1749_TAU_MIN_FALLBACK_SOURCE_PACK.csv | True | TFB1749_4_tau_min;SOURCE_OR_DERIVATION_NEEDED | True | tau-min fallback artifact pack |
| SRC2512_9_source_readout_kernel_2118 | source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_KERNELS_NONCLAIM.csv | True | KSR2118_1_orbit_WEP_kernel;OFFICIAL_FORM_SKELETON_NUMERIC_INPUTS_MISSING | True | source/readout WEP kernel skeleton and missing numeric inputs |
| SRC2512_10_source_owner_2122 | source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_STATUS_NONCLAIM.csv | True | SRO2122_6_verdict;COM2122_2_countermodel | True | conditional source/readout owner theorem and surviving countermodel |

## Tau Nondegeneracy Proof Attempt
| proof_id | target | claim_shape | formal_status | missing_clause | verdict |
| --- | --- | --- | --- | --- | --- |
| TAUP2512_0_definition | tau_WEP | tau_WEP := N_eta^-1 <K_CMSM, S_Earth x M_TiPt> in one branch-locked linear readout convention | DEFINITION_LOCKED_CONDITIONAL | K_CMSM, source worldtube, material tensor, eta normalization, and branch lock are not live | NOT_NUMERIC |
| TAUP2512_1_nondegeneracy_theorem | tau_min | If \|N_eta\| is finite positive, \|\|K_CMSM\|\|>0, \|\|V_TiPt\|\|>0, and dist(V_TiPt,ker K_CMSM)>=c_min\|\|V_TiPt\|\| with c_min>0, then \|tau_WEP\|>=tau_min>0 | EXACT_CONDITIONAL_THEOREM | c_min/alignment floor or direct projection computation is missing | NOT_PROMOTED |
| TAUP2512_2_nullspace_countermodel | tau_min | Nonzero source and material vectors do not imply tau_WEP nonzero because V_TiPt can lie in ker(K_CMSM) | COUNTERMODEL_ACTIVE | need official readout alignment or parent theorem excluding kernel alignment | BLOCKS_SHORTCUT |
| TAUP2512_3_parent_geometry_limit | parent nondegeneracy proof | q/e_obs descent can prove vertical silence of readout variation, but it does not by itself prove a positive experimental projection amplitude | DERIVATION_LIMIT_IDENTIFIED | external protocol/readout normalization or a separate nondegeneracy axiom/theorem is needed | PARENT_ZERO_ROUTE_NOT_ENOUGH_FOR_TAU_MIN |
| TAUP2512_4_tau_zero_meaning | tau_WEP=0 | tau_WEP=0 would mean WEP blindness of this projection, not source-weight safety in PPN/R10/clock/orbit | ARENA_LIMIT | PPN/R10/clock/orbital kernels remain separate | NO_LOCAL_GR_INFERENCE |
| TAUP2512_5_verdict | tau_WEP lower bound | derive tau_min>0 from parent geometry or live source-backed readout data | CONDITIONAL_THEOREM_WRITTEN_BUT_UNSIGNED | MISSING_NONDEGENERACY_CERTIFICATE_OR_LIVE_ARTIFACTS | TAU_MIN_NOT_DERIVED_ACQUISITION_GATE_ACTIVE |

## Tau-Min Certificate Contract
| certificate_id | quantity | required_value | units | accepted_routes | required_evidence | current_status |
| --- | --- | --- | --- | --- | --- | --- |
| CERT2512_0_tau_min | tau_min | positive finite numeric lower bound | dimensionless | official data computation; parent nondegeneracy theorem | tau_min>0; sign_or_abs_convention; confidence; derivation_or_source_path; assumptions | MISSING_TAU_MIN |
| CERT2512_1_branch_lock | same_parent_branch_id | one branch shared by readout, source, material, C_parent, eta convention, bound | identifier | manifest hash lock | all artifacts declare identical branch id and hashes | MISSING_LIVE_BRANCH_LOCK |
| CERT2512_2_no_shortcut | tau_WEP normalization | not set to 1 or assumed nonzero | policy | derived normalization; direct computation | explicit no-unity assertion and source-backed normalization | NO_UNITY_SHORTCUT_ENFORCED |
| CERT2512_3_nullspace | alignment floor c_min | dist(V_TiPt,ker K_CMSM)>=c_min\|\|V_TiPt\|\| | dimensionless | linear algebra computation from live arrays; parent theorem excluding kernel alignment | K_CMSM matrix, V_TiPt vector, norm convention, c_min>0 | MISSING_ALIGNMENT_FLOOR |
| CERT2512_4_width_conversion | Delta_w_TiPt width | abs(Delta_w_TiPt)<=2.8e-15/tau_min | dimensionless | only after CERT2512_0 through CERT2512_3 pass | WEP product bound plus tau_min certificate | BLOCKED_UNTIL_TAU_MIN |

## Live Artifact Gate
| artifact_id | filename | role | live_exists | current_status | import_ready |
| --- | --- | --- | --- | --- | --- |
| LIVE2512_0_readout | P_WEP_K_CMSM_readout.csv | official CMSM readout/design matrix | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_1_source | P_WEP_R_source_Earth_worldtube.csv | Earth source worldtube/source weighting | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_2_material | P_WEP_TiPt_material_response_tensor.csv | TA6V/PtRh10 material response tensor | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_3_eta | P_WEP_eta_product_convention.csv | eta convention and normalization | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_4_branch_lock | P_WEP_same_parent_branch_lock.csv | same-parent branch guard | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_5_parent | P_WEP_C_parent_or_zero_certificate.csv | finite parent coefficient or parent-signed zero certificate | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_6_tau_min | P_WEP_tau_min_lower_bound.csv | strict positive tau lower bound | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_7_manifest | P_WEP_tau_parser_manifest.json | hash/schema/unit/source manifest | False | MISSING_LIVE_ARTIFACT | False |
| LIVE2512_8_verdict | live tau artifact set | complete branch-locked tau-min evidence pack | True | LIVE_SET_INCOMPLETE | False |

## Delta-w Width Law
| law_id | quantity | law | numeric_value | units | status |
| --- | --- | --- | --- | --- | --- |
| WIDTH2512_0_product_bound | P_WEP_relative_source_weight | abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15 | 2.8e-15 | dimensionless product | EXACT_PRODUCT_BOUND_FROM_2511_NONCLAIM |
| WIDTH2512_1_width_if_tau_min | Delta_w_TiPt | if abs(tau_WEP)>=tau_min>0 then abs(Delta_w_TiPt)<=2.8e-15/tau_min | MISSING_TAU_MIN | dimensionless source-weight width | EXACT_CONDITIONAL_WIDTH_LAW_NOT_EVALUABLE |
| WIDTH2512_2_tau_zero_case | WEP sensitivity | if tau_WEP=0 then WEP does not bound Delta_w_TiPt on this projection | NOT_A_PASS | arena statement | WEP_BLINDNESS_NOT_LOCAL_GR_SAFETY |
| WIDTH2512_3_total_guard | local source-weight safety | WEP width cannot replace PPN/R10/clock/orbit kernels for the same Delta_w_eff vector | MISSING_CROSS_ARENA_KERNELS | policy | LOCAL_GR_STILL_BLOCKED |

## Nonclaim Dry Run
| case_id | case_description | result_status | blocking_markers | pass_fail | claim_pass |
| --- | --- | --- | --- | --- | --- |
| DRY2512_0_live_missing | run tau-min conversion with no live drop artifacts | REFUSED_LIVE_SET_INCOMPLETE | MISSING_LIVE_ARTIFACTS;MISSING_TAU_MIN | BLOCKED_NONCLAIM | False |
| DRY2512_1_tau_equals_one | set tau_WEP=1 by convention | REFUSED_TAU_UNITY_SHORTCUT | NO_TAU_UNITY_SHORTCUT;MISSING_NORMALIZATION_DERIVATION | BLOCKED_NONCLAIM | False |
| DRY2512_2_nonzero_source_material | infer tau nonzero from nonzero source/material vectors alone | REFUSED_NULLSPACE_COUNTERMODEL | MISSING_ALIGNMENT_FLOOR;KER_K_CMSM_NULLSPACE_NOT_EXCLUDED | BLOCKED_NONCLAIM | False |
| DRY2512_3_product_to_width | convert 2.8e-15 product ceiling into Delta_w width without tau_min | REFUSED_MISSING_TAU_MIN | MISSING_TAU_MIN;WIDTH_LAW_NOT_EVALUABLE | BLOCKED_NONCLAIM | False |
| DRY2512_4_wep_to_ppn | use WEP tau result to infer PPN/local-GR closure | REFUSED_WRONG_ARENA_INFERENCE | MISSING_PPN_SOURCE_KERNEL;MISSING_FIXED_GM_MAP | BLOCKED_NONCLAIM | False |

## Decision Ledger
| decision_id | decision | rationale | status |
| --- | --- | --- | --- |
| DEC2512_0_gain | TAU_NONDEGENERACY_THEOREM_WRITTEN_CONDITIONALLY | A positive tau lower bound requires an alignment floor between the readout kernel and source/material vector. | conditional_not_promoted |
| DEC2512_1_reject | NO_TAU_SHORTCUT | tau_WEP cannot be set to 1, and nonzero source/material factors do not exclude the readout-kernel nullspace. | enforced |
| DEC2512_2_data | LIVE_MICROSCOPE_TAU_PACK_MISSING | The live drop has no complete branch-locked readout/source/material/tau_min artifact set. | blocked_external_data_route |
| DEC2512_3_width | DELTAW_WIDTH_BLOCKED_BY_TAU_MIN | The product bound survives, but standalone Delta_w_TiPt width remains nonnumeric until tau_min exists. | retained_nonclaim |
| DEC2512_4_best_next | PIVOT_TO_PPN_SOURCE_KERNEL_FIXED_GM_MAP | The WEP tau route is now correctly caged; the GR/Newton bridge needs the PPN/source-normalization response kernel. | selected |

## Next Target
| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2512_0_selected | selected_theory_route | 2513-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md | scripts/Y5_R2FR_source_weight_PPN_response_kernel_fixed_GM_map_2513.py | derive or bound how Delta_w_eff enters gamma, beta, preferred-frame/source-exchange terms, and measured-GM transfer in a fixed local weak-field convention | PPN source-weight response rows have units, source paths, comparator bounds, no fitted-G absorption, and valid_for_claim=false unless kernels and coefficients are real | do not infer PPN/local GR from WEP; do not import GR as the response kernel; do not absorb relative weights into measured G |
| NEXT2512_1_data_route | held_until_files_exist | 2513b-Y5-R2FR-MICROSCOPE-tau-live-drop-validator.md | scripts/Y5_R2FR_MICROSCOPE_tau_live_drop_validator_2513b.py | validate live MICROSCOPE tau drop artifacts if the exact files appear in the 1704 live folder | all exact live files parse, branch-lock, hash-lock, declare units/sign conventions, and keep nonclaim flags until later promotion | do not fabricate arrays, do not treat templates as data, do not use bound anchors as predictions |

## Validation
| check_id | status | detail |
| --- | --- | --- |
| VAL2512_00_sources_exist | PASS |  |
| VAL2512_01_source_needles | PASS |  |
| VAL2512_02_conditional_theorem | PASS | nondegeneracy theorem written conditionally |
| VAL2512_03_nullspace_guard | PASS | nullspace shortcut blocker present |
| VAL2512_04_tau_min_missing | PASS | tau_min remains missing |
| VAL2512_05_live_set_incomplete | PASS | live artifact set incomplete as expected |
| VAL2512_06_width_blocked | PASS | Delta_w width not evaluated |
| VAL2512_07_dryruns_block_claims | PASS | all dry runs nonclaim |
| VAL2512_08_next_target | PASS | PPN fixed-GM route selected |
| VAL2512_09_no_claim_flags | PASS |  |
| VAL2512_10_branch_copies | PASS |  |
| VAL2512_11_no_formalization_artifacts | PASS |  |
| VAL2512_12_pycache_absent | PASS |  |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_SOURCE_REGISTER | PASS | OK; rows=11 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_TAU_NONDEGENERACY_PROOF_ATTEMPT | PASS | OK; rows=6 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_TAU_MIN_CERTIFICATE_CONTRACT | PASS | OK; rows=5 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_LIVE_TAU_ARTIFACT_GATE | PASS | OK; rows=9 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_DELTAW_WIDTH_LAW | PASS | OK; rows=4 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_NONCLAIM_DRYRUN_RESULTS | PASS | OK; rows=5 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_DECISION_LEDGER | PASS | OK; rows=5 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_NEXT_TARGET | PASS | OK; rows=2 |
| VAL2512_CSV_P8_Y5_NO_SHADOW_2512_BRANCH_COPIES | PASS | OK; rows=4 |
| VAL2512_COPY_CSV_tau_nondegeneracy | PASS | OK; rows=6 |
| VAL2512_COPY_CSV_tau_live_gate | PASS | OK; rows=9 |
| VAL2512_COPY_CSV_delta_w_width | PASS | OK; rows=4 |
| VAL2512_COPY_CSV_ppn_next | PASS | OK; rows=2 |
| VAL2512_OVERALL | PASS | 2512 writes the conditional tau nondegeneracy theorem, refuses shortcuts, and pivots to PPN source kernel |
