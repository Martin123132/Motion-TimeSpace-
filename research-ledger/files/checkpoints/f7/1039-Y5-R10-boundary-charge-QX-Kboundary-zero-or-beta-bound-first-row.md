# 1039 Y5 R10 boundary charge QX/Kboundary zero or beta-bound first row

**Derived narrow result:** for proper compact representative-`X` transformations, where the generator and required finite jets vanish on a boundary collar, both `Q_X` and `K_boundary` vanish. That is real hygiene for the GR-reduction route.

**Claim ceiling:** this does **not** close the full local-GR/R10 branch. Source worldtubes, large/non-proper transformations, reference/mass projections, exactness, counterterms, and the parent bracket are still open.

**Fallback staged:** the first concrete beta/projection row is `alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local`, anchored to the source-backed `alpha3 <= 4e-20` bound but nonclaim until `K_boundary_alpha3` and `Phi_boundary_local` are derived or sourced.

## Source register
| source_id | source_path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC1039_0_1038_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1038_NEXT_TARGET.csv | true | true | 1038 handoff to boundary charge/cocycle or first beta row. |
| SRC1039_1_1038_closure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv | true | true | 1038 boundary obstruction inside the Omega/DCX closure audit. |
| SRC1039_2_581_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv | true | true | 581 boundary charge audit. |
| SRC1039_3_582_boundary | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv | true | true | 582 boundary differentiability audit. |
| SRC1039_4_669_theta_QX | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv | true | true | 669 Noether current/charge decomposition ledger. |
| SRC1039_5_671_owner_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv | true | true | 671 boundary charge owner gate. |
| SRC1039_6_735_proper_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_735_PROPER_BOUNDARY_DOMAIN_THEOREM.csv | true | true | 735 proper compact-support boundary-domain theorem. |
| SRC1039_7_1019_exactness | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv | true | true | 1019 boundary exactness clauses. |
| SRC1039_8_976_alpha3 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_976_K_BOUNDARY_ALPHA3_SOURCE_ACQUISITION.csv | true | true | 976 alpha3 source acquisition row for K_boundary. |
| SRC1039_9_977_alpha3_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_977_K_BOUNDARY_ALPHA3_STATUS.csv | true | true | 977 K_boundary alpha3 non-scoreable status. |
| SRC1039_10_local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | true | true | External local bounds including the alpha3 anchor. |
| SRC1039_11_R10_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | true | true | 1034 nonclaim R10 bound review candidate. |
| SRC1039_12_R10_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\R10_alpha_lambda_bound_prediction_runner.py | true | true | Existing R10 alpha(lambda) runner. |

## Compact/proper boundary silence lemma
| lemma_id | statement | derivation | status | claim_scope | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QK1039_0_variational_identity | For a differentiable local generator G_X[epsilon], the possible obstruction is a finite-jet surface density k_X[delta Y, epsilon] on partial Sigma. | delta G_X[epsilon] = bulk constraint variation + integral_partialSigma k_X[delta Y, epsilon]; Q_X is chosen to cancel or own this term. | STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_G | sets the problem; does not prove silence | false | false |
| QK1039_1_proper_collar_condition | If epsilon_X and all finite jets entering k_X vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_X or its jets vanishes pointwise. | support(epsilon_X) compactly contained in Sigma implies epsilon_X\|partialSigma = nabla^a epsilon_X\|partialSigma = 0 for required finite derivative order a. | DERIVED_NARROW_CONDITIONAL_ZERO | proper compact representative transformations only | false | false |
| QK1039_2_QX_zero | Under QK1039_1, Q_X[epsilon] = integral_partialSigma q_X[epsilon] = 0 and delta Q_X[epsilon] = 0. | q_X and delta q_X are finite-jet local surface expressions in epsilon_X and fields; the epsilon_X jet factors vanish on the boundary collar. | DERIVED_NARROW_PROPER_BRANCH_ONLY | kills representative edge charge for compact local gauge variations, not physical source or large transformations | false | false |
| QK1039_3_Kboundary_zero | Under QK1039_1 for both epsilon_X and eta_X, K_boundary[epsilon,eta] = 0 for any finite-jet local boundary cocycle. | the cocycle is a surface bilinear in the generators and finite jets; every boundary term contains a vanished generator jet. | DERIVED_NARROW_PROPER_BRANCH_ONLY | compact proper algebra closes with zero boundary cocycle | false | false |
| QK1039_4_GR_charge_guard | The proper-X zero does not erase observed ADM/time/rotation or GR Hamiltonian charges. | the vanishing condition applies to representative X parameters only; physical Hamiltonian generators remain in the observed boundary sector. | GUARD_RETAINED | prevents a fake proof that deletes GR charges to save MTS | false | false |
| QK1039_5_source_boundary_limit | The compact/proper lemma does not prove Q_X=0 for source worldtubes, large transformations, reference-boundary terms, or range-kernel weighted edge projections. | R10 and local source tests can involve nonzero boundary/support data; those terms are exactly the BCA581/BD582/BCG671 residuals. | FULL_LOCAL_CLAIM_STILL_BLOCKED | source/test beta rows remain active | false | false |
| QK1039_6_verdict | Q_X=0 and K_boundary=0 are derived only for the proper compact representative sub-branch. | QK1039_1 through QK1039_4 close the narrow boundary algebra, while QK1039_5 blocks promotion to R10/local-GR. | DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED | useful GR-reduction hygiene, not an empirical pass | false | false |

## QX/Kboundary claim gate
| gate_id | claim | gate_status | evidence | not_enough_because | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QKG1039_0_proper_compact_sublemma | proper compact representative-X transformations carry no boundary charge or cocycle | conditional_narrow_pass | epsilon_X and required finite jets vanish on a boundary collar, forcing Q_X and K_boundary surface densities to vanish | does not cover source worldtubes, large/non-proper transformations, reference terms, mass projection, or range-kernel edge rows | false | false |
| QKG1039_1_full_QX_zero | Q_X=0 for all local source/test boundaries | fail_current_claim | BCG671 and BE1019 keep Q_edge and exactness clauses open | B_X owner, exact primitive, counterterm, reference subtraction, and projector orthogonality remain missing | false | false |
| QKG1039_2_full_Kboundary_zero | K_boundary=0 for source/test or improper edge transformations | fail_current_claim | the compact-collar proof only controls finite-jet terms with vanished generator data | parent Omega and differentiable generator bracket are still not computed | false | false |

## Boundary residual beta rows
| residual_id | symbol | formula_or_contract | why_retained | missing_inputs | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BRES1039_0_Qbar_edge_XH | Qbar_edge_XH(lambda) | Qbar_edge_XH(lambda)=integral_partialSigma F_lambda epsilon_nu B_X^nu with source/reference projection | non-proper/source boundary values are not killed by the compact representative lemma | B_X owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units | false | false |
| BRES1039_1_K_boundary_alpha3 | K_boundary_alpha3 | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | the alpha3 preferred-frame anchor is extremely tight and is the cleanest first boundary-flux projection | K_boundary_alpha3; Phi_boundary_local; projection normalization; theorem-zero or numeric source | false | false |
| BRES1039_2_reference_mass_projection | Pi_M^H[Q_edge] | mass/Hamiltonian reference projector must be orthogonal to Q_edge or explicitly bounded | a zero boundary charge proof must not delete physical GR mass/energy charges | reference subtraction; Pi_M action on edge charge; no-double-count split | false | false |
| BRES1039_3_no_double_count | Q_bulk + Q_edge split | bulk and edge source terms must be orthogonal or explicitly added in absolute value | source charge cannot be hidden twice or canceled by bookkeeping | projection rules and source split | false | false |

## First beta projection template
| projection_id | residual_symbol | observable | projection_formula | empirical_anchor | bound | required_inputs | current_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FBP1039_0_boundary_alpha3 | K_boundary_alpha3 * Phi_boundary_local | alpha3 | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | 4e-20 | K_boundary_alpha3; Phi_boundary_local; normalization; source_path or theorem-zero | SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING | false | false |
| FBP1039_1_R10_edge_beta | Qbar_edge_XH(lambda) * qbar_XT(lambda) | alpha_R10(lambda) | \|alpha_edge(lambda)\| <= \|K_X^R10(lambda)\| \|Qbar_edge_XH(lambda)\| \|qbar_XT(lambda)\| plus absolute tails | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv | alpha_bound(lambda) review-candidate curve | K_X^R10(lambda); Qbar_edge_XH(lambda); qbar_XT(lambda); promoted bound curve; units | BOUND_CURVE_REVIEW_ONLY_PROJECTION_MISSING | false | false |
| FBP1039_2_absolute_tail_gate | boundary_abs_tail | all local arenas | unknown Q_X/K_boundary/source-support components add in absolute value; no cancellation credit | R10;alpha3;PPN;WEP;clock;Gdot ledgers | multiple | component theorem-zero or numeric bound rows | CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED | false | false |

## Alpha3 anchor ledger
| anchor_id | dataset_id | observable | upper_bound | units | reference | use_in_1039 | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A3A1039_0_source_bound | Will_2014_PPN_alpha3_table | alpha3 | 4e-20 | dimensionless | https://www2.math.ethz.ch/EMIS/journals/LRG/Articles/lrr-2014-4/articlese4.html | anchor only for first beta projection row; not an MTS pass | false |

## MTS alpha smoke template
| model_id | branch_id | lambda_value | alpha_predicted | force_law_form | derivation_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | proper_compact_QX_Kboundary_zero_sublemma | ALL_LOCAL_R10_RANGE | MISSING_EXTENSION_TO_SOURCE_TEST_BOUNDARIES | Q_X=K_boundary=0 only for compact proper representative-X transformations | template_invalid_narrow_sublemma_not_full_R10_branch | false |
| MTS_source_normalized_Newton_branch | boundary_alpha3_projection_template | MISSING_NOT_R10_RANGE | MISSING_K_BOUNDARY_ALPHA3_TIMES_PHI_BOUNDARY_LOCAL | alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local | template_invalid_projection_coefficients_missing | false |
| MTS_source_normalized_Newton_branch | R10_edge_beta_template | MISSING_PARENT_LAMBDA_X | MISSING_KX_QBAR_EDGE_XH_QBAR_XT | \|alpha_edge\| <= \|K_X^R10\| \|Qbar_edge_XH\| \|qbar_XT\| plus absolute tails | template_invalid_edge_projection_missing | false |

## Runner smoke status
| smoke_id | valid_mts_rows | valid_bound_rows | comparison_rows | R10_pass_for_claim | claim_allowed | expected_result |
| --- | --- | --- | --- | --- | --- | --- |
| SMOKE1039_0_runner_status | 0 | 0 | 1 | false | false | blocked_nonclaim |

## Placeholder refusal runner
| refusal_id | object | current_status | refusal_status | failure_reasons | score_eligible | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| REF1039_QK1039_0_variational_identity | For a differentiable local generator G_X[epsilon], the possible obstruction is a finite-jet surface density k_X[delta Y, epsilon] on partial Sigma. | STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_G | full_boundary_claim_not_promoted | STRUCTURAL_IDENTITY_CONDITIONAL_ON_PARENT_G;CLAIM_POLICY_FALSE | false | false |
| REF1039_QK1039_1_proper_collar_condition | If epsilon_X and all finite jets entering k_X vanish on an open collar of partial Sigma, every local boundary monomial containing epsilon_X or its jets vanishes pointwise. | DERIVED_NARROW_CONDITIONAL_ZERO | full_boundary_claim_not_promoted | DERIVED_NARROW_CONDITIONAL_ZERO;CLAIM_POLICY_FALSE | false | false |
| REF1039_QK1039_4_GR_charge_guard | The proper-X zero does not erase observed ADM/time/rotation or GR Hamiltonian charges. | GUARD_RETAINED | full_boundary_claim_not_promoted | GUARD_RETAINED;CLAIM_POLICY_FALSE | false | false |
| REF1039_QK1039_5_source_boundary_limit | The compact/proper lemma does not prove Q_X=0 for source worldtubes, large transformations, reference-boundary terms, or range-kernel weighted edge projections. | FULL_LOCAL_CLAIM_STILL_BLOCKED | full_boundary_claim_not_promoted | FULL_LOCAL_CLAIM_STILL_BLOCKED;CLAIM_POLICY_FALSE | false | false |
| REF1039_QK1039_6_verdict | Q_X=0 and K_boundary=0 are derived only for the proper compact representative sub-branch. | DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED | full_boundary_claim_not_promoted | DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED;CLAIM_POLICY_FALSE | false | false |
| REF1039_QKG1039_0_proper_compact_sublemma | proper compact representative-X transformations carry no boundary charge or cocycle | conditional_narrow_pass | boundary_gate_not_claim_promoted | does not cover source worldtubes, large/non-proper transformations, reference terms, mass projection, or range-kernel edge rows | false | false |
| REF1039_QKG1039_1_full_QX_zero | Q_X=0 for all local source/test boundaries | fail_current_claim | boundary_gate_not_claim_promoted | B_X owner, exact primitive, counterterm, reference subtraction, and projector orthogonality remain missing | false | false |
| REF1039_QKG1039_2_full_Kboundary_zero | K_boundary=0 for source/test or improper edge transformations | fail_current_claim | boundary_gate_not_claim_promoted | parent Omega and differentiable generator bracket are still not computed | false | false |
| REF1039_BRES1039_0_Qbar_edge_XH | Qbar_edge_XH(lambda) | B_X owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units | residual_retained_missing_inputs | B_X owner; F_lambda kernel; source boundary class; Pi_M/Pi_EH projection; units;SCORE_READY_FALSE | false | false |
| REF1039_BRES1039_1_K_boundary_alpha3 | K_boundary_alpha3 | K_boundary_alpha3; Phi_boundary_local; projection normalization; theorem-zero or numeric source | residual_retained_missing_inputs | K_boundary_alpha3; Phi_boundary_local; projection normalization; theorem-zero or numeric source;SCORE_READY_FALSE | false | false |
| REF1039_BRES1039_2_reference_mass_projection | Pi_M^H[Q_edge] | reference subtraction; Pi_M action on edge charge; no-double-count split | residual_retained_missing_inputs | reference subtraction; Pi_M action on edge charge; no-double-count split;SCORE_READY_FALSE | false | false |
| REF1039_BRES1039_3_no_double_count | Q_bulk + Q_edge split | projection rules and source split | residual_retained_missing_inputs | projection rules and source split;SCORE_READY_FALSE | false | false |
| REF1039_FBP1039_0_boundary_alpha3 | K_boundary_alpha3 * Phi_boundary_local | SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING | projection_row_rejected_missing_coefficients | SOURCE_BACKED_ANCHOR_READY_PROJECTION_MISSING;SCORE_READY_FALSE | false | false |
| REF1039_FBP1039_1_R10_edge_beta | Qbar_edge_XH(lambda) * qbar_XT(lambda) | BOUND_CURVE_REVIEW_ONLY_PROJECTION_MISSING | projection_row_rejected_missing_coefficients | BOUND_CURVE_REVIEW_ONLY_PROJECTION_MISSING;SCORE_READY_FALSE | false | false |
| REF1039_FBP1039_2_absolute_tail_gate | boundary_abs_tail | CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED | projection_row_rejected_missing_coefficients | CLAIM_BLOCKED_UNTIL_COMPONENTS_SOURCE_BACKED;SCORE_READY_FALSE | false | false |

## Claim gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CGATE1039_0_compact_proper_sublemma | compact proper representative-X boundary transformations are silent | conditional_narrow_only | finite-jet boundary terms vanish when the representative generator and required jets vanish on the boundary collar | false | false |
| CGATE1039_1_full_local_GR | local GR/no-pole boundary branch is fully closed | false | source worldtubes, reference/mass projection, exactness, counterterms, parent bracket, and matter/source readout remain unproved | false | false |
| CGATE1039_2_alpha3_projection | K_boundary alpha3 row is score-ready | false | alpha3 external anchor exists but K_boundary_alpha3 and Phi_boundary_local are missing | false | false |
| CGATE1039_3_R10_edge | R10 edge beta row is score-ready | false | R10 bound curve is review-only and K_X/Qbar_edge/qbar_XT are missing | false | false |

## Decision ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1039_0_boundary_derivation | A real but narrow boundary result was derived: proper compact representative-X transformations have Q_X=0 and K_boundary=0. | finite-jet boundary charges and cocycles vanish pointwise when the generator and required jets vanish on the boundary collar. | do not promote to R10/local-GR; attack the non-proper/source boundary formula next | false |
| DEC1039_1_empirical_fallback | The first beta/projection fallback row is alpha3_MTS = K_boundary_alpha3 * Phi_boundary_local. | alpha3 has a source-backed tight anchor, and existing 976/977 files already isolated this exact missing K/Phi pair. | derive or source K_boundary_alpha3 and Phi_boundary_local, or prove both theorem-zero | false |
| DEC1039_2_next_target | Next target should write the parent boundary charge formula rather than inventing a numeric coefficient. | a formula for B_X/Q_X decides both the no-pole route and the K_boundary_alpha3 fallback row. | 1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md | false |

## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1039_SUMMARY | pass | 1039 boundary Q_X/K_boundary or beta-bound first row validation summary | 2026-06-14T07:26:12.885536+00:00 |
| V1039_0_sources_exist | pass | all 1039 source paths exist and expected needles are present | 2026-06-14T07:26:12.885548+00:00 |
| V1039_1_compact_boundary_sublemma | pass | proper compact Q_X/K_boundary zero is derived but source-boundary promotion is blocked | 2026-06-14T07:26:12.885553+00:00 |
| V1039_2_qx_kboundary_gates_nonclaim | pass | Q_X/K_boundary gates keep all claims non-promoted | 2026-06-14T07:26:12.885555+00:00 |
| V1039_3_boundary_residuals_retained | pass | boundary source/test residuals are retained and non-scoreable | 2026-06-14T07:26:12.885558+00:00 |
| V1039_4_first_projection_alpha3_anchor | pass | first beta projection uses source-backed alpha3 anchor but remains nonclaim | 2026-06-14T07:26:12.885561+00:00 |
| V1039_5_alpha3_anchor_source_backed | pass | alpha3 external anchor is captured from local bound ledger | 2026-06-14T07:26:12.885563+00:00 |
| V1039_6_mts_template_schema_nonclaim | pass | MTS smoke template has runner schema and no claim-valid rows | 2026-06-14T07:26:12.885565+00:00 |
| V1039_7_runner_smoke_refuses_claim | pass | existing R10 runner refuses the 1039 nonclaim rows | 2026-06-14T07:26:12.885568+00:00 |
| V1039_8_claim_gates_blocked | pass | all public/empirical claim gates remain blocked | 2026-06-14T07:26:12.885570+00:00 |
| V1039_9_next_target_written | pass | next target row is present | 2026-06-14T07:26:12.885573+00:00 |
| V1039_10_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T07:26:12.885575+00:00 |
| V1039_11_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T07:26:12.885578+00:00 |

## Next target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md | derive the explicit parent boundary charge density B_X/Q_X from the symplectic potential and allowed boundary class; if this cannot close, build the nonclaim alpha3 projection coefficient row for K_boundary_alpha3 and Phi_boundary_local | Theta_Y boundary term, B_X surface density, exact/proper split, reference subtraction, Pi_M/Pi_EH projection, K_boundary cocycle formula, alpha3 projection normalization | invented K_boundary values, deleting GR charges, naked linear c_g scoring, cancellation between residuals, R10/local-GR pass claim, formalization-workbench edits, GitHub action | false |
