# 3822 - Independent Source Ledger And Local Test-Ready Source Rows

## Status

`PASS_NONCLAIM_LOCAL_SOURCE_LEDGER_AND_TEST_ROWS_BUILT`

This checkpoint turns the active-mass/source-normalization branch into a test-facing ledger. It does not claim local GR or Newton. It says, arena by arena, what can be used as independent source evidence, what is only product evidence, and what input would be source-smuggling.

## Source Evidence Schema

| schema_id | status_label | definition | claim_policy |
| --- | --- | --- | --- |
| SES3822_0_independent_source | independent_source | source mass/geometry/composition is supplied before and outside the tested gravitational residual | can feed a claim only after numeric values, units, uncertainty and provenance exist |
| SES3822_1_product_evidence | product_evidence | the observable constrains G_ref*M_H_ref or a derived product such as mu=GM | cannot prove source normalization by itself |
| SES3822_2_partial_readout | partial_readout | official readout/geometry/time-axis information exists but not the full parent projection kernel | useful for smoke tests; no claim |
| SES3822_3_template_only | template_only | allowed and forbidden source inputs are specified but values are missing | schema-ready; no numerical claim |
| SES3822_4_forbidden_as_source | forbidden_as_source | same observable would be used both to define the source and test the prediction | must remain blocked |

## Local Arena Source Ledger

| arena_id | arena | source_evidence_status | allowed_inputs | forbidden_inputs | mass_input_policy |
| --- | --- | --- | --- | --- | --- |
| ARENA3822_0_R10_lab | R10_short_range_lab | template_only | weighed attractor/test masses; composition/density-volume; apparatus geometry; separation profile; boundary/reference; 3821 stress-virial zero-or-bound vector | Yukawa force fit or alpha(lambda) residual converted into source mass | independent_source_required_before_alpha_claim |
| ARENA3822_1_WEP | WEP_MICROSCOPE_lab | partial_readout | material composition; test-body mass/inertia; official orbit/readout kernel; parent material coupling vector; stress-virial correction vector | eta residual used to choose composition weight or source normalization | composition_source_independent_but_parent_kernel_missing |
| ARENA3822_2_PPN | PPN_gamma_beta | product_evidence | independent body model if available; density/radius/composition priors; PPN readout covariance; fixed G_ref policy | ephemeris mu=GM used as M_H_ref for the same PPN/Newton claim | product_only_until_independent_body_mass_and_PiM_fixedness |
| ARENA3822_3_clock | clock_redshift_Gdot | template_only | geodetic potential model; independent mass/density model; clock trajectory; tau/reference lock; boundary clock class | clock residual used to define the same tau/source potential it tests | independent_potential_model_required |
| ARENA3822_4_orbital | orbital_GM_Gauss | product_evidence | mu_fit as product observable; independent mass model where available; PPN/orbit covariance; radial range bins | M_H_ref=mu_fit/G_ref as source mass for Newton recovery | mu_fit_product_only |
| ARENA3822_5_EM_stress | EM_Poynting_source_stress | template_only | same-current Hilbert stress; EM field energy; Poynting flux; apparatus/support stress; total-system domain | matter-only tube when field energy or Poynting flux has exterior support | total_Hilbert_source_required |

## Correction Vector Arena Map

| map_id | arena | stress_virial_vector | source_mass_vector | no_cancellation_policy |
| --- | --- | --- | --- | --- |
| CVM3822_0_R10_lab | R10_short_range_lab | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | epsilon_pressure_binding_total;epsilon_open_domain;epsilon_surface_stress;R_PiM_commutator | sum_abs components unless a theorem-zero row is source-signed |
| CVM3822_1_WEP | WEP_MICROSCOPE_lab | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | epsilon_pressure_binding_total;epsilon_parent_exchange;epsilon_source_weight;epsilon_pi;epsilon_ai | sum_abs components unless a theorem-zero row is source-signed |
| CVM3822_2_PPN | PPN_gamma_beta | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | epsilon_pressure_binding_total;R_mu_split;R_PiM_commutator;Delta_PPN_readout | sum_abs components unless a theorem-zero row is source-signed |
| CVM3822_3_clock | clock_redshift_Gdot | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | epsilon_covariant_frame;epsilon_boundary_ref;R_clock_tau;R_source_ledger | sum_abs components unless a theorem-zero row is source-signed |
| CVM3822_4_orbital | orbital_GM_Gauss | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | R_mu_split;R_GM_anti_circularity;R_PiM_commutator;epsilon_pressure_binding_total | sum_abs components unless a theorem-zero row is source-signed |
| CVM3822_5_EM_stress | EM_Poynting_source_stress | epsilon_virial_accel+epsilon_surface_stress+epsilon_covariant_frame+epsilon_open_domain+epsilon_parent_exchange | epsilon_open_domain;epsilon_parent_exchange;epsilon_field;epsilon_surface_stress | sum_abs components unless a theorem-zero row is source-signed |

## Local Test-Ready Source Rows

| test_row_id | arena | observable_or_bound | source_input_status | prediction_status | must_not_use |
| --- | --- | --- | --- | --- | --- |
| LTR3822_0_R10_alpha_lambda | R10_short_range_lab | alpha(lambda) or force residual | template_only_no_numeric_source_mass_or_geometry | schema_ready_nonclaim | force residual as mass normalization |
| LTR3822_1_WEP_eta | WEP_MICROSCOPE_lab | eta_AB | partial_readout_nonclaim | bound_target_ready_kernel_missing | eta residual to define species/source weight |
| LTR3822_2_PPN_gamma_beta | PPN_gamma_beta | gamma_minus_1;beta_minus_1 | product_evidence_only | residual_vector_ready_source_mass_missing | ephemeris mu as independent mass |
| LTR3822_3_clock_tau | clock_redshift_Gdot | clock redshift;Gdot-like drift | template_only_clock_owner_missing | obstruction_ledger_ready | clock anomaly to set tau/source potential |
| LTR3822_4_orbital_mu | orbital_GM_Gauss | mu_fit=GM;range residual;precession | product_evidence_only | anti_circularity_guard_ready | M_H_ref=mu_fit/G_ref |
| LTR3822_5_EM_source_stress | EM_Poynting_source_stress | field energy/Poynting stress contribution | template_only_total_domain_required | total_Hilbert_accounting_ready_nonclaim | matter-only support as total source when field support leaks |

## Claim Gates

| gate_id | gate_status | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3822_0_sources | PASS_NONCLAIM | false | all source paths and needles present |
| GATE3822_1_required_arenas | PASS_NONCLAIM | false | R10/WEP/PPN/clock/orbital/EM source rows present |
| GATE3822_2_no_claim_rows | PASS_NONCLAIM | false | all ledger and test rows remain nonclaim |
| GATE3822_3_forbidden_inputs | PASS_GUARD | false | each row declares forbidden source-smuggling inputs |
| GATE3822_4_orbital_GM_guard | PASS_GUARD | false | orbital mu_fit is product evidence only |
| GATE3822_5_independent_source_claim | BLOCKED_INPUT_REQUIRED | false | no numeric independent source row is claim-ready |
| GATE3822_6_Newton_local_GR_claim | BLOCKED | false | source ledger is test-ready but source normalization/Pi_M/PPN gates remain open |

## Next Target

`3823-Y5-R2FR-PiM-total-fixedness-commutator-and-worldtube-domain-zero-or-bound.md`

Target: prove or bound `Pi_M_total` fixedness, `[d,Pi_M]J_H`, and source worldtube/domain stability so the test-facing rows get an actual source-normalization kernel.

## Machine Outputs

| status | summary |
| --- | --- |
| PASS_NONCLAIM_LOCAL_SOURCE_LEDGER_AND_TEST_ROWS_BUILT | 3822 builds local arena source-ledger rows for R10/WEP/PPN/clock/orbital/EM, carries the 3821 stress-virial correction vector into each, and keeps orbital GM as product evidence only. |
