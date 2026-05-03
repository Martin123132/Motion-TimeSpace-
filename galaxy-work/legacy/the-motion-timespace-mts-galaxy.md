\section*{The Motion--Timespace (MTS) Galaxy Law}
\subsection*{A Transport--Response Derivation for Disk Galaxies}

\subsection*{1. Framework}

We consider a scalar field
\[
\psi : \mathbb{R}^4 \to \mathbb{R},
\]
whose coarse-grained gradient covariance defines an emergent spacetime metric
\[
g_{\mu\nu} = \eta_{\mu\nu} + \langle \partial_\mu \psi , \partial_\nu \psi \rangle.
\]

Curvature--motion exchange is encoded in
\[
\Gamma = \mathcal{F}[\psi,g].
\]

The action is
\[
S = \int d^4x \sqrt{-g}
\Big[
\frac{1}{2\kappa}(R - 2\Gamma)
-\frac{Z_\Gamma}{2}\nabla_\mu \Gamma \nabla^\mu \Gamma
-U(\Gamma)
-\frac{Z_\psi}{2}\nabla_\mu \psi \nabla^\mu \psi
-W(\psi)
+\lambda(\Gamma - \mathcal{F}[\psi,g])
+\mathcal{L}_{\rm matter}
+\mathcal{L}_{\rm trans}
\Big].
\]

\subsection*{2. Transport Closure and Background Law}

The transport sector is
\[
\mathcal{L}_{\rm trans}
=
\mu \left(
u^\mu \nabla_\mu \chi
+
\frac{\chi}{\tau_\Gamma}
-
e_r^\alpha e_r^\beta \Sigma_{\alpha\beta}
\right),
\]

with isotropic closure
\[
\Sigma_{\mu\nu} = \frac{\Gamma}{4} g_{\mu\nu}.
\]

This yields
\[
u^\mu \nabla_\mu \chi + \frac{\chi}{\tau_\Gamma} = \frac{\Gamma}{4}.
\]

In the stationary outer-disk limit,
\[
v_\Gamma \frac{d\chi}{dr} + \frac{\chi}{\tau_\Gamma} = \frac{\Gamma_0}{4}.
\]

Defining
\[
L = v_\Gamma \tau_\Gamma,
\]

we obtain
\[
\chi(r) = \frac{\Gamma_0}{4} L \left(1 - e^{-r/L}\right).
\]

With
\[
\chi(r) = V^2(r) - V_{\rm bar}^2(r),
\]

\[
V^2(r) =
V_{\rm bar}^2(r)
+
\frac{\Gamma_0}{4} L \left(1 - e^{-r/L}\right).
\]

Using
\[
L = k \frac{j_{\rm bar}}{V_{\rm bar,char}}, \quad k \approx 0.9,
\]

and
\[
\Gamma_0 = \frac{cH_0}{2\pi},
\]

we obtain
\[
\Gamma_{\rm drive}^{(0)} = \frac{cH_0}{8\pi}.
\]

Thus
\[
V^2(r) =
V_{\rm bar}^2(r)
+
\frac{cH_0}{8\pi}
\left(k \frac{j_{\rm bar}}{V_{\rm bar,char}}\right)
\left[1 - \exp\!\left(-\frac{r V_{\rm bar,char}}{k j_{\rm bar}}\right)\right].
\]

\subsection*{3. Shape Correction}

Generalising the response,
\[
1-\exp[-(r/L)^q],
\]

with
\[
q \approx 1.3,
\]

improves LTG fits.

\subsection*{4. Linearized Correction Sector}

With
\[
\Gamma = \Gamma_{\rm bg} + \delta\Gamma,
\]

\[
(\nabla^2 - \ell_\Gamma^{-2})\delta\Gamma
=
-\frac{\delta S_\Gamma}{Z_\Gamma},
\quad
\ell_\Gamma=\sqrt{\frac{Z_\Gamma}{m_\Gamma^2}}.
\]

\subsection*{5. Bulge Correction}

For compact sources,
\[
\delta\Gamma_b \sim \frac{Q_b}{Z_\Gamma r_{\rm bul}}.
\]

Including gradient-sensitive closure,
\[
e_r^\mu e_r^\nu \Sigma_{\mu\nu}
=
\frac{\Gamma}{4}
+
\zeta\,\ell_\Gamma\, e_r^\mu \nabla_\mu \Gamma,
\]

gives
\[
\alpha_b \propto \left(\frac{r_{\rm disk}}{r_{\rm bul}}\right)^2.
\]

Empirically,
\[
1 + A_b\, b_{\rm frac}, \quad A_b \approx 0.4566.
\]

\subsection*{6. Gas Correction}

Transport memory obeys
\[
\frac{d\chi}{dt} + \frac{\chi}{\tau_\Gamma} = \frac{\Gamma_{\rm drive}(t)}{4}.
\]

Define
\[
z = (1-f_{\rm gas})\left|\ln\frac{h}{L}\right|.
\]

Preferred form:
\[
1 + A_g \left(1 - e^{-\lambda z}\right),
\]

\[
A_g \approx 1.0709, \quad \lambda \approx 0.4.
\]

\subsection*{7. Full LTG Law}

\[
V^2(r)=V_{\rm bar}^2(r)
+
\frac{cH_0}{8\pi}
\left[
1
+
0.4566\,b_{\rm frac}
+
1.0709\left(1-e^{-0.4(1-f_{\rm gas})|\ln(h/L)|}\right)
\right]
\left(
0.9\,\frac{j_{\rm bar}}{V_{\rm bar,char}}
\right)
\left[
1-\exp\!\left(
-\left(\frac{rV_{\rm bar,char}}{0.9\,j_{\rm bar}}\right)^{1.3}
\right)
\right].
\]

\subsection*{8. Results}

Clean LTGs:
\[
\text{RMSE} \sim 8\text{--}10\ \text{km/s}
\]

Full LTG sample:
\[
16.8 \to 15.8\ \text{km/s}
\]

Gas-poor LTGs:
\[
17.3 \to 15.7\ \text{km/s}
\]

ETGs:
\[
\gtrsim 49\ \text{km/s}
\]

\subsection*{9. Interpretation}

\begin{itemize}
\item Background law governs disk galaxies
\item Corrections arise from structure
\item Shape distinguishes populations
\item ETGs require a different response family
\end{itemize}

\subsection*{10. Conclusion}

\[
\boxed{
\text{Disk galaxy rotation curves follow a cosmologically normalised transport-response law with structural corrections.}
}
\]
