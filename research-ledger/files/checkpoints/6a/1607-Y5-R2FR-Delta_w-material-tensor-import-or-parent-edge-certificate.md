# 1607 - R2/fR Delta_w Material Tensor Import Or Parent Edge Certificate

## Verdict
- 1607 audits the finite `Delta_w` material route instead of trying to zero the coupling by physical connectedness alone.
- The current corpus has useful Ti/Pt composition context plus electron, Coulomb, and surface/binding proxy/smoke sensitivities, but not a full MTS parent material-response tensor.
- The electron proxy is explicitly quarantined: `DeltaF_e * delta_w_e_proxy` reconstructs the `2.8e-15` MICROSCOPE product-bound anchor, so it is bound-inverted smoke, not a prediction.
- Parent-edge certificate route remains open but unproved; material tensor rows can bound finite residuals but cannot by themselves theorem-zero `Delta_w_A`.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1607_0_1606_doc | 1606-Y5-R2FR-parent-owned-matter-graph-or-Delta_w-component-bound-pack.md | True | True | POG1606_4_verdict; PARENT_OWNED_GRAPH_NOT_DERIVED |
| SRC1607_1_1606_validation | source-intake/mts_residuals/P8_Y5_BRR545_1606_VALIDATION.csv | True | True | VAL1606_OVERALL; PASS |
| SRC1607_2_1606_pack | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv | True | True | DWB1606_1_delta_w_e; PROXY_UNIT_KERNEL_ONLY |
| SRC1607_3_1606_readiness | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1606_DELTA_W_SCORE_READINESS.csv | True | True | READY1606_5_verdict; Delta_w branch score-ready |
| SRC1607_4_1606_edges | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1606_PARENT_OWNED_EDGE_AUDIT.csv | True | True | EDGE1606_7_verdict; NOT_PARENT_CERTIFIED |
| SRC1607_5_1606_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1606_NEXT_TARGET.csv | True | True | 1607-Y5-R2FR-Delta_w-material-tensor-import-or-parent-edge-certificate.md; parent material-response tensor |
| SRC1607_6_1595_bound_anchor | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_SOURCE_BACKED_BETA_DELTAW_CANDIDATE.csv | True | True | SBC1595_0_MICROSCOPE_Delta_w_tau_bound_anchor; absolute product bound |
| SRC1607_7_1595_claim_limits | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_CANDIDATE_CLAIM_LIMITS.csv | True | True | CLM1595_3_material_map_missing; material map missing |
| SRC1607_8_1595_next_inputs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1595_NEXT_INPUT_REQUIREMENTS.csv | True | True | NIR1595_2_material_map; Ti/Pt response tensor |
| SRC1607_9_1481_material_context | source-intake/microscope/branch_locked_wep/coefficients/WEP_material_context_pack_nonclaim_1481.csv | True | True | MAT1481_6_full_tensor; MISSING_FULL_PARENT_MATERIAL_TENSOR |
| SRC1607_10_1479_component_pack | source-intake/microscope/branch_locked_wep/coefficients/component_delta_w_bound_pack_nonclaim_1479.csv | True | True | CBP1479_1_delta_w_e; PROXY_UNIT_KERNEL_ONLY |
| SRC1607_11_983_constituents | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | True | True | M983_0_PtRh10; M983_1_TiAlloy |
| SRC1607_12_1424_material_vectors | source-intake/mts_residuals/P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv | True | True | MAT1424_2_electron_mass_fraction; AUDITED_NUMERIC_PARENT_NORMALIZATION_MISSING |
| SRC1607_13_983_proxy_vectors | source-intake/mts_residuals/P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv | True | True | M983_0_PtRh10; proxy_charge_vector_computed |
| SRC1607_14_1053_charge_matrix | source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv | True | True | WCM1053_6; MISSING_FULL_MATERIAL_TENSOR |
| SRC1607_15_1080_tensor_candidates | source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv | True | True | MAT1080_4_full_tensor_upgrade; MISSING_FULL_MATERIAL_TENSOR |

## Material Tensor Import Schema

| schema_id | field | required_policy |
| --- | --- | --- |
| MTS1607_0_row_id | row_id | stable tensor row id |
| MTS1607_1_composition_pair | composition_pair | TA6V_minus_PtRh10 or declared source/test pair |
| MTS1607_2_component | component | electron/EM_Coulomb/light_quark/QCD_gluon/nuclear_binding/measure_J/current_c/nonHilbert_zeta/other_parent_component |
| MTS1607_3_sensitivity_value | sensitivity_value | finite numeric tensor component or DERIVED_ZERO |
| MTS1607_4_sensitivity_uncertainty | sensitivity_uncertainty | numeric uncertainty/interval or exact theorem tag |
| MTS1607_5_units | units | dimensionless sensitivity in declared MTS parent WEP basis |
| MTS1607_6_sign_convention | sign_convention | TA6V_minus_PtRh10 and positive-couples-stronger convention |
| MTS1607_7_basis | basis | MTS parent material-response basis; external DD smoke basis must be labelled proxy |
| MTS1607_8_source_path | source_path | local artifact, DOI, or URL; local path must exist |
| MTS1607_9_source_anchor | source_anchor | row/table/equation anchor |
| MTS1607_10_parent_owner_status | parent_owner_status | PARENT_OWNED/SOURCE_BACKED_CONTEXT/PROXY_NONCLAIM/MISSING |
| MTS1607_11_no_bound_inversion | no_bound_inversion | true for claim-grade rows; false/templates rejected |
| MTS1607_12_no_double_counting_rule | no_double_counting_rule | states component independence/covariance rule |
| MTS1607_13_valid_for_claim | valid_for_claim | false until full tensor, tau, source/readout and component gates pass |
| MTS1607_14_claim_allowed | claim_allowed | false until full local branch gates pass |

## Material Tensor Import Template

| row_id | component | sensitivity_value | basis | parser_status |
| --- | --- | --- | --- | --- |
| MTT1607_0_electron | electron | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_1_EM_Coulomb | EM_Coulomb | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_2_light_quark | light_quark | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_3_QCD_gluon | QCD_gluon | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_4_nuclear_binding | nuclear_binding | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_5_measure_J | measure_J | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_6_current_c | current_c | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |
| MTT1607_7_nonHilbert_zeta | nonHilbert_zeta | MISSING_PARENT_MATERIAL_TENSOR_COMPONENT | MISSING_MTS_PARENT_WEP_MATERIAL_RESPONSE_BASIS | TEMPLATE_ONLY_NOT_IMPORTABLE |

## Material Tensor Context Audit

| audit_id | object | value_or_status | usable_level | why_not_claim |
| --- | --- | --- | --- | --- |
| MTA1607_0_pair_convention | MICROSCOPE Ti/Pt pair convention | TA6V_minus_PtRh10 | CONTEXT_ONLY | pair convention does not supply parent material-response tensor |
| MTA1607_1_composition | PtRh10 and TA6V alloy mass fractions | PtRh10=Pt0.90/Rh0.10;TA6V=Ti0.90/Al0.06/V0.04 | SOURCE_BACKED_COMPOSITION_CONTEXT | composition is not an MTS parent response tensor |
| MTA1607_2_electron_fraction_proxy | electron rest-mass fraction contrast | 3.129116287420e-05 | AUDITED_NUMERIC_PROXY | parent mass functional and source/readout/tau normalization missing |
| MTA1607_3_DD_alpha_smoke | external DD alpha/Coulomb contrast | -1.989808886825e-03 | EXTERNAL_SMOKE_NUMERIC_NOT_PARENT_BASIS | MTS parent EM/Coulomb owner and basis map missing |
| MTA1607_4_DD_surface_smoke | external DD surface/binding contrast | -3.306456347405e-03 | EXTERNAL_SMOKE_NUMERIC_NOT_FULL_TENSOR | full nuclear/isotopic tensor and MTS basis map missing |
| MTA1607_5_full_tensor | full R_TA6V_minus_PtRh10 material tensor | MISSING_FULL_PARENT_MATERIAL_TENSOR | BLOCKED | parent response basis, isotope/alloy averaging, component covariance and source/readout environment stack missing |

## Component Sensitivity Pack

| sensitivity_id | component | sensitivity_value | status | why_not_claim |
| --- | --- | --- | --- | --- |
| SEN1607_0_electron | electron | 3.129116287420e-05 | AUDITED_NUMERIC_PROXY_PARENT_NORMALIZATION_MISSING | electron rest-mass fraction contrast; not parent mass functional |
| SEN1607_1_EM_Coulomb | EM_Coulomb | -1.989808886825e-03 | DD_SMOKE_NOT_MTS_PARENT_BASIS | external DD Coulomb smoke contrast only |
| SEN1607_2_nuclear_surface | nuclear_binding | -3.306456347405e-03 | DD_SMOKE_NOT_FULL_TENSOR | external DD surface/binding smoke contrast only |
| SEN1607_3_light_quark | light_quark | MISSING_PARENT_COMPONENT_SENSITIVITY | MISSING | light-quark/sigma material sensitivity not sourced |
| SEN1607_4_QCD_gluon | QCD_gluon | MISSING_PARENT_COMPONENT_SENSITIVITY | MISSING | QCD/gluon/bulk material sensitivity not sourced |
| SEN1607_5_measure_J | measure_J | MISSING_PARENT_COMPONENT_SENSITIVITY | MISSING | species-measure/Jacobian sensitivity not sourced |
| SEN1607_6_current_c | current_c | MISSING_PARENT_COMPONENT_SENSITIVITY | MISSING | current/source normalization sensitivity not sourced |
| SEN1607_7_nonHilbert_zeta | nonHilbert_zeta | MISSING_PARENT_COMPONENT_SENSITIVITY | MISSING | non-Hilbert/readout sensitivity not sourced |

## Bound-Inversion Audit

| audit_id | formula | computed_value | comparison_anchor | status | effect |
| --- | --- | --- | --- | --- | --- |
| BIA1607_0_electron_proxy_product | abs(DeltaF_e_TiPt * delta_w_e_proxy) | 2.799999999999850E-15 | MICROSCOPE product-bound anchor 2.8e-15 | BOUND_INVERSION_PROXY_DETECTED | may be used as nonclaim smoke/validator check only, not as MTS prediction |
| BIA1607_1_missing_tau | abs(Delta_w_TiPt*tau_WEP) <= bound cannot become abs(Delta_w_TiPt) <= bound/tau without tau_WEP | NOT_COMPUTABLE | NIR1595_0_tau_WEP | TAU_WEP_MISSING_BLOCKS_BOUND_INVERSION | Delta_w prior width remains blocked |
| BIA1607_2_material_map_missing | Delta_w_TiPt = DeltaF_TiPt dot delta_w_component_vector + residuals | NOT_COMPUTABLE | NIR1595_2_material_map;MAT1481_6_full_tensor | FULL_MATERIAL_TENSOR_MISSING | no WEP material score |

## Parent Edge Certificate Status

| edge_id | target | current_status | effect |
| --- | --- | --- | --- |
| PEC1607_0_parent_edge_certificate | prove QED/QCD/Yukawa/binding/material edges are parent-owned L_action morphisms | NOT_DERIVED | cannot theorem-zero Delta_w_component_vector |
| PEC1607_1_material_tensor_vs_edge | use material tensor as finite route, not graph-zero proof | FINITE_ROUTE_ONLY | material import can bound components but cannot by itself collapse w_A to w_* |
| PEC1607_2_verdict | parent edge certificate route | PARENT_EDGE_CERTIFICATE_MISSING | continue finite vector route or source parent-edge theorem |

## Score Readiness

| readiness_id | requirement | ready | blocker |
| --- | --- | --- | --- |
| READY1607_0_full_tensor | full parent material-response tensor | False | MAT1080_4/MAT1481_6 remain MISSING_FULL_PARENT_MATERIAL_TENSOR |
| READY1607_1_component_sensitivities | all component sensitivities numeric or theorem-zero | False | electron/EM/nuclear are proxy/smoke; light-quark/QCD/measure/current/NH missing |
| READY1607_2_bound_inversion | no bound-inverted component proxies | False | electron proxy product equals MICROSCOPE bound anchor |
| READY1607_3_tau_readout | tau_WEP/source worldtube/readout kernel exists | False | NIR1595 tau/source/readout requirements remain open |
| READY1607_4_parent_edges | parent-owned edge certificate exists | False | PEC1607 keeps edge route missing |
| READY1607_5_verdict | Delta_w material branch score-ready | False | full tensor/component/tau/readout/edge gates open |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1607_0_material_tensor_import | material tensor import must supply all declared component sensitivities, units, sign, MTS parent basis, source anchors, covariance/no-double-counting rule | context/proxy/smoke rows only; full parent tensor missing | MATERIAL_TENSOR_NOT_SCORE_READY | finite Delta_w_TiPt score blocked |
| RUN1607_1_bound_inversion_firewall | component values derived from empirical bound inversion cannot be treated as theory predictions | electron proxy product reconstructs 2.8e-15 bound | REJECT_BOUND_INVERTED_PROXY_AS_PREDICTION | electron proxy retained only as nonclaim smoke check |
| RUN1607_2_parent_edge_certificate | parent edge certificate must be an explicit parent action graph theorem/source, not physical connectedness alone | no parent-edge source imported | REJECT_PARENT_EDGE_THEOREM_ZERO | no Delta_w theorem-zero |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1607_0_material_tensor | full Ti/Pt parent material-response tensor | BLOCKED | full tensor missing; proxies/smoke only |
| CG1607_1_component_sensitivities | component sensitivity pack score | BLOCKED | not all components sourced/numeric/theorem-zero |
| CG1607_2_bound_firewall | bound-inverted proxy as prediction | BLOCKED | electron proxy reconstructs product bound |
| CG1607_3_parent_edges | parent-owned graph theorem-zero | BLOCKED | no parent edge certificate |
| CG1607_4_tau_readout | tau_WEP/source/readout projection | BLOCKED | tau/source/readout kernel still missing |
| CG1607_5_WEP_local_GR | WEP/Newton/local-GR claim | BLOCKED | material/tau/coupling gates open |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1607_0_material_route | MATERIAL_TENSOR_CONTEXT_READY_FULL_TENSOR_MISSING | composition/proxy/smoke rows exist, but not a full MTS parent material-response tensor | source/import claim-safe Ti/Pt parent material tensor or keep material score blocked |
| DEC1607_1_bound_proxy | BOUND_INVERTED_ELECTRON_PROXY_QUARANTINED | electron sensitivity times delta_w_e proxy reconstructs the 2.8e-15 empirical bound | do not treat electron proxy as prediction; require parent coefficient or independent source-backed component value |
| DEC1607_2_next | NEXT_1608_TAU_WEP_READOUT_KERNEL_OR_MATERIAL_TENSOR_SOURCE_FILE | material tensor remains missing, and tau/source/readout is required before any bound or material row becomes a WEP score | derive/source tau_WEP and readout kernel, or import a real Ti/Pt parent material tensor file into the 1607 input schema |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1608-Y5-R2FR-tau-WEP-readout-kernel-or-material-tensor-source-file.md | scripts/Y5_R2FR_tau_WEP_readout_kernel_or_material_tensor_source_file.py | derive/source tau_WEP and MICROSCOPE readout/source projection, or import a real Ti/Pt parent material tensor through the 1607 schema | claim-safe nonclaim tau/readout/material input that is independent of bound inversion, with units/sign/source anchors; no WEP/local-GR claim until all gates pass | do not use bound inversion, tau_eff=1, DD-only proxies, physical connectedness alone, closure-only zero, measured-G absorption, or public/local-GR claims |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1607_0_sources_exist | PASS | all cited 1607 local source paths exist |
| VAL1607_1_needles_found | PASS | all required 1607 source needles found |
| VAL1607_2_tensor_schema | PASS | material tensor import schema written |
| VAL1607_3_template_nonimportable | PASS | material tensor template remains nonimportable |
| VAL1607_4_full_tensor_missing | PASS | full parent material tensor remains missing |
| VAL1607_5_sensitivities_nonclaim | PASS | component sensitivity rows remain nonclaim |
| VAL1607_6_bound_inversion_detected | PASS | electron proxy bound inversion detected |
| VAL1607_7_parent_edge_missing | PASS | parent edge certificate remains missing |
| VAL1607_8_score_not_ready | PASS | Delta_w material branch remains not score-ready |
| VAL1607_9_runner_refuses_claims | PASS | runner refuses bound-inverted proxy as prediction |
| VAL1607_10_claim_gates_closed | PASS | all 1607 claim gates remain closed |
| VAL1607_11_decision_next | PASS | decision selects 1608 tau/readout or material tensor source file |
| VAL1607_12_csv_parse | PASS | all generated 1607 CSVs parse |
| VAL1607_13_claim_safety_flags | PASS | no generated 1607 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed |
| VAL1607_14_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1607_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1607_16_formalization_untouched | PASS | no 1607 outputs found under formalization-workbench |
| VAL1607_OVERALL | PASS | 1607 Delta_w material tensor import or parent edge certificate validation |
