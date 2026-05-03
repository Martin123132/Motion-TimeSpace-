# Renormalization-Flow Geometry of Riemann Zeta Zeros  
## Evidence for a Low-Dimensional Manifold and Intrinsic Stiffness

### Abstract

We study the motion of nontrivial zeros of the Riemann zeta function under a continuous smoothing flow applied to the Riemann–Siegel \( Z(t) \) function. By tracking zeros across a family of smoothing scales \( \sigma \), we observe that the induced zero dynamics admit an effective low-dimensional description. In particular, we find robust evidence that the flow is well-approximated by a two-dimensional renormalization-group (RG) manifold, stable across windows, perturbations, and estimator choices. Deviations from the clean flow induce a geometric stiffness that depends primarily on the intrinsic RG displacement rather than the raw perturbation amplitude. The stiffness scale is set by the mean zero spacing, suggesting a universal geometric structure in the zeta zero flow. While this does not constitute a proof of the Riemann Hypothesis, it reveals previously unexplored organizing principles governing zero dynamics on the critical line.

---

### 1. Introduction

The nontrivial zeros of the Riemann zeta function encode deep arithmetic structure and play a central role in analytic number theory. While extensive work has studied their statistical properties, comparatively little attention has been paid to their *dynamical behavior* under controlled deformations of the zeta function.

In this work, we study the evolution of zeta zeros under a continuous smoothing flow applied to the Riemann–Siegel \( Z(t) \) function. The smoothing parameter \( \sigma \) acts analogously to a renormalization scale, inducing a flow of zero locations \( t_n(\sigma) \). By tracking these trajectories, we investigate whether the induced dynamics admit a reduced geometric description.

Our primary finding is that the zero flow exhibits a stable two-dimensional RG manifold, together with an intrinsic stiffness that resists departures from the clean flow. This stiffness is geometric rather than coordinate-dependent and scales naturally with the mean zero spacing.

---

### 2. Zero Flow Construction

Let \( Z(t) \) denote the Riemann–Siegel function. For a given smoothing scale \( \sigma > 0 \), we define a smoothed function
\[
Z_\sigma(t) = \mathcal{S}_\sigma[Z](t),
\]
where \( \mathcal{S}_\sigma \) denotes a Gaussian smoothing operator implemented in Fourier space.

For each \( \sigma \), we numerically locate the zeros \( \{t_n(\sigma)\} \) of \( Z_\sigma(t) \) within a fixed window. At \( \sigma = 0 \), these coincide with the usual zeta zeros on the critical line.

We define the zero displacement vectors
\[
\Delta Z(\sigma) = t(\sigma) - t(0),
\]
and study their structure as functions of \( \sigma \).

---

### 3. Evidence for a Two-Dimensional RG Manifold

Across multiple windows and smoothing scales, we find that the collection of displacement vectors \( \Delta Z(\sigma) \) lies overwhelmingly within a two-dimensional subspace of the full zero configuration space.

This is established via:
- Singular value decomposition of the displacement ensemble,
- Stability of the dominant two singular directions under window changes,
- Persistence under different corruption and perturbation modes.

Attempts to reduce the flow to a one-dimensional (scalar) RG description consistently fail, while the two-dimensional description remains robust. This strongly suggests that the effective RG dynamics of zeta zeros are intrinsically two-dimensional.

---

### 4. Perturbations and Geometric Energy

To probe the structure of the RG manifold, we introduce controlled perturbations by displacing a single zero at a fixed smoothing scale and propagating this perturbation through the flow.

We define a geometric energy \( E \) as the principal angle between the clean RG plane and the perturbed RG plane, extracted via subspace comparison. This energy measures how strongly the perturbation deforms the RG geometry.

Crucially, we find that:
- \( E \) is symmetric under positive/negative perturbations,
- Odd (antisymmetric) components are subdominant,
- The energy grows smoothly and monotonically with perturbation strength.

These properties indicate a genuine geometric obstruction rather than estimator artefacts.

---

### 5. Intrinsic Coordinate and Normalization

A key result is that the energy \( E \) is not best understood as a function of the raw perturbation amplitude. Instead, it is naturally parameterized by the intrinsic RG displacement
\[
r = \|\mathrm{Proj}_{\mathrm{RG}}(\Delta Z)\|.
\]

When expressed as \( E(r) \), the energy profile becomes smoother and more universal. Furthermore, normalizing by the mean zero spacing \( \bar{\Delta} \) yields
\[
\frac{E}{\bar{\Delta}} \sim C \, r,
\]
over a wide range of perturbations.

This demonstrates that the observed stiffness is an intrinsic property of the RG geometry, not an artefact of coordinate choice or local density.

---

### 6. Robustness Tests

We subjected the analysis to extensive stress tests, including:
- Window-to-window comparisons,
- Ordering violations among zeros,
- Multi-\( \sigma \) perturbations,
- Alternative projection and gauge choices.

In all cases, the two-dimensional closure persists, while perturbations manifest as smooth deformations within or transverse to the RG manifold. No evidence was found for numerical instability or spurious dimensional reduction.

---

### 7. Interpretation and Implications

Our results indicate that the flow of zeta zeros under smoothing is governed by a low-dimensional geometric structure with intrinsic rigidity. While this does not imply a proof of the Riemann Hypothesis, it provides a new perspective on why zeros on the critical line behave coherently under deformation.

The existence of a universal stiffness scale tied to mean zero spacing suggests that the critical line is not merely a static constraint, but a dynamically stable configuration under natural analytic flows.

---

### 8. Conclusions and Outlook

We have identified a robust two-dimensional renormalization structure in the flow of Riemann zeta zeros and demonstrated the presence of intrinsic geometric stiffness. These findings open several avenues for future work, including:
- Analytic characterization of the RG generators,
- Extension to higher zeros and larger windows,
- Comparison with random matrix models under analogous flows.

While not resolving the Riemann Hypothesis, this work uncovers new organizing principles in the geometry of zeta zeros that merit further investigation.

---
