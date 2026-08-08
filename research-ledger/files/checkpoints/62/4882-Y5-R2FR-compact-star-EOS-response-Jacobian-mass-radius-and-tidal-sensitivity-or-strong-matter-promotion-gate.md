# 4882 Y5 R2FR compact-star TOV/Love response Jacobian and strong-matter gate

**Status:** The compact-star response problem left by checkpoint 4881 is now executable and differentiated. A coupled TOV plus relativistic `l=2` Love system is solved together with tangent equations for the `a_R` and `a_C` contact directions and for central density. Moving-surface terms and the fixed-mass projection are derived. Sixteen nonlinear finite-difference checks reproduce the tangent derivatives with maximum relative error `1.16e-6`. On a controlled causal `Gamma=2` polytrope, inherited contact-cap envelopes remain below `5.1e-17` even near `0.99 Mmax`; however, the EOS fails the observed two-solar-mass requirement and is not a microphysical promotion dataset.

Marker: `MTS_TOV_LOVE_RESPONSE_JACOBIAN_4882`.

## 1. EOS and unit contract

Use geometrized units `G=c=1` with one length unit

\[
L_\odot=GM_\odot/c^2=1476.669691\ {m m}.
\]

The controlled analytic EOS is

\[
p=Kn^2,
\qquad
\rho=n+p,
\qquad
K=100L_\odot^2.
\]

Its sound speed is

\[
c_s^2=\frac{dp/dn}{d\rho/dn}
=\frac{2Kn}{1+2Kn},
\]

so `0<=c_s^2<1`. Both density and pressure vanish continuously at the surface, avoiding the self-bound surface-jump correction.

This EOS is deliberately a response benchmark. Its maximum mass is `1.63728 M_sun`; because it does not support an observed `2 M_sun` star, it is not used for an astrophysical claim.

## 2. Contact directions in TOV units

Checkpoint 4881 gives

\[
\rho_{\rm eff}
=\rho-\lambda_R f_R-\lambda_Cf_C,
\]

\[
p_{\rm eff}
=p-\lambda_Rd_R-\lambda_Cd_C,
\]

with

\[
f_R=(\rho-3p)^2,
\qquad
f_C=4\rho(\rho/3+p),
\]

\[
d_A=n\frac{df_A}{dn}-f_A.
\]

In the TOV geometrized convention,

\[
\boxed{
\lambda_R=8\pi a_R\bar\ell_P^2,
\qquad
\lambda_C=8\pi a_C\bar\ell_P^2.
}
\]

The inherited checkpoint-4878 derivative-control caps become

\[
|\lambda_R|<5.66324\times10^{-11}\ {m m}^2
=2.59716\times10^{-17}L_\odot^2,
\]

\[
|\lambda_C|<1.69897\times10^{-10}\ {m m}^2
=7.79148\times10^{-17}L_\odot^2.
\]

These remain branch-control caps, not measured coefficients.

## 3. Coupled TOV-Love system

Let

\[
Y(r)=(m(r),n(r),y(r)),
\]

where `y=rH'/H` is the standard relativistic quadrupolar tidal variable. The background obeys

\[
Y'=f(r,Y;\lambda_R,\lambda_C).
\]

The first two components are the effective-EOS TOV equations from checkpoint 4881. The third is the Hinderer equation

\[
ry'+y^2+yF_T+r^2Q_T=0,
\]

with

\[
F_T=\frac{1-4\pi r^2(\rho_{\rm eff}-p_{\rm eff})}
{1-2m/r},
\]

\[
Q_T=
\frac{4\pi[5\rho_{\rm eff}+9p_{\rm eff}
+(\rho_{\rm eff}+p_{\rm eff})/c_{s,{\rm eff}}^2]}
{1-2m/r}
-\frac6{r^2(1-2m/r)}
-\frac{4(m+4\pi r^3p_{\rm eff})^2}
{r^4(1-2m/r)^2}.
\]

The implementation follows the relativistic matching construction of [Hinderer](https://arxiv.org/abs/0711.2420). At the center, `m=0` and `y=2`.

At the surface, compactness `C=M/R`, `y_R`, and the standard exterior matching formula give `k_2`; the dimensionless tidal deformability is

\[
\Lambda_T=\frac{2k_2}{3C^5}.
\]

## 4. Linear response operator

For either contact direction `A in {R,C}`, define

\[
Z_A=\frac{\partial Y}{\partial\lambda_A}.
\]

Differentiating the complete radial system before evaluating observables gives

\[
\boxed{
Z_A'=J_YZ_A+s_A,
\qquad
J_Y=\frac{\partial f}{\partial Y},
\qquad
s_A=\frac{\partial f}{\partial\lambda_A}.
}
\]

The Jacobian and sources are evaluated by complex-step differentiation of the same EOS-owned right-hand side. A third homogeneous tangent

\[
Z_c=\frac{\partial Y}{\partial n_c},
\qquad
Z_c'=J_YZ_c
\]

tracks the stable stellar sequence.

This is a genuine response operator: it does not rerun a finite coefficient and divide by it, and it uses the same equations for background, tangents and nonlinear validation.

## 5. Moving-surface theorem

The surface is defined by

\[
n(R,\lambda_A)=0.
\]

Differentiating this event gives

\[
\boxed{
R_A=-\frac{(Z_A)_n}{n'_s}.
}
\]

Because the EOS has zero surface density,

\[
m'_s=4\pi R^2\rho_s=0,
\]

so

\[
\boxed{M_A=(Z_A)_m.}
\]

The tidal matching variable requires its own surface displacement:

\[
\boxed{
(y_R)_A=(Z_A)_y+y'_sR_A.
}
\]

All `k_2` and `Lambda_T` derivatives are then obtained by differentiating the exterior matching function with respect to `(M,R,y_R)`.

## 6. Fixed-mass projection and turning point

At fixed central density the contact generally changes `M`. To compare stars at the same observed mass, shift along the stable GR sequence:

\[
\boxed{
\left.\delta n_c\right|_M
=-\frac{M_A}{M_c}\delta\lambda_A,
\qquad
M_c=\frac{\partial M}{\partial n_c}.
}
\]

For any observable `O`,

\[
\boxed{
\left.O_A\right|_M
=O_A+O_c\left(-\frac{M_A}{M_c}\right).
}
\]

Define the dimensionless turning-point condition number

\[
\boxed{
\kappa_{\rm turn}
=\left|\frac{d\ln M}{d\ln n_c}\right|^{-1}.
}
\]

As `dM/dn_c -> 0`, the fixed-mass projection becomes singular. This is a physical stability boundary, not a numerical failure, and prevents an unqualified maximum-mass promotion.

## 7. Background benchmarks

The stable branch and tidal solver give:

| model | `M/M_sun` | `R` (`km`) | `C` | `k2` | `Lambda_T` | `kappa_turn` |
|---|---:|---:|---:|---:|---:|---:|
| low mass | `1.00000` | `15.9120` | `0.09280` | `0.12500` | `12107.1` | `1.676` |
| canonical | `1.40000` | `14.1557` | `0.14604` | `0.07391` | `741.704` | `2.860` |
| `0.99 Mmax` | `1.62090` | `12.0464` | `0.19869` | `0.03803` | `81.8639` | `11.625` |

The maximum-mass solution is

\[
M_{\max}=1.637276M_\odot,
\qquad
R_{\max}=11.2746\ {m km}.
\]

## 8. Contact-response envelopes

Applying both coefficient caps independently and adding absolute tangent contributions gives:

| model | `|delta M|/M` fixed `n_c` | `|delta R|/R` fixed `M` | `|delta Lambda_T|/Lambda_T` fixed `M` | `|delta n_c|/n_c` fixed `M` |
|---|---:|---:|---:|---:|
| `1.0 M_sun` | `1.917e-18` | `9.604e-19` | `5.830e-18` | `3.213e-18` |
| `1.4 M_sun` | `1.913e-18` | `1.538e-18` | `1.073e-17` | `5.469e-18` |
| `0.99 Mmax` | `1.897e-18` | `6.112e-18` | `5.034e-17` | `2.205e-17` |

The fixed-central-density mass response remains near `2e-18`. Radius and tidal responses grow near the turning point because the fixed-mass sequence projection is becoming ill-conditioned. The derived response framework captures this amplification rather than hiding it inside a mean-density estimate.

## 9. Nonlinear validation

For the canonical model, each `lambda_R` and `lambda_C` tangent was checked against centered nonlinear solves at `+/-0.01 L_sun^2`:

- four observables at fixed central density;
- central density, radius, `k2` and `Lambda_T` at fixed mass.

All `16` derivatives pass. The maximum relative discrepancy is

\[
\boxed{1.15423\times10^{-6}.}
\]

The validation step is vastly larger than the physical caps but remains in the linear regime, making the derivative signal numerically resolvable.

## 10. Decision and next target

The following are now derived:

- coupled effective-EOS TOV and relativistic Love equations;
- contact and central-density tangent operators;
- moving-surface mass, radius and tidal response;
- fixed-observed-mass projection;
- an explicit turning-point condition number;
- nonlinear validation of both contact directions;
- physical cap envelopes for three stable-sequence models.

The strong-matter background is **not promoted publicly** because the `Gamma=2`, `K=100` EOS is a controlled analytic benchmark and fails the two-solar-mass requirement. A tabulated independently motivated EOS family is required to distinguish EOS degeneracy from a gravity residual.

Claim guards:

- Do not call the analytic polytrope a realistic neutron-star EOS.
- Do not extrapolate fixed-mass responses through `dM/dn_c=0`.
- Do not omit the moving-surface terms in radius or Love derivatives.
- Do not compare fixed-central-density and fixed-mass responses as if they were the same observable.
- Do not call derivative-control caps measured `a_R,a_C` values.
- Do not promote the tiny benchmark residuals to EOS-independent bounds.

Decision:

`TOV_LOVE_TANGENT_OPERATOR_DERIVED; MOVING_SURFACE_AND_FIXED_MASS_PROJECTIONS_DERIVED; TURNING_POINT_SINGULARITY_EXPLICIT; SIXTEEN_NONLINEAR_DERIVATIVE_CHECKS_PASS; CONTACT_CAP_RESPONSES_BELOW_5P1E_MINUS17_ON_CONTROLLED_POLYTROPE; MICROPHYSICAL_STRONG_MATTER_PROMOTION_WITHHELD`.

Next target:

`4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md`
