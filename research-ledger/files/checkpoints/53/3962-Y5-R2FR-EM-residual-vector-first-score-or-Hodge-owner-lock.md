# 3962 - EM Residual Vector First Score Or Hodge Owner Lock

Timestamp: `2026-07-01T15:07:23+00:00`

## Result

3962 turns the EM leftovers into one scoreable vector:

`epsilon_EM <= A_F(|f_A| ||F^2|| + |g_A| ||F*F||) + A_H|Delta_Hodge_EM| + A_P|Phi_EM_rad| + A_R|C_EM_readout| + A_W|w_EM-1| + A_Q|C_JQ|`.

Known conditional zero pieces:

- visible minimal Maxwell extra-source leakage is zero if it uses `*_obs` and is inside `T_total`;
- internal matter-EM exchange is bookkeeping-zero in total stress;
- hidden `F^2/F*F` linear source is zero if the coefficient factorizes through `Sigma_loc` or no hidden-visible Hom exists;
- Poynting flux is zero on the stationary isolated no-flux branch;
- Hodge leakage is zero if `*_EM=*_obs[e_obs(q)]`.

Still open:

- `C_EM_readout`;
- `w_EM-1`;
- `C_JQ`;
- global parent signing of the Hodge/readout/normalization owner.

## Source/Register

- Sources found: `18/18`
- EM residual vector: `source-intake\mts_residuals\P8_Y5_R2FR_3962_EM_RESIDUAL_VECTOR.csv`
- Hodge owner gate: `source-intake\mts_residuals\P8_Y5_R2FR_3962_HODGE_OWNER_LOCK_OR_BOUND.csv`
- First score row: `source-intake\mts_residuals\P8_Y5_R2FR_3962_EM_FIRST_NONCLAIM_SCORE_ROW.csv`
- C_A feed update: `source-intake\mts_residuals\P8_Y5_R2FR_3962_CA_TOTAL_EM_FEED_UPDATE.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3962_VALIDATION.csv`

## Next Target

`3963-Y5-R2FR-source-coupling-product-Newton-G-constancy-or-residual-score.md`
