# 987 Y5 R10: Coulomb To AlphaEM Normal Form Or Parent Zero Gate

Status: `Y5_R10_987_Coulomb_WEP_routes_to_btheta_alphaEM_not_bkappa_finite_route_parent_unsigned`

Claim ceiling: no WEP pass, no clock pass, no `b_theta_alpha_EM` bound, no `b_kappa` bound, no local-GR claim.

## Readout

987 classifies the cleanest finite WEP route. The Coulomb proxy is an EM/fine-structure sensitivity. It should route first to `b_theta_alpha_EM`, not to `b_kappa`. Universal `kappa` remains invisible to differential WEP unless it becomes composition dependent.

There are three honest branches: constant/locked EM gives `C_C=0` if parent-signed; finite `alpha_EM(X)` gives a `b_theta_alpha_EM` channel; marker-dependent `alpha_EM(I_Q,m)` is forbidden or retained as `b_m` closure. No branch is claim-ready yet.

## Source Register

| source_id | role | exists | needle_found | path |
| --- | --- | --- | --- | --- |
| 986_doc | handoff selecting Coulomb-to-alphaEM normal form | true | true | 986-Y5-R10-Ci-to-MTS-slot-map-or-parent-zero-theorem.md |
| 986_map | C_C to b_theta_alpha route | true | true | source-intake/mts_residuals/P8_Y5_R10_986_CI_TO_MTS_SLOT_MAP.csv |
| 986_obligations | EM normal-form proof obligation | true | true | source-intake/mts_residuals/P8_Y5_R10_986_PROOF_OBLIGATIONS.csv |
| 984_imported_basis | imported Coulomb charge basis | true | true | source-intake/mts_residuals/P8_Y5_R10_984_IMPORTED_PHENOMENOLOGICAL_BASIS.csv |
| 983_delta | MICROSCOPE Coulomb proxy contrast | true | true | source-intake/mts_residuals/P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv |
| 622_doc | b_theta alpha_EM slot and parent matter contract | true | true | 622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md |
| 448_doc | constant-sector hazard and forbidden alpha_EM(Z) vertices | true | true | 448-constant-sector-universality-theorem-attempt.md |
| 240_doc | older alpha_EM(Z) direct memory-probe hazard | true | true | 240-universal-coupling-parent-contract-or-local-bound-data-runner.md |

## EM Normal Forms

| form_id | normal_form | Coulomb_effect | MTS_slot | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EMNF987_0_parent_zero_constant_EM | EM sector is part of ordinary matter with constant representation data | C_C=0 for local MTS X direction | none; parent-zero branch | RELATIVE_ZERO_THEOREM | parent-signed constant-sector trivial action and no marker/source-weight term | false |
| EMNF987_1_finite_alphaEM_X | EM coupling depends on local MTS branch | C_C = P_C_alpha * b_alpha * profile_X | b_theta_alpha_EM | FINITE_ROUTE_IDENTIFIED_NOT_DERIVED | parent EM coupling term, P_C_alpha sensitivity, profile_X normalization | false |
| EMNF987_2_marker_dependent_alpha | EM coupling depends on quotient/material marker | C_C may be nonzero but belongs to marker/closure branch | b_m or forbidden post-readout branch | FORBIDDEN_OR_RETAINED_MARKER_ROUTE | marker taxonomy/no-extension theorem or explicit finite b_m bound | false |
| EMNF987_3_emergent_EM_geometry_locked | EM is emergent/geometry-locked with no independent alpha_EM X-variation | C_C=0 if the emergent EM map is parent-signed | parent-zero or derived EM-lock branch | PROMISING_BUT_NOT_PARENT_SIGNED | actual emergent EM parent map plus Maxwell/fine-structure limit | false |
| EMNF987_4_verdict | Coulomb-to-alphaEM status | finite WEP Coulomb channel is b_theta_alpha_EM, not b_kappa | b_theta_alpha_EM first | CLEAN_FINITE_ROUTE_BUT_PARENT_UNSIGNED | EM normal form and profile normalization | false |

## Coulomb Projection

| projection_id | formula | known_from_983 | known_from_986 | missing_inputs | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CPROJ987_0_symbolic_map | eta_Coulomb = DeltaQ_C * P_C_alpha * b_alpha * profile_X | DeltaQ_C = -2.574514671e+00 for TiAlloy - PtRh10 proxy | C_C routes to b_theta_alpha_EM | P_C_alpha,b_alpha,profile_X | not_scoreable | false |
| CPROJ987_1_identity_debug_link | if P_C_alpha*profile_X=1, then \|b_alpha\| <= 2.715851682e-15 | IB983_coulomb_proxy identity debug bound | identity assumption is not an MTS map | proof P_C_alpha*profile_X=1 or actual value | debug_only | false |
| CPROJ987_2_clock_EM_link | same b_alpha should also face clock/fine-structure tests: d ln alpha_EM/dXhat |  | WEP Coulomb and clocks must not be scored independently if they share b_alpha | clock sensitivity matrix and local Xhat environment profile | cross_arena_coupling_needed | false |

## Parent-Zero Gate

| gate_id | condition | math_form | result_if_signed | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PZG987_0_constant_EM | alpha_EM is representation data with trivial local MTS action | L_X alpha_EM=0 | C_C=0 | not_parent_signed | false |
| PZG987_1_no_direct_vertex | parent matter action has no alpha_EM(X), alpha_EM(I_Q), or alpha_EM(m) vertex | partial_X Z_F = partial_IQ Z_F = partial_m Z_F = 0 | no direct EM WEP/clock source | forbidden_policy_only | false |
| PZG987_2_emergent_EM_lock | if EM is emergent, its fine-structure readout is local-X silent | D alpha_EM[Dq(X)] = 0 | C_C=0 without separately postulating constant alpha | not_derived | false |
| PZG987_3_verdict | parent-zero branch for Coulomb WEP channel | EMNF987_0 or EMNF987_3 plus source-universality gates | C_C theorem-zero | relative_only | false |

## Claim Gates

| gate_id | claim | gate_pass | claim_allowed | why_not |
| --- | --- | --- | --- | --- |
| CGATE987_0_route | Coulomb route maps to b_theta_alpha_EM rather than b_kappa | route_identified | false | route identity is not a numeric coefficient bound |
| CGATE987_1_btheta_bound | MICROSCOPE bounds b_theta_alpha_EM | false | false | P_C_alpha and profile_X are missing |
| CGATE987_2_parent_zero | C_C is theorem-zero | false | false | constant/emergent EM lock is not parent-signed |
| CGATE987_3_WEP_clock_combined | WEP+clock alpha_EM branch passes | false | false | clock sensitivity/environment profile not connected |
| CGATE987_4_local_GR | local-GR branch passes | false | false | EM route is a finite/nonclaim map audit |

## Decision Ledger

| decision_id | topic | result | reason | next_action |
| --- | --- | --- | --- | --- |
| DEC987_0_route | Coulomb WEP channel | routes_to_btheta_alpha_not_bkappa | Coulomb binding is an EM/fine-structure matter-constant sensitivity | connect this slot to clock/fine-structure constraints before numeric scoring |
| DEC987_1_zero | parent-zero branch | possible_but_unsigned | constant/emergent EM lock could set C_C=0, but the parent EM map is missing | derive EM-lock theorem or retain finite b_theta_alpha placeholder |
| DEC987_2_best_next | next checkpoint | alphaEM_clock_WEP_joint_prior_or_EM_lock_theorem | the same b_alpha should be constrained by WEP Coulomb and clock/fine-structure arenas, so the next move is cross-arena tying | write 988 alpha_EM WEP-clock joint-prior skeleton or EM-lock theorem attempt |

## Validation

| check_id | result | detail | generated_utc |
| --- | --- | --- | --- |
| V987_0_sources | pass | all source files exist and needles are found | 2026-06-14T02:04:47.162543+00:00 |
| V987_1_normal_form_verdict | pass | Coulomb route verdict is finite but parent-unsigned | 2026-06-14T02:04:47.162556+00:00 |
| V987_2_projection_nonclaim | pass | projection rows remain nonclaim | 2026-06-14T02:04:47.162559+00:00 |
| V987_3_parent_zero_nonclaim | pass | parent-zero gate remains nonclaim | 2026-06-14T02:04:47.162562+00:00 |
| V987_4_claim_gates_safe | pass | claim gates block WEP/clock/local-GR claims | 2026-06-14T02:04:47.162565+00:00 |
| V987_5_next_decision | pass | 988 alphaEM WEP-clock/EM-lock target selected | 2026-06-14T02:04:47.162567+00:00 |
| V987_6_next_target_written | pass | next target row is present and nonclaim | 2026-06-14T02:04:47.162570+00:00 |
| V987_7_formalization_untouched | pass | formalization-workbench modified-file count since script start is 0 | 2026-06-14T02:04:47.162572+00:00 |
| V987_READY | pass | 987 checkpoint pack validation summary | 2026-06-14T02:04:47.162575+00:00 |

## Next Target

| next_target | objective | include | exclude | valid_for_claim |
| --- | --- | --- | --- | --- |
| 988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md | tie the Coulomb WEP b_theta_alpha route to clock/fine-structure constraints, or derive an EM-lock theorem that sets local alpha_EM variation to zero | WEP Coulomb proxy, d_ln_alpha_EM_dXhat prior slot, clock sensitivity placeholders, EM-lock parent gate | WEP pass, clock pass, invented sensitivity coefficients, b_kappa claim, GitHub action, formalization-workbench edits | false |
