# 2400 — Ordinary Matter Exchange Graph Connectivity And Source-Shadow Ban Or Delta-w Block Bound

## Result

This checkpoint gives the cleanest coupling result so far:

If ordinary matter sectors are vertices in an exchange graph `G_ord`, and an edge `A--B` means the parent matter equations allow a nonzero exchange current `C_AB^nu`, then the weighted source ansatz

`E^{mu nu}=kappa_0 sum_A (1+epsilon_A) T_A^{mu nu}`

is Bianchi/Noether consistent on that edge only if

`(epsilon_A-epsilon_B) C_AB^nu=0`.

For a genuine nonzero edge this forces `epsilon_A=epsilon_B`.  Along a connected component, equality propagates.  So species-level source weights collapse into one common calibration per connected ordinary exchange block.

That is a real tightening: the old wound `delta_w_species` becomes

`delta_w_block + delta_w_shadow`.

The remaining loopholes are now sharp:

1. prove the ordinary matter exchange graph has one connected component under the parent action;
2. prove no source-shadow functional can return hidden non-Hilbert source weights.

Neither is promoted here.  Local GR/Newton remains blocked.

## Source Register

| source_id | source_path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC2400_2399_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2399-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md | true | immediate parent: selected exchange graph/source-shadow target | false |
| SRC2400_2399_label_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2399_LABEL_FORGETTING_PROOF_ATTEMPT.csv | true | species-label forgetting proof attempt | false |
| SRC2400_2399_domain_fork | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2399_SOURCE_DOMAIN_FORK_AUDIT.csv | true | counterdomains left open by 2399 | false |
| SRC2400_1765_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md | true | earlier total-Hilbert/no-prefactor attempt | false |
| SRC2400_1765_no_source_prefactor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv | true | same-action and exchange-filter source | false |
| SRC2400_1765_total_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv | true | total Hilbert owner and source-shadow gap | false |
| SRC2400_954_parent_clause | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv | true | older parent-action source-side clause | false |
| SRC2400_977_constant_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv | true | constant source certificate attempt and Bianchi caveat | false |

## Exchange Graph Definition

| row_id | object | definition | condition | status | issue | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EG2400_0_vertices | ordinary matter exchange graph vertices | V_ord={A: ordinary Hilbert-source sector T_A is present in S_matter} | sector stress must be obtained from the same observed coframe/metric variation | DEFINITION | component choices are bookkeeping until the parent action fixes the actual matter ontology | false |
| EG2400_1_edges | exchange edges | edge A--B exists when an allowed parent matter solution has nonzero local exchange current C_AB^nu with nabla_mu T_A^{mu nu}=C_AB^nu and nabla_mu T_B^{mu nu}=-C_AB^nu | exchange current must be ordinary-sector, not a hidden source-shadow return | DEFINITION | needs parent-signed matter-sector map before real SM/clock/orbital cases can be stamped | false |
| EG2400_2_components | connected ordinary source blocks | B_I are connected components of G_ord=(V_ord,E_exchange); T_BI=sum_{A in B_I} T_A | within a connected component, arbitrary allowed exchange histories are admitted | DERIVED_BOOKKEEPING | if G_ord is not connected, each component may carry one common residual weight | false |
| EG2400_3_weighted_source | weighted source ansatz | E^{mu nu}=kappa_0 sum_A (1+epsilon_A) T_A^{mu nu} | epsilon_A are constant source weights after the same-action filter has removed action-level duplication | TEST_ANSATZ | nonconstant epsilon_A would create derivative terms and is a separate forbidden slot | false |

## Connectivity Proof Attempt

| row_id | claim | derivation | condition | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CONN2400_0_bianchi_start | Bianchi/Noether consistency tests weighted source universality | 0=nabla_mu E^{mu nu}=kappa_0 sum_A (1+epsilon_A) nabla_mu T_A^{mu nu} | geometric left side has the GR/EH identity and matter equations give sum_A nabla_mu T_A^{mu nu}=0 | only weighted exchange imbalance remains | CONDITIONAL_DERIVATION | false |
| CONN2400_1_edge_constraint | one nonzero exchange edge collapses two weights | for an A--B exchange, weighted divergence contains (epsilon_A-epsilon_B) C_AB^nu | C_AB^nu can vary over allowed local histories and is not identically zero | epsilon_A=epsilon_B on that edge | CONDITIONAL_THEOREM | false |
| CONN2400_2_connected_component | connected ordinary exchange component has one common calibration | edge equality propagates along every path in G_ord, so epsilon_A=epsilon_B for all A,B in the same B_I | G_ord component is connected through nonzero ordinary exchange currents | T_active on B_I is kappa_I T_BI rather than species-by-species kappa_A T_A | CONDITIONAL_THEOREM | false |
| CONN2400_3_global_connectivity | all ordinary matter has one common source calibration | if G_ord has exactly one connected component, all epsilon_A collapse to epsilon_common | parent signs ordinary matter exchange connectivity and no source-shadow sector returns independent weights | delta_w_block=0 up to one absorbed Newton/G calibration | NOT_CLAIMED | false |
| CONN2400_4_current_verdict | current MTS proves local source universality | 2399+2400 derive the collapse rule, not the parent-signed connectivity/source-shadow facts | missing parent matter ontology, hidden source-shadow exclusion, and arena projections | delta_w_species is no longer the right wound; delta_w_block plus delta_w_shadow are the remaining wounds | PARTIAL_REFINEMENT_NOT_PROOF | false |

## Source-Shadow Ban Audit

| row_id | slot | definition | needed_ban | status | issue | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SSB2400_0_forbidden_shape | source-shadow functional | S_shadow[e_obs,Phi]=sum_I eta_I int d^4x sqrt(-g_obs) U_I(Phi,e_obs,T_BI) whose metric/coframe derivative contributes to the active source but is not ordinary matter stress | parent action grammar must exclude source-only, representative-dependent, and post-variation source weighting functionals | IDENTIFIED_NOT_EXCLUDED | same-action filter does not by itself ban a hidden gravitational/source functional | false |
| SSB2400_1_total_hilbert_owner | total Hilbert source owner | T_total := -2/sqrt(-g_obs) delta S_matter/delta g_obs; interactions and binding stresses are inside this same derivative | no independent active-source owner besides S_matter and the geometric EH/MTS side | PARTIAL_FROM_1765_954_977 | existing clauses state the need but do not yet prove the parent grammar | false |
| SSB2400_2_disformal_weyl_return | representative-dependent return | matter sees e_obs but hidden Weyl/disformal dependence of e_obs on MTS fields can return apparent source weights after projection | observed coframe/frame lock plus quotient invariance must eliminate direct species/block-labelled coefficients | OPEN | ties back to the R2FR frame-source leak and q_loc closure gates | false |
| SSB2400_3_current_verdict | source-shadow ban | no non-Hilbert ordinary-source functional may feed q_loc^nu or local field equations | explicit parent-action exclusion theorem | BLOCKED_AS_PROOF | without this theorem, local GR remains a conditional branch rather than a derived limit | false |

## Delta-w Block Bound Input

| row_id | residual | definition | observable_link | needed_input | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DWB2400_0_delta_w_block | delta_w_block | max_{I,J}\|epsilon_I-epsilon_J\| over disconnected ordinary exchange components B_I | WEP/R10, PPN, clock-comparison, orbital composition tests | parent-signed component map plus arena projection coefficients | BOUND_INPUT_NOT_NUMERIC | false |
| DWB2400_1_delta_w_shadow | delta_w_shadow | effective source-weight leakage from non-Hilbert source-shadow functionals or representative-dependent returns | same arenas as delta_w_block, plus local q_loc residual vector | source-shadow exclusion theorem or explicit shadow coupling coefficient | ROOT_BLOCKER | false |
| DWB2400_2_single_component_common_mode | epsilon_common | one universal common calibration on a connected ordinary component | absorbed into measured G/Newton normalization, not a WEP-violating local residual | one connected ordinary component and no source shadow | BENIGN_IF_PARENT_SIGNED | false |
| DWB2400_3_bound_rows | delta_w_block_bound_pack | future numeric pack should carry tau_R10, tau_PPN, tau_clock, tau_orbital and projection coefficients K_X,Qbar_XH,lambda_X | local tests if proof route fails | real source-backed bounds and parent projection coefficients | NOT_BUILT_NUMERICALLY_HERE | false |

## Decision Ledger

| row_id | decision | reason | consequence | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2400_0_keep_derivation_route | keep deriving rather than jumping to fits | exchange connectivity gives an exact equality theorem if parent facts are signed | do not spend the next step on numeric delta_w bounds until source-shadow grammar is attacked | false |
| DEC2400_1_refine_wound | replace species wound with block/shadow wound | Noether/Bianchi exchange edges force equal weights inside connected ordinary components | future local tests should bound delta_w_block and delta_w_shadow, not raw species weights | false |
| DEC2400_2_no_local_GR_promotion | do not promote local GR/Newton reduction | ordinary exchange graph connectivity and source-shadow exclusion are not parent-signed | GR bridge remains promising but conditional | false |
| DEC2400_3_next | attack source-shadow exclusion grammar next | this is now the highest-leverage remaining coupling loophole | select 2401 source-shadow functional exclusion parent-action grammar | false |

## Claim Gates

| row_id | gate | status | why | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2400_0_exchange_connectivity | ordinary exchange graph connected | BLOCKED | 2400 proves the consequence of connectivity, not the parent-signed graph itself | false |
| CG2400_1_source_shadow_ban | source-shadow functional excluded | BLOCKED | no explicit parent-action grammar theorem yet forbids hidden source functional returns | false |
| CG2400_2_delta_w_block_zero | delta_w_block=0 | BLOCKED | requires one connected ordinary block plus source-shadow ban | false |
| CG2400_3_GR_Newton | local GR/Newton reduction | BLOCKED | source universality is refined but not closed | false |

## Refusal Runner

| row_id | claim | allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| REF2400_0_claim_connected_graph | MTS proves all ordinary matter sectors are exchange-connected | false | requires parent-signed matter ontology and exchange-current graph | false |
| REF2400_1_claim_no_source_shadow | MTS excludes all source-shadow functionals | false | source-shadow grammar has been isolated but not proved impossible | false |
| REF2400_2_claim_local_GR | local GR/Newton limit is derived | false | 2400 is a coupling-collapse lemma, not the final local limit proof | false |

## Next Target

| row_id | next_doc | why | expected_output | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2400_0_selected | 2401-Y5-R2FR-source-shadow-functional-exclusion-parent-action-grammar-or-shadow-bound-pack.md | source-shadow is now the cleanest remaining loophole after exchange-connectivity collapses block weights conditionally | either a parent grammar theorem banning source shadows, or a source-shadow bound pack with explicit nonclaim rows | false |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2400_00_sources_exist | PASS | all required source paths exist |
| VAL2400_01_needles_found | PASS | all source needles found |
| VAL2400_02_exchange_graph_defined | PASS | ordinary exchange graph and edge current are defined |
| VAL2400_03_edge_collapse_theorem | PASS | edge exchange collapse theorem recorded |
| VAL2400_04_block_refinement | PASS | raw species wound refined to block/shadow wounds |
| VAL2400_05_source_shadow_retained | PASS | source-shadow route is isolated but not claimed closed |
| VAL2400_06_global_claims_blocked | PASS | exchange connectivity, shadow ban, delta_w zero, and GR/Newton gates remain blocked |
| VAL2400_07_csv_parse | PASS | generated CSVs parse and have rows |
| VAL2400_08_no_claim_flags | PASS | no generated row has valid_for_claim=true |
| VAL2400_09_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs |
| VAL2400_10_next_selected | PASS | source-shadow grammar route selected next |
| VAL2400_OVERALL | PASS | 2400 derives the exchange-edge weight-collapse lemma, refines the coupling wound to delta_w_block/delta_w_shadow, refuses local-GR promotion, and selects source-shadow grammar next |

## Practical Status

The coupling problem is not solved, but it is now much less foggy.  We no longer have to fear arbitrary
species-by-species source weights if the ordinary source graph is connected.  The real enemy is narrower:
either disconnected conserved source blocks, or a hidden source-shadow functional.  That makes the next proof
target precise enough to attack rather than just circle.
