# 4885 - Gamma memory determinant, bath weight and induced-branch arbitration

Marker: `MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885`

Status: private derivation checkpoint; not a public claim.

## 1. Decision

This checkpoint resolves the immediate 4884 fork rather than carrying it as
another missing-input label.

1. The particle-sector `Gamma` printed in the corpus is a first-order,
   irreversible response variable. It is not an ordinary second-order UV
   scalar and cannot contribute a separate `+1/2 Tr log D` determinant.
2. The corpus separately contains a canonical covariant curvature-memory
   scalar `M`. Its quadratic Hessian supplies exactly one legitimate real
   scalar determinant if it is explicitly joined to the selected parent.
3. The 4873 closed-bath construction makes the original first-order `Gamma`
   law the controlled overdamped retarded limit of `M`; it does not create a
   second species.
4. A healthy passive bilinear bath with nonnegative microscopic curvature
   weights cannot generate the negative nonminimal coupling required by the
   4884 pure-induced three-boson branch.
5. The printed `b T M^2` coupling gives a useful infrared curvature
   correspondence only after an Einstein branch exists. Using the Einstein
   trace to generate the Einstein coefficient itself would be circular.
6. The pure-induced positive-Einstein route from 4884 is therefore demoted.
   The selected local correspondence branch is the smaller and more honest
   renormalized-Einstein EFT: one Newton coefficient is calibrated once, as
   in GR, while the universal loop residuals remain derived.

The theory is not demoted with that branch. What is removed is an unsupported
claim that the existing bath automatically predicts both the sign and size of
the Einstein term.

## 2. Corpus signature audit

The particle construction prints

```text
dGamma/dt = S[K] - mu Gamma,
S[K] = K^2/(1 + K^2/S_max).
```

This equation has one retarded pole and an arrow of time. No corresponding
second-order kinetic operator, canonical momentum or independent functional
measure is printed there. Counting it as a UV scalar would double count an IR
response coordinate.

The cosmology corpus instead contains

\[
S_M=\int d^4x\sqrt{-g}\left[
-\frac12(\nabla M)^2-\frac{a}{4}M^4+bTM^2
\right].
\]

That action has a unit kinetic residue and an ordinary scalar measure. The old
1983 parent scan did not inspect these cosmology files, so its broad
"no canonical memory action" verdict is superseded only on this narrow point.
The selected 4875 parent still does not list `M`; a same-parent join remains
an explicit theory choice rather than a historical fact silently inferred
from file proximity.

## 3. Canonical memory Hessian

The renormalizable curved-space completion is written as

\[
S_M=\int\sqrt{-g}\left[-\frac12(\nabla M)^2
-\frac12m_0^2M^2-\frac12\xi_MRM^2
-\frac{a}{4}M^4+bTM^2\right].
\]

For `M=Mbar+delta M`, the quadratic operator is

\[
\mathcal D_M=-\Box+m_0^2+3a\bar M^2-2bT+\xi_MR.
\]

Therefore

\[
\Gamma_M^{(1)}=\frac12\operatorname{Tr}\log\mathcal D_M
\]

is one real-scalar determinant. The existing printed action corresponds to
`m0=0` and `xi_M=0` before matter-background effects.

For dust, `T=-rho`, `b<0`, and `a>0`,

\[
M_*^2=\frac{2|b|\rho}{a},
\qquad
V_{,MM}(M_*)=4|b|\rho>0.
\]

This establishes a well-defined density-supported local Hessian. It does not
yet establish that the resulting scalar profile is screened outside a body.

## 4. Minimal same-parent completion and overdamped map

The smallest explicit join compatible with checkpoints 4873 and 4875 is

\[
S_{\rm join}=S_H+S_\psi+S_M+S_{\rm matter}
+\int d\Omega\left(S_{X_\Omega}
+\int d^4x\sqrt{-g}\,g_\Omega M X_\Omega\right),
\]

with the same public metric in every term. This is a candidate completion,
not a uniqueness theorem. Its purpose is to test whether the two already
printed pieces can consistently be the same physical memory sector.

After integrating the bath, the retarded homogeneous response is

\[
G_R(\omega)=\frac{1}
{\Omega_M^2-\omega^2-i\gamma_M\omega}.
\]

The time-domain equation with curvature source `J_K` is

\[
\ddot M+\gamma_M\dot M+\Omega_M^2M=J_K+\zeta.
\]

In the controlled regime where the inertial term is small,

\[
\dot M=\frac{J_K}{\gamma_M}
-\frac{\Omega_M^2}{\gamma_M}M,
\]

and the corpus law follows under

\[
\Gamma=g_MM,
\qquad
J_K=\frac{\gamma_M}{g_M}S[K],
\qquad
\mu=\frac{\Omega_M^2}{\gamma_M}.
\]

The relative transfer-function error made by dropping `omega^2` is

\[
\left|\frac{\omega^2}
{\Omega_M^2-i\gamma_M\omega}\right|.
\]

Nine probes spanning `Omega_M^2/gamma_M^2=0.1,1,10` and frequencies up to
one percent of the smaller relaxation scale remain below `10^-3` relative
error. This is an explicit low-frequency derivation of the first-order law,
not an assertion that it is fundamental at every frequency.

## 5. Passive-bath nonminimal-weight theorem

Take healthy bath operators

\[
\mathcal D_X=\Omega_X^2-\Box+\xi_XR
\]

and bilinear real couplings `g_X M X`. Integrating out `X` gives the Schur
complement

\[
\mathcal D_{\rm eff}=\mathcal D_M
-\int dX\,g_X^2\mathcal D_X^{-1}.
\]

At derivative order two,

\[
\mathcal D_X^{-1}=\Omega_X^{-2}
-\Omega_X^{-4}(-\Box+\xi_XR)+O(\partial^4),
\]

so with `w_X=g_X^2/Omega_X^4>=0`,

\[
Z_{\rm eff}=1+\int dX\,w_X,
\qquad
\xi_{\rm eff}=\frac{\xi_M+\int dX\,w_X\xi_X}
{1+\int dX\,w_X}.
\]

Hence `xi_M>=0` and every `xi_X>=0` imply `xi_eff>=0`. The required 4884
condition `xi_eff<-1/18`, including the anchor `xi_eff=-1/9`, cannot emerge
from this passive minimally/nonnegatively coupled bath. It requires a
microscopic negative curvature coefficient or a genuinely different signed
operator. The bath still derives damping; it does not derive the desired
negative curvature weight.

## 6. Why `b T M^2` does not rescue induced gravity

Off shell, `T` is an independent matter operator. The UV Hessian contains
`-2bT`; this is not an `R` coefficient in vacuum.

After an Einstein branch has already been established,

\[
T=-\overline M_{\rm Pl}^2R
\]

maps

\[
+bTM^2=-\frac12\xi_{\rm IR}RM^2,
\qquad
\xi_{\rm IR}=2b\overline M_{\rm Pl}^2.
\]

This is a valid infrared frame relation. Substituting it before deriving the
Einstein term would assume the trace equation whose coefficient the argument
was meant to generate, so it is forbidden in the pure-induced proof.

At the old `W1=1` anchor,

\[
b\overline M_{\rm Pl}^2=-\frac1{18},
\qquad
\xi_{\rm IR}=-\frac19.
\]

On the maximum sampled compact-star curvature
`Rmax=9.927914952e-9 m^-2`, the printed `m0=0`, `M=0` branch has

\[
m_{\rm eff}^2=-\frac{R}{9},
\qquad
\ell_{\rm tach}=30.109\ {\rm km},
\qquad
|m_{\rm eff}|=6.55382\times10^{-12}\ {\rm eV}.
\]

The nonzero dust minimum instead has

\[
m_*^2=\frac{2R}{9}>0,
\qquad
\ell_*=21.290\ {\rm km}.
\]

The zero branch therefore fails the prior local stability gate, while the
nonzero branch opens a real scalarization/screening problem. It cannot be
declared safe without solving the interior profile, exterior charge and
same-parent cosmological evolution.

## 7. Renormalized-Einstein fallback

The minimal explicit spectrum `complex psi + M + U(1)` with minimal scalar
curvature weights has

\[
N_s=3,
\quad N_V=1,
\quad W_0=5,
\quad W_1=-1,
\quad S_{h^2}=3,
\quad W_C=15,
\quad \frac{a_R}{a_C}=\frac13.
\]

It does not induce a positive Einstein coefficient by itself. Instead define
the renormalized local branch once:

\[
M_R^2=M_0^2+M_{\rm loop}^2
=\overline M_{\rm Pl}^2,
\]

\[
M_{\rm loop}^2=-\frac{\Lambda_{\rm UV}^2}{96\pi^2},
\qquad
M_0^2=\overline M_{\rm Pl}^2
+\frac{\Lambda_{\rm UV}^2}{96\pi^2}.
\]

This route does not predict Newton's constant. It gives it the same status as
the single measured coupling in GR and forbids arena-by-arena retuning. At
`LambdaUV/MbarPl=1`, `4pi`, and `4pi sqrt(6)`, the matched renormalized value
is exactly one in Planck units; the last point has `M0^2/MbarPl^2=2`.

The universal loop ray remains derived. Across the existing BSK24, SLY4 and
DD2 response calculation, its largest radius/tidal shifts are more than `75`
orders below the observational interval widths. Finite Wilsonian matching,
integrated-`H`/ghost thresholds and the active `M` fifth-force profile remain
open rather than being set to zero.

## 8. Arbitration

| Question | Result |
|---|---|
| Is first-order `Gamma` a UV scalar species? | No |
| Is there a canonical memory scalar in the corpus? | Yes: `M`, conditional on explicit parent join |
| Can its bath derive the first-order memory law? | Yes, in a controlled overdamped regime |
| Can a nonnegative passive bath derive `xi<-1/18`? | No |
| Can `b T M^2` non-circularly induce the Einstein term? | No |
| Does the printed anchor stay on `M=0` in compact-star curvature? | No |
| Is the 4884 pure-induced three-boson route retained? | Demoted |
| Selected local branch | Once-calibrated renormalized EH plus derived residuals |
| Is `G_N` predicted? | No |
| Is active-memory local viability proved? | No; direct scalarization/screening test required |

Checkpoint claim status:

```text
canonical M determinant identified;
Gamma overdamped map derived;
negative-xi passive-bath route rejected;
pure-induced three-boson branch demoted;
renormalized-EH fallback selected;
private nonclaim.
```

## 9. Next target

`4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md`

The next calculation must solve rather than merely name the active-`M`
problem:

1. derive the static spherical `M(r)` equation from the same action and a
   realistic matter trace;
2. solve regular-center, surface-matched profiles through the three existing
   EOS families;
3. extract scalar charge, fifth-force and compact-body sensitivity;
4. test whether the same `a,b,m0,xi_M` branch admits the required FLRW memory
   history without local/cosmological parameter switching;
5. retain the renormalized-EH local branch if screening fails and demote the
   active scalar to a phenomenological closure if no shared parameter region
   exists.

## Sources

- MTS particle memory law: `core-mts-framework/field-theory/axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md`.
- MTS canonical memory action: `cosmology/activation-cosmology/frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md`.
- MTS density-supported branch: `cosmology/activation-cosmology/cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md`.
- Closed-bath parent: `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`.
- [Crossley, Glorioso and Liu, effective field theory of dissipative fluids](https://arxiv.org/abs/1511.03646).
- [Hinterbichler and Khoury, symmetron screening comparison](https://arxiv.org/abs/1001.4525).
- [Vassilevich, heat-kernel expansion review](https://arxiv.org/abs/hep-th/0306138).

