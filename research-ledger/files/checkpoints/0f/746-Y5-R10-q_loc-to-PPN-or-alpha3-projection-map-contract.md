# 746 - Y5 R10 q_loc To PPN Or alpha3 Projection Map Contract

Start point: 745 showed that a unit `c_qM` smoke row is not automatically safe or fatal. It depends entirely on which observable projection `q_loc` actually feeds.

Current result: **the projection map is now componentwise, and alpha3 momentum-flux is selected as the next highest-pressure target if that projection exists**.

The core rule is:

```text
q_loc^nu -> {delta_gamma_q, delta_beta_q, alpha1_q, alpha2_q, alpha3_q, xi_q, alpha_q(lambda)}
```

There is no legal single scalar pass. Beta/gamma remain interesting because the old compact-shell number is below their naive locks if the normalization matched. But alpha3 is the dragon: if `q_loc` has a momentum-flux/preferred-frame projection, the product must satisfy

```text
alpha3_q = W_q_alpha3 * epsilon_q_momentum
|alpha3_q| <= 4.0e-20
```

No such zero theorem or product row exists yet.

## Summary

| Field | Value |
| --- | --- |
| Status | `Y5_R10_746_q_loc_projection_map_contract_written_alpha3_pressure_selected_nonclaim` |
| Claim ceiling | `projection_map_contract_only_no_q_loc_PPN_alpha3_R10_pass_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass` |
| Main result | q_loc projection map contract written; alpha3 branch selected if momentum projection applies |
| Next target | `747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md` |

## Projection Contract

| contract_id | clause | mathematical_form | required_inputs | current_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QPC746_0_decompose_q_loc | q_loc must be decomposed before any PPN/alpha3/R10 comparison | q_loc^nu = q_T tau^nu + q_L n^nu + q_V^nu + q_TF^nu with channel-specific projectors | observed frame; tau/n split; spatial projector; domain/shell; units; source path | contract_written_components_unfilled | prevents scalar smoke from becoming all-channel evidence | false |
| QPC746_1_scalar_even_PPN | beta/gamma channels need scalar/even weak-field map | delta_beta_q or delta_gamma_q = W_even[q_T,q_L,q_TF] * q_proxy | weak-field Green operator; gauge; beta/gamma normalization; W_even coefficient | not_executable | old beta-smoke remains interesting but not claimable | false |
| QPC746_2_alpha3_momentum_flux | alpha3 applies only to momentum-flux/preferred-frame projection | alpha3_q = W_q_alpha3 * epsilon_q_momentum | q_loc momentum flux component; preferred-frame map; W_q_alpha3; source path; alpha3 bound | highest_pressure_if_nonzero | alpha3 is the most dangerous branch only if q_loc has this vector/flux projection | false |
| QPC746_3_R10_range | R10 applies only if q_loc supplies finite-range kernel | alpha_q(lambda)=c_q_alpha(lambda) * q_proxy | lambda; range kernel; real bound curve; c_q_alpha(lambda); no-range theorem or source | not_executable | R10 remains unscoreable without lambda/projection map | false |
| QPC746_4_no_single_scalar_pass | one c_qM scalar cannot decide PPN, alpha3, and R10 together | Delta_q = {delta_gamma_q, delta_beta_q, alpha_i_q, xi_q, alpha_q(lambda)} componentwise | separate coefficients and bounds per component; no cancellation | policy_active | all outputs remain nonclaim until component map is filled | false |

## Channel Router

| route_id | target | condition | known_pressure | current_result | missing | priority | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QCR746_0_beta_scalar_U2 | R4_beta | q_loc maps to O(U^2) scalar g00 coefficient with same beta normalization | unit smoke ratio to beta = 0.0952901533535509 | provisionally_below_if_same_normalization_but_conversion_missing | q_loc_U2_conversion_factor; A/B source equation; weak-field Green operator | medium_after_alpha3 | false |
| QCR746_1_gamma_slip | R3_gamma | q_loc sources spatial curvature slip or non-EH operator tail | unit smoke ratio to gamma = 0.323157911372912 | below_naive_lock_but_map_missing | spatial metric Green operator; gauge; slip coefficient | medium_after_alpha3 | false |
| QCR746_2_alpha3_momentum_flux | R7_alpha3 | q_loc has momentum nonconservation/preferred-frame flux projection | unit smoke ratio to alpha3 = 185815799039424 | highest_pressure_branch_if_projection_applies | W_q_alpha3; epsilon_q_momentum; theorem-zero of momentum flux or numeric product | highest | false |
| QCR746_3_xi_alpha2_preferred_location | R6_alpha2/R8_xi | q_loc carries domain/vector/preferred-location anisotropy | unit smoke above xi and alpha2 naive locks | danger_branch_if_anisotropy_projection_applies | domain/vector anisotropy coefficient; location potential map | high_after_alpha3 | false |
| QCR746_4_R10_range | R10_alpha_lambda | q_loc has finite-range/range-dependent source kernel | not scoreable without lambda | unrouted | lambda; c_q_alpha(lambda); real bound curve; range kernel | defer_until_range_kernel_exists | false |

## Alpha3 Momentum-Flux Gate

| gate_id | target | formula | current_status | blocker | acceptance | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| A3Q746_0_product_law | alpha3_q | alpha3_q = W_q_alpha3 * epsilon_q_momentum | product_law_written_inputs_missing | W_q_alpha3 and epsilon_q_momentum are not sourced; theorem-zero not proved | valid only if product is theorem-zero or numeric and \|alpha3_q\|<=4e-20 | false |
| A3Q746_1_zero_route | epsilon_q_momentum=0 | P_momentum q_loc = 0 or q_loc is purely scalar/even with no g0i/preferred-frame flux | not_derived | observed q_loc decomposition and parent Ward zero through O(U^2) missing | would remove alpha3 pressure for q_loc only, not other alpha3 channels | false |
| A3Q746_2_bound_route | numeric alpha3_q bound | \|W_q_alpha3 * epsilon_q_momentum\| <= 4.0e-20 | not_scoreable | numeric product missing; naive unit projection would exceed bound by huge factor if W=1 and epsilon=q_proxy | requires source-backed product, not q_proxy direct comparison | false |
| A3Q746_3_next | next target | derive zero of q_loc momentum flux or fill W_q_alpha3 epsilon_q_momentum product | selected | highest-pressure branch unresolved | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |

## PPN Scalar/Vector Gate

| gate_id | target | formula | current_status | known_pressure | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PPNQ746_0_beta | delta_beta_q | delta_beta_q = W_q_beta * q_proxy | conversion_missing | old QBU526 says below beta if same normalization | W_q_beta; source A/B equation; U2 conversion factor | false |
| PPNQ746_1_gamma | delta_gamma_q | delta_gamma_q = W_q_gamma * q_proxy | map_missing | unit smoke below gamma naive lock | spatial curvature slip map and gauge | false |
| PPNQ746_2_preferred_frame | alpha1/alpha2/alpha3/xi | Delta_pref_q = W_pref_q * q_proxy | highest_tightness_unresolved | alpha2/xi/alpha3 naive locks are much tighter than q_proxy | vector/preferred-frame decomposition | false |
| PPNQ746_3_envelope | componentwise PPN q_loc envelope | \|Delta_PPN_q\| <= {\|delta_gamma_q\|,\|delta_beta_q\|,\|alpha_i_q\|,\|xi_q\|} componentwise | not_run | no cancellation allowed | all W coefficients and component source rows | false |

## R10 Range Gate

| gate_id | target | formula | current_status | missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| R10Q746_0_range_kernel | alpha_q(lambda) | alpha_q(lambda)=c_q_alpha(lambda)*q_proxy | lambda_kernel_missing | lambda, kernel shape, source normalization, real bound curve comparison | false |
| R10Q746_1_no_range_zero | c_q_alpha(lambda)=0 | q_loc has no finite-range source kernel in compact local branch | not_derived | mass-gap/no-range theorem tied to q_loc, not just scalar memory | false |
| R10Q746_2_defer | R10 branch priority | defer until alpha3/preferred-frame projection is routed or killed | deferred_not_rejected | projection map and range kernel | false |

## Y5 Runner Update

| runner_id | source_row | status_after_746 | zero_or_input | still_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| Y5R746_q_loc_PPN | Y5B_8/Y5B_9/PPN524_7 | projection_contract_written_not_executable | component map required before beta/gamma/alpha_i/xi scoring | W_q_beta; W_q_gamma; W_q_alpha3; W_q_xi; component decomposition | false |
| Y5R746_alpha3 | R7_alpha3 | highest_pressure_branch_selected_if_momentum_projection_applies | alpha3_q = W_q_alpha3 * epsilon_q_momentum | momentum-flux zero theorem or numeric product <=4e-20 | false |
| Y5R746_R10 | R10_alpha_lambda | deferred_until_range_kernel_exists | alpha_q(lambda)=c_q_alpha(lambda)*q_proxy | lambda/range kernel and curve comparison | false |

## Decisions

| decision_id | decision | meaning | claim_status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D746_0_projection_contract | write componentwise q_loc projection contract | q_loc must be split before any PPN/alpha3/R10 comparison | contract_only | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |
| D746_1_beta_gamma | keep beta/gamma as lower-pressure but unresolved | unit smoke is below naive beta/gamma locks, but U2/slip conversion is missing | interesting_not_claim | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |
| D746_2_alpha3 | select alpha3 momentum-flux branch as next target | if q_loc has preferred-frame/momentum-flux projection, alpha3 is the tightest danger lock | highest_pressure_nonclaim | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |
| D746_3_R10 | defer R10 range branch | R10 cannot score until lambda/range kernel exists; alpha3 routing is more urgent | deferred_not_rejected | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |

## Route Update

| route_id | allowed_after_746 | forbidden_after_746 | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| RU746_0_allowed | say q_loc projection map is now componentwise | use one scalar smoke number as PPN/R10/alpha3 evidence | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |
| RU746_1_allowed | attack alpha3 by proving q_loc momentum-flux zero or filling W_q_alpha3 epsilon_q_momentum | claim alpha3 failure/pass from q_proxy alone | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |
| RU746_2_allowed | defer R10 until q_loc finite-range kernel exists | invent lambda from the compact-shell proxy | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 745_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\745-Y5-R10-c_qM-engineering-smoke-row-or-source-backed-Mref-hunt.md | true | true | immediate projection-map handoff | false |
| 745_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_745_VALIDATION.csv | true | true | prior validation guard | false |
| 745_locks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_745_NAIVE_LOCK_COMPARISON.csv | true | true | naive lock comparison forcing projection map | false |
| PPN_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PPN_RESIDUAL_VECTOR.csv | true | true | PPN residual vector with q_loc and alpha3 rows | false |
| PPN_metric_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv | true | true | metric expansion contract | false |
| PPN_gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PPN_SOURCE_STABILITY_GATES.csv | true | true | PPN promotion gates | false |
| beta_q_loc_gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BETA_QLOC_ACCEPTANCE_GATES.csv | true | true | beta/q_loc acceptance gates | false |
| beta_q_loc_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BETA_QLOC_DECISION.csv | true | true | beta provisional and alpha3 warning | false |
| q_loc_U2_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_QLOC_U2_BOUND.csv | true | true | older q_loc U2/beta/alpha3 smoke comparison | false |
| q_loc_transfer | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv | true | true | q_loc observable transfer map skeleton | false |
| alpha3_product_input | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ALPHA3_BOUND_PRODUCT_INPUT.csv | true | true | alpha3 product input template | false |
| alpha3_product_eval | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv | true | true | alpha3 product evaluator | false |
| q_loc_spec | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_QLOC_BOUND_RUNNER_SPEC.csv | true | true | q_loc bound runner spec | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V746_0_source_paths_exist | pass | source_rows=13 |
| V746_1_source_needles_present | pass | all source files contain expected evidence needles |
| V746_2_prior_745_clean | pass | 745 validation has no failures |
| V746_3_component_decomposition_required | pass | component decomposition contract written |
| V746_4_alpha3_product_law_written | pass | alpha3 product law written |
| V746_5_alpha3_selected_next | pass | alpha3 is highest pressure branch if projection applies |
| V746_6_beta_gamma_not_claimed | pass | beta/gamma gates remain nonclaim |
| V746_7_R10_deferred | pass | R10 deferred until range kernel exists |
| V746_8_no_single_scalar_policy | pass | single scalar c_qM cannot decide all observables |
| V746_9_Y5_rows_retained | pass | PPN/alpha3/R10 rows retained |
| V746_10_no_claim_rows_promoted | pass | all generated rows valid_for_claim=false |
| V746_11_next_target_selected | pass | 747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md |
| V746_12_outputs_scoped | pass | all outputs under post-checkpoint-work |
| V746_13_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V746_14_no_local_arena_claim | pass | R10/PPN/Newton/local-GR claims remain blocked |
| V746_15_validation_rows_ready | pass | validation table constructed |

## Plain-English Verdict

This gets us out of scalar fog. `q_loc` is not one number anymore; it has to pick a lane. If it lands in beta/gamma, the old smoke number is not terrifying, though still unclaimable. If it lands in alpha3/preferred-frame momentum flux, it is under the nastiest microscope in the whole local branch. So the best next attack is not R10 and not broad PPN: prove the `q_loc` momentum-flux projection is zero, or write the actual `W_q_alpha3 epsilon_q_momentum` product and face the bound.
