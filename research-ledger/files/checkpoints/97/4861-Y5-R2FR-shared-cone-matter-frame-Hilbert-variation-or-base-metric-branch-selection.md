# 4861 Y5 R2FR shared-cone matter-frame Hilbert variation or base-metric branch selection

Marker: `PUBLIC_FRAME_VARIATION_SELECTION_4861`.

**Status:** The matter-frame fork is no longer left unresolved. The shared characteristic metric

\[
\widehat g^{\mu\nu}=g^{\mu\nu}+p u^\mu u^\nu
\]

is selected as the lead private public metric for rods, clocks, photons, free fall and Hilbert source readout. Varying one matter action `S_matter[Psi,A,gHat]` proves that the apparent `beta_u=-p` electromagnetic flow charge in the base variables is one component of a universal induced source carried by every matter momentum flux. It is not a photon-only patch.

Transforming the complete 4857 gravity coefficients into the public frame gives `c13_hat=0` while `c14_hat` and `c123_hat` remain finite and positive. Tensor and photon modes are exactly luminal; scalar and vector modes remain positive and at least luminal. The physical public-frame PPN coefficients are

\[
\widehat\alpha_1=-\frac{8dp}{d+p},
\qquad
\widehat\alpha_2=\frac{d(3d-p)}{d+p},
\]

and

\[
\frac{\widehat G_{\rm cos}}{\widehat G_N}=1-p.
\]

These replace, rather than add to, the source-specific base-frame EM projections. On the retained `p<=1e-15` working corridor they are negligible. The remaining hard targets are now quantitative: obtain an independent absolute bound on `p` in the public frame and derive the nonlinear strong-coupling cutoff or gauge-restoration mechanism.

**Decision:** `PUBLIC_GHAT_SELECTED_AS_LEAD_PRIVATE_MATTER_SOURCE_FRAME_UNIVERSAL_CHAIN_RULE_SOURCE_AND_TRANSFORMED_HEALTHY_MODES_PPN_NEWTON_DERIVED_ABSOLUTE_P_CUTOFF_STRONG_FIELD_OPEN_NONCLAIM`.

## 1. Select one public matter action

The lead correspondence action now uses

\[
\boxed{
S_{\rm matter}^{\rm pub}=S_{\rm matter}[\Psi,A,\widehat g;\theta_{\rm univ}],
}
\]

with the following declared scope:

```text
all ordinary rods and clocks measure gHat;
all freely falling test bodies couple minimally to gHat;
Maxwell uses the gHat Hodge star;
the charged current comes from the same matter action;
the active local source is the gHat Hilbert tensor;
constants theta_univ are fixed/superselected on the local branch.
```

This closes the optical-shadow ambiguity inside the private correspondence framework. It is an architecture selection, not a claim that the original scalar corpus already derived the public metric.

The same-`g`, `beta_u=0` branch remains the explicit control/fallback if the new absolute-`p` or cutoff tests reject the public branch.

## 2. Exact Hilbert and flow-source chain rule

For constant `p`,

\[
\boxed{
\delta\widehat g^{\mu\nu}
=\delta g^{\mu\nu}
+p\left(u^\mu\delta u^\nu+u^\nu\delta u^\mu\right).
}
\]

Define the public Hilbert tensor by

\[
\delta S_{\rm matter}
=-\frac12\int d^4x\sqrt{-\widehat g}\,
\widehat T_{\mu\nu}\delta\widehat g^{\mu\nu}.
\]

Since

\[
\frac{\sqrt{-\widehat g}}{\sqrt{-g}}=\frac1{\sqrt{1-p}},
\]

the same variation written in the base variables gives

\[
\boxed{
T^{\rm base}_{\mu\nu}
=\frac{1}{\sqrt{1-p}}\widehat T_{\mu\nu},
}
\]

and the induced flow Euler source

\[
\boxed{
J^{(u)}_\nu
=\frac{p}{\sqrt{1-p}}\widehat T_{\mu\nu}u^\mu.
}
\]

Only the component orthogonal to the unit flow is physical after the normalization multiplier is eliminated:

\[
\boxed{
J^{(u)\perp}_\nu
=\frac{p}{\sqrt{1-p}}
h_\nu{}^\lambda\widehat T_{\mu\lambda}u^\mu.
}
\]

In the local rest frame `T_hat_0i=-P_i` with the present signature, so

\[
J^{(u)\perp}_i
=-\frac{p}{\sqrt{1-p}}P_i.
\]

After the common field normalization this is exactly the `beta_u=-p` Poynting source found at 4860. The important new result is universality: the same equation applies to mechanical, fluid, particle and electromagnetic momentum flux. The EM term is not an independently inserted preferred-frame charge.

Public-frame diffeomorphism invariance gives

\[
\widehat\nabla_\mu\widehat T^{\mu\nu}=0
\]

on matter shell. In the base representation, `T_base` and `J_u` obey the corresponding chain-rule Ward identity and exchange momentum internally with the flow. They cannot be varied or tuned independently.

## 3. Transform the gravity coefficients

Use the constant Foster map with

\[
B=\frac1{1-p},
\qquad
\widehat u^\mu=\sqrt{1-p}\,u^\mu.
\]

Transforming the 4857 safe-surface coefficients gives

\[
\boxed{
\widehat c_1=\frac D2,
\qquad
\widehat c_3=-\frac D2,
}
\]

\[
\boxed{
\widehat c_2
=\frac{2p^2}{3(d+p)(1-p)},
\qquad
\widehat c_4
=\frac{2dp}{d+p}-\frac D2,
}
\]

where `D=d+p-dp`. Therefore

\[
\boxed{
\widehat c_{13}=0,
\qquad
\widehat d=D>0,
}
\]

while

\[
\boxed{
\widehat c_{14}=\frac{2dp}{d+p}>0,
\qquad
\widehat c_{123}
=\frac{2p^2}{3(d+p)(1-p)}>0.
}
\]

This is the decisive frame result. A luminal tensor (`c13_hat=0`) does not imply the singular `c14=c123=0` endpoint. The scalar and vector modes retain finite kinetic owners at every finite `p,d`.

The gravitational action normalization transforms by a constant,

\[
\widehat G_{\ae}=\frac{G_{\ae}}{\sqrt{1-p}},
\]

which is absorbed into the measured Newton calibration below.

## 4. Public-frame mode gate

The tensor sector is

\[
\boxed{
\widehat q_T=1,
\qquad
\widehat c_T^2=1.
}
\]

The vector sector is

\[
\boxed{
\widehat q_V=\widehat c_{14}=\frac{2dp}{d+p},
\qquad
\widehat c_V^2=\frac{D(d+p)}{4dp}.
}
\]

The scalar sector is

\[
\boxed{
\widehat q_S=\frac{3D}{p^2},
\qquad
\widehat c_S^2=\frac{p}{3d}.
}
\]

For `0<p<1` and `0<d<=p/3`, all kinetic coefficients are positive. Also

\[
\widehat c_S^2\ge1.
\]

Writing `d=rp`,

\[
\widehat c_V^2
=\frac{(1+r)(1+r-rp)}{4r}\ge1
\]

for `0<r<=1/3`. Photon and tensor characteristics both use `gHat`, so

\[
\boxed{\widehat c_\gamma=\widehat c_T=1.}
\]

The finite public branch therefore passes the linear ghost, gradient and principal Cherenkov gates without relying on the old relative tensor/photon bound.

## 5. Recompute the physical PPN parameters

Matter is minimal in the public frame, so the standard Einstein-aether PPN formulas apply directly to the hatted coefficients. They give

\[
\widehat\gamma=\widehat\beta_{\rm PPN}=1,
\qquad
\widehat\xi=\widehat\zeta_i=\widehat\alpha_3=0,
\]

and

\[
\boxed{
\widehat\alpha_1=-\frac{8dp}{d+p}.
}
\]

The second preferred-frame coefficient is

\[
\boxed{
\widehat\alpha_2=\frac{d(3d-p)}{d+p}.
}
\]

For `d=rp`,

\[
|\widehat\alpha_1|le2p.
\]

The shape controlling `alpha2` is

\[
f(r)=\frac{r(1-3r)}{1+r},
\]

whose maximum on `0<r<=1/3` occurs at

\[
r_*=-1+\frac{2\sqrt3}{3}
\]

and equals

\[
\boxed{f_{\max}=7-4\sqrt3\simeq0.0717968.}
\]

Thus

\[
\boxed{
|\widehat\alpha_2|le(7-4\sqrt3)p.
}
\]

On the retained `p<=1e-15` working corridor,

```text
abs(alpha1_hat) <= 2.0e-15;
abs(alpha2_hat) <= 7.17968e-17.
```

The old 4858/4859 source-specific EM `alpha1/alpha2` values must not be added to these. Those calculations decomposed an optical-only/base-frame source. Once every matter sector is transformed to `gHat`, their direct flow source is part of the universal coefficient transformation and the hatted PPN formulas are the physical readout.

## 6. Newton, source charge, cosmology and clocks

The public Newton constant is

\[
\boxed{
\widehat G_N
=\frac{\widehat G_{\ae}}
{1-\widehat c_{14}/2}.
}
\]

The weak field equation is therefore

\[
\boxed{
\widehat\Delta\widehat U
=-4\pi\widehat G_N\widehat\rho.
}
\]

Because `rho_hat` is the `00` component of the same public Hilbert tensor that appears in the full field equation, the 4852 linear Hilbert/Gauss/ADM source-charge equality carries into this frame without a species or EM weight. `G_N_hat` is calibrated once, exactly as Newton's constant is calibrated in GR rather than predicted from dimensionless geometry alone.

For a homogeneous background,

\[
\widehat G_{\rm cos}
=\frac{\widehat G_{\ae}}
{1+\widehat c_\theta/2},
\qquad
\widehat c_\theta=3\widehat c_2.
\]

The exact ratio is

\[
\boxed{
\frac{\widehat G_{\rm cos}}{\widehat G_N}=1-p.
}
\]

The exact equality from the original frame is replaced by one controlled physical parameter. This becomes an independent absolute-`p` test channel.

All ideal clocks and rods use

\[
d\widehat\tau^2=-\widehat g_{\mu\nu}dx^\mu dx^\nu,
\]

and photons are null with respect to the same metric. A constant `p` therefore creates no separate photon-versus-clock readout drift. Minimal universal matter coupling gives weak-equivalence-principle universality at the action level; strong self-gravity remains separate.

## 7. Branch selection

Three internally defined branches were compared:

1. **Optical-only shared cone:** `g` remains public and only photon/tensor waves use `gHat`. This retains an explicit matter-versus-wave frame and is no longer preferred.
2. **Same-`g` minimal Maxwell:** `beta_u=0`. This is retained as the conservative control and fallback.
3. **Public shared cone:** every ordinary matter/readout sector uses `gHat`, and gravity is transformed consistently. This is selected as the lead private unified branch.

The selected branch wins structurally because it has:

```text
one rods/clocks/photons/free-fall/source metric;
one Hilbert source action;
one universal induced flow source in the base representation;
no independent beta_u coefficient;
luminal tensor and photon modes;
finite positive scalar/vector kinetic owners;
explicit PPN and Newton/cosmology residuals.
```

The cost is equally explicit:

```text
relative GW timing cannot bound absolute p;
PPN is no longer exactly zero, only O(p);
G_cos/G_N=1-p rather than exactly one;
the nonlinear cutoff and compact-body sensitivities are unknown;
the original MTS scalar grammar has not primitively derived the public metric choice.
```

This is a genuine branch selection, not a public theory claim. If the next absolute-`p` and cutoff gates fail, the framework returns to the same-`g`, `beta_u=0` control without damaging checkpoints 4857-4860.

## 8. Result and next target

Closed here:

```text
full matter-frame Hilbert/flow chain-rule variation;
universal rather than EM-only source coupling;
complete gravity coefficient transformation to gHat;
finite c13_hat=0 with c14_hat,c123_hat positive;
public scalar/vector/tensor mode stability and speeds;
universal public-frame PPN vector;
calibrated Newton Poisson/source equation;
exact G_cos/G_N=1-p relation;
same-metric clock/photon and weak free-fall architecture;
lead public-gHat branch selection with same-g fallback.
```

Still open:

```text
strongest source-backed absolute p interval in the public frame;
strong-coupling/nonlinear cutoff as qV,c123 become small;
compact-body sensitivities and radiation interference;
full nonlinear ADM/Komar source map in the public frame;
genuine exact-GR gauge restoration at the endpoint;
primitive MTS derivation of the public metric and coefficient surface.
```

Primary cross-checks: [Foster's coefficient transformation](https://arxiv.org/abs/gr-qc/0502066), [Foster and Jacobson's PPN formulas](https://arxiv.org/abs/gr-qc/0509083), and [Oost, Mukohyama and Wang's mode actions](https://arxiv.org/abs/1802.04303).

Next: `4862-Y5-R2FR-public-frame-absolute-p-bound-and-strong-coupling-cutoff-or-fallback-selection.md`.
