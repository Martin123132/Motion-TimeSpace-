# 3634 Y5 R2FR explicit q-map and DqZ evaluation or X source row

**Status:** 3634 converts Dq_Z_norm from a missing placeholder into an exact positive component norm. The no-cancellation lemma says local verticality requires four zeros, not a tuned sum: geometry, source/readout, clock/marker, and boundary/projector. The strongest next attack is the coupling block partial_Z M_obs, because source/readout leakage reopens J_X even if geometry looks vertical.

**Claim ceiling:** no DqZ theorem-zero, local-GR, PPN, R10/R11, WEP, clock, or Newton claim is allowed from 3634.

## Main result

The first real calculation target is now in a form we can actually attack:

```text
||Dq[partial_Z]||_Q^2 = w_G||partial_Z G_obs||^2
                       + w_M||partial_Z M_obs||^2
                       + w_T||partial_Z Theta_obs||^2
                       + w_B||partial_Z B_obs||^2,
w_i > 0.
```

Therefore `Dq_Z_norm=0` requires componentwise zero. No cancellation trick is allowed. This is useful because it says exactly where the coupling hunt goes next: the source/readout block `partial_Z M_obs`.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3633_NEXT_TARGET.csv | True | True | 3633 handoff: construct q enough to evaluate Dq[partial_Z]. |
| q_map_3633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3633_CANDIDATE_Q_MAP.csv | True | True | candidate q components and excluded fibre condition. |
| dqz_target_3633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3633_BOUND_PACK_FILL_TARGETS.csv | True | True | first selected non-vague target from the absent-pole audit. |
| q_audit_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv | True | True | prior q audit showing q is not computable yet. |
| field_chart_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv | True | True | field chart separating visible quotient data from residual vector candidates. |
| dq_tests_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv | True | True | existing Dq_Z test says Z basis and q dependence are missing. |
| retained_dq_leaks_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv | True | True | older retained Dq leak row now upgraded from missing formula to component norm. |
| status_3633 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3633_STATUS.csv | True | True | 3633 status selecting Dq_Z_norm as the next exact test. |

## q-map component norm

| norm_id | component | definition | normalization | zero_condition | no_cancellation_guard | status |
| --- | --- | --- | --- | --- | --- | --- |
| NORM3634_0_full_definition | Dq_Z_norm | \|\|Dq[partial_Z]\|\|_Q^2 = w_G\|\|partial_Z G_obs\|\|^2 + w_M\|\|partial_Z M_obs\|\|^2 + w_T\|\|partial_Z Theta_obs\|\|^2 + w_B\|\|partial_Z B_obs\|\|^2 | each norm is dimensionless after dividing by its arena reference scale; weights w_i are strictly positive | Dq_Z_norm=0 iff every component derivative is zero | positive weights forbid source/boundary cancellation against geometry | EXACT_COMPONENT_NORM_DEFINITION |
| NORM3634_1_geometry | G_obs=(e_obs,g_obs,nabla_obs) | \|\|partial_Z G_obs\|\|^2_G | coframe/metric/connection norm in observed local frame | partial_Z e_obs=0, partial_Z g_obs=0, and partial_Z nabla_obs=0 | geometry cannot cancel source or boundary components | COMPONENT_DEFINED_NOT_EVALUATED |
| NORM3634_2_source_readout | M_obs=(mu_obs, GM readout, source mass, orbit/Hamiltonian normalization) | \|\|partial_Z M_obs\|\|^2_M | dimensionless source/readout norm after dividing by measured reference mass or Hamiltonian scale | partial_Z mu_obs=0 and no Z-dependence in GM calibration/source charge | source coupling cannot be hidden by a geometry zero | COMPONENT_DEFINED_NOT_EVALUATED |
| NORM3634_3_clock_marker | Theta_obs=(clock map, constants, material markers) | \|\|partial_Z Theta_obs\|\|^2_T | dimensionless marker/clock norm | clock rate, constants, and material labels are q-owned or externally fixed | clock/marker leakage is independently bounded | COMPONENT_DEFINED_NOT_EVALUATED |
| NORM3634_4_boundary_projector | B_obs=(boundary class, Pi_M, reference term) | \|\|partial_Z B_obs\|\|^2_B | dimensionless boundary/projector norm on compact local collar | Q_boundary[partial_Z]=0, exact, or proper and Pi_M has no Z leakage | edge charge is not allowed to compensate bulk silence | COMPONENT_DEFINED_NOT_EVALUATED |

## No-cancellation lemma

| lemma_id | statement | derivation | use_in_framework | status |
| --- | --- | --- | --- | --- |
| LEM3634_0_positive_norm | For positive weights and positive-definite component norms, Dq_Z_norm=0 is equivalent to componentwise zero. | A sum of nonnegative terms w_i\|\|A_i\|\|^2 can vanish only when each A_i vanishes. | This prevents a fake local-GR pass where source or boundary leakage is cancelled by a tuned geometry sign. | PROVED_CONDITIONAL_ON_NORM_CHOICE |
| LEM3634_1_component_zero_contract | The strict quotient route must prove four separate zeros: geometry, source/readout, clock/marker, and boundary/projector. | Dq[partial_Z]=(partial_Z G_obs, partial_Z M_obs, partial_Z Theta_obs, partial_Z B_obs). | A geometry-only proof is insufficient; the coupling/source block is a first-class target, not an afterthought. | PROVED_AS_DEFINITIONAL_SPLIT |
| LEM3634_2_failure_mode | If any component derivative is nonzero or unsigned, Z cannot be promoted to an absent quotient fibre for local tests. | nonzero partial_Z component implies Dq[partial_Z] != 0, so Z is visible to at least one physical readout. | The branch then moves to J_X/Dq leak coefficient rows instead of another theorem-zero attempt. | PROVED_DECISION_RULE |

## Component evaluation

| component_id | component | current_best_case | live_evidence | evaluation | needed_to_close | opens_if_fails |
| --- | --- | --- | --- | --- | --- | --- |
| DQZ3634_0_geometry | partial_Z G_obs | zero if the observed metric/coframe are defined wholly from q and Z is only representative fibre | field-chart 1667 gives partial alignment but not action/coframe ownership | UNSIGNED_ZERO_CANDIDATE | explicit e_obs(Phi), g_obs(Phi), and nabla_obs(Phi) with no Z dependence | R0 direct geometry and PPN geometry residuals |
| DQZ3634_1_source_readout | partial_Z M_obs | zero only if source mass, GM calibration, Hamiltonian normalization, and orbit readouts descend through q | retained Dsource_readout leak row and 3629 source-coupling obstruction | OPEN_HIGHEST_PRESSURE_COMPONENT | derive source/readout descent or compute nonzero source leakage | J_X, R1 WEP source charge, R10/R11 source normalization, orbital/clock leakage |
| DQZ3634_2_clock_marker | partial_Z Theta_obs | zero if clocks/constants/material markers are fixed standards or q-owned | retained Dtheta_marker leak row | OPEN | explicit clock and marker map independent of Z | clock redshift, constants/material marker, EM/fine-structure style channels |
| DQZ3634_3_boundary_projector | partial_Z B_obs | zero/exact/proper if boundary class and Pi_M are q-owned | 3632 boundary charge owner missing; boundary_projector_Dq_leak retained | OPEN | boundary charge and projector silence on local collar | preferred-frame alpha3/xi, memory flux, source normalization edge rows |
| DQZ3634_4_verdict | Dq_Z_norm | exact norm formula exists and prevents cancellations | component zeros are not signed, especially source/readout | FORMULA_FILLED_BUT_NOT_THEOREM_ZERO | prove all four components zero or score first nonzero component | source/readout descent or J_X residual row is the next attack |

## Filled DqZ row

| row_id | symbol | value_or_formula | units | zero_condition | fill_level | score_status | next_measurement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DQL3634_0_Dq_Z_filled_formula | Dq_Z_norm | sqrt(w_G\|\|partial_Z G_obs\|\|^2 + w_M\|\|partial_Z M_obs\|\|^2 + w_T\|\|partial_Z Theta_obs\|\|^2 + w_B\|\|partial_Z B_obs\|\|^2) | dimensionless after component normalization | partial_Z G_obs=partial_Z M_obs=partial_Z Theta_obs=partial_Z B_obs=0 | symbolic_formula_filled_not_numeric_not_claim | not_scoreable_until_component_zeros_or_bounds | source/readout component partial_Z M_obs is highest pressure |

## Branch split

| branch_id_local | condition | result | current_status | next_test |
| --- | --- | --- | --- | --- |
| BR3634_A_strict_quotient | all four component derivatives vanish and boundary charge is zero/exact/proper | Z is absent quotient fibre; J_Z/J_X=0; no X/Z pole; R10 X-sector silent | BEST_ROUTE_NOT_SIGNED | prove partial_Z M_obs=0 after geometry candidate is written |
| BR3634_B_source_leak | geometry component may vanish but source/readout or marker component is nonzero/unsigned | coupling is physical or closure-assumed; open J_X and source-charge residual rows | MOST_LIKELY_LIVE_BOTTLENECK | derive source/readout descent or fill J_X with units/projection |
| BR3634_C_boundary_leak | bulk components vanish but boundary/projector component survives | bulk no-pole theorem is not enough; preferred-frame/source normalization edge channels remain | BOUNDARY_RISK_OPEN | prove Q_boundary[partial_Z]=0/exact/proper or score boundary_flux_X |
| BR3634_D_physical_XZ | Z/X is retained as a physical local mode | must score Z_X, M_X^2, K_X, qbar_XT, Qbar_XH, lambda_X, J_X | FALLBACK_EMPIRICAL_BRANCH | do not claim GR reduction; run residual coefficient acquisition |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3634_0_formula_filled | Dq_Z_norm is no longer just a missing placeholder; it has an exact positive component norm with a no-cancellation lemma. | SYMBOLIC_ROW_FILLED | evaluate the four component derivatives instead of repeating broad q-owner audits |
| DEC3634_1_coupling_focus | The source/readout component partial_Z M_obs is the highest-pressure coupling target because geometry-only verticality cannot kill source charges. | SOURCE_READOUT_NEXT | attempt source/readout descent theorem or open J_X row |
| DEC3634_2_claim_ceiling | No local-GR or R10 pass is promoted because component zeros are not signed. | NO_CLAIM | keep strict quotient as route A and residual coefficient scoring as route B |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3635-Y5-R2FR-source-readout-descent-zero-or-JX-residual-row.md | scripts/Y5_R2FR_3635_source_readout_descent_zero_or_JX_residual_row.py | try to prove partial_Z M_obs=0 for source mass, GM calibration, Hamiltonian normalization, and orbit/readout maps; if not, create the first J_X/source-charge residual row with units/projection requirements | either source/readout descent is theorem-zero from q, or a nonclaim J_X/Dsource_readout row is executable enough to drive R1/R10/R11 comparisons later |
