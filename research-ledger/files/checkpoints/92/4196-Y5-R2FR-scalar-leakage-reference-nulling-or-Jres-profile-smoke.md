# 4196 - Y5 R2FR Scalar Leakage Reference Nulling Or Jres Profile Smoke

Decision: `SCALAR_REFERENCE_NULLING_THEOREM_SHARPENS_ROUTE_STATIONARITY_ALONE_REJECTED_ZTHETA_ZDOTB_NEED_PARENT_REVERSAL_OR_ENVELOPE_ZLCG_PRUNED_JRES_PROFILE_NEXT`

## Summary

4196 tries to derive scalar leakage reference nulling.

It proves:

```text
stationary background alone is insufficient;
parent reversal/involution is sufficient;
parent envelope/extremum is sufficient only for readouts owned by the minimized functional;
smooth Q_theta/Q_dotB repair is clean but not parent-derived;
z_Lcg must stay pruned unless its reference or RG role is parent-derived.
```

## What Moved

The old scalar-channel problem is now less foggy:

- `z_theta` and `z_dotB` are not killed by ordinary spatial symmetry.
- They can be killed by a parent local reversal/equilibrium theorem or by envelope ownership.
- `z_Lcg` is not a physical primitive source until its reference is derived.
- The clean closure branch is mathematically sane enough to profile numerically, but not claim.

## Next

Run `4197-Y5-R2FR-normalized-Jres-profile-smoke-with-4194-budgets.md` to stop circling the symbolic obstruction and see whether the private clean-closure branch has plausible amplitude against the 4194 `Gdot/G` and gradient budgets.
