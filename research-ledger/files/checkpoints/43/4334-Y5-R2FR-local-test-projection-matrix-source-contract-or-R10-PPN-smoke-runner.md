# 4334 Y5-R2FR local-test projection matrix source contract or R10/PPN smoke runner

Marker: `PPC4161_LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_OR_R10_PPN_SMOKE_4334`

Decision: `LOCAL_TEST_PROJECTION_MATRIX_SOURCE_CONTRACT_BUILT_R10_PPN_SMOKE_BLOCKED_UNTIL_NUMERIC_SOURCE_ROWS_NONCLAIM`

## Result

The testing bridge is now explicit: `R_arena = Pi_arena T_open`. The R10/PPN smoke runner exists as a claim-blocking schema and refuses to score placeholders.

## Projection Contract

| arena | projection_symbol | required_numeric_inputs | missing_marker | valid_for_claim |
| --- | --- | --- | --- | --- |
| R10 short-range fifth-force | Pi_R10(lambda) | K_X; Qbar_XH(lambda); P_A qbarXT_vec; lambda_X; alpha_bound(lambda); lab composition support | MISSING_R10_PARENT_COEFFICIENTS_AND_BOUND_CURVE | False |
| PPN/Cassini/local solar tests | Pi_PPN | metric Green operator; gamma/beta transfer; preferred-frame map; Gdot clock/orbital convention; range/profile | MISSING_LOCAL_METRIC_TRANSFER_MATRIX | False |
| clock/redshift/atomic standards | Pi_clock | clock species map; alpha/mass sensitivity coefficients; tau reference convention; EM source normalization | MISSING_CLOCK_SPECIES_TRANSFER_MATRIX | False |
| orbital/ephemeris/binary dynamics | Pi_orbital | GM convention; orbital frame; range/time transfer; source support; no-flux domain map | MISSING_ORBITAL_FRAME_AND_GM_TRANSFER_MATRIX | False |
| EM/stress/Poynting/radiation | Pi_EM | open radiation flux; constitutive deformation; source current normalization; Hodge ownership map | MISSING_EM_FLUX_CONSTITUTIVE_TRANSFER_MATRIX | False |
| WEP/source-composition | Pi_WEP | composition charge basis; material sensitivity matrix; source-normalization map; marker/theta coupling map | MISSING_SOURCE_CHARGE_PROJECTION | False |

## Smoke Status

| arena | focus | score_attempted | smoke_result | claim_allowed |
| --- | --- | --- | --- | --- |
| R10 short-range fifth-force | R10_PPN_FOCUS | False | blocked_missing_projection_matrix | False |
| PPN/Cassini/local solar tests | R10_PPN_FOCUS | False | blocked_missing_projection_matrix | False |
| clock/redshift/atomic standards | SUPPORTING_ARENA | False | blocked_missing_projection_matrix | False |
| orbital/ephemeris/binary dynamics | SUPPORTING_ARENA | False | blocked_missing_projection_matrix | False |
| EM/stress/Poynting/radiation | SUPPORTING_ARENA | False | blocked_missing_projection_matrix | False |
| WEP/source-composition | SUPPORTING_ARENA | False | blocked_missing_projection_matrix | False |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4335-Y5-R2FR-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md | Can one projection row be made source-backed enough to run a genuine nonclaim smoke score? | try Pi_PPN gamma/beta from the local metric-transfer contract; if blocked, try R10 alpha(lambda) using 982/563-style K_X Qbar_XH lambda rows and a real bound curve |
