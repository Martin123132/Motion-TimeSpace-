# 4853 Y5 R2FR Maxwell/U1 stress, current and stationary-Poynting rebase

**Status:** The scalar-only Maxwell route is rejected. The core MTS `psi` field is audited as a real scalar, while the archived pre-charge EM equation is parabolic and explicitly lacks charge, Coulomb force, radiation pressure and polarization response. A smooth complex phase gradient is pure gauge and cannot repair this. The competitive correspondence spine therefore requires an explicit parent `U(1)` connection sector. Once that field content is stated, Maxwell equations, two transverse modes, Hilbert stress, current conservation, matter-EM exchange and stationary Poynting routing follow from one action. The remaining hard problem is the parent origin or adoption of the connection and symmetry-legal MTS constitutive couplings.

**Decision:** `SCALAR_MAXWELL_ROUTE_REJECTED_MINIMAL_PARENT_U1_CORRESPONDENCE_ACTION_DERIVES_MAXWELL_STRESS_CURRENT_TWO_MODES_AND_STATIONARY_POYNTING_ROUTING_PARENT_ORIGIN_AND_CONSTITUTIVE_TERMS_OPEN_NONCLAIM`.

Marker: `SCALAR_ONLY_MAXWELL_NO_GO`.

## 1. Why the current scalar branch is not Maxwell

The core audit identifies

\[
\psi:\mathbb R^4\rightarrow\mathbb R
\]

as a fundamental scalar candidate. A linear perturbation of a Lorentz scalar carries helicity zero. A photon requires two transverse helicities, a Gauss constraint and a local gauge redundancy. Calling a scalar oscillation “transverse” does not change its representation.

The archived pre-charge equation is

\[
\partial_t\psi=c^2\nabla^2\psi-\lambda\psi|\psi|^{1/3}-\Gamma\psi.
\]

Its principal part is first order in time and second order in space, so it is a diffusion/relaxation equation rather than the hyperbolic Maxwell wave system. The source document itself reports no Coulomb force, charge differentiation, radiation pressure, polarization force or resonant charge response.

Complexifying the field does not solve the connection problem. If

\[
\psi=\rho e^{i\theta_Q},
\qquad
\Pi_Q=\frac{\operatorname{Im}(\psi^*d\psi)}{\rho^2}=d\theta_Q,
\]

then the previous reconstruction

\[
A=q_*^{-1}(d\theta_Q-\Pi_Q)
\]

gives `A=0` and `F=dA=0` on a smooth patch. Defining `Pi_Q=dtheta_Q-q_*A` instead already assumes `A` and is circular.

Therefore:

\[
\boxed{\text{current scalar/pre-charge MTS}\not\Rightarrow\text{Maxwell}.}
\]

The pre-charge simulations remain potentially useful dissipative scalar analogues. They are not the photon sector of the formal field theory.

## 2. Minimal honest field-content extension

The competitive correspondence action now requires a connection on a principal `U(1)` bundle:

\[
A\in\Omega^1(M),
\qquad
F=dA,
\qquad
A\mapsto A+d\chi.
\]

This is not claimed to emerge from the current scalar. It is an explicit field of the correspondence framework, just as the coframe/connection and matter fields are explicit. The 3783-3786 two-Clebsch-pair/`CP^2` Berry route remains a possible future derivation of this connection from a richer MTS internal multiplet.

The local parent correspondence action is

\[
S_{\rm corr}=S_{\rm EC/EH}[e,\omega]
+S_{\rm MTS}[\psi,\Gamma,u,Q,Z]
+S_A[A,g_{\rm obs}]
+S_{\rm charged}[\Psi,A,g_{\rm obs}]
+S_{\rm boundary},
\]

with

\[
\boxed{
S_A+S_{\rm int}
=\int d^4x\sqrt{-g}\left[-\frac{\lambda_A}{4}F_{\mu\nu}F^{\mu\nu}
-g_JA_\mu j^\mu\right].
}
\]

This is the minimal classical Maxwell correspondence branch. It does not predict the numerical value of the electromagnetic coupling.

## 3. Operator classification

Assume on the local branch:

1. diffeomorphism and local Lorentz invariance;
2. `U(1)` gauge invariance;
3. locality, parity evenness and at most two derivatives;
4. an action quadratic in `A`;
5. no additional constitutive tensor or active field inserted into the photon kinetic term.

Gauge invariance requires `A` to enter through `F`. In four dimensions the metric and orientation produce

\[
F_{\mu\nu}F^{\mu\nu}
\quad\text{and}\quad
F_{\mu\nu}\widetilde F^{\mu\nu}.
\]

The second term with constant coefficient is topological and has no local Hilbert stress. Consequently the parity-even local kinetic term is uniquely `F^2` within this operator domain.

This theorem does not globalize by symmetry alone. The MTS time flow permits legal operators such as

\[
u^\mu u^\nu F_{\mu\alpha}F_\nu{}^\alpha,
\]

and active scalars permit `f(X)F^2`. Those are explicit constitutive residuals unless the parent action excludes them. Gauge invariance alone does not kill them. General gauge-invariant Lorentz-violating photon operators and their dispersion/birefringence signatures are independently classified by [Kostelecký and Mewes](https://arxiv.org/abs/0905.0031).

## 4. Maxwell and charge equations

Variation of `A_nu` gives

\[
\boxed{\lambda_A\nabla_\mu F^{\mu\nu}=g_Jj^\nu.}
\]

Together with `F=dA`,

\[
\boxed{\nabla_{[\alpha}F_{\mu\nu]}=0.}
\]

Taking a divergence gives

\[
\boxed{\nabla_\nu j^\nu=0}
\]

when `g_J` and `lambda_A` are constants on the local branch. The same result is the Ward identity of the charged matter action.

## 5. Two photon modes and the observed light cone

The connection has four components. One first-class gauge freedom and its Gauss constraint remove two canonical pairs, leaving

\[
\boxed{N_{\rm photon}=2.}
\]

For `lambda_A>0` the Hamiltonian density is positive,

\[
\rho_A=\frac{\lambda_A}{2}(E^2+B^2),
\]

and the principal equation in Lorenz gauge is

\[
g_{\rm obs}^{\alpha\beta}\nabla_\alpha\nabla_\beta A_\mu+\text{curvature/lower-order terms}=0.
\]

Thus the two photon polarizations propagate on the same observed metric null cone in the minimal branch. This is the Maxwell limit that a scalar mode could not supply.

## 6. Hilbert stress and source ownership

Metric variation gives

\[
\boxed{
T_A^{\mu\nu}=\lambda_A\left(
F^\mu{}_{\alpha}F^{\nu\alpha}
-\frac14g^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}
\right).
}
\]

This tensor is varied from the same observed metric used by the EH block and matter. It therefore enters the source exactly once:

\[
T_H^{\mu\nu}=T_{\rm matter}^{\mu\nu}+T_A^{\mu\nu}
+T_{\rm binding}^{\mu\nu}+\cdots.
\]

Using the Maxwell equation,

\[
\nabla_\mu T_A^{\mu\nu}
=-g_JF^\nu{}_{\lambda}j^\lambda,
\]

while the charged-matter Ward identity gives

\[
\nabla_\mu T_{\rm matter}^{\mu\nu}
=+g_JF^\nu{}_{\lambda}j^\lambda.
\]

Hence

\[
\boxed{\nabla_\mu T_{\rm total}^{\mu\nu}=0.}
\]

The Lorentz force is internal exchange, not an independent non-Hilbert source.

## 7. Coupling normalization

Canonical normalization is

\[
A_c=\sqrt{\lambda_A}A,
\qquad
e_{\rm eff}=\frac{g_J}{\sqrt{\lambda_A}}.
\]

Therefore the physical classical coupling obeys

\[
\boxed{\alpha_{\rm eff}\propto\frac{g_J^2}{\lambda_A}.}
\]

Under `A'=sA`,

\[
\lambda_A'=\lambda_A/s^2,
\qquad
g_J'=g_J/s,
\]

so `g_J^2/lambda_A` is invariant. One EM coupling may be calibrated exactly as one gravitational coupling is calibrated. A field normalization or compact charge label does not predict the number `alpha`.

## 8. Poynting is stress transport, not a second source

For an observer `u`,

\[
E_\mu=F_{\mu\nu}u^\nu,
\qquad
B_\mu=({}^\star F)_{\mu\nu}u^\nu,
\]

and the spatial energy flux is

\[
\boxed{S^\mu=-h^\mu{}_{\alpha}T_A^{\alpha\beta}u_\beta
=\lambda_A(E\times B)^\mu.}
\]

Thus Poynting flow is the `0i` component of the same Hilbert tensor. Adding it again as an MTS force or source would double count it.

## 9. Stationary boundary theorem

Let `xi` be the stationary observed-time Killing field and define

\[
J_E^\mu=-T_{\rm total}^{\mu}{}_{\nu}\xi^\nu.
\]

When the equations hold and `L_xi` annihilates the fields,

\[
\nabla_\mu J_E^\mu=0.
\]

Integrating over a worldtube gives

\[
\Delta E_{\rm total}+\int_{\partial W}J_E^\mu n_\mu d\Sigma=0.
\]

For a stationary isolated source, `Delta E_total=0`, no matter crosses the wall, and bound finite-energy fields have faster-than-radiative falloff. For example `E=O(R^-2)` and `B=O(R^-3)` give an absolute surface-flux envelope `O(R^-3)`. Therefore

\[
\boxed{\lim_{R\to\infty}\oint_{S_R}S\cdot dA=0}
\]

for the stationary bound-field branch. Local Poynting circulation may remain and stays inside `T_A`.

Radiative fields instead have `E,B=O(R^-1)`, so their integrated flux can remain finite. The theorem does not erase radiation:

\[
\Phi_{\rm rad}=\int dt\oint S\cdot dA
\]

remains an explicit open-system/Hamiltonian mass-change term.

## 10. MTS constitutive residual

In an isotropic observed frame write

\[
\mathcal L_A=\frac{\lambda_A}{2}
\left[(1+\chi_E)E^2-(1+\chi_B)B^2\right].
\]

Then

\[
\boxed{\frac{c_\gamma^2}{c_{\rm obs}^2}
=\frac{1+\chi_B}{1+\chi_E}.}
\]

A common `chi_E=chi_B` is a normalization shift. Their difference changes photon speed; tensor coefficients generate anisotropy or birefringence. This is the correct empirical target if the MTS time flow couples directly to `F`.

For analytic scalar couplings `f(X)F^2`, the exact stationary zeroes `Gamma_active=theta=Q=Z=0` imply `f(X)=f(0)` on the local background, and `f(0)` is absorbed into `lambda_A`. Fluctuation, transition and cosmological vertices remain live. The nonzero normalized time flow `u` is different: `u u F F` does not vanish merely because `theta=0`.

## 11. Rebased EM result

Inside the explicit minimal `U(1)` correspondence branch, the following now follow from the action rather than closure assumptions:

```text
Maxwell equations
two transverse photon modes
same-observed-metric Hodge star
positive Maxwell energy for lambda_A>0
Hilbert stress included once
same-current Ward exchange
stationary nonradiative net Poynting flux = 0
physical coupling = g_J^2/lambda_A, calibrated once
```

The remaining vector is

```text
E_U1_origin
E_Hodge/time-flow constitutive tensor
E_XF2_dynamic outside the stationary silent background
E_alpha_absolute/charge-lattice origin
E_radiative_flux on open branches
E_QED_quantum completion
```

The central architectural correction is explicit: MTS can presently be an Einstein-Maxwell-compatible multi-field theory, but it cannot honestly claim that its current scalar alone derives photons.

## Next target

`4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md`

