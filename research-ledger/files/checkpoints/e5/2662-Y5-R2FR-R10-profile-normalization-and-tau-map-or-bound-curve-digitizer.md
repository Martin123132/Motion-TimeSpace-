# 2662 - R10 Profile Normalization And Tau Map Or Bound Curve Digitizer

## Purpose

This checkpoint derives the R10 profile/tau map far enough to stop treating `tau_R10` as a free knob. It also decides whether a full bound-curve digitizer should happen now or after the MTS-side projection factors are sourced.

## Result

- `tau_R10(lambda)` is now an explicit same-convention profile functional: `I_MTS_X/I_unit_Yukawa`.
- The point-pair Yukawa algebra is clean, but real R10 scoring needs the extended source/test geometry and readout convention.
- `tau_R10=1` is forbidden unless the same-kernel, same-charge, same-geometry, same-normalization and no-tail gates are all signed.
- Full external bound-curve digitization is deferred: without `K_X`, `Qbar_XH`, `c_g` and the tau/profile inputs, a full curve still cannot score MTS.

## Source Register

| source_id | role | path | exists | needles_required | missing_needles | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC2662_2661_doc | immediate handoff selecting R10 profile normalization and tau map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2661-Y5-R2FR-R10-projection-first-fill-or-visible-domain-source-signature.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_2660_doc | coupling vector R10 component and no-cancellation envelope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2660-Y5-R2FR-coupling-residual-vector-runner-or-visible-domain-signature-proof.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_947_doc | prior projection attempt showing tau_R10 and parent coefficients missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_1025_doc | alpha prefactor, Qbar_XH projection and coupling normalization gap | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_1048_doc | R10 source/test charge projection through alpha/mass/clock matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_563_doc | anchor-only noncurve data and symbolic MTS alpha blocker | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |
| SRC2662_437_doc | R10 alpha(lambda) executable curve contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\437-R10-alpha-lambda-executable-curve-contract.md | True | 3 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-23T04:20:54.983990+00:00 |

## Tau/Profile Derivation

| branch_id | derivation_id | object | statement | derived_form | status | missing_for_claim | score_ready | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_0_target | tau_R10(lambda) | tau_R10 is the same-convention map from the parent X-channel force kernel and source/test charge profiles into the empirical Yukawa alpha(lambda) convention. | alpha_R10(lambda)=K_X(lambda) Qbar_XH tau_R10(lambda) c_g + alpha_tail_abs(lambda) | TARGET_SHARP | source/test charge profiles, readout kernel, geometry convention, K_X, Qbar_XH, c_g and tail envelope | False | False | 2026-06-23T04:20:54.989072+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_1_point_kernel | point-source Yukawa normalization | For a parent scalar kernel G_X(r)=exp(-r/lambda)/(4*pi*Z_X*r), the point-pair force has the same radial Yukawa shape as the standard alpha(lambda) comparator. | alpha_point(lambda)=Q_source_X Q_test_X/(4*pi*Z_X*G_obs*M_source*M_test) under the same mass/charge normalization | EXACT_CONDITIONAL_KERNEL_FORM | source/test charges and Z_X/G_obs same-frame normalization | False | False | 2026-06-23T04:20:54.989072+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_2_extended_profile | extended source/test profile functional | For extended bodies, the point-pair kernel must be folded through the same source density, test density and readout weighting used by the experimental alpha(lambda) bound. | tau_R10(lambda)=I_MTS_X(lambda;rho_s,rho_t,W_readout)/I_unit_Yukawa(lambda;rho_s,rho_t,W_readout) | DERIVED_SYMBOLIC_PROFILE_FUNCTIONAL | rho_s, rho_t, W_readout, geometry/separation modulation and unit-Yukawa denominator | False | False | 2026-06-23T04:20:54.989072+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_3_bound_convention | external bound convention match | The alpha(lambda) bound is claim-usable only when the MTS projection is expressed in the same Yukawa potential and finite-geometry convention as the published bound curve. | alpha_MTS(lambda) is comparable iff force_law_form, lambda units, source/test normalization and geometry folding match the bound curve contract | CONVENTION_MATCH_REQUIRED | full claim-valid alpha(lambda) curve and experiment geometry convention | False | False | 2026-06-23T04:20:54.989072+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_4_tau_identity_conditions | tau_R10=1 shortcut | tau_R10=1 is allowed only in a signed point-pair/same-profile limit where MTS and the published unit-Yukawa kernel use identical source/test weighting and readout normalization. | tau_R10=1 iff I_MTS_X/I_unit_Yukawa=1 after Qbar and K_X normalization are already fixed | CONDITIONAL_IDENTITY_NOT_ACTIVE | identity conditions are not parent-signed or experiment-sourced | False | False | 2026-06-23T04:20:54.989072+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | TAU2662_5_verdict | R10 tau/profile map | The tau/profile map is derived as a symbolic functional, but no numeric or theorem-zero R10 projection is produced. | R10 projection remains nonclaim until the profile functional is evaluated or collapsed by signed identity conditions | TAU_R10_PROFILE_MAP_DERIVED_SYMBOLIC_NOT_NUMERIC | numeric geometry/source/test/readout inputs or parent-signed tau identity conditions | False | False | 2026-06-23T04:20:54.989072+00:00 |

## Tau Identity Gate

| branch_id | gate_id | condition | status | gate_pass | blocks_tau_one | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_0_same_kernel | MTS finite-range kernel exactly matches standard Yukawa kernel | CONDITIONAL_FORM_ONLY | False | True | False | 2026-06-23T04:20:54.989097+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_1_mass_proportional_charge | source/test X charge densities are proportional to the mass densities used by the bound convention | MISSING_SOURCE_TEST_CHARGE_NORMALIZATION | False | True | False | 2026-06-23T04:20:54.989097+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_2_same_geometry | same extended-body geometry and readout weighting as alpha(lambda) bound | MISSING_EXPERIMENT_GEOMETRY_TRANSFER | False | True | False | 2026-06-23T04:20:54.989097+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_3_same_normalization | K_X, Qbar_XH, c_g and G_obs normalization already fixed in the same frame | MISSING_PARENT_NORMALIZATION | False | True | False | 2026-06-23T04:20:54.989097+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_4_no_tail | alpha_tail_abs(lambda)=0 by theorem or source-backed negligible bound | MISSING_TAIL_ZERO_OR_BOUND | False | True | False | 2026-06-23T04:20:54.989097+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | ID2662_5_tau_one_verdict | tau_R10=1 may be used for claim scoring | TAU_ONE_SHORTCUT_FORBIDDEN | False | True | False | 2026-06-23T04:20:54.989097+00:00 |

## Profile Normalization Template

| branch_id | template_id | system_id | lambda_value | lambda_units | source_profile | test_profile | readout_kernel | unit_yukawa_denominator | mts_kernel_numerator | tau_R10_formula | K_X_formula | Qbar_XH_formula | c_g_status | tail_policy | score_ready | valid_for_claim | notes | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | PROF2662_0_R10_unit_yukawa | R10_source_test_profile | MISSING_LAMBDA_GRID | m | MISSING_RHO_SOURCE_AND_GEOMETRY | MISSING_RHO_TEST_AND_GEOMETRY | MISSING_W_READOUT | I_unit_Yukawa(lambda;rho_s,rho_t,W_readout) | I_MTS_X(lambda;rho_s,rho_t,W_readout) | I_MTS_X/I_unit_Yukawa | MISSING_K_X_OR_THEOREM_ZERO | MISSING_QBAR_XH_OR_THEOREM_ZERO | MISSING_C_G_OR_VISIBLE_DOMAIN_ZERO | absolute_tail_required_no_cancellation | False | False | Template only; evaluates the same-convention profile functional once real geometry/profile inputs exist. | 2026-06-23T04:20:54.989105+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | PROF2662_1_point_pair_limit | R10_point_pair_limit | MISSING_LAMBDA_GRID | m | point_source_only_if_bound_convention_matches | point_test_only_if_bound_convention_matches | ideal_pair_separation_r | exp(-r/lambda)/r | exp(-r/lambda)/(4*pi*Z_X*r) | 1 only after K_X/Qbar/c_g normalization absorbs 1/(4*pi*Z_X) and charge-to-mass ratios | MISSING_NORMALIZATION | MISSING_SOURCE_CHARGE | MISSING_C_G_OR_VISIBLE_DOMAIN_ZERO | absolute_tail_required_no_cancellation | False | False | Analytic limit for checking algebra, not a claim route for real R10 geometry. | 2026-06-23T04:20:54.989105+00:00 |

## Bound Curve Route Ledger

| branch_id | route_id | route | status | why | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | BCR2662_0_anchor_status | existing anchor rows | ANCHOR_ONLY_NONCLAIM | useful for smoke/unit checks but not a full alpha(lambda) curve | keep nonclaim | False | 2026-06-23T04:20:54.989113+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | BCR2662_1_full_curve | digitize/import full R10 alpha(lambda) curve | DEFER_UNTIL_PROFILE_MAP_HAS_INPUTS | a full curve still cannot score without tau_R10, K_X, Qbar_XH, c_g and tails | return after profile/source normalization rows exist | False | 2026-06-23T04:20:54.989113+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | BCR2662_2_claim_condition | claim-valid R10 comparison | BLOCKED | requires both MTS alpha(lambda) rows and bound rows with valid_for_claim=true | no R10 pass claim | False | 2026-06-23T04:20:54.989113+00:00 |

## Profile Runner Results

| branch_id | runner_id | template_id | has_missing_markers | score_ready | runner_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | RUN2662_yukawa | PROF2662_0_R10_unit_yukawa | True | False | REJECTED_MISSING_PROFILE_OR_NORMALIZATION | False | False | 2026-06-23T04:20:54.989120+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | RUN2662_limit | PROF2662_1_point_pair_limit | True | False | REJECTED_MISSING_PROFILE_OR_NORMALIZATION | False | False | 2026-06-23T04:20:54.989120+00:00 |

## Claim Gates

| branch_id | gate_id | requirement | current_status | evidence_ref | gate_pass | blocks_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | CG2662_0_tau_map | tau_R10 profile functional is numeric or theorem-collapsed | FAIL_SYMBOLIC_ONLY | TAU2662_5_verdict | False | True | False | 2026-06-23T04:20:54.989144+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | CG2662_1_tau_one | tau_R10=1 shortcut is legal | FAIL_TAU_ONE_SHORTCUT_FORBIDDEN | ID2662_5_tau_one_verdict | False | True | False | 2026-06-23T04:20:54.989144+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | CG2662_2_profile_inputs | R10 source/test/readout profile inputs exist | FAIL_PROFILE_INPUTS_MISSING | PROF2662 rows | False | True | False | 2026-06-23T04:20:54.989144+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | CG2662_3_bound_curve | claim-valid full alpha(lambda) bound curve exists | FAIL_FULL_CURVE_DEFERRED | BCR2662_1_full_curve | False | True | False | 2026-06-23T04:20:54.989144+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | CG2662_4_verdict | R10 projection can be scored or claimed | CLAIM_BLOCKED | symbolic tau map; missing profile inputs; anchor-only bound rows | False | True | False | 2026-06-23T04:20:54.989144+00:00 |

## Decision Ledger

| branch_id | decision_id | decision | reason | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | DEC2662_0_tau_status | tau_R10 is derived as a profile functional, not a number | the same-convention geometry/readout/source profiles are missing | source or derive Qbar/source-test profile normalization | False | False | 2026-06-23T04:20:54.989150+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | DEC2662_1_tau_one_policy | tau_R10=1 remains forbidden for claims | identity conditions are not parent-signed or experiment-sourced | use the profile functional or prove every identity condition | False | False | 2026-06-23T04:20:54.989150+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | DEC2662_2_bound_curve_policy | full bound curve digitization is useful but not first priority | MTS-side projection factors are still symbolic | fill source/test charge normalization and K_X/Qbar_XH before curve digitization | False | False | 2026-06-23T04:20:54.989150+00:00 |

## Next Target

| branch_id | next_id | status | next_doc | next_script | task | must_include | must_exclude | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | NEXT2662_0_selected | selected | 2663-Y5-R2FR-R10-source-test-charge-normalization-or-QbarXH-source-row.md | scripts/Y5_R2FR_R10_source_test_charge_normalization_or_QbarXH_source_row_2663.py | derive/source the source-test charge normalization feeding K_X(lambda), Qbar_XH and the tau_R10 profile functional | source density, test density, charge-to-mass normalization, Qbar_XH, K_X, Z_X/G_obs frame, visible-domain zero switch, no-cancellation tail policy | tau=1 shortcut, point-pair limit as real experiment, alpha=1 anchor as full curve, invented c_g or Qbar values, R10 pass claim, GitHub action, formalization-workbench edits | False | False | 2026-06-23T04:20:54.989158+00:00 |

## Project Status Snapshot

| branch_id | status_id | topic | status | detail | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | STAT2662_0_progress | R10 tau/profile | SYMBOLIC_FUNCTIONAL_DERIVED | tau_R10 is now an explicit same-convention profile functional, not a free knob | False | False | 2026-06-23T04:20:54.989162+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | STAT2662_1_claim | R10 claim status | BLOCKED_NONCLAIM | no numeric tau/profile factors or full claim-valid bound curve exist | False | False | 2026-06-23T04:20:54.989162+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | STAT2662_2_best_next | next route | SOURCE_TEST_CHARGE_NORMALIZATION | Qbar_XH/K_X/source-test normalization is the next useful MTS-side input | False | False | 2026-06-23T04:20:54.989162+00:00 |
| Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | STAT2662_3_project | local GR route | TEST_PIPELINE_TIGHTER_NOT_CLOSED | the R10 lane is becoming executable while the GR reduction claim remains blocked | False | False | 2026-06-23T04:20:54.989162+00:00 |

## Branch Copies

| copy_id | role | source | destination | exists | parseable_csv | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| COPY2662_queue | R10 profile/tau input queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_TAU_PROFILE_2662_PROFILE_NORMALIZATION_TEMPLATE_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2662_R10_PROFILE_TAU_INPUT_QUEUE_NONCLAIM.csv | True | True | False | 2026-06-23T04:20:54.995562+00:00 |
| COPY2662_local_bounds | R10 tau profile derivation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_TAU_PROFILE_2662_TAU_PROFILE_DERIVATION.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_tau_profile_map_2662_NONCLAIM.csv | True | True | False | 2026-06-23T04:20:54.995562+00:00 |
| COPY2662_source_weight | tau identity gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_TAU_PROFILE_2662_TAU_IDENTITY_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\R10_PROFILE_TAU_MAP_2662_NONCLAIM.csv | True | True | False | 2026-06-23T04:20:54.995562+00:00 |
| COPY2662_microscope | profile template copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_TAU_PROFILE_2662_PROFILE_NORMALIZATION_TEMPLATE_NONCLAIM.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_2662_R10_PROFILE_TEMPLATE.csv | True | True | False | 2026-06-23T04:20:54.995562+00:00 |
| COPY2662_quarantine | profile runner refusal results | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_TAU_PROFILE_2662_PROFILE_RUNNER_RESULTS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\quarantine\2662\P8_Y5_2662_PROFILE_RUNNER_RESULTS.csv | True | True | False | 2026-06-23T04:20:54.995562+00:00 |

## Validation

| timestamp_utc | checkpoint | branch_id | valid_for_claim | claim_allowed | validation_id | status | detail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_00_sources | PASS | all cited source paths exist and required needles are present |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_01_tau_functional | PASS | tau_R10 profile map is derived symbolically but not numeric |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_02_tau_one_guard | PASS | tau=1 shortcut is forbidden unless all identity gates close |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_03_template | PASS | profile templates are staged as nonclaim rows |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_04_runner_refuses | PASS | profile runner refuses missing inputs |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_05_bound_route | PASS | full bound curve is deferred until MTS-side profile factors exist |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_06_claim_gates_blocked | PASS | claim gates block R10 scoring |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_07_next_target | PASS | 2663 source/test charge normalization target selected |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_08_branch_copies | PASS | branch copies exist and parse |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_09_csv_parse | PASS | all generated CSVs parse cleanly |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_10_formalization_untouched | PASS | no 2662 outputs are written under formalization-workbench |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_11_pycache_absent | PASS | scripts __pycache__ absent |
| 2026-06-23T04:20:56.373065+00:00 | 2662 | Y5_R2FR_R10_PROFILE_TAU_MAP_2662 | False | False | VAL2662_OVERALL | PASS | 2662 derives a symbolic same-convention R10 tau/profile functional, forbids tau=1 shortcut, defers full curve digitization, and selects source-test charge normalization next |
