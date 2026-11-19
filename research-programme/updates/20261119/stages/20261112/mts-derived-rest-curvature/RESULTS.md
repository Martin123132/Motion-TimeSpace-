# Derived rest-curvature result — 12 November 2026

## Outcome

Rest curvature is now calculated from the coupled equations, including massive neutrinos, the slow scalar, actual background derivatives and the native photon/baryon equations. The original 910-row preparation/reference packets remain byte-identical for both baseline and MTS. No bank, physical grid, parameter, normalization or tolerance changed.

The conservative uniform-curvature ceiling does NOT close the MTS pressure argument: a preparation node reaches |zeta''|=.00668191679964326 versus .0035630317480616954. This is a failure of that sufficient bound, not a failure of the propagated prediction. Baseline's sampled maximum is 1.6183479953737727e-6 versus its density ceiling 812.7620592489602; that sample comparison is not a continuum proof either.

## Direct equation-derived correction

Freeze each node's quadratic rest coefficient before scoring. Reuse the previous coherent primitive evolution, signed weights, sources and linear control; run the unchanged 32/64 step checks.

| Relative error over the nine original reports | Baseline density | MTS density | MTS current | MTS pressure |
|---|---:|---:|---:|---:|
| Raw quadratic prediction | 3.44730e-10 | 7.82336e-10 | 1.92143e-11 | 2.38584e-7 |
| Including numerical working allowance | 1.01787e-9 | 1.79254e-9 | 9.44376e-10 | 1.37183e-6 |
| Unchanged gate | 2e-5 | 2e-5 | 2e-5 | 2e-5 |

All eight intervals pass for both cases; baseline dust current/pressure remain exactly zero. Raw MTS pressure discrepancy improves about 6.04 times from the saved linear result (1.44171e-6); with numerical allowance it improves from 2.57495e-6 to 1.37183e-6. This is an exposed numerical comparison, not a new observational test.

Final MTS quadratic-minus-linear changes (density,current,pressure):

    (3.4170399149102693e-10, 4.137142017857087e-12, 3.053629067271621e-10).

Independent signed adjoint response reproduces those changes within the explicit integration/arithmetic allowance. The actual effect is much smaller than the maximum-node sufficient envelope can establish; signed preparation and response weights matter.

## Why this advances the next step

The largest curvature is dominated by two specifically identified terms: heavy-background denominator curvature and the live heavy current feeding eta_k. DERIVATION.md derives an enlarged (u,w,eta_k) system that keeps both responses live. The source readout already contains the remaining-sector density/current and derivatives needed to initialize and test it. No new galaxy or local coupling is introduced.

The quadratic coefficient is a local expansion, not a bound on all later rest curvature. Do not promote this result to a certified continuous uniform remainder estimate. The next stage should test the live metric-state formulation rather than fit a cutoff, loosen the pressure gate, or choose a convenient rest interpolant.

## Reproducibility and scope

146 baseline and 683 MTS capture/reconstruction checks pass, including original-output parity, native continuity equations, component sums, and independent scalar second derivatives. Eleven independent high-precision identity controls pass. Final reconstruction and enlarged-system initial RHS checks are in validation.json.

ATTEMPT-01.md preserves one failed added diagnostic and its repair: the continuity identity needed the same native force representation near a zero, not a tolerance change. Both native builds, logs and receipts remain saved. No earlier checkpoint was modified. No new observations, fits, publication, browser handoff or other-chat changes. Goal remains paused; task-owned processes are checked in CLEANUP-VERIFIED.json.
