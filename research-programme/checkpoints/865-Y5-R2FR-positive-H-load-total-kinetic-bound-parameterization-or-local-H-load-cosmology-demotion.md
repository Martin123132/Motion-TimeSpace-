# 4849 Y5 R2FR positive H-load total-kinetic-bound parameterization

**Status:** The sign-complete positive \(H\)-load branch has been derived and tested. A kinetic-fraction parameterization guarantees a unique background root and prevents the optimizer from crossing the homogeneous kinetic fold. The branch produces a substantial SH0ES improvement, including better AIC and BIC than the fitted baselines, but every SH0ES fit runs to the imposed kinetic cap. The no-SH0ES branch is roughly CPL-level in raw chi-square and is not preferred after comparison with the best fitted baselines. The result is an unstable internal lead, not a cosmology claim.

**Decision:** `POSITIVE_H_LOAD_KINETIC_FRACTION_PARAMETERIZATION_DERIVED_SH0ES_AIC_BIC_GAIN_PERSISTS_UNDER_STRICT_CAP_BUT_REMAINS_KINETIC_EDGE_NO_SH0ES_NOT_PREFERRED_PRIVATE_LEAD_ONLY`.

## 1. Positive-density branch

The implicit equation remains

\[
E^2=\Omega_m(1+z)^3+1-\Omega_m
+A_H[R((qE)^3)-R(q^3)].
\]

Select

\[
q^3\ge y_{\rho=0},
\qquad
A_H\ge0.
\]

Then the action-derived active density at \(z=0\) is nonnegative:

\[
A_HR(q^3)\ge0.
\]

In this domain,

\[
G_{\theta\theta}
=3A_Hq^2h(q),
\]

where

\[
h(q)=\frac{2qF'(q^3)+3q^4F''(q^3)}{3}<0.
\]

The homogeneous kinetic bracket is

\[
\mathcal K_0
=6+9G_{\theta\theta}
=6+27A_Hq^2h(q).
\]

## 2. Exact kinetic-fraction parameterization

Define

\[
A_{\max}(q)
=\frac{6}{-27q^2h(q)},
\]

and parameterize

\[
A_H=f_KA_{\max}(q),
\qquad
0\le f_K<1.
\]

This gives the exact identity

\[
\boxed{\mathcal K_0=6(1-f_K)}.
\]

The derivative of the implicit Friedmann equation at \(z=0\) is

\[
\left.\frac{\partial\mathcal F_E}{\partial E}\right|_0
=2+9A_Hq^2h(q)
=2(1-f_K).
\]

For both retained kernels, \(|h|\) decreases beyond the positive-density threshold. Therefore for \(z\ge0\),

\[
\frac{\partial\mathcal F_E}{\partial E}
\ge 2E(1-f_K)>0.
\]

The same parameter simultaneously prevents a homogeneous kinetic sign flip and a folded/multiple background root.

## 3. Prior structure

Three real-data matrices were run:

1. `standard`: \(f_K\le0.95\), kernel load up to 99% saturation;
2. `broad`: \(f_K\le0.95\), kernel load up to 99.9% saturation;
3. `strict`: \(f_K\le0.80\), kernel load up to 99.9% saturation.

The saturation limit is numerical, not fundamental. Comparing standard and broad runs tests whether the earlier \(q\) edge was merely a finite kernel-box artifact. Comparing broad and strict runs tests dependence on the physical kinetic fold.

All runs used Pantheon+, DESI DR2 BAO, 768 integration points, at least three deterministic starts, and the fitted LCDM, \(w\)CDM and CPL baselines from the same likelihood execution.

## 4. SH0ES results

### Broad \(f_K\le0.95\)

| Kernel | chi2 | Delta chi2 vs LCDM | Delta AIC vs best baseline | Delta BIC vs best baseline | Edges |
|---|---:|---:|---:|---:|---|
| exponential | 1745.844 | -27.903 | -9.985 | -6.378 | \(f_K=\) high |
| tanh | 1745.809 | -27.938 | -10.020 | -6.413 | \(f_K=\) high |

The broader saturation box removes the \(q\) edge. Both kernels still select

\[
f_K=0.95,
\qquad
\mathcal K_0=0.30,
\qquad
\min\partial_E\mathcal F_E=0.10.
\]

The fitted constant background is negative:

\[
\Omega_{\Gamma0}=-1.72
\]

for the broad exponential fit and

\[
\Omega_{\Gamma0}=-0.48
\]

for broad tanh. The total \(z=0\) closure is still exact, but the bare-constant/active-memory cancellation is physically costly and must not be hidden.

### Strict \(f_K\le0.80\)

| Kernel | chi2 | Delta chi2 vs LCDM | Delta AIC vs best baseline | Delta BIC vs best baseline | Edges |
|---|---:|---:|---:|---:|---|
| exponential | 1749.064 | -24.683 | -6.765 | -3.158 | \(f_K=\) high |
| tanh | 1749.047 | -24.700 | -6.782 | -3.175 | \(f_K=\) high |

The gain survives a stricter homogeneous margin:

\[
\mathcal K_0=1.20,
\qquad
\min\partial_E\mathcal F_E=0.40.
\]

But both optimizers again stop at the largest permitted \(f_K\). The improvement is therefore monotonic toward the fold rather than an interior best fit.

## 5. no-SH0ES results

The broad and strict runs agree because their optima are interior in \(f_K\):

| Kernel | chi2 | Delta chi2 vs LCDM | Delta AIC vs best baseline | Delta BIC vs best baseline | Edges |
|---|---:|---:|---:|---:|---|
| exponential | 1463.857 | -6.208 | +1.148 | +8.593 | \(q=\) low |
| tanh | 1464.456 | -5.609 | +1.747 | +9.192 | \(q=\) low |

The exponential branch has a slightly lower raw chi-square than CPL:

\[
1463.857<1464.291,
\]

with the same five fitted parameters. However \(w\)CDM is the best AIC baseline and LCDM is the best BIC baseline, so the \(H\)-load branch is not selected after the appropriate comparison.

Both kernels choose the lower positive-density boundary:

\[
R(q^3)=0.
\]

Thus the no-SH0ES data prefer the smallest possible present active density in this branch, not the strong SH0ES response.

## 6. What is and is not learned

The positive branch is not numerical rubbish:

- it solves the implicit equation to residuals below \(3\times10^{-15}\);
- the background derivative remains positive;
- its strict SH0ES fit beats the fitted baselines by both AIC and BIC;
- exponential and tanh give nearly identical best-fit behavior.

It is not stable evidence:

- SH0ES always drives to the kinetic cap;
- the best broad fits require negative bare \(\Gamma_0\) and large cancellation;
- no-SH0ES does not beat the best baseline after penalties;
- no perturbation, CMB or growth likelihood has tested the near-fold response;
- the full scalar/vector kinetic matrix remains unproved.

The correct status is

\[
\text{real internal lead, edge-dependent, nonclaim}.
\]

## 7. Branch decision

The local \(H\)-load cosmology should not be completely deleted because the strict SH0ES gain is substantial and survives both kernels. It should no longer be treated as the default cosmological spine because its gain is tied to calibration pressure and the kinetic boundary.

No further blind widening is justified. The next test must attack the actual failure mode:

1. derive the scalar/vector perturbation matrix around the fitted branch;
2. impose a parent-owned lower bound on \(\mathcal K_0\), not an arbitrary optimizer cap;
3. include growth/CMB or chronometer data that directly constrain \(H(z)\);
4. reject the branch if the gain disappears once the kinetic margin and non-SH0ES evidence are enforced.

The causal history/current route remains the cleaner alternative if this edge cannot be regularized from the parent action.

## 8. Run evidence

- `post-checkpoint-work/runs/20260709-4849-H-load-positive-smoke-fit`
- `post-checkpoint-work/runs/20260709-4849-H-load-positive-broad`
- `post-checkpoint-work/runs/20260709-4849-H-load-positive-strict`

All checkpoint rows remain `valid_for_claim=false`.

## 9. Next target

`4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md`
