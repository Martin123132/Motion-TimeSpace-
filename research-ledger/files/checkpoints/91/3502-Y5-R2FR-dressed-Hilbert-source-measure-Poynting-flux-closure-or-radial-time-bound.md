# 3502 - Dressed Hilbert Source Measure, Poynting Flux Closure or Radial-Time Bound

## Current Verdict
- **Derivation progress:** `D_r M_H=0` and `D_t M_H=0` now have explicit conditional zero proofs from total Hilbert/Noether charge closure and boundary flux balance.
- **EM/Poynting clarified:** ordinary stationary Maxwell stress dresses `M_H`; radiative, background, nonminimal, Hodge, normalization, or readout leakage becomes an explicit coefficient.
- **Still not a claim:** the required parent signatures are not all signed: observed Hodge/coframe, unique Maxwell normalization, charge/current owner, total source current closure, and extra-sector silence remain gates.
- **Next best move:** derive the observed Hodge/Maxwell owner and total Hilbert current closure, because that is the shortest path from conditional theorem to actual MTS local-GR progress.

## Dressed Source Flux Closure Theorem
| theorem_id | claim_piece | statement | result | remaining_gap | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DFC3502_0_dressed_source_definition | M_H is dressed Hilbert source charge | The source mass that can reduce to Newton is not bare rest mass; it is the Hamiltonian/Hilbert charge of the total observed source, including binding and field dressing. | DEFINITION_LOCK_ADOPTED_FOR_LOCAL_BRANCH | MTS must parent-sign Pi_M, tau, e_obs, and source pullback as the same object before this is a claim | False |
| DFC3502_1_total_Hilbert_current_closure | radial flux closure | If the local exterior annulus is source-free and the total projected Hilbert current is closed, the dressed charge is independent of linking radius. | CONDITIONAL_ZERO_FOR_D_R_MH | extra-sector current, metric projector stress, nonEH charge and frame/domain leakage still have to vanish or be bounded | False |
| DFC3502_2_time_flux_closure | time drift closure | If the local branch is stationary with no net flux through the timelike boundary, the dressed charge is time-independent. | CONDITIONAL_ZERO_FOR_D_T_MH | stationarity, radiative leakage, background-field flux and moving boundary terms must be parent-silent or coefficient-filled | False |
| DFC3502_3_Maxwell_stress_dressing | ordinary EM belongs inside M_H | For minimally coupled Maxwell on the observed geometry, EM energy, pressure, momentum density and Poynting flow are components of T_EM and therefore dress M_H rather than becoming an extra fifth force. | CONDITIONAL_ZERO_FOR_ORDINARY_STATIONARY_EM_EXTRA | observed Hodge/coframe, EM normalization, charge/current normalization and unique F2 owner remain unsigned | False |
| DFC3502_4_matter_EM_exchange_cancels_in_total | internal Lorentz exchange is not source leakage | Matter and EM exchange energy-momentum internally, but only the total stress-current must be conserved; internal Lorentz exchange is not a loss of M_H. | INTERNAL_EXCHANGE_CANCELS_CONDITIONALLY | the charged matter current owner and representation/charge normalization must be fixed | False |
| DFC3502_5_cross_term_fallback | when EM becomes mu_extra | Nonminimal MTS-EM terms, independent EM action multipliers, hidden gauge-kinetic functions, radiative Poynting leakage, or wave/relic background flux are not absorbed into M_H unless parent-owned. | COEFFICIENT_FALLBACK_REQUIRED_IF_PRESENT | fill P8_EM_Poynting_source_flux_or_cross_term_vector.csv rows or derive their parent exclusion | False |

## Radial and Time M_H Status
| status_id | target | candidate_result | blocking_terms | observable_pressure | artifact_if_failed | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RT3502_0_radial_MH | D_r M_H | 0 if d(Pi_M J_H)=0 on the source-free exterior annulus | Delta_nonEH;Delta_PiM_metric;Delta_extra;Delta_frame;Delta_cal;Delta_PPN | partial_r_ln_mu_obs;R10_alpha_lambda;PPN_beta | P8_radial_mu_profile_or_zero.csv | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | False |
| RT3502_1_time_MH | D_t M_H | 0 if tau is stationary and total boundary energy flux vanishes | radiative_Poynting_flux;background_field_flux;moving_boundary;time_dependent_memory;reference_drift | Gdot_over_G;clock_drift;orbital_GMdot | P8_time_drift_residual_or_zero.csv | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | False |
| RT3502_2_EM_ordinary | epsilon_EM_extra ordinary minimal Maxwell | 0 if S_EM is minimally coupled to e_obs and its stress is inside T_total | observed_Hodge_unsigned;EM_normalization_unsigned;charge_current_owner_unsigned | Maxwell stress;clock energy;source coupling;alpha owner | P8_EM_Poynting_source_flux_or_cross_term_vector.csv | CONDITIONAL_DRESSING_ROUTE | False |
| RT3502_3_EM_leakage | epsilon_EM_extra leakage | retained coefficient unless parent excludes or flux is zero | nonminimal_XF2;w_EM;hidden_gauge_kinetic;radiative_flux;readout_regeneration | Gdot;WEP;clock;PPN;source normalization | P8_EM_Poynting_source_flux_or_cross_term_vector.csv | RETAINED_COEFFICIENT_VECTOR_CREATED | False |

## EM Poynting Source-Flux Vector
| component_id | source | symbol | candidate_value | zero_condition | status | observable_links | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EMF3502_0_minimal_bound_field_stress | ordinary_minimal_Maxwell_bound_fields | epsilon_EM_bound | 0_CONDITIONAL_INSIDE_MH | same observed Hodge/coframe, minimal Maxwell variation, stationary bound fields | CONDITIONAL_ZERO_ROUTE | Maxwell_stress;Newton_source_charge | False |
| EMF3502_1_radiative_poynting_flux | radiative_or_background_Poynting_flux | Phi_EM_rad/(G_ref M_H) | MISSING_FLUX_OR_ZERO_THEOREM | stationary isolated local branch with no net radiative/background flux | RETAINED_FLUX_COEFFICIENT_REQUIRED | Gdot_over_G;clock_drift;source_time_hair | False |
| EMF3502_2_nonminimal_XF2 | nonminimal_MTS_EM_cross_term | C_XF2 | MISSING_PARENT_EXCLUSION_OR_BOUND | parent operator domain forbids hidden-visible EM coefficient morphisms | RETAINED_OPERATOR_COEFFICIENT_REQUIRED | alpha_EM;clock;WEP;R10;PPN | False |
| EMF3502_3_EM_normalization_multiplier | independent_EM_action_multiplier | w_EM | MISSING_UNIQUE_F2_OR_ALPHA_OWNER | unique Maxwell curvature norm plus charge/current/fine-structure owner | RETAINED_NORMALIZATION_COEFFICIENT_REQUIRED | alpha_EM;binding_energy;WEP;clock | False |
| EMF3502_4_observed_Hodge_flow_rule | Hodge_or_constitutive_background | Delta_Hodge_EM | MISSING_OBSERVED_HODGE_PARENT_SIGNATURE | MTS derives the observed EM Hodge/flow rule from the same e_obs/q data | RETAINED_HODGE_FLOW_COEFFICIENT_REQUIRED | Maxwell_limit;light_cone;clock;PPN | False |
| EMF3502_5_matter_EM_internal_exchange | matter_EM_Lorentz_exchange | epsilon_internal_exchange | 0_CONDITIONAL_IN_TOTAL_STRESS | matter and EM are varied in the same parent action with the same charge current | CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS | source_charge;WEP;EM_matter_coupling | False |
| EMF3502_6_readout_radiative_regeneration | effective_readout_or_loop_regeneration | C_EM_readout | MISSING_READOUT_CLOSURE_OR_BOUND | radiative/readout closure preserves visible-sector pullback and unique EM owner | RETAINED_EFFECTIVE_COEFFICIENT_REQUIRED | clock;WEP;alpha_EM;binding_response | False |

## Decisions
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3502_0_MH_dressing | Adopt dressed Hilbert charge as the only acceptable local Newton source definition. | Bare mass loses field energy and binding; the exterior field sees the total Hamiltonian/Hilbert charge. | False | False |
| DEC3502_1_radial_time_progress | D_r M_H and D_t M_H now have conditional zero proofs, not just placeholders. | Stokes/Noether closure gives radial silence; Hamiltonian flux balance gives time silence, but only after parent current and flux premises are signed. | False | False |
| DEC3502_2_EM_stress_policy | Ordinary stationary Maxwell stress is source dressing; nonminimal/radiative Poynting leakage is explicit mu_extra. | This uses the Poynting vector as a diagnostic instead of treating EM as either ignored or magically solved. | False | False |
| DEC3502_3_next_choke | Next target is observed Hodge/Maxwell owner plus total Hilbert current closure. | That is the parent signature needed to turn the conditional Poynting/Hilbert theorem into actual MTS progress. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md | scripts/Y5_R2FR_3503_observed_Hodge_Maxwell_owner_and_total_Hilbert_current_closure_or_EM_bound.py | Derive that Maxwell stress, Poynting flow, matter stress and the source measure all use the same observed coframe/Hodge and one total Hilbert current; otherwise fill the EM/Hodge/current coefficient bounds. | observed Hodge/coframe is q/e_obs-owned, Maxwell action has no independent F2 multiplier, charge/current normalization is fixed, and d(Pi_M J_H_total)=0 in the stationary exterior. | no importing Maxwell by hand as a closure axiom; no ignoring Poynting flux; no bare-mass source; no alpha-owner claim from units alone | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3502_0_sources_exist | True | all cited local source-register paths exist | False |
| VAL3502_1_csv_parse | True | P8_Y5_R2FR_3502_SOURCE_REGISTER.csv:12; P8_Y5_R2FR_3502_DRESSED_SOURCE_FLUX_CLOSURE_THEOREM.csv:6; P8_Y5_R2FR_3502_RADIAL_TIME_MH_STATUS.csv:4; P8_Y5_R2FR_3502_EM_POYNTING_SOURCE_FLUX_VECTOR.csv:7; P8_EM_Poynting_source_flux_or_cross_term_vector.csv:7; P8_Y5_R2FR_3502_DECISION_LEDGER.csv:4; P8_Y5_R2FR_3502_NEXT_TARGET.csv:1 | False |
| VAL3502_2_radial_time_conditional_zero | True | D_r M_H and D_t M_H conditional zero routes present | False |
| VAL3502_3_em_flux_vector_created | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Poynting_source_flux_or_cross_term_vector.csv | False |
| VAL3502_4_ordinary_em_dressed_not_ignored | True | ordinary stationary Maxwell stress is routed into M_H conditionally | False |
| VAL3502_5_retained_leakage_rows | True | radiative/nonminimal/Hodge/readout leakage rows remain explicit | False |
| VAL3502_6_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3502_7_no_formalization_outputs | True | outputs stay under post-checkpoint-work/source-intake | False |
| VAL3502_8_next_target | True | 3503-Y5-R2FR-observed-Hodge-Maxwell-owner-and-total-Hilbert-current-closure-or-EM-bound.md | False |
| VAL3502_SUMMARY | True | PASS | False |

Generated: 2026-06-29T06:04:01.682330+00:00
