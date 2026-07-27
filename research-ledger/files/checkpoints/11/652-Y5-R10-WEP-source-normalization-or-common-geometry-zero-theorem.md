# 652 Y5/R10 WEP Source Normalization or Common-Geometry Zero Theorem

## Verdict

- Status: `Y5_R10_WEP_common_geometry_zero_theorem_conditional_source_normalization_target_retained_nonclaim`
- Claim ceiling: `conditional_WEP_zero_theorem_and_beta_source_target_only_no_WEP_or_local_GR_claim`
- A clean common-geometry zero theorem can be written: if all matter sees one species-blind geometry and no local `alpha_EM(chi_X)`/mass/class-response vertex survives, the differential WEP alpha charge is zero.
- The theorem is still conditional, not parent-signed, because the current parent action has not derived the matter functor, no-alpha-vertex rule, or selector Ward identity.
- If the zero theorem fails, the source-normalization fallback must satisfy `|beta_source_alpha| <= 2.887e-05` in the stricter 651 smoke channel.
- Rescaling `kappa_alpha` is not an escape, because clocks constrain the product `|kappa_alpha*S_lab_alpha|`, and WEP uses that same product.

## Source Register

| source_id | label | path | exists | role |
| --- | --- | --- | --- | --- |
| S652_0 | checkpoint_651_doc | 651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md | true | prior WEP alpha stress test |
| S652_1 | validation_651 | source-intake/mts_residuals/P8_Y5_BRR545_651_VALIDATION.csv | true | prior validation |
| S652_2 | WEP_stress_651 | source-intake/mts_residuals/P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv | true | unit-source WEP overshoot rows |
| S652_3 | charge_estimate_651 | source-intake/mts_residuals/P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv | true | Ti/Pt composition charge smoke rows |
| S652_4 | screening_gates_651 | source-intake/mts_residuals/P8_Y5_R10_651_SCREENING_OPTION_GATES.csv | true | zero theorem versus source-normalization fork |
| S652_5 | cross_arena_contract_650 | source-intake/mts_residuals/P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv | true | same-screen cross-arena contract |
| S652_6 | screen_rule_650 | source-intake/mts_residuals/P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv | true | product-bound screen owner |
| S652_7 | WEP_species_universality_371 | 371-WEP-species-universality-or-active-eta-runner.md | true | species universality no-go |
| S652_8 | WEP_observed_coframe_373 | 373-one-observed-coframe-parent-selector-or-WEP-closure.md | true | one observed coframe closure contract |
| S652_9 | WEP_common_F_388 | 388-WEP-species-symmetry-common-F-parent-selector-attempt.md | true | species-blind geometry functor contract |
| S652_10 | generator_script_652 | scripts/Y5_R10_WEP_source_normalization_or_common_geometry_zero_theorem.py | true | this checkpoint generator |

## Common-Geometry Zero Theorem

| theorem_id | name | proof_status | parent_signed | what_it_would_close | what_it_does_not_close |
| --- | --- | --- | --- | --- | --- |
| CGZ652 | conditional common-geometry WEP alpha zero theorem | proved_as_conditional_template | false | direct MICROSCOPE Ti/Pt alpha-composition WEP channel | universal metric fifth-force/PPN/source-normalization residuals and local-GR reduction |

## Proof Clause Audit

| clause_id | needed_statement | mathematical_form | current_status | failure_if_missing |
| --- | --- | --- | --- | --- |
| CGZ652_0_single_geometry_argument | All matter species use one observed coframe ehat and connection omega[ehat]. | S_m=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A] | conditional_closure_not_parent_derived | species metrics or coframes reintroduce WEP violation |
| CGZ652_1_species_labels_internal_only | Species labels live only in ordinary internal constants/representations and not in class-sector spurions. | theta_A={m_A,q_A,spin_A,rep_A} with partial_chi_X theta_A=0 | not_parent_derived | m_A(chi_X), q_A(chi_X), or alpha_A(chi_X) gives composition charges |
| CGZ652_2_no_alpha_or_mass_vertex | No local alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-energy response is a direct matter argument. | delta S_matter/d chi_X \|_{ehat,theta_A}=0 | unsigned_and_currently_the_hard_blocker | Damour-Donoghue composition charges become physically sourced |
| CGZ652_3_representative_vertices_forbidden | Matter cannot couple to representative data B_perp, b_2, Cperp, or local representative leakage. | S_matter descends to quotient/class observables only | conditional_progress_but_not_enough_for_common_F | direct representative WEP forces return |
| CGZ652_4_selector_stress_ward_identity | Any selector enforcing ehat/common-F owns its stress in the total Ward identity. | nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0 | open | zero theorem hides an unconserved selector force |
| CGZ652_5_local_domain_classifier | The local lab/source domain is selected before data and shares the 650 screen contract. | D_parent(local source/test bodies) fixed before fitting eta_AB | not_parent_derived | WEP-specific screening becomes post-hoc special pleading |

## Source-Normalization Target

| target_id | channel | eta_bound | clock_product_bound_used | delta_Q_abs | required_abs_beta_source_max | kappa_rescaling_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BST652_0_alpha_Coulomb | alpha/Coulomb composition charge | 2.800000e-15 | 2.932961e-08 | 1.989808886825e-03 | 4.797780522732e-05 | independent_of_kappa_if_clock_product_bound_is_saturated | numeric_target_not_derived |
| BST652_1_surface_binding | nuclear surface/binding composition charge | 2.800000e-15 | 2.932961e-08 | 3.306456347405e-03 | 2.887280314062e-05 | independent_of_kappa_if_clock_product_bound_is_saturated | numeric_target_not_derived |
| BST652_2_robust_target | robust stricter of alpha/surface smoke channels | 2.800000e-15 | 2.932961e-08 | 3.306456347405e-03 | 2.887280314062e-05 | not_fixed_by_kappa_rescaling | recommended_nonclaim_stress_target |

## Parent Action Contract

| contract_id | required_parent_statement | must_show | promotion_condition | current_status |
| --- | --- | --- | --- | --- |
| PAC652_0_matter_functor | Matter action is a species-blind functor of one observed geometry. | all matter sectors receive ehat from the same parent map and species labels do not alter the map | derived from parent action, not assumed as minimal coupling | unsigned |
| PAC652_1_constants_independent | Local matter constants and alpha_EM are not functions of chi_X/C_D in lab/source domains. | partial_chi_X theta_A=0 and no lambda_A f(chi_X)F^2 survives | explicit operator exclusion or quotient descent proof | unsigned |
| PAC652_2_source_stress_accounting | Selector/source normalization stress is included in the conserved total stress ledger. | no hidden fifth force remains after imposing common geometry | Ward identity closes with T_selector and T_MTS | open |
| PAC652_3_beta_source_owner | If common-geometry zero fails, beta_source_alpha is derived and below the robust target. | abs(beta_source_alpha) <= 2.887e-05 | parent/source-normalization theorem or sourced empirical calibration | numeric_target_only |

## Decision Gates

| gate_id | gate | result | consequence |
| --- | --- | --- | --- |
| DG652_0_conditional_zero_theorem | common-geometry WEP alpha zero theorem written | pass_template | exact clauses now exist for parent action to sign |
| DG652_1_parent_signed_zero | all common-geometry clauses are parent-derived | fail_unsigned | WEP zero is not claimed |
| DG652_2_beta_target | source-normalization target written | pass_nonclaim | finite-alpha branch has an exact beta_source target if zero theorem fails |
| DG652_3_kappa_rescale_escape | change kappa_alpha to evade WEP while keeping clock product bound | fail_policy | WEP target uses \|kappa_alpha*S_lab_alpha\|, so kappa rescaling alone does not rescue the branch |
| DG652_4_public_WEP_claim | claim WEP/local-GR pass | fail_policy | private theorem/bound contract only |

## Decision

| decision_id | route | decision | why | next_target |
| --- | --- | --- | --- | --- |
| D652_0 | common_geometry_zero | conditional_theorem_written_not_parent_signed | it would kill the direct composition channel, but the parent matter functor and no-alpha-vertex clauses are still unsigned | 653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md |
| D652_1 | source_normalization_bound | retained_as_numeric_fallback_target | if zero theorem fails, beta_source_alpha must be below the 651/652 WEP target | 653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md |
| D652_2 | next_parent_action_test | try_to_sign_parent_matter_functor_or_demote_to_closure | this is the least handwavy WEP route and the one a serious referee would accept if derived | 653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md |

## Next Contract

| contract_id | work_item | acceptance_condition |
| --- | --- | --- |
| NC652_0 | Try to sign the species-blind parent matter functor from the MTS parent action. | derive one ehat for all matter and show theta_A is internal-only/chi-independent |
| NC652_1 | If parent signing fails, demote common geometry to an explicit WEP closure axiom. | closure label is explicit and WEP/local-GR claim remains blocked |
| NC652_2 | Keep beta_source_alpha as the fallback numeric target. | future source-normalization theorem must beat the robust beta target, not just be small by assertion |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| V652_0_source_paths_exist | pass | all cited local source paths exist |
| V652_1_prior_651_validation_clean | pass | 651 validation remains clean |
| V652_2_conditional_theorem_written | pass | common-geometry zero theorem template is written |
| V652_3_theorem_not_parent_signed | pass | zero theorem remains parent-unsigned |
| V652_4_unsigned_clauses_present | pass | proof audit preserves unsigned blockers |
| V652_5_beta_target_strict | pass | robust beta target is below 3e-5 |
| V652_6_kappa_rescale_rejected | pass | kappa rescale escape is blocked |
| V652_7_parent_contract_unsigned | pass | parent action contract remains unsigned/nonclaim |
| V652_8_public_claim_blocked | pass | public WEP/local-GR claim is blocked |
| V652_9_decisions_nonclaim | pass | decision rows are nonclaim |
| V652_10_next_target_653 | pass | next target points to 653 |
| V652_11_summary_blocks_claim | pass | summary blocks WEP claim |
| V652_12_formalization_workbench_unchanged | pass | formalization files changed after cutoff: 0 |

## Interpretation

- This is progress: WEP is no longer a vague danger; it is now either a clean geometry theorem or a precise source-normalization target.
- The preferred route is still derivation, not tuning: prove the matter functor and no-alpha-vertex clauses from the parent action.
- If that cannot be signed, the honest move is to mark WEP safety as closure and keep local-GR/WEP claims blocked.

## Nonclaim Summary

| status | conditional_zero_theorem_written | parent_signed_zero | clock_product_bound_used | robust_beta_source_alpha_target | kappa_rescale_escape | WEP_claim | hardest_blocker | next_target |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_WEP_common_geometry_zero_theorem_conditional_source_normalization_target_retained_nonclaim | true | false | 2.933e-08 | 2.887e-05 | false | false | parent matter functor/no-alpha-vertex/selector Ward clauses are unsigned | 653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md |
