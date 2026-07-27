# 4904 - Current unified action, Ward interfaces and prediction ledger

Marker: `MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904`

## Decision

The current framework can now be written as one internally consistent
low-energy field theory without adding the same physics twice:

\[
\boxed{
\Gamma_{\rm current}
=\Gamma_{\rm grav,R}[\widehat g(\mathcal H)]
+S_{\rm SM}[\widehat g(\mathcal H),\Phi_{\rm SM}]
+\Gamma_{\rm MTS,res}
+S_{\partial}+S_{\rm gf+gh}.
}
\]

The active baseline condition is

\[
\boxed{\Gamma_{\rm MTS,res}=0.}
\]

This does not delete the microscopic MTS programme. The proposed variables
`(psi_r,psi_a,X)` occupy the ultraviolet completion/matching layer and are
integrated once into the renormalized gravity coefficients and form factors.
The tested bath is not an active extra cosmological source after checkpoint
4896. A future nonzero MTS residual must be an independently derived covariant
operator that passes the re-entry gates.

The assembly closes the present structural goal:

- one integrated public metric;
- one Einstein stiffness and cosmological matching coefficient;
- one anomaly-free Standard-Model gauge/matter/Higgs action;
- QED and Maxwell as infrared limits of that action, not extra sectors;
- one total Hilbert source with closed Diff and gauge Ward identities;
- a declared boundary contract;
- a double-count-free parameter basis.

It also exposes the central remaining gap. The active GR+SM baseline contains
the usual nineteen Standard-Model parameters plus `G_N` and `Lambda_cal`, for
twenty-one empirical inputs before neutrino masses and higher EFT terms. The
current active novel MTS numerical-prediction count is zero. The programme has
real structural and conditional results, but competitiveness now requires one
nonzero parent-derived MTS operator with a frozen coefficient and an
independent observable.

## 1. Two-layer architecture

### 1.1 Microscopic proposal

The integrated-parent partition function has the schematic field space

\[
Z_{\rm parent}=\int
\frac{D\mathcal H\,D\psi_rD\psi_aDXD\Phi_{\rm SM}}
{\operatorname{Vol}(\mathrm{Diff}\times G_{\rm SM})}
\exp iS_{\rm parent}.
\]

All kinetic operators use

\[
\widehat g^{\mu\nu}
=\frac{\mathcal H^{\mu\nu}}{\sqrt{-\det\mathcal H}}.
\]

The microscopic MTS fields are not added again after their determinants and
matching contributions have been absorbed into renormalized coefficients.

### 1.2 Current low-energy action

The gravitational block is

\[
\begin{aligned}
\Gamma_{\rm grav,R}={}&\int d^4x\sqrt{-\widehat g}
\left[
\frac{M_R^2}{2}(\widehat R-2\Lambda_{\rm cal})
+a_R\widehat R^2+a_C\widehat C^2+a_E\widehat E_4
\right]\\
&+\Gamma_{\rm nonlocal}[\widehat g].
\end{aligned}
\]

The two-derivative baseline uses the calibrated `M_R,Lambda_cal`; curvature
and nonlocal terms are strict-EFT residuals with open matching coefficients.

The active matter block is

\[
\begin{aligned}
S_{\rm SM}=\int d^4x\sqrt{-\widehat g}\,[
&-\tfrac14G_A^2-\tfrac14W_I^2-\tfrac14B^2
-\frac{\theta_{\rm QCD}}{32\pi^2}G_A\widetilde G_A\\
&+\sum_f i\chi_f^\dagger\bar\sigma^\mu D_\mu\chi_f
+|D H|^2+\mu_H^2H^\dagger H-\lambda_H(H^\dagger H)^2
-\mathcal L_Y].
\end{aligned}
\]

The chiral representations are those audited at 4901 and are anomaly-free.
The active Higgs is the linear doublet fixed at 4903.

## 2. Active, frozen and retired sectors

| sector | current role | action status |
|---|---|---|
| integrated `H`/Diff | public metric field space | active architecture |
| renormalized gravity | GR, Newton, metric cosmology | active |
| chiral Standard Model | gauge, matter, linear Higgs | active correspondence |
| QED/Maxwell | post-EWSB low-energy limit | not an extra summand |
| microscopic MTS variables | proposed UV completion/matching | integrated out at current scale |
| `Gamma_MTS,res` | future non-GR operator slot | zero on active baseline |
| reciprocal bath cosmology | methods and failure evidence | retired source |
| `CP^2` Higgs | internal geometry clue | frozen |
| `SO(5)/SO(4)` Higgs | precision comparator | optional, inactive |
| galaxy programme | separate empirical pillar | not yet action-owned |

This table prevents historical work from silently re-entering the action.

## 3. Electromagnetism is a limit, not a second photon

At the full Standard-Model level the neutral gauge variables are `(W^3,B)`.
After electroweak breaking,

\[
\begin{pmatrix}A\\ Z\end{pmatrix}
=
\begin{pmatrix}
\sin\theta_W&\cos\theta_W\\
\cos\theta_W&-\sin\theta_W
\end{pmatrix}
\begin{pmatrix}W^3\\B\end{pmatrix}.
\]

The rotation is orthogonal and rank two. It preserves the field count:

\[
8+3+1=12
\quad\longrightarrow\quad
8+2+1+1=12.
\]

Therefore the checkpoint-4899 Maxwell connection and checkpoint-4900 Dirac
QED module are the infrared descriptions of the photon and recombined chiral
matter. Adding them beside `S_SM` would create a thirteenth gauge boson and
duplicate fermions.

The matching identities are

\[
Q=T_3+Y,
\qquad
e=g_2\sin\theta_W=g_Y\cos\theta_W.
\]

Consequently `alpha`, `g_2`, and `g_Y` are not three independent inputs. A
valid basis is either `(g_2,g_Y)` or `(alpha,sin^2 theta_W)` at a stated scale.

## 4. No-double-counting contract

The executable gate enforces ten identities:

1. `S_EM` is not added to `S_SM`;
2. post-EWSB Dirac fields are not added to the underlying chiral fields;
3. the Einstein term appears once;
4. `Lambda_cal` appears once;
5. only the linear Higgs is active;
6. microscopic determinants are absorbed into matching coefficients once;
7. the retired bath is absent from active cosmology;
8. the galaxy law is not inserted before an action map exists;
9. electromagnetic couplings use one independent basis;
10. `G_N` and `M_R` are one parameter through `G_N=1/(8pi M_R^2)`.

All ten close.

## 5. Diff and gauge Ward identities

Define the metric Euler tensor

\[
E_g^{\mu\nu}=\frac{2}{\sqrt{-g}}
\frac{\delta\Gamma}{\delta g_{\mu\nu}}.
\]

Diff invariance gives the off-shell identity

\[
2\nabla_\mu E_g^{\mu}{}_{\nu}
=\sum_i E_i\,\delta_\nu\Phi_i.
\]

On all matter/gauge/Higgs equations,

\[
\boxed{\nabla_\mu T_{\rm total}^{\mu}{}_{\nu}=0.}
\]

This is the same source required by the Bianchi identity

\[
\nabla_\mu(G^{\mu}{}_{\nu}+\Lambda_{\rm cal}\delta^\mu_\nu)=0.
\]

Gauge symmetry gives schematically

\[
D_\mu E_A^{a\mu}+E_\chi T^a\chi+E_HT^aH=0,
\]

and hence covariant current conservation on shell. The gauge Hilbert stress
obeys

\[
\nabla_\mu T_{\rm gauge}^{\mu\nu}
=-F_a^{\nu\mu}J^a_\mu,
\]

with the opposite Lorentz force in matter/Higgs stress.

The exchange incidence matrix for nodes `(gauge,fermion,Higgs,MTS_baseline)`
and edges `(gauge-fermion,gauge-Higgs,fermion-Higgs)` is

\[
B=\begin{pmatrix}
-1&-1&0\\
1&0&-1\\
0&1&1\\
0&0&0
\end{pmatrix}.
\]

Every column sums to zero and `rank(B)=2`. The first three sectors form one
connected exchange component; the current MTS residual is a second decoupled
component with `Q_MTS^nu=0`. A future MTS interaction must add an action edge
and equal-opposite exchange terms rather than a one-sided source.

## 6. Boundary contract

The variational problem includes:

- the Gibbons-Hawking-York term for the Einstein block;
- higher-derivative boundary completion or fixed derivative data before
  nonperturbative use of `R^2,C^2`;
- Euler boundary bookkeeping on bounded domains;
- consistent gauge flux or tangential-connection data;
- self-adjoint fermion and Dirichlet/Robin Higgs data;
- a new boundary derivation for every future MTS residual operator.

The strict two-derivative baseline is closed. The general nonperturbative
higher-derivative boundary problem remains open and is not hidden.

## 7. Independent parameter basis

The massless-neutrino GR+SM baseline has:

| block | independent physical inputs |
|---|---:|
| gravity stiffness `M_R` or `G_N` | 1 |
| renormalized `Lambda_cal` | 1 |
| Standard-Model gauge couplings | 3 |
| linear-Higgs block | 2 |
| charged masses and CKM | 13 |
| strong-CP angle | 1 |
| **total** | **21** |

The Standard-Model subtotal is the usual nineteen. `G_N` and `Lambda_cal` add
two. These are imported, calibrated or bounded inputs, not MTS numerical
predictions.

A Dirac-neutrino extension adds seven physical parameters; a Majorana branch
adds nine. At four-derivative gravity order, `a_R,a_C,a_E` add three matching
coefficients, while a general nonlocal/higher EFT contains functional or
unbounded additional data. These are not smuggled into the baseline count.

## 8. Known-limit ladder

The assembled action has a clean sequence:

```text
current action
  -> Gamma_MTS,res=0 and two-derivative gravity
  -> GR + chiral Standard Model
  -> weak stationary gravity: Newton and PPN
  -> homogeneous gravity: metric Lambda cosmology
  -> electroweak breaking: QCD + QED + massive W,Z,H
  -> low-energy classical limit: Maxwell + charged matter
```

Six known-limit gates close. Activating a novel nonzero MTS residual does not.

## 9. Prediction ledger

Current achievements fall into distinct evidential classes:

| class | examples | novel MTS numerical prediction? |
|---|---|---:|
| derived architecture | Diff field space, spin-2 pole, common Hilbert source | no |
| known-limit identities | Newton/PPN, photon count, anomalies, `rho=1` | no |
| conditional theorems | hypercharge rank, QED beta form, custodial coupling curve | no |
| global calibrations | `G_N`, `Lambda_cal`, nineteen SM parameters | no |
| active novel MTS numerical predictions | none | **0** |
| unmapped evidence pillars | galaxy work and quarantined cosmology methods | not yet |

This is not “nothing.” It is a coherent field-theory platform and a precise
account of what has actually been derived. It also means that the next useful
step cannot be another correspondence check. It must construct the smallest
nonzero symmetry-allowed MTS residual operator, derive its coefficient without
using the target observable, and test an independent consequence.

## 10. Arbitration

```text
CURRENT ACTION
    -> ONE DIFF-COVARIANT RENORMALIZED GR+SM EFT
    -> NO DUPLICATE PHOTON, HIGGS, GRAVITY OR BATH

WARD INTERFACES
    -> TOTAL HILBERT SOURCE CONSERVED
    -> GAUGE/HIGGS/FERMION EXCHANGES CANCEL
    -> MTS BASELINE DECOUPLED

PARAMETERS
    -> 19 SM + G_N + Lambda_cal = 21 BASELINE INPUTS
    -> NEUTRINO AND EFT EXTENSIONS OPEN

PREDICTIVITY
    -> STRUCTURAL PROGRESS REAL
    -> ACTIVE NOVEL MTS NUMERIC PREDICTION COUNT = 0
    -> FIRST NONTRIVIAL OPERATOR IS NOW THE PRIORITY
```

No GitHub action or public unified-theory claim follows from this checkpoint.

## Next target

`4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md`
