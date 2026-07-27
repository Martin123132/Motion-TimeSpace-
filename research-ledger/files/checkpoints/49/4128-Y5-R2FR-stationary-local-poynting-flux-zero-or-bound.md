# 4128 - Stationary Local Poynting Flux Zero or Bound

## Verdict

- Decision: `STATIONARY_LOCAL_PHI_EM_RAD_ZERO_DERIVED_RADIATIVE_BOUND_RETAINED`.
- For compact stationary isolated local systems, net exterior Poynting leakage `Phi_EM_rad` is zero.
- This does not set the Poynting vector or EM stress to zero; bound-field EM stress remains in `J_H_total`.
- Radiative, driven, external-background, and cosmological branches keep the flux-window bound.

## Generated Outputs

- `P8_Y5_R2FR_4128_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4128_NO_FLUX_THEOREM`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_NO_FLUX_THEOREM.csv`
- `P8_Y5_R2FR_4128_BRANCH_SELECTOR`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_BRANCH_SELECTOR.csv`
- `P8_Y5_R2FR_4128_RESIDUAL_UPDATE`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_RESIDUAL_UPDATE.csv`
- `P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_LOCAL_COUPLING_STATUS.csv`
- `P8_Y5_R2FR_4128_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_DECISION_GATES.csv`
- `P8_Y5_R2FR_4128_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_STATUS.csv`
- `P8_Y5_R2FR_4128_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4128_NEXT_TARGET.csv`

## No-Flux Theorem

| theorem_id | object | status |
|---|---|---|
| NFT4128_0_poynting_identity | Maxwell/Poynting identity | EXACT_OBSERVED_MAXWELL_IDENTITY |
| NFT4128_1_stationary_exterior | stationary isolated exterior collar | STATIONARY_LOCAL_ZERO_DERIVED |
| NFT4128_2_bound_field_guard | bound Coulomb/magnetostatic fields | CIRCULATING_POYNTING_NOT_ERASED |
| NFT4128_3_radiative_fallback | radiative or driven branch | FLUX_BOUND_TEMPLATE_RETAINED |
| NFT4128_4_scope_guard | local not cosmological | LOCAL_BRANCH_ONLY |

## Branch Selector

| branch | result | status |
|---|---|---|
| stationary_isolated_local | Phi_EM_rad=0 | USE_ZERO_ROW_FOR_LOCAL_STATIC_BRANCH |
| stationary_with_internal_circulation | Phi_EM_rad=0 while T_EM and angular/momentum density remain in J_H_total | ZERO_LEAKAGE_NOT_ZERO_STRESS |
| radiative_or_nonstationary | retain epsilon_Phi_EM_rad bound | BOUND_ROW_REQUIRED |
| background_or_incoming_flux | retain signed incoming/outgoing flux row | BOUND_ROW_REQUIRED |

## Residual Update

| symbol | branch | result |
|---|---|---|
| beta_Phi_EM_rad | stationary_isolated_local | 0 |
| epsilon_Phi_EM_rad | stationary_isolated_local | 0 |
| epsilon_EM_source_total_static | stationary_isolated_local | epsilon_Hodge_EM + epsilon_ZQ + epsilon_JQ + epsilon_EM_readout + epsilon_DeltaJ + epsilon_dB_impr |
| epsilon_Phi_EM_rad | radiative_or_background | (|d_t U_EM| + |W_JE| + |Phi_incoming| + |Phi_improvement|)/|G_ref M_H| over declared window |

## Claim Ceiling

- no local_GR, Newton, PPN, R10, Gdot, clock, EM, Maxwell, or source-normalization pass.
- This is a local stationary-branch simplification, not a full EM/local-GR claim.

## Next Target

- `4129-Y5-R2FR-observed-hodge-current-owner-clause.md`
