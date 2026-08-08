# 4856 Y5 R2FR normalized time-flow Hilbert and preferred-frame gate

Marker: `TIME_FLOW_HILBERT_PREFERRED_FRAME_4856`.

**Status:** The previously symbolic direct Hilbert-response coefficient is now derived. Varying the normalized time-flow constraint and the `eta_u u u F F` operator together supplies a multiplier term that fixed-`u` metric variation alone misses. On the stationary aligned electric branch the complete contribution is exactly Maxwell stress with coefficient `eta_u`; therefore the static coefficient is `C_uT=1`, and the 4855 Reissner-Nordstrom exterior remains exact after replacing `Z_A` by `lambda_E=Z_A+eta_u`. The same variation shows that local Poynting flow is an exact source of the time-flow Euler equation. In a no-exterior-field stationary fixed point the entire `uF` preferred-frame source vanishes, but this does not close `alpha1` or `alpha2` because the healthy parent time/coframe kinetic owner required by 4847 is still unspecified.

**Decision:** `DIRECT_NORMALIZED_UFF_HILBERT_RESPONSE_AND_NO_FIELD_PPN_ZERO_DERIVED_PARENT_TIME_KINETIC_OWNER_OPEN_PRIVATE_NONCLAIM`.

## 1. Combined action and normalized-flow equation

Use the existing local correspondence action

\[
S_{G\lambda}=-\frac1\kappa\int d^4x\sqrt{-g}
\left[G(\theta)+\lambda_u(u^\mu u_\mu+1)\right],
\qquad \theta=\nabla_\mu u^\mu,
\]

together with

\[
S_{uF}=\frac{\eta_u}{2}\int d^4x\sqrt{-g}\,I,
\qquad
I=u^\mu u^\nu F_{\mu\alpha}F_\nu{}^\alpha.
\]

Define

\[
f=G_\theta,
\qquad
K_{\mu\nu}=F_{\mu\alpha}F_\nu{}^\alpha,
\qquad
V_\mu=u^\alpha F_{\alpha\mu},
\qquad I=V_\mu V^\mu.
\]

Variation with respect to the independent contravariant flow gives

\[
\boxed{
\nabla_\mu f-2\lambda_u u_\mu
+\kappa\eta_u K_{\mu\nu}u^\nu=0.
}
\]

Contracting with `u^mu` and using `u^2=-1` gives

\[
\boxed{
\lambda_u=-\frac12\left(\dot f+\kappa\eta_u I\right),
\qquad \dot f=u^\mu\nabla_\mu f.
}
\]

The spatial projection is

\[
\boxed{
D_\mu f=-\kappa\eta_u\mathcal S_\mu,
\qquad
\mathcal S_\mu=h_\mu{}^\rho K_{\rho\nu}u^\nu.
}
\]

In a local flow-rest frame, the executable symbolic decomposition gives

\[
\mathcal S_i=(\mathbf E\times\mathbf B)_i.
\]

Thus Poynting flow is an actual source of the time-flow equation. A vanishing net boundary flux does not imply `S_mu=0` pointwise; stationary circulating electromagnetic momentum can still excite the parent flow.

## 2. Multiplier-complete Hilbert tensor

Holding `u^mu` fixed during the metric variation, the direct constitutive term gives

\[
T^{(\eta,\mathrm{fixed}\ u)}_{\mu\nu}
=-\eta_uV_\mu V_\nu
+\frac{\eta_u}{2}g_{\mu\nu}I.
\]

Before using the flow equation, the memory-plus-constraint stress is

\[
\kappa T^{(G\lambda)}_{\mu\nu}
=\left[\nabla_\alpha(fu^\alpha)-G\right]g_{\mu\nu}
-2\lambda_u u_\mu u_\nu.
\]

Substituting the full multiplier equation and adding the direct metric variation yields

\[
\boxed{
\kappa T^{(\mathrm{flow}+uF)}_{\mu\nu}
=\left[\nabla_\alpha(fu^\alpha)-G\right]g_{\mu\nu}
+\dot f\,u_\mu u_\nu
+\kappa\eta_u\left(
Iu_\mu u_\nu-V_\mu V_\nu+\frac12g_{\mu\nu}I
\right).
}
\]

At the stationary local memory fixed point `G=f=dot f=0`,

\[
\boxed{
T^{uF}_{\mu\nu}=\eta_u\left(
Iu_\mu u_\nu-V_\mu V_\nu+\frac12g_{\mu\nu}I
\right).
}
\]

Its irreducible flow-frame components are

\[
\rho_{uF}=\frac{\eta_u I}{2},
\qquad q^{uF}_\mu=0,
\qquad p_{uF}=\frac{\eta_u I}{6},
\]

\[
\pi^{uF}_{\mu\nu}
=-\eta_u\left(V_\mu V_\nu-\frac13h_{\mu\nu}I\right),
\qquad {T^{uF\,\mu}}_\mu=0.
\]

The unit constraint is essential: omitting its on-shell multiplier contribution gives an incomplete source tensor.

## 3. Static electric closure and `C_uT`

For an aligned electrostatic field, `B=0`, so `S_mu=0`. In the flow-rest frame the tensor above is precisely the standard pure-electric Maxwell tensor multiplied by `eta_u`. Adding the `Z_A` Maxwell block therefore gives

\[
T^{(Z_A)}_{\mu\nu}+T^{uF}_{\mu\nu}
=T^{\rm Maxwell}_{\mu\nu}[\lambda_E],
\qquad
\lambda_E=Z_A+\eta_u.
\]

Hence

\[
\boxed{C_{uT}^{\rm direct}=1.}
\]

After canonical normalization,

\[
Q_c^2=\frac{g_J^2N_Q^2}{\lambda_E},
\]

so the exact 4855 Reissner-Nordstrom metric and its mass partition remain valid on this aligned no-Poynting branch even when `eta_u` is nonzero. This closes the direct static source response; it does not solve induced flow dynamics when `E cross B` is nonzero.

## 4. Preferred-frame split

If

\[
F_{\mu\nu}^{\rm ext}=0,
\qquad G=f=\dot f=0,
\]

then both the `uF` stress and its flow-Euler source vanish identically. Therefore this operator contributes

\[
\boxed{\alpha_1^{uF}=\alpha_2^{uF}=0}
\]

on the no-field local branch. This is a sector zero, not a full-theory PPN theorem: a dynamical preferred time flow can still generate preferred-frame solutions through its parent kinetic action.

For a source with electromagnetic energy fraction

\[
\epsilon_{\rm EM}=\frac{E_{\rm EM}}{M_{\rm ADM}c^2},
\]

the finite projection form is

\[
|\alpha_1^{uF}|\le C_1
\left|\frac{\eta_u}{\lambda_E}\right|\epsilon_{\rm EM},
\qquad
|\alpha_2^{uF}|\le C_2
\left|\frac{\eta_u}{\lambda_E}\right|\epsilon_{\rm EM}.
\]

Since

\[
\left|\frac{\eta_u}{\lambda_E}\right|
=\left|\frac{\kappa_u}{1+\kappa_u}\right|
\lesssim6.0\times10^{-15}
\]

under the 4854 propagation assumptions, reaching the existing conservative local envelopes would require approximately

\[
C_1\epsilon_{\rm EM}\gtrsim1.67\times10^{10},
\qquad
C_2\epsilon_{\rm EM}\gtrsim3.33\times10^5.
\]

These are pressure estimates only. The coefficients `C1,C2` are moving-source Green-response coefficients and are not assigned order unity as a claim.

## 5. Conditional parent kinetic completion map

The `G(theta)` block cannot by itself be the healthy kinetic owner of the time flow. If, conditionally, the missing two-derivative parent completion belongs to the general unit-timelike-vector/Einstein-aether class, its weak-field preferred-frame coefficients are

\[
\alpha_1=-\frac{8(c_3^2+c_1c_4)}{2c_1-c_1^2+c_3^2},
\]

\[
\alpha_2=\frac{\alpha_1}{2}
-\frac{(c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4)}
{(c_1+c_2+c_3)(2-c_1-c_4)}.
\]

Away from singular denominators, the exact joint PPN-zero surface is

\[
\boxed{
c_4=-\frac{c_3^2}{c_1},
\qquad
c_2=\frac{-2c_1^2-c_1c_3+c_3^2}{3c_1}.
}
\]

The runner verifies both substitutions symbolically and at a rational sample point. This is a completion gate, not adoption of Einstein-aether dynamics. PPN zero is insufficient by itself: mode kinetic signs, gradient stability, strong coupling, and the conditional post-GW170817 pressure `|c_1+c_3|<=10^-15` must be checked together.

## 6. Result and next obstruction

Closed here:

```text
direct aligned static normalized-u Hilbert response C_uT = 1;
exact Poynting source of the u Euler equation;
no-field uF contribution alpha1 = alpha2 = 0;
conditional algebraic PPN-safe surface for a general unit-vector completion.
```

Still open:

```text
parent-owned healthy time/coframe kinetic operator;
mode stability and strong-coupling control on any PPN-safe surface;
moving/rotating/magnetized source Green coefficients C1 and C2;
primitive parent derivation of EH/coframe;
external EM multipoles, radiation, open boundaries, charge quantization and QED.
```

Primary conditional-completion/comparator sources: [Foster and Jacobson, 2006](https://arxiv.org/abs/gr-qc/0509083), [Shao and Wex, 2012](https://arxiv.org/abs/1209.4503), [Shao et al., 2013](https://arxiv.org/abs/1307.2552), and [Oost et al., 2018](https://arxiv.org/abs/1802.04303).

Next: `4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md`.
