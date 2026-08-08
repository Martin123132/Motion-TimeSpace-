# 3356 — Local Collar Contact-Support Exclusion Under AX1090

Generated: `2026-06-28T03:55:39.253346+00:00`

## Summary
- This checkpoint proves the useful part of the contact route: contact/interface terms vanish for pointwise local bulk equations away from their support.
- The proof is not a handwave: choose a compact collar/ball around a bulk point disjoint from the closed contact support; distributional contact terms then evaluate to zero on all local test variations.
- It does **not** close whole-body Newton/PPN source normalization, because material surfaces or contact multipoles can still affect integrated mass and exterior fields.
- So the local-GR branch improves, but no full local-GR/Newton claim is promoted.

## Local Source Register
| source_id | path | exists | parseable | usage | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LSRC3356_0_3355_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3355-Y5-R2FR-boundary-contact-zero-flux-or-contact-bound-under-AX1090.md | true | true | 3355 boundary/contact split and next target | false |
| LSRC3356_1_3355_decomposition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3355_BOUNDARY_CONTACT_DECOMPOSITION.csv | true | true | contact/interface survivor definition | false |
| LSRC3356_2_3355_lemmas | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3355_ZERO_FLUX_LEMMA_ROWS.csv | true | true | compact support and contact survivor lemmas | false |
| LSRC3356_3_3355_eps | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3355_EPSILON_BOUNDARY_CONTACT_SPLIT.csv | true | true | epsilon boundary/contact split | false |
| LSRC3356_4_3355_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3355_CONTACT_BOUND_TEMPLATE.csv | true | true | numeric contact-bound template | false |
| LSRC3356_5_3355_gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3355_PROMOTION_GATES.csv | true | true | 3355 gate status | false |
| LSRC3356_6_3354_alias | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3354_ALIAS_FAMILY_INVENTORY.csv | true | true | alias closure handoff | false |
| LSRC3356_7_3350_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3350_EXPLICIT_RESIDUAL_ROWS.csv | true | true | original local residual rows | false |
| LSRC3356_8_boundary_alpha3 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv | true | true | prior boundary no-flux attempt | false |

## Local Collar Support Theorem
| theorem_id | object | statement | proof_or_rule | result | claim_scope | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| COL3356_0_contact_support_set | C_contact = supp(T_contact) | Treat contact/interface leakage as a closed support set for a distributional source term. | Distributional contact terms act only on test variations whose support intersects their support. | DEFINITION_FOR_LOCAL_TEST_FUNCTIONS | local variational calculus | false |
| COL3356_1_pointwise_collar | p notin C_contact | For any local bulk point outside contact support, there exists an open collar/ball U_p with compact closure and U_p cap C_contact = empty. | Closed-set separation/topological locality: positive distance to closed support in a sufficiently small coordinate patch. | PASS_LOCAL_POINTWISE_ZERO | bulk pointwise Euler-Lagrange equation away from contact support | false |
| COL3356_2_test_variation_zero | delta fields with supp(delta) subset U_p | The contact variation is zero for all compact-support variations inside U_p. | <T_contact, delta g> = 0 because supp(delta g) cap supp(T_contact) = empty. | EPSILON_CONTACT_LOCAL_BULK_ZERO | local bulk equations only | false |
| COL3356_3_integrated_source_warning | whole body, material surface, orbital/PPN source multipoles | The collar theorem does not remove contact support that lies on the material boundary or contributes to integrated source multipoles. | Whole-body integrals and exterior fields can receive surface/contact distributions even when pointwise bulk equations away from the surface are clean. | GLOBAL_NEWTON_PPN_NOT_CLOSED | integrated source normalization and exterior solution | false |

## Arena Classification
| arena_id | arena | contact_support_relation | epsilon_boundary_contact_status | what_this_closes | what_remains_open | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ARENA3356_0_interior_bulk | ordinary material interior / vacuum bulk point away from contact support | disjoint by collar choice | 0_for_local_bulk_equation | pointwise contact leakage in local Euler-Lagrange equation | parent-domain signature; whole-source integration | false |
| ARENA3356_1_material_surface | ordinary material boundary or interface | may intersect local source support | OPEN_UNLESS_SURFACE_STRESS_IS_ORDINARY_HILBERT_OR_ZERO | nothing global | surface stress ownership, contact amplitude, no-marker/no-flux premise | false |
| ARENA3356_2_exterior_orbital_field | exterior gravitational field sourced by integrated body | contact support can affect multipole moments through boundary integrals | OPEN_AS_SOURCE_NORMALIZATION_RESIDUAL | local vacuum field equations away from contact support | GM normalization, PPN multipoles, orbital source support | false |
| ARENA3356_3_scalar_monopole_contact | universal scalar stationary contact/monopole | support may exist but projects only to constant monopole if premises hold | CALIBRATION_ONLY_IF_PARENT_OWNED | vector/preferred-frame leakage conditionally | parent ownership of scalar homogeneous marker-free premises | false |

## Epsilon Contact Update
| update_id | symbol | arena | value_or_bound | authority | component_status | valid_for_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ECU3356_0_pointwise_bulk | epsilon_boundary_contact[p] | p notin supp(T_contact) | 0 | local collar support theorem | EXACT_LOCAL_POINTWISE_ZERO | true | false |
| ECU3356_1_surface_contact | epsilon_boundary_contact_surface | p in supp(T_contact) or local variations intersect interface | MISSING_SURFACE_STRESS_OWNER_OR_NUMERIC_CONTACT_BOUND | 3355 contact template retained | OPEN | false | false |
| ECU3356_2_integrated_source | epsilon_boundary_contact_integrated | whole-body Newton/PPN/orbital source | MISSING_INTEGRATED_CONTACT_MULTIPOLE_OR_MONOPOLE_CALIBRATION_THEOREM | collar theorem explicitly insufficient for integrated source | OPEN | false | false |

## Newton / PPN Implications
| row_id | target | 3356_effect | status | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NPPN3356_0_local_vacuum | local vacuum/bulk field equation away from contact support | contact/interface source term is zero pointwise | IMPROVED_CONDITIONAL_ROUTE | left-hand EH/Newton operator and parent-domain signature still need collapse | false |
| NPPN3356_1_Newton_source | Newtonian Poisson source and measured GM | bulk contact is killed away from surfaces, but surface/contact distributions may renormalize integrated mass | NOT_CLOSED | requires surface stress ownership or universal monopole calibration theorem | false |
| NPPN3356_2_PPN_multipoles | PPN residual vector and preferred-frame/source multipoles | pure scalar stationary boundary remains conditionally safe; vector/contact support remains retained | NOT_CLOSED | requires no-marker/no-vector/no-normal-flux parent ownership | false |

## Promotion Gates
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3356_0_pointwise_contact_zero | epsilon_boundary_contact vanishes for local bulk equations away from contact support | true | compact collar disjoint from closed contact support makes distributional contact variation zero | false |
| GATE3356_1_surface_contact_zero_or_bound | surface/interface contact source is zero, ordinary Hilbert-owned, or source-backed bounded | false | surface stress/contact amplitude not parent-owned or numeric | false |
| GATE3356_2_integrated_Newton_source_closed | integrated Newton/PPN source normalization is closed against contact support | false | whole-body surface/contact multipoles remain open | false |
| GATE3356_3_parent_domain_ready_for_collapse | boundary/contact blocker is reduced enough to attempt parent-domain signature collapse | true | remaining contact branch is typed as surface/integrated-source ownership rather than generic boundary leakage | false |
| GATE3356_4_local_GR_claim | local GR/Newton source-coupling branch is claim-ready | false | surface/integrated contact source and parent-domain signature remain unpromoted | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3356_0 | Did 3356 prove the contact branch away? | partly: exact pointwise bulk zero, not whole-source zero | local collars kill distributional contact terms away from their support, but material surfaces/integrated source multipoles can still matter | collapse parent-domain signature with explicit remaining surface/integrated-source caveat, then attack surface stress ownership | false |
| DEC3356_1 | Is this enough to try the parent-domain signature certificate? | yes as an intermediate theorem gate | generic source-shadow/readout/boundary fog has been reduced to named residuals with exact local-bulk zeros and explicit surface exceptions | 3357 parent-domain signature collapse attempt | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3357-Y5-R2FR-parent-domain-signature-collapse-under-AX1090.md | scripts/Y5_R2FR_3357_parent_domain_signature_collapse.py | combine 3346 parent action syntax, 3354 alias reductions, 3355 boundary split, and 3356 collar theorem into one parent-domain signature certificate with explicit remaining surface/integrated-source caveats | 3356 has narrowed the contact blocker enough that the parent-domain proof can be attempted honestly | false |
| 3358-Y5-R2FR-surface-stress-owner-or-contact-multipole-bound-under-AX1090.md | scripts/Y5_R2FR_3358_surface_stress_owner_or_contact_multipole_bound.py | prove surface/contact stress is ordinary Hilbert-owned or universal monopole-only, or build a finite no-cancellation contact multipole bound | this is the remaining Newton/PPN source-normalization survivor after local collar exclusion | false |
