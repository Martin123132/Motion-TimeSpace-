# Physical cold averaging remainder — verified 2026-11-08

## Advance
The retained coupled relative-phase system now has a derived physical normalization, a useful growth-norm estimate, and a qualified slow-background drift/remainder at the saved cold midpoint.

The construction reuses the sealed cold coefficient banks. It does not replace the theory, change the physical grids/bank/tolerances, reset a perturbation initial mode, or fit an extra parameter.

## Derivation
The heavy relative pair now uses the same density/velocity scale as the retained cold-fluid coordinates:
h=sqrt(rho_h) H/k. For u=D zeta,
A=D B D^-1+D_N D^-1.
The phase-dependent derivative of D is included BEFORE taking the physical-clock average.

Three exact identities verify the weight derivative, its analytic periodic primitive, and skew streaming in the remote G192 tail. An independent analytic formula reproduces the Fourier primitive and mean at about1e-15 relative accuracy.

The exact averaged-coordinate remainder is
E=(I+C)^-1[A C-C Abar-D_sigma C f].
Both physical flow directions, f0 and cos(2theta)fc, are included. The baseline has no heavy phase, and its primitive/remainder vanish.

See DERIVATION.md for equations, endpoint maps and the conditional transfer theorem.

## Results at the saved cold midpoint
These are operator/norm quantities, not fractional observational errors.

| k family | Mean growth norm GR | Mean growth norm spatial Poisson | GR remainder bound | Poisson remainder bound |
|---|---:|---:|---:|---:|
| half |0.06490645|0.06490753|1.169686e-8|2.026239e-7|
| balanced |0.06485761|0.06485788|1.167669e-8|5.533896e-8|
| double |0.06411359|0.06411366|1.167190e-8|1.856515e-8|

The growth norms apply to the explicitly defined weighted perturbation norm, not directly to density contrast. All baseline values are approximately0.06491. Large streaming frequencies remain in the equations but cancel from the symmetric growth form; the G192 hierarchy has not been discarded.

The remainder bounds cover every phase of the RETAINED FINITE FOURIER POLYNOMIALS at this midpoint. Their numerator uses commutator cancellation and explicitly bounds all omitted finite-polynomial harmonics. They are not yet a uniform analytic-source or whole-history bound.
Primitive norm bounds are about5.57e-9. The sampled GR remainder is about9.5e-9, below its polynomial bound.

## Validation
- 36 shifted physical-source families, containing9,216 coefficient evaluations.
- 288 independently checked native phases on those shifted families.
- 18 shifted baseline controls, with zero phase dependence.
- Nine frozen independent phase angles, both GR/spatial-Poisson.
- Twelve full-G192 symmetric-block/norm checks.
- Three exact symbolic identities plus independent mean/primitive scaling checks.

Largest retained errors:
- Native shifted scalar coefficient residual:4.640235e-7 absolute.
- Relative drift/remainder width or phase refinement:1.601775e-10.
- Independent remainder prediction:9.781977e-13 relative.
- Independent native scalar residual:3.444107e-7 absolute.

Numerical gate2e-5 and algebra gate1e-10 are unchanged. No failures or tolerance changes were needed in this stage.
Final audit independently reconstructs the mean, primitive, physical drift, remainder and polynomial bound from saved packets.

## Transfer theorem and next physical step
If the growth, remainder and primitive bounds hold ALONG a physical coefficient path, then with the same initial state and the periodic endpoint maps:
||u_exact-u_approx||/||u_initial||
<= (1+q)/(1-q) exp(g DeltaN) [exp(e DeltaN)-1].

This is now a usable derived statement, rather than a bound dominated by arbitrary large coordinate coefficients. The JSON files include explicitly CONDITIONAL frozen-constant illustrations; those numbers are not reported as achieved history errors.

Next: derive a uniform cold-window envelope from the analytic phase structure and the saved background tube. Use endpoint/interior evaluations as checks, not as proof of an unsampled interval. Include the background replacement budget and inverse physical endpoint maps, then transport the retained preparation for common-frame GR/spatial-Poisson comparisons.
A promising analytic route is a weighted Fourier norm: small source/metric denominators permit Neumann bounds on inverse maps, with a controlled analytic tail beyond the256-node representation. No unsourced late phase is required merely to bound that periodic endpoint correction.

## Saved work
- energy_math.py and DERIVATION.md: physical scaling and exact formulas.
- energy_operator.py: unchanged stable generator; high-precision reference is sampled every32 phases on shifted families, while every candidate phase is evaluated.
- each label/energy-01/: reused and physically transformed central banks.
- each label/drift-01/: all paired source shifts and baseline controls.
- each label/remainder-01/: drift, remainder, phase-polynomial bounds and refinement evidence.
- each label/independent-01/: frozen predictions and native/G192 controls.
- identities/result.json, audit/result.json: independent checks.
- CLEANUP.json and closeout.json: exact process receipts and complete artifact hashes.

All work stays local. Original sources and the previous checkpoint remain intact.
