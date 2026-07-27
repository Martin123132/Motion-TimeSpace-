# 3403 - Y5/R2FR PiM boundary readout operator beta residual fill under AX1090

## Summary
- 3403 fills the retained `kappa_v` lanes left after the 3402 `a_v=0` and `B_source=A_source^2` conditional results.
- PiM, boundary, readout, operator, coupling and q_loc now each have a conditional zero route plus a finite no-cancellation residual formula.
- The q_loc beta diagnostic is below the beta target only provisionally, but it is not accepted because the alpha3/preferred-frame guard is severe.
- Beta/local-GR remains unclaimed: values and parent signatures are still missing, but the remaining beta work is now localized.
- Generated UTC: `2026-06-28T09:23:56.162944+00:00`.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| SRC3403_00_3402_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md | True | retained_beta_lane_source | False |
| SRC3403_01_3402_impact | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3402_KAPPAV_IMPACT.csv | True | retained_beta_lane_source | False |
| SRC3403_02_3401_components | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3401_KAPPAV_COMPONENT_LEDGER.csv | True | retained_beta_lane_source | False |
| SRC3403_03_3401_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3401_KAPPAV_BOUND_TARGET.csv | True | retained_beta_lane_source | False |
| SRC3403_04_3400_clauses | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv | True | retained_beta_lane_source | False |
| SRC3403_05_pim_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3373_PIM_CHAINMAP_COMMUTATOR_THEOREM_ATTEMPT.csv | True | retained_beta_lane_source | False |
| SRC3403_06_boundary_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv | True | retained_beta_lane_source | False |
| SRC3403_07_boundary_flux_placement | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3393_BOUNDARY_FLUX_PLACEMENT_THEOREM.csv | True | retained_beta_lane_source | False |
| SRC3403_08_ppn_projector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3391_PPN_PROJECTOR_CONSTANCY_THEOREM.csv | True | retained_beta_lane_source | False |
| SRC3403_09_ppn_parent_clause | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3392_FIXED_PPN_PARENT_CLAUSE_CANDIDATE.csv | True | retained_beta_lane_source | False |
| SRC3403_10_r11_beta_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R11_BETA_COMPONENT_VECTOR.csv | True | retained_beta_lane_source | False |
| SRC3403_11_local_eh_operator_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv | True | retained_beta_lane_source | False |
| SRC3403_12_jpim_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv | True | retained_beta_lane_source | False |
| SRC3403_13_jreadout_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv | True | retained_beta_lane_source | False |
| SRC3403_14_beta_envelope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BETA_ENVELOPE_COMPONENTS.csv | True | retained_beta_lane_source | False |
| SRC3403_15_beta_finite_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv | True | retained_beta_lane_source | False |
| SRC3403_16_local_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv | True | retained_beta_lane_source | False |

## Retained Lane Zero Theorems
| lane_id | lane | conditional_zero_theorem | required_clauses | current_status | residual_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ZL3403_0_PiM | kappa_PiM | If Pi_M is a parent-owned fixed q-basic topological chain map on the compact exterior source-current complex, then [d,Pi_M]J_H=0 and delta_g Pi_M=0, so the PiM beta lane vanishes. | PCM3373_1;PCM3373_2;PCM3373_3;PC3400_3 | VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | J_PiM_comm; I_commutator_abs; projector_stress_beta_equiv | False |
| ZL3403_1_boundary | kappa_boundary | If the annulus is fixed, the primitive/reference is parent-fixed, relative boundary cohomology is trivial, physical Hilbert flux is already in the source measure, and H_ref is source-blind, then B_zero_flux=Delta_symp=0 and no boundary U^2 beta lane survives. | BZF3376_0..5;BF3393_0..1;PC3400_4 | VALID_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | B_zero_flux; Delta_symp; boundary_domain_beta | False |
| ZL3403_2_readout | kappa_readout | If PPN observables are read by one fixed post-smoothing P_PPN in one local PPN/Fermi patch and the same observed coframe is used through O(U^2), then no adaptive readout/gauge projector creates beta. | PT3391_0..1;PC3392_0..3;PC3400_0;PC3400_6 | DERIVED_EXACT_IF_PARENT_CLAUSES_HOLD_NOT_SIGNED | J_readout; delta_beta_readout; adaptive projector/gauge drift | False |
| ZL3403_3_operator | kappa_operator | If the compact local exterior is EH-only with no scalar/vector/torsion/nonmetricity/bulk-X/nonlocal/projector-domain operators or each retained coefficient is zero, then the R11 operator beta lane vanishes. | SCEH529_1;SCEH529_2;SCEH529_6;PRE1512_0..7 | CONDITIONAL_EH_NOHAIR_ROUTE_R11_COEFFICIENTS_MISSING | sum_i_abs_delta_beta_R11_i | False |
| ZL3403_4_coupling | kappa_coupling | If PC3400 source-coupling clauses are adopted through O(U^2), with fixed kappa_MTS, ell_J, no calibration feedback and same U in Poisson/H_tau/PPN, then coupling does not re-enter beta. | PC3400_0..6 plus O(U^2) extension | FIRST_ORDER_ROUTE_STAGED_SECOND_ORDER_EXTENSION_UNSIGNED | B_coupling_U2; calibration feedback; delta_kappa/delta_ellJ second-order tails | False |
| ZL3403_5_q_loc | q_loc beta/projection guard | If q_loc is Ward-zero through O(U^2), its beta and preferred-frame/location projections vanish; otherwise beta-only safety is insufficient because the same channel may project into alpha_i/alpha3/xi. | q_loc U2 projection; alpha_i/alpha3/xi projection map; Bianchi/Ward exchange gate | PROVISIONAL_BETA_NUMERIC_EXISTS_ALPHA3_GUARD_NOT_SAFE | delta_beta_q_loc plus preferred-frame guard | False |

## Retained Lane Residual Formulas
| formula_id | lane | absolute_bound | source | input_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RF3403_0_PiM | kappa_PiM | \|kappa_PiM\| <= 2*(I_commutator_abs + DmPiM_JH + Ddomain_PiM + projector_stress_beta_equiv + R_eq_integral + B_zero_flux + E_worldtube + E_extra_current + E_MHref_guard + E_calibration) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv | SCHEMA_READY_VALUES_MISSING | False |
| RF3403_1_boundary | kappa_boundary | \|kappa_boundary\| <= 2*B_boundary_domain with B_boundary_domain sourced by boundary/reference/domain/projector-stress beta projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv | SCHEMA_READY_VALUES_MISSING | False |
| RF3403_2_readout | kappa_readout | \|kappa_readout\| <= 2*B_readout, with J_readout <= J_PiM_comm+J_Ploc_comm+J_worldtube_comm+J_material_comm+J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv | SCHEMA_READY_VALUES_MISSING | False |
| RF3403_3_operator | kappa_operator | \|kappa_operator\| <= 2*sum_i \|delta_beta_R11_i\| across R11 operator families | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R11_BETA_COMPONENT_VECTOR.csv | R11_VECTOR_EXISTS_COEFFICIENTS_MISSING | False |
| RF3403_4_coupling | kappa_coupling | \|kappa_coupling\| <= 2*(B_delta_kappa_U2 + B_delta_ellJ_U2 + B_calibration_feedback + B_source_baseline_U2) | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3400_PARENT_SIGNATURE_CLAUSES.csv | SECOND_ORDER_EXTENSION_UNSIGNED | False |
| RF3403_5_q_loc | q_loc beta/projection guard | \|kappa_q_loc\| <= 2*B_q_loc_beta only after physical U2 projection is signed; must also satisfy alpha_i/alpha3/xi projections | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BETA_ENVELOPE_COMPONENTS.csv | PROVISIONAL_BETA_ONLY_NOT_ACCEPTED | False |

## Operator Family Status
| operator_id | operator_family | component | zero_or_safe_condition | current_evidence | status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B530_0_source_AB | source_normalization_operator | delta_beta_source | source equation or EH mass-family theorem gives B_source=A_source^2 after measured-GM normalization | A_source and B_source missing; measured-GM chain unfilled | unfilled | False | False |
| B530_1_R2_fR_scalar | R2_fR_scalar_mode | delta_beta_R2_fR | c_R2=c_fR=0, scalar mass infinite, source coupling zero, or mapped residual below beta/gamma/R10 locks | R11 skeleton/template only | template_only | False | False |
| B530_2_Ricci_Weyl | Ricci_Weyl_squared | delta_beta_Ricci_Weyl | coefficients zero, pure topological combination with harmless boundary, or weak-field map below beta/gamma/xi locks | R11 skeleton/template only | template_only | False | False |
| B530_3_scalar_class | scalar_tensor_class_metric | delta_beta_scalar_class | phi/C constant universal with zero stress/source charge, infinite mass, or mapped residual below locks | retained; no local silence theorem | unfilled_retained | False | False |
| B530_4_boundary | boundary_topological_terms | delta_beta_boundary | pure boundary/topological/class term has no exterior stress, no flux, no monopole shift, and no readout stress | boundary rows retained; no no-flux theorem promoted | template_only | False | False |
| B530_5_projector_domain | projector_domain_stress | delta_beta_projector_domain | projector/domain variables are metric-independent topological masks or first-class constraints with zero exterior stress | domain/projector rows retained; alpha3 lock extremely tight | unfilled_retained | False | False |
| B530_6_nonlocal_memory | nonlocal_memory_kernel | delta_beta_nonlocal | compact-local kernel silence, screening, zero norm, or residual map below local locks | template only; cosmology memory cannot be imported as local silence | template_only | False | False |
| B530_7_q_loc | q_loc_Gamma_Khat | delta_beta_q_loc | Ward-zero through O(U^2) or compact profile maps below beta without violating alpha3/preferred-frame gates | provisional compact-shell budget only; U2 normalization not proved | provisional_budget_not_claim | False | False |
| B530_8_torsion_nonmetricity | torsion_nonmetricity | delta_beta_connection_readout | Levi-Civita compatibility theorem or projective/spin modes are inert for all matter/readout sectors | P4 rows are template-only; metric compatibility not parent-derived | template_only | False | False |
| B530_9_vector_preferred_frame | vector_preferred_frame | delta_beta_vector_frame | vector absent, pure gauge, dynamically aligned with zero stress, or mapped below preferred-frame locks | retained; no zero theorem | unfilled_retained | False | False |
| B530_10_bulk_X | bulk_X_force_law | delta_beta_bulk_X | positive source-free mass-gap no-hair or alpha_X(lambda_X) plus PPN/source map below locks | operator/source map not parent-derived | unfilled_retained | False | False |
| B530_11_readout_frame | observed_readout_frame | delta_beta_readout | same observed metric/coframe theorem through second PPN order | same-readout theorem open | unfilled_retained | False | False |

## q_loc Beta/Alpha Guard
| guard_id | quantity | value | beta_bound | bound_fraction | kappa_equivalent | kappav_target | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QG3403_0_beta_projection | delta_beta_q_loc | 7.432631961576971e-06 | 7.8e-05 | 0.09529015335355091 | 1.4865263923153942e-05 | 0.000156 | BETA_ONLY_PROVISIONAL_BELOW_BOUND | False |
| QG3403_1_alpha3_warning | q_loc_alpha3_projection_warning | 185815799039424.3 | 7.8e-05 |  |  |  | SEVERE_PREFERRED_FRAME_WARNING_IF_SAME_PROJECTION_APPLIES | False |
| QG3403_2_acceptance | q_loc lane acceptance |  | 7.8e-05 |  |  | 0.000156 | NOT_ACCEPTED_FOR_KAPPAV_SCORE_UNTIL_U2_AND_ALPHA_VECTOR_PROJECTIONS_ARE_SIGNED | False |

## Component Scorecard
| score_id | lane | best_status | claim_status | next_needed | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CS3403_0_eta | eta_v | CONDITIONALLY_ZERO_FROM_3402 | NOT_PARENT_SIGNED | source-calibrated EH/log-lapse parent ownership | False | False |
| CS3403_1_source_quad | kappa_source_quad | CONDITIONALLY_ZERO_FROM_3402 | NOT_PARENT_SIGNED | one-parameter source family / B_source=A_source^2 ownership | False | False |
| CS3403_2_PiM | kappa_PiM | CONDITIONAL_CHAINMAP_ZERO | NOT_PARENT_SIGNED | fixed topological Pi_M plus source-current domain and no projector stress | False | False |
| CS3403_3_boundary | kappa_boundary | CONDITIONAL_STOKES_FIXED_ANNULUS_ZERO | NOT_PARENT_SIGNED | fixed primitive/reference, trivial relative class, no hidden physical flux | False | False |
| CS3403_4_readout | kappa_readout | CONDITIONAL_FIXED_READOUT_ZERO | NOT_PARENT_SIGNED_THROUGH_O_U2 | single observed coframe/readout theorem through O(U^2) | False | False |
| CS3403_5_operator | kappa_operator | EH_NOHAIR_ROUTE_OR_R11_VECTOR | R11_COEFFICIENTS_MISSING | EH-only/no-hair parent theorem or zero/bound all R11 families | False | False |
| CS3403_6_coupling | kappa_coupling | FIRST_ORDER_PC3400_STAGED | O_U2_EXTENSION_UNSIGNED | second-order PC3400 extension and no calibration feedback | False | False |
| CS3403_7_q_loc | q_loc beta/projection guard | BETA_PROVISIONAL_BELOW_BOUND_BUT_ALPHA_GUARD_SEVERE | NOT_ACCEPTED | physical U2 projection and alpha_i/alpha3/xi projection split | False | False |

## Kappa_v Reduced Envelope
| envelope_id | formula | condition | kappav_target | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ENV3403_0_if_eta_source_zero | \|kappa_v\| <= \|kappa_PiM\|+\|kappa_boundary\|+\|kappa_readout\|+\|kappa_operator\|+\|kappa_coupling\|+\|kappa_q_loc\| | uses 3402 conditional zeroes for eta_v and source_quad only | 0.000156 | REDUCED_ENVELOPE_CONDITIONAL_NOT_SCORE_READY | False |
| ENV3403_1_all_lanes_zero | all retained lanes theorem-zero => kappa_v=0 => beta=1 | PiM chainmap, boundary Stokes, fixed readout, EH/no-hair operator, O(U2) coupling and q_loc vector silence all signed | 0.000156 | EXACT_CONDITIONAL_LOCAL_BETA_ROUTE | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3403_0_zero_routes | zero routes exist for retained kappa_v lanes | True | PiM, boundary, readout, operator, coupling and q_loc conditional routes are written | False | False |
| GATE3403_1_formulas | finite formulas exist for retained lanes if zero routes fail | True | absolute no-cancellation formulas are written for PiM, boundary, readout, operator, coupling and q_loc | False | False |
| GATE3403_2_values | retained lane values are score-ready | False | component values/theorem signatures remain missing | False | False |
| GATE3403_3_q_loc | q_loc is safe for beta/full PPN | False | beta-only provisional value is below beta lock, but alpha3/preferred-frame guard is severe and projection is unsigned | False | False |
| GATE3403_4_beta | kappa_v=0 or beta bound pass is derived | False | reduced envelope is conditional and not populated with values | False | False |
| GATE3403_5_local_GR | local GR/PPN is derived | False | beta still nonclaim and alpha_i/zeta_i/xi vector remains open | False | False |

## Nonclaim Runner
| run_id | test | status | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN3403_0_zero_routes | retained lane zero theorem extraction | PASS_CONDITIONAL_ROUTES_EXTRACTED | six retained lane routes written | False |
| RUN3403_1_formulas | finite residual formulas | PASS_FORMULAS_WRITTEN_VALUES_MISSING | absolute residual formulas written without cancellation credit | False |
| RUN3403_2_q_loc | q_loc beta/alpha guard | PASS_GUARD_RETAINED_NOT_ACCEPTED | beta-only provisional is not used as a score because alpha/vector projection is unsafe | False |
| RUN3403_3_claim_firewall | beta/local-GR claim | BLOCKED_NO_CLAIM | kappa_v and full PPN remain unclaimed | False |

## Decision Ledger
| decision_id | finding | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3403_0_progress | all retained kappa_v lanes now have either a conditional zero route or an explicit finite formula | PiM chainmap, boundary Stokes, fixed readout, EH/no-hair, O(U2) coupling and q_loc vector guard are separated | choose the highest-leverage parent ownership audit rather than re-scanning beta | False |
| DEC3403_1_qloc | q_loc is not currently fatal for beta-only but remains dangerous for full PPN | provisional beta projection is below beta target, while alpha3/preferred-frame guard is severe if that projection applies | derive physical U2 and alpha-vector projection split before accepting any q_loc budget | False |
| DEC3403_2_best_next | the best route is source-calibrated EH/no-hair parent ownership | that single audit could activate eta/source zeroes and kill operator/readout/boundary lanes as parent theorems | build 3404 source-calibrated EH parent ownership audit | False |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3403_0_sources_exist | all registered sources exist | True | sources=17 |
| VAL3403_1_zero_routes | retained lane zero routes are present | True |  |
| VAL3403_2_formulas | retained lane formulas are present | True |  |
| VAL3403_3_operator_families | operator family status rows imported | True |  |
| VAL3403_4_qloc_guard | q_loc beta and alpha guard recorded | True |  |
| VAL3403_5_values_block | component values remain blocked | True |  |
| VAL3403_6_claim_gates | beta/local-GR gates remain blocked | True |  |
| VAL3403_7_no_overclaim | all generated rows remain nonclaim | True |  |
| VAL3403_8_scope | no 3403 output path targets formalization-workbench | True |  |
| VAL3403_9_next_target | next target moves to EH parent ownership audit | True |  |
| VAL3403_10_overall | 3403 validation overall | True | all required checks passed |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md | scripts/Y5_R2FR_3404_source_calibrated_EH_parent_ownership_audit.py | audit whether the source-calibrated EH one-parameter/no-hair branch can be parent-owned by MTS without importing GR as an axiom | this is the least-fragmented route to close eta/source/operator/readout/boundary beta lanes together | False |
| 3405-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md | scripts/Y5_R2FR_3405_q_loc_U2_alpha_vector_projection_split.py | derive the physical U2 beta projection and separate alpha_i/alpha3/xi projections of q_loc | q_loc cannot be accepted as beta-safe until the preferred-frame projection is separated or killed | False |
