# 4916 - Covariantization map, direct-flow charge and primitive ownership

Marker: `MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916`

## Decision

The missing map can be constructed explicitly, but it is not uniquely forced
by the original scalar action.

The current serious parent is not the rejected fixed-background scalar-only
theory. It is the integrated principal-density theory selected at checkpoint
4875, with a covariant closed scalar-bath sector and the GR-parity Standard
Model matter action already adopted at checkpoints 4446 and 4904.

Checkpoint 4916 now supplies four concrete results.

1. Every retained flat kinetic term has an explicit map into the one public
   metric `g(H)`, including the motion scalar, bath, Higgs, gauge and fermion
   sectors.
2. Variation through the densitized inverse metric is derived exactly:

   \[
   \boxed{
   \frac{\delta S_{\rm matter}}{\delta\mathcal H^{\mu\nu}}
   =-\frac12\left(T_{\mu\nu}-\frac12g_{\mu\nu}T\right).
   }
   \]

   Trace reversal is an involution in four dimensions, so this map loses no
   source information.
3. The ordinary Standard-Model action has no bath-flow, motion-scalar or bath
   argument. Its direct flow current is therefore exactly zero at tree level
   in the selected parent.
4. Diff and Standard-Model gauge symmetry do not prove an all-orders zero.
   Curvature-Higgs, disformal, anisotropic gauge/Higgs/fermion and hidden-scalar
   coefficient operators are symmetry allowed. Their absence is a parent
   architecture selection at the matching action, not a uniqueness theorem.

The honest status is therefore

```text
explicit eta -> g(H) map                 = CONSTRUCTED
H-density/Hilbert source chain           = DERIVED EXACTLY
tree direct ordinary-matter flow charge  = ZERO ON SELECTED PARENT
symmetry uniqueness of minimal map       = FALSE
all-orders flow/hidden re-entry           = OPEN: CALCULATE OR BOUND
matter-pullback ownership                = EXPLICIT PRIMITIVE GR-PARITY FUNCTOR
strict scalar-only GR derivation          = REJECTED
```

This moves the theory forward without disguising minimal coupling as something
the old scalar action proved.

## 1. Reconcile the actual parent with the original corpus

The original core action used

\[
\mathcal L_\psi
=\frac{(\partial_t\psi)^2}{2c^2}
-\frac12|\nabla\psi|^2
-\gamma\psi\partial_t\psi
-\frac\lambda n|\psi|^n.
\]

Checkpoint 4872 proved that the `gamma` term is a boundary term and cannot
generate damping. It also proved that the raw additive covariance metric and a
single normalized scalar gradient do not supply the selected local branch.

Checkpoint 4873 repaired the variational problem by introducing a covariant
closed bath or its Schwinger-Keldysh reduction. Checkpoint 4875 then selected
the independent integrated tensor density `H` modulo Diff. The current closed
parent can therefore be written schematically as

\[
\boxed{
\begin{aligned}
Z_{\rm parent}=\int
\frac{D\mathcal H\,D\psi\,DX\,D\Phi_{\rm SM}}
{\operatorname{Vol}(\mathrm{Diff}\times G_{\rm SM})}
\exp i[&S_H[\mathcal H]+S_\psi[\mathcal H,\psi]
+S_X[\mathcal H,X]\\
&+S_{\psi X}[\mathcal H,\psi,X]
+S_{\rm SM}[g(\mathcal H),\Phi_{\rm SM}]
+S_{\rm gf}+S_{\rm gh}].
\end{aligned}
}
\]

The bath state defines a Landau vector only after reduction to the open
description. No public flow vector is an argument of the fundamental ordinary
matter action.

## 2. Exact principal-density map

In four dimensions define

\[
\mathcal H^{\mu\nu}=\sqrt{-g}\,g^{\mu\nu}.
\]

Its determinant gives the volume directly:

\[
\det\mathcal H=g,
\qquad
\sqrt{-g}=\sqrt{-\det\mathcal H}.
\]

The inverse map is

\[
\boxed{
g^{\mu\nu}
=\frac{\mathcal H^{\mu\nu}}{\sqrt{-\det\mathcal H}},
\qquad
g_{\mu\nu}
=\sqrt{-\det\mathcal H}\,
(\mathcal H^{-1})_{\mu\nu}.
}
\]

At the flat saddle `H^mn=eta^mn`, the determinant is `-1` and the map returns
the Minkowski metric exactly. The fixed spacetime `eta_mn` is therefore not a
second tensor in the curved parent. The symbol `eta_ab` remains only as the
internal tangent-space metric of the coframe.

## 3. Explicit covariantization functor

Define the minimal GR-parity lift `C_H^min` by

\[
d^4x\mapsto d^4x\sqrt{-g(\mathcal H)},
\qquad
\eta^{\mu\nu}\mapsto g^{\mu\nu}(\mathcal H),
\]

\[
\partial_\mu\mapsto\nabla_\mu
\quad\text{or}\quad
D_\mu=\partial_\mu+\omega_\mu[e(\mathcal H)]+A_\mu,
\]

with masses, representations, gauge couplings and Yukawa constants carried
unchanged as calibrated Standard-Model data.

### 3.1 Motion scalar

After removing the false damping boundary term, the conservative scalar lift
is

\[
\boxed{
S_\psi[\mathcal H,\psi]
=-\frac12\int d^4x\,
\mathcal H^{\mu\nu}\partial_\mu\psi\partial_\nu\psi
-\int d^4x\sqrt{-g(\mathcal H)}\,V(\psi).
}
\]

For the literal tested branch,

\[
V(\psi)=\frac34g_\psi|\psi|^{4/3}.
\]

This is the continuum action whose densitized-metric variation underlies the
4910--4914 stress-response calculations.

### 3.2 Closed bath and open reduction

Each bath kinetic term receives the same metric lift, and

\[
S_{\psi X}
=\int d^4x\sqrt{-g}\int d\Omega\,
g_\Omega\psi X_\Omega.
\]

After choosing a bath state and integrating the bath, the local Markovian
limit has the valid doubled action

\[
S_{\rm SK}=\int d^4x\sqrt{-g}\left[
\psi_a\left(-\Box_g\psi_r+V'(\psi_r)
+\gamma u_{\rm bath}^\mu\nabla_\mu\psi_r\right)
+\frac{i}{2}\mathcal N\psi_a^2
\right].
\]

The state vector `u_bath` belongs to the reduced MTS-bath influence
functional. It is not inserted into the ordinary matter action.

### 3.3 GR-parity Standard Model

The Higgs kinetic and potential terms map to

\[
S_H=\int d^4x\left[
\mathcal H^{\mu\nu}
(D_\mu H_{\rm SM})^\dagger D_\nu H_{\rm SM}
-\sqrt{-g}\,V_H
\right].
\]

Every gauge factor has

\[
S_{\rm gauge}
=-\frac14\int d^4x\sqrt{-g}\,
g^{\mu\rho}g^{\nu\sigma}
F^A_{\mu\nu}F^A_{\rho\sigma}.
\]

Fermions use any coframe satisfying

\[
g_{\mu\nu}=\eta_{ab}e^a{}_\mu e^b{}_\nu
\]

and its torsion-free spin connection:

\[
S_f=\int d^4x\sqrt{-g}\,
i\bar f\gamma^ae_a{}^\mu
(\partial_\mu+\omega_\mu[e]+A_\mu)f.
\]

The freedom `e -> Lambda(x)e` is an exact local Lorentz redundancy; the script
verifies the boost identity symbolically. No independent torsion or connection
is introduced on this branch.

## 4. Exact `H`-source chain

Let

\[
s=\sqrt{-\det\mathcal H}.
\]

For an arbitrary symmetric variation,

\[
\boxed{
\delta g^{\mu\nu}
=\frac1s\left[
\delta\mathcal H^{\mu\nu}
-\frac12\mathcal H^{\mu\nu}
(\mathcal H^{-1})_{\alpha\beta}
\delta\mathcal H^{\alpha\beta}
\right].
}
\]

Using

\[
\delta S_{\rm matter}
=-\frac12\int d^4x\sqrt{-g}\,
T_{\mu\nu}\delta g^{\mu\nu},
\]

gives

\[
\boxed{
\delta S_{\rm matter}
=-\frac12\int d^4x
\left(T_{\mu\nu}-\frac12g_{\mu\nu}T\right)
\delta\mathcal H^{\mu\nu}.
}
\]

Define trace reversal in four dimensions by

\[
\mathcal R_4(T)_{\mu\nu}
=T_{\mu\nu}-\frac12g_{\mu\nu}T.
\]

Its trace is `-T`, so

\[
\boxed{\mathcal R_4^2=1.}
\]

The densitized source is therefore exactly equivalent to the Hilbert source.
It cannot hide or discard a species, trace or Poynting component. Twelve
random Lorentzian metric/source variations close the map, Jacobian, source
chain and involution below `2e-9` in the executable check.

For Maxwell, `T=0`, so its `H` source is simply `-T_EM/2`; the Poynting
components remain part of that same source.

## 5. Tree-level no-direct-flow theorem

The selected ordinary matter action has argument set

\[
\operatorname{Args}(S_{\rm SM})
=\{\mathcal H,\Phi_{\rm SM},\theta_{\rm SM}\}.
\]

The hidden set is

\[
\{\psi_r,\psi_a,X,u_{\rm bath},\rho_{\rm bath}\}.
\]

Their intersection is empty. At fixed `H`,

\[
\boxed{
\frac{\delta S_{\rm SM}}{\delta u_{\rm bath}^\mu}=0,
\qquad
\frac{\delta S_{\rm SM}}{\delta\psi}=0,
\qquad
\frac{\delta S_{\rm SM}}{\delta X}=0.
}
\]

Thus

\[
\boxed{J_{u,\mu}^{\rm SM}=0}
\]

at the matching action. This is a domain theorem for the written parent, not
an empirical cancellation.

At fixed external `H`, the path integral factorizes:

\[
Z[\mathcal H]
=Z_{\rm MTS+bath}[\mathcal H]Z_{\rm SM}[\mathcal H].
\]

After the metric is integrated, the first cross-sector interaction is

\[
\Gamma_{\rm cross}
\sim\frac1{M_R^2}
T_{\rm MTS}\,D_{\rm EH}\,T_{\rm SM}.
\]

This is ordinary universal gravitational exchange, not a separately tunable
flow charge.

## 6. Why minimal covariantization is not symmetry-unique

The construction above is clean, but covariance alone allows counteroperators
that vanish in the flat or no-flow presentation. Examples include

\[
\xi_H R H_{\rm SM}^\dagger H_{\rm SM},
\]

\[
\frac{b_u}{2}u^\mu u^\nu T_{\mu\nu},
\qquad
c_{Au}u^\mu u^\nu F^A_{\mu\alpha}F^A_\nu{}^\alpha,
\]

\[
c_{Hu}u^\mu u^\nu(D_\mu H_{\rm SM})^\dagger D_\nu H_{\rm SM},
\]

\[
c_{fu}u^\mu u^\nu\bar f\gamma_\mu iD_\nu f,
\qquad
\mu_f u_\mu\bar f\gamma^\mu f,
\]

and, if a hidden scalar invariant survives,

\[
f(I_X)F^2,
\qquad
m_A(I_X)\bar\psi_A\psi_A.
\]

All can be written in a Diff- and gauge-invariant way. Some require additional
discrete-symmetry or state assumptions, but ordinary covariance does not remove
the dimension-four anisotropic kinetic operators. The curvature-Higgs term
also proves non-uniqueness even without a flow spurion, although it may be moved
between EFT bases with correlated operators.

Therefore

\[
\boxed{
\mathrm{Diff}+G_{\rm SM}
\not\Longrightarrow
\text{unique minimal matter lift}.
}
\]

This explicitly confirms the obstruction found in checkpoints 1090--1091 and
prevents a no-hidden-visible-Hom axiom from being smuggled in as a theorem.

## 7. Radiative and state re-entry gate

The tree theorem does not automatically extend to every reduced 1PI action.
After selecting a bath state and integrating metric or hidden fluctuations,
the state supplies `u` or hidden scalar invariants. The operators in section 6
can then be generated unless a stronger symmetry, trivial invariant algebra,
or explicit matching calculation removes them.

The correct split is

```text
bare/renormalized matching action:
    J_u^SM = 0 exactly by selected field domain;

universal metric exchange:
    retained and owned by the same calibrated M_R;

mixed state-dependent local 1PI operators:
    coefficients not yet calculated;
    not set to theorem-zero;
    next derive-or-bound target.
```

An all-orders zero is therefore not claimed. The active baseline may continue
to use `Gamma_MTS,res=0` for calculations, but this is now accompanied by an
explicit re-entry basis and cannot support a public local-GR claim until the
mixed coefficients are calculated or empirically bounded.

## 8. Primitive ownership verdict

The parent field theory must declare its fields and coupling functor. The
following distinction is now fixed.

| object | status |
|---|---|
| integrated `H` and Diff | explicit primitive parent data |
| closed scalar-bath covariant action | constructed repair of the old scalar action |
| GR-parity Standard-Model lift | explicit primitive parent coupling functor |
| densitized source chain | derived exactly |
| universal source coefficient | derived from one action and calibrated `M_R` |
| tree direct-flow current | derived zero on the selected parent |
| all-orders flow/hidden current | open re-entry calculation/bound |
| numerical `G_N` | calibrated once, not predicted |
| strict scalar-only graviton/GR claim | rejected |

Calling the GR-parity lift primitive is not a hidden fitted closure: it adds no
arena-specific coefficient and is stated in the parent action before tests.
It is nevertheless not a derivation from `psi` alone. A deeper future theory
may derive this functor; the current framework must own it honestly as field
content.

## 9. Local-limit consequence

On the selected tree-level, two-derivative parent:

\[
M_R^2(G_{\mu\nu}+\Lambda g_{\mu\nu})=T^{\rm total}_{\mu\nu},
\qquad
G_N=\frac1{8\pi M_R^2},
\]

with

\[
\nabla_\mu T_{\rm total}^{\mu\nu}=0,
\qquad
T_{\rm EM}^{0i}=(\mathbf E\times\mathbf B)^i.
\]

This keeps the GR, Newton and Maxwell/Poynting route coherent and eliminates a
tree-level direct flow charge without pretending that every allowed mixed 1PI
operator has vanished.

## 10. Gate result

```text
RETAINED ACTION AUDIT                  = PASS
EXPLICIT COVARIANTIZATION MAP          = PASS
FLAT LIMIT                             = PASS
LOCAL LORENTZ REDUNDANCY               = PASS
H-DENSITY SOURCE CHAIN                 = PASS
TRACE-REVERSE INVERTIBILITY            = PASS
TREE DIRECT FLOW CHARGE                = ZERO DERIVED
UNIVERSAL METRIC EXCHANGE              = RETAINED
SYMMETRY UNIQUENESS                    = FAIL: COUNTEROPERATORS EXIST
PRIMITIVE MATTER FUNCTOR               = FROZEN EXPLICITLY
ALL-ORDERS MIXED OPERATOR ZERO         = NOT CLAIMED
PUBLIC UNIFIED-THEORY CLAIM            = BLOCKED
```

No GitHub action or public claim is authorized.

## Next target

`4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md`

Calculate the first mixed state-dependent matter operator generated by the
closed scalar-bath plus integrated-metric parent. Separate the universal
nonlocal graviton exchange from local 1PI counteroperators. If a coefficient
cannot yet be calculated, map the disformal, gauge, Higgs and fermion
anisotropy basis into existing PPN, clock, electromagnetic and local-Lorentz
bounds with no cancellation and no theorem-zero assumption.

## Sources

- `core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md`
- `post-checkpoint-work/4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md`
- `post-checkpoint-work/4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`
- `post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md`
- `post-checkpoint-work/1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md`
- `post-checkpoint-work/4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md`
- `post-checkpoint-work/4539-Y5-R2FR-parent-adopt-GR-parity-HQNP-selector-or-freeze-as-effective-local-GR-branch.md`
- `post-checkpoint-work/4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md`
- `post-checkpoint-work/4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4916_covariantization_map_and_flow_charge.py`
