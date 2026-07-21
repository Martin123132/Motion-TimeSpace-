# 4843 Y5 R2FR source-universality branch reconciliation and Newton-chain propagation

**Status:** 4843 corrects the live branch state. The literal MTS action already contains one standard `L_matter` block and one metric variation, while the private GR-parity branch explicitly adopted one visible matter action with no source/species/material-label map into active-source coefficients. Therefore relative `delta_w_species` and `kappa_A_source_rel` vanish on those branches after the universal common mode is separated. The later 4841/4842 runners remain useful only off branch or after a reactivation guard fails.

**Decision:** `SOURCE_PREFACTOR_ZERO_RESTORED_ON_LITERAL_CORE_ACTION_AND_PRIVATE_GR_PARITY_BRANCH_STRICT_PRIMITIVE_ORIGIN_OPEN_NEWTON_CHAIN_REBASED_NONCLAIM`.

## Core derivation

The declared action syntax is:

```text
S_core = int sqrt(-g) [R/(2 kappa) - L_Lambda + L_matter]
T_H = -2/sqrt(-g) delta S_matter/delta g
```

On the literal/private standard-visible branch, write any putative source coefficient as:

```text
kappa_A = kappa_common 1_A + delta kappa_A
```

The action grammar has one common matter coefficient and no active-source argument built from species, material, hidden or readout labels. Hence:

```text
P_perp delta kappa = 0
delta_w_species = 0
kappa_A_source_rel = 0
E_source_prefactor = 0
delta_MHref_prefactor = 0
delta_Newton_source_prefactor = 0
```

The 4537 connected-graph rank result is a consistency check on the imported component expansion; it is not needed to re-prove a source coefficient absent from the adopted action syntax.

This does **not** imply the full density or Newton residual is zero. The retained nonprefactor envelope is:

```text
E_density_nonpref = E_action_vertical + E_constant_marker + E_matter_lift
                  + E_Hodge_EM + E_Poynting_boundary + E_nonminimal_EM
                  + E_distributional_shell + E_readout_state
E_source_descent_nonpref = E_density_nonpref + E_nonHilbert + E_PiM_Htau
E_Newton_nonpref = E_source_descent_nonpref + E_00 + E_PPN
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4843_00_core_action | True | True | literal MTS full action contains one standard matter term |
| SRC4843_01_fundamental_action | True | True | second core action source repeats one matter block and Hilbert variation |
| SRC4843_02_visible_import | True | True | GR-parity visible matter import contract |
| SRC4843_03_adoption_4446 | True | True | private no-source-prefactor adoption |
| SRC4843_04_rank_4537 | True | True | component graph rank cross-check |
| SRC4843_05_density_4587 | True | True | density q-basic theorem and Poynting once-only lock |
| SRC4843_06_zero_4758 | True | True | already propagated private source-weight zero |
| SRC4843_07_doc_4758 | True | True | explicit branch-state correction and metric-side handoff |
| SRC4843_08_newton_4838 | True | True | current Newton residual runner |
| SRC4843_09_doc_4841 | True | True | later off-branch delta-w fallback |
| SRC4843_10_doc_4842 | True | True | later graph/no-Hom fallback |
| SRC4843_11_strict_origin | True | True | strict primitive-origin control |
| SRC4843_12_runner | True | True | 4843 executable reconciliation runner |
| SRC4843_13_generator | True | True | 4843 generator and validator |

## Theorem audit

| theorem_id | object | current_result | remaining_scope |
| --- | --- | --- | --- |
| SUR4843_0_literal_action | literal MTS matter syntax | ONE_MATTER_BLOCK_BY_DECLARED_ACTION_SYNTAX | strict primitive uniqueness remains separate |
| SUR4843_1_Hilbert_variation | single Hilbert source | EXACT_ON_LITERAL_AND_IMPORTED_BRANCHES | non-Hilbert/boundary currents remain separate |
| SUR4843_2_relative_prefactor | relative source-prefactor zero | BRANCH_EXACT_ZERO | reopens only if an explicit hidden/source/readout prefactor is added |
| SUR4843_3_graph_rank | component graph rank | CONSISTENCY_CHECK_NOT_PRIMARY_PREMISE | current global parent edge ownership remains irrelevant to adopted branch zero |
| SUR4843_4_density_feed | source-prefactor density feed | PROPAGATED_ZERO | other 4587 density components remain |
| SUR4843_5_Newton_feed | Newton source-prefactor feed | PROPAGATED_ZERO | E_00, PPN, PiM/Htau, boundary and non-Hilbert pieces remain |
| SUR4843_6_strict_origin | strict primitive origin | OPEN_NOT_REQUIRED_FOR_PRIVATE_CORRESPONDENCE | required for a global primitive-origin claim |
| SUR4843_7_history_fix | 4841/4842 branch status | REBASED_AS_FALLBACK_NOT_LIVE_PRIVATE_BLOCKER | do not reopen private w_A without explicit reactivation evidence |

## Newton-chain propagation

| propagation_id | quantity | branch_value | effect | survivor_or_guard |
| --- | --- | --- | --- | --- |
| PROP4843_0_delta_w | delta_w_species | 0 | 4841 source-only weight feed removed on literal/private branch | off-branch finite runner retained |
| PROP4843_1_kappaA | kappa_A_source_rel | 0 | 4842 relative source-prefactor feed removed on literal/private branch | hidden/readout reactivation guard retained |
| PROP4843_2_density | E_source_prefactor | 0 | source-prefactor component removed from 4840 density envelope | action/constant/lift/Hodge/Poynting/support/readout pieces remain |
| PROP4843_3_MHref | delta_MHref_prefactor | 0 | source-prefactor component removed from 4839 source descent | PiM/Htau, boundary, nonHilbert and physical MHref remain |
| PROP4843_4_Newton | delta_Newton_source_prefactor | 0 | source-prefactor component removed from 4838 Newton envelope | E00, PPN, boundary, common-G and source profile remain |
| PROP4843_5_PPN | source-weight PPN subvector | 0 | WEP/gamma/beta/preferred-frame source-weight pieces remain zero from 4758 | non-source PPN vector remains |
| PROP4843_6_next | primary live derivation | E_00 | attack metric residual from literal MTS action | 4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md |

## Runner output

| row_id | runner_status | delta_w_species_abs | kappaA_source_rel_abs | delta_Newton_source_prefactor_abs | density_nonprefactor_abs | Newton_nonprefactor_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4843_0_literal_core_action_zero_pass | SOURCE_UNIVERSALITY_ZERO_PASS_PRIVATE_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | RETAINED_SEPARATELY | RETAINED_SEPARATELY |  |
| RUN4843_1_private_GR_parity_rollforward_pass | SOURCE_UNIVERSALITY_ZERO_PASS_PRIVATE_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | RETAINED_SEPARATELY | RETAINED_SEPARATELY |  |
| RUN4843_2_public_strict_origin_control_blocked | BLOCKED_STRICT_PRIMITIVE_ORIGIN | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | MISSING_motion_time_space_primitive_origin_signed;MISSING_global_parent_action_exhaustion_signed;MISSING_global_hidden_visible_interface_signed;MISSING_global_boundary_nonhilbert_silence_signed |
| RUN4843_3_live_remaining_Newton_envelope_missing | BLOCKED_REMAINING_NEWTON_ENVELOPE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_E_action_vertical_abs;MISSING_E_constant_marker_abs;MISSING_E_matter_lift_abs;MISSING_E_Hodge_EM_abs;MISSING_E_Poynting_boundary_abs;MISSING_E_nonminimal_EM_abs;MISSING_E_distributional_shell_abs;MISSING_E_readout_state_abs;MISSING_E_nonHilbert_abs;MISSING_E_PiM_Htau_abs;MISSING_E_E00_abs;MISSING_E_PPN_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_remaining_abs |
| RUN4843_4_remaining_Newton_envelope_smoke_pass | REMAINING_NEWTON_ENVELOPE_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 2.000000000000000e-03 | 4.500000000000000e-03 |  |
| RUN4843_5_hidden_marker_reactivation_control | BLOCKED_PRIVATE_SOURCE_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | MISSING_no_hidden_marker_source_signed |
| RUN4843_6_forbidden_reopen_private_wA | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4843_7_forbidden_full_density_zero | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4843_8_forbidden_public_promotion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4843_9_forbidden_G_absorption | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | RETAINED_SEPARATELY | RETAINED_SEPARATELY | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Validation

| check_id | status | detail |
| --- | --- | --- |
| VAL4843_00_sources_exist | PASS | all cited source paths exist |
| VAL4843_01_needles_found | PASS | all cited source needles found |
| VAL4843_02_runner_compiles | PASS | runner compiles |
| VAL4843_03_generator_compiles | PASS | generator compiles |
| VAL4843_04_output_count | PASS | outputs=10 inputs=10 |
| VAL4843_05_claims_false | PASS | all runner rows remain nonclaim |
| VAL4843_06_literal_zero | PASS | literal core action branch source-prefactor zero passes |
| VAL4843_07_private_rollforward | PASS | 4446/4537/4758 private zero propagates through Newton source-prefactor row |
| VAL4843_08_strict_origin_blocked | PASS | MISSING_motion_time_space_primitive_origin_signed;MISSING_global_parent_action_exhaustion_signed;MISSING_global_hidden_visible_interface_signed;MISSING_global_boundary_nonhilbert_silence_signed |
| VAL4843_09_live_envelope_blocked | PASS | MISSING_E_action_vertical_abs;MISSING_E_constant_marker_abs;MISSING_E_matter_lift_abs;MISSING_E_Hodge_EM_abs;MISSING_E_Poynting_boundary_abs;MISSING_E_nonminimal_EM_abs;MISSING_E_distributional_shell_abs;MISSING_E_readout_state_abs;MISSING_E_nonHilbert_abs;MISSING_E_PiM_Htau_abs;MISSING_E_E00_abs;MISSING_E_PPN_abs;MISSING_P_Newton_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_remaining_abs |
| VAL4843_10_smoke_values | PASS | remaining nonprefactor envelope arithmetic passes |
| VAL4843_11_reactivation_guard | PASS | hidden marker correctly reopens the finite route |
| VAL4843_12_forbidden_routes | PASS | all forbidden branch promotions and absorptions fail |
| VAL4843_13_resume_rebased | PASS | resume records corrected branch state and next E00 target |
| VAL4843_14_no_pycache | PASS | scripts __pycache__ removed |

## What changed

- The source-weight loop is closed again on the literal/private branch; 4841/4842 are off-branch fallback machinery.
- Zero is propagated into the exact source-prefactor pieces of the density, `M_H_ref`, Newton and PPN chains.
- Every non-source residual remains explicit, so this is not a local-GR or Newton claim.
- The next derivation target moves to the metric side: `E_00` from the literal MTS action.

## Next target

`4844-Y5-R2FR-E00-parent-residual-collapse-from-literal-MTS-action-or-first-physical-coefficient-row.md`
