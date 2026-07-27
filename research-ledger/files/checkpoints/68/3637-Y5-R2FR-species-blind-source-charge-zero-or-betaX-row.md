# 3637 Y5 R2FR species-blind source charge zero or betaX row

**Status:** 3637 derives the conditional species-blind source-charge theorem and fills the eta_source_AB row as a beta_X species-difference skeleton. The live corpus still lacks the parent no-marker/source-blind proof, so no WEP/source claim is promoted. Crucially, common-mode beta_X remains separate: eta_source_AB can vanish while a universal source coupling still affects R10/Gdot/radial/source-normalization channels.

**Claim ceiling:** no R1 source-WEP, Newton, R10/R11, local-GR, or PPN claim is allowed from 3637.

## Main result

The first comparator is now a clean beta-difference row:

```text
beta_X^A := partial_{X_N} ln(mu_obs^A)
Delta beta_X_AB := beta_X^A - beta_X^B
eta_source_AB = 2|Delta beta_X_AB| / |2 + beta_X^A + beta_X^B|.
```

If parent source/matter labels are species-blind quotient data, `Delta beta_X_AB=0`. That would pass the differential source-charge channel. But it does **not** kill a common `beta_X`; common beta still has to be handled by R10/Gdot/radial/source-normalization rows.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3636 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3636_NEXT_TARGET.csv | True | True | 3636 selected species-blind source charge as first comparator. |
| comparator_3636 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3636_FIRST_COMPARATOR_CHANNEL.csv | True | True | first comparator channel and beta difference formula. |
| source_hair_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | True | True | existing derivative-hair source-charge gate. |
| source_norm_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_source_normalization_residual_vector_TEMPLATE.csv | True | True | template row for eta_source_AB. |
| local_residual_template | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\MTS_local_residual_predictions_TEMPLATE.csv | True | True | local residual R1 source-charge row. |
| constant_gm_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | True | True | current runner says source-charge prediction is missing. |
| local_gr_action_blocks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv | True | True | minimal local-GR action block requiring universal matter/source coupling. |
| fixed_point_conditions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv | True | True | fixed-point condition for common observed coframe and source readout. |
| qbar_source_guard_1027 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md | True | True | guard that WEP/species-blindness does not kill common-mode source charge. |
| marker_guard_1028 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md | True | True | material/EM/clock marker theorem is still missing. |

## Species-blind theorem

| theorem_id | statement | identity | derivation | status |
| --- | --- | --- | --- | --- |
| SBT3637_0_species_charge_definition | For each allowed source/test material label A, define beta_X^A := partial_XN ln mu_obs^A. | Delta beta_X_AB := beta_X^A - beta_X^B = partial_XN ln(mu_obs^A/mu_obs^B) | This is the differential source charge that appears in eta_source_AB. It is distinct from the common-mode source charge. | DEFINITION_EXACT |
| SBT3637_1_species_blind_sufficient_condition | If the parent matter/source functor uses one q-owned action density and species labels theta_A are q-owned/superselected, then beta_X^A=beta_X^B for all A,B. | Lie_XN theta_A=0 and no species-dependent source prefactor => Delta beta_X_AB=0 | The X derivative sees only common q-data, so the species/material difference vanishes. | CONDITIONAL_THEOREM_NOT_PARENT_SIGNED |
| SBT3637_2_eta_zero_corollary | If Delta beta_X_AB=0, source-charge WEP eta_source_AB is zero at this beta-difference level. | eta_source_AB = 2\|beta_X^A-beta_X^B\|/\|2+beta_X^A+beta_X^B\| = 0 | The denominator is finite for small or allowed charges; exact equality of beta charges kills the differential signal. | CONDITIONAL_COROLLARY |
| SBT3637_3_common_mode_guard | Species blindness does not imply beta_X^A=0. A common nonzero beta_X can pass eta_source_AB while still sourcing R10, clocks, or source normalization. | beta_X^A=beta_X^B=beta_common != 0 => eta_source_AB=0 but J_X_source=rho_H beta_common/X_* may survive | WEP constrains differential charge; fifth-force and source-normalization channels also see common charge. | GUARD_PROVED |
| SBT3637_4_live_verdict | The live corpus has the conditional theorem but not the parent no-marker/source-blind signature. | Delta beta_X_AB=0 is not claim-live | Existing gates retain species/material marker and source-prefactor failure modes. | THEOREM_NOT_SIGNED_BETAX_ROW_REQUIRED |

## Beta species decomposition

| decomp_id | quantity | formula | meaning | zero_condition | status |
| --- | --- | --- | --- | --- | --- |
| BXD3637_0_master | Delta beta_X_AB | Delta_AB beta_X = Delta_AB partial_XN ln G_eff + Delta_AB partial_XN ln M_eff + Delta_AB partial_XN ln(1+epsilon_mu) | species/material dependence of the normalized source charge | all three terms vanish componentwise or a parent identity proves universal cancellation | EXACT_DIFFERENCE_IDENTITY |
| BXD3637_1_Geff | Delta_AB partial_XN ln G_eff | 0 only if kappa/G_eff carries no species, composition, source-owner, or material label | global coupling can create source-charge WEP violation if it is species-marked | constant universal coupling superselection with no species labels | OPEN_NOT_PARENT_DERIVED |
| BXD3637_2_Meff | Delta_AB partial_XN ln M_eff | 0 only if Pi_M J_H is source-material blind and calibrated before readout | projected source mass can carry composition dependence through Pi_M, J_H, or source support | source Ward/Hilbert current and Pi_M are parent-owned and selector-blind | OPEN_NOT_PARENT_DERIVED |
| BXD3637_3_epsilon_mu | Delta_AB partial_XN ln(1+epsilon_mu) | 0 only if boundary/bulk/domain/memory/non-EH extra mass channel is absent or universal derivative-free | hidden mass-channel hair can be composition dependent even after common geometry is selected | mu_extra zero theorem or universal constant calibration with no species derivative | FAILED_MISSING_COEFFICIENT_VECTOR |
| BXD3637_4_marker | material/EM/clock marker contribution | Delta beta_marker_AB = sum_i (s_i^A-s_i^B) b_i, including mass, EM binding, clock, or material labels | ordinary matter can be geometrically universal while constants/markers carry X dependence | no-marker theorem or numeric b_i bounds | MISSING_NO_MARKER_THEOREM |

## Common-mode guard

| guard_id | guard | counterexample | effect |
| --- | --- | --- | --- |
| CMG3637_0_wep_scope | eta_source_AB only constrains Delta beta_X_AB, not beta_common. | beta_X^A=beta_X^B=beta_common gives eta_source_AB=0 while alpha_X(lambda) can be nonzero. | passing source-charge WEP cannot promote R10/local-GR silence |
| CMG3637_1_common_fifth_force | common beta_X couples universally to source and test masses. | universal Weyl/source prefactor leaves composition unchanged but mediates a finite-range force if X has a pole | common-mode beta must go to R10/Gdot/radial/source-normalization rows |
| CMG3637_2_marker_loophole | no observed coframe split does not exclude material/EM/clock marker dependence. | m_A(X), alpha_EM(X), or binding-energy markers alter beta_X^A-beta_X^B with the same geometry | no-marker theorem or b_A/b_alpha rows remain required |

## eta source beta row

| row_id | observable | predicted_value | small_charge_limit | beta_difference | bound_or_target | derivation_status | score_status | common_mode_guard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ETA3637_0_betaX_species_difference | eta_source_AB;eta_WEP_source_charge | eta_source_AB = 2\|Delta beta_X_AB\|/\|2+beta_X^A+beta_X^B\| | eta_source_AB ~= \|Delta beta_X_AB\| | Delta beta_X_AB = Delta_AB partial_XN ln G_eff + Delta_AB partial_XN ln M_eff + Delta_AB partial_XN ln(1+epsilon_mu) + Delta beta_marker_AB | abs(eta_source_AB) <= 2.8e-15 or derived universal source charge | symbolic_executable_beta_difference_not_numeric | not_scoreable_until_beta_components_or_zero_theorem | eta_source_AB=0 does not imply beta_common=0 or R10/local-GR silence |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3637_0_theorem | Species-blind source-charge zero is conditionally derived if all species/material labels are q-owned and source action has no species-prefactor X slot. | CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | do not claim R1 source WEP until no-marker/source-blind clauses are parent-signed or beta components are bounded |
| DEC3637_1_row | The eta_source_AB row is now expressed as a beta_X species-difference skeleton tied to the existing 2.8e-15 target. | BETAX_DIFFERENCE_ROW_FILLED | fill or prove zero for Geff, Meff, epsilon_mu, and marker beta components |
| DEC3637_2_guard | A WEP/source-charge pass would not kill common-mode beta_X; R10/Gdot/radial common-mode rows must remain active. | COMMON_MODE_GUARD_LOCKED | next target should attack no-marker theorem or common-mode beta normalization explicitly |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3638-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md | scripts/Y5_R2FR_3638_no_marker_source_theorem_or_beta_component_pack.py | try to prove the no-marker/source-blind theorem for masses, EM constants, material labels, source prefactors, and clock/readout markers; if not, build beta component rows b_A, b_alpha, b_source, and beta_common | either marker/source labels are q-owned and Lie_X theta_A=0, or the beta_X row gains component placeholders with units, sensitivities, observable links, and no-cancellation guards |
