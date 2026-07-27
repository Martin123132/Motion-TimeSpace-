# 2786 - Finite WEP source-vector and material-tensor acquisition pack under AX1090

## Private Verdict

2786 makes the WEP route more usable without pretending it is solved. The source anchors are now staged: MICROSCOPE composition/readout references, Earth composition reference, R2FR toy material deltas, external DD smoke deltas, C_parent contract, same-basis gates, and runner refusal. The bottleneck is still the coupling/basis owner: without a parent response basis and C_parent, the material/source rows are bookkeeping, not a derived MTS WEP prediction.

## Source Register
| row_id | source_key | exists | needle_found | source_role |
| --- | --- | --- | --- | --- |
| SRC2786_00_2785_next | 2785_next | True | True | current handoff into finite WEP acquisition pack |
| SRC2786_01_2785_validation | 2785_validation | True | True | 2785 validation baseline |
| SRC2786_02_2785_narrow | 2785_narrow | True | True | narrow current-owner partial verdict |
| SRC2786_03_2785_contract | 2785_contract | True | True | finite WEP source-vector contract |
| SRC2786_04_2785_material_contract | 2785_material_contract | True | True | material tensor contract |
| SRC2786_05_1080_web | 1080_web | True | True | R10 web/source candidate register |
| SRC2786_06_1080_earth | 1080_earth | True | True | R10 Earth/source vector acquisition status |
| SRC2786_07_1080_material | 1080_material | True | True | R10 material tensor acquisition status |
| SRC2786_08_1080_cparent | 1080_cparent | True | True | R10 C_parent contract |
| SRC2786_09_1080_readout | 1080_readout | True | True | R10 MICROSCOPE readout gate |
| SRC2786_10_1081_basis | 1081_basis | True | True | R10 parent-basis derivation obstruction |
| SRC2786_11_1081_dd_delta | 1081_dd_delta | True | True | external DD smoke material deltas |
| SRC2786_12_2781_tau_shape | 2781_tau_shape | True | True | R2FR surrogate tau shape status |
| SRC2786_13_2780_cmsm | 2780_cmsm | True | True | R2FR official CMSM export check |
| SRC2786_14_local_bounds | local_bounds | True | True | MICROSCOPE WEP bound row |

## Web/Source Candidate Register
| web_source_id | role | source_url | extraction_status |
| --- | --- | --- | --- |
| WEB2786_0_MICROSCOPE_SF2A_2023 | MICROSCOPE test-mass composition and measurement model | https://inspirehep.net/files/9a51796b3d7d940b16bd170876e35e4e | SOURCE_IDENTIFIED_AND_SUMMARIZED_FROM_1080 |
| WEB2786_1_DAMOUR_DONOGHUE_2010 | external phenomenological material-charge basis | https://arxiv.org/abs/1007.2792 | SOURCE_IDENTIFIED_FOR_PHENOMENOLOGICAL_BASIS_ONLY |
| WEB2786_2_MCDONOUGH_SUN_1995 | Earth/source composition reference candidate | https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/ | REFERENCE_IDENTIFIED_NOT_VECTORIZED |
| WEB2786_3_MICROSCOPE_RESULTS_2023 | official analysis/readout/data-portal context | https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf | SOURCE_IDENTIFIED_ARRAYS_NOT_IMPORTED |

## Earth Source Vector Candidates
| source_vector_id | object | basis | status | missing_for_claim |
| --- | --- | --- | --- | --- |
| EARTH2786_0_source_role | R_source^Earth | observed MICROSCOPE source leg | SOURCE_ROLE_IDENTIFIED | composition/profile vector in the same parent basis as R_material and C_parent |
| EARTH2786_1_bulk_composition_reference | R_source^Earth | bulk Earth composition reference candidate | REFERENCE_IDENTIFIED_NOT_VECTORIZED | extract elemental/geophysical composition table and map to parent/source basis |
| EARTH2786_2_parent_basis_block | R_source^Earth | MISSING_MTS_PARENT_BASIS | MISSING_FOR_CLAIM | MTS must choose/derive the basis before Earth composition becomes a source vector |
| EARTH2786_3_common_mode_alternative | R_source^Earth common-mode theorem | THEOREM_ROUTE | THEOREM_ROUTE_NOT_SIGNED | parent theorem that source response is universal/common-mode without measured-G absorption |
| EARTH2786_4_acquisition_task | R_source^Earth acquisition task | PENDING_PARENT_OR_DD_BASIS | ACTIONABLE_BUT_NONCLAIM | same-basis map into C_parent and DeltaR_material |

## Material Composition And Tensor Candidates
| material_id | object | mapped_basis | numeric_components | status | missing_for_claim |
| --- | --- | --- | --- | --- | --- |
| MAT2786_0_PtRh10_MICROSCOPE | PtRh10 | MICROSCOPE_COMPOSITION_CONTEXT_ONLY | composition_context_numeric | SOURCE_BACKED_COMPOSITION_CONTEXT | parent response basis and full material tensor |
| MAT2786_1_TA6V_MICROSCOPE | TA6V | MICROSCOPE_COMPOSITION_CONTEXT_ONLY | composition_context_numeric | SOURCE_BACKED_COMPOSITION_CONTEXT | parent response basis and full material tensor |
| MAT2786_2_R2FR_toy_delta | R_TA6V_minus_PtRh10 toy components | TOY_Z_OVER_A_NEUTRON_EXCESS_NOT_PARENT | Delta_q_Z_over_A_toy=0.05573878418681388;Delta_q_neutron_excess_toy=-0.11147756837362778 | TOY_NUMERIC_NOT_CLAIM_BASIS | parent response basis; uncertainty; source vector; coefficient owner |
| MAT2786_3_delta_alpha_smoke | R_TA6V_minus_PtRh10 alpha/Coulomb smoke component | DD_ALPHA_COULOMB_EXTERNAL_PHENOMENOLOGICAL | Delta_Q_alpha_Coulomb=-1.989808886825e-03;abs=0.001989808886825 | SMOKE_NUMERIC_NOT_FULL_TENSOR | MTS parent basis; source vector; tau/readout; coefficient owner |
| MAT2786_4_delta_surface_smoke | R_TA6V_minus_PtRh10 surface/binding smoke component | DD_SURFACE_BINDING_EXTERNAL_PHENOMENOLOGICAL | Delta_Q_surface_binding=-3.306456347405e-03;abs=0.003306456347405 | SMOKE_NUMERIC_NOT_FULL_TENSOR | MTS parent basis; source vector; tau/readout; coefficient owner |
| MAT2786_5_full_tensor_upgrade | R_TA6V_minus_PtRh10 full material tensor | MISSING_MTS_PARENT_BASIS | MISSING_FULL_MATERIAL_TENSOR | MISSING_FOR_CLAIM | parent basis and full response map |

## C_parent Coefficient Contract
| coefficient_id | object | candidate_basis | value | status | missing_for_claim |
| --- | --- | --- | --- | --- | --- |
| CP2786_0_definition | C_parent | MISSING_MTS_PARENT_BASIS | MISSING_PARENT_COEFFICIENT | MISSING_FOR_CLAIM | derive from parent action or explicitly source as finite phenomenological coefficient |
| CP2786_1_current_owner_partial | C_parent | current-owner subtheorem | NO_NUMERIC_COEFFICIENT_SUPPLIED | PARTIAL_THEOREM_NOT_COEFFICIENT | pre-variation action/species weights or finite coefficient still unresolved |
| CP2786_2_DD_basis_external | C_parent in Damour-Donoghue basis | DD_ALPHA_SURFACE_EXTERNAL | MISSING_DD_COEFFICIENT_VECTOR | PHENOMENOLOGICAL_BASIS_AVAILABLE_NONCLAIM | MTS-to-DD basis map and coefficient derivation |
| CP2786_3_finite_source_option | C_parent finite sourced-input route | PENDING_PARENT_OR_EXTERNAL_BASIS | MISSING_SOURCED_FINITE_COEFFICIENT | ACQUISITION_CONTRACT_ONLY | source path, prior, units, sign convention, and non-fundamental label |

## MICROSCOPE Readout Gate
| readout_id | object | status | missing_for_claim |
| --- | --- | --- | --- |
| READ2786_0_measurement_equation | K_MICROSCOPE readout model | MODEL_STRUCTURE_SOURCE_BACKED | official arrays/masks or validated reconstruction in the same product convention |
| READ2786_1_CMSM_portal | official CMSM data portal | OFFICIAL_PORTAL_IDENTIFIED_ARRAYS_NOT_IMPORTED | download/import gx,gz,Sxx,Sxz/masks or user-assisted official export |
| READ2786_2_surrogate_matrix | surrogate K_MICROSCOPE | SURROGATE_AVAILABLE_NONCLAIM | official arrays and parent material/source map |
| READ2786_3_physical_tau | physical tau_WEP | NOT_ACQUIRED | official arrays plus C_parent/R_source/R_material product basis |

## Same-Basis Closure Gate
| basis_gate_id | object | current_status | blocking_input | claim_allowed |
| --- | --- | --- | --- | --- |
| BASIS2786_0_same_basis_formula | same-basis finite WEP product | NOT_CLOSED | MISSING_MTS_PARENT_BASIS | False |
| BASIS2786_1_external_DD_basis | Damour-Donoghue alpha/surface basis | EXTERNAL_SMOKE_ONLY | PARENT_TO_DD_MAP_MISSING | False |
| BASIS2786_2_source_common_mode | source common-mode theorem | THEOREM_NOT_SIGNED | SOURCE_VECTOR_OR_COMMON_MODE_PROOF_MISSING | False |
| BASIS2786_3_readout_projection | MICROSCOPE arena projection | SURROGATE_ONLY | OFFICIAL_ARRAYS_OR_VALIDATED_RECONSTRUCTION_MISSING | False |

## Acquisition Priority Ledger
| acquisition_id | task | required_artifact | priority | status |
| --- | --- | --- | --- | --- |
| ACQ2786_0_parent_basis | derive or select finite WEP basis | MTS parent action slots -> response basis I | FIRST | PENDING_SOURCE_OR_DERIVATION |
| ACQ2786_1_C_parent | derive/source coefficient vector | C_parent^I with units, sign convention, source path | SECOND | PENDING_SOURCE_OR_DERIVATION |
| ACQ2786_2_R_source | vectorize Earth/source | R_source_I^Earth from source composition/worldtube or theorem common-mode proof | THIRD | PENDING_SOURCE_OR_DERIVATION |
| ACQ2786_3_DeltaR_material | build full material tensor | R_TA6V_I - R_PtRh10_I with uncertainty and composition provenance | THIRD | PENDING_SOURCE_OR_DERIVATION |
| ACQ2786_4_K_readout | import/validate MICROSCOPE readout | gx,gz,Sxx,Sxz,masks and tau_WEP projection | FOURTH | PENDING_SOURCE_OR_DERIVATION |
| ACQ2786_5_runner | run finite WEP product comparator | numeric same-basis product against eta bound | LAST | PENDING_SOURCE_OR_DERIVATION |

## Finite WEP Input Pack
| input_id | object | candidate_value | status | blocks_claim |
| --- | --- | --- | --- | --- |
| FIP2786_0_product_formula | P_WEP finite product | P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE | FORMULA_READY_NONCLAIM | all numeric input rows still required |
| FIP2786_1_C_parent | C_parent | MISSING_PARENT_COEFFICIENT | MISSING_FOR_CLAIM | no MTS coupling magnitude or basis owner |
| FIP2786_2_R_source | R_source^Earth | REFERENCE_IDENTIFIED_NOT_VECTORIZED | MISSING_FOR_CLAIM | no same-basis Earth source vector |
| FIP2786_3_R_material | R_TA6V - R_PtRh10 | R2FR toy vector and DD smoke deltas available; full tensor missing | PARTIAL_SMOKE_NUMERIC_NONCLAIM | external smoke/toy basis not parent MTS basis; full tensor missing |
| FIP2786_4_K_readout | K_MICROSCOPE | surrogate available; official portal identified; arrays not imported | SURROGATE_ONLY_NONCLAIM | official arrays or validated reconstruction required |
| FIP2786_5_tau_WEP | tau_WEP | MISSING_PHYSICAL_TAU | MISSING_FOR_CLAIM | tau cannot be set to one or absorbed into measured G |

## Product Stub And Bound
| prediction_id | product_symbol | product_value | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| PRED2786_0_WEP_finite_input_pack_nonclaim | P_WEP_relative_source_weight | MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_READOUT_TAU_NUMERIC_PRODUCT | ACQUISITION_PACK_READY_PRODUCT_MISSING | False |

| bound_id | observable | upper_bound | units | valid_bound_row |
| --- | --- | --- | --- | --- |
| BOUND2786_0_MICROSCOPE_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | True |

| runner_id | valid_prediction_rows | valid_bound_rows | claim_allowed | expected_result |
| --- | --- | --- | --- | --- |
| APR2786_0_WEP_finite_input_pack_product_stub | 0 | 1 | False | reject acquisition-pack rows until same-basis numeric product exists |

## Claim Gates
| gate_id | gate | supporting_context_present | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2786_0_sources | source candidates identified | True | False | paper/source roles are staged but not transformed into final vectors |
| CG2786_1_parent_basis | MTS parent finite WEP basis | False | False | basis not derived |
| CG2786_2_C_parent | C_parent coefficient vector | False | False | coefficient missing |
| CG2786_3_R_source | R_source^Earth vector | False | False | Earth composition/reference not vectorized in parent basis |
| CG2786_4_R_material | R_TA6V - R_PtRh10 full material tensor | False | False | only composition context, toy vector, and external smoke deltas exist |
| CG2786_5_K_readout_tau | K_MICROSCOPE and tau_WEP | False | False | surrogate readout only; physical tau not acquired |
| CG2786_6_product_runner | finite WEP product runner | False | False | valid_prediction_rows=0 |

## Decision Ledger
| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC2786_0_pack_value | finite WEP acquisition pack is now source-anchored but not score-ready | MICROSCOPE material/readout references, DD material charge basis, Earth composition reference, and R2FR surrogate status are named | do not claim; instantiate a basis only as a nonclaim smoke runner |
| DEC2786_1_key_gap | the coupling/basis gap is now the bottleneck | C_parent and the MTS parent response basis determine whether material/source rows are physics or just bookkeeping | try parent-basis derivation before treating DD rows as anything more than a comparator |
| DEC2786_2_next_route | build a parent-basis derivation or DD smoke runner as the next practical scaffold | the pack can test pipeline algebra once a basis policy is explicit | 2787 should derive MTS parent WEP basis first; if unsigned, instantiate DD alpha/surface smoke runner with strict nonclaim gates |

## Validation
| validation_id | passed | detail |
| --- | --- | --- |
| VAL2786_0_sources | True | every cited source path exists and source needle was found |
| VAL2786_1_web_sources_identified | True | web/source candidates are recorded with URLs |
| VAL2786_2_earth_source_blocked | True | Earth/source vector reference exists but same-basis vector is missing |
| VAL2786_3_material_context | True | MICROSCOPE material compositions are recorded |
| VAL2786_4_material_full_tensor_missing | True | full parent material tensor remains missing |
| VAL2786_5_c_parent_missing | True | C_parent coefficient remains missing |
| VAL2786_6_readout_tau_missing | True | physical tau_WEP remains missing |
| VAL2786_7_same_basis_gate_blocks | True | same-basis closure gates block claims |
| VAL2786_8_acquisition_priority_written | True | acquisition priority ledger is written |
| VAL2786_9_input_pack_nonclaim | True | finite WEP input pack remains nonclaim and missing claim inputs |
| VAL2786_10_prediction_nonclaim_missing | True | prediction row remains missing same-basis finite inputs |
| VAL2786_11_bound_numeric | True | bound import is positive numeric |
| VAL2786_12_runner_refuses | True | runner reports no valid prediction rows and claim false |
| VAL2786_13_claim_gates_safe | True | all claim gates deny WEP/local-GR claim |
| VAL2786_14_next_target | True | 2787 handoff written |
| VAL2786_15_branch_outputs | True | branch copies exist and contain rows |
| VAL2786_16_csv_parse | True | all generated CSV outputs parse cleanly |
| VAL2786_17_no_claim_flags | True | no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true |
| VAL2786_18_generated_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work |
| VAL2786_19_formalization_untouched | True | formalization-workbench modified-file count remains zero during this run |
| VAL2786_20_pycache_absent | True | scripts __pycache__ absent at validation write |
| VAL2786_OVERALL | True | 2786 turns the finite WEP route into a source-anchored acquisition pack. MICROSCOPE composition/readout sources, Earth-source reference, R2FR toy and DD smoke material rows, C_parent contract, same-basis gates, and runner refusal are staged; no WEP/local-GR claim is allowed until a same-basis numeric product exists. |

## Next Target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2786_0_2787 | 2787-Y5-R2FR-parent-WEP-basis-derivation-or-DD-finite-WEP-smoke-runner-under-AX1090.md | try to derive the MTS parent WEP response basis and coefficient map; if it remains unsigned, instantiate a Damour-Donoghue alpha/surface finite-WEP smoke runner with explicit source/readout policy and strict nonclaim gates | parent response basis; C_parent units; MTS-to-DD map; Earth source policy; TA6V/PtRh10 smoke deltas; MICROSCOPE readout gate; product runner refusal | DD smoke as MTS claim; unit source/readout as tau_WEP; measured-G absorption; tau=1; public claim; GitHub; formalization edits |
