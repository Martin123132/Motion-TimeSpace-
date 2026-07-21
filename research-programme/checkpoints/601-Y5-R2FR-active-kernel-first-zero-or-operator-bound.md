# 4585 - Active kernel first zero or operator bound

Marker: `PPC4161_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585`  
Branch: `MTS_R2FR_Y5_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585`  
Decision: `ACTIVE_KERNEL_PRODUCT_RULE_AND_FIXED_QBASIC_ZERO_CONTRACT_DERIVED_SOURCE_WORLDTUBE_FIRST_BOUND_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4585 turns the active-kernel blocker into a precise contract.

The key identity is:

```text
O_f(K_A J_H) = (O_f K_A)J_H + K_A(O_f J_H).
```

The previous checkpoints attacked the `J_H` and source-tail side.  The remaining kernel debt is exactly:

```text
C_KA := sup_{||f||_inf<=1} ||(O_f K_A)J_H||_TV / M_H_ref.
```

If an arena kernel is declared before variation as fixed/q-basic downstream data, then:

```text
O_f K_A = 0.
```

If not, it must receive a real operator norm.  No cancellation is allowed between arenas.

## Product-rule theorem

| checkpoint | theorem_id | claim | derivation | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | KPR4585_0_product_rule | The active kernel debt is exactly the product-rule derivative of the response kernel. | For an arena readout R_A=K_A J_H, O_f(K_A J_H)=(O_f K_A)J_H+K_A(O_f J_H). Earlier source/material/EM/apparatus reductions act on J_H or source tails; the surviving active-kernel term is (O_f K_A)J_H. | The kernel problem is no longer vague: prove O_f K_A=0 for each arena or bound ||(O_f K_A)J_H||/M_H_ref. | EXACT_PRODUCT_RULE_DERIVED | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | KPR4585_1_fixed_qbasic_kernel_zero | A kernel declared before variation as fixed/q-basic downstream data has O_f K_A=0. | If K_A=Kbar_A(q, P_protocol, e_obs, tau_obs, units, orientation) and the protocol object is fixed before source variation, then the compact source probe does not vary K_A. Hence O_f K_A=0 and the arena contributes no C_kernel_active. | The fixed-kernel theorem from 4581 is lifted to each named active kernel as a certificate test. | CONDITIONAL_ZERO_CERTIFICATE_DERIVED | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | KPR4585_2_operator_norm_fallback | If K_A is active, the fallback is an operator norm, not a placeholder. | C_KA := sup_{||f||_inf<=1} ||(O_f K_A)J_H||_TV/M_H_ref. The total active kernel envelope is the no-cancellation sum over source_worldtube, WEP, clock, light, orbital_GM and projective kernels. | Every arena now has a precise row to source: fixed-kernel certificate or finite operator norm with domain, units, support and source path. | BOUND_SCHEMA_DERIVED_VALUES_MISSING | 2026-07-06T12:42:25.672466+00:00 | False |

## Kernel certificate matrix

| checkpoint | certificate_id | symbol | kernel_shape | zero_certificate | fallback | source_anchor | certificate_currently_signed | numeric_operator_norm_present | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | KC4585_0_source_worldtube | K_source_worldtube | Delta_source(lambda)=int K_source rho_source_residual | fixed source support/profile and no post-fit source selector | C_K_source_worldtube <= sup_{||f||_inf<=1} ||(O_f K_source_worldtube)J_H||_TV/M_H_ref | KSR2118_0_source_worldtube_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KC4585_1_WEP | K_WEP | tau_WEP=<P_inst(t)[Delta_a_source-Delta_a_test]>_segments | official orbit/readout kernel fixed before variation and source-universality branch active | C_K_WEP <= sup_{||f||_inf<=1} ||(O_f K_WEP)J_H||_TV/M_H_ref | KSR2118_1_orbit_WEP_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KC4585_2_clock | K_clock | delta_nu/nu=P_clock[Q_trace, rod calibration, material markers, projective trace] | clock/rod/readout protocol fixed before variation with no material marker reentry | C_K_clock <= sup_{||f||_inf<=1} ||(O_f K_clock)J_H||_TV/M_H_ref | KSR2118_2_clock_redshift_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KC4585_3_light | K_light | gamma_minus_1 or Shapiro residual=P_lightcone[Q_shear, photon branch, source geometry] | lightcone response descends through observed metric/q and no active photon-branch selector | C_K_light <= sup_{||f||_inf<=1} ||(O_f K_light)J_H||_TV/M_H_ref | KSR2118_3_lightcone_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KC4585_4_orbital_GM | K_GM_orbit | delta(GM)_obs or fifth-force residual=P_orbit[source_support, readout_action, inverse-square split, time/range law] | GM convention and orbital transfer fixed before readout with no fitted-G absorption | C_K_GM_orbit <= sup_{||f||_inf<=1} ||(O_f K_GM_orbit)J_H||_TV/M_H_ref | KSR2118_4_orbital_GM_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KC4585_5_projective | K_projective | projective residual=P_projective[source, clock, WEP] | all-sector projective invariance certificate or fixed gauge projection | C_K_projective <= sup_{||f||_inf<=1} ||(O_f K_projective)J_H||_TV/M_H_ref | KSR2118_6_projective_trace_kernel | False | False | CERTIFICATE_OR_BOUND_REQUIRED | False | False | 2026-07-06T12:42:25.672466+00:00 |

## Operator-bound schema

| checkpoint | bound_id | needed_input | definition | status | valid_for_claim | claim_allowed | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | KBS4585_0_domain | kernel domain/support | W_loc, Sigma, source support, source profile and boundary class | MISSING_FIXED_DOMAIN_OR_OPERATOR_DOMAIN | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KBS4585_1_protocol | protocol fixed-before-variation flag | P_protocol timestamp/source path; no residual-fit selector | MISSING_PROTOCOL_CERTIFICATE | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KBS4585_2_operator_norm | operator norm N_KA | sup_{||f||<=1} ||O_f K_A|| on declared Banach/TV domain | MISSING_OPERATOR_NORM | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KBS4585_3_source_norm | source norm ||J_H||/M_H_ref | finite same-Hilbert source charge normalization | MISSING_SOURCE_NORM_OR_MHREF | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KBS4585_4_units | common units/projection | map each arena kernel to dimensionless C_kernel contribution | MISSING_COMMON_UNITS | False | False | 2026-07-06T12:42:25.672466+00:00 |
| 4585 | KBS4585_5_total | C_kernel_active | sum_A C_KA with no cancellation | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-06T12:42:25.672466+00:00 |

## Reduction rows

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | KRD4585_0_kernel_total_bound | C_kernel_active | C_kernel_active <= C_K_source_worldtube + C_K_WEP + C_K_clock + C_K_light + C_K_GM_orbit + C_K_projective | any kernel certificate unsigned | NO_CANCELLATION_OPERATOR_BOUND | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | KRD4585_1_kernel_total_zero | C_kernel_active | C_kernel_active=0 | all six kernel zero certificates signed: O_f K_A=0 for every active arena | CONDITIONAL_ZERO_CERTIFICATE_NOT_YET_SIGNED | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | KRD4585_2_Creadout_if_kernel_zero | C_readout | C_readout <= C_EFT_active + C_tau_tail | 4584 strict branch plus all active kernel certificates | NEXT_REDUCTION_IF_KERNELS_CLOSE | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | KRD4585_3_first_target | K_source_worldtube | C_K_source_worldtube <= sup_{||f||_inf<=1} ||(O_f K_source_worldtube)J_H||_TV/M_H_ref | first foundational kernel; feeds R10/PPN/orbital/source support | SELECTED_NEXT_ZERO_OR_OPERATOR_NORM_TARGET | 2026-07-06T12:42:25.672466+00:00 | False |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | CTRL4585_fixed_kernel | kernel fixed before variation | O_f K_A=0 | CONTROL_PASS | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | CTRL4585_active_response | kernel depends on fitted source support/readout residual | operator norm retained | COUNTERMODEL_CAUGHT | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | CTRL4585_no_cancellation | one kernel positive and another negative | sum absolute component bounds | FIREWALL_PASS | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | CTRL4585_WEP_not_official | surrogate/MICROSCOPE kernel not official fixed data | WEP certificate remains unsigned | FIREWALL_PASS | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | CTRL4585_orbital_GM | kernel uses fitted GM to define source | reject zero; route to operator/source convention | COUNTERMODEL_CAUGHT | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | CTRL4585_no_local_claim | kernel schema exists | no local-GR/R10/PPN claim | FIREWALL_PASS | 2026-07-06T12:42:25.672466+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4585 | PROM4585_0_product_rule | Active kernel product rule derived. | PASSED | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | PROM4585_1_fixed_zero | Fixed q-basic kernel zero certificate derived. | PASSED_CONDITIONAL | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | PROM4585_2_operator_schema | Operator norm fallback schema emitted. | PASSED | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | PROM4585_3_kernel_values | Actual arena kernel certificates/operator norms are sourced. | BLOCKED | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | PROM4585_4_next_source_worldtube | Source-worldtube selected as first kernel target. | PASSED | 2026-07-06T12:42:25.672466+00:00 | False | False |
| 4585 | PROM4585_5_no_public_claim | No local-GR/R10/PPN claim from kernel schema. | PASSED_FIREWALL | 2026-07-06T12:42:25.672466+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4585 | MTS_R2FR_Y5_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585 | 2026-07-06T12:42:25.672466+00:00 | ACTIVE_KERNEL_PRODUCT_RULE_AND_FIXED_QBASIC_ZERO_CONTRACT_DERIVED_SOURCE_WORLDTUBE_FIRST_BOUND_RETAINED_NONCLAIM | 4585 derives the exact active-kernel product rule and the fixed/q-basic kernel zero certificate. The old 'missing active kernels' are now six explicit certificate-or-operator-norm rows. No arena kernel is claimed closed yet; the first target is source-worldtube because it feeds source support, R10, PPN and orbital readouts. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | MTS_R2FR_Y5_ACTIVE_KERNEL_FIRST_ZERO_OR_OPERATOR_BOUND_4585 | 2026-07-06T12:42:25.672466+00:00 | 4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md | The source-worldtube kernel is the first and most upstream active kernel; if fixed or bounded, several downstream arena kernels stop inheriting source-support ambiguity. | prove K_source_worldtube is fixed q-basic/source-domain data, or source a finite operator norm on the declared local collar | stage source profile/support/operator norm rows with units, M_H_ref normalization and no fitted-G absorption | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4585 | SRC4585_00_4584_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4584-Y5-R2FR-parent-material-tensor-and-apparatus-support-zero-or-bound.md | True | C_readout <= C_kernel_active + C_EFT_active + C_tau_tail | True | 4584 handoff | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_01_4584_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4584_MATERIAL_APPARATUS_REDUCTION_ROWS.csv | True | MAR4584_3_Creadout_update | True | 4584 Creadout reduction | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_02_4584_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4584_NEXT_TARGET.csv | True | active-kernel-first-zero-or-operator-bound | True | 4584 selected 4585 | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_03_4581_fixed_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\597-PPC4161-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md | True | C_kernel_fixed = 0 | True | fixed kernel zero theorem | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_04_4581_active_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\597-PPC4161-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md | True | C_kernel_active <= K_clock | True | active kernel tail bound | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_05_4582_operator_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\598-PPC4161-material-response-tail-and-active-kernel-first-bound-or-owner-zero.md | True | C_kernel_active <= sum_A | True | 4582 active operator norm | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_06_4582_kernel_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4582_ACTIVE_KERNEL_BOUND_INTERFACE.csv | True | AK4582_0_source_worldtube | True | 4582 active kernel interface | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_07_2118_kernels | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv | True | KSR2118_7_total_no_cancellation | True | explicit exception kernels | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_08_operator_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\514-PPC4161-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md | True | R_A = Pi_A T_shell | True | arena operator contract precedent | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_09_fixed_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | q-basic readout/domain data | True | fixed q-basic collar precedent | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_10_domain_cert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_0_protocol_object | True | pre-variation protocol object | 2026-07-06T12:42:25.672466+00:00 | False |
| 4585 | SRC4585_11_claim_426 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-426 | True | prior claim register handoff | 2026-07-06T12:42:25.672466+00:00 | False |
