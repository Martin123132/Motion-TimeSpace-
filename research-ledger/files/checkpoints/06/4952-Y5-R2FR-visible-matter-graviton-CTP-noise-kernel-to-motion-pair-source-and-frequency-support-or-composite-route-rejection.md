# 4952 - Visible-matter/graviton CTP pair source and spectral-support decision

Date: 2026-07-13

Marker: `MTS_VISIBLE_MATTER_GRAVITON_CTP_PAIR_SOURCE_SUPPORT_4952`.

Status: private analytic, primary-source-acquired, source-executed and
data-executed checkpoint. This is the full non-equilibrium source calculation
selected at 4951, not another missing-input ledger. The unchanged parent does
contain a conserved visible-matter-to-motion-pair channel at order `kappa^4`
in its rate. The channel nevertheless does not derive the late-time galaxy
state: ground-state and stationary sources have zero positive-energy emission,
DC Poynting flux does not evade that result, and smooth galactic harmonics do
not directly populate motion modes at the observed radial scale. Formation
transients or a derived kinetic cascade remain open. The 4947 stationary
`psi=0` local GR/Newton/Maxwell branch is retained.

## 1. Parent normalization and pair vertex

Use canonical weak-field normalization and signature `(+---)`:

```text
g_mn=eta_mn+kappa h_mn,
kappa^2=32 pi G_N,
S_int=(kappa/2) int h_mn T^mn.
```

For the regular local motion branch, `m_psi^2=m_gap^2/Z0`, the vacuum-to-pair
stress matrix element is

```text
V^mn(p,pprime)
 =Z0[p^m pprime^n+p^n pprime^m
     -eta^mn(p.pprime+m_psi^2)].
```

With `q=p+pprime` and `p^2=pprime^2=m_psi^2`, direct contraction gives

```text
q_m V^mn=0.
```

The pair vertex is therefore safe between conserved sources. In de Donder
gauge only

```text
P_mnrs=(eta_mr eta_ns+eta_ms eta_nr-eta_mn eta_rs)/2
```

survives; gauge-dependent longitudinal terms vanish. The `C^2 X` portal does
not add a one-graviton pair vertex around flat `psi=0`, because

```text
C=O(kappa h),
C^2 X=O(kappa^2 h^2 psi^2).
```

This calculation uses the pair vertex already present in the unchanged parent
and does not reinsert the rejected static `xi R psi^2` route.

## 2. Matter noise through the graviton

For visible-matter stress fluctuations

```text
t_m^mn=T_m^mn-<T_m^mn>,
N_m^mnrs(x,y)=<{t_m^mn(x),t_m^rs(y)}> /2,
```

the linear retarded metric response is

```text
h_ind=(kappa/2)D_R t_m.
```

Consequently the induced graviton Hadamard/noise kernel is

```text
N_h^ind=(kappa^2/4)D_R N_m D_A.
```

Coupling this metric to the motion stress and integrating the Gaussian metric
fluctuation gives the exact quadratic difference-field noise term

```text
Im S_IF^psi
 =(kappa^4/32)
   T_psi^- D_R N_m D_A T_psi^-.
```

The corresponding exchange amplitude and rate kernel are

```text
A_(m->psipsi)
 =(kappa^2/4) T_m^mn D_mnrs V^rs,

dGamma
 =(kappa^4/16)(1/2!) dPi_p dPi_pprime
   [V P S_m^em(q) P V]/|q^2+i0|^2.
```

The `1/2!` is displayed separately for identical final quanta. Overall delta
functions and state normalization follow the declared invariant phase-space
convention. The important result is not a fitted coefficient: the parent
supplies one universal order-`kappa^4` rate channel.

## 3. Symmetrized noise is not emission

The Hu-Verdaguer noise kernel is a symmetrized correlator. Real pair creation
uses the unsymmetrized bath-emission spectrum. Define it without a Fourier-sign
ambiguity by its spectral sum:

```text
S_m^em(q)
 =2 pi sum_(i,f) p_i
  <i|t_m|f><f|t_m|i>
  delta(q0-E_i+E_f) delta3(q-P_i+P_f),
q0>0.
```

For an exact stationary ground state, `E_f>=E_0`, so

```text
S_m^em(q0>0)=0.
```

Vacuum stress noise can remain nonzero while the vacuum remains stable. It
produces fluctuations and vacuum polarization, not a populated motion state.
For a thermal stationary bath, detailed balance instead gives

```text
S_em(omega)
 =exp[-hbar omega/(k_B T)] S_abs(omega),
omega>0.
```

Thus neither the symmetrized kernel nor its zero-point part may be inserted as
an occupation source.

## 4. Exact support and profile thresholds

Two on-shell motion quanta obey

```text
q=p+pprime,
q^2>=4m_psi^2,
omega^2>=c^2 Q^2+4 omega_gap^2,
omega_gap=c/lambda_c.
```

For a source of radius `R`, angular frequency `Omega=v/R` and temporal
harmonic `n`, three distinct necessary thresholds are useful.

At total spatial momentum `Q=1/R`,

```text
n_Q >=(c/v)sqrt[1+4(R/lambda_c)^2].
```

To create at least one mode with `k>=1/R`, allowing the partner to be at rest,

```text
n_1 >=(R/v)
       [sqrt((c/R)^2+omega_gap^2)+omega_gap].
```

To create two modes each capable of resolving the radial scale,

```text
n_2 >=2(c/v)sqrt[1+(R/lambda_c)^2].
```

For a massless field, a low harmonic has

```text
k_max R<=n v/c,
lambda_min/R>=2 pi c/(n v).
```

A low harmonic may create extremely long-wavelength massless pairs; it cannot
be renamed as direct occupation of the measured galactic radial profile. A
subsequent cascade is a separate kinetic derivation.

## 5. Public galaxy execution

The locked read-only `MTS-Galaxy-Lab-` sample contains 175 outer LTG rows.
For every galaxy the script deliberately uses

```text
Omega=v_outer/R_outer,
```

which is a generous upper frequency proxy rather than a fitted pattern speed.
Four Compton cases were evaluated: massless, 100 kpc, 10 kpc and 1 kpc.

For the massless case:

```text
n_1 minimum/median/maximum = 901 / 3007 / 16843,
n_2 minimum/median/maximum = 1801 / 6014 / 33685.
```

The easiest two-profile row is `UGC02487`; the hardest is `UGC07577`. None of
the 175 rows can populate two outer-scale modes with smooth harmonics `n<=4`.
Finite mass only raises the thresholds. These are support calculations, not a
pair-rate amplitude fit and not a new galaxy likelihood.

## 6. Sourced compact-object comparison

Kilic et al. give for `J2211+1136`

```text
P=70.32 s,
M=1.268 M_sun,
log10(g/[cm s^-2])=9.214.
```

The sourced values imply

```text
R=sqrt(GM/g)=3.2064318e6 m,
v/c=9.55658e-4,
n_1=1047,
n_2=2093
```

on the massless branch. Hessels et al. give `716 Hz` and `R<16 km` for
`PSR J1748-2446ad`. Using the 16 km upper limit deliberately minimizes the
harmonic thresholds:

```text
v/c=0.2401000,
n_1=5,
n_2=9.
```

Frequency support therefore does not provide a galaxy-only environmental
selector. The white-dwarf requirement is comparable to the easiest galaxies,
and a fast neutron star reaches its own radial scale at far lower harmonics.
This does not claim either object actually emits motion pairs: the appropriate
stress emission spectrum and amplitude still have to be calculated. It does
prove that a broad universal high-frequency source cannot be declared locally
silent from frequency arguments alone.

## 7. Poynting vector and waves

The Poynting vector was included rather than ignored.

```text
stationary T_EM^0i:
  nonzero momentum flow but omega=0
  -> stationary metric/frame dragging
  -> zero positive-energy pair source;

periodic EM stress:
  DC plus sum/difference harmonics
  -> pair source allowed only on timelike emission support;

high-frequency radiation or plasma noise:
  sufficient microscopic frequency may exist
  -> directly creates short-scale modes
  -> galaxy-scale occupation requires a derived cascade/transport law.
```

Checkpoint 4947 fixes one Maxwell stress and one graviton residue. There is
no independent Poynting coupling available for galaxy tuning or local
suppression.

## 8. Decision

```text
parent h-psi-psi vertex                         = derived;
pair-vertex Ward identity                      = exact;
matter-induced graviton noise                  = derived;
motion influence-noise coefficient             = kappa^4/32;
matter-to-pair rate kernel                     = derived at kappa^4/16;
symmetrized vacuum noise as particle source    = false;
stationary matter or DC Poynting source        = exact zero;
two-particle timelike support                  = derived;
175-galaxy direct n<=4 profile support         = zero;
frequency support as galaxy-only selector      = false;
late-time smooth CTP direct galaxy route       = rejected;
formation transient or derived kinetic cascade = open;
4947 local GR/Newton/Maxwell branch             = retained;
full MTS galaxy unification                     = false.
```

This is a route rejection after constructing the source and executing its
support, not a report that a coefficient is missing. The surviving
non-equilibrium possibility must derive both injection and redistribution.

## 9. Artifacts

- `post-checkpoint-work/scripts/Y5_R2FR_4952_visible_matter_graviton_CTP_pair_source_gate.py`
- `post-checkpoint-work/scripts/Y5_R2FR_4952_visible_matter_graviton_CTP_pair_source_validation.py`
- `post-checkpoint-work/source-intake/functional_rg/4952/PROVENANCE.md`
- `post-checkpoint-work/source-intake/functional_rg/4952/visible_matter_graviton_CTP_pair_source_results.json`
- `post-checkpoint-work/source-intake/functional_rg/4952/parent_hpsipsi_vertex_and_CTP_chain.csv`
- `post-checkpoint-work/source-intake/functional_rg/4952/emission_spectrum_and_support_theorem.csv`
- `post-checkpoint-work/source-intake/functional_rg/4952/SPARC_outer_harmonic_support_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4952/local_compact_rotator_harmonic_support_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4952/Poynting_and_wave_source_gate.csv`
- `post-checkpoint-work/source-intake/functional_rg/4952/CTP_pair_source_route_decision.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4952_VALIDATION.csv`

## Next target

`4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md`

Reconstruct a physically bounded galaxy-formation stress spectrum, insert it
into the derived 4952 emission kernel, and derive the `X2` collision integral
and redistribution time. The route survives only if one universal parent
coefficient can produce the required macroscopic galaxy occupation within a
formation time while remaining below white-dwarf, neutron-star and local
energy-injection bounds. Do not insert an initial occupation, cascade rate or
environmental switch.
