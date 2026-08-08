# 1730 - Tobs Support Annulus Split Or First Norm Source Row

## Verdict
- 1730 tests the cleanest way to silence the moving-`tau` source-current leak: make the active compact exterior annulus genuinely source-free.
- The theorem shape is good: if `W_source=closure(supp J_H[tau_obs])`, `A_ext cap W_source=empty`, and boundary/source flux is retained elsewhere, then bulk `T_obs|A_ext=0` and the bulk `C_Tobs_tau` piece is zero.
- Current result: this is **not signed** for current MTS. The worldtube selector, surface pair, support split, same-frame `T_obs`, boundary-flux handoff, surface/corner policy, and norm units are still open.
- The fallback is now a first nonclaim `sup_A_norm_Tobs_op` row plus boundary-flux and surface-distribution guard rows.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.

## Conditional Theorem
If the source worldtube and linked exterior annulus are parent-owned, then a vacuum exterior works exactly the way the GR intuition wants: ordinary matter stress vanishes in the bulk annulus while mass is carried by boundary/Hamiltonian/source-normalization data. The forbidden move is to use `T_obs|A_ext=0` to delete the source rather than move it into the conserved charge ledger.

## Source Register
| source_id | source_key | source_path | exists | needles_present |
| --- | --- | --- | --- | --- |
| SRC1730_0_1729_doc | 1729_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md | True | True |
| SRC1730_1_1729_next | 1729_next_target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1729_NEXT_TARGET.csv | True | True |
| SRC1730_2_1729_C_Tobs | 1729_C_Tobs_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv | True | True |
| SRC1730_3_1724_annulus_audit | 1724_annulus_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1724_ANNULUS_NORM_TAU_OWNER_AUDIT.csv | True | True |
| SRC1730_4_1016_selector_contract | 1016_selector_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv | True | True |
| SRC1730_5_1016_selector_attempt | 1016_selector_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1016_SELECTOR_THEOREM_ATTEMPT.csv | True | True |
| SRC1730_6_1016_claim_gate | 1016_claim_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1016_CLAIM_GATE.csv | True | True |
| SRC1730_7_662_parent_clauses | 662_parent_clause_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv | True | True |
| SRC1730_8_662_bound_template | 662_bound_input_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_662_BOUND_INPUT_TEMPLATE.csv | True | True |
| SRC1730_9_1720_JH_row | 1720_JH_norm_row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv | True | True |
| SRC1730_10_1719_ingredients | 1719_JH_ingredient | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv | True | True |
| SRC1730_11_683_same_frame | 683_same_frame_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv | True | True |
| SRC1730_12_1729_validation | 1729_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1729_VALIDATION.csv | True | True |

## Annulus Support Audit
| audit_id | support_clause | current_status | blocking_gap | zero_route_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ASA1730_0_worldtube_selector | parent Hilbert worldtube selector | CONDITIONAL_SELECTOR_ONLY | 1016 gives the exact selector contract, but current MTS does not parent-sign J_H, tau_obs, or compact support | False | False |
| ASA1730_1_surface_pair | linked surface pair | SURFACE_PAIR_NOT_SOURCED | 1724 records missing S1/S2, homology, orientation and annulus measure inputs | False | False |
| ASA1730_2_source_free_annulus | A_ext excludes ordinary matter support | SOURCE_FREE_ANNULUS_NOT_PARENT_SIGNED | A_ext is still a template and no support certificate proves supp(T_obs) cap A_ext is empty | False | False |
| ASA1730_3_Tobs_bulk_zero | bulk T_obs vanishes on A_ext | CONDITIONAL_THEOREM_ONLY | 1720 keeps T_obs/J_H conditional and 683 keeps same-frame measure unsigned | False | False |
| ASA1730_4_boundary_flux_accounting | boundary/source charge is retained outside bulk T_obs zero | BOUNDARY_FLUX_ACCOUNTING_MISSING | 662 and Hamiltonian charge contracts keep boundary/reference/PiM/source-normalization flux rows unsigned | False | False |
| ASA1730_5_surface_distribution_policy | distributional shell and corner policy | SURFACE_DISTRIBUTION_POLICY_MISSING | no current row certifies that shell/corner terms vanish or are moved into a sourced boundary coefficient | False | False |
| ASA1730_6_norm_pair_and_units | Tobs operator norm convention | NORM_PAIR_AND_UNITS_MISSING | 1720/1724 source rows have not declared the common annulus norm owner | False | False |
| ASA1730_7_verdict | T_obs vacuum-annulus verdict | VACUUM_ANNULUS_ZERO_NOT_SIGNED | worldtube selector, surfaces, support split, same-frame T_obs, boundary flux and norm units remain open | False | False |

## Vacuum Annulus Theorem
| theorem_id | theorem_step | statement | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAT1730_0_setup | define support-owned exterior annulus | Let W_source=closure(supp J_H[tau_obs]) and A_ext be the compact region between fixed linked surfaces S1,S2 with A_ext cap W_source empty. | CONDITIONAL_SETUP_NOT_PARENT_SIGNED | False |
| VAT1730_1_bulk_zero | ordinary Hilbert stress support | If T_obs is sourced only by ordinary matter support and the support split is regular, then T_obs\|A_ext=0 in the bulk. | CONDITIONAL_BULK_ZERO_THEOREM | False |
| VAT1730_2_delta_tau_map_zero | moving tau source-current silence in the bulk | If T_obs\|A_ext=0, then L_Tobs^A[delta tau]=star_A(T_obs(delta tau,.))=0 and C_Tobs_tau^bulk=0. | CONDITIONAL_EFFECT_ONLY | False |
| VAT1730_3_boundary_guard | mass source is not deleted | The theorem is legal only if boundary charge, Pi_M flux, reference subtraction, and source-normalization rows retain the mass information excluded from the bulk annulus. | BOUNDARY_GUARD_REQUIRED_NOT_FILLED | False |
| VAT1730_4_current_branch_verdict | current MTS theorem status | The vacuum-annulus route is mathematically clean but not a current-MTS theorem because the antecedents are unsigned. | FAIL_CURRENT_CLAIM | False |

## Tobs Norm Source Rows
| row_id | quantity | current_status | missing_inputs | numeric_value | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TNS1730_0_Z_Tobs_Aext_candidate | Z_Tobs_Aext_bulk | ZERO_ROUTE_CONDITIONAL_ANTECEDENTS_MISSING | MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_SURFACE_PAIR;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_TOBS_SUPPORT_PROOF;MISSING_BOUNDARY_FLUX_ACCOUNTING;MISSING_SURFACE_DISTRIBUTION_POLICY | MISSING_Z_TOBS_AEXT_BULK | boolean_theorem_zero_MISSING | False | False |
| TNS1730_1_sup_A_Tobs_op | sup_A_norm_Tobs_op | FIRST_NORM_SOURCE_ROW_TEMPLATE | MISSING_SYSTEM_ID;MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_OBSERVED_METRIC_OR_COFRAME;MISSING_VOLUME_FORM;MISSING_STRESS_COMPONENTS_OR_ENERGY_DENSITY_BOUND;MISSING_HODGE_FACTOR;MISSING_UNITS | MISSING_SUP_A_TOBS_OP | stress_energy_or_current_conversion_units_MISSING | False | False |
| TNS1730_2_C_Tobs_tau_from_sup | C_Tobs_tau | COEFFICIENT_UPDATE_TEMPLATE | MISSING_SUP_A_TOBS_OP;MISSING_C_STAR_MEASURE;MISSING_NORM_PAIR;MISSING_TAU_NORM;MISSING_CURRENT_NORM;MISSING_UNITS | MISSING_C_TOBS_TAU | current_norm_per_tau_norm_MISSING | False | False |
| TNS1730_3_boundary_flux_guard | B_flux_Tobs_support | BOUNDARY_FLUX_GUARD_ROW_TEMPLATE | MISSING_M_H_REF;MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_PIM_CHAIN_MAP;MISSING_UNITS | MISSING_B_FLUX_TOBS_SUPPORT | charge_or_dimensionless_after_MHref_MISSING | False | False |
| TNS1730_4_surface_distribution_guard | S_surface_Tobs_Aext | SURFACE_TERM_GUARD_ROW_TEMPLATE | MISSING_SURFACE_STRESS_POLICY;MISSING_CORNER_TERMS;MISSING_REGULARIZATION;MISSING_BOUNDARY_FLUX_ROW | MISSING_SURFACE_TOBS_AEXT | stress_integral_or_boundary_charge_units_MISSING | False | False |

## Runner Refusal
| run_id | quantity | runner_decision | refusal_reasons | accepted_for_scoring | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| RUN1730_0_vacuum_annulus_zero | T_obs\|A_ext=0 | REFUSE_CLAIM | MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_SURFACE_PAIR;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_SAME_FRAME_TOBS;MISSING_BOUNDARY_FLUX_ACCOUNTING | False | False |
| RUN1730_1_Tobs_norm_source_row | sup_A_norm_Tobs_op | ACCEPT_SCHEMA_REFUSE_SCORING | MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_STRESS_BOUND;MISSING_HODGE_FACTOR;MISSING_UNITS | False | False |
| RUN1730_2_C_Tobs_tau | C_Tobs_tau | BOUND_FORM_ONLY_REFUSE_SCORING | MISSING_SUP_A_TOBS_OP_OR_ZERO_THEOREM;MISSING_C_STAR_MEASURE;MISSING_TAU_NORM;MISSING_CURRENT_NORM | False | False |
| RUN1730_3_Newton_local_GR | Newton/local-GR reduction | BLOCKED_NO_CLAIM | VACUUM_ANNULUS_ZERO_NOT_SIGNED;BOUNDARY_FLUX_GUARD_UNFILLED;MHREF_JH_NDOMAIN_PPN_OPEN | False | False |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC1730_0_vacuum_annulus_route | keep the vacuum-annulus zero theorem as the clean route | if A_ext is genuinely source-free, the bulk T_obs moving-tau source-current coefficient can vanish without a fitted cancellation | prove the worldtube/surface/support antecedents or keep the coefficient finite |
| DEC1730_1_no_mass_erasure | do not let bulk T_obs zero erase the mass source | a vacuum exterior in GR still carries mass through boundary/Hamiltonian flux, not local matter stress in the annulus | require B_flux/M_H_ref/PiM/source-normalization accounting before any C_Tobs_tau zero promotion |
| DEC1730_2_best_next | attack A_ext surface-pair and support certificate next | numeric T_obs stress values are premature until the branch knows whether the active annulus is source-free or not | 1731 should parent-sign or explicitly source W_source, S1, S2, A_ext cap W_source, and the boundary-flux handoff |

## Next Target
| route_id | next_target | script | objective | selection_status |
| --- | --- | --- | --- | --- |
| NEXT1730_0_primary | 1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md | scripts/Y5_R2FR_Aext_surface_pair_support_certificate_or_boundary_flux_row.py | parent-sign or source W_source, S1, S2, A_ext cap W_source empty, and boundary-flux handoff; otherwise keep Tobs norm row finite and nonclaim | selected |
| NEXT1730_1_parallel_norm_units | 1731b-Y5-R2FR-Tobs-norm-units-and-Hodge-factor-source-row.md | scripts/Y5_R2FR_Tobs_norm_units_and_Hodge_factor_source_row.py | fill norm type, observed volume form, Hodge-star conversion and units for sup_A \|\|T_obs\|\|_op without scoring it | held_parallel |
| NEXT1730_2_later_CdeltaTau_stack | 1732-Y5-R2FR-CdeltaTau-source-piece-stack-runner.md | scripts/Y5_R2FR_CdeltaTau_source_piece_stack_runner.py | combine Z_Tobs_Aext or sup_A_Tobs with C_Tobs_tau only after the annulus and boundary guards are closed | later |

## Claim Gates
| claim_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1730_0_vacuum_annulus_zero | T_obs vanishes on the compact exterior annulus | BLOCKED_NO_CLAIM | ASA1730_7 says the vacuum-annulus zero theorem is not signed |
| CG1730_1_C_Tobs_tau_zero | C_Tobs_tau bulk is theorem-zero | BLOCKED_NO_CLAIM | support split, boundary flux handoff, and surface distribution policy are missing |
| CG1730_2_Tobs_norm_source_backed | sup_A \|\|T_obs\|\|_op is source-backed | BLOCKED_NO_CLAIM | first norm source row lacks A_ext, norm type, stress bound, Hodge factor and units |
| CG1730_3_MHref_JH_Ndomain | M_H_ref/J_H/N_domain can reopen | BLOCKED_NO_CLAIM | bulk source-current piece and boundary mass-flux handoff are both unclosed |
| CG1730_4_Newton_local_GR | Newton/local-GR reduction is derived | BLOCKED_NO_CLAIM | support geometry, fixed tau, Hamiltonian charge, source normalization and PPN vector remain open |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL1730_0_sources_exist | PASS | all cited source paths exist |
| VAL1730_1_needles_present | PASS | required source needles are present |
| VAL1730_2_1729_handoff_preserved | PASS | 1729 selected support-annulus route |
| VAL1730_3_annulus_audit_complete | PASS | annulus audit covers selector, surfaces, support, bulk zero, boundary flux, surface terms, norm and verdict |
| VAL1730_4_vacuum_zero_blocked | PASS | vacuum-annulus zero remains unsigned |
| VAL1730_5_conditional_theorem_written | PASS | conditional bulk C_Tobs_tau zero theorem is written |
| VAL1730_6_norm_rows_nonclaim | PASS | all norm/source rows carry missing markers and remain nonclaim |
| VAL1730_7_boundary_guard_present | PASS | boundary flux guard row is present |
| VAL1730_8_runner_refusals_cover_chain | PASS | runner refusals cover vacuum zero, norm row, C_Tobs_tau and local-GR |
| VAL1730_9_decision_next | PASS | decision selects A_ext surface-pair/support certificate next |
| VAL1730_10_next_selected | PASS | next target row selects 1731 primary route |
| VAL1730_11_claim_gates_blocked | PASS | claim gates remain blocked |
| VAL1730_12_csv_parse | PASS | all generated 1730 CSVs parse |
| VAL1730_13_no_claim_flags | PASS | all generated scoring and claim flags remain false |
| VAL1730_14_branch_copies | PASS | branch/quarantine/queue copies exist |
| VAL1730_15_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1730_16_formalization_untouched | PASS | no 1730 outputs found under formalization-workbench |
| VAL1730_OVERALL | PASS | 1730 Tobs support-annulus validation |

## Working Interpretation
This is one of the less grim local-branch moves. A vacuum exterior annulus is exactly how a GR-like theory can have no local matter stress in the exterior without losing the source mass. But the price is strict: the mass must reappear through a parent-owned boundary/Hamiltonian/source-normalization chain. So 1730 does not close local GR, but it gives us a cleaner fork: either prove the annulus/support/boundary handoff, or pay `C_Tobs_tau` as a finite source-current residual.
