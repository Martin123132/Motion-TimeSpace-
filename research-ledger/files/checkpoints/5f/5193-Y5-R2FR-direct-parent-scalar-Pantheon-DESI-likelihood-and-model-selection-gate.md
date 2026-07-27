# 5193 - Direct parent-scalar Pantheon+/DESI likelihood and model-selection gate

Marker: `MTS_5193_DIRECT_PARENT_SCALAR_SN_BAO_LIKELIHOOD`

**Verdict:** checkpoint 5192 has been converted into a direct data model. The
parent scalar was not approximated by the rejected `p=3,u=1/4` closure. Its
regular homogeneous mode was solved at every likelihood evaluation and scored
on exactly the same 1,624 Pantheon+ shape rows and 13 DESI DR2 BAO rows as the
fitted baselines, with the same full covariance matrices and the same two
profiled nuisance parameters.

The numerical result remains nonclaim. The action owns the universal mass
coordinate and the homogeneous equations; it does not select the fitted mass
or state amplitude.

## 1. Matched likelihood contract

```text
Pantheon+ rows                 = 1624 non-calibrators;
Pantheon+ covariance           = full STAT+SYS;
SN nuisance                    = one analytic additive offset;
DESI DR2 BAO rows              = 13;
DESI DR2 covariance            = full Gaussian covariance;
BAO nuisance                   = one analytic common scale alpha;
local-H0/SH0ES calibration     = absent;
fixed radiation density        = Omega_r=9e-05;
total scored points            = 1637.
```

The four data hashes match the historical no-SH0ES run. All models use the
same selected rows, covariances, integration grid, and nuisance profiling.

## 2. Parent-scalar parameterization

Define

```text
x=dot(psi_c)/(sqrt(6) M_R H),
y=m_gap psi_c/(sqrt(6) M_R H),
mu=m_gap/H0.
```

At `N=0`, flatness is imposed exactly:

```text
Omega_psi,0=f_scalar(1-Omega_m-Omega_r),
Omega_Lambda=(1-f_scalar)(1-Omega_m-Omega_r),
x_0=-sqrt(Omega_psi,0) sin(theta),
y_0= sqrt(Omega_psi,0) cos(theta).
```

The backward autonomous system is

```text
x'=-(3+h)x-(mu/E)y,
y'=(mu/E)x-hy,
(ln E)'=h,
h=-3Omega_m(N)/2-2Omega_r(N)-3x^2.
```

`theta` is not fitted. It is shot uniquely onto the regular frozen mode
`x(N_reg)=0` at every likelihood evaluation. The free-`Lambda` model therefore
has three shape parameters:

```text
Omega_m, log10(mu), f_scalar.
```

The `Lambda=0` ablation fixes `f_scalar=1` and has two shape parameters.
The SN offset and BAO scale are counted for every model.

## 3. Fitted scores

```text
LCDM                            chi2=1470.562757549 k=3 AIC=1476.562757549 BIC=1492.764619281 edge=False
wCDM                            chi2=1465.423415643 k=4 AIC=1473.423415643 BIC=1495.025897952 edge=False
CPL                             chi2=1465.092704776 k=5 AIC=1475.092704776 BIC=1502.095807663 edge=False
M6_fixed                        chi2=1465.259900462 k=3 AIC=1471.259900462 BIC=1487.461762194 edge=False
M6_fitted                       chi2=1465.259376497 k=4 AIC=1473.259376497 BIC=1494.861858807 edge=False
ParentScalar_Lambda_free        chi2=1465.102494153 k=5 AIC=1475.102494153 BIC=1502.105597040 edge=False
ParentScalar_Lambda_zero        chi2=1465.130710710 k=4 AIC=1473.130710710 BIC=1494.733193019 edge=False
ParentScalar_narrow_prior       chi2=1465.102490821 k=5 AIC=1475.102490821 BIC=1502.105593708 edge=False
ParentScalar_N7                 chi2=1465.102490735 k=5 AIC=1475.102490735 BIC=1502.105593622 edge=False
```

The lowest primary AIC is `M6_fixed`. The lowest primary BIC is
`M6_fixed`. Information criteria are reported rather than turned
into a binary victory claim.

`M6_fixed` is retained only as the historical empirical closure comparator:
checkpoint 5192 rejects its identity with the source-free parent scalar.
Restricting the comparison to standard baselines and direct parent-owned
models, the lowest AIC is `ParentScalar_Lambda_zero` and the lowest BIC is
`LCDM`. Their disagreement is part of the result, not something to average
away.

Direct comparisons:

```text
ParentScalar_Lambda_free minus LCDM: Delta chi2=-5.4602634, Delta AIC=-1.4602634, Delta BIC=9.34097776
ParentScalar_Lambda_free minus wCDM: Delta chi2=-0.32092149, Delta AIC=1.67907851, Delta BIC=7.07969909
ParentScalar_Lambda_free minus CPL: Delta chi2=0.00978937692, Delta AIC=0.00978937692, Delta BIC=0.00978937692
ParentScalar_Lambda_zero minus LCDM: Delta chi2=-5.43204684, Delta AIC=-3.43204684, Delta BIC=1.96857374
ParentScalar_Lambda_zero minus wCDM: Delta chi2=-0.292704933, Delta AIC=-0.292704933, Delta BIC=-0.292704933
ParentScalar_Lambda_zero minus CPL: Delta chi2=0.0380059331, Delta AIC=-1.96199407, Delta BIC=-7.36261464
```

## 4. Parent best-fit branch

```text
Omega_m       = 0.302295098208018,
mu=m_gap/H0   = 1.79759020906334,
f_scalar      = 0.200600672417876,
Omega_Lambda  = 0.55767288340378,
theta         = 0.523064034367258,
chi_initial   = 0.293207312395323,
early x       = 3.4558607588095e-09,
max constraint residual
              = 1.11022302462516e-15.
```

These fitted numbers are not a derivation of `J_gap` or the cosmological
state. They are the data-preferred coordinates inside the parent-owned model
family under the declared priors.

## 5. Robustness branches

```text
free Lambda broad prior:
  chi2=1465.10249415,
  edge=False;

Lambda=0 ablation:
  chi2=1465.13071071,
  Delta chi2=0.0282165562317,
  edge=False;

narrow parent prior:
  chi2=1465.10249082,
  Delta chi2=-3.33257139573e-06,
  edge=False;

regular surface N=-7:
  chi2=1465.10249074,
  Delta chi2=-3.41822237715e-06,
  edge=False.
```

Any prior-edge branch remains unstable evidence even if its raw chi-squared
is low.

## 6. Identifiability and physical reading

The broad free-`Lambda` minimum is interior, but an interior point is not the
same thing as a well-measured parameter split. A direct finite-difference
Hessian gives

```text
minimum eigenvalue = 0.571453041489006,
maximum eigenvalue = 31463.2644234443,
condition number   = 55058.3549987975,
corr(log10(mu),f_scalar)
                   = -0.997948547124753,
status             = WEAK_MASS_STATE_SPLIT.
```

Thus the background constrains a combined thaw history much more strongly
than it separately measures the universal mass and state share. Local
Gaussian curvature estimates are

```text
sigma(Omega_m)  = 0.0107691115267379,
sigma(log10_mu) = 1.22188187627554,
sigma(f_scalar) = 1.41785672463727.
```

These are diagnostics, not posterior intervals. They explain why the
`Lambda=0` ablation is the cleaner predictive branch: it removes the nearly
degenerate split while retaining a fit competitive with wCDM and CPL.

At the free-`Lambda` optimum,

```text
Omega_scalar,kinetic,0
  = 0.0349207175400662,
Omega_scalar,potential,0
  = 0.105021300848136,
w_dark,effective,0
  = -0.899885402532645.
```

## 7. Decision

```text
old M6 equals direct parent scalar             = false;
parent scalar background equation in scorer   = direct ODE;
regular homogeneous mode                      = solved, not fitted;
flatness                                      = exact;
SN and BAO nuisance freedom                    = matched;
historical baselines                          = reproduced within tolerance;
parent scalar parameter estimates             = fit coordinates, not derived;
cosmology-support claim                        = false;
full MTS unification claim                     = false.
```

## 8. Next target

If the direct branch is competitive and not wholly edge-supported, checkpoint
5194 should add independent growth/CMB perturbation equations for this exact
background before promotion. If it is not competitive, 5194 should diagnose
which redshift and observable blocks reject it and return to the parent
potential/state-selection problem rather than tune a replacement closure.

## 9. Machine artifacts

- `source-intake/functional_rg/5193/fit_summary.csv`
- `source-intake/functional_rg/5193/parameter_estimates.csv`
- `source-intake/functional_rg/5193/prior_edge_table.csv`
- `source-intake/functional_rg/5193/baseline_comparison.csv`
- `source-intake/functional_rg/5193/robustness_matrix.csv`
- `source-intake/functional_rg/5193/parent_scalar_identifiability.csv`
- `source-intake/functional_rg/5193/residual_summary.csv`
- `source-intake/functional_rg/5193/parent_scalar_background.csv`
- `source-intake/functional_rg/5193/source_provenance.csv`
- `source-intake/functional_rg/5193/direct_parent_scalar_likelihood_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5193_VALIDATION.csv`
