# 5166 - Sourced CIE cooling, clumping-derived assembly clock and forward-response gate

Marker: `MTS_5166_SOURCED_CIE_COOLING_DERIVED_CLOCK_FORWARD_RESPONSE_GATE`.

Date: `2026-07-21`.

## Question

Checkpoint 5165 proved that Poynting/total-energy conservation excludes an
impulsive source but cannot select a one-orbit clock: every positive monotone
history can be assigned a luminosity satisfying the same integrated identity.
This checkpoint asks the missing constructive question. Does ordinary charged-
baryon plasma microphysics supply a clock before the galaxy response is read?

## Entropy and cooling projection

For baryon current `N_b^mu=n_b u^mu`, the closed worldtube obeys

```text
nabla_mu N_b^mu=0.
```

The checkpoint-5165 Maxwell exchange is split from escaping radiation as

```text
nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda,
nabla_mu T_b^{mu nu}= F^nu_lambda J^lambda-G_rad^nu.
```

Contracting with `u_nu` and using the first law gives the minimal entropy
projection

```text
n_b T u^mu nabla_mu s=j_cond^mu E_mu-Q_rad.
```

On the neutral, no-external-heating, optically thin CIE branch,

```text
Q_rad=n_H^2[Lambda_prim(n_H,T)+(Z/Zsun)Lambda_metal(n_H,T)].
```

The cooling coefficients are read from the immutable Grackle
`CloudyData_noUVB.h5` table at commit `928696482fbe15d9bac4382de6134d95568f099c`. They are not
inferred from `q`, the rotation curve or a desired duration.

The same checkpoint-5164 mass coordinate gives

```text
M_hot(<r,lambda)=[b-mu lambda]M_X(<r),
T_vir=mu_bar m_p G M_tot(R_edge)/(2 k_B R_edge),
K(lambda) dot(lambda)=L_CIE(lambda),
t(lambda)=integral_0^lambda K(x)/L_CIE(x) dx.
```

Thus the response receives the inverse of the final integral directly. A C2
ramp with a fitted or manually chosen duration is not used.

## Sourced inputs and numerical result

The fixed-edge virial solution is

```text
T_vir                         = 1314274.0487669532 K
mean molecular weight         = 0.61226
tau_e(lambda=0)               = 0.00028960082791591003
tau_e(lambda=1)               = 0.0001492436225264951
Cloudy shell n_H range        = 9.758469145473242e-06 .. 0.002952095954325897 cm^-3.
```

The optical-depth values are far inside the XSTAR electron-scattering
reference envelope `tau_e<=0.3`; line and photoelectric escape are not thereby
proved. The inherited two antithetic particle states give a Poisson-self-pair-
subtracted, radial-gradient-controlled clumping factor
`C=1.5385341412037419` at cell width
`27.824538897172758 kpc`. Pair means at the three
predeclared resolutions are `{13: 1.5167698711776387, 20: 1.497631108966023, 26: 1.5385341412037419}`.

With this resolved pair clumping, the forward-frozen CIE clocks are

```text
Z=0.1 Zsun: 4.302288610288357 Gyr = 3.2142398640115175 transition orbits;
Z=0.3 Zsun: 1.826692151371429 Gyr = 1.3647217246593508 transition orbits.
```

The inherited one-to-four-orbit response window is
`1.338508883067272 .. 5.354035532269088 Gyr`. Both standard
benchmark metallicity branches enter it without reading `q`. The inverse
metallicity corridor is recorded only as a requirement; UGC09133 has no hot-
phase metallicity measurement in the inherited source and the corridor is not
used to choose the two forward runs.

## Direct initial-value response

The exact CIE schedules were inserted into the checkpoint-5164 particle
evolution. Results are

```text
Z=0.1: q=2.376080267862411, RMSE=0.2791849168854609 dex,
       transition v^2 ratio=0.3736892830524089;
Z=0.3: q=2.426883714866849, RMSE=0.2911000922263307 dex,
       transition v^2 ratio=0.3560018000834963.
```

The parent interval is `1.511977636680018 .. 2.20499007120595`.
The time-refined `Z=0.3` value is `2.4231802176392696`, differing by
`0.0037034972275793443` from the primary run.

## Decision and claim boundary

`SOURCED_CIE_CLOCK_IMPROVES_THE_BASELINE_RMSE_BUT_BOTH_PREDECLARED_FORWARD_BRANCHES_MISS_THE_PARENT_Q_BAND_SO_ONE_ZONE_HOMOLOGOUS_COOLING_IS_REJECTED_AS_THE_COMPLETED_PARENT_CLOCK`.

This is a constructive advance and a useful rejection. A sourced plasma law now
replaces the arbitrary duration and is propagated through the actual inherited
dynamics, but both predeclared branches lie above the parent `q` interval. The
one-zone homologous CIE clock is therefore rejected as the completed parent
mechanism rather than promoted because it improved the RMSE. The next derivation
must replace homologous depletion by a radial entropy/cooling-flow solve; line
transfer and the unmeasured hot-phase metallicity must also be bounded.

```text
baryon entropy projection derived                         = yes;
real CIE coefficient table sourced                       = yes;
resolved clumping estimated without Poisson self-pairs   = yes;
clock duration fitted to q                               = no;
exact derived lambda(t) evolved forward                  = yes;
one-zone homologous CIE clock passes parent q gate        = false;
UGC09133 metallicity measured                            = no;
radial radiation-hydrodynamic cooling flow solved        = no;
local GR/Newton/Maxwell branch modified                   = no;
galaxy or full-MTS claim                                  = false.
```

All `22` validation rows pass. The protected
`formalization-workbench` digest remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub action occurred.
