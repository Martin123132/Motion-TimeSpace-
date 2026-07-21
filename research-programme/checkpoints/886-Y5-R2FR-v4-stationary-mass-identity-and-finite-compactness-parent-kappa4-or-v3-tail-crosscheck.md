# 4870 - Quartic stationary-mass identity and finite-compactness parent response

Marker: `V4_STATIONARY_MASS_IDENTITY_4870`

Decision: `STATIONARY_TOTAL_MASS_VARIATION_AND_SMALL_P_ENVELOPE_THEOREM_MAKE_ONSHELL_L4_THE_PARENT_CORRESPONDENCE_KAPPA4_ZERO_BOUNDARY_V3_PROFILE_CANCELED_FINITE_C_GRID_INSIDE_BINARY_WINDOWS_CHARGE_SPLIT_D4_DERIVED_NOT_FREE_C3_EXTERNAL_CONFLICT_AND_V3_TAIL_CROSSCHECK_OPEN_PRIVATE_NONCLAIM`

## Result

The quartic compact-body response is no longer waiting on an assumed ADM completion inside the selected public correspondence action.

Yagi et al.'s strong-field mass formula writes the total stationary mass as minus the spatial integral of the Einstein, aether and matter Lagrangians. For neighboring stationary solutions at fixed couplings and baryon number, the metric and compact-matter variations reduce to vanishing outer surface terms in the asymptotically Cartesian gauge. The velocity dependence is therefore carried by the on-shell aether functional.

In the correlated public limit `c_i=p cbar_i+O(p2)`, this gives a first-order-`p` envelope theorem: metric and matter backreaction do not add a second independent mass coefficient. The leading flow profile extremizes `L2`, so an independent zero-boundary `v3` profile drops out of the `v4` mass coefficient. The exact `L4` functional from checkpoint 4868 is therefore the physical parent-correspondence quartic response at `O(p)`.

At `r=1/3,C=0.3`,

```text
f_parent      =  0.27696368;
kappa4_parent = -0.15842314;
g_parent      = -0.43649409.
```

A 26-row finite-compactness scan gives the conservative private envelopes

```text
|kappa4_parent| < 0.159;
|g_parent|      < 0.47;
```

over the sampled public corridor `1/30<=r<=1/3`, `0.03<=C<=0.3`, with additional compactness refinement on `r=1/3`. These are inside the inherited no-cancellation binary boxes by factors greater than `9.1` and `24.7` respectively.

This is a prediction of the selected Einstein-aether correspondence action, not yet a primitive derivation from the original MTS scalar corpus and not a public local-GR claim. The `C3` first-sensitivity conflict found in checkpoint 4869 remains an external consistency gate, and the independent `v3,l=1` asymptotic extraction remains required as a cross-check.

## Stationary total-mass theorem

For a stationary star, use the first-derivative Einstein Lagrangian and write

\[
M_{\rm tot}=-\int_\Sigma d^3x
\left(\mathcal L_g+\mathcal L_{\ae}+\mathcal L_m\right).
\]

For a one-parameter family labeled by the asymptotic relative velocity `v`, variation gives Euler terms plus spatial-boundary terms. On shell:

1. the metric surface term vanishes in the asymptotically Cartesian gauge `g=eta+O(1/R)`;
2. the matter surface term vanishes because the fluid has compact support;
3. the unit constraint is preserved between neighboring solutions;
4. the remaining aether surface term equals the variation of its on-shell radial functional.

Now take the public small-coupling family

\[
\mathcal L_{\ae}=p\,\overline{\mathcal L}_{\ae}+O(p^2).
\]

Smoothness of the stationary branch at fixed finite `r` gives

\[
M(v,p)=M_{\rm GR}
-p\,\overline I_{\ae}^{\rm on}(v)+O(p^2),
\]

up to the common `16 pi G` normalization retained below. Metric and matter corrections begin at `O(p)` but multiply their zeroth-order Euler equations, so they do not create an additional first-order-`p` mass functional. This is the standard stationary envelope theorem applied to the correlated public branch.

The theorem requires a regular gauge-fixed stationary branch. The finite-C collocation solve and independent variational Hessian smoke test from checkpoint 4868 supply numerical evidence for that assumption over the sampled corridor; they do not constitute a global existence proof.

## Elimination of the third-order profile

Normalize the spatial flow by its exact asymptotic factor `gamma v` and write

\[
q(v,R)=q_1(R)+v^2q_3(R)+O(v^4),
\qquad q=(a,b).
\]

The reduced aether functional is

\[
\overline I_{\ae}
=v^2 I_2[q]+v^4I_4[q]+O(v^6).
\]

Expanding about `q1` gives

\[
\overline I_{\ae}^{\rm on}
=v^2I_2[q_1]
+v^4\left(I_4[q_1]+\delta I_2[q_1;q_3]\right)
+O(v^6).
\]

The first variation is

\[
\delta I_2[q_1;q_3]
=\int dR\,q_3\,\mathcal E[q_1]
+\left[\Pi_{q_1}\cdot q_3\right]_0^\infty.
\]

The Euler term vanishes because `q1` solves the finite-C `L2` equation. Smooth-center regularity removes the inner boundary, and the residual profile has `q3(infinity)=0` because the complete `gamma v` boundary normalization was already factored out. Therefore

\[
\boxed{\delta I_2[q_1;q_3]=0.}
\]

No `q3` closure or fitted coefficient is needed for the mass response. A direct `v3` solution remains useful only as an independent asymptotic check.

## Parent finite-C coefficients

With `Rstar=1` and `M=C/G` at `p=0`, the executable normalization is

\[
\boxed{
f_{\rm parent}=-\frac{I_2[q_1]}{8\pi\mathcal C},
\qquad
\kappa_{4,{\rm parent}}=
\frac{I_4[q_1]}{16\pi\mathcal C}.
}
\]

The independent second response is

\[
\boxed{g_{\rm parent}=3f_{\rm parent}+8\kappa_{4,{\rm parent}}.}
\]

The small-compactness limits reproduce checkpoint 4867:

\[
f_{\rm parent}
=\frac{10Cr(3r+11)}{21(1+r)}+O(C^2),
\]

\[
\kappa_{4,{\rm parent}}
=-\frac{Cr(27r^2+57r+98)}{21(1+r)}+O(C^2).
\]

Thus the finite-background result is a resummation of the same parent action, not a phenomenological interpolation.

## Charge split

Foster's conserved-energy split remains

\[
Q_4=E_{{\rm ADM},4}+E_{\ae,4}.
\]

Checkpoint 4868 introduced

\[
D_4=E_{{\rm ADM},4}-B_4,
\qquad Q_4=B_4+E_{\ae,4}+D_4.
\]

The stationary-mass theorem gives `Q4=B4` at first order in `p`, so

\[
\boxed{D_4=-E_{\ae,4}.}
\]

At `r=1/3,C=0.3`,

```text
B4/M       = -0.15842314;
E_aether4/M= -0.18918470;
E_ADM4/M   = +0.03076156;
D4/M       = +0.18918470.
```

`D4` is therefore a derived charge-partition term, not an independent response parameter. The broad interval from checkpoint 4868 is superseded inside this parent branch.

## Finite-corridor scan

The numerical grid uses collocation residuals at or below `1.0e-7`, solves at outer radii `100` and `200`, and removes the leading `1/Rmax` error by Richardson extrapolation. The core grid is

```text
r = 1/30, 1/12, 1/6, 1/4, 1/3;
C = 0.03, 0.10, 0.20, 0.30.
```

Six additional rows refine `r=1/3` across `C=0.125..0.275`. The largest sampled quartic magnitude is

\[
|\kappa_4|=0.15842317
\]

at `r=1/3,C=0.3`. The largest sampled second-response magnitude is `0.46284` near `r=1/3,C=0.2`; the conservative envelope `0.47` covers the refined rows.

Using `p_uniform=1.3928203230e-6`,

\[
p_{\rm uniform}|\kappa_4|<2.22\times10^{-7},
\qquad
p_{\rm uniform}|g|<6.55\times10^{-7}.
\]

The inherited sufficient boxes are not approached.

## Remaining external gate

The stationary theorem closes the mass accounting of the selected parent correspondence action. It does not erase checkpoint 4869's independent discrepancy:

\[
4.94<a_3^{\rm parent}<5.00,
\qquad
a_3^{\rm Gupta}=10.8375176022.
\]

Because the two calculations agree through `C2`, the conflict is treated as a localized source/convention audit rather than evidence for a free ADM completion. The finite-C parent `f`, `kappa4`, and `g` remain private nonclaim until a full coupled first-order solve or source-level `C3` rederivation arbitrates the branch.

## Decision

Within the selected public correspondence action and to first order in `p`, finite-compactness `kappa4` and `g` are derived and comfortably satisfy the direct binary sufficient windows. The next work is not another completion parameter: it is an independent `v3,l=1` asymptotic extraction plus a source-level arbitration of the `C3` first-sensitivity conflict.

Next: `4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-C3-arbitration.md`.

Sources: [Yagi et al. 2013](https://arxiv.org/abs/1311.7144); [Foster 2005](https://arxiv.org/abs/gr-qc/0509121); [Eling 2005](https://arxiv.org/abs/gr-qc/0507059); [Gupta et al. 2021](https://arxiv.org/abs/2104.04596).
