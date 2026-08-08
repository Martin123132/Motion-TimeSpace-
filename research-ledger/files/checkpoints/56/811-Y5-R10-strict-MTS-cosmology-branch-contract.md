# 811 - Y5 R10 Strict MTS Cosmology Branch Contract

Current result: **the next cosmology branch is no longer allowed to win by flexible rescue-fitting**. `C1_parent_locked_memory` is defined as a pre-data contract: C0 stays in the ring as a closure benchmark, while C1 must lock the memory shape, amplitude corridor, perturbation rules, and fair baseline scorecard before any run.

Generated UTC: `2026-06-12T17:11:56+00:00`

## Non-Claim Summary

| status | claim_ceiling | strict_branch_name | purpose | current_status | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_811_strict_MTS_cosmology_branch_contract_locked_nonclaim | strict_branch_contract_only_no_fit_no_support_claim_no_local_GR_claim | C1_parent_locked_memory | replace C0 rescue-fitting with a predeclared branch whose shape/amplitude freedoms are parent-locked or explicitly demoted | contract_locked_no_run | 812-Y5-R10-parent-locked-memory-branch-preflight.md | false |

## Strict Branch Contract

| contract_id | rule | allowed | forbidden | promotion_condition | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SC811_0_C0_benchmark_only | C0 remains a closure-only benchmark and stress-test comparator. | use C0 to measure whether stricter branches lose useful residual anatomy | using C0 near-competitiveness as MTS evidence | parent-derived amplitude and perturbation contract before a new support fit | false |
| SC811_1_C1_parent_locked_memory | The next branch is C1_parent_locked_memory: same radflat FLRW structure, but with shape and amplitude locks predeclared before data. | algebraic preflight, parameter-lock audit, dry-run manifest | broad b_mem, alpha_act, or nu_act fit after seeing SN/BAO/growth/CMB residuals | all locks sourced, finite, and not inferred from target-data best fits | false |
| SC811_2_equal_baseline_boxing_ring | LCDM, wCDM, CPL, C0, and C1 must enter the same diagnostic ring. | score near-ties as informative under honest parameter counts | MTS-only jackknife prosecution or baseline-only immunity | same splits, same covariance, same residual anatomy, same AIC/BIC bookkeeping | false |
| SC811_3_local_GR_firewall | No cosmology result can upgrade the local GR/PPN branch. | cosmology can rank parent-memory candidates | cosmology success substituting for MTS -> GR -> Newton | separate local GR theorem and PPN residual bound | false |

## Equation Spec

| equation_id | equation | lock_status | free_before_preflight | must_not_fit_freely | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EQ811_0_radflat_background | E(z)^2 = Omega_r0(1+z)^4 + Omega_m0(1+z)^3 + (1 - Omega_m0 - Omega_r0) + b_mem F(N) | structure_locked_from_radflat_branch | Omega_m0,H0,rd_like_calibration_only_if_baselines_get_equivalent_freedom | b_mem,F_shape_after_residuals | false |
| EQ811_1_memory_shape | F(N) = 1 - exp[-(N/u_s)^nu], F(0)=0, F(infinity)=1, 0<=F<=1 | shape_must_be_parent_or_predeclared | none unless explicit stress-only row | u_s,alpha_act,nu | false |
| EQ811_2_source_budget | b_mem = integral S_Gamma(N)dN = a_F DeltaR/[3 eta^2], eta=H0 L_cg/c | identity_derives_corridor_not_prediction | predeclared finite corridor only | post-hoc b_mem amplitude | false |
| EQ811_3_Bianchi_closure | w_Gamma(z) = -1 + (1+z) Omega_Gamma'(z)/(3 Omega_Gamma(z)) | required_conservation_identity | none | w_Gamma independent of Omega_Gamma | false |

## Parameter Locks

| parameter | C0_status | C1_lock | if_unlocked | valid_for_claim |
| --- | --- | --- | --- | --- |
| alpha_act | previously fitted_or_frozen_from_prior_clue | derive from equality-clock/parent threshold law or predeclare fixed value before any new data | branch becomes stress-only | false |
| nu_act | previously fitted_or_frozen_from_prior_clue | derive from hazard/source distribution or predeclare finite fixed value before any new data | branch becomes stress-only | false |
| b_mem | not_stable_between_CMB_only_and_full_joint | derive or predeclare a narrow parent corridor from eta,a_F,DeltaR before fitting | C1 collapses back to C0 closure benchmark | false |
| eta=H0 L_cg/c | corridor_only | source from parent coarse-graining scale rather than target cosmology fit | amplitude prediction absent | false |
| a_F DeltaR | corridor_only | source sign and order from trace-coupling/endpoint theorem | positive sign remains conditional and magnitude remains phenomenological | false |

## Perturbation Requirements

| requirement | minimum_contract | why | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- |
| effective_sound_speed | declare c_s^2 or smooth-limit rule before growth/CMB scoring | growth cannot be interpreted if memory clustering is arbitrary | background-only phenomenology | false |
| anisotropic_stress | declare pi_Gamma=0, bounded, or parent-derived nonzero form | CMB lensing/slip constraints depend on stress | compressed-CMB-only internal check | false |
| matter_coupling | declare conserved separate fluid or exchange current with sourced coupling | growth response changes if matter is exchanging energy/momentum | no physical growth claim | false |
| early_time_limit | prove memory fraction is negligible or CMB-compatible before recombination-sensitive claims | CMB cannot be trusted if early-time sector floats | no CMB support language | false |
| growth_sign_prediction | predeclare whether C1 raises/lowers f sigma8 or distances in target redshift windows | prevents after-the-fact residual storytelling | no holdout upgrade | false |

## Baseline Parity Gate

| gate_id | rule | pass_condition | fail_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| BG811_0_model_set | Fit/report LCDM, wCDM, CPL, C0_frozen_benchmark, and C1_parent_locked_memory together. | all usable or explicitly failed with same optimizer diagnostics | MTS-only diagnostics or missing flexible baselines | false |
| BG811_1_split_set | Report SH0ES and no-SH0ES separately; never merge them into one support sentence. | local-H0 pressure cannot carry the evidence label | claim depends on local-H0 branch alone | false |
| BG811_2_residual_anatomy | Report SN, BAO quantity, H(z), growth, CMB distance-prior components separately. | gain/loss anatomy is visible | single aggregate chi2 hides where the model wins or loses | false |
| BG811_3_parameter_count | Count every fitted calibration, shape, amplitude, and nuisance freedom consistently across branches. | AIC/BIC are honest enough to score a boxing-round decision | C1 gets free hidden knobs | false |

## Acceptance Scorecard

| band | criterion | interpretation | allowed_language | forbidden_language | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| competitive_round | Delta AIC <= 2 or Delta BIC <= 2 against best fair baseline with no edge flags | interesting near-tie or light win, not proof | competitive under this diagnostic | confirmed or preferred as fundamental physics | false |
| weak_loss_but_alive | 2 < Delta BIC <= 6 with stable parameters and useful residual anatomy | not dead, route needs derivation or sharper data split | survives as constraint clue | evidence pillar | false |
| strong_penalty | Delta BIC > 6 or repeated residual failure under fair baselines | branch should be demoted or replaced | failed this gate | pipeline issue unless baselines fail the same diagnostic | false |
| automatic_nonclaim | prior edge, post-hoc parameter unlock, missing parent source, missing perturbation contract, or local-GR overclaim | development clue only | stress result | support claim | false |

## Demotion Rules

| rule_id | trigger | result | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DR811_0_C1_to_C0 | b_mem, alpha_act, or nu_act must be fit broadly to survive | demote C1 back to C0 closure benchmark | return to parent amplitude/shape derivation | false |
| DR811_1_background_only | perturbation contract cannot be stated without arbitrary knobs | cosmology remains background-only phenomenology | do not run growth/CMB support claims | false |
| DR811_2_data_mismatch | C1 fails fair baselines by strong-penalty band with no shared baseline failure | replace branch rather than rescue-fit | derive a different memory source or abandon this cosmology route | false |
| DR811_3_local_firewall | any readout tries to promote local GR/PPN from cosmology | invalidate claim language | return to MTS -> GR -> Newton derivation | false |

## Next Decision

| decision_id | decision | reason | next_target | run_now | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ND811_0_no_data_run | no data run from 811 | the strict branch contract must be locked before code touches data | 812-Y5-R10-parent-locked-memory-branch-preflight.md | false | false |
| ND811_1_preflight_next | build parent-locked memory branch preflight | C1 needs a machine-checkable parameter-lock manifest before empirical testing | 812-Y5-R10-parent-locked-memory-branch-preflight.md | false | false |

## Source Register

| source_id | path | exists | needle_check | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 810_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\810-Y5-R10-cosmology-evidence-readout-pack.md | true | pass | immediate readout selecting strict branch | false |
| 810_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_810_VALIDATION.csv | true | pass | prior checkpoint validation | false |
| formal_147_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\147-cosmology-evidence-readout-pack.md | true | pass | frozen SN/BAO clue and claim ceiling | false |
| formal_155_Hz | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\155-cosmology-status-after-Hz-covariance.md | true | pass | H(z) non-support and perturbation-contract route | false |
| formal_172_radflat | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\172-radiation-consistent-CMB-calibration-branch.md | true | pass | radiation-consistent flatness convention | false |
| formal_176_demotion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\176-C0-radflat-demotion-decision.md | true | pass | C0 benchmark demotion | false |
| formal_177_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\177-parent-amplitude-repair-contract.md | true | pass | no-fit parent amplitude contract | false |
| formal_178_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\178-parent-amplitude-theorem-attempt.md | true | pass | amplitude theorem attempt and strict-branch target | false |
| formal_174_bmem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\174-bmem-parent-boundary-law.md | true | pass | b_mem identity and non-prediction | false |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V811_0_sources_exist_and_needles | pass | all source paths exist and needles are present |
| V811_1_prior_810_clean | pass | P8_Y5_BRR545_810_VALIDATION.csv clean |
| V811_2_outputs_scoped | pass | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work |
| V811_3_all_rows_nonclaim | pass | all generated rows valid_for_claim=false |
| V811_4_C0_benchmark_only | pass | C0 retained only as closure benchmark |
| V811_5_parameter_locks_complete | pass | shape and amplitude locks are explicit |
| V811_6_perturbation_contract_present | pass | growth/CMB perturbation obligations present |
| V811_7_baseline_parity_present | pass | LCDM/wCDM/CPL baseline parity required |
| V811_8_no_data_run_selected | pass | contract only; no data run selected |
| V811_9_next_target_selected | pass | 812-Y5-R10-parent-locked-memory-branch-preflight.md |
| V811_10_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 |
| V811_11_validation_rows_ready | pass | validation table constructed |

## Verdict

This is the disciplined route: C0 stays useful, but it is not allowed to carry the flag. C1 only enters the data ring after the parent locks are explicit. If those locks cannot be supplied, the cosmology branch remains a constraint clue and we go back to the parent derivation rather than shopping for a fit.

## Next Target

`812-Y5-R10-parent-locked-memory-branch-preflight.md`
