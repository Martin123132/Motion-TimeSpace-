# 4690 - Y5/R2FR Z_X/M_X^2/lambda_X Range Owner Or Body-Charge Score First Fill

Marker: `PPC4161_RANGE_OWNER_NORMALIZATION_INVARIANT_CURRENT_BRANCH_4690`

Decision: `RANGE_NORMALIZATION_INVARIANT_LAW_CURRENT_BRANCH_VALUES_MISSING_NONCLAIM`

## Result

4690 imports the normalization-invariant range law:

```text
S_X^(2)=1/2 int sqrt(g)[Z_X |grad X|^2 + M_X^2 X^2] - int sqrt(g) X rho_X
(-Z_X nabla^2 + M_X^2)X=rho_X
lambda_X=sqrt(Z_X/M_X^2)
```

Under `X=a X_prime`, raw `Z_X` and raw charge move:

```text
Z_prime=a^2 Z_X,  M_prime^2=a^2 M_X^2,  rho_prime=a rho_X,  q_prime=a q_X.
```

So the physical score objects are invariant:

```text
lambda_X,
I_X^ST := Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T),
Q_boundary_X/Z_X.
```

This is the coupling lesson in cleaner form: do not chase a naked coupling constant if field normalization can move it. Score only invariant products or theorem-zero branches.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line_number | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | SRC4690_00_4689_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4689_NEXT_TARGET.csv | True | 4690-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md | True | 2 | 4689 selected range-owner target. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_01_4689_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4689_STATUS.csv | True | PPC4161_BODY_CHARGE_SCORE_VECTOR_CURRENT_BRANCH_4689 | True | 2 | 4689 current branch status. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_02_4602_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_RANGE_OWNER_NORMALIZATION_THEOREM.csv | True | RNG4602_4_invariant_alpha_owner | True | 6 | 4602 normalization/range theorem. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_03_4602_invariant | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_INVARIANT_SCORE_LAW.csv | True | INV4602_3_rank_zero_no_lambda | True | 5 | 4602 invariant score law. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_04_4602_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_RANGE_OWNER_INPUT_ROWS.csv | True | RIN4602_1 | True | 3 | 4602 memory/fibre range inputs. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_05_4602_score | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_SCORE_VECTOR_RANGE_UPDATE.csv | True | SUP4602_4 | True | 6 | 4602 score-vector range update. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_06_4602_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_REMAINING_RANGE_INPUT_BLOCKERS.csv | True | MIS4602_6_full_bounds | True | 8 | 4602 remaining blockers. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_07_4602_controls | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_CONTROL_ROWS.csv | True | CTRL4602_mixed_modes | True | 4 | 4602 controls. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_08_4602_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_STATUS.csv | True | PPC4161_ZX_MX2_LAMBDAX_RANGE_OWNER_OR_BODY_CHARGE_SCORE_FIRST_FILL_4602 | True | 2 | 4602 status. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_09_4602_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4602_NEXT_TARGET.csv | True | 4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | True | 2 | 4602 next target. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_10_4602_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4602_VALIDATION.csv | True | VAL4602_OVERALL | True | 19 | 4602 validation passed. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_11_4603_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4603_STATUS.csv | True | SOURCE_TEST_INVARIANT_PRODUCT_DERIVED_SCHEMA_READY_NONCLAIM | True | 2 | 4603 next rung exists. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_12_4603_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4603_NEXT_TARGET.csv | True | 4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md | True | 2 | 4603 next target. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_13_4603_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4603_VALIDATION.csv | True | VAL4603_OVERALL | True | 19 | 4603 validation passed. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_14_formal618 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\618-PPC4161-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md | True | raw `Z_X` and raw charge | True | 25 | formal range-owner invariant law. | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SRC4690_15_formal619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\619-PPC4161-source-test-charge-invariant-product-or-first-numeric-bound-row.md | True | I_X^ST(lambda_X) | True | 27 | formal source/test invariant product handoff. | False | 2026-07-07T18:59:52+00:00 |

## Range Owner Normalization Theorem

| checkpoint | theorem_id | statement | formula | consequence | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | RNG4690_0_quadratic_normal_form | A finite-range body-charge field must come from a parent quadratic block with gradient and Hessian terms on the same quotient domain. | S_X^(2)=1/2 int sqrt(g)[Z_X \|grad X\|^2 + M_X^2 X^2] - int sqrt(g) X rho_X + S_boundary | (-Z_X nabla^2+M_X^2)X=rho_X and lambda_X=sqrt(Z_X/M_X^2) | DERIVED_NORMAL_FORM_PARENT_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | RNG4690_1_rescaling_invariance | Raw Z_X and raw source charge are not separately observable because field normalization can be rescaled. | X=a X_prime => Z_prime=a^2 Z_X, M_prime^2=a^2 M_X^2, rho_prime=a rho_X, q_prime=a q_X | lambda_prime=lambda_X and q_S q_T/Z_X is invariant; score rows must use invariant products, not naked Z_X | EXACT_NORMALIZATION_GAUGE_LAW | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | RNG4690_2_rank_zero_vs_finite_range | The local route splits cleanly: auxiliary rank-zero vertical coordinates are algebraic, while nonzero principal symbol modes must be scored as finite-range fields. | K_AB=0 => M_AB z^B=-R_A; K_AB>0 and M_AB>0 => lambda_i=sqrt(Z_i/M_i^2) | do not run a Yukawa/R10 score for a true auxiliary rank-zero closure; do not claim closure for a propagating finite-range branch without alpha/PPN bounds | BRANCH_SPLIT_DERIVED | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | RNG4690_3_claim_grade_range_owner | Claim-grade lambda_X requires a parent principal symbol and Hessian projected onto the same physical mode after gauge/constraint reduction. | Z_X=<v_X,K v_X>, M_X^2=<v_X,H v_X>, lambda_X=sqrt(Z_X/M_X^2) | memory/fibre ranges remain missing until v_X,K,H,units and sign are sourced | SOURCE_ROW_CONTRACT_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | RNG4690_4_invariant_alpha_owner | The R10/fifth-force score should be carried by lambda_X and an invariant source-test product, with the chosen Green-kernel convention declared. | alpha_X(lambda_X)=K_X I_X^ST, I_X^ST:=Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T) | the 4603 target is the invariant source/test product, not a raw source charge alone | INVARIANT_SCORE_OBJECT_DEFINED_NONCLAIM | False | False | 2026-07-07T18:59:52+00:00 |

## Invariant Score Law

| checkpoint | law_id | object | definition | field_rescaling | claim_input | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | INV4690_0_lambda | lambda_X | sqrt(Z_X/M_X^2) on a finite-range principal branch | invariant under X=a X_prime | parent-projected K/H eigenvalue pair with units | FORMULA_DERIVED_NUMERIC_VALUE_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | INV4690_1_source_product | I_X^ST | Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T), or declared equivalent if the Green convention absorbs 4*pi/Z_X | invariant because Qbar and qbar scale with a while Z scales with a^2 | source/test charge integrals, Z convention, G_N/GM calibration and source paths | INVARIANT_OBJECT_DEFINED_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | INV4690_2_boundary_product | Q_boundary_X/Z_X | boundary Green charge contribution divided by the same operator normalization | invariant when boundary charge is varied in the same X normalization | no-flux theorem or finite boundary integral with matching normalization | BOUNDARY_INVARIANT_DEFINED_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | INV4690_3_rank_zero_no_lambda | auxiliary rank-zero branch | K_AB=0, M_AB coercive, z algebraically locked or bounded by m_min^-1 residuals | not a finite-range Yukawa field; score uses algebraic residual norm, not lambda_X | parent K=0, M_AB>=m_min and source RHS zero/bound | AUXILIARY_ROUTE_SEPARATED_NOT_CLAIMED | False | False | 2026-07-07T18:59:52+00:00 |

## Range Owner Input Rows

| checkpoint | range_id | sector | operator_normalization | mass_gap | range_symbol | range_formula | invariant_source_test_product | invariant_boundary_product | required_parent_inputs | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | RIN4690_0 | memory | Z_mem | M2_mem | lambda_mem | lambda_mem=sqrt(Z_mem/M2_mem) | I_mem^ST | Q_boundary_mem/Z_mem | physical mode v_X; principal symbol K; Hessian H; unit convention; source/test charge normalization | RANGE_FORMULA_DERIVED_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | RIN4690_1 | fibre | Z_h | M2_h | lambda_h | lambda_h=sqrt(Z_h/M2_h) | I_h^ST | Q_boundary_h/Z_h | physical mode v_X; principal symbol K; Hessian H; unit convention; source/test charge normalization | RANGE_FORMULA_DERIVED_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |

## Score Vector Range Update

| checkpoint | update_id | arena | update | score_law | required_inputs | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | SUP4690_0 | R10 | score by lambda_X plus invariant I_X^ST | alpha_X(lambda_X)=K_R10_X I_X^ST plus boundary/direct tails | lambda_X;I_X^ST;Q_boundary_X/Z_X;alpha_bound(lambda);units | INVARIANT_SCORE_FORM_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SUP4690_1 | PPN | score by A_X/Z-normalized amplitude or direct invariant tails | Delta p_i <= sum_X \|\|K_iX\|\| \|A_X\| + \|direct_tail_i\|, with A_X built from rho_X/Z_X | lambda_X;B_X/Z_X;C_X/Z_X;J_X/Z_X;Q_boundary_X/Z_X;K_iX | INVARIANT_SCORE_FORM_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SUP4690_2 | orbital_GM | score by Yukawa acceleration with explicit calibration | Delta a/a_N=alpha_X(1+r/lambda_X)exp(-r/lambda_X) | lambda_X;alpha_X;GM convention;orbital threshold | INVARIANT_SCORE_FORM_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SUP4690_3 | clock_WEP | score material/clock response from invariant coupling derivatives | Delta O <= K_material I_X^material + K_clock C_X^final/Z_X + direct tails | material source integrals;clock kernels;standard/weight rows | INVARIANT_SCORE_FORM_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SUP4690_4 | EM_Poynting | score EM/open flux as direct tail before alpha comparison | Delta O_EM <= K_EM(\|J_EM\|/Z_X+\|Delta_Hodge\|+\|Phi_EM\|+\|b_alpha\|) | same-Hodge owner or finite Poynting/EM flux profile | INVARIANT_SCORE_FORM_READY_VALUES_MISSING | False | False | 2026-07-07T18:59:52+00:00 |

## Remaining Range Input Blockers

| checkpoint | missing_id | missing_input | required_evidence | why_it_matters | current_status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | MIS4690_0_principal_symbol | K_AB or Z_X | parent second variation gradient block on physical quotient | needed to distinguish auxiliary from finite-range | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_1_hessian | H_AB or M_X^2 | parent second variation Hessian/mass block | needed for coercivity/range | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_2_mode_basis | v_X | same mode basis for K,H,source and readout | prevents mixing memory/fibre directions | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_3_units | unit convention | SI/natural-unit conversion, c/hbar and 4*pi Green convention | prevents fake alpha normalization | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_4_source_product | I_X^ST | source/test charge-over-Z invariant with calibration | 4603 target | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_5_boundary_product | Q_boundary_X/Z_X | boundary integral or no-flux theorem in same normalization | separate from C_X boundary leakage | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | MIS4690_6_full_bounds | alpha/PPN/clock/orbit/EM bounds | source-backed empirical comparison tables/kernels | needed only after source product exists | MISSING_BLOCKS_CLAIM | False | False | 2026-07-07T18:59:52+00:00 |

## Survivor Update

| checkpoint | survivor_id | residual_family | status_after_4690 | next_action | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | SURV4690_0_lambda | lambda_X | range is invariant under field normalization; numeric values still missing | 4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SURV4690_1_source_product | I_X^ST | raw source/test charges replaced by invariant product target | 4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SURV4690_2_rank_zero | auxiliary rank-zero branch | separated from finite-range Yukawa scoring | do not run R10 alpha on true auxiliary closure | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SURV4690_3_mode_basis | v_X/K/H same-mode lock | still required for claim-grade range rows | keep blocker active | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | SURV4690_4_empirical_scoring | R10/PPN/clock/orbit/EM | score laws are invariant-form ready but values/bounds missing | defer pass/fail claims | False | False | 2026-07-07T18:59:52+00:00 |

## Controls

| checkpoint | control_id | input_branch | expected | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | CTRL4690_raw_Z_rescale | X is rescaled and raw Z_X changes | lambda_X and Q_S q_T/Z_X stay invariant; raw Z-only claims fail | COUNTERMODEL_CAUGHT | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | CTRL4690_rank_zero_firewall | K_AB=0 auxiliary branch is fed into a Yukawa alpha runner | reject finite-range score; use algebraic residual or local closure theorem | GUARD_ACTIVE | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | CTRL4690_mixed_modes | Z_X from one mode, M_X^2 from another, source charge from a third | range row invalid until same mode basis is declared | COUNTERMODEL_CAUGHT | False | False | 2026-07-07T18:59:52+00:00 |
| 4690 | CTRL4690_missing_units | lambda or alpha product has no unit/Green-kernel convention | score row stays nonclaim | GUARD_ACTIVE | False | False | 2026-07-07T18:59:52+00:00 |

## Decision

| checkpoint | decision | summary | next_target | public_claim | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4690 | RANGE_NORMALIZATION_INVARIANT_LAW_CURRENT_BRANCH_VALUES_MISSING_NONCLAIM | 4690 imports the range-owner normalization-invariant law into the current branch. Raw Z_X and raw source charge are normalization-gauge objects; lambda_X and source/test charge-over-Z products are the physical score objects. The finite-range branch is separated from auxiliary rank-zero closure. | 4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | False | False | 2026-07-07T18:59:52+00:00 |

## Status

| checkpoint | marker | claim_id | decision | derived | not_derived | claim_status | local_GR_public_claim | next_target | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | PPC4161_RANGE_OWNER_NORMALIZATION_INVARIANT_CURRENT_BRANCH_4690 | L-532 | RANGE_NORMALIZATION_INVARIANT_LAW_CURRENT_BRANCH_VALUES_MISSING_NONCLAIM | quadratic range normal form; field-rescaling invariant law; invariant lambda and source-product objects; auxiliary rank-zero versus finite-range branch split; memory/fibre range input rows | numeric parent K/H eigenvalues; numeric lambda_mem/lambda_h; invariant source/test product; boundary/Z product; R10/PPN/clock/orbital/EM pass | PRIVATE_NONCLAIM | False | 4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | False | 2026-07-07T18:59:52+00:00 |

## Next Target

| checkpoint | next_id | target | reason | derive_first | fallback | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4690 | NT4690_0 | 4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md | 4690 shows the physical score row is not raw Z_X or raw charge but lambda_X plus invariant source/test product. The next useful target is therefore I_X^ST or a theorem-zero for it. | derive source/test charge-over-Z invariant from parent Hilbert/source functor and test-body coupling | emit first nonclaim numeric-bound row for I_X^ST with units, source paths and blockers | False | 2026-07-07T18:59:52+00:00 |

## Validation

| checkpoint | check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4690 | VAL4690_0_sources_exist | True | all source-register paths exist | False |
| 4690 | VAL4690_1_needles_found | True | all source-register needles found | False |
| 4690 | VAL4690_2_rescaling_law | True | field-rescaling invariant law present | False |
| 4690 | VAL4690_3_rankzero_split | True | rank-zero and finite-range split present | False |
| 4690 | VAL4690_4_invariant_objects | True | invariant score objects present | False |
| 4690 | VAL4690_5_memory_fibre_range | True | memory/fibre range rows present | False |
| 4690 | VAL4690_6_score_update | True | score update uses invariant/range objects | False |
| 4690 | VAL4690_7_blockers | True | remaining blockers start with principal symbol | False |
| 4690 | VAL4690_8_next_source_test | True | next source/test invariant target selected | False |
| 4690 | VAL4690_9_claim_row_exists | True | claims register contains L-532 | False |
| 4690 | VAL4690_10_formal_doc | True | formal doc exists with marker | False |
| 4690 | VAL4690_11_post_doc | True | post checkpoint exists with marker | False |
| 4690 | VAL4690_12_spine_marker | True | spine marker written | False |
| 4690 | VAL4690_13_packet_marker | True | packet marker written | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_SOURCE_REGISTER | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_SOURCE_REGISTER.csv parses with 16 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_RANGE_OWNER_NORMALIZATION_THEOREM | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_RANGE_OWNER_NORMALIZATION_THEOREM.csv parses with 5 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_INVARIANT_SCORE_LAW | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_INVARIANT_SCORE_LAW.csv parses with 4 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_RANGE_OWNER_INPUT_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_RANGE_OWNER_INPUT_ROWS.csv parses with 2 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_SCORE_VECTOR_RANGE_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_SCORE_VECTOR_RANGE_UPDATE.csv parses with 5 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_REMAINING_RANGE_INPUT_BLOCKERS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_REMAINING_RANGE_INPUT_BLOCKERS.csv parses with 7 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_SURVIVOR_UPDATE | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_SURVIVOR_UPDATE.csv parses with 5 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_CONTROL_ROWS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_CONTROL_ROWS.csv parses with 4 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_DECISION | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_DECISION.csv parses with 1 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_STATUS | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_STATUS.csv parses with 1 rows | False |
| 4690 | VAL4690_csv_P8_Y5_R2FR_4690_NEXT_TARGET | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4690_NEXT_TARGET.csv parses with 1 rows | False |
| 4690 | VAL4690_14_no_claim_rows_true | True | generated rows keep valid_for_claim false | False |
| 4690 | VAL4690_15_pycache_absent | True | scripts __pycache__ absent | False |
| 4690 | VAL4690_OVERALL | True | PASS | False |
