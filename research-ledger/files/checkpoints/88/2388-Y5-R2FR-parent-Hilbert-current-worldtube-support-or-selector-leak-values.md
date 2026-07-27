# 2388 - parent Hilbert current worldtube support or selector leak values

## Result

2388 takes the 2387 handoff literally: do not treat `W_source` as a fitted domain label.  Make it the support of a
parent-owned Hilbert current, or keep the selector as a leak.

The conditional derivation is:

1. Start with a parent matter action `S_m[e_obs,psi_m]=int L_m`.
2. Vary with respect to the observed coframe:
   `delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m`.
3. Contract the Hilbert coframe current with a parent-fixed time generator:
   `J_H[tau] := -tau^a T_a`.
4. Define the source worldtube before readout:
   `W_source[tau] := closure(supp J_H[tau])`.

If `L_m`, `e_obs`, `tau`, the matter variables, and the support rule are all parent-owned, then `W_source` is a
covariant pre-readout selector.  If the support is compact and remains away from the annulus boundary during source
variation, the 2387 no-crossing argument can carry `D_source C_top=0` conditionally.

This is useful, but it is not yet a current-MTS local-GR proof.  The current corpus still lacks an explicit parent
matter Lagrangian, same-frame `tau/e_obs` lock, compact-support or tail theorem, no-marker proof, no-crossing
certificate, positive `M_H_ref`, and Hilbert/topological same-object equality.

So 2388 improves the derivation route, but refuses promotion.  No `W_source` pass, local-GR pass, Newton pass, PPN,
clock, orbital, R10, or public/GitHub claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2388_00_2387_doc | 2387_domain_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2387-Y5-R2FR-boundary-domain-selector-continuity-no-crossing-or-class-leak-values.md | true | true | 2387 selects parent Hilbert current/worldtube support as next gate | false |
| SRC2388_01_2387_certificates | 2387_domain_certificates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2387_DOMAIN_CERTIFICATE_MATRIX.csv | true | true | certificate gaps that 2388 must either close or carry as leak rows | false |
| SRC2388_02_1016_doc | 1016_parent_worldtube_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md | true | true | prior legal selector contract and missing parent Lagrangian warning | false |
| SRC2388_03_1718_doc | 1718_support_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1718-Y5-R2FR-worldtube-support-owner-or-Icommutator-domain-numerator-bound.md | true | true | worldtube support owner audit | false |
| SRC2388_04_1760_doc | 1760_matter_worldtube_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md | true | true | matter/worldtube quotient descent obstruction | false |
| SRC2388_05_2183_doc | 2183_worldtube_hilbert_selector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md | true | true | worldtube-Hilbert selector theorem attempt | false |
| SRC2388_06_1714_equality_doc | 1714_worldtube_hilbert_equality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | true | true | source normalization requires the same Hilbert object, not merely a closed charge | false |
| SRC2388_07_parent_contract_csv | parent_action_contract_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv | true | true | parent action contract clauses for current/worldtube ownership | false |
| SRC2388_08_source_measure_csv | worldtube_source_measure_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv | true | true | GR/Newton transfer requires dressed Hamiltonian source charge | false |
| SRC2388_09_2182_doc | 2182_topological_hilbert_equality | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md | true | true | topological route must become same Hilbert source object | false |

## Hilbert Current Selector Theorem

| row_id | step | statement | derivation_status | required_parent_clause | current_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HCS2388_0_parent_matter_variation | parent Hilbert current definition | For a parent matter action S_m[e_obs,psi_m]=int L_m, define the coframe Hilbert current T_a by delta L_m = E_m delta psi_m + T_a wedge delta e_obs^a + dTheta_m. | CONDITIONAL_STANDARD_VARIATIONAL_IDENTITY | explicit diffeomorphism-covariant L_m with one observed coframe e_obs and fixed matter variables | no signed MTS parent matter Lagrangian supplies T_a | false |
| HCS2388_1_tau_contraction | time-generator contraction | For a parent-fixed time generator tau=tau^a e_a, set J_H[tau] := -tau^a T_a, equivalently J_H^mu[tau]=T^mu_nu tau^nu in metric notation up to the chosen sign convention. | CONDITIONAL_CURRENT_FORMULA | tau fixed before source/readout and measured in the same observed frame as matter, clocks, rods, and orbital readout | tau/e_obs same-frame lock not parent-signed for this branch | false |
| HCS2388_2_worldtube_support | worldtube support selector | Define W_source[tau] := closure(supp J_H[tau]) before any residual fit; if J_H is parent-owned, W_source is selected by the source current rather than by a fitted radius or boundary. | CONDITIONAL_SELECTOR_DEFINITION | J_H is a real parent current and support is regular enough to admit linked exterior surfaces | support compactness/regularity and source-tail treatment remain unsigned | false |
| HCS2388_3_diffeomorphism_naturality | covariant support transformation | If L_m is natural under diffeomorphisms, then phi_*J_H[tau;Phi]=J_H[phi_*tau;phi_*Phi], so supp(J_H) and W_source transform covariantly. | CONDITIONAL_NATURALITY_THEOREM | no external material marker, noncovariant cutoff, or readout-chosen support mask | no-marker/no-cutoff grammar is still a contract row, not a parent theorem | false |
| HCS2388_4_no_crossing_implication | domain no-crossing handoff | If W_source is compact and remains a positive distance from the annulus boundary during the allowed source variation, then the linked surface class cannot jump and D_source C_top=0 follows conditionally. | CONDITIONAL_HANDOFF_TO_2387 | compact support, fixed linked surfaces, no retuning after readout, no topology-changing source event | the no-crossing certificate is not sourced by a parent support theorem | false |
| HCS2388_5_realistic_tail_warning | compactness caveat | For fields with exterior stress, radiation, scalar tails, or long-range electromagnetic energy, closure(supp J_H) need not be compact; the compact-source theorem then becomes a tail-bound problem, not a zero proof. | OBSTRUCTION_RETAINED | either prove exterior Hilbert tail vanishes in the selected matter sector or provide a finite tail/source-pack bound | no sector-by-sector tail theorem exists | false |

## Worldtube Support Certificate

| row_id | certificate | required_test | status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| WSC2388_0_parent_Lm | explicit parent matter Lagrangian | write L_m[e_obs,psi_m,Dpsi_m] and derive T_a = delta L_m/delta e_obs^a before readout | MISSING_PARENT_MATTER_LAGRANGIAN | epsilon_JH_owner | false |
| WSC2388_1_same_frame | single observed source frame | matter, clocks, rods, tau, and orbital readout use the same e_obs/theta frame | MISSING_SAME_FRAME_TAU_EOBS_LOCK | Delta_frame_source_over_MH | false |
| WSC2388_2_parent_tau | parent-owned time generator tau | tau is selected by parent boundary/asymptotic data, not by local residual fitting | MISSING_PARENT_TAU_SELECTOR | epsilon_tau_selector | false |
| WSC2388_3_support_compact | compact regular Hilbert support | closure(supp J_H[tau]) is compact/regular or an exterior tail norm is bounded | MISSING_COMPACT_SUPPORT_OR_TAIL_BOUND | epsilon_support_tail | false |
| WSC2388_4_no_marker | no material marker or readout mask | W_source is computed from J_H only; no fitted radius, galaxy mask, or residual-tuned boundary enters | MISSING_NO_MARKER_NO_READOUT_MASK_PROOF | epsilon_marker_selector | false |
| WSC2388_5_no_crossing | source-free annulus/no-crossing | A cap W_source remains empty under the allowed source variation with linked surfaces fixed | MISSING_NO_CROSSING_CERTIFICATE | epsilon_crossing_flux | false |
| WSC2388_6_MHref | positive same-frame M_H_ref | derive finite positive Hamiltonian/Hilbert charge denominator in the same tau/e_obs frame | MISSING_POSITIVE_MHREF | all normalized rows remain non-score-ready | false |
| WSC2388_7_same_object | same Hilbert/topological source object | Pi_M J_H = J_M_top + dB_zero + R_eq with R_eq and boundary flux either zero or bounded | MISSING_TOPOLOGICAL_HILBERT_EQUALITY | epsilon_M_source_mismatch | false |

## Selector Leak Values

| row_id | quantity | formula | units | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SLV2388_0_JH_owner | epsilon_JH_owner | abs(Delta C_top_from_nonparent_JH * K_class)/M_H_ref | dimensionless after M_H_ref normalization | MISSING_PARENT_MATTER_LAGRANGIAN;MISSING_K_CLASS;MISSING_M_H_REF | false | false |
| SLV2388_1_tau_frame | Delta_frame_source_over_MH | abs(integral_S (J_H[tau_local]-J_H[tau_parent]))/M_H_ref | dimensionless | MISSING_PARENT_TAU_SELECTOR;MISSING_SAME_FRAME_CURRENT;MISSING_M_H_REF | false | false |
| SLV2388_2_support_tail | epsilon_support_tail | integral_{M\W_delta} \|J_H[tau]\| / M_H_ref | dimensionless source-charge fraction | MISSING_JH_DENSITY;MISSING_W_DELTA;MISSING_TAIL_NORM;MISSING_M_H_REF | false | false |
| SLV2388_3_marker_selector | epsilon_marker_selector | abs(Delta C_top_from_readout_mask * K_marker)/M_H_ref | dimensionless | MISSING_NO_MARKER_PROOF;MISSING_K_MARKER;MISSING_M_H_REF | false | false |
| SLV2388_4_crossing_flux | epsilon_crossing_flux | integral_path integral_{partial A} \|i_n J_H[tau]\| dlambda / M_H_ref | dimensionless | MISSING_NO_CROSSING_PATH;MISSING_BOUNDARY_FLUX;MISSING_M_H_REF | false | false |
| SLV2388_5_same_object | epsilon_M_source_mismatch | abs(integral_S (Pi_M J_H - J_M_top - dB_zero))/M_H_ref | dimensionless source-charge mismatch | MISSING_PIM_JH;MISSING_JM_TOP;MISSING_B_ZERO;MISSING_R_EQ;MISSING_M_H_REF | false | false |
| SLV2388_6_total | Delta_ref_worldtube_selector_total_over_MH | epsilon_JH_owner + Delta_frame_source_over_MH + epsilon_support_tail + epsilon_marker_selector + epsilon_crossing_flux + epsilon_M_source_mismatch | dimensionless | COMPONENTS_MISSING | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2388_0_accept_shape | accept conditional Hilbert-current/worldtube selector shape | the variational definition J_H[tau] := -tau^a delta L_m/delta e_obs^a is the right GR-compatible source object when parent-owned | worldtube selection is no longer arbitrary in form; it is a parent-current problem | CONDITIONAL_SELECTOR_SHAPE_ACCEPTED | false |
| DEC2388_1_no_promotion | do not claim parent-owned W_source for current MTS | explicit L_m, tau/e_obs lock, compact/tail theorem, no-marker proof, no-crossing certificate, M_H_ref, and Pi_M/J_M_top equality are missing | local-GR/Newton/R10/PPN/orbital/clock claims remain blocked | WORLD_TUBE_SELECTOR_NOT_PARENT_SIGNED | false |
| DEC2388_2_tail_route | retain tail-bound fallback | realistic fields can have exterior stress/tails, so compact support cannot be assumed globally | if zero support fails, score support-tail and crossing-flux rows rather than hiding them | TAIL_BOUND_FALLBACK_REQUIRED | false |
| DEC2388_3_next | attack parent matter action current density next | without an explicit L_m and same-frame tau/e_obs lock, J_H remains a legal placeholder | 2389 should derive the parent matter-current density or fill epsilon_JH_owner and Delta_frame_source rows | SELECT_2389_PARENT_MATTER_CURRENT_DENSITY | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2388_0_selector_shape | Hilbert-current selector formula shape | PASS_CONDITIONAL_THEOREM_ONLY | use as derivation route, not as evidence | false |
| CG2388_1_parent_Lm | explicit parent matter Lagrangian | FAIL | J_H owner not claim-grade | false |
| CG2388_2_tau_frame | same-frame tau/e_obs source current | FAIL | source-frame leakage remains open | false |
| CG2388_3_compact_tail | compact support or explicit tail bound | FAIL | no-crossing theorem cannot be promoted | false |
| CG2388_4_MHref | positive same-frame M_H_ref | FAIL | normalized residual rows remain non-score-ready | false |
| CG2388_5_GR_Newton | GR/Newton local source normalization | BLOCKED | no local-GR/Newton claim | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2388_0_claim_Wsource | W_source is now parent-derived for current MTS | false | the selector formula is conditional; parent L_m and same-frame tau/e_obs lock are missing | WSC2388_0_parent_Lm;WSC2388_1_same_frame;WSC2388_2_parent_tau | false |
| REF2388_1_assume_compact | compact support/no-crossing is automatic | false | long-range field stress or tails can make support noncompact; a zero theorem or tail bound is required | WSC2388_3_support_compact;SLV2388_2_support_tail;SLV2388_4_crossing_flux | false |
| REF2388_2_score_residuals | selector leak rows can be scored now | false | M_H_ref and all parent coefficients/source paths are missing | SLV2388_0_JH_owner;SLV2388_6_total;WSC2388_6_MHref | false |
| REF2388_3_claim_GR | local GR/Newton follows from the Hilbert-current shape | false | GR/Newton also requires EH exterior fixed point, Hamiltonian charge equality, M_H_ref, PPN closure, and same object Pi_M/J_H/J_M_top | WSC2388_7_same_object;CG2388_5_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2388_0_selected | 2389-Y5-R2FR-parent-matter-action-current-density-or-JH-owner-leak-values.md | write an explicit parent matter action sector and derive T_a and J_H[tau] in the same observed coframe before readout | fill epsilon_JH_owner, Delta_frame_source_over_MH, and epsilon_tau_selector rows with sourced finite bounds and valid_for_claim=false | false |
| NEXT2388_1_parallel | 2389b-Y5-R2FR-compact-support-tail-bound-or-crossing-flux-row.md | prove sector-specific compact support/no exterior Hilbert tail for the local source class | source a support-tail norm and no-crossing boundary-flux row | false |
| NEXT2388_2_parallel | 2389c-Y5-R2FR-Hilbert-topological-same-object-or-epsilonM-row.md | derive Pi_M J_H = J_M_top + dB_zero with R_eq=0 and zero linked boundary flux | carry epsilon_M_source_mismatch as finite nonclaim residual | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2388_00_sources_exist | PASS | all required source paths exist | false |
| VAL2388_01_needles_found | PASS | all source needles found | false |
| VAL2388_02_current_formula_present | PASS | Hilbert current contraction formula is present | false |
| VAL2388_03_worldtube_support_present | PASS | worldtube support selector definition is present | false |
| VAL2388_04_required_gaps_explicit | PASS | parent Lm/tau/support/no-marker/no-crossing/MHref/equality gaps explicit | false |
| VAL2388_05_value_rows_nonready | PASS | selector leak rows remain non-score-ready | false |
| VAL2388_06_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2388_07_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2388_08_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2388_09_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2388_10_next_selected | PASS | parent matter action/current density selected next | false |
| VAL2388_OVERALL | PASS | 2388 derives conditional parent Hilbert-current/worldtube selector shape, refuses promotion without parent Lm/tau/support/MHref/equality, and selects current-density ownership next | false |

## Practical Status

This is a real narrowing of the GR/Newton bridge.  We are no longer asking vaguely whether the local boundary
knows the source.  The question is now whether the parent action can produce one observed-frame Hilbert current
`J_H[tau]`, and whether its support is compact or tail-bounded enough to choose linked exterior domains without
readout retuning.  That is the next honest lock.
