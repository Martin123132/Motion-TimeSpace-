# 3911 — PiM/Htau Commutator Zero or First Gdot Numeric Row

Timestamp: `2026-07-01T10:08:07+00:00`

## Result

This pass attacks the source-coupling algebra directly. The `R_PiM + R_Htau` blocker is now a two-part derivation target:

1. a source-domain connection commutator;
2. a covariant-phase-space `H_tau` curl.

Source chart:
`z^A=(M,s^a,r^I) with Pi_M^H=partial_M at fixed shape s^a, reference/surface/frame r^I`

Horizontal lift:
`D_X^H = D_X + A_X^M partial_M + A_X^a partial_a + A_X^I partial_I`

Exact commutator:
`[D_X^H,Pi_M^H]H = -(partial_M A_X^M) partial_M H -(partial_M A_X^a) partial_a H -(partial_M A_X^I) partial_I H`

Mass-flat zero condition:
`if partial_M A_X^M=partial_M A_X^a=partial_M A_X^I=0 and D_X^H keeps tau,Sigma,H_ref fixed, then [D_X^H,Pi_M^H]H=0`

Hamiltonian curl identity:
`curl(delta H_tau)(delta_1,delta_2)=int_S i_tau omega_MTS(delta_1,delta_2)+int_partialS corner_tau(delta_1,delta_2)`

Htau zero condition:
`if tau is fixed/stationary, omega_MTS has zero or exact boundary flux on the source collar, and reference/corner terms are source-blind, then R_Htau=0`

Combined executable bound:
`|R_PiM+R_Htau| <= K_M|partial_M A_X^M| + K_shape||partial_M A_X^a|| + K_ref||partial_M A_X^I|| + |Pi_M int_S i_tau omega_MTS|/|Pi_M H_tau| + |corner_tau|/|Pi_M H_tau|`

## What This Means

- If the parent source geometry forces a mass-flat horizontal lift and an exact/zero source-collar symplectic curl, then `R_PiM+R_Htau=0`.
- If not, the same equations give coefficient rows for a nonclaim `dotG/G` bound.
- The result is not a local-GR/Newton/PPN/R10 claim yet because `A_X^A` and `omega_MTS` are not parent-owned in this checkpoint.

## First Nonclaim Gdot Slot

`Gdot_total <= 0 + (|R_PiM+R_Htau| + |R_Ward| + |R_ref| + |R_W| + |R_frame| + |R_units| + |R_side_flux|) + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|`

The `0` smoke row exists only for the double-zero branch. It remains `valid_for_claim=false` until the parent action signs the source-domain connection and `H_tau` curl exactness.

## Source Register

- Source rows found: `20/20`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3911_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3911_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3911_SOURCE_DOMAIN_CONNECTION_DERIVATION.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3911_FIRST_GDOT_NUMERIC_NONCLAIM_ROW.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3911_BRANCH_DECISION_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3911_NEXT_TARGET.csv`

## Next Target

`3912-Y5-R2FR-source-domain-connection-from-product-quotient-geometry-or-bound-input.md`

Goal: derive `A_X^A` mass-flatness from the parent quotient/product chart, or demote that part to explicit coefficient-bound inputs.
