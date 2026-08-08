# 5165 - Baryon/Maxwell/Poynting assembly-clock identifiability and energy-bound gate

Marker: `MTS_5165_BARYON_MAXWELL_POYNTING_ASSEMBLY_CLOCK_GATE`.

Date: `2026-07-21`.

## Question actually answered

Checkpoint 5164 found that a mass-conserving visible-source history near one
transition orbit moves the resolved collisionless exponent into numerical
contact with the parent band. This checkpoint asks whether the existing
baryon plus Maxwell/Poynting equations *derive that duration*, rather than
selecting it because it works.

They do not derive a unique duration, but the calculation is not merely a
missing-input ledger. It proves the precise non-identifiability theorem,
computes the parent-owned energy barrier, excludes an impulsive history, and
shows that the one-to-four-orbit response is energetically admissible and not
a single finely tuned clock point.

## Covariant derivation

The existing parent action gives

```text
nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda,
nabla_mu T_matter^{mu nu}=+F^nu_lambda J^lambda,
nabla_mu(T_EM^{mu nu}+T_matter^{mu nu})=0.
```

Poynting flow is the `0i` component of this same Hilbert stress, not another
source. For the observed-time Killing field `xi`, the worldtube current
`J_E^mu=-T^mu_nu xi^nu` therefore obeys

```text
Delta E_total + integral_boundary J_E.n dSigma = 0.
```

On the closed-baryon worldtube branch, or with any matter flux retained
explicitly, a one-coordinate quasistatic assembly `lambda(t)` becomes, after
retaining endpoint field energy and mechanical work in `E_mech(lambda)`,

```text
L_out(t)=K(lambda) dot(lambda),
K(lambda)=-dE_mech/dlambda,
dot(lambda)=L_out/K.
```

The last expression is a clock only if the charged-matter state supplies a
constitutive `L_out[lambda,state]`. Maxwell evolution determines `F` for a
specified current; current conservation does not determine the dissipative
current, emissivity, opacity or boundary flux. For every positive duration
`T` and every monotone endpoint-preserving `lambda_T`,

```text
L_T(t)=K(lambda_T) dot(lambda_T)
```

has the same integrated endpoint energy. The generated clock families verify
this identity numerically. Energy conservation alone therefore has an
infinite family of clocks, not a hidden one-orbit prediction.

## Frozen-profile energy projection

The calculation uses exactly the checkpoint-5164 mass-conserving source
coordinate. With `b=Omega_b/Omega_X`, measured condensed mass `M_c`, resolved
motion mass `M_X`, and `mu=M_c(R_edge)/M_X(R_edge)`,

```text
M_b(r,lambda)=(b-lambda mu)M_X(r)+lambda M_c(r),
M_tot(r,lambda)=(1+b)M_X(r)+lambda[M_c(r)-mu M_X(r)].
```

Thus the baryon mass at the fixed edge is independent of `lambda`. On the
spherical frozen-motion endpoint branch,

```text
W(lambda)=-G integral_0^R M_tot(r,lambda) dM_tot(r,lambda)/r
         =W0+W1 lambda+W2 lambda^2,
E_vir(lambda)=W(lambda)/2,
K(lambda)=-(W1+2W2 lambda)/2.
```

For the primary resolved pair,

```text
M_X(R_edge)                  = 2514412294695.019 Msun
M_c(R_edge)                  = 225804813799.87292 Msun
Delta E_binding              = 3.578693974236985e+52 J
Delta E_radiated (virial)    = 1.7893469871184925e+52 J
K_min                        = 7.410020069160251e+51 J
quadrature relative change   = 1.0662775091098126e-07
```

`K` stays positive, so every tested monotone history has nonnegative outgoing
power. This endpoint estimate is conditional on spherical projection, a
frozen motion profile and virialized endpoints; it is not presented as a
full radiative-hydrodynamic simulation.

## Clock and response result

The fixed-edge light-crossing time is
`0.0011797696063842644 Gyr`. The zero-duration impulsive history is
therefore rejected. All four distinct positive durations already predeclared
in checkpoint 5164 remain causal and lie far below the diagnostic condensed-
baryon Eddington luminosity scale.

For the one-orbit `C2` history,

```text
T                              = 1.338508883067272 Gyr
required average luminosity    = 4.236130605845907e+35 W
required average luminosity    = 1106617190.6598504 Lsun
required peak luminosity       = 8.885675232120723e+35 W
peak / condensed Eddington     = 3.1303025149258354e-07
```

UGC09133's tabulated SPARC surface photometry integrates to
`273938375290.21222 Lsun`; a flat completion of
the unmeasured central cell gives
`280768050139.6599 Lsun`. These are
Spitzer 3.6-micron luminosity scales, not bolometric cooling luminosities, so
they are capacity comparators only and are never used to select a clock.

The one-orbit numerical refinement interval still intersects the parent `q`
band. More importantly, the predeclared one- and four-orbit primary responses
differ by only `0.004884644110929592` in `q`. The useful
response is therefore stable over a factor-four duration bracket even though
the parent has not yet selected a member of that bracket.

## Decision

Route decision:
**POYNTING_ENERGY_BALANCE_EXCLUDES_IMPULSIVE_ASSEMBLY_AND_PROVES_A_BROAD_ONE_TO_FOUR_ORBIT_RESPONSE_ENERGETICALLY_ADMISSIBLE_BUT_CANNOT_SELECT_A_CLOCK_WITHOUT_A_PARENT_CONSTITUTIVE_EMISSIVITY**.

This is a positive bound and a clean no-go for one proposed derivation route:

```text
same parent Maxwell/Hilbert/Poynting source used      = yes;
mass-conserving energy barrier derived                = yes;
impulsive assembly excluded                           = yes;
one-orbit history energetically admissible            = yes;
one-to-four-orbit response robust                      = yes;
energy conservation uniquely selects assembly clock   = no;
constitutive emissivity/current parent-derived        = no;
galaxy or full-MTS claim                               = false.
```

The next non-circular target is the charged-baryon constitutive law, not
another arbitrary response scan: project covariant baryon continuity, Euler
and entropy equations with the already-derived Maxwell exchange into an
explicit cooling/escape luminosity `L_out[lambda,state]`. Standard plasma or
radiative inputs must be sourced and held fixed before the response is read.
If that law cannot place the clock inside the broad one-to-four-orbit window,
the visible-source route is closure-only and the collective density-matrix
stress route becomes the next parent-owned alternative.

All `21` validation rows pass. Every generated row
remains nonclaim, all source hashes are unchanged, the protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`, and no GitHub action was
performed.
