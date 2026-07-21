# 4869 - Metric Ward completion and the compactness-C3 discrepancy

Marker: `L1_METRIC_WARD_AND_C3_DISCREPANCY_4869`

Decision: `FULL_GR_MATTER_L1_SHIFT_HESSIAN_AND_AETHER_SOURCE_DERIVED_GAUGE_INVARIANT_METRIC_RESPONSE_EQUALS_ONSHELL_BULK_BOUNDARY_FUNCTIONAL_GUPTA_AGREEMENT_THROUGH_C2_BUT_C3_CONFLICT_LOCALIZED_4868_NONZERO_D2_CALIBRATION_WITHDRAWN_V4_WARD_EXTENSION_NEXT_PRIVATE_NONCLAIM`

## Result

Checkpoint 4868 found a smooth finite-compactness flow branch but treated its difference from the Tolman VII `C3` series at `C=0.3` as proof that an independent ADM completion was missing. That inference was too strong because the comparison used a truncated series at a point where its `C3` term is as large as its `C2` term.

The metric response has now been derived instead of represented by `D2`. The complete stationary `l=1` GR shift action, the comoving perfect-fluid term, and the linear aether source have been generated from the parent correspondence action. Their Ward reduction leaves one gauge-invariant shift combination `Z`, and the radial metric equation fixes it algebraically from the aether profile.

At infinity, the metric sensitivity extracted from `Z` is identically equal to the on-shell bulk boundary functional once the exterior aether equation is imposed. Therefore the parent action does not produce an independent fitted `D2` term. The `D2/M=0.3071` number introduced in checkpoint 4868 by forcing the `C3` series value at `C=0.3` is withdrawn.

A symmetric positive/negative compactness calculation then localizes the external disagreement:

```text
coefficient of C:    parent action = 10/7;       Gupta = 10/7;
coefficient of C^2:  parent action is consistent with -2.68259518;
coefficient of C^3:  parent action = 4.94..5.00; Gupta = 10.83751760.
```

The mismatch begins at `C3`; it is not a generic failure of the finite-background solve and it is too large to be explained by the numerical residual. Neither side is promoted at finite compactness until the source of this coefficient conflict is found or the full first-order stellar system independently selects one branch.

## GR plus matter shift functional

Use ADM variables for the GR Tolman VII background,

\[
ds^2=-N^2dt^2+h_{ij}(dx^i+\beta^i dt)(dx^j+\beta^jdt),
\]

with the stationary polar dipole shift

\[
\beta_R=\epsilon k(R)\cos\theta,
\qquad
\beta_\theta=-\epsilon R s(R)\sin\theta.
\]

The exact angularly integrated Einstein shift functional is

\[
I_{\rm GR}^{(2)}=\int dR\,d\Omega\,N\sqrt h
\left(K_{ij}K^{ij}-K^2\right),
\]

where

\[
K_{ij}=\frac{D_i\beta_j+D_j\beta_i}{2N}.
\]

For a perfect fluid comoving with the coordinates, the required quadratic matter term is

\[
I_{\rm m}^{(2)}=
\int dR\,d\Omega\,
\frac{\sqrt h}{2N}(\rho+P)\beta_i\beta^i.
\]

Its coefficient is not guessed. Multiplying this term by `16 pi G` inside the gravitational normalization makes every compact-support time reparameterization

\[
k=N^2H',\qquad s=\frac{N^2H}{R}
\]

an exact zero mode on the GR TOV background. Either sign or any other coefficient violates the Ward identity by a term proportional to `(rho+P)`.

## Gauge-invariant shift equation

Define

\[
X=\frac{N'}N
=\frac{A^2-1}{2R}+4\pi GRA^2P
\]

and

\[
\boxed{
Z=k-Rs'-s+2RXs.
}
\]

`Z` vanishes for the pure gauge mode above. Varying the exact GR-plus-matter functional gives

\[
\boxed{
\mathcal E_k^{\rm GR+m}=-\frac{8\pi}{3AN}Z,
}

\[
\mathcal E_s^{\rm GR+m}
=-\frac{8\pi}{3AN}
\left[
RZ'+\left(A^2-1+4\pi GR^2A^2(P-\rho)\right)Z
\right].
\]

The second equation is the radial Ward derivative of the first.

The first-order public aether action supplies an exact cross functional

\[
I_{\ae}^{(kv)}=
\int dR\,L_{kv}[a,b;k,s].
\]

If

\[
\mathcal S_k=
\frac{d}{dR}\frac{\partial L_{kv}}{\partial k'}
-\frac{\partial L_{kv}}{\partial k},
\]

the full radial momentum equation is algebraic:

\[
\boxed{
Z=-\frac{3AN}{8\pi}\mathcal S_k.
}
\]

The executable `Lkv` and its 106-operation Euler source are in `scripts/Y5_R2FR_4869_l1_metric_response_source.py`. No metric-response coefficient is inserted.

## Asymptotic sensitivity identity

Let the fixed-background flow tails be

\[
a=1+\frac{A_\infty}{R}+O(R^{-2}),
\qquad
b=1+\frac{B_\infty}{R}+O(R^{-2}).
\]

On the Schwarzschild exterior, the sourced metric invariant has

\[
\boxed{
\frac{Z_\infty}{M/R}
=-\frac{4(A_\infty-2B_\infty-\mathcal C)}
{3\mathcal C(1+r)}.
}
\]

The exact Yagi-Foster asymptotic map gives, at first order in `p`,

\[
f=\frac14\left(\frac{Z_\infty}{M/R}+2\bar c_{14}\right),
\qquad
\bar c_{14}=\frac{2r}{1+r}.
\]

Therefore

\[
\boxed{
f_{\rm metric}
=\frac{-A_\infty+2B_\infty+\mathcal C(1+3r)}
{3\mathcal C(1+r)}.
}
\]

Independently, the stationary quadratic flow action reduces to its outer boundary and gives

\[
f_{\rm bulk}
=\frac{
(3r^2+6r+1)A_\infty+4B_\infty
+\mathcal C(6r^2+18r+8)
}{18\mathcal C(1+r)}.
\]

The exterior flow equation imposes

\[
\boxed{
(3r^2+6r+7)A_\infty-8B_\infty
+2\mathcal C(3r^2+1)=0.
}

Substitution proves

\[
\boxed{f_{\rm metric}=f_{\rm bulk}.}
\]

This is the missing metric completion theorem at first response. Standard ADM and aether surface pieces still exist separately, but their split cannot be used to add a new free `D2` on top of the parent-action mass response.

## Controlled compactness-series comparison

The numerical coefficient test uses paired `+C` and `-C` GR backgrounds. This is a mathematical parity diagnostic around `C=0`, not a claim that negative-density stars are physical. If

\[
f(C)=a_1C+a_2C^2+a_3C^3+\cdots,
\]

then

\[
a_2(C)=\frac{f(C)+f(-C)}{2C^2}=a_2+O(C^2),
\]

\[
a_3(C)=\frac{f(C)-f(-C)-2a_1C}{2C^3}=a_3+O(C^2).
\]

Three-domain outer-radius control (`Rmax=100,200,400`), quadratic `1/Rmax` extrapolation and `2e-8` BVP residuals give

| `C` | `a2(C)` | `a3(C)` |
|---:|---:|---:|
| 0.015 | -2.68473756 | 4.96135544 |
| 0.020 | -2.68619992 | 4.96409959 |
| 0.030 | -2.69054982 | 4.97224212 |
| 0.040 | -2.69671969 | 4.98379186 |

Linear and quadratic extrapolations in `C2` place the parent-action cubic coefficient conservatively in

\[
\boxed{4.94<a_3^{\rm parent}<5.00.}
\]

The Gupta-Tolman expression gives

\[
a_3^{\rm Gupta}
=\frac{975961420}{90053964}
=10.8375176022\ldots.
\]

The intervals are disjoint by at least `5.8375`. The conflict is therefore real at the current equation level, although its origin remains open. Candidate causes to test are the correlated public-frame limit of the published `C3` expression, an omitted boundary/convention term in the reduced action, or an error in one of the long analytic `C3` calculations.

## Consequence for the quartic response

Checkpoint 4868's finite `D4` interval remains an algebraic reparameterization of the observational box, but `D4` is no longer presumed to be an independent physical completion merely because the first-response `C3` expression differs at `C=0.3`.

The next decisive theorem is the quartic extension of the mass-variation identity: generate the `v3,l=1` surface source and prove whether the on-shell `L4` functional already equals the physical `kappa4`, or whether a nonvanishing metric/matter boundary residual survives. Only then should `kappa4_bulk=-0.1584` at the endpoint be promoted or rejected.

## Decision

The parent action's first-response metric completion is derived and contains no adjustable closure. The external `C3` series is retained as a serious unresolved cross-check, not used as exact finite-compactness calibration. The project advances to the quartic Ward/surface identity rather than solving for a completion coefficient whose independence has not been established.

Next: `4870-Y5-R2FR-v4-mass-variation-surface-identity-and-v3-l1-asymptotic-response-or-ADM-monopole.md`.

Sources: [Yagi et al. 2013](https://arxiv.org/abs/1311.7144); [Gupta et al. 2021](https://arxiv.org/abs/2104.04596); [Foster 2005](https://arxiv.org/abs/gr-qc/0509121); [Eling 2005](https://arxiv.org/abs/gr-qc/0507059).
