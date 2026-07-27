# 981 Y5 R10: Finite Coupling Prior Source Acquisition b_kappa Gdot alpha3

Status: `Y5_R10_981_source_backed_observational_anchors_acquired_nonclaim_projection_maps_missing`

Claim ceiling: source acquisition only. No `b_kappa` bound, no `K_boundary_alpha3` bound, no `qbar` pass, no WEP/PPN/local-GR pass, and no public claim.

## Readout

After 980, continuous constants cannot honestly be theorem-zeroed by the no-marker functor route. 981 therefore hardens the first finite local coupling anchors from external sources, while keeping every row nonclaim until the projection from observation to MTS coefficient is derived.

The key caution is alpha3: the tight `4.0e-20` number is a strong-field pulsar `alpha3_hat` bound, not automatically the weak-field local PPN boundary coefficient. The weak-field solar-system alpha3 bound is much weaker but context-closer. Both are retained separately.

## Local Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 980_doc | handoff: no-marker theorem failed globally and finite coupling priors are needed | true | true | 980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md |
| 980_fallback | local finite-prior fallback rows | true | true | source-intake/mts_residuals/P8_Y5_R10_980_FINITE_PRIOR_FALLBACK.csv |
| 979_prior_priority | earlier coupling-prior source priority | true | true | source-intake/mts_residuals/P8_Y5_R10_979_QBAR_PRIOR_SOURCE_PRIORITY.csv |
| 417_boundary | local alpha3/Gdot anchor rows needing source hardening | true | true | 417-boundary-exchange-nohair-theorem-attempt.md |

## Web Source Ledger

| web_source_id | title | year | url | doi_or_journal | extracted_quantity | value | units | confidence_or_note | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WEB981_0_MICROSCOPE_WEP | MICROSCOPE mission: final results of the test of the Equivalence Principle | 2022 | https://arxiv.org/abs/2209.15487 | Phys. Rev. Lett. 129, 121102; DOI https://doi.org/10.1103/PhysRevLett.129.121102 | eta(Ti,Pt) | -1.5e-15 | dimensionless | 1 sigma statistical and systematic errors reported separately; use only as WEP/source-splitting anchor | false |
| WEB981_1_LLR_GDOT | Benefit of New High-Precision LLR Data for the Determination of Relativistic Parameters | 2021 | https://arxiv.org/abs/2012.12032 | Universe 7(2), 34; DOI https://doi.org/10.3390/universe7020034 | Gdot/G0 | -5.0e-15 | yr^-1 | reported uncertainty; local 417 anchor appears to use 9.6e-15 yr^-1 as an uncertainty-scale bound | false |
| WEB981_2_ALPHA3_STRONG_PULSAR | Discovery of Three Wide-orbit Binary Pulsars: Implications for Binary Evolution and Equivalence Principles | 2005 | https://arxiv.org/abs/astro-ph/0506188 | Astrophysical Journal source via arXiv | strong-field alpha3_hat upper limit | 4.0e-20 | dimensionless | 95 percent upper limit on alpha3_hat; not automatically identical to weak-field local PPN alpha3 | false |
| WEB981_3_ALPHA3_WEAK_SOLAR | Orbital motions and the conservation-law/preferred-frame alpha3 parameter | 2014 | https://arxiv.org/abs/1309.7149 | Galaxies 2(4), 482-495; DOI https://doi.org/10.3390/galaxies2040482 | weak-field alpha3 upper estimate | 6.0e-10 | dimensionless | preliminary weak-field bound using supplementary perihelion precessions; less tight than pulsar alpha3_hat but closer to local PPN context | false |

## Candidate Coupling Priors

| prior_id | component | observable_channel | source_id | candidate_value | candidate_units | candidate_convention | MTS_projection_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CP981_0_b_kappa_species_split_WEP | b_kappa | WEP/source-composition | WEB981_0_MICROSCOPE_WEP | 6.992e-15 | dimensionless | rough \|central\|+2*sqrt(stat^2+syst^2) screening envelope from eta(Ti,Pt); not a derived MTS coefficient | MISSING_SOURCE_CHARGE_PROJECTION | false |
| CP981_1_kappa_running_Gdot | b_kappa | Gdot/orbital/local-time drift | WEB981_1_LLR_GDOT | 2.420e-14 | yr^-1 | rough \|central\|+2*sigma screening envelope from LLR Gdot/G0; not an MTS drift profile | MISSING_ENVIRONMENT_PROFILE_AND_XHAT_TIME_MAP | false |
| CP981_2_alpha3_strong_pulsar | boundary_alpha3_flux | strong-field pulsar preferred-frame/conservation-law | WEB981_2_ALPHA3_STRONG_PULSAR | 4.000e-20 | dimensionless | 95 percent upper limit on alpha3_hat; keep separate from local weak-field alpha3 | MISSING_STRONG_TO_LOCAL_PPN_PROJECTION | false |
| CP981_3_alpha3_weak_solar | boundary_alpha3_flux | weak-field solar-system preferred-frame | WEB981_3_ALPHA3_WEAK_SOLAR | 6.000e-10 | dimensionless | preliminary weak-field bound; useful as context but much weaker than pulsar alpha3_hat | MISSING_BOUNDARY_ALPHA3_PROJECTION_MATRIX | false |

## Local Anchor Reconciliation

| anchor_id | local_anchor | web_source_match | reconciliation | action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LAR981_0_417_Gdot | 417 Gdot_drift = 9.600e-15 yr^-1 | WEB981_1_LLR_GDOT reports uncertainty 9.6e-15 yr^-1 around central -5.0e-15 yr^-1 | local row appears to store the 1 sigma uncertainty scale, not a conservative absolute bound | replace claim language with convention-labelled screening envelope before scoring | false |
| LAR981_1_417_alpha3 | 417 alpha3_flux = 4.000e-20 dimensionless | WEB981_2_ALPHA3_STRONG_PULSAR gives alpha3_hat 95 percent upper limit 4.0e-20 | source is strong-field pulsar alpha3_hat; not automatically a weak-field local boundary alpha3 coefficient | keep separate from weak-field solar alpha3 and require projection before use | false |
| LAR981_2_WEP_source_split | 979/980 b_kappa species_source_weight_splitting needs external bound | WEB981_0_MICROSCOPE_WEP gives Ti/Pt Eotvos result at 10^-15 scale | good first WEP anchor, but maps to b_kappa only through composition/source-charge sensitivity matrix | source composition sensitivities or derive universal Hilbert source before scoring | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CGATE981_0_source_provenance | external source rows have usable provenance | true | false | provenance exists, but MTS coefficient projection is missing |
| CGATE981_1_numeric_MTS_priors | candidate values are valid MTS priors | false | false | candidate values are observational anchors, not projected MTS coefficient bounds |
| CGATE981_2_b_kappa_bound | b_kappa species/source splitting is bounded | false | false | composition/source-charge projection matrix is missing |
| CGATE981_3_alpha3_bound | K_boundary_alpha3 is bounded for MTS local branch | false | false | strong-field alpha3_hat and weak-field alpha3 need separate projection conventions |
| CGATE981_4_local_GR | R10/WEP/PPN/local-GR branch passes | false | false | source acquisition only; no runner scoring or parent derivation |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC981_0_source_acquisition | finite coupling priors | source_backed_observational_anchors_acquired | MICROSCOPE, LLR Gdot, pulsar alpha3_hat, and solar alpha3 sources are recorded | derive projection maps from observational anchors to MTS residual coefficients |
| DEC981_1_alpha3_policy | alpha3 | split_strong_and_weak_alpha3 | 4e-20 is strong-field alpha3_hat; weak-field solar-system alpha3 is much weaker but context-closer | do not use pulsar alpha3_hat as local PPN prior without a projection argument |
| DEC981_2_Gdot_policy | Gdot | local_anchor_relabel_needed | 417's 9.6e-15 yr^-1 matches the LLR uncertainty scale, not a full conservative absolute envelope | store both central value and chosen envelope convention before any scoring |
| DEC981_3_best_next | next checkpoint | projection_matrix_or_screening_runner | we now have source anchors; the blocker is mapping them into b_kappa, K_boundary_alpha3, and local residual vector components | write 982 coupling-bound projection matrix skeleton and nonclaim screening runner |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V981_0_local_sources | pass | local handoff/source anchors exist and needles are found | 2026-06-14T01:35:49.847941+00:00 |
| V981_1_web_source_urls | pass | web source URLs and DOI/journal strings are recorded | 2026-06-14T01:35:49.847952+00:00 |
| V981_2_web_values_numeric | pass | web source extracted values parse as numeric | 2026-06-14T01:35:49.847956+00:00 |
| V981_3_units_recognized | pass | all web source units are recognized | 2026-06-14T01:35:49.847958+00:00 |
| V981_4_web_sources_nonclaim | pass | all web source rows remain valid_for_claim=false | 2026-06-14T01:35:49.847961+00:00 |
| V981_5_candidate_priors_nonclaim | pass | candidate priors are blocked nonclaim rows | 2026-06-14T01:35:49.847963+00:00 |
| V981_6_projection_missing | pass | every candidate prior still requires an MTS projection map | 2026-06-14T01:35:49.847966+00:00 |
| V981_7_anchor_reconciliation_nonclaim | pass | local anchor reconciliations remain nonclaim | 2026-06-14T01:35:49.847968+00:00 |
| V981_8_claim_gates_safe | pass | claim gates do not allow local-GR or coefficient-bound claims | 2026-06-14T01:35:49.847970+00:00 |
| V981_9_decision_next_target | pass | 982 projection matrix/screening runner selected | 2026-06-14T01:35:49.847973+00:00 |
| V981_10_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T01:35:49.847975+00:00 |
| V981_11_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T01:35:49.847977+00:00 |
| V981_READY | pass | 981 checkpoint pack validation summary | 2026-06-14T01:35:49.847980+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 982-Y5-R10-coupling-bound-projection-matrix-skeleton-and-screening-runner.md | map WEP/Gdot/alpha3 observational anchors into explicit MTS residual coefficient slots without claiming a pass | composition/source-charge projection placeholders, Gdot-to-Xhat environment map, strong-vs-weak alpha3 split, screening-only runner | local-GR pass, theorem-zero promotion, invented projection coefficients, GitHub action, formalization-workbench edits | false |
