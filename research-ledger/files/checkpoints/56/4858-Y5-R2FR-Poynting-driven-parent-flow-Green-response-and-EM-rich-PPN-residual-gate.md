# 4858 Y5 R2FR Poynting-driven parent-flow Green response and EM-rich PPN gate

Marker: `POYNTING_FLOW_GREEN_EM_PPN_4858`.

**Status:** The schematic `(eta_u/lambda_E)/c14` pressure from 4857 is replaced by the exact coupled stationary transverse solution. The physical flow tilt can indeed be enhanced when the kinetic corridor approaches its singular endpoint, but the same metric-flow constraint that enforces the ordinary PPN-safe branch cancels that inverse kinetic denominator from the metric seen by matter. After Newton calibration, every stationary transverse electromagnetic momentum multipole is multiplied by

\[
R_B=1-\frac{d}{d+p}\frac{\eta_u}{Z_A}.
\]

Across the full finite corridor and the source-backed photon-speed interval, `|R_B-1|<=1.5e-15`. In the standard stationary transverse PPN projection this gives `|alpha1_EM,T|<=1.2e-14` for a pure electromagnetic momentum source. `alpha2` cancels from this projector and is not claimed closed outside it. The internal flow has no uniform corridor-wide bound without a nonzero lower floor on `p`, so nonlinear flow control and the exact-GR endpoint remain open.

**Decision:** `STATIONARY_TRANSVERSE_POYNTING_GREEN_AND_CALIBRATED_METRIC_ALPHA1_TRANSFER_DERIVED_INTERNAL_FLOW_FLOOR_ALPHA2_RETARDED_STRONG_FIELD_OPEN_PRIVATE_NONCLAIM`.

## 1. Correct transverse variable and quadratic action

Work around the local Minkowski/time-flow fixed point in the transverse gauge

\[
g_{0i}=B_i,\qquad \partial_iB_i=0,
\qquad \delta u^i=v_i,\qquad \partial_iv_i=0.
\]

The covariant spatial flow perturbation is

\[
\boxed{W_i:=\delta u_i=B_i+v_i.}
\]

This is the physical tilt relative to the background slicing. Direct second variation of the EH plus unit-flow action gives

\[
16\pi G_{\ae}\mathcal L_V
=c_{14}\dot W_i\dot W_i
-c_1\partial_jW_i\partial_jW_i
+p\,\partial_jB_i\partial_jW_i
+\frac{1-p}{2}\partial_jB_i\partial_jB_i,
\]

where `p=c1+c3` and `d=c1-c3`. In the original contravariant-flow variables the stationary spatial block is equivalently

\[
16\pi G_{\ae}\mathcal L_{V,\rm stat}
=\frac{1-d}{2}(\partial B)^2
-d\,\partial B\partial v-c_1(\partial v)^2.
\]

Eliminating the nondynamical shift in vacuum gives

\[
A_V=c_1+\frac{p^2}{2(1-p)}
=\frac{d+p-dp}{2(1-p)},
\]

which exactly matches the reduced spin-1 gradient coefficient in the primary Einstein-aether perturbation action. This cross-check fixes the variable and removes the earlier ambiguity between `c14` and the actual stationary gradient denominator.

## 2. Keep the two source owners separate

Let

\[
P_i^{\rm EM}=Z_A(\mathbf E\times\mathbf B)_i,
\qquad
\beta_u:=\frac{\eta_u}{Z_A}.
\]

The universal Hilbert momentum couples to `B_i`, while the constitutive flow charge couples to the independent contravariant flow:

\[
\mathcal L_{\rm source}
=B_iP_i^{\rm EM}+\eta_u(\mathbf E\times\mathbf B)_iv_i.
\]

The multiplier-complete 4856 result is important here: the `uF` block has no independent background-frame Hilbert momentum flux, even though it sources the flow Euler equation. Combining the two source entries before variation would erase the constraint cancellation derived below.

After applying the transverse projector, the stationary field equations are

\[
\boxed{
\begin{pmatrix}
-(1-d)&d\\
d&2c_1
\end{pmatrix}
\begin{pmatrix}\Delta B_i\\ \Delta v_i\end{pmatrix}
=-16\pi G_{\ae}
\begin{pmatrix}P_i^T\\ \beta_uP_i^T\end{pmatrix}.
}
\]

Its determinant is

\[
-D,\qquad D:=d+p-dp>0
\]

throughout the finite 4857 corridor.

## 3. Exact Green response

Solving the matrix and using `W=B+v` gives

\[
\boxed{
\Delta W_i
=16\pi G_{\ae}\frac{p-\beta_u}{D}P_i^T,
}
\]

\[
\boxed{
\Delta B_i
=16\pi G_{\ae}
\left[1+\frac{d(p-\beta_u)}{D}\right]P_i^T.
}
\]

For isolated stationary boundary conditions,

\[
W_i(\mathbf x)
=-4G_{\ae}\frac{p-\beta_u}{D}
\int\frac{P_i^T(\mathbf x')}{|\mathbf x-\mathbf x'|}\,d^3x',
\]

\[
B_i(\mathbf x)
=-4G_{\ae}\left[1+\frac{d(p-\beta_u)}{D}\right]
\int\frac{P_i^T(\mathbf x')}{|\mathbf x-\mathbf x'|}\,d^3x'.
\]

Overall signs change with the `g0i` and Green-function convention; the transfer ratios below do not.

## 4. Newton calibration produces the decisive cancellation

On the exact PPN-safe surface,

\[
\frac{G_{\ae}}{G_N}=1-\frac{c_{14}}2
=\frac{D}{d+p}.
\]

Relative to the GR metric Green function built with measured `G_N`, the exact metric and flow ratios are therefore

\[
\boxed{
R_B:=\frac{B}{B_{\rm GR}}
=1-\frac{d}{d+p}\beta_u,
}
\]

\[
\boxed{
R_W:=\frac{W}{B_{\rm GR}}
=\frac{p-\beta_u}{d+p}.
}
\]

This is the main result. `R_W` can be large as `p,d` approach zero at fixed nonzero `beta_u`, but the observable metric residual is

\[
\boxed{
\delta_B:=R_B-1=-\frac{d}{d+p}\beta_u,
}
\]

with no inverse `D`, `c14`, or `p` enhancement. At `beta_u=0`, the nonzero ordinary-source flow response is exactly what makes `R_B=1` on the PPN-safe branch. At `beta_u=p`, the direct transverse flow vanishes, but this is not the calibrated metric-GR condition.

## 5. Source-backed bound

Checkpoint 4854 gives the conservative interval

\[
-6.0\times10^{-15}\lesssim\beta_u\lesssim1.4\times10^{-15}.
\]

The healthy corridor has `0<d<=p/3`, hence

\[
0<\frac d{d+p}\le\frac14.
\]

Therefore, uniformly over every finite point in the corridor,

\[
\boxed{|\delta_B|\le1.5\times10^{-15}.}
\]

No lower bound on `p` was used. By contrast, `R_W` has no uniform bound when `p->0` at fixed `beta_u`; metric safety does not prove internal-flow perturbativity.

For a compact source of radius `R`, positivity of the constitutive photon block gives

\[
|P^{\rm EM}|\le r_\gamma\rho_{\rm EM},
\qquad r_\gamma=\sqrt{Z_A/(Z_A+\eta_u)}.
\]

Outside the source,

\[
\frac{|\delta B|}{U}
\le4\frac{d|\beta_u|}{d+p}
r_\gamma\epsilon_{\rm EM}\frac r{r-R},
\qquad
\epsilon_{\rm EM}=\frac{E_{\rm EM}}{M}.
\]

Thus the far-zone coefficient is at most approximately `6e-15 epsilon_EM`, without assigning an unknown order-one Green coefficient.

## 6. Exact stationary transverse PPN projection

Foster and Jacobson write the standard PPN difference as

\[
(g_{0i})_{\ae}-(g_{0i})_{\rm GR}
=\frac{\alpha_1-\alpha_2}{2}V_i
+\frac{\alpha_2}{2}W_i^{\rm PPN}.
\]

For a stationary conserved transverse momentum source,

\[
V_i=W_i^{\rm PPN},
\]

so `alpha2` cancels and the residual is `alpha1 V_i/2`. Since the GR coefficient is `4V_i` in that convention,

\[
\boxed{
\alpha_{1,\rm EM}^{T}=8\delta_B
=-8\frac{d}{d+p}\beta_u.
}
\]

For a pure stationary transverse electromagnetic source,

\[
\boxed{|\alpha_{1,\rm EM}^{T}|\le1.2\times10^{-14},}
\]

well below the conservative `R5` comparator `10^-4`. For a composite body this is a source-specific coefficient multiplied by its transverse electromagnetic momentum-potential fraction; it is not a new universal PPN constant.

The statement

\[
\alpha_{2,\rm EM}^{T}=0
\]

is only a projector zero. It does not close longitudinal energy exchange, moving-frame scalar response, retarded fields, compact-body sensitivities, or the strong-field `alpha2` analogue.

## 7. Multipoles and source classes

The common Green integral has the far-zone expansion

\[
\mathcal I_i(\mathbf x)
=\frac{\Pi_i}{r}+\frac{n_a\mathcal D_{ia}}{r^2}+O(r^{-3}),
\]

\[
\Pi_i=\int P_i^T d^3x,
\qquad
\mathcal D_{ia}=\int x'_aP_i^T d^3x'.
\]

A closed-system rest frame sets total momentum to zero, not necessarily electromagnetic momentum separately; hidden mechanical momentum blocks a general `Pi_i^EM=0` theorem. Reflection symmetry or stationary axisymmetric azimuthal circulation does set the vector monopole to zero, leaving the angular-momentum dipole. Every stationary transverse multipole receives the same `R_B`, so source geometry cannot recreate the canceled inverse-kinetic enhancement.

Aligned electrostatics and pure comoving magnetostatics have `E cross B=0` pointwise and retain the exact 4855/4856 result. Radiative or locally powered systems are outside this Poisson theorem.

## 8. Result

Closed here:

```text
correct physical transverse flow variable W_i;
exact coupled metric-flow Poisson matrix;
isolated stationary Green functions;
Newton-calibrated metric transfer R_B=1-d beta_u/(d+p);
uniform |delta_B|<=1.5e-15;
exact stationary-transverse alpha1 map and |alpha1_EM,T|<=1.2e-14;
multipole transfer without geometry-dependent amplification.
```

Still open:

```text
uniform internal-flow bound without a lower p floor;
longitudinal EM power transfer and alpha2;
retarded Green functions and extra-mode radiation;
strong-field sensitivities and compact-body flow charge;
nonlinear saturation/cutoff;
regular exact-GR gauge restoration or flow elimination;
primitive MTS selection of p and d and primitive EH/U1 origin.
```

Primary sources: [Oost, Mukohyama and Wang](https://arxiv.org/abs/1802.04303), [Jacobson and Mattingly](https://arxiv.org/abs/gr-qc/0402005), and [Foster and Jacobson](https://arxiv.org/abs/gr-qc/0509083).

Next: `4859-Y5-R2FR-longitudinal-EM-power-transfer-retarded-flow-and-alpha2-radiation-gate.md`.

Resolution at 4859: the exact retarded spin-1 and direct spin-0 kernels are derived; the separately conserved weak-source result is `alpha2_EM=beta_u(3p-d)/(p+d)`, while powered exchange carries a separate `Xi_i` potential. Endpoint regularity of the linear EM response requires `beta_u=O(p)` rather than an arbitrary lower `p` floor.

Frame note at 4861: these source-specific transfer coefficients remain valid for the optical-only/base-`g` decomposition. On the selected public-`gHat` branch every matter sector carries the chain-rule flow source, so the transformed universal PPN coefficients must be used instead of adding an EM residual separately.
