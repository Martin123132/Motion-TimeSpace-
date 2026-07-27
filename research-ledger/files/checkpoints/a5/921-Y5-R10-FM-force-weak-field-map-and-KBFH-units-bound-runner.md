# 921 - Y5/R10 FM Force Weak-Field Map And KBFH Units Bound Runner

Private local-bound interface checkpoint. This is not a public R10, WEP, clock, PPN, orbital, local-GR, or unified-field claim.

Status: `Y5_R10_921_FM_force_weak_field_map_written_KBFH_units_missing_bound_runner_smoke_nonclaim`

Claim ceiling: `FM_force_weak_field_bound_interface_only_no_R10_WEP_PPN_clock_orbital_pass_no_local_GR_claim`

Current result: **the coupling residual now has a weak-field/bounds interface, but it cannot be scored until parent units and projection coefficients exist.**

The internal pressure variable is:

```text
epsilon_FM := |K_BF_H| |A_M| |dPiMJ_leak| / N_FM
              + |K_BF_H| |B_zero_flux| / N_B.
```

That is not yet physics evidence. It becomes a testable prediction only after `K_BF_H`, `A_M`, `J_H`, the weak-field projection coefficients, and any finite range law are parent/source-backed.

The R10 rule remains strict:

```text
a_FM/a_N = alpha_FM (1+r/lambda_FM) exp(-r/lambda_FM)
```

only exists if MTS derives `alpha_FM(lambda_FM)` and `lambda_FM`. Otherwise the row is symbolic and blocked.

## Non-Claim Summary

| status | claim_ceiling | current_result | practical_meaning | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| Y5_R10_921_FM_force_weak_field_map_written_KBFH_units_missing_bound_runner_smoke_nonclaim | FM_force_weak_field_bound_interface_only_no_R10_WEP_PPN_clock_orbital_pass_no_local_GR_claim | weak-field map and bound-runner interface are written; K_BF_H units, parent normalization, range law, and projection coefficients are missing | the coupling branch is now testable in shape but not numerically claimable | 922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md | false | 2026-06-13T17:13:02.200883+00:00 |


## Source Register

| source_id | path | role | needle | exists | needle_found | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 920_doc | 920-Y5-R10-PiM-current-offshell-closure-and-holonomy-zero-or-FM-force-bound.md | hands off F_M_force/K_BF_H/dPiMJ_leak/A_M_holonomy/B_zero_flux source-ready schema | Source-Ready Force Bound Pack | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 920_validation | source-intake/mts_residuals/P8_Y5_BRR545_920_VALIDATION.csv | proves 920 was generated and nonclaim | V920_10_validation_rows_ready | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 920_bound_pack | source-intake/mts_residuals/P8_Y5_R10_920_SOURCE_READY_FORCE_BOUND_PACK.csv | input symbols and required columns for this weak-field map | F_M_force | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 377_fifth_force_map | 377-fifth-force-range-coupling-map.md | Yukawa force-law contract and alpha(lambda) discipline | a_extra/a_GR = alpha_Y (1 + r/lambda_Y) exp(-r/lambda_Y) | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 359_PPN_guardrail | 359-source-locked-PPN-residual-runner-from-derived-force-ledger.md | source-locked local guardrail budget philosophy | gamma_minus_1 | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 374_source_lock_manifest | 374-fifth-force-preferred-frame-source-lock-manifest.md | preferred-frame and fifth-force source-lock manifest | source-lock manifest records | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| 427_bounds_csv | 427-source-normalization-bounds-csv-template-fill.md | local_bound_claims intake discipline: bounds are not MTS predictions | these are bounds on possible residual channels | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | local bound rows for WEP, clocks, PPN, Gdot, R10, and operator ledger | R10_fifth_force | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| R10_digitized_curve | source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv | R10 bound curve file; currently still placeholder/digitization-blocked | MISSING_DIGITIZED_ALPHA_BOUND | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| PPN_template | source-intake/mts_residuals/P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv | PPN evaluator input template for residual vector mapping | gamma | true | true | false | 2026-06-13T17:13:02.200883+00:00 |
| Cextra_force_map | source-intake/mts_residuals/P8_Y5_CEXTRA_BULK_MEMORY_RANGE_FORCE_LAW_MAP.csv | prior force-law map showing R10 curve requirements | R10_alpha_lambda_curve_MTS_source_normalization.csv | true | true | false | 2026-06-13T17:13:02.200883+00:00 |


## Weak-Field Map

| map_id | quantity | definition | formula | needed_inputs | maps_to | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WFM921_0_dimensionless_residual | epsilon_FM | dimensionless local coupling pressure from the mass-gauge matter-current residual | epsilon_FM := \|K_BF_H\| \|A_M\| \|dPiMJ_leak\| / N_FM + \|K_BF_H\| \|B_zero_flux\| / N_B | K_BF_H units; A_M normalization; dPiMJ_leak units; boundary-flux normalization; source path | internal pressure only until projection coefficients are supplied | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_1_Yukawa_R10 | alpha_FM(lambda_FM) | R10 inverse-square-law equivalent only if the residual has a derived finite-range potential | a_FM/a_N = alpha_FM (1+r/lambda_FM) exp(-r/lambda_FM) | lambda_FM; alpha_FM; source coupling; screening/composition; real R10 bound curve | R10_fifth_force | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_2_WEP | eta_FM_AB | composition/source-charge difference induced by the coupling branch | eta_FM_AB := \|C_eta_A epsilon_FM_A - C_eta_B epsilon_FM_B\| | species/source coefficients C_eta_A,B or no-species theorem; materials; normalization | R1_WEP_source_charge | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_3_clock | alpha_clock_FM | clock/redshift sensitivity to nonmetric or source-normalization coupling | alpha_clock_FM := C_clock_FM epsilon_FM_clock | clock projection coefficient; coupling to transition standards; source path | R2_clock_redshift | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_4_PPN_gamma_beta | delta_gamma_FM, delta_beta_FM | metric-potential slip and second-order source-normalization residues | delta_gamma_FM=C_gamma_FM epsilon_FM; delta_beta_FM=C_beta_FM epsilon_FM^2 or C_beta1_FM epsilon_FM | weak-field metric solution; projection to gij and g00 orders; coefficients | R3_gamma;R4_beta | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_5_preferred_frame | alpha1_FM, alpha2_FM, alpha3_FM, xi_FM | preferred-frame/location residues if A_M, holonomy, or Pi_M leakage selects a local frame/domain | alpha_i_FM := C_alpha_i_FM epsilon_FM_frame; xi_FM:=C_xi_FM epsilon_FM_aniso | frame vector/domain orientation; holonomy anisotropy; metric g0i projection | R5_alpha1;R6_alpha2;R7_alpha3;R8_xi | false | false | 2026-06-13T17:13:02.200883+00:00 |
| WFM921_6_Gdot_or_orbital | Gdot_FM_over_G, delta_mu_orbital | time/radial drift of the effective source normalization from nonclosed Pi_M current | Gdot/G ~ d_t epsilon_FM; delta_mu_orbital ~ integral_shell dPiMJ_leak / M | time profile; radial shell profile; orbital normalization; source path | R9_Gdot;orbital_source_normalization | false | false | 2026-06-13T17:13:02.200883+00:00 |


## Units And Projection Audit

| unit_id | symbol | required_unit_decision | current_status | blocks | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| UNIT921_0_KBFH | K_BF_H | coefficient units must make integral A_M wedge Pi_M J_H an action | MISSING_PARENT_UNITS | all numeric force, R10, WEP, PPN, clock, and orbital claims | false | 2026-06-13T17:13:02.200883+00:00 |
| UNIT921_1_A_M | A_M | mass-gauge one-form normalization and whether line integral is dimensionless | MISSING_GAUGE_NORMALIZATION | A_M_holonomy and F_M_force scale | false | 2026-06-13T17:13:02.200883+00:00 |
| UNIT921_2_dPiMJ | dPiMJ_leak | mass-current divergence, shell flux, or dimensionless normalized leakage | MISSING_CURRENT_NORMALIZATION | epsilon_FM and orbital/source-normalization maps | false | 2026-06-13T17:13:02.200883+00:00 |
| UNIT921_3_lambdaFM | lambda_FM | finite range/transition length for any Yukawa-equivalent score | MISSING_RANGE_LAW | R10 alpha(lambda) | false | 2026-06-13T17:13:02.200883+00:00 |
| UNIT921_4_projection_coefficients | C_eta,C_clock,C_gamma,C_beta,C_alpha_i,C_xi | dimensionless weak-field projection coefficients from parent linearization | MISSING_LINEARIZED_PARENT_MAP | arena-specific bound comparison | false | 2026-06-13T17:13:02.200883+00:00 |


## Local Bound Arena Map

| map_id | local_bound_row | observable | upper_bound | units | FM_residual | acceptance_rule | required_MTS_inputs | score_status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BAM921_0_WEP | R1_WEP_source_charge | eta_WEP_source_charge | 2.8e-15 | dimensionless | eta_FM_AB | eta_FM_AB <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_1_clock | R2_clock_redshift | alpha_clock_redshift | 2.48e-05 | dimensionless | alpha_clock_FM | abs(alpha_clock_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_2_gamma | R3_gamma | gamma_minus_1 | 2.3e-05 | dimensionless | delta_gamma_FM | abs(delta_gamma_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_3_beta | R4_beta | beta_minus_1 | 7.8e-05 | dimensionless | delta_beta_FM | abs(delta_beta_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_4_alpha1 | R5_alpha1 | alpha1 | 1e-04 | dimensionless | alpha1_FM | abs(alpha1_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_5_alpha2 | R6_alpha2 | alpha2 | 2e-09 | dimensionless | alpha2_FM | abs(alpha2_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_6_alpha3 | R7_alpha3 | alpha3 | 4e-20 | dimensionless | alpha3_FM | abs(alpha3_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_7_xi | R8_xi | xi | 4e-09 | dimensionless | xi_FM | abs(xi_FM) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_8_Gdot | R9_Gdot | Gdot_over_G | 9.6e-15 | yr^-1 | Gdot_FM_over_G | abs(Gdot/G) <= bound | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |
| BAM921_9_R10 | R10_fifth_force | delta_G_or_fifth_force_yukawa | alpha(lambda) | range-dependent | alpha_FM(lambda_FM) | abs(alpha_FM(lambda)) <= alpha_bound(lambda) | parent units; projection coefficient; source path; numeric residual | not_scored_missing_MTS_inputs | false | 2026-06-13T17:13:02.200883+00:00 |


## Nonclaim Smoke Rows

| smoke_id | branch | input_status | formula | expected_runner_result | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SMK921_0_schema_only_epsilon | FM_force_nonclaim | MISSING_KBFH_UNITS;MISSING_A_NORM;MISSING_dPiMJ_NUMERIC | epsilon_FM = \|K_BF_H\| \|A_M\| \|dPiMJ_leak\| / N_FM | blocked_missing_parent_units | false | false | 2026-06-13T17:13:02.200883+00:00 |
| SMK921_1_R10_symbolic_only | R10_alpha_lambda | MISSING_lambda_FM;MISSING_alpha_FM;R10_DIGITIZED_CURVE_PLACEHOLDER | alpha_FM(lambda_FM) compared to alpha_bound(lambda) | blocked_symbolic_curve_required | false | false | 2026-06-13T17:13:02.200883+00:00 |
| SMK921_2_PPN_vector_placeholder | PPN_WEP_clock_vector | MISSING_projection_coefficients | residual_i = C_i epsilon_FM | blocked_missing_linearized_parent_map | false | false | 2026-06-13T17:13:02.200883+00:00 |


## Branch Decision

| decision_id | branch | verdict | reason | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| BD921_0_map_written | weak_field_bound_interface | schema_ready_nonclaim | FM coupling residual now maps to WEP, clock, PPN, preferred-frame, Gdot/orbital, and R10 arenas | false | false | 2026-06-13T17:13:02.200883+00:00 |
| BD921_1_KBFH_blocks_score | units_and_parent_normalization | main_blocker | without K_BF_H units and A_M/J_H normalization, no numerical force or alpha(lambda) is meaningful | false | false | 2026-06-13T17:13:02.200883+00:00 |
| BD921_2_next | parent_units_or_smoke_runner | selected | next step should either parent-sign K_BF_H normalization or create a strict local-bound smoke runner that fails cleanly | false | false | 2026-06-13T17:13:02.200883+00:00 |


## Claim Gate

| gate_id | claim | blocker | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| CGATE921_0_KBFH_units | K_BF_H has parent-derived units and normalization | not supplied by the current parent action | false | false | 2026-06-13T17:13:02.200883+00:00 |
| CGATE921_1_force_projection | F_M_force projects to a local acceleration/metric residual | linearized parent map and projection coefficients are missing | false | false | 2026-06-13T17:13:02.200883+00:00 |
| CGATE921_2_R10_alpha_lambda | FM branch has a valid alpha(lambda) R10 score | range law, alpha_FM(lambda), and real digitized bound curve are missing | false | false | 2026-06-13T17:13:02.200883+00:00 |
| CGATE921_3_local_bounds_pass | FM branch passes WEP/clock/PPN/orbital/local-GR bounds | smoke rows are schema-only and intentionally invalid for claim | false | false | 2026-06-13T17:13:02.200883+00:00 |


## Next Target

| next_target | objective | include | exclude | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- |
| 922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md | either derive K_BF_H units/normalization from the parent BF/mass-gauge action or run a strict nonclaim local-bound smoke runner that proves all missing fields block scoring | action dimensions, A_M normalization, J_H form degree/units, epsilon_FM normalization, local_bound_claims join, R10 curve status | numeric pass claims, alpha(lambda) without a range law, free G/M absorption, GitHub action, formalization-workbench edits | false | 2026-06-13T17:13:02.200883+00:00 |


## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V921_0_sources_exist_and_needles | pass | all source paths exist and needles are present | 2026-06-13T17:13:02.200883+00:00 |
| V921_1_prior_920_clean | pass | P8_Y5_BRR545_920_VALIDATION.csv clean | 2026-06-13T17:13:02.200883+00:00 |
| V921_2_weak_field_map_nonclaim | pass | weak-field map covers epsilon, R10, WEP, clock, PPN, preferred-frame, and Gdot/orbital rows | 2026-06-13T17:13:02.200883+00:00 |
| V921_3_units_block_scoring | pass | all units/projection prerequisites remain explicit blockers | 2026-06-13T17:13:02.200883+00:00 |
| V921_4_local_bounds_joined | pass | WEP, clock, gamma, beta, alpha1, alpha2, alpha3, xi, Gdot, and R10 bound rows are mapped | 2026-06-13T17:13:02.200883+00:00 |
| V921_5_smoke_rows_block_claim | pass | all smoke rows are expected to block scoring until missing inputs are supplied | 2026-06-13T17:13:02.200883+00:00 |
| V921_6_claim_gates_false | pass | KBFH units, projection, R10, and local-bound pass gates remain false | 2026-06-13T17:13:02.200883+00:00 |
| V921_7_decisions_nonclaim | pass | decision selects parent-units or strict smoke runner without promotion | 2026-06-13T17:13:02.200883+00:00 |
| V921_8_all_generated_rows_nonclaim | pass | all generated rows keep guarded claim fields false | 2026-06-13T17:13:02.200883+00:00 |
| V921_9_formalization_workbench_untouched | pass | formalization_changed_after_cutoff=0 | 2026-06-13T17:13:02.200883+00:00 |
| V921_10_next_target_selected | pass | 922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md | 2026-06-13T17:13:02.200883+00:00 |
| V921_11_validation_rows_ready | pass | validation table constructed | 2026-06-13T17:13:02.200883+00:00 |

