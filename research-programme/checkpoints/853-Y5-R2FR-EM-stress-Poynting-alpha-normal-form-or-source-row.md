# 4837 Y5 R2FR EM stress Poynting alpha normal form or source row

**Status:** 4837 fences the EM route. Calibrated Maxwell stress and the Poynting vector are usable as conditional source bookkeeping on the observed geometry, but MTS does not yet derive the full EM normal form. The live gates are observed Hodge/coframe ownership, unique Maxwell `F^2`, charge-current normalization, nonminimal `X F^2`, radiative/readout closure, and exterior Poynting flux.

**Decision:** `EM_STRESS_POYNTING_ALPHA_NORMAL_FORM_UNSIGNED_SOURCE_ROW_STAGED_NONCLAIM`.

**Claim ceiling:** no derived-alpha, Maxwell-source, local-GR, Newtonian, R10, WEP, clock, PPN, or calibrated-coupling claim is allowed from 4837.

## Core derivation

```text
S_EM = -1/4 integral mu_obs lambda_EM F_mu_nu F^mu_nu
delta_g S_EM -> T_EM
S_Poynting = E cross B

Zero route:
*_EM = *_obs[e_obs(q)]
lambda_EM = C_P N_Q with no lambda_A F_Q^2 and no f_X(Phi)F_Q^2
charge/current normalization fixed by same parent owner
Phi_EM_rad = integral_boundary S_Poynting dot n dA = 0

Fallback:
EM_total =
  (epsilon_EM_bound + Delta_Hodge_EM + w_EM + C_JQ + epsilon_internal_exchange)
  + Phi_EM_rad
  + (C_XF2 + w_EM + C_JQ + C_EM_readout)

qbar_XT_EM_feed = P_EM_qbar EM_total
alpha_source = K_source Qbar_source_XH_bound qbar_XT_EM_feed
```

## Source register

| source_id | exists | needle_found | role |
| --- | --- | --- | --- |
| SRC4837_00_resume | True | True | 4836 selected this EM target. |
| SRC4837_01_4836_doc | True | True | EM stress/Poynting handoff. |
| SRC4837_02_637_alpha | True | True | alpha/charge blocker. |
| SRC4837_03_1057_unique | True | True | unique Maxwell F2 blocker. |
| SRC4837_04_1057_alpha | True | True | conditional alpha zero route. |
| SRC4837_05_1397_verdict | True | True | lambda_A fallback verdict. |
| SRC4837_06_1397_lambda | True | True | standalone Maxwell counterterm source row. |
| SRC4837_07_990_contract | True | True | minimal parent action EM lock contract. |
| SRC4837_08_poynting_stress | True | True | Maxwell stress/Poynting component. |
| SRC4837_09_poynting_flux | True | True | Poynting flux blocker. |
| SRC4837_10_poynting_XF2 | True | True | nonminimal XF2 blocker. |
| SRC4837_11_hodge | True | True | Hodge/constitutive owner. |
| SRC4837_12_current_norm | True | True | charge-current normalization. |
| SRC4837_13_unique_status | True | True | calibrated alpha baseline. |
| SRC4837_14_visible_status | True | True | EM residual narrowing. |
| SRC4837_15_scalar_identity | True | True | CXF2 alpha identity. |
| SRC4837_16_current_alpha | True | True | Ward alpha residual. |
| SRC4837_17_alpha_runner | True | True | alpha bound runner blocked row. |
| SRC4837_18_alpha_source_runner | True | True | source alpha bound runner blocked row. |
| SRC4837_19_hodge_flow | True | True | Hodge flow bound vector. |
| SRC4837_20_local_interface | True | True | calibrated Maxwell stress interface. |
| SRC4837_21_runner | True | True | 4837 executable runner. |

## EM audit

| clause_id | object | current_result | needed_signature_or_input |
| --- | --- | --- | --- |
| EM4837_0_calibrated_identity | calibrated Maxwell stress | USABLE_CONDITIONAL_IDENTITY | observed Hodge/current gates remain |
| EM4837_1_hodge | observed EM Hodge/coframe | OPEN_BLOCKER | parent observed Hodge/constitutive signature |
| EM4837_2_unique_F2 | unique Maxwell kinetic owner | FAILS_CURRENT_CORPUS | operator-domain exhaustion or retain lambda_A |
| EM4837_3_XF2 | nonminimal hidden-visible EM operator | EXACT_IDENTITY_NOT_ZERO | zero theorem or finite alpha derivative source row |
| EM4837_4_charge_current | charge-current normalization | OPEN_BLOCKER | T_Q/current/charge lattice owner |
| EM4837_5_poynting | radiative/background Poynting flux | OPEN_BLOCKER | stationary isolated zero theorem or flux bound |
| EM4837_6_exchange | matter-EM internal exchange | CONDITIONAL_TOTAL_STRESS_ZERO | same matter+EM parent action/current |
| EM4837_7_alpha_baseline | calibrated alpha branch | SAFE_BASELINE_NONCLAIM | nonzero C_XF2 branch must be scored |

## EM source-row contract

| contract_id | quantity | definition | status |
| --- | --- | --- | --- |
| EMC4837_0_zero | EM residual zero | observed Hodge + minimal Maxwell action + unique F2 + charge-current owner + alpha superselection + no Poynting flux | conditional_only |
| EMC4837_1_stress | Maxwell stress residual | epsilon_EM_bound + Delta_Hodge_EM + w_EM + C_JQ + epsilon_internal_exchange | runner_ready |
| EMC4837_2_alpha | alpha drift residual | C_XF2 + w_EM + C_JQ + C_EM_readout | runner_ready |
| EMC4837_3_poynting | Poynting flux residual | Phi_EM_rad/(G_ref M_H) or window-normalized flux row | runner_ready |
| EMC4837_4_alpha_identity | b_alpha identity | b_alpha = 2 z_g - z_lambda plus readout; absolute bound uses 2\|z_g\|+\|z_lambda\|+\|C_readout\| | runner_ready |
| EMC4837_5_next | kappa/G/Newton source gate | return to source-current normalization and Newtonian Poisson denominator | next_target |

## Runner output

| row_id | runner_status | maxwell_stress_residual_abs | poynting_flux_residual_abs | alpha_drift_residual_abs | EM_total_residual_abs | qbar_XT_EM_feed_abs | alpha_source_abs | BY5_EM_feed_abs | missing_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN4837_0_live_EM_zero_missing | BLOCKED_EM_STRESS_ALPHA_ZERO_CLAUSES | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_source_signed;MISSING_units_signed;MISSING_same_branch_signed;MISSING_no_cancellation_guard;MISSING_observed_hodge_coframe_signed;MISSING_minimal_maxwell_action_signed;MISSING_unique_F2_parent_owner_signed;MISSING_fixed_charge_current_normalization_signed;MISSING_alpha_superselection_signed;MISSING_no_nonminimal_XF2_signed;MISSING_poynting_boundary_flux_zero_signed;MISSING_matter_EM_exchange_total_stress_signed;MISSING_readout_radiative_closure_signed;MISSING_no_unit_rescaling_alpha_signed;MISSING_no_measured_GM_absorption_signed |
| RUN4837_1_conditional_EM_zero_pass | EM_STRESS_ALPHA_ZERO_PASS_NONCLAIM | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 | 0.000000000000000e+00 |  |
| RUN4837_2_live_EM_bound_missing | BLOCKED_EM_RESIDUAL_BOUND_INPUTS | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_epsilon_EM_bound_abs;MISSING_Delta_Hodge_EM_abs;MISSING_w_EM_abs;MISSING_C_XF2_abs;MISSING_C_JQ_abs;MISSING_Phi_EM_rad_abs;MISSING_C_EM_readout_abs;MISSING_epsilon_internal_exchange_abs;MISSING_P_EM_qbar_abs;MISSING_Qbar_source_XH_bound_abs;MISSING_K_source_abs;MISSING_tau_BY5_EM_abs |
| RUN4837_3_direct_EM_bound_smoke_pass | EM_RESIDUAL_BOUND_PASS_NONCLAIM | 4.800000000000000e-03 | 4.000000000000000e-04 | 3.600000000000000e-03 | 8.800000000000001e-03 | 8.800000000000001e-03 | 1.947000000000000e-04 | 1.760000000000000e-02 |  |
| RUN4837_4_alpha_identity_smoke_pass | ALPHA_IDENTITY_BOUND_PASS_NONCLAIM | MISSING_NUMERIC_VALUE | 1.700000000000000e-04 | 1.700000000000000e-03 | 2.074000000000000e-03 | 2.074000000000000e-03 | 4.588724999999999e-05 | 4.148000000000000e-03 |  |
| RUN4837_5_forbidden_unique_F2_aesthetic | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_6_forbidden_hodge_assertion | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_7_forbidden_dropped_XF2 | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_8_forbidden_calibrated_alpha_derived | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_9_forbidden_poynting_ignored | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_10_forbidden_charge_norm_cheat | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_11_forbidden_unit_rescaling | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_12_forbidden_measured_GM_source | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_13_forbidden_cancellation | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |
| RUN4837_14_forbidden_GR_import | FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | MISSING_NUMERIC_VALUE | FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE |

## Decision ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC4837_0_identity | Calibrated Maxwell stress/Poynting is usable as a conditional bookkeeping identity. | The corpus already records variation of calibrated Maxwell action as a source interface, but Hodge/current/F2 gates remain. | use EM stress in local source ledger only with residual gates visible |
| DEC4837_1_zero | The live EM zero theorem is not signed. | Unique F2 fails current corpus, C_XF2 is an exact alpha throat, charge-current normalization and Poynting flux remain open. | retain EM source row |
| DEC4837_2_alpha | Alpha may be calibrated locally but not claimed derived. | This lets Maxwell/GR source bookkeeping proceed honestly while any nonzero C_XF2 branch must face clock/WEP/R10 bounds. | do not sell calibrated alpha as a prediction |
| DEC4837_3_next | Return to kappa/G/source normalization and Newtonian limit. | EM is now fenced; the decisive GR/Newton denominator is the Hilbert source-current/kappa/G branch. | 4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md |

## Validation

| validation_id | result | detail |
| --- | --- | --- |
| VAL4837_00_sources_exist | PASS | all cited source paths exist |
| VAL4837_01_needles_found | PASS | all source needles found |
| VAL4837_02_output_count | PASS | all runner rows emitted |
| VAL4837_03_expected_statuses | PASS | runner statuses match expected pass/block/fail modes |
| VAL4837_04_live_zero_blocked | PASS | live EM zero remains blocked |
| VAL4837_05_live_bound_blocked | PASS | live EM source row remains missing |
| VAL4837_06_direct_smoke_pass | PASS | direct EM smoke computes stress, Poynting and alpha envelope |
| VAL4837_07_alpha_identity_smoke_pass | PASS | alpha identity smoke computes b_alpha product envelope |
| VAL4837_08_forbidden_routes_fail | PASS | forbidden shortcuts fail closed |
| VAL4837_09_no_claim_allowed | PASS | no runner row allows a claim |
| VAL4837_10_runner_compiles | PASS | runner compiled before execution |
| VAL4837_11_next_target_written | PASS | next target CSV written |

## Next target

`4838-Y5-R2FR-kappa-G-source-normalization-Newtonian-limit-gate.md`
