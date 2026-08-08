# 4255 - Fill first Dq probe matrix row or parent Pi4 source row

**Status:** `DQ_COORDINATE_PROBE_MATRIX_FILLED_AS_SEMINORM_SMOKE_PHYSICAL_NORM_BRIDGE_STILL_MISSING_NONCLAIM`.

## Result

The first 4254 source-probe matrix socket is filled by a Dq-coordinate identity matrix:

```text
S_Dq = I, sigma_Dq = 1.
```

This is deliberately nonclaim. Physical `Hperp` still needs:

```text
||Hperp||_F/F_ref <= C_HDq ||Dq[Hperp]||_W + eta_Dq_kernel.
```

## Next Target

`4256-Y5-R2FR-fill-Dq-component-values-or-physical-Hperp-Dq-norm-equivalence.md`
