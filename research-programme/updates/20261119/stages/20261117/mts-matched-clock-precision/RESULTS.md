# Matched clock, radiation energy and photon–baryon continuity | 17 November 2026

The expansion correction is reproducible for a fixed initial preparation. On the original four MTS cells, the radiation result also survives deriving the photon density from continuity instead of supplying its saved interior values. That replacement alone does **not** resolve the much smaller baseline signal. The saved baseline density and relative motion already disagree inside every tested interval.

## What was held fixed

The physical restart remains epoch 4252 in `../mts-carried-defect-budget-20261117/`. This stage is a diagnostic branch, not its replacement. Both resolutions retain their own initial perturbations; no state is tuned, no extra energy-transfer or gravity parameter is introduced, and no observational data are used. Numerical gate: 2e-5; algebra gate: 1e-10. “Four cells” means four original intervals per branch, not four independent experiments or the full history.

## Rebuilding the clock

Start before the saved late history, at the original matched scale and scalar fields. Evolve the same flat positive Friedmann branch in both scale and log-scale coordinates; subtract the reference scale only after extended-precision evolution. All original clock/field boundaries, all 3,615 baseline and 7,855 MTS saved times, and all radiation probes were reused. The analytic dust-plus-radiation control agrees to better than 6e-33 in scale. See `CONTRACT.md`, `clock-precision.json` and the two integration reports.

Changing step size alters the scale correction by at most 1.46e-16 (baseline) or 1.45e-13 (MTS), relative to the peak correction for the **same** binary matched state. The baseline correction itself peaks at only 2.71e-15. Initializing instead on the smooth interpretation shifts it by 2.38% of that small correction; evaluating a common trajectory against the two represented reference scales differs by 18.26% of the smooth peak correction. These are sensitivity to input conventions, **not** percent changes to cosmic expansion.

## Radiation and the missing baseline accuracy

| Branch | Cells | Matched-clock radiation working allowance, relative to its own signal | Derive photon density: radiation budget against native reference |
|---|---|---:|---:|
| Baseline | 892, 3112, 1204, 2409 | 0.89%–7.33% | 1.79%–14.80%; 0/4 pass |
| MTS parent | 96, 5264, 2618, 5236 | 1.20e-7–4.75e-7 | 2.39e-7–6.75e-7; 4/4 pass |
| MTS approximation | same four MTS cells | 1.38e-7–5.10e-7 | 2.75e-7–7.45e-7; 4/4 pass |

The last column is deliberately stricter: it includes comparison against both archived resolutions as well as numerical refinement. See `radiation-comparison.csv`, `two-momenta.json`, and `monopole-result.json` for separate budgets. Raw changes are conditional on this saved mode, not fitted sky amplitudes. An unresolved baseline cannot support a comparative physics claim.

The exact drag propagator distinguishes an inherited slip from fresh forcing. At baseline cell 892 less than 1.31e-84 of the entering **resolution difference** can be attributed to direct survival of the earliest saved slip difference with other sources fixed. Feedback through the other fields is not bounded by this statement. The joint baryon–photon momentum equations cancel internal collision momentum; the relative, rather than common, velocity accounts for over 99.9% of the conditional baseline energy shift when swapping the left states. On each cell the photon density contributes about 104%, 99%, 87% and 74% of the signed newly required resolution difference. These are a force decomposition, not probabilities: quadrupole and other forces can oppose it, and 1.3–7.0% in absolute terms is unaccounted for. See `MEMORY.md`, `TWO-MOMENTA.md`, `drag-memory.json`, and `drive-balance.json`.

## A control that does not depend on the metric source

With photon velocity defined as 3q_gamma/4 and slip s = v_b - 3q_gamma/4, the native continuity equations give, for each mode,

    (delta_gamma - 4 delta_b/3)' = 4 k s/3 .

The same identity holds for the finite changed-minus-original quantities. Its integral compares **two distinct pieces of saved data** (densities and velocities); the common synchronous metric term cancels. Normalization is by the integral of the absolute changed slip times 4k/3, not by a near-zero signed endpoint. On the finer baseline trajectory, discrepancy divided by this scale is 0.421, 1.069, 1.947 and 2.433, against numerical allowances of 5.43e-7 to 1.80e-6. An independent 65-decimal calculation on the original, slightly nonuniform times tests 32 partial integrals per cell at both resolutions. Baseline passes 0/256; MTS parent passes 256/256 and its approximation 256/256. These are nested checks, not independent trials. See `relative-entropy.json` and `interior-balance.json`.

As a constructive test, `monopole.py` integrates the slip with both momenta and recovers the photon density from the left photon density, the baryon-density increment, and the integrated slip. It does not supply the tested changed photon density from the interior. It still inherits the saved baryon density, quadrupole, old photon drive and both left perturbation states. It preserves the four parent radiation comparisons but does not make the baseline converge. The native implementation contains a subtraction of two separately rounded right-hand sides; this is a candidate source of error, not proved to be the sole one.

## Next calculation

From the *original* matched perturbations, use cold dark matter (CDM) as a shared density reference: (delta_b - delta_c)' = -k v_b and (delta_gamma - 4 delta_c/3)' = -k q_gamma. Evolve their finite differences with the two momenta and one common metric source, instead of subtracting three individually rounded native continuity rows. Include the independently derived finite expansion correction and retain the pressure and quadrupole feedback. Compare the reconstructed native rows at identical states before testing an early matched interval and the existing radiation cells; an imposed identity alone is not a prediction. Do not overwrite the 4252 history or promote the integrated spectrum on these local checks.
