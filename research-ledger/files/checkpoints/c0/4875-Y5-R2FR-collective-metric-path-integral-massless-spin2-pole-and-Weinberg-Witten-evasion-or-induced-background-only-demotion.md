# 4875 - Collective metric path integral, massless spin-2 pole and no-go arbitration

Marker: INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875

Decision: INTEGRATED_DIFF_PRINCIPAL_DENSITY_PARENT_CONSTRUCTED_EH_PROJECTOR_POLE_AND_WARD_DERIVED_WEINBERG_WITTEN_EVADED_BY_GAUGE_PARENT_STRICT_SCALAR_COMPOSITE_REJECTED_H_AND_DIFF_PRIMITIVE_DYNAMICS_INDUCED_PRIVATE_NONCLAIM

## Result

Checkpoint 4874 reduced the local-GR route to one question: whether the principal-density metric is a genuine integrated gauge variable with a physical massless spin-2 pole.

The answer is now branch-dependent and exact.

### Viable branch

Promote the densitized principal symbol \(\mathcal H^{\mu\nu}\) to an auxiliary **integrated** tensor-density variable from the start and quotient its field space by diffeomorphisms. It need not have a bare Einstein-Hilbert kinetic term. Microscopic motion, bath and matter fluctuations induce that term.

On this branch:

- the Einstein-Hilbert quadratic Hessian has the standard massless spin-2 pole;
- the spin-2 residue is positive for \(M_*^2>0\);
- exact Diff/BRST symmetry supplies the linear and nonlinear Ward identities;
- only helicities \(+2,-2\) propagate physically;
- the Weinberg-Witten trigger is absent because there is no gauge-invariant local Lorentz-covariant total gravitational stress tensor;
- Weinberg soft consistency activates universal source coupling.

### Rejected branch

If \(\mathcal H^{\mu\nu}\) is only a composite expectation value or Legendre variable of the original fixed-\(\eta\) scalar theory, then a massless graviton would be a composite spin-2 state inside an ordinary Lorentz-invariant QFT with a covariant conserved stress tensor. That triggers Weinberg-Witten.

Therefore:

\[
\boxed{
\text{strict fixed-background scalar-only composite graviton}
\quad\text{is rejected}.
}
\]

The one-loop \(\widehat R\) term on that strict branch is only an external/background response functional, not proof of dynamical gravity.

The selected MTS route is:

\[
\boxed{
\text{integrated diffeomorphic principal-density parent}
}
\]

with primitive field/symmetry data \((\mathcal H^{\mu\nu},{\rm Diff})\) and induced metric dynamics.

This is an explicit field-theory upgrade, not a hidden closure. Every serious field theory must declare its integration variables and gauge redundancy. What remains emergent here is the Einstein-Hilbert stiffness and its scale, not the existence of the gauge variable itself.

## 1. Minimal integrated parent

Define the public metric from \(\mathcal H^{\mu\nu}\) as in checkpoint 4874:

\[
\widehat g^{\mu\nu}
=
\frac{\mathcal H^{\mu\nu}}
{\sqrt{-\det\mathcal H}},
\qquad
\sqrt{-\widehat g}
=
\sqrt{-\det\mathcal H}.
\]

The parent partition function is

\[
\boxed{
Z=
\int
\frac{
\mathcal D\mathcal H\,
\mathcal D\psi_r\,
\mathcal D\psi_a\,
\mathcal DX
}{
{\rm Vol}({\rm Diff})
}
\exp i\left[
S_0[\widehat g(\mathcal H),\psi_r,\psi_a,X,\Psi,A]
+S_{\rm gf}+S_{\rm gh}
\right].
}
\]

Here:

- \(\psi_r,\psi_a\) are the open MTS average/response variables;
- \(X\) denotes a closed bath completion;
- \(\Psi,A\) denote matter and gauge sectors;
- \(S_{\rm gf},S_{\rm gh}\) are gauge-fixing and ghost terms;
- every kinetic operator uses \(\widehat g(\mathcal H)\);
- the action, measure and regulator are Diff/BRST covariant.

As a contravariant tensor density of weight \(+1\),

\[
\delta_\xi\mathcal H^{\mu\nu}
=
\xi^\rho\partial_\rho\mathcal H^{\mu\nu}
-\mathcal H^{\rho\nu}\partial_\rho\xi^\mu
-\mathcal H^{\mu\rho}\partial_\rho\xi^\nu
+\mathcal H^{\mu\nu}\partial_\rho\xi^\rho.
\]

The microscopic boundary condition may set the bare gravitational stiffness to zero,

\[
M_0^2(\Lambda_{\rm UV})=0,
\]

while retaining the cosmological/counterterm structure required by the regulator. Integrating the microscopic fields gives

\[
\Gamma_{\rm ind}[\widehat g]
=
\frac{M_*^2}{2}
\int\sqrt{-\widehat g}\,\widehat R
-\int\sqrt{-\widehat g}\,\rho_{\rm vac}
+\Gamma_{R^2}
+\Gamma_{\rm nonlocal}
+\cdots.
\]

The one-loop anchor from checkpoint 4873 supplies

\[
M_*^2=
\frac{N_s(1-6\xi)\Lambda_{\rm UV}^2}{96\pi^2}
\]

in the stated scalar/proper-time convention.

The construction does not claim that \(M_0^2=0\) is radiatively protected or regulator-independent. It is a UV boundary condition. The induced cosmological term and higher operators must be renormalized and tested.

## 2. Quadratic Einstein-Hilbert Hessian

Expand around a flat saddle,

\[
\widehat g_{\mu\nu}
=
\eta_{\mu\nu}
+\frac{1}{M_*}h_{\mu\nu},
\qquad
\Lambda_{\rm eff}=0.
\]

On the transverse symmetric sector, the gauge-invariant Einstein-Hilbert Hessian is

\[
\boxed{
\Gamma^{(2)}_{\rm EH}
=
M_*^2q^2
\left(
P^{(2)}-2P^{(0s)}
\right).
}
\]

Here \(P^{(2)}\) and \(P^{(0s)}\) are the Barnes-Rivers transverse spin-2 and scalar projectors. Their orthogonality gives

\[
\left(P^{(2)}-2P^{(0s)}\right)
\left(P^{(2)}-\frac12P^{(0s)}\right)
=
P^{(2)}+P^{(0s)}.
\]

Therefore the conserved-source propagator is

\[
\boxed{
D_{\mu\nu,\rho\sigma}(q)
=
\frac{i}{
M_*^2(q^2+i0)
}
\left(
P^{(2)}
-\frac12P^{(0s)}
\right)_{\mu\nu,\rho\sigma}
+\text{gauge terms}.
}
\]

The checkpoint script verifies the projector inversion exactly.

The spin-2 residue is

\[
\boxed{
{\rm Res}_{q^2=0}D^{(2)}
=
\frac1{M_*^2}>0
}
\]

when \(M_*^2>0\).

The \(P^{(0s)}\) source-trace term is not an independent propagating scalar in Einstein gravity. Diffeomorphism constraints leave the two physical helicities \(+2,-2\). A genuine extra scalar would require an additional independent pole from \(R^2\), state or matter sectors; such poles remain explicit residual tests.

If \(\Lambda_{\rm eff}\ne0\), the expansion and projector language must be replaced by the corresponding (A)dS helicity decomposition. The flat result is not applied outside its saddle domain.

## 3. Ward identity and physical spectrum

Because \(\mathcal H\) is integrated modulo Diff and the regulator is covariant, the effective action obeys

\[
\boxed{
\widehat\nabla_\mu
\left[
\frac{2}{\sqrt{-\widehat g}}
\frac{\delta\Gamma}{\delta\widehat g_{\mu\nu}}
\right]=0.
}
\]

Linearizing around the flat saddle gives

\[
\boxed{
q_\mu
\Gamma^{(2)\mu\nu,\rho\sigma}(q)=0.
}
\]

In projector form, the ungauge-fixed Hessian annihilates the longitudinal projector. The symbolic script verifies

\[
\Gamma^{(2)}P_L=0.
\]

Gauge fixing makes the operator invertible; BRST identities ensure that longitudinal and ghost modes do not enter physical amplitudes.

This supplies the missing distinction from checkpoint 4874. The Ward identity is not inferred from the heat-kernel coefficient. It follows from the declared integrated gauge field space.

## 4. Source exchange and Newtonian limit

For conserved sources, single-graviton exchange is

\[
\mathcal A(q)
=
\frac{i}{
M_*^2(q^2+i0)
}
\left(
T_{\mu\nu}T^{\mu\nu}
-\frac12T^2
\right).
\]

For a nonrelativistic source dominated by \(T_{00}=\rho\),

\[
T_{\mu\nu}T^{\mu\nu}
-\frac12T^2
=
\frac12\rho^2>0.
\]

With the standard action normalization,

\[
\boxed{
G_N=\frac1{8\pi M_*^2}.
}
\]

The soft theorem from checkpoint 4874 forces the same gravitational coupling for every species once the massless spin-2 pole and Ward identity exist. Thus equality of inertial and gravitational mass is activated on this branch rather than separately postulated.

The local leading source is the total public Hilbert tensor. Electromagnetic energy and Poynting momentum appear through \(T_{\mu\nu}^{\rm EM}\), not through a separate aether charge.

## 5. Weinberg-Witten arbitration

### 5.1 Strict scalar-only branch

Suppose

\[
\mathcal H^{\mu\nu}
=
\langle\mathcal O^{\mu\nu}[\psi]\rangle
\]

is only a Legendre-transform collective of the fixed-background scalar theory.

Then:

- the microscopic theory is formulated on \(\eta_{\mu\nu}\);
- it has a Lorentz-covariant conserved stress tensor;
- a massless spin-2 pole would be a composite particle carrying energy.

The Weinberg-Witten trigger is complete. This branch cannot own a physical composite graviton.

Decision:

\[
\boxed{
\text{reject strict scalar-only composite gravity}.
}
\]

### 5.2 Integrated principal-density branch

Now \(\mathcal H^{\mu\nu}\) is an independent integration variable with exact Diff redundancy. Its Einstein-Hilbert dynamics may be loop-induced, but the gauge field itself is not a composite particle of a fixed-background QFT.

The full gravitational system has no gauge-invariant local Lorentz-covariant total stress tensor. This violates a theorem premise in exactly the same structural way that GR does.

Decision:

\[
\boxed{
\text{Weinberg-Witten is not triggered on the integrated-Diff parent}.
}
\]

This is a demonstrated evasion conditional on exact Diff/BRST invariance of the parent measure and regulator. If a chosen regulator breaks that symmetry without a restorable Ward identity, the evasion fails.

## 6. What is fundamental and what is emergent

The branch is not advertised as “gravity from one scalar with nothing else.” That statement is rejected.

Primitive field/symmetry data:

\[
\mathcal H^{\mu\nu},\quad
{\rm Diff},\quad
\psi_r,\psi_a,\quad
X,\quad
\Psi,A.
\]

Emergent/induced data:

\[
M_*^2,\quad
\Lambda_{\rm eff},\quad
c_{R^2},c_{R_{\mu\nu}^2},\quad
\Gamma_{\rm nonlocal},\quad
\text{optional state-flow Kubo terms}.
\]

The MTS interpretation is that \(\mathcal H^{\mu\nu}\) is the local motion-time-space kinetic density or geometric order parameter. It has no required bare stiffness; the microscopic motion/state spectrum gives it elasticity.

This is a defensible induced-gravity theory. It is not a scalar-only emergent-graviton theory.

## 7. Conditional local-GR theorem

Under the explicit assumptions:

1. \(\mathcal H^{\mu\nu}\) is integrated modulo Diff;
2. the action, measure and regulator preserve the BRST Ward identities;
3. \(M_*^2>0\);
4. \(\Lambda_{\rm eff}\) selects the background used for the pole expansion;
5. Einstein-Hilbert dominates \(R^2\) and nonlocal terms in the local infrared;
6. all matter sectors use \(\widehat g(\mathcal H)\);

then:

\[
\boxed{
\Gamma_{\rm local}
=
\frac{M_*^2}{2}
\int\sqrt{-\widehat g}
(\widehat R-2\Lambda_{\rm eff})
+
S_{\rm matter}[\widehat g,\Psi,A]
+
O(\partial^4/\Lambda_{\rm UV}^2).
}
\]

Consequently:

- the physical gravitational spectrum contains helicities \(+2,-2\);
- universal coupling follows from the soft theorem;
- local PPN equals GR at leading two derivatives;
- Newtonian gravity has \(G_N=(8\pi M_*^2)^{-1}\);
- Maxwell, clocks, rods, free fall and Poynting stress use one public metric.

This is a real conditional derivation. The conditions are explicit parent data and hierarchy gates, not fitted closure coefficients.

## 8. Remaining work

The next checkpoint must turn this parent contract into a fully normalized minimal action and calculate rather than merely name:

- the \(\mathcal H\) saddle equation;
- the induced cosmological term and subtraction;
- the covariant regulator matching for \(M_*^2\);
- the first \(R^2\) and \(R_{\mu\nu}^2\) coefficients;
- the local hierarchy where the spin-2 pole dominates;
- the precise map from MTS Hadamard/bath data to \(N_s,\xi,\Lambda_{\rm UV}\);
- the observable residuals for R10, clocks, PPN, cosmology and compact bodies.

The strict scalar-only branch is no longer a live local-gravity route. The integrated-Diff principal-density branch is selected privately and remains nonclaim until its normalization and residual hierarchy are derived and tested.

Next: 4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md

Sources: [Weinberg and Witten](https://doi.org/10.1016/0370-2693(80)90212-9); [Weinberg soft theorem](https://journals.aps.org/pr/abstract/10.1103/PhysRev.135.B1049); [Deser self-coupling](https://arxiv.org/abs/gr-qc/0411023); [Vassilevich heat kernel](https://arxiv.org/abs/hep-th/0306138); post-checkpoint-work/4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md.

