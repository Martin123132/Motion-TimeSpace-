# 3168 - Anisotropic Shapiro Quadrupole Kernel or Source Transfer Contract under AX1090

Private checkpoint. This follows 3167 by deriving the line-of-sight quadrupole kernel that scalar Cassini `gamma` does not directly test.

## From Scalar Gamma To Line-of-Sight Quadrupole

3167 proved the scalar readout fact:

```text
<P2>_S2 = 0
```

so a pure `l=2` residual does not directly shift the scalar PPN monopole `gamma-1`.

3168 asks the next physical question:

```text
does the same pure P2 residual affect an actual Shapiro/light ray?
```

Yes, generically.

For a small spatial-trace residual of the form:

```text
delta g_ij = A W(r) P2(cos theta) delta_ij
```

the first-order null travel-time perturbation has the shape:

```text
Delta t_Q = (A/(2c)) int_path W(r(s)) P2(cos theta(s)) ds.
```

In the current lane:

```text
A = K_2 C_K2_unit.
```

The convention factor can be absorbed into the final observable projection if the exact metric normalization differs. The important point is that the line-of-sight functional is not the same as the spherical monopole functional.

## Normalized Kernel

Define the normalized quadrupole line-of-sight kernel:

```text
Pi_quad_LOS[W] =
int W(r(s)) P2(cos theta(s)) ds / int W(r(s)) ds.
```

Then:

```text
Delta_quad_norm = K_2 C_K2_unit Pi_quad_LOS.
```

Since:

```text
P2(x) in [-1/2, 1]
```

and for a positive radial weight `W >= 0`:

```text
|Pi_quad_LOS| <= 1.
```

This is a rigorous profile-agnostic envelope.

## Straight-Ray Geometry

Let:

```text
x(s) = b_vec + s k
```

where `k` is the light-ray direction, `b_vec` is the impact vector, and `a` is the source quadrupole axis.

For any even radial weight `W(r)`:

```text
Pi_Q =
(3/2) [(a.bhat)^2 B_W + (a.k)^2 (1 - B_W)] - 1/2
```

with:

```text
B_W = <b^2/(b^2+s^2)>_W.
```

For a Shapiro-style `W=1/r` weight and symmetric endpoints `s in [-L,L]`, with:

```text
rho = L/b,
```

the closed form is:

```text
B_1/r(rho) = rho / (sqrt(1 + rho^2) asinh(rho)).
```

So the quadrupole kernel is now a computable geometry object, not a handwave.

## Example Kernels

For `W=1/r`:

| rho=L/b | axis parallel to ray | axis along impact | axis transverse |
|---:|---:|---:|---:|
| 1 | -2.034172425867156e-1 | 7.034172425867156e-1 | -5.000000000000000e-1 |
| 3 | 2.174501812515741e-1 | 2.825498187484259e-1 | -5.000000000000000e-1 |
| 10 | 5.021865251326121e-1 | -2.186525132612138e-3 | -5.000000000000000e-1 |
| 100 | 7.169067413687833e-1 | -2.169067413687832e-1 | -5.000000000000000e-1 |
| 1000 | 8.026551177773267e-1 | -3.026551177773267e-1 | -5.000000000000000e-1 |

The important lesson is that the line-of-sight quadrupole kernel can be order unity. Spherical orthogonality does not imply Shapiro invisibility.

## Quadrupole Gate Contract

The real anisotropic gate is:

```text
K_2 <= epsilon_quad / (|Pi_quad_LOS| C_K2_unit).
```

Here:

```text
C_K2_unit = 3.593766357482964e-24.
```

What is still missing is:

```text
epsilon_quad
```

the empirical anisotropic/STF Shapiro or light-bending residual bound in the correct convention.

The scalar Cassini `gamma` envelope:

```text
6.7e-5
```

may be used only as a borrowed smoke scale, not as a quadrupole bound. If one temporarily borrows it with `|Pi_quad_LOS|=1`, the smoke bound is:

```text
K_2 <= 1.864339340271583e19.
```

That reproduces the 3166 unit-projection number, but now with the correct interpretation:

```text
worst-case anisotropic envelope smoke, not scalar gamma evidence.
```

## Source-Domain Transfer

The other active obstruction remains:

```text
Earth l=2 K2 lane != Solar Shapiro K2 lane
```

unless a transfer theorem is supplied.

The next usable relation is:

```text
K2_solar = T_source(Earth_l2_to_solar_los) K2_earth
```

or else `K2_solar` must be constructed directly from the solar/source-domain geometry.

## Claim State

3168 claims a mathematical kernel shape:

```text
Pi_quad_LOS[W] = int W P2 / int W,
|Pi_quad_LOS| <= 1,
```

and a closed straight-ray `W=1/r` example.

3168 does not claim:

- PPN safety;
- Shapiro safety;
- light-bending safety;
- local-GR recovery;
- source-domain universality;
- Cassini quadrupole residual pass;
- scalar gamma pass;
- Earth-to-solar transfer.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3168_anisotropic_Shapiro_quadrupole_kernel.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_INPUTS.csv` |
| LOS kernel derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_LOS_KERNEL_DERIVATION.csv` |
| orientation examples | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_ORIENTATION_EXAMPLES.csv` |
| quadrupole gate contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_QUADRUPOLE_GATE_CONTRACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3168_VALIDATION.csv` |

## Decision

3168 promotes the next target to:

```text
3169-Y5-R2FR-STF-Shapiro-source-bound-or-solar-domain-K2-transfer-under-AX1090.
```

Best next attack:

```text
source a real anisotropic/STF Shapiro or light-bending bound,
or derive a solar-domain K2 transfer law.
```

This is the right place to push next because the kernel is now derived; the remaining question is whether the data/readout side supplies an actual `epsilon_quad`.
