# 3921 - P00 Common-Mode Source Zero or XiN Numeric Bound Fill

Timestamp: `2026-07-01T10:56:29+00:00`

## Result

The common-mode route now has a sharper exterior theorem:

`C_0 nabla^2 Xi_N = -kappa_R P00[R11]`

If the retained scalar source vanishes in the source-free exterior:

`P00[R11]=0 => nabla^2 Xi_N=0 in the source-free exterior`.

The exterior solution is:

`Xi_N = xi_0 U_N + const + sum_{l>=1,m} a_l r^{-(l+1)}Y_lm`.

The harmless part is only:

`const is gauge; xi_0 U_N is measured-GM calibration if xi_0 is time/source/frame independent`.

Everything else is residual:

`Xi_N^res := Xi_N - xi_0 U_N - const`.

Beta still needs the square law:

`xi_2=2xi_0+xi_0^2 and Xi_N^res=0 => delta_beta_common=0`.

## Meaning

This is the clean split we needed. A P00-zero exterior does not automatically prove local GR, but it says the remaining common mode is either a universal monopole calibration or a real residual. Multipoles, radial shape, time drift, source dependence, boundary/projector/domain stress and nonlocal tails cannot be hidden in measured `GM`.

Fallback bound vector:

`B_Xi := |Delta_sq|/(1+xi_1)^2 + |epsilon_r| + |partial_t ln(1+xi_1)|/B_Gdot + |Delta_AB xi_1|/B_WEP`.

## Source Register

- Source rows found: `22/22`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3921_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3921_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3921_P00_ZERO_HARMONIC_EXTERIOR_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3921_XIN_NUMERIC_BOUND_FILL_ROWS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3921_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3921_NEXT_TARGET.csv`

## Next Target

`3922-Y5-R2FR-boundary-projector-domain-multipole-zero-or-local-bound-fill.md`
