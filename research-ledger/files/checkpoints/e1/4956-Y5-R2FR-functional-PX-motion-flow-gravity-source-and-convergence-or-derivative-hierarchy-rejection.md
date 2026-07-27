# 4956 - Functional `P(X)` gravity-motion flow and fixed-germ gate

Date: 2026-07-13

Marker: `MTS_FUNCTIONAL_PX_FIXED_FUNCTION_DECISION_4956`.

Status: private analytic, source-locked and numerically executed checkpoint.
This checkpoint replaces the nonclosed finite-polynomial parent used only as
a diagnostic at 4955 by one functional `P_k(X)` projector. It establishes a
Gaussian-connected, locally regular fixed-function germ in the declared
minimal flat gravity-motion sector. It does not establish a global fixed
function, the infrared motion trajectory, the full curved derivative sector,
or full MTS unification. The 4947 local GR/Newton/Maxwell branch is retained.

## 1. Functional coordinate and operator firewall

Use the dimensionless variables

```text
x=Z_psi X/k^4,
p_k(x)=k^-4 P_k(X),
p_k(0)=0,
p_k'(0)=1/2.
```

The calculation keeps the complete constant-gradient `P(X)` tower. It is
therefore not the coefficient-by-coefficient closure rejected at 4955. Its
declared firewall is nevertheless strict:

```text
included:  flat constant-gradient P(X), metric-motion mixing, eta_psi;
excluded:  O2, O4, O5, curved-background projectors, nonconstant gradients;
parent g*: inherited from the source-locked 4935 minimal GR branch;
schemes:   eta_N=0 reference and eta_N=-2 fixed-point insertion.
```

The inherited value

```text
g*=0.1305603732179711
```

is a controlled comparator from the completed minimal gravity-photon
trajectory, not a declaration that the full MTS fixed point has already been
found.

## 2. Exact functional gravity-motion Hessian

Let `E_A` be the orthonormal ten-component basis of symmetric tensors,
`t_A=tr(E_A)`, and

```text
K_AB=delta_AB-(1/2)t_A t_B
```

be the inverse DeWitt metric. Let the background motion gradient define the
unit vector `e_mu`, `d_A=e.E_A.e`, radial loop coordinate `q` and angular
coordinate `z=e.qhat`. The second variation of `sqrt(g)P(X)` gives the exact
minimal flat blocks

```text
H_hh=I_10+32pi g K[p M0+x p' M1+x^2 p'' M2],

H_hpsi=sqrt(32pi g) q K sqrt(x)[p' B1+x p'' B2],

H_psipsi=1+q^2[2p'-1+4x p'' z^2].
```

Here

```text
M0=(1/4)tt^T-(1/2)I_10,
M1=2A_e-(1/2)(td^T+dt^T),
M2=dd^T,
B1=t z-2(e.E_A.qhat),
B2=-2d z.
```

The spectrally normalized Litim insertion is

```text
W_A=1-(eta_A/2)(1-q^2),  A in {N,psi}.
```

After subtracting the field-independent `x=0` trace, the functional equation
is

```text
partial_t p=-4p+(4+eta_psi)x p'
 +(1/8pi^2)int_0^1 dq q^3
  <Tr[H^-1 W]-Tr[W]_(x=0)>_S3.
```

The normalization condition `beta_[p'(0)]=0` fixes

```text
eta_psi=-Q1_fixed/[1/2+Q1_eta].
```

No finite next coefficient is set to zero in deriving this functional
projector. Polynomial orders are used only as a convergence sequence for its
local Taylor germ.

## 3. Independent calibration targets

The functional inverse-series implementation reproduces both independent
4955 target structures:

```text
pure scalar Q2 and Q3 hierarchy error       <=1.09e-15,
gravity Q2/g^2                              =20,
gravity Q3/g^3                              =-208pi/5,
maximum calibration relative error         =3.05e-15.
```

The gravity calibration holds at `g=10^-5,10^-3,10^-2,g*`. This is a strong
normalization check because the `X2` source was published independently and
the `X3` source was derived at 4955 before the functional code existed.

## 4. Gaussian-connected fixed-germ sequence

The calculation first continues the `N=2` Gaussian matter root from `g=0` to
`g*`, then raises the polynomial projection from `N=2` through `N=12`, and
finally continues the complete `N=12` solution back to `g=0`. Every step
passes in both regulator insertions, and both endpoint coefficient norms are
exactly zero at numerical precision.

At `N=12` the two declared schemes give

```text
                         eta_N=0              eta_N=-2
eta_psi                 -0.05790340816       -0.06569466058
a2                      -0.08980815464       -0.12252807013
a3                       0.07018018017        0.11542500444
r3=a3/(2a2^2)            4.35063788925        3.84413576778
C_24(r3)                 3.2118768144e-6      2.0131123408e-6
```

Across orders `N=8,...,12`, the largest relative spread of any of
`a2,a3,eta_psi,r3` is `7.99e-9`. The low functional coordinates therefore
converge much faster than the declared `10^-4` gate. The UV fixed-germ ratio
is legitimately scheme bracketed as

```text
3.84413576778 <= r3_UV,germ <= 4.35063788925.
```

This is not yet the infrared `r3` entering a galaxy-formation or local rate.
That number requires integrating the functional coefficients down the
source-locked GR trajectory.

## 5. Local regularity, global warning

The high Taylor coefficients alternate and grow. At `N=12`, for example,

```text
a12=-3.15854e6  for eta_N=0,
a12=-9.29872e6  for eta_N=-2.
```

This is not hidden as numerical noise. It limits the domain in which the
Taylor representation is supported. Direct scalar-convexity and full
11-by-11 Hessian singular-value scans give

```text
0<=x<=0.1:
  both schemes convex;
  min singular value >=0.3370;
  local fixed-function germ retained.

0<=x<=0.25:
  both N=12 schemes lose scalar convexity;
  first longitudinal zeros =0.14757 and 0.13343;
  global regular fixed function not established.
```

The correct conclusion is therefore local and useful: a stable analytic germ
exists around the GR/Gaussian-connected background, but its global
continuation cannot be inferred from this polynomial chart.

## 6. Physics decision

Checkpoint 4955 showed that gravity inevitably generates `X3` and that a
finite polynomial parent is nonclosed. Checkpoint 4956 now makes the required
leap: the full local `P(X)` tower has a calibrated, Gaussian-connected and
convergent low-coordinate fixed germ. This converts `r3` from an arbitrary
closure parameter into a derived UV scheme bracket within the declared
sector.

It does not yet connect that bracket to infrared observations. The decisive
next calculation is an RG trajectory, not another fixed-point audit:

```text
minimal flat functional P(X) Hessian          = derived;
4955 X2 and X3 sources                        = reproduced;
Gaussian-connected roots N=2..12             = retained;
low-coordinate convergence                   = passed;
local regular germ on x<=0.1                  = retained;
global regular fixed function on x<=0.25      = not established;
UV r3 fixed-germ bracket                      = derived;
infrared r3 trajectory                        = open;
O2/O4/O5 and curved residual projectors       = open;
4947 local GR/Newton/Maxwell branch            = retained;
full MTS unification                          = false.
```

## 7. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4956_functional_PX_fixed_function_gate.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4956_functional_PX_fixed_function_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4956/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_PX_fixed_function_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_PX_Hessian_contract.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_PX_calibration.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/polynomial_GR_homotopy_trace.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/polynomial_fixed_point_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_coefficient_convergence.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_regular_convexity_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4956/functional_PX_route_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4956_VALIDATION.csv`

## Next target

`4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md`

Integrate the converged low functional coordinates down the source-locked
4935 GR-connected trajectory, propagate both regulator insertions as a scheme
band, and require the flow to remain inside the `x<=0.1` regular domain.
Derive or bound the omitted `O2`, `O4`, `O5` and curved-projector residuals.
Only the resulting infrared `r3` may be inserted into the 4954 six-point
kernel or used to decide whether a full unequal-time 2PI solve is warranted.

