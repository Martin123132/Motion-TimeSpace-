# 4908 - Microscopic metric three-point vertex and Weyl-cubic matching

Marker: `MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908`

## Decision

This checkpoint performs the microscopic calculation selected by 4907. It
does not return another galaxy closure or merely relabel an unknown
coefficient.

The public-metric coupling of the printed motion scalar has a nonzero
one-graviton--two-scalar vertex and satisfies the exact gravitational Ward
identity. The complete one-loop metric three-point functional is the required
triangle-plus-seagull combination. For a smooth heavy real scalar its
parity-even Weyl-cubic coefficient is

\[
\zeta_{\psi}^{(1)}
=\frac{1}{30240(4\pi)^2m_\psi^2}
\]

before the finite-cutoff weight. Thus the route does not vanish because the
metric vertex is absent.

The printed MTS potential creates a different and sharper result. With

\[
V(\psi)=\frac{3\lambda}{4}|\psi|^{4/3},
\]

the only stable classical vacuum for `lambda>0` is `psi=0`, where `V''` is
not finite. A Legendre source `J` gives

\[
\bar\psi_J=(J/\lambda)^3,
\qquad
m_J^2=\frac{\lambda^3}{3J^2},
\]

and therefore the source-regularized Hessian contribution is

\[
\boxed{
\zeta_{\psi,J}^{(1)}
=\frac{N_\psi J^2}{10080(4\pi)^2\lambda^3}
\exp\!\left[-\frac{\lambda^3}
{3J^2\Lambda_{\rm UV}^2}\right].
}
\]

Its formal `J -> 0` limit is exactly zero, with or without first removing
the proper-time cutoff. However, the scalar self-interactions diverge in the
same limit. The Gaussian expansion is therefore uncontrolled there, so this
is a **one-loop Hessian-sector zero limit**, not an all-orders theorem that
the interacting scalar contributes nothing.

An exact rescaling makes the remaining problem much smaller. Defining

\[
\mu=\lambda^{3/8},\qquad x=y/\mu,\qquad\psi=\mu\phi,
\]

removes `lambda` from the dimensionless scalar action. A properly defined
nonperturbative scalar sector must consequently have

\[
m_{\rm gap}=c_m\mu,
\qquad
\boxed{\zeta_{\psi,\rm NP}=c_6\lambda^{-3/4}}.
\]

The whole scalar question is reduced to the dimensionless mass-gap constant
`c_m` and stress-three-point matching constant `c_6`, rather than an arbitrary
function. Neither is calculated by the existing corpus measure.

The active decision remains

\[
\boxed{\Gamma_{\rm MTS,res}=0.}
\]

This is not a claim that the physical total Weyl-cubic coefficient is zero.
It means no controlled nonzero coefficient has passed the action-entry gate.

## 1. Parent slice actually being varied

Checkpoint 4904 fixes the active infrared fields to the public metric and the
Standard Model. The microscopic variables `(psi_r,psi_a,X)` have been
integrated into matching data. The corresponding conservative scalar test is
therefore the covariant Hessian of one physical motion scalar, not two
independent `r/a` particles.

The printed term

\[
-\gamma\psi\partial_t\psi
=-\frac{\gamma}{2}\partial_t(\psi^2)
\]

is a boundary term for constant `gamma`. It neither changes the bulk Hessian
nor generates a gravitational threshold. The repaired Schwinger--Keldysh
action supplies damping, but closed-time-path normalization obeys

\[
\Gamma_{\rm SK}[g,g]=0.
\]

It cannot be read as two Euclidean scalar determinants. A conservative local
Weyl coefficient must be matched in a specified closed completion.

For the best-case covariant conservative scalar branch,

\[
S_\psi=-\frac12\int d^4x\sqrt{-g}
\left[(\nabla\psi)^2+2V(\psi)+\xi_\psi R\psi^2\right],
\]

and a constant flat background has

\[
\mathcal D_\psi=-\Box+V''(\bar\psi).
\]

The core files correspond to no printed nonminimal curvature term. On the
Ricci-flat Weyl-cubic projection, the displayed scalar coefficient is in any
case independent of such an `R psi^2` term.

## 2. Exact cusp-Hessian calculation

For either sign away from zero,

\[
V'(\psi)=\lambda\,\operatorname{sgn}(\psi)|\psi|^{1/3},
\]

\[
V''(\psi)=\frac{\lambda}{3}|\psi|^{-2/3}.
\]

The complete classical branch split is:

| branch | result |
|---|---|
| `lambda>0` | bounded potential, unique vacuum `psi=0`, no finite Gaussian Hessian |
| `lambda=0` | massless scalar; local `1/m^2` derivative expansion invalid and response is nonlocal |
| `lambda<0` | potential unbounded below; no stable vacuum |

Introduce an auxiliary homogeneous source through `V-J psi`. For `J>0`,

\[
V'(\bar\psi_J)=J
\quad\Longrightarrow\quad
\bar\psi_J=(J/\lambda)^3.
\]

The first fluctuation couplings are then

\[
m_J^2=V''(\bar\psi_J)=\frac{\lambda^3}{3J^2},
\]

\[
g_{3,J}=V'''(\bar\psi_J)
=-\frac{2\lambda^6}{9J^5},
\qquad
g_{4,J}=V''''(\bar\psi_J)
=\frac{10\lambda^9}{27J^8}.
\]

This is an explicit Hessian and interaction calculation. A nonzero
`bar psi` without `J` would not solve the parent vacuum equation and would
amount to inserting an environmental background by hand.

## 3. Scalar--metric vertex and Ward identity

Use

\[
g_{\mu\nu}=\eta_{\mu\nu}+M_R^{-1}h_{\mu\nu}.
\]

With the overall factor `-i/(2 M_R)` stripped, the one-graviton--two-scalar
vertex is

\[
\boxed{
V_{\mu\nu}(p',p)
=p'_\mu p_\nu+p'_\nu p_\mu
-\eta_{\mu\nu}(p'\!\cdot p-m_J^2).
}
\]

For `q=p'-p`, direct contraction gives

\[
\boxed{
q^\mu V_{\mu\nu}
=p_\nu\bigl(p'^2-m_J^2\bigr)
-p'_\nu\bigl(p^2-m_J^2\bigr).
}
\]

This is the scalar gravitational Ward identity. It vanishes between on-shell
scalar legs. The executable tensor calculation returns four exact zeros and
therefore confirms that the metric vertex is present and consistently
Hilbert-coupled.

## 4. Exact induced metric three-point functional

Let

\[
\Gamma_\psi[g]=\frac12\operatorname{Tr}\log\mathcal D[g],
\qquad G=\mathcal D^{-1},
\]

and write `D_i`, `D_ij`, and `D_123` for metric variations. The complete
third variation is

\[
\boxed{
\begin{aligned}
\delta_1\delta_2\delta_3\Gamma_\psi
=\frac12\operatorname{Tr}\big[&
GD_{123}
-GD_1GD_{23}-GD_2GD_{13}-GD_3GD_{12}\\
&+GD_1GD_2GD_3+GD_1GD_3GD_2
\big].
\end{aligned}}
\]

The first term is the three-metric seagull, the next three are mixed
two-plus-one insertions, and the final two are the scalar triangle
orientations. Keeping only the triangle would violate the Diff Ward identity.

For one commuting deformation, the generator verifies

\[
\frac{d^3}{dt^3}\log D(t)\bigg|_0
=\frac{D_3}{D_0}
-3\frac{D_1D_2}{D_0^2}
+2\frac{D_1^3}{D_0^3}.
\]

## 5. Weyl-cubic projection

After the flat-saddle volume term, Einstein stiffness and four-derivative
matching are separated, the first local on-shell pure-gravity projection is

\[
\mathcal O_+
=C_{\mu\nu}{}^{\rho\sigma}
 C_{\rho\sigma}{}^{\alpha\beta}
 C_{\alpha\beta}{}^{\mu\nu}.
\]

For one smooth massive real scalar, the source-backed heat-kernel matching is

\[
\boxed{
\zeta_+^{(s)}
=\frac{e^{-m^2/\Lambda_{\rm UV}^2}}
{30240(4\pi)^2m^2}.
}
\]

The parity-odd scalar threshold is exactly zero. A complex scalar would count
as two real scalar determinants, but the primitive corpus still has a
real/complex normalization conflict; Schwinger--Keldysh doubling does not
resolve it.

Substitution of the exact sourced Hessian gives

\[
\zeta_{+,J}^{(\psi)}
=\frac{N_\psi J^2}{10080(4\pi)^2\lambda^3}
e^{-\lambda^3/(3J^2\Lambda_{\rm UV}^2)}.
\]

Both orders of limits give

\[
\lim_{J\to0^+}\zeta_{+,J}^{(\psi)}=0,
\qquad
\lim_{J\to0^+}\lim_{\Lambda_{\rm UV}\to\infty}
\zeta_{+,J}^{(\psi)}=0.
\]

This is the exact formal answer from the existing **Hessian**.

## 6. Why that zero is not promoted to an all-orders theorem

Set

\[
\mu=\lambda^{3/8},
\qquad
j=J/\mu^3.
\]

Then

\[
\frac{\bar\psi_J}{\mu}=j^3,
\qquad
\frac{m_J}{\mu}=\frac1{\sqrt3|j|},
\]

but the dimensionless interaction controls are

\[
\boxed{
\left|\frac{g_{3,J}}{m_J}\right|
=\frac{2\sqrt3}{9|j|^4},
\qquad
|g_{4,J}|=\frac{10}{27|j|^8}.
}
\]

At `j=1` both are below one. At `j=0.5`, they are `6.1584` and
`94.8148`; they then diverge as the vacuum is approached. The formal
one-loop coefficient falls as `j^2`, but the expansion producing it loses
control.

Therefore:

```text
one-loop Hessian-sector vacuum limit = zero;
controlled all-order scalar zero     = not proved;
nonzero Gaussian coefficient         = requires an externally sourced background;
physical interacting coefficient     = nonperturbative stress-three-point problem.
```

This distinction prevents both opposite errors: claiming a nonzero MTS
prediction from an arbitrary background, or declaring the full interacting
sector identically zero from an uncontrolled saddle.

## 7. Exact nonperturbative reduction

In four dimensions,

\[
[\psi]=1,
\qquad
[\lambda]=\frac83.
\]

The change of variables

\[
x^\mu=y^\mu/\mu,
\qquad
\psi=\mu\phi,
\qquad
\mu=\lambda^{3/8}
\]

gives

\[
S_\psi
=\int d^4y\left[
\frac12(\partial\phi)^2
+\frac34|\phi|^{4/3}
\right]
\]

before regulator and measure terms. Hence, once a renormalized measure and
continuum prescription exist, dimensional analysis fixes

\[
m_{\rm gap}=c_m\lambda^{3/8},
\qquad
\zeta_{\psi,\rm NP}=c_6\lambda^{-3/4}.
\]

This is a derivation, not a placeholder list: an apparently functional
matching problem is reduced to two dimensionless constants. The next stage
must calculate them from the scalar two-point and stress three-point
functions rather than fit them to a gravitational target.

## 8. Total coefficient ownership

The novel parity-even coefficient has the owner equation

\[
\boxed{
\zeta_{+,\rm MTS}
=\zeta_{+,b}
+N_\psi c_6\lambda^{-3/4}
+\zeta_{+,X}
+\zeta_{+,\mathcal H+gh}.
}
\]

Ordinary Standard-Model thresholds are known-physics contributions and are
not relabelled as novel MTS predictions. The present parent does not jointly
fix:

- the real/complex physical motion-field count;
- the renormalized nonanalytic scalar measure and `c_6`;
- the closed-bath spectrum and curvature couplings;
- the integrated metric/ghost six-derivative matching;
- the Wilsonian boundary value `zeta_+,b`.

Diff symmetry permits `O_+`; it does not force its boundary coefficient to
zero. Consequently the total physical coefficient is not set to zero. The
active residual slot remains zero because no value is promoted.

## 9. Local GR, Newton and Maxwell gates

Around flat space,

\[
C[h]=M_R^{-1}C^{(1)}[h]+O(h^2),
\]

so

\[
\int\sqrt{-g}\,C^3
=M_R^{-3}\int(C^{(1)}[h])^3+O(h^4).
\]

The executable expansion gives

\[
\delta\int C^3\big|_{h=0}=0,
\qquad
\delta^2\int C^3\big|_{h=0}=0,
\qquad
\delta^3\int C^3\big|_{h=0}\ne0.
\]

Therefore a Weyl-cubic residual:

- does not change the flat graviton propagator or massless spin-2 residue;
- does not alter linear Newton exchange or recalibrate `G_N`;
- first changes nonlinear/strong metric response;
- has vertex scaling `Gamma_hhh,C3 ~ zeta q^6/M_R^3`;
- is small relative to the Einstein vertex when

  \[
  \boxed{\epsilon_3(q)=|\zeta|q^4/M_R^2\ll1.}
  \]

The operator is pure metric. Fixed-metric MTS/SM factorization still gives no
direct MTS `F^2 C` threshold. Minimal Maxwell propagation, electromagnetic
Hilbert stress and the Poynting vector therefore remain on the same public
metric. No local-GR, Newton, WEP, clock or Maxwell defect is introduced while
the residual is inactive.

## 10. Arbitration

```text
MICROSCOPIC METRIC VERTEX
    -> NONZERO
    -> EXACT SCALAR WARD IDENTITY PASSES

INDUCED METRIC THREE-POINT FUNCTION
    -> TRIANGLE PLUS ALL SEAGULL TERMS DERIVED
    -> PARITY-ODD SCALAR THRESHOLD EXACTLY ZERO

PRINTED n=4/3 MOTION POTENTIAL
    -> UNIQUE STABLE VACUUM IS A NON-C2 CUSP
    -> SOURCE-REGULATED HESSIAN DERIVED
    -> FORMAL ONE-LOOP C3 VACUUM LIMIT IS ZERO
    -> GAUSSIAN CONTROL FAILS IN THAT LIMIT

NONPERTURBATIVE CONTENT
    -> mu=lambda^(3/8)
    -> m_gap=c_m mu
    -> zeta_psi=c_6 lambda^(-3/4)
    -> c_m AND c_6 REQUIRE CALCULATION

LOCAL KNOWN LIMITS
    -> C3 HAS NO FLAT QUADRATIC HESSIAN
    -> GR PROPAGATOR, NEWTON AND MAXWELL BASELINE PRESERVED

ACTIVE Gamma_MTS,res
    -> 0
```

No GitHub action or public residual claim follows from this checkpoint.

## Next target

`4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md`

The next stage should define one regulator and renormalization prescription
for the dimensionless `|phi|^(4/3)` theory, calculate its mass gap, and obtain
the connected stress-tensor three-point projection needed for `c_6`. If a
controlled measure cannot be defined or the result remains regulator-bound,
the printed scalar is demoted as a UV matching owner rather than being given
an arbitrary Weyl coefficient.

## Sources

- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`.
- `core-mts-framework/field-theory/the-effective-field-theory-of-motion-timespace.md`.
- `post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md`.
- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`.
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`.
- `post-checkpoint-work/4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md`.
- `post-checkpoint-work/4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md`.
- `post-checkpoint-work/4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`.
- [Goon, *Heavy Fields and Gravity*](https://arxiv.org/abs/1611.02705).
- [Vassilevich, *Heat kernel expansion: user's manual*](https://arxiv.org/abs/hep-th/0306138).
- [Crossley, Glorioso and Liu, *Effective field theory of dissipative fluids*](https://arxiv.org/abs/1511.03646).
- `post-checkpoint-work/source-intake/microscopic_vertex/4908/PROVENANCE.md`.

