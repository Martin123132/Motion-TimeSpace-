# 1128 - Y5/R10 Parent Branch Selector Ownership: N_D, Q_coh, P_coh

**Current verdict:** parent ownership of `N_D`, `Q_coh`, and `P_coh` is not closed. The local/FLRW branch split has a useful conditional shape, but it is still not a parent-derived selector.

**Best candidate:** build one smooth parent invariant `I_D >= 0`, such as `||P_coh J_D||^2` or a normalized `det(Q_coh)`, with local `I_D=0` and FLRW `I_D>0`.

**Guard:** the selector cannot use empirical success, hand-picked domains, discontinuous readout masks, or global all-domain zero.

**No claim:** no local no-flux, domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1128.

## Source Register
| source_id | relative_path | exists | needle | needle_found | note |
| --- | --- | --- | --- | --- | --- |
| SRC1128_0_1127_next | source-intake/mts_residuals/P8_Y5_R10_1127_NEXT_TARGET.csv | true | NEXT1127_0_1128 | true | 1127 handoff to parent branch selector ownership. |
| SRC1128_1_1127_audit | source-intake/mts_residuals/P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv | true | BS1127_3_verdict | true | 1127 says branch selector has conditional shape but no parent ownership. |
| SRC1128_2_1127_rule | source-intake/mts_residuals/P8_Y5_R10_1127_CANDIDATE_BRANCH_RULE.csv | true | BR1127_0_selector_variable | true | 1127 candidate rule names N_D/Q_coh/P_coh ownership. |
| SRC1128_3_602_gate | source-intake/mts_residuals/P8_Y5_R10_602_LOCAL_FLRW_BRANCH_GATE.csv | true | LFG602_2_FLRW_active | true | 602 has conditional support for FLRW-active branch. |
| SRC1128_4_609_split | source-intake/mts_residuals/P8_Y5_R10_609_LOCAL_FLRW_BRANCH_SPLIT_GATE.csv | true | LF609_3_verdict | true | 609 says local/FLRW split is not closed and global zero is forbidden. |
| SRC1128_5_822_FLRW | source-intake/mts_residuals/P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv | true | F822_3_locked_shape | true | 822 gives conditional FLRW determinant/locked-shape reduction. |
| SRC1128_6_parent_contract | source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv | true | PAC1055_6_single_parent_action | true | 1055 parent contract gives one-action discipline but not branch selector derivation. |
| SRC1128_7_topological_route | source-intake/mts_residuals/P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv | true | TL1056_4_verdict | true | 1056 shows topological-level ownership routes need explicit inheritance theorem. |
| SRC1128_8_domain_ownership | source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv | true | P3_local_trivial_representative | true | Local trivial representative remains conditional. |
| SRC1128_9_newton_stack | source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv | true | SN4_closed_Meff_flux | true | Closed flux remains not parent-derived in Newton/local-GR stack. |

## Ownership Audit
| owner_id | object | candidate_meaning | parent_ownership_required | current_support | current_status | missing_certificate | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OWN1128_0_ND | N_D | domain branch scalar/log-volume or activation amplitude; FLRW reduction N_D=ln(1+z) | N_D is a parent variable or parent-derived invariant before readout, varied/owned in S_parent, and not fitted from residual success | 822 gives conditional volume/FLRW relation; 602/609 use N_D for local/FLRW split | CONDITIONAL_NOT_PARENT_OWNED | parent action term or invariant construction for N_D, plus local N_D=0 theorem | false | false |
| OWN1128_1_Qcoh | Q_coh | coherent load/current object whose determinant supplies FLRW active memory shape | Q_coh is selected by parent equations/projection, positive/oriented, and varied or stress-accounted before FLRW reduction | 822 gives conditional det(Q)=X_load^3 and locked shape if Q_coh exists | MISSING_PARENT_PROJECTION_AND_NORMALIZATION | formula for Q_coh from parent fields and proof it is not imported from fit history | false | false |
| OWN1128_2_Pcoh | P_coh | coherent projector selecting local trivial versus FLRW active memory/domain class | P_coh is an allowed parent projector/quotient map with variation/stress ownership and no readout-mask insertion | 1127 candidate rule needs P_coh; 1055 gives general parent quotient discipline | MISSING_PARENT_PROJECTOR_OWNERSHIP | projector construction, kernel/image algebra, variation ledger, and no empirical selector proof | false | false |
| OWN1128_3_BD | B_D branch selector | one rule: local if N_D=0/exact class, FLRW if N_D>0/coherent class | B_D is built from parent-owned N_D/Q_coh/P_coh and does not use residuals, fit quality, or hand-picked domains | 602 no-empirical-window gate passes as policy; 609 split has conditional support | RULE_SHAPE_READY_NOT_DERIVED | single parent selector theorem producing both local and FLRW branches | false | false |

## Parent Branch Action Contract
| contract_id | contract_clause | minimal_form | acceptance | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BA1128_0_parent_variables | declare branch ingredients before readout | S_parent contains or derives N_D[Phi], Q_coh[Phi], P_coh[Phi] before any empirical scoring | local and FLRW branch conditions are computed from parent fields only | MISSING_PARENT_FORMULA | false |
| BA1128_1_smooth_selector | avoid discontinuous hand-picked branch switch | use parent-owned invariant I_D>=0, e.g. I_D=||P_coh J_D||^2 or det(Q_coh) normalized, with local I_D=0 and FLRW I_D>0 | branch response can be smooth/double-zero and varied; no imposed plateau | CANDIDATE_NOT_DERIVED | false |
| BA1128_2_local_reduction | local branch certificate | I_D=0 -> N_D=0 -> [J_D]_local exact/trivial -> epsilon_domain_flux=0 | parent theorem, not local assumption, not data-selected | CONDITIONAL_NOT_PARENT_DERIVED | false |
| BA1128_3_FLRW_reduction | FLRW branch survival | homogeneous coherent branch -> N_D=-ln(a)=ln(1+z), Q_coh positive/oriented, memory projection active | same parent selector as local branch; no global zero | CONDITIONAL_SUPPORTED_NOT_PARENT_OWNED | false |
| BA1128_4_variation_and_stress | branch selector is varied or its stress is retained | delta_g N_D, delta_g Q_coh, delta_g P_coh terms are zero by theorem or mapped into residual rows | no hidden selector/domain stress in local GR reduction | MISSING_VARIATION_LEDGER | false |

## Reduction Checks
| check_id | statement | condition | status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RED1128_0_local_if_owned | If parent-owned I_D=0 in compact stationary local branch, then q_D_vector_flux can be zero. | N_D=0/exact local class plus scalar stationary selector and R11 vector silence | CONDITIONAL_ONLY | would close direct alpha3 flux path, but source-normalization/stress siblings remain guarded | false |
| RED1128_1_FLRW_if_owned | If parent-owned I_D>0 in coherent FLRW branch, cosmological memory remains active. | N_D=ln(1+z), Q_coh/P_coh owned, normalized, and not imported from fits | CONDITIONAL_SUPPORTED | preserves cosmology while allowing local no-flux | false |
| RED1128_2_global_zero_forbidden | A global all-domain zero selector is not allowed. | would set local and FLRW branch inactive together | FORBIDDEN_GUARD | prevents overstrong local-GR fix from destroying MTS cosmology | false |
| RED1128_3_current_verdict | Parent ownership of N_D/Q_coh/P_coh is not proved in current corpus. | OWN1128_0 through OWN1128_3 all need parent certificates | OWNERSHIP_NOT_CLOSED | alpha3/local-GR remains blocked | false |

## Claim Gates
| gate_id | rule | gate_pass | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| G1128_0_ND_owned | N_D is parent-owned and varied/owned | false | N_D has conditional FLRW/local use but no parent action certificate | false |
| G1128_1_Qcoh_owned | Q_coh is parent-owned, positive/oriented, normalized | false | Q_coh projection and normalization are not parent-derived | false |
| G1128_2_Pcoh_owned | P_coh projector is parent-owned with variation/stress ledger | false | P_coh construction and variation ownership are missing | false |
| G1128_3_no_empirical_selector | selector cannot use residual success or fit quality | true_nonclaim | policy guard is explicit and preserved | false |
| G1128_4_branch_selector_closed | one parent selector yields local exact and FLRW active branches | false | ownership certificates for N_D/Q_coh/P_coh are missing | false |
| G1128_5_alpha3_local_GR | local no-flux/alpha3/local-GR can promote | false | branch selector remains unclosed | false |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1128_0_verdict | parent_branch_selector_ownership_not_closed | N_D/Q_coh/P_coh have useful conditional shape but no parent ownership certificate | derive a parent invariant I_D or cohomology-norm selector action | false |
| D1128_1_best_next | cohomology_norm_selector_action_first | a single parent invariant I_D>=0 could distinguish local zero from FLRW active without empirical switching | try I_D=||P_coh J_D||^2 or det(Q_coh) as parent-owned smooth selector | false |
| D1128_2_guard | keep_global_zero_forbidden | global all-domain zero would erase FLRW/cosmological memory | preserve local/FLRW split and alpha3 guard | false |

## Validation
| check_id | result | detail | valid_for_claim |
| --- | --- | --- | --- |
| V1128_0_sources_exist | pass | all cited local source paths exist and needles are found | false |
| V1128_1_ownership_coverage | pass | N_D, Q_coh, P_coh, and branch selector ownership rows are present | false |
| V1128_2_contract_coverage | pass | parent branch action contract includes smooth selector invariant | false |
| V1128_3_reduction_guard | pass | ownership remains unclosed and global zero is forbidden | false |
| V1128_4_gates_blocked | pass | claim gates remain blocked except no-empirical-selector guard | false |
| V1128_5_no_claim_rows | pass | all generated rows remain nonclaim | false |
| V1128_6_next_target | pass | 1129 handoff targets cohomology-norm branch selector action | false |
| V1128_7_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | false |
| V1128_8_csv_parse | pass | all 1128 CSV outputs parse cleanly | false |
| V1128_9_formalization_untouched | pass | generator writes no outputs under formalization-workbench | false |
| V1128_SUMMARY | pass | 1128 sharpens parent ownership debt for N_D/Q_coh/P_coh and stages I_D selector target | false |

## Next Target
| next_id | next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT1128_0_1129 | 1129-Y5-R10-cohomology-norm-branch-selector-action-or-reject.md | try to construct a parent-owned smooth branch selector invariant I_D, such as ||P_coh J_D||^2 or normalized det(Q_coh), that gives local I_D=0 and FLRW I_D>0 without empirical switching | I_D; N_D; Q_coh; P_coh; smooth/double-zero response; variation/stress ledger; local no-flux; FLRW active branch | global all-domain zero; discontinuous hand-picked domains; empirical selector; local-GR claim; GitHub; formalization edits | false |
