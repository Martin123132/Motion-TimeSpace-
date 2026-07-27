# 4336 Y5-R2FR open-tail PiPPN metric-transfer derivation or R10 parent-alpha fill

Marker: `PPC4161_OPEN_TAIL_PIPPN_METRIC_TRANSFER_DERIVATION_OR_R10_PARENT_ALPHA_FILL_4336`

Decision: `OPEN_TAIL_PIPPN_OPERATOR_FACTORISATION_DERIVED_NUMERIC_MATRIX_BLOCKED_BY_Q_PROFILE_METRIC_COUPLING_AND_BOUNDARY_DATA_NONCLAIM`

## Result

The open-tail PPN transfer is now derived as a symbolic operator factorisation:

```text
Pi_PPN=P_PPN G_metric^bc C_gK P_E[(K_L G_Box^bc S_q)+S_perp].
```

This is progress, but it is nonclaim. The numeric matrix remains blocked by the q-profile kernel, metric Green/coupling normalization, boundary constants, `K_perp`, and PPN normalization.

## Bottleneck

| item | status | notes |
| --- | --- | --- |
| open-tail Pi_PPN transfer | SYMBOLIC_FACTORISATION_DERIVED | Pi_PPN=P_PPN G_metric C_gK P_E[(K_L G_Box S_q)+S_perp] |
| metric response coupling | OPEN_CRITICAL | C_gK and G_metric are the coupling/metric-response bottleneck |
| S_q q-profile kernel | OPEN_CRITICAL | needs physical q_loc(x), amplitude, boundary profile and source weights |
| R10 alpha(lambda) fallback | BLOCKED | parent alpha coefficients and claim-valid bound curve still missing |
| next target | NEXT_TARGET | source S_q and metric coupling first; pivot to R10 only if that stalls |

## Blockers

| blocked_route | missing_input | needed_for_release | status |
| --- | --- | --- | --- |
| numeric Pi_PPN open-tail matrix | MISSING_SQ_QLOC_KERNEL | source-backed map from T_open components to q_loc^nu(x), including local profile, shell width, boundary amplitude and sector weights | blocked |
| q_loc to A_loc amplitude | MISSING_BOX_GREEN_BOUNDARY_CONSTANT | static/retarded Green-function choice and inner/outer boundary conditions for A_loc^nu | blocked |
| K_tr to metric perturbation | MISSING_METRIC_GREEN_OPERATOR_AND_CgK_COUPLING | parent-signed weak-field equation fixing how K_tr,loc sources h_mu_nu and its coupling normalization | blocked |
| transverse/homogeneous source safety | MISSING_KPERP_SOURCE_OR_ZERO | derive K_perp=0, order-three suppression, or independent PPN-safe bound | blocked |
| gamma/beta/preferred-frame readout | MISSING_PPN_PROJECTION_NORMALIZATION | same metric/clock/rod normalization against Newtonian U used by local tests | blocked |
| R10 alpha(lambda) fallback | MISSING_R10_PARENT_ALPHA_COEFFICIENTS_AND_CLAIM_VALID_BOUND_CURVE | Z_X, M_X^2, K_X, Qbar_XH, qbar_XT/P_A plus full source-backed alpha(lambda) curve | blocked |

## Next

| next_target | target_question | preferred_route |
| --- | --- | --- |
| 4337-Y5-R2FR-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md | Can S_q and C_gK/G_metric be derived or source-filled enough to make Pi_PPN numeric, or must the work pivot to R10 parent alpha coefficients? | derive/source the q-profile kernel S_q and weak-field metric coupling C_gK from the parent local equations, then compute gamma/beta/preferred-frame rows |
