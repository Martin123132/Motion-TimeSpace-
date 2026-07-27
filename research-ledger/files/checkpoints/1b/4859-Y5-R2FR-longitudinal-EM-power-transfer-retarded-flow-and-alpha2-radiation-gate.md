# 4859 Y5 R2FR longitudinal EM power transfer, retarded flow and alpha2/radiation gate

Marker: `LONGITUDINAL_RETARDED_ALPHA2_RADIATION_4859`.

**Status:** The stationary result at 4858 now has an exact linear retarded continuation. The transverse electromagnetic momentum sources the positive-energy spin-1 mode, while the divergence/time-transfer part sources the positive-energy spin-0 mode. For a separately conserved weak electromagnetic subsource, the longitudinal metric maps to

\[
\alpha_{2,\rm EM}
=\beta_u\frac{3p-d}{p+d},
\qquad
|\alpha_{2,\rm EM}|\le1.8\times10^{-14}.
\]

Powered matter-EM exchange adds a distinct non-PPN potential and is not hidden inside that bound. The radiation calculation exposes the endpoint condition that had been missing: at fixed nonzero `beta_u`, both direct extra-mode power coefficients diverge as `beta_u^2/p`. The minimal regular route is

\[
\boxed{\beta_u=\zeta p,\qquad \zeta=O(1).}
\]

This makes the internal flow finite and the sourced vector/direct-scalar radiation coefficients vanish linearly with `p`. It is a derived regularity gate, not yet a primitive MTS coupling derivation.

**Decision:** `RETARDED_VECTOR_AND_DIRECT_SCALAR_KERNELS_DERIVED_WEAK_EM_ALPHA2_BOUNDED_POWERED_EXCHANGE_EXPLICIT_BETA_OVER_P_COSCALING_REQUIRED_PARENT_ORIGIN_STRONG_FIELD_OPEN_PRIVATE_NONCLAIM`.

## 1. Source split and conventions

Remain on the finite PPN-safe surface from 4857 and define

\[
D=d+p-dp,
\qquad
c_{14}=\frac{2dp}{d+p},
\qquad
c_{123}=\frac{2p^2}{3(d+p)},
\]

\[
q_S=\frac{3(1-p)D}{p^2},
\qquad
c_S^2=\frac{p}{3d(1-p)},
\qquad
c_V^2=\frac{D(d+p)}{4dp(1-p)}.
\]

The electromagnetic Hilbert momentum and direct flow charge remain separate:

\[
P_i^{\rm EM}=Z_A(\mathbf E\times\mathbf B)_i,
\qquad
J_i=\beta_uP_i^{\rm EM},
\qquad
\beta_u=\frac{\eta_u}{Z_A}.
\]

Write the Helmholtz split as `P_i=P_i^T+P_i^L`. The transverse component drives the spin-1 field. The longitudinal component enters through

\[
\boxed{\Sigma_{\rm EM}:=
\partial_t\Delta^{-1}\partial_iP_i^{\rm EM}.}
\]

The inverse Laplacian uses the isolated/decaying spatial boundary condition. In the radiation zone the equivalent Fourier projector is used, avoiding any false assumption that `Delta^-1 div P` has compact support.

## 2. Exact retarded transverse response

With the physical covariant flow tilt `W_i=B_i+v_i`, the full transverse quadratic action is

\[
16\pi G_{\ae}\mathcal L_V
=c_{14}\dot W_i\dot W_i
-c_1\partial_jW_i\partial_jW_i
+p\partial_jB_i\partial_jW_i
+\frac{1-p}{2}\partial_jB_i\partial_jB_i.
\]

The source term is

\[
\mathcal L_{\rm src}^{T}
=\beta_uP_i^TW_i+(1-\beta_u)P_i^TB_i.
\]

Varying the nondynamical shift gives

\[
\Delta B_i
=-\frac{p}{1-p}\Delta W_i
+\frac{16\pi G_{\ae}(1-\beta_u)}{1-p}P_i^T.
\]

Substitution into the flow equation yields

\[
\boxed{
c_{14}\ddot W_i
-\frac{D}{2(1-p)}\Delta W_i
=\frac{8\pi G_{\ae}(\beta_u-p)}{1-p}P_i^T.
}
\]

The speed is exactly `c_V`, so the outgoing solution is

\[
\boxed{
W_i(t,\mathbf x)
=\frac{4G_{\ae}(\beta_u-p)}{D}
\int\frac{P_i^T(t-R/c_V,\mathbf x')}{R}\,d^3x',
\qquad R=|\mathbf x-\mathbf x'|.
}
\]

Outside the source,

\[
B_i^{\rm rad}=-\frac{p}{1-p}W_i^{\rm rad}.
\]

The zero-frequency limit recovers the 4858 Poisson equation exactly; this is not a separate closure ansatz.

## 3. Longitudinal scalar action and power-transfer source

Use scalar gauge `h_0i=0`, `E=0`, write the spatial curvature perturbation as `psi`, and define the flow expansion perturbation

\[
\Theta:=\partial_iU_i.
\]

Direct second variation of the EH plus unit-flow owner, after eliminating the lapse but before eliminating `Theta`, gives

\[
16\pi G_{\ae}\mathcal L_S
=-3A\dot\psi^2-2A\dot\psi\Theta-c_{123}\Theta^2
-\frac{2(2-c_{14})}{c_{14}}(\nabla\psi)^2,
\]

where `A=2+c_theta=2-c14` on the safe surface. The direct source fixes the exact constraint

\[
\boxed{
c_{123}\Theta
=-A\dot\psi
-8\pi G_{\ae}\Delta^{-1}\partial_iJ_i.
}
\]

Eliminating `Theta` reproduces the primary reduced scalar action,

\[
S_S^{(2)}
=\frac1{8\pi G_{\ae}}
\int d^4x\,q_S
\left[\dot\psi^2-c_S^2(\nabla\psi)^2\right],
\]

and gives the sourced wave equation

\[
\boxed{
(\partial_t^2-c_S^2\Delta)\psi
=-\frac{4\pi G_{\ae}\beta_u}{1-p}\Sigma_{\rm EM}.
}
\]

Formally,

\[
\psi(t,\mathbf x)
=-\frac{G_{\ae}\beta_u}{(1-p)c_S^2}
\int\frac{\Sigma_{\rm EM}(t-R/c_S,\mathbf x')}{R}\,d^3x'.
\]

For a compact source the on-shell Fourier form is cleaner:

\[
\psi_{\rm rad}(\omega,r,\mathbf n)
=\frac{G_{\ae}\beta_u}{(1-p)c_Sr}
n_i\widetilde P_i^{\rm EM}
\left(\omega,\frac{\omega}{c_S}\mathbf n\right).
\]

Stationary divergence-free Poynting circulation has `Sigma_EM=0`; time-dependent longitudinal power transfer does not.

## 4. Exact weak-source alpha2 map

Foster and Jacobson's standard PPN gauge uses

\[
h_{0i,i}=-3\dot U+\theta_0n_{i,i},
\qquad
\theta_0=-\frac{c_1+2c_3-c_4}{2-c_{14}}.
\]

On the safe surface,

\[
\boxed{
\frac{G_{\ae}}{G_N}\frac{\theta_0}{c_{123}}=-\frac32.
}
\]

For a separately conserved electromagnetic subsource,

\[
\dot\rho_{\rm EM}+\partial_iP_i^{\rm EM}=0,
\]

the longitudinal constraint and gauge condition give

\[
\boxed{
\delta g_{0i}^{L}
=-\frac32\beta_u\chi_{,0i}.
}
\]

Here `Delta chi=-2U` and `chi_,0i=V_i-W_i^PPN=2V_i^L`. The standard difference is

\[
\delta g_{0i}
=\frac{\alpha_1}{2}V_i
-\frac{\alpha_2}{2}\chi_{,0i}.
\]

Combining this with the transverse coefficient from 4858,

\[
\alpha_{1,\rm EM}=-8\frac{d}{d+p}\beta_u,
\]

gives

\[
\boxed{
\alpha_{2,\rm EM}
=\frac{\alpha_{1,\rm EM}}2+3\beta_u
=\beta_u\frac{3p-d}{p+d}.
}
\]

Since `0<d/p<=1/3`,

\[
2\le\frac{3p-d}{p+d}<3.
\]

Using `|beta_u|<=6e-15`,

\[
\boxed{|\alpha_{2,\rm EM}|\le1.8\times10^{-14}.}
\]

This lies more than `1.1e5` below the weak-source `R6` comparator `2e-9`. It is a source-specific linear coefficient, not a universal or strong-field alpha2 pass.

The direct lapse response is even more suppressed. With `x=omega^2/k^2` and `U_EM` the Newton potential of the separately conserved EM energy,

\[
\boxed{
\frac{H_{\beta}}{U_{\rm EM}}
=-\frac{18\beta_udD\,x^2}
{(d+p)[p-3d(1-p)x]}.
}
\]

The order-`beta_u x` terms cancel; the first direct lapse correction is order `beta_u v^4` away from the scalar pole.

## 5. Powered EM is a separate observable

Define the local EM energy-exchange density

\[
\mathcal Q_{\rm EM}:=
\dot\rho_{\rm EM}+\partial_iP_i^{\rm EM}
\]

and its longitudinal potential

\[
\boxed{
\Xi_i:=8\pi G_N\partial_i\Delta^{-2}\mathcal Q_{\rm EM}.
}
\]

Then the leading weak longitudinal metric response is

\[
\boxed{
\delta g_{0i}^{L}
=-\frac32\beta_u\chi_{,0i}
+\frac32\beta_u\Xi_i.
}
\]

For a closed EM subsource `Xi_i=0`. In a powered circuit, plasma, antenna or matter-EM exchange region it need not vanish. The second term is not a universal PPN potential and must be evaluated from an actual source profile. Total matter-plus-EM conservation does not erase the fact that the constitutive flow charge is carried by the EM momentum sector.

## 6. Positive extra-mode self-power

Let

\[
Q_i^{\rm EM}:=\int P_i^{\rm EM}\,d^3x.
\]

The leading long-wavelength transverse projector obeys

\[
\int d\Omega\,
|\Pi_{ij}(\mathbf n)\dot Q_j|^2
=\frac{8\pi}{3}|\dot{\mathbf Q}|^2.
\]

The vector quadratic action therefore gives

\[
\boxed{
\mathcal P_V^{\rm dip}
=\frac{16G_{\ae}}3
c_{14}c_V\frac{(\beta_u-p)^2}{D^2}
|\dot{\mathbf Q}_{\rm EM}|^2.
}
\]

The direct constitutive scalar self-channel gives

\[
\boxed{
\mathcal P_{S,\beta}^{\rm dip}
=\frac{G_{\ae}q_S\beta_u^2}
{3(1-p)^2c_S}
|\dot{\mathbf Q}_{\rm EM}|^2.
}
\]

Both coefficients are nonnegative in the 4857 corridor. The first includes the linear Hilbert/direct EM momentum source combination. The second is only the direct `beta_u` scalar self-term: universal scalar sourcing, interference, nonlinear gravitational sources and compact-body sensitivities are not included. Consequently these are controlled linear radiation channels, not a binary-pulsar damping prediction.

At `p=1e-15`, `d=p/3`,

```text
D = 1.333333333333333e-15;
c14 = 5.0e-16;
cV = 1.154700538379252;
cS = 1.0000000000000005;
qS = 3.999999999999995e15.
```

The dimensionless coefficients multiplying `Gae |dot Q_EM|^2` are

```text
beta_u=-6.0e-15: C_V=8.48705e-14, C_S=4.80000e-14;
beta_u=0:        C_V=1.73205e-15, C_S=0;
beta_u=p:        C_V=0,           C_S=1.33333e-15;
beta_u=1.4e-15:  C_V=2.77128e-16, C_S=2.61333e-15.
```

These are coefficient diagnostics, not observational bounds, because no physical `dot Q_EM` source profile has yet been inserted.

## 7. Coupling co-scaling theorem

Approach the exact-GR endpoint along

\[
d=rp,
\qquad 0<r\le\frac13.
\]

At fixed nonzero `beta_u`,

\[
R_W\sim-\frac{\beta_u}{(1+r)p},
\]

and both displayed radiation coefficients scale as `beta_u^2/p`. The endpoint is therefore not uniformly regular in this EM sector even though the stationary metric residual remains tiny.

Now impose

\[
\boxed{\beta_u=\zeta p}
\]

with finite `zeta`. Then

\[
\boxed{
R_W\longrightarrow\frac{1-\zeta}{1+r},
\qquad
\delta_B=-\frac{r\zeta}{1+r}p\longrightarrow0.
}
\]

The radiation coefficients obey

\[
\boxed{
\frac{C_V}{p}\longrightarrow
\frac{16\sqrt r}{3(1+r)^2}(\zeta-1)^2,
}
\]

\[
\boxed{
\frac{C_S}{p}\longrightarrow
\sqrt{3r}(1+r)\zeta^2.
}
\]

Thus `beta_u=O(p)` is the minimal scaling that simultaneously keeps the linear internal transverse response finite and makes these direct EM extra-mode power coefficients vanish at the local-GR endpoint. The special value `zeta=1` cancels the transverse spin-1 source, but the direct scalar channel remains unless `zeta=0`; it is not a full-radiation zero.

The missing theorem has now changed shape. We no longer need an arbitrary lower `p` floor solely to control this linear EM response if the parent action derives a finite ratio

\[
\zeta=\frac{\beta_u}{p}.
\]

No current parent symmetry or coefficient equation derives that ratio. It remains the hard origin problem rather than being silently fitted.

## 8. Result and next test

Closed here:

```text
exact retarded transverse spin-1 Green operator;
exact longitudinal direct scalar constraint and wave operator;
stationary/divergence-free scalar-source zero;
separately conserved weak EM alpha2 map and 1.8e-14 bound;
powered-exchange Xi_i residual isolated rather than hidden;
positive vector and direct-scalar self-power coefficients;
proof that fixed beta_u is singular as p->0;
proof that beta_u=zeta p regularizes this linear EM endpoint.
```

Still open:

```text
parent derivation of finite zeta=beta_u/p;
first physical powered or radiative EM source profile for Xi_i and dot Q_EM;
universal scalar radiation and interference with the direct channel;
compact-body sensitivities and strong-field source charges;
nonlinear cutoff and backreaction;
regular gauge-restored/eliminated exact-GR endpoint;
primitive MTS origin of the EH, U1 and unit-flow coefficient surface.
```

Primary cross-checks: [Oost, Mukohyama and Wang](https://arxiv.org/abs/1802.04303), [Foster and Jacobson](https://arxiv.org/abs/gr-qc/0509083), and [Foster](https://arxiv.org/abs/gr-qc/0602004).

Next: `4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md`.

Resolution at 4860: minimal Maxwell propagation on the tensor characteristic metric gives the explicit nonzero law `beta_u=-p` (`zeta=-1`), while same-base-metric Maxwell gives the conservative `beta_u=0` branch. The relative messenger bound is on `epsilon_cone=beta_u+p`, not on `beta_u` independently.

Frame note at 4861: the selected public-`gHat` branch transforms all matter and gravity consistently. Its physical PPN values are the universal hatted coefficients; the direct scalar/vector rows here are retained as base-frame channel diagnostics and must not be double counted.
