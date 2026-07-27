# 3606 - BqWeyl no-spurion zero or finite Weyl bound

## Verdict
3606 proves the useful algebraic fact: a metric/epsilon-only scalar linear in one Weyl tensor vanishes.  So a nonzero `B_qWeyl` requires a Weyl-type spurion/projector/readout tensor `P^{abcd}`.

That is a good theorem route, but not a live claim: current MTS has not parent-signed the typed no-spurion grammar or q representation.  Therefore `B_qWeyl=0` stays conditional and `E_BqWeyl` remains a finite-row problem.

The finite law is `E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl||` plus boundary/source tails.  Quadratic Weyl `D_qWeyl2` is a separate guard, not killed by the linear index theorem.

## BqWeyl Theorem Gate
- `BQW3606_0_target`: TARGET_IMPORTED - Prove B_qWeyl=0 from QAP plus no-Weyl-spurion/index theorem, or retain finite B_qWeyl rows.
- `BQW3606_1_metric_trace_index_lemma`: EXACT_INDEX_LEMMA - Any scalar linear in C_abcd formed only from metric contractions vanishes because the Weyl tensor is trace-free.
- `BQW3606_2_epsilon_index_lemma`: EXACT_INDEX_LEMMA - epsilon^{abcd}C_abcd also vanishes for a single Weyl tensor; parity-odd curvature scalars begin at quadratic order C*Cdual.
- `BQW3606_3_spurion_necessity`: EXACT_CONDITIONAL_THEOREM - A nonzero scalar linear in Weyl has form q P^{abcd} C_abcd, where P^{abcd} is a Weyl-type spurion/projector/readout tensor.
- `BQW3606_4_QAP_no_spurion_route`: CONDITIONAL_ZERO_THEOREM_NOT_LIVE - If QAP removes q_private source dependence and the parent grammar admits q only as scalar/quotient/pure-density with no Weyl spurion, then B_qWeyl=0.
- `BQW3606_5_finite_bound_law`: EXACT_BOUND_LAW_NONCLAIM - E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| plus boundary/source tails.
- `BQW3606_6_quadratic_guard`: SEPARATE_RESIDUAL_GUARD - B_qWeyl(linear)=0 does not kill D_qWeyl2 q C_abcd C^abcd or q C*Cdual towers.
- `BQW3606_7_current_MTS_verdict`: BOUND_BRANCH_ACTIVE_NO_CLAIM - The linear index theorem is solid, but parent typed grammar, q representation, no-spurion/projector/readout kernel and higher-curvature tower exclusions are not signed.
- `BQW3606_8_best_next_move`: NEXT_TARGET_SELECTED - Either parent-sign the no-spurion grammar or fill the finite B_qWeyl row with B_qWeyl, G_q, C_Weyl profile, units and arena projections.

## BqWeyl Bound Rows
- `BQB3606_0_Z_linear` / `Z_BqWeyl_linear`: BOUND_REQUIRED_OR_ZERO_SWITCH - B_qWeyl=0 if QAP plus typed no-Weyl-spurion grammar is parent-signed
- `BQB3606_1_BqWeyl` / `B_qWeyl`: BOUND_REQUIRED_FIRST_DANGEROUS - linear q-Weyl/tidal curvature mixing coefficient
- `BQB3606_2_Gq` / `G_q_or_Lq_inverse`: BOUND_REQUIRED - same-domain q Green/operator response
- `BQB3606_3_CWeyl` / `C_Weyl_local_profile`: BOUND_REQUIRED - local Weyl/tidal curvature profile entering G_q C_Weyl
- `BQB3606_4_tau_arena` / `tau_BqWeyl_arena`: BOUND_REQUIRED - projection from q-Weyl profile to R10/PPN/clock/orbital/local residuals
- `BQB3606_5_Pspurion` / `P_Weyl_spurion`: BOUND_REQUIRED_IF_ZERO_ROUTE_FAILS - hidden P^{abcd}C_abcd/projector/readout kernel countermodel amplitude
- `BQB3606_6_DqWeyl2_guard` / `D_qWeyl2`: SEPARATE_GUARD_BOUND_REQUIRED - quadratic Weyl/higher-curvature residual not killed by linear theorem
- `BQB3606_7_ppn_kernel_bridge` / `b_R_common_Weyl`: ARENA_KERNEL_NONCLAIM - Cassini-style PPN gamma bridge for common Weyl/frame kernel
- `BQB3606_8_E_BqWeyl_total` / `E_BqWeyl`: TOTAL_BOUND_BRANCH_ACTIVE - tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| + boundary/source tails

## Countermodel Guards
- `BQG3606_0_weyl_spurion` / `q P^{abcd} C_abcd`: blocks linear BqWeyl zero - legal unless parent object-language forbids Weyl-type spurion/projector/readout tensors
- `BQG3606_1_projector_source_map` / `post-variation curvature/readout source map`: blocks variational local-GR reduction - legal unless action normal form rejects readout re-entry before source variation
- `BQG3606_2_hidden_frame` / `hidden conformal/disformal/readout frame`: shifts effect into clocks, matter constants or PPN - legal unless matter/source/readout descent and hidden-frame absence are signed
- `BQG3606_3_quadratic_weyl` / `q C_abcd C^abcd or q C*Cdual`: requires no-tower theorem or finite D_qWeyl2 row - not removed by one-Weyl index theorem
- `BQG3606_4_hidden_curvature_coefficient` / `F(I_hid)R or F(I_hid)C^2`: feeds curvature coefficients despite linear zero - legal if hidden scalar invariant survives

## Promotion Gates
- `PROM3606_0_index_lemma`: PASS_EXACT_LEMMA - metric/epsilon-only scalar linear in Weyl vanishes
- `PROM3606_1_spurion_theorem`: PASS_CONDITIONAL_THEOREM - nonzero B_qWeyl requires P^{abcd}C_abcd or equivalent projector/readout object
- `PROM3606_2_current_zero_claim`: FAIL_CURRENT_CLAIM - parent typed grammar/q representation/no-spurion clauses are not signed
- `PROM3606_3_current_finite_bound`: FAIL_CURRENT_CLAIM - B_qWeyl coefficient, q operator, Weyl profile and arena projections are missing
- `PROM3606_4_quadratic_guard`: PASS_GUARD - linear B_qWeyl zero does not remove D_qWeyl2
- `PROM3606_5_local_vacuum_guard`: PASS_GUARD - Weyl/tidal curvature survives exterior vacuum
- `PROM3606_6_no_Newton_GR_claim`: FAIL_CURRENT_CLAIM - E_BqWeyl is not zero or source-backed finite
- `PROM3606_7_bound_pack`: PASS_NONCLAIM - zero switch and finite input rows are source-ready but not score-ready
- `PROM3606_8_next_target`: PASS_ROUTE_SELECTED - parent-sign no-spurion grammar or fill finite BqWeyl row

## Status
- `BQWEYL_INDEX_THEOREM_STRONG_PARENT_SIGNATURE_UNSIGNED`: 3606 proves the useful algebra: metric/epsilon-only one-Weyl scalars vanish, so a nonzero linear B_qWeyl needs a Weyl-type spurion/projector/readout tensor. The live corpus does not parent-sign no-spurion grammar, so the zero theorem is conditional and the finite row remains missing.
- Decision: retain Z_BqWeyl_linear as a conditional zero switch, keep B_qWeyl/G_q/C_Weyl/tau_arena/spurion/D_qWeyl2 rows nonclaim, and next either parent-sign the no-spurion grammar or fill finite BqWeyl inputs
- Still missing: parent typed object-language, q scalar/density representation, object-language exhaustion, no P^{abcd}/projector/readout kernel, hidden-frame exclusion, B_qWeyl coefficient, q operator normalization, Weyl profile, arena projections and D_qWeyl2 no-tower guard

## Validation
- `VAL3606_0_sources_exist`: PASS (all required 3606 source paths exist)
- `VAL3606_1_needles_found`: PASS (all selected 3606 source anchors found)
- `VAL3606_2_outputs_exist`: PASS (all pre-validation 3606 csv output files written)
- `VAL3606_3_csv_parse`: PASS (source_register:20; bqweyl_theorem:9; bqweyl_bound_rows:9; countermodel_guards:5; promotion_gates:9; status:1; next_target:1; canonical_status:1)
- `VAL3606_4_index_lemmas_present`: PASS (index and spurion necessity rows present)
- `VAL3606_5_bound_rows_present`: PASS (critical BqWeyl bound rows present)
- `VAL3606_6_countermodels_present`: PASS (Weyl spurion and quadratic Weyl guards present)
- `VAL3606_7_claims_blocked`: PASS (BqWeyl zero/finite/local-GR claims are blocked)
- `VAL3606_8_quadratic_guard`: PASS (DqWeyl2 guard present)
- `VAL3606_9_next_target_selected`: PASS (3607 BqWeyl parent-signature/finite-row target selected)
- `VAL3606_10_no_claim_flags`: PASS (all generated physics rows remain nonclaim)
- `VAL3606_11_generated_source_paths_exist`: PASS (every generated row source_path exists)
- `VAL3606_12_formalization_workbench_untouched`: PASS (no 3606 checkpoint output appears in formalization-workbench outside package/venv noise)

## Next target
- `NEXT3606_0` -> `3607-Y5-R2FR-BqWeyl-parent-signature-or-finite-row-acquisition.md`
- Objective: try to parent-sign the no-Weyl-spurion grammar; if that fails, stage finite B_qWeyl acquisition rows for B_qWeyl, G_q, C_Weyl profile, tau_arena projections, units and D_qWeyl2 guard
