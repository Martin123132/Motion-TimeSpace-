# 3489: Connected Matter Category Certificate Or `J_spurion` Bound Source

## Current Verdict
- **Template result:** the ordinary-matter physical interaction graph is connected.
- **Claim guard:** template connectedness is not parent-owned connectedness; 1464/1452/1461 still block theorem-zero.
- **Concrete progress:** `epsilon_J_spurion` is upgraded from missing-only to product-bounded-not-isolated via WEP source-product rows.
- **No claim:** no local-GR/source-coupling pass is claimed.

## Graph Components
| component_id | node_count | nodes | template_connected_component | parent_owned_connected_component | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| COMP3489_0 | 10 | atom;bulk_matter;down_quark;electron;gluon;neutron;nucleus;photon;proton;up_quark | True | False | TEMPLATE_CONNECTED_PARENT_GRAPH_UNSIGNED | False |

## Certificates
| certificate_id | statement | evidence | passed | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CERT3489_0_template_graph_connected | The physical ordinary-matter template graph is connected. | component_count=1 | True | supports the connected-category premise shape only | False |
| CERT3489_1_parent_graph_owner | The connected graph is supplied as a parent-owned matter category. | 1464 status says physical template is guidance, not parent proof | False | blocks theorem-zero for epsilon_J_spurion | False |
| CERT3489_2_species_blind_measure | The parent action supplies one species-blind measure/current normalization. | 1452 common measure/current theorem remains unsigned | False | blocks theorem-zero for epsilon_species_measure | False |
| CERT3489_3_source_label_forgetting | Source/readout functor forgets labels before source normalization. | 1461 says label-forgetting/no-relative-slot clause is not reduced | False | blocks theorem-zero for epsilon_source_reentry | False |

## J Spurion Product Bounds
| product_bound_id | arena | observable_row | product_symbol | bound_value | bound_units | isolates_epsilon | missing_for_isolation | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JSPB3489_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | MICROSCOPE_TIPT_EARTH_FIELD | MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10 | abs(S_E^q) * abs(Delta_epsilon_Jspurion_AB) | 2.755102040816e-15 | dimensionless_eta | False | parent-owned lower bound on abs(S_E^q) or theorem-zero for source amplitude | False |
| JSPB3489_1_MATRIX3473_1_EOTWASH_Be_minus_Ti | EOTWASH_BETI_EARTH_FIELD | MATRIX3473_1_EOTWASH_Be_minus_Ti | abs(S_E^q) * abs(Delta_epsilon_Jspurion_AB) | 3.828000000000e-13 | dimensionless_eta | False | parent-owned lower bound on abs(S_E^q) or theorem-zero for source amplitude | False |

## Finite Coefficient Updates
| coefficient_id | symbol | old_status | new_status | bound_source | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| JSP3488_0_J_spurion_envelope | epsilon_J_spurion | MISSING_THEOREM_ZERO_OR_SOURCE_BOUND | PRODUCT_BOUNDED_NOT_ISOLATED | JSPB3489_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10;JSPB3489_1_MATRIX3473_1_EOTWASH_Be_minus_Ti | epsilon_J_spurion is not numeric, but its source product is now tied to WEP eta bounds. | False |
| JSP3488_1_species_measure_envelope | epsilon_species_measure | MISSING_THEOREM_ZERO_OR_SOURCE_BOUND | STILL_MISSING_THEOREM_ZERO_OR_SOURCE_BOUND |  | not bounded by the current WEP source-product interface in this checkpoint | False |
| JSP3488_2_source_reentry_envelope | epsilon_source_reentry | MISSING_THEOREM_ZERO_OR_SOURCE_BOUND | STILL_MISSING_THEOREM_ZERO_OR_SOURCE_BOUND |  | not bounded by the current WEP source-product interface in this checkpoint | False |

## Theorems
| theorem_id | statement | proof | result | valid_for_claim |
| --- | --- | --- | --- | --- |
| THM3489_0_template_connectedness | The ordinary-matter physical template graph containing quarks, gluons, photons, electrons, nuclei, atoms, and bulk matter is connected. | The edge list links all nodes through EM, QCD, bound-state, atomic, and composition morphism templates; the graph traversal returns one component. | connectedness premise is structurally plausible but parent-owner unsigned | False |
| THM3489_1_parent_certificate_failure | Template connectedness does not sign the parent matter category. | 1464 explicitly labels the interaction web as physical guidance and retains graph-owner/source-label-forgetting/calibration blockers. | epsilon_J_spurion theorem-zero is not claimable yet | False |
| THM3489_2_product_bound | Even without isolated epsilon_J_spurion, WEP rows source a finite product bound on abs(S_E^q) times the spurion contrast. | A source/species prefactor residual enters eta as a product with the common Earth source leg; measured eta bounds constrain that product. | J_spurion residual moves from missing-only to PRODUCT_BOUNDED_NOT_ISOLATED | False |

## Gates
| gate_id | requirement | passed | evidence | blocks_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3489_0_template_connected | ordinary matter template graph is connected | True | component scan | False | False |
| GATE3489_1_parent_graph_owned | parent action owns the connected graph | False | 1464 parent-owned graph not constructed | True | False |
| GATE3489_2_species_blind_measure_owned | parent action owns species-blind measure/current normalization | False | 1452 theorem unsigned; Jacobian/current countermodels survive | True | False |
| GATE3489_3_source_label_forgetting_owned | source labels cannot reenter after quotient/readout | False | 1461 label-forgetting/no-relative-slot clause not reduced | True | False |
| GATE3489_4_Jspurion_product_bound | finite source-backed product bound rows exist for J_spurion | True | product_bound_rows=2 | False | False |

## Decisions
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3489_0_connectedness | Template connectedness is established; parent-owned connectedness is not. | The graph is connected, but 1464 says the graph has not been supplied by the parent action. | False | False |
| DEC3489_1_Jspurion_status | Upgrade epsilon_J_spurion from missing-only to product-bounded-not-isolated. | WEP eta rows bound abs(S_E^q)*abs(Delta epsilon_Jspurion), but no source-amplitude lower bound isolates epsilon_Jspurion. | False | False |
| DEC3489_2_best_next_attack | Attack species-blind measure/current ownership next, because it blocks both epsilon_species_measure and parent graph signing. | 1452 has explicit quantum-measure and current-owner routes plus surviving countermodels; this is the next load-bearing residual. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3490-Y5-R2FR-species-blind-measure-current-owner-or-product-bound-upgrade.md | scripts/Y5_R2FR_3490_species_blind_measure_current_owner_or_product_bound_upgrade.py | Try to derive the species-blind parent measure/current owner; if not, upgrade epsilon_species_measure and current-rescaling residuals into finite product-bound rows. | common measure/current theorem signed, or epsilon_species_measure/J_nonH/c_A current residuals get source-backed product bounds | using classical EOM equivalence as source proof; deleting species Jacobian countermodel; isolating epsilon without source amplitude | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3489_0_sources_exist | True | all cited local sources exist | False |
| VAL3489_1_csv_parse | True | source_register:9; graph_nodes:10; graph_edges:14; components:1; certificates:4; product_bounds:2; finite_updates:3; theorems:3; gates:5; decisions:3; next_target:1 | False |
| VAL3489_2_template_graph_connected | True | components=1 | False |
| VAL3489_3_product_bounds_exist | True | product_bounds=2 | False |
| VAL3489_4_parent_claim_blocked | True | parent graph/measure/source-label gates block claim | False |
| VAL3489_5_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3489_6_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3489_SUMMARY | True | PASS | False |

_Generated: 2026-06-29T04:37:44.812105+00:00_
