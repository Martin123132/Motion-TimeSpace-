# 4913 - Matched interacting TTT smoke, analytic channel repair, and non-promotion

Marker: MTS_MATCHED_INTERACTING_TTT_SMOKE_4913

## Decision

This checkpoint executes the short interacting motion-scalar stress
three-point calculation selected at 4912. It measures the mass gap, evaluates
the full triangle-plus-contact response on all twelve rank-eight source
geometries, subtracts the exact mass-matched free response on the identical
regulator, and tests site and half-link stress stencils at two cutoffs.

The first two-cutoff extraction produced an apparent jump from order one
tenth to order ten. That jump is rejected as a measurement artifact. Two
specific defects were found and repaired:

1. The homogeneous cosine response at zero momentum contains all eight sign
   channels, whereas the analytic nonzero-momentum branch contains only the
   all-plus and all-minus momentum closures. Mixing those normalizations
   creates a discontinuity at the first fit point which is amplified as the
   sixth momentum derivative.
2. The N=16 row fitted an unnecessary q^8 nuisance term with five points.
   Its design condition was 1963.53 and its q^6 weight norm was 28.0413.
   The justified cubic fit has condition 125.454 and weight norm 1.48637.

After both repairs the catastrophic cutoff jump disappears. The final
covariance-aware projected rows are:

| lattice row | stencil | delta zeta | standard error | significance | covariant residual |
|---|---|---:|---:|---:|---:|
| N=12, mu=0.6 | site | 0.198784 | 0.124403 | 1.598 | 0.5933 |
| N=12, mu=0.6 | half-link | 0.166185 | 0.108050 | 1.538 | 0.6602 |
| N=16, mu=0.4 | site | -0.040970 | 0.139526 | -0.294 | 0.7999 |
| N=16, mu=0.4 | half-link | -0.048986 | 0.101479 | -0.483 | 0.8829 |

The two stencils agree well inside their statistical errors. The N=12 to
N=16 differences are 1.29 and 1.45 conservative quadrature standard errors
for the raw coefficient, and 1.56 and 1.61 for mu^2 delta-zeta. Therefore the
data do not establish a nonzero residual and do not show the prior blow-up.
They also do not establish a continuum coefficient: there are only two
cutoffs and 59--88 percent of each response vector remains outside the
covariant rank-eight image.

The paired sampled-free control variate increases the projected standard
error by factors 1.35--1.46. It is rejected for production. The primary
estimator is the interacting response minus the deterministic exact
mass-matched free response.

No long run is authorized by this checkpoint. No six-derivative coefficient
is inserted into the active action, and

\[
\boxed{\Gamma_{\mathrm{MTS,res}}=0}
\]

is preserved.

## 1. Literal scalar chain

The Euclidean lattice action is

\[
S[\psi]=\sum_x\left[
\frac12\sum_{\mu}(\psi_{x+\hat\mu}-\psi_x)^2
+\frac34 g\,|\psi_x|^{4/3}\right],
\qquad
g=\hat\mu^{8/3}.
\]

The two final rows use

\[
(N,\hat\mu)=(12,0.6),\qquad(16,0.4).
\]

Checkerboard Metropolis updates are followed by an exact free overrelaxation
and an accept/reject interacting overrelaxation. Their measured properties
are:

| row | pole mass | error | tau of zero-mode square | Metropolis acceptance | overrelax acceptance |
|---|---:|---:|---:|---:|---:|
| N12 | 0.602470 | 0.051804 | 0.681 | 0.5039 | 0.9832 |
| N16 | 0.309419 | 0.031028 | 1.566 | 0.5106 | 0.9940 |

The chains supply 125 and 112 jackknife blocks. This is a smoke-quality
coefficient test, not a precision continuum ensemble.

## 2. Full response estimator

For first metric insertions S_i, pair contacts S_ij and the triple contact
S_123, the connected third response is

\[
\boxed{
R_{123}
=\langle S_{123}\rangle
-\operatorname{Cov}(S_1,S_{23})
-\operatorname{Cov}(S_2,S_{13})
-\operatorname{Cov}(S_3,S_{12})
+\langle\delta S_1\delta S_2\delta S_3\rangle .
}
\]

The traceful determinant contacts derived at 4912 are retained exactly.
Coordinate-space and FFT implementations agree in all site and half-link
tests through 5.69 times 10^-14.

The claim-bearing finite-regulator estimator is

\[
\boxed{
\widehat{\Delta y}_a
=\widehat y_{\mathrm{int}}^a
-y_{\mathrm{free,exact}}^a(\widehat m_{\mathrm{gap}}).
}
\]

The mass-matched free term is evaluated deterministically from the complete
free determinant, not estimated from a second noisy chain.

## 3. Paired control-variate arbitration

A synchronously updated free chain with reference mass m_0 gives the unbiased
family

\[
\widehat{\Delta y}_{a,\beta}
=\widehat y_{\mathrm{int}}^a
-\beta\left[
\widehat y_{\mathrm{free}}^a(m_0)
-y_{\mathrm{free,exact}}^a(m_0)\right]
-y_{\mathrm{free,exact}}^a(\widehat m_{\mathrm{gap}}).
\]

The primary estimator has beta=0. The common-random-number diagnostic tested
beta=1. Although the fields remain correlated at 0.63--0.68, the nonlinear
connected TTT observables are not correlated strongly enough in the useful
direction. Beta=1 increases the projected error:

| row | site paired/primary error | half-link paired/primary error |
|---|---:|---:|
| N12 | 1.348 | 1.368 |
| N16 | 1.442 | 1.458 |

The paired control is therefore rejected rather than averaged into the
primary result.

## 4. Analytic zero-momentum cosine channel

For nonzero source momenta satisfying k_1+k_2+k_3=0, a product of real cosine
sources selects only the all-plus and all-minus closures:

\[
R_{\cos}(q>0)
=\frac14\operatorname{Re}\left[
e^{i(\phi_1+\phi_2+\phi_3)}W^{+++}(q)\right].
\]

At q=0 every sign assignment is spatially homogeneous. The raw measured
response is instead

\[
R_{\mathrm{hom}}(0)
=\left(\prod_i\cos\phi_i\right)W(0).
\]

The q-to-zero analytic branch is consequently

\[
\boxed{
R_{\cos}^{\mathrm{an}}(0)
=
\frac{\cos(\phi_1+\phi_2+\phi_3)}
{4\prod_i\cos\phi_i}
R_{\mathrm{hom}}(0).
}
\]

This projection is applied to every full-sample and jackknife response and to
the exact free reference. Its algebraic validation residual is 2.78 times
10^-17. The rejected extraction mixed R_hom(0) directly with R_cos(q>0);
for the twelve phase triples the normalization mismatch is approximately a
factor four before the sixth-derivative amplification.

## 5. Conditioned q^6 extraction

For scales s=0,...,s_max define

\[
x_s=\left(\frac{2\pi s}{N}\right)^2,\qquad
X_{sj}=x_s^j,\quad j=0,\ldots,d.
\]

The q^6 coefficient is the linear functional

\[
\boxed{
y_6=w^T R,\qquad w^T=e_3^T X^+.
}
\]

The N=12 row uses s_max=3 and d=3. The N=16 row uses s_max=4 and d=3, making
the second fit overdetermined. The accepted design diagnostics are:

| row | polynomial degree | condition number | norm of q^6 weights |
|---|---:|---:|---:|
| N12 | 3 | 198.360 | 2.56484 |
| N16 | 3 | 125.454 | 1.48637 |

The rejected N16 degree-four interpolation had condition 1963.53 and weight
norm 28.0413. Its large negative coefficient was a predictable noise
amplification, not a continuum datum.

## 6. Cutoff and stencil gates

The same-stencil cutoff differences are

\[
\frac{|0.198784-(-0.040970)|}
{\sqrt{0.124403^2+0.139526^2}}=1.29,
\]

\[
\frac{|0.166185-(-0.048986)|}
{\sqrt{0.108050^2+0.101479^2}}=1.45.
\]

For the dimensionally scaled quantity \hat\mu^2\Delta\zeta the corresponding
values are 1.56 and 1.61. These conservative comparisons do not use
cross-cutoff covariance because the chains are independent. They show that
zero remains allowed; they do not define a two-point continuum intercept.

At fixed cutoff the site-to-half-link shifts are only 0.0326 and 0.0080.
Those stencils share configurations and are not independent measurements, so
they are treated as a regulator diagnostic rather than averaged.

The decisive failed gate is covariance:

\[
r_{\mathrm{cov}}
=\frac{\|y-M\widehat c\|_2}{\|y\|_2}
=0.593\text{--}0.883.
\]

The response is not yet concentrated in the continuum covariant image. A
nonzero quotient coefficient cannot be separated reliably from finite-volume,
hypercubic and statistical components.

## 7. Theory gates

    traceful interacting observables       = validated;
    analytic q=0 cosine channel            = repaired and validated;
    q6 design conditioning                 = pass;
    mass-gap and chain-health smoke        = pass;
    paired beta=1 control                  = rejected;
    site versus half-link diagnostic       = compatible;
    two-cutoff zero compatibility          = pass as diagnostic only;
    common continuum coefficient           = not established;
    covariant-image residual               = fail;
    interacting long run                   = withheld;
    active six-derivative residual          = zero preserved;
    GR/Newton/PPN/Maxwell                   = unchanged.

This checkpoint materially advances the calculation by removing a false
cutoff catastrophe and fixing the correct observable channel. It does not
turn a sub-two-sigma smoke result into an MTS prediction.

## 8. Next target

4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md

Use independent interacting seeds at N=12 and N=16, retain the exact
mass-matched subtraction, record cross-stencil jackknife covariance, and add a
direct q=0 momentum-derivative or coordinate-moment estimator that does not
infer a sixth derivative from four or five noisy ordinates. Promote a
coefficient only if independent replicas agree, the covariant-image residual
falls substantially, and the two cutoffs support a common limit. Otherwise
demote the interacting C-cubed residual to zero at this order.

No GitHub action or public claim is authorized.

## Sources

- post-checkpoint-work/4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md
- post-checkpoint-work/scripts/Y5_R2FR_4913_matched_interacting_TTT_smoke.py
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4913_CHAIN_SUMMARY.csv
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4913_OBSERVABLE_VALIDATION.csv
- post-checkpoint-work/runs/20260712-4913-channel-fixed-checkpoint/log.txt
