# Constraint ledger and independent heavy-field reconstruction

For the saved mode use the inherited definitions (conformal solver units):
\[
D=k^2+\mathrm{jac}/2,\quad
\Phi_H=(U-E/2-3\mathcal H J/(2k^2))/D,\quad
\Psi=\Phi_H+(\mathrm{shear}-Q)/k^2,\quad
\Phi'_M=J/(2k^2)-\mathcal H\Psi+F_q.
\]
The scalar \(F\) used below to build \(U\) is a **first-order** mode variable; the capital \(J\) above is the total source current at the order of the constraint test. They are not interchangeable. The diagnostic is \(R=\partial_\eta\Phi_H-\Phi'_M\). Its absolute gate uses \(\max_\eta |R|/\max_\eta|\Phi'_M|\), separately per seed. The numerator and denominator need not peak at the same epoch. No Fourier phases are rotated before differencing.

For each species, state or quadratic source separately, form its \(\Phi_i,\Psi_i,\Phi'_{M,i}\) with that run's actual time-dependent common denominator, then differentiate \(\Phi_i\) with the same spline as the saved readout. This includes both seeds' heavy energy and momentum, slow field, baryons, cold matter, photon intensity and current, collisionless multipoles and the recoupled 77-bin residual, plus \(U,Q,F_q\). All complex contributions sum back to both metric determinations. For matched minus explicit-wave surroundings, a peak share means \(\Re(\Delta R_i/\Delta R)\); a window share means \(\Re\int \Delta R_i\Delta R^* d\eta/\int|\Delta R|^2d\eta\). Negative shares can cancel positive ones. Neither is a Bayesian probability or a fraction of observed photons.

**Identify the geometric term.** Using the exact saved mode-pair contractions \(\mathcal C\), the implemented source is
\[
 U=-k^2\mathcal C(\phi,\phi)+2\,\mathrm{lap}(\phi,\phi)
     -\tfrac12\,\mathrm{grad}(\phi,\phi)+\tfrac32\mathcal C(F,F),\qquad
 F=-\frac{\mathrm{dgq}+(\mathrm{grho}+\mathrm{gpres})\sigma}{2k}.
\]
Here each input \(F\) uses its own mode wavenumber. The \(\sigma\) in its gauge transformation is not the output anisotropic stress. The audit reconstructs \(U\) on all saved post-switch forcing knots from the two native histories. For a difference of bilinear products the exact finite identity is \(\mathcal C(\Delta x,\bar y)+\mathcal C(\bar x,\Delta y)\) with arithmetic midpoints. Decomposing the metric denominator and expansion with the same product rule accounts for the small common-coefficient difference separately. The sign convention in the ranking tables is matched minus wave; the pressure restoration below goes in the reverse direction.

**Predict the change from heavy-field inputs.** In native conformal units let \(b\) be the homogeneous heavy field, \(v=b'\), \(m_h\) the saved mass. The native wave has \(p_h=(v^2-a^2m_h^2 b^2)/2\), \(\rho_h+p_h=v^2\), and synchronous momentum \(q_h=k v\,\delta b_{\rm syn}\). The matched native heavy background instead uses pressure zero, enthalpy \(\rho_\mathrm{match}/a\), and its saved fluid momentum \(q_{h,f}\). The diagnostic momentum was cross-checked against the field formula rather than inferred from the metric residual. Match at the same conformal time; use each branch's own background scale and keep the host shear fixed. On the matched host this gives the prediction
\[
 \delta F_h=-\frac{q_{h,w}-q_{h,f}+(v^2-\rho_\mathrm{match}/a_f)\sigma_f}{2k}.
\]
Use the opposite difference and the wave host's \(\sigma_w\) for removal. At the output wavenumber compute
\[
 \delta U_h=\tfrac32\big[\mathcal C(F,\delta F_h)+
              \mathcal C(\delta F_h,F)+\mathcal C(\delta F_h,\delta F_h)\big].
\]
This retains both cross terms and the square; no positive-real variance, sign assumption, or fitted amplitude substitutes for the complex mode coupling. The paired test does not read a donor \(U\) to build \(\delta U_h\); donor \(F^2\) and \(U\) are used for validation and separately labelled swaps. A pressure-only test instead changes just \(p\,\sigma\), not the synchronous current. It fails the metric gate.

**Interpretation.** Only the indicated forcing term is replaced. Matter, the metric constraints, both launches, and 77 collisionless bins are recoupled after each intervention. The cold baseline and the earlier photon histories remain sealed inputs. All runs stop their gravity driving at 89.6. A sign reversal on exchanging the source identifies the numerical cause in this retained construction. Restoring microscopic stress in one quadratic term is not yet a derivation that the effective theory must keep it there, or only there. A self-contained closure must derive the unresolved flux correlations in a common time slicing from its own state, not consult the post-switch wave as an oracle.

**Reproduction.** In this folder: run the matched and wave companion replays at p16 and p32, rank using `rank_sources_89.py`, reconstruct native `geometry_sources_89.py` inputs and run its rank mode, then build the pressure-only and paired heavy packets. The replay switches are `U`, `@u:flux_square`, `@u:F_pressure`, `@heavy-pressure`, and `@heavy-pair`. Each source test has a reverse case. Finally score transport, verify the controls, and check the stage manifest. Source paths and the native stress implementation hash are recorded with the packets. No new data collection is needed.
