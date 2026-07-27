# 999 Y5 R10: B_ref Fixed-Branch Selector or Delta_ref Source-Coefficient Provenance

Status: `Y5_R10_999_Bref_fixed_branch_selector_not_signed_source_component_provenance_gate_staged_nonclaim`

Claim ceiling: no parent-owned `B_ref` fixed-branch selector, no `B_ref` source-blindness theorem, no `partial_source Delta_ref=0`, no score-ready `Delta_ref_source_component_over_MH`, no `Delta_ref` pass, no `RC994_0=0`, no `deltaH` curl closure, no `FB554_0=0`, no Newton/PPN/R10/R11/orbit/local-GR pass.

## Readout

999 asks the right selector question: what parent rule forces the reference branch before source/readout exists? The current corpus has a useful `B_ref` scaffold, but not a selector equation. That means source-blindness is still a conditional route, not a current theorem.

The gain is concrete: any future finite `Delta_ref_source_component_over_MH` row now needs exact provenance for `partial_source_Delta_ref`, source scale, `B_ref` rule, and same-frame `M_H_ref`. No magic pocket, no calibration rabbit.

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 998_doc | handoff selecting fixed-branch selector or source coefficient provenance | true | true | 998-Y5-R10-Bref-source-blindness-theorem-or-Delta-ref-source-component-row.md |
| 998_theorem_attempt | source-blind theorem attempt | true | true | source-intake/mts_residuals/P8_Y5_R10_998_BREF_SOURCE_BLIND_THEOREM_ATTEMPT.csv |
| 998_leakage | source leakage channels | true | true | source-intake/mts_residuals/P8_Y5_R10_998_SOURCE_LEAKAGE_CHANNEL_AUDIT.csv |
| 998_countermodels | countermodels blocking notation-only proof | true | true | source-intake/mts_residuals/P8_Y5_R10_998_COUNTERMODEL_LEDGER.csv |
| 998_component_template | source component template | true | true | source-intake/mts_residuals/P8_Y5_R10_998_DELTA_REF_SOURCE_COMPONENT_TEMPLATE.csv |
| 998_refusal | strict anti-cheat policy | true | true | source-intake/mts_residuals/P8_Y5_R10_998_STRICT_REFUSAL_LEDGER.csv |
| 997_derivative_component | partial_source Delta_ref component audit | true | true | source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv |
| 667_action_ansatz | candidate B_ref and fixed branch scaffold | true | true | source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv |
| 667_variation | reference derivative ledger | true | true | source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv |
| 668_boundary_lock | fixed branch lock failure | true | true | source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv |
| 950_source_countermodel | source/species countermodel warning | true | true | source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv |

## Fixed-Branch Selector Attempt

| selector_id | claim | mathematical_form | would_close | current_evidence | current_status | missing_signature | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FBS999_0_selector_definition | a fixed-branch selector Sigma_ref is defined before source/readout | Sigma_ref(Phi_parent) -> (gamma_ref,tau_ref,C_top,B_ct,S0) and B_ref=B_ref[Sigma_ref] | turns B_ref into fixed branch data instead of a chosen subtraction | 667 defines H_ref and B_ref scaffolds | definition_level_only | parent action/constraint that uniquely selects Sigma_ref | false |
| FBS999_1_parent_variational_owner | Sigma_ref is selected by parent Euler/Ward/topological conditions | delta S_parent/delta Sigma_ref=0 or C_top/topology/stationarity fixes Sigma_ref | prevents post-fit reference selection | 668 marks B_ref fixed branch as fail_current_claim | not_signed | explicit selector equation and boundary condition from parent action | false |
| FBS999_2_source_independence | selector is independent of matter/source labels and fitted source parameters | D_source Sigma_ref=0; D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=D_source S0=0 | partial_source Delta_ref=0 by chain rule | 998 records the source-blindness theorem as conditional only | not_signed | no source labels/material markers/GM calibration in selector inputs | false |
| FBS999_3_surface_domain_lock | reference surface/domain is fixed independently of the source choice | D_source S0=0 and linked surfaces are selected by the same parent domain rule | blocks source dependence through moving surfaces rather than B_ref integrand | 998 leakage audit flags S0=S0[source] as unexcluded | not_signed | source-blind linking-surface/domain selector | false |
| FBS999_4_no_GM_calibration | selector cannot use observed GM, fitted mass, or source-current normalization | partial_{GM_obs,M_fit,kappa_A,M_H_ref} Sigma_ref=0 | prevents reference subtraction from absorbing the source mass we need to derive | 998 countermodel CM998_1 remains legal | not_signed | source-current equality/Gauss readout kept downstream of selector | false |
| FBS999_5_counterterm_convention | counterterm convention is fixed before readout | B_ct=B_ct[Sigma_ref] and D_source B_ct=0 | prevents source-dependent counterterm cancellation | 998 flags B_ct[source,fit,calibration] as unexcluded | not_signed | counterterm convention with source path and equation reference | false |
| FBS999_6_same_frame_denominator | selector and denominator use same tau/coframe/frame | tau_ref=tau_Q=tau_source and M_H_ref>0 in that same frame | makes Delta_ref_source_component_over_MH meaningful | 997/998 keep M_H_ref missing and forbid orbital GM substitution | not_signed | same-frame Hamiltonian/source mass owner | false |
| FBS999_7_verdict | fixed-branch selector makes B_ref source-blind for current MTS | FBS999_0 through FBS999_6 all signed => partial_source Delta_ref=0 | the source component of Delta_ref theorem-zero | all decisive selector clauses remain unsigned | fail_current_claim | parent-owned Sigma_ref and same-frame denominator | false |

## Future Parent-Action Selector Contract

| contract_id | future_parent_action_must_supply | minimum_form | acceptance_test | current_fill | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FBC999_0_selector_function | a named selector function Sigma_ref | Sigma_ref: boundary/topology/stationarity data -> gamma_ref,tau_ref,C_top,B_ct,S0 | selector inputs contain no source/material/GM/calibration labels | MISSING_PARENT_SELECTOR | false |
| FBC999_1_variation_or_constraint | variation/constraint equation fixing Sigma_ref | E_Sigma=0, Ward condition, topological class, or stationarity condition | equation is written in parent variables with source path/equation reference | MISSING_SELECTOR_EQUATION | false |
| FBC999_2_source_blind_derivatives | componentwise derivative-zero certificate | D_source gamma_ref=D_source tau_ref=D_source C_top=D_source B_ct=D_source S0=0 | each component is theorem-zero or source-backed bounded | MISSING_SOURCE_BLIND_COMPONENT_CERTIFICATE | false |
| FBC999_3_no_marker_clause | no material/source marker clause | delta Sigma_ref/delta(m_A,theta_A,kappa_A,composition_A)=0 | excludes 950/998 source-weight countermodels | MISSING_NO_MARKER_SELECTOR_CLAUSE | false |
| FBC999_4_no_GM_calibration | no measured-GM/fitted-source calibration in selector | partial_{GM_obs,M_fit,M_H_ref} Sigma_ref=0 before source-current equality | no orbital/observed GM appears in B_ref or B_ct provenance | MISSING_NO_GM_CALIBRATION_CERTIFICATE | false |
| FBC999_5_counterterm_provenance | counterterm convention fixed before readout | B_ct formula, units, boundary convention, source path, equation reference | D_source B_ct=0 or finite sourced source-component residual | MISSING_COUNTERTERM_CONVENTION | false |
| FBC999_6_MHref_sidecar | same-frame positive M_H_ref sidecar | M_H_ref;units;tau_id;frame_id;source_path;equation_ref | positive Hamiltonian denominator; no orbital GM substitution | MISSING_SAME_FRAME_MHREF | false |

## Delta_ref Source-Coefficient Provenance Gate

| provenance_id | coefficient | target_row | required_provenance | acceptance_rule | current_value | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DCP999_0_partial_source_derivative | partial_source_Delta_ref | Delta_ref_source_component_over_MH | source_parameter;derivative_value;units;source_path;equation_ref;extraction_method;valid_for_claim | numeric derivative or theorem_zero=true with parent-signed selector | MISSING_NUMERIC_DERIVATIVE_OR_THEOREM_ZERO | false | false |
| DCP999_1_source_scale | Delta_source_scale | Delta_ref_source_component_over_MH | definition of source variation scale; units; source_path;equation_ref | source parameter must be physically defined, not chosen to shrink the residual | MISSING_SOURCE_SCALE | false | false |
| DCP999_2_Bref_rule | B_ref_rule | Delta_ref_source_component_over_MH | B_ref formula; boundary convention; counterterm convention; source_path;equation_ref | formula must be fixed before source/readout and contain no hidden GM/source labels | MISSING_PARENT_BREF_RULE | false | false |
| DCP999_3_MHref | M_H_ref | Delta_ref_source_component_over_MH | positive same-frame Hamiltonian source mass; units; tau/frame ids; source_path;equation_ref | same-frame and not orbital GM imported before Gauss/source-current proof | MISSING_SAME_FRAME_MHREF | false | false |
| DCP999_4_component_bound | Delta_ref_source_component_over_MH | Delta_ref_source_component_over_MH | partial_source_Delta_ref;Delta_source_scale;M_H_ref;absolute-value rule;source_path;valid_for_claim | abs(partial_source_Delta_ref*Delta_source_scale)/M_H_ref with no cancellation credit | MISSING_COMPONENT_INPUTS | false | false |

## Runner Readiness

| runner_id | object | ready | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DCR999_0_schema_ready | Delta_ref source-component finite row | true | required fields and absolute-value rule are specified | false | false |
| DCR999_1_values_ready | numeric/theorem-zero inputs | false | partial_source_Delta_ref, source scale, B_ref rule, and M_H_ref are missing | false | false |
| DCR999_2_no_silent_zero | zero-theorem switch | false | selector theorem not parent-signed | false | false |
| DCR999_3_no_downstream_score | Delta_ref/RC994_0/local-GR score | false | this is one source-component row only and the denominator/source-current route remains open | false | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CG999_0_fixed_branch_selector | B_ref fixed-branch selector is parent-owned | false | false | selector equation, no-marker clause, no-GM calibration, counterterm convention, and M_H_ref sidecar are missing |
| CG999_1_source_blind_Bref | B_ref is source-blind | false | false | source-blindness depends on the unsigned selector |
| CG999_2_source_component_score | Delta_ref_source_component_over_MH is score-ready | false | false | coefficient provenance rows are MISSING and score_ready=false |
| CG999_3_downstream | Delta_ref, RC994_0, deltaH, FB554_0, Newton/PPN/R10/local-GR pass | false | false | 999 only locks selector/provenance requirements and does not close the residual |

## Decision Ledger

| decision_id | decision | reason | effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC999_0_selector_attempt | do not promote the fixed-branch selector theorem | the current corpus has a useful B_ref scaffold but not the parent selector equation or no-marker/GM/counterterm sidecars | B_ref source-blindness and partial_source Delta_ref remain unclaimed | false |
| DEC999_1_provenance_gate | stage finite source-component provenance requirements | if the selector cannot be signed, the source component must be bounded from sourced inputs | future numeric row cannot be scored without exact provenance | false |
| DEC999_2_next_target | move to a runnable strict provenance checker | the schema is now explicit enough to refuse bad rows automatically | 1000 can build the refusal/validation runner for any proposed Delta_ref source coefficient | false |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V999_0_sources | pass | all cited local source files exist and expected needles are found | 2026-06-14T03:23:21.197256+00:00 |
| V999_1_selector_attempt_fail_closed | pass | fixed-branch selector theorem is attempted but not promoted | 2026-06-14T03:23:21.197269+00:00 |
| V999_2_parent_contract_missing | pass | future parent-action selector contract is explicit and missing-marked | 2026-06-14T03:23:21.197273+00:00 |
| V999_3_provenance_missing | pass | finite source-component provenance rows are missing and score_ready=false | 2026-06-14T03:23:21.197275+00:00 |
| V999_4_runner_readiness_safe | pass | schema is ready but values/claims are refused | 2026-06-14T03:23:21.197278+00:00 |
| V999_5_claim_gates_safe | pass | selector, source-blindness, source component score, and downstream claims are blocked | 2026-06-14T03:23:21.197281+00:00 |
| V999_6_decision_written | pass | strict provenance runner selected next | 2026-06-14T03:23:21.197283+00:00 |
| V999_7_next_target_written | pass | 1000 target row is present and nonclaim | 2026-06-14T03:23:21.197285+00:00 |
| V999_8_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T03:23:21.197288+00:00 |
| V999_READY | pass | 999 B_ref fixed-branch selector/provenance validation summary | 2026-06-14T03:23:21.197290+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1000-Y5-R10-Delta-ref-source-coefficient-strict-provenance-runner.md | build a strict runner that refuses Delta_ref_source_component rows unless selector theorem or finite coefficient provenance is complete | partial_source_Delta_ref, Delta_source_scale, B_ref rule, M_H_ref, units, equation/source paths, theorem-zero switch, no-cancellation guard | invented coefficients, zero-by-closure, Delta_ref pass, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action, formalization-workbench edits | false |
