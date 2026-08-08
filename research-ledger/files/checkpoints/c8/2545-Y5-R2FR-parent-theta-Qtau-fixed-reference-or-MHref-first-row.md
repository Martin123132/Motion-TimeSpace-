# 2545 - parent theta/Qtau fixed-reference or M_H_ref first row

## Result

2545 is not another table-circle. It reopens the 2544 parent theta/Qtau/fixed-reference/MHref target, checks the older 2380 attempt, and extracts one real algebraic gain:

`L' = L + d mu`, `theta' = theta + delta mu`, `Q'_tau = Q_tau + i_tau mu`, so

`k'_tau = delta Q'_tau - i_tau theta' = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau`

whenever `tau` and the integration surface are fixed and there are no corner/topological/anomalous pieces. In plain terms: exact boundary improvements do not change the Hamiltonian surface one-form. That gives a conditional zero for the exact-improvement part of `B_zero_flux`.

This does **not** derive `M_H_ref`, `H_ref`, full `theta_MTS`, full `Q_tau^MTS`, the source-measure bridge, or local GR/Newton recovery. The gain is narrower but real: `B_zero_flux` is now split into an exact piece that can cancel algebraically and a remainder vector that must be classified or bounded.

## Source Register

| source_id | source_path | path_exists | needle_found | role |
| --- | --- | --- | --- | --- |
| SRC2545_0_2544_doc | 2544-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md | true | true | 2544 selected parent theta/Qtau/fixed-reference/MHref gate |
| SRC2545_1_2544_validation | source-intake/mts_residuals/P8_Y5_BRR545_2544_VALIDATION.csv | true | true | 2544 validation anchor |
| SRC2545_2_2544_theorem | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BZERO_NOFLUX_THEOREM_AUDIT.csv | true | true | current Bzero theorem obstruction rows |
| SRC2545_3_2544_bound | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BZERO_FIRST_BOUND_ROW.csv | true | true | current nonclaim Bzero numerator/denominator row |
| SRC2545_4_2544_dependency | source-intake/mts_residuals/P8_Y5_NO_SHADOW_2544_BOUNDARY_DENOMINATOR_DEPENDENCY.csv | true | true | current denominator dependency rows |
| SRC2545_5_2380_doc | 2380-Y5-R2FR-parent-theta-Qtau-fixed-reference-or-MHref-first-row.md | true | true | older exact-improvement derivation precedent |
| SRC2545_6_2380_validation | source-intake/mts_residuals/P8_Y5_BRR545_2380_VALIDATION.csv | true | true | 2380 validation anchor |
| SRC2545_7_2380_exact | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv | true | true | exact-improvement cancellation rows |
| SRC2545_8_2380_recheck | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_THETA_QTAU_GATE_RECHECK.csv | true | true | theta/Qtau and MHref recheck precedent |
| SRC2545_9_2380_reduction | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_BZERO_RESIDUAL_REDUCTION.csv | true | true | Bzero residual decomposition precedent |
| SRC2545_10_2380_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2380_NEXT_TARGET.csv | true | true | boundary classification next target precedent |

## Exact Improvement Cancellation Derivation

| row_id | derivation_step | statement | condition | result | remaining_obstruction |
| --- | --- | --- | --- | --- | --- |
| EIC2545_0_setup | exact boundary improvement setup | Let L_prime = L + d mu for a boundary/improvement (n-1)-form mu. | mu is a genuine exact improvement on the same field bundle and boundary class | only the theta and Q_tau representatives shift; equations of motion are unchanged | non-exact, corner, topological, or readout-dependent pieces are not covered |
| EIC2545_1_theta_shift | symplectic potential shift | delta L_prime = E_A delta Phi^A + d(theta + delta mu), so theta_prime = theta + delta mu. | single parent variation exists and delta acts on fields, not on the chosen generator tau | exact improvement contribution to theta is delta mu | parent MTS theta still not globally extracted sector-by-sector |
| EIC2545_2_charge_shift | Noether charge representative shift | J_tau_prime = theta_prime(L_tau Phi) - i_tau L_prime = J_tau + d(i_tau mu), hence Q_tau_prime = Q_tau + i_tau mu up to exact/corner terms. | tau is fixed, the Cartan identity is used in the same boundary class, and corner ambiguities are absent or separately retained | exact improvement contribution to Q_tau is i_tau mu | field-dependent tau, corner terms, and global cohomology can create residuals |
| EIC2545_3_k_invariance | Hamiltonian surface one-form cancellation | k_tau_prime = delta Q_tau_prime - i_tau theta_prime = k_tau + delta(i_tau mu) - i_tau(delta mu) = k_tau when [delta,i_tau]=0. | fixed tau, fixed surface embedding, no anomalous corner/codimension-two contribution | exact boundary improvements do not change delta H_tau | if tau or the surface/readout is field-dependent, a commutator residual remains |
| EIC2545_4_boundary_component | Bzero exact-improvement component | B_zero_flux_exact := integral_S(delta(i_tau mu)-i_tau(delta mu)) = 0 under the fixed-tau exact-improvement clauses. | every candidate Bzero term is classified as exact mu with no corner/topological/field-dependent remainder | the exact-improvement part of B_zero_flux is conditionally zero | classification of actual MTS boundary/reference terms is still missing |
| EIC2545_5_not_MHref | denominator caveat | The cancellation law reduces a numerator channel only; it does not create H_tau, H_ref, M_H_ref, or the source-measure bridge. | none | local GR/Newton remains blocked until M_H_ref and source equality are derived or bounded | positive same-frame M_H_ref and Pi_M J_H = J_M_top + dB_zero |

## Theta/Qtau Gate Recheck

| row_id | gate | status_before_2545 | new_2545_result | claim_effect | next_action |
| --- | --- | --- | --- | --- | --- |
| TQR2545_0_no_circle | same target already attempted | 2339/2340/2380 staged theta_Qtau_Htau_Href/MHref rows but did not promote | do not repeat the first-row table; carry forward the exact boundary-improvement cancellation law | component reduction only, not global closure | classify actual boundary/reference terms into exact/corner/topological/field-dependent classes |
| TQR2545_1_parent_variation | single parent current-chain variation | MISSING_SINGLE_PARENT_VARIATION | exact-improvement algebra is available once a parent variation and mu term are identified | not enough to own theta_MTS globally | sector certificates for EH anchor, matter/source, boundary/reference, extra/projector/glue |
| TQR2545_2_theta_Qtau | theta_MTS and Q_tau^MTS extraction | MISSING_PARENT_THETA_QTAU | boundary exact-improvement shifts are algebraically controlled | Q_tau total remains unowned outside the exact-improvement component | write component ledger: Q_EH, Q_matter/source, Q_boundary_exact, Q_corner, Q_extra, Q_projector |
| TQR2545_3_fixed_reference | fixed H_ref/counterterm before readout | MISSING_FIXED_REFERENCE_CERTIFICATE | exact improvements cannot be used as post-hoc cancellation knobs in delta H | H_ref still must be fixed by a source-independent selector | derive or bound Delta_ref for unfixed/non-exact reference choices |
| TQR2545_4_integrability | H_tau integrability | MISSING_HTAU_INTEGRABILITY | exact improvement does not spoil delta H_tau when [delta,i_tau]=0 | other nonintegrable sector pieces still block H_tau | compute residual one-form Delta_H_res over sector matrix |
| TQR2545_5_MHref | positive same-frame M_H_ref | MISSING_POSITIVE_MHREF | unchanged: denominator missing | Bzero/R_eq/I_commutator/PPN rows remain non-score-ready | fill H_tau-H_ref from parent charge or keep MHref row nonclaim |
| TQR2545_6_source_measure | Hamiltonian charge equals measured source normalization | MISSING_SOURCE_MEASURE_BRIDGE | unchanged: exact boundary-improvement cancellation is not the Poisson/Gauss bridge | Newton/GR recovery cannot be claimed from a conserved charge alone | prove Pi_M J_H = J_M_top + dB_zero or retain R_eq |

## Bzero Residual Reduction

| row_id | component | formula | status | zero_condition | residual_if_condition_fails |
| --- | --- | --- | --- | --- | --- |
| BRR2545_0_exact_improvement | B_exact_improvement | integral_S(delta(i_tau mu)-i_tau(delta mu)) | CONDITIONAL_ZERO_DERIVED | mu exact; tau fixed; surface fixed; no corner anomaly; [delta,i_tau]=0 | Delta_exact_commutator |
| BRR2545_1_corner | B_corner | corner/codimension-two contribution to Q_tau or theta | UNCLASSIFIED_RETAINS_BOUND_ROW | corner term absent or paired by fixed corner convention | epsilon_corner_abs |
| BRR2545_2_topological | B_topological_or_nonexact | closed-but-not-exact or topological boundary representative | UNCLASSIFIED_RETAINS_BOUND_ROW | cohomology class fixed and source-independent or projected silent | epsilon_top_abs |
| BRR2545_3_field_dependent_tau | B_delta_tau | delta(i_tau mu)-i_tau(delta mu) when delta tau != 0 or readout surface moves | UNCLASSIFIED_RETAINS_BOUND_ROW | tau and S_outer locked before variation | epsilon_delta_tau_abs |
| BRR2545_4_reference | B_reference_unfixed | H_ref shift or post-readout counterterm choice | MISSING_FIXED_REFERENCE | H_ref selector fixed before source/readout and independent of fitted residual | Delta_ref_over_MH |
| BRR2545_5_total | B_zero_flux_reduced | B_zero_flux = B_exact_improvement_zero + B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux | REDUCED_NOT_CLOSED | all non-exact/corner/tau/reference/flux pieces vanish or are bounded with M_H_ref | epsilon_Bzero_abs remains non-score-ready |

## M_H_ref First Row Update

| row_id | quantity | formula | status | update_from_2545 | score_ready |
| --- | --- | --- | --- | --- | --- |
| MHR2545_0_denominator | M_H_ref | M_H_ref := H_tau[S_outer] - H_ref | STILL_MISSING_VALUES | no denominator derived; exact-improvement cancellation only reduces a numerator component | false |
| MHR2545_1_bzero_reduced_numerator | B_zero_flux_remainder | B_rem := B_corner + B_topological + B_delta_tau + B_reference + B_nonintegrable_flux | REMAINDER_VECTOR_DEFINED | exact-improvement piece removed from the hard numerator if classification succeeds | false |
| MHR2545_2_claim_switch | epsilon_Bzero_abs | abs(B_rem)/M_H_ref | NON_SCORE_READY | requires classified B_rem and positive same-frame M_H_ref | false |

## Decision Ledger

| row_id | decision | reason | consequence | status |
| --- | --- | --- | --- | --- |
| DEC2545_0_derivation_gain | keep exact-improvement cancellation law | it is a real local algebraic result for theta/Q_tau shifts: exact boundary improvements cancel from delta H_tau under fixed tau | B_zero_flux is reduced to a remainder classification problem, not one undifferentiated mystery term | COMPONENT_DERIVATION_ACCEPTED_CONDITIONALLY |
| DEC2545_1_no_global_promotion | do not claim B_zero_flux=0, M_H_ref, local GR or Newton recovery | actual MTS boundary/reference terms are not yet classified and denominator/source-measure bridge is still missing | 2544 Bzero row remains nonclaim but now has a sharper numerator decomposition | GLOBAL_CLAIMS_BLOCKED |
| DEC2545_2_no_circling | do not repeat generic M_H_ref first-row staging as the next step | older line already staged M_H_ref and parent charge rows; the new work must classify boundary pieces or derive fixed reference | 2546 selected as boundary term classification/fixed-reference selector | ANTI_CIRCLING_ROUTE_SELECTED |
| DEC2545_3_github_policy | no GitHub update from 2545 | useful private derivation progress, but still no stable public claim | continue private goal until a clean derived/conditional/blocked checkpoint exists | NO_GITHUB |

## Claim Gates

| row_id | gate | gate_status | claim_effect |
| --- | --- | --- | --- |
| CG2545_0_exact_improvement_component | exact boundary improvement cancellation derived under fixed-tau assumptions | PASS_CONDITIONAL_COMPONENT_ONLY | can remove exact-improvement numerator component only after term classification |
| CG2545_1_boundary_classification | all actual MTS boundary/reference terms classified as exact or residual | FAIL_PENDING_CLASSIFICATION | B_zero_flux global zero not allowed |
| CG2545_2_fixed_reference | fixed H_ref/counterterm selector before readout | FAIL | Delta_ref remains live |
| CG2545_3_MHref | positive same-frame M_H_ref denominator | FAIL | normalized local residuals remain non-score-ready |
| CG2545_4_source_measure | Hamiltonian charge equals measured source charge | FAIL | Newton/GR source normalization bridge remains blocked |
| CG2545_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | private derivation progress only |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows |
| --- | --- | --- | --- | --- |
| REF2545_0_exact_to_global | declare B_zero_flux=0 because exact improvements cancel | false | the actual MTS boundary/reference stack may include corner, topological, field-dependent tau, unfixed reference, or nonintegrable flux pieces | BRR2545_1_corner;BRR2545_2_topological;BRR2545_3_field_dependent_tau;BRR2545_4_reference;CG2545_1_boundary_classification |
| REF2545_1_MHref_from_orbit | fill M_H_ref using observed orbital GM before deriving source-measure bridge | false | this would borrow Newton to prove Newton/GR recovery | TQR2545_5_MHref;TQR2545_6_source_measure;CG2545_4_source_measure |
| REF2545_2_reference_cancellation | choose H_ref after seeing B_zero_flux to cancel the residual | false | fixed reference must be selected before source/readout and cannot be a fitted knob | TQR2545_3_fixed_reference;CG2545_2_fixed_reference |
| REF2545_3_public_claim | publish 2545 as local GR/Newton evidence | false | component derivation is promising but global denominator and source bridge remain absent | CG2545_3_MHref;CG2545_4_source_measure;CG2545_5_local_GR_Newton |

## Next Target

| row_id | priority | next_file | success_condition | fallback_condition |
| --- | --- | --- | --- | --- |
| NEXT2545_0_selected | selected | 2546-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md | classify every actual MTS boundary/reference/improvement term into exact-mu, corner, topological/non-exact, field-dependent-tau, unfixed-reference, or nonintegrable-flux classes | retain a finite B_rem vector with one row per unclassified/non-exact component and keep epsilon_Bzero_abs nonclaim |
| NEXT2545_1_parallel | parallel | 2546b-Y5-R2FR-fixed-reference-selector-or-Delta-ref-row.md | derive a source-independent H_ref/counterterm selector fixed before readout | stage Delta_ref_over_MH as a nonclaim residual row |
| NEXT2545_2_parallel | parallel | 2546c-Y5-R2FR-Htau-integrability-one-form-or-DeltaH-row.md | prove the reduced k_tau one-form is closed on the private branch after exact improvements cancel | stage Delta_H_res/M_H_ref nonclaim component |

## Validation

| row_id | status | detail |
| --- | --- | --- |
| VAL2545_00_required_sources_exist | PASS | all required source paths exist |
| VAL2545_01_required_needles_found | PASS | all source needles found |
| VAL2545_02_outputs_exist | PASS | all 2545 output files written |
| VAL2545_03_csv_parse | PASS | all generated CSV files parse and contain rows |
| VAL2545_04_exact_improvement_law_present | PASS | exact-improvement k_tau cancellation and boundary component rows present |
| VAL2545_05_remainder_classes_present | PASS | corner/topological/tau/reference remainders retained |
| VAL2545_06_MHref_not_promoted | PASS | M_H_ref rows remain non-score-ready |
| VAL2545_07_global_gates_blocked | PASS | global Bzero/MHref/source/local-GR gates remain blocked |
| VAL2545_08_next_selected | PASS | boundary term classification selected next |
| VAL2545_09_github_blocked | PASS | public claim/GitHub framing blocked |
| VAL2545_10_branch_copies | PASS | all nonclaim branch copies exist |
| VAL2545_11_no_positive_claim_flags | PASS | all generated claim/readiness flags remain negative |
| VAL2545_12_formalization_untouched | PASS | project is not a git worktree here; generator writes only under post-checkpoint-work |
| VAL2545_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2545_OVERALL | PASS | 2545 derives the exact-improvement cancellation component, keeps global/local claims blocked, and selects boundary classification/fixed-reference next |

## Generated Files

- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_SOURCE_REGISTER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_THETA_QTAU_GATE_RECHECK.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_BZERO_RESIDUAL_REDUCTION.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_MHREF_FIRST_ROW_UPDATE.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_DECISION_LEDGER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_CLAIM_GATES.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_REFUSAL_RUNNER.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_NEXT_TARGET.csv`
- `source-intake/mts_residuals/P8_Y5_NO_SHADOW_2545_BRANCH_COPIES.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_2545_VALIDATION.csv`

## Practical Status

This is a genuine small derivation win. We are not smuggling GR in; we used the standard current-chain algebra that any acceptable parent action must satisfy. The exact-improvement part of the boundary problem can disappear by algebra, but only after the actual MTS boundary/reference terms are classified as exact improvements with fixed `tau`. If they are corners, topological terms, field-dependent readout/surface terms, or unfixed references, they stay as residuals.

The project is therefore slightly less grim than 2544: the boundary blocker has structure now. But it is not solved. The next useful shot is to classify the actual boundary/reference terms, not to stage another generic `M_H_ref` row.
