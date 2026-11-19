# Derived feedback propagated through the original perturbation system

Completed locally on2026-11-09. The preceding feedback-source stage is retained unchanged. Authoritative final comparisons are each family's comparison-02/result.json, qualified projections are projection-02, and the full audit is audit/result.json. Earlier cubic projection-01/comparison-01 outputs remain available as superseded diagnostics.

## Physical advance

The previously derived h=R_total delta_s now has a computed accumulated response:
    z_N=M z+h, z(N0)=0.
All source components, original phase history, GR/spatial-Poisson branches and full G192 hierarchy are retained. Adding this z does not replace the inherited physical mode or reset its existing error.

Eighteen forward calculations cover baseline/MTS, three original wavelengths,4096/2048 maximum time steps, andnine/five original source epochs. The same ten terminal physical maps are used for each case. No fitted coefficient, new dataset or changed physical source is introduced.

## What the calculations show

The entries below are fractions of the retained original reference-output scales, not new observational fit statistics. Each value is a maximum over both branches and the ten terminal channels.

| Wavelength | Calculated terminal shift | Qualified numerical Cauchy budget | Observed nine/five-source change | Corrected reference error |
|---|---:|---:|---:|---:|
| half | 4.4718484232131906e-12 | 5.944201289679067e-11 | 2.733301281717532e-16 | 5.590060527714786e-7 |
| balanced | 5.39182212094739e-12 | 5.04168594107294e-11 | 7.08864463301631e-16 | 3.790790125353669e-7 |
| double | 1.5742822012396283e-11 | 7.286743244560731e-11 | 7.185141807540435e-16 | 0.0000016289008777856873 |

Thus this particular feedback is very small in the tested interval. Its largest terminal shift is1.5742822012396283e-11, while the largest retained comparison error remains1.6289008777856873e-6. The nine/five-source change is a numerical diagnostic, not a rigorous bound on an unsampled physical source.

Baseline shifts are of order1e-55 of the retained reference scales. They were calculated rather than artificially zeroed; they are rounding-level implementation controls, not a newly resolved physical effect. The baseline's normal-form contribution is exactly zero; its map contribution remains explicit.

## Independent derived response check

Reused the original source-independent adjoints satisfying lambda_N=-M^T lambda. Their signed projection of h agrees with the new forward response. The maximum disagreement normalized by the component absolute-response budget is7.208389714610088e-7. All120 terminal numerical/physical checks pass in the final representation.

The first cubic reuse attempt left three Cauchy-budget interpolation checks above2e-5: half/spatial-Poisson Pi, double/spatial-Poisson Pi, and double/spatial-Poisson delta_gamma. These are recorded rather than overwritten.

Differentiating the same adjoint equation gives
    lambda_NN=-M_N^T lambda-M^T lambda_N.
M_N is calculated from the retained operator splines and previously derived opacity derivative. Quintic Hermite interpolation then uses the SAME saved endpoint values plus derived first/second derivatives. No residual fit or new adjoint ODE solve was used. Both models and all wavelengths receive the same treatment; independent finite-difference operator-rate checks accompany all12 saved endpoint-jet records.

With the derived curvature:
- Maximum64/32 adjoint interpolation change in signed projections: 0.000008319355926351564.
- Maximum64/32 change in the numerical Cauchy budget: 0.000014718359721189341.
- Maximum quadrature change in signed projections: 3.233044920795457e-8.
- Maximum quadrature change in the numerical Cauchy budget: 1.1810616013893391e-7.
- All remain below the unchanged2e-5 numerical gate.

These are numerically qualified budgets for the retained interpolated source and adjoints, not certified continuous-time enclosures.

## Source uncertainty stays explicit

All24 strict forward time-step controls pass; the maximum feedback-relative difference is2.2438554251275495e-10. Sixteen of24 strict nine/five source-interpolation controls remain above2e-5: ten MTS components andsix tiny baseline map components.

The largest MTS feedback-relative source change is0.002634911892599208; baseline map-relative changes reach2.974096747830337 because their calculated signals are extremely small. No source control was relabeled as passed merely because its effect on the physical outputs is negligible. The corresponding maximum observed MTS physical-output change is7.185141807540435e-16. This is retained numerical evidence, not a continuum error theorem.

The prior omission budget and current h budget can be added only as the conditional budget for the two sources propagated under M. Their maximum such sum is3.0091956787157726e-6. It must not be called the remaining error after adding z: that error has different sources, explicitly including R z, physical-background mismatch and inherited discrepancies.

## What remains to advance

The tested h contribution is now calculated, so repeatedly polishing its tiny baseline tail is not the next priority. Derive the physical-background mismatch forcing in the same coordinates and retain/bound R z, then use the resulting budget to advance the original prepared trajectory toward the cold regime. NEXT.md gives the concrete operator identity to test.

The original bank, physical grids, couplings, preparation and tolerances remain unchanged: ALGEBRA1e-10, GATE2e-5 and DOP853 rtol2e-12/atol2e-14. One below-normal single-thread worker ran at a time. There were no failed numerical-worker attempts; the superseded cubic diagnostics were completed calculations with explicit unresolved checks. No GitHub, subagents, compiler, apps or servers were used. Final process exits and artifact hashes are recorded by the closeout.

