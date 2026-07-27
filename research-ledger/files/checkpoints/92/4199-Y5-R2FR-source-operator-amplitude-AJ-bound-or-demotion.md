# 4199 - Y5 R2FR Source Operator Amplitude AJ Bound Or Demotion

Decision: `SOURCE_OPERATOR_AJ_BOUND_CONTRACT_DERIVED_SUPPORT_POWERS_COMPATIBLE_BUT_COEFFICIENTS_BOUNDARY_KPERP_PARENT_OWNER_MISSING_DEMOTE_IF_UNSIGNED_NONCLAIM`

## Summary

4199 derives the current best `A_J` amplitude contract:

```text
A_J,eff <= C_D C_S
         + D_m C_M C_lap/L_B^2
         + C_M C_t/T_B
         + A_boundary/U_B^2.
```

The exponent route is compatible:

```text
nS=1, nL=2.
```

But the route is still nonclaim because the coefficients, boundary routing, and `K_perp` zero/bound are not parent-signed.

## Practical Verdict

This is not circling: the next blocker is now specific.

Either prove boundary/`Kperp` zero and source-operator coefficient bounds, or demote the clean local branch to an explicit finite closure with priors.
