# 4940 - Metric-kernel O4 source, self-backreacted fixed point and direct-trace gate

Marker: `MTS_METRIC_KERNEL_O4_SOURCE_SELF_BACKREACTED_GATE_4940`.

Date: `2026-07-12`.

Status: private analytic and source-executed checkpoint. A parent-owned part
of the previously open curved motion source is now derived from the essential
metric RG kernel. It is nonzero, so `u_O4=0` is not invariant in the executed
known-source system. The resulting six-coordinate fixed point and finite
two-scale family are solved with the O4 feedback included. The separate
off-shell metric-scalar/mixed Hessian contribution on the right-hand side of
the functional trace remains open; full O4 closure and local-GR promotion are
therefore false.

## 1. Parent-owned source

The source-complete essential gravity kernel contains

```text
Psi^g_mn
  contains gamma_C2
  (C_abcd C^abcd g_mn-8 Lambda S_mn).
```

This is not a new MTS closure. It is an existing parent field-redefinition
coefficient in the hash-locked essential flow. On the Ricci-flat projection,

```text
Psi^g_mn=gamma_C2 C^2 g_mn.
```

For the canonical motion kinetic term

```text
S_psi=(1/2) integral sqrt(g) g^mn partial_m psi partial_n psi,
```

direct metric variation gives, in `d` dimensions,

```text
Psi^g_mn delta S_psi/delta g_mn
  =[(d-2)/4] gamma_C2 C^2 (nabla psi)^2.
```

Thus in four dimensions the left-hand side of the essential flow contains

```text
(gamma_C2/2) O4,

O4=C_abcd C^abcd (nabla psi)^2.
```

Because the flow convention is

```text
partial_t Gamma+Psi^A delta_A Gamma=RHS,
```

the known metric-kernel contribution to the dimensionless coupling is

```text
beta_uO4=4u_O4-gamma_C2/2+S_O4,direct.
```

This fixes both the sign and normalization of a nonzero parent source. The
remaining `S_O4,direct` denotes only the explicit metric-scalar and mixed
Hessian traces on the right-hand side; it is not folded into `gamma_C2`.

## 2. O4 feedback into the gravity solve

The scalar Hessian in a constant-Weyl projection is

```text
Gamma_psi,psi^(2)
  =(1+2u_O4 C^2)(-Box)+m^2.
```

For the optimized `eta_psi=0` threshold with

```text
D_psi=1/(1+w),
```

the term linear in `u_O4` is

```text
delta W=-2u_O4 C^2 z D_psi^2.
```

The scalar heat-kernel `a_0` and `a_2=R/6` coefficients then give the exact
feedback rows used in the source system,

```text
Delta RHS_C2
  =-u_O4 D_psi^2/(24pi^2),

Delta RHS_RC2
  =-u_O4 D_psi^2/(96pi^2).
```

The completed 4934 linear source solve is rerun at every beta evaluation;
these rows are not appended after solving. The massless scalar Newton source
is likewise inserted before the solve through

```text
Delta beta_g=g^2/[6pi(1+w)].
```

## 3. Six-coordinate ultraviolet point

Solving

```text
beta_(g,g_plus,g_minus,g_CFF,h_C3,u_O4)=0
```

with `S_O4,direct` explicitly omitted but not declared zero gives

```text
(g,g_plus,g_minus,g_CFF,h_C3,u_O4)_*
 =(0.130878136124880,
   0.371466079910460,
   3.45320848803473,
   0.00409533354414041,
   3.91680160559022e-6,
  -0.00180507540864851).
```

The beta residual is

```text
||beta||_infinity=1.42490481635e-13.
```

At this point,

```text
gamma_C2=-0.0144406032691879,

-gamma_C2/2=0.00721281432164576.
```

The five coordinates inherited from 4939 shift by at most `0.0785%`.
Therefore the forced O4 portal is dynamically nonzero but does not dislodge
the previously found interacting branch.

## 4. Stability and predictivity

The six-coordinate beta eigenvalues are

```text
lambda={
 -1.89272499395975,
  0.211673731949398,
  0.228846442027132,
  0.280756616947861,
  1.08865267955632,
  3.99602545229438
}.
```

There is exactly one relevant direction. The O4 mode is strongly irrelevant
and remains close to its canonical value `+4`; it does not introduce another
free ultraviolet datum.

Adding the regular motion mass gives

```text
theta_mass=1.84969344551166  for v=+2lambda,

theta_mass=1.85848385394298  for v=-2lambda.
```

Each seven-coordinate block has exactly two relevant directions: the gravity
scale and the already identified universal motion-gap scale. The O4 source
therefore does not worsen the two-scale predictivity count.

## 5. Gaussian Wilson limit

The source solve gives

```text
gamma_C2 proportional to g^2
```

near the Gaussian endpoint. A log-log fit over the executed sequence returns

```text
power=2.00000118097930.
```

Consequently

```text
W_O4=u_O4/g^2
```

has a finite Gaussian limit rather than a divergent one. The three massless
controls converge to approximately

```text
W_O4,IR=-3.31918.
```

This is a Wilson coefficient in the declared RG normalization, not a PPN or
laboratory fifth-force observable.

## 6. Finite two-scale family

The full known-source system was integrated for three gravity amplitudes,
seven `R_UV` values and both mass-sign maps. All 42 positive-mass runs and all
three massless controls reach `g=1e-10`.

Across the positive-mass family,

```text
-3.31918185 <=W_O4,IR<=-3.31843918.
```

The largest absolute finite-mass displacement from the matched massless
control is

```text
|Delta W_O4|<7.41e-4.
```

For `R_UV=1`, the three gravity seeds give

```text
J_gap,IR=0.23766--0.23991  for v=+2lambda,

J_gap,IR=0.22898--0.23095  for v=-2lambda.
```

The change relative to 4939 is expected: the trajectory now includes the
O4-to-gravity feedback rows at every step. Seed drift in `W_O4` remains below
`1.52e-6` relative over the complete grid.

## 7. Exact cancellation contract

The current fixed-point equation is

```text
0=4u_O4,*-gamma_C2,*/2+S_O4,direct,*.
```

An exact `u_O4,*=0` branch would therefore require

```text
S_O4,direct,*=gamma_C2(u_O4=0)_*/2
              =-0.00721281432164576
```

in the same regulator, field variables, projection and essential scheme.
Neither a generic zero nor a cancellation may now be assumed. This numeric
identity is the falsifiable target for the direct trace.

## 8. Claim boundary

```text
parent metric-kernel O4 source                 = derived nonzero;
scalar O4 feedback into C2 and RC2 rows        = derived and included;
six-coordinate known-source fixed point        = solved;
known-source finite two-scale O4 family         = solved;
O4 adds a relevant direction                   = false;
u_O4=0 known-source invariant surface           = false;
direct metric-scalar/mixed RHS trace            = open;
full O4 parent fixed point                      = false;
physical PPN/clock/fifth-force residual         = open;
full MTS fixed point                            = false;
local GR/Newton/Maxwell promotion               = false.
```

## 9. Next target

`4941-Y5-R2FR-direct-metric-scalar-C2p2-trace-and-O4-cancellation-or-shift-gate.md`

Evaluate the explicit right-hand-side metric-scalar and mixed Hessian traces
with two background scalar derivatives and two Weyl tensors in the same
source scheme. Test the exact cancellation value above. If it does not cancel,
insert the calculated shift into the six-coordinate point and rerun the same
finite family; do not create another free O4 parameter and do not project to
local claims before this trace closes.

