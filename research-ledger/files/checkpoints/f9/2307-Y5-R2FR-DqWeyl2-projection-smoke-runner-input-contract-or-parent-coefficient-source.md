# 2307 — D_qWeyl2 Projection Smoke-Runner Input Contract Or Parent Coefficient Source

## Summary

2307 turns the 2306 Weyl-squared projection into a runner contract. It does not claim a physical bound. The parent coefficient `D_qWeyl2`, the q Green operator/normalization `Z_q`, and the observable projection `P_arena[q]` are still missing.

What is now concrete is the plumbing: given a finite source mass and radius, compute `mu=GM/c^2`, `K_C2_ext=64*pi*mu^2/R_body^3`, and a massless far-field scaffold `q(r)=D_qWeyl2*K_C2_ext/(4*pi*Z_q*r)`. The dry-run table proves the kernel calculation works, while every row remains nonclaim.

## Source Register

| row_id | source_key | source_path | exists | needles_found | source_role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC2307_00_2306_doc | 2306_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md | true | true | direct 2306 handoff | false |
| SRC2307_01_2306_validation | 2306_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2306_VALIDATION.csv | true | true | 2306 validation | false |
| SRC2307_02_2306_projection | 2306_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2306_SCHWARZSCHILD_WEYL2_PROJECTION_LAW.csv | true | true | Weyl2 projection law | false |
| SRC2307_03_2306_bound | 2306_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW.csv | true | true | first bound row with missing parent coefficient | false |
| SRC2307_04_2306_arena | 2306_arena | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2306_ARENA_PROJECTION_REQUIREMENTS.csv | true | true | arena projection missing | false |
| SRC2307_05_2132_no_tower | 2132_no_tower | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2132_NO_TOWER_THEOREM_ATTEMPT.csv | true | true | no-tower theorem not derived | false |
| SRC2307_06_963_doc | 963_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md | true | true | second-order parent signature not signed | false |
| SRC2307_07_1343_doc | 1343_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md | true | true | higher-curvature zero signature not derived | false |
| SRC2307_08_2135_doc | 2135_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md | true | true | curvature coefficient morphism remains live | false |
| SRC2307_09_2301_residuals | 2301_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv | true | true | q curvature residual schema missing values | false |
| SRC2307_10_2304_refusal | 2304_refusal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2304_REFUSAL_RUNNER.csv | true | true | earlier arena projection refusal | false |
| SRC2307_11_1235_requirements | 1235_requirements | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv | true | true | readout/radiative closure unsigned | false |

## Parent Coefficient Source Hunt

| row_id | target | hunt_result | evidence | required_source | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HUNT2307_0_DqWeyl2 | D_qWeyl2 parent coefficient | NOT_FOUND_CURRENT_CORPUS | 2306 bound row still reports MISSING_PARENT_COEFFICIENT; 1343 and 2132 keep no-tower/no-higher-curvature unsigned | parent action term or theorem-zero row with normalization and sign | run only symbolic/nonclaim smoke contract | false |
| HUNT2307_1_Lq | q Green operator L_q or G_q | NOT_FOUND_CURRENT_CORPUS | 2306 bound row reports MISSING_Q_GREEN_OPERATOR | kinetic normalization, mass/Yukawa scale, boundary conditions, sign convention | keep massless/Yukawa formulas as branches, not evidence | false |
| HUNT2307_2_Pobs | observable projection P_arena[q] | NOT_FOUND_CURRENT_CORPUS | 2306 arena matrix and 2304 refusal both block orbital/PPN/clock/R10 projections | map q profile into acceleration, metric potentials, clock/alpha shifts, or R10 alpha(lambda) | dry-run only produces source kernel, not observable residual | false |
| HUNT2307_3_verdict | execute claim-grade D_qWeyl2 runner | BLOCKED | coefficient, operator, body model, and observable map are not all source-backed | HUNT2307_0 through HUNT2307_2 must become sourced numeric/theorem rows | nonclaim smoke runner input contract and symbolic dry run | false |

## Smoke-Runner Input Contract

| row_id | field | required | units | role | claim_requirement | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IN2307_0_source_mass | M_source | true | kg | sets mu=GM/c^2 | source-backed body catalogue for claim-grade run | DRYRUN_CAN_ACCEPT_NUMERIC | false |
| IN2307_1_source_radius | R_body | true | m | finite-size cutoff for integral 64*pi*mu^2/R_body^3 | interior/regularity prescription, not point-particle shortcut | DRYRUN_CAN_ACCEPT_NUMERIC | false |
| IN2307_2_DqWeyl2 | D_qWeyl2 | true | parent_normalized | multiplies q C^2 source | parent-sourced coefficient or theorem-zero | MISSING_PARENT_COEFFICIENT | false |
| IN2307_3_Zq | Z_q | true | parent_normalized | q kinetic/operator normalization | source-backed q operator | MISSING_Q_OPERATOR | false |
| IN2307_4_lambda_q | lambda_q | branch_optional | m | Yukawa/range branch for massive q operator | mass/range from parent Hessian or data prior | MISSING_Q_RANGE | false |
| IN2307_5_Pobs | P_arena | true_for_observable_claim | arena_specific | maps q profile to PPN/orbital/R10/clock observable | source-backed arena projection | MISSING_OBSERVABLE_MAP | false |
| IN2307_6_sign_boundary | sign_and_boundary_condition | true | symbolic | fixes whether q solves +Lq q=S or -Lq q=S and boundary/tail terms | parent variational sign convention and boundary term | MISSING_PARENT_CONVENTION | false |

## Projection Algebra

| row_id | symbol | formula | units | status | claim_note | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| ALG2307_0_mu | mu | mu=G*M_source/c^2 | m | READY | uses GR background as projection scaffold, not proof of MTS local GR | false |
| ALG2307_1_C2 | C2(r) | 48*mu^2/r^6 | m^-4 | READY | Schwarzschild exterior identity | false |
| ALG2307_2_integrated_kernel | K_C2_ext | 64*pi*mu^2/R_body^3 | m^-1 | READY | finite-radius source kernel; diverges for R_body -> 0 | false |
| ALG2307_3_massless_q_far | q_far_massless | q(r)=D_qWeyl2*K_C2_ext/(4*pi*Z_q*r)=16*D_qWeyl2*mu^2/(Z_q*R_body^3*r) | depends_on_D_and_Zq | FORMULA_READY_INPUTS_MISSING | requires q operator normalization and observable projection | false |
| ALG2307_4_yukawa_far | q_far_yukawa | q(r)≈D_qWeyl2*K_C2_ext*exp(-(r-R_body)/lambda_q)/(4*pi*Z_q*r) for far-field/profile approximation | depends_on_D_and_Zq | APPROX_BRANCH_INPUTS_MISSING | massive branch needs full finite-profile Green function for claim-grade work | false |
| ALG2307_5_observable | O_arena | O_arena=P_arena[q(r),grad q(r),metric backreaction,readout] | arena_specific | MISSING_OBSERVABLE_MAP | no R10/PPN/orbital/clock claim until P_arena is parent-sourced | false |

## Projection Smoke Dry-Run

| row_id | source_label | mass_kg | radius_m | mu_m | K_C2_ext_m_inv | q_prefactor_at_1m_per_D_over_Zq | status | claim_blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DRY2307_0_earth | Earth_illustrative | 5.97220000e+24 | 6.37100000e+06 | 4.43505144e-03 | 1.52934108e-23 | 1.21701096e-24 | DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE | D_qWeyl2, Z_q, interior model, and P_arena missing | false |
| DRY2307_1_sun | Sun_illustrative | 1.98847000e+30 | 6.95700000e+08 | 1.47666969e+03 | 1.30205868e-18 | 1.03614538e-19 | DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE | D_qWeyl2, Z_q, interior model, and P_arena missing | false |
| DRY2307_2_lab_1kg_5cm | lab_1kg_5cm_illustrative | 1.00000000e+00 | 5.00000000e-02 | 7.42616027e-28 | 8.87050754e-49 | 7.05892561e-50 | DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE | D_qWeyl2, Z_q, interior model, and P_arena missing | false |

## Claim Gates

| row_id | gate | passed | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE2307_0_sources | source paths and needles valid | true | ledger is checkable | false |
| GATE2307_1_coefficient_hunt | parent coefficient/source hunt performed | true | missing D_qWeyl2 is explicit | false |
| GATE2307_2_runner_contract | smoke-runner input contract written | true | future testing inputs are concrete | false |
| GATE2307_3_dryrun_kernel | dry-run kernel table finite and positive | true | plumbing can compute projection kernels | false |
| GATE2307_4_claim_inputs | D_qWeyl2, Z_q, P_arena, and body model source-backed | false | no local bound claim | false |
| GATE2307_5_local_claim | R10/PPN/orbital/clock/local-GR claim allowed | false | all public claims remain blocked | false |

## Refusal Runner

| row_id | claim | allowed | reason | blocking_rows | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| REF2307_0_dryrun_claim | dry-run table is physical evidence | false | dry-run uses illustrative source constants and omits D_qWeyl2/Z_q/P_arena | HUNT2307_0_DqWeyl2;HUNT2307_1_Lq;HUNT2307_2_Pobs | false |
| REF2307_1_bound_claim | D_qWeyl2 passes local bound | false | runner contract is ready but claim-grade inputs are missing | IN2307_2_DqWeyl2;IN2307_3_Zq;IN2307_5_Pobs;IN2307_6_sign_boundary | false |
| REF2307_2_GR_claim | MTS reduces to local GR/Newton | false | this only builds one higher-curvature projection scaffold; EH/source descent and Newtonian limit remain open | GATE2307_4_claim_inputs;GATE2307_5_local_claim | false |

## Decision Ledger

| row_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2307_0 | PARENT_COEFFICIENT_NOT_FOUND | no current source signs D_qWeyl2 or Z_q; no-tower route remains unsigned | keep D_qWeyl2 as nonclaim residual | false |
| DEC2307_1 | SMOKE_CONTRACT_READY | mass/radius to C2 kernel to q-profile formulas are now explicit and machine-readable | when coefficient/operator assumptions exist, convert contract into executable nonclaim runner | false |
| DEC2307_2 | BEST_NEXT_TARGET_IS_SOURCE_DESCENT_OR_DQWEYL2_COEFFICIENT | the projection side is no longer the bottleneck; the missing physics is parent coefficient/operator/observable coupling | attack D_qWeyl2 coefficient source or q operator normalization before more numeric tests | false |
| DEC2307_3_next | NEXT_TARGET_SELECTED | a runner without D_qWeyl2/Z_q/P_arena would be numerology, so next should try to derive/source one of those inputs | 2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md | false |

## Next Target

| row_id | next_target | why | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| NEXT2307_0 | 2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md | 2307 proves projection plumbing but leaves parent coefficient, q operator, and observable map missing | nonclaim_private_next_step | false |

## Branch Copies

| row_id | source_csv | branch_copy_path | copy_exists | row_count | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2307_0_input_contract | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2307_SMOKE_RUNNER_INPUT_CONTRACT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2307_DQWEYL2_SMOKE_INPUT_CONTRACT_NONCLAIM.csv | true | 7 | false |
| COPY2307_1_projection_algebra | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2307_PROJECTION_ALGEBRA.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2307_DQWEYL2_PROJECTION_ALGEBRA_NONCLAIM.csv | true | 6 | false |
| COPY2307_2_dryrun | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2307_PROJECTION_SMOKE_DRYRUN.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\q_DqWeyl2_projection_smoke_dryrun_nonclaim_2307.csv | true | 3 | false |
| COPY2307_3_coefficient_hunt | source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2307_PARENT_COEFFICIENT_SOURCE_HUNT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\DQWEYL2_PARENT_COEFFICIENT_HUNT_2307_NONCLAIM.csv | true | 4 | false |

## Validation

| row_id | status | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL2307_00_sources_exist | PASS | every cited local source path exists | false |
| VAL2307_01_needles_found | PASS | all source needles were found | false |
| VAL2307_02_coefficient_missing | PASS | D_qWeyl2 coefficient remains missing | false |
| VAL2307_03_operator_missing | PASS | q Green operator remains missing | false |
| VAL2307_04_contract_required_fields | PASS | input contract has required fields | false |
| VAL2307_05_algebra_formula | PASS | massless q far-field formula recorded | false |
| VAL2307_06_dryrun_positive | PASS | dry-run kernels are positive | false |
| VAL2307_07_dryrun_nonclaim | PASS | dry-run rows are kernel-only nonclaim | false |
| VAL2307_08_claim_gates | PASS | local claim gate false | false |
| VAL2307_09_refusal_runner | PASS | refusal runner blocks claims | false |
| VAL2307_10_next_target | PASS | next target selected | false |
| VAL2307_11_branch_copies_parse | PASS | branch copies exist and parse | false |
| VAL2307_12_no_claim_flags | PASS | no generated row is valid_for_claim=true | false |
| VAL2307_13_formalization_untouched_by_2307 | PASS | no 2307 output appears in formalization-workbench | false |
| VAL2307_OVERALL | PASS | 2307 confirms D_qWeyl2/Z_q/P_arena are unsourced, writes a smoke-runner input contract, and produces nonclaim positive projection-kernel dry-run rows. | false |
