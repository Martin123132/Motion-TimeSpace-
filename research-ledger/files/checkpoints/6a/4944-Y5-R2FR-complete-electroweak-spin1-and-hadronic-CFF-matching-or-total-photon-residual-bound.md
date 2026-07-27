# 4944 - Visible CFF thresholds and total photon residual bound

Marker: `MTS_VISIBLE_CFF_THRESHOLD_TOTAL_RESIDUAL_BOUND_4944`.

Date: `2026-07-13`.

Status: private analytic, source-acquired and source-executed checkpoint. The
free-lepton threshold is retained, the scalar-QED coefficient is translated
into pointlike charged-pion and charged-kaon anchors, and the complete
dimension-six heat-kernel monomial set is used to derive a conservative
charged-`W` envelope. Confined QCD is not replaced by a free-current-quark
sum and its local remainder is not set to zero. Instead, an exact triangle
bound transfers the existing two-sided secondary PSR recast onto the complete
infrared `CFF` coefficient and every unmatched threshold. The total bound is
then projected onto the same five local systems as checkpoint 4942. This
constructs a real conditional photon-residual bound without pretending that
the exact signed `W` coefficient, hadronic `TJJ` matching or a primary robust
two-sided likelihood has been completed.

## 1. Convention and decomposition

Keep the checkpoint-4931 convention

```text
L_EM=-F_mn F^mn/4+c_gamma C_mnrs F^mn F^rs.
```

Below all charged thresholds,

```text
c_gamma^IR
 =c_gamma^parent
  +c_gamma^leptons
  +c_gamma^W
  +c_gamma^QCD
  +c_gamma^other.
```

Every term uses one field normalization and curvature convention. No term is
allowed to cancel another unless an explicit signed calculation supplies that
cancellation.

The completed parent envelope and free-lepton subtotal are

```text
|c_gamma^parent|=7.92263868782e-72 m^2,

c_gamma^(e+mu+tau)=-9.62179442357e-31 m^2.
```

The electron remains overwhelmingly dominant among the elementary Dirac
thresholds.

## 2. Scalar-QED threshold and hadronic anchors

The locked scalar Drummond-Hathrell action gives, in the adopted convention,

```text
Delta c_gamma^(scalar)
 =+Q^2 alpha_EM/(720pi) (hbar/(mc))^2.
```

Its magnitude is half the Dirac coefficient and its relative sign is
opposite. Using the 2025 PDG masses gives

```text
charged pion pointlike anchor
  =+6.44865665329e-36 m^2,

charged kaon pointlike anchor
  =+5.15430497960e-37 m^2.
```

The pion anchor is `6.70e-6` of the electron magnitude. These rows are useful
signed low-mass controls, not complete QCD matching. Current `u,d,s` masses
are not inserted into a free `1/m_q^2` formula below confinement.

Curved chiral EFT contains additional non-minimal curvature operators and
low-energy constants. The acquired 2026 source establishes that general
counterterm fact; it does not by itself calculate the pure-photon `CFF`
low-energy constant. Therefore

```text
c_gamma^QCD
 =c_pi-loop+c_K-loop+c_QCD,local+heavier spectral terms
```

is kept as a matching identity. `c_QCD,local` is neither erased nor tuned.

## 3. Charged-W heat-kernel envelope

In background-field Feynman gauge, the charged massive gauge block can be
organized as

```text
Delta_1
 =-D^2 delta+m_W^2 delta+R+2ieF,

Gamma_W=Tr ln Delta_1-Tr ln Delta_0.
```

The second term is the net Goldstone/ghost subtraction for the charged pair.
On the Ricci-flat `CFF` projection, the complete dimension-six bosonic UOLEA
contains the relevant monomials

```text
Riemann Omega^2,
(D.Omega)^2,
(D Omega)^2,
U box U,
U Omega^2,
Omega^3,
U^3.
```

A term-by-term absolute trace and two-form derivative-reduction audit gives

```text
K_raw
 =5/180
  +5(1/90+1/360)4
  +(1/12)4x4
  +1/3
 =1.97222222222.
```

`Omega^3` has no one-spin-curvature/two-photon trace because the Lorentz
curvature generator is traceless; `U^3` contains no curvature. Scalar and
Ricci terms vanish on the declared projection. Taking

```text
K_W=10>5 K_raw
```

therefore leaves a factor-five algebraic safety margin and yields

```text
|c_gamma^W|
 <=K_W alpha_EM/(4pi)(hbar/(m_W c))^2
 =3.50065341376e-38 m^2.
```

This is less than `3.64e-8` of the electron coefficient. It is a conservative
complete-dimension-six envelope, not an exact signed electroweak matching
coefficient. Thus the `W` threshold cannot threaten the local hierarchy even
though its sign remains open.

## 4. Calculable control interval

Combining the parent, free leptons, the `W` envelope and pointlike pion/kaon
anchors gives

```text
-9.62172513276331e-31
 <=c_gamma^control
 <=-9.62172443263263e-31 m^2,

|c_gamma^control|
 <=9.62172513276331e-31 m^2.
```

This interval is not the physical total because the hadronic local remainder
has not been calculated. It is the complete source-executed control packet
available at this checkpoint.

## 5. Total and unmatched-remainder bound

Checkpoint 4931 records the secondary two-sided recast of the legacy
PSR B1534+12 result,

```text
sqrt(|c_gamma^IR|)<2.45 km,

|c_gamma^IR|<=B_PSR=6.0025e6 m^2.
```

This row is model conditional and not a reconstructed primary likelihood. It
does, however, act on the complete infrared coefficient. Define

```text
c_unmatched=c_gamma^IR-c_gamma^control.
```

Then the triangle inequality gives exactly

```text
|c_unmatched|
 <=B_PSR+|c_gamma^control|.
```

Numerically the added control term is invisible at the printed precision, so
the conditional unmatched-threshold envelope is `6.0025e6 m^2`. This binds
the hadronic and any other residual jointly without assuming either is zero
and without relying on a cancellation.

## 6. Five-system residual projection

For the 4942 Ricci-flat geometric-optics transfer,

```text
|Delta v_pol|/c
 =12|c_gamma|M_geom/r^3.
```

The calculable control and conditional total envelopes are

| system | calculable control | conditional complete-total bound |
|---|---:|---:|
| Earth | `1.98020e-52` | `1.23535e-15` |
| Sun | `5.06351e-53` | `3.15886e-16` |
| one-solar-mass white dwarf | `4.97077e-47` | `3.10101e-10` |
| 1.4-solar-mass, 12-km neutron star | `1.38134e-38` | `8.61750e-2` |
| ten-solar-mass horizon | `6.61877e-39` | `4.12911e-2` |

All conditional rows remain below the declared ten-percent linear-control
gate. The compact rows are not tiny enough to promote a precision compact
Maxwell theorem from this conditional bound. The solar-system rows are
extremely small, but `CFF` birefringence is a distinct radial/polarization
effect and is not relabeled as a constant PPN `gamma`.

## 7. What is now established

```text
free-lepton CFF subtotal                       = calculated;
scalar-QED CFF coefficient                    = calculated;
pointlike pion and kaon anchors               = calculated;
free-current-quark infrared sum               = rejected;
charged-W complete dimension-six envelope     = derived;
charged-W exact signed coefficient            = open;
hadronic local CFF matching                   = open and not set zero;
conditional complete-total CFF bound          = constructed;
conditional unmatched-remainder bound         = constructed;
five-system total residual vector             = calculated;
arena-specific coefficient retuning           = absent.
```

The main advance is not another missing-input ledger: the unresolved split
matching is bypassed by a bound on the complete coefficient, and that bound is
propagated to actual local residuals.

## 8. Claim boundary

```text
elementary and pointlike control packet        = derived;
electroweak spin-1 magnitude safety            = derived by envelope;
exact signed W threshold                       = false;
first-principles QCD TJJ coefficient           = false;
QCD remainder assumed zero                     = false;
primary robust two-sided CFF likelihood        = false;
complete physical CFF prediction               = false;
conditional total photon residual bound       = true;
local Maxwell promotion                        = false;
full MTS fixed point                           = false.
```

The `2.45 km` bound must always carry its secondary and model-conditional
label. It cannot be converted into a parent prediction or a general Maxwell
pass.

## 9. Next target

`4945-Y5-R2FR-primary-two-sided-CFF-likelihood-or-QCD-TJJ-dispersion-bound-and-local-Maxwell-certificate.md`

Attempt one of two genuine upgrades. First preference: reconstruct a primary
two-polarization PSR likelihood with both signs and competing operators. If
the required timing/polarization data are unavailable, derive a dispersive or
chiral bound on the hadronic `TJJ` coefficient using measured electromagnetic
and gravitational form factors. Promote a local Maxwell certificate only if
one route replaces the conditional secondary bound without retuning the
coefficient between systems.

No GitHub action is authorized.
