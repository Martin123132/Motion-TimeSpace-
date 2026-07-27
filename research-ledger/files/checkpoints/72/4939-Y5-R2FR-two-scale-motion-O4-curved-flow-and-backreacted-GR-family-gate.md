# 4939 - Two-scale motion O4 and backreacted GR-family gate

Marker: `MTS_TWO_SCALE_O4_KNOWN_SOURCE_BACKREACTED_GR_FAMILY_GATE_4939`.

Date: `2026-07-12`.

Status: private analytic and source-executed checkpoint. The massless motion
scalar is now inserted into the completed essential beta system before the
fixed point is solved, and the finite mass threshold is backreacted throughout
the GR-connected family. The scalar and photon pieces of the O4 source are
closed exactly; the off-shell gravity-motion mixed O4 source remains open.
Consequently the finite family is a real known-source calculation, but not yet
the full O4-completed MTS trajectory or a local-GR claim.

## 1. Correction to the spectator approximation

Checkpoint 4938 differentiated

```text
Delta beta_g=g^2/[6pi(1+w_psi)]
```

about the 4934 fixed point, but retained the 4934 point as the background.
That was sufficient for a first transfer derivative, not for the enlarged
fixed point, because at `w_psi=0` the scalar source itself is nonzero.

The present checkpoint solves

```text
beta_x^4939(x,w)
 =beta_x^4934(x)
  +(g^2/[6pi(1+w)],0,0,0,0),

x=(g,g_plus,g_minus,g_CFF,h_C3).
```

The neutral scalar has no direct one-loop source for the photon coordinates,
and its optimized `eta_psi=0` minimal `a_6` row is zero.
Its indirect effects on the photon and C3 coordinates occur through the
shifted gravity trajectory and are retained.

## 2. Heat-kernel and threshold derivation

For the optimized scalar kernel,

```text
Q_2/k^4=1/[2(1+w)],

Q_1/k^2=1/(1+w),

Q_0=1/(1+w),

Q_-1=0.
```

The minimal scalar coefficient

```text
a_4=(5R^2-2R_mn^2+2R_mnrs^2)/360

   =R^2/80+S_mn^2/60+Euler/180
```

reproduces the essential Newton source above. The inessential curved rows
cannot be inserted alone into the natural essential source system: they must
be accompanied by the matching field-redefinition basis. Directly inserting
only those raw rows produces a scheme-inconsistent result. The source-owned
essential beta is therefore used rather than an incomplete raw-row splice.

## 3. Backreacted ultraviolet point

The massless scalar shifts the completed point to

```text
(g,g_plus,g_minus,g_CFF,h_C3)
 =(0.130890578648081,
   0.371493332004294,
   3.45050247019694,
   0.00409512566078930,
   3.91621590325141e-6).
```

The beta residual is

```text
||beta||_infinity=4.68138673588e-14.
```

Relative to 4934, the coordinate shifts are approximately

```text
{+0.253%,+7.057%,+6.351%,+9.789%,-0.788%}.
```

Thus the scalar baseline is not numerically negligible in the ultraviolet
photon/Wilson coordinates and should not have remained a spectator.

The five-coordinate gravity/photon/C3 spectrum is

```text
lambda={
 -1.89247649906140,
  0.212971533014970,
  0.228010326907034,
  0.280887036593853,
  1.08876224382846
}.
```

It retains exactly one relevant direction. The former complex pair becomes
real, while the smallest positive stability margin remains `0.21297`.

## 4. Enlarged motion stability

The exact mass column at the shifted point is

```text
partial_w beta_x|_0
 =(-g_*^2/(6pi),0,0,0,0)
 =(-0.000908899055773,0,0,0,0).
```

For the two source/action-sign maps,

```text
v=+2lambda:
  A_*=0.150321281767,
  theta_mass=1.84967871823,
  theta_mass/theta_g=0.977385303939;

v=-2lambda:
  A_*=0.141529201049,
  theta_mass=1.85847079895,
  theta_mass/theta_g=0.982031111019.
```

Both six-coordinate systems have exactly two relevant directions. The
mass-eigenvector gravity-response solves have infinity residuals below
`1.46e-16`. Including the scalar baseline therefore changes the
fixed point and transfer coefficients but not the two-scale parameter count.

## 5. Finite backreacted GR family

The finite system

```text
partial_t x
 =beta_x^4934(x)
  +(g^2/[6pi(1+w)],0,0,0,0),

partial_t ln w=-2+A(g,v_sign)
```

was integrated from the shifted point using three gravity amplitudes,

```text
epsilon={1e-5,3e-6,1e-6},
```

both sign maps and

```text
R_UV={1e-12,1e-10,1e-8,1e-6,1e-4,1e-2,1}.
```

The initial gravity coordinates include the calculated mass-eigenvector
rotation rather than adding `w` on top of an unchanged gravity
seed. All 42 positive-mass runs and three massless comparison runs reach
`g=1e-10`.

At small `R_UV`,

```text
J_gap,IR/R_UV
 about 0.26259  for v=+2lambda,

J_gap,IR/R_UV
 about 0.26220  for v=-2lambda.
```

At `R_UV=1` the finite threshold feedback makes the map nonlinear,

```text
J_gap,IR=0.200597389473  for v=+2lambda,

J_gap,IR=0.188519777494  for v=-2lambda.
```

The maximum three-seed drift of `J_gap,IR` over the executed grid is
below `7.05e-6`. This is the first finite, backreacted two-scale
family rather than an infinitesimal spectator transfer.

## 6. Wilson-coordinate response

The massless scalar branch ends at

```text
W_plus=0.00842756254464,

W_minus=0.0988519754609,

W_C=0.000603273211879,

A_C3=-2.19279241490e-5.
```

Across the finite grid the largest absolute shifts from the massless branch
are

```text
|Delta W_plus| <=6.67641e-5,

|Delta W_minus|<=6.34396e-4,

|Delta W_C|    <=3.07626e-6,

|Delta A_C3|   <=7.63362e-8.
```

These are trajectory Wilson responses. They are not direct laboratory
Maxwell residuals.

## 7. O4 source theorem

For

```text
S_O4=u_O4 integral sqrt(g) C^2(nabla psi)^2,
```

the exact projector and Hessian are

```text
P_O4
 =(1/2)partial_(C^2)partial_(p^2)Gamma_psi_psi^(2)|0,

Delta Gamma_psi_psi^(2)
 =-2u_O4 nabla_mu[C^2 nabla^mu].
```

With `utilde_O4=k^4u_O4/Z_psi`, the known beta structure is

```text
beta_utilde_O4
 =(4+eta_psi)utilde_O4
  +S_O4^(gravity-mixed).
```

Three source statements are exact in the current regular mass branch:

1. the isolated quadratic scalar trace is background-scalar independent, so
   its two-scalar O4 source is zero;
2. the neutral photon trace contains no background motion scalar, so its
   direct O4 source is zero;
3. at `eta_psi=0`, `Q_-1=0`, so the minimal scalar C3
   row is zero.

The remaining term is the off-shell curved gravity-motion and mixed Hessian
trace at `C^2p^2`. It is not fixed by the flat functional-potential
calculation. Therefore

```text
u_O4=0 known-source trajectory        = calculated diagnostic;

u_O4=0 full-parent invariant surface  = not proved.
```

This is a sharper result than either freezing O4 or declaring the whole
source unknown: the scalar and photon routes are closed, leaving one explicit
gravity-mixed trace.

## 8. Local threshold residual

At every executed endpoint the derived Newton-flow residual is

```text
Delta beta_g/g
 =g/[6pi(1+w)]
 =g^2/[6pi(g+J_gap)].
```

At `g=1e-10` it is at most about `5.31e-12` and becomes
far smaller once the scalar decouples. The direct neutral-scalar photon beta
rows and minimal `eta_psi=0` C3 row are zero.

This is an RG-threshold residual, not a PPN `beta/gamma` score and
not a clock, fifth-force or Coulomb observable. Those require the local
source projection and the remaining O4 gravity-mixed coefficient.

## 9. Claim boundary

```text
massless scalar fixed-point backreaction       = calculated;
finite mass-threshold GR family                = calculated;
three-seed finite-family convergence           = passed;
neutral scalar direct Maxwell beta source      = exact zero;
minimal eta_psi=0 scalar C3 source              = exact zero;
scalar and photon O4 sources                    = exact zero;
gravity-mixed O4 source                         = open;
u_O4=0 full-parent invariant surface            = false;
physical PPN/clock/fifth-force residual         = open;
full MTS fixed point                            = false;
local GR/Newton/Maxwell promotion               = false.
```

## 10. Next target

`4940-Y5-R2FR-curved-gravity-motion-O4-additive-source-and-full-invariant-submanifold-gate.md`

Compute the remaining off-shell metric-scalar/mixed trace with two background
motion legs and two Weyl tensors. Either derive
`S_O4^(gravity-mixed)` and include `utilde_O4` in the
fixed point and finite family, or prove that it vanishes in the declared
source scheme. Do not use the known-source `u_O4=0` family as the
full parent before that gate closes.

