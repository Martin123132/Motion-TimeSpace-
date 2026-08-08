# 2396 — Matter Source Lift And No Direct Slot Proof Or Source Charge Row

## Result

2396 turns the matter/source problem into a clean sufficient theorem plus a sharp coupling obstruction.

The safe matter action shape is

`S_matter = sum_A int L_A(e_obs(q(Phi)), psi_A, D_omega[e_obs(q)] psi_A; theta_A) + dB_A`.

For a pure vertical `v in ker(Dq)`,

`delta_v S_matter = G_e[v] + G_psi[v] + G_theta[v] + G_direct[v] + G_W[v] + G_B[v] + G_nonHilbert[v]`.

If `e_obs` and `omega_obs` descend through `q`, matter fields and constants have a fixed lift, the worldtube is the
Hilbert support selected before readout, and the parent grammar forbids direct residual matter/source slots, then all
terms vanish or reduce to ordinary constraints.  In that case

`Theta_matter(v)-mu_matter[v]` carries no physical vertical kernel charge, so conditionally `Q_v^matter=0`.

The catch is the important bit: current MTS does not yet forbid the dangerous coupling forms

`V_m[X,rho_A,W_source,C_top]`, `A_A(X)L_A`, `A(X)J_H`, source-only prefactors, species-frame factors, or material
markers outside `q/Obs_e`.

So the matter/source theorem is exact as a route, but not claim-grade yet.  The coupling/no-direct-slot grammar is now
the root bottleneck.

## Source Register

| source_id | path | needed_for | needles | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC2396_2395_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2395-Y5-R2FR-EH-local-geometry-kernel-split-or-EH-contamination-row.md | 2395 selected matter/source lift next | NEXT2395_0_selected|matter/source lift|hidden source/coupling charge|VAL2395_OVERALL | false |
| SRC2396_2389_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md | observed-frame matter action and Hilbert current grammar | S_m[Phi,psi_m]|delta L_m = E_m delta psi_m|J_H[tau]|MCD2389_3_vertical_descent_zero | false |
| SRC2396_2389_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2389_CURRENT_OWNER_CERTIFICATE.csv | matter/source ownership blockers | OCC2389_2_Lm_density|OCC2389_4_matter_lift|OCC2389_5_no_direct_slots|OCC2389_7_MHref | false |
| SRC2396_2389_leaks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2389_JH_OWNER_LEAK_VALUES.csv | matter/source residual rows | epsilon_hidden_source_slot|epsilon_marker_matter_lift|Delta_JH_owner_total_over_MH | false |
| SRC2396_1760_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md | matter/worldtube quotient descent theorem and A_matter interface | MWD1760_1_conditional_theorem|CR1760_6_direct_vertex|PRE1760_4_no_shadow_prefactor|AM1760_8_A_matter | false |
| SRC2396_1771_sector_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1771_SECTOR_ACTION_VARIATION_LEDGER.csv | nonminimal coupling sector warning | SAV1771_3_nonminimal|S_nonmin = int sqrt(-g)|A(X)J_m|MUST_CLASSIFY_NOT_FORBIDDEN | false |
| SRC2396_2394_sector_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2394_SECTOR_VARIATION_LEDGER.csv | matter/source sector in total Qv split | SVL2394_1_matter_source|MISSING_MATTER_THETA_DESCENT|MISSING_SOURCE_CONSTRAINT_CHARGE_SPLIT | false |
| SRC2396_2390_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2390_SAME_FRAME_CERTIFICATE.csv | same-frame matter/readout requirements | SFC2390_2_same_readout|SFC2390_4_no_shadow_frame|SFC2390_5_projector_support | false |

## Matter Source Lift Theorem

| row_id | claim | statement | derivation_status | consequence | missing_for_current_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MSL2396_0_matter_action_grammar | ordinary matter must be an observed-frame quotient functor | Use S_matter=sum_A int L_A(e_obs(q(Phi)),psi_A,D_omega[e_obs(q)]psi_A;theta_A)+dB_A, with no independent residual/source/worldtube slot. | CONDITIONAL_GR_COMPATIBLE_GRAMMAR | matter sees the same geometry as GR and cannot source the vertical residual except through q | explicit parent L_m densities and q/Obs_e ownership remain unsigned | false |
| MSL2396_1_vertical_variation_decomposition | vertical matter variation decomposes into named leak channels | delta_v S_matter = G_e[v]+G_psi[v]+G_theta[v]+G_direct[v]+G_W[v]+G_B[v]+G_nonHilbert[v]. | DECOMPOSITION_CONTRACT | no hidden matter-source term can disappear without being assigned to a channel | component values and common normalization are not supplied | false |
| MSL2396_2_geometry_chain_zero | geometry part vanishes for pure vertical v | If Dq(v)=0 and e_obs=Obs_e(q(Phi)), then G_e[v]=int T_a wedge delta_v e_obs^a=0; connection terms vanish when omega_obs is built from e_obs. | CONDITIONAL_CHAIN_RULE_PROOF | matter does not feel residual vertical motion through the metric/coframe channel | basic coframe, connection descent, and same-frame readout are unsigned | false |
| MSL2396_3_lift_and_constants_zero | matter lift and constants carry no vertical marker | If delta_v psi_A=0 up to owned gauge/local-Lorentz transformations, and delta_v theta_A=0 for representation constants/material standards, then G_psi[v]+G_theta[v]=0 modulo ordinary constraints. | CONDITIONAL_LIFT_PROOF | vertical residuals cannot hide as material labels, species standards, or changing constants | matter lift/no-marker and constant-superselection signatures remain unsigned | false |
| MSL2396_4_no_direct_slot_zero | direct matter/source coupling is forbidden | If the parent grammar forbids V_m[X,rho_A,W_source,C_top], A_A(X)L_A, A(X)J_H, species-frame factors, and source-only prefactors outside q/Obs_e, then G_direct[v]=0. | CONDITIONAL_NO_SLOT_THEOREM | this is the coupling choke point: without it, matter can reintroduce a fifth-force/source charge while looking GR-like | no-direct-slot/coupling grammar is not parent-derived | false |
| MSL2396_5_worldtube_support_zero | source worldtube descends through Hilbert support | If W_source=closure(supp J_H[tau]) with J_H and tau derived before readout from the same e_obs branch, then delta_v W_source=0 for regular compact sources. | CONDITIONAL_SUPPORT_PROOF | source support cannot be retuned to absorb residual fields | support regularity, tau ownership, projector descent, and tail bounds remain unsigned | false |
| MSL2396_6_Qv_matter_zero | matter/source vertical Qv is constraint-only or zero | When MSL2396_0 through MSL2396_5 hold and boundary terms are silent, Theta_matter(v)-mu_matter[v] contributes no physical vertical kernel charge, so Q_v^matter=0 up to ordinary constraints. | CONDITIONAL_MATTER_QV_ZERO | the matter/source door can close without fitting if the coupling grammar is signed | boundary, source support, no-direct-slot, and M_H_ref clauses are not signed | false |
| MSL2396_7_verdict | matter/source sector status | 2396 gives the exact sufficient theorem for matter/source invisibility, but current MTS does not pass because the no-direct coupling/source slot, matter lift, worldtube support, and M_H_ref remain unsigned. | CONDITIONAL_ROUTE_EXACT_NOT_PROMOTED | the next bottleneck is the parent coupling/no-direct-slot grammar, not more vague source language | OCC2389_4_matter_lift;OCC2389_5_no_direct_slots;SAV1771_3_nonminimal;OCC2389_7_MHref | false |

## Matter Zero Certificate

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MSC2396_0_Lm_density | explicit observed-frame matter Lagrangian density | L_A(e_obs,psi_A,Dpsi_A;theta_A) is written and varied before readout | MISSING_EXPLICIT_LM_DENSITY | epsilon_JH_owner | false |
| MSC2396_1_q_eobs_connection | q/e_obs/omega descent | e_obs and omega_obs are functors of q(Phi), so Dq(v)=0 kills geometry and connection variation | MISSING_Q_EOBS_CONNECTION_DESCENT | A_geom_matter | false |
| MSC2396_2_matter_lift | matter lift/no-marker proof | vertical v does not independently move psi_A, constants, species labels, material standards, or representation data | MISSING_MATTER_LIFT_NO_MARKER_PROOF | epsilon_marker_matter_lift | false |
| MSC2396_3_no_direct_slot | no direct residual matter/source coupling | forbid V_m[X,rho_A,W_source,C_top], A_A(X)L_A, A(X)J_H, source prefactors, and shadow species frames outside q/Obs_e | MISSING_NO_DIRECT_SLOT_GRAMMAR | epsilon_hidden_source_slot | false |
| MSC2396_4_worldtube_support | Hilbert worldtube support owner | W_source is closure(supp J_H[tau]) with compact/regular support, not an after-fit mask | MISSING_SUPPORT_OR_TAIL_THEOREM | epsilon_support_tail | false |
| MSC2396_5_boundary | matter/source boundary silence | matter boundary/worldtube exact terms are zero, proper, compact-support silent, or explicitly bounded | MISSING_MATTER_BOUNDARY_NOFLUX_OR_BOUND | A_boundary_matter | false |
| MSC2396_6_MHref | positive same-frame M_H_ref | normalize source and charge rows by the same parent Hilbert/GR reference branch | MISSING_POSITIVE_MHREF | all normalized source rows remain non-score-ready | false |
| MSC2396_7_matter_zero_ready | matter/source vertical zero theorem readiness | MSC2396_0 through MSC2396_6 pass together | CONDITIONAL_THEOREM_READY_BUT_UNSIGNED | epsilon_Qv_matter_source_retained | false |

## Source Charge Rows

| quantity_id | definition | units | formula_or_bound | current_value_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| epsilon_Qv_matter_source | matter/source contribution to vertical kernel charge | dimensionless after M_H_ref normalization | 0 if MSC2396_0..MSC2396_6 pass; otherwise retained as source-charge row | CONDITIONAL_ZERO_UNSIGNED | false |
| epsilon_hidden_source_slot | direct residual coupling to matter/source/worldtube slot | dimensionless after M_H_ref normalization | abs(partial_X V_m[X,rho_A,W_source,C_top]|_{X=0})/M_H_ref | MISSING_NO_DIRECT_SLOT_PROOF | false |
| epsilon_nonminimal_coupling_slot | A_A(X)L_A, A(X)J_H, species-frame, or source-prefactor coupling leak | dimensionless after M_H_ref normalization | ||delta_X S_nonmin||/M_H_ref | MISSING_COUPLING_GRAMMAR_OR_BOUND | false |
| epsilon_marker_matter_lift | vertical movement of matter representation data, constants, species labels, or material standards | dimensionless after M_H_ref normalization | abs(delta_v psi_A contribution + delta_v theta_A contribution + marker terms)/M_H_ref | MISSING_MATTER_LIFT_NO_MARKER_PROOF | false |
| epsilon_support_tail | worldtube support/readout-tail contribution to source charge | dimensionless after M_H_ref normalization | ||delta_v W_source or exterior Hilbert tail||/M_H_ref | MISSING_SUPPORT_OR_TAIL_THEOREM | false |
| Delta_matter_source_total_over_MH | total unclosed matter/source vertical charge channel | dimensionless | epsilon_Qv_matter_source + epsilon_hidden_source_slot + epsilon_nonminimal_coupling_slot + epsilon_marker_matter_lift + epsilon_support_tail | COMPONENTS_MISSING | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2396_0_accept_conditional_matter_zero | accept quotient-only observed-frame matter as the clean local-GR route | if matter only sees e_obs(q) and fixed representation data, vertical residuals do not source ordinary matter | the matter problem becomes a parent grammar/coupling-signature problem | CONDITIONAL_MATTER_ZERO_ACCEPTED | false |
| DEC2396_1_coupling_is_root_bottleneck | treat no-direct coupling/source slot as the next root bottleneck | A(X)L_m, A(X)J_H, source-prefactors, or species frames would defeat the vertical zero while looking like ordinary matter | do not bury coupling inside generic matter prose | COUPLING_SLOT_HUNT_SELECTED | false |
| DEC2396_2_no_current_promotion | do not claim matter/source pass for current MTS | L_m, lift, no-direct-slot, support, boundary, and M_H_ref certificates are unsigned | epsilon_Qv_matter_source and coupling leak rows remain nonclaim | MATTER_ZERO_NOT_PROMOTED | false |
| DEC2396_3_next | attack no-direct matter coupling grammar next | this is the smallest decisive clause that can close or expose the coupling leak | 2397 should forbid direct residual matter/source slots or convert them into sourced bound rows | SELECT_2397_NO_DIRECT_COUPLING_GRAMMAR | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2396_0_matter_source_zero | matter/source vertical Qv zero | CONDITIONAL_BLOCKED | the theorem is exact if clauses pass, but current MTS has not signed them | false |
| CG2396_1_no_direct_coupling | no direct residual matter/source coupling | BLOCKED | coupling leak remains live | false |
| CG2396_2_total_Qv | total vertical Qv extracted | BLOCKED | extra/projector/boundary/coupling sectors remain unclosed | false |
| CG2396_3_GR_Newton | local GR/Newton reduction | BLOCKED | matter/source zero is necessary but not sufficient | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2396_0_claim_matter_zero | matter/source vertical charge vanishes for current MTS | false | the proof requires unsigned L_m, q/e_obs, matter lift, no-direct-slot, support, boundary, and M_H_ref clauses | MSC2396_0_Lm_density;MSC2396_2_matter_lift;MSC2396_3_no_direct_slot;MSC2396_4_worldtube_support;MSC2396_6_MHref | false |
| REF2396_1_claim_no_coupling_leak | there is no hidden matter/source coupling leak | false | S_nonmin, A(X)L_m, A(X)J_H, source prefactors, and species frames are not forbidden by a parent grammar yet | MSC2396_3_no_direct_slot;epsilon_nonminimal_coupling_slot | false |
| REF2396_2_claim_local_GR | local GR/Newton is derived from 2396 | false | 2396 only handles the matter/source sufficient theorem conditionally; total Qv, PPN, Newtonian limit, projector, boundary, and extra sectors remain | CG2396_2_total_Qv;CG2396_3_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2396_0_selected | 2397-Y5-R2FR-no-direct-matter-coupling-grammar-or-coupling-charge-row.md | prove the parent action grammar forbids A(X)L_m, A(X)J_H, species-frame factors, source-prefactors, material markers, and V_m[X,rho_A,W_source] | retain epsilon_nonminimal_coupling_slot and epsilon_hidden_source_slot as sourced nonclaim bound rows | false |
| NEXT2396_1_parallel | 2397b-Y5-R2FR-explicit-standard-matter-Lm-sidecar-and-variation-conventions.md | write explicit dust/scalar/EM matter sidecar Lagrangians and variation conventions in the observed frame | keep epsilon_JH_owner non-score-ready | false |
| NEXT2396_2_later | 2397c-Y5-R2FR-worldtube-support-tail-and-MHref-source-normalization.md | derive W_source, support compactness/tails, tau, and positive M_H_ref from one parent branch | retain epsilon_support_tail and all normalized source rows as non-score-ready | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2396_00_sources_exist | PASS | all required source paths exist | false |
| VAL2396_01_needles_found | PASS | all source needles found | false |
| VAL2396_02_action_grammar_present | PASS | observed-frame quotient matter action grammar is present | false |
| VAL2396_03_variation_decomposition_present | PASS | vertical matter variation is decomposed into leak channels | false |
| VAL2396_04_no_direct_coupling_guard_present | PASS | direct coupling/source-prefactor guard is present | false |
| VAL2396_05_matter_Qv_zero_present | PASS | conditional matter/source Qv zero statement is present | false |
| VAL2396_06_required_gaps_explicit | PASS | Lm, q/eobs, lift, no-direct-slot, support, and M_H_ref gaps explicit | false |
| VAL2396_07_source_charge_rows_nonready | PASS | matter/source charge rows remain nonclaim/nonready | false |
| VAL2396_08_global_claims_blocked | PASS | matter/source, coupling, total Qv, and GR/Newton gates not promoted | false |
| VAL2396_09_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2396_10_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2396_11_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2396_12_next_selected | PASS | no-direct matter coupling grammar selected next | false |
| VAL2396_OVERALL | PASS | 2396 states the exact matter/source vertical-zero theorem, isolates the no-direct coupling slot as root bottleneck, refuses promotion, and selects coupling grammar next | false |

## Practical Status

This is where the theory is now most honestly exposed.  EH can be made silent by quotient geometry.  Matter can also
be made silent, but only if the coupling grammar is strict enough.  If the parent action allows even one source-only
prefactor or residual matter vertex, local GR does not follow; it becomes a finite coupling/source-charge residual
that must be bounded.  The next move is therefore exactly the coupling hunt.
