# 4197 - Y5 R2FR Normalized Jres Profile Smoke With 4194 Budgets

Decision: `NORMALIZED_JRES_SMOKE_FINDS_STRONG_LOCAL_WINDOW_PLAUSIBLE_ONLY_WITH_SMALL_AMPLITUDE_OR_RELAXATION_PRODUCT_WEAK_LOCAL_WINDOW_HARD_NONCLAIM`

## Summary

4197 runs the numeric smoke test requested by 4196.

It imports the 4194 normalized budgets and scans:

```text
A_J in [1e-06, 0.0001, 0.01, 0.1, 1.0, 10.0]
scale in [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
boundary_AJ_equiv in [0.0, 1e-06, 0.0001, 0.01, 1.0]
```

against strong/weak local windows, `|c_Gamma|` rows, `Gdot/G`, and gradient constraints.

## Main Result

The branch is not killed, but it is not free.

- Strong local window: plausible if `A_J,eff` is small or `mu_Xi T_res` is order several for `A_J,eff~1`.
- Weak local window: hard for `|c_Gamma|~1`; it needs tiny `A_J,eff`, small `|c_Gamma|`, or very large relaxation product.
- Dominant constraint: `Gdot/G`.
- No claim: all numbers are assumption-grid rows.

## Next

`4198-Y5-R2FR-parent-amplitude-owner-for-AJ-muXiTres-cGamma.md` should stop treating `A_J` as a mystery box and try to derive or bound it from the parent source/operator normalization.
