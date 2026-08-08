# 3248 - q-Basic Local Collar Source or First Poynting Arena Row Fill under AX1090

Generated: `2026-06-27T04:15:01.899272+00:00`

Status: `Y5_R2FR_3248_qbasic_geodesic_collar_formula_partially_fills_Poynting_arena_row_Wsource_unsigned_nonclaim`

Claim ceiling: `collar_formula_only_no_parent_Wsource_no_numeric_Poynting_score_no_amplitude_score_no_local_GR_claim`

## Summary

- `3248` makes the constructive move: define the local collar from the Hilbert source support, `W_source=closure(supp J_H[tau])`, and the public metric distance `rho_pub=dist_gpub(x,W_source)`.

- This gives explicit candidate boundary functions: `s_i=rho_pub^2-r_i^2`, `S_i={s_i=0}`, `A_ext[r1,r2]={r1<=rho_pub<=r2}`, and `chi_B=eta((rho_pub-r1)/(r2-r1))`.

- If `W_source`, `g_pub`, `e_obs`, `tau`, radii and regularity all descend through `q`, the collar, frame `u`, and normal `n` are fixed under vertical response directions by chain rule.

- Current MTS still cannot claim the row because `W_source/J_H/tau/e_obs/r1/r2/regularity` are not parent-signed, and the Poynting flux constants/norms remain missing.

- The first Poynting arena row is partially filled with formulas rather than blanks, while `valid_for_claim=false` stays locked.

## q-Basic Collar Construction Attempt

| collar_id | object | candidate_formula | qbasic_condition | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COL3248_0_worldtube_selector | source worldtube | W_source := closure(supp J_H[tau]) | J_H, tau, e_obs and support topology are parent-owned q-basic objects | CONDITIONAL_SELECTOR_FROM_1016_NOT_PARENT_SIGNED | false |
| COL3248_1_distance_function | public metric distance to W_source | rho_pub(x) := dist_{g_pub(q)}(x,W_source) | g_pub and W_source descend through q; use a normal tubular neighbourhood avoiding cut locus/caustics | CONDITIONAL_GEOMETRIC_CONSTRUCTION | false |
| COL3248_2_boundary_levels | boundary level functions | s_i(x) := rho_pub(x)^2-r_i^2, S_i := {s_i=0}, A_ext[r1,r2] := {r1<=rho_pub<=r2} | r1,r2 fixed before readout; grad s_i non-null/spacelike as required; orientation fixed | FORMULA_FILLED_INPUTS_UNSIGNED | false |
| COL3248_3_smooth_collar | collar cutoff | chi_B(x) := eta((rho_pub(x)-r1)/(r2-r1)) with eta fixed once | eta,r1,r2 fixed constants and rho_pub q-basic | FORMULA_FILLED_INPUTS_UNSIGNED | false |
| COL3248_4_frame_normal | observed frame and normal | u := clock leg of e_obs(q); n_i := grad_i s_i / sqrt(\|g_pub^{ab} grad_a s_i grad_b s_i\|) | e_obs=Obs_e(q), g_pub=q-owned, non-null boundary, common orientation | FORMULA_FILLED_INPUTS_UNSIGNED | false |

## Collar q-Basic Chain-Rule Theorem

| theorem_id | statement | proof | current_status | claim_allowed |
| --- | --- | --- | --- | --- |
| THM3248_0_chain_rule | If W_source, g_pub, r_i and eta are q-basic, then s_i, chi_B, u and n are fixed by any vertical response direction e_A. | D_A rho_pub = D rho_pub[Dq(e_A)] plus source-support variation; both vanish when g_pub and W_source descend through q. Then D_A s_i=D_A chi_B=D_A u=D_A n=0, away from nonregular boundary points. | EXACT_CONDITIONAL_THEOREM | false |
| THM3248_1_regular_tube | The geodesic collar is legal only inside a regular tubular neighbourhood of W_source. | Distance to a submanifold/support can fail at cut loci, caustics, null boundaries or nonsmooth support; those defects must be excluded or bounded. | DOMAIN_GUARD_REQUIRED | false |
| THM3248_2_not_numeric | The formula partially fills the score row but does not make it numeric or claim-grade. | The corpus still lacks parent-signed W_source, J_H/tau, r1/r2, non-null guard, flux regime, C_flux/C_coll, flux norms, and e_A trace norm. | PARTIAL_FILL_ONLY | false |

## First Poynting Arena Row Partial Fill

| arena_row_id | boundary_id | surface_class | s_B | chi_B | frame_u | normal_n | filled_fields | still_missing | computed_J_Poynting_bound | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ARENA3248_0_qbasic_geodesic_collar_partial_fill | qbasic_geodesic_collar_Wsource_r1_r2_CONDITIONAL | A_ext[r1,r2]={x:r1<=dist_gpub(x,W_source)<=r2}; S_i={dist_gpub^2-r_i^2=0} | s_i(x)=dist_gpub(x,W_source)^2-r_i^2 | chi_B(x)=eta((dist_gpub(x,W_source)-r1)/(r2-r1)) | u=e_obs_clock_leg(q) | n=normalize_gpub(grad s_i) | boundary_id;surface_class;s_B;chi_B;frame_u;normal_n | parent-signed W_source;J_H;tau;e_obs selector;r1;r2;eta;non-null regularity;orientation;flux regime;C_flux;C_coll;flux norms;eA trace norm;units | NOT_COMPUTED | PARTIAL_FORMULA_FILL_NONCLAIM | false |
| ARENA3248_1_source_worldtube_finite_bound | source_worldtube_Wsource_CONDITIONAL | material/Hilbert source support worldtube boundary | support boundary of J_H[tau] if regular | source-support mask chi_source from parent Hilbert support | MISSING_same_frame_source_u | MISSING_worldtube_normal | surface_class;s_B_template;chi_B_template | same-frame source support;worldtube regularity;normal;flux norm;source measure glue | NOT_COMPUTED | FINITE_BOUND_FALLBACK_NONCLAIM | false |

## Collar Missing Signatures

| missing_id | field | needed_signature | current_evidence | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| MISS3248_0_Wsource | W_source | parent-owned compact Hilbert source worldtube W_source=closure(supp J_H[tau]) | 1016 writes exact selector contract but current MTS claim fails | boundary_id claim; source-worldtube finite-bound claim | false |
| MISS3248_1_JH_tau_eobs | J_H;tau;e_obs | same observed coframe/time generator/source current before readout | 3136 and 2600 provide conditional coframe/clock/tau routes; not parent-signed | frame_u claim and source support | false |
| MISS3248_2_radii_regular | r1;r2;regularity | fixed radii, regular tubular neighbourhood, non-null boundaries, orientation | no source-backed local collar radii/regularity row found in inspected sources | normal_n and C_flux trace norm | false |
| MISS3248_3_flux_inputs | flux constants and norms | C_flux,C_coll,\|\|T_EM(u,n)\|\|,\|\|e_A\|\| trace norm, units | 3234 supplies formulas but marks inputs missing | computed_J_Poynting_bound | false |

## Score Row Update

| score_update_id | score_id | previous_status | new_partial_fields | not_filled | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SCU3248_0_PJS3246 | PJS3246_0_first_component | MISSING_PARENT_BOUNDARY_ID and MISSING_BOUNDARY_COLLAR_WORLDTUBE_CLASS | boundary_id=qbasic_geodesic_collar_Wsource_r1_r2_CONDITIONAL; surface_class=A_ext[r1,r2]; frame_u=e_obs_clock_leg(q); normal_n=normalize(grad s_i) | source-backed W_source,r1,r2,regularity,flux constants,norms,units | schema improves from blank boundary to conditional collar formula; valid_for_claim remains false | false |

## Claim Gates

| claim_gate_id | claim | condition_passed | status | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3248_0_collar_formula | q-basic collar formula exists | true | geodesic/source-support formula written | false |
| CG3248_1_current_boundary | current MTS owns q-basic collar boundary | false | W_source/J_H/tau/e_obs/radii/regularity not parent-signed | false |
| CG3248_2_score_numeric | Poynting Jtot row is numeric/source-backed | false | flux constants/norms/eA units still missing | false |
| CG3248_3_local_GR | local GR/Newton/PPN reduction | false | no numeric qloc/amplitude residual | false |

## Decision Ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC3248_0_partial_fill | Use the Hilbert-source geodesic collar as the best q-basic collar candidate. | It is derived from public metric distance and parent source support, so it is the least post-hoc boundary choice if its premises close. | Attack W_source/J_H/tau/e_obs ownership rather than inventing a radius. |
| DEC3248_1_no_claim | Do not promote the collar or Poynting score row. | The source support and regularity inputs are still unsigned and flux inputs are absent. | Keep the row as partial formula fill, nonclaim. |
| DEC3248_2_fallback | Keep source-worldtube finite-bound row as the fallback. | If the q-basic exterior collar cannot be signed, physical source-worldtube flux must be bounded rather than erased. | Build a source-worldtube selector/fill row next. |

## Next Target

| next_id | priority | next_doc | next_script | objective | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3248_0_3249 | selected_primary | 3249-Y5-R2FR-Wsource-JH-tau-eobs-selector-or-source-worldtube-Poynting-bound-row-under-AX1090.md | scripts/Y5_R2FR_3249_Wsource_JH_tau_eobs_selector_or_source_worldtube_Poynting_bound_row.py | Try to parent-sign or source W_source=closure(supp J_H[tau]), the same observed coframe/time generator, and the source support regularity needed for the q-basic collar; if not, fill the source-worldtube finite-bound row explicitly as nonclaim. | do not choose radii after seeing flux; do not claim measured-GM/source glue; do not edit formalization-workbench | false |

## Source Register

| source_id | source_path | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3248_3247 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3247-Y5-R2FR-parent-owned-boundary-frame-certificate-or-Poynting-arena-source-row-under-AX1090.md | true | true | immediate q-basic collar handoff | L11:- `3247` derives the clean boundary/frame theorem: if the local boundary/collar is q-basic, `B={s_B(q)=0}` or `chi_B(q)`, and `e_obs=Obs_e(q)`, then every vertical response direction with `Dq[e_A]=0` fixes `B`, `u`, and  \| L15:- Current MTS still does not get a numeric Poynting row because the actual `s_B/chi_B`, non-null normal guard, orientation/collar support, and observed-frame selector are not parent-signed. \| L25:\| BFC3247_0_boundary_definition \| q-basic local boundary/collar \| Let B be the level set s_B(q(Phi))=0 or support collar chi_B(q(Phi)) chosen before source/readout. \| For a response vertical e_A with Dq[e_A]=0, D_A s_B(q \| L27:\| BFC3247_2_normal_definition \| boundary normal n \| Let n_mu = grad_mu s_B / sqrt(\\|g_pub^{ab} grad_a s_B grad_b s_B\\|) on a non-null q-basic boundary. \| If g_pub and s_B descend through q, then D_A n=0 except at caustic | false |
| SRC3248_1016_selector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md | true | true | parent worldtube support selector contract | L3:**Status:** The legal selector contract is now explicit: `W_source = closure(supp J_H[tau])` is a valid pre-readout source worldtube only if the parent action owns `J_H`, `e_obs`, `tau`, compact support, linking surfaces \| L5:**Claim ceiling:** no parent selector, source-measure equality, `R_eq` score, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1016. \| L26:\| contract_id \| required_clause \| mathematical_form \| current_status \| failure_if_missing \| valid_for_claim \| \| L31:\| PSC1016_3_support_selector \| compact source worldtube is selected by Hilbert source support, not by fitted mass radius \| W_source := closure(supp J_H[tau]); S1,S2 link W_source in the source-free exterior \| formal_sele | false |
| SRC3248_1015_same_object | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md | true | true | same compact Hilbert source worldtube lemma | L3:**Status:** The exact same-object lemma is now written: a fixed compact Hilbert source worldtube plus a Poincare-dual topological representative would give `Pi_M J_H = J_M_top + dB_zero` when the residual class `R_eq` an \| L5:**Claim ceiling:** no topological-Hilbert equality, closed Hilbert flux, measured-GM closure, Newton/GR reduction, R10/R11 pass, PPN pass, or local-GR claim is allowed from 1015. \| L18:\| SRC1015_8_hwt_attempt \| source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv \| true \| true \| Hilbert worldtube glue theorem attempt. \| \| L19:\| SRC1015_9_hwt_certificate \| source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv \| true \| true \| Hilbert worldtube certificate gaps. \| | false |
| SRC3248_1150_glue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md | true | true | Hilbert-worldtube glue status | L1:# 1150 - Y5/R10 Hilbert-Worldtube Glue or PiM Equality-Commutator First Row \| L3:**Current verdict:** Hilbert/worldtube glue is not derived for current MTS. The exact contract exists, but the worldtube source, Hilbert-PiM charge map, topological boundary match, exact/reference zero, PiM commutator, p \| L16:\| SRC1150_0_1149_next \| source-intake/mts_residuals/P8_Y5_R10_1149_NEXT_TARGET.csv \| true \| NEXT1149_0_1150 \| true \| handoff requiring Hilbert/worldtube glue or first PiM equality/commutator row. \| \| L17:\| SRC1150_1_1149_lemma \| source-intake/mts_residuals/P8_Y5_R10_1149_SOURCE_OWNER_MINIMAL_LEMMA_ATTEMPT.csv \| true \| LEM1149_6_worldtube_glue \| true \| minimal source-owner lemma leaves worldtube glue open. \| | false |
| SRC3248_worldtube_clauses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv | true | true | worldtube/exterior annulus clauses | L2:W504_0_worldtube_setup,compact source is represented by a worldtube W and the test region is an exterior annulus A with boundaries S1 and S2 linking W,A = exterior(W) between S1 and S2; no source support in A,definition  \| L5:W504_3_exterior_closure_equation,radial independence follows if the parent charge form is closed in the compact exterior,dQ_M[τ] = C_EH + C_extra + C_projector + C_boundary + C_Lambda_sub = 0 in A,"vacuum exterior equati \| L6:W504_4_worldtube_source_measure_glue,the worldtube source measure and the exterior Noether charge must read the same mass,M_source[W] = integral_S Q_M[τ] = M_eff before orbital fitting,interior-to-exterior matching or Ga \| L7:W504_5_calibration_and_limits,the charge must reduce to GR/Poisson/Newton in the local weak-field limit,Q_M[τ] -> Komar/ADM/Gauss mass charge; ∇²Φ = 4πGρ; exterior ∇²Φ = 0,"normalization of G_ref, τ, and weak-field metri | false |
| SRC3248_worldtube_measure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | true | true | worldtube source measure theorem | L2:T510_0_EH_reference_glue,"In an EH plus minimally coupled matter parent theory, the on-shell diffeomorphism Noether current gives a closed exterior surface charge; the difference between two linking surfaces is the Hamil \| L3:T510_1_worldtube_source_measure,"A worldtube source measure equals the exterior mass charge only when it is defined as the dressed Hamiltonian/Noether source charge, not as bare rest-matter mass.",M_source[W] := H_tau[ou \| L4:T510_2_MTS_transfer_condition,"MTS inherits the EH worldtube glue only if its local exterior fixed point has the EH symplectic charge, one observed source frame, constant kappa, silent extra sectors, and a fixed Pi_M pro \| L5:T510_3_Newton_PPN_readout,"Even after worldtube glue, local GR needs the same charge to control the 1/r metric coefficient and the second-order PPN terms.","g_00=-1+2G_ref M_source/r + O(r^-2); g_ij=(1+2 gamma G_ref M_so | false |
| SRC3248_hwg_certificate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv | true | true | Hilbert worldtube certificate gaps | L2:HWG535_0_worldtube_fixed_before_readout,compact Hilbert source worldtube is selected by parent structure before orbital readout,"W_source subset M fixed by parent source/support/topology, not by fitted mu_obs",missing_ce \| L3:HWG535_1_source_measure_owned,the measure used to define Q_M is the same observed Hilbert source measure,Q_M=int_W rho_H dV_H with dV_H owned by e_obs/source variation,missing_certificate,false \| L4:HWG535_2_topological_representative_matches_worldtube_boundary,omega_M_top represents the boundary class of the same Hilbert source worldtube,int_boundary(W_source) omega_M_top=1 and no independent topological label,miss \| L5:HWG535_3_exact_term_zero,the exact difference term has zero compact boundary integral,Pi_M J_H-J_M_top=dB_zero and int_boundary dB_zero=0,missing_certificate_or_bound,false | false |
| SRC3248_hsm_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | true | true | Hamiltonian source measure contract | L3:HSM541_1_integrable_charge,"Hamiltonian charge has fixed reference, fixed time generator, and integrable variation","delta H_tau = int_S(delta Q_tau - i_tau theta), reference fixed once",not_derived_for_current_MTS,Delta \| L4:HSM541_2_observed_worldtube_source,worldtube source measure is fixed by the same observed Hilbert source current before readout,W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref,not_derived,frame/source-measure resid \| L7:HSM541_5_Gauss_orbital_readout,same charge controls Poisson/Gauss surface integral and pure inverse-square orbital acceleration,nabla^2 Phi=4*pi*G_ref*rho_H; a_r=-G_ref*M_source/r^2,not_derived,"Delta_cal, radial hair, a | false |
| SRC3248_3136_coframe | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md | true | true | observed coframe/clock selector | L1:# 3136 - Observed-Coframe Clock Functional Owner under AX1090 \| L3:Private checkpoint. This follows 3135 by trying to derive the clock readout functional instead of merely declaring that it is missing. \| L7:3136 proves the clean conditional clock theorem: \| L10:ordinary clock matter descends to the observed coframe | false |
| SRC3248_3234_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md | true | true | Poynting flux formula needing B,u,n | L13::= int_B w_perp T_EM(u,n) dSigma \| L22::= C_flux \|\|S_EM dot n\|\|_B + B_corner_flux. \| L28:J_Poynting_bound <= C_coll \|\|T_EM(u,n)\|\|_collar. \| L43:F^2=0 does not imply S_EM dot n=0 or T_EM(u,n)=0. | false |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3248_0_sources_exist | true | all cited source paths exist | True |
| VAL3248_1_source_hits | true | source evidence hits are present | True |
| VAL3248_2_csvs_parse | true | all generated CSV files parse | True |
| VAL3248_3_outputs_under_post_checkpoint | true | all outputs are under post-checkpoint-work | True |
| VAL3248_4_formalization_clean | true | no 3248 outputs in formalization-workbench | formalization_3248_count=0 |
| VAL3248_5_formula_filled | true | q-basic collar formula row was written | True |
| VAL3248_6_missing_retained | true | missing signatures remain explicit and nonclaim | True |
| VAL3248_7_claims_blocked | true | all claim gates remain blocked | True |
| VAL3248_8_partial_nonclaim | true | arena partial-fill rows remain nonclaim | True |
| VAL3248_9_next_written | true | 3249 next target written | True |
| VAL3248_10_doc_written | true | 3248 markdown checkpoint exists | True |
| VAL3248_OVERALL | true | 3248 validation overall | all required validation rows passed |

## Generated Evidence

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_QBASIC_COLLAR_CONSTRUCTION_ATTEMPT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_COLLAR_QBASIC_CHAIN_RULE_THEOREM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_FIRST_POYNTING_ARENA_ROW_PARTIAL_FILL.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_COLLAR_MISSING_SIGNATURES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_SCORE_ROW_UPDATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_CLAIM_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3248_VALIDATION.csv`