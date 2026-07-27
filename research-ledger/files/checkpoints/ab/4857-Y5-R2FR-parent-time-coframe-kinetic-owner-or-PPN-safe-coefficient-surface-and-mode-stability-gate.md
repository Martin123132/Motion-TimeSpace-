# 4857 Y5 R2FR parent time-flow kinetic owner and stability corridor

Marker: `PARENT_TIME_FLOW_KINETIC_STABILITY_4857`.

**Status:** The missing quadratic owner of the already present MTS time flow is filled at the private correspondence-theory level. Diffeomorphism covariance, a unit timelike vector, parity evenness, and at most two derivatives leave the four-operator Einstein-aether/unit-flow basis. This is an EFT completion of existing field content, not a new field and not a primitive derivation of its coefficients from the original scalar grammar. Imposing the exact weak-field `alpha1=alpha2=0` surface and rewriting it in GW-adapted variables produces a finite analytic corridor in which all scalar, vector, and tensor kinetic coefficients are positive, all mode speeds are at least luminal, the tensor speed satisfies the conservative GW170817 bound, and the Newtonian and cosmological gravitational constants coincide exactly. The exact `c13=0` endpoint is singular because the vector and scalar kinetic combinations vanish; exact GR still requires a genuine gauge-restoration or field-elimination theorem.

**Decision:** `MINIMAL_UNIT_FLOW_EFT_OWNER_AND_PPN_GW_STABILITY_CORRIDOR_DERIVED_EXACT_GR_ENDPOINT_SINGULAR_PRIVATE_NONCLAIM`.

## 1. Why this is an owner rather than another closure

The corpus already uses a normalized physical flow `u` in the memory and electromagnetic constitutive actions. Checkpoints 79-80 correctly rejected a stress-free clock/reference action as a physical owner: a metric-normalized time direction either gravitates or is only gauge bookkeeping. The remaining honest choices are:

1. eliminate `u` as a physical field by an actual gauge theorem; or
2. give the existing physical `u` its complete local kinetic action and test it.

This checkpoint takes the second route as the finite correspondence branch. With universal matter coupling to the same public metric,

\[
S_{\rm par}=\frac1{2\kappa_*}\int d^4x\sqrt{-g}
\left[R-2\Lambda
-K^{\alpha\beta}{}_{\mu\nu}
\nabla_\alpha u^\mu\nabla_\beta u^\nu
+\lambda_u(u^2+1)-2G(\theta)\right]
+S_A[g,u,A]+S_m[g,\Psi],
\]

where

\[
\boxed{
K^{\alpha\beta}{}_{\mu\nu}
=c_1g^{\alpha\beta}g_{\mu\nu}
+c_2\delta^\alpha_\mu\delta^\beta_\nu
+c_3\delta^\alpha_\nu\delta^\beta_\mu
-c_4u^\alpha u^\beta g_{\mu\nu}.
}
\]

Up to integration-by-parts and curvature identities, this is the complete parity-even quadratic two-derivative basis for a unit timelike vector. No direct matter-`u` charge is introduced.

The kinematic combinations are

\[
c_\sigma=c_{13}=c_1+c_3,
\qquad
c_\omega=c_1-c_3,
\qquad
c_a=c_{14}=c_1+c_4,
\qquad
c_\theta=c_{13}+3c_2.
\]

The existing memory function `G(theta)` remains the nonlinear coherent-load block. The new quadratic basis supplies the parent operator that 4847 and 4850 showed was missing at the local fixed point.

## 2. Exact PPN-safe surface

For the general unit-flow action, the only weak-field PPN coefficients that differ from GR are

\[
\alpha_1=-\frac{8(c_3^2+c_1c_4)}
{2c_1-c_1^2+c_3^2},
\]

\[
\alpha_2=\frac{\alpha_1}{2}
-\frac{(c_1+2c_3-c_4)(2c_1+3c_2+c_3+c_4)}
{(c_1+c_2+c_3)(2-c_1-c_4)}.
\]

Away from singular denominators,

\[
\boxed{
c_4=-\frac{c_3^2}{c_1},
\qquad
c_2=\frac{-2c_1^2-c_1c_3+c_3^2}{3c_1}
}
\]

sets both to zero exactly. The remaining weak-field PPN parameters equal their GR values when matter couples universally to `g_mu_nu`.

Introduce variables adapted to the tensor-speed and vorticity sectors,

\[
p=c_{13}=c_1+c_3,
\qquad
d=c_1-c_3.
\]

Then

\[
c_1=\frac{p+d}{2},
\qquad
c_3=\frac{p-d}{2},
\]

and the full safe surface becomes

\[
\boxed{
c_2=-\frac{p(3d+p)}{3(d+p)},
\qquad
c_4=-\frac{(p-d)^2}{2(p+d)}.
}
\]

Useful exact combinations are

\[
\boxed{
c_{14}=\frac{2dp}{d+p},
\qquad
c_{123}=\frac{2p^2}{3(d+p)},
\qquad
c_\theta=-\frac{2dp}{d+p}=-c_{14}.
}
\]

## 3. Mode kinetic coefficients and speeds

The quadratic scalar, vector, and tensor time-kinetic coefficients are

\[
q_S=\frac{(1-c_{13})(2+c_{13}+3c_2)}{c_{123}},
\qquad
q_V=c_{14},
\qquad
q_T=1-c_{13}.
\]

On the PPN-safe surface,

\[
q_S=\frac{3(1-p)(d+p-dp)}{p^2},
\qquad
q_V=\frac{2dp}{d+p},
\qquad
q_T=1-p.
\]

The squared mode speeds reduce to

\[
\boxed{
c_S^2=\frac{p}{3d(1-p)},
\qquad
c_V^2=\frac{(d+p)(d+p-dp)}{4dp(1-p)},
\qquad
c_T^2=\frac1{1-p}.
}
\]

Therefore the finite corridor

\[
\boxed{
0<p\le10^{-15},
\qquad
0<d\le\frac p3
}
\]

is sufficient for positive time-kinetic coefficients, positive gradients, and mode speeds at least equal to the matter light speed. To see the speed result, put `d=r p` with `0<r<=1/3`:

\[
c_S^2=\frac1{3r(1-p)}\ge1,
\]

\[
c_V^2
=\frac{1+r}{4r}
\left[(1+r)+\frac{p}{1-p}\right]
\ge\frac{(1+r)^2}{4r}\ge1,
\]

\[
c_T^2=\frac1{1-p}\ge1.
\]

Thus the same corridor avoids vacuum gravitational Cherenkov emission at the principal-mode level. The positive sign choice `p>0` also makes the tensor slightly superluminal rather than subluminal; the upper limit is inside the conservative multimessenger `|c13|<10^-15` envelope.

## 4. Exact Newton/cosmology calibration lock

For this action,

\[
G_N=\frac{G_{\ae}}{1-c_{14}/2},
\qquad
G_{\rm cos}=\frac{G_{\ae}}{1+(c_{13}+3c_2)/2}.
\]

Because the PPN-safe surface gives `c_theta=c13+3c2=-c14`,

\[
\boxed{G_{\rm cos}=G_N}
\]

exactly. The parent time-flow regularizer therefore does not introduce an independent Newton-versus-FLRW gravitational calibration. The observed `G_N` still calibrates the common denominator; this does not derive its numerical value from first principles.

Within the sufficient corridor, `c14<=p/2`, so

\[
0<\frac{G_N}{G_{\ae}}-1
=\frac{c_{14}}{2-c_{14}}
\le\frac{p}{4-p}
\lesssim2.5\times10^{-16}.
\]

## 5. Finite benchmark

The nonpredictive upper-edge point

\[
p=10^{-15},
\qquad d=p/3
\]

gives approximately

\[
(c_1,c_2,c_3,c_4)
=(6.67,-5.00,3.33,-1.67)\times10^{-16},
\]

\[
c_{14}=c_{123}=5.0\times10^{-16},
\]

\[
c_S^2\simeq c_T^2\simeq1+10^{-15},
\qquad
c_V^2\simeq\frac43.
\]

The canonical vector kinetic scale proxy `Mbar_Pl sqrt(qV)` is about `5.4e10 GeV`. This shows the finite point is not automatically a low-energy strong-coupling disaster, but it is not a nonlinear cutoff calculation and there is no derived lower floor on `p` or `d`.

## 6. Exact-GR endpoint obstruction

The exact tensor-luminal limit is not regular on the PPN-safe physical-flow surface. Setting

\[
p=c_{13}=0
\]

forces

\[
c_{14}=0,
\qquad
c_{123}=0.
\]

Hence the vector time-kinetic coefficient vanishes and the scalar normalization/speed expressions become nonuniform. If `p->0` and `d=r p`, all four `c_i` vanish linearly and the extra modes lose canonical normalization even though their formal speed ratios can remain finite.

Therefore

\[
\boxed{
\text{finite PPN/GW-compatible physical-flow branch exists,}
\quad
\text{but exact GR is not a regular coefficient limit.}
}
\]

An exact GR reduction requires a parent theorem that restores local Lorentz gauge freedom or removes `u` as a physical mode when the memory/constitutive operators switch off. Merely setting coefficients to zero is insufficient.

## 7. Electromagnetic consequence

Checkpoint 4856 derived

\[
D_\mu G_\theta=-\kappa\eta_u\mathcal S_\mu.
\]

The present action supplies the missing Green operator, but it also sharpens the bound: transverse response can scale schematically as

\[
\delta u_\perp\sim
\frac{\eta_u/\lambda_E}{c_{14}}
\,\mathcal G_\perp*\mathcal S.
\]

At the upper-edge benchmark, the conservative `|eta_u/lambda_E|<=6e-15` and `c14=5e-16` give a coefficient ratio as large as `12`. Thus the propagation bound does not by itself guarantee a tiny induced flow. Observable PPN response still multiplies the source electromagnetic energy fraction and geometry, so this is pressure, not a failure verdict.

This is now calculable rather than symbolic. The next task is to derive the stationary Poynting-driven Green response and map real source profiles into `alpha1/alpha2` residuals.

## 8. Result

Closed here:

```text
complete minimal quadratic owner for the existing physical time flow;
exact alpha1=alpha2=0 coefficient surface;
finite positive-kinetic, gradient-stable, no-Cherenkov GW corridor;
exact G_cos=G_N calibration lock;
nondegenerate local quadratic flow operator in the finite branch.
```

Still open:

```text
primitive MTS selection of p and d;
regular exact-GR gauge-restoration/elimination theorem;
nonlinear strong-coupling cutoff;
Poynting-driven source Green response;
strong-field sensitivities and extra-mode radiation;
primitive EH/coframe origin.
```

Primary sources: [Foster and Jacobson](https://arxiv.org/abs/gr-qc/0509083), [Jacobson and Mattingly](https://arxiv.org/abs/gr-qc/0402005), and [Oost, Mukohyama, and Wang](https://arxiv.org/abs/1802.04303).

Next: `4858-Y5-R2FR-Poynting-driven-parent-flow-Green-response-and-EM-rich-PPN-residual-gate.md`.

**4858 resolution note:** the schematic `(eta_u/lambda_E)/c14` pressure in section 7 is superseded by the exact coupled solve in checkpoint 4858. The physical flow can still be enhanced, but the Newton-calibrated metric transfer is `R_B=1-d(eta_u/Z_A)/(d+p)` and has no inverse kinetic denominator.

**4860 propagation note:** `p<=1e-15` remains the conservative working corridor. Its direct GW170817 interpretation is branch-dependent once the photon speed is allowed to depend on `beta_u`: the measured combination is `epsilon_cone=beta_u+p`. On the shared-cone branch `beta_u=-p`, relative GW timing is identically silent on absolute `p`, so an independent `p` provenance is required.
