# 1163 — Y5/R10 topological Cperp source contract and edge-bound runner stub

**Current verdict:** the topological/projector branch is now executable as a strict acquisition contract, but it is still not a claim. `C_perp=(I-P_D)C` is only a candidate until the parent `C` object, `P_D`, `d_rel`, relative closedness, and `B_C` primitive are sourced.

**Main progress:** the edge-bound runner stub now has a hard input schema and refuses to evaluate or claim while the 1162 rows remain source-anchor-only. This is good discipline: we have a machine gate that prevents us from accidentally turning placeholders into a local/R10 result.

**Best next target:** source or derive the parent `C/P_D/d_rel` trio first. If that stalls, attack the first edge theorem/bound directly, starting with `C_corner=0` or `d_S(F epsilon)=0/bounded`.

## Source register

| source_id | relative_path | needle | exists | needle_found | role |
| --- | --- | --- | --- | --- | --- |
| SRC1163_0_1162_next | source-intake/mts_residuals/P8_Y5_R10_1162_NEXT_TARGET.csv | NEXT1162_0_1163 | True | True | handoff requiring strict Cperp source contract and no-claim runner stub. |
| SRC1163_1_1162_candidate_choice | source-intake/mts_residuals/P8_Y5_R10_1162_STRICT_CPERP_CANDIDATE_CHOICE.csv | CAND1162_0_topological_projector_residual | True | True | single selected acquisition candidate C_perp=(I-P_D)C. |
| SRC1163_2_1162_edge_fill | source-intake/mts_residuals/P8_Y5_R10_1162_EDGE_BOUND_FIRST_SOURCE_FILL.csv | EFS1162_0_C_corner | True | True | first edge-bound source-fill row set imported into the runner stub. |
| SRC1163_3_1161_source_pack | source-intake/mts_residuals/P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv | CDSRC1161_0_Cperp_definition | True | True | older explicit missing-source pack for Cperp, P_D, d_rel, closedness, and selector. |
| SRC1163_4_272_quotient | 272-quotient-configuration-principle-from-topological-projector.md | [C] = C / ker(P_D). | True | True | quotient route supporting the candidate contract shape. |
| SRC1163_5_272_relative_exactness | 272-quotient-configuration-principle-from-topological-projector.md | Cperp residuals are relative-exact representatives | True | True | conditional exactness route and its open burden. |
| SRC1163_6_1020_weighted_stokes | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | ETB1020_1_weighted_Stokes_identity | True | True | edge-bound formula source for corner and surface derivative terms. |
| SRC1163_7_1020_BC_primitive | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | BXP1020_2_exact_primitive | True | True | primitive row showing the exact primitive remains not derived. |
| SRC1163_8_1020_cohomology | 1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md | BDC1020_2_relative_cohomology | True | True | harmonic edge mode zero-or-bound requirement. |
| SRC1163_9_1019_projector | 1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md | SP1019_6_projector_zero_or_bound | True | True | projector source bound requirement for Qbar_CXH. |
| SRC1163_10_1040_QX | 1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md | BX1040_2_candidate_QX | True | True | boundary charge formula contract tied to edge readout. |
| SRC1163_11_1040_cocycle | 1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md | KBC1040_0_contract | True | True | boundary cocycle source-contract row. |
| SRC1163_12_1144_selector | source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv | RC1144_2_same_parent_law | True | True | local-trivial/FLRW-active branch selector remains a missing parent-law requirement. |
| SRC1163_13_1146_no_flux | source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv | NF1146_6_verdict | True | True | epsilon no-flux sibling gate remains blocked. |

## Strict Cperp source contract

| contract_id | clause | strict_requirement | candidate_value | current_status | missing_piece | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CTC1163_0_candidate_lock | single C_perp candidate | Carry only C_perp=(I-P_D)C or equivalent topological/projector residual; no candidate switching. | C_perp=(I-P_D)C | ACQUISITION_CANDIDATE_ONLY | parent-signed definition not yet supplied | False |
| CTC1163_1_parent_C_object | parent C object | Define C as a specific parent field/cochain/form with bundle, degree, orientation, units, and variation rule. | C is the object projected by P_D | MISSING_PARENT_C_OBJECT | actual C variable owner and degree | False |
| CTC1163_2_PD_owner | P_D projector ownership | Source P_D as an idempotent, metric-independent or explicitly metric-dependent projector with delta P_D rule. | P_D from quotient/topological projector route | PARTIAL_SHAPE_SUPPORT_ONLY | projector definition, domain rule, idempotence proof, and variation | False |
| CTC1163_3_Cperp_definition | C_perp definition | After C and P_D are sourced, define C_perp=(I-P_D)C and state whether it is bulk, boundary, or relative-pair valued. | C_perp=(I-P_D)C | FORMULA_STUB_NOT_DEFINITION | C and P_D must be parent-owned first | False |
| CTC1163_4_form_degree_units | form degree and units | Give form degree k, boundary degree k-1, dimensions, normalization, and integration measure. | unspecified | MISSING_FORM_DEGREE_AND_UNITS | degree, units, and normalization | False |
| CTC1163_5_relative_pair | relative domain pair | Specify local domain U, boundary S, pullback i_star, boundary class, support/collar conditions, and allowed variations. | (U,S) relative pair | PARTIAL_BOUNDARY_SHAPE_SUPPORT | C-sector relative pair and allowed boundary class | False |
| CTC1163_6_drel_complex | d_rel operator | Instantiate d_rel on Omega_C^k(U,S), including signs, nilpotency, boundary pullback, and source terms. | standard relative differential shape only | MISSING_DREL_OPERATOR_FOR_C_SECTOR | actual complexes and sign convention | False |
| CTC1163_7_closedness_identity | relative closedness | Prove d_rel C_perp=0 or identify nonzero source/support terms to bound. | d_rel C_perp=0 desired | MISSING_CPERP_CLOSEDNESS_PROOF | Noether/Bianchi/Euler identity with boundary/source terms | False |
| CTC1163_8_exactness_or_harmonic_bound | relative exactness or harmonic bound | Either source C_perp=d_rel B_C with h_C=0, or supply h_C and residual bounds. | Cperp residuals are relative-exact representatives | CONDITIONAL_ROUTE_OPEN | B_C primitive and H_rel certificate | False |
| CTC1163_9_BC_primitive | B_C primitive | Write B_C or b_C explicitly and define the norm used in the weighted-Stokes edge bound. | B_C primitive placeholder | NOT_DERIVED | primitive formula and norm | False |
| CTC1163_10_edge_readout | edge readout formula | Use weighted Stokes to compute or bound corner, derivative-weight, primitive, harmonic, residual, and cocycle terms. | |Q_C| <= |C_corner| + ||d_S(F eps)|| ||B_C|| + |h_C| + |r_C| + |K_boundary Qbar_CXH| | FORMULA_STUB_ONLY | all numeric/theorem-zero edge inputs | False |
| CTC1163_11_branch_selector | local trivial / FLRW active selector | Prove from one parent law when local branch has trivial C_perp while FLRW/domain branch is active. | same-parent-law selector required | MISSING_PARENT_BRANCH_SELECTION_LAW | no hand-switch theorem | False |
| CTC1163_12_no_frame_shortcut | no hidden c_g/frame shortcut | Do not rename frame/A_g/Xhat residual as C_perp unless a no-shadow matter quotient theorem is independently sourced. | frame residual excluded from C_perp definition | GUARD_ACTIVE | no-shadow theorem still missing | False |
| CTC1163_13_claim_promotion | claim promotion gate | Only promote after C, P_D, d_rel, closedness/exactness, B_C, edge terms, selector, and no-shadow gates close. | promotion blocked | BLOCKED | multiple parent and edge inputs missing | False |

## Edge-bound input schema

| input_id | quantity | required_kind | units_requirement | current_input_status | numeric_value | theorem_zero_certificate | runner_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EIS1163_0_C_corner | C_corner | zero_theorem_or_nonnegative_abs_numeric_bound | declared_by_boundary_charge_convention | SOURCE_ANCHOR_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | additive_edge_bound_term | False |
| EIS1163_1_norm_dS_Feps | norm_dS_Feps | closed_weight_zero_theorem_or_nonnegative_dual_surface_norm | dual_surface_norm | SOURCE_ANCHOR_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | multiplicative_weight_derivative_factor | False |
| EIS1163_2_norm_bC | norm_bC | explicit_BC_primitive_norm_or_zero_certificate | dual_to_norm_dS_Feps | BLOCKED_BY_CPERP_PRIMITIVE | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | multiplicative_primitive_norm_factor | False |
| EIS1163_3_harmonic_edge_abs | harmonic_edge_abs | H_rel_zero_theorem_or_nonnegative_abs_bound | boundary_charge_units | SOURCE_ANCHOR_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | additive_harmonic_bound_term | False |
| EIS1163_4_residual_edge_abs | residual_edge_abs | residual_zero_theorem_or_nonnegative_abs_bound | boundary_charge_units | SOURCE_ANCHOR_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | additive_residual_bound_term | False |
| EIS1163_5_K_boundary | K_boundary | cocycle_zero_theorem_or_nonnegative_operator_bound | boundary_generator_units | FORMULA_CONTRACT_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | multiplicative_cocycle_operator_factor | False |
| EIS1163_6_Qbar_CXH | Qbar_CXH | projector_zero_theorem_or_nonnegative_abs_source_bound | dimensionless_after_MH_normalization | SOURCE_ANCHOR_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | multiplicative_projected_source_factor | False |
| EIS1163_7_branch_selector | local_trivial_FLRW_active_selector | parent_branch_function_or_boolean_theorem | boolean_theorem_or_branch_functional | SHAPE_SUPPORT_ONLY_VALUE_MISSING | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | branch_gate_not_numeric_term | False |
| EIS1163_8_epsilon_no_flux_sibling | epsilon_domain_flux_zero_or_bound | epsilon_no_flux_theorem_or_nonnegative_profile_bound | alpha3_product_convention | SIBLING_GATE_BLOCKED | MISSING_NUMERIC_VALUE | MISSING_THEOREM_ZERO_CERTIFICATE | sibling_flux_gate | False |

## Edge-bound formula stubs

| formula_id | formula | status | evaluation | valid_for_claim |
| --- | --- | --- | --- | --- |
| EBF1163_0_edge_bound_formula | |Q_C| <= |C_corner| + ||d_S(F eps)||_* ||B_C||_* + |h_C| + |r_C| + |K_boundary Qbar_CXH| + epsilon_flux_sibling | FORMULA_STUB_ONLY_INPUTS_MISSING | not_evaluated | False |
| EBF1163_1_zero_route | Q_C=0 only if corner=0, d_S(F eps)=0 or B_C=0, h_C=0, r_C=0, K_boundary Qbar_CXH=0, selector local-trivial, and epsilon flux gate closes | CONDITIONAL_ONLY_NOT_MET | blocked | False |
| EBF1163_2_finite_bound_route | Finite local residual may be bounded only after every additive/multiplicative term has sourced units and values | INPUT_SCHEMA_READY_VALUES_MISSING | blocked | False |

## Runner stub results

| run_id | test | input_rows | status | claim_allowed | detail |
| --- | --- | --- | --- | --- | --- |
| RUN1163_0_load_edge_schema | load 1162 edge-fill rows into strict runner schema | 9 | SCHEMA_LOADED_INPUTS_MISSING | False | schema is usable but every edge quantity still needs a numeric bound or theorem-zero certificate |
| RUN1163_1_claim_refusal | refuse Cperp/local claim when required inputs are missing | 9 | PASS_REFUSED_CLAIM_AS_DESIGNED | False | claim_allowed remains false because no required edge input is sourced |
| RUN1163_2_formula_evaluation | evaluate edge-bound formula only if all inputs are sourced | 9 | NOT_EVALUATED_BY_GATE | False | runner intentionally does not compute a numeric residual from placeholder rows |

## No-cheat guards

| guard_id | guard | failure_mode_prevented | status | valid_for_claim |
| --- | --- | --- | --- | --- |
| GUA1163_0_no_candidate_switching | Only the topological/projector C_perp candidate may be carried into this branch. | mixing J_rel/domain current or frame residual definitions into one symbol | ACTIVE | False |
| GUA1163_1_no_frame_cg_renaming | Frame/A_g/Xhat residuals cannot be relabelled as C_perp without a separate no-shadow theorem. | hiding the common-frame coupling problem inside notation | ACTIVE | False |
| GUA1163_2_no_numeric_placeholders | MISSING, anchor-only, symbolic, or nonclaim rows cannot enter a numeric edge-bound result. | accidental fake local/R10 pass | ACTIVE | False |
| GUA1163_3_no_zero_by_exactness_alone | Exactness does not zero the edge charge unless corner, weight derivative, harmonic, residual, and cocycle terms also close. | Stokes theorem misuse | ACTIVE | False |
| GUA1163_4_no_local_claim | No local GR/Newton/R10/PPN/WEP/clock/orbital claim follows from this stub. | overclaiming from a runner harness | ACTIVE | False |

## Claim gates

| gate_id | gate | required_evidence | current_status | claim_allowed |
| --- | --- | --- | --- | --- |
| CG1163_0_candidate_source_contract | C, P_D, C_perp, form degree, units, variation rule, and d_rel are parent-sourced | CTC1163_1 through CTC1163_7 closed with valid source paths | BLOCKED | False |
| CG1163_1_exactness_or_bound | C_perp exactness, B_C primitive, H_rel/harmonic, residual, and boundary terms are zeroed or bounded | CTC1163_8 through CTC1163_10 plus EIS1163 rows sourced | BLOCKED | False |
| CG1163_2_runner_claim_allowed | edge-bound runner returns claim_allowed=true | all schema rows have numeric values or theorem-zero certificates | BLOCKED_RUNNER_REFUSES_CLAIM | False |
| CG1163_3_branch_and_no_shadow | same-parent branch selector and no hidden c_g/frame shortcut theorem close | CTC1163_11 and CTC1163_12 closed | BLOCKED | False |
| CG1163_4_local_claim_promotion | local GR/Newton/R10/PPN/WEP/clock/orbital promotion | all previous gates pass plus arena projections | BLOCKED_NO_LOCAL_CLAIM | False |

## Decision ledger

| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1163_0_contract_status | strict_source_contract_written_but_not_satisfied | the topological/projector candidate is now legally specified as an acquisition branch, but C, P_D, d_rel, closedness, and B_C remain source-missing | source or derive one hard parent clause rather than broaden the branch | False |
| D1163_1_runner_status | edge_bound_runner_stub_refuses_claim | every edge input is schema-visible but still lacks a numeric bound or theorem-zero certificate | fill first edge term or prove a zero condition | False |
| D1163_2_best_next | target_parent_C_PD_drel_source_hunt_or_first_edge_zero_certificate | this is the narrowest route that can turn the candidate from a scaffold into either a theorem branch or a finite bound | 1164 should attempt C/P_D/d_rel source closure first; if it fails, attack C_corner or d_S(F eps) zero/bound | False |

## Validation

| check_id | result | detail | claim_allowed |
| --- | --- | --- | --- |
| V1163_0_sources_exist | pass | all cited local source paths exist and needles are found | False |
| V1163_1_contract_complete_shape | pass | strict source contract includes all required Cperp clauses | False |
| V1163_2_contract_not_satisfied | pass | contract remains intentionally unsatisfied/nonclaim | False |
| V1163_3_edge_schema_complete | pass | edge schema has one row for every 1162 edge-fill quantity | False |
| V1163_4_no_invented_edge_values | pass | runner stub contains no numeric values or theorem-zero certificates | False |
| V1163_5_runner_refuses_claim | pass | runner refuses edge/local claim while inputs are missing | False |
| V1163_6_guards_active | pass | candidate, frame-shortcut, placeholder, exactness, and local-claim guards are active | False |
| V1163_7_claim_gates_blocked | pass | all claim gates remain blocked | False |
| V1163_8_no_claim_rows | pass | all generated rows remain nonclaim | False |
| V1163_9_next_target | pass | 1164 handoff targets parent C/P_D/d_rel source hunt or first edge zero certificate | False |
| V1163_10_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | False |
| V1163_11_csv_parse | pass | all 1163 CSV outputs parse cleanly | False |
| V1163_12_formalization_untouched | pass | generator writes no outputs under formalization-workbench | False |
| V1163_SUMMARY | pass | 1163 converts the selected topological/projector Cperp branch into a strict source contract and no-claim edge-bound runner stub | False |

## Next target

| next_id | next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT1163_0_1164 | 1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md | try to source or derive the parent C object, P_D projector ownership, and C-sector d_rel complex; if not closed, fill the first edge-bound zero/bound certificate such as C_corner or d_S(F epsilon) | C object; P_D owner; form degree; d_rel signs; closedness/source terms; C_corner theorem/bound; dS_Feps theorem/bound; runner dry-run | candidate switching; invented edge numbers; frame residual renaming; c_g zero claim; local-GR claim; GitHub; formalization edits | False |
