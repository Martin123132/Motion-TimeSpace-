# 1127 - Y5/R10 Local-vs-FLRW Branch Selector No-Flux Certificate

**Current verdict:** the local-vs-FLRW split has the right conditional shape, but the parent branch selector is not closed. Local `epsilon_domain_flux=0` is still conditional, while FLRW memory is conditionally preserved.

**Good news:** the route does not require killing cosmology. A serious branch selector would set the compact local branch to exact/trivial while keeping the coherent FLRW branch active.

**Guard:** global all-domain zero is forbidden because it would erase the cosmological memory mechanism.

**No claim:** no domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1127.

## Source Register
| source_id | relative_path | exists | needle | needle_found | note |
| --- | --- | --- | --- | --- | --- |
| SRC1127_0_1126_next | source-intake/mts_residuals/P8_Y5_R10_1126_NEXT_TARGET.csv | true | NEXT1126_0_1127 | true | 1126 handoff to local-vs-FLRW branch selector. |
| SRC1127_1_1126_obligations | source-intake/mts_residuals/P8_Y5_R10_1126_SELECTOR_LOCAL_FLUX_OBLIGATIONS.csv | true | OB1126_2_branch_selector | true | 1126 requires local-vs-FLRW branch selector. |
| SRC1127_2_602_gate | source-intake/mts_residuals/P8_Y5_R10_602_LOCAL_FLRW_BRANCH_GATE.csv | true | LFG602_2_FLRW_active | true | 602 supports FLRW-active branch conditionally. |
| SRC1127_3_609_split | source-intake/mts_residuals/P8_Y5_R10_609_LOCAL_FLRW_BRANCH_SPLIT_GATE.csv | true | LF609_2_no_overstrong_zero | true | 609 forbids global all-domain zero because it kills cosmology. |
| SRC1127_4_822_FLRW | source-intake/mts_residuals/P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv | true | F822_1_FLRW_time | true | 822 gives conditional FLRW N_D=-ln(a)=ln(1+z) reduction. |
| SRC1127_5_ownership | source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv | true | P3_local_trivial_representative | true | Local trivial representative remains conditional. |
| SRC1127_6_no_vector | source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv | true | T2_no_flux_local_representative | true | No-flux local representative is conditional, not parent-derived. |
| SRC1127_7_newton_stack | source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv | true | SN4_closed_Meff_flux | true | Newton/local-GR stack keeps closed flux not parent-derived. |

## Branch Selector Audit
| branch_id | branch | needed_statement | current_support | current_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BS1127_0_local | compact stationary local branch | N_D=0 or equivalent exact/trivial local domain representative, giving epsilon_domain_flux=0 | 602/609/T2 give conditional local-zero/no-flux route | CONDITIONAL_NOT_PARENT_DERIVED | local trivial relative class and scalar selector are not parent-owned | false |
| BS1127_1_FLRW | coherent FLRW/cosmological memory branch | N_D>0 or coherent expansion class remains active, with N_D=-ln(a)=ln(1+z) in FLRW | 602/609/822 give conditional support for active FLRW shape | CONDITIONAL_SUPPORTED_NOT_PARENT_OWNED | Q_coh/P_coh/domain normalization and selector ownership are not parent-derived | false |
| BS1127_2_no_overstrong_zero | global all-domain zero | forbidden route: all domains globally zero | 609 marks this as forbidden because it kills cosmological memory | FORBIDDEN_GUARD | not a unification route | false |
| BS1127_3_verdict | parent local-vs-FLRW selector | one parent selector yields local exact/trivial branch and FLRW coherent active branch without outcome fitting | conditional shape exists but parent ownership is missing | BRANCH_SELECTOR_NOT_CLOSED | same selector must produce both branches from parent variables, not hand-picked domains | false |

## Candidate Rule
| rule_id | candidate_rule | formal_shape | status | must_prove | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR1127_0_selector_variable | B_D selects branch by parent-owned invariant N_D or coherent determinant/current class | B_D=local if N_D=0 or [J_D]_local exact; B_D=FLRW if N_D>0/coherent expansion class | CANDIDATE_NOT_PARENT_DERIVED | N_D/Q_coh/P_coh exists before empirical readout and is varied/owned by parent action | false |
| BR1127_1_local_zero_effect | local branch implies q_D_vector_flux=0 | B_D=local -> epsilon_domain_flux=0 -> W_domain_alpha3*epsilon_domain_flux=0 | CONDITIONAL_EFFECT_ONLY | local branch condition is parent-selected, not imposed plateau | false |
| BR1127_2_FLRW_survival | FLRW branch keeps cosmological memory active | B_D=FLRW -> N_D=-ln(a)=ln(1+z), Q_coh positive/oriented, memory projection active | CONDITIONAL_SUPPORTED | Q_coh/P_coh and normalization are parent-owned, not fit-history imported | false |
| BR1127_3_no_data_gate | branch selector cannot use residual success or empirical fit quality | B_D depends only on parent scalar/topological/boundary-current ingredients | POLICY_PASS_NOT_POSITIVE_DERIVATION | actual parent ingredients exist and are sufficient | false |

## Effects If Closed
| effect_id | if_statement | then_statement | claim_effect | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EFF1127_0_if_closed_local | parent selector closes local exact/trivial branch | epsilon_domain_flux=0 locally; q_D_vector_flux alpha3 branch collapses | would unblock one direct alpha3 path, but R11 source-normalization/stress siblings remain guarded | CONDITIONAL_ONLY | false |
| EFF1127_1_if_closed_FLRW | same parent selector preserves coherent FLRW branch | cosmological memory route remains available for FLRW tests | prevents local-GR proof from deleting cosmology mechanism | CONDITIONAL_ONLY | false |
| EFF1127_2_if_not_closed | branch selector remains unsigned | 1126 executable product rows stay active and alpha3 remains blocked | no PPN/R10/local-GR promotion | ACTIVE_CURRENT_STATE | false |

## Claim Gates
| gate_id | rule | gate_pass | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| G1127_0_local_branch | local branch exact/trivial representative is parent-derived | false | local representative remains conditional | false |
| G1127_1_FLRW_branch | FLRW active branch is parent-owned | false | FLRW shape is conditionally supported but Q_coh/P_coh ownership is missing | false |
| G1127_2_no_overstrong_zero | global all-domain zero is forbidden | true_nonclaim | 1127 keeps this guard explicit | false |
| G1127_3_qD_flux_closed | q_D_vector_flux=0 follows from branch selector | false | branch selector is not parent-owned | false |
| G1127_4_local_GR | local-GR/PPN branch can promote | false | alpha3 flux, R11 source-normalization, and stress siblings remain blocked | false |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1127_0_verdict | branch_selector_not_closed | local/FLRW split has conditional support but lacks parent-owned selector variables | derive parent ownership of N_D/Q_coh/P_coh or return to executable flux products | false |
| D1127_1_best_next | parent_selector_ownership_first | this is the cleanest way to silence local flux without killing cosmology | prove N_D/Q_coh/P_coh are parent variables with branch conditions | false |
| D1127_2_guard | do_not_use_global_zero | global all-domain zero would erase FLRW/cosmological memory | keep local and FLRW branches separate | false |

## Validation
| check_id | result | detail | valid_for_claim |
| --- | --- | --- | --- |
| V1127_0_sources_exist | pass | all cited local source paths exist and needles are found | false |
| V1127_1_branch_coverage | pass | local, FLRW, forbidden global-zero, and selector verdict rows are covered | false |
| V1127_2_selector_not_closed | pass | branch selector remains unclosed | false |
| V1127_3_FLRW_preserved | pass | FLRW active branch shape is preserved | false |
| V1127_4_no_overstrong_zero_guard | pass | global all-domain zero is forbidden | false |
| V1127_5_gates_blocked | pass | claim gates remain blocked | false |
| V1127_6_no_claim_rows | pass | all generated rows remain nonclaim | false |
| V1127_7_next_target | pass | 1128 handoff targets parent branch selector ownership | false |
| V1127_8_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | false |
| V1127_9_csv_parse | pass | all 1127 CSV outputs parse cleanly | false |
| V1127_10_formalization_untouched | pass | generator writes no outputs under formalization-workbench | false |
| V1127_SUMMARY | pass | 1127 preserves local/FLRW split as conditional and keeps alpha3 blocked | false |

## Next Target
| next_id | next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT1127_0_1128 | 1128-Y5-R10-parent-branch-selector-ownership-ND-Qcoh-Pcoh.md | derive parent ownership of the branch selector variables N_D, Q_coh, and P_coh so local exact/trivial branch and FLRW active branch come from one rule rather than hand-picked domains | N_D; Q_coh; P_coh; local N_D=0; FLRW N_D=ln(1+z); no empirical selector; no global all-domain zero; alpha3 flux guard | killing cosmology; plateau axiom; tuned cancellation; local-GR claim; GitHub; formalization edits | false |
