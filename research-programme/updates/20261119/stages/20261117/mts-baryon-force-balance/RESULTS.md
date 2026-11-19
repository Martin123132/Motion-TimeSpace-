# Accumulated baryon force balance — 17 November 2026

## Result

Both baseline and MTS pass the original 2e-5 full native-velocity tolerance,
including the frozen working sampling, rounding and 32/64 evolution allowances.
The force terms were integrated from saved pressure and photon/baryon moments;
the endpoint baryon velocity was reserved for checking the result, not used to
set interpolation slopes. No scattering bank, grid, parameter, or tolerance changed.

| Case | Old full balance, relative to reference | Coherent full balance | Correction-relative check |
|---|---:|---:|---|
| Baseline (cold) | 3.31701e-7 | 3.31702e-7 | unresolved |
| MTS (heavy) | 5.61324e-7 | 5.60870e-7 | 8.17297e-4; fails 2e-5 |

These relative balances include residual plus estimated numerical allowance.
They are not likelihoods, observational errors, or uniform mathematical bounds.

The MTS final native velocity-transfer correction independently reconstructed
from integrated forces is about -1.01180361e-7, versus the canonical saved
-1.01281235e-7. Their difference is 1.00874e-10, about 0.10% of this endpoint
correction. Across the whole window, correction residual plus working allowance
is 2.52397e-10, or 0.08173% of its maximum amplitude. It therefore passes the
full-output budget but not 0.002% precision relative to the tiny correction itself.
The baseline correction is much smaller than the conservative arithmetic
envelope and is not resolved; its reconstructed sign must not be interpreted.

## What produces the MTS response?

Derived finite-difference decomposition of the final transfer correction:

| Contribution | Transfer change |
|---|---:|
| Integrated pressure change | +1.27357e-15 |
| Integrated photon-drag change | +1.31234804e-7 |
| Removed old background contact | -1.24673e-10 |
| Initial matched momentum change | 0 |
| Scale-factor normalization | +2.87334e-10 |
| Metric endpoint change | -2.32528708e-7 |
| H normalization | -4.91203e-11 |

Photon-drag evolution and the metric endpoint supply the large opposing terms.
This is not mainly a change of H normalization. Pressure is small in this
particular window, not generally absent from the theory.

Deleting photon drag, the metric endpoint, or the matched initial contribution
is detected for both cases. Deleting pressure alone is not detected at the broad
full-output tolerance; the coherent background contact vanishes by construction
of the consistent background. An insensitive omission test is not called a
successful detection or permission to delete a physical term.

## Saved-support qualifications

Each case uses 29,766 unique saved times on its inherited approximately
1.15594-Mpc conformal-time interval, not 902 independently reset universes.
Original corner metadata identify 297 baseline and 732 MTS corners.
Corner-spanning unsampled gaps occupy 18.97% and 39.92% of the interval,
respectively. They use explicit linear bridges; sampled smooth regions use
piecewise PCHIP primitives. Stride4/2/1 refinements retain corner neighbours,
and a separate fine trapezoid comparison is included. Underlying 32/64
evolution histories are also compared.

The shared cross-corner interpolation error cannot be rigorously bounded by
decimation alone. Actual velocity endpoint closure independently checks the
sum over the saved interval. No rigorous between-sample remainder or separately
validated accuracy for every cancelling force term is claimed.

The native transfer convention is -k(v_b+sigma)/H with k=5 Mpc^-1.
The metric endpoint comes from the supplied coherent/old metric histories.
This is conditional force-balance verification, not an independent gravitational
forecast, new observational fit, frequency-resolved distortion spectrum, or
complete sky prediction. Keep quantum-measure questions separate.

The old full source-pressure budget of 87.5966% remains inherited; this stage
does not silently reinterpret it as a propagated uncertainty for all observables.
Previous response-relative failures and finite-neutrino qualifications remain.

## Verification and reproducibility

- Four symbolic identities, including Thomson momentum exchange.
- Manufactured constant/linear integration controls, including an unsampled corner.
- Native Euler identities and stable quotient/product comparisons at 1e-10.
- Exact repeated arrays and reports for both models.
- Canonical earlier transfer comparison, exact trapezoid-map check, and omission controls.
- 45 verification checks pass; the two scientific correction-relative gates remain false.
- Prior sealed inputs checked before and after; no previous checkpoint overwritten.
- One bounded, single-thread, below-normal worker at a time, no continuing worker.

Authoritative files in this directory: protocol.json, DERIVATION.md,
frozen-reference.json, cold-result.json, heavy-result.json, verification.json,
cold-balance.npz, heavy-balance.npz. Code: run_balance.py and verify_balance.py.
Source roots are absolute in protocol.json and inputs.json. Existing native
equations.f90:2458 and original integrated_math.py supply the Euler law and
interpolation-corner definitions, respectively.

