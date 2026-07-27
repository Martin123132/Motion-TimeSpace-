# 3349 — Source-Backed Ordinary Matter Graph Certificate Under AX1090

Generated: `2026-06-28T03:17:11.989637+00:00`

## Summary
- This checkpoint attacks the 3348 graph route: source-sign ordinary matter connectivity before falling back to material charge fitting.
- Progress: the electron/EM/nuclear/macroscopic material graph is no longer private-only; it now has external source anchors.
- Verdict: `R_AB=0` is still not promoted, because graph closure needs Ti/Pt arena inventory, binding conventions, decoupled-block exclusion, and the parent no-projector signature.
- This is still useful: the remaining blockers are now separated from the fallback `R_TiPt=beta dot Delta chi_TiPt` charge-table branch.

## Web Source Register
| web_source_id | title | url | source_type | usage | confidence | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WEB3349_0_hilbert_metric_variation | Hilbert stress-energy from metric variation / action source owner | https://arxiv.org/abs/2211.03092 | field_theory_reference | anchors the Hilbert-source convention T_H as an action/metric variation object | source_anchor_not_full_parent_signature | false |
| WEB3349_1_em_stress_exchange | Electromagnetic stress-energy exchange with charged matter / Lorentz-force density | https://arxiv.org/abs/1404.5250 | classical_field_theory_reference | anchors the charged-matter--EM exchange edge used in the ordinary matter graph | source_anchor_not_material_specific | false |
| WEB3349_2_pdg_standard_model | Particle Data Group Review: The Standard Model | https://pdg.lbl.gov/2023/reviews/rpp2023-rev-standard-model.pdf | authoritative_review | anchors the ordinary particle/gauge-interaction setting for charged leptons, quarks, and gauge fields | source_anchor | false |
| WEB3349_3_pdg_qcd | Particle Data Group Review: Quantum Chromodynamics | https://pdg.lbl.gov/2023/reviews/rpp2023-rev-qcd.pdf | authoritative_review | anchors the quark/gluon strong-interaction and nuclear-binding edge family | source_anchor_not_nuclear_model | false |
| WEB3349_4_nist_atomic_weights | NIST Atomic Weights and Isotopic Compositions | https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl | measurement_reference | anchors Ti/Pt ordinary material composition as standard atomic species, not hidden test-body sectors | source_anchor_materials_not_alloy_inventory | false |
| WEB3349_5_ciaaw_elements | CIAAW Standard Atomic Weights | https://ciaaw.org/atomic-weights.htm | measurement_reference | secondary anchor for ordinary element composition in Ti/Pt material inventories | source_anchor_materials_not_alloy_inventory | false |

## Graph Node Basis Source Sign
| node_id | ordinary_component | graph_role | source_anchor_ids | source_signed | promotion_status | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NODE3349_0_charged_leptons | electrons / charged leptonic matter | charged matter node coupled to EM/gauge sector | WEB3349_2_pdg_standard_model; WEB3349_1_em_stress_exchange | true | SOURCE_ANCHORED_NODE | material/alloy inventory and parent source-map ownership still not closed | false |
| NODE3349_1_baryons_quarks | protons/neutrons as baryonic/quark-gluon matter | nuclear matter node coupled through QCD/nuclear binding | WEB3349_2_pdg_standard_model; WEB3349_3_pdg_qcd | true | SOURCE_ANCHORED_NODE | no material-specific nuclear binding decomposition yet | false |
| NODE3349_2_em_binding | EM field and EM binding stress | exchange edge carrier between charged constituents | WEB3349_1_em_stress_exchange | true | SOURCE_ANCHORED_BINDING_NODE | falloff/boundary/improvement convention not parent-signed | false |
| NODE3349_3_nuclear_binding | strong/nuclear binding stress | exchange edge carrier inside nuclei | WEB3349_3_pdg_qcd | true | SOURCE_ANCHORED_BINDING_NODE | nuclear effective model and binding-energy convention not source-table closed | false |
| NODE3349_4_TiPt_materials | Titanium / Platinum test-body ordinary atomic material | MICROSCOPE material arena anchor | WEB3349_4_nist_atomic_weights; WEB3349_5_ciaaw_elements | true | ELEMENT_ANCHORED_NOT_ALLOY_CLOSED | exact MICROSCOPE alloy composition and binding-energy inventory not acquired | false |

## Graph Edge Certificate
| edge_id | edge | exchange_constraint | source_anchor_ids | source_signed | certificate_status | promotion_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EDGE3349_0_electron_EM_nucleus | charged lepton -- EM/binding stress -- nucleus | C_e^nu + C_EM/bind^nu + C_nucleus^nu = 0 for the interacting ordinary subsystem | WEB3349_1_em_stress_exchange; WEB3349_2_pdg_standard_model | true | SOURCE_ANCHORED_STANDARD_EDGE | not yet a material-specific Hilbert-stress decomposition for Ti/Pt alloys | false |
| EDGE3349_1_proton_neutron_nuclear_binding | proton/quark matter -- strong/nuclear binding -- neutron/quark matter | C_p^nu + C_n^nu + C_nuclear_bind^nu = 0 in the effective nuclear subsystem | WEB3349_3_pdg_qcd | true | SOURCE_ANCHORED_STANDARD_EDGE | effective nuclear component convention and binding stress split not closed | false |
| EDGE3349_2_atom_molecule_lattice_inheritance | atoms/molecules/solids inherit a total ordinary Hilbert source from constituent plus binding stresses | T_body = T_rest + T_EM_bind + T_nuclear_bind + T_lattice + ... | WEB3349_1_em_stress_exchange; WEB3349_3_pdg_qcd; WEB3349_4_nist_atomic_weights | true | SOURCE_ANCHORED_MACROSCOPIC_INHERITANCE | lattice/material model and alloy inventory not closed | false |
| EDGE3349_3_decoupled_hidden_block_exclusion | ordinary test body -- no exchange -- hidden/decoupled block | T_D excluded from ordinary Ti/Pt body unless source inventory explicitly includes it | LSRC3349_3_2616_graph_attempt; LSRC3349_4_2616_connectivity | false | ARENA_EXCLUSION_NOT_SOURCE_SIGNED | requires explicit local arena inventory excluding dark/hidden/decoupled source blocks from the tested bodies | false |

## Graph Closure Theorem Status
| closure_id | claim_piece | result | evidence | missing_for_promotion | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CLOSE3349_0_graph_edges | ordinary matter graph has source-backed standard edges | PARTIAL_SOURCE_SIGNED | EM, QCD/strong, Standard Model, and Ti/Pt element anchors are recorded | material-specific alloy inventory, binding-energy convention, and decoupled-block arena exclusion | false |
| CLOSE3349_1_connected_component_weight | connected graph collapses relative source weights to one common measured-G mode | THEOREM_AVAILABLE_IF_GRAPH_AND_PARENT_SIGNED | 3348 theorem and 3345/2616 collapse rows | parent source-map ownership and graph closure both required | false |
| CLOSE3349_2_decoupled_exception | no decoupled block contributes to local ordinary Ti/Pt test bodies | NOT_CLOSED | local corpus has an arena-exclusion contract but not a source-backed local inventory | test-body source inventory excluding hidden/dark/decoupled conserved blocks | false |
| CLOSE3349_3_RAB_zero_route | R_AB=0 no-independent-slot route | NOT_PROMOTED | source anchors strengthen the graph route but do not close every promotion clause | CLOSE3349_1 plus CLOSE3349_2 plus parent source-map no-projector signature | false |

## RAB Zero Promotion Gate
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3349_0_source_anchors_recorded | ordinary matter graph has external source anchors | true | web source register includes Hilbert/EM/SM/QCD/NIST/CIAAW anchors and graph rows link to them | false |
| GATE3349_1_graph_closed_for_TiPt | Ti/Pt ordinary matter graph is fully closed | false | exact alloy/material inventory and binding-energy decomposition remain absent | false |
| GATE3349_2_decoupled_arena_excluded | decoupled nonordinary source blocks are excluded from the local WEP arena | false | arena exclusion is a contract but not source-signed for the tested bodies | false |
| GATE3349_3_RAB_zero_promoted | R_AB=0 is promoted for current MTS local ordinary matter | false | source anchors are not enough without graph closure, decoupled exclusion, and parent no-projector signature | false |
| GATE3349_4_local_GR_claim | local GR/Newton source-coupling branch is claim-ready | false | R_AB zero route improved but not promoted; finite material-charge fallback remains open | false |

## Fallback Material Table Trigger
| fallback_id | trigger | fallback_action | relationship_to_RAB | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FB3349_0_material_table_needed_if_graph_not_closed | GATE3349_1_graph_closed_for_TiPt=false or GATE3349_2_decoupled_arena_excluded=false | build Ti/Pt material charge table with electron/proton/neutron, EM binding, nuclear binding, alloy composition, and beta-normalization rows | R_TiPt=beta dot Delta chi_TiPt on the explicit spurion branch | nonclaim_until_source_backed_and_parent_owned | false |
| FB3349_1_graph_route_still_preferred | ordinary graph evidence improves but does not close | first try arena inventory/exclusion before fitting material charges | if graph closes, no independent ordinary R_AB slot remains | preferred_derivation_route | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3349_0 | Did 3349 source-sign the ordinary matter graph enough to promote R_AB=0? | not yet | standard EM/QCD/SM/material anchors are now recorded, but Ti/Pt alloy inventory, binding split, decoupled arena exclusion, and parent no-projector signature remain open | close the local arena inventory/exclusion before falling back to charge fitting | false |
| DEC3349_1 | Did 3349 move the work forward? | yes | the graph route is now source-anchored rather than private-only, and its exact promotion blockers are separated from the finite material-table fallback | 3350 should build a local ordinary source-arena inventory for MICROSCOPE-like bodies | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3350-Y5-R2FR-local-ordinary-source-arena-inventory-under-AX1090.md | scripts/Y5_R2FR_3350_local_ordinary_source_arena_inventory.py | build the local source-arena inventory that either excludes decoupled/hidden blocks from ordinary Ti/Pt-like test bodies or forces them into explicit finite residual rows | this is the remaining graph-route blocker before falling back to arbitrary material-charge response fitting | false |
| 3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md | scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py | fallback branch: acquire Ti/Pt composition and build nonclaim Delta chi rows for beta dot Delta chi_TiPt | needed if 3350 cannot close the no-independent-slot graph route | false |
