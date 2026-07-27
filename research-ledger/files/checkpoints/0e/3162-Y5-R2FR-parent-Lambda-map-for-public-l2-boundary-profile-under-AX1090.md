# 3162 - Parent Lambda Map for Public l2 Boundary Profile under AX1090

Private checkpoint. This follows 3161 by attacking the unsigned map:

```text
public metric l=2 boundary profile -> parent exact primitive Lambda.
```

3161 computed `B_exact` only under the conditional identification:

```text
Lambda(theta) = A_public P2(cos theta).
```

3162 asks whether that identification is parent-signed.

## Result

The round-sphere mathematical map is clean.

For the selected first-domain sphere:

```text
Lambda = A P2(cos theta)
```

has:

```text
d_S Lambda
```

as an exact boundary 1-form, `l=2` is zero-mean, and `H^1(S^2)=0` removes harmonic 1-form ambiguity.

But the parent action has not signed that the public metric profile is the parent exact primitive.

So the correct interface is:

```text
Lambda_parent := M_Lambda A_public P2(cos theta).
```

The old hidden assumption was:

```text
M_Lambda = 1.
```

3162 does not promote that assumption.

## Contract

From 3161, for the Earth J2 full-shell metric profile:

```text
A_public = 1.505618541755115e-12.
```

For `M_Lambda = 1`, 3161 found:

```text
||Lambda||_hat = 2.386903626527921e-12
B_exact        = 5.846695950192112e-12.
```

3162 therefore rewrites these as:

```text
||Lambda||_hat(M_Lambda) = |M_Lambda| * 2.386903626527921e-12
B_exact(M_Lambda)        = |M_Lambda| * 5.846695950192112e-12.
```

The tightest `l=2` first-domain cap becomes:

```text
L_W_phys |M_Lambda| <= 1.661478072732745e20.
```

Using the more conservative general sphere Hodge constant:

```text
L_W_phys |M_Lambda| <= 9.592548125449111e19.
```

## What Is Proved

3162 proves the mathematical part:

- the `l=2` scalar profile has a canonical exact surface derivative;
- the zero-mean gauge fixes the scalar constant;
- `S^2` has no harmonic 1-form channel;
- the metric multipole/tide component is not allowed to be erased as gauge.

This means the remaining ambiguity is not geometric fog. It is the parent map scale:

```text
M_Lambda.
```

## What Is Not Proved

The current corpus does not prove:

```text
M_Lambda = 1.
```

The blockers are specific:

- the parent boundary primitive is formula-shaped but not derived;
- the total q-basic boundary sector is not parent-signed;
- counterterm/reference/residual mixing is still live;
- public readout `g_obs` may not equal the primitive that appears in `B_surf=d_S Lambda+h+r`.

So 3162 blocks the public claim.

## Countermodel Guards

The live countermodels are:

```text
Lambda_parent = M_Lambda A_public P2,    M_Lambda != 1.
```

or:

```text
Lambda_parent = M_Lambda A_public P2 + Lambda_ref + Lambda_corner + Lambda_residual.
```

or:

```text
public l=2 profile is readout-only and not the parent boundary primitive.
```

The forbidden shortcut is:

```text
public l=2 multipole/tide drift is pure gauge.
```

That shortcut is blocked because physical metric multipole/tide drift must be bounded or theorem-zeroed, not quotiented away.

## Claim State

No claim is promoted.

3162 does not claim:

- local closure;
- local-GR recovery;
- WEP;
- R10;
- PPN safety;
- clock safety;
- orbital safety;
- Maxwell recovery;
- Newtonian recovery.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3162_parent_Lambda_map_for_public_l2_boundary_profile.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_INPUTS.csv` |
| map audit | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_PARENT_LAMBDA_MAP_AUDIT.csv` |
| coefficient contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_MLAMBDA_COEFFICIENT_CONTRACT.csv` |
| countermodel guards | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_COUNTERMODEL_GUARDS.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3162_VALIDATION.csv` |

## Decision

3162 promotes the next target to:

```text
3163-Y5-R2FR-MLambda-scale-from-qbasic-boundary-primitive-or-closure-under-AX1090.
```

Best next attack:

```text
derive M_Lambda from the strong q-basic boundary primitive,
or carry L_W_phys |M_Lambda| as the explicit closure product.
```

If `M_Lambda = 1` is derived, then `L_W_phys` is the final unresolved local product factor. If it is not derived, the local branch can still be tested, but only as a closure branch with `L_W_phys |M_Lambda|` bounded.
