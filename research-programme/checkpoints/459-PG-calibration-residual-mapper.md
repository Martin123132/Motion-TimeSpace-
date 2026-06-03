# 459 - PG Calibration Residual Mapper

Private P8/R0-R11 residual-mapping checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 458 made the Poisson/Gauss measured-GM bridge exact but conditional. This checkpoint converts every failed `PG0-PG10` condition into explicit residual rows.

The aim is to stop the branch from saying "not derived yet" in prose. Each failure must now become either:

```text
derived_zero,
derived_bound,
numeric residual input,
R10 curve,
R11 operator vector,
or retained no-claim row.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/PG_calibration_residual_mapper.py` |
| Run directory | `runs\20260602-191500-PG-calibration-residual-mapper` |
| Status | `PG_calibration_residual_mapper_written_failed_PG_rows_mapped_to_P8_R11_inputs_no_numeric_residuals_loaded_no_Newton_or_local_GR_pass` |
| Claim ceiling | `PG_residual_mapper_only_no_measured_GM_Newton_PPN_or_local_GR_pass` |
| Residual map | `source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv` |
| Input template | `source-intake\mts_residuals\P8_PG_calibration_residual_INPUT_TEMPLATE.csv` |
| Next target | `460-source-normalized-Newton-branch-theorem-stack.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md | True | immediate PG0-PG10 calibration gate to be mapped |
| source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv | True | machine-readable PG calibration contract rows |
| source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv | True | canonical P8 measured-GM/source-normalization residual rows |
| source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv | True | canonical R0-R11 local residual prediction template |
| source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv | True | R11 non-EH operator-vector template required if EH-only is not derived |
| 438-R11-nonEH-coefficient-vector-contract.md | True | R11 symbolic no-pass coefficient-vector contract |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | EH/source-normalization retained ledger and row transition policy |
| 450-Hilbert-source-to-measured-monopole-calibration-gate.md | True | Hilbert source to measured monopole calibration blockers |
| 452-constant-universal-Geff-kappa-identity-attempt.md | True | constant universal G_eff/kappa residual map |
| runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv | True | machine-readable R0-R11 residual components and locks |
| runs/20260602-143000-source-normalization-residual-vector-refinement/results/mu_obs_decomposition.csv | True | machine-readable mu_obs decomposition into source-normalization channels |
| runs/20260602-181500-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate/results/Poisson_Gauss_calibration_contract.csv | True | run artifact for PG0-PG10 rows |

## 4. Template Health

| artifact | count | expected | status |
| --- | --- | --- | --- |
| PG_contract_rows | 11 | 11 | pass |
| P8_source_template_rows | 8 | 8 | pass |
| MTS_local_R_template_rows | 12 | 12 | pass |
| PG_residual_map_rows | 11 | 11 | pass |
| PG_residual_input_template_rows | 9 | 9 | pass |

## 5. PG to Residual Map

The PG residual map has been written to `source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv`.

| pg_id | failed_premise | activated_residual_component | residual_symbol | affected_rows | activation_rule | required_input | current_status | valid_for_claim | source_gate | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PG0_Hamiltonian_charge_input | B_xi is not parent-derived as a well-defined observed-time charge | R11_EH_operator_ledger;P8_Meff_conservation;P8_frame_calibration_split | c_nonEH_operator_vector;dln_Meff_dt;delta_frame_source | R2;R4;R5;R6;R8;R9;R11 | if HC0-HC3 are not derived, the candidate Hamiltonian charge is reference/operator/frame conditional | parent charge proof or retained charge/reference/operator residual vector | retained_missing_parent_charge | false | 458-PG0 | no Poisson/Gauss calibration can start without a real observed-time charge |
| PG1_charge_equals_projected_Hilbert_source | B_xi/G_eff is not shown equal to M_eff[Pi_M J_H] | P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra;R11_EH_operator_ledger | dln_Meff_dt;mu_extra_boundary_bulk_domain;c_nonEH_operator_vector | R1;R4;R9;R10;R11 | if charge-current equality is missing, measured source mass is a retained calibration split | source-current Ward/Pi_M proof or numeric/source-normalization residual | retained_charge_current_split | false | 458-PG1 | conserved geometric charge is not automatically the Newton source |
| PG2_same_frame_weak_field_potential | matter orbits are not proved to read the same Phi sourced by the metric equation | P8_frame_calibration_split;R0_identity_coframe_direct;R2_clock_redshift;R11_EH_operator_ledger | delta_frame_source;eta_WEP_direct_geometry;alpha_clock_redshift;c_nonEH_operator_vector | R0;R1;R2;R11 | if the potential/frame map is missing, calibration can hide a frame split | same-frame coframe theorem or frame residual below WEP/clock/operator locks | retained_frame_split | false | 458-PG2 | clock or direct-WEP success alone does not clear the source-frame split |
| PG3_EH_to_Poisson_coefficient | EH-to-Poisson coefficient is conditional on EH-only and zero source_residuals | R11_EH_operator_ledger;P8_boundary_bulk_domain_mu_extra;P8_range_dependence | c_nonEH_operator_vector;mu_extra_boundary_bulk_domain;alpha(lambda) | R3;R4;R8;R10;R11 | if EH-only/source purity is missing, the Poisson coefficient is an operator/source residual | EH-only theorem-zero or complete R11 vector plus source residual map | retained_operator_source_residual | false | 458-PG3 | the algebra passes only inside the same-frame EH/source premise stack |
| PG4_Gauss_surface_integral | surface integral is not proved equal to enclosed M_eff without residual volume/boundary terms | P8_radial_source_hair;P8_boundary_bulk_domain_mu_extra;P8_Meff_conservation | partial_r_ln_mu_obs;mu_extra_boundary_bulk_domain;dln_Meff_dt | R3;R4;R7;R8;R9;R10;R11 | if Gauss integral equality is missing, radial/boundary/source hair remains active | closed Pi_M flux plus zero boundary/source residual theorem or numeric residual envelope | retained_Gauss_surface_residual | false | 458-PG4 | this is the main measured-GM monopole calibration row |
| PG5_orbital_inverse_square_readout | test bodies are not proved to read a pure inverse-square Gauss monopole | P8_range_dependence;P8_radial_source_hair;P8_species_source_charge;P8_frame_calibration_split | alpha(lambda);partial_r_ln_mu_obs;eta_source_AB;delta_frame_source | R1;R2;R4;R10;R11 | if orbital readout has extra force/source/frame terms, GM is empirical not derived | slow-particle geodesic proof plus alpha(lambda)=0/source/frame theorem or residual curve | retained_orbital_readout_residual | false | 458-PG5 | finite-range/radial effects cannot be absorbed into one GM |
| PG6_zero_mu_extra_and_source_residuals | mu_extra and S_res are not theorem-zero | P8_boundary_bulk_domain_mu_extra;P8_radial_source_hair;P8_range_dependence;R11_EH_operator_ledger | mu_extra_boundary_bulk_domain;partial_r_ln_mu_obs;alpha(lambda);c_nonEH_operator_vector | R3;R4;R7;R8;R9;R10;R11 | if source_residuals survive, Gauss mass includes their volume/boundary contribution | Ward/no-hair/topological zero proof or executable coefficient map for all mu_extra channels | retained_mu_extra_source_residual | false | 458-PG6 | source_residuals are measured physics, not notation |
| PG7_constant_universal_Geff | G_eff/kappa_eff is not parent-derived constant/universal/source-blind/range-blind | P8_Geff_time_drift;P8_species_source_charge;P8_range_dependence;R11_EH_operator_ledger | dln_Geff_dt;eta_source_AB;alpha(lambda);c_nonEH_operator_vector | R1;R4;R9;R10;R11 | if G_eff derivatives or source labels are unproved, Gdot/source/fifth-force rows remain active | CU1-CU7 theorem-zero proof or derivative/source/range residual values | retained_Geff_derivative_residual | false | 458-PG7 | constant offset is calibration only after all derivatives vanish |
| PG8_no_derivative_hair | mu_obs derivative silence is not parent-derived | P8_Geff_time_drift;P8_Meff_conservation;P8_species_source_charge;P8_range_dependence;P8_radial_source_hair;P8_frame_calibration_split | dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;delta_frame_source | R0;R1;R2;R4;R8;R9;R10;R11 | if any time/radial/species/range/frame/domain derivative is unproved, the matching row stays retained | row-specific theorem-zero source or numeric derivative/curve/profile | retained_derivative_hair_vector | false | 458-PG8 | this is the anti-calibration-cheat row |
| PG9_second_order_source_stability | first-order measured-GM calibration is not proved stable at beta/gamma/PPN order | P8_nonlinear_beta_source_residue;R3_gamma;R11_EH_operator_ledger | delta_beta_source;gamma_minus_1;c_nonEH_operator_vector | R3;R4;R11 | if second-order weak-field calculation is missing, Poisson cannot be promoted to local GR | second-order PPN source/operator derivation or beta/gamma residual values | retained_second_order_source_residual | false | 458-PG9 | Poisson success is a first-order source gate only |
| PG10_retained_residual_fallback | failed PG rows need executable residual data before any claim | all_P8_source_normalization_components;R11_EH_operator_ledger | dln_Geff_dt;dln_Meff_dt;eta_source_AB;alpha(lambda);partial_r_ln_mu_obs;mu_extra/(GM);delta_beta_source;c_nonEH_operator_vector | R1;R3;R4;R7;R8;R9;R10;R11 | if no theorem-zero proof exists, output templates and mark valid_for_claim=false | filled residual input template or derived-zero sources | template_policy_only | false | 458-PG10 | manual no-promotion discipline is replaced by machine-readable rows |

## 6. Residual Input Template

The fillable PG residual input template has been written to `source-intake\mts_residuals\P8_PG_calibration_residual_INPUT_TEMPLATE.csv`.

| model_id | branch_id | pg_id | component_id | symbol | units | normalization | affected_rows | observable_link | bound_or_target | required_input | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_branch_name | PG_calibration_branch | PG7;PG8 | P8_Geff_time_drift | dln_Geff_dt | yr^-1 | d ln G_eff / dt or d ln kappa_eff / dt | R9;R11 | Gdot_over_G | 9.6e-15 yr^-1 or derived zero | numeric drift, derived-zero proof, or explicit superselection source | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | d ln mu_obs/dt = d ln(G_eff M_eff)/dt | fill_derivation_or_run_path | same observed frame; local branch; source-normalized measured GM | false | cosmological memory success cannot override local Gdot lock |
| MTS_branch_name | PG_calibration_branch | PG1;PG4;PG8 | P8_Meff_conservation | dln_Meff_dt | yr^-1 | d ln M_eff / dt after separating G_eff drift | R4;R9;R11 | beta_minus_1;Gdot_over_G | beta/Gdot locks or derived conservation | mass-flux closure proof or mass drift residual | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | mu_obs = G_eff M_eff + mu_extra | fill_derivation_or_run_path | compact source; no unowned flux; no hidden boundary/memory exchange | false | source mass conservation must be owned, not assumed |
| MTS_branch_name | PG_calibration_branch | PG5;PG7;PG8 | P8_species_source_charge | eta_source_AB | dimensionless | composition/source derivative of ln mu_obs | R1;R11 | eta_WEP_source_charge | 2.8e-15 or derived universal source charge | species/source-charge theorem or eta_source_AB residual | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | partial_A mu_obs = 0 | fill_derivation_or_run_path | species/material markers do not alter active gravitational source | false | direct WEP proxy is not the full source-normalization proof |
| MTS_branch_name | PG_calibration_branch | PG3;PG5;PG6;PG7;PG8 | P8_range_dependence | alpha(lambda) | range-dependent | Yukawa/non-Yukawa fifth-force curve or derivative of ln mu_obs with range scale | R10;R11 | delta_G_or_fifth_force_yukawa | verified alpha(lambda) bound curve or derived zero | curve file with lambda/alpha_predicted/alpha_bound or no finite-range theorem | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | partial_lambda mu_obs = 0 | fill_curve_path_or_derivation | same-frame source charge; screening/range assumptions explicit | false | symbolic R10 cannot pass without executable curve or theorem-zero |
| MTS_branch_name | PG_calibration_branch | PG4;PG5;PG6;PG8 | P8_radial_source_hair | partial_r_ln_mu_obs | inverse_length_or_dimensionless_envelope | radial derivative or residual envelope relative to measured GM | R3;R4;R10;R11 | gamma_minus_1;beta_minus_1;alpha(lambda) | zero radial hair or mapped PPN/fifth-force residuals | radial profile, no-hair proof, or coefficient map | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | partial_r mu_obs = 0 | fill_profile_or_derivation_path | compact exterior; boundary/domain hair accounted for | false | radial dependence is physics, not calibration |
| MTS_branch_name | PG_calibration_branch | PG1;PG3;PG4;PG6 | P8_boundary_bulk_domain_mu_extra | mu_extra_boundary_bulk_domain | dimensionless_or_GM_units_after_normalization | mu_extra/(G_eff M_eff) or explicit GM units | R3;R4;R7;R8;R9;R11 | gamma;beta;alpha3;xi;Gdot;operator_ledger | zero owned exchange or coefficient residuals below row locks | exchange coefficients, Ward/no-hair proof, or boundary/domain residual map | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | mu_extra = 0 | fill_exchange_derivation_or_run_path | boundary, bulk, domain, projector, memory, and connection channels visible | false | alpha3 lock is severe for unowned exchange |
| MTS_branch_name | PG_calibration_branch | PG0;PG2;PG5;PG8 | P8_frame_calibration_split | delta_frame_source | dimensionless | relative frame/source calibration residual | R0;R2;R11 | eta_WEP_direct_geometry;clock_redshift;operator_ledger | one observed frame or explicit residual below row locks | parent frame theorem or frame split residual | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | same observed coframe for matter and metric source variation | fill_frame_derivation_or_run_path | matter, clocks, rods, photons, and metric source use same observed frame | false | calibration cannot hide a frame split |
| MTS_branch_name | PG_calibration_branch | PG9 | P8_nonlinear_beta_source_residue | delta_beta_source | dimensionless | beta_minus_1 contribution assigned to source normalization | R4;R11 | beta_minus_1 | 7.8e-05 or derived second-order source closure | second-order weak-field source derivation or beta source residual | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | PPN beta after measured-GM normalization | fill_second_order_derivation_or_run_path | same observed frame; measured-GM normalization held fixed at PPN order | false | first-order Poisson success does not clear beta |
| MTS_branch_name | PG_calibration_branch | PG0;PG1;PG3;PG6;PG7;PG9 | R11_EH_operator_ledger | c_nonEH_operator_vector | operator family | full R11 coefficient-vector normalization | R3;R4;R5;R6;R8;R10;R11 | operator_ledger;gamma;beta;preferred_frame;fifth_force | EH-only theorem-zero or executable coefficient vector | R11 operator-vector file or EH-only parent theorem | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | R11_nonEH_operator_vector_TEMPLATE.csv | fill_operator_vector_or_EH_theorem_path | local, same-frame, source-normalized exterior branch | false | symbolic operator row cannot pass without coefficient/vector map |

## 7. R0-R11 Row Transitions

| row_id | activated_by | new_state | why | claim_credit |
| --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | PG2;PG8 | retained_frame_control | same-frame potential/source map remains conditional | no |
| R1_WEP_source_charge | PG1;PG5;PG7;PG8 | retained_source_charge | measured source strength may carry species/source dependence | no |
| R2_clock_redshift | PG0;PG2;PG5;PG8 | retained_same_frame_clock | orbits/clocks/source may not share one observed frame | no |
| R3_gamma | PG3;PG4;PG6;PG9 | retained_operator_slip | Poisson source purity does not prove spatial curvature/slip | no |
| R4_beta | PG0;PG1;PG3;PG4;PG5;PG6;PG7;PG8;PG9 | retained_source_normalization_beta | measured-GM and second-order source stability are not derived | no |
| R5_alpha1 | PG0 | retained_preferred_frame_vector | observed-time charge generator can carry vector/preferred-frame ambiguity | no |
| R6_alpha2 | PG0 | retained_preferred_frame_vector | observed-time charge generator can carry vector/preferred-frame ambiguity | no |
| R7_alpha3 | PG4;PG6 | retained_exchange_flux | boundary/source residual flux can become momentum nonconservation | no |
| R8_xi | PG0;PG3;PG4;PG6;PG8 | retained_boundary_domain_location | boundary/domain hair can shift Gauss source or preferred-location response | no |
| R9_Gdot | PG0;PG1;PG4;PG6;PG7;PG8 | retained_Gdot_source_drift | G_eff and M_eff derivative silence is not derived | no |
| R10_fifth_force | PG1;PG3;PG4;PG5;PG6;PG7;PG8 | retained_curve_required | range/radial dependence requires alpha(lambda) curve or theorem-zero | no |
| R11_EH_operator_ledger | PG0-PG10 | retained_operator_vector_required | EH-only exterior and source-normalized operator purity are not parent-derived | no |

## 8. Gate Tests

| gate | pass_condition | current_result | evidence |
| --- | --- | --- | --- |
| PG_rows_mapped_to_residual_components | every PG0-PG10 row activates one or more P8/R11 residual components | pass | 11 PG map rows written |
| input_template_written | all canonical P8 source-normalization components plus R11 operator vector have fillable rows | pass | 9 residual input rows written |
| claim_flags_blocked | all generated residual input template rows have valid_for_claim=false | pass | template rows are scaffolding until filled with theorem-zero or numeric residuals |
| row_transitions_preserve_no_promotion | R0-R11 transitions keep no theorem credit | pass | 12 row transitions have claim_credit=no |
| numeric_residuals_loaded | real theorem-zero, numeric residual, R10 curve, or R11 vector inputs are loaded | fail | this checkpoint writes mapper/template only |
| measured_GM_parent_derived | PG1 and PG4-PG8 are closed by theorem-zero or valid residual evidence | fail | all current PG blockers remain retained |
| Newton_or_local_GR_promoted | P8/R11 and PPN rows are theorem-zero or empirically scored | fail | residual mapper only |

## 9. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| PG residual mapper written | pass | PG0-PG10 mapped into P8/R11 components |
| source-normalization input template written | pass | P8/R11 fillable template rows emitted |
| symbolic pass-through blocked | pass | all mapper-generated input rows have valid_for_claim=false |
| measured GM parent-derived | fail | no PG theorem-zero or numeric residual input supplied |
| Newton/PPN/local GR promoted | fail | mapper only; no residual row has claim credit |

## 10. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| map_schema_matches | pass | source-intake\mts_residuals\P8_PG_calibration_residual_MAP.csv |
| input_schema_matches | pass | source-intake\mts_residuals\P8_PG_calibration_residual_INPUT_TEMPLATE.csv |
| template_health_passes | pass | PG_contract_rows=11; P8_source_template_rows=8; MTS_local_R_template_rows=12; PG_residual_map_rows=11; PG_residual_input_template_rows=9 |
| claim_flags_blocked | pass | all generated input rows valid_for_claim=false |
| row_transition_claims_blocked | pass | all R0-R11 transitions keep claim_credit=no |
| PG_rows_mapped_to_residual_components | pass | 11 PG map rows written |
| input_template_written | pass | 9 residual input rows written |
| claim_flags_blocked | pass | template rows are scaffolding until filled with theorem-zero or numeric residuals |
| row_transitions_preserve_no_promotion | pass | 12 row transitions have claim_credit=no |
| numeric_residuals_loaded | fail | this checkpoint writes mapper/template only |
| measured_GM_parent_derived | fail | all current PG blockers remain retained |
| Newton_or_local_GR_promoted | fail | residual mapper only |
| claim_ceiling_enforced | pass | PG_residual_mapper_only_no_measured_GM_Newton_PPN_or_local_GR_pass |

## 11. Decision

The failed Poisson/Gauss calibration premises are now machine-routed into explicit P8/R11 residual components. This removes a major ambiguity: when PG1 or PG4-PG8 are not derived, the result is no longer a vague 'calibration gap' but concrete rows such as dln_Geff_dt, dln_Meff_dt, eta_source_AB, alpha(lambda), partial_r ln mu_obs, mu_extra/(GM), delta_frame_source, delta_beta_source, and c_nonEH_operator_vector. No numeric residuals or theorem-zero proofs were loaded here, so measured GM, Newton, PPN, and local GR remain unpromoted.

Practical read: this is the referee's scorecard for the Newton route. If the Hamiltonian charge does not become `GM`, we now know exactly which row gets punched: drift, source charge, radial hair, `mu_extra`, frame split, beta source residue, or the R11 operator vector. That is progress because it turns a philosophical blocker into fillable rows.

## 12. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 460-source-normalized-Newton-branch-theorem-stack.md | assemble the finite Newton branch theorem using the PG mapper so the exact remaining derivation debts are visible |
| 2 | fill_or_derive_PG_residual_inputs | the mapper is only useful once rows are filled with theorem-zero proofs, numeric residuals, R10 curves, or R11 vectors |
| 3 | second-order PPN source stability attempt | PG9 remains the direct blocker from first-order Newton source calibration to local-GR/PPN completion |
