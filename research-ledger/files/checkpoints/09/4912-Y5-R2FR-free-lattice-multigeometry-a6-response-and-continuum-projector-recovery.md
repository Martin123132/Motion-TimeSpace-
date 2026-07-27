# 4912 - Independent continuum TTT recovery and matched lattice subtraction

Marker: `MTS_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_PROJECTOR_4912`

## Decision

Checkpoint 4911 proved the geometric rank-eight projector using the sourced
heat-kernel vector `y=M c_a6`. This checkpoint supplies the independent test:
it differentiates the actual free scalar determinant to sixth order in the
external momentum for all twelve traceful source geometries.

The first arbitrary-source implementation failed for a precise reason. The
4910 response formula was derived for traceless TT polarizations; the 4911
rank-generating ensemble is deliberately traceful. Reusing the TT formula
omitted the first mass-volume vertex and every trace term in the pair and
triple seagulls. Those determinant derivatives are now derived and included.

With the complete triangle-plus-seagull response, direct continuum momentum
integration recovers

\[
\boxed{
m^2\zeta_s=2.094105151327707\times10^{-7}
}
\]

at both `m=1` and `m=2`, compared with

\[
\frac1{30240(4\pi)^2}
=2.0941051513379998\times10^{-7}.
\]

The ratio is `0.9999999999950849`, the twelve-geometry response residual is
`9.376e-16`, and every leave-one-geometry ratio lies in
`[0.9999999999931295,0.9999999999983918]`. This is an independent determinant
recovery, not `M` multiplied by a supplied coefficient vector.

The absolute coarse-lattice route fails decisively. Across nearest and
improved stencils at `(N,am)=(8,1)` and `(16,0.5)`, the rank-eight residual is
`15.4--41.5%`, the apparent coefficient is `-1127` to `-3911` times the
continuum value, and leave-one projections can change sign. Two-point
extrapolations of those rows are explicitly invalid. No coarse absolute
coefficient is retained.

The selected nonperturbative route is therefore a same-regulator matched
subtraction:

\[
\boxed{
y_{ren}=y_{free}^{cont}(m_{gap})
+\lim_{a\to0}\left[y_{int}^{a}-y_{free}^{a}(m_{gap},Z_T)\right].
}
\]

The free continuum restoration term is now fixed independently. A paired
interacting smoke run is permitted next, but the interacting long run and any
coefficient promotion remain withheld. Thus

\[
\boxed{\Gamma_{\rm MTS,res}=0.}
\]

## 1. Complete traceful determinant contacts

For

\[
H=I+\epsilon_1e_1+\epsilon_2e_2+\epsilon_3e_3,
\qquad V(H)=\sqrt{\det H},
\]

write `t_i=tr(e_i)` and `t_ij=tr(e_i e_j)`. The required derivatives are

\[
\boxed{V_i=\frac12t_i,}
\]

\[
\boxed{V_{ij}=\frac14t_it_j-\frac12t_{ij},}
\]

and

\[
\boxed{
\begin{aligned}
V_{123}={}&\frac12[\operatorname{tr}(e_1e_2e_3)
+\operatorname{tr}(e_1e_3e_2)]\\
&-\frac14[t_{12}t_3+t_{13}t_2+t_{23}t_1]
+\frac18t_1t_2t_3.
\end{aligned}}
\]

The scalar kernel derivatives are

\[
K_i=K_i^{kin}+m^2V_i,
\qquad K_{ij}=m^2V_{ij},
\qquad K_{123}=m^2V_{123}.
\]

All three formulas agree with the independent nilpotent determinant engine at
machine precision: the first and pair residuals are zero, and the triple
residual is `5.55e-17`. In the TT limit, `t_i=0`, they reduce exactly to the
4910 contacts, so the previous dense validation is preserved.

## 2. Exact sixth-order determinant derivative

For lattice momentum `p` and a common external scaling parameter `t`, every
shift is `p+t r`. A seventh-component Taylor algebra stores coefficients from
`t^0` through `t^6`. Propagator inversion is recursive:

\[
G_0=D_0^{-1},
\qquad
G_n=-D_0^{-1}\sum_{k=1}^{n}D_kG_{n-k}.
\]

The complete determinant response is evaluated as

\[
\frac12\operatorname{Tr}\left[
GK_{123}-GK_1GK_{23}-GK_2GK_{13}-GK_3GK_{12}
+GK_1GK_2GK_3+GK_1GK_3GK_2
\right].
\]

The `t^6` component is obtained directly. It is not inferred by subtracting
fitted `q^0`, `q^2`, and `q^4` numbers. Three independent checks pass:

- the arbitrary code reproduces the 4910 direct response to `1.73e-18`;
- its Taylor polynomial reproduces a direct small-momentum response to
  `1.73e-18`;
- the series inverse closes to `2.61e-16`.

For real cosine sources, only the all-plus and all-minus momentum closures
survive. Therefore

\[
y_{r,6}^{cos}=\frac14\operatorname{Re}\left[
e^{i(\phi_1+\phi_2+\phi_3)}W_{r,6}^{+++}
\right].
\]

## 3. Independent continuum loop

The continuum limit is evaluated directly from the same determinant identity,
using

\[
G(p+tr)=\frac1{(p+tr)^2+m^2},
\qquad
K_i^{kin}=(p+tr+te_i)_\mu e_i^{\mu\nu}(p+tr)_\nu,
\]

with the complete mass contacts above. The four-dimensional loop measure is
integrated in radial and `S^3` coordinates. The radial map

\[
p=m\tan\left(\frac{\pi x}{2}\right),\qquad 0<x<1,
\]

uses 64 Gauss--Legendre nodes; the angular polynomial uses order eight and 16
azimuthal nodes. No heat-kernel coefficient is supplied to this calculation.

For both masses:

| mass | response residual | `m^2 zeta / target` | leave-one range |
|---:|---:|---:|---:|
| `1` | `9.376e-16` | `0.9999999999950849` | `0.9999999999931--0.9999999999984` |
| `2` | `9.376e-16` | `0.9999999999950849` | `0.9999999999931--0.9999999999984` |

The exact `1/m^2` scaling is therefore recovered independently. Individual
off-shell coefficients need not equal one chosen heat-kernel representative;
the quotient-invariant Ricci-flat functional agrees exactly, which is the
physical test selected at 4911.

## 4. Why the absolute coarse lattice fails

The two lattice stencils are:

\[
d_+(p)=e^{ip}-1
\]

and the second-order one-sided derivative

\[
d_+^{imp}(p)=\frac{-3+4e^{ip}-e^{2ip}}2,
\]

each averaged with its reflected backward partner. The tested rows keep
`N am=8` while changing `am` from one to one half.

| stencil and row | quotient residual | apparent `m^2 zeta / target` |
|---|---:|---:|
| nearest, `N=8`, `am=1` | `0.2421` | `-1371.96` |
| improved, `N=8`, `am=1` | `0.4150` | `-3910.84` |
| nearest, `N=16`, `am=0.5` | `0.2218` | `-1127.40` |
| improved, `N=16`, `am=0.5` | `0.1535` | `-1298.73` |

The large components outside the covariant rank-eight image are hypercubic
cutoff artifacts. Their source dependence is so large that leave-one fits can
cross zero. A two-point line through either stencil merely produces another
large negative number; it is recorded as `valid_continuum_fit=false` and is
not evidence against the independently recovered continuum determinant.

## 5. Matched subtraction

The literal motion-scalar interaction is

\[
\frac34\lambda|\psi|^{4/3},
\qquad [\lambda]=\frac83,
\qquad \mu=\lambda^{3/8}.
\]

Its dimensionless ultraviolet strength is

\[
\boxed{g_{eff}(p)=\frac{\lambda}{p^{8/3}}
=\left(\frac\mu p\right)^{8/3}\longrightarrow0.}
\]

The short-distance fixed point is therefore the free kinetic theory. This
selects, but does not by itself numerically prove, cancellation of the leading
same-regulator geometric artifacts. The executable renormalization condition
is:

1. Measure `m_gap` and the stress normalization `Z_T` in the interacting
   ensemble.
2. Evaluate a free reference with the same lattice, stencil, sources,
   contacts, `m_ref=m_gap`, and `Z_T`.
3. Form the paired full-covariance difference
   `Delta y_a=y_int^a-y_free^a`.
4. Extrapolate `Delta y_a` across cutoffs and both stencils.
5. Restore the independently known continuum response:

\[
\boxed{
\zeta_{int}=\frac1{30240(4\pi)^2m_{gap}^2}
+v_{RF}P_8\lim_{a\to0}\Delta y_a.
}
\]

The subtraction is a defined renormalization scheme, not a permission to
assume the difference converges. The next smoke run must demonstrate smaller
cutoff and stencil variation in `Delta y` than in either absolute response.

## 6. Theory gates

```text
traceful determinant contacts             = exact;
sixth-order Taylor response                = validated;
independent continuum determinant          = exact scalar C3 recovered;
absolute coarse-lattice coefficient        = rejected;
same-regulator matched subtraction         = selected;
paired interacting smoke                   = permitted next;
interacting long run                       = withheld;
GR/Newton/PPN                              = unchanged;
Maxwell/Poynting                           = unchanged;
Gamma_MTS,res                              = 0.
```

The result strengthens source coupling discipline but does not add a
six-derivative term to the active MTS action. `C^3` still begins at cubic
metric order, so the calibrated massless spin-two pole and linear local limits
remain untouched.

## 7. Next target

`4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-continuum-coefficient-or-zero-residual.md`

Run paired short interacting/free chains at two cutoffs and both stencils,
using common random numbers where possible. Measure the full covariance of
`Delta y`, test the rank-eight and leave-one projections, and launch no long
run unless the matched difference has a common regulator trend.

No GitHub action or public claim is authorized.

## Sources

- `post-checkpoint-work/4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-TTT-Weyl-cubic-projection.md`
- `post-checkpoint-work/4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md`
- `post-checkpoint-work/scripts/Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4912_CONTINUUM_RECOVERY.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4912_QUOTIENT_RECOVERY.csv`
- `post-checkpoint-work/runs/20260712-4912-checkpoint/log.txt`
