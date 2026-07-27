# 4626 - Source-Backed Yukawa Bound Table And Local-G Map

Timestamp UTC: `2026-07-06T18:01:33.530347+00:00`
Branch: `MTS_R2FR_Y5_SOURCE_BACKED_YUKAWA_LOCAL_G_MAP_4626`
Marker: `PPC4161_SOURCE_BACKED_YUKAWA_BOUND_TABLE_AND_LOCAL_G_MAP_4626`
Decision: `SOURCE_BACKED_ANCHORS_READY_FULL_CURVES_AND_MTS_NUMERIC_ROWS_STILL_BLOCK_LOCAL_GR_CLAIM`

## Result

4626 adds real source-backed bound anchors, but refuses to promote them into a full local-GR claim. The R10 row is an alpha=1 threshold anchor, not a digitized alpha(lambda) curve.

Main source-backed anchor:

`lambda = 38.6e-6 m`, `alpha_bound = 1` from the Eot-Wash 2020 short-range inverse-square result.

Local-G map:

`alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)` must be compared to `alpha_bound(lambda_mem)`.

Current verdict: empirical interface is ready for smoke tests, but claim-grade comparison is blocked by missing MTS numeric rows and missing full bound curves.

## Sources
| checkpoint | source_id | source_kind | path | path_exists | needle | needle_found | line | source_url | web_evidence | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | SRC4626_00_4625_next | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_NEXT_TARGET.csv | True | 4626-Y5-R2FR-source-backed-yukawa-bound-table-and-local-G-map.md | True | 2 |  |  | 4625 selected source-backed Yukawa/local-G map. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_01_4625_charge | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_TRACE_CHARGE_DERIVATION_ROWS.csv | True | QDER4625_0_gauss_law | True | 2 |  |  | 4625 Q_mem charge law. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_02_4625_zero | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_QMEM_ZERO_ROUTES.csv | True | QZ4625_0_parent_decoupling | True | 2 |  |  | 4625 exact zero route. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_03_4625_screen | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_SCREENING_OR_MASS_GAP_ROWS.csv | True | SCR4625_0_large_gap | True | 2 |  |  | 4625 screening/gap row. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_04_4625_yukawa | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_YUKAWA_BOUND_MAPPING_ROWS.csv | True | YB4625_0_alpha_yukawa_map | True | 2 |  |  | 4625 Yukawa alpha map. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_05_4625_arena | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4625_LOCAL_ARENA_BOUND_ROWS_NONCLAIM.csv | True | ARENA4625_0_R10_short_range | True | 2 |  |  | 4625 local arena row. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | SRC4626_06_4625_validation | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4625_VALIDATION.csv | True | VAL4625_OVERALL | True | 17 |  |  | 4625 validation. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | WEB4626_0_EOTWASH_2020 | web_primary_or_indexed |  | True |  | True |  | https://arxiv.org/abs/2002.11761 | arXiv lines 21-23: torsion balance separations 52 um to 3.0 mm; gravitational-strength Yukawa ranges <38.6 um at 95 percent confidence. | R10 short-range inverse-square/Yukawa alpha=1 threshold anchor. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | WEB4626_1_MICROSCOPE_2022 | web_primary_or_indexed |  | True |  | True |  | https://arxiv.org/abs/2209.15487 | arXiv lines 20-23: MICROSCOPE tests WEP to 1e-15 and reports eta(Ti,Pt)=(-1.5 +/-2.3 stat +/-1.5 syst)e-15 at 1 sigma. | WEP/Eotvos composition anchor. | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | WEB4626_2_CASSINI_2003 | web_primary_or_indexed |  | True |  | True |  | https://pubmed.ncbi.nlm.nih.gov/14508481/ | PubMed/search abstract reports gamma = 1 + (2.1 +/- 2.3)e-5. | Solar-system PPN gamma/local-G consistency anchor. | False | 2026-07-06T18:01:33.530347+00:00 |

## Source-Backed Bound Anchors
| checkpoint | anchor_id | arena | observable | lambda_value_m | alpha_bound | bound_type | confidence | source_url | source_evidence | full_curve | anchor_only | usable_for_smoke | valid_for_claim | claim_allowed | timestamp_utc | eta_bound_conservative_2sigma | gamma_minus_one_bound_conservative_2sigma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | BA4626_0_R10_EOTWASH_ALPHA1 | R10_short_range_inverse_square | Yukawa alpha(lambda) | 3.86e-05 | 1.0 | threshold_anchor_alpha_equals_1 | 95_percent | https://arxiv.org/abs/2002.11761 | gravitational-strength Yukawa interactions limited to ranges below 38.6 um; separations 52 um to 3.0 mm | False | True | True | False | False | 2026-07-06T18:01:33.530347+00:00 |  |  |
| 4626 | BA4626_1_WEP_MICROSCOPE_TiPt | WEP_Eotvos | eta_TiPt |  |  | derived_2sigma_from_stat_syst_1sigma | approx_2sigma_internal_gate | https://arxiv.org/abs/2209.15487 | eta(Ti,Pt)=(-1.5 +/- 2.3 stat +/- 1.5 syst)e-15 at 1 sigma; internal 2sigma gate uses 2*sqrt(2.3^2+1.5^2)e-15 | False | True | True | False | False | 2026-07-06T18:01:33.530347+00:00 | 5.5e-15 |  |
| 4626 | BA4626_2_PPN_CASSINI_GAMMA | solar_system_PPN | gamma_minus_one |  |  | derived_abs_mean_plus_2sigma | approx_2sigma_internal_gate | https://pubmed.ncbi.nlm.nih.gov/14508481/ | gamma=1+(2.1 +/-2.3)e-5; internal conservative gate uses (abs(2.1)+2*2.3)e-5 | False | True | True | False | False | 2026-07-06T18:01:33.530347+00:00 |  | 6.7e-05 |

## Local-G Bound Map Rows
| checkpoint | map_id | from_mts | to_observable | comparison | available_anchor | claim_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | LGM4626_0_R10_alpha | alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source) | Yukawa alpha(lambda) | require alpha_Y(lambda_mem) <= alpha_bound(lambda_mem) | BA4626_0_R10_EOTWASH_ALPHA1 | ANCHOR_ONLY_FULL_CURVE_MISSING | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | LGM4626_1_WEP_eta | eta_AB(lambda) ~= (alpha_A-alpha_B) Q_eff_source exp(-r/lambda)(1+r/lambda)/(4*pi Z_mem g r^2) | Eotvos eta_AB | require |eta_AB| <= eta_bound for the relevant composition/source geometry | BA4626_1_WEP_MICROSCOPE_TiPt | COMPOSITION_AND_GEOMETRY_MAP_MISSING | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | LGM4626_2_orbital_newton | delta_a/a_N ~= alpha_Y exp(-r/lambda_mem)(1+r/lambda_mem) | inverse-square/orbital residual | require residual below scale-dependent orbital/local-G bound | none_yet | SOURCE_BACKED_ORBITAL_BOUND_CURVE_MISSING | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | LGM4626_3_PPN_gamma | metric slip projection c_gamma(lambda)*alpha_Y(lambda) | gamma_minus_one | require |gamma-1| <= Cassini-style gamma bound after deriving projection c_gamma | BA4626_2_PPN_CASSINI_GAMMA | PPN_PROJECTION_COEFFICIENT_MISSING | False | False | 2026-07-06T18:01:33.530347+00:00 |

## MTS Yukawa Input Requirements
| checkpoint | input_id | symbol | definition | needed_for | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | MIN4626_0_lambda_mem | lambda_mem | sqrt(Z_mem/M2_mem) | all Yukawa/local-G comparisons | MISSING_ZMEM_M2MEM_NUMERIC_OR_BOUND | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | MIN4626_1_Qeff | Q_eff_source | S_scr Q_mem or exact zero | alpha_Y and WEP residuals | MISSING_QMEM_ZERO_SCREENING_OR_VALUE | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | MIN4626_2_alpha_A | alpha_A, alpha_B | test-body memory sensitivities | WEP and universal Yukawa force mapping | MISSING_UNIVERSAL_OR_COMPOSITION_DEPENDENT_SENSITIVITY | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | MIN4626_3_bound_curves | alpha_bound(lambda), eta_bound(lambda), orbital_bound(lambda) | source-backed full curves or safe interpolation tables | claim-grade local-G/PPN/Newtonian comparison | ANCHORS_ONLY_FULL_CURVES_MISSING | False | False | 2026-07-06T18:01:33.530347+00:00 |

## Bound Runner Dry-Run Rows
| checkpoint | runner_id | input_case | acceptance | failure_mode | ready_to_execute | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | RUN4626_0_anchor_smoke | lambda_mem=38.6e-6 m; alpha_Y numeric supplied | if alpha_Y<=1 at this anchor, R10 anchor smoke passes only at anchor point | does not prove full curve or other lambda values | True | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | RUN4626_1_missing_mts_inputs | current MTS rows with Q_eff/lambda/alpha_A missing | must fail closed with MISSING_MTS_NUMERIC_INPUT | any pass without Q_eff/lambda/sensitivity is invalid | True | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | RUN4626_2_full_claim | full source-backed curves plus MTS numeric rows | all relevant arenas pass across the claimed lambda/profile domain | blocked until full curves or defensible anchors for the claimed domain exist | False | False | False | 2026-07-06T18:01:33.530347+00:00 |

## Controls
| checkpoint | control_id | rule | violation_blocks_claim | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4626 | CTL4626_0_no_anchor_overclaim | A single alpha=1 threshold anchor is not a full alpha(lambda) curve. | True | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | CTL4626_1_no_mts_missing_pass | No bound runner can pass without lambda_mem, Q_eff, Z_mem and sensitivity rows. | True | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | CTL4626_2_ppn_projection_needed | Cassini gamma bounds cannot be applied to MTS until a metric-slip projection coefficient is derived. | True | 2026-07-06T18:01:33.530347+00:00 |

## Blockers
| checkpoint | blocker_id | blocks | missing | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4626 | BLK4626_0_MTS_numeric | any local-G empirical pass | lambda_mem, Q_eff_source, alpha_A/B, Z_mem | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | BLK4626_1_full_curves | claim-grade R10/WEP/orbital comparison | source-backed alpha(lambda), eta(lambda), orbital/local-G bound curves or domain-safe anchors | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | BLK4626_2_projection | PPN gamma use | MTS metric-slip projection coefficient c_gamma(lambda) | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | False | 2026-07-06T18:01:33.530347+00:00 |

## Promotion Gates
| checkpoint | gate_id | promotion_condition | current_result | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4626 | PROM4626_0_anchor_smoke | MTS provides numeric lambda/Qeff/alpha at anchor and passes the anchor inequality. | blocked_missing_mts_numeric | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | PROM4626_1_full_curve | Full source-backed curves and MTS profile domain pass with no extrapolation overclaim. | blocked_missing_full_curves | False | False | 2026-07-06T18:01:33.530347+00:00 |
| 4626 | PROM4626_2_exact_zero | Q_eff=0 or beta_T=0 parent theorem makes empirical Yukawa comparison unnecessary for that branch. | blocked_parent_zero_unsigned | False | False | 2026-07-06T18:01:33.530347+00:00 |

## Decision
| checkpoint | decision_id | decision | meaning | status | best_route | next_target | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | DEC4626_0 | SOURCE_BACKED_ANCHORS_READY_FULL_CURVES_AND_MTS_NUMERIC_ROWS_STILL_BLOCK_LOCAL_GR_CLAIM | Real source-backed anchors now exist for R10 alpha=1, MICROSCOPE WEP and Cassini gamma, but the branch remains nonclaim because MTS numeric inputs and full bound curves are missing. | NONCLAIM_PRIVATE_EMPIRICAL_INTERFACE_STAGE | derive beta_T/Q_eff exact zero or first numeric row before spending effort on full curves | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | False | False | 2026-07-06T18:01:33.530347+00:00 |

## Status
| checkpoint | branch_id | status | summary | valid_for_claim | claim_allowed | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | MTS_R2FR_Y5_SOURCE_BACKED_YUKAWA_LOCAL_G_MAP_4626 | PRIVATE_NONCLAIM_EMPIRICAL_INTERFACE_ADVANCE | Source-backed anchor table and local-G map written; no claim because anchors are not full curves and MTS numeric rows are missing. | False | False | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | 2026-07-06T18:01:33.530347+00:00 |

## Next Target
| checkpoint | branch_id | timestamp_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4626 | MTS_R2FR_Y5_SOURCE_BACKED_YUKAWA_LOCAL_G_MAP_4626 | 2026-07-06T18:01:33.530347+00:00 | 4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md | The empirical map is ready to accept numbers; the next bottleneck is beta_T/Q_eff/lambda_mem ownership or first numeric smoke row. | try beta_T=0, Q_eff=0 or parent screening theorem | stage first numeric nonclaim MTS smoke row and run anchor comparisons | False |

## Claim Safety

All rows remain `valid_for_claim=false`. Anchors can be used for smoke discipline only; full claims require full curves or a parent exact-zero route.
