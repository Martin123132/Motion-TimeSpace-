# 985 Y5 R10: WEP Imported-Basis Screening Runner MICROSCOPE TiPt

Status: `Y5_R10_985_WEP_imported_basis_screening_runner_operational_nonclaim_Ci_to_MTS_map_missing`

Claim ceiling: no WEP pass, no `b_kappa` bound, no `b_theta` bound, no source-charge theorem-zero promotion, and no local-GR claim.

## Readout

985 makes the imported-basis branch runnable without making it claimable. The runner computes:

`eta_pred = DeltaY_e*C_Ye + Deltaq_N*C_N + Deltaq_C*C_C + DeltaAbar*C_A`.

The zero branch, identity branch, and multi-axis debug branches are all useful for scale discipline. None of them is MTS evidence until either the parent universal-source zero theorem is signed or the `C_i -> b_theta/b_kappa/b_m` map is derived.

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 984_doc | handoff selecting WEP imported-basis runner | true | true | 984-Y5-R10-source-charge-basis-derivation-or-phenomenological-basis-import.md |
| 984_imported_basis | imported nonclaim charge basis | true | true | source-intake/mts_residuals/P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv |
| 984_basis_map | basis-to-MTS-slot map showing missing b_kappa route | true | true | source-intake/mts_residuals/P8_Y5_R10_984_BASIS_TO_MTS_SLOT_MAP.csv |
| 983_delta_vector | MICROSCOPE alloy proxy deltas | true | true | source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv |
| 983_identity_bounds | identity debug bounds for single-proxy sanity | true | true | source-intake/mts_residuals/P8_Y5_R10_983_IDENTITY_DEBUG_BOUNDS.csv |
| 981_candidates | eta screening envelope source row | true | true | source-intake/mts_residuals/P8_Y5_R10_981_COUPLING_PRIOR_CANDIDATES.csv |

## Coefficient Vector Template

| coefficient_id | symbol | basis_feature | MTS_slot_candidate | status | value | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| C985_0_C_Ye | C_Ye | Y_e_proxy | b_theta_or_b_m | MISSING_PHENOMENOLOGICAL_COEFFICIENT | MISSING | false |
| C985_1_C_N | C_N | neutron_excess_proxy | b_theta_or_b_kappa_after_source_projection | MISSING_PHENOMENOLOGICAL_COEFFICIENT | MISSING | false |
| C985_2_C_C | C_C | coulomb_proxy | b_theta_alpha_EM_first | MISSING_PHENOMENOLOGICAL_COEFFICIENT | MISSING | false |
| C985_3_C_A | C_A | A_bar_proxy | b_m_or_nonstandard_source_marker | MISSING_PHENOMENOLOGICAL_COEFFICIENT | MISSING | false |
| C985_4_S_source | S_source | source_normalization | b_kappa | MISSING_CI_TO_MTS_SLOT_MAP | MISSING | false |

## Screening Scenarios

| scenario_id | description | scenario_type | eta_pred | eta_bound | abs_eta_over_bound | screen_result | why_not_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCEN985_0_parent_zero_debug | all imported coefficients set to zero | parent_zero_debug_only | 0.000000000e+00 | 6.992000000e-15 | 0.000000000e+00 | screen_pass_debug | universal Hilbert source would imply this only if parent gates are signed | false |
| SCEN985_1_identity_Y_e_proxy | single proxy coefficient saturates eta envelope: Y_e_proxy | identity_debug_only | 6.992000002e-15 | 6.992000000e-15 | 1.000000000e+00 | screen_fail_debug | single-proxy dominance is not an MTS source-charge projection | false |
| SCEN985_1_identity_neutron_excess_proxy | single proxy coefficient saturates eta envelope: neutron_excess_proxy | identity_debug_only | -6.992000000e-15 | 6.992000000e-15 | 1.000000000e+00 | screen_pass_debug | single-proxy dominance is not an MTS source-charge projection | false |
| SCEN985_1_identity_coulomb_proxy | single proxy coefficient saturates eta envelope: coulomb_proxy | identity_debug_only | -6.992000000e-15 | 6.992000000e-15 | 9.999999999e-01 | screen_pass_debug | single-proxy dominance is not an MTS source-charge projection | false |
| SCEN985_1_identity_A_bar_proxy | single proxy coefficient saturates eta envelope: A_bar_proxy | identity_debug_only | -6.992000000e-15 | 6.992000000e-15 | 9.999999999e-01 | screen_pass_debug | single-proxy dominance is not an MTS source-charge projection | false |
| SCEN985_2_multiaxis_0.1x_identity | all proxy coefficients set to 0.1 times their identity debug bound | multi_axis_debug_only | -1.398400000e-15 | 6.992000000e-15 | 2.000000000e-01 | screen_pass_debug | simultaneous coefficients can add or cancel; no C_i-to-MTS map supplied | false |
| SCEN985_2_multiaxis_0.01x_identity | all proxy coefficients set to 0.01 times their identity debug bound | multi_axis_debug_only | -1.398400000e-16 | 6.992000000e-15 | 2.000000000e-02 | screen_pass_debug | simultaneous coefficients can add or cancel; no C_i-to-MTS map supplied | false |

## Hard Gates

| gate_id | requirement | gate_result | claim_allowed | detail | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| HG985_0_runner_executes | screening runner produces eta_pred and ratio rows | pass | false | runner arithmetic works but scenarios are debug-only | false |
| HG985_1_parent_zero_claim | parent-zero branch can be claimed | blocked_parent_gates_unsigned | false | universal source theorem is relative, not parent-signed | false |
| HG985_2_imported_basis_claim | imported C_i basis bounds MTS coefficients | blocked_missing_Ci_to_MTS_map | false | C_i are phenomenological placeholders, not b_kappa/b_theta values | false |
| HG985_3_WEP_pass | MICROSCOPE WEP pass for MTS local branch | blocked_no_claim | false | no scored MTS coefficient row exists | false |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC985_0_runner | imported-basis WEP runner | screening_runner_operational_nonclaim | eta prediction arithmetic now exists for zero, identity, and multi-axis debug scenarios | do not treat debug screen pass/fail as theory evidence |
| DEC985_1_theory | MTS coefficient status | Ci_to_MTS_map_missing | imported phenomenological coefficients are not b_kappa or b_theta without a parent coupling map | derive or explicitly choose a Ci-to-slot map before any WEP scoring |
| DEC985_2_best_next | next checkpoint | derive_Ci_to_MTS_slot_map_or_parent_zero_theorem | the runner exists; the remaining physics is the map or the parent zero theorem | write 986 Ci-to-MTS slot map attempt, prioritizing alpha_EM/Coulomb to b_theta and source-normalization to b_kappa |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V985_0_sources | pass | all source files exist and needles are found | 2026-06-14T01:52:00.646520+00:00 |
| V985_1_coefficients_nonclaim | pass | C_i coefficient template rows remain missing/nonclaim | 2026-06-14T01:52:00.646534+00:00 |
| V985_2_scenarios_nonclaim | pass | all runner scenarios remain nonclaim | 2026-06-14T01:52:00.646538+00:00 |
| V985_3_runner_arithmetic | pass | eta_pred ratios parse and are nonnegative | 2026-06-14T01:52:00.646541+00:00 |
| V985_4_hard_gates_safe | pass | hard gates block WEP/MTS coefficient claims | 2026-06-14T01:52:00.646543+00:00 |
| V985_5_next_decision | pass | 986 C_i-to-MTS map or parent-zero theorem selected | 2026-06-14T01:52:00.646546+00:00 |
| V985_6_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T01:52:00.646549+00:00 |
| V985_7_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T01:52:00.646551+00:00 |
| V985_READY | pass | 985 checkpoint pack validation summary | 2026-06-14T01:52:00.646554+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 986-Y5-R10-Ci-to-MTS-slot-map-or-parent-zero-theorem.md | derive the map from phenomenological WEP coefficients C_i to MTS slots b_theta/b_kappa/b_m, or prove the parent universal-source zero theorem instead | Coulomb-to-alpha_EM route, nuclear-binding-to-matter-constant route, source-normalization-to-b_kappa route, hard claim gates | WEP pass, invented C_i values, theorem-zero promotion without parent signatures, GitHub action, formalization-workbench edits | false |
