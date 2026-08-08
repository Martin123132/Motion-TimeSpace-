# 1909 - Ti/Pt Alloy Material-Binding Projection Or Blocker Ledger

## Purpose

This checkpoint tries to upgrade the 1908 natural Ti/Pt element stub into the actual MICROSCOPE alloy/material branch. It succeeds only at the scaffold level: PtRh10 and TA6V alloy composition plus a differential proxy vector are now source-backed local nonclaim rows, but the binding/material response tensor and readout/source contraction remain absent.

## Result

- PtRh10 and TA6V alloy mass-fraction composition is now staged as source-backed context.
- The branch sign convention is locked to `TA6V_minus_PtRh10`, matching the existing MICROSCOPE WEP material convention rows.
- A single nonclaim proxy vector now carries `Z/A`, `N/A`, neutron-excess, electron-rest-mass, Coulomb-proxy, and `Abar` contrasts.
- Material-binding projection is explicitly blocked by six separated blockers.
- No WEP, local-GR, or material-response claim is promoted.

## Source Register

| source_id | source_path | exists | needle_count | missing_needles | status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1908_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1908-Y5-R2FR-graph-source-extraction-and-TiPt-component-projection.md | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1908_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1908_VALIDATION.csv | True | 1 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1908_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1908_NEXT_TARGET.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1908_isotopes | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1908_TIPT_NIST_ISOTOPE_COMPONENTS_SOURCE_BACKED_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1908_element_stub | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1908_TIPT_ELEMENT_LEVEL_PROJECTION_STUB_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1908_graph_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1908_GRAPH_SOURCE_EXTRACTION_STATUS_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 983_constituents | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 983_proxy_vectors | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1061_material_convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1424_material_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1330_electron_fractions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\component-fractions\raw\P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1481_context_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\coefficients\WEP_material_context_pack_nonclaim_1481.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1607_tensor_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\R2FR_material_tensor_context_audit_nonclaim_1607.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |
| 1900_official_data | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | True | 2 |  | EXISTS_NEEDLES_CONFIRMED | False | 2026-06-19T19:58:27.242913+00:00 |

## Web Source Ledger

| source_id | source_url | role | extracted_or_used | source_status | source_backed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WEB1909_0_MICROSCOPE_FINAL_PRL_ARXIV | https://arxiv.org/abs/2209.15487 | final MICROSCOPE WEP result and Ti/Pt alloy experiment context | bound/context only; no official readout arrays imported | SOURCE_URL_RECORDED_CONTEXT_ONLY | True | False |
| WEB1909_1_MICROSCOPE_CQG_RESULT | https://arxiv.org/abs/2209.15488 | long-form MICROSCOPE WEP analysis and material/readout context | composition convention cross-check; no source-worldtube kernel imported | SOURCE_URL_RECORDED_CONTEXT_ONLY | True | False |
| WEB1909_2_MICROSCOPE_CQG_DOI | https://doi.org/10.1088/1361-6382/ac84be | published CQG DOI for WEP result | bibliographic provenance for local nonclaim composition context | DOI_RECORDED | True | False |
| WEB1909_3_MICROSCOPE_MISSION_COMPOSITION | https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | mission summary source for PtRh10 and TA6V composition convention | supports PtRh10=90% Pt/10% Rh and TA6V=90% Ti/6% Al/4% V context already present in local 983 rows | SOURCE_URL_RECORDED_COMPOSITION_CONTEXT | True | False |
| WEB1909_4_NIST_ISOTOPIC_CONTEXT | https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl | natural isotope/atomic weight context from 1908 | Ti/Pt extracted in 1908; Al/V/Rh exact isotope expansion still not imported here | PARTIAL_COMPONENT_SOURCE_RECORDED | True | False |

## Alloy Composition Rows

| composition_id | material_id | element | mass_fraction | A_context | Z | source_row | local_source_path | web_source_context | mass_fraction_sum_for_material | source_backed_composition_context | exact_flight_isotope_mix | binding_decomposed | readout_corrected | valid_projection_row | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AC1909_PtRh10_Pt | PtRh10 | Pt | 0.900000000000 | 195.1 | 78 | WEB983_0_MICROSCOPE_CQG_COMPOSITION | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | https://arxiv.org/abs/2209.15488; https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | 1.000000000000 | True | False | False | False | False | False |
| AC1909_PtRh10_Rh | PtRh10 | Rh | 0.100000000000 | 102.9 | 45 | WEB983_0_MICROSCOPE_CQG_COMPOSITION | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | https://arxiv.org/abs/2209.15488; https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | 1.000000000000 | True | False | False | False | False | False |
| AC1909_TA6V_Ti | TA6V | Ti | 0.900000000000 | 47.9 | 22 | WEB983_0_MICROSCOPE_CQG_COMPOSITION | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | https://arxiv.org/abs/2209.15488; https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | 1.000000000000 | True | False | False | False | False | False |
| AC1909_TA6V_Al | TA6V | Al | 0.060000000000 | 27.0 | 13 | WEB983_0_MICROSCOPE_CQG_COMPOSITION | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | https://arxiv.org/abs/2209.15488; https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | 1.000000000000 | True | False | False | False | False | False |
| AC1909_TA6V_V | TA6V | V | 0.040000000000 | 50.9 | 23 | WEB983_0_MICROSCOPE_CQG_COMPOSITION | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv | https://arxiv.org/abs/2209.15488; https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | 1.000000000000 | True | False | False | False | False | False |

## Alloy Proxy Vector

| proxy_id | material_id | left_minus_right | mass_fraction_sum | Z_over_A_proxy | N_over_A_proxy | neutron_excess_proxy | electron_rest_mass_fraction | coulomb_formula_proxy | A_bar_proxy | basis_convention | source_anchor | usable_level | missing_for_claim | source_backed_composition_context | binding_decomposed | projection_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AP1909_PtRh10 | PtRh10 | not_applicable | 1.000000000000 | 4.035472576671e-01 | 5.964527423329e-01 | 1.929054846659e-01 | 2.213928246174e-04 | 5.187582949e+00 | 1.858800000000e+02 | MICROSCOPE alloy mass-fraction proxy from 983 plus electron candidate 1330 | P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv; P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv | ALLOY_PROXY_CONTEXT_ONLY | binding-energy split, parent MTS response basis, source-worldtube/readout kernels, tau normalization | True | False | False | False |
| AP1909_TA6V | TA6V | not_applicable | 1.000000000000 | 4.603247141798e-01 | 5.396752858202e-01 | 7.935057164042e-02 | 2.526839874916e-04 | 2.613068278e+00 | 4.676600000000e+01 | MICROSCOPE alloy mass-fraction proxy from 983 plus electron candidate 1330 | P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv; P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv | ALLOY_PROXY_CONTEXT_ONLY | binding-energy split, parent MTS response basis, source-worldtube/readout kernels, tau normalization | True | False | False | False |
| AP1909_TA6V_minus_PtRh10 | TA6V_minus_PtRh10 | TA6V_minus_PtRh10 | not_applicable | 5.677745651272e-02 | -5.677745651272e-02 | -1.135549130254e-01 | 3.129116287420e-05 | -2.574514671000e+00 | -1.391140000000e+02 | same sign as MCON1061_0_test_pair and 1481 context pack | P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair; P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv:MAT1424_2_electron_mass_fraction | DIFFERENTIAL_ALLOY_PROXY_CONTEXT_ONLY | full material tensor, MTS parent coefficient owner, no-double-counting rule, source/readout/tau normalization | True | False | False | False |

## Binding Projection Blocker Ledger

| blocker_id | needed_object | current_input | why_it_blocks | minimum_acceptance | candidate_source | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BB1909_0_flight_material_isotopes | flight-material isotope fractions for PtRh10 and TA6V | natural Ti/Pt isotope rows plus alloy elemental mass fractions | flight material may not equal natural elemental isotope mix; Al, V, Rh isotope rows were not expanded in 1909 | source-backed isotope table for Pt, Rh, Ti, Al, V or official statement permitting natural abundance proxy | https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl; https://arxiv.org/abs/2209.15488 | MISSING_FULL_FLIGHT_ISOTOPE_MIX | False |
| BB1909_1_atomic_nuclear_mass_convention | atomic-to-nuclear mass and electron subtraction convention | electron rest-mass fraction proxy from 1330 | atomic masses include electrons and chemical/nuclear conventions; WEP response tensor needs one no-double-counting mass functional | parent-signed mass functional or source-backed convention splitting electron, proton, neutron, binding, and residual mass | P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_CANDIDATE_NONCLAIM.csv; PDG/CODATA/AME source pack | MISSING_MASS_FUNCTIONAL_NO_DOUBLE_COUNT_RULE | False |
| BB1909_2_EM_Coulomb_binding_owner | EM/Coulomb binding response under MTS parent generator | DD-style smoke components and rough coulomb_formula_proxy | external Damour-Donoghue or liquid-drop proxies cannot be imported as MTS parent coefficients without an operator owner | MTS parent EM owner, sign convention, derivative map, and bounded mismatch to any external proxy | P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv; C_parent_WEP_EM_edge_signing_decision_1466.csv | MISSING_PARENT_EM_BINDING_OPERATOR_OWNER | False |
| BB1909_3_nuclear_binding_decomposition | nuclear volume/surface/asymmetry/pairing/QCD split | surface/binding smoke contrast only | one scalar surface proxy cannot stand in for a source-basis tensor unless the parent basis selects it | exact mass-defect tensor or parent theorem reducing nuclear binding to retained components | AME2020/nuclear-mass source pack; P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv | MISSING_NUCLEAR_BINDING_TENSOR | False |
| BB1909_4_lattice_impurity_and_shape | alloy lattice/chemical binding, impurities, coatings, and test-body geometry convention | bulk mass-fraction alloy labels only | flight test bodies are not abstract elemental mixtures; local source response may depend on material processing/coatings if parent coupling sees those sectors | official material spec or parent theorem proving these sectors are common-mode/negligible | https://arxiv.org/abs/2209.15488; https://doi.org/10.1088/1361-6382/ac84be | MISSING_FLIGHT_MATERIAL_SYSTEMATICS_OR_ZERO_THEOREM | False |
| BB1909_5_source_readout_kernel | source-worldtube/readout/tau kernel | official portal targets and surrogate guard from 1900 | a material vector is not an eta prediction until it is contracted with source, readout, and normalization kernels | official CMSM arrays or parent-signed point-source/common-mode theorem plus tau/product convention | P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | MISSING_SOURCE_READOUT_TAU_KERNEL | False |

## Projection Status

| row_id | object | current_status | gain | remaining_blocker | source_anchor | projection_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MP1909_0_alloy_composition | PtRh10 and TA6V alloy mass-fraction composition | SOURCE_BACKED_COMPOSITION_CONTEXT_FILLED | moves beyond 1908 natural Ti/Pt element-only stub | not a binding/material response tensor | P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv | False | False |
| MP1909_1_differential_proxy | TA6V_minus_PtRh10 differential alloy proxy vector | NUMERIC_PROXY_CONTEXT_FILLED_NONCLAIM | Z/A, N/A, neutron-excess, electron-rest-mass, Coulomb-proxy and Abar contrasts are now in one sign convention | parent basis/no-double-count/readout/source/tau missing | P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_PROXY_VECTOR_NONCLAIM.csv:AP1909_TA6V_minus_PtRh10 | False | False |
| MP1909_2_binding_projection | material binding projection row | BINDING_PROJECTION_BLOCKED_EXPLICITLY | blockers are now separated by isotope, mass convention, EM owner, nuclear tensor, flight material, and readout kernel | BB1909_0 through BB1909_5 | P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv | False | False |
| MP1909_3_verdict | 1909 Ti/Pt material projection | ALLOY_PROXY_GAINED_MATERIAL_BINDING_PROJECTION_STILL_BLOCKED | source-backed alloy proxy scaffold is usable for smoke/debug only | full parent material tensor and source/readout product | MP1909_0_alloy_composition; MP1909_1_differential_proxy; MP1909_2_binding_projection | False | False |

## Claim Gate

| gate_id | condition | current_status | source_anchor | gate_pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1909_0_alloy | alloy mass fractions are source-backed and sum to unity | PASS_CONTEXT_ONLY | P8_Y5_PARENT_QLOC_1909_TIPT_ALLOY_COMPOSITION_SOURCE_BACKED_NONCLAIM.csv | False | False |
| CG1909_1_binding | material binding tensor is source-backed or parent-derived | FAIL_BINDING_PROJECTION_BLOCKED_EXPLICITLY | P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv | False | False |
| CG1909_2_readout | material tensor is contracted with source-worldtube/readout/tau kernels | FAIL_SOURCE_READOUT_TAU_KERNEL_MISSING | P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv | False | False |
| CG1909_3_claim | 1909 supports WEP/local-GR claim-grade projection | CLAIM_BLOCKED | CG1909_0_alloy through CG1909_2_readout | False | False |

## Decision Ledger

| decision_id | decision | reason | status | next_dependency | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC1909_0_keep | keep alloy proxy scaffold | it is a real improvement over natural Ti/Pt stubs and fixes the sign convention around TA6V_minus_PtRh10 | ALLOY_PROXY_CONTEXT_GAINED_NONCLAIM | binding/material tensor owner | False |
| DEC1909_1_block | do not promote binding projection | binding decomposition, parent basis, no-double-counting, and readout/source kernels are still absent | MATERIAL_BINDING_PROJECTION_BLOCKED | derive parent material response functional or source exact mass-defect tensor | False |
| DEC1909_2_next | attack parent material response functional before more data polishing | more alloy proxies will not become physics until a parent-owned tensor says what the retained components mean | NEXT_TARGET_SELECTED | 1910 parent material response functional or exact mass-defect tensor contract | False |

## Next Target

| branch_id | route_id | selection_status | target_doc | target_script | objective | success_condition | do_not | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | NEXT1909_0_primary | selected | 1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md | scripts/Y5_R2FR_parent_material_response_functional_or_exact_mass_defect_tensor_contract_1910.py | derive the parent material response functional that maps constituent/binding data into Delta_w, or write the exact source contract for an external mass-defect tensor | parent-owned no-double-count response basis, or precise external tensor acquisition contract that cannot be mistaken for a claim | do not promote alloy proxies, DD smoke components, or natural isotope rows as MTS WEP predictions | False | False |

## Project Status Snapshot

| status_id | area | summary | risk_level | project_meaning | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| STAT1909_0_gain | material data | 1909 now carries source-backed PtRh10/TA6V alloy composition and a unified differential proxy vector | REAL_PROGRESS_NONCLAIM | the WEP branch has moved from element stubs to actual alloy context | derive parent material response functional | False |
| STAT1909_1_block | binding projection | the real missing piece is not more Z/A arithmetic; it is the parent-owned material/binding response tensor | CENTRAL_THEORY_GAP_EXPOSED | this is exactly the coupling/material-response hole the local branch has been circling | prove or contract the response functional | False |
| STAT1909_2_claim | WEP/local-GR | claim remains blocked; the new rows are smoke/debug scaffolds only | SAFE_NONCLAIM | we gained usable structure without weakening the standards | 1910 response functional route | False |

## Validation

| validation_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL1909_00_sources | PASS | all local source paths exist and needles found | False |
| VAL1909_01_alloy_rows | PASS | alloy rows numeric and mass fractions sum to unity | False |
| VAL1909_02_proxy_rows | PASS | proxy rows finite and include TA6V_minus_PtRh10 contrast | False |
| VAL1909_03_blocker_ledger | PASS | binding/source/readout blockers remain explicit | False |
| VAL1909_04_projection_status | PASS | projection remains blocked after alloy proxy gain | False |
| VAL1909_05_claim_gate | PASS | claim remains blocked | False |
| VAL1909_06_next_target | PASS | 1910 parent response functional route selected | False |
| VAL1909_07_claim_flags_safe | PASS | all claim/projection/binding/readout flags remain false | False |
| VAL1909_08_csv_parse | PASS | parsed 10 csv files | False |
| VAL1909_09_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\TIPT_ALLOY_PROXY_VECTOR_1909_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_1909_TIPT_MATERIAL_BINDING_PROJECTION_STATUS_NONCLAIM.csv; D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR1909_TIPT_MATERIAL_BINDING_BLOCKERS_NONCLAIM.csv | False |
| VAL1909_10_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False |
| VAL1909_11_formalization_untouched | PASS | formalization_1909_artifact_count=0 | False |
| VAL1909_OVERALL | PASS | 1909 Ti/Pt alloy material-binding projection or blocker ledger | False |
