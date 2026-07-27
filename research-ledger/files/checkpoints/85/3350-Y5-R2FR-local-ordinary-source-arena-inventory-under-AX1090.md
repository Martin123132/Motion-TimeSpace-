# 3350 — Local Ordinary Source-Arena Inventory Under AX1090

Generated: `2026-06-28T03:21:54.149413+00:00`

## Summary
- This checkpoint attacks the decoupled-block blocker left by 3349.
- Result: hidden/decoupled blocks are excluded from the ordinary Ti/Pt material inventory unless explicitly listed, but they are not thereby excluded from the full parent field-equation arena.
- So `R_AB=0` is strengthened for the ordinary material graph, while `epsilon_decoupled_field`, `epsilon_readout_source_shadow`, and `epsilon_boundary_contact` remain explicit nonclaim residual rows.
- This prevents smuggling hidden blocks into a fake material response factor and keeps the local-GR route honest.

## Web Source Register
| web_source_id | title | url | usage | scope | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| WEB3350_0_MICROSCOPE_TiPt | MICROSCOPE Mission final Ti/Pt equivalence-principle result | https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 | anchors the local WEP arena as ordinary Ti/Pt test masses with measured eta_TiPt | ordinary material test-body arena, not a parent MTS source signature | false |
| WEB3350_1_NIST_atomic_compositions | NIST Atomic Weights and Isotopic Compositions | https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl | anchors Ti/Pt as standard ordinary atomic elements | element-level material identity, not exact MICROSCOPE alloy decomposition | false |
| WEB3350_2_PDG_standard_model | Particle Data Group Review: The Standard Model | https://pdg.lbl.gov/2023/reviews/rpp2023-rev-standard-model.pdf | anchors ordinary matter/gauge sectors in the source-arena inventory | ordinary-sector component classification | false |
| WEB3350_3_PDG_QCD | Particle Data Group Review: Quantum Chromodynamics | https://pdg.lbl.gov/2023/reviews/rpp2023-rev-qcd.pdf | anchors nuclear/strong binding as ordinary-sector content | ordinary-sector binding classification, not material-specific binding table | false |

## Local Arena Definition
| arena_id | arena | included_source_domain | excluded_by_definition | not_excluded_by_definition | source_anchor_ids | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ARENA3350_0_MICROSCOPE_TiPt_material | local WEP Ti/Pt ordinary material test-body arena | ordinary atomic/electronic/nuclear/material Hilbert stress of Ti/Pt-like test bodies | nonordinary hidden/dark/decoupled blocks not listed as test-body material constituents | ambient/background parent fields, hidden sectors coupled through the field equation, readout/projector terms | WEB3350_0_MICROSCOPE_TiPt; WEB3350_1_NIST_atomic_compositions | ARENA_SPLIT_DEFINED | false |
| ARENA3350_1_parent_field_equation | local parent field-equation source arena | all variational source terms admitted by S_parent plus explicit residual blocks | nothing beyond the signed parent action object language | decoupled conserved sectors if present in S_parent or local environment | LSRC3350_0_3349_doc; LSRC3350_5_3348_basis | FIELD_EQUATION_ARENA_REMAINS_PARENT_SIGNED_ONLY | false |

## Ordinary Source Inventory
| inventory_id | ordinary_component | arena_status | graph_connection | source_anchor_ids | RAB_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ORD3350_0_electrons | bound electrons / charged leptonic matter | included_in_ordinary_TiPt_material | connected to nuclei through EM/binding stress | WEB3350_2_PDG_standard_model; LSRC3350_1_3349_edges | part of total Hilbert stress; no independent R_AB if graph closes | false |
| ORD3350_1_nuclear_matter | protons/neutrons/quark-gluon nuclear content | included_in_ordinary_TiPt_material | connected through strong/nuclear binding | WEB3350_2_PDG_standard_model; WEB3350_3_PDG_QCD | part of total Hilbert stress; no independent R_AB if graph closes | false |
| ORD3350_2_binding_stresses | EM, nuclear, molecular, and lattice binding stresses | included_in_ordinary_TiPt_material_as_binding_content | edge carriers that make the ordinary material graph connected | LSRC3350_1_3349_edges | must be included in T_H rather than counted as a separate source projector | false |
| ORD3350_3_alloy_material_detail | exact MICROSCOPE Ti/Pt alloy and material processing detail | not_acquired | needed only for material-charge fallback or fine source table | WEB3350_0_MICROSCOPE_TiPt; WEB3350_1_NIST_atomic_compositions | not needed for pure Hilbert zero theorem, but needed for nonzero beta dot Delta chi_TiPt fallback | false |

## Decoupled Block Audit
| block_id | candidate_block | arena_result | reason | remaining_risk | residual_symbol | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DECPL3350_0_material_constituent_hidden_block | hidden/dark/decoupled sector as literal Ti/Pt material constituent | EXCLUDED_FROM_ORDINARY_MATERIAL_INVENTORY | Ti/Pt material arena is defined by ordinary atomic/nuclear constituents and binding stresses; no source anchor lists a hidden-sector constituent | does not exclude a parent hidden field coupled to local gravity outside material composition | none_for_material_inventory; epsilon_decoupled_field remains | false |
| DECPL3350_1_ambient_decoupled_background | ambient/background decoupled conserved source block | NOT_EXCLUDED_FROM_PARENT_FIELD_ARENA | ordinary material composition does not prove the local parent field equation lacks a separately conserved residual block | could enter common source calibration, PPN, WEP, or local field equation as an explicit residual | epsilon_decoupled_field | false |
| DECPL3350_2_readout_projector_shadow | readout/projector-created apparent decoupled source | NOT_EXCLUDED_UNTIL_PARENT_NO_PROJECTOR_SIGNED | 3350 inventories material sources, not the whole readout grammar | source-shadow/readout residual can imitate a material response | epsilon_readout_source_shadow | false |
| DECPL3350_3_boundary_improvement_contact | boundary/improvement/contact source near test bodies | NOT_EXCLUDED_UNTIL_BOUNDARY_CONDITION_SIGNED | binding stresses belong in T_H, but unclassified boundary/contact terms are a separate parent-action issue | finite local contact residual if boundary conditions fail | epsilon_boundary_contact | false |

## Arena Exclusion Theorem
| theorem_id | claim_piece | mathematical_form | result | promotion_limit | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| AEX3350_0_material_exclusion | hidden/decoupled blocks are not ordinary Ti/Pt material constituents | T_material^TiPt = T_e + T_nuc + T_EM_bind + T_nuclear_bind + T_lattice + ... ; T_D not in T_material unless the material inventory explicitly includes it | CONDITIONAL_MATERIAL_ARENA_EXCLUSION | does not exclude T_D from S_parent or from ambient/local field-equation sources | false |
| AEX3350_1_graph_route_update | ordinary material branch of R_AB has no hidden constituent slot | R_AB^ordinary=0 if T_active=T_H and ordinary graph is connected; hidden T_D is not a material-composition correction but a separate residual branch | GRAPH_ROUTE_STRENGTHENED_NOT_PROMOTED | parent no-projector/source-shadow signature and field-equation decoupled-block bound remain open | false |
| AEX3350_2_no_smuggling_rule | do not hide decoupled blocks inside R_AB | R_TiPt=beta dot Delta chi_TiPt only for explicit material/source charges; T_D uses epsilon_decoupled_field or epsilon_boundary_contact rows | CLASSIFICATION_RULE_DERIVED | finite residual rows still need numeric/source-backed couplings or parent zeros | false |

## Explicit Residual Rows
| residual_id | symbol | meaning | arena | bound_form | numeric_status | valid_for_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RES3350_0_epsilon_decoupled_field | epsilon_decoupled_field | separately conserved nonordinary/hidden/background source contribution to the local parent field equation | parent field-equation source arena | \|\|T_D\|\| / \|\|T_H^ordinary\|\| times coupling/projection factor | MISSING_DENSITY_COUPLING_AND_PARENT_OWNERSHIP | false | false |
| RES3350_1_epsilon_readout_source_shadow | epsilon_readout_source_shadow | apparent source block created by post-solution readout/projector operation | readout/source-shadow grammar | projector norm times source-shadow amplitude | MISSING_PARENT_NO_PROJECTOR_SIGNATURE_OR_NUMERIC_PROJECTOR_NORM | false | false |
| RES3350_2_epsilon_boundary_contact | epsilon_boundary_contact | boundary/improvement/contact source term not included in ordinary bulk Hilbert material stress | boundary/contact local source arena | boundary flux/contact term divided by ordinary bulk Hilbert source norm | MISSING_BOUNDARY_CONDITION_OR_CONTACT_BOUND | false | false |

## RAB Zero Route Update
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3350_0_material_arena_split | ordinary Ti/Pt material arena is separated from parent field-equation arena | true | 3350 explicitly distinguishes ordinary material constituents from ambient/parent residual sources | false |
| GATE3350_1_hidden_material_constituent_excluded | hidden/decoupled blocks are excluded from ordinary Ti/Pt material inventory unless explicitly listed | true | ordinary material inventory uses atomic/nuclear/binding components; hidden blocks are moved to residual rows | false |
| GATE3350_2_parent_decoupled_field_excluded | decoupled/hidden blocks are excluded from the local parent field-equation arena | false | material composition does not prove parent field equation has no T_D or boundary/source-shadow residual | false |
| GATE3350_3_RAB_zero_promoted | R_AB=0 no-independent-slot route is promoted | false | ordinary material branch is cleaner, but parent no-projector and decoupled field residuals remain open | false |
| GATE3350_4_local_GR_claim | local GR/Newton source-coupling branch is claim-ready | false | explicit residual rows remain without parent zeros or numeric bounds | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3350_0 | Did 3350 close the decoupled-block blocker? | partly | hidden/decoupled blocks are excluded from ordinary Ti/Pt material composition, but not from the full parent field equation | try to prove parent no-decoupled-field/no-boundary-contact for local ordinary arenas, or source finite residual bounds | false |
| DEC3350_1 | Did 3350 reduce the need for charge fitting? | yes | ordinary material R_AB stays on the Hilbert-zero branch; charge fitting is only for explicit spurion/projector branches, not hidden blocks smuggled into material response | 3351 should attack parent decoupled-field silence before 3349b charge-table fallback | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3351-Y5-R2FR-parent-decoupled-field-silence-or-bound-under-AX1090.md | scripts/Y5_R2FR_3351_parent_decoupled_field_silence_or_bound.py | prove local parent action has no separately conserved decoupled source block in ordinary WEP/PPN arenas, or convert epsilon_decoupled_field into sourced finite residual rows | 3350 moved hidden blocks out of material R_AB, but the parent field-equation arena still needs a zero or bound | false |
| 3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md | scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py | fallback branch for explicit spurion/projector material charges beta dot Delta chi_TiPt | needed only if a nonzero source-projector charge basis is deliberately retained | false |
