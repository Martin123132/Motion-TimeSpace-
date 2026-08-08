# 2383 - parent selector equation for Sigma_ref or Delta-ref source pack

## Result

2383 takes the leap from "the selector must be source-blind" to the actual mathematical route that could make it true.

If a parent boundary/reference equation

`E_Sigma(Sigma_ref; B_class, C_top, tau, e_infty) = 0`

contains no source/material/GM/readout/residual inputs, then differentiating with respect to source gives

`(partial E_Sigma / partial Sigma_ref) D_source Sigma_ref + partial_source E_Sigma = 0`.

If `partial_source E_Sigma=0` and the selector Hessian/operator is invertible after quotienting gauge/topological zero
modes, the implicit-function theorem gives `D_source Sigma_ref=0`.  Then 2382's chain rule gives
`D_source B_ref=D_source H_ref=0`.

That is a serious theorem shape.  But current MTS does **not** yet provide `E_Sigma`, the no-forbidden-input proof, the
nondegeneracy certificate, or positive same-frame `M_H_ref`.  So no fixed-reference, `Delta_ref=0`, Newton, local-GR, or
public claim follows.  The fallback `Delta_ref` source pack remains live.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2383_00_2382_doc | 2382_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2382-Y5-R2FR-fixed-boundary-class-and-Href-selector-or-Delta-ref-row.md | true | true | 2382 selected parent selector equation as next target | false |
| SRC2383_01_2382_theorem | 2382_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv | true | true | source-blind chain-rule theorem and nonpromotion gate | false |
| SRC2383_02_2382_grammar | 2382_grammar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2382_SELECTOR_INPUT_GRAMMAR.csv | true | true | allowed/forbidden selector input grammar | false |
| SRC2383_03_999_doc | 999_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md | true | true | older fixed-branch selector equation gap | false |
| SRC2383_04_999_parent_contract | 999_parent_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv | true | true | parent action selector contract rows | false |
| SRC2383_05_999_selector_attempt | 999_selector_attempt | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv | true | true | fixed-branch selector attempt failure rows | false |
| SRC2383_06_1000_schema | 1000_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1000_STRICT_INPUT_SCHEMA.csv | true | true | fallback Delta_ref source-pack schema | false |
| SRC2383_07_1001_radius_audit | 1001_radius_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv | true | true | surface-domain selector no-retune blocker | false |
| SRC2383_08_545_doc | 545_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md | true | true | minimal reference action contract not parent-owned | false |

## Implicit Selector Theorem

| row_id | step | statement | condition | result | missing_in_current_corpus | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| IST2383_0_setup | selector equation setup | Let E_Sigma(Sigma_ref; B_class, C_top, tau, e_infty)=0 be the parent boundary/reference selector equation. | E_Sigma contains no source/material/GM/readout/residual inputs | Sigma_ref is selected by parent structural data, not by fit | explicit E_Sigma equation and source path | false |
| IST2383_1_source_free_equation | source-free equation derivative | D_source E_Sigma = (partial E_Sigma/partial Sigma_ref) D_source Sigma_ref + partial_source E_Sigma. | partial_source E_Sigma=0 because no forbidden source inputs appear | Hessian/operator times D_source Sigma_ref is zero | no-marker/no-GM/no-readout certificate for E_Sigma | false |
| IST2383_2_non_degeneracy | implicit function nondegeneracy | If partial E_Sigma/partial Sigma_ref is invertible on the allowed boundary class after gauge/topological zero modes are quotiented, then D_source Sigma_ref=0. | selector Hessian/operator has no source-dependent flat branch or uncontrolled zero mode | source-blindness follows from the implicit function theorem | nondegeneracy/unique-branch certificate | false |
| IST2383_3_reference_zero | Delta_ref source component | D_source Sigma_ref=0 implies D_source B_ref=0 and D_source H_ref=0 by the 2382 chain-rule criterion. | same selector controls B_ref, H_ref, surface S0 and counterterm B_ct | partial_source Delta_ref=0 conditionally | parent-owned Sigma_ref and counterterm/surface provenance | false |
| IST2383_4_failure_modes | failure modes | If E_Sigma contains source labels, GM calibration, post-readout residual data, moving surfaces, or degenerate branch choices, the theorem fails. | none | Delta_ref components must be source-packed rather than zeroed | finite component numerators and M_H_ref | false |
| IST2383_5_verdict | current verdict | The implicit-function route is mathematically sharp but not parent-signed in current MTS. | E_Sigma source-free plus nondegenerate branch certificate are not present | selector equation theorem is not promoted; Delta_ref source pack remains required | E_Sigma, no-forbidden-input proof, nondegeneracy certificate, M_H_ref | false |

## Selector Equation Candidates

| row_id | candidate_equation | allowed_inputs | forbidden_inputs | current_status | would_close | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEC2383_0_boundary_stationarity | delta_{Sigma_ref} S_parent_boundary = 0 | boundary class, tau, coframe, corner/topology data | source labels, observed GM, fitted mass, residual value | CANDIDATE_NOT_IN_CORPUS | FRT2382 source-blindness if source-free and nondegenerate | Delta_ref_counterterm_component_over_MH | false |
| SEC2383_1_Ward_charge_lock | Ward/diffeomorphism charge normalization fixes reference branch | generator tau, asymptotic symmetry class, boundary orientation | measured source charge before Hilbert/topological equality | CANDIDATE_NOT_IN_CORPUS | pre-readout H_ref selector | R_eq/I_commutator remain parallel | false |
| SEC2383_2_topological_selector | C_top(Sigma_ref)=C_top^0 with fixed relative cohomology class | topological class and boundary homology | material/source composition or orbital normalization | CANDIDATE_PARTIAL_ONLY | topological part of selector if also unique and same-frame | epsilon_top_abs and Delta_ref_surface_component_over_MH | false |
| SEC2383_3_stationary_vacuum_reference | reference branch is the unique source-free stationary solution in the same boundary class | zero-source stationary branch and asymptotic coframe | using reference-only zero as evidence for current source branch | CANDIDATE_RISKY_UNOWNED | reference selector if uniqueness and no source retuning are proved | reference-only zero refused; Delta_ref source pack | false |
| SEC2383_4_verdict | current MTS parent selector equation | source-free parent structural data | all source/readout/calibration labels | NOT_DERIVED | none yet | source-pack Delta_ref components | false |

## Delta Ref Source Pack

| row_id | component | formula | required_fields | current_value | status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DSP2383_0_source_derivative | partial_source_Delta_ref | finite derivative or theorem_zero=true with PARENT_SIGNED_SELECTOR_TRUE | source_parameter;derivative_value;units;source_path;equation_ref;extraction_method | MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO | REQUIRED_IF_SELECTOR_THEOREM_FAILS | false | false |
| DSP2383_1_selector_hessian | selector_non_degeneracy_or_branch_leak | norm(Psi_zero_mode_or_branch_drift)/M_H_ref or theorem_zero via invertible Hessian | Hessian/operator;gauge quotient;zero_mode_basis;branch_id;source_path | MISSING_SELECTOR_HESSIAN | REQUIRED_FOR_IMPLICIT_THEOREM | false | false |
| DSP2383_2_forbidden_input_audit | selector_forbidden_input_leak | sum_abs(partial_forbidden Sigma_ref * forbidden_scale)/M_H_ref | GM/material/residual/readout derivatives;scales;units;source paths | MISSING_FORBIDDEN_INPUT_DERIVATIVES | REQUIRED_IF_NO_MARKER_PROOF_FAILS | false | false |
| DSP2383_3_total | Delta_ref_source_pack_total | abs(partial_source_Delta_ref*Delta_source_scale)/M_H_ref + selector_branch_leak + forbidden_input_leak | all component values;positive same-frame M_H_ref;absolute no-cancellation guard | COMPONENTS_MISSING | NONCLAIM_SOURCE_PACK_STAGED | false | false |

## Decision Ledger

| row_id | decision | reason | consequence | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC2383_0_math_gain | keep implicit-function selector theorem as the right route | a source-free nondegenerate parent selector equation would prove D_source Sigma_ref=0 instead of assuming it | fixed-reference problem is now an equation/nondegeneracy target, not a vague convention | CONDITIONAL_THEOREM_ACCEPTED | false |
| DEC2383_1_no_promotion | do not promote fixed-reference theorem | current corpus lacks E_Sigma, no-forbidden-input proof, nondegenerate branch certificate and M_H_ref | Delta_ref source pack remains live | THEOREM_NOT_PARENT_SIGNED | false |
| DEC2383_2_next | attack boundary stationarity equation or source-pack Delta_ref | SEC2383_0 is the least hand-wavy parent-action route; if it cannot be written, source-pack is the honest fallback | 2384 should try to write delta_{Sigma_ref}S_boundary=0 explicitly or fill source-pack inputs | SELECT_2384_BOUNDARY_STATIONARITY | false |

## Claim Gates

| row_id | gate | gate_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2383_0_implicit_selector_route | implicit-function source-blindness theorem shape | PASS_CONDITIONAL_SHAPE_ONLY | valid target for future parent action | false |
| CG2383_1_Esigma | explicit parent selector equation E_Sigma=0 | FAIL | D_source Sigma_ref not proved | false |
| CG2383_2_non_degeneracy | nondegenerate unique reference branch after quotienting gauge/topological zero modes | FAIL | branch drift can source Delta_ref | false |
| CG2383_3_no_forbidden_inputs | selector equation has no source/GM/material/readout/residual inputs | FAIL_UNSIGNED | source-blindness remains conditional | false |
| CG2383_4_MHref | positive same-frame M_H_ref | FAIL | Delta_ref source pack cannot be scored | false |
| CG2383_5_local_GR_Newton | local GR/Newton recovery | FAIL_NONCLAIM | reference/source-measure/denominator gates remain open | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2383_0_assume_selector | assume Sigma_ref is source-blind without E_Sigma | false | 2383 derives the route but requires the parent equation and nondegeneracy certificate | IST2383_0_setup;IST2383_2_non_degeneracy;CG2383_1_Esigma | false |
| REF2383_1_degenerate_branch | use a degenerate reference branch and still declare D_source Sigma_ref=0 | false | zero modes/branch drift can carry source dependence unless quotient/nondegeneracy is proved | IST2383_2_non_degeneracy;DSP2383_1_selector_hessian | false |
| REF2383_2_source_pack_score | score Delta_ref source pack now | false | component numerators, source scales, Hessian, forbidden-input derivatives and M_H_ref are missing | DSP2383_0_source_derivative;DSP2383_1_selector_hessian;DSP2383_3_total;CG2383_4_MHref | false |

## Next Target

| row_id | next_file | success_condition | fallback_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2383_0_selected | 2384-Y5-R2FR-boundary-stationarity-equation-for-Sigma-ref-or-source-pack-fill.md | write an explicit source-free delta_{Sigma_ref} S_parent_boundary=0 equation and nondegeneracy/no-forbidden-input certificate | fill Delta_ref source-pack component rows with finite numerators, units, source paths and valid_for_claim=false | false |
| NEXT2383_1_parallel | 2384b-Y5-R2FR-selector-Hessian-zero-modes-or-branch-leak-row.md | prove the selector Hessian is invertible after quotienting gauge/topological zero modes | retain selector_branch_leak nonclaim component | false |
| NEXT2383_2_parallel | 2384c-Y5-R2FR-same-frame-MHref-sidecar-or-denominator-row.md | derive positive same-frame M_H_ref needed to score every normalized row | keep normalized local residuals non-score-ready | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2383_00_sources_exist | PASS | all required source paths exist | false |
| VAL2383_01_needles_found | PASS | all source needles found | false |
| VAL2383_02_implicit_theorem_present | PASS | implicit-function nondegeneracy and reference-zero rows present | false |
| VAL2383_03_stationarity_candidate_present | PASS | boundary stationarity candidate selected | false |
| VAL2383_04_source_pack_nonready | PASS | Delta_ref source pack rows remain non-score-ready | false |
| VAL2383_05_global_claims_blocked | PASS | global/local gates remain blocked | false |
| VAL2383_06_csv_parse | PASS | generated CSVs parse and have rows | false |
| VAL2383_07_no_claim_flags | PASS | no generated row has valid_for_claim=true | false |
| VAL2383_08_formalization_untouched_by_script | PASS | script writes only post-checkpoint-work outputs | false |
| VAL2383_09_next_selected | PASS | boundary stationarity equation selected next | false |
| VAL2383_OVERALL | PASS | 2383 derives the implicit-function selector route, refuses promotion without E_Sigma/nondegeneracy/MHref, and selects boundary stationarity next | false |

## Practical Status

This is a proper forward step.  We are no longer merely demanding that `H_ref` be fixed; we now have the exact parent
selector equation route and the mathematical proof shape that would make source-blindness follow.  The monster is still
alive because `E_Sigma` is not written, but it has a neck now.

Next best strike: `2384`, try to write `delta_{Sigma_ref} S_parent_boundary = 0` explicitly.  If that cannot be done,
stop pretending and fill the `Delta_ref` source pack.
