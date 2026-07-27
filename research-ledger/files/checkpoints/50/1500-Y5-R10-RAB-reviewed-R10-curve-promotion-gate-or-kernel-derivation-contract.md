# 1500 - Reviewed R10 Curve Promotion Gate or Kernel Derivation Contract

## Verdict
- The 1499 visual R10 points are not promoted to the live curve file.
- A concrete `delta_w -> alpha(lambda)` kernel contract is now written.
- The next physics target is derivational: map MTS local residuals into the R10 Yukawa convention or retain explicit closure variables.

## Curve Promotion Gate
| promotion_check_id | requirement | requirement_satisfied | promotion_effect |
| --- | --- | --- | --- |
| PROM1500_0_source_curve | source curve points are visual estimates, not reviewed digitization | False | BLOCKS_LIVE_CURVE_PROMOTION |
| PROM1500_1_machine_table | no machine-readable primary R10 alpha(lambda) table found | False | BLOCKS_LIVE_CURVE_PROMOTION |
| PROM1500_2_axis_review | axis calibration is visual/nonclaim and still requires review | False | BLOCKS_LIVE_CURVE_PROMOTION |
| PROM1500_3_curve_identity | Eot-Wash 2020 curve identity is plausible but not independently reviewed | False | BLOCKS_LIVE_CURVE_PROMOTION |
| PROM1500_4_kernel | delta_w-to-alpha projection kernel absent | False | BLOCKS_LIVE_CURVE_PROMOTION |
| PROM1500_5_live_target | live R10 curve target must remain absent | False | BLOCKS_LIVE_CURVE_PROMOTION |

## Equation Convention Register
| equation_id | equation | claim_status |
| --- | --- | --- |
| EQ1500_0_R10_bound_convention | V(r)=V_N(r)[1+alpha exp(-r/lambda)] | SOURCE_CONVENTION_NOT_MTS_PREDICTION |
| EQ1500_1_MTS_projection_target | alpha_MTS(lambda)=sum_a C_a * tau_R10_a(lambda) * delta_w_a | CONTRACT_ONLY_COEFFICIENTS_MISSING |
| EQ1500_2_R10_acceptance | |alpha_MTS(lambda_i)| <= alpha_bound(lambda_i) for every reviewed curve row i | NOT_EVALUABLE_YET |

## Kernel Contract
| kernel_input_id | required_input | owner | current_status |
| --- | --- | --- | --- |
| KERN1500_0_curve | reviewed alpha_bound(lambda) curve | empirical_bound | MISSING_LIVE_TARGET |
| KERN1500_1_delta_w_basis | delta_w component basis and units | MTS_residual_basis | MISSING |
| KERN1500_2_coefficients | component coupling coefficients C_a | parent_action_or_explicit_residual | MISSING_FORBIDDEN_IMPORT |
| KERN1500_3_geometry | R10 source/test geometry response tau_R10_a(lambda) | experimental_projection | MISSING |
| KERN1500_4_range_law | mapping between MTS local residual range and Yukawa lambda | theory_projection | MISSING |
| KERN1500_5_sign | absolute/plus/minus alpha convention | comparison_convention | CONTRACT_WRITTEN_NEEDS_REVIEW |
| KERN1500_6_output | computed alpha_MTS(lambda) rows | score_input | MISSING |

## Kernel Stub
| stub_id | stub_path | stub_rows | stub_status |
| --- | --- | --- | --- |
| STUB1500_0_kernel | source-intake\r10\derived\staging\R10_delta_w_kernel_contract_STUB_NONCLAIM_1500.csv | 9 | NONCLAIM_KERNEL_STRUCTURE_WRITTEN_WITH_MISSING_INPUTS |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1500_0_local_sources | PASS | all cited 1499/staged point paths exist |
| VAL1500_1_promotion_blocked | PASS | all curve-promotion requirements are unsatisfied |
| VAL1500_2_kernel_stub | PASS | kernel stub exists and remains nonclaim |
| VAL1500_3_live_targets_absent | PASS | live R10 curve/kernel targets remain absent |
| VAL1500_4_Cparent_refused | PASS | C_parent import was not performed |
| VAL1500_5_csv_parse | PASS | all generated 1500 CSVs parse cleanly |
| VAL1500_6_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1500_7_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1500_8_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1500_9_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1500_10_overall | PASS | 1500 refused curve promotion and wrote the delta_w-to-alpha kernel contract |

## Next Target
| next_id | next_target | script | objective |
| --- | --- | --- | --- |
| NEXT1500_0_1501 | 1501-Y5-R10-RAB-delta-w-to-yukawa-alpha-kernel-derivation-attempt.md | scripts/Y5_R10_RAB_delta_w_to_yukawa_alpha_kernel_derivation_attempt.py | attempt to derive the weak-field map from MTS local delta_w residuals to an effective Yukawa alpha(lambda); if derivation fails, retain explicit kernel closure variables |
