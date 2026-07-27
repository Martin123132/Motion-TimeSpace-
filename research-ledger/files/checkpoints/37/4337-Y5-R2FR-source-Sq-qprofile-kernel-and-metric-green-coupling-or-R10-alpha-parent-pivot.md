# 4337 Y5-R2FR source S_q q-profile kernel and metric Green coupling or R10 alpha parent pivot

Marker: `PPC4161_SOURCE_SQ_QPROFILE_KERNEL_AND_METRIC_GREEN_COUPLING_OR_R10_ALPHA_PARENT_PIVOT_4337`

Decision: `ORDINARY_COUPLING_IMPORTED_AS_CALIBRATED_KAPPA_EFF_OPEN_TAIL_COUPLING_REDUCED_TO_CGAMMA_PROFILE_COEFFICIENT_NONCLAIM`

## Result

The 4336 coupling bottleneck has been split:

```text
C_matter = kappa_eff = 8*pi*G_cal/c^4
C_gK^Gamma = kappa_eff c_Gamma
```

Ordinary matter coupling is structurally imported as calibrated GR-like coupling. Open transition tails reduce to `c_Gamma` times the q-profile/source-kernel rows. So the next target is no longer “find the coupling”; it is “prove `c_Gamma=0`/metric-null, or source finite `c_Gamma` and profile coefficients.”

## Benchmarks

| branch | S_PPN_unit_cGamma | cGamma_max_for_gate | unit_cGamma_status | interpretation |
| --- | --- | --- | --- | --- |
| direct linear q_profile | 1.0131066902400628e-01 | 9.8706287268031276e-05 | FAIL | direct AU linear memory projection survives only if c_Gamma is below about 1e-4 or F1/M_tr is further suppressed |
| quadratic fixed-point q_profile | 1.4327492214684143e-06 | 6.9795885072972315e+00 | CONDITIONAL_PASS_SOURCE_AMPLITUDE_ONLY | quadratic branch can tolerate c_Gamma order unity at this source-amplitude proxy, but only if the fixed-point/no-hair profile is parent-owned |

## Blockers

| blocked_route | missing_input | needed_for_release | status |
| --- | --- | --- | --- |
| numeric open-tail PPN matrix | MISSING_CGAMMA_PARENT_ZERO_OR_FINITE_SOURCE_VALUE | parent metric-null/source-kernel theorem or finite c_Gamma normalization fixed before local tests | blocked |
| S_q profile scoring | MISSING_A_SRC_A_LAP_A_DRIFT_TRES_TAUL_PROFILE_ROWS | A_src, A_lap, A_drift, T_res/tau_L and arena projection coefficients from parent/profile source rows | blocked |
| quadratic fixed-point source-amplitude pass | MISSING_PARENT_DOUBLE_ZERO_NOHAIR_PROFILE | F1=0, bounded M_tr, ell_tr/L_cg and no unsuppressed boundary/source injection from parent law | blocked |
| R10 alpha(lambda) fallback | MISSING_R10_PARENT_ALPHA_COEFFICIENTS_AND_CLAIM_VALID_BOUND_CURVE | Z_X, M_X^2, K_X, Qbar_XH, qbar_XT/P_A plus full source-backed alpha(lambda) curve | blocked |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4338-Y5-R2FR-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md | Can c_Gamma be parent-zero/metric-null, or can finite c_Gamma and S_q profile coefficients be source-filled enough to score PPN? | derive metric-null source-kernel theorem: Sigma_metric[q_tr]=0 or c_Gamma=0 in compact local collars |
