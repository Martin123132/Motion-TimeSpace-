# 956 Y5 R10: Source-Side GR Reduction Spine And Left-Hand EH Gate Map

Status: `Y5_R10_956_source_side_spine_consolidated_left_hand_EH_Newton_gates_mapped_nonclaim`

Claim ceiling: `structural_map_only_no_source_side_claim_no_EH_claim_no_Newton_claim_no_local_GR_claim`

## Result

This checkpoint gives the cleanest local-GR bridge map so far.

The source side is no longer foggy. The conditional route is: one observed coframe, no species-label source functor, total Hilbert variation of one matter action, no source-only relative `w_A`, and one common `kappa_univ` calibrated to measured `G`. If those parent clauses are signed, the right-hand side becomes the ordinary GR/Newton matter source.

But that is only half the bridge. The left-hand side still needs EH/operator selection, extra-sector silence, one-parameter no-hair, measured-GM/worldtube calibration, constant source normalization, and full PPN vector completion. EH baseline machinery exists, but it does not silence MTS extra sectors by itself.

So the honest state is: source-side spine sharpened; full GR/Newton reduction not claimable yet.

```text
RHS route: kappa_univ T_total, conditional but sharp.
LHS route: EH + zero/bounded residuals, still open.
Newton route: needs measured-GM/worldtube calibration plus no extra Poisson hair.
```

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 955_doc | handoff: conditional source-side spine and relative w_A obstruction | true | true | 955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md |
| 955_validation | previous checkpoint validation | true | true | source-intake/mts_residuals/P8_Y5_BRR545_955_VALIDATION.csv |
| 955_minimal_matter | minimal matter/source coupling lemma | true | true | source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv |
| 955_prefactor_classification | common-mode vs relative species source prefactors | true | true | source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv |
| 953_source_functor_theorem | conditional no-species-label uniqueness theorem | true | true | source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv |
| 954_label_forgetting | label-forgetting by total Hilbert variation | true | true | source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv |
| 912_EH_baseline | EH metric-core baseline and extra-omega warning | true | true | source-intake/mts_residuals/P8_Y5_R10_912_EH_CORE_BASELINE.csv |
| 529_source_calibrated_EH_stack | source-calibrated EH/PPN proof-stack rungs | true | true | source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv |
| 529_source_calibrated_EH_blockers | highest-priority EH/source-normalization blockers | true | true | source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS.csv |
| 482_local_GR_promotion_gates | local GR residual promotion gates | true | true | source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv |
| 505_EH_requirements | local EH reduction requirements | true | true | source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv |
| 655_EH_premise_audit | EH-only premise audit | true | true | source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv |

## Source-Side GR/Newton Spine

| spine_id | condition | current_status | if_closed | remaining_blocker |
| --- | --- | --- | --- | --- |
| SSG956_0_observed_coframe | one observed coframe/metric used by matter, source variation, clocks, photons, and readout | conditional_from_prior_contracts | ordinary source and observables refer to the same geometry | readout-frame and hidden-sector variations still need parent closure through PPN order |
| SSG956_1_no_species_source_functor | source functor has no species-label argument | conditional_theorem_from_953 | relative source couplings cannot be formed | parent label-forgetting/source-domain clause unsigned |
| SSG956_2_total_Hilbert_source | active ordinary source is total Hilbert/coframe derivative of one matter action | conditional_variational_mechanism_from_954 | species decomposition is bookkeeping rather than separate source channels | source-only species prefactors w_A must be absent or bounded |
| SSG956_3_minimal_matter_action | matter dynamics and active source come from the same minimal matter functional | exact_contract_not_parent_signed_from_955 | relative w_A/w_B source residual is removed by construction | schema has not been derived from deeper quotient/no-extra-slot principle |
| SSG956_4_common_kappa_calibration | one common coupling is calibrated to measured Newton G | common_mode_harmless_but_measured_GM_chain_open | common normalization becomes units rather than a new composition force | measured-GM/worldtube/source-normalization chain remains open in older gates |
| SSG956_5_source_side_verdict | source-side GR/Newton matter term | conditional_spine_sharp_not_claimable | right-hand side of local GR/Newton limit is structurally standard | DeltaJ_hidden and DeltaJ_species must be theorem-zero or bounded; left-hand EH still separate |

## Left-Hand EH/Newton Gate Map

| gate_id | required_condition | current_status | blocks | next_action |
| --- | --- | --- | --- | --- |
| LHG956_0_EH_core_selection | local exterior metric/coframe operator reduces to Einstein-Hilbert plus harmless Lambda/background | not_parent_derived | EH-only local GR claim and Newtonian source-normalized promotion | derive metric-only second-order EH selection or retain executable R11/nonEH vector |
| LHG956_1_extra_sector_silence | motion/time/domain/memory/projector/boundary/connection sectors have no projected local exterior stress/charge | active_primary_obstruction | Hamiltonian charge integrability, PPN vector, and local no-hair family | prove gauge/topological/no-hair silence or retain each residual with sourced bounds |
| LHG956_2_one_parameter_nohair | compact exterior is a one-parameter mass family with no independent scalar/vector/domain/boundary hair | not_derived | Newtonian potential and PPN beta/gamma source identification | derive sector no-hair theorems or fill residual vector rows |
| LHG956_3_measured_GM_calibration | EH mass parameter equals measured orbital GM and Hilbert/projected source charge | not_derived | Newtonian mechanics reduction even if EH operator is selected | derive Gauss/Poisson/worldtube source-measure calibration or keep M_eff residual |
| LHG956_4_constant_source_normalization | mass/source normalization has no time/radius/species/range/frame/domain derivative | not_derived | fifth-force, Gdot, WEP/source normalization, and radial-hair claims | combine source-side 953-955 with radial/domain/boundary no-hair gates |
| LHG956_5_PPN_completion | observed weak-field expansion reaches GR PPN values with no quadratic leakage | failed_for_claim_current_vector | local GR claim even if leading Newtonian order looks good | fill or theorem-zero every local residual vector component without cancellation |

## Hidden-Current Bypass Gates

| hidden_id | channel | risk | current_status | required_closure | feeds_gate |
| --- | --- | --- | --- | --- | --- |
| HCG956_0_relative_species_prefactor | relative w_A/w_B or kappa_A/kappa_B source weight | composition-dependent source normalization | live_residual_from_955 | parent no-source-prefactor theorem or sourced epsilon_A bound | SSG956_3; LHG956_4; PPN/WEP source channels |
| HCG956_1_marker_domain_boundary_weight | marker/domain/boundary/post-readout disguised source prefactor | kappa_A returns after apparent label-forgetting | hidden_spurion_channel_from_955 | no-spurion theorem or explicit residual vector rows | SSG956_5; LHG956_1; LHG956_4 |
| HCG956_2_nonHilbert_current | spin/torsion/boundary/non-Hilbert active current | bypasses Hilbert-current uniqueness and changes source or PPN charges | parallel_open_gate_from_955_and_912 | absent/exact/projected silent theorem or retained bound row | SSG956_5; LHG956_1; LHG956_5 |
| HCG956_3_omega_extra | extra-sector symplectic flux | EH baseline charge form does not integrate to full MTS Hamiltonian charge | active_obstruction_from_911_912 | omega_extra=0/gauge/topological/no-flux or bounded charge residual | LHG956_1; LHG956_2; LHG956_5 |
| HCG956_4_R11_nonEH_operator | non-EH/R11 operator vector | conserved non-EH tensors alter beta/gamma/preferred-frame observables | template_or_unfilled_in_prior_gates | EH-only theorem or executable nonEH coefficient vector with bounds | LHG956_0; LHG956_5 |
| HCG956_5_worldtube_source_measure | source-measure/worldtube/Gauss calibration | metric mass parameter not equal to measured orbital GM | open_high_priority_blocker | derive worldtube source law and measured-GM calibration | SSG956_4; LHG956_3; Newtonian reduction |

## Reduction Equation Spine

| equation_id | equation | GR_limit_condition | Newton_limit_condition | current_status |
| --- | --- | --- | --- | --- |
| REQ956_0_full_local_equation | E_MTS[g,e_obs,X,D,...] = kappa_univ T_total + DeltaJ_species + DeltaJ_hidden | E_MTS -> G_munu+Lambda g_munu and DeltaJ_species=DeltaJ_hidden=0 | weak-field 00 equation gives nabla^2 U = 4 pi G_ref rho_obs with mu_EH=G_ref M_obs | framework_spine_only |
| REQ956_1_left_hand_residual_split | E_MTS = E_EH + DeltaE_R11 + DeltaE_q_loc + DeltaE_boundary + DeltaE_domain + DeltaE_connection + ... | each DeltaE term theorem-zero/gauge/topological/no-hair or separately bounded | no extra Poisson source, no radial hair, no range dependence | residual_split_required_not_closed |
| REQ956_2_source_residual_split | T_source = T_total + DeltaT_w + DeltaT_NH + DeltaT_boundary | DeltaT_w=DeltaT_NH=DeltaT_boundary=0 or retained below bounds | source mass is conserved, universal, and calibrated to measured GM | source_side_conditional_from_953_955 |
| REQ956_3_PPN_vector_condition | Delta_PPN = (gamma-1, beta-1, alpha1, alpha2, alpha3, xi, Gdot/G, range_terms, ...) | every component is zero/theorem-derived or scored below bound without cancellation | leading Newtonian piece is not promoted until source normalization and local residual vector pass | promotion_gates_fail_for_claim |

## Decision Ledger

| decision_id | topic | result | reason | next_action | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| DEC956_0_source_side | source-side GR/Newton spine | conditional_spine_consolidated | 953-955 now give a coherent route from one matter action to one total Hilbert source with common kappa | do not claim source closure until no-source-prefactor and hidden-current clauses are parent-signed or bounded | false |
| DEC956_1_left_hand | left-hand EH/Newton gate | still_open_high_pressure | EH baseline exists, but EH selection, extra-sector silence, one-parameter no-hair, measured GM, and PPN completion remain open | attack left-hand EH parent selection or produce executable residual vector rows | false |
| DEC956_2_project_overview | overall local GR bridge | not_claimable_but_structurally_clearer | the bridge is now split into exact source-side clauses and left-hand operator/no-hair/calibration gates | write a parent-local-GR spine ledger and choose the next highest-leverage derivation: EH selection vs measured-GM calibration | false |

## Claim Gate

| gate_id | claim | current_evidence | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- |
| CGATE956_0_source_side_GR | source side reduces to GR/Newton matter source | conditional spine only; relative w_A and hidden currents remain open | false | false |
| CGATE956_1_left_hand_EH | left-hand local field equation is EH in observed frame | EH baseline conditional; extra-sector and R11 blockers active | false | false |
| CGATE956_2_Newtonian_limit | MTS derives Newtonian mechanics locally | source-side structure sharpened but measured-GM/no-hair gates open | false | false |
| CGATE956_3_full_local_GR_PPN | local GR/PPN vector passes | promotion gates fail for claim and residual vector rows remain unfilled | false | false |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V956_0_sources_exist_and_needles | pass | all 956 source paths exist and needles are present | 2026-06-13T22:43:59.878499+00:00 |
| V956_1_prior_955_clean | pass | P8_Y5_BRR545_955_VALIDATION.csv clean | 2026-06-13T22:43:59.878512+00:00 |
| V956_2_source_spine_ready | pass | source-side GR/Newton conditional spine consolidated | 2026-06-13T22:43:59.878515+00:00 |
| V956_3_source_spine_nonclaim | pass | source-side spine remains nonclaim | 2026-06-13T22:43:59.878518+00:00 |
| V956_4_left_hand_gates_mapped | pass | left-hand EH/Newton gates mapped | 2026-06-13T22:43:59.878520+00:00 |
| V956_5_hidden_current_gates_mapped | pass | hidden-current bypass gates mapped | 2026-06-13T22:43:59.878523+00:00 |
| V956_6_reduction_equation_spine_mapped | pass | reduction equation residual split mapped | 2026-06-13T22:43:59.878526+00:00 |
| V956_7_decisions_nonclaim | pass | decision ledger remains nonclaim | 2026-06-13T22:43:59.878528+00:00 |
| V956_8_claim_gates_false | pass | all claim gates remain false | 2026-06-13T22:43:59.878531+00:00 |
| V956_9_next_target_selected | pass | 957 parent-local-GR spine ledger selected | 2026-06-13T22:43:59.878533+00:00 |
| V956_10_no_claims_promoted | pass | all generated rows are valid_for_claim=false | 2026-06-13T22:43:59.878536+00:00 |
| V956_11_formalization_workbench_untouched | pass | formalization_changed_after_start=0 | 2026-06-13T22:43:59.878539+00:00 |
| V956_12_validation_rows_ready | pass | validation table constructed | 2026-06-13T22:43:59.878541+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md | turn the 956 map into a parent-local-GR spine ledger and select the next high-leverage derivation branch: EH-only operator selection or measured-GM/worldtube calibration | source-side clauses, left-hand EH gates, Newtonian weak-field conditions, measured-GM chain, residual-vector blockers, next derivation decision | invented coefficients, local-GR claim, GitHub action, formalization-workbench edits | false |
