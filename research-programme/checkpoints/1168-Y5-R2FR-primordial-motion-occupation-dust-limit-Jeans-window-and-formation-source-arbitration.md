# 5152 - Primordial motion occupation, dust limit and Jeans window

Marker: `MTS_5152_PRIMORDIAL_MOTION_OCCUPATION_JEANS_GATE`.

Date: `2026-07-20`.

## Decision

The one-machine/two-cog criterion is now explicit. The same low-energy parent
action used for local GR is retained,

```text
S = integral sqrt(-g) [M_R^2(R-2 Lambda)/2
                       -(nabla psi)^2/2-m_gap^2 psi^2/2
                       +higher parent operators]
    +S_matter[g,A,Phi_SM].
```

No galaxy-only coupling or arena switch is added. Ordinary matter, Maxwell
stress including Poynting momentum, and the motion-state stress all enter the
same Hilbert tensor. The local cog remains metric-coupled GR plus the tiny
external stress of the galactic state. The galaxy cog is allowed to contain a
nonvacuum motion population.

The controlled local and formation calculations at 4949 and 4953--4959 show
that a static baryonic metric does not manufacture that population and the
tested high-frequency cascades cannot supply it. Checkpoint 5152 therefore
tests the logically distinct primordial-state route rather than repeating
those rejected kernels.

**Result:** a primordial reflection-even massive motion state survives the
background, WKB and instantaneous linear-Jeans gates. It is selected as the
next dynamical route. This does not yet derive its abundance or prove that
nonlinear collapse generates the checkpoint-5151 `n_q` profile.

## 1. Reflection-even state without a local scalar charge

For a homogeneous representative,

```text
ddot(psi)+3H dot(psi)+m_gap^2 psi=0.
```

The CTP state can be the even mixture

```text
rho_even=(|+psi_i><+psi_i|+|-psi_i><-psi_i|)/2.
```

Every odd correlator, including `<psi>`, vanishes, while its quadratic stress
is identical to either representative. Thus the construction does not add a
linear matter charge and does not undo the reflection-even local source
theorem. Its abundance is initial-state data, not local particle production.

## 2. Exact radiation-era dust theorem

In radiation domination `H=1/(2t)`. With `x=m_gap t`, the regular solution is

```text
psi/psi_i=2^(1/4) Gamma(5/4) x^(-1/4) J_(1/4)(x).
```

For `x>>1`, its oscillation-averaged stress obeys

```text
<p_psi>=0,
<rho_psi>=C_RD m_gap^2 psi_i^2 (a_osc/a)^3,
C_RD=4 Gamma(5/4)^2/pi=1.0460496200531022,
H_rad(a_osc)=m_gap.
```

The numerical Bessel audit gives maximum Klein--Gordon residual
`4.441e-16`, late-cycle
`<w>=1.471e-03`, and asymptotic
comoving-energy error `5.266e-08`.
This is a derivation of dust behavior, not an assumed equation of state.

The MTS component replaces the `Omega_CDM` part of the checkpoint-4897
baseline; it is not added on top:

```text
Omega_b=0.04924319136384048,
Omega_X=Omega_m-Omega_b=0.2657568086361595,
Omega_m=0.315.
```

At the all-galaxy WKB floor `m_gap=2.81669166215576e-22 eV`, oscillations
begin at `z=4544345.804762872`. The exact radiation matching requires
`psi_i=0.04316877211439324 Mbar_Pl`. The motion/radiation
ratio at onset is only `0.0006497861092370445`,
and the largest calculated transition-era change to `H` relative to the
metric-only CDM baseline is `0.0002938260154063954`.
All tested masses begin oscillating well before equality.

This closes the background *existence* question with one global initial
amplitude. It does not derive that amplitude from the parent state-preparation
law, and primordial isocurvature has not yet been tested.

## 3. Linear clustering and the mass window

The nonrelativistic scalar perturbation obeys

```text
ddot(delta)+2H dot(delta)
 +[hbar^2 k^4/(4m_gap^2 a^4)-4 pi G rho]delta=0,

k_phys,J^4=16 pi G rho m_gap^2/hbar^2.
```

Using the total matter density in the gravity term, the marginal WKB mass has
at equality

```text
lambda_J,com=0.4142000432323609 Mpc,
k_J,com=15.1694462852936 Mpc^-1,
M_J=1477632934.0064604 Msun.
```

The intentionally conservative internal benchmark `m_gap=1e-20 eV` gives

```text
lambda_J,com(eq)=0.0695152027839874 Mpc,
M_J(eq)=6985146.588722531 Msun,
z_osc=27077078.079300284,
psi_i/Mbar_Pl=0.017684977958814553.
```

These are instantaneous Jeans scales, not a transfer-function, CMB or
Lyman-alpha likelihood. They prove that a nonempty clustering window exists;
they do not establish observational preference.

## 4. Joint galaxy/WKB gate

All `350` checkpoint-5151 galaxy/parent rows imply

```text
m_gap >= 2.81669166215576e-22 eV
    for lambda_db <= R_n,
m_gap >= 2.8166916621557602e-21 eV
    for lambda_db <= 0.1 R_n.
```

Demanding additionally that the instantaneous equality Jeans wavelength be
below `100 kpc` gives

```text
m_gap >= 4.8323634180988915e-21 eV.
```

The joint internal lower benchmark is therefore
`4.8323634180988915e-21 eV`; `1e-20 eV` passes.
This is an engineering target for the next collapse calculation, not a fitted
or observed MTS mass and not an upper bound.

## 5. Higher-derivative control

For the parent `c_ess X^2` operator, the exact quadratic-control condition at
oscillation is

```text
|c_ess| X_osc < epsilon,
X_osc approximately (m_gap psi_i)^2/2.
```

Across the mass grid, one-percent control requires the equivalent suppression
scale `Lambda_ess=|c_ess|^(-1/4)` above at most
`9812.829327108715 eV`. A Planck-natural
coefficient gives maximum `|c_ess|X=2.6374310757624864e-96`.
The free massive approximation is therefore easily controlled for a
Planck-suppressed comparator, but the actual infrared parent `c_ess` still has
to be transported and inserted.

## 6. Mercury and the local cog

No direct scalar fifth force is introduced. At the explicitly declared
checkpoint-5151 host location, the largest halo tide/solar ratio remains
`3.100454538921604e-13`. The homogeneous cosmological
motion density gives only `9.276849079440763e-25`
at Mercury. A diagnostic `0.3 GeV/cm^3` local scalar density gives a largest
oscillating metric-potential amplitude
`6.123486393339988e-19` over the tested
mass grid. These checks preserve the local cog but are not a complete global
Solar-System PPN or pulsar-timing likelihood.

## 7. What moved and what remains

Derived or constructed here:

```text
one action for local and galactic sectors                  = retained;
reflection-even primordial state with <psi>=0              = constructed;
exact radiation-era dust limit                             = derived;
Omega_X replacement of CDM background                      = executed;
nonempty WKB plus linear-clustering mass window             = derived;
static/formation source no-go bypass without contradiction = established.
```

Still absent:

```text
parent preparation of psi_i or Omega_X                     = not derived;
primordial perturbation/isocurvature spectrum               = not derived;
IR value of c_ess and all higher-operator control           = incomplete;
nonlinear collapse to C_n and n_q                           = not derived;
finite core and outer boundary                              = not derived;
flattened rotating distribution and lensing likelihood     = not derived.
```

The branch is therefore more than an inserted galaxy closure, because one
primordial state evolves under one parent action and passes explicit
background/scale/local gates. But until nonlinear evolution selects the MTS
profile and normalization, it remains observationally indistinguishable in
its background role from ordinary ultralight scalar dark matter. That is the
next falsifiable boundary, not a wording problem.

## 8. Next calculation

Evolve the reflection-even state from cosmological initial data through the
Schrodinger--Poisson/Vlasov limit at three fixed masses: the strict WKB floor,
`1e-20 eV`, and `1e-18 eV`. The gate is whether one global initial spectrum
and the parent interaction generate, without a galaxy-by-galaxy shape fit,

```text
C_n proportional (ell_gap/L_eff)^q_parent,
n_q(r)=r^q/(R_n^q+r^q),
a finite central core,
a finite outer boundary,
and the checkpoint-5151 conserved stress.
```

If not, the current galaxy state route is scalar-halo closure and must be
demoted. No direct formation-emission route is to be retried without a new
parent operator.

Primary references:

- Turner, coherent scalar oscillations: https://doi.org/10.1103/PhysRevD.28.1243
- Hwang and Noh, linear CDM limit: https://arxiv.org/abs/0902.4738
- Hu, Barkana and Gruzinov, Jeans/wave scale: https://arxiv.org/abs/astro-ph/0003365
- Schive et al., nonlinear wave-halo formation: https://arxiv.org/abs/1407.7762
- Khmelnitsky and Rubakov, oscillating metric diagnostic: https://arxiv.org/abs/1309.5888

All `23` validation checks pass. The protected
`formalization-workbench` hash remains `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.
No GitHub or galaxy-repository write occurred.
