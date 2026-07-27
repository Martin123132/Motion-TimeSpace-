# 2744 - Y5 R2/f(R): Local Closure PPN Benchmark Derived-vs-Assumed Ledger Under AX1090

Status: `Y5_R2FR_2744_local_closure_ppn_benchmark_nonclaim_deviation_budget_next`

## Private Verdict

2744 stops the local branch from cheating and also keeps its strongest useful result.

Under the explicit closure

`T^2=1-L`, `R_AB=ln(T^2 S)=0`, `Q_R=0`,

we get

`S=1/T^2=1/(1-L)`, `p=1`, and `gamma=1`.

That is the clean local GR control lane. It is useful because it gives a benchmark against which deviations can be tested. It is not a parent derivation because `R_AB=0`, `Q_R=0`, beta completion, conservation, source normalization, and matter universality remain unproved by the parent theory.

So the next move is no longer verbal derivation. It is a sensitivity/bound budget: if residual reciprocal hair or coupling drift survives, how large can it be before R10/PPN/clocks/orbits kill it?

## Source Register

| source_id | description | source_path | exists | needles_present | missing_needles | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2744_0_2743_doc | 2743 demotes zero-charge route to explicit closure benchmark and selects this PPN ledger. | 2743-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-or-closure-demotion-under-AX1090.md | True | True |  | False |
| SRC2744_1_2743_validation | 2743 validation output. | source-intake/mts_residuals/P8_Y5_BRR545_2743_VALIDATION.csv | True | True |  | False |
| SRC2744_2_1556_doc | prior local closure PPN benchmark and ledger. | 1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md | True | True |  | False |
| SRC2744_3_13_local_closure | local closure PPN source text. | 13-local-closure-PPN-benchmark.md | True | True |  | False |
| SRC2744_4_10_observer_contract | observer-map contract for gamma/beta/conservation warning. | 10-observer-map-symplectic-contract.md | True | True |  | False |
| SRC2744_5_1556_derived_csv | machine-readable prior derived-vs-assumed ledger. | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv | True | True |  | False |
| SRC2744_6_1556_ppn_csv | machine-readable prior PPN benchmark requirements. | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv | True | True |  | False |
| SRC2744_7_1556_controls_csv | machine-readable closure control values. | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv | True | True |  | False |
| SRC2744_8_2743_queue | live acquisition queue into this checkpoint. | source-intake/rab-sector/acquisition-queue/JR2743_LOCAL_CLOSURE_PPN_BENCHMARK_NEXT.csv | True | True |  | False |

## Closure Assumption Ledger

| assumption_id | statement | classification | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| ASM2744_0_clock_load | T^2=1-L | assumed_or_prior_local_clock_load | Newtonian clock/load side is used as weak-field scaffold | False |
| ASM2744_1_reciprocity | R_AB=ln(T^2 S)=0 | explicit_closure_assumption | not parent-derived after phase-volume and zero-charge audits | False |
| ASM2744_2_spatial_routing | S=1/T^2=1/(1-L) | derived_inside_closure | follows algebraically from ASM2744_0 and ASM2744_1 | False |
| ASM2744_3_reciprocal_charge | Q_R=0 | explicit_closure_assumption | zero-charge theorem failed; kept as closure only | False |
| ASM2744_4_areal_radius | angular sector=r^2 dOmega^2 | benchmark_coordinate_condition | defines the local control lane but must not be used to derive AB=1 | False |
| ASM2744_5_matter_universality | all matter uses same observer coframe | test_required_not_derived_here | needed for WEP/clocks/PPN interpretation | False |
| ASM2744_6_claim_policy | closure is not derivation | guard | benchmark may test deviations but cannot prove parent theory | False |

## Derived vs Assumed Ledger

| ledger_id | quantity | status | basis | limitation | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DVA2744_0_p_equals_1 | p=1 | DERIVED_WITHIN_CLOSURE | from T^2=1-L and R_AB=0 | not parent-derived | False |
| DVA2744_1_gamma | gamma=1 | DERIVED_WITHIN_CLOSURE | spatial curvature lane p=1 gives gamma=1 | only under closure | False |
| DVA2744_2_beta | beta=1 | BENCHMARK_CONTROL_VALUE | accepted in the Schwarzschild-equivalent control lane | not derived by MTS parent action | False |
| DVA2744_3_Newton | Newtonian acceleration | TEST_REQUIRED | T^2 weak-field term must produce correct slow-particle acceleration | requires source normalization/Poisson bridge | False |
| DVA2744_4_conservation | Bianchi-like consistency | TEST_REQUIRED | field equations must imply conservation identity | not supplied by closure | False |
| DVA2744_5_matter | universal matter coupling | TEST_REQUIRED | same coframe for clocks, matter, photons, and orbital readouts | not supplied by closure | False |
| DVA2744_6_source_norm | measured GM/source normalization | TEST_REQUIRED | same source charge must feed Poisson/orbit/PPN | not supplied by closure | False |
| DVA2744_7_tracefree | tracefree metric transfer | BLOCKED_OUTSIDE_SCALAR_CLOSURE | scalar reciprocity does not fix tracefree tensor map | requires separate metric/coframe definition | False |
| DVA2744_8_parent_origin | R_AB=0 parent derivation | BLOCKED_NOT_DERIVED | gauge/Noether/phase-volume attempts failed | future first-class constraint only | False |

## PPN Benchmark Requirements

| ppn_id | observable | closure_value_or_condition | benchmark_status | remaining_requirement | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PPN2744_0_gamma | gamma_minus_1 | 0 under R_AB=0 closure | closure_control | Cassini/local bound can test deviations, not derivation | False |
| PPN2744_1_beta | beta_minus_1 | 0 in exact Schwarzschild-equivalent control lane | benchmark_control_not_parent_derived | second-order weak-field source closure still required | False |
| PPN2744_2_alpha1 | alpha1 | 0 only if no preferred-frame/shadow-frame residuals | test_required | frame/coframe descent not proven by closure | False |
| PPN2744_3_alpha2 | alpha2 | 0 only if no spin/preferred-frame residuals | test_required | not handled by scalar R_AB closure | False |
| PPN2744_4_alpha3_xi | alpha3,xi | 0 only if boundary/source fluxes vanish | test_required | boundary/no-charge/source-normalization gates remain open | False |
| PPN2744_5_Gdot | Gdot/G | 0 only if source normalization is time-stationary | test_required | measured-GM/source-normalization theorem missing | False |
| PPN2744_6_R10 | alpha(lambda) | 0 only if no finite-range q/source hair survives | test_required | closure says nothing about all retained residual sectors | False |
| PPN2744_7_WEP_clock | eta,delta ln nu | 0 only with universal matter/coframe coupling | test_required | matter universality not derived by closure | False |

## Observable Control Values

| observable_id | observable | control_value | units | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| OBS2744_0_gps | GPS satellite-minus-ground | 38.60879935757566 | microseconds/day | GR_CONTROL_UNDER_CLOSURE | False |
| OBS2744_1_light_bending | solar limb light bending | 1.7512432813682448 | arcsec | GR_CONTROL_UNDER_CLOSURE | False |
| OBS2744_2_shapiro | solar Shapiro scale | 119.4750358485562 | microseconds | GR_CONTROL_UNDER_CLOSURE | False |
| OBS2744_3_mercury | Mercury perihelion | 42.98201260912118 | arcsec/century | GR_CONTROL_UNDER_CLOSURE | False |
| OBS2744_4_gamma | gamma | 1 | dimensionless | CLOSURE_CONTROL | False |
| OBS2744_5_beta | beta | 1 | dimensionless | CLOSURE_CONTROL | False |

## Closure Benchmark Runner

| runner_id | check | current_status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| RUN2744_0_assumptions | closure assumptions explicit | PASS_NONCLAIM | R_AB=0 and Q_R=0 are labelled closure assumptions | False |
| RUN2744_1_gamma | gamma control | PASS_CLOSURE_CONTROL | gamma=1 follows inside closure | False |
| RUN2744_2_beta | beta control | PASS_BENCHMARK_NOT_DERIVATION | beta=1 is a GR-control value, not parent-derived | False |
| RUN2744_3_conservation | Bianchi/conservation | REFUSED_MISSING_PARENT_IDENTITY | closure does not supply field equations | False |
| RUN2744_4_matter | matter universality | REFUSED_MISSING_MATTER_DESCENT | closure does not prove universal coupling | False |
| RUN2744_5_source | Newton/source normalization | REFUSED_MISSING_SOURCE_BRIDGE | closure does not prove Poisson/Gauss/orbital GM bridge | False |
| RUN2744_6_score_status | derived local GR/Newton claim | REFUSED_NOT_DERIVED | closure benchmark is not derivation | False |

## Decision Ledger

| decision_id | decision | result | rationale | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2744_0_result | The R_AB=0 closure benchmark is cleanly separated from derivation. | CLOSURE_CONTROL_LEDGER_WRITTEN | gamma/beta controls are useful but nonclaim | False |
| DEC2744_1_missing | The missing gates are conservation, matter universality, source normalization, and deviation coefficients. | TEST_REQUIRED_GATES_REMAIN | these decide whether closure can become a credible local branch | False |
| DEC2744_2_next | Next target is closure-deviation PPN sensitivity. | NEXT_2745_DEVIATION_SENSITIVITY | quantify q_R, beta drift, matter drift, source-normalization residuals, and residual R_AB hair against local bounds | False |
| DEC2744_3_strategy | Stop trying to declare local GR derived before the residual budget exists. | TEST_FIRST_DISCIPLINE | this is the route that gets us toward real constraints instead of more verbal closure | False |

## Claim Gates

| claim_gate_id | claim | gate_passed | status | claim_allowed | valid_for_claim | reason |
| --- | --- | --- | --- | --- | --- | --- |
| GATE2744_0_assumption_ledger | closure assumption ledger | True | PASS_NONCLAIM | False | False | assumed vs derived is explicit |
| GATE2744_1_ppn_benchmark | PPN benchmark ledger | True | PASS_NONCLAIM | False | False | control values and remaining gates are written |
| GATE2744_2_gamma_control | gamma=1 under closure | True | PASS_CLOSURE_CONTROL | False | False | not a parent derivation |
| GATE2744_3_beta_control | beta=1 under closure | True | PASS_BENCHMARK_NOT_DERIVATION | False | False | second-order source closure remains required |
| GATE2744_4_parent_origin | R_AB=0 parent origin | False | BLOCKED | False | False | 2743 rejected current derivation routes |
| GATE2744_5_universality_conservation | matter universality and conservation | False | BLOCKED | False | False | closure does not supply field equations or matter descent |
| GATE2744_6_GR_Newton | derived GR/Newton limit | False | BLOCKED_NO_CLAIM | False | False | benchmark is not derivation |

## Next Target

| next_id | status | target_doc | target_script | mission | acceptance | forbidden | selected | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2744_0_2745 | selected_primary | 2745-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget-under-AX1090.md | scripts/Y5_R2FR_closure_deviation_PPN_sensitivity_and_bound_budget_under_AX1090_2745.py | turn the closure benchmark into a deviation budget for q_R, beta drift, matter-universality drift, source-normalization drift, and residual R_AB hair against local bounds | write nonclaim sensitivity rows and identify which coefficients need source-backed values before R10/PPN/clock/orbital testing | do not call closure deviations predictions without sourced coefficients; do not claim local GR derivation; do not edit formalization-workbench | True | False |

## Branch Copies

| copy_id | source_table | copy_path | purpose | exists | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR2744_0_derived | source-intake/mts_residuals/P8_Y5_R2FR_2744_DERIVED_VS_ASSUMED_LEDGER.csv | source-intake/source-weight/local_closure_derived_vs_assumed_2744_NONCLAIM.csv | source-weight derived-vs-assumed local closure ledger | True | False |
| BR2744_1_ppn | source-intake/mts_residuals/P8_Y5_R2FR_2744_PPN_BENCHMARK_REQUIREMENTS.csv | source-intake/local_bounds/local_closure_ppn_benchmark_2744_NONCLAIM.csv | local-bound PPN benchmark requirements | True | False |
| BR2744_2_next_queue | source-intake/mts_residuals/P8_Y5_R2FR_2744_NEXT_TARGET.csv | source-intake/rab-sector/acquisition-queue/JR2744_CLOSURE_DEVIATION_PPN_SENSITIVITY_NEXT.csv | RAB acquisition queue for closure-deviation PPN sensitivity | True | False |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL2744_0_sources | True | all source paths exist and required anchors/needles are present | 2026-06-23T14:16:18.677389+00:00 |
| VAL2744_1_assumptions | True | R_AB=0 and Q_R=0 are explicitly labelled closure assumptions | 2026-06-23T14:16:18.677402+00:00 |
| VAL2744_2_derived_vs_assumed | True | gamma is closure-derived while parent origin remains blocked | 2026-06-23T14:16:18.677406+00:00 |
| VAL2744_3_ppn_requirements | True | PPN/Newton/local requirements ledger written | 2026-06-23T14:16:18.677409+00:00 |
| VAL2744_4_observable_controls | True | observable control values recorded | 2026-06-23T14:16:18.677413+00:00 |
| VAL2744_5_runner_refuses_derivation | True | runner refuses derived local GR claim | 2026-06-23T14:16:18.677416+00:00 |
| VAL2744_6_claim_gates | True | claim gates keep all prediction/claim flags false | 2026-06-23T14:16:18.677419+00:00 |
| VAL2744_7_next_target | True | next target is closure-deviation PPN sensitivity and bound budget | 2026-06-23T14:16:18.677422+00:00 |
| VAL2744_8_branch_outputs | True | branch copies exist | 2026-06-23T14:16:18.677425+00:00 |
| VAL2744_9_csv_parse | True | P8_Y5_R2FR_2744_SOURCE_REGISTER.csv:9:ok; P8_Y5_R2FR_2744_CLOSURE_ASSUMPTION_LEDGER.csv:7:ok; local_closure_derived_vs_assumed_2744_NONCLAIM.csv:9:ok; local_closure_ppn_benchmark_2744_NONCLAIM.csv:8:ok; P8_Y5_R2FR_2744_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv:6:ok; P8_Y5_R2FR_2744_CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv:7:ok; P8_Y5_R2FR_2744_DECISION_LEDGER.csv:4:ok; P8_Y5_R2FR_2744_CLAIM_GATES.csv:7:ok; P8_Y5_R2FR_2744_NEXT_TARGET.csv:1:ok; P8_Y5_R2FR_2744_BRANCH_COPIES.csv:3:ok; JR2744_CLOSURE_DEVIATION_PPN_SENSITIVITY_NEXT.csv:1:ok | 2026-06-23T14:16:18.677430+00:00 |
| VAL2744_10_pycache_absent | True | scripts __pycache__ absent=True | 2026-06-23T14:16:18.677440+00:00 |
| VAL2744_11_formalization_untouched | True | formalization-workbench recent modified-file count since script start = 0 | 2026-06-23T14:16:18.677443+00:00 |
| VAL2744_OVERALL | True | 2744 formalizes the R_AB=0 closure benchmark, separates derived/assumed/test-required local conditions, and selects closure-deviation sensitivity next | 2026-06-23T14:16:18.677450+00:00 |

## Plain-English Read

This is a good place to be, because now the argument is honest enough to test. We have a closure lane that lands on the GR control values, but we are not pretending it is derived. The next round is where the gloves come back on: quantify the allowed deviation budget and see whether the remaining hair/coupling terms can survive real local bounds.
