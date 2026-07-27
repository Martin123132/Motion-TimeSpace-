# 1244-Y5-R10-QR-statistical-policy-and-GM-convention-pack

**Current verdict:** 1244 fills the non-theory prerequisites for future finite `q_R_hat` scoring: GM/source convention and a strict one-sigma nonclaim gamma policy. It still does **not** supply `q_R_hat`.

**Main progress:** future `q_R_hat` rows now have a declared normalization and pass policy. The strict smoke guardrail is `abs(q_R_hat) <= 4.6e-5`, derived from `gamma_minus_1_QR=-q_R_hat/2` and `sigma_gamma=2.3e-5`.

**No-claim guard:** no `Q_R=0`, finite `Q_R` pass, PPN pass, local-GR pass, WEP/R10 pass, or public source-coupling claim is promoted.

Generated UTC: 2026-06-15T08:17:34.160172+00:00

## Source Register
| source_id | local_path | needle | purpose | absolute_path | path_exists | needle_found | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1244_0_1243_next | source-intake/mts_residuals/P8_Y5_R10_1243_NEXT_TARGET.csv | NEXT1243_0_1244 | 1243 handoff to GM convention and statistical policy pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1243_NEXT_TARGET.csv | True | True | False | False |
| SRC1244_1_1243_hunt | source-intake/mts_residuals/P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv | HUNT1243_2_GM_policy | GM policy source-hunt row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv | True | True | False | False |
| SRC1244_2_1243_stat | source-intake/mts_residuals/P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv | HUNT1243_3_statistical_policy | statistical policy source-hunt row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1243_SOURCE_HUNT_LEDGER.csv | True | True | False | False |
| SRC1244_3_1240_bound | source-intake/mts_residuals/P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | QB1240_3_pass_rule | pass-rule schema requiring N_sigma and uncertainty policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_BOUND_INPUT_SCHEMA.csv | True | True | False | False |
| SRC1244_4_1240_map | source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | QMAP1240_2_dimensionless_qR | q_R_hat normalization | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv | True | True | False | False |
| SRC1244_5_1240_comparator | source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv | COMP1240_0_gamma_Cassini | Cassini gamma comparator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv | True | True | False | False |
| SRC1244_6_1181_source | source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv | SRC1181W_0_Cassini_gamma | Cassini gamma provenance and uncertainty | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv | True | True | False | False |

## GM Convention Pack
| convention_id | quantity | convention | required_future_row | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| GM1244_0_qR_definition | q_R_hat | q_R_hat = Q_R c^2/(G M_source) | finite q_R_hat candidates must declare whether they supply q_R_hat directly or raw Q_R plus G M_source | CONVENTION_DECLARED_NONCLAIM | False | False |
| GM1244_1_source_body | M_source | for Cassini gamma comparator rows, the default source body is the solar-system central mass used by the cited gamma analysis; future rows must name the source body explicitly | source_body=Sun or explicit alternative with reason | CONVENTION_DECLARED_NONCLAIM | False | False |
| GM1244_2_measured_GM | G M_source | use measured/dynamical GM from the same weak-field comparator convention; do not infer GM from MTS q_R fitting | GM_source_value or directly_dimensionless_q_R_hat plus provenance | CONVENTION_DECLARED_SOURCE_STILL_REQUIRED_FOR_RAW_QR | False | False |
| GM1244_3_coordinate | r and U | weak-field map assumes areal-radial matching and U=GM/r in the same convention used by QMAP1240 | coordinate_convention=areal_radial_weak_field or explicit mapping correction | CONVENTION_DECLARED_NONCLAIM | False | False |

## PPN Gamma Statistical Policy
| policy_id | policy_name | observable | central_value | sigma | N_sigma | pass_rule | use | source | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| STAT1244_0_default_smoke | strict_one_sigma_nonclaim_smoke | gamma_minus_1 | 2.1e-5 | 2.3e-5 | 1 | abs(gamma_minus_1_QR) <= 1 * 2.3e-5 | strict smoke/refusal policy only; not a discovery or publication criterion | source-intake/mts_residuals/P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv:SRC1181W_0_Cassini_gamma | False | False |
| STAT1244_1_center_handling | residual_about_GR_zero | gamma_minus_1_QR | 0 expected for closure GR baseline; observed central value is recorded but not fitted | 2.3e-5 | 1 | compare finite residual magnitude to uncertainty guardrail, not to a fitted offset | prevents using the observed central offset as an MTS fit target | source-intake/mts_residuals/P8_Y5_R10_1240_PPN_COMPARATOR_LEDGER.csv:COMP1240_0_gamma_Cassini | False | False |
| STAT1244_2_alt_policy | looser_two_or_three_sigma | gamma_minus_1 | 2.1e-5 | 2.3e-5 | 2_or_3_only_if_explicitly_labelled | allowed only as sensitivity branch, never replacing strict smoke | future robustness/sensitivity branch | same comparator; branch must be labelled separately | False | False |

## QR Bound Derivation Nonclaim
| derive_id | input | policy | result | numeric_guardrail | units | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QBD1244_0_projection | gamma_minus_1_QR = -q_R_hat/2 | strict_one_sigma_nonclaim_smoke | abs(q_R_hat) <= 2*N_sigma*sigma_gamma | 4.6e-05 | dimensionless | NONCLAIM_GUARDRAIL_DERIVED_FROM_SCHEMA | False | False |
| QBD1244_1_missing_qR | q_R_hat | strict_one_sigma_nonclaim_smoke | q_R_hat value remains missing | MISSING_QR_VALUE | dimensionless | NO_NUMERIC_MTS_SCORE | False | False |

## Runner Policy Feed
| feed_id | target_runner | N_sigma | sigma_gamma | q_R_hat_abs_guardrail | GM_convention_status | q_R_hat_status | feed_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RPF1244_0_policy | 1241 Q_R nonclaim smoke runner | 1 | 2.3e-5 | 4.6e-05 | DECLARED_CONTRACT_ONLY | MISSING_QR_VALUE_UNCHANGED | POLICY_READY_QR_VALUE_MISSING | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1244_0_policy_filled | fill N_sigma/sigma_gamma policy for future smoke runner | 1241 refused numeric q_R_hat rows without statistical policy | future finite q_R_hat rows can now be rejected for value/source rather than missing policy | False | False |
| DEC1244_1_GM_convention_filled | declare GM/source convention requirements | q_R_hat normalization is meaningless without source mass convention | future finite rows must name source body and GM provenance or provide directly dimensionless q_R_hat | False | False |
| DEC1244_2_qR_still_missing | do not fabricate q_R_hat | 1244 only fills policy and convention prerequisites | feed policy into smoke runner while keeping q_R_hat missing | False | False |

## Claim Gates
| gate_id | claim | status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE1244_0_policy | nonclaim statistical policy exists | PASS_NONCLAIM | strict one-sigma smoke policy and guardrail are declared | False | False |
| GATE1244_1_GM_convention | GM convention contract exists | PASS_NONCLAIM | q_R_hat normalization and future source-body/GM requirements are declared | False | False |
| GATE1244_2_qR_value | q_R_hat value exists | BLOCKED | runner policy feed keeps q_R_hat_status=MISSING_QR_VALUE_UNCHANGED | False | False |
| GATE1244_3_local_GR | local GR/Newton pass | BLOCKED | policy/convention plumbing is not a Q_R theorem or finite value | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not_do | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1244_0_1245 | 1245-Y5-R10-PPN-QR-policy-fed-smoke-runner-and-source-hunt-update.md | scripts/Y5_R10_PPN_QR_policy_fed_smoke_runner_and_source_hunt_update.py | feed the 1244 statistical policy and GM convention into the 1241 Q_R smoke runner, verify the only remaining refusal is missing q_R_hat/source theorem, and update the source-hunt ledger | runner no longer fails for missing policy, still refuses missing q_R_hat, and no local-GR/PPN claim is promoted | do not fabricate q_R_hat, do not run long jobs, and do not claim local GR | False | False |

## Validation
| check_id | check | status | details | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| VAL1244_0_sources_exist | all cited local sources exist | PASS | 7/7 sources exist | False | False |
| VAL1244_1_needles_found | all cited local needles found | PASS | 7/7 needles found | False | False |
| VAL1244_2_GM_convention | GM/source convention rows are declared | PASS | gm_rows=4 | False | False |
| VAL1244_3_stat_policy | strict one-sigma nonclaim policy is declared | PASS | N_sigma=1 sigma_gamma=2.3e-5 | False | False |
| VAL1244_4_q_bound | q_R_hat guardrail derives from gamma schema | PASS | abs(q_R_hat)<=4.6e-5 strict smoke guardrail | False | False |
| VAL1244_5_qR_missing | q_R_hat remains missing | PASS | MISSING_QR_VALUE_UNCHANGED | False | False |
| VAL1244_6_claim_gates | claim gates remain blocked/nonclaim | PASS | claim_gate_rows=4 | False | False |
| VAL1244_7_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables | False | False |
| VAL1244_8_next_target_1245 | next target is policy-fed Q_R smoke runner | PASS | 1245-Y5-R10-PPN-QR-policy-fed-smoke-runner-and-source-hunt-update.md | False | False |
| VAL1244_9_csv_parse | all generated CSVs parse cleanly | PASS | P8_Y5_R10_1244_SOURCE_REGISTER.csv:7; P8_Y5_R10_1244_GM_CONVENTION_PACK.csv:4; P8_Y5_R10_1244_PPN_GAMMA_STATISTICAL_POLICY.csv:3; P8_Y5_R10_1244_QR_BOUND_DERIVATION_NONCLAIM.csv:2; P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv:1; P8_Y5_R10_1244_DECISION_LEDGER.csv:3; P8_Y5_R10_1244_CLAIM_GATES.csv:4; P8_Y5_R10_1244_NEXT_TARGET.csv:1 | False | False |
| VAL1244_10_formalization_untouched | formalization-workbench untouched during run | PASS | formalization_recent_write_count_since_run_start=0 | False | False |
| VAL1244_11_overall | overall 1244 validation | PASS | 1244 declares GM convention and nonclaim PPN gamma statistical policy while leaving q_R_hat missing | False | False |
