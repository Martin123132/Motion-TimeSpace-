# 608 Y5 R10 double-zero exponent origin or source-neutrality proof

Generated: 2026-06-05T21:02:01.277340+00:00  
Status: `Y5_R10_p2_norm_square_theorem_derived_conditionally_parent_marker_exclusion_not_signed`  
Claim ceiling: `conditional_p2_p3_origin_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass`  
Next target: `609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md`  
Run root: `runs/20260605-210201-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof`

## Verdict
- The best derivation is the norm-square theorem: if the compact-shell variable is a primitive amplitude `a_D`, and the parent action has no linear marker covector, then smooth scalar activation starts at `||a_D||^2`, so `p=2`.
- This is a real conditional theorem, not just a wish. It is also not yet a claim, because the current corpus has not parent-owned the amplitude, fibre metric, and no-marker symmetry.
- The determinant route still gives a beautiful `p=3` shape, but only for parent-owned `Q_coh`; raw `det(Q)` is forbidden because it leaks tracefree shear.
- Source/test/no-pole neutrality remains a fallback, not the first promotion route.

## Source Register
| source_file | exists | role |
| --- | --- | --- |
| 607-Y5-R10-compact-shell-parent-coefficient-factorization-or-theorem-zero.md | True | immediate 607 handoff |
| source-intake/mts_residuals/P8_Y5_BRR545_607_VALIDATION.csv | True | prior validation gate |
| source-intake/mts_residuals/P8_Y5_R10_607_EPSILON_EXPONENT_GATE.csv | True | p gate requiring origin |
| 476-double-zero-memory-coupling-origin-or-coefficient-runner.md | True | p>=2 requirement and determinant clue |
| 475-domain-selector-parent-action-clause-or-coefficient-fill.md | True | double-zero parent action clause |
| 478-determinant-current-parent-ownership-or-demotion.md | True | det(Q_coh) p=3 ownership audit |
| 275-JC-three-form-memory-current-from-Q.md | True | conditional determinant current construction |
| 276-coherent-domain-projector-from-parent-variables.md | True | fixed-D Q_coh projection |
| 309-MTS-boundary-projector-contract-attempt.md | True | P_MTS/P_coh projector contract |
| 572-Y5-R10-parent-coefficient-envelope-or-neutrality-theorem.md | True | zero-factor and neutrality theorem attempts |
| 573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md | True | no-marker theorem reduction |
| 574-Y5-R10-local-invariant-generator-elimination-or-finite-envelope.md | True | surviving marker generators |
| 576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md | True | qbar_XT source-current conditional theorem |
| 407-primitive-relational-quotient-action-sketch.md | True | primitive quotient action sketch |
| 413-no-marker-parent-action-theorem-attempt.md | True | no-marker parent theorem attempt |
| source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | True | anchor-only non-claim R10 bound rows |
| scripts/R10_alpha_lambda_bound_prediction_runner.py | True | existing comparator reused unchanged |
| scripts/Y5_R10_double_zero_exponent_origin_or_source_neutrality_proof.py | True | this checkpoint generator |

## Norm-Square P2 Theorem Attempt
| step_id | claim | math_form | derivation | result | promotion_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NS608_0_define_primitive_amplitude | compact-shell activation has a primitive amplitude a_D in a relative-memory/source fibre E_D | a_D in E_D, local trivial branch a_D=0, epsilon_amp=\|\|a_D\|\| | 607's epsilon exponent can be made precise only by deciding whether epsilon_shell is a primitive amplitude or an already-squared invariant. | amplitude_variable_defined_as_theorem_target | conditional | current proxy 7.432631961576971e-06 is not yet proved to be \|\|a_D\|\| rather than \|\|a_D\|\|^2 or another scalar | false |
| NS608_1_no_linear_marker | a scalar parent action cannot contain a naked linear a_D term if no orientation/source marker vector exists | S_act[a_D]=S_act[-a_D] or more generally S_act[R a_D]=S_act[a_D] for R in O(E_D) | a linear term L(a_D)=ell(a_D) requires a parent-owned covector ell in E_D*, which is exactly a material/domain/source marker. | linear_term_forbidden_if_no_marker_theorem_holds | conditional_theorem | 573/574 did not eliminate all marker generators for claim | false |
| NS608_2_taylor_evenness | smooth marker-free activation has no odd linear term at a_D=0 | F(a_D)=F(0)+1/2 H_D(a_D,a_D)+O(\|\|a_D\|\|^4) | O(E_D) or sign invariance forces dF_0=0. Local silence additionally requires F(0)=0. | leading_activation_order_is_quadratic_in_primitive_amplitude | conditional_pass | requires parent-owned fibre metric/inner product and no-linear-marker theorem | false |
| NS608_3_p2_source_law | if epsilon_shell is the primitive amplitude norm, p=2 follows | J_X = epsilon_amp^2 kappa_X rho_X + O(epsilon_amp^4); alpha_X=epsilon_amp^2 C_X + O(epsilon_amp^4) | insert NS608_2 into 607's Green-function factorization. | p_equals_2_derived_conditionally | not_parent_signed | epsilon proxy/amplitude identification and no-marker symmetry are not parent-derived | false |
| NS608_4_epsilon_notation_warning | p depends on what epsilon_shell denotes | if epsilon_shell=A_D=\|\|a_D\|\|^2, then alpha=epsilon_shell C_X is p=1 in epsilon but p=2 in primitive a_D | avoid fake p=2 promotion by locking the primitive variable before scoring. | notation_gate_required | guardrail | current compact-shell proxy has not been decomposed into primitive amplitude versus invariant norm | false |
| NS608_5_normsquare_verdict | the norm-square route derives p>=2 | no linear marker + smooth scalar parent + epsilon=\|\|a_D\|\| => p=2 | this is the best clean theorem shape for local-GR silence. | conditional_p2_theorem_derived_not_claim_promoted | theorem_target | parent-owned no-marker and epsilon-amplitude identification remain unsatisfied | false |

## Determinant P3 Theorem Attempt
| step_id | claim | math_form | source_support | result | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DET608_0_fixed_domain_shape | coherent determinant gives p=3 | J_C=det(Q_coh) Omega_D/V_D; integral_D J_C=(N_D/u3)^3 | 275 derives the fixed-domain kinematic shape | p3_shape_supported_conditionally | fixed-D and Q_coh ownership are not enough for physical local branch | false |
| DET608_1_raw_det_rejected | raw det(Q) is safe | det(XI+S)=X^3-(X/2)Tr(S^2)+det(S) | 275/478 show tracefree shear leaks into raw determinant | fail_raw_route | would activate local shear/GW/environmental channels | false |
| DET608_2_Qcoh_projection | Q_coh projection removes shear | P_coh[Q]^i_j=(1/3)<Tr Q>_D delta^i_j | 276 derives this for fixed D and fixed norm | fixed_D_projection_pass | physical D, P_MTS, Ward stress, and source channel still not parent-owned | false |
| DET608_3_FLRW_survival | determinant route keeps FLRW active | FLRW Q_coh=(N/u3)I so integral_D J_C=(N/u3)^3 | 275 gives FLRW reduction and endpoint regularity | FLRW_survival_conditionally_good | same parent selector must derive local zero and FLRW nonzero without a fitted window | false |
| DET608_4_parent_ownership | det(Q_coh) is parent-owned as physical source | S_parent -> D, P_MTS, P_coh, Ward-safe stress, R11 source silence | 478 says this ownership chain fails current corpus | not_parent_owned | domain selection/projector/Ward/R11 gates remain open | false |
| DET608_5_verdict | p=3 is derived for the physical local branch | alpha_X=epsilon_amp^3 C_X | shape yes, ownership no | p3_theorem_target_not_claim | only parent-owned Q_coh determinant can be used; raw determinant is forbidden | false |

## Source-Neutrality Fallback
| fallback_id | zero_target | proof_shape | source_status | why_not_promoted | if_closed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SN608_0_qbar_XT | qbar_XT=0 | ordinary matter action factors through one observed X-blind coframe and MTS-trivial constants | conditional theorem from 572/576 | 573/574 did not eliminate marker generators and 579 conformal countermodel remains legal | C_X=0 for ordinary test bodies | false |
| SN608_1_Qbar_XH | Qbar_XH(lambda)=0 | compact source, boundary, memory, domain, projector channels are in X kernel or orthogonal to Pi_M | not derived | hidden source channels and Pi_M projector ownership remain open | C_X=0 for laboratory sources | false |
| SN608_2_KX | K_X=0 | X is a first-class constraint/no-pole mode before source variation | not derived | 607 branch explicitly retains a finite quadratic X block | no finite Yukawa exchange | false |
| SN608_3_priority | source neutrality as fallback | derive one zero factor only if p-origin path cannot be parent-owned | defer | p>=2 route is more local-GR-friendly because it attacks source activation, not just one test channel | R10 alpha can be theorem-zero without relying on epsilon power | false |

## Counterexample Gate
| counterexample_id | construction | why_allowed_without_premise | damage | blocked_by | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CE608_0_linear_marker_covector | parent action contains ell(a_D) X with a nonzero covector ell in E_D* | if no-marker/O(E_D) symmetry is not parent-derived, ell is a legal source marker | p=1 returns and double-zero local silence fails | parent-owned marker exclusion or O(E_D) invariant norm-square action | false |
| CE608_1_epsilon_already_squared | epsilon_shell is defined as A_D=\|\|a_D\|\|^2 rather than primitive \|\|a_D\|\| | current proxy provenance does not identify primitive amplitude | p=1 in epsilon notation can be physically p=2; scoring becomes ambiguous | explicit amplitude/norm-square ledger before any alpha row promotion | false |
| CE608_2_raw_determinant_shear | use det(Q) instead of det(Q_coh) | if projection ownership is skipped, raw determinant is the simple-looking parent scalar | tracefree shear leaks into local branch and can violate GR recovery | parent-owned coherent projection plus Ward stress accounting | false |
| CE608_3_conformal_matter_coupling | hat_g_mu_nu=exp(2 a X) g_mu_nu | covariant universal matter coupling alone does not force a=0 | qbar_XT and J_matter are nonzero even if p>=2 reduces compact-shell source | X-blind observed coframe and constant-sector no-marker theorem | false |
| CE608_4_overstrong_zero_kills_FLRW | impose all compact-shell/domain activation zero in every domain | a closure can silence local branch by also murdering cosmology | loses the unified-field spine because FLRW memory branch dies | same parent selector must give local trivial and FLRW nontrivial classes | false |

## Exponent Decision
| decision_id | candidate | mathematical_status | claim_status | why | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ED608_0_p2_normsquare | p=2 from norm-square/even parent activation | conditional theorem derived | not promoted | requires no-linear-marker/O(E_D) symmetry and primitive epsilon identification | parent-own norm-square activation | false |
| ED608_1_p3_determinant | p=3 from det(Q_coh) | conditional fixed-D shape supported | not promoted | raw det leaks shear and Q_coh/D/P_MTS/Ward/R11 ownership is incomplete | keep as theorem target, not first promotion route | false |
| ED608_2_p1_finite | p=1 finite residual | still legal unless marker exclusion closes | retained fallback | linear marker covector counterexample remains legal without no-marker theorem | score later only if p>=2 cannot be derived and coefficients are numeric | false |
| ED608_3_zero_factor | source/test/no-pole neutrality | conditional fallback | not promoted | qbar/source/K zero routes remain blocked by 572/576/579 | try only after p-origin route is exhausted | false |

## Parent Input Update
| input_id | required_input | exact_definition | current_status | needed_to_promote | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PUI608_0_primitive_amplitude | a_D and epsilon_amp=\|\|a_D\|\| | primitive compact-shell relative-memory/source amplitude before squaring | not_parent_identified | prove current epsilon_shell proxy is the primitive amplitude or rewrite p in primitive variables | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| PUI608_1_marker_exclusion | no parent covector ell(a_D) | no natural material/domain/source marker can select a sign/direction in E_D | conditional_only | eliminate 573/574 marker generators or encode O(E_D) symmetry in parent action | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| PUI608_2_fibre_metric | parent-owned inner product on E_D | positive relative-memory/domain fibre metric used to form \|\|a_D\|\|^2 | not_parent_owned | derive inner product from parent symplectic/Hodge/relative complex without closure | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| PUI608_3_local_FLRW_split | local a_D=0, FLRW a_D!=0 | same selector gives exact local trivial class and nontrivial FLRW coherent class | conditional | derive branch split without fitted window or PPN-motivated collar choice | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| PUI608_4_CX | C_X(lambda_X) | sigma_X kappa_X Qbar_XH(lambda_X) qbar_XT/(4*pi Z_X G_obs) | symbolic | numeric source/test/Hessian coefficients or a source-neutrality zero | defer until p branch is parent-owned | false |

## MTS Double-Zero Template
| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_double_zero_exponent_origin | R10_normsquare_p2_symbolic | R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE | 3.86e-5 | m | (epsilon_amp**2)*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | symbolic_double_zero_origin_nonclaim | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md::NS608_3_or_DET608_0 | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md | MISSING_PARENT_OWNED_EPSILON_AMP;MISSING_NO_MARKER_SYMMETRY;MISSING_C_X;anchor_bound_only | false | Template row only: conditional norm-square theorem target; runner must reject until parent inputs and bound curve are claim-grade. |
| MTS_double_zero_exponent_origin | R10_determinant_p3_symbolic | R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE | 3.86e-5 | m | (epsilon_amp**3)*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM | Yukawa_potential_alpha | symbolic_double_zero_origin_nonclaim | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md::NS608_3_or_DET608_0 | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md | MISSING_PARENT_OWNED_EPSILON_AMP;MISSING_NO_MARKER_SYMMETRY;MISSING_C_X;anchor_bound_only | false | Template row only: conditional determinant theorem target; runner must reject until parent inputs and bound curve are claim-grade. |
| MTS_double_zero_exponent_origin | R10_normsquare_p2_symbolic | R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE | 5.6e-5 | m | (epsilon_amp**2)*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | symbolic_double_zero_origin_nonclaim | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md::NS608_3_or_DET608_0 | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md | MISSING_PARENT_OWNED_EPSILON_AMP;MISSING_NO_MARKER_SYMMETRY;MISSING_C_X;anchor_bound_only | false | Template row only: conditional norm-square theorem target; runner must reject until parent inputs and bound curve are claim-grade. |
| MTS_double_zero_exponent_origin | R10_determinant_p3_symbolic | R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE | 5.6e-5 | m | (epsilon_amp**3)*C_X(lambda_X) | 1.0 | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv::R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM | Yukawa_potential_alpha | symbolic_double_zero_origin_nonclaim | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md::NS608_3_or_DET608_0 | 608-Y5-R10-double-zero-exponent-origin-or-source-neutrality-proof.md | MISSING_PARENT_OWNED_EPSILON_AMP;MISSING_NO_MARKER_SYMMETRY;MISSING_C_X;anchor_bound_only | false | Template row only: conditional determinant theorem target; runner must reject until parent inputs and bound curve are claim-grade. |

## Runner Summary
| runner_id | mts_curve | bound_curve | mts_rows | valid_mts_rows | bound_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | R10_pass_for_claim | claim_allowed | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R10_RUNNER_608_DOUBLE_ZERO_TEMPLATE_RECHECK | source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_DOUBLE_ZERO_EXPONENT_TEMPLATE.csv | source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv | 4 | 0 | 2 | 0 | 1 | 0 | 1 | False | False | required blocked result: p=2/p=3 templates remain symbolic and anchor bounds are nonclaim |

## Decision
| decision_id | status | decision | meaning | next_target | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| D608_0_normsquare_theorem | conditional_theorem_derived | accept p=2 as a valid theorem if parent owns primitive amplitude, norm-square action, and no-linear-marker symmetry | this is the cleanest local-GR-friendly route but not a current claim | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| D608_1_determinant_theorem | conditional_shape_only | keep p=3 determinant route as a theorem target, not first promotion route | det(Q_coh) is stronger but depends on more projector/domain ownership than norm-square p=2 | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| D608_2_source_neutrality | fallback_not_promoted | do not switch to source neutrality until p-origin route is exhausted | qbar/source/no-pole zeros are useful but currently less close than the norm-square theorem | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |
| D608_3_claim_ceiling | conditional_p2_p3_origin_attempt_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass | no R10, WEP, PPN, or local-GR pass | p>=2 is conditional and C_X/lambda/bound-curve inputs remain unresolved | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md | false |

## Route Update
| route_id | allowed_after_608 | forbidden_after_608 | next_action |
| --- | --- | --- | --- |
| RU608_0_primary | try to parent-own the norm-square activation and no-linear-marker symmetry | use p=2 in claim rows before epsilon_amp and marker exclusion are parent-derived | 609-Y5-R10-parent-own-norm-square-activation-or-finite-p1-branch.md |
| RU608_1_determinant | retain det(Q_coh) as p=3 theorem target | use raw det(Q) or ignore shear leakage | defer unless norm-square route fails |
| RU608_2_fallback | fallback to qbar/source/no-pole neutrality or finite p=1 score if p>=2 fails | erase p=1 counterexample without no-marker theorem | keep finite branch retained |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| V608_0_source_paths_exist | pass | missing=0 |
| V608_1_prior_607_clean | pass | prior_rows=10;prior_failures=0 |
| V608_2_normsquare_p2_conditional | pass | no linear marker + smooth scalar parent + epsilon=\|\|a_D\|\| => p=2 |
| V608_3_p2_not_promoted | pass | norm_rows=6;claim_rows=0 |
| V608_4_determinant_p3_not_promoted | pass | only parent-owned Q_coh determinant can be used; raw determinant is forbidden |
| V608_5_source_neutrality_not_promoted | pass | source_neutrality_rows=4;claim_rows=0 |
| V608_6_counterexamples_block_shortcuts | pass | counterexamples=5 |
| V608_7_template_symbolic_nonclaim | pass | template_rows=4;symbolic=True;nonclaim=True |
| V608_8_runner_blocks_template | pass | valid_mts=0;valid_bound=0;R10_pass=False;claim_allowed=False |
| V608_9_no_claim_rows | pass | claim_rows=0 |
| V608_10_no_R10_or_local_GR_claim | pass | R10_pass=false;WEP=false;PPN=false;local_GR=false |

## Practical Read
This is one of the better-looking local-branch moves so far. We have not proved local GR, but we found the exact parent-action shape that would make the annoying linear residual illegal: no linear marker plus norm-square activation. That is very engineering-flavoured: if there is no signed handle to grab, the first scalar you can build is quadratic. The next lock is therefore narrow and concrete: parent-own the primitive amplitude/fibre metric/no-marker symmetry, or admit the finite `p=1` branch remains legal.
