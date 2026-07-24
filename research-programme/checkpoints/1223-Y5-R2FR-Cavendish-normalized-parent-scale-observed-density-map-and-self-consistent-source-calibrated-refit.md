# 5207 - Cavendish-Normalized Parent Scale, Observed-Density Map and Self-Consistent Source-Calibrated Refit

Private derivation and empirical robustness checkpoint. No GitHub action and
no public cosmology or full-MTS claim.

Checkpoint marker: `MTS_5207_CAVENDISH_SOURCE_CALIBRATED_REFIT`.

## Executive result

Checkpoint 5206 solved the finite-`zeta_c` Jordan background but deliberately
retained the action-scale density convention. Checkpoint 5207 removes that
last source-normalization convention.

Define the measured reduced Newton scale by

```text
M_N^2=1/(8 pi G_N).
```

The same parent action predicts

```text
G_cav,0
 =1/(8 pi M_R^2)
   [(2f0+4f_phi0^2)/(2f0+3f_phi0^2)]/f0
 =g0/(8 pi M_R^2).
```

Requiring `G_cav,0=G_N` gives the exact relation

```text
s=M_R^2/M_N^2=g0.
```

This derives the ratio of the parent and measured gravitational scales. It
does not derive the absolute dimensionful magnitude of `G_N`.

## 1. Coupled boundary-value problem

Observed density parameters and action-scale density parameters obey

```text
Omega_i,bare=Omega_i,observed/s.
```

At every likelihood evaluation the runner simultaneously solves

```text
ln E(0)^2=0,
ln[s/g(phi0)]=0,
```

for the regular-mode amplitude and `s`. The field phase remains derived from
the `N=-18` regular Frobenius boundary condition. No source coefficient,
scalar fraction or phase is fitted.

The symbolic calibration residual is

```text
0,
```

and the present Poisson-source residual is

```text
0.
```

Numerically,

```text
Omega_m,bare (G_eff,0/G_bare)/Omega_m,observed
 =1.
```

Thus the Newtonian source coefficient at the present epoch is normalized to
measured `G_N` by the parent relation itself.

## 2. Fixed-parameter calibration test

Applying the exact map to the checkpoint-5206 signed optimum without
refitting gives

```text
Delta chi2_joint
 =-0.10670332004.
```

This is the direct size of the convention correction before the likelihood
is allowed to readjust.

## 3. Calibrated refit

The source-calibrated optimum is

```text
zeta_c                    =-1.99251066833e-05;
Omega_m,observed           =0.311668148681;
Omega_m,bare               =0.311626152088;
mu=m_gap/H0                =0.764819326846;
H0                         =67.2431118289 km/s/Mpc;
phi0                       =2.60046992189;
q0                         =-0.416499237103;
M_R^2/M_N^2                =1.00013476594;
M_R/M_N                    =1.0000673807;
G_bare/G_N                 =0.999865252216;
gamma-1                    =-1.07404748973e-08;
Gdot/G                     =-2.96875085343e-15 yr^-1;
chi2_cosmology             =1474.0873573;
chi2_local                 =0.879271025525;
chi2_joint                 =1474.96662833.
```

Relative to the uncalibrated checkpoint-5206 signed fit:

```text
Delta chi2_joint=-0.10670332004;
Delta AIC_joint =-0.10670332004;
Delta BIC_joint =-0.10670332004.
```

Both models have the same parameter count, so this is a pure calibration
sensitivity comparison.

Relative to the locked minimal zero-Lambda parent:

```text
Delta AIC_joint=1.79263185641;
Delta BIC_joint=7.19994956688.
```

Relative to fitted LCDM:

```text
Delta AIC_joint=0.646470636365;
Delta BIC_joint=11.4611060573.
```

The finite signed coupling remains an allowed near-GR coordinate only if it
is interior and locally bounded. It is not promoted merely because the
source calibration is numerically small.

## 4. Local-GR branch distinction

The calculation above is the unscreened long-range branch used by checkpoint
5204: the local field inherits the cosmological `phi0`. On a separate exact
local branch with

```text
phi_local=0,
q_local=0,
```

one instead has `g_local=1` and `M_R=M_N`. No local transition or screening
mechanism between the cosmological state and that exact local branch has
been derived, so the two calibrations are recorded separately rather than
blended.

## 5. Decision

```text
Cavendish parent-scale ratio derived              = yes;
observed-to-bare density map derived              = yes;
flatness and source calibration solved together  = yes;
present Newtonian source residual                 =2.220e-16;
regular/numerical gates                            =true;
signed local two-sigma envelopes                   =true;
absolute numerical G_N derived                    = no;
local transition phi_cosmology -> 0 derived       = no;
common F_R,V,Z,X2 trajectory selected             = no;
official CMB likelihood                           = no;
cosmology-support claim                           = false;
full MTS claim                                    = false.
```

Selected next route:

```text
DERIVE_COMMON_F_R_V_Z_X2_RUNNING_AND_ABSOLUTE_PARENT_SCALE_SELECTION.
```

The source-coupling normalization is no longer a free gap. What remains is
genuinely upstream: select the running coefficients and the absolute parent
scale from the parent theory, or show that they must remain measured inputs.

## 6. Evidence products

- `source-intake/functional_rg/5207/Cavendish_source_map.csv`
- `source-intake/functional_rg/5207/calibrated_fit_summary.csv`
- `source-intake/functional_rg/5207/calibrated_fit_parameters.csv`
- `source-intake/functional_rg/5207/calibration_branch_comparison.csv`
- `source-intake/functional_rg/5207/calibration_sensitivity.csv`
- `source-intake/functional_rg/5207/model_comparisons.csv`
- `source-intake/functional_rg/5207/regular_and_source_validation.csv`
- `source-intake/functional_rg/5207/calibrated_background_samples.csv`
- `source-intake/functional_rg/5207/source_provenance.csv`
- `source-intake/functional_rg/5207/Cavendish_source_calibrated_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5207_VALIDATION.csv`
