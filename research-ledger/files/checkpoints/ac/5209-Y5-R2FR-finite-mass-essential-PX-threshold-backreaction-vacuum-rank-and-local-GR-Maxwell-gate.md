# 5209 - Finite-Mass Essential `P(X)` Threshold, Backreaction, Vacuum Rank and Local-GR/Maxwell Gate

Private derivation and robustness checkpoint. No GitHub action and no
full-MTS, vacuum-selection or public cosmology claim.

Marker: `MTS_5209_FINITE_MASS_ESSENTIAL_PX_VACUUM_BRANCH_GATE`.

## Executive result

The finite motion mass can be inserted into the locked optimized functional
trace without inventing a closure. For scalar and graviton propagator counts
`p_s,p_g`,

```text
q_i,n^(p_s,p_g)(w_s,w_g)
 =[1/n!-eta_i/(2(n+1)!)]
  /[(1+w_s)^p_s(1+w_g)^p_g].
```

After the checkpoint-4958 essential metric quotient, the weak sources are

```text
y=1/(1+w);

S2(w)
 =24-(32/3)y-(4/3)y^2+4y^3;

S3(w)/pi
 =-96+144y-96y^2-(224/5)y^3+(256/5)y^4.
```

Thus `S2(0)=16` and `S3(0)=-208 pi/5`, exactly reproducing the locked
massless coefficients. The mass-deformed numerical Hessian reproduces both
formulae at every calibration point.

## 1. Exact `A2` trajectory

With `w=m_gap^2/k^2`, `dw/d ln k=-2w`, and
`A2=a2/g^2`, the leading essential weak flow is

```text
dA2/d ln k=S2(w).
```

An exact primitive is

```text
F2(w)
 =-8 ln w-4 ln(1+w)-(4w+7)/[3(1+w)^2],

-2w dF2/dw=S2(w).
```

The symbolic residual is `0`. Relative to
the massless logarithm, the finite-mass correction starts as

```text
Delta A2_mass=-(2/3)w-(7/3)w^2+4w^3+O(w^4).
```

## 2. Scale-consistency/no-overlap theorem

The locked local polynomial projector is controlled for

```text
x=Y/k^4<=0.1,
Y=M_R^2 H^2 q^2.
```

A finite-mass threshold requires `w=m_gap^2/k^2` of order one. At `w=1`,

```text
x=Y/m_gap^4.
```

The exact fitted checkpoint-5208 background gives

```text
max w inside x<=0.1
 =1.350715928101e-47;

min x when w=1
 =5.481153409542e+92.
```

Therefore the finite-mass threshold region and the controlled local `P(X)`
polynomial region do not overlap anywhere on `-18<=N<=0`. Evaluating the
whole finite polynomial at `k~m_gap~H0` would place it at an enormous
dimensionless gradient and is not a controlled functional calculation.

Inside the controlled region the maximum relative mass change in `A2` is

```text
6.613374035043e-51.
```

This closes the finite-mass question at the resolved local-functional order:
the massless essential trajectory is valid where the local expansion is
valid. The `k~H` rows are retained only as formal `X2`-coefficient
extrapolations, not as a full-`P(X)` claim.

## 3. Cosmological nonlinear-stress bound

For the Lorentzian convention

```text
P(Y)=Y/2+sum_(n>=2) c_n Y^n,
rho_n=(2n-1)c_n Y^n,
M_R^2=(8 pi G_N)^-1,
```

the exact `X2` ratios are

```text
rho_X2/rho_kinetic
 =6 A2 G_N H^2 q^2/(8 pi);

Omega_X2
 =A2 G_N H^2 q^4/(8 pi).
```

Scanning the exact refitted background gives

```text
max |rho_X2/rho_kinetic|
 =6.344596947491e-121;

max |Omega_X2|
 =1.833061566226e-122;

max |c_s^2-1|
 =8.459462596654e-121.
```

The resolved `N=3..8` local-polynomial partial sum is at most
`10^(-183.716801)` relative to
the canonical kinetic density. The actual checkpoint-4958 `A3` would need
at least `63.518541` additional orders
of magnitude to equal the already negligible `X2` term.

The exact baseline likelihood replay remains

```text
chi2_joint=1475.171854806321.
```

The derived nonlinear background fraction is far below numerical and
observational resolution, so a refit cannot produce a meaningful parameter
shift.

## 4. Vacuum-rank theorem

For a normalized even regular-mode state, adding nonlinear `P(X)` terms
changes the homogeneous constraint from

```text
Omega_Lambda+K2 sigma2=R
```

to

```text
Omega_Lambda+K2 sigma2+c2 K4 sigma4+...=R.
```

The first Jacobian is `[1,K2]`, with rank one and nullity one. The nonlinear
Jacobian is `[1,K2,c2 K4,...]`, still rank one but with at least two null
directions. Even imposing the un-derived Gaussian closure
`sigma4=3 sigma2^2` leaves one equation for
`{Omega_Lambda,sigma2}`.

Three explicit positive witnesses are generated from the locked
checkpoint-5205 row. Therefore essential `P(X)` cannot select
`Lambda_cal=0`; it makes the state-moment degeneracy larger unless an
independent parent state law fixes every required moment.

The conservative finite mass-dependent one-loop vacuum piece obeys

```text
|Delta Omega_vac,mass|
 <=8.781062042761e-123.
```

It is both renormalization-condition dependent and far too small to select
the observed vacuum split.

## 5. Local GR, Newton and Maxwell

On the selected constant-`F_R` branch,

```text
delta S_m/delta chi =0;
delta S_EM/delta chi=0.
```

The standard Maxwell stress tensor and its on-shell conservation law remain
unchanged. `P(X)` changes only the motion stress and scalar principal
operator. Its sound-cone and stress corrections are bounded above, so the
checkpoint-5208 local response and cosmological-tide bounds are unchanged
to the displayed accuracy. Newton calibration remains
`M_R^2=(8 pi G_N)^-1`.

## 6. Decision

```text
mass-deformed optimized threshold              = derived;
essential X2 and X3 weak sources               = derived and calibrated;
exact finite-mass A2 primitive                 = derived;
controlled-PX / finite-mass overlap            = excluded on fitted history;
finite-mass nonlinear cosmology backreaction   = bounded negligible;
direct material scalar charge                  = exact zero;
direct Maxwell-motion portal                   = exact zero;
Newton calibration                             = unchanged;
Lambda_cal=0 from P(X)                         = rejected by rank theorem;
parent vacuum-coordinate selection             = still open;
all-order nonlocal effective action             = still open;
full MTS unification                           = not claimed.
```

The next target is not another finite-polynomial scan. It is

```text
DERIVE_PARENT_VACUUM_COORDINATE_OWNERSHIP_OR_PROVE_THAT_LAMBDA_CAL_IS_
AN_INDEPENDENT_RENORMALIZATION_CONDITION.
```

## 7. Evidence

Generator:

`scripts/Y5_R2FR_5209_finite_mass_PX_vacuum_branch_gate.py`

Evidence directory:

`source-intake/functional_rg/5209/`

Evidence CSV digest:

`bd7c18f88d15245f58f4ce195563233ea3a7441194b08dac78637d3868e83538`

Validation:

`source-intake/mts_residuals/P8_Y5_BRR545_5209_VALIDATION.csv`
