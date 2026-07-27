# 3961 - EM Poynting Hidden F2 Exclusion Or Flux Bound Values

Timestamp: `2026-07-01T15:02:41+00:00`

## Result

3961 derives the EM source-current danger directly:

`J_A^EM|0 = -(1/4mu0)[(partial_A f)|0 F^2 + (partial_A g)|0 F*F] + J_A^Hodge + J_A^readout`.

This means gauge symmetry alone is not enough. `F^2` and `F*F` are legal scalars.

The clean zero route is:

`f(Y)=f_0 + fbar Sigma_loc(Y)+...`, `g(Y)=g_0 + gbar Sigma_loc(Y)+...`

so `partial_A f|0 = partial_A g|0 = 0` because `Sigma_loc=G_ABY^AY^B` has a double zero.

For the Poynting channel:

`dU_EM/dt + integral_boundary S dot n = - integral_D J dot E`.

So the stationary isolated branch gives `Phi_EM_rad=0`; otherwise it is bounded by field-energy change plus matter work.

## Source/Register

- Sources found: `19/19`
- Hidden EM variation: `source-intake\mts_residuals\P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv`
- Sigma EM gate: `source-intake\mts_residuals\P8_Y5_R2FR_3961_SIGMA_FACTOR_EM_EXCLUSION_GATE.csv`
- Poynting theorem/bound: `source-intake\mts_residuals\P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv`
- First zero values: `source-intake\mts_residuals\P8_Y5_R2FR_3961_EM_FIRST_CONDITIONAL_ZERO_VALUES.csv`
- Bound templates: `source-intake\mts_residuals\P8_Y5_R2FR_3961_EM_BOUND_VALUE_TEMPLATES.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3961_VALIDATION.csv`

## Next Target

`3962-Y5-R2FR-EM-residual-vector-first-score-or-Hodge-owner-lock.md`
