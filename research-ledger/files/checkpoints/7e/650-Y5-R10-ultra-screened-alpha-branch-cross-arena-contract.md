# 650 Y5/R10 Ultra-Screened Alpha Branch Cross-Arena Contract

## Verdict

- Status: `Y5_R10_ultra_screened_alpha_branch_cross_arena_contract_formalized_nonclaim`
- Claim ceiling: `cross_arena_screening_contract_only_no_clock_WEP_R10_EM_or_PPN_claim`
- The finite-alpha branch survives only if the same local screening variable is used across clocks, WEP, R10, and local EM.
- This forbids a clock-only escape hatch: if `S_lab_alpha` is tiny for clocks, it must be tiny for every local alpha-sensitive arena unless the parent action derives a domain-specific exception.
- For `|kappa_alpha|=1`, the imported Yb clock product bound requires `S_lab_alpha <= 2.933e-08`.
- PPN/local-GR reduction is not solved by alpha screening and remains a separate derivation target.

## Source Register

| source_id | label | path | exists | role |
| --- | --- | --- | --- | --- |
| S650_0 | checkpoint_649_doc | 649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md | true | prior local silence / ultra-screen fork |
| S650_1 | validation_649 | source-intake/mts_residuals/P8_Y5_BRR545_649_VALIDATION.csv | true | prior validation |
| S650_2 | ultra_screen_branch_649 | source-intake/mts_residuals/P8_Y5_R10_649_ULTRA_SCREENED_ALPHA_BRANCH.csv | true | screening pressure imported from Yb clock product bound |
| S650_3 | branch_policy_649 | source-intake/mts_residuals/P8_Y5_R10_649_BRANCH_POLICY.csv | true | no clock-only special pleading warning |
| S650_4 | silence_clause_audit_649 | source-intake/mts_residuals/P8_Y5_R10_649_SILENCE_CLAUSE_AUDIT.csv | true | unsigned local silence clauses |
| S650_5 | cross_arena_matrix_641 | source-intake/mts_residuals/P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv | true | prior alpha reaction matrix |
| S650_6 | bound_input_ledger_645 | source-intake/mts_residuals/P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv | true | local arena bound input ledger |
| S650_7 | local_bound_matrix_639 | source-intake/mts_residuals/P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv | true | WEP/R10/PPN/Gdot local bound matrix |
| S650_8 | clock_alpha_source_646 | source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv | true | source-backed clock alpha sensitivities |
| S650_9 | clock_product_bound_647 | source-intake/mts_residuals/P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv | true | clock product bound owner |
| S650_10 | generator_script_650 | scripts/Y5_R10_ultra_screened_alpha_branch_cross_arena_contract.py | true | this checkpoint generator |

## Ultra-Screened Rule

| rule_id | screen_variable | source_bound_owner | formula | scope | status |
| --- | --- | --- | --- | --- | --- |
| USR650_0_shared_screen_variable | S_lab_alpha = \|dchi_X/dN\|_lab | Yb+ E3/E2 clock product row via 649 USB649_2 | \|kappa_alpha\| * S_lab_alpha <= 2.933e-08 | all local alpha-sensitive arenas unless a parent-signed local silence theorem replaces it | cross_arena_contract_nonclaim |
| USR650_1_no_clock_only_screen | S_lab_alpha | branch policy BP649_3 | same S_lab_alpha must be used in clocks, WEP, R10, and local EM projections | forbids hiding alpha drift only in clock experiments | no_special_pleading_gate |
| USR650_2_domain_classifier_required | D_parent(domain) | silence clause LCS649_0 | lab/bound screening and FLRW/galaxy unscreened behaviour require a parent-derived domain classifier | prevents post-hoc lab-versus-cosmology toggles | missing_parent_derivation |

## Cross-Arena Contract

| arena_id | arena | bound_owner | shared_screen_variable | required_projection | current_status | score_ready |
| --- | --- | --- | --- | --- | --- | --- |
| R2_clocks | atomic clocks and alpha drift | Yb+ E3/E2 product bound | S_lab_alpha | delta_nu_ab/nu_ab = (K_a_alpha-K_b_alpha) kappa_alpha H0 S_lab_alpha | bounded_product_not_standalone_pass | false |
| R0_R1_WEP | MICROSCOPE/Eotvos composition dependence | eta_AB <= 2.8e-15 ledger row | S_lab_alpha | eta_AB = beta_source tau_WEP sum_i[(S_Ai-S_Bi) kappa_i], with alpha channel tied to S_lab_alpha if it survives locally | projection_missing_blocks_score | false |
| R10_short_range | short-range fifth force / alpha(lambda) | R10 bound ledger / alpha(lambda) source slot | S_lab_alpha | alpha_R10(lambda)=tau_R10(lambda) beta_source beta_test c_eff(lambda), with any alpha-channel piece using the same lab screen | prediction_missing_blocks_score | false |
| EM_spectra | local and astrophysical EM spectra | source slot from 645, not yet filled | S_lab_alpha plus parent domain classifier | delta_alpha/alpha = kappa_alpha Delta chi_X, with lab Delta chi_X obeying S_lab_alpha and nonlocal rows requiring D_parent(domain) | source_and_domain_missing_blocks_score | false |
| PPN_Gdot_orbital | PPN, Gdot, orbital residuals | 639 local bound matrix | not_sufficient_by_itself | metric/coframe/source-normalization operators must reduce to GR independently of the alpha screen | separate_GR_reduction_still_required | false |

## Projection Requirements

| requirement_id | arena_id | needed_input | missing_piece | acceptance_condition | status |
| --- | --- | --- | --- | --- | --- |
| PR650_0_clocks | R2_clocks | source-backed K_alpha pair and tau_clock_time = H0 S_lab_alpha | parent derivation of S_lab_alpha or local silence | either prove tau_clock=0 from parent clauses or keep \|kappa_alpha*S_lab_alpha\| <= 2.933e-08 | numeric_product_only |
| PR650_1_WEP | R0_R1_WEP | Delta composition sensitivities, source normalization beta_source, tau_WEP, and material map | alpha-dependent body sensitivities and parent source normalization | WEP prediction uses same S_lab_alpha and does not invent a new arena-specific screen | blocked_missing_projection |
| PR650_2_R10 | R10_short_range | alpha(lambda) curve, tau_R10(lambda), beta_source, beta_test, Z_eff, and c_eff(lambda) | numeric parent prediction and full sourced bound curve | R10 prediction obeys same lab screening if it contains the alpha channel | blocked_missing_projection |
| PR650_3_EM_spectra | EM_spectra | chosen spectra dataset, alpha sensitivity coefficients, Delta chi_X map, and domain labels | source-backed EM spectra rows plus parent domain classifier | local spectra share S_lab_alpha; nonlocal spectra use a pre-declared D_parent(domain) | blocked_missing_source_and_domain |
| PR650_4_PPN | PPN_Gdot_orbital | metric-sector operator coefficients, coframe descent, source normalization, and observed-G map | derived GR/local PPN branch | metric residuals are separately suppressed or derived; alpha screening alone is not accepted | blocked_separate_GR_reduction |

## No-Special-Pleading Gates

| gate_id | gate | result | consequence |
| --- | --- | --- | --- |
| NG650_0_same_screen_variable | same S_lab_alpha is used in clocks, WEP, R10, and local EM | pass_contract_written | future rows that use arena-specific alpha screens fail validation |
| NG650_1_no_clock_only_silence | clock-only silence or screen is forbidden | pass_policy | the branch must survive cross-arena, not just clocks |
| NG650_2_parent_domain_classifier | lab/bound versus FLRW/galaxy domain classifier is parent-derived before fitting data | fail_missing | screened lab plus unscreened cosmology remains a contract, not a claim |
| NG650_3_WEP_R10_EM_projection | WEP, R10, and EM spectra have numeric projections using the shared screen | fail_missing | no local-alpha evidence score is allowed |
| NG650_4_PPN_not_fixed_by_alpha | metric/PPN residuals are not repaired by alpha screening alone | pass_blocker | local GR reduction stays a separate derivation target |
| NG650_5_public_claim | public local alpha or local GR pass claim | fail_policy | private robustness contract only |

## Decision

| decision_id | route | decision | why | next_target |
| --- | --- | --- | --- | --- |
| D650_0 | ultra_screened_alpha_branch | retained_as_cross_arena_contract_only | it is the only finite-alpha survival path after clocks, but it must now face WEP/R10/EM with the same screen | 651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md |
| D650_1 | local_chiX_silence_theorem | kept_dormant_not_claimed | six local silence clauses are still parent-unsigned | 651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md |
| D650_2 | next_arena | select_WEP_stress_test_first | WEP is the next hardest local alpha-sensitive arena with a strong numeric bound and no range-curve ambiguity | 651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md |

## Next Contract

| contract_id | work_item | acceptance_condition |
| --- | --- | --- |
| NC650_0 | Fill WEP alpha-sensitivity/source-normalization rows or prove the shared screen kills the WEP alpha channel. | eta_AB row uses S_lab_alpha and source-backed material sensitivities; otherwise remains blocked |
| NC650_1 | Reject any arena-specific screening factor not derived from the parent domain classifier. | future runner fails rows with S_clock != S_WEP != S_R10 != S_EM unless parent-sourced |
| NC650_2 | Keep PPN/local GR reduction separate from alpha screening. | metric/coframe residuals require their own zero or bound proof |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V650_0_source_paths_exist | pass | all cited local source paths exist |
| V650_1_prior_649_validation_clean | pass | 649 validation remains clean |
| V650_2_kappa_one_screen_imported | pass | kappa=1 screen imported from 649 and remains below 3e-8 |
| V650_3_shared_screen_defined | pass | shared lab alpha screen is explicit |
| V650_4_required_arenas_covered | pass | clock, WEP, R10, EM, and PPN/orbital arenas are covered |
| V650_5_contract_rows_nonclaim | pass | all cross-arena rows remain nonclaim and unscored |
| V650_6_projection_blocks_present | pass | missing WEP/R10/EM/PPN projections are explicit blockers |
| V650_7_no_special_pleading_gates_present | pass | no-special-pleading gates are present |
| V650_8_domain_classifier_still_missing | pass | parent domain classifier remains missing |
| V650_9_public_claim_blocked | pass | public claim gate is blocked |
| V650_10_decisions_nonclaim | pass | decision rows are nonclaim |
| V650_11_next_target_WEP | pass | next target selects WEP screening stress test |
| V650_12_summary_blocks_claim | pass | summary blocks clock-only escape and WEP claim |
| V650_13_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is the right ruthless move: the alpha branch is allowed to live, but it must fight the whole local-card table, not just clocks.
- The best next punch is WEP because it is local, numerically sharp, and does not need an R10 range-curve digitization before it can hurt us.
- If WEP also accepts the same screen without special pleading, the branch looks disciplined; if it needs a different screen, the finite-alpha route likely collapses back to a closure-only theorem.

## Nonclaim Summary

| status | same_screen_variable_required | screen_variable | kappa_one_screen_bound | clock_only_escape_allowed | WEP_ready | R10_ready | EM_spectra_ready | PPN_local_GR_ready | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_ultra_screened_alpha_branch_cross_arena_contract_formalized_nonclaim | true | S_lab_alpha=\|dchi_X/dN\|_lab | 2.933e-08 | false | false | false | false | false | parent domain classifier plus WEP/R10/EM projection coefficients are missing | 651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md |
