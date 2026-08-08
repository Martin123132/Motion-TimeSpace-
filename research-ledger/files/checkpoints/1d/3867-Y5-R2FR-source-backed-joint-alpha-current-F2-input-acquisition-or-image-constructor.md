# 3867 — Source-Backed Joint Alpha / Current / F2 Input Acquisition Or Image Constructor

Generated: `2026-07-01T05:55:30+00:00`

## Purpose

3866 made the joint runner executable:

`b_alpha_X = 2 z_g - s_XF2`

`|s_XF2 tau_A| <= |b_alpha_X tau_A| + 2|z_g tau_A|`

3867 stops treating the missing inputs as vibes. It imports the strongest local source-backed rows we currently have, separates external evidence from MTS-side prediction inputs, and decides the next derivation gate.

## Source Register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC3867_00_3866_theorem | source-intake\mts_residuals\P8_Y5_R2FR_3866_JOINT_RUNNER_THEOREM.csv | True | True | 3866 handoff: runner executable, needs inputs or image constructor |
| SRC3867_01_3866_schema | source-intake\mts_residuals\P8_Y5_R2FR_3866_JOINT_INPUT_SCHEMA.csv | True | True | required z_g_tau input schema |
| SRC3867_02_3866_results | source-intake\mts_residuals\P8_Y5_R2FR_3866_DRYRUN_RESULTS.csv | True | True | alpha-only dryrun block |
| SRC3867_03_3866_next | source-intake\mts_residuals\P8_Y5_R2FR_3866_NEXT_TARGET.csv | True | True | declared 3867 target |
| SRC3867_04_3866_validation | source-intake\mts_residuals\P8_Y5_BRR545_3866_VALIDATION.csv | True | True | previous validation pass |
| SRC3867_05_clock_bound | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv | True | True | best current clock alpha product bound |
| SRC3867_06_wep_projection | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv | True | True | MICROSCOPE alpha/Coulomb projection |
| SRC3867_07_r10_projection | source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv | True | True | R10 alpha product-law projection |
| SRC3867_08_zg_components | source-intake\mts_residuals\P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv | True | True | z_g component decomposition and identity |
| SRC3867_09_zg_zero | source-intake\mts_residuals\P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv | True | True | z_g zero theorem verdict |
| SRC3867_10_balpha_template | source-intake\mts_residuals\P8_Y5_R2FR_3118_BALPHA_PRODUCT_INPUTS_TEMPLATE.csv | True | True | b_alpha product input template |
| SRC3867_11_image_exhaustion | source-intake\mts_residuals\P8_Y5_R2FR_2766_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv | True | True | visible image exhaustion verdict |
| SRC3867_12_no_hom | source-intake\mts_residuals\P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv | True | True | typed no-hidden-visible-hom conditional theorem |
| SRC3867_13_f2_counterterms | source-intake\mts_residuals\P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv | True | True | surviving hidden scalar F2 counterterm |

## Source-Backed Input Schema

| schema_id | field | owner | requirement | current_status |
| --- | --- | --- | --- | --- |
| SCHEMA3867_0 | external_bound | external experiment/source | required for scoring | clock and WEP partial; R10 curve not promoted |
| SCHEMA3867_1 | tau_A | MTS projection/readout | required for scoring | missing except absorbed clock product form |
| SCHEMA3867_2 | b_alpha_tau | MTS alpha drift/source coefficient | required for scoring | template only |
| SCHEMA3867_3 | z_g_tau | MTS current normalization | required for scoring | missing and not zero-proved |
| SCHEMA3867_4 | s_XF2_tau | MTS F2 coefficient | optional if inferred from identity; required for direct score | missing |
| SCHEMA3867_5 | projection_consistency | domain matching | required for scoring | missing |
| SCHEMA3867_6 | image_constructor_certificate | parent action | alternative to numeric scoring | conditional only |

## Acquisition Status

| status_id | arena | input_class | status | usable_now | missing_for_claim |
| --- | --- | --- | --- | --- | --- |
| ACQ3867_0_clock_bound | clock | external_bound | SOURCE_BACKED_AVAILABLE | True | MTS b_alpha_tau_clock; z_g_tau_clock; s_XF2_tau_clock or parent image theorem; clock readout normalization |
| ACQ3867_1_wep_projection | MICROSCOPE_WEP | external_bound_and_material_alpha_projection | SOURCE_BACKED_PARTIAL | True | beta_source_alpha theorem/prior; tau_WEP; shared domain rule; full material model; z_g_tau_WEP; s_XF2_tau_WEP |
| ACQ3867_2_r10_projection | R10_short_range | product_law_projection | FORMULA_ONLY_NONCLAIM | False | lambda_X; Z_X; K_X(lambda); beta_s; beta_t; epsilon_tail; promoted alpha_bound(lambda) curve; z_g_tau_R10; s_XF2_tau_R10 |
| ACQ3867_3_zg_components | all_local_arenas | MTS_current_normalization | DECOMPOSITION_AVAILABLE_VALUES_MISSING | False | z_Qstar; z_lattice,A; z_Noether,A; z_cA_post,A; z_readout,A; source-arena extensions |
| ACQ3867_4_parent_image | parent_visible_operator_domain | alternative_exact_derivation | CONDITIONAL_UNSIGNED | False | quotient exactness/fullness; no hidden-visible Hom signed by parent; radiative/readout stability; boundary/local projection silence |

## Candidate Rows

| candidate_id | arena | external_status | external_bound_value | b_alpha_tau | z_g_tau | s_XF2_tau | runner_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CAND3867_0_clock_alpha_product | clock | SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE | 2.1e-18 | MISSING_BALPHA_TIMES_TAU_CLOCK | MISSING_ZG_TIMES_TAU_CLOCK | MISSING_SXF2_TIMES_TAU_CLOCK | BLOCKED_EXTERNAL_BOUND_AVAILABLE_MTS_JOINT_INPUTS_MISSING |
| CAND3867_1_wep_alpha_coulomb | MICROSCOPE_WEP | SOURCE_BACKED_WEP_BOUND_PARTIAL_ALPHA_PROJECTION | 2.8e-15 | MISSING_BETA_SOURCE_ALPHA_TIMES_BALPHA_TIMES_TAU_WEP | MISSING_ZG_TIMES_TAU_WEP | MISSING_SXF2_TIMES_TAU_WEP | BLOCKED_MISSING_SOURCE_PROJECTION_AND_ZG_SXF2 |
| CAND3867_2_r10_product_law | R10_short_range | PRODUCT_LAW_ONLY_NONCLAIM | MISSING_VALID_ALPHA_BOUND_CURVE | MISSING_KX_BETA_SOURCE_BETA_TEST_TAIL | MISSING_ZG_TIMES_TAU_R10 | MISSING_SXF2_TIMES_TAU_R10 | BLOCKED_R10_PROFILE_BETA_BOUND_CURVE_AND_ZG_SXF2_MISSING |
| CAND3867_3_zg_decomposition | all_local_arenas | MTS_COMPONENT_DECOMPOSITION_IMPORTED | not_external_bound | linked_by_identity | MISSING_COMPONENT_VALUES_OR_ZERO_PROOF | linked_by_identity | BLOCKED_ZG_ZERO_OR_BOUND_NOT_PROVED |
| CAND3867_4_parent_image_constructor | parent_visible_operator_domain | CONDITIONAL_THEOREM_IMPORTED | not_numeric_route | zero_if_image_constructor_closes | zero_if_current_owner_closes | zero_if_no_extra_F2_image_closes | BLOCKED_PARENT_IMAGE_CONSTRUCTOR_UNSIGNED |
| CAND3867_5_hidden_F2_counterterm | visible_EM | LEGAL_IF_NO_HOM_UNSIGNED | counterexample_not_bound | can_be_reopened_by_hidden_F2 | separate_current_normalization_still_live | MISSING_OR_ALLOWED_COUNTERTERM | BLOCKED_HIDDEN_SCALAR_F2_COUNTERTERM_NOT_EXCLUDED |

## Runner Reevaluation

| reeval_id | arena | external_bound_positive | missing_mts_joint_inputs | verdict | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| RUN3867_0_clock_alpha_product | clock | True | True | BLOCKED_SOURCE_BOUND_READY_MTS_SIDE_MISSING | False |
| RUN3867_1_wep_alpha_coulomb | MICROSCOPE_WEP | True | True | BLOCKED_SOURCE_BOUND_READY_MTS_SIDE_MISSING | False |
| RUN3867_2_r10_product_law | R10_short_range | False | True | BLOCKED_R10_PROFILE_BETA_BOUND_CURVE_AND_ZG_SXF2_MISSING | False |
| RUN3867_3_zg_decomposition | all_local_arenas | False | True | BLOCKED_ZG_ZERO_OR_BOUND_NOT_PROVED | False |
| RUN3867_4_parent_image_constructor | parent_visible_operator_domain | False | False | BLOCKED_THEOREM_ROUTE_UNSIGNED | False |
| RUN3867_5_hidden_F2_counterterm | visible_EM | False | True | BLOCKED_COUNTERTERM_ROUTE_STILL_OPEN | False |

## Image Constructor Audit

| audit_id | clause | status | source_row | next_action |
| --- | --- | --- | --- | --- |
| IMG3867_0_parent_generator_category | ParentGenerate[Phi,q_obs,Dq,F_parent,theta_rep,topology,e_obs] category exists | PARTIAL_CONTRACT | VOE2766_1_parent_generator_domain | turn contract into explicit functor/domain object |
| IMG3867_1_quotient_exactness_fullness | visible quotient functor is exact/full enough to exhaust coefficient objects | UNSIGNED | VOE2766_2_quotient_functor_exactness | prove no extra Coeff(O_vis) object appears after quotient |
| IMG3867_2_no_hidden_visible_hom | Hom(C_hid,Coeff(F_Q^2)) absent/constant | CONDITIONAL_NOT_PARENT_SIGNED | ODT2659_1_exact_typed_theorem | make typed-domain exclusion a parent theorem, not closure |
| IMG3867_3_no_independent_F2 | no independent visible Coeff(F_Q^2) | OPEN_COUNTERTERM | CT1057_1_hidden_scalar | kill hidden scalar F2 and radiative/readout reentry |
| IMG3867_4_radiative_readout_stability | effective/readout action stays in parent image | UNSIGNED | VOE2766_4_radiative_readout_closure | prove loops/apparatus maps cannot generate extra visible coefficients |
| IMG3867_5_boundary_projection_silence | boundary/local projection does not generate visible coefficient tails | UNSIGNED | VOE2766_5_boundary_projection_silence | derive or keep as explicit closure |
| IMG3867_6_current_normalization_owner | z_g current normalization is parent-owned/zero or bounded | UNSIGNED | ZG3680_7_verdict | next gate: z_g component zero proof or source-backed values |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3867_0_sources | PASS | False | source register resolves all imported ledgers |
| GATE3867_1_clock_external_bound | PASS | False | ACB1052_2 imported as nonclaim product bound |
| GATE3867_2_wep_external_bound | PASS | False | AWP1052_0 imported as nonclaim partial projection |
| GATE3867_3_r10_valid_curve | BLOCKED | False | RAP1052_0 is product law only; no promoted bound curve/coefficient rows |
| GATE3867_4_mts_joint_inputs | BLOCKED | False | all scored arenas still miss MTS-side joint products |
| GATE3867_5_zg_zero_or_bound | BLOCKED | False | 3680 says z_g=0 not proved and component values missing |
| GATE3867_6_image_constructor | BLOCKED | False | image route still conditional/unsigned |
| GATE3867_7_no_claim_leak | PASS | False | nonclaim discipline preserved |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3867_0 | 3867 imports real clock/WEP source-backed rows but keeps them nonclaim | we have usable evidence plumbing without pretending MTS predictions exist |
| DEC3867_1 | the next mathematical target is z_g, not another generic audit | go after z_Qstar, z_lattice, z_Noether, z_cA_post and z_readout zero/bound clauses directly |
| DEC3867_2 | R10 remains bound-curve/coefficient blocked | do not spend more tokens scoring R10 until alpha_bound(lambda), K_X, beta_s and beta_t are source-backed |
| DEC3867_3 | hidden F2 counterterm is the active counterexample to no-extra-F2 | prove no hidden-visible Hom/trivial hidden invariant algebra or retain explicit closure |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3867_0 | 3868-Y5-R2FR-zg-component-zero-proof-or-source-backed-current-normalization-inputs.md | derive or source the z_g component products z_Qstar, z_lattice, z_Noether, z_cA_post and z_readout in one local arena before any alpha/F2 claim | 3867 shows external clock/WEP evidence is available, but the runner blocks because z_g is neither zeroed nor bounded; z_g is the coupling/current-normalization bottleneck |

## Bottom Line

This is progress, not a retreat: clock and WEP now have source-backed external rows wired into the joint runner, and the runner correctly refuses to promote them because the missing piece is the MTS-side current/coupling normalization, especially `z_g`.

The next best move is therefore not another broad audit. It is a narrow strike on `z_g`: prove or bound the component law for `z_Qstar`, `z_lattice`, `z_Noether`, `z_cA_post`, and `z_readout` in one arena.
