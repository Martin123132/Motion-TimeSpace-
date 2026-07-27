# 5151 - Parent projective occupation to conserved Einstein-cluster stress and two-metric cog gate

Marker: `MTS_5151_PROJECTIVE_OCCUPATION_EINSTEIN_CLUSTER_STRESS_GATE`.

Date: `2026-07-20`.

## Decision

The direct state-stress route is constructively viable at the stationary
existence level. It does not need the checkpoint-5150 propagator dressing.
The reflection-even CTP two-point state has a collisionless Wigner limit

```text
Delta T^munu_state = integral dPi p^mu p^nu f(x,p),
p^mu nabla_mu f = 0,
<psi> = 0.
```

A stationary axisymmetric distribution may depend on the conserved orbit
labels `E`, `L_z` and a third integral where one exists. The explicit
spherical circular-orbit member derived below is also axisymmetric and gives
one conserved, positive stress realizing the machine/cog requirement. This
is an existence theorem, not yet the parent-selected galaxy state.

Primary comparison sources for static and axisymmetric Einstein--Vlasov
states and circular-orbit clusters are
`https://arxiv.org/abs/gr-qc/9304028`,
`https://arxiv.org/abs/1006.1225` and
`https://arxiv.org/abs/0705.1756`.

## Exact positive cored-profile representation

For any `0<q<2`, set `alpha=q/2` and `s=x^2`. The projective occupation has
the exact Stieltjes representation

```text
n_q(x)=x^q/(1+x^q)
      =integral_0^infinity dt [x^2/(x^2+t)] rho_q(t),

rho_q(t)=sin(pi alpha) t^(alpha-1)
         /{pi[1+2t^alpha cos(pi alpha)+t^(2alpha)]}.
```

The density is positive and normalized. Each kernel
`x^2/(x^2+t)` is a regular cored flat-rotation component with

```text
rho_t(r)=U_infinity/(4pi G)
         (r^2+3r_c^2)/(r^2+r_c^2)^2,
r_c=L sqrt(t).
```

Thus the fractional projective law is not an arbitrary singular halo profile:
it is a unique positive continuum of regular core scales. The two parent
exponents `1.8496934455116607` and `1.858483853942984` both lie inside the positivity
window. Numerical quadrature reconstructs the occupation with worst relative
error `2.695982226145779e-15`.

The uncut continuum still has `rho proportional r^(q-2)` at the exact centre
and a linearly growing mass at infinity. For the parent exponents the central
force behaves as `r^(q-1)` and therefore vanishes, unlike an extrapolated
`q=0.77` force. A finite smallest core and outer density boundary are still
mandatory for a globally regular, finite-mass state; they must come from
`J_gap`, formation and the parent boundary state rather than per-galaxy
patches.

## Parent exponent maps to the empirical support

The old galaxy support is `1-exp[-(r/L_eff)^0.77]`. It was already proved not
to be the projective occupation itself. Allowing only one global conversion
`n_q(a r/L_eff)`, with no galaxy-by-galaxy shape parameter, gives

```text
best parent mapping = Wetterich_v_equals_plus_2lambda,
q_parent            = 1.8496934455116607,
a                    = 1.7271465744325227,
R_n/L_eff            = 0.578989655425489,
shape RMSE           = 0.06514699919477658.
```

The rejected 5148 common-propagator route had shape RMSE
`0.0616004223044119`. The direct parent-state value is
slightly worse but genuinely comparable, and it uses the parent exponent
near `1.85` rather than relabelling it as `0.77`. The required source-amplitude
law is now concrete:

```text
R_n=xi ell_gap C_n^(-1/q_parent)=L_eff/a,
C_n=(xi ell_gap a/L_eff)^q_parent.
```

This scaling is derived. Its normalization and dynamical population are not.
The numerical `q_parent` values are critical exponents of the source-locked
parent Hessian. Their transport to the infrared occupied state under the
`k proportional 1/r` shell map remains conditional; this checkpoint proves
that the parent values have a viable stress realization, not that the RG
trajectory has already delivered them unchanged to galaxies.

## Conserved stress and both metric functions

Use areal radius and

```text
ds^2=-A(r)c^2dt^2+B(r)dr^2+r^2dOmega^2,
beta(r)=v_c^2(r)/c^2.
```

First isolate the motion component to prove existence. Take a reflection-even
ensemble of massive motion quanta on circular orbits with all orbital planes
populated symmetrically. Its radial pressure and net momentum vanish. The
exact spherical Einstein equations, circular-geodesic condition and
conservation law give

```text
p_r=0,
w=Gm/(c^2r)=beta/(1+2beta),
B=(1-2w)^(-1)=1+2beta,
d ln A/d ln r=2beta,
p_t=p_theta=p_phi=rho c^2 beta/2,

rho=c^2/(4pi G r^2)
    [w+d w/d ln r].
```

For `beta=beta_infinity n_q(a r/L_eff)`, both metric functions are explicit:

```text
A(r)/A(L_eff)
 =[(1+(a r/L_eff)^q)/(1+a^q)]^(2 beta_infinity/q),
B(r)=1+2 beta_infinity n_q(a r/L_eff).
```

The density is positive, the weak-field circular-shell gate has
`kappa_r^2 proportional n_q[2+q(1-n_q)]>0`, and the dominant-energy margin is
enormous for the executed galaxies. No radial pressure or lensing slip was
inserted by hand: the tangential stress follows from conservation.

Those closed forms are the exact isolated-cluster existence solution. In an
actual baryonic galaxy the motion quanta orbit in the **total** metric. At
leading weak order the density contribution superposes while conservation
changes the motion tangential stress to

```text
p_t,motion/(rho_motion c^2)=v_total^2/(2c^2).
```

The all-point execution below uses this total baryonic-plus-motion velocity;
it does not mislabel the isolated expression as an exact disk solution.

## All-175 scale and local-cog execution

Using only the locked amplitude `U_infinity=Gamma0 L_eff` from the read-only
5148 interface, both parent mappings were evaluated for all 175 galaxies.

```text
maximum beta_infinity                         = 5.669295153257982e-07,
maximum p_t/(rho c^2)                         = 2.834647576628991e-07,
maximum weak lensing-gradient proxy deviation = 5.669288725083764e-07,
largest WKB m_gap floor at R_n                 = 2.81669166215576e-22 eV,
largest embedded Mercury tidal ratio           = 6.614360568718464e-19.
```

The full read-only ROTMOD pass then evaluates all
`3391` measured radii with the unchanged baryonic law.
For the best parent mapping it gives

```text
mean RMSE:   21.024301108192173 km/s
locked mean: 21.889021670909763 km/s
median RMSE: 16.044649772143135 km/s
locked med.: 17.153268394916555 km/s
wins:        121/175
pooled RMSE: 33.48575685418064 versus 33.75732021897959 km/s
```

This is a genuine out-of-construction interface smoke: the one global phase
conversion was chosen against the published support shape, not optimized per
galaxy or against the velocities. It modestly improves the unweighted radial
RMSE. It is not a replacement for the galaxy project's uncertainty,
jackknife and population tests.

All total velocities remain nonrelativistic, with maximum
`v_total^2/c^2=1.2191437962544262e-06` and motion
`p_t/(rho c^2)<=6.095718981272131e-07`. The
leading pressure-sensitive lensing order is below
`1.2191408236384825e-06`. A projected deflection
claim still requires a finite outer boundary because the untruncated plateau
is not asymptotically flat.

An occupied galactic state need not vanish at the Solar System. Its uniform
acceleration is shared by Sun and planet; the relative orbital effect is the
halo tide. At the explicitly declared diagnostic location `R_host=L_eff`,
the worst Mercury ratio is below `7e-19` and the worst Neptune ratio is below
`4e-13`, while the classical scalar fifth force remains zero. This is not a
global Solar-System PPN bound, but it demonstrates how the Mercury cog can
keep turning inside a smooth occupied galactic state.

## What is and is not achieved

```text
CTP state stress from positive occupation                = derived in WKB form;
stationary axisymmetric kinetic contract                 = derived;
spherical circular-orbit realization                     = constructed;
projective occupation as positive cored continuum        = exact;
parent q near 1.85 retained                              = yes;
parent q transported to the occupied infrared state      = not yet derived;
conserved rho, p_r, p_t                                  = derived;
both spherical metric functions                          = derived;
rotation support and leading lensing compatibility       = passed conditionally;
embedded local Mercury/planet cog                         = strongly suppressed;
one universal metric/Hilbert coupling                     = retained;
source-selected C_n and total occupation                  = not yet derived;
finite central core and outer halo boundary               = not yet derived;
full flattened axisymmetric galaxy solution               = not yet solved;
full projected lensing likelihood                         = not yet run;
galaxy or full-MTS claim                                  = false.
```

If the parent cannot generate the required `C_n`, state normalization and
finite boundaries, this route is only collisionless scalar halo matter under
a new name. The next derivation must therefore attack the source selection,
not refit the stress profile: obtain the circular-state occupation from the
formation CTP kernel with one `J_gap` and carry the exponent down the
occupied infrared trajectory, or reject this route.

All `21` validation checks pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. No GitHub or galaxy-repo
write occurred.
