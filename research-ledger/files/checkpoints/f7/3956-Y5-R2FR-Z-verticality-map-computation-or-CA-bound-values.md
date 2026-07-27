# 3956 - Z Verticality Map Computation Or C_A Bound Values

Timestamp: `2026-07-01T14:33:14+00:00`

## Result

3956 performs the first explicit verticality computation for the response-doublet branch.

Define:

`R_even = (R_+ + R_-)/2`

`Z = (R_+ - R_-)/2`

and the quotient:

`q_RD(R_+,R_-) = R_even`.

Then:

`Dq_RD[partial_Z] = (1/2)(1) + (1/2)(-1) = 0`.

So `Z` is exactly vertical for this constructed response-doublet quotient.

If `g_obs = gbar(R_even,Q_pub,...)` and has no direct `Z` readout, then:

`C_Z = partial_Z g_obs = 0`

and:

`J_Z^obs = 1/2 T_obs C_Z = 0`.

## Honest Scope

This is a real computed branch, not a public claim. Current MTS still needs actual variable adoption:

- actual residual variables mapped to `R_+`, `R_-`, `R_even`, `Z`;
- actual observable metric/readout proved to depend on `R_even` but not `Z`;
- direct/measure/support source-current terms closed.

## Source Register

- Source rows found: `11/11`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3956_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3956_VALIDATION.csv`

## Next Target

`3957-Y5-R2FR-response-doublet-parent-adoption-or-current-Z-map.md`
