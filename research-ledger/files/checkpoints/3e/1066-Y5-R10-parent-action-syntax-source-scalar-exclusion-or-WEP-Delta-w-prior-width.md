# 1066 — Parent Action Syntax Source-Scalar Exclusion Or WEP Delta-w Prior Width

**Current verdict:** the source-scalar exclusion lemma is now exact as a conditional theorem, but not parent-derived. The block is action-scale/measure ownership: `w_A S_A` is not safely dismissible as a classical normalization.

**Finite branch:** if the theorem fails, the WEP row needs both `Delta_w_TiPt` and `tau_WEP`; the MICROSCOPE bound and material convention alone are not a prediction.

**No shortcut:** relative source weights cannot be absorbed into measured `G`, `tau_WEP` cannot be set to one, and signed cancellation is refused unless a full sourced material/readout model exists.

## Source-Scalar Exclusion Lemma
| lemma_id | claim | formal_statement | attempt_result | gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SSE1066_0_target | exclude inert source-only species scalars from the parent action syntax | If a scalar x_A changes only active gravitational source strength and has no observable/gauge/representation/geometry type, then x_A is not an admissible parent argument. | TARGET_SHARPENED | typing principle must be parent-derived rather than adopted as minimality | false |
| SSE1066_1_object_language_route | typed parent arguments are geometry, matter fields, gauge/current data, representation constants, or universal constants | Arg(S_parent) subset Gamma(E_geom) union Gamma(E_matter) union Conn union Theta_meas union Theta_univ. | CONDITIONAL_TYPING_LEMMA | the exact parent object language is not yet derived from deeper MTS primitives | false |
| SSE1066_2_variation_before_readout | post-variation source selectors cannot generate species weights | T_matter := delta S_matter/delta e_obs before readout/projector reduction; no F((T_A,A)) after variation. | CLEAN_IF_PARENT_VARIATION_ORDER_SIGNED | readout/EFT backreaction closure remains unsigned in the 1055 chain | false |
| SSE1066_3_naturality_route | natural source scalar across ordinary matter coproduct should be common | Nat(Obj(C_matter), R_+) = constants if the ordinary matter category is connected by allowed morphisms. | HELPFUL_CONDITIONAL_ONLY | species components can be disconnected; a family w_A is natural on disconnected/simple-object components | false |
| SSE1066_4_quantum_action_scale_obstruction | multiplying S_A by w_A is not guaranteed to be a harmless classical redundancy | S_A -> w_A S_A can leave classical EOM form invariant while changing Hilbert stress, path-integral weight, and source normalization. | OBSTRUCTION_SURVIVES | needs parent quantum/statistical/action-scale normalization owner | false |
| SSE1066_5_verdict | parent source-scalar exclusion lemma | typed object language + variation-before-readout + common action-scale normalization => no inert species source scalar w_A | CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED | action-scale/measure normalization and parent object-language typing remain unsigned | false |


## Object-Language Typing
| type_id | candidate | type_status | why | wA_effect | signature_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| OLT1066_0_geometry | e_obs, g_obs, connection | admissible | observable geometry and its connection determine matter dynamics and Hilbert variation | species blind if one observed coframe is signed | conditional | false |
| OLT1066_1_matter_fields | Psi_A | admissible | ordinary species fields are dynamical variables | labels are bookkeeping unless source coupling can see them after variation | allowed | false |
| OLT1066_2_measured_parameters | m_A, q_A, representation data, interaction couplings | admissible_if_observable | they affect spectra, scattering, charge/current, or representation labels | not source-only if they are measured in nongravitational channels | current_owner_unsigned | false |
| OLT1066_3_universal_constant | single w_common or kappa_univ | calibration_only | a common multiplier can be absorbed into measured coupling only after universality guards | cannot absorb relative w_A/w_B | guarded_by_common_mode_rule | false |
| OLT1066_4_inert_source_scalar | w_A multiplying only S_A/source strength | rejected_by_candidate_typing | it has no independent observable, gauge, representation, or geometry role | would create WEP-sensitive T_source=sum_A w_A T_A | not_parent_signed | false |
| OLT1066_5_hidden_marker | w(m,D,boundary,A) | rejected_or_residual | marker/domain/boundary scalars can reintroduce labels under another name | must be theorem-forbidden or explicitly bounded | obstruction_active_from_980 | false |
| OLT1066_6_verdict | object-language typing proof | conditional_not_parent_derived | typing kills w_A if accepted, but acceptance still rests on parent syntax/measure axioms | Delta_w_TiPt not theorem-zero yet | open | false |


## Operator-Domain Rule Audit
| rule_id | rule | formal_form | result | obstruction | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ODR1066_0_allowed_coefficient_ring | visible coefficients may depend only on q_loc and fixed representation/topological data | Coeff(O_vis) in Alg[q_loc,Theta_rep,Level_EM] | POWERFUL_IF_SIGNED | same rule was a contract in 1055, not a theorem | false |
| ODR1066_1_continuous_target_obstruction | source scalar target R_+ is continuous | nonconstant invariant I gives w=w0+epsilon I unless invariant algebra/action target is forbidden | OBSTRUCTION_FROM_980 | one untrivialized invariant scalar can feed continuous source weights | false |
| ODR1066_2_species_component_obstruction | species labels may form disconnected components | Nat(C_disconnected,R_+) admits independent constants on components | OBSTRUCTION_SURVIVES | need connected/rich morphism category or explicit no external source-label argument | false |
| ODR1066_3_action_scale_target | action-scale coefficients are not ordinary measured couplings unless parent measure owns them | w_A S_A is a coefficient of the variational weight, not simply a field redefinition | REQUIRES_PARENT_MEASURE_OWNER | quantum/statistical normalization of each matter sector is not signed | false |
| ODR1066_4_verdict | operator-domain source-scalar exclusion | Hom(Arg_parent,R_+^species_source_only)=empty | EXACT_RULE_NOT_DERIVED | requires invariant algebra triviality/no-extension plus parent action-scale ownership | false |


## Field / Measure / Quantum Normalization
| audit_id | issue | effect | required_closure | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| FMQ1066_0_classical_EOM_rescaling | overall S_A multiplier may not change isolated classical equations | tempts false dismissal of w_A | show same multiplier is gauge/quotient redundancy for source and quantum measure too | not_closed | false |
| FMQ1066_1_Hilbert_source_rescaling | overall S_A multiplier rescales Hilbert stress | directly produces T_source=sum_A w_A T_A | ban inert source scalars or prove universal common action normalization | active_obstruction | false |
| FMQ1066_2_path_integral_weight | action scale controls phase/statistical weight | species-dependent hbar/effective action scale would be physically meaningful | single parent hbar/action measure owner for all ordinary matter | parent_owner_missing | false |
| FMQ1066_3_measure_jacobian | species-dependent Jacobian can mimic w_A | hidden measure/coframe descent can reopen source labels | species-blind measure/coframe/boundary descent theorem | parallel_open_gate | false |
| FMQ1066_4_verdict | field/measure/quantum normalization closure | blocks promotion of Delta_w_TiPt=0 | derive a universal parent action-scale normalization or retain finite Delta_w prior | NOT_PARENT_SIGNED | false |


## WEP Delta-w Prior Width Schema
| prior_id | quantity | value_or_status | units | formula_or_requirement | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DWP1066_0_WEP_bound | eta_TiPt_bound | 2.8e-15 | dimensionless | abs(P_WEP_relative_source_weight) <= eta_TiPt_bound | bound_anchor_available | false |
| DWP1066_1_material_pair | AB | TA6V_minus_PtRh10 | convention | Delta_w_TiPt := w_Ti_source - w_Pt_source in the MICROSCOPE convention | context_available | false |
| DWP1066_2_theorem_zero_option | Delta_w_TiPt | MISSING_PARENT_SOURCE_SCALAR_EXCLUSION | dimensionless | Delta_w_TiPt=0 only if SSE1066_5 is parent signed | not_available | false |
| DWP1066_3_finite_prior_width | abs(Delta_w_TiPt) | MISSING_NUMERIC_PRIOR_WIDTH | dimensionless | if tau_WEP is numeric and nonzero, require abs(Delta_w_TiPt) <= 2.8e-15/abs(tau_WEP) | blocked_by_tau_WEP | false |
| DWP1066_4_tau_WEP | tau_WEP | MISSING_LAB_SOURCE_ORBIT_PROJECTION | dimensionless | derive from Earth/source worldtube, spacecraft orbit, observed coframe, and force readout | not_available | false |
| DWP1066_5_product | P_WEP_relative_source_weight | MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP | dimensionless | P = abs(Delta_w_TiPt * tau_WEP); no cancellation/sign trick accepted | not_scoreable | false |


## tau_WEP Projection Contract
| contract_id | input | required_form | current_status | blocks | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TWP1066_0_source_worldtube | Earth/source worldtube and source stress profile | T_source^Earth(x) in observed local frame, with composition/source-weight convention | missing | tau_WEP normalization | false |
| TWP1066_1_orbit_average | MICROSCOPE orbit and averaging convention | time/orbit average of differential acceleration channel in the same convention as eta_AB | missing | projection from local source profile to observed eta_AB | false |
| TWP1066_2_observed_coframe | observed coframe/readout frame | same e_obs for force law, clocks, source variation, and readout | conditional_from_prior_spine | frame consistency of tau_WEP | false |
| TWP1066_3_material_response | test-body material/source tensor | Ti/Pt material response to relative source-weight channel, not just alpha/Coulomb charge | material_pair_only | full Delta_w_TiPt mapping | false |
| TWP1066_4_force_readout | differential acceleration readout map | map from parent source residual to eta_AB with units and sign/absolute convention | missing | scoreable WEP product | false |
| TWP1066_5_no_unity_shortcut | tau_WEP value | numeric sourced value, theorem-zero, or explicit retained nuisance with prior | unity_forbidden | cannot set tau_WEP=1 | false |
| TWP1066_6_no_cancellation | sign/material cancellation | absolute product bound unless a signed material model is fully derived and sourced | absolute_guard_enforced | cannot hide product by cancellation | false |
| TWP1066_7_verdict | tau_WEP projection | tau_WEP = functional[source worldtube, orbit average, e_obs, material tensor, force readout] | PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED | finite Delta_w prior width and WEP runner scoring | false |


## WEP Product Candidate
| prediction_id | arena | product_symbol | product_value | product_units | product_source | inputs_present | required_inputs | derivation_status | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRED1066_0_WEP_Delta_w_prior_width_product | MICROSCOPE_WEP | P_WEP_relative_source_weight | MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP | dimensionless | source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv | eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10 | parent source-scalar theorem-zero OR numeric Delta_w_TiPt prior width;tau_WEP projection;absolute product source | MISSING_DELTA_W_TAUPROJECTION_PRODUCT | false | The finite branch is now explicit: if the theorem fails, Delta_w_TiPt and tau_WEP must be sourced before scoring. |


## WEP Bound Import
| bound_id | arena | product_symbol | bound_value | bound_units | bound_source | source_row | bound_type | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOUND1066_0_WEP_source_charge | MICROSCOPE_WEP | P_WEP_relative_source_weight | 2.8e-15 | dimensionless | source-intake/local_bounds/local_bound_claims.csv | R1_WEP_source_charge | numeric_bound_anchor_nonclaim | true | MICROSCOPE Ti/Pt source-charge proxy bound; only a bound anchor, not a prediction. |


## Runner Status
| runner_id | prediction_rows | bound_rows | valid_prediction_rows | valid_bound_rows | comparison_rows | passed_rows | blocked_or_failed_rows | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR1066_0_WEP_Delta_w_prior_width | 1 | 1 | 0 | 1 | 1 | 0 | 1 | false | 2026-06-14T10:37:13.002585+00:00 |


## Runner Comparisons
| comparison_id | arena | product_symbol | product_value | bound_value | comparison_status | pass_for_claim | issues |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PRODUCT_COMPARE_NO_VALID_PREDICTIONS |  |  |  |  | not_run | false | no valid MTS alpha product prediction rows |


## Claim Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG1066_0_source_scalar_exclusion | inert source-only species scalars are parent-forbidden | false | object-language typing and action-scale ownership are not parent-derived | false | false |
| CG1066_1_Delta_w_theorem_zero | Delta_w_TiPt=0 | false | source-scalar exclusion lemma remains conditional | false | false |
| CG1066_2_finite_Delta_w_prior | finite Delta_w_TiPt prior width is scoreable | false | tau_WEP projection is missing and no numeric Delta_w prior is sourced | false | false |
| CG1066_3_WEP_product_runner | first WEP relative-weight product passes bound | false | runner has valid_prediction_rows=0 | false | false |
| CG1066_4_local_GR_source_branch | local GR/Newton source coupling is derived | false | coupling source-side branch still needs parent action-scale/current/projection closure | false | false |


## Decisions
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC1066_0_lemma_status | source-scalar exclusion is a strong conditional lemma, not a theorem | the proof needs parent object-language typing plus action-scale/measure ownership | attack the quantum/action-scale normalization owner | false |
| DEC1066_1_finite_branch_status | WEP finite branch is now explicitly parameterized by Delta_w_TiPt and tau_WEP | bound and material convention exist, but both prediction inputs are missing | derive tau_WEP or source a numeric prior width only after tau is defined | false |
| DEC1066_2_best_next | next target is parent action-scale normalization or tau_WEP local projection | action-scale closure kills w_A cleanly; tau_WEP is the finite-branch bottleneck if the theorem fails | 1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md | false |


## Source Register
| source_id | relative_path | exists | needle | needle_found | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC1066_0_1065_next | source-intake/mts_residuals/P8_Y5_R10_1065_NEXT_TARGET.csv | true | 1066-Y5-R10-parent-action-syntax-source-scalar-exclusion | true | false |
| SRC1066_1_1065_grammar | source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv | true | PGG1065_5_verdict | true | false |
| SRC1066_2_1065_allowed | source-intake/mts_residuals/P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv | true | AAG1065_4_source_only_species_scalar | true | false |
| SRC1066_3_1065_field | source-intake/mts_residuals/P8_Y5_R10_1065_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv | true | FNL1065_1_action_scale_quantum_weight | true | false |
| SRC1066_4_1065_charge | source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv | true | CIN1065_2_current_owner | true | false |
| SRC1066_5_1065_zero | source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv | true | WTZ1065_4_verdict | true | false |
| SRC1066_6_1065_wep | source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv | true | WEP1065_2_delta_w | true | false |
| SRC1066_7_1065_product | source-intake/mts_residuals/P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv | true | PRED1065_0_WEP_relative_source_weight_first_row | true | false |
| SRC1066_8_1055_parent | source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv | true | PAC1055_4_source_label_forgetting | true | false |
| SRC1066_9_1055_counter | source-intake/mts_residuals/P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv | true | CE1055_3_relative_source_weight | true | false |
| SRC1066_10_980_theorem | source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv | true | NMF980_2_scalar_obstruction_lemma | true | false |
| SRC1066_11_980_counter | source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv | true | CEX980_2_species_kappa | true | false |
| SRC1066_12_989_owner | source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv | true | ELA989_2_current_owner | true | false |
| SRC1066_13_1061_tau | source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv | true | INF1061_4_tau_WEP | true | false |
| SRC1066_14_1061_material | source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv | true | MCON1061_0_test_pair | true | false |
| SRC1066_15_local_bounds | source-intake/local_bounds/local_bound_claims.csv | true | R1_WEP_source_charge | true | false |
| SRC1066_16_393_common | 393-source-normalized-Newtonian-limit-under-identity-closure.md | true | Only a constant, universal, range-independent | true | false |


## Validation
| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V1066_SUMMARY | pass | 1066 parent source-scalar exclusion / WEP Delta_w prior-width validation summary | 2026-06-14T10:37:15.578819+00:00 |
| V1066_1_sources_exist_and_needles | pass | every cited source path exists and every source needle was found | 2026-06-14T10:37:13.003960+00:00 |
| V1066_2_exclusion_not_promoted | pass | source-scalar exclusion remains conditional | 2026-06-14T10:37:13.004000+00:00 |
| V1066_3_object_typing_blocks_wA | pass | object-language typing rejects w_A only as candidate grammar | 2026-06-14T10:37:13.004010+00:00 |
| V1066_4_operator_obstructions_written | pass | operator-domain continuous/species obstructions are written | 2026-06-14T10:37:13.004035+00:00 |
| V1066_5_action_scale_obstruction_written | pass | field/measure/quantum action-scale obstruction is retained | 2026-06-14T10:37:13.004060+00:00 |
| V1066_6_delta_w_schema_missing_inputs | pass | Delta_w theorem-zero and tau_WEP inputs remain missing | 2026-06-14T10:37:13.004072+00:00 |
| V1066_7_tau_contract_written | pass | tau_WEP projection contract is written but not derived | 2026-06-14T10:37:13.004082+00:00 |
| V1066_8_prediction_nonclaim | pass | WEP Delta_w product prediction remains nonclaim | 2026-06-14T10:37:13.004090+00:00 |
| V1066_9_bound_anchor_numeric | pass | WEP bound anchor is numeric | 2026-06-14T10:37:13.004100+00:00 |
| V1066_10_runner_refuses_placeholder | pass | strict runner refuses missing Delta_w/tau product | 2026-06-14T10:37:13.004107+00:00 |
| V1066_11_claim_gates_blocked | pass | all source-scalar/WEP/local-GR claim gates remain blocked | 2026-06-14T10:37:13.004117+00:00 |
| V1066_12_next_target_written | pass | next target selects action-scale normalization or tau projection | 2026-06-14T10:37:13.004124+00:00 |
| V1066_13_generated_files_in_post_checkpoint | pass | all generated files are under post-checkpoint-work | 2026-06-14T10:37:13.009855+00:00 |
| V1066_14_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T10:37:15.578802+00:00 |


## Next Target
| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md | derive the parent action-scale/measure normalization that forbids species-dependent S_A multipliers; if it fails, start filling tau_WEP as a real local source/orbit/readout projection instead of a unity shortcut. | single hbar/action-measure owner, classical EOM vs Hilbert stress distinction, path-integral/action-scale typing, species-blind measure descent, tau_WEP source-worldtube/orbit/readout functional | setting w_A=1 by convention, setting tau_WEP=1, absorbing relative weights into measured G, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits | false |

