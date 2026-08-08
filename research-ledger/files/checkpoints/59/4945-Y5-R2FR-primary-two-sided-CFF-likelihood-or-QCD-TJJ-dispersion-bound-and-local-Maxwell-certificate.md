# 4945 - Primary CFF sign, pulsar geometry and weak-local certificate

Marker: `MTS_PRIMARY_CFF_TWO_SIGN_GEOMETRY_LOCAL_CERTIFICATE_4945`.

Date: `2026-07-13`.

Status: private analytic, source-acquired and source-executed checkpoint. This
checkpoint proves that the primary polarization-splitting formula is
two-sided in the photon-curvature coefficient. It also finds that the legacy
`6.0e6 m^2` pulsar number used by checkpoints 4931 and 4944 cannot be
reproduced from the primary formula and stated source geometry. Replacing the
stellar-radius path by the measured binary-orbit impact parameter gives a
much weaker historical envelope. The correction is propagated rather than
hidden. It leaves a conditional weak-local CFF certificate for Earth and Sun,
but removes the former compact-object certificate and does not create a raw
likelihood or a general Maxwell theorem.

## 1. Primary mode equation and coefficient sign

Keep the convention

```text
L_EM=-F_mn F^mn/4+c_gamma C_mnrs F^mn F^rs.
```

The primary source derives, on a Schwarzschild exterior,

```text
p^2=+/-12 c_gamma (GM/r^3)p_3^2,
c_(gamma,+/-)=+/-12 c_gamma.
```

Writing the positive geometric travel factor as `A`, its two mode times are

```text
T_+(c_gamma)=T_GR+12 c_gamma A,
T_-(c_gamma)=T_GR-12 c_gamma A.
```

Therefore

```text
T_+(-c_gamma)=T_-(c_gamma),
T_-(-c_gamma)=T_+(c_gamma),

Delta T_signed=24 c_gamma A,
Delta T_split =24 |c_gamma| A.
```

A coefficient-sign reversal exchanges the mode labels. The observable
separation of an unresolved pair of orthogonally polarized pulses is even in
`c_gamma`. Consequently any threshold on the splitting is mathematically a
two-sided coefficient gate:

```text
|Delta T_split|<=tau_max
  implies
|c_gamma|<=tau_max/K,

K=24 M_geom S/(c b^2)>0.
```

This closes the sign question without imposing `c_gamma>0`. It constructs a
top-hat acceptance gate, not a statistical likelihood.

## 2. Audit of the legacy printed bound

The 2003 source states

```text
tau_max=1 microsecond,
M_companion=1.33 M_sun,
R_companion=10 km,
c_gamma<0.6e11 cm^2=6.0e6 m^2.
```

Its own far-observer formula is

```text
Delta T_split
 =24 c_gamma M_geom S/(c b^2),

S=sqrt(1-b^2/r_f^2)+sqrt(1-b^2/r_i^2).
```

For an observer at Earth, the first term is effectively one and hence

```text
1<=S<=2.
```

Substituting the source's stated `10 km`, `1.33 M_sun`, one-microsecond
allowance and printed bound backwards gives

```text
S_inferred=0.1060074.
```

That is outside the allowed interval. With `S=2`, the same formula and stated
grazing radius instead give

```text
|c_gamma|<=3.18022e5 m^2.
```

The printed number would correspond to an effective impact parameter about
`43.4 km` at `S=2`, but no such value is stated or derived. Thus the printed
`6.0e6 m^2` number and its `6.0025e6 m^2` secondary recast are not
reproducible evidence. Their old five-system projections remain historical
checkpoint outputs but are superseded for current inference.

## 3. Physical PSR B1534+12 impact parameter

The updated timing source gives

```text
P_b=0.420737298879 day,
e=0.27367752,
omega=283.306012 degree,
s=sin(i)=0.9772+/-0.0016,
m_2=1.3455 M_sun,
M=2.678463 M_sun.
```

On the already selected local-GR/Newton branch,

```text
a=c[T_sun M(P_b/2pi)^2]^(1/3),
r(f)=a(1-e^2)/(1+e cos f),
b^2(f)=r^2(f)[1-s^2 sin^2(omega+f)].
```

The conjunction stationary equation is

```text
e sin f/(1+e cos f)
 -s^2 sin(omega+f)cos(omega+f)
  /[1-s^2 sin^2(omega+f)]
 =0.
```

Solving it, rather than replacing the ray by the neutron-star radius, gives

```text
central physical impact b =6.11083e8 m,
central S                 =1.97719169,
central |c_gamma| bound   =1.18743e15 m^2.
```

Using `s-2 sigma`, the lower two-sigma companion mass and upper two-sigma
total mass gives the deliberately weaker envelope

```text
b_cons                    =6.52014e8 m,
|c_gamma^IR|_cons         =1.35442e15 m^2.
```

The impact parameter is more than `6.1e4` times the stated stellar radius.
At the conservative coefficient bound the expansion parameter on the actual
pulsar propagation leg is only

```text
12|c_gamma|M_geom/b^3=1.16e-7,
```

so the weak-curvature formula is internally perturbative there. The envelope
still inherits the historical one-microsecond allowance; it is not a new fit
to pulse data.

## 4. Why this is not yet a primary likelihood

The acquired 2014 package reports 22 years of timing, preserves polarimetric
information in the backend products and gives a `4.57 microsecond` global RMS
residual. The 2020 FAST study directly shows polarization-dependent emission
states and a `62 microsecond` single-pulse jitter scale. Neither source
archive supplies polarization-separated TOAs, their covariance, a
machine-readable Stokes timing data set or a likelihood containing the CFF
template.

The claim in the 2003 source that all systematics disappear in a polarization
difference is therefore too broad. Astrometry and emission epoch are common
mode, but orthogonal emission modes, magnetized plasma, profile evolution and
jitter need not be.

The operator audit gives:

```text
R F^2 and Ricci_mn F^mr F^n_r = zero on the Ricci-flat exterior;
on-shell D F D F representatives = not an independent exterior pole;
minimal GR/Maxwell               = common metric cone;
cold plasma                      = frequency-dependent nuisance;
magnetized plasma                = polarization-dependent nuisance;
intrinsic orthogonal modes       = source-phase nuisance;
parity-odd C F Ftilde            = absent only by the declared parent symmetry.
```

An extreme Euler-Heisenberg control with a `1e11 T` surface field and a
`12 km` dipole radius gives

```text
Delta T_QED<=3.96e-30 s,
```

so magnetic-vacuum birefringence is negligible at the measured impact
parameter. Plasma and intrinsic polarized pulse structure remain the real
raw-likelihood competitors.

## 5. Corrected universal local projection

Using the conservative geometry-corrected envelope in

```text
|Delta v_pol|/c=12|c_gamma|M_geom/r^3
```

gives:

| system | corrected envelope | interpretation |
|---|---:|---|
| Earth | `2.78747e-7` | conditional weak-local CFF certificate |
| Sun | `7.12774e-8` | conditional weak-local CFF certificate |
| one-solar-mass white dwarf | `6.99719e-2` | linear but not precision-small |
| 1.4-solar-mass, 12-km neutron star | `1.94447e7` | outside linear transfer; no certificate |
| ten-solar-mass horizon | `9.31703e6` | outside linear transfer; no certificate |

The calculable parent, lepton, pointlike-hadron and charged-vector control
packet remains around `9.62e-31 m^2` and is negligible on every row. The large
historical envelope concerns the unmatched physical total. It cannot be used
to claim compact propagation control.

## 6. What is now established

```text
coefficient-sign label swap                    = proved;
physical pulse-splitting gate                  = two-sided;
legacy 6.0e6 m^2 bound                         = nonreproducible and superseded;
measured-orbit historical envelope             = derived;
Ricci and derivative exterior competitors      = removed at retained order;
extreme magnetic-vacuum competitor             = bounded negligible;
Earth/Sun CFF residual under historical gate   = below 1e-6;
primary polarization-resolved likelihood       = absent;
compact-object transfer                        = uncontrolled;
QCD TJJ matching                               = open.
```

This is a correction, not a defeat of the local GR branch. The metric,
Newtonian and no-fifth-force results of checkpoints 4942-4943 are unchanged.
What is weakened is only the previous empirical bound on the separate
curvature-photon operator.

## 7. Claim boundary

```text
primary-formula sign theorem                   = true;
primary-formula two-sided top-hat              = true;
source printed numeric bound                   = false;
geometry-corrected historical envelope         = true;
primary raw-data robust likelihood             = false;
conditional Earth/Sun CFF certificate          = true;
general local Maxwell promotion                = false;
complete physical CFF prediction               = false;
full MTS fixed point                           = false.
```

No coefficient is retuned between systems. No hadronic remainder is set to
zero. No compact result is inferred outside the linear domain.

## 8. Next target

`4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md`

Derive or rigorously bound the confined-QCD contribution to the Ricci-flat
`CFF` coefficient from the gravitational-current-current three-point
function, chiral spectral information and measured hadronic form factors.
Combine it with the already calculated lepton, scalar and charged-vector
packet. Promote a predictive weak-local Maxwell action only if the total
coefficient closes without the flawed pulsar number or a cancellation
assumption.

