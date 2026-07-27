# 3590 - GK outer work absorption or finite branch failure

## Verdict
3590 derives the lawful absorbed finite branch.  If

`X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2`,

then `eta_GK < 1` gives

`X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]`.

The current corpus does not sign `eta_GK < 1` and does not supply noncircular `F0_GK_abs`, so the branch is retained as an explicit residual parameter rather than refilled again as if it were score-ready.

## Absorption theorem
- `ABS3590_0_starting_inequality`: DERIVED_ABSORPTION_FORM - X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2
- `ABS3590_1_absorption_condition`: EXACT_NECESSARY_FOR_THIS_BRANCH - 0 <= eta_GK < 1
- `ABS3590_2_absorbed_bound`: DERIVED_EXACT_QUADRATIC_ROOT - X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]
- `ABS3590_3_zero_fixed_work_limit`: DERIVED_LIMIT_CASE - if F0_GK_abs=0 and eta_GK<1 then X_GK <= a_GK/(1-eta_GK)
- `ABS3590_4_failure_condition`: PASS_GUARD - if eta_GK>=1 or eta_GK is unsigned, the finite branch cannot be score-ready

## Eta budget
- `ETA3590_0_eta_cross` `eta_cross_GK`: FORMULA_DERIVED_VALUES_MISSING - max(0, |c_AG|C_cross - min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2))/N_GK
- `ETA3590_1_eta_projector` `eta_projector_GK`: MISSING_PROJECTOR_DESCENT_BOUND - operator norm of field-dependent or noncommuting projector stress/leakage divided by X_GK^2
- `ETA3590_2_eta_boundary_feedback` `eta_boundary_feedback_GK`: MISSING_BOUNDARY_FEEDBACK_BOUND - quadratic part of boundary/symplectic feedback after fixed Phi_boundary_GK is removed
- `ETA3590_3_eta_metric_response` `eta_metric_response_GK`: MISSING_ARENA_PROJECTION_BOUND - metric-response/observable backreaction coefficient from GK stress to the same X_GK norm
- `ETA3590_4_eta_sum` `eta_GK`: SUM_FORMULA_READY_VALUES_MISSING - eta_cross_GK + eta_projector_GK + eta_boundary_feedback_GK + eta_metric_response_GK
- `ETA3590_5_eta_gate` `eta_GK<1`: NOT_PARENT_SIGNED_CURRENT_CORPUS - parent-signed strict smallness of the total quadratic defect

## Outer work pack
- `FOUT3590_0_F_source_tail` `F_source_tail_GK_abs`: MISSING_FIXED_SOURCE_TAIL_VALUE_OR_ZERO - fixed source-support/current tail independent of X_GK after J_GK_norm is split into the linear term
- `FOUT3590_1_F_boundary_fixed` `F_boundary_fixed_GK_abs`: MISSING_FIXED_BOUNDARY_VALUE_OR_ZERO - fixed boundary/reference/symplectic work independent of X_GK after Phi_boundary_GK is split into the trace-linear term
- `FOUT3590_2_F_topology_fixed` `F_topology_fixed_GK_abs`: MISSING_TOPOLOGY_ZERO_OR_FINITE_VALUE - fixed topological/harmonic charge not controlled by local GK amplitude
- `FOUT3590_3_F_geometry_background` `F_geometry_background_GK_abs`: MISSING_ESTAT_BACKGROUND_VALUE_OR_ZERO - fixed stationary-domain/E_stat background leakage not proportional to u_GK
- `FOUT3590_4_F0_sum` `F0_GK_abs`: SUM_FORMULA_READY_VALUES_MISSING - F_source_tail_GK_abs + F_boundary_fixed_GK_abs + F_topology_fixed_GK_abs + F_geometry_background_GK_abs

## Branch verdict
- `BV3590_0_absorbed_formula` `epsilon_GK_hair_absorbed`: AVAILABLE_CONDITIONAL_FORMULA - K_GK*[a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]
- `BV3590_1_current_eta_result` `eta_GK`: FAIL_CURRENT_SCORE - eta_GK<1 is not parent-signed; eta_cross has a formal expression but missing coefficients, while projector/boundary/metric feedback bounds are absent
- `BV3590_2_current_F0_result` `F0_GK_abs`: FAIL_CURRENT_SCORE - no source-backed noncircular fixed outer-work value exists in the current corpus
- `BV3590_3_demoted_residual_parameter` `X_GK_residual`: STRUCTURAL_NON_SCORE_READY_RESIDUAL - retain X_GK_residual as an explicit local-GR residual parameter rather than recycling the input-pack search
- `BV3590_4_local_claim_policy` `local_GR_R10_PPN_claim`: CLAIM_BLOCKED - blocked until eta_GK<1 or F0/K/source-boundary-topology rows are parent-signed and numeric/sourced

## Gates
- `GATE3590_0_sources`: PASS (all source paths and selected anchors exist)
- `GATE3590_1_absorption_theorem`: PASS_DERIVED (exact eta absorption bound is derived from the quadratic inequality)
- `GATE3590_2_no_lambda`: PASS_GUARD (absorbed finite branch still does not use lambda_GK denominator)
- `GATE3590_3_eta_less_than_one`: FAIL_CURRENT_SCORE (eta_GK<1 is not parent-signed)
- `GATE3590_4_F0_noncircular`: FAIL_CURRENT_SCORE (F0_GK_abs has no source-backed noncircular fixed value)
- `GATE3590_5_demote_residual`: PASS_GUARD (GK finite branch is retained as explicit residual parameter instead of endlessly refilled)
- `GATE3590_6_local_GR`: FAIL_CURRENT_CLAIM (source coupling/Newton/PPN/local-GR closure remains blocked)

## Status
- `ABSORPTION_THEOREM_DERIVED_GK_BRANCH_DEMOTED_TO_EXPLICIT_RESIDUAL`: 3590 derives the exact absorption law for the finite GK branch: from X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2, eta_GK<1 gives X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]. This is the lawful replacement for smuggling epsilon_cross_hair_GK into F_outer.
- Decision: current corpus does not sign eta_GK<1 or provide noncircular F0_GK_abs, so GK finite hair is retained as an explicit residual parameter and not repeatedly refilled as if score-ready
- Still missing: parent-signed eta_cross/eta_projector/eta_boundary/eta_metric bounds; noncircular fixed F0_GK_abs components; K_GK observable map; units/domain lock; source coupling/Newton/PPN closure

## Validation
- `VAL3590_0_sources_exist`: PASS (all required 3590 source paths exist)
- `VAL3590_1_required_needles_found`: PASS (all selected 3590 anchors found)
- `VAL3590_2_outputs_exist`: PASS (all pre-validation 3590 output files written)
- `VAL3590_3_csv_parse`: PASS (source_register:18; absorption_theorem:5; eta_budget:6; outer_work_pack:5; branch_verdict:5; activation_gates:7; status:1; next_target:1; canonical_status:1)
- `VAL3590_4_absorption_formula_present`: PASS (absorbed eta bound is present)
- `VAL3590_5_eta_budget_complete`: PASS (all eta budget rows are present)
- `VAL3590_6_F0_pack_complete`: PASS (all noncircular F0 slots are present)
- `VAL3590_7_no_lambda_denominator`: PASS (absorption theorem does not use lambda_GK)
- `VAL3590_8_eta_not_signed`: PASS (eta_GK<1 remains explicitly unsigned)
- `VAL3590_9_branch_demoted`: PASS (GK branch demoted to explicit residual parameter)
- `VAL3590_10_score_blocked`: PASS (score remains blocked by eta and F0 gates)
- `VAL3590_11_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3590_12_next_target_selected`: PASS (3591 source-coupling target selected)
- `VAL3590_13_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3590_14_formalization_workbench_untouched`: PASS (no 3590 checkpoint output appears in formalization-workbench)

## Next target
- `NEXT3590_0` -> `3591-Y5-R2FR-source-coupling-GM-calibration-or-residual-contract.md`
- Objective: pivot from GK finite-hair refill to source coupling: derive the parent Hilbert/Noether charge to Newtonian GM transfer, or write the explicit residual contract that carries unclosed GK/local hair into PPN/Newton tests
