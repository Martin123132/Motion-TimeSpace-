# 5036 — paired epsilon full cyclic vector and local/nonlocal decomposition

**Status: COMPLETE — the bounded paired full-vector smoke gate passes; the epsilon-zero and fixed-target physics gates remain open.**

## Exact estimator

For every physical s-channel cosine `z`,

```text
t/s = -(1-z)/2,
u/s = -(1+z)/2,
z_t = (3+z)/(1-z),
z_u = -(3-z)/(1+z),

C_epsilon(z) = D(z+i epsilon)
             + (t/s)^3 D(z_t+i epsilon)
             + (u/s)^3 D(z_u+i epsilon).
```

The same scrambled Sobol event is used at `epsilon=(0.08,0.04,0.02)`.
Successive differences are therefore paired regulator differences, not
differences between unrelated outer samples.

## Local/nonlocal split

For the locked vector at `z=(-0.6,-0.3,0,0.3,0.6)` and
`phi(z)=1-z^2`, each event is decomposed before the fixed 5018 target is
loaded:

```text
a_epsilon = (phi dot C_epsilon)/(phi dot phi),
R_epsilon = C_epsilon-a_epsilon phi,
phi dot R_epsilon = 0.
```

The projection is complex at finite regulator. The target determines neither
`a_epsilon`, the residual, the kernels nor the extrapolation.

## Closed run

The immutable run is
`source-intake/functional_rg/5036/runs/paired_full_vector_s2_v1`, with config
digest
`c0aa91447dc8a438175bd493f32a9b9fff8d04037c640dfb55d4737c67972c81`.

```text
expected/terminal jobs = 99/99
exact source imports   = 51
new converged kernels  = 48
failed/unconverged     = 0/0
v4 radius adjustments = 0
```

Every new kernel uses its own target-specific canonical projective Feynman
homotopy and the shrinking-radius `v4` pair-local residue rule. All 48 closed
at the initial `0.1*safe_scale` circle. No raised path, topology-class
interpolation or representative kernel is used.

## Full-vector ladder

The two-scramble means are ordered by increasing `z`:

```text
epsilon=0.08
  (187.200592-8.552235i, 73.631174-4.572872i,
    51.588107-4.036278i, 65.508951+15.037658i,
    55.782011+0.839938i)

epsilon=0.04
  (187.420976-4.520057i, 73.748562-2.359300i,
    51.800979-2.021891i, 75.275815+11.670801i,
    55.752727+0.557826i)

epsilon=0.02
  (187.481228-2.498005i, 73.785658-1.252448i,
    51.856331-1.006513i, 79.281696+6.737080i,
    55.744673+0.394230i).
```

The corresponding local coefficients are

```text
epsilon=0.08 : 96.021893+0.158487i
epsilon=0.04 : 98.706431+1.126704i
epsilon=0.02 : 99.790585+0.759074i.
```

## Convergence gates

All tests use the paired mean differences, not unpaired error bars:

```text
quantity                    0.08->0.04   0.04->0.02   p_eff
full-vector L2 step          11.494850      6.838742    0.749185
local-coefficient step        2.853803      1.144789    1.317804
nonlocal z=-0.6               3.726722      2.344572    0.668582
nonlocal z=-0.3               2.680240      1.726019    0.634914
nonlocal z= 0.0               2.683954      1.723701    0.638851
nonlocal z=+0.3               8.466696      5.501692    0.621924
nonlocal z=+0.6               1.966356      0.705564    1.478677
```

Thus the full vector, the local coefficient and every nonlocal component
contract on this bounded ladder. The largest eventwise projection residual is
`6.75017e-14`. The largest central global-24/global-32 relative difference is
`1.97538e-14`. These close the numerical smoke gate, not the physical
epsilon-zero limit.

## Linear diagnostic and fixed target

Without assuming it is the true asymptotic law, the linear diagnostic
`2*C_0.02-C_0.04` gives

```text
full vector =
  (187.541481-0.475954i, 73.822754-0.145595i,
    51.911683+0.008865i, 83.287576+1.803358i,
    55.736619+0.230633i)

local coefficient = 100.874739+0.391444i.
```

Only after that eventwise decomposition is the real nonlocal residual compared
with the untouched 5018 target:

```text
z       predicted      two-scramble SE      target       difference
-0.6    122.981648          30.421749       28.710948     94.270700
-0.3    -17.973259           6.635836       -9.009423     -8.963836
 0.0    -48.963056           9.586162      -20.453828    -28.509228
+0.3     -8.508436          37.089649       -8.940934      0.432498
+0.6     -8.823214          46.728802       28.771322    -37.594536
```

The unweighted residual RMS is `47.3152`, essentially unchanged from the
finite-regulator 5034 smoke. This is not a target match. It is also not a
rejection: two independent one-point scrambles provide only one variance
degree of freedom. The two extrapolated events separately give local
coefficients `116.7801` and `84.9694`, and the visible `z<->-z` imbalance is
another direct warning that outer variance remains dominant. Gaussian-sigma
language is not valid here.

## Decision

Checkpoint 5036 establishes one real forward result: the canonical transported
cut can be evaluated across the full cyclic vector and its regulator steps
contract in the predicted local direction and in all five untouched nonlocal
components. It does **not** establish the epsilon-zero coefficient, production
precision, a 5018 match, crossing-complete `hhh`, local GR or full MTS.

The next target is a bounded outer-precision and reflection-control run. Add
independent paired scrambles without imposing `z<->-z` symmetry, verify error
scaling and extrapolation stability, and only then make a fixed-target verdict.
No target fitting and no GitHub action are authorized.

Marker: `MTS_5036_PAIRED_EPSILON_FULL_CYCLIC_VECTOR`.
