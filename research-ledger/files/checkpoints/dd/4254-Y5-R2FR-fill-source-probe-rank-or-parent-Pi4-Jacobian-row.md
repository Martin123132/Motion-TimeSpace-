# 4254 - Fill source-probe rank or parent Pi4 Jacobian row

**Status:** `SOURCE_PROBE_SVD_RANK_RUNNER_BUILT_CURRENT_DQ_VALUES_MISSING_NONCLAIM`.

## Result

4254 builds the executable weighted rank runner:

```text
sigma_S^2 = lambda_min(S^T W S),
E_Dq,H = sqrt(sum_i w_i epsilon_i^2),
A_H <= (C_S C_perp/sigma_S) E_Dq,H + eta_domain.
```

The existing 4243 Dq rows are explicit `MISSING`, so the runner is ready but not scoreable.

## Next Target

`4255-Y5-R2FR-fill-first-Dq-probe-matrix-row-or-parent-Pi4-source-row.md`
