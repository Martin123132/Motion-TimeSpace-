# 4345 Y5-R2FR first source-backed owner-tail or Kperp score row

Marker: `PPC4161_FIRST_SOURCE_BACKED_OWNER_TAIL_OR_KPERP_SCORE_ROW_4345`

Decision: `FIRST_NORMALIZED_OWNER_TAIL_AND_KPERP_SCORE_ROWS_BUILT_SOURCE_FORMULA_BACKED_NUMERIC_NONCLAIM`

## Result

4345 builds the first executable nonclaim score rows.

```text
lambda_RI,smoke = pi^2 = 9.869604401089358
R_Lambda ceiling = lambda_RI,smoke * bound_a
Y_Kperp_i = |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)
strict unit-weight ceiling = 1.0e-16
```

These rows are source-formula-backed and numeric, but not claim-valid: real collar spectrum, transfer constants, units, boundary terms, and Kperp coefficients still have to replace the smoke values.

## Handoff

| next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- |
| 4346-Y5-R2FR-fill-real-owner-tail-Kperp-values-or-adopt-clean-sector.md | Can the real lambda_RI and Kperp/owner-tail coefficients be sourced, or can clean sector/zero theorems remove them before scoring? | source/sign physical lambda_RI, B_RI=0, I_RI=0 and Kperp clean sector | fill real numeric C_T,S_T,B_T,I_T,Z_T,W_i^K, Pi_a^RI, B_RI and I_RI rows and run the nonclaim score table |
