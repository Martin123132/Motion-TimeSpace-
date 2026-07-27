# 2381 - boundary term classification exact vs corner/reference

## Result

2381 classifies the boundary problem exposed by 2379 and partially reduced by 2380.

The exact-improvement component is the good news: if an actual MTS boundary term is `d mu`/`d_S b_X`, with fixed `tau`,
fixed surface, no corner, no harmonic/topological part, and closed weight, it is conditionally silent in the Hamiltonian
variation.  That is the cleanest derived route so far for one chunk of `B_zero_flux`.

The bad-but-useful news is that the actual boundary remainder is not empty yet.  It splits into corner, topological or
non-exact, field-dependent tau/surface, unfixed reference, nonintegrable flux, and Hilbert/topological source-equality
pieces.  The selected next attack is therefore the fixed boundary class plus `H_ref/B_ref` selector, because an unfixed
reference can fake charge closure.

No `B_zero_flux=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or GitHub/public claim is made.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2381_00_2380_doc | 2380_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md | true | true | 2380 exact-improvement cancellation law and Bzero split | false |
| SRC2381_01_2380_bzero_reduction | 2380_bzero_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv | true | true | machine-readable 2380 remainder vector | false |
| SRC2381_02_1019_doc | 1019_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md | true | true | older exactness/Stokes and projector orthogonality precedent | false |
| SRC2381_03_1019_exactness_csv | 1019_exactness_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv | true | true | exactness/counterterm clause source | false |
| SRC2381_04_1020_doc | 1020_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | true | true | domain/cohomology/corner classification precedent | false |
| SRC2381_05_1020_domain_csv | 1020_domain_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv | true | true | boundary domain certificate rows | false |
| SRC2381_06_1020_weighted_stokes_csv | 1020_weighted_stokes_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv | true | true | exact/harmonic/residual decomposition source | false |
| SRC2381_07_1771_doc | 1771_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md | true | true | boundary/reference as known local residual sector | false |
| SRC2381_08_1772_doc | 1772_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md | true | true | Hilbert/topological equality guard connected to B_zero | false |
| SRC2381_09_2379_doc | 2379_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | true | true | current Bzero theorem gate failure and denominator gate | false |

## Boundary Term Classification

| row_id | class | candidate_form | classification | current_evidence | missing_certificate | residual_if_missing | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BTC2381_0_exact_improvement | exact_improvement | B = d mu or boundary momentum B_X = d_S b_X with closed weight | CONDITIONAL_ZERO_CLASS | 2380 proves k_tau invariance for exact mu; 1019/1020 give weighted-Stokes clauses | explicit parent primitive mu/b_X, fixed tau, fixed surface, closed kernel/weight, no corner, no harmonic part | Delta_exact_commutator or edge residual source pack | component can be zero only after actual term classification | false |
| BTC2381_1_corner | corner_codimension_two | corner charge Q_C or codimension-two contribution to Q_tau/theta | LIVE_REMAINDER | 1020 requires no active corner boundary or explicit Q_C | corner-free surface or included corner charge with fixed convention | epsilon_corner_abs | blocks Bzero zero theorem | false |
| BTC2381_2_topological_nonexact | topological_or_nonexact | closed but non-exact h_X, harmonic edge mode, or fixed cohomology class | LIVE_REMAINDER | 1020 decomposes B_X = d_S b_X + h_X + r_X | h_X=0, projected silent, or separately source-bounded in same boundary class | epsilon_top_abs | exactness cannot erase harmonic/topological charge | false |
| BTC2381_3_field_dependent_tau_surface | field_dependent_tau_or_surface | [delta,i_tau]mu, delta S_outer, moving readout surface, radial profile | LIVE_REMAINDER | 2380 cancellation needs fixed tau and fixed surface | delta tau=0, delta S_outer=0, same-frame surface lock before variation | epsilon_delta_tau_abs | exact-improvement cancellation no longer follows | false |
| BTC2381_4_fixed_reference | unfixed_reference_counterterm | H_ref or B_ref chosen/shifted after source/readout | PRIMARY_LIVE_REMAINDER | 1771 and 2379 keep fixed-before-readout reference missing; 2380 says exact improvements cannot be fitted knobs | source-independent H_ref/B_ref selector fixed before readout and shared boundary class | Delta_ref_over_MH | can fake charge closure if not fixed, so it is the selected next attack | false |
| BTC2381_5_nonintegrable_flux | nonintegrable_flux | field-space curl of delta Q_tau - i_tau theta or flux through open annulus | LIVE_REMAINDER | 2339/2340/2379 keep H_tau integrability missing | closed one-form on field space after exact/corner/reference split | Delta_H_res_over_MH | H_tau and M_H_ref remain placeholder if nonintegrable | false |
| BTC2381_6_Hilbert_topological_equality | source_measure_equality_remainder | Pi_M J_H - J_M_top - dB_zero | PARALLEL_ROOT_REMAINDER | 1772 warns a closed topological current can be the wrong conserved object | Pi_M J_H = J_M_top + dB_zero with silent/included Bzero and same M_H_ref | R_eq_integral and I_commutator remain | Newton/GR source normalization cannot be claimed from boundary zero alone | false |
| BTC2381_7_total | Bzero_remainder_total | B_rem = B_corner + B_top + B_delta_tau + B_ref + B_nonintegrable + B_source_measure | REDUCED_BUT_NOT_CLOSED | 2380 plus 1019/1020/1772 | all live classes zeroed or finite source-bounded with positive same-frame M_H_ref | epsilon_Brem_abs | Bzero is now structured but still nonclaim | false |

## Boundary Certificate Matrix

| row_id | certificate | needed_for | current_status | test | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BCC2381_0_parent_primitive | explicit exact primitive | exact_improvement zero | MISSING_PARENT_PRIMITIVE | write mu or b_X from parent L/theta/Q, not by posterior fitting | BTC2381_0_exact_improvement | false |
| BCC2381_1_surface | corner-free compact linked surface | Stokes/no-corner zero | MISSING_CORNER_CERTIFICATE | partial S=0 or all corners included with Q_C | BTC2381_1_corner | false |
| BCC2381_2_cohomology | relative cohomology/harmonic silence | topological/non-exact zero | MISSING_COHOMOLOGY_CERTIFICATE | h_X=0 or h_X sourced as finite residual in same boundary class | BTC2381_2_topological_nonexact | false |
| BCC2381_3_tau_surface_lock | fixed tau and fixed S_outer | 2380 k_tau cancellation | MISSING_TAU_SURFACE_LOCK | delta tau=0, delta S_outer=0, no readout-induced surface retuning | BTC2381_3_field_dependent_tau_surface | false |
| BCC2381_4_fixed_reference | fixed H_ref/B_ref selector | no cancellation knob and same boundary class | MISSING_FIXED_REFERENCE_SELECTOR | H_ref/B_ref fixed before source/readout and independent of residual sign/magnitude | BTC2381_4_fixed_reference | false |
| BCC2381_5_integrability | closed Hamiltonian one-form | H_tau and M_H_ref | MISSING_HTAU_INTEGRABILITY | delta(k_tau)=0 on reduced branch, or finite Delta_H_res row | BTC2381_5_nonintegrable_flux | false |
| BCC2381_6_source_measure | Hilbert/topological source equality | Newton/GR source normalization | MISSING_SOURCE_MEASURE_EQUALITY | Pi_M J_H = J_M_top + dB_zero and same charge gives Poisson/Gauss source before orbital GM | BTC2381_6_Hilbert_topological_equality | false |
| BCC2381_7_MHref | positive same-frame M_H_ref | normalized residual scoring | MISSING_POSITIVE_MHREF | finite positive H_tau[S_outer]-H_ref with source/equation path and no orbital-GM import | all normalized rows | false |

## Brem Bound Rows

| row_id | quantity | formula | units | status | required_inputs | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BRB2381_0_epsilon_Brem | epsilon_Brem_abs | (abs(B_corner)+abs(B_top)+abs(B_delta_tau)+abs(Delta_ref)+abs(Delta_H_res)+abs(R_eq_component))/M_H_ref | dimensionless after same-frame M_H_ref normalization | SCHEMA_READY_VALUES_MISSING | component numerators; units; source paths; fixed H_ref; positive M_H_ref; no-cancellation guard | false | false |
| BRB2381_1_exact_switch | B_exact_improvement_zero_switch | true iff B=B_exact, tau/S fixed, no corner, no harmonic/topological class, closed weight | boolean theorem switch | SWITCH_BLOCKED_PENDING_TERM_CLASSIFICATION | explicit parent primitive and boundary class certificates | false | false |
| BRB2381_2_Delta_ref | Delta_ref_over_MH | abs(H_ref_shift_or_unfixed_counterterm)/M_H_ref | dimensionless after same-frame M_H_ref normalization | PRIMARY_NEXT_BOUND_IF_SELECTOR_FAILS | H_ref selector or finite reference-shift numerator, M_H_ref, no-cancellation guard | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2381_0_classification_result | classify Bzero into exact, corner, topological, tau/surface, reference, nonintegrable and source-measure pieces | 2380 makes exact improvements algebraically silent, but 1019/1020/1772 show exactness is not enough without domain/cohomology/reference/source equality | the boundary blocker is structured into certificates and residual rows | CLASSIFICATION_BUILT_NONCLAIM | false |
| DEC2381_1_primary_next | attack fixed boundary class and H_ref selector next | unfixed reference can fake charge closure and is repeatedly listed as the practical boundary hazard | 2382 should derive a pre-readout H_ref/B_ref selector or stage Delta_ref_over_MH | SELECT_2382_FIXED_REFERENCE | false |
| DEC2381_2_no_claim | do not claim Bzero/local GR/Newton | all certificate classes except the abstract exact-improvement algebra are still unsigned or missing values | private derivation route continues; no GitHub update | GLOBAL_CLAIMS_BLOCKED | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2381_0_term_classification | all actual MTS boundary/reference terms classified | FAIL_PARTIAL_CLASSIFICATION_ONLY | cannot set Bzero=0 globally | false |
| CG2381_1_exact_component | exact-improvement component zero | PASS_CONDITIONAL_COMPONENT_ONLY | usable after explicit parent primitive and domain certificates | false |
| CG2381_2_fixed_reference | fixed H_ref/B_ref selector | FAIL | Delta_ref remains selected blocker | false |
| CG2381_3_MHref | positive same-frame M_H_ref | FAIL | epsilon_Brem_abs cannot be scored | false |
| CG2381_4_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | boundary and source-measure bridges remain open | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2381_0_Stokes_overclaim | exact/Stokes route kills every boundary term | false | corner, harmonic/topological, non-owned residual, moving surface and fixed-reference conditions remain | BTC2381_1_corner;BTC2381_2_topological_nonexact;BTC2381_3_field_dependent_tau_surface;BTC2381_4_fixed_reference | false |
| REF2381_1_reference_fit | choose B_ref/H_ref after readout to cancel B_rem | false | reference must be selected before source/readout or it becomes a fitted cancellation knob | BCC2381_4_fixed_reference;CG2381_2_fixed_reference | false |
| REF2381_2_closed_wrong_object | closed topological charge is enough for measured GM/Newton | false | 1772 shows the topological current can be the wrong conserved object without Hilbert/source equality | BTC2381_6_Hilbert_topological_equality;BCC2381_6_source_measure | false |
| REF2381_3_public_checkpoint | publish this as a local GR/Newton pass | false | classification is progress, not closure; values and certificates are missing | CG2381_0_term_classification;CG2381_3_MHref;CG2381_4_local_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2381_0_selected | 2382-Y5-R2FR-fixed-boundary-class-and-Href-selector-or-Delta-ref-row.md | derive a source-independent boundary class plus H_ref/B_ref selector fixed before source/readout and compatible with exact-improvement cancellation | stage Delta_ref_over_MH with source path, units, no-cancellation guard and valid_for_claim=false | false |
| NEXT2381_1_parallel | 2382b-Y5-R2FR-parent-primitive-mu-or-boundary-residual-source-pack.md | write the explicit parent primitive mu/b_X for actual MTS boundary terms | retain exact switch blocked and source-pack every unowned boundary term | false |
| NEXT2381_2_parallel | 2382c-Y5-R2FR-Hilbert-topological-source-equality-or-Req-bound.md | prove Pi_M J_H = J_M_top + dB_zero in the same boundary class | retain R_eq_integral and I_commutator bound rows | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2381_00_sources_exist | PASS | all required source paths exist | false |
| VAL2381_01_needles_found | PASS | all source needles found | false |
| VAL2381_02_all_remainder_classes | PASS | boundary classes cover exact/corner/topological/tau/reference/flux/source-measure | false |
| VAL2381_03_reference_selected | PASS | fixed reference selected as primary live remainder | false |
| VAL2381_04_certificates_blocked | PASS | all required certificates remain explicit missing gates | false |
| VAL2381_05_bound_rows_nonready | PASS | Brem/Delta_ref bound rows remain non-score-ready | false |
| VAL2381_06_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2381_07_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2381_08_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2381_09_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2381_10_next_selected | PASS | fixed boundary class/H_ref selector selected next | false |
| VAL2381_OVERALL | PASS | 2381 classifies the Bzero remainder, keeps exact-improvement zero conditional, selects fixed-reference/Href selector next, and blocks all public/local claims | false |

## Practical Status

This is the non-circling branch.  We did not just say "boundary term missing" again.  The boundary term now has bins,
switches, and residual names.  The exact part has a real mathematical cancellation route; the reference part is the
most dangerous unresolved piece because it can masquerade as a solved source charge if selected after readout.

So the next best strike is `2382`: derive a fixed pre-readout boundary/reference selector, or admit `Delta_ref_over_MH`
as the honest residual.
