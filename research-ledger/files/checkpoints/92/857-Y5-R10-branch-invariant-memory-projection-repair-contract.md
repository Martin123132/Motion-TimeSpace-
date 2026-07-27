# 857 - Y5 R10 Branch-Invariant Memory Projection Repair Contract

Current result: **the branch split is now fenced behind a parent-plus-response contract**. The allowed cosmology object is not a free branch-specific `b_mem`; it is a branch-invariant parent memory channel plus an optional response channel that is forced to zero unless independently sourced before scoring.

## Non-Claim Summary

| status | claim_ceiling | what_changed | selected_route | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_857_branch_invariant_projection_contract_written_nonclaim | contract_only_no_scored_repair_no_response_source_no_support_claim | converted the branch split into a strict parent-plus-response contract | parent_only_shared_memory_stress_test | support, repaired fit, response physics, local-GR pass, public evidence | 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md | false |

## Projection Contract

| contract_id | clause | mathematical_form | acceptance_gate | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BIP857_0_two_channel_identity | replace branch-specific b_mem readout with parent plus optional response | E2_B(z)=E2_LCDM_B(z)+b_P A_P(z)+b_R[B] A_R_B(z) | b_P is branch-invariant; b_R[B] is zero unless sourced before scoring | contract_written_not_scored | false |
| BIP857_1_parent_invariance | parent memory channel must not know which calibration branch was used | partial_B b_P = 0 and partial_B A_P(z)=0 | same b_P and same A_P are used for no_SH0ES and SH0ES branches | required_for_858 | false |
| BIP857_2_response_zero_limit | response channel must vanish in the absence of an independent local/calibration source | q_B=0 or MISSING_SOURCE => b_R[B]=0 | branch split in b_eff disappears when q_B is absent | required_for_858 | false |
| BIP857_3_no_target_inversion | do not infer b_R[B] by subtracting the fitted branch target from the parent amplitude | b_R[B] != b_eff_fit[B]-b_P unless q_B and C_R are independently signed first | target-derived response rows remain invalid for claim | guard_written | false |
| BIP857_4_gr_limit | cosmology repair must retain the standard zero-memory baseline limit | b_P=0 and b_R[B]=0 => E2_B(z)=E2_LCDM_B(z) | null-control parity remains exact before any MTS preference is discussed | required_for_858 | false |

## Channel Decomposition

| channel_id | object | meaning | allowed_source | forbidden_source | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CH857_0_parent_memory | b_P A_P(z) | branch-invariant parent memory deformation of the expansion history | parent derivation or shared-amplitude stress test only | separate SH0ES/no-SH0ES fitted b_mem values | candidate_channel_not_claimed | false |
| CH857_1_response_projection | b_R[B] A_R_B(z) | optional branch/local response projection | independent q_B and response coefficient C_R signed before scoring | using required response magnitude solved from target split | set_to_zero_until_sourced | false |
| CH857_2_effective_readout | b_eff[B]=b_P+b_R[B] | diagnostic readout after parent and response terms are specified | computed from contract terms | primitive independent fitted parameter per branch | diagnostic_only | false |
| CH857_3_calibration_offset | Delta M_B or nuisance offset | SN calibration/marginalization mode | likelihood nuisance accounting | promoting a projected-out offset into a physical field amplitude | not_a_parent_memory_source | false |

## Branch Split Response Ledger

| ledger_id | b_parent_choice | required_b_response_no_sh0es | required_b_response_sh0es | diagnosis | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BS857_0_no_sh0es_anchor | 0.0157305087947 | 0 | 0.0967220815343 | matches low-pressure branch but needs unsourced SH0ES response | blocked_without_independent_q_B | false |
| BS857_1_midpoint_parent | 0.0640915495618 | -0.0483610407671 | 0.0483610407672 | symmetrizes branch pressure but both responses are target-derived | blocked_without_independent_q_B | false |
| BS857_2_sh0es_anchor | 0.112452590329 | -0.0967220815343 | 0 | matches local-H0-pressure branch but needs unsourced no-SH0ES response | blocked_without_independent_q_B | false |
| BS857_3_response_zero_default | single_shared_b_parent_to_be_stress_tested | 0 | 0 | only route that does not smuggle a branch response into the model | selected_for_858_parent_only_stress_test | false |

## Response Source Gate

| gate_id | requirement | failure_mode | action_if_failed | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RG857_0_independent_q_B | q_B must be measured, derived, or otherwise signed independently of the fitted target split | MISSING_INDEPENDENT_SOURCE or solved-from-target amplitude | set b_R[B]=0 | failed_currently | false |
| RG857_1_response_coefficient | C_R must come from a parent projection, local geometry, or stated likelihood-response map | free coefficient tuned to match SH0ES/no-SH0ES split | response channel remains closure-only | missing_currently | false |
| RG857_2_projected_offset_rejection | global SN calibration offset cannot source b_R after nuisance projection removes it | using MU_SH0ES minus m_b_corr as physical memory amplitude | reject as source | passed_rejection | false |
| RG857_3_response_pre_registration | response vector and amplitude must be recorded before any scoring run that uses them | post-hoc response chosen after seeing BIC | score as exploratory nonclaim only | required_next | false |

## BAO And Conservation Guard

| guard_id | guard | mathematical_check | status | valid_for_claim |
| --- | --- | --- | --- | --- |
| BCG857_0_bao_residual_split | SN improvement and BAO penalty must be reported separately | Delta chi2_total = Delta chi2_SN + Delta chi2_BAO + Delta chi2_priors | required_for_858 | false |
| BCG857_1_no_hidden_bao_breakage | response or parent memory cannot be preferred if it wins SN by silently breaking BAO | BAO residual table and max-pull ledger are mandatory | required_for_858 | false |
| BCG857_2_conservation_branch | if the response is physical, the parent action must conserve the combined stress-energy | nabla_mu(T_parent^{mu nu}+T_response^{mu nu})=0 | unsigned_so_response_not_physical_claim | false |
| BCG857_3_likelihood_projection_branch | if response is merely observational projection, it cannot be advertised as field-theory dynamics | response rows labelled likelihood_level_only | required_if_response_reintroduced | false |

## Acceptance Tests

| test_id | test | pass_condition | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| AT857_0_shared_parent | same b_P and A_P used in no_SH0ES and SH0ES branches | no branch-specific b_mem parameter appears in the scored model | ready_for_858 | false |
| AT857_1_response_zero_default | without independent q_B, b_R[B] is forced to zero | all response rows are zero or explicitly invalid for claim | ready_for_858 | false |
| AT857_2_null_control | b_P=0 reproduces fitted baseline/null-control parity | MTS null row tracks baseline within numerical tolerance | required_for_858 | false |
| AT857_3_SN_BAO_split | parent-only memory score reports SN and BAO deltas separately | no total BIC statement without sector ledger | required_for_858 | false |
| AT857_4_parent_survival | shared parent amplitude remains competitive when response is zero | 858 determines whether signal survives without branch-specific amplitude | deferred_to_858 | false |

## Route Choice

| route_id | route | status | reason | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| RC857_0_selected | branch_invariant_parent_only_memory_stress_test | selected | the response source is not signed, so the honest next test is b_R=0 with one shared parent amplitude | shared b_P, b_R=0, null control, SN/BAO split, no branch b_mem fitting | target-derived response amplitude, support claim, public evidence | false |
| RC857_1_deferred | independent_response_source_reintroduction | deferred | can reopen only if q_B and C_R are sourced before scoring | pre-registered response vector and conservation/likelihood label | post-hoc split matching | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG857_0_no_repaired_score | the memory projection has passed a repaired fit | forbidden | 857 writes the contract only; no repaired model has been scored | false |
| CG857_1_no_response_physics | branch response is physical field dynamics | forbidden | q_B, C_R, and conservation accounting are unsigned | false |
| CG857_2_no_branch_knob | separate branch b_mem values are acceptable evidence | forbidden | separate b_eff values are diagnostic targets, not primitive parameters | false |
| CG857_3_allowed_contract | a private nonclaim contract now blocks branch-specific memory smuggling | allowed_private_nonclaim | the next scoring target is forced into a stricter parent-only test | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D857_0 | branch-invariant memory projection contract is now explicit | b_eff is demoted to diagnostic readout unless it decomposes into b_P plus sourced response | contract_only_no_scored_repair_no_response_source_no_support_claim | false | 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md | false |
| D857_1 | response channel is set to zero until independently sourced | 856 showed the available calibration/local-response candidates fail or are unsourced | contract_only_no_scored_repair_no_response_source_no_support_claim | false | 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md | false |
| D857_2 | next fair test is parent-only shared-amplitude stress | if the lead survives without branch amplitude freedom, the MTS cosmology route becomes much cleaner | contract_only_no_scored_repair_no_response_source_no_support_claim | false | 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md | score the strict parent-only memory model with one shared b_P and b_R=0 | null parity, no_SH0ES and SH0ES branches, SN/BAO sector deltas, BIC/AIC, no branch-specific b_mem | response amplitude, target inversion, public claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 856_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md | true | pass | selected repair route | false |
| 856_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_856_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| 856_repair_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_856_MEMORY_PROJECTION_REPAIR_CONTRACT.csv | true | pass | unimplemented repair clauses | false |
| 856_branch_targets | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_856_BRANCH_TARGET_CONSTRAINTS.csv | true | pass | branch effective-amplitude targets | false |
| 856_source_test | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_856_INDEPENDENT_RESPONSE_SOURCE_TEST.csv | true | pass | failed independent response source test | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V857_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V857_1_prior_856_clean | pass | P8_Y5_BRR545_856_VALIDATION.csv clean |
| V857_2_projection_contract_has_parent_and_response | pass | contract contains b_P parent channel and zero-response limit |
| V857_3_effective_bmem_demoted_to_diagnostic | pass | b_eff is not a primitive branch parameter |
| V857_4_branch_split_not_claimed | pass | target-derived responses remain blocked and response-zero route selected |
| V857_5_response_gate_sets_missing_source_to_zero | pass | missing independent q_B forces b_R=0 |
| V857_6_bao_and_conservation_guards_present | pass | BAO split and conservation guards recorded |
| V857_7_acceptance_tests_ready | pass | strict 858 acceptance tests recorded |
| V857_8_route_selected | pass | parent-only shared-memory stress test selected |
| V857_9_claim_allowed_false | pass | decision rows keep claim_allowed=false |
| V857_10_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V857_11_next_target_selected | pass | 858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md |
| V857_12_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V857_13_validation_rows_ready | pass | validation table constructed |
