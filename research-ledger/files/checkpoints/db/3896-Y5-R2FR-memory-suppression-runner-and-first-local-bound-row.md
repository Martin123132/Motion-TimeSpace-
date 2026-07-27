# 3896 - Memory Suppression Runner and First Local Bound Row

Generated: `2026-07-01T08:53:08+00:00`

## Result

3896 turns the 3895 suppression formula into an executable non-claim runner.

Runner equations:

- `X_static_bound=(J_open_plus_B_lift)/(a_min*C_P_over_L_D2+m_min2)`
- `X_dynamic_bound=exp(-gamma_mem_Delta_t)*X_initial+(1-exp(-gamma_mem_Delta_t))*X_static_bound`
- `DeltaO_i_bound=K_i*X_dynamic_bound+K_i_grad*gradX_bound`

The live MTS row is intentionally blocked because the parent-owned numbers are still not filled. The runner also includes two artificial dry-runs: one checks arithmetic can pass a bound, and one proves the runner rejects a non-positive gap. This is not a physics claim; it is the machinery needed before a physics claim can even be evaluated.

## Input Schema

| field | role | units | required | claim_gate |
| --- | --- | --- | --- | --- |
| a_min | principal-symbol lower bound | dimensionless after normalization | True | must be parent-signed positive |
| C_P_over_L_D2 | Poincare/domain eigenvalue lower bound | 1/length^2 | True | must be sourced by local matching domain |
| m_min2 | memory mass/gap lower bound | 1/length^2 | True | must be parent-derived or zero-mode removed |
| J_open_plus_B_lift | remaining wall/boundary/history source norm | operator-normalized source | True | must sum real component norms with no cancellation credit |
| gamma_mem_Delta_t | history suppression exponent | dimensionless | True | must come from retarded kernel/local matching interval |
| X_initial | incoming memory amplitude | X units | True | zero only if no-incoming-memory clause is signed |
| gradX_bound | gradient memory bound | X/length | False | needed for gradient-sensitive arenas |
| K_i | observable derivative with respect to X_mem | arena units per X | True | must be differentiated from readout map |
| K_i_grad | observable derivative with respect to grad X_mem | arena units per X/length | False | must be differentiated from readout map |

## Local Bound Anchors

| bound_id | arena | observable | bound_value | units | comparison | source_path |
| --- | --- | --- | --- | --- | --- | --- |
| BND3896_0_alpha3 | PPN/preferred-frame | alpha3 | 4e-20 | dimensionless | abs(predicted_alpha3) <= bound_value | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv |
| BND3896_1_Gdot | clock/orbital/local-G drift | abs(Gdot/G) | 9.6e-15 | yr^-1 | abs(predicted_Gdot_over_G) <= bound_value | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv |
| BND3896_2_alpha2 | PPN/preferred-frame | alpha2 | 2e-09 | dimensionless | abs(predicted_alpha2) <= bound_value | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv |
| BND3896_3_xi | PPN/preferred-location | xi | 4e-09 | dimensionless | abs(predicted_xi) <= bound_value | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv |
| BND3896_4_gamma | PPN/R10 gamma-scale | abs(gamma-1) | 2.3e-05 | dimensionless | abs(predicted_gamma_minus_one) <= bound_value | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv |

## Runner Inputs

| case_id | case_type | arena | a_min | C_P_over_L_D2 | m_min2 | J_open_plus_B_lift | gamma_mem_Delta_t | K_i | bound_to_compare | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIVE3896_placeholder | live_candidate | all | MISSING_PARENT_SIGN | MISSING_DOMAIN_SCALE | MISSING_MEMORY_GAP | MISSING_SOURCE_NORM | MISSING_HISTORY_KERNEL | MISSING_ARENA_DERIVATIVE | MISSING_BOUND_SELECTION | False |
| DRY3896_unit_pass | artificial_arithmetic_check | alpha3 | 1.0 | 1.0 | 0.0 | 1e-25 | 5.0 | 1.0 | 4e-20 | False |
| DRY3896_gap_fail | artificial_failure_check | alpha3 | 0.0 | 0.0 | 0.0 | 1e-25 | 1.0 | 1.0 | 4e-20 | False |

## Runner Output

| case_id | arena | lambda_gap | X_static_bound | X_dynamic_bound | DeltaO_bound | bound_to_compare | runner_status | failure_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LIVE3896_placeholder | all |  |  |  |  | MISSING_BOUND_SELECTION | BLOCKED_MISSING_INPUTS | a_min;C_P_over_L_D2;m_min2;J_open_plus_B_lift;gamma_mem_Delta_t;X_initial;K_i;bound_to_compare |
| DRY3896_unit_pass | alpha3 | 1.0 | 1e-25 | 9.932620530009146e-26 | 9.932620530009146e-26 | 4e-20 | PASS_DRYRUN_ARITHMETIC_ONLY |  |
| DRY3896_gap_fail | alpha3 | 0.0 |  |  |  | 4e-20 | FAIL_NONPOSITIVE_GAP | lambda_gap<=0 |

## Local-GR Decision Gate

| gate_id | gate | result | status | claim_allowed |
| --- | --- | --- | --- | --- |
| LGG3896_0_schema | memory suppression schema | all required fields are explicit | PASS_EXECUTABLE_SCHEMA | False |
| LGG3896_1_bounds | first local bound anchors | alpha3/Gdot/alpha2/xi/gamma anchors carried as comparison bounds only | PASS_BOUNDS_NONCLAIM | False |
| LGG3896_2_live | live MTS memory row | live candidate row remains blocked by missing parent numeric inputs | BLOCKED_MISSING_PARENT_NUMBERS | False |
| LGG3896_3_arithmetic | runner arithmetic | dry-run pass and nonpositive-gap failure are both detected | PASS_DRYRUN_ONLY | False |
| LGG3896_4_local_GR | local-GR promotion | no claim until live sourced MTS inputs beat local bounds | BLOCKED_NO_CLAIM_EXECUTABLE_ROUTE_OPEN | False |

## Source Register

Resolved `7/7` source rows.

| source_id | path | needle_found | role |
| --- | --- | --- | --- |
| SRC3896_00_next | source-intake\mts_residuals\P8_Y5_R2FR_3895_NEXT_TARGET.csv | True | 3895 selected executable suppression runner |
| SRC3896_01_law | source-intake\mts_residuals\P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv | True | 3895 static memory suppression law |
| SRC3896_02_numeric | source-intake\mts_residuals\P8_Y5_R2FR_3895_FIRST_NUMERIC_MEMORY_ROW_INTERFACE.csv | True | 3895 numeric row interface |
| SRC3896_03_gate | source-intake\mts_residuals\P8_Y5_R2FR_3895_LOCAL_GR_DECISION_GATE.csv | True | 3895 no-claim local-GR gate |
| SRC3896_04_validation | source-intake\mts_residuals\P8_Y5_BRR545_3895_VALIDATION.csv | True | 3895 validation |
| SRC3896_05_bound_pack | source-intake\mts_residuals\P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv | True | existing local pressure-bound anchor row |
| SRC3896_06_status | source-intake\mts_residuals\P8_Y5_R2FR_3895_STATUS.csv | True | 3895 status |

## Next Target

| next_id | target_checkpoint | objective | why_next |
| --- | --- | --- | --- |
| NEXT3896_0 | 3897-Y5-R2FR-derive-memory-Ki-projection-or-fill-first-physical-row.md | derive the observable projection derivatives K_alpha3, K_Gdot, K_gamma, K_R10, K_clock, K_orbital from the readout map; if derivation fails, keep the runner live but mark physical rows blocked | 3896 made the suppression bound executable, so the next non-circular move is deriving the arena K_i maps rather than creating more missing-input ledgers |

## Bottom Line

This checkpoint gives us a working scoreboard for the memory branch. The next hard leap is no longer "find what is missing"; it is deriving the projection coefficients `K_i` from the readout map so a physical memory row can be run against the local bounds.
