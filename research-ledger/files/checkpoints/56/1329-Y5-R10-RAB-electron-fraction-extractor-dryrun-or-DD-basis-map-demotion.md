# 1329-Y5-R10-RAB-electron-fraction-extractor-dryrun-or-DD-basis-map-demotion

**Current verdict:** 1329 gets the first real numeric component dry-run into the source pipeline: the electron rest-mass fraction contrast between TA6V and PtRh10 is finite, schema-shaped, and nonclaim. This is progress, not a WEP or local-GR pass.

**Main progress:** the electron component is now concrete enough to inspect. The dry-run gives `Delta F_e(TA6V-PtRh10) = 3.129116287540e-05` with a deliberately conservative nonclaim envelope `3.359523483104e-06`.

**Decision:** keep the calculation as a partial component row. The full `Delta_w_TiPt` branch still needs light-quark, QCD/gluon, EM/Coulomb, nuclear surface, measure/readout, and the parent basis map.

## Source Register
| source_id | local_path | needle | exists | needle_found | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC1329_0_1328_next | source-intake/mts_residuals/P8_Y5_R10_1328_NEXT_TARGET.csv | NEXT1328_0_1329 | True | True | selected 1329 target | False | False |
| SRC1329_1_1328_public_sources | source-intake/mts_residuals/P8_Y5_R10_1328_PUBLIC_SOURCE_CANDIDATE_REGISTER.csv | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | True | True | electron source candidate provenance | False | False |
| SRC1329_2_1328_route_matrix | source-intake/mts_residuals/P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv | ROUTE1328_TA6V_electron | True | True | electron route matrix | False | False |
| SRC1329_3_1233_schema | source-intake/mts_residuals/P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | fraction_value | True | True | component fraction schema | False | False |
| SRC1329_4_983_material_constituents | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | M983_1_TiAlloy | True | True | local MICROSCOPE constituent rows | False | False |
| SRC1329_5_1080_material_context | source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv | MAT1080_1_TA6V_MICROSCOPE | True | True | source-backed material context and nonclaim gate | False | False |
| SRC1329_6_1328_validation | source-intake/mts_residuals/P8_Y5_BRR545_1328_VALIDATION.csv | VAL1328_11_overall | True | True | 1328 pass gate | False | False |

## Electron Fraction Input Constants
| constant_id | symbol | value | units | source | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONST1329_0_m_e_u | m_e/u | 5.485799090650e-04 | dimensionless atomic-mass-unit ratio | CODATA/NIST electron mass in atomic mass units; manual dry-run constant | MANUAL_DRYRUN_CONSTANT_NOT_CLAIM_GRADE | False | False |
| CONST1329_Ti_atomic_weight | A_std(Ti) | 47.867 | u | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION | False | False |
| CONST1329_Al_atomic_weight | A_std(Al) | 26.9815385 | u | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION | False | False |
| CONST1329_V_atomic_weight | A_std(V) | 50.9415 | u | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION | False | False |
| CONST1329_Pt_atomic_weight | A_std(Pt) | 195.084 | u | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION | False | False |
| CONST1329_Rh_atomic_weight | A_std(Rh) | 102.9055 | u | PSRC1328_3_NIST_atomic_weights_isotopic_compositions | MANUAL_DRYRUN_VALUE_NOT_AUDITED_EXTRACTION | False | False |

## Element Contributions
| contribution_id | material_id | element | mass_fraction | Z | A_microscope_context | A_nist_standard_weight | microscope_A_contribution | nist_weight_contribution | source | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EFC1329_TA6V_Ti | TA6V | Ti | 0.90 | 22 | 47.9 | 47.867 | 2.267616325571e-04 | 2.269179643489e-04 | WEB983_0_MICROSCOPE_CQG_COMPOSITION;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE | False | False |
| EFC1329_TA6V_Al | TA6V | Al | 0.06 | 13 | 27.0 | 26.9815385 | 1.584786403966e-05 | 1.585870757780e-05 | WEB983_0_MICROSCOPE_CQG_COMPOSITION;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE | False | False |
| EFC1329_TA6V_V | TA6V | V | 0.04 | 23 | 50.9 | 50.9415 | 9.915393248326e-06 | 9.907315574528e-06 | WEB983_0_MICROSCOPE_CQG_COMPOSITION;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE | False | False |
| EFC1329_PtRh10_Pt | PtRh10 | Pt | 0.90 | 78 | 195.1 | 195.084 | 1.973875428824e-04 | 1.974037318097e-04 | WEB983_0_MICROSCOPE_CQG_COMPOSITION;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE | False | False |
| EFC1329_PtRh10_Rh | PtRh10 | Rh | 0.10 | 45 | 102.9 | 102.9055 | 2.399037503200e-05 | 2.398909281615e-05 | WEB983_0_MICROSCOPE_CQG_COMPOSITION;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | DRYRUN_CONTRIBUTION_NOT_CLAIM_GRADE | False | False |

## Electron Fraction Dry-Run Rows
| row_id | material_id | component_id | fraction_value | fraction_uncertainty | basis_convention | source_path_or_url | extraction_method | microscope_A_crosscheck_fraction | uncertainty_model | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFI1329_TA6V_electron | TA6V | electron | 2.526839875012e-04 | 2.526839875012e-06 | other_with_source | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | formula | 2.525248898451e-04 | max(1_percent_dryrun_envelope, abs(NIST_standard_weight_fraction - MICROSCOPE_A_context_fraction)) | SCHEMA_VALID_NUMERIC_DRYRUN_NONCLAIM | False | False |
| CFI1329_PtRh10_electron | PtRh10 | electron | 2.213928246258e-04 | 2.213928246258e-06 | other_with_source | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | formula | 2.213779179144e-04 | max(1_percent_dryrun_envelope, abs(NIST_standard_weight_fraction - MICROSCOPE_A_context_fraction)) | SCHEMA_VALID_NUMERIC_DRYRUN_NONCLAIM | False | False |

## Raw Candidate File
Schema-shaped nonclaim candidate written to:

`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\component-fractions\raw\P8_Y5_R10_1329_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv`

| row_id | material_id | component_id | fraction_value | fraction_uncertainty | basis_convention | source_path_or_url | extraction_method | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CFI1329_TA6V_electron | TA6V | electron | 2.526839875012e-04 | 2.526839875012e-06 | other_with_source | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | formula | False |
| CFI1329_PtRh10_electron | PtRh10 | electron | 2.213928246258e-04 | 2.213928246258e-06 | other_with_source | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv;PSRC1328_3_NIST_atomic_weights_isotopic_compositions | formula | False |

## Electron Delta Vector
| delta_id | component_id | left_material | right_material | delta_fraction | abs_delta_fraction | delta_uncertainty | interpretation | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DELTA1329_0_TA6V_minus_PtRh10_electron | electron | TA6V | PtRh10 | 3.129116287540e-05 | 3.129116287540e-05 | 3.359523483104e-06 | electron rest-mass fraction contrast only; not WEP and not full Delta_w_TiPt | NUMERIC_DRYRUN_NONCLAIM | False | False |

## Acceptance Ledger
| acceptance_id | target | status | details | blocks_claim | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| ACC1329_0_schema_rows | raw electron candidate rows | SCHEMA_VALID_NUMERIC_NONCLAIM | raw_path=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\component-fractions\raw\P8_Y5_R10_1329_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv;rows=2 | True | False | False |
| ACC1329_1_numeric_values | fraction_value and fraction_uncertainty | FINITE_NUMERIC | all electron dry-run rows finite; uncertainty is dry-run envelope not source-grade | True | False | False |
| ACC1329_2_parent_normalization | MTS parent mass-normalization convention | MISSING_PARENT_SIGNATURE | electron rest mass is measurable, but parent must still sign whether this is the source-weight component used in Delta_w | True | False | False |
| ACC1329_3_component_completeness | full Delta_w_TiPt component vector | INCOMPLETE_ONE_COMPONENT_ONLY | light_quark, QCD_gluon, EM_Coulomb, nuclear_surface, and measure_readout remain unresolved | True | False | False |

## DD Basis Map Demotion Ledger
| demotion_id | object | status | reason | needed_for_promotion | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| DD1329_0_parent_basis_map | Damour-Donoghue charge basis | DEMOTED_TO_EXTERNAL_COMPARATOR | DD charges are valuable physics, but not derived from the MTS parent action in the current corpus | explicit parent basis map from MTS source weights to DD charge vector with no double counting | False | False |
| DD1329_1_alpha_surface_smoke | existing alpha/surface smoke deltas | KEEP_QUARANTINED | smoke deltas are useful comparator pressure, not a full material response tensor | source-backed component fractions and parent coefficient map | False | False |

## Delta-w Runner Update
| runner_id | target | input_status | runner_status | reason | score_ready | valid_prediction_row | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN1329_0_electron_component | electron component of finite Delta_w_TiPt | NUMERIC_DRYRUN_AVAILABLE_NONCLAIM | PARTIAL_COMPONENT_READY_NOT_SCOREABLE | electron contrast is numeric, but one component cannot score WEP or close local GR | False | False | False | False |
| RUN1329_1_full_Delta_w | full Delta_w_TiPt source vector | MISSING_NON_ELECTRON_COMPONENTS_AND_PARENT_MAP | REFUSED_NOT_SCOREABLE | quark/QCD/EM/nuclear/readout components and parent basis map remain missing | False | False | False | False |

## Anti-Shortcut Gates
| gate_id | shortcut | enforcement | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| SHORT1329_0_no_electron_only_WEP | score WEP from electron fraction contrast alone | REFUSED | ENFORCED | False | False |
| SHORT1329_1_no_NIST_manual_as_claim | treat manually entered atomic weights as audited claim-grade extraction | REFUSED until a table/digitization extractor is audited | ENFORCED | False | False |
| SHORT1329_2_no_DD_parent_basis_shortcut | promote DD charges to MTS parent basis | REFUSED by DD demotion ledger | ENFORCED | False | False |
| SHORT1329_3_no_local_GR_claim | turn one component dry-run into local-GR pass | REFUSED | ENFORCED | False | False |

## Decision Ledger
| decision_id | decision | because | effect | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC1329_0_electron_progress | electron component is now numeric in dry-run form | composition and mass-normalization inputs are concrete enough for a nonclaim formula pass | we have the first real component contrast, but no full Delta_w or WEP score | False | False |
| DEC1329_1_next_bottleneck | next bottleneck is parent basis mapping or audited extraction | electron fraction alone is clean but too small a slice of the source vector | move to either audited atomic/isotope extraction or parent DD/QCD map gate | False | False |

## Next Target
| next_id | target_file | target_script | task | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT1329_0_1330 | 1330-Y5-R10-RAB-audited-electron-source-extractor-or-parent-DD-map-gate.md | scripts/Y5_R10_RAB_audited_electron_source_extractor_or_parent_DD_map_gate.py | replace manual atomic-weight constants with an audited source extractor, or attempt the parent map from MTS source weights to external DD charges | electron fraction rows become audit-extracted nonclaim inputs, or DD remains explicitly demoted with a sharper parent-map theorem blocker | do not score WEP, do not promote DD to parent MTS, do not claim Delta_w=0, and do not claim local GR | False | False |

## Validation
| check_id | check | status | details |
| --- | --- | --- | --- |
| VAL1329_0_sources_exist | registered local source paths exist and anchors are found | PASS | 7/7 source anchors found |
| VAL1329_1_raw_candidate_schema | raw electron candidate file exists with 1233 schema fields | PASS | raw_path=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\component-fractions\raw\P8_Y5_R10_1329_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv;raw_rows=2 |
| VAL1329_2_numeric_rows | electron fraction rows and delta are finite numeric dry-run values | PASS | TA6V=2.526839875012e-04;PtRh10=2.213928246258e-04;delta=3.129116287540e-05 |
| VAL1329_3_raw_rows_nonclaim | raw candidate rows remain valid_for_claim=false | PASS | raw electron candidate rows are schema-valid but nonclaim |
| VAL1329_4_one_component_only | dry-run is explicitly electron component only | PASS | non-electron source components remain unresolved |
| VAL1329_5_DD_demoted | DD basis remains external comparator only | PASS | DD1329_0_parent_basis_map=DEMOTED_TO_EXTERNAL_COMPARATOR;DD1329_1_alpha_surface_smoke=KEEP_QUARANTINED |
| VAL1329_6_runner_not_scoreable | Delta_w and WEP runners are not score-ready | PASS | RUN1329_0_electron_component=PARTIAL_COMPONENT_READY_NOT_SCOREABLE;RUN1329_1_full_Delta_w=REFUSED_NOT_SCOREABLE |
| VAL1329_7_shortcuts_enforced | anti-shortcut gates are enforced | PASS | SHORT1329_0_no_electron_only_WEP;SHORT1329_1_no_NIST_manual_as_claim;SHORT1329_2_no_DD_parent_basis_shortcut;SHORT1329_3_no_local_GR_claim |
| VAL1329_8_nonclaim_policy | all generated rows remain nonclaim | PASS | valid_for_claim=false and claim_allowed=false where present |
| VAL1329_9_formalization_untouched | formalization-workbench untouched by generated outputs | PASS | formalization_generated_output_count=0 |
| VAL1329_10_next_target_1330 | next target routes to audited electron extractor or parent DD map gate | PASS | 1330-Y5-R10-RAB-audited-electron-source-extractor-or-parent-DD-map-gate.md |
| VAL1329_11_overall | overall 1329 validation | PASS | 1329 produces the first numeric nonclaim electron component dry-run and refuses WEP/local-GR promotion |
