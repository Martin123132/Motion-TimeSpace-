# 5194 - Parent Canonical-Scalar Perturbation, Growth, and Compressed-CMB Gate

Private derivation and empirical gate. This is not a public cosmology-support
claim.

Checkpoint marker: `MTS_5194_PARENT_CANONICAL_SCALAR_PERTURBATION_GROWTH_CMB`.

## 1. What changed

Checkpoint 5193 fitted the parent homogeneous scalar but deliberately did not
promote the old smooth-growth proxy. This checkpoint varies the same surviving
low-energy parent action to linear order. The perturbation owner is therefore
no longer missing:

```text
S_O2 = integral sqrt(-g) [
  Mpl^2 (R - 2 Lambda)/2
  - (partial psi)^2/2
  - m_gap^2 psi^2/2
] + S_m[g,Psi].
```

It fixes, rather than fits,

```text
Box psi - m_gap^2 psi = 0,
c_s,rf^2 = 1,
Pi_psi^i_j|TF = 0,
nabla_mu T_m^{mu nu} = 0.
```

Thus matter remains metric-geodesic, the scalar has no direct fifth force, and
the scalar contributes no intrinsic linear gravitational slip. Standard
photon/neutrino anisotropic stress is not relabelled as an MTS effect.

## 2. Exact linear scalar equations

With

```text
ds^2=a^2[-(1+2 Psi)deta^2+(1-2 Phi)dx^2],
psi=psi_bar+delta_psi,
```

the parent Klein-Gordon equation gives

```text
delta_psi'' + 2 Hc delta_psi'
+ (k^2+a^2 m_gap^2) delta_psi
- psi_bar'(Psi'+3 Phi')
+ 2 a^2 m_gap^2 psi_bar Psi = 0.
```

The scalar stress perturbations are

```text
delta rho_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  + m_gap^2 psi_bar delta_psi,

delta p_psi =
  (psi_bar' delta_psi' - psi_bar'^2 Psi)/a^2
  - m_gap^2 psi_bar delta_psi,

delta q_psi = -psi_bar' delta_psi/a^2,
Pi_psi = 0.
```

The high-k quadratic action has equal positive time- and space-gradient
coefficients. Therefore the scalar is ghost-free at this order and its
rest-frame sound speed is exactly one. The free-`Lambda` branch can be treated
as one conserved fluid because adding a cosmological constant changes neither
the total momentum nor rest-frame perturbations:

```text
rho_D=rho_psi+rho_Lambda,
p_D=p_psi-rho_Lambda,
1+w_D=dot(psi)^2/rho_D,
c_s,rf^2=1.
```

## 3. Stable early branch

The 5193 backward solution is excellent to `N=-5`, but extending a backwards
shoot to CMB times can amplify its numerically decaying mode. Checkpoint 5194
therefore starts at `N=-12` with the regular radiation-era series

```text
x_i = -(mu/E_i)^2 chi_i / 5
```

and integrates forward, solving `E(0)=1` for `chi_i`. It reproduces the 5193
present branch:

| branch | `mu` | `chi(-12)` | present `theta` | max Friedmann residual |
|---|---:|---:|---:|---:|
| `ParentScalar_Lambda_free` | 1.79759020906 | 0.293207517124 | 0.523064034594 | 2.220e-15 |
| `ParentScalar_Lambda_zero` | 0.880675983364 | 1.02643171042 | 0.238814110897 | 2.109e-15 |

No closure activation function is used.

## 4. Real SDSS/eBOSS growth test

The primary test uses the source-locked SDSS/eBOSS DR16 `BAO-plus` vectors and
their full per-sample covariance blocks. It contains 14 rows, including five
`f sigma8` measurements. For every model the same two nuisances are solved
analytically in one generalized least-squares system:

```text
alpha_RSD = c/(H0 r_d),
sigma8_0.
```

The smooth subhorizon equation is now the derived canonical-scalar limit,
not a declaration:

```text
D_NN + [2 + d ln H/dN] D_N - 3 Omega_m D/2
  = O[(aH/k)^2].
```

| model | primary chi2 | `alpha_RSD` | `sigma8_0` | combined AIC | combined BIC |
|---|---:|---:|---:|---:|---:|
| `LCDM` | 14.2525133 | 29.9425306 | 0.878171222 | 1494.81527 | 1521.86095 |
| `wCDM` | 11.6284895 | 30.3665244 | 0.897973255 | 1489.05191 | 1521.50672 |
| `CPL` | 12.3051954 | 30.4081439 | 0.887393616 | 1491.3979 | 1529.26186 |
| `ParentScalar_Lambda_free` | 11.891023 | 30.3965583 | 0.892154201 | 1490.99352 | 1528.85747 |
| `ParentScalar_Lambda_zero` | 12.0904028 | 30.4016316 | 0.890773855 | 1489.22111 | 1521.67593 |

The combined columns add this independent primary SDSS/eBOSS compression to
the checkpoint-5193 Pantheon+ and DESI DR2 score. The alternative
`Full-shape-only` compression is a robustness branch and is not double-counted.

Every model is subjected to the same leave-one-sample-out calculation:

| excluded sample | parent-free minus wCDM chi2 | parent-free minus LCDM chi2 |
|---|---:|---:|
| `BOSS_DR12_LRG` | 0.191851 | -1.9698 |
| `MGS` | 0.250053 | -1.63934 |
| `eBOSS_DR16_LRG` | 0.163707 | -2.02189 |
| `eBOSS_DR16_QSO` | 0.126907 | -0.603925 |

All four reruns keep both profiled nuisances interior. Across these matched
jackknifes the free parent differs from wCDM by
`[0.126907, 0.250053]` in chi2 and from
LCDM by `[-2.02189, -0.603925]`. This is a
fair baseline stress test: no failure rule is applied only to MTS.

| parent | baseline | delta growth chi2 | delta combined AIC | delta combined BIC |
|---|---|---:|---:|---:|
| `ParentScalar_Lambda_free` | `LCDM` | -2.36149 | -3.82175 | 6.99652 |
| `ParentScalar_Lambda_free` | `wCDM` | 0.262533 | 1.94161 | 7.35075 |
| `ParentScalar_Lambda_free` | `CPL` | -0.414172 | -0.404383 | -0.404383 |
| `ParentScalar_Lambda_zero` | `LCDM` | -2.16211 | -5.59416 | -0.185021 |
| `ParentScalar_Lambda_zero` | `wCDM` | 0.461913 | 0.169208 | 0.169208 |
| `ParentScalar_Lambda_zero` | `CPL` | -0.214793 | -2.17679 | -7.58592 |

Negative differences favour the parent row. Absolute information-criterion
differences below about two are treated as draw-scale, not as a knockout.

## 5. Full linear-transfer check

CAMB `1.6.6` evolves the tabulated parent `w(a)` with
`c_s^2=1`. A forward regular background removes the false early kinetic mode
that appeared when a finite-precision backwards solution was extrapolated.
The fluid integrator uses only a numerical floor
`1+w >= 0.0001` where the dark fraction is early and negligible.
An exact-table PPF comparator changes normalized `f sigma8` by at most

```text
3.285962e-07.
```

Across the tested RSD redshifts, the largest mismatch between the
parent-to-LCDM growth response from CAMB and from the derived subhorizon
equation is

```text
5.436604e-05.
```

The largest CAMB difference between total transfer density with and without
dark-energy perturbations on `k >= 0.01 h/Mpc` is

```text
3.094851e-04.
```

This is a measured transfer diagnostic, not a hand-inserted suppression
factor.

## 6. Compressed CMB gate

The source-locked Planck-2018 distance-prior vector and full covariance are
used only as a conditional diagnostic. `Omega_m` and the late branch stay at
their 5193 values; `Omega_b h^2` and `n_s` are held at the prior means; only
`H0` is profiled. No Planck, ACT, or SPT official likelihood is run.

| model | profiled `H0` | compressed chi2 | `R` | `l_A` | fixed-`A_s` sigma8 |
|---|---:|---:|---:|---:|---:|
| `LCDM` | 68.226921 | 3.8895001 | 1.7439461 | 301.42073 | 0.80725065 |
| `wCDM` | 67.532519 | 86.502287 | 1.7240515 | 301.26746 | 0.75791063 |
| `CPL` | 67.513722 | 20.636317 | 1.7369679 | 301.36696 | 0.78730065 |
| `ParentScalar_Lambda_free` | 67.518538 | 42.54972 | 1.731592 | 301.32552 | 0.77502834 |
| `ParentScalar_Lambda_zero` | 67.505584 | 37.28613 | 1.7327234 | 301.33426 | 0.77741439 |

CAMB spectra through `ell=800` and transfer functions are finite for
both parent branches. Their spectra residuals are machine outputs for the next
likelihood step, not support evidence.

The compressed diagnostic is adverse to the parent late-only fits:
LCDM gives chi2
`3.8895`,
whereas the free-`Lambda` and zero-`Lambda` parent branches give
`42.5497`
and
`37.2861`.
This is not an official rejection because the late parameters are frozen and
only `H0` is refitted, but it is real pressure. The next CMB pass must refit
every baseline and parent branch under the same CMB information rather than
explaining this discrepancy away.

## 7. O4 handoff

The largest checkpoint-5193 homogeneous `delta_F` is multiplied by the
deliberately conservative `[(k c)/H0]^4` envelope at
`k=0.3 Mpc^-1`. The result is

```text
2.667100e-230.
```

It remains negligible on this low-energy branch. This does not replace the
all-scale UV-completion boundary.

## 8. Decision

```text
canonical scalar perturbation owner       = derived at O2;
no-ghost principal sign                   = passed;
rest-frame sound speed                    = c_s^2=1 exactly;
intrinsic scalar anisotropic stress       = zero exactly;
direct scalar force on matter             = absent by minimal coupling;
forward regular CMB-time background       = constructed and 5193-matched;
SDSS/eBOSS full-covariance growth test     = executed;
CAMB linear transfer/spectra smoke        = executed;
official CMB likelihood                   = not run;
mass-gap value from parent                = not derived;
homogeneous state selection from parent   = not derived;
full MTS cosmology/unification claim      = false.
```

The correct next target is an official-likelihood-ready parent scalar module
or a parent selection law for `m_gap/H0` and the homogeneous state. The growth
perturbation gap itself is no longer merely listed as missing.

## 9. Machine artifacts

- `source-intake/functional_rg/5194/perturbation_contract.csv`
- `source-intake/functional_rg/5194/parent_scalar_forward_background.csv`
- `source-intake/functional_rg/5194/parent_forward_diagnostics.csv`
- `source-intake/functional_rg/5194/growth_data_schema.csv`
- `source-intake/functional_rg/5194/growth_fit_summary.csv`
- `source-intake/functional_rg/5194/growth_residuals.csv`
- `source-intake/functional_rg/5194/growth_jackknife.csv`
- `source-intake/functional_rg/5194/growth_baseline_comparison.csv`
- `source-intake/functional_rg/5194/combined_SN_DESI_SDSS_scores.csv`
- `source-intake/functional_rg/5194/compressed_CMB_profile.csv`
- `source-intake/functional_rg/5194/CAMB_branch_summary.csv`
- `source-intake/functional_rg/5194/CAMB_fluid_PPF_convergence.csv`
- `source-intake/functional_rg/5194/CAMB_vs_smooth_growth.csv`
- `source-intake/functional_rg/5194/CAMB_dark_energy_clustering.csv`
- `source-intake/functional_rg/5194/CAMB_spectra_residual_summary.csv`
- `source-intake/functional_rg/5194/O4_perturbation_envelope.csv`
- `source-intake/functional_rg/5194/source_provenance.csv`
- `source-intake/functional_rg/5194/parent_scalar_perturbation_growth_CMB_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5194_VALIDATION.csv`
