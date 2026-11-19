# Longer coupled window: angular boundary derived and tested

Date: 2026-11-10. Status: **verified numerical progress in the retained coupled equations**. Both the cold baseline and MTS heavy case pass the final refined control. The previous failure evidence is retained, not overwritten. The overall research goal remains open.

## Scope and preserved inputs

The same controlled late-time initial-value problem now spans Delta ln(a)=0.01 instead of 0.001, from z=10 to about 9.890548, at k=5/Mpc. The physical masses, G, parent action, initial prescription, momentum-distribution normalization, four heavy canonical coordinates and original production files remain unchanged. The numerical gate is 2e-5; the algebra gate is 1e-10.

This stage regenerates the background over the extended interval; it does not extrapolate the short spline. There are 321 background positions, 641 thermal samples with independent midpoint interpolation checks, and 17 actual native regime captures per case. Regimes remain those supported by the retained late-time interface. Exact saved initial states are reused only after overlap and preparation checks.

Background solver refinement is at most 1.215e-15 in the saved normalized comparison, with 32/64-momentum difference at most 1.866e-10. Friedmann and pressure-clock residuals are at most 6.662e-16 and 6.698e-16 respectively. Complete operator overlap with the short interval agrees to at most 3.728e-16. These are internal consistency measurements, not observational precision estimates.

Sources: `background-result.json`, `thermal-regime-result.json`, `interface-result.json`, `conservative-rows-result.json` and the inherited manifest `frozen-inputs.json`.

## Failure found by widening the interval

The original angular cutoff lmax=16 with its asymptotic last-row closure is inaccurate for the newly prepared late-time streaming disturbance. Merely refining time or checking conservation would have missed this.

An independent characteristic representation of the same collisionless equation, driven by each saved coupled metric, finds the following approximately equal discrepancies in both models:

| Neutrino source | Original closure versus characteristic solution |
|---|---:|
| Density | 0.0119407 |
| Current | 0.0125494 |
| Anisotropic stress | 0.1056973 |

These are maximum differences normalized by each field's peak amplitude over the nine common-scale-factor probes, not pointwise ratios at the final epoch. The original coupled 32/64-momentum comparison also fails for several readouts; it is not promoted as converged. In contrast, passive 64/128 and 128/256 momentum integrations of the characteristic response to the **same** metric agree within 3.376e-11 and 5.192e-15. Those passive diagnostics are not new coupled 128/256-node backgrounds.

All original packets and failed comparison flags remain available in `cold64-result.json`, `heavy64-result.json`, `cold-characteristic-result.json`, `heavy-characteristic-result.json` and the original validation record.

## Repair derived from the field equations

The exact last retained hierarchy equation is

    F16' = k v (16 F15 - 17 F17)/33.

The eliminated F17 is a free-streaming term plus the causal characteristic integral of the metric sources. Its angular kernel follows from the Legendre recurrence and spherical Bessel projection, not a fit to the numerical discrepancy. See `CHARACTERISTIC-CONTRACT.md`, `ANGULAR-REPAIR-CONTRACT.md` and `ANGULAR-REPAIR-DERIVATION.md`.

We regenerate that boundary from the saved metric, evolve the **whole coupled state**, regenerate it from the new metric, and evolve again. The gravitational response, rest species and all four heavy coordinates remain coupled. This is not an observer-only correction. Appending a constant coordinate represents affine forcing within an iterate; it introduces no physical field or free coefficient.

The boundary is evaluated at the actual integration and probe times, not interpolated in the evolution. Its metric-history interpolation and time quadrature have separate controls. Generalizing the characteristic elimination gives a finite-interval linear Volterra equation. Under regular-background and bounded-kernel assumptions, its ordered-integral series converges with a factorial bound. No uniform numerical kernel bound has been computed: that conditional existence/uniqueness argument is not an error certificate for two iterations or a nonlinear/global theorem.

## Time refinement: retain the miss, then test the remedy

With the derived boundary, the 128/256-step comparison passes the physical-source checks but fails the full-state gate: maximum shared-boundary difference is about 4.94018e-5, above 2e-5. `cold-boundary-analysis-result.json`, `heavy-boundary-analysis-result.json` and `validation.json` preserve that failure.

The additional 512-step runs use the **same iteration-2 metric forcing history**, mass, background, quadrature and tolerance. The extended evaluation bank matches all 264 exactly shared old-bank points with zero floating-point difference. Only the time step changes; no new iteration or parameter adjustment is disguised as refinement.

| Final 256/512 comparison | Cold baseline | MTS heavy |
|---|---:|---:|
| Full-state difference on shared boundaries | 3.10684098e-6 | 3.10684100e-6 |
| Full-state difference at common-scale-factor probes | 2.60358169e-6 | 2.60358174e-6 |
| Largest physical-source/readout difference | 3.75943e-12 | 3.39858e-9 |
| Independent normalized metric residual | 2.33629e-10 | 2.33880e-10 |
| Algebraic identity residual | 4.27183e-16 | 1.58220e-16 |
| Supplied F17 versus final-metric reconstruction | 9.50543e-14 | 9.30996e-14 |
| Final numerical acceptance | PASS | PASS |

The state difference decreases by about 15.9, consistent with the fourth-order time scheme on this test. State differences use the frozen coordinate normalization; they are not percentages of a galaxy velocity or cosmological observable. The physical-source/readout comparison uses each field's peak amplitude separately.

Independent characteristic reconstruction from the final 512-step metric agrees with the evolved neutrino moments as follows:

| Final characteristic discrepancy | Cold baseline | MTS heavy |
|---|---:|---:|
| Density | 2.13565e-14 | 1.14561e-13 |
| Current | 3.87919e-14 | 1.98107e-13 |
| Anisotropic stress | 2.53218e-13 | 3.42055e-13 |

Time-quadrature, metric-history interpolation, streaming-phase and passive momentum checks also pass. Very small differences here are agreement between two numerical representations of the same retained equations, not a claim of thirteen-digit physical accuracy. Boundary consistency is sampled at every saved 512-step boundary; low-moment comparisons use nine probes. Neither is a uniform all-time bound.

Authoritative final evidence: `cold-refinement512-result.json`, `heavy-refinement512-result.json`, their NPZ analysis packets, the complete `closed512-*.npz` trajectories and `validation-refinement.json`. The heavy run deliberately yielded after step384, then resumed from its verified completed receipt; it was not a retry of a failed calculation.

## Physical size and approximation limits

The repaired 256-step result changes the original truncated Phi by about 5.2355e-5 of its peak, total current by about 0.0076261 and anisotropic stress by about 0.1056973. Those changes are internal numerical corrections in both models, not an improvement against observational data. The much smaller final time-refinement errors are reported separately above.

The source-ordering diagnostic from the original extended paired control remains informative. The baseline slow scalar density source has peak about 7.25971e-23 Mpc^-2, but its rate/(k times peak density) is about 1.11081 and pressure/peak density about 1.00122. It is tiny, but not uniformly slowly varying. The heavy case's combined custom source is about 8.18183e-13 Mpc^-2, with corresponding ratios 2.13107e-4 and 3.36577e-8; its pressure-rate ratio is 1.11967e-10. These are source-order diagnostics, not a complete bound on omitted radiation terms. A later restored-hierarchy comparison or derived remainder bound must justify broader use of the leading radiation approximation.

This stage repairs standard thermal-neutrino angular transport inside the retained MTS comparison. It does not derive a new MTS interaction or substitute a new theory. The W2 carrier, late heavy-background regime and leading radiation approximation retain their documented scope. The seed is a controlled late initial condition, not a primordial reconstruction, formation model or galactic occupation law. No observational fits, new data downloads or parameter calibration occurred.

## Validation, ownership and next step

The original implementation/provenance validator passes 1296 checks while explicitly recording the failed 128/256 repair. The refinement validator passes 1288 checks and separately records **both final physical reports true**. The check sets overlap; their counts are not independent discoveries and should not be added as physical evidence. Input hashes, packet chains, worker identities, unchanged code, finite states and no-bytecode conditions are checked.

`seal_stage.py` and `verify_closeout.py` seal the finished evidence and verify exact task-owned worker exits. `closeout.json` and `CLEANUP-VERIFIED.json` are the completion receipts. No other chat, application, service or worker is stopped. No GitHub action, subagent, browser operation, relay loop or Galaxy-file change occurred.

`GALAXY-UPDATE-08-RECEIPT.md` retains the separate NGC3198 handoff with attribution and its geometry limitations. Its reported observational progress does not select a parent heavy-field population.

**Next:** one independent wavelength with the same background, a properly recomputed physical seed, actual mode-specific regime checks and the derived coupled angular boundary. Then connect the prepared perturbations to the retained primordial/heavy matching history rather than polishing the same k=5 test. See `NEXT.md`.
