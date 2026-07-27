# 3964 - Hilbert Source Denominator PiM Owner Or Flux Bound

Timestamp: `2026-07-01T15:16:12+00:00`

## Result

3964 attacks the mass/source denominator needed for Newton:

`M_eff[S] := N_G int_S Pi_M J_H[tau]`.

The core flux identity is:

`M_eff(S2)-M_eff(S1)=N_G int_A d(Pi_M J_H)`.

With the product rule:

`d(Pi_M J_H)=Pi_M dJ_H + (dPi_M) wedge J_H + exchange/boundary/source terms`.

Therefore:

- if `d(Pi_M J_H)=0` from a real parent Ward/topological/Hamiltonian origin, then `M_eff` has no radial/time flux hair;
- if not, the failure is a named residual vector:

`epsilon_Meff_flux <= |Delta_flux|+|Delta_PiM|+|Delta_symp|+|Delta_extra|+|Delta_cal|+|Delta_frame|+|Delta_nonEH|+|Delta_PPN|`.

This feeds the 3963 Newton score:

`epsilon_Newton_source <= |D ln Pi_G| + epsilon_Meff_flux + |D ln(1+epsilon_mu)| + ...`.

## Source/Register

- Sources found: `23/23`
- Denominator identity: `source-intake\mts_residuals\P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv`
- Flux theorem/bound: `source-intake\mts_residuals\P8_Y5_R2FR_3964_PIM_FLUX_CLOSURE_THEOREM_OR_BOUND.csv`
- Residual vector: `source-intake\mts_residuals\P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv`
- Newton feed update: `source-intake\mts_residuals\P8_Y5_R2FR_3964_NEWTON_SOURCE_SCORE_FEED_UPDATE.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3964_VALIDATION.csv`

## Next Target

`3965-Y5-R2FR-PiM-commutator-projector-stress-or-Gauss-bound.md`
