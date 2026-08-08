# 628 Y5 R10 real local bound input sources for cg or Zcg proof

Generated: 2026-06-06T02:15:20.281493+00:00  
Status: `Y5_R10_real_local_bound_sources_acquired_as_nonclaim_candidates_cg_and_Zcg_still_unsourced`  
Claim ceiling: `source_acquisition_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass`  
Next target: `629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md`

## Verdict
- 628 acquired real external source candidates for local bound inputs, but it did **not** find a source for `Z_cg=true` or a numeric/theorem-zero `c_g`.
- Eot-Wash 2020 is the right R10 primary source candidate. It gives a strong anchor, but not a machine-ready full `alpha_bound(lambda)` curve in this checkpoint.
- Cassini, LLR, atomic-clock, and MICROSCOPE sources are useful baseline candidates. They do not by themselves define `tau_PPN`, `tau_clock`, `tau_orbital`, or the MTS projection matrix.
- Therefore every row remains nonclaim and every local arena remains blocked.

## What Was Actually Acquired
```text
R10 source candidate: Eot-Wash 2020 PRL/arXiv
R10 anchor: alpha=1 excluded above lambda=38.6 micrometer, noncurve
PPN baseline candidate: Cassini gamma
Orbital/PPN baseline candidate: LLR 2018
Clock baseline candidate: Rosenband/NIST Al+/Hg+ clock ratio
WEP side candidate: MICROSCOPE final result
```

What was **not** acquired:

```text
Z_cg=true parent proof
c_g numeric/theorem-zero source
tau_R10/tau_PPN/tau_clock/tau_orbital projection model
K_X/Qbar_XH/lambda_X parent inputs
full alpha_bound(lambda) curve
```

## Local Source Register
| source_file | exists | role |
| --- | --- | --- |
| 627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md | True | immediate handoff: Z_cg false and c_g acquisition ledger |
| source-intake/mts_residuals/P8_Y5_BRR545_627_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_627_CG_ACQUISITION_LEDGER.csv | True | required c_g/local inputs |
| source-intake/mts_residuals/P8_Y5_R10_627_ARENA_BLOCKER_MATRIX.csv | True | arena blockers |
| source-intake/mts_residuals/P8_Y5_R10_627_SOURCE_REQUIREMENTS.csv | True | source requirements |
| 626-Y5-R10-quotient-invariant-matter-action-signature-or-cg-bound-input.md | True | descent criterion and c_g bound schema |
| 625-Y5-R10-no-representative-Weyl-disformal-coupling-or-cg-prior.md | True | representative Weyl/disformal source branch |
| scripts/Y5_R10_real_local_bound_input_sources_for_cg_or_Zcg_proof.py | True | this checkpoint generator |

## External Source Candidates
| source_id | arena | needed_input | title | authors_year | url | doi | extracted_value | extraction_method | source_confidence | source_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXT628_0_R10_EOTWASH_2020_PRL | R10 | alpha_bound_lambda | New Test of the Gravitational 1/r^2 Law at Separations down to 52 micrometers | Lee, Adelberger, Cook, Fleischer, Heckel 2020 | https://doi.org/10.1103/PhysRevLett.124.101101 | 10.1103/PhysRevLett.124.101101 | alpha=1 anchor: lambda < 38.6 micrometer at 95% confidence; separations 52 micrometer to 3.0 mm | abstract_anchor_only_not_full_curve | high_for_anchor_low_for_curve | source_candidate_anchor_only | false |
| EXT628_1_R10_EOTWASH_2020_ARXIV | R10 | alpha_bound_lambda | arXiv full text for Eot-Wash 2020 inverse-square-law test | Lee et al. 2020 | https://arxiv.org/abs/2002.11761 | 10.1103/PhysRevLett.124.101101 | candidate full-curve figure source; not digitized in this checkpoint | source_located_not_digitized | high_for_paper_low_for_machine_curve | full_curve_digitization_candidate | false |
| EXT628_2_PPN_CASSINI_2003 | PPN | tau_PPN_or_PPN_baseline | A test of general relativity using radio links with the Cassini spacecraft | Bertotti, Iess, Tortora 2003 | https://doi.org/10.1038/nature01997 | 10.1038/nature01997 | gamma - 1 = (2.1 +/- 2.3)e-5 | published_summary_value | high_for_PPN_baseline_not_tau_projection | baseline_candidate_not_cg_projection | false |
| EXT628_3_ORBITAL_LLR_2018 | orbital_PPN | tau_orbital_or_orbital_baseline | Relativistic tests with lunar laser ranging | Hofmann and Muller 2018 | https://doi.org/10.1088/1361-6382/aa8f7a | 10.1088/1361-6382/aa8f7a | Gdot/G=(7.1 +/- 7.6)e-14 yr^-1; beta-1=(-4.5 +/- 5.6)e-5; gamma-1=(-1.2 +/- 1.2)e-4 | abstract_values | high_for_orbital_baseline_not_tau_projection | baseline_candidate_not_cg_projection | false |
| EXT628_4_CLOCK_ROSENBAND_2008 | clock | tau_clock_or_clock_baseline | Frequency ratio of Al+ and Hg+ single-ion optical clocks; metrology at the 17th decimal place | Rosenband et al. 2008 | https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place | 10.1126/science.1154622 | alpha_dot/alpha=(1.4 +/- 1.7)e-17 yr^-1 preliminary constraint | NIST_publication_page | high_for_clock_constant_drift_not_tau_clock | baseline_candidate_not_cg_projection | false |
| EXT628_5_WEP_MICROSCOPE_2022 | WEP_side_constraint | composition_baseline_optional | MICROSCOPE Mission: Final Results of the Test of the Equivalence Principle | Touboul et al. 2022 | https://doi.org/10.1103/PhysRevLett.129.121102 | 10.1103/PhysRevLett.129.121102 | eta(Ti,Pt)=(-1.5 +/- 2.3 stat +/- 1.5 syst)e-15 | PubMed/arXiv summary value | high_for_WEP_baseline_not_cg_projection | side_constraint_candidate | false |

## Z_cg Source Audit
| audit_id | needed_proof | source_found | source_candidate | why_not_enough | Z_cg_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ZSRC628_0_parent_q | parent quotient map q:Phi_parent -> Q_MTS | false | local contracts only from 626/627 | contract rows do not construct q from parent action | unsigned | false |
| ZSRC628_1_verticality | v_X in ker(Dq) on local matter branch | false | conditional rows from 623-627 | conditional verticality is not a parent theorem | unsigned | false |
| ZSRC628_2_matter_descent | S_matter=Sbar[q(Phi),Psi,theta] | false | conditional descent criterion in 626 | criterion is not an action derivation | unsigned | false |
| ZSRC628_3_no_representative_frame | no representative Weyl/disformal coefficients | false | 625 exclusion lemma | exclusion depends on unsigned quotient-invariant matter action | unsigned | false |
| ZSRC628_4_total | Z_cg=true | false | none | zero proof remains local contract only | false | false |

## Acquisition Status
| input_id | parameter | source_status_after_628 | best_source_candidate | candidate_value | units | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRCACQ628_0_Z_cg | Z_cg | not_sourced | local parent proof still missing | false | boolean | parent proof unsigned | false |
| SRCACQ628_1_c_g | c_g | not_sourced | none; theory coefficient requires parent model or fit protocol | MISSING_PARENT_INPUT | dimensionless | no parent coefficient or empirical mapping | false |
| SRCACQ628_2_tau_R10 | tau_R10 | not_sourced | Eot-Wash material/source geometry, but projection model absent | MISSING_ARENA_PROJECTION | dimensionless | tau_R10 projection not derived | false |
| SRCACQ628_3_tau_PPN | tau_PPN | not_sourced | Cassini and LLR PPN baselines | MISSING_ARENA_PROJECTION | dimensionless | tau_PPN projection not derived | false |
| SRCACQ628_4_tau_clock | tau_clock | not_sourced | Rosenband/NIST clock constraint | MISSING_ARENA_PROJECTION | dimensionless | clock common-frame projection not derived | false |
| SRCACQ628_5_tau_orbital | tau_orbital | not_sourced | LLR orbital/PPN baseline | MISSING_ARENA_PROJECTION | dimensionless | orbital common-frame projection not derived | false |
| SRCACQ628_6_K_X | K_X | not_sourced | none in external experimental sources; parent kernel needed | MISSING_PARENT_INPUT | schema_required | parent kernel missing | false |
| SRCACQ628_7_Qbar_XH | Qbar_XH | not_sourced | none in external experimental sources; parent projection needed | MISSING_PARENT_INPUT | schema_required | parent projection missing | false |
| SRCACQ628_8_lambda_X | lambda_X | not_sourced | Eot-Wash constrains Yukawa lambda externally but does not define parent lambda_X | MISSING_PARENT_INPUT | length | parent range missing | false |
| SRCACQ628_9_alpha_bound_lambda | alpha_bound_lambda | anchor_candidate_only | Eot-Wash 2020 PRL/arXiv | alpha=1 excluded above lambda=38.6 micrometer; full curve not digitized | dimensionless_bound_vs_length | anchor-only non-curve and other local inputs missing | false |

## Nonclaim Numeric Anchors
| anchor_id | source_id | quantity | value | uncertainty | units | meaning | use_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ANCH628_0_R10_alpha1 | EXT628_0_R10_EOTWASH_2020_PRL | alpha_equal_1_lambda_limit | 38.6 | not_extracted | micrometer | gravitational-strength Yukawa interaction range limit at 95 percent confidence | anchor_only_non_curve | false |
| ANCH628_1_R10_min_separation | EXT628_0_R10_EOTWASH_2020_PRL | minimum_detector_attractor_separation | 52 | not_extracted | micrometer | experimental separation lower end | context_only | false |
| ANCH628_2_PPN_Cassini_gamma | EXT628_2_PPN_CASSINI_2003 | gamma_minus_one | 2.1e-5 | 2.3e-5 | dimensionless | Cassini PPN gamma baseline | baseline_not_tau_projection | false |
| ANCH628_3_LLR_gamma | EXT628_3_ORBITAL_LLR_2018 | gamma_minus_one | -1.2e-4 | 1.2e-4 | dimensionless | LLR PPN gamma baseline | baseline_not_tau_projection | false |
| ANCH628_4_CLOCK_alpha_dot | EXT628_4_CLOCK_ROSENBAND_2008 | alpha_dot_over_alpha | 1.4e-17 | 1.7e-17 | yr^-1 | clock constraint on temporal fine-structure variation | baseline_not_tau_clock | false |
| ANCH628_5_MICROSCOPE_eta | EXT628_5_WEP_MICROSCOPE_2022 | eta_Ti_Pt | -1.5e-15 | 2.3e-15_stat_1.5e-15_syst | dimensionless | WEP side constraint candidate | side_constraint_not_cg_projection | false |

## Arena Source Status
| arena_id | source_status | usable_now | blockers | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ARENA628_0_R10 | partial_anchor_found | false | full alpha_bound(lambda) curve not digitized; c_g,tau_R10,K_X,Qbar_XH,lambda_X missing | digitize/source R10 bound curve or keep alpha=1 anchor nonclaim | false |
| ARENA628_1_PPN | baseline_sources_found | false | tau_PPN, c_g, lambda_X/profile/M_PPN projection missing | derive PPN projection before scoring against Cassini/LLR | false |
| ARENA628_2_CLOCK | clock_baseline_source_found | false | tau_clock, c_g, environment profile and clock sensitivity mapping missing | derive common-frame clock projection or keep clock source as baseline only | false |
| ARENA628_3_ORBITAL | LLR_baseline_source_found | false | tau_orbital, c_g, lambda_X, source profile and orbital projection missing | derive orbital projection or use LLR only as future baseline | false |
| ARENA628_4_ZCG | not_found | false | parent quotient-invariant matter action proof absent | return to derivation if a parent action candidate is supplied | false |

## Decision
| decision_id | status | decision | meaning | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D628_0_main_verdict | Y5_R10_real_local_bound_sources_acquired_as_nonclaim_candidates_cg_and_Zcg_still_unsourced | real local bound source candidates acquired, but no c_g or Z_cg source found | external sources provide arena baselines/anchors, not the parent coefficient or projection needed for claims | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | false |
| D628_1_R10 | R10_anchor_found_full_curve_needed | use Eot-Wash 2020 as the R10 primary source candidate | alpha=1/lambda=38.6 micrometer is anchor-only; full alpha(lambda) curve still needs digitization/table extraction | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | false |
| D628_2_local_baselines | PPN_clock_orbital_baselines_found | record Cassini, LLR, Rosenband, and MICROSCOPE as baseline candidates | these are useful future comparators but not direct c_g projections | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | false |
| D628_3_claim_ceiling | source_acquisition_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass | no local claim | all candidate source rows remain nonclaim and arena rows remain blocked | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md | false |

## Route Update
| route_id | allowed_after_628 | forbidden_after_628 | next_action |
| --- | --- | --- | --- |
| RU628_0_allowed | cite external sources as candidate anchors/baselines | treat any source candidate as c_g or Z_cg proof | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md |
| RU628_1_allowed | digitize/source the Eot-Wash alpha(lambda) curve before R10 scoring | use alpha=1 anchor as a full bound curve | R10 curve digitization or source-backed table search |
| RU628_2_allowed | derive arena projection matrices before using PPN/clock/orbital baselines | compare c_g to Cassini/LLR/clocks without tau_A and profile model | build c_g projection smoke runner after R10 curve handling |

## Nonclaim Summary
| status | claim_ceiling | external_sources_found | Z_cg_sourced | c_g_sourced | alpha_bound_lambda_full_curve_sourced | alpha_bound_lambda_anchor_found | PPN_baseline_found | clock_baseline_found | orbital_baseline_found | R10_pass | WEP_pass | PPN_pass | clock_pass | orbital_pass | local_GR_pass | next_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_real_local_bound_sources_acquired_as_nonclaim_candidates_cg_and_Zcg_still_unsourced | source_acquisition_only_no_cg_zero_no_R10_WEP_PPN_clock_or_local_GR_pass | true | false | false | false | true | true | true | true | false | false | false | false | false | false | 629-Y5-R10-R10-bound-curve-digitization-or-cg-projection-smoke-runner.md |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V628_0_local_source_paths_exist | pass | missing=0 |
| V628_1_prior_627_clean | pass | prior_exists=True;prior_rows=9;prior_failures=0 |
| V628_2_external_sources_recorded | pass | external_rows=6;external_complete=True |
| V628_3_no_Zcg_or_cg_source_claim | pass | no_zcg=True;acquisition_safe=True |
| V628_4_R10_anchor_noncurve | pass | r10_anchor=True;anchors_nonclaim=True |
| V628_5_arenas_remain_blocked | pass | arena_rows=5;arenas_blocked=True |
| V628_6_all_claim_flags_false | pass | all_valid_for_claim_false=True |
| V628_7_no_local_claim | pass | Z_cg=false;c_g=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false |

## Practical Read
This is progress, but it is not evidence yet. We now have real source handles for the local tests, especially R10. The next clean technical move is to digitize or otherwise source the Eot-Wash `alpha_bound(lambda)` curve and build a nonclaim projection smoke runner. Until `c_g`, `tau_A`, `K_X`, `Qbar_XH`, and `lambda_X` are sourced or zero-derived, no local arena can pass.
