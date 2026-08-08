# 4127 - Shortest Source Signature Clause Attack

## Verdict

- Decision: `POYNTING_DOUBLE_COUNT_SUBTERM_ELIMINATED_EM_SOURCE_RESIDUAL_REDUCED`.
- One subterm is actually removed: an extra independent Poynting source coefficient is double-counting.
- This works only inside the single dressed source branch `M_H^dress[J_H_total]` from 4126.
- Full EM source ownership is not solved; the remaining residual vector is smaller and sharper.

## Generated Outputs

- `P8_Y5_R2FR_4127_SOURCE_REGISTER`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_POYNTING_ONCE_THEOREM.csv`
- `P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_KILLED_SUBTERM_ROWS.csv`
- `P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_REMAINING_EM_RESIDUALS.csv`
- `P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_EM_BOUND_UPDATE_ROWS.csv`
- `P8_Y5_R2FR_4127_DECISION_GATES`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_DECISION_GATES.csv`
- `P8_Y5_R2FR_4127_STATUS`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_STATUS.csv`
- `P8_Y5_R2FR_4127_NEXT_TARGET`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4127_NEXT_TARGET.csv`

## Poynting Once Theorem

| theorem_id | object | status |
|---|---|---|
| POT4127_0_definition_lock | single dressed source functional | DEFINITION_LOCK_IMPORTED_FROM_4126 |
| POT4127_1_maxwell_balance | Poynting theorem as stress conservation split | POYNTING_IS_HILBERT_FLUX |
| POT4127_2_no_extra_coefficient | extra Poynting source coefficient | EXTRA_POYNTING_COEFFICIENT_ZERO_BY_SINGLE_SOURCE_FUNCTIONAL |
| POT4127_3_double_count_zero | epsilon_EM_double_count | SUBTERM_ELIMINATED_BY_DEFINITION_LOCK |
| POT4127_4_remaining_not_zero | beta_source_EM | FULL_EM_SOURCE_ZERO_UNSIGNED |

## Killed Subterm

| symbol | result | status |
|---|---|---|
| c_Poynt_extra | c_Poynt_extra=0 | EXACT_WITHIN_SINGLE_DRESSED_SOURCE_BRANCH |
| epsilon_EM_double_count | epsilon_EM_double_count=0 for M_source^dress=ell_M(Pi_M J_H_total) | ELIMINATED_AS_INDEPENDENT_RESIDUAL |
| beta_source_EM_reduced | beta_source_EM_reduced=beta_Hodge_EM+beta_ZQ+beta_JQ+beta_Phi_EM_rad+beta_EM_readout+beta_DeltaJ+beta_dB_impr | RESIDUAL_VECTOR_REDUCED_NOT_CLOSED |

## Remaining EM Residuals

| symbol | closure_needed | status |
|---|---|---|
| beta_Hodge_EM | observed-Hodge ownership by q/e_obs | OPEN_OWNER_OR_BOUND_REQUIRED |
| beta_ZQ | unique Maxwell normalization and alpha/charge owner | OPEN_OWNER_OR_BOUND_REQUIRED |
| beta_JQ | same current normalization in Lorentz force and Maxwell stress | OPEN_OWNER_OR_BOUND_REQUIRED |
| beta_Phi_EM_rad | stationary isolated source theorem or explicit flux bound | OPEN_ZERO_OR_BOUND_REQUIRED |
| beta_EM_readout | readout-after-variation closure | OPEN_OWNER_OR_BOUND_REQUIRED |
| beta_DeltaJ | total Hilbert current Ward closure including matter, EM, extra, boundary | OPEN_CURRENT_CLOSURE_REQUIRED |
| beta_dB_impr | boundary silence or explicit retained improvement row | OPEN_BOUNDARY_SILENCE_REQUIRED |

## Claim Ceiling

- no local_GR, Newton, PPN, R10, Gdot, clock, EM, Maxwell, or source-normalization pass.
- This is a coupling-space simplification, not a local-GR pass.

## Next Target

- `4128-Y5-R2FR-stationary-local-poynting-flux-zero-or-bound.md`
