# 2395 — EH Local Geometry Kernel Split Or EH Contamination Row

## Result

2395 gets a real derivation foothold.

If the observed local geometry is genuinely quotient-owned,

`e_obs(Phi) = Obs_e(q(Phi))`,

and the tested vector is a pure local vertical direction,

`v_k in ker(Dq)` with no observed spacetime generator `xi`,

then

`delta_v e_obs = DObs_e[Dq(v_k)] = 0`.

For an EH term built only from `e_obs`,

`delta_v L_EH = E_EH dot delta_v e_obs + dTheta_EH(e_obs;delta_v e_obs) = 0`,

so

`Theta_EH(e_obs;v_k)=0`, `mu_EH[v_k]=0`, `J_EH[v_k]=0`, and conditionally `Q_EH[v_k]=0`

after the compact/local zero-flux boundary class is fixed.

That is the good news.  The guardrail is just as important: the ordinary EH/GR diffeomorphism charge is not being
zeroed.  If a parent tangent has an observed spacetime part `h_xi`, then `Q_EH[h_xi]` is the GR reference charge.
Only the pure quotient-kernel part `k` is supposed to vanish.  This is exactly the route MTS needs if it is going to
reduce to GR instead of replacing GR with a hidden residual charge.

Current MTS still cannot claim the EH pass, because the q/Obs_e ownership, basic coframe proof, pure vertical split,
zero-flux surface class, and same-frame `M_H_ref` are not all signed.  So 2395 is a conditional theorem plus a retained
EH contamination row, not a public local-GR claim.

## Source Register

| source_id | path | needed_for | needles | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC2395_2394_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2394-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md | EH sector split selected by 2394 | SVL2394_0_EH_local_geometry|epsilon_Qv_EH_kernel_split|NEXT2394_0_selected|VAL2394_OVERALL | false |
| SRC2395_2394_sector_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2394_SECTOR_VARIATION_LEDGER.csv | machine-readable EH sector row | SVL2394_0_EH_local_geometry|MISSING_BASIC_COFRAME_TO_KILL_THETA_EH|MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT | false |
| SRC2395_2394_leak_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2394_QV_PIECE_LEAK_ROWS.csv | EH contamination leak row | epsilon_Qv_EH_kernel_split|MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT|epsilon_Qv_total | false |
| SRC2395_2391_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md | quotient/basic coframe theorem and anti-tautology guard | Q_vis := Phi_parent/V|e_parent = Obs_e o q|DObs_e[Dq(v)] = 0|projection-by-declaration | false |
| SRC2395_2391_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv | q/Obs_e prerequisite statuses | QOC2391_2_presymplectic_null|QOC2391_3_basic_coframe|MISSING_BASIC_COFRAME_PROOF|QOC2391_4_no_projection_declaration | false |
| SRC2395_2390_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md | same-frame chain rule | e_obs(Phi) := Obs_e(q(Phi))|Lie_v e_obs = DObs_e[Dq(v)] = 0|SFL2390_1_vertical_kernel | false |
| SRC2395_2390_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv | same-frame ownership prerequisites | SFC2390_1_Obs_e|SFC2390_2_same_readout|SFC2390_4_no_shadow_frame | false |
| SRC2395_2393_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md | vertical Noether current and Qv contract | J_v := Theta_parent(v_epsilon) - mu_v|J_v = dQ_v + C_v|VQC2393_4_Qv | false |

## EH Kernel Split Theorem

| row_id | claim | statement | derivation_status | consequence | missing_for_current_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EHK2395_0_pure_vertical_definition | pure vertical EH test direction | A pure local vertical vector v_k is a parent tangent with Dq(v_k)=0 and no observed spacetime generator xi at the readout/boundary surface. | DEFINITION_REQUIRED | separates internal quotient-kernel motion from physical GR diffeomorphism charge | parent q, vertical basis, and boundary/readout split are not fully signed | false |
| EHK2395_1_chain_rule_EH_silence | pure vertical leaves observed local geometry fixed | If e_obs(Phi)=Obs_e(q(Phi)) and Dq(v_k)=0, then delta_v e_obs = DObs_e[Dq(v_k)] = 0. | CONDITIONAL_CHAIN_RULE_PROOF | the EH Lagrangian built only from e_obs has no pure-vertical local variation | Obs_e/q ownership and basic coframe proof remain unsigned | false |
| EHK2395_2_theta_EH_zero | EH symplectic potential is zero on pure vertical kernel | For L_EH[e_obs], delta_v L_EH = E_EH dot delta_v e_obs + dTheta_EH(e_obs;delta_v e_obs). If delta_v e_obs=0 pointwise, then Theta_EH(e_obs;v_k)=0. | CONDITIONAL_VARIATION_PROOF | epsilon_theta_EH_kernel_split is killed if the chain-rule hypotheses are signed | basic coframe and pure-vertical split are not current certificates | false |
| EHK2395_3_mu_EH_zero | EH Noether boundary term mu_EH is zero for pure vertical v | Because v_k is not an observed diffeomorphism and delta_v L_EH=0 rather than L_xi L_EH=d(i_xi L_EH), the EH diffeomorphism boundary term mu_xi is not activated. | CONDITIONAL_SPLIT_PROOF | standard GR charge belongs to observed xi, not pure kernel v_k | horizontal observed-diffeomorphism lift and boundary class are not fixed | false |
| EHK2395_4_Qv_EH_zero | pure vertical EH charge vanishes | J_EH[v_k]=Theta_EH(v_k)-mu_EH[v_k]=0, so dQ_EH[v_k]+C_EH[v_k]=0. With zero compact/local boundary flux, choose Q_EH[v_k]=0 as the kernel contribution. | CONDITIONAL_ZERO_CHARGE_PROOF | EH no longer contaminates epsilon_Qv_EH_kernel_split once prerequisites are signed | zero compact flux and boundary/reference convention remain separate locks | false |
| EHK2395_5_observed_xi_reference | observed diffeomorphism EH charge is reference, not kernel | If a parent tangent decomposes as h_xi+k with Dq(k)=0 and h_xi projecting to an observed spacetime diffeomorphism, then Q_EH[h_xi] is the ordinary GR reference charge and must not be counted as Q_v^kernel. | CONDITIONAL_REFERENCE_SPLIT | GR mass/ADM/Komar-like charge can be retained as the baseline while pure vertical residuals are tested separately | horizontal lift h_xi and M_H_ref normalization are not parent-fixed | false |
| EHK2395_6_verdict | EH sector status | 2395 conditionally proves the EH pure-kernel zero, but does not promote a current-MTS EH pass because q/Obs_e, pure vertical split, zero flux, boundary convention, and M_H_ref are not all signed. | CONDITIONAL_EH_ZERO_NOT_PROMOTED | the EH door is now mathematically narrow; the live work moves to signing prerequisites and non-EH sectors | QOC2391_3_basic_coframe;QOC2391_2_presymplectic_null;SFC2390_1_Obs_e;VQC2393_7_MHref | false |

## EH Zero Certificate

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EHC2395_0_q_Obs_e_owned | parent-owned observed coframe | e_obs=Obs_e(q(Phi)) with q and Obs_e fixed before local readout | MISSING_PARENT_Q_OBS_E_OWNERSHIP | epsilon_DObs_e | false |
| EHC2395_1_basic_coframe | basic coframe along vertical fibres | Lie_v e_obs=0 for every pure local vertical v in ker(Dq) | MISSING_BASIC_COFRAME_PROOF | epsilon_Qv_EH_kernel_split | false |
| EHC2395_2_pure_vertical_split | pure vertical vs observed diffeomorphism split | v_k has Dq(v_k)=0 and no observed xi/asymptotic generator; h_xi carries the ordinary GR charge separately | MISSING_KERNEL_VS_OBSERVED_DIFF_SPLIT | epsilon_Qv_EH_kernel_split | false |
| EHC2395_3_boundary_flux | zero compact/local EH flux for pure vertical v | pure vertical v is compact/local or derivative-silent on the charge surface, and boundary/reference terms are assigned to the boundary sector | MISSING_EH_ZERO_FLUX_BOUNDARY_CLASS | epsilon_Qv_boundary | false |
| EHC2395_4_MHref | same-frame positive Hamiltonian reference | M_H_ref is derived from the observed GR reference branch, not imported from orbital fitting | MISSING_POSITIVE_SAME_FRAME_MHREF | all normalized Qv rows remain non-score-ready | false |
| EHC2395_5_EH_conditional_ready | EH kernel-zero theorem readiness | EHC2395_0 through EHC2395_4 pass together | CONDITIONAL_THEOREM_READY_BUT_UNSIGNED | epsilon_Qv_EH_kernel_split_retained | false |

## EH Contamination Rows

| quantity_id | definition | units | formula_or_bound | current_value_status | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| epsilon_Qv_EH_kernel_split | EH/reference charge contamination caused by failing to separate pure vertical kernel motion from observed spacetime diffeomorphism charge | dimensionless after M_H_ref normalization | 0 if EHC2395_0..EHC2395_4 pass; otherwise retain as source row | CONDITIONAL_ZERO_UNSIGNED | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | false |
| epsilon_theta_EH_kernel_split | EH symplectic-potential response to a supposed vertical direction | dimensionless after M_H_ref normalization | ||Theta_EH(e_obs;DObs_e[Dq(v)])||/M_H_ref | MISSING_DOBS_VERTICAL_NORM_AND_MHREF | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | false |
| epsilon_xi_leak | ordinary observed diffeomorphism charge accidentally counted as vertical kernel charge | dimensionless after M_H_ref normalization | Q_EH[h_xi]/M_H_ref if h_xi is not separated from k | MISSING_HORIZONTAL_VERTICAL_SPLIT | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | false |
| epsilon_EH_boundary_flux | pure-vertical EH boundary or reference-improvement flux | dimensionless after M_H_ref normalization | integral_S(delta Q_EH[v_k]-i_v Theta_EH+delta B_EH)/M_H_ref | MISSING_ZERO_FLUX_SURFACE_CLASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2395_0_accept_conditional_EH_zero | accept the conditional EH pure-kernel zero theorem | if e_obs descends through q and v is truly in ker(Dq), the EH local geometry does not move | EH contamination is no longer a conceptual mystery; it is a prerequisite-signature problem | CONDITIONAL_EH_ZERO_ACCEPTED | false |
| DEC2395_1_keep_GR_reference_separate | keep observed GR diffeomorphism charge as reference, not kernel | ordinary EH charge belongs to h_xi, while pure kernel k must carry no observed xi | MTS can reduce to GR without double-counting GR mass as residual kernel charge | REFERENCE_SPLIT_REQUIRED | false |
| DEC2395_2_no_current_promotion | do not claim EH sector pass for current MTS | q/Obs_e ownership, basic coframe, vertical basis, zero flux, and M_H_ref remain unsigned | epsilon_Qv_EH_kernel_split remains nonclaim until certificates close | EH_ZERO_NOT_PROMOTED | false |
| DEC2395_3_next | attack matter/source lift and no-direct-slot proof next | once EH is conditionally separated, the next local-GR danger is hidden source/coupling charge in ordinary matter and worldtube normalization | 2396 should prove matter/source vertical invisibility or keep epsilon_Qv_matter_source live | SELECT_2396_MATTER_SOURCE_LIFT | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2395_0_EH_kernel_zero | EH pure vertical kernel charge zero | CONDITIONAL_BLOCKED | mathematically derived under q/Obs_e and pure-vertical split, but not current-MTS claim-grade | false |
| CG2395_1_total_Qv | total vertical Qv extracted | BLOCKED | non-EH sectors remain unclosed | false |
| CG2395_2_matter_source | matter/source vertical invisibility | BLOCKED | ordinary source/coupling sector remains next root blocker | false |
| CG2395_3_GR_Newton | local GR/Newton reduction | BLOCKED | EH conditional zero is necessary but not sufficient | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2395_0_claim_EH_pass | EH sector is fully passed for current MTS | false | the proof is conditional on unsigned q/Obs_e, pure vertical split, zero flux, and M_H_ref clauses | EHC2395_0_q_Obs_e_owned;EHC2395_1_basic_coframe;EHC2395_2_pure_vertical_split;EHC2395_3_boundary_flux;EHC2395_4_MHref | false |
| REF2395_1_claim_GR_charge_zero | ordinary GR/EH diffeomorphism charge vanishes | false | observed xi charge is the GR reference branch, not the pure vertical kernel branch | EHK2395_5_observed_xi_reference;DEC2395_1_keep_GR_reference_separate | false |
| REF2395_2_claim_local_GR | local GR/Newton is derived from 2395 | false | 2395 only handles the EH door conditionally; matter, extra, projector, boundary, coupling, PPN, and Newtonian-limit gates remain | CG2395_1_total_Qv;CG2395_2_matter_source;CG2395_3_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2395_0_selected | 2396-Y5-R2FR-matter-source-lift-and-no-direct-slot-proof-or-source-charge-row.md | prove S_matter descends through q/Obs_e, vertical v does not move matter representation/source slots, and matter/source Qv is constraint-only | retain epsilon_Qv_matter_source, epsilon_hidden_source_slot, and M_H_ref source rows as nonclaim | false |
| NEXT2395_1_parallel | 2396b-Y5-R2FR-basic-coframe-vertical-basis-signature-or-DObsE-bound.md | sign parent q/Obs_e and Lie_v e_obs=0 for the actual local vertical basis | keep epsilon_DObs_e and epsilon_Qv_EH_kernel_split as finite bound/source rows | false |
| NEXT2395_2_later | 2396c-Y5-R2FR-MHref-reference-normalization-and-EH-boundary-class.md | fix GR reference charge, positive M_H_ref, and compact/local zero-flux boundary class | retain epsilon_EH_boundary_flux and all normalized rows as non-score-ready | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2395_00_sources_exist | PASS | all required source paths exist | false |
| VAL2395_01_needles_found | PASS | all source needles found | false |
| VAL2395_02_chain_rule_present | PASS | EH chain-rule kernel silence is present | false |
| VAL2395_03_theta_Qv_zero_present | PASS | conditional Theta_EH and Q_EH zero statements are present | false |
| VAL2395_04_observed_xi_guard_present | PASS | observed diffeomorphism reference-charge guard is present | false |
| VAL2395_05_required_gaps_explicit | PASS | q/Obs_e, basic coframe, pure split, zero flux, and M_H_ref gaps explicit | false |
| VAL2395_06_contamination_rows_nonready | PASS | EH contamination rows remain nonclaim/nonready | false |
| VAL2395_07_global_claims_blocked | PASS | EH pass, total Qv, matter/source, and GR/Newton gates not promoted | false |
| VAL2395_08_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2395_09_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2395_10_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2395_11_next_selected | PASS | matter/source lift and no-direct-slot proof selected next | false |
| VAL2395_OVERALL | PASS | 2395 conditionally proves the EH pure-vertical kernel zero, separates observed GR charge as reference, refuses current-MTS promotion, and selects matter/source lift next | false |

## Practical Status

This is a net improvement.  The EH door is no longer vague: if `e_obs` is quotient-basic and `v` is truly pure
vertical, EH contributes no kernel charge.  That means the local-GR route is not obviously dead at the EH level.
The next danger is less forgiving: matter/source/coupling.  If ordinary matter has a hidden direct slot, source
prefactor, or representation marker outside q/Obs_e, the local branch leaks even if EH behaves perfectly.
