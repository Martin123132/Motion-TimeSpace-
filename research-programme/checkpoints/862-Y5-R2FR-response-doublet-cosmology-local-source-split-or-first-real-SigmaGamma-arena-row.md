# 4846 Y5 R2FR response-doublet cosmology/local split and coherent-load action

**Status:** A same-law local/FLRW action candidate is now constructed. The exchange-odd response field cannot analytically produce the required cubic endpoint by itself. The repaired candidate separates the exchange-even coherent volume load \(Q^\mu{}_\nu\) from the exchange-odd local response \(Z\). An action-level auxiliary constraint makes \(\det_3Q\) active on FLRW expansion and exactly zero on a stationary Killing branch, without a local/cosmological environment switch.

**Decision:** `ANALYTIC_ODD_RESPONSE_CUBIC_NO_GO_PROVED_AUXILIARY_COHERENT_LOAD_ACTION_GIVES_SAME_LAW_LOCAL_ZERO_FLRW_ACTIVE_H_LOAD_BRANCH_PRIVATE_NONCLAIM`.

## 1. Endpoint-power obstruction

Let \(s\) be a regular signed activation variable with \(s=0\) at the local fixed point. If the 4845 response carrier is exchange odd,

\[
Z(-s)=-Z(s),
\]

and its scalar density is analytic and exchange even, then

\[
\Gamma_Z(Z)=c_2 Z^2+c_4 Z^4+\cdots.
\]

If \(Z=z_p s^p+O(s^{p+2})\), every leading power in \(\Gamma_Z\) is even:

\[
\Gamma_Z=O(s^{2p}).
\]

For analytic odd \(Z\), \(p\) is odd and \(2p\in\{2,6,10,\ldots\}\). Therefore a regular exchange-even \(Z\) density cannot produce the existing cubic endpoint

\[
F(s)=s^3+O(s^6).
\]

The formal escape \(Z\sim s^{3/2}\) is nonanalytic at the origin and is rejected. The 4845 sentence suggesting that cosmological history should simply source \(Z\) is therefore too narrow: \(Z\) can remain the locally suppressed odd mode, but it cannot be the sole analytic owner of the cubic memory law.

## 2. Even/odd response decomposition

Use the response pair as

\[
R_+ = Q+Z,\qquad R_- = Q-Z.
\]

Under response exchange,

\[
Q\mapsto Q,\qquad Z\mapsto-Z.
\]

The cubic determinant of \(Q\) is compatible with exchange symmetry because \(Q\), unlike \(Z\), is exchange even.

Let the observed-time flow be

\[
u^\mu=\frac{\tau_{\rm obs}^\mu}
{\sqrt{-g_{\alpha\beta}\tau_{\rm obs}^\alpha\tau_{\rm obs}^\beta}},
\qquad
h^\mu{}_\nu=\delta^\mu{}_\nu+u^\mu u_\nu,
\qquad
\theta=\nabla_\mu u^\mu,
\]

in \(c=1\) units. The same \(\tau_{\rm obs}\) must serve sources, clocks, photons and orbits; otherwise this is merely a chosen preferred frame.

Take \(Q^\mu{}_\nu\) to be spatial:

\[
Q=hQh.
\]

Its covariant three-dimensional determinant is

\[
I_Q=\det{}_3Q
=\frac{1}{6}\left[
(\operatorname{Tr}_hQ)^3
-3\operatorname{Tr}_hQ\,\operatorname{Tr}_h(Q^2)
+2\operatorname{Tr}_h(Q^3)
\right].
\]

On the isotropic branch \(Q=s\,h\), this gives exactly

\[
I_Q=s^3.
\]

## 3. Auxiliary coherent-load action

Introduce a spatial multiplier \(\Lambda^\nu{}_\mu\) and the local constraint

\[
\mathcal C_Q{}^\mu{}_\nu
=Q^\mu{}_\nu-\frac{\ell_Q\theta}{3}h^\mu{}_\nu.
\]

The combined private candidate is

\[
\Gamma_{\rm eff}
=\Gamma_0
+\Gamma_\star F(I_Q)
+\Lambda^\nu{}_\mu\mathcal C_Q{}^\mu{}_\nu
+\Gamma_Z[Z],
\]

\[
S_\Gamma=-\frac{1}{\kappa}\int d^4x\sqrt{-g}\,\Gamma_{\rm eff}.
\]

Here \([\Gamma_0]=[\Gamma_\star]=L^{-2}\), \([\ell_Q]=L\), \(Q\) is dimensionless and \([\Lambda]=L^{-2}\).

Variation gives

\[
\frac{\delta S}{\delta\Lambda}=0
\quad\Longrightarrow\quad
Q=\frac{\ell_Q\theta}{3}h,
\]

and

\[
\frac{\delta S}{\delta Q}=0
\quad\Longrightarrow\quad
\Lambda=-\Gamma_\star F'(I_Q)\operatorname{Cof}_h(Q).
\]

For \(Q=s h\),

\[
\operatorname{Cof}_h(Q)=s^2h,
\]

so the multiplier begins at \(O(s^2)\). It must be retained during metric and \(u\)-variation; dropping it would hide the stress that makes the action Bianchi consistent.

After the auxiliary equations are imposed,

\[
\Gamma_{\rm mem,on-shell}
=\Gamma_\star F\!\left[\left(\frac{\ell_Q\theta}{3}\right)^3\right].
\]

This is a local covariant volume-load law. It does not use a fitted domain, an after-the-fact projector, or a local/FLRW switch.

## 4. Exact stationary local branch

Let \(k^\mu\) be the parent stationary Killing generator and

\[
u^\mu=k^\mu/N,\qquad N=\sqrt{-k^2}.
\]

Then

\[
\nabla_\mu u^\mu
=N^{-1}\nabla_\mu k^\mu+k^\mu\nabla_\mu(N^{-1})=0,
\]

because a Killing vector has zero divergence and its norm is constant along its own flow.

Therefore

\[
\theta=0
\Longrightarrow
Q=0,\quad I_Q=0,\quad \operatorname{Cof}(Q)=0,\quad\Lambda=0.
\]

For either retained kernel,

\[
F(0)=0,\qquad
\frac{dF(s^3)}{ds}\bigg|_{s=0}=0.
\]

Together with the 4845 positive-action theorem for \(Z\),

\[
Z=0,
\]

the active sector satisfies

\[
\Gamma_{\rm active}=0,\qquad
\Pi_{\rm active}=0,\qquad
\Sigma_{\rm active}=0,\qquad
q_{\rm active}^\nu=0.
\]

This is an exact theorem on the private candidate branch, conditional on the single observed-time generator actually being parent owned and Killing in the tested local solution. \(\Gamma_0\) remains as the separately scored cosmological background.

For finite nonstationarity, let

\[
s=\ell_Q\theta/3.
\]

Near \(s=0\),

\[
\Gamma_{\rm mem}/\Gamma_\star=s^3+O(s^6),
\qquad
\frac{1}{\Gamma_\star}\frac{d\Gamma_{\rm mem}}{ds}
=3s^2+O(s^5).
\]

The local action correction is cubic and its field response is quadratically suppressed. A physical PPN/clock/orbital bound still requires the same-frame profile of \(\theta\), \(\ell_Q\), \(\Gamma_\star\), and the full \(u\)-variation.

## 5. FLRW reduction and metric response

For comoving FLRW,

\[
\theta=3H,\qquad
Q^\mu{}_\nu=\ell_QH\,h^\mu{}_\nu,\qquad
y=I_Q=(\ell_QH)^3.
\]

Hence

\[
\Gamma_{\rm mem}(H)=\Gamma_\star F(y).
\]

It is not consistent to identify this function directly with an energy density. Variation of the lapse and scale factor gives

\[
\kappa\rho_{\rm mem}
=\Gamma_{\rm mem}-H\Gamma_{{\rm mem},H},
\]

\[
\kappa p_{\rm mem}
=-\Gamma_{\rm mem}+H\Gamma_{{\rm mem},H}
+\frac{1}{3}\frac{d\Gamma_{{\rm mem},H}}{dt}.
\]

For a general \(F(y)\), with

\[
\epsilon_H=\dot H/H^2,
\]

these become

\[
\frac{\kappa\rho_{\rm mem}}{\Gamma_\star}
=F-3yF',
\]

\[
\frac{\kappa p_{\rm mem}}{\Gamma_\star}
=-F+3yF'
+y\epsilon_H(2F'+3yF'').
\]

The pressure is therefore action-derived and obeys the FLRW continuity identity. This also exposes a major correction to the older effective-fluid treatment: the metric response term \(-3yF'\) cannot be discarded.

## 6. Kernel result

Two kernels were tested:

\[
F_+(y)=1-e^{-y},
\]

and

\[
F_{\rm safe}(y)=\tanh y.
\]

Both have the required cubic local endpoint after \(y=s^3\). The exponential kernel is acceptable only on the expanding \(y\ge0\) branch because it is unbounded for large negative \(y\). The hyperbolic-tangent completion is bounded under expansion and contraction.

For positive \(\Gamma_\star\), the action-derived FLRW density changes sign at

\[
y_{\rho=0}=1.9038136944403834
\]

for \(1-e^{-y}\), and

\[
y_{\rho=0}=1.4192231900240135
\]

for \(\tanh y\). This is not a fit or a viability claim. It is a new sign/scale gate: the sign of \(\Gamma_\star\) and the value of \(\ell_QH\) cannot be chosen without checking the full cosmological solution.

## 7. What this replaces

The derived local action predicts

\[
I_Q=(\ell_QH)^3,
\]

not

\[
I_M=(N/u_3)^3.
\]

The old \(N/u_3\) memory shape remains a conditional nonlocal/domain-history construction. It is not derived by this checkpoint and must not be silently relabelled as the new action.

The new branch is more fundamental but empirically untested. It now needs a direct comparison against the old \(N\)-memory model, \(\Lambda\)CDM, \(w\)CDM and CPL.

## 8. Scope and remaining theorem burden

This checkpoint closes the analytic parity problem and constructs one same-action local/FLRW mechanism. It does not yet prove:

1. that \(\tau_{\rm obs}\) is the unique parent source/clock/orbit generator;
2. that its local solution is Killing in every PPN arena;
3. the MTS origin of \(\ell_Q\) and \(\Gamma_\star\);
4. the full covariant Hilbert stress and \(u/\tau\) Euler equation away from FLRW;
5. a cosmological data preference for the \(H\)-load law;
6. Maxwell/EM or the remaining non-\(\Gamma\) PPN residuals.

The action is therefore private and nonclaim, but the central split is no longer a plateau axiom or an environment switch.

## 9. Machine results

- `P8_Y5_R2FR_4846_ENDPOINT_OBSTRUCTION.csv`: proves the response-parity obstruction.
- `P8_Y5_R2FR_4846_ACTION_CONSTRUCTION.csv`: records the candidate action and Euler equations.
- `P8_Y5_R2FR_4846_BRANCH_OUTPUT.csv`: separates global adoption, exact private local theorem, finite nonstationary branch and forbidden hand switch.
- `P8_Y5_R2FR_4846_LOCAL_ENDPOINT_OUTPUT.csv`: verifies cubic action and quadratic field response.
- `P8_Y5_R2FR_4846_FLRW_STRESS_OUTPUT.csv`: evaluates the action-derived density/pressure and sign roots.

All rows remain `valid_for_claim=false`.

## 10. Next target

`4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md`
