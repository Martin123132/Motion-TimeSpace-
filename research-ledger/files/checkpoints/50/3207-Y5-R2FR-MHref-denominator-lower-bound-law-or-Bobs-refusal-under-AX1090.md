# 3207 - MHref Denominator Lower-Bound Law Or Bobs Refusal Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Bobs residual score, or public-facing result.

## Result

3207 does **not** find a current claim-valid `M_H_ref` value.

It does move the branch forward: the denominator route is no longer only "find `M_H_ref` or stop". The derived escape hatch is a no-cancellation lower-bound law:

```text
alpha_tau[deltaPhi] = int_S(delta Q_tau^MTS - i_tau Theta_MTS) - delta H_ref
M_H_ref := G_ref^-1 * (H_tau[S_outer] - H_ref)
G_ref M_H_ref = G_ref M_EH + sum_i Delta_i
epsilon_abs := sum_i |Delta_i| / (G_ref M_EH)
if M_EH > 0 and epsilon_abs < 1, then M_H_ref >= M_EH(1 - epsilon_abs) > 0
```

That gives two honest routes into the 3206 Bobs runner:

1. exact route: derive `H_tau`, `H_ref`, `G_ref`, same-frame locks, and positivity directly;
2. bound route: source `M_EH` plus every `Delta_i` residual with no cancellation and prove `epsilon_abs < 1`.

Current verdict:

```text
M_H_ref law: derived conditionally.
M_H_ref row: not claim-valid.
Bobs score: still refused.
New route: fill epsilon_abs components, starting with delta_H_tau curl and fixed-reference residual.
```

## Denominator Law

| law_id | object | statement | derivation_status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LAW3207_0_phase_space_one_form | alpha_tau | alpha_tau[deltaPhi]=int_S(delta Q_tau^MTS-i_tau Theta_MTS)-delta H_ref; H_tau exists on a branch only if d_F alpha_tau=0 | EXACT_CONDITIONAL_COVARIANT_PHASE_SPACE_CRITERION | theta_MTS;Q_tau_MTS;boundary_policy;reference_lock;field_space_curl_zero_or_bound | false |
| LAW3207_1_MHref_definition | M_H_ref | M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref) in one tau/coframe/source/readout branch | DEFINITION_LAW_SOURCE_BACKED_BY_2550_NOT_VALUE | finite_H_tau;fixed_H_ref;constant_G_ref;same_frame_lock;positive_value | false |
| LAW3207_2_EH_plus_residual_decomposition | G_ref*M_H_ref | G_ref*M_H_ref = G_ref*M_EH + Delta_nonEH + Delta_ref + Delta_boundary + Delta_projector + Delta_source_measure + Delta_coupling + Delta_Kperp + Delta_EM | LINEAR_RESIDUAL_DECOMPOSITION_OF_THE_CHARGE_BRANCH | source_backed_M_EH_comparator;all_Delta_i_zero_or_finite_bounds_same_frame | false |
| LAW3207_3_positive_lower_bound | M_H_ref_lower_bound | If M_EH>0 and epsilon_abs:=sum_i |Delta_i|/(G_ref*M_EH)<1, then M_H_ref >= M_EH*(1-epsilon_abs)>0 | DERIVED_TRIANGLE_INEQUALITY_BOUND | M_EH_source_row;Delta_i_bound_rows;shared_units;shared_surface;no_EH_import_claim | false |
| LAW3207_4_Bobs_acceptance_rule | Bobs_denominator_input | 3206 may accept either exact positive M_H_ref or a source-backed same-frame lower bound M_H_ref_lower_bound, but not observed orbital GM | ACCEPTANCE_RULE_FOR_FUTURE_RUNNER_PATCH | no current exact value or lower-bound rows exist | false |
| LAW3207_5_current_verdict | current_MTS_Bobs_denominator | law derived, but no current source-backed row satisfies the 3206 positive same-frame denominator gate | BOBS_REFUSAL_REMAINS_ACTIVE | M_EH and Delta_i rows or parent theta/Qtau certificate | false |

## First Candidate Rows

| row_id | symbol | definition | M_H_ref | M_H_ref_lower_bound | status | feeds_3206 | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MH3207_0_exact_candidate | M_H_ref | G_ref^-1*(H_tau[S_outer]-H_ref) | MISSING_EXACT_PARENT_CHARGE_VALUE | NOT_APPLICABLE_EXACT_ROUTE | NOT_VALID_FOR_3206 | DEN3206_00_MH_ref | false |
| MH3207_1_lower_bound_candidate | M_H_ref_lower_bound | M_EH*(1-epsilon_abs), epsilon_abs=sum_i |Delta_i|/(G_ref*M_EH) | MISSING_FROM_BOUND_UNTIL_COMPONENTS_FILLED | MISSING_M_EH_AND_DELTA_I_ROWS | SOURCE_READY_TEMPLATE_ONLY | DEN3206_00_MH_ref_after_runner_patch_or_manual_review | false |

## Positivity Gate

| gate_id | gate | pass | status | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G3207_0_system_worldtube | source system and worldtube fixed before readout | false | MISSING_SYSTEM_WORLDTUBE_SOURCE_ROW | anonymous denominators can normalize the wrong source | false |
| G3207_1_same_frame | same tau/coframe/source/readout frame | false | MISSING_SAME_FRAME_CERTIFICATE | frame mismatch can fake a denominator agreement | false |
| G3207_2_Htau_integrability | alpha_tau field-space curl zero or finite bound | false | MISSING_DELTA_H_TAU_CURL_ZERO_OR_BOUND | without integrability H_tau is not a state function | false |
| G3207_3_fixed_reference | H_ref fixed and source/readout silent | false | MISSING_FIXED_REFERENCE_LOCK | a moving reference can absorb local residuals | false |
| G3207_4_Gref_lock | G_ref constant and parent-owned before orbital calibration | false | CONDITIONAL_ROUTE_NOT_PARENT_ADOPTED | G drift or fitted G can hide source normalization failure | false |
| G3207_5_EH_positive_comparator | M_EH positive same-frame comparator/source row | false | MISSING_SOURCE_BACKED_M_EH_ROW | the lower-bound law needs a positive baseline scale | false |
| G3207_6_residual_bounds | all Delta_i residuals zero or source-backed finite with shared units | false | MISSING_DELTA_I_BOUND_ROWS | epsilon_abs cannot be evaluated without component bounds | false |
| G3207_7_epsilon_less_than_one | epsilon_abs < 1 | false | NOT_EVALUATED_COMPONENTS_MISSING | positivity lower bound fails if residuals can exceed baseline | false |
| G3207_8_no_orbital_GM | no orbital GM, EH-only charge, fitted reference, or post-readout calibration is used as denominator proof | true | ANTI_CIRCULARITY_GUARD_ACTIVE | keeps Newton/GR reduction as output rather than input | false |
| G3207_9_verdict | positive same-frame Bobs denominator exists now | false | DENOMINATOR_LAW_DERIVED_ROW_NOT_FILLED | 3206 remains honestly refused until exact or lower-bound route is sourced | false |

## Bobs Patch Queue

| queue_id | target | patch_or_fill_action | current_status | priority | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BQ3207_0_exact_MHref | P8_Y5_R2FR_3206_BOBS_COMPONENT_SCHEMA DEN3206_00_MH_ref | fill exact M_H_ref row only after H_tau/H_ref/G_ref/same-frame certificates exist | WAITING_FOR_PARENT_CHARGE_CERTIFICATE | 0 | false |
| BQ3207_1_lower_bound | 3206 denominator acceptance extension | allow a source-backed positive lower bound M_H_ref_lower_bound as denominator scale after manual runner patch | DERIVED_LAW_NO_VALUES | 1 | false |
| BQ3207_2_first_component | epsilon_abs residual components | start with Delta_ref and delta_H_tau curl because they block both exact and lower-bound routes | NEXT_DERIVATION_TARGET | 2 | false |

## Decision

`MHREF_DENOMINATOR_LOWER_BOUND_LAW_DERIVED_BOBS_REFUSAL_REMAINS`.

Claim status: `NO_LOCAL_GR_NEWTON_PPN_R10_OR_BOBS_SCORE_CLAIM`.

Best next route: derive or source the first epsilon_abs component, starting with delta_H_tau curl and fixed-reference residual.

Next target:

```text
3208-Y5-R2FR-Htau-one-form-exactness-or-first-DeltaH-curl-bound-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_MHREF_FIRST_ROW_CANDIDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_POSITIVITY_BOUND_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_BOBS_3206_PATCH_QUEUE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3207_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3207_00_inputs_exist | true | inputs=8 |
| VAL3207_01_definition_law_present | true | M_H_ref := G_ref^-1*(H_tau[S_outer]-H_ref) |
| VAL3207_02_lower_bound_law_present | true | M_H_ref >= M_EH*(1-epsilon_abs)>0 if M_EH>0 and epsilon_abs<1 |
| VAL3207_03_candidate_rows_nonclaim | true | candidate_rows=2 |
| VAL3207_04_positivity_gate_refuses | true | denominator law derived but exact/lower-bound values missing |
| VAL3207_05_anti_circularity_guard | true | observed orbital GM is test output, not denominator proof input |
| VAL3207_06_decision_next_target | true | 3208-Y5-R2FR-Htau-one-form-exactness-or-first-DeltaH-curl-bound-under-AX1090 |
| VAL3207_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3207_08_csv_parse | true | P8_Y5_R2FR_3207_INPUTS.csv;P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv;P8_Y5_R2FR_3207_MHREF_FIRST_ROW_CANDIDATE.csv;P8_Y5_R2FR_3207_POSITIVITY_BOUND_GATE.csv;P8_Y5_R2FR_3207_BOBS_3206_PATCH_QUEUE.csv;P8_Y5_R2FR_3207_DECISION.csv |

All generated rows remain `valid_for_claim=false`.
