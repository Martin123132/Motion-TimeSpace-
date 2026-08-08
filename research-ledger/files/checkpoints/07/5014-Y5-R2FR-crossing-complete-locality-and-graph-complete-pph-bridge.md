# 5014 — crossing-complete locality and graph-complete pph bridge

## Result

The `J=4` target introduced in checkpoint 5013 is not a legal locality test. Bern's sourced real two-loop equation contains the full crossing object `[Re(M) Re(F)]^(2)`, whereas 5013 imposed locality mode by mode on one direct-channel discontinuity. Crossing acts on the complete infinite tower before locality is assessed.

An exact counterexample makes this decisive. Define

```text
w_q=q^4/(s^4+t^4+u^4),
F_q=w_q stu,
d_s(z)=F_s/s^3=2(1-z^2)/(z^2+3)^2.
```

Every even direct partial wave of `d_s`, including `J>=4`, is nonzero, but `F_s+F_t+F_u=stu` exactly. Therefore neither `D_3,J=-D_hh,J` nor the claimed reduction of the three-particle problem to only `J=0,2` follows from locality. Checkpoint 5013 is superseded on those statements; its exact full-real `F1` moments remain useful.

## Graph-complete 4988 match

The three independently Ward-safe Luna Bose pairings have exact soft coefficients

```text
C_s=-(t-u)^2/(4s),
C_t=-(s-u)^2/(4t),
C_u=-(s-t)^2/(4u),
C_s+C_t+C_u=C4.
```

On `s+t+u=0`,

```text
C_t+C_u=-s^2/t-s^2/u-7s/4.
```

Hence the hard exchange packet removed in checkpoint 4988 has the unique graph-complete five-point lift

```text
M5_sing=M_t+M_u+(7s/4)S_vec,
M5_reg=M_s-(7s/4)S_vec.
```

No coefficient was fitted. Every pair block and `S_vec` is separately Ward safe, and the measured soft-factor residual is `2.006e-05`.

## Integrated direct-channel result

The robust sampler uses two-endpoint importance sampling for the external angle and four-axis mixtures around both incoming and outgoing hard directions for each internal sphere. It integrates the angular-first plus distribution with `20`-point Gauss-Legendre quadrature and `32768` Sobol geometries per seed.

| J | raw angular-first D/G^3 | graph-complete 4988 D/G^3 |
|---:|---:|---:|
| 0 | 6.37412526 +/- 0.5 | 3.08790981 +/- 0.033 |
| 2 | 5.87029813 +/- 0.35 | 0.0295153559 +/- 0.016 |
| 4 | 3.60440369 +/- 0.26 | -0.006683951 +/- 0.01 |
| 6 | 2.13950643 +/- 0.37 | 0.00704332097 +/- 0.0055 |
| 8 | 1.42584397 +/- 0.4 | 0.0132240893 +/- 0.0062 |

The raw column retains the hard `t/u` exchange packet and is a scheme diagnostic only. The graph-complete column is the direct `phi phi h` contribution matched to checkpoint 4988. Neither column is compared to the rejected 5013 `J=4` target.

## Status

- Pairwise Luna soft-channel map and Ward identities: **derived and checked**.
- Graph-complete finite-`x` 4988 subtraction: **derived, not fitted**.
- Angular-first raw and matched plus integrals: **executed with multi-seed RQMC**.
- Checkpoint 5013 direct per-`J` locality rule: **superseded**.
- Crossing continuation of the direct function and graph-complete `hhh` integral: **next active calculation**.
- Coupled crossing-local projection, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: analytically continue the graph-complete direct kernels into the crossed `t/u` sheets (or derive the equivalent crossing kernel), add the `hhh` sector, and test locality only on the complete cyclic object.
