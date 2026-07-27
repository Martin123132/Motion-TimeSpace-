# 4682 - Y5/R2FR cR2/MR Parent Scale Gap or Full Finite-Range Bound After Torsion

Marker: `PPC4161_CR2_MR_FINITE_RANGE_GATE_CURRENT_BRANCH_4682`

Decision: `CR2_MR_REDUCED_TO_EXTRA_MODE_ZERO_COMPONENTWISE_BODY_CHARGE_OR_FINITE_RANGE_BOUND_CURRENT_BRANCH_NONCLAIM`

## Result

4682 imports the cR2/MR finite-range ladder into the current branch after the torsion narrowing.

```text
Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r)
c_R2_eff_total = c_cell + c_bare + 0.5 B^T L^-1 B
                 + c_measure + c_boundary + c_marker
```

For positive `L`, `B^T L^-1 B = ||L^-1/2 B||^2`, so a positive memory/fibre operator does not erase a nonzero source vertex. Exterior source-free equations also do not erase body charge.

The cR2/MR branch now closes only through:

```text
parent no-extra-mode selector,
componentwise c_R2_eff_total = 0,
body charge A_body = 0,
heavy mass gap M_i L_arena >> 1,
or source-backed R10/orbital/PPN finite bound.
```

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | SRC4682_00_4681_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4681_NEXT_TARGET.csv | True | 4682-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md | True | 2 | 4681 selected current cR2/MR target. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_01_4681_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4681_STATUS.csv | True | cR2_MR | True | 2 | 4681 status retains cR2/MR as broad survivor. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_02_4454_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4454_STATUS.csv | True | lambda<38.6um_for_alpha1 | True | 2 | older cR2 mode map and short-range anchor. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_03_4454_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4454_NEXT_TARGET.csv | True | cR2-parent-scale-signature-or-alpha-lambda-projection-row | True | 2 | older parent-scale/projection handoff. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_04_4594_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_CR2_ZERO_BOUND_THEOREM.csv | True | TH4594_1_componentwise_zero | True | 3 | componentwise cR2 zero/bound law. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_05_4594_profile | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_FINITE_RANGE_PROFILE_LAW.csv | True | FR4594_2_hidden_memory_fibre | True | 4 | hidden/memory/fibre finite-range profile law. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_06_4594_bounds | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_R10_ORBITAL_BOUND_INTERFACE.csv | True | B4594_0_R10_curve | True | 2 | R10/orbital/PPN finite bound interface. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_07_4594_survivor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_SURVIVOR_UPDATE.csv | True | SURV4594_2_cR2_MR | True | 4 | post-cR2 survivor update. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_08_4594_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_STATUS.csv | True | CR2_MR_REDUCED_TO_PARENT_EXTRA_MODE_ZERO | True | 2 | 4594 decision/status. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_09_4594_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_NEXT_TARGET.csv | True | memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate | True | 2 | 4594 selected memory/fibre owner target. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_10_4594_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4594_VALIDATION.csv | True | VAL4594_18_next_memory_fibre | True | 20 | 4594 validation selected the next memory/fibre owner target. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_11_4595_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_STATUS.csv | True | MEMORY_FIBRE_BC_ZERO_SWITCH | True | 2 | next owner gate already exists. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_12_4595_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv | True | ZS4595_0_common_operator | True | 2 | memory/fibre zero switch source. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_13_4595_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4595_VALIDATION.csv | True | VAL4595_OVERALL | True | 19 | 4595 validation passed. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_14_formal610 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\610-PPC4161-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md | True | c_R2_eff_total = c_cell | True | 22 | formal cR2 finite-range result. | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SRC4682_15_formal611 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\611-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | True | B_X=C_X=J_X=Q_boundary_X=0 | True | 17 | formal next memory/fibre zero switch. | False | 2026-07-07T18:19:21+00:00 |

## cR2 Theorem Import

| checkpoint | theorem_id | claim | derivation | zero_or_exit | finite_bound | status | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | TH4682_0_mode_decomposition | After torsion narrowing, c_R2/M_R is a finite-range extra-mode problem, not a generic local-residual fog. | Import 4594: curvature-square terms map into scalar/tensor Yukawa channels with alpha_i and M_i; each channel is compared without cross-cancellation. | parent two-derivative/no-extra-mode selector sets all curvature-square propagating coefficients to zero | Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r) | CR2_MODE_DECOMPOSITION_IMPORTED_CURRENT_BRANCH | False | 2026-07-07T18:19:21+00:00 |
| 4682 | TH4682_1_componentwise_zero | Without a named parent identity, c_R2_eff_total closes only by componentwise zero/topological/boundary silence. | Use c_R2_eff_total=c_cell+c_bare+0.5 B^T L^-1 B+c_measure+c_boundary+c_marker. | c_cell=c_bare=c_measure=c_boundary=c_marker=0 and B_X=0 on every retained physical hidden/memory/fibre direction, or a parent Ward/topological identity proves the sum is identically zero | \|c_R2_eff_total\| <= sum absolute component bounds; no tuned cancellation credit | COMPONENTWISE_ZERO_OR_ABSOLUTE_BOUND_REQUIRED | False | 2026-07-07T18:19:21+00:00 |
| 4682 | TH4682_2_positive_hidden_obstruction | Positive memory/fibre no-hair is not enough; the curvature-linear vertex must vanish. | If L is positive on the physical quotient, B^T L^-1 B=\|\|L^-1/2 B\|\|^2>=0 and equals zero only when B=0 on the physical subspace. | B_mem=B_h=0, plus C/J/boundary source charges zero if those fields couple to matter/source readout | 0.5 B^T L^-1 B <= 0.5 \|\|B\|\|^2/lambda_min(L) with source-backed B and lambda_min rows | NO_XR_VERTEX_REQUIRED_NOT_OPTIONAL | False | 2026-07-07T18:19:21+00:00 |
| 4682 | TH4682_3_body_charge_zero | Exterior source-free equations do not erase scalaron/body tails. | For (-Z_X nabla^2+M_X^2)X=rho_X, the exterior amplitude A_body is a weighted interior/boundary charge. | A_body=0 iff Q_X[body]+Q_boundary=0 under the selected Green-function convention | \|A_body\| <= [exp(R_body/lambda_X) int_body \|rho_X\| dV + \|Q_boundary\|]/(4*pi \|Z_X\|) | BODY_CHARGE_ZERO_OR_BOUND_REQUIRED | False | 2026-07-07T18:19:21+00:00 |
| 4682 | TH4682_4_empirical_range_bound | If parent zero/body-charge zero fails, c_R2/M_R must be scored as a finite-range Yukawa/scalar-Hessian branch. | The alpha=1 short-range anchor is useful but not sufficient; claim-grade closure needs full alpha(lambda), orbital or PPN projection rows with MTS source charges. | M_i L_arena >> 1, or full source-backed alpha_i(lambda_i)/A_body projection lies below R10, orbital and PPN bounds | R10 \|alpha_X(lambda)\|<=alpha_bound(lambda); orbital \|Delta a/a_N\|=\|alpha\|(1+r/lambda)exp(-r/lambda); Hessian profile H_R formula | FINITE_RANGE_SCORE_SHAPE_READY_INPUTS_UNSIGNED | False | 2026-07-07T18:19:21+00:00 |

## Finite-Range Profile Law

| checkpoint | profile_id | target | formula | zero_condition | needed_inputs | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | FR4682_0_standard_yukawa | curvature-square weak-field potential | Phi/Phi_N = 1 + sum_i alpha_i exp(-M_i r) | all alpha_i=0 or M_i L_arena >> 1 with source-backed lower M_i | alpha_i;M_i;arena radius;source/test projection;no-cancellation convention | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | FR4682_1_standard_R2_scalaron | R2/fR scalaron | R(r)=A_body exp(-m_R r)/r; H_R=\|A_body\| exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3) | c_R2_eff_total=0 or A_body=0 | A_body;m_R;MTS-to-mu normalization;screening/source convention | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | FR4682_2_hidden_memory_fibre | integrated-out memory/fibre scalar contribution | Delta c_R2_hidden = 0.5 B^T L^-1 B; if L>0 then zero iff B=0 | B_mem=B_h=0 on physical quotient plus source/boundary charge silence | Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;Z_h;M2_h;B_h;C_h;J_h;Q_boundary_h | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | FR4682_3_anchor_only_short_range | Eot-Wash alpha=1 anchor | lambda < 38.6 um for alpha approx 1; M > 0.0051121 eV for a single gravitational-strength Yukawa | not a zero theorem; anchor only | claim-grade alpha(lambda) curve and MTS alpha_i(lambda_i) projection | False | False | 2026-07-07T18:19:21+00:00 |

## R10 / Orbital / PPN Bound Interface

| checkpoint | bound_id | arena | formula | status | missing_inputs | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | B4682_0_R10_curve | R10 short-range inverse-square tests | \|alpha_X(lambda)\| <= alpha_bound(lambda) | FULL_CURVE_AND_MTS_PROJECTION_REQUIRED | claim-grade alpha_bound(lambda); alpha_X mapping; lambda_X; source/test charges; units | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | B4682_1_R10_anchor | R10 alpha=1 anchor | lambda<38.6um -> M>0.0051121eV for alpha=1 single-Yukawa | ANCHOR_ONLY_NONCLAIM | not valid for non-alpha=1 or multi-channel MTS projection without curve | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | B4682_2_orbital_large_lambda | orbital/inverse-square acceleration | \|Delta a/a_N\|=\|alpha\|(1+r/lambda)exp(-r/lambda) | FORMULA_READY_VALUES_UNSIGNED | alpha; lambda; arena radius; ephemeris/orbital threshold; projection convention | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | B4682_3_PPN_scalaron | PPN beta/gamma scalaron branch | standard template: mu <= 1.443476e15 m^2 and lambda_R <= 9.306372e7 m only if MTS-to-f(R) map is signed | STANDARD_TEMPLATE_READY_MTS_NORMALIZATION_UNSIGNED | N_MTS_to_fR; c_R2_eff_total; A_body/screening; source convention | False | False | 2026-07-07T18:19:21+00:00 |

## cR2 Exit Conditions

| checkpoint | exit_id | exit_route | condition | current_status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | EXIT4682_0_parent_no_extra_mode | parent two-derivative/no-extra-light-mode selector | all curvature-square propagating coefficients absent | PARENT_SELECTOR_UNSIGNED | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | EXIT4682_1_componentwise_zero | componentwise c_R2_eff_total zero | c_cell,c_bare,c_measure,c_boundary,c_marker and B_X all zero, or named identity | ZERO_COMPONENTS_UNSIGNED | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | EXIT4682_2_body_charge_zero | scalaron/body-charge zero | Q_X[body]+Q_boundary=0 under selected Green function | BODY_CHARGE_UNSIGNED | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | EXIT4682_3_heavy_mass_gap | parent heavy scale | M_i L_arena >> 1 with sourced M_i lower bound | MASS_GAP_UNSIGNED | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | EXIT4682_4_finite_bound | finite R10/orbital/PPN bound | source-backed alpha(lambda)/A_body below arena bounds | BOUND_INTERFACE_READY_VALUES_MISSING | False | False | 2026-07-07T18:19:21+00:00 |

## Survivor Update

| checkpoint | survivor_id | residual_family | status_after_4682 | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | SURV4682_0_EH_principal | EH principal / public parent adoption | still public blocker | retain parent selector/adoption gate | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SURV4682_1_cGamma | c_Gamma local memory coupling | unchanged finite survivor | derive memory support/projector zero or source profile coefficients | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SURV4682_2_cR2_MR | c_R2/M_R finite-range curvature-square branch | reduced to extra-mode zero, componentwise c_R2_eff_total zero, body-charge zero, heavy mass gap or finite source-backed bound | 4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SURV4682_3_memory_fibre_BC | memory/fibre B,C,J,boundary owners | selected next owner/zero-switch target | 4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | SURV4682_4_material_projection_global | Lambda/material/projection/global parent | unchanged blocker | keep promotion firewall active | False | False | 2026-07-07T18:19:21+00:00 |

## Controls

| checkpoint | control_id | rule | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4682 | CTRL4682_0 | Do not use the alpha=1 anchor as a full c_R2/M_R proof. | ACTIVE | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | CTRL4682_1 | Do not use exterior source-free language to erase body charge. | ACTIVE | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | CTRL4682_2 | Do not allow cancellation between c_cell, c_bare, B^T L^-1 B, measure, boundary and marker pieces. | ACTIVE | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | CTRL4682_3 | Positive L_X helps only after B_X/C_X/J_X/Q_boundary_X source silence is signed or bounded. | ACTIVE | False | False | 2026-07-07T18:19:21+00:00 |
| 4682 | CTRL4682_4 | Move next to memory/fibre B,C,J,boundary owner rows rather than looping c_R2 labels. | ACTIVE | False | False | 2026-07-07T18:19:21+00:00 |

## Decision

| checkpoint | decision | summary | next_target | public_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4682 | CR2_MR_REDUCED_TO_EXTRA_MODE_ZERO_COMPONENTWISE_BODY_CHARGE_OR_FINITE_RANGE_BOUND_CURRENT_BRANCH_NONCLAIM | 4682 imports the 4594 c_R2/M_R finite-range ladder into the current branch after torsion narrowing. The branch now has exact exits: parent no-extra-mode selector, componentwise c_R2_eff_total zero, body-charge zero, heavy parent mass gap, or finite R10/orbital/PPN bound. Positive memory/fibre operators do not erase B_X source vertices; the next target is the memory/fibre B,C,J,boundary owner zero-switch or first body-charge coefficient row. | 4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | False | False | 2026-07-07T18:19:21+00:00 |

## Status

| checkpoint | marker | claim_id | decision | cR2_status | strict_zero_exits | finite_bound_exits | next_owner_target | local_GR_public_claim | remaining_broad_survivors | next_target | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | PPC4161_CR2_MR_FINITE_RANGE_GATE_CURRENT_BRANCH_4682 | L-524 | CR2_MR_REDUCED_TO_EXTRA_MODE_ZERO_COMPONENTWISE_BODY_CHARGE_OR_FINITE_RANGE_BOUND_CURRENT_BRANCH_NONCLAIM | finite-range extra-mode/body-charge gate | two_derivative_selector;c_R2_eff_total=0;A_body=0;M_i L_arena>>1 | R10_alpha_curve;orbital_acceleration;PPN_scalaron;Hessian_AE | memory/fibre B,C,J,Q_boundary zero switch | False | EH_public_adoption;cGamma;memory_fibre_BC_source_charge;Lambda_material_projection;global_parent | 4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | False | 2026-07-07T18:19:21+00:00 |

## Next Target

| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4682 | NT4682_0 | 4683-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md | c_R2/M_R has been reduced to finite-range/body-charge exits; the live pressure is now memory/fibre B,C,J,boundary source owners. | parent-sign B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 and B_h=C_h=J_h=Q_boundary_h=0 from object-language/action-inventory exclusion | fill the first body-charge coefficient row: Z_X, M_X^2, B_X, C_X, J_X, Q_boundary_X and R10/PPN/orbital projection | False | 2026-07-07T18:19:21+00:00 |

## Validation

| checkpoint | check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4682 | VAL4682_0_sources_exist | True | all source-register paths exist | False |
| 4682 | VAL4682_1_needles_found | True | all source-register needles found | False |
| 4682 | VAL4682_2_componentwise_zero | True | componentwise cR2 zero law present | False |
| 4682 | VAL4682_3_body_charge_law | True | body-charge zero/bound law present | False |
| 4682 | VAL4682_4_finite_profiles | True | finite-range profile rows present | False |
| 4682 | VAL4682_5_bound_interfaces | True | R10/orbital/PPN bound interfaces present | False |
| 4682 | VAL4682_6_exit_conditions | True | five cR2 exit routes written | False |
| 4682 | VAL4682_7_next_memory_fibre | True | next memory/fibre target selected | False |
| 4682 | VAL4682_8_claim_row_exists | True | claims register contains L-524 | False |
| 4682 | VAL4682_9_formal_doc | True | formal doc exists with marker | False |
| 4682 | VAL4682_10_post_doc | True | post checkpoint exists with marker | False |
| 4682 | VAL4682_11_spine_marker | True | spine marker written | False |
| 4682 | VAL4682_12_packet_marker | True | packet marker written | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_SOURCE_REGISTER | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_SOURCE_REGISTER.csv parses with 16 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_CR2_ZERO_BOUND_THEOREM_IMPORT | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_CR2_ZERO_BOUND_THEOREM_IMPORT.csv parses with 5 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_FINITE_RANGE_PROFILE_LAW | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_FINITE_RANGE_PROFILE_LAW.csv parses with 4 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_R10_ORBITAL_BOUND_INTERFACE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_R10_ORBITAL_BOUND_INTERFACE.csv parses with 4 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_CR2_EXIT_CONDITIONS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_CR2_EXIT_CONDITIONS.csv parses with 5 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_SURVIVOR_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_SURVIVOR_UPDATE.csv parses with 5 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_CONTROL_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_CONTROL_ROWS.csv parses with 5 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_DECISION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_DECISION.csv parses with 1 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_STATUS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_STATUS.csv parses with 1 rows | False |
| 4682 | VAL4682_csv_P8_Y5_R2FR_4682_NEXT_TARGET | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4682_NEXT_TARGET.csv parses with 1 rows | False |
| 4682 | VAL4682_13_no_claim_rows_true | True | generated rows keep valid_for_claim false | False |
| 4682 | VAL4682_14_pycache_absent | True | scripts __pycache__ absent | False |
| 4682 | VAL4682_OVERALL | True | PASS | False |
