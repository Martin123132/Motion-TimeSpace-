# 3288 - Same-public-metric or ZQ impedance owner split under AX1090

## Summary

3288 separates two things that were getting tangled:

1. **Metric identification:** EM nonbirefringence/Hodge closure gives a conformal cone `[g_EM]`. It does **not** by itself prove the matter/clock/source metric `g_pub`.
2. **Scalar coupling:** the Maxwell impedance `Z_Q` does not need its numerical value derived immediately for local Maxwell/GR reduction, but it must be universal and vertical-silent: `L_v Z_Q=0`.

This is the fair standard. GR uses an empirical `G`; a first serious MTS local limit may also use calibrated constants. What it cannot do is let those constants drift with hidden variables, source composition, readout convention, or radiative threshold choices.

In four dimensions, the Hodge star on 2-forms is conformally invariant, so EM can fix the light cone while matter/clocks/rods fix the public coframe scale. Therefore the same-metric gate becomes:

`[g_EM]=[g_pub]` plus shared observed coframe `e_obs` for matter, clocks, rods, source current, and EM stress.

The scalar coupling gate becomes:

`Z_Q = C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout`

with no cancellation games. Constant calibrated pieces are weaker than derivation but not fatal; hidden/radiative/readout drift is fatal unless derived zero or bounded.

Selected residual envelope remains:

`|residual| <= 1.389797711495e-12`.

## Metric Identification Split
| metric_gate_id | object | statement | status |
| --- | --- | --- | --- |
| MGS3288_0_conformal_cone | EM cone metric | 3287 reconstructs only [g_EM] from nonbirefringent EM propagation; this is a conformal light-cone statement, not full matter metric ownership. | DERIVED_SPLIT |
| MGS3288_1_4D_Hodge_conformal_invariance | Hodge star on 2-forms | In four spacetime dimensions, the Hodge star acting on 2-forms is conformally invariant, so EM Hodge data can match the public cone without fixing the clock/rod conformal scale. | DERIVED_STANDARD_GEOMETRIC_FACT |
| MGS3288_2_public_metric_identity | same public metric | To use EM stress in the local GR source equation, require [g_EM]=[g_pub] plus the matter/clock/source coframe e_obs fixes the representative scale used in S_matter, clocks, rods, and Hilbert stress. | EXACT_CONDITIONAL_NOT_PARENT_SIGNED |
| MGS3288_3_bimetric_escape | metric split residual | If [g_EM] differs from [g_pub] or the scale/coframe is not shared, the branch becomes an optical-metric/source-frame residual rather than a local-GR pass. | LIVE_RESIDUAL_ROUTE |

## Z_Q Impedance Decomposition
| zq_id | piece | vertical_status | local_GR_role | prediction_role | status |
| --- | --- | --- | --- | --- | --- |
| ZQS3288_0_parent_piece | C_P N_Q | q-basic if C_P and N_Q are parent-fixed | acceptable calibrated coupling if universal and vertical-silent | does not by itself predict alpha value unless C_P,N_Q are derived numerically | CONDITIONAL_SUPPORT |
| ZQS3288_1_constant_lambda | lambda_A0 F_Q^2 | vertical-silent if truly constant and universal | can be absorbed into empirical Z_Q like GR absorbs empirical G; not fatal to local Maxwell/GR reduction | blocks a derived alpha value and weakens unification claim | ALLOWED_BUT_NOT_PREDICTIVE |
| ZQS3288_2_hidden_scalar | f_X(I_hid) F_Q^2 | not vertical-silent unless f_X is absent or constant on vertical fibres | dangerous: creates alpha/source fifth-force and readout drift | requires product-bound/source projection rows | LIVE_DANGEROUS_RESIDUAL |
| ZQS3288_3_radiative_readout | delta_lambda_rad + readout Hodge/hbar*c terms | not vertical-silent unless effective/readout functor is parent-closed | dangerous for measured clocks/spectra even if tree-level block is quiet | requires radiative/readout closure or empirical product bounds | LIVE_READOUT_RESIDUAL |
| ZQS3288_4_total | Z_Q = C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout | q-basic iff L_v Z_Q=0 for the whole sum without cancellation games | only q-basic universal Z_Q belongs in clean local Maxwell/GR limit | numeric value can be calibrated initially, but drift/universality cannot be assumed | SPLIT_CONTRACT |

## Local GR Relevance Table
| criterion_id | question | answer | reason | status |
| --- | --- | --- | --- | --- |
| LGR3288_0_value_vs_silence | must MTS derive the numerical value of Z_Q immediately? | no for local GR/Maxwell reduction; yes eventually for a stronger unification/prediction claim | GR uses empirical G, but local tests require constants to be universal and not hidden/environment drifting. | FAIR_CLAIM_STANDARD |
| LGR3288_1_metric_requirement | what metric condition is minimally needed? | [g_EM]=[g_pub] for light cones plus shared matter/clock/source coframe for the observed representative | EM nonbirefringence gives the cone; clocks/rods/matter fix the public scale used by source stress. | EXACT_CONDITIONAL |
| LGR3288_2_coupling_requirement | what Z_Q condition is minimally needed? | L_v Z_Q=0 and universal source/readout convention; numerical Z_Q may be calibrated at first pass | drifting or species/source-dependent Z_Q creates fifth-force/clock/WEP pressure; a constant empirical coupling does not. | EXACT_CONDITIONAL |
| LGR3288_3_no_cancellation | can hidden/radiative terms cancel to make L_v Z_Q=0? | not as a theorem; each nonparent term must be absent, q-basic, or separately bounded | cancellation between unrelated sectors would be a closure assumption and not robust under data splits. | NO_CANCELLATION_GUARD |

## Finite Residual Rows
| row_id | prediction | abs_bound | source_status | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SPL3288_0_clean_local_limit_conditional | 0 | 1.389797711495e-12 | THEOREM_CONDITIONAL_IF_SAME_CONE_COFRAME_AND_LVZQ_ZERO | PASS_NUMERIC_NONCLAIM | false |
| SPL3288_1_metric_split_residual | Pi_g[L_v([g_EM]-[g_pub]) + L_v(scale/coframe)]/N_g | 1.389797711495e-12 | MISSING_NUMERIC_METRIC_SPLIT_PROJECTION | REFUSE_MISSING_SOURCE_NONCLAIM | false |
| SPL3288_2_ZQ_drift_residual | L_v ln Z_Q = L_v ln(C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout) | 1.389797711495e-12 | MISSING_NUMERIC_ZQ_DRIFT_PROJECTION | REFUSE_MISSING_SOURCE_NONCLAIM | false |
| SPL3288_3_half_bound_smoke | 6.948988557475e-13 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |
| SPL3288_4_twice_bound_smoke | 2.779595422990e-12 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |

## Split Bound Runner
| row_id | prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SPL3288_0_clean_local_limit_conditional | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| SPL3288_1_metric_split_residual | Pi_g[L_v([g_EM]-[g_pub]) + L_v(scale/coframe)]/N_g | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| SPL3288_2_ZQ_drift_residual | L_v ln Z_Q = L_v ln(C_P N_Q + lambda_A0 + f_X + delta_lambda_rad + readout) | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| SPL3288_3_half_bound_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| SPL3288_4_twice_bound_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3288_0_metric_split_derived | true | false | same-public-metric split is refined into EM cone equality plus clock/matter coframe scale. |
| GATE3288_1_ZQ_value_vs_silence_split | true | false | constant calibrated Z_Q is separated from dangerous hidden/radiative/readout drift. |
| GATE3288_2_same_cone_coframe_signed | false | false | same cone/coframe theorem remains conditional in 1009/1012/1016. |
| GATE3288_3_LvZQ_zero_signed | false | false | Z_Q q-basic theorem remains unsigned because no-extra-F2/operator-domain/readout closure are not derived. |
| GATE3288_4_numeric_residual_sourced | false | false | no numeric metric-split or Z_Q-drift projection row exists. |
| GATE3288_5_no_claim | true | false | no local-GR/Maxwell/alpha/PPN/clock claim is allowed from this split. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3288_0_fair_constant_standard | A calibrated constant Z_Q is not fatal to local GR/Maxwell reduction. | this matches how GR handles G: the first requirement is universality and vertical silence, not immediate numerical derivation. | false |
| DEC3288_1_real_coupling_danger | Hidden/radiative/readout drift in Z_Q remains fatal unless derived zero or bounded. | the coupling bottleneck is now precise: L_v Z_Q and source/readout universality, not aesthetic dislike of constants. | false |
| DEC3288_2_metric_path | EM Hodge reconstruction only fixes the cone; local GR needs shared coframe/scale with matter and clocks. | prevents overclaiming from EM waves while preserving the useful Poynting/Hodge route. | false |
| DEC3288_3_next_work | Next target should try the q-basic Z_Q theorem as vertical silence, not alpha-value derivation. | it is the least costly coupling win: prove no drift/universality first, leave exact alpha value as later stronger target. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3288_0_3289 | 3289-Y5-R2FR-qbasic-ZQ-vertical-silence-or-alpha-product-residual-under-AX1090.md | Try to prove L_v Z_Q=0 as a universality/vertical-silence theorem without deriving the numerical alpha value: separate constant calibrated pieces from hidden, source-dependent, radiative, and readout pieces; if the theorem fails, retain a source-ready alpha/Z_Q product residual. | Do not require numerical alpha derivation for local-GR reduction, but do not allow hidden drift, species/source dependence, radiative readout leakage, or cancellation between pieces. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3288_0_sources_exist | all cited source paths exist | true |  |
| VAL3288_1_sources_parse | all cited source paths parse | true |  |
| VAL3288_2_outputs_parse | all 3288 non-validation output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3288_3_metric_conformal_split_present | metric table separates conformal cone and coframe scale | true |  |
| VAL3288_4_ZQ_value_vs_drift_present | Z_Q table separates calibrated constants from dangerous drift | true |  |
| VAL3288_5_local_GR_fair_standard_present | local GR relevance table allows calibrated value but requires silence | true |  |
| VAL3288_6_residual_rows_refuse_missing_sources | metric split and Z_Q drift residual rows refuse missing numeric projections | true |  |
| VAL3288_7_runner_expectations | split runner expectations all match | true | SPL3288_0_clean_local_limit_conditional=PASS_NUMERIC_NONCLAIM;SPL3288_1_metric_split_residual=REFUSE_MISSING_SOURCE_NONCLAIM;SPL3288_2_ZQ_drift_residual=REFUSE_MISSING_SOURCE_NONCLAIM;SPL3288_3_half_bound_smoke=PASS_NUMERIC_NONCLAIM;SPL3288_4_twice_bound_smoke=FAIL_BOUND |
| VAL3288_8_claim_gates_false | no 3288 gate allows local-GR/alpha/Maxwell claim | true |  |
| VAL3288_9_next_target_focused | next target focuses q-basic Z_Q vertical silence | true |  |
| VAL3288_10_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3288_11_overall | 3288 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T16:45:32.110036+00:00
