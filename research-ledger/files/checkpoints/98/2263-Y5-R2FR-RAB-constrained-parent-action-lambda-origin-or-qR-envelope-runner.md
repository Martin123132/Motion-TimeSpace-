# 2263 - Y5/R2FR R_AB Constrained Parent Action Lambda Origin Or q_R Envelope Runner

## Verdict

2263 tries the derivation route first. The nonpropagating `lambda_R R_AB` constraint is still the cleanest local-GR route because it kills reciprocal hair before it becomes a fifth-force/PPN residual. But the current corpus does **not** derive the parent origin of `lambda_R`.

So the branch remains nonclaim. The exact constrained-parent-action contract is now written, and the fallback `q_R/Q_R` screening runner is wired to the existing local bounds gates. The runner has controls that pass/fail as expected, but the actual MTS row is refused because no parent `q_R` or `Q_R` value/bound exists yet.

No local-GR/Newton, PPN, R10, WEP, clock, orbital, `lambda_R`, `R_AB=0`, `Q_R=0`, or empirical support claim is made.

## Source Register
| source_id | source_key | source_path | exists | needles_present | validation_overall_pass | role |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2263_00_2262_doc | 2262_doc | 2262-Y5-R2FR-RAB-ownership-as-quotient-representative-or-finite-residual-envelope.md | True | True |  | handoff: lambda-origin or finite q_R envelope selected |
| SRC2263_01_2262_validation | 2262_validation | source-intake/mts_residuals/P8_Y5_BRR545_2262_VALIDATION.csv | True | True | True | confirms 2262 passed before 2263 starts |
| SRC2263_02_2262_envelope | 2262_envelope | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2262_FINITE_RAB_RESIDUAL_ENVELOPE.csv | True | True |  | nonclaim q_R/Q_R residual envelope seed |
| SRC2263_03_07_constraint | constraint_07 | 07-nonpropagating-reciprocity-constraint.md | True | True |  | clean nonpropagating constraint route |
| SRC2263_04_08_phase | phase_08 | 08-phase-volume-reciprocity-origin.md | True | True |  | motion-capacity/radial-cell motivation |
| SRC2263_05_09_hamiltonian | hamiltonian_09 | 09-hamiltonian-radial-cell-derivation.md | True | True |  | rejects generic Hamiltonian/Liouville derivation |
| SRC2263_06_10_observer | observer_10 | 10-observer-map-symplectic-contract.md | True | True |  | R_AB/J_q normalization and missing theorem |
| SRC2263_07_11_current | current_11 | 11-cell-current-origin-attempt.md | True | True |  | ordinary current route leaves Q_R hair |
| SRC2263_08_12_noether | noether_12 | 12-gauge-noether-origin-audit.md | True | True |  | gauge/Noether audit: constraint possible but absent |
| SRC2263_09_14_sensitivity | sensitivity_14 | 14-closure-deviation-PPN-sensitivity.md | True | True |  | internal conversion coefficients from q_R/beta/clock/matter leaks to observables |
| SRC2263_10_15_map | map_15 | 15-local-observables-data-map.md | True | True |  | published local screening gates map |
| SRC2263_11_16_runner | runner_16 | 16-local-bounds-gate-runner.md | True | True |  | prior local bounds gate runner |
| SRC2263_12_gates_15 | gates_15 | runs/20260530-232024-local-observables-data-map/results/mts_parameter_screening_gates.csv | True | True |  | machine-readable local screening gates |
| SRC2263_13_translations_15 | translations_15 | runs/20260530-232024-local-observables-data-map/results/observable_bound_translations.csv | True | True |  | machine-readable observable conversion coefficients |
| SRC2263_14_summary_16 | summary_16 | runs/20260530-232506-local-bounds-gate-runner/results/candidate_branch_summary.csv | True | True |  | prior pass/fail branch screening summary |
| SRC2263_15_gate_results_16 | gate_results_16 | runs/20260530-232506-local-bounds-gate-runner/results/branch_parameter_gate_results.csv | True | True |  | prior parameter-by-parameter screening results |
| SRC2263_16_local_bounds | local_bounds | source-intake/local_bounds/local_bound_claims.csv | True | True |  | local published-bound source ledger |

## Lambda-Origin Audit
| audit_id | candidate_origin | derives | does_not_derive | status | why_it_fails | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| LAM2263_0_motion_capacity_identity | c^2=v_space^2+v_clock^2+v_load^2 | T^2=1-L clock/load side | spatial routing S or J_q=T sqrt(S)=1 | PARTIAL_SUPPORT_ONLY | clock capacity alone leaves the routing exponent p open | False |
| LAM2263_1_radial_cell_principle | radial t-r clock-routing cell preservation | if adopted, T sqrt(S)=1 and therefore R_AB=0/p=1 | why this specific cell is separately preserved | MOTIVATED_NOT_PARENT_DERIVED | generic volume, Hamiltonian, and Liouville preservation are too weak | False |
| LAM2263_2_cell_current | conserved reciprocal-cell current | W partial_r R_AB=Q_R | Q_R=0 | REJECTED_AS_ZERO_THEOREM | ordinary current conservation creates a conserved hair charge rather than a constraint | False |
| LAM2263_3_gauge_noether | coordinate gauge, cell-scale gauge, or bare Noether identity | a warning about what cannot be used | lambda_R equation R_AB=0 | REJECTED_CURRENT_SCAFFOLD | areal radius fixes radial gauge; cell-scale changes observables; Noether identities relate equations but do not create a multiplier equation | False |
| LAM2263_4_nonpropagating_constraint | parent algebraic constraint S_lambda=int lambda_R R_AB | R_AB=0 and no Q_R hair if parent-signed | the parent origin of lambda_R | EXACT_CONDITIONAL_NOT_SIGNED | current corpus can state the constraint but cannot yet derive it from primitives | False |
| LAM2263_5_verdict | lambda_R origin | nothing claimable yet | local GR/Newton/PPN safety | LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY | the missing theorem is a constrained parent action or constraint algebra, not another name for reciprocity | False |

## Constrained Parent Action Contract
| contract_id | contract_clause | required_statement | current_status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CPA2263_0_parent_variable | parent variable owns J_q or R_AB | J_q=T sqrt(S), R_AB=2 ln J_q, and the parent action declares whether this is constrained data | CONTRACT_WRITTEN_NOT_DERIVED | derive the parent variable and measure from motion/time/space primitives | False |
| CPA2263_1_multiplier_origin | lambda_R origin | lambda_R is a parent multiplier/reaction stress associated with radial-cell capacity balance, not an inserted GR lock | MISSING_PARENT_ORIGIN | derive lambda_R from a constraint algebra or variational capacity principle | False |
| CPA2263_2_action_form | nonpropagating action form | S_parent=S_Q[Q,Psi,theta]+int mu lambda_R R_AB with no D R_AB term | EXACT_IF_SIGNED | show this is generated by ParentGenerate rather than appended | False |
| CPA2263_3_variation | constraint variation | delta_lambda S=R_AB=0 and delta_R S solves lambda_R/reaction terms without producing Q_R hair | FORMAL_CONDITIONAL | prove allowed boundary variations and reaction stress ownership | False |
| CPA2263_4_no_kinetic_operator | operator exclusion | D R_AB and D lambda_R constructors are absent or pure boundary-exact | MISSING_GRAMMAR_PROOF | typed ParentGenerate grammar must exclude kinetic reciprocal strain | False |
| CPA2263_5_matter_order | matter/readout order | matter/readout uses the constrained observed coframe after parent variation, with no shadow frame | UNSIGNED_READOUT_ORDER | derive same-coframe matter functor and no-marker constants | False |
| CPA2263_6_no_GR_import | no GR import | the constraint is not Schwarzschild AB=1, Einstein vacuum equations, or fitted p=1 in disguise | POLICY_GATE_ACTIVE | source the derivation from primitives only | False |
| CPA2263_7_verdict | constrained parent action | CPA2263_0 through CPA2263_6 jointly close | NOT_DERIVED_CURRENT_CORPUS | move to q_R envelope until the parent action is supplied | False |

## Constraint Algebra Gates
| gate_id | gate | required_statement | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| CAG2263_0_primary_constraint | primary multiplier | pi_lambda approximately 0 and delta_lambda S=R_AB | MISSING_PARENT_HAMILTONIAN | False |
| CAG2263_1_secondary_constraint | secondary radial-cell constraint | R_AB approximately 0 preserved under parent evolution | MISSING_CONSTRAINT_EVOLUTION | False |
| CAG2263_2_reaction_stress | reaction stress ownership | lambda_R enters only as reaction stress enforcing cell balance, not as new long-range source | MISSING_REACTION_STRESS_MAP | False |
| CAG2263_3_boundary | boundary/corner differentiability | boundary variation has no R_AB hair charge or cancels with exact/proper term | MISSING_BOUNDARY_PROOF | False |
| CAG2263_4_degree_count | degree count | R_AB/lambda_R pair carries no propagating local degree | MISSING_DIRAC_COUNT | False |
| CAG2263_5_matter | matter/source compatibility | ordinary matter cannot source the constrained variable independently | MISSING_MATTER_DESCENT | False |
| CAG2263_6_verdict | constraint algebra closes | all constraint and boundary gates close jointly | NOT_CLOSED | False |

## Local Screening Gates
| parameter | adopted_screening_gate | gate_source | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| q_R | 2.3e-05 | cassini_bertotti_2003 | screening_gate_not_fit_result | False |
| delta_beta | 7.16e-05 | inpop20a_fienga_2021 | screening_gate_not_fit_result | False |
| alpha_clock | 2.48e-05 | galileo_delva_2018 | screening_gate_not_fit_result | False |
| epsilon_matter | 2.745906043549196e-15 | microscope_touboul_2022 | screening_gate_not_fit_result | False |
| Q_R | 0.0 | closure_definition | theory_gate_not_observational_fit | False |

## Observable Translations
| observable | mts_parameter | linear_coefficient | adopted_parameter_gate | implied_1gate_observable_shift | observable_unit | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| solar_light_bending | q_R | 0.8756216406841224 | 2.3e-05 | 2.0139297735734814e-05 | arcsec | False |
| solar_shapiro | q_R | 59.7375179242781 | 2.3e-05 | 0.0013739629122583963 | microseconds | False |
| mercury_perihelion_gamma | q_R | 28.65467507274745 | 2.3e-05 | 0.0006590575266731914 | arcsec_per_century | False |
| mercury_perihelion_beta | delta_beta | -14.327337536373726 | 7.16e-05 | -0.0010258373676043588 | arcsec_per_century | False |
| gps_gravitational_redshift | alpha_clock | 45.718449825926655 | 2.48e-05 | 0.001133817555682981 | microseconds_per_day | False |
| eotvos_proxy | epsilon_matter | 1.0 | 2.745906043549196e-15 | 2.745906043549196e-15 | dimensionless | False |

## q_R Candidate Screening Runner
| candidate_id | candidate_type | q_R | delta_beta | alpha_clock | epsilon_matter | reciprocal_charge_Q_R | verdict | failed_parameters | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN2263_0_closure_control | control_baseline | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | pass_control_not_signal |  | False | False |
| RUN2263_1_unsigned_lambda_constraint | theory_target_unsigned | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | blocked_unsigned_theory_target | lambda_R_parent_origin | False | False |
| RUN2263_2_MTS_unknown_qR | actual_MTS_gap_row |  |  |  |  |  | not_scoreable_missing_parent_values | q_R;delta_beta;alpha_clock;epsilon_matter;Q_R | False | False |
| RUN2263_3_qR_at_gate | edge_case | 2.3e-05 | 0.0 | 0.0 | 0.0 | 0.0 | pass_screening_not_claim |  | False | False |
| RUN2263_4_qR_ten_times_gate | fail_probe | 0.00023 | 0.0 | 0.0 | 0.0 | 0.0 | fail_screening | q_R | False | False |
| RUN2263_5_QR_hair_small_qR | theory_fail_probe | 1e-06 | 0.0 | 0.0 | 0.0 | 1e-06 | fail_screening | Q_R | False | False |
| RUN2263_6_mixed_inside_gates | candidate_probe | 1e-05 | 2e-05 | 1e-05 | 1e-15 | 0.0 | pass_screening_not_claim |  | False | False |

## q_R Candidate Observable Impacts
| candidate_id | observable | shift | unit | depends_on | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RUN2263_0_closure_control | solar_light_bending | 0.0 | arcsec | q_R | False |
| RUN2263_0_closure_control | solar_shapiro | 0.0 | microseconds | q_R | False |
| RUN2263_0_closure_control | mercury_perihelion_combined | 0.0 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_0_closure_control | gps_gravitational_redshift | 0.0 | microseconds_per_day | alpha_clock | False |
| RUN2263_0_closure_control | eotvos_proxy | 0.0 | dimensionless | epsilon_matter | False |
| RUN2263_1_unsigned_lambda_constraint | solar_light_bending | 0.0 | arcsec | q_R | False |
| RUN2263_1_unsigned_lambda_constraint | solar_shapiro | 0.0 | microseconds | q_R | False |
| RUN2263_1_unsigned_lambda_constraint | mercury_perihelion_combined | 0.0 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_1_unsigned_lambda_constraint | gps_gravitational_redshift | 0.0 | microseconds_per_day | alpha_clock | False |
| RUN2263_1_unsigned_lambda_constraint | eotvos_proxy | 0.0 | dimensionless | epsilon_matter | False |
| RUN2263_2_MTS_unknown_qR | all_local_observables | MISSING_PARENT_VALUE_OR_BOUND | mixed | q_R;delta_beta;alpha_clock;epsilon_matter | False |
| RUN2263_3_qR_at_gate | solar_light_bending | 2.0139297735734814e-05 | arcsec | q_R | False |
| RUN2263_3_qR_at_gate | solar_shapiro | 0.0013739629122583963 | microseconds | q_R | False |
| RUN2263_3_qR_at_gate | mercury_perihelion_combined | 0.0006590575266731914 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_3_qR_at_gate | gps_gravitational_redshift | 0.0 | microseconds_per_day | alpha_clock | False |
| RUN2263_3_qR_at_gate | eotvos_proxy | 0.0 | dimensionless | epsilon_matter | False |
| RUN2263_4_qR_ten_times_gate | solar_light_bending | 0.00020139297735734816 | arcsec | q_R | False |
| RUN2263_4_qR_ten_times_gate | solar_shapiro | 0.013739629122583964 | microseconds | q_R | False |
| RUN2263_4_qR_ten_times_gate | mercury_perihelion_combined | 0.006590575266731914 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_4_qR_ten_times_gate | gps_gravitational_redshift | 0.0 | microseconds_per_day | alpha_clock | False |
| RUN2263_4_qR_ten_times_gate | eotvos_proxy | 0.0 | dimensionless | epsilon_matter | False |
| RUN2263_5_QR_hair_small_qR | solar_light_bending | 8.756216406841223e-07 | arcsec | q_R | False |
| RUN2263_5_QR_hair_small_qR | solar_shapiro | 5.97375179242781e-05 | microseconds | q_R | False |
| RUN2263_5_QR_hair_small_qR | mercury_perihelion_combined | 2.8654675072747452e-05 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_5_QR_hair_small_qR | gps_gravitational_redshift | 0.0 | microseconds_per_day | alpha_clock | False |
| RUN2263_5_QR_hair_small_qR | eotvos_proxy | 0.0 | dimensionless | epsilon_matter | False |
| RUN2263_6_mixed_inside_gates | solar_light_bending | 8.756216406841225e-06 | arcsec | q_R | False |
| RUN2263_6_mixed_inside_gates | solar_shapiro | 0.000597375179242781 | microseconds | q_R | False |
| RUN2263_6_mixed_inside_gates | mercury_perihelion_combined | 0.0 | arcsec_per_century | q_R;delta_beta | False |
| RUN2263_6_mixed_inside_gates | gps_gravitational_redshift | 0.0004571844982592666 | microseconds_per_day | alpha_clock | False |
| RUN2263_6_mixed_inside_gates | eotvos_proxy | 1e-15 | dimensionless | epsilon_matter | False |

## Refusal Runner
| refusal_id | attempted_claim | runner_result | blocked_by | score_eligible | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2263_0_lambda_origin | lambda_R parent origin derived | BLOCKED | LAM2263_5_verdict=LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY | False | False |
| REF2263_1_constrained_action | nonpropagating R_AB constraint is parent-signed | BLOCKED | CPA2263_7_verdict=NOT_DERIVED_CURRENT_CORPUS | False | False |
| REF2263_2_constraint_algebra | constraint algebra/degree count closes | BLOCKED | CAG2263_6_verdict=NOT_CLOSED | False | False |
| REF2263_3_QR_zero | Q_R=0 theorem | BLOCKED | current and boundary audits leave Q_R hair unless parent constraint is signed | False | False |
| REF2263_4_actual_MTS_score | actual MTS q_R row can be scored | BLOCKED | RUN2263_2_MTS_unknown_qR lacks parent values/bounds | False | False |
| REF2263_5_local_GR | derived local GR/Newton/PPN safety | BLOCKED | only closure/control and screening harness pass; no derivation claim | False | False |

## Claim Gates
| claim_id | claim | gate_pass | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2263_0_lambda_origin | lambda_R origin from primitives | False | candidate origins motivate but do not derive the multiplier | False |
| CG2263_1_parent_constraint | parent-signed nonpropagating R_AB constraint | False | contract written but not parent-derived | False |
| CG2263_2_constraint_algebra | Dirac/constraint/boundary closure | False | Hamiltonian, boundary, degree-count and matter gates remain missing | False |
| CG2263_3_qR_numeric | actual MTS q_R numeric envelope score | False | actual q_R/Q_R values remain missing | False |
| CG2263_4_empirical | local empirical support for MTS | False | screening harness is not raw-data likelihood and not evidence | False |
| CG2263_5_local_GR_Newton | derived local GR/Newton/PPN recovery | False | not achieved; closure remains control baseline only | False |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2263_0_derivation | LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY | motion-capacity and radial-cell principles motivate lambda_R R_AB but do not supply parent multiplier origin or constraint algebra | do not claim local GR from the constraint | False |
| DEC2263_1_contract | CONSTRAINED_PARENT_ACTION_CONTRACT_WRITTEN | the exact future contract is now stated: parent variable, multiplier origin, action form, no kinetic R_AB, boundary silence, matter order, no GR import | use this as the acceptance gate for any future derivation | False |
| DEC2263_2_runner | QR_ENVELOPE_RUNNER_OPERATIONAL_NONCLAIM | screening gates and observable translations are wired, with pass/fail controls and MTS unknown row refused | fill parent q_R/Q_R values or derive zero before scoring | False |
| DEC2263_3_next | PARENT_CONSTRAINT_ALGEBRA_OR_QR_VALUE_SOURCE_NEXT | the next useful step is either true constraint algebra construction or first source-backed q_R/Q_R parent value/bound | 2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md | False |

## Next Target
| route_id | next_target | script | objective | selection_status | success_condition |
| --- | --- | --- | --- | --- | --- |
| NEXT2263_0_primary | 2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md | scripts/Y5_R2FR_RAB_parent_constraint_algebra_or_first_qR_value_source_2264.py | try to build the actual parent constraint algebra for lambda_R/R_AB; if it fails, acquire the first source-backed parent q_R or Q_R value/bound row for the local screening runner | selected | constraint algebra gates close without GR import, or q_R/Q_R gets a sourced parent value/bound while still nonclaim |
| NEXT2263_1_parallel | 2264b-Y5-R2FR-RAB-raw-local-bound-source-refresh.md | scripts/Y5_R2FR_RAB_raw_local_bound_source_refresh_2264b.py | refresh local published bound sources and provenance without using them as MTS evidence | held_parallel | local bound ledger sources are current, cited, and separated from MTS coefficient evidence |

## Branch Copies
| copy_id | source_path | target_path | target_exists | target_parses | reason |
| --- | --- | --- | --- | --- | --- |
| BC2263_contract | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2263_CONSTRAINED_PARENT_ACTION_CONTRACT.csv | source-intake/rab-sector/acquisition-queue/JR2263_LAMBDA_ORIGIN_CONTRACT_NONCLAIM.csv | True | True | lambda-origin constrained-parent-action contract nonclaim copy |
| BC2263_qr_runner | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2263_QR_CANDIDATE_SCREENING_RUNNER.csv | source-intake/rab-sector/acquisition-queue/JR2263_QR_SCREENING_RUNNER_NONCLAIM.csv | True | True | q_R/Q_R screening runner nonclaim copy |
| BC2263_branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2263_CLAIM_GATES.csv | source-intake/microscope/branch_locked_wep/residuals/RAB_lambda_origin_and_qR_screening_refusal_2263.csv | True | True | branch-locked local/WEP refusal gates |
| BC2263_beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2263_DECISION_LEDGER.csv | source-intake/beta-source/docs/RAB_LAMBDA_ORIGIN_OR_QR_ENVELOPE_2263_NONCLAIM.csv | True | True | portable lambda-origin/q_R-envelope decision ledger |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2263_0_sources_exist | PASS | all cited source paths exist |
| VAL2263_1_needles_present | PASS | all cited source needles are present |
| VAL2263_2_prior_validation | PASS | 2262 validation passes |
| VAL2263_3_lambda_not_derived | PASS | lambda origin is not falsely promoted |
| VAL2263_4_contract_written | PASS | constrained parent-action contract written and kept unsigned |
| VAL2263_5_algebra_not_closed | PASS | constraint algebra gates remain open |
| VAL2263_6_screening_gates_loaded | PASS | local screening gates loaded |
| VAL2263_7_translations_loaded | PASS | observable translation coefficients loaded |
| VAL2263_8_runner_controls | PASS | q_R runner has pass/fail controls and refuses actual MTS unknown row |
| VAL2263_9_impacts_written | PASS | observable impacts written |
| VAL2263_10_refusal_blocks | PASS | refusal runner blocks current claims |
| VAL2263_11_claim_gates_blocked | PASS | claim gates remain blocked |
| VAL2263_12_next_selected | PASS | 2264 parent constraint algebra or first q_R source target selected |
| VAL2263_13_csv_parse | PASS | all generated 2263 CSVs parse |
| VAL2263_14_no_claim_flags | PASS | no generated score/claim flags are true |
| VAL2263_15_branch_copies | PASS | branch/queue copies exist and parse |
| VAL2263_16_pycache_absent | PASS | scripts __pycache__ absent |
| VAL2263_17_formalization_no_2263 | PASS | formalization-workbench has no 2263 output files |
| VAL2263_OVERALL | PASS | 2263 rejects current lambda-origin derivation, writes the constrained-parent-action contract, wires the q_R/Q_R nonclaim screening runner, and selects 2264 |

## Working Interpretation

This is a useful narrowing. A derived local-GR lane now requires an actual constrained parent action, not another motivational sentence. If that parent action cannot be built, the honest route is a `q_R/Q_R` residual programme with hard local screens. That is not as glamorous as closing GR, but it is testable and it stops the branch from becoming a smuggled Schwarzschild axiom.