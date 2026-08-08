# 649 Y5/R10 Local chi_X Silence Theorem or Ultra-Screened Alpha Branch

## Verdict

- Status: `Y5_R10_local_chiX_silence_conditional_not_parent_signed_ultra_screened_alpha_branch_formalized_nonclaim`
- Claim ceiling: `conditional_local_chiX_silence_theorem_plus_ultra_screened_finite_alpha_contract_only_no_clock_or_local_claim`
- The local silence theorem can be written as a clean conditional theorem, but the current corpus cannot sign its clauses.
- Therefore finite alpha is retained only as an ultra-screened nonclaim branch.
- Order-one `kappa_alpha` requires `|dchi_X/dN| <= 2.933e-08` in lab domains from the Yb clock product bound.

## Source Register

| source_id | label | path | exists | role |
| --- | --- | --- | --- | --- |
| S649_0 | checkpoint_648_doc | 648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md | true | prior clock product-bound fork |
| S649_1 | validation_648 | source-intake/mts_residuals/P8_Y5_BRR545_648_VALIDATION.csv | true | prior validation |
| S649_2 | product_runner_648 | source-intake/mts_residuals/P8_Y5_R10_648_CLOCK_PRODUCT_BOUND_RUNNER.csv | true | clock product-bound runner |
| S649_3 | tau_survival_648 | source-intake/mts_residuals/P8_Y5_R10_648_TAU_SURVIVAL_REQUIREMENTS.csv | true | tau survival requirements |
| S649_4 | local_attempt_648 | source-intake/mts_residuals/P8_Y5_R10_648_LOCAL_CHIX_DYNAMICS_ATTEMPT.csv | true | local chiX dynamics attempt |
| S649_5 | strict_local_coframe_242 | 242-strict-local-coframe-branch-or-domain-projector-action.md | true | strict local coframe conditional route |
| S649_6 | boundary_state_local_silence_300 | 300-boundary-state-local-silence-theorem-attempt.md | true | closed/gapped local silence conditional route |
| S649_7 | clock_functional_156 | 156-clock-projection-functional-theorem-or-demotion.md | true | clock scalar local-silence clue |
| S649_8 | parent_vertical_norm_644 | 644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md | true | demoted zero route and rescaling counterexamples |
| S649_9 | generator_script_649 | scripts/Y5_R10_local_chiX_silence_theorem_or_ultra_screened_alpha_branch.py | true | this checkpoint generator |

## Conditional Silence Theorem

| theorem_id | name | proof_status | corpus_status | consequence_if_signed |
| --- | --- | --- | --- | --- |
| LCS649 | conditional local chi_X silence theorem | proved_as_conditional_template | premises_unsigned | clock product bound is satisfied by tau_clock=0 without constraining standalone kappa_alpha |

## Silence Clause Audit

| clause_id | needed_statement | current_status | failure_mode | result_for_tau |
| --- | --- | --- | --- | --- |
| LCS649_0_domain_classifier | A parent domain classifier separates lab/bound systems from FLRW/open systems before fitting data. | not_parent_derived | local/FLRW split becomes an escape hatch if chosen after seeing clock bounds | no active tau_clock zero |
| LCS649_1_closed_gapped_lab_domain | Laboratory clock domains are closed/gapped in the chi_X boundary channel: [J_chi]_local=0 and rho_chi_local=0. | conditional_only | ordinary baths, horizons, galaxies, or time-dependent local systems may leak | tau_clock=0 only if closure/gap is parent-signed |
| LCS649_2_strict_matter_coframe | The local matter/clock coframe is strict and does not include chi_X or a direct alpha-pressure scalar. | conditional_only | if matter clocks see chi_X directly, clock bounds bite immediately | tau_clock=0 only if local representative is selected by parent action |
| LCS649_3_clock_scalar_vanishes | The signed clock scalar satisfies C_clock=0 for lab/local domains, e.g. X_D=0 or stationary bound-domain projection. | theorem_target_not_derived | cell clock scalar may be gauge/closure and not physical | not enough alone |
| LCS649_4_no_alpha_vertex | No local alpha_EM(chi_X), f_A(chi_X)F^2, or coframe leakage term survives in the lab effective action. | not_forbidden_by_current_corpus | lambda_A F^2/coframe leakage reopens finite alpha drift | blocks silence claim |
| LCS649_5_edge_cases | Clock experiments are not in an edge class that sources chi_X drift through radiation, horizons, material stress, or environmental coupling. | open | unmodeled lab/environment channel invalidates silence assumption | requires source ledger before claim |

## Ultra-Screened Alpha Branch

| branch_id | assumed_abs_kappa_alpha | required_abs_tau_clock_time_yr_inv_max | required_abs_dchi_dN_over_H0_max | branch_rule | status |
| --- | --- | --- | --- | --- | --- |
| USB649_0 | 0.01 | 2.100000e-16 | 2.932961e-06 | \|dchi_X/dN\| <= 2.933e-06 for \|kappa_alpha\|=0.01 | ultra_screened_nonclaim_contract |
| USB649_1 | 0.1 | 2.100000e-17 | 2.932961e-07 | \|dchi_X/dN\| <= 2.933e-07 for \|kappa_alpha\|=0.1 | ultra_screened_nonclaim_contract |
| USB649_2 | 1 | 2.100000e-18 | 2.932961e-08 | \|dchi_X/dN\| <= 2.933e-08 for \|kappa_alpha\|=1 | ultra_screened_nonclaim_contract |
| USB649_3 | 10 | 2.100000e-19 | 2.932961e-09 | \|dchi_X/dN\| <= 2.933e-09 for \|kappa_alpha\|=10 | ultra_screened_nonclaim_contract |

## Branch Policy

| policy_id | rule | reason | status |
| --- | --- | --- | --- |
| BP649_0_no_silence_claim | Do not use tau_clock=0 unless all local silence clauses are parent-signed. | otherwise clocks are evaded by assumption | active |
| BP649_1_product_not_standalone | Clock rows constrain kappa_alpha*tau_clock, not kappa_alpha alone. | tau dynamics are not derived | active |
| BP649_2_ultra_screened_fallback | If silence is not proved, finite alpha branch must carry explicit ultra-screening prior from Yb clocks. | order-one kappa requires \|dchi_X/dN\| <= 2.93e-8 H0-normalized | selected_fallback |
| BP649_3_cross_arena_warning | Ultra-screening must later be checked against WEP/R10/EM spectra, not only clocks. | clock-only survival may fail in other local arenas | next_contract |

## Decision Gates

| gate_id | gate | result | consequence |
| --- | --- | --- | --- |
| DG649_0_conditional_theorem_written | conditional local chi_X silence theorem exists | pass_template | future parent action has exact clauses to prove |
| DG649_1_parent_signed_silence | parent signs all local silence clauses | fail | tau_clock=0 cannot be used as active evidence |
| DG649_2_ultra_screened_branch | ultra-screened finite branch is formalized | pass_nonclaim | finite alpha branch survives only with explicit clock-screening prior |
| DG649_3_public_claim | clock/local pass claim allowed | fail_policy | no public clock or local claim |

## Next Contract

| contract_id | work_item | acceptance_condition |
| --- | --- | --- |
| NC649_0 | Carry the ultra-screened alpha branch into WEP/R10/EM spectra cross-arena consistency. | same screening variable and branch policy used across arenas; no clock-only special pleading |
| NC649_1 | Try to identify a physical screening mechanism for \|dchi_X/dN\| << 1 in lab domains. | mechanism derives from parent domain/classifier/coframe, not a fitted small number |
| NC649_2 | Keep local silence theorem as dormant proof target with explicit clauses. | future promotion must close all six LCS649 clauses |

## Decision

| decision_id | route | decision | why | next_target |
| --- | --- | --- | --- | --- |
| D649_0 | local_chiX_silence | conditional_theorem_written_not_selected_as_claim | strict coframe and closed/gapped routes are still parent-unsigned | 650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md |
| D649_1 | ultra_screened_alpha_branch | selected_nonclaim_fallback | clock data require explicit ultra-screening unless local silence is proved | 650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V649_0_source_paths_exist | pass | all cited local source paths exist |
| V649_1_prior_648_validation_clean | pass | 648 validation remains clean |
| V649_2_conditional_theorem_written | pass | conditional local silence theorem is written |
| V649_3_silence_clauses_unsigned | pass | silence clauses remain unsigned |
| V649_4_no_clause_claim | pass | silence clauses are nonclaim |
| V649_5_ultra_screen_kappa_one | pass | order-one kappa requires dchi/dN below 3e-8 |
| V649_6_branch_rows_nonclaim | pass | ultra-screened branch rows are nonclaim |
| V649_7_policy_has_no_special_pleading | pass | cross-arena warning policy is present |
| V649_8_gate_blocks_public_claim | pass | public claim gate is blocked |
| V649_9_next_contract_points_to_650 | pass | next contract points to 650 |
| V649_10_decisions_nonclaim | pass | decision rows are nonclaim |
| V649_11_summary_nonclaim | pass | summary blocks silence claim and selects nonclaim fallback |
| V649_12_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is a clean survival route, not a win: MTS must either prove local silence or accept ultra-screening as part of the finite alpha branch.
- The good news is the needed theorem is now explicit; the bad news is the clock bound leaves almost no room for unscreened local drift.
- The next fair test is cross-arena consistency: the same screening rule must not be invented only to dodge clocks.

## Nonclaim Summary

| status | conditional_silence_theorem_written | local_chiX_silence_claim | ultra_screened_branch_selected | order_one_kappa_requires_dchi_dN_below | standalone_clock_pass | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_local_chiX_silence_conditional_not_parent_signed_ultra_screened_alpha_branch_formalized_nonclaim | true | false | true_nonclaim | 2.933e-08 | false | parent domain classifier plus strict local coframe plus no-alpha-vertex clauses are unsigned | 650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md |
