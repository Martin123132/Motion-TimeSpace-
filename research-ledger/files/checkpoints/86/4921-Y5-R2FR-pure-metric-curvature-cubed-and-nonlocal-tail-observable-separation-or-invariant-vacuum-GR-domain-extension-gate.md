# 4921 - Pure-metric curvature-cubed observable and nonlocal-tail separation

**SUPERSEDED BY CHECKPOINT 4922.** The algebra below remains a valid declared
Burger--Emond--Moynihan `lambda beta1` probe benchmark, but it is not the
invariant bound on the corpus parity-even Weyl-cubic packet `zeta_+`. On a
smooth four-dimensional Ricci-flat background,

```text
zeta_+ = lambda(beta2+beta1/2),
```

whereas the displayed `r^-6` probe potential depends only on `lambda beta1`.
The counterexample `beta1=0`, `beta2!=0` proves that the old `L3` coordinate
cannot determine `zeta_+`. Consequently the Galileo, Cassini and Mercury
numbers below are historical `beta1`-route benchmarks only and must not be
used as active total-`C^3` bounds. Checkpoint 4922 replaces the active map by
`ell_+^4=abs(16 pi G_N zeta_+)`, the pure-`I1` static solution, and the direct
GW170608 posterior. The nonlocal-class separation and fixed-metric Maxwell
statement survive this correction.

**Historical status:** This checkpoint repaired the curvature-only proxy but
then over-identified one basis coordinate with the full invariant cubic
coefficient. It is retained for auditability, not as the current certificate.

Marker: `MTS_C3_NONLOCAL_OBSERVABLE_DOMAIN_GATE_4921`.

## 1. Operator and coefficient ownership

Use the on-shell operational parity-even cubic basis employed by Burger,
Emond and Moynihan,

```text
S = integral sqrt(-g) [R/(16 pi G_N) + d3 I3 + ...].
```

Only the coefficient combination `d3` entering their nonrotating exterior
potential is used here. Define the observable length

```text
L3^4 = 144 pi G_N abs(d3).
```

This definition prevents a comparison between differently normalised `c6`,
`lambda beta1` and Weyl-cubic symbols. The complete renormalized owner is

```text
d3_total(mu)
  = d3_finite(mu)
  + d3_GS_running(mu)
  + d3_massive_threshold(mu).
```

Three statements must remain separate:

1. the Goroff-Sagnotti pole fixes a universal two-loop running residue;
2. massive thresholds can generate finite local `1/m^2` terms; and
3. neither statement fixes the arbitrary finite renormalization condition.

Checkpoint 4914 retained `Gamma_MTS,res=0` after the attempted interacting
TTT extraction failed its promotion gates. That is a selected renormalization
branch with no promoted residual. It is not a theorem that `d3_total=0` at
every scale. Massless modes remain in nonlocal logarithmic form factors and
must not be converted into divergent local `1/m^2` coefficients.

## 2. Exact weak Schwarzschild transfer

The source-backed nonrotating potential is

```text
Phi(r) = G_N M/r - 288 pi G_N^3 d3 M^2/r^6.
```

With `r_s=2G_N M/c^2` and the magnitude definition above,

```text
delta Phi = -L3^4 r_s^2/(2r^6),
abs(delta Phi/Phi_N) = L3^4 r_s/r^5,
abs(delta a/a_N)     = 6 L3^4 r_s/r^5.
```

The acceleration factor six is essential: the observable must be obtained by
differentiating the `r^-6` potential, not by inserting the Kretschmann scalar
into an action-density ratio.

For equal weak metric potentials, direct line-of-sight integration gives

```text
integral[-infinity,infinity] dz/(b^2+z^2)^4 = 5 pi/(16 b^7),

abs(delta alpha/alpha_GR) = (15 pi/16)L3^4 r_s/b^5,
abs(delta gamma)          = (15 pi/8)L3^4 r_s/b^5.
```

The corresponding static clock and Kepler-orbit maps are

```text
abs(alpha_clock)
  = L3^4 r_s abs(r1^-6-r2^-6)/abs(r1^-1-r2^-1),

abs(Delta varpi)
  = 30 pi L3^4 r_s/[a^5(1-e^2)^5]
    (1 + 3e^2/2 + e^4/8)
```

per orbit. The pericentre result follows from the first-order Gauss equation
and the exact integral of `cos(f)(1+e cos(f))^5`.

These corrections are not constant shifts of the PPN parameters. They are
higher-radial-power residuals that can be reported as experiment-specific
equivalent `delta gamma`, clock or orbit anomalies.

## 3. Current simple local envelopes

The existing primary anchors are processed one at a time. No covariance,
joint likelihood, cancellation or official cubic-gravity analysis is
invented.

| arena | observable tolerance | private `L3` upper envelope |
|---|---:|---:|
| Galileo eccentric-satellite redshift | `abs(alpha_clock)<2.48e-5` | `6.9276471e7 m` |
| Cassini solar conjunction | `abs(delta gamma)<2.3e-5` | `1.2260080e9 m` |
| MESSENGER Mercury perihelion | `0.0015 arcsec/century` | `2.3603965e9 m` |

The selected conservative local envelope is therefore

```text
L3 < 6.92765e7 m
```

from the Galileo clock projection. At that value the independently projected
Cassini equivalent residual is `2.34476e-10`, and the Mercury residual is
`1.29960e-17 rad/orbit`.

The Eot-Wash R10 Yukawa `alpha(lambda)` curve is **not** reused. A local
`r^-6` force must be integrated over the actual patterned extended sources;
the `52 micrometre` minimum gap alone is not an observable bound. R10 remains
an explicit geometry-calculation target rather than a fabricated constraint.

## 4. Strong-curvature control

For generic curvature, the field-equation power-counting ratio is

```text
epsilon_K = 16 pi G_N abs(d3) K = L3^4 K/9.
```

This is the correct use of a curvature invariant: it controls the local EFT
expansion, but it is not itself the weak observable transfer. For a
Schwarzschild geometry,

```text
K = 12 r_s^2/r^6,
epsilon_K(r_s) = (4/3)(L3/r_s)^4.
```

Requiring `epsilon_K<0.01` gives the following background-domain caps:

| system | `L3` cap for one-percent control |
|---|---:|
| Earth surface | `5.0247e10 m` |
| Sun surface | `9.9367e10 m` |
| one-solar-mass, `7000 km` white dwarf | `1.0029e8 m` |
| `1.4 M_sun`, `12 km` neutron star | `6.0161e3 m` |
| `10 M_sun` Schwarzschild horizon | `8.6912e3 m` |

The local clock envelope controls Earth, Sun and the white-dwarf benchmark,
but it is roughly four orders of magnitude too weak to certify neutron-star
or black-hole curvature. Those kilometre-scale values are domain-of-validity
requirements, not observational limits.

## 5. Universal pure-gravity running

In the convention

```text
Gamma_div^(2)
 = [209/(2880(4 pi)^4)] (kappa^2/epsilon)
   integral sqrt(-g) I3,
kappa^2 = 32 pi G_N,
```

the pole residue fixes the logarithmic running but not the finite `d3` value.
For one unit of logarithm,

```text
L3_GS
 = [18(209/2880)/pi^2]^(1/4) l_P
 = 0.603159 l_P
 = 9.74858e-36 m.
```

Even an illustrative `abs(log)=100` gives `L3=3.08277e-35 m` and
`epsilon_K=1.58e-156` at a ten-solar-mass Schwarzschild horizon. This proves
that the universal running residue is harmless in every present arena. It
does not prove that UV finite matching is zero.

## 6. Local and nonlocal terms are not merged

The pure-metric ledger contains physically distinct classes:

| class | source/state scope | leading radial image |
|---|---|---|
| local `R^2,C^2` | selected four-dimensional Einstein branch | exact background zero or contact |
| quadratic nonlocal logarithms | eternal source-free Schwarzschild at calculated order | no background correction |
| massless-loop material/scattering amplitude | material source or scattering state | `r^-3` quantum tail |
| local `I3` | nonlinear vacuum exterior | `r^-6` potential |

Calmet and El-Menoufi's no-correction result for eternal Schwarzschild through
quadratic curvature order does not erase the source-dependent `r^-3` quantum
potential used in checkpoint 4878. Conversely, neither nonlocal result erases
the local `r^-6` cubic correction. Different radial powers and source/state
definitions cannot be silently cancelled.

## 7. Maxwell and the Poynting vector

Pure `I3` contains no electromagnetic field tensor. Therefore, at fixed
metric, it changes neither the Maxwell action nor the conserved current. Its
first and second variations around flat space vanish, so it introduces no
linear photon pole, vacuum birefringence or direct Poynting-vector
renormalization.

The electromagnetic Hilbert tensor, including its energy flux, remains a
source of the public metric. Cubic gravity can therefore feed back on an
electromagnetic configuration through the nonlinear corrected geometry. A
direct `R F^2` or `R_mn F^ma F^n_a` effect belongs to the separately tracked
mixed-curvature operator class, not to pure `I3`.

## 8. Domain decision

The checkpoint-4880 exact result is now stated with its correct scope:

```text
EH + local R2 + local C2:
    selected Einstein vacuum backgrounds remain exact;

EH + local R2 + local C2 + nonzero C3:
    Schwarzschild/Kerr are generally deformed at nonlinear order.
```

Decision:

```text
weak C3 observable transfer          = derived;
simple local one-parameter envelope  = L3 < 6.92765e7 m;
R10 C3 projection                    = blocked pending apparatus geometry;
universal two-loop running           = Planck-scale and harmless;
finite renormalized C3 matching      = not derived;
weak invariant-vacuum GR certificate = retained with explicit C3 clause;
compact-vacuum exact-GR extension    = not promoted;
full MTS-to-GR                       = false.
```

The next non-circular step is a direct strong-field cubic-curvature bound
from waveform, tidal/Love or ringdown observables. That test must constrain
the same declared `L3` coefficient rather than introducing another closure
symbol.

## 9. Reproducible artifacts

- `scripts/Y5_R2FR_4921_C3_nonlocal_observable_domain.py`
- `scripts/Y5_R2FR_4921_C3_nonlocal_observable_domain_validation.py`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_COEFFICIENT_OWNERSHIP.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_WEAK_FIELD_TRANSFER.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_LOCAL_ARENA_BOUNDS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_STRONG_DOMAIN.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_GOROFF_SAGNOTTI_RUNNING.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_NONLOCAL_SEPARATION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_MAXWELL_PROJECTION.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_4921_GATE_DECISION.csv`

No GitHub action or public claim is authorized by this checkpoint.
