# 4237 - AJ Source Coefficient Theorem Or Numeric Fill Pack

**Status:** `AJ_SOURCE_COEFFICIENT_THEOREM_DERIVED_TO_VERTICAL_CURRENT_AND_M2_SHAPE_FUNCTION_NUMERIC_FILL_OPEN_NONCLAIM`.

## Forward Move

4237 turns:

```text
A_src + A_lap + A_drift
```

into:

```text
S_A H_L^A + D_m Delta_h M_2 - D_t M_2,
M_2 = 1/2 H_AB H_L^A H_L^B.
```

That is the derivation leap: the obstruction is now a vertical-current/M2 profile problem, not three disconnected closure constants.

## Still Not A Pass

The required source rows are not filled:

```text
S_A H_L^A,
Delta_h M_2,
D_t M_2,
D_m,
T_res/tau_L,
c_Gamma,
profile_a/J_a.
```

## Next

`4238-Y5-R2FR-vertical-current-M2-zero-theorem-or-profile-sampler.md`
