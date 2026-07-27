# 4215 Y5 R2FR reference-lock curl zero or first ref bound row

**Status:** `REFERENCE_LOCK_CURL_ZERO_CONDITIONALLY_DERIVED_FOR_PARENT_SELECTED_SOURCE_BLIND_HREF_DELTA_REF_BOUND_ROW_RETAINED_NONCLAIM`.

**Forward move:** `I_ref` is conditionally zero for a parent-selected fixed source-blind reference:

```text
H_ref fixed before source/radius/frame/readout variation
=> d_field(delta H_ref)=0
=> I_ref=curl(-delta H_ref)=0.
```

If `H_ref` is fitted from observed residuals or drifts with source/readout/radius/frame, it is not a reference; it is a residual counterterm and must be scored.

## Files written

- `formalization-workbench\231-PPC4161-reference-lock-curl-zero-or-bound.md`
- `source-intake\mts_residuals\P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_4215_REFERENCE_BOUND_COMPONENTS.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_4215_DECISION.csv`

## Next target

`4216-Y5-R2FR-tau-surface-frame-lock-or-curl-bound-row.md`.
