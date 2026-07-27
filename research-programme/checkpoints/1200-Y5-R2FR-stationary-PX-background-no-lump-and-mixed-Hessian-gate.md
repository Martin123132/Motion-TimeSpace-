# 5184 - Stationary P(X) background no-lump and mixed-Hessian gate

Marker: `MTS_5184_STATIONARY_PX_BACKGROUND_NO_LUMP_MIXED_HESSIAN_GATE`.

Date: `2026-07-23`.

## Decision

Checkpoint 5184 does the calculation requested at checkpoint 5183 rather than
assuming a nonzero motion profile. The result is a controlled negative for
the **classical stationary-background** route inside the currently certified
local EFT:

```text
THE_HEALTHY_SOURCE_FREE_PARENT_PX_SECTOR_HAS_NO_REGULAR_LOCALIZED_STATIC_MOTION_BACKGROUND_ON_A_HORIZON_FREE_STATIC_GALAXY_SLICE_BECAUSE_THE_SHIFT_CURRENT_IDENTITY_WITH_PX_POSITIVE_AND_ZERO_BOUNDARY_FLUX_FORCES_THE_SPATIAL_GRADIENT_TO_ZERO_ORDINARY_BARYONS_SUPPLY_NEITHER_A_SCALAR_SOURCE_NOR_A_JUNCTION_FLUX_A_HOMOGENEOUS_TIMELIKE_CLOCK_IS_GLOBAL_STATE_DATA_WITH_NONZERO_STRESS_AND_HAS_EXACTLY_ZERO_STATIC_METRIC_SCALAR_MIXING_A_HOMOGENEOUS_SPACELIKE_GRADIENT_IS_NONLOCALIZED_ANISOTROPIC_AND_GENERATES_A_K_ZERO_SCHUR_KERNEL_RATHER_THAN_THE_REQUIRED_K_TIMES_NQ_KERNEL_A_NULL_GRADIENT_CARRIES_NULL_STRESS_AND_THE_PX_ZERO_STEALTH_ESCAPE_REQUIRES_A_DEGENERATE_SCALAR_CONE_OUTSIDE_THE_CERTIFIED_CHART_AFTER_THE_LONGITUDINAL_EIGENVALUE_HAS_ALREADY_CROSSED_ZERO_THEREFORE_THE_CURRENT_CLASSICAL_STATIONARY_BACKGROUND_ROUTE_IS_REJECTED_WITHIN_THE_CERTIFIED_LOCAL_EFT_AND_THE_NEXT_CONSTRUCTIVE_ROUTE_IS_THE_PARENT_OWNED_INTERACTING_OCCUPIED_STATE_CTP_STRESS_BEYOND_THE_ALREADY_COUNTED_CLASSICAL_VLASOV_DENSITY
```

This does not reject the occupied-state programme. It separates two objects
that had been at risk of being mixed:

```text
classical background:       <psi> != 0;
occupied two-point state:   <psi> = 0 but F_X(x,y) != 0.
```

Checkpoint 5151 constructed the second object. The theorem below rejects a
regular source-free localized member of the first object in the healthy
`P_X>0` corridor.

## 1. Scope

Use the parent packet

```text
S_P = integral sqrt(-g) P(X),
X = g^munu nabla_mu psi nabla_nu psi,
P(0)=0,
P_X(0)=1/2.
```

The exact shift current and Hilbert source are

```text
J^mu = 2 P_X nabla^mu psi,
nabla_mu J^mu = 0,

T^mu_nu = 2 P_X v^mu v_nu - delta^mu_nu P.
```

Checkpoint 4943 supplies the essential source clause:

```text
delta S_SM/delta psi = 0,
Q_psi = 0,
```

including ordinary-matter interiors and nonsingular junctions. The theorem is
for a connected, horizon-free static galaxy slice, regular fields, constant
asymptotic scalar data, zero scalar boundary flux and positive spatial
principal operator. It is not advertised as a theorem about an unknown
nonperturbative UV completion.

## 2. Exact static no-lump theorem

Write

```text
ds^2 = -N^2 dt^2 + gamma_ij dx^i dx^j,
N>0,
partial_t psi=0.
```

The current equation becomes

```text
D_i[2 N P_X D^i psi]=0.
```

Multiply by `psi-psi_inf`, integrate over the static slice and integrate by
parts:

```text
integral_Sigma 2 N sqrt(gamma) P_X |D psi|^2

 = boundary_integral 2 N P_X (psi-psi_inf) n^i D_i psi.
```

The parent ordinary-matter theorem makes the interior/junction contribution
zero. Constant asymptotic data or zero scalar flux makes the outer term zero.
If

```text
P_X >= epsilon > 0
```

throughout the profile, the integrand is nonnegative and vanishes only when

```text
D_i psi=0.
```

Thus the requested regular localized static background is exactly constant.
This is not a boundary condition smuggled into the response: it follows from
the parent source theorem, regularity and the healthy principal sign.

The result also holds for a positive definite strict-EFT spatial kinetic
tensor `K_eff^ij`, including the bounded local curvature contacts of
checkpoint 4943. A positive `(Box psi)^2` coordinate strengthens the
integrated identity. An unfixed negative coefficient cannot be iterated
nonperturbatively to manufacture a lump: checkpoint 4983 treats that
coordinate in strict EFT and forbids promotion of its spurious heavy pole.

## 3. Spherical stationary extension

For

```text
ds^2=-N(r)^2 dt^2+A(r)^2 dr^2+r^2 dOmega^2,
psi=q_clock t+phi(r),
```

the radial current integrates once:

```text
Q = 2 N r^2 P_X phi'(r)/A = constant.
```

A regular centre has `Q=0`; checkpoint 4943 also forbids baryons from
supplying a nonzero junction charge. On the healthy branch,

```text
Q=0 and P_X>0  =>  phi'(r)=0.
```

There is a second exact check. A diagonal static metric requires

```text
T_tr=2 P_X q_clock phi'(r)=0.
```

Therefore a stationary radial profile plus a clock does not evade the
theorem. It reduces to a homogeneous timelike clock, a pure radial branch
with forbidden flux, or the degenerate `P_X=0` branch.

## 4. Stress and the stealth escape

For a nonnull constant gradient, the stress has three eigenvalues `-P` and
one eigenvalue

```text
2 X P_X-P.
```

Removing only the anisotropic/rank-one part requires `P_X=0`. Exact zero
stress additionally requires `P=0`. A null gradient at `X=0` is not stealth:

```text
P(0)=0,
P_X(0)=1/2,
T_mn = 2 P_X(0) v_m v_n != 0.
```

The source-locked order-eight trajectory gives:

| scheme | first `lambda_L=0` | first `P_X=0` | certified chart |
|---|---:|---:|---:|
| dynamic `eta_N` | 0.158098249516021 | 0.236527539730595 | `x<=0.1` |
| reference `eta_N=0` | 0.175979291246878 | 0.262824710655261 | `x<=0.1` |

In both schemes the longitudinal principal eigenvalue crosses zero before
`P_X` reaches zero, and both events are outside the certified chart. At
`P_X=0` the transverse scalar kinetic eigenvalue itself vanishes. The
would-be stealth point is therefore neither a healthy derived phase nor a
controlled response pole.

All `242` stored order-eight
trajectory rows remain convex on `x<=0.1`. Recomputing their selected UV
principal minima agrees with the source table to
`1.110e-16`.

## 5. Exact timelike mixed Hessian

Checkpoint 4982 derived

```text
delta_h delta_chi L
 =P_X[tr(h)(v.w)-2v.h.w]
  -2P_XX(v.h.v)(v.w).
```

Use signature `(-,+,+,+)` and Newtonian gauge

```text
h_00=-2 Phi,
h_ij=-2 Psi delta_ij.
```

For `v_mu=(q_clock,0,0,0)` and fluctuation frequency `omega`,

```text
B_(Phi,Psi)
 =2 q_clock omega
   [P_X-2 q_clock^2 P_XX, 3 P_X],

K_chichi
 =2 P_X k^2
  -2(P_X-2 q_clock^2 P_XX) omega^2.
```

Consequently

```text
omega=0  =>  B_(Phi,Psi)=(0,0).
```

The finite-frequency Schur correction vanishes as `omega^2/k^2` in the
quasistatic limit. A homogeneous clock can affect cosmological/time-dependent
response, but it cannot supply the missing static galaxy kernel. Its
amplitude is also a global current/initial-state datum, not a baryon-selected
local profile.

## 6. Exact spacelike mixed Hessian

For a constant spacelike gradient `v_mu=(0,0,0,V)`, set

```text
X=V^2,
k_parallel=k cos(theta),
U=[P_X,-P_X+2 X P_XX].
```

The exact static blocks are

```text
B_(Phi,Psi)=2 V k_parallel U,

K_chichi
 =2 k^2[P_X+2 X P_XX cos(theta)^2].
```

Integrating the scalar fluctuation gives

```text
B K_chichi^-1 B^T

 =2 X cos(theta)^2 U U^T
  /[P_X+2 X P_XX cos(theta)^2].
```

This result is:

1. anisotropic;
2. homogeneous of degree zero in `k`;
3. singular only when the directional scalar principal cone degenerates;
4. carried by a nonlocalized, stressed background whose amplitude and
   direction are not selected by the parent source.

An independent `40000`-sample numerical
contraction gives maximum mixed and Schur residuals
`1.235e-15` and
`2.776e-16`.

## 7. Scaling against the required response

Checkpoint 5183 restated the required kernel scaling as

```text
d_required(k) proportional k n_q(k/mu),
n_q(x)=1/(1+x^q),
q=0.77.
```

The constant-gradient Schur kernel is `k^0`. Relative to the Einstein
constraint kernel `a proportional k^2`, the two alternatives are

```text
required relative response:            n_q(x)/x,
constant-gradient relative response:   1/x^2.
```

The executed low/high slopes are:

| object | low slope | high slope |
|---|---:|---:|
| required kernel | 0.999944863714249 | 0.230055136285751 |
| constant-gradient kernel | 0 | 0 |
| required relative response | -1.00005513628575 | -1.76994486371425 |
| constant-gradient relative response | -2 | -2 |

No constant normalization repairs both asymptotic slopes. Allowing the
background to vary spatially would abandon the constant-gradient Hessian, but
the no-lump theorem has already excluded a regular localized source-free
profile in the healthy corridor.

## 8. What survives and what comes next

```text
regular localized classical P(X) galaxy background = rejected in certified corridor;
timelike clock as static galaxy response            = exact zero;
spacelike/null constant gradient                     = nonlocalized/stressed/anisotropic;
P_X=0 stealth escape                                 = unhealthy and uncertified;
zero-gradient local GR/Newton/Maxwell branch         = retained;
checkpoint-5151 occupied-state stress                = distinct and retained;
full local-GR or galaxy claim                        = false.
```

The next calculation must not try another arbitrary classical profile.
Checkpoint 5185 should derive the first parent-owned **interacting**
occupied-state stress from the existing essential `X^2/X^3` vertices in the
CTP/2PI hierarchy. It must:

1. satisfy the metric Ward identity;
2. remove the classical Vlasov density already counted at checkpoint 5171;
3. test whether the remaining static kernel is compensated,
   scale-dependent and local-vacuum silent;
4. derive its state normalization or reject the route.

That is a constructive forward calculation, not another missing-input list.

## 9. Audit

All `35` validations pass. Every evidence row
remains `valid_for_claim=false`. The protected `formalization-workbench`
digest remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758` and the
checkpoint-5176 ensemble remains
`254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b`. No GitHub action occurred.

Generated files:

- `source-intake/functional_rg/5184/stationary_background_classification.csv`
- `source-intake/functional_rg/5184/static_no_lump_and_flux_theorem.csv`
- `source-intake/functional_rg/5184/timelike_spacelike_mixed_Hessian.csv`
- `source-intake/functional_rg/5184/stealth_root_and_principal_cone_gate.csv`
- `source-intake/functional_rg/5184/stationary_background_scaling_comparison.csv`
- `source-intake/functional_rg/5184/stationary_background_route_decision.csv`
- `source-intake/functional_rg/5184/source_provenance.csv`
- `source-intake/functional_rg/5184/stationary_PX_background_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5184_VALIDATION.csv`
