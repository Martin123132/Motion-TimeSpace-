# 4926 - Known massive thresholds and motion-scale normalization

Marker: `MTS_KNOWN_THRESHOLD_MOTION_SCALE_4926`.

**Decision:** the calculable low-energy threshold sector is now assembled
without a free-quark sum, and the old motion-scale formula has been repaired
dimensionally rather than copied into the canonical action. The result is a
real reduction of the open problem:

1. every source-locked colorless Standard-Model threshold is negligible by at
   least about `97` coefficient orders relative to the neutron-star
   one-percent target;
2. every individual mode heavy enough for the declared local expansion is
   automatically compact-safe by about `80` coefficient orders even at the
   lowest allowed mass;
3. the printed MTS `lambda` has mass dimension `3`, not the canonical
   `8/3`; a unique dimensional repair introduces one mass normalization
   `M_N` and gives an exact one-parameter scale family;
4. a minimal one-scale benchmark places the motion pole at the Planck scale
   and its Weyl-cubic threshold about `159` coefficient orders below the
   compact target, but the dimensionless normalization is not promoted;
5. all unresolved ultraviolet, QCD and nonpromoted MTS matching still appears
   as the same **one signed** low-energy coefficient `a_IR`.

The calculable thresholds are therefore no longer a missing box. They cannot
close compact GR because the finite ultraviolet Wilson boundary and the exact
interacting QCD matching moment remain open.

No compact-GR, full MTS-to-GR or public theory claim is opened.

## 1. Source-locked spectrum

The checkpoint locks three durable inputs under SHA-256:

- the official 2026 PDG SQLite database;
- NuFIT 6.0 v2;
- the heavy-field gravity calculation used for the spin ratios.

The PDG database is queried through its official Python API. The values used
in the threshold calculation are

| field | mass | counting | `r_i` |
|---|---:|---|---:|
| electron | `0.51099895069 MeV` | one Dirac field | `-4` |
| muon | `105.6583755 MeV` | one Dirac field | `-4` |
| tau | `1.776932465 GeV` | one Dirac field | `-4` |
| `W+/-` | `80.3625 GeV` | one complex Proca, two real vectors | `+6` |
| `Z` | `91.1878733 GeV` | one real Proca | `+3` |
| Higgs | `125.130944 GeV` | one real scalar | `+1` |

For every massive mode with `Q << m`, checkpoint 4925 gives

```text
Delta zeta_i=r_i/[30240(4pi)^2 m_i^2],

Delta a_i
 =16piG Delta zeta_i
 =r_i l_P^2 (hbar c/m_i)^2/(30240pi).
```

The signed non-neutrino colorless sum is

```text
a_e+mu+tau+W+Z+H=-1.640178869062048e-99 m^4,
abs(a)^(1/4)=2.012439361341142e-25 m.
```

The electron dominates this subtotal. The signs have been retained; absolute
values were not silently added.

## 2. Neutrino scenarios, not a false absolute-mass claim

NuFIT 6.0 supplies the benchmark splittings

```text
Delta m21^2 = 7.49e-5 eV^2,
Delta m3l^2 = +2.534e-3 eV^2  (normal),
Delta m3l^2 = -2.510e-3 eV^2  (inverted).
```

Oscillations do not fix the lightest mass or whether each massive state is
Dirac or Majorana. Four explicit lightest-zero scenarios are therefore used.
One Majorana determinant is counted as half a Dirac determinant, so its ratio
is `-2` rather than `-4`.

| scenario | positive masses (eV) | `abs(a_nu)^(1/4)` |
|---|---|---:|
| normal Majorana | `0.00865448, 0.0503389` | `1.30983e-21 m` |
| normal Dirac | `0.00865448, 0.0503389` | `1.55766e-21 m` |
| inverted Majorana | `0.0493467, 0.0500999` | `6.45162e-22 m` |
| inverted Dirac | `0.0493467, 0.0500999` | `7.67231e-22 m` |

The exactly massless eigenstate is not inserted into `1/m^2`. It remains in
the nonlocal metric form factor. The largest complete colorless benchmark is
the normal-Dirac row,

```text
abs(a_visible)^(1/4)=1.557659434600340e-21 m,
abs(a_visible)/ell_NS^4=4.044516337887705e-98.
```

Thus the hierarchy and Dirac/Majorana uncertainty cannot threaten the selected
compact domain in any displayed benchmark.

## 3. Exact locality-envelope theorem

The local expansion itself supplies a stronger guard. For one Dirac field,

```text
abs(a_D(m))
 =4 l_P^2(hbar c/m)^2/(30240pi)
```

decreases monotonically with `m`. Therefore, for a declared local threshold
`m >= zeta Q`, its largest possible coefficient is obtained at `m=zeta Q`.

For the GW250114 reference scale

```text
Q_GW=1.931429329341656e-12 eV,
zeta=10,

abs(a_D)^(1/4)<=3.273337966535713e-17 m,
abs(a_D)/ell_NS^4<=7.887510411996691e-81.
```

This is a per-field theorem. A finite multiplicity scales the coefficient
linearly and its length only as the fourth root. It does not bound a genuinely
massless nonlocal form factor or an arbitrary infinite tower.

## 4. QCD firewall without free-quark double counting

No free `u,d,s` threshold is legitimate below confinement. Adding perturbative
heavy-quark rows while retaining an all-QCD infrared block would also double
count unless a complete scale-by-scale subtraction were specified. The
checkpoint therefore treats the entire colored sector as one renormalized
matching block.

The source-locked neutral-pion mass defines only a normalization unit,

```text
a_QCD^R=C_QCD a_pi_unit,

a_pi_unit
 =l_P^2(hbar c/m_pi0)^2/(30240pi)
 =5.876822985279802e-105 m^4.
```

Saturating the neutron-star one-percent target would require

```text
abs(C_QCD)=2.476742382711873e118.
```

This is a powerful naturalness firewall, not a zero theorem. The Weyl-cubic
coefficient is a three-stress matching moment and no positive two-point
spectral bound on `C_QCD` has been derived. The exact QCD contribution remains
inside `a_IR` rather than being set to one or zero.

## 5. The printed motion scale fails a canonical dimension check

In four natural-unit dimensions a canonical scalar has

```text
[psi]=1,
[g_psi |psi|^(4/3)]=4,
[g_psi]=8/3,
mu=g_psi^(3/8).
```

The original formulas instead give

```text
gamma=Phi_G M_Pl,
lambda_old=Phi_G^3 M_Pl^2 gamma=Phi_G^4 M_Pl^3,

[gamma]=1,
[lambda_old]=3.
```

Consequently `lambda_old` cannot be substituted directly for the canonical
`g_psi`. That old identification is dimensionally rejected.

The repair can be derived exactly. Let the old field have mass dimension
`Delta`. Requiring its kinetic and fractional-potential terms to have the same
dimension gives

```text
2+2Delta=3+(4/3)Delta,
Delta=3/2.
```

Both terms then have dimension five, so the action needs one inverse-mass
normalization:

```text
S_old
 =1/M_N integral d4x [
      1/2 (partial phi_old)^2
     +3/4 lambda_old |phi_old|^(4/3)].
```

With

```text
psi=phi_old/sqrt(M_N),
```

the canonical coupling and physical scale are

```text
g_psi=lambda_old M_N^(-1/3),
mu=g_psi^(3/8)
  =lambda_old^(3/8) M_N^(-1/8).
```

The same dimension assignment makes `gamma phi_old partial_t phi_old`
homogeneous, but it does not revive damping: for constant `gamma` that term is
a boundary term, and the closed bath remains the valid damping owner.

## 6. Exact one-parameter normalization family

Write the required normalization as

```text
M_N=C_N M_Pl,
```

where `C_N>0`. The repaired old formulas imply

```text
g_psi
 =Phi_G^4 C_N^(-1/3) M_Pl^(8/3),

mu
 =Phi_G^(3/2) C_N^(-1/8) M_Pl,

m_gap
 =c_m Phi_G^(3/2) C_N^(-1/8) M_Pl.
```

This is stronger than saying “the scale is missing”: its complete dependence
on the missing normalization is now known, and it enters only through an
eighth root.

The minimal no-second-scale benchmark `C_N=1` gives

```text
M_Pl             =1.220890128583896e28 eV,
mu                =2.512800690133141e28 eV,
m_gap central     =2.566294935950309e28 eV,
ell_motion        =6.349828232642897e-37 m per real pole,
a_motion/ell_NS^4 =1.116926163776280e-159.
```

The conservative low-`c_m` profile gives

```text
ell_motion=7.521920618201166e-37 m.
```

Neither row promotes `C_N=1` or the lattice pilot. They quantify the exact
consequence of the minimal branch.

For one real pole, the compact scale floor becomes

```text
C_N < 4.27399341872e634.
```

For `N_real` equal poles this upper bound scales as `N_real^(-4)`. Equivalently,
in the canonical parameterization

```text
g_psi=C_psi M_Pl^(8/3),
```

one pole needs only

```text
C_psi>1.960375552989088e-211,
```

with `C_psi,min` scaling as `N_real^(4/3)`. This does not derive the physical
normalization; it proves that almost the entire positive normalization space is
already compact-safe for the motion threshold alone.

## 7. One-Wilson infrared collapse

At the GW reference scale the honest decomposition is

```text
a_IR
 =a_unresolved^R
  +a_visible
  +a_motion(C_N,c_m,N_real)
  +Delta a_GS,

a_unresolved^R
 =a_UV,H^R+a_QCD^R+a_MTS,res^R.
```

The three labels inside `a_unresolved^R` describe microscopic provenance, not
three independently observable low-energy parameters. A local ringdown or
compact observable sees their renormalized sum.

Across the four neutrino rows the known offset is only

```text
5.90e-104 to 1.00e-102
```

of the current conservative GW coefficient envelope. Subtracting it produces
the same displayed interval to all practical precision. The low-energy test
theory therefore still has exactly one signed `a_IR`, with no species- or
arena-specific closure functions.

## 8. Gate result

```text
PDG/NuFIT/heavy-field sources            = checksum locked;
colorless massive thresholds             = calculated;
massless fields                           = retained as nonlocal;
free-quark infrared sum                   = rejected;
QCD coefficient                           = one interacting block, open;
old lambda -> canonical g identification  = rejected dimensionally;
motion normalization family               = derived exactly;
C_N=1                                     = conditional benchmark only;
known thresholds below compact target     = derived;
independent low-energy I1 test parameters  = one;
weak invariant-vacuum GR                  = retained;
compact vacuum/matter GR                  = not promoted;
full MTS-to-GR                             = not promoted.
```

The next derivation must attack the remaining normalization rather than circle
it. The old covariance metric relation contains an unnormalized gradient
bilinear. The direct target is therefore

`4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md`.

It must try to fix `C_N` by matching the canonical motion stress residue and
the coefficient of the metric-covariance map to the already selected Einstein
residue. If that coefficient is only another field convention, the result must
prove the redundancy and leave `a_IR` as the single empirical input.

No GitHub action is authorized.

## Sources

- `post-checkpoint-work/source-intake/particle_data/4926/PROVENANCE.md`.
- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`.
- `post-checkpoint-work/4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md`.
- `post-checkpoint-work/4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md`.
- `post-checkpoint-work/4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md`.
- `post-checkpoint-work/4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md`.
- `post-checkpoint-work/scripts/Y5_R2FR_4926_known_threshold_spectrum_motion_scale.py`.
