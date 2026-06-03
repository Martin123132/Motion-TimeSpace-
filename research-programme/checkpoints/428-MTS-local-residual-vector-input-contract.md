# 428 - MTS Local Residual Vector Input Contract

Private residual-input checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 427 proved the sourced local-bound evaluator can run. This checkpoint defines the missing physics object: the MTS local residual vector.

From this point on, a local-GR/Newton claim is not allowed to mean "the bounds file exists" or "Poisson algebra looks clean." It must mean MTS supplies a 12-component residual vector, with formula sources and derivation status, and that vector is either theorem-zero for the right reason or empirically below sourced bounds.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/MTS_local_residual_vector_input_contract.py` |
| Run directory | `runs/20260602-094500-MTS-local-residual-vector-input-contract` |
| Prediction template | `source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv` |
| Status | `MTS_local_residual_vector_input_contract_written_12_component_prediction_template_ready_no_MTS_residuals_loaded_no_local_GR_pass` |
| Claim ceiling | `MTS_residual_vector_input_contract_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass` |
| Next target | `429-Ward-Bianchi-exchange-owner-for-Poisson-source.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 424-same-frame-EH-source-Poisson-reduction-gate.md | True | Poisson bridge, source_residuals, mu_extra, and PPN-completion blockers |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | EH-operator/source-normalization retained rows and local-bound test matrix |
| 427-source-normalization-bounds-csv-template-fill.md | True | verified external/internal source-bound rows |
| 427-local-bound-runner-v4-evaluate-smoke.md | True | evaluate-mode result showing bounds loaded but MTS residual vector absent |
| source-intake/local_bounds/local_bound_claims.csv | True | sourced local-bound constraints for comparison |
| runs/20260602-093000-local-bound-runner-v4-evaluate-smoke/results/evaluation_digest.csv | True | row IDs, observables, source locks, and symbolic/deferred status |
| 402-EH-source-normalization-parent-pair.md | True | same-frame EH/source and measured-GM normalization equations |

## 4. The 12-Component Residual Vector

| row_id | observable | MTS_output_name | source_bound | current_MTS_status |
| --- | --- | --- | --- | --- |
| R0_identity_coframe_direct | eta_WEP_direct_geometry | eta_geom_AB | 2.8e-15 | closure_control_only |
| R1_WEP_source_charge | eta_WEP_source_charge | eta_source_AB | 2.8e-15 | retained_four_channel_budget |
| R2_clock_redshift | alpha_clock_redshift | alpha_clock | 2.48e-05 | retained_same_frame_clock_check |
| R3_gamma | gamma_minus_1 | gamma_minus_1 | 2.3e-05 | EH_operator_slip_test |
| R4_beta | beta_minus_1 | beta_minus_1 | 7.8e-05 | source_normalization_beta_test |
| R5_alpha1 | alpha1 | alpha1 | 1e-04 | vector_preferred_frame_test |
| R6_alpha2 | alpha2 | alpha2 | 2e-09 | vector_preferred_frame_test |
| R7_alpha3 | alpha3 | alpha3_or_flux_residual | 4e-20 | boundary_exchange_ultratight_test |
| R8_xi | xi | xi | 4e-09 | domain_shear_preferred_location_test |
| R9_Gdot | Gdot_over_G | dln_mu_obs_dt_or_dln_Geff_dt | 9.6e-15 | memory_source_drift_test |
| R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha_of_lambda_curve | alpha(lambda) | symbolic_curve_required |
| R11_EH_operator_ledger | non_EH_operator_coefficients | c_nonEH_operator_vector | symbolic | retained_EH_operator_ledger |

Compactly:

```text
r_local =
(eta_geom, eta_source, alpha_clock, gamma-1, beta-1,
 alpha1, alpha2, alpha3, xi, dln(mu_obs)/dt, alpha(lambda), c_nonEH)
```

The first ten entries can be numeric scalars once a branch is specified. The last two are not scalar placeholders: `alpha(lambda)` is a curve and `c_nonEH` is an operator-coefficient/vector map.

## 5. Local-GR Pass Requirements

| requirement | rows_controlled | empirical_pass_condition | derived_GR_condition |
| --- | --- | --- | --- |
| same_frame_source | R0;R2;R3;R4;R11 | all affected residuals below bounds | condition follows from parent action, not closure |
| EH_operator_selection | R3;R4;R5;R6;R8;R10;R11 | mapped residuals below bounds and R11 vector supplied | R11 theorem-zero or exact coefficient map from parent action |
| source_residuals_zero | R1;R4;R7;R9;R10 | source, beta, flux, drift, and fifth-force residuals below bounds | Ward/Bianchi exchange owner kills q_loc^nu and mu_extra without axiom |
| measured_GM_normalized | R1;R4;R9;R10 | eta_source, beta, Gdot, alpha(lambda) below bounds | partial_A mu_obs = partial_t mu_obs = partial_lambda mu_obs = 0 by theorem |
| PPN_completion | R3;R4;R5;R6;R7;R8 | PPN residual vector below sourced bounds | second-order weak-field expansion reduces to GR, not only Poisson/Newton |
| symbolic_rows_resolved | R10;R11 | curve/vector evaluator can compare against sourced constraints | finite-range and non-EH channels vanish or are parent-forbidden |

This is the key distinction:

```text
empirical viability: residuals are below sourced bounds
derived local GR: same-frame + EH + source-normalization + PPN + symbolic rows are parent-derived
```

The first is a good Mayweather round. The second is the title belt.

## 6. Comparison Rules

| rule_id | applies_to | algorithm | fail_label |
| --- | --- | --- | --- |
| numeric_abs_compare | R0-R9 numeric rows | compare max(abs(predicted_value), abs(upper_envelope if supplied)) to sourced upper_bound in matching units | empirical_residual_exceeds_bound |
| symbolic_curve_compare | R10 fifth-force row | load curve_or_vector_file with lambda and alpha_predicted(lambda), compare to alpha_bound(lambda) over declared range | curve_missing_or_exceeds_bound |
| operator_vector_compare | R11 non-EH operator row | load coefficient vector and require maps to affected PPN/fifth-force rows or theorem-zero proof | operator_vector_missing_or_unmapped |
| derivation_status_gate | all rows | closure_assumed/speculative rows can be empirical stress tests but cannot support derived_local_GR_candidate | claim_request_exceeds_derivation_status |
| all_rows_or_no_local_GR | full vector | derived local GR requires all 12 rows resolved plus same-frame/EH/source-normalization proofs | partial_vector_no_local_GR |

## 7. Bound Alignment

| row_id | component_bound | evaluate_upper_bound | alignment_status |
| --- | --- | --- | --- |
| R0_identity_coframe_direct | 2.8e-15 | 2.8e-15 | pass |
| R1_WEP_source_charge | 2.8e-15 | 2.8e-15 | pass |
| R2_clock_redshift | 2.48e-05 | 2.48e-05 | pass |
| R3_gamma | 2.3e-05 | 2.3e-05 | pass |
| R4_beta | 7.8e-05 | 7.8e-05 | pass |
| R5_alpha1 | 1e-04 | 1e-04 | pass |
| R6_alpha2 | 2e-09 | 2e-09 | pass |
| R7_alpha3 | 4e-20 | 4e-20 | pass |
| R8_xi | 4e-09 | 4e-09 | pass |
| R9_Gdot | 9.6e-15 | 9.6e-15 | pass |
| R10_fifth_force | alpha(lambda) | alpha(lambda) | pass |
| R11_EH_operator_ledger | symbolic | symbolic | pass |

## 8. Prediction Intake Artifacts

| artifact | exists | row_count | purpose |
| --- | --- | --- | --- |
| MTS_local_residual_predictions_TEMPLATE.csv | True | 12 | blank prediction template; not MTS evidence |
| README.md | True |  | rules for filling MTS residual predictions |

## 9. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | 0 missing source paths |
| residual_schema_written | pass | 16 schema columns |
| twelve_component_vector_written | pass | 12 residual components |
| prediction_template_written | pass | research-programme\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv |
| bound_alignment_checked | pass | 0 row-bound alignments need review |
| symbolic_components_marked | pass | 2 symbolic/curve/vector components |
| local_GR_pass_requirements_written | pass | 6 all-row requirements |
| comparison_rules_written | pass | 5 comparison rules |
| MTS_residuals_loaded | not_run | template only; no MTS prediction values supplied |
| local_GR_promoted | fail | input contract only; no WEP/EH/Newton/PPN/fifth-force pass |
| claim_ceiling_enforced | pass | MTS_residual_vector_input_contract_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass |

## 10. Decision

The MTS local residual vector is now defined as a 12-component object aligned to the sourced local-bound evaluator. No MTS predictions were loaded. The next physics bottleneck is to derive or estimate the components, especially q_loc^nu/source_residuals/mu_extra and the R10/R11 symbolic rows.

Practical read: the project now has a real empirical spine for the local-GR question. The testing side is no longer the bottleneck. The bottleneck is derivation: can MTS produce `source_residuals=0`, `mu_extra=0`, no preferred-frame/domain leakage, and a resolved R10/R11 curve/vector story without sneaking in GR?

## 11. Next Target

`429-Ward-Bianchi-exchange-owner-for-Poisson-source.md`
