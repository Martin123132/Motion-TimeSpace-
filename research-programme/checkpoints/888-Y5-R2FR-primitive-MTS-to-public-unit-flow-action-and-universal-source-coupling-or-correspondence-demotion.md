# 4872 - Primitive MTS to the public unit-flow action and universal source coupling

Marker: PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872

Decision: CORE_DAMPING_AND_COVARIANT_RANK_ONE_METRIC_CLAIMS_REJECTED_INVERSE_CONNECTED_COVARIANCE_PUBLIC_METRIC_AND_LANDAU_FLOW_CANDIDATE_CONSTRUCTED_LOCAL_LORENTZ_REDUNDANCY_DERIVED_MULTIMODE_REQUIRED_UNIT_FLOW_OPERATOR_BASIS_AND_OP_DECOUPLING_DERIVED_COEFFICIENT_RATIOS_AND_UNIVERSAL_SOURCE_DESCENT_REMAIN_EFT_MATCHING_CORRESPONDENCE_DEMOTED_NOT_DISCARDED_PRIVATE_NONCLAIM

## Result

The primitive-ownership question has been attacked at the equations rather than returned as another missing-input row. Four exact results follow.

1. The term used in both core papers to generate microscopic damping is a total derivative. For constant gamma,

\[
-\gamma\psi\partial_t\psi
=-\frac{\gamma}{2}\partial_t(\psi^2),
\qquad
\frac{\delta}{\delta\psi}\int d^4x\,
(-\gamma\psi\partial_t\psi)=0.
\]

It cannot generate \(+\gamma\partial_t\psi\) in a bulk Euler equation. The advertised primitive scalar equation therefore does not follow from the advertised action.

2. The core covariant metric ansatz has the wrong rank-one sign for the retained healthy public branch. If

\[
Q_{\mu\nu}=q u_\mu u_\nu,\qquad q\ge0,
\qquad
g^{\rm core}_{\mu\nu}=\eta_{\mu\nu}+Q_{\mu\nu},
\]

then, for \(u^2=-1\) and \(0\le q<1\),

\[
(g_{\rm core}^{-1})^{\mu\nu}
=\eta^{\mu\nu}-\frac{q}{1-q}u^\mu u^\nu.
\]

Relative to the checkpoint-4861 convention

\[
\widehat g^{\mu\nu}=g^{\mu\nu}+p u^\mu u^\nu,
\]

the core ansatz gives

\[
\boxed{p_{\rm core}=-\frac{q}{1-q}\le0,}
\]

whereas the stable correspondence corridor requires \(p>0\).

3. The minimal sign-corrected primitive candidate is an inverse connected-covariance metric:

\[
\boxed{
\mathcal C^{\mu\nu}(x)
=\ell_*^2\left[
\overline{\partial^\mu\psi\,\partial^\nu\psi}
-\overline{\partial^\mu\psi}\,
 \overline{\partial^\nu\psi}
\right],
\qquad
\widehat g^{\mu\nu}=\eta^{\mu\nu}+\mathcal C^{\mu\nu}.
}
\]

For a rank-one timelike covariance \(\mathcal C^{\mu\nu}=q u^\mu u^\nu\), this gives \(p=q\ge0\),

\[
\widehat g_{\mu\nu}
=\eta_{\mu\nu}-\frac{q}{1-q}u_\mu u_\nu,
\qquad
\frac{\det\widehat g}{\det\eta}=\frac1{1-q},
\]

and preserves Lorentzian signature for \(0\le q<1\). The scale \(\ell_*\), centering, smoothing state and signature gate are compulsory; the unnormalised raw second moment in the core text is not yet a metric theorem.

4. A single deterministic scalar gradient cannot own the selected spin-1 flow sector. If

\[
u_\mu=N\partial_\mu\psi,
\]

then

\[
u\wedge du=N\,d\psi\wedge dN\wedge d\psi=0.
\]

The flow is hypersurface-orthogonal and has zero vorticity. The public correspondence branch instead has

\[
\widehat c_\omega=\widehat c_1-\widehat c_3=D>0.
\]

Therefore the selected vector branch requires a genuinely multi-directional smoothed covariance or ensemble state. It cannot be obtained by merely normalising \(d\psi\).

These results do not destroy checkpoints 4857-4871. They change their status precisely: the unit-flow action is a well-tested correspondence EFT matching layer, not yet a primitive consequence of the scalar action printed in the core corpus.

## 1. Exact primitive-action audit

The scalar Lagrangian used in the core files is

\[
\mathcal L_\psi=
\frac{(\partial_t\psi)^2}{2c^2}
-\frac{|\nabla\psi|^2}{2}
-\gamma\psi\partial_t\psi
-\frac{\lambda}{n}|\psi|^n.
\]

The Euler derivative of the gamma term vanishes because the two first-derivative contributions cancel. The resulting conservative equation is instead

\[
\frac1{c^2}\partial_t^2\psi-\nabla^2\psi
+\lambda\,\operatorname{sgn}(\psi)|\psi|^{n-1}=0
\]

away from \(\psi=0\), with no damping. For \(n=4/3\), the potential derivative is \(\lambda\operatorname{sgn}(\psi)|\psi|^{1/3}\); writing only \(\lambda|\psi|^{1/3}\) silently restricts the field to a nonnegative branch.

A local one-field, time-translation-invariant ordinary action cannot generate irreversible friction without additional degrees of freedom, a nonlocal influence functional, or a doubled/open-system variational structure. This becomes the first repair target rather than an adjustable sign.

The fixed \(\eta\) and explicit \(\partial_t\) also mean that the printed microscopic action has a preferred background chart. General covariance of the infrared action requires a further quotient statement: after coarse graining, \(\eta\) and the smoothing chart must not remain separately observable.

## 2. Connected covariance and public metric

Let a normalized smoothing kernel or state define

\[
\overline{X}(x)=\int d^4y\,W_\ell(x,y)X(y),
\qquad
\int d^4y\,W_\ell(x,y)=1.
\]

The connected moment in the boxed result removes coherent mean flow from the fluctuation covariance. The scale \(\ell_*\) supplies the dimensions needed to add the covariance to a metric. A candidate public metric exists only when:

- \(\mathcal C^{\mu\nu}\) is symmetric and transforms as a rank-two tensor;
- \(\widehat g^{\mu\nu}=\eta^{\mu\nu}+\mathcal C^{\mu\nu}\) is nondegenerate;
- \(\widehat g\) has one negative and three positive eigenvalues;
- the smoothing prescription is local on infrared scales;
- \(\eta\) and \(W_\ell\) do not survive as independently observable structures in \(\Gamma_{\rm IR}\).

The first three clauses are algebraic. The last two are dynamical descent clauses and are not supplied by the current core action.

Once \(\widehat g\) is Lorentzian, a coframe factorization always exists:

\[
\widehat g_{\mu\nu}=\eta_{AB}e^A{}_\mu e^B{}_\nu.
\]

It has the exact local redundancy

\[
e^A{}_\mu\longrightarrow\Lambda^A{}_B(x)e^B{}_\mu,
\qquad
\Lambda^T\eta\Lambda=\eta.
\]

This derives the local-Lorentz part of the old \(A_{\rm MF}\) route as a factorization redundancy. A local translation field \(X^A\), a translational compensator \(B^A\), and an independent spin connection are not forced. On the torsion-free metric branch, the spin connection is the composite Levi-Civita connection \(\omega[e]\). This removes an unnecessary affine axiom from the GR bridge; it does not by itself derive the Einstein-Hilbert coefficient.

## 3. Composite flow and the rank gate

Define the physical flow as the unique future-directed timelike eigenvector of the smoothed microscopic stress or covariance endomorphism. A stress definition is

\[
\overline T^\mu{}_{\nu}[\psi]u^\nu
=-\rho_\psi u^\mu,
\qquad
\widehat g_{\mu\nu}u^\mu u^\nu=-1.
\]

This is covariant and locally smooth provided the timelike eigenvalue is simple and separated from the other eigenvalues by a nonzero spectral gap. The sign is fixed by time orientation. The unit flow is then composite rather than a new primitive field.

The single-gradient no-go is exact, but a multi-realization covariance can evade it. Consider two microscopic gradient realizations

\[
d\phi_1=dt+\epsilon dx,
\qquad
d\phi_2=dt+\epsilon dy,
\]

with positive local weights \(w_1=1+y\), \(w_2=1+x\). To first order in \(\epsilon\), the timelike eigenflow has

\[
v_x=-\epsilon\frac{1+y}{2+x+y},
\qquad
v_y=-\epsilon\frac{1+x}{2+x+y},
\]

and

\[
\boxed{
\partial_xv_y-\partial_yv_x
=\epsilon\frac{x-y}{(2+x+y)^2}\ne0
}
\]

generically. Thus smoothing one scalar over multiple microscopic directions can produce a non-integrable eigenflow even though every individual realization is a gradient. The required spin-1 route is mathematically available, but it depends on a real smoothing ensemble or state that the current corpus has not defined.

## 4. Infrared operator theorem

Assume the repaired quotient produces only \(\widehat g\), the normalized composite flow \(u\), scalar state variables, and gapped microscopic residuals. Also assume locality, parity evenness, diffeomorphism invariance, and an expansion through two derivatives. Then the infrared action has the form

\[
\boxed{
\Gamma_{\rm IR}=
\frac{M_*^2}{2}\int d^4x\sqrt{-\widehat g}
\left[
\widehat R-2\Lambda_*
-\widehat K^{\alpha\beta}{}_{\mu\nu}
 \widehat\nabla_\alpha u^\mu
 \widehat\nabla_\beta u^\nu
+\lambda_u(u^2+1)
\right]
+S_{\rm matter}[\widehat g,\Psi,A]
+O(\partial^4/M_{\rm gap}^2),
}
\]

where

\[
\widehat K^{\alpha\beta}{}_{\mu\nu}
=\widehat c_1\widehat g^{\alpha\beta}\widehat g_{\mu\nu}
+\widehat c_2\delta^\alpha_\mu\delta^\beta_\nu
+\widehat c_3\delta^\alpha_\nu\delta^\beta_\mu
-\widehat c_4u^\alpha u^\beta\widehat g_{\mu\nu}.
\]

This derives the four-operator architecture from the corrected macroscopic variables. It does not derive the four coefficient values.

The coefficients are not arbitrary in principle. For four infinitesimal calibration backgrounds \(\mathcal B_I(\epsilon)\) that isolate expansion, shear, vorticity and acceleration and satisfy

\[
\int\sqrt{-\widehat g}\,\mathcal O_J[\mathcal B_I]
=\epsilon^2\delta_{IJ}+O(\epsilon^3),
\]

their exact microscopic matching definition is

\[
\boxed{
c_I=-\frac1{M_*^2}
\left.\frac{d^2\Gamma_{\rm micro}[\mathcal B_I(\epsilon)]}{d\epsilon^2}
\right|_{\epsilon=0}.
}
\]

These are Kubo/response coefficients of the smoothing state. They become calculable only after the microscopic measure, state, kernel and repaired action are specified.

There is nevertheless one new coefficient theorem. Let \(p\) measure the anisotropic connected covariance and let \(V^\mu=\sqrt p\,u^\mu\) be the nonsingular unnormalised order parameter. If the effective action is analytic in \(V\) and the flow disappears when \(p=0\), every physical unit-flow coefficient must obey

\[
\boxed{\widehat c_i=p\,\overline c_i+O(p^2).}
\]

The checkpoint-4861 public surface satisfies this exactly. With \(d=rp\),

\[
\frac{\widehat c_1}{p}\to\frac{1+r}{2},
\quad
\frac{\widehat c_2}{p}\to\frac{2}{3(1+r)},
\quad
\frac{\widehat c_3}{p}\to-\frac{1+r}{2},
\]

\[
\frac{\widehat c_4}{p}\to-\frac{(1-r)^2}{2(1+r)},
\qquad
\frac{\widehat c_{14}}{p}\to\frac{2r}{1+r}.
\]

The \(O(p)\) scaling is now structurally derived under analyticity. The displayed ratios and \(r\) remain PPN/stability-selected EFT matching data, not outputs of the current scalar action.

## 5. Universal source descent and the Poynting vector

Let \(q_{\rm cg}\) be the coarse quotient from microscopic configurations to the public variables:

\[
q_{\rm cg}:\psi\longmapsto(\widehat g,u,p,\ldots).
\]

Universal source coupling follows if and only if the microscopic interaction descends through the same quotient:

\[
\boxed{
S_{\rm int}[\psi,\Psi,A]
=\overline S_{\rm int}[q_{\rm cg}(\psi),\Psi,A],
\qquad
\overline S_{\rm int}=S_{\rm matter}[\widehat g,\Psi,A],
}
\]

with no species-dependent metric and no independent direct \(u\) charge. Under this premise,

\[
\delta S_{\rm matter}
=-\frac12\int\sqrt{-\widehat g}\,
\widehat T_{\mu\nu}\delta\widehat g^{\mu\nu},
\qquad
\widehat\nabla_\mu\widehat T^{\mu\nu}=0
\]

on matter shell.

In the base/disformal representation used by checkpoint 4861, the same chain rule gives

\[
J^{(u)\perp}_\nu
=\frac{p}{\sqrt{1-p}}
h_\nu{}^\lambda\widehat T_{\mu\lambda}u^\mu.
\]

For electromagnetism, the spatial projection is the Poynting momentum flux. Therefore the Poynting vector really does drive the background flow in this representation, but it does so as one component of the universal Hilbert source. It is not a separate electromagnetic patch or an independently tunable coupling.

The quotient premise is not proved by the existing scalar corpus. Consequently universal coupling remains one explicit primitive clause even though all of its downstream chain-rule consequences are derived.

## 6. GR, Newton and Maxwell limits

### GR

If \(p\to0\), analyticity gives \(c_i\to0\). If the higher-derivative modes also remain gapped and \(\Lambda_*\) is treated separately, then

\[
\Gamma_{\rm IR}\longrightarrow
\frac{M_*^2}{2}\int\sqrt{-\widehat g}\,\widehat R
+S_{\rm matter}[\widehat g,\Psi,A].
\]

This is a genuine conditional GR limit. The current corpus has not yet derived \(M_*\), the gap, or source descent, so it is not yet a primitive MTS-to-GR theorem.

### Newton

The public weak-field limit remains

\[
\widehat\Delta\widehat U=-4\pi\widehat G_N\widehat\rho,
\qquad
\boxed{
\widehat G_N=
\frac{1}{8\pi M_*^2(1-\widehat c_{14}/2)}.
}
\]

This shows exactly what a derivation of Newton's constant would require: calculate \(M_*\) and \(c_{14}\) from the microscopic response. The core formulas for \(\gamma\) and \(\lambda\) already contain \(G\), so they use Newton's constant as an input and cannot simultaneously derive it without circularity.

### Maxwell

Given the same public metric, locality, \(U(1)\) gauge invariance, parity evenness and the two-derivative truncation select

\[
S_{\rm EM}=-\frac1{4\mu_*}\int d^4x\sqrt{-\widehat g}\,
F_{\mu\nu}F^{\mu\nu}
+\int d^4x\sqrt{-\widehat g}\,A_\mu J^\mu
\]

up to the topological \(F\wedge F\) term and higher derivatives. Maxwell propagation, Hilbert stress and the Poynting source then use the same geometry. The gauge coupling, charge spectrum and microscopic origin of \(A_\mu\) remain separate particle/EM derivation targets.

## 7. Ownership decision

| Layer | 4872 status | Reason |
|---|---|---|
| Printed scalar damping action | rejected as a bulk parent | its gamma term is a boundary |
| Printed covariant metric covariance | rejected for the retained rank-one sign | it gives \(p\le0\) |
| Inverse connected-covariance metric | constructed candidate | exact \(p=q\ge0\), inverse and determinant identities pass |
| Local Lorentz coframe redundancy | derived kinematically | every Lorentzian metric factorization has it |
| Physical unit flow | constructed conditionally | unique timelike Landau eigenvector requires a spectral gap |
| Single-gradient vector branch | ruled out | Frobenius forces zero vorticity |
| Multimode vector branch | existence proved | explicit positive-weight covariance has nonzero eigenflow curl |
| Four unit-flow operators | derived conditionally | complete parity-even two-derivative basis |
| \(c_i=O(p)\) | derived under analytic decoupling | flow order parameter vanishes at \(p=0\) |
| Exact \(c_i(p,r)\) ratios | EFT matched, not primitive | smoothing response coefficients are unevaluated |
| Universal public matter coupling | quotient theorem with unsigned premise | microscopic matter descent is absent from the core action |
| 4857-4871 calculations | retained as correspondence results | internally tested but not primitive MTS predictions |
| Local GR/Newton/Maxwell claim | blocked | repaired parent measure, Kubo coefficients and source descent remain open |

## Consequence

This checkpoint does not end the route. It removes three pieces of false freedom: the original gamma term cannot be tuned into damping; the covariant rank-one covariance cannot be tuned into \(p>0\); and a normalized single scalar gradient cannot be tuned into a spin-1 flow.

It also replaces the old broad \(A_{\rm MF}\) ownership gap by a smaller constructive target:

- build a covariant doubled/open microscopic action;
- define its connected smoothing measure and inverse metric covariance;
- derive the Landau-flow response kernels;
- evaluate \(M_*\) and the four \(c_i\) Kubo coefficients;
- prove that every matter sector descends through the same public metric.

If that target closes, the compact-body and PPN machinery already developed becomes a primitive MTS test suite. If it does not, the Einstein-aether/unit-flow branch remains an explicit effective closure and must not be advertised as a fundamental derivation.

Next: 4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md

Primary local sources: core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md; core-mts-framework/field-theory/the-effective-field-theory-of-motion-timespace.md; post-checkpoint-work/4562-Y5-R2FR-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md; post-checkpoint-work/4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md; post-checkpoint-work/4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md; post-checkpoint-work/4871-Y5-R2FR-v3-l1-asymptotic-kappa4-crosscheck-and-full-first-order-C3-arbitration.md.

