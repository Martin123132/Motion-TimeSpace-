# 3683 - Hilbert-worldtube charge identity or R_Hsrc bound row

**Status:** RHSRC_OPERATOR_AND_BOUND_EM_SUBSLOTS_ZERO_FULL_SOURCE_IDENTITY_BLOCKED_NONCLAIM

This checkpoint attacks the source bridge itself. It does not prove `R_Hsrc=0`, but it removes two genuine non-dynamical pieces: the independent `Pi_M` operator commutator on the typed identity branch, and duplicate stationary bound EM/Poynting source accounting.

## Main result

`R_Hsrc = G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H`.

On the preferred typed Hilbert current branch:

`R_PiMop = 0`.

For stationary bound minimal EM/Poynting stress using the same observed Hodge/current and Hilbert denominator:

`R_EM_bound_duplicate = 0`.

The reduced source-bridge residual is:

`R_Hsrc = R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux`.

The source-ready normalized envelope is:

`abs(z_RHsrc,A) <= (|R_Qtau_owner|+|R_support|+|R_extra|+|R_boundary|+|R_cal|+|R_EM_flux|)/N_H`.

So the next attack is precise: prove or bound `R_Qtau_owner`, not generic coupling.

## Identity audit rows
- `HCI3683_0_target`: TARGET_NOT_PROVED - prove the Hilbert-worldtube charge identity -> the target is exact, but current corpus only supports subslot reductions
- `HCI3683_1_identity_PiM_operator`: EXACT_TYPED_OPERATOR_ZERO - independent Pi_M operator commutator vanishes on the typed identity branch -> R_PiMop = 0 on the preferred Hilbert mass-current complex
- `HCI3683_2_static_EM_dressing`: EXACT_CONDITIONAL_ONCE_ONLY_DRESSING - minimal stationary EM/Poynting stress is part of dressed Hilbert source -> R_EM_bound_duplicate = 0 under the same-denominator branch
- `HCI3683_3_Qtau_equality_gap`: NOETHER_HAMILTONIAN_EQUALITY_MISSING - Q_tau is not yet proved equal to the dressed Hilbert source charge -> R_Qtau_owner remains the dominant bridge residual
- `HCI3683_4_support_qbasic_gap`: SUPPORT_QBASIC_RESIDUAL_RETAINED - source worldtube/support is not fully q-basic and fixed -> R_support remains live
- `HCI3683_5_extra_sector_gap`: EXTRA_SECTOR_RESIDUAL_RETAINED - extra/non-Hilbert mass charge is not zeroed -> R_extra remains live
- `HCI3683_6_boundary_calibration_gap`: BOUNDARY_CALIBRATION_RESIDUAL_RETAINED - boundary/reference and absolute calibration remain unowned -> R_boundary and R_cal remain live
- `HCI3683_7_verdict`: RHSRC_ZERO_NOT_PROVED_TWO_SUBSLOTS_REMOVED - current corpus proves R_Hsrc=0 -> move next to R_Qtau_owner rather than circling generic coupling

## R_Hsrc split rows
- `RHS3683_0_identity_definition`: DEFINITION_NONCLAIM - `R_Hsrc` -> `G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H`
- `RHS3683_1_PiM_operator`: EXACT_TYPED_OPERATOR_ZERO - `R_PiMop` -> `0`
- `RHS3683_2_EM_bound_duplicate`: CONDITIONAL_ONCE_ONLY_ZERO - `R_EM_bound_duplicate` -> `0`
- `RHS3683_3_Qtau_owner`: MISSING_PARENT_NOETHER_HAMILTONIAN_EQUALITY - `R_Qtau_owner` -> `G_ref^-1 Q_tau^MTS - ell_M(Pi_M^H J_H^dress) - dB_H`
- `RHS3683_4_support`: MISSING_SUPPORT_QBASIC_LOCK - `R_support` -> `Delta_Wsource + Delta_frame + Delta_qbasic`
- `RHS3683_5_extra`: MISSING_EXTRA_SECTOR_SILENCE - `R_extra` -> `Pi_M^H J_extra + Q_nonEH + A_parent`
- `RHS3683_6_boundary`: MISSING_BOUNDARY_REFERENCE_ZERO_FLUX - `R_boundary` -> `Delta_ref + Delta_symp + B_flux + dB_H_mismatch`
- `RHS3683_7_calibration`: MISSING_ABSOLUTE_CALIBRATION_BRIDGE - `R_cal` -> `Delta_Gref + Delta_PoissonGauss + Delta_orbital_readout`
- `RHS3683_8_EM_flux`: MISSING_EM_FLUX_OR_CONSTITUTIVE_BOUND - `R_EM_flux` -> `Phi_EM_rad + Delta_Hodge_EM + Delta_EM_norm + C_EM_readout`
- `RHS3683_9_reduced_RHsrc`: REDUCED_NO_CANCELLATION_VECTOR - `R_Hsrc` -> `R_Qtau_owner + R_support + R_extra + R_boundary + R_cal + R_EM_flux`
- `RHS3683_10_normalized_bound`: FORMULA_READY_INPUTS_MISSING - `abs(z_RHsrc,A)` -> `(|R_Qtau_owner|+|R_support|+|R_extra|+|R_boundary|+|R_cal|+|R_EM_flux|)/N_H`

## Bound schema rows
- `RHB3683_0_identity_row`: FORMULA_READY_INPUTS_MISSING - `R_Hsrc` -> `G_ref^-1 Q_tau - Pi_M^H J_H^dress - dB_H`; exact source-bridge residual definition
- `RHB3683_1_operator_zero`: THEOREM_ZERO_SUBSLOT_NONCLAIM - `R_PiMop` -> `0`; typed identity/inclusion Pi_M^H kills independent projector operator commutator
- `RHB3683_2_bound_EM_duplicate_zero`: THEOREM_ZERO_SUBSLOT_NONCLAIM - `R_EM_bound_duplicate` -> `0`; stationary bound minimal EM stress is already in J_H^dress
- `RHB3683_3_Qtau_owner_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_Qtau_owner)/N_H` -> `MISSING_RQTAU_OWNER_BOUND_VALUE`; needs parent Noether charge extraction, integrable H_tau, fixed reference and same-frame source pairing
- `RHB3683_4_support_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_support)/N_H` -> `MISSING_SUPPORT_QBASIC_BOUND_VALUE`; needs q-basic worldtube/support coordinates and fixed source frame
- `RHB3683_5_extra_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_extra)/N_H` -> `MISSING_EXTRA_SECTOR_BOUND_VALUE`; needs non-Hilbert/non-EH/projector/domain mass charge silence or finite coefficient rows
- `RHB3683_6_boundary_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_boundary)/N_H` -> `MISSING_BOUNDARY_REFERENCE_BOUND_VALUE`; needs fixed reference, zero symplectic/reference flux, and boundary convention
- `RHB3683_7_calibration_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_cal)/N_H` -> `MISSING_CALIBRATION_BOUND_VALUE`; needs G_ref ownership, Poisson/Gauss coefficient and orbital readout derivation
- `RHB3683_8_EM_flux_bound`: FORMULA_READY_INPUTS_MISSING - `abs(R_EM_flux)/N_H` -> `MISSING_EM_FLUX_BOUND_VALUE`; needs radiative Poynting flux/Hodge/action-scale/readout bounds
- `RHB3683_9_total_bound`: FORMULA_READY_INPUTS_MISSING - `abs(z_RHsrc,A)` -> `(abs(R_Qtau_owner)+abs(R_support)+abs(R_extra)+abs(R_boundary)+abs(R_cal)+abs(R_EM_flux))/N_H`; source-ready finite envelope; not numeric or claim-valid until N_H and every component norm are sourced

## Dressed source accounting
- `DSA3683_0_dressed_source`: DEFINITION_BRANCH_NONCLAIM - `J_H^dress` -> `J_matter + J_EM(bound) + J_binding + J_pressure + exact_improvements`
- `DSA3683_1_matter_EM_exchange`: CONDITIONAL_EXCHANGE_ZERO - `nabla_mu(T_matter+T_EM)^{mu nu}` -> `0 under common current plus Lorentz exchange cancellation`
- `DSA3683_2_static_bound_EM`: CONDITIONAL_INSIDE_MH - `Delta M_EM_bound` -> `integral_Sigma T_EM(u,u) dV_obs inside M_H`
- `DSA3683_3_radiative_flux`: RETAINED_BOUND_INPUT - `Phi_EM_rad` -> `integral_boundary S_Poynting dot n dA`
- `DSA3683_4_Hodge_mismatch`: RETAINED_BOUND_INPUT - `Delta_Hodge_EM` -> `||*_EM - *_obs[e_obs(q)]|| plus constitutive sub-bounds`
- `DSA3683_5_EM_normalization`: RETAINED_ALPHA_SOURCE_LINK - `Delta_EM_norm` -> `D_X ln lambda_A plus C_XF2/action-scale terms`

## Decisions
- `DEC3683_0_reduction`: REAL_REDUCTION - identity Pi_M^H removes independent projector-operator debt -> remove R_PiMop from R_Hsrc
- `DEC3683_1_poynting_accounting`: REAL_REDUCTION_WITH_GUARDS - static EM/Poynting source accounting is now once-only -> do not double-count static EM as a separate source residual
- `DEC3683_2_not_full_identity`: QTAU_SUPPORT_EXTRA_BOUNDARY_CALIBRATION_RETAINED - R_Hsrc=0 is not proved -> carry reduced residual vector forward
- `DEC3683_3_next_route`: NEXT_BEST_TARGET - Q_tau-to-Hilbert source equality is now the best next throat -> derive R_Qtau_owner=0 or source its bound row
- `DEC3683_4_claim_discipline`: PRIVATE_NONCLAIM - no Newton/local-GR/PPN/R10/WEP claim -> continue privately

## Claim gates
- `CG3683_0_RHsrc_zero`: BLOCKED_REDUCED_RESIDUALS_LIVE - claim R_Hsrc=0 because R_Qtau_owner, support, extra, boundary, calibration and EM flux terms remain unsigned
- `CG3683_1_Newton_GR_source`: BLOCKED_QTAU_AND_CALIBRATION - claim Newton/GR source bridge because Noether charge equality and Poisson/Gauss/orbital calibration are not derived
- `CG3683_2_static_EM_overclaim`: BLOCKED_EM_FLUX_HODGE_NORM - claim all EM/Poynting effects vanish because only stationary bound minimal EM duplicate accounting is zero; radiative/Hodge/normalization terms remain
- `CG3683_3_zg_or_alpha_direct`: BLOCKED_SOURCE_CURRENT_STILL_LIVE - treat alpha/clock as direct s_XF2 evidence because source current bridge still includes R_Hsrc residuals
- `CG3683_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private derivation checkpoint only

## Next target
`3684-Y5-R2FR-Qtau-Hilbert-Noether-bridge-or-RQtau-bound-row.md` via `scripts/Y5_R2FR_3684_Qtau_Hilbert_Noether_bridge_or_RQtau_bound_row.py`.

## Sources
- `handoff_3682`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3682_NEXT_TARGET.csv` exists=True needle_found=True
- `identity_1818`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1818_HILBERT_WORLDTUBE_CHARGE_IDENTITY_THEOREM.csv` exists=True needle_found=True
- `closure_3558`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv` exists=True needle_found=True
- `adoption_3559`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv` exists=True needle_found=True
- `density_3561`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv` exists=True needle_found=True
- `equality_3592`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3592_PIM_HILBERT_EQUALITY_ATTEMPT.csv` exists=True needle_found=True
- `worldtube_3596`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3596_WORLDTUBE_HILBERT_SOURCE_MEASURE_LOCK.csv` exists=True needle_found=True
- `poynting_3612`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv` exists=True needle_found=True
- `hamiltonian_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv` exists=True needle_found=True
- `poisson_contract`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv` exists=True needle_found=True
