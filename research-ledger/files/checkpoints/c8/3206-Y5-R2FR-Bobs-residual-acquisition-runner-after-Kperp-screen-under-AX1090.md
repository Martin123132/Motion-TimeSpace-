# 3206 - Bobs Residual Acquisition Runner After Kperp Screen Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, residual score, parent-action promotion, R10 pass, clock pass, orbital pass, or public-facing result.

## Result

3206 turns the Bobs pivot into an executable acquisition/refusal runner.

Verdict:

```text
Bobs runner: built.
Residual score: refused.
Reason: M_H_ref and source-backed component rows are missing.
```

This is progress because the scoring path now has a machine-readable schema and a hard refusal gate, not vibes.

## Component Schema

- `DEN3206_00_MH_ref`: `M_H_ref_same_frame` - positive same-frame Hamiltonian/Newton denominator
- `BOB3206_01_source_measure`: `B_obs_source_measure_over_MH` - projected source-measure / source-normalization leakage
- `BOB3206_02_boundary_improvement`: `B_obs_boundary_improvement_over_MH` - boundary/reference/worldtube improvement flux
- `BOB3206_03_projector_commutator`: `B_obs_projector_commutator_over_MH` - commutator leakage from P_loc/Pi_M/projector/frame split
- `BOB3206_04_corner_edge`: `B_obs_corner_edge_over_MH` - corner/edge/tau-reference/surface mismatch residual
- `BOB3206_05_Kperp_residual`: `B_obs_Kperp_residual_over_MH` - parked Kperp extension residual if local suppression is not parent-derived
- `BOB3206_06_EM_Poynting`: `B_obs_EM_Poynting_over_MH` - EM/Poynting subchannel bound from 3200
- `BOB3206_07_bulk_Euler`: `B_obs_bulk_Euler_over_MH` - bulk reduced Euler/Ward symbol residual
- `BOB3206_08_total_no_cancellation`: `B_observed_reduced_flux_over_MH` - absolute sum of live component bounds with no cancellation credit

## Refusal Gate

- `REF3206_00_denominator`: `M_H_ref positive same-frame denominator` -> `false`; M_H_ref is missing, nonsourced, or not valid_for_claim
- `REF3206_01_components`: `all required Bobs components numeric/source-backed` -> `false`; valid_components=0 required_components=7
- `REF3206_02_no_cancellation`: `absolute no-cancellation total` -> `false`; cannot build total until denominator and every live component row are valid
- `REF3206_03_overall`: `Bobs residual score readiness` -> `false`; SCORE_REFUSED_CURRENT_CORPUS: acquisition schema exists but source-backed rows do not

## Dry Run

- Status: `NOT_RUN_REFUSED`
- Score: `NOT_COMPUTED`
- Interpretation: runner is executable but refuses to score without source-backed denominator and component rows

## Acquisition Queue

- `ACQ3206_00`: `M_H_ref_same_frame` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_01`: `B_obs_source_measure_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_02`: `B_obs_boundary_improvement_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_03`: `B_obs_projector_commutator_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_04`: `B_obs_corner_edge_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_05`: `B_obs_Kperp_residual_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_06`: `B_obs_EM_Poynting_over_MH` -> `MISSING_SOURCE_BACKED_ROW`
- `ACQ3206_07`: `B_obs_bulk_Euler_over_MH` -> `MISSING_SOURCE_BACKED_ROW`

## Decision

`BOBS_RUNNER_BUILT_SCORE_REFUSED_UNTIL_SOURCE_ROWS_EXIST`.

Claim status: `NO_LOCAL_GR_NEWTON_PPN_OR_RESIDUAL_SCORE_CLAIM`.

Decision: the Bobs acquisition runner is now executable and refuses scoring because M_H_ref and all live component rows are missing/source-invalid in the current corpus

Best next route: acquire the first source-backed row, starting with M_H_ref same-frame denominator before any component score

Next target:

```text
3207-Y5-R2FR-MH-ref-denominator-source-row-or-Bobs-runner-remains-refused-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_BOBS_CANDIDATE_INPUT_TEMPLATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_SCORING_REFUSAL_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_DRYRUN_SCORE_TABLE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_NEXT_ACQUISITION_QUEUE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3206_VALIDATION.csv`

## Validation

- `VAL3206_00_inputs_exist`: `true` - inputs=7
- `VAL3206_01_schema_complete`: `true` - schema_rows=9
- `VAL3206_02_template_nonclaim`: `true` - template_rows=9
- `VAL3206_03_refusal_active`: `true` - M_H_ref positive same-frame denominator=false;all required Bobs components numeric/source-backed=false;absolute no-cancellation total=false;Bobs residual score readiness=false
- `VAL3206_04_dryrun_no_score`: `true` - runner is executable but refuses to score without source-backed denominator and component rows
- `VAL3206_05_queue_prioritizes_denominator`: `true` - ACQ3206_00=M_H_ref_same_frame;ACQ3206_01=B_obs_source_measure_over_MH;ACQ3206_02=B_obs_boundary_improvement_over_MH;ACQ3206_03=B_obs_projector_commutator_over_MH
- `VAL3206_06_decision_nonclaim`: `true` - 3207-Y5-R2FR-MH-ref-denominator-source-row-or-Bobs-runner-remains-refused-under-AX1090
- `VAL3206_07_no_claim_leak`: `true` - no local-GR, Newton, PPN, Bobs score, or residual claim
- `VAL3206_08_csv_parse`: `true` - P8_Y5_R2FR_3206_INPUTS.csv;P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA.csv;P8_Y5_R2FR_3206_BOBS_CANDIDATE_INPUT_TEMPLATE.csv;P8_Y5_R2FR_3206_SCORING_REFUSAL_GATE.csv;P8_Y5_R2FR_3206_DRYRUN_SCORE_TABLE.csv;P8_Y5_R2FR_3206_NEXT_ACQUISITION_QUEUE.csv;P8_Y5_R2FR_3206_DECISION.csv

All generated rows remain `valid_for_claim=false`.
