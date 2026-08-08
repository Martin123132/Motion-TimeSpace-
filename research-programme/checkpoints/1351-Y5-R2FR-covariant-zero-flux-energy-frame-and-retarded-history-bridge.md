# 5335 - Covariant zero-flux energy frame and retarded-history bridge

Date: `2026-08-06`

Marker: `MTS_5335_COVARIANT_ENERGY_FRAME_RETARDED_FOLD_BRIDGE`.

## Executive result

The extra maths is useful, but not in the naive form

```text
Poynting flow = a new fundamental MTS motion field.
```

That identification is rejected. Checkpoints 4175, 4207, 5187 and 5211
already derive the Poynting vector as the `0i` component of the Maxwell
Hilbert stress. Adding it again would double-count the same source.

The useful result is a three-object separation:

```text
w_obs^mu = q^mu[n]/epsilon[n]
    observer-dependent energy-transport velocity;

U_L^mu:
T^mu_nu U_L^nu = -rho_L U_L^mu
    derived zero-flux/Landau energy frame when a timelike eigenvector exists;

J_ret = |1-rhat.v/u|
    retarded history-map Jacobian of a specified causal wave operator.
```

They are not the same field.

Two genuine MTS bridges survive:

1. for `X<0`, the existing scalar clock
   `U_chi,mu=-nabla_mu chi/sqrt(-X)` is exactly the Landau frame of its own
   classical `P(X,chi)` stress;
2. a reflection-even occupied state with `<chi>=0` can have a nonzero
   variational stress `T_occ`. Where that stress is type I, its timelike
   eigenvector defines a covariant state flow without adding a new parent
   vector or breaking the exact local `chi=0` GR branch.

The retarded-history work supplies a sharper conditional result. Its fold
density is proportional to `Delta^(-1/2)`. If the parent occupied-state
common-scalar projection is critical at zero momentum and isotropy gives

```text
Delta(k)=d2 (|k|/mu)^2+O(k^4),    d2>0,
```

then

```text
Delta(k)^(-1/2)
 =mu/[sqrt(d2)|k|]+O(|k|/mu).
```

This is exactly the missing deep-infrared exponent
`C_q~mu/|k|` isolated in checkpoint 5189. It does not yet derive the
critical state, coefficient, crossover exponent `q=0.77`, Ward identity or
galaxy amplitude. It converts the old open target into a concrete
critical-fold theorem that can now be proved or rejected from the parent CTP
kernel.

## 1. Covariant stress decomposition

Use signature `(-,+,+,+)`, set `c=1`, and let `n^mu n_mu=-1`. Define

```text
h^mu_nu = delta^mu_nu+n^mu n_nu,

epsilon[n] = T_mn n^m n^n,

q^mu[n] = -h^mu_a T^ab n_b.
```

The projector identity gives

```text
n_mu q^mu=0.
```

The future energy current is

```text
J^mu=-T^mu_nu n^nu=epsilon n^mu+q^mu.
```

Under the dominant energy condition it is causal:

```text
J_mu J^mu=-epsilon^2+q_mu q^mu<=0,

q_mu q^mu<=epsilon^2.
```

Therefore `w_obs^mu=q^mu/epsilon` is subluminal when defined. It still
depends on `n`; it is a decomposition of a tensor relative to an observer,
not an observer-independent parent field.

## 2. The zero-flux energy frame is a different object

If `T^mu_nu` has a future timelike eigenvector,

```text
T^mu_nu U_L^nu=-rho_L U_L^mu,
U_L^mu U_L,mu=-1,
```

then projection orthogonal to `U_L` gives

```text
q^mu[U_L]=0.
```

For two opposing null streams with lab energy weights `a,b>0`,

```text
epsilon_lab=a+b,
q_lab^x=a-b,

w_obs^x=(a-b)/(a+b),

beta_L=(sqrt(a)-sqrt(b))/(sqrt(a)+sqrt(b)),
rho_L=2 sqrt(a b).
```

The executed `a=4,b=1` case gives

```text
w_obs^x=0.6,
beta_L=1/3,
rho_L=4,
|q[U_L]|=0.
```

Thus the source formula `S/u` is a valid observer-frame energy-transport
velocity, but it is not generally the boost velocity of the zero-flux frame.
For `a=b`, both vanish while `rho_L=2a>0`. This proves that zero net flow
does not mean zero energy. For `b->0`, `beta_L->1`; a single nonzero null
stream has no timelike rest frame.

## 3. Exact Maxwell null/non-null discriminator

For Maxwell fields in a local orthonormal frame,

```text
u_EM=(E^2+B^2)/2,
S=E cross B.
```

Direct algebra gives

```text
u_EM^2-|S|^2
 =[(E^2-B^2)^2]/4+(E.B)^2
 =I^2/16+J^2/16
```

up to the declared invariant signs

```text
I=2(B^2-E^2),
J=-4 E.B.
```

Consequently:

```text
nonzero null field: I=J=0, |S|=u_EM
    -> no timelike zero-Poynting frame;

non-null field: I or J nonzero, |S|<u_EM
    -> a local timelike zero-Poynting frame exists;

vacuum: T_EM=0
    -> every observer is an eigenvector, but S/u is undefined.
```

The five executed field cases close this identity with maximum numerical
residual `2.776e-16`. This null and vacuum degeneracy rules out using a
Landau frame as a globally fundamental replacement for the metric, coframe or
MTS scalar.

## 4. Exact map to the existing MTS scalar

Checkpoint 5189 has

```text
T_chi^mu_nu
 =2 P_X nabla^mu chi nabla_nu chi-delta^mu_nu P.
```

For `X<0`, set

```text
U_chi,mu=-nabla_mu chi/sqrt(-X).
```

Then

```text
T_chi^mu_nu U_chi^nu
 =(2P_X X-P)U_chi^mu
 =-rho_chi U_chi^mu,

rho_chi=P-2P_X X.
```

Therefore the classical motion clock is already the zero-flux frame of its
own stress. Because `U_chi` is proportional to an exact one-form,

```text
U_chi wedge dU_chi=0.
```

It is hypersurface-orthogonal. A generic total-matter energy frame can be
vortical, so the global equation

```text
U_chi=U_L[T_total]
```

cannot be imposed without adding a new matter-locking equation absent from
the parent action.

On the checkpoint-5211 selected local branch,

```text
chi=0,
nabla chi=0,
T_chi=0.
```

`U_chi` is then unnecessary and undefined, while the exact two-derivative
GR+Maxwell truncation remains valid. The energy-frame construction neither
repairs nor damages that branch.

## 5. Reflection-even occupied-state survivor

Checkpoint 4948 keeps

```text
<chi>=0,
Delta G_state=G_state-G_vac,

T_occ,mn
 =-2/sqrt(-g)
   delta[Gamma_2PI-S_g]/delta g^mn
   at stationary G.
```

This allows a nonzero, conserved, reflection-even state stress without a
classical scalar charge. If `T_occ` is type I, define

```text
T_occ^mu_nu U_occ^nu=-rho_occ U_occ^mu.
```

`U_occ` is then a derived description of the state, not an independent field
and not a second source. The primary object remains `T_occ` or its CTP
spectral kernel. In null/type-II patches the eigenframe can fail while the
stress remains well defined, so all dynamics must be written in terms of the
stress/kernel rather than `U_occ` alone.

This is the clean place where the zero-net-flow intuition helps MTS: it gives
a covariant occupied-state flow diagnostic compatible with `<chi>=0` and the
existing fifth-force zero.

## 6. Exact retarded-history Jacobian

For the flat source-owned model,

```text
(partial_t^2-u^2 Laplacian)phi=J,
J(x,t)=q(t)delta^3(x-z(t)).
```

Write

```text
g(tau)=t-tau-R(tau)/u,
R(tau)=|x-z(tau)|.
```

The retarded Green integral contains `delta(g(tau))`. For simple roots,

```text
delta(g(tau))
 =sum_r delta(tau-tau_r)/|g'(tau_r)|,

g'(tau_r)
 =-[1-rhat_r.v_r/u].
```

Hence

```text
phi(x,t)
 =sum_r q(tau_r)/
  [4 pi u^2 R_r |1-rhat_r.v_r/u|].
```

The runner reproduces the source's two supercritical roots

```text
tau_1=0.32037766123870326,
tau_2=0.7907334498724078
```

to maximum error `5.551e-17`. Both have

```text
R_r |1-beta cos(theta_r)|
 =sqrt(Delta)
 =0.1322875655532294,
```

so their unit-source amplitudes agree at
`0.601549141925419` to `8.882e-16`. The maximum root residual is
`2.220e-16`; the finite-difference Jacobian residual is `4.525e-11`.

## 7. Covariantization and its ownership gate

For a covariant hyperbolic scalar operator, the local Hadamard form is
schematically

```text
G_ret(x,x')
 =Theta_+(x,x')
  [U_H(x,x') delta(sigma)+V_H(x,x') Theta(-sigma)].
```

Here `sigma` is Synge's world function. Integration over a point worldline
gives a direct root weight

```text
1/|sigma_;a' u_s^a'|
```

and a curvature/mass tail from `V_H`. The flat history Jacobian is the direct
term of this covariant construction after the source parameter and charge
normalization are fixed.

This does not derive geometry. The metric, characteristic cone, mode speed
and tail must come from the principal symbol and retarded inverse of the
existing parent Hessian. The toy speed `u` cannot be imported as a new MTS
coefficient.

For the selected canonical local motion scalar, the principal cone is
luminal at leading order and ordinary material histories are timelike.
The straight-map fold requires `beta=v/u>1`; therefore it is absent on that
local branch. A galaxy-state fold would require a parent-derived subluminal
collective occupied mode or a more general non-injective history map. That
condition is useful because it allows the local GR branch to remain silent,
but it also creates a compulsory causality/Cherenkov stability gate.

## 8. Finite-root no-go and critical-fold IR theorem

A finite set of regular retarded roots has spectrum

```text
Phi(omega)=sum_r A_r exp(-i omega tau_r)
          =sum_n (-i omega)^n/n! sum_r A_r tau_r^n.
```

It is analytic at `omega=0`. The executed second-order Taylor residual at
`omega=1e-5` is `5.287e-17`. Finite regular histories therefore cannot by
themselves generate the nonanalytic checkpoint-5189 target
`C_q~mu/|k|`.

At a fold, however,

```text
rho_history~Delta^(-1/2).
```

For an isotropic stationary state, an analytic scalar discriminant has

```text
Delta(k)=Delta_0+d2(|k|/mu)^2+O(k^4).
```

There are two exact branches:

```text
Delta_0>0:
rho_history -> Delta_0^(-1/2)
    finite; no 1/|k|;

Delta_0=0, d2>0:
rho_history
 =mu/[sqrt(d2)|k|]+O(|k|/mu).
```

The exponent audit gives

```text
fold      Delta^(-1/2) -> |k|^-1      target match;
cusp      Delta^(-2/3) -> |k|^-4/3    mismatch;
segment   Delta^(-1)   -> |k|^-2      mismatch.
```

The fitted slopes are `-1.0000000000000002`,
`-1.3333333333333324` and `-2.0000000000000004`. Thus the fold is the
unique one of the three source-tested singularity classes that supplies the
required infrared exponent under an analytic isotropic `k^2` normal form.

This is conditional, not a fit and not a galaxy result. The parent still has
to derive:

```text
Delta_0=0;
d2>0;
nonzero occupied-state fold weight;
causal spectral sign;
common-channel projection;
zero slip mixing;
bounded TT projection;
amplitude A;
the crossover q=0.77.
```

## 9. Decision

```text
Poynting as an extra MTS source                       = rejected;
observer flux velocity as a fundamental field        = rejected;
global total-stress frame = scalar clock              = rejected;
classical U_chi as own P(X)-stress Landau frame       = derived;
occupied T_occ timelike eigenframe                    = viable diagnostic;
single/null global frame                              = impossible;
flat retarded Jacobian root formula                   = reproduced;
finite regular roots as 1/|k| kernel                  = rejected;
critical fold plus isotropic k^2 normal form           = exact conditional 1/|k| bridge;
local selected two-derivative GR+Maxwell branch       = retained;
new parent coupling claim                             = false;
derived galaxy susceptibility                         = false;
full MTS claim                                        = false.
```

The extra maths has therefore produced a real narrowing and one constructive
mechanism. It has not replaced the parent action.

## 10. Next derivation

The next theory target is:

```text
derive the occupied-motion retarded CTP kernel from the parent chi Hessian;
extract its isotropic common-scalar discriminant Delta(omega,k);
prove or reject Delta(0,0)=0 and d2>0;
derive the state weight and characteristic speed;
then impose Ward, slip and TT gates before fitting any galaxy amplitude.
```

If the parent kernel does not generate the critical fold, this route is
rejected rather than repaired with an inserted `1/|k|` closure. If it does,
the infrared exponent is no longer phenomenological; only its amplitude and
crossover remain to be calculated.

## Artifacts

- `scripts/Y5_R2FR_5335_covariant_zero_flux_energy_frame_and_retarded_history_bridge.py`
- `source-intake/maths_exploration/5335/maths-exploration-bridge-source-lock.md`
- `source-intake/functional_rg/5335/source_register.csv`
- `source-intake/functional_rg/5335/covariant_energy_frame_theorem.csv`
- `source-intake/functional_rg/5335/energy_frame_numeric_cases.csv`
- `source-intake/functional_rg/5335/electromagnetic_null_nonnull_energy_frame_classification.csv`
- `source-intake/functional_rg/5335/retarded_history_Jacobian_checks.csv`
- `source-intake/functional_rg/5335/retarded_covariantization_and_analyticity.csv`
- `source-intake/functional_rg/5335/critical_fold_IR_susceptibility_bridge.csv`
- `source-intake/functional_rg/5335/MTS_energy_frame_retarded_bridge_verdict.csv`
- `source-intake/functional_rg/5335/branch_safety_and_claim_boundary.csv`
- `source-intake/functional_rg/5335/next_target.csv`
- `source-intake/functional_rg/5335/covariant_energy_frame_retarded_history_bridge_result.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5335_VALIDATION.csv`

All `16/16` validation gates pass. The protected formalization-workbench
digest remains
`0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f`.
No GitHub action occurred.
