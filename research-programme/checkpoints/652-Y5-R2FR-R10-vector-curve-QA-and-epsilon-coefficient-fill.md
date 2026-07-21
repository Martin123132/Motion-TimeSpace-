# 4636 - R10 Vector Curve QA And Epsilon Coefficient Fill

Marker: `PPC4161_R10_VECTOR_CURVE_QA_AND_EPSILON_COEFFICIENT_FILL_4636`

Branch: `MTS_R2FR_Y5_R10_VECTOR_QA_EPSILON_ENVELOPE_4636`

Timestamp: `2026-07-06T19:19:19.407324+00:00`

## Result

4636 converts the 4635 R10 vector curve into a hard envelope for the observable source-coupling product.

The useful reduction is:

`Xi_AB(lambda_mem) := C_N epsilon_A epsilon_B / Z_min`

and the R10 gate is:

`|Xi_AB| <= alpha_bound(lambda_mem)`.

This is progress because R10 does not need us to separately know `epsilon_A`, `epsilon_B`, `Z_min`, and `C_N` before doing anything. It needs the parent-owned observable product `Xi_AB` plus `lambda_mem`. WEP/PPN still need the split and composition maps, so this does not overclaim.

## Source Register

| checkpoint | source_id | path | path_exists | needle | needle_found | line | role | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | SRC4636_00_4635_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4635_VALIDATION.csv | True | VAL4635_OVERALL | True | 19 | 4635 validation. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_01_4635_curve | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv | True | R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1 | True | 2 | 4635 vector curve. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_02_4635_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_R10_CURVE_STATUS_ROWS.csv | True | FULL_VECTOR_CURVE_EXTRACTED_FROM_FIG5B1_NONCLAIM | True | 2 | 4635 curve status. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_03_4635_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_PROJECTION_INPUT_REQUIREMENTS.csv | True | alpha_bound(lambda) | True | 7 | projection inputs. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_04_4635_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_VECTOR_CURVE_RUNNER_RESULTS.csv | True | RUN4635_0_current_live_R10 | True | 2 | live fail-closed runner. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_05_4635_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4635_NEXT_TARGET.csv | True | 4636-Y5-R2FR-R10-vector-curve-QA-and-epsilon-coefficient-fill.md | True | 2 | 4635 selected 4636. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_06_yukawa_convention | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10_curve_acquisition\4635\source\FB_ISL_pdf.tex | True | V(r)=V_N(r) [1+\alpha \exp({-r/\lambda})] | True | 43 | Yukawa convention in paper. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_07_alpha1_anchor | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10_curve_acquisition\4635\source\FB_ISL_pdf.tex | True | lambda<38.6\,\mu$m | True | 151 | published alpha=1 threshold. | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | SRC4636_08_fig5b1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\r10_curve_acquisition\4635\source\fig5b1.pdf | True |  | True | 0 | source vector figure. | False | 2026-07-06T19:19:19.407324+00:00 |

## Curve QA

| checkpoint | qa_id | status | detail | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4636 | QA4636_0_curve_present | PASS | 176 vector points loaded | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | QA4636_1_lambda_monotone | PASS | lambda values are strictly increasing | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | QA4636_2_alpha_nonincreasing | PASS | alpha bound decreases with lambda | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | QA4636_3_alpha1_anchor_crossing | PASS_FOR_SMOKE_QA | vector alpha=1 crossing=3.83693961472e-05 m; source anchor=3.86e-05 m; fractional error=-0.00597419 | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | QA4636_4_claim_grade | BLOCKED_NONCLAIM | official supplemental +/- alpha numeric rows or manual digitization QA still required before promotion | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Observable Xi Reduction

| checkpoint | row_id | statement | derivation_role | result | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | XI4636_0_define_observable_combo | Define Xi_AB(lambda_mem) := C_N epsilon_A epsilon_B / Z_min. | R10 observes this product combination, not the individual split into epsilon_A, epsilon_B, Z_min and C_N. | R10 coefficient target reduced to one observable parent-owned Xi_AB row. | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | XI4636_1_R10_gate | For the Yukawa convention V=V_N[1+alpha exp(-r/lambda)], R10 requires |Xi_AB| <= alpha_bound(lambda_mem). | Direct comparison of MTS scalar/Yukawa residual with Eot-Wash alpha(lambda). | The extracted curve can bound Xi_AB as a function of lambda_mem. | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | XI4636_2_epsilon_product | epsilon_A epsilon_B <= (Z_min/C_N) alpha_bound(lambda_mem). | Product envelope if the parent action supplies Z_min/C_N. | R10 gives a hard product ceiling once lambda_mem is known. | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | XI4636_3_symmetric_epsilon | If epsilon_A=epsilon_B=epsilon, then epsilon <= sqrt((Z_min/C_N) alpha_bound(lambda_mem)). | Readable symmetric-coupling envelope. | The local branch can now say how small symmetric coupling must be at each range. | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | XI4636_4_exact_zero | If no-slot/branch-extremum gives epsilon_A=0 or epsilon_B=0, then Xi_AB=0 and R10 is silent for this channel. | Exact local-GR route preserved. | Still conditional because the parent zero theorem is unsigned. | False | False | 2026-07-06T19:19:19.407324+00:00 |

## R10 Epsilon/Xi Envelope

| checkpoint | envelope_id | lambda_um | lambda_m | alpha_bound_abs | Xi_AB_max | epsilon_product_bound | symmetric_epsilon_max_if_Z_over_CN_1 | status | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | ENV4636_0 | 6 | 6e-06 | 692809.000865 | 692809.000865 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 832.351488774 | CANONICAL_ORDER_ONE_PRODUCT_ALLOWED_BY_VECTOR_SMOKE | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_1 | 10 | 1e-05 | 3002.42435853 | 3002.42435853 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 54.7943825454 | CANONICAL_ORDER_ONE_PRODUCT_ALLOWED_BY_VECTOR_SMOKE | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_2 | 20 | 2e-05 | 20.4989208714 | 20.4989208714 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 4.52757339768 | CANONICAL_ORDER_ONE_PRODUCT_ALLOWED_BY_VECTOR_SMOKE | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_3 | 30 | 3e-05 | 2.68500641949 | 2.68500641949 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 1.63859891965 | CANONICAL_ORDER_ONE_PRODUCT_ALLOWED_BY_VECTOR_SMOKE | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_4 | 38.6 | 3.86e-05 | 0.978211726949 | 0.978211726949 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.989045866959 | SUB_ORDER_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_5 | 50 | 5e-05 | 0.411641169874 | 0.411641169874 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.641592682216 | SUB_ORDER_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_6 | 70 | 7e-05 | 0.164750107778 | 0.164750107778 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.405894207619 | SUB_ORDER_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_7 | 85 | 8.5e-05 | 0.105346347391 | 0.105346347391 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.324571020565 | SUB_ORDER_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_8 | 100 | 0.0001 | 0.0755863083618 | 0.0755863083618 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.274929642567 | SMALL_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_9 | 200 | 0.0002 | 0.0315709160515 | 0.0315709160515 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.177682064518 | SMALL_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_10 | 500 | 0.0005 | 0.0253596688774 | 0.0253596688774 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.159247194253 | SMALL_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | ENV4636_11 | 1000 | 0.001 | 0.019096638734 | 0.019096638734 | (epsilon_A epsilon_B) <= (Z_min/C_N) * alpha_bound | 0.138190588442 | SMALL_PRODUCT_REQUIRED | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Xi To Lambda Max

| checkpoint | inverse_id | Xi_AB_assumed | lambda_max_for_pass_um | status | interpretation | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | INV4636_0 | 10000 | 8.78609997589 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_1 | 1000 | 11.3696075113 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_2 | 100 | 15.4968203036 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_3 | 10 | 22.8045788819 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_4 | 1 | 38.3693961472 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_5 | 0.1 | 87.1176356483 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_6 | 0.03 | 223.159730352 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_7 | 0.02 | 919.181738206 | CROSSING_FOUND | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | INV4636_8 | 0.01 | >=1000.05466489 | ALLOWED_THROUGH_FULL_EXTRACTED_RANGE | larger lambda needs smaller Xi_AB; exact-zero route bypasses this finite envelope only if parent-signed | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Parent Coefficient Targets

| checkpoint | target_id | target | why_this_is_better_than_circling | needed_parent_input | current_status | next_action | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | TGT4636_0_XiAB_direct | Xi_AB := C_N epsilon_A epsilon_B/Z_min | R10 only needs this product; deriving Xi_AB directly avoids demanding separately numeric epsilon_A, epsilon_B, Z_min and C_N before any progress. | same-branch quadratic/source action giving the observable Yukawa normalization | FORMULA_FILLED_NUMERIC_PARENT_ROW_MISSING | 4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | TGT4636_1_lambda_mem | lambda_mem=sqrt(Z_mem/M2_mem) | the R10 curve now converts a parent Hessian ratio into a concrete allowed coupling ceiling | positive gap ratio M2_mem/Z_mem or exact-zero source | FORMULA_FILLED_NUMERIC_PARENT_ROW_MISSING | 4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | TGT4636_2_exact_zero_factor | epsilon_A=0 or epsilon_B=0 | a single parent zero factor makes Xi_AB vanish without tuning the curve | signed no-source-slot/q-basic A_m, branch extremum, or parent involution | CONDITIONAL_UNSIGNED | try to sign the parent Xi zero theorem while retaining finite envelope | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | TGT4636_3_WEP_split_caveat | epsilon_A versus epsilon_B split and composition dependence | R10 can use Xi_AB, but WEP/PPN cannot; this separates what is genuinely needed for each arena | composition/source projection maps | STILL_REQUIRED_AFTER_R10 | do not use R10 Xi success as WEP/PPN success | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Runner Results

| checkpoint | run_id | Xi_AB | lambda_mem_m | alpha_bound_vector | result | reason | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | RUN4636_0_current_live | MISSING_PARENT_COEFFICIENT | MISSING_PARENT_HESSIAN_RATIO |  | FAIL_CLOSED_MISSING_XI_AND_LAMBDA | live branch has no parent Xi_AB/lambda row | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_1_exact_zero | 0 | 0.001 | 0.019096638734 | CONDITIONAL_EXACT_ZERO_PASS_ALGEBRA_ONLY | Xi_AB=0 if parent zero theorem is signed | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_2_order_one_at_vector_crossing | 1 | 3.83693961472e-05 | 0.999999999999 | PASS_WITHIN_VECTOR_QA_TOLERANCE_NONCLAIM | order-one Xi at extracted alpha=1 crossing | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_3_order_one_at_source_anchor | 1 | 3.86e-05 | 0.978211726949 | FAIL_VECTOR_ENVELOPE_XI_ABOVE_BOUND | source anchor is slightly to the right of vector crossing; this is QA-sensitive | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_4_order_one_at_50um | 1 | 5e-05 | 0.411641169874 | FAIL_VECTOR_ENVELOPE_XI_ABOVE_BOUND | order-one Xi at 50 um | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_5_point075_at_100um | 0.075 | 0.0001 | 0.0755863083618 | PASS_WITHIN_VECTOR_QA_TOLERANCE_NONCLAIM | near-bound small Xi at 100 um | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_6_point1_at_100um | 0.1 | 0.0001 | 0.0755863083618 | FAIL_VECTOR_ENVELOPE_XI_ABOVE_BOUND | slightly too-large Xi at 100 um | False | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | RUN4636_7_point01_at_1mm | 0.01 | 0.001 | 0.019096638734 | PASS_VECTOR_ENVELOPE_SMOKE_ONLY_NONCLAIM | small Xi at 1 mm | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Controls

| checkpoint | control_id | rule | violation_blocks_claim | timestamp_utc |
| --- | --- | --- | --- | --- |
| 4636 | CTL4636_0_no_Xi_fitting_from_bound | Do not choose Xi_AB from the R10 bound; Xi_AB must come from a parent coefficient row or exact-zero theorem. | True | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | CTL4636_1_curve_is_nonclaim | The vector-extracted curve is an internal smoke gate until official supplement/manual QA promotes it. | True | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | CTL4636_2_R10_not_WEP | A product Xi_AB bound does not replace composition-dependent WEP/PPN projections. | True | 2026-07-06T19:19:19.407324+00:00 |

## Blockers

| checkpoint | blocker_id | blocks | missing | next_action | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4636 | BLK4636_0_parent_Xi | R10/local-G finite branch | parent-owned Xi_AB and lambda_mem, or exact-zero factor | 4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | BLK4636_1_curve_promotion | claim-grade R10 comparison | official supplemental numeric +/- alpha rows or independent manual QA of vector extraction | keep vector curve as smoke until promoted | False | 2026-07-06T19:19:19.407324+00:00 |
| 4636 | BLK4636_2_other_arenas | WEP/PPN/clock/orbital use | source/test composition projection and metric-sector residual maps | after Xi_AB row exists, propagate to WEP/PPN with separate projections | False | 2026-07-06T19:19:19.407324+00:00 |

## Decision

| checkpoint | decision_id | decision | meaning | status | best_route | next_target | valid_for_claim | claim_allowed | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4636 | DEC4636_0 | R10_REDUCES_TO_OBSERVABLE_XI_ENVELOPE_PARENT_COEFFICIENT_TARGET_DEFINED_NONCLAIM | The R10 problem now has a concrete derived target: parent theory must supply Xi_AB and lambda_mem, or prove one factor is zero. The vector curve turns those into numeric pass/fail envelopes. | NONCLAIM_ENVELOPE_READY_PARENT_XI_TARGET_NEXT | derive or sign Xi_AB=0; if not, derive Xi_AB and lambda_mem and compare to the envelope. | 4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md | False | False | 2026-07-06T19:19:19.407324+00:00 |

## Next Target

`4637-Y5-R2FR-parent-XiAB-coefficient-zero-or-numeric-row.md`
