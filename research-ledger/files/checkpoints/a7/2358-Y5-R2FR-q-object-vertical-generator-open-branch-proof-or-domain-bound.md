# 2358 — `q` Object / Vertical Generator Open-Branch Proof Or Domain Bound

Created UTC: `2026-06-21T20:25:33.760650+00:00`

Branch: `MTS_R2FR_Q_OBJECT_VERTICAL_GENERATOR_OPEN_BRANCH_2358`

## Result

Result: the **`q` object / vertical-generator proof does not close for current MTS yet**.

The exact theorem route is now clear: build a parent local field chart and equivalence relation, define
`q: Phi_parent -> Q_vis`, prove the candidate generators are tangent to fibres on an open branch, and verify the full
`Dq` matrix: coframe, source/readout, constants/markers, boundary/projector and tau pushforward.

That does **not** happen in the current corpus. Therefore `MCA2357` remains a clean coupling candidate, not a local-GR/Newton
derivation. The finite fallback is the explicit no-cancellation envelope `epsilon_Dq_open_branch_abs`.

## Source Audit

| row_id | source_key | exists | needles_found | source_role |
| --- | --- | --- | --- | --- |
| SRC2358_00_2357_doc | 2357_doc | true | true | 2357 handoff |
| SRC2358_01_2357_validation | 2357_validation | true | true | 2357 validation |
| SRC2358_02_2357_signing_q | 2357_signing | true | true | q object still upstream |
| SRC2358_03_2357_inputs | 2357_inputs | true | true | q vertical input requirement |
| SRC2358_04_2357_next | 2357_next | true | true | machine handoff |
| SRC2358_05_1157_qmap | 1157_qmap | true | true | q-map/null generator verdict |
| SRC2358_06_1157_cg | 1157_cg | true | true | c_g first fill zero theorem block |
| SRC2358_07_1737_q_contract | 1737_q_contract | true | true | q-map contract |
| SRC2358_08_1737_basis | 1737_basis | true | true | vertical basis contract |
| SRC2358_09_1737_dq | 1737_dq | true | true | Dq matrix requirements |
| SRC2358_10_1737_finite | 1737_finite | true | true | finite Dq source rows |
| SRC2358_11_1738_kernel | 1738_kernel | true | true | coframe kernel clause verdict |
| SRC2358_12_1738_theorem | 1738_theorem | true | true | coframe chain-rule theorem |
| SRC2358_13_1738_directions | 1738_directions | true | true | direction classification |
| SRC2358_14_1738_rows | 1738_rows | true | true | finite DObs_e rows |
| SRC2358_15_1739_ownership | 1739_ownership | true | true | coframe ownership gate |
| SRC2358_16_1739_theorem | 1739_theorem | true | true | common-frame zero theorem |
| SRC2358_17_1739_bg | 1739_bg | true | true | common-frame derivative rows |
| SRC2358_18_1575_vertical | 1575_vertical | true | true | RAB verticality verdict |
| SRC2358_19_1575_trilemma | 1575_trilemma | true | true | coframe visibility trilemma |
| SRC2358_20_1575_matter | 1575_matter | true | true | matter descent still unsigned |
| SRC2358_21_1621_constraint | 1621_constraint | true | true | constraint-first alternative |
| SRC2358_22_1621_nopole | 1621_nopole | true | true | no-pole alternative |
| SRC2358_23_1505_vertical | 1505_vertical | true | true | quotient vertical theorem ledger |
| SRC2358_24_1505_dq | 1505_dq | true | true | Dq verticality tests |


## Open-Branch Audit

| row_id | gate | mathematical_requirement | proof_status | failure_if_missing | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QVA2358_0_parent_chart | parent local field chart | Phi_parent=(Q_vis, r_aux, gauge, boundary) on an open neighbourhood with smooth admissible domain | CHART_CONTRACT_ONLY | open-branch Dq(v)=0 cannot even be stated | false | false |
| QVA2358_1_equivalence_relation | parent equivalence relation | Phi~Phi' iff ordinary-matter-visible observables and parent-owned constants/readouts agree | EQUIVALENCE_RELATION_NOT_DERIVED | q can be chosen post-hoc to hide residuals | false | false |
| QVA2358_2_q_map | q object | q: Phi_parent -> Q_vis is a parent map, not a closure label | Q_OBJECT_NOT_PARENT_SIGNED | matter coupling action uses q without deriving it | false | false |
| QVA2358_3_vertical_basis | candidate vertical generator basis | v_a are tangent to fibres of q on an open branch, with owned compensators if needed | VERTICAL_BASIS_NOT_SIGNED | residual directions may be physical coframe/source modes | false | false |
| QVA2358_4_Dq_matrix | componentwise Dq kernel | DObs_e[v]=Dsource_readout[v]=Dtheta_marker[v]=Dboundary_projector[v]=Dtau_pushforward[v]=0 | Dq_KERNEL_UNSIGNED_RETAIN_FINITE_ROWS | common-frame/source/readout leakage survives | false | false |
| QVA2358_5_null_presymplectic_route | null/presymplectic generator | Omega(v_a,delta)=0 plus zero boundary charge on the same branch | CONDITIONAL_ROUTE_NOT_CURRENTLY_SIGNED | verticality by missing kinetic term is not evidence | false | false |
| QVA2358_6_constraint_no_pole_route | constraint/no-pole elimination before matter | residual is algebraic/second-class/absent before matter coupling, with no boundary/readout reentry | BEST_ALTERNATIVE_NOT_DERIVED | finite source-current/Yukawa rows remain live | false | false |
| QVA2358_7_open_branch_verdict | q/v open-branch proof | QVA2358_0 through QVA2358_6 all close in one parent branch | OPEN_BRANCH_VERTICALITY_NOT_DERIVED | MCA2357 cannot fire as a local-GR/Newton proof | false | false |


## Dq Kernel Gate Matrix

| row_id | component | meaning | zero_requirement | current_status | finite_fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| DQM2358_0_DObs_e | DObs_e[v] | observed coframe/metric derivative | QVA2358_2_q_map;QVA2358_4_Dq_matrix | MISSING_THEOREM_OR_NUMERIC_DOBS_E | DObs_e[v]_finite_row | false |
| DQM2358_1_Dsource_readout | Dsource_readout[v] | source/clock/orbit/photon/ruler/boundary readout derivative | QVA2358_1_equivalence_relation;QVA2358_4_Dq_matrix | MISSING_SOURCE_READOUT_DESCENT | Dsource_readout[v]_finite_row | false |
| DQM2358_2_Dtheta_marker | Dtheta_marker[v] | ordinary constants/material marker derivative | QVA2358_1_equivalence_relation;MCA2357 fixed-theta contract | MISSING_CONSTANT_MARKER_DESCENT | Dtheta_marker[v]_finite_row | false |
| DQM2358_3_Dboundary_projector | Dboundary_projector[v] | boundary/projector/source-measure derivative | QVA2358_4_Dq_matrix;QVA2358_6_constraint_no_pole_route | MISSING_BOUNDARY_PROJECTOR_BASICNESS | Dboundary_projector[v]_finite_row | false |
| DQM2358_4_Dtau_pushforward | Dq(L_tau Phi)-L_tau_red q(Phi) | tau pushforward/source-clock-orbit lock | tau parent selection;source/charge/clock/orbit branch lock | MISSING_TAU_PROJECTABILITY | Dq(L_tau Phi)-L_tau_red q(Phi)_finite_row | false |
| DQM2358_5_kernel_total | Dq[v_a] | total Dq kernel over candidate vertical basis | all DQM2358_0..4 zero on same open branch | Dq_KERNEL_UNSIGNED_RETAIN_BOUND_ROWS | Dq[v_a]_finite_row | false |


## Quotient / Constraint Routes

| row_id | route | condition | would_deliver | current_status | rank | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| QCR2358_0_quotient_route | quotient representative route | q object, equivalence relation, vertical basis and Dq matrix all parent-signed | v_a in ker(Dq); MCA2357 matter descent fires; support motion theorem-zero | BEST_ZERO_ROUTE_UNSIGNED | 1 | false |
| QCR2358_1_constraint_route | constraint/no-pole route | residual eliminated algebraically/second-class before matter coupling, no boundary/readout reentry | no local source-current pole without relying on vertical-by-label | BEST_LOCAL_GR_ROUTE_UNSIGNED | 2 | false |
| QCR2358_2_finite_bound_route | finite Dq/domain bound route | q/v proof fails but Dq, source/readout, common-frame, boundary and M_H_ref rows are numeric | testable residual vector instead of GR reduction theorem | MISSING_NUMERIC_INPUTS | 3 | false |
| QCR2358_3_closure_axiom | closure axiom | declare residual vertical/zero without q, Dq or constraint proof | nothing claim-grade | REFUSED | 99 | false |


## Dq / Domain Bound Rows

| row_id | quantity | component | formula | status | units | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DQB2358_0_total | epsilon_Dq_open_branch_abs | absolute no-cancellation Dq/domain leakage envelope | |DObs_e|+|Dsource_readout|+|Dtheta_marker|+|Dboundary_projector|+|Dtau_pushforward|+|boundary_charge| | MISSING_COMPONENT_VALUES | dimensionless_or_declared_component_norm | false | false |
| DQB2358_1_DObs_e | DObs_e_leak_abs | coframe/metric visibility of candidate vertical direction | ||e_obs^-1 DObs_e[v_a]|| | MISSING_DOBS_E_ZERO_OR_NUMERIC_ROW | dimensionless_per_declared_direction_unit | false | false |
| DQB2358_2_Dsource_readout | Dsource_readout_leak_abs | source/clock/orbit/boundary readout visibility | ||Dsource_readout[Dq(v_a)]|| | MISSING_SOURCE_READOUT_ZERO_OR_NUMERIC_ROW | declared_readout_norm | false | false |
| DQB2358_3_Dtheta_marker | Dtheta_marker_leak_abs | constant/material marker derivative | sum_A ||L_v theta_A|| or material marker norm | MISSING_THETA_MARKER_ZERO_OR_NUMERIC_ROW | dimensionless_or_declared_marker_norm | false | false |
| DQB2358_4_Dboundary_projector | Dboundary_projector_leak_abs | boundary/projector/source-measure variation | ||Dboundary_projector[Dq(v_a)]|| | MISSING_BOUNDARY_PROJECTOR_ZERO_OR_NUMERIC_ROW | boundary_projector_norm | false | false |
| DQB2358_5_Dtau_pushforward | Dtau_pushforward_leak_abs | tau projectability/source-clock-orbit mismatch | ||Dq(L_tau Phi)-L_tau_red q(Phi)|| | MISSING_TAU_PROJECTABILITY_ZERO_OR_NUMERIC_ROW | tau_pushforward_norm | false | false |
| DQB2358_6_boundary_charge | Q_boundary_v_abs | boundary charge carried by the would-be vertical generator | abs(int_boundary Q_v)/M_H_ref or declared boundary normalization | MISSING_BOUNDARY_CHARGE_ZERO_OR_NUMERIC_ROW | dimensionless_after_M_H_ref_or_declared_boundary_units | false | false |
| DQB2358_7_acceptance_rule | Dq_bound_acceptance | acceptance rule | no Dq/domain row can score until every component has theorem-zero or numeric source path, units, direction basis and normalization | NONCLAIM_ACCEPTANCE_RULE_INSTALLED | gate | false | false |


## Decision Ledger

| row_id | decision | reason | effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2358_0_result | do not claim q-object/open-branch verticality for current MTS | parent chart, equivalence relation, Dq matrix, boundary/tau projectability, and null/constraint proof are unsigned | MCA2357 cannot yet fire as a local-GR/Newton derivation | false |
| DEC2358_1_progress | q/v gate is now precise | the required proof has been reduced to open-branch chart + Dq matrix + no boundary charge, not a vague verticality claim | future work can attack rows QVA2358/DQM2358 directly | false |
| DEC2358_2_best_route | prefer parent q-object construction before numeric fallback | if q and Dq close, the coupling theorem becomes clean; if not, the finite Dq vector is the honest empirical branch | 2359 should build the field chart/equivalence relation contract or select constraint/no-pole explicitly | false |


## Claim Gates

| row_id | claim | passes_public_claim | blocked_by | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2358_0_q_object | parent q object is constructed | false | QVA2358_0_parent_chart;QVA2358_1_equivalence_relation;QVA2358_2_q_map | false |
| CG2358_1_vertical_generator | v_a in ker(Dq) on an open local branch | false | QVA2358_3_vertical_basis;QVA2358_4_Dq_matrix;DQM2358_5_kernel_total | false |
| CG2358_2_constraint_no_pole | constraint/no-pole alternative removes residual before matter | false | QVA2358_6_constraint_no_pole_route;QCR2358_1_constraint_route | false |
| CG2358_3_local_GR_Newton | local GR/Newton source-current gate reopens | false | q/v not derived; constraint/no-pole not derived; finite Dq bound rows missing | false |


## Refusal Runner

| row_id | temptation | allowed | why_not | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2358_0_q_by_declaration | define q to exclude every troublesome residual | false | q must be supplied by parent kinematics/action before readout, not chosen after the local tests | QVA2358_1_equivalence_relation;QVA2358_2_q_map | false |
| REF2358_1_vertical_by_label | call v vertical without computing the Dq matrix | false | DObs_e, source/readout, markers, boundary/projector and tau pushforward must all vanish or be bounded | QVA2358_4_Dq_matrix;DQM2358_5_kernel_total | false |
| REF2358_2_missing_kinetic_as_null | treat absent/missing kinetic terms as proof of null gauge direction | false | null direction needs presymplectic degeneracy and zero boundary/source charge, not absence of a written term | QVA2358_5_null_presymplectic_route;DQB2358_6_boundary_charge | false |
| REF2358_3_magic_constraint | insert a multiplier to remove the residual and call it derived | false | constraint/no-pole route needs parent origin, algebraic sort, no kinetic pole and boundary/readout stability | QVA2358_6_constraint_no_pole_route;CG2358_2_constraint_no_pole | false |


## Next Targets

| row_id | next_target | why | route_type | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2358_0 | 2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md | the missing proof starts at the parent field chart/equivalence relation; if that cannot be sourced, choose the constraint/no-pole route explicitly | derivation_first | false |
| NEXT2358_1 | 2359b-Y5-R2FR-Dq-matrix-finite-bound-input-pack.md | fallback if q/v cannot close: source every Dq/domain component row with units and arena projection | fallback_nonclaim | false |


## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2358_00_required_sources_exist | PASS | every required source path exists | false |
| VAL2358_01_required_needles_found | PASS | all required source needles were found | false |
| VAL2358_02_outputs_exist | PASS | all 2358 outputs written | false |
| VAL2358_03_open_branch_audit_written | PASS | open-branch q/v audit written and blocked | false |
| VAL2358_04_dq_gate_nonclaim | PASS | Dq kernel gates remain nonclaim | false |
| VAL2358_05_bound_rows_nonclaim | PASS | Dq/domain bound rows remain non-score-ready | false |
| VAL2358_06_claim_gates_blocked | PASS | all public claim gates blocked | false |
| VAL2358_07_next_selected | PASS | 2359 field-chart/equivalence target selected | false |
| VAL2358_08_branch_copies_parse | PASS | branch copies exist | false |
| VAL2358_09_formalization_untouched | PASS | no 2358 checkpoint output appears in formalization-workbench | false |
| VAL2358_10_no_claim_flags | PASS | no generated row has claim/score-ready/parent-signed true flags | false |
| VAL2358_11_no_github_policy | PASS | public GitHub update not recommended from 2358 | false |
| VAL2358_OVERALL | PASS | 2358 audits the q-object/open-branch vertical-generator proof, refuses q-by-declaration and vertical-by-label, keeps Dq/domain bound rows nonclaim, and selects parent field-chart/equivalence construction as 2359. | false |

