# 4866 - Quartic boost hierarchy and leading compact-star kernel gate

Marker: `QUARTIC_BOOST_HIERARCHY_KERNEL_4866`

Decision: `QUARTIC_MASS_RESPONSE_ISOLATED_VELOCITY_HARMONIC_HIERARCHY_DERIVED_LEADING_C_L1_QUOTIENT_KERNEL_TRIVIAL_FINITE_KAPPA4_BOUND_NONEMPTY_NUMERIC_PARENT_VALUE_OPEN_PRIVATE_NONCLAIM`

## Scope

This checkpoint attempts the missing compact-star derivation rather than assigning a value to the second sensitivity. It does four things:

1. isolates the genuinely dynamical quartic mass response from special-relativistic gamma kinematics;
2. derives the velocity and angular-harmonic hierarchy that a boosted-star calculation must obey;
3. proves that the physical leading-compactness `l=1` homogeneous kernel is trivial after fixing the asymptotic boost normalization;
4. converts the preferred-frame measurements into a bound on the genuine quartic coefficient.

It does not solve the finite-compactness second- and third-order boosted-star equations. The result therefore narrows the missing calculation and removes one possible leading-order obstruction, but it does not yet derive a numerical parent value for `sigma'` or claim local-GR closure.

## Exact quartic mass response

Use the Gupta/Foster compact-body mass convention

\[
\mu(\gamma)=m\left[1+\sigma(1-\gamma)
+\frac12\sigma'(1-\gamma)^2+O((1-\gamma)^3)\right],
\qquad \gamma=(1-v^2)^{-1/2}.
\]

Since

\[
\gamma=1+\frac12v^2+\frac38v^4+O(v^6),
\]

direct expansion gives

\[
\boxed{
\frac{\mu}{m}=1-\frac12\sigma v^2
+\frac18(\sigma'-3\sigma)v^4+O(v^6).
}
\]

The corresponding point-particle Lagrangian is

\[
\boxed{
\frac{L}{m}=-1+\frac12(1+\sigma)v^2
+\frac18(1+\sigma-\sigma')v^4+O(v^6).
}
\]

On the regular public branch, write

\[
\sigma=p f+O(p^2),\qquad \sigma'=p g+O(p^2).
\]

The coefficient `g` contains a kinematic contribution because the quadratic response is defined using `gamma`, not directly using `v`. Define the independent quartic mass response

\[
\boxed{\kappa_4\equiv\frac{g-3f}{8},\qquad g=3f+8\kappa_4.}
\]

Then

\[
\boxed{
\frac{\mu}{m}=1-\frac12p f v^2+p\kappa_4v^4
+O(v^6,p^2).
}
\]

Thus `g=3f` means `kappa4=0`: it is the special case in which the mass function has no independent `p v4` coefficient. It is a useful diagnostic closure, not a result derived from the parent action.

## Mandatory velocity-harmonic hierarchy

For an axisymmetric boost, let `P_l(cos theta)` denote the Legendre harmonics. The angular products obey

\[
P_1^2=\frac13P_0+\frac23P_2,
\]

\[
P_1P_2=\frac25P_1+\frac35P_3,
\qquad
P_1^3=\frac35P_1+\frac25P_3.
\]

Consequently the perturbation hierarchy is

```text
v^0 : l=0       spherical background;
v^1 : l=1       first boost response and sigma;
v^2 : l=0,2     quadratic backreaction;
v^3 : l=1,3     quartic mass response and sigma'.
```

The desired third-order equation has the schematic form

\[
\boxed{
\mathcal L_1\Phi_{3,1}
=J_{3,1}[\Phi_0,\Phi_{1,1},\Phi_{2,0},\Phi_{2,2}].
}
\]

Its source includes both cubic first-order terms and products of the first-order field with the second-order monopole and quadrupole. Therefore an `O(v3),l=1` calculation that skips the `O(v2),l=0,2` solve cannot determine `kappa4`; it silently imposes a closure on the missing backreaction.

The published compact-star calculation used here supplies the `O(v0)` and `O(v1)` systems. It does not supply the required `O(v2)` and `O(v3)` systems, so those equations must be generated from the public action rather than inferred from the existing first-sensitivity formula.

## Leading-compactness physical-kernel proof

At leading compactness, the homogeneous `l=1` radial equation for the independent `W` mode is

\[
W''-\frac{2}{r^2}W=0.
\]

Center regularity and asymptotic decay select

\[
W_{\rm in}=D r^2,\qquad W_{\rm out}=\frac{A}{r}.
\]

Continuity of `W` and `W'` at the stellar radius `R` gives

\[
\begin{pmatrix}
R^2&-R^{-1}\\
2R&R^{-2}
\end{pmatrix}
\begin{pmatrix}D\\A\end{pmatrix}=0,
\qquad
\det=3.
\]

Hence `D=A=0`. Equivalently, multiplying the radial equation by `W`, integrating over the matched interior and exterior domains, and using the boundary and matching conditions gives

\[
\boxed{
\int_0^\infty\left[(W')^2+\frac{2W^2}{r^2}\right]dr=0,
}
\]

which also forces `W=0`.

For the remaining homogeneous first-order fields, set `D_SK=K-S`. Their difference equation is

\[
rD_{SK}'+3D_{SK}=0,
\qquad D_{SK}=\frac{c}{r^3}.
\]

Center regularity forces `c=0`. The remaining common `S=K=C0` solution changes the asymptotic boost normalization; fixing the prescribed public-frame boost removes it. Therefore

\[
\boxed{
\ker(\mathcal L_1)/\{\text{asymptotic boost normalization}\}=\{0\}
\quad\text{at leading compactness}.
}
\]

This proves uniqueness of the sourced leading-compactness `l=1` solve once the lower-order source is supplied. It does not prove that the full compact-star Hessian stays invertible for every `C<=0.3`. A finite-compactness determinant or direct boundary-value solve is still required to exclude a zero crossing.

## Compactness regularity already owned

The first-response coefficients established in checkpoint 4864 have denominators

\[
21(1+r),\qquad 63063(1+r)^2,
\qquad 112567455(1+r)^3,
\]

through `C3`, and the complete first-response factor obeys

\[
\lim_{r\to0^+}F(p,r,C)=0.
\]

The symbolic audit therefore finds no `p` pole or `r` pole in the retained first-response compactness series. This is evidence that the public co-scaling limit is regular through that order. It is not a bound on the missing quartic-response remainder and is not substituted for the finite-compactness Hessian test.

## Preferred-frame transfer in the quartic basis

Substitute

\[
g_A=3f_A+8\kappa_{4A}
\]

into the exact checkpoint-4865 transfer. Then

\[
\widehat\alpha_1=pH_1(f_A,3f_A+8\kappa_{4A})+O(p^2),
\]

\[
\widehat\alpha_2=pH_2(f_A,3f_A+8\kappa_{4A})+O(p^2).
\]

At the public endpoint `r=1/3`, the second coefficient becomes

\[
\boxed{
H_2=f_1f_2+3(xf_1+yf_2)
+8(x\kappa_{41}+y\kappa_{42}).
}
\]

Using the direct J1738 binary rows, the complete `0<r<=1/3` corridor, the established neutron-star and white-dwarf first-response envelopes, a three-percent first-response stress, and no cancellation between the two body coefficients gives

\[
\boxed{|\kappa_{41}|,|\kappa_{42}|\le1.4532678437.}
\]

The `alpha1` row controls this intersection. The corresponding `alpha2`-only box is about `25.9351`. At `p_uniform`, the maximum direct quartic coefficient in the mass expansion is

\[
\boxed{p_{\rm uniform}|\kappa_4|\le2.0241409875\times10^{-6}.}
\]

All 216 corners of the stressed `p-r-C-kappa4` audit pass the direct binary preferred-frame rows. This is a sufficient observational window, not a prediction that the parent theory produces a coefficient inside it. Applying these rows also retains the checkpoint-4865 requirement that the asymptotic public flow match the CMB preferred frame.

## Decision

The quartic target is now sharper than the previous generic Schur complement. The actual unknown is the independent `p v4` mass coefficient `kappa4`. Its calculation requires the second-order monopole/quadrupole backreaction before the third-order dipole solve. The physical leading-compactness dipole operator has no homogeneous zero mode, so the route does not fail at its first operator gate.

The public branch remains alive under the finite sufficient box above. It is not promoted because neither the finite-compactness determinant nor the numerical parent value of `kappa4` has been derived. The next derivation must build the `O(v2),l=0,2` equations from the public action, solve their regular/asymptotic boundary problem, and use them in the `O(v3),l=1` source.

Next: `4867-Y5-R2FR-second-order-boost-l0-l2-star-equations-and-third-order-l1-source-or-finite-kappa4-fallback.md`.

Sources: [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Foster 2007](https://arxiv.org/abs/0706.0704); [Will 2018](https://arxiv.org/abs/1801.08999); [Taherasghari and Will 2025](https://arxiv.org/abs/2506.03843); [Foster 2006](https://arxiv.org/abs/gr-qc/0602004).
