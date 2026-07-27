# 1647 - Hybrid EH Quotient Current Owner Or deltaH Curl Source Fill

**Private status:** nonclaim checkpoint. No full hybrid current owner, `delta_H_tau` zero, stable Hamiltonian charge, `M_H_ref`, `M_*`, PPN pass, local-GR pass, Newton pass, R10 pass, WEP pass, clock pass, or orbital pass is claimed.

## Verdict

The hybrid route gets a real but narrow win:

```text
Q_tau^MTS = Q_EH + Q_extra + Q_boundary/ref + Q_projector + C_source
```

The EH piece remains a conditional GR baseline. Representative-only ghost channels can be pruned when they are proper, pullback-only, or matter-marker silent. But this does **not** prove the full current owner, because the surviving flux is observed/reduced, not merely representative:

```text
delta_H_tau curl still contains:
B_observed_reduced_flux_over_MH
Y5_projected_source_flux_over_MH
tau_ref_surface_mismatch_over_MH
```

So `delta_H_tau_nonintegrable_over_MH` is not theorem-zero. The next target is the observed reduced Ward/no-flux route: either derive `B_observed_reduced_flux_over_MH = 0`, or fill it as a source-backed component row.

## Source Register

| source_id | path | path_exists | needles_found | role |
| --- | --- | --- | --- | --- |
| 1646_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1646-Y5-R2FR-theta-Qtau-current-owner-or-deltaH-component-source-row.md | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 1646_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1646_VALIDATION.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 1646_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_NEXT_TARGET.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 1646_current | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 1646_qtau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_QTAU_DECOMPOSITION_STATUS.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\772-Y5-R10-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_772_VALIDATION.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_hybrid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_772_HYBRID_CURRENT_OWNER_AUDIT.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_narrow | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_772_NARROW_ZERO_IMPORT_LEDGER.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_curl | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_772_DELTAH_CURL_DECOMPOSITION.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_772_DELTAH_CURL_SOURCE_FILL_FALLBACK.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 772_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_772_DECISION_MATRIX.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 734_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 735_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_735_SECOND_ZERO_ATTEMPT.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 736_zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 737_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 738_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 773_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\773-Y5-R10-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 773_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_773_VALIDATION.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |
| 773_component | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_773_DELTAH_CURL_COMPONENT_FILL.csv | True | True | 1647 hybrid EH-plus-quotient current-owner test |

## Hybrid Current Owner Audit

| audit_id | hybrid_clause | test | current_result | what_it_prunes | what_remains |
| --- | --- | --- | --- | --- | --- |
| HCO1647_0_observed_EH_current | observed GR sector uses the EH current | Q_tau^MTS has an EH part Q_EH[g_obs,tau] with fixed boundary/reference | CONDITIONAL_REFERENCE_ALLOWED | prevents rebuilding the GR Hamiltonian current from scratch where observed EH assumptions truly hold | EH-only does not own MTS extra, boundary, q_loc/Y5/Y6, projector, tau/reference, or coupling terms |
| HCO1647_1_hybrid_split | parent configuration splits into observed quotient plus representative fibre | Y=(O_GR,Phi_red,R_rep,B_ref) and pi_h(Y)=(O_GR,Phi_red,B_ref) | FORMAL_MAP_CONSTRUCTED_NOT_FULL_PARENT_SIGNATURE | representative variables are not automatically observed local fields | Gamma/Khat/P_loc symbol match, matter descent, boundary/reference and ADM separation remain unsigned |
| HCO1647_2_representative_vertical_zero | representative-fibre motion cannot directly source q_loc when q_loc objects are pullbacks | L_{v_X^rep} q_loc^nu=0 under Gamma/Khat/P_loc pullback premises | NARROW_ZERO_IMPORTED | direct hidden representative fifth-force source | observed reduced q_loc itself can be nonzero through Phi_red/Euler/boundary/source terms |
| HCO1647_3_proper_boundary_zero | proper representative transformations have zero representative boundary charge | Q_X^rep[partial U]=0 for compact-support or boundary-collar-vanishing v_X^rep | NARROW_ZERO_IMPORTED | pure representative improper edge charge | observed reduced boundary/source-measure flux and non-proper edge modes remain live |
| HCO1647_4_matter_marker_zero | ordinary matter/readout has no direct representative marker | delta_{v_X^rep}S_matter=0 if matter functors factor through Q_obs^hybrid | NARROW_ZERO_IMPORTED_CONDITIONAL | direct representative matter-marker/source-frame charge | full source normalization, mu_extra, PiM flux closure, Gauss/orbital calibration and PPN stability remain open |
| HCO1647_5_reduced_q_loc_owner | Gamma/Khat/P_loc are owned by a reduced GK action on Q_obs^hybrid | S_GK^hyb gives Gamma_eff=gamma, K_hat=metric response, q_loc=P_loc div(T_GK) | FAILED_CURRENT_SYMBOL_MATCH | nothing beyond conditional pullback zero | observed q_loc residual, Y5/Y6, PPN tail, boundary flux, and source projection |
| HCO1647_6_source_projector_owner | same-frame source current and PiM projector close projected mass flux | d(Pi_M J_H)=0 on compact local exterior | BLOCKED_BY_SOURCE_PROJECTOR_CHAIN | standard matter Ward identity only | projector commutator, exchange flux, boundary/anomaly flux, Hilbert/topological equality |
| HCO1647_7_owner_verdict | accept hybrid EH+quotient current owner for FB5540/q_R local branch | HCO1647_0 through HCO1647_6 jointly close | FAIL_CURRENT_CLAIM | representative-only ghost channels are pruned | observed reduced boundary/source flux and deltaH curl must be derived or source-filled |

## Narrow Zero Import Ledger

| zero_id | source_row | zero_statement | status_after_1647 | legitimate_use | residual_left |
| --- | --- | --- | --- | --- | --- |
| NZI1647_0_representative_q_loc_variation | FZA734_0_representative_vertical_q_loc_variation | L_{v_X^rep} q_loc^nu=0 under hybrid pullback premises | IMPORTED_CONDITIONAL_ZERO | remove direct representative-fibre source dependence | observed reduced q_loc from Phi_red/Euler/boundary/source terms |
| NZI1647_1_proper_representative_boundary | SZA735_0_proper_representative_boundary_charge | Q_X^rep[partial U]=0 for proper representative transformations | IMPORTED_CONDITIONAL_ZERO | remove pure representative improper boundary charge from proper gauge domain | observed reduced boundary flux, edge modes, corner flux, ADM/reference split |
| NZI1647_2_proper_corner_symplectic | SZA735_1_proper_corner_symplectic_flux | Omega_boundary(delta Y,v_X^rep)=0 for representative support vanishing in boundary collar | IMPORTED_CONDITIONAL_ZERO | remove proper representative corner symplectic leakage | boundary flux carried by Q_obs^hybrid/Phi_red/matter readout |
| NZI1647_3_matter_no_marker | TZA736_0_direct_representative_matter_marker | delta_{v_X^rep}S_matter=0 under strict no-marker one-coframe contract | IMPORTED_CONDITIONAL_ZERO | remove direct representative matter-marker coupling | dressed source mass, mu_extra, C_qmu q_loc, Gauss calibration, PPN stability |
| NZI1647_4_ADM_double_count_guard | SZA735_2_ADM_double_count_guard | ordinary ADM/time/rotation/boost charges remain in Q_obs^hybrid, not in representative vertical domain | GUARD_IMPORTED_NOT_FULL_PROOF | avoid quotienting away physical EH Hamiltonian generators | Pi_M/Pi_EH projection, M_H_ref, source equality and Poisson/Gauss calibration |

## deltaH Curl Decomposition

| curl_id | curl_term | hybrid_status | current_result | source_fill_if_fails |
| --- | --- | --- | --- | --- |
| CDC1647_0_EH_observed_flux | int_S i_tau omega_EH | CONDITIONAL_GR_BASELINE | NOT_FULL_MTS_OWNER_BUT_ALLOWED_REFERENCE_PIECE | deltaH_EH_boundary_flux_over_MH |
| CDC1647_1_representative_vertical_flux | Omega_boundary(delta Y,v_X^rep)+Q_X^rep | PROPER_REPRESENTATIVE_PIECE_PRUNED_CONDITIONALLY | NARROW_ZERO_ONLY | QX_rep_improper_edge_flux_over_MH |
| CDC1647_2_observed_reduced_boundary_flux | P_loc B_boundary^nu and reduced observed source flux | NOT_PRUNED | OPEN_PRIMARY_NEXT_TARGET | B_observed_reduced_flux_over_MH |
| CDC1647_3_Y5_source_projector_flux | d(Pi_M J_H) and source-normalization projection | NOT_PRUNED | BLOCKED_BY_SOURCE_PROJECTOR_CHAIN | Y5_projected_source_flux_over_MH |
| CDC1647_4_tau_reference_surface | Delta_tau+Delta_S+Delta_ref | NOT_PRUNED | STILL_OPEN_FROM_1645_1646 | tau_ref_surface_mismatch_over_MH |
| CDC1647_5_total_deltaH | delta_H_tau_nonintegrable_over_MH | NOT_ZERO | SOURCE_FILL_REQUIRED_IF_NEXT_ZERO_FAILS | DHS1646_0_deltaH_curl |

## deltaH Curl Source Fill Fallback

| fill_id | quantity | definition | current_status | claim_gate |
| --- | --- | --- | --- | --- |
| HSF1647_0_observed_reduced_boundary_flux | B_observed_reduced_flux_over_MH | abs(P_loc B_boundary^nu contribution to curl(deltaH))/M_H_ref | MISSING_OBSERVED_REDUCED_BOUNDARY_FLUX_ZERO_OR_NUMERIC | theorem-zero or source-backed bound before deltaH pass |
| HSF1647_1_Y5_projected_source_flux | Y5_projected_source_flux_over_MH | abs(integral_A d(Pi_M J_H))/M_H_ref or equivalent projected source-mass flux | MISSING_PIM_PROJECTED_FLUX_ZERO_OR_NUMERIC | closed projected mass current or source-backed radial/source flux bound |
| HSF1647_2_tau_ref_surface_mismatch | tau_ref_surface_mismatch_over_MH | abs(Delta_tau+Delta_S+Delta_ref)/M_H_ref | MISSING_TAU_REF_SURFACE_ZERO_OR_NUMERIC | same tau/reference/surface theorem or source-backed mismatch bound |
| HSF1647_3_deltaH_total | delta_H_tau_nonintegrable_over_MH | sum of nonnegative curl components with no cancellation credit | MISSING_COMPONENTS | every component zero/bounded and no placeholder markers |

## Decisions

| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC1647_0_hybrid_not_promoted | do not accept the hybrid EH+quotient route as a full current owner yet | it prunes representative-only channels but observed reduced q_loc/source/boundary/tau flux remains open | H_tau/MHref/local-GR remain blocked |
| DEC1647_1_keep_narrow_zeros | retain the representative narrow zeros as discipline gates | they remove fake representative channels and stop EH/ADM double counting | representative ghosts are pruned but observed flux must still be derived or bounded |
| DEC1647_2_next_observed_flux | attack observed reduced boundary/source flux next | it is the first live deltaH curl term not killed by representative quotient silence | 1648 should derive a reduced Ward/no-flux theorem or fill B_observed_reduced_flux_over_MH |

## Claim Gates

| gate_id | claim | gate_pass | status | blocker |
| --- | --- | --- | --- | --- |
| CG1647_0_hybrid_current_owner | hybrid EH+quotient route is a full current owner | False | BLOCKED | OBSERVED_REDUCED_FLUX_AND_PROJECTOR_SOURCE_FLUX_OPEN |
| CG1647_1_representative_narrow_zeros | representative-only ghost channels are pruned | True | PASS_AS_NARROW_INTERNAL_ZERO_ONLY | does not imply observed flux zero |
| CG1647_2_deltaH_zero | delta_H_tau_nonintegrable_over_MH is theorem-zero | False | NO_CLAIM | B_observed_reduced_flux_over_MH and Y5_projected_source_flux_over_MH remain live |
| CG1647_3_local_GR_PPN_R10 | local GR, PPN, R10, or Newton pass follows from 1647 | False | NO_CLAIM | hybrid current owner remains nonclaim |
| CG1647_4_guardrail | hybrid current-owner guardrail is installed | True | PASS_AS_INTERNAL_GUARDRAIL_ONLY | guardrail is not evidence |

## Next Target

| next_target | script | objective | success_condition |
| --- | --- | --- | --- |
| 1648-Y5-R2FR-observed-reduced-boundary-source-flux-zero-or-deltaH-curl-component-fill.md | scripts/Y5_R2FR_observed_reduced_boundary_source_flux_zero_or_deltaH_curl_component_fill.py | derive the observed reduced Ward/no-flux theorem for B_observed_reduced_flux_over_MH, or fill it as a source-ready deltaH curl component row | S_red, Gamma_eff/K_hat/P_loc, reduced Euler equations, boundary/reference no-flux, source-measure silence, projector descent, and tau/surface lock jointly prove zero or yield explicit bounded rows |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1647_0_sources_exist | PASS | all cited 1647 source paths exist and needles are present |
| VAL1647_1_hybrid_owner_not_promoted | PASS | hybrid owner audit refuses full promotion |
| VAL1647_2_narrow_zeros_imported | PASS | representative narrow zeros and ADM guard imported |
| VAL1647_3_deltaH_live_terms_decomposed | PASS | deltaH curl live terms are decomposed |
| VAL1647_4_fallback_rows_staged | PASS | fallback source rows are staged as nonclaim |
| VAL1647_5_next_observed_flux_selected | PASS | observed reduced boundary/source flux selected next |
| VAL1647_6_claim_gates_safe | PASS | all claim gates keep MTS claims false |
| VAL1647_7_next_target_selected | PASS | next target selects observed reduced boundary/source flux |
| VAL1647_8_csv_parse | PASS | all generated 1647 CSVs parse |
| VAL1647_9_no_mts_claim_flags | PASS | all 1647 generated rows keep MTS claim/no-score flags false |
| VAL1647_10_branch_copies | PASS | branch/quarantine copies exist |
| VAL1647_11_queue_copies | PASS | acquisition queue nonclaim copies exist |
| VAL1647_12_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1647_13_formalization_untouched | PASS | no 1647 outputs found under formalization-workbench |
| VAL1647_OVERALL | PASS | 1647 hybrid EH quotient current-owner and deltaH curl source-fill validation |
