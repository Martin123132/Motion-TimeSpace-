# 846 - Y5 R10 Strict Cosmology Branch Dry-Run Spec

Current result: **the strict cosmology branch now has a dry-run specification, but it is not ready for scoring**. Execution is blocked until `847` supplies a candidate file or a parent amplitude law/range with numeric `b_mem`, shape source, and parameter-penalty fields. No long fit is authorized here.

## Non-Claim Summary

| status | claim_ceiling | what_changed | what_blocks_execution | what_is_not_claimed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_846_strict_cosmology_dry_run_spec_ready_nonclaim | dry_run_spec_only_no_fit_no_support_claim | future strict cosmology run now has dry-run input, candidate, baseline, output, and command schemas | missing 847 candidate file or parent amplitude law/range | new score, model support, branch death, local-GR progress, candidate execution readiness | 847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md | false |

## Dry-Run Inputs

| input_id | input_type | path | required_for | exists_now | execution_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| IN846_0_contract | contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\846-Y5-R10-strict-cosmology-branch-dry-run-spec.md | dry-run interpretation | false | generated_by_this_checkpoint | false |
| IN846_1_candidate_file | candidate_branch_file | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv | actual dry-run execution | false | blocked_until_847_candidate_file_or_parent_amplitude_law | false |
| IN846_2_SN_BAO_script | script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\cosmology_likelihood_smoke.py | SN/BAO baseline parity | true | available_reference_do_not_modify | false |
| IN846_3_Hz_script | script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\Hz_covariance_likelihood_smoke.py | H(z) guardrail | true | available_reference_do_not_modify | false |
| IN846_4_growth_CMB_script | script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\joint_growth_CMB_radflat_readout.py | growth/CMB guardrail | true | available_reference_do_not_modify | false |

## Candidate Branch Schema

| field | required | allowed_values_or_rule | example | blocks_execution_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| candidate_id | true | unique stable identifier | S2_corridor_mid | true | false |
| branch_class | true | C0_benchmark\|parent_predicted\|predeclared_corridor\|null_control | predeclared_corridor | true | false |
| b_mem_mode | true | fixed_parent\|fixed_predeclared\|corridor_predeclared\|zero_control\|benchmark_display_only | corridor_predeclared | true | false |
| b_mem_value_or_range | true | numeric fixed value or closed numeric range declared before scoring; no MISSING placeholders | [0.03,0.12] | true | false |
| shape_source | true | parent/equality-scale derivation path or predeclared benchmark source | 178_parent_corridor | true | false |
| parameter_count_delta | true | integer penalty relative to baseline, including amplitude/shape freedom | 1 | true | false |
| claim_label | true | benchmark_only\|exploratory_nonclaim\|support_grade_candidate_blocked | exploratory_nonclaim | true | false |

## Baseline Symmetry Matrix

| arena | required_baselines | required_MTS_branches | symmetry_rule | pass_output | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SN_BAO_background | LambdaCDM,wCDM,CPL | null_control,C0_benchmark,predeclared_corridor,parent_predicted_if_available | same nuisance offsets, covariance choice, calibration freedom, and AIC/BIC parameter counting | delta_chi2_delta_AIC_delta_BIC_residuals_edge_flags | false |
| Hz_chronometer | M0_or_LambdaCDM,wCDM_if_available | same candidate set as SN_BAO where formula is defined | same diagonal/covariance branch and same redshift windows | delta_chi2_covariance_verdict_windowed_verdict | false |
| growth_CMB_radflat | LCDM_radflat,wCDM_or_best_available_growth_baseline | C0_benchmark,predeclared_corridor,parent_predicted_if_available | same sigma8_0 refit rule and same compressed CMB distance-prior treatment | growth_chi2_CMB_chi2_joint_AIC_BIC_parameter_penalties | false |

## Output Schema

| output_file | purpose | required_fields | created_by_846 | valid_for_claim |
| --- | --- | --- | --- | --- |
| runs/<timestamp>/log.txt | human-readable dry-run or future execution log | start time, command, dry_run_only flag, source hashes/paths, warnings | false | false |
| runs/<timestamp>/status.json | machine-readable status for VS Code/phone handoff | status, dry_run_only, candidate_file, all_inputs_present, claim_allowed=false | false | false |
| runs/<timestamp>/STRICT_BRANCH_SCORECARD.csv | future score table across candidates and baselines | arena,candidate,baseline,chi2,AIC,BIC,delta_AIC,delta_BIC,edge_flag,claim_label | false | false |
| runs/<timestamp>/COMPLETE.marker | completion marker for long-run workflow | plain marker only after dry-run/execution completes | false | false |

## Dry-Run Commands

| command_id | command | mode | dry_run_only | long_fit_allowed | requires_847 | expected_runtime | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CMD846_0_schema_only | python post-checkpoint-work\scripts\Y5_R10_strict_cosmology_branch_dry_run_spec.py | schema_generation_only | true | false | false | seconds | false |
| CMD846_1_future_input_check | python post-checkpoint-work\scripts\strict_cosmology_branch_runner.py --candidates source-intake\mts_residuals\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv --dry-run --no-fit | future_candidate_input_check | true | false | true | seconds_to_minutes | false |
| CMD846_2_future_scoring_run | python post-checkpoint-work\scripts\strict_cosmology_branch_runner.py --candidates source-intake\mts_residuals\P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv --run-score --write-run-dir | future_explicit_execution_only | false | only_after_user_go_ahead | true | unknown_may_be_long | false |

## Claim Guard

| guard_id | claim | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG846_0_no_fit | 846 runs or scores cosmology models | forbidden | 846 is only a dry-run specification and schema checkpoint | false |
| CG846_1_no_candidate_ready | strict branch is ready for execution now | forbidden | candidate file and parent amplitude law/range are deferred to 847 | false |
| CG846_2_no_support | dry-run setup permits support language | forbidden | all dry-run outputs must keep claim_allowed=false until data and parent-amplitude gates pass | false |
| CG846_3_allowed_spec | future strict cosmology run now has an input/output dry-run specification | allowed_private_nonclaim | this is an execution discipline artifact, not evidence | false |

## Decision

| decision_id | finding | reason | status | claim_allowed | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| D846_0 | dry-run spec is ready | candidate schema, baseline matrix, output schema, and command modes are defined | dry_run_spec_only_no_fit_no_support_claim | false | 847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md | false |
| D846_1 | actual execution remains blocked | 847 must provide a candidate file or parent amplitude law before any strict branch input check | dry_run_spec_only_no_fit_no_support_claim | false | 847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md | false |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md | create the strict candidate file or derive/fix the parent amplitude law before any scoring run | candidate rows, numeric b_mem fixed/range values, shape source, parameter penalties, claim labels, execution eligibility | long fit, support claim, death claim, local-GR claim, formalization-workbench edits | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 845_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\845-Y5-R10-strict-MTS-cosmology-branch-contract.md | true | pass | strict branch contract handoff | false |
| 845_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_845_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| cosmology_likelihood_smoke_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\cosmology_likelihood_smoke.py | true | pass | existing SN/BAO cosmology likelihood machinery | false |
| Hz_covariance_likelihood_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\Hz_covariance_likelihood_smoke.py | true | pass | existing H(z) covariance smoke machinery | false |
| full_joint_radflat_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\full_joint_radflat_phenomenology_fit.py | true | pass | existing full joint radflat fit machinery | false |
| joint_growth_CMB_radflat_script | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\scripts\joint_growth_CMB_radflat_readout.py | true | pass | existing growth/CMB radflat readout machinery | false |
| pantheon_plus_data | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\data\cosmology\pantheon_plus\Pantheon+SH0ES.dat | true | pass | SN data availability check | false |
| desi_dr2_bao_mean | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\data\cosmology\desi_dr2_bao\desi_gaussian_bao_ALL_GCcomb_mean.txt | true | pass | BAO mean data availability check | false |
| Hz_data | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\data\cosmology\cosmic_chronometers\Hz.csv | true | pass | chronometer data availability check | false |
| growth_data | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\data\cosmology\growth_CMB\sdss_eboss_dr16\BAO-plus\sdss_DR12_LRG_FSBAO_DMDHfs8.txt | true | pass | growth/BAO-plus data availability check | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V846_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V846_1_prior_845_clean | pass | P8_Y5_BRR545_845_VALIDATION.csv clean |
| V846_2_reference_inputs_exist | pass | referenced formalization scripts/data exist |
| V846_3_candidate_schema_blocks_missing_values | pass | candidate schema requires predeclared numeric amplitude/source/penalty fields |
| V846_4_baseline_matrix_complete | pass | SN/BAO, H(z), and growth/CMB arenas included |
| V846_5_output_schema_complete | pass | log, status, scorecard, and completion marker schemas included |
| V846_6_no_long_run_authorized | pass | future scoring is blocked until 847 and long run requires explicit go-ahead |
| V846_7_no_claims | pass | candidate readiness and support claims forbidden |
| V846_8_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V846_9_next_target_selected | pass | 847-Y5-R10-strict-cosmology-candidate-file-or-parent-amplitude-law.md |
| V846_10_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V846_11_validation_rows_ready | pass | validation table constructed |
