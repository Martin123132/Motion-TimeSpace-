# 1316: RAB P0 Alpha Coupling Input Source Or Derivation Attack

**Current verdict:** 1316 tries the derivation route first. It does not promote `b_alpha=0`, clock silence, WEP/source silence, R10 silence, or cross-arena transfer. Every route remains either an exact conditional theorem or a finite source-input requirement.

**Main progress:** the coupling bottleneck is now equation-shaped. The work no longer says merely "missing coupling"; it states the product forms and exact inputs that must be derived or sourced before any P0 alpha row can score.

**Decision:** build a fillable source-intake template/runner next. If a parent primitive appears, it can enter as a theorem-zero certificate; otherwise each product must be numeric, sourced, and provenance-checked.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1316_0_1315_next | source-intake/mts_residuals/P8_Y5_R10_1315_NEXT_TARGET.csv | NEXT1315_0_1316 | True | True | handoff into P0 alpha coupling derivation/source attack | False | False |
| SRC1316_1_1315_blockers | source-intake/mts_residuals/P8_Y5_R10_1315_MISSING_INPUT_BLOCKER_LEDGER.csv | BLK1315_3_0 | True | True | P0 blocker inventory | False | False |
| SRC1316_2_1315_score | source-intake/mts_residuals/P8_Y5_R10_1315_FIRST_NONCLAIM_SCORE_TABLE.csv | NCS1315_3_3_r10 | True | True | current nonclaim score table | False | False |
| SRC1316_3_1315_shortcuts | source-intake/mts_residuals/P8_Y5_R10_1315_ANTI_SHORTCUT_GATES.csv | SHORT1315_1_no_threshold_prediction | True | True | anti-shortcut policy | False | False |
| SRC1316_4_1315_r10 | source-intake/mts_residuals/P8_Y5_R10_1315_R10_REFUSAL_DETAIL.csv | R10REF1315_3_decision | True | True | R10 refusal detail | False | False |
| SRC1316_5_1314_parent | source-intake/mts_residuals/P8_Y5_R10_1314_PARENT_PRIMITIVE_ESCAPE_HATCH.csv | PESC1314_1_alpha_F2 | True | True | parent primitive escape hatch state | False | False |
| SRC1316_6_1314_schema | source-intake/mts_residuals/P8_Y5_R10_1314_ALPHA_SCOREPACK_INPUT_SCHEMA.csv | AS1314_3_r10_vector | True | True | scorepack input schema | False | False |
| SRC1316_7_1313_hsc | source-intake/mts_residuals/P8_Y5_R10_1313_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK_UPDATE.csv | HSC1313_1_alpha | True | True | hidden scalar and source/readout counterexamples | False | False |
| SRC1316_8_1312_balpha | source-intake/mts_residuals/P8_Y5_R10_1312_B_ALPHA_NO_F2_PROOF_AUDIT.csv | B_ALPHA_THEOREM_ZERO_NOT_DERIVED | True | True | b_alpha theorem-zero failure state | False | False |

## P0 Blocker Import
| import_id | source_blocker_id | runner_row_id | blocker_token | blocker_source | priority | current_disposition | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMP1316_0 | BLK1315_0_0 | RUN1314_0_alpha | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | runner_missing_inputs | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_1 | BLK1315_0_acquisition | RUN1314_0_alpha | MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE | source_acquisition_ledger | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_2 | BLK1315_0_counterexample | RUN1314_0_alpha | HSC1313_1_alpha | counterexample_lock | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_3 | BLK1315_1_0 | RUN1314_1_clock | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | runner_missing_inputs | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_4 | BLK1315_1_acquisition | RUN1314_1_clock | MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT | source_acquisition_ledger | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_5 | BLK1315_1_counterexample | RUN1314_1_clock | HSC1313_3_clock_readout | counterexample_lock | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_6 | BLK1315_2_0 | RUN1314_2_wep | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | runner_missing_inputs | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_7 | BLK1315_2_acquisition | RUN1314_2_wep | MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT | source_acquisition_ledger | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_8 | BLK1315_2_counterexample | RUN1314_2_wep | HSC1313_4_source_weight | counterexample_lock | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_9 | BLK1315_3_0 | RUN1314_3_r10 | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | runner_missing_inputs | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_10 | BLK1315_3_acquisition | RUN1314_3_r10 | MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND | source_acquisition_ledger | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_11 | BLK1315_3_counterexample | RUN1314_3_r10 | HSC1313_1_alpha;HSC1313_4_source_weight | counterexample_lock | P0 | ATTACKED_IN_1316 | False | False |
| IMP1316_12 | BLK1315_4_0 | RUN1314_4_cross_arena | MISSING_CROSS_ARENA_PARENT_MAP | runner_missing_inputs | P1 | ATTACKED_IN_1316 | False | False |
| IMP1316_13 | BLK1315_4_acquisition | RUN1314_4_cross_arena | MISSING_CROSS_ARENA_PARENT_MAP | source_acquisition_ledger | P1 | ATTACKED_IN_1316 | False | False |
| IMP1316_14 | BLK1315_4_counterexample | RUN1314_4_cross_arena | HSC1313_0_generic;HSC1313_3_clock_readout | counterexample_lock | P1 | ATTACKED_IN_1316 | False | False |

## Derivation Attack Ledger
| attack_id | target | conditional_result | obstruction | output_formula_if_not_zero | required_source_fill | promotion_status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DVA1316_0_alpha_F2 | b_alpha/c_alpha theorem-zero | EXACT_IF_PARENT_SIGNED | PESC1314_1_alpha_F2 is counterexample-active; HSC1313_1_alpha permits f(I_hid)F_Q^2; radiative/readout closure is not signed. | P_alpha=abs(b_alpha or c_alpha_DD) | numeric b_alpha/c_alpha with units, branch, normalization, source path, or a signed parent primitive killing f(I_hid)F_Q^2 and readout regeneration | NOT_PROMOTED | False | False |
| DVA1316_1_clock_readout | clock alpha product | EXACT_IF_READOUT_SIGNED | HSC1313_3_clock_readout remains active; the source-backed clock product bound is not a standalone b_alpha value. | P_clock_alpha=abs(b_alpha*tau_clock_time) or direct sourced P_clock_alpha | tau_clock_time or direct P_clock_alpha with clock pair, alpha sensitivity/readout model, time units, branch, and source path | NOT_PROMOTED | False | False |
| DVA1316_2_wep_source | WEP alpha/source product | EXACT_IF_SOURCE_MAP_SIGNED | HSC1313_4_source_weight remains active; beta_source_alpha, tau_WEP, material DeltaQ_alpha, readout kernel, and source profile are not parent-signed. | P_WEP_alpha=abs(beta_source_alpha*b_alpha*tau_WEP*DeltaQ_alpha_AB) or direct sourced P_WEP_alpha | beta_source_alpha, b_alpha/theorem-zero, tau_WEP, material pair, DeltaQ_alpha_AB, source/worldtube profile, readout kernel, and source paths | NOT_PROMOTED | False | False |
| DVA1316_3_r10_product | R10 alpha(lambda) product | EXACT_IF_BRANCH_VECTOR_AND_BOUND_SIGNED | R10REF1315 keeps numeric product, promoted bound curve, and source/test projection missing; HSC1313_1_alpha and HSC1313_4_source_weight stay active. | P_R10_alpha(lambda)=abs(Z_X*K_X(lambda)*beta_source(lambda)*beta_test(lambda)*tau_R10*epsilon_tail) | lambda_X, Z_X, K_X(lambda), beta_source(lambda), beta_test(lambda), tau_R10, epsilon_tail, promoted alpha_bound(lambda), and source paths | NOT_PROMOTED | False | False |
| DVA1316_4_cross_arena | shared alpha branch transfer | EXACT_IF_PARENT_BRANCH_FUNCTOR_SIGNED | The current rows are separate pressure/threshold rows; no same-branch readout functor is signed. | same_branch_id plus arena maps F_clock,F_WEP,F_R10,F_local with no threshold transfer | branch classifier, readout functor, arena product maps, and explicit statement of which products can and cannot transfer | NOT_PROMOTED | False | False |
| DVA1316_5_parent_primitive | new parent grammar primitive | EXACT_CONTRACT_WRITTEN_NOT_SOURCE_SIGNED | No source-backed primitive clause is present in the current corpus. | not a numeric product; theorem-zero route only if parent object-language certificate exists | primitive statement, parent action clause, typed coefficient-domain rule, no-hidden-argument rule, radiative closure, readout closure, source path | NOT_PROMOTED | False | False |

## Product Formula Requirements
| formula_id | runner_row_id | canonical_product | minimum_inputs | current_available | why_not_numeric | promotion_rule | score_ready | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FORM1316_0_alpha | RUN1314_0_alpha | P_alpha=abs(b_alpha or c_alpha_DD) | b_alpha_or_c_alpha;units;branch_id;normalization;source_path;or theorem_zero_certificate | threshold_abs_only | threshold is a comparison fence, not a prediction | numeric source-backed coefficient or signed theorem-zero | False | False | False |
| FORM1316_1_clock | RUN1314_1_clock | P_clock_alpha=abs(b_alpha*tau_clock_time) or direct P_clock_alpha | b_alpha_or_zero;tau_clock_time;clock_pair;readout_model;units;source_path | clock_bound_only | tau/readout map missing; product bound cannot be divided by assumed tau | direct numeric product or signed tau/readout map | False | False | False |
| FORM1316_2_wep | RUN1314_2_wep | P_WEP_alpha=abs(beta_source_alpha*b_alpha*tau_WEP*DeltaQ_alpha_AB) or direct P_WEP_alpha | beta_source_alpha;b_alpha_or_zero;tau_WEP;DeltaQ_alpha_AB;material_pair;source_profile;readout_kernel;source_path | pressure_target_only | source normalization, material response, and tau/readout are missing | direct numeric WEP product or every factor sourced/derived | False | False | False |
| FORM1316_3_r10 | RUN1314_3_r10 | P_R10_alpha(lambda)=abs(Z_X*K_X(lambda)*beta_source(lambda)*beta_test(lambda)*tau_R10*epsilon_tail) | lambda_X;Z_X;K_X(lambda);beta_source(lambda);beta_test(lambda);tau_R10;epsilon_tail;alpha_bound_lambda;source_path | review_candidate_or_anchor_only_nonclaim | finite product vector and promoted claim-valid alpha_bound(lambda) curve are missing | numeric source-backed product and promoted bound curve | False | False | False |
| FORM1316_4_cross_arena | RUN1314_4_cross_arena | same_branch_id plus arena maps F_clock,F_WEP,F_R10,F_local | parent_branch_classifier;readout_functor;arena_product_maps;nontransfer_statement | separate_pressure_rows_only | no signed common branch map; arena thresholds cannot be transferred | one signed parent branch/readout map or explicit separate-product declaration | False | False | False |

## P0 Source Requirement Ledger
| requirement_id | needed_object | arena | minimum_usable_form | current_status | resolution_type | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ1316_0_balpha | b_alpha/c_alpha | alpha;clock;WEP;R10 | numeric coefficient or theorem-zero certificate | MISSING_SOURCE_BACKED_COEFFICIENT_OR_PARENT_PRIMITIVE | derive_or_source | False | False |
| REQ1316_1_norm | fixed EM current normalization | alpha | normalization convention and branch id | MISSING_NORMALIZATION_SOURCE | derive_or_source | False | False |
| REQ1316_2_no_hidden | no-hidden visible coefficient primitive | alpha;WEP;R10 | typed parent object-language rule | MISSING_PARENT_PRIMITIVE | derive_or_source | False | False |
| REQ1316_3_radiative | radiative/readout closure | alpha;clock | closure proof that loops/readout do not regenerate F_Q^2 coefficient | MISSING_RADIATIVE_READOUT_CLOSURE | derive_or_source | False | False |
| REQ1316_4_tau_clock | tau_clock_time | clock | clock readout projection or direct product | MISSING_CLOCK_READOUT_MAP | derive_or_source | False | False |
| REQ1316_5_clock_model | clock sensitivity/readout model | clock | clock pair, sensitivity vector, units, source path | MISSING_CLOCK_MODEL | derive_or_source | False | False |
| REQ1316_6_beta_source | beta_source_alpha | WEP;R10 | source normalization coefficient as function of parent branch | MISSING_SOURCE_NORMALIZATION | derive_or_source | False | False |
| REQ1316_7_tau_wep | tau_WEP | WEP | WEP branch projection/readout factor | MISSING_TAU_WEP | derive_or_source | False | False |
| REQ1316_8_material | DeltaQ_alpha_AB/material map | WEP | material pair response and readout kernel | MISSING_MATERIAL_RESPONSE | derive_or_source | False | False |
| REQ1316_9_source_profile | source/worldtube profile | WEP;R10;local | finite source profile and domain | MISSING_SOURCE_PROFILE | derive_or_source | False | False |
| REQ1316_10_lambda | lambda_X | R10 | range scale with units and branch id | MISSING_LAMBDA_X | derive_or_source | False | False |
| REQ1316_11_ZX | Z_X | R10 | branch amplitude/normalization | MISSING_Z_X | derive_or_source | False | False |
| REQ1316_12_KX | K_X(lambda) | R10 | kernel or profile factor as lambda function | MISSING_K_X | derive_or_source | False | False |
| REQ1316_13_beta_test | beta_test(lambda) | R10 | test-body coupling/readout factor | MISSING_BETA_TEST | derive_or_source | False | False |
| REQ1316_14_tail | epsilon_tail | R10 | finite-size/tail correction convention | MISSING_EPSILON_TAIL | derive_or_source | False | False |
| REQ1316_15_bound | alpha_bound(lambda) | R10 | digitized/source-backed promoted bound curve | MISSING_PROMOTED_BOUND_CURVE | derive_or_source | False | False |
| REQ1316_16_branch | parent branch classifier | cross_arena | shared branch id and arena maps | MISSING_CROSS_ARENA_PARENT_MAP | derive_or_source | False | False |

## Counterexample Disposition
| counterexample_id | blocks | 1316_disposition | reason | required_to_close | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| HSC1313_1_alpha | b_alpha/c_alpha theorem-zero and R10 alpha product | ACTIVE | f(I_hid)F_Q^2 remains legal without parent no-hidden/radiative/readout primitive | signed typed coefficient-domain primitive or source-backed finite coefficient | False | False |
| HSC1313_3_clock_readout | clock product transfer | ACTIVE | readout can reintroduce alpha dependence after EFT/spectroscopy | signed readout functor or direct P_clock_alpha source | False | False |
| HSC1313_4_source_weight | WEP/R10 source-side theorem-zero and local source branch | ACTIVE | source-only species weights remain syntactically possible | signed source-normalization theorem or source-backed beta/tau/material rows | False | False |
| R10REF1315_product_bound_source | R10 claim row | ACTIVE | numeric R10 product, promoted alpha_bound(lambda), and source/test projection are all missing | complete R10 product vector plus promoted bound curve | False | False |

## Promotion Gates
| gate_id | gate | must_have | current_status | claim_rule | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| GATE1316_0_parent_theorem | parent theorem-zero route | typed visible coefficient domain, no hidden scalar arguments, fixed normalization, radiative/readout closure | BLOCKED | theorem-zero cannot be claimed from minimality or absence in a chosen effective action | False | False |
| GATE1316_1_numeric_prediction | finite numeric product route | numeric predicted_abs_value with units, branch, source path, and no MISSING tokens | BLOCKED | thresholds and bounds are comparison fences, never predictions | False | False |
| GATE1316_2_clock | clock row | tau_clock_time/readout map or direct clock product | BLOCKED | clock product bound cannot be divided by assumed tau | False | False |
| GATE1316_3_wep_source | WEP/source row | source normalization, tau_WEP, material response, source profile, readout kernel | BLOCKED | beta_source_alpha and tau_WEP cannot be set to unity | False | False |
| GATE1316_4_r10 | R10 row | finite R10 product vector and promoted alpha_bound(lambda) curve | BLOCKED | review-candidate or anchor-only bounds remain nonclaim | False | False |
| GATE1316_5_cross_arena | cross-arena transfer | same parent branch classifier and arena readout maps | BLOCKED | clock/WEP/R10 products do not transfer without signed functor | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1316_0_derivation | P0 coupling derivation attempted but not promoted | all theorem-zero routes remain exact conditionals with active hidden-scalar/readout/source counterexamples | use the product formulas and source ledger as the exact intake contract | False | False |
| DEC1316_1_contract | P0 coupling is now equation-shaped | alpha, clock, WEP, R10, and cross-arena rows have explicit product forms and minimum input lists | build a source-intake template/runner that can accept real coefficients or theorem-zero certificates without hand edits | False | False |
| DEC1316_2_no_claim | no R10/WEP/clock/local-GR claim | no P0 blocker was closed by proof or sourced numeric input | 1317 should turn this into a fillable input template and priority runner | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1316_0_1317 | 1317-Y5-R10-RAB-P0-alpha-source-intake-template-and-priority-runner.md | scripts/Y5_R10_RAB_P0_alpha_source_intake_template_and_priority_runner.py | convert the 1316 exact product/source contract into fillable nonclaim source-intake templates and a runner that refuses rows until numeric/provenanced inputs or signed theorem-zero certificates exist | every P0 required input has a template field, validation rule, provenance field, and refusal reason; no row can become claim-valid from thresholds or unity assumptions | do not invent coefficient values; do not transfer clock bounds into WEP/R10; do not claim local-GR/R10 | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1316_0_sources_exist | registered source paths exist and anchors are found | PASS | 9/9 source anchors found |
| VAL1316_1_blockers_imported | 1315 blockers imported and P0 subset identified | PASS | blocker_rows=15 p0_rows=12 |
| VAL1316_2_derivation_attempts_cover_p0 | derivation attacks cover alpha, clock, WEP, R10, cross-arena, and parent primitive | PASS | NOT_PROMOTED;NOT_PROMOTED;NOT_PROMOTED;NOT_PROMOTED;NOT_PROMOTED;NOT_PROMOTED |
| VAL1316_3_no_derivation_promoted | no P0 derivation is promoted as a claim | PASS | all derivation rows remain exact conditionals or source requirements |
| VAL1316_4_product_formulas_written | canonical product formulas exist for all scorepack rows | PASS | FORM1316_0_alpha;FORM1316_1_clock;FORM1316_2_wep;FORM1316_3_r10;FORM1316_4_cross_arena |
| VAL1316_5_source_requirements_exact | source requirements enumerate P0 missing inputs | PASS | requirements=17 |
| VAL1316_6_counterexamples_active | counterexample locks remain active | PASS | HSC1313_1_alpha;HSC1313_3_clock_readout;HSC1313_4_source_weight;R10REF1315_product_bound_source |
| VAL1316_7_promotion_gates_block | promotion gates block claims until proof/source inputs exist | PASS | GATE1316_0_parent_theorem;GATE1316_1_numeric_prediction;GATE1316_2_clock;GATE1316_3_wep_source;GATE1316_4_r10;GATE1316_5_cross_arena |
| VAL1316_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false throughout generated tables |
| VAL1316_9_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1316_10_next_target_1317 | next target routes to source-intake template and priority runner | PASS | 1317-Y5-R10-RAB-P0-alpha-source-intake-template-and-priority-runner.md |
| VAL1316_11_overall | overall 1316 validation | PASS | 1316 attacks P0 coupling derivations, promotes none, writes exact product/source contract, and routes to fillable source-intake runner |
