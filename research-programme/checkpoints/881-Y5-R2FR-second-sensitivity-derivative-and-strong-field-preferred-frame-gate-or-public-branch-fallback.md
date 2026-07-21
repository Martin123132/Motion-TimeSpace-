# 4865 - Second sensitivity and strong preferred-frame gate

Marker: `SECOND_SENSITIVITY_HAT_ALPHA_4865`

Decision: `SECOND_SENSITIVITY_O_P_SCALING_DERIVED_ON_REGULAR_FINITE_R_BRANCH_CORRECTED_HAT_ALPHA_TRANSFER_EXACT_BINARY_PREFERRED_FRAME_WINDOW_NONEMPTY_NUMERIC_QUARTIC_RESPONSE_AND_SOLITARY_MAP_OPEN_PRIVATE_NONCLAIM`

## Scope

This checkpoint goes after the missing second compact-body response rather than merely listing it. It proves its small-`p` scaling on a regular compact-star branch, derives the corrected strong-field preferred-frame transfer exactly, and turns the binary-pulsar measurements into a quantitative target for the still-uncomputed coefficient.

It does not assign a numerical value to that coefficient without the required quartic boosted-star calculation. It also does not apply a solitary-pulsar spin-precession bound to a binary orbital formula.

## Sensitivity notation

Gupta et al. expand

\[
\mu(\gamma)=\widetilde m\left[1+\sigma(1-\gamma)
+\frac12\sigma'(1-\gamma)^2+\cdots\right],
\]

with

\[
\sigma=-\left.\frac{d\ln\mu}{d\ln\gamma}\right|_1,
\qquad
\sigma'=\sigma+\sigma^2+
\left.\frac{d^2\ln\mu}{d(\ln\gamma)^2}\right|_1.
\]

The 2025 Taherasghari-Will notation has the opposite sign for its first sensitivity and calls the quadratic Taylor coefficient `a_s`; direct matching gives

\[
s_A^{\rm TW}=-\sigma_A^{\rm Gupta},
\qquad a_{sA}^{\rm TW}=\sigma_A^{\prime\,\rm Gupta}.
\]

That work confirms that the quadratic response enters current compact-binary PN dynamics, but it treats the sensitivity coefficients as body inputs rather than deriving their stellar values.

## Regular-response theorem

Let `x=ln(gamma)` and let `Y` collect all gauge-fixed compact-star profile perturbations induced by a boost relative to the public flow. At fixed finite `0<r<=1/3`, the established public coefficient surface gives the reduced expansion

\[
I[p,x,Y]=I_{\rm GR}+pI_1[x,Y;r,C]+O(p^2).
\]

Assume the leading stationary problem

\[
D_YI_1[x,Y_0]=0
\]

has the required regular boundary solution and that its gauge-fixed Hessian

\[
H_{YY}=D_Y^2I_1
\]

is invertible. The implicit-function theorem then gives

\[
Y_*(x,p)=Y_0(x)+O(p),
\qquad
\ln\mu=\ln m_{\rm GR}+p h(x;r,C)+O(p^2).
\]

Therefore

\[
\boxed{\sigma=p f+O(p^2),\qquad f=-h_x(0),}
\]

and

\[
\boxed{\sigma'=p g+O(p^2),\qquad g=f+h_{xx}(0).}
\]

The second derivative is the on-shell Schur complement

\[
\boxed{
h_{xx}=I_{1,xx}-I_{1,xY}H_{YY}^{-1}I_{1,Yx}.
}
\]

This is a real derivation of the scaling and of the missing calculation. It also identifies the precise failure mode: if the compact-star Hessian develops a zero mode, `H_YY^-1` can diverge and the regular `sigma'=O(p)` conclusion fails. Vacuum mode positivity does not by itself exclude that strong-field event.

The 4864 result `s=pF+p O(C^4)` is consistent because `sigma=s/(1-s)=pF+O(p^2)+p O(C^4)`, so `f=F` through the retained compactness order.

## Corrected preferred-frame transfer

For bodies 1 and 2, write

\[
x=\frac{m_2}{m_1+m_2},\qquad y=1-x,
\qquad \sigma_A=p f_A+O(p^2),\qquad \sigma'_A=p g_A+O(p^2).
\]

Substitution into the corrected Gupta EIH coefficients gives

\[
\widehat\alpha_1=pH_1+O(p^2),
\qquad
\widehat\alpha_2=pH_2+O(p^2),
\]

where the exact leading coefficients reduce to

\[
\begin{aligned}
H_1=2\bigg[&\frac{4(1-2x)}{1+r}f_1f_2
+(5x-4)f_1+(5x-1)f_2+x^2g_1-y^2g_2\\
&+\frac{4r(1-2x)}{1+r}\bigg],
\end{aligned}
\]

\[
\begin{aligned}
H_2={}&\frac{3r^2+6r-1}{1+r}f_1f_2
+(1-3r)(f_1+f_2)+xg_1+yg_2
+\frac{r(3r-1)}{1+r}.
\end{aligned}
\]

All apparent inverse powers of the small couplings cancel. At the public endpoint `r=1/3`,

\[
H_1=2\left[3(1-2x)f_1f_2+(5x-4)f_1+(5x-1)f_2
+x^2g_1-y^2g_2+(1-2x)\right],
\]

\[
\boxed{H_2=f_1f_2+xg_1+yg_2.}
\]

The generator verifies eight independent symbolic identities, including the corrected `Q`, `R`, `H1`, and `H2` limits.

## Source-backed binary window

For PSR J1738+0333, Shao and Wex report the following CMB-preferred-frame limits:

\[
-3.5\times10^{-5}<\widehat\alpha_1<3.3\times10^{-5},
\qquad
|\widehat\alpha_2|<2.9\times10^{-4}
\]

at 95 percent confidence. The second number is the J1738-specific row; the tighter combined `1.8e-4` result assumes an approximately common strong parameter across J1738 and J1012 and is retained only as a conditional row.

Applying these rows to MTS also assumes that the asymptotic public flow is the cosmological/CMB rest frame. That is the natural current branch identification, but it remains an explicit FLRW-to-local matching condition rather than a hidden premise.

At the established `p_uniform=1.3928203230e-6`, the direct J1738 measurements allow

\[
|H_1|\le23.6929,
\qquad |H_2|\le208.211.
\]

Using `0<=f_NS<=Fmax`, the white-dwarf envelope from 4864, every `0<r<=1/3`, and no cancellation between independent terms gives the sufficient leading-order box

\[
\boxed{|g_1|,|g_2|\le11.7108.}
\]

Inflating both retained first-response envelopes by three percent still gives

\[
\boxed{|g_1|,|g_2|\le11.6490.}
\]

This is not a prediction that `g` lies in that box. It is a concrete target: a future quartic stellar derivation only needs a finite coefficient of order ten or below to leave the entire current public `p,r` corridor inside the direct binary preferred-frame limits without cancellation.

For the nominal J1738 compactness at `r=1/3`,

```text
f_NS = 0.2242394451
f_WD = 0.0001428303
```

and three diagnostic completions give, at `p_uniform`,

```text
g_A=0       : hat_alpha1=1.7055e-8, hat_alpha2=4.4610e-11
g_A=f_A     : hat_alpha1=2.4339e-8, hat_alpha2=3.4671e-8
g_A=3 f_A   : hat_alpha1=3.8908e-8, hat_alpha2=1.0392e-7
```

These are smoke diagnostics, not parent predictions. All pass the direct binary rows by large margins. The 108-point `p-r-C-response` grid also passes.

More generally, for every finite `H1,H2`, these binary bounds alone leave a nonempty positive asymptotic interval

\[
p<\min\left[p_{\rm uniform},
\frac{3.3\times10^{-5}}{|H_1|},
\frac{2.9\times10^{-4}}{|H_2|}\right].
\]

The 4863 cutoff floor must still be intersected separately; the explicit `p_uniform` response box above already does so within the established viable branch rather than relying on arbitrarily tiny `p`.

## Solitary-pulsar quarantine

Shao et al. obtain

\[
|\widehat\alpha_2|<1.6\times10^{-9}
\]

from solitary-pulsar spin precession. At `p_uniform`, this corresponds numerically to a coefficient scale `0.00114875`, far tighter than the binary rows. It is not applied here because the observable is a one-body spin-precession map, whereas `H2` above is a two-body orbital EIH combination. Equating them without deriving the public-frame one-body map would manufacture a constraint.

## Decision

The missing second sensitivity is no longer an unstructured unknown. Its `O(p)` scaling is derived under an explicit regularity condition; its exact contribution to both corrected strong preferred-frame parameters is derived; and direct binary data leave a broad finite-response window.

The public branch is therefore retained. It is not promoted. The decisive missing object is now the quartic boosted-star Schur complement `I1_xx-I1_xY H_YY^-1 I1_Yx`. Computing it will either produce `g`, bound it, or expose the compact-star zero mode that rejects this route.

The 2025 direct radiation-reaction calculation also reports disagreements with older far-zone flux formulas. Consequently, the 4864 dipole result remains a smoke gate until those conventions are reconciled; the conservative preferred-frame result here does not depend on that flux dispute.

Next: `4866-Y5-R2FR-quartic-boost-compact-star-Hessian-and-sigma-prime-coefficient-or-finite-response-fallback.md`.

Sources: [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Shao and Wex 2012](https://arxiv.org/abs/1209.4503); [Shao et al. 2013](https://arxiv.org/abs/1307.2552); [Taherasghari and Will 2025](https://arxiv.org/abs/2506.03843); [Foster 2007](https://arxiv.org/abs/0706.0704).
