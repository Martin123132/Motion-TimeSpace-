# 4252 - Mixed memory-Qshear transfer inputs or direct Hperp profile acquisition

**Status:** `MIXED_MEMORY_QSHEAR_SYMPLECTIC_EXTRACTOR_BUILT_DIRECT_PROFILE_BRANCH_STILL_SOURCE_BLOCKED_NONCLAIM`.

## Result

4252 derives the actual mixed transfer coefficients:

```text
B_a = omega(Y_m,Y_a)
    = C1_m D1_a - C1_a D1_m + C2_m D2_a - C2_a D2_m,

G_ab = omega(Y_a,Y_b)
     = C1_a D1_b - C1_b D1_a + C2_a D2_b - C2_b D2_a.
```

For a Q-shear selector `Y_Q=Pi4(X_Q)`, this is:

```text
B_a = omega(DPi4_X X_m, DPi4_X X_a),
G_ab = omega(DPi4_X X_a, DPi4_X X_b).
```

That is the useful move: the coupling is now a sourceable Jacobian contraction, not a black-box coefficient.

## Current Claim Gate

No local-GR/PPN/R10/clock/orbital claim is allowed yet. The extractor is ready, but parent-owned numeric/theorem-zero rows for `Y_m`, `Y_a`, `Z_1`, `Z_2`, and eta terms are still required.

## Next Target

`4253-Y5-R2FR-source-Jacobian-or-first-direct-Hperp-profile-fill.md`
