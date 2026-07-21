# 4868 - Finite-compactness variational reduction and ADM completion gate

Marker: `FINITE_COMPACTNESS_VARIATIONAL_ADM_COMPLETION_4868`

Decision: `SMALL_P_FIXED_GR_AETHER_FUNCTIONAL_AND_FINITE_C_BVP_DERIVED_TWO_SOLVER_SMOKE_REGULAR_RAW_BULK_EXTRAPOLATION_REJECTED_BY_KNOWN_FIRST_SENSITIVITY_EXACT_AETHER_NOETHER_CHARGE_AND_SINGLE_V4_ADM_COMPLETION_INTERVAL_DERIVED_PRIVATE_NONCLAIM`

Supersession note from checkpoint 4869: the `C=0.3` comparison to a series truncated at `C3` does not by itself prove that the resummed bulk branch is incomplete. The exact `l=1` metric Ward calculation makes the parent-action metric extraction equal to the bulk boundary functional, while a symmetric small-`C` test localizes the disagreement with Gupta et al. to the `C3` coefficient. The numerical `D2` calibration and the statement that a nonzero independent ADM completion is proved are therefore withdrawn; the `D4` interval remains only a bookkeeping allowance until the quartic Ward identity is derived.

## Result

The finite-compactness calculation has advanced, but the tempting shortcut does not give the physical quartic response by itself.

At fixed `r` and to first order in the public deviation parameter `p`, the moving-star problem reduces exactly to a unit-flow variational problem on the general-relativistic Tolman VII background. Its complete bulk coefficients through `v4`, its Euler boundary-value system, and its asymptotic aether Noether charge are now explicit. A collocation solve and an independent finite-basis variational solve find a regular fixed-background profile throughout the sampled corridor.

The decisive regression is negative: at `r=1/3,C=0.3`, the extrapolated fixed-background bulk result is

```text
f_bulk       = 0.27696368;
kappa4_bulk  = -0.15842314;
```

whereas the source-backed Tolman VII first response through `C3` is

```text
f_C3 = 0.4797508374.
```

The `42.27%` first-response deficit proves that `kappa4_bulk` is not a physical finite-compactness prediction. The missing contribution is no longer an unspecified whole boosted-star system: after adding the exact aether surface charge, it is one `v4,l=0` metric/matter ADM completion coefficient. The inherited binary window gives an explicit interval for that coefficient.

No finite-neutron-star `kappa4`, `g`, local-GR, or solitary-pulsar claim is promoted.

## Small-`p` reduction

On the selected public surface,

\[
c_i=p\,\bar c_i+O(p^2),
\]

with

\[
\bar c_1=\frac{1+r}{2},\qquad
\bar c_3=-\frac{1+r}{2},\qquad
\bar c_2=\frac{2}{3(1+r)},
\]

\[
\bar c_{14}=\frac{2r}{1+r},\qquad
\bar c_4=\bar c_{14}-\bar c_1.
\]

The `p0` metric and matter fields are the GR stellar solution. The leading flow equation is obtained by varying the coefficient of `p` on that fixed background. Metric and matter perturbations are still required to reconstruct the conserved mass; they do not enter the leading fixed-background flow Euler equation.

Write the GR metric as

\[
ds^2=-N(R)^2dt^2+A(R)^2dR^2+R^2d\Omega^2,
\]

and parameterize the physical spatial flow in the body frame by

\[
u^{\hat R}=\gamma v\,a(R)\cos\theta,
\qquad
u^{\hat\theta}=-\gamma v\,b(R)\sin\theta.
\]

The time component is fixed, not postulated:

\[
u^{\hat0}=\sqrt{1+\gamma^2v^2
\left(a^2\cos^2\theta+b^2\sin^2\theta\right)}.
\]

Substitution into

\[
\bar K=\bar c_1 I_1+\bar c_2 I_2+\bar c_3 I_3-\bar c_4 I_4
\]

and exact angular integration gives

\[
\int d^3x\sqrt{-g}\,\bar K
=\int dR\left[v^2L_2(a,b)+v^4L_4(a,b)+O(v^6)\right].
\]

The executable symbolic expressions for `L2` and `L4` are in `scripts/Y5_R2FR_4868_fixed_background_variational_remainder.py`. `L2` is quadratic in `(a,b,a',b')`; `L4` is the complete quartic coefficient after the unit constraint and the boundary factor `gamma v` are expanded consistently.

Let `q=(a,b)^T` and define

\[
D=L_{2,q'q'},\qquad M=L_{2,q'q},\qquad F=L_{2,qq}.
\]

The exact radial equation is

\[
\boxed{
Dq''+(D'+M-M^T)q'+(M'-F)q=0.
}
\]

Smooth-center and asymptotic-wind conditions are

\[
a-b=O(R^2),\qquad a',b'=O(R),
\]

\[
a=1+\frac{A_\infty}{R}+O(R^{-2}),\qquad
b=1+\frac{B_\infty}{R}+O(R^{-2}).
\]

An independent `v3` profile with zero residual boundary data does not contribute to the stationary bulk `v4` coefficient: its cross-term is the first variation of `L2`, hence an Euler term plus a vanishing boundary term. This closes the fixed-background bulk functional; it does not close the conserved ADM mass.

## Numerical solve

The background is the exact GR Tolman VII solution with `Rstar=1` and

\[
m(R)=\frac{\mathcal C}{2}(5R^3-3R^5),\qquad
\rho(R)=\frac{15\mathcal C}{8\pi}(1-R^2)
\]

inside the star, matched to Schwarzschild outside.

The precision result uses `scipy.solve_bvp`, regular-center conditions, first asymptotic Robin conditions, and a linear `1/Rmax` Richardson extrapolation from `Rmax=200` and `400`. The independent rational-basis variational solve has a positive sampled Hessian and agrees at the percent level before its basis becomes ill-conditioned. It is a cross-check, not a proof of global coercivity.

At the endpoint `r=1/3,C=0.3`, the extrapolated tails are

```text
A_infinity = -0.35073278;
B_infinity = -0.30918749.
```

The small-compactness scan returns the checkpoint-4867 weak coefficients, while the finite-compactness first-response comparison rejects the raw bulk extrapolation. This is the calibration that prevents a numerically smooth but physically incomplete branch from being promoted.

## Exact aether surface charge

Foster's Noether charge gives

\[
E_{\ae}=
\frac{1}{8\pi G}\int_\infty dS\,
t_a(r^bt_c+r_ct^b)K^a{}_b\bar u^c.
\]

For the asymptotic tails above and `Rstar=1`, its coefficients at first order in `p` are

\[
\frac{E_{\ae,2}}p=
\frac{
9\mathcal Cr^2-36\mathcal Cr+11\mathcal C
(3r^2+1)A_\infty+(12r+4)B_\infty
}{18(1+r)G},
\]

\[
\frac{E_{\ae,4}}p=
\frac{
45\mathcal Cr^2-135\mathcal Cr+50\mathcal C
(12r^2-9r+7)A_\infty
(-12r^2+54r-2)B_\infty
}{45(1+r)G}.
\]

The static term is

\[
\frac{E_{\ae,0}}p=-\frac{\mathcal Cr}{(1+r)G},
\]

which reproduces the published aligned result `E_ae=-(c14/2)M_ADM` at this order.

A pure GR boost gives

\[
A_\infty=B_\infty=-2\mathcal C+O(\mathcal C^2).
\]

Consequently the surface charge alone contains universal `O(C)` pieces,

\[
\frac{E_{\ae,2}}p=
\frac{\mathcal C(3r^2-60r+1)}{18(1+r)G}+O(\mathcal C^2),
\]

\[
\frac{E_{\ae,4}}p=
\frac{\mathcal C(9r^2-45r+8)}{9(1+r)G}+O(\mathcal C^2).
\]

These are frame/metric-charge terms. They must cancel against the corresponding ADM contribution before the structure-dependent response, which begins at `O(C2)` in the mass coefficient, is read. Adding the bulk and aether surface numbers without that completion produces an unphysical result and is explicitly quarantined.

## ADM completion contract

The conserved energy is

\[
Q_n=E_{{\rm ADM},n}+E_{\ae,n}.
\]

For bookkeeping, define the computed fixed-background bulk coefficient `B_n` and the residual completion

\[
D_n:=E_{{\rm ADM},n}-B_n,
\qquad
Q_n=B_n+E_{\ae,n}+D_n.
\]

`D_n` is a definition of the missing metric/matter completion; it is not a new physical field or fitted closure.

The known first response fixes

\[
\frac{Q_2}{M}=-\frac f2,
\]

and therefore calibrates both `E_ADM,2` and `D2`. At `r=1/3,C=0.3`,

```text
B2/M       = -0.13848184;
E_ae,2/M   = -0.40849217;
Q2/M       = -0.23987542;
E_ADM,2/M  = +0.16861675;
D2/M       = +0.30709859.
```

This nonzero completion explains the failed bulk-only regression.

For the quartic response,

\[
\kappa_4=\frac{Q_4}{M}
=\frac{B_4+E_{\ae,4}+D_4}{M}.
\]

At the same endpoint,

```text
B4/M       = -0.15842314;
E_ae,4/M   = -0.18918470.
```

The inherited no-cancellation binary box `|kappa4|<=1.4532678437` becomes

\[
\boxed{
-1.1056600\le \frac{D_4}{M}\le1.8008757.
}
\]

Equivalently, the standard metric ADM coefficient must obey

\[
-1.2640831\le\frac{E_{{\rm ADM},4}}M\le1.6424525.
\]

The leading-compactness continuation would require `D4/M=-0.0809636`, well inside this interval, but that number is only a diagnostic center inherited from checkpoint 4867. The finite-compactness `D4` must be derived from the `v4,l=0` Einstein/Hamiltonian constraint.

## What is closed and what is not

Closed here:

1. the fixed-`r`, first-order-`p` GR-background flow reduction;
2. the exact angularly reduced `L2` and `L4` functionals;
3. the finite-compactness flow BVP and two-solver smoke regularity;
4. the exact asymptotic aether energy through `v4`;
5. the rejection of the bulk-only finite-compactness prediction;
6. the one-scalar ADM completion contract and its observational interval.

Still open:

1. the sourced `v4,l=0` metric/Hamiltonian equation at fixed baryon number;
2. the asymptotic ADM monopole `D4` and therefore physical finite-`C` `kappa4`;
3. the `v3,l=1` asymptotic coefficient needed for the independent response extraction;
4. a tabulated-EoS repetition;
5. the solitary one-body preferred-frame map and local-GR promotion.

## Decision

The fixed-background route is retained as a derived subproblem and rejected as a standalone mass prediction. The next calculation is not another source hunt or another placeholder audit: it is the single `v4,l=0` linearized Einstein/Hamiltonian constraint whose asymptotic monopole supplies `D4`.

Next: `4869-Y5-R2FR-v4-l0-linearized-Einstein-constraint-and-ADM-monopole-or-kappa4-completion-bound.md`.

Sources: [Foster 2005](https://arxiv.org/abs/gr-qc/0509121); [Eling 2005](https://arxiv.org/abs/gr-qc/0507059); [Foster 2007](https://arxiv.org/abs/0706.0704); [Gupta et al. 2021](https://arxiv.org/abs/2104.04596).
