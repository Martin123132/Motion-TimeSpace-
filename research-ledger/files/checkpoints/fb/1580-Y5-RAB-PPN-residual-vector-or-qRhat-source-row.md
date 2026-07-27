# 1580 - R_AB PPN Residual Vector Or qRhat Source Row

## Verdict
- A conditional PPN bridge is now derived: with `R_AB=ln(A B)` and PPN-compatible weak-field variables, `R_AB=2(gamma-1)U_N+O(U_N^2)`.
- This defines the useful local hair variable `q_R_hat:=R_AB^(1)/(2U_N)`, so `gamma_minus_1=q_R_hat+tails` at leading order.
- If the exterior current-hair branch is retained, `W R_AB'=Q_R` with `W~r^2` gives the bound target `q_R_hat~sigma_Q Q_R/(2GM)`.
- Cassini therefore becomes a real bound contract on `q_R_hat` or `Q_R/(2GM)`, not a pass, because the value, gauge/source denominator, and tails are missing.
- No Cassini, PPN, local GR/Newton, no-charge, beta, conservation, R10, WEP, clock, or orbital claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1580_0_1579_doc | 1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md | True | True | NEXT_1580_RAB_PPN_RESIDUAL_VECTOR_OR_QRHAT_SOURCE_ROW; gamma_minus_1=C_QR q_R_hat+tails |
| SRC1580_1_1579_validation | source-intake/mts_residuals/P8_Y5_BRR545_1579_VALIDATION.csv | True | True | VAL1579_OVERALL; PASS |
| SRC1580_2_1579_acquisition | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1579_COMPONENT_SOURCE_ACQUISITION_LEDGER.csv | True | True | ACQ1579_8_tau_PPN; MISSING_PPN_PROJECTION |
| SRC1580_3_1579_external | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv | True | True | EXT1579_1_PPN; upper_bound=2.3e-05 dimensionless |
| SRC1580_4_1579_dry_run | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1579_COMPARATOR_DRY_RUN.csv | True | True | DRY1579_1_PPN; INTERNAL_PROJECTION_MISSING |
| SRC1580_5_05_reciprocity | 05-reciprocity-theorem-attempt.md | True | True | R_AB = ln(A B) = ln(T^2 S).; W R_AB' = Q_R. |
| SRC1580_6_10_observer | 10-observer-map-symplectic-contract.md | True | True | R_AB = ln(T^2 S) = 2 ln(J_q).; gamma - 1 = 0 after R_AB=0. |
| SRC1580_7_1577_doc | 1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md | True | True | W_R partial_r R_AB=Q_R; FINITE_COMPONENT_BOUND_FILL_STARTED_NONCLAIM |
| SRC1580_8_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | True | Cassini_Shapiro_gamma_2003; gamma_minus_1; 2.3e-05 |

## PPN Bridge Derivation

| bridge_id | object | equation | status | blocking_gap |
| --- | --- | --- | --- | --- |
| PPNB1580_0_observer_identity | observer reciprocal strain | R_AB=ln(A B)=ln(T^2 S) | FORMAL_INPUT | requires PPN-compatible identification of A=T^2 and B=S in the same weak-field radial gauge |
| PPNB1580_1_ppn_expansion | weak-field PPN metric | A=1-2 U_N+O(U_N^2), B=1+2 gamma U_N+O(U_N^2) | FORMAL_COMPARATOR_GRAMMAR | does not import Einstein equations; it defines the observable gamma channel |
| PPNB1580_2_linear_bridge | linearized reciprocal strain | R_AB=ln[(1-2 U_N)(1+2 gamma U_N)]=2(gamma-1)U_N+O(U_N^2) | DERIVED_CONDITIONAL_BRIDGE | valid only after gauge/source denominator and observer-map matching are fixed |
| PPNB1580_3_qRhat_definition | dimensionless local hair | q_R_hat:=R_AB^(1)/(2 U_N) | FORMAL_DEFINITION_VALUE_MISSING | numeric q_R_hat remains missing because R_AB profile/source charge is not derived |
| PPNB1580_4_residual_vector | PPN gamma residual | gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+O(U_N) | FORMAL_NONCLAIM_VECTOR_READY | tails must be zero-proved or absolutely bounded before Cassini scoring |
| PPNB1580_5_current_hair_projection | exterior reciprocal hair if current branch is retained | W~r^2 and W R_AB'=Q_R imply R_AB~sigma_Q Q_R/r, so q_R_hat~sigma_Q Q_R/(2 G M) | CONDITIONAL_BOUND_TARGET | sign convention, W normalization, M/source denominator, and tails remain unsourced |

## q_R_hat Source Row

| row_id | symbol | definition | units | value | current_status | why_not_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QRHAT1580_0_definition | q_R_hat | q_R_hat:=R_AB^(1)/(2 U_N) in a PPN-compatible weak-field observer gauge | dimensionless |  | FORMAL_DEFINITION_DERIVED_VALUE_MISSING | R_AB profile, Q_R/source denominator, gauge matching, and boundary/source tails are not sourced |
| QRHAT1580_1_current_hair_target | Q_R/(2GM) | if W~r^2 and R_AB~sigma_Q Q_R/r, then q_R_hat~sigma_Q Q_R/(2GM) | dimensionless after source-mass normalization |  | CONDITIONAL_BOUND_TARGET_VALUE_MISSING | Q_R, W normalization, source mass convention, and tail envelope are missing |

## Cassini Bound Contract

| contract_id | observable | external_upper_bound | mts_bound_expression | conditional_QR_expression | current_status |
| --- | --- | --- | --- | --- | --- |
| CAS1580_0_gamma_bound | gamma_minus_1 | 2.3e-05 | abs(q_R_hat+delta_gauge+delta_source+delta_boundary) <= external_upper_bound at leading PPN order | abs(sigma_Q Q_R/(2GM)+tails) <= external_upper_bound if W~r^2 and R_AB~sigma_Q Q_R/r | BOUND_CONTRACT_ONLY_NO_MTS_VALUE |

## PPN Dry Run

| dry_run_id | arena | external_bound | required_missing_inputs | dry_run_status | blocker |
| --- | --- | --- | --- | --- | --- |
| PPNDRY1580_0_Cassini | PPN/Cassini gamma | 2.3e-05 | q_R_hat numeric or Q_R/(2GM); delta_gauge; delta_source; delta_boundary; PPN gauge/source denominator | NOT_RUN_BLOCKED | FORMAL_BRIDGE_READY_BUT_QRHAT_VALUE_MISSING |
| PPNDRY1580_1_GR_limit | local GR reduction | gamma_minus_1=0 target | Q_R=0 theorem or q_R_hat=0 theorem; beta-1=0; conservation/Bianchi identity; common matter coframe | NOT_RUN_BLOCKED | GAMMA_BRIDGE_ALONE_NOT_FULL_GR_REDUCTION |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1580_0_bridge | R_AB to gamma_minus_1 formal bridge exists | PASS_FORMAL_NONCLAIM | linear PPN expansion gives R_AB=2(gamma-1)U_N conditionally |
| GATE1580_1_qRhat_value | q_R_hat numeric/theorem-zero row exists | BLOCKED_NO_CLAIM | q_R_hat and Q_R/(2GM) remain value-missing |
| GATE1580_2_Cassini_score | Cassini PPN comparison can be scored | BLOCKED_NO_CLAIM | tails, gauge/source denominator and q_R_hat are missing |
| GATE1580_3_local_GR | derived local GR/Newton reduction | BLOCKED_NO_CLAIM | gamma bridge does not prove Q_R=0, beta=1, conservation or common matter coupling |
| GATE1580_4_finite_branch | finite R_AB branch passes local tests | BLOCKED_NO_CLAIM | only a bound contract exists; no prediction is made |

## Decision

| decision_id | decision | reason | consequence |
| --- | --- | --- | --- |
| DEC1580_0_progress | PPN_BRIDGE_DERIVED_CONDITIONALLY | R_AB=ln(AB) gives gamma_minus_1=R_AB/(2U_N)+tails at leading PPN order | the PPN/local-GR test now has a real MTS-facing residual variable q_R_hat |
| DEC1580_1_claim_ceiling | NO_CASSINI_OR_GR_CLAIM | q_R_hat/Q_R, gauge/source denominator, and boundary/source tails are missing | Cassini becomes a bound contract, not a pass/fail result |
| DEC1580_2_next | NEXT_1581_RAB_QRHAT_PROFILE_AND_CASSINI_BOUND_ROW_OR_NO_CHARGE_RETURN | the next step is to use W R_AB'=Q_R and W~r^2 to either bound Q_R/(2GM) or return to a parent no-charge theorem | derive/source the radial hair amplitude before scoring Cassini |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1580_0_sources_exist | PASS | all cited source paths exist |
| VAL1580_1_needles_found | PASS | all source needles found |
| VAL1580_2_bridge_formula | PASS | linear PPN bridge R_AB=2(gamma-1)U_N is recorded |
| VAL1580_3_qrhat_definition_nonclaim | PASS | q_R_hat formal definition exists but remains value-missing |
| VAL1580_4_cassini_contract_only | PASS | Cassini row is a bound contract only |
| VAL1580_5_ppn_dry_run_blocked | PASS | PPN dry-run rows block scoring |
| VAL1580_6_claim_gates_closed | PASS | claim gates remain nonclaim even when formal bridge passes |
| VAL1580_7_decision_next | PASS | decision selects q_R_hat profile and Cassini bound target |
| VAL1580_8_csv_parse | PASS | all generated 1580 CSVs parse cleanly |
| VAL1580_9_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1580_10_no_raw_accepted | PASS | no 1580 rows written to raw/accepted finite directories |
| VAL1580_11_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1580_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1580_13_formalization_untouched | PASS | all generated 1580 paths are outside formalization-workbench; git status is clean when available |
| VAL1580_OVERALL | PASS | 1580 PPN residual vector/q_Rhat source-row validation |

## Next Target

| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md | scripts/Y5_RAB_qRhat_profile_and_Cassini_bound_row_or_no_charge_return.py | derive the radial q_R_hat profile from W R_AB'=Q_R and W~r^2, then write a Cassini bound row for Q_R/(2GM) or return to the no-charge theorem route | do not claim Cassini pass or local GR unless Q_R=0/q_R_hat=0 and all PPN tails/gauge/source denominators are parent-signed |
