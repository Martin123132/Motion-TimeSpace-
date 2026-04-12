\documentclass[11pt]{article}

\usepackage{amsmath, amssymb, graphicx, geometry}
\geometry{margin=1in}

\title{A Density-Coupled Motion Field Model for Predictive Galaxy Rotation Curves Without Dark Matter}

\author{M. Ollett}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
We present a field-based framework for predicting galaxy rotation curves directly from baryonic structure without invoking dark matter halos or per-galaxy parameter fitting. The model introduces a scalar motion-support field governed by a nonlinear, density-dependent screening equation. Baryonic structure drives the field through a combination of gradient and local density terms, while rotation velocity is determined by the square-root of cumulative field support.

Applied to the SPARC rotation curve dataset, the model reduces median residuals from $\sim72$ km/s (baryonic-only) to $\sim17$ km/s. The framework naturally reproduces the baryonic Tully--Fisher relation (BTFR) and yields consistent scaling laws across galaxies. We interpret the results as evidence for a nonlinear medium in which gravitational response emerges from density-coupled field dynamics.
\end{abstract}

\section{Introduction}

Galaxy rotation curves have historically required either unseen mass components (dark matter halos) or modifications to gravitational laws to reconcile observations with baryonic matter.

In this work, we construct a predictive field model directly from baryonic structure, without per-galaxy tuning or additional matter components. The guiding principle is minimal: matter generates a field, the field propagates nonlinearly, and observable velocities emerge from cumulative field behaviour.

\section{Field Framework}

We define a scalar field $u(r)$ governed by:
\begin{equation}
\nabla^2 u - \beta \rho(r)^{1/2} u = -A \rho(r)
\end{equation}

where $\rho(r)$ is an effective baryonic source, $A$ is a coupling constant, and $\beta$ sets the screening strength.

\subsection{Variational Formulation}

The field equation arises from minimising:
\begin{equation}
E[u] = \int \left[
|\nabla u|^2 + \beta \rho^{1/2} u^2 - 2A \rho u
\right] dV
\end{equation}

\section{Source Construction}

Baryonic velocity is defined as:
\begin{equation}
V_{\text{bar}}^2 =
V_{\text{gas}}|V_{\text{gas}}|
+ \Upsilon_d V_{\text{disk}}|V_{\text{disk}}|
+ \Upsilon_b V_{\text{bul}}|V_{\text{bul}}|
\end{equation}

We define:
\begin{equation}
\rho_{\text{grad}} =
\frac{d}{dr}\left(\sqrt{r^2 + R_c^2}\,V_{\text{bar}}^2\right)/(r^2 + R_c^2)
\end{equation}

\begin{equation}
\rho_{\text{local}} \propto \frac{V_{\text{bar}}^2}{r}
\end{equation}

\begin{equation}
\rho = (1-\lambda)\rho_{\text{grad}} + \lambda \rho_{\text{local}}
\end{equation}

with $\lambda \approx 0.28$.

\section{Observable Mapping}

Define:
\begin{equation}
U(r) = \int_0^r u(s)\,ds
\end{equation}

Velocity is given by:
\begin{equation}
V(r) = V_{\text{flat}} \left(\frac{U(r)}{U_\infty}\right)^{1/2}
\end{equation}

\section{Method}

We apply the model to the SPARC ROTMOD dataset. For each galaxy:

\begin{enumerate}
\item Construct $\rho(r)$ from baryonic velocities
\item Solve the field equation numerically
\item Compute $U(r)$
\item Derive $V(r)$
\item Compare to observed rotation curves
\end{enumerate}

No per-galaxy parameters are adjusted.

\section{Results}

\subsection{Rotation Curve Fits}

Median RMSE:
\begin{itemize}
\item Baryonic: $\sim72$ km/s
\item Model: $\sim17$ km/s
\end{itemize}

\subsection{Scaling Relations}

We observe:
\begin{equation}
U_\infty \propto M, \quad C \propto M, \quad R_s \propto M^{-1/2}
\end{equation}

\subsection{Emergent BTFR}

\begin{equation}
V^2 \propto M \quad \Rightarrow \quad V^4 \propto M
\end{equation}

\section{Discussion}

The model introduces three key features:

\begin{itemize}
\item Density-dependent screening: $\sim \rho^{1/2}$
\item Mixed source driving: gradient + local density
\item Energy-based observable: $V^2 \propto U$
\end{itemize}

This differs from dark matter models (no halos) and MOND (no fixed acceleration scale).

\section{Limitations}

We do not derive $\beta$ or $\lambda$ from first principles, nor address cosmology or relativistic extensions.

\section{Conclusion}

A nonlinear, density-coupled motion field can reproduce galaxy rotation curves and scaling relations from baryonic input alone. This provides a predictive framework for galactic dynamics without dark matter.

\end{document}
