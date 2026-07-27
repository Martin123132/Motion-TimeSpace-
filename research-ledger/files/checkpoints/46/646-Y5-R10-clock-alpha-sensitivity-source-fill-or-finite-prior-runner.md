# 646 Y5/R10 Clock Alpha Sensitivity Source Fill or Finite Prior Runner

## Verdict

- Status: `Y5_R10_clock_alpha_sources_filled_R2_redshift_repaired_finite_runner_still_blocked_by_chiX_tau`
- Claim ceiling: `clock_alpha_sensitivity_source_fill_and_symbolic_runner_only_no_numeric_kappa_alpha_score_no_clock_or_local_claim`
- Important repair: the Galileo `alpha` redshift row is not `alpha_EM`; it is an LPI/gravitational-redshift violation parameter.
- Source-backed optical-clock alpha pairs are now staged: Al+/Hg+ and Yb+ E3/E2.
- The finite runner is symbolic only. It cannot score MTS until `chi_X`/`Xhat` and `tau_clock` are derived or explicitly defined.

## Source Register

| source_id | label | source_kind | path_or_url | available | role |
| --- | --- | --- | --- | --- | --- |
| S646_0 | checkpoint_645_doc | local | 645-Y5-R10-finite-kappa-alpha-bound-input-fill-and-prior-discipline.md | true | prior finite-branch discipline checkpoint |
| S646_1 | validation_645 | local | source-intake/mts_residuals/P8_Y5_BRR545_645_VALIDATION.csv | true | prior validation |
| S646_2 | bound_input_645 | local | source-intake/mts_residuals/P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv | true | finite branch bound input ledger |
| S646_3 | projection_readiness_645 | local | source-intake/mts_residuals/P8_Y5_R10_645_PROJECTION_READINESS.csv | true | projection-readiness input |
| S646_4 | finite_prior_645 | local | source-intake/mts_residuals/P8_Y5_R10_645_FINITE_PRIOR_DISCIPLINE.csv | true | finite prior input |
| S646_5 | local_bound_matrix_639 | local | source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv | true | R2 clock-redshift row to repair |
| S646_6 | generator_script_646 | local | scripts/Y5_R10_clock_alpha_sensitivity_source_fill_or_finite_prior_runner.py | true | this checkpoint generator |
| W646_0 | NIST_Rosenband_AlHg | web | https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place | true | NIST record for Al+/Hg+ optical-clock ratio and alpha drift statement |
| W646_1 | Dzuba_Flambaum_arXiv_1999 | web | https://arxiv.org/abs/physics/9908047 | true | primary theory paper defining optical-clock alpha sensitivity idea |
| W646_2 | Frontiers_HCI_clock_review_2023 | web | https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full | true | source table for K_alpha values and clock-pair sensitivity differences |
| W646_3 | PTB_Yb_clock_alpha_limit | web | https://oar.ptb.de/resources/show/10.7795/110.20211216 | true | PTB source for Yb+ E3/E2 alpha-drift limit |
| W646_4 | Galileo_redshift_PRL_pdf | web | https://nebula.esa.int/sites/default/files/neb_tec_study/1301/C4000115150Paper.pdf | true | R2 redshift bound source; used only as LPI/redshift parameter source, not alpha_EM |

## Clock Alpha Sensitivity Sources

| clock_pair_id | clock_pair | K_alpha_1 | K_alpha_2 | delta_K_alpha_used | alpha_drift_source_value | numeric_score_ready |
| --- | --- | --- | --- | --- | --- | --- |
| CAS646_0_AlHg | 27Al+ / 199Hg+ | 0.008 | -2.94 | 2.95 | NIST: 1.4e-17 +/- 1.7e-17 yr^-1; Frontiers table reports -1.6e-17 +/- 2.3e-17 yr^-1 | false |
| CAS646_1_YbE3E2 | 171Yb+ E3 / 171Yb+ E2 | -5.95 | 1.03 | -6.95 | PTB/Frontiers: 1.0e-18 +/- 1.1e-18 yr^-1 | false |

## R2 Redshift Repair

| repair_id | source_row_id | old_label | repair_status | correct_interpretation | forbidden_use |
| --- | --- | --- | --- | --- | --- |
| R2R646_0 | R2_clock_redshift | alpha_clock_redshift | not_alpha_EM | Galileo eccentric-satellite row constrains an LPI/gravitational-redshift violation parameter called alpha in that paper, not the fine-structure constant alpha_EM. | do_not_use_as_delta_alpha_EM_or_clock_K_alpha_pair_bound |

## Clock Projection Ledger

| projection_id | law | MTS_substitution | MTS_law | missing_to_score |
| --- | --- | --- | --- | --- |
| CPL646_0_pair_ratio | d ln(nu_a/nu_b) = (K_alpha_a - K_alpha_b) d ln(alpha_EM) | d ln(alpha_EM) = kappa_alpha d chi_X | d ln R_ab = delta_K_alpha * kappa_alpha * d chi_X | d chi_X for the experiment or tau_clock mapping |
| CPL646_1_time_drift | d ln R_ab/dt = delta_K_alpha * d ln(alpha_EM)/dt | d ln(alpha_EM)/dt = kappa_alpha d chi_X/dt | d ln R_ab/dt = delta_K_alpha * kappa_alpha * d chi_X/dt | d chi_X/dt from MTS local/cosmological state |
| CPL646_2_gravitational_potential_coupling | d ln R_ab = delta_K_alpha * k_alpha_Phi d Phi/c^2 | k_alpha_Phi must be mapped from kappa_alpha and chi_X(Phi) | d ln R_ab = delta_K_alpha * kappa_alpha * (d chi_X/d Phi) d Phi | chi_X(Phi) or local potential projection |

## Finite Runner Smoke

| runner_id | clock_pair_id | normalized_kappa_alpha_factor | delta_K_alpha_used | normalized_response_dlnR_per_dchiX | numeric_score_ready |
| --- | --- | --- | --- | --- | --- |
| FCR646_00 | CAS646_0_AlHg | -10 | 2.95 | -29.5 | false |
| FCR646_01 | CAS646_0_AlHg | -1 | 2.95 | -2.95 | false |
| FCR646_02 | CAS646_0_AlHg | -0.1 | 2.95 | -0.295 | false |
| FCR646_03 | CAS646_0_AlHg | -0.01 | 2.95 | -0.0295 | false |
| FCR646_04 | CAS646_0_AlHg | 0.01 | 2.95 | 0.0295 | false |
| FCR646_05 | CAS646_0_AlHg | 0.1 | 2.95 | 0.295 | false |
| FCR646_06 | CAS646_0_AlHg | 1 | 2.95 | 2.95 | false |
| FCR646_07 | CAS646_0_AlHg | 10 | 2.95 | 29.5 | false |
| FCR646_08 | CAS646_1_YbE3E2 | -10 | -6.95 | 69.5 | false |
| FCR646_09 | CAS646_1_YbE3E2 | -1 | -6.95 | 6.95 | false |

- Full symbolic runner rows: `16`

## Readiness Gates

| gate_id | gate | result | blocks |
| --- | --- | --- | --- |
| RG646_0_R2_repair | R2 redshift alpha is separated from alpha_EM | pass_repaired | misusing Galileo redshift alpha as fine-structure alpha |
| RG646_1_deltaK_source | clock-pair delta_K_alpha values are source-backed | pass_for_source_fill | none for symbolic runner |
| RG646_2_chiX | MTS chi_X or Xhat unit exists | fail_missing | physical kappa_alpha score |
| RG646_3_tau_clock | tau_clock/time/potential map exists | fail_missing | clock bound projection into MTS variables |
| RG646_4_claim | finite runner may make a clock-alpha claim | fail_policy | no numeric score until RG646_2 and RG646_3 pass |

## Decision

| decision_id | route | decision | why | next_target |
| --- | --- | --- | --- | --- |
| D646_0 | clock_alpha_source_fill | source_fill_complete_nonclaim | Al/Hg and Yb E3/E2 provide source-backed delta_K_alpha clock pairs | 647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md |
| D646_1 | finite_prior_runner | symbolic_runner_complete_numeric_runner_blocked | delta_K is real, but chi_X and tau_clock are still missing | 647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V646_0_sources_available | pass | all local sources exist and web source strings are valid URLs |
| V646_1_prior_645_validation_clean | pass | 645 validation remains clean |
| V646_2_clock_pairs_source_backed | pass | clock delta_K rows are numeric and nonzero |
| V646_3_clock_rows_nonclaim | pass | clock rows remain nonclaim |
| V646_4_R2_repair_explicit | pass | R2 alpha notation trap is repaired |
| V646_5_projection_rows_blocked | pass | projection rows remain blocked |
| V646_6_runner_row_count | pass | symbolic runner covers two clock pairs times eight normalized factors |
| V646_7_runner_nonclaim | pass | finite runner rows remain nonclaim |
| V646_8_gates_block_numeric_score | pass | chiX and tau_clock gates block numeric scoring |
| V646_9_decisions_nonclaim | pass | decision rows do not claim pass |
| V646_10_summary_nonclaim | pass | summary stays nonclaim and records R2 repair |
| V646_11_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is a useful correction: the clock path is alive, but the previous R2 row cannot be used as a fine-structure-alpha bound.
- The real clock-alpha path now runs through frequency-ratio pairs with `delta_K_alpha` coefficients.
- Next, we need the MTS side of the bridge: `chi_X` and `tau_clock`; without them, the runner stays smoke-only.

## Nonclaim Summary

| status | R2_repaired | clock_alpha_sources_filled | symbolic_runner_rows | numeric_score_allowed | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_clock_alpha_sources_filled_R2_redshift_repaired_finite_runner_still_blocked_by_chiX_tau | true | true | 16 | false | chi_X/Xhat unit and tau_clock/time-potential map are still missing | 647-Y5-R10-derive-or-define-chiX-and-tau-clock-map.md |
