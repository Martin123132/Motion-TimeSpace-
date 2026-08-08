# 871 - Y5/R10 c_T Trace Leakage Bound Source Row Builder

Status: `Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim`  
Claim ceiling: `source_ready_cT_bound_ledger_only_no_R10_PPN_clock_WEP_or_orbital_pass`  
Generated UTC: `2026-06-13T11:12:38.503225+00:00`

Current result: **the c_T coupling is now source-ready but not theory-ready**. R10 anchors, Cassini/INPOP PPN gates, Galileo clock redshift, MICROSCOPE WEP, and LLR/orbital source candidates are staged with units and provenance. None of them becomes a c_T bound because the parent projection from `P_loc J_trace` to observable amplitudes is still missing.

## Nonclaim Summary
| status | claim_ceiling | what_changed | best_partial_result | hard_blockers | what_is_not_claimed | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim | source_ready_cT_bound_ledger_only_no_R10_PPN_clock_WEP_or_orbital_pass | built a c_T source/bound ledger across R10, PPN, clocks/WEP, and orbital channels | the data gates are now explicit and nonclaim; R10 anchor rows are positive numeric smoke anchors | parent c_T projection coefficient, full R10 curve, source normalization, matter marker silence | c_T bound, c_T zero, R10 pass, PPN pass, clock/WEP pass, orbital pass, local GR/Newton | 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md | false | 2026-06-13T11:12:38.503225+00:00 |

## Source Register
| source_id | path | exists | needle_check | role | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 870_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md | true | pass | immediate c_T trace leakage handoff | false | 2026-06-13T11:12:38.503225+00:00 |
| 870_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_870_VALIDATION.csv | true | pass | prior checkpoint validation | false | 2026-06-13T11:12:38.503225+00:00 |
| 563_R10_anchor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md | true | pass | real R10 anchor source hierarchy and full-curve blocker | false | 2026-06-13T11:12:38.503225+00:00 |
| 15_local_observables | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\15-local-observables-data-map.md | true | pass | published PPN, clock, WEP local observable gates | false | 2026-06-13T11:12:38.503225+00:00 |
| 15_published_bound_sources | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\runs\20260530-232024-local-observables-data-map\results\published_bound_sources.csv | true | pass | local source URL ledger for published observable gates | false | 2026-06-13T11:12:38.503225+00:00 |
| 393_Newton_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\393-source-normalized-Newtonian-limit-under-identity-closure.md | true | pass | source-normalized Newtonian limit and GM absorption blocker | false | 2026-06-13T11:12:38.503225+00:00 |
| 179_PPN_silence | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\179-local-GR-PPN-silence-contract.md | true | pass | PPN silence target and q_loc blocker | false | 2026-06-13T11:12:38.503225+00:00 |

## Bound Source Candidates
| source_id | arena | observable | source_title | year | source_url | doi | extraction_method | source_status | units | usable_as | valid_for_claim | notes | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC871_R10_EOTWASH_2020_ANCHOR | R10_short_range_inverse_square | alpha(lambda)_Yukawa_strength | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um | 2020 | https://arxiv.org/abs/2002.11761; https://pubmed.ncbi.nlm.nih.gov/32216404/ | 10.1103/PhysRevLett.124.101101 | anchor_only_alpha_equals_1_threshold_from_563_source_hierarchy | anchor_only_noncurve | lambda:m; alpha:dimensionless | provenance_and_smoke_anchor_only | false | Full alpha(lambda) curve still absent; do not score a c_T claim from this anchor. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_R10_EOTWASH_2007_ANCHOR | R10_short_range_inverse_square | alpha(lambda)_Yukawa_strength | Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale | 2007 | https://arxiv.org/abs/hep-ph/0611184; https://link.aps.org/doi/10.1103/PhysRevLett.98.021101 | 10.1103/PhysRevLett.98.021101 | anchor_only_abs_alpha_le_1_threshold_from_563_source_hierarchy | continuity_anchor_only_noncurve | lambda:m; alpha:dimensionless | historical_continuity_and_smoke_anchor_only | false | Older threshold anchor; useful for plumbing but not a modern claim curve. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_PPN_CASSINI_GAMMA | PPN_radio_science | gamma_minus_one | Cassini radio-link Shapiro delay gamma constraint | 2003 | https://pubmed.ncbi.nlm.nih.gov/14508481/; https://doi.org/10.1038/nature01997 | 10.1038/nature01997 | published_bound_source_map_and_direct_citation | source_candidate_numeric_bound_available | dimensionless | PPN gamma bound only after c_T_to_gamma projection exists | false | Local map records gamma=1+(2.1+/-2.3)e-5; projection from c_T is missing. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_PPN_INPOP20A_BETA_GAMMA | PPN_planetary_ephemerides | beta_minus_one_and_gamma_minus_one | INPOP20a planetary ephemerides conservative PPN intervals | 2021 | https://arxiv.org/abs/2111.04499 | not_recorded_in_15_source_map | published_bound_source_map | source_candidate_numeric_bound_available | dimensionless | planetary PPN cross-check after c_T projection exists | false | Local map records beta and gamma conservative intervals; not a raw likelihood. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_CLOCK_GALILEO_REDSHIFT | clock_redshift | redshift_fractional_deviation | Galileo eccentric-satellite gravitational redshift test | 2018 | https://arxiv.org/abs/1812.03711 | not_recorded_in_15_source_map | published_bound_source_map | source_candidate_numeric_bound_available | dimensionless_fractional_deviation | clock/load anomaly gate after c_T_to_clock projection exists | false | Local map records (+0.19 +/- 2.48)e-5; projection from trace leakage to clock observable is absent. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_WEP_MICROSCOPE_FINAL | weak_equivalence_principle | eta_Ti_Pt | MICROSCOPE mission final WEP result | 2022 | https://arxiv.org/abs/2209.15487; https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 | 10.1103/PhysRevLett.129.121102 | published_bound_source_map_and_PRL_source_candidate | source_candidate_numeric_bound_available | dimensionless_Eotvos_ratio | WEP/composition coupling gate after species projection exists | false | Local map records quadrature proxy 2.745906043549196e-15; c_T composition projection is missing. | 2026-06-13T11:12:38.503225+00:00 |
| SRC871_ORBITAL_LLR_REVIEW | orbital_lunar_laser_ranging | Gdot_over_G_or_anomalous_radial_acceleration | Tests of Gravity Using Lunar Laser Ranging | 2010 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/ | 10.12942/lrr-2010-7 | source_candidate_review_context_only | review_candidate_no_numeric_row_extracted | arena_dependent | orbital source hierarchy only until numeric observable and c_T projection are selected | false | Use to choose a source-normalization/orbital bound, not as a direct c_T claim row. | 2026-06-13T11:12:38.503225+00:00 |

## c_T Projection Contract
| projection_id | arena | observable | input_cT_piece | required_formula | current_status | missing_inputs | claim_consequence | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PC871_0_R10_alpha_lambda | R10_short_range_inverse_square | alpha_T(lambda) | c_T * P_loc J_trace finite-range scalar component | alpha_T(lambda)=F_T[c_T,lambda_T,G_eff,M_eff,source_geometry] | blocked_projection_missing_and_full_curve_missing | parent c_T coefficient; lambda_T/mass gap; source-normalized coupling; full alpha(lambda) curve | R10/fifth-force claim forbidden; anchors are smoke-only | false | 2026-06-13T11:12:38.503225+00:00 |
| PC871_1_PPN_gamma_beta | PPN_solar_system | gamma-1,beta-1 | local scalar trace leakage in metric potentials | gamma-1=G_T_gamma*c_T and beta-1=G_T_beta*c_T plus source-normalization terms | blocked_parent_response_operator_missing | metric response operator; gauge fixing; source-normalization residual split; degeneracy with c_S | PPN/local-GR claim forbidden | false | 2026-06-13T11:12:38.503225+00:00 |
| PC871_2_clock_WEP | clock_and_WEP | clock drift and eta composition charge | trace leakage into matter clocks/species markers | delta_nu/nu=C_T_clock*c_T and eta_AB=C_T_AB*c_T | blocked_species_marker_projection_missing | matter action descent; species marker/no-marker theorem; clock functional; c_e separation | clock/WEP claim forbidden | false | 2026-06-13T11:12:38.503225+00:00 |
| PC871_3_orbital_GM | orbital_dynamics | Gdot/G,delta_GM,anomalous_radial_acceleration | trace leakage into observed source normalization | delta_mu/mu=C_T_mu*c_T with mu_obs=G_eff*M_eff+mu_extra | blocked_source_normalization_missing | constant universal absorption proof; time constancy; source geometry; separation from c_S | Newton/orbital/local-GR claim forbidden | false | 2026-06-13T11:12:38.503225+00:00 |

## c_T Bound Rows
| bound_id | arena | observable | bound_value | bound_units | lambda_value | lambda_units | confidence | source_id | source_path_or_url | extraction_status | projection_status | valid_for_claim | notes | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR | R10_short_range_inverse_square | alpha(lambda) | 1.0 | dimensionless_alpha | 3.86e-5 | m | 95_percent | SRC871_R10_EOTWASH_2020_ANCHOR | 563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM; https://arxiv.org/abs/2002.11761 | anchor_only_noncurve | missing_cT_to_alpha_projection | false | Positive numeric source-backed threshold anchor, deliberately invalid for claim scoring. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_R10_EOTWASH_2007_ALPHA1_56UM_ANCHOR | R10_short_range_inverse_square | alpha(lambda) | 1.0 | dimensionless_alpha | 5.6e-5 | m | 95_percent | SRC871_R10_EOTWASH_2007_ANCHOR | 563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM; https://arxiv.org/abs/hep-ph/0611184 | anchor_only_noncurve | missing_cT_to_alpha_projection | false | Continuity anchor only; not a full bound curve and not a claim row. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_PPN_CASSINI_GAMMA_SIGMA | PPN_radio_science | gamma_minus_one | 2.3e-5 | dimensionless_1sigma | not_applicable | not_applicable | 1sigma_published_uncertainty | SRC871_PPN_CASSINI_GAMMA | 15-local-observables-data-map.md::Cassini radio science; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::cassini_bertotti_2003 | numeric_published_bound_available | missing_cT_to_gamma_projection | false | Bound exists but is not a c_T bound until the response coefficient is derived. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_PPN_INPOP20A_BETA_INTERVAL | PPN_planetary_ephemerides | beta_minus_one | 7.16e-5 | dimensionless_conservative_interval | not_applicable | not_applicable | conservative_acceptable_interval | SRC871_PPN_INPOP20A_BETA_GAMMA | 15-local-observables-data-map.md::INPOP20a planetary ephemerides; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::inpop20a_fienga_2021 | numeric_published_bound_available | missing_cT_to_beta_projection | false | Conservative PPN gate only; not a one-parameter c_T likelihood. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_CLOCK_GALILEO_REDSHIFT_SIGMA | clock_redshift | redshift_fractional_deviation | 2.48e-5 | dimensionless_1sigma_fractional_deviation | not_applicable | not_applicable | 1sigma_published_uncertainty | SRC871_CLOCK_GALILEO_REDSHIFT | 15-local-observables-data-map.md::Galileo eccentric satellites; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::galileo_delva_2018 | numeric_published_bound_available | missing_cT_to_clock_projection | false | Clock bound is source-ready but the MTS clock functional is not derived. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_WEP_MICROSCOPE_ETA_PROXY | weak_equivalence_principle | eta_Ti_Pt | 2.745906043549196e-15 | dimensionless_Eotvos_quadrature_proxy | not_applicable | not_applicable | combined_1sigma_proxy_from_stat_syst | SRC871_WEP_MICROSCOPE_FINAL | 15-local-observables-data-map.md::MICROSCOPE final WEP result; runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv::microscope_touboul_2022 | numeric_published_bound_available | missing_cT_species_marker_projection | false | WEP bound is very sharp; precisely why the species/no-marker theorem cannot be hand-waved. | 2026-06-13T11:12:38.503225+00:00 |
| CT871_ORBITAL_LLR_REVIEW_PLACEHOLDER | orbital_lunar_laser_ranging | Gdot_over_G_or_anomalous_radial_acceleration | MISSING_NUMERIC_ORBITAL_BOUND_SELECTION | arena_dependent | not_applicable | not_applicable | not_selected | SRC871_ORBITAL_LLR_REVIEW | https://pmc.ncbi.nlm.nih.gov/articles/PMC5253913/ | review_candidate_no_numeric_row_extracted | missing_cT_to_GM_or_acceleration_projection | false | Kept as an acquisition row only; choose a specific orbital observable before any calculator. | 2026-06-13T11:12:38.503225+00:00 |

## Claim Readiness
| gate_id | required_for_claim | status | reason | next_action | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| CR871_0_parent_cT_projection | derive c_T from parent action or prove c_T=0 | blocked | 870 left P_loc J_trace no-hair unsigned; 871 only stages external gates | derive c_T response coefficient or theorem-zero return | false | 2026-06-13T11:12:38.503225+00:00 |
| CR871_1_R10_full_curve | full positive numeric alpha(lambda) curve or official table | blocked | 563 has only alpha=1 threshold anchors | digitize/source PRL 2020 curve before any R10 score | false | 2026-06-13T11:12:38.503225+00:00 |
| CR871_2_source_normalization | map trace leakage through G_eff,M_eff,GM absorption without hiding a force | blocked | 393 source-normalized Newtonian branch is conditional only | derive constant universal absorption or keep c_S/c_T residual split | false | 2026-06-13T11:12:38.503225+00:00 |
| CR871_3_matter_marker_silence | prove c_T does not induce species-dependent clocks/WEP charge | blocked | clock/WEP gates are sharp and matter descent is not parent-signed | connect c_T to matter descent/no-marker theorem or bound it explicitly | false | 2026-06-13T11:12:38.503225+00:00 |

## Route Choice
| route_id | route | status | reason | include | exclude | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RC871_0_selected | cT_parent_projection_coefficient_or_theorem_zero_return | selected | source rows now exist; the missing object is not more data but the parent map from P_loc J_trace to observables | derive c_T response coefficient, prove c_T=0, or write exact closure status if neither works | claim scoring, local GR pass, GitHub action, formalization-workbench edits | false | 2026-06-13T11:12:38.503225+00:00 |

## Claim Guard
| guard_id | claim | status | reason | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| CG871_0_no_cT_bound_claim | c_T is bounded by R10/PPN/clock/WEP/orbital tests | forbidden | external bounds are source-ready but c_T observable projection is missing | false | 2026-06-13T11:12:38.503225+00:00 |
| CG871_1_no_R10_claim | R10/fifth-force pass | forbidden | only threshold anchors exist and parent alpha_T(lambda) is absent | false | 2026-06-13T11:12:38.503225+00:00 |
| CG871_2_no_local_GR_claim | local GR/Newton follows | forbidden | c_T is only one retained q_loc channel and source normalization remains conditional | false | 2026-06-13T11:12:38.503225+00:00 |
| CG871_3_allowed_private_result | c_T bound source rows are staged and all claim gates remain closed | allowed_private_nonclaim | 871 improves test plumbing without overstating theory status | false | 2026-06-13T11:12:38.503225+00:00 |

## Decision
| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D871_0 | cT_bound_sources_staged | R10 anchors plus PPN, clock, WEP, and orbital source candidates are recorded with units and provenance | Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim | false | 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md | false | 2026-06-13T11:12:38.503225+00:00 |
| D871_1 | parent_projection_missing_is_now_primary_blocker | without F_T from c_T/P_loc J_trace to observable amplitudes, data cannot decide the local branch | Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim | false | 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md | false | 2026-06-13T11:12:38.503225+00:00 |
| D871_2 | the_coupling_is_the_fight | local tests are not the weak part of the plumbing; the weak part is the coupling/projection coefficient | Y5_R10_871_cT_bound_source_rows_staged_parent_projection_missing_nonclaim | false | 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md | false | 2026-06-13T11:12:38.503225+00:00 |

## Next Target
| next_target | objective | include | exclude | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md | derive the c_T parent projection coefficient from P_loc J_trace to alpha(lambda), PPN, clock/WEP, and orbital observables, or prove c_T=0 | parent variation, response operator, source normalization, matter descent/no-marker clauses, theorem-zero fallback | claim rows, fitted shortcuts, hidden calibration, formalization-workbench edits, GitHub action | false | 2026-06-13T11:12:38.503225+00:00 |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V871_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V871_1_prior_870_clean | pass | P8_Y5_BRR545_870_VALIDATION.csv clean |
| V871_2_source_candidates_nonclaim_with_urls | pass | source_candidates=7 nonclaim with URLs |
| V871_3_R10_anchor_rows_positive_numeric_nonclaim | pass | r10_anchor_rows=2 positive numeric and nonclaim |
| V871_4_projection_contract_blocks_claim | pass | all c_T observable projections remain blocked by missing parent inputs |
| V871_5_claim_readiness_blocked | pass | all claim readiness gates remain blocked |
| V871_6_no_valid_claim_row_has_missing_markers | pass | no valid_for_claim=true row contains missing markers |
| V871_7_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V871_8_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V871_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V871_10_route_selected | pass | 872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md |
| V871_11_validation_rows_ready | pass | validation table constructed |
