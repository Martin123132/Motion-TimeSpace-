# 4873 - Covariant open parent, connected covariance kernel and local-branch arbitration

Marker: OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873

Decision: COVARIANT_SK_DAMPING_PARENT_CONSTRUCTED_CONNECTED_HADAMARD_METRIC_MAP_DEFINED_ONE_LOOP_EH_AND_GN_ANCHOR_DERIVED_COVARIANCE_DOES_NOT_FIX_FLOW_KUBO_METRIC_ONLY_QUOTIENT_SELECTED_AS_LEAD_PRIMITIVE_LOCAL_GR_BRANCH_UNIT_FLOW_RETAINED_EXTENSION_BACKGROUND_AND_UNIVERSAL_SYMBOL_OPEN_PRIVATE_NONCLAIM

## Result

Checkpoint 4872 showed that the printed one-field action cannot generate damping. This checkpoint supplies a valid covariant open-system variational replacement and then follows its consequences far enough to choose the next local-gravity branch.

The main results are:

1. A doubled Schwinger-Keldysh action generates the advertised damping in the physical equation while satisfying the required normalization, reality and positive-noise conditions.
2. The connected covariance is now defined by the renormalized Hadamard two-point function rather than an informal smoothing bracket.
3. Integrating Gaussian microscopic fields gives a calculable Einstein-Hilbert coefficient. With a proper-time cutoff, \(N_s\) real scalars and nonminimal coupling \(\xi\),

\[
\boxed{
M_*^2=
\frac{N_s(1-6\xi)}{96\pi^2}\Lambda_{\rm UV}^2.
}
\]

On a metric-only branch,

\[
\boxed{
G_N=\frac1{8\pi M_*^2}
=\frac{12\pi}{N_s(1-6\xi)\Lambda_{\rm UV}^2}.
}
\]

This is an induced-gravity anchor, not yet a regulator-independent MTS prediction.
4. The equal-point covariance does not determine the four unit-flow Kubo coefficients. An exact positive spectral counterexample has identical normalization and covariance moment but response moments \(1\) and \(11/4\).
5. If the infrared quotient depends only on the public metric and scalar state variables, while the Landau flow is a composite readout rather than an independent argument, then

\[
\boxed{c_1=c_2=c_3=c_4=0}
\]

as functional identities. Exact GR is reached by removing the independent flow field, not by taking the singular zero-kinetic endpoint of the Einstein-aether chart.
6. The metric-only induced-GR quotient is therefore selected as the lead primitive local branch. The nonzero unit-flow theory remains a tested state-flow extension and can be promoted only if a microscopic response calculation actually generates its safe coefficient ratios.

This is a larger change of architecture than another coefficient bound. It gives MTS a direct route to local GR while preserving the 4857-4871 work as a stress-tested extension rather than forcing it into the primitive spine.

## 1. A variational action that really produces damping

Use Schwinger-Keldysh average and response fields \(\psi_r,\psi_a\). Let

\[
\mathcal E_\psi[\psi_r]
=-\widehat\Box\psi_r+V'(\psi_r)
\]

denote the conservative Euler operator. The local Markovian open action is

\[
\boxed{
S_{\rm SK}=\int d^4x\sqrt{-\widehat g}
\left[
\psi_a\left(
\mathcal E_\psi[\psi_r]
+\gamma u^\mu\widehat\nabla_\mu\psi_r
\right)
+\frac{i}{2}\mathcal N\psi_a^2
\right].
}
\]

At the physical limit \(\psi_a=0\),

\[
\left.
\frac{\delta S_{\rm SK}}{\delta\psi_a}
\right|_{\psi_a=0}
=
\mathcal E_\psi[\psi_r]
+\gamma u^\mu\widehat\nabla_\mu\psi_r=0.
\]

The damping is now a bulk response term rather than a boundary.

The action satisfies the elementary closed-time-path conditions

\[
S_{\rm SK}[\psi_r,0]=0,
\]

\[
S_{\rm SK}^*[\psi_r,\psi_a]
=-S_{\rm SK}[\psi_r,-\psi_a],
\]

\[
\operatorname{Im}S_{\rm SK}
=\frac12\int\sqrt{-\widehat g}\,
\mathcal N\psi_a^2\ge0
\qquad(\mathcal N\ge0).
\]

These are executable identities in the checkpoint script. They are the correct structure for dissipative dynamics; an ordinary undoubled real action cannot supply them.

A closed microscopic completion may use a continuum of bath fields \(X_\Omega\),

\[
S_{\rm closed}=S_\psi+
\int d\Omega\,S_{X_\Omega}
+\int d^4x\sqrt{-\widehat g}
\int d\Omega\,g_\Omega\psi X_\Omega.
\]

The bath state defines

\[
\overline T^\mu{}_{\nu,{\rm bath}}u^\nu
=-\rho_{\rm bath}u^\mu.
\]

After the bath is integrated out, an Ohmic low-frequency retarded self-energy

\[
\Sigma_R(\omega)=-i\gamma\omega+O(\omega^2)
\]

gives the local damping term. In a thermal classical Markov limit, the KMS/fluctuation-dissipation relation gives

\[
\mathcal N=2\gamma T.
\]

Thus the time orientation comes from the state Landau vector, not from writing a preferred coordinate \(t\) into the action. The bath spectrum and state are new parent data that must be derived or specified; the construction proves existence, not uniqueness.

This architecture follows the general doubled-field constraints developed for dissipative effective theories by [Crossley, Glorioso and Liu](https://arxiv.org/abs/1511.03646).

## 2. Replace informal smoothing by the Hadamard kernel

For a state \(\rho\), define the connected symmetric two-point function

\[
G_H(x,y)
=\frac12
\left\langle
\{\delta\psi(x),\delta\psi(y)\}
\right\rangle_\rho,
\qquad
\delta\psi=\psi-\langle\psi\rangle_\rho.
\]

The sign-corrected covariance of checkpoint 4872 becomes

\[
\boxed{
\mathcal C^{\mu\nu}(x)
=
\ell_*^2
\left[
\widehat\nabla_x^\mu
\widehat\nabla_y^\nu
G_H(x,y)
\right]_{y\to x}^{\rm ren}.
}
\]

This definition supplies:

- centering;
- a physical state;
- a tensorial point-split regulator;
- an explicit renormalization operation;
- a calculable object once the propagator and bath spectrum are given.

The public metric candidate remains

\[
\widehat g^{\mu\nu}
=g_{\rm ref}^{\mu\nu}+\mathcal C^{\mu\nu}.
\]

The new definition is sharper, but the reference metric has not disappeared. Primitive background independence requires the infrared generating functional to satisfy

\[
\frac{\delta\Gamma_{\rm IR}}
{\delta g_{\rm ref}^{\mu\nu}}
\bigg|_{\widehat g,\ {\rm public\ data}}=0.
\]

That is the exact next quotient test. Until it is proved, \(g_{\rm ref}\) is a scaffold rather than an eliminated microscopic background.

## 3. One-loop induced Einstein-Hilbert coefficient

Consider \(N_s\) real Gaussian fluctuations with public kinetic operator

\[
\mathcal D=-\widehat\Box+\xi\widehat R+m^2.
\]

Their one-loop Euclidean functional is

\[
\Gamma_1=\frac{N_s}{2}\operatorname{Tr}\ln\mathcal D.
\]

The proper-time representation and heat-kernel expansion give

\[
\operatorname{Tr}e^{-s\mathcal D}
=
\frac1{(4\pi s)^2}
\int d^4x\sqrt{\widehat g}
\left[
1+s\left(\frac16-\xi\right)\widehat R+O(s^2)
\right].
\]

Using \(s\ge\Lambda_{\rm UV}^{-2}\), the Lorentzian Einstein-Hilbert normalization has magnitude

\[
\Gamma_1\supset
\frac{N_s(1/6-\xi)\Lambda_{\rm UV}^2}
{32\pi^2}
\int d^4x\sqrt{-\widehat g}\,\widehat R.
\]

Equating this to \(M_*^2\widehat R/2\) gives

\[
\boxed{
M_*^2=
\frac{N_s(1-6\xi)\Lambda_{\rm UV}^2}
{96\pi^2}.
}
\]

For this scalar/cutoff convention, a positive Einstein-Hilbert coefficient requires \(\xi<1/6\). If \(\Lambda_{\rm UV}=\ell_*^{-1}\),

\[
M_*^2=
\frac{N_s(1-6\xi)}
{96\pi^2\ell_*^2}.
\]

This is the first explicit non-circular formula connecting a microscopic MTS correlation scale to Newton's constant:

\[
\boxed{
G_N=
\frac{12\pi\ell_*^2}
{N_s(1-6\xi)}
}
\]

on the metric-only branch.

The result is deliberately an anchor rather than a claimed prediction. Power divergences depend on the microscopic regulator and counterterm prescription. The same expansion also produces a vacuum term of magnitude

\[
|\rho_{\rm vac}^{(1)}|
\sim\frac{N_s\Lambda_{\rm UV}^4}{64\pi^2},
\]

so inducing the observed Einstein-Hilbert scale does not solve the cosmological-constant problem. The heat-kernel coefficient and induced-gravity interpretation are source-backed by [Vassilevich](https://arxiv.org/abs/hep-th/0306138) and [Visser](https://arxiv.org/abs/gr-qc/0204062).

The important advance is exact: MTS can derive \(G_N\) only if it derives \(\ell_*\), \(N_s\), \(\xi\), the regulator and the subtraction rule without already inserting \(G\). The old formulas for \(\gamma\) and \(\lambda\), which contain \(G\), cannot do that job.

## 4. Why covariance cannot fix the aether coefficients

The public covariance is one moment of the microscopic spectral data. The derivative response coefficients are different moments.

A positive discrete counterexample makes the underdetermination exact.

Spectrum A:

\[
\rho_A:\quad w=1,\quad\omega=1.
\]

Spectrum B:

\[
\rho_B:\quad
w_1=\frac13,\ \omega_1=\frac12;
\qquad
w_2=\frac23,\ \omega_2=2.
\]

Both have unit normalization and the same covariance moment

\[
\sum_i\frac{w_i}{\omega_i}=1.
\]

A higher response moment gives

\[
\sum_i\frac{w_i}{\omega_i^3}
=
\begin{cases}
1,&A,\\[3pt]
11/4,&B.
\end{cases}
\]

Therefore equal connected covariance does not determine the Kubo/derivative response. In field language, the metric two-point datum does not determine stress-stress and higher connected correlators.

This proves a real limitation of the primitive corpus:

\[
\boxed{
\mathcal C^{\mu\nu}
\ \not\Rightarrow\
(\widehat c_1,\widehat c_2,\widehat c_3,\widehat c_4).
}
\]

The four coefficients require the full retarded state response, not just the equal-point covariance metric. No amount of algebra on the covariance ansatz alone can derive the checkpoint-4861 \(r\)-dependent safe surface.

## 5. The metric-only quotient theorem

There are now two logically distinct infrared quotients.

### 5.1 Metric-only quotient

\[
\Gamma_{\rm IR}
=\Gamma_{\rm IR}[\widehat g,\vartheta_{\rm scalar},\Psi,A].
\]

The Landau vector is a diagnostic eigenvector of the state. It is not independently varied. At fixed \(\widehat g\),

\[
\frac{\delta\Gamma_{\rm IR}}{\delta u^\mu}=0.
\]

Consequently every independent unit-flow derivative coefficient vanishes:

\[
\boxed{
\widehat c_1=\widehat c_2=\widehat c_3=\widehat c_4=0.
}
\]

This is not the singular \(c_i\to0\) endpoint of a theory that still contains a zero-kinetic vector. The vector is absent from the field space. The local propagating spectrum is therefore the metric spectrum, not a degenerate tensor-vector-scalar aether spectrum.

At two derivatives,

\[
\Gamma_{\rm IR}^{\rm local}
=
\frac{M_*^2}{2}
\int d^4x\sqrt{-\widehat g}
(\widehat R-2\Lambda_*)
+S_{\rm matter}[\widehat g,\Psi,A].
\]

This gives exact local GR once background independence and universal source descent are proved.

### 5.2 State-flow quotient

\[
\Gamma_{\rm IR}
=\Gamma_{\rm IR}[\widehat g,u,\vartheta_{\rm scalar},\Psi,A].
\]

Now the four unit-flow operators are allowed and their coefficients are independent Kubo data. Checkpoints 4857-4871 provide a complete, tested correspondence branch for this case, but the primitive covariance does not select its ratios.

The branch decision is therefore:

\[
\boxed{
\text{lead primitive local branch}
=
\text{metric-only induced GR};
}
\]

\[
\boxed{
\text{nonzero unit-flow branch}
=
\text{retained state-flow extension}.
}
\]

This is a private architecture selection, not yet a local-GR claim. It prevents the entire fundamental theory from being held hostage by an optional preferred-frame extension.

## 6. Local GR, Newton, Maxwell and Poynting consequences

If the metric-only quotient closes, the leading local action is Einstein-Hilbert plus universal matter. Then:

### GR and PPN

There is no independently varied preferred-frame field. The local PPN parameters are the GR values because the theory is GR at two derivatives, not because four aether parameters were tuned to a PPN-safe surface.

Higher-curvature corrections are suppressed by

\[
E^2/\Lambda_{\rm UV}^2
\]

or the corresponding curvature ratio. Their coefficients must still be bounded by R10, Solar-System and compact-object data.

### Newton

The weak static equation is

\[
\widehat\nabla^2 U=4\pi G_N\rho,
\qquad
G_N=\frac1{8\pi M_*^2}.
\]

The induced-gravity formula gives a microscopic target for \(G_N\), subject to the regulator caveat.

### Maxwell

If every matter principal symbol descends through the same \(\widehat g\), then the leading parity-even \(U(1)\) action is

\[
S_{\rm EM}
=-\frac14
\int d^4x\sqrt{-\widehat g}\,
F_{\mu\nu}F^{\mu\nu}
+\int d^4x\sqrt{-\widehat g}\,A_\mu J^\mu.
\]

Its Hilbert stress, Poynting vector, clocks and null cone all use the same public metric. On the metric-only branch, Poynting flux gravitates through \(T_{\mu\nu}^{\rm EM}\); it does not source an independent local aether mode.

The remaining Maxwell issue is not the local action form. It is proving that photons, charged matter, clocks and neutral matter share the same microscopic principal symbol and deriving charge itself.

## 7. What survives from the unit-flow programme

Nothing in 4857-4871 is deleted.

It remains useful in three roles:

1. a complete test harness if the microscopic state retains an independent flow response;
2. a quantitative upper envelope for preferred-frame leakage away from the metric-only quotient;
3. an extension candidate for cosmological, galactic or nonequilibrium regimes where the state cannot be reduced to the local metric alone.

What changes is the burden of proof. The unit-flow branch no longer sits in the primitive local spine by default. It must earn that position through a nonzero microscopic Kubo calculation.

The compact-body \(f,\kappa_4,g\), PPN, radiation and cutoff results remain conditional predictions of that extension.

## 8. Remaining root gates

The local route is now concentrated into four proof obligations:

1. **Background independence:** show \(g_{\rm ref}\) disappears from \(\Gamma_{\rm IR}\) at fixed public data.
2. **Universal principal symbol:** show every matter and gauge kinetic operator has the same \(\widehat g^{\mu\nu}\).
3. **Microscopic scale:** derive \(N_s,\xi,\ell_*\), the regulator and subtraction prescription without input \(G\).
4. **Vacuum/state terms:** separate or derive the induced \(\Lambda_*\), nonlocal memory and large-scale residuals without reintroducing local preferred-frame leakage.

This is substantially narrower than deriving a full nonzero aether coefficient surface from the original scalar covariance.

## Decision

The damping problem is repaired at the open-action level, the covariance is promoted to a renormalized two-point object, and the Einstein-Hilbert/Newton normalization has a calculable one-loop anchor. A no-go theorem proves that covariance alone cannot fix the nonzero unit-flow coefficients.

The lead primitive local branch is now metric-only induced GR. The unit-flow action is retained as a tested extension rather than discarded or smuggled into the fundamental spine.

Next: 4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md

Sources: [Crossley, Glorioso and Liu](https://arxiv.org/abs/1511.03646); [Vassilevich](https://arxiv.org/abs/hep-th/0306138); [Visser](https://arxiv.org/abs/gr-qc/0204062); post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md; post-checkpoint-work/4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md.

