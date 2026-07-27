# 5204 - Curvature-triggered homogeneous motion state: local PPN, `Gdot` and preparation no-overlap theorem

Date: 2026-07-24

Marker: `MTS_5204_CURVATURE_TRIGGERED_MOTION_STATE_NO_OVERLAP`

Status: private analytic and source-executed checkpoint. This is a derivation,
not another missing-coefficient ledger. It tests and rejects one concrete
mechanism for generating the fitted homogeneous motion state while retaining
the near-minimal curvature coordinate and the checkpoint-5203 local-GR branch.
It does not promote the checkpoint-5195 compressed-CMB fits or make a full MTS
claim.

## Executive result

1. A convention ambiguity is removed. In the canonically normalized motion
   coordinate `chi=sqrt(Z0) psi`, define

   ```text
   zeta_c = F_R''(0)/(2 Z0),
   F_R = M_R^2 + zeta_c chi^2 + O(chi^4).
   ```

   Therefore the checkpoint-4951 coefficient is

   ```text
   xi_4951 = zeta_c = xi2_5203/(2 Z0).
   ```

   This factor of two must be fixed before importing either the Hessian or the
   one-loop beta function.

2. The exact fixed-curvature onset functional is

   ```text
   V_eff(chi;R)
    = (m_pole^2-zeta_c R) chi^2/2
      +lambda4 chi^4/24.
   ```

   For `lambda4>0`, it has the pitchfork

   ```text
   chi=0,

   chi_*^2=6(zeta_c R-m_pole^2)/lambda4,

   V_eff''(chi_*)=2(zeta_c R-m_pole^2)>0.
   ```

   This derives the candidate mechanism completely at homogeneous onset. It
   also exposes its problem: reflection symmetry leaves `chi=0` exact, and
   the nonzero minima return continuously to zero when curvature falls.

3. Reconstructing the two checkpoint-5195 target states gives
   `chi_0/M_R=0.841386` and `2.60405`. Cassini permits only
   `zeta_c<=4.87292e-3` and `1.58016e-3` in the standard long-range
   Jordan-minimal scalar-tensor map. A deliberately conservative two-sigma
   LLR drift envelope tightens these to

   ```text
   zeta_c <= 5.65824e-4  (Lambda free),
   zeta_c <= 1.62711e-4  (Lambda zero).
   ```

4. The fitted states would have to remain curvature-broken today only if

   ```text
   zeta_c > m_pole^2/R_0
          =0.172378 or 0.0672585.
   ```

   These floors exceed the LLR ceilings by factors `304.65` and `413.36`.
   There is no present broken-branch/local-bound overlap.

5. Deep in matter domination, the radial restoring mass at the nonzero
   minimum obeys

   ```text
   m_rad^2/H^2 -> 6 zeta_c.
   ```

   Even the deliberately weak tracking requirement `m_rad>=H` needs
   `zeta_c>=1/6`. The LLR ceilings are smaller by factors `294.56` and
   `1024.31`. Thus the field cannot adiabatically follow the moving minimum
   and use it to forget its initial amplitude.

6. The most generous linear matter-era comparator amplifies a seed from
   equality to today by at most `1.00925` and `1.00266` at the LLR ceilings.
   The actual matter-era tachyonic interval ends near `z=13.25` and `14.65`,
   giving only `1.00622` and `1.00176`. This is not an amplitude-selection
   mechanism.

The decision is therefore:

```text
curvature-triggered preparation of the 5195 state = rejected;
near-minimal F_R coordinate                       = retained;
checkpoint-5203 local GR branch                   = retained;
common F_R,V,Z,X2 trajectory fully selected       = no;
next route                                        =
  derive Gamma_rho_i homogeneous state preparation
  or demote parent-scalar cosmology to fitted closure.
```

## 1. Why checkpoint 4886 is not being recycled

Checkpoint 4886 tested a direct universal trace owner,

```text
S_m=S_m[A^2(phi)g,Psi_m],
A(phi)=exp(beta phi^2).
```

The checkpoint-5203 parent instead places visible matter minimally in one
Jordan coframe and retains the curvature function required by the interacting
motion functional:

```text
S = integral sqrt(-g) [
      F_R(chi) R/2
      -(partial chi)^2/2
      -V(chi)
    ]
    +S_visible[g,Psi].
```

After transformation to the Einstein frame,

```text
A_E^2=M_R^2/F_R=(1+zeta_c phi^2)^-1,
phi=chi/M_R.
```

Its small-field expansion gives

```text
ln A_E=-zeta_c phi^2/2+O(phi^4),
beta_4886=-zeta_c/2.
```

Thus the two routes are distinct parent constructions, but their local
scalar-tensor pressure is related rather than avoidable. The 4886 result is
used only as a normalization cross-check; all 5204 bounds are recalculated
from the checkpoint-5203 curvature owner.

## 2. Exact homogeneous branch law

The canonically normalized linear operator about `chi=0` is

```text
K_chichi=-Box+m_pole^2-zeta_c R.
```

Neither `chi^2 X`, `X^2` nor higher even potential terms alter this first
onset. With the minimal positive quartic stabilizer,

```text
dV_eff/dchi
 =chi[m_pole^2-zeta_c R+lambda4 chi^2/6].
```

For `zeta_c R>m_pole^2`,

```text
chi_*^2
 =6(zeta_c R-m_pole^2)/lambda4,

Delta V_eff(chi_*)
 =-3(zeta_c R-m_pole^2)^2/(2 lambda4).
```

The radial Hessian is positive:

```text
V_eff''(chi_*)=2(zeta_c R-m_pole^2).
```

This proves the local bifurcation. It does not choose the sign, create a
classical seed, or normalize a state. Exact `chi=0` initial data remain exact
because the equation is homogeneous and reflection even.

## 3. Matter-era preparation test

Using `N=ln a`, the linear homogeneous equation is

```text
chi_NN+(3+H_N/H)chi_N
 +(m_pole^2/H^2-zeta_c R/H^2)chi=0.
```

Deep in matter domination,

```text
H_N/H=-3/2,
R/H^2=3,
m_pole^2/H^2 << 1.
```

The growing index is therefore

```text
s_+
 =[-3/2+sqrt(9/4+12 zeta_c)]/2
 =2 zeta_c+O(zeta_c^2).
```

At the broken minimum,

```text
m_rad^2/H^2
 =2(3 zeta_c-m_pole^2/H^2)
 ->6 zeta_c.
```

The condition `zeta_c>=1/6` used here is intentionally generous. It asks only
for `m_rad>=H`; true overdamped adiabatic tracking would require a stronger
inequality. Failure of this weaker condition is sufficient to reject
minimum tracking.

For the locally allowed values, the matter-era restoration points are

| 5195 target | `z_eq` | `z_exit` at LLR ceiling | maximum equality-to-exit growth | deliberately extended equality-to-today growth |
|---|---:|---:|---:|---:|
| `ParentScalar_Lambda_free` | 3436.41 | 13.2453 | 1.00622 | 1.00925 |
| `ParentScalar_Lambda_zero` | 3461.62 | 14.6537 | 1.00176 | 1.00266 |

The extended column removes the stabilizing mass and pretends the
matter-curvature instability lasts until today. It is deliberately more
generous than the actual tachyonic interval. Even this cannot erase or select
initial data.

There are only two outcomes:

```text
track the minimum:
  chi_* -> 0 at symmetry restoration, so the fitted nonzero state is lost;

fail to track:
  a residual chi survives, but its amplitude remains initial-state data.
```

Curvature by itself therefore does not supply the missing homogeneous
preparation functional.

## 4. Reconstructing the 5195 targets

Checkpoint 5195 uses

```text
x=dot(chi)/(sqrt(6) M_R H),
y=m_pole chi/(sqrt(6) M_R H),
mu=m_pole/H0.
```

At `N=0`,

```text
x_0=-sqrt(Omega_chi) sin(theta),
y_0= sqrt(Omega_chi) cos(theta),

chi_0/M_R=sqrt(6)y_0/mu,
d(chi/M_R)/dN=sqrt(6)x_0.
```

The locked fitted target rows give:

| target | `mu` | `Omega_chi,0` | `theta_0` | `chi_0/M_R` | `d(chi/M_R)/dN` | `R_0/H_0^2` |
|---|---:|---:|---:|---:|---:|---:|
| `Lambda_free` | 1.232099 | 0.201781 | 0.341775 | 0.841386 | -0.368780 | 8.806624 |
| `Lambda_zero` | 0.763868 | 0.688275 | 0.206092 | 2.604048 | -0.415852 | 8.675401 |

These are empirical target states, not parent-derived constants. A finite
`zeta_c` changes their background equations, so the 5195 likelihood is not
promoted or silently reused. The target rows are used only to ask whether the
new curvature coordinate can prepare the state it was supposed to explain.

## 5. Local scalar-tensor map

For canonical `Z=1`,

```text
F_R/M_R^2=1+zeta_c phi^2,
F_R,chi=2 zeta_c chi.
```

The exact Damour--Esposito-Farese coupling is

```text
alpha_0^2
 =F_R,chi^2/[2 F_R+3 F_R,chi^2]
 =2 zeta_c^2 phi_0^2
  /[1+zeta_c phi_0^2+6 zeta_c^2 phi_0^2].
```

The long-range weak-source PPN result is

```text
gamma-1=-2 alpha_0^2/(1+alpha_0^2).
```

The local Cavendish normalization is

```text
G_cav
 =1/(8 pi F_R)
  [2 F_R+4 F_R,chi^2]/[2 F_R+3 F_R,chi^2].
```

Consequently the fitted `phi_N` gives an absolute prediction for
`d ln G_cav/dt` once `zeta_c` is chosen; it is not an independent coefficient.

The source ledger records

```text
Cassini:
 gamma-1=(2.1 +/- 2.3)e-5;
 conservative absolute two-sigma envelope =6.7e-5;
 alpha_0^2<3.35011223e-5.

LLR:
 Gdot/G=(-5.0 +/- 9.6)e-15 yr^-1;
 conservative absolute two-sigma envelope =2.42e-14 yr^-1.
```

The resulting GR-connected ceilings are:

| target | Cassini `zeta_c,max` | `Gdot` at Cassini ceiling, yr^-1 | LLR `zeta_c,max` | `gamma-1` at LLR ceiling |
|---|---:|---:|---:|---:|
| `Lambda_free` | 4.87292e-3 | 2.05994e-13 | 5.65824e-4 | -9.06232e-7 |
| `Lambda_zero` | 1.58016e-3 | 2.32130e-13 | 1.62711e-4 | -7.17323e-7 |

The LLR row is the stronger gate for these moving target states.

## 6. Range and compact-object checks

The fitted masses give

```text
m_pole AU
 =1.34478e-15  (Lambda free),
 =8.30650e-16  (Lambda zero).
```

Solar-System Yukawa attenuation is therefore negligible. The long-range PPN
and drift map cannot be evaded by calling the field short ranged.

Checkpoint 4950 gives the easiest tested compact instability threshold

```text
zeta_c,crit(neutron-star top-hat)=2.38703.
```

The LLR ceilings are smaller by factors `4218.68` and `14670.34`.
Therefore this particular allowed branch is safely below the inherited
compact-body instability thresholds. This is useful: the route is not being
rejected because every local test is assumed hostile. It passes compact
stability and fails specifically as a cosmological state selector.

Positive `zeta_c` also makes positive-curvature matter more, not less,
tachyonic. It does not provide a symmetron-like local restoration escape.

## 7. No-overlap theorem

Assume:

1. the same canonically normalized scalar owns the checkpoint-5195 target and
   the checkpoint-5203 `F_R` coordinate;
2. visible matter is minimally coupled to the single Jordan coframe;
3. no new disformal frame, kinetic-screening function or independent local
   state switch is inserted;
4. the scalar is long ranged on Solar-System scales, as the fitted mass
   requires;
5. the conservative Cassini and LLR envelopes above are applied;
6. the minimal even stabilizer is regular near onset.

Then:

```text
present curvature-broken state:
 zeta_c >= {0.172378, 0.0672585};

local moving-state ceiling:
 zeta_c <= {5.65824e-4, 1.62711e-4};

minimal adiabatic tracking:
 zeta_c >= 1/6.
```

Both target rows have empty intersections. Moreover the exact homogeneous
equation has no additive source, and the maximum locally allowed linear
growth is percent-level or smaller. Therefore:

```text
the analytic chi^2 R pitchfork cannot derive the 5195 homogeneous amplitude.
```

This conclusion is scoped. A strongly field-dependent `Z(chi)`, a genuinely
new screening operator or a CTP state functional would define a different
calculation and require a complete cosmological refit plus renewed local
tests. They are not hidden escape clauses inside this theorem.

## 8. Joint RG trajectory

The checkpoint-4951 fixed-background comparator is

```text
beta_lambda4=3 lambda4^2/(16 pi^2),
beta_zeta=lambda4(zeta_c-1/6)/(16 pi^2).
```

It has the exact first integral

```text
(zeta_c-1/6)/lambda4^(1/3)=constant.
```

Thus the one-loop system transports one trajectory invariant; it does not
select its value. Also, preserving the checkpoint-5195 quadratic target to
ten percent requires approximately

```text
lambda4 < 8.99e-121  (Lambda free),
lambda4 < 3.58e-122  (Lambda zero).
```

At such values the displayed infrared running is physically negligible over
finite cosmological logarithms. It cannot be invoked as a dynamical selector
for `zeta_c`.

The conformal comparator `zeta_c=1/6` would make the deep-matter radial mass
only marginally Hubble sized, but on the fitted present states it predicts

```text
gamma-1=-0.06168, Gdot/G=4.88e-12 yr^-1;
gamma-1=-0.20716, Gdot/G=1.10e-11 yr^-1.
```

It is not a viable physical endpoint for these targets.

## 9. What survives

This checkpoint does not damage the derived local spine:

```text
translation-gauge coframe ancestry     = retained;
TEGR/EH identity                       = retained;
one Hilbert source                     = retained;
Newton/PPN/Maxwell local leading limit = retained on chi=0;
analytic Z2 local double zero          = retained;
positive local scalar Hessian          = required and satisfied at small zeta_c;
near-minimal F_R EFT coordinate        = retained.
```

What is removed is one attempted explanation of the cosmological state:

```text
curvature pitchfork as amplitude selector = rejected.
```

The common action remains viable as an EFT packet, but the nonzero
homogeneous state is still a state-selection problem rather than a consequence
of `F_R R`.

## 10. Executed evidence

Generator:

`scripts/Y5_R2FR_5204_curvature_triggered_motion_state_gate.py`

Evidence directory:

`source-intake/functional_rg/5204/`

Files:

```text
canonical_curvature_and_bifurcation_derivation.csv
parent_scalar_local_bound_and_preparation_rows.csv
curvature_trigger_corridor_scan.csv
joint_flow_invariant_and_trajectory_status.csv
route_decision.csv
source_provenance.csv
curvature_triggered_motion_state_results.json
```

Validation:

`source-intake/mts_residuals/P8_Y5_BRR545_5204_VALIDATION.csv`

Every evidence row remains `valid_for_full_MTS_claim=false`.

## 11. Next derivation

The selected route is

```text
DERIVE_CTP_HOMOGENEOUS_STATE_PREPARATION_OR_DEMOTE_PARENT_SCALAR_COSMOLOGY.
```

The next construction must start from the already required
`Gamma_rho_i[Sigma_i]` rather than adding another bulk curvature coefficient.
It must produce, in one calculation:

1. a normalized initial density functional;
2. the regular radiation-era homogeneous state or a unique state measure;
3. conserved bulk-plus-state stress;
4. no local stationary scalar charge on the selected local branch;
5. the checkpoint-5195 amplitude and phase without fitting them as new parent
   constants;
6. a full scalar-tensor cosmology refit if the prepared state keeps finite
   `F_R'`.

If no such state functional can be derived, the parent-scalar likelihood work
remains valuable phenomenology but is demoted to fitted closure. The
local-GR/Newton/Maxwell derivation remains intact either way.

## Sources

- Checkpoint 4886: direct-trace scalar-tensor completion and Cassini relation.
- Checkpoints 4950 and 4951: curvature Hessian, local spectral thresholds and
  fixed-background `V-F-Z-X2` flow.
- Checkpoints 5193 and 5195: canonical homogeneous variables and locked fitted
  target states.
- Checkpoint 5203: one canonical translation-gauge parent action.
- `source-intake/local_bounds/local_bound_claims.csv`: Cassini and LLR source
  anchors, including DOI `10.1038/nature01997` and
  DOI `10.3390/universe7020034`.
