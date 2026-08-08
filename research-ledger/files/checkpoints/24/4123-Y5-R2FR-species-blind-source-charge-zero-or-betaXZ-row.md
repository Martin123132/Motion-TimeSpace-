# 4123 - Species-Blind Source-Charge Zero or BetaXZ Row

## Verdict

- Decision: `SPECIES_BLIND_THEOREM_CONDITIONAL_BETAXZ_DIFFERENCE_ROW_FILLED_COMMON_MODE_GUARD_ACTIVE`.
- First comparator is now exact: `eta_source_AB` is a beta-difference row for both `X` and `Z` directions.
- If species/material labels are q-owned and have no `X/Z` marker slot, `Delta beta_X=Delta beta_Z=0` conditionally.
- Common-mode beta remains live: source-charge WEP can pass while R10/Gdot/radial/source-normalization or EM channels still fail.
- No WEP/source or local-GR claim is made.

## Generated Outputs

- `P8_Y5_R2FR_4123_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_SPECIES_BLIND_THEOREM.csv`
- `P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_BETAXZ_SPECIES_DECOMPOSITION.csv`
- `P8_Y5_R2FR_4123_COMMON_MODE_GUARD`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_COMMON_MODE_GUARD.csv`
- `P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_ETA_SOURCE_AB_BETAXZ_ROWS.csv`
- `P8_Y5_R2FR_4123_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_DECISION_GATES.csv`
- `P8_Y5_R2FR_4123_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4123_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4123_STATUS.csv`

## Species-Blind Theorem

| theorem_id | identity | status |
|---|---|---|
| SBT4123_0_species_charge_definition | `Delta beta_{A_res}^{mn}:=beta_{A_res}^m-beta_{A_res}^n=partial_{A_res,N} ln(mu_obs^m/mu_obs^n)` | DEFINITION_EXACT |
| SBT4123_1_species_blind_sufficient_condition | `Lie_{A_res,N} theta_m=0 and no species-dependent source prefactor => Delta beta_{A_res}^{mn}=0` | CONDITIONAL_THEOREM_NOT_PARENT_SIGNED |
| SBT4123_2_eta_zero_corollary | `eta_source_mn=2|beta_{A_res}^m-beta_{A_res}^n|/|2+beta_{A_res}^m+beta_{A_res}^n|=0` | CONDITIONAL_COROLLARY |
| SBT4123_3_common_mode_guard | `beta_{A_res}^m=beta_{A_res}^n=beta_common != 0 => eta_source_mn=0 but J_A_source=rho_H beta_common/A_* may survive` | GUARD_PROVED |
| SBT4123_4_live_verdict | `Delta beta_X^{mn}=Delta beta_Z^{mn}=0 is not claim-live` | THEOREM_NOT_SIGNED_BETAXZ_ROW_REQUIRED |

## Beta Decomposition

| decomp_id | quantity | status |
|---|---|---|
| BXD4123_0_master_X | Delta beta_X_mn | EXACT_DIFFERENCE_IDENTITY |
| BXD4123_1_master_Z | Delta beta_Z_mn | EXACT_DIFFERENCE_IDENTITY |
| BXD4123_2_Geff | Delta_mn partial_AN ln G_eff | OPEN_NOT_PARENT_DERIVED |
| BXD4123_3_Meff | Delta_mn partial_AN ln M_eff | OPEN_NOT_PARENT_DERIVED |
| BXD4123_4_epsilon_mu | Delta_mn partial_AN ln(1+epsilon_mu) | FAILED_MISSING_COEFFICIENT_VECTOR |
| BXD4123_5_marker_EM_clock | Delta beta_marker_mn | MISSING_NO_MARKER_THEOREM |

## Common-Mode Guard

| guard_id | effect |
|---|---|
| CMG4123_0_wep_scope | passing source-charge WEP cannot promote R10/local-GR silence |
| CMG4123_1_common_fifth_force | common-mode beta must go to R10/Gdot/radial/source-normalization rows |
| CMG4123_2_marker_loophole | no-marker theorem or b_mass/b_alpha/b_clock rows remain required |
| CMG4123_3_EM_common_mode | EM common mode must stay in EM/Gdot/R10 rows unless theorem-zeroed |

## Eta Source Rows

| row_id | predicted_value | score_status |
|---|---|---|
| ETA4123_0_betaX_species_difference | `eta_source_mn=2|Delta beta_X_mn|/|2+beta_X^m+beta_X^n|` | not_scoreable_until_beta_components_or_zero_theorem |
| ETA4123_1_betaZ_species_difference | `eta_source_mn=2|Delta beta_Z_mn|/|2+beta_Z^m+beta_Z^n|` | not_scoreable_until_beta_components_or_zero_theorem |

## Next Target

- `4124-Y5-R2FR-no-marker-source-theorem-or-beta-component-pack.md`
- Prove no-marker/source-blindness or build component rows for mass, EM constants, material labels, source prefactors, clock markers, and common-mode beta.
