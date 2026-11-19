# Analytic cold phase continuation — 2026-11-08

Previous turn: verified progress, sealed physical cold averaging remainder.
This stage keeps all original bank/grids/tolerances and baseline controls. No GitHub.
Cutoff 2026-11-08T04:30Z, less than four hours from the 00:40Z start.
One owned numerical worker/thread, below-normal CPU4; real owner holds bind.

## Constructive target
Derive the analytic phase dependence of the closed, physical relative generator.
Use the finite harmonic stress/metric numerators, not an assumed decay inferred from a sampled FFT.
Derive pole-free weighted Fourier bounds for the coordinate/metric inverses throughout the inherited cold tube.
Construct and qualify the rational operator at the cold midpoint and endpoints, for baseline/MTS and all three k.
Obtain an analytic truncation/alias bound at each coefficient state, separated from finite-precision source error and slow-jet discretization.

## Fixed checks
ALGEBRA=1e-10 and GATE=2e-5 unchanged. Use saved background and accepted native DLL only.
Eight phase nodes recover proven degree-two source numerators; held-out phases and saved256-node banks are independent checks.
Slow metric-coefficient jets use inherited fourth-order differences, widths .001 and .0005; their errors are not silently called exact derivatives.
Baseline has no heavy phase; test its phase independence and identity maps.
Full G192 tail remains; phase-dependent support is finite because the remote streaming is phase independent.

## Claim discipline
A theorem for the analytic finite-harmonic/rational source is not an interval-arithmetic certificate of native floating-point evaluation.
A midpoint/endpoints norm is not a cold-history supremum. Uniform inverse hypotheses are derived separately from the saved tube.
No late mode or microscopic phase is invented. Full history transport needs coefficient/background uncertainty and physical endpoint maps.
All failures are retained; no automatic retries or tolerance widening.
