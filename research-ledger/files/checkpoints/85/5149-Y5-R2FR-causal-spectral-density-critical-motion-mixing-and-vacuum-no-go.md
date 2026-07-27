# 5149 - Causal spectral density, critical motion mixing and vacuum no-go

Marker: `MTS_5149_CAUSAL_SPECTRAL_DENSITY_CRITICAL_MOTION_MIXING_GATE`.

Date: `2026-07-20`.

## Decision

The checkpoint-5148 response is not left as an arbitrary nonlocal function.
Its static spectral measure is derived exactly and is positive for the locked
`q=0.77`. It therefore admits a causal continuum **response**
completion. The same function cannot be promoted to a Lorentz-invariant
vacuum graviton propagator with a positive Kallen--Lehmann continuum: that
continuum has the opposite sign. The viable interpretation is consequently a
state-dependent motion-medium susceptibility inside the existing universal
metric theory, not a replacement vacuum graviton.

## Exact static spectral representation

For `s=k^2`, checkpoint 5148's dimensionless factor is

```text
C_q(s)=mu^(1+q)/[sqrt(s)(s^(q/2)+mu^q)].
```

Across the cut `s=-t+i0`, its Stieltjes density is

```text
rho_C(t)=mu^(1+q)[mu^q+t^(q/2)cos(pi q/2)]
         /{pi sqrt(t)[mu^(2q)+2mu^q t^(q/2)cos(pi q/2)+t^q]}.
```

For `0<q<=1`, every factor is nonnegative and hence

```text
C_q(s)=integral_0^infinity rho_C(t)/(s+t) dt,
rho_C(t)>0.
```

The numerical reconstruction spans twelve decades in `s/mu^2` and has
maximum relative error `5.98642246885106e-11`.
The minimum sampled density is `2.6991731518749142e-12`.

One causal continuation is the retarded oscillator continuum

```text
C_R(omega,k)=integral_0^infinity dt rho_C(t)
              /[k^2+t-(omega+i0)^2].
```

This proves existence of a causal response kernel. It does not prove that the
current MTS state supplies precisely this density or coupling.

## Vacuum positivity gate

On the physical transverse conserved-source spin-2 coefficient, if one
instead declares

```text
D_vac(s)=[1+A C_q(s)]/(M_R^2 s),
```

then away from the massless pole its continuum density is

```text
rho_D(t)=-A rho_C(t)/(M_R^2 t)<0  for A>0.
```

That fails vacuum Kallen--Lehmann positivity. The checkpoint-5148 kernel is
therefore rejected as a fundamental Lorentz-invariant vacuum propagator. A
medium CTP response can evade that vacuum inference because the state breaks
Lorentz invariance and the complete metric-plus-medium system, not the
reduced static metric kernel alone, owns positivity.

## Critical mixing theorem

For the Hessian Schur complement define

```text
zeta(k)=B K_chi^-1 B_dagger/K_h
       =A C_q/(1+A C_q).
```

The executed asymptotics are

```text
zeta(k) ~ A(mu/k)^(1+q)                    at k >> mu,
1-zeta(k) ~ k/(A mu)                       at k << mu.
```

The measured log slopes are `-1.7696613135637107` and
`1.0002827701968626`, against exact targets
`-1.77` and `+1`. Thus the galaxy state must approach unit
normalized metric-motion mixing in the infrared, with determinant

```text
det Gamma2 = K_h K_chi(1-zeta) proportional to |k| K_h K_chi.
```

This is a criticality condition, not a small loop correction.

## Current-parent compatibility

The checkpoint-4949 stationary local operator has `m_gap^2>0`, positive
quadratic form and `B=0` on the reflection-even vacuum. More generally, a
finite local gapped Hessian with analytic coefficients has a Taylor series in
`k^2`; without a determinant zero it gives finite renormalization, and even a
local tuning cannot generate the required `|k|` term. It therefore cannot
produce the 5148 response in its stationary vacuum.

The remaining route is precise: an occupied, gapless or critical CTP
collective state must generate a transverse nonanalytic stress response and
the full Hessian must satisfy the unit-mixing limit without a negative-norm
mode or Jeans instability. Time-dependent Poynting or gravitational flux may
enter only through that same retarded stress correlator; the stationary/DC
no-pair theorem remains intact.

## Next calculation

Construct the smallest reflection-even occupied-state Hessian allowed by the
functional `P(X)` parent, calculate its retarded stress-stress polarization,
and test three non-negotiable conditions:

1. transverse Ward identity;
2. `1-zeta(k)` linear in `|k|` across the galactic corridor;
3. positive full-system spectral/gradient matrix.

If a regular gapped state cannot satisfy them, the current motion-scalar
realization of the 5148 bridge is rejected rather than renamed as closure.

All `13` validation checks pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub or galaxy-repo
write occurred.
