# 4914 - Complex-source TTT replicas and residual-operator demotion

Marker: MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914

## Decision

Checkpoint 4913 removed a false zero-mode discontinuity from the real-cosine
stress three-point estimator but left a noisy, strongly noncovariant
two-cutoff result. This checkpoint constructs an independent complex
all-plus source channel, differentiates it directly through q^6, validates it
against the exact free determinant, tests its variance on an interacting
replica, and then builds the lower-variance discrete-FFT version.

The direct Taylor estimator is mathematically correct but statistically
unusable on the interacting chain:

\[
\Delta\zeta_{\rm direct}=1814.8\pm2446.2.
\]

It is rejected. Sixth coordinate moments amplify Monte Carlo variance much
more severely than the conditioned discrete momentum fit.

The complex discrete estimator removes the six nonconserving sign channels
which contaminate a finite-sample real-cosine response. On independent N=12
and N=16 chains it gives:

| row | stencil | delta zeta | statistical error | significance | covariant residual |
|---|---|---:|---:|---:|---:|
| N12, mu=0.6 | site | -0.02799 | 0.07432 | -0.38 | 0.982 |
| N12, mu=0.6 | half-link | -0.02582 | 0.06905 | -0.37 | 1.029 |
| N16, mu=0.4 | site | -0.14621 | 0.07178 | -2.04 | 0.489 |
| N16, mu=0.4 | half-link | -0.11528 | 0.06178 | -1.87 | 0.495 |

The dimensionally appropriate quantity is

\[
c_{\rm res}=\hat\mu^2\Delta\zeta.
\]

Its N12-to-N16 shifts are only 0.46 standard deviations for the site
stencil and 0.34 for the half-link stencil. Combining the two complex rows
at fixed stencil gives

\[
c_{\rm res}^{site}=-0.0213\pm0.0106,
\qquad
c_{\rm res}^{half}=-0.0172\pm0.0092.
\]

A cross-stencil covariance fit gives a combined complex-only value near
-0.018 with approximately 2.3-sigma significance. This remains below the
promotion threshold and the response geometry fails: the joint covariant
residual is 1.016 at N12 and 0.545 at N16.

Combining the independent 4913 and 4914 chains separately by stencil reduces
the scaled significance to 1.58 and 1.52 sigma. Thus the apparent negative
complex-only residual is not robust across the full evidence set.

The exact mass-matched free response was repeated above and below each
measured pole mass. Mass uncertainty contributes at most 5.1 times 10^-6 to
errors of order 0.06--0.07 and is negligible. The central finite-difference
linearity residual is below 1.5 times 10^-5.

No interacting six-derivative operator is promoted. The active theory keeps

\[
\boxed{\Gamma_{\mathrm{MTS,res}}=0.}
\]

This closes the present C-cubed residual search as a disciplined null result
and returns the main programme to the parent Einstein-Hilbert residue,
universal source coupling and measured Newton-constant calibration.

## 1. Complex source branch

For source momenta satisfying

\[
r_1+r_2+r_3=0,
\]

define phase-free complex insertions

\[
J_i(x;q)=e^{-iqr_i\cdot x}.
\]

The all-plus connected response is

\[
W^{+++}(q)=
\langle S_{123}\rangle
-\sum_{\rm cyclic}\operatorname{Cov}(S_i,S_{jk})
+\langle\delta S_1\delta S_2\delta S_3\rangle .
\]

For real cosine sources,

\[
\prod_i\cos(qr_i\cdot x+\phi_i)
\]

contains eight complex sign branches. In the exactly translation-invariant
expectation only the all-plus and all-minus closures survive. A finite Monte
Carlo sample does not enforce that selection exactly, so the other six
branches add variance.

The physical cosine-channel coefficient in the present Fourier convention is

\[
\boxed{
y_6^{\cos}
=\frac14\operatorname{Re}\left[
e^{-i(\phi_1+\phi_2+\phi_3)}W^{+++}_6
\right].
}
\]

The exact eight-branch reconstruction agrees with the existing real-cosine
observable at 1.95 times 10^-15. The all-minus response is the exact complex
conjugate of all-plus.

## 2. Direct Taylor construction

For centered lattice coordinates X, each source is expanded exactly:

\[
e^{-iqr\cdot X}
=\sum_{n=0}^{6}\frac{[-i(r\cdot X)]^n}{n!}q^n+O(q^7).
\]

The site and half-link metric insertions, pair contacts and triple contact are
carried as seventh-component polynomial jets. Products in the connected
response use exact truncated convolution.

Validation results:

| test | relative residual |
|---|---:|
| optimized site jet versus full jet | 1.86e-16 |
| jet reconstruction at finite q | 1.05e-13 |
| origin invariance | 3.82e-14 |
| complex FFT versus direct integer momentum | 7.32e-16 |
| eight channels versus real cosine | 1.95e-15 |
| all-minus versus conjugate all-plus | 0 |

On arbitrary finite samples the six nonconserving branches can carry 84
percent of the real-cosine response norm. They vanish in expectation but are
not harmless for variance.

## 3. Independent free determinant gate

Exact Gaussian fields with

\[
K(p)=m^2+4\sum_\mu\sin^2(p_\mu/2)
\]

were sampled directly at N=4 and m=1. The direct complex Taylor estimator was
run for 1600 fields on all twelve source geometries and compared with the
independent determinant series from checkpoint 4912.

Every component lies within 2.28 standard deviations of the exact answer.
After the finite-sample inverse-covariance correction,

\[
\chi^2_{\rm Hartlap}/12=1.312.
\]

This validates the observable convention, contact hierarchy and complex
phase map statistically against the exact determinant.

## 4. Why direct moments are rejected

The direct q^6 derivative contains coordinate moments through sixth order.
Although the total response is exactly independent of coordinate origin,
individual stochastic terms are large and cancel only after ensemble
averaging. On the N12 interacting smoke chain the projected result is

\[
1814.8\pm2446.2,
\qquad r_{\rm cov}=0.630.
\]

Increasing that chain from 160 to 500 observations would reduce the error only
by a factor of about 1.8, leaving it thousands of times less precise than the
discrete estimator. The direct-moment route is therefore rejected for
production rather than hidden behind a longer run.

## 5. Complex discrete estimator

At the allowed lattice scales, the potential and sixteen kinetic bilinears
are Fourier transformed once per field. The complex first, pair and triple
insertions are read directly at their signed momenta. No real-cosine sign
average is performed.

The same conditioned cubic extraction as checkpoint 4913 is retained:

\[
x_s=(2\pi s/N)^2,\qquad
y_6=e_3^T X^+R.
\]

The N12 and N16 design conditions remain 198.36 and 125.45. Independent
seeds 491511 and 491512 are used after the estimator-specific seed offset.
The chains have positive mass gaps, approximately 0.50 Metropolis acceptance,
overrelaxation acceptance above 0.98, and zero-mode autocorrelation below 1.5
observations.

The 160-observation complex smoke already reached errors of 0.13, comparable
to the 500-observation real-cosine calculation. At checkpoint depth the errors
fall to 0.06--0.07.

## 6. Replica and cutoff arbitration

The independent 4913-to-4914 shifts are below 1.57 standard deviations in all
four cutoff/stencil comparisons. No estimator conflict is measured.

For the complex estimator alone:

| combination | scaled coefficient | error | significance |
|---|---:|---:|---:|
| site, N12+N16 | -0.02132 | 0.01055 | -2.02 |
| half-link, N12+N16 | -0.01720 | 0.00919 | -1.87 |
| joint stencils and cutoffs | about -0.018 | about 0.008 | about -2.3 |

For all independent 4913 and 4914 rows:

| stencil | scaled coefficient | error | significance |
|---|---:|---:|---:|
| site | -0.01471 | 0.00933 | -1.58 |
| half-link | -0.01190 | 0.00783 | -1.52 |

The result is therefore compatible with zero once estimator replication is
included. More importantly, the N12 covariant-image gate fails badly and the
N16 residual remains near one half. A quotient coefficient cannot be promoted
from a response whose majority is not in the continuum tensor image.

## 7. Theory gates

    complex Taylor algebra                  = PASS;
    origin and phase conventions             = PASS;
    exact free determinant smoke             = PASS;
    direct coordinate-moment estimator       = REJECTED FOR VARIANCE;
    complex discrete FFT estimator           = SELECTED;
    independent estimator compatibility      = PASS;
    dimensionally scaled cutoff consistency  = PASS DIAGNOSTIC;
    three-sigma nonzero residual              = FAIL;
    covariant-image response                  = FAIL;
    exact free mass propagation               = NEGLIGIBLE;
    interacting C-cubed promotion             = BLOCKED;
    Gamma_MTS,res                             = ZERO PRESERVED;
    GR/Newton/PPN/Maxwell                     = UNCHANGED.

This is a null result for the optional six-derivative residual, not a failure
of the independently recovered free determinant or the lower-derivative local
GR branch.

## 8. Next target

4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md

Return to the central unification problem. Starting from the existing
metric-only local branch, derive the coefficient multiplying the
Einstein-Hilbert kinetic residue and its universal matter source from one
parent variation. Determine whether measured G is a boundary datum analogous
to the undetermined GR coupling or whether MTS predicts it from the motion
measure. Reject any route that inserts the source coefficient independently
of the kinetic residue.

No GitHub action or public claim is authorized.

## Sources

- post-checkpoint-work/4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-continuum-coefficient-or-zero-residual.md
- post-checkpoint-work/scripts/Y5_R2FR_4914_complex_source_Taylor_TTT_replica.py
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4914_JET_ALGEBRA_VALIDATION.csv
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4914_FREE_DETERMINANT_JET_SMOKE.csv
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4914_COMPLEX_PROJECTED_REPLICA.csv
- post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4914_MASS_AUGMENTED_PROJECTION.csv
- post-checkpoint-work/runs/20260712-4914-complex-discrete-checkpoint/log.txt

