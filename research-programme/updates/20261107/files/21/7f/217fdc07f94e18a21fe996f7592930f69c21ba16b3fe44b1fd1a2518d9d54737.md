# 5195 - Matched Joint CMB-Informed Parent Refit and Physical Sound-Horizon Gate

Private derivation and empirical robustness checkpoint. This is not an
official CMB likelihood and not a public MTS cosmology-support claim.

Checkpoint marker: `MTS_5195_MATCHED_JOINT_CMB_INFORMED_PARENT_REFIT`.

## 1. The calculation that 5194 required

Checkpoint 5194 found a real compressed-CMB discrepancy after freezing the
5193 late parameters and profiling only `H0`. Checkpoint 5195 does not write
that down as another missing target. It refits all five models under one
matched likelihood:

```text
Pantheon+ noncalibrator rows       = 1624, full STAT+SYS covariance;
DESI DR2 BAO rows                  = 13, full covariance;
primary SDSS/eBOSS growth rows     = 5 f sigma8 rows;
compressed CMB rows                = 4, full covariance;
total primary rows                 = 1646;
SH0ES/local-H0 calibration         = absent.
```

The primary growth score retains only the marginal `f sigma8` rows. This
avoids pretending that DESI DR2 and legacy SDSS/eBOSS BAO distance vectors
have a known zero cross-survey covariance. The 14-row SDSS BAO-plus vector is
still refitted as a labelled robustness branch.

## 2. One physical distance calibration

The independent BAO nuisance used in 5193 and 5194 is removed. CAMB
`1.6.6` computes `r_drag` from the fitted physical baryon and
cold-matter densities, and every DESI/SDSS distance uses

```text
alpha_phys = c/(H0 r_drag),
DM/rd = alpha_phys integral_0^z dz/E,
DH/rd = alpha_phys/E,
DV/rd = alpha_phys[z(integral_0^z dz/E)^2/E]^(1/3).
```

The only analytic nuisance coordinates are the Pantheon+ offset, `n_s` inside
the full compressed-CMB covariance, and `sigma8_0` when growth is present.
No independent `BAO alpha` remains.

## 3. Matched primary result

| model | SN chi2 | DESI chi2 | growth chi2 | CMB chi2 | total chi2 | AIC | BIC | edge |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `LCDM` | 1459.911146 | 12.013110 | 3.446589 | 1.844397 | 1477.215242 | 1489.215242 | 1521.651862 | `False` |
| `wCDM` | 1458.081506 | 11.336511 | 3.385655 | 3.151975 | 1475.955647 | 1489.955647 | 1527.798371 | `False` |
| `CPL` | 1456.461453 | 9.688985 | 3.278028 | 1.281761 | 1470.710226 | 1486.710226 | 1529.959054 | `False` |
| `ParentScalar_Lambda_free` | 1456.524426 | 10.457743 | 3.292389 | 3.703715 | 1473.978274 | 1489.978274 | 1533.227101 | `False` |
| `ParentScalar_Lambda_zero` | 1456.454432 | 10.651045 | 3.279027 | 3.684577 | 1474.069081 | 1488.069081 | 1525.911804 | `False` |

The physical calibration coordinates are:

| model | Omega_m | H0 | Omega_b h2 | r_drag Mpc | c/(H0 r_drag) | n_s | sigma8_0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `LCDM` | 0.30270678 | 68.40528 | 0.022509172 | 147.34623 | 29.743498 | 0.96952455 | 0.85634708 |
| `wCDM` | 0.3049614 | 68.026882 | 0.022554674 | 147.44576 | 29.888757 | 0.97083051 | 0.85883651 |
| `CPL` | 0.31023858 | 67.632659 | 0.022485273 | 147.29631 | 30.093478 | 0.96882286 | 0.85836667 |
| `ParentScalar_Lambda_free` | 0.30936656 | 67.492044 | 0.022573237 | 147.4846 | 30.117676 | 0.97129854 | 0.86104872 |
| `ParentScalar_Lambda_zero` | 0.31163541 | 67.242776 | 0.022563826 | 147.49585 | 30.227015 | 0.97128177 | 0.86151558 |

The lowest primary AIC is `CPL` and the lowest primary BIC is
`LCDM`. This statement is bookkeeping, not a claim that a
compressed distance prior is equivalent to the official Planck likelihood.

The frozen-parameter CMB values from 5194 were `42.5497` and `37.2861` for
the free- and zero-Lambda parents. After the matched refit they are
`3.70371` and
`3.68458`. The earlier pressure
is therefore absorbed without a prior edge, but only inside this compressed
diagnostic.

## 4. Like-for-like model comparisons

| parent | baseline | delta chi2 | delta AIC | delta BIC | parent edge |
|---|---|---:|---:|---:|---|
| `ParentScalar_Lambda_free` | `LCDM` | -3.23697 | 0.763032 | 11.5752 | `False` |
| `ParentScalar_Lambda_free` | `wCDM` | -1.97737 | 0.0226266 | 5.42873 | `False` |
| `ParentScalar_Lambda_free` | `CPL` | 3.26805 | 3.26805 | 3.26805 | `False` |
| `ParentScalar_Lambda_zero` | `LCDM` | -3.14616 | -1.14616 | 4.25994 | `False` |
| `ParentScalar_Lambda_zero` | `wCDM` | -1.88657 | -1.88657 | -1.88657 | `False` |
| `ParentScalar_Lambda_zero` | `CPL` | 3.35885 | 1.35885 | -4.04725 | `False` |

Negative differences favour the parent. Absolute information-criterion
differences below two are treated as draw-scale. The equal-count free-parent
versus CPL comparison gives

```text
delta AIC=3.26804719,
delta BIC=3.26804719.
```

The equal-count zero-Lambda-parent versus wCDM comparison gives

```text
delta AIC=-1.88656637,
delta BIC=-1.88656637.
```

Thus the zero-Lambda parent is the cleaner surviving parent candidate. It is
within
`1.35885` AIC units of the
lowest-AIC CPL fit, while its BIC is
`4.25994` above the
lowest-BIC LCDM fit. This is competitive/draw-scale under AIC and moderate
LCDM preference under BIC, not a universal model-selection victory.

Any comparison whose parent row hits a prior edge remains unstable evidence,
even if its raw information criterion is favourable.

## 5. Edge and identifiability audit

| primary model | edge coordinates |
|---|---|
| `LCDM` | none |
| `wCDM` | none |
| `CPL` | none |
| `ParentScalar_Lambda_free` | none |
| `ParentScalar_Lambda_zero` | none |

Parent models with an edge flag: `none`. The wide-mass
robustness branch below distinguishes a genuine finite optimum from a fit
that merely runs toward the LambdaCDM-like `mu -> 0` limit.

The fitted parent states are:

| parent | mu=m_gap/H0 | Omega_scalar,0 | Omega_Lambda,0 | theta_0 | w_dark,0 |
|---|---:|---:|---:|---:|---:|
| `ParentScalar_Lambda_free` | 1.2320991 | 0.20178091 | 0.48876253 | 0.34177506 | -0.9343517 |
| `ParentScalar_Lambda_zero` | 0.76386801 | 0.68827459 | 0 | 0.20609219 | -0.91624792 |

These are empirical coordinates of a parent-owned model, not a derivation of
the mass gap or homogeneous state.

The local finite-difference Hessian in prior-normalized coordinates gives:

| parent | min eigenvalue | condition | sigma(log10 mu) | sigma(f_scalar) | corr(log10 mu,f) | status |
|---|---:|---:|---:|---:|---:|---|
| `ParentScalar_Lambda_free` | 29.9254 | 102590 | 0.207972 | 0.249593 | -0.862012 | `POSITIVE_BUT_WEAK_LOCAL_CURVATURE` |
| `ParentScalar_Lambda_zero` | 925.351 | 3333.23 | 0.10953 |  |  | `POSITIVE_LOCAL_CURVATURE` |

Both optima have positive local curvature. The free-Lambda mass/state split
remains weak and correlated; the zero-Lambda branch is substantially cleaner.
These Gaussian curvature numbers are not posterior intervals.

## 6. Robustness matrix

| configuration | model | total chi2 | CMB chi2 | AIC | BIC | edge |
|---|---|---:|---:|---:|---:|---|
| `robustness_full_SDSS_wCDM_prior` | `LCDM` | 1488.780923 | 1.387572 | 1500.780923 | 1533.250261 | `False` |
| `robustness_full_SDSS_wCDM_prior` | `wCDM` | 1486.952939 | 2.839998 | 1500.952939 | 1538.833833 | `False` |
| `robustness_full_SDSS_wCDM_prior` | `CPL` | 1481.750325 | 0.930467 | 1497.750325 | 1541.042776 | `False` |
| `robustness_full_SDSS_wCDM_prior` | `ParentScalar_Lambda_free` | 1484.272904 | 3.289740 | 1500.272904 | 1543.565354 | `False` |
| `robustness_full_SDSS_wCDM_prior` | `ParentScalar_Lambda_zero` | 1484.119694 | 3.285355 | 1498.119694 | 1536.000588 | `False` |
| `robustness_fs8_LCDM_prior` | `LCDM` | 1477.812648 | 2.469363 | 1489.812648 | 1522.249268 | `False` |
| `robustness_fs8_LCDM_prior` | `wCDM` | 1476.753546 | 3.922294 | 1490.753546 | 1528.596270 | `False` |
| `robustness_fs8_LCDM_prior` | `CPL` | 1470.588340 | 1.155067 | 1486.588340 | 1529.837167 | `False` |
| `robustness_fs8_LCDM_prior` | `ParentScalar_Lambda_free` | 1474.852716 | 4.588510 | 1490.852716 | 1534.101543 | `False` |
| `robustness_fs8_LCDM_prior` | `ParentScalar_Lambda_zero` | 1474.907082 | 4.249599 | 1488.907082 | 1526.749805 | `False` |
| `robustness_no_growth_wCDM_prior` | `LCDM` | 1473.768322 | 1.841967 | 1483.768322 | 1510.783627 | `False` |
| `robustness_no_growth_wCDM_prior` | `wCDM` | 1472.568947 | 3.128636 | 1484.568947 | 1516.987313 | `False` |
| `robustness_no_growth_wCDM_prior` | `CPL` | 1467.432198 | 1.281761 | 1481.432198 | 1519.253626 | `False` |
| `robustness_no_growth_wCDM_prior` | `ParentScalar_Lambda_free` | 1470.685884 | 3.703715 | 1484.685884 | 1522.507312 | `False` |
| `robustness_no_growth_wCDM_prior` | `ParentScalar_Lambda_zero` | 1470.789124 | 3.683488 | 1482.789124 | 1515.207490 | `False` |
| `robustness_parent_wide_mass` | `ParentScalar_Lambda_free` | 1473.978274 | 3.703715 | 1489.978274 | 1533.227101 | `False` |
| `robustness_parent_wide_mass` | `ParentScalar_Lambda_zero` | 1474.068350 | 3.683634 | 1488.068350 | 1525.911073 | `False` |

The matrix includes the full 14-row SDSS BAO-plus vector, the alternative
LCDM compressed-prior table, a no-growth refit, and a parent-only mass prior
extended to `log10(mu)=-4`. The full-SDSS row is explicitly nonclaim because
the unavailable DESI/SDSS cross-survey covariance is not fabricated.

## 7. Exact forward-parent validation

Optimization uses the fast regular phase shoot at `N=-7`. Each primary parent
optimum is then rebuilt from the `N=-12` radiation-era regular series and
rescored:

| parent | max relative E difference | delta total chi2 | delta CMB chi2 | fluid-PPF delta l_A | max constraint |
|---|---:|---:|---:|---:|---:|
| `ParentScalar_Lambda_free` | 6.946e-06 | 1.303e-03 | 1.913e-07 | -3.957e-07 | 2.220e-15 |
| `ParentScalar_Lambda_zero` | 6.945e-06 | 1.318e-03 | 1.122e-07 | -3.740e-07 | 2.220e-15 |

This verifies that the optimization shortcut did not create the result. The
fluid-versus-PPF column is a numerical implementation comparator; PPF is not
substituted for the canonical parent derivation.

The fixed-grid growth integrator used during optimization is independently
compared with the checkpoint-5194 high-accuracy DOP853 solution at every
observed growth redshift. Its largest fractional difference across all five
primary best fits is

```text
3.133077e-06.
```

## 8. Interpretation ceiling

The compressed vector is model-dependent. The wCDM table is used identically
for all primary rows, and the LCDM table is a robustness rerun. That is a fair
internal pressure test, but it cannot establish an official CMB pass or
failure for a new dynamic field.

```text
physical H0-r_drag calibration        = implemented;
all five models jointly refitted      = yes;
same covariance and nuisance rules    = yes;
independent BAO scale                  = removed;
parent forward regular branch checked = yes;
official Planck/ACT/SPT likelihood    = no;
cosmology-support claim               = false;
full MTS unification claim            = false.
```

The next physics decision follows the actual fit. An interior competitive
parent branch earns an official-likelihood-ready implementation. An
edge-driven `mu -> 0` or `f_scalar -> 0` result does not: it sends the work
back to deriving the parent mass/state selection law and calibrated source
coupling before spending an official-likelihood run on an unselected branch.
Either way, the current cosmology discrepancy has now been calculated rather
than circulated as an unsigned target.

This result is the interior case. The next cosmology gate is therefore an
official-likelihood-ready implementation. The higher-priority field-theory
target remains derivation of the finite `m_gap/H0` and homogeneous-state
selection from the parent `J_gap`/source-coupling structure; the fitted values
cannot be promoted as fundamental constants until that derivation exists.

## 9. Machine artifacts

- `source-intake/functional_rg/5195/likelihood_contract.csv`
- `source-intake/functional_rg/5195/joint_fit_summary.csv`
- `source-intake/functional_rg/5195/joint_fit_parameters.csv`
- `source-intake/functional_rg/5195/prior_edge_audit.csv`
- `source-intake/functional_rg/5195/model_comparisons.csv`
- `source-intake/functional_rg/5195/physical_sound_horizon_calibration.csv`
- `source-intake/functional_rg/5195/compressed_CMB_predictions.csv`
- `source-intake/functional_rg/5195/growth_residuals.csv`
- `source-intake/functional_rg/5195/growth_integrator_validation.csv`
- `source-intake/functional_rg/5195/parent_forward_validation.csv`
- `source-intake/functional_rg/5195/parent_state_summary.csv`
- `source-intake/functional_rg/5195/parent_local_identifiability.csv`
- `source-intake/functional_rg/5195/source_provenance.csv`
- `source-intake/functional_rg/5195/joint_CMB_informed_refit_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5195_VALIDATION.csv`

Total optimizer runtime recorded across the fit matrix is
`1092.277` seconds.
