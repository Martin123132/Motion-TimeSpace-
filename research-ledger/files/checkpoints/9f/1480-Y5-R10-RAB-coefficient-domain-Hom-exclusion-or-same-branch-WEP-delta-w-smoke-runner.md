# 1480 — R10/RAB Coefficient-Domain Hom Exclusion Or Same-Branch WEP Delta-w Smoke Runner

## Verdict
- Coefficient-domain `Hom(C_hid/species, Coeff_source)=Const/absent` is still exact conditional, not parent-derived.
- The scalar invariant counterexample survives: one untrivialized hidden/local scalar can feed a source coefficient unless the target is forbidden.
- The same-branch WEP runner is now explicit and refuses the claim-grade MTS score; only electron/DD proxy rows are computed, quarantined, and nonclaim.

## Hom Exclusion Attempt
| theorem_id | status | current_blocker |
|---|---|---|
| CDH1480_0_target | TARGET_EXACT | operator-domain exhaustion is still a contract and scalar invariant obstruction survives |
| CDH1480_1_trivial_hidden_algebra | EXACT_CONDITIONAL_THEOREM | current corpus has not proved hidden invariant algebra triviality |
| CDH1480_2_target_forbidden | POWERFUL_CONDITIONAL_NOT_REDUCED | forbidden-target rule is not derived from MTS primitives |
| CDH1480_3_scalar_counterexample | COUNTEREXAMPLE_PROVED | must prove trivial invariant algebra or forbid source coefficient target |
| CDH1480_4_radiative_readout | UNSIGNED_CLOSURE | radiative/readout closure remains unsigned |
| CDH1480_5_verdict | PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED | trivial invariant algebra, forbidden coefficient targets, source label forgetting, and readout closure remain unsigned |

## Hom Obstructions
| obstruction_id | status | required_to_close |
|---|---|---|
| HOB1480_0_scalar_I | COUNTEREXAMPLE_PROVED | prove O(C_hid)^inv=R or forbid coefficient target |
| HOB1480_1_species_label | COUNTEREXAMPLE_SURVIVES | source-label forgetting plus no source-only prefactor syntax |
| HOB1480_2_marker_domain | COUNTEREXAMPLE_SURVIVES | no-marker/no-extension theorem and readout no-reentry |
| HOB1480_3_current_label | CURRENT_OWNER_UNSIGNED | Noether/Hilbert current owner and non-Hilbert silence |
| HOB1480_4_readout_kernel | READOUT_TRANSFER_UNSIGNED | official source-worldtube/readout transfer closure |
| HOB1480_5_effective_action | UNSIGNED_CLOSURE | radiative/readout closure theorem or finite residual priors |

## Same-Branch WEP Inputs
| input_id | object | current_value | input_present |
|---|---|---|---:|
| WIN1480_0_eta_bound | eta_bound | 2.8e-15 | True |
| WIN1480_1_C_parent | C_parent delta_w coefficient vector | MISSING_PARENT_COEFFICIENT | False |
| WIN1480_2_R_source | R_source Earth/source vector | MISSING_SOURCE_VECTOR | False |
| WIN1480_3_R_material | R_TA6V_minus_PtRh10 material tensor | PARTIAL_SMOKE_ONLY | False |
| WIN1480_4_K_CMSM | MICROSCOPE readout/orbit kernel | MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY | False |
| WIN1480_5_no_cancellation | component covariance/no-cancellation | MISSING_NO_CANCELLATION_ENVELOPE | False |
| WIN1480_6_same_branch_lock | same branch convention | MISSING_SAME_BRANCH_PRODUCT_CONVENTION | False |

## WEP Smoke Results
| smoke_id | status | computed_value | why_nonclaim |
|---|---|---|---|
| WSR1480_0_same_branch_MTS_claim_grade | BLOCKED_MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_CMSM_COVARIANCE | NOT_COMPUTED | same-branch product inputs are missing |
| WSR1480_1_electron_unit_kernel_quarantine | PROXY_COMPUTED_QUARANTINED | 8.948213306283e-11 | unit-kernel electron proxy lacks parent tau/source/readout/product convention |
| WSR1480_2_DD_alpha_external_quarantine | EXTERNAL_DD_SMOKE_COMPUTED_QUARANTINED | 1.407170315973e-12 | DD alpha/Coulomb smoke is not MTS parent basis |
| WSR1480_3_DD_surface_external_quarantine | EXTERNAL_DD_SMOKE_COMPUTED_QUARANTINED | 8.468280557212e-13 | DD surface/binding smoke is not full MTS material tensor |
| WSR1480_4_no_cancellation_guard | PASS_GUARD_ACTIVE | NOT_COMPUTED | prevents cherry-picking component cancellations |

## Proxy Quarantine
| proxy_id | value | quarantine_reason |
|---|---|---|
| PQ1480_0_electron_unit_kernel | 8.948213306283e-11 | unit-kernel assumption; no tau_WEP/source/readout normalization |
| PQ1480_1_DD_alpha_smoke | 1.407170315973e-12 | external phenomenological basis; not MTS parent source basis |
| PQ1480_2_DD_surface_smoke | 8.468280557212e-13 | external phenomenological basis; not full MTS material tensor |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
|---|---|---|
| REJ1480_0_parent_basis | MISSING_PARENT_COUPLING_BASIS | cannot compare coefficients before delta_w vector basis is declared |
| REJ1480_1_C_parent | MISSING_PARENT_COEFFICIENT | no parent coefficient vector or theorem-zero certificate |
| REJ1480_2_R_source | MISSING_SOURCE_VECTOR | Earth/source worldtube and composition are not in parent basis |
| REJ1480_3_R_material | MISSING_FULL_PARENT_MATERIAL_TENSOR | Ti/Pt material tensor is only composition context plus DD smoke rows |
| REJ1480_4_K_CMSM | MISSING_READOUT_KERNEL | official MICROSCOPE/readout/orbit kernel is not imported |
| REJ1480_5_covariance | MISSING_NO_CANCELLATION_ENVELOPE | no covariance/norm rule for component cancellations |
| REJ1480_6_same_branch | MISSING_SAME_BRANCH_PRODUCT_CONVENTION | unit-kernel/external smoke rows cannot be promoted |
| REJ1480_7_Hom | HOM_EXCLUSION_NOT_PARENT_DERIVED | source-only coefficients remain legal residuals |

## Gates
| gate_id | gate_pass | claim_effect |
|---|---:|---|
| GATE1480_0_Hom_conditional | True | contract support only |
| GATE1480_1_Hom_refused | True | source coefficients stay live |
| GATE1480_2_obstructions_retained | True | no local-GR/GR source universality claim |
| GATE1480_3_same_branch_runner_blocked | True | runner exists but refuses score |
| GATE1480_4_proxies_quarantined | True | no proxy promoted as MTS |
| GATE1480_5_rejection_complete | True | claim firewall active |

## Decision Ledger
- `DEC1480_0_Hom_status`: coefficient-domain Hom exclusion remains exact conditional, not parent-derived — delta_w source coefficients remain live residuals.
- `DEC1480_1_runner_status`: same-branch WEP runner is built but refuses the MTS score — only proxy/quarantine rows are computed.
- `DEC1480_2_next_step`: fill the same-branch WEP material/readout pack next — 1481 should acquire/source Ti/Pt tensor, tau/readout, covariance, and source vector rows.

## Validation
| check_id | result | detail |
|---|---|---|
| VAL1480_0_sources | PASS | all cited local source paths exist |
| VAL1480_1_Hom_conditional | PASS | Hom exclusion conditional theorem route recorded |
| VAL1480_2_Hom_refused | PASS | Hom theorem-zero promotion refused |
| VAL1480_3_obstructions_retained | PASS | scalar/species/marker/current/readout obstructions retained |
| VAL1480_4_input_matrix_blocks | PASS | same-branch WEP input matrix contains missing blockers |
| VAL1480_5_same_branch_blocked | PASS | claim-grade MTS WEP smoke row refuses score |
| VAL1480_6_proxy_numeric | PASS | quarantine proxy rows compute numeric smoke values |
| VAL1480_7_proxy_nonclaim | PASS | proxy rows remain nonclaim |
| VAL1480_8_rejection_blocks | PASS | runner rejection ledger blocks claim |
| VAL1480_9_gate_claim_false | PASS | all gates keep claim flags false |
| VAL1480_10_generated_csv_parse | PASS | all generated 1480 CSVs parse cleanly |
| VAL1480_11_branch_copies | PASS | nonclaim branch/quarantine copies written |
| VAL1480_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1480_13_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1480_14_overall | PASS | 1480 refuses Hom theorem-zero and builds same-branch WEP smoke runner with quarantined proxy values |

## Source Register
| source_id | exists | path_or_url | usage |
|---|---:|---|---|
| SRC1480_0_prev_next | True | `source-intake\mts_residuals\P8_Y5_R10_1479_NEXT_TARGET.csv` | 1479 handoff selecting coefficient-domain Hom exclusion or same-branch WEP smoke runner |
| SRC1480_1_prev_validation | True | `source-intake\mts_residuals\P8_Y5_BRR545_1479_VALIDATION.csv` | 1479 validation baseline |
| SRC1480_2_prev_theorem | True | `source-intake\mts_residuals\P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv` | no-source-only prefactor theorem attempt |
| SRC1480_3_prev_hom | True | `source-intake\mts_residuals\P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv` | Hom species/source prefactor audit |
| SRC1480_4_prev_bound_inputs | True | `source-intake\mts_residuals\P8_Y5_R10_1479_DELTA_W_BOUND_INPUT_REQUIREMENTS.csv` | delta_w bound input requirements |
| SRC1480_5_prev_bound_pack | True | `source-intake\mts_residuals\P8_Y5_R10_1479_COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv` | component delta_w bound pack |
| SRC1480_6_prev_anchors | True | `source-intake\mts_residuals\P8_Y5_R10_1479_DELTA_W_BOUND_ANCHOR_PACK_NONCLAIM.csv` | delta_w bound anchor pack |
| SRC1480_7_prev_firewall | True | `source-intake\mts_residuals\P8_Y5_R10_1479_CLAIM_FIREWALL_AND_NO_BOUND_INVERSION.csv` | claim firewall |
| SRC1480_8_PFT1050 | True | `source-intake\mts_residuals\P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv` | product functor theorem attempt |
| SRC1480_9_NMM1051 | True | `source-intake\mts_residuals\P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv` | no mixed morphism lemma attempt |
| SRC1480_10_ISO1051 | True | `source-intake\mts_residuals\P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv` | invariant scalar obstruction audit |
| SRC1480_11_VOE1058 | True | `source-intake\mts_residuals\P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv` | visible operator-domain exhaustion attempt |
| SRC1480_12_NMF980 | True | `source-intake\mts_residuals\P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv` | no-marker functor theorem attempt |
| SRC1480_13_ODR1066 | True | `source-intake\mts_residuals\P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv` | operator-domain rule audit |
| SRC1480_14_OLT1066 | True | `source-intake\mts_residuals\P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv` | object-language typing audit |
| SRC1480_15_OG1451 | True | `source-intake\mts_residuals\P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv` | operator grammar theorem attempt |
| SRC1480_16_REQ1451 | True | `source-intake\mts_residuals\P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv` | epsilon_A bound input requirements |
| SRC1480_17_ANCH1451 | True | `source-intake\mts_residuals\P8_Y5_R10_1451_ARENA_BOUND_ANCHOR_MAP_NONCLAIM.csv` | arena bound anchor map |
| SRC1480_18_PACK1426 | True | `source-intake\mts_residuals\P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv` | finite WEP coefficient input pack |
| SRC1480_19_EB1333 | True | `source-intake\mts_residuals\P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv` | electron residual bound contract |
| SRC1480_20_RSC1416 | True | `source-intake\mts_residuals\P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv` | first R_source coefficient row |
| SRC1480_21_CM1416 | True | `source-intake\mts_residuals\P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv` | source slot countermodel ledger |
| SRC1480_22_local_bounds | True | `source-intake\local_bounds\local_bound_claims.csv` | local bound anchors |
| SRC1480_23_MAT983 | True | `source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv` | MICROSCOPE material constituents |
| SRC1480_24_MAT1080 | True | `source-intake\mts_residuals\P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv` | material composition/tensor candidates |
| SRC1480_25_WCM1053 | True | `source-intake\mts_residuals\P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv` | WEP composition charge smoke matrix |
| SRC1480_26_COMP1232 | True | `source-intake\mts_residuals\P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv` | component fraction formula ledger |
| SRC1480_27_FSP1232 | True | `source-intake\mts_residuals\P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv` | Ti/Pt component fraction source pack |

## Next Target
- `1481-Y5-R10-RAB-same-branch-WEP-material-tau-source-pack-or-Hom-parent-generator-proof.md` via `scripts/Y5_R10_RAB_same_branch_WEP_material_tau_source_pack_or_Hom_parent_generator_proof.py`: try to source/fill the same-branch WEP material tensor, source vector, tau/readout kernel, covariance/no-cancellation, and product convention; if blocked, sharpen the parent-generator proof needed for coefficient-domain Hom exclusion
