# 4860 Y5 R2FR parent coupling co-scaling law or first EM radiation profile test

Marker: `SHARED_CONE_COUPLING_LAW_4860`.

**Status:** The parent-coupling hunt has produced a constructive nonzero mechanism rather than another missing-coefficient entry. The spin-2 principal symbol already defines an effective inverse characteristic metric

\[
\widehat g^{\mu\nu}=g^{\mu\nu}+p\,u^\mu u^\nu.
\]

Writing the Maxwell kinetic action minimally with this same characteristic metric and expanding it back into the 4854 basis gives exactly

\[
\boxed{\eta_u=-pZ_A,\qquad \beta_u=-p,\qquad \zeta=-1.}
\]

No new coefficient is fitted. Photon and tensor cones coincide exactly, the 4859 endpoint regularity condition is automatic, and the stationary/retarded observables stay finite. A lower-risk same-base-metric Maxwell branch gives the other parameter-free solution `beta_u=0`. The old independent fixed-`beta_u` branch is demoted.

The calculation also corrects the earlier multimessenger interpretation: once `c_T` depends on `p`, GW170817/GRB170817A constrains `epsilon_cone=beta_u+p`, not `beta_u` alone. The shared-cone branch has `epsilon_cone=0` identically. This means relative GW timing no longer provides an absolute upper bound on `p` in that branch, so the current `p<=1e-15` corridor remains a conservative working corridor pending the matter-frame test.

**Decision:** `SHARED_CHARACTERISTIC_METRIC_CONSTRUCTS_BETA_U_MINUS_P_EXACTLY_SAME_G_BETA_ZERO_RETAINED_CORRECTED_MULTIMESSENGER_COMBINATION_DERIVED_MATTER_FRAME_AND_ABSOLUTE_P_OPEN_PRIVATE_NONCLAIM`.

## 1. Correct the measured cone combination

On the 4857 safe surface,

\[
c_T^2=\frac1{1-p}.
\]

The 4854 constitutive block gives

\[
c_\gamma^2=\frac1{1+\beta_u},
\qquad \beta_u=\frac{\eta_u}{Z_A}.
\]

Therefore the relative messenger speed is

\[
\boxed{
\delta_c:=\frac{c_T}{c_\gamma}-1
=\sqrt{\frac{1+\beta_u}{1-p}}-1.
}
\]

Solving exactly,

\[
\boxed{
\beta_u=(1-p)(1+\delta_c)^2-1.
}
\]

The combination directly constrained by relative propagation is thus

\[
\boxed{
\epsilon_{\rm cone}:=\beta_u+p
=(1-p)(2\delta_c+\delta_c^2).
}
\]

Using the reported interval

\[
-3\times10^{-15}\le\delta_c\le7\times10^{-16},
\]

and `p=1e-15` gives

```text
-5.999999999999985e-15 <= epsilon_cone
                              <= 1.39999999999999909e-15.
```

The 4854 interval for `beta_u` is the `p=0` specialization of this relation. It must not be reused as an independent coefficient interval after the tensor sector is active.

## 2. Tensor characteristic metric

The tensor equation has principal part

\[
(1-p)\partial_t^2h_{ij}^{TT}-\Delta h_{ij}^{TT}=0.
\]

In the local flow rest frame this is equivalent to

\[
\widehat g^{\mu\nu}k_\mu k_\nu=0,
\qquad
\boxed{\widehat g^{\mu\nu}=g^{\mu\nu}+p u^\mu u^\nu.}
\]

For `0<p<1`, the inverse and determinant follow from the Sherman-Morrison and matrix-determinant lemmas:

\[
\boxed{
\widehat g_{\mu\nu}
=g_{\mu\nu}-\frac{p}{1-p}u_\mu u_\nu,
}
\]

\[
\boxed{
\sqrt{-\widehat g}=\frac{\sqrt{-g}}{\sqrt{1-p}}.
}
\]

This uses the existing flow and the already derived coefficient `p`; it introduces no new field.

## 3. Minimal Maxwell action on the shared cone

Consider the explicit kinetic block

\[
\boxed{
S_A^{\rm shared}
=-\frac{Z_*}{4}\int d^4x\sqrt{-\widehat g}\,
\widehat g^{\mu\rho}\widehat g^{\nu\sigma}
F_{\mu\nu}F_{\rho\sigma}.
}
\]

Antisymmetry of `F` removes the term quadratic in four factors of `u`. Exact expansion gives

\[
S_A^{\rm shared}
=-\frac{Z_*}{4\sqrt{1-p}}
\int d^4x\sqrt{-g}
\left[
F_{\mu\nu}F^{\mu\nu}
+2p\,u^\mu u^\nu F_{\mu\alpha}F_\nu{}^\alpha
\right].
\]

Matching to

\[
\mathcal L_A=-\frac{Z_A}{4}F^2
+\frac{\eta_u}{2}u^\mu u^\nu F_{\mu\alpha}F_\nu{}^\alpha
\]

gives

\[
\boxed{
Z_A=\frac{Z_*}{\sqrt{1-p}},
\qquad
\eta_u=-\frac{pZ_*}{\sqrt{1-p}}=-pZ_A.
}
\]

Hence

\[
\boxed{\beta_u=-p,\qquad\zeta=\frac{\beta_u}{p}=-1.}
\]

The rest-frame electric and magnetic coefficients are

\[
\lambda_E=Z_A(1-p),
\qquad
\lambda_B=Z_A.
\]

Both are positive for `Z_A>0` and `0<p<1`, and

\[
\boxed{
c_\gamma^2=\frac{\lambda_B}{\lambda_E}
=\frac1{1-p}=c_T^2.
}
\]

This is the sought nonzero co-scaling mechanism. It is an explicit action construction, not the assertion `beta_u proportional to p` written after seeing the endpoint divergence.

## 4. Consequences for the local response

Substituting `beta_u=-p` into 4858-4859 gives

\[
\boxed{
R_B=1+\frac{dp}{d+p},
\qquad
R_W=\frac{2p}{d+p}.
}
\]

For `d=rp`,

\[
R_W=\frac2{1+r},
\]

which is finite throughout `0<r<=1/3`. The source-specific weak coefficients become

\[
\boxed{
\alpha_{1,\rm EM}=8\frac{dp}{d+p},
\qquad
\alpha_{2,\rm EM}=-p\frac{3p-d}{d+p}.
}
\]

Therefore

\[
|R_B-1|\le\frac p4,
\qquad
|\alpha_{1,\rm EM}|\le2p,
\qquad
|\alpha_{2,\rm EM}|\le3p.
\]

At the retained working benchmark `p=1e-15`, `d=p/3`,

```text
epsilon_cone = 0;
R_B-1 = 2.5e-16;
R_W = 1.5;
alpha1_EM = 2.0e-15;
alpha2_EM = -2.0e-15.
```

The radiation coefficients multiplying `Gae |dot Q_EM|^2` are

```text
C_V = 6.928203230275515e-15;
C_S,direct = 1.333333333333334e-15.
```

Both vanish linearly with `p`. The shared-cone construction therefore satisfies every linear EM regularity condition found at 4859 without a lower kinetic floor.

## 5. The two parameter-free regular branches

The parent action now has two clean possibilities rather than one unexplained continuous `beta_u`:

### A. Same-base-metric/Hodge branch

\[
S_A=-\frac{Z_A}{4}\int\sqrt{-g}\,F^2,
\qquad
\boxed{\beta_u=0.}
\]

This is the lowest-risk correspondence baseline. It has no direct flow constitutive operator, obeys the 4859 regularity gate with `zeta=0`, and preserves the interpretation of relative GW timing as a bound on `p`. It is the branch selected if the 3779 no-shadow-metric criterion is adopted literally.

### B. Shared-characteristic-metric branch

\[
S_A=S_A^{\rm shared}[\widehat g],
\qquad
\boxed{\beta_u=-p.}
\]

This is the lead nonzero unification candidate. It uses no extra coefficient and makes the photon and tensor characteristics identical. It must still answer whether `gHat` is only the common radiation/optical metric or the public metric for all matter.

At the upper working benchmark, the response-cancellation choice `beta_u=p` gives `delta_c approximately 1e-15`, outside the `7e-16` upper interval. It also lacks a parent action owner. It is therefore not selected merely because it sets the transverse flow source to zero.

A fixed nonzero `beta_u` independent of `p` remains endpoint-singular and is demoted from the preferred theory spine.

## 6. Field-redefinition cross-check and no-shortcut result

Foster's constant transformation

\[
g'_{\mu\nu}=g_{\mu\nu}-(1-B)u_\mu u_\nu,
\qquad
u'^\mu=\frac{u^\mu}{\sqrt B}
\]

generates from pure GR the special aether coefficients

\[
c_1=-\frac{(1-B)^2}{2B},
\quad c_2=\frac{1-B}{B},
\quad c_3=-\frac{1-B^2}{2B},
\quad c_4=\frac{(1-B)^2}{2B}.
\]

Choosing `B=1/(1-p)` gives

\[
c_{13}=p,
\qquad
d=-\frac{p}{1-p},
\qquad
c_{14}=c_{123}=0.
\]

Minimal Maxwell propagation on `g'` again appears as `beta_u=-p` in the `g` variables. This independently cross-checks the shared-cone algebra and demonstrates that an exact gauge/redefinition route to GR exists in coefficient space.

It is not the current finite 4857 branch: that branch has `d>0`, `c14>0`, and `c123>0`, whereas the GR-equivalent family has `d<0` and degenerate scalar/vector kinetic combinations. Vacuum GR equivalence also requires matter to be transformed consistently. The Foster family is therefore an existence clue for eventual gauge restoration, not a shortcut that promotes the current finite branch to exact GR.

## 7. What moved and what remains

Closed here:

```text
exact relative photon/tensor cone formula;
correction from standalone beta_u bound to epsilon_cone=beta_u+p;
explicit shared characteristic metric;
exact Maxwell expansion and beta_u=-p coupling law;
automatic zeta=-1 endpoint regularity;
finite stationary, PPN and direct radiation response on the working corridor;
same-g beta_u=0 branch retained as the lowest-risk alternative;
fixed independent beta_u and response-tuned beta_u=p demoted;
pure-GR disformal family checked and prevented from becoming a false shortcut.
```

Still open:

```text
whether the parent MTS ontology selects same-g or shared-characteristic Maxwell;
whether gHat is optical-only or the public metric for rods, clocks and all matter;
full Hilbert/source variation if matter uses gHat;
an absolute source for p on the exact shared-cone branch;
strong-field sensitivities and complete scalar radiation;
genuine gauge restoration for the finite d>0 route;
primitive MTS derivation of the adopted EH/U1/unit-flow action blocks.
```

Primary cross-checks: [Foster's metric-redefinition calculation](https://arxiv.org/abs/gr-qc/0502066), [Oost, Mukohyama and Wang's mode speeds](https://arxiv.org/abs/1802.04303), and the [GW170817/GRB170817A relative-speed result](https://arxiv.org/abs/1710.05834).

Next: `4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md`.

Resolution at 4861: `gHat` is selected as the lead private public metric for all ordinary matter and source readout. The chain rule makes the base-frame `beta_u=-p` flow source universal. The transformed physical coefficients have `c13_hat=0` with finite positive `c14_hat,c123_hat`; public PPN and `G_cos/G_N=1-p` replace the optical-only source projections.
