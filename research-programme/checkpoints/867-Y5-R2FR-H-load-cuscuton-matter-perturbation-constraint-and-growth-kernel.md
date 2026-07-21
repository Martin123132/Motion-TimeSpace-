# 4851 Y5 R2FR H-load cuscuton matter constraint, growth kernel and acceleration gate

**Status:** The minimal cuscuton-equivalent (H)-load branch now has its exact dust perturbation constraint, modified Poisson equation and potential-growth equation. The constraint is pole-free and recovers the standard calibrated Newton coefficient at high wavenumber. However, differentiating the implicit background exposes a decisive failure of the SH0ES edge: every SH0ES best fit is strongly decelerating today, despite its distance-only AIC/BIC gain. The no-SH0ES interior rows accelerate and have finite growth kernels, but remain statistically unpreferred.

**Decision:** `SH0ES_EDGE_FAILS_ACCELERATION_GATE_CUSCUTON_CONSTRAINT_AND_HIGH_K_NEWTON_LIMIT_PASS_NO_SH0ES_INTERIOR_ACCELERATES_BUT_IS_UNPREFERRED_PRIVATE_NONCLAIM`.

## 1. Exact background derivatives

Write the implicit equation as

\[
\mathcal F(E,z)=E^2-\Omega_{m0}(1+z)^3-1+\Omega_{m0}
-A_H\left[R((qE)^3)-R(q^3)\right]=0.
\]

The 4849 branch has

\[
\mathcal F_E>0.
\]

Implicit differentiation gives

\[
\boxed{
E'(z)=\frac{3\Omega_{m0}(1+z)^2}{\mathcal F_E}>0
}
\]

and therefore

\[
\boxed{
\dot H=-H_0^2(1+z)EE'<0.
}
\]

This sign is exact for the complete fitted expanding branch; it is not a numerical-grid inference.

At (z=0),

\[
\mathcal F_E(1,0)=2(1-f_K),
\]

so

\[
E'_0=\frac{3\Omega_{m0}}{2(1-f_K)},
\qquad
\boxed{
q_0=-1+\frac{3\Omega_{m0}}{2(1-f_K)}.
}
\]

Present acceleration requires

\[
\boxed{
f_K<1-\frac32\Omega_{m0}.
}
\]

## 2. The SH0ES distance lead fails the acceleration gate

All six SH0ES positive-(H)-load rows fail (q_0<0):

- broad (f_K=0.95) rows have (q_0\simeq8.85);
- standard (f_K=0.95) rows have (q_0\simeq8.9);
- strict (f_K=0.80) rows have (q_0\simeq1.42).

Their present jerk values are also extremely negative: order (10^4) for the broad/standard cap and order (10^2) for the strict cap. The distance likelihood was exploiting an ultra-low-redshift boundary layer near the implicit fold, not finding a conventional accelerating late-time solution.

The six no-SH0ES rows instead have

\[
q_0\simeq-0.47
\]

for the exponential kernel and

\[
q_0\simeq-0.45
\]

for the tanh kernel, with jerk near unity. Those rows pass this physical gate but did not beat the best 4849 AIC/BIC baselines.

The SH0ES AIC/BIC improvement is therefore demoted. It remains a useful warning about calibration-sensitive boundary layers, not evidence for the theory.

## 3. Exact cuscuton perturbation constraint

For longitudinal-gauge scalar perturbations with pressureless matter, the minimally coupled cuscuton constraint is

\[
\boxed{
\delta\phi_k=
\frac{3\dot\phi(\dot\Phi+H\Phi)}{k^2/a^2-3\dot H}.
}
\]

This is the standard minimal-cuscuton result derived in [Afshordi et al.](https://arxiv.org/abs/astro-ph/0702002) and follows directly for the 4850 Legendre field. It contains no second time derivative of (\delta\phi).

Define

\[
D_k=\frac{k^2}{a^2}-3\dot H.
\]

Since (\dot H<0),

\[
\boxed{D_k>0}
\]

for every real (k) and every fitted (z\ge0). The minimal branch has no finite-wavenumber cuscuton constraint pole.

## 4. Modified Poisson equation and local Newton limit

Eliminating (\delta\phi) gives

\[
\boxed{
\frac{k^2}{a^2}\Phi
+\left[
3H+\frac{9H(2\dot H+3H^2\Omega_m)}{2D_k}
\right](\dot\Phi+H\Phi)
+\frac{\delta\rho_m}{2M_{\rm Pl}^2}=0.
}
\]

At local/subhorizon wavenumber,

\[
\frac{k^2}{a^2}\gg H^2,|\dot H|,
\]

the second term is suppressed by (H^2a^2/k^2), giving

\[
\boxed{
\frac{k^2}{a^2}\Phi
=-\frac{\delta\rho_m}{2M_{\rm Pl}^2}
+O\!\left(\frac{H^2a^2}{k^2}\right).
}
\]

Thus the calibrated Newton/Poisson coefficient is unchanged. Together with the exact stationary local memory zero, this removes the (H)-load memory sector as a local Newton obstruction without fitting (G) or importing a plateau.

## 5. Potential-growth kernel

The exact dust potential equation is

\[
(1+C_2)\ddot\Phi
+(4H+C_1+C_2H+C_3)\dot\Phi
+C_\Phi\Phi=0,
\]

where

\[
C_1=\frac{3(\ddot H+3H\dot H)}{D_k},
\]

\[
C_2=\frac{3(2\dot H+3H^2\Omega_m)}{2D_k},
\]

\[
C_3=
\frac{3[2H(k/a)^2+3\ddot H](2\dot H+3H^2\Omega_m)}{2D_k^2},
\]

and

\[
C_\Phi=3H^2+\dot H-\frac32\Omega_mH^2+C_1H+C_2\dot H+C_3H.
\]

At (k=0), exact substitution of the implicit derivative gives

\[
\boxed{1+C_2=\frac{\mathcal F_E}{2E}>0.}
\]

At (z=0), this is (1-f_K). For finite (k), the negative (C_2) magnitude decreases, so the coefficient is even farther from zero. All 72 model/mode scan rows pass (D_k>0) and (1+C_2>0) over (0\le z\le50).

## 6. Growth smoke result

The exact kernel was integrated from (z=50) with matter-era smoke normalization

\[
\Phi=1,
\qquad
d\Phi/dz=0,
\]

for (k=10^{-3},10^{-2},10^{-1}\,h\,\mathrm{Mpc}^{-1}). Broad/strict SH0ES and broad no-SH0ES rows were compared to matched-(\Omega_{m0}) LCDM backgrounds.

All eighteen integrations are finite. On (k\ge10^{-2}\,h\,\mathrm{Mpc}^{-1}), the present potential and density transfer are percent-level departures from matched LCDM, approaching the exact Newton coefficient at higher (k). These are smoke transfers, not growth-data likelihoods: the initial spectrum, radiation, neutrinos and covariance have not been supplied.

## 7. Branch decision and local-GR consequence

The disciplined result is:

1. the minimal cuscuton completion is constraint-safe and has an exact high-(k) Newton limit;
2. the SH0ES edge is rejected because it predicts present deceleration and an extreme low-redshift jerk;
3. the no-SH0ES interior branch remains mathematically viable but empirically unpreferred;
4. no cosmology claim follows from the growth smoke;
5. local stationary silence plus high-(k) Poisson recovery should now be propagated into the local-GR residual spine.

This closes the immediate cosmological perturbation gate without pretending the attractive distance-only edge survived.

## 8. Machine evidence

- `P8_Y5_R2FR_4851_BACKGROUND_ACCELERATION_GATE.csv`
- `P8_Y5_R2FR_4851_CONSTRAINT_KERNEL.csv`
- `P8_Y5_R2FR_4851_GROWTH_SMOKE.csv`
- `P8_Y5_R2FR_4851_PERTURBATION_THEOREMS.csv`
- `P8_Y5_BRR545_4851_VALIDATION.csv`

All outputs remain `valid_for_claim=false`.

## 9. Next target

`4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md`
