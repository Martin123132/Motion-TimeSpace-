# 1481 — R10/RAB Same-Branch WEP Material/Tau/Source Pack Or Hom Parent Generator Proof

## Verdict
- WEP material context is now staged: alloy composition, electron proxy, and DD alpha/surface smoke contrasts are locally available.
- The same-branch claim-grade WEP product is still blocked: `C_parent`, `R_source`, full `R_material`, `K_CMSM/tau_WEP`, covariance, and branch convention are not filled.
- The Hom parent-generator route is sharpened but still open; it needs a real parent-generator image/exhaustion proof, not just a grammar contract.

## Material Context
| row_id | value_or_status | filled_level | missing_for_claim |
|---|---|---|---|
| MAT1481_0_pair_convention | TA6V_minus_PtRh10 | SMOKE_CONTEXT_FILLED | same-branch parent material tensor and readout/source convention |
| MAT1481_1_mass_fraction_sums | PtRh10=1.000000;TA6V=1.000000 | COMPOSITION_CONTEXT_FILLED | isotopic/energy-fraction tensor and parent response basis |
| MAT1481_2_electron_fraction_proxy | 3.129116287420e-05 | AUDITED_NUMERIC_PROXY | parent mass functional, tau/readout/source normalization, and same-branch coefficient |
| MAT1481_3_Ye_proxy_delta | 5.677745650000e-02 | TOY_PROXY_ONLY | not an energy/source tensor; parent basis and no-double-counting rule missing |
| MAT1481_4_DD_alpha_smoke | 1.989808886825e-03 | EXTERNAL_SMOKE_NUMERIC | MTS parent EM/Coulomb source basis and readout/source normalization |
| MAT1481_5_DD_surface_smoke | 3.306456347405e-03 | EXTERNAL_SMOKE_NUMERIC | full nuclear/isotopic source tensor and MTS basis map |
| MAT1481_6_full_tensor | MISSING_FULL_PARENT_MATERIAL_TENSOR | BLOCKED | parent response basis, full material tensor, isotope/alloy averaging, and source/readout environment stack |

## Tau Source Readout Pack
| pack_id | current_status | needed_for |
|---|---|---|
| TAU1481_0_official_arrays | OFFICIAL_ARRAYS_NOT_IMPORTED | K_CMSM/readout kernel |
| TAU1481_1_product_convention | NORMALIZATION_NOT_FILLED | same-branch product convention and units/sign |
| TAU1481_2_source_worldtube | MISSING_SOURCE_PROFILE_WEIGHTING | R_source source leg |
| TAU1481_3_orbit_average | MISSING_ORBIT_AVERAGE_ARRAYS | O_orbit/tau_WEP |
| TAU1481_4_branch_classifier | MISSING_BRANCH_CLASSIFIER | anti-branch-mixing gate |
| TAU1481_5_intake_acceptance | BLOCKED_LOCAL_FILE_COUNT_0 | parser/tau_WEP evaluation permission |
| TAU1481_6_symbolic_tau | TAU_EFF_NOT_FILLED | convert proxy epsilon_e into same-branch WEP bound |

## Same-Branch Contract
| contract_id | current_status | factor |
|---|---|---|
| SBC1481_0_formula | FORMULA_READY_INPUTS_MISSING | eta_pred = |K_CMSM * R_source dot C_parent dot R_material| |
| SBC1481_1_C_parent | MISSING_PARENT_COEFFICIENT | parent delta_w/component coefficient vector |
| SBC1481_2_R_source | MISSING_SOURCE_VECTOR | Earth/source vector in same basis |
| SBC1481_3_R_material | PARTIAL_CONTEXT_ONLY | TA6V-PtRh10 material tensor |
| SBC1481_4_K_CMSM | MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY | readout/orbit/source projection kernel |
| SBC1481_5_covariance | MISSING_NO_CANCELLATION_ENVELOPE | component covariance/no-cancellation envelope |
| SBC1481_6_eta_bound | BOUND_ANCHOR_FILLED_NONCLAIM | MICROSCOPE eta source-charge bound |

## Smoke Update
| smoke_id | status | computed_value | why_nonclaim |
|---|---|---|---|
| WUP1481_0_same_branch_claim_grade | BLOCKED_MISSING_C_PARENT_R_SOURCE_K_CMSM_COVARIANCE_FULL_TENSOR | NOT_COMPUTED | same-branch product factors remain missing or proxy-only |
| WUP1481_1_electron_tau_rescaling_template | UNIT_TAU_ONLY_QUARANTINED | 8.948213306283e-11 | unit tau_eff=1 is a smoke convention only |
| WUP1481_2_DD_alpha_quarantine | EXTERNAL_SMOKE_QUARANTINED | 1.407170315973e-12 | DD alpha basis is external and not same-branch MTS |
| WUP1481_3_DD_surface_quarantine | EXTERNAL_SMOKE_QUARANTINED | 8.468280557212e-13 | DD surface basis is external and not full MTS tensor |

## Hom Parent Generator
| proof_id | current_status | next_action |
|---|---|---|
| HPG1481_0_parent_generator_image | CONTRACT_EXACT_NOT_DERIVED | construct ParentGenerate functor and prove image exhaustion |
| HPG1481_1_no_hidden_generator | BLOCKED_BY_SCALAR_OBSTRUCTION | prove O(C_hid)^inv=R or target exclusion |
| HPG1481_2_no_species_generator | CONDITIONAL_TYPING_NOT_PARENT_SIGNED | derive no-source-only prefactor grammar |
| HPG1481_3_readout_closure | UNSIGNED_CLOSURE | derive radiative/readout closure or keep finite residuals |
| HPG1481_4_verdict | NOT_CLOSED | same-branch WEP pack remains needed |

## Rejection Ledger
| rejection_id | blocking_marker | reason |
|---|---|---|
| REJ1481_0_C_parent | MISSING_PARENT_COEFFICIENT | no parent coefficient vector/theorem-zero certificate |
| REJ1481_1_R_source | MISSING_SOURCE_VECTOR | source worldtube/profile not accepted in parent basis |
| REJ1481_2_K_CMSM | MISSING_READOUT_KERNEL | official MICROSCOPE arrays/product convention/orbit average missing |
| REJ1481_3_tau | TAU_EFF_NOT_FILLED | tau_eff_e remains symbolic; unit tau is quarantine only |
| REJ1481_4_full_tensor | MISSING_FULL_PARENT_MATERIAL_TENSOR | composition and DD smoke context are not full MTS material tensor |
| REJ1481_5_covariance | MISSING_NO_CANCELLATION_ENVELOPE | no same-basis covariance/norm policy |
| REJ1481_6_Hom | HOM_PARENT_GENERATOR_NOT_DERIVED | source coefficient Hom remains live |

## Gates
| gate_id | gate_pass | claim_effect |
|---|---:|---|
| GATE1481_0_material_context | True | context only; not material tensor |
| GATE1481_1_full_tensor_missing | True | blocks WEP score |
| GATE1481_2_tau_blocked | True | K_CMSM/tau_WEP not score-ready |
| GATE1481_3_product_blocked | True | same-branch WEP runner refuses claim score |
| GATE1481_4_Hom_not_closed | True | source coefficient residuals remain live |
| GATE1481_5_rejection_complete | True | no WEP/local-GR promotion |

## Decision Ledger
- `DEC1481_0_material_status`: material context is harvested but not upgraded to claim-grade tensor — R_material remains partial/proxy-only.
- `DEC1481_1_tau_status`: tau/readout/source pack remains blocked — unit-kernel proxy remains quarantine only.
- `DEC1481_2_next_step`: build an official MICROSCOPE intake/acquisition runner next — 1482 should stage official file acquisition/provenance/schema checks or continue Hom generator proof if data remains unavailable.

## Validation
| check_id | result | detail |
|---|---|---|
| VAL1481_0_sources | PASS | all cited local source paths exist |
| VAL1481_1_mass_sums | PASS | PtRh10 and TA6V mass fractions sum to 1.0 |
| VAL1481_2_material_nonclaim | PASS | material context harvested but full tensor remains missing/nonclaim |
| VAL1481_3_tau_blocked | PASS | tau/source/readout pack remains blocked |
| VAL1481_4_product_blocked | PASS | same-branch product contract not score-ready |
| VAL1481_5_smoke_nonclaim | PASS | updated smoke rows remain nonclaim |
| VAL1481_6_Hom_open | PASS | Hom parent-generator proof remains open |
| VAL1481_7_rejection_blocks | PASS | rejection ledger blocks claim |
| VAL1481_8_gates_claim_false | PASS | all gates keep claim flags false |
| VAL1481_9_generated_csv_parse | PASS | all generated 1481 CSVs parse cleanly |
| VAL1481_10_branch_copies | PASS | nonclaim branch/quarantine copies written |
| VAL1481_11_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1481_12_formalization_untouched | PASS | formalization modified-file count since start=0 |
| VAL1481_13_overall | PASS | 1481 stages same-branch WEP material/tau/source pack as nonclaim and keeps Hom generator proof open |

## Source Register
| source_id | exists | path_or_url | usage |
|---|---:|---|---|
| SRC1481_0_prev_next | True | `source-intake\mts_residuals\P8_Y5_R10_1480_NEXT_TARGET.csv` | 1480 handoff selecting same-branch WEP pack or Hom generator proof |
| SRC1481_1_prev_validation | True | `source-intake\mts_residuals\P8_Y5_BRR545_1480_VALIDATION.csv` | 1480 validation baseline |
| SRC1481_2_prev_inputs | True | `source-intake\mts_residuals\P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_INPUT_MATRIX.csv` | same-branch WEP input matrix |
| SRC1481_3_prev_smoke | True | `source-intake\mts_residuals\P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv` | 1480 WEP smoke results |
| SRC1481_4_prev_proxy | True | `source-intake\mts_residuals\P8_Y5_R10_1480_PROXY_SMOKE_QUARANTINE_RESULTS.csv` | quarantined proxy smoke results |
| SRC1481_5_prev_rejection | True | `source-intake\mts_residuals\P8_Y5_R10_1480_RUNNER_REJECTION_LEDGER.csv` | runner rejection ledger |
| SRC1481_6_prev_Hom | True | `source-intake\mts_residuals\P8_Y5_R10_1480_COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT.csv` | coefficient-domain Hom attempt |
| SRC1481_7_prev_Hom_obstructions | True | `source-intake\mts_residuals\P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv` | Hom obstruction ledger |
| SRC1481_8_local_bounds | True | `source-intake\local_bounds\local_bound_claims.csv` | eta bound and local bound anchors |
| SRC1481_9_MAT651 | True | `source-intake\mts_residuals\P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv` | MICROSCOPE material model context |
| SRC1481_10_MAT983 | True | `source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv` | MICROSCOPE material constituents |
| SRC1481_11_PROXY983 | True | `source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv` | proxy material charge vectors |
| SRC1481_12_MCON1061 | True | `source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv` | WEP material convention |
| SRC1481_13_MREQ1068 | True | `source-intake\mts_residuals\P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv` | material response requirements |
| SRC1481_14_MAT1080 | True | `source-intake\mts_residuals\P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv` | material tensor candidates |
| SRC1481_15_NOCANCEL1087 | True | `source-intake\mts_residuals\P8_Y5_R10_1087_ALL_MATERIAL_NO_CANCELLATION_POLICY.csv` | all-material no-cancellation policy |
| SRC1481_16_WCM1053 | True | `source-intake\mts_residuals\P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv` | WEP composition charge matrix |
| SRC1481_17_MAT1424 | True | `source-intake\mts_residuals\P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv` | Ti/Pt material vector candidates |
| SRC1481_18_FSP1232 | True | `source-intake\mts_residuals\P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv` | Ti/Pt component fraction source pack |
| SRC1481_19_FORM1232 | True | `source-intake\mts_residuals\P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv` | component fraction formula ledger |
| SRC1481_20_WAIT1335 | True | `source-intake\mts_residuals\P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv` | readout/source waitstate |
| SRC1481_21_MAN1335 | True | `source-intake\mts_residuals\P8_Y5_R10_1335_OFFICIAL_INPUT_REQUEST_MANIFEST.csv` | official input request manifest |
| SRC1481_22_WPN1335 | True | `source-intake\mts_residuals\P8_Y5_R10_1335_ELECTRON_WEP_PRODUCT_NORMALIZATION_CONTRACT.csv` | electron WEP product normalization contract |
| SRC1481_23_TAU1335 | True | `source-intake\mts_residuals\P8_Y5_R10_1335_EPSILON_E_BOUND_RESCALING_TABLE.csv` | epsilon_e tau sensitivity table |
| SRC1481_24_INTAKE1228 | True | `source-intake\mts_residuals\P8_Y5_R10_1228_INTAKE_DIRECTORY_CONTRACT.csv` | MICROSCOPE intake directory contract |
| SRC1481_25_ACCEPT1228 | True | `source-intake\mts_residuals\P8_Y5_R10_1228_ACCEPTANCE_GATE_MATRIX.csv` | MICROSCOPE acceptance gates |
| SRC1481_26_FEED1228 | True | `source-intake\mts_residuals\P8_Y5_R10_1228_TAU_WEP_FEED_UPDATE.csv` | tau_WEP feed update |
| SRC1481_27_PACK1426 | True | `source-intake\mts_residuals\P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv` | finite WEP coefficient input pack |
| SRC1481_28_PFT1050 | True | `source-intake\mts_residuals\P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv` | product functor theorem attempt |
| SRC1481_29_NMM1051 | True | `source-intake\mts_residuals\P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv` | no mixed morphism lemma |
| SRC1481_30_VOE1058 | True | `source-intake\mts_residuals\P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv` | visible operator-domain exhaustion attempt |
| SRC1481_31_NMF980 | True | `source-intake\mts_residuals\P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv` | no-marker functor theorem attempt |

## Next Target
- `1482-Y5-R10-RAB-MICROSCOPE-official-readout-source-intake-runner-or-Hom-generator-closure.md` via `scripts/Y5_R10_RAB_MICROSCOPE_official_readout_source_intake_runner_or_Hom_generator_closure.py`: try to acquire or stage official MICROSCOPE readout/source-worldtube/product-convention inputs with provenance/schema gates; if unavailable, sharpen the parent-generator closure proof for Hom exclusion
