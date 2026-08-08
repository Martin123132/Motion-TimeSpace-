# 2380 - parent theta/Qtau fixed-reference or M_H_ref first row

## Result

2380 is not another table-circle.  It reopens the 2379 parent theta/Qtau/fixed-reference/MHref target, checks the older
2339/2340 attempts, and extracts one real algebraic gain:

`L' = L + d mu`, `theta' = theta + delta mu`, `Q'_tau = Q_tau + i_tau mu`, so

`k'_tau = delta Q'_tau - i_tau theta' = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau`

whenever `tau` and the integration surface are fixed and there are no corner/topological/anomalous pieces.  In plain
terms: exact boundary improvements do not change the Hamiltonian surface one-form.  That gives a conditional zero for
the exact-improvement part of `B_zero_flux`.

This does **not** derive `M_H_ref`, `H_ref`, full `theta_MTS`, full `Q_tau^MTS`, the source-measure bridge, or local
GR/Newton recovery.  The gain is narrower but real: `B_zero_flux` is now split into an exact piece that can cancel
algebraically and a remainder vector that must be classified or bounded.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2380_00_2379_doc | 2379_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | true | true | current branch selected parent charge/fixed-reference/MHref as next blocker | false |
| SRC2380_01_2379_bzero_audit | 2379_bzero_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2379_BZERO_NOFLUX_THEOREM_AUDIT.csv | true | true | current Bzero theorem obstruction rows | false |
| SRC2380_02_2379_bzero_row | 2379_bzero_row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2379_BZERO_FIRST_BOUND_ROW.csv | true | true | current nonclaim Bzero numerator/denominator row | false |
| SRC2380_03_2339_doc | 2339_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2339-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md | true | true | older exact target attempt; prevents duplicate circling | false |
| SRC2380_04_2340_doc | 2340_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2340-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md | true | true | older parent charge extraction route; identifies EH-anchor residual route | false |
| SRC2380_05_2378_doc | 2378_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2378-Y5-R2FR-boundary-projective-residual-split-under-private-SRNG.md | true | true | boundary/improvement flux status before 2379 | false |
| SRC2380_06_2377_doc | 2377_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2377-Y5-R2FR-downstream-observation-functor-naturality-or-SRNG-adoption.md | true | true | private SRNG/OFC branch status used only as conditional background | false |
| SRC2380_07_2339_validation | 2339_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2339_VALIDATION.csv | true | true | older same-target validation | false |
| SRC2380_08_2340_validation | 2340_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2340_VALIDATION.csv | true | true | older parent extraction validation | false |

## Exact Improvement Cancellation Derivation

| row_id | derivation_step | statement | condition | result | remaining_obstruction | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EIC2380_0_setup | exact boundary improvement setup | Let L_prime = L + d mu for a boundary/improvement (n-1)-form mu. | mu is a genuine exact improvement on the same field bundle and boundary class | only the theta and Q_tau representatives shift; equations of motion are unchanged | non-exact, corner, topological, or readout-dependent pieces are not covered | false |
| EIC2380_1_theta_shift | symplectic potential shift | delta L_prime = E_A delta Phi^A + d(theta + delta mu), so theta_prime = theta + delta mu. | single parent variation exists and delta acts on fields, not on the chosen generator tau | exact improvement contribution to theta is delta mu | parent MTS theta still not globally extracted sector-by-sector | false |
| EIC2380_2_charge_shift | Noether charge representative shift | J_tau_prime = theta_prime(L_tau Phi) - i_tau L_prime = J_tau + d(i_tau mu), hence Q_tau_prime = Q_tau + i_tau mu up to exact/corner terms. | tau is fixed, the Cartan identity is used in the same boundary class, and corner ambiguities are absent or separately retained | exact improvement contribution to Q_tau is i_tau mu | field-dependent tau, corner terms, and global cohomology can create residuals | false |
| EIC2380_3_k_invariance | Hamiltonian surface one-form cancellation | k_tau_prime = delta Q_tau_prime - i_tau theta_prime = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau when [delta,i_tau]=0. | fixed tau, fixed surface embedding, no anomalous corner/codimension-two contribution | exact boundary improvements do not change delta H_tau | if tau or the surface/readout is field-dependent, a commutator residual remains | false |
| EIC2380_4_boundary_component | Bzero exact-improvement component | B_zero_flux_exact := integral_S(delta(i_tau mu)-i_tau(delta mu)) = 0 under the fixed-tau exact-improvement clauses. | every candidate Bzero term is classified as exact mu with no corner/topological/field-dependent remainder | the exact-improvement part of B_zero_flux is conditionally zero | classification of actual MTS boundary/reference terms is still missing | false |
| EIC2380_5_not_MHref | denominator caveat | The cancellation law reduces a numerator channel only; it does not create H_tau, H_ref, M_H_ref, or the source-measure bridge. | none | local GR/Newton remains blocked until M_H_ref and source equality are derived or bounded | positive same-frame M_H_ref and Pi_M J_H = J_M_top + dB_zero | false |

## Theta/Qtau Gate Recheck

| row_id | gate | status_before_2380 | new_2380_result | claim_effect | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TQR2380_0_no_circle | same target already attempted | 2339/2340 staged theta_Qtau_Htau_Href/MHref rows but did not promote | do not repeat the first-row table; extract one exact boundary-improvement cancellation law | component reduction only, not global closure | classify actual boundary/reference terms into exact/corner/topological/field-dependent classes | false |
| TQR2380_1_parent_variation | single parent current-chain variation | MISSING_SINGLE_PARENT_VARIATION | exact-improvement algebra is available once a parent variation and mu term are identified | not enough to own theta_MTS globally | sector certificates for EH anchor, matter/source, boundary/reference, extra/projector/glue | false |
| TQR2380_2_theta_Qtau | theta_MTS and Q_tau^MTS extraction | MISSING_PARENT_THETA_QTAU | boundary exact-improvement shifts are algebraically controlled | Q_tau total remains unowned outside the exact-improvement component | write component ledger: Q_EH, Q_matter/source, Q_boundary_exact, Q_corner, Q_extra, Q_projector | false |
| TQR2380_3_fixed_reference | fixed H_ref/counterterm before readout | MISSING_FIXED_REFERENCE_CERTIFICATE | exact improvements cannot be used as post-hoc cancellation knobs in delta H | H_ref still must be fixed by a source-independent selector | derive or bound Delta_ref for unfixed/non-exact reference choices | false |
| TQR2380_4_integrability | H_tau integrability | MISSING_HTAU_INTEGRABILITY | exact improvement does not spoil delta H_tau when [delta,i_tau]=0 | other nonintegrable sector pieces still block H_tau | compute residual one-form Delta_H_res over sector matrix | false |
| TQR2380_5_MHref | positive same-frame M_H_ref | MISSING_POSITIVE_MHREF | unchanged: denominator missing | Bzero/R_eq/I_commutator/PPN rows remain non-score-ready | fill H_tau-H_ref from parent charge or keep MHref row nonclaim | false |
| TQR2380_6_source_measure | Hamiltonian charge equals measured source normalization | MISSING_SOURCE_MEASURE_BRIDGE | unchanged: exact boundary-improvement cancellation is not the Poisson/Gauss bridge | Newton/GR recovery cannot be claimed from a conserved charge alone | prove Pi_M J_H = J_M_top + dB_zero or retain R_eq | false |

## Bzero Residual Reduction

| row_id | component | formula | status | zero_condition | residual_if_condition_fails | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| BRR2380_0_exact_improvement | B_exact_improvement | integral_S(delta(i_tau mu)-i_tau(delta mu)) | CONDITIONAL_ZERO_DERIVED | mu exact; tau fixed; surface fixed; no corner anomaly; [delta,i_tau]=0 | Delta_exact_commutator | false |
| BRR2380_1_corner | B_corner | corner/codimension-two contribution to Q_tau or theta | UNCLASSIFIED_RETAINS_BOUND_ROW | corner term absent or paired by fixed corner convention | epsilon_corner_abs | false |
| BRR2380_2_topological | B_topological_or_nonexact | closed-but-not-exact or topological boundary representative | UNCLASSIFIED_RETAINS_BOUND_ROW | cohomology class fixed and source-independent or projected silent | epsilon_top_abs | false |
| BRR2380_3_field_dependent_tau | B_delta_tau | delta(i_tau mu)-i_tau(delta mu) when delta tau != 0 or readout surface moves | UNCLASSIFIED_RETAINS_BOUND_ROW | tau and S_outer locked before variation | epsilon_delta_tau_abs | false |
| BRR2380_4_reference | B_reference_unfixed | H_ref shift or post-readout counterterm choice | MISSING_FIXED_REFERENCE | H_ref selector fixed before source/readout and independent of fitted residual | Delta_ref_over_MH | false |
| BRR2380_5_total | B_zero_flux_reduced | B_zero_flux = B_exact_improvement_zero + B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux | REDUCED_NOT_CLOSED | all non-exact/corner/tau/reference/flux pieces vanish or are bounded with M_H_ref | epsilon_Bzero_abs remains non-score-ready | false |

## M_H_ref First Row Update

| row_id | quantity | formula | status | update_from_2380 | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MHR2380_0_denominator | M_H_ref | M_H_ref := H_tau[S_outer] - H_ref | STILL_MISSING_VALUES | no denominator derived; exact-improvement cancellation only reduces a numerator component | false | false |
| MHR2380_1_bzero_reduced_numerator | B_zero_flux_remainder | B_rem := B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux | REMAINDER_VECTOR_DEFINED | exact-improvement piece removed from the hard numerator if classification succeeds | false | false |
| MHR2380_2_claim_switch | epsilon_Bzero_abs | abs(B_rem)/M_H_ref | NON_SCORE_READY | requires classified B_rem and positive same-frame M_H_ref | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2380_0_derivation_gain | keep exact-improvement cancellation law | it is a real local algebraic result for theta/Q_tau shifts: exact boundary improvements cancel from delta H_tau under fixed tau | B_zero_flux is reduced to a remainder classification problem, not one undifferentiated mystery term | COMPONENT_DERIVATION_ACCEPTED_CONDITIONALLY | false |
| DEC2380_1_no_global_promotion | do not claim B_zero_flux=0, M_H_ref, local GR or Newton recovery | actual MTS boundary/reference terms are not yet classified and denominator/source-measure bridge is still missing | 2379 Bzero row remains nonclaim but now has a sharper numerator decomposition | GLOBAL_CLAIMS_BLOCKED | false |
| DEC2380_2_no_circling | do not repeat 2339/2340 first-row staging as the next step | older line already staged M_H_ref and parent charge rows; the new work must classify the boundary pieces or derive fixed reference | 2381 selected as boundary term classification/fixed-reference selector, not another generic MHref audit | ANTI_CIRCLING_ROUTE_SELECTED | false |
| DEC2380_3_github_policy | no GitHub update from 2380 | useful private derivation progress, but still no stable public claim | continue private goal until a clean derived/conditional/blocked checkpoint exists | NO_GITHUB | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2380_0_exact_improvement_component | exact boundary improvement cancellation derived under fixed-tau assumptions | PASS_CONDITIONAL_COMPONENT_ONLY | can remove exact-improvement numerator component only after term classification | false |
| CG2380_1_boundary_classification | all actual MTS boundary/reference terms classified as exact or residual | FAIL_PENDING_CLASSIFICATION | B_zero_flux global zero not allowed | false |
| CG2380_2_fixed_reference | fixed H_ref/counterterm selector before readout | FAIL | Delta_ref remains live | false |
| CG2380_3_MHref | positive same-frame M_H_ref denominator | FAIL | normalized local residuals remain non-score-ready | false |
| CG2380_4_source_measure | Hamiltonian charge equals measured source charge | FAIL | Newton/GR source normalization bridge remains blocked | false |
| CG2380_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | private derivation progress only | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2380_0_exact_to_global | declare B_zero_flux=0 because exact improvements cancel | false | the actual MTS boundary/reference stack may include corner, topological, field-dependent tau, unfixed reference, or nonintegrable flux pieces | BRR2380_1_corner;BRR2380_2_topological;BRR2380_3_field_dependent_tau;BRR2380_4_reference;CG2380_1_boundary_classification | false |
| REF2380_1_MHref_from_orbit | fill M_H_ref using observed orbital GM before deriving source-measure bridge | false | this would borrow Newton to prove Newton/GR recovery | TQR2380_5_MHref;TQR2380_6_source_measure;CG2380_4_source_measure | false |
| REF2380_2_reference_cancellation | choose H_ref after seeing B_zero_flux to cancel the residual | false | fixed reference must be selected before source/readout and cannot be a fitted knob | TQR2380_3_fixed_reference;CG2380_2_fixed_reference | false |
| REF2380_3_public_claim | publish 2380 as local GR/Newton evidence | false | component derivation is promising but global denominator and source bridge remain absent | CG2380_3_MHref;CG2380_4_source_measure;CG2380_5_local_GR_Newton | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2380_0_selected | 2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md | classify every actual MTS boundary/reference/improvement term into exact-mu, corner, topological/non-exact, field-dependent-tau, unfixed-reference, or nonintegrable-flux classes | retain a finite B_rem vector with one row per unclassified/non-exact component and keep epsilon_Bzero_abs nonclaim | false |
| NEXT2380_1_parallel | 2381b-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md | derive a source-independent H_ref/counterterm selector fixed before readout | stage Delta_ref_over_MH as a nonclaim residual row | false |
| NEXT2380_2_parallel | 2381c-Y5-R2FR-Htau-integrability-one-form-or-DeltaH-row.md | prove the reduced k_tau one-form is closed on the private branch after exact improvements cancel | stage Delta_H_res/M_H_ref nonclaim component | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2380_00_sources_exist | PASS | all required source paths exist | false |
| VAL2380_01_needles_found | PASS | all source needles found | false |
| VAL2380_02_exact_improvement_law_present | PASS | exact-improvement k_tau cancellation and boundary component rows present | false |
| VAL2380_03_remainder_classes_present | PASS | corner/topological/tau/reference remainders retained | false |
| VAL2380_04_MHref_not_promoted | PASS | M_H_ref rows remain non-score-ready | false |
| VAL2380_05_global_gates_blocked | PASS | global Bzero/MHref/source/local-GR gates remain blocked | false |
| VAL2380_06_next_selected | PASS | boundary term classification selected next | false |
| VAL2380_07_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2380_08_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2380_09_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2380_OVERALL | PASS | 2380 derives the exact-improvement cancellation component, keeps global/local claims blocked, and selects boundary classification/fixed-reference next | false |

## Practical Status

This is a genuine small derivation win.  We are not smuggling GR in; we used the standard current-chain algebra that any
acceptable parent action must satisfy.  The exact-improvement part of the boundary problem can disappear by algebra,
but only after the actual MTS boundary/reference terms are classified as exact improvements with fixed `tau`.  If they
are corners, topological terms, field-dependent readout/surface terms, or unfixed references, they stay as residuals.

The project is therefore slightly less grim than 2379: the boundary blocker has structure now.  But it is not solved.
The next useful shot is to classify the actual boundary/reference terms, not to stage another generic `M_H_ref` row.
