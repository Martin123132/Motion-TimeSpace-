# 4955 - Gravity-generated `X3`, functional-hierarchy gate and fixed-ratio decision

Date: 2026-07-13

Marker: `MTS_X3_PARENT_FLOW_HIERARCHY_DECISION_4955`.

Status: private analytic, source-locked, symbolically reproducible and
data-executed checkpoint. This checkpoint does not pretend that a finite
`X2-X3` truncation is the complete motion theory. It derives the missing
minimal-gravity `X3` source, calibrates it against the published `X2` source,
and then proves exactly why the resulting finite polynomial flow is not
closed. The 4947 local GR/Newton/Maxwell branch remains unchanged.

## 1. Source-complete derivative basis

The Hilbert-series source gives the complete CP-even, shift-symmetric
six-derivative scalar-gravity basis

```text
O1=[(nabla phi)^2]^3,
O2=(nabla phi)^2(nabla nabla phi)^2,
O3=C^3,
O4=C^2(nabla phi)^2,
O5=C(nabla phi)^2(nabla nabla phi).
```

`O1=X_source^3` is the unique constant-gradient six-field coordinate entering
the 4954 contact amplitude. The same source states that the eight-derivative
basis contains the independent `dphi^8=X_source^4` structure. Therefore a
flow projection for `O1` may be exact at a declared basepoint without making
the whole five-operator block, or its higher-derivative completion, closed.

The conventions used below are

```text
X_source=(nabla phi)^2,
P(X_source)=X_source/2+c X_source^2+e X_source^3+f X_source^4+...,
X_recent=X_source/2,
u_X2=4c,
v_X3=8e,
r3=v_X3/u_X2^2=e/(2c^2).
```

## 2. Exact minimal-gravity `X3` source

Start from the source's scalar kinetic Hessian on a flat, constant-gradient
background in harmonic gauge. In the orthonormal ten-component symmetric
tensor basis, let

```text
K_AB=delta_AB-(1/2)t_A t_B
```

be the four-dimensional inverse DeWitt metric. Let `B` be the mixed
metric-scalar kinetic vertex and `V_X` the two-graviton kinetic vertex. Direct
symbolic contraction gives

```text
Tr(K V_X)=0,
B^T K B=1/2.
```

For radial loop coordinate `q`, angular coordinate `z`, and
`s^2=32 pi g`, expand the regulated inverse Hessian with a term linear in the
background gradient, `M1`, and a term quadratic in it, `M2`. The required
inverse-series coefficients are

```text
C4=Tr(M2^2)-3Tr(M1^2 M2)+Tr(M1^4),

C6=-Tr(M2^3)+4Tr(M1^2 M2^2)+2Tr(M1 M2 M1 M2)
   -5Tr(M1^4 M2)+Tr(M1^6).
```

The exact `S3` angular averages are

```text
<C4>=(8q^4-9q^2+12)/16,
<C6>=(8q^6-15q^4+9q^2-3)/32.
```

The Litim-ball radial integrals and four-dimensional momentum measure give

```text
int_0^1 dq q^3 <C4> = 5/32,
int_0^1 dq q^3 <C6> = -13/1280,

flow_X2 = [5/(256 pi^2)]s^4 X_source^2,
flow_X3 = [-13/(10240 pi^2)]s^6 X_source^3.
```

Consequently, at `lambda=eta_N=eta_s=0` and at vanishing matter couplings,

```text
beta_c|0 = 20 g^2,
beta_e|0 = -(208 pi/5)g^3.
```

The first coefficient exactly reproduces the published scalar-gravity result.
It is an internal normalization calibration of the new second coefficient,
not merely a dimensional estimate. The conclusion is strict within this
flat natural-Litim basepoint:

```text
g != 0  =>  beta_e(e=0) != 0.
```

Thus the `X3` zero surface is not invariant. Natural Type I and the 4941
curvature-endomorphism Type II agree for this flat additive projection because
the curvature endomorphism vanishes here. This does not establish a
regulator-independent curved-space coefficient.

## 3. Exact finite-polynomial nonclosure theorem

The flat scalar sector can be tested without guessing the next coefficient.
For `x=X_source/k^4`, the constant-gradient Type-I/Litim flow at `eta_s=0` is

```text
partial_t p(x)=-4p+4x p'
 +1/(8pi^2) int_0^1 dq q^3
  <[1+q^2(2p'-1+4x p'' mu^2)]^-1>_S3.
```

Expanding this functional equation gives

```text
beta_c =4c+5c^2/(8pi^2)-e/(4pi^2),

beta_e =8e-37c^3/(10pi^2)+21ce/(8pi^2)-5f/(12pi^2),

beta_f =12f+25c^4/pi^2-243c^2e/(10pi^2)
             +9cf/(2pi^2)+45e^2/(16pi^2)-5h5/(8pi^2).
```

More generally, if `a_n x^n` is retained, the linear feed from the next
coordinate is

```text
partial beta_(a_n)/partial a_(n+1)
 =-(n+1)(n+2)/(48pi^2),   n>=2.
```

This is nonzero at every finite order. Therefore neither `X2`, `X2-X3`, nor
`X2-X3-X4` is an autonomous parent truncation. Setting the next coefficient
to zero is a closure assumption, not a derivation. The legitimate routes are
a functional `P_k(X)` solution or a demonstrated convergence/error bound for
successive truncations.

The theorem is useful forward movement: it prevents the project from spending
another sequence of checkpoints adding one coefficient at a time while
mistaking a finite polynomial for the parent theory.

## 4. Leading GR-forced trajectory

For orientation only, retain the Gaussian/GR pieces already derived in the
lower essential quotient:

```text
beta_g=2g,
beta_c,ess=4c_ess+16g^2,
beta_e=8e-(208pi/5)g^3.
```

Their exact leading solutions are

```text
g(k)=g0(k/k0)^2,
c_ess(k)=g(k)^2[C_c+16ln(k/k0)],
e(k)=(104pi/5)g(k)^3+C_e g(k)^4.
```

The recent-convention forced coordinate is therefore

```text
v_X3,forced=(832pi/5)g^3.
```

Canonical scaling cancels from the leading ratio flow, leaving

```text
beta_r3=-(104pi/5)g^3/c_ess^2-32r3 g^2/c_ess.
```

For the particular forced solution `C_c=C_e=0`,

```text
r3(k)=13pi/[320 g(k) ln(k/k0)^2].
```

So gravity forces a nonzero absolute `X3` coordinate, but this minimal system
does not generate a finite scale-independent `r3`. The omitted `X4` feed,
the other six-derivative operators, anomalous dimensions, cosmological
constant and the six-derivative essential quotient enter before this can be
called the complete GR-connected motion trajectory.

## 5. SPARC orientation gate

The minimal forced coordinate was evaluated on all 1050 inherited 4954 rows
using

```text
g_E=G_N E^2=(E/M_Pl)^2,
v_X3=(832pi/5)g_E^3,
B_X3=|v_X3|(rho_psi/E^4)^2,
(sigma_24 E^2)_contact=C2 v_X3^2.
```

Rescaling the deliberately generous 4954 unit-six-point envelope by
`v_X3^2` is an orientation comparator, not a complete occupied-state rate.
The execution gives

```text
rows                                             = 1050,
positive high-frequency rows                     = 692,
maximum |v_X3,forced|                             = 1.57849678213e-46,
maximum background coordinate                    = 3.66353471510e-123,
maximum contact sigma_24 E^2                      = 1.35654226663e-98,
maximum forced contact log-gain on high rows      = 9.64077770446e-127,
minimum required high-row log-gain                = 14.9116937188,
minimal forced comparator failures                = 692/692.
```

The leading Gaussian/GR forced contact is therefore far too small to rescue
the controlled high-frequency production route. Because the functional
parent flow is not closed, this is not a rejection of every possible MTS
trajectory, direct profile-frequency formation amplitude, or genuinely broad
nonequilibrium state.

## 6. Decision

```text
complete CP-even six-derivative basis            = source signed;
minimal-gravity X3 additive source               = derived exactly;
published X2 source normalization                = reproduced exactly;
X3=0 invariant surface                           = rejected;
finite X2-X3 polynomial flow                     = rejected as nonclosed;
general finite P(X) polynomial closure           = rejected exactly;
minimal GR-forced absolute X3 trajectory          = derived;
finite parent-fixed r3                            = not derived;
minimal forced SPARC contact comparator           = rejected on 692/692;
full unequal-time 2PI solve                       = deferred pending parent flow;
direct profile-frequency formation amplitude      = open;
4947 local GR/Newton/Maxwell branch                = retained;
full MTS unification                              = false.
```

## 7. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4955_X3_parent_flow_and_hierarchy.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4955_X3_parent_flow_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4955/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4955/X3_parent_flow_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4955/minimal_gravity_X2_X3_source_projection.csv`
- `post-checkpoint-work/source-intake/functional_rg/4955/PX_coefficient_hierarchy.csv`
- `post-checkpoint-work/source-intake/functional_rg/4955/six_derivative_operator_flow_roles.csv`
- `post-checkpoint-work/source-intake/functional_rg/4955/GR_gaussian_X3_forced_trajectory.csv`
- `post-checkpoint-work/source-intake/functional_rg/4955/SPARC_parent_forced_X3_coordinate_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4955/X3_parent_flow_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4955_VALIDATION.csv`

## Next target

`4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md`

Construct the full constant-gradient gravity-motion Hessian for a running
function `P_k(X)`, derive its fixed-function equation, and solve it with
regularity, convexity and convergence gates. Compare polynomial projections
through increasing order rather than setting the next coefficient to zero.
Only a stable functional trajectory may supply `r3` to the 4954 amplitude or
warrant a full unequal-time 2PI calculation. Keep `O2`, `O4`, `O5` and curved
projection residuals explicit rather than claiming that flat `P(X)` completes
the whole motion sector.
