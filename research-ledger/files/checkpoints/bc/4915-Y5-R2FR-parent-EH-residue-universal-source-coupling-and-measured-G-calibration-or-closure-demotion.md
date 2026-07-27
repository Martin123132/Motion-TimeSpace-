# 4915 - Parent EH residue, universal source coupling and measured-G ownership

Marker: `MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915`

## Decision

This checkpoint closes a real normalization gap without repeating checkpoint
4898.

Checkpoint 4898 proved that the present microscopic matching problem cannot
predict the numerical value of Newton's constant: one observation constrains
only the renormalized Einstein stiffness. The question left by checkpoint 4914
is different. It asks whether the Einstein kinetic residue and the matter
source vertex were inserted independently.

They are not independent when both are obtained from the one functional

\[
\boxed{
\Gamma_{\rm IR}[g,\Phi]
=\frac{M_R^2}{2}\int d^4x\sqrt{-g}
(R-2\Lambda_{\rm cal})+S_{\rm matter}[g,\Phi].
}
\]

The exact result is

```text
one parent metric variation          = PASS
arbitrary graviton normalization     = CANCELS FROM EXCHANGE
independent baseline source factor   = ABSENT
universal species coupling           = SOFT/DIFF CONSISTENCY
Newton strength                      = ONE GLOBAL G CALIBRATION
microscopic numerical prediction G  = OPEN, NOT CLAIMED
strict-scalar origin of matter map   = OPEN PRIMITIVE BRIDGE
```

Thus the selected integrated-`H` parent has a conditionally complete local-GR
source normalization. It does not yet derive the parent matter pullback from
the original fixed-background scalar corpus, and it does not predict `G_N`.

## 1. One variation, not two inserted equations

Define the physical Hilbert source by

\[
T_{\mu\nu}
=-\frac{2}{\sqrt{-g}}
\frac{\delta S_{\rm matter}}{\delta g^{\mu\nu}}.
\]

After the required gravitational boundary term is included, the bulk
variation is

\[
\delta\Gamma_{\rm IR}
=\frac12\int d^4x\sqrt{-g}
\left[
M_R^2(G_{\mu\nu}+\Lambda_{\rm cal}g_{\mu\nu})
-T_{\mu\nu}
\right]\delta g^{\mu\nu}.
\]

The metric equation is therefore

\[
\boxed{
M_R^2(G_{\mu\nu}+\Lambda_{\rm cal}g_{\mu\nu})
=T_{\mu\nu}.
}
\]

There is no second source normalization in this equation. The coefficient of
the source is fixed by the definition of the stress tensor of the same matter
action that supplies inertial clocks, rods and masses.

## 2. Field-normalization-invariant residue theorem

The intermediate graviton field can be normalized arbitrarily. Write

\[
g_{\mu\nu}=\eta_{\mu\nu}+a h_{\mu\nu},
\qquad a\ne0.
\]

On the conserved transverse source sector define

\[
K=P^{(2)}-2P^{(0s)},
\qquad
K^{-1}=P^{(2)}-\frac12P^{(0s)}.
\]

Using the convention in which `a=2/M_R` gives a canonically normalized
graviton, the quadratic Hessian, propagator and linear source vertex are

\[
\Gamma^{(2)}_a
=\frac{M_R^2a^2}{4}q^2K,
\]

\[
D_a(q)
=\frac{4i}{M_R^2a^2(q^2+i0)}K^{-1},
\]

and

\[
S_{\rm matter}[\eta+ah,\Phi]
=S_{\rm matter}[\eta,\Phi]
+\frac{a}{2}\int d^4x\,h_{\mu\nu}T^{\mu\nu}
+O(h^2).
\]

Consequently the two-vertex exchange kernel is exactly

\[
\boxed{
\left(\frac a2\right)^2D_a(q)
=\frac{i}{M_R^2(q^2+i0)}
\left(P^{(2)}-\frac12P^{(0s)}\right).
}
\]

The arbitrary scale `a` cancels. The physical source exchange is

\[
\boxed{
\mathcal A(q)
=\frac{i}{M_R^2(q^2+i0)}
\left(T_{\mu\nu}T^{\mu\nu}-\frac12T^2\right),
}
\]

up to the usual overall sign and external-source conventions. The same
`M_R` owns the graviton self-interaction, pole residue and source exchange.

Two internally consistent conventions are useful:

| perturbation scale | Hessian | source vertex | propagator |
|---|---|---|---|
| `a=2/M_R` | `q^2 K` | `1/M_R` | `i K^-1/q^2` |
| `a=1` | `M_R^2 q^2 K/4` | `1/2` | `4i K^-1/(M_R^2 q^2)` |

Neither convention introduces a physical extra coupling.

## 3. Repair of the checkpoint-4875 notation

Checkpoint 4875 displayed

\[
g_{\mu\nu}=\eta_{\mu\nu}+h_{\mu\nu}/M_*
\]

and later displayed an unrescaled Hessian proportional to `M_*^2 q^2` for the
same symbol `h`. Those expressions use two different intermediate field
normalizations. Taken literally together, they are not a normalization-complete
derivation.

At `a=1/M_R`, the consistent entries in the convention above are

\[
\Gamma^{(2)}=\frac14q^2K,
\qquad
V_T=\frac1{2M_R}.
\]

The physical exchange amplitude and the relation
`G_N=(8 pi M_R^2)^-1` stated by checkpoint 4875 remain correct because they are
normalization invariant. Checkpoint 4915 supersedes only its intermediate
field notation, not its pole or Newton conclusions.

## 4. Why an independent source coefficient is not allowed

Suppose one writes only at linear order

\[
\Delta S_{\rm linear}
=\frac{c_s}{M_R}\int h_{\mu\nu}T^{\mu\nu}
\]

while retaining the same flat-space matter action. Unless `c_s=1` in the
canonical convention, this term is not the expansion of the declared
`S_matter[g,Phi]`. It needs a different nonlinear completion and is a new
interaction, not a normalization choice. It may not be hidden in the active
minimal baseline.

Multiplying the entire matter action by a constant does not create a second
gravitational coupling either. The physical Hilbert tensor is then defined by
varying that multiplied action, so the metric equation still has unit
coefficient in front of the physical source. Matter wavefunction, mass and
charge normalizations must be fixed in that same action.

Nonminimal curvature operators such as `xi R phi^2`, higher-dimension matter
operators or a direct flow charge are possible residual interactions. They
must be written explicitly, matched and tested. They do not alter the theorem
for the minimally coupled two-derivative baseline.

## 5. Universal species coupling

The single metric already gives one source. Independently, the soft-graviton
condition from checkpoint 4874 supplies a consistency test. For three species,
momentum conservation and soft gauge invariance reduce to

\[
\begin{pmatrix}
1&0&-1\\
0&1&-1
\end{pmatrix}
\begin{pmatrix}\kappa_1\\\kappa_2\\\kappa_3\end{pmatrix}=0.
\]

The matrix has rank two and nullspace

\[
\operatorname{span}(1,1,1).
\]

Hence every species has the same leading coupling. This fixes equality, not
the numerical value of that common coupling. The latter remains `1/M_R` after
canonical normalization and is calibrated by `G_N`.

## 6. Newton limit

For

\[
g_{00}=-(1+2\Phi)
\]

in the weak stationary limit,

\[
G_{00}=2\nabla^2\Phi+O(\Phi^2).
\]

With `T_00=rho`, the parent equation gives

\[
\nabla^2\Phi
=\frac{\rho}{2M_R^2}
=4\pi G_N\rho,
\qquad
\boxed{G_N=\frac1{8\pi M_R^2}}.
\]

The sign of the potential solution depends on the convention for `Phi`; the
coefficient relation is invariant. The same equation gives the standard GR
PPN values `gamma=beta=1` on the already certified two-derivative metric-only
branch.

## 7. Maxwell and the Poynting source

For the same public metric,

\[
S_{\rm EM}=-\frac14\int d^4x\sqrt{-g}\,
F_{\mu\nu}F^{\mu\nu}.
\]

Its Hilbert tensor is

\[
T^{\rm EM}_{\mu\nu}
=F_{\mu\alpha}F_\nu{}^\alpha
-\frac14g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}.
\]

The symbolic calculation verifies in a local inertial frame

\[
T^{00}_{\rm EM}=\frac12(E^2+B^2),
\qquad
T^{0i}_{\rm EM}=(\mathbf E\times\mathbf B)^i,
\qquad
T^\mu{}_\mu=0.
\]

Thus the Poynting vector is already the electromagnetic momentum component of
the one Hilbert source. It acts on the public metric without a separate
Poynting-to-gravity coefficient.

## 8. Bianchi and exchange closure

The geometric identity

\[
\nabla^\mu(G_{\mu\nu}+\Lambda_{\rm cal}g_{\mu\nu})=0
\]

is compatible with the matter equation because Diff invariance of the same
functional gives

\[
\nabla^\mu T_{\mu\nu}^{\rm total}=0
\]

on all matter equations. For Maxwell plus charged matter,

\[
\nabla_\mu T_{\rm EM}^{\mu\nu}=-F^{\nu\mu}J_\mu,
\qquad
\nabla_\mu T_{\rm matter}^{\mu\nu}=+F^{\nu\mu}J_\mu.
\]

The exchange cancels in the total tensor. A one-sided flow or electromagnetic
source would violate this incidence balance and remains forbidden.

## 9. Ownership verdict

| object | status after 4915 |
|---|---|
| integrated `H` and `Diff` | explicit primitive parent field/symmetry data |
| `g(H)` reconstruction | derived and invertible in the selected branch |
| one massless spin-2 pole | conditional positive-residue result |
| equality of species couplings | derived from soft/Diff consistency |
| source vertex relative to kinetic residue | derived exactly from one functional |
| separate baseline source coefficient | absent and forbidden |
| `M_R^2` or `G_N` | one globally calibrated relevant coupling |
| microscopic numerical prediction of `G_N` | rank-deficient and open |
| `S_matter[g(H),Phi]` from the strict scalar-only corpus | not derived |
| `Gamma_MTS,res` | zero after checkpoint 4914 |

This is the correct present claim:

\[
\boxed{
\text{selected integrated-}H\text{ parent}
\Longrightarrow
\text{normalized GR source structure with one measured }G_N.
}
\]

It is not yet the stronger claim

\[
\text{original fixed-background motion scalar alone}
\Longrightarrow
\text{all of GR and its measured }G_N.
\]

The strict scalar-only composite-graviton route was already rejected at 4875.
The remaining microscopic bridge is constructive rather than numerical: write
the explicit covariantization map from the motion action and matter sectors to
the integrated-`H` parent, prove that no direct flow charge survives, or freeze
that map honestly as primitive field-theory data.

## 10. Gate result

```text
SINGLE PARENT FUNCTIONAL              = PASS
CANONICAL NORMALIZATION               = PASS
FIELD-RESCALING INVARIANCE            = PASS
SOURCE/PER-POLE RELATION              = PASS
SOFT UNIVERSALITY                     = PASS
NEWTON COEFFICIENT                    = PASS
MAXWELL/POYNTING HILBERT SOURCE       = PASS
BIANCHI/WARD COMPATIBILITY            = PASS
INDEPENDENT SOURCE COEFFICIENT        = ABSENT
ONE GLOBAL G CALIBRATION              = RETAINED
MICROSCOPIC G PREDICTION              = NOT CLAIMED
MICROSCOPIC MATTER PULLBACK           = OPEN
PUBLIC UNIFIED-THEORY CLAIM           = BLOCKED
```

No GitHub action or public claim is authorized.

## Next target

`4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md`

Construct the explicit map from the retained microscopic motion action and
Standard-Model kinetic operators to `S_parent[H,Phi]`. Prove uniqueness at the
two-derivative level under Diff, gauge symmetry and the soft theorem, including
the absence of a direct public-flow charge. If the map cannot be obtained from
the original variables, freeze it as an explicit primitive rather than
pretending that checkpoint 4915 derived its microscopic origin.

## Sources

- `post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md`
- `post-checkpoint-work/4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md`
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`
- `post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md`
- `post-checkpoint-work/4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md`
- `post-checkpoint-work/4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4915_single_functional_EH_source_residue.py`

