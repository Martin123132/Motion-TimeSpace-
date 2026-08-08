# 5208 - Common Minimal Motion Trajectory, Canonical-`Z` Quotient, Absolute-Scale Covariance and Local-GR Selection

Private derivation and empirical robustness checkpoint. No GitHub action and
no full-MTS or public cosmology claim.

Marker: `MTS_5208_COMMON_MINIMAL_MOTION_TRAJECTORY_SCALE_COVARIANCE`.

## Executive result

The checkpoint-5207 finite-curvature branch is not the unique route connecting
the cosmological scalar to local GR. A cleaner source-selected branch exists.

For one scalar with `Z(psi)>0`, define

```text
chi(psi)=integral_0^psi sqrt(Z(u)) du.
```

Then the two-derivative kinetic term is canonical exactly. Near the
reflection-symmetric origin,

```text
m_can^2       =m2/Z0;
lambda4_can   =lambda4/Z0^2-2 m2 z2/Z0^3;
xi_can        =xi2/Z0;
zeta_c        =xi2/(2 Z0);
c_X2,can      =c_X2/Z0^2.
```

Thus `Z`, `F_R`, `V` and `c_X2` are not four independent germs. The physical
trajectory must be stated in canonical invariant coordinates.

## 1. Minimal common trajectory

The locked parent results imply:

```text
massless shift-symmetric surface:
  m2=lambda4=xi=z2=0 is invariant;

relevant mass eigenvector:
  no linear xi component in the exact source comparator;

regular quartic:
  irrelevant in the MTS potential projection;

essential X2 function:
  one GR-connected relevant direction and therefore trajectory-owned.
```

The leading common trajectory is consequently

```text
F_R(chi)=M_R^2;
V(chi)=m_gap^2 chi^2/2;
Z_can=1;
P_ge2(X)=the locked GR-connected essential P(X) trajectory;
Lambda_cal=0 as an explicit branch hypothesis.
```

This is a two-scale theory, not a parameter-free theory: measured `G_N` and
one universal `J_gap=G_N m_gap^2` remain the two relevant data. No value may
be retuned by arena.

## 2. Absolute-scale theorem

For an autonomous dimensionless RG system, translating RG time gives

```text
u_delta(k)=u(exp(-delta)k);
G_N -> exp(-2delta) G_N;
m_gap -> exp(delta) m_gap;
G_N m_gap^2 -> G_N m_gap^2.
```

Therefore an autonomous parent flow can predict dimensionless ratios and
critical exponents but cannot select an absolute number in SI units. The
measured value of `G_N` is one legitimate dimensional integration constant,
just as in GR. This is an exact scale-covariance result rather than an
unfilled coefficient ledger.

For the fitted minimal branch,

```text
H0                    =1.434376050624e-33 eV;
m_gap                 =1.097038525483e-33 eV;
J_gap                 =8.074034372765e-123;
ln(M_N/H0)            =138.684455218.
```

## 3. Direct source-selected refit

Fixing `zeta_c=0` rather than fitting it gives

```text
Omega_m               =0.311668148681;
mu=m_gap/H0           =0.764819326846;
H0                    =67.2431118289 km/s/Mpc;
Omega_b h^2           =0.0225663102893;
phi0                  =2.60060760456;
q0                    =-0.416353415857;
M_R^2/M_N^2           =1;
present source ratio  =1;
gamma-1               =-0;
Gdot/G                =-0 yr^-1;
chi2_joint            =1475.17185481;
AIC_joint             =1489.17185481;
BIC_joint             =1527.02307878.
```

Against the fitted finite-`zeta_c` checkpoint-5207 branch:

```text
Delta chi2=0.205226478543;
Delta AIC =-1.79477352146;
Delta BIC =-7.20209123193.
```

The finite coupling buys only a small chi-square change. AIC is draw-scale
but numerically favors the minimal branch, while BIC clearly favors it after
the extra coordinate is counted. The source-selected zero-coupling branch is
therefore the better parent default.

Against standard comparators:

```text
minimal minus LCDM: Delta AIC=-1.1483,
                    Delta BIC=4.25901;
minimal minus wCDM: Delta AIC=-1.88871,
                    Delta BIC=-1.88871;
minimal minus CPL:  Delta AIC=1.35671,
                    Delta BIC=-4.05061.
```

This remains internal model-discipline evidence, not a cosmological claim.

## 4. Why local GR no longer needs a scalar transition

On the selected branch `F_R` is constant and visible matter has no direct
motion portal. Therefore the direct scalar charge of a material body is
exactly zero. A local metric perturbation can nevertheless force a tiny
response of the time-dependent homogeneous scalar:

```text
(k^2/a^2+m_gap^2) delta chi
 approximately -2 m_gap^2 chi_bar Phi
              +4 dot(chi_bar) dot(Phi).
```

Taking `k>=c/r` and the causal envelope `omega<=k` gives

```text
|delta chi/chi_bar|
 <=[2|Phi|m_gap^2
    +4|Phi||dot(chi_bar)/chi_bar|omega]
   /(k^2+m_gap^2)
 <=6.873755e-24
```

over the selected local systems. The homogeneous cosmological scalar also
contributes background stress, but its largest tested solar-system tidal
ratio is only

```text
1.054152e-19.
```

Thus the finite-`zeta` problem of dynamically forcing
`phi_cosmology -> phi_local=0` disappears on this common minimal branch.

## 5. Generated `X^2` term

The weak essential flow is

```text
beta_g=2g;
beta_c=4c+16g^2;
c=A_X2 g^2;
beta_A_X2=16.
```

Extrapolating the two locked checkpoint-4958 trajectory schemes to `k~H`
and scanning `0.01<=k/H<=100` gives

```text
max |rho_X2/rho_kinetic|
 =7.869411e-120;

max |Omega_X2|
 =1.364164e-120.
```

The generated derivative interaction is therefore retained in the parent
action but cannot be used as a cosmological fit parameter.

## 6. Remaining boundary

```text
canonical Z quotient                              = derived;
minimal mass-only F_R,V trajectory                = selected at known order;
essential X2 trajectory                           = inherited and bounded;
absolute G_N prediction from autonomous RG        = rejected exactly;
local scalar transition                           = unnecessary on zeta=0;
local GR/Newton/Maxwell leading branch             = retained;
finite-mass nonlinear functional backreaction      = not fully calculated;
absolute Lambda_cal=0 selection                    = not derived;
full MTS unification                               = not claimed.
```

Selected next route:

```text
DERIVE_FINITE_MASS_ESSENTIAL_PX_BACKREACTION_AND_VACUUM_BRANCH_SELECTION.
```
