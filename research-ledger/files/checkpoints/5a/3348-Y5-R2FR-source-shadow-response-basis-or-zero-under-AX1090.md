# 3348 — Source-Shadow Response Basis Or Zero Under AX1090

Generated: `2026-06-28T03:07:24.576367+00:00`

## Summary
- This checkpoint attacks the `R_AB` material/source response factor exposed by 3347.
- The important result is a fork: on the ordinary connected Hilbert-source branch, `R_AB=0` after measured-`G_N` calibration; a nonzero `R_AB` is not Hilbert stress, it is an explicit spurion/projector charge basis.
- The previous `R_TiPt=1` row is demoted to schema smoke only, not physics.
- The lower-scrutiny next route is to source-sign the ordinary matter exchange graph; if that fails, build a source-backed Ti/Pt charge table for the finite-bound branch.

## Response Basis Theorem
| theorem_id | claim_piece | mathematical_form | derivation | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RTH3348_0_definition | R_AB is a projection, not a primitive constant | eta_AB ~= epsilon_source_shadow R_AB; R_AB := P_AB[Pi_rel(T_H)] / \|\|T_H\|\| | 3347 split P_src into common mode plus relative projector; only the relative projector can survive measured-G calibration. | DERIVED_FROM_3347 | false |
| RTH3348_1_hilbert_connected_zero | ordinary Hilbert-connected matter has no independent R_AB slot | if T_active=T_H=sum_i T_i and sum_i nabla_mu T_i^{mu nu}=0 on a connected exchange graph, then weighted conservation forces w_i=w_* and R_AB^Hilbert=0 | Noether exchange constraints on connected matter components collapse relative weights to one common measured-G calibration. | EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | false |
| RTH3348_2_spurion_response_fork | nonzero R_AB requires an extra material/source charge basis | R_AB(beta)=beta dot (chi_A-chi_B), chi in {electron fraction, proton/neutron split, EM binding, nuclear binding, lattice/boundary marker, hidden marker} | A nonzero material response is not produced by the total Hilbert stress alone; it is a source projector, spurion, or extension coefficient that must be parent-owned or empirically bounded. | DERIVED_FORK_TO_EXPLICIT_RESIDUAL_BASIS | false |
| RTH3348_3_current_verdict | current MTS response basis | R_AB is either 0 on the signed Hilbert-connected branch, or symbolic beta dot Delta chi_AB on the unsigned extension branch | The unit response row is demoted to smoke only; future claims need either graph/parent closure or source-backed material charge rows. | DICHOTOMY_CLOSED_RESPONSE_NOT_CLAIMED | false |

## Hilbert Graph Collapse
| graph_id | component | constraint | derivation_use | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HGC3348_0_nodes | ordinary atomic/nuclear matter components | nodes={charged leptons, protons, neutrons, EM binding, nuclear binding, molecular/lattice binding} | defines the candidate connected Hilbert-source graph whose relative weights would collapse | CANDIDATE_NODE_BASIS_FROM_2616_NOT_PUBLIC_SOURCED | false |
| HGC3348_1_exchange_constraint | interacting component currents | nabla_mu T_i^{mu nu}=C_i^nu and sum_i C_i^nu=0; source conservation of sum_i w_i T_i requires sum_i w_i C_i^nu=0 | nonzero exchange edges force equal source weights across connected nodes | DERIVED_CONDITIONAL_GRAPH_THEOREM | false |
| HGC3348_2_common_mode | connected ordinary component | w_i=w_* for all nodes in the connected component | w_* rescales kappa and is absorbed into measured G_N; it gives no WEP R_AB | DERIVED_COMMON_MODE_COLLAPSE | false |
| HGC3348_3_decoupled_exception | decoupled conserved block | nabla_mu T_D^{mu nu}=0 independently | a decoupled block can keep an independent source weight only if it is inventoried in the local arena and bounded | RESIDUAL_EXCEPTION_REQUIRES_ARENA_INVENTORY | false |

## Material Response Basis
| basis_id | branch | basis | R_TiPt | formula | status | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RB3348_0_hilbert_total | zero-route | total Hilbert stress T_H | 0 | R_AB^Hilbert=0 after common measured-G calibration | EXACT_CONDITIONAL_IF_PARENT_AND_GRAPH_SIGNED | parent source map and source-backed connected matter graph are not yet fully signed | false |
| RB3348_1_common_mode | calibration-route | universal source scale C_0 | 0 | G_N=G_*(1+C_0), so differential WEP response cancels | DERIVED_COMMON_MODE_NOT_LOCAL_WEP_RESIDUAL | global/cosmological calibration treated separately | false |
| RB3348_2_spurion_vector | finite-bound-route | chi_k material/source charges | beta dot (chi_Ti-chi_Pt) | eta_TiPt ~= epsilon_source_shadow beta_k Delta chi_k(Ti,Pt) | SYMBOLIC_EXTENSION_BASIS_NOT_PARENT_DERIVED | need source-backed Ti/Pt material composition, binding-energy convention, and beta normalization | false |
| RB3348_3_unit_smoke | smoke-only-route | private unit response | 1 | epsilon_source_shadow <= eta_TiPt for schema testing only | DEMOTED_SCHEMA_SMOKE_ONLY | unit response is not a derived MTS material basis | false |

## Bound Reinterpretation
| bound_id | branch | observable | response_factor | bound_or_theorem | numeric_value | source_path | valid_for_component_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BR3348_0_hilbert_zero_branch | zero-route | eta_TiPt | R_TiPt=0 | no finite division is used; source-shadow response is absent if Hilbert-connected parent branch closes | theorem_zero_conditional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3347_LOCAL_NEWTONIAN_PROJECTION.csv | false | false |
| BR3348_1_symbolic_spurion_branch | finite-bound-route | eta_TiPt | R_TiPt=beta dot Delta chi_TiPt | \|epsilon_source_shadow\| <= 4.245906e-15 / \|beta dot Delta chi_TiPt\| | symbolic_until_chi_and_beta_sourced | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv | false | false |
| BR3348_2_unit_smoke_branch | smoke-only-route | eta_TiPt | R_TiPt=1 | \|epsilon_source_shadow\| <= 4.245906e-15 | 4.245906e-15 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv | true | false |

## Promotion Gates
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3348_0_response_dichotomy | R_AB is either zero on the Hilbert-connected branch or an explicit spurion/charge response | true | 3348 derives the Hilbert-collapse/spurion-fork structure | false |
| GATE3348_1_hilbert_zero_parent_signed | R_AB=0 is parent-signed for current MTS ordinary matter | false | parent source-map and source-backed connected graph certificate remain unsigned | false |
| GATE3348_2_unit_response_demoted | the previous unit response is treated only as smoke | true | 3348 preserves it only in BR3348_2_unit_smoke_branch with valid_for_claim=false | false |
| GATE3348_3_finite_response_claim | finite epsilon_source_shadow bound is claim-ready in MTS basis | false | beta and Delta chi_TiPt are symbolic until source-backed material composition and normalization are supplied | false |
| GATE3348_4_local_GR_claim | local GR/Newton source-coupling branch is claim-ready | false | source response basis is narrowed but not parent-signed or fully sourced | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3348_0 | Did 3348 derive R_AB as an MTS-owned material number? | not as a numeric claim | the derivation shows R_AB vanishes on the Hilbert-connected branch; nonzero R_AB is a symbolic spurion/charge basis requiring source-backed material rows | try to close the source-backed ordinary matter graph certificate before building empirical charge tables | false |
| DEC3348_1 | Did 3348 move beyond missing-ledger work? | yes | it demotes the unit response, proves the response fork, and identifies the lower-scrutiny route: no independent ordinary R_AB slot | 3349 should source-sign the connected Hilbert matter graph or explicitly fail into a material-composition table | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3349-Y5-R2FR-source-backed-ordinary-matter-graph-certificate-under-AX1090.md | scripts/Y5_R2FR_3349_source_backed_ordinary_matter_graph_certificate.py | source-sign the connected ordinary matter Hilbert graph enough to promote the R_AB=0 no-independent-slot route, or explicitly fail to the material charge-table branch | this is lower-scrutiny than fitting arbitrary WEP charges: if the graph closes, source-shadow material response is common-mode only | false |
| 3349b-Y5-R2FR-TiPt-material-charge-table-nonclaim.md | scripts/Y5_R2FR_3349b_TiPt_material_charge_table_nonclaim.py | if the graph route fails, acquire source-backed Ti/Pt composition and build symbolic/numeric Delta chi rows without claiming MTS local GR | needed only for the finite-bound spurion branch R_TiPt=beta dot Delta chi_TiPt | false |
