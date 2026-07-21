# 5153 - Quantum-regularized projective halo, cosmological boundary and primordial inventory

Marker: `MTS_5153_QUANTUM_CORE_VIRIAL_INVENTORY_GATE`.

Date: `2026-07-20`.

## Decision

Checkpoint 5153 does not insert an arbitrary cored halo or an arbitrary outer
taper. It starts from the exact positive projective mixture proved at 5151,
uses the same `m_gap` window derived at 5152 to remove unresolved components,
and uses the metric-only cosmological spherical-collapse density to define a
finite outer boundary. This constructs one finite, positive, stationary
Einstein-cluster family for every existing galaxy/parent row.

The construction passes all measured-radius, density, stability, inventory,
Jeans and Schwarzschild-junction gates. It closes finite-core and finite-mass
*existence* conditionally. It does not prove that cosmological collapse
dynamically selects this family; that is now the single decisive next gate.

## 1. No new inner profile

For `alpha=q/2` and `0<q<2`, checkpoint 5151 proved

```text
n_q(x)=integral_0^infinity dt [x^2/(x^2+t)] rho_q(t),

rho_q(t)=sin(pi alpha)t^(alpha-1)
 /{pi[1+2t^alpha cos(pi alpha)+t^(2alpha)]}.
```

Each kernel is a regular cored component. The original mild cusp comes only
from integrating the continuum down to `t=0`. The same WKB relation used at
5151 fixes, without another galaxy parameter,

```text
r_c/R_n=lambda_db/R_n=m_WKB,row/m_gap,
t_min=(r_c/R_n)^2.
```

Removing only components below that resolution and renormalizing gives

```text
S_q,c(x)=N_q(t_min)^(-1)
 integral_tmin^infinity dt [x^2/(x^2+t)]rho_q(t),

N_q=1-F_q(t_min),
F_q(t)={atan[(t^alpha+cos pi alpha)/sin pi alpha]
          -(pi/2-pi alpha)}/(pi alpha).
```

This has exact properties

```text
S_q,c(0)=0,
S_q,c(infinity)=1,
dS_q,c/dx>0,
rho(0)=3 v_infinity^2 <1/t>/(4piG R_n^2)<infinity,
rho(r)>0,
2S+xS'>0.
```

Across all `1050` state/mass rows, the retained positive spectral weight is at
least `0.9988461464454078`, the largest
`r_c/R_n` is `0.09999999999999999`, and central
densities range from `0.007606819858269044` to
`0.6496827104087403 Msun/pc^3`. The maximum
independent adaptive-quadrature disagreement is
`1.2096434964803393e-12`.

This is parameter-free within the declared lower-cut prescription once
`m_gap` is fixed; it is not proved to be the unique physical regularization.
Whether nonlinear wave dynamics imposes precisely this spectral cutoff
remains unproved.

## 2. Cosmological outer boundary and exact local exterior

The checkpoint-4897 flat metric baseline gives at `z=0`

```text
Delta_vir,c=18pi^2+82(Omega_m-1)-39(Omega_m-1)^2
           =103.18310421960845,
f_X=Omega_X/Omega_m=0.8436724083687603.
```

For the exact circular-state relation

```text
beta=v_infinity^2 S_q,c/c^2,
w=G M_X/(c^2 r)=beta/(1+2beta),
M_total=M_X/f_X,
```

the virial condition `3M_total/(4pi r_vir^3)=Delta_vir,c rho_crit`
reduces to one scalar equation

```text
r_vir^2
 =2 v_infinity^2 S_q,c(r_vir/R_n)
  /[f_X Delta_vir,c H_0^2(1+2beta_vir)].
```

Because every mixture kernel has logarithmic slope below two, the mean
interior density decreases and the positive root is unique. Set the circular
state to zero beyond that orbit and continue with Schwarzschild mass
`M_X(r_vir)`. `M`, `A`, `B` and the circular derivative match at the boundary;
`p_r=0` means the finite density step does not require a radial-pressure shell.

The executed radii satisfy
`r_vir/R_n >= 13.878761943180828`. Every measured point lies inside, with
maximum `r_obs/r_vir=0.21418358696685266`. Motion masses
are finite and range from `7039600319.562261` to
`5946603008326.871 Msun`. The maximum virial identity
residual is `4.218847493575595e-15` and the exact
Schwarzschild compactness-junction residual is
`5.293955920339377e-23`.

The sharp edge is a valid compact-support circular state, not yet a derived
smooth collapse edge.

## 3. Primordial supply instead of local manufacture

For every finite motion mass,

```text
R_L=[3M_X/(4pi rho_X,0)]^(1/3),
N_X=M_X/(m_gap),
```

so a finite comoving patch of the single checkpoint-5152 primordial state
contains the exact required inventory. Across the full execution,

```text
R_L=0.3687892880629518
    ...3.486197169269676 Mpc,
N_X=7.852322844824549e+93
    ...2.3549391693494064e+99,
minimum M_total/M_Jeans(eq)=178.56962804284632,
minimum R_L/lambda_Jeans(eq)=2.8155818571381523.
```

Thus none of the candidate halos needs the rejected local multiplicity
cascade. This proves available finite inventory, not the primordial power or
probability for each patch to collapse.

## 4. Does regularization break the galaxy cog?

No profile parameter was fitted. The existing `q_parent`, one global phase
map, `L_eff`, `v_infinity`, baryonic law and all `3391` measured radii were
held fixed. Three masses and two parent branches give `20346` executed radial
points.

At the strict WKB floor the two pooled finite-profile RMSE values are
`[33.49199553668417, 33.48576002254654]` versus
unregularized `[33.49199260520024, 33.48575685418064]`.
At `1e-20 eV` they are
`[33.491992884754026, 33.485757159310225]`.
The largest support change at any measured point over the entire mass grid is
`0.0009778925282547743` and no observed point
crosses the virial boundary. Therefore the physically finite construction
preserves the checkpoint-5151 galaxy result rather than obtaining regularity
by changing its fit.

This remains an unweighted interface smoke, not a galaxy likelihood.

## 5. Exact status

```text
positive finite-core equilibrium family              = constructed;
finite cosmological virial boundary                   = constructed conditionally;
exact Schwarzschild exterior junction                 = derived;
finite primordial inventory for every halo            = derived;
all candidate patches above instantaneous Jeans gate  = verified;
parent q profile preserved on all measured radii      = verified;

wave dynamics selects t_min coefficient               = not derived;
primordial spectrum creates the Lagrangian patches    = not derived;
collapse selects C_n and n_q as an attractor           = not derived;
smooth outer-edge distribution                        = not derived;
flattened rotating state and lensing likelihood       = not derived.
```

This is real movement: the earlier infinite cusp/mass objections no longer
block existence, and the formation-number objection is bypassed by one finite
primordial inventory. But equilibrium existence cannot be promoted into a
formation theorem.

## 6. Next calculation

Perform the phase-space gate before a costly cosmological run. Invert the
finite density and metric to a nonnegative distribution function, first in
the isotropic Eddington/Vlasov branch and then in the circular anisotropic
limit already known to exist. Test radial-orbit stability and whether a
single dimensionless distribution can cover all mass rows. If no positive
finite distribution continuously connects the cosmological initial state to
the `q_parent` profile, demote this route. If it passes, execute the nonlinear
Schrodinger--Poisson/Vlasov collapse at the three fixed masses.

Primary references:

- wave/Jeans support: https://arxiv.org/abs/astro-ph/0003365
- nonlinear wave halos: https://arxiv.org/abs/1407.7762
- spherical-collapse virial scaling: https://arxiv.org/abs/astro-ph/9710107
- compact static Einstein--Vlasov states: https://arxiv.org/abs/gr-qc/9304028

All `24` validations pass. The protected
`formalization-workbench` hash remains
`b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`. The galaxy sample was
read-only. No GitHub action occurred.
