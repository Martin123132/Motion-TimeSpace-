# 4874 - Metric-only background independence, principal symbol and universal coupling

Marker: DIRECT_PRINCIPAL_METRIC_SOFT_UNIVERSALITY_AND_SPIN2_NO_GO_GATE_4874

Decision: ADDITIVE_SPLIT_WARD_IDENTITY_DERIVED_REFERENCE_METRIC_REMOVED_BY_DIRECT_DENSITIZED_PRINCIPAL_SYMBOL_METRIC_SOFT_GRAVITON_UNIVERSAL_COUPLING_DERIVED_CONDITIONALLY_HEAT_KERNEL_NOT_A_SPIN2_POLE_PROOF_WEINBERG_WITTEN_GATE_OPEN_METRIC_ONLY_LOCAL_GR_ROUTE_NARROWED_PRIVATE_NONCLAIM

## Result

Checkpoint 4873 selected a metric-only local branch but left two questions: whether the reference metric can be removed and whether all matter species must couple to the same public metric.

This checkpoint obtains a stronger answer than freezing both as axioms.

1. For an additive representation \(\widehat g=g_{\rm ref}+\mathcal C\), background independence is exactly a split Ward identity.
2. The reference split can be avoided entirely by defining the public metric directly from the densitized principal symbol of the infrared kinetic operator.
3. If that metric supports one positive-residue massless spin-2 pole and a Lorentz-invariant local S matrix, the soft-graviton consistency condition forces one universal gravitational coupling to every species.
4. The heat-kernel Einstein-Hilbert coefficient found at 4873 is not by itself proof that such a physical spin-2 pole exists.
5. A naive composite graviton built inside the fixed-background scalar theory faces the Weinberg-Witten theorem. MTS must derive emergent diffeomorphism redundancy or show explicitly which theorem premise fails.

The universal-source problem is therefore no longer an arbitrary coupling search. It is reduced to one spectral/gauge question:

\[
\boxed{
\text{Does the collective public metric possess a genuine massless spin-2 pole
with emergent diffeomorphism Ward identities?}
}
\]

If yes, universal coupling follows. If no, the induced Einstein-Hilbert term is only a background response functional and the local-GR derivation fails.

## 1. Exact split Ward identity

Retain temporarily

\[
\widehat g^{\mu\nu}
=g_{\rm ref}^{\mu\nu}+\mathcal C^{\mu\nu}.
\]

A change of split at fixed public metric is

\[
\delta g_{\rm ref}^{\mu\nu}=\epsilon^{\mu\nu},
\qquad
\delta\mathcal C^{\mu\nu}=-\epsilon^{\mu\nu},
\qquad
\delta\widehat g^{\mu\nu}=0.
\]

Therefore background independence requires

\[
\boxed{
\mathcal W_{\rm split}\Gamma
\equiv
\left(
\frac{\delta}{\delta g_{\rm ref}^{\mu\nu}}
-\frac{\delta}{\delta\mathcal C^{\mu\nu}}
\right)\Gamma=0.
}
\]

The symbolic regression uses

\[
\Gamma_{\rm good}=F(g_{\rm ref}+\mathcal C)
\]

and obtains zero, while

\[
\Gamma_{\rm bad}=g_{\rm ref}^2+\mathcal C^3
\]

gives a nonzero residual \(2g_{\rm ref}-3\mathcal C^2\).

This identity is a precise audit tool, but the legacy microscopic action and regulator do not prove it. Rather than imposing split symmetry on an additive ansatz, the cleaner route is to stop using the reference split as the primitive definition.

## 2. Define the metric from the principal density

Let the two-derivative 1PI kinetic operator have a symmetric, nondegenerate Lorentzian principal density

\[
\mathcal H^{\mu\nu}(x).
\]

For a scalar,

\[
\Gamma^{(2)}
\supset
-\partial_\mu
\left(
\mathcal H^{\mu\nu}\partial_\nu
\right).
\]

In four dimensions a densitized inverse metric obeys

\[
\mathcal H^{\mu\nu}
=\sqrt{-\widehat g}\,\widehat g^{\mu\nu}.
\]

This relation is invertible. Since

\[
\det\mathcal H^{\mu\nu}=\det\widehat g_{\mu\nu},
\]

the public metric is reconstructed directly:

\[
\boxed{
\sqrt{-\widehat g}
=\sqrt{-\det\mathcal H},
\qquad
\widehat g^{\mu\nu}
=\frac{\mathcal H^{\mu\nu}}
{\sqrt{-\det\mathcal H}}.
}
\]

The checkpoint script verifies the determinant, inverse and reconstruction identities exactly for a general diagonal Lorentzian principal density.

This definition needs no \(g_{\rm ref}\). The Hadamard covariance of 4873 remains useful, but its role changes:

\[
G_H,\ \Sigma_R,\ \rho
\quad\longrightarrow\quad
\mathcal H^{\mu\nu}
\quad\longrightarrow\quad
\widehat g_{\mu\nu}.
\]

The public metric is the normalized infrared kinetic response, not a raw additive perturbation of a hidden metric.

The new gates are:

- \(\mathcal H^{\mu\nu}\) must be Lorentzian and nondegenerate;
- its low-energy limit must be local;
- all physical sectors must share it up to wavefunction normalization;
- its collective fluctuations must contain the physical spin-2 spectrum.

## 3. The physical massless-spin-2 gate

Checkpoint 4873 derived a term

\[
\frac{M_*^2}{2}
\int\sqrt{-\widehat g}\,\widehat R
\]

in a one-loop response functional. That calculation treats \(\widehat g\) as a background or collective argument. It does not prove that the microscopic path integral includes integration over \(\widehat g\), nor that its two-point function has a propagating graviton pole.

The required spectral statement is

\[
\boxed{
\langle h_{\mu\nu}h_{\rho\sigma}\rangle(q)
=
\frac{i\,\Pi^{(2)}_{\mu\nu,\rho\sigma}}
{M_*^2(q^2+i0)}
+\text{gauge terms}
+\text{massive/analytic terms}.
}
\]

It must satisfy:

\[
M_*^2>0,
\]

\[
q^\mu\Gamma_{\mu\nu,\rho\sigma}^{(2)}(q)=0,
\]

and the physical spectrum must contain exactly the helicity \(+2,-2\) massless pole, with no negative-residue spin-2 pole and no additional unsuppressed scalar.

The heat-kernel coefficient is necessary evidence for a kinetic term. It is not sufficient evidence for this pole or its field-space measure.

This becomes the next hard derivation rather than being hidden inside the phrase “induced gravity.”

## 4. Universal coupling from the soft graviton

Assume the pole gate closes and consider emission of a soft graviton of momentum \(q\) and polarization \(\epsilon_{\mu\nu}\). The leading factorized amplitude is

\[
\mathcal M_{n+1}
=
\left[
\sum_i
\eta_i\kappa_i
\frac{p_i^\mu p_i^\nu\epsilon_{\mu\nu}}
{p_i\cdot q}
\right]\mathcal M_n
+O(q^0),
\]

where \(\eta_i=+1\) for outgoing and \(-1\) for incoming legs.

Mass-shell gauge invariance under

\[
\epsilon_{\mu\nu}
\longrightarrow
\epsilon_{\mu\nu}
+q_\mu\xi_\nu+q_\nu\xi_\mu
\]

requires

\[
\sum_i\eta_i\kappa_i p_i^\nu=0.
\]

Momentum conservation gives

\[
\sum_i\eta_i p_i^\nu=0.
\]

For arbitrary external momenta, both identities are compatible only when

\[
\boxed{
\kappa_1=\kappa_2=\cdots=\kappa.
}
\]

The checkpoint script verifies the algebra on an arbitrary three-leg momentum basis: the two independent momentum coefficients force \(\kappa_1=\kappa_2=\kappa_3\).

This is the equality of gravitational and inertial coupling. It is not imposed species by species. It follows from one massless spin-2 pole, Lorentz invariance, soft factorization and gauge consistency. The source is Weinberg's original [soft-graviton argument](https://journals.aps.org/pr/abstract/10.1103/PhysRev.135.B1049).

At the two-derivative infrared level, universal coupling and the spin-2 gauge completion lead to the Einstein interaction structure; Weinberg's perturbative construction is the relevant primary result: [Photons and Gravitons in Perturbation Theory](https://journals.aps.org/pr/abstract/10.1103/PhysRev.138.B988).

## 5. Common principal symbols

Under the same assumptions, local Lorentz invariance gives the leading species operators

\[
\mathcal P_s
=
Z_s\widehat g^{\mu\nu}k_\mu k_\nu
+O(k^4/\Lambda_{\rm UV}^2)
\]

for scalars,

\[
\mathcal P_f
=
Z_f\gamma^A e_A{}^\mu k_\mu,
\qquad
\mathcal P_f^2
\propto
\widehat g^{\mu\nu}k_\mu k_\nu
\]

for fermions, and the same transverse null cone for photons.

The factors \(Z_s,Z_f,\ldots\) are removable wavefunction normalizations and do not create species-dependent cones. Curvature couplings and higher-dimension operators remain allowed residuals, but they are suppressed and testable.

Thus the universal-principal-symbol contract is derivable conditionally:

\[
\boxed{
\text{one massless spin-2 pole}
+\text{Lorentz/local soft consistency}
\Longrightarrow
\text{one leading gravitational coupling and one local metric cone}.
}
\]

This is stronger than simply postulating one matter metric, but every premise must be verified in the emergent MTS state.

## 6. Weinberg-Witten obstruction

The positive soft theorem has a corresponding no-go gate.

The Weinberg-Witten result applies when a microscopic theory has:

- exact Lorentz invariance;
- a Lorentz-covariant conserved stress tensor;
- a massless spin-2 state that is composite within that theory.

Under those premises, a composite massless spin-2 state carrying energy is forbidden. See [Weinberg and Witten, Limits on Massless Particles](https://doi.org/10.1016/0370-2693(80)90212-9).

The original fixed-background scalar MTS action appears close to the theorem's trigger: it is an ordinary scalar field on \(\eta_{\mu\nu}\) with a conventional stress tensor. Therefore MTS cannot merely declare a bound state of \(\psi\) to be the graviton.

The admissible route is narrower:

\[
\boxed{
\text{derive emergent diffeomorphism redundancy so that gravitational energy
has no gauge-invariant local Lorentz-covariant stress tensor,}
}
\]

or demonstrate explicitly that another theorem premise fails.

This is not automatically fatal. General relativity itself evades the theorem because gravitational stress is not represented by a gauge-invariant local Lorentz tensor. Work on emergent gauge redundancy shows how the theorem can be avoided, but the evasion must be demonstrated in MTS rather than cited as a possibility.

## 7. Local GR, Newton and Maxwell chain

If the principal-density, pole, gauge and soft gates all close, then the two-derivative local chain is:

\[
\mathcal H^{\mu\nu}
\longrightarrow
\widehat g_{\mu\nu}
\longrightarrow
\text{one massless spin-2 pole}
\longrightarrow
\text{universal }\kappa
\longrightarrow
S_{\rm EH}+S_{\rm matter}[\widehat g].
\]

Consequences:

### GR and PPN

The metric-only two-derivative theory is GR (or the same local weak-field dynamics in a unimodular presentation) plus a cosmological integration/parameter sector. Its PPN values are the GR values.

### Newton

The soft theorem supplies equality of inertial and gravitational mass. The static weak-field equation is

\[
\nabla^2U=4\pi G_N\rho,
\qquad
G_N=\frac1{8\pi M_*^2}.
\]

### Maxwell and Poynting stress

The photon principal symbol uses the same \(\widehat g\), and \(U(1)\) gauge invariance gives the Maxwell action at two derivatives. Its Hilbert tensor, including Poynting momentum, enters the same universal gravitational source.

### Residuals

The first permitted deviations are:

- higher-curvature operators;
- higher-dimension species operators;
- nonlocal state/memory terms;
- optional nonzero state-flow Kubo response.

These are extension coefficients to derive or bound, not modifications required to obtain local gravity.

## 8. Decision and exact remaining gap

Closed here:

- exact split Ward identity;
- exact reference-free metric reconstruction from \(\mathcal H^{\mu\nu}\);
- exact soft-coupling universality algebra;
- explicit common-principal-symbol contract;
- explicit distinction between an induced \(\widehat R\) coefficient and a physical graviton pole;
- explicit Weinberg-Witten trigger/evasion gate.

Not closed:

- the collective metric path-integral measure;
- a positive physical spin-2 pole;
- emergent diffeomorphism Ward identities;
- a demonstrated Weinberg-Witten evasion;
- the MTS derivation of \(\Lambda_{\rm UV}\), vacuum subtraction and higher-curvature coefficients.

No equivalence axiom is frozen yet because the soft theorem can derive universality if the pole/gauge gate closes. The next work should attack that gate directly.

Next: 4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md

Sources: [Weinberg 1964](https://journals.aps.org/pr/abstract/10.1103/PhysRev.135.B1049); [Weinberg 1965](https://journals.aps.org/pr/abstract/10.1103/PhysRev.138.B988); [Weinberg and Witten 1980](https://doi.org/10.1016/0370-2693(80)90212-9); [Hertzberg and Sandora](https://arxiv.org/abs/1704.05071); post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md.

