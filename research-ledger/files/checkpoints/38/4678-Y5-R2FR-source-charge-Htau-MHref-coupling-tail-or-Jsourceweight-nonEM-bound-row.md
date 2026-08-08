# 4678 - Y5/R2FR Source-Charge Htau/MHref Coupling Tail or Jsourceweight nonEM Bound Row

**Current verdict:** 4678 makes the source-coupling route sharper and less circular.

After 4677:

```text
J_source_weight_abs_after_visible_EM
  = |J_EM_open_dynamic| + |J_source_weight_nonEM|
```

4678 splits the nonEM term:

```text
J_source_weight_nonEM
  = |J_rel_nonEM|
  + |J_common_derivative|
  + |R_eq|
  + |B_zero|
  + |epsilon_HM|.
```

The exact derivation route is:

```text
parent-owned connected nonEM graph
+ one action-density/current owner
+ no Hom(SpeciesLabel, active-source coefficient)
+ constructor exhaustion
+ no hidden/readout re-entry
=> w_A = w_* on the ordinary nonEM component.
```

`w_*` is allowed as calibrated `G_cal/GM` only if derivative-silent. If it varies, it becomes a common-mode fifth-force/source tail for R10/PPN/clock/orbital tests. This is not a public local-GR claim; it is the clean contract for the next proof.

## Runner results

| checkpoint | runner_id | passed | status | detail | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | RUN4678_0_sources | True | PASS | all source paths and needles found | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_1_derivation | True | PASS | scalar-naturality theorem imported | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_2_theorem | True | PASS | future classical owner zero route staged | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_3_vector | True | PASS | post-owner-signed vector written | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_4_tails | True | PASS | R_eq/B_zero/Htau tail contracts written | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_5_common | True | PASS | common G calibration guard written | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_6_nonclaim | True | PASS | all generated rows remain nonclaim | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | RUN4678_7_next | True | PASS | next target selected | False | False | 2026-07-07T17:51:06.211401+00:00 |

## Decision

| checkpoint | decision | why | promoted | claim_allowed | valid_for_claim | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | NONEM_CLASSICAL_SOURCE_WEIGHT_ROUTE_DERIVED_COMMON_G_CALIBRATION_SPLIT_REQ_BZERO_HTAU_TAILS_REMAIN | 4678 imports 4440-4442 into the post-4677 source-weight language. The fixed EM piece is already removed. The nonEM relative source-weight route is now an exact classical scalar-naturality theorem, not a hbar-first bottleneck. Current parent graph/current/no-Hom/Htau clauses remain unsigned, so the residual vector is reduced but nonclaim. | False | False | False | 4679-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md | 2026-07-07T17:51:06.211401+00:00 |

## Status

| checkpoint | branch | fixed_visible_EM_removed | nonEM_classical_route_derived | relative_nonEM_weight_zero_parent_signed | common_G_calibration_guard_written | Req_Bzero_Htau_tails_written | numeric_bound_sourced | local_GR_claim | r10_claim | ppn_claim | decision | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | MTS_R2FR_Y5_SOURCE_CHARGE_HTAU_MHREF_NONEM_SOURCE_WEIGHT_4678 | True | True | False | True | True | False | False | False | False | NONEM_CLASSICAL_SOURCE_WEIGHT_ROUTE_DERIVED_COMMON_G_CALIBRATION_SPLIT_REQ_BZERO_HTAU_TAILS_REMAIN | 4679-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md | 2026-07-07T17:51:06.211401+00:00 |

## Next target

| checkpoint | next_target | why | derive_route | fallback_route | avoid | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | 4679-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md | 4678 turns the source-coupling problem into one concrete proof target: parent-sign a connected nonEM graph/current edge, or fill the first R_eq compact-test/B_zero/Htau tail value. | Parent-sign one nonzero ordinary nonEM action-density/current graph edge with no species/source prefactor, constructor exhaustion, variation-before-readout and no hidden readout re-entry. | Fill R_eq compact-test/multipole, B_zero boundary flux or epsilon_HM with value, units, source path, projection coefficient, arena bound and no-cancellation guard. | Do not use hbar-only ownership, physical template edges, observed GM, or comparator bounds as source definitions. | False | 2026-07-07T17:51:06.211401+00:00 |

## Derivation rows

| checkpoint | derivation_id | claim | equation_or_rule | consequence | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | DER4678_0_nonEM_weight_split | After 4677, split the nonEM source-weight survivor into relative, common-derivative and same-current/source-charge tails. | J_source_weight_nonEM = J_rel_nonEM + J_common_derivative + R_eq + B_zero + epsilon_HM | This replaces one vague coupling term with five testable/derivable objects. | SOURCE_WEIGHT_SPLIT_REFINED | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | DER4678_1_scalar_naturality_theorem | A parent-owned connected nonEM matter graph collapses relative action/source weights. | For every nonzero edge f:A->B, w_B F(f)=F(f)w_A. Since F(f) != 0, w_A=w_B; connectedness gives w_A=w_*. | Relative nonEM source weights vanish if the edge graph, no-source-Hom and no-readout-reentry clauses are parent-signed. | EXACT_CONDITIONAL_DERIVATION | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | DER4678_2_common_G_calibration_guard | The surviving common w_* is not a prediction of numerical G_N; it is allowed as calibrated GR-style G only if derivative-silent. | D_X w_* = D_t w_* = D_frame w_* = D_readout w_* = 0 on the tested branch. | If derivative-silent, w_* is absorbed into G_cal/GM; if not, it becomes J_common_derivative and is tested by R10/PPN/clock/orbital rows. | COMMON_MODE_NOT_HIDDEN | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | DER4678_3_same_current_gate | Even with J_rel_nonEM=0, local Newton/GR still needs the source current equality. | Pi_M J_H = J_M^top + dB_zero + R_eq, with R_eq=0, boundary flux zero and H_tau-H_ref=M_H_ref on the same worldtube. | The next finite fallback is R_eq compact-test/multipole, B_zero flux, or epsilon_HM; not fitted GM. | REQ_BZERO_HTAU_REMAIN | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | DER4678_4_hbar_guard | Universal hbar/quantum measure remains important but is not the first classical local-source lock. | Classical source weights are killed by parent action-density/current/graph/no-Hom/no-reentry. hbar closes quantum/statistical consistency after that. | This is the less scrutiny-heavy route: do the classical source theorem first, then hbar/quantum guard. | HBAR_DEMOTED_TO_QUANTUM_GUARD | False | False | 2026-07-07T17:51:06.211401+00:00 |

## nonEM classical source-weight theorem

| checkpoint | theorem_id | branch | one_classical_parent_action | no_source_Hom_and_no_reentry | parent_owned_connected_nonEM_graph | total_Hilbert_current_owner | hbar_quantum_guard | relative_nonEM_weight_zero | claim_allowed | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | THM4678_0_current_branch | current post-4677 branch | False | False | False | False | False | False | False | CURRENT_BRANCH_OPEN_NONCLAIM | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | THM4678_1_future_classical_owner | future classical nonEM owner branch | True | True | True | True | True | True | False | RELATIVE_NONEM_SOURCE_WEIGHT_ZERO_READY_IF_PARENT_SIGNED | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | THM4678_2_hbar_only_counterroute | hbar owner without classical graph/current | False | False | False | False | True | False | False | HBAR_ONLY_INADEQUATE_FOR_CLASSICAL_SOURCE_WEIGHT | False | 2026-07-07T17:51:06.211401+00:00 |

## Jsourceweight/source-charge split

| checkpoint | vector_id | symbol | formula | meaning | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | VEC4678_0_after_4677 | J_source_weight_abs_after_visible_EM | \|J_EM_open_dynamic\| + \|J_source_weight_nonEM\| | 4677 state | INPUT_VECTOR | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | VEC4678_1_split_nonEM | J_source_weight_nonEM | \|J_rel_nonEM\| + \|J_common_derivative\| + \|R_eq\| + \|B_zero\| + \|epsilon_HM\| | 4678 splits nonEM source weight into theorem-zero and source-current/Htau tails | REFINED_VECTOR | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | VEC4678_2_future_classical_owner | J_rel_nonEM | 0 if one parent action-density/current owner + no Hom + connected nonEM graph + no reentry are signed | exact conditional zero branch | DERIVED_ZERO_CONDITIONAL | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | VEC4678_3_current_claim_safe_vector | J_source_weight_abs_4678_current | \|J_EM_open_dynamic\| + \|J_rel_nonEM_owner_gap\| + \|J_common_derivative\| + \|R_eq\| + \|B_zero\| + \|epsilon_HM\| | current branch keeps unsigned owner gap explicit | NONCLAIM_BOUND_VECTOR | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | VEC4678_4_if_owner_signed | J_source_weight_abs_4678_owner_signed | \|J_EM_open_dynamic\| + \|J_common_derivative\| + \|R_eq\| + \|B_zero\| + \|epsilon_HM\| | what remains after classical nonEM source-weight theorem is signed | NEXT_REDUCED_VECTOR | False | False | 2026-07-07T17:51:06.211401+00:00 |

## Req/Bzero/Htau tail contracts

| checkpoint | tail_id | quantity | definition | units | current_value | test_arena | numeric_ready | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | TAIL4678_0_R_eq | R_eq_compact_test | R_eq[varphi]=int_W (Pi_M J_H-J_M_top-dB_zero) varphi | source_current_distribution | MISSING_REQ_COMPACT_TEST_VALUE | Newton/PPN/orbital same-current tests | False | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | TAIL4678_1_B_zero | B_zero_boundary_flux | Phi_B=int_partialW B_zero/M_H_ref | dimensionless | MISSING_BZERO_FLUX_VALUE | boundary silence/Gdot/orbital tests | False | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | TAIL4678_2_epsilon_HM | Htau_MHref_mismatch | epsilon_HM=\|H_tau[S]-H_ref-M_H_ref\|/M_H_ref | dimensionless | MISSING_HTAU_MHREF_MISMATCH | same-worldtube Hamiltonian/Hilbert source lock | False | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | TAIL4678_3_common_derivative | J_common_derivative | \|D_X ln w_*\|+\|D_t ln w_*\|+\|D_frame ln w_*\|+\|D_readout ln w_*\| | per_source_coordinate_or_declared | MISSING_DERIVATIVE_SILENCE_ROW | R10/PPN/clock/orbital common-mode pressure | False | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | TAIL4678_4_open_EM | J_EM_open_dynamic | \|E_rad_EM\|+\|C_EM_readout\|+\|C_XF2_global_dynamic\|+\|C_JQ_global_dynamic\| | common_source_weight_units | MISSING_OPEN_EM_SOURCE_ROWS | open radiation/readout/global EM branch | False | False | False | 2026-07-07T17:51:06.211401+00:00 |

## Common G calibration guard

| checkpoint | mode_id | condition | effect | interpretation | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | CM4678_0_constant_common_mode | w_* constant over tested branch | absorbed into G_cal/GM | allowed GR-style calibration | NOT_A_CLAIM_TO_DERIVE_NUMERIC_G | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CM4678_1_derivative_common_mode | D w_* != 0 | composition-blind fifth-force/time/source drift | must be scored by R10/PPN/clock/orbital rows | LIVE_TAIL | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CM4678_2_WEP_warning | C_A=C_B=C_common | differential WEP can pass while common fifth force remains | do not use MICROSCOPE alone as local-GR safety | COMMON_MODE_SURVIVES_WEP | False | False | 2026-07-07T17:51:06.211401+00:00 |

## Controls

| checkpoint | control_id | rule | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4678 | CTRL4678_0_no_fitted_G_backfill | Do not use observed orbital GM or fitted G_N as the source-charge proof. | ACTIVE | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CTRL4678_1_common_mode_allowed_only_if_silent | A universal common mode is calibration only if derivative/readout/range silent. | ACTIVE | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CTRL4678_2_hbar_not_first_local_lock | Do not block the classical local-source derivation on hbar before testing action-density/current/graph/no-Hom. | ACTIVE | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CTRL4678_3_no_template_edges | A physical standard-model graph template is not a parent-owned edge certificate. | ACTIVE | False | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | CTRL4678_4_no_local_GR_claim | No local-GR/Newton/PPN/R10 claim until the theorem clauses or finite tails are source-backed. | ACTIVE | False | False | 2026-07-07T17:51:06.211401+00:00 |

## Source register

| checkpoint | source_id | source_path | path_exists | needle | needle_found | line_number | note | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4678 | SRC4678_00_4677_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4677_NEXT_TARGET.csv | True | source-charge/H_tau/MHref/nonEM source-current ownership | True | 2 | 4677 selected this coupling/source-charge target. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_01_4677_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4677_JSOURCEWEIGHT_AFTER_VISIBLE_EM.csv | True | JSW4677_1_after_fixed_visible_EM_import | True | 3 | after visible EM, source-weight vector is open EM plus nonEM. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_02_4677_open | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4677_OPEN_EM_AND_NONEM_SURVIVORS.csv | True | OPEN4677_3_nonEM_weight | True | 5 | nonEM source-weight survivor from 4677. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_03_formal693 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\693-PPC4161-visible-EM-action-edge-parent-signature-or-Jsourceweight-bound-input.md | True | J_source_weight_abs_after_visible_EM | True | 15 | formal 4677 source-weight rewrite. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_04_4440_common | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4440_DERIVATION_ROWS.csv | True | SC4440_0_common_mode_split | True | 2 | common Hilbert source mode is calibrated G, not physical tail. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_05_4440_newton | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4440_DERIVATION_ROWS.csv | True | SC4440_1_structural_newton_bridge | True | 3 | conditional GR/Newton source bridge. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_06_4440_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4440_REDUCED_CONTRACT_ROWS.csv | True | RC4440_0_clean_source_law | True | 2 | source law reduced to Htau/MHref/action-current contract. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_07_4440_tail | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4440_EPSILON_GSRC_TAIL_BOUND_OUTPUT.csv | True | TAIL4440_4_R10_contract | True | 6 | R10/PPN/clock/orbital tail contract precedent. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_08_4441_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4441_ACTION_MEASURE_CURRENT_OWNER_OUTPUT.csv | True | AMCO4441_0_current_after_EM_subcontract | True | 2 | fixed EM subcontract closed, nonEM owner open. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_09_4441_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4441_REDUCTION_ROWS.csv | True | RED4441_1_nonEM_owner | True | 3 | nonEM owner exact conditional, unsigned. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_10_4442_route | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4442_NONEM_SOURCE_ROUTE_OUTPUT.csv | True | NEM4442_0_current_post_EM_branch | True | 2 | current post-EM nonEM route state. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_11_4442_derivation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4442_DERIVATION_ROWS.csv | True | NEM4442_1_scalar_naturality_reused | True | 3 | connected graph collapses source weights. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_12_4442_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4442_REDUCTION_ROWS.csv | True | RED4442_1_classical_no_wA_route | True | 3 | hbar-free classical no-wA route. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_13_4442_tail | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4442_REQ_BZERO_FIRST_TAIL_OUTPUT.csv | True | TAIL4442_0_Req_compact_test_live | True | 2 | R_eq/Bzero/Htau live tail rows. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_14_4442_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4442_VALIDATION.csv | True | VAL4442_17_pycache_absent | True | 19 | 4442 validation. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_15_formal456 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\456-PPC4161-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md | True | epsilon_Gsrc_perp | True | 19 | physical source-coupling tail after common-mode split. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_16_formal457 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\457-PPC4161-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md | True | AMCO4441_1_nonEM_owner_contract | True | 54 | post-EM nonEM owner target. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_17_formal458 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\458-PPC4161-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md | True | NEM4442_1_scalar_naturality_reused | True | 57 | formal route split and scalar naturality theorem. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_18_formal377 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\377-PPC4161-transition-owner-no-wA-theorem-or-explicit-source-coupling-closure.md | True | TH4361_0_scalar_naturality | True | 69 | older scalar action-weight naturality theorem. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_19_formal436 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md | True | AMR4420_0_joint_contract | True | 39 | same-current R_eq/Bzero source contract. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_20_formal481 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\481-PPC4161-source-charge-universality-zero-proof-or-WEP-material-vector-runner.md | True | COMMON_MODE_SURVIVES_WEP | True | 36 | common mode can pass WEP while still affecting R10/PPN/orbital. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_21_post4378 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md | True | topological profile defect | True | 22 | R_eq/topological compact-test and multipole source row precedent. | False | 2026-07-07T17:51:06.211401+00:00 |
| 4678 | SRC4678_22_post3574 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3574-Y5-R2FR-topological-mass-current-origin-or-Meff-drift-source-row.md | True | Pi_M J_H = J_M^top + dB_zero + R_eq | True | 8 | topological source current decomposition. | False | 2026-07-07T17:51:06.211401+00:00 |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL4678_0_sources | True | all source paths and needles found | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_SOURCE_REGISTER.csv | True | rows=23 columns=10 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_DERIVATION_ROWS.csv | True | rows=5 columns=9 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_NONEM_CLASSICAL_SOURCE_WEIGHT_THEOREM.csv | True | rows=3 columns=13 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_JSOURCEWEIGHT_SOURCE_CHARGE_SPLIT.csv | True | rows=5 columns=9 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv | True | rows=5 columns=11 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_COMMON_G_CALIBRATION_GUARD.csv | True | rows=3 columns=9 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_CONTROL_ROWS.csv | True | rows=5 columns=7 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_RUNNER_RESULTS.csv | True | rows=8 columns=8 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_DECISION.csv | True | rows=1 columns=8 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_STATUS.csv | True | rows=1 columns=14 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_parse_P8_Y5_R2FR_4678_NEXT_TARGET.csv | True | rows=1 columns=8 | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_1_runner_pass | True | runner rows passed | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_2_outputs_exist | True | post/formal/csv outputs exist | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_3_claim_row_exists | True | L-520 present | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_4_markers | True | spine and packet markers present | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_5_no_claim_promotion | True | runner remains nonclaim | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_6_pycache_absent | True | scripts __pycache__ absent | 2026-07-07T17:51:06.211401+00:00 |
| VAL4678_OVERALL | True | PASS | 2026-07-07T17:51:06.211401+00:00 |
