# 2024 Y5 R2FR: Observed-Representative Split Or Active Z_X M_X^2 Row

Private checkpoint. This pass writes the bridge theorem behind the hybrid route: local GR lives on `g_obs/e_obs`, while the MTS `X` direction must be quotient-vertical/exact or else become an active residual.

## Current Verdict

The observed/representative split is now precise but not signed. If a parent map `q` exists, `Dq[v_X]=0`, and `e_obs=E(q(Phi))`, then the chain rule gives `DObs_e[v_X]=0` and hence `v_X[g_obs]=0`. That is the clean way for MTS extra motion/time representatives to avoid sourcing the observed local GR metric.

The missing bridge is concrete: compute the parent `q/pi` map, the field-by-field `v_X`, and the `Dq` matrix. Matter/readout descent, representative theta exactness, boundary class, tau lock, and extra-sector silence remain required before any local-GR/Newton claim. If the split fails, the active `Z_X/M_X^2` row remains the fallback.

## Source Register

| source_id | source_path | status | needles | note |
| --- | --- | --- | --- | --- |
| SRC2024_00_2023_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2023-Y5-R2FR-parent-X-normal-form-or-ZX-MX2-first-row.md | EXISTS_NEEDLES_CONFIRMED | NEXT2023_0_2024;DEC2023_1_best_route;XNF2023_3_EH_plus_quotient_extra | 2023 handoff selects observed/representative split as best GR bridge. |
| SRC2024_01_1022_vertical | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md | EXISTS_NEEDLES_CONFIRMED | VQC1022_0_q_map;VQC1022_2_matter_descent;VQC1022_7_verdict | vertical quotient construction and no-pole theorem contract. |
| SRC2024_02_1737_qmap | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv | EXISTS_NEEDLES_CONFIRMED | QMAP1737_1_e_obs;QMAP1737_5_Z_phi_RAB | Q map contract with observed geometry and candidate vertical directions. |
| SRC2024_03_1737_dq | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv | EXISTS_NEEDLES_CONFIRMED | DQM1737_0_DObs_e;DQM1737_5_Dq_total_kernel | Dq matrix requirements for observed coframe and total kernel. |
| SRC2024_04_1737_coframe | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1737_COFRAME_FUNCTOR_ZERO_ATTEMPT.csv | EXISTS_NEEDLES_CONFIRMED | CFZ1737_0_exact_conditional;CFZ1737_3_current_verdict | coframe functor zero theorem attempt. |
| SRC2024_05_1780_signature | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv | EXISTS_NEEDLES_CONFIRMED | QTS1780_0_parent_q_map;QTS1780_7_verdict | q/Dq/tau/source functor signature gate. |
| SRC2024_06_1786_hybrid | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1786_HYBRID_EH_QUOTIENT_AUDIT.csv | EXISTS_NEEDLES_CONFIRMED | HQA1786_0_EH_core;HQA1786_5_verdict | hybrid EH-plus-quotient-extra selected nonclaim route. |
| SRC2024_07_1786_strict | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1786_STRICT_QUOTIENT_ZERO_AUDIT.csv | EXISTS_NEEDLES_CONFIRMED | SQA1786_0_q_candidate;SQA1786_5_verdict | strict quotient-zero audit and failure to promote. |
| SRC2024_08_1787_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1787_HYBRID_ACTION_SPLIT.csv | EXISTS_NEEDLES_CONFIRMED | HAS1787_1_action;HAS1787_5_verdict | hybrid action split machine-readable source. |
| SRC2024_09_1787_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1787_CONDITIONAL_REDUCTION_THEOREM.csv | EXISTS_NEEDLES_CONFIRMED | HCT1787_0_conditional_GR_reduction;HCT1787_4_verdict | conditional GR/Newton reduction theorem. |
| SRC2024_10_1787_silence | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv | EXISTS_NEEDLES_CONFIRMED | ESM1787_5_bulk_X_memory;ESM1787_7_matter_frame | extra-sector silence matrix. |
| SRC2024_11_2023_routes | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2023_X_NORMAL_FORM_ROUTE_MATRIX.csv | EXISTS_NEEDLES_CONFIRMED | XNF2023_3_EH_plus_quotient_extra;XNF2023_4_active_positive_operator | 2023 normal-form route matrix. |

## Observed/Representative Split Theorem

| theorem_id | claim | mathematical_form | status | proof_value | missing_for_claim | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ORS2024_0_field_split | observed/representative field split | Phi_parent=(e_obs,g_obs,Psi_m,theta_A; R_X,Phi_red,boundary,Pi_M,D,Gamma) | SPLIT_CONTRACT_WRITTEN | separates the GR-observed variables from representative/MTS extra variables | parent action field chart and q/pi map are not signed | false | false |
| ORS2024_1_EH_core | observed local EH core | S_obs=S_EH[g_obs]+S_matter[Psi,e_obs,theta]+B_ref[g_obs,S] | CONDITIONAL_EH_CORE_AVAILABLE | provides the GR/Newton target if extra sectors are silent | metric-only, second-order, common-source and reference clauses are unsigned | false | false |
| ORS2024_2_q_map | quotient map to observed data | q:Conf_parent -> Q_vis=(e_obs,g_obs,source/readout data,theta_owned), with X representative directions excluded | Q_MAP_CANDIDATE_NOT_COMPUTABLE | would make X representative rather than physical if its vertical basis is in ker(Dq) | q is a contract, not derived from a parent variational reduction | false | false |
| ORS2024_3_Dq_vX_gobs_zero | observed geometry invariant under X | Dq[v_X]=0 and e_obs=E(q(Phi)) imply DObs_e[v_X]=DE_q(Dq[v_X])=0 and v_X[g_obs]=0 | EXACT_CHAIN_RULE_CONDITIONAL | this is the cleanest theorem for preventing X from sourcing local GR geometry | Dq[v_X], E(q), and field-by-field v_X are not parent-computable | false | false |
| ORS2024_4_representative_theta_exact | representative-sector symplectic silence | theta_rep(v_X)=dB_X or 0, Q_X proper/exact, and omega_rep(delta,v_X)=0 modulo fixed boundary class | THETA_EXACTNESS_NOT_SIGNED | would remove X from Q_tau/M_H_ref instead of fitting its coefficient | boundary class, differentiable generator, and exact representative theta are open | false | false |
| ORS2024_5_matter_readout_descent | ordinary matter and readout descend through observed variables | S_m=sum_A S_A[Psi_A,e_obs,theta_A], Dsource_readout[Dq(v_X)]=0, and no shadow/source marker depends on X | MATTER_READOUT_DESCENT_NOT_SIGNED | would make qbar_XT=0 and prevent WEP/clock/orbit leakage | hidden frames, material markers, source prefactors, and readout feedback remain open | false | false |
| ORS2024_6_extra_sector_filter | hybrid extra-sector silence/bound filter | DeltaE_extra_i in {0,gauge,topological_no_flux,positive_source_free_silent,retained_bound} and \|Delta_local\|<=sum_i\|Delta_i\| | FILTER_EXACT_INPUTS_MISSING | prevents smuggling non-EH sectors into the EH core | R2/fR, connection, projector, boundary, source, matter-frame and bulk-X rows remain open | false | false |
| ORS2024_7_active_ZX_fallback | active X coefficient fallback | if v_X[g_obs] or theta_rep exactness fails, use active L_X with Z_X,M_X^2,J_X,boundary,Pi_M rows | FALLBACK_SCHEMA_ONLY | keeps empirical testing honest if X is physical | Z_X/M_X^2/source/boundary/projection rows are missing | false | false |
| ORS2024_8_verdict | observed/representative split currently proves local GR | ORS2024_0 through ORS2024_6 close in one parent branch | SPLIT_THEOREM_NOT_SIGNED | the bridge theorem is now explicit and targets the right missing clauses | q/Dq/g_obs invariance, theta exactness, boundary, matter/readout and residual filter are unsigned | false | false |

## Certificate / Leak Rows

| row_id | certificate | definition | required_payload | current_status | numeric_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OSC2024_0_q_map | q/pi map | explicit parent quotient map and observed functor | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_Q_MAP | MISSING | false | false |
| OSC2024_1_vX_basis | v_X field action | field-by-field representative vertical generator | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_VERTICAL_BASIS | MISSING | false | false |
| OSC2024_2_Dq_kernel | Dq[v_X]=0 | computed Dq matrix proves X direction is in kernel | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_DQ_KERNEL_CERTIFICATE | MISSING | false | false |
| OSC2024_3_gobs_invariance | v_X[g_obs]=0 | observed coframe/metric invariant under representative direction | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_DOBS_E_ZERO | MISSING | false | false |
| OSC2024_4_theta_exact | theta_rep(v_X)=dB_X or 0 | representative symplectic charge is exact/proper/fixed-boundary | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_REP_THETA_EXACTNESS | MISSING | false | false |
| OSC2024_5_boundary_class | boundary/reference class | no improper X edge charge and fixed B_ref/H_ref | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_BOUNDARY_CLASS | MISSING | false | false |
| OSC2024_6_matter_descent | S_matter descends | ordinary matter uses only e_obs/theta_owned with no X marker | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_MATTER_FUNCTOR_DESCENT | MISSING | false | false |
| OSC2024_7_readout_descent | source/clock/orbit/readout descends | readout is post-solution functor of Q_vis only | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_READOUT_FUNCTOR_DESCENT | MISSING | false | false |
| OSC2024_8_tau_lock | tau projectability | Dq(L_tau Phi)=L_tau_red q(Phi) and one tau across source/clock/orbit/charge | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_TAU_PROJECTABILITY | MISSING | false | false |
| OSC2024_9_residual_filter | extra-sector residual filter | all non-EH sectors theorem-zero or source-backed bounded | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_EXTRA_SECTOR_SILENCE | MISSING | false | false |
| OSC2024_10_active_fallback | active Z_X/M_X^2 fallback | if split fails, active operator rows exist with units/source paths | theorem_zero_or_numeric_bound;units_if_numeric;source_path;assumptions;valid_for_claim | MISSING_ACTIVE_COEFFICIENT_ROWS | MISSING | false | false |

## Claim Gates

| gate_id | gate | passed_for_nonclaim | passed_for_claim | reason |
| --- | --- | --- | --- | --- |
| CG2024_0_split_theorem_written | observed/representative split theorem is explicit | true | false | chain-rule bridge and required certificates are named |
| CG2024_1_hybrid_route_retained | EH-plus-quotient-extra remains active nonclaim route | true | false | hybrid is best GR bridge but not promoted |
| CG2024_2_q_map_signed | q/pi map is parent-signed | false | false | q is candidate-only |
| CG2024_3_Dq_gobs_zero | Dq[v_X]=0 and v_X[g_obs]=0 are signed | false | false | Dq matrix and observed functor not computable |
| CG2024_4_theta_boundary_exact | representative theta and boundary charge are exact/proper | false | false | boundary/generator exactness open |
| CG2024_5_matter_readout_descends | matter/readout sees only observed variables | false | false | no-shadow/source/readout functor clauses open |
| CG2024_6_extra_sector_silence | all non-EH sectors zero/bounded | false | false | silence matrix remains open |
| CG2024_7_local_GR_Newton | local GR/Newton reduction follows | false | false | split certificates and Q_tau/M_H_ref gates remain open |

## Refusal Runner

| refusal_id | attempted_claim | verdict | reason | accepted_for_claim |
| --- | --- | --- | --- | --- |
| REF2024_0_projection_by_declaration | put e_obs inside q by declaration and call X gauge | REFUSE | q and ker(Dq) must be derived from parent reduction, not declared. | false |
| REF2024_1_chain_rule_without_Dq | use chain-rule zero without Dq[v_X]=0 | REFUSE | DObs_e[v_X]=DE(Dq[v_X]) vanishes only after Dq[v_X] is signed. | false |
| REF2024_2_EH_core_as_full_theory | treat EH core as full local theory | REFUSE | S_extra and residual silence matrix are still open. | false |
| REF2024_3_matter_blind_by_words | assume ordinary matter/readout is blind to X | REFUSE | hidden frames, constants, source prefactors, and readout feedback need theorem or bounds. | false |
| REF2024_4_score_active_X | score active X/Z_X/M_X^2 fallback now | REFUSE | active coefficient rows remain missing/nonclaim. | false |
| REF2024_5_local_GR | claim local GR/Newton after 2024 | REFUSE | bridge theorem is conditional and all major certificates remain unsigned. | false |

## Decision Ledger

| decision_id | verdict | rationale | next_action |
| --- | --- | --- | --- |
| DEC2024_0_result | OBS_REP_SPLIT_BRIDGE_WRITTEN_NOT_SIGNED | The exact chain-rule route is now written: if q and Dq place v_X in the kernel and e_obs factors through q, then X cannot move the observed metric. | do not claim local GR; attack Dq[v_X] and DObs_e[v_X] directly |
| DEC2024_1_best_next | DQ_VX_GOBS_ZERO_IS_FIRST_CERTIFICATE | Without Dq[v_X]=0 and v_X[g_obs]=0, the quotient/hybrid route cannot even start. | build 2025 to prove Dq/v_X observed-metric zero or emit a finite DObs_e leak row |
| DEC2024_2_active_fallback | ACTIVE_ZX_MX2_REMAINS_FALLBACK | If observed/representative split fails, X returns as active residual and must be treated with Z_X/M_X^2/source/bound rows. | keep active coefficient queue but do not prioritize it ahead of Dq/g_obs zero |

## Branch Copies

| copy_id | path | exists | note |
| --- | --- | --- | --- |
| COPY2024_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_OBS_REP_SPLIT_2024_NONCLAIM.csv | true | observed/representative split theorem nonclaim copy |
| COPY2024_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2024_OBS_REP_SPLIT_STATUS_NONCLAIM.csv | true | split claim-gate status nonclaim copy |
| COPY2024_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2024_DQ_VX_GOBS_LEAK_ROW_QUEUE.csv | true | Dq/vX/g_obs leak row acquisition queue |

## Next Target

| target_id | next_doc | objective | required_inputs | excluded |
| --- | --- | --- | --- | --- |
| NEXT2024_0_2025 | 2025-Y5-R2FR-Dq-vX-observed-metric-zero-or-finite-DObs-leak-row.md | prove Dq[v_X]=0 and v_X[g_obs]=0 for the observed/representative split, or emit a finite DObs_e/Dg_obs leak row with units and source paths | parent field chart; q/pi map; v_X action on all fields; Dq matrix; Obs_e(q) functor; norm for DObs_e leak; source path; boundary/matter assumptions | projection by declaration; chain-rule zero without Dq; local-GR claim; active X scoring; GitHub; formalization-workbench edits |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL2024_00_sources | PASS | all cited source paths exist and needles are found |
| VAL2024_01_chain_rule | PASS | chain-rule observed geometry zero is explicit |
| VAL2024_02_split_not_promoted | PASS | observed/representative split is not falsely promoted |
| VAL2024_03_certificate_rows_nonclaim | PASS | all certificate/source rows remain missing/nonclaim |
| VAL2024_04_claim_gates_blocked | PASS | all claim gates remain blocked |
| VAL2024_05_refusals_active | PASS | refusals remain active |
| VAL2024_06_projection_refused | PASS | projection-by-declaration shortcut is refused |
| VAL2024_07_next_decision | PASS | decision selects Dq/vX/g_obs zero next |
| VAL2024_08_next_target | PASS | 2025 Dq/vX observed metric target is selected |
| VAL2024_09_csv_parse | PASS | all generated CSV outputs parse cleanly |
| VAL2024_10_branch_copies | PASS | branch-copy CSVs exist and parse |
| VAL2024_11_no_formalization_edits | PASS | formalization-workbench modified-file count remains 0 and no 2024 split artifacts appear there |
| VAL2024_12_output_scope | PASS | all outputs are under post-checkpoint-work |
| VAL2024_OVERALL | PASS | 2024 observed representative split or active Z_X M_X^2 row |
