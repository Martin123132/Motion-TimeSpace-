# 2804 - Y5 R2FR q_loc Surface Traction No-Flux Or First Real Force Bound Under AX1090

## Private Verdict

2804 tries the clean route: make the compact-body surface traction vanish without sneaking in a plateau axiom.

The no-flux proof does not close. It would close if `tau_q` were parent-signed as an antisymmetric superpotential with controlled curvature/remainder, or if the parent field equations gave a true local surface-silence theorem. Neither is currently in the corpus.

The fallback does improve the situation: the first force-bound row is now written in concrete boundary data, `Gamma_eff`, `K_hat`, time-dipole, and projector/connection terms. It is still nonnumeric because `zeta_q`, q_loc units, body measure, and boundary norms are not sourced.

Therefore 2804 makes no local-GR, WEP, orbital, PPN, or source-normalization claim. The next best move is proof-first again: hunt for a parent superpotential/no-traction structure; failing that, source `zeta_q` and unit contracts.

## Surface Traction No-Flux Attempt
| no_flux_id | claim_piece | mathematical_form | status | interpretation |
| --- | --- | --- | --- | --- |
| SNF2804_0_surface_traction_object | surface traction to kill | Phi_A^i := oint_{partial Sigma_A} tau_q^{ji} n_j dS | DEFINED_FROM_2803 | This is now the precise local-vacuum surface object, not a vague plateau. |
| SNF2804_1_superpotential_route | antisymmetric superpotential would kill flux on closed compact surfaces | tau_q^{ji}=nabla_k U_q^{kji}+R_q^{ji}, U_q^{kji}=-U_q^{jki}; Phi_A^i=int_{Sigma_A}[nabla_j,nabla_k]U_q^{kji}+oint R_q^{ji}n_jdS | SUPERPOTENTIAL_NOT_SIGNED | This is the cleanest no-flux theorem route, but the parent action has not supplied U_q. |
| SNF2804_2_local_vacuum_surface_route | traction vanishes on the chosen compact-body boundary | tau_q^{ji}\|_{partial Sigma_A}=0 | NO_LOCAL_SURFACE_SILENCE_THEOREM | Cannot assume this; it must follow from field equations or source support. |
| SNF2804_3_stationary_dipole_route | time dipole term vanishes or averages away | d/dt int_{Sigma_A} P_loc K_hat^{0i}sqrt(gamma)d^3x=0 or <dD_A^i/dt>_orbit=0 | STATIONARITY_NOT_SIGNED | Without this, local force can leak through time-dependent internal momentum. |
| SNF2804_4_projector_connection_route | projector/connection corrections vanish or are bounded | C_P^i=C_conn^i=0 or \|C_P^i+C_conn^i\|<=epsilon_PC | PROJECTOR_CONNECTION_NOT_CLOSED | This is the same hard projector ownership issue seen earlier, now in force language. |
| SNF2804_5_verdict | surface-traction no-flux theorem | Phi_A^i=0 only if SNF2804_1 or SNF2804_2 plus SNF2804_3 and SNF2804_4 close | FAIL_CURRENT_CLAIM | No local-GR/WEP claim; however, the required clauses are now exact. |

## Traction Bound Decomposition
| bound_piece_id | quantity | bound_form | meaning | status |
| --- | --- | --- | --- | --- |
| TBD2804_0_flux_decomposition | Phi_A^i | oint P_loc Gamma_eff n^i dS - oint P_loc K_hat^{ji}n_j dS + Phi_density^i + Phi_projector^i | surface force flux split into Gamma, K_hat, density, and projector pieces | exact decomposition up to declared correction terms |
| TBD2804_1_norm_bound | \|Phi_A\| | <= A_A(\|\|P_loc Gamma_eff\|\|_partial + \|\|P_loc K_hat\|\|_partial + \|\|delta tau_projector\|\|_partial) | first real surface-traction norm bound form | nonnumeric until boundary area and norms are sourced |
| TBD2804_2_superpotential_curvature_bound | \|Phi_A\| if tau_q=nabla U_q+R_q | <= Vol_A \|\|Riemann * U_q\|\| + A_A \|\|R_q\|\|_partial | if superpotential exists, only curvature/remainder leakage remains | requires parent U_q and curvature scale |
| TBD2804_3_stationary_correction | \|dD_A/dt\| | <= omega_A \|D_A\| or zero under exact stationary branch | time-dipole correction for force bound | requires stationarity or orbital average theorem |
| TBD2804_4_projector_connection_bound | \|C_P+C_conn\| | <= epsilon_P + epsilon_conn | commutator/connection correction budget | requires P_loc domain constants |

## First Real Force Bound Attempt
| force_bound_id | observable | bound_form | units | missing_inputs | status |
| --- | --- | --- | --- | --- | --- |
| FFB2804_0_single_body_acceleration | delta a_A | \|delta a_A\| <= \|zeta_q\|/M_A [A_A(\|\|P Gamma_eff\|\|+\|\|P K_hat\|\|+\|\|delta tau\|\|)+\|dD_A/dt\|+epsilon_P+epsilon_conn] | acceleration | zeta_q; M_A; boundary area; Gamma/K_hat boundary norms; time-dipole; projector constants | BOUND_FORM_DERIVED_NOT_NUMERIC |
| FFB2804_1_WEP_eta | eta_AB | <= (\|zeta_q\|/g_N)\|I_A/M_A-I_B/M_B\| + \|Phi_A/M_A-Phi_B/M_B\|/g_N | dimensionless | two-body moments; source/test-body masses; local g_N; zeta_q | BOUND_FORM_DERIVED_NOT_NUMERIC |
| FFB2804_2_orbital_residual | delta a_orb | <= \|zeta_q\| \|I_source\|/M_source + \|Phi_source\|/M_source, scored without measured-G absorption | acceleration | source body moment; no-absorption split; orbital radius/source model | BOUND_FORM_DERIVED_NOT_NUMERIC |
| FFB2804_3_first_real_row_verdict | first force-bound row | no numeric row can be claimed until zeta_q and q_loc units are sourced | nonclaim | parent normalization and boundary norm data are absent | RUNNER_BLOCKED_CORRECTLY |

## Force Bound Runner
| runner_id | input_id | schema_ok | units_declared | numeric_inputs_present | score_ready | claim_allowed | failure_reasons |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN2804_0 | FFB2804_0_single_body_acceleration | True | True | False | False | False | BOUND_FORM_DERIVED_NOT_NUMERIC;zeta_q; M_A; boundary area; Gamma/K_hat boundary norms; time-dipole; projector constants;VALID_FOR_CLAIM_FALSE |
| RUN2804_1 | FFB2804_1_WEP_eta | True | True | False | False | False | BOUND_FORM_DERIVED_NOT_NUMERIC;two-body moments; source/test-body masses; local g_N; zeta_q;VALID_FOR_CLAIM_FALSE |
| RUN2804_2 | FFB2804_2_orbital_residual | True | True | False | False | False | BOUND_FORM_DERIVED_NOT_NUMERIC;source body moment; no-absorption split; orbital radius/source model;VALID_FOR_CLAIM_FALSE |
| RUN2804_3 | FFB2804_3_first_real_row_verdict | True | True | False | False | False | RUNNER_BLOCKED_CORRECTLY;parent normalization and boundary norm data are absent;VALID_FOR_CLAIM_FALSE |

## Unit And Source Acquisition Ledger
| acquisition_id | quantity | role | status | priority |
| --- | --- | --- | --- | --- |
| ACQ2804_0_zeta_q | zeta_q | normalization in f_q^nu=zeta_q q_loc^nu | MISSING_PARENT_NORMALIZATION | highest priority |
| ACQ2804_1_q_loc_units | q_loc units | [zeta_q q_loc]=force density | MISSING_QLOC_UNIT_CONVENTION | highest priority |
| ACQ2804_2_surface_norms | \|\|P Gamma_eff\|\|_partial and \|\|P K_hat\|\|_partial | surface traction norm | MISSING_BOUNDARY_NORMS | needed for numeric force row |
| ACQ2804_3_body_measure | M_A and A_A | same body mass and boundary area used in force/source map | MISSING_SOURCE_OWNER | needed for WEP/orbital row |
| ACQ2804_4_projector_constants | epsilon_P, epsilon_conn | projector/connection correction budget | MISSING_PROJECTOR_CONTROL | needed for no-flux or bound |
| ACQ2804_5_no_absorption | measured-G no-absorption score | force/source hair not hidden in fitted GM | POLICY_EXISTS_NOT_SCORED | needed before orbital claim |

## Claim Gates
| gate_id | claim | gate_pass | claim_allowed | reason |
| --- | --- | --- | --- | --- |
| CG2804_0_surface_object | q_loc surface traction object is explicit | True | False | tau_q/Phi_A decomposition is written |
| CG2804_1_no_flux | surface traction no-flux theorem is proved | False | False | superpotential/local-surface-silence route is not parent-signed |
| CG2804_2_stationary_projector | stationary dipole and projector/connection terms vanish | False | False | stationarity and P_loc commutator control are missing |
| CG2804_3_first_force_bound | first real WEP/orbital force-bound row is score-ready | False | False | zeta_q, q_loc units, and boundary norms are absent |
| CG2804_4_local_claim | local GR/WEP/orbital claim can be made | False | False | no-flux and numeric-bound routes both fail |
| CG2804_5_nonclaim_pack | 2804 nonclaim no-flux/bound pack is ready | True | False | next target is superpotential/source acquisition |

## Decision Ledger
| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC2804_0_no_flux_not_proved | Surface no-flux is not proved. | The exact routes require a parent superpotential or a local surface-silence theorem; neither is sourced. | do not claim local GR/WEP |
| DEC2804_1_bound_shape_improved | The first force-bound shape is now sharper. | The bound is in Gamma/K_hat boundary norms plus time/projector corrections, not an amorphous q_loc proxy. | source zeta_q and q_loc units next |
| DEC2804_2_best_next | Best next target is superpotential or source acquisition. | Either prove tau_q is an exact antisymmetric superpotential/no-traction object, or obtain the normalization needed for numeric bounds. | 2805 should choose proof-first with bound fallback |

## Validation
| validation_id | passed | detail |
| --- | --- | --- |
| VAL2804_0_sources_exist | True | all source-register paths exist |
| VAL2804_1_sources_nonempty | True | all source-register paths contain text |
| VAL2804_2_surface_object_defined | True | surface traction object is defined |
| VAL2804_3_no_flux_not_promoted | True | no-flux theorem fails safely |
| VAL2804_4_traction_bound_decomposed | True | traction norm bound is decomposed |
| VAL2804_5_force_bound_not_numeric | True | force-bound rows remain nonnumeric |
| VAL2804_6_runner_blocks_claim | True | runner blocks all force-bound claims |
| VAL2804_7_acquisition_high_priority | True | zeta_q acquisition is prioritized |
| VAL2804_8_claim_gates_safe | True | all claim gates keep claims blocked |
| VAL2804_9_next_target_2805 | True | next target is 2805 |
| VAL2804_10_branch_outputs_exist | True | branch copies were written |
| VAL2804_11_outputs_exist | True | all generated output paths exist |
| VAL2804_12_csv_parse | True | all generated CSV outputs parse |
| VAL2804_13_cited_paths_exist | True | all cited copy/source paths in generated rows exist |
| VAL2804_14_no_claim_flags | True | no valid_for_claim or claim_allowed flag is true |
| VAL2804_15_generated_under_post_checkpoint | True | all generated artifacts remain under post-checkpoint-work |
| VAL2804_16_formalization_untouched | True | formalization-workbench was not modified during this run |
| VAL2804_17_pycache_absent | True | scripts __pycache__ absent before compile step |
| VAL2804_OVERALL | True | 2804 defines the q_loc surface traction no-flux proof clauses, refuses promotion, sharpens the first force-bound shape, and selects superpotential/zeta-unit acquisition as 2805. |

## Next Target
| next_id | next_target | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2804_0_2805 | 2805-Y5-R2FR-q_loc-superpotential-no-traction-or-zeta-unit-source-acquisition-under-AX1090.md | prove tau_q is a parent-signed antisymmetric superpotential/no-traction object, or source zeta_q/q_loc units for the first numeric WEP/orbital force-bound row | U_q superpotential; tau_q remainder R_q; curvature leakage; zeta_q; q_loc units; Gamma/K_hat boundary norms; no measured-G absorption | plateau axiom; proxy scoring; local-GR/WEP/orbital claim; fitted cancellation; GitHub; formalization edits |
