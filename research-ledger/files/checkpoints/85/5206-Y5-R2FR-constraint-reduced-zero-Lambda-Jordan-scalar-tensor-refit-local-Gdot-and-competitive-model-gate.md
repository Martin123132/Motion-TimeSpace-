# 5206 - Constraint-Reduced Zero-Lambda Jordan Scalar-Tensor Refit, Local Gdot and Competitive-Model Gate

Private derivation and empirical robustness checkpoint. This remains an
internal compressed-CMB calculation, not an official cosmology or full-MTS
claim.

Checkpoint marker: `MTS_5206_CONSTRAINT_REDUCED_SCALAR_TENSOR_REFIT`.

## Executive result

This checkpoint performs the calculation requested by checkpoint 5205 rather
than restating it. The same checkpoint-5203 Jordan action is reduced to

```text
F/M_R^2=1+zeta_c phi^2,
Z=1,
V=M_R^2 m_gap^2 phi^2/2,
Lambda_cal=0.
```

The regular radiation mode is imposed at `N=-18`; its singular partner is
excluded. The sole homogeneous amplitude is then shot until the exact
Hamiltonian constraint gives `E(0)=1`. No scalar fraction or present phase is
fitted. The fitted coordinates are therefore

```text
Omega_m, log10(m_gap/H0), H0, Omega_b h^2, zeta_c,
```

with `n_s` and `sigma8_0` analytically profiled as in checkpoint 5195.

The exact `zeta_c=0` rebuild changes the locked 5195 total cosmology score by
only

```text
-2.7453097573e-09.
```

That is the compatibility gate: the scalar-tensor implementation reduces
numerically to the already tested minimal parent rather than replacing it
with a new closure.

## 1. Derived FLRW system

With `q=dphi/dN`, `h=d ln H/dN` and `mu=m_gap/H0`, the Hamiltonian equation is

```text
E^2[f+f_N-q^2/6]
 =Omega_m exp(-3N)+Omega_r exp(-4N)+mu^2 phi^2/6.
```

The scalar equation is

```text
q_N=-(3+h)q-mu^2 phi/E^2+6 zeta_c phi(2+h).
```

Eliminating `q_N` from the independent spatial metric equation gives the
closed Raychaudhuri expression recorded in
`source-intake/functional_rg/5206/Jordan_FLRW_equations.csv`. SymPy returns

```text
Raychaudhuri substitution residual = 0,
scalar substitution residual       = 0.
```

The numerical constraint, `d ln E/dN` identity, positive-`F` condition and
Einstein-frame kinetic sign are checked independently.

## 2. State selection is now constraint-reduced

The regular boundary condition is

```text
q_i/phi_i
 =(3/2) zeta_c (Omega_m/Omega_r) a_i
  -mu^2 a_i^4/(5 Omega_r)
  +O(r_i^2,a_i^5).
```

At `N=-18` the explicit remainder bound is below the validation tolerance.
Changing the initial surface to `N=-16` changes the observable background by
less than the recorded start-sensitivity limit. Flatness determines the
initial second moment/amplitude at every likelihood evaluation. Thus the
zero-Lambda parent no longer carries the old fitted `f_scalar` or a fitted
phase.

This is conditional on the declared `Lambda_cal=0` branch. It does not derive
the absolute vacuum-energy origin.

## 3. Physical sound horizon and growth

CAMB supplies standard recombination redshifts and the physical-density
microphysics. The runner then recomputes the sound-horizon integrals using
the scalar-tensor `E(N)` and rescales the CAMB `r_drag` and `r_star`. This
avoids representing the nonminimal background as an invented positive dark
fluid. The small residual approximation is that the recombination redshifts
are held fixed; the maximum pre-recombination `H` shift is reported.

For the five primary `f sigma8` rows the subhorizon equation uses the derived
long-range scalar-tensor coupling

```text
G_eff/G_bare
 =[(2f+4f_phi^2)/(2f+3f_phi^2)]/f.
```

At the lowest observed scale, `k=0.01 h/Mpc`, the omitted Yukawa range
correction is below the machine-recorded `10^-3` gate. A second score
normalizes `G_eff` to its present Cavendish value; its growth-chi-squared
shift is recorded rather than hidden.

## 4. Direct local likelihood

The refitted state predicts both local rows:

```text
gamma-1=-2 alpha_0^2/(1+alpha_0^2),
Gdot/G=H0 q0 d_phi ln G_cav.
```

The runner scores the published Gaussian anchors used by checkpoint 5204:

```text
Cassini gamma-1=(2.1 +/- 2.3)e-5,
LLR Gdot/G=(-5.0 +/- 9.6)e-15 yr^-1.
```

This is stronger and cleaner than imposing a frozen `zeta_c` ceiling from the
old state: every likelihood evaluation recomputes `phi0`, `q0`, `gamma` and
`Gdot`.

## 5. Joint refit

| scalar-tensor model | cosmology chi2 | local chi2 | joint chi2 | joint AIC | joint BIC | zeta_c | edge |
|---|---:|---:|---:|---:|---:|---:|---|
| `ParentST_Lambda_zero_signed_zeta` | 1474.194051 | 0.879281 | 1475.073332 | 1491.073332 | 1534.331873 | -1.99251067e-05 | `False` |
| `ParentST_Lambda_zero_positive_zeta` | 1474.068284 | 1.104916 | 1475.173199 | 1491.173199 | 1534.431741 | 0 | `True` |

The signed result has

```text
phi0=2.600392406,
q0=-0.4164797851,
gamma-1=-1.073983451e-08,
Gdot/G=-2.968523689e-15 yr^-1,
G_cav/G_bare=1.000134758.
```

The positive-only branch has `zeta_c=0` and differs
from the locked minimal parent by

```text
Delta AIC_joint=1.99920292,
Delta BIC_joint=7.40652063.
```

An edge-hitting positive-only result is not called evidence for a nonzero
coupling.

## 6. Locked comparators

| model | cosmology chi2 | local chi2 | joint chi2 | joint AIC | joint BIC |
|---|---:|---:|---:|---:|---:|
| `LCDM` | 1477.215242 | 1.104916 | 1478.320158 | 1490.320158 | 1522.764064 |
| `wCDM` | 1475.955647 | 1.104916 | 1477.060563 | 1491.060563 | 1528.911787 |
| `CPL` | 1470.710226 | 1.104916 | 1471.815142 | 1487.815142 | 1531.073684 |
| `ParentScalar_Lambda_zero_minimal_locked` | 1474.069081 | 1.104916 | 1475.173996 | 1489.173996 | 1527.025220 |

For the signed scalar-tensor branch:

```text
versus minimal zero-Lambda parent:
  Delta AIC_joint=1.89933518,
  Delta BIC_joint=7.30665289;

versus LCDM:
  Delta AIC_joint=0.753173956,
  Delta BIC_joint=11.5678094;

versus CPL:
  Delta AIC_joint=3.25818944,
  Delta BIC_joint=3.25818944.
```

Negative differences favour the scalar-tensor model; absolute differences
below two are draw-scale. The compressed-CMB caveat remains exactly the same
as checkpoint 5195.

## 7. Decision

```text
full Jordan FLRW equations solved                 = yes;
regular phase derived, not fitted                 = yes;
homogeneous amplitude fixed by flatness           = yes;
finite zeta scored against Cassini and LLR        = yes;
scalar-tensor subhorizon growth inserted          = yes;
physical sound-horizon response inserted          = yes;
regular/numerical validation                      = true;
growth approximation validation                   = true;
signed local two-sigma envelopes                   = true;
absolute Lambda_cal=0 origin derived              = no;
common F_R,V,Z,X2 RG trajectory selected          = no;
official CMB likelihood                           = no;
cosmology-support claim                           = false;
full MTS claim                                    = false.
```

Selected next route:

```text
DERIVE_COMMON_F_R_V_Z_X2_TRAJECTORY_AND_PRESENT_G_SOURCE_NORMALIZATION.
```

If the finite coupling is not selected after its parameter penalty, the
result is still constructive: the local-GR corridor and the competitive
minimal cosmology are now connected by one explicitly solved Jordan system,
and the remaining problem is coefficient selection rather than a missing
background equation.

## 8. Evidence products

- `source-intake/functional_rg/5206/Jordan_FLRW_equations.csv`
- `source-intake/functional_rg/5206/regular_shoot_validation.csv`
- `source-intake/functional_rg/5206/locked_comparator_summary.csv`
- `source-intake/functional_rg/5206/scalar_tensor_fit_summary.csv`
- `source-intake/functional_rg/5206/scalar_tensor_fit_parameters.csv`
- `source-intake/functional_rg/5206/local_PPN_Gdot_likelihood.csv`
- `source-intake/functional_rg/5206/growth_effective_G_validation.csv`
- `source-intake/functional_rg/5206/zeta_profile.csv`
- `source-intake/functional_rg/5206/model_comparisons.csv`
- `source-intake/functional_rg/5206/background_samples.csv`
- `source-intake/functional_rg/5206/source_provenance.csv`
- `source-intake/functional_rg/5206/constraint_reduced_scalar_tensor_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5206_VALIDATION.csv`
