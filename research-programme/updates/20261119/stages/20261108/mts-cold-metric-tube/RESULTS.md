# Cold metric/background coupling — verified 2026-11-08

## Scientific advance
Combining the retained scalar continuity and current equations cancels the large oscillatory pressure terms in the GR metric-rate row. The heavy scalar now has a compact, source-derived momentum-constraint form, with the existing quadrature defect kept explicit.

The derivation extends to the FULL native momentum row, for both baseline and MTS:

    Phi_N+Psi=(1-3Delta/d)[Q+Delta e_alpha/sqrt(rho_c)]/(2kH)-3P_b/d.

This matches63 full native rows across the three cold epochs and all three inherited wavelengths. Worst relative error4.080448e-16. The54 separate heavy-column checks agree to8.532282e-14 relative.

The quadrature and baryon-pressure terms are not hidden. The native approximation omits the baryon pressure term in density continuity while retaining it in the velocity equation; the resulting -3P_b/d term appears in BOTH baseline and MTS. Its largest tested coefficient is6.007380e-14, while the explicit quadrature correction is up to2.008955e-8. These are coordinate-row coefficients, not fractional observational errors. This stage preserves the inherited source rather than silently changing it.

## Exact source derivatives
Derived epsilon=3rho/d0 and its exact directional derivatives:

    epsilon_0=epsilon[-1-d0,0/d0]
    epsilon_c=3epsilon(1-epsilon).

The normalized metric denominator is exactly1-epsilon cos(2theta). Its constant coefficient is exactly1 and both constant derivatives exactly0. This replaces cancellation-prone numerical differences without changing the bank, grids or tolerances.

Old numerical jets agree with the derived derivatives within1.895443e-6 relative. Replacing them changes the already-qualified coupled generator by at most3.330669e-16 absolute. Baseline heavy-phase denominator and derivatives are exactly absent; the total baseline denominator is checked separately.

## Uniform background uncertainty, not sampled maxima
The inherited scalar uncertainty tube is propagated through the compact metric formulas using50-digit outward-rounded interval automatic derivatives. The enclosure covers the entire saved cold window and all phases, including the original background radius and heavy-density uncertainty.

It bounds the heavy columns of the full coupled metric and their coordinate-feedback inverse. It does not set other perturbations to zero or evolve a new heavy-only cosmology.

| k family | GR metric-column difference | Spatial-Poisson difference | GR closed-inverse difference | Poisson closed-inverse difference |
|---|---:|---:|---:|---:|
|half|2.526800e-12|1.882468e-9|3.341283e-20|1.782087e-17|
|balanced|6.341206e-13|1.180451e-10|8.415476e-21|1.118712e-18|
|double|1.610615e-13|7.479083e-12|2.180761e-21|7.152341e-20|

These are dimensionless coefficient/operator bounds in the stated relative coordinates. Physical-energy readout bounds L_h/h are saved separately in audit/result.json and have units Mpc; do not read them as percentages. Their largest GR and Poisson bounds are2.647476e-5 Mpc and0.03149918 Mpc respectively.

The actual phase-uniform closure contractions are at most6.437003e-15 for GR and2.297785e-12 for spatial Poisson on this interval enclosure. Thus the saved background uncertainty is harmless to inversion of THIS scalar/metric feedback map. It does not imply negligible self-gravity or certify the entire evolution error.

## Independent checks and provenance
- Seven exact symbolic identities, including the full retained momentum row.
-63 full-row native checks,54 heavy-column checks, baseline phase controls.
-288 independent70-digit tube fixtures, using the original unsimplified stress/current equations and forcing matrices.
-648 independent70-digit derivatives checked against the interval automatic-derivative bounds.
- Bounds frozen before fixtures; largest fixture/bound ratio0.9999998736408525.
- Original numerical2e-5 and algebra1e-10 gates unchanged.

The intervals concern the retained finite thermal source and previously accepted background tube. Native arithmetic and the parent's thermal-continuum/global-ODE accuracy are not independently certified by these interval calculations. Their existing provenance and checks remain in force.

One implementation attempt was preserved after a TypeError applying abs() to a list of matrix differences. The corrected, separately named collector converts the list to an array; it does not relax any physics check. DEVELOPMENT.md records this. Accepted outputs use metric-02, not the incomplete metric-01 folder.

## Next physical calculation
Use the full momentum identity to derive and bound the remaining external-matter metric columns in the SAME coupled system. The defect derivative and most pressure cancellation are now eliminated algebraically, so this need not repeat the earlier cancellation-heavy reconstruction.
Carry the free-generator/source-derivative uncertainty, including the saved conformal-clock uncertainty in hierarchy closures, into the uniform coefficient/remainder budget. Then transport the original preparation with both physical endpoint maps and the previously derived logarithmic-norm control.

## Files
- DERIVATION.md: scalar/full momentum identities, exact denominator jets and interval sensitivity proof.
- metric_math.py, momentum_identity.py, interval_math.py: accepted formulas and implementation.
- collect_metric_v2.py and each label/metric-02/: accepted native/source results and repaired packets.
- validate_tube.py and tube-validation/: independent70-digit tests with frozen bounds.
- audit_metric.py and audit/result.json: source hashes, symbolic checks, reproduced intervals and gradient audit.
- CLEANUP.json and closeout.json: exact worker exits and artifact seal.

All work stays local. Earlier stages, original bank/grids and the retained theory are preserved.
