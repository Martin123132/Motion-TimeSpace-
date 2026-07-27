# 3157 - LWlambda Factor or First Source-Domain Multipole Fill under AX1090

Private checkpoint. This follows 3156:

```text
either derive/source L_Wphys_Lambda,
or choose the first concrete source/domain and fill J2 or E_ext with source-backed values.
```

## Result

3157 attacks the missing product directly:

```text
L_Wphys_Lambda := L_W_phys ||Lambda||_*.
```

The main result is a guard:

```text
L_Wphys_Lambda cannot be made small by changing norm convention.
```

If the boundary norm rescales as:

```text
||.|| -> a ||.||,
```

then:

```text
L_W_phys -> L_W_phys/a,
||Lambda||_* -> a ||Lambda||_*,
```

so:

```text
L_W_phys ||Lambda||_*
```

is invariant.

That means the product must be derived, zeroed, or bounded. It cannot be hidden in notation.

## Control Routes

3157 gives four honest routes.

### Route A - Kernel Physical Annihilator

If:

```text
D_z Wbar P_phys = 0,
```

then:

```text
L_Wphys_Lambda = 0.
```

This is stronger than the 3154 pure-gauge theorem. It would mean `Wbar` is blind to physical boundary drift, not merely gauge drift. Current corpus does not sign this.

### Route B - Primitive Zero

If:

```text
Lambda = 0
```

in:

```text
B_surf = d_S Lambda + h + r,
```

then:

```text
L_Wphys_Lambda = 0.
```

Current corpus does not parent-sign a boundary condition that kills `Lambda` without deleting physical charges.

### Route C - Hodge/Poincare Primitive Bound

If the boundary complex, gauge condition, and cohomology/corner policy are parent-owned:

```text
||Lambda||_* <= C_Hodge(S,norm,boundary_condition) ||B_exact||_*.
```

Then:

```text
L_Wphys_Lambda <= L_W_phys C_Hodge ||B_exact||_*.
```

This is the finite theorem route, but `L_W_phys`, `C_Hodge`, and `||B_exact||_*` are not sourced yet.

### Route D - Source-Domain Reverse Cap

If a source-domain value is filled first, then the product must satisfy the reverse cap:

```text
L_Wphys_Lambda <= cap/B_component.
```

This lets us test whether a proposed `J2`, tide, or spin value is even compatible before claiming anything.

## Reverse Caps

The inherited single cap is:

```text
5.970964001482571e-04.
```

The equal diagnostic cap is:

```text
9.951606669137618e-05.
```

For a generic component:

```text
L_Wphys_Lambda <= cap/B_component.
```

For quadrupole/J2:

```text
L_Wphys_Lambda <= cap/(C2 * epsilon_G * (R_body/R)^2 * |J2|).
```

For an external tide:

```text
L_Wphys_Lambda <= cap c^2/(C_tide * ||E_ext|| * R^2).
```

For spin/frame dragging:

```text
L_Wphys_Lambda <= cap c^3 R^2/(C_spin * G * |J|).
```

No numeric values are filled here.

## Gate Status

| gate | status | reason |
|---|---|---|
| norm-scaling guard | `pass_nonclaim` | product is invariant under dual norm scaling |
| physical kernel annihilator | `fail_for_claim` | only pure-gauge annihilator is proved |
| primitive zero | `fail_for_claim` | no parent boundary condition kills `Lambda` safely |
| Hodge/Poincare inputs | `fail_for_claim` | `C_Hodge`, `B_exact`, domain constants missing |
| reverse caps | `pass_nonclaim` | `J2`, tide, and spin product ceilings are now explicit |

## Meaning

3157 prevents a quiet cheat and makes the next fill disciplined.

We cannot say:

```text
choose units/norms so L_Wphys_Lambda is small.
```

We can only say:

```text
prove L_Wphys_Lambda = 0,
or source/bound it,
or fill a source-domain component and demand the reverse product cap.
```

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_LWLAMBDA_CONTROL_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_LWLAMBDA_GATE_STATUS.csv` |
| product contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_LWLAMBDA_PRODUCT_CONTRACT.csv` |
| reverse caps | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_REVERSE_SOURCE_CAPS.csv` |
| score impact | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_SCORE_IMPACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3157_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3157_LWlambda_factor_or_first_source_domain_multipole_fill.py` |

## Decision

3157 does not promote local closure, local-GR recovery, WEP, R10, PPN, clock, orbital, Maxwell, or Newton claims.

It promotes the next target to:

```text
3158:
choose a concrete source/domain and run a reverse-cap smoke test,
or derive the Hodge/Poincare primitive product factors.
```

The strongest practical next move is a nonclaim reverse-cap smoke test: pick one controlled domain, fill provisional source-backed `J2` or `E_ext`, and report the required ceiling on `L_Wphys_Lambda`.
