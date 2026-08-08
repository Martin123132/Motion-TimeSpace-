# 4848 Y5 R2FR H-load background equation, negative-amplitude window and cosmology smoke

**Status:** The action-derived \(H\)-load branch has been solved as an implicit Friedmann equation and tested against real Pantheon+ and DESI DR2 BAO data. Both negative-amplitude kernels collapse to \(A_H=0\) on the SH0ES and no-SH0ES branches. The simplest local \(H\)-load cosmological completion is therefore empirically demoted; this is a physics result, not a failed optimizer.

**Decision:** `H_LOAD_IMPLICIT_BACKGROUND_UNIQUE_BRANCH_DERIVED_REAL_PANTHEON_DESI_SMOKE_NEGATIVE_AMPLITUDE_COLLAPSES_TO_LCDM_BOTH_KERNELS_AND_BRANCHES_PRIVATE_NONCLAIM`.

## 1. Normalized background equation

Checkpoint 4847 gives

\[
\kappa\rho_{\rm mem}
=\Gamma_\star R(y),
\qquad
R(y):=F(y)-3yF'(y),
\qquad
y=(\ell_QH)^3.
\]

Define

\[
E(z)=H(z)/H_0,
\qquad
q=\ell_QH_0,
\qquad
A_H=\Gamma_\star/(3H_0^2).
\]

Flat closure at \(z=0\) fixes the constant background:

\[
\Omega_{\Gamma0}
=1-\Omega_{m0}-A_HR(q^3).
\]

The Friedmann equation is therefore

\[
\boxed{
E^2
=\Omega_{m0}(1+z)^3
+1-\Omega_{m0}
+A_H\left[
R((qE)^3)-R(q^3)
\right]
}.
\]

This is implicit because the memory density depends on \(H\) itself. The runner solves this equation directly; it never substitutes \(\Gamma_\star F\) for the density.

## 2. Unique physical branch

Let

\[
\mathcal F_E
=E^2-\Omega_{m0}(1+z)^3-1+\Omega_{m0}
-A_H[R((qE)^3)-R(q^3)].
\]

Then

\[
\frac{\partial\mathcal F_E}{\partial E}
=2E-3A_Hq^3E^2R'(y),
\]

with

\[
R'(y)=-2F'(y)-3yF''(y).
\]

The 4847 negative-amplitude windows begin exactly where

\[
R'(y)\ge0.
\]

For \(z\ge0\), \(E\ge1\), so \(y\ge q^3\). With

\[
A_H\le0,
\]

the implicit derivative obeys

\[
\frac{\partial\mathcal F_E}{\partial E}\ge2E>0.
\]

Therefore the data-era expanding branch is unique and has no fold or root jumping. At \(z>0\), \(\mathcal F_E(E=1)<0\) and \(\mathcal F_E\to+\infty\), so exactly one root exists above \(E=1\).

The numerical solver reached maximum equation residuals below

\[
2.1\times10^{-15}
\]

in the nonzero-amplitude dry run.

## 3. Sign theorem

Since \(R'(y)\ge0\) and \(E(z)\ge1\),

\[
R((qE)^3)-R(q^3)\ge0.
\]

Thus the negative-amplitude branch satisfies

\[
A_H[R((qE)^3)-R(q^3)]\le0.
\]

At fixed \(\Omega_{m0}\), this branch can only lower \(E^2(z)\) relative to flat \(\Lambda\)CDM for \(z>0\). This is a sharp prediction of the derived sign window, not a fitting convention.

## 4. Fit setup

Data:

- Pantheon+ `MU_SH0ES` branch: 1701 usable supernova rows;
- Pantheon+ no-SH0ES shape branch with calibrators removed;
- DESI DR2 BAO: 13 correlated measurements.

Fitted baselines:

- flat \(\Lambda\)CDM: \(H_0,\Omega_{m0},r_d\);
- \(w\)CDM: baseline parameters plus \(w\);
- CPL: baseline parameters plus \(w_0,w_a\).

Each \(H\)-load model fitted

\[
H_0,\Omega_{m0},r_d,A_H,q,
\]

with \(A_H\in[-2,0]\) and \(q\) restricted to the derived negative-amplitude density/convexity window:

\[
0.8735804647\le q\le1.2393904597
\]

for \(1-e^{-y}\), and

\[
0.8487655861\le q\le1.1237858678
\]

for \(\tanh y\).

The smoke run used 768 integration points, 50 optimizer iterations and three deterministic starts.

## 5. Results

### SH0ES branch

| Model | chi2 | AIC | BIC | Delta AIC vs best baseline | Delta BIC vs best baseline |
|---|---:|---:|---:|---:|---:|
| LCDM | 1773.747 | 1779.747 | 1796.087 | +13.918 | +6.632 |
| wCDM | 1759.669 | 1767.669 | 1789.455 | +1.840 | 0.000 |
| CPL | 1755.829 | 1765.829 | 1793.062 | 0.000 | +3.607 |
| H-load exponential | 1773.747 | 1783.747 | 1810.980 | +17.918 | +21.525 |
| H-load tanh | 1773.747 | 1783.747 | 1810.980 | +17.918 | +21.525 |

Both \(H\)-load fits return

\[
A_H=0.
\]

### no-SH0ES branch

| Model | chi2 | AIC | BIC | Delta AIC vs best baseline | Delta BIC vs best baseline |
|---|---:|---:|---:|---:|---:|
| LCDM | 1470.065 | 1476.065 | 1492.267 | +3.356 | 0.000 |
| wCDM | 1464.709 | 1472.709 | 1494.312 | 0.000 | +2.044 |
| CPL | 1464.291 | 1474.291 | 1501.294 | +1.582 | +9.027 |
| H-load exponential | 1470.065 | 1480.065 | 1507.068 | +7.356 | +14.801 |
| H-load tanh | 1470.065 | 1480.065 | 1507.068 | +7.356 | +14.801 |

Again,

\[
A_H=0
\]

for both kernels.

The fitted \(q\) value is physically unidentified once \(A_H=0\). Any \(q\)-edge flag on those rows is therefore not evidence about the scale; the meaningful edge is \(A_H=0\).

## 6. Interpretation

The result rejects this combination:

\[
\text{local expansion load}
+\text{cubic determinant}
+\text{negative-amplitude density/convexity window}
\]

as a useful late-time background correction for these SN+BAO likelihoods.

It does not reject:

- the 4845 exchange-odd local suppression theorem;
- the exact covariant stress derivation in 4847;
- the older \(N/u_3\) history model, which has a different redshift dependence;
- a positive-amplitude branch satisfying the total kinetic bound;
- the rest of the MTS field programme.

The correct response is not to widen the negative prior. The sign theorem already shows that every more-negative value pushes \(E(z)\) in the same disfavoured direction.

## 7. Next disciplined fork

One sign-complete test remains before the local \(H\)-load route should be demoted completely:

1. derive a positive-\(A_H\) parameterization that enforces

\[
6+9G_{\theta\theta}>0
\]

throughout the fitted redshift range;

2. test both positive-density and closure-compensated positive-amplitude branches;

3. if they also collapse or fail AIC/BIC, retire the local \(H\)-load cosmology and return to a causal parent-owned history/current action.

No public cosmology or local-GR claim follows from 4848.

## 8. Run evidence

`post-checkpoint-work/runs/20260709-4848-H-load-smoke-fit-bg2`

All checkpoint rows remain `valid_for_claim=false`.

## 9. Next target

`4849-Y5-R2FR-positive-H-load-total-kinetic-bound-parameterization-or-local-H-load-cosmology-demotion.md`
