# 2382 - fixed boundary class and Href selector or Delta-ref row

## Result

2382 derives the exact *criterion* for a safe boundary/reference selector:

`Sigma_ref = Sigma_ref(boundary_class, topology, corner convention, asymptotic coframe, tau, stationary/vacuum branch)`

with no source/material/GM/readout/residual inputs.  If `D_source Sigma_ref = 0`, then by the chain rule

`D_source B_ref = (delta B_ref/delta Sigma_ref) D_source Sigma_ref = 0`

and likewise `D_source H_ref=0`.  That is the clean condition under which the source component of `Delta_ref` vanishes.

But the current corpus still does **not** supply the parent equation that fixes `Sigma_ref`, nor the no-marker/no-GM
certificate, nor the surface no-retune certificate, nor positive same-frame `M_H_ref`.  So the selector theorem is not
promoted.  `Delta_ref_over_MH` is staged as a nonclaim residual row.

No `B_zero_flux=0`, `Delta_ref=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or GitHub/public claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2382_00_2381_doc | 2381_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md | true | true | current handoff selecting fixed-reference selector or Delta_ref row | false |
| SRC2382_01_2381_classification | 2381_classification | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2381_BOUNDARY_TERM_CLASSIFICATION.csv | true | true | machine-readable fixed-reference live remainder | false |
| SRC2382_02_999_doc | 999_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md | true | true | strict fixed-branch selector precedent | false |
| SRC2382_03_999_selector_attempt | 999_selector_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv | true | true | fixed branch selector attempt rows | false |
| SRC2382_04_999_parent_contract | 999_parent_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv | true | true | future parent selector contract | false |
| SRC2382_05_1000_schema | 1000_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1000_STRICT_INPUT_SCHEMA.csv | true | true | strict Delta_ref provenance schema | false |
| SRC2382_06_1001_radius_audit | 1001_radius_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv | true | true | surface/domain/no-retune reference audit | false |
| SRC2382_07_545_doc | 545_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md | true | true | minimal boundary-reference action contract precedent | false |
| SRC2382_08_543_doc | 543_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md | true | true | original boundary-reference residual failure | false |
| SRC2382_09_2379_doc | 2379_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | true | true | current Bzero theorem dependency | false |

## Fixed Reference Selector Theorem

| row_id | theorem_step | statement | derivation | required_for_zero | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FRT2382_0_selector_object | selector object | Define a reference selector Sigma_ref assigning (gamma_ref,tau_ref,C_top,B_ct,S0) from boundary/topology/stationarity data. | H_ref and B_ref become functions of Sigma_ref rather than after-the-fact subtractions. | named Sigma_ref with parent source/equation path | DEFINITION_CONTRACT_ONLY | false |
| FRT2382_1_allowed_inputs | allowed selector inputs | Sigma_ref may depend on fixed boundary class, topology/cohomology, orientation/corner convention, asymptotic coframe, tau convention and stationary/vacuum branch data. | These are pre-readout structural data, not measured source normalizations. | input grammar has no source/material/GM labels | GRAMMAR_WRITTEN_NOT_PARENT_SIGNED | false |
| FRT2382_2_source_blind_chain_rule | source-blindness chain rule | If D_source Sigma_ref=0, then D_source B_ref=(delta B_ref/delta Sigma_ref)D_source Sigma_ref=0 and D_source H_ref=0. | This is the exact chain-rule condition that would set the source component of Delta_ref to zero. | componentwise D_source gamma_ref=tau_ref=C_top=B_ct=S0=0 | CONDITIONAL_THEOREM_DERIVED | false |
| FRT2382_3_no_GM_laundering | no GM/fitted-source laundering | Sigma_ref must satisfy partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} Sigma_ref=0 before the source-measure bridge is derived. | Otherwise the reference subtraction can absorb the charge we are trying to derive. | no measured-GM, fitted mass, composition or M_H_ref labels in selector provenance | FORBIDDEN_INPUT_RULE_DERIVED | false |
| FRT2382_4_no_retune | no-retune surface/domain rule | D_source S0=0 and linked surfaces remain in one parent boundary class; B_ref is not retuned as source, radius or readout changes. | Prevents source dependence from entering through a moving comparison surface rather than the B_ref integrand. | surface class, corner convention, no-crossed-source and no-retune certificates | CONDITIONAL_ROUTE_NOT_SIGNED | false |
| FRT2382_5_MHref_sidecar | same-frame denominator sidecar | Any Delta_ref/M_H_ref row requires finite positive M_H_ref in the same tau/coframe/frame as H_ref. | A source-blind H_ref is not enough if the denominator is imported from orbital GM or a different frame. | M_H_ref source path, equation ref, units, tau_id, frame_id, no orbital-GM import | MISSING_POSITIVE_MHREF | false |
| FRT2382_6_verdict | current theorem verdict | The source-blindness criterion is derived, but the current corpus does not parent-sign Sigma_ref or M_H_ref. | FRT2382_0..5 give a sharp contract and refusal gate, not a completed reference theorem. | parent selector equation plus same-frame M_H_ref | THEOREM_NOT_PROMOTED_RETAIN_DELTA_REF_ROW | false |

## Selector Input Grammar

| row_id | input | allowed | role | certificate_required | violation_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SIG2382_0_boundary_class | fixed boundary class | true | selects which surfaces/corners/cohomology classes are admissible | boundary class id and no-retune rule | Delta_ref can change with source/readout surface | false |
| SIG2382_1_topology | topology/cohomology/orientation/corner convention | true | fixes topological and corner reference data before source variation | C_top and corner convention source path | topological/corner charge can hide in H_ref | false |
| SIG2382_2_frame_tau | asymptotic coframe and tau convention | true | locks the Hamiltonian generator and denominator frame | tau_id/frame_id/coframe_id shared by Q_tau, H_ref and M_H_ref | same-frame normalization fails | false |
| SIG2382_3_stationary_vacuum_branch | stationary/vacuum reference branch data | conditional | can define zero-source comparison only if selected by parent equation rather than fit | selector equation or Ward/topological condition | reference-only zero is not MTS evidence | false |
| SIG2382_4_observed_GM | observed GM/orbital mass/fitted source normalization | false | forbidden calibration input | absence proof in B_ref/H_ref provenance | borrow Newton/source normalization to prove Newton/source normalization | false |
| SIG2382_5_material_labels | composition, material marker, source parameter kappa_A or m_A | false | forbidden source-label input | D_source Sigma_ref=0 and no marker labels | reference subtraction becomes source-dependent | false |
| SIG2382_6_residual_sign | observed residual sign/magnitude | false | forbidden cancellation knob | timestamp/order: selector fixed before readout | post-hoc counterterm cancellation | false |

## Delta Ref Bound Rows

| row_id | quantity | formula | required_inputs | current_value | status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DRR2382_0_source_component | Delta_ref_source_component_over_MH | abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref | partial_source_Delta_ref;Delta_source_scale;B_ref_rule;M_H_ref;source_path;equation_ref;no_cancellation_guard | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_SOURCE_SCALE;MISSING_PARENT_BREF_RULE;MISSING_M_H_REF | SCHEMA_READY_VALUES_MISSING | false | false |
| DRR2382_1_surface_component | Delta_ref_surface_component_over_MH | abs(partial_surface_Delta_ref * Delta_surface_profile)/M_H_ref | surface_class_id;partial_surface_Delta_ref;Delta_surface_profile;closed_B_ref_certificate;corner_certificate;M_H_ref | MISSING_SURFACE_CLASS_ID;MISSING_PARTIAL_SURFACE_DERIVATIVE;MISSING_M_H_REF | SCHEMA_READY_VALUES_MISSING | false | false |
| DRR2382_2_counterterm_component | Delta_ref_counterterm_component_over_MH | abs(Delta_B_ct_unfixed_or_retuned)/M_H_ref | B_ct formula;counterterm convention;pre-readout timestamp/source path;M_H_ref;no-cancellation guard | MISSING_COUNTERTERM_CONVENTION;MISSING_PRE_READOUT_SELECTOR;MISSING_M_H_REF | SCHEMA_READY_VALUES_MISSING | false | false |
| DRR2382_3_total_absolute | Delta_ref_over_MH | (abs(Delta_ref_source)+abs(Delta_ref_surface)+abs(Delta_ref_counterterm)+abs(Delta_ref_corner_top))/M_H_ref | all component numerators;positive same-frame M_H_ref;absolute no-cancellation rule | COMPONENTS_MISSING | PRIMARY_BOUND_ROW_STAGED_NONCLAIM | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2382_0_conditional_gain | accept the source-blind selector criterion as a conditional theorem | if Sigma_ref is fixed before source/readout and D_source Sigma_ref=0, then chain rule gives D_source H_ref=D_source B_ref=0 | we now know exactly what a future parent action must sign | CONDITIONAL_SELECTOR_CRITERION_DERIVED | false |
| DEC2382_1_no_promotion | do not promote fixed-reference theorem | the current corpus still lacks parent selector equation, no-marker/no-GM proof, surface no-retune certificate and same-frame M_H_ref | Delta_ref_over_MH remains staged as nonclaim | THEOREM_NOT_PARENT_SIGNED | false |
| DEC2382_2_next | attack parent selector equation next | the missing object is not another table value; it is the equation or Ward/topological condition that fixes Sigma_ref | 2383 should try to derive E_Sigma=0/topological selector, otherwise source-acquire Delta_ref components | SELECT_2383_PARENT_SELECTOR_EQUATION | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2382_0_selector_criterion | source-blind selector chain-rule criterion | PASS_CONDITIONAL_CRITERION_ONLY | defines what would make Delta_ref source component zero | false |
| CG2382_1_parent_selector_equation | parent equation or Ward/topological condition fixes Sigma_ref | FAIL | fixed-reference theorem not promoted | false |
| CG2382_2_no_GM_no_marker | no GM/source/material labels in selector | FAIL_UNSIGNED | source-blindness remains conditional | false |
| CG2382_3_surface_no_retune | surface/domain/corner no-retune certificate | FAIL | surface Delta_ref component remains | false |
| CG2382_4_MHref | positive same-frame M_H_ref | FAIL | Delta_ref_over_MH cannot be scored | false |
| CG2382_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | boundary/reference and source-measure gates remain open | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2382_0_reference_only_zero | use reference-only zero as current MTS evidence | false | reference-only zero is not a parent-signed MTS selector theorem | FRT2382_0_selector_object;CG2382_1_parent_selector_equation | false |
| REF2382_1_GM_selector | let Sigma_ref depend on observed GM/fitted mass/M_H_ref | false | this borrows source normalization before deriving it | FRT2382_3_no_GM_laundering;SIG2382_4_observed_GM | false |
| REF2382_2_posthoc_counterterm | choose B_ct after reading the residual | false | post-readout counterterms are cancellation knobs, not derived boundary data | SIG2382_6_residual_sign;DRR2382_2_counterterm_component | false |
| REF2382_3_score_delta_ref | score Delta_ref_over_MH now | false | component numerators, B_ref rule, source paths, equation refs, and M_H_ref are missing | DRR2382_0_source_component;DRR2382_1_surface_component;DRR2382_2_counterterm_component;CG2382_4_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2382_0_selected | 2383-Y5-R2FR-parent-selector-equation-for-Sigma-ref-or-Delta-ref-source-pack.md | derive a parent Euler/Ward/topological/stationarity equation that fixes Sigma_ref without source, GM, material or post-readout inputs | fill Delta_ref component source pack with finite numerators, units, source paths, equation refs and valid_for_claim=false | false |
| NEXT2382_1_parallel | 2383b-Y5-R2FR-MHref-same-frame-sidecar-or-denominator-row.md | derive finite positive same-frame M_H_ref compatible with Sigma_ref | keep all normalized boundary rows non-score-ready | false |
| NEXT2382_2_parallel | 2383c-Y5-R2FR-Hilbert-topological-source-equality-or-Req-row.md | prove the Hamiltonian/topological charge is the Hilbert/source charge entering Poisson/Gauss | retain R_eq/I_commutator rows | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2382_00_sources_exist | PASS | all required source paths exist | false |
| VAL2382_01_needles_found | PASS | all source needles found | false |
| VAL2382_02_chain_rule_criterion_present | PASS | source-blindness chain-rule criterion present as conditional theorem | false |
| VAL2382_03_forbidden_inputs_present | PASS | forbidden GM/material/post-readout selector inputs present | false |
| VAL2382_04_delta_ref_rows_nonready | PASS | Delta_ref rows remain non-score-ready | false |
| VAL2382_05_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2382_06_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2382_07_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2382_08_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2382_09_next_selected | PASS | parent selector equation selected next | false |
| VAL2382_OVERALL | PASS | 2382 derives the conditional source-blind reference selector criterion, refuses promotion without parent selector/MHref, and stages Delta_ref rows nonclaim | false |

## Practical Status

This is another useful tightening.  The reference problem is no longer just "choose a boundary term carefully"; it is a
specific selector equation problem.  If the parent action can produce `Sigma_ref` from source-blind boundary/topological
data, `Delta_ref` gets a real zero route.  If not, the honest path is a finite `Delta_ref_over_MH` source pack.

The best next strike is therefore `2383`: try to derive the parent selector equation for `Sigma_ref`.  That is the
actual leap forward; another placeholder denominator row would be circling.
