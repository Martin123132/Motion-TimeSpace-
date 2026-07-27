# 1341-Y5-R10-RAB-R2FR-scalar-mode-zero-theorem-or-source-backed-bound-row

**Current verdict:** 1341 does not derive the `R2/fR` scalar-mode zero theorem. The second-order filter is clean, but MTS has not parent-signed the no-extra-scalar/no-integrated-out-curvature-tower premises.

**Main progress:** the finite scalar branch is now source-backed but nonclaim: Lee 2020 supplies an anchor-only R10 Yukawa source, Capozziello/Stabile supply f(R) Yukawa/PPN theory sources, and Cassini supplies a PPN source candidate. The runner still rejects every row because the MTS coefficient, full alpha(lambda) curve, and regime map are missing.

**Decision:** next target is `1342`: either close the integrated-out R2/fR tower loophole, or acquire/digitize the full source-backed R10 alpha(lambda) curve before any finite scalar scoring.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1341_0_1340_next | source-intake/mts_residuals/P8_Y5_R10_1340_NEXT_TARGET.csv | NEXT1340_0_1341 | True | True | selected 1341 target | False | False |
| SRC1341_1_1340_schema | source-intake/mts_residuals/P8_Y5_R10_1340_R11_EXECUTABLE_INPUT_SCHEMA.csv | R11SCHEMA1340_1_R2FR | True | True | R2/fR executable schema | False | False |
| SRC1341_2_1340_template | source-intake/mts_residuals/P8_Y5_R10_1340_R11_EXECUTABLE_INPUT_TEMPLATE.csv | R11IN1340_0_R2FR_prediction_required | True | True | R2/fR prediction template | False | False |
| SRC1341_3_1340_validation | source-intake/mts_residuals/P8_Y5_BRR545_1340_VALIDATION.csv | VAL1340_11_overall | True | True | 1340 pass gate | False | False |
| SRC1341_4_960_zero_attempt | source-intake/mts_residuals/P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv | R2FR960_4_verdict | True | True | R2/fR zero-or-bound attempt | False | False |
| SRC1341_5_963_derivative_audit | source-intake/mts_residuals/P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv | DO963_6_verdict | True | True | derivative-order audit | False | False |
| SRC1341_6_963_runner_spec | source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv | R2RUN963_4_decision_logic | True | True | R2/fR runner spec | False | False |
| SRC1341_7_964_minimality | source-intake/mts_residuals/P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv | MIN964_5_verdict | True | True | minimality theorem attempt | False | False |
| SRC1341_8_964_template | source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv | R2IN964_2_Lee2020_anchor | True | True | existing R2/fR nonclaim input template | False | False |
| SRC1341_9_964_runner | source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv | R2RUN964_VERDICT | True | True | existing strict nonclaim runner | False | False |
| SRC1341_10_965_primitive | source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv | PQ965_5_verdict | True | True | primitive quotient theorem attempt | False | False |

## Web Source Ledger
| web_id | url | source_type | source_note | use_in_1341 | extraction_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WEB1341_0_Lee2020_R10 | https://arxiv.org/abs/2002.11761 | short-range inverse-square/Yukawa bound | arXiv abstract gives gravitational-strength Yukawa range limit below 38.6 micrometres at 95 percent confidence | anchor-only R10 scalar-mode bound row | ANCHOR_ONLY_NON_CURVE | False | False |
| WEB1341_1_Capozziello2009_fR_Newtonian | https://arxiv.org/abs/0901.0448 | f(R) Newtonian-limit theory source | arXiv abstract states analytic metric f(R) models generally give Yukawa-like corrections and only f(R)=R recovers the standard Newtonian potential | conceptual source for R2/fR scalar-mode/Yukawa residual | THEORY_SOURCE_NOT_NUMERIC_BOUND | False | False |
| WEB1341_2_Stabile2010_fR_PPN | https://arxiv.org/abs/1004.1973 | f(R) post-Newtonian source | arXiv abstract states f(R) PN solutions include Yukawa/oscillating corrections and converge to GR when f tends to R | PPN map/source requirement for finite scalar branch | THEORY_SOURCE_NOT_NUMERIC_BOUND | False | False |
| WEB1341_3_Cassini_gamma | https://pubmed.ncbi.nlm.nih.gov/14508481/ | PPN gamma experimental source | PubMed record identifies Bertotti, Iess, Tortora Nature 2003, DOI 10.1038/nature01997 | PPN gamma source candidate; exact numeric row remains nonclaim until formula/regime map is complete | SOURCE_STRING_RECORDED_PPN_MAP_MISSING | False | False |

## R2FR Zero Theorem Attempt
| attempt_id | claim | formal_move | result | gap | promotion_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R2ZERO1341_0_target | R2/fR scalar mode is absent in the local exterior branch | show c_R2=c_fR=0 or that the term is topological/redundant/non-propagating after parent reduction | TARGET_EXACT | requires parent-signed metric-only second-order no-extra-scalar theorem | NOT_PROMOTED | False | False |
| R2ZERO1341_1_second_order_filter | second-order metric-only premise kills R2/fR | R2/fR generically creates fourth-order/scalar dynamics unless coefficient vanishes | FILTER_CLEAN | filter says what must vanish; it does not prove MTS coefficient vanishes | CONDITIONAL_ONLY | False | False |
| R2ZERO1341_2_topological_escape | R2/fR term is topological or boundary-harmless | classify the local curvature-squared piece as topological/no-flux | ESCAPE_NOT_AVAILABLE_FOR_GENERIC_R2FR | R^2 and generic f(R) are not the 4D Gauss-Bonnet topological invariant | COUNTERMODEL_SURVIVES | False | False |
| R2ZERO1341_3_integrated_out_tower | eliminated hidden sectors cannot regenerate R2/fR in S_eff[g] | prove solved auxiliary/projector/memory/scalar sectors give no higher-curvature effective action | NOT_DERIVED | previous audits mark integrated-out f(R), R2, Yukawa, and nonlocal terms as open hazards | COUNTERMODEL_SURVIVES | False | False |
| R2ZERO1341_4_primitive_minimality | MTS primitive quotient forbids curvature-squared marker extensions | derive no natural marker/curvature-tower constructor from motion/time/space primitives | NOT_DERIVED | primitive quotient/no-marker theorem remains unsigned | COUNTERMODEL_SURVIVES | False | False |
| R2ZERO1341_5_verdict | c_R2/c_fR is parent-zeroed | combine second-order filter, no integrated-out tower, primitive minimality, and no-extra-scalar clauses | ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS | zero theorem remains conditional; finite scalar bound row is required | BOUND_ROUTE_SELECTED_NONCLAIM | False | False |

## Scalar Mode Map Contract
| map_id | model_family | potential_or_observable_form | map_status | source_basis | missing_for_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SMAP1341_0_generic_yukawa | metric_fR_or_quadratic_R2 | Phi(r) = -G M/r * [1 + alpha_s exp(-r/lambda_s)] | STANDARD_FORM_RECORDED_NONCLAIM | WEB1341_1_Capozziello2009_fR_Newtonian;WEB1341_2_Stabile2010_fR_PPN | parent coefficient normalization, source shape, screening regime, and exact equation reference | False | False |
| SMAP1341_1_quadratic_convention | R + c_R2 R^2 convention | candidate unscreened scalar map: alpha_s=1/3, lambda_s=hbar/(m_s c), m_s^2 ~ 1/(6 c_R2) in common normalization | CONVENTION_DEPENDENT_NEEDS_PARENT_NORMALIZATION | R2RUN963_1_mass_coupling_map says formula known but MTS inputs missing; external equation source must be pinned before claim | MTS coefficient units/sign and exact convention linking c_R2 to scalaron mass | False | False |
| SMAP1341_2_PPN_regime | solar-system scalar PPN | gamma/beta depend on scalar range, screening, source profile, and observation regime | SOURCE_CANDIDATE_RECORDED_MAP_NOT_FILLED | WEB1341_2_Stabile2010_fR_PPN;WEB1341_3_Cassini_gamma | explicit gamma(beta,lambda,alpha) projection and Cassini-compatible regime selection | False | False |

## Source Backed Bound Rows Nonclaim
| bound_id | arena | bound_quantity | lambda_value | lambda_units | alpha_bound | confidence_or_context | source_url | extraction_method | curve_status | missing_for_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND1341_0_R10_Lee2020_anchor | R10_short_range_Yukawa | gravitational_strength_Yukawa_range | 38.6 | micrometre | 1.0 | 95_percent_confidence_gravitational_strength_anchor | https://arxiv.org/abs/2002.11761 | arXiv_abstract_anchor_only | ANCHOR_ONLY_NON_CURVE | full alpha(lambda) curve and interpolation at predicted alpha/lambda | False | False |
| BOUND1341_1_R10_full_curve_required | R10_short_range_Yukawa | alpha_bound(lambda) | MISSING_DIGITIZED_CURVE | micrometre | MISSING_DIGITIZED_CURVE | full curve required before any scalar-mode pass/fail claim | MISSING_FULL_CURVE_SOURCE_EXTRACTION | not_acquired | FULL_CURVE_REQUIRED | digitized/source-backed curve rows with units and provenance | False | False |
| BOUND1341_2_PPN_Cassini_source_candidate | solar_system_PPN | gamma_minus_1 | not_applicable | not_applicable | not_applicable | Cassini gamma source candidate; formula/regime map missing | https://pubmed.ncbi.nlm.nih.gov/14508481/ | source_string_recorded | PPN_SOURCE_CANDIDATE_MAP_MISSING | explicit R2/fR scalar prediction for gamma in Cassini regime and chosen confidence convention | False | False |

## MTS R2FR Prediction Template
| prediction_id | model_id | coefficient_symbol | coefficient_value | coefficient_units | alpha_predicted | lambda_predicted_um | mass_eV | screening_flag | source_file | formula_reference | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1341_0_MTS_coefficient_required | MTS_R2FR_scalar_mode_candidate | c_R2_or_c_fR | MISSING_PARENT_INPUT | MISSING_UNITS | MISSING_ALPHA | MISSING_LAMBDA | MISSING_MASS | MISSING_SCREENING_STATUS | MISSING_SOURCE_FILE | MISSING_FORMULA_REFERENCE | False | False |
| PRED1341_1_zero_switch | MTS_R2FR_zero_route | c_R2_or_c_fR | 0_IF_R2ZERO1341_PARENT_THEOREM_SIGNED_ELSE_MISSING | not_applicable_if_zero | 0_IF_PARENT_SIGNED_ELSE_MISSING | not_applicable_if_zero | infinite_if_parent_signed_else_missing | not_applicable_if_zero | P8_Y5_R10_1341_R2FR_ZERO_THEOREM_ATTEMPT.csv | R2ZERO1341_5_verdict | False | False |

## R2FR Bound Runner Dryrun
| run_id | prediction_id | accepted_for_scoring | claim_allowed | verdict | missing_fields | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1341_0_MTS_coefficient_required | PRED1341_0_MTS_coefficient_required | False | False | REJECTED_MISSING_MTS_PREDICTION_INPUTS | coefficient_value;coefficient_units;alpha_predicted;lambda_predicted_um;mass_eV;screening_flag;source_file;formula_reference | strict R2/fR runner: no pass without parent-zero theorem or complete MTS prediction plus source-backed full bound curve | False |
| RUN1341_1_zero_switch | PRED1341_1_zero_switch | False | False | REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED | none | strict R2/fR runner: no pass without parent-zero theorem or complete MTS prediction plus source-backed full bound curve | False |
| RUN1341_VERDICT | all_rows | False | False | R2FR_BRANCH_BLOCKED_NONCLAIM | parent_zero_signature_or_MTS_coefficient_and_full_bound_curve | zero theorem failed; bound route is prepared but not scoreable | False |

## Claim Gate
| gate_id | claim | allowed_if | current_status | reason | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| CLAIM1341_0_zero_theorem | R2/fR scalar mode zero | R2ZERO1341_5_verdict becomes parent-signed with no integrated-out tower loophole | BLOCKED | zero theorem not derived | False | False |
| CLAIM1341_1_bound_pass | finite R2/fR scalar branch passes R10/PPN bounds | complete MTS coefficient prediction plus full source-backed alpha(lambda)/PPN bound rows | BLOCKED | MTS coefficient and full curve/regime map missing | False | False |
| CLAIM1341_2_EH_core | EH core/local-GR left-hand side | R2/fR plus every other R11 family is zeroed or bounded and GM/PPN gates pass | BLOCKED | 1341 only handles first scalar family as nonclaim | False | False |

## Decision Ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1341_0_zero_result | R2/fR scalar-mode zero theorem is not derived | second-order/no-extra-scalar/minimal quotient premises remain unsigned and integrated-out towers remain possible | finite scalar bound route must remain live | False | False |
| DEC1341_1_bound_result | source-backed bound scaffold is improved but nonclaim | Lee 2020 gives an anchor, Cassini gives a PPN source candidate, but full curve, MTS coefficient, and regime map are missing | next work should acquire/digitize full R10 curve or derive scalar-mode zero before any scoring | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1341_0_1342 | 1342-Y5-R10-RAB-R2FR-full-bound-curve-acquisition-or-integrated-out-tower-zero-proof.md | scripts/Y5_R10_RAB_R2FR_full_bound_curve_acquisition_or_integrated_out_tower_zero_proof.py | either close the integrated-out R2/fR tower loophole or acquire a source-backed full alpha(lambda) bound curve for finite scalar-mode scoring | a parent-zero proof for c_R2/c_fR, or a full nonclaim bound-curve intake with interpolation checks and provenance | do not claim from anchor-only rows, do not infer missing MTS coefficient, do not promote EH/local GR | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1341_0_sources_exist | registered local source paths exist and anchors are found | PASS | 11/11 source anchors found |
| VAL1341_1_web_sources_recorded | external source URLs are recorded for theory and bound provenance | PASS | WEB1341_0_Lee2020_R10;WEB1341_1_Capozziello2009_fR_Newtonian;WEB1341_2_Stabile2010_fR_PPN;WEB1341_3_Cassini_gamma |
| VAL1341_2_zero_not_derived | R2/fR zero theorem is not promoted | PASS | R2ZERO1341_5_verdict=ZERO_THEOREM_NOT_DERIVED_CURRENT_CORPUS |
| VAL1341_3_scalar_map_nonclaim | scalar-mode map rows remain nonclaim and convention-guarded | PASS | SMAP1341_0_generic_yukawa=STANDARD_FORM_RECORDED_NONCLAIM;SMAP1341_1_quadratic_convention=CONVENTION_DEPENDENT_NEEDS_PARENT_NORMALIZATION;SMAP1341_2_PPN_regime=SOURCE_CANDIDATE_RECORDED_MAP_NOT_FILLED |
| VAL1341_4_anchor_only_no_claim | R10 Lee 2020 source is anchor-only non-curve and cannot claim | PASS | BOUND1341_0_R10_Lee2020_anchor=ANCHOR_ONLY_NON_CURVE |
| VAL1341_5_full_curve_missing | full source-backed alpha(lambda) curve remains required | PASS | BOUND1341_1_R10_full_curve_required=FULL_CURVE_REQUIRED |
| VAL1341_6_runner_rejects | strict R2/fR dry-run rejects zero switch and missing MTS prediction | PASS | RUN1341_0_MTS_coefficient_required=REJECTED_MISSING_MTS_PREDICTION_INPUTS;RUN1341_1_zero_switch=REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED;RUN1341_VERDICT=R2FR_BRANCH_BLOCKED_NONCLAIM |
| VAL1341_7_claims_blocked | zero, bound-pass, and EH/local-GR claims remain blocked | PASS | CLAIM1341_0_zero_theorem=BLOCKED;CLAIM1341_1_bound_pass=BLOCKED;CLAIM1341_2_EH_core=BLOCKED |
| VAL1341_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false where present |
| VAL1341_9_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1341_10_next_target_1342 | next target routes to full bound curve acquisition or integrated-out tower zero proof | PASS | 1342-Y5-R10-RAB-R2FR-full-bound-curve-acquisition-or-integrated-out-tower-zero-proof.md |
| VAL1341_11_overall | overall 1341 validation | PASS | 1341 fails the R2/fR zero theorem honestly and prepares source-backed but nonclaim scalar bound rows |
