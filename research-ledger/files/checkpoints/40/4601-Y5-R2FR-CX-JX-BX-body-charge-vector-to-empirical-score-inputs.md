# 4601 Y5 R2FR C_X/J_X/B_X body-charge vector to empirical score inputs

Private checkpoint generated at `2026-07-06T14:47:01.173783+00:00`.

Marker: `PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601`
Branch: `MTS_R2FR_Y5_BODY_CHARGE_SCORE_INPUT_INTERFACE_4601`
Decision: `BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_NONCLAIM`
Claim register: `L-443`

## Result

4601 turns the 4595-4600 body-charge work into an empirical score-input interface. The local branch is now organized as:

```text
(-Z_X nabla^2 + M_X^2) delta_X = rho_X,
rho_X = B_X R_obs + C_X^final_live T + J_X^live,
lambda_X = sqrt(Z_X/M_X^2),
|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|).
```

The scoring vector is sector separated:

```text
memory: Z_mem, M2_mem, lambda_mem, B_mem_eff, C_mem^final_live,
        J_mem_live, Q_boundary_mem, W_mem/body profile;

fibre:  Z_h, M2_h, lambda_h, B_h, C_h^final_live,
        J_h_live, Q_boundary_h, W_h/body profile.
```

And arena separated:

```text
R10, PPN/local-GR, clock/WEP, orbital/GM, EM/Poynting.
```

No prediction is made. The useful advance is that a future runner now has a strict schema and a blocker ledger: if a row does not have parent-owned/theorem-zero or source-backed numeric values, it cannot become a claim.

The next best target is `4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md`, because `Z_X`, `M_X^2` and `lambda_X` are the first hard gate before any amplitude or alpha score can be honest.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | SRC4601_00_4600_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md | True | C_X^final_live | True | 34 | 4600 final C_X handoff. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_01_616_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\616-PPC4161-boundary-nonHilbert-zero-or-final-CXlive-norm.md | True | C_X^final_live | True | 27 | formal 4600 final C_X statement. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_02_4600_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_NEXT_TARGET.csv | True | 4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md | True | 2 | machine-readable 4600 next target. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_03_4600_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_STATUS.csv | True | B_X/J_X/Q_boundary/Z_X/M_X^2 arena scoring | True | 2 | 4600 names missing body-charge scoring. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_04_4600_body | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv | True | BU4600_1_memory | True | 3 | final C_X in A_mem. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_05_4600_interface | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_EMPIRICAL_SCORE_INPUT_INTERFACE.csv | True | E4600_0_R10 | True | 2 | arena interface handoff. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_06_4600_final_cx | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv | True | C4600_4_final | True | 6 | final C_X norm row. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_07_4595_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_FINITE_INPUT_SCHEMA.csv | True | schema4595_0_memory_Z | True | 2 | finite input schema. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_08_4595_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv | True | ZS4595_0_common_operator | True | 2 | common zero switch. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_09_4595_mem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv | True | MEM4595_2_amplitude | True | 4 | memory amplitude law. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_10_4595_fib | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_FIBRE_BODY_CHARGE_BOUND.csv | True | FIB4595_2_amplitude | True | 4 | fibre amplitude law. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_11_4595_bmem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4595_BMEM_EFF_INSERTION.csv | True | BM4595_5_combined | True | 7 | B_mem_eff source vector. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_12_4596_jlive | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv | True | J4596_5_live_total | True | 7 | J_X live vector. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_13_4596_coeff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv | True | CO4596_6_Qboundary | True | 8 | first body-charge coefficient rows. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_14_4597_cx | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv | True | CX4597_7_live_total | True | 9 | C_X live vector ancestry. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_15_4506_body | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv | True | BCIN4506_2_zero_switch | True | 4 | body-charge input row. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_16_4505_green | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv | True | BC4505_2_absolute_bound | True | 4 | Green-function amplitude bound. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_17_4514_insert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv | True | BCB4514_5_arena | True | 7 | arena projection missing. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_18_4514_vector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv | True | BMV4514_6_combined | True | 8 | B_mem effective component vector. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_19_4515_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4515_SOURCE_COUPLING_BOUND.csv | True | SB4515_2_amplitude | True | 4 | source-coupling amplitude bound. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_20_4523_alpha_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4523_FIRST_ALPHA_RUNNER_INPUTS.csv | True | AIR4523_0_Z | True | 8 | alpha runner input blockers. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_21_4524_alpha_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4524_RESIDUAL_ALPHA_INPUT_CONTRACT.csv | True | RAI4524_4_mass_range | True | 6 | residual alpha contract. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_22_4524_alpha_law | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4524_FINITE_RESIDUAL_ALPHA_LAW.csv | True | FRA4524_4_finite_range_mode | True | 6 | finite range alpha law. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_23_4594_R10 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4594_R10_ORBITAL_BOUND_INTERFACE.csv | True | B4594_0_R10_curve | True | 2 | R10 bound interface. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_24_4592_PPN | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4592_PPN_VECTOR_IMPACT_ROWS.csv | True | PPN4592_7_R10_clock_WEP_orbital | True | 9 | PPN side arena survivors. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_25_4447_PPN | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_OUTPUT.csv | True | PPN4447_1_gamma_minus_1_source_norm | True | 3 | PPN residual output. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_26_4530_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4530_BOUNDARY_POYNTING_SPLIT.csv | True | B4530_2_radiative_poynting_flux | True | 4 | Poynting routing. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_27_4583_EM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4583_CHARGE_CURRENT_EM_READOUT_OWNER_THEOREM.csv | True | CCO4583_4_open_dynamic_bound | True | 6 | EM dynamic bound schema. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_28_4486_M2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv | True | M2I4486_3_recast_hessian_product_bound | True | 5 | first M2/Hessian finite scorer input. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_29_4475_lambda | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4475_LAMBDAM_SOURCE_ROW.csv | True | LMR4475_1_lambda_M | True | 3 | lambda/range source row. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_30_4476_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4476_LAMBDAM_PROJECTION_MAP.csv | True | PMAP4476_0_universal_projection | True | 2 | projection map template. | 2026-07-06T14:47:01.173783+00:00 | False |
| 4601 | SRC4601_31_claim_442 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-442 | True | 457 | claim-register handoff from 4600. | 2026-07-06T14:47:01.173783+00:00 | False |

## Field Operator Inputs

| checkpoint | operator_id | sector | field_equation | source_density | range_law | amplitude_bound | zero_switch | current_status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | OP4601_0_common | common_X | (-Z_X nabla^2 + M_X^2) delta_X = rho_X | rho_X = B_X R_obs + C_X^final_live T + J_X^live | lambda_X=sqrt(Z_X/M_X^2) | \|A_X\| <= [exp(R_body/lambda_X) int_body \|rho_X\| dV + \|Q_boundary_X\|]/(4*pi \|Z_X\|) | Z_X>0, M_X^2>0, zero modes removed, and B_X=C_X^final_live=J_X^live=Q_boundary_X=0 in the same parent branch | DERIVED_STRUCTURE_VALUES_MISSING | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | OP4601_1_memory | memory | (-Z_mem nabla^2 + M2_mem) delta_m = rho_mem | rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live | lambda_mem=sqrt(Z_mem/M2_mem) | \|A_mem\| <= [exp(R_body/lambda_mem) int_body (\|B_mem_eff\|\|R_obs\|+\|C_mem^final_live\|\|T\|+\|J_mem_live\|) dV + \|Q_boundary_mem\|]/(4*pi \|Z_mem\|) | B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0 plus positive L_mem | MEMORY_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | OP4601_2_fibre | fibre | (-Z_h nabla^2 + M2_h) delta_h = rho_h | rho_h = B_h R_obs + C_h^final_live T + J_h_live | lambda_h=sqrt(Z_h/M2_h) | \|A_h\| <= [exp(R_body/lambda_h) int_body (\|B_h\|\|R_obs\|+\|C_h^final_live\|\|T\|+\|J_h_live\|) dV + \|Q_boundary_h\|]/(4*pi \|Z_h\|) | B_h=C_h^final_live=J_h_live=Q_boundary_h=0 plus positive L_h | FIBRE_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING | False | 2026-07-06T14:47:01.173783+00:00 |

## Body-Charge Score Vector

| checkpoint | component_id | sector | symbol | role | source_anchor | required_for_claim | score_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | BCV4601_00 | memory | Z_mem | operator normalization | 4595 schema4595_0_memory_Z;4506 BCIN4506_0_memory_density | positive numeric/source-backed value or theorem normalization | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_01 | memory | M2_mem | operator mass gap | 4595 schema4595_1_memory_M2;4524 RAI4524_4_mass_range | positive numeric/source-backed value; lambda_mem convention | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_02 | memory | lambda_mem | range | lambda_mem=sqrt(Z_mem/M2_mem) | derived from Z_mem/M2_mem with units | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_03 | memory | B_mem_eff | curvature/source-normalization source vector | 4595 BM4595_5_combined;4514 BMV4514_6_combined | component zeros or absolute B vector values | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_04 | memory | C_mem^final_live | matter-trace coupling | 4600 BU4600_1_memory;4600 C4600_4_final | all C subblocks zero or source-backed norms | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_05 | memory | J_mem_live | direct/Poynting/non-Hilbert current | 4596 J4596_5_live_total | zero certificate or flux/current profile | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_06 | memory | Q_boundary_mem | Green boundary charge | 4595 schema4595_5_memory_boundary;4600 BU4600_3_boundary_separation | no-flux/topological theorem or finite boundary integral | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_07 | memory | W_mem/body profile | body profile and screening kernel | 4505 BC4505_2_absolute_bound;4514 BCB4514_3_amplitude | body radius/profile/source units | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_08 | fibre | Z_h | operator normalization | 4595 schema4595_6_fibre_Z;4506 BCIN4506_1_fibre_density | positive numeric/source-backed value or theorem normalization | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_09 | fibre | M2_h | operator mass gap | 4595 schema4595_7_fibre_M2;4524 RAI4524_4_mass_range | positive numeric/source-backed value; lambda_h convention | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_10 | fibre | lambda_h | range | lambda_h=sqrt(Z_h/M2_h) | derived from Z_h/M2_h with units | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_11 | fibre | B_h | curvature/source fibre source vector | 4595 schema4595_8_fibre_B | parent action exclusion or finite coefficient | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_12 | fibre | C_h^final_live | matter-trace fibre coupling | 4600 BU4600_2_fibre;4600 C4600_4_final | all C subblocks zero or source-backed norms | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_13 | fibre | J_h_live | direct/Poynting/non-Hilbert fibre current | 4596 J4596_5_live_total | zero certificate or flux/current profile | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_14 | fibre | Q_boundary_h | Green boundary charge | 4595 schema4595_11_fibre_boundary;4600 BU4600_3_boundary_separation | no-flux/topological theorem or finite boundary integral | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | BCV4601_15 | fibre | W_h/body profile | body profile and screening kernel | 4505 BC4505_2_absolute_bound;4595 FIB4595_2_amplitude | body radius/profile/source units | MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Arena Score Matrix

| checkpoint | arena_id | arena | observable_target | score_law | required_inputs | acceptance_gate | score_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | ASM4601_0 | R10 | short-range inverse-square | alpha_X(lambda_X) from A_X or K_R10_X Qbar_XS qbar_XT/(G_N M_S m_T M_X^2) | Z_X;M_X^2;lambda_X;B_X;C_X^final_live;J_X_live;Q_boundary_X;K_R10_X;Qbar_XS;qbar_XT;alpha_bound(lambda) | full source-backed alpha(lambda) curve and MTS projection convention | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | ASM4601_1 | PPN | gamma,beta,alpha_i,xi,zeta_i,Gdot | Delta p_i <= sum_X \|\|K_iX\|\| \|A_X\| + direct_tail_i | A_X vector;K_gamma,K_beta,K_alpha_i,K_xi,K_zeta,K_Gdot;EH principal block;survivor tails | compare against GR baseline and PPN limits without absorbing into fitted G/GM | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | ASM4601_2 | clock_WEP | clock redshift, WEP eta, material universality | Delta O <= K_C C_X^final_live + K_shadow E_shadow_projector + K_std C_X^std_weight_live + material_tail | material sensitivities;clock kernels;source/test composition;standard/weight rows;shadow rows | source-backed material coefficients and same-frame calibration | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | ASM4601_3 | orbital_GM | orbital acceleration/light-time/GM transfer | Delta a/a_N = alpha_X (1+r/lambda_X) exp(-r/lambda_X) plus boundary/reference drift terms | alpha_X;lambda_X;Q_boundary_X;Delta_symp_X;J_boundary_X;GM calibration rule;orbital threshold | no absorption into fitted GM unless a separate nuisance/control branch is declared | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | ASM4601_4 | EM_Poynting | EM stress, Poynting flux, alpha_EM/current owner | Delta O_EM <= K_EM(\|J_X^EM_open\|+\|Delta_Hodge_EM_X\|+\|Phi_EM_rad\|+\|C_XF2\|+\|b_alpha\|) | same-Hodge/current owner;closed collar or Poynting flux profile;EM readout tail;units | stationary no-flux theorem or sourced radiative/open-flux profile | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Missing Input Ledger

| checkpoint | missing_id | missing_input | required_evidence | priority | current_status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | MIS4601_0_operator_range | Z_X,M_X^2,lambda_X | parent quadratic operator/eigenvalue with unit convention | 4602 target | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_1_body_source_vector | B_X,C_X^final_live,J_X_live,Q_boundary_X | component zero certificates or finite source-backed values | after range owner | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_2_body_profile | R_body,R_obs,T,W_X,screening | body/source profile in declared units | before any numeric amplitude | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_3_source_test_charges | Qbar_XS,qbar_XT,M_S,m_T,G_N | same-frame source/test charge and calibration convention | before R10 alpha | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_4_arena_kernels | K_R10,K_PPN,K_clock,K_orbit,K_EM | transfer operators with dimensions and baseline convention | before scoring | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_5_external_bounds | alpha_bound(lambda),PPN/clock/orbital thresholds | source-backed bounds or official tables | before pass/fail claim | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_6_EM_flux | Phi_EM_rad,Delta_Hodge_EM,C_XF2,b_alpha | stationary no-flux theorem or finite EM/Poynting profile | before EM branch scoring | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | MIS4601_7_no_cancellation | component signs/correlation | parent-owned cancellation if not using absolute sums | default absolute envelope | MISSING_BLOCKS_CLAIM | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Nonclaim Runner Schema

| checkpoint | column_id | column_name | type | meaning | required_before_claim | schema_status | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | RS4601_00 | run_id | string | unique run tag | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_01 | sector | enum(memory,fibre) | which X sector is scored | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_02 | arena | enum(R10,PPN,clock_WEP,orbital_GM,EM_Poynting) | test arena | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_03 | Z_X | numeric_or_THEOREM_ZERO | operator normalization | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_04 | M2_X | numeric_or_THEOREM_ZERO | operator mass gap | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_05 | lambda_X | numeric | range in declared units | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_06 | B_X_norm | numeric_or_zero_certificate | curvature/source vector norm | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_07 | C_X_final_norm | numeric_or_zero_certificate | final matter-trace coupling norm | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_08 | J_X_live_norm | numeric_or_zero_certificate | live current norm | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_09 | Q_boundary_X_norm | numeric_or_zero_certificate | Green boundary charge norm | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_10 | K_arena | numeric_or_matrix | arena transfer kernel | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_11 | source_charge | numeric_or_zero_certificate | source body charge | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_12 | test_charge | numeric_or_zero_certificate | test body charge | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_13 | calibration | string_with_units | G_N/GM/source convention | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_14 | bound_reference | source_path_or_url | empirical bound source | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_15 | predicted_value | numeric | computed residual or alpha | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_16 | units | string | units for every numeric input | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_17 | source_paths | semicolon_paths | local/web provenance | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_18 | valid_for_claim | boolean | true only when all numeric/theorem/source conditions pass | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | RS4601_19 | blockers | semicolon_strings | missing fields if invalid | True | REQUIRED_COLUMN | False | 2026-07-06T14:47:01.173783+00:00 |

## Controls

| checkpoint | control_id | input_branch | expected | status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | CTRL4601_placeholder_block | any score row uses MISSING, placeholder, inferred-from-bound, or unsourced numeric values | valid_for_claim remains false and claim_allowed remains false | GUARD_ACTIVE | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | CTRL4601_range_first | B/C/J/Q values are proposed but Z_X,M_X^2,lambda_X are missing | amplitude and R10 scoring remain blocked | COUNTERMODEL_CAUGHT | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | CTRL4601_GM_absorption | orbital or PPN residual is hidden inside fitted G/GM without a declared nuisance comparison | score row rejected; calibration must be explicit | GUARD_ACTIVE | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | CTRL4601_Poynting_firewall | Poynting/EM flux is set to zero by convention rather than same-Hodge closed-collar theorem | EM_Poynting and J_X_live rows stay open | COUNTERMODEL_CAUGHT | False | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | CTRL4601_no_cancellation | B,C,J,Q terms cancel numerically without a parent signed relation | absolute-sum bound used; no cancellation credit | GUARD_ACTIVE | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Promotion Gates

| checkpoint | gate_id | claim | passed | detail | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4601 | PROM4601_0_sources_exist | all cited source paths exist | True | source register path check | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | PROM4601_1_needles_found | all cited source needles found | True | source register needle check | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | PROM4601_2_two_sectors | memory and fibre score vectors both emitted | True | sector-separated rows for memory and fibre | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | PROM4601_3_five_arenas | R10/PPN/clock/orbital/EM arena rows emitted | True | arena score matrix has five rows | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | PROM4601_4_runner_schema | nonclaim runner schema emitted | True | future numeric row has required columns and blockers | False | 2026-07-06T14:47:01.173783+00:00 |
| 4601 | PROM4601_5_no_claim | no empirical pass emitted | True | interface only; values and source-backed bounds remain missing | False | 2026-07-06T14:47:01.173783+00:00 |

## Decision

| checkpoint | branch | marker | claim_id | decision | score_vector_ready | arena_matrix_ready | runner_schema_ready | numeric_prediction_present | empirical_pass_claimed | next_target | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | MTS_R2FR_Y5_BODY_CHARGE_SCORE_INPUT_INTERFACE_4601 | PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601 | L-443 | BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_NONCLAIM | True | True | True | False | False | 4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | next_target | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601 | L-443 | BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_NONCLAIM | sector-separated body-charge score vector; field operator/range/amplitude law; R10/PPN/clock/orbital/EM arena score matrix; missing-input ledger; nonclaim runner schema | numeric Z_X/M_X^2/lambda_X; numeric or theorem-zero B_X,C_X,J_X,Q_boundary_X; source/test charges; arena kernels; external bound comparisons; local-GR/R10/PPN pass | PRIVATE_NONCLAIM | 4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md | False | False | 2026-07-06T14:47:01.173783+00:00 |

## Next Target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4601 | MTS_R2FR_Y5_BODY_CHARGE_SCORE_INPUT_INTERFACE_4601 | 2026-07-06T14:47:01.173783+00:00 | 4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md | The score interface shows the first hard blocker is not B/C/J bookkeeping but the operator/range owner: without Z_X,M_X^2 and lambda_X no body-charge amplitude or R10/PPN projection is scoreable. | derive parent quadratic operator normalization, mass gap and range for memory/fibre sectors in the same quotient domain | emit the first nonclaim source row for Z_X,M_X^2,lambda_X with explicit units and blockers | False |
