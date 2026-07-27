# 3313 - Upgraded WEP matrix with material-confidence rows under AX1090

Run UTC: `2026-06-27T19:21:46.014275+00:00`

## Verdict

The WEP matrix has been rebuilt using the upgraded material deltas and confidence rows from `3312`.

Every scalar/spin2, MICROSCOPE/Eot-Wash, lambda-grid row now has:

- upgraded `Delta_q` material contrasts;
- a proxy `eta95` row;
- explicit `A_i`;
- explicit `F(lambda)`.

The result is still nonclaim. It bounds `A_i * (s_i dot Delta_q)` only. It does not by itself prove universal source coupling or local GR.

## Source Register

- `SRC3313_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3312-Y5-R2FR-exact-WEP-material-confidence-ledger-or-parent-Ai-proof-under-AX1090.md` — exists=true; role=3312 upgraded input handoff
- `SRC3313_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3312_EXACT_WEP_MATERIAL_LEDGER.csv` — exists=true; role=3312 material ledger
- `SRC3313_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3312_UPGRADED_PAIR_DELTAS.csv` — exists=true; role=3312 upgraded pair deltas
- `SRC3313_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3312_CONFIDENCE_LEDGER.csv` — exists=true; role=3312 confidence rows
- `SRC3313_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3312_BOUND_INPUT_UPDATE.csv` — exists=true; role=3312 bound input updates
- `SRC3313_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3312_NEXT_TARGET.csv` — exists=true; role=3312 next target
- `SRC3313_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3312_VALIDATION.csv` — exists=true; role=3312 validation
- `SRC3313_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3310_WEP_KLAMBDA_ENVELOPE.csv` — exists=true; role=3310 lambda envelope
- `SRC3313_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3311_ALPHA_XI_FACTOR_LAW.csv` — exists=true; role=3311 A_i factor law

## Summary

- `LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt`: best proxy bound `5.38197584536e-15` at lambda=1e+13 m; pair=PAIR3312_0_MICROSCOPE_PtRh10_TA6V.
- `LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti`: best proxy bound `3.528e-13` at lambda=1e+13 m; pair=PAIR3312_1_EOTWASH_Be_Ti.
- `LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt`: best proxy bound `5.38197584536e-15` at lambda=1e+13 m; pair=PAIR3312_0_MICROSCOPE_PtRh10_TA6V.
- `LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti`: best proxy bound `3.528e-13` at lambda=1e+13 m; pair=PAIR3312_1_EOTWASH_Be_Ti.

## Final Claim Blockers

- `FBLK3313_0_parent_Ai` `A_0, A_2`: matrix bounds A_i*s_i combinations, not s_i or local-GR safety alone.
- `FBLK3313_1_exact_assay` `alloy/isotope/purity and binding model`: material charge deltas are upgraded but not exact experimental charges.
- `FBLK3313_2_covariance` `full covariance/systematic confidence treatment`: eta95_proxy is not a final experiment likelihood.
- `FBLK3313_3_cancellation` `scalar/spin2 cancellation rule`: scalar and spin2 rows must stay separate unless parent derives shared/canceling structure.

## Runner

- `RUN3313_0_matrix_complete`: `PASS_NONCLAIM` — rows=44
- `RUN3313_1_summary_complete`: `PASS_NONCLAIM` — LC3308_scalar_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_scalar_WEP3306_1_EOTWASH_Be_Ti;LC3308_spin2_WEP3306_0_MICROSCOPE_Ti_Pt;LC3308_spin2_WEP3306_1_EOTWASH_Be_Ti
- `RUN3313_2_claim_permission`: `REFUSE_CLAIM_PARENT_Ai_ASSAY_COVARIANCE_CANCELLATION_MISSING` — A_0, A_2;alloy/isotope/purity and binding model;full covariance/systematic confidence treatment;scalar/spin2 cancellation rule

## Promotion Gates

- `GATE3313_0_WEP_matrix_claim`: passed=false; claim=upgraded WEP matrix bounds MTS source coefficients for a local-GR claim
- `GATE3313_1_parent_Ai_route`: passed=false; claim=source factor route closed by parent proof
- `GATE3313_2_empirical_route`: passed=false; claim=source factor route closed empirically by WEP matrix

## Decision

- `DEC3313_0`: yes, nonclaim — the matrix now uses upgraded material deltas and proxy 95 confidence rows over the lambda grid
- `DEC3313_1`: not yet — it bounds A_i*s_i projections only; parent A_i, exact assay, covariance, and cancellation policy remain open

## Next Target

- `3314-Y5-R2FR-parent-Ai-derivation-or-final-WEP-likelihood-blocker-ranking-under-AX1090.md`
- `scripts/Y5_R2FR_3314_parent_Ai_derivation_or_final_WEP_likelihood_blocker_ranking.py`
- Objective: rank the remaining source-coupling blockers and attempt parent A_i derivation before spending more effort on exact WEP likelihood/material assay extraction
