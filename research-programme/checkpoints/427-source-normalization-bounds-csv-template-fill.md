# 427 - Source-Normalization Bounds CSV Template Fill

Private source-intake checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 426 proved the runner-v4 dry-run machinery works. This checkpoint fills the actual `source-intake/local_bounds/local_bound_claims.csv` file with verified local-bound sources so evaluate mode can run.

The important discipline: these are bounds on possible residual channels, not predictions of MTS. They become tests of MTS only after we supply an MTS residual vector for `eta`, `gamma`, `beta`, `alpha_i`, `xi`, `Gdot/G`, fifth-force curves, and non-EH coefficients.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_bounds_csv_template_fill.py` |
| Run directory | `runs/20260602-092500-source-normalization-bounds-csv-template-fill` |
| Claims CSV | `source-intake/local_bounds/local_bound_claims.csv` |
| Status | `source_normalization_bounds_csv_template_fill_written_verified_local_bound_claims_csv_ready_for_evaluate_no_data_claim_no_local_GR_pass` |
| Claim ceiling | `verified_bounds_source_intake_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `427-local-bound-runner-v4-evaluate-smoke.md` |

## 3. Local Source Register

| source_file | exists | role |
| --- | --- | --- |
| 426-local-bound-runner-v4-dryrun-wrapper.md | True | source-intake and evaluate workflow contract |
| source-intake/local_bounds/local_bound_claims_TEMPLATE.csv | True | runner-v4 generated template and required schema |
| runs/20260602-091000-local-bound-runner-v4-dryrun-wrapper/results/schema_validation.csv | True | dry-run schema validation evidence |
| scripts/local_bound_runner_v4_real_data_interface.py | True | evaluate-mode schema and source-lock evaluator |
| runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_data_targets.csv | True | canonical R0-R11 local target map |

## 4. Verified External/Internal Sources

| source_id | source_type | used_for_rows | verification_status |
| --- | --- | --- | --- |
| MICROSCOPE_PRL_2022 | primary_PRL_arxiv | R0;R1 | web_verified |
| GALILEO_REDSHIFT_DELVA_PRL_2018 | primary_PRL_arxiv | R2 | web_verified |
| CASSINI_NATURE_2003 | primary_Nature | R3 | web_verified |
| WILL_LIVING_REVIEWS_2014_PPN_TABLE | review_Living_Reviews | R4;R5;R6;R7;R8 | web_verified |
| BISKUPEK_MULLER_TORRE_UNIVERSE_2021 | primary_LLR_article | R9 | web_verified |
| ADELBERGER_HECKEL_NELSON_2003_ISL | review_inverse_square_law | R10 | web_verified_symbolic |
| MTS_OPERATOR_LEDGER_425 | internal_retained_operator_ledger | R11 | local_verified_symbolic |

## 5. Claims CSV Rows

| row_id | dataset_id | observable | upper_bound | reference_note |
| --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | MICROSCOPE_final_TiPt | eta_WEP_direct_geometry | 2.8e-15 | MICROSCOPE Ti/Pt WEP result; maps only direct geometry/source test row, not a theorem-zero promotion |
| R1_WEP_source_charge | MICROSCOPE_final_TiPt_source_charge_proxy | eta_WEP_source_charge | 2.8e-15 | Uses same WEP source as direct proxy; full source-normalization R1 channel remains retained |
| R2_clock_redshift | Galileo_redshift_Delva_2018 | alpha_clock_redshift | 2.48e-05 | Galileo eccentric satellites redshift/LPI test; clock row only |
| R3_gamma | Cassini_Shapiro_gamma_2003 | gamma_minus_1 | 2.3e-05 | Cassini Shapiro/radio-link gamma result |
| R4_beta | Will_2014_PPN_beta_table | beta_minus_1 | 7.8e-05 | Will 2014 review reports beta-1=(-4.1 +/- 7.8)e-5 and Table 4 limit about 8e-5 |
| R5_alpha1 | Will_2014_PPN_alpha1_table | alpha1 | 1e-04 | Will Table 4 gives 1e-4 LLR and 4e-5 PSR J1738+0333; conservative solar-system-compatible row uses 1e-4 |
| R6_alpha2 | Will_2014_PPN_alpha2_table | alpha2 | 2e-09 | Will Table 4 alpha2 preferred-frame bound; strong-field caveat retained |
| R7_alpha3 | Will_2014_PPN_alpha3_table | alpha3 | 4e-20 | Will Table 4 alpha3 pulsar acceleration bound; ultratight exchange/flux lock |
| R8_xi | Will_2014_PPN_xi_table | xi | 4e-09 | Will Table 4 preferred-location xi bound; strong-field caveat retained |
| R9_Gdot | LLR_Biskupek_Muller_Torre_2021 | Gdot_over_G | 9.6e-15 | LLR result Gdot/G0=(-5.0 +/- 9.6)e-15 yr^-1 |
| R10_fifth_force | Adelberger_Heckel_Nelson_2003_ISL_curve | delta_G_or_fifth_force_yukawa | alpha(lambda) | Inverse-square law constraints are a curve in alpha(lambda); this row is intentionally symbolic and unscored |
| R11_EH_operator_ledger | MTS_EH_operator_retained_ledger_425 | non_EH_operator_coefficients | symbolic | Operator-family row is internal retained ledger, not an empirical pass |

## 6. Row Quality

| row_id | numeric_or_symbolic_policy | template_lock_match_or_symbolic | quality_status |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | numeric_evaluate_ready | True | pass |
| R1_WEP_source_charge | numeric_evaluate_ready | True | pass |
| R2_clock_redshift | numeric_evaluate_ready | False | review |
| R3_gamma | numeric_evaluate_ready | True | pass |
| R4_beta | numeric_evaluate_ready | True | pass |
| R5_alpha1 | numeric_evaluate_ready | False | review |
| R6_alpha2 | numeric_evaluate_ready | True | pass |
| R7_alpha3 | numeric_evaluate_ready | True | pass |
| R8_xi | numeric_evaluate_ready | True | pass |
| R9_Gdot | numeric_evaluate_ready | True | pass |
| R10_fifth_force | symbolic_deferred | True | pass |
| R11_EH_operator_ledger | symbolic_deferred | True | pass |

## 7. Symbolic Rows Deferred

| row_id | observable | upper_bound | reason_deferred | claim_policy |
| --- | --- | --- | --- | --- |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha(lambda) | requires range-dependent curve or operator-family coefficient ledger | no_symbolic_pass |
| R11_EH_operator_ledger | non_EH_operator_coefficients | symbolic | requires range-dependent curve or operator-family coefficient ledger | no_symbolic_pass |

## 8. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| local_source_paths_exist | pass | 0 missing local source paths |
| claims_csv_written | pass | research-programme\source-intake\local_bounds\local_bound_claims.csv |
| claims_row_count | pass | 12 rows |
| claims_rows_map_to_template | pass | all claim row IDs in template |
| references_verified_not_placeholders | pass | 0 missing/placeholder references |
| row_quality_passed | review | 2 rows need review |
| symbolic_rows_deferred | pass | 2 symbolic rows: R10 and R11 expected |
| MTS_residual_vector_loaded | not_run | bounds source-intake only; no MTS residual vector supplied |
| local_GR_promoted | fail | source intake is not WEP/EH/Newton/PPN/fifth-force proof |
| claim_ceiling_enforced | pass | verified_bounds_source_intake_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 9. Decision

Create a verified local_bound_claims.csv from primary/review sources for rows R0-R11, while explicitly preserving the symbolic fifth-force and non-EH-operator rows. This source-intake file is suitable for evaluate-mode smoke testing, but it is not evidence that MTS passes the local bounds because no MTS residual vector has been supplied yet.

Practical read: we now have a real source-intake file. The next move is the evaluate smoke. If that passes, the bottleneck becomes physics again: derive or estimate the actual MTS residual vector. That is where local GR either starts earning its keep or gets shoved back into closure-only.

## 10. Next Target

`427-local-bound-runner-v4-evaluate-smoke.md`
