# Moving-source energy current: derivation and matched numerical test

Private/post-checkpoint-only. No GitHub action, coefficient fit, new trajectory, mode deletion, or change to the archived action. This report accompanies `DERIVATION-20260921-moving-source-localized-Legendre-current.md`.

## What has moved forward

The fixed-mesh quadratic current lemma now extends to the actual moving-source matter action of the retained annular candidate, including its nonquadratic proper-time clock, all field/source kinetic cross terms, moving physical cuts, Gram-node transport and explicit metric work. The current is calculated from the action and its Hessian before consulting the previous Ward-source result.

For all retained coordinates q, velocity v, matter Hessian M and Euler residual E,

    B=L_q-p_q v-p_t, E=B-M a,
    J_R=v^T(B_R-M_R M^-1 B),
    d_t H_R+J_R=Q_R-P_R,
    Q_R=-(L_R)_t, P_R=v^T M_R M^-1 E.

The implementation retains all 16,425 degrees of freedom, and uses the exact clock inertia m*N^2/(F*s^3), not a constant nonrelativistic mass. At the whole-domain cut the derived current is exactly zero algebraically. At a physical interior cut it includes the derivative of the moving cutoff; dropping that derivative is a different calculation.

## Structural invertibility, rather than a numerical assumption alone

On the N,F,J,s>0 chart with m>0, the velocity quadratic form of the Hessian is a sum of nonnegative wave squares and positive dust terms. If it vanishes, the source-velocity polynomial must vanish at every positively weighted material quadrature point. The retained degree is14, while the full assembly has48 distinct material points, so all source-velocity coefficients vanish. Then the wave squares force each quadratic spatial velocity polynomial to vanish at at least three distinct points in every cell. Applying the same material-polynomial argument kills all retained field-velocity coefficients. Thus no nonzero retained velocity lies in the kernel. The pinned field coordinate is not reintroduced as a spurious degree of freedom.

This proves positive definiteness under the stated chart and positive-quadrature assumptions. The banded field Cholesky and source Schur complement check the actual finite assembly as well. The smallest normalized source Schur eigenvalue is approximately0.08057 and the smallest normalized field Cholesky pivot approximately0.35673 in the cases inspected.

## Matched action/Ward comparison

Both MTS variants and the reference receive exactly the same procedure. Full Hessian integration uses spatial order12/material order48; local physical cuts use segmented orders8 and12, with512 and768 material samples respectively. Both archived Richardson metric and velocity estimates are retained. The five earlier diagnostic radii are unchanged, with additional empty and whole-domain cuts.

The independent comparison is

    J_new(R)-J_old(R)+P_R = integral^R I*r^2*div(T)_t dr.

Its right-hand side comes from the separately sealed cell/face/dust/Gram calculation, not from the new current or from the measured mass-current error. This is a numerical action-identity test using shared archived states and metric tangents, not new observational evidence.

| Order12 case | Maximum old mass-current residual | Maximum new residual | Maximum action/Ward difference (energy units) |
| --- | ---: | ---: | ---: |
| Reference | 1.37497678258e-11 | 1.42327870124e-12 | 5.54388447740e-18 |
| MTS primary | 3.66658021621e-11 | 1.42033046485e-12 | 2.98259148550e-17 |
| MTS alternative | 3.66658021604e-11 | 1.42033030425e-12 | 4.63533554629e-18 |

These are the inherited internal coordinate/canonical units, not laboratory SI error bars. The reference improves by roughly10 times and both MTS variants by roughly26 times. No free multiplier, boundary constant, or measured residual is supplied to the current calculation. Across both quadrature orders the maximum action/Ward discrepancy is3.083e-17; the whole-domain current is below3.273e-18. The archived momentum chain rule agrees to2.542e-15, and the full Hessian solve residual is below1.171e-15 relative.

## Conditional bridge to the mixed gravity constraint

The preceding radial-constraint derivation established, for I=N/sqrt(F), a_g=kappa/I and R_old=mu_t+a_g*J_old,

    R_old=-a_g*W_R

with compatible zero inner current and exact radial constraints, where W_R is the weighted temporal Ward integral. Combining this with the newly derived current gives

    R_new=mu_t+a_g*J_new=-a_g*P_R.

Thus the exact semidiscrete Euler equations E=0 are sufficient to eliminate this mixed mass-current defect, provided the diagonal constraints, inner condition and stated stress-energy balance hold. This is an explicit implication, not a fitted cancellation or an assumption that the archived acceleration residual is zero.

There is also a useful bound. For the same positive local/full integration, 0<=M_R<=M, and Cauchy-Schwarz gives

    |P_R| <= sqrt(v^T M_R v)*sqrt(E^T M^-1 E)
          <= sqrt(v^T M v)*sqrt(E^T M^-1 E).

The corresponding conditional mass-current bound is a_g times this expression. The checker evaluates the global dual-norm diagnostic and retains the actual localized projection. Numerically assembled and separately integrated quadratures are not advertised as an interval-certified bound.

## What the remaining offset means

The computed Euler-projection contribution is small but explicitly retained. Correcting the current leaves approximately1.4e-12 of mass-current mismatch shared by reference and MTS. Including the measured Euler projection returns the same small post-source offset found in the previous independent Ward calculation. This isolates the remaining discrepancy from the missing moving-source current terms; proving its numerical origin still requires the direct radial-constraint tangent rather than a fitted subtraction.

The constructed current is a localized semidiscrete energy current. Its full inverse Hessian can couple distant coefficients. The metric partial derivatives used here treat the archived background as given; they do not silently replace the full reduced gravity-matter Hessian. A gravitational mixed stress must be supplied by the same underlying action, rather than by relabeling a numerically useful energy current.

## Next constructive calculation

Derive the radial-shift variation of the same action and compare its mixed stress with this now-explicit current, retaining the coordinate-map and Gram terms. That will decide whether the energy-flow and gravity-flow equations follow from one action at finite resolution, or whether a specific completion/continuum-limit term is needed. Separately, the direct constraint tangent can test the shared mass-derivative offset without changing the physics or fitting it away.

## Reproducibility and scope

- Derivation: `DERIVATION-20260921-moving-source-localized-Legendre-current.md`.
- Helper: `scripts/annular_moving_Legendre_current_20260921.py`.
- Runner: `scripts/run_annular_moving_Legendre_current_20260921.py`.
- Independent checker: `scripts/seal_annular_moving_Legendre_current_20260921.py`.
- Fresh numerical evidence: `source-intake/navier-stokes/20260914/annular-moving-Legendre-current-attempt01/status.json`.
- Parent evidence: `source-intake/navier-stokes/20260914/annular-candidate-Ward-source-v2-final-integrity.json`.

The numerical run completed successfully in1643.901seconds (about27.4minutes), with18/18 predeclared comparisons passing. Its worker has exited. The independent checker records exact nonquadratic clock/coordinate-cut identities, the earlier quadratic reduction, sparse inverse residuals, independent label summation, every recorded scientific gate, omission controls, dual-norm diagnostics, inherited hashes and protected-workbench checks in `source-intake/navier-stokes/20260914/annular-moving-Legendre-current-final-integrity.json`. That seal, once COMPLETE, is authoritative for the independent validation count and CSV tables. Earlier files and unsuccessful attempts are preserved. One single-core BelowNormal numerical worker was used; the small Python launcher was not a second numerical job.
