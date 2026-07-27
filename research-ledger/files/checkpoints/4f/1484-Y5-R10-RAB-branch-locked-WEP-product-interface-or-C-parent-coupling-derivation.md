# 1484 - Branch-Locked WEP Product Interface Or C Parent Coupling Derivation

## Verdict
- The WEP/local branch now has a complete product interface: `eta_pred = |sum_X C_parent_X R_material_X tau_eff_X|` in one branch/basis.
- This is progress toward derivability, not a claim: `C_parent`, `R_material`, `R_source/K_CMSM`, numeric `tau_eff`, and product sign/units remain blocked.
- The coupling remains the boss fight. The next move is a direct parent functional-derivative or universal-matter double-zero proof attempt.

## Product Interface
| interface_id | symbol_or_factor | current_status | required_basis |
|---|---|---|---|
| WPI1484_0_formula | eta_pred | FORMULA_LOCKED_INPUTS_MISSING | single parent response basis X shared by C_parent, R_material, R_source/tau_eff |
| WPI1484_1_C_parent | C_parent_X | MISSING_C_PARENT_IMPORT | parent response basis X with units/sign/source path |
| WPI1484_2_R_material | R_material_X | MISSING_FULL_PARENT_MATERIAL_TENSOR | same parent response basis X as C_parent_X |
| WPI1484_3_tau_eff | tau_eff_X | SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT | same X basis and same observed coframe/product convention |
| WPI1484_4_product_convention | eta(Ti,Pt) | PARTIAL_PENDING_NONCLAIM | same branch id and no pending sign/readout/source units |
| WPI1484_5_branch_guard | same_parent_branch_id | GUARD_EXISTS_NONCLAIM | MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 |

## Factor Schema
| schema_id | field | applies_to | requirement |
|---|---|---|---|
| FPS1484_0 | same_parent_branch_id | all | must equal active branch id |
| FPS1484_1 | basis_id | all factors | single parent response basis label X |
| FPS1484_2 | component_id | all factors | component index within X basis |
| FPS1484_3 | value | C_parent/R_material/tau_eff rows | not allowed to be MISSING/PENDING/fit-from-bound |
| FPS1484_4 | uncertainty | finite numeric factors | required for nonzero empirical comparison |
| FPS1484_5 | units | all numeric factors | must multiply to dimensionless eta |
| FPS1484_6 | sign_convention | all signed factors | body order, axis, source orientation, and parent sign |
| FPS1484_7 | source_url_or_path | all factors | local file, URL, DOI, or theorem source |
| FPS1484_8 | parent_status | C_parent | closure-only rows refused |
| FPS1484_9 | zero_certificate_status | C_parent zero route | zero only valid with parent proof |
| FPS1484_10 | double_count_rule | material/source | prevents composition/source/readout duplication |
| FPS1484_11 | normalization_rule | tau/product | declared average and denominator convention |
| FPS1484_12 | valid_prediction_row | all | must be true only after every gate passes |

## Compatibility Matrix
| compat_id | condition_pass | current_status | score_effect |
|---|---|---|---|
| COMP1484_0_branch | False | BRANCH_GUARD_NONCLAIM_OR_UNSIGNED | required before WEP score |
| COMP1484_1_C_parent | False | MISSING_C_PARENT_IMPORT | required before WEP score |
| COMP1484_2_material | False | MISSING_FULL_PARENT_MATERIAL_TENSOR | required before WEP score |
| COMP1484_3_readout | False | MISSING_LIVE_READOUT_MATRIX | required before WEP score |
| COMP1484_4_source | False | MISSING_SOURCE_WORLDTUBE | required before WEP score |
| COMP1484_5_product | False | PENDING_PRODUCT_SIGN_UNITS_ORBIT | required before WEP score |
| COMP1484_6_tau | False | TAU_SYMBOLIC_ONLY | required before WEP score |
| COMP1484_7_units | False | UNIT_PRODUCT_NOT_EVALUABLE | required before WEP score |
| COMP1484_8_no_shortcuts | True | PASS_REFUSAL_RULE_ONLY | guards against false positives |

## Refusal Tests
| test_id | bad_input | actual_result | test_pass |
|---|---|---|---|
| REF1484_0_tau_unit | tau_eff_X=1 with no official readout/source rows | REFUSE_TAU_UNIT_KERNEL_SHORTCUT | True |
| REF1484_1_bound_inversion | choose C_parent from MICROSCOPE eta bound | REFUSE_BOUND_AS_PREDICTION | True |
| REF1484_2_DD_proxy | use Damour-Donoghue/material smoke coefficient as MTS C_parent | REFUSE_EXTERNAL_PROXY_AS_PARENT_COEFFICIENT | True |
| REF1484_3_mixed_basis | multiply C_parent, R_material, R_source, tau from different basis labels | REFUSE_MIXED_BRANCH_OR_BASIS | True |
| REF1484_4_measured_G_absorption | absorb relative WEP residual into measured G or common-mode denominator | REFUSE_RELATIVE_MEASURED_G_ABSORPTION | True |
| REF1484_5_closure_zero | declare C_parent=0 from closure preference without proof | REFUSE_UNSIGNED_ZERO | True |
| REF1484_6_requirements_as_data | parse P_WEP_K_CMSM_readout_REQUIREMENTS.csv as live K_CMSM data | REFUSE_REQUIREMENTS_ONLY_FILE | True |

## C Parent Derivation Attempt
| derivation_id | current_status | next_action |
|---|---|---|
| CPD1484_0_define_generator | PARTIAL_SYMBOLIC_ONLY | derive V_WEP from parent action object language, not from empirical eta |
| CPD1484_1_functional_derivative | CONTRACT_STATED_NOT_EVALUABLE | find/synthesize parent action sector whose variation owns this slot |
| CPD1484_2_double_zero_route | CONDITIONAL_THEOREM_ONLY | prove connected ordinary matter category, action-density line owner, and no source-only prefactor from parent action |
| CPD1484_3_finite_route | MISSING_IMPORT_ROW | keep finite route open as nonclaim input if a parent coefficient source appears |
| CPD1484_4_GR_Newton_limit | NOT_DERIVED_FOR_LOCAL_LIMIT | attack coupling zero first; data only tests after theory coefficient exists |
| CPD1484_5_verdict | NOT_CLOSED | next target should go straight at parent functional derivative / universal matter branch proof |

## Local GR/Newton Link
| link_id | target_limit | current_status | missing_for_claim |
|---|---|---|---|
| LGR1484_0_Newton | Newtonian local source law | OPEN | requires C_parent zero or same-branch finite residual bound |
| LGR1484_1_GR | GR local equivalence principle | OPEN | requires universal matter/coframe branch and no species/source prefactor |
| LGR1484_2_PPN | PPN local metric readout | OPEN | requires PPN coefficient map plus C_parent/tau/material/source interface |
| LGR1484_3_WEP | MICROSCOPE same-branch WEP test | BLOCKED | requires all product factors and official source files |
| LGR1484_4_derivation_priority | best route | NEXT | interface now names exact missing factors |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
|---|---|---|
| REJ1484_0_C_parent | MISSING_C_PARENT_IMPORT | no theorem-zero or source-backed finite coefficient exists |
| REJ1484_1_material | MISSING_FULL_PARENT_MATERIAL_TENSOR | R_material_X absent |
| REJ1484_2_tau | TAU_SYMBOLIC_ONLY | tau_eff_X is typed but not evaluated |
| REJ1484_3_readout | MISSING_LIVE_READOUT_MATRIX | K_CMSM data absent |
| REJ1484_4_source | MISSING_SOURCE_WORLDTUBE | R_source data absent |
| REJ1484_5_product | PENDING_PRODUCT_SIGN_UNITS_ORBIT | product convention partial |
| REJ1484_6_branch | BRANCH_GUARD_NONCLAIM_OR_UNSIGNED | branch guard exists as nonclaim scaffold only |
| REJ1484_7_local_GR | LOCAL_GR_REDUCTION_NOT_DERIVED | GR/Newton reduction still depends on coupling/double-zero proof |
| REJ1484_8_no_claim | CLAIM_PROMOTION_FORBIDDEN | no numeric WEP/local-GR claim allowed |

## No-Claim Gates
| gate_id | gate_pass | detail |
|---|---|---|
| GATE1484_0_interface_written | True | branch-locked product interface exists |
| GATE1484_1_schema_written | True | factor schema with basis/units/sign/provenance exists |
| GATE1484_2_refusals_pass | True | shortcut refusal tests pass |
| GATE1484_3_C_parent_blocked | True | C_parent import absent |
| GATE1484_4_tau_blocked | True | tau remains symbolic |
| GATE1484_5_data_blocked | True | readout/source live files absent |
| GATE1484_6_local_GR_open | True | GR/Newton derivation link remains open |
| GATE1484_7_claim_flags_false | True | all generated claim flags false |

## Decision Ledger
- `DEC1484_0_interface_not_score`: write product interface as a type/compatibility contract, not a prediction - future rows have a legal slot without enabling a claim.
- `DEC1484_1_refuse_Cparent_import`: do not create C_parent_WEP_slot_import.csv - coupling remains the main physics bottleneck.
- `DEC1484_2_data_after_derivation`: keep MICROSCOPE data acquisition useful but secondary - next target should attack C_parent derivation directly.
- `DEC1484_3_local_GR_route`: local GR/Newton route is now stated as product-zero/product-bound, not vague plateau language - 1485 should try universal matter branch / functional derivative proof.

## Validation
| check_id | result | detail |
|---|---|---|
| VAL1484_0_sources | PASS | all cited local source paths exist |
| VAL1484_1_interface | PASS | branch-locked WEP product interface written |
| VAL1484_2_factor_schema | PASS | factor schema covers basis/units/sign/provenance |
| VAL1484_3_compatibility_blocks | PASS | compatibility matrix blocks score paths |
| VAL1484_4_refusals | PASS | shortcut refusal tests pass |
| VAL1484_5_C_parent_open | PASS | C_parent derivation remains open/nonclaim |
| VAL1484_6_clause_gates | PASS | prior C_parent clauses remain blocked |
| VAL1484_7_local_GR_link | PASS | local GR/Newton link ledger points to derivation priority |
| VAL1484_8_rejections | PASS | rejection ledger blocks claim |
| VAL1484_9_no_claim_gates | PASS | no-claim gates pass |
| VAL1484_10_decisions | PASS | decision ledger keeps claims false |
| VAL1484_11_next | PASS | 1485 handoff written |
| VAL1484_12_csv_parse | PASS | all generated 1484 CSVs parse cleanly |
| VAL1484_13_branch_copies | PASS | branch/quarantine copies written |
| VAL1484_14_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1484_15_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1484_16_claim_flags_false | PASS | all prediction/claim flags remain false |
| VAL1484_17_overall | PASS | 1484 locks the branch-locked WEP product interface and keeps C_parent/local-GR derivation open |

## Next Target
| next_id | next_target | script | objective |
|---|---|---|---|
| NEXT1484_0_1485 | 1485-Y5-R10-RAB-C-parent-WEP-functional-derivative-or-universal-matter-double-zero-proof.md | scripts/Y5_R10_RAB_C_parent_WEP_functional_derivative_or_universal_matter_double_zero_proof.py | try to derive the WEP coupling slot from a parent functional derivative, or prove the universal-matter double-zero theorem needed for local GR/Newton reduction; otherwise keep C_parent as explicit closure-only debt |
