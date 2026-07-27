# 4253 - Source Jacobian or first direct Hperp profile fill

**Status:** `NO_PARENT_JACOBIAN_FOUND_DQ_DEFECT_TO_HPERP_TOMOGRAPHY_BRIDGE_DERIVED_NONCLAIM`.

## Result

No live source-backed `Y_m/Y_a` Jacobian candidate exists yet, and 4253 rejects hand-choosing `Pi4`.

The forward move is the new source-probe tomography bridge:

```text
A_H <= sigma_S^-1 C_S C_perp E_Dq,H + eta_domain,

h_U_C1 <= sigma_S1^-1 C_S1 C_perp E_Dq,H_C1
          + (||nabla S||/sigma_S1) A_H
          + eta_C1.
```

So the first direct `Hperp` profile can be filled either from parent `Pi4/X_m/X_a` rows or from source-probe rank plus Dq-defect envelopes.

## Next Target

`4254-Y5-R2FR-fill-source-probe-rank-or-parent-Pi4-Jacobian-row.md`
