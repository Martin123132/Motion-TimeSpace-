# Integrated correction: source match improves, remainder uncertainty unresolved

## What advanced

The derived background-defect correction is now integrated through the original background rather than frozen as a constant curvature. Its coefficients are equation-owned, not fitted. Exact native clock/background exports reproduce the previous prepared values; all original fields, grids, bank, masses, coupling and tolerances are unchanged. Quadrature and integration-by-parts controls pass.

Frozen predictions were scored only after their inputs/results were saved. These reference data were already exposed in earlier work; no observational holdout claim is made.

| Maximum relative source discrepancy | Cold baseline | Heavy MTS |
|---|---:|---:|
| Density | 3.4471e-10 | 2.5449e-9 |
| Current | exactly zero | 1.9377e-9 |
| Pressure | exactly zero | 2.0205e-6 |

All raw source discrepancies pass2e-5 over all eight intervals. The heavy pressure discrepancy is about22.8times smaller than the preceding constant-curvature result4.6102e-5. The first-order previously accepted result and rejected quadratic result remain unchanged.

## Acceptance is not inferred from the small residual alone

The primary prediction freezes the remaining curvature R. Its predeclared6/8-knot variation estimates are unstable for heavy pressure: their propagated discrepancy is7.00845e-8, or2.76132e-4 relative. The larger variation allowance is1.25359e-7. Including this working allowance gives4.97203e-4 relative, so the primary paired uncertainty gate is NOT passed. Cold passes; heavy density/current pass. The inferred cubic variants are diagnostic failures, not fitted repairs.

The direct remainder-integral follow-up preserves that primary verdict. It uses the original910 reference epochs (902preparation plus8continuation), with the first902readout rows bit-identical. No new physical grids or long evolution are introduced. Its final signed pressure variation estimates are:

- natural cubic: +1.182223144206145e-9;
- PCHIP: -9.738083345909504e-9;
- piecewise linear: +5.086070461955921e-10.

The natural-cubic estimate alone lies inside the gate, but that is not sufficient. Their absolute-weighted representation envelope reaches6.43171e-5 in pressure source units (0.2534relative); current's envelope also fails its gate. This is a conservative finite representation-sensitivity diagnostic, NOT a measured25%physical error, a certified bound or evidence of a25%model failure. Strong cancellation prevents these interpolants from establishing the necessary remainder accuracy. No convenient interpolant is selected and no result is promoted on the basis of the smallest discrepancy.

## Best next step

DERIVATION.md reduces the existing constraint to a coupled primitive pair with time-dependent background and live scalar self-gravity. Test a frozen first-order rest expansion from its already-derived initial value/rate, then form the source and weighted sum from the coherently propagated primitives. This targets the cancellation problem directly instead of adding another noisy derivative or changing the tolerance. It remains an approximate local rest closure to test, not the full hierarchy.

The stage leaves a genuinely improved no-fit source prediction and a specific unresolved error-control issue. It does not silently turn numerical uncertainty into a physical rejection or an accepted full-window error bound.

Everything stays private/local; the goal remains paused. REPAIR.md records one list/array plumbing error in the first diagnostic attempt, which produced no scientific result; its failed receipts remain intact. Cleanup verifies the task-owned worker identities, compiler children and old source hashes, preserving all other chats and services.
