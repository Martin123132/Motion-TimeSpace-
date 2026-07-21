# 4675 - Y5/R2FR Source Branch-Force Residual Zero or First Numeric Bound Row

**Current verdict:** 4675 moves the coupling problem forward by shrinking `J_m_unowned`. The visible Hilbert matter term, post-solution Hilbert source readout, fixed compact collar/projector term, and extra standalone Poynting source are imported only as conditional zeros. The remaining object is the survivor vector:

```text
J_m_survivor =
  J_source_weight
+ J_coeff
+ J_nonHilbert
+ J_open_boundary
+ J_domain_reentry
+ E_m_res.
```

Therefore:

```text
|B_826| <= |a_F| L_cg^-2 |J_m_survivor|.
```

This is not a local-GR/R10/PPN claim. It is a sharper coupling target: prove or bound the survivor vector.

## Runner results

| checkpoint | runner_id | passed | status | detail | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | RUN4675_0_sources | True | PASS | all source paths and needles found | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_1_reduction | True | PASS | Jm survivor reduction row present | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_2_zero_imports | True | PASS | conditional zero imports recorded | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_3_survivor | True | PASS | source-weight survivor selected | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_4_bound | True | PASS | numeric bound row schema present | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_5_nonclaim | True | PASS | all rows remain nonclaim | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RUN4675_6_next | True | PASS | next target selected | False | False | 2026-07-07T17:26:12.686903+00:00 |

## Decision

| checkpoint | decision | why | promoted | claim_allowed | valid_for_claim | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | JM_UNOWNED_REDUCED_TO_SURVIVOR_VECTOR_CONDITIONAL_ZEROS_IMPORTED_NUMERIC_BOUND_ROW_READY_NONCLAIM | 4675 imports only already-established conditional zeros and compresses J_m_unowned to a survivor vector. The leading survivor is source-weight/current normalization, with coefficient, non-Hilbert, open-boundary/domain and Euler-certificate terms retained. | False | False | False | 4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md | 2026-07-07T17:26:12.686903+00:00 |

## Status

| checkpoint | branch | conditional_zeros_imported | Jm_survivor_vector_defined | source_weight_closed | numeric_bound_sourced | B826_zero | local_GR_claim | r10_claim | ppn_claim | decision | next_target | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | MTS_R2FR_Y5_SOURCE_BRANCH_FORCE_RESIDUAL_ZERO_OR_FIRST_NUMERIC_BOUND_ROW_4675 | True | True | False | False | False | False | False | False | JM_UNOWNED_REDUCED_TO_SURVIVOR_VECTOR_CONDITIONAL_ZEROS_IMPORTED_NUMERIC_BOUND_ROW_READY_NONCLAIM | 4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md | 2026-07-07T17:26:12.686903+00:00 |

## Next target

| checkpoint | next_target | why | derive_route | fallback_route | avoid | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | 4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md | After conditional zero imports, the most dangerous survivor is J_source_weight/current normalization. It is the coupling problem in its sharpest form. | Try to prove one common action/current owner forbids w_A, kappa_A and species current prefactors before variation. | Fill first numeric/source-backed bound row for delta_kappa_A or source-current normalization. | Do not use classical EOM rescaling as proof; Hilbert source still sees w_A. | False | 2026-07-07T17:26:12.686903+00:00 |

## Jm component reduction

| checkpoint | reduction_id | object | mathematical_form | source | status | consequence | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | RED4675_0_start | J_m_unowned | J_m_src + J_m_bdy + J_m_readout + J_m_domain + E_m_res | 4674 exact identity | STARTING_VECTOR | B_826 = -a_F L_cg^-2 J_m_unowned | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_1_visible_Hilbert | J_visible_matter | 0 on the q-owned visible Hilbert branch | 4303 + 2158 | CONDITIONAL_ZERO_IMPORTED | ordinary matter stress remains in T_Hilbert; it is not a separate m-lock force | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_2_source_readout | J_readout_Hilbert_charge | 0 for post-solution Hilbert/ADM source-charge readout | 4266 + 1454 + 1455 | CONDITIONAL_ZERO_IMPORTED | readout cannot re-enter the parent Euler equation if downstream | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_3_fixed_boundary | J_fixed_collar_projector | 0 on fixed compact no-flux collar/projector branch | 4268 | CONDITIONAL_ZERO_IMPORTED | moving/open boundary pieces survive separately | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_4_poynting_once | J_extra_Poynting | 0 on single Maxwell-Hodge Hilbert-owner branch | 4263 + 4312 + 4303 | CONDITIONAL_ZERO_IMPORTED | Poynting is real flux inside T_EM or a boundary residual, not a second hidden source | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_5_survivor_identity | J_m_survivor | J_source_weight + J_coeff + J_nonHilbert + J_open_boundary + J_domain_reentry + J_Euler_res | component reduction | SURVIVOR_VECTOR_DEFINED | this is the actual coupling gap after conditional zero imports | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | RED4675_6_B826_reduced_bound | B_826 | \|B_826\| <= \|a_F\| L_cg^-2 \|J_m_survivor\| | 4674 + 4675 | BOUND_SHARPENED_NONCLAIM | no local-GR/R10/PPN claim until survivor vector is zero or bounded | False | False | 2026-07-07T17:26:12.686903+00:00 |

## Conditional zero import matrix

| checkpoint | zero_id | component | condition | import_status | not_killed | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | ZERO4675_0_visible_matter | visible Hilbert matter m-lock force | S_matter has no direct m slot and depends only on g_obs(q) | CONDITIONAL_ZERO | parent visible-Hilbert split still unsigned globally | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | ZERO4675_1_source_readout | post-solution source readout | Q_src=Qbar[T_obs,g_obs,Sigma_obs,xi_obs] downstream of Hilbert variation | CONDITIONAL_ZERO | coefficient/G_N/source-current normalization remains outside this zero | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | ZERO4675_2_fixed_collar | fixed collar/projector derivative | W_loc,n,orientation,Pi_loc q-basic before variation and no source crossing | CONDITIONAL_ZERO | open radiation/source crossing/domain selector survives | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | ZERO4675_3_poynting_extra | extra standalone Poynting source | single Maxwell-Hodge/Hilbert owner with no c_Poynt_extra | CONDITIONAL_ZERO | radiative flux enters boundary residual if nonzero | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | ZERO4675_4_domain_projection | downstream projection as parent force | derivative-before-projection and variation-before-readout | CONDITIONAL_ZERO | pre-action selector/domain dependence survives | False | False | 2026-07-07T17:26:12.686903+00:00 |

## Jm survivor vector

| checkpoint | survivor_id | symbol | meaning | required_inputs | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | SURV4675_0_source_weight | J_source_weight | w_A, kappa_A, source-only prefactor/current normalization before variation | delta_kappa_A;w_A_prime;source_current_norm | PRIMARY_NEXT_TARGET | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_1_coeff | J_coeff | common kappa/G_N/ell_J/calibration coefficient owner | delta_v_kappa_cal;delta_v_ell_J | SURVIVES_AS_COEFFICIENT_GATE | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_2_nonHilbert | J_nonHilbert | non-Hilbert screened source, hidden EM/current, torsion/connection/memory tail | q_nonH;S_cg_nonHilbert;Q_m_H_nonHilbert | BOUND_OR_ZERO_REQUIRED | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_3_open_boundary | J_open_boundary | source crossing, radiative flux, memory pullback, corner/edge terms | R_source_crossing;R_rad_flux;R_memory_pullback;R_corner_edge | BOUND_OR_ZERO_REQUIRED | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_4_domain_reentry | J_domain_reentry | pre-action domain selector/projector or branch classifier | Delta_domain_selector_projector;q_domain | BOUND_OR_ZERO_REQUIRED | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_5_euler | E_m_res | parent branch equation/stationarity certificate missing | E_m_res;lambda_m;no_zero_mode | PARENT_EULER_CERTIFICATE_REQUIRED | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SURV4675_6_total | J_m_survivor_abs | absolute no-cancellation sum of survivor components | all above in common normalization | SCHEMA_READY_VALUES_MISSING | False | False | 2026-07-07T17:26:12.686903+00:00 |

## First numeric Jm bound row

| checkpoint | bound_id | symbol | formula | units | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | JMB4675_0_master | J_m_survivor_abs | \|J_source_weight\|+\|J_coeff\|+\|J_nonHilbert\|+\|J_open_boundary\|+\|J_domain_reentry\|+\|E_m_res\| | common_m_lock_force_units | MISSING_COMPONENT_VALUES | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | JMB4675_1_B826 | B826_bound | \|a_F\| L_cg^-2 J_m_survivor_abs | B826_units_from_4507 | MISSING_AF_LCG_AND_JM_VALUES | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | JMB4675_2_R10 | alpha_R10_projection | tau_R10(lambda_mem) * B826_bound or source-normalized equivalent | arena_declared_units | MISSING_ARENA_PROJECTION | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | JMB4675_3_PPN | PPN_projection | tau_PPN dot survivor vector | PPN_residual_units | MISSING_TAU_PPN | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | JMB4675_4_orbital | orbital_projection | tau_orbital dot source_weight/open_boundary/domain components | orbital_residual_units | MISSING_TAU_ORBITAL | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | JMB4675_5_claim_gate | valid_for_claim | true only after all numeric inputs are source-backed and comparator limits exist | boolean | FALSE_NOW | False | False | 2026-07-07T17:26:12.686903+00:00 |

## Controls

| checkpoint | control_id | rule | status | claim_allowed | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- |
| 4675 | CTRL4675_0_no_public_zero | Conditional zero imports do not make public local-GR/R10/PPN claims. | ACTIVE | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | CTRL4675_1_no_cancellation | Use absolute survivor-vector bounds; do not cancel components against each other. | ACTIVE | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | CTRL4675_2_no_poynting_double_count | Poynting is T_EM flux or boundary flux, not a second bulk source. | ACTIVE | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | CTRL4675_3_no_fitted_G_hiding | Measured G/GM may calibrate common scale only; it cannot hide relative source weights. | ACTIVE | False | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | CTRL4675_4_same_branch | Zeros, coefficients, and bounds must refer to the same parent local branch. | ACTIVE | False | False | 2026-07-07T17:26:12.686903+00:00 |

## Source register

| checkpoint | source_id | source_path | path_exists | needle | needle_found | line_number | note | valid_for_claim | timestamp_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4675 | SRC4675_00_4674_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4674_NEXT_TARGET.csv | True | 4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md | True | 2 | 4674 selected this target. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_01_4674_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4674_R826_EULER_RESIDUAL_PROOF.csv | True | PR4674_2_exact_identity | True | 4 | B826 Euler-residual identity. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_02_4674_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4674_FIRST_FINITE_B826_BOUND_SCHEMA.csv | True | BND4674_0_master | True | 2 | first B826 bound schema. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_03_4674_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4674_STATUS.csv | True | euler_identity_derived | True | 1 | 4674 status. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_04_4674_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_4674_VALIDATION.csv | True | VAL4674_OVERALL,True,PASS | True | 15 | 4674 validation. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_05_doc4674 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4674-Y5-R2FR-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md | True | B_826 = -a_F | True | 24 | 4674 derivation prose. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_06_formal690 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\690-PPC4161-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md | True | B_826 = -a_F | True | 24 | 4674 formal note. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_07_4266_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4266_SOURCE_READOUT_THEOREM.csv | True | SRCRO4266_2_charge_readout_zero | True | 4 | source charge readout zero. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_08_4266_remainder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4266_REMAINDER_SPLIT_ROWS.csv | True | REM4266_0_kappa_G_owner | True | 2 | coupling coefficient remainder. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_09_4268_theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4268_BOUNDARY_PROJECTOR_THEOREM.csv | True | BPROJ4268_1_fixed_collar_qbasic | True | 3 | fixed collar theorem. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_10_4268_remainder | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4268_OPEN_BOUNDARY_RESIDUAL_SPLIT_ROWS.csv | True | BRES4268_3_open_radiation | True | 5 | open radiation retained. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_11_4263_closed | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv | True | CCT4263_0_poynting_owner | True | 2 | Poynting counted once. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_12_4312_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_EM_POYNTING_CANCELLATION_THEOREM.csv | True | EC4312_2_once_only | True | 4 | extra Poynting coefficient zero condition. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_13_4303_visible | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4303_VISIBLE_HILBERT_M_LOCK_SILENCE_THEOREM.csv | True | VHS4303_1_matter_silence | True | 3 | visible matter m-lock silence. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_14_4303_matrix | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4303_COMPONENT_ZERO_NORM_MATRIX.csv | True | CM4303_2_screened_source | True | 4 | non-Hilbert screened source survivor. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_15_2158_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_IDENTITY.csv | True | SZI2158_2_zero_theorem | True | 4 | ordinary source-zero theorem. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_16_2158_decomp | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv | True | JQD2158_3_source_weight | True | 5 | source-weight survivor. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_17_2127_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2127_INERTIAL_ACTIVE_SOURCE_IDENTITY_ATTEMPT.csv | True | IAS2127_2_classical_rescale_obstruction | True | 4 | source-weight obstruction. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_18_4301_euler | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4301_EULER_LOCK_DERIVATION.csv | True | EL4301_3_exact_nohair | True | 5 | positive operator/nohair gate. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_19_1454_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv | True | VBR1454_2_post_selector_kill | True | 4 | variation-before-readout. | False | 2026-07-07T17:26:12.686903+00:00 |
| 4675 | SRC4675_20_1455_projection | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv | True | DBP1455_2_projection | True | 4 | derivative-before-projection. | False | 2026-07-07T17:26:12.686903+00:00 |

## Validation

| validation_id | passed | detail | timestamp_utc |
| --- | --- | --- | --- |
| VAL4675_0_sources | True | all source paths and needles found | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_SOURCE_REGISTER.csv | True | rows=21 columns=10 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_JM_UNOWNED_COMPONENT_REDUCTION.csv | True | rows=7 columns=10 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_CONDITIONAL_ZERO_IMPORT_MATRIX.csv | True | rows=5 columns=9 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_JM_SURVIVOR_VECTOR.csv | True | rows=7 columns=9 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_FIRST_JM_NUMERIC_BOUND_ROW.csv | True | rows=6 columns=9 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_CONTROL_ROWS.csv | True | rows=5 columns=7 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_RUNNER_RESULTS.csv | True | rows=7 columns=8 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_DECISION.csv | True | rows=1 columns=8 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_STATUS.csv | True | rows=1 columns=13 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_parse_P8_Y5_R2FR_4675_NEXT_TARGET.csv | True | rows=1 columns=8 | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_1_runner_pass | True | runner rows passed | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_2_outputs_exist | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\691-PPC4161-source-branch-force-residual-zero-or-first-numeric-bound-row.md;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_SOURCE_REGISTER.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_JM_UNOWNED_COMPONENT_REDUCTION.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_CONDITIONAL_ZERO_IMPORT_MATRIX.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_JM_SURVIVOR_VECTOR.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_FIRST_JM_NUMERIC_BOUND_ROW.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_CONTROL_ROWS.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_RUNNER_RESULTS.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_DECISION.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_STATUS.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4675_NEXT_TARGET.csv | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_3_no_claim_promotion | True | valid_for_claim remains false | 2026-07-07T17:26:12.686903+00:00 |
| VAL4675_OVERALL | True | PASS | 2026-07-07T17:26:12.686903+00:00 |
