# 3446 - Htau Exact One-Form Reference Lock or MHref Denominator Bound

## Summary
- This checkpoint attacks the denominator left open by 3445: `H_tau-H_ref`.
- The exact route is now precise: define the Hamiltonian variation one-form `alpha_tau`; if `d_F alpha_tau=0`, with fixed source-blind `H_ref`, same `tau/frame`, and positive non-orbital `M_H_ref`, then `H_tau-H_ref` can be a source denominator.
- The fallback is also precise: field-space Stokes turns nonzero curl into `Delta_H_curl_bound`, which feeds an absolute denominator residual.
- Current MTS does not yet parent-own `Theta_MTS`, `Q_tau^MTS`, curl silence, fixed reference, or positive same-frame `M_H_ref`, so no local-GR/Newton promotion is allowed.
- The `Pi_M^H` win from 3445 is preserved: `I_commutator^H` stays removed in the preferred branch and is not reopened here.

## Source Register
| source_id | path | exists | role | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| doc_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3445-Y5-R2FR-Hilbert-identity-PiM-parent-adoption-or-Htau-source-current-lock-under-AX1090.md | True | immediate Htau handoff | False | False |
| next_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_NEXT_TARGET.csv | True | machine-readable 3446 target | False | False |
| htau_lock_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_HTAU_SOURCE_CURRENT_LOCK_AUDIT.csv | True | Htau lock audit | False | False |
| residual_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_RESIDUAL_VECTOR_AFTER_PIMH_ADOPTION.csv | True | denominator residual vector target | False | False |
| pc3400_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_PC3400_3_UPDATE.csv | True | PC3400.3 split after PiMH adoption | False | False |
| curl_law_3208 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv | True | closed-one-form and field-space Stokes law | False | False |
| curl_audit_2667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv | True | prior Htau curl audit | False | False |
| integrability_gate_2667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv | True | integrability gates | False | False |
| reference_lock_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv | True | reference/tau/MHref lock law | False | False |
| reference_selector_2382 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv | True | source-blind reference selector theorem | False | False |
| htau_href_status_2351 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2351_HTAU_HREF_SOURCE_ROW_STATUS.csv | True | Htau/Href source row status | False | False |
| mhref_schema_1017 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv | True | M_H_ref first-row schema | False | False |
| theta_qtau_reference_2339 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2339_THETA_QTAU_FIXED_REFERENCE_AUDIT.csv | True | theta/Q_tau/fixed-reference audit | False | False |
| theta_qtau_owner_1646 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1646_THETA_QTAU_CURRENT_OWNER_AUDIT.csv | True | parent current owner audit | False | False |
| hamiltonian_charge_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv | True | mass-current Hamiltonian charge contract | False | False |
| htau_certificate_2445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2445_HTAU_SOURCE_CHARGE_CERTIFICATE_AUDIT.csv | True | Htau source-charge certificate blockers | False | False |
| htau_mhref_1732 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv | True | M_H_ref source rows | False | False |
| htau_worldtube_2938 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv | True | Htau/worldtube source measure theorem | False | False |
| htau_extraction_3006 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3006_HTAU_EXTRACTION_ROWS.csv | True | theta/Q_tau/Htau extraction rows | False | False |
| parent_adoption_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv | True | PiMH branch adoption contract | False | False |
| commutator_reduction_3445 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3445_COMMUTATOR_REDUCTION.csv | True | PiMH commutator carryforward | False | False |

## Exact One-Form Theorem
| theorem_id | claim_piece | statement | derivation | result | missing_to_promote | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HOT3446_0_define_alpha | Hamiltonian variation one-form | alpha_tau(delta Phi)=int_S(delta Q_tau^MTS-i_tau Theta_MTS(delta Phi))-delta H_ref | This is the covariant phase-space definition of the Hamiltonian variation on a fixed branch. | EXACT_CONDITIONAL_DEFINITION | Theta_MTS, Q_tau^MTS, tau_id, surface_pair and fixed H_ref must be parent-owned | False | False |
| HOT3446_1_curl_law | field-space curl law | d_F alpha_tau(delta_1,delta_2)=-int_S i_tau omega_MTS(delta_1,delta_2)+C_tau+C_S+C_ref | For fixed tau, surface class and reference selector, only the symplectic flux term remains; moving branch data add explicit correction terms rather than hidden H_tau shifts. | DERIVED_ACCOUNTING_IDENTITY | sector omega_MTS, boundary pullback units, tau/surface/reference variation rows | False | False |
| HOT3446_2_exact_denominator_route | H_tau-H_ref as state-function denominator | If d_F alpha_tau=0 on the allowed local branch and H_ref is fixed/source-blind, then H_tau exists path-independently and M_H_ref:=H_tau[S_outer]-H_ref can be a pre-orbit source denominator. | A closed one-form on the branch integrates to a state function. Positivity and same-frame/source-current equality are separate gates, so exactness alone is not enough for Newton. | EXACT_IF_CLOSED_ONE_FORM_REFERENCE_AND_POSITIVITY_LOCKS_PASS | all curl components theorem-zero, positive same-frame M_H_ref, no orbital-GM import | False | False |
| HOT3446_3_bound_route | non-integrable denominator bound | /Delta H_tau(path_1,path_0)/ <= int_BF /d_F alpha_tau/ <= A_F sup_BF /d_F alpha_tau/ | Field-space Stokes converts nonzero curl into an explicit denominator ambiguity bound. This is the correct fallback if exactness fails. | DERIVED_BOUND_ROUTE_NO_NUMERIC_VALUES | field-space patch B_F, area/norm convention, component sup bounds, M_H_ref lower bound | False | False |
| HOT3446_4_verdict | current H_tau exactness | The exact theorem shape exists, but current MTS does not parent-own Theta/Q_tau, curl silence, fixed reference, tau/surface lock or M_H_ref positivity together. | The result is not another vague gap: it is a precise denominator residual vector with a Stokes-bound route. | HTAU_DENOMINATOR_NOT_PROMOTED_BOUND_VECTOR_REQUIRED | Theta/Q_tau parent current extraction is the next root | False | False |

## Reference Lock Split
| lock_id | object | zero_condition | exact_rule | current_status | fallback_component | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RLS3446_0_selector | Sigma_ref | Sigma_ref depends only on fixed boundary class, topology, orientation/corner convention, asymptotic coframe, tau convention and stationary/vacuum branch data | if D_source Sigma_ref=0 then D_source H_ref=0 by chain rule | CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | epsilon_ref_source | False | False |
| RLS3446_1_no_GM_laundering | H_ref provenance | partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} Sigma_ref=0 before source bridge is derived | forbid any reference selector that uses the target measured source normalization | FORBIDDEN_INPUT_RULE_ACTIVE_SOURCE_CERTIFICATE_MISSING | epsilon_ref_laundering_guard | False | False |
| RLS3446_2_surface_no_retune | S_outer/S_inner/reference surface class | linked surfaces stay in one parent boundary class and are not retuned with source/radius/orbit | D_source S=0 and D_source corner convention=0 | CONDITIONAL_ROUTE_NOT_SIGNED | epsilon_surface_retune | False | False |
| RLS3446_3_same_frame_sidecar | M_H_ref denominator frame | M_H_ref is finite, positive, same tau/coframe/frame and not imported from orbital GM | all normalized reference/curl residuals use this denominator only after it is independently sourced | MISSING_POSITIVE_SAME_FRAME_MHREF | M_H_ref_lower_bound_missing | False | False |

## MHref Denominator Bound Rows
| row_id | quantity | definition | formula | required_columns | current_status | numeric_or_theorem_value | score_ready | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DBR3446_0_M_H_ref | M_H_ref | positive same-frame Hamiltonian source denominator H_tau[S_outer]-H_ref for the Pi_M^H branch | M_H_ref := H_tau[tau_obs,S_outer]-H_ref[S_outer] | system_id;tau_id;frame_id;surface_outer;Q_tau_integral;H_ref;M_H_ref;M_H_ref_lower;units;reference_rule;source_path;no_orbital_GM | MISSING_POSITIVE_SAME_FRAME_MHREF | MISSING_M_H_REF | False | False | False |
| DBR3446_1_delta_H_curl | Delta_H_curl_bound | field-space path-dependence of H_tau from nonzero d_F alpha_tau | int_BF /d_F alpha_tau/ <= A_F sup_BF/-int_S i_tau omega_MTS + C_tau+C_S+C_ref/ | system_id;field_space_patch;variation_pair;A_F;curl_sup_bound;components;units;source_path | MISSING_CURL_COMPONENT_BOUNDS | MISSING_DELTA_H_CURL_BOUND | False | False | False |
| DBR3446_2_reference_shift | Delta_ref_over_MH | source/range/time/frame dependence of H_ref or reference subtraction normalized by M_H_ref | abs(Delta_ref)/M_H_ref_lower if source-blind reference theorem is not signed | system_id;reference_selector;Delta_ref;derivative_profile;M_H_ref_lower;units;source_path;no_GM_laundering | MISSING_REFERENCE_ZERO_OR_VALUE | MISSING_DELTA_REF | False | False | False |
| DBR3446_3_tau_surface_frame | epsilon_tau_surface_frame | mismatch from tau, surface, coframe or frame moving between source charge, clocks, orbitals, PPN and R10 | (abs(C_tau)+abs(C_S)+abs(C_frame))/M_H_ref_lower | system_id;tau_source;tau_charge;tau_clock;tau_readout;surface_pair;frame_id;mismatch_bound;units;source_path | MISSING_TAU_SURFACE_FRAME_LOCK_OR_BOUND | MISSING_TAU_SURFACE_FRAME_BOUND | False | False | False |
| DBR3446_4_symplectic_boundary | epsilon_symplectic_boundary | boundary/corner/projector/non-EH symplectic flux contribution to H_tau exactness | abs(int_S i_tau omega_extra + B_zero_flux + Delta_symp)/M_H_ref_lower | system_id;sector;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref_lower;units;source_path | MISSING_SYMPLECTIC_BOUNDARY_ZERO_OR_BOUND | MISSING_SYMPLECTIC_BOUNDARY_BOUND | False | False | False |
| DBR3446_5_epsilon_den_total | epsilon_Htau_denominator_abs | absolute no-cancellation denominator residual after Pi_M^H adoption | (abs(Delta_H_curl_bound)+abs(Delta_ref)+abs(C_tau)+abs(C_S)+abs(C_frame)+abs(symplectic_boundary_flux))/M_H_ref_lower | all DBR3446_0..4 component columns plus source_paths and no_cancellation_flag | MISSING_COMPONENT_VALUES_TOTAL_NONCLAIM | MISSING_COMPONENT_VALUES | False | False | False |

## PiMH Carryforward
| carry_id | quantity | 3445_status | 3446_effect | reactivates_if | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PCH3446_0_commutator | I_commutator^H | 0 in the Hilbert identity branch | removed from the denominator residual unless non-identity PiM is reintroduced | old topological, Hodge, Green, DeWitt, domain or post-readout PiM is used | False | False |
| PCH3446_1_projector_stress | epsilon_projector_stress^H | no independent projector stress for identity/inclusion map | not part of H_tau curl for preferred Pi_M^H branch | metric/domain projector replaces Pi_M^H | False | False |
| PCH3446_2_extra_current | -Pi_M^H dJ_extra | retained | not solved by H_tau exactness; remains separate source-exchange term in Omega_GM^H | always live until extra-current zero theorem or source-bound vector exists | False | False |

## Source Denominator Residual Vector
| residual_id | symbol | definition | after_3446 | zero_or_bound_next | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SDR3446_0_denominator | epsilon_Htau_denominator_abs | absolute H_tau/H_ref/tau/reference/symplectic denominator ambiguity normalized by M_H_ref_lower | exact formula and bound schema derived, values missing | derive theta/Q_tau/current-chain exactness or fill DBR3446 rows | False | False |
| SDR3446_1_total_source_bridge | Omega_GM^H | -Pi_M^H dJ_extra + A_parent + Delta_coupling + Delta_cal + Delta_PPN + epsilon_Htau_denominator_abs | I_commutator^H removed; denominator residual isolated; extra/current/coupling terms still live | attack parent theta/Q_tau extraction, then source-exchange/coupling calibration | False | False |

## PC3400.3 Htau Update
| update_id | pc_clause | before | after | delta | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PCU3446_0_PC3400_3 | PC3400_3_Htau_PiM_chain | PiM chain-map component solved conditionally by Pi_M^H; H_tau/MHref/reference/tau still unsigned | H_tau exactness is reduced to closed-one-form plus source-blind reference plus positive same-frame M_H_ref | PC3400_3 is now blocked by theta/Q_tau/current-chain and denominator rows, not by PiM commutator | False | False |
| PCU3446_1_RSB3424_0 | epsilon_HPiM_Z | /partial_Z ln(M_H/(J_H^M))/ + epsilon_Htau_curl + epsilon_ref + epsilon_tau_frame | epsilon_Htau_denominator_abs with explicit DBR3446 component rows and field-space Stokes bound | source denominator ambiguity is executable as a future bound vector | False | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PG3446_0_sources | all 3446 cited source paths exist | True | source register path check | False | False |
| PG3446_1_closed_one_form_theorem | the exact H_tau closed-one-form theorem and Stokes bound are written | True | HOT3446_2 and HOT3446_3 provide exact and bound routes | False | False |
| PG3446_2_Htau_exactness_claim | H_tau-H_ref is currently a parent-signed exact denominator | False | Theta/Q_tau, d_F alpha closure, reference selector, tau/frame and M_H_ref positivity are not all signed | False | False |
| PG3446_3_bound_rows_ready | denominator bound rows are schema-ready but nonclaim | True | DBR3446 rows name components, required columns and no-cancellation total | False | False |
| PG3446_4_local_GR_Newton | local GR/Newton/source coupling can be promoted | False | denominator values/source proofs, extra-current projection, coupling and PPN calibration remain live | False | False |

## Decision Ledger
| decision_id | decision | because | next_action | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3446_0_Htau_status | Do not treat H_tau as a denominator unless alpha_tau is closed or bounded. | non-integrable Hamiltonian variation is path-dependent and can hide source-normalization drift | attack Theta/Q_tau parent current extraction first | False | False |
| DEC3446_1_bound_route | Use field-space Stokes as the fallback instead of handwaving integrability. | it turns failure of exactness into a quantitative residual route once component bounds exist | fill Delta_H_curl_bound, Delta_ref, tau/surface/frame and M_H_ref_lower rows | False | False |
| DEC3446_2_PiM_not_reopened | Do not reopen the PiM commutator while staying in the Hilbert-identity branch. | 3445 already killed I_commutator^H; the remaining obstruction is denominator ownership | only reactivate I_commutator if a non-identity PiM branch is used | False | False |

## Next Target
| target_doc | target_script | objective | success_condition | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| 3447-Y5-R2FR-parent-Theta-Q_tau-extraction-or-deltaH-curl-first-component-row-under-AX1090.md | scripts/Y5_R2FR_3447_parent_Theta_Qtau_extraction_or_deltaHcurl_first_component_row.py | extract or bound the first missing H_tau denominator component by deriving parent Theta_MTS and Q_tau^MTS for the adopted Hilbert-identity branch; if extraction fails, stage the first source-backed Delta_H_curl component row with units, surface pair, variation pair and source path | Theta/Q_tau owner chain exists for the local branch, or DBR3446_1 receives a schema-valid nonclaim component row instead of staying symbolic | False | False |

## Runner Nonclaim
| runner_id | branch | closed_one_form_theorem_written | theta_qtau_owned | mhref_positive | score_ready | result | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN3446_0_exact_route | Pi_M^H_Htau_denominator | True | False | False | False | EXACT_ROUTE_DEFINED_NOT_CLAIM_READY | False | False |
| RUN3446_1_bound_route | Htau_field_space_Stokes_bound | True | False | False | False | BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM | False | False |

## Validation
| check_id | condition | passed | detail |
| --- | --- | --- | --- |
| VAL3446_0_sources_exist | all cited 3446 source paths exist | True | 21/21 source paths exist |
| VAL3446_1_closed_one_form | exact closed-one-form theorem route is present | True | H_tau exact route written |
| VAL3446_2_stokes_bound | field-space Stokes fallback bound is present | True | non-integrability bound route written |
| VAL3446_3_mhref_row | M_H_ref denominator row remains explicit and nonclaim | True | M_H_ref not imported from orbital GM |
| VAL3446_4_reference_split | reference selector chain-rule and no-GM laundering rules are retained | True | reference lock split written |
| VAL3446_5_PiMH_carryforward | I_commutator^H remains removed and not reopened | True | PiMH improvement carried forward |
| VAL3446_6_exact_not_promoted | H_tau exactness is not falsely promoted | True | denominator remains nonclaim |
| VAL3446_7_next_target | next target attacks Theta/Q_tau extraction or first curl row | True | 3447-Y5-R2FR-parent-Theta-Q_tau-extraction-or-deltaH-curl-first-component-row-under-AX1090.md |
| VAL3446_8_generated_csv_parse | generated CSV rows parse cleanly | True | CSV reader pass for generated outputs present before validation write |
| VAL3446_9_nonclaim | all generated rows remain nonclaim | True | valid_for_claim=false and claim_allowed=false wherever present |
| VAL3446_10_formalization_untouched | formalization-workbench modified-file count remains 0 during this run | True | modified_count_since_start=0 |
| VAL3446_11_overall | 3446 Htau denominator checkpoint is internally valid | True | PASS |

## Bottom Line
The source denominator is no longer a fog bank. Either `alpha_tau` is a closed one-form on the adopted branch, or the failure is an explicit field-space curl/reference/frame residual normalized by a non-orbital `M_H_ref`. The next honest move is `Theta_MTS` and `Q_tau^MTS`; without them, `H_tau` is not a derived mass denominator.
