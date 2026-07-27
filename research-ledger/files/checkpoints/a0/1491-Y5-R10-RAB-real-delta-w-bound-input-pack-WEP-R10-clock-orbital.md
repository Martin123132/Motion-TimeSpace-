# 1491 - Real delta w Bound Input Pack: WEP, R10, Clock, Orbital

## Verdict
- `delta_w` is now staged as an empirical residual branch, not a theorem-zero coupling claim.
- MICROSCOPE, clocks, and orbital/Gdot have useful source-backed bound anchors; EotWash WEP and R10 still need source acquisition or curve/kernel promotion.
- No arena is score-ready because component basis, projection kernels, same-branch convention, and no-cancellation policy are still missing.

## Bound Anchors
| anchor_id | arena | bound_status | bound_value | why_nonclaim |
| --- | --- | --- | --- | --- |
| BAN1491_0_MICROSCOPE_TiPt | WEP_MICROSCOPE_TiPt | SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE | 2.8e-15 | official eta bound exists, but C_parent/source vector/material tensor/K_CMSM/product convention/tau_eff remain missing |
| BAN1491_1_EotWash_WEP | WEP_EotWash_material_pairs | LOCAL_SOURCE_ACQUISITION_REQUIRED | MISSING_SOURCE_BACKED_BOUND | no local EotWash WEP material/source vector and eta row is available in this workspace yet |
| BAN1491_2_R10_short_range | R10_short_range_inverse_square | SYMBOLIC_CURVE_ANCHOR_ONLY | alpha(lambda) | review/source anchor exists, but no promoted digitized alpha(lambda) curve, lambda convention, or delta_w kernel is loaded |
| BAN1491_3_clock_product | clock_alpha_mass | SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE | 2.1e-18 | clock row bounds a product; tau_clock/source-coefficient split and delta_w projection are missing |
| BAN1491_4_orbital_Gdot | orbital_GM_time_drift | SOURCE_BACKED_BOUND_ANCHOR_AVAILABLE | 9.6e-15 | orbital/GM bound anchor exists, but worldtube source map, measured-GM convention, and delta_w projection are missing |

## Delta w Input Pack
| input_id | arena | current_status | bound_or_value | missing_for_claim |
| --- | --- | --- | --- | --- |
| DWI1491_0_core_model | core | MISSING_PARENT_COMPONENT_BASIS | MISSING | parent component basis, covariance/no-cancellation policy, same-branch convention |
| DWI1491_1_MICROSCOPE_TiPt | WEP_MICROSCOPE_TiPt | BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED | 2.8e-15 | official readout arrays, source worldtube, full material tensor, product convention, tau_eff |
| DWI1491_2_EotWash_WEP | WEP_EotWash_material_pairs | SOURCE_ACQUISITION_REQUIRED | MISSING_SOURCE_BACKED_BOUND | published eta bound, material/source composition vectors, attractor/source map, range/profile transfer |
| DWI1491_3_R10 | R10_short_range | SYMBOLIC_ANCHOR_ONLY_CURVE_KERNEL_MISSING | alpha(lambda) | promoted digitized alpha(lambda) curve, lambda convention, Yukawa/non-Yukawa kernel, source/test composition |
| DWI1491_4_clock | clock_alpha_mass | PRODUCT_BOUND_AVAILABLE_PROJECTION_BLOCKED | 2.1e-18 | tau_clock, clock readout kernel, alpha/mass/source-coefficient split, no cross-arena transfer proof |
| DWI1491_5_orbital | orbital_GM_time_drift | BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED | 9.6e-15 | source body composition, worldtube/Gauss bridge, measured GM convention, orbital residual projection |

## Projection Requirements
| requirement_id | arena | current_status | acceptance_rule |
| --- | --- | --- | --- |
| APR1491_0_component_basis | all_arenas | MISSING_PARENT_COUPLING_BASIS | same basis across WEP/R10/clock/orbital |
| APR1491_1_material_source | WEP/R10 | PARTIAL_OR_MISSING | Ti/Pt full tensor, EotWash material pairs, R10 source/test composition |
| APR1491_2_tau_projection | all_arenas | MISSING_ARENA_PROJECTIONS | tau_WEP, tau_R10(lambda), tau_clock, orbital/worldtube projection |
| APR1491_3_readout | MICROSCOPE/clock/orbital | MISSING_OR_PARTIAL | CMSM arrays, clock readout functional, measured GM convention |
| APR1491_4_R10_curve | R10 | MISSING_PROMOTED_CURVE_AND_KERNEL | full curve or machine-readable table with lambda convention |
| APR1491_5_no_cancellation | all_arenas | MISSING_NO_CANCELLATION_ENVELOPE | norm/covariance policy before comparing multi-component vectors |
| APR1491_6_same_branch | all_arenas | MISSING_SAME_BRANCH_PRODUCT_CONVENTION | C_parent/source/material/readout/bound must share units/sign/basis |

## Calibration Gates
| gate_id | gate | current_status | rule |
| --- | --- | --- | --- |
| CG1491_0_common_mode | common w_star calibration | guarded | w_star is not a WEP signal only if species/time/range/frame/source-body silent |
| CG1491_1_delta_definition | delta_w_A = w_A - w_star | locked | all arena rows compare relative source weights, not common calibration |
| CG1491_2_no_cancellation | no tuned vector cancellation | active_block | component products must pass by norm/covariance or parent identity, not cherry-picked cancellation |
| CG1491_3_same_branch | same branch product | active_block | do not mix DD smoke, MICROSCOPE surrogate, and parent basis rows as one claim |
| CG1491_4_cross_arena | no cross-arena transfer | active_block | clock product bound cannot become WEP/R10 bound without a projection theorem |

## Readiness Matrix
| readiness_id | arena | source_backed_bound_anchor_available | score_ready | status_detail |
| --- | --- | --- | --- | --- |
| RDY1491_0_MICROSCOPE | WEP_MICROSCOPE_TiPt | True | False | bound anchor exists; official readout/material/source/product convention missing |
| RDY1491_1_EotWash | WEP_EotWash_material_pairs | False | False | local source-backed WEP material-pair bound row missing |
| RDY1491_2_R10 | R10_short_range | False | False | symbolic alpha(lambda) anchor only; curve/kernel missing |
| RDY1491_3_clock | clock_alpha_mass | True | False | product bound exists; tau/readout/alpha-mass-source split missing |
| RDY1491_4_orbital | orbital_GM_time_drift | True | False | Gdot/GM anchor exists; worldtube/orbital projection missing |
| RDY1491_5_overall | all_arenas | False | False | no arena has all bound, source vector, projection kernel, units, and same-branch lock |

## Local GR/Newton Status
| status_id | target | current_status | claim_effect |
| --- | --- | --- | --- |
| LRS1491_0_delta_w | delta_w residual branch | INPUTS_STAGED_NOT_SCORE_READY | coupling still not theorem-zero |
| LRS1491_1_WEP | WEP/MICROSCOPE | BOUND_ANCHOR_ONLY | WEP claim blocked |
| LRS1491_2_R10 | short-range/R10 | CURVE_KERNEL_MISSING | R10 claim blocked |
| LRS1491_3_clock_orbit | clock/orbital | PROJECTION_MISSING | cannot transfer to local-GR coupling |
| LRS1491_4_verdict | local GR/Newton status | NOT_CLOSED_NEXT_SOURCE_ACQUISITION_RUNNER | no local-GR/Newton/WEP/R10 claim from 1491 |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
| --- | --- | --- |
| REJ1491_0_theorem | COUPLING_THEOREM_NOT_DERIVED | delta_w remains a residual branch, not theorem-zero |
| REJ1491_1_projection | ARENA_PROJECTIONS_MISSING | tau/readout/worldtube kernels are missing or partial |
| REJ1491_2_EotWash | EOTWASH_SOURCE_ACQUISITION_REQUIRED | no local EotWash WEP source-backed bound row exists |
| REJ1491_3_R10 | R10_CURVE_KERNEL_MISSING | alpha(lambda) is symbolic and not promoted |
| REJ1491_4_MICROSCOPE | MICROSCOPE_OFFICIAL_FILES_MISSING | official arrays/source/product/full material tensor missing |
| REJ1491_5_clock | CLOCK_PRODUCT_NOT_DELTA_W | clock bounds product terms only and cannot transfer without projection |
| REJ1491_6_orbit | ORBITAL_WORLDTUBE_MAP_MISSING | Gdot/GM anchor lacks delta_w source projection |
| REJ1491_7_Cparent | C_PARENT_IMPORT_FORBIDDEN | no coupling theorem/import allowed |
| REJ1491_8_claim | CLAIM_PROMOTION_FORBIDDEN | no WEP/local-GR/Newton/R10 claim allowed |

## Decision Ledger
- `DEC1491_0_bound_pack`: keep delta_w pack nonclaim - do not run score/comparison yet.
- `DEC1491_1_source_priority`: prioritize source acquisition - build acquisition ledger for EotWash/R10/MICROSCOPE official files.
- `DEC1491_2_MICROSCOPE`: retain MICROSCOPE as strongest bound anchor - fill official files/product convention before claim-grade WEP run.
- `DEC1491_3_no_transfer`: do not transfer clock/orbital anchors to WEP - keep each arena separate until tau maps exist.

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1491_0_sources | PASS | all cited local source paths exist |
| VAL1491_1_anchor_rows | PASS | five arena anchor rows written |
| VAL1491_2_source_backed_paths | PASS | source-backed anchors have local source paths |
| VAL1491_3_missing_rows_nonclaim | PASS | missing/symbolic anchors remain nonclaim |
| VAL1491_4_input_pack_nonclaim | PASS | all delta_w input rows are nonclaim and not score-ready |
| VAL1491_5_projection_requirements_open | PASS | arena projection requirements remain open |
| VAL1491_6_calibration_gates | PASS | common calibration/no-cancellation gates are active |
| VAL1491_7_overall_not_ready | PASS | overall delta_w branch is not score-ready |
| VAL1491_8_no_Cparent_import | PASS | live C_parent import remains absent and refused |
| VAL1491_9_local_blocked | PASS | local GR/Newton/WEP remains blocked pending source acquisition |
| VAL1491_10_rejections | PASS | rejection ledger blocks claim promotion |
| VAL1491_11_decisions | PASS | decision ledger prioritizes source acquisition |
| VAL1491_12_next | PASS | 1492 handoff written |
| VAL1491_13_csv_parse | PASS | all generated 1491 CSVs parse cleanly |
| VAL1491_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1491_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1491_16_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1491_17_claim_flags_false | PASS | all prediction/claim flags remain false |
| VAL1491_18_overall | PASS | 1491 builds a nonclaim source-backed delta_w input pack and hands off to source acquisition |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1491_0_1492 | 1492-Y5-R10-RAB-delta-w-source-acquisition-ledger-EotWash-R10-MICROSCOPE.md | scripts/Y5_R10_RAB_delta_w_source_acquisition_ledger_EotWash_R10_MICROSCOPE.py | acquire or ledger real source files for EotWash WEP material-pair bounds, R10 alpha(lambda) curve, and MICROSCOPE official readout/source/product files before any delta_w scoring |
