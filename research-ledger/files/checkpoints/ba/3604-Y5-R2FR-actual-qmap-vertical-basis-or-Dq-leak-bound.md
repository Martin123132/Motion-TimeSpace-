# 3604 - actual qmap vertical basis or Dq leak bound

## Verdict
3604 turns `Dq(v_X)=0` from a slogan into a matrix gate.  A direction is vertical only when every q-component derivative vanishes on the same parent q-map and branch.

No candidate direction passes that gate yet.  `v_q` is the best first attack, `v_memory_tau`, `v_coeff`, and `v_boundary` are conditional, `delta_projector` is an obstruction rather than a vertical direction, and `v_RAB` is rejected under the current observer-cell map.

The useful nonzero law is now `epsilon_Dq[v] := ||Dq[v]||_q/||v|| <= sum_a epsilon_a[v]`.  This is the row that feeds the 3603 `A_X` bound instead of pretending verticality is already proven.

## Qmap Vertical Theorem Gate
- `DQV3604_0_target`: TARGET_IMPORTED - Construct the actual q-map/Dq matrix and certify which residual directions are vertical; otherwise retain Dq leak bounds direction by direction.
- `DQV3604_1_vertical_criterion`: EXACT_MATRIX_CRITERION - For q=(q_geom,q_tau,q_matter,q_boundary,q_coeff,q_projector,readout), a direction v is vertical iff every listed Dq_a[v] is zero on the same branch.
- `DQV3604_2_norm_bound_law`: EXACT_BOUND_LAW_NONCLAIM - epsilon_Dq[v] := ||Dq[v]||_q/||v|| <= sum_a epsilon_a[v] using a declared q-component norm; zero requires every component epsilon_a[v]=0.
- `DQV3604_3_vq_candidate`: CANDIDATE_HIGHEST_PRIORITY_NOT_CERTIFIED - v_q can be vertical only if q_private is first-class or source-silent across geometry, tau, matter, boundary and readout q-components.
- `DQV3604_4_memory_tau_candidate`: CANDIDATE_NOT_CERTIFIED - Private memory/time/coframe directions can be vertical only if the public tau/coframe/readout functor is fixed before clocks, source support, R10 and orbits.
- `DQV3604_5_coeff_candidate`: CANDIDATE_NOT_CERTIFIED - Hidden coefficient directions can be vertical only if visible constants and source/current scales are q-basic constants or parent normal-form slots.
- `DQV3604_6_boundary_candidate`: LOCAL_CANDIDATE_NOT_CERTIFIED - Boundary/reference directions are at best locally vertical after fixed boundary class, zero compact flux, source-blind H_ref and corner silence.
- `DQV3604_7_RAB_rejection`: REJECTED_CURRENT_BRANCH - R_AB/lambda_R is not eligible for the q-basic zero theorem under the current observer-cell map because Dq[v_RAB] is nonzero unless the observer map is rebuilt or the field is constraint-eliminated first.
- `DQV3604_8_projector_direction`: OBSTRUCTION_NOT_VERTICAL - delta Pi_M or readout-kernel variation is not a vertical direction unless projectors are fixed before variation or every projector derivative is retained separately.
- `DQV3604_9_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - No candidate residual direction has a fully source-backed Dq[v]=0 certificate.  v_q remains the best first target, but it needs first-class/source-vector silence or a Dq leak bound.

## Direction Matrix Audit
- `DQM3604_0_v_q_private` / `v_q_private`: zero_conditional - E_first_class+E_matter+E_boundary+E_readout
- `DQM3604_1_v_memory_tau` / `v_memory_tau`: zero_conditional - E_tau_lock+E_clock+E_frame+E_source_support
- `DQM3604_2_v_coeff` / `v_coeff`: zero_conditional - E_coeff_descent+E_source_scale+E_clock_constants
- `DQM3604_3_v_boundary` / `v_boundary_reference`: local_zero_conditional - E_boundary_flux+E_Href_source+E_corner
- `DQM3604_4_v_RAB` / `v_RAB`: rejected_nonzero_current_map - DObs_e_R+c_aux+Z_R+q_R
- `DQM3604_5_delta_projector` / `delta_projector`: obstruction_not_vertical - c_projector_operator+Delta_support+readout_order
- `DQM3604_6_Y_target` / `Y_target`: target_not_q_primitive - A_X=dYbar(Dq[v])+E_Y

## Dq Leak Bound Rows
- `DQB3604_0_total` / `epsilon_Dq_total`: BOUND_REQUIRED_CRITICAL - max_i ||Dq[v_i]||_q/||v_i|| or declared component norm envelope
- `DQB3604_1_v_q_private` / `epsilon_Dq_vq`: BOUND_REQUIRED_HIGHEST_PRIORITY - ||Dq[v_q]||_q/||v_q|| <= E_first_class+E_matter+E_boundary+E_readout
- `DQB3604_2_v_memory_tau` / `epsilon_Dq_memory_tau`: BOUND_REQUIRED - ||Dq[v_memory]|| <= E_tau_lock+E_clock+E_frame+E_source_support
- `DQB3604_3_v_coeff` / `epsilon_Dq_coeff`: BOUND_REQUIRED - ||Dq[v_coeff]|| <= E_coeff_descent+E_source_scale+E_clock_constants
- `DQB3604_4_v_boundary` / `epsilon_Dq_boundary`: BOUND_REQUIRED_LOCAL_ONLY - ||Dq[v_boundary]||_local <= E_boundary_flux+E_Href_source+E_corner
- `DQB3604_5_v_RAB` / `epsilon_Dq_RAB`: REJECTED_BOUND_REQUIRED_IF_REUSED - Dq[v_RAB] retained nonzero unless observer-cell map rebuilt or constraint-first elimination is proved
- `DQB3604_6_delta_projector` / `epsilon_Dq_projector`: BOUND_REQUIRED_OBSTRUCTION - ||Dq[delta Pi_M]|| <= c_projector_operator+Delta_support+readout_order
- `DQB3604_7_q_parent_definition` / `epsilon_q_parent`: BOUND_REQUIRED_CRITICAL - q(Phi)=Q_vis projection ownership defect
- `DQB3604_8_Ax_transfer` / `epsilon_AX_from_Dq`: TRANSFER_ROW_NONCLAIM - ||dYbar|| epsilon_Dq + E_Y

## Promotion Gates
- `PROM3604_0_vertical_matrix_criterion`: PASS_EXACT_CRITERION - v is vertical only if every q-component derivative vanishes on the same branch
- `PROM3604_1_Dq_bound_law`: PASS_EXACT_BOUND_LAW - unsigned verticality becomes epsilon_Dq component bounds with no cancellation
- `PROM3604_2_current_vertical_basis_claim`: FAIL_CURRENT_CLAIM - no candidate direction has source-backed Dq[v]=0 across all q-components
- `PROM3604_3_vq_priority`: PASS_ROUTE_SELECTED - v_q is the highest-priority candidate but requires first-class/source-vector silence or Dq leak bound
- `PROM3604_4_RAB_guard`: PASS_GUARD - v_RAB cannot be used in q-basic zero theorems unless the observer map is rebuilt or constraint-first elimination is proved
- `PROM3604_5_anti_tautology_guard`: PASS_GUARD - source coordinates are derived targets, not q-map components inserted to force A_X=0
- `PROM3604_6_no_Newton_GR_claim`: FAIL_CURRENT_CLAIM - q-basic source-coordinate/H_tau/density/support zeros stay conditional while Dq matrix is unsigned
- `PROM3604_7_bound_pack`: PASS_NONCLAIM - all candidate direction rows are source-ready but not score-ready
- `PROM3604_8_next_target`: PASS_ROUTE_SELECTED - attack v_q first-class/source-vector silence or fill epsilon_Dq_vq bound

## Status
- `ACTUAL_QMAP_VERTICAL_BASIS_UNSIGNED_DQ_LEAK_BOUNDS_INSTALLED`: 3604 turns verticality into an explicit Dq matrix problem: v is in ker(Dq) only if every q-component derivative vanishes on the same branch. No candidate direction currently passes; v_q is the best first attack, while v_RAB is rejected under the current observer map.
- Decision: keep q-basic zero theorems conditional, retain epsilon_Dq rows for v_q, v_memory_tau, v_coeff, v_boundary, v_RAB and delta_projector, and move next to the v_q first-class/source-vector silence proof or bound
- Still missing: parent-owned q definition, residual basis action, Dq entries, first-class/source-vector silence for v_q, tau/frame lock for memory directions, coefficient descent, compact boundary/reference silence, projector fixedness and a declared q-component norm

## Validation
- `VAL3604_0_sources_exist`: PASS (all required 3604 source paths exist)
- `VAL3604_1_needles_found`: PASS (all selected 3604 source anchors found)
- `VAL3604_2_outputs_exist`: PASS (all pre-validation 3604 csv output files written)
- `VAL3604_3_csv_parse`: PASS (source_register:19; vertical_theorem:10; direction_matrix:7; dq_leak_bounds:9; promotion_gates:9; status:1; next_target:1; canonical_status:1)
- `VAL3604_4_vertical_criterion_present`: PASS (Dq matrix verticality criterion present)
- `VAL3604_5_direction_rows_present`: PASS (all candidate direction matrix rows present)
- `VAL3604_6_Dq_bound_rows_present`: PASS (all candidate Dq leak bound rows present)
- `VAL3604_7_no_vertical_claims`: PASS (no direction is certified eligible for q-basic zero)
- `VAL3604_8_claims_blocked`: PASS (vertical basis and Newton/GR claims are blocked)
- `VAL3604_9_RAB_guard`: PASS (R_AB rejection guard present)
- `VAL3604_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3604_11_next_target_selected`: PASS (3605 v_q target selected)
- `VAL3604_12_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3604_13_formalization_workbench_untouched`: PASS (no 3604 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3604_0` -> `3605-Y5-R2FR-vq-first-class-source-vector-silence-or-Dq-vq-bound.md`
- Objective: try to prove v_q is first-class/source-silent across geometry, tau, matter, boundary and readout q-components; if not, retain epsilon_Dq_vq with B_qW, C_qT, matter, boundary and readout tail bounds
