# 948 Y5 R10: Clock/WEP Product-Bound Runner Or Constant-Superselection No-Marker Theorem

Status: `Y5_R10_948_product_bound_runners_written_constant_superselection_theorem_not_closed_nonclaim`

Claim ceiling: `clock_WEP_source_bounds_executable_only_no_zero_theorem_no_local_GR_claim`

## Result

This checkpoint took the 947 opening and made it sharper. The theorem route was attempted first: if ordinary constants/source weights are parent-signed superselection labels, then the chain-rule descent proof kills `b_A` and clock leakage cleanly.

That proof is valid only conditionally. The current corpus still permits the countermodel where the quotient metric descends but ordinary constants or source weights depend on a matter-visible marker. So the theorem does not close.

The useful win is practical: the clock and WEP source-side inequalities are now explicit nonclaim runners. They cannot score MTS yet, but when a future parent coefficient or zero theorem appears, these rows are ready to receive it.

```text
derive-zero route: clean but unsigned,
finite-product route: executable as source-side bound only,
no WEP/clock/local-GR claim promoted.
```

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 947_doc | handoff: source side improved but coefficient/projection handshake missing | true | true | 947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md |
| 947_validation | previous checkpoint validation | true | true | source-intake/mts_residuals/P8_Y5_BRR545_947_VALIDATION.csv |
| 947_next_target | 948 target selection | true | true | source-intake/mts_residuals/P8_Y5_R10_947_NEXT_TARGET.csv |
| 947_bound_interface | clock/WEP interface rows inherited from 947 | true | true | source-intake/mts_residuals/P8_Y5_R10_947_BOUND_INTERFACE_UPDATE.csv |
| 647_clock_product_bound | source-backed clock product bounds | true | true | source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv |
| 647_tau_clock_map | clock product-map definition | true | true | source-intake/mts_residuals/P8_Y5_R10_647_TAU_CLOCK_MAP.csv |
| 646_clock_alpha_sensitivity | clock alpha sensitivities | true | true | source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv |
| 766_clock_source_lock | clock source-lock and Galileo exclusion | true | true | source-intake/mts_residuals/P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv |
| 651_WEP_stress | WEP source-normalization stress bounds | true | true | source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv |
| 651_material_model | MICROSCOPE material model | true | true | source-intake/mts_residuals/P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv |
| no_species_contract | constant/source no-marker contract | true | true | source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv |
| 763_no_marker_spurion | no-marker/no-spurion theorem attempt | true | true | source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv |
| 633_matter_frame_cases | matter-frame candidate classification | true | true | source-intake/mts_residuals/P8_Y5_R10_633_MATTER_FRAME_CANDIDATE_CLASSIFICATION.csv |
| 631_source_charge_law | source/test charge law with quotient-zero branch | true | true | source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv |
| local_bounds | local WEP/clock empirical anchors | true | true | source-intake/local_bounds/local_bound_claims.csv |

## Constant-Superselection Theorem Attempt

| theorem_id | statement | proof_status | blocking_gap | counterexample_status | closes_zero |
| --- | --- | --- | --- | --- | --- |
| CST948_0_target | ordinary constants and source weights are selector-trivial superselection labels | target_identified | not yet parent-selected as an axiom/theorem of S_parent | legal_until_excluded | false |
| CST948_1_conditional_chain_rule | if S_matter descends through q and constants are external labels, vertical variations cannot change ordinary constants | valid_conditional_lemma | premises are stronger than the current parent corpus signs | counterexamples excluded only if premises are parent-signed | false |
| CST948_2_constant_sector | alpha_EM, charge normalization, and mass ratios do not depend on markers or quotient representatives | not_derived | species_internal_constants counterexample remains allowed by current sources | legal | false |
| CST948_3_source_weight | source normalization is species blind and does not carry a selector-dependent kappa_A | not_parent_signed | selector-blind measured-GM/source-current theorem missing | species-weighted source remains legal | false |
| CST948_4_countermodel | metric descent alone does not force constants or source weights to be marker-free | countermodel_blocks_unconditional_theorem | must forbid matter-visible marker dependence at parent-action level | legal_until_no_marker_parent_clause | false |
| CST948_5_total_verdict | constant-superselection/no-marker theorem sets b_A and clock product leakage to zero | not_closed_current_corpus | S0/S1/S2/S3/S4 plus NMS763 constant/source clauses remain unsigned | countermodel_retained | false |

## Clock Product-Bound Runner

| run_id | clock_pair | product_symbol | bound_1sigma_abs | bound_2sigma_abs | mts_prediction_abs | score_ready | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLK948_0_CAS646_0_AlHg | 27Al+ / 199Hg+ | kappa_alpha * tau_clock_time | 3.900000000000e-17 | 6.200000000000e-17 | MISSING_MTS_PRODUCT | false | BOUND_ONLY_NONCLAIM_STANDALONE_PRODUCT_MISSING |
| CLK948_1_CAS646_1_YbE3E2 | 171Yb+ E3 / 171Yb+ E2 | kappa_alpha * tau_clock_time | 2.100000000000e-18 | 3.200000000000e-18 | MISSING_MTS_PRODUCT | false | BOUND_ONLY_NONCLAIM_STANDALONE_PRODUCT_MISSING |

## WEP Product-Bound Runner

| run_id | channel | product_symbol | required_abs_product_max | score_rule | score_ready | verdict |
| --- | --- | --- | --- | --- | --- | --- |
| WEP948_0_WAS651_0_alpha_Coulomb | alpha/Coulomb composition channel | beta_source_normalized | 4.797780522732e-05 | \|beta_source_normalized\| <= required_abs_product_max for this channel | false | BOUND_ONLY_NONCLAIM_MTS_SOURCE_NORMALIZATION_MISSING |
| WEP948_1_WAS651_1_surface_binding | nuclear surface/binding composition channel | beta_source_normalized | 2.887280314062e-05 | \|beta_source_normalized\| <= required_abs_product_max for this channel | false | BOUND_ONLY_NONCLAIM_MTS_SOURCE_NORMALIZATION_MISSING |
| WEP948_2_WAS651_2_clock_screen_only | cross-arena rule diagnostic | not_applicable | not_applicable | clock screen alone is not a WEP source-force prediction | false | clock_screen_alone_is_not_a_WEP_pass_because_force_source_normalization_is_independent |

## Product-Bound Scoreboard

| score_id | arena | best_bound_statement | best_bound_value | mts_input_needed | can_score_now | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| PBS948_0_clock_product | clock alpha drift | Yb E3/E2 gives the strongest loaded product bound | 2.1e-18 | numeric kappa_alpha*tau_clock_time or theorem-zero constant sector | false | false |
| PBS948_1_WEP_product | MICROSCOPE/WEP source normalization | surface/binding diagnostic gives the tightest loaded beta_source cap | 2.887280314062e-05 | numeric source-normalized beta_source or theorem-zero species/source charge | false | false |
| PBS948_2_zero_theorem | constant-superselection/no-marker | if parent-signed, products are zero and local clock/WEP side constraints are automatically silent | NOT_DERIVED | parent-signed S0/S1/S2/S3/S4 plus no-marker clauses | false | false |

## Decision Ledger

| decision_id | topic | result | reason | next_action | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC948_0_theorem_attempt | constant-superselection/no-marker theorem | conditional_lemma_valid_but_not_parent_signed | the chain-rule zero proof works if constants/source weights are external selector-trivial labels, but current corpus still permits marker-dependent constants/source weights | try to parent-sign a constant-sector clause or keep finite source coefficients as explicit inputs | false |
| DEC948_1_clock_runner | clock product-bound runner | source_bound_executable_nonclaim | Al/Hg and Yb product bounds are source-backed, but standalone MTS product is missing | add candidate input schema for kappa_alpha*tau_clock_time or derive zero | false |
| DEC948_2_WEP_runner | WEP source-product runner | diagnostic_beta_caps_executable_nonclaim | MICROSCOPE stress rows produce explicit beta_source caps, but source normalization and MTS b_A are missing | derive source-normalization species-blind theorem or provide finite beta_source input | false |

## Claim Gate

| gate_id | claim | current_evidence | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- |
| CGATE948_0_constant_superselection | b_A and clock product leakage are theorem-zero | conditional lemma plus legal countermodel | false | false |
| CGATE948_1_clock_product_score | clock product bound passed by MTS | source bounds only | false | false |
| CGATE948_2_WEP_product_score | MICROSCOPE/WEP product bound passed by MTS | diagnostic beta caps only | false | false |
| CGATE948_3_local_GR | local GR/PPN/R10 branch passes | 948 improves clock/WEP side only; R10/PPN still blocked from 947 | false | false |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V948_0_sources_exist_and_needles | pass | all 948 source paths exist and needles are present | 2026-06-13T19:53:38.005798+00:00 |
| V948_1_prior_947_clean | pass | P8_Y5_BRR545_947_VALIDATION.csv clean | 2026-06-13T19:53:38.005811+00:00 |
| V948_2_theorem_not_closed | pass | constant-superselection total theorem remains unclosed | 2026-06-13T19:53:38.005814+00:00 |
| V948_3_countermodel_retained | pass | marker-dependent constant countermodel recorded | 2026-06-13T19:53:38.005817+00:00 |
| V948_4_clock_bounds_numeric | pass | clock product bounds are positive numeric rows | 2026-06-13T19:53:38.005819+00:00 |
| V948_5_clock_runner_nonclaim | pass | clock runner has no MTS product prediction | 2026-06-13T19:53:38.005822+00:00 |
| V948_6_WEP_caps_numeric | pass | WEP source-product caps are numeric or explicitly diagnostic-only | 2026-06-13T19:53:38.005824+00:00 |
| V948_7_WEP_runner_nonclaim | pass | WEP runner has no MTS source-normalized prediction | 2026-06-13T19:53:38.005827+00:00 |
| V948_8_scoreboard_nonclaim | pass | scoreboard can_score_now=false for every row | 2026-06-13T19:53:38.005829+00:00 |
| V948_9_decisions_nonclaim | pass | decision ledger remains nonclaim | 2026-06-13T19:53:38.005832+00:00 |
| V948_10_claim_gates_false | pass | all claim gates remain false | 2026-06-13T19:53:38.005834+00:00 |
| V948_11_next_target_selected | pass | 949 parent constant-sector or finite source coefficient target selected | 2026-06-13T19:53:38.005837+00:00 |
| V948_12_no_claims_promoted | pass | all generated rows are valid_for_claim=false | 2026-06-13T19:53:38.005839+00:00 |
| V948_13_formalization_workbench_untouched | pass | formalization_changed_after_start=0 | 2026-06-13T19:53:38.005843+00:00 |
| V948_14_validation_rows_ready | pass | validation table constructed | 2026-06-13T19:53:38.005845+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md | either parent-sign the constant/source no-marker clause that makes clock/WEP products theorem-zero, or create a finite candidate input schema for kappa_alpha*tau_clock_time and beta_source so the new product runners can score future MTS predictions | S0-S4 constant/source clauses, no-marker countermodel exclusion, clock product bound input, WEP beta_source cap input, nonclaim candidate schema | claiming local-GR, claiming WEP/clock pass from source-only bounds, GitHub action, formalization-workbench edits | false |
